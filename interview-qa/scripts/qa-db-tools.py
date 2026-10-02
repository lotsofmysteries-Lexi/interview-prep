#!/usr/bin/env python3
"""qa-db-tools.py — QA 题库运营工具

用法:
  python3 qa-db-tools.py index                      # 重建 index.md（只索引 active 题）
  python3 qa-db-tools.py tags                       # tags 词表统计 + 近似 tag 提示
  python3 qa-db-tools.py dedup --query "题干文本"    # 输入题干，输出近似题清单（查重提示）
  python3 qa-db-tools.py stats                      # 各文件题数 / 状态统计

设计约定:
  - 题目标记行格式: "### Q-XX-NNN：{题干}"
  - tags 行: "- tags: [a, b, c]"
  - 状态行(可选): "- status: active|review|deprecated"，缺省 active
  - index.md 只索引 active 题；CHANGELOG.md 由人工维护，本脚本不改
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

QA_DB = Path(__file__).resolve().parent.parent / "references" / "qa-db"
CATEGORY_FILES = {
    "01-project-experience.md": ("PE", "项目与产品经验"),
    "02-methodology.md": ("MD", "产品方法论"),
    "03-ai-technical.md": ("AT", "AI 技术实操"),
    "04-nontechnical.md": ("NT", "非技术"),
    "05-presale-delivery.md": ("PS", "售前交付/行业方案"),
}

Q_RE = re.compile(r"^###\s+(Q-[A-Z]{2}-\d{3})[：:]\s*(.+)$")
TAGS_RE = re.compile(r"^-\s*tags:\s*\[(.+?)\]")
STATUS_RE = re.compile(r"^-\s*status:\s*(active|review|deprecated)")


def parse_questions():
    """返回 [{id, title, tags, status, file, category}] 列表。"""
    questions = []
    if not QA_DB.exists():
        sys.exit(f"题库目录不存在: {QA_DB}")
    for fname, (code, cname) in CATEGORY_FILES.items():
        fpath = QA_DB / fname
        if not fpath.exists():
            continue
        current = None
        for line in fpath.read_text(encoding="utf-8").splitlines():
            m = Q_RE.match(line.strip())
            if m:
                current = {"id": m.group(1), "title": m.group(2).strip(),
                           "tags": [], "status": "active", "file": fname, "category": cname}
                questions.append(current)
                continue
            if current is None:
                continue
            m = TAGS_RE.match(line.strip())
            if m:
                current["tags"] = [t.strip().lower() for t in m.group(1).split(",") if t.strip()]
                continue
            m = STATUS_RE.match(line.strip())
            if m:
                current["status"] = m.group(1)
    return questions


def cmd_index():
    questions = parse_questions()
    active = [q for q in questions if q["status"] == "active"]
    lines = ["# qa-db 总索引", "",
             f"> 由 qa-db-tools.py 自动生成，请勿手工编辑。共 {len(active)} 道 active 题"
             f"（另有 {len(questions) - len(active)} 道非 active 未列出）。", ""]
    for fname, (code, cname) in CATEGORY_FILES.items():
        qs = [q for q in active if q["file"] == fname]
        if not qs:
            continue
        lines.append(f"## {cname}（{len(qs)} 题）")
        lines.append("")
        lines.append("| 题号 | 题干 | tags |")
        lines.append("|------|------|------|")
        for q in qs:
            lines.append(f"| {q['id']} | {q['title'][:60]} | {', '.join(q['tags'])} |")
        lines.append("")
    out = QA_DB / "index.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index.md 已重建: {len(active)} 道 active 题 -> {out}")


def cmd_tags():
    questions = parse_questions()
    counter = Counter(t for q in questions for t in q["tags"])
    print(f"共 {len(counter)} 个不同 tag：\n")
    for tag, n in counter.most_common():
        print(f"  {tag}: {n}")
    # 近似 tag 提示：互为子串或仅大小写/分隔差异
    names = sorted(counter)
    warns = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a != b and (a in b or b in a):
                warns.append((a, b))
    if warns:
        print("\n⚠️ 疑似同义/包含关系的 tag（建议归一）:")
        for a, b in warns:
            print(f"  {a}  <->  {b}")
    else:
        print("\n未发现疑似同义 tag。")


def _similarity(a, b):
    """字符 bigram Dice 相似度，足够做中文题干查重。"""
    def grams(s):
        s = re.sub(r"[^\w\u4e00-\u9fff]", "", s.lower())
        return {s[i:i + 2] for i in range(len(s) - 1)} or {s}
    ga, gb = grams(a), grams(b)
    return 2 * len(ga & gb) / (len(ga) + len(gb)) if ga and gb else 0.0


def cmd_dedup(query, threshold=0.45):
    questions = parse_questions()
    scored = sorted(((_similarity(query, q["title"] + " " + " ".join(q.get("variants", []))), q)
                     for q in questions), key=lambda x: -x[0])[:8]
    hits = [(s, q) for s, q in scored if s >= threshold]
    if not hits:
        print(f"未发现与「{query}」相似度 ≥ {threshold} 的已有题，可作为新题入库。")
        return
    print(f"与「{query}」相似的已有题（建议合并为变体，不另开新题）:")
    for s, q in hits:
        print(f"  [{s:.2f}] {q['id']} {q['title'][:50]}  ({q['file']})")


def cmd_stats():
    questions = parse_questions()
    by_file = Counter(q["file"] for q in questions)
    by_status = Counter(q["status"] for q in questions)
    print("各文件题数:")
    for fname, (code, cname) in CATEGORY_FILES.items():
        print(f"  {fname}: {by_file.get(fname, 0)}（{cname}）")
    print(f"合计: {sum(by_file.values())}")
    print(f"状态分布: {dict(by_status)}")


def main():
    p = argparse.ArgumentParser(description="QA 题库运营工具")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index", help="重建 index.md")
    sub.add_parser("tags", help="tags 词表统计与近似提示")
    d = sub.add_parser("dedup", help="题干查重")
    d.add_argument("--query", required=True)
    sub.add_parser("stats", help="统计")
    args = p.parse_args()
    if args.cmd == "index":
        cmd_index()
    elif args.cmd == "tags":
        cmd_tags()
    elif args.cmd == "dedup":
        cmd_dedup(args.query)
    elif args.cmd == "stats":
        cmd_stats()


if __name__ == "__main__":
    main()
