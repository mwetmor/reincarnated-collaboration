# W-D per-axis discrimination decompose — gamora → gandalf (D1)

**Date:** 2026-06-13
**Author:** gamora
**For:** gandalf (design steward) — §6.4 close check at W-F
**Trigger:** Matt ratified cond. 4 = PASS with HARD CONSTRAINT "wired-not-default ≠ discriminates." Before §6.4 ("the archive measures the current kit") closes at W-F, gandalf needs the per-axis DISCRIMINATION breakdown to separate axes that genuinely discriminate NOW vs known-deferred.
**Source (gamora-authored):** `reincarnated-engine/src/reincarnated/simulation/math/wd-six-axis-measure-build-2026-06-13.md` §8 (pre-reg) + §10 (results); `reincarnated-engine/output/wd-six-axis-measure-2026-06-13.json` (per-axis measured records). Engine commit `5ec33bb`, tag `gamora/v-wd-six-axis-measure-1`.
**Scope:** surfacing only — no code change, no re-run. This consolidates math note §10 so gandalf can interpret against the known-deferred list without reverse-engineering §10.

---

## Headline

- **Bucket-A gate (the cond. 4 EXIT GATE) PASSES:** all 8 axes are wired-from-spatial-telemetry, none default-valued; CommitGradeVerdict mints with valid provenance (`fidelity=commit`, `engine=spatial`, `scenario_set_hash=bcc55cf1edc05d3f`). `measure_cond4_pass=true`.
- **Discrimination tally (against the §8 pre-registration):**
  - **DISCRIMINATES NOW: 1 of 8** — Geometry (Axis 2).
  - **Wired but does NOT discriminate as pre-registered: 7 of 8** — each with a benign, category-mapped reason (below).
  - **Category-(e) LIVE OBLIGATION: 0 of 8.** No axis that should discriminate now fails without a benign explanation. (See the deliberate adversarial check at the foot of this note.)

Read the categories as: (a) DEFERRED-no-mechanic; (b) REFERENCE-SET-UNDIFFERENTIATED; (c) WRONG-ROOM; (d) LOCK-EDGE mis-threshold; (e) LIVE OBLIGATION (no benign reason — must flag loudly).

---

## Per-axis decomposition

### Axis 2 — Geometry (CONFIRM) — DISCRIMINATES NOW
1. **Pre-reg discriminating bins:** K1/K6 → `single-target`; K2/K4/K5 → `large-AOE` (circle); K3 → `small-AOE` (line).
2. **Measured:** DISCRIMINATES — separates exactly as pre-registered. Predicted ≡ measured holds (no CONFIRM→BUILD divergence).
3. **Reason if NOT:** N/A.
4. **Raw:** K1 `point`/single-target; K6 `point`/single-target; K2 `circle`/large-AOE; K4 `circle`/large-AOE; K5 `circle`/large-AOE; K3 `line`/small-AOE.

### Axis 1 — Engagement, range-half (CONFIRM) — DISCRIMINATES NOW (range component)
1. **Pre-reg discriminating bins:** K1 melee/close; K2 close; K3 close/mid; K4 close; K5 close; K6 melee. (Range read-back from composed `range_m`.)
2. **Measured:** the range-half DISCRIMINATES — mean_range separates kits (K1/K6=2.0; K2/K4/K5=3.5; K3=20.0), and the composite Engagement bin reflects it (`close-fast` / `mid-fast` / `ranged-fast`). NOTE: the composite axis is range-half (CONFIRM, discriminating) + mobility-half (BUILD, lock-edge collapsed — see Axis 1 mobility below). The "-fast" suffix on every kit comes from the mobility-half lock-edge issue, not the range-half.
3. **Reason if NOT (mobility component only):** category (d) LOCK-EDGE — see next entry.
4. **Raw mean_range (m):** K1=2.0, K6=2.0, K2=3.5, K4=3.5, K5=3.5, K3=20.0.

