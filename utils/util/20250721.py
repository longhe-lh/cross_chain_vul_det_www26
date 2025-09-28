import os
import shutil


def copy_json_to_bridge_dirs(src_dir, dst_dir):
    print(f"📁 扫描 JSON 源目录: {src_dir}")

    if not os.path.exists(src_dir):
        print("❌ 源目录不存在")
        return
    if not os.path.exists(dst_dir):
        print("❌ 目标目录不存在")
        return

    for file_name in os.listdir(src_dir):
        if file_name.endswith(".json"):
            bridge_name = os.path.splitext(file_name)[0]
            json_path = os.path.join(src_dir, file_name)
            target_dir = os.path.join(dst_dir, bridge_name)
            target_path = os.path.join(target_dir, file_name)

            if os.path.isdir(target_dir):
                shutil.copy2(json_path, target_path)
                print(f"✅ 已复制: {file_name} -> {target_path}")
            else:
                print(f"⚠️ 跳过: {file_name}，因为 {target_dir} 不存在")


# 示例调用（替换成你的真实路径）
copy_json_to_bridge_dirs(r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\07-dev_proj_new_bank\dataset0721\manually_mark_vul_dataset_bank\smart_contract_vul\train_data",
                         r"D:\LongHe\01-PHD\02-基于LLM的跨链漏洞检测\07-dev_proj_new_bank\dataset0721\manually_mark_vul_dataset")
