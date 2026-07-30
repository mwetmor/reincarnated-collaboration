# WR2-ENCGEO Cell C — movement policy v2 (Mechanism C), player only

**Run:** WR2-ENCGEO-2026-07-29 · **Cell:** C (RELAUNCH) · **Seam:** gamora · **Date:** 2026-07-29
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §1 mechanism C, §8.14–8.15
**Build contract:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` §C / §D / §E / §G (Cell C row)
**Math note:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-c-movement-policy-2026-07-29.md`
**Rulings applied:** R-WR2-4, -5, -9, -10, -13, -14, -17 · SS-1 · **Baseline pin:** `4f09e35` (charter §8.9)
**Engine commits (NOT PUSHED):** `61a6be4` (build) · `ecea69f` (gates) · this note's commit
**Status:** COMPLETE. All gates PASS on the first lap. **The pre-authorized tuning lap did NOT fire.**
Nothing graded here — the cell computes, the conductor grades.

---

## Verdict table

| # | Gate-2 deliverable | verdict |
|---|---|---|
| 1 | **S-2a** — player wall-contact share ≤ 5 % of player-alive ticks, PER TIER | **PASS — 0.000 / 0.000 / 0.000 / 1.004 %** (§2) |
| 2 | **S-2b** — final-10-s wall share ≤ 20 % (no terminal corner-pin) | **PASS — boss 2.580 %, others 0.000 %** (§2) |
| 3 | **S-3** — no-evasion player still killable · win reachable on `pre` · `post` still won | **PASS on all three. No lap fired.** ⚑ one leg REPORTED, §3 |
| 4 | **S-4** — byte-reproducible at fixed seed, twice | **PASS — 150/150, un-normalized** (§4) |
| 5 | §B-6 residual counters re-reported | **REPORTED — GREW 7 → 180 ticks. Not repaired.** (§5) |
| 6 | Flag-OFF full regression, name-diff vs the 81-name baseline | **PASS — `removed=0 added=0`** (§6) |
| 7 | Flag-OFF byte-identity vs `4f09e35` | **PASS — 450/450, sole diff `header.engine_git_hash`** (§6) |
| 8 | Trajectory reconstruction on `boss__B__seed74000802` — does it turn? | **PASS — 3.84 → 150.80 rad, 24.00 circles** (§7) |
| 9 | Unit tests: precedence · root/CC · heading · flip · band · wall falloff · flag-OFF | **PASS — 43 new, all green** (§8) |
| 10 | Math note, new file for C | **`simulation/math/wr2-c-movement-policy-2026-07-29.md`** |
| 11 | Riding obligations: Cell-A WARN-1 gating, Cell-B WARN-3 comment | **BOTH DISCHARGED** (§9) |
| 12 | SS-1 — banked batteries untouched | **ASSERTED MECHANICALLY + verified by mtime** (§11) |

---

## 0 — ⚑ STEP 0: the interrupted WIP was **ADOPTED**, not discarded. Here is why, and what the audit did not cover.

The brief's default was DISCARD-via-stash, on the correct reasoning that an interrupted fragment is
of *unknown completeness*. **I declined the default, because I closed that unknown rather than
assumed it away.**

What was actually on the floor: 7 modified files, and — not named in the brief — **3 untracked NEW
files** the previous agent had also written: `policy/reposition.py` (the whole pure helper),
`tests/test_wr2_c_movement_policy.py` (43 tests), `simulation/math/wr2-c-movement-policy-2026-07-29.md`,
plus the battery driver `wr2_cell_c_move_2026_07_29.py`. So the fragment was not a fragment. It was
a substantially complete cell, ~900 lines.

**The decision procedure, stated because a discard/adopt call on someone else's dead work should be
auditable:**

1. I read **every changed line** of all seven modified files and all four new ones — not skimmed,
   diffed against `4f09e35` and checked clause-by-clause against spec §C-0…§C-7, §D-1…§D-7, and §E's
   frozen/tunable wall.
