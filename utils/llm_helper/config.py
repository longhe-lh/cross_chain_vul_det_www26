import os
from dotenv import load_dotenv


def load_env():
    load_dotenv()


load_env()


def get_config():
    return {
        # 硅基流动
        "SiliconCloud_API_KEY": os.getenv("SiliconCloud_API_KEY", ""),
        "SiliconCloud_BASE_URL": os.getenv("SiliconCloud_BASE_URL", "https://api.siliconflow.cn/v1/chat/completions"),
        "SiliconCloud_MODEL": os.getenv("SiliconCloud_MODEL", "Qwen/QwQ-32B"),
        # OpenAI
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4"),
        # 百度AI
        "BAIDU_API_KEY": os.getenv("BAIDU_API_KEY", ""),
        "BAIDU_SECRET_KEY": os.getenv("BAIDU_SECRET_KEY", ""),
        "BAIDU_BASE_URL": os.getenv("BAIDU_BASE_URL",
                                    "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"),
        # 阿里云AI
        "ALIYUN_API_KEY": os.getenv("ALIYUN_API_KEY", ""),
        "ALIYUN_BASE_URL": os.getenv("ALIYUN_BASE_URL",
                                     "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"),
        "ALIYUN_BASE_MODEL": os.getenv("ALIYUN_BASE_MODEL", "qwen-turbo"),

        # DeepSeek AI
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY", ""),
        "DEEPSEEK_BASE_URL": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1/chat/completions"),
        "DEEPSEEK_MODEL": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),

        # 默认使用 Qwen
        "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "Qwen/QwQ-32B")
    }


def validate_config(model_type=None):
    cfg = get_config()
    model_type = model_type or cfg["DEFAULT_MODEL"]
    if model_type == "openai" and not cfg["OPENAI_API_KEY"]:
        raise ValueError("OpenAI API Key 未设置")
    elif model_type == "baidu" and (not cfg["BAIDU_API_KEY"] or not cfg["BAIDU_SECRET_KEY"]):
        raise ValueError("百度文心 API Key 或 Secret Key 未设置")
    elif model_type == "aliyun" and not cfg["ALIYUN_API_KEY"]:
        raise ValueError("阿里通义 API Key 未设置")
    elif model_type == "Qwen/QwQ-32B" and not cfg["SiliconCloud_API_KEY"]:
        raise ValueError("通义千问 API Key 未设置")
    elif model_type == "deepseek" and not cfg["DEEPSEEK_API_KEY"]:
        raise ValueError("DeepSeek API Key 未设置")
