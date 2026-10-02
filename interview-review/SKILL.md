---
name: interview-review
description: 面试复盘：面试结束后基于转录文稿/笔记和 vault 档案做系统化复盘，定位答得失、改写更优回答、生成档案补丁回流 vault。当用户要"复盘刚才的面试""整理面试记录"时使用。
---

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

## 新题回流 qa-db（v2.0 新增）

复盘 Step 1 提取的 QA 对中，**被问到但没准备/答得不好的通用题**（不限于本项目的项目专属细节），
按 `interview-qa/references/qa-db-maintenance.md` 的 SOP 入库 qa-db：
查重（`qa-db-tools.py dedup`）→ 格式入库 → `index` 重建 → CHANGELOG 记一笔。
这是题库四条新题来源渠道中的主渠道，每次复盘顺手完成，不需要用户单独发起。
