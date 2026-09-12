# 一页纸骨架 Schema

## 字段定义

```yaml
project_skeleton:
  project_name: string
    # 示例："AI合同条款风险分级助手"

  one_line_positioning: string
    # 一句话定位，≤30字
    # 示例："为建筑施工企业提供合同条款自动审查与风险分级的AI产品"

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
    # 示例："RAG + 规则引擎 + LLM辅助判断"

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
```

## 校验规则

- `time_period` 与 `tech_stack` 必须匹配时代（calibration-rules.md）
- `your_role` 的措辞必须与用户年限对应的叙事视角一致
- `expected_metrics` 的数值必须与 `team_composition` 和 `time_period` 规模匹配
- `company` 如涉及真实公司名须脱敏

## Vault 存储路径

`interview-vault/projects/proj-{NNN}/skeleton.md`
