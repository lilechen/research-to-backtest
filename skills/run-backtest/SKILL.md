---
name: run-backtest
description: (未实现,占位)把可回测规格 YAML 翻译成 akquant 代码并跑回测,输出回测结果与诊断。规划中,待 specify-backtest 稳定后实现。
---

# 跑回测(未实现)

此 skill 为占位。规划功能:

1. 读入 `<名>.系统规格.yaml`。
2. 把通用算子(SMA/slope/rolling_max/ratio/ATR 等)机械翻译成 akquant Python 代码。
3. 用 `<名>.操作化日志.md` 的高风险行生成敏感性测试(改变操作化选择,看回测结果稳健性)。
4. 跑回测,输出收益曲线、回撤、胜率、交易明细。
5. 把回测结果与策略 .md 中的历史案例对照,标记显著偏离。

状态:未实现。先用 `extract-trading-system` + `specify-backtest` 产出前两阶段产物。
