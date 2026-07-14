# ============================================================
# 文件：utils/excel_parser.py
# 作用：从 Excel 文件中读取采购订单数据，返回字典格式
# 依赖：pandas（读取 Excel），openpyxl（处理 .xlsx 格式）
# ============================================================

import pandas as pd # pandas是数据分析库，用于读取excel/csv
from pathlib import Path    # Path用于处理文件路径，比字符串拼接更安全


def parse_excel_order(file_path: str) -> dict:
    """
    从Excel文件读取采购订单数据，返回一个字典。
    """

    # 第1步：用pandas读取Excel File
    # pd.read_excel()会把Excel读成一个DataFrame（类似表格）
    # 如果文件不存在，抛出Error
    df = pd.read_excel(file_path)

    # 清理列名：去除首尾空格
    df.columns = df.columns.str.strip()

    # 第2步：取第一行数据，比如只有一笔订单的情况

    if len(df) == 0:
        raise ValueError("Excel文件为空，没有数据行")
    
    # df.iloc[0]取第一行，返回一个Series（类似字典，列名作为key）
    row = df.iloc[0]

    # 第3步：定义列名映射（中英文 both ok）
    # 格式：{"实际列名": "标准字段名"}
    col_map = {
        "订单编号": "order_id",
        "供应商名称": "supplier_name",
        "总金额": "total_amount",
        "交货日期": "delivery_date",
        "合同条款": "contract_clause",
        "order_id": "order_id",
        "supplier_name": "supplier_name",
        "total_amount": "total_amount",
        "delivery_date": "delivery_date",
        "contract_clause": "contract_clause"
    }

    # 反向映射：从 Excel 列名中寻找对应的标准字段
    # 先找出所有在 Excel 中存在的列名（df.columns 是实际列名列表）
    # 然后从 col_map 中查找对应的标准字段名，取第一个匹配的值

    def get_standard_field(field_name):
        # 找出col_map中值为filed_name的所有键值
        possible_cols = [k for k, v in col_map.items() if v == field_name]
        for col in possible_cols:
            if col in df.columns:   # 确保该列存在
                val = row.get(col)  # 从第一行数据中取出该列的值
                if pd.notna(val) and str(val).strip() != "":    # 检查值是否不是NaN(pandas空值标记)
                    return str(val).strip()
        return None
    


    # 第4步：从row中提取数据
    # get_standard_field()方法，如果列名存在则返回值，否则返回默认值
    
    order_id = get_standard_field("order_id") or "PO-UNKNOWN"
    supplier_name = get_standard_field("supplier_name") or "未知供应商"
    total_amount = get_standard_field("total_amount") or 0.0
    delivery_date = get_standard_field("delivery_date") or "未指定"
    contract_clause = get_standard_field("contract_clause") or "无条款"

    try:
        total_amount = float(total_amount)
    except (ValueError, TypeError):
        total_amount = 0.0

    # 第5步：返回字典
    return{
        "order_id": order_id,
        "supplier_name": supplier_name,
        "total_amount": total_amount,
        "delivery_date": delivery_date,
        "contract_clause": contract_clause
    }