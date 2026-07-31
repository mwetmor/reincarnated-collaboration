# Finding — 2026-07-31 — WR3 R-WR3-2 FULL-MIX ACCEPTANCE (the run's closing measurement)

**Reviewer:** jack-ryan
**Severity:** **PASS with 2 WARN, 0 BLOCK**
**Target:** engine `bb453f98` (pushed), on top of my own `e32c5ed8`
**Developer:** gamora (simulation seam). **Conductor:** gandalf (RUN-CONDUCTOR)
**Commission:** R-WR3-44(9) — Gate-2 on the acceptance landing
**Acceptance:** charter R-WR3-2 (MATT-SIGNED) · R-WR3-43 · R-WR3-44 · my prior verdict `2026-07-31-gate2-wr3-w2-encounter-ai.md`
**Principles applied:** 1 (math-before-code), 2 (smoke/full-regen gate), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity matters), 6 (cross-seam round-trip)
**Disciplines cited:** #1 (+ **new clause 1.3**), #3, #10, #11, #12, #63, #64, #65, #66, #67, **#68 (minted here)**, Pattern P8, ADR-002, ADR-004

> ## ⚑ THE RUN'S §0 TARGET-STATE IS REACHED.
> **R-WR3-2 is MEASURED, and it PASSES, on the arm of record.** `W = 1.0000` reproduces
> independently from the artifact's own per-cell data under the pre-pinned rule; the
> assumption-free floor holds at every swept corner; the arm reproduces the frozen anchor
> digit-for-digit. **Neither WARN below touches the R-WR3-2 verdict** — both land on a *carried*
> W-2 gate's attribution and on one test limb. **Wind-down may begin.**

---

## 0. Verdict summary

| Commission review point | Verdict |
|---|---|
| **1** — does the pre-registration pin the rule BEFORE the data | **PASS with an INFO, and a new #1.3 clause** — the rule is pinned and the known-in-advance figures are *disclosed*, not hidden; but the claim is structurally uncheckable at Gate-2 |
| **2** — is P-ACC-A genuinely pre-registered; are the discriminators computed correctly | **PASS** — saturation declared before the run, carried into the artifact; all four discriminators recomputed exactly |
| **3** — the arm-of-record defect + the retirement ruling | **Reversibility PROVEN byte-for-byte. Ruling: CONCUR, with one amendment** (§3.3) |
| **4** — my four WARNs + the named precondition | **ALL FIVE DISCHARGED**, three of them beyond the disposition |
| **5** — `test_H4b` vacuous-proof? `m1_armed` single-writer sound? | **Repair SOUND; `test_H4b`'s third assertion is itself vacuous** — **WARN-2** |
| **6** — sweep integrity per #65 | **PASS** — reproduced independently: sweep 1 +1/−0, sweep 2 **0/−0**, pass delta reconciles to the test |
| — | **WARN-1 (new, §2.1):** G-W2-5's PASS is correctly graded; its **attribution** is falsified by the artifact's own per-arm block |

**Discipline material: 1 number MINTED, 1 clause ADDED, 0 declined.** §5.

---

## 1. What I reproduced independently (nothing accepted on report)

Every figure below was recomputed from `output/kitcal_g5/wr3_acc/wr3_acc.json`, the `f808b46d`
git object, or the `/tmp` sweep artifacts — not read from the commit message or the math note.

