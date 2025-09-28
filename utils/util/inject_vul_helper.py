"""
    实现步骤：
    1. 从漏洞项目中读取：漏洞函数和detail描述
    2. 将漏洞函数 和 detail 分别插入到 非漏洞的数据集中

"""
import os
import re
import sys

from utils.dependence_analysis.deps_analysis import get_analyzer
from utils.util.util import read_json_file, convert_any_to_gbk, remove_blank_lines

import json
from typing import List, Union


def update_jsonl(
    input_file: str,
    output_file: str,
    new_detail: str,
    new_functions: Union[str, List[str]]
):
    """
    读取 JSONL 文件，为每条记录追加函数并修改 detail 字段，写入新的 JSONL 文件。

    :param input_file: 原始 .jsonl 文件路径
    :param output_file: 修改后的 .jsonl 文件保存路径
    :param new_detail: 要设置的新 detail 字符串
    :param new_functions: 要添加的函数（字符串或字符串列表）
    """
    # 保证 new_functions 是列表
    if isinstance(new_functions, str):
        new_functions = [new_functions]

    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        for line_num, line in enumerate(fin, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)

                # 修改 detail 字段
                data["detail"] = new_detail

                # 修改 label 字段
                data["label"] = "Yes"

                # 添加函数
                if "functions" in data:
                    data["functions"].extend(new_functions)
                else:
                    data["functions"] = new_functions.copy()

                # 写入新行
                fout.write(json.dumps(data, ensure_ascii=False) + "\n")

            except json.JSONDecodeError as e:
                print(f"第 {line_num} 行解析失败：", e)


if __name__ == '__main__':
    dir_path = r"../../dataset1/vul_data"

    base_output_path = r"../../lm_teacher/input"

    for root, dirs, files in os.walk(dir_path):
        for d in dirs:
            if d == 'contracts':
                bridge_path = root
                src_dir_path = os.path.join(root, d)
                bridge_name = os.path.basename(os.path.dirname(os.path.join(root, d)))
                blg_path = os.path.join(bridge_path, f"{bridge_name}.json")
                data = read_json_file(blg_path)

                vul_entry_func = data.get('vulnerable_entry_function')
                file_name = vul_entry_func.get('file')
                func_name = vul_entry_func.get('name')
                detail = data.get('detail')
                print(f"=========={bridge_name}=======")
                convert_any_to_gbk(os.path.join(src_dir_path, file_name))
                # 删除文件中的多余空行（由编码格式改变后所产生）
                # collapse_blank_lines(path)
                remove_blank_lines(os.path.join(src_dir_path, file_name))

                # 获取函数内容

                lang = file_name.split('.')[-1]
                find_func_body, trace_deps = get_analyzer(lang)

                func_body = find_func_body(os.path.join(src_dir_path, file_name), func_name)
                if not func_body:
                    print('未找到函数体')
                    sys.exit(1)
                print(f"func_name:{func_name} \n func_body: {re.sub(r' {2,}', ' ', func_body)}")
                print(f"detail : {detail}")

                # 将数据写入到 没有漏洞的 跨链桥项目中

                output_file_path = os.path.join(base_output_path, f"{bridge_name}_inject.jsonl")
                if not os.path.exists(output_file_path):
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        pass

                update_jsonl(
                    input_file="../../lm_teacher/input/non_vul_cross_chain_data.jsonl",
                    output_file=output_file_path,
                    new_detail=detail,
                    new_functions=func_body
                )


