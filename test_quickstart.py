# ============================================================
# 文件：test_quickstart.py
# 作用：跑通 LangGraph 官方 Quickstart 示例，理解核心概念
# 运行方式：python test_quickstart.py
# ============================================================
# 导入类型注解相关模块（用于定义 State 的数据结构）
from typing import Annotated
from typing_extensions import TypedDict

# 导入 LangGraph 核心类
from langgraph.graph import StateGraph, START, END
# add_messages 是一个“归约器”，用于将新消息追加到消息列表中，而不是覆盖
from langgraph.graph.message import add_messages

# 导入Langgraph的OpenAI兼容客户端（用于调用DeepSeek V4 Flash模型）
from langchain_openai import ChatOpenAI

# 导入操作系统和dotenv模块，用于读取.env文件中的API Key
import os
from dotenv import load_dotenv


# 加载.env文件中的环境变量（如 DEEPSEEK_API_KEY），确保在运行前已创建.env文件并写入API Key
load_dotenv()


# 第1步：定义状态state
# state是所有节点共享的“数据容器”，类似一个全局的字典
# TypeDict只是做类型提示，不强制检查
class State(TypedDict):
    # message 字段存储对话历史
    # Annotated[list, add_messages] 表示这是一个列表类型，并且在更新时使用 add_messages 归约器追加
    messages: Annotated[list,add_messages]  # 消息列表，存储对话历史

# 第2步：创建LLM实例
# ChatOpenAI是LangChain提供的通用OpenAI兼容客户端，这里调用的是DeepSeek V4 Flash模型
llm = ChatOpenAI(
    model="deepseek-v4-flash",  # 模型名称
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 读取环境变量中的API Key
    base_url="https://api.deepseek.com/v1", # DeepSeek API的基础URL
    temperature=0.3,    # 控制输出随机性（0~1，越低越确定）
    extra_body={
        "thinking": {"type": "enabled"},    # 启用深度思考
        "reasoning_effort": "high"  # 设置推理强度为高
    }
)

# 第3步：定义节点函数Nodes
# 节点就是普通的Python函数，只要符合输入输出规范，就可以被LangGraph调用
# 它接收当前状态，然后返回更新后的状态（部分或全部）
def chatbot(state: State):
    """
    这是最简单的节点：把用户消息发给LLM，得到回复后将回复追加到message中
    """
    # state["messages"]是当前对话的历史列表
    # llm.invoke()会调用DS API，并返回一个完整的响应对象
    response = llm.invoke(state["messages"])

    # 返回一个字典, Langgraph会自动将它合并到当前状态中
    # 这里我们将新的响应消息放到message列表的末尾
    return {
        "messages": [response]
    }

# 第4步：创建状态图StateGraph
# StateGraph是图的构建器，它接收状态类型为参数
graph_builder = StateGraph(State)

# 将chatbot函数注册为一个名为“chatbot”的节点
graph_builder.add_node(chatbot, name="chatbot")

# 添加边：从START（图的入口）到chatbot节点
graph_builder.add_edge(START, "chatbot")

# 再从chatbot节点到END
graph_builder.add_edge("chatbot", END)

# 第5步：编译图
# 编译会做基本的检查（比如节点是否存在），并生成可运行的图对象
graph = graph_builder.compile()

# 第6步：运行测试
if __name__ == "__main__":
    # invoke()是运行图的主要方法，需传入初始状态
    # 初始状态是一个字典，至少包含message字段
    result = graph.invoke({
        "messages": [{"role": "user", "content": "你好，请介绍一下LangGraph是什么？"}]
    })

    # 打印最后一条消息的内容（即LLM的回复）
    print(result["messages"][-1].content)
