import json


def convert_teacher_to_student(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line in infile:
            data = json.loads(line.strip())

            # 拼接函数内容
            functions_text = "\n".join(data["functions"])

            # 规则部分拼接（可选）
            rule = data.get("rule", {})
            if rule:
                rule_text = f"Cause: {rule.get('cause', '')} Impact: {rule.get('impact', '')} Recommendation: {rule.get('recommendation', '')}"
            else:
                rule_text = ""

            # 构建格式2的 JSON 对象
            converted = {
                "instruction": "You are a smart contract auditor. Analyze the functions below and determine whether a vulnerability exists. Provide your reasoning and final answer.",
                "input": f"=== Smart Contract Functions ===\n{functions_text}\n\n=== Rule (if any) ===\n{rule_text}",
                "output": f"CoT: {data['CoT']}\nLabel: {data['label']}"
            }

            # 写入新文件
            outfile.write(json.dumps(converted, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    # 示例用法
    convert_teacher_to_student("../lm_teacher/output/data.jsonl", "./train_data/sft_data.jsonl")
