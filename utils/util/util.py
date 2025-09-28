import json
import os
import re

import chardet


def convert_any_to_gbk(file_path, output_path=None):
    if output_path is None:
        output_path = file_path

    try:
        # 以二进制读入，检测编码
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            src_encoding = result['encoding']
            print(f"[INFO] {file_path} 原始编码: {src_encoding}")

        # 用检测到的编码解码
        text = raw_data.decode(src_encoding)

        # 再写为 gbk 编码，遇不能编码字符时替换为 ?
        with open(output_path, 'w', encoding='gbk', errors='replace') as f:
            f.write(text)

        print(f"[SUCCESS] 转换为 GBK: {output_path}")
    except Exception as e:
        print(f"[ERROR] 转换失败: {file_path}, 错误: {e}")


def batch_convert_all_to_gbk(root_dir, exts=(".go", ".sol", ".py", ".java", ".vy", ".rs")):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(exts):
                path = os.path.join(root, file)
                convert_any_to_gbk(path)
                # 删除文件中的多余空行（由编码格式改变后所产生）
                remove_blank_lines(path)


def remove_blank_lines(filepath: str):
    """
    删除文件中所有空行（只包含空格或制表符的行也视为空行），直接修改原文件。

    :param filepath: 要处理的文件路径
    """
    with open(filepath, 'r', encoding='gbk') as f:
        content = f.read()

    # 删除所有只包含空格、制表符或换行符的行
    no_blanks = re.sub(r'^[ \t]*\n', '', content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(no_blanks)


def collapse_blank_lines(filepath: str):
    """
    将文件中多个连续空行压缩为一个空行，直接修改原文件。

    :param filepath: 要处理的文件路径
    """
    with open(filepath, 'r', encoding='gbk') as f:
        content = f.read()

    # 替换两个以上的连续空行（可包含空格或制表符）
    collapsed = re.sub(r'(?:[ \t]*\n){2,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(collapsed)


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"The JSON file does not exist: {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")


def read_file_by_row_encode(file_path):
    try:
        # 以二进制读入，检测编码
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            src_encoding = result['encoding']
            # print(f"[INFO] {file_path} 原始编码: {src_encoding}")

        with open(file_path, "r", encoding=src_encoding) as f:
            data = f.read()
            return data
    except Exception as e:
        print(f"[ERROR] 转换失败: {file_path}, 错误: {e}")
