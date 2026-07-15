# ============================================================
# 文件：utils/pdf_parser.py
# 作用：从 PDF 文件中提取合同条款文本，并进行结构化清洗
# 依赖：pdfplumber（专门用于提取 PDF 文本和表格）
# ============================================================

import re
import pdfplumber   # PDF解析库，支持表格提取
from pathlib import Path    # 处理文件路径

def clean_text(text: str) -> dict:
    """
    清洗PDF提取的原始文本：
    - 合并多余换行（连续换行保留2个
    - 去除首尾空白
    - 合并连续空格
    """

    # 连续3个以上的换行替换为2个
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 连续多个空格替换为1个
    text = re.sub(r' {2,}', ' ', text)
    # 去除首尾空白
    text = text.strip()
    return text

def extract_delivery_date(text: str) -> str:
    """
    从合同文本中提取交付日期，支持多种格式：
    - 2025-06-18
    - 2025年6月18日
    - 2025/06/18
    - 2025/6/18
    """
    # 1. 先尝试匹配带关键词的日期
    patterns_with_keyword = [
        # 带关键词 + 连字符格式
        r'(?:交货|送货|预计送达)日期[：:]\s*(\d{4})-(\d{1,2})-(\d{1,2})',
        # 带关键词 + 中文格式
        r'(?:交货|送货|预计送达)日期[：:]\s*(\d{4})年(\d{1,2})月(\d{1,2})日',
        # 带关键词 + 斜杠格式
        r'(?:交货|送货|预计送达)日期[：:]\s*(\d{4})/(\d{1,2})/(\d{1,2})',
    ]
    
    for pattern in patterns_with_keyword:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                year, month, day = groups
                return f"{year}-{int(month):02d}-{int(day):02d}"
    
    # 2. 如果没找到带关键词的，尝试纯日期格式
    patterns_pure = [
        r'(\d{4})-(\d{1,2})-(\d{1,2})',      # 2025-06-18
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2025年6月18日
        r'(\d{4})/(\d{1,2})/(\d{1,2})',      # 2025/06/18
    ]
    
    for pattern in patterns_pure:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                year, month, day = groups
                return f"{year}-{int(month):02d}-{int(day):02d}"
    
    return "待提取（PDF）"


def extract_structured_fields(text: str) -> dict:
    """
     从合同文本中尝试提取结构化字段：
    - 合同编号 / 订单编号
    - 供应商名称（乙方）
    - 总金额
    """

    # 第1步：提取合同编号（支持多种格式）
    # 实在不行把格式扔给AI解析re表达式
    order_id = "PO-UNKNOWN" # 赋默认值
    patterns = [
        r'合同编号[：:]\s*([A-Za-z0-9\-_\u4e00-\u9fa5]+)',
        r'订单编号[：:]\s*([A-Za-z0-9\-_\u4e00-\u9fa5]+)',
        r'PO[#]?\s*([A-Za-z0-9\-_\u4e00-\u9fa5]+)',
        r'Contract\s*(?:ID|No\.?)[：:]\s*([A-Za-z0-9\-_\u4e00-\u9fa5]+)'
    ]
    for pattern in patterns:
        # re.search()在文本中查找匹配
        # re.IGNORECASE 忽略大小写
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # match.group(1)取出第一个括号里面的内容（编号值）
            order_id = match.group(1).strip()
            break # 找到第一个匹配就退出循环

    # 第2步：提取供应商名称
    supplier_name = "待提取（PDF）" # 赋默认值
    
    patterns = [
        r'乙方[（(]供应商[）)]?[：:]\s*([^\n]{2,30})',  # "乙方（供应商）：鑫达物流有限公司"
        r'供应商[：:]\s*([^\n]{2,30})',                # "供应商：鑫达物流有限公司"
        r'Party B[（(]Supplier[）)]?[：:]\s*([^\n]{2,30})',  # "Party B (Supplier): Xin Da Logistics"
    ]   # 按需结合RE规则补充

    for pattern in patterns:
        # re.search()在文本中查找匹配
        # re.IGNORCASE忽略大小写
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            supplier_name = match.group(1).strip()
            break

    # 第3步：提取总金额
    total_amount = 0.0 # 赋默认值

    patterns = [
        r'总金额[：:]\s*([\d,]+\.?\d*)\s*元',   # "总金额：125000.00元"
        r'合同金额[：:]\s*([\d,]+\.?\d*)\s*元', # "合同金额：125000.00元"
        r'金额[：:]\s*([\d,]+\.?\d*)\s*元',     # "金额：125000.00元"
        r'([\d,]+\.?\d*)\s*万元',               # "12.5万元"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            total_amount = float(match.group(1).replace(',',""))
            if '万元' in match.group(0):
                total_amount *= 10000
            break

    # 提取日期
    delivery_date = extract_delivery_date(text)

    # 返回提取到的三个字段
    return{
        "order_id": order_id,
        "supplier_name": supplier_name,
        "total_amount": total_amount,
        "delivery_date": delivery_date,
    }



def parse_pdf_contract(file_path: str) -> dict:
    """
    从PDF文件提取合同条款文本，返回一个结构化字典
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
    
    # 第3步：清洗文本
    cleanned_text = clean_text(text)

    # 第4步：提取结构化字段
    structured = extract_structured_fields(cleanned_text)
    


    # 第5步：截取前3000个字符作为合同条款
    # 直接返回全部文本会占用大量Token，截取前3000字符
    # 生产环境可结合RAG分段检索，或者让LLM自己决定需要哪部分
    contract_clause = text[:3000]

    # 第4步：返回字典
    # pdf通常没有结构化的订单号、供应商名称，用文件名做临时ID
    return{
         "order_id": structured["order_id"],       # 文件名（不含扩展名）
        "supplier_name": structured["supplier_name"],         # 占位符
        "total_amount": structured["total_amount"],
        "delivery_date": structured["delivery_date"],
        "contract_clause": contract_clause      # 提取到的合同条款文本
        # 可以在 risk_analysis 节点中用 LLM 从文本中提取供应商名称和金额
    }
