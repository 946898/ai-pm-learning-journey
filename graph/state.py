# ============================================================
# 文件：graph/state.py
# 作用：定义采购订单审核 Agent 的状态数据结构
# ============================================================

from typing import TypedDict, Optional, List, Annotated
from langgraph.graph.message import add_messages


class OrderState(TypedDict):
    """
    采购订单审核 Agent 的状态数据结构
    这是整个Agent的“共享内容”，所有节点都能读写这些字段
    """

    # 对话相关（支持多轮交互）
    # messages 字段存储对话历史，使用 add_messages 归约器追加新消息
    messages: Annotated[list, add_messages]  # 消息列表，存储对话历史

    # 输入文件
    file_path: Optional[str]    # Day5新增，输入的文件路径

    # 订单输入数据
    # 由第一个节点(parser_order)填充
    order_id: Optional[str]  # 当前处理的订单 ID
    supplier_name: Optional[str]  # 供应商名称
    total_mount: Optional[float]  # 订单总金额
    delivery_date: Optional[str]  # 交货日期
    contract_clauses: Optional[list[str]]  # 合同条款列表
    
    # 中间计算结果
    # 由risk_analysis节点计算并填充
    risk_score: Optional[int]  # 风险评分（0~100，越高风险越大）
    risk_level: Optional[str]  # 风险等级（低、中、高）
    risk_points: Optional[List[str]]  # 风险点列表（如“供应商信用不足”、“交货延迟风险”等）
    
    # 供应商核验结果
    # 由supplier_verify节点计算并填充
    supplier_risk_data: Optional[dict]  # check_supplier_risk函数返回，供应商风险数据（如信用评分、历史违约记录等）

    # 最终决策
    # 由条件边后的终端节点填充
    final_decision: Optional[str]  # 最终审核决策（批准、拒绝、需要人工复核）
    final_reason: Optional[str]  # 决策理由
    requires_human_review: Optional[bool]  # 是否需要人工复核, 默认false
   
