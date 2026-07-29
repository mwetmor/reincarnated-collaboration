# Finding — 2026-07-29 — WR2-ENCGEO Cell B + Cell B-FIX (combatant collision, surface-to-surface range)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **CLEAR-with-notes** (3 WARN, 7 INFO; no BLOCK)
**Target:** engine `6dca36a` + `4f09e35`, reviewed as ONE landing (charter §8.12)
**Developer:** gamora
**Run:** WR2-ENCGEO-2026-07-29, conductor gandalf. Charter §3 gates S-1 / S-4 (**S-2 explicitly NOT
this gate**, R-WR2-11). Rulings applied: R-WR2-3/-7/-8/-11/-12/-14/-16/-17.
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity), 6
(cross-seam round-trip)
**Disciplines cited:** #1, #3, #4, #10, #11, #12

---

## What I found

The landed law conforms to spec §E's frozen rows and to R-WR2-16's erratum text, the flag-OFF path is
the legacy law verbatim, and every quantitative claim I re-measured reproduced — several to 17
significant figures. I wrote my own S-1 checker from the charter §3 predicate (no engine import, no
reuse of gamora's driver), **validated it on the preserved HALT battery first** so that a PASS could
not be a silently-inert instrument, and then ran it on the B-FIX battery: 450/450, worst slack
−0.000998449474877816 m, 0 violating pair-samples of 323,780. I re-fired the full armed battery from
the clean committed tree and byte-compared it against the banked artifacts: **450/450 traces identical,
the only differing bytes in the entire battery being the header's `engine_git_hash`
(`6dca36a-dirty` → `4f09e35`)** — which simultaneously closes the artifact-provenance question and
supplies a third independent determinism replicate. The full regression name-diff is empty both
directions and the two name sets are byte-identical. What I did falsify is characterization, not
mechanism: the cell note and math note describe the worst-slack pair as "mob↔mob … not a wall pair at
all," and it is neither — it is player↔mob with both bodies sitting on the south-wall clamp; and the
residual chain is anchored on a corner-pinned player, not on free pack geometry. The conclusions those
sentences support survive; the sentences do not. Separately, the frozen `ITER_MAX = 8` has **zero**
remaining headroom on the measured worst case, not the "factor-of-four margin" the math note claims,
and two production comment blocks still carry the NaN mechanism this run formally errata'd.

---

## 1. Full regression, name-diff law (Obligation 1) — **PASS, empty both directions**

Run **alone**, foreground, tree frozen at `4f09e35`, no parallel suite, no worktree — per the B-FIX
ledger's own catch (charter §8.11, Discipline #3 generalization).

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6084 passed, 3 warnings, 21 errors in 1206.20s (0:20:06)   EXIT=1

baseline names: 81   mine: 81
removed (in baseline, not mine): 0
added (mine, not baseline):      0
name sets byte-identical:        YES
```

Baseline: `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`
(81 names, pinned at `9bfbdda`+ per Cell-A INFO-1). `60 failed / 21 errors` reproduces the baseline
exactly; `6084 passed` is the baseline's `6082` plus two — the arithmetic the name-diff cannot show.
This independently reproduces gamora's Run 3 to the count. Adjacent-suites-green was not used as a
criterion anywhere in this review.

**Judging the 2-test delta** (`tests/test_wr2_b_body_separation.py`, 40 → 42; the file passes 42/42):

- `test_both_bodies_clamped_leaves_a_residual_that_is_COUNTED_not_silent` — **good, and load-bearing.**
  Builds a 1.6 m corridor so both 0.5 m bodies are pinned against opposing walls, and asserts the
  predicate is violated **and** `(resid, resid_m) == (1, 0.4)`. This is the branch §B-6 exists for; it
  proves the tripwire is live rather than merely unfired, and it pins R-WR2-3's "the boundary wins"
  ordering. Derived from spec geometry, not a magic constant (Discipline #9).
- `test_shortfall_transfer_never_exceeds_the_gap_partial_clamp_slides_the_wall` — **good.** Pins the
  `[0, share]` bound from math note §12.2 on the partial-clamp (wall-slide) case, and asserts the pair
  lands **at or beyond** contact with the over-resolution bounded by the forced perpendicular slide.
  This is the assertion that stops the transfer from being an unbounded correction.

Neither test weakens an existing guard, widens an exclusion set, or hard-codes a value the mechanism
should derive. The rewritten HALT test
(`test_wall_pinned_SMALL_body_NOW_reaches_the_predicate_R_WR2_16`) monkeypatches `BODY_SEP_ITER_MAX`
to 2 **inside the test only** to make the "≤ 2 sweeps" claim mechanical; the production constant is
untouched and `test_iter_max_and_eps_are_the_frozen_values` still asserts `8 / 0.001 / 1e-6`. That is
strengthening, not drift.

---

## 2. Frozen-row conformance (Obligation 2) — **CONFORMS on every row**

Read against spec §E and the §B-2 erratum banner, in `spatial_engine.py`:

| Frozen row | Site | Verdict |
|---|---|---|
| `ITER_MAX = 8` | `:183` | ✅ unchanged; asserted by test |
| `ε_touch = 0.001` | `:181` | ✅ unchanged; asserted by test |
| separation predicate `d ≥ rᵢ+rⱼ` | `:2368-2370` (`gap = (rᵢ+rⱼ) − d`; `gap ≤ ε → continue`) | ✅ |
| split law, area-weighted `r²` | `:2180-2202` | ✅ zero-denominator guard only; no actor branch |
| one law everywhere (R-WR2-12) | `_body_separation_split` has no player/mob/boss test | ✅ |
| index order over `all_entities` | `:2357-2364`, plain `range(n)` on the caller's list | ✅ no sort, no filter-and-reindex |
| dead-exempt, skipped IN PLACE | `:2359-2364` | ✅ `continue`, never `remove` |
| clamp OUTERMOST, unconditional | `:2438-2439` | ✅ after the sweep loop, over all entities |
| coincident fallback (§B-5) | `:2154-2177` — `normalize(spawnᵢ−spawnⱼ)` then `(1.0, 0.0)` | ✅ deterministic, RNG-free |
| §B-6 counter semantics (pre-correction) | `:2345-2349`, `:2430-2431`, `:2441-2443` | ✅ unchanged |
| both flags default `False` | `:2209`, `:3130`, `:7273` | ✅ |

**The R-WR2-16 transfer matches the erratum banner clause by clause** (`:2386-2429`): realized
post-clamp displacement measured per pass along the normal (`:2407-2408`); annulled magnitude
transfers to the pair partner in the same pass, partner re-clamps (`:2411-2418`); same index order,
zero RNG, in-place float adds, no accumulate-then-sum (§D-4 survives); `ITER_MAX` untouched; S-1
predicate untouched; **no corner special case beyond what the transfer gives** — the transfer is
applied once per pair per sweep and explicitly not iterated to a fixed point (`:2419-2429`), so the
second-order both-clamped shortfall falls through to §B-6's counters rather than into a branch.

Both shortfalls are computed **before** either is written (`:2407-2410` precede `:2411`), so the two
transfers act on disjoint bodies from a common measured state — the "no new ordering dependency"
claim is true as built, not merely as documented.

---

## 3. Flag-OFF byte-identity (Obligation 3) — **CONFIRMED, statically and dynamically**

**Static, strong form.** I extracted the executable lines of `_apply_soft_collision` at `9bfbdda` and
at HEAD and diffed them. The legacy body differs in exactly three places, all accounted for:

1. signature gains `*, body_separation_v2: bool = False` and a `tuple[int, float]` return;
2. `if body_separation_v2: return _apply_body_separation_v2(...)` dispatch at the top, and
   `return 0, 0.0` at the bottom;
3. SS-B-2: `others = [e for e in entities if e not in bosses]` →
   `others = [e for e in entities if not any(e is _b for _b in bosses)]`.

Nothing else in the legacy spring, the 80 %-of-contact threshold, the `d > 0.0001` skip, the boss
hard-body block or the final re-clamp moved by a character. The B-FIX diff on `spatial_engine.py` is
**two hunks, both inside `_apply_body_separation_v2`** — unreachable at `body_separation_v2=False`.
The second SS-B-2 conversion (`policy/seam.py` `choose_target`) is the same shape.

**Dynamic.** I did not re-run gamora's two-tree comparison; instead I ran the stronger test available
to me — see §4(d) — which byte-compares 450 armed traces produced at HEAD against the banked ones and
finds a single differing field in the whole battery. Flag-OFF non-perturbation is additionally carried
by the regression's own `TestByteIdentity` digests, which are in the 6084 passing and were the tests
that caught the unconditional-key leak in the first place.

---

## 4. Independent falsification (Obligation 4) — **four claims re-measured; two characterizations falsified**

### (a) S-1, with an instrument proven live before it was trusted

I wrote `/tmp/jr_s1_checker.py` from the charter §3 predicate alone: living pairs only, radii read
from each trace header's per-entity `entity_radius_m` (never a global), `d ≥ rᵢ+rⱼ − 0.01` on **every**
tick of **all 450** traces. No engine import, no shared code with gamora's driver.

**Positive control first.** Run against the preserved HALT battery `wr2_cell_b_s1/`:

```
traces                : 129 / 450 PASS
worst slack           : -0.25216185346109277
violating pair-samples: 81861 / 340828
violating ticks       : 81756 / 133848
per-leg pass          : R2_proxy 40/150 · R2_proxy_resists_low 40/150 · R3 49/150
```

Every figure matches the HALT record to 17 s.f., including the per-leg split. **The checker can
detect failure**, so its PASS on the B-FIX battery is a measurement rather than an absence.

**B-FIX battery `wr2_cell_b_s1_r2/`:**

```
traces                : 450 / 450 PASS S-1
worst slack           : -0.000998449474877816
violating pair-samples: 0 / 323780
violating ticks       : 0 / 134460
```

Identical to gamora's claim in every digit, including the pair-sample denominator. **S-1 PASSES.**
The worst slack is the `gap ≤ ε_touch → continue` skip threshold appearing as its own value
(`1.0 − 0.9990015505251222 = 0.00099845 ≤ 0.001`) — a correctly-converged solver's worst case, and an
order of magnitude inside S-1's 1 cm.

### (b) The 7 residual ticks — located and verified independently

From the three leg reports, without reading gamora's census: **7 ticks total** (3 + 3 + 1), seeds
**74000801 / 74000816 / 74000824**, **all `mixed_pack`**, max `0.0012118003135626054`. Worst
**post-solver** overlap recomputed from the emitted frames on each flagged fight:

| seed | my measurement | gamora's | pair |
|---|---|---|---|
| 74000801 | −0.0009484870212331797 | −0.00094849 | `hero_boar_h07_0` ↔ `slitha_melee_b01_2` |
| 74000816 | −0.0007134239228215877 | −0.00071342 | same |
| 74000824 | −0.0009484870212331797 | −0.00094849 | same |

All inside `ε_touch`. **The disposition holds:** counter non-zero + S-1 green = the tripwire fired on
a pre-correction reading of sweep 8 and the tick converged anyway. The registered prediction of 0 was
missed and is reported as missed (math note §12.5) — Discipline #11 honoured, nothing widened to
absorb it.

### (c) The shuffled-order test does prove order-dependence

`test_shuffled_order_differs_the_invariant_is_real` runs the solver on the *same* four-body pile under
`[0,1,2,3]` and `[3,1,0,2]` and asserts the resulting position maps **differ** — and then asserts both
orderings still satisfy the predicate. That is the correct shape: it proves the §D-2 ordering
invariant is load-bearing (asserting they *matched* would be asserting Jacobi), while showing order
changes *where* bodies land and not *whether* they separate. Companion tests pin
non-reordering of the caller list, dead-skipped-in-place, and `SpatialEntity` unhashability.

### (d) Provenance — the strongest check, and it closes cleanly

The banked B-FIX traces stamp `engine_git_hash: 6dca36a-dirty`: the graded battery was fired from an
**uncommitted** tree, so nothing mechanically bound the S-1/S-4 evidence to `4f09e35`. Cheap to
falsify, so I falsified it. From the clean committed tree at `4f09e35`, tracked `src/` and `tests/`
verified diff-free, I re-fired the full 3-leg armed battery (9.4 s wall) and byte-compared all 450
traces against the banked set:

```
traces compared              : 450
identical modulo header prov.: 450
genuinely differing          :   0
differing header fields      : ['engine_git_hash']
engine_git_hash pairs        : ('6dca36a-dirty', '4f09e35')
S-1 (re-fire)                : pass=True 450/450 worst_slack=-0.000998449474877816
RESIDUALS (re-fire)          : ticks=7 max=0.0012118003135626054
```

**The only differing bytes in the entire 450-trace battery are the commit stamp itself.** The banked
evidence *is* the committed code. This is also a **third** determinism replicate — a different
process, a different tree state, hours later — corroborating S-4 beyond gamora's two, and it means my
§4(a) S-1 result applies to HEAD and not merely to an artifact.

### (e) ⚑ FALSIFIED — two characterizations, both about walls

Cell note §B-3 and math note §12.5 state the worst-slack pair is *"a **mob↔mob** pair
(`gd-werewolf-kitcal-1` ↔ `hero_boar_h07_0`) … **not a wall pair at all**."* Both halves are wrong.

- `gd-werewolf-kitcal-1` is the **player** — the trace header records `"side":"player",
  "is_player":true, "entity_radius_m":0.5`. The pair is **player↔mob**, contact 1.0 m.
- At `mixed_pack__none__seed74000806` tick 80 both bodies sit at **y = 0.5**, which is exactly the
  south-wall clamp for a 0.5 m radius on the 36×36 arena. Both are wall-clamped.

And math note §12.5's *"Every flagged pair is mob↔mob in a dense pack chain, not a wall pair"* is
incomplete on the same axis. At the residual tick of seed 74000801 the geometry is:

```
tick 93   player  (35.500000000, 0.500000000)   <- CORNER-pinned: x = 36.0 − 0.5, y = 0.5
          boar    (34.500000000, 0.500000000)   <- south-wall pinned, blocked in +x by the player
          slitha  (33.557312200, 0.830822667)
```

The *pair* is mob↔mob, but the *chain* terminates on a corner-pinned player. **The mechanism survives
both corrections** — the worst slack really is the ε-skip threshold (the separation normal there is
x-aligned, so the y-clamp annuls nothing), and the residual really is §B-6's pre-correction
over-report (verified post-solver, §4(b)). But the sentences the conductor will read when grading say
"no wall is involved," and a wall is involved in both. See **WARN-1**. Discipline #10, #11.

---

## 5. D-2 / D-3 obligations (Obligation 5) — **DISCHARGED**

**D-2 ordering invariant, incl. the player-index-0 bias:** present in the math note (§6.2) and, better,
in the solver's own docstring at `spatial_engine.py:2324-2337` — "never sort / never
filter-and-reindex / never iterate a set or a dict keyed on entities," with the bias named explicitly
("the player is index 0 and resolves against every mob before any mob↔mob pair"). Named before
discovery, as spec §D-2 asked.

**D-3 sweep, re-run with my own tool.** AST walk over every `ast.Compare` carrying `In`/`NotIn` across
all 34 `.py` files in `spatial_gauntlet/` (a text grep cannot separate `x in y` from `for x in y` —
Discipline #4): **104 memberships, zero with an entity on the left and a container of entities on the
right.** The 6 that survive my entity-shaped filter are all string / tuple / constant-set membership
(`role in _SPENDER_ROLES`, `e.name in _AURA_RIDER_NAMES`, …). A targeted grep for
`(not )?in (bosses|alive_mobs|entities|all_entities|mobs|others|targets)` returns nothing outside
`for` statements. Both converted sites confirmed in identity form
(`spatial_engine.py:2272`, `policy/seam.py:72`). **Obligation discharged.** See **INFO-3** on the
denominator.

---

## 6. SS-1 (Obligation 6) — **CONFIRMED**

`wr1_battery_2/` and `wr1_battery_2_aim/`, across the combined landing:

- `git status --porcelain` on both roots: **empty**
- `git diff --stat 9bfbdda..HEAD` on both paths: **empty**
- 454 + 454 = 908 files, unchanged count
- newest mtime anywhere in either root: **11:40:41** (Cell A's own emission). **Zero** files touched
  after 12:00; Cell B's first commit is 13:20:53.

The B-FIX battery landed in the sibling `wr2_cell_b_s1_r2/` and the HALT battery `wr2_cell_b_s1/` was
**preserved, not overwritten** — which is what makes §B-10's before/after diff and my own §4(a)
positive control possible at all. That was the right call and it paid for itself inside this review.

---

## 7. R-WR2-17 scope check (Obligation 7) — **CONFORMS**

`_select_skill_for_entity`, `spatial_engine.py:2620-2622`:

```python
if body_separation_v2:
    return nearest_dist <= range_m + nearest_target.entity_radius
return nearest_dist <= range_m
```

- **All attackers:** `:2336`-vicinity is the shared selector — the player action phase (`:5483`) and
  the mob action phase (`:5683`) both route through it with `self._body_separation_v2`. There is no
  actor qualifier, so the ruling applies to mobs and the boss as ratified.
- **Gated to the flag:** yes, single `if`.
- **Centre-to-centre verbatim when OFF:** yes, the untouched expression on the fallthrough.
- Radius read from `nearest_target.entity_radius`, never a global — consistent with §B-1.
- The pre-existing `range_m = float(skill.get("range_m") or 2.0)` falsy-zero coercion is inherited
  and **reported rather than silently repaired** (cell note §2). Correct: repairing it here would be
  an unflagged behaviour change outside B's scope.

See **INFO-2** for the one consequence of SS-B-1 that is not yet on anyone's list.

---

## Rationale

Verdict is **CLEAR-with-notes** rather than CLEAR because of WARN-1/-2/-3, and rather than BLOCK
because nothing in the landed *law* is defective: S-1 reproduces at 450/450 under an instrument proven
able to fail, the frozen rows conform row by row, the flag-OFF path is provably the legacy law, the
banked evidence is provably the committed code, and the regression name-diff is empty. Under
**Principle 5**, severity is proportionate: WARN-1 is a wrong *characterization* attached to a right
*conclusion*, WARN-2 is a **forward** margin risk that lands in Cell C's lap and not in B's, and
WARN-3 is a stale rationale in a comment whose *conclusion* every other artifact has already
corrected. None of the three is a defect a re-run would change.

**Principle 1 (math-before-code) is satisfied unusually well here.** The math note precedes the
implementation (§12 opens by saying so), the HALT was diagnosed to a closed-form fixed point that
returned the scenario's actual boss speed, and R-WR2-16's resolution was argued as arithmetic
(`q → 0`, `Δ` drops out) rather than as preference. **Principle 2**: adjacent-suite smoke fired first,
then the full regression alone. **Principle 3 / 6**: MIGRATION.md is filed with the landing, names
star-lord and drax by seam, and leads with "THIS ARM IS MECHANICAL, NOT EMISSION-ONLY" — which is the
right warning to put first for a flag that moves geometry rather than instrumentation.

Two process behaviours deserve naming as good rather than merely acceptable. The HALT was reported
with the resolution *costed but not taken*, against a unit test that a resolution would be forced to
change — that is what stops a spec defect from being quietly absorbed into a build. And the missed
prediction (residual = 0, measured 7) was recorded as missed, with the counter's semantics defended
rather than redefined to make the miss disappear.

---

## WARN

**WARN-1 — the two "no wall involved" claims are false, and they are the sentences the conductor will
grade on.** Cell note §B-3 and math note §12.5 identify the worst-slack pair as "mob↔mob … not a wall
pair at all"; it is player↔mob (`gd-werewolf-kitcal-1` is `is_player: true`) with **both** bodies on
the south-wall clamp at `y = 0.5`. Math note §12.5's "every flagged pair is … not a wall pair" is
likewise incomplete: the residual chain terminates on a **corner-pinned player** at `(35.5, 0.5)`
(§4(e) for the tick-93 geometry). The conclusions are unaffected — the worst slack is the ε-skip
threshold because the normal is x-aligned and the y-clamp annuls nothing, and the residual is the
pre-correction over-report, both verified in §4 — but the claim that no wall-involved configuration is
residual any more is stated more broadly than the measurement supports. **This matters forward,** not
backward: the conductor's read of "the corner is solved" and Cell C's risk model both rest on it.
*Discipline #10 (attribution clarity — change one thing, measure one thing), #11.*
**Remedy:** an erratum on cell note §B-3 and math note §12.5 restating both as "the pair's separation
normal is unaffected by the clamp" rather than "no wall is involved." No code change, no re-run.

**WARN-2 — `ITER_MAX = 8` has ZERO measured headroom, not the "factor-of-four margin" the math note
claims, and it is a FROZEN row.** Math note §12.4 concludes "`2 ≤ ITER_MAX = 8` with a factor-of-four
margin." That accounting is correct for an isolated pair and is falsified as a global statement by
§12.5's own measurement. From the solver's control flow (`spatial_engine.py:2355-2443`),
`collision_residual_ticks` can increment **only** if all 8 sweeps executed **and** the 8th still
observed `gap > ε_touch`. So on each of the 7 measured ticks the entire frozen budget was consumed and
the ninth sweep was the one that would have closed it — the margin on the observed worst case is
**1×, not 4×**. Nothing is wrong today (S-1 is green, verified twice). But Cell C is a movement policy
whose explicit purpose is to change where bodies sit relative to walls and to each other, `mixed_pack`
is the tier where chain propagation binds, and **raising `ITER_MAX` is spec §E drift and R-WR2-16
refused it** — so if a post-C chain exceeds 8, the remedy is not available without a fresh conductor
ruling. *Disciplines #1, #11.*
**Remedy:** correct §12.4's margin sentence to distinguish per-pair cost from chain cost; and add
`collision_residual_ticks` to Cell C's and Cell BAT's reported gates as a **watched** quantity (it is
already emitted — this costs nothing) so a rise is seen when it happens rather than at S-1's failure.

**WARN-3 — SS-B-2's only in-code rationale is a mechanism this run has formally errata'd, on two
UNFLAGGED default-path changes.** `spatial_engine.py:2258-2271` and `:2330-2331`, and
`policy/seam.py:58-72`, all still state the NaN self-miss as "the live hazard" — the boss failing
`e not in bosses` against its own entry. Charter §8.9 banks the erratum, spec §D-3(3) carries the
banner, math note §6.4 carries the correction, the cell note §3 carries it, and
`test_entity_membership_hazard_is_value_equality_not_the_nan_self_test` pins it. Only the production
comments do not — and they are the sole justification a future reader finds for two changes that land
**without a flag on the default path**. The correct rationale (§D-3(1): value-equality between
distinct entities, held off only by unstated `entity_id` uniqueness) is *stronger*, because it makes
the byte-identity claim unconditional rather than NaN-conditional. *Discipline #12 (a semantic shift
must be framed correctly, not merely framed), #11.*
**Remedy:** replace the NaN paragraph in both comment blocks with the §D-3(1) rationale and cite the
erratum. Documentation-only; **I approve this class directly under ADR-002** — it needs no conductor
ruling and no re-run.

---

## INFO

- **INFO-1 — the artifact-provenance gap is real but is now CLOSED by this gate, not by the cell.**
  The banked B-FIX traces stamp `6dca36a-dirty`; the graded S-1/S-4 evidence was produced from an
  uncommitted tree and nothing in the cell bound it to `4f09e35`. Cell A hit the same class and
  re-fired clean (charter §8.2); Cell B did not. I closed it by re-firing from the committed tree —
  450/450 identical modulo the commit stamp (§4(d)). **Standing recommendation for Cell C and Cell
  BAT:** fire the graded battery from a committed tree, or state the straddle in the cell note. The
  detector gamora built in SESSION 90 exists precisely to make this visible, and here it worked — the
  stamp told the truth and nobody read it.

- **INFO-2 — SS-B-1 moved the SELECTOR but not the AoE hit kernels, opening a narrow select-but-whiff
  window that did not exist before.** `_compute_circle_hits` uses `aoe_radius` (`AOE_RADIUS_DEFAULTS`
  3.0–4.5, `spatial_engine.py:190-197`) measured **centre-to-centre** and untouched by the flag.
  Against the 1.5 m-radius boss a `burst_damage` circle (radius 3.0) can now be selected at up to
  `2.0 + 1.5 = 3.5` m and hit nothing. Cone (`CONE_RANGE_M = 5.0`) and line (`LINE_RANGE_M = 20.0`)
  have headroom; circle does not. Reachability under **B alone** is low — separation holds at 2.0 and
  the player has no contact-range policy — but **C's preferred-range band is designed to hold the
  player further out**, which is exactly the direction that walks into the window. Not a Cell B defect
  (the selector is where R-WR2-8 names the fix) and not S-3's problem yet. **Carry into Cell C's build
  obligations and the S-6 diff table.**

- **INFO-3 — the D-3 sweep's denominator does not reproduce; its result does.** The cell note and
  math note report "66 compares audited … re-sweep 64." My AST walk over the same package finds
  **104** `In`/`NotIn` compares across 34 files (`spatial_engine.py` 47, `kitcal_g5_harness.py` 13,
  …). The substantive claim — zero entity-container memberships remain, both hits converted — is
  independently confirmed (§5). But the sweep's *scope* is not reconstructible from the note's
  description, which weakens it as a re-runnable obligation for Cell C. **Remedy:** state the file set
  or commit the sweep script.

- **INFO-4 — AGENT_STATE is stale relative to the final landing (recurrence of Cell-A INFO-7).**
  `src/reincarnated/simulation/AGENT_STATE.md`'s header is SESSION 92 and still reads "**it HALTS ON
  S-1**", "129/450 traces pass", "40 new unit tests", and "NOT PUSHED". The landing is S-1 450/450, 42
  tests, and charter §8.11 records the push. A reader arriving at the seam checkpoint gets the HALT,
  not its resolution. Second occurrence in two cells; worth making the B-FIX-style appendix the
  default shape for any cell that lands in two commits.

- **INFO-5 — Principle 6 round-trip: substance present, declared form still absent (recurrence of
  Cell-A INFO-5).** `MIGRATION.md` names star-lord and drax as consumers, leads with the
  mechanical-vs-emission-only distinction, and states the non-poolability rule and the branch key
  consumers must read. What it does not carry is a declared acknowledgement round-trip — no consumer
  seam has signed that they have read it. Non-blocking (the flag is default-OFF and nothing is owed to
  ship, as the doc itself says), but the WR2 AFTER-baton is where drax actually consumes this and the
  ack should land before then.

- **INFO-6 — the HALT battery's preservation was load-bearing for THIS review, not only for the
  record.** `wr2_cell_b_s1/` being left in place beside `_r2/` is what let me validate my own S-1
  instrument on a known-failing corpus before trusting its PASS (§4(a)). A review that can only ever
  return PASS is not a gate. Emitting the resolution to a sibling rather than overwriting is worth
  promoting from a cell-level choice to a run-level convention.

- **INFO-7 — the Discipline #3 generalization is correct and should be ratified.** Charter §8.11 and
  cell note §B-5 derive "no parallel regens of the same seed" → **"no parallel pytest suites sharing
  an editable install"** from a diagnosed `__pycache__` listdir/remove race, with the confirming
  detail that a bare `cd <worktree> && pytest` imports the *main* tree's package via
  `_editable_impl_reincarnated_engine.pth`. It corroborates WR1 INFO-8. I honoured it in this review
  (regression run alone, all trace analysis done on JSON with no package import). **This is a
  discipline refinement and therefore mine to draft under ADR-002**; queued as a wave-tail item rather
  than written here, so it lands as one amendment with whatever Cell C adds.

---

## Action

- [ ] **gamora (documentation-only, jack-ryan-approved under ADR-002, no re-run):** erratum on cell
      note §B-3 + math note §12.5 for **WARN-1**; correct math note §12.4's margin sentence for
      **WARN-2**; replace the NaN rationale in `spatial_engine.py:2258-2271` / `:2330-2331` and
      `policy/seam.py:58-72` for **WARN-3**; refresh AGENT_STATE to the B-FIX landing (**INFO-4**).
- [ ] **gamora (at Cell C, non-blocking):** carry **INFO-2** (circle-AoE select-but-whiff window)
      into the C build obligations; state the D-3 sweep's file set or commit the script (**INFO-3**);
      fire Cell C's graded battery from a committed tree (**INFO-1**).
- [ ] **gandalf (conductor):** note **WARN-2** — `ITER_MAX` headroom is 1×, not 4×, and it is a frozen
      row R-WR2-16 already refused to raise; recommend adding `collision_residual_ticks` as a watched
      quantity at Cell C and Cell BAT. Cell C's flag-OFF baseline **confirmed** to pin at `6dca36a`:
      B-FIX adds no key to any returned dict or report surface (verified — the diff is two hunks inside
      `_apply_body_separation_v2`). **Cell C is released to fire.**
- [ ] **Matt:** **no decision required by this finding.** R-WR2-8/-17's veto window closes at this
      verdict per charter §8.12; this gate found the surface-to-surface build conformant to the ruling
      as written, and **INFO-2** is the only consequence of it not yet on a list — it is Cell C's to
      carry, not a reason to reopen the ruling.

---

## References

**Governing**
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` (§2, §3, §7 R-WR2-7..-17, §8.8–8.12)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` (§B incl. both erratum banners, §D, §E, §G)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-a.md` (INFO-1 baseline pin, INFO-5/-7 recurrences)

**Reviewed**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
  (`:168-184` frozen constants · `:2154-2202` normal + split · `:2205-2289` legacy path, **`:2258-2271` WARN-3** ·
  `:2292-2443` the v2 solver, **`:2330-2331` WARN-3**, `:2386-2429` the R-WR2-16 transfer · `:2595-2622` SS-B-1 ·
  `:190-197` + `:1528-1590` AoE kernels, **INFO-2** · `:7608-7613` conditional key emission)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/policy/seam.py` (`:58-72` SS-B-2, **WARN-3**)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` (`:645-646`, `:869-870`, `:1797-1798`, `:1856-1858`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_b_sep_2026_07_29.py`
- `~/Games/reincarnated-engine/tests/test_wr2_b_body_separation.py` (42 tests; the 2-test delta judged in §1)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wr2-b-body-separation-2026-07-29.md` (§6.2, §6.4, **§12.4 WARN-2**, **§12.5 WARN-1**, §12.6)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-29 entry, **INFO-5**)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (**INFO-4**)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-b-collision.md` (incl. B-FIX appendix; **§B-3 WARN-1**)

**Evidence measured by this review**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_cell_b_s1_r2/` (450 traces + 3 leg reports; S-1 + residual census recomputed)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_cell_b_s1/` (preserved HALT battery — instrument positive control)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/`, `…/wr1_battery_2_aim/` (SS-1)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt` (81-name baseline)
- Scratch (not banked): `/tmp/jr_s1_checker.py`, `/tmp/jr_d3_sweep.py`, `/tmp/jr_wr2_cellb_regression.txt`, `/tmp/jr_wr2_refire/`

---

*jack-ryan, 2026-07-29. Gate 2 on the combined `6dca36a`+`4f09e35` landing. The instrument was proven
able to fail before its PASS was reported. **Cell C holds no longer — CLEAR-with-notes.***
