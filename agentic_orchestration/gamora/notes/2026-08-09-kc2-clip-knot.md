# KC2 CLIP-KNOT — the gate was right, my § D sentence was wrong, and the repair is eight knots

**Date:** 2026-08-09 · **Author:** gamora (simulation seam) · **Conductor:** gandalf, RUN-CONDUCTOR
**Commission:** **R-L82-1** (ledger L-82(b), meta `78ecaf11`), fired from star-lord's
`G-LOCO-ONE-TRAJECTORY` red (halt note 2026-08-09 § 4 H-1, engine `1ef5919a`).
**Law:** the R-L80-2 DETERMINISM VERIFICATION LAW, unchanged and binding.

---

## 0 · VERDICT LINE

| | |
|---|---|
| **Determinism** | **EXACT on all three legs.** LEG-2's OFF/ON digest is `fcf57111…` — **the same value as L-81**, which is the sharpest single statement available: the recorder was extended and the simulated surface did not move by one bit. |
| **Knots** | 995 → **1,003** (+8). Histogram `{2: 61, 3: 271, 5: 4, 6: 8}`. Kinds gain `clip: 13`, `unclip: 0`; **every other kind count is identical**. |
| **Artifact** | `src/reincarnated/simulation/output/kc2-phase-e-actor-paths-E-s09-cp150-R-L82-1-20260809_041421.json` |
| **SHA-256** | **`2ba67fc152c3a688e3e41ab1c5c3de4a1552baa28390554f5f174210de30cca7`** |
| **Additivity of the knot set** | **SUBSET-EXACT** — all 995 prior knots reproduce at the same `(run_tick, x, y)`; 5 gained a tag; 8 are new. |
| **One-trajectory cross-check** | **PASS** — 1,415 rows, max \|Δ\| = **0.000e+00 m**, 0 beyond 0.002 m. **With a caveat I state myself, § 5.** |
| **Tests** | knot file 29 → **39**; KC2 + locomotion + blast radius **382/382**; red tree at the L-74(d) baseline. |

---

## 1 · WHAT WAS ACTUALLY WRONG — and it was in my note, not only in my code

The 2026-08-08 predicate keyed on **direction**. § D of the math note then asserted speed fidelity
in one sentence:

> ~~Within a leg ‖x(t_{k+1})−x(t_k)‖ = v_a·period exactly **(unmodified `min`)**…~~

The parenthetical was an **assumption that the `min` never binds inside a leg, carried as if it
were a derivation.** It binds on every arrival. That is a **speed change with no direction change**
— invisible to the 1e-9 rad bend test, to the dwell boundaries and to the markers alike.

⚑ **The most useful thing I can say about my own checks: the polyline-length check was truthful
and irrelevant.** `max |Δ| = 2.1e-13 m` is a real measurement of a quantity that is
**parameterisation-blind** — length does not care how time is distributed along a fixed polyline.
The § F determinism law compares the run to itself and cannot see it either. **Neither of my two
strongest checks was capable of falsifying the claim they appeared to support.** Only a check that
re-derives position at a tick and compares it against an *independently emitted* position can, and
that check lived in another seam. The gate did its job; my note's § D is now a struck sentence with
the reason printed beside it, corrigenda-forward, rather than a quiet edit.

---

## 2 · THE PREDICATE — a knot is a change of VELOCITY, and direction is half of one

