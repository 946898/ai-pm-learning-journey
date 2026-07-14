# ============================================================
# 文件：graph/agent.py
# 作用：组装 StateGraph，定义节点、边和条件边，编译成可运行的 Agent
# ============================================================

from typing import Literal
from langgraph.graph import StateGraph, START, END
from graph.nodes import parser_order, risk_analysis, supplier_verify
from graph.state import OrderState

# 两个终端节点，只打印日志并设置最终决策
def auto_approve(state: OrderState) -> dict:
    """
    终端节点：低/中风险订单自动通过
    """
    print(f"√ 订单{state.get('order_id', '未知')}已自动通过。")
    return{
        "final_decision": "pass",
        "requires_human_review": False
    }

def human_review(state: OrderState) -> dict:
    """
    终端节点：高风险订单需人工复核
    """
    print(f"× 订单{state.get('order_id', '未知')}需人工复核。")
    return{
        "final_decision": "wait check",
        "requires_human_review": True
    }

# 条件边路由函数
def route_after_verify(state: OrderState) -> Literal["auto_approve", "human_review"]:
    """
    根据供应商风险等级决定走哪个节点
    """

    risk_data = state.get("supplier_risk_data", {})
    risk_level = risk_data.get("risk_level", "低风险")

    # ----- 调试打印 -----
    print(f" [DEBUG] supplier_risk_data: {risk_data}")
    print(f" [DEBUG] risk_level: {risk_level}")
    # -------------------


    # 高风险 -> 人工复核，否则自动通过
    if risk_level == "高风险":
        return "human_review"
    else:
        return "auto_approve"
    
# 构建图
# 创建图构建器, 传入状态类型
graph_builder = StateGraph(OrderState)

# 添加所有节点
graph_builder.add_node("parser_order", parser_order)
graph_builder.add_node("risk_analysis", risk_analysis)
graph_builder.add_node("supplier_verify", supplier_verify)
graph_builder.add_node("auto_approve", auto_approve)
graph_builder.add_node("human_review", human_review)

# 添加普通边
graph_builder.add_edge(START, "parser_order")
graph_builder.add_edge("parser_order", "risk_analysis")
graph_builder.add_edge("risk_analysis", "supplier_verify")

# 添加条件边
graph_builder.add_conditional_edges(
    "supplier_verify",  # 从哪一个节点出发
    route_after_verify,
    {
        "auto_approve": "auto_approve",   # 若返回“auto_approve” -> 去auto_approve节点
        "human_review": "human_review"    # 若返回“human_review” -> 去human_review节点
    }
)

# 两个终端节点都指向END（结束）
graph_builder.add_edge("auto_approve", END)
graph_builder.add_edge("human_review", END)

# 编译图
agent = graph_builder.compile()
