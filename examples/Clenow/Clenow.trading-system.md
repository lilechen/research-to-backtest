# Clenow 趋势跟踪交易系统(人可执行)

抽取自:Andreas F. Clenow《Following the Trend: Diversified Managed Futures Trading》(Second Edition, 2023)
资料类型:book
页码引用:PDF 页码(原书中印张页码与 PDF 页码因前 matter 错位约 +22,如书中 "p.45" ≈ PDF p.67;以下标 PDF 页码)

> 本文档为 `extract-trading-system` skill 的完整产物。三阶段来源:本会话主对话读 `/tmp/clenow_p1-57.txt`(PDF p.1-57,Ch.1-2 + Ch.3 前半)+ `/tmp/clenow_p58-113.txt`(PDF p.58-113,**核心:Ch.3 后半 + Ch.4 完整核心策略 + Ch.5 开头**)→ 合成核心规则;reader 2 历史笔记(p.114-226,Ch.5-6 绩效与逐年回顾);reader 3 部分笔记(p.227-339,Ch.7-14 变体)。

---

## 1. 系统概览与边际

**核心系统:跨资产类别、多空对称、加趋势过滤的 Donchian 突破趋势跟踪(CTA)**。

边际来自两条独立来源:**(a) 危机 alpha** ——股市受困时趋势跟踪通常在盈利(2008 +207.4% 单年 p.89;2002 +24.7% p.138;1998 LTCM +30% p.91;2020 Covid 股市跌约 1/3 而趋势模型涨 24.1% p.112);**(b) 少数极端盈利覆盖大量小亏** ——"few extreme gains make up for many small losses. If the trade you skip happens to be the one that finally pays off, your entire year may be ruined."(p.182)。日常 >90% 的天数收益在 ±4% 内,只有极少数双位数日(p.86)。

20 年(2002-2021)作者演示基金:US$10M → US$121M,**年化 13.3% 扣费后**(p.229, 233);交易总盈利 US$140M + 利息 US$8M,管理费 US$17.5M + 业绩费 US$20M(p.233)。**核心策略样本内(全期回测, ~1992-2021)** 年化 15.81%,最大回撤 -39.43%,Sharpe 0.70(p.73, Table 4.4);风险因子 15bp 下。

策略**方向无关**(direction agnostic),多空对称规则(setup/exit/sizing 均对称,p.74):"symmetrical rules for longs and shorts both in terms of entry and exit and in position sizing"。**短边作为波动率 dampener**,使长边能以更大仓位交易(p.116)。自 2001 以来归因(表 5.2, p.116):核心年化 18.24% / 最大回撤 -43.30% / 波动 27.52% / Sharpe 0.722;长边归因 20.37% / -32.58% / 21.02% / 0.988;短边归因 -2.13% / -54.27% / 15.90% / -0.056。**短边单独极差**,但作为"保险"在危机年大赚(2008 短边 +95.9%, p.177)。

**作者自承核心策略最大缺陷**(p.255):"the strategy treats every position completely independently and does not take into account how related they are to each other"——仓位层面做风控,非组合层面(静态等风险,无组合自适应)。

**核心 vs 大多数 CTA 基金的相似性**(p.69-70):多个 CTA 的 long-term correlation 都极高(BTOP 50 与 Millburn 0.80,与 Dunn 0.80,Table 4.3),**他们基本上都在做同一件事**——作者论证可以"用非常简单的规则解释数十亿美元趋势跟踪行业的大部分回报"。

**作者 meta-提醒**(p.208):"Once deployed, we are effectively passengers."——一旦按系统执行,你只是个乘客。趋势跟踪"已多次被宣布死亡,每次都为时过早"(p.214)。专业好交易员年化 15-20%(p.288-289);20% 长期年化"is a respectable target to shoot for, but that you will probably never reach it"(p.289)。

## 2. 交易宇宙

**五大板块,约 100 个合约**(Table 3.2, p.72;作者明确倾向农业):

