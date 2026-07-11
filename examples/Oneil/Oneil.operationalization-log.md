# O'Neil 操作化日志

策略来源:Oneil.trading-system.md
规格:Oneil.system-spec.yaml

回测的是「操作化版 O'Neil CAN SLIM 核心系统」,不是原方法。下表逐条记录翻译与保真度风险。**高风险行需审阅确认。**

## 操作化日志

| 书中原话 | 回测谓词 | 保真度风险 | 备注 |
|---|---|---|---|
| 当前季度 EPS ≥25% | `CurrQtrEPSGrowth >= 0.25` | 低 | p.24-25, 194 明示 |
| 年度 EPS 增长 ≥25%/3-5 年 | `AnnualEPSGrowth >= 0.25` | 低 | p.194 明示 |
| Sales 增长 ≥25% | (外部 earnings feed) | 低 | p.30, 194 |
| ROE ≥17% | `ROE >= 0.17` | 低 | p.194;大赢家常 30/40/50%+ |
| 日均成交 ≥1M | `AvgVol50d * price >= 1_000_000` | 低 | p.173 |
| 薄量禁重仓(<400k) | `AvgVol50d * price < 400_000 → exclude` | 低 | p.165 |
| FTD: 指数 +1.5% 且 volume > 前日 | `IndexClose_t/IndexClose_{t-1} - 1 >= 0.015 AND IndexVolume_t > IndexVolume_{t-1}` | 低 | p.21 |
| Distribution day: 指数 -0.2% 且 volume > 前日 | `IndexClose_t/IndexClose_{t-1} - 1 <= -0.002 AND IndexVolume_t > IndexVolume_{t-1}` | 低 | p.23 |
| 4-5 周 5-6 个 distribution day 转弱 | (滚动计数,4-5 周窗口内累计) | 低 | p.23 |
| 突破量 ≥40% above average | `Volume_t >= 1.4 * AvgVol50d_t` | 低 | p.25, 165, 192 |
| 50-day MA | `SMA(close, 50)` | 低 | p.46 |
| 10-week MA | `SMA(close, 50)` (10w ≈ 50 trading days) | 中 | p.46-47, 133;简化 |
| 200-day MA | `SMA(close, 200)` | 低 | p.90-91 |
| 10-day MA(强势股) | `SMA(close, 10)` | 低 | p.72-73 |
| 21-day MA | `SMA(close, 21)` | 低 | p.158 |
| 7-8% 硬止损 | `close < entry_price * 0.925` | 低 | p.45, 188 |
| 4-5% 提前止损(Brian) | `close < entry_price * 0.955` | 中 | p.49, 个案 |
| 5-6% 止损(Barbara, 波动市) | `close < entry_price * 0.945` | 中 | p.101, 个案 |
| 20-25% 常规锁利 | `close >= entry_price * 1.225` | 低 | p.46 |
| 8 周例外(突破后 2-3 周 +20% → ≥8 周) | `close >= entry_price * 1.20 within 15 trading days of breakout → hold >= 40 trading days` | 中 | p.46, 71, 181;时间窗口需精确 |
| 跌破 MA50d + 放量清仓 | `close < MA50d AND Volume > AvgVol50d` | 低 | p.46 |
| 跌破 MA10w + 重成交量 | `close < MA10w AND Volume > AvgVol50d * 1.5` | 中 | p.133;阈值选择 |
| 首次跌破 MA10d(强势股, 持仓 ≥8 周) | `close < MA10d after 40 holding days` | 中 | p.72-73 |
| 跌破 MA200d 清仓 | `close < MA200d` | 低 | p.90-91 |
| Jim 特殊再入场:跌破 MA50d 当日收回 → 同日买回 | (日内触发) | 中 | p.138-139 |
| Climax run / 顶部识别 | (规则难量化,排他性 + 多信号协同) | **高** | p.46-47, 105, 138 |
| Cup-with-handle / Double bottom / Flat base | (排除,人工看图) | **高** | p.25-26;不可计算 |
| Three-weeks-tight(3 周 close range <1%) | `(rolling_max(close,15) - rolling_min(close,15)) / rolling_mean(close,15) < 0.01` | 中 | p.26-27;代理 |
| High tight flags | (排除,人工看图) | **高** | p.110 |
| Buyable gap-up | (排除,需事件 + 基本面协同) | **高** | p.148-149 |
| A/D Rating(IBD 专有) | `UpDownVolRatio > 1.2` 代理 | **高** | p.147;真实 IBD 专有 |
| RS line 新高 | `RS_line == max(RS_line, 252)` | 低 | p.127, 142 |
| Up/Down Volume Ratio > 1.2 | `UpDownVolRatio > 1.2` | 低 | p.140 |
| 13F 持仓突变(Vinik Crocs 案例) | (外部数据,需季度持仓报告) | 中 | p.133 |
| 行业领导性 / Sector Leader | (行业排名/RS 阈值,无硬数) | **高** | p.42, 174, 181, 193 |
| 市场广度 ≥10-15 只 setup | (跨标的计数) | 低 | p.107 |
| Sleep test | (主观) | **高** | p.143 |
| Max 持仓 6(个人)/ 15(基金) | (常量) | 低 | p.91, 134 |
| 单标的 ≤30%(Kier) | (常量) | 低 | p.134 |
| FTD 后初始暴露 ≤20%(Ed) | (常量) | 低 | p.115-116 |
| 加仓必须浮盈 | (规则) | 低 | p.55 |
| 永不向下摊平 | (规则) | 低 | p.56 |
| 财报前不新进买入 | (事件检测) | 低 | p.101-102 |
| FTD 后 4 周内高质量新 leader 突破 | (FTD 后 20 交易日窗口) | 低 | p.56 |
| 100% 现金合法 | (regime = correction 时) | 低 | p.178 |
| Market Pulse 三态(confirmed / pressure / correction) | (基于 FTD + distribution day + MA21d 状态) | 低 | p.21 |
| Earl Semel "形态破损不下单" 风格 | (regime 切换时强制减仓) | 低 | p.114 |
| IBD 报纸 / eIBD / MarketSmith 数据依赖 | (回测需外部数据源) | -- | 必备,不建模 |

