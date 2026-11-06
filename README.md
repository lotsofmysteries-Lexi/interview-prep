# interview-skills

WorkBuddy 面试准备 skill 套件，含 6 个协同工作的 skill：

| Skill | 用途 |
|-------|------|
| `interview-prep` | 面试准备本体：深度建档 → 场景选择 → 项目骨架 → 全量方案 → 入库，生成项目唯一档案（full-card） |
| `interview-jd` | JD 解析 + 人岗匹配（快档），深度公司/岗位分析 + 求职画像维护（深档，盖洛普框架） |
| `interview-qa` | 交互式 QA 演练：自我介绍口述版 + 题库（qa-db）× 项目档案现场生成问答 |
| `interview-resume` | 简历生成：可投递正式简历（个人简介三行三句、禁技术细节词）+ HTML 版 |
| `interview-mock` | 面试模拟：按面试官类型单点演练 |
| `interview-review` | 面试复盘：面后回流，新题入库、补丁合并回项目档案 |

数据全部落盘在本地 `interview-vault/`，简历、QA、模拟面试共享同一套项目档案。

## 安装

一条命令安装全部 6 个 skill（需要 Node ≥ 16.14）：

```bash
npx github:lotsofmysteries-Lexi/interview-prep
```

只安装其中一个：

```bash
npx github:lotsofmysteries-Lexi/interview-prep interview-prep
npx github:lotsofmysteries-Lexi/interview-prep interview-jd
```

Skill 会被复制到 `~/.workbuddy/skills/<skill名>/`。安装后重启 WorkBuddy（或重新扫描 skill）即可生效。

## 使用

在 WorkBuddy 对话中：

```
/interview-prep 开始        # 首次建档，建立个人画像与项目蓝图
/interview-prep 新建项目    # 生成一个完整项目档案
/interview-prep 查看状态    # 查看当前进度与下一步动作
```

建档完成后按面试环节继续：`/interview-jd`（JD 匹配）→ `/interview-resume`（简历）→ `/interview-qa`（问答演练）→ `/interview-mock`（模拟面试）→ `/interview-review`（面后复盘）。

## 更新

重新执行安装命令即可覆盖为最新版：

```bash
npx github:lotsofmysteries-Lexi/interview-prep
```

注意：覆盖会替换 `~/.workbuddy/skills/` 下的 skill 代码；`interview-vault/` 数据目录不受影响。

## 本地开发

```bash
git clone https://github.com/lotsofmysteries-Lexi/interview-prep.git
cd interview-prep
node cli.js                    # 把当前仓库的 6 个 skill 装到本机
node cli.js interview-prep     # 只装一个
```