- **Agriculture** (19):Cotton, Corn, Lumber, Live Cattle, Lean Hogs, Oats, Rough Rice, Soybeans, Sugar 11, Wheat Chicago, Soybean Oil, Cocoa, Milk Class III, Feeder Cattle, Coffee Arabica, Coffee Robusta, Wheat Kansas, Sugar White, Orange Juice, Canola, Soybean Meal。
- **Non-Agricultural (金属 + 能源)** (10):Gasoil, Light sweet crude, Heating oil, Brent Crude, Natural gas (HH), Gasoline, Gold, Copper, Palladium, Platinum, Silver。
- **Currencies** (10):AUD/USD, GBP/USD, EUR/USD, JPY/USD, NZD/USD, CHF/USD, CAD/USD, MXN/USD, Dollar Index(以及非 USD 交叉 EUR/CHF、EUR/GBP、EUR/JPY 等)。
- **Equities** (16):CAC 40, DAX, FTSE 100, HS China Enterprises, Hang Seng, Nasdaq 100, Nikkei 225, S&P 500, Euro Stoxx 50, Russell 2000, S&P 400, S&P/TSX 60, Dow Jones, Volatility Index, MSCI Taiwan, SPI 200, IBEX 35。
- **Rates** (16):Bund, Schatz, Long Gilt, Canadian Bankers' Acceptance, US 2Y, US 10Y, Eurodollar, Euroswiss, Euribor, Short sterling, Euro-BTP Long-Term, Euro-Bobl, 5-Year US T-Note, US T-Bond, 10-Year Govt of Canada Bond, 30 Day Federal Funds(以及 AU 10Y/3Y/90 Day、JP 10Y、CD 10Y/90 Day 等)。

合约规格详见 Table 2.2-2.6(p.33-43):每合约的 point value、报价币种、交易所。

**持仓数范围**(历年):22(2002)→ 54(2017),近期 35(2018)/ 46(2019)/ 47(2020)/ 48(2021)。**农业板块最有价值**——市场间相关性低,且对中小账户有"小账户优势"(p.33-34, 51-52)。

**最低资产基准**:US$1M(偏激进);US$1-5M 仍需缩减宇宙(p.266-267)。小账户考虑 mini contracts,但利率板块缺 mini、农业 mini 流动性差。

**账户币种**:USD / CHF / EUR / GBP / HKD / JPY / CAD / AUD / BRL / MXN / ZAR 等(凡涉及合约报价币种)。

**明确不适用**:
- **ETF 不行**:现金工具、杠杆贵且受限,无法建 250% 仓位;商品/农业 ETF 稀少且多为打包,破坏分散(p.286)。
- **股票不行**:同质化太高、无分散;"No, trend following does not work on stocks"(p.285)。股票上做的是动量模型,非趋势跟踪(p.285)。
- **单个合约或单一资产类不行**:作者明确"at best plain silly and at worst suicidal"(p.49)——单市场策略"is for those people with either extreme skill or for those who simply have a death wish"。
- **股票指数以外的单股期货**:作者明确不感兴趣(p.39)。

## 3. 时间框架与执行节奏

- **日线数据,end-of-day 取值**(p.51):作者只用 daily data,不需盘中数据。
- **执行日 = 信号次日**(p.61):"if a signal is generated on a Tuesday, the strategy simulation assumes that we buy on Wednesday morning and that we get a generally bad entry price"——防止数据偷窥(data snooping)。
- **假设各交易所开盘时下市价单拿开盘价**(p.268)。
- **全球市场开盘**跨日本、香港、新加坡、欧洲、北美(p.269)。
- **持仓周期数月级**:典型例 EUR 2002 持仓数月(p.137);Schatz 2008 中→2009-02(p.176);Sugar 2010 7-10 月(p.188)。
- **管理费每日计提、按季支付;业绩费按年支付、high-water mark**(p.129-130, 138, 201, 206)。
- **月度再平衡**(高效前沿分析,p.126)。
- **复盘节奏**:不需高频盯盘,日终检查信号即可。开仓首日复制回测当前状态、立即进入全部仓位(p.132)。

## 4. 建仓信号

> **核心策略**(Ch.4 "Core Strategy", p.74)由**两个组件组合**:趋势过滤(MA cross)+ 突破入场(Donchian)。

### 4.1 趋势过滤(Trend Filter)

- **用 EMA 50 与 EMA 100 的相对位置判断市场 regime**(p.71-74):
  - **看多(bullish)**:EMA 50 > EMA 100
  - **看空(bearish)**:EMA 50 < EMA 100
- 这是**过滤器**,不直接产生入场信号,只决定**允许的入场方向**。
- 作者明示初始两个简单策略**不用过滤**(p.57),"to keep the models as simple as possible for the first demonstration"——核心策略加过滤是为了**避免在横盘市反复止损 + 在强趋势中逆势开仓**(p.71-72, 4.6/4.7 图)。
- **执行**:EMA 50 / 100 都用**指数移动平均**(p.60, 第二版用 EMA,第一版用 SMA)。

### 4.2 入场触发(Donchian Breakout)

入场**仅在趋势过滤允许的方向**(p.74):

- **做多入场**:今日 close ≥ 过去 **100 个交易日**的**最高收盘价** AND 当前趋势为 bullish → 次日开盘买入。
- **做空入场**:今日 close ≤ 过去 **100 个交易日**的**最低收盘价** AND 当前趋势为 bearish → 次日开盘卖空。
- "100-day breakout entry" — 作者明示比第一版的 50-day 翻倍(p.61)。
- **执行日 = 信号次日**(p.62)。

