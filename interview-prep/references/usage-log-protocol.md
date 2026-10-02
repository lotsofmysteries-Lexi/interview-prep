# 全量交互 log 协议

> 触发：interview-* 任一 skill 会话结束（Phase 4 入库完成，或用户中止）时**自动执行**，不需用户提醒。
> 目标：每次使用都产出全量交互 log（用户反馈分析 / 耗时 / token 消耗统计），供 skill 运营方持续改进。

## 双阶段设计（协议本身必须轻）

1. **过程中**：只做轻量记录点——在 workspace 下 `skill-logs/records/` 追加 JSONL 行，每行一次关键事件，不写长文
2. **收尾时**：把 JSONL 记录点汇编成 Markdown log（优先调用 `scripts/usage-log-tools.py`；脚本不可用时按本协议字段手工成文）

## 记录点格式（JSONL，一行一事件）

```json
{"t":"2026-10-02T19:30:00","phase":"phase3-proj001","event":"file_write","target":"full-card.md","tokens_est":12000}
{"t":"...","phase":"phase3-proj001","event":"user_feedback","quote":"这里需要扩充两个 agent 怎么编排","rework":"深度不足"}
{"t":"...","phase":"deploy","event":"error","detail":"Edit old_string not found","resolution":"reread+retry"}
```

- `phase`：phase0-profiling / phase1-scene / phase2-skeleton / phase3-full / phase4-entry / qa / resume / jd / mock / review / deploy
- `event`：file_read / file_write / user_feedback / error / tool_fail / stage_done
- `tokens_est`：粗估即可（字符量 ÷ 1.5，中文），标注高消耗环节用

## 最终 log 字段规范

文件：workspace 下 `skill-logs/usage-{skill名}-{日期}-{人设名}.md`

| 字段 | 内容 | 来源 |
|------|------|------|
| 时间线 | 各阶段起止、关键工具调用、文件读写清单 | event: stage_done/file_* |
| 用户反馈全录 | 每轮返工的选区/原话**逐字记录** + 对应修改 | event: user_feedback |
| 返工分析 | 返工次数、原因分类（深度不足/格式偏差/流程顺序/数字错误） | 汇总 user_feedback |
| 效率统计 | 总耗时、确认轮次、产物文件数与字数 | 时间线汇总 |
| Token 估算 | 各阶段上下文吞吐估算，标出 top3 高消耗环节 | 汇总 tokens_est |
| 异常清单 | 报错、工具失败、降级路径及解决方式 | event: error/tool_fail |
| 改进信号 | 本次暴露的 skill 缺陷，供优化迭代直接取用 | 综合以上 |

## 约束

- log 协议**不得反向增加会话 token 开销**：过程中只写记录点，禁止边走边写分析长文
- 记录点文件（JSONL）在成文后保留，供脚本汇总跨会话统计
- 用户明确说"不用记 log"时可跳过最终成文，但记录点照常写（成本极低）
