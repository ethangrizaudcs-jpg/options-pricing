# Option Pricing & Hedging — from Black-Scholes to Autocallables

> **Work in progress.**

A from-scratch study of how an equity option is priced, how a trader hedges it and where the hedging P&L comes from, what the market tells us through implied volatility, and how these building blocks combine into a structured product.

## Roadmap

| Step | Topic | Status |
|------|-------|--------|
| 0 | Setup & introduction to markets | ✅ |
| 1 | Black-Scholes, Greeks & Monte Carlo | ⏳ |
| 2 | Delta hedging & P&L attribution (core) | ⏳ |
| 3 | Implied volatility & smile on market data | ⏳ |
| 4 | Autocallable pricing (structuring) | ⏳ |
| 5 | Final write-up | ⏳ |

## Repository layout

```
src/optlab/   reusable, typed library code
notebooks/    one notebook per step (exploration, plots, analysis)
tests/        pytest suite
figures/      exported plots
data/         cached market data
docs/         study notes and interview Q&A
```

## Quick start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
```
