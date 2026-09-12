# 完整项目档案 Schema

一个项目的完整档案 = metadata + 6 个阶段内容块 + 自动提取索引。

## 结构定义

```yaml
project_card:
  # ── 元数据 ──
  metadata:
    project_id: string          # 如 "proj-001"
    skeleton_ref: string        # 关联的骨架文件路径
    created_at: date
    last_modified: date
    readiness_score: integer    # 准备度评分（0-100），Phase 4 计算
    readiness_details: string   # 准备度说明

  # ── 6 阶段内容 ──
  stages:
    - stage_1_initiation:       # 立项与业务价值
        <<: *stage-content       # 遵循 stage-content.md schema
    - stage_2_requirements:     # 需求分析
        <<: *stage-content
    - stage_3_data:             # 数据准备
        <<: *stage-content
    - stage_4_design:           # 方案设计
        <<: *stage-content
    - stage_5_testing:          # 测试验证
        <<: *stage-content
    - stage_6_deployment:       # 部署与运营
        <<: *stage-content

  # ── 自动提取索引（Phase 4 入库时生成）──
  extracted_indices:
    skills:
      - skill_name: string
        source_stage: string    # 从哪个阶段提取
        proficiency: enum [能用, 懂原理, 能讲取舍]
          # 能用：仅在技术栈中提及
          # 懂原理：在方案本体中有具体描述
          # 能讲取舍：在演进脉络中有决策讨论

    metrics:
      - metric_name: string
        value: string
        source: string          # 来自哪个阶段的落地参数或成果

    evidence:
      - capability: string     # 能力标签（如"技术选型""跨部门协调"）
        proof: string          # 证据（引用方案本体或演进脉络的具体内容）
        source_stage: string

    qa_bank:
      - question: string
        answer: string
        type: enum [方案类, 决策类, 落地类, 反思类]
        source_stage: string
        probing_intensity: enum [极高, 高, 中]

    keywords:
      - string                 # 全文提取的关键词，供 JD 匹配使用
```

## Vault 存储路径

```
interview-vault/projects/proj-{NNN}/
├── skeleton.md      # 一页纸骨架（Phase 2 产出）
├── full-card.md     # 完整档案（Phase 3+4 产出，遵循本 schema）
└── qa-bank.md       # 追问QA库（从 extracted_indices.qa_bank 单独导出）
```

## 版本与补丁

面试复盘（interview-review skill）可能产生档案补丁：
- 补丁存储在 `interview-vault/interviews/<公司-日期>/patches/`
- 补丁经用户 HITL 确认后合并回 `full-card.md`
- 合并后 `last_modified` 更新，`readiness_score` 重新计算
