# Scope, provenance and limitations

- Reconstructed educational implementation, not the previously generated original simulator ZIP.
- All bundled candles are invented. Not historical Solana price series or real-market backtests.
- Intrabar high/low ordering is unknown; stops are processed before trailing updates.
- Only one simultaneous position, no multi-token agent trading.
- Cash-based daily/weekly loss gates are approximations, not portfolio mark-to-market risk.
- No MEV, rug pull, transfer-tax, on-chain failure, route quote, pool-age or liquidity analysis.
- Fixed slippage and fees are assumptions, not executable quotes.
- Historical synthetic ending balance ~$89.400624 belongs to a separate test.
