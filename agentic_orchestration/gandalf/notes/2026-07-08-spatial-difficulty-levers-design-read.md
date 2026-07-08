# Spatial Difficulty Levers — Design Read (the R1 touchpoint, design-finding form)

**Author:** gandalf (SPEC-AUTHOR; §6 asks are ELICITOR)
**Date:** 2026-07-08
**Commissioned:** Matt, Pattern-B session ("take the work item") — the design read on gamora's routed finding
**Input:** `agentic_orchestration/gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md`
**Verified against source:** `spatial_gauntlet/arena.py` (multiplier :49-55, leash :60-90, SCENARIO_OPEN_ARENA :488, SCENARIO_CHOKEPOINT :575, SCENARIO_MAGIC_PACK :746, registry :1088), `spatial_engine.py:3441` (multiplier application site), `gauntlet_sim.py:173-177, :860-884` (season_emit / family-certification gate)
**Chain context:** this ruling = the **R1 Matt touchpoint** of the pre-ratified chain (arrived in design-finding form, not halt form). Does NOT block R2 (Tier-1 re-fire). Gates **R4 / Leg-C**.

---

## 1. Top-line — the instrument has lost its gradient

gamora's G1/G2 finding is correct and I ratify both halves. But the two routed levers
("open_arena leash/positional geometry" + "magic_pack HP-multiplier scope") are surface
expressions of one deeper condition:

**The endgame-BC WR surface is saturated at both rails.** 323 floor events (WR=0.000) +
278 ceiling events (WR=1.000), and — decisive — **every logged extreme is exactly 0.000 or
1.000; the matrix shows no mid-band mass anywhere.** Every room is either free or impossible
for every kit. A calibrated difficulty instrument places a kit population on a **gradient**;
this one produces a step function. That is the definition of uncalibrated — and it is the
same degeneracy the 1.5× was invented to repair on 2026-05-19 (then: all 51 classes at
WR=1.000), now recurred in mixed two-rail form.

**Why it recurred: three difficulty-relevant dials moved independently; the joint state was
never re-ruled.**

| Dial | Ruled | Change | Re-checked against the others? |
|---|---|---|---|
| Per-mob HP regime | 2026-05-28 (endgame profile) | ~2,019 → 26,500 swarm-mid (~13×) | No — profile explicitly "DOES NOT modify arena.py" |
| Legacy ×1.5 runtime multiplier | 2026-05-19 (for the OLD regime + OLD 8-mob rooms) | still stacking in 2 of 3 rooms | No — parked, Matt-scheduling-pending (twice in decisions-log) |
| Room density + geometry | 2026-07-07 (F1/F2 re-population, Q11) | open_arena 8→~40 mobs; magic_pack 4→~24; rooms re-based | No — leash + clock + HP inherited unexamined |

Illustrative arithmetic (assumptions: swarm-mid 26,500 for all tiers — elite/magic ≥ that;
fixed 120s kills-only clock, unchanged since original calibration):

- **open_arena** total kill budget: was ~8 × 3,028 ≈ **24k HP** at last joint calibration →
  now ~40 × 26,500 × 1.5 ≈ **1.59M HP** (~65×) on the same 120s clock. ≈13.3k sustained
  effective DPS just on mob HP, before repositioning cost.
- **chokepoint_corridor**: ~24 × 26,500 × 1.5 ≈ 954k — but the funnel multiplies effective
  AOE throughput; all 12 kits wall it at 1.000.
- **magic_pack**: ~24 × 26,500 × 1.0 ≈ 636k — the LOWEST HP budget of the three, yet 7/12
  kits floor it.

Kit output also grew over the same period (endgame-BC kits vs the old heuristic cohort), so
the 65× is **not** a mismatch magnitude — it is a count of how far the dials traveled while
nobody measured them jointly. The observed two-rail surface is the proof they did not land
in balance.

**The magic_pack line is the smoking gun on mechanism:** everyone walls the corridor at the
HIGHEST per-mob HP while the caster room floors seven kits at the LOWEST. **HP is not the
discriminating variable.** The discriminant is engagement geometry — which is why the
`1.5→1.25` remedy was wrong in *kind*, not just scope (gamora's structural-incapability
point stands and is now over-determined).

---

## 2. Refinement on G2 — pattern is signal; amplitude is artifact

gamora reads the 10/12 bimodality as "positional identity, the design signal the engine
exists to emit." Half-ratify, with one load-bearing refinement:

