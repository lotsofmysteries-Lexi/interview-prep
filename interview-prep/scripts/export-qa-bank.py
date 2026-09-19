import re
import pathlib

import yaml

STAGE_META = {
    "stage_1": ("阶段1：立项与业务价值", "⭐⭐⭐（极高追问）"),
    "stage_2": ("阶段2：需求分析", "⭐⭐（高追问）"),
    "stage_3": ("阶段3：数据准备", "⭐（中追问）"),
    "stage_4": ("阶段4：方案设计", "⭐⭐⭐（极高追问）"),
    "stage_5": ("阶段5：测试验证", "⭐⭐（高追问）"),
    "stage_6": ("阶段6：部署与运营", "⭐（中追问）"),
}
ORDER = ["stage_1", "stage_2", "stage_3", "stage_4", "stage_5", "stage_6"]


def stage_key(value):
    m = re.match(r"(stage_\d)", str(value or ""))
    return m.group(1) if m else None


def build(proj_id):
    path = pathlib.Path(proj_id) / "full-card.md"
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    proj_name = title.split("：", 1)[1] if "：" in title else title

    blocks = re.findall(r"```yaml\n(.*?)\n```", text, re.S)
    indices = yaml.safe_load(blocks[-1])["extracted_indices"]
    qa = indices["qa_bank"]

    fab = sum(1 for q in qa if q.get("source") == "fabricated")

    out = []
    out.append("# 面试追问 QA 库")
    out.append("")
    out.append(f"> 项目：**{proj_name}**（`{proj_id}`）  ")
    out.append(f"> 来源：`projects/{proj_id}/full-card.md` → `extracted_indices.qa_bank`  ")
    out.append(f"> 条目数：{len(qa)} 组 ｜ 覆盖 6 个阶段")
    out.append("> ")
    out.append(f"> ⚠️ **{fab}/{len(qa)} 条标注 `source: fabricated`** —— 表示该问答的核心事实依据，落在")
    out.append("> `skeleton.md`「信源分界」的 🟡 / 🔴 档位（数字为推演，或原件零字）。")
    out.append("> **这些不是「必须背下来」的事实**：面试时按「这是我当时的判断 / 口径」来讲，")
    out.append("> 不要在细节上给出无法支撑的确定感。")
    out.append("")
    out.append("---")
    out.append("")

    for key in ORDER:
        items = [q for q in qa if stage_key(q.get("source_stage")) == key]
        if not items:
            continue
        name, stars = STAGE_META[key]
        out.append(f"## {name} {stars}")
        out.append("")
        for q in items:
            flag = "　`⚠️ fabricated`" if q.get("source") == "fabricated" else ""
            out.append(f"**[{q['type']}]** {q['question']}{flag}")
            out.append(f"> {q['answer']}")
            out.append("")
        out.append("---")
        out.append("")

    out.append("## 附：按追问类型速览（只列问题，便于按类复习）")
    out.append("")
    for t in ["方案类", "决策类", "落地类", "反思类"]:
        items = [q for q in qa if q["type"] == t]
        if not items:
            continue
        out.append(f"### {t}（{len(items)} 组）")
        out.append("")
        for q in items:
            key = stage_key(q.get("source_stage"))
            short = STAGE_META[key][0][:4] if key in STAGE_META else "?"
            out.append(f"- [{short}] {q['question']}")
        out.append("")

    target = pathlib.Path(proj_id) / "qa-bank.md"
    body = "\n".join(out).rstrip() + "\n"

    # 保留手工维护的段落（脚本无法生成的部分，如「高频通用追问」）——
    # 否则每次重跑都会把人工补写的内容冲掉。
    manual_marker = "## 高频通用追问"
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if old.startswith(manual_marker):
            i = 0
        else:
            i = old.find("\n" + manual_marker)
        if i >= 0:
            body = body + "\n" + old[i:].lstrip("\n")

    target.write_text(body, encoding="utf-8")
    return target, len(qa), fab


def discover(targets):
    """未指定项目时，自动扫描当前目录下带 full-card.md 的 proj-* 目录。"""
    if targets:
        return list(targets)
    return sorted(p.name for p in pathlib.Path(".").glob("proj-*") if (p / "full-card.md").exists())


if __name__ == "__main__":
    import sys

    ids = discover(sys.argv[1:])
    if not ids:
        raise SystemExit("未找到任何 proj-*/full-card.md —— 请在 interview-vault/projects/ 下执行")
    for pid in ids:
        target, n, f = build(pid)
        print(f"{pid}: {target} | {n} QA | fabricated {f}")