## 高风险行汇总(需审阅)

1. **Base pattern 检测**(cup-with-handle / double bottom / flat base / high tight flag):完全不可计算,必须人工看图或机器学习图像识别。**回测版会丢失 O'Neil 系统最核心的入场信号**。
2. **A/D Rating**(IBD 专有指标):用 UpDownVolRatio 代理,真实 IBD 算法不公开,**代理与原指标可能有显著差异**。
3. **Buyable gap-up / Climax top 检测**:都依赖事件 + 多信号协同,纯量价规则无法准确捕捉。
4. **行业领导性排名**:无硬阈值,需人工判断。回测版只能做到"按 ROE/RS 排序"。
5. **Sleep test**:主观降仓触发,无法编码,完全丢失。

## 排除项(原方法中不可直接计算的元素)

| 元素 | 处理 | 备注 |
|---|---|---|
| Cup-with-handle / Double bottom / Flat base / High tight flag | 排除 | 人工看图,不可计算 |
| Buyable gap-up(财报跳空) | 排除 | 事件型,需基本面协同 |
| A/D Rating(IBD 专有) | 代理 | UpDownVolRatio > 1.2 近似 |
| Industry Leader ranking | 排除 | 无硬阈值,需人工 |
| IBD / MarketSmith / Leaderboard 整套生态 | 排除 | 商业数据/工具,回测版不依赖 |
| Sleep test 主观降仓 | 排除 | 主观,无法编码 |
| 期权/指数 calls(Jeannie SPY calls 案例) | 排除 | 不是 CAN SLIM 主系统 |
| 做空规则(Leaderboard cut list) | 排除 | 不是 CAN SLIM 主系统 |

## 建议

- 回测结果应理解为「CAN SLIM 七要素 + 均线出场规则」的简化版下限,不是原系统的真实表现。
- 对高风险行做敏感性测试:
  - 三种 base pattern 识别方案的对比(纯量价 / 人工标注 / 机器学习)
  - A/D Rating 代理 vs UpDownVolRatio vs IBD 真值
  - 行业领导性用不同代理(RS 排名 / IBD 等权 / 人工)
- 个人交易者人工补充:
  - 每个候选必须附图表截图 + 周线观察笔记 + 买卖规则来源
  - IBD 订阅必要(回测版无法复制 IBD 生态)
- **变体形态**(high tight flag、buyable gap-up、swing pullback)是单独子策略,需分别抽取和回测。

## 缺口与可改进

- 「书中未明确」**base 形态精确测量**:cup 深度、handle 深度、pivot 计算、base 最短/最长天数未完整展开
- 「书中未明确」**FTD 完整日数规则**:从 correction low 后第几天才算有效 FTD 未给
- 「书中未明确」**行业相对强弱阈值**:行业排名前 X 或行业 RS 阈值
- 「书中未明确」**组合行业上限/相关性上限/回撤熔断**:用 Market Pulse + distribution days + cash + 持仓数管理,无硬参数
- 「书中未明确」**财报处理细则**:profit cushion 大小、财报前几天禁买
- 「书中未明确」**订单价格细则**:stop-limit 宽度、滑点容忍

详见 Oneil.trading-system.md §12。