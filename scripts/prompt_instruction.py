import requests
import json
import time

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-c658c61cbb5141b38803d49df4a2ea3a"
API_URL = "https://api.deepseek.com/v1/chat/completions"

import re

def extract_json_from_markdown(text: str) -> str:
    try:
        # 尝试匹配完整的 ```json 包裹内容
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return match.group(1)

        # 尝试提取看似完整的 JSON 对象，从 { 开始匹配到最后一个 }
        json_start = text.find("{")
        json_end = text.rfind("}")
        if json_start != -1 and json_end != -1 and json_end > json_start:
            return text[json_start:json_end+1]

        raise ValueError("No complete JSON object found")
    except Exception as e:
        raise ValueError(f"Failed to extract JSON from text: {e}")

def build_fix_prompt(response_text: str):
    return f"""
The following response was intended to be a JSON object but is malformed or truncated.

Please fix the formatting and return a complete, valid JSON object. Do NOT include explanations or commentary. Just return the fixed JSON.

Malformed content:
{response_text.strip()}
"""

def fix_malformed_json(response_text):
    prompt = build_fix_prompt(response_text)
    fixed_response = call_deepseek(prompt)
    cleaned = extract_json_from_markdown(fixed_response)
    return json.loads(cleaned)

# 构造 prompt
# def build_prompt(item):
#     functions = "\n\n".join(item["functions"])
#     detail = item["detail"]
#     label = item["label"]
#
#     prompt = f"""You are a smart contract security expert.
#
# Below is a group of smart contract functions and an analysis of their behavior.
#
# === Smart Contract Functions ===
# {functions}
#
# === Analysis Detail ===
# {detail}
#
# === Task ===
# 1. Think step-by-step about whether this function group contains a vulnerability and why. Output your reasoning as 'CoT'.
# 2. Extract the core vulnerable logic or important operations from these functions and return them in simplified **code-style pseudocode**, preserving original **syntax and structure** (`function xxx(...) { ... }`) but **removing all irrelevant or verbose operations**. Keep the output short and readable while **maintaining audit-relevant logic**.
# 3. If the label is 'Yes', write a concise and readable sentence that describes why this vulnerability occurs, including its cause, impact, and recommendation. Return it as a **plain text string**. If the label is 'No', return an empty string ("").
#
# Return your answer in JSON format like:
# {{
#   "CoT": "...",
#   "functions": [... simplified function logic ...],
#   "label": "{label}",
#   "rule": {{...}}  # or empty if label is No
# }}
# """
#     return prompt
# ----------------------------------------70%------------------------------------------------------------------------------------
def build_prompt(item):
    functions = "\n\n".join(item["functions"])
    detail = item["detail"]
    label = item["label"]

    prompt = f"""You are a smart contract security expert.

Below is a group of smart contract functions and an analysis of their behavior.

=== Smart Contract Functions ===
{functions}

=== Analysis Detail ===
{detail}

=== Task ===

1. Perform a step-by-step security audit from Step 1 to Step 5. Use the following strict format:
   - **Step 1: Behavior Summary**
     Briefly summarize what each function does. Be factual and direct.
   - **Step 2: Security-Critical Logic**
     List key operations such as external calls, token transfers, access control, state changes, or signature verifications.
   - **Step 3: Assumptions**
     Identify critical assumptions made by the contract (e.g. input correctness, token behavior, caller trust, external contract reliability).
   - **Step 4: Assumption Enforcement**
     For each assumption, clearly state whether it is enforced by the contract code (e.g. `require`) or left unchecked.
   - **Step 5: Vulnerability Conclusion**
     Decide whether a vulnerability exists. If so, explain the exact reason, without rhetorical or emotional language. Only use factual, causal, or conditional reasoning.

**Important**:
- Do NOT skip any step. Output all 5 steps in your answer, even if a step has no content (write `"Step X: None"`).
- Avoid using rhetorical connectors like “however”, “but”, “actually”, “in fact”, “instead”. Your tone should be formal and analytical.
- Use only logical deduction and avoid speculation.

Label this structured reasoning section as `"CoT"`.

2. Extract the core logic relevant to potential vulnerabilities in **code-style pseudocode**:
  - Preserve the original `function xxx(...) {{ ... }}` syntax
  - Retain critical operations such as: state updates, external calls, permission checks, and signature verifications
  - Remove boilerplate code, logging, comments, and unrelated internal calculations
  - Keep the output short, clean, and readable

3. If a vulnerability is found (label is 'Yes'), summarize a **generalized security rule** that applies to similar situations. Do not refer to specific function or variable names. Return the rule as a JSON object with the following keys:
  - "pattern": the kind of logic or structure this rule applies to
  - "issue": what the general security risk is
  - "recommendation": how this type of issue can be avoided or mitigated

If the label is 'No', **do not fabricate a rule** — return an empty object: {{}}

Ensure your final answer is valid JSON. Do not include extra text, comments, or explanations outside the JSON.

Return your output as a valid JSON object. Enclose all string values in double quotes. Escape internal quotes or special characters as needed.

For example:
{{
  "CoT": "Step-by-step reasoning here...",
  "functions": [
    "function example(...) {{\n  if (x > 0) {{ ... }}\n}}"
  ],
  "label": "{label}",
  "rule": {{
    "pattern": "...",
    "issue": "...",
    "recommendation": "..."
  }}
}}

"""
    return prompt

