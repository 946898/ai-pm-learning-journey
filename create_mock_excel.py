# ============================================================
# 文件：create_mock_excel.py（根目录，一次性运行）
# 作用：生成一个测试用的 Excel 采购订单文件
# 运行：python create_mock_excel.py
# ============================================================

import pandas as pd

# 准备数据
data = [{
    "订单编号": "PO-2026-001",
    "供应商名称": "华诚供应链",
    "总金额": 125000.0,
    "交货日期": "2026-08-15",
    "合同条款": "逾期交货违约金：每延迟一日，支付合同总金额的0.05%；违约金总额不超过合同金额的10%"
}]

# 创建DataFrame并写入Excel
df = pd.DataFrame(data)
df.to_excel("mock_order.xlsx", index=False)

print("√已生成测试文件：mock_order.xlsx")