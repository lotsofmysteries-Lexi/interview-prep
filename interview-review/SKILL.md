# interview-review — 面试复盘

面试结束后，基于转录文稿和 vault 档案快照进行系统化复盘，产出档案补丁回流到 vault。

## 前置条件

- `interview-vault/profile/master.md` 存在
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`
- 用户提供面试转录文稿（ASR 逐字稿或口述复盘）

## 使用场景

| 意图 | 说明 |
|------|------|
| "面试复盘" / "复盘一下" | 输入转录文稿，执行 4 步复盘 |
| "分析面试表现" | 同上 |
| "面试官问了什么" | 仅执行 Step 1（文稿解析） |

## 生成流程

4 步 pipeline，详见 `references/review-pipeline.md`：

1. 面试转录文稿解析 → 结构化 QA 对列表
2. 查漏补缺卡片比对 → 调用/未调用/缺失分析
3. 面试官立场分析 → 关心点排序 + 隐性需求
4. 档案补丁生成 → HITL 确认后合并回 vault

## 输出存储

```
interview-vault/interviews/<公司-日期>/
├── transcript.md        # 原始转录（用户提供）
├── qa-pairs.md          # Step 1 产出：结构化 QA 对
├── review.md            # Step 2-3 产出：比对结果 + 立场分析
└── patches/             # Step 4 产出：档案补丁
    ├── patch-001.md
    └── ...
```
