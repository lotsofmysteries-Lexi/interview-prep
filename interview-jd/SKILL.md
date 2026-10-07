---
name: interview-jd
description: JD 解析与人岗匹配 + 深度岗位与公司分析。快档：解析目标岗位 JD，与 vault 项目档案做匹配分析，产出匹配度报告、缺口清单、迁移建议和简历裁剪策略。深档：拆解岗位本质与公司战略定位，联网双子 Agent 检索，人格-岗位匹配，产出 company-analysis.md 深度报告。当用户发来 JD 要求"解析这个岗位""匹配度怎么样""针对性改简历"（快档）或"深度分析这家公司""值不值得去""帮我准备这家公司的面试"（深档）时使用。
---

# interview-jd（匹配报告确认 = JD-CP-01，深档确认 = JD-CP-02/03，见 interview-prep/references/interaction-protocol.md） — JD 解析 + 匹配 + 深度分析

双档设计：

| 档位 | 流程 | 触发 |
|------|------|------|
| 快档 | JD 结构化 + vault 匹配 + 缺口清单 + 简历裁剪 | "分析这个 JD""匹配度怎么样""差距在哪" |
| 深档 | 联网深度分析（岗位本质拆解 + 公司分析 + 人格匹配 + HR 话术） | "深度分析这家公司""值不值得去""帮我准备这家公司的面试"，或快档结束后经 JD-CP-02 确认升级 |

## 前置条件

- `interview-vault/profile/master.md` 存在
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`
- 用户提供目标 JD 文本
- 深档额外：`profile/work-style.yaml`（不存在时按首次引导创建）；联网检索能力

## 快档：JD 解析 + 匹配

解析目标岗位的 JD，与 vault 中的项目档案做匹配分析，产出匹配度报告、缺口清单和迁移建议。流程详见 `references/jd-match-rules.md`。

快档结束后，若用户意图涉及投递决策或面试备战（或主动询问"再深入一点"），发 JD-CP-02 确认升级深档。

## 深档：深度岗位与公司分析

job-analyzer V2.2 方法论融入：不分析 JD 写了什么，拆解岗位本质；基于 work-style 侧写做人格-岗位匹配。

流程详见 `references/deep-analysis/deep-workflow.md`（Phase 0-5），配套框架：

- `references/deep-analysis/analysis-framework.md` — JD 信号解码 + T01-T15 岗位类型框架
- `references/deep-analysis/gallup-framework.md` — 盖洛普四领域映射
- `references/deep-analysis/gallup-profile-guide.md` — 侧写三层架构与渐进式题库（30 条）
- `references/deep-analysis/hr-response-templates.md` — HR 沟通话术模板

## 输出存储

```
interview-vault/outputs/jd-match/<公司-岗位>/
├── jd-analysis.md          # 快档：JD 解析
├── match-report.md         # 快档：匹配报告
└── company-analysis.md     # 深档：8 章深度报告（固定文件名，前端右栏依赖此契约）
```

## 侧写数据

- `interview-vault/profile/work-style.yaml` — 工作偏好/能量模式/职业价值观三层侧写（与 master.md 的事实型画像正交，master 中有链接）
- 每次深档结束后经 JD-CP-03 收集校准反馈 + 2-3 个渐进式侧写问题，更新 work-style.yaml

## 联动其他 skill

- 快档：匹配报告可触发 interview-resume 重新生成；缺口清单可输入 interview-mock；JD 分析结果可输入 interview-qa
- 深档：能力迁移性章节 → interview-resume 业务价值链路；HR 话术 + 岗位本质 → interview-qa 演练第三源；风险与 KPI 推断 → interview-mock 考察点
