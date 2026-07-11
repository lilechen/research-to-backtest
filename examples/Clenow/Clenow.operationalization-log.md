# Clenow 操作化日志

策略来源:Clenow.trading-system.md
规格:Clenow.system-spec.yaml

回测的是「操作化版 Clenow 核心策略(Ch.4)」,不是原方法。下表逐条记录翻译与保真度风险。**高风险行需审阅确认。**

## 操作化日志

| 书中原话 | 回测谓词 | 保真度风险 | 备注 |
|---|---|---|---|
| EMA 50 / EMA 100(指数移动平均) | `EMA(close, 50)` / `EMA(close, 100)` | 低 | 作者明示 Ch.4 p.60 + p.74 |
| 「趋势为多」(EMA 50 > EMA 100) | `regime = bullish` | 低 | Ch.4 p.74 |
| 「趋势为空」(EMA 50 < EMA 100) | `regime = bearish` | 低 | Ch.4 p.74 |
| 「今日 close ≥ 过去 100 日最高 close」 | `close >= rolling_max(close, 100)` | 低 | Ch.4 p.61-62, p.74 明示 |
| 「今日 close ≤ 过去 100 日最低 close」 | `close <= rolling_min(close, 100)` | 低 | Ch.4 p.61-62 |
| 「平多:close ≤ 过去 50 日最低 close」 | `close <= rolling_min(close, 50)` | 低 | Ch.4 p.62, p.74 |
| 「平空:close ≥ 过去 50 日最高 close」 | `close >= rolling_max(close, 50)` | 低 | Ch.4 p.62, p.74 |
| 「入场必须与趋势同向」 | `entry.and: regime == 同向` | 低 | Ch.4 p.74 |
| 「趋势翻转硬出场」 | `exit.long/short: regime == 反向` → 强制平仓 | 低 | Ch.4 p.74 |
| 「多空对称」 | 入场/出场/sizing 全部对称实现(无独立字段) | 低 | Ch.4 p.115 |
| 「必须接每一个信号」 | `always_take: true`,无 filter 字段 | 低 | Ch.4 + p.182, 198 明示 |
| 「信号次日开盘执行」 | `fill: next_open` + `next_day_execution: true` | 中 | 信号→成交差一天;Ch.4 p.61 |
| 「总是假设差入场」 | (作者用 volume-based slippage 算法,Ch.3 p.55) | 中 | 实际滑点难精确建模 |
| ATR20 | `ATR(close, 20, smoothing: ema)` | 低 | Ch.4 p.74 明示 |
| 「0.15% 风险因子」 | `risk_factor: 0.0015` | 低 | Ch.4 p.74 + Table 4.5 核心值 |
| 「合约数 = 0.0015 × Equity / (ATR20 × PointValue)」 | `Contracts = 0.0015 × Equity / (ATR20 × PointValue)` | 低 | Ch.3 p.52 + Ch.4 p.74 明示 |
| 「取整向下,保守」 | `round: down` | 低 | Ch.3 p.52 |
| 「风险因子 4 档:7.5/10/15/30bp」 | 默认 15bp,其他档作敏感性测试 | 低 | Table 4.5 p.77 |
| 「无时间止损」 | `time_stop: null` | -- | 原方法不设 |
| 「无移动止损」 | `trailing: null` | -- | 原方法不设 |
| 「无显式止损单」 | `stop_loss.type: none` | 中 | 出场靠反向 Donchian + 趋势翻转,不是传统 stop;行为接近但语义不同 |
| 「无回撤熔断」 | `drawdown_circuit_breaker: null` | -- | 原方法不设;作者明示缺陷(p.222) |
| 「极端事件人工干预」 | 未编码 | **高** | 作者个人主张(Ch.4 p.175),无阈值,不可系统化 |
| 「组合无自适应风控」 | `max_per_sector/correlation_cap: null` | **高** | 作者明示缺陷(Ch.4 p.222, 255);54 仓时 risk-on 8.1% |
| 「缺口穿透止损风险」(heating oil 2011) | 未编码 | **高** | 日频模型固有风险(Ch.5 p.194);回测版会低估此类损失 |
| 「佣金 $1 + 交易所费 $1.5」 | `commission.per_contract_usd: 2.5` | 中 | 实际随合约价值变化,此处平均化 |
| 「1.5% 管理费(按季付每日计提)」 | `fees.management_annual: 0.015` | 低 | Ch.4 p.83-84 |
| 「15% 业绩费(按年付)+ HWM」 | `fees.performance_annual: 0.15, high_water_mark: true` | 低 | Ch.4 p.83-84 |
| 「65% 闲置投 G7 政府债(2 年期)」 | 入 assumptions | 低 | Ch.4 p.79-81 |
| 「数据用 back-adjusted continuous contracts」 | 入 assumptions | 低 | Ch.2 p.27-30 明示 |
| 「期初资金 US$10M」 | 入 assumptions | 低 | Ch.4 p.131 |
| 「短边作为波动率 dampener」 | (无独立字段,体现于多空对称 sizing) | 中 | 作者哲学(Ch.5 p.116);单独短边表现极差 |
| 「信号触发后立刻处理(无人工)」「必须接」 | `always_take: true` | 低 | Ch.4 + p.182 |
| 「单边/震荡市表现差」 | (无独立规则,体现于「无过滤器」+「靠趋势本身」) | -- | Ch.5 p.86-87 + Ch.6 多年回顾 |
| 2002-2021 演示基金:US$10M → US$121M(年化 13.3% 扣费) | 入 assumptions(用作参考基线) | 低 | Ch.4 p.131, p.229, 233 |
| 30 年板块长边归因:Rates 9.10% / Agri 6.43% / Equities 5.44% / Currencies -0.18% / Non-Agri -0.41% | (作为 backtest 输出对照,非规则) | 低 | Ch.5 Table 5.3 p.119 |

