import json
import logging
import time

from global_config.global_config import LLM_MODEL_NAME
from utils.llm_helper.llm_api import call_llm_api
from utils.llm_helper.prompts import get_lm_teacher_prompt
from lm_helper import extract_causes_from_jsonl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lm_tea_kn_extr(input_path, output_path, error_log_path, model_type="deepseek"):
    with open(input_path, 'r', encoding='utf-8') as f, \
            open(output_path, 'w', encoding='utf-8') as out_f, \
            open(error_log_path, 'w', encoding='utf-8') as err_f:

        for idx, line in enumerate(f, 1):
            item = json.loads(line)
            messages = get_lm_teacher_prompt(item)

            try:
                response_text = call_llm_api(messages, model_type=model_type, temperature=0.3, max_tokens=1024)
                cleaned = response_text.strip().strip("```json").strip("```").strip()
                result = json.loads(cleaned)
                print(result)
                out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
                print(f"[✓] Sample {idx} done.")
            except Exception as e:
                print(f"[✗] Error on sample {idx}: {e}")
                err_f.write(f"Sample {idx} Error:\n{str(e)}\nPrompt:\n{messages[1]['content']}\n{'=' * 80}\n")
            time.sleep(1.2)

    print("✅ All Done. Augmented data saved to:", output_path)


if __name__ == '__main__':
    # 调用大模型知识提取
    lm_tea_kn_extr(
        input_path="./input/cross_chain_data.jsonl",
        output_path="./output/data.jsonl",
        error_log_path="./err_log/err_log.txt",
        model_type=LLM_MODEL_NAME
    )

    # 提取 lm_teacher 中生成的规则
    try:
        num = extract_causes_from_jsonl(
            jsonl_path="./output/data.jsonl",
            output_path="rule/rules.jsonl"
        )
        print(f"规则提取并追加完成 ✅ 共写入 {num} 条规则")
    except Exception as e:
        print(f"错误：{e}")

