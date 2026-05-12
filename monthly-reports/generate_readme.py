"""
generate_readme.py
扫描当前文件夹下的 HTML 文件，按文件名规则生成中文说明，并写入 README.md。

【命名规则说明】
文件名格式一般为：YYYYMM_<类型标识>.html
- 含 "mkt"      → 市场报告
- 含 "out-game" → CP社区报告
- 其他          → 竞品报告

月份映射：202601 → 2026年1月，以此类推。

如需新增规则，在下方 RULES 列表里添加即可（优先级从上到下，第一个匹配的生效）。
"""

import os
import re

# ── 文件夹路径（相对于仓库根目录执行）────────────────────────────────────────
FOLDER = "monthly-reports"

# ── 规则列表：(文件名关键词, 报告类型描述)  优先级从上到下 ──────────────────
RULES = [
    ("mkt",      "市场报告"),
    ("out-game", "CP社区报告"),
]
DEFAULT_TYPE = "竞品报告"  # 不匹配任何关键词时的默认类型


def month_label(yyyymm: str) -> str:
    """将 '202604' 转换为 '2026年4月'"""
    year = yyyymm[:4]
    month = str(int(yyyymm[4:6]))  # 去掉前导零
    return f"{year}年{month}月"


def describe(filename: str) -> str:
    """根据文件名生成中文说明"""
    # 提取开头的 YYYYMM
    m = re.match(r"(\d{6})", filename)
    prefix = month_label(m.group(1)) if m else ""

    # 匹配类型关键词
    report_type = DEFAULT_TYPE
    for keyword, label in RULES:
        if keyword in filename:
            report_type = label
            break

    return f"{prefix}{report_type}"


def generate_readme():
    # 收集所有 HTML 文件（排除脚本自身所在文件夹里的非 HTML 文件）
    html_files = sorted(
        f for f in os.listdir(FOLDER)
        if f.endswith(".html")
    )

    # 构建 Markdown 表格
    lines = [
        "# 📁 monthly-reports\n",
        "本文件夹存放各月度报告，文件列表如下：\n",
        "| 文件名 | 说明 | 链接 |",
        "| ------ | ---- | ---- |",
    ]

    for f in html_files:
        desc = describe(f)
        lines.append(f"| {f} | {desc} | [{f}]({f}) |")

    lines.append("")  # 末尾空行

    readme_path = os.path.join(FOLDER, "README.md")
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"✅ README.md 已更新，共收录 {len(html_files)} 个文件。")
    for f in html_files:
        print(f"   {f}  →  {describe(f)}")


if __name__ == "__main__":
    generate_readme()
