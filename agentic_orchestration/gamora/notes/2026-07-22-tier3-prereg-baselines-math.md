# Tier-3 PREREG-beat — Part 2 NEUTRAL-ARENA BASELINES — MATH NOTE

**Discipline #1 (math-before-code):** written BEFORE the baseline harness. The per-kit
kit-synthesis mapping + the calibration modifier are a non-trivial modifier-formula
decision; they must be justified before code.

**Author:** named-gamora sub-agent · 2026-07-22 · PREREG-beat (conductor: gandalf RUN-CONDUCTOR)
**Binds:** ruling L-13; the prereg's X (effect-size threshold) is DERIVED BY THE CONDUCTOR
from the variance data this beat produces. I derive NOTHING; I only produce the variance.

---

## §0 — What "baseline" means here (the design question)

The prereg needs an **empirical input**: for the 131 family-resolved spine kits
(W3-eligible pool), how much do fight metrics VARY — (a) run-to-run for one kit
(within-kit / seed variance) and (b) kit-to-kit (between-kit variance). The
conductor derives X (the effect-size threshold a W3 showcase/stress contrast must
clear) from these. **X ≈ some multiple of the noise floor**; the noise floor is the
within-kit seed variance, and the signal ceiling is the between-kit variance.

Therefore the baseline MUST satisfy two properties or it is useless:
1. **Between-kit variance must EXIST** — different kits must produce different metric
   distributions. If every kit runs an identical synthetic damage kit, the only
   variance is arena-seed noise → X would be underivable (no signal band). ⇒ the kit
   is the VARIABLE: each kit_id's BC-axis vector drives a distinct kit shape.
2. **Outcomes must land in a MEASURABLE BAND** — not all-floor (WR=0 mmk=0, zero
   variance) and not all-ceiling (WR=1, saturated). The W2 scenario driver floored at
   WR=0.0 because it used `damage_modifier=1.0` on a weak fixed kit (the R2 calibration
   floor). ⇒ a calibration `damage_modifier` places the reference near mid-band so
   between-kit shape differences resolve as measurable spread.

## §1 — The arena is held NEUTRAL-constant; the kit is the variable

