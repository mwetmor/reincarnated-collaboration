# Aware-Fighter Ablation — Trace Investigation (Mechanism Diagnosis)

**Author:** named-gamora (simulation seam) · **Date:** 2026-07-22
**Authority:** gandalf RUN-CONDUCTOR (trace-investigation work order) · **Engine:** FROZEN at `2f43045`
**Gate under diagnosis:** aware-fighter ablation, commit `116aa896`, verdict-input clear-guard TRIPPED (14 mismatches).

> **This is MECHANISM DIAGNOSIS of a completed, sealed gate. It is explicitly NOT a re-scoring.**
> No gate-verdict word (PASS/FAIL/PARTIAL) is asserted here — that is the conductor's synthesis. This
> file establishes FACTS about the mechanism behind the clear-guard trip. The gate's frozen bar and
> its verdict state are untouched by everything below, including §4.

---

## 0. What the on-disk dumps contained (dump-contents finding)

The two full-run JSONs (`…-blind-full.json`, `…-aware-full.json`) are **SUMMARY-ONLY**. Each is
`{arm, mode, engine_src, engine_bound, policy_config, n_cells, results}` where `results` is a dict of
256 per-fight records keyed `island|tier|kit|composition|seed`. Each record carries:
`player_damage_taken, elapsed_s, all_mobs_killed, winner, player_kill, mobs_killed, total_mob_count,
triple{mobs_killed,total_aoe_hits,player_damage_total}, trace_len`.

`trace_len` is an **integer count** — the decision-trace **bodies are NOT embedded**, and there is no
per-tick HP, no chosen-target record, no distance profile. The engine's `run_spatial_fight()` *does*
build the `(tick, chosen_target_id, movement_intent)` trace when `trace_decisions=True` (it is
returned under `raw["decision_traces"]`), but the gate runner captured only `len(trace)` to disk.

**Consequence:** questions 2a–2d (switch rate, time-between-kills, unfinished-mob HP, chosen-target
distance) cannot be answered from the dumps. They require the trace bodies + richer per-decision reads.
→ diagnostic re-observation (§1).

---

## 1. Method (incl. diagnostic re-runs) + engine-frozen attestation

**Re-observation, not new gate data.** The engine is deterministic; re-running a cell at the same
hash/seed/config reproduces the fight bit-for-bit. I re-ran a **diagnostic subset** with full trace
capture + a read-only instrument, then verified the re-run reproduced the sealed gate numbers exactly.

**Diagnostic script:** `2026-07-22-aware-fighter-ablation-trace-diagnostic.py` (collab notes only).
- **Frame logic REUSED VERBATIM** from the gate runner via file-path module load of the W3′ gate
  machinery (`2026-07-22-tier3-w3prime-gate.py`) — same selection → formation → scenario → cell build,
  same seeds `{20260722,20260723,20260724,20260725}`, same `BLIND_CONFIG` / `AWARE_CANDIDATE_CONFIG`
  imported verbatim.
- **Instrument = read-only monkeypatch applied from the collab-notes script** (zero engine edits): it
  wraps `spatial_engine._get_player_primary_target` with a recorder that calls the REAL selector, then
  records pure READS (chosen target's `entity_id`/distance/`hp`/`max_hp`; alive-set size; per-mob HP
  snapshot; nearest-alive distance). The wrapper returns exactly what the real selector returns → fight
  trajectory byte-identical to the gate. Only the player decision (engine :3920) is intercepted; ally/
  mob selection (`_policy_choose_target` at :1957/:3137/:3239) is untouched.
