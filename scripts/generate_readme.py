"""
generate_readme.py
统一为三个文件夹生成 README.md：根目录、monthly-reports、weekly-reports。

【如何扩展规则】
- 在各文件夹的 FOLDER_CONFIG 里修改 rules / default_type
- 新增文件夹：在 FOLDER_CONFIG 末尾追加一项即可
"""

import os
import re

# ══════════════════════════════════════════════════════════════════
#  各文件夹配置
#  rules: [(文件名关键词, 说明)]  —— 从上到下第一个匹配的生效
#  default_type: 没有关键词匹配时使用的说明
# ══════════════════════════════════════════════════════════════════
FOLDER_CONFIG = {

    # ── 根目录 ────────────────────────────────────────────────────
    ".": {
        "title": "my-reports",
        "intro": "仓库根目录重要文件一览",
        "rules": [
            ("dashboard_kr_light", "韩服竞品大盘（精简版）"),
            ("dashboard_kr",       "韩服竞品大盘"),
            ("dashboard_light",    "竞品大盘（精简版）"),
            ("dashboard",          "竞品大盘"),
            ("dunhuang",           "敦煌旅游攻略"),   # 示例：非报告类文件
        ],
        "default_type": "报告文件",
        "readme_path": "README.md",
    },

    # ── monthly-reports ───────────────────────────────────────────
    "monthly-reports": {
        "title": "📁 monthly-reports",
        "intro": "本文件夹存放各月度报告，文件列表如下：",
        "rules": [
            ("mkt",      "市场报告"),
            ("out-game", "CP社区报告"),
        ],
        "default_type": "竞品报告",
        "readme_path": "monthly-reports/README.md",
    },

    # ── weekly-reports ────────────────────────────────────────────
    "weekly-reports": {
        "title": "📁 weekly-reports",
        "intro": "本文件夹存放各周度报告，文件列表如下：",
        "rules": [
            ("mkt",      "市场周报"),
            ("out-game", "CP社区周报"),
        ],
        "default_type": "竞品周报",
        "readme_path": "weekly-reports/README.md",
    },
}


# ══════════════════════════════════════════════════════════════════
#  工具函数
# ══════════════════════════════════════════════════════════════════

def month_label(yyyymm: str) -> str:
    """'202604' → '2026年4月'"""
    year, month = yyyymm[:4], str(int(yyyymm[4:6]))
    return f"{year}年{month}月"


def week_label(yyyyww: str) -> str:
    """'202615' → '2026年第15周'  (格式 YYYYWW，共6位)"""
    year, week = yyyyww[:4], str(int(yyyyww[4:6]))
    return f"{year}年第{week}周"


def extract_prefix(filename: str, folder: str) -> str:
    """从文件名提取时间前缀，monthly 用月份，weekly 用周次，根目录不加前缀"""
    if folder == "monthly-reports":
        m = re.match(r"(\d{6})", filename)
        return month_label(m.group(1)) if m else ""
    if folder == "weekly-reports":
        m = re.match(r"(\d{6})", filename)
        return week_label(m.group(1)) if m else ""
    return ""  # 根目录不自动加前缀


def describe(filename: str, folder: str, cfg: dict) -> str:
    prefix = extract_prefix(filename, folder)
    report_type = cfg["default_type"]
    for keyword, label in cfg["rules"]:
        if keyword in filename:
            report_type = label
            break
    return f"{prefix}{report_type}" if prefix else report_type


def list_html_files(folder: str) -> list:
    path = folder if folder != "." else "."
    return sorted(f for f in os.listdir(path) if f.endswith(".html"))


def generate_readme(folder: str, cfg: dict):
    html_files = list_html_files(folder)

    # 文件夹前缀（用于生成相对链接）
    link_prefix = f"{folder}/" if folder != "." else ""

    lines = [
        f"# {cfg['title']}\n",
        f"{cfg['intro']}\n",
        "| 文件名 | 说明 | 链接 |",
        "| ------ | ---- | ---- |",
    ]

    for f in html_files:
        desc = describe(f, folder, cfg)
        link = f"{link_prefix}{f}"
        lines.append(f"| {f} | {desc} | [{f}]({link}) |")

    lines.append("")  # 末尾换行

    with open(cfg["readme_path"], "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"✅ {cfg['readme_path']} 已更新，共 {len(html_files)} 个文件")
    for f in html_files:
        print(f"   {f}  →  {describe(f, folder, cfg)}")


# ══════════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    for folder, cfg in FOLDER_CONFIG.items():
        # 若文件夹不存在则跳过（避免 weekly-reports 尚未创建时报错）
        target = folder if folder != "." else "."
        if not os.path.isdir(target):
            print(f"⚠️  文件夹 '{folder}' 不存在，跳过")
            continue
        generate_readme(folder, cfg)
