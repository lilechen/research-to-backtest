<div align="center">

# research-to-backtest

**Turn a trading book or paper PDF into a backtestable trading system.**

A Claude Code skill suite · `PDF → human strategy → structured spec → backtest`

<p>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/lilechen/research-to-backtest?style=flat-square&label=License" alt="License: MIT"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/stargazers"><img src="https://img.shields.io/github/stars/lilechen/research-to-backtest?style=flat-square" alt="Stars"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/issues"><img src="https://img.shields.io/github/issues/lilechen/research-to-backtest?style=flat-square" alt="Issues"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/commits/main"><img src="https://img.shields.io/github/last-commit/lilechen/research-to-backtest?style=flat-square" alt="Last Commit"/></a>
  <a href="https://github.com/lilechen/research-to-backtest/tree/main/skills"><img src="https://img.shields.io/badge/Claude%20Code-Skills-blueviolet?style=flat-square" alt="Claude Code Skills"/></a>
</p>

[中文](README.md) · [Examples](#examples) · [Install](#quick-start) · [Contributing](#contributing)

</div>

---

## Table of Contents

- [The Problem](#the-problem)
- [What It Does](#what-it-does)
- [Pipeline](#pipeline)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Design Principles](#design-principles)
- [How It Works](#how-it-works)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## The Problem

Trading books describe methods with **judgment words** — "RS improving", "MA flattening", "breaks resistance", "head-and-shoulders". Humans understand them; backtest engines don't.

If you backtest a book's method directly, you're actually backtesting an *operationalization* of it, not the original. Most people skip that step and get results that look reasonable but don't match what they'd actually do when sitting in front of the screen.

**The problem isn't lack of backtest power — it's the missing intermediate artifact that separates "human-readable judgment" from "machine-computable predicate", and honestly records every translation in between.**

## What It Does

A three-stage Claude Code skill suite that turns a book or paper PDF into something you can both **trade by hand** and **backtest mechanically**:

| Stage | What | Artifact |
|---|---|---|
| **1. Extract** | Distill the trading system into a human-readable document (judgment words preserved, every rule cited to a page) | `<name>.trading-system.md` |
| **2. Specify** | Translate to framework-agnostic YAML + **operationalization log** that records every "book wording → predicate" mapping with fidelity-risk grade | `<name>.system-spec.yaml` + `<name>.operationalization-log.md` |
| **3. Run** | Generate backtest code from the YAML (target: [akquant](https://github.com/lilechen/akquant), a Rust-Python quant framework) | akquant code + backtest results |

Non-computable elements (head-and-shoulders, trendlines, round-number psychology) are honestly **excluded and logged**, never force-coded.

## Pipeline

```
   ┌─────────┐    ┌──────────────────┐    ┌─────────────────────┐    ┌──────────┐
   │   PDF   │    │  Human Strategy   │    │  Framework-Agnostic │    │  Backtest│
   │  book / │──▶ │  (judgment kept) │──▶ │  YAML Spec           │──▶ │  akquant │
   │  paper  │    │  13-section doc   │    │  + Operational Log  │    │  code    │
   └─────────┘    └──────────────────┘    └─────────────────────┘    └──────────┘
        ▲                 ▲                          ▲                      ▲
        │                 │                          │                      │
   extract-             (judgment              specify-backtest         run-backtest
   trading-              you can              (faithful translation)     (planned ⏳)
   system                actually read)
   ✅ v1
```

**Why two stages?** Because **you're backtesting an operationalization, not the original method**. Without knowing how the operationalization was done, the backtest results have no meaning for you. The operationalization log is the soul of this project.

## Quick Start

### Prerequisites

- [Claude Code](https://docs.claude.com/claude-code) CLI (authenticated)
- macOS / Linux (`pdftotext` ships with macOS; Linux needs `apt install poppler-utils`)
- Python 3.10+ (only for the helper script)

### Install

```bash
git clone https://github.com/lilechen/research-to-backtest.git
cd research-to-backtest

# Symlink skills into your Claude Code skills directory
ln -s "$(pwd)/skills/extract-trading-system" ~/.claude/skills/extract-trading-system
ln -s "$(pwd)/skills/specify-backtest"        ~/.claude/skills/specify-backtest
```

### Use

```bash
# Stage 1: extract a human-readable strategy from a PDF
$extract-trading-system
> PDF: /path/to/book.pdf
> Type: book   # or paper

# Stage 2: convert to a backtestable spec
$specify-backtest
> Strategy: /path/to/<name>.trading-system.md
```

**Artifacts**:

- Stage 1 → `<name>.trading-system.md` (placed next to PDF or in `examples/<book>/`)
- Stage 2 → `<name>.system-spec.yaml` + `<name>.operationalization-log.md`

**Always review the "high-risk" rows in the log** — these are where the backtest deviates most from the original method.

## Examples

`examples/` is organized as one folder per book, covering two contrasting document styles:

| Folder | Document | Type | Demonstrates |
|---|---|---|---|
| [`Weinstein/`](examples/Weinstein/) | Stan Weinstein, *Secrets for Profiting in Bull and Bear Markets* | book | **Full three-stage pipeline** — stage analysis + visual judgment + chart patterns + spec YAML + operationalization log |
| [`Clenow/`](examples/Clenow/) | Andreas F. Clenow, *Following the Trend* | book | **Full three-stage pipeline** — fully quantitative CTA trend-following, with 4-档 risk levels, 30-year sector attribution, 2002-2021 year-by-year |
| [`Oneil/`](examples/Oneil/) | William J. O'Neil, *How to Make Money in Stocks* | book | **Stage 1 (CANSLIM growth-stock style)** — 7-factor screen + cup-with-handle / base patterns + 7-month cycle |

When extracting a new document, drop its artifacts into `examples/<book-name>/`.

## Design Principles

1. **Human-readable first.** Stage 1 keeps judgment words. A person can sit down and trade it, knowing which parts are judgment.
2. **The operationalization log is the soul.** Stage 2 records every "book wording → predicate" mapping with fidelity risk (low / medium / high). **A spec without a log is not trustworthy.**
3. **Honest gaps.** Non-computable elements are excluded and logged, never fabricated or force-coded. "Explicit in the book" vs "inferred" are strictly distinguished.
4. **Framework-agnostic YAML.** Uses generic operators (SMA, slope, rolling_max, ratio, ATR). Any backtest engine can consume it.
5. **Original numbers preserved verbatim.** Every key rule cites a PDF page, for human cross-checking.

## How It Works

### Repository Layout

```
research-to-backtest/
├── skills/
│   ├── extract-trading-system/        Stage 1: PDF → human strategy
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── system-template.md           (13-section template)
│   │   │   ├── reader-prompt.md             (parallel reader sub-agent prompt)
│   │   │   ├── synthesizer-prompt.md        (merge sub-agent prompt)
│   │   │   ├── long-pdf-reading.md          (long-PDF parallel protocol)
│   │   │   └── extract-and-chunk.py         (pdftotext chunking helper)
│   │   └── agents/openai.yaml
│   ├── specify-backtest/               Stage 2: strategy → YAML + log
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── spec-schema.yaml
│   │   │   ├── operationalization-guide.md
│   │   │   └── critic-prompt.md             (adversarial checker)
│   │   └── agents/openai.yaml
│   └── run-backtest/                   Stage 3: spec → backtest (TBD)
├── examples/
│   ├── Weinstein/                      (3 files: trading-system + spec + log)
│   ├── Clenow/                         (3 files: trading-system + spec + log)
│   └── Oneil/                          (1 file: trading-system; Stage 2 pending)
├── README.md / README.en.md
└── LICENSE
```

### Stage 1 Internal Flow (`extract-trading-system`)

```
PDF → mdls / pdfinfo to get page count
     → ≤80 pages: single read
     → >80 pages: chunk into ~60-page blocks (extract-and-chunk.py)
                ↓
                N reader agents in parallel (read .txt, Write notes to /tmp/...)
                ↓
                1 synthesizer agent (read all notes + example, Write final doc)
                ↓
                13-section complete document
```

### Model Compatibility

- **Models with image input** (GPT-4o / Claude / etc.): readers use Read's `pages` param to visually ingest the PDF.
- **Text-only models** (e.g., glm family): auto-fallback to `pdftotext` extraction + readers consume `.txt` files (with `=== PAGE N ===` markers).
- **Detection signal**: if a probe read returns `Model only support text input`, switch to the text-fallback path. Only re-run the failed reader, not all.

## Roadmap

| Stage | Skill | Status | Notes |
|---|---|---|---|
| 1 | `extract-trading-system` | ✅ v1 | Long-PDF parallel chunks, text-model fallback, synthesizer sub-agent |
| 2 | `specify-backtest` | ✅ v1 | Framework-agnostic YAML + operationalization log + critic check |
| 3 | `run-backtest` (akquant) | ⏳ Planned | Target: Rust-Python quant framework, generate backtest code from YAML |

## Contributing

Issues and PRs welcome.

**To add a new skill:**

1. Create `skills/<your-skill>/` with a `SKILL.md` (see `skills/extract-trading-system/SKILL.md` for format)
2. Reference materials go in `skills/<your-skill>/references/`
3. Add an agent descriptor at `skills/<your-skill>/agents/openai.yaml`
4. Open a PR with one example extraction under `examples/`

Filing issues for bugs / improvements / new-skill ideas is also welcome.

## Testing

Each skill ships with reference docs that serve as lightweight integration tests. To verify manually:

```bash
# Re-run Stage 1 on an example book and diff against the committed artifact
$extract-trading-system
> PDF: examples/Weinstein/Weinstein.pdf
# ...compare against examples/Weinstein/Weinstein.trading-system.md
```

CI + automated diff comparison: planned.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

- Design inspired by Robert Carver's *Systematic Trading* and its emphasis on backtest fidelity
- The "operationalization log" framing is original to this project; if you find it useful, a star helps others discover it
- Document processing powered by [poppler](https://poppler.freedesktop.org/)'s `pdftotext`

---

Made for traders who actually read the books.