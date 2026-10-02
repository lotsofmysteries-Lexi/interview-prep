---
name: interview-qa
description: 面试口述与问答演练：基于 qa-db 题库 × vault 项目档案做交互式 QA 演练、面试口述版（3-5分钟/项目）、自我介绍（30秒/1分钟/3分钟三版本）。当用户要"QA演练""口述版""项目讲述""自我介绍"等面试表达材料时使用。
---

# interview-qa — 交互式 QA 演练 + 口述版 + 自我介绍

基于两层数据派生面试准备材料：**题库层**（`references/qa-db/`，通用题目）× **事实层**（vault 项目的 full-card）。QA 演练是交互环节，不落独立题库文件。

## 前置条件

- `interview-vault/profile/master.md` 存在（含项目骨架一览）
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`

## 命令路由

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| "QA演练" / "考我QA" / "追问准备" | 交互式 QA 演练 | `references/qa-bank-rules.md` |
| "口述版" / "怎么讲" | 口述版生成 | `references/oral-version-rules.md` |
| "自我介绍" | 自我介绍生成 | `references/self-intro-rules.md` |

## 数据来源（两层）

| 层 | 来源 | 提供什么 |
|----|------|---------|
| 题库层 | `interview-qa/references/qa-db/`（跨 skill 单一事实源） | 通用题干 + 回答框架 + 融合钩子（122 题，五类） |
| 事实层 | `projects/proj-*/full-card.md`（咬合总账/方案细节/追问预埋）+ `profile/master.md`（骨架/软肋清单） | 具体数字、架构决策、项目名 |
| 口述版 | projects/proj-*/full-card.md → stages.solution + extracted_indices.metrics | — |
| 自我介绍 | profile/master.md + 跨项目 evidence + industry_thread | — |

## QA 演练流程（交互优化环节；协议点 QA-CP-01~03，见 interview-prep/references/interaction-protocol.md）

1. **命中**：读 full-card 主题 tags → 用 `scripts/qa-db-tools.py dedup --query` 与 index.md 命中相关题（预计每项目 25-40 题）
2. **融合**：命中题的"回答框架 × 事实层"按融合钩子注入具体事实，生成个性化答案
3. **逐题交互**：一题一确认（用户可答→对照→追问），符合逐条确认偏好
4. **去重**：与 full-card 追问预埋重叠的题只讲增量，追问预埋是项目专属事实的唯一来源
5. **留存**：默认不落盘；用户要求留存时写入 `interviews/qa-sessions/{日期}-{主题}.md`

> v2.0 变更：不再生成独立 `qa-bank.md` / `outputs/qa-bank-full.md`。full-card 的 `extracted_indices.qa_bank`（追问预埋）是项目专属 QA 的唯一事实源，通用题来自 qa-db。

## 输出存储

```
interview-vault/
├── outputs/
│   ├── oral-versions/
│   │   └── proj-{NNN}-oral.md   # 每个项目的口述版
│   └── self-intro.md            # 自我介绍
└── interviews/qa-sessions/      # QA 演练留存（仅用户要求时）
```