Per dispatch: neutral = `open_arena` (the harness's open 36×36 field). Verified
neutral: `choke_zones=[]`, `has_boss=False`, `has_mini_boss=False`,
`continuous_spawn=None`, `timed_add_waves=()`, `gather_primitive_default=False`,
`win_condition='all_mobs_killed'`, 40 mobs (3 elite + 37 swarm). No formation shaping,
no choke, no wave injection — exactly the no-formation-pressure scenario.

Design: for each of the 131 kits, run N seeds of `open_arena` with a kit dict
SYNTHESIZED from that kit's BC attributes. Arena geometry + mob roster are byte-identical
across all kits (neutrality); only the player kit shape changes. This isolates
between-kit variance to the KIT, which is the whole point.

## §2 — Kit-as-variable via BC-cell → real fighting PlayerClass (CORRECTED after §2-probe)

**§2-probe finding (Discipline #11 — verified before committing budget):** a raw
hand-rolled `class_dict` (skill dicts with `damage_multiplier`) produces a PASSIVE
player — `player_damage_total=0.0, mobs_killed=0` even with a 50m-reach circle at
`damage_modifier=20`. Confirmed at `spatial_engine.py`: the player only issues attacks
when a real `PlayerClass` object is threaded via the `player_class=` kwarg (the
PRODUCTION PATH — it supplies the combatant_state/resolver projection that drives player
attack behavior). Hand-rolled dicts do NOT engage. The four-family BUILD smoke only
asserts `aoe_hits>0` (engagement), never player kills, which masked this. **Therefore
the baseline MUST build a real fighting PlayerClass per kit.**

The faithful, generation-seam-clean, smoke-viable path: map each corpus kit's BC vector
to the nearest materialized endgame BC-cell (`endgame_bc_{range}_{tempo}_{amp}_{attr}_none`,
17 neutral cells in `endgame_encounter_catalog`) and build that cell's real PlayerClass
via `martial_bar_rederivation_driver._build_martial_player_class(cell_id, idx,
"balanced")` (0.22s/build, LLM-free, 12 real skills from `per_skill_emitter`). The kit is
STILL the variable: its BC vector `(range_val, tempo_val, amp_val, attr_val)` selects the
cell, so different BC vectors → different fighters → different fight metrics (verified:
melee/high/flat/str killed 2 pdmg 450; ranged/low/spiky/int killed 18 pdmg 7575;
ranged/med/var/wis killed 11 pdmg 2475 — genuine spread).

Vocab bridge (corpus → catalog): `range {melee→melee, dual→mid, ranged→ranged}`;
`tempo {high→high, med→medium, low→low}`; `amp {flat→flat, spiky→spiky, var→variable}`;
`attr` upper-cased. Nearest-cell distance = weighted hamming (range+attr weighted ×2 as
primary axes, tempo+amp ×1). Coverage over the 131 kits: 29 exact / 80 dist-1 / 20 dist-2
/ 2 dist-3; 16 of 17 cells used. NO coverage holes (nearest always resolves).

**HONEST LIMITATION (declared):** with nearest-cell mapping, kits sharing a BC-cell get
the SAME PlayerClass, so the between-kit variance is really **between-CELL** variance
(16 distinct fighters), not 131 distinct fighters. Kits in one cell differ only by
family/era/court metadata, not fighter shape → their pairwise fighter-variance is 0.
This is the correct trade: 16 REAL fighting players (production path, valid metrics) beats
131 PASSIVE non-fighters (zero metrics). The variance I report is between-cell + seed;
I state the cell-granularity explicitly so the conductor derives X against the right
signal. Per-kit rows still carry each kit's cell assignment + within-kit(seed) variance.
This does NOT patch the generation seam (I only CALL the existing martial builder); a
future finer-grained baseline (one KitCandidate per corpus kit) would be a rocket-seam
generation task, flagged not undertaken.

## §3 — Calibration modifier (operating point)

With the real-PlayerClass path, `damage_modifier=1.0` (the metrology driver's native
instrument value — NO dead-wall dmod) already yields a NON-degenerate graded band
(mobs_killed 2–18/40 across cells in the §2-probe; pdmg 450–7575). So I adopt
**`damage_modifier=1.0`** — the attested native operating point, applied UNIFORMLY across
all kits (holding it constant keeps neutrality; between-kit signal comes from the
BC-cell fighter, not a power knob). This matches the metrology driver exactly, so my
baselines are instrument-comparable to the Lane-3 metrology run. The absolute WR level
(all winner=monster in the ~5s smoke) is NOT the deliverable; the graded per-metric
VARIANCE STRUCTURE (mobs_killed, player_damage_total, elapsed_s, aoe_hits, geometry
fractions) is. The §5 empirical check confirms the band is non-degenerate before I
report variance as meaningful.

## §4 — Seed budget (Discipline #2 — smoke-scale)

Dispatch suggests ~4 seeds/kit; my discretion. I choose **4 seeds/kit** ×
131 kits = **524 fights**. Justification:
- Discipline #2 says iterate on smoke, not full regen. 524 fights of a 40-mob open_arena
  (~4–9s sim-elapsed each, sub-second wall each) is a smoke-scale budget (~minutes wall,
  not the 30–60 min full-regen regime).
- 4 seeds gives a within-kit sample of n=4 per metric — enough to compute a per-kit
  spread (range + stdev) as a NOISE-FLOOR estimate, which is all the conductor needs to
  set X's lower bound. It is NOT enough for a tight per-kit CI (that would be a
  full-regen justification), and I do NOT claim one — I report the spread as a
  smoke-scale variance estimate, explicitly bounded.
- Fixed seed set {20260722, 20260723, 20260724, 20260725} shared across all kits so the
  seed axis is held identical (paired design — between-kit differences are not confounded
  by different seed draws). Discipline #3 (no parallel regens of the same seed) is
  honored: this is a single sequential process, one seed set, no parallel same-seed runs.
- PlayerClass builds are CACHED per cell (16 distinct builds, ~0.22s each ≈ 4s total);
  the 524 fights dominate wall time. Each cell's PlayerClass is built once and reused
  across all kits mapped to it and all 4 seeds (deterministic build; seed varies only
  the fight, not the fighter).

## §5 — Empirical checks the harness output must pass (Discipline #11)

Before reporting variance as meaningful, verify (not assume):
1. **Non-degenerate band:** the pool's WR (or mmk) is not all-0 and not all-1. If it is,
   the variance is a floor/ceiling artifact and I say so.
2. **Between-kit > within-kit:** for the gate to be derivable, at least SOME metrics must
   show between-kit stdev > mean within-kit stdev (signal exceeds noise). I report the
   ratio per metric; metrics where it holds are "stable enough to gate on" (a statistical
   OBSERVATION — the conductor DECLARES the subset, I only observe).
3. **Per-era feasibility:** n≥8 resolved kits/era AND ≥1 element-court represented/era
   (both already confirmed from corpus.db: I=27, II=53, III=20, IV=31, all ≥5 courts).

## §6 — Metric superset captured (declare NOTHING; capture BROADLY)

Per dispatch, the conductor's prereg DECLARES the metric subset; I capture the harness's
full emitted superset. `SpatialFightResult` emits 44 fields; I capture the combat-relevant
scalar subset per fight: `winner, elapsed_s, player_kill, mobs_killed, total_mob_count,
total_aoe_hits, player_damage_total, damage_taken_while_committed, completion_rate,
whiff_rate, sustain_uptime, total_displacement, max_flanking_count, total_flanking_ticks,
cone/line/circle_hit_fraction, forced_break_count, move_cancel_count,
drain_exhaustion_events`. Per-kit aggregate: mean + stdev + min + max over the 4 seeds,
per metric. I DECLARE no subset; the variance tables carry all captured metrics.

## §7 — What I do NOT do (hard rules)

- No prereg authoring: X/Y derivation + metric declaration are the CONDUCTOR's. I deliver
  variance data only.
- No scoring-weight changes (Part 1 froze them per L-13(a)).
- Zero engine-repo writes; corpus.db + sidecar read-only.
- The calibration `damage_modifier=6.0` is a MEASUREMENT operating-point, not a committed
  balance constant — it does not touch the engine's balance loop and is scoped to this
  read-only baseline measurement.
