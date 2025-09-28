import json

def flatten_rule(rule_obj):
    if isinstance(rule_obj, str):
        return rule_obj.strip()
    elif isinstance(rule_obj, dict):
        parts = []
        if "cause" in rule_obj:
            parts.append(f"Cause: {rule_obj['cause']}")
        if "impact" in rule_obj:
            parts.append(f"Impact: {rule_obj['impact']}")
        if "recommendation" in rule_obj:
            parts.append(f"Recommendation: {rule_obj['recommendation']}")
        return " ".join(parts)
    else:
        return ""

# def convert_to_sft_format(item):
#     functions = "\n".join(item["functions"])
#     rule_text = flatten_rule(item.get("rule", ""))
#     return {
#         "instruction": "You are a smart contract auditor. Analyze the functions below and determine whether a vulnerability exists. Provide your reasoning and final answer.",
#         "input": f"=== Smart Contract Functions ===\n{functions}\n\n=== Rule (if any) ===\n{rule_text}",
#         "output": f"Label: {item['label']}\nCoT: {item['CoT']}"
#     }

# def convert_all_templates(item):
#     functions = "\n".join(item["functions"])
#     cot = item["CoT"].strip()
#     label = item["label"]
#
#     templates = [
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are a smart contract auditor. Analyze the functions below step-by-step and conclude if a vulnerability exists.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"### Smart Contract Functions ###\n{functions}\n\n"
#                 "### Task ###\n"
#                 "1. Identify function behavior\n"
#                 "2. Analyze critical operations (permission checks, state changes, external calls)\n"
#                 "3. Evaluate input validation and trust assumptions\n"
#                 "4. Conclude vulnerability presence\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are a security expert. The user provides contract logic and requests a structured vulnerability analysis.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "User provided smart contract code for review:\n"
#                 f"{functions}\n\n"
#                 "Please:\n"
#                 "- Describe function purpose\n"
#                 "- Note unsafe inputs/trust assumptions\n"
#                 "- Walk step-by-step logic\n"
#                 "- State final verdict Yes/No\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are reviewing smart contract safety. Provide detailed reasoning and a yes/no outcome.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"{functions}\n\n"
#                 "Questions to address:\n"
#                 "1. What does each function do?\n"
#                 "2. Are there missing checks or unsafe interactions?\n"
#                 "3. What is your step-by-step reasoning?\n"
#                 "4. Final vulnerability verdict?\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You act as a smart contract auditor. Examine the functions and identify any security issues, explaining your thought process.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "Functions under review:\n"
#                 f"{functions}\n\n"
#                 "Please provide:\n"
#                 "- Description of critical logic\n"
#                 "- Step-by-step vulnerability analysis (CoT)\n"
#                 "- Final answer yes or no\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#     ]
#     return templates

# def convert_all_templates(item):
#     functions = "\n".join(item["functions"])
#     cot = item["CoT"].strip()
#     label = item["label"]
#
#     templates = [
#
#         {
#             "instruction": "You are a smart contract security auditor. Use the 5-step structure below to determine if a vulnerability exists.",
#             "input": (
#                 f"=== Smart Contract Functions ===\n{functions}\n\n"
#                 "=== Task ===\n"
#                 "1. Summarize what each function does (Step 1)\n"
#                 "2. Identify security-relevant operations (Step 2)\n"
#                 "3. State assumptions made by the contract (Step 3)\n"
#                 "4. Check how each assumption is enforced (Step 4)\n"
#                 "5. Decide if a vulnerability exists and explain why (Step 5)"
#             ),
#             "output": f"<｜begin▁of▁sentence｜>\nCoT: {cot}\n\nLabel:{label}\n<|EOT|>"
#         },
#
#         {
#             "instruction": "You are a smart contract security expert. Review the code and determine if it is vulnerable.",
#             "input": (
#                 f"Smart contract under review:\n{functions}\n\n"
#                 "Your report must contain:\n"
#                 "- Purpose of each function\n"
#                 "- Security-critical operations\n"
#                 "- Assumptions and enforcement\n"
#                 "- Whether a vulnerability exists\n\n"
#                 "Conclude with:\nLabel: Yes or Label: No"
#             ),
#             "output": f"<｜begin▁of▁sentence｜>\nCoT: {cot}\n\nLabel:{label}\n<|EOT|>"
#         },
#
#         {
#             "instruction": "You are an attacker analyzing this smart contract for potential exploits.",
#             "input": (
#                 f"Target smart contract code:\n{functions}\n\n"
#                 "Answer the following:\n"
#                 "1. What is the purpose of each function?\n"
#                 "2. Are there any assumptions that, if broken, can be exploited?\n"
#                 "3. Can you describe a potential exploit path?\n\n"
#                 "Answer:\nLabel: Yes or No and explain why."
#             ),
#             "output": f"<｜begin▁of▁sentence｜>\nCoT: {cot}\n\nLabel:{label}\n<|EOT|>"
#         },
#
#         {
#             "instruction": "You are auditing smart contract functions. Follow the thought process to determine whether a vulnerability exists.",
#             "input": (
#                 f"Functions to analyze:\n{functions}\n\n"
#                 "Start reasoning step-by-step:\n"
#                 "- Step 1: What do the functions do?\n"
#                 "- Step 2: What are the critical operations?\n"
#                 "- Step 3: What assumptions are being made?\n"
#                 "- Step 4: Are the assumptions enforced?\n"
#                 "- Step 5: Final verdict?\n\n"
#                 "Please end with:\nLabel: Yes or No"
#             ),
#             "output": f"<｜begin▁of▁sentence｜>\nCoT: {cot}\n\nLabel:{label}\n<|EOT|>"
#         },
#     ]
#
#     return templates