### 4.3 入场检查清单(实际下单前)

每只合约、每天日终检查:

1. 收盘价计算完成(避免盘中假信号)。
2. 计算 50-day EMA 与 100-day EMA。
3. 若 EMA 50 > EMA 100:允许做多,不允许做空;若 EMA 50 < EMA 100:允许做空,不允许做多。
4. 比较今日 close 与过去 100 天 high/low 极值。
5. 若 close ≥ 100-day high 且趋势 bullish → 生成多头入场信号(明日开盘买)。
6. 若 close ≤ 100-day low 且趋势 bearish → 生成空头入场信号(明日开盘卖空)。
7. 按 §6 公式计算合约数,取整向下(rounded down,保守)。
8. 检查账户保证金,确保有足够 margin + maintenance。

> **作者明示**:"the buy-and-sell rules are far subordinate in importance to position sizing and diversification... For a trend-following strategy, it is quite possible to have flawed entry and exit rules in combination with good diversification and risk rules and still be profitable, but the other way around is a recipe for disaster."(p.55-56)。**入场规则的精确性**远不如 sizing + 分散重要。

### 4.4 两个基础策略(参考,非核心)

- **策略 1:MA Cross**(p.60-61):EMA 50 > EMA 100 → 多;反之 → 空。**永远在市场**(always in market),一反转就翻向。回测表现:18.18% 年化 / -64.67% DD / Sharpe 0.73(全期)。
- **策略 2:Donchian Breakout**(p.61-62):100-day high 入场 / 100-day low 入场(反向);50-day low 平多 / 50-day high 平空。**不在市场时也可**(不是 always in)。回测表现:17.90% / -47.19% / 0.77(全期)。
- 这两个策略**没有趋势过滤**,会产生大量假信号。**核心策略 = 策略 2(突破) + 策略 1 作过滤**(p.73-74)。

## 5. 出场信号

出场由**两个独立触发**任一满足即出场(p.74):

### 5.1 反向 Donchian 触发(价格反转)

- **平多头**:今日 close ≤ 过去 **50 个交易日**的最低收盘价。
- **平空头**:今日 close ≥ 过去 **50 个交易日**的**最高收盘价**。
- 即"50-day opposite breakout exit"——比入场窗口(100-day)短一半,更快响应反转。

### 5.2 趋势过滤翻转

- **平多头**:EMA 50 < EMA 100(趋势转 bearish)。
- **平空头**:EMA 50 > EMA 100(趋势转 bullish)。
- 即使价格未触发反向 Donchian,趋势翻转也强制平仓。

### 5.3 出场检查清单

每日对每持仓:

1. 计算 50-day EMA 与 100-day EMA,判断趋势方向。
2. 比较今日 close 与 50-day high/low 极值。
3. 若(持仓为多 AND close ≤ 50-day low)OR (EMA 50 < EMA 100)→ 出多信号(明日开盘平)。
4. 若(持仓为空 AND close ≥ 50-day high)OR (EMA 50 > EMA 100)→ 平空信号(明日开盘平)。

### 5.4 时间止损 / 移动止损

- **明确无时间止损**(作者未在核心策略中设时间止损)。
- **明确无移动止损 / trailing stop**——作者只用了反向 Donchian + 趋势翻转两种出场,**没有传统的跟踪止损**。
- 这是**重要缺口**(详见 §12):经典 CTA 常用的 ATR 倍数止损、time-based stop 在 Clenow 核心策略中都**不存在**。出场完全靠"价格或趋势自己反转"。

### 5.5 缺口风险(止损被单日大缺口穿透)

- 日频趋势模型的固有风险(heating oil 2011, p.194):"the price powered far through our theoretical stop, and we gave back far more money than intended. This is always a risk with trend models operating on daily data"。
- 作者未给具体应对(无显式 gap protection),靠"价格实际触发反向 Donchian"自然处理。

## 6. 仓位 sizing

### 6.1 核心公式(Ch.3 p.52, Ch.4 核心策略 p.74)

```
Contracts = (0.0015 × Equity) / (ATR20 × PointValue)
```

其中:
- **0.0015 = 15 basis points**(核心策略目标日波动对组合的理论冲击)
- **Equity** = 账户总值,或分配给该策略的资金
- **ATR20** = **20 日 ATR**(Average True Range over 20 days,**指数移动平均平滑**——作者 Ch.3 p.52 明示"I use an exponential moving average to arrive at the normal trading range")
- **PointValue** = 合约点值(每变动 1 点的美元价值)
- 取整向下(round down),保守

