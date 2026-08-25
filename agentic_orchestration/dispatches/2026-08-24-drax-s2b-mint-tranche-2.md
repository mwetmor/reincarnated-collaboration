# Dispatch — 2026-08-24 — drax — Step-2 VFX mint, TRANCHE 2 (the seven remaining T1 rows + the stage fix)

**Status:** PENDING — FIREABLE
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-24 (launch word covering the whole carve-out #2 agenda)
**Pattern:** B (dedicated session)
**Gates:** jack-ryan Gate-1 DESIGN-MODE — **RETURNED 2026-08-24: PASS-WITH-FINDINGS, ten amendments BINDING. Read § Gate record before Row 1.** A-1 fires before the first cathedral capture; A-2's seven sensitivity receipts gate rows 3–7; A-7 removes `stock_vfx_enabled` from this dispatch's scope.
**⚑⚑ ALSO READ `§ AMENDMENT G` (in the E-0 block, above Required reading) BEFORE YOUR FIRST CATHEDRAL CAPTURE.** galadriel verified E-0's instrument choice and returned *"right instrument, wrong number."* **9.35 % is a scene number, not an effect number; the comparable quantity is ΔHLF against a matched fx-off control, which makes E-1 the instrument rather than backfill; and S-A1/S-A2/S-A3 are the derived pass thresholds that A-1 requires you to pre-register — verbatim, WITH THE OPERATOR NAMED.** ⚑ **G-4 corrects a number I got wrong in Amendment G's own first draft: your bare-stage calibration target is `0.304 %` on the SOBEL operator, NOT the `0.218 %` that both my E-0 bullet and jack-ryan's A-2(ii) row originally carried.** A-5's `melee_arc` re-anchor and A-10's `circle` windup donor are folded into their row bodies; the struck text is left visible in both.
**Position in wave:** tranche 1 minted (3 rows) + WW-AB minted (`whirlwind`) → **galadriel's minted gate returned with 7 findings** → **you mint tranche 2** → galadriel re-gates → gandalf DRIFT-CRITIC.

---

## Context

Tranche 1 proved the loop. Three rows minted, all seven acceptance criteria met, and galadriel's gate returned a scorecard rather than a HALT — **her six HALT conditions were stated in advance and not one of them fired.** The instruments you built (`s2a_census.gd`, `gate.json`, the stage-clock pin, the four-arm control matrix) now exist and are proven, which is why this tranche is seven rows instead of three: **the marginal cost per row collapsed once the method was paid for.**

Four of the 24 T-A rows are minted (`melee_strike`, `ground_targeted_circle`, `aura`, `whirlwind`). **This dispatch takes the seven remaining T1 rows — 605 skills of T-K, the largest single block left.** After it lands, T1 is complete and only T2/T3 rows (13 rows, 202 skills) remain.

**But the gate came back with one finding that changes the stage before it changes the rows**, and it goes in first.

---

## ⚑ E-0 — THE STAGE FIX. IT GATES EVERY ROW ARM IN THIS TRANCHE.

galadriel's § 1.9, verbatim:

> **The S axis cannot be scored on the standing register-2 HLF harness unless the capture stage carries environment geometry.** The register-2 anchors (HLF 14.4 % graybox, 9.35 % cathedral) were measured on stages with walls, arches and pillars for VFX light to fall on. **The s2a stage is 99.78 % bare floor**, so HLF collapses to 0.13–0.74 % on nominal arms — a number about the *stage*, not the *effect*.

**This is the C-3 error class through a fourth door**, and you named the third one yourself (the coverage target not being camera-portable). C-3 was *a real measurement taken against the wrong stage*. So is this. Her tranche-1 S scores are all **4 with an explicit ceiling** — *"cannot reach 5 without a comparable instrument."*

**Her routing named you and me. I am making the call: the stage fix goes in BEFORE the seven rows, not after.** The reasoning is arithmetic, not preference — minting seven rows on a bare stage buys seven more rows of unscoreable S, and the re-capture cost then is seven rows instead of one stage.

### E-0 scope

- [ ] **Wire the `dark_fantasy_cathedral` recipe into the s2 capture harness as a selectable stage.** It already exists and it **is** the register-2 baseline anchor (9.35 %) — that is precisely why it is the right instrument: the S axis becomes a comparison against a number measured on the same geometry.
- [ ] **Every row in this tranche gets at minimum ONE arm staged on it**, in addition to its bare-stage arms. Bare-stage arms are **not** retired — they remain the clean measurement surface for coverage, perimeter definition and contact tests, where a busy background is a confound rather than an instrument. **You are adding a stage, not replacing one.**
- [ ] **Derive the stage's structured-content fraction the way you derived the emitter census** — do not declare it. ⚑ **CORRECTED 2026-08-24 (Amendment G-4): the number you calibrate against is `99.696 % floor / 0.304 % structured, SOBEL |∇| > 10, § 1.9a` — NOT the `99.78 % / 0.218 %` this bullet originally carried.** Both are real measurements of the same frame (`melee_ctl_03-s1-contact.png`) by two different operators — forward-difference vs Sobel. **Never average them, and never mix them.** All three stage-adequacy bars below are denominated in Sobel. Report the same two numbers for the cathedral stage, **naming the operator**, so galadriel can state what her instrument is standing on. If the cathedral stage also comes back near-bare, **that is a finding and the S axis stays non-comparable** — say so rather than shipping a stage that does not fix the thing it was built to fix.
- [ ] **C-3 uniformity check extends to the new stage.** galadriel's method: sample a ground band away from caster and effect in **every** arm; floor luminance must be consistent within a stage. Tranche 1 returned spread **0.000** across 21 arms. Two stages means **two** uniformity cohorts — do not pool them, and do not let a cathedral arm read as a divergent-albedo outlier against bare-stage arms.

### E-1 — backfill the four minted rows (cheap, and it makes the whole gate comparable)

- [ ] **Re-capture control arms only for `melee_strike`, `ground_targeted_circle`, `aura` and `whirlwind` on the cathedral stage.** **NO RE-MINT.** Nothing about those four effects changes; you are re-photographing them against an instrument that can see the S axis.
- [ ] One arm per row is sufficient. If an effect's *readability* changes materially against structured geometry — an additive effect that had near-perfect contrast by construction on a bare floor may not — **that is a finding about the R axis on the harder test**, and galadriel's own § 2.0 anticipates it: her stage *"reproduces the flattering condition."* Surface it; do not tune the effect to rescue the number.

**E-0 and E-1 are the only items in this dispatch that may proceed before the Gate-1 record below is filled in.**

---

### ⚑⚑ AMENDMENT G — POST-AUTHORING, FROM GALADRIEL, 2026-08-24. READ BEFORE YOUR FIRST CATHEDRAL CAPTURE. IT CHANGES THE NUMBER E-0 AIMS AT AND IT CHANGES WHAT E-1 IS.

I routed my E-0 instrument choice to galadriel for verification rather than assuming it. Her verdict: **"Right instrument. Wrong number — and I did name it for a weaker reason than the one you used."** Three findings, all binding, all derived (`galadriel/pipeline/stage_adequacy.py`, `galadriel/reports/s2-gate-2026-08-24/m-stage-adequacy.json`, notes § 1.9a, commit `74df5fc8`):

**G-1 — ⚑ THE 9.35 % CATHEDRAL ANCHOR IS A SCENE NUMBER, NOT AN EFFECT NUMBER. DO NOT COMPARE A MINT'S ABSOLUTE HLF TO IT.**
Decomposed: **9.343 % = 1.759 % stage + 7.584 % effect.** The cathedral clears her own 1.5 % bloom threshold **with zero hero VFX in the scene.** Her words: *"Comparing a mint's absolute HLF to 9.35 % compares an effect against an effect-plus-scene. That is C-3 through a fifth door."* My E-0 text above says the S axis *"becomes a comparison against a number measured on the same geometry."* **That sentence is wrong and is hereby struck.** Same geometry is necessary and not sufficient.

**G-2 — ⚑ THE COMPARABLE QUANTITY IS ΔHLF AGAINST A MATCHED fx-OFF CONTROL ON THE SAME STAGE. NEVER HLF.**
Consequence, and it is the one that reorders your work: **E-1 is not backfill. E-1 is the instrument.** Verbatim: *"You scoped it as 'makes the scorecard comparable.' It is more than that — the fx-off control arm is the only thing that converts HLF from a statement about a stage into a statement about an effect. Without it there is no S axis on any stage, cathedral included."* Read the § E-1 heading above as **"E-1 — the fx-off control arms, without which no S score in this tranche is a statement about an effect"** and sequence it accordingly. Every row in this tranche needs an fx-off control on every stage it is captured on, not just the four already-minted rows.

**G-3 — 9.35 % IS NOT CAMERA-PORTABLE EITHER.** It was measured 1152×648 top-down in Movie Maker; we render 1920×1080 on the ratified camera. **Same error class as the ≈ 20 % GTC finding and as A-5's `melee_arc` ≈ 12 %.** This is now the third instance. Treat any percentage lifted from a foreign camera as non-portable **by default**, and say so in the mint note rather than re-deriving the rule a fourth time.

#### The derived stage-adequacy thresholds — these REPLACE my "if it comes back near-bare, that is a finding," which had no pass condition and therefore could not fail

Her measured floor, both stages, effect-off:

| | s2a bare | cathedral (no hero VFX) |
|---|---:|---:|
| structured content — **Sobel \|∇\| > 10** (⚑ name the operator, always) | **0.304 %** | **44.570 %** |
| HLF with no VFX | **0.0018 %** | **1.759 %** |
| luma spread p25→p75 | **1.07** | **34.60** |

- **S-A1 — structured content ≥ 15 %.** One third of the measured 44.570 %. ⚑ **The one-third safety fraction is her judgment and is labelled as such; the quantity it is a fraction of is measured.** Do not report the fraction without the label (#40).
- **S-A2 — the same density must hold LOCAL TO THE EFFECT.** A global fraction is gameable: the s2a stage's structured pixels **all sit in one 59×94 px island**. Measure the density in the effect's own neighbourhood, not over the frame.
- **S-A3 — ⚑ STAGE-CARRIED LIGHT FRACTION ≥ 0.12. THIS IS THE DECIDER, AND GALADRIEL ASKED SPECIFICALLY THAT IT GO IN YOUR DISPATCH.** Of the pixels that newly cross the HLF threshold when the effect fires, what share lies **outside the emitter's own contiguous core**. **Frame (#64 FRAME FORM, carried on the same line because this is the decider):** derived on galadriel's cathedral anchor **fr01, 1152×648 top-down Movie Maker framing**, HLF-threshold crossing with connected-component decomposition — 59,656 newly-crossing px across **447 components**, largest component = **75.93 %**, so stage-carried = **0.241**. **The bar is half of that.** On a bare stage this is ≈ 0 by construction, which is exactly why it is the decider and why S-A1 alone would not have been.
  ⚑ **OPEN, and I am flagging it rather than assuming it: is S-A3 camera-portable?** It is a dimensionless *ratio*, which is what makes it look portable — but **connected-component counts are resolution-sensitive**; at 1920×1080 structure that merged into one component at 1152×648 may resolve into several, which moves the largest-component share and therefore the ratio. **I do not know the direction or magnitude of that effect and neither does this dispatch.** Report your component count alongside the ratio so galadriel can judge it at re-gate. **If your component count is wildly off 447, say so and do not silently pass or fail against 0.12** — that is a finding about the bar, not about your stage. This is exactly the trap that produced instances 2–6; the difference is that it is named in advance this time.

#### How this composes with jack-ryan's A-1 — it interlocks, it does not conflict

A-1 requires you to pre-register, before the first cathedral capture, *"the expected structured-content fraction for the cathedral stage, the margin below which E-0's refutation condition fires, and the two-cohort C-3 partition."* **S-A1 / S-A2 / S-A3 ARE those pre-registration values, and they were derived independently of your capture, which is what makes them a legitimate pre-registration rather than a post-hoc fit.** Pre-register them **verbatim, with the instrument named** — galadriel's constraint, and it is the whole point: *"a bar restated without its operator is not the bar."* Then measure.

**G-4 — ⚑ I GOT THIS WRONG IN THE FIRST DRAFT OF AMENDMENT G AND GALADRIEL CAUGHT IT. THE CORRECTION IS THE MOST IMPORTANT LINE IN THIS BLOCK.**
I originally told you A-2 item (ii) meant reproducing galadriel's **0.218 %**. **It does not. A-2(ii) is checked against 0.304 %, on the Sobel instrument (`galadriel/pipeline/stage_adequacy.py`).** Her ruling, verbatim:

> *"0.218 % and 0.304 % are two operators on the same frame, not a discrepancy. Forward-difference vs Sobel |∇| > 10, both at ∇ > 10, both on `melee_ctl_03-s1-contact.png`. Confirmed by the floors: 100 − 0.218 = 99.782 (§ 2.0's 99.78), 100 − 0.304 = 99.696 (§ 1.9a). Never average them. … Calibrating drax's derivation on the forward-difference number and then judging its cathedral output against a Sobel-derived bar is a cross-instrument comparison: **C-3 through a sixth door, inside the amendment written to close the fifth.**"*

**All three bars are denominated in Sobel** — S-A1's 15 % is one third of the *Sobel*-measured 44.570 %. § 2.0's 0.218 % is a scorecard-narrative figure with **no cathedral counterpart**, so it cannot found the instrument. Keep it only as a provenance note. **This is the fifth and sixth instance in this run of a real measurement compared against the wrong reference frame** — that error class is now the dominant defect mode of this whole tranche, and it keeps arriving *inside* the corrections written to close its previous instance. Assume it is present in anything you are about to compare.

**G-5 — the cathedral's Sobel numbers already exist, and you must NOT expect to match them.** galadriel has 44.570 % structured / 55.430 % bare at the anchor framing (fr01). That framing is 1152×648 top-down Movie Maker; **you render 1920×1080 on the ratified camera. Expecting your cathedral figure to match hers is the § 1.9a(iii) camera-portability trap** — the same trap as 9.35 %, as GTC's ≈ 20 %, as `melee_arc`'s ≈ 12 %. **Only the BARE-STAGE reproduction is the calibration.** The cathedral figure is judged against S-A1's 15 % bar, whose one-third safety fraction exists precisely to absorb the camera difference.

#### One thing that is now KR's, not yours

galadriel has been notified of the two-cohort C-3 partition (A-1 / jack-ryan's disposition item 1). **You do not carry that notification.** It is discharged, and she did better than accept it — **she ACCEPTED it and re-stated HALT-3 generally**, so it survives every future multi-stage tranche rather than being patched for this one. Her amended § 1.8 condition 3, which is what you will actually be gated against:

> *"Captures were not rendered at the ratified albedo, **or arms diverge within a (row × stage) cohort.** Albedo uniformity is evaluated per stage cohort and **never pooled across stages** — a cross-stage difference is a scene property, not a divergence. **A tranche spanning N stages returns N spreads, each reported separately.**"*

**Practical consequence for you: report two spreads, not one, and do not reconcile them.** Tranche 1's 0.000 across 21 arms was a single-cohort result and remains valid on the amended wording.

---

## Required reading before starting

1. **`agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md`** — **STATUS: SEALED. The filename says DRAFT; the STATUS line governs. This is law.**
   - **§ 1** design-law digest · **§ 1.1** L-19 owner criterion · **§ 1.2** style register · **§ 2** the P0-b constraints · **§ 3.0** column semantics **before any row**
   - **Your seven rows: § 3.1.3, § 3.1.4, § 3.1.5, § 3.1.6, § 3.1.7, § 3.1.9, § 3.1.10**
   - **§ 6.1** revisit triggers · **§ 7** what the spec does NOT decide (do not read silence as permission)
2. **`agentic_orchestration/galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`** — **the gate you are building toward, and it now carries three standing instrument corrections that bind you:**
   - **§ 1.2** — the L-19 test made a number: expansion / ground-mark persistence / **body-illumination fraction with a step change at contact**. `magical-cause` rows invert test (3) as an **anti-tamper check** — a magical field that spikes at contact has had physical tells smuggled in. **`self_buff` is `magical-cause` and this applies to it directly.**
   - **§ 1.3** — ⚑ **hue-angle separation must NOT be used to adjudicate RT-2.** Hue is undefined at zero chroma and unstable near it. **Use CIEDE2000 in CIE L\*a\*b\* on rendered pixels, and report added light alongside.** Applied to tranche 1 this **moved which pair is the minimum.** Your `neutral`/`wind` 3.0° finding was measured on the superseded instrument — re-measure it on this one before you carry it forward.
   - **§ 1.3 fork test** — whether an RT-2 collapse indicts the *surface class* or the *palette* is decided by **ΔE(rendered) vs ΔE(added), pairwise.** Systematic compression ⇒ surface. Rendered ≈ added ⇒ faithful transmitter, palette indicted. This replaces "these are two pastels I authored," which is an argument from intent a gate cannot verify.
   - **§ 1.5** — C-3 verified rather than declared, and its **honest limit**: uniformity is what pixels can attest; the absolute 0.085 rests on your `render.txt` declaration.
   - **§ 1.9** — the stage-adequacy rule (E-0 above).
3. **`agentic_orchestration/drax/notes/2026-08-24-s2a-mint-note.md`** — **your own tranche-1 note, re-read as INPUT rather than as findings.** Especially § 0 (WARN/INFO), § 9.6 (routed findings) and the method half.
4. `agentic_orchestration/drax/notes/2026-08-24-rt5-beam-vfx-preflight.md` — **RT-5 returned `LOADS`.** 18/19 pack scenes load and instantiate clean; the one failure is the vendor showcase scene, which no T-A row consumes. **`line` (§ 3.1.10) is CLEAR to schedule.** The C-7 mechanism was measured and is not the one that is live — but **do not rebuild the UID cache**, which is the operation C-7 actually warns against.
5. `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` — **L-19** (owner criterion), **L-29** (the folds — **(4) `beam_channel` ↔ `line` DISTINCT, load-bearing for § 3.1.10; (8) the `self_buff` sub-flag**), **L-39** (key-grain audit), **L-41** (the `aura` anchor param, as precedent for how a grain question resolves).
6. `canonical/reap-die-rise-story/style-register.md` — register A, bounded stylized-low-poly-3D (Synty) through a fixed 2.5D ARPG camera.

### ⚠ Quarantine status

The **WW-AB clean-room protocol is discharged** — you have minted `whirlwind`, so the experiment it protected is complete. **However, lifting the quarantine on L-36 / L-37 / sealed spec § 5 / the carve-out request is gandalf's call, not mine, and he has not made it.** Practically this costs you nothing: **not one of the seven rows in this tranche consumes any of those four documents.** If you find yourself reaching for § 5 — which is *Matt's deserving list*, and where `self_buff`'s `transformation` sub-shape and `totem`'s delegate body both live — **HALT to knight-rider.** Both of those are explicitly out of scope below, so reaching for § 5 is itself the signal that scope has drifted.

---

## The P0-b constraints — which bind, which do not

- **C-1 — disable shadow casting on additive/emissive VFX meshes at mount time.** Binds **every** row.
- **C-2 — beam `−Z` orientation.** ⚑ **BINDS `line` (§ 3.1.10)** — the row states the orientation contract explicitly: **aim-vector → yaw, explicit.** This is the first tranche where C-2 is live.
- **C-3 — additive stacking blows to white over a light floor; 0.085 reads correctly.** Binds every row, and now across **two** stages (E-0).
- **C-4 — lifecycle class is a real authoring axis** (spread > 5×). ⚑ **Load-bearing on `line`:** its class is **`travelling burst`, explicitly NOT `sustained`** — that is the axis L-29(4) uses to separate it from `beam_channel`, and **two lifecycle classes cannot share one VFX selection.** Build the travelling burst; do not let the beam pack's sustained grammar leak in because the assets came from a beam pack.
- **C-5 — readability floor AND ceiling** (**0.03 % → 67 % peak screen coverage; frame: YOUR OWN § 7.5 corpus measurement at OUR locked camera** — `p_trail` 535 px at the floor, `b_expl` 46 %, `x_attr` 67 % at the ceiling). Binds every row. ⚑ **Frame named per #64 FRAME FORM even though you are the measurer** — I swept this band as a candidate instance of the wrong-reference-frame class and it came back **clean**, precisely because it is ours and not lifted. Stating that is cheaper than someone re-deriving the check later.
- **C-7 — beam-pack `uid://` fragility.** **Measured and non-blocking (RT-5), with one standing prohibition: do not trigger a UID-cache rebuild.**
- **C-6** (zero attractor content) binds `vortex_pull` — not in this tranche.

### ⚑ C-8 — carry it forward, derived, on both stages

`s2a_census.gd` exists and it earned its keep: it found a third emitter nobody had enumerated (the Greatsword's emissive material, **on the very blade the trail is generated from**). galadriel accepted the tranche-1 declaration **specifically because it was derived by ancestry rather than hand-listed** (Discipline #76).

- [ ] **Run the census at every capture mark, on both stages.** The cathedral stage is new geometry and **new geometry is exactly where an un-enumerated emitter enters** — a torch, a brazier, a glowing rune on a wall. If the cathedral recipe ships emissive set-dressing, **that is not automatically a defect** (a lit environment is the point), but it **must be declared and classed** — INHERITED-BY-DESIGN is a legitimate class; INHERITED-AND-UNNOTICED is not.
- [ ] ~~**`KingRig.stock_vfx_enabled` — flip the default to `false`, and make the throne-room / presentation scenes opt in explicitly** … *an opt-in at four call sites is cheaper than a confound in every capture forever* … *if the opt-in surface turns out to be materially larger than a handful of scenes, stop and tell me*.~~
  ⚑ **STRUCK BY GATE-1 A-7. DO NOT DO THIS IN THIS TRANCHE.** Two reasons, and the second one is mine to own:
  **(a) It is not load-bearing here.** Tranche 1 already returned `non_authored_emitter_count: 0` on **21/21 arms with the default still `true`** — the declarative export already controls the confound. The flip is hygiene, and it would ship **untested** inside a tag whose gate measures mint quality: one tag, two unrelated changes, one receipt (#10 at the dispatch layer).
  **(b) ⚠ My struck text was a bare hand-list with an undecidable escape hatch** — *"four call sites" / "a handful of scenes" / "materially larger than a handful"* is a threshold with no derivation, so my own stop-and-tell-me condition could never have been evaluated. **#76 clause 1**, applied by jack-ryan to a dispatch I authored, on a rule whose founding instances are two documents he authored. **The fix is the rule: derive the opt-in call-site set mechanically, report the set, then flip — in its own change, with its own receipt.** The derivation is also what makes the escape hatch decidable for the first time.
  **The decision itself stands and is still yours** (seam authority, ADR-002). It moves out of this tag, not off the board.

---

## Math-before-code (Discipline #1)

Mint note at `agentic_orchestration/drax/notes/2026-08-24-s2b-mint-note.md`, **committed before the first effect node exists** — the tranche-1 ordering (`40d22e99` §§ 0–8 before any mint, § 9 RESULTS after) is the receipt shape and it is what DRIFT-CRITIC audits against.

Per row, state:

1. **The layer decomposition** T-A names, mapped to concrete Godot nodes/materials.
2. **What takes the tint and what must NOT** — from the row's Tier-1 surface-class clause, translated into the property you will vary. **The "must NOT" clauses are acceptance criteria, not advice.**
3. **The lifecycle class and how you realize it.**
4. **Stage-albedo value per stage** (C-3, now two cohorts).
5. **The element-variant set** sufficient to demonstrate Tier-1 without becoming a content lap.
6. **NEW — the pre-flight self-check you will run for each of the three tranche-1 method defects** (see below). Name the check and its expected refuting output, not just its name.

---

## ⚑ The three method defects from tranche 1 are now STANDING PRE-FLIGHT CHECKS

You found all three and each of them **produced a plausible number first**. That is the whole hazard: none of them announced itself. Seven rows is seven more chances for each.

1. **"Inspect the artifact that ships, not the one you authored."** The weapon trail never rendered — `MeshInstance3D.mesh` was never assigned, and every probe interrogated the mesh being *built* rather than the instance that *draws*. Mesh AABB valid, instance AABB `(0,0,0)`.
   → **Pre-flight per row: assert the DRAWN instance's AABB is non-degenerate before you measure anything about the effect.**
2. **"A control must control everything that moves."** Effects on a fixed 1/60 s clock, rig and mob `AnimationPlayer`s on real frame time — the ON/OFF diff reported 404–573 "trail pixels" that were **entirely animation phase**, and you nearly read it as readability evidence.
   → **Pre-flight per row: `00-pre` / `08-post` must diff to exactly 0 with the effect disabled.** Tranche 1's receipt was 0 on all five melee arms. **Reproduce that receipt per row, on both stages** — the cathedral stage may carry animated set-dressing (flickering torches, banners) that reintroduces this defect through the new geometry.
3. **Controls on one side only.** The read-through ratio came back **6.383** (the trail apparently *more* visible inside a field) and rebuilt as a proper four-arm matrix it was **0.998**.
   → **Pre-flight per row: every ratio has a matched control on BOTH sides.**
   *(And the fourth instance: the GTC payload rendered sub-pixel, caught only because `erupt` and `descend` returned **byte-identical** coverage — which two variants differing only in payload direction cannot. **A suspiciously identical number is evidence, and so is a suspiciously good one.**)*

**Plus the one that arrives from inside the effect:** an intermediate melee tune was highly readable **and had lost its element tint** — additive blown to cream. C-3 from inside rather than off the floor, and more dangerous because **nothing in the frame complains.** Check `tinted_count` and measured chroma on every arm, not just the ones you suspect.

### ⚑ ADDED 2026-08-24 AFTER AUTHORING — two instrument findings from jack-ryan's Gate-2, both of which land inside this tranche

Gate-2 returned **PASS-WITH-FINDINGS on both tranche-1 tags** (2 WARN · 4 INFO · 1 ESCALATE · **0 BLOCK**) — `agentic_orchestration/qa/findings/2026-08-24-step2-first-landings.md`. Two findings are instrument defects that would ride into this tranche unchanged, so they are scope here:

**(a) WARN-1 — the `C8_DECLARATION` key does not carry the axes the run varies.** The payload omits `fx` and `rt`, so **8 of 21 tranche-1 declarations collapse onto 2 keys.** It is **latent, not active** — log position disambiguates them *today* — and it **stops** disambiguating them the moment a declaration is lifted into a per-arm record, which is exactly what a two-stage tranche does. **Add `fx` and `rt` to the declaration key before the first capture.** *(Note the shape: this is a derived instrument whose derivation is correct and whose **identity key** is under-specified — the census walks by ancestry, faultlessly, and then files the result under a name that cannot tell two arms apart.)*

**(b) `scripts/vfx_probe_delta.py` reports two different coverages under names that describe neither, and the artifact invites the wrong inference.** `byte_identical` is computed from `sha_set()` over **every frame**; `samples` comes from `idxs`, **at most 14 entries**; and `frames_a` / `frames_b` describes neither of them. **No field names either comparison's coverage.** Routed to you rather than fixed by jack-ryan because it is your instrument.
→ **Fix it before this tranche's first measurement, and fix it in the direction § 75.5 clause 5.4 now requires: every identity claim carries its own coverage on the same record.** A sampled claim must not be able to borrow an all-frame claim's authority by sitting next to it in the same JSON object.

**Both of these are the tranche-1 lesson at one remove.** Your three method defects were *measurements that produced a plausible number first*. These two are *records that produce a plausible reading first* — the number is right and the label lets a reader take more from it than it can support. Same family, one layer out, and this tranche is where they would first cause a false verdict rather than a latent one.

### ⚑ HALT-AND-SURFACE after the first two rows

If any **new** instrument defect of the tranche-1 class appears in rows 1–2 — a measurement that produced a plausible number before it produced a correct one — **stop, surface it to knight-rider, and do not carry the remaining five rows on an instrument you have just found to be wrong.** Seven rows minted on a defective instrument is seven rows to re-mint. This is a cheap circuit-breaker and I would rather pay it than not.

---

## Scope — the seven rows

### Row 1 — `self_buff` (§ 3.1.3) — 112 skills / 102 kits · `magical-cause`

- [ ] Mint the **`buff-decal` sub-shape ONLY**: two swappable layers — **(a) a floor decal under the caster, (b) local body-adjacent emitters.** Both sit on our two cheapest register levers.
- [ ] **⚠ The `transformation` sub-shape is OUT OF SCOPE — by ruling, not by omission.** L-29(8) carries both sub-shapes under one archetype **deliberately unsplit**, and the spec names this *"the one genuine SPLIT question found in the whole run, deliberately NOT executed here."* A transformation **replaces** the silhouette; a decal buff **must not touch it** — opposite requirements on the same property, which one canonical cannot serve. It is on **Matt's deserving list (§ 5, Class-A item 2)**, a commitment boundary rather than a reasoning boundary. **If you find yourself authoring a silhouette replacement, stop.** *(Same shape as `aura`'s L-41 narrowing at tranche 1 — mint the default case, hold the rest.)*
- [ ] **THE GOVERNING PROPERTY: does not obscure the character.** These 112 skills will frequently be **active during other skills** — every other archetype's VFX must remain readable **through** this one. **Tint the decal and the local emitters; cap opacity and radius; never let a Tier-1 recolour raise coverage.**
- [ ] ⚑ **This row demands a read-through measurement, and you already built the instrument for it** — the four-arm matrix that produced **0.998** on `aura`. **Run it here with a different second effect on top** (a `melee_strike` or `ground_targeted_circle` arm from tranche 1 is already minted and available). A retention ratio meaningfully below 1.0 means this row is eating the readability of the archetypes it co-occurs with, and **112 skills makes that the most consequential occlusion risk in T-A.**
- [ ] **`magical-cause` is CORRECT here.** Do not "fix" it into a physical read. And per galadriel § 1.2, **the contact test is INVERTED as an anti-tamper check** — this effect **should NOT** spike at contact. Do not add a contact response to flatter the L-19 score; that corrupts a row the rubric calibrates on.
- [ ] Lifecycle `sustained`. Windup gap (`windup = N` on 3 of 4) is a **coherent** `motion_signature_attested = NULL` property, not under-research — do not invent a windup to fill it.

### Row 2 — `totem` (§ 3.1.4) — 97 skills / 80 kits · `two-layered`

- [ ] Mint the **three-phase separation: summon / delegate-active / impact.** **That separation IS the authoring structure** — collapsing it loses the archetype.
- [ ] **L-19 is `two-layered`: `magical-cause` (the manifestation) + `physical-cause` (the delegate's slam). BOTH must be authored.** This is the only row in T-A with a split causality class, and galadriel's § 1.2 test has to be applied per-layer: the slam **must** show the contact step change; the manifestation must not.
- [ ] **The anticipation beat is the row's selected property and its hardest one.** Ancestral Warchief was chosen because it is the **only** candidate with an explicit anticipation beat **on the delegate itself** (raised arm before the slam) — *"the player must read that the totem is about to act."* **No other candidate teaches it.** If your delegate acts without a readable windup, the row has failed its selected property even if every other measurement passes.
- [ ] **⚠ PARAMETERIZATION CEILING — stated in the spec (L-30) so it is not discovered as a defect: a summon-delegate needs a MODEL. Tier-1 can recolour what the totem THROWS; it cannot recolour what the totem IS. `P = 4` is that ceiling, not a mark-down.** 97 skills sit behind it and it is a **model-pipeline** dependency, not a VFX one. **Do not attempt to solve it.** The delegate body routes to § 5 Class-A item 3 as a **conditional** Tier-2 candidate — conditional because a body is not a flourish and the cost sits in a different pipeline.
- [ ] **Use a placeholder delegate body and declare it as a scaffold (Discipline #40).** A scaffold that ships undeclared is the failure mode; a scaffold that ships declared is the correct answer to a model-pipeline dependency you are not authorized to open.
- [ ] Tier-1 is `PAYLOAD-CARRIED` **on the delegate's ATTACK only.**
- [ ] Lifecycle: `sustained` (delegate presence) **with `burst` sub-events** — composite by construction, same class as `ground_targeted_circle`'s composite, so the residue-coexistence capture pattern transfers.

### Row 3 — `circle` ⊕ `ring` (§ 3.1.5) — 93 skills / 88 kits · `physical-cause`

- [ ] Mint: caster-centred, ground-plane · layers — **(a) a distributed set of solid blade meshes erupting on a literal circumference, (b) hit reactions on adjacent bodies.**
- [ ] **`physical-cause` was DECISIVE here** — Ring of Steel is the **only action-CAUSED reference in either the `circle` or the `ring` pool**. Real blades erupt on a circumference **with hit reactions on the bodies they reach.** Under L-19 that outweighed a subdued palette, and the palette is scored against **our** register, where a ring of simple blade meshes lifted by light is **register-1 geometry reaching register-2** — exactly the A-holds measurement.
- [ ] **RT-8 precedent applies: mint the `annulus` `tier1_layer_flag`.** Under it, layer (a) becomes **a travelling front with an OPEN interior** that preserves character visibility (D2R Poison Nova grammar). **This is a Tier-1 layer TOGGLE, not a second effect** — if it cannot share the base emitter cleanly, **that is a FINDING for the next lap, surfaced, not a silent fork.** (`erupt`/`descend` shared its emitter byte-identically at tranche 1; use the same `perimeter_hash`-class receipt.)
- [ ] **Tier-1: motif-swap the erupting element** (blades → shards → flame tongues → bolts); **tint the front and the contact response.**
- [ ] ⚑ **THE CLEAREST STATEMENT IN THE RUN OF WHAT NOT TO BUILD is attached to this row.** The 8 frames captured under a `circle` hypothesis resolved by icon template-match (L-28) to **War Cry**, not Judgment, and are **EXCLUDED from the pool** — but retained as a **finding**: *a player-centred expanding annulus with a propagating front, a ground residue, and **no contact response on the bodies it overtakes*** — **a second independent instance of the EoR L-19 failure mode, in a different skill, in the same game.** Your `annulus` variant is **structurally the same object as that failure**. The single property separating them is **the contact response on overtaken bodies.** Build it, measure it, and put the measurement in `gate.json`.
- [ ] **Frame-set pointer: NONE.** There is no first-party GD frameset for this archetype. That is a **provenance fact, not a silent gap** — do not read the absence as permission to substitute the excluded War Cry frames.
- [ ] ⚑ **RESTORED PER GATE-1 A-10 — THE WINDUP DONOR. I dropped it when authoring; it is the second separator on this row after the contact response.** Spec § 3.1.5 carries **D3 · Condemn** as *"the corpus's best windup donor for the radial-burst family,"* named explicitly against the run-wide **80.5 % windup scarcity**. **`circle` is the only row in this tranche with a named windup donor**, its lifecycle is `burst` with windup **Y**, and this dispatch's stated quality criterion is telegraph literacy. For a caster-centred expanding annulus that is *structurally the same object* as the EoR failure, **the windup is what tells a player the ring is coming before it overtakes them** — the contact response tells them it landed. **Both, or the row only half-answers the failure it was built against.** Report lead time and pre-`t_burst` emitter activity, in the shape GTC set (*telegraph full at 0.183 s with payload 5.5 m out*).
- [ ] Lifecycle `burst`, **windup Y**.

### Row 4 — `single_target` (§ 3.1.6) — 90 skills / 77 kits

- [ ] Mint: projectile · **three visibly separated layers — (a) payload body, (b) trail, (c) impact residue on the target.**
- [ ] **This row has the cleanest Tier-1 evidence pair in T-A: two references supplying BOTH causality classes on identical delivery geometry.** Canonical Essence Drain is `magical-cause`; runner-up LE Javelin is `physical-cause` **with contact WITNESSED** (t ≈ 5.60 s, white burst on an enemy body, red streak leading in). **Cite the runner-up for physical-element parameterizations.**
- [ ] **Tier-1: tint all three layers; motif-swap the payload body** (orb → spear → shard → bolt).
- [ ] ⚑ **THE LOAD-BEARING BOUNDARY — and it constrains a dimension, not a colour.** Essence Drain's trail is **narrow enough that it does not read as a beam.** Javelin's flight streak spans **≈ 40 % of the crop width and reads as an elongated luminous LINE.** Under L-29(4), protecting the `single_target` / `line` boundary is load-bearing for archetype identity — **Essence Drain PROTECTS it; Javelin SOFTENS it.** **Measure your trail's aspect ratio and put it in `gate.json`.** You are minting `line` in this same tranche (Row 7); **the two rows must be distinguishable at the gameplay camera, and you are the only person who will ever see them side by side before a player does.** A cross-row separation measurement between Rows 4 and 7 is the single highest-value thing this tranche can produce that no single-row dispatch could.
- [ ] ⚠ **`reference_window` has a `t_end` for a reason.** Measured **t ≈ 0.40 – 0.90 s**. **Later segments of the Javelin clip show denser multi-projectile multi-hit behaviour that MUST NOT be read as base `single_target` grammar** — and you are minting `multi_projectile` in this tranche too, so the contamination risk is live in both directions.
- [ ] **Javelin's honest limits, carried forward:** the dark spear against dark terrain at t = 0.53 / 0.73 is **genuinely low-contrast** and identity is carried almost entirely by the wake — **a real risk in our dark-mood register**, and E-0's cathedral stage is where that risk becomes visible. The clip is **1280×500, horizontally letterboxed — vertical framing and vertical coverage CANNOT be assessed from it.** It is a geometry and phase-separation master, **not a camera-framing reference.**
- [ ] Lifecycle `burst` (travel + impact).

### Row 5 — `melee_arc` (§ 3.1.7) — 76 skills / 63 kits · `physical-cause`

- [ ] Mint: caster-origin, frontal, ground-plane · layers — **(a) a broad TRANSLUCENT pale crescent on the ground plane (radius ≈ 2× character height), (b) contact response on bodies inside it.**
- [ ] ⚑ **RE-ANCHORED PER GATE-1 A-5 — the original text handed you `Reference coverage ≈ 12 % — mid-band against C-5`. THAT IS STRUCK.** It is a percentage lifted from a foreign camera, which is the exact bar galadriel's § 1.6 ruled **NON-PORTABLE** (*"never against a spec percentage lifted from another camera"*) — the same door the ≈ 20 % GTC finding closed at tranche 1 and the same door Amendment G-3 closed on 9.35 %. **Third instance; do not open it a fourth time.** The two portable properties replace it: **(a) angular extent < 360° and radial thickness / outer radius** — that ratio is what makes a crescent not a field, and it is camera-invariant; **(b) background-structure retention through the arc** and **caster-pixel retention at the arc's origin**, both measured as retention fractions rather than absolute coverage. Put all three numbers in `gate.json`.
- [ ] **Caster legible at the arc's origin and NOT occluded; terrain visible THROUGH the arc.** That is the **explicit correction of EoR failure #2** and it is an acceptance criterion. ⚑ **Interlock, and it is an independent argument for E-0 going first: on a 99.78 %-bare floor, "terrain visible THROUGH the arc" is UNTESTABLE, because there is no terrain. The cathedral stage is what makes this row's core prohibition measurable at all.** Capture this row's retention arm on the cathedral stage or the criterion is unfalsifiable.
- [ ] **`physical-cause`, the purest read available: the arc IS the weapon's own path, not an energy wave chasing it.** This is the same failure mode `melee_strike` was built against — you have already solved it once on a TRAIL-BOUNDED surface, and the crescent is the harder case because a ground-plane crescent looks like a field until it is proven otherwise by its contact response.
- [ ] **Tier-1: blade-motif swap (scythe → axe → claw → greatsword) — the cheapest high-yield parameterization in T-A.** Tint the crescent and the contact spark. **DO NOT thicken the crescent into a field** — **79 % of this archetype's referent members are element-agnostic** (§ 4.2.3), which is the same argument that capped `melee_strike`'s tint at 70 %.
- [ ] Lifecycle `burst` — **short-lived, so it never occludes.** That is a design property, not an incidental one.
- [ ] **Cadence donor is Hades II — ⚠ use it for BEATS ONLY. It is hand-drawn 2D top-down: the beat structure transfers, the surface does not. Do not let it set a 3D style target.**
- [ ] ⚠ **Honest limit on the extraction master: the scythe blade itself is NOT in the frame** — the sweep has passed and only the trail remains. The L-19 claim is **confirmed-CONSISTENT, not proven.** You are the first person who can actually prove it, because you control the motion: **capture the sweep with the blade in frame and the crescent co-located with its path.** That is a genuine evidence upgrade this row has never had.

### Row 6 — `multi_projectile` (§ 3.1.9) — 68 skills / 63 kits · `physical-cause`

- [ ] Mint: projectile fan from a caster origin · layers — **(a) per-projectile body, (b) per-projectile trail, (c) per-impact response.**
- [ ] **Tier-1 is `TRAIL-BOUNDED` (projectile bodies + trails). ⚠ COUNT / SPACING / RANGE ARE ENGINE PARAMETERS, NOT TIER-1 ELEMENT PARAMETERS — do not conflate them.** *A fire multishot and a water multishot differ in tint and motif, not in fan geometry.* Demonstrating Tier-1 by varying the fan is demonstrating the wrong axis, and it would be the `single_target`-boundary error in a second location.
- [ ] The reference makes the three parameter axes **visually explicit** — that is § 3.3's requirement rendered as a picture. **Build the fan parameterizable and declare the three axes as ENGINE-driven** (a contract note, not a contract change — see the Principle-6 gate below).
- [ ] **Cross-row check against Row 4:** a `multi_projectile` arm with count = 1 must be distinguishable from `single_target`, or the fold boundary is carried by count alone. Measure it.
- [ ] Lifecycle `burst`.

### Row 7 — `line` (§ 3.1.10) — 51 skills / 48 kits · `physical-cause` · **RT-5 CLEAR**

- [ ] Mint: travelling linear payload · layers — **(a) the travelling body, (b) a pierce-persistent trail, (c) per-target contact response.**
- [ ] ⚑ **C-2 IS LIVE FOR THE FIRST TIME: the orientation contract is explicit — aim-vector → yaw.** You wrote C-2 from your own probe (beam assets orient `−Z`). **Assert the realized yaw against the aim vector in `gate.json`** — an orientation defect that ships is invisible in a single forward-facing capture and catastrophic at any other angle. **Capture at ≥ 3 distinct aim vectors.**
- [ ] ⚑ **Lifecycle is `travelling burst` — EXPLICITLY NOT `sustained`.** This is the axis L-29(4) separates `line` from `beam_channel` on; C-4 measured the class spread at **> 5×** and **two different lifecycle classes cannot share one VFX selection.** The assets come from a beam pack whose native grammar is sustained — **do not let the pack's grammar decide the row's lifecycle.**
- [ ] **`pierce` is the discriminator protecting the `single_target` boundary** — *a payload that continues through a target reads as a line; one that terminates reads as a projectile.* **Author the pierce-persistent trail and measure persistence past first contact.** With Row 4 in the same tranche, prove the pair separates.
- [ ] **Tier-1: `PAYLOAD-CARRIED`.** Tint body + trail + contact; **motif-swap the body** (bone spear → ice lance → lightning javelin).
- [ ] **Confound register: none named — and here that is a positive, not a neutral.** *Pale spear against dark floors is the highest-contrast read in the archetype, and our register is dark-mood.* E-0's cathedral stage is where you verify that claim survives structured geometry.
- [ ] **Do not trigger a UID-cache rebuild** (C-7's actual hazard; RT-5 verified the cache byte-identical before/after its probe and you should hold that property).

---

## ⚑ The confound-register finding from tranche 1 propagates into this tranche

Your WARN #1 established something with teeth beyond the row it was found on:

> **A tier upgrade can DOWNGRADE a row's confound register.** `DOSSIER-TEXT` rows carry *"no confound named"* for the trivial reason that **nobody looked**, and other rows rest their empty registers on the same silence.

Four rows in this tranche carry **`Confound register: none named`** or near-silence (`circle`, `line`, and `multi_projectile`'s single named item; `single_target`'s register is unusually thorough by contrast).

- [ ] **For any row where you cut or inspect an extraction master, RE-AUDIT the confound register and report the delta in BOTH directions** (Discipline #76 clause 2). A register that gains an entry after inspection is the expected outcome, not a defect — **and a register that stays empty after actual inspection is worth strictly more than one that stayed empty because nobody opened the file.**
- [ ] **Do NOT patch the sealed spec.** You were right at tranche 1: you do not rewrite a sealed document. **Route to gandalf via the mint note, as you did.**
- [ ] **Name which side of galadriel's comparison each confound lands on.** Your tranche-1 insight — the Rive confound is on **her Judge-To side**, the mirror image of C-8 on the Judge-From side — is the general form. **A confound she cannot see is a false verdict in either direction.**

---

## Cross-seam contract change? (Principle 6 gate)

Does this dispatch add, modify, rename or remove any field on a telemetry schema table, a `fight_log` key, a loadout dict key, an export packet structure, or any inter-seam fixture dict?

**NO.** **Round-trip: not applicable — no cross-seam contract change in this dispatch.** This is Godot-side presentation authoring.

**Two items sit NEAR the boundary and are deliberately held on this side of it:**

1. **`multi_projectile`'s count / spacing / range** are named as ENGINE parameters by the spec. **You author the VFX to accept them; you do NOT wire them to engine emission in this dispatch.** If a later lap drives them from the engine, that is a contract change **then**, and it gets its own MIGRATION.md per ADR-004.
2. **`totem`'s delegate body** is a model-pipeline dependency, not a VFX one. **Placeholder + Discipline #40 declaration.** Opening the model pipeline is a scope amendment, not a build step.

---

## Acceptance criteria

- [ ] **E-0:** cathedral stage wired into the s2 harness; structured-content fraction **derived and reported** for both stages; C-3 uniformity verified **within each stage cohort separately**
- [ ] **E-1:** control arms re-captured for the four already-minted rows on the cathedral stage; **no re-mint**; any R-axis delta against structured geometry surfaced as a finding
- [ ] Seven base bindings minted, each demonstrably built to its row's stated layer decomposition
- [ ] Each row's Tier-1 parameterization demonstrated on the layers T-A permits and **NOT** on the layers T-A forbids — **the "must NOT" clauses are acceptance criteria**
- [ ] **`totem` authored two-layered** (`magical-cause` manifestation + `physical-cause` slam), with the **anticipation beat present and measured**
- [ ] **`self_buff` read-through retention measured** with a matched four-arm control against a tranche-1 effect
- [ ] **`circle`'s `annulus` layer flag** exists, and its **contact response on overtaken bodies is measured** (the single property separating it from the logged War Cry failure)
- [ ] **Rows 4 / 6 / 7 cross-row separation measured** — `single_target` vs `multi_projectile`(count=1) vs `line`; the fold boundaries proven at the gameplay camera, not asserted
- [ ] **`line` C-2 orientation asserted at ≥ 3 aim vectors**; lifecycle proven `travelling burst`, not `sustained`
- [ ] **C-8 census derived at every mark on BOTH stages**; any cathedral-stage emitter declared and classed
- [ ] **All three tranche-1 method pre-flights run per row**, with their receipts in `gate.json` (drawn-instance AABB non-degenerate; `00-pre`/`08-post` diff exactly 0 with effect disabled; every ratio matched on both sides)
- [ ] **RT-2 re-measured on CIEDE2000, not hue angle**, including a re-measure of the tranche-1 `neutral`/`wind` pair, with the ΔE(rendered) vs ΔE(added) fork test applied — **⚑ AMENDED BY A-4: RT-2 is recorded PER ROW with explicit `n/a` on the five non-`TRAIL-BOUNDED` rows; this tranche's RT-2 population is `melee_arc` + `multi_projectile`, and the fork test is now cross-row**
- [ ] **⚑ A-2 — the seven instrument sensitivity receipts, in `gate.json`, before rows 3–7 start**
- [ ] **⚑ A-6 — the cross-row separation threshold DERIVED** (within-row null + the `melee_strike`/`ground_targeted_circle` positive control from the tranche-1 captures), with the anti-tuning clause stated in the mint note before measuring
- [ ] **⚑ A-5 — the four assertable "must NOT" clauses carry named measurements**; `melee_arc` re-anchored off the non-portable ≈ 12 % coverage figure
- [ ] Mint note committed **before** minting, covering all six required items per row — **plus A-1's E-0/E-1 pre-registration, which fires before the first cathedral capture**
- [ ] ~~`KingRig.stock_vfx_enabled` default flipped to `false`~~ — **⚑ REMOVED FROM SCOPE BY A-7.** Not load-bearing for this tranche (tranche 1 hit `non_authored_emitter_count: 0` on 21/21 arms with the default still `true`). Derive the opt-in call-site set mechanically (#76 cl. 1), then flip in its own change with its own receipt.
- [ ] Confound registers re-audited where an extraction master was inspected; **delta reported in both directions**
- [ ] Round-trip: not applicable — no cross-seam contract change
- [ ] `AGENT_STATE.md` updated at session end
- [ ] Tag: `drax/v<X.Y>-s2b-mint-tranche-2`

---

## Quality criterion

**Game-quality goal this dispatch serves:** *telegraph literacy at the scale where it starts paying.* Tranche 1 proved one archetype can read as deliberate visual language. **This tranche is where the language acquires a grammar** — seven rows minted together, four of which sit on fold boundaries with each other (`single_target` / `line` / `multi_projectile`; `circle`'s annulus against the EoR failure). **A player learns a vocabulary by learning what its words are NOT**, and this is the only tranche in which those distinctions can be measured side by side before a player has to make them under pressure.

**Refutation conditions** (surface to knight-rider **before** executing if any apply):
- The cathedral stage does not materially raise structured-content fraction — **the S axis stays non-comparable and E-0 has not done its job**; say so rather than shipping the stage
- Two rows in this tranche converge in authoring (same emitter, same anchor, same coverage envelope) — **a fold finding; record it.** With three projectile-family rows in one tranche this is a live possibility, not a formality
- A row's "must NOT" clause cannot be honored without the effect becoming unreadable — **that is an RT-2/surface-class finding, not a licence to widen the tint**
- Acceptance criteria can pass without the effect reading as its archetype at the gameplay camera
- Building to T-A requires reopening a § 1 design-law ruling — **HALT to Matt, not a design conversation**
- The scope of this tranche (seven rows) proves too large to hold a consistent instrument across — **that is the HALT-and-surface circuit-breaker above; use it**
- A scaffold value ships without a Discipline #40 declaration

---

## Out of scope (explicit non-goals)

- **The 13 remaining T2/T3 rows** — `dash_attack`, `ground_slam`, `beam_channel`, `blink`, `cone`, `orbit`, `chain`, `vortex_pull`, `placed_lane`, `ricochet_bounce`, `teleport`, `leap_strike`, `fork`. Tranche 3, sequenced after this one gates.
- **`vortex_pull`** — **AUTHOR-not-SELECT**, blocked on the engine-side displacement dependency (X-2), and **RT-6 rules that a VFX-only score on it is not a score.** Not this tranche and not next unless the dependency has landed.
- **`self_buff`'s `transformation` sub-shape** — Matt's deserving list, § 5 Class-A item 2.
- **`totem`'s delegate BODY** — § 5 Class-A item 3, conditional Tier-2, **different pipeline**. Placeholder + declaration only.
- **`aura`'s `world_placed` (4) and `delegate_carried` (2)** — L-41; the latter is HELD as the summoner GAP. Nothing minted for either, and this tranche does not reopen them.
- **Tier-2 flourishes.** **Tier-2 law is SEALED** (A-1 YES · A-2 ADOPT + WW-AB · A-3 Synty-first/Meshy · **Class B REJECTED**). **Reopening any of the four is a HALT to Matt.**
- **Bespoke-per-kit anything.** Matt verbatim: *"We should only adopt one move per skill-type, not one more per kit."*
- **Re-minting the four already-minted rows.** E-1 is a **re-capture**, not a re-mint.
- **Asset-selection debates.** T-A gives semantics, readability targets, emitter geometry and constraints. **Asset selection is yours** (§ 7.1) — make it, record it, do not escalate it.
- **Re-grading elements / `vfx_mapping_tier`** — rocket's seam (X-3).
- **Rewriting the sealed spec.** Findings route to gandalf.
- Modifying anything under `Assets/` (read-only).

---

## Open questions for you to resolve and document

- Which pack assets get mounted per layer, per row, and why (§ 7.1 — explicitly yours)
- The element-variant set per row sufficient to demonstrate Tier-1 without becoming a content lap
- Whether `circle`'s `annulus` flag shares the base emitter cleanly (the RT-8 question, one row over)
- Whether the three projectile-family rows (4, 6, 7) separate at the gameplay camera on measurement rather than on intent
- Whether the cathedral stage introduces animated set-dressing that reintroduces method defect #2 through new geometry

---

## References

- Sealed spec: `gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` (STATUS governs)
- Charter + ledger L-1…L-41: `gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`
- Tranche-1 dispatch + completion record: `dispatches/2026-08-24-drax-s2a-mint-tranche-1.md`
- Tranche-1 mint note: `drax/notes/2026-08-24-s2a-mint-note.md`
- Gate procedure + tranche-1 scorecard: `galadriel/notes/2026-08-24-s2-minted-gate-procedure.md`
- RT-5 pre-flight: `drax/notes/2026-08-24-rt5-beam-vfx-preflight.md`

---

## Gate record

**jack-ryan Gate-1 DESIGN-MODE — 2026-08-24 — PASS-WITH-FINDINGS → ten amendments applied, BINDING.**
Approved directly under **ADR-002** (dispatch documents are documentation-only). **Nothing escalated to Matt** — no § 1 design-law ruling is implicated, no cross-seam contract moves, and no locked decisions-log entry conflicts (checked against `decisions-log.md` through `2026-08-24 #75/#76`).
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 5 (severity) · 6 (round-trip gate).
**Disciplines cited:** #1, #10, #40, #63, #70, #73, #75 (cl. 1–3), § 75.5 cl. 5.4, #76 (cl. 1).

### Ruling on the E-0/E-1 pre-Gate-1 split — LEGITIMATE, with one correction to its stated premise

The split holds. A dispatch is not indivisible, and executing a **landed** gate verdict (galadriel § 1.9, routed finding #7, class *procedure item*, routed to KR/drax) ahead of a review that has no standing over it is a refinement of the gate, not a hole in it. **I would not have ruled differently had I been in queue.**

**But the premise "carries no design surface" is false in two places, and both are cheap now:**

1. **E-0's fourth bullet partitions a pre-registered HALT population.** galadriel's HALT condition 3 fires on *"captures not rendered at the ratified albedo, or arms diverge."* Instructing drax to hold **two uniformity cohorts and not pool them** changes the set over which her own HALT evaluates. The instruction is substantively right — pooling two stages would manufacture a divergence — but it is a change to a gate's pre-registered condition made by the dispatcher. **Action: KR notifies galadriel that the cohort is partitioned, before she re-gates.** Not drax's to carry.
2. **E-0 has no math-before-code receipt, because § Math-before-code is row-scoped and E-0 has no row.** The stage fix is the item that conditions every subsequent measurement in this tranche, and as written its adequacy verdict would be authored *after* its result is known. **This is the one thing the split actually cost, and it is still recoverable.** See A-1.

### The amendments

**A-1 — ⚑ FIRES BEFORE THE FIRST CATHEDRAL CAPTURE (Discipline #1).** Write the **E-0/E-1 section of the mint note now**, pre-registering: the expected structured-content fraction for the cathedral stage, the margin below which E-0's refutation condition fires, and the two-cohort C-3 partition. If a cathedral arm has already been captured, state that in the note and mark the pre-registration as partial rather than back-dating it.

**A-2 — ⚑ THE FIVE NEW INSTRUMENTS EACH NEED A SENSITIVITY PROOF BEFORE THEIR READING IS EVIDENCE (#75 clause 2). This is the amendment that carries the tranche.** The claim *"the instruments now exist and are proven"* is true of tranche 1's instruments and **false of this tranche's**. Five surfaces here have never been run: (i) the cathedral stage, (ii) the structured-content derivation, (iii) **CIEDE2000 replacing hue angle**, (iv) the C-2 yaw assertion, (v) the cross-row separation measurement — plus two instrument *fixes* (`C8_DECLARATION` key, `vfx_probe_delta.py` coverage fields), which are new code paths, not repairs to proven ones. Each gets a **known-negative that must move the number**:

| # | Instrument | Known-negative that must move it |
|---|---|---|
| i | cathedral stage | structured-content fraction measured **effect-off** must equal the effect-on value (the stage number must not depend on the effect) **and** differ from the bare stage by the A-1 margin |
| ii | structured-content derivation | ⚑ **NUMBER CORRECTED BY GALADRIEL 2026-08-24 (Amendment G-4) — jack-ryan's row as authored said "reproduce galadriel's **0.218 %** (§ 2.0)"; the correct target is **0.304 %, Sobel \|∇\| > 10, § 1.9a**.** Both figures are real and measure the same frame with different operators; § 2.0's is forward-difference and has no cathedral counterpart, so it cannot found the instrument while the bars are Sobel-denominated. Run the derivation on the **bare** stage and reproduce **0.304 %**, naming the operator. A derivation that cannot reproduce a known value is not yet an instrument — *and a known value restated without its operator is not a known value* |
| iii | CIEDE2000 | a **known-identical** pair (one element, two arms) → ≈ 0, **and** a **known-different** pair (`fire`\|`water`, tranche-1 hue sep 31.2°) → large. Both legs, or the metric change is unproven on this harness |
| iv | C-2 yaw assert | one arm with a **deliberately wrong** yaw; the assertion must **fail**. A yaw assert that has only ever passed is #75 cl. 2 verbatim |
| v | cross-row separation | the positive control in A-6 |
| fix a | `C8_DECLARATION` + `fx`/`rt` | re-derive the collision set after the fix; tranche 1 collapsed **8 declarations onto 2 keys** — the receipt is that delta going to **zero** |
| fix b | `vfx_probe_delta.py` | emit one record where the all-frame and sampled coverages **differ**, proving the two are now separable on the record (§ 75.5 cl. 5.4) |

**Rows 3–7 do not start until these seven receipts are in `gate.json`.** They cost two arms and no re-render.

**A-3 — the HALT-and-surface circuit-breaker is RE-SPECIFIED, because as written it cannot fire.** Its trigger is *"if any new instrument defect of the tranche-1 class appears in rows 1–2."* Tranche-1-class defects are **silent by construction** — #75's own text: *"all five probes were checked, in the sense that their authors read them and believed them; four of five returned values in a plausible range, which is what suppressed the check."* A breaker that depends on noticing an undetectable-by-construction defect is an intention, not a control. **Replaced by a scheduled receipt gate: A-2's seven receipts ARE the checkpoint.** If any fails, **the cut is 7 → 4** — mint `self_buff`, `totem`, `circle`, `melee_arc` (independently mintable) and **re-dispatch rows 4/6/7 as a unit**, because the projectile trio's value is co-tranche measurement and cutting one of the three destroys the other two's criterion. **Seven rows is not the wrong number. Seven rows on seven un-sensitivity-proven instruments is the wrong number.**

**A-4 — state the Tier-1 surface class per row, and name the RT-2 population (#63, #70).** The dispatch's own Math-before-code item 2 sends drax to *"the row's Tier-1 surface-class clause"* and then omits the class on **four of seven rows**. From the sealed spec: `self_buff` **FIELD-CARRIED** · `totem` **PAYLOAD-CARRIED** (delegate attack only) · `circle` **PAYLOAD-CARRIED** · `single_target` **PAYLOAD-CARRIED** · `melee_arc` **TRAIL-BOUNDED** · `multi_projectile` **TRAIL-BOUNDED** · `line` **PAYLOAD-CARRIED**.
**Consequence the dispatch missed: RT-2 fires only on TRAIL-BOUNDED rows, so this tranche's RT-2 population is `melee_arc` + `multi_projectile` — and the dispatch identifies only one of the two.** Record RT-2 **per row** with explicit `n/a` on the other five, as galadriel did in tranche 1 — do not omit.
**And this is an upgrade, not just a correction: two TRAIL-BOUNDED rows on one palette make the § 1.3 fork test cross-row for the first time.** RT-2 firing on **one** row indicts the **row**; firing on **both** indicts the class or the palette, and ΔE(rendered)-vs-ΔE(added) decides which. Tranche 1 could only run that fork within a single row. **The second row is free — it is being captured anyway.**

**A-5 — four "must NOT" clauses admit numeric treatment and currently have none; one is mis-anchored.** Answering the dispatcher's question directly: **five of the prohibitions are assertable, three are provenance/scope prohibitions correctly honoured by declaration, and one is anchored to a bar galadriel already ruled non-portable.**

- `self_buff` **"never let a Tier-1 recolour raise coverage"** → assert `coverage(element_i) ≤ coverage(baseline) + ε` across element arms. Same shape as `aura`'s ring-radius spread **0.5 px**. **"Cap opacity and radius"** has **no number and no source** — derive the cap from the read-through requirement rather than declaring one, and state the derivation.
- `self_buff` **read-through** — *"meaningfully below 1.0"* is not a threshold. Tranche 1 returned **0.998** on `aura`; use it as the anchor and state the band. Run it on `aura`'s **worst-case element** too (galadriel finding #6, 1.84× effective-opacity spread, *"read-through untested on the worst-case element"* — cheap to close, and this row is where it matters for 112 skills).
- `totem` **"the slam must show the contact step change; the manifestation must not"** → **the sharpest test in the tranche**: galadriel's § 1.2 test (3) applied twice on one row with **opposite expected signs**. Tranche 1's `melee_strike` gives the scale (0.2 % → 34.1 %). **Promote it to an acceptance criterion** — it is currently only in the row body. Likewise the anticipation beat: *"measured"* names no measurement; GTC's *"telegraph full at 0.183 s with payload 5.5 m out"* is the precedent shape — report lead time and delegate-pixel activity before `t_slam`.
- `circle` **`annulus`** → **two comparisons with opposite expected signs on one record, and the dispatch names only one.** `perimeter_hash` **byte-identical** proves shared emitter (identity = good); interior fill must **differ** by a stated margin (identity = a near-inert parameter, which is exactly galadriel's finding #5 on `payload_vector`: byte-identical at 7 of 8 marks). Name both, with their own coverage each (**§ 75.5 cl. 5.4**).
- `multi_projectile` **"count / spacing / range are ENGINE params, not Tier-1"** → **the clearest missing assert in the tranche, and tranche 1 already ran its twin.** Assert **spread ≈ 0** for projectile count, angular spacing and range **across element arms**. *Not conflating them* is an intention; a zero spread is a receipt.
- `melee_arc` **"DO NOT thicken the crescent into a field"** → ⚠ **the dispatch hands drax `Reference coverage ≈ 12 %`, which is the one bar galadriel's § 1.6 ruled NON-PORTABLE** (*"never against a spec percentage lifted from another camera"*) — the same C-3-error-class door the ≈ 20 % GTC finding closed at tranche 1. **Re-anchor to the two properties that are portable:** (a) **angular extent < 360° and radial thickness / outer radius**, which is what makes a crescent not a field; (b) **"terrain visible THROUGH the arc"** and **"caster legible and NOT occluded"**, both stated in the spec as the explicit correction of EoR failure #2, both directly measurable as background-structure retention and caster-pixel retention. **Note the interlock: on a 99.78 %-bare floor, "terrain visible through the arc" is untestable because there is no terrain. E-0 is what makes this row's core prohibition measurable at all** — which is an independent argument for the stage going first.
- **Correctly honoured by declaration, no assert owed:** the `transformation` sub-shape, the delegate body (**#40** scaffold), Hades II as beats-only, the excluded War Cry frames, and the Javelin `t_end`. These are scope and provenance boundaries, not measurable properties. Do not manufacture asserts for them.
- `line`: two cheap receipts the dispatch asks for in prose — **`travelling burst`** = authored coverage returns to zero with no steady-state plateau; **no UID-cache rebuild** = cache hash byte-identical before/after, exactly as RT-5 already demonstrated. Put both in `gate.json`.

**A-6 — the cross-row separation criterion is LEGITIMATE and its missing threshold is a real defect. Do not invent one — derive it.** The criterion as written (*"proven separable at the gameplay camera"*) is a **rendered-appearance** claim carried by intent, and this wave already ruled that **only pixels refute pixels** (#19.1, per-claim-type row, 2026-08-24). Construct it as a pairwise separation matrix over **rendered shape descriptors** at the ratified camera — aspect ratio, radial extent, trail length/width, pierce persistence past first contact, payload count, contact-event count and location — with the three arms held at **one fixed element** (#10).

- **Null (lower bound):** within-row separation across the same row's element arms. Under the P-axis geometric-invariance requirement this should be ≈ 0, and it is being measured anyway.
- **Positive control (scale anchor):** `melee_strike` vs `ground_targeted_circle` — two **already-minted, unambiguously distinct** rows whose descriptor distance is computable from the tranche-1 captures **at zero cost**. This is also A-2's item (v) sensitivity proof: a separation instrument that has never been shown to return "distinct" is not an instrument.
- **Pass criterion:** cross-row separation among {`single_target`, `multi_projectile`(count=1), `line`} **exceeds the within-row null by a stated margin**, reported against the known-distinct pair as scale. Threshold with a source, both legs free.
- ⚑ **Anti-tuning clause, and it is binding.** A negative result is a **finding routed to gandalf about L-29's fold**, **NOT a licence to differentiate the effects until the number passes.** A threshold on an acceptance criterion creates pressure to author artificial distinctness, which would corrupt the archetype semantics T-A locked — § 75.5 cl. 5.6 inverted (*do not change the artifact to suit the instrument*). **Say this in the mint note before you measure.**

**A-7 — `KingRig.stock_vfx_enabled` comes OUT of this dispatch's scope and tag.** It is drax's to decide (seam authority, ADR-002) and the routed decision is sound. Two reasons it does not belong here: (a) **it is not load-bearing for this tranche** — tranche 1 already achieved `non_authored_emitter_count: 0` on **21/21 arms with the default still `true`**, via the declarative export, so the confound is already controlled; (b) it changes scenes **none of the seven rows exercise**, so it would ship untested inside a tag whose gate measures VFX mint quality — one tag, two unrelated changes, one receipt (#10 at the dispatch layer).
⚠ **And as written it is a bare hand-list: "four call sites" / "a handful of scenes" / "materially larger than a handful" is a threshold with no derivation, which makes the escape hatch undecidable.** **#76 clause 1**, whose standing effect is *"Gate-1 surfaces a bare hand-list with no governing predicate as WARN at minimum"* — applied here to a dispatch I did not author, on a rule whose founding instances are two documents I did. **Derive the opt-in call-site set mechanically, report it, then flip, in its own change.** The derivation also makes KR's own stop-and-tell-me condition decidable for the first time.

**A-8 — declare the two-stage coverage boundary, and state the disposition of tranche 1's verdicts (#70, #63).** E-1 produces a **second capture set for four already-verdicted rows on a different stage.** Nothing may pool them. Two things need saying in the mint note: (a) every arm declares its stage, and any absolute R or S claim names the stage population it covers; (b) **E-1 is not a re-open.** My Gate-2 verdict on `drax/v0.1-s2a-mint-tranche-1` scored the **record** and is unaffected. galadriel's tranche-1 R scores were capped at 4 *citing this exact stage limitation* (§ 2.0), so an R-axis delta on the cathedral stage is a **finding on the harder test**, as the dispatch already says — it is hers to disposition, and she should say whether it re-scores or annotates. **Better raised now than discovered at her re-gate.**

**A-9 — four refutation conditions added to the § Quality criterion block.**
1. **Any of A-2's seven sensitivity receipts fails** → A-3's cut fires. *(The block currently has no condition covering its own new instruments — the largest gap in it.)*
2. **The cathedral stage's own emitters cannot be held constant across arms** → the stage has traded one non-comparability for another. Declared-and-classed satisfies galadriel's HALT 1, but a brazier that is an authored **light source** moves C-3 and the R axis. *Declared is not the same as controlled.*
3. **The three projectile-family rows do not separate on RENDERED descriptors** → fold finding to gandalf, under A-6's anti-tuning clause. The existing condition covers *authoring* convergence (same emitter/anchor/coverage); three rows can be authored differently and still render indistinguishably, and it is the rendered side that reaches a player.
4. **RT-2 splits across the two TRAIL-BOUNDED rows** → row indicted, not class; both → fork test decides (A-4).

**A-10 — `circle`'s windup donor is missing.** Spec § 3.1.5 carries **D3 · Condemn** as *"the corpus's best windup donor for the radial-burst family,"* explicitly against the run-wide **80.5 % windup scarcity**. The dispatch carries the row's excluded-frames finding and drops the donor. `circle` is the **only row in this tranche with a named windup donor**, its lifecycle is `burst` with windup Y, and this dispatch's own quality criterion is telegraph literacy — for a caster-centred expanding annulus that is *"structurally the same object"* as the EoR failure, the windup is the second separator after the contact response. **Restore it.**

**ℹ INFO — one overclaim, corrected so it cannot bend a threshold.** *"The only tranche in which those distinctions can be measured side by side"* is not true: once rows 4/6/7 are minted, re-capturing them together is cheap. Overstating the one-shot-ness creates pressure to accept a weak separation result rather than re-run — which is precisely what A-6's anti-tuning clause exists to prevent. **The cross-row measurement is high-value because it is early, not because it is unrepeatable.**

### Verified clean, stated so it is not re-litigated

- **Principle 6 gate — the `NO` is correct.** Verified independently: all seven rows are `reincarnated-godot/` presentation-internal; `multi_projectile`'s count/spacing/range are held on this side of the boundary; `totem`'s delegate body is held as a model-pipeline dependency. **No MIGRATION.md owed** (ADR-004). Round-trip **n/a**.
- **Spec fidelity, rows 1–7, checked line-by-line against § 3.1.3–3.1.10.** No row mis-states its emitter geometry, causality class, lifecycle class or scope boundary. The two hardest constraints to carry — `totem`'s `two-layered` split causality and `line`'s `travelling burst` vs `beam_channel` — are carried **more explicitly than the spec states them**. A-4 and A-10 are omissions, not distortions.
- **Quarantine handling is correct** — the tranche consumes none of L-36/L-37/§ 5/carve-out, the reach-for-§-5 signal is the right tripwire, and lifting is correctly left to gandalf.
- **Both Gate-2 WARNs from `2026-08-24-step2-first-landings.md` are folded in and correctly characterised**, including WARN-1's *latent-not-active* status and why a two-stage tranche is where it stops being latent.

### Pre-declared Gate-2 BLOCK condition (stated in advance so it is an output, not a judgment under pressure)

**If rows 3–7 are minted without A-2's seven sensitivity receipts in `gate.json`, that is a Gate-2 BLOCK on the tranche-2 tag.** Declared here rather than issued now because the fix is additive, drax has not reached Row 1, and I hold dispatch-amendment authority under ADR-002 — a BLOCK now would stop work that an amendment can steer. **Seven rows re-minted on an instrument found wrong at row 6 is the outcome this clause exists to buy off, and it is the same arithmetic the dispatch used to put E-0 ahead of the rows.**

### Disposition

- **E-0 / E-1: CLEARED, continuing** — with **A-1 firing before the first cathedral capture** and KR notifying galadriel of the cohort partition.
- **Rows 1–7: CLEARED TO START** on A-1 and A-4 being folded into the mint note. A-2's receipts gate **rows 3–7**, not rows 1–2.
- **A-7 leaves this dispatch's scope.** Everything else is a mint-note and `gate.json` obligation.
- **Nothing escalated to Matt.**

---

## Completion record

**Appended by drax, 2026-08-24.** Godot `08d4715`; tags `drax/v0.1-s2b-e0-stage-fix` and
`drax/v0.1-s2b-e0-gate1-amendments`, both pushed.
Mint note: `agentic_orchestration/drax/notes/2026-08-24-s2b-mint-note.md`.
Receipts: `reincarnated-godot/harness_logs/s2b_e1_2026-08-24/{gate,sensitivity}.json` (152 PNG).

### Status: **E-0 + E-1 + the two unblocked C-8 items COMPLETE. Rows 1–7 NOT STARTED.**

Gate-1 landed **mid-execution**. Its ten binding amendments re-scope the rows, and four of
them change what a row mint must contain before it can begin — **A-2/A-3** (the receipt gate
that replaces the circuit-breaker), **A-4** (surface classes omitted on 4 of 7 rows; this
tranche's RT-2 population is `melee_arc` + `multi_projectile`, making the § 1.3 fork test
cross-row for the first time), **A-5** (`melee_arc`'s ≈ 12 % bar is the one § 1.6 ruled
non-portable), **A-6** (derived separation threshold). Starting Row 1 would mint against a
scope already amended.

### E-0 — the derived answer

**Instrument calibrated before it was believed.** HLF ported verbatim from
`register-metrics.mjs` and re-measured against galadriel's own anchors: graybox **14.342 %**
vs published **14.4 %**; cathedral **9.451 %** vs **9.35 %**. *(And the published anchors are
lifecycle **maxima**, not means — comparing against a mean would understate every stage by
~2 pp.)*

| stage | structured content | vs bare | HLF (control) | HLF (effect ON) | max luma, effect ON |
|---|---:|---:|---:|---:|---:|
| bare | **0.304 %** | — | 0.0015 % | 0.0064 % | **242** |
| **cathedral** (ordered) | **23.440 %** | **77.1×** | 0.0000 % | **0.0000 %** | 193 |
| **arena** (built after measuring) | **45.111 %** | **148.4×** | 0.0000 % | **0.0000 %** | 195 |

**On the dispatch's stated refutation test, E-0 passes decisively.** Two things it did not
anticipate:

- **The 9.35 % anchor is ~80 % hero VFX.** Decomposed along its own lifecycle: pre-ignition
  (braziers only) **1.71–2.50 %**, hero burn **6.32–9.45 %**, post-stop 2.84–3.96 %. It is
  not a stage number and should not be used as one.
- **HLF does not survive the fix, and geometry is not why.** The same effect peaks at luma
  **242** on the bare env and **195** on the lift env — either side of the 204 cut. Lowering
  the cut inverts the wrong way (at >150: bare 0.078 %, arena 0.016 %). **The cohorts sit on
  different transfer functions: HLF is non-comparable across TONEMAPS, a direction § 1.9 had
  not named.**

**Replacement instrument proposed — GLF**, the fraction of authored pixels landing where the
*control* frame carries geometry (∇ > 10):

| row (peak) | bare | **arena** | cathedral |
|---|---:|---:|---:|
| `melee_strike` @ contact | 0.194 | **0.676** | 0.515 |
| `ground_targeted_circle` | — | **0.717** | 0.250 |
| `aura` @ steady | 0.114 | **0.700** | 0.279 |
| `whirlwind` @ sustain | — | **0.835** | 0.712 |

**68–84 % of every effect's light lands on environment geometry on the arena stage, against
3–19 % on bare — and that bare fraction is the actors' own silhouettes, the only structure a
bare floor has.** It operationalizes § 1.9's own wording and was *unaskable* before E-0.

**⚑ A third recipe was built because the measurement said to.** `Demo_Cathedral_01.tscn` is a
six-section **showcase diorama**, not a room; its ritual circle sits on an **outdoor terrace**
and at the ratified camera terrain occludes **81 %** of `melee_strike`'s authored pixels
(13,802 arena → 2,589 cathedral). `arena` is the same pack and same lift rig in a room the
camera can photograph, lifted from `render_boss_arena.gd`, sized from **our** camera footprint,
with two pillar rings because § 1.9 asked literally for *"pillars for VFX light to fall on"*.
**Recommended as the S-axis cohort of record;** the cathedral is retained and captured beside it.

**C-3 uniformity — per cohort, never pooled**, and the finer cohort is the real one (a pooled
spread on a textured floor measures the roster, not albedo divergence):

| cohort | `melee` | `gtc` | `aura` | `whirlwind` |
|---|---:|---:|---:|---:|
| arena | **0.0000** | **0.0000** | **0.0000** | 0.8716 |
| cathedral | **0.0000** | **0.0000** | **0.0000** | 2.4192 |

Three of four rows reproduce tranche 1's 0.000 receipt on both new stages. Whirlwind's spread
is the caster **moving at 3.5 m/s** through the sample band — an archetype property, named.

**C-8 on new geometry:** cathedral ships **0** particle emitters and 29 OmniLights (1 survives
the arena filter); arena carries 4 static brazier OmniLights. All `INHERITED-BY-DESIGN`,
census-enumerated at every mark, inside `C8_DECLARATION`. The lift recipe's hero VFX are
omitted **and the omission is declared**.

### E-1 — four rows re-captured, with the receipt that it is not a re-mint

152 PNG, both structured stages, `fx=on` + `fx=novfx` per row per stage (two arms, not the one
allowed — method defect #3 was a ratio missing a control on one side).

> **46 of 46 `melee`/`gtc`/`aura` fx-on frames BYTE-IDENTICAL across the § 3.1 control fix.**

**R-axis delta:** against the arena stage three of four rows hold **89–94 %** of bare-stage
authored pixels, mean added luma 27–31 on structure. **The effects survive structured
geometry. Nothing was retuned to rescue a number** — including `melee_strike`'s 81 % loss on
the cathedral, where the stage was indicted instead, which is where the fault was.

### ⚑ FOUR new defects of the tranche-1 class

1. **`s2a_ground_circle.fire()` un-stripped its own control.** `visible=false` at build time,
   `visible=true` at run time ⇒ fx and ctl **byte-identical** ⇒ gate reported
   **`authored_px = 0`**, which reads as *"invisible against structured geometry"*, an R-axis
   finding, and was a **contaminated control**. Never fired before: tranche 1 had **no novfx
   arm on this row**. Fixed; true figure **88,761 px**.
2. **⚑ `wwcr_stage.gd` NEVER RECEIVED THE TRANCHE-1 CLOCK PIN.** Two runs of *unmodified* code
   differ by **144–1,028 px**, including at `00-pre`. **I found method defect #2, fixed it
   where I found it, elevated it to a standing pre-flight, and left the sibling stage alone.**
   Back-ported; **0 drift across two runs on all 10 marks.**
   **This affects the LANDED `whirlwind` clean-room mint (`1692d6e`,
   `drax/v0.1-s2-whirlwind-cleanroom-1`) — its ON/OFF diffs carry animation phase. Whether
   that moves the WW-AB verdict is galadriel's call. ROUTED.**
3. **My own gate table read two archetypes' SPECIFIED residue as broken determinism**
   (`gtc 07-late = 56,984`, `ww 09-off = 3,973`). Localising the pixels settled it. **A
   plausible number can be a false alarm as well as a false pass.**
4. **⚑ The gradient operator — and Gate-1 caught this one, not me.** I calibrated against
   § 2.0's **0.218 %** (forward-difference), landed on `sobel/4 = 0.2699 %`, and **declared a
   1.24× offset**. A-2(ii) + galadriel's **G-4** give the correct target: **0.304 %, Sobel
   |∇| > 10, § 1.9a**. Re-swept: **raw Sobel = 0.3038 %**. *0.2699 % matched neither published
   operator, and declaring an offset made the mismatch look handled.*

Plus **reported-not-fixed**: the `wwcr` novfx control is not pose-matched before `T_BEGIN`
(83 px at `00-pre`). The repair reaches inside a minted effect, which E-1 forbids; the failing
receipt ships as a failing receipt.

### Gate-1 amendments folded

| | |
|---|---|
| **A-1** | Pre-registration marked **PARTIAL and NOT back-dated** — arms were already captured, so § 1.5's adequacy verdict was authored after its result was known. The two-cohort C-3 partition and the derive-don't-declare rules **were** genuinely pre-registered in code. |
| **A-2** | **3 of 7 sensitivity receipts BANKED**, all PASS: structured-content reproduces 0.304 % to **0.0002** with the operator named; the stage number **does not depend on the effect** (effect contributes 0.16–2.6 % of stage content — I did *not* claim exact equality, which is the flattering answer and is false); **CIEDE2000 on BOTH legs** — known-identical **ΔE = 0.0000** using *two different RT-8 arms that render byte-identical*, not a file against itself; known-different **18.70**. **4 owed before rows 3–7.** |
| **A-3** | Receipt gate accepted as the checkpoint replacing the circuit-breaker. |
| **A-6** | Anti-tuning clause **recorded before any cross-row measurement exists**. |
| **A-7** | ⚠ **BREACH, DISCLOSED.** The `stock_vfx_enabled` flip shipped inside `drax/v0.1-s2b-e0-stage-fix` before A-7 landed. **Tag not deleted or moved** (destructive, not mine unasked) — revert-and-reland is **KR's call**. A-7's *substantive* requirement is met: the opt-in set is **derived mechanically with a stated governing predicate** (#76 cl. 1), **15 sites — 7 opt in, 1 explicit false, 7 new default**, against an estimate of four. |

### RT-2 on CIEDE2000 — my tranche-1 finding is REFUTED

**`fire|earth` is the minimum on all four marks; mask choice never moves it. My
`neutral|wind` "3.0°" is third and is refuted.** Third independent measurement, same verdict —
plus one addition: **the collapse is tightest at CONTACT (6.50), not on the trail (7.28)**,
i.e. at the instant the effect is largest and the player is looking. `neutral|water` (7.35) is
a fourth pair absent from both prior matrices. **Fork test: ratio 0.805–1.053, mean |transfer|
1.66 ΔE ⇒ FAITHFUL TRANSMITTER. RT-2 does not fire; surface class exonerated, PALETTE indicted
→ rocket (X-3).**

### Acceptance criteria

| Criterion | Status |
|---|---|
| E-0 stage wired; structured-content **derived and reported** for both stages | ✅ |
| E-0 C-3 uniformity **within each cohort separately** | ✅ (+ per-row refinement) |
| E-1 control arms re-captured; **no re-mint**; R-axis delta surfaced | ✅ byte-identity receipt |
| **RT-2 re-measured on CIEDE2000**, tranche-1 pair re-measured, fork test applied | ✅ **refuted** |
| `stock_vfx_enabled` flipped, opt-in derived | ✅ — ⚠ **but tag-scope breach, A-7** |
| C-8 census derived at every mark on both stages; new emitters declared and classed | ✅ |
| Mint note committed | ✅ |
| Round-trip: not applicable — no cross-seam contract change | ✅ |
| Tag + push | ✅ ×2 |
| Sealed spec **not** patched; findings routed to gandalf | ✅ |
| Nothing under `Assets/` modified | ✅ |
| `AGENT_STATE.md` updated | ✅ |
| **Seven rows minted** | ❌ **NOT STARTED — Gate-1 amendments re-scope them; 4 of 7 A-2 receipts owed** |

**8 findings routed** (mint note § 8) — galadriel (3), knight-rider (2), rocket (1),
jack-ryan (1), gandalf via KR (1). **Not escalated to Matt:** no § 1 design-law ruling
required reopening; no sealed binding moved; the sealed spec was not patched.

