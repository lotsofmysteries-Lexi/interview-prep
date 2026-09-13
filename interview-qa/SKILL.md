# interview-qa — 追问 QA + 口述版 + 自我介绍

基于 interview-prep 生成的 vault 数据，派生面试准备的文字材料：追问 QA 库、面试口述版、自我介绍。

## 前置条件

- `interview-vault/profile/master.md` 存在
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`

## 命令路由

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| "QA库" / "追问准备" | QA 库生成 | `references/qa-bank-rules.md` |
| "口述版" / "怎么讲" | 口述版生成 | `references/oral-version-rules.md` |
| "自我介绍" | 自我介绍生成 | `references/self-intro-rules.md` |

## 数据来源

| 输出 | vault 数据来源 |
|------|--------------|
| QA 库 | projects/proj-*/full-card.md → stages.probing_prep + extracted_indices.qa_bank |
| 口述版 | projects/proj-*/full-card.md → stages.solution + extracted_indices.metrics |
| 自我介绍 | profile/master.md + 跨项目 evidence + industry_thread |

## 输出存储

```
interview-vault/outputs/
├── qa-bank-full.md          # 全量 QA 库
├── oral-versions/
│   └── proj-{NNN}-oral.md   # 每个项目的口述版
└── self-intro.md            # 自我介绍
```