### 6.2 风控档位(Ch.4 Table 4.5, p.77)

作者明确测试了 4 档风控(同一策略不同 risk factor):

| 风险因子 | 年化 | 最大回撤 | 波动率 | Sharpe |
|---|---|---|---|---|
| **7.5 bp** | 8.88% | -22.23% | 13.08% | 0.72 |
| **10 bp** | 11.63% | -28.69% | 17.41% | 0.72 |
| **15 bp(核心)** | 15.81% | -39.43% | 25.90% | 0.70 |
| **30 bp** | 25.94% | -64.66% | 49.57% | 0.71 |

**关键观察**:4 档 Sharpe 几乎一致(~0.71-0.72),但**回撤与收益线性放大**。**作者推荐 15bp**(核心演示值);个人交易者按风险承受力选择(p.77)。30bp 在 2008 后回撤 -64.66%,**作者明示"likely to be achieved in real life"风险极高,实际可能 -75% 到 -80%**(p.77)。

**重要算术提醒**(p.77):70% 回撤后,需 **+234%** 才回到起点。**这不是翻倍,是三倍**。

### 6.3 其他 sizing 方法(参考,非作者核心)

- **margin to equity**(p.53):0.5% margin/equity per position。某些大型基金使用,但作者本人回避("this method has always made me wary")——交易所 margin 设定主观且会突变。
- **standard deviation**(p.53):用日收益率(不是价格)的标准差替代 ATR。需要先验证是 return-based std 不是 price-based std。

### 6.4 波动率恒定假设的缺陷

作者自承(p.52, p.132):"volatility is not stationary and can change dramatically over the course of a position's lifetime"。position size **在入场时锁定,持仓期间不调整**——这是"flawed assumption"。可作为改进点。

## 7. 组合层面风险

### 7.1 持仓数

- **范围**:22(2002)→ 54(2017)。近期 35(2018)/ 46(2019)/ 47(2020)/ 48(2021)。
- 持仓数随**可用趋势**自动变化:无趋势时很多合约被过滤/出场,有趋势时多个合约同时持仓。

### 7.2 集中押注风险(作者明示)

- **趋势齐发时形成集中押注**(p.159):"when the trends are really on, these kinds of trading models tend to build concentrated exposure to a single or a few themes"。例:2006 年初"massive 29% risk exposure"长股(p.159);2017 年 54 仓"far more than normal... a very risky portfolio"(p.222)。
- 2008 年 9 月后**日组合波动可达 20%+ 单日**(p.175):"you might have seen daily moves in the portfolio of 20% or more. In a single day!"。

### 7.3 高相关性风险

- 危机期不同指数相关性趋于 1,造成"painful losses in a very short time"(p.119-120)。
- **作者明示无组合层面自适应风控**(p.222, 255):"Under the current rules, we don't adapt risk on a portfolio level, but rather keep each position risk static"——54 仓位时组合 risk-on 等于 8.1%(54 × 0.15%)。

### 7.4 回撤熔断

- 核心策略最大回撤 **-39.43%**(15bp 风控, Table 4.4)。
- **作者未设显式回撤熔断 / 自动减仓规则**——这是缺口(详见 §12)。
- 行业老话:"no such thing as a third bad year for a hedge fund"(p.207)——连亏两年基本完蛋。

### 7.5 现金管理(自由政府钱)

- **核心策略典型 margin-to-equity 比率 10-20%**(p.79):大部分时间是闲置现金。
- **建议把闲置现金 65% 投在政府债券**(p.81, Table 4.6),US$10M 基金可放 US$6M 在国债。
- **强烈建议只用 G7 政府债**(p.80),不用低信用发行人。**利率收益是"free government money"**,是 managed futures 长期收益的重要组成(尤其 1980s-1990s)。
- **注意**:此收益**逐年下降**(Table 4.6):2006 年 +3.84%,2008 年 +1.87%,2020 年 +0.24%,2021 年 +0.25%——低利率环境下基本消失。
- **作者提醒**(p.81):"Odds are that interests will stay low for some time"——未来不会再有 1980s 的"easy money"环境。

### 7.6 高效前沿配置(Ch.5, Table 5.5)

| 期货配置 % | Return | Vol | Sharpe |
|---|---|---|---|
| 0% | 10.04 | 18.22 | 0.55 |
| **50%** | 13.10 | 13.66 | **0.96** |
| **60%** | 13.72 | 14.84 | **0.92** |
| 100% | 16.16 | 23.71 | 0.68 |

**Sharpe 峰值在 50-60% 区间**。**低于 30-40% 期货配置无意义**(p.126-127)——这是把 trend futures 与股票组合时的最优权重。

### 7.7 极端事件人工干预(非系统规则)

