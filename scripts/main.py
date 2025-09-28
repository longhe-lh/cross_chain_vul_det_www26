import os
import json
import re

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_func_name(func_def: str) -> str:
    match = re.search(r'\b(?:function|func)\s+([a-zA-Z0-9_]+)\s*\(', func_def)
    return match.group(1) if match else ""

def load_vul_info(train_path: str):
    data = load_json(train_path)
    sig = data.get("vulnerable_entry_function", {}).get("signature", "")
    detail = data.get("detail", "")
    func_name = extract_func_name(sig)
    return func_name, detail

def collect_function_groups(llm_data: dict) -> list:
    pattern = re.compile(r'(\D+)?(\d+)$')
    group_map = {}

    for section in ["src_chain", "det_chain"]:
        if section not in llm_data:
            continue
        for key, func_list in llm_data[section].items():
            match = pattern.match(key)
            if not match:
                continue
            suffix = match.group(2)
            if suffix not in group_map:
                group_map[suffix] = []
            for func_obj in func_list:
                group_map[suffix].extend(func_obj.values())

    groups = list(group_map.values())

    if "rel_chain" in llm_data:
        for func_list in llm_data["rel_chain"].values():
            rel_funcs = []
            for func_obj in func_list:
                rel_funcs.extend(func_obj.values())
            if rel_funcs:
                groups.append(rel_funcs)

    return groups

def build_dataset(blg_base_dir: str, train_data_dir: str, output_path: str):
    dataset = []

    for project in os.listdir(blg_base_dir):
        project_dir = os.path.join(blg_base_dir, project)
        llm_path = os.path.join(project_dir, "llm_input_info.json")
        train_path = os.path.join(train_data_dir, f"{project}.json")

        if not os.path.isfile(llm_path):
            continue

        try:
            llm_data = load_json(llm_path)
            function_groups = collect_function_groups(llm_data)
            vulnerable_func, detail = "", ""

            if os.path.isfile(train_path):
                vulnerable_func, detail = load_vul_info(train_path)

            for group in function_groups:
                func_names = [extract_func_name(code) for code in group]
                label = "Yes" if vulnerable_func in func_names else "No"
                dataset.append({
                    "project": project,
                    "functions": group,
                    "label": label,
                    "detail": detail if label == "Yes" else "No known vulnerability found in this function group."
                })
                print({
                    "project": project,
                    "functions": group,
                    "label": label,
                    "detail": detail if label == "Yes" else "No known vulnerability found in this function group."
                })

        except Exception as e:
            print(f"Error parsing {project}: {e}")

    with open(output_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


# 启动执行
build_dataset(
    blg_base_dir="../Data/blg_and_cag",
    train_data_dir="../Data/train_data",
    output_path="../cross_chain_data.jsonl"
)

