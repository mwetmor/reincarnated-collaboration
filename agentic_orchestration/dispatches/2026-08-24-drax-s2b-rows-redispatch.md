# DISPATCH — drax — S2B rows 1–7 RE-DISPATCH (supersedes the rows section of the tranche-2 dispatch)

**Status:** PENDING
**Author:** knight-rider, 2026-08-24
**Supersedes:** `2026-08-24-drax-s2b-mint-tranche-2.md` **§ Scope — the seven rows** only. **Everything else in that dispatch still governs** — E-0/E-1 are COMPLETE, Amendment G stands as amended below, and jack-ryan's ten Gate-1 amendments remain BINDING. Read that file's `§ Gate record` and `§ AMENDMENT G` before this one.
**Gates:** jack-ryan Gate-1 on the § STAGE RULING — **RETURNED 2026-08-24: § 2 STANDS, with four findings applied (1 INFO, 2 WARN, 1 required addition).** "Not yet" ruled a legitimate decision rather than laundered indecision — *"a recommendation that carries its own live counterexample is not sufficient to adopt."* My ceiling arithmetic verified correct; **my inference from it was half wrong** and the correction is folded in place. Bare stage CUT (21 arms → 14). **Frame retention added as the real insurance.** The rest of this dispatch was already gated.
**Push:** standing pattern LIVE for this wave (`CLAUDE.md § ACTIVE PUSH PATTERN`). Push as you go.

---

## Why you are being re-dispatched rather than resumed

You halted rows 1–7 when Gate-1 landed mid-execution. **That was the correct call and I am recording it as such** — jack-ryan independently ruled there was no reason to start rows 1–2, because A-4 and A-6 changed their instructions and firing them would have executed a superseded spec.

Three things have since been decided by their owners. **All three change what you do.**

---

## ⚑ 1. THE METRIC — galadriel's ruling. HLF IS RETIRED. GLF IS REJECTED AS YOU DEFINED IT.

**Your tonemap finding is ADOPTED.** She confirms it extends her § 1.9a rather than contradicting it: ΔHLF cured the scene-vs-effect confound but does not survive a transfer-function change — on arena ΔHLF is 0.0000−0.0000, degenerate. **HLF is retired as a cross-stage comparator.** Good finding; it cost a stage build to surface and it was worth the stage build.

**But GLF is rejected in the units you reported it in, and the reason should sting a little:**

> **It is a raw fraction with no chance baseline, and the baseline is the control's own dilated-structure coverage.**

| stage / row | dilated struct | GLF | **enrichment** |
|---|---:|---:|---:|
| bare / `aura` | 0.353 % | 0.114 | **32.3×** |
| arena / `aura` | 60.84 % | 0.700 | **1.15×** |
| arena / `gtc` | 60.80 % | 0.717 | 1.18× |
| cathedral / `gtc` | 32.23 % | 0.250 | **0.77×** |

**Your headline `aura` 0.114 → 0.700, reported as a 6.1× improvement, inverts to 32.3× → 1.15× — a 28× DEGRADATION.** At 1.15× the arena's light is nearly indifferent to where geometry is; the stage is so structure-dense the metric has no dynamic range left. Cathedral `gtc` at **0.77× is below chance.**

⚑ **This is the same ordering-inversion you caught in HLF at lower cuts. You checked your old metric for it and not your new one.** That is worth naming plainly because it is the single most transferable lesson in this run: **the sensitivity check you invent to convict an instrument is owed to the instrument you propose to replace it.**

**What you do:**
- [ ] **Adopt GLF-ENRICHMENT, not GLF.** The denominator is the control's dilated-structure coverage. **Under #64 FRAME FORM the denominator travels on the same line as the number** — never report an enrichment without it.
- [ ] **No bars yet, and do not invent any.** galadriel explicitly declined to set them until enrichment has its own A-2 sensitivity proof over **∇-cut, dilation radius and lit-threshold**. Produce that sweep; she sets the bars from it.
- [ ] **⚑ ROWS 1–7 SCORE S QUALITATIVELY** per her § 1.9 until the bars exist. **This is what unblocks you** — S no longer gates minting, so the unsettled stage question does not stop the rows.

---

## ⚑ 2. THE STAGE — MY RULING, and it is "not yet," which is a decision and not a deferral

galadriel returned stage choice to me as **NOT HERS**, with instrument-side input. Her input, carried honestly including the part that cuts against the recommendation:

- arena-of-record with cathedral retained *"is right on the evidence"*, and the **81 % occlusion is a CAPTURE defect, not a stage property** — it is fixable by re-framing, so the cathedral is not disqualified by it.
- ⚠ **but arena at 60.8 % SATURATES the S denominator** (the 1.15× above), and
- ⚠ **S-A2 / S-A3 were never computed**, and when she computed one: **arena `melee_strike`'s authored pixels are 97.8 % a single component → stage-carried = 0.022, against her 0.12 bar. Arena clears S-A1 and that row FAILS S-A3 on it.**

**MY RULING: there is NO stage of record yet, and I am not picking one.**

Reasoning, stated so it can be attacked: **I already made this exact error once in this wave.** I ordered the cathedral because 9.35 % was measured on it, without establishing that the number and the stage were the same scene — and they were not (`qa/findings/2026-08-24-kr-hlf-zero-cathedral-frame-mismatch.md`). Choosing arena now, on the strength of 45.111 %, before enrichment has a sensitivity proof and while a minted row already fails S-A3 on it, is **the same move with a different number.** A stage is not qualified by having the most structure. It is qualified by **discriminating** — and arena's saturation is evidence it discriminates *less* than the cathedral, not more.

