import json
import os.path

from codebase_to_text import CodebaseToText

from global_config.global_config import LLM_MODEL_NAME
from utils.llm_helper.analyzer import analyze_bridge_contract

if __name__ == '__main__':
    # 合约路径和参数示例
    contract_pro_path = r"../../dataset/train_datas/vul_src_code/anyswap"
    bridge_name = "anyswap"

    # 合约 pro 转文本
    pro_info_file_dir_path = os.path.join("./out/", bridge_name)
    if not os.path.exists(pro_info_file_dir_path):
        os.makedirs(pro_info_file_dir_path)
    pro_info_file_path = os.path.join(pro_info_file_dir_path, f"{bridge_name}_pro_info.txt")
    with open(pro_info_file_path, "w", encoding="utf-8") as f:
        f.write("")

    code_to_text = CodebaseToText(
        input_path=contract_pro_path,
        output_path=pro_info_file_path,
        output_type="txt",
        verbose=True,             # 是否打印日志信息
        exclude_hidden=True       # 否要隐藏文件
    )

    code_to_text.get_file()

    output_path = os.path.join(r"./out/", bridge_name)
    model_type = LLM_MODEL_NAME  # 可选: "openai"、"baidu"、"aliyun"、"Qwen/QwQ-32B"、"deepseek"
    # 目前可用 aliyun, "Qwen/QwQ-32B","deepseek"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    report = True

    with open(pro_info_file_path, 'r', encoding='utf-8') as f:
        contract_code = f.read()

    # 调用核心分析流程
    result, report_content = analyze_bridge_contract(
        contract_code,
        bridge_name=bridge_name,
        model_type=model_type,
        output=os.path.join(output_path, f"{bridge_name}.json"),
        report=report
    )
    print("分析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if report_content:
        print("\n分析报告:")
        print(report_content)

    # 比较多个 LLM 分析的结果
    # to do sth

    # try:
    #     result1 = load_json_result("sample_analysis.json")
    #     result2 = load_json_result("another_analysis.json")
    #     comparison = compare_analysis_results(result1, result2)
    #     print("比较结果:")
    #     print(json.dumps(comparison, ensure_ascii=False, indent=2))
    # except FileNotFoundError:
    #     print("请先运行 example_analysis() 生成分析结果文件")