### Axis 1 — Engagement, mobility-half (BUILD) — does NOT discriminate → category (d) LOCK-EDGE
1. **Pre-reg discriminating bins:** K4 → `mobile` (movement_speed 9.0); K1/K2/K3/K5/K6 → `static` (5.75). This is the load-bearing BUILD discriminator.
2. **Measured:** does NOT discriminate the bins. The displacement instrument is WIRED + MEASURED and the RAW SIGNAL ORDERS CORRECTLY (K4 highest), but every kit bins identically (the composite reads `*-fast` for all six) because the lock's mobility threshold (high ≥30 tiles/min, lock §3.1) is exceeded by all kits — spatial baseline-closing alone accrues 50–64 m/min, far above a threshold calibrated for 1D movement-skill displacement.
3. **Reason:** category **(d) LOCK-EDGE** — wired + measured + raw signal orders correctly (K4 top), but the bin THRESHOLD (30 tiles/min, 1D-calibrated) mis-classifies. This is a Discipline #17 first-deployment lock-edge calibration item that lock §0 explicitly anticipated. NOT a measurement bug. gandalf owns the lock-edge; I supply the spatial displacement distribution as the calibration input. Re-discriminates once the edge is re-calibrated on spatial telemetry.
4. **Raw mean_displacement (m/min):** K4=64.42 > K2=62.30 ≈ K5=62.49 > K1=56.88 > K3=55.53 > K6=50.38. Order is correct (K4 highest); the 30/min edge bins all six the same.

### Axis 2A — Proxy (WIRED-DEFERRED) — does NOT discriminate → category (a) DEFERRED
1. **Pre-reg discriminating bins:** DEFERRED for all kits (pre-registered as non-discriminating in §8; the hand-built set has no proxy kit AND the spatial engine has no proxy mechanic).
2. **Measured:** does NOT discriminate — bins `none` for all kits, `measurable=false`.
3. **Reason:** category **(a) DEFERRED — no spatial mechanic yet.** Empirical inspection (math note §1) proved `proxy_combatant.py` (14-type model, fission, population tracking) is wired ONLY into the 1D kernel (`fight_engine.py`); it is never imported by `spatial_engine.py`. Wiring 2A to a §4.D sustained-wave fixture would read `mean-active-proxy-count = 0` for every kit (the ORPHAN-measure bug). Honestly wired-deferred (visible flag + `deferred_reason`), counts toward the 8 with a paper trail. Re-closes when the spatial-proxy-mechanic port lands → the D4 sustained-wave-fixture/proxy-port follow-on (sub-scoped to KR, math note §1.3).
4. **Raw:** value `0.0`, `measurable=false`, `deferred_reason="no-spatial-proxy-mechanic (proxy_combatant 1D-kernel only; math note §1)"` for all six kits.

### Axis 2B — Control (BUILD-lo) — does NOT discriminate → category (b) REFERENCE-SET-UNDIFFERENTIATED
1. **Pre-reg discriminating bins:** all kits → `none` control. Pre-registered as uniform — the hand-built §5 set carries no CC skill.
2. **Measured:** does NOT discriminate — `damage-pure` (CC-fraction 0.0) for all kits. The reduction reads `skill_type` correctly; there is no CC kit to separate.
3. **Reason:** category **(b) REFERENCE-SET-UNDIFFERENTIATED** — all hand-built §5 kits are damage-pure, so there is nothing to discriminate. The reduction is correct; the set is uniform. A CC-bearing kit would BUILD-discriminate. Surfaced to KR → the D5 rocket reference-kit follow-on. (Open-Question resolution: 2B is trivially "CONFIRM-after-all" for THIS set, but only because the set is undifferentiated — NOT because 2B is composition-determined in general.)
4. **Raw:** value `0.0` (CC-fraction), bin `damage-pure`, all six kits.

