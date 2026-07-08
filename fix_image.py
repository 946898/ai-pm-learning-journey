import os
import re
import shutil
from pathlib import Path

# 配置区
PROJECT_ROOT = Path(__file__).parent  # 脚本所在目录即为项目根目录
SOURCE_IMG_DIR = Path(r"C:\Users\zhouxu48\AppData\Roaming\Typora\typora-user-images")
TARGET_IMG_DIR = PROJECT_ROOT / "images"

# 确保目标目录存在
TARGET_IMG_DIR.mkdir(exist_ok=True)

# 第一步：复制所有图片
print("📦 正在复制图片...")
copied_count = 0
for img_file in SOURCE_IMG_DIR.glob("*"):  # 所有文件（不递归）
    if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
        shutil.copy2(img_file, TARGET_IMG_DIR / img_file.name)
        copied_count += 1
print(f"✅ 已复制 {copied_count} 张图片到 {TARGET_IMG_DIR}")

# 第二步：扫描所有 .md 文件，替换图片引用
print("🔍 正在扫描 Markdown 文件并替换引用...")
md_files = list(PROJECT_ROOT.rglob("*.md"))  # 递归查找所有 .md 文件

# 旧路径的正则：匹配以 C:\Users\...\typora-user-images\ 开头的绝对路径
pattern = re.compile(r'\!\[.*?\]\(C:\\Users\\[^\\]+\\AppData\\Roaming\\Typora\\typora-user-images\\([^)]+)\)')

modified_count = 0
for md_file in md_files:
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换为相对路径
    new_content, num = pattern.subn(r'![图片](./images/\1)', content)
    
    if num > 0:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_count += 1
        print(f"  ✅ 已处理: {md_file.relative_to(PROJECT_ROOT)} (替换 {num} 处)")

print(f"\n🎉 完成！共修改 {modified_count} 个 Markdown 文件。")
print("💡 请检查替换结果，然后执行 git add . 并提交。")