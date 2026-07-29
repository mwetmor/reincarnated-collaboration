# Finding — 2026-07-29 — WR1-G2-M3M12b (realized-count operator + M-3 `piloted_competence`)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Verdict:** **PASS-with-notes** on `7a5eb88`
**Severity:** WARN (two new, both non-gating) · INFO ×5 · **both inherited WARNs CLOSED**
**Target:** engine `7a5eb88` (parent `ddf51a8`; math note `b56c850`, landing `7063845`)
**Developer:** gamora
**Run:** WR1-2026-07-28, cell `WR1-BUILD-M3+M12b` (conductor: gandalf, RUN-CONDUCTOR; charter §8.9–§8.11)
**Predecessor finding:** `qa/findings/2026-07-29-gate2-gamora-wr1-m12.md` (`072ef543`)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate before commit), 3 (cross-seam impact),
4 (decisions/charter as truth), 5 (severity + escalation), 6 (cross-seam contract round-trip)
**Disciplines cited:** #1, #8 (schema validation at boundaries), #9 (attribution clarity),
#11 (empirical inspection over assumption), #12 (semantic-shifting changes declared)
**ADRs:** ADR-002 (tiered approval), ADR-004 (MIGRATION for cross-seam handoff), ADR-006 (read-only)

**Review posture:** read-only on the engine tree. I ran pytest (writes `.pytest_cache` only) and
imported the shipped modules to re-measure. Nothing was written into `reincarnated-engine/`. No
`git checkout`, `stash`, `worktree` or config change. The tree was verified clean on tracked
`src/` + `tests/` at `7a5eb88` before the regression started and again after it finished.

---

## 0 — THE OWED REGRESSION (gating item, routed to me by the conductor) — **CLOSED, CRITERION MET**

The builder's pre-registered two-sided regression never ran (§7 of the build note: orphaned log,
cell died first). I ran the full suite myself at `7a5eb88`:

```
60 failed, 5911 passed, 3 warnings, 21 errors in 1428.21s (0:23:48)
HEAD before = HEAD after = 7a5eb883231ec965dd5e4d2a8cb67ca7ae2e424e
tracked-dirty(src/,tests/) before = [] , after = []
```

**Failure-NAME diff against `ddf51a8`: EMPTY.** 81 names on each side (60 FAILED + 21 ERROR),
identical sets, `diff` returns nothing. The pre-registered criterion is met.

**Baseline provenance, stated precisely.** My own `ddf51a8` run reproduced the *counts*
(60 / 5884 / 21) but I did not preserve its per-test names. The name baseline I diffed against is
extracted by me from `/tmp/wr1_m12_after_full.txt` — gamora's full `ddf51a8` pytest output, which
survived on disk — whose summary line (`60 failed, 5884 passed, 21 errors`) is byte-for-byte the
figure I independently reproduced at that commit. I re-derived the name list from the raw output
rather than trusting the derived `wr1_after_names.txt`; the two are identical.

**The arithmetic closes exactly.** `5911 − 5884 = 27`. At HEAD the two suites collect
`41 + 27 = 68`; at `ddf51a8` the M-12 suite collected 41. Delta = **27 = the new suite, entire**.
No pre-existing test moved from pass to fail, and **no test from either WR1 suite appears anywhere
in the failure set** (`grep` count 0).

**Bonus closure of my own prior audit limit.** The `ddf51a8` finding recorded that I could not
reproduce that lap's BEFORE side and accepted `5843 / 60 / 21` as audit-of-record. Both of gamora's
full outputs from that lap survive on disk; I diffed their name sets directly —
**BEFORE(60/5843/21) vs AFTER(60/5884/21) is also EMPTY.** That caveat is now closed by artifact
rather than by trust.

---

## 1 — INHERITED WARN #1 (angular-offset RNG source): **CLOSED**

`spatial_engine.py:4060` — `_spoke_offset = _gd_draw_spoke_offset(self._gd_nova_rng)`. It is the
dedicated sub-stream (`nova_substream(seed)`, `:2931`), one draw per **successful** cast, sited
after the range check (`:4048`) and after the 80 % gate draw (`:4050`). It is the landing's only
new RNG consumption; the M-3 policy and the telegraph draw nothing.

