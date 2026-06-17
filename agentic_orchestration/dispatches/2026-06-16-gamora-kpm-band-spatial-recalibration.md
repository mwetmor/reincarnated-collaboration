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

---

## gandalf RULING + Stage-2 SCOPE EXPANSION (gandalf ruled 2026-06-16; Matt-authorized 2026-06-16)

**Headline: FIX THE INSTRUMENT BEFORE ANY BAND** (the valid non-band outcome this dispatch invited). gandalf verified the defect at code level.

1. **Metric numerator → MOBS/MIN.** The Phase-3 gate is mis-wired to rooms/min (`kills = 1 if player_kill`, win-flag, `t4_sim_cycling.py:1077`). Engine already computes `mobs_killed` (`spatial_engine.py:1702`); fix is `f.kills = fr.mobs_killed`. A correctness defect, not a tuning dial — genre TMPM canon + RESOLVE-band derivation + instrument-consistency all converge. Collapses the ~5–55× divergence with `SPATIAL_ENCOUNTER_KPM_BAND` by construction.
2. **Band → DEFERRED.** No band approved on the broken numerator. Returns to gandalf after re-characterization in mobs/min. gamora's harness/slice/stratification/proxy-surface all carry forward unchanged.
3. **Bimodality (`MOB_HP_DIFFICULTY_MULTIPLIER=1.5`) must NOT be papered over** (Discipline #13 drift — conflating scale-artifact with slog would cull legitimate defensive archetypes). Sequenced downstream of the numerator fix; re-read on mobs/min before deciding if it's a separate `MOB_HP` reconciliation workstream.

**Matt-authorized EXPANDED Stage-2 sequence:**
- **2a (gamora):** numerator fix `f.kills = fr.mobs_killed` — Discipline #12 semantic shift; enumerate the full `StratumFightBatch.observed_kpm` consumer set + flag in MIGRATION.
- **2b (gamora):** re-characterize same 54-kit slice in mobs/min (harness exists). Return distribution + consumer audit to KR.
- **2c (gandalf):** KR routes the mobs/min distribution to gandalf for the per-shell felt-rhythm band ruling (bimodality handled on corrected data: p25/p75 mode-bracket vs p10/p90).
- **2d (gamora):** wire gandalf-approved band into the Phase-3 gate.
- **Gate-2 (jack-ryan):** on the combined semantic-shift + band wire-in; MUST verify the full `observed_kpm` consumer set (RESOLVE cert at `gauntlet_sim.py:1003/1029` is CORRECTED-by-this, not broken).
- v1.72 MIGRATION numbering-collision reconcile stays a Stage-2 housekeeping item.

Interim guard holds: Phase-3 season-gen output NON-CANONICAL until Stage 2 lands.

---

## Completion record — Stage 2a + 2b (gamora, 2026-06-16)

**Status:** STAGE 2a + 2b COMPLETE. Instrument fixed (numerator → mobs/min), slice re-characterized in mobs/min, distribution + verdicts handed up. NO band wired (2d), NO band self-approved (2c is gandalf's). NO Gate-2 yet (jack-ryan). NO push (Matt-gated). Auto-committed in-scope.

### 2a — numerator fix (Discipline #12 SEMANTIC SHIFT)
- `t4_sim_cycling.py:1077`: `kills = 1 if fr.player_kill else 0` (rooms/min) → `kills = fr.mobs_killed` (mobs/min). Denominator (`fr.elapsed_s`) UNCHANGED. `fr.mobs_killed` verified on `SpatialFightResult` (`spatial_engine.py:1702` compute, `:1815` surface).
- Math note: `simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2A-NUMERATOR-FIX.md` — full consumer audit (§4, 14 consumers) + sub-gate-3 semantic interaction (§5).
- MIGRATION v1.74 — semantic-shift entry + consumer audit; supersedes the v1.73 rooms/min warning.
- **Consumer-audit verdict: CLEAN — NO hidden rooms/min dependency.** Every band-comparison consumer (W4G gate `t4_sim_cycling.py:682-700/800-831`; RESOLVE cert `gauntlet_sim.py:1003/1029`; Track-1 `gauntlet_sim.py:1051`; phase7 `phase7_bridge.py`/`phase7_verdict.py`) judges against a mobs/min-derived band → all were silently MIS-comparing under rooms/min and are CORRECTED by the fix. RESOLVE cert is CORRECTED-by-this, NOT broken (as the dispatch required). One semantic INTERACTION: sub-gate-3 `_check_zero_damage_floor` (`t4_sim_cycling.py:714`) predicate `f.kills==0` shifts from "didn't clear the room" (win-flag FALSE-POSITIVE on 7/8-mob near-clears) to "killed literally zero mobs" (true zero-damage floor — its named intent). Moves TOWARD correctness; WARN-not-BLOCK so cannot harden any verdict. Flagged for jack-ryan Gate-2.

### 2b — re-characterization in mobs/min (full slice)
- Run: `output/kpm-band-spatial-recal-full-20260616_232152.json` — n_cells=3078 (= Stage-1 slice exactly), 256.6s blocking foreground (single in-session command; NOT backgrounded — the prior-two-sessions park-failure cause).
- Characterization doc: `simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2B-MOBSMIN-CHARACTERIZATION.md`.

**Mobs/min distribution (per-shell p50 / IQR):** boss_with_adds 2.84/1.00 · chokepoint_corridor 13.96/2.69 · elite_pack 6.95/3.58 · magic_pack 8.76/3.74 · mini_boss 1.55/2.31 · open_arena 13.51/3.48. Cohort-invariant within shell (means agree ≤0.1) → per-shell band suffices.

**Bimodality verdict: PERSISTS + SHARPENED on the 3 boss/elite shells.** p10→p25 valley: boss_with_adds 9.97×, elite_pack 6.20×, mini_boss ∞ (literal zero-clear floor). UNIMODAL on chokepoint/magic/open (1.06–1.20×). The low mode is the `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` HP-wall artifact (low-throughput melee vs 1.5×-inflated mob HP), shell-specific to boss/elite, ≈5–20% of cells. NOT papered over (gandalf item 3) — the multiplier IS the mechanism; whether it warrants a separate `MOB_HP` workstream is gandalf's 2c call.

**RESOLVE-band convergence verdict: order-of-magnitude DIVERGENCE COLLAPSED (5–55× → 0.63–4.74×), floor residual on 3 open shells.** 3 boss/elite shells (boss_with_adds, elite_pack, mini_boss): median INSIDE RESOLVE balanced band — full convergence by construction, as gandalf predicted. 3 open shells (chokepoint, magic, open_arena): median AT/BELOW RESOLVE floor (median/floor 0.63–1.00×) — residual is a derivation-idealization gap (RESOLVE floor assumes pure 43-TMPM; spatial instrument includes travel/telegraph/approach overhead), NOT a numerator defect.

**Provisional per-shell bracket (NOT self-approved — gandalf 2c rules):**

| shell | p10/p90 (central 80%) | p25/p75 (mode-only) | median |
|---|---|---|---|
| boss_with_adds | [0.25, 3.78] | [2.49, 3.49] | 2.84 |
| chokepoint_corridor | [11.65, 15.88] | [12.38, 15.07] | 13.96 |
| elite_pack | [0.91, 10.00] | [5.65, 9.23] | 6.95 |
| magic_pack | [6.06, 11.43] | [7.27, 11.01] | 8.76 |
| mini_boss | [0.00, 3.30] | [0.57, 2.88] | 1.55 |
| open_arena | [9.90, 15.53] | [11.08, 14.56] | 13.51 |

On the 3 unimodal open shells p10/p90 is a clean band; on the 3 bimodal boss/elite shells p25/p75 excludes the `MOB_HP=1.5` low mode (adopt ONLY if gandalf judges the low mode genuine non-clear, not a defensive archetype to preserve — Discipline #13).

**READY FOR GANDALF 2c BAND RULING.** Two design Qs: (1) mode-bracket on the 3 bimodal shells + `MOB_HP=1.5` separate-workstream call; (2) open-shell floor residual (empirical-anchor recommended vs RESOLVE-floor). KR routes to gandalf. v1.72 MIGRATION numbering-collision reconcile + 2d wire-in + Gate-2 still pending.

---

## Completion record — Stage 2d (gamora, 2026-06-16)

**Status:** STAGE 2d COMPLETE — gandalf-APPROVED per-shell mobs/min band WIRED into the Phase-3 W4G gate; legacy 1D-duel 137–836 band REPLACED; RESOLVE band untouched; v1.72 numbering-collision RECONCILED; smoke PASSES. NO band re-opened (gandalf ruled). NO Gate-2 self-close. NO interim-guard lift. NO push (Matt-gated). Auto-committed in-scope under tag intent `gamora/v1.1-kpm-band-spatial-recalibration`.

### What wired (the EXACT gandalf table landed)
`ENCOUNTER_COHORT_KPM_BAND` (`gauntlet_sim.py:206`) values replaced. Per-shell band replicated across all 4 cohort columns (cohort-invariant per gandalf; gate `[shell][cohort]` lookup + `_route_tier_1` predicate UNCHANGED). Verified via import:
- boss_with_adds [2.49, 3.78] · elite_pack [5.65, 10.00] · mini_boss [0.57, 3.30] (bimodal: p25-lo / p90-hi)
- chokepoint_corridor [11.65, 15.88] · magic_pack [6.06, 11.43] · open_arena [9.90, 15.53] (unimodal: p10/p90)
- Deliberate asymmetry preserved verbatim (p25-lo slog cut, p90-hi keep fast-clear tail). `SPATIAL_ENCOUNTER_KPM_BAND` (RESOLVE) UNCHANGED at all 6 shells.

### Smoke (Discipline #2) — PASSES (against the 2b n=3078 mobs/min distribution, judged through the WIRED constant + real `_route_tier_1`)
- **Central mass PASSES:** p50 / p25 / p75 IN-band on all 6 shells. Real gate routing on open_arena: p50=13.51 → `PROVISIONAL_PASS`; lo/hi edges (9.90/15.53) → `PROVISIONAL_PASS` (inclusive).
- **Genuine non-clear (slog) REJECTS:** p5 below `lo` on all 6 shells → `REJECT`.
- **Trivialize REJECTS:** per-shell max above `hi` on all 6 shells → `REJECT`. (open_arena kpm=20.0 → `REJECT`.)
- Clean build/import: `gauntlet_sim` + `t4_sim_cycling`; 6-shell / 4-cohort structural asserts hold.

### v1.72 numbering-collision reconcile — DONE
AOE re-home (rocket's seam, top of MIGRATION) RETAINS v1.72; t4-repoint (gamora's seam) renumbered v1.72 → **v1.75** (number-only). New Stage-2d entry is **v1.76**. jack-ryan verifies at Gate-2.

### Artifacts (committed under tag intent `gamora/v1.1-kpm-band-spatial-recalibration`)
- Math note: `simulation/math/kpm-band-spatial-recalibration-2026-06-16-STAGE2D-BAND-WIREIN.md`
- Code: `simulation/gauntlet_sim.py` (`ENCOUNTER_COHORT_KPM_BAND` values)
- MIGRATION: `simulation/MIGRATION.md` v1.76 (wire-in + provenance stamp + v1.72 reconcile) + v1.75 (renumbered) + v1.73/v1.74 cross-ref updates
- Provenance stamp (gandalf-required): bands empirically anchored to the 2026-06-16 determined-slice (`output/kpm-band-spatial-recal-full-20260616_232152.json`, n=3078); RE-FIT candidates if `MOB_HP_DIFFICULTY_MULTIPLIER` changes (composes with the separate MOB_HP workstream — documentation, not dependency).

### Interim guard
Phase-3 season-gen output stays **NON-CANONICAL until jack-ryan Gate-2 PASS** — guard LIFTS on Gate-2 PASS, NOT before, NOT self-closed here.

**READY FOR JACK-RYAN GATE-2.** qa/pending submission carries: full `observed_kpm` 14-consumer audit (Stage-2a §4), sub-gate-3 zero-damage-floor interaction (`t4_sim_cycling.py:714`, WARN-not-BLOCK), and the two-witness expectation (clean build/import + healthy-slice central mass passes / slog+trivialize reject). NO push.
