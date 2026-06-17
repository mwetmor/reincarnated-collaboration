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

---

## Completion record — Stage 1 (gamora, 2026-06-16)

**Status:** STAGE 1 COMPLETE — characterize + propose. NO gate wired (Stage 2 is gandalf-ruling-gated, then jack-ryan Gate-2). Band NOT self-approved.

**Data reconciliation (the labeling discrepancy, resolved first):**
- The `*-smoke-20260616_224010.json` (`mode: smoke, n_cells: 95`) is a SMOKE SUBSET (`kits[:5]` × one encounter/shell → only 2 weak melee probe archetypes). NOT the full slice.
- The 68k-line `/tmp/kpm_full_run.log` is pure WARNING-level spatial-engine telemetry (0 per-cell KPM values). The "large run" impression is a log-volume artifact; the full distribution was NOT recoverable from the log.
- **The genuine full slice WAS persisted by a prior session:** `output/kpm-band-spatial-recal-full-20260616_224528.json`, **n_cells = 3078 = 54 kits × 18 encounters × viable cohorts.** Authoritative; crc32-stable seeds make it reproducible. A confirmation re-run was started and then killed as redundant (no parallel same-seed regen left running). All Stage-1 numbers are from the n=3078 FULL slice.

**Key findings (full slice REVISES the smoke-based framing):**
1. **boss_with_adds + mini_boss are NOT all-zero/unclearable** — that was a 2-kit smoke artifact. They carry a real ~10-25% zero-clear LOW tail, but central mass clears (boss median 1.42, mini median 0.44). The degeneracy claim is PARTIALLY confirmed (real low tail), substantially revised (not uniformly degenerate).
2. **Root cause #1 — mob-HP scale mismatch:** CONFIRMED, and BIMODAL (elite p10=0.148 vs p25=1.884). "Clear near-instantly or never" produces a bimodal mixture, not a uniform band. `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` per `[R2 calibration]` log lines.
3. **Root cause #2 — METRIC-NUMERATOR DIVERGENCE (rooms/min vs mobs/min) — LOAD-BEARING:** W4G numerator is `kills = 1 if fr.player_kill else 0` (`t4_sim_cycling.py:1077`, win-flag ≤1/fight) = rooms/min. RESOLVE `SPATIAL_ENCOUNTER_KPM_BAND` (`gauntlet_sim.py:341-347`) is mobs/min (pack-arithmetic, `A≈43 TMPM`). Both gate AND RESOLVE consume the same `observed_kpm` (`gauntlet_sim.py:1003/1029`) → inconsistent numerators (~5-55× per shell). This is the instrument-level question gandalf must rule.
4. **Row-by-row cross-check vs RESOLVE band:** DIVERGES on every shell (~5-55×). Not convergence; the factor is the per-won-room mob-count fingerprint of root cause #2.
5. **Proxy-reusable surface CONFIRMED** (per-fight objects retained, keyed; `proxy_reusable_surface: true`). `proxy_contribution_pct` NOT implemented (Synty-paused).

**Artifacts (committed under tag intent `gamora/v1.1-kpm-band-spatial-recalibration`):**
- Math note (findings §7): `simulation/math/kpm-band-spatial-recalibration-2026-06-16.md`
- Stage-1 RETURN: `simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE1-RETURN.md`
- Harness: `scripts/gamora_kpm_band_spatial_recalibration_2026_06_16.py`
- Full output: `output/kpm-band-spatial-recal-full-20260616_224528.json`
- MIGRATION Stage-1 entry: `simulation/MIGRATION.md` v1.73 (v1.72 collision-reconcile deferred to Stage 2)

**Interim guard restated:** Phase-3 season-gen output remains NON-CANONICAL until Stage 2 lands the gandalf-approved band (jack-ryan-gated).

**READY FOR GANDALF RULING** — KR routes. Two questions: (1) instrument-level: rooms/min vs mobs/min numerator; (2) felt-rhythm: per-shell central-mass band cut. NO push (Matt-gated).
