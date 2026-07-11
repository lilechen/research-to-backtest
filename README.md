# research-to-backtest

> 一篇文献,一个交易系统。

[English](README.en.md) | 中文

一套 Claude Code skill,把交易书或论文 PDF 里的方法,分阶段转成可回测的交易系统。

```
PDF ──► 人读策略 ──► 结构化规格 ──► 回测
       extract-trading   specify-backtest   run-backtest
```

## 管线

| 阶段 | skill | 输入 -> 输出 | 产物 |
|---|---|---|---|
| 1 | `extract-trading-system` ✅ | PDF -> 人读策略 | `<名>.交易系统.md` |
| 2 | `specify-backtest` ✅ | 策略.md -> 可回测规格 | `<名>.系统规格.yaml` + `<名>.操作化日志.md` |
| 3 | `run-backtest` ⏳ | 规格.yaml -> 回测 | akquant 代码 + 回测结果 |

## 为什么分两步

书里的方法多用判断词("RS 改善""均线走平""突破阻力")。人能读懂,回测系统不认。直接回测书的方法,回测的其实是某个"操作化版本",不是原方法。所以:

- **阶段 1** 保留判断词,人照着能做,心里清楚哪些是判断。
- **阶段 2** 把每条判断翻译成可计算谓词,用操作化日志记录"原话 -> 谓词"及保真度风险,可逐条审、逐条改。
- 非可计算元素(头肩底、趋势线、整数心理)诚实排除并记日志,不强行编码。

## 安装

把 `skills/` 下的目录软链或复制到 Claude Code 的 skill 目录:

```bash
ln -s "$(pwd)/skills/extract-trading-system" <你的 skill 目录>/extract-trading-system
ln -s "$(pwd)/skills/specify-backtest"        <你的 skill 目录>/specify-backtest
```

之后用 `$extract-trading-system` / `$specify-backtest` 触发。

## 使用

```bash
# 阶段 1:从 PDF 抽人读策略
$extract-trading-system
PDF: /path/to/book.pdf
类型: book   # 或 paper

# 阶段 2:转可回测规格
$specify-backtest
策略: /path/to/<名>.交易系统.md
```

阶段 2 产出 `<名>.系统规格.yaml` + `<名>.操作化日志.md`。审日志里"高风险"行,按需改规格后重跑。

## 示例

`examples/` 下每本书一个子文件夹,各文献独立。覆盖两种典型文献风格:

| 文件夹 | 文献 | 类型 | 含文件 | 演示 |
|---|---|---|---|---|
| `Weinstein/` | Stan Weinstein《Secrets for Profiting in Bull and Bear Markets》 | book | 3 份:系统文档 + 系统规格 yaml + 操作化日志 | 完整三阶段管线 |
| `Clenow/` | Andreas F. Clenow《Following the Trend》 | book | 1 份:系统文档 | 阶段 1(量化趋势跟踪风格) |

跑新文献时,在 `examples/<书名>/` 下放对应的三份产物(若已跑阶段 2)。

## 设计要点

- 长 PDF(>80 页)自动并行分段精读再合成(默认 ~60 页/reader,可调)。
- 纯文本模型下用 `pdftotext` 提取文本后让 reader 读 `.txt`(附 `extract-and-chunk.py` 脚本)。
- reader 笔记与最终合成由独立的 synthesizer agent 完成,主对话不做合成长 Write。
- 原话数字原样保留,关键判据标页码。
- 书中明确 vs 推断严格区分。
- 缺口诚实记录,不编造。

## License

MIT,见 [LICENSE](LICENSE)。