## 高风险行汇总(需审阅)

1. **极端事件人工干预**(Ch.4 p.175):作者个人主张「日波动 > 20% 单日时减仓」,无明确阈值,无法编码。**回测结果会继承此缺失**。
2. **缺口穿透止损**(Ch.5 p.194):日频模型的固有风险(heating oil 2011 单日跳空穿透理论 stop)。**回测版系统性低估此类损失**。
3. **组合层无自适应风控**(Ch.4 p.222):54 仓时 risk-on 达 8.1%,远高于多数 CTA 实盘做法。**个人交易者应自行加仓数上限**。
4. **「多空对称」隐含短边单独无意义**(Ch.5 p.116):短边 -2.13% 复合 + -54.27% 最大回撤。短边作为保险有价值,作为独立策略毫无价值。

## 排除项(原方法中不可直接计算的元素)

| 元素 | 处理 | 备注 |
|---|---|---|
| 图形形态(头肩底、双底等) | 排除 | 作者核心策略不依赖形态(Ch.3 p.55-56 明示入场规则最不重要) |
| 趋势线(≥3 点手绘) | 排除 | 不可直接计算 |
| 整数关口心理 | 排除 | 不影响核心策略 |
| 短边单独作为策略 | 排除 | 仅作保险,作者明示不推荐单独使用 |

## 建议

- 回测结果应理解为「简化版 Clenow 核心策略(无变体)」的下限,不是原方法的真实表现。
- 对高风险行做敏感性测试:
  - 换 Donchian 窗口(50/100/150 日入场,25/50/75 日出场)
  - 换风险因子(7.5/10/15/30 bp)
  - 加仓数上限(模拟组合自适应)
  - 加 20% 单日波动减仓规则(模拟「极端事件人工干预」)
- 阶段 3 run-backtest 时,先以 15bp 为基线,4 档风险因子做参数扫描。
- **变体系统(反趋势 Ch.7、期限结构 Ch.8)未纳入此 spec**——它们的规则在 Clenow.trading-system.md §12-B 仅有概要,完整抽取需后续精读 p.227-339。