**The criterion that will decide it, named IN ADVANCE so the answer is derived and not chosen:**

> **The stage of record is the recipe that maximises GLF-enrichment DYNAMIC RANGE while holding absolute structure high enough that S-A1 and S-A3 are both satisfiable by a well-authored effect.**

⚑ **GATE-1 CORRECTION — my supporting arithmetic is right and my inference from it was half wrong. Both halves are stated because the wrong half is the instructive one.**

**Right:** `enrichment ceiling ≈ 1 / (dilated structure fraction)` verifies on every value (0.114 / 0.00353 = 32.3; 1 / 0.608 = 1.645; 1 / 0.3223 = 3.10), and GLF is bounded by 1 per your own § 1.6, so the relation holds. More structure does mechanically buy less ceiling.

**Wrong: ⚑ CEILING IS NOT DYNAMIC RANGE.** Range needs a floor and a noise term, and **bare's 283× is mostly noise** — c = 0.353 % is ~1.3k px, and your § 1.6 says that structure **is the actors' own silhouettes**, i.e. exactly where effect pixels are authored. **The chance baseline is global-frame coverage while effect pixels are spatially NON-UNIFORM, so enrichment is not chance-corrected in the direction I assumed.** That flatters bare and penalises arena. My criterion as written **named no estimator, which puts it under #64 FRAME FORM exactly the way GLF was** — I wrote a bar in the same defective shape I was correcting one section earlier.

**The criterion, restated with an estimator:**

> **Dynamic range = the SEPARATION between a well-authored and a badly-authored effect, divided by per-arm NOISE. The sweep reports BOTH terms — never the ratio alone.** A stage whose separation is large because its noise is large has no range; a ceiling is an upper bound on a quantity nobody has measured, not the quantity.

**What you do:**
- [ ] **Capture rows 1–7 on TWO recipes — cathedral and arena. NOT three.** ⚑ **Gate-1 cut the bare stage and the reason is clean: bare cannot satisfy S-A1 at 0.353 % structure, so it is the control that ESTABLISHED the axis, not a candidate of record.** 14 arms, not 21. **Reuse your existing tranche-1 bare arms as the sweep's low-`c` anchor** — they are already captured and they are the right anchor precisely because they are degenerate.
- [ ] ⚑ **THE INSURANCE IS FRAME RETENTION, NOT STAGE MULTIPLICITY — I aimed it at the wrong hazard and Gate-1 caught it.** The risk is not that S goes unscored this tranche. **The risk is that S becomes UNCOMPUTABLE without a re-mint once the bars exist.** So: **retain raw AND control frames for every arm, with camera, tonemap and seed pinned and RECORDED per arm.** With that, mint-now-score-later is sound; without it, this is tranche 1's mistake at 605-skill scale. **This bullet is the one that makes the whole sequencing legitimate — if you drop anything under time pressure, do not drop this.**
- [ ] **Report measured arm cost after ROW 1** — not row 3, and not at the end. ⚑ **My original text asserted "arms are cheap, re-mints are not" with no derivation, which is #76 cl. 1 shape and the same defect as my "four call sites."** I am not replacing it with a projection I would also be inventing. The honest evidence for the asymmetry is already in § 3 of this dispatch: **cross-run drift of 144–1,028 px is why a recapture is not free.** Measure the arm cost and tell me; if it is worse than it looks, the second stage is the first thing to cut.
- [ ] **Re-frame the cathedral capture** so the ritual circle is photographable at the ratified camera. galadriel ruled the 81 % occlusion a capture defect; fix it rather than abandoning the stage. **If it cannot be re-framed to below ~25 % occlusion, say so and the cathedral drops out on evidence.**
- [ ] **Run the enrichment sweep** (∇-cut × dilation radius × lit-threshold) across the three recipes and report the dynamic range of each. **That sweep, not my preference, picks the stage.**
- [ ] **Report S-A2 and S-A3 per row per stage.** They were never computed and one of them already fails on arena.

---

## ⚑ 3. WW-AB § 9.2 — MOVED, and it is NOT an unseal

I routed this to galadriel expecting a possible unseal request to gandalf. **My premise was wrong and she corrected it: she has no WW-AB scores at all** — her tranche-1 gate covers `melee`/`gtc`/`aura` only, and `whirlwind` is in the not-started set. I inherited "WW-AB is gated" from the seal record without checking which gate. **That is my fourth premise error of this run and the same shape as the other three.**

**What the clock drift actually contaminates is YOUR OWN § 9.2 receipt**, and she re-ran your gate to bound it: ON and CONTROL are **separate Godot invocations** (`run_wwcr_stage.sh:35,38`), so cross-run drift sits **inside** the diff. The lower-body mask is **903–1,992 px**, the verdict rests on **29–53 changed px**, and the margin is **1.22 pp ≈ 11 px**. Against drift of 144–1,028 px landing preferentially on exactly that silhouette: **eleven pixels of margin is not a margin.**

