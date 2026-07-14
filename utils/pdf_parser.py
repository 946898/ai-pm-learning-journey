# ============================================================
# 文件：utils/pdf_parser.py
# 作用：从 PDF 文件中提取合同条款文本
# 依赖：pdfplumber（专门用于提取 PDF 文本和表格）
# ============================================================

import pdfplumber   # PDF解析库，支持表格提取
from pathlib import Path    # 处理文件路径

def parse_pdf_contract(file_path: str) -> dict:
    """
    从PDF文件提取合同条款文本，返回一个字典
    """
    
    # 第1步：用pdfplumber打开PDF并提取全文
    text = "" # 用于累计所有页面的文本
    
    with pdfplumber.open(file_path) as pdf:
        # pdf.pages是一个列表，每个元素代表一页
        for page in pdf.pages:
            # page.extract_text()提取当前页的文本，如无法提取则返回None
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n" # 每页加换行符分隔

    # 第2步：处理空文本的情况
    if not text.strip():
        # 如果提取不到文本，可能是扫描件（图片格式）
        # 先返回占位符，后面用OCR或多模态LLM处理
        return{
            "order_id": Path(file_path).stem,    # 用文件名（不含扩展名）作为临时订单号
            "supplier_name": "待提取（PDF无文字）",
            "total_amount": 0.0,
            "delivery_date": "待提取（PDF无文字）",
            "contract_clause": "无法提取合同条款，PDF可能为扫描件",
        }
    
    # 第3步：截取前2000个字符作为合同条款
    # 直接返回全部文本会占用大量Token，截取前2000字符
    # 生产环境可结合RAG分段检索，或者让LLM自己决定需要哪部分
    contract_clause = text[:2000]

    # 第4步：返回字典
    # pdf通常没有结构化的订单号、供应商名称，用文件名做临时ID
    return{
         "order_id": Path(file_path).stem,       # 文件名（不含扩展名）
        "supplier_name": "待提取（PDF）",         # 占位符
        "total_amount": 0.0,
        "delivery_date": "待提取（PDF）",
        "contract_clause": contract_clause,      # 提取到的合同条款文本
        # 可以在 risk_analysis 节点中用 LLM 从文本中提取供应商名称和金额
    }