作者**个人主张**(p.175):"I would advocate for overriding the model and greatly reducing risk if something like this ever happens again. Better still, have a plan in place for unthinkable events."——但**未系统化**,未给具体阈值。

## 8. 过滤器与不交易条件

**核心原则:无过滤器,必须接每一个交易信号**(p.182, 198)。

- "it's imperative that you take every single trade"——跳过信号会毁掉整年。"There just isn't any way of knowing in advance which trades will pay off and which will not."
- 趋势不发(无趋势)市场造成反复小亏(Live Cattle 2009 p.182),但模型仍持续接每一个信号。
- **趋势过滤**(EMA 50/100)是**方向过滤器**(决定可不可以做多/做空),**不是信号过滤器**——不能因为"信号不靠谱"就跳过。

**作者明示**(p.49, 51-52):**单市场或单资产类不行**,**至少 100 个合约 + 5 板块分散**。

**股票 / ETF 不适用**(详见 §2)。

## 9. 执行机制

### 9.1 订单类型

- **开盘市价单**(p.61, 268):信号次日开盘按市价买入/卖出。**不试图优化入场价**——"a generally bad entry price with the slippage and commission assumptions"。
- **无 buy-stop / sell-stop 预挂单**:作者**显式不用** GTC stop orders(对比 Weinstein 的做法)。**完全 EOD 信号 + 次日开盘执行**。

### 9.2 佣金与滑点(回测假设,p.55)

- **佣金**:US$1 / 合约
- **交易所费**:US$1.5 / 合约
- **滑点**:基于成交量的滑点算法(volume-based),模拟实际成交——**总是假设差执行**:"we always get poor executions, because life tends to have a mean sense of humour"
- 永远**高估成本**:"you should always try to err on the side of caution and rather overestimate your costs. It's much nicer to get positive surprises in reality."

### 9.3 费率结构(Ch.4, p.83-84)

- **管理费 1.5%**(按季付、每日计提)
- **业绩费 15%**(按年付、high-water mark——回撤后需先涨回旧 HWM 才再计业绩费)
- 这些费率**显著降低长期净收益**(Figure 4.12)。**核心策略扣费后年化从 ~16% 降至 ~13.3%**(p.229, 233)。
- **作者建议**:新管理人**只用管理费预算**("survive on just the management fees"),不能依赖业绩费——单年不顺就完蛋。

### 9.4 多币种处理

- 合约 P&L 在合约币种结算,**结算日才换成基础币种**(p.22-23):"the only exchange rate that has any bearing on the final settlement of the position is that of the closing day"。
- **不要对名义金额做货币对冲**——只对当前 P&L 做动态对冲(很难),通常**接受货币敞口**。
- 银行账户需保留多币种现金以避免透支费用(p.24)。

### 9.5 数据要求(Ch.2, 重要但易被忽视)

- **必须用调整过的连续合约**(back-adjusted continuous contracts,p.27-30),不是简单把一个合约接到下一个——否则 basis gap 会污染回测。
- **优先用单个合约的真实历史**做回测(p.31)——只有当算力不够时才用 pre-calculated continuations。
- **on-the-fly 连续合约计算**(p.31)最接近实盘。
- 不要用 c1 codes from Reuters 的默认未调整序列。
- 作者推荐:**识别最活跃合约(open interest)→ rollover 时把旧合约 close 链到新合约 close → 整段时间序列回溯调整**。

### 9.6 数据 snooping 防护

- 信号次日执行(p.61),不是当日——避免"用未来信息"做回测。
- 回测平台应能阻止同日信号-成交。

## 10. 心理与纪律

- **必须接每一个交易信号**(p.182, 198)。
- **不要做线性外推的"无用算术"**(p.142, 149):看到 +30% 就推算全年。
- 不要用"playing with the bank's money"等赌博用语——从高点回撤就是真实亏损(p.162):"You don't pick arbitrary points to calculate profits and losses."
- 投资者总会拿你和股市比(p.130):"human nature to want to gain when everyone else is gaining"。
- 行业老话:"no such thing as a third bad year for a hedge fund"(p.207)。
- **起步时点的运气是决定性因素**(p.135, 198):若 2012 年开局第一年就 -20%,"can be a career killer"。
- **长期曲线掩盖短期痛苦体验**(p.146):"long-term charts do for you; obscure the shorter-term and the real-life experience"。
- 这行会让你变成犬儒和悲观者(p.161)。
- 逆境中"trust in the plan, have faith"(p.165)。
- **Mark Twain 名言**(p.97):"lies, damned lies, and backtests"——永远不要相信别人(包括作者)没自己复现的回测。
- **John Maynard Keynes 名言**(p.98):"In the long run, we are all dead"——别只看长期曲线。
- **作者对市场的悲观判断**(p.103-105):1980s 5% 自由利率 + 趋势跟踪 = 几乎免费的午餐;这种环境不会再回来。

