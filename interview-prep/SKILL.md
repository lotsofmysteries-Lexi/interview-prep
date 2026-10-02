---
name: interview-prep
description: 面试准备项目生成引擎：深度采集用户信息，推演生成完整 AI 项目档案（interview-vault），供简历、QA、面试模拟等下游 skill 使用。当用户要准备 AI 岗位面试、系统化构建项目经历、建档/新建项目/选场景/生成骨架/生成详情/入库时使用。
---

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
Phase 1+2 × 项目1  场景 → 骨架确认（+对比表初始版）
Phase 1+2 × 项目2  场景 → 骨架确认（+增量冲突检查）
Phase 1+2 × 项目3  场景 → 骨架确认（+增量检查+终检 = 复核完成）
  ↓
简历框架（基于骨架先出一版，仅展示）
  ↓
Phase 3+4 × 项目1  全量生成（立项/方案/测试逐段确认，需求/数据/部署打包确认）→ 入库
Phase 3+4 × 项目2  全量生成 → 入库
Phase 3+4 × 项目3  全量生成 → 入库
  ↓
全量下游输出（简历精装版 / QA演练 / 口述版 / 技能清单 ...）
```

### 生成策略（Token/效率规则，强制）

1. **渐进式文件加载**：进入对应 Phase 才读该 phase 的 reference 文件，禁止一次性全量加载。用户中途跳阶段时，补读目标阶段的 reference 再继续
2. **增量生成**：多轮扩写/修改用**增量 Edit** 替代全文件重写；扩写前先输出"扩写计划"（改哪几节、各节加什么）经用户确认再动手，避免返工整篇重写
3. **机械操作转脚本**：索引生成、格式校验、文件合并等确定性操作一律走 `scripts/`，不占对话 token

### 交互 log（收尾强制）

会话结束（Phase 4 入库完成或用户中止）时，按 `references/usage-log-protocol.md` 自动生成全量交互 log：过程中只写 JSONL 轻量记录点（`skill-logs/records/`），收尾用 `interview-prep/scripts/usage-log-tools.py` 汇编成文。用户明确说"不用记 log"可跳过成文，记录点照常写。

### 写作哲学

- 不写痛点，写行动和交付物
- 写营收不写省钱
- 具体不抽象，每个数字可验证
- 生成逻辑是推演不是扩写
- 详见 `references/calibration-rules.md` 第7节

### 信源分界（强制）

推演的副作用是**真实内容与虚构内容在成品里长得一模一样**。所以每个项目的骨架（存于
`profile/master.md` 的「项目骨架一览」章节）必须附一节 `## 信源分界`，把全部内容按
🟢原件直给 / 🟡有线索·数字待填 / 🔴零字全推演 三档归类，
并标出**骨架级风险**（方向错了要整个重做的那一项，区别于数字级风险）。

- 素材薄弱时（一句话或零量化），分界节开头必须先说明源本身的问题，而不是只列"数字待替换"
- Phase 2 终检时（随末个骨架确认），在 `outputs/resume-framework.md` 输出「信源分界总表」+ 风险排序
- 详见 `references/source-boundary.md`

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

## 数据存储（v2.0 结构）

```
interview-vault/
├── profile/master.md                    # Phase 0 画像 + 各项目骨架（「项目骨架一览」章节，Phase 2 追加）+ 信源分界
├── projects/proj-{NNN}/
│   └── full-card.md                     # Phase 3+4 产出：项目唯一全量档案
│                                        #   （综述 / 6阶段方案 / 咬合总账 / 追问预埋 / extracted_indices）
├── outputs/
│   └── resume-framework.md              # Phase 2 终检后产出
└── interviews/                          # 面试复盘 + QA 演练留存
```

**v2.0 去冗余规则**（分层事实源，任何信息只存一处）：

| 信息 | 唯一存储位置 |
|------|-------------|
| 骨架级内容（一页纸骨架 + 信源分界） | `profile/master.md` 项目骨架一览 |
| 方案级内容（6 阶段方案 / 咬合总账 / 追问预埋） | `projects/proj-{NNN}/full-card.md` |
| QA 题目（通用题库） | `interview-qa/references/qa-db/`（跨 skill 单一事实源，本 skill 跨包引用，不复制） |
| QA 事实答案 | 不落独立文件——由 interview-qa 交互环节现场生成（qa-db 命中 × full-card 事实），留存才写入 `interviews/` |

> v1 的 `projects/proj-{NNN}/skeleton.md` 与 `qa-bank.md` 已废弃；旧 vault 按 phase4 的迁移说明一次性并入。

## 下游 skill

本 skill 的产出（vault 数据）供以下下游 skill 使用：

| Skill | 用途 | 依赖 |
|-------|------|------|
| interview-resume | 简历生成 | profile（含骨架一览）+ projects；业务价值段遵循 `references/north-star-metrics.md` |
| interview-qa | 交互式 QA 演练 + 口述版 + 自我介绍 | `interview-qa/references/qa-db/`（题库层）× full-card（事实层）|
| interview-jd | JD 解析 + 匹配 | profile + projects（keywords）|
| interview-mock | 面试模拟 | 全部 vault 数据 + qa-db |
| interview-review | 面试复盘 | 全部 vault 数据 + 面试记录；新题回流 qa-db |
