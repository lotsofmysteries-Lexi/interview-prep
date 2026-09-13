# 用户画像 Schema

## 采集字段

```yaml
user_profile:
  work_years:
    total: integer          # 总工作年限
    ai_related: integer     # AI相关年限（2023年起算）
    description: "总年限含全部全职经历；AI年限从首个AI相关项目起算"

  education:
    school: string
    major: string
    level: enum [专科, 本科, 硕士, 博士]
    graduation_year: integer
    gpa: string | null      # 可选
    campus_highlights: list  # 可选，校园核心经历

  industry_background:
    - industry: string      # 行业名称（如"建筑工程""金融""电商"）
      years: integer        # 在该行业的年限
      role: string          # 在该行业的角色（如"产品经理""数据分析师"）
    description: "按时间倒序列出所有全职所在行业"

  target_role:
    title: string           # 目标岗位名称（如"AI产品经理"）
    jd_text: string | null  # JD原文（可选，有则用于匹配和差异化）
    company: string | null  # 目标公司（可选）

  existing_materials:
    - type: enum [旧简历, PRD, 项目文档, 原型, 竞品分析, 其他]
      summary: string       # 系统提取的摘要
      raw_content: string   # 原始内容
    description: "用户上传的已有素材，作为项目生成的种子输入"

  delivery_mode:
    primary: enum [全自研, 部分外包, 服务商合作, 混合]
    description: >
      只影响"谁执行"，不影响"谁懂技术"。
      无论哪种模式，用户都深度参与方案设计，对技术细节非常了解。
```

## 系统派生字段（采集完成后自动计算）

```yaml
derived:
  writing_system:
    value: enum [校招, 社招0-5年, 社招5年+]
    rule: "无全职经历→校招；total≤5→社招0-5年；total>5→社招5年+"
    boundary: "4.5-5.5年边界需向用户确认一次"

  project_count_suggestion:
    value: integer
    rule: "参见 calibration-rules.md 年限→项目数量表"

  role_baseline:
    value: string           # 如"模块级主导""端到端负责"
    rule: "参见 calibration-rules.md 年限→叙事视角表"

  industry_thread:
    value: string           # 如"建筑工程行业的AI落地"
    rule: "从 industry_background 提取主线行业"
```

## Vault 存储路径

`interview-vault/profile/master.md`
