# ============================================================
# 文件：utils/order_loader.py
# 作用：根据文件扩展名自动选择合适的解析器
# 这是“门面模式（Facade Pattern）”的应用——对外提供统一接口
# ============================================================

from pathlib import Path
from .excel_parser import parse_excel_order # .表格从当前包untils导入
from .pdf_parser import parse_pdf_contract


def load_order(file_path: str) -> dict:
    """
    根据文件扩展名选择解析器，返回订单数据字典，本版本支持.xlsx, .xls, .pdf
    """

    # 第1步：解析文件扩展名
    path = Path(file_path)  # 转换为Path对象
    suffix = path.suffix.lower()    # 获取扩展名并转为小写如.xlsx, .pdf

    # 第2步：根据扩展名路由到对应解析器
    if suffix in [".xlsx", ".xls"]:
        # EXCEL文件，调用EXCEL解析器
        return parse_excel_order(file_path)
    
    elif suffix == ".pdf":
        # PDF文件，调用PDF解析器
        return parse_pdf_contract(file_path)
    
    else:
        # 不支持的格式，抛出异常
        raise ValueError(f"不支持的文件格式：{suffix}, 请使用 .xlsx、 .xls 或 .pdf")
    