# ----------------------------------------------------------qwen COt-label------------------------------------
# def convert_all_templates_qwen(item):
#     functions = "\n".join(item["functions"])
#     cot = item["CoT"].strip()
#     label = item["label"]
#
#     templates = []
#
#     system_prompt = (
#         "You are a smart contract security expert. Analyze the contract below step-by-step "
#         "to determine if it contains a vulnerability using a structured reasoning process."
#     )
#
#     user_templates = [
#         (
#             "You are a smart contract security auditor. Use the 5-step structure below to determine if a vulnerability exists.",
#             f"=== Smart Contract Functions ===\n{functions}\n\n"
#             "=== Task ===\n"
#             "1. Summarize what each function does (Step 1)\n"
#             "2. Identify security-relevant operations (Step 2)\n"
#             "3. State assumptions made by the contract (Step 3)\n"
#             "4. Check how each assumption is enforced (Step 4)\n"
#             "5. Decide if a vulnerability exists and explain why (Step 5)"
#         ),
#         (
#             "You are a smart contract security expert. Review the code and determine if it is vulnerable.",
#             f"Smart contract under review:\n{functions}\n\n"
#             "Your report must contain:\n"
#             "- Purpose of each function\n"
#             "- Security-critical operations\n"
#             "- Assumptions and enforcement\n"
#             "- Whether a vulnerability exists\n\n"
#             "Conclude with:\nLabel: Yes or Label: No"
#         ),
#         (
#             "You are an attacker analyzing this smart contract for potential exploits.",
#             f"Target smart contract code:\n{functions}\n\n"
#             "Answer the following:\n"
#             "1. What is the purpose of each function?\n"
#             "2. Are there any assumptions that, if broken, can be exploited?\n"
#             "3. Can you describe a potential exploit path?\n\n"
#             "Answer:\nLabel: Yes or No and explain why."
#         ),
#         (
#             "You are auditing smart contract functions. Follow the thought process to determine whether a vulnerability exists.",
#             f"Functions to analyze:\n{functions}\n\n"
#             "Start reasoning step-by-step:\n"
#             "- Step 1: What do the functions do?\n"
#             "- Step 2: What are the critical operations?\n"
#             "- Step 3: What assumptions are being made?\n"
#             "- Step 4: Are the assumptions enforced?\n"
#             "- Step 5: Final verdict?\n\n"
#             "Please end with:\nLabel: Yes or No"
#         ),
#     ]
#
#     for inst, input_text in user_templates:
#         prompt = (
#             f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
#             f"<|im_start|>user\n{inst}\n\n{input_text}<|im_end|>\n"
#             f"<|im_start|>assistant\n"
#         )
#
#         full_label = f"{cot}\n\nLabel: {label}"
#         templates.append({
#             "prompt": prompt,
#             "label": full_label
#         })
#
#     return templates

