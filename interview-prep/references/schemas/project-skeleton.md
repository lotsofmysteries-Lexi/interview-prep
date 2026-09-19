# 一页纸骨架 Schema

## 字段定义

```yaml
project_skeleton:
  project_name: string
    # 以业务场景命名，不用"XX AI 系统"
    # 示例："施工合同智能风控平台"

  one_line_positioning: string
    # 一句话定位，≤30字，业务价值先行，技术服务于理解
    # 示例："给施工企业做'合同条款秒级风险筛查'的智能审查平台"

  time_period: string
    # 格式：YYYY.MM - YYYY.MM 或 YYYY.MM - 至今
    # 约束：必须与时间线→技术栈匹配表一致（参见 calibration-rules.md）

  company: string
    # 用户填写或系统建议，脱敏处理（如"某建筑集团"）

  business_background:
    why_do_it: string
      # 业务背景——为什么要做这个项目，含业务规模数据
    why_ai: string
      # 为什么用AI——该场景的AI适配性论证

  project_objectives:
    business_objective: string
      # 业务目标，含具体数值预期
    ai_objective: string
      # AI效果目标（准确率/召回率/延迟等），含数值预期

  your_role: string
    # 基于年限自动校准的角色描述
    # 示例："产品经理（独立负责AI产品线，向产品总监汇报）"

  delivery_mode: string
    # 继承自用户画像，可按项目微调
    # 示例："核心方案自主设计，开发执行部分外包，你负责方案主导+技术对接+验收"

  tech_stack: string
    # 必须与时间线对应的技术时代匹配
    # 骨架阶段用泛化表述（如"混合检索+规则引擎+大模型推理"），Phase 3 再展开具体组件
    # 示例："混合检索 + 规则引擎 + 大模型推理"

  team_composition: string
    # 团队构成，含角色和人数
    # 示例："产品1人（你）+ 后端2人 + 前端1人 + 法务顾问1人 + 外包AI团队3-4人"

  expected_metrics:
    - metric_name: string
      before: string
      after: string
      improvement: string
    # 示例：
    # - 审查周期：5天 → 1天（-80%）
    # - 高风险漏检率：18% → 4.5%（-75%）
    # 约束：数值必须通过行业常识校验（参见 calibration-rules.md）

  source_boundary:
    # 必填。骨架之后独立成节 `## 信源分界`，不在 yaml 里展开，此处仅登记元信息
    # 详见 references/source-boundary.md
    direct: [string]
      # 🟢 原件直给——素材里能指到原句的内容
    inferred: [string]
      # 🟡 素材提到了方向，量级/数字为系统推演
    fabricated: [string]
      # 🔴 素材零字、全部推演（核心卖点/技术决策/价值主张常落在此档）
    skeleton_level_risk: string
      # ⚠️ 骨架级风险：一旦不符需整个项目重做的那一项（区别于数字级）
      # 三个典型位置：核心差异化是什么 / 用户实际负责什么 / 成果是什么
    source_strength: enum [书面详实, 书面薄弱, 仅口述, 无任何依据]
      # 仅"无任何依据"或"仅口述"时，分界节开头须直白说明源本身的问题
```

## 校验规则

- `time_period` 与 `tech_stack` 必须匹配时代（calibration-rules.md）
- `your_role` 的措辞必须与用户年限对应的叙事视角一致
- `expected_metrics` 的数值必须与 `team_composition` 和 `time_period` 规模匹配
- `company` 如涉及真实公司名须脱敏
- **`source_boundary` 必填**：三档均需给出（某档为空也要显式写"无"），且必须标出 `skeleton_level_risk`
- **`source_strength` 为"仅口述"或"无任何依据"时**：核对清单第 1 位必须是前置项
  「这段经历是否存在」，并提示该内容无法通过背调

## Vault 存储路径

`interview-vault/projects/proj-{NNN}/skeleton.md`
