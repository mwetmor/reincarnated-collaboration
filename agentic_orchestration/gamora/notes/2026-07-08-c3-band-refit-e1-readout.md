# C3 KPM band re-fit on the E1-widened population — first content-bearing per-axis readout

**From:** gamora (simulation seam) → **routing:** Matt **via gandalf** (dispatch §6.6; first
content-bearing pilot readout).
**Date:** 2026-07-08 (run completed 2026-07-09 00:37; 39 min wall).
**Dispatch:** `2026-07-08-gamora-C3-band-refit-e1-widened.md` (Pattern B; Gate-1 PASS-WITH-AMENDMENTS).
**Math note (Disc #1, landed FIRST):**
  `reincarnated-engine/src/reincarnated/simulation/math/c3-band-refit-e1-2026-07-08.md`.
**Driver + report:** `simulation/c3_band_refit_e1_driver.py`;
  `simulation/output/c3_band_refit_e1/c3_band_refit_e1_report.json`.
**Tag:** `gamora/v1.4-c3-band-refit-1` (intermediate; NOT pushed — KR batches).

---

## 0. TOP LINE

The E1-widened population (11–12 distinct per-skill geometries/kit, verified live) was regenerated at
the canonical season seed (14001 → 54 kits / 66 configs), and the two-arm certification ran on the
`w5g1 arm="G"` per-shell four-cohort path. **PLUMBING TOOK** (arm G ≠ arm S; max_abs_delta 52.68 KPM;
cohort-count == 4 asserted). **Result: NO KPM band's derivation moves.** All five clear-shell bands are
DENSITY/GEOMETRY-anchored (rider-4), and E1 is an EMITTER change (per-skill geometry), NOT a
room-density change — so the anchors are invariant to it. The re-fit is a **re-VALIDATION** (cross-check
the arm-G distribution against each anchor), NOT a numeric re-fit. **The bands STAND at their current
values.** Three shells surface a density-model-review FINDING (below); none is auto-resolved (rider-4:
diagnose, do not curve-fit).

---

## 1. THE RE-FIT BAND TABLE (arm-G declared baseline, E1-widened @14001)

| Family room | Band (floor, ceiling) — **STANDS** | Class | arm-G cross-check |
|---|---|---|---|
| open_arena | (20.87, 53.33) | density-anchor | in-band 84.6% · **AGREE** |
| chokepoint_corridor | (12.52, 60.00) | density-anchor | in-band 19.4% · above-ceiling 479 · **DISAGREE (finding §4)** |
| magic_pack | (12.52, 102.86) | density-anchor | in-band 86.9% · **AGREE** |
| elite_pack | (8.26, 28.13) | density-anchor (r3a-step7) | p25=29.03 > ceiling · KPM-450-cap saturation · **DISAGREE (finding §4)** |
| dense_cell | (12.52, 102.86) | density-anchor · GEOMETRY-ONLY | in-band 63.6% · above-ceiling 72 · **DISAGREE (finding §4)** |
| boss_with_adds | (2.49, 3.78) | F3 sanity-rail | success-judged; KPM re-observed as telemetry |
| mini_boss | (0.57, 3.30) | F3 sanity-rail | success-judged; KPM re-observed as telemetry |

Rider-3 disposition semantics UNCHANGED: below-floor = HARD FAIL · in-band = PASS · over-ceiling =
FLAG_PASS_OVERPOWERED → balance review. The geometry-only caveats (dense_cell, escape_lane) are
preserved; the shared-102.86-ceiling INFO (magic_pack + dense_cell both listen at 102.86) carries
forward — the rails-at-ceiling falsifier is now LIVE-tested (§4).

**Why the density bands do not move (the correct reading of "re-fit at the declared baseline"):** the
pivot ruled bands re-fit at each new declared baseline. For a density anchor the re-fit is a
re-VALIDATION at that baseline, not a curve-fit. The baseline MOVED (stripped arm S → geared arm G);
the bands are RE-CONFIRMED against it. An endpoint moves ONLY on a diagnosed density-model
mis-specification, never to green pass cells (rider-4 / anti-Goodhart).

**elite_pack classification correction (Disc #11):** the run's raw report initially labeled elite_pack
"percentile-fit" (the legacy `gauntlet_sim.py:505` comment). r3a-step7 VERIFIED it density-anchored
(mob_count=3, `_ELITE_ARENA` 28×28, KILLS_ONLY; the 2026-07-07 re-lock did not touch its
mob_count/geometry). Corrected in the deliverable + math note §1; the band STANDS at (8.26, 28.13).

---

## 2. FOUR-COHORT PER-COHORT DELTA MAP (arm G − arm S, KPM; all four cohorts distinct)

| cohort | open_arena | chokepoint | magic_pack | elite_pack | dense_cell | boss_adds | mini_boss |
|---|---|---|---|---|---|---|---|
| DPS-min-maxer | +4.29 | +6.48 | +10.96 | +12.70 | +14.00 | +24.51 | +0.00 |
| Balanced | +4.85 | +16.27 | +6.81 | +12.34 | +13.89 | +11.26 | +52.68 |
| Defensive | +0.00 | +0.00 | +4.89 | +11.90 | +0.00 | +3.14 | +43.52 |
| Hybrid | +6.74 | +16.52 | +7.03 | +11.32 | +14.08 | +11.32 | +52.24 |

Four DISTINCT per-cohort deltas — acceptance criterion 4 satisfied (NOT the single-cohort trap; the
w5g1 path iterates COHORT_ARCHETYPES natively). ALL deltas ≥ 0 (gear raises clear-speed KPM, as
designed). Defensive shows +0.00 on several clear shells — its gear tilt adds no offensive throughput
there, so no KPM shift (a genuine cohort-tilt signature, not a plumbing gap; the offensive cohorts move).

**Supplementary Leg-i cell-grain per-cohort per-FAMILY map** (`--all-cohorts-arm-g` @14001;
`output/leg_i_cell_grain/c3_leg_i_all_cohorts_14001.json`), the F-grain view via DERIVED_BARS:

| cohort | F1 (dense_cell) | F2 (open_arena) | F3 (boss) | F4 (escape_lane) |
|---|---|---|---|---|
| DPS-min-maxer | −10.45 | +10.02 | +1.07 | −3.02 |
| Balanced / Defensive / Hybrid | −10.11 | +12.06 | +1.07 | −3.11 |

(The F-grain cohorts near-agree because certification_gear's tilt is ADDITIVE on a shared +35% core —
band-invariance by design, per the C2 build. The w5g1 per-SHELL map §2 is the band-refit input; the
Leg-i F-grain map is the supplementary cross-view.)

---

## 3. TWO-COMPONENT DELTA ATTRIBUTION (INFO-1 — Gate-1 amendment 2, entangled-fallback APPLIED)

The re-fit delta is read against the largely **Path-3 geometry-blind** pre-E1 baseline (INFO-1,
verified `7956484`): pre-E1, `small_aoe`/`large_aoe` were never valid `_RICH_TO_SPATIAL` keys, so ~2/3
of the amplitude space was geometry-blind (B11 dead behind an invalid-key collapse). The band shift has
two components:

- **(a) Path-3-correction** — B11 mechanics now FIRE on the ~2/3 amplitude space previously
  geometry-blind.
- **(b) geometry-variety** — 3-shape → 11–12 distinct per-kit geometries; B11 multipliers vary
  per-skill.

**Entangled-fallback (Gate-1 amendment 2 — no false split):** these two act on OVERLAPPING amplitude
space (~2/3 of it). They are **NOT cleanly separable from the arm-G distributions alone.** I give the
bounding characterization, NOT a manufactured decomposition:
- The delta is DOMINATED by the overlap region (~2/3 amplitude) where both components act jointly.
- LOWER bound on pure geometry-variety: the ~1/3 region that was NOT Path-3-blind pre-E1 (the single
  valid collapse key) — band movement there is uncontaminated variety.
- The overlapping ~2/3 is JOINTLY attributed; no clean X%/Y% split is asserted (would be false
  precision the data does not support — Disc #12 / reframe-validity).
- **The full band shift is NOT attributed to "geometry variety"** — a material part is the correction
  of a silent degradation (Path-3). Both components named; entanglement stated.

**Operationally this matters little for the BANDS** because none of the density anchors moved — but it
matters for reading the arm-G DISTRIBUTION shift (§4): the above-ceiling mass is driven jointly by (a)
B11 now firing + (b) the +35% gear, off a baseline that was largely geometry-blind. The shift is real
and jointly-caused; do not credit it wholly to either lever.

---

## 4. DENSITY-MODEL-REVIEW FINDINGS (rider-4 — diagnose, do NOT curve-fit) — ROUTE TO gandalf/Matt

Three shells' arm-G distribution departs the density anchor ABOVE the ceiling. Per rider-4 I do NOT
move the ceiling to green the geared cells. The diagnosis:

- **The density anchors were derived at the STRIPPED clear-time intent.** The declared baseline MOVED
  stripped → geared (arm G, +35% dmg / +18% armor / +12% hp). The geared arm clears FASTER → higher
  KPM → a large fraction lands above the stripped-derived ceiling. This is the EXPECTED consequence of
  the baseline shift, NOT a band error and NOT kit non-viability.
- **chokepoint_corridor** (in-band 19.4%, 479 above-ceiling): the funnel AOE-concentration term the
  room is designed to exploit, amplified by B11-now-firing + gear, pushes most geared kits past the
  60.0 ceiling. The floor holds (0 below-floor).
- **dense_cell** (in-band 63.6%, 72 above-ceiling): GEOMETRY-ONLY band's FIRST empirical test. It
  admits the majority but a fast-clear tail rails above 102.86 — the rails-at-ceiling falsifier
  (shared with magic_pack) fires for the geared fast-clear tail.
- **elite_pack** (p25=29.03 > ceiling 28.13): the 3-mob room + gear = near-instant clear that
  SATURATES the KPM=450 instrument cap (p90 == max == 450.0). This is an **instrument-cap artifact**
  (3-mob room → tiny clear time → KPM cap), NOT a content signal.

**Two dispositions, both consistent with locked policy — Matt rules:**
1. **Rider-3 absorbs it:** above-ceiling = FLAG_PASS_OVERPOWERED → balance-review / difficulty-ladder
   input (ruling A). The bands STAND; the geared over-ceiling mass flags for review. This is the
   lowest-friction reading and consistent with the pivot's E5-C (arm G is the cert baseline; over-power
   flags, does not fail).
2. **Re-anchor at the geared clear-time intent:** if the geared baseline is the durable cert baseline,
   the density anchors could re-derive their ceilings at the GEARED clear-time window (the succession
   the pilot_policy entry (4) named). This is a density-model review, math-note-first, NOT done here.

**My recommendation:** disposition 1 (Rider-3 absorbs) for now — it is what the locked semantics
already prescribe, and the reframe-validity result (§5) says KPM still discriminates. Re-anchoring
(disposition 2) is a larger density-model-review work-unit that should fire only if Matt rules the
geared baseline durable AND the FLAG_PASS volume is judged too high to be useful as a difficulty
signal. The elite_pack KPM-450-cap is a separate instrument item (the 3-mob room may need a higher cap
or a clear-time-floor guard) — flagged, not fixed here.

---

## 5. REFRAME-VALIDITY — the falsifier does NOT fire (ruling A survives)

Registered falsifier (pilot_policy (4), `94ec548`): *if arm G compresses the KPM spread materially
toward point-mass, ruling A's KPM-as-measurement claim is re-examined.*

| shell | arm-S spread | arm-G spread | compression ratio |
|---|---|---|---|
| open_arena | 167.61 | 165.28 | 0.986 |
| chokepoint_corridor | 99.33 | 99.33 | 1.000 |
| magic_pack | 122.69 | 125.23 | 1.021 |
| elite_pack | 442.13 | 442.13 | 1.000 |
| dense_cell | 297.12 | 297.12 | 1.000 |

**Compression ratio ≈ 1.0 everywhere (0.986–1.021). Arm G does NOT compress the spread.** The falsifier
does NOT fire. Ruling A's "clear-speed KPM is THE measurement" holds under the geared baseline: gear
shifts the distribution UP but PRESERVES its spread, so KPM still discriminates. (Reframe-validity
discipline: no stripped figure is quoted as the geared baseline; "~2.4×" is not propagated.)

---

## 6. #2-FF + DISCIPLINE COMPLIANCE

- **#2-FF pre-fire PATH verification** (§4 of math note): `[C3-PREFIRE] cohort_count=4
  arm_g_differs=True max_abs_delta_kpm=0.0079 shells=2` — asserted cohort-count==4 in the FIRST log
  line (defeats the INFO-2 single-cohort trap; a bare non-zero check would not). PASS, exit 0.
- **#2-FF run banner** named both arms + the tier-1 pack-clear instrument + the E1-widened population +
  COUNT=4 cohorts + all 7 re-fit shells + Discipline #3.
- **Discipline #1:** math note landed FIRST; corrected in-flight for the r3a-step7 elite_pack finding.
- **Discipline #3:** arm S then arm G at the SAME w5g1 deterministic seed (base_seed_t1/t2 are
  config/cohort/enc functions — arm-invariant). No parallel same-seed regen.
- **Discipline #1.1 / #2.1:** resource-bounds projected; tier-1-only band-fit decision (math note §8 —
  the band reads tier_1_kpm, tier-2 is the WR gate, not the band-fit input) collapsed 110,880 fights
  (10.5 hr, over budget) → 36,960 fights (39 min actual). Smoke rehearsal measured per-fight wall first.
- **Discipline #12:** the declared-baseline MOVE (stripped → geared) is framed, not buried; routed for
  the succession decisions-log entry.
- **Instrument guard:** affixed mobs / content encounters never entered the gauntlet — the four-family
  clean instrument only.

---

## 7. WHAT THIS RUN DOES / DOES NOT DO

- **DOES:** re-validate the seven KPM bands at the arm-G declared baseline on the E1-widened
  population; produce the four-cohort per-cohort delta map; attribute the two-component delta (INFO-1
  entangled fallback); test reframe-validity (falsifier does not fire); surface three density-model
  findings + one instrument-cap finding.
- **DOES NOT:** move any band (density anchors invariant to E1; rider-4); un-gate emission (C4 is
  GATE1-bound); resolve the density-model findings (routed for Matt ruling §4); change the four-family
  judge (UNAMENDED); touch the emitter (E1 landed); change any telemetry/star-lord schema (all
  in-JSON gamora-side, no MIGRATION).

**Surface-ledger C3 flips ✓ on Matt-seen** (the bands are re-validated at the declared baseline; the
current set STANDS as the certification instrument). The density-model-review findings (§4) are a
follow-on ruling, not a blocker to the C3 flip.

---

**Signed:** gamora, 2026-07-08. First content-bearing per-axis certification readout under the
Matt-ratified full-run pivot. Routed to Matt via gandalf.
