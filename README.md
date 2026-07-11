<div align="center">

# research-to-backtest

**把一本交易书/论文 PDF,变成可回测的交易系统。**

Claude Code skill 套件 · `PDF → 人读策略 → 结构化规格 → 回测`

<p>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/lilechen/research-to-backtest?style=flat-square&label=License" alt="License: MIT"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/stargazers"><img src="https://img.shields.io/github/stars/lilechen/research-to-backtest?style=flat-square" alt="Stars"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/issues"><img src="https://img.shields.io/github/issues/lilechen/research-to-backtest?style=flat-square" alt="Issues"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/commits/main"><img src="https://img.shields.io/github/last-commit/lilechen/research-to-backtest?style=flat-square" alt="Last Commit"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/tree/main/skills"><img src="https://img.shields.io/badge/Claude%20Code-Skills-blueviolet?style=flat-square" alt="Claude Code Skills"/></a>
</p>

[English](README.en.md) · [示例](#示例) · [安装](#快速开始) · [贡献](#贡献)

</div>

---

## 目录

- [问题](#问题)
- [解决](#解决)
- [管线](#管线)
- [快速开始](#快速开始)
- [示例](#示例)
- [设计原则](#设计原则)
- [它是怎么工作的](#它是怎么工作的)
- [路线图](#路线图)
- [贡献](#贡献)
- [测试](#测试)
- [许可证](#许可证)
- [致谢](#致谢)

---

## 问题

交易书描述方法时大量使用**判断词**——"RS 改善""均线走平""突破阻力""头肩底"。人能读懂,回测引擎不认。

直接回测书里的方法,回测的其实是某个**操作化版本**,不是原方法。大多数人跳过操作化这一步,得到的结果看起来合理,但跟他们实际坐在屏幕前会做的事对不上。

**问题不是缺回测能力,是缺一个把"人读判断"和"机器可计算"分开、并诚实记录每一步翻译的中间产物。**

## 解决

一个三阶段 Claude Code skill 套件,把一本书或一篇论文 PDF 变成既能**人手交易**又能**机械回测**的东西:

| 阶段 | 做什么 | 产物 |
|---|---|---|
| **1. 抽取** | 提炼交易系统为人可读文档(保留判断词,每条规则标页码) | `<name>.trading-system.md` |
| **2. 规格化** | 翻译为框架无关 YAML + **操作化日志**(逐条记"原话 → 谓词"和保真度风险) | `<name>.system-spec.yaml` + `<name>.operationalization-log.md` |
| **3. 回测** | 把 YAML 转成回测代码(目标:[akquant](https://github.com/lilechen/akquant),Rust-Python 量化框架) | akquant 代码 + 回测结果 |

不可计算元素(头肩底、趋势线、整数心理)诚实**排除并记日志**,绝不强行编码。

## 管线

```
   ┌─────────┐    ┌──────────────────┐    ┌─────────────────────┐    ┌──────────┐
   │  PDF    │    │  人读策略          │    │  框架无关 YAML 规格   │    │  回测     │
   │ book /  │──▶ │  (判断词保留)      │──▶ │  + 操作化日志         │──▶ │  akquant │
   │  paper  │    │  13 节模板          │    │  (每条映射 + 风险)    │    │  代码     │
   └─────────┘    └──────────────────┘    └─────────────────────┘    └──────────┘
        ▲                 ▲                          ▲                      ▲
        │                 │                          │                      │
   extract-             (你读得                 specify-backtest         run-backtest
   trading-              懂的判断)              (忠实翻译)              (待实现 ⏳)
   system
   ✅ v1
```

**为什么分两步?** 因为**回测的不是原方法,是操作化版本**。如果不知道操作化怎么做的,回测结果对你没有意义。操作化日志是这件事的灵魂。

## 快速开始

### 前置依赖

- [Claude Code](https://docs.claude.com/claude-code) CLI(已登录)
- macOS / Linux(`pdftotext` 在 macOS 默认有;Linux 需 `apt install poppler-utils`)
- Python 3.10+(仅运行辅助脚本时)

### 安装

```bash
git clone https://github.com/lilechen/research-to-backtest.git
cd research-to-backtest

# 把 skills 软链到 Claude Code skills 目录
ln -s "$(pwd)/skills/extract-trading-system" ~/.claude/skills/extract-trading-system
ln -s "$(pwd)/skills/specify-backtest"        ~/.claude/skills/specify-backtest
```

### 使用

```bash
# 阶段 1:从 PDF 抽取人读策略
$extract-trading-system
> PDF: /path/to/book.pdf
> 类型: book   # 或 paper

# 阶段 2:转可回测规格
$specify-backtest
> 策略: /path/to/<name>.trading-system.md
```

**产物**:

- 阶段 1 → `<name>.trading-system.md`(放在 PDF 同目录或 `examples/<书名>/`)
- 阶段 2 → `<name>.system-spec.yaml` + `<name>.operationalization-log.md`

**务必审日志里「高风险」行**——这些是回测与原方法偏差最大的地方。

## 示例

`examples/` 下每本书一个子文件夹,覆盖两种典型文献风格:

| 文件夹 | 文献 | 类型 | 演示 |
|---|---|---|---|
| [`Weinstein/`](examples/Weinstein/) | Stan Weinstein《Secrets for Profiting in Bull and Bear Markets》 | book | **完整三阶段管线** —— 阶段分析 + 视觉判据 + 形态工具 + 系统规格 YAML + 操作化日志 |
| [`Clenow/`](examples/Clenow/) | Andreas F. Clenow《Following the Trend》 | book | **完整三阶段管线** —— 全定量 CTA 趋势跟踪,含 4 档风控(7.5/10/15/30bp)、30 年板块归因表、2002-2021 逐年收益 |
| [`Oneil/`](examples/Oneil/) | William J. O'Neil《How to Make Money in Stocks》 | book | **阶段 1(CANSLIM 成长股风格)** —— 七要素筛选 + cup-with-handle / base 等形态 + 7 个月周期 |

跑新文献时,在 `examples/<书名>/` 下放对应三份产物(若已跑阶段 2)。

## 设计原则

1. **人可读优先。** 阶段 1 保留判断词,人照着能做,心里清楚哪些是判断、哪些是客观规则。
2. **操作化日志是灵魂。** 阶段 2 逐条记录"原话 → 谓词"映射,每条标保真度风险(低/中/高)。**没有日志的规格不可信。**
3. **诚实缺口。** 非可计算元素排除并记日志,从不编造或强行编码。书中明确 vs 推断严格区分。
4. **框架无关。** YAML 用通用算子(SMA / slope / rolling_max / ratio / ATR),任何回测引擎都能消费。
5. **原话数字原样保留。** 关键判据都标 PDF 页码,便于人工核对。

## 它是怎么工作的

### 仓库结构

```
research-to-backtest/
├── skills/
│   ├── extract-trading-system/       Stage 1: PDF → 人读策略
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── system-template.md           (13 节模板)
│   │   │   ├── reader-prompt.md             (并行 reader 子 agent 提示词)
│   │   │   ├── synthesizer-prompt.md        (合并子 agent 提示词)
│   │   │   ├── long-pdf-reading.md          (长 PDF 并行分段协议)
│   │   │   └── extract-and-chunk.py         (pdftotext 分块脚本)
│   │   └── agents/openai.yaml
│   ├── specify-backtest/              Stage 2: 策略 → YAML + 日志
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── spec-schema.yaml
│   │   │   ├── operationalization-guide.md
│   │   │   └── critic-prompt.md             (对抗式检查)
│   │   └── agents/openai.yaml
│   └── run-backtest/                  Stage 3: 规格 → 回测 (TBD)
├── examples/
│   ├── Weinstein/                     (3 份:trading-system + spec + log)
│   ├── Clenow/                        (3 份:trading-system + spec + log)
│   └── Oneil/                         (1 份:trading-system,Stage 2 待补)
├── README.md / README.en.md
└── LICENSE
```

### 阶段 1 内部流程(`extract-trading-system`)

```
PDF → mdls 查页数
     → ≤80 页:单次精读
     → >80 页:按 ~60 页分块 (extract-and-chunk.py)
                ↓
                N 个 reader agent 并行(读 .txt,Write 笔记到 /tmp/...)
                ↓
                1 个 synthesizer agent(读全部笔记 + example,Write 最终文档)
                ↓
                13 节完整文档
```

### 模型兼容性

- **支持图像输入的模型**(GPT-4o / Claude / 等):reader 用 Read 的 `pages` 参数视觉读 PDF。
- **纯文本模型**(如 glm 系列):自动 fallback 到 `pdftotext` 提取 + reader 读 `.txt`(附 `=== PAGE N ===` 标记)。
- 检测信号:试读时返回 `Model only support text input` 即切到 fallback。

## 路线图

| 阶段 | skill | 状态 | 备注 |
|---|---|---|---|
| 1 | `extract-trading-system` | ✅ v1 | 长 PDF 并行分段、文本模型 fallback、synthesizer 子 agent |
| 2 | `specify-backtest` | ✅ v1 | 框架无关 YAML + 操作化日志 + critic 检查 |
| 3 | `run-backtest` (akquant) | ⏳ 计划中 | 目标:Rust-Python 量化框架,把 YAML 转成回测代码 |

## 贡献

欢迎 Issue 和 PR。

加新 skill:

1. 在 `skills/<your-skill>/` 下创建 `SKILL.md`(参考 `skills/extract-trading-system/SKILL.md` 的格式)
2. 参考材料放 `skills/<your-skill>/references/`
3. 加 agent 描述符 `skills/<your-skill>/agents/openai.yaml`
4. PR 时附一份 example extraction 在 `examples/` 下

提 Issue 描述 bug / 改进点 / 新 skill 想法都可以。

## 测试

每个 skill 自带 reference 文档,作为轻量级集成测试。手动验证:

```bash
# 拿 example book 重跑 stage 1,与 examples/ 下文档对照
$extract-trading-system
> PDF: examples/Weinstein/Weinstein.pdf
# ...对比 examples/Weinstein/Weinstein.trading-system.md
```

后续计划:加 CI + 自动对比 diff。

## 许可证

MIT — 见 [LICENSE](LICENSE)。

## 致谢

- 设计灵感来自 Robert Carver《Systematic Trading》对回测忠实性的强调
- 「操作化日志」框架为本项目原创;觉得有用请给个 star
- 文档处理基于 [poppler](https://poppler.freedesktop.org/) 的 `pdftotext`

---

Made for traders who actually read the books.