# ============================================================
# 文件：crew/agents.py
# 作用：定义三个专用 Agent：审核 Agent、风控 Agent、异常 Agent
# ============================================================

import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from crewai import Agent, LLM # 从crewai导入Agent、LLM类
from crewai.tools import tool   # 导入tool装饰器
from tools.supplier_risk_check import check_supplier_risk
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()   # 加载.env文件

# 创建DS LLM 实例
deepseek_llm = LLM(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
    stream=False,
    extra_body={
        "thinking": {"type": "enabled"},
        "reasoning_effort": "medium"
    }
)


# ---使用装饰器将函数转化为工具
@tool("check_supplier_risk")    # 明确指定工具名称
def supplier_risk_tool(supplier_name: str) -> str:
    """
    查询供应商的履约风险，包括历史交货延迟率、质量合格率、资质到期日。
    参数 supplier_name: 供应商全称，如'华诚供应链'
    """
    import json
    result = check_supplier_risk(supplier_name)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ---- Agent 1：审核 Agent ----
# 负责解析订单信息，提取关键字段
audit_agent = Agent(
    role="采购订单审核专员",
    goal="准确解析采购订单信息，提取供应商名称、金额、交货日期等关键字段",
    backstory="""你是一名经验丰富的采购订单审核专员，擅长从各种格式的订单中
    提取关键信息，并对订单的完整性和规范性进行初步判断。""",
    verbose=True,   # 是否打印日志，默认为False
    allow_delegation=False, # 是否允许将任务委托给其他Agent，默认为False
    max_iter=10,    # 最大迭代10次
    llm=deepseek_llm
)


# ---- Agent 2：风控 Agent ----
# 负责评估供应商风险，调用 check_supplier_risk 工具
risk_agent = Agent(
    role="供应商风控专员",
    goal="评估供应商的履约风险，包括历史交货延迟率、质量合格率等",
    backstory="""你是一名资深的风控专员，擅长通过数据分析供应商的风险状况。
    你会调用供应商风险查询工具来获取数据，并根据数据做出判断。""",
    verbose=True,
    allow_delegation=False,
    max_iter=10,    # 最大迭代10次
    tools=[supplier_risk_tool],  # 没法直接绑定工具函数，传入的工具函数
    cache=True,  # 启用工具缓存
    llm=deepseek_llm
)


# ---- Agent 3：异常 Agent ----
# 负责处理高风险订单，生成异常处理建议
exception_agent = Agent(
    role="异常处理专员",
    goal="针对高风险订单，生成详细的异常处理建议和应对方案",
    backstory="""你是一名经验丰富的异常处理专家，专门处理高风险采购订单。
    你会分析风险原因，提出具体的应对措施和替代方案。""",
    verbose=True,
    allow_delegation=False,
    max_iter=10,    # 最大迭代10次
    llm=deepseek_llm
)