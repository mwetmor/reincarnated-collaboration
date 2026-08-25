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

*(to be appended by drax)*