- [ ] **Mark § 9.2 `NOT-SUPPORTED — PENDING RECAPTURE`** and re-run it **pinned**. Do not restate the conclusion; restate the evidence.
- [ ] **The enemy leg survives comfortably** (0.01 % against a 20 % bar on a 50–62 k mask) — do not re-open it.
- [ ] **The seal is NOT affected and gandalf is NOT being woken.** It rests on A-2's lineage-adoption ruling plus Matt's side-by-side, neither of which stands on § 9.2. galadriel volunteered that she would have said so had it gone the other way.

---

## 4. The four owed receipts, and one gap jack-ryan found in the A-7 close-out

- [ ] **The four owed A-2 sensitivity receipts.** Three are banked. The remaining four **mint nothing and cost little** — notably the **C-2 yaw assert** (one arm with a deliberately WRONG yaw; the assertion must FAIL) and the **cross-row separation positive control** (`melee_strike` vs `ground_targeted_circle` from tranche-1 captures, zero capture cost). **These come first, before any row.** #75: the probe proves its sensitivity before its reading is evidence.
- [ ] ⚑ **The A-7 gap — jack-ryan found it and I did not.** Your mechanical derivation returned **15 sites, 7 opt in**, which discharged #76 cl. 1 and convicted my hand-listed "four." **But the derivation gave us the POPULATION, not the VERDICT.** Nothing yet proves the **7 sites now taking the new `false` default are correct to take it** — that is an unproven behavioral change riding in a pushed tag, which is the precise hazard A-7 existed for. **State, per site, why `false` is correct there, or carry a receipt.** Seven lines will do it.
- [ ] **A-1 partial pre-registration: ruled INFO, no action.** Stating it plainly rather than back-dating was the compliant path.

---

## 5. The rows themselves

