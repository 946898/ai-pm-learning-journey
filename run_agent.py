# ============================================================
# 文件：run_agent.py（放在项目根目录）
# 作用：运行采购审核 Agent
# 运行方式：python run_agent.py
# ============================================================

from graph.agent import agent   # 导入编译好的图
from graph.state import OrderState # 导入状态类型

# 第1步：Day5新增，指定要处理的文件
INPUT_FILE = ["mock_order.xlsx","mock_contract.pdf"]


# 第2步：构造初始状态（所有字段必须符合OrderState定义）
for file_path in INPUT_FILE:
    initial_state = OrderState(
        # 对话历史
        messages=[],

        file_path = file_path, # Day5新增，指定输入文件

        # 订单相关字段
        order_id="",
        total_mount=0.0,
        supplier_name="",
        delivery_date="",
        contract_clauses="",

        # 风险相关字段
        risk_level=None,
        risk_points=[],
        risk_score=None,
        
        # 供应商校验数据
        supplier_risk_data=None,

        # 最终决策（初始为空）
        final_decision=None,
        final_reason=None,
        requires_human_review=False
    )

    # 第3步：运行Agent
    print(f"正在处理文件：{INPUT_FILE}")
    print("-" * 50)

    # 调用invoke()运行图，传入初始状态
    # 返回最终状态，包含所有节点更新后的完整数据
    final_state = agent.invoke(initial_state)

    # 打印最终决策
    print("-" * 50)
    print(f"\n最终决策：{final_state.get('final_decision')}")
    print(f"是否需要人工复核: {final_state.get('requires_human_review')}")