# -------------------------------------------------------------------------------------------------

# ----------------------------------------------------假阴性-------------------------
# def build_prompt(item):
#     functions = "\n\n".join(item["functions"])
#     detail = item["detail"]
#     label = item["label"]
#
#     prompt = f"""You are a smart contract security auditor. Your job has three tasks:
#
#     1. Analyze the smart contract functions below to determine if a vulnerability exists. Use a structured 5-step format to walk through the reasoning chain clearly and causally. Highlight assumptions about token behavior, external calls, or signature trust that could lead to attacks if violated.
#
#     2. Extract the **minimal set of code lines** that directly support your vulnerability reasoning from Step 2–4. Only retain lines **explicitly discussed** in Step 2–4. If not mentioned in the reasoning, do NOT keep that line.
#
#     3. If a vulnerability exists (label is "Yes"), write a generalized security rule.
#
#     === Smart Contract Functions ===
#     {functions}
#
#     === Analysis Detail ===
#     {detail}
#
#     === Task ===
#
#     Step 1–5 Security Reasoning:
#     Use this format:
#        - Step 1: Behavior Summary
#        - Step 2: Security-Critical Logic
#        - Step 3: Assumptions
#        - Step 4: Assumption Enforcement
#        - Step 5: Vulnerability Conclusion
#
#     * Only refer to code that appears in the original functions.
#     * Use clear, causal logic and do not hallucinate.
#     * Every line you reference in Step 2–4 must appear in the extracted function set.
#
#     Code Extraction:
#     After reasoning, extract the function definitions mentioned in Step 2–4.
#     For each function:
#     - Keep full signature
#     - Only retain lines mentioned in Step 2–4
#     - If a variable is used, show its full form (e.g., `_swapData.callTo` instead of `callTo`)
#     - Exclude any logic not involved in security checks, approvals, external calls, or access control
#     - Do not include unused lines or math-only logic
#
#     Example:
#     If you write in Step 2:
#     "Calls _swapData.callTo.call(...)"
#     Then the function must include:
#     "  (bool success, ) = _swapData.callTo.call(...);"
#
#     Rule Generation:
#     If label == "Yes", output:
#     "rule": {{
#       "pattern": "<Pattern of vulnerable logic>",
#       "issue": "<What goes wrong?>",
#       "recommendation": "<How to fix it>"
#     }}
#
#     If label == "No", output: "rule": {{}}
#
#     === Output Format ===
#     Return only valid JSON:
#
#     {{
#       "CoT": "Step 1: ... Step 2: ... Step 3: ... Step 4: ... Step 5: ...",
#       "functions": ["function ... {{\n  ...\n}}", "..."],
#       "label": "{label}",
#       "rule": {{...}} or {{}}
#     }}
#     """
#     return prompt

# --------------------------------- gpt---------------------------
# def build_prompt(item):
#     functions = "\n\n".join(item["functions"])
#     detail = item["detail"]
#     label = item["label"]
#
#     prompt = f"""You are a smart contract security expert. You have three tasks:
#
# 1. **Analyze the smart contract functions** below for vulnerabilities using a structured 5-step reasoning process. If any assumption (e.g., about external calls, permissions, or token behavior) is not enforced and leads to sensitive operations, you must conclude that a vulnerability exists.
#
# 2. **Extract only the minimal code** directly relevant to Step 2–4. Every line must correspond to an operation explicitly discussed in your reasoning. Do not keep helper logic, math, or unused variables.
#
# 3. **If a vulnerability exists (label = "Yes")**, write a generalized security rule.
#
# === Smart Contract Functions ===
# {functions}
#
# === Analysis Detail ===
# {detail}
#
# === Task ===
#
# Follow this format strictly:
#
# **Step 1: Behavior Summary**
# Describe what each function does. Be factual.
#
# **Step 2: Security-Critical Logic**
# Identify key operations: external calls, permission checks, asset movements, or signature verification.
#
# **Step 3: Assumptions**
# List assumptions made by the code (e.g., call target is safe, balance checks are valid, signer is trusted).
#
# **Step 4: Assumption Enforcement**
# Check if those assumptions are enforced (e.g., require, validation, signature check). If any assumption is **not enforced**, state that clearly.
#
# **Step 5: Vulnerability Conclusion**
# If any assumption is unenforced and could lead to token loss, unauthorized access, or arbitrary logic execution, conclude that a **vulnerability exists**.
# Be definitive:
# - Say: “A vulnerability exists because...”
# - Or: “No vulnerability exists because all assumptions are enforced.”
#
# Then write:
# Label: Yes
# "label": "Yes"
#
# Or:
# Label: No
# "label": "No"
#
# ---
#
# **Code Extraction**
# Extract only code lines discussed in Step 2–4.
# - Keep original function names.
# - Keep full function signatures.
# - Show complete variable paths (e.g., `_data.callTo` not `callTo`)
# - Escape newlines as `\\n`
#
# Example:
# If Step 2 mentions `_swapData.callTo.call(...)`, include:
# "function swap(...) {{\\n  (bool success, ) = _swapData.callTo.call(...);\\n}}"
#
# ---
#
# **Rule Generation**
# If vulnerability exists, output:
#
# "rule": {{
#   "pattern": "<description of vulnerable logic>",
#   "issue": "<what goes wrong>",
#   "recommendation": "<how to fix it>"
# }}
#
# If not, use:
# "rule": {{}}
#
# ---
#
# **Final Output Format**
# Return valid JSON with the following structure:
#
# {{
#   "CoT": "Step 1: ... Step 2: ... Step 3: ... Step 4: ... Step 5: ...\\nLabel: Yes\\n\"label\": \"Yes\"",
#   "functions": [
#     "function swap(...) {{\\n  (bool success, ) = _swapData.callTo.call(...);\\n}}"
#   ],
#   "label": "Yes",
#   "rule": {{
#     "pattern": "...",
#     "issue": "...",
#     "recommendation": "..."
#   }}
# }}
#
# If the label is No, output:
# "rule": {{}}
#
# Do not include any explanation or markdown. Output must be JSON only.
# """
#     return prompt

# 调用 DeepSeek API
def call_deepseek(prompt, model="deepseek-chat", max_tokens=1024):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a smart contract security auditor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print("==== Raw Response ====")
    print(response.text)  # 打印前 1000 个字符（避免太长）
    print("======================")

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    try:
        content = response.json()
        return content["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"JSON decode error or missing content: {response.text}") from e


# 主程序
input_path = "cross_chain_data.jsonl"
output_path = "data_cot_test2.jsonl"
error_log_path = "error_log2.txt"

with open(input_path, 'r', encoding='utf-8') as f, \
     open(output_path, 'w', encoding='utf-8') as out_f, \
     open(error_log_path, 'w', encoding='utf-8') as err_f:

    for idx, line in enumerate(f, 1):
        if idx<=62:
            continue
        item = json.loads(line)
        prompt = build_prompt(item)
        print(prompt)
        # try:
        #     response_text = call_deepseek(prompt)
        #     cleaned = extract_json_from_markdown(response_text)
        #     result = json.loads(cleaned)
        #     print(result)
        #     out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
        #     print(f"[✓] Sample {idx} done.")
        #
        # except Exception as e:
        #     print(f"[!] Error on sample {idx}, trying to fix...")
        #     try:
        #         result = fix_malformed_json(response_text)
        #         print(result)
        #         out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
        #         print(f"[✓] Sample {idx} fixed and written.")
        #     except Exception as fix_err:
        #         print(f"[✗] Fix failed on sample {idx}: {fix_err}")
        #         err_f.write(
        #             f"Sample {idx} Error:\n{str(fix_err)}\nOriginal Prompt:\n{prompt}\nOriginal Output:\n{response_text}\n{'=' * 80}\n")
        # time.sleep(1.2)
        # # break

print("All Done. Augmented data saved to:", output_path)