Math note § C.1, written before the code (Discipline #1). Clause **C2b**:

> record a knot at the pre-step position whenever `travel ≠ _last_travel` on a step that does not
> already bend — where `_last_travel` is the per-step travel **of the leg beginning at the last
> recorded knot**, refreshed only at a knot, exactly as `_last_dir` already was.

**Enumeration first, instance second** (the commission asked for this and it is the part that makes
the fix a fix rather than a patch). Reading `step` as the only place a position moves, the per-step
displacement magnitude is exactly one of three things:

| | case | condition | `travel` |
|---|---|---|---|
| S1 | FULL | `slack ≥ v·dt` | `v·dt` — bitwise the same double every step of a leg |
| S2 | CLIPPED | `0 < slack < v·dt` | `slack`. **Two sources:** (a) engage-ring arrival, (b) exact patrol-node arrival |
| S3 | ZERO | `slack ≤ 0` | 0 — a dwell |

and **nothing else in the model**: `speed_m_per_s` is assigned once in `build_mover` and never
re-assigned (pinned by a test that also greps `step`'s source), `Δt` is the wave's period passed at
the single call site with no partial final tick, `d_engage_m` is a module constant. There is no
acceleration term, no haste/slow modifier, no terrain cost, no collision push-out. **Standing
obligation recorded in the note:** adding any one of those re-opens this predicate, because the
proof consumes the completeness of that three-case partition.

The prior predicate covered S3 (`halt`) and every direction change (`bend`), and **left S2
uncovered**. That is the whole defect, stated as a gap in a partition rather than as a bug.

**The predicate is source-agnostic:** it never asks *why* a step was short, so S2(a) and S2(b) are
handled by one clause. R-L82-1 names the engage ring; the code does not.

### 2.1 · Exactness, proved (§ C.1.3)

Every knot is an **end-of-tick** position (C1/C2/C2b/C3 record `pre` at `k−1`; markers record
`xy_post` at `k`) — so the vertices are samples of one function on the integer grid, no half-ticks.
Between consecutive knots at `a < b`, *no knot was recorded*, so by the contrapositive every step in
`(a, b]` carries the leg's direction (within ε) **and** the leg's travel exactly. The displacement
per step is therefore a constant vector, and the interpolant equals the true position to within the
already-computed `L·ε ≤ 1.25e-7 m`. Three boundary cases are checked rather than waved at: a marker
knot lies *on* the uniform sub-leg it interrupts; the spawn knot is a true end-of-tick position
because the body is not stepped before `k*`; a dwell has both endpoints because dedup is on the
**triple**.

### 2.2 · The mirror case, in the predicate even though this run has none

`travel < v·dt` alone would leave the **rise back out** of a clipped step unrecorded — clipped step,
then a full step on the *same bearing*, then no knot until much later, and the interior
non-uniformity is back one layer down. Physically that is a player retreating exactly along the
approach bearing, which `CAMP_THEN_COLLECT` makes reachable in principle. So C2b is symmetric and
emits `unclip`. **Measured on this run: 0.** A synthetic test exercises it. A predicate that is
right only on the run it was written for is a fitted predicate.

---

## 3 · THE DETERMINISM LAW — re-run in full, not inherited

Three legs, printed by the driver, no tolerance parameter anywhere in it:

```
LEG-1  unmodified `execute_run` vs the committed artifact   526 leaves,     0 diffs   EXACT
LEG-2  recorder OFF vs ON, whole emitted surface        114,680 leaves,     0 diffs   EXACT
       sha256 OFF = sha256 ON = fcf571110da067d36e7aec842a34bbe4fe37f380b8fb4c591d871c5e6e5ecc7a
LEG-3  the counts ledger row L-80 published                 12 pins,  12/12 match     EXACT
```

⚑ **`fcf57111…` is the same digest L-81 recorded.** Not "no differences found" — the identical
number, from a build with a new clause inside the step loop. One named exclusion, printed:
`wall_s`, a host wall-clock reading and not a simulated quantity.

Re-execution reproduces the artifact byte-identically apart from `started_utc` / `wall_s` (checked
on a second run, then the duplicate was deleted). The results JSON of record was opened READ-ONLY.
**The prior knots artifact was not touched and stays on disk** — it is the record of the prior
predicate and of what the gate was measuring when it fired.

---

## 4 · RECONCILIATION — 13, not 12, and the 13th is a finding about the metric

Star-lord enumerated **12** non-uniform legs on 12 bodies, all class `contact → engage+halt`.
I measure **13** clipped steps on 13 bodies. They reconcile exactly:

* **12 are his, 1:1.** Of those, **8 produce a NEW knot** — the legs with an interior tick, his 8
  violations — and **4 MERGE** onto the `contact` knot already sitting at that tick. Those 4 are
  precisely his *"four legs span one tick, no interior, harmless"*, and the predicate decided that,
  I did not. **995 + 8 = 1,003.** The expected `~1,007` was the ceiling; the merge is the reason
  it landed lower.
* **The 13th is `w162_a012`** — a p05 ambush body that spawned 2.58 m from the player (outside the
  2.4 m ring, inside the 3 m disc), took **one clipped step** to the ring and died on it. Its entire
  path is that one leg.

⚑ **Why no consumer-side metric could have found it.** The per-leg metric compares each leg's
implied speed to *that body's own maximum*. A body whose whole path is one moving leg is compared
**to itself** — ratio 1, never flagged, however clipped the leg is. That is a structural blind spot
of the metric, not a defect in it: only the source can tell that a step was short when there is no
unclipped step to compare it against. Harmless here (one-tick leg, no interior), but **12 was a
lower bound and is now known to be one.** Same body, incidentally, as one of the six H-4 hit-test
offenders — two unrelated facts about one unlucky ambush spawn.

### 4.1 · What star-lord's HALT PIN should say (his file, his edit — I did not touch it)

The pin asserts `len(nonuniform) == 12` and the docstring predicts it "goes to zero". **It does
not, and should not.** A clipped step is a real speed change and stays non-uniform under that
metric after the repair. What the repair removes is the **interior tick**:

```
non-uniform legs : 12 on 12 bodies · tick spans [1] · all span exactly 1 tick: True
    8 × ('clip',)            -> ('engage', 'halt')
    4 × ('contact', 'clip')  -> ('engage', 'halt')
```

**The true post-repair assertion is `tick_span == 1` for every non-uniform leg** — a leg spanning
one tick has no interior integer tick, so `run_tick` interpolation cannot misplace a body on it.
Full stale/survive table in the MIGRATION entry. Two of his five pins break by design (H-1's and
the four-red wall's), three survive. Nothing of his moves until he repoints the artifact constants,
because he pinned by **digest** — which is why that pinning was the right call.

---

## 5 · ⚑ THE HONEST LIMIT ON MY OWN GREEN

I ran his gate here before handing off, **importing `_path_position` from his validator rather than
re-implementing it** — two implementations agreeing with each other would prove only that they
agree, which is the vacuous-pass class L-82(a) named. Result: **1,415 rows, max |Δ| = 0.000e+00 m,
0 beyond tolerance.**

Then I classified what those rows actually exercise, and the artifact carries the classification:

```
659 rows land ON a knot · 756 inside a DWELL (exact for free) · 0 inside a MOVING leg
```

**After the repair this run has no event row strictly inside a moving leg** — the 8 offenders
became on-knot rows. So the PASS is **necessary but not sufficient**: it never exercises the limb of
the interpolation that does real arithmetic. Reporting "zero error over 1,415 rows" without that
sentence would be an overclaim, and it is stated in the artifact
(`amendment_gates.g2_….coverage_caveat`) rather than left for a reader to notice.

The moving-leg limb is carried instead by § C.1.3's proof and by **synthetic tests that walk a mover
with no wave, no disc, no damage and therefore no event row anywhere** — which is also the
falsification of the rejected `UNION-SUPPLEMENT` (option 4): the predicate reads `travel`, a motion
quantity, and `Mover.step` structurally cannot see an event stream, **so it fires where there is no
evidence to be driven by.** The counterfactual is measured, not asserted: drop the clip vertex from
that synthetic path and the interior ticks move by **0.393 m — 393 position quanta, 196× the gate's
tolerance.**

---

## 6 · SEMANTIC SHIFT, NAMED (Discipline #12)

`path_model` still reads `"piecewise-linear, VERTEX-COMPLETE"`. **The word did not change; its
extension did.** Under the prior predicate it meant *every direction vertex*. It now means *every
velocity vertex*. A consumer who read the old word correctly still read a path that disagreed with
its own damage rows by up to 0.154 m on 8 ticks, on ticks where damage was dealt.

This is filed as a shift and not as a bug fix because a downstream reader who cached the old meaning
holds a stale **belief**, not a stale number — and the number they would compute from the belief
looks perfectly reasonable. Flagged for star-lord: his `_path_coverage_declaration()` sentence
("a knot is recorded at every **direction change**…") is now incomplete on the wire. His surface,
his words; suggested wording is in the MIGRATION entry, not taken.

---

## 7 · TESTS + BLAST RADIUS (Discipline #10 — enumerated, not assumed)

* `tests/test_kc2_actor_path_knots.py` **29 → 39**. New § 9: the clipped step gets a knot with no
  event stream present · interpolation reproduces **every** interior tick of a clipped leg · the
  measured counterfactual without the clip vertex · the `unclip` mirror case · a dwell clears the
  leg travel · `v_a` / `Δt` constancy pinned so the § C.1.1 enumeration stays complete · **every
  non-uniform leg on waves 151/160/170 spans exactly one tick** (the invariant that replaces the
  halt pin) · the merged-tag case stays enumerable.
* Determinism tests kept **as the law**, unedited.
* Blast radius: 13 files reference the seam (`locomotion` / `record_actor_paths` / `PathKnot` /
  `load_actor_path_knots`). Suites run whole: **382/382 green** across KC2 + locomotion + adapter +
  baton + surfaces + channel/disc + energy/devotion + micro-oracles + monster-stats + opposition +
  census + s1-ramp.
* Full tree: **10,443 P / 63 F / 21 E — EXACTLY the L-74(d) non-gating baseline**, unchanged by
  construction (no red node imports this seam).
* Star-lord's adapter suite is green **right now** because it loads the prior artifact by his
  pinned digest. That is the intended state at handoff, not an accident.

---

## 8 · WHAT THIS DOES NOT CLAIM

* **OBJ-1 is not closed.** This is the supply side; the union re-law is star-lord's seam and drax's
  countersign.
* **`v_ref` is still `DECLARED-FREE-PARAMETER`** (HALT-2). A faithfully recorded path through a
  declared-parameter model is a faithful record of *that model*.
* **R-L82-2 / 3 / 4 are untouched** — M-7's box shape, R-LOCO-1's still bodies and the hit-test
  boundary are star-lord's three, and the wall stays red until they land.
* **The exactness proof is for THIS motion law.** Add acceleration, haste, terrain cost or a
  variable tick period and the § C.1.1 enumeration is incomplete and the predicate must be
  re-derived. That obligation is written into the math note, not left in this report.

---

**Deliverables:** math note § C.1 + § D corrigendum · `kc2/locomotion.py` C2b (no `run.py` change —
the plumbing already existed) · artifact `…-R-L82-1-20260809_041421.json` @ `2ba67fc1…` ·
determinism block printed above · `simulation/MIGRATION.md` [2026-08-09] · tests 39 ·
`simulation/AGENT_STATE.md`.
**Refs:** L-80(c) · L-81 · L-82(a)(b) · R-L80-2 · **R-L82-1** · R-LOCA-1 · AC-10.6 · AC-10.11 ·
§ 11.3 · § 11.4 pin 4 · Disciplines #1, #2, #10, #11, #12.