- **9 diagnostic cells** × 2 arms × 2 compositions × 4 seeds = **144 fights, SEQUENTIAL** (Discipline
  #3). corpus.db opened READ-ONLY. Cells: ranged-direct-volley FAIL-all-4 (`IV|high|
  poe1-kinetic-fusillade`, `I|high|d2-bowazon`); ranged-DoT aware-cleared-MORE (`II|high|
  poe1-caustic-arrow`, `I|high|d2-poison-javazon`); melee-volley big-delta-no-trip (`I|low|
  poe1-frost-blades`); ranged-volley medium-delta-no-trip contrast (`II|high|poe1-spark`); clean
  controls (`III|high|gd-primal-strike-vindicator`, `I|high|d2-frenzy-barb` delta 0.00; `II|high|
  poe1-armageddon-brand` delta +34).

**Determinism / non-perturbation check (Discipline #11):** all **144/144** re-run fights reproduced
the sealed gate's `player_damage_taken` (|Δ| = 0.0), `mobs_killed` (Δ = 0), and `trace_len` exactly.
The instrument is provably side-effect-free w.r.t. engine state; the diagnostic data is valid.

**Engine-frozen attestation (both beats of the diagnostic run):**
- HEAD `2f43045` at `run_start` AND `run_end` (unmoved).
- Tracked `*.py` diff under `src/reincarnated/`: **EMPTY** at both beats.
- Only tracked delta in the engine repo is the pre-existing exempt `src/reincarnated/output/
  leg3_pilot_section8a1_band_measurement.json` (star-lord's seam; RC-1 (iii) exempt) — **not touched
  by this investigation.**

Output dump (untracked, regenerable): `2026-07-22-aware-fighter-ablation-trace-dump.json`.

**Structural note that governs the whole read (empirical inspection):** the W3′ methodology builds a
**neutral martial fighter from the BC cell** (`_build_martial_player_class`), not the named kit's real
skills — every cell gets the same "Wind Chain A/B/C" skill template; the DIFFERENTIATION is entirely in
the BC cell (`range_val`) + the scenario formation + the kit's `draft_family` label. This makes each
fight a pure function of **(cell-range-band, formation-class, delivery-family)**, so the 32 cells
**collapse to 15 distinct encounter-delta values** (cells sharing that tuple are bit-identical). The
"kit" is a label on an equivalence class. This is why `d2-bowazon` and `poe1-kinetic-fusillade` produce
byte-identical intake/kills/traces across all seeds and both arms.

---

## 2. Per-question findings (2a–2d)

All numbers below are the deterministic re-run values (= sealed gate values). Encounter arm unless
noted. "Detour" = per-decision `chosen_distance − nearest_alive_distance` (BLIND ≡ nearest-first ⇒ its
detour is exactly 0.0 every decision — the byte-equality of the fast path, confirmed).

### 2a. Target-SWITCH rate + chosen-not-nearest rate
The single quantitative fingerprint of the policy difference:

| cell (class) | arm | switch-rate/dec | % chosen ≠ nearest | detour mean (m/dec) |
|---|---|---|---|---|
| bowazon / kinetic-fusillade (ranged-direct) | BLIND | 0.214 | **0%** | **0.00** |
| bowazon / kinetic-fusillade (ranged-direct) | AWARE | 0.109 | **57–59%** | **0.59** |
| caustic-arrow / poison-javazon (ranged-DoT) | BLIND | 0.19–0.375 | 0% | 0.00 |
| caustic-arrow / poison-javazon (ranged-DoT) | AWARE | 0.429 | 39% | 0.19 |
| frost-blades (melee-volley) | BLIND | 0.120 | 0% | 0.00 |
| frost-blades (melee-volley) | AWARE | 0.083 | 11% | **0.16** |
| clean controls (proxy/emplacement) | AWARE | +0.03–0.04 vs blind | 17–24% | 0.5–0.6 |

**Finding:** AWARE picks a **non-nearest** target 39–59% of the time; BLIND, 0%. The `distance_normalized`
term at 1/6 weight cannot hold commitment against the five geometry terms. Note switch-RATE alone is
ambiguous (AWARE can have LONGER dwell-runs while committing to the wrong target — see bowazon below);
**detour** is the clean signal, and it is strictly 0 for BLIND, strictly positive for AWARE, everywhere.

### 2b. Time-between-kills / kills-vs-tick shape
Kill events reconstructed from alive-set drops, aligned to engine ticks. The decisive shape is the
**mass-AOE burst**:

- **BLIND ranged-direct (bowazon, seed 23):** kills 0→1→2→3 slowly (ticks 10/24/38), then **+25 in ONE
  tick (tick 53)**, then +4/+5/+1 → 40. Mechanism: commit to nearest → walk into the pack centroid →
  one positioned AOE clears the cluster. First-kill tick 10, last-kill tick 55.
- **AWARE ranged-direct (bowazon, seed 23):** kills reach cumulative **3 and stay flat** through 100%
  of decisions (kills@[25/50/75/100% of decisions] = [0,1,2,3]). The mass-burst **never happens** —
  the detour keeps the player off any stable cluster; the player dies (winner=`monster`) before the
  positioned AOE can land. Last-kill tick 41 (fight ends ~tick 53 by death).
- **Frost-blades (melee):** BOTH arms get the burst (BLIND +17 @ tick 42; AWARE +19 @ tick 45). AWARE
  simply needs EXTRA later bursts (+6 @ tick 79, +1 @ tick 95) to mop up stragglers it detoured away
  from → +45% duration but a full clear.

### 2c. Unfinished-mob HP distribution at fight-end (spread-thin signature)
**The signature is stronger than "many mobs at mid HP."** At the last decision of every failing fight,
the surviving mobs are at **≈100% HP** (mean HP-frac = 1.00; 0 mobs in the 0–80% band; all survivors in
the >80% band). Examples: AWARE bowazon leaves **37 mobs at full HP**, 3 dead; BLIND caustic-arrow
seed-23 (stuck 16/40) leaves 37 at full HP.

**Mechanism this reveals:** the neutral AOE **one-shots** any mob inside its footprint (single-hit kill)
and leaves everything outside it **untouched at full HP** — there is no chip/attrition. So "spread thin"
here is *geometric coverage*, not *diluted per-target damage*: when the aware detour de-centers the
player from the pack, the AOE footprint covers fewer mobs, and the uncovered mobs stay pristine. A
`wasted-dwell` measure (chosen target already ≤5% HP) returned **0/N in every fight** — confirming mobs
never sit at low HP; they are full until the AOE deletes them.

### 2d. Chosen-target distance profile
Mean chosen-target distance at choice time (encounter):

| cell (class) | BLIND mean chosen-dist | AWARE mean chosen-dist | AWARE mean nearest-dist |
|---|---|---|---|
| bowazon/kinetic-fusillade (ranged-direct) | 5.4 m | 6.1–6.3 m | 5.5–5.7 m |
| caustic/javazon (ranged-DoT) | 1.7 m | 1.9 m | 1.8 m |
| frost-blades (melee-volley) | 4.5 m | 4.1 m | 4.0 m |
| primal-strike/frenzy (control) | 2.2–2.3 m | 3.1–3.2 m | 2.5–2.6 m |

**Finding:** the aware chosen-target is consistently FARTHER than nearest (the detour), but the raw
gap is small (~0.5–0.8 m). The catastrophe is **not** driven by picking a *distant* target — it is
driven by **oscillation** (e.g. bowazon seed-23: player commits to `mob_0` closing 14.8→11.9 m, then at
dec 8 switches to `mob_39` at 18.7 m when nearest is 13.4 m, walks toward it for 4 ticks, then bounces
back). The player closes on nobody, so it never reaches the pack-centroid AOE moment. Distance magnitude
is a symptom; the load-bearing effect is loss of commitment.

---

## 3. Kit-class cross-tab (question 3)

Classified all 32 cells by `draft_family` × `range_val` (cell-range band). Mean per-cell encounter
intake delta = `blind − aware` (positive ⇒ aware took LESS intake):

| class | n cells | mean enc Δ (blind−aware) | median enc Δ | enc mismatches | baseline mismatches |
|---|---|---|---|---|---|
| **ranged-direct-volley** | 3 | **−3638.4** (aware WORSE) | −4852.6 | **2** | **2** |
| **melee-volley** (frost-blades) | 3 | **−2677.2** (aware WORSE, but clears) | −2677.2 | 0 | 0 |
| **ranged-DoT** (DOT-AILMENT) | 4 | **+1382.9** (aware BETTER) | +1382.9 | **2** | **2** |
| melee-direct (MELEE-STRIKE/WHIRLWIND) | 7 | +81.5 (~neutral) | 0.0 | 0 | 0 |
| proxy/emplacement (AURA/TOTEM/TRAP/BEAM) | 15 | +34.3 (~neutral) | +34.2 | 0 | 0 |

**The sign flips exactly on delivery-class, and ALL 8 mismatched cell-slots are RANGED:**
- **ranged-direct-volley** → aware substantially WORSE. These are the guard-tripping FAIL-all-4 cells.
- **ranged-DoT** → aware substantially BETTER. These are the bidirectional aware-cleared-MORE cells.
- **melee** (direct or volley) and **proxy/emplacement** → near-neutral or aware-worse-but-still-clears
  (never trips the guard).

**Frost-blades anomaly, resolved (its actual delivery):** `range_val = melee`, cell-range band =
`melee`, `draft_family = MULTI-PROJECTILE-VOLLEY`, element cold. It is a **melee-reach AOE** kit. Its
−2677 delta is real (aware takes +30% intake) but it does NOT trip the guard because it **clears 40/40
in both arms** — the melee fighter's detour is small (0.16 m/dec) so it never leaves the pack's reach;
its AOE keeps landing; it just needs more time (7.5 s → 10.9 s, +45%) to mop up. Contrast the ranged
volley (`poe1-spark`, −1210, no trip) which fails-to-clear in BOTH arms (12/40 vs 13/40) → no
disagreement → no guard trip. **Guard trips require the arms to DISAGREE on clear**; that only happens
where BLIND's baseline was a full clear that the aware detour breaks (ranged-direct), or where AWARE
repairs a BLIND stall (ranged-DoT).

---

## 4. Clean-cell-only aggregate intake margin — **MECHANISM DIAGNOSTIC ONLY**

> **This §4 number is a mechanism diagnostic, not a re-scoring; it does not touch the gate verdict
> state, which remains the conductor's.** It is reported because the work order asks for it, with the
> caveats that make it non-load-bearing.

Restricting to the **clean set** = encounter cell-seeds where BOTH arms cleared 40/40 (no
clear-outcome confound): **18 of 128** encounter fight-cells qualify.

- `Ibar_blind_clean` = 10865.89 · `Ibar_aware_clean` = 12178.84 · abs margin (blind−aware) = **−1312.94**
  · **M_rel = −12.08%** (aware took MORE intake on the clean set).

**Two caveats that make this unrepresentative:**
1. **Biased subsample.** Only 18/128 cells clear both ways; 110 are excluded precisely because a clear
   differed. The clean set is dominated by exactly the two classes with large deltas — it is not a
   random slice of the frame.
2. **Class-confounded.** Broken out: melee-volley (n=12) M_rel = **−29.71%**; ranged-DoT (n=6) M_rel =
   **+9.71%**. The −12% aggregate is the frost-blades melee-volley class outvoting the DoT class by
   count, not a uniform effect. Reading a single scalar off this set would launder a class-regime
   difference into a false "overall" number.

---

## 5. Seed-20260723 note (question 5)

**Formations are seed-invariant.** BLIND bowazon's chosen-target sequence for the first 5 decisions is
IDENTICAL across all four seeds (`mob_39, mob_0, mob_0, mob_0, mob_0`); mob spawn positions do not
depend on seed. The AWARE bowazon first-10-decision trajectory is likewise identical across all seeds —
yet the outcome diverges (3/40 on seed-23 vs 28/40 on the others). **What differs between seeds is only
the combat RNG (mob attack timing / hit resolution), which decides WHEN the player dies — not WHERE the
player targets.**

- **Encounter ranged-direct:** every seed's AWARE bowazon ends `winner = monster` (player death). Seed-23
  is simply the seed whose death RNG lands during the aware detour's worst window, catching the fight at
  cumulative-3 kills instead of cumulative-28.
- **DoT flip is a BLIND stall being repaired, concentrated on seed-23:** BLIND caustic/javazon at
  seed-23 dies at 16/40 (elapsed 4.3 s, winner=monster) because it glues to one target (dwell-runs mean
  4.9, long) while the pack overwhelms it; AWARE's frequent switching (dwell-runs mean 2.3, 25 runs)
  spreads the DoT and clears 40/40. On the other three seeds BLIND survives, so no flip.
- **All 4 matched-baseline mismatches are seed-23** for the same reason: baseline is geometry-sparse, so
  AWARE ≈ BLIND (both clear 40/40) on seeds 22/24/25; only seed-23's death RNG kills the aware player
  (18/40, winner=monster) before it grinds through the more-spread baseline.
- **Seed-23 is NOT globally anomalous:** its aware-encounter aggregate intake (15111.7) is the
  2nd-LOWEST of the four seeds (range 14993–15189). The seed effect is entirely localized to specific
  cells' clear-outcome flips, not a global intake shift — consistent with the tiny SD_seed.

---

## Hypothesis verdict-of-fact

**Conductor's hypothesis:** *equal-weight dilution of the distance term (1/6 in AWARE vs 1.0 in BLIND)
breaks target-COMMITMENT for direct-damage ranged kits — fire spreads across the pack, no mob dies
quickly, packs survive longer, player eats catastrophic intake tails; the SAME spread HELPS DoT-spread
kits where BLIND wastes hits re-poisoning the already-poisoned nearest target; kit-class-dependent
regime change.*

### VERDICT: **CONFIRMED — with one mechanism correction on the "how."**

**Confirmed with numbers:**
- The **dilution is real and is the sole mechanism**: `AWARE_CANDIDATE_CONFIG` uses `distance_normalized`
  (min-max → [0,1]) at weight 1.0 among six equal terms ⇒ effective 1/6 influence, vs BLIND's raw
  `-distance` at weight 1.0 as the sole argmax key. The behavioral fingerprint is **detour = 0.00 m/dec
  (BLIND) vs 0.16–0.61 m/dec (AWARE)** and **% chosen-not-nearest = 0% (BLIND) vs 39–59% (AWARE)**.
- **Commitment IS broken for direct-damage ranged kits** (ranged-direct-volley, mean Δ **−3638**, aware
  WORSE; the FAIL-all-4 guard-trippers). Packs survive: aware leaves **37/40 mobs at full HP**; the
  mass-AOE burst (+25 kills in one tick for BLIND) **never fires** under AWARE. Duration +6.6% overall
  (Ī: 14730.75 → 15116.08 confirmed).
- **The SAME spread HELPS DoT kits** (ranged-DoT, mean Δ **+1383**, aware BETTER; the aware-cleared-MORE
  cells). BLIND stalls on one target and dies; AWARE's switching (dwell-runs mean 2.3 vs BLIND 4.9)
  spreads the ailment and clears.
- **Kit-class-dependent regime change is exact:** sign flips on delivery-class, ALL 8 mismatched
  cell-slots are ranged; melee + proxy/emplacement are near-neutral.

**Mechanism correction (Discipline #12 framing — state the how precisely, don't bury it):** the
hypothesis's phrasing "fire spreads across the pack, no mob dies quickly" and "BLIND wastes hits
re-poisoning the already-poisoned nearest target" implies **per-target damage dilution / HP chipping**.
The traces show the mechanism is **geometric, not attritional**:
1. Ranged-direct: the AOE **one-shots** whatever is inside its footprint and leaves the rest at **100%
   HP** — nothing is "chipped." The failure is that the aware **detour de-centers the player from the
   pack**, so the AOE footprint covers fewer mobs and never catches the cluster before the player dies.
   It is loss of *positioning/commitment*, realized as reduced *AOE coverage*, not diluted damage.
2. DoT: BLIND does not "re-hit an already-low-HP target" (mobs are never low-HP; they are full until
   the DoT expiry deletes them). BLIND **over-DWELLS** on one committed target while its DoT ticks on a
   delay, and the pack overwhelms the stationary player. AWARE's forced switching moves it off the
   dwelt target sooner, spreading fresh DoT stacks. The benefit is *reduced dwell / wider ailment
   application*, not *avoiding wasted damage on a dying mob*.

The **direction and class-dependence of the hypothesis are fully borne out**; only the damage-model
detail of the "why" is refined (coverage/commitment, not chip-dilution).

---

## Anomalies / deviations disclosed (Discipline #11)

- **A1 — Neutral-cell equivalence collapse:** 32 cells → 15 distinct encounter behaviors; the mismatch
  "kits" are labels on bit-identical equivalence classes (e.g. bowazon ≡ kinetic-fusillade byte-for-byte
  every seed/arm). Not a defect — it is the W3′ methodology; but it means the "8 distinct mismatched
  cell-slots" are really ~3 distinct mechanisms (ranged-direct fail, ranged-DoT repair, and the
  baseline-only seed-23 death). Flagged so the conductor doesn't over-count independent evidence.
- **A2 — Aware clear-failure is near-universal, not guard-specific:** 27 of 32 aware-encounter cells
  kill <40. The guard fired only on the subset where the arms DISAGREE on a full clear. Framing matters
  for any "how many cells regressed" statement: the guard trip is a *disagreement* count, not a *failure*
  count.
- **A3 — Wrapper decision-count vs engine trace_len:** my recorder logged `n_decisions_recorded` =
  `trace_len_engine + 1` in some fights (the wrapper fires once on the terminal decision before the
  engine's own trace snapshot boundary). Immaterial to every metric (all use the aligned prefix); the
  determinism check matched engine `trace_len` exactly. Disclosed for completeness.
- **A4 — §4 clean-set caveat restated:** the clean-cell margin (−12.08%) is a biased, class-confounded
  subsample (18/128) reported as mechanism-diagnostic only; it is NOT a re-scoring and does not bear on
  the gate verdict state.
- **No deviation from the frame otherwise:** engine `2f43045` unmoved at both diagnostic beats; zero
  `*.py` diff under `src/reincarnated/`; corpus.db read-only; fights sequential; instrument
  provably non-perturbing (144/144 byte-identical to seal).

---

## Artifacts

- Findings (this file): `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-trace-investigation.md`
- Diagnostic script: `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-trace-diagnostic.py`
- Regenerated trace dump (untracked, regenerable): `…/2026-07-22-aware-fighter-ablation-trace-dump.json`
- Inputs consumed (unmodified): `…-blind-full.json`, `…-aware-full.json`, `…-verdict-input.json`,
  `…-runner.py`, `2026-07-22-tier3-w3prime-gate.py`.