**Sequence-shift declaration: made, and I can sharpen it usefully.** SS-M12b-2 declares "the nova
is no longer deterministic given `(r, regime)` … single-number reproductions do not [hold]", and
§2.5 states the live fight moved. The precise mechanism is narrower than my WARN assumed: because
the offset is drawn *after* the same cast's gate draw, cast *k*'s gate draw is displaced by
(*k*−1) offsets — **a fight with one successful cast is unshifted.** I re-ran the live boss fight
and this is exactly what happens:

| | `ddf51a8` (recorded) | `7a5eb88` (my measurement) |
|---|---|---|
| crossing time | t = 1.951 s | **t = 1.951 s** — unchanged |
| crossing radius | r* = 5.617 m | **r* = 5.6170 m** — unchanged |
| delivered | 489.48 | **207.40** (n = 1) |

So the non-reproduction is **entirely the count operator, not the cast timing** — which is a
cleaner attribution than "the figures will not reproduce", and it means the r* = 5.617 standoff
that R-WR1-13 routes to the wave is *not* an artifact of the new draw.

## 2 — INHERITED WARN #2 (tombstone keeps the oracle table as a POSITIVE pin): **CLOSED, and strengthened**

`test_T_M2_4_THE_ERRATUM_TOMBSTONE__old_operator_falsified_new_one_agrees` (M-12 suite :400–446)
now carries **three** pins at all six spec radii, not one:

1. the oracle's `(mean, min, max)` table asserted **positively** (`:415–426`) — the table survives;
2. the falsified scalar asserted to **fail** the spec's ≤5 % tolerance (`:430`) — the negative;
3. **new**: `n_expected` == oracle mean and `n_bounds` == oracle `(min, max)` (`:436–437`) — the
   replacement pinned positively against the same instrument.

Plus the 7.689 m boundary and the inside/outside gap assertions. Strictly stronger than what I
asked for. The prose typo I flagged as INFO #1 last lap is repaired at the live sites (`:441–442`
now reads `r·sin(11.25°) ≤ blast → 7.689`, arc form distinguished).

---

## 3 — CLAIMS RE-MEASURED (not read)

I imported the shipped modules and re-derived each claim with my own sweeps and my own seeds.

### 3.1 Operator properties (claim 3) — **CONFIRMED**, with one scoping correction

My own 20,001-point deterministic offset sweep at every spec radius:

| r | `n_expected` | my swept mean | Δ | `⌊W/S⌋+1` | my max | my min | support |
|---|---|---|---|---|---|---|---|
| 1.0 | 16.00000 | 16.00000 | 0 | 16 | 16 | 16 | {16} |
| 2.0 | 4.31914 | 4.31913 | −1.1e−5 | 5 | 5 | 4 | {4,5} |
| 2.5 | 3.27732 | 3.27729 | −3.8e−5 | 4 | 4 | 3 | {3,4} |
| 5.0 | 1.55179 | 1.55177 | −1.5e−5 | 2 | 2 | 1 | {1,2} |
| 9.0 | 0.85281 | 0.85281 | +1.3e−6 | 1 | 1 | 0 | {0,1} |
| 12.0 | 0.63829 | 0.63832 | +2.9e−5 | 1 | 1 | 0 | {0,1} |