# ----------------------Good--------------------------------
def convert_all_templates_qwen(item):
    functions = "\n".join(item["functions"])
    cot = item["CoT"].strip()
    label = item["label"]

    templates = []

    system_prompt = (
        "You are a smart contract security expert. Analyze the contract below step-by-step "
        "to determine if it contains a vulnerability using a structured reasoning process."
    )

    user_templates = [
        (
            "You are a smart contract security auditor. Use the 5-step structure below to determine if a vulnerability exists.",
            f"=== Smart Contract Functions ===\n{functions}\n\n"
            "=== Task ===\n"
            "First give the final vulnerability label (Label: Yes or Label: No)"
            "- Then provide reasoning using the following 5 steps:\n"
            "1. Summarize what each function does (Step 1)\n"
            "2. Identify security-relevant operations (Step 2)\n"
            "3. State assumptions made by the contract (Step 3)\n"
            "4. Check how each assumption is enforced (Step 4)\n"
            "5. Decide if a vulnerability exists and explain why (Step 5)"
        ),
        (
            "You are a smart contract security expert. Review the code and determine if it is vulnerable.",
            f"Smart contract under review:\n{functions}\n\n"
            "Your output must follow this format:\n"
            "- First state: Label: Yes or Label: No\n"
            "- Then provide reasoning using the following 5 steps:\n"
            "  - Step 1: Behavior Summary\n"
            "  - Step 2: Security-Critical Logic\n"
            "  - Step 3: Assumptions\n"
            "  - Step 4: Assumption Enforcement\n"
            "  - Step 5: Vulnerability Conclusion"
        ),
        (
            "You are an attacker analyzing this smart contract for potential exploits.",
            f"Target smart contract code:\n{functions}\n\n"
            "Your output must follow this structure:\n"
            "- First write: Label: Yes or Label: No\n"
            "- Then reason step-by-step:\n"
            "  - Step 1: Behavior Summary\n"
            "  - Step 2: Security-Critical Logic\n"
            "  - Step 3: Assumptions\n"
            "  - Step 4: Assumption Enforcement\n"
            "  - Step 5: Vulnerability Conclusion"
        ),
        (
            "You are auditing smart contract functions. Follow the thought process to determine whether a vulnerability exists.",
            f"Functions to analyze:\n{functions}\n\n"
            "Start with:\nLabel: Yes or Label: No\n\n"
            "Then reason step-by-step:\n"
            "- Step 1: What do the functions do?\n"
            "- Step 2: What are the critical operations?\n"
            "- Step 3: What assumptions are being made?\n"
            "- Step 4: Are the assumptions enforced?\n"
            "- Step 5: Final explanation of the vulnerability decision"
        ),
    ]

    for inst, input_text in user_templates:
        prompt = (
            f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
            f"<|im_start|>user\n{inst}\n\n{input_text}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        full_label = f"Label: {label}\n\nReason:{cot}"
        templates.append({
            "prompt": prompt,
            "label": full_label
        })

    return templates

# def convert_all_templates(item):
#     functions = "\n".join(item["functions"])
#     cot = item["CoT"].strip()
#     label = item["label"]
#
#     templates = [
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are a smart contract security expert. Use a structured 5-step process to determine if the following code contains a vulnerability.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"### Smart Contract Functions ###\n{functions}\n\n"
#                 "### Task ###\n"
#                 "- First output: Label: Yes or Label: No\n"
#                 "- Then follow the 5-step reasoning format:\n"
#                 "  1. Behavior Summary\n"
#                 "  2. Security-Critical Logic\n"
#                 "  3. Assumptions\n"
#                 "  4. Assumption Enforcement\n"
#                 "  5. Vulnerability Conclusion\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are a smart contract vulnerability auditor. Carefully analyze the contract and provide a structured diagnosis.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"=== Contract Code ===\n{functions}\n\n"
#                 "Follow these steps:\n"
#                 "- Step 1: Describe function behavior\n"
#                 "- Step 2: Identify critical operations\n"
#                 "- Step 3: List key assumptions\n"
#                 "- Step 4: Check if assumptions are enforced\n"
#                 "- Step 5: Conclude if there's a vulnerability\n"
#                 "Finally, state: Label: Yes or Label: No\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are a blockchain security analyst. Evaluate the provided smart contract logic step-by-step to detect vulnerabilities.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"{functions}\n\n"
#                 "Your analysis must:\n"
#                 "- Begin with: Label: Yes or Label: No\n"
#                 "- Then answer:\n"
#                 "  1. What does the contract do?\n"
#                 "  2. What critical operations are involved?\n"
#                 "  3. What assumptions are made?\n"
#                 "  4. Are they enforced?\n"
#                 "  5. Why does (or doesn't) this cause a vulnerability?\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#
#         {
#             "instruction": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 "You are analyzing smart contract functions for potential exploits. Provide a conclusive label and structured justification.\n"
#                 "<|EOT|>"
#             ),
#             "input": (
#                 "<｜begin▁of▁sentence｜>\nassistant\n"
#                 f"Functions to review:\n{functions}\n\n"
#                 "Respond using this structure:\n"
#                 "- Label: Yes or Label: No\n"
#                 "- Step-by-step reasoning:\n"
#                 "  Step 1: Behavior Summary\n"
#                 "  Step 2: Security-Critical Logic\n"
#                 "  Step 3: Assumptions\n"
#                 "  Step 4: Assumption Enforcement\n"
#                 "  Step 5: Vulnerability Conclusion\n"
#                 "<|EOT|>"
#             ),
#             "output": (
#                 f"<｜begin▁of▁sentence｜>\nLabel:{label}\n\n"
#                 f"Reason: {cot}\n"
#                 "<|EOT|>"
#             )
#         },
#     ]
#     return templates
# def convert_all_templates_codellama(item):
#     functions = "\n".join(item["functions"])
#     cot = item["CoT"].strip()
#     label = item["label"]
#
#     templates = []
#
#     base_templates = [
#         (
#             "You are a smart contract security expert. Use a structured 5-step process to determine if the following code contains a vulnerability.",
#             f"### Smart Contract Functions ###\n<code>\n{functions}\n</code>\n\n"
#             "### Task ###\n"
#             "- First output: Label: Yes or Label: No\n"
#             "- Then follow the 5-step reasoning format:\n"
#             "  1. Behavior Summary\n"
#             "  2. Security-Critical Logic\n"
#             "  3. Assumptions\n"
#             "  4. Assumption Enforcement\n"
#             "  5. Vulnerability Conclusion"
#         ),
#         (
#             "You are a smart contract vulnerability auditor. Carefully analyze the contract and provide a structured diagnosis.",
#             f"=== Contract Code ===\n<code>\n{functions}\n</code>\n\n"
#             "Follow these steps:\n"
#             "- Step 1: Describe function behavior\n"
#             "- Step 2: Identify critical operations\n"
#             "- Step 3: List key assumptions\n"
#             "- Step 4: Check if assumptions are enforced\n"
#             "- Step 5: Conclude if there's a vulnerability\n"
#             "Finally, state: Label: Yes or Label: No"
#         ),
#         (
#             "You are a blockchain security analyst. Evaluate the provided smart contract logic step-by-step to detect vulnerabilities.",
#             f"<code>\n{functions}\n</code>\n\n"
#             "Your analysis must:\n"
#             "- Begin with: Label: Yes or Label: No\n"
#             "- Then answer:\n"
#             "  1. What does the contract do?\n"
#             "  2. What critical operations are involved?\n"
#             "  3. What assumptions are made?\n"
#             "  4. Are they enforced?\n"
#             "  5. Why does (or doesn't) this cause a vulnerability?"
#         ),
#         (
#             "You are analyzing smart contract functions for potential exploits. Provide a conclusive label and structured justification.",
#             f"Functions to review:\n<code>\n{functions}\n</code>\n\n"
#             "Respond using this structure:\n"
#             "- Label: Yes or Label: No\n"
#             "- Step-by-step reasoning:\n"
#             "  Step 1: Behavior Summary\n"
#             "  Step 2: Security-Critical Logic\n"
#             "  Step 3: Assumptions\n"
#             "  Step 4: Assumption Enforcement\n"
#             "  Step 5: Vulnerability Conclusion"
#         )
#     ]
#
#     for system_inst, user_input in base_templates:
#         prompt = (
#             f"<s>[INST] <<SYS>>\n{system_inst}\n<</SYS>>\n\n{user_input}\n[/INST]"
#         )
#
#         full_label = f"Label:{label}\n\nReason: {cot}</s>"
#
#         templates.append({
#             "prompt": prompt,
#             "label": full_label
#         })
#
#     return templates

# with open("data.jsonl", "r", encoding="utf-8") as f, open("sft_data1.jsonl", "w", encoding="utf-8") as out_f:
#     for line in f:
#         item = json.loads(line)
#         converted = convert_to_sft_format(item)
#         out_f.write(json.dumps(converted, ensure_ascii=False) + "\n")
with open("data_gpt_text3_deepseek70.jsonl", "r", encoding="utf-8") as f, open("sft_data_multi_templates_gpt_text3_deepseek70_qwen4.jsonl", "w", encoding="utf-8") as out_f:
    for line in f:
        item = json.loads(line)
        converted_list = convert_all_templates_qwen(item)
        for entry in converted_list:
            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")