- **The PATTERN (differential WR by scenario) is design intent.** A melee kit that walls a
  corridor and struggles in the open is a working class. Rider 4 stands: do not fix content
  to satisfy the instrument.
- **The AMPLITUDE (0.000 / 1.000 binary) is instrument artifact.** Bimodal-by-design ≠
  binary-by-design. Design intent is a melee kit at corridor 0.85 / open-field 0.35 —
  *weaker in the open*, not *nonexistent in the open*. WR=0.000 is not identity; it is a
  **lockout**. Player-consequence anchor: these scenarios prefigure descent floor archetypes.
  The player on an open floor with a melee build should feel "this is my weak map — pull
  carefully, fight in bites" (D2 open desert vs a zealer; PoE pack-by-pack routing). A floor
  type that is *arithmetically unwinnable for your build* is not identity texture — no ARPG
  ships it.
- Symmetrically: **chokepoint at 1.000-for-all is ALSO degenerate.** Its stated intent is
  "exploits cone/line AOE; tests spatial positioning advantage" — a room every kit walls
  advantages nobody and measures nothing. The recalibration target is a gradient on BOTH
  rails: floors lift AND walls come off the ceiling.

This dissolves the apparent tension between "bimodality is design" and "0/18 is failure":
the design wants differential; the instrument currently exaggerates differential into binary.

---

## 3. The levers, ruled properly

### Lever 1 — HP-difficulty governance (the fork Matt rules)

The 2026-05-28 endgame profile chose its words precisely: durability is baked into the stat
specification *"rather than applying a runtime multiplier."* The gauntlet path then applies
the legacy runtime multiplier ON TOP (spatial_engine.py:3441, scenario-membership gated) —
two difficulty systems from two eras, stacking in two rooms and not the third. Options:

- **Option A — un-stack (my lean).** The endgame-BC gauntlet path stops applying
  `MOB_HP_DIFFICULTY_MULTIPLIER`; the constant stays at 1.5 for the legacy convergence
  instrument it was actually ruled for. Endgame difficulty is governed by ONE system (the
  profile + scenario design: density, composition, clock). Honors the 2026-05-28 "rather
  than" intent; single small change at one application site; **the parked
  "re-calibration" workstream resolves as SCOPE-RETIREMENT, not re-tuning** — no constant
  moves at all. Side effect: open_arena/chokepoint budgets drop 33% (1.59M→1.06M).
  **This is not Goodhart** — it is resolving *which ruling governs endgame difficulty* in
  favor of the ruling that already claimed that ground, not softening a calibrated dial to
  green a gate. The Goodhart line gamora refused (move a parked constant to pass) stays
  refused.
- **Option B — extend + re-rule the multiplier** (add magic_pack to scope; re-derive values
  per scenario vs the endgame regime). Rejected lean: doubles down on the runtime-multiplier
  pattern the endgame profile explicitly retired; proliferates parked constants; and §1
  shows HP is not the discriminant anyway.
- **Option C — per-scenario difficulty spec block** (HP factor + density + clock as one
  governed structure per scenario). Right *eventual* shape if the scenario family keeps
  growing; more machinery than the unblock needs. Compatible follow-on to A, not an
  alternative.

### Lever 2 — engagement model (the real open_arena lever)

Verified from the spawn tables: player spawns (18, 30); nearest trash ~7-10m; farthest
~30m; **every mob's 25-35m leash covers the player spawn → the entire ~40-mob field
converges from tick 0.** The 35m override was itself calibrated 2026-05-19 for the RETIRED
50×50 geometry ("mob at y=12 leashes at y=47 > player at y=40") — the 2026-07-07 re-basing
to 36×36 never re-checked it. It is a **third inherited-uncalibrated constant.**

At 8 mobs, total-engagement was survivable arithmetic. At genre F1/F2 density it is
alpha-strike-vs-army — and it silently breaks the scenario's own certification intent:
"spread-target throughput / **repositioning cost**" presumes engagements you reposition
*between*. There is no repositioning when everything is on you at once.

Genre canon is unambiguous: open fields engage in **proximity waves** (D2 pack-local aggro
radii; D3 density pulls; PoE pack spacing). Choosing bite size is where open-field player
skill lives. The lever: pack-local activation so open_arena plays as ~3-4 serial waves
(e.g., trash activation radii in the 12-15m range — gamora maths the actual values). This
is not instrument-softening; it is restoring the genre's open-field grammar the room is
supposed to certify against. A total-aggro open field would be bad GAME design too — the
sim accidentally built a room no ARPG would ship.

