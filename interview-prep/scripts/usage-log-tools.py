#!/usr/bin/env python3
"""usage-log-tools.py — 交互 log 汇编工具

用法:
  python3 usage-log-tools.py build <records.jsonl> --skill interview-prep --persona likex [--out <dir>]

从轻量记录点（JSONL）汇编成最终 Markdown 交互 log，字段对齐 usage-log-protocol.md：
时间线 / 用户反馈全录 / 返工分析 / 效率统计 / Token 估算 / 异常清单 / 改进信号。

JSONL 记录点格式（一行一事件）:
  {"t":"ISO时间","phase":"phase3-full","event":"user_feedback","quote":"原话","rework":"深度不足"}
  event ∈ file_read | file_write | user_feedback | error | tool_fail | stage_done
  tokens_est 可选，附在任意事件上
"""
import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REWORK_CATS = {"深度不足", "格式偏差", "流程顺序", "数字错误", "其他"}


def _fmt_time(t):
    try:
        return datetime.fromisoformat(t).strftime("%H:%M:%S")
    except (ValueError, TypeError):
        return str(t)


def _duration(records):
    times = [r["t"] for r in records if r.get("t")]
    if len(times) < 2:
        return "—"
    try:
        ts = sorted(datetime.fromisoformat(t) for t in times)
        secs = int((ts[-1] - ts[0]).total_seconds())
        return f"{secs // 60} 分 {secs % 60} 秒"
    except ValueError:
        return "—"


def build(records_path, skill, persona, out_dir):
    records = []
    for line in Path(records_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not records:
        sys.exit("记录点为空或格式错误，未生成 log。")

    records.sort(key=lambda r: r.get("t", ""))
    date = records[0].get("t", "")[:10]
    phases = sorted({r.get("phase", "?") for r in records})

    # 时间线：每阶段的起止与文件读写
    by_phase = defaultdict(list)
    for r in records:
        by_phase[r.get("phase", "?")].append(r)
    timeline = ["| 阶段 | 起止 | 文件读 | 文件写 |", "|------|------|--------|--------|"]
    for ph in phases:
        rs = by_phase[ph]
        reads = {r.get("target", "?") for r in rs if r.get("event") == "file_read"}
        writes = {r.get("target", "?") for r in rs if r.get("event") == "file_write"}
        span = f"{_fmt_time(rs[0]['t'])} – {_fmt_time(rs[-1]['t'])}" if rs and rs[0].get("t") else "—"
        timeline.append(f"| {ph} | {span} | {len(reads)} | {len(writes)} |")

    # 用户反馈全录（逐字）+ 返工分析
    feedbacks = [r for r in records if r.get("event") == "user_feedback"]
    feedback_sec = ["| 时间 | 阶段 | 原话（逐字） | 归类 |", "|------|------|--------------|------|"]
    rework_counter = Counter()
    for r in feedbacks:
        cat = r.get("rework") if r.get("rework") in REWORK_CATS else "其他"
        rework_counter[cat] += 1
        quote = (r.get("quote", "") or "").replace("|", "\\|").replace("\n", " ")
        feedback_sec.append(f"| {_fmt_time(r.get('t',''))} | {r.get('phase','?')} | {quote} | {cat} |")
    if not feedbacks:
        feedback_sec.append("| — | — | 本会话无返工反馈 | — |")

    # 效率统计 + token 估算
    tokens_by_phase = defaultdict(int)
    for r in records:
        tokens_by_phase[r.get("phase", "?")] += r.get("tokens_est", 0)
    total_tokens = sum(tokens_by_phase.values())
    top3 = sorted(tokens_by_phase.items(), key=lambda x: -x[1])[:3]
    eff = [f"- 总耗时: {_duration(records)}",
           f"- 阶段数: {len(phases)}；确认轮次（用户反馈数）: {len(feedbacks)}",
           f"- 产物写入次数: {sum(1 for r in records if r.get('event') == 'file_write')}",
           f"- Token 粗估总量: {total_tokens}（中文按字符÷1.5）",
           f"- Top3 高消耗阶段: {', '.join(f'{p}({n})' for p, n in top3) if top3 else '—'}"]

    # 异常清单
    errors = [r for r in records if r.get("event") in ("error", "tool_fail")]
    err_sec = ["| 时间 | 类型 | 详情 | 解决 |", "|------|------|------|------|"]
    for r in errors:
        err_sec.append(f"| {_fmt_time(r.get('t',''))} | {r.get('event')} | "
                       f"{(r.get('detail','') or '').replace('|','\\|')} | "
                       f"{(r.get('resolution','') or '—').replace('|','\\|')} |")
    if not errors:
        err_sec.append("| — | — | 无异常 | — |")

    # 改进信号：启发式——出现"弱/缺"自检缺口、同类错误重复、返工 ≥2 的阶段
    signals = []
    for cat, n in rework_counter.items():
        if n >= 2:
            signals.append(f"「{cat}」类返工 {n} 次，建议检查对应阶段的生成规则")
    err_counter = Counter(r.get("detail", "") for r in errors)
    for detail, n in err_counter.items():
        if n >= 2:
            signals.append(f"同一异常重复 {n} 次：{detail[:50]}")
    if not signals:
        signals.append("本次未发现明显缺陷信号")

    md = f"""# 交互 Log — {skill} / {persona} / {date}

> 由 usage-log-tools.py 从记录点自动汇编（协议见 interview-prep/references/usage-log-protocol.md）

## 1. 时间线

{'\n'.join(timeline)}

## 2. 用户反馈全录

{'\n'.join(feedback_sec)}

## 3. 返工分析

- 返工总数: {len(feedbacks)}
- 分类分布: {dict(rework_counter) if rework_counter else '无'}

## 4. 效率统计

{chr(10).join(eff)}

## 5. Token 估算

- 各阶段: {dict(tokens_by_phase)}

## 6. 异常清单

{chr(10).join(err_sec)}

## 7. 改进信号

{chr(10).join('- ' + s for s in signals)}
"""
    out_dir = Path(out_dir) if out_dir else Path.cwd() / "skill-logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"usage-{skill}-{date}-{persona}.md"
    out.write_text(md, encoding="utf-8")
    print(f"log 已生成: {out}")


def main():
    p = argparse.ArgumentParser(description="交互 log 汇编工具")
    b = p.add_subparsers(dest="cmd", required=True)
    g = b.add_parser("build", help="从 JSONL 记录点汇编 log")
    g.add_argument("records", help="JSONL 记录点文件路径")
    g.add_argument("--skill", required=True)
    g.add_argument("--persona", required=True)
    g.add_argument("--out", default=None, help="输出目录（默认 ./skill-logs）")
    args = p.parse_args()
    build(args.records, args.skill, args.persona, args.out)


if __name__ == "__main__":
    import sys
    main()
