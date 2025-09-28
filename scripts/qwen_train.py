import os
os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"
os.environ["TORCH_DIST_DISABLE_TENSOR"] = "1"     # 禁用 DTensor 分布式 tensor
os.environ["TORCH_DISTRIBUTED_USE_DTENSOR"] = "0"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
import torch
import os

local_rank = int(os.environ.get("LOCAL_RANK", 0))
torch.cuda.set_device(local_rank)
print(f"[Rank {local_rank}] Using CUDA device: {torch.cuda.current_device()}")

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch
from transformers import TrainingArguments
from trl import SFTTrainer
from accelerate import infer_auto_device_map
from accelerate.utils import get_balanced_memory

print("./new_final_data_train3.jsonl")
dataset = load_dataset("json", data_files="./new_final_data_train3.jsonl")
print("Qwen/Qwen1.5-7B-Chat")
model_name = "Qwen/Qwen1.5-7B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_prompt(example):
    prompt = example["prompt"]
    label = example["label"]

    prompt_tokens = tokenizer(prompt, truncation=True, max_length=2048)
    label_tokens = tokenizer(label, truncation=True, max_length=2048)
    prompt_ids = prompt_tokens["input_ids"]
    label_ids = label_tokens["input_ids"]

    input_ids = prompt_ids + label_ids
    input_ids = input_ids[:4096]

    labels = [-100] * len(prompt_ids) + label_ids
    labels = labels[:4096]

    return {
        "input_ids": input_ids,
        "labels": labels,
        "attention_mask": [1] * len(input_ids)
    }
tokenized_dataset = dataset["train"].map(tokenize_prompt, remove_columns=dataset["train"].column_names)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,  # 或 torch.float16
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    trust_remote_code=True,
    offload_folder="offload"
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir="./qwen_7B/output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    num_train_epochs=3,
    logging_steps=5,
    save_steps=80,
    report_to="none",
    run_name="qwen_lora",
    learning_rate=2e-4,
    bf16=True,
    deepspeed="./ds_config_zero2.json",
)

trainer = SFTTrainer(
    model=model,
    train_dataset=tokenized_dataset,
    args=training_args,
)
print("Model device:", next(model.parameters()).device)
trainer.train()
trainer.save_model()