### Lever 3 — magic_pack: the scope question dissolves

"Should magic_pack join `MOB_HP_DIFFICULTY_SCENARIOS`?" — **No, and under Option A the
question ceases to exist.** Extending the multiplier to magic_pack would make it HARDER
(more HP = longer exposure); the floors say the room already over-kills. The real
mechanism suspect: a **14m-deep room** whose 25-35m leashes cover everything → whole-room
engagement in a space too shallow to kite, re-populated 4→24 without re-checking depth
against density. The floored seven are precisely the wis/int caster-stat kits (low armor,
spiky output — dead in the alpha window). Same serial-engagement treatment as Lever 2,
and/or room depth.

Design note worth keeping: casters-struggle-vs-caster-packs is legitimate mirror-matchup
identity texture (D2 souls vs sorceresses) — *gradient*-legitimate, not lockout-legitimate.
After recalibration I expect and WANT the caster kits to sit LOWER in this room than the
dex kits. Just not at 0.000.

### Lever 4 — certification criterion (flag now, rule with data)

`season_emit` is disjunctive across cohorts, but within a cohort `family_certification_pass`
demands in-band performance per encounter family — and the bands are **two-sided**, so
WR=1.000 walls fail exactly as WR=0.000 floors do. Under confirmed differential-by-design
identity, a per-family two-sided band structurally punishes the kits whose identity is
sharpest. My design position: per-scenario extremes belong in the REPORT as identity
texture (measure-then-filter already ships this); certification should read the portfolio.
**But do not rule this yet** — we cannot separate criterion-shape failure from
difficulty-state failure until the difficulty state is recalibrated. Rule levers 1-3, re-run
($0), read the new band report; if structural fails persist on a working gradient, THEN
rule the criterion with data in hand. (Slots between R2's report and R4 in the ratified
chain — no new touchpoint needed unless it fires.)

---

## 4. The anti-Goodhart acceptance criterion

The recalibration's acceptance criterion must NOT be "N/18 pass." It is:

> **The WR surface regains a gradient:** meaningful per-scenario WR mass in (0.05, 0.95)
> across the 12-kit population; per-kit differentials (corridor vs open) persist as
> *spread*, not *rails*.

We tune until the instrument discriminates, then read which kits are genuinely weak. Kits
still floored on a calibrated gradient are TRUE content findings — that is rider 4 honored,
not violated. Passing kits is downstream of a working instrument; we never tune toward the
gate.

---

## 5. Sequencing (what Matt actually schedules)

1. **No chain block:** R2 re-fire proceeds as ratified once Gate-2 greens — it measures the
   CURRENT state and becomes the before-side of the before/after diff. $0.
2. **gamora, $0, minutes:** termination-reason split of the 323 floor events from the
   existing v3 log (death vs timeout-with-mobs-alive, per scenario). Weights Lever 1 vs
   Lever 2 empirically before either moves — timeout-dominant floors implicate the HP
   budget; death-dominant floors implicate the engagement model.
3. **Matt rules the fork** (§6 below).
4. **gamora executes ruled levers + $0 gauntlet re-run** → before/after band-report diff →
   §4 gradient check.
5. **Lever 4 ruling if needed** (with the new report).
6. **R4 / Leg-C hold-clears** against a coherent difficulty state.

---

## 6. Asks (ELICITOR — Matt rules)

| # | Fork | gandalf lean |
|---|---|---|
| 1 | HP-difficulty governance: **A** un-stack (retire legacy ×1.5 from endgame path) / B extend+re-rule / C per-scenario spec block | **A** now; C as eventual shape if scenario family grows |
| 2 | Engagement model: authorize serial-engagement (pack-local activation) design pass for open_arena + magic_pack, gamora maths the radii, gated by the step-2 termination split | **Yes** — it restores both the certification intent and the genre's open-field grammar |
| 3 | Scheduling: slot steps 2-4 as the pre-R4 work unit on Leg-C's critical path (this consumes the chain's R1 touchpoint; remaining Matt touchpoint = R5 band-sheet values) | **Yes** — it is already on the critical path; naming it makes the chain honest |

**Sign-off:** gandalf, 2026-07-08. Anchors: gamora design-finding note (2026-07-08);
`arena.py` mob-HP + leash + scenario blocks (verified this session); `gauntlet_sim.py`
emission-gate structure; 2026-05-28 endgame-profile ruling ("rather than applying a runtime
multiplier"); F1/F2 re-population Q11 (2026-07-07); riders 1/4/5 of the Lane-C verdict.
