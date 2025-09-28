import json
import os
import re

import chardet
import tiktoken
from codebase_to_text import CodebaseToText

from eblg_build.eblg_helper import validate_and_refine_until_passed
from utils.llm_helper.analyzer import analyze_split_bridge_contract, analyze_merge_bridge_chunks
from utils.util.util import batch_convert_all_to_gbk


### Early stage: Project reading
def convert_contracts_to_txt(bridge_dir_path: str, output_dir_path: str, bridge_name: str) -> str:
    """
    将合约项目中的代码文件（contracts 目录）转换为单一的 TXT 文件，并保存到指定路径。

    参数:
        bridge_dir_path (str): 合约项目 contracts 目录路径（通常为 {bridge_pro_dir_path}/contracts）。
        output_dir_path (str): 转换后 TXT 文件的输出目录。
        bridge_name (str): 跨链桥名称，用于命名输出文件。

    返回:
        str: 转换后的 TXT 文件的完整路径。

    功能说明:
        - 创建输出目录（如果不存在）。
        - 批量将 contracts 目录下代码转换为 GBK 编码。
        - 使用 CodebaseToText 工具，将代码文件合并为一个 TXT 文本。
        - 返回输出 TXT 路径。
    """
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    pro_to_text_file_path = os.path.join(output_dir_path, f"{bridge_name}.txt")

    # 初始化输出文件为空
    with open(pro_to_text_file_path, 'w', encoding="gbk") as f:
        f.write("")

    # 转换为 gbk 编码
    batch_convert_all_to_gbk(bridge_dir_path)

    # 调用工具转换为 txt
    code_to_text = CodebaseToText(
        input_path=bridge_dir_path,
        output_path=pro_to_text_file_path,
        output_type="txt",
        verbose=True,
        exclude_hidden=True
    )
    code_to_text.get_file()

    return pro_to_text_file_path


### Step1: Split by file
def split_integrated_project(
        input_file: str,
        output_dir: str = "chunks_output",
        max_tokens: int = 20000,
        model: str = "gpt-4"
):
    """
    按文件为单位，将整合后的大项目文件分块，单块不超过 max_tokens。
    文件格式要求：
    1. 文件开始前有 "File Contents"
    2. 每个文件的起始标记为:
        <路径>
        File type: .sol

    3. 文件结束标记为:
        --------------------------------------------------
        File End
        --------------------------------------------------

    参数:
        input_file:  输入的整合文件路径
        output_dir:  输出分块目录
        max_tokens:  每个块的最大 token 数
        model:       使用的模型，用于 tiktoken tokenizer
    """
    os.makedirs(output_dir, exist_ok=True)
    enc = tiktoken.encoding_for_model(model)

    # 读取全文
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # 从 File Contents 之后开始处理
    if "File Contents" not in text:
        raise ValueError("文件中未找到 'File Contents'")
    text = text.split("File Contents", 1)[1]

    # 匹配每个文件（路径 + File type + 文件内容 + 结束标记）
    pattern = re.compile(
        r"\n([^\n]+?)\n"  # 文件路径
        r"(File type:.*?)\n"  # File type 行
        r"(.*?)"  # 文件内容
        r"--------------------------------------------------\s*\nFile End\s*\n--------------------------------------------------",
        re.DOTALL
    )
    matches = pattern.findall(text)

    files = []
    for filepath, filetype_line, filecontent in matches:
        filepath = filepath.strip()
        tokens = len(enc.encode(filecontent))
        files.append((filepath, filetype_line.strip(), filecontent, tokens))

    print(f"共解析出 {len(files)} 个文件")

    # 按文件分块
    chunks = []
    current_chunk = []
    current_tokens = 0

    for filepath, filetype_line, content, tokens in files:
        if tokens > max_tokens:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_tokens = 0
            chunks.append([(filepath, filetype_line, content, tokens)])
        else:
            if current_tokens + tokens > max_tokens:
                chunks.append(current_chunk)
                current_chunk = []
                current_tokens = 0
            current_chunk.append((filepath, filetype_line, content, tokens))
            current_tokens += tokens

    if current_chunk:
        chunks.append(current_chunk)

    # 输出分块文件
    for i, chunk in enumerate(chunks, start=1):
        chunk_file = os.path.join(output_dir, f"chunk_{i}.txt")
        total_tokens = sum(t for _, _, _, t in chunk)
        with open(chunk_file, "w", encoding="utf-8") as cf:
            cf.write(f"Chunk {i}, total tokens: {total_tokens}\n\n")
            for path, filetype_line, content, tks in chunk:
                normalized_path = path.replace("\\", "/")
                filename = normalized_path.split("/")[-1]
                cf.write(
                    "--------------------------------------------------\nFile Start\n--------------------------------------------------\n\n")
                cf.write(f"File Name: {filename}\n")
                cf.write(f"{filetype_line}\n\n")
                cf.write(content.strip() + "\n")
                cf.write(
                    "--------------------------------------------------\nFile End\n--------------------------------------------------\n\n")
        print(f"Chunk {i}: {len(chunk)} files, {total_tokens} tokens")

    print(f"\n生成 {len(chunks)} 个 chunk，保存在 {output_dir}")
    return chunks