| claim of record | my result |
|---|---|
| mix weights from save ABSOLUTES (882/7/3), `N=150`, `N_boss=2` | `trash 0.92 · champion 0.046667 · mixed_pack 0.02 · boss 0.013333`, **Σ = 1.0 exactly** — identical to the artifact |
| **`W = Σ w_t·H1_t = 1.0000`** on FULL **and** on flag-OFF | **reproduced**, both arms, from the per-tier `H1` and my own weights |
| saturation: `H1 = 1.0` in **all 32 cells** | **confirmed** — 32 cells enumerated, zero non-`1.0`, `n = 200` in every one. 6,400 fights |
| assumption-free floor `0.8865` at the adverse corner | `125/141 = 0.88652482…` — **exact**; it is the artifact's own `min(trash_only_bound)` over the sweep |
| `W = 1.0` at all 18 sweep corners | **confirmed** — `{1.0}` is the entire value set |
| mix-weighted intake `0.10236017566213086` | **recomputed to the last float** from the per-tier intakes × my weights |
| worst-seed boss intake `1.112183…` pools | present and consistent with `dmg_taken_mean / player_pool = 313.6046/759.0 = 0.4131813` on the mean limb |
| G-ACC-0: anchor reproduced digit-for-digit | `1.0 / 36.10666666666687 / 384.0105222222797` measured **==** banked, at the anchor's own `n=30`, with `ANCHOR_*` as module constants (`wr3_cell_acc:50-54`) and `anchor_ok` an `==` identity (`:564-566`) |
| G-W2-4 trash: `363` rolls, `0.5096` vs B11 `0.50` | `185/(185+178) = 0.5096418…`, `n ≥ 200`, `|Δ| = 0.0096 ≤ 0.10` — **PASS is correct** |
| G-W2-5: trash `2.298` · mixed_pack `10.820` · champion `0.165` · boss NOT ELIGIBLE | figures confirmed — **but see WARN-1** |
| WARN-1 restatement arithmetic `1.87–2.16×` | `0.86×43.1/17.13 = 2.164`; `0.86×50/21.33 = 2.016`; `0.86×60.8/27.90 = 1.874` — **correct** |
| `m1_armed` construction sites | **exactly one** in production (`spatial_engine.py:4034`); the rest are test constructions |
| sub-flag inertness (G-ACC-4) | 104 keys, 0 diffs, `banked_artifact_written: false` |
| G-W2-10 sink neutrality | 4 tiers × `n=10` seed-matched sinked/unsinked legs, `identical: true` on all four; `out_of_vocabulary: []` |

**The punching-bag repair is verified in the landed data, not just in the narrative.** The M1-off
arms now read boss `intake 0.622307` (vs FULL `0.413181`) — *higher* than the armed arm, which is
the mechanically correct direction. The pre-repair `0.0000` signature is gone from every cell.

---

## 2. The two WARNs

### 2.1 WARN-1 — G-W2-5's grade is right; the sentence attached to it is falsified by gamora's own artifact

The math note's §10 says of the stagger gate:

> *"predicted 2.15 s for a Common pack and declared itself a LOWER bound … Measured live: 2.298 s,
> i.e. 6.9 % above — the declared direction, at the declared magnitude. That is the model earning
> its keep."*