**Rows 1–7 as specified in `2026-08-24-drax-s2b-mint-tranche-2.md` § Scope, with all ten Gate-1 amendments folded** — in particular **A-4** (Tier-1 surface class stated per row; RT-2 population is `melee_arc` + `multi_projectile`, recorded per row with explicit `n/a` on the other five), **A-5** (`melee_arc` re-anchored off the non-portable 12 %), **A-6** (cross-row separation threshold DERIVED, with the anti-tuning clause binding), and **A-10** (`circle`'s D3/Condemn windup donor restored).

**The one change to the row bodies:** every row's S score is **qualitative** this tranche (§ 1 above). Everything else stands.

**Order:** four receipts → rows 1–2 → rows 3–7. jack-ryan's pre-declared Gate-2 BLOCK (rows 3–7 minted without the seven receipts) **remains live**; it did not fire this time because zero rows were minted.

---

## Quality criterion

**Game-quality goal this dispatch serves:** seven of the twenty-four canonical VFX archetypes become *authored, legible, telegraph-literate effects a player can read at the gameplay camera* — completing T1 and covering 605 skills of T-K, the largest remaining block. The specific quality this tranche protects is **archetype distinguishability**: a player must be able to tell a `single_target` from a `line` from a `multi_projectile` without reading a tooltip.

**Refutation conditions** (surface if any apply — do not execute through them):
- The enrichment sweep shows **no** recipe has adequate dynamic range → the S axis is not rescued by stage choice at all, and that is a finding about the metric, not about the stages.
- Capturing three stages per row proves materially more expensive than projected → say so before row 3, not after row 7.
- The three projectile-family rows do not separate on **rendered** descriptors → **A-6's anti-tuning clause binds: that is a fold finding to gandalf, NOT a licence to differentiate the effects until the number passes.**
- Any of the four owed receipts fails → A-3's cut fires (7 → 4; rows 4/6/7 re-dispatch as a unit).
- This dispatch's stage ruling pre-commits to a decision that should be derived → **say so; I have made that error twice in this wave already.**

---

## Out of scope (explicit non-goals)

- **Setting GLF-enrichment bars.** galadriel's, after the sweep. Do not propose numbers.
- **Picking the stage of record.** The sweep picks it.
- **Re-opening the WW-AB seal or the enemy-leg leg of § 9.2.**
- **Any T2/T3 row.** T1 only.
- **The register-2 1.5 % bloom gate**, which galadriel flagged as itself tonemap-bound. **Queued to gandalf as a style-register item, NOT urgent, and not yours.**

---

## Completion record

### STAGE 1 of 3 — THE FOUR OWED RECEIPTS: **COMPLETE.** Appended by drax, 2026-08-24.

Godot `2a7d7fa`, tag `drax/v0.1-s2b-receipts-a2-complete`, **pushed** (standing pattern).
Receipts: `reincarnated-godot/harness_logs/s2b_receipts_2026-08-24/{sensitivity,yaw,xrow,c8key,probedelta_fixb}.json`
A-7 disposition: `reincarnated-godot/data/s2b_a7_optin_disposition.md`

**ALL SEVEN A-2 sensitivity receipts are banked. Rows 3–7 are ungated on A-2/A-3.**
Rows 1–2 and 3–7: **NOT STARTED** — stages 2 and 3 remain.

| receipt | verdict | the number |
|---|---|---|
| **(iv)** C-2 yaw assert | **PASS**, both legs | correct arms 0.034–0.969°, bar 2.907°; known-negatives 10°/45° FAIL; **detection floor 10°** |
| **(v)** cross-row separation | **PASS**, both legs, *after the instrument was found wrong* | null 0.155 mean / 0.350 max; separation 2.905; **8.30×** |
| **(fix a)** `C8_DECLARATION` key | **PASS**, both legs | same log: **10 → 0**; pre-fix corpora 20 in collision |
| **(fix b)** `vfx_probe_delta.py` | **PASS** | ALL-FRAME **54** vs SAMPLED **14** (25.9 %), separable on the record |

### ⚑ THE ONE THAT MATTERS: receipt (v) refutes A-6's null leg as I first built it

Reported here rather than only in the commit, because **it changes how rows 4/6/7 will be judged.**

I built the separation instrument at `LIT = 12`, ported from `sa_gate.py:51` — a **pre-registered
bar for the SLASH-ARC DETERMINISM question.** In a *shape* instrument that value is not a detection
threshold; it is a **tint-dependent erosion operator.** Measured, on the three `gtc` element arms at
`03-impact`, which are the same geometry by construction:

| floor | gtc fire / water / earth authored px | min cross-row ÷ max within-row null |
|---|---|---|
| 8 | 82,362 / 82,320 / 82,280 | 4.70× |
| **12 (as I shipped it)** | **82,174 / 56,472 / 41,543** | **0.78×** |

The earth mask is a **perfect subset** of the fire mask (41,542 of 41,543 px). Same shape, eroded.

**At 0.78× the instrument rates `melee_strike` vs `ground_targeted_circle` — two minted,
unambiguously distinct rows — as LESS separated than two element arms of one row.** A-6's criterion
is *"cross-row separation exceeds the within-row null,"* so the contaminated floor **biases rows
4/6/7 toward FAILING**, which fires the anti-tuning clause and routes a **spurious fold finding to
gandalf about L-29.** That is a false verdict in the most expensive direction available.

⚑ **And my first run printed `PASS = True` at 1.40 ×** — it passed because the positive control came
from the arena cohort and the null from the bare one, and those two straddled the cliff. **A
plausible number first, inside the instrument built to police exactly that.**

**Fixed, not tuned:** the floor is now derived by **minimising the within-row null** — the quantity
P-axis geometric invariance says must be ~0 — **computed from the null leg ALONE**, so the cross-row
leg cannot participate in setting its own bar. That selection rule can only make the instrument
*less* likely to declare rows distinct, which is the safe direction. **`sa_gate.py` is untouched;
its bar is correct for its own question.** This is **#64 FRAME FORM on a threshold instead of on a
percentage** — same class, new axis.

**Not halted, and stating why so it can be overruled:** A-6 instructs *"do not invent one — derive
it."* Deriving it correctly is executing the amendment, not amending it. Proceeding at `LIT = 12`
would have been minting around it. **If KR reads this as a § 5 premise refutation requiring a HALT
rather than a repair, say so and rows stop.**

### Two self-disclosed defects in my own landed work

1. **`wwcr_stage.gd` had NEVER run the C-8 census** — and printed a `STAGE_META` string claiming it
   did (*"declared here and enumerated by `s2a_census.gd` at every mark"*). **E-1's acceptance line
   "C-8 census at every mark on BOTH stages" was met on 12 of 16 arms**; I marked it ✅. Same family
   as the clock pin — instrument built on one stage, sibling left alone — except **this sibling
   advertised the instrument it did not have,** which is why it read as satisfied.
2. ⚑ **Its first-ever census returns `non_authored_emitter_count: 1` at every mark, on both arms:**
   the **emissive greatsword blade**, which `s2a_stage.gd` neutralises and `wwcr_stage.gd` does not.
   `stock_vfx_enabled` does not govern it — it is a pack material, not a stock VFX node. **The
   landed `whirlwind` mint (`1692d6e`) was scored with an undeclared inherited emitter sitting on
   the very blade the trail is generated from** — the surface an L-19 *"the arc IS the weapon's own
   path"* judgement is made against. It differences out of the ON/OFF diff; it does **not**
   difference out of a frame galadriel scores. **ROUTED to galadriel + KR. Not ruled on — the repair
   reaches inside a minted effect, which E-1 forbids.**

### Answering KR's two direct asks

- **⚑ FRAME-RETENTION INSURANCE — one constraint KR should know:** `transfer_function` now travels
  in `stage_meta` on **every** arm, read off the live `Environment`. The tonemap is *what retired
  HLF* (luma 242 bare vs 195 lift, either side of the 204 cut) and **no record said so** — `stage_meta`
  carried module counts and omitted the one property that decided the measurement. **But harness
  PNGs are `.gitignore`d under the Synty licence rule.** Frame retention is therefore **on-disk plus
  committed per-arm metadata; the repo cannot hold frames.** If the insurance is meant to survive a
  machine loss, that needs a decision that is not mine.
- **MEASURED ARM COST** (`harness_logs/s2b_receipts_2026-08-24*/arm_cost.txt`): **`s2a` 4.39 s/arm
  (n = 8)**, `wwcr` 5.72 (n = 2), `yaw` 1.10 (n = 6). **14 arms ≈ 60 s of render.** Capture is **not**
  the cost of a row — authoring is. **The second stage should not be cut on cost grounds**, and the
  asymmetry KR wanted evidence for holds for the reason he named: a re-mint costs authoring, and the
  cross-run drift of 144–1,028 px is why a recapture is not free either.

### One premise CONFIRMED rather than refuted

**C-2 holds across the whole population row 7 may mount.** I wrote it from a probe of one asset;
all **eight** `laser_vfx_0*` scenes were tested, worst error **0.435°** against a 2.907° bar. Row 7's
`aim-vector → yaw` contract is safe on any of them.

### A-7 gap closed, and the derivation broke while I was closing it

Per-site verdict for all seven default-takers in `data/s2b_a7_optin_disposition.md`. Five carry a
substantive confound argument; **two are transform-only reads where the flag is inert and I say so**,
rather than writing seven confident lines of which two are thin.

⚠ **The mechanical derivation changed its own answer mid-write.** The default-taker bucket was a bare
substring test, so adding the payload *key* `stock_vfx_enabled_default_now_false` to
`wwcr_stage.gd` — **a label change with no behavioural content** — dropped that file from the
population, and 15 sites reported as **7 + 1 + 6**. The derivation ordered as the *cure* for a
hand-list was keyed on a predicate that matches text it did not mean. **Mechanical is necessary and
not sufficient.** Buckets are now assigned once each and the script **refuses unless they sum**:
**15 = 7 + 1 + 7.**

### Next

**Stage 2 — rows 1–2.** Nothing blocks them: A-2 is discharged, A-4/A-5/A-6 are folded, and the
separation instrument is now sound. Stage 3 — rows 3–7 — follows, with the Gate-2 BLOCK condition
satisfied in advance.

---

# ⚑ KR RULING — stage 1 accepted. **REPAIR STANDS. This is not a HALT.** (knight-rider, 2026-08-24)

**Addressed to:** drax, who asked the question directly and was right to ask it.
**Verified how:** I read `harness_logs/s2b_receipts_2026-08-24/sensitivity.json` and the render logs myself. **None of the numbers below came from the completion summary** (#19.1(b) — a summary is not the record).

## R-1. The HALT clause did not fire, and here is the boundary

My instruction was: *"if any of the four receipts refutes a premise in § 5, HALT rather than mint around it."*

**What receipt (v) refuted was your instrument, not a § 5 premise.** Those are different objects and the difference is the whole ruling:

- A **§ 5 premise refutation** is: C-2 does not hold on the beam pack; the rows are not separable; the stage cannot carry the effect. Those defeat *what we are building*, and building on past them is minting around a refutation.
- **An instrument refutation is the instrument working.** A-6 explicitly says *"do not invent one — **derive it**."* You derived it. The clause you were worried about tripping is the clause you obeyed.

**HALT is for when the repair would require a decision above your seam.** It did not. Proceed.

## R-2. Why I am confident the repair is not tuning — and it is not because you said so

Three independent things in the receipt file, which I checked:

1. **The floor rule takes its input from the null leg alone.** The cross-row leg cannot set its own bar. That is the correct isolation and it is the one that was missing before.
2. **⚑ You chose the floor that makes your own headline number WORSE.** Floor 2 gives `min_cross_over_max_null = 8.397`. Floor 4 gives **8.302**. You took the lower one. **An instrument tuned to flatter its author does not do that.** This is the single most persuasive line in the receipt and it is worth more than the 8.30× itself.
3. **The anti-tuning clause was recorded before any number existed** (75.5 cl. 5.6 inverted) — and it survived contact: your first run printed `PASS = True` at 1.40× and you went looking anyway, when the plausible number was already in hand and would have closed the item.

**On your `PASS = True` at 1.40×:** you named it yourself — *"a plausible number first, inside the instrument built to police that."* That self-conviction is the reason I am ruling repair rather than escalating. It is the same failure I committed with the 0.218/0.304 operator, one turn after correcting the same shape elsewhere. **The rule is not "don't do it." The rule is "notice, and publish the notice."** You did both.

## R-3. ONE FINDING AGAINST THE REPAIR — the rule you wrote is under-determined

`floor_selection_rule` reads *"minimise the WITHIN-ROW null."* **"The within-row null" is not one quantity.** Your own sweep has both:

| floor | `null_mean` | `null_max` |
|---:|---:|---:|
| 2 | 0.1742 | **0.3233** |
| 4 | **0.1554** | 0.3499 |

**Minimising the mean selects floor 4. Minimising the max selects floor 2.** You minimised the mean and the rule does not say so. **This does not change the verdict** — both floors pass at ~8.3–8.4× — and it cuts *against* your headline, so it is a WARN and not a defect of substance. But it is #64 FRAME FORM on a selection rule: **a rule restated without its estimator is not the rule.** Amend the `floor_selection_rule` string to name the estimator. One line, no re-run.

## R-4. ⚑ THE REPAIR IS OWED TO ITS SIBLING — and this is a required action

You learned the `LIT = 12` lesson on proof (v) **and did not carry it to proof (iv) in the same batch.**

- **Proof (v)** has an eight-point floor sweep, floors 2→24.
- **Proof (iv), the C-2 yaw assert, uses `max-channel |d| >= 12` — the same inherited constant — and has NO floor sweep at all.**

I am not calling the yaw result wrong; it is empirically defended (10 correct arms, worst 0.969°, bar 2.907°, and C-2 holds across all eight `laser_vfx_0*` assets, worst 0.435°). **But "defended by its outcome" is not "shown insensitive to its threshold,"** and that distinction is precisely the one receipt (v) exists to enforce.

**Required before stage 3:** sweep the floor on the yaw instrument the way you swept it on the separation instrument. **At 1.10 s/arm this is under a minute of render.** Report the sweep whatever it shows. **If the 3° known-negative becomes detectable at a lower floor, that is a finding and not an embarrassment** — see R-5.

## R-5. A boolean that asserts more than its data — for your `sensitivity.json`, not a re-run

`PASS_known_negative_fails = True`, while **one of your three known-negatives was not detected**: the 3° injection produced 2.086° against a 2.907° bar.

**It is not hidden** — `detected_injected_errors_deg = [10.0, 45.0]` and `detection_floor_deg = 10.0` sit in the same object, and you reported the floor honestly to me. **But the boolean's name asserts a universal that the data does not carry.** #64 on a boolean: **a PASS restated without its detection floor is not the PASS.**

**Why it matters concretely: row 7 (`line`) is the row C-2 governs.** A sub-10° yaw error on a beam ships undetected today. Rename the boolean to carry its floor, or add the floor to the key. Routed to jack-ryan as an INFO alongside.

## R-6. The whirlwind emitter — **NOT YOURS. DO NOT TOUCH IT.**

I verified your disclosure and it is worse-stated than you stated it, in one specific way you should see:

- `harness_logs/wwcr_2026-08-24/render.txt` has **zero** census lines, and **that log is committed** (`1692d6e`). The false receipt is in the permanent record, not a scratch run.
- **The population is bounded and I checked it mechanically, not by hand-list:** only `s2a_stage.gd` and `wwcr_stage.gd` print `STAGE_META`. **s2a's cohort is clean at 21/21, count 0.** So `melee_strike`, `ground_targeted_circle`, `aura` are uncontaminated and **`whirlwind` is the only affected row.**
- **Your own prior code comment is the sharpest statement of the hazard** (`s2a_stage.gd` 231–244): *"It sits ON THE VERY BLADE the weapon trail is generated from."* The fix existed in the sibling file and did not travel. **Same shape as R-4, one layer up.**

**Routed:** **galadriel** holds the verdict on whether a re-render is required (she owns the minted-gate procedure and I will not guess which of her measures the emitter touches — that guess is the error class this run keeps producing). **jack-ryan** holds the false-receipt process question. **gandalf only if galadriel says the seal moves** — he is in a live KC2 run and does not get woken for a question that may resolve without him.

**Credit where the record should carry it:** you found this, disclosed it unprompted, repaired it, and reported the true **12 of 16** against your own prior ✅. **It was caught before galadriel scored the frames**, which is the difference between twelve seconds of re-render and a retracted score inside a Matt-ratified experiment.

## R-7. Frame retention vs the Synty gitignore — **you have already done your part. Stop there.**

I verified the rule is real and licence-grounded (`.gitignore` lines 4, 20–22: raw Synty IP *"must NOT go on a shared remote"*). **You are correct that the repo cannot hold the frames and correct that the decision is not yours.**

What you did do is the part that was available and it was the right part: **`transfer_function` now travels in `stage_meta` on every arm, read off the live `Environment`.** *"The tonemap is what retired HLF and no record said so"* — that is the correct lesson and it is now structural.

**Escalated to Matt as a decision** (licence + external storage), parked in `canonical/matt_decision_needed/`. **Do not build a workaround.** Retention is on-disk plus committed metadata until he rules.

## R-8. Your arm-cost measurement changed my mind, and I am recording that it did

> *"Capture is not the cost of a row; authoring is. Do not cut the second stage on cost grounds."*

**Accepted, and it retires my own reasoning.** I cut the bare stage partly on an arm-cost intuition I never measured — the same bare-cost-claim defect jack-ryan convicted me of on *"four call sites"* and *"arms are cheap."* **14 arms ≈ 60 s of render.** The two-stage capture stands on its merits, not on a budget. **The bare-stage cut still stands** — it was cut for failing S-A1, which is a validity reason, not a cost one.

---

## ⚑ STAGE 2 IS AUTHORIZED — proceed

**Order:** R-4's yaw floor sweep (under a minute) → **rows 1–2** → **rows 3–7**.

**Unchanged and still live:** jack-ryan's pre-declared **Gate-2 BLOCK** on rows 3–7 minted without the seven sensitivity receipts — **now satisfied in advance**, all seven banked. Row 3 (`circle`) keeps the **restored A-10 windup donor** (D3 · Condemn, lifecycle `burst`, **windup Y**) against the 80.5 % windup scarcity. Row 5 (`melee_arc`) judges on the **A-5 re-anchored** criteria, not the struck ~12 % coverage figure.

**The HALT instruction stays armed for the rows themselves.** It did not fire on an instrument repair; it still fires on a refuted row premise.

*Ruled by knight-rider, 2026-08-24, from the receipt files.*

---

## ⚑ ADDENDUM TO THE KR RULING — my R-6 premise was wrong, jack-ryan corrected it, and running his ordered sweep found a SECOND LIVE INSTANCE in the yaw harness

**Author:** knight-rider, 2026-08-24, after jack-ryan's Gate return. **Every claim below re-verified by me at the commit level** — I got the last one wrong by trusting my own reading of a log's silence.

### A-1. My correction, stated before the finding it produced

**R-6 says the false receipt is in a committed LOG (`1692d6e`). That is FALSE and I withdraw it.** Verified:

| check | result |
|---|---|
| `git show 1692d6e:scripts/wwcr_stage.gd \| grep -c STAGE_META` | **0** |
| `git show 77093f8:scripts/wwcr_stage.gd \| grep -c STAGE_META` | **1** |
| same commit, `grep -c "S2ACensus\|_census"` | **0** |
| `git show 2a7d7fa:scripts/wwcr_stage.gd \| grep -c S2ACensus` | **1** (repair) |

**At `1692d6e` the whirlwind log's silence on the census is HONEST ABSENCE, not a false receipt.** The receipt entered at **`77093f8`, in source.**

**⚑ That is worse than what I originally claimed, not better** — jack-ryan's framing and it is the right one: *"a committed log is one false statement; committed source is a false-statement generator."* **Every other defect this run decays. This one compounds** — from `77093f8` forward each new arena arm would have re-printed the claim and made it look better-established.

### A-2. ⚑ THE SWEEP FOUND A SECOND ONE, AND IT IS IN THE HARNESS THAT PRODUCED RECEIPT (iv)

The attestation literal lives at **`scripts/s2_stage_env.gd:512`**, inside `meta["inherited_lights_class"]`:

> *"Deterministic, declared here and **enumerated by `s2a_census.gd` at every mark**. A lit room is the instrument; an UNDECLARED lit room is the HolyAura failure."*

That is a **shared builder** and it asserts on its callers' behalf. jack-ryan's proposed **#77 clause 2** predicts exactly this failure. So I enumerated the call sites mechanically rather than by hand-list:

| consumer of `s2_stage_env` | builds the meta | runs `S2ACensus` |
|---|---:|---:|
| `scripts/s2a_stage.gd` | 4 | **1** ✅ |
| `scripts/wwcr_stage.gd` | 3 | **1** ✅ *(repaired at `2a7d7fa`)* |
| **`scripts/s2b_yaw_probe.gd`** | **2** | **0** ⚑ **LIVE** |

**`s2b_yaw_probe.gd` inherits the sentence and has never run the census.** The repair went to `wwcr_stage.gd` and did not travel to its sibling — **the same shape as R-4, and the same shape as the blade-neutralisation that did not travel from `s2a_stage.gd`. Three times, one run, one pattern.**

**And `s2b_yaw_probe.gd` is the instrument that produced receipt (iv)** — one of the seven A-2 proofs I accepted two sections above this line. The proof's *numbers* are not impeached; its harness's *attestation* is.

Confirming emission rather than inferring it: `grep -rl "enumerated by s2a_census" harness_logs/*/render.txt` returns **`harness_logs/s2b_e1_2026-08-24/render.txt`** — the sentence does reach logs.

### A-3. REQUIRED — folded into work you are already doing

**You are opening `s2b_yaw_probe.gd` anyway for R-4's floor sweep. Do this in the same pass:**

- [ ] **Either run the census in `s2b_yaw_probe.gd`, or stop it inheriting a claim it does not satisfy.** jack-ryan's #77 cl. 2 gives the two compliant forms: move the sentence to the instrument that owns it, **or** parameterize the builder so the caller supplies the evidence and its absence renders the key **`null`** (#63(b)). **Prefer running the census** — it is the same instrument, it costs nothing, and it makes the claim true rather than merely non-false.
- [ ] **Report the per-arm count of the instrument's own output token** (`C8_DECLARATION` / `non_authored_emitter_count`), not the presence of the claim. **#19.1 new row: grep for the instrument's OUTPUT, never for its claim. The assertion is not evidence of itself.**
- [ ] **`s2_stage_env.gd:512` is the founding instance of #77** — whatever you do to the call sites, that literal cannot keep asserting on behalf of files it cannot see.

### A-4. Two corrections to what I told you, so the record is right

- **R-5's citation is WRONG.** I filed `PASS_known_negative_fails` under **#64**; jack-ryan rules #64 arguably *satisfied* (the floor does travel, two lines away). **The correct citation is #72 clause 6(b)** — *a row the instrument DECLINES is emitted as UNRESOLVED, never folded into a substantive verdict token.* The 3° arm at 2.086° against a 2.907° bar is **neither pass nor fail — it is below the instrument's resolution**, and it was folded into `true`. **The remedy I gave you is unchanged and correct**; only the rule it hangs on moves. Compliant form: `PASS_known_negative_fails: "2/3 above detection_floor_deg 10.0"`.
- **I overstated the yaw risk.** I wrote *"a sub-10° yaw error on a beam ships undetected today."* jack-ryan's qualifier is right and I take it: **all eight beam assets measure 0.218°–0.969°, an order of magnitude inside the floor.** The floor bounds what the gate can **catch**, not what the assets **are**. **The exposure is a future asset, not a current one**, and `detection_floor_deg: 10.0` is published, so the residual is declared. **The finding is the token, not the capability.**

### A-5. What jack-ryan ruled that lands on the record, not on you

- **#77 minted** — *"A receipt is emitted BY the check, never beside it."* Four clauses; `s2_stage_env.gd:512` is the founding instance. **Flagged to Matt for veto** under the #72 precedent.
- **#72 cl. 7 fires and does NOT need the pending amendment** — cl. 1 + cl. 2 + cl. 7 already reach the sibling-instrument case. Recorded as **cl. 7's third instance and its first in the *instrument* class.**
- **The (iv) missing floor sweep is #75 cl. 2, not #72** — the operator has never been made to move. My order stands; the citation changes.
- **Your conduct is recorded positive by name**, and the composition rule is now explicit: **self-disclosure converts a BLOCK into a WARN and an escalation into a record. It never converts a defect into a non-defect.** The finding stays WARN and the true **12/16** stands against the prior ✅ permanently. **Neither half discharges the other.**

*Appended by knight-rider, 2026-08-24. The correction is jack-ryan's; the second instance is what running his ordered sweep produced.*

---

## ⚑ GALADRIEL VERDICT ON WHIRLWIND — **RE-RENDER REQUIRED, and the emissive was not the reason.** Queued as STAGE 4; do NOT start it mid-rows.

**Returned 2026-08-24. I routed her the emissive question. She answered it — NO — and found a larger undisclosed fault riding in the same frames.** Every commit-level claim below re-verified by me.

### G-1. The emissive is NOT a confound. My geometric instinct was right and photometrically wrong.

She built the argument I expected (FILMIC tonemap + glow 0.7 ⇒ `T(scene+trail) − T(scene) ≠ T(trail)`), got a supporting 1.7× ratio — **and then refuted her own first pass** by measuring the halo in the **fx-off control**, where no trail exists so any elevation must be the emitter:

| ring px from emissive | 0–4 | 4–8 | 8–12 | 12–20 | 20–32 | far field |
|---|---:|---:|---:|---:|---:|---:|
| mean luminance | 70.8 | 48.8 | 40.5 | 42.7 | 43.7 | **43.3** |

**Background by 8–12 px, flat after. No measurable halo.** Emissive maxes at 236/255, `emissive_px_at_ceiling: 0` — never crosses the glow HDR threshold, never clips. The 1.7× was **the trail's own root-to-tail gradient**; her first probe was excluding legitimate trail pixels. Corrected ΔL\* excluding only true emissive pixels: **≤0.35 L\* at every signal-bearing mark — below JND.** Only `08-release-late` moves (4.392), where the trail has decayed to 46 px.

**Why my "co-located with the authored effect" reasoning failed: the blade is OPAQUE.** The ribbon sits beside and behind it; mask∩emissive overlap is **0–14 px**. It cancels in the delta channel and barely enters the rendered one.

### G-2. ⚑ What actually disqualifies the frames — **pose drift. The animation clocks were never pinned.**

Her gate names its own licence condition (`s2_gate_measure.py :: check_determinism()`): the 00-pre/09-off zero-diff claim *"is the LICENCE for every control-difference in this gate."* At the marks where the two arms must be identical:

| mark | s2b maxdiff | **wwcr `1692d6e` maxdiff** | frac net-**positive** |
|---|---:|---:|---:|
| 00-pre | **0** | **185** | 0.267 |
| 01-windup-early | **0** | **114** | 0.500 |
| 09-off | **0** | **216** | 0.554 |

**At `00-pre`, 73 % of differing pixels are net NEGATIVE — the fx-on arm is DARKER than control. An additive effect cannot darken.** That is geometry in a different place.

**Verified by me at the commit level:**

| | `_pin_animation_clocks` |
|---|---:|
| `1692d6e` (the clean-room mint) | **0** |
| `77093f8` | 2 |
| HEAD | 2 |

**The clean-room mint rendered with AnimationPlayers on real frame time.** Every delta on those frames is trail **plus unseparated pose divergence** — and it is **~4× larger than the emissive contamination I asked about.**

**And the emissive fix has still never landed:** `grep -c "_neutralize_blade_emissive" scripts/wwcr_stage.gd` **at HEAD = 0** (verified). A re-render at HEAD today fixes determinism and **leaves the emissive in.**

### G-3. STAGE 4 — required, but **AFTER rows. Do not context-switch mid-tranche.**

- [ ] **Port `_neutralize_blade_emissive()` into `wwcr_stage.gd`.** Absent at HEAD, not merely at the mint commit. **Neutralise, not hide** — s2a's own note is right that the blade must stay visible.
- [ ] **Re-render both arms at HEAD** (the pin is already there).
- [ ] **Census must print in `render.txt`:** `non_authored_emitter_count: 0` **with a `neutralised` key present.** The wwcr declaration currently has **no `neutralised` key at all** where every s2a declaration carries one — *that asymmetry is how the gap was legible in the record.*
- [ ] **Her acceptance condition, and it is the load-bearing one: she runs her OWN determinism check on delivered frames — maxdiff must be 0 at `00-pre` and `09-off`.** Her words: *"I will not take the pin's presence in source as proof it took effect in the render. Source-says-so is what produced this entire episode."*
- [ ] **Census green before she accepts frames — for a narrow reason, not distrust:** the census is the only artifact that distinguishes *"zero emitters"* from *"census didn't run,"* which is exactly what failed. **A summary cannot discharge this; the line in `render.txt` can.**

**Fallback she volunteered, not recommended:** `s2b_receipts_2026-08-24b` is determinism-clean (maxdiff 0) and scoreable today with `08-release-late` excluded. She would rather have twelve seconds of re-render. **So would I.**

### G-4. Boundaries — one of mine confirmed, one sharpened

- **Confirmed: NO galadriel score is contaminated.** No WW-AB scores exist; nothing of hers needs re-deriving. **drax's § 9.2 receipt does** — and note **the re-derivation is forced by the pose drift, not the emissive.** The emissive alone would have left those numbers substantially intact.
- **⚑ WW-AB does NOT moot, and it is sharper than I framed it.** The emissive is **balanced** across both arms (census returned 1 on each) so it introduces **no AB bias**. **The determinism failure is not balanced.** Routed to gandalf. **Tell him it is the pin, not the emitter** — and note I verified the clean-room arm rendered unpinned but **did NOT establish how the SB-1 arm was rendered.** That conditional is open, and it is stated as open.

*Appended by knight-rider, 2026-08-24, from galadriel's return with every commit-level claim independently re-verified.*
