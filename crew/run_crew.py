# ============================================================
# 文件：crew/run_crew.py
# 作用：运行三 Agent 协同工作流
# 运行方式：python -m crew.run_crew
# ============================================================

import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from crewai import Crew
from crew.agents import audit_agent, risk_agent, exception_agent
from crew.task import parse_task, risk_task, exception_task


# ---- 创建 Crew ----
# 按顺序执行：parse → risk → exception（仅当高风险时触发）
order_crew = Crew(
    agents=[audit_agent, risk_agent, exception_agent],
    tasks=[parse_task, risk_task, exception_task],
    verbose=True,
)


# ---- 运行测试 ----
if __name__ == "__main__":
    # 模拟用户输入：一个高风险供应商的订单
    input_data = {
        "order_info": "供应商：鑫达物流，金额：125000元，交货日期：2026-08-15"
    }
    
    print("=" * 50)
    print("🚀 启动三 Agent 协同工作流")
    print("=" * 50)
    
    result = order_crew.kickoff(inputs=input_data)
    
    print("\n" + "=" * 50)
    print("✅ 工作流完成，最终输出：")
    print("=" * 50)
    print(result)