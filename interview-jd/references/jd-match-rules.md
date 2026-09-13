# JD 解析与匹配规则

## Step 1: JD 结构化解析

将 JD 原文解析为结构化字段：

```yaml
jd_analysis:
  company: string
  position: string
  level: string           # 推断的职级（初级/中级/高级/资深）

  requirements:
    hard_skills:
      - skill: string
        required: boolean  # 必须 vs 优先
        evidence: string   # JD 原文中的表述
    soft_skills:
      - skill: string
        evidence: string

    experience:
      years: string        # 如"3-5年"
      industry: string     # 行业要求（如有）
      specific: list       # 特定经验要求（如"有大模型落地经验"）

    education:
      level: string
      major: string | null

  responsibilities:
    - string               # 岗位职责，逐条

  hidden_requirements:
    - requirement: string  # 从职责描述中推断的隐性要求
      reasoning: string    # 推断依据
```

## Step 2: 匹配分析

将 JD 要求与 vault 数据逐项比对：

### 数据来源

| JD 要求 | vault 匹配源 |
|---------|-------------|
| 硬技能 | projects/*/extracted_indices.skills |
| 经验年限 | profile/master.md → work_years |
| 行业经验 | profile/master.md → industry_background |
| 特定经验 | projects/*/extracted_indices.keywords + evidence |
| 软技能 | projects/*/extracted_indices.evidence |

### 匹配度评分

| 匹配状态 | 说明 | 分值 |
|---------|------|------|
| 完全匹配 | vault 中有对应技能/经验，且有项目证据 | 100% |
| 部分匹配 | 有相关但不完全对应的经验（可迁移） | 60% |
| 弱匹配 | vault 中有提及但没有深入使用 | 30% |
| 未匹配 | vault 中找不到对应内容 | 0% |

### 匹配报告格式

```
JD 匹配报告：[公司] - [岗位]
─────────────────────────────────────────

整体匹配度：78%

硬技能匹配
  ✅ RAG 系统搭建：完全匹配
     证据：项目2中搭建了建筑规范文档的 RAG 检索系统（extracted_indices.skills）
  ⚠️ Agent 开发经验：部分匹配
     证据：项目3中有 Agent 工作流设计经验，但偏产品侧，JD 要求有工程实现经验
     迁移建议：强调你在 Agent 工作流中的技术选型和架构决策
  ❌ 多模态模型经验：未匹配
     建议：如实说明，强调你在文档混合内容（表格+图纸+文本）处理上的经验可迁移

经验匹配
  ✅ 工作年限：匹配（JD要求3-5年，你有4年）
  ✅ 行业经验：匹配（建筑/工程行业AI落地）
  ⚠️ 团队管理经验：JD提到"带团队"，你的经历以独立负责为主
     迁移建议：强调跨部门协调和外包团队管理经验

缺口清单（按重要性排序）
  1. 多模态模型经验（JD 必须项）→ 建议准备迁移叙事
  2. 团队管理经验（JD 优先项）→ 建议包装跨部门协调为管理经验
  3. ...

简历调整建议
  - 项目2 的描述中增加"混合内容处理"的技术细节，靠近多模态方向
  - 个人简介中增加"跨团队协调"相关表述
  - 技能清单中补充 [JD 中出现但简历未列的技能]
─────────────────────────────────────────
```

## Step 3: 用户参与

```
以上是 JD 匹配分析结果。

对于未匹配和部分匹配的项，你可以：
  1. 告诉我你其实有相关经验，我来补充到 vault 中
  2. 确认缺口，我提供迁移叙事的建议
  3. 根据匹配结果调整简历侧重点

你想怎么处理？
```

## 联动其他 skill

- 匹配报告可触发 interview-resume 重新生成（调整简历侧重）
- 缺口清单可输入 interview-mock（面试模拟时重点考察缺口区域）
- JD 分析结果可输入 interview-qa（补充 JD 相关的追问准备）