### Step2: Step 2: Block analysis
def analyze_bridge_code_with_llm(txt_file_path: str, output_dir: str, bridge_name: str, bridge_dir: str,
                                 model_type: str) -> None:
    """
    使用指定的大语言模型分析桥合约代码，并验证生成的 JSON 输出。

    参数:
        txt_file_path (str): 包含合约代码的 TXT 文件路径。
        output_dir (str): 输出分析结果的目录。
        bridge_name (str): 跨链桥名称，用于命名输出 JSON。
        bridge_dir (str): 合约项目的 contracts 目录路径。
        model_type (str): 使用的大语言模型类型，例如 "openai"、"Qwen/QwQ-32B" 等。

    功能说明:
        - 读取 TXT 文件内容（自动检测编码）。
        - 调用 LLM 模型分析合约代码，生成结构化 JSON 文件。
        - 尝试多轮验证与修正，确保 JSON 格式合法。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 自动检测编码并读取内容
    with open(txt_file_path, 'rb') as f:
        contract_code_binary = f.read()
    encoding = chardet.detect(contract_code_binary)['encoding']
    with open(txt_file_path, 'r', encoding=encoding) as f:
        contract_code = f.read()

    output_json_path = os.path.join(output_dir, f"{bridge_name}.json")

    try:
        # 第一步：LLM 分析生成初步 JSON
        analyze_split_bridge_contract(
            contract_code,
            bridge_name=bridge_name,
            model_type=model_type,
            output=output_json_path,
            report=True
        )

        # 第二步：验证并修复 JSON，最多尝试 max_attempts 次
        validate_and_refine_until_passed(
            contract_code=contract_code,
            bridge_name=bridge_name,
            output_pro_dir_path=output_dir,
            bridge_dir_path=bridge_dir,
            max_attempts=10,
            check_chain_tail_match=False  # 不检查编号尾部
        )

    except Exception as e:
        print(f"[ERROR] 合约分析失败: {e}")


### Step 3: Summarize and merge
def analyze_merge_chunks_with_llm(chunk_json_dir: str, output_dir: str, bridge_name: str,
                                  bridge_dir: str, model_type: str) -> None:
    """
    合并多个 JSON 分析片段，使用 LLM 进行统一分析并校验输出。

    参数:
        chunk_json_dir (str): 拆分模式生成的多个 JSON 文件的目录。
        output_dir (str): 合并结果输出目录。
        bridge_name (str): 跨链桥名称，用于命名输出文件。
        bridge_dir (str): 合约项目的 contracts 目录路径（用于验证阶段）。
        model_type (str): 使用的大语言模型类型，例如 "openai"、"Qwen/QwQ-32B" 等。

    步骤:
        1. 读取 chunk_json_dir 中所有 JSON 文件，按顺序合并为字符串输入。
        2. 使用合并提示词调用 LLM 进行合并分析。
        3. 对合并结果进行结构校验和多轮修复。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取所有 JSON chunk 文件内容
    chunk_contents = []
    for filename in sorted(os.listdir(chunk_json_dir)):
        if filename.endswith(".json"):
            with open(os.path.join(chunk_json_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    json_obj = json.load(f)
                    json_str = json.dumps(json_obj, ensure_ascii=False, indent=2)
                    chunk_contents.append(json_str)
                except Exception as e:
                    print(f"[WARN] 跳过无效 JSON 文件: {filename}，原因: {e}")

    if not chunk_contents:
        print("[ERROR] 未找到有效的 JSON 分析片段")
        return

    # 拼接成 LLM 输入格式
    all_chunk_json = "\n\n".join(chunk_contents)

    output_json_path = os.path.join(output_dir, f"{bridge_name}_merged.json")

    try:
        # 第一步：LLM 合并分析多个 chunk
        merged_result, _ = analyze_merge_bridge_chunks(
            all_chunk_json=all_chunk_json,
            bridge_name=bridge_name,
            model_type=model_type,
            output=output_json_path,
            report=True
        )

        # 第二步：验证并修复合并后的 JSON 结构
        with open(output_json_path, 'r', encoding='utf-8') as f:
            merged_code_for_validation = f.read()

        validate_and_refine_until_passed(
            contract_code=merged_code_for_validation,
            bridge_name=f"{bridge_name}_merged",
            output_pro_dir_path=output_dir,
            bridge_dir_path=bridge_dir,
            max_attempts=10
        )

    except Exception as e:
        print(f"[ERROR] 合并分析失败: {e}")
