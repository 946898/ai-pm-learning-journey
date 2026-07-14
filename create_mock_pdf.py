# ============================================================
# 文件：create_mock_pdf.py
# 作用：生成一个测试用的采购合同 PDF 文件（mock_contract.pdf）
# 依赖：reportlab（需要先安装：pip install reportlab）
# 运行：python create_mock_pdf.py
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_mock_contract_pdf(output_path="mock_contract.pdf"):
    """
    生成一份包含采购合同条款的 PDF 文件
    """
    # 创建画布
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # 设置字体（reportlab 默认支持 Helvetica，中文字体需要额外注册，这里用默认字体）
    # 如果系统有中文字体，可以注册，这里我们用 Helvetica 并确保内容为 ASCII/英文
    # 对于中文内容，reportlab 可能不支持显示，建议用英文或拼音

    # ---- 标题 ----
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Procurement Contract")

    # ---- 基本信息 ----
    c.setFont("Helvetica", 12)
    y = height - 80
    lines = [
        "Contract ID: PO-2026-001",
        "",
        "Party A (Buyer): XX Technology Co., Ltd.",
        "Party B (Supplier): Xin Da Logistics Co., Ltd.",
        "",
        "Clause 1: Delivery Terms",
        "The Supplier shall deliver the goods to Party A's designated",
        "warehouse on or before August 15, 2026.",
        "",
        "Clause 2: Late Delivery Penalty",
        "If the Supplier fails to deliver on time, for each day of delay,",
        "the Supplier shall pay Party A a penalty of 0.05% of the total",
        "contract amount. The total penalty shall not exceed 10% of the",
        "contract amount.",
        "",
        "Clause 3: Quality Assurance",
        "The Supplier guarantees that all delivered goods meet the",
        "applicable national quality standards.",
        "",
        "Clause 4: Liability for Breach",
        "If the Supplier breaches any term of this contract, Party A",
        "shall have the right to terminate the contract immediately.",
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 18

    # ---- 保存 PDF ----
    c.save()
    print(f" 已生成 PDF 文件: {output_path}")
    print(f" 文件路径: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    # 安装依赖：pip install reportlab
    create_mock_contract_pdf()