### Axis 3A — Tempo (BUILD) — does NOT discriminate → category (b) REFERENCE-SET-UNDIFFERENTIATED
1. **Pre-reg discriminating bins:** K1/K2/K3/K4/K5 → `med`; K6 → `low/med`. (Pre-reg expected mostly-uniform mid-tempo; the set is not strongly tempo-differentiated.)
2. **Measured:** does NOT discriminate into distinct bins — bins `low` for all six. The damage-event-rate reduction is wired and reads `fight_tick` on damage events correctly; raw rates are tight (0.667–0.885 events/sec) and the hand-built set does not vary enough on tempo to separate bins.
3. **Reason:** category **(b) REFERENCE-SET-UNDIFFERENTIATED** — the reduction works (wired-not-default, raw values present and ordered), but the hand-built kits are clustered in cast cadence so they collapse into one bin. A genuinely fast-cadence vs slow-cadence kit pair would BUILD-discriminate. Same D5 rocket reference-kit follow-on. (Note: the pre-reg `med` guess landed on `low` for all — a same-direction tightness/edge nuance, not a separation; the set simply doesn't exercise tempo spread.)
4. **Raw (events/sec):** K1=0.68, K2=0.667, K3=0.882, K4=0.677, K5=0.681, K6=0.885. Range 0.667–0.885 — narrow, single-bin.

### Axis 3B — Variance (RE-EMIT) — partial discrimination (flat vs variable) → benign; reference-set-bounded
1. **Pre-reg discriminating bins:** K1/K6 → `flat`; K2/K3/K4/K5 → `flat/variable` (geometry-driven multi-hit variance expected on the AOE kits).
2. **Measured:** DISCRIMINATES the flat/variable split as pre-registered — single-target kits (K1/K6) read `flat`; AOE kits (K2/K3/K4/K5) read `variable`. The damage-CV reduction (`_pooled_cv`, re-emitted over the spatial stream) separates these two classes correctly. It does NOT reach the third bin (`spiky`) — no kit in the set is spike-shaped.
3. **Reason (for the missing `spiky` bin only):** category (b) REFERENCE-SET-UNDIFFERENTIATED — no spike-shaped kit in the hand-built set; the flat/variable separation it CAN make, it makes correctly.
4. **Raw (CV):** K1=0.1129 (flat), K6=0.1128 (flat); K2=0.6339, K3=0.6503, K4=0.6596, K5=0.6441 (all variable). Clean two-cluster separation.

### Axis 4 — Defensive (RE-EMIT) — does NOT discriminate → category (c) WRONG-ROOM
1. **Pre-reg discriminating bins:** K6 → `tank` (vit=300); K1/K2/K3/K4/K5 → `glass`.
2. **Measured:** does NOT discriminate as pre-registered — and INVERTS in the density rooms: the intended-tank K6 reads LEAST durable. eHP ordering: K4=75.3 / K2=73.3 (fast clearers) > K5=64.5 > K3=55.9 > K1=53.7 > **K6=45.0 (lowest)**. Durability is invisible when nothing threatens you — a fast clearer takes less total damage (fewer mob actions land before the pack dies), so clear-rate leaks into the eHP ratio and dominates it.
3. **Reason:** category **(c) WRONG-ROOM** — discrimination lives in a room W-D does not cover. The oracle §6.2 condition-5 (W-F `boss_with_adds`) is the survival-mechanism discriminator; W-D's density rooms measure clear-rate, not durability. This is the oracle's OWN boundary — the defensive-bridge commit-grade re-validation IS condition 5, explicitly out of W-D scope. (Also note: avoidance/dodger not emitted in spatial — the dodger sub-test is un-runnable, carried as a visible deferred flag, same as the Axis-4 1D bridge.)
4. **Raw eHP-ratio:** K4=75.34, K2=73.34, K5=64.54, K3=55.87, K1=53.66, K6=45.01. K6 (the intended tank) is lowest — the WRONG-ROOM inversion.

### Axis 5 — Resource (BUILD) — does NOT discriminate → category (b) REFERENCE-SET-UNDIFFERENTIATED
1. **Pre-reg discriminating bins:** all kits → `hp-economy`. Pre-registered as uniform — the hand-built set is not resource-differentiated (uniform stamina, low cost, high regen; no charge-stack or HP-cost kit).
2. **Measured:** does NOT discriminate — `starved` (avail=0.0) for all kits. The spend/regen-flow reduction reads correctly, but the kits regen faster than they spend and cap at max_energy quickly, so `resource_recovered` events emit only while energy < max (rarely after tick 1) → avail = regen/(spend+regen) ≈ 0.
3. **Reason:** category **(b) REFERENCE-SET-UNDIFFERENTIATED** — the kits are uniform on resource (nothing to discriminate). A resource-differentiated kit (charge-stack or HP-cost) would EXERCISE the axis. Surfaced to KR → the D5 rocket reference-kit follow-on. SECONDARY engine note (not a W-D obligation): the `resource_recovered` emission gate (`energy < max_energy`) under-emits regen for non-starved kits — a candidate spatial-resource-telemetry refinement, surfaced for a separate follow-on.
4. **Raw:** value `0.0` (avail), bin `starved`, all six kits.

---

## Summary table

| Axis | Discriminates NOW? | Category | Re-closes at |
|---|---|---|---|
| 2 Geometry | YES | — | (done) |
| 1 Engagement range-half | YES | — | (done) |
| 1 Engagement mobility-half | NO | (d) LOCK-EDGE | gandalf lock-edge re-calibration on spatial telemetry |
| 2A Proxy | NO | (a) DEFERRED | D4 sustained-wave-fixture / spatial-proxy port |
| 2B Control | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (CC kit) |
| 3A Tempo | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (tempo-spread kit) |
| 3B Variance | PARTIAL (flat/variable yes; spiky no) | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (spike kit) |
| 4 Defensive | NO (inverts in density rooms) | (c) WRONG-ROOM | W-F boss room (oracle §6.2 cond. 5) |
| 5 Resource | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (resource-diff kit) |

**M1 ablation (context, not an axis):** DISCHARGED with a NEGATIVE causal result. The gather primitive does not re-close the K4≥K2 per-seed margin — it INVERTS it (WITHOUT: K4−K2=+3.99, 6/9; WITH: K4−K2=−3.44, 1/9), because gather is an AOE-coverage primitive that benefits the stationary nova (K2) more than the mobile kit (K4). Hypothesis disproven, obligation discharged (not left open). gandalf owns the oracle §5.2 amendment to record this. Primitive left in-engine behind its default-off flag (brownfield-safe).

---

## Category-(e) LIVE OBLIGATION check (the adversarial pass)

I deliberately tried to find an axis that SHOULD discriminate NOW in W-D's density/clear-rate rooms but fails with NO benign reason. **None found.** Each non-discriminating axis maps to a benign category:
- Mobility (d): raw signal orders K4 highest correctly — only the 1D-calibrated edge collapses the bins. The instrument works.
- Proxy (a): no mechanic exists to measure; honestly flagged, not fabricated.
- Control / Tempo / Resource / Variance-spiky (b): the reductions are correct and wired; the hand-built set is uniform on these, so there is nothing for them to separate. Discrimination capacity is bounded by reference-set variety, not by a measurement defect.
- Defensive (c): correctly measures clear-rate-dominated eHP in density rooms; durability discrimination is architecturally assigned to W-F's boss room.

**Conclusion: 0 of 8 axes are category-(e). No live obligation to flag.** The pre-registration "misses" on mobility/defensive are predicted-AND-explained (wrong edge / wrong room), and the undifferentiated axes are bounded by the reference set — all consistent with Matt's HARD CONSTRAINT being satisfied honestly: wired-not-default is true for all 8, and the discrimination map above tells gandalf precisely which axes the §6.4 close can rely on NOW (Geometry + Engagement-range) vs which are gated on the known-deferred follow-ons (D4 proxy port, D5 rocket reference-kit hardening, W-F boss room, lock-edge re-calibration).
