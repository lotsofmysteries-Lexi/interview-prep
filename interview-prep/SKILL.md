# interview-prep — 项目生成引擎

面试准备的本体 skill。通过深度采集用户信息，推演生成完整的 AI 项目档案，供下游 skill（简历、QA、面试模拟等）使用。

## 使用场景

用户想准备 AI 相关岗位的面试，需要系统化地构建项目经历。

## 前置检查

1. 检查 `interview-vault/profile/master.md` 是否存在
   - 不存在 → 进入 Phase 0 建档
   - 存在 → 读取画像，跳过 Phase 0

2. 检查 `interview-vault/projects/` 下已有项目数量
   - 与画像中的项目蓝图对比，确认还需要生成几个项目

## 命令路由

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| 首次使用 / "开始" / "建档" | Phase 0 | `references/phase0-profiling.md` |
| "新建项目" / "下一个项目" | Phase 1→2→3→4 | 按顺序走完一个项目的生成流程 |
| "选场景" | Phase 1 | `references/phase1-scene-selection.md` |
| "生成骨架" | Phase 2 | `references/phase2-skeleton.md` |
| "生成详情" / "全量生成" | Phase 3 | `references/phase3-full-generation.md` |
| "入库" / "评估准备度" | Phase 4 | `references/phase4-vault-entry.md` |
| "查看状态" / "进度" | 状态总览 | 列出所有项目及其当前阶段 |

## 全局规则

### 交互节奏（先广后深）

```
Phase 0  建档（一次性）
  ↓
Phase 1+2 × 项目1  场景 → 骨架
Phase 1+2 × 项目2  场景 → 骨架
Phase 1+2 × 项目3  场景 → 骨架
  ↓
统一复核（所有骨架并排对比）
  ↓
简历框架（基于骨架先出一版）
  ↓
Phase 3+4 × 项目1  全量生成 → 入库
Phase 3+4 × 项目2  全量生成 → 入库
Phase 3+4 × 项目3  全量生成 → 入库
  ↓
全量下游输出（简历精装版 / QA库 / 口述版 / 技能清单 ...）
```

### 写作哲学

- 不写痛点，写行动和交付物
- 写营收不写省钱
- 具体不抽象，每个数字可验证
- 生成逻辑是推演不是扩写
- 详见 `references/calibration-rules.md` 第7节

### 校准规则

所有项目生成环节必须遵循 `references/calibration-rules.md` 中的校准规则：
- 年限 → 项目数量 / 叙事视角
- 时间线 → 技术栈匹配
- 交付模式 → 叙事视角
- 落地参数 → 合理范围

### 内容结构

每个阶段的内容遵循 `references/schemas/stage-content.md`：
- 方案本体（最终方案 + 演进脉络）
- 落地参数（数字互相咬合）
- 追问预埋（4类：方案/决策/落地/反思）

### 交付模式原则

无论用户的交付模式是自研、外包还是服务商合作，生成的内容都必须确保：用户能讲清每一个技术决策的理由。交付模式只影响"谁执行"，不影响"谁懂技术"。

## 数据存储

```
interview-vault/
├── profile/master.md                    # Phase 0 产出
├── projects/proj-{NNN}/
│   ├── skeleton.md                      # Phase 2 产出
│   ├── full-card.md                     # Phase 3+4 产出
│   └── qa-bank.md                       # Phase 4 提取
├── outputs/
│   └── resume-framework.md              # Phase 2 统一复核后产出
└── interviews/                          # 面试复盘产出
```

## 下游 skill

本 skill 的产出（vault 数据）供以下下游 skill 使用：

| Skill | 用途 | 依赖 |
|-------|------|------|
| interview-resume | 简历生成 | profile + projects |
| interview-qa | 追问QA + 口述版 + 自我介绍 | projects（qa_bank + extracted_indices）|
| interview-jd | JD 解析 + 匹配 | profile + projects（keywords）|
| interview-mock | 面试模拟 | 全部 vault 数据 |
| interview-review | 面试复盘 | 全部 vault 数据 + 面试记录 |
