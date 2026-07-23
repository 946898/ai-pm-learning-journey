# ============================================================
# 文件：crew/tasks.py
# 作用：定义三个 Task，对应三个 Agent 的工作
# ============================================================

from crewai import Task
from crew.agents import audit_agent, risk_agent, exception_agent


# ---- Task 1：订单解析 ----
# 由 audit_agent 执行
parse_task = Task(
    description="""解析用户提供的采购订单信息:{order_info}。
    从订单中提取以下字段：
    - 供应商名称（supplier_name）
    - 订单总金额（total_amount）
    - 交货日期（delivery_date）
    - 合同条款（contract_clause）
    
    如果信息不完整，请标记缺失字段。""",
    expected_output="""结构化的订单信息：
    {
        "supplier_name": "xxx",
        "total_amount": xxx,
        "delivery_date": "xxxx-xx-xx",
        "contract_clause": "xxx"
    }""",
    agent=audit_agent  # 分配给 audit_agent，传入实例not str
)


# ---- Task 2：供应商风险评估 ----
# 由 risk_agent 执行，会调用 check_supplier_risk 工具
risk_task = Task(
    description="""基于供应商名称（从上一个任务的结果中获取supplier_name），**必须调用供应商风险查询工具（check_supplier_risk）**来获取风险数据。
    需要获取：
    - 历史交货延迟率
    - 质量合格率
    - 资质到期日
    - 综合风险等级（低/中/高）
    
    如果供应商在数据库中不存在，标记为"未知供应商，建议人工核实"。""",
    expected_output="""供应商风险报告：
    {
        "supplier_name": "xxx",
        "delay_rate": x.xx,
        "quality_pass_rate": x.xx,
        "cert_expire": "xxxx-xx-xx",
        "risk_level": "低/中/高"
    }""",
    agent=risk_agent    # 传入实例not str
)


# ---- Task 3：异常处理 ----
# 由 exception_agent 执行，仅在风险等级为"高风险"时触发
exception_task = Task(
    description="""基于上一个任务（供应商风险评估）的结果，针对高风险供应商生成异常处理建议。
    建议应包括：
    1. 风险原因分析
    2. 具体应对措施（如：启动备选供应商、重新谈判条款等）
    3. 后续跟进建议""",
    expected_output="""异常处理报告：
    {
        "risk_analysis": "xxx",
        "countermeasures": ["措施1", "措施2", ...],
        "follow_up": "xxx"
    }""",
    agent=exception_agent   # 传入实例not str
)