## 11. 适用行情与失效场景

**适用**:
- 持续趋势市(任意方向)。
- **危机 alpha**:2008 +207.4% 单年(p.89);2002 +24.7%(p.138);1990 熊市 +40%(p.91);1998 LTCM +30%(p.91);2000-2003 dot-com +200% 累计(p.92);2020 Covid +24.1%(p.112)。

**失效 / 困难**:
- 震荡无趋势(Live Cattle 2009 p.182):反复入场反复亏。
- 带剧烈反向尖刺的"趋势"也赚不到钱(coffee 2015 p.216):"this particular bear market trend was not in any way profitable"。
- 板块轮动急转(2003 年 3 月从 +30% 跌到 -5%, p.143)。
- 缺口穿透止损(2011 heating oil p.194)。
- 头部假突破(2004 Gilt p.151;2012 US 10Y p.200)。
- 股市单边牛而其他板块全亏(2013 +2.2%、2017 +3.7% 而 MSCI +25%, p.206, 224-225)。
- 全板块慢失血(2012 -20.1%, p.200-201)。
- **股指因 HFT 与全球化相关性升高**,比十几年前更难做(p.119)。
- **短边多数年份亏钱**,但危机年大赚(2008 短边 +95.9%, p.177)。
- **10 年横盘**(作者 Ch.4 实测, p.97):"ten years of almost flat performance"——长期持有需要信仰。
- **核心策略样本内回测 2015-2019 表现平淡**(p.88),2020 才恢复。

## 12. 缺口与补全

### A. 已识别的明确缺口(原方法不留)

- **时间止损 / 持仓最长期限**:**不存在**。作者只用反向 Donchian + 趋势翻转,无时间维度出场。**推断**:个人交易者可加"持仓 N 周无趋势进展 → 减半"作为纪律补丁,非原方法。
- **移动止损 / trailing stop**:**不存在**。出场完全靠"价格或趋势自己反转"。**推断**:不补——加移动止损会与核心规则冲突。
- **gap protection / 盘中穿透风险**:**无显式应对**。作者明示日频模型的固有风险(heating oil 2011),靠反向 Donchian 自然处理(但可能给更多损失)。
- **图形形态过滤(头肩底/双底/趋势线等)**:**完全不用**。所有"形态"都翻译成 Donchian 突破 + EMA 过滤。
- **个股过滤器**(RS 为正、流通市值、最低价等):**完全不用**。**推断**:Clenow 不屑于个股层面的过滤——宇宙层面用流动性即可。
- **相关性上限 / 板块集中度上限**:**没有**。作者靠分散到 100 个合约解决,不强加相关性约束。
- **回撤熔断 / 自动减仓**:**没有系统化**。作者只个人主张极端事件人工干预(p.175)。
- **波动率自适应的 sizing 改进**:作者明示"sizing uses ATR20 但假设 vol 恒定"的缺陷(p.52, 132)。Ch.9 提到 Volatility-Based Stop Loss(p.262)作为改进方向,但核心策略未包含。

### B. 变体系统(Ch.7-14)

作者演示了多个变体,但**核心策略 = Ch.4 主策略**,变体仅作扩展:

1. **反趋势模型(Ch.7, p.235-242)**:均值回归型,短期波动比趋势跟踪更剧烈,"what is important with this kind of model is the entry"(p.238),交易"less liquid contracts"。**具体规则(reader 3 部分覆盖)**:
   - 40/80 EMA + 3 ATR 回撤 + 20 日时间止损(p.261,需 reader 3 后续确认)。
2. **期限结构 / 曲线交易(Ch.8, p.243-252)**:基于 contango/backwardation 偏置做方向性投注。
   - "contango 内含看空偏置(合约逐日向现货收敛下行);backwardation 内含看多偏置"(p.246-247)。
   - 实际操作:每周一次,contango ≥ 15% 做空 / backwardation ≥ 7.5% 做多,200% 总敞口(p.271-272,需 reader 3 后续确认)。
   - **实际只在商品板块最有意义**(p.245)。
3. **三策略等权组合**(p.283,需 reader 3 后续确认):核心 + 反趋势 + 期限结构各 33/33/34%,月度再平衡,组合 Sharpe 1.29。
4. **改进(Ch.9)**:
   - 波动率止损(Volatility-Based Stop Loss, p.262)——替换固定 Donchian 出场。
   - 相关性矩阵用于 sizing(p.255)。
   - 优化(optimisation)的危险(p.257)——作者明确反对过度优化。