Mean = W/S; max = ⌊W/S⌋+1; support never leaves two adjacent integers. A seeded 20,000-draw MC on
my own seed (90210, not gamora's) lands inside 4·SE at every radius. The gapless boundary computes
to **7.688746 m**; aimed at the worst azimuth (half a spoke spacing) the count steps **2 → 0**
across it (2 at r = 7.688, 0 at r = 7.690), which is the cleanest possible demonstration of the
claim. **R-WR1-11(a) holds on independent measurement.**

**Scoping correction — the `==` agreement claim is true inside the footprint and NOT universal.**
The build note §2.2, the module docstring and the commit message all say the closed form agrees
with the segment oracle "per azimuth, with `==`, not to a tolerance." I swept 18,720 (radius,
azimuth) pairs and found three disagreement classes:

| class | where | character |
|---|---|---|
| α = π branch edge | **r = 1.5 exactly** (r == blast) | FP knife edge; 1.4999 and 1.500001 agree perfectly. Measure-zero. |
| \|Δ\| = α ties | e.g. **r = 3.0** (α = π/6 exactly, landing on lattice azimuths) | FP tie between `abs(Δ) <= α` and `hypot <= blast`. 3/1440. Measure-zero. |
| **beyond the footprint** | **r ∈ (12.0, ≈13.5]** | **real, non-measure-zero: 432/720 azimuths at r = 12.5.** |

The third is not a tie. `coverage_half_angle` returns 0 for `r > projectile_distance_m`, so the
closed form says *nothing lands* beyond 12.0 m; the oracle keeps counting to ≈13.5 m because a
segment's **far endpoint** still carries a 1.5 m blast. Note §1 does declare "beyond `r > R`: no
coverage at all" as the model, so this is a *declared* modelling choice — but the unqualified `==`
claim sits three sections later, and the shipped test's radius list stops at **12.0, the last
agreeing radius.** Damage consequence today is **zero** (`band_scale_at(r) = 0` beyond 12.0, so
`raw_payload` returns `{}` — I verified `nova_delivered(13.0, count=16) = 0.0`), and the direction
is **gate-adverse** (the model discards a 1.5 m annulus of true coverage). INFO, not WARN — but the
`==` sentence should be scoped to `r ≤ R`, because the oracle is now *the definition of truth* per
R-WR1-11 and a truth instrument that disagrees with the operator anywhere should say where.

### 3.2 Distribution (claim 4) — **CONFIRMED EXACTLY**

My own 1 mm sweep over (0, 12], with my own two-point mixture, independently recovers the intervals:

```
P(D>=541) == 1  on  (0, 1.624) u [2.500, 2.701)
P(D>=541) >  0  on  (0, 1.805) u [2.500, 3.920)
max P over all r >= 3.920  =  0.000000     (largest r with P>0 is 3.919)
```

Byte-identical to the note. Boundary neighbourhoods behave as claimed and for the stated reason —
at 1.804→1.805 the support drops 6→5; at 2.499→2.500 the ×2.0 band cliff lifts D(3) from 311.10 to
622.20; at 3.919→3.920 the support drops 3→2. All ten rows of the §2.3 table reproduce to ±0.005,
including **r = 5.0 → E[D] = 321.84, P = 0.0000** and the Jensen gap at r = 2.5 (**701.78** vs
`D(E[n])` **699.57**). The R-WR1-11(b) reporting obligation ("min/mean/max + tail probability at
r=5 **and** at fixture range") is discharged in the shipped test, not only in prose.

### 3.3 M-3 (claim 5) — **CONFIRMED**, with an audit note that makes the claim *stronger*

- **Default-off / byte-identical unarmed.** I reran the arm myself: nova-free fights, armed vs
  unarmed, **zero differing fields** across the 47-field `SpatialFightResult`.
  **What the test actually compares:** `dataclasses.asdict(result)` minus `fight_id` / `created_at`
  — a 47-field summary including every RNG-derived counter, across three seeds. That is a strong
  empirical check but it is not a byte-level trace, and the note leans on it. **The actual guarantee
  is stronger and is not argued:** `spatial_engine.py:4989` gates on
  `self._piloted_competence is not None and self._gd_nova is not None`, so with no nova the policy
  is *structurally unreachable*, not merely observed-inert. And `GD_NOVA_SKILL_KEY` has exactly one
  producer in the tree — `kitcal_g5_scenarios.py` — so production and the balance loop cannot mint a
  nova at all. **Double containment; canonical §7.2 is safe by construction.** Recommend the note
  and the docstring rest on the structural argument, with the A/B as corroboration.
- **Argmin is a true two-point expectation.** `telegraph_response.py:219` calls
  `nova_expected_delivered`, which is the `(1−φ)·D(n_min) + φ·D(n_max)` mixture built from two
  integer-count calls to the resolver's own `nova_delivered`. **Not `D(E[n])`**, and R-M3-1's
  one-implementation rule survives.
- **SS-M12b-5 is implemented, not merely described.** `_m3_telegraph_response` returns `True` on
  HOLD as well as EVADE (`:4188–4190`), and `:4993`'s `if _m3_handled: pass` preempts the advance
  branch. Under a live telegraph the pilot does not close. Behavioural claim, correctly framed.
- **No RNG in the policy.** The module imports `math`, `dataclasses`, `typing` and three names from
  `gd_nova` — nothing else. That absence is airtight. **`test_T_M3_6`'s RNG half is vacuous as
  written**, though: it captures the bit-state of a `default_rng(12345)` the policy holds no
  reference to and could not consume. The load-bearing evidence (no RNG import anywhere in the
  module) is the one not asserted. INFO — the conclusion is right, the instrument isn't.
- **Live non-vacuity reproduces to the digit.** 4 evades; crossing radius 5.6170 → **6.6999** m;
  first evade 9.2311 → 8.9900 m lowering projected payload **241.37 → 177.07**. The note's
  "5.62 → 6.70" and "241.4 → 177.1" are exact.

### 3.4 The two spec corrections (claim 6) — **CONFIRMED, both re-derived from the shipped functions**

| | measured by me | note claims |
|---|---|---|
| 5 m → 9 m under the realized operator | **321.84 → 247.62 = −23.1 %** | −23 % |
| 5 m → 9 m under the retired scalar | **524.28 → 536.83 = +2.4 %** | +2 % |
| §9.2 optimum, argmin of E[D] over (0, 12] | **r = 8.999, E[D] = 176.89** | 8.99⁻ |
| E[D](2.49⁻) ÷ E[D](8.99⁻) | **341.45 / 177.07 = 1.928×** | 1.9× |
| 2.5 m cliff greedy penalty (2.4 m, 1 m budget) | 3.40 m → **482.6** vs 2.49 m → **341.5**, **+41.3 %** | +41 % |
| 9 m cliff greedy penalty (8.5 m, 1 m budget) | 9.50 m → **234.5** vs 8.99 m → **177.1**, **+32.4 %** | +32 % |

The brief's own worked example is indeed falsified by the ruling that produced it, and gamora
reported the reversal instead of reproducing a number the operator no longer yields. The M-1
arithmetic is preserved and correctly re-attributed: passing the retired count explicitly still
returns **524.28 / 536.83 / 595.06**, so the suite now records what those numbers were evidence
*for* (M-1) and what they were never evidence for (delivered damage at r = 5).

### 3.5 `emit_telegraphs` emission-only (claim 7) — **CONFIRMED**, with one coverage gap in the static half

The in-suite test is **48 pairs** (2 nova × 2 regimes × 4 tiers × 3 seeds); the note's 80 is the
out-of-suite run at 5 seeds. Both arithmetics check out. The comparison is the same 47-field result
digest, and there is a **non-vacuity guard** (`assert saw_events`) plus an explicit
`telegraph_buffer == []` on the off arm. That is the right construction.

**Gap worth naming:** the static half asserts `"rng" not in src and "random" not in src` over
`_mint_telegraph_spec` — but the **nova's** telegraph is not minted there. It is inline at
`spatial_engine.py:4085–4117`, gated on `self._emit_telegraphs or self._frame_sink is not None`,
i.e. the flag *does* control whether `_gd_nova_delivered(...)` is called and a `TelegraphSpec`
constructed. I read that block: `count=None`, pure, no RNG, no state mutation, buffer append and
sink call only. So the verdict stands — but the static assertion covers a function the empirical
A/B's nova arm never exercises. The empirical half is what is actually load-bearing here.

---

## ⚠ NEW WARN #1 — `MovementIntent.EVADE` reaches `replica-frame/v1` with no MIGRATION.md entry (ADR-004)

`policy/seam.py` gains `EVADE = "evade"`, and `spatial_engine.py:4177–4182` emits it as the
`intent` string on the **existing `replica-frame/v1` decision channel** whenever a frame sink is
attached. The note calls this "no schema change", and field-wise that is true — but the *value set*
of an emitted field grew, and that channel is drax's render surface under R-KC1-19a
("sim thinks, Godot renders") and star-lord's export surface. A downstream exhaustive match on
`intent` is now non-exhaustive.

gamora **declared this correctly in the source** (seam.py comment names the non-exhaustive-match
hazard by SS number) — the gap is the *record*, not the awareness. `MIGRATION.md`'s newest entry is
still the M-12 landing, which filed two strictly smaller parse risks (a twelfth
`calibration_override_fields` name; a third colon segment in the nova `attack_id`). This is the same
class and it is larger.

Mitigating, and why this is WARN and not BLOCK: `"evade"` can only be emitted when
`piloted_competence` is armed, which only the GD-replica acceptance battery does. Production traces
cannot contain it. But **G-D is precisely the lap where replica traces get rendered**, and the arm
is what produces G-B's second leg. **Discipline #8 / ADR-004 / Principle 6.**

**Action:** a short MIGRATION.md entry naming the third `intent` value, its arming precondition, and
"drax/star-lord owe nothing to ship". Round-trip per Principle 6 before the baton renders.

## ⚠ NEW WARN #2 — `latency_floor_ok()` is advisory; R-M3-3's floor is not enforced

`PilotedCompetence.latency_floor_ok()` is called by **nothing** in `src/` — only by
`test_R_M3_3_*`. The dataclass is frozen with no `__post_init__` validation, so
`PilotedCompetence(reaction_latency_s=0.05)` constructs cleanly and the engine will run it. The
reaction latency is the **graded arm's load-bearing calibration parameter** (R-M3-3's 0.2–0.4 s
non-corpus bracket, with 0.0 as the declared ceiling arm), and a sub-tick value would credit
evasion with reflexes the bracket explicitly refuses.

This is the mirror image of the pattern I commended in the M-1 landing: `_coerce_mitigation_law`
**rejects rather than defaults**, so a typo'd law raises instead of silently reporting a comparison
it never ran. Here a typo'd latency silently grades a superhuman pilot. **Discipline #8 — validate
at the boundary, in the same failure direction the sibling door already chose.**

**Action:** raise from `__post_init__` (or have the engine assert `latency_floor_ok()` at arming).
Within-seam, no API change to any consumer — mine to approve under ADR-002 once done.

---

## Notes (INFO — none gate the landing)

1. **A stale number in the shipped source.** `telegraph_response.py:39–40` states the 2.4 m greedy
   case as `E[delivered] 478.9` / `(greedy +40 %)`. The shipped functions give **482.6 / +41.3 %**
   (build note §3.2 has it right; the 8.5 m row in the same docstring is correct). Discipline #9 —
   the module docstring is the first thing the next reader trusts.
2. **The `2r sin(11.25°) → 7.645` typo now lives only inside the preserved-verbatim tombstone
   block** (`gd_nova.py:445`). Live sites are repaired. Leaving history verbatim is defensible —
   but that preserved block is exactly what a reader opens when looking up the erratum, so a single
   bracketed `[corrected: r·sin(11.25°) ≤ blast → 7.689]` would close it without editing the record.
3. **Epsilon-evades spend an action slot for ~0 HP.** In the live fight, evades 2–4 move 0.007 m,
   0.003 m and 0.000 m for cumulative projected gain of **0.19 HP**, and tick 12 logs
   `payload 176.88 → 176.88`. This is the declared tangential-chord artifact (§3.4.2) — but its
   *consequence* (a full uptime tick bought for 1e-5 HP, since `<` is strict) is not stated. Measured
   cost in this fight is **zero** (`player_damage_total` identical to float noise), so nothing is
   broken; it is geometry luck, not design. Naming it before the battery runs is cheaper than
   explaining it after.
4. **Test count off by one.** The note says the new suite is 26 tests; it collects **27**. The
   regression arithmetic closes on 27, so the note's own §6 evidence line understates itself.
5. **My prior finding's audit limit is now closed** — see §0. Worth carrying into the record so
   nobody re-derives it.

---

## Rationale

**Discipline #1** is satisfied in its strongest form: the math note landed at `b56c850`, *before*
the implementation at `7063845`, and the note's §2.5 ("what it costs, stated plainly") retires the
landing's own predecessor evidence rather than defending it. **Discipline #12** is satisfied — six
semantic shifts are enumerated in §5 of the build note and in the commit message, including one
(SS-M12b-5) that is a behavioural claim the builder explicitly offers the conductor the chance to
reverse. **Discipline #11** is satisfied twice over: the falsified operator was **deleted, not
re-pointed**, surviving only as `EXT_1_3_FALSIFIED_n` behind a tombstone that would go red if
anyone quietly aimed the name at new arithmetic — and R-M3-1's hazard *fired during the very cell
that implemented it* (the spec's prescribed 2.5⁻ shelf stopped being optimal), which the `argmin`
form absorbed at zero cost because nothing was hard-coded.

The behaviour that earns the PASS is §8 of the build note: gamora named four things the conductor
should look at, three of which weaken the builder's own position — the sim/fixture geometry
mismatch, the brief's falsified worked example, and a gate-**favourable** new bias reported first.
Reporting the bias that flatters your gate, before the gate runs, is the discipline the run is
built on.

Gate-2 was correctly **not** self-cleared. The two WARNs are both fixable inside the seam and
neither touches a number.

**The BLOCK-tier forward finding from `ddf51a8` is not re-raised here.** R-WR1-13 resolved it: G-B
grades on a fixture-congruent probe at GAL-3's measured range, with 5.62 m reported alongside as
behaviour. The melee-contact reconciliation in the build note §2.4 is provisional pending WR1-GAL-3
and is **not graded by this finding**.

---

## Action

- [x] **jack-ryan:** verdict **PASS-with-notes** on `7a5eb88`. Gating regression **CLOSED** —
      60 / 5911 / 21, failure-name diff vs `ddf51a8` **EMPTY**, delta `+27` = the new suite exactly.
      Nothing needs reverting or re-tagging.
- [x] **jack-ryan:** inherited WARN #1 (offset on `_gd_nova_rng`, shift declared) **CLOSED**;
      inherited WARN #2 (oracle table retained as a positive pin) **CLOSED and strengthened**.
- [ ] **gamora, WARN:** file a `MIGRATION.md` entry for `MovementIntent.EVADE` reaching
      `replica-frame/v1`'s `intent` field (ADR-004 / Principle 6), and enforce `latency_floor_ok()`
      at construction rather than leaving it advisory (Discipline #8).
- [ ] **gamora, INFO (any convenient landing):** correct `telegraph_response.py:39` to 482.6 / +41 %;
      scope the "closed form == oracle" claim to `r ≤ projectile_distance_m` and name the
      (12.0, 13.5] annulus as a declared gate-adverse absence; bracket the preserved `7.645` typo;
      state the epsilon-evade uptime consequence; correct 26 → 27.
- [ ] **gandalf (conductor), INFO:** the ≥541 relocation and the R-WR1-11 operator are confirmed by
      independent measurement. The r* = 5.617 standoff is **not** an artifact of the new draw — the
      first cast's timing is bit-identical to `ddf51a8` — which strengthens R-WR1-13's routing of
      the standoff to the wave as a scenario/kit finding.
- [ ] **Matt:** aware only. No escalation. Both WARNs are within-seam and mine to approve under
      ADR-002 once addressed.

---

## References

**Engine (`7a5eb88`, read-only):**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/gd_nova.py` (`coverage_half_angle` :272, `n_expected` :297, `n_bounds` :318, `draw_spoke_offset` :340, `n_realized` :355, `EXT_1_3_FALSIFIED_n` :394, `oracle_count_at` :474, `nova_expected_delivered` :616)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/telegraph_response.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/seam.py` (`MovementIntent.EVADE`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (:2931 sub-stream, :4050 gate draw, :4060 offset draw, :4085–4117 nova telegraph, :4130–4224 `_m3_telegraph_response`, :4989–4994 the default-off gate)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/wr1-m12b-m3-realized-count-telegraph-response-2026-07-29.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (newest entry is still M-12 — see WARN #1)
- `/Users/admin/Games/reincarnated-engine/tests/test_wr1_m12b_m3_realized_count_telegraph_response.py` (27 tests)
- `/Users/admin/Games/reincarnated-engine/tests/test_wr1_m12_gd_mitigation_nova.py` (41 tests; tombstone :400–446)

**Meta-repo:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr1-build-m3-m12b.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (§8.9 R-WR1-11 / R-WR1-12; §8.11 R-WR1-13)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr1-m12.md`

**Regression artifacts (ephemeral, `/tmp`, recorded for reproducibility):**
`jr_wr1_g2_regression.sh`, `jr_wr1_after_7a5eb88.txt`, `jr_wr1_after_names.txt`,
`jr_ddf51a8_names.txt` (extracted by me from gamora's surviving `wr1_m12_after_full.txt`),
`jr_wr1_measure.py`.

*Filed by jack-ryan, WR1-G2-M3M12b. Read-only on the engine tree; the builder writes, the reviewer
reads (LAP0 precedent).*
