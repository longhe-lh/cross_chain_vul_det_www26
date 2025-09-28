import os

from utils.util.util import read_json_file

if __name__ == '__main__':
    # dir_path = "../../dataset1/non_vul_data"
    dir_path = "../../dataset1/vul_data"
    for root, dirs, files in os.walk(dir_path):
        for d in dirs:
            if d == 'contracts':
                bridge_path = root
                src_dir_path = os.path.join(root, d)
                bridge_name = os.path.basename(os.path.dirname(os.path.join(root, d)))
                blg_path = os.path.join(bridge_path, f"{bridge_name}.json")
                data = read_json_file(blg_path)
                llm_input_info = os.path.join(bridge_path, "llm_input_info.json")
                merge_code_path = os.path.join(bridge_path, f"{bridge_name}.txt")
                if os.path.exists(llm_input_info):
                    os.remove(llm_input_info)
                else:
                    print(f"file path: {llm_input_info} not exist")
