# Solana Six-Agent Paper-Trading Desk

**Offline Python paper-trading simulator and auditable six-agent decision-workflow design.**

> **Status:** Early public portfolio release. This execution engine is a **reconstructed educational implementation** based on project records, not an exact copy of the original simulator. Synthetic OHLCV fixtures only. No wallet connections, Solana transactions, live feeds, or autonomous AI inference are implemented. Not investment advice.

## Six-role design

```text
Scout → Filter → Bear → Analyst → Executor → Risk
```

The roles are a documented proposed workflow, **not six deployed agent services**. See [architecture](docs/architecture.md).

## Run locally

Requires Python 3.10+; no third-party dependencies or API keys.

```bash
python main.py
python -m unittest discover -s tests -v
```

Demo output is written to `output/results.json` and `output/orders.csv` and uses **invented candles**.

## Reconstructed demo rules

- $90 initial virtual equity; at most 8% allocated to an entry.
- Closed-candle momentum signal (+3%) with **next-candle-open** execution.
- 1% assumed adverse slippage each side, 0.35% assumed fee each side, $0.01 per transaction leg.
- 6% initial stop; trailing mechanism arms after +12% high-water gain and updates next candle.
- Gap-aware stop fills; at most 2 entries per UTC day.
- Illustrative 2% daily and 5% weekly cash-based loss gates.

**Limitations:** Single position at a time; not yet a multi-token engine. Daily/weekly gates use cash, not full marked-to-market equity. No live pool verification, mint/freeze checks, token holder analysis, or six-agent autonomous evaluation is implemented in runnable code.

## Keep performance ledgers separate

| Ledger | Status | Interpretation |
|---|---|---|
| Historical market-observation paper ledger | $90, zero approved trades | No trades placed; risk vetoes logged in earlier project records |
| Historical synthetic mechanical test | $90 → ~$89.400624 | Different deterministic test; **not market performance** |
| This repo's demo | `python main.py` | Newly reconstructed synthetic fixture; neither historical ledger |

The original standalone simulator source ZIP has not been recovered; it should be compared before claiming exact historical reproduction.

## Roadmap

- [x] Public README and reconstructed stdlib-only synthetic simulator.
- [x] Basic unit tests and example fixture.
- [ ] Recover and reconcile original simulator source and historical runs.
- [ ] Implement independently testable six-role veto/evidence pipeline.
- [ ] Develop V1 and V2 as independent strategies.
- [ ] Add optional no-cost, read-only market data ingestion and provenance controls.
- [ ] Build AgentOps-style animated monitoring dashboard.

See [architecture](docs/architecture.md), [limitations](docs/limitations.md), and [strategy notes](strategies/README.md).

**Safety:** No API keys, wallets, or live orders. Synthetic results do not demonstrate profitability.