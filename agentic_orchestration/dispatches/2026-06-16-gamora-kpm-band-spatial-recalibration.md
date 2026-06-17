# Dispatch — 2026-06-16 — gamora — Phase-3 KPM-band recalibration to the 2D spatial instrument

**From:** knight-rider (relaying gandalf design-intent, Matt-authorized 2026-06-16)
**To:** gamora (simulation seam)
**Design owner:** gandalf (design-spec-as-math; final band ruling is gandalf's)
**Status:** COMMISSIONED — small standalone dispatch. Do NOT bundle behind the paused proxy work.
**Estimated effort:** ~0.5–1 day (harness + distribution characterization + band proposal; then a gated wire-in after gandalf rules)

## Why
The b6/1D-sim deletion follow-on B repointed the W4G/W5G gauntlet KPM sweep onto the 2D spatial sim (commit `de09d8b`, Gate-2 PASS-WITH-INFO). `observed_kpm` is now measured on the spatial pack-clear instrument (KPM ceiling ~44), but the Phase-3 gate still compares it against the **legacy 1D-duel band (150–836)** → systematic over-rejection. decisions-log `2026-06-16` carries this as the open recalibration item. This dispatch closes it.

## Design intent (gandalf, relayed by Matt — do NOT re-litigate)
The Phase-3 KPM gate is a **pacing gate on the now-spatial instrument, not a damage-rate check.** It should reject kits that clear a pack **too slowly (slog)** or **implausibly fast (trivialize)**, preserving the felt-rhythm zone. The band brackets the *central mass* of healthy-kit pacing — it is not a DPS floor/ceiling.

## Stage 1 — characterize + propose (gamora → gandalf)
1. **Math note first (Discipline #1).** State the instrument (spatial pack-clear), the metric definition (`observed_kpm` as the repoint produces it), and the characterization plan BEFORE running.
2. **Run the representative-loadout HEALTHY slice** — the determined keystone slice (the Wave-2 representative-loadout "determined ~90%" slice) — through the **repointed 2D spatial sim**.
3. **Characterize the `observed_kpm` distribution:** mean, spread (sd/IQR), and percentiles (at least p5/p10/p25/p50/p75/p90/p95).
4. **Propose a band** that brackets the central mass — reject only genuine slog (low tail) / trivialize (high tail) outliers.
5. **Return the distribution + the proposed band to gandalf for the FINAL ruling.** Do NOT self-approve the band — gandalf owns the felt-rhythm call. KR routes your Stage-1 return to gandalf.

## Stage 2 — wire-in (gamora, AFTER gandalf rules; jack-ryan gates)
6. Wire the **gandalf-approved** band into the Phase-3 gate (replaces the 150–836 1D-duel constant).
7. **jack-ryan Gate-2** on the wire-in — it changes a gate threshold, so it gates (two-witness: clean + the healthy slice passes its central mass, slog/trivialize outliers reject).

## Forward-compat (build into the Stage-1 harness)
Build the harness pass so the **future proxy `proxy_contribution_pct` measure can reuse the same slice + the same spatial instrument** — shared instrument, separate timelines. Don't hardwire it to KPM-only; leave the per-fight result surface reusable. (Proxy work itself is PAUSED behind Synty substrate-acquisition — this is harness-shape forward-compat only, not proxy implementation.)

## Interim guard (state in the math note + MIGRATION)
Until this recalibration lands, treat any **Phase-3 season-gen output as NON-CANONICAL** — the KPM gate is known-mis-calibrated; do NOT archive Phase-3 results as canonical.

## Also fold in (routine, no gandalf input)
- **MIGRATION v1.72 numbering collision:** the AOE re-home entry AND the t4-repoint entry both claim `v1.72`. Reconcile the numbering with jack-ryan (assign the next free number to one of them) as part of this dispatch's MIGRATION write. Routine attribution hygiene (Discipline #9).

## Out of scope
- Do NOT implement the proxy `proxy_contribution_pct` measure (Synty-paused) — only leave the harness reusable.
- Do NOT touch generation/output seams.
- Do NOT self-rule the band — gandalf rules.

## Tag intent
`gamora/v1.1-kpm-band-spatial-recalibration` (seam-prefixed). Do NOT push (Matt-gated).

## Gate
Stage 1: gandalf final band ruling. Stage 2: jack-ryan Gate-2 on the threshold wire-in.
