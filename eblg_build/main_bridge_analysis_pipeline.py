import os
import glob
import multiprocessing
from blg_builder import (
    convert_contracts_to_txt,
    split_integrated_project,
    analyze_bridge_code_with_llm,
    analyze_merge_chunks_with_llm
)
from utils.dependence_analysis.deps_analysis import dependence_analysis


def process_single_chunk(chunk_txt_path, chunk_output_dir, bridge_name, bridge_dir, model_type):
    analyze_bridge_code_with_llm(
        txt_file_path=chunk_txt_path,
        output_dir=chunk_output_dir,
        bridge_name=os.path.splitext(os.path.basename(chunk_txt_path))[0],  # 单独chunk名
        bridge_dir=bridge_dir,
        model_type=model_type
    )


def run_full_bridge_analysis(bridge_pro_dir, output_base_dir, bridge_name, model_type):
    """
    全流程：1. 读取合约工程 -> 2. 拆分 -> 3. 并行分析 -> 4. 合并
    """
    contracts_txt_dir = os.path.join(output_base_dir, "txt_files")
    chunks_dir = os.path.join(output_base_dir, "chunks")
    chunk_json_dir = os.path.join(output_base_dir, "chunk_jsons")
    merged_output_dir = os.path.join(output_base_dir, "final_output")

    os.makedirs(contracts_txt_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)
    os.makedirs(chunk_json_dir, exist_ok=True)
    os.makedirs(merged_output_dir, exist_ok=True)

    # Step 1: 合约工程读取 -> 合并为 txt
    convert_contracts_to_txt(bridge_pro_dir, contracts_txt_dir, bridge_name)
    bridge_txt_path = os.path.join(contracts_txt_dir, f"{bridge_name}.txt")

    # Step 2: 拆分 txt 为 chunk 文件
    split_integrated_project(bridge_txt_path, chunks_dir, max_tokens=20000)

    # Step 3: 并行分析每个 chunk
    chunk_txt_paths = sorted(glob.glob(os.path.join(chunks_dir, "*.txt")))
    chunk_args = []
    for chunk_txt_path in chunk_txt_paths:
        chunk_args.append((
            chunk_txt_path,
            chunk_json_dir,
            bridge_name,
            bridge_pro_dir,
            model_type
        ))

    with multiprocessing.Pool(processes=min(8, len(chunk_args))) as pool:
        pool.starmap(process_single_chunk, chunk_args)

    # Step 4: 合并所有 chunk 分析结果为最终 JSON
    analyze_merge_chunks_with_llm(
        chunk_json_dir=chunk_json_dir,
        output_dir=merged_output_dir,
        bridge_name=bridge_name,
        bridge_dir=bridge_pro_dir,
        model_type=model_type
    )


if __name__ == "__main__":
    # 示例调用参数
    bridge_project_path = "../dataset1/vul_data/anyswapv4/contracts"
    output_dir = "./analysis_output"
    bridge_name = "anyswapv4"
    model_type = "aliyun"  # 例如：openai 或 Qwen/QwQ-32B 或 aliyun

    run_full_bridge_analysis(
        bridge_pro_dir=bridge_project_path,
        output_base_dir=output_dir,
        bridge_name=bridge_name,
        model_type=model_type
    )

    # 依赖分析
    dependence_analysis(
        input_blg_path="./analysis_output/final_output/anyswapv4_merged.json",
        contract_base_path="../dataset1/vul_data/anyswapv4/contracts",
        output_res_path="./analysis_output/final_output"
    )
