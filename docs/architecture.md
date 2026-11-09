# Six-role architecture (design only)

1. **Scout:** Discover recent Solana token pools and capture timestamped candidate IDs and sources.
2. **Filter:** Reject candidates failing liquidity, age, token-authority, or holder checks; unknown mandatory evidence triggers veto.
3. **Bear:** Record three distinct, evidence-based objections.
4. **Analyst:** Verify and rebut objections; unresolved material risks prevent paper orders.
5. **Executor:** Calculate hypothetical next-candle entries and exits, including slippage and fees; no wallet calls.
6. **Risk:** Enforce position/exposure limits and auditable decisions.

**Implementation status:** Roles are conceptual. The executable code is an offline single-position simulator, not six running AI services. Proposed agent events will record role, candidate ID, UTC timestamp, evidence sources, reason, decision and prior event IDs.
