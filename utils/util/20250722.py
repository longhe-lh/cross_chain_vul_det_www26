import json
import os

import chardet
from codebase_to_text import CodebaseToText

from eblg_build.eblg_helper import list_valid_files, extract_func_and_file_pairs, validate_section
from utils.util.util import batch_convert_all_to_gbk, collapse_blank_lines, read_json_file


def validate_json_file_1(data, dir_path):
    """
    从文件读取 JSON 并按照规则校验单个桥配置。
    仅支持第二种格式：顶层有且仅有一个键，该键对应桥对象。
    返回 (is_valid: bool, errors: list[str])
    """
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

    errors = validate_section(section, valid_files, pairs, dir_path)

    return len(errors) == 0, errors


def validate_json():
    blg_path = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\11-datasets\error\json文件格式错误\Across Bridge\Across Bridge.json"
    bridge_dir_path = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\11-datasets\error\json文件格式错误\Across Bridge\contracts"

    try:
        with open(blg_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"The JSON file does not exist: {blg_path}")
    except json.JSONDecodeError as e:
        print("JSON parsing failed: {e}")

    blg = data.get('blg')

    ok, errs = validate_json_file_1(blg, bridge_dir_path)
    if errs:
        for err in errs:
            print(f"- {err}")


def read_file_with_encoding(file_path):
    # 第一步：读取部分内容以检测编码
    with open(file_path, 'rb') as f:
        raw_data = f.read(2048)  # 只读取部分内容即可检测编码
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    if not encoding:
        raise ValueError("无法检测到文件的编码格式")

    # 第二步：使用检测到的编码重新读取整个文件
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()

    return content


if __name__ == '__main__':
    dir_path = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\07-dev_proj_new_bank\dataset1\vul_data"

    for root, dirs, files in os.walk(dir_path):
        for d in dirs:
            if d == 'contracts':
                bridge_path = root
                src_dir_path = os.path.join(root, d)
                bridge_name = os.path.basename(os.path.dirname(os.path.join(root, d)))
                blg_path = os.path.join(bridge_path, f"{bridge_name}.json")
                data = read_json_file(blg_path)

                vul_bridge_src = read_file_with_encoding(os.path.join(bridge_path, f"{bridge_name}.txt"))
                vul_func_info = data.get("vulnerable_entry_function")
                vul_func_info.pop('lines', None)
                vul_detail_info = data.get("detail")

                print(f"============={bridge_path}===========")

                print(f"vul_func_info: {vul_func_info}")
                print(f"vul_detail_info: {vul_detail_info}")

                print("==============end==========")
