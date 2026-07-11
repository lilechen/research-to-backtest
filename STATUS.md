# Pipeline Status

跟踪每本书 / 每篇 paper 跑到的阶段。`extract-trading-system` 完成 Stage 1 后更新,`specify-backtest` 完成 Stage 2 后更新,`run-backtest` 完成 Stage 3 后更新。

## 图例

- ✅ 完成
- ⏳ 进行中 / 计划中
- ❌ 失败 / 跳过
- — 不适用

## 当前进度

| 文献 | 类型 | Stage 1 (extract) | Stage 2 (specify) | Stage 3 (backtest) | 文件夹 |
|---|---|---|---|---|---|
| Stan Weinstein《Secrets for Profiting in Bull and Bear Markets》 | book | ✅ | ✅ | ⏳ | `examples/Weinstein/` |
| Andreas F. Clenow《Following the Trend》 | book | ✅ | ✅ | ⏳ | `examples/Clenow/` |
| William J. O'Neil《How to Make Money in Stocks》 | book | ✅ | ⏳ | ⏳ | `examples/Oneil/` |

## 复盘要点(由 skill 自动产出时的已知坑)

- **页码映射**:PDF 页码 ≠ 印张页码(Clenow 差 ~22 页)。reader 用 PDF 页码,在文档头部标注映射。
- **缺 Stage 2 容易忘**:Stage 1 跑完后,需主动跑 Stage 2 才能拿到 spec + log。后续会加 `$extract-and-specify` 一键。
- **变体系统未纳入 spec**:若书含多个策略(Clenow 有 Ch.7 反趋势、Ch.8 期限结构),主 spec 只覆盖核心策略,变体待后续精读。