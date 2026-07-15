# ============================================================
# 文件：create_pdf_chinese.py
# 作用：生成一份包含中文内容的采购合同 PDF
# 运行：python create_pdf_chinese.py
# ============================================================

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ---------- 自动查找系统中文字体 ----------
def find_chinese_font():
    """
    在系统中查找常见的中文字体文件
    """
    # Windows 常见字体路径
    win_fonts = [
        "C:/Windows/Fonts/simsun.ttc",        # 宋体
        "C:/Windows/Fonts/simhei.ttf",        # 黑体
        "C:/Windows/Fonts/msyh.ttc",          # 微软雅黑
        "C:/Windows/Fonts/msyhbd.ttc",        # 微软雅黑粗体
        "C:/Windows/Fonts/simkai.ttf",        # 楷体
        "C:/Windows/Fonts/SIMLI.TTF",         # 隶书
    ]
    
    # macOS 常见字体路径
    mac_fonts = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STSong.ttf",
    ]
    
    # Linux 常见字体路径（需手动安装中文字体）
    linux_fonts = [
        "/usr/share/fonts/truetype/arphic/uming.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]

    # 根据操作系统选择候选列表
    if sys.platform.startswith("win"):
        candidates = win_fonts
    elif sys.platform.startswith("darwin"):
        candidates = mac_fonts
    else:
        candidates = linux_fonts

    # 检查是否存在
    for f in candidates:
        if os.path.exists(f):
            return f
    
    # 如果找不到，用 fc-list 查找（Linux）
    if sys.platform.startswith("linux"):
        try:
            import subprocess
            result = subprocess.run(
                ["fc-list", ":lang=zh", "file"],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split("\n")
            if lines:
                font_path = lines[0].split(":")[0]
                if os.path.exists(font_path):
                    return font_path
        except:
            pass

    return None


# ---------- 生成 PDF ----------
def create_chinese_pdf(output_path="mock_contract.pdf"):
    """
    生成一份包含中文内容的采购合同 PDF
    """
    # ---- 1. 查找字体 ----
    font_path = find_chinese_font()
    if font_path is None:
        print("× 未找到系统中文字体，请手动指定字体路径。")
        print("   Windows: C:/Windows/Fonts/simsun.ttc")
        print("   macOS: /System/Library/Fonts/PingFang.ttc")
        print("   Linux: /usr/share/fonts/truetype/wqy/wqy-microhei.ttc")
        print("   找到后，修改脚本中的 font_path 变量")
        sys.exit(1)

    # ---- 2. 注册字体 ----
    try:
        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
        print(f"√ 使用字体: {font_path}")
    except Exception as e:
        print(f"× 注册字体失败: {e}")
        sys.exit(1)

    # ---- 3. 创建 PDF ----
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # 标题
    c.setFont('ChineseFont', 18)
    c.drawString(50, height - 50, "采购合同")

    # 正文内容
    c.setFont('ChineseFont', 12)
    y = height - 80
    lines = [
        "合同编号：PO-2026-001",
        "",
        "订单编号：POS32407150001",
        "",
        "甲方（采购方）：XX 科技有限公司",
        "乙方（供应商）：鑫达物流",
        "",
        "第一条 交货条款",
        "乙方应于 2026 年 8 月 15 日前将货物运抵甲方指定仓库。",
        "",
        "第二条 逾期交货违约金",
        "如乙方未能按时交货，每延迟一日，应向甲方支付合同总金额的 0.05% 作为违约金。",
        "违约金总额不超过合同总金额的 10%。",
        "",
        "第三条 质量保证",
        "乙方保证所供货物符合国家相关质量标准。",
        "",
        "第四条 违约责任",
        "如乙方违反本合同任何条款，甲方有权立即终止合同。",
        "",
        "甲方（盖章）：________",
        "乙方（盖章）：________",
        "签署日期：2026 年 7 月 15 日",
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()
    print(f"√ PDF 已生成: {output_path}")


if __name__ == "__main__":
    # 检查 reportlab 是否安装
    try:
        import reportlab
    except ImportError:
        print("× 请先安装 reportlab: pip install reportlab")
        sys.exit(1)

    create_chinese_pdf()