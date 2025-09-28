import os
import shutil


def collect_contracts_to_target(input_root, output_root):
    for bridge_name in os.listdir(input_root):
        bridge_path = os.path.join(input_root, bridge_name)
        contract_path = os.path.join(bridge_path, "contract")

        if not os.path.isdir(contract_path):
            print(f"❌ Skipped {bridge_name}: no contract folder")
            continue

        # 创建新的 BridgeX 输出目录
        output_bridge_dir = os.path.join(output_root, bridge_name)
        output_contracts_dir = os.path.join(output_bridge_dir, "contracts")
        os.makedirs(output_contracts_dir, exist_ok=True)

        seen_filenames = set()

        # 遍历 BridgeX/contract/** 下所有 .sol 文件
        for dirpath, _, filenames in os.walk(contract_path):
            for file_name in filenames:
                if not file_name.endswith(".sol"):
                    continue

                if file_name in seen_filenames:
                    print(f"[{bridge_name}] Skipped duplicate: {file_name}")
                    continue

                seen_filenames.add(file_name)
                src_file_path = os.path.join(dirpath, file_name)
                dst_file_path = os.path.join(output_contracts_dir, file_name)

                shutil.copy2(src_file_path, dst_file_path)
                print(f"[{bridge_name}] Copied: {file_name} → {dst_file_path}")

    print("\n✅ All bridges processed.")


if __name__ == "__main__":
    # 输入 Bridges 根目录路径
    input_bridges_root = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\10-data-deduplicate\non_vul_bridges"

    # 输出目录，所有 BridgeX 的合约将被放到这里
    output_collected_root = r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\10-data-deduplicate\dedup_non_vul_bridges"

    collect_contracts_to_target(input_bridges_root, output_collected_root)
