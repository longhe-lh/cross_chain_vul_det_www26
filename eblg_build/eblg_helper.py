import os
import re
import json
import argparse
import time

from utils.dependence_analysis.deps_analysis import get_analyzer
from utils.llm_helper.analyzer import refine_analysis_result, save_analysis_result

VALID_EXTS = {'.go', '.rs', '.java', '.py', '.vy', '.sol'}


def list_valid_files(dir_path, exts=None):
    """
    列出目录下所有指定后缀的文件名
    """
    if exts is None:
        exts = VALID_EXTS
    try:
        files = os.listdir(dir_path)
    except FileNotFoundError:
        raise ValueError(f"指定目录不存在: {dir_path}")
    return {fname for fname in files if os.path.splitext(fname)[1] in exts}


def collect_file_names(obj, key='file_name', collected=None):
    """
    递归收集 JSON 中所有 file_name 字段的值
    """
    if collected is None:
        collected = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and isinstance(v, str):
                collected.append(v)
            else:
                collect_file_names(v, key, collected)
    elif isinstance(obj, list):
        for item in obj:
            collect_file_names(item, key, collected)
    return collected


def extract_digits(names):
    """
    从字符串列表中提取末尾数字，返回所有成功提取到的数字集合
    """
    digits = set()
    pattern = re.compile(r'(\d+)$')
    for name in names:
        m = pattern.search(name)
        if m:
            digits.add(m.group(1))
    return digits


def validate_section(section, valid_files, pairs, dir_path, check_chain_tail_match=True):
    """
    校验单个桥配置，返回错误列表。
    参数：
        - check_chain_tail_match: 是否校验 src_chain 和 det_chain 事件的编号尾部是否对齐。
    """
    errors = []
    roles = section.get('roles')
    if roles is None:
        return ["The 'roles' field is missing in the configuration."]

    # 校验 src_chain, det_chain 是否为 list
    for field in ('src_chain', 'det_chain'):
        if field not in roles:
            errors.append(f"The '{field}' field is missing in 'roles'.")
        elif not isinstance(roles[field], list):
            errors.append(f"roles.{field} is not a list.")

    # 校验 rel_chain 是否为list (允许为空)
    if 'rel_chain' not in roles:
        errors.append("The 'rel_chain' field (which can be an empty list) must exist in roles.")
    elif not isinstance(roles['rel_chain'], list):
        errors.append("roles.rel_chain is not a list.")

    # 可选：校验 src_chain 与 det_chain 尾号是否对应
    if check_chain_tail_match:
        src = roles.get('src_chain', [])
        det = roles.get('det_chain', [])
        if isinstance(src, list) and isinstance(det, list):
            src_digits = extract_digits(src)
            det_digits = extract_digits(det)
            for v in src:
                if not re.search(r'\d+$', v):
                    errors.append(f"The element '{v}' of src_chain does not end with a number.")
            for v in det:
                if not re.search(r'\d+$', v):
                    errors.append(f"The det_chain element '{v}' does not end with a number.")
            if src_digits.isdisjoint(det_digits):
                errors.append(f"The last digits of src_chain and det_chain have no corresponding relationship: src_digits={src_digits}, det_digits={det_digits}")

    # 校验 rel_chain 元素不以数字结尾
    rel = roles.get('rel_chain', [])
    if isinstance(rel, list):
        for v in rel:
            if re.search(r'\d+$', v):
                errors.append(f"The '{v}' element of rel_chain cannot end with a number.")

    # 校验函数是否在指定文件中存在
    for func_name, file_name in pairs:
        # print(f"函数名: {func_name}, 文件名: {file_name}")
        if file_name not in valid_files: # 文件不存在
            tag = 0
            for valid_file in valid_files:
                lang = file_name.split(".")[-1]
                find_func_body, _ = get_analyzer(lang)
                func_body = find_func_body(os.path.join(dir_path, valid_file), func_name)
                if func_body is not None:
                    errors.append(
                        f"The function {func_name} could not be located because the file {file_name} does not exist."
                        f" However, it is defined in {valid_file}. "
                    )
                    break
                else:
                    tag += 1
            if tag == len(valid_files):
                errors.append(f"The function {func_name} does not exist.")

        else: # 文件存在
            lang = file_name.split(".")[-1]
            find_func_body, _ = get_analyzer(lang)
            func_body = find_func_body(os.path.join(dir_path, file_name), func_name)
            if func_body is None:
                errors.append(f"No function named {func_name} was found in {file_name}.")

    return errors


