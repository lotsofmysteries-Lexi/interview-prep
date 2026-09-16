---
name: interview-resume
description: 简历生成：基于 interview-vault 项目档案自动派生简历，输出可复制文本简历 + 自适应 HTML 简历双版本。当用户要"生成简历""出简历""简历精装版"时使用。
---

# interview-resume — 简历生成

基于 interview-prep 生成的 vault 数据，自动派生简历。输出双版本：可复制文本简历 + 自适应 HTML 简历。

## 前置条件

- `interview-vault/profile/master.md` 存在（用户画像）
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`（完整档案）

如果前置条件不满足，提示用户先使用 interview-prep skill 完成建档和项目生成。

## 使用场景

| 意图 | 说明 |
|------|------|
| "生成简历" | 基于 vault 全量数据生成完整简历 |
| "更新简历" | vault 数据变更后重新生成 |
| "调整简历" | 微调已生成的简历（措辞、排版、排序） |

## 生成流程

1. **读取 vault**：读取画像 + 所有已入库项目的完整档案
2. **确定写作体系**：根据画像中的 `writing_system` 套用对应体系（见 `references/resume-text-rules.md`）
3. **生成项目段**：从每个项目的 6 阶段档案中提取核心内容，压缩为简历项目段
4. **生成个人简介**：（社招才有）从跨项目能力证据中提炼职业主线
5. **组装完整简历**：按写作体系的模块顺序组装
6. **页数检查**：确保 ≤2 页，溢出时按规则精简
7. **输出双版本**：文本版 + HTML 版

## 数据来源映射

| 简历模块 | vault 数据来源 |
|---------|--------------|
| 基础信息 | profile/master.md |
| 个人简介 | 跨项目的 extracted_indices.evidence + industry_thread |
| 教育经历 | profile/master.md → education |
| 工作/项目经历 | projects/proj-*/full-card.md → stages + metadata |
| 专业技能 | projects/proj-*/full-card.md → extracted_indices.skills |
| 量化成果 | projects/proj-*/full-card.md → extracted_indices.metrics |

## 引用规则

- `references/resume-text-rules.md`：三套写作体系 + 项目段压缩规则
- `references/resume-html-template.md`：HTML 排版规格
- `interview-prep/references/calibration-rules.md`：写作哲学 + 禁止清单

## 输出存储

```
interview-vault/outputs/
├── resume-text.md       # 文本版
└── resume.html          # HTML 版
```
