# Next Steps Checklist

## Day 0: Verify Runtime
- [ ] Run `./run_mvp.sh free` (or `run_mvp.bat free` on Windows).
- [ ] Confirm tests pass and bot prints decision output.

## Day 1-3: Paper Observation (dry-run)
- [ ] Keep `dry_run=true` in `config/bot.example.json`.
- [ ] Record decisions and reasons every run.
- [ ] Tune `min_mentions_5m`, `min_growth_rate`, `min_sentiment`.

## Day 4+: Integration Prep
- [ ] Prepare narrative API credentials for `--mode http` (optional).
- [ ] Prepare FourMeme API/SDK docs and auth method.
- [ ] Define risk caps (daily loss, max creations/day, slippage).

## Go-live Gate
- [ ] At least 3 days of stable dry-run behavior.
- [ ] Stop-loss/take-profit params reviewed.
- [ ] Key management plan ready (no plaintext private keys).
