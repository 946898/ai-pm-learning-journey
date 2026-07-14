# ============================================================
# 文件：graph/llm_client.py
# 作用：提供一个工厂函数，用于创建配置好的 DeepSeek LLM 实例
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 读取 .env 文件中的环境变量，确保在运行前已创建 .env 文件并写入 DEEPSEEK_API_KEY
load_dotenv()

def get_deepseek_llm(temperature=0.3, reasoning_effort="medium"):
    """
    返回配置好的 DeepSeek V4 Flash LLM 实例，供 LangGraph 节点调用
    """

    extra_body = {
        "thinking": {"type": "enabled"},  # 启用深度思考
        "resoning_effort": reasoning_effort  # 设置推理强度（low, medium, high）
    }


    return ChatOpenAI(
        model="deepseek-v4-flash",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        temperature=temperature, # 输出随机性
        model_kwargs={"extra_body": extra_body} # 深度思考和推理强度通过 model_kwargs 传递
    )