2. Conformance came back clean on every frozen row: precedence order, heading-on-target (structurally
   unavailable — the helper has no heading output at all), no attack suppression, the flip trigger
   SET, flag defaults, `entity_radius` never written, zero RNG.
3. It was green: 43/43 unit tests passed in 0.26 s.
4. **Adopt beat rebuild on the merits, not on cost.** Rebuilding ~900 lines of already-verified,
   already-spec-conformant work would have burned an hour and re-exposed the cell to the same server
   death, to arrive at code I had just finished proving correct.

**What the audit could NOT cover, and how I closed it.** An audit proves conformance of *code*. It
cannot verify *measurements*. And `MIGRATION.md` §5/§7 carried specific measured numbers
(`~150 rad`, `0.48 → 0.07`, `44/60 → 0/60`) while **no `wr2_cell_c/` battery existed** and math note
§12 was still its `written post-run` placeholder. Those numbers were therefore **unverified prose in
a consumer-facing document** — the single real hazard in the inherited work.

So I treated every inherited number as unmeasured and **re-derived all of them from my own battery.**
Result: the trajectory and straightness figures **corroborate to the digit** (3.84 → 150.80;
0.4836 → 0.0732), and the nova finding is real but its **wording was wrong** — corrected in §10.

**Disposition of the rest of the debris.** The stray `54000` (9 bytes, `   53752` — a shell redirect
typo) was DELETED. The meta-repo Cell-B note diff was **KEPT**: it is two coherent, well-cited
errata banners discharging charter §8.13 WARN-1, evidence-backed and correctly scoped as
documentation-only. Reverting it would have destroyed a riding obligation already correctly done.

