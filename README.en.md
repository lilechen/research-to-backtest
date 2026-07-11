# research-to-backtest

> One document, one trading system.

English | [中文](README.md)

A Claude Code skill suite that turns the method in a trading book or paper PDF into a backtestable trading system, in stages.

```
PDF ──► human-readable strategy ──► structured spec ──► backtest
       extract-trading-system         specify-backtest      run-backtest
```

## Pipeline

| Stage | Skill | Input -> Output | Artifact |
|---|---|---|---|
| 1 | `extract-trading-system` ✅ | PDF -> human strategy | `<name>.交易系统.md` |
| 2 | `specify-backtest` ✅ | strategy.md -> backtestable spec | `<name>.系统规格.yaml` + `<name>.操作化日志.md` |
| 3 | `run-backtest` ⏳ | spec.yaml -> backtest | akquant code + results |

## Why two steps

Books describe methods with judgment words ("RS improving", "MA flattening", "breaks resistance"). Humans understand them; backtest engines don't. Backtesting a book's method directly actually backtests an *operationalization* of it, not the original. So:

- **Stage 1** keeps the judgment words — a human can trade it and knows which parts are judgment.
- **Stage 2** translates each judgment into a computable predicate, and an *operationalization log* records every "book wording -> predicate" mapping with a fidelity-risk grade, so you can review and tweak each.
- Non-computable elements (head-and-shoulders, trendlines, round-number psychology) are honestly excluded and logged, never force-coded.

## Install

Symlink or copy the directories under `skills/` into your Claude Code skill directory:

```bash
ln -s "$(pwd)/skills/extract-trading-system" <your-skill-dir>/extract-trading-system
ln -s "$(pwd)/skills/specify-backtest"        <your-skill-dir>/specify-backtest
```

Then invoke with `$extract-trading-system` / `$specify-backtest`.

## Usage

```bash
# Stage 1: extract a human-readable strategy from a PDF
$extract-trading-system
PDF: /path/to/book.pdf
type: book   # or paper

# Stage 2: convert to a backtestable spec
$specify-backtest
strategy: /path/to/<name>.交易系统.md
```

Stage 2 produces `<name>.系统规格.yaml` + `<name>.操作化日志.md`. Review the "high-risk" rows in the log; tweak the spec and re-run as needed.

## Example

`examples/` contains a full example generated from Stan Weinstein's *Secrets for Profiting in Bull and Bear Markets* (three files), for reference.

## Design notes

- Long PDFs (>80 pages) are read in parallel chunks then synthesized.
- Original numbers and wording are preserved verbatim; key criteria cite page numbers.
- "Explicit in the book" vs "inferred" are strictly distinguished.
- Gaps are recorded honestly, never fabricated.

## License

MIT — see [LICENSE](LICENSE).