5. **实务(Ch.10)**:所需资本、live trading、执行、现金管理、回撤期监控。
6. **建模(Ch.11)**:Python + Zipline、backtesting 危险(p.282)。
7. **股票上的趋势跟踪(Ch.12)**:不适用(p.283-286)。
8. **以交易为生(Ch.13)**:好交易员赚多少(p.287-289),找交易工作、自营、OPM。
9. **最终警告(Ch.14)**:基金 diminishing returns、初始风控、go live。

### C. 明确缺口但有合理推断

- **个人交易者应排除机构专属规则**:管理费/业绩费/高水位(mgmt 1.5% / perf 15%)是机构业务模型,个人自营可省。
- **个人应保留更高现金缓冲**:作者机构级 10-20% margin-to-equity 对个人风险过高,建议留 30-50% 现金 + 国债缓冲。
- **缺数据时的回退参数**:
  - ATR 周期未给具体值时,用 20-day(作者明示, p.74)。
  - EMA 周期未给时,用 50 / 100(作者明示, p.60-61)。
  - Donchian 窗口未给时,入场 100-day / 出场 50-day(作者明示, p.61-62)。
  - Risk factor 未给时,起步 15bp(作者核心值, p.74)。

### D. 已知缺陷与边界

- **静态等风险**(无组合自适应,p.222)。
- **单边市场下表现差**(单边牛股市 + 其他全亏,2013/2017)。
- **回撤周期可能很长**(2015-2019 横盘 5 年,p.88)。
- **短边单看极差**(复合 -2.13%,回撤过半,作者明示作为保险有价值,p.116)。
- **作者明示 backtest vs live 的关键差异**:"Our strategy is a back-test and thereby a theoretical return of strategy created after the fact. These rules are created to explain trend following as a phenomenon and to teach the principles behind it."(p.97-98)——**回测结果系统性高估实盘表现**。

## 13. 验证路径

### 13.1 完整年度模拟(US$10M 起步、无资金进出、含佣金滑点、扣费)

核心策略(15bp 风控,扣费)逐年收益(来源:reader 2 历史笔记 + 本会话 Ch.4 Table 4.2):

| 年 | 交易结果 % | 期末 NAV (US$) | 页 |
|---|---|---|---|
| 2002 | +24.70 | 12,095,344 | p.138 |
| 2003 | +22.50 | 14,343,723 | p.145 |
| 2004 | +12.60 | 15,877,218 | p.152 |
| 2005 | +6.90 | 16,914,224 | p.158 |
| 2006 | +24.90 | 20,784,702 | p.164 |
| 2007 | +3.10 | 21,550,738 | p.170 |
| 2008 | +136.80 | 46,313,195 | p.178 |
| 2009 | +25.70 | 55,977,147 | p.183 |
| 2010 | +30.50 | 69,795,629 | p.189 |
| 2011 | +2.70 | 70,666,752 | p.195 |
| 2012 | -20.10 | 55,726,577 | p.201 |
| 2013 | +2.20 | 56,232,130 | p.206 |
| 2014 | +52.60 | 82,632,021 | p.212 |
| 2015 | -5.90 | 76,954,416 | p.217 |
| 2016 | +11.00 | 84,305,179 | p.222 |
| 2017 | +3.7 (gain) | — | p.224 |

20 年合计(2002-2021):US$10M → US$121M,**年化 13.3% 扣费后**(p.229, 233)。

### 13.2 关键单笔案例(带数字、标的、页码)

- 欧元多头 2002:1.02 → 1.16 (p.137)。
- Euro Stoxx 空头 2003:3 月见顶回落、V 型反弹止损、后转多(p.145)。
- Long Gilt 2004:3 月高点建多、假突破、双位数亏损(p.151)。
- Nikkei 多头 2005 下半年(p.157)。
- Nasdaq V 型 2006:5 月跌 → 短、7 月 V 反 → 长(p.163)。
- Soybean 多头 2007 年 10 月 → 2008 年 2 月(p.169)。
- German Schatz 多头 2008 年中 → 次年 2 月(p.176)。
- Euro Stoxx 50 空头 2008:8-10 月主盈利、之后高波动难赚(p.177)。
- Live Cattle 2009:无趋势反复止损(p.182)。
- Sugar 多头 2010:7 月 → 10 月,牛市后 abrupt end(p.188)。
- Heating oil 缺口 2011:单日大动穿透理论止损(p.194)。
- US 10Y Treasury 2012:看空 head-fake 后转多(p.200)。
- S&P 500 多头 2013:全年单边(p.205)。
- Short Crude Oil 2014:6 月起持续下跌(p.211)。
- Coffee 2015:有下跌趋势但反复尖刺,全亏(p.216)。
- Arabica coffee 多头 2016:震荡持至 11 月趋势结束(p.219)。
- Hang Seng 多头 2017:全年单边牛市(p.226)。

### 13.3 2008 板块归因(表 6.27, p.177)

长边 +43.0、短边 +95.9、合计 +136.8;
长非农 +15.1、长利率 +23.0;
短股票 +35.6、短非农 +24.7。

### 13.4 30 年板块长边归因(表 5.3, p.119, 费前 %)

| 板块 | 长边 % | 备注 |
|---|---|---|
| Currencies | -0.18 | 长期横盘 |
| Agriculture | 6.43 | 最稳定 |
| Non-Agri | -0.41 | 长期横盘 |
| Equities | 5.44 | |
| Rates | 9.10 | **主力** |
| **合计** | **20.37** | |
| 短边合计 | -2.13 | |

### 13.5 高效前沿(表 5.5, p.127)

| 期货配置 % | Return | Vol | Sharpe |
|---|---|---|---|
| 0% | 10.04 | 18.22 | 0.55 |
| 50% | 13.10 | 13.66 | **0.96** |
| 60% | 13.72 | 14.84 | 0.92 |
| 100% | 16.16 | 23.71 | 0.68 |

**Sharpe 峰值 50-60% 期货配置**;低于 30-40% 无意义(p.126-127)。

### 13.6 组合快照(表 5.4, p.122-123, 2009-05-21)

全持仓 USD 暴露 / %,其中 Euribor 26,429,000(264.3%)、30 Day Federal Funds 49,496,555(495.0%)、Eurodollar 24,092,375(240.9%)。

### 13.7 纸面验证建议

按 §4-§6 规则手算以下案例,对照书中后续走势:

1. **Soybean 2007-10 多头入场**(p.169):当时 close 是否 ≥ 100-day high? EMA 50 是否 > EMA 100? ATR20 × point value 计算合约数?持仓至 2008-02——期间是否触发 50-day low 出场?趋势是否翻空?
2. **Heating oil 2011 缺口**(p.194):开盘跳空情况下,反向 Donchian 是否同日触发?出场价 vs 信号价的偏差?
3. **Long Gilt 2004 假突破**(p.151):入场后多久触发反向 Donchian 或趋势翻转?最大浮亏多少?
4. **核心策略 2008 月度收益**(Table 5.1, p.89):逐月对比核心策略月度 +27.8/+30.2/-8.5/-1.7/+6.0/+1.2/-12.2/-0.7/+26.6/+47.2/+11.5/+5.7 = +207.4%——验证危机 alpha 的实际幅度。

### 13.8 进入 `specify-backtest` 前需特别关注

- **完整可计算**:Donchian 100/50 窗口 + EMA 50/100 + ATR20 sizing 公式 → 可直接转 YAML 谓词。
- **缺失元素**:无时间止损、无移动止损、无回撤熔断 → 标记为缺口,可不编码或按推断加补丁。
- **现金管理**:65% 国债缓冲是"软"规则,可入假设。
- **费率结构**:1.5% mgmt + 15% perf + HWM + $1 佣金 + $1.5 交易所费 + volume slippage → 完整入 assumptions。
- **数据要求**:必须用 adjusted continuations 或单合约历史 → 入 assumptions。
- **风险档位**:7.5/10/15/30bp 4 档可作为敏感性测试维度。
- **变体系统(反趋势、期限结构)**目前仅 §12 列出,需进一步精读 Ch.7-8 才能完整抽取。

---

## 附录:抽取过程

- **本会话主对话读取的文件**:
  - `/tmp/clenow_p1-57.txt`(PDF p.1-57,Ch.1-2 + Ch.3 前半,1995 行)
  - `/tmp/clenow_p58-113.txt`(PDF p.58-113,**核心:Ch.3 后半 + Ch.4 完整 + Ch.5 开头**,2110 行)
- **会话历史已有**(来自之前 reader agent 的 task-notification):
  - Reader 2:PDF p.114-226 完整 13 节笔记(Ch.5-6 绩效归因 + 2002-2017 逐年回顾)
  - Reader 3:PDF p.227-339 部分笔记(sections 1-2 + section 3 前半;Ch.7-14 变体部分)
- **未读**:PDF p.227-339 完整文本(变体系统规则未完整抽取,见 §12-B)
- **风格对齐**:参考 `research-to-backtest/examples/Weinstein/Weinstein.trading-system.md` 的密度、内联页码 (p.X)、「推断」/「书中未明确」/「排除」标记、案例带数字。
- **替代的前 PARTIAL 版本**:曾因 quota 中断生成,核心规则标"待补";本次完整版已覆盖所有 ⏳ 缺口,版本应替换使用。