import re
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
# import sys
# sys.stdout = open("output_log.txt", "w", encoding="utf-8")

base_model_path = "Qwen/Qwen2.5-7B-Instruct"
lora_model_path = "./qwen_7B/output"
print(lora_model_path,base_model_path)
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    quantization_config=bnb_config,
    trust_remote_code=True,
    device_map="auto",
)

model = PeftModel.from_pretrained(base_model, lora_model_path)
model.eval()
print("./new_final_data_test3_rule.jsonl")
test_dataset = load_dataset("json", data_files="./new_final_data_test3_rule.jsonl")["train"]

def extract_label(text: str) -> str:
    match = re.search(r"Label:\s*(Yes|No)", text, re.IGNORECASE)
    return match.group(1).capitalize() if match else "Unknown"

correct = 0
total = 0

for sample in test_dataset:
    prompt = sample["prompt"]
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=2048).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.pad_token_id
        )

    input_len = inputs["input_ids"].shape[1]
    gen_text = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    pred_label = extract_label(gen_text)
    true_label = "Yes" if "Label: Yes" in sample["label"] else "No"

    total += 1
    correct += int(pred_label == true_label)

    # print("output_text", "---" * 10, "\n", output_text)
    print(f"pred: {pred_label}, true: {true_label}")
    print(f"total: {total}, correct: {correct}")

print(f"\nAccuracy: {correct/total:.2%} ({correct}/{total})")
