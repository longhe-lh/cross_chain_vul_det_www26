import json
import logging

from global_config.global_config import LLM_MODEL_NAME
from utils.llm_helper.config import validate_config
from utils.llm_helper.llm_api import call_llm_api, extract_json_from_response
from utils.llm_helper.prompts import get_system_prompt, get_analysis_prompt, get_refinement_prompt, \
    get_split_system_prompt, get_split_analysis_prompt, get_merge_system_prompt, get_merge_analysis_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_split_bridge_contract(contract_code, bridge_name="CrossChainBridge", model_type=None, output=None,
                                  report=False):
    """
    拆分模式：分析单个代码片段的跨链合约逻辑，供外部调用
    """
    validate_config(model_type)
    if not contract_code.strip():
        raise ValueError("合约代码为空")
    result = analyze_split_contract(contract_code, bridge_name, model_type)
    if "err_log" in result:
        raise RuntimeError(f"分析过程中发生错误: {result['err_log']}")
    if output:
        save_analysis_result(result, output)
    report_content = None
    if report:
        report_content = generate_analysis_report(result)
        if output:
            report_file = output.replace('.json', '_report.md')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
    return result, report_content


def analyze_split_contract(contract_code, bridge_name="CrossChainBridge", model_type=None):
    """
    拆分模式：分析单个跨链桥代码片段
    """
    try:
        logger.info(f"开始拆分分析跨链桥合约片段: {bridge_name}")
        messages = [
            {"role": "system", "content": get_split_system_prompt()},
            {"role": "user", "content": get_split_analysis_prompt(contract_code)}
        ]
        response = call_llm_api(messages, model_type)
        analysis_result = extract_json_from_response(response)
        if not analysis_result:
            logger.error("无法从响应中提取JSON结果")
            return {"err_log": "无法解析大模型响应"}
        return analysis_result
    except Exception as e:
        logger.error(f"分析过程中发生错误: {str(e)}")
        return {"err_log": str(e)}


def analyze_merge_bridge_chunks(all_chunk_json, bridge_name="CrossChainBridge", model_type=None, output=None, report=False):
    """
    合并模式：合并多个分析片段的 JSON，重构完整桥逻辑
    """
    validate_config(model_type)
    if not all_chunk_json.strip():
        raise ValueError("输入的 JSON 合约片段为空")
    result = analyze_merge_contract(all_chunk_json, bridge_name, model_type)
    if "err_log" in result:
        raise RuntimeError(f"合并分析过程中发生错误: {result['err_log']}")
    if output:
        save_analysis_result(result, output)
    report_content = None
    if report:
        report_content = generate_analysis_report(result)
        if output:
            report_file = output.replace('.json', '_report.md')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
    return result, report_content


def analyze_merge_contract(all_chunk_json, bridge_name="CrossChainBridge", model_type=None):
    """
    合并模式：合并多个合约分析 JSON 片段为一个完整结构
    """
    try:
        logger.info(f"开始合并分析跨链桥合约: {bridge_name}")
        messages = [
            {"role": "system", "content": get_merge_system_prompt()},
            {"role": "user", "content": get_merge_analysis_prompt(all_chunk_json)}
        ]
        response = call_llm_api(messages, model_type)
        merged_result = extract_json_from_response(response)
        if not merged_result:
            logger.error("无法从响应中提取合并后的JSON结果")
            return {"err_log": "无法解析大模型响应"}
        return merged_result
    except Exception as e:
        logger.error(f"合并分析过程中发生错误: {str(e)}")
        return {"err_log": str(e)}


def analyze_bridge_contract(contract_code, bridge_name="CrossChainBridge", model_type=None, output=None, report=False):
    """
    分析合约主流程，供外部调用
    """
    validate_config(model_type)
    if not contract_code.strip():
        raise ValueError("合约代码为空")
    result = analyze_contract(contract_code, bridge_name, model_type)
    if "err_log" in result:
        raise RuntimeError(f"分析过程中发生错误: {result['err_log']}")
    if output:
        save_analysis_result(result, output)
    report_content = None
    if report:
        report_content = generate_analysis_report(result)
        if output:
            report_file = output.replace('.json', '_report.md')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
    return result, report_content


def analyze_contract(contract_code, bridge_name="CrossChainBridge", model_type=None):
    try:
        logger.info(f"开始分析跨链桥合约: {bridge_name}")
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": get_analysis_prompt(contract_code, bridge_name)}
        ]
        response = call_llm_api(messages, model_type)
        analysis_result = extract_json_from_response(response)
        if not analysis_result:
            logger.error("无法从响应中提取JSON结果")
            return {"err_log": "无法解析大模型响应"}
        # valid, msg = validate_analysis_result(analysis_result)
        # if not valid:
        #     logger.warning(f"分析结果格式校验失败: {msg}")
        #     analysis_result = refine_analysis_result(contract_code, analysis_result, msg, model_type)
        # logger.info("跨链桥合约分析完成")
        return analysis_result
    except Exception as e:
        logger.error(f"分析过程中发生错误: {str(e)}")
        return {"err_log": str(e)}


