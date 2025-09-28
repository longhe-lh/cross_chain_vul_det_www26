def get_system_prompt():
    return """
你是一个专业的智能合约安全分析师，专门分析跨链桥合约的跨链逻辑。
你的任务是：
1. 细致分析提供的跨链桥智能合约代码
2. 识别合约中的跨链逻辑和关键操作
3. 提取事件和关键操作语句
4. 按照指定的JSON格式输出分析结果
分析要求：
- 识别源链(src_chain)、中继链(rel_chain)、目标链(det_chain)的相关事件和函数
- 提取关键操作语句，如transfer、require、assert等
- 分析跨链类型（同构或异构）
- 识别各链上的角色和职责
- 构建嵌套的事件结构关系
- 源链角色需要和目标连角色在跨链流程中对齐（命名方式：源链事件_1, 目标链事件_1）
- 仅需要保留函数名即可，不需要参数信息
输出格式必须严格按照提供的JSON结构，不要添加任何额外的解释或说明。
"""


def get_analysis_prompt(contract_code, bridge_name="CrossChainBridge"):
    return f"""
请分析以下跨链桥智能合约代码，并按照指定格式输出跨链逻辑分析结果：

合约代码：
```solidity
{contract_code}
```

请按照以下JSON格式输出分析结果，不要添加任何额外的解释：

```json
{{
  "{bridge_name}": {{
    "interoperability": "homogeneous | heterogeneous",
    "roles": {{
      "src_chain": [<event names>],
      "rel_chain": [<event names>],
      "det_chain": [<event names>]
    }},
    "src_chain": {{
      "chain_name": "<source chain name>",
      "events": {{
        "<EventName>": {{
          "0": {{
            "func_name": "<function signature>",
            "file_name": "<file name>",
            "key_ops": [<关键操作语句，如 transfer、require 等>],
            "child": {{
              ... // 嵌套结构
            }}
          }}
        }}
      }}
    }},
    "rel_chain": {{
      "chain_name": "<relay chain name, 如果没有留空>",
      "events": {{}}
    }},
    "det_chain": {{
      "chain_name": "<destination chain name>",
      "events": {{
        "<EventName>": {{
          ...
        }}
      }}
    }}
  }}
}}
```

请确保：
1. 准确识别所有跨链相关的事件和函数
2. 提取所有关键操作语句
3. 正确构建嵌套结构
4. 判断跨链类型（同构/异构）
5. 识别各链的角色和职责
只输出JSON格式的结果，不要包含任何其他内容。
"""


def get_refinement_prompt(original_analysis, feedback):
    return f"""
基于以下反馈，请优化跨链桥分析结果：

原始分析结果：
{original_analysis}

反馈意见：
{feedback}

请根据反馈意见重新分析并输出优化后的JSON格式结果。确保：
1. 解决反馈中提到的问题
2. 保持JSON格式的正确性
3. 提高分析的准确性和完整性
只输出优化后的JSON结果，不要包含任何其他内容。
"""


# 以下为 lm_teacher 的提示词

def get_lm_teacher_prompt(item):
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
1. Think step-by-step about whether this function group contains a vulnerability and why. Output your reasoning as 'CoT'.
2. Extract the core vulnerable logic or important operations from these functions and return them in simplified **code-style pseudocode**, preserving original **syntax and structure** (`function xxx(...) { ... }`) but **removing all irrelevant or verbose operations**. Keep the output short and readable while **maintaining audit-relevant logic**.
3. If the label is 'Yes', write a concise and readable sentence that describes why this vulnerability occurs, including its cause, impact, and recommendation. Return it as a **plain text string**. If the label is 'No', return an empty string ("").

Return your answer in JSON format like:
{{
  "CoT": "...",
  "functions": [... simplified function logic ...],
  "label": "{label}",
  "rule": {{...}}  # or empty if label is No
}}
"""

    messages = [
        {"role": "system", "content": "You are a smart contract security auditor."},
        {"role": "user", "content": prompt}
    ]

    return messages
