# ============================================================
# 文件：run_agent.py（放在项目根目录）
# 作用：运行采购审核 Agent
# 运行方式：python run_agent.py
# ============================================================

from graph.agent import agent   # 导入编译好的图
from graph.state import OrderState # 导入状态类型
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from pathlib import Path

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
    # 每个文件使用唯一的 thread_id
    config = {"configurable": {"thread_id": f"order-{file_path}"}}
    final_state = agent.invoke(initial_state, config=config)

    
    # 在每次处理完文件后，创建表格
    console = Console()

    # 创建表格
    table = Table(title=f"审核报告 - {Path(file_path).name}", box=box.ROUNDED, show_header=True,header_style="bold cyan")

    # 添加列
    table.add_column("字段", style="bold yellow", width=14)
    table.add_column("值", style="green", width=14)

    # 添加行
    table.add_row("订单号", final_state.get("order_id", "N/A"))
    table.add_row("供应商", final_state.get("supplier_name", "N/A"))
    table.add_row("风险等级", final_state.get("risk_level", "N/A"))
    table.add_row("风险评分", str(final_state.get("risk_score", "N/A")))
    table.add_row("风险点", "\n".join(final_state.get("risk_points", [])) or "无")
    table.add_row("最终决策", final_state.get("final_decision", "N/A"))

    # 打印表格
    console.print(table)

    # 如果通过/驳回，显示一个带颜色的状态
    
    if final_state.get("requires_human_review"):
        console.print(Panel("待人工复核", style="bold yellow"))
        
    elif final_state.get("final_decision") == "通过":
        console.print(Panel("审核通过", style="bold green"))
    elif final_state.get("final_decision") == "驳回":
        console.print(Panel("审核驳回"), style="bold red")
    else:
        console.print(Panel("审核通过", style="bold green"))