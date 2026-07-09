# Dispatch — gamora: C3 KPM band re-fit on the E1-widened population (first content-bearing per-axis run)

**From:** knight-rider → **To:** gamora (simulation seam — band tables + certification driver)
**Date:** 2026-07-08
**Pattern:** B (multi-hour compute; math-before-code) — **Gate-1 (jack-ryan) REQUIRED before fire**
**Authority:** Matt-ratified full-run pivot 2026-07-08 (decisions-log `a50db87`, Q13 APPROVED). Surface-ledger row **C3 — OPEN, `gates-on: E1` now SATISFIED** (E1 landed `bfc94eb`, Gate-2 PASS `7956484`). Matt sequencing directive 2026-07-08: *"C3 BAND RE-FIT (main line, next compute)."*
**Status:** FIRE-READY — jack-ryan Gate-1 **PASS-WITH-AMENDMENTS** (2026-07-08); both amendments folded (§2 bullet 3 entangled-delta fallback + §6 criterion 4 four-cohort enumeration & cohort-count==4 pre-fire assertion). Cleared to execute.

---

## 0. Why this run exists

The live KPM band tables were fit to **STRIPPED distributions on the now-SCRAPPED seed-57000000 population** (surface-ledger C1/C3; pivot ruling C1). Two things invalidate them as the certification instrument:

1. **Population changed** — the emission population now regenerates on the **E1-widened emitter** (per-skill kernel geometry over the rich vocabulary, `bfc94eb`). Geometry widening SHIFTS effective throughput (B11 multipliers the sim applies), so the KPM distributions move.
2. **Baseline changed** — the pivot ruled certification measures the **declared baseline = arm G (geared)** (E5-C; pilot_policy instrument-vs-content rider, `ce595a7`). Bands must be fit to arm-G distributions, not stripped.

This run regenerates the per-axis population on the E1-widened emitter, runs the two-arm certification, and **re-fits the KPM bands at the declared baseline (arm G)**. It is the **first content-bearing per-axis certification run** — its readout routes to Matt via gandalf.

## 1. The two Gate-2 riders (BIND the run config — from jack-ryan finding `7956484`)

- **INFO-1 — Path-3-blind pre-E1 baseline.** The pre-E1 emitter emitted `small_aoe`/`large_aoe`, which were **never valid `_RICH_TO_SPATIAL` keys** → the old population was largely **Path-3 geometry-blind**. The re-fit delta (how much bands moved) MUST be read against **that** Path-3 baseline, NOT a clean 3-shape one. Do not attribute the full band shift to "geometry variety" — part of it is the correction of a silent degradation. Name the two components in the readout.
- **INFO-2 — four-cohort arm-G config.** The `leg_i_cell_grain_two_arm_driver.py` defaults arm G to a **single `Balanced` cohort**. The content fire MUST exercise the **four-cohort arm-G path** (`--all-cohorts-arm-g`, or `w5g1 arm="G"` per-cohort) so the **per-cohort delta map** exists. A single-cohort run does not satisfy this dispatch.

## 2. MATH-BEFORE-CODE (Discipline #1) — REQUIRED, precedes any re-fit

