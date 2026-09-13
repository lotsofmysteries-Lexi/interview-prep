# interview-mock — 面试模拟

角色扮演面试官，基于 vault 全量数据进行模拟面试。支持已知问题测试和未预料问题应变。

## 前置条件

- `interview-vault/profile/master.md` 存在
- `interview-vault/projects/` 下至少有 1 个项目的 `full-card.md`
- 建议至少完成 2 个项目的全量生成再进行模拟

## 使用场景

| 意图 | 说明 |
|------|------|
| "模拟面试" | 完整模拟面试流程 |
| "练习追问" | 针对特定项目的追问练习 |
| "压力面" | 高强度追问模式 |

## 生成流程

详见 `references/simulation-rules.md`。

## 数据来源

| 来源 | 用途 |
|------|------|
| profile/master.md | 面试官了解候选人背景 |
| projects/*/full-card.md | 全量项目档案 |
| projects/*/qa-bank.md | 追问题库 |
| outputs/jd-match/ | JD 匹配缺口（如有） |
| interviews/ | 历史面试记录（如有） |
