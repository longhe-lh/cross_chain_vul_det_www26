import os
import shutil

import chardet
from codebase_to_text import CodebaseToText

from eblg_build.eblg_helper import validate_and_refine_until_passed
from utils.llm_helper.analyzer import analyze_bridge_contract
from utils.util.util import batch_convert_all_to_gbk


def collect_contracts_and_run_analysis(input_root, output_root, model_type):
    for bridge_name in os.listdir(input_root):
        bridge_path = os.path.join(input_root, bridge_name)
        contract_path = os.path.join(bridge_path, "contract")

        if not os.path.isdir(contract_path):
            print(f"❌ Skipped {bridge_name}: no contract folder")
            continue

        # 输出 BridgeX 目录和 contracts 子目录
        output_bridge_dir = os.path.join(output_root, bridge_name)
        contracts_dir = os.path.join(output_bridge_dir, "contracts")
        os.makedirs(contracts_dir, exist_ok=True)

        seen_files = set()

        # 复制唯一合约文件
        for dirpath, _, filenames in os.walk(contract_path):
            for file_name in filenames:
                if not file_name.endswith(".sol"):
                    continue
                if file_name in seen_files:
                    continue

                seen_files.add(file_name)
                src_file = os.path.join(dirpath, file_name)
                dst_file = os.path.join(contracts_dir, file_name)
                shutil.copy2(src_file, dst_file)

        # 合并为 BridgeX.txt
        merged_txt_path = os.path.join(output_bridge_dir, f"{bridge_name}.txt")

        code_to_text = CodebaseToText(
            input_path=contracts_dir,
            output_path=merged_txt_path,
            output_type="txt",
            verbose=True,
            exclude_hidden=True
        )
        batch_convert_all_to_gbk(contracts_dir)
        code_to_text.get_file()

        # 读取合约文本内容
        try:
            # with open(merged_txt_path, 'r', encoding='gbk') as f:
            #     contract_code = f.read()

            with open(merged_txt_path, 'rb') as f:
                contract_code = f.read()
            with open(merged_txt_path, 'r', encoding=chardet.detect(contract_code)['encoding']) as f1:
                contract_code = f1.read()

        except Exception as e:
            print(f"❌ Failed to read {merged_txt_path}: {e}")
            continue

        # 执行分析和验证
        try:
            print(f"🚀 Analyzing {bridge_name}...")
            output_json_path = os.path.join(output_bridge_dir, f"{bridge_name}.json")

            analyze_bridge_contract(
                contract_code,
                bridge_name=bridge_name,
                model_type=model_type,
                output=output_json_path,
                report=True
            )

            print(f"🛠 Validating {bridge_name}...")
            validate_and_refine_until_passed(
                contract_code=contract_code,
                bridge_name=bridge_name,
                output_pro_dir_path=output_bridge_dir,
                bridge_dir_path=os.path.join(output_bridge_dir, "contracts"),
                max_attempts=10
            )

            print(f"✅ {bridge_name} analysis complete.\n")

        except Exception as e:
            print(f"❌ Error processing {bridge_name}: {e}")

    print("🎉 All bridges processed.\n")


if __name__ == "__main__":
    # 输入路径
    input_bridges_root = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\10-data-deduplicate\test_20250721\non_vul_bridges"
    # 整理后的输出路径
    output_collected_root = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\10-data-deduplicate\test_20250721\dedup_non_vul_bridges"
    # 分析模型类型标识
    model_type = "Qwen/QwQ-32B"

    collect_contracts_and_run_analysis(
        input_root=input_bridges_root,
        output_root=output_collected_root,
        model_type=model_type
    )
