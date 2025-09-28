import re
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import pandas as pd

results = []

base_model_path = "Qwen/Qwen1.5-7B-Chat"
lora_model_path = "./qwen_7B/output"
print(lora_model_path, base_model_path)

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
print("./test_data_final2.jsonl")
test_dataset = load_dataset("json", data_files="./test_data_final2.jsonl")["train"]

def extract_label(text: str) -> str:
    match = re.search(r"Label:\s*(Yes|No)", text, re.IGNORECASE)
    return match.group(1).capitalize() if match else "Unknown"

tp = fp = tn = fn = 0
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
    correct_flag = int(pred_label == true_label)
    correct += correct_flag

    if pred_label == "Yes" and true_label == "Yes":
        tp += 1
    elif pred_label == "Yes" and true_label == "No":
        fp += 1
    elif pred_label == "No" and true_label == "No":
        tn += 1
    elif pred_label == "No" and true_label == "Yes":
        fn += 1

    print(f"pred: {pred_label}, true: {true_label}")
    print(f"total: {total}, correct: {correct}")
    results.append({
        "prompt": prompt,
        "true_label": true_label,
        "pred_label": pred_label,
        "is_correct": correct_flag,
        "gen_text": gen_text.strip()
    })

df = pd.DataFrame(results)
df.to_csv("prediction_results.csv", index=False, encoding="utf-8")

accuracy = correct / total if total > 0 else 0
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print("\nEvaluation Results:")
print(f"Accuracy : {accuracy:.2%} ({correct}/{total})")
print(f"Precision: {precision:.2%}")
print(f"Recall   : {recall:.2%}")
print(f"F1-score : {f1:.2%}")
print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
print("prediction_results.csv get")