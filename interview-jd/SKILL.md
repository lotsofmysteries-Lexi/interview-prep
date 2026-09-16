---
name: interview-jd
description: JD 解析与人岗匹配：解析目标岗位 JD，与 vault 项目档案做匹配分析，产出匹配度报告、缺口清单、迁移建议和简历裁剪策略。当用户发来 JD 要求"解析这个岗位""匹配度怎么样""针对性改简历"时使用。
---

# interview-jd — JD 解析 + 匹配

解析目标岗位的 JD，与 vault 中的项目档案做匹配分析，产出匹配度报告、缺口清单和迁移建议。

## 前置条件

- `interview-vault/profile/master.md` 存在
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`
- 用户提供目标 JD 文本

## 使用场景

| 意图 | 说明 |
|------|------|
| "分析这个 JD" | 输入 JD 文本，输出匹配报告 |
| "跟我的经历匹配吗" | JD vs vault 数据的匹配分析 |
| "差距在哪" | 缺口分析 + 迁移建议 |

## 生成流程

详见 `references/jd-match-rules.md`。

## 输出存储

```
interview-vault/outputs/jd-match/<公司-岗位>/
├── jd-analysis.md       # JD 解析
└── match-report.md      # 匹配报告
```