def extract_func_and_file_pairs(data):
    result = []

    def recurse(obj):
        if isinstance(obj, dict):
            if "func_name" in obj and "file_name" in obj:
                result.append((obj["func_name"], obj["file_name"]))
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    return result


def validate_json_file(json_file_path, dir_path, check_chain_tail_match=True):
    """
    从文件读取 JSON 并按照规则校验单个桥配置。
    参数：
        - check_chain_tail_match: 是否校验编号尾部是否对齐（用于拆分阶段关闭）。
    返回 (is_valid: bool, errors: list[str])
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, [f"The JSON file does not exist: {json_file_path}"]
    except json.JSONDecodeError as e:
        return False, [f"JSON parsing failed: {e}"]

    if not isinstance(data, dict) or len(data) != 1:
        return False, ["The top-level JSON must wrap the object format for a single bridge name."]
    # 提取唯一的桥配置对象
    section = next(iter(data.values()))

    try:
        valid_files = list_valid_files(dir_path)
    except ValueError as e:
        return False, [str(e)]

    # pairs 用于校验 func_name 是否在 file_name 所在文件中
    pairs = extract_func_and_file_pairs(data)

    errors = validate_section(section, valid_files, pairs, dir_path, check_chain_tail_match=check_chain_tail_match)

    return len(errors) == 0, errors


def validate_and_refine_until_passed(
        contract_code: str,
        bridge_name: str,
        output_pro_dir_path: str,
        bridge_dir_path: str,
        max_attempts: int = 10,
        check_chain_tail_match: bool = True
):
    """
    参数：
        - contract_code: 原始桥合约代码
        - bridge_name: 桥名（用于输出 JSON 文件命名）
        - output_pro_dir_path: 分析结果输出路径
        - bridge_dir_path: 合约源代码路径
        - max_attempts: 最大尝试次数
        - check_chain_tail_match: 是否检查 src_chain 与 det_chain 尾号对应性（拆分阶段设为 False）
    """
    blg_path = os.path.join(output_pro_dir_path, f"{bridge_name}.json")
    attempt = 0

    print("开始验证生成的 blg json 格式...")

    while attempt < max_attempts:
        attempt += 1
        ok, errs = validate_json_file(blg_path, bridge_dir_path, check_chain_tail_match=check_chain_tail_match)

        if ok:
            print(f"✅ 验证通过（共尝试 {attempt} 次）: {blg_path}")
            return

        print(f"\n❌ 验证失败（第 {attempt} 次），尝试优化中...\n错误如下：")
        all_errs = "\n".join(f"- {err}" for err in errs)
        print(all_errs)

        try:
            with open(blg_path, 'r', encoding='utf-8') as f:
                original_result = f.read()

            # refine_analysis_result 函数需接受原始字符串和错误信息返回 refined 字符串
            refined_result = refine_analysis_result(contract_code, original_result, all_errs)

            if refined_result:
                save_analysis_result(refined_result, blg_path)

            time.sleep(1)

        except Exception as e:
            print(f"❗ 优化过程异常：{e}")
            break

    print(f"\n🚫 最多尝试 {max_attempts} 次仍未通过验证，请检查文件：{blg_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="校验单桥 JSON 文件（第二种格式）及文件名合法性")
    parser.add_argument('--json', '--json-file', dest='json_file', type=str, required=True,
                        help='待校验的 JSON 文件路径')
    parser.add_argument('--dir', dest='dir_path', type=str, required=True,
                        help='用于校验的目录路径')
    args = parser.parse_args()

    ok, errs = validate_json_file(args.json_file, args.dir_path)
    if ok:
        print("校验通过 ✅")
    else:
        print("校验失败 ❌，错误如下：")
        for e in errs:
            print(" -", e)
