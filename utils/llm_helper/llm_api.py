import json
import requests
import re
from openai import OpenAI
from utils.llm_helper.config import get_config


def call_llm_api(messages, model_type=None, **kwargs):
    config = get_config()
    model_type = model_type or config["DEFAULT_MODEL"]
    if model_type == "openai":
        return call_openai_api(messages, config, **kwargs)
    elif model_type == "baidu":
        return call_baidu_api(messages, config, **kwargs)
    elif model_type == "aliyun":
        return call_aliyun_api(messages, config, **kwargs)
    elif model_type == "Qwen/QwQ-32B":
        return call_siliconcloud_api(messages, config, **kwargs)
    elif model_type == "deepseek":
        return call_deepseek_api(messages, config, **kwargs)
    else:
        raise ValueError(f"不支持的大模型类型: {model_type}")


def extract_json_from_response(response):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        brace_match = re.search(r'\{.*\}', response, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass
    return None


def call_openai_api(messages, config, **kwargs):
    client = OpenAI(api_key=config["OPENAI_API_KEY"], base_url=config["OPENAI_BASE_URL"])
    try:
        response = client.chat.completions.create(
            model=config["OPENAI_MODEL"],
            messages=messages,
            temperature=kwargs.get('temperature', 0.1),
            max_tokens=kwargs.get('max_tokens', 4000),
            **kwargs
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API调用失败: {str(e)}")


def call_baidu_api(messages, config, **kwargs):
    access_token = get_baidu_access_token(config)
    url = f"{config['BAIDU_BASE_URL']}?access_token={access_token}"
    baidu_messages = []
    for msg in messages:
        if msg["role"] == "user":
            baidu_messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            baidu_messages.append({"role": "assistant", "content": msg["content"]})
        elif msg["role"] == "system":
            if baidu_messages and baidu_messages[-1]["role"] == "user":
                baidu_messages[-1]["content"] = msg["content"] + "\n\n" + baidu_messages[-1]["content"]
            else:
                baidu_messages.append({"role": "user", "content": msg["content"]})
    payload = {
        "messages": baidu_messages,
        "temperature": kwargs.get('temperature', 0.1),
        "max_output_tokens": kwargs.get('max_tokens', 4000)
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("result", "")
        else:
            raise Exception(f"百度API调用失败: {response.text}")
    except Exception as e:
        raise Exception(f"百度API调用失败: {str(e)}")


def get_baidu_access_token(config):
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": config["BAIDU_API_KEY"],
        "client_secret": config["BAIDU_SECRET_KEY"]
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("获取百度访问令牌失败")


def call_aliyun_api(messages, config, **kwargs):
    url = config["ALIYUN_BASE_URL"]
    headers = {
        "Authorization": f"Bearer {config['ALIYUN_API_KEY']}",
        "Content-Type": "application/json"
    }
    aliyun_messages = []
    for msg in messages:
        if msg["role"] in ["user", "assistant"]:
            aliyun_messages.append({"role": msg["role"], "content": msg["content"]})
        elif msg["role"] == "system":
            if aliyun_messages and aliyun_messages[-1]["role"] == "user":
                aliyun_messages[-1]["content"] = msg["content"] + "\n\n" + aliyun_messages[-1]["content"]
            else:
                aliyun_messages.append({"role": "user", "content": msg["content"]})
    payload = {
        "model": config['ALIYUN_BASE_MODEL'],
        "input": {"messages": aliyun_messages},
        "parameters": {
            "temperature": kwargs.get('temperature', 0.0),
            "max_tokens": kwargs.get('max_tokens', 4000)
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("text", "")
        else:
            raise Exception(f"阿里通义API调用失败: {response.text}")
    except Exception as e:
        raise Exception(f"阿里通义API调用失败: {str(e)}")


def call_siliconcloud_api(messages, config, **kwargs):
    url = config["SiliconCloud_BASE_URL"]
    headers = {
        "Authorization": f"Bearer {config['SiliconCloud_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": config["SiliconCloud_MODEL"],
        "messages": messages,
        "temperature": kwargs.get('temperature', 0.1),
        "max_tokens": kwargs.get('max_tokens', 4000)
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"SiliconCloud API调用失败: {response.text}")
    except Exception as e:
        raise Exception(f"SiliconCloud API调用失败: {str(e)}")


def call_deepseek_api(messages, config, **kwargs):
    url = config['DEEPSEEK_BASE_URL']
    headers = {
        "Authorization": f"Bearer {config['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": config['DEEPSEEK_MODEL'],
        "messages": messages,
        "temperature": kwargs.get('temperature', 0.3),
        "max_tokens": kwargs.get('max_tokens', 1024)
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"DeepSeek API调用失败: {response.text}")
    except Exception as e:
        raise Exception(f"DeepSeek API调用失败: {str(e)}")