def validate_analysis_result(result):
    """
    校验分析结果的结构和主要字段，返回 (True, msg) 或 (False, 错误信息)
    """
    if not isinstance(result, dict):
        return False, "The analysis result is not of dictionary type"
    if not result:
        return False, "The analysis result is empty"
    # 只校验顶层结构和主要字段
    for bridge_name, bridge_data in result.items():
        if not isinstance(bridge_data, dict):
            return False, f"Bridge {bridge_name} data is not a dictionary"
        for key in ["interoperability", "roles", "src_chain", "rel_chain", "det_chain"]:
            if key not in bridge_data:
                return False, f"Bridge {bridge_name} Missing field: {key}"
        # 校验 roles
        rolers = bridge_data["roles"]
        if not isinstance(rolers, dict):
            return False, f"The roles of the bridge {bridge_name} are not dictionaries"
        for role in ["src_chain", "rel_chain", "det_chain"]:
            if role not in rolers:
                return False, f"The roles of the bridge {bridge_name} are missing: {role}"
        # 校验链结构
        for chain_key in ["src_chain", "rel_chain", "det_chain"]:
            chain = bridge_data[chain_key]
            if not isinstance(chain, dict):
                return False, f"The {chain_key} of the bridge {bridge_name} is not a dictionary"
            if "chain_name" not in chain:
                return False, f"The {chain_key} of the bridge {bridge_name} is missing chain_name"
            if "events" not in chain:
                return False, f"The {chain_key} of the bridge {bridge_name} is missing events"
    return True, "Correct format"


def refine_analysis_result(contract_code, original_result, feedback, model_type=LLM_MODEL_NAME):
    try:
        logger.info("尝试优化分析结果...")
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user",
             "content": get_refinement_prompt(contract_code, json.dumps(original_result, ensure_ascii=False, indent=2),
                                              feedback)}
        ]
        response = call_llm_api(messages, model_type)
        refined_result = extract_json_from_response(response)
        if refined_result:
            logger.info("分析结果优化成功")
            return refined_result
        else:
            logger.warning("无法优化分析结果，返回原始结果")
            return original_result
    except Exception as e:
        logger.error(f"优化分析结果时发生错误: {str(e)}")
        return original_result


def save_analysis_result(result, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"分析结果已保存到: {output_file}")
    except Exception as e:
        logger.error(f"保存分析结果时发生错误: {str(e)}")


def load_json_result(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        logger.info(f"分析结果已从文件加载: {input_file}")
        return result
    except Exception as e:
        logger.error(f"加载分析结果时发生错误: {str(e)}")
        return {"err_log": str(e)}


def compare_analysis_results(result1, result2):
    try:
        comparison = {
            "similarity_score": 0.0,
            "differences": [],
            "common_elements": []
        }

        def extract_events(result):
            events = set()
            for bridge_name, bridge_data in result.items():
                for chain_type in ["src_chain", "rel_chain", "det_chain"]:
                    if chain_type in bridge_data:
                        chain_events = bridge_data[chain_type].get("events", {})
                        for event_name in chain_events.keys():
                            events.add(f"{chain_type}_{event_name}")
            return events

        events1 = extract_events(result1)
        events2 = extract_events(result2)
        if events1 or events2:
            intersection = events1.intersection(events2)
            union = events1.union(events2)
            comparison["similarity_score"] = len(intersection) / len(union) if union else 0.0
            comparison["common_elements"] = list(intersection)
            comparison["differences"] = {
                "only_in_result1": list(events1 - events2),
                "only_in_result2": list(events2 - events1)
            }
        return comparison
    except Exception as e:
        logger.error(f"比较分析结果时发生错误: {str(e)}")
        return {"err_log": str(e)}


def generate_analysis_report(result):
    try:
        report = []
        report.append("# 跨链桥合约分析报告\n")
        for bridge_name, bridge_data in result.items():
            report.append(f"## 跨链桥: {bridge_name}\n")
            interoperability = bridge_data.get("interoperability", "unknown")
            report.append(f"**跨链类型**: {interoperability}\n")
            rolers = bridge_data.get("roles", {})
            report.append("### 角色分析\n")
            for role, events in rolers.items():
                if events:
                    report.append(f"- **{role}**: {', '.join(events)}\n")
            for chain_type in ["src_chain", "rel_chain", "det_chain"]:
                chain_data = bridge_data.get(chain_type, {})
                chain_name = chain_data.get("chain_name", "Unknown")
                events = chain_data.get("events", {})
                report.append(f"### {chain_type}: {chain_name}\n")
                if events:
                    for event_name, event_data in events.items():
                        report.append(f"- **事件**: {event_name}\n")
                        for func_id, func_data in event_data.items():
                            func_name = func_data.get("func_name", "Unknown")
                            key_ops = func_data.get("key_ops", [])
                            report.append(f"  - 函数: {func_name}\n")
                            if key_ops:
                                report.append(f"  - 关键操作: {', '.join(key_ops)}\n")
                else:
                    report.append("- 无事件\n")
            report.append("---\n")
        return "".join(report)
    except Exception as e:
        logger.error(f"生成分析报告时发生错误: {str(e)}")
        return f"生成报告时发生错误: {str(e)}"
