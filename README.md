# Solana Six-Agent Paper-Trading Desk

**Offline Python paper-trading simulator and auditable six-agent decision-workflow design.**

> **Status:** Early public portfolio release. The execution engine is a **reconstructed educational implementation** based on earlier project records, not the exact original source. Synthetic OHLCV data only. No wallets, live trades, live market feeds, or autonomous AI agent services. Not investment advice.

## Architecture

```text
Scout → Filter → Bear → Analyst → Executor → Risk
```

The six roles are **planned workflow components**, not working AI services. See [architecture](docs/architecture.md).

## Quick start

Python 3.10+; no paid APIs, keys or third-party packages required.

```bash
python main.py
python -m unittest discover -s tests -v
```

Demo outputs: `output/results.json` and `output/orders.csv` (ignored by Git). The supplied OHLCV candles are invented and do **not** constitute a historical backtest.

## Simulator assumptions

- Initial simulated cash: **$90**.
- Maximum **8%** of available cash allocated per entry; two entries per UTC day.
- A previous closed-candle +3% momentum signal triggers a **next-candle-open** entry.
- 1% adverse slippage and 0.35% assumed fee per side; $0.01 fixed cost per leg.
- 6% initial stop; trailing mechanism after +12% high-water gain, next-candle activation.
- Gap-aware stop handling and illustrative 2% daily / 5% weekly cash-based loss gates.

**Limitations:** Single active position, not three. Cash-based loss controls are not complete portfolio risk accounting. No live token screening, pool age, rug checks, holder analysis, quote verification or automated multi-agent debate is implemented.

## Separate accounting — never combine

| Record | Status | Interpretation |
|---|---|---|
| Historical market-observation **paper ledger** | $90 equity; zero approved trades | No real money or actual orders |
| Prior separate **synthetic mechanical test** | $90 → ~$89.400624 | Distinct invented test, not real-market performance |
| Current repository demo | Run `python main.py` | Newly reconstructed synthetic fixture, not either historical ledger |

The original simulator ZIP/source was not recovered; historical results cannot be claimed as reproduced by this repository.

## Latest Development — November 9, 2026

Our separate working project added a **SQLite-backed paper portfolio**, **read-only Jupiter quote probes**, **research-cycle orchestration**, and an **ownership/liquidity audit with fail-closed risk decisions**.

These developments are **documented but their original Python source files have not yet been imported into this public GitHub repository**. The code published here remains a reconstructed offline synthetic simulator, not a live trading system.

The separate market-observation paper ledger recorded **$90.000000 with no approved trades**; a distinct working-project **synthetic-only** ledger recorded **$90.488309**. These are not live returns and must not be combined with other synthetic tests.

Read the [November 9 development report](docs/2026-11-09-development.md) for module status, evidence limitations, recorded results, and a safe source-import checklist.

## Project contents

- [Simulation engine](simulator/engine.py), [entrypoint](main.py), [unit tests](tests/test_engine.py) and [synthetic sample](examples/synthetic_candles.csv)
- [Design of the six roles](docs/architecture.md)
- [Model limitations](docs/limitations.md)
- [Separate V1/V2 strategy roadmap](strategies/README.md)
- [Agent implementation status](agents/README.md) and [dashboard status](dashboard/README.md)

## Roadmap

- [x] Publish a reproducible, offline educational simulator.
- [x] Include synthetic fixture, documentation and unit tests.
- [ ] Recover and reconcile original simulator and historical execution records.
- [ ] Implement six independent agent decision/veto modules.
- [ ] Develop V1 and V2 separately without overwriting either.
- [ ] Add optional free read-only timestamped market-data integration.
- [ ] Build a dark AgentOps-style event dashboard.

## Safety

Educational software only. No wallet connections, API secrets, real orders or claims of profitability. Synthetic P&L should not be presented as market performance.

MIT licensed.