**Attribution (Discipline #10).** The build in `61a6be4` is the interrupted agent's work, audited and
adopted by me; I own the audit, the corrections, and everything from §2 onward. The commit says so.

---

## 1 — What was built

`MovementIntent.REPOSITION`, precedence **EVADE ▸ REPOSITION ▸ ADVANCE ▸ HOLD** with
`_m3_telegraph_response`'s tick claim preserved verbatim — the REPOSITION limb sits strictly below the
`if _m3_handled` branch, so a pilot reading a nova is not simultaneously circling.

A pure `policy/reposition.py`: `reposition_vector` / `preferred_range_band` / `wall_repulsion` /
`flip_ticks`. No RNG, no mutation, no engine reads; every input an explicit scalar; the orbit sign is
engine state passed in and handed back. It returns a **velocity in m/s** and the engine multiplies by
`Δt · _e4_move_scale`, clamps, and accrues realized displacement — the same multiplicative chain every
other player motion uses.

**C-1's degeneracy dissolved, and I verified it rather than assuming R-WR2-17 fixed it.** The spec
attached the run's sharpest ⚠ here: against the boss `r_contact = 2.0` and `min_attack_range = 2.0`,
so `band_outer = 2.00 < band_inner = 2.10` and the band **inverts**. The quantity `band_outer` is
clipped against is the reach at which a skill may be *selected*, and R-WR2-17 moved that
surface-to-surface. Re-derived against the EFFECTIVE reach:

| target | band_inner | `min_attack_range` | reach (B armed) | band_outer | width |
|---|---|---|---|---|---|
| boss (r 1.5) | 2.10 | 2.00 | **3.50** | **2.70** | 0.60 |
| standard mob (r 0.5) | 1.10 | 2.00 | **2.50** | **1.70** | 0.60 |

**The width binds in both rows and the reach term is slack by 0.80 m** — the regime the spec's
defaults were chosen for. The inversion guard is retained anyway, because R-WR2-14 ships two
independent flags and C-armed-without-B reverts the reach; that combination is not the gated one and
is reported rather than designed for. Unit-tested over a sweep of radii and ranges.

### ⚠ SEMANTIC SHIFT SS-C-3 — named, because it is the mechanism and not a side effect

Pre-R-WR2-17, `band_outer ≤ min_attack_range` held identically, so spec §C-0's *"REPOSITION where
today HOLD"* and §C-1's *"REPOSITION iff `d ≤ band_outer`"* described the same set. **Post-R-WR2-17
they do not:** `band_outer 2.70 > min_attack_range 2.00`, so `d ∈ (2.00, 2.70]` was ADVANCE and is
now REPOSITION.

I implemented §C-1's radial rule, not §C-0's prose, and that is a fork I should name rather than
bury. §C-1 is the operative text (*"`d > band_outer` → that IS ADVANCE"*), and the arithmetic decides
it: under §C-0's literal formula the player must be inside 2.00 m to reposition, which post-B is
**unreachable** — the band would be a set of measure zero and C would remain the no-op it exists to
fill. §12.6 then measured the consequence exactly: `advance` moves by −51 across the battery, all of
it in `mixed_pack`, with boss/champion/trash invariant at their Cell-A banked values.

Also: `ORBIT_SPEED_FRAC` 0.60 tangential; **state-driven** flip (wall-dot / dwell 4.0 s /
target-change, debounce 0.8 s, **uniform across all three triggers** — named as my choice in math
note §3.2, since §C-2 states the debounce's purpose only against rule 1); seconds converted at read
time via one rounding rule (§D-6); quadratic wall repulsion over a 3.0 m band; composition cap at
`movement_speed`; **zero RNG draws end to end** (R-WR2-10). Heading untouched (C-5). No attack
suppression (C-6 / R-WR2-9). Player only — `_navigate_entity` untouched and the boss gets no
wall-awareness (R-WR2-13), asserted by test over the symbols the arm would have to introduce.

Two further shifts named at the build commit: **SS-C-1** the intent enum grows a fourth value (so
exhaustive matches outside the seam are non-exhaustive by *two* — SS-M12b-4's warning compounds);
**SS-C-2** `_trace_decisions` now gates BOTH `decision` emitters, so the flag names a trace-content
invariant rather than a battery arm.

---

## 2 — S-2: de-cornering. **PASS on both clauses, every tier — and the corner state is GONE.**

Measured from the emitted frames with the WR1-ENV clamp probe's predicate **verbatim** (`CLAMP_EPS`
1e-6, per-entity radius from the header, never a global), so BEFORE and AFTER are the same
measurement rather than two similar ones.

| tier | traces | player-alive ticks | wall ticks | **wall share** | WR1 BEFORE | final-10 s | corner |
|---|---|---|---|---|---|---|---|
| trash | 90 | 5,292 | 0 | **0.000 %** | 51.99 % | 0.000 % | 0.000 % |
| champion | 90 | 6,223 | 0 | **0.000 %** | 0.06 % | 0.000 % | 0.000 % |
| mixed_pack | 90 | 22,550 | 0 | **0.000 %** | 75.33 % | 0.000 % | 0.000 % |
| boss | 180 | 99,699 | 1,001 | **1.004 %** | 75.03 % | **2.580 %** | 0.000 % |

Boss clears the 5 % tier gate by 5× and the 20 % terminal-pin gate by 7.8×. Per leg: pre 0.829 %,
post 0.897 %, pre_endpoint 0.488 %.

**The PASS is not an average hiding a pinned outlier**, which is the obvious way to fake this gate:
the worst SINGLE trace is **1.47 %** (`pre/boss__B__seed74000810`) and the worst single final window
is **6.00 %** (`pre/boss__A__seed74000800`) — both inside the aggregate thresholds.

**The corner share is 0.000 % on every tier.** WR1-ENV measured the boss-tier player standing on the
exact point (0.5, 0.5) for a median **70.8 %** of its alive ticks. In 450 fights it happens **zero
times**. That is spec §C-3's "the corner falls out for free" measured rather than argued: there is no
corner special case anywhere in the build, and there are no corners.

The residual 1.004 % on boss is not a pin. Boss fights are the long ones (370–630 ticks) and an orbit
about a 1.5 m body carries the player into the 3.0 m band on the arena's short diagonals; the wall
term then turns it. The final-10-s number is what says it turns *before* the fight ends.

---

## 3 — S-3: outcome symmetry. **PASS on all three predicates. The lap did not fire, and the AoE whiff window was never reached for.**

Three arms, one changed thing between adjacent pairs (Discipline #10), so no mechanism's contribution
is claimed from the WR1→CellC diff alone. Boss-tier win rates:

| leg / arm | WR1 (neither) | Cell B (B only) | **Cell C (B + C)** | predicate |
|---|---|---|---|---|
| pre / A (no-evasion) | 0.000 | 0.000 | **0.000** | **S-3a PASS** — still killable |
| pre / B | 0.467 | 1.000 | **1.000** | **S-3b PASS** — win reachable |
| post / A | 1.000 | 1.000 | **1.000** | **S-3c PASS** |
| post / B | 1.000 | 1.000 | **1.000** | **S-3c PASS** |
| pre_endpoint / B | 0.067 | 0.033 | **0.000** | ⚑ not a predicate — see below |

Mean boss durations: pre/A 37.2 → 51.0 → 49.4 s; pre/B 57.9 → 64.9 → 67.2 s. S-6's table, not a gate.

**The tuning lap was NOT spent, so §E is untouched and every parameter still sits at its spec
default.** The charter's S-3 diagnosis order (check the circle-AoE whiff window BEFORE touching any
dial) was therefore never entered. I note explicitly that I did **not** reach for a dial: nothing
failed. `band_outer` at 2.70 m against the boss also sits **0.80 m clear** of the `aoe_radius` 3.0 /
selection 3.5 whiff window jack-ryan named, and there is a unit test pinning that clearance
(`test_band_outer_stays_clear_of_the_circle_AoE_whiff_window`) so a future lap that moves
`BAND_WIDTH` cannot walk into it silently.

### ⚑ REPORTED, NOT GRADED — `pre_endpoint`/arm B reaches 0.000

The charter's S-3b names **the pre leg**, which is 1.000, so this is not the graded quantity and
**I claim no FAIL.** But the endpoint leg's boss win rate has gone **0.067 → 0.033 → 0.000** across
the three arms: it was already 1-in-30 before C, and C removed the last one. A leg's win rate hitting
zero touches the *spirit* of "win still REACHABLE" on a leg the predicate does not name, and the
honest move is to put it in front of the conductor rather than leave it in a table. It is also the
one number in this cell where I would not object to being told to look again.

---

## 4 — S-4: determinism. **PASS, 150/150 byte-identical.**

`pre` leg fired twice into two scratch roots, from **this one process and this one tree**, so
`engine_git_hash` is identical by construction and the comparison is **un-normalized** — Cell A's
lesson, that a determinism check straddling a tree change measures the tree and not the RNG.
`matched = 150/150`, `differed = 0`.

This is the expected result rather than a lucky one: R-WR2-10 was implemented as zero draws, the flip
is a pure function of `(t̂, û_wall, ticks_since_flip, target_changed)`, spec §D-1's `ORBIT_STREAM_SALT`
sub-stream is neither constructed nor drawn, and no stream position moves anywhere — which is also
what keeps the S-6 before/after diff uncontaminated by draw-position drift.

---

## 5 — §B-6 residual counters: **GREW 7 → 180 ticks. Reported, not repaired — and the composition is not what I predicted.**

| | Cell B (`4f09e35`) | **Cell C** |
|---|---|---|
| `collision_residual_ticks` | 7 | **180** |
| `collision_residual_max_m` | 0.0012118 | **0.0013506** |
| locus | `mixed_pack`, mob↔mob pack chains, 3 seeds | **`trash`, ALL 90 fights, exactly 2 ticks each** |
| `mixed_pack` | 7 | **0** |

Prediction #5 said the counters would grow and declined to predict zero. **Direction HIT — locus
MISSED, and I record it as a miss** (Discipline #11, and Cell B's own precedent of recording its
0-prediction as missed). I named `mixed_pack`, where the chain binds. `mixed_pack` went to **zero**.
All 180 are `trash`, at **exactly 2 ticks and an identical `max_m` to 17 significant figures in all
90 trash fights, every seed, every leg.**

**That uniformity is the finding.** Seed- and leg-invariance means this is a deterministic geometric
consequence of the trash spawn layout plus C's opening motion, not a stochastic pile-up — which is a
better-behaved object than a growing chain residual would have been.

**Verified against the emitted frames, never the solver's own counters** — an instrument that grades
itself is not a gate (math note §8, Cell B's law). Worst POST-solver overlap over the trash traces:
**0.0009889945962079372 m**, on a **player↔mob** pair with **neither body on any clamp bound at that
tick** (both axes measured — I state the wall status because §8.13 WARN-1 is precisely the mistake of
asserting wall-involvement one way or the other without checking). It equals S-1's worst slack to
17 s.f.: the `gap ≤ ε_touch → continue` skip threshold showing up as its own value, i.e. §B-6's
deliberate **pre-correction over-report**, unchanged in KIND from Cell B. Inside `ε_touch = 0.001` and
an order of magnitude inside S-1's 1 cm.

**S-1 carry-forward PASSES 450/450** — 312,956 pair-samples, zero violations, worst slack
−0.000989 m. Cell B's geometric invariant survives a configuration space it never visited.

`ITER_MAX = 8` **stays frozen.** No gate needs it, and raising it to pass one was refused at
R-WR2-16. Charter §8.13 ledgered the distinction — a rise answering a *measured* over-constraint
would be a mechanism amendment ruled on evidence — and this measurement knocks on exactly that door.
**It is the conductor's to open, not mine.** WARN-2 discharged as a report.

---

## 6 — Flag-OFF: **regression name-diff EMPTY both directions, and byte-identical to `4f09e35`.**

**Full suite, run ALONE** — charter §8.11's lesson (no parallel pytest against a shared editable
install; the `__pycache__` race that cost Cell B two false regression runs). `60 failed / 6,128
passed / 21 errors in 1,226.30 s`.

Name-diff against the 81-name baseline
(`agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`):
**81 observed, 81 baseline, `removed = 0`, `added = 0`.** The `+44` on passed is exactly the 43 new
tests in `tests/test_wr2_c_movement_policy.py` plus the one new SS-C-2 test in the M-12b file; Cell B
landed at 6,084.

**Byte-identity, measured ACROSS TWO TREES.** A `git worktree` at `4f09e35` and this one, identical
argv in both (`--trace-decisions --body-separation-v2`, **no** `--movement-policy-v2`), three legs,
450 traces, and a recursive field-diff carrying **no a-priori exclusion** — the exclusion set is
*discovered*, which is the form jack-ryan's Cell-A Gate-2 asked for:

- **The only trace field that differs anywhere is `header.engine_git_hash`.** Nothing else, over
  450 pairs. It differs by construction: two commits.
- Fight rows differ in **`trace_path` alone** — the scratch out-dir this comparison chose, not a
  behaviour difference. Every other fight-row field is equal in all 450 rows.
- `report["wave_regime"]` gains exactly the one declared additive key,
  `movement_policy_v2_wr2_c: false` (MIGRATION §1).

Per MIGRATION §1, **Cell BAT's flag-OFF byte-identity snapshot must pin at THIS landing**, not at
`4f09e35` — same class as Cell B's INFO-1, same reason: a flag-OFF report now carries one more key.

---

## 7 — Trajectory reconstruction on `boss__B__seed74000802`: **the path TURNS.**

The trace WR1-ENV used to establish drift-not-orbit. Three quantities, because they answer three
different objections, and a plot is read where a number is checked:

| quantity | WR1 (neither) | Cell B (B only) | **Cell C (B + C)** |
|---|---|---|---|
| `total_abs_turn_rad` | 3.84 | 4.07 | **150.80** |
| in full circles | 0.61 | 0.65 | **24.00** |
| `azimuth_sweep_rad` about the boss | −0.14 | −0.25 | **+6.32** |
| `azimuth_reversals` | 1 | 3 | **21** |
| `straightness_ratio` (net / path) | 0.4836 | 0.4838 | **0.0732** |

Prediction #6 said heading change goes from ≈ 0 to **≥ 2π**. **HIT by a factor of 24.**

Why three and not one: `net_turn_rad` is ≈ 0 for a straight line *and* for a policy that orbits one
way then the other, so it cannot be the headline — which is exactly why the flip exists.
`total_abs_turn_rad` separates a line from any turning path. And `azimuth_sweep` is the quantity
"orbit" actually names: the player sweeps **+6.32 rad about the boss — a full circuit** (2π = 6.283)
— where it swept −0.14 before. Straightness collapsing 0.48 → 0.07 is the signature of a closed
orbit rather than a drift. The 21 reversals are the flip state machine appearing in the *geometry*
rather than in its own log.

Cell B moved these numbers by ~6 % (3.84 → 4.07). **Cell C is the mechanism that turns the path**, and
the B-only column is what proves it.

---

## 8 — Unit tests: 43 new, all green, every item the brief named

`tests/test_wr2_c_movement_policy.py`, 43 tests, 0.26 s. Mapped to the asks:

- **precedence order** — REPOSITION preempts ADVANCE inside the band; ADVANCE still owns beyond it;
  HOLD when movement is suspended; `band_outer=None` is the legacy classifier byte-for-byte; **plus a
  grid-equivalence test pinning the engine's INLINED predicate against the seam's declared one** —
  Cell B's HALT was a transcription defect of exactly that shape, so the two are pinned rather than
  trusted to agree.
- **root / CC zeroing** — the strong form: with the player permanently movement-locked the helper is
  **never called at all** (0 calls vs > 200 in the control). A test that only checked "did not move"
  would also pass on an implementation that computed an orbit and multiplied it by zero.
- **heading stays on target** — measured on the live engine, **exact to < 1e-12** on every armed tick
  (an ordering fact makes it exact, not statistical), **with the failure mode as a control**: the same
  ticks would sit ≥ `CONE_HALF_ANGLE_RAD` away under a tangent-writing bug. C-5 is the easiest way to
  silently kill S-3 and this is the assertion that makes that structurally unavailable.
- **flip determinism + debounce** — dwell fires at the period and not before; target-change fires once
  debounce elapsed; the wall trigger flips ONLY when the tangent drives into the band; debounce blocks
  every trigger uniformly; a wall-pressed orbit **settles instead of chattering**; the flip consumes
  no RNG.
- **band derivation vs effective range** — boss 2.10–2.70 and mob 1.10–1.70 pinned; the C-1
  degeneracy proved REAL without R-WR2-17 and the guard proved to hold; non-inversion over a sweep of
  radii and ranges; **`band_outer` clear of the circle-AoE whiff window.**
- **wall-repulsion falloff** — exactly zero outside the band; quadratic with **zero value AND zero
  slope at the band edge**; inward on each face; the SW corner falling out with no corner code;
  magnitude never exceeding unity.
- **flag default-OFF byte-identity** — defaults False on both entry points; flag-OFF reproduces the
  pre-C fight in every reported quantity; **and P-2's converse, `test_arming_C_MOVES_the_fight`**, so
  no later measurement rests on an arm that might be inert.
- plus: helper purity over 1,000 calls, coincident-target `(1,0)` fallback, composition cap binding,
  tunable defaults **equal to spec §E**, no attack suppression (code-lines only, so the limb's own
  explanatory comment is not read as the violation), no mob-nav reach, and de-cornering on one seed
  (> 50 % → ≤ 5 %) so a regression is caught by pytest and not only by a 450-fight battery.

`tests/test_wr1_m12b_m3_realized_count_telegraph_response.py` amended for SS-C-1 (the cardinality pin
moves 3 → 4 and names the new member — the pin is the tripwire that caught the change, so it moves
rather than being loosened to `>=`) and SS-C-2.

---

## 9 — Riding obligations: both discharged

**(a) Charter §8.6 WARN-1 — the second, ungated `frame_sink.decision(...)`** on the evade branch
(`spatial_engine.py:4258`). Now **unified** under `_trace_decisions` rather than merely also gated, so
the two emitters cannot drift apart again. **SS-C-2, named:** `_trace_decisions` now means "the trace
carries `decision` records" for both emitters unconditionally; an M-3-armed caller with
`trace_decisions=False` used to get records and now does not. Unreachable today (M-3 is dark on every
production and battery path, so no banked trace came from the ungated emitter) — which is why it was
an INFO and not a defect — but Cell C rewrites that branch's precedence, so it closes here.
`test_SS_C_2_the_decision_channel_is_DARK_unless_trace_decisions_is_armed` pins the invariant from
the side that was previously false, and asserts the policy actually fired first so the assertion is
not vacuous.

**(b) Charter §8.13 WARN-3 — the SS-B-2 in-code rationale.** Both sites
(`_apply_soft_collision` and `policy/seam.choose_target`) now cite **§D-3(1) value-equality between
two DISTINCT entities**, and say plainly that the §D-3(3) NaN self-miss **does not reproduce**
(`list.__contains__` tests `x is e or x == e`, so a body matches its own entry by identity before
equality runs). This mattered because those comments were the only place the errata'd mechanism still
stood as the justification for two **unflagged default-path** changes — and the corrected rationale is
*stronger*: the byte-identity claim becomes unconditional rather than NaN-conditional. Pinned by
`test_WARN_3_...`. Errata banners also carried into the Cell B math note for WARN-1 and WARN-2.

---

## 10 — ⚑ For the conductor: the nova-dark finding, re-verified and its wording CORRECTED

Not Cell C's, not Cell C's to repair — but Cell C found it, and I re-verified it independently rather
than inherit it.

| arm | `circle`-shape telegraphs (the nova ring) on `boss__B__seed74000802` | `n_nova_crossings`, boss leg | `max_realized_count` |
|---|---|---|---|
| WR1, neither flag | **1** (tick 8, `…:nova:1`) | 44 | 2 |
| Cell B, `_bsep` only | **0** | 0 | 0 |
| Cell C, `_bsep_mv2` | **0** | 0 | 0 |

**B-only and B+C are both zero, so Mechanism C is not the cause.** The finding is B's, at the base
commit `4f09e35`, before C existed.

**⚠ Wording corrected, against §8.13 WARN-1's own lesson.** The inherited note said *"boss-tier nova
casts fell 44/60 → 0/60"*. **44 is `n_nova_crossings`, a per-leg aggregate — not a count of casts**,
and conflating the two is exactly the class of sentence that gate caught in Cell B. Restated by field
name in both MIGRATION §7 and math note §12.3.

Mechanism, isolated to one line: SS-B-1 moved the skill **selector** to surface-to-surface but not the
nova's own cast gate (`spatial_engine.py:4435`, `fire_range_m = 10.0`, still centre-to-centre). The
selector now admits the nova out to 10.5 m against the 0.5 m-radius player, so the single per-fight
attempt lands in a 0.5 m **select-but-refuse** window, is refused, and **still pays the 6.0 s reuse
`Delay`**; by the time it expires the boss is in melee contact and `ready_indices[0]` returns index-0
melee forever. Falsifier, same seed, same tree, one flag: **OFF → tick 8, d = 9.2311, gate PASSES,
ring minted; ON → tick 7, d = 10.2086, gate REFUSES, 6.0 s burned.**

**Second and larger instance of jack-ryan's Cell-B INFO-2 select-but-whiff class** — same seam, but
this one is a *refusal that bills the cooldown* rather than a whiff. It also means the charter's
S-3 **death-2 band clause is structurally unreachable at the base commit**, for a B-side reason no
C dial can touch, which is why S-3 is graded here on the win-rate triple.

**Scope:** extending SS-B-1 to `fire_range_m` is a reading of **R-WR2-8/-17, which are conductor
rulings**; spec §E marks every B row **NO**; no §E tunable reaches it. Routed up with the falsifier,
not repaired.

**Consumer consequence, already in MIGRATION §7 for drax:** any `_bsep` or `_bsep_mv2` boss trace
carries **no ring telegraph and no crossing**, so a renderer expecting the GD-replica nova renders
nothing.

---

## 11 — Artifacts, SS-1, and what is committed

| artifact | status |
|---|---|
| `output/kitcal_g5/wr2_cell_c/` (162 MB, 450 traces + 3 reports) | on disk, **NOT committed** — regenerable in ~10 s |
| `output/kitcal_g5/wr2_cell_c/wr2_cell_c_statistics.json` | **COMMITTED** — every gate computation |
| `output/kitcal_g5/wr2_cell_c/wr2_cell_c_s4.json` | **COMMITTED** — the S-4 replicate |
| `simulation/wr2_cell_c_move_2026_07_29.py` | **COMMITTED** — the driver; battery + S-1/-2/-3/-4 + trajectory + census |
| flag-OFF two-tree comparison batteries | scratch, removed; the result lives in the statistics artifact |
| `git worktree` at `4f09e35` | removed after the comparison |

**SS-1 asserted mechanically, not promised.** `_assert_not_banked` refuses to write to
`wr1_battery_2`, `wr1_battery_2_aim`, `wr2_cell_b_s1` or `wr2_cell_b_s1_r2` (or any descendant) —
extended over Cell B's version to cover Cell B's *own* two batteries, because jack-ryan's INFO-6
established that preserving the failing battery beside its passing sibling is what let the review
validate its instrument on a known-failing corpus first. That makes both roots evidence, not scratch.
**Verified independently by mtime:** all four carry timestamps from before this session began.

**Discipline #3:** legs fired sequentially, never in parallel. **Charter §8.11:** the full suite ran
alone, with nothing else against the editable install.

---

## 12 — For the conductor: the four things that need a ruling or a note

1. **Nothing is owed on the gates.** S-2, S-3, S-4, the flag-OFF regression, byte-identity and the
   trajectory reconstruction all PASS on the first lap. **The pre-authorized tuning lap is UNSPENT**
   and every §E parameter still sits at its spec default.
2. **`pre_endpoint`/arm B = 0.000** (§3). Not an S-3 predicate; surfaced anyway because a leg's boss
   win rate reached zero and the trend across three arms is monotone. Your call whether it is a
   finding.
3. **Residual counters 7 → 180** (§5). WARN-2's watched quantity, reported not repaired, `ITER_MAX`
   frozen. The measurement is precisely the "measured over-constraint post-C" case §8.13 ledgered as
   *rulable on evidence* — the geometry is fine (worst post-solver overlap 0.98 mm, S-1 450/450), so
   this is about whether a counter that over-reports by construction should keep doing so.
4. **The nova is dark under `_bsep`** (§10). A B-side one-line units gap, verified independently,
   wording corrected, falsified on a single seed. It removes S-3's death-2 clause and blanks the
   ring for drax's renderer. Ruling needed on whether SS-B-1 extends to `fire_range_m`.

**MIGRATION for downstream:** `simulation/MIGRATION.md` — one additive report key, one conditional
result-dict key, a fourth `intent` value (`reposition`, **dominant by an order of magnitude** on a
`_mv2` boss trace, so a renderer drawing aim-lines only for `advance`/`hold` draws nothing for ~97 %
of the fight), the SS-C-2 gating shift, an unchanged `replica-frame/v1` schema carrying a very
different trajectory, `total_displacement` accruing at a third site with changed meaning, and the two
⚑ consumer notes (nova-dark, residual counters).

**NOT PUSHED.** The conductor pushes.

---

*Cell C closes. Gates computed, not graded. — gamora*