Author a math note (`simulation/math/c3-band-refit-e1-<date>.md`) BEFORE re-fitting. It must answer:
- **The re-fit methodology** — how each band's (floor, ceiling) is derived from the arm-G distribution (percentile choice, per-family, per-cohort aggregation rule). State it explicitly; the current bands' derivation is the reference to match or justify departing from.
- **Declared-baseline statement** — bands are fit to **arm G**; the stripped arm is the scaling-delta DIAGNOSTIC (E5-C), not the cert measure. Do NOT quote any stripped figure as the geared baseline (reframe-validity discipline).
- **The two-component delta (INFO-1)** — separate (a) the Path-3-correction component from (b) the genuine geometry-variety component of the band shift. Name both. **[Gate-1 amendment 2, jack-ryan INFO]** If the two components are not cleanly separable from the arm-G distributions alone (they may be entangled — the Path-3 correction and the geometry variety act on overlapping amplitude space, ~2/3 of it), state that explicitly and give the bounding characterization rather than a false-precision split — do NOT manufacture a clean decomposition the data does not support (Discipline #12 / reframe-validity).
- **Geometry-only band caveats preserved** — `dense_cell` and `escape_lane` bands remain GEOMETRY-ONLY per the pilot_policy entry; the shared-102.86-ceiling INFO on `magic_pack`/`dense_cell` carries forward or is re-derived — state which.

## 3. The current-instrument band set (reference — the set being re-fit)

Per pilot_policy entry (`ce595a7`), the 2026-07-08 ratified set (STRIPPED, scrapped population — reference only, NOT the target):

| Family room | (floor, ceiling) | note |
|---|---|---|
| open_arena | (20.87, 53.33) | |
| chokepoint_corridor | (12.52, 60.00) | |
| magic_pack | (12.52, 102.86) | shared-ceiling INFO |
| elite_pack | (8.26, 28.13) | |
| dense_cell | (12.52, 102.86) | GEOMETRY-ONLY |
| boss_with_adds | (2.49, 3.78) | |
| mini_boss | (0.57, 3.30) | |
| escape_lane | exit ≥ 0.80 + KPM [60,150] | F4 criterion, GEOMETRY-ONLY |

Rider-3 disposition semantics unchanged: below-floor = HARD FAIL · in-band = PASS · over-ceiling = FLAG_PASS_OVERPOWERED → balance review.

## 4. Cross-seam discipline (ADR-004)

- No sim contract CHANGE expected — you re-fit values you own (band tables) on a population from the already-landed E1 emitter (no rocket interface change). If the re-fit surfaces a need to change what the driver reports to star-lord telemetry, that is cross-seam → MIGRATION.md + Matt before tagging.
- **Discipline #3 (no parallel regens of same seed):** arm S and arm G run at the SAME per-cell seed (the driver already enforces this; confirm in the run banner).

## 5. #2-FF fields (MANDATORY — eat our own cooking)

- **Verdict-rendering instrument named:** the re-fit band tables + the per-cohort arm-G delta map + the two-component (Path-3 vs geometry) attribution.
- **One-command pre-fire verification** that exercises the PATH (lesson from the C2 halt — verify emission-path reachability, not just leaf existence): a single command proving the four-cohort arm-G path actually runs and produces a non-zero per-cohort delta before the full re-fit fires. It MUST assert **cohort-count == 4** in its first-log line (a single-cohort run also produces a non-zero delta, so a bare non-zero check does NOT defeat the INFO-2 default-to-Balanced trap). State the expected first-log line.
- **Precondition state cited:** surface-ledger C3 row; decisions-log `a50db87` + `ce595a7`; Gate-2 finding `7956484` (both riders).

## 6. Acceptance criteria

1. Math note lands FIRST (Discipline #1), answering §2.
2. Population regenerated on the E1-widened emitter; two-arm certification run with the **four-cohort arm-G path** (INFO-2).
3. KPM bands re-fit to the **arm-G declared baseline**; the re-fit set replaces the current-instrument set as the certification bands (surface-ledger C3 flips ✓ on Matt-seen).
4. Per-cohort arm-G delta map produced **for all four cohorts** — the readout MUST enumerate four distinct per-cohort deltas (a single-cohort delta map is a **HARD FAIL** of this criterion, per INFO-2; the driver DEFAULTS to a single `Balanced` cohort — that is the trap). The #2-FF pre-fire one-command verification (§5) MUST assert **cohort-count == 4** in its first-log line, not merely that a non-zero delta exists (a single-cohort run also produces a non-zero delta). Two-component delta (INFO-1) attributed in the readout. **[Gate-1 amendment 1, jack-ryan WARN]**
5. #2-FF fields present in the run banner.
6. **First content-bearing pilot readout authored and routed to Matt via gandalf** (Matt's directive).
7. Tag `gamora/v<X.Y>-c3-band-refit-1` (seam prefix — intermediate; Matt approves any prefix drop).

## 7. Explicitly OUT OF SCOPE (prevents scope creep)

- **E2/E3/E4 axes** (economy / hybrid / timing) — separate queued axes; E2 is HELD pending gandalf's design note.
- **Emitter changes** — E1 landed; do not touch `per_skill_emitter.py`.
- **The mob-affix layer (E10)** — separate design-first track (legolas → gandalf design session).
- **Emission fire of any size (C4)** — GATE1-bound; this run re-fits bands + produces the readout, it does NOT un-gate emission.

## 8. Instrument guard (STANDING — all runs)

Affixed mobs and content encounters **never enter the certification gauntlet rooms.** The gauntlet certifies kits against the clean four-family instrument; content-side affix/encounter layers live outside it.

---

**Required reading (gamora, at session start):**
1. This dispatch.
2. `canonical/current-to-end-state/surface-ledger.md` — C3 row (+ both riders) + E1/C2 (✓, landed).
3. `agentic_orchestration/qa/findings/2026-07-08-batched-gate2-gamora-completion-rocket-e1.md` — INFO-1 + INFO-2 verbatim.
4. `design/decisions/decisions-log.md` — `a50db87` (pivot) + `ce595a7`/`8185098` (pilot_policy two-arm + band set).
5. Your own `leg_i_cell_grain_two_arm_driver.py` + the SESSION-60 completion record (four-cohort arm-G path).

**Sign-off:** knight-rider, 2026-07-08 (DRAFT — Gate-1 pending). Fires on jack-ryan Gate-1 PASS.
