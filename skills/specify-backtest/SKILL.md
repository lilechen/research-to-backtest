---
name: specify-backtest
description: 把一份人可读的交易系统策略(由 extract-trading-system 产出)转成框架无关、可回测的结构化规格(YAML)和一份操作化日志。用于把策略里的判断词操作化成可计算谓词,逐条记录"书里原话 -> 谓词"的翻译及保真度风险,让回测结果可信、可审、可改。输入为策略 .md 文件,输出为 <name>.system-spec.yaml + <name>.operationalization-log.md。
---

# 转成可回测规格

## 核心流程

1. **先读策略文档。** 读入 `<name>.trading-system.md`,理解整套系统的规则、参数、缺口。
2. **逐条操作化。** 按 `references/operationalization-guide.md`,把每条规则从散文/判断词翻译成可计算谓词(指标、参数、方向、阈值)。能直接翻的翻;不能翻的进日志。
3. **填规格。** 按 `references/spec-schema.yaml` 的结构填 YAML。每个字段要么是明确谓词,要么标 `null` + 在日志记缺口。
4. **对抗式检查。** 用 `references/critic-prompt.md` 的挑刺者检查:哪些谓词还有歧义?哪些书中规则没被翻译?哪些参数缺失?据反馈修补。
5. **诚实排除非计算元素。** 头肩底、趋势线、整数心理等不可直接计算的元素,排除并记日志,不强行编码。可给代理变量建议,但须标注「代理」并记保真度风险。
6. **产出两份文件。** `<name>.system-spec.yaml` + `<name>.operationalization-log.md`。

## 操作化日志是灵魂

回测的是"操作化版本",不是原方法。日志逐条记录翻译,每条标保真度风险(低/中/高)。高风险行需用户审阅确认。没有日志的规格不可信。

## 输出约束

- YAML 框架无关(不绑 akquant 或任何特定框架),指标用通用算子(SMA、slope、rolling_max、ratio 等)。
- 每个指标给 name + type + 参数,可被机械翻译成代码。
- regime/state 用状态机表达(如适用)。
- 执行假设(fill、滑点、佣金)显式写出。
- `assumptions` 段汇总所有保真度风险点。
- 日志表:书中原话 | 回测谓词 | 保真度风险(低/中/高) | 备注。

## 参考资料

填规格时,读取 `references/spec-schema.yaml`。
翻译判断词时,读取 `references/operationalization-guide.md`。
做完整性检查时,读取 `references/critic-prompt.md`。
