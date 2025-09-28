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


def build_dataset(base_dir: str, output_path: str, type: str):
    dataset = []

    for project in os.listdir(base_dir):
        project_dir = os.path.join(base_dir, project)
        llm_path = os.path.join(project_dir, "llm_input_info.json")
        train_path = os.path.join(project_dir, f"{project}.json")

        if not os.path.isfile(llm_path):
            continue

        try:
            llm_data = load_json(llm_path)
            function_groups = collect_function_groups(llm_data)
            vulnerable_func, detail = "", ""

            if type == "train":
                if os.path.isfile(train_path):
                    vulnerable_func, detail = load_vul_info(train_path)

            for group in function_groups:
                if type == "train":
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
                elif type == "test":
                    dataset.append({
                        "project": project,
                        "functions": group,
                        # "label": label,
                        "detail": detail # if label == "Yes" else "No known vulnerability found in this function group."
                    })
                    print({
                        "project": project,
                        "functions": group,
                        # "label": label,
                        "detail": detail # if label == "Yes" else "No known vulnerability found in this function group."
                    })

        except Exception as e:
            print(f"Error parsing {project}: {e}")

    with open(output_path, 'w', encoding='gbk') as f:
        for item in dataset:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


def extract_causes_from_jsonl(jsonl_path: str, output_path: str) -> int:
    """
    逐行读取 JSONL 文件，解析每行 JSON，提取 'rule' 字段中的 'cause' 值（非空），
    并以追加模式写入输出文件，每条 cause 占一行。

    :param jsonl_path: 输入 JSONL 文件路径
    :param output_path: 输出文件路径（追加模式）
    :return: 写入 cause 的数量
    """
    count = 0
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'a', encoding='utf-8') as outfile:
            for raw in infile:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                rule = obj.get('rule')
                if not isinstance(rule, dict):
                    continue
                cause = rule.get('cause')
                if not isinstance(cause, str):
                    continue
                cause_str = cause.strip()
                if not cause_str:
                    continue
                out_obj = {"rule": cause_str}
                outfile.write(json.dumps(out_obj, ensure_ascii=False) + '\n')
                count += 1
            outfile.flush()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件未找到: {e.filename}")
    except IOError as e:
        raise IOError(f"文件读写错误: {e}")
    return count


if __name__ == '__main__':
    # 启动执行
    # print("==================non_vul_data==================")
    # build_dataset(
    #     base_dir=r"../dataset1/non_vul_data",
    #     output_path="./input/non_vul_cross_chain_data.jsonl",
    #     type="train"
    # )
    # print("==================vul_data==================")
    # build_dataset(
    #     base_dir=r"../dataset1/vul_data",
    #     output_path="./input/vul_cross_chain_data.jsonl",
    #     type="train"
    # )

    print("==================add_non_vul_data==================")
    build_dataset(
        base_dir=r"../dataset1/add_non_vul_data",
        output_path="./input/add_non_vul_cross_chain_data.jsonl",
        type="train"
    )


