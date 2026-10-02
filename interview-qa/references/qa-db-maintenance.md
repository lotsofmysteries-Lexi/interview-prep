# qa-db 运营手册

> 读者：skill 运营方（产品方案设计方）。qa-db 是"活题库"，本手册定义持续运营的 SOP。
> 定位：运营只发生在 `interview-qa/references/qa-db/`（单一事实源）；各 vault 的 QA 产物是派生物，题库更新后不自动回流，需要时对某 vault 重跑一次 interview-qa 演练即可。

## 新题来源渠道（四条）

| 渠道 | 说明 | 抓取时机 |
|------|------|---------|
| 面试复盘 | interview-review 从真实面试转录中提取"被问到但没准备/答得不好"的题 | 每次复盘结束顺手入库 |
| 会话 log 信号 | usage-log 的"返工分析/改进信号"字段中暴露的 QA 缺口 | skill 优化迭代时 |
| 行业热点 | 新模型发布、新监管要求、新岗位 JD 出现的新考点 | 不定期 |
| 人工精选 | 看面经、行业文章时的主动收藏 | 随时 |

## 运营 SOP（六步）

### 1. 入库

按统一格式写入对应分类文件（01-05），题号接续该文件现有最大编号：

```markdown
### Q-XX-NNN：{题干}
- tags: [3-5 个小写主题词，从 index.md 既有词表取]
- 回答框架:
  1. {要点，3-6 条，骨架式，不写死具体数字和项目名}
- 融合钩子: {full-card 咬合总账 / full-card 方案细节 / master 骨架一览 / master 软肋清单 / master 用户画像}
```

### 2. 查重

先查重再定题号——近似题合并为已有题的"变体问法"，不另开新题：

```bash
python3 <skill>/interview-qa/scripts/qa-db-tools.py dedup --query "新题题干"
```

### 3. 索引

```bash
python3 <skill>/interview-qa/scripts/qa-db-tools.py index   # 重建 index.md
python3 <skill>/interview-qa/scripts/qa-db-tools.py tags    # 检查同义 tag
```

tags 按既有词表取，避免同义 tag 蔓延（如 `rag`/`RAG`/`检索增强` 只留一个）。

### 4. 版本记录

在 `qa-db/CHANGELOG.md` 顶部追加一行记录：日期 / 来源 / 新增 N 题 / 合并 N 题 / 状态变更 N 题。

### 5. 生命周期

每题可加状态标记（缺省 active）：

- `active`：可用，index.md 只索引 active 题
- `review`：答案框架过期（如涉及已淘汰技术栈），待复核
- `deprecated`：不再考察，保留备查（保留文件内原题，加 `- status: deprecated` 行）

### 6. 复核节奏

**每季度**扫一遍 review 状态题。AI 领域考点衰减快——2024 年的 Agent 框架题到 2026 年可能整体过时；模型版本、评测口径类题目优先复核。

## 工具命令速查

```bash
T=<skill>/interview-qa/scripts/qa-db-tools.py
python3 $T stats                 # 各文件题数 / 状态统计
python3 $T index                 # 重建 index.md
python3 $T tags                  # tags 词表统计 + 近似 tag 提示
python3 $T dedup --query "..."   # 新题查重
```
