import json
import os
import re
import sys

from utils.dependence_analysis import analyzers
from utils.dependence_analysis.analyzers import extract_key_ops


def get_analyzer(lang):
    if lang == 'py':
        return analyzers.find_py_function_body, analyzers.trace_dependencies_py
    elif lang == 'sol':
        return analyzers.find_sol_function_body, analyzers.trace_dependencies_sol
    elif lang == 'java':
        return analyzers.find_java_function_body, analyzers.trace_dependencies_java
    elif lang == 'go':
        return analyzers.find_go_function_body, analyzers.trace_dependencies_go
    elif lang == 'rs':
        return analyzers.find_rs_function_body, analyzers.trace_dependencies_rs
    elif lang == 'vy':
        return analyzers.find_vy_function_body, analyzers.trace_dependencies_vy
    else:
        raise ValueError(f'不支持的语言类型: {lang}')


def dependence_analysis(input_blg_path, contract_base_path, output_res_path):
    """
    提取llm输入信息
    input_blg_path: blg.json 文件路径
    src_base_path: 合约源文件目录（目录下可能存在多个文件）
    output_res_path: 输出文件路径
    """
    data = {}
    for chain_type in ["src_chain", "rel_chain", "det_chain"]:
        func_key_ops = extract_key_ops(input_blg_path, chain_type)
        chain_info = func_key_ops.get(chain_type, {})
        data[chain_type] = {}
        for event_name, func_info in chain_info["events"].items():
            data[chain_type][event_name] = []
            for func_name, file_name_and_key_ops in func_info.items():
                file_name = file_name_and_key_ops['file_name']
                lang = file_name.split('.')[-1]
                find_func_body, trace_deps = get_analyzer(lang)
                func_body = find_func_body(os.path.join(contract_base_path, file_name), func_name)
                if not func_body:
                    print('未找到函数体')
                    sys.exit(1)
                # 针对部分编程语言，函数体需要去掉声明部分
                func_body_no_declaration = ""
                if lang in ['sol', 'java', 'go', 'rs'] and '{' in func_body:
                    func_body_no_declaration = func_body[func_body.index('{'):]
                count = 0
                first_op = ""
                temp_deps = []
                for key_op in file_name_and_key_ops['key_ops']:
                    deps = trace_deps(os.path.join(contract_base_path, file_name), func_body_no_declaration, key_op)
                    if deps:
                        count += 1
                        if count == 1:
                            first_op = key_op
                        temp_deps.extend(deps)
                    # print('依赖链:')
                    # for d in deps:
                    #     print(d)
                temp_deps = list(dict.fromkeys(temp_deps))
                new_str = ""
                for dep in temp_deps:
                    new_str += dep
                    new_str += "\n"
                new_str += first_op
                new_func_body = str(func_body).replace(first_op, new_str)
                data[chain_type][event_name].append({func_name : re.sub(r' {2,}', ' ', new_func_body)})
    # 保存数据
    with open(os.path.join(output_res_path, "llm_input_info.json"), 'w', encoding='gbk') as f:
        json.dump(data, f, indent=4)
    return data
