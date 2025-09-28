import os
import time

import chardet
from codebase_to_text import CodebaseToText

from eblg_build.eblg_helper import validate_json_file, validate_and_refine_until_passed
from global_config.global_config import LLM_MODEL_NAME
from utils.llm_helper.analyzer import analyze_bridge_contract, refine_analysis_result
from utils.dependence_analysis.deps_analysis import dependence_analysis
from utils.util.util import batch_convert_all_to_gbk, collapse_blank_lines


def build_eblg_batch(all_brg_root_dir_path, output_dir_path):
    """
    批量构建 eblg
    输入：包含所有桥合约项目的文件夹路径; 指定输出路径
    输出：以文件形式输出到指定文件夹下
    """
    for root, dirs, files in os.walk(all_brg_root_dir_path):
        for dir in dirs:
            bridge_dir_path = os.path.join(root, dir)
            bridge_name = dir
            print(f"桥合约项目路径：{bridge_dir_path}")
            # 合约 pro 转 txt
            output_pro_dir_path = os.path.join(output_dir_path, bridge_name)
            build_eblg_single(bridge_dir_path, output_pro_dir_path, bridge_name)


def build_eblg_single(bridge_pro_dir_path, out_put_dir_path, bridge_name):
    """
    单个构建 eblg
    输入：桥合约项目的文件夹路径; 指定输出路径; 跨链桥名称
    输出：以文件形式输出到指定文件夹下
    """
    bridge_dir_path = os.path.join(bridge_pro_dir_path, "contracts")
    output_pro_dir_path = out_put_dir_path
    print(f"桥合约项目路径：{bridge_dir_path}")
    # 合约 pro 转 txt
    if not os.path.exists(output_pro_dir_path):
        os.makedirs(output_pro_dir_path)
    pro_to_text_file_path = os.path.join(output_pro_dir_path, f"{bridge_name}.txt")
    with open(pro_to_text_file_path, 'w', encoding="gbk") as f:
        f.write("")
    code_to_text = CodebaseToText(
        input_path=bridge_dir_path,
        output_path=pro_to_text_file_path,
        output_type="txt",
        verbose=True,  # 是否打印日志信息
        exclude_hidden=True  # 是否排除隐藏文件
    )
    batch_convert_all_to_gbk(bridge_dir_path)
    code_to_text.get_file()

    # 开始分析
    model_type = LLM_MODEL_NAME  # 可选: "openai"、"baidu"、"aliyun"、"Qwen/QwQ-32B"、"deepseek"
    if not os.path.exists(output_pro_dir_path):
        os.makedirs(output_pro_dir_path)
    with open(pro_to_text_file_path, 'rb') as f:
        contract_code = f.read()
    with open(pro_to_text_file_path, 'r', encoding=chardet.detect(contract_code)['encoding']) as f1:
        contract_code = f1.read()
    # 调用核心分析流程
    try:
        analyze_bridge_contract(
            contract_code,
            bridge_name=bridge_name,
            model_type=model_type,
            output=os.path.join(output_pro_dir_path, f"{bridge_name}.json"),
            report=True
        )

        # 开始验证生成的blg的json格式
        validate_and_refine_until_passed(
            contract_code=contract_code,
            bridge_name=bridge_name,
            output_pro_dir_path=output_pro_dir_path,
            bridge_dir_path=bridge_dir_path,
            max_attempts=10
        )

    except Exception as e:
        print(e)
    # 依赖分析
    try:
        dependence_analysis(
            os.path.join(output_pro_dir_path, f"{bridge_name}.json"),
            bridge_dir_path,
            output_pro_dir_path
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    """
        在测试跨链桥项目时，只是分析单个跨链桥
        以跨链桥项目为输入，其中源码存在于跨链桥下的 contracts 目录下
    """
    try:
        build_eblg_single(
            bridge_pro_dir_path="../dataset1/test_data/Chainswap",
            out_put_dir_path="../dataset1/test_data/Chainswap",
            bridge_name="ChainSwap"
        )
    except Exception as e:
        print(e)
