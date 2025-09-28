import os

from utils.dependence_analysis.deps_analysis import dependence_analysis


def train_data_build(data_path):
    """
    根据文件夹下的跨链桥项目中的 contracts 和 {bridge_name}.json 文件构建 llm_input_info.json
    """
    for entry in os.listdir(data_path):
        print(f"Bridge name: {entry} process ...")
        bridge_dir = os.path.join(data_path, entry)
        if os.path.isdir(bridge_dir):
            contracts_path = os.path.join(bridge_dir, "contracts")
            # batch_convert_all_to_gbk(contracts_path)
            json_file = os.path.join(bridge_dir, f"{entry}.json")
            if os.path.isfile(json_file):
                try:
                    dependence_analysis(json_file, contracts_path, bridge_dir)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    """
        用于训练的数据 eblg 构建，不会调用 llm api
        直接传入需要分析的所有跨链桥项目的汇总文件路径
    """
    # print("==================non_vul_data==================")
    # train_data_build(r"../dataset1/non_vul_data")
    # print("===================vul_data=================")
    # train_data_build(r"../dataset1/vul_data")
    # print("===================add_non_vul_data=================")
    # train_data_build(r"../dataset1/add_non_vul_data")

    dependence_analysis(
        "../dataset1/vul_data/BSCTokenHub/BSCTokenHub.json",
        "../dataset1/vul_data/BSCTokenHub/contracts",
        "../dataset1/vul_data/BSCTokenHub"
    )