That reading is quoted forward into the charter at **R-WR3-44(7)** (*"trash 2.298 s · mixed_pack
10.820 s stagger"*) and into **MIGRATION §3**. The artifact emits, per arm, the data that
contradicts it — and nobody read it:

| tier | `M1` | `M1+M2` | `M1+M3` | `FULL` |
|---|---|---|---|---|
| trash | **3.008** | **2.298** | 3.008 | **2.298** |
| mixed_pack | **10.820** | 10.820 | 10.820 | 10.820 |
| champion | **0.165** | 0.165 | 0.165 | 0.165 |

Three things follow, and all three are measured, not argued:

1. **The `2.15 s` static model models the DISTRESS path** (W-2 note §2.3, `call_delay_s = 2.0`).
   The M1-only arm — proximity with **no distress call at all** — reads **3.008 s**, i.e. **+40 %**
   over the model. Arming M2, the mechanism the model is a model *of*, moves the number **DOWN**
   to 2.298. The "6.9 % above" is a comparison against the arm in which the modelled mechanism is
   *reducing* the quantity. The confirmed direction is real; the quoted magnitude selects an arm
   without saying so.
   *(Mechanism, for the record: `social_activations` 0 → 185, `bodies_never_engaged` 481 → 408.
   The call converts never-engaged bodies — which are `None` and excluded from the width — into
   bodies engaged near the minimum, which narrows the spread. That is a coherent finding and a
   more interesting one than the note claims.)*
2. **`mixed_pack 10.820 s` is not social stagger.** `M1 == M1+M2 == M1+M3 == FULL` to the last
   float; M2's contribution is **exactly 0.000**, consistent with G-W2-4's own
   `distress_calls_no_eligible_target == distress_calls_emitted` (888 = 888) on that tier. The
   10.820 s is proximity-radius spread plus player travel time. It is presently crossing the
   ADR-004 seam labelled "stagger".
3. **`champion 0.165 s FAILS`** — also identical on every M1-on arm. The honest naming of the
   failure is right; the failure is a **spawn-geometry** fact (3 of 4 bodies inside 15 m at spawn,
   as P-ACC-D itself predicted), not a distress-mechanism failure. The gap is named without its
   mechanism.

**This does not un-grade the gate.** G-W2-5's criterion was pre-registered arm-agnostically —
*per-fight `max(t_engage) − min(t_engage)`, mean `> 0.5 s` on ≥ 1 eligible tier, graded on the FULL
arm* — and 2.298 s meets it. **PASS stands.** What does not stand is the attribution sentence.

**Rationale.** This is **Discipline #64's basis-propagation clause** — the clause I ratified one
landing ago, on WARN-1 of the W-2 verdict — recurring at the next layer down: a magnitude quoted on
a basis the emitting artifact's own data does not support, which then crossed a seam. Also
**Discipline #10** (attribution clarity) and **Principle 1**. The landing already carries the
antidote: the per-arm emission required by the discipline minted below (§5) is exactly what let me
find this in ten minutes.

**Note the shape.** The M2-off arms are not seed-matched to the M1-only arm in the `_w2_rng` stream
(§5.3, declared). That disclosure explains *some* noise; it does not explain a 24 % move with a
clean mechanism and a `0.000` sibling on three other tiers. And §5.3's disclosure does not travel
with the number it qualifies — which is the same defect one level up.

### 2.2 WARN-2 — `test_H4b`'s third assertion cannot fail. The non-vacuity limb has a vacuous limb.

`tests/test_wr3_fullmix_acceptance.py:129-131`:

```python
# the mobs must also MOVE: a frozen mob is the same defect with a different symptom
assert any(m.is_activated or getattr(m, "_w2_state").m1_armed is False
           for e in m1_off for m in e.mobs)
```

The arm under test is `_fight("trash", 3, wr3_encounter_ai_v1=True, wr3_encounter_ai_m1=False)`.
Every mob on that arm is constructed with `m1_armed=self._w2_m1 = False`
(`spatial_engine.py:4034`). So `m1_armed is False` is **True for every mob by construction**, the
disjunction short-circuits, and `any(...)` is satisfied **unconditionally** — including against the
exact defective build this test exists to catch. The assertion is the one limb of `test_H4b` that
addresses the symptom named in its own comment (frozen mobs), and it is inert.

**The repair itself is sound and I am not contesting it.** The first two assertions carry the whole
load and carry it well: `_intake(m1_off) > 0.0` fails hard on the punching-bag build, and
`_intake(m1_off) > 0.25 * _intake(off)` bounds the *degree*, which is the stronger property. And
the `m1_armed` design passes the **#67** question — *does the pin bind the surface that moves?*
There is exactly one production construction site; `m1_armed` is a per-body copy of `_w2_m1` fixed
at `__init__` and never mutated; the two phase gates (`:7523`, `:8179`) and the label
(`wr3_encounter_ai.py:490`) all read that one field. Single-writer, single-source, no staleness
window.

**Rationale.** **Discipline #67** in its exact minted form — *#65 catches a test that starts
failing; #67 catches a test that keeps passing for the wrong reason.* The docstring's claim
(*"This limb asserts the fight is still a fight"*) is a **scope claim**, and one of its three limbs
does not have the scope. **Pattern P8** is the shape.

**Remediation is trivial:** strike the disjunct, or re-bind to something the defective build would
fail — e.g. positional movement, or `sum(1 for m in e.mobs if m.is_activated) > 0` on an arm where
the pre-W-2 rule is expected to latch.

---

## 3. The arm-of-record defect and the retirement ruling

### 3.1 Reversibility — PROVEN, not accepted

I reconstructed it from the git object rather than from the claim:

- `f808b46d:…/wr3_w2.json` = **6,956 bytes**, `sha256 697eb867e780be349520ff41777954457cfbaf61…`
- current file: 2 new top-level keys (`_DEFECT_arm_is_not_the_arm_of_record`, `_RELABEL_G_W2_4`);
  **0 keys removed; 0 shared-key values changed** (whole-object comparison, not spot-check)
- stripping the `_`-prefixed keys and re-serialising with the file's own writer shape
  (`json.dumps(indent=1, sort_keys=True)`, no trailing newline) yields bytes **byte-identical** to
  the `f808b46d` object

**Annotated-not-re-based: CONFIRMED at the byte level, both directions.** This is the third
correct use of the `_`-prefix annotation shape this run and it is now a reliable pattern.

### 3.2 The defect claim — confirmed, and it is real

`f808b46d:wr3_cell_w2_2026_07_31.py:69-94` passes `wr3_stage2b_v1=True` to `build_scenarios` and
its `run_spatial_fight` call does **not** carry it, nor `evade_skill_v1`, nor
`wr3_outgoing_stage_id="S2_FULL"`; `fixture_class_dict` omits `lifesteal_scope="attack_only"` and
`wr3_stage2_v1`. I checked the two flags gamora did *not* list —
`wr3_icearmor_enabled` (default `True`) and `boss_dmg_per_hit` (`BOSS_DMG_DEFAULT = 50.0`) — and
both are non-divergences. `max_hp=759.0` hardcoded is also a non-divergence: every tier's
`player_pool` is 759.0.

### 3.3 RULING on R-WR3-44(3) — **CONCUR**, with one amendment

**I concur with retiring the W-2 cell as an effect-size instrument in favour of the acceptance
cell.** The warrant is not "the acc cell is newer" — it is that the acc cell **discharges
everything the retirement costs**, which I verified item by item:

- **the retired claim is re-measured on the arm of record**, with a real 8-arm grid rather than an
  inference from counters (WARN-4's own remedy);
- **the surviving gates survive for stated reasons that hold.** G-W2-1 was graded on the *anchor*
  cell and never read the W-2 arm. G-W2-3's mechanism fact and G-W2-8's `heal_on_return_hp = 0.0`
  are **independently re-confirmed on the arm of record** in `wr3_acc.json` (boss:
  `distress_calls_emitted 554 == no_eligible_target 554`; `heal_on_return_hp 0.0`). G-W2-7's
  NOT-SAMPLED reading is re-taken on the 57 %-longer boss fight and still reads unsampled
  (`pursuit_timeouts 0`, `returns_started 0`). G-W2-2/6/9 are unit-pinned and run no battery.
- **re-firing the W-2 cell would duplicate a measurement already made correctly.** I looked for
  something the W-2 cell measured that the acc cell does not and found none.

**AMENDMENT (the one thing I would change):** the divergence is enumerated in one direction only.
The W-2 cell also **passes two flags the arm of record does not** — `emit_telegraphs=True` and
`nova_telegraph_v2=True` — and the acceptance note's own §1.1 measures them at **`36.107 → 43.807 s`
on boss duration**, i.e. **+7.7 s**, which is *larger in magnitude than the W-2 lap's entire
headline effect size* (`−1.737 s`). §0(1) and MIGRATION §1 both frame the defect as *omissions*.
The consumer-facing instruction (*"do NOT quote the W-2 cell's boss figures"*) is correct and
sufficient for a consumer who obeys it; the **reason** given is under-inclusive for a consumer who
wants to know how far off the figures are.

**Requested:** one sentence in MIGRATION §1 naming the two additions and the `+7.7 s` they carry.
No number moves. This does not gate the ruling — **the retirement stands as ruled.**

---

## 4. My four WARNs and the precondition — item by item

| item | disposition | verdict |
|---|---|---|
| **PRECONDITION (stagger instrument)** — per-body `t_engage` must exist before R-WR3-2 win rates are graded with W-2 armed | `EncounterAIState.t_engage: Optional[float]`, written at the single site that sets the latch; `None` preserved end-to-end (never-engaged bodies are kept in the vector so the denominator is visible); per-fight operationalisation *declared* because the original criterion did not specify it | **DISCHARGED — and it earned its keep immediately**: it is the instrument WARN-1 above is written from. `None`-preservation verified in the raw vectors |
| **WARN-1** — the `1.64–1.89×` magnitude rests on a factor the seam itself retired | restated **1.87–2.16×** model/model with the basis declared and the parity evidence attached; the `×0.7517` row **STRUCK**; a **#64 basis-propagation sweep table** with a per-site disposition (6 sites restated, 2 charter sites correctly declared NOT-MINE-TO-EDIT and flagged up) | **DISCHARGED, exceeds disposition** — I asked for a restatement and got the sweep the clause actually requires. Arithmetic re-verified |
| **WARN-2** — 2 of 10 gates ungraded; G-W2-5 ungradeable as built | **G-W2-5 GRADED**, with `champion FAILS at 0.165 s` reported as a failure and `boss NOT ELIGIBLE` declared rather than skipped; **G-W2-10 GRADED** on the emission limb with a byte-neutrality proof (seed-matched sinked/unsinked, 4 tiers × n=10, `identical: true`) rather than an assertion | **DISCHARGED** — no third state anywhere in the lap, exactly as commissioned. *The grade is sound; see WARN-1 on the attribution* |
| **WARN-3** — G-W2-4 labelled PASS; on its own criterion NOT MET | re-labelled **CRITERION NOT MET ON n** *in the banked artifact* via the additive annotation; re-powered to n=200 and re-graded **PASS on trash** (363 rolls); the other three declared **NOT SAMPLED ON n** with the mechanism reason attached, and the note pre-registers **before the run** that more seeds will not fix them | **DISCHARGED, exceeds disposition** — the pre-registration of the expected non-sampling is the part I did not ask for and is the better practice |
| **WARN-4** — pre-registered per-mechanism arms do not exist; two surfaces say they do | 3 sub-flags, 8 real arms, byte-inertness **proven** (104 keys / 0 diffs); **M3 measured at exactly 0.0000 on all four tiers in a real arm**; M2 shown non-independent by measurement (P-ACC-C) rather than by assertion | **DISCHARGED, exceeds disposition** — and the build of these arms is what surfaced the punching-bag defect |
| INFO-2/3/4 (docstrings) | not separately re-audited; no consumer surface | **carried, closed** |

---

## 5. Discipline material — ADR-002 direct authority (documentation-only)

**Committed to `design/working-agreement/engineering-disciplines.md`, engine repo, NOT pushed.**

### 5.1 MINTED — **Discipline #68. Ceiling statistics**

*A statistic at its ceiling is not a measurement; declare the saturation before the run and emit a
discriminator beside it.*

Four founding instances in this one landing, and the second is what pays for the number:

1. `W`/`H1` saturated across all 32 cells, pre-registered as `P-ACC-A` **before** the run and
   carried into the artifact as a `SATURATION_DECLARED` key so a JSON-only consumer gets the caveat;
2. **the defect the ceiling hid** — the M1-off arms fought inert mobs, `H1 = 1.0000` on all 32
   cells **could not have shown it**, the non-decisional intake column did, and only because the
   pre-registration required it per arm;
3. `P-ACC-B` recorded as a **NON-TEST** rather than as corroboration;
4. the **floor** case — `G-W2-4` graded NOT-SAMPLED-ON-n with a mechanism reason rather than a
   renegotiated threshold.

**Why a number and not a merge** (the #58-DECLINED test applied): **#63** governs how a zero is
*emitted*; **#66** governs a discriminator's *survival across a seam*. Neither states the
proposition, which is about the **grading instrument's dynamic range** — whether a bounded
statistic may carry a verdict at all. Nearest existing gate (#11) speaks to falsifiers of the
*hypothesis*, not of the *instrument*.

### 5.2 ADDED — **Discipline #1 clause 1.3. Precedence evidenced, not asserted** (FORWARD HABIT)

*A math note claiming "written BEFORE the measurement" lands in its own commit before the battery,
or declares its disclosure explicitly.*

**No new number**, on the #58-DECLINED precedent: this is #1's own central guarantee made
checkable, not a second proposition. **Not retroactive** — no banked lap is re-opened; the habit
binds from the next run's first pre-registered lap.

Triggering fact, stated descriptively: all three WR3 math notes landed in the same commit as their
own data (`git log --diff-filter=A` confirms), so **no Gate-2 in this run has been able to check the
discipline's central claim**; and the acceptance note's **§2.5 sits physically between §2.2 and
§2.3**, out of numerical order, inside a block §10 declares *"unedited"*. This is a
**verifiability** gap, **not an honesty one** — §1.3 of the note itself is exemplary disclosure
(*"measured before this note was finished … every armed figure is pinned blind"*) and is named in
the clause as the exemplar of the honest single-commit form.

### 5.3 DECLINED — none

---

## 6. Cross-checks that found nothing (recorded so the negative is on the record)

| checked | result |
|---|---|
| sweep integrity per #65, name-diffed by me from the raw `/tmp` files | baseline 82 · sweep 1 **83 (+1/−0**, the T8 door, declared with its warrant**)** · sweep 2 **82 (0/−0)**. Pass delta `10,005 − 9,973 = 32`; `pytest --collect-only` gives **31** in `test_wr3_fullmix_acceptance.py` (29 defs, one parametrized ×3) **+ 1** = 32. **Reconciles exactly** |
| decisions-log / locked-decision conflict (Principle 4) | none. `wr3_encounter_ai_v1` stays default OFF; `HEAL_ON_RETURN_FRACTION` untouched; D1/D2 remain Matt's and **nothing in the landing presumes either** |
| cross-seam surface (Principle 3, ADR-004) | `replica-frame/v1` unbumped; `AI_STATES` unchanged; no result-dict field, no telemetry write; 3 new keywords all default `True` under a parent defaulting `False`, byte-inertness **proven** on 104 keys |
| the mix's one real hole (`N_boss` not save-measured) | correctly quarantined — `G-ACC-3` makes it non-decisional, and the bound is monotone in `N_boss` so the adverse corner is genuinely adverse |
| modelled Veteran uplift leaking into a weight | **it does not.** Weights derive from save absolutes only; U-V1's 10× champion over-prediction is not load-bearing anywhere in the decision rule |
| `m1_armed` staleness / second-writer risk | none — one production construction site, set at `__init__`, never mutated |

### INFO (no action gated)

- **INFO-1.** `N_BOSS_SWEEP = (0, 1, 2, 3, 4, 6)` — **`5` is absent**. The note (§2.3) and the
  artifact both say *"swept 0…6"*; the sweep is 18 corners, not 21. **Non-decisional** — the bound
  is monotone decreasing in `N_boss` and the adverse corner (6) is present, so the floor is the
  true floor. Restate as the literal set, or add the value. Cite **#65**'s reflexive form.
- **INFO-2.** §0(1)'s reconstruction table labels rows 2–3 with `+`, implying an additive chain
  that row 4 (`full arm of record`) breaks — row 4 also *removes* two flags. Presentational.
- **INFO-3.** Covered in §3.3: the W-2 divergence is enumerated one-directionally.

---

## 7. Action

- [ ] **gamora (WARN-1):** restate G-W2-5's grade with its **per-arm decomposition**. Specifically:
      (a) name that `mixed_pack 10.820 s` carries **zero** M2 contribution and is proximity+travel
      spread; (b) give the `2.15 s` model comparison against the **M1-only** arm (3.008 s, +40 %)
      as well as FULL, and record that arming the modelled mechanism moves the number **down**;
      (c) name `champion 0.165 s` as a spawn-geometry outcome. The figure has crossed into
      **MIGRATION §3** and into the **charter at R-WR3-44(7)** — #64's basis-propagation clause
      requires the restatement to reach both.
- [ ] **gamora (WARN-2):** `test_wr3_fullmix_acceptance.py:130-131` — strike the vacuous disjunct or
      re-bind it to a property the defective build fails.
- [ ] **gamora (§3.3 amendment):** one sentence in MIGRATION §1 naming `emit_telegraphs` /
      `nova_telegraph_v2` as *additions* and the `+7.7 s` boss-duration delta they carry.
- [ ] **gamora (INFO-1):** `N_BOSS_SWEEP` — add `5`, or restate the note and artifact as the literal set.
- [ ] **gandalf (conductor):** R-WR3-44(3) retirement ruling — **CONCURRED**, no revision needed.
      R-WR3-44(7)'s quoted stagger figures inherit WARN-1's restatement (append-only
      forward-pointer, the shape already used at R-WR3-44(8)).
- [ ] **gandalf (conductor):** **#68 + #1.3 are in-tree at engine HEAD, uncommitted-to-remote.**
      #1.3 is a **forward habit** and binds from the next run — flag it at the next run's charter,
      not at this run's wind-down.
- [ ] **Matt:** **no decision required by this verdict.** Return surface unchanged: D1/D2, T11, the
      deferred watch, and the grill (now carrying the discriminating-statistic, hero-taxonomy,
      champion-stagger and inert-mechanism items). I re-verified that **nothing built presumes
      D1/D2**.

---

## 8. CLOSING STATEMENT — does this landing sustain the run's target-state?

**YES.**

**R-WR3-2 is measured on the arm of record and it PASSES.** The decision rule (`W > 0.500`) was
pinned before the battery; `W = 1.0000` reproduces independently from the artifact's own per-cell
data under my own recomputed weights; the verdict holds at **all 18 swept corners**; and the
assumption-free floor `w_trash·H1_trash = 0.8865` means neither of the mix's two named assumptions
can move the sign. The arm is the frozen anchor's own arm and reproduces its banked figures **to
every printed digit**, so the measurement sits on the referent-parity anchor rather than beside it.
**Matt's signed sentence is satisfied — flag-armed and flag-OFF.**

**And it passes SATURATED, which the lap said first.** That is the part I want on the record as a
*strength*. A lap that measures its owner's acceptance criterion and reports *"this PASSES, and the
PASS carries almost no information"* — **in the pre-registration, before the run** — is doing the
harder thing. The landing then proved its own point: the ceiling hid a battery fought against
punching bags, and the discriminator the pre-registration insisted on is what found it. That
sequence is why **#68** is minted rather than noted.

Neither WARN reaches the verdict. **WARN-1** lands on a *carried* W-2 gate's attribution — the
gate's own pre-registered criterion is met and its PASS stands; what needs restating is a sentence
about *why* the number is what it is. **WARN-2** lands on one inert limb of a repair whose other
two limbs carry the load. Neither is a principle violation; both are precision debts of exactly the
class this run has been policing, and both are cheap.

**The run's §0 target-state is REACHED. Wind-down may begin.** The premise error, the self-caught
punching-bag defect, the Hero-profile find and my WARN-1 are all the *same* lesson arriving from
four directions — **a saturated statistic cannot see its own failures** — and the design lap now
inherits it with the instruments already built.

---

## References

**Engine `bb453f98`:**
- `src/reincarnated/simulation/math/wr3-fullmix-acceptance-2026-07-31.md` (§§0–10)
- `src/reincarnated/simulation/wr3_cell_acc_2026_07_31.py` (`:50-54` anchor constants, `:86-87`
  sweep tuple, `:142-145` arm, `:171-177` engine half, `:283-291` weights, `:564-566` identity)
- `src/reincarnated/simulation/output/kitcal_g5/wr3_acc/wr3_acc.json` (9,402 lines)
- `src/reincarnated/simulation/output/kitcal_g5/wr3_w2/wr3_w2.json` (annotated; reversibility proven)
- `src/reincarnated/simulation/spatial_gauntlet/wr3_encounter_ai.py` (`:202-231`, `:490`)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (`:4016-4053`, `:5992`, `:6071`,
  `:7517-7523`, `:8174-8179`, `:10015-10017`)
- `tests/test_wr3_fullmix_acceptance.py` (`:105-131` **WARN-2**, `:396-430`)
- `tests/test_wr3_w2_encounter_ai.py` (`:71-92` the #67 arm-coverage guard)
- `src/reincarnated/simulation/MIGRATION.md` (new entry §§0–5; the WARN-1 restatement + sweep table)

**Sweep artifacts (`/tmp`, name-diffed independently):** `wr3_w2_sweep_final.txt` (baseline, 82) ·
`wr3_acc_sweep_final.txt` (83) · `wr3_acc_sweep_v2.txt` (82)

**Governance:**
- `agentic_orchestration/qa/findings/2026-07-31-gate2-wr3-w2-encounter-ai.md` (prior verdict)
- `agentic_orchestration/gandalf/notes/2026-07-30-wr3-kite-commit-run-charter.md` (R-WR3-43, R-WR3-44)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (**#68** + **#1.3** landed here)
