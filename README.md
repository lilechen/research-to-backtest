# research-to-backtest

> 一篇文献,一个交易系统。

把交易书或论文( PDF )里的方法,分三步转成可回测的交易系统。

## 管线

| 阶段 | skill | 输入 → 输出 | 产物 |
|---|---|---|---|
| 1 | `extract-trading-system` | PDF → 人读策略 | `<名>.交易系统.md` |
| 2 | `specify-backtest` | 策略.md → 可回测规格 | `<名>.系统规格.yaml` + `<名>.操作化日志.md` |
| 3 | `run-backtest`(未实现) | 规格.yaml → 回测 | akquant 代码 + 回测结果 |

阶段 1 产出人可执行的系统规格;阶段 2 把人版里的判断词操作化成可计算谓词,并逐条记录保真度风险;阶段 3(计划中)落到 akquant 代码并跑回测。

## 为什么分两步(人版 + 可回测版)

书里的方法多用判断词("RS 改善""均线走平""突破阻力")。人能读懂,但回测系统不认。直接回测书的方法,其实回测的是某个"操作化版本",不是原方法。所以:

- 阶段 1 保留判断词,人照着能做,且心里清楚哪些是判断。
- 阶段 2 把每条判断翻译成谓词,用操作化日志记录"书里原话 → 谓词"及保真度风险,你能逐条审、逐条改。
- 非可计算元素(头肩底、趋势线、整数心理)诚实排除并记日志,不强行编码。

## 安装

把 `skills/` 下的目录软链或复制到 Claude Code 的 skill 目录,例如:

```bash
ln -s "$(pwd)/skills/extract-trading-system" ~/Desktop/invest/skill/extract-trading-system
ln -s "$(pwd)/skills/specify-backtest" ~/Desktop/invest/skill/specify-backtest
```

之后用 `$extract-trading-system` / `$specify-backtest` 或 `/extract-trading-system` / `/specify-backtest` 触发。

## 使用

### 阶段 1:抽取交易系统
```
$extract-trading-system
PDF: /path/to/book.pdf
类型: book   # 或 paper
```
产出 `<名>.交易系统.md`。

### 阶段 2:转成可回测规格
```
$specify-backtest
策略: /path/to/<名>.交易系统.md
```
产出 `<名>.系统规格.yaml` + `<名>.操作化日志.md`。审日志里"高风险"行,按需改规格后重跑。

## 示例

`examples/` 下有从 Stan Weinstein《Secrets for Profiting in Bull and Bear Markets》生成的完整示例(三份文件),可作为参考。

## 设计要点

- 长 PDF(>80 页)自动并行分段精读再合成。
- 原话数字原样保留,关键判据标页码。
- 书中明确 vs 推断严格区分。
- 缺口诚实记录,不编造。
