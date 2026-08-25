# Dispatch — 2026-08-24 — drax — Step-2 VFX mint, TRANCHE 2 (the seven remaining T1 rows + the stage fix)

**Status:** PENDING — FIREABLE
**From:** knight-rider (Step-2 build wave, carve-out #2)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-24 (launch word covering the whole carve-out #2 agenda)
**Pattern:** B (dedicated session)
**Gates:** jack-ryan Gate-1 DESIGN-MODE — **pending; see § Gate record.** Fire on his return; do not wait to start **E-0**, which is a stage fix ordered by a landed gate verdict and carries no design surface.
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
- [ ] **Derive the stage's structured-content fraction the way you derived the emitter census** — do not declare it. galadriel measured the s2a stage at **99.78 % bare floor / 0.218 % structured content (∇ > 10)**. Report the same two numbers for the cathedral stage so she can state what her instrument is standing on. If the cathedral stage also comes back near-bare, **that is a finding and the S axis stays non-comparable** — say so rather than shipping a stage that does not fix the thing it was built to fix.
- [ ] **C-3 uniformity check extends to the new stage.** galadriel's method: sample a ground band away from caster and effect in **every** arm; floor luminance must be consistent within a stage. Tranche 1 returned spread **0.000** across 21 arms. Two stages means **two** uniformity cohorts — do not pool them, and do not let a cathedral arm read as a divergent-albedo outlier against bare-stage arms.

### E-1 — backfill the four minted rows (cheap, and it makes the whole gate comparable)

- [ ] **Re-capture control arms only for `melee_strike`, `ground_targeted_circle`, `aura` and `whirlwind` on the cathedral stage.** **NO RE-MINT.** Nothing about those four effects changes; you are re-photographing them against an instrument that can see the S axis.
- [ ] One arm per row is sufficient. If an effect's *readability* changes materially against structured geometry — an additive effect that had near-perfect contrast by construction on a bare floor may not — **that is a finding about the R axis on the harder test**, and galadriel's own § 2.0 anticipates it: her stage *"reproduces the flattering condition."* Surface it; do not tune the effect to rescue the number.

**E-0 and E-1 are the only items in this dispatch that may proceed before the Gate-1 record below is filled in.**

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
- **C-5 — readability floor AND ceiling** (0.03 % → 67 %). Binds every row. Your own C-5 invisibility datum (`p_trail` 535 px) is the floor you measure against.
- **C-7 — beam-pack `uid://` fragility.** **Measured and non-blocking (RT-5), with one standing prohibition: do not trigger a UID-cache rebuild.**
- **C-6** (zero attractor content) binds `vortex_pull` — not in this tranche.

### ⚑ C-8 — carry it forward, derived, on both stages

`s2a_census.gd` exists and it earned its keep: it found a third emitter nobody had enumerated (the Greatsword's emissive material, **on the very blade the trail is generated from**). galadriel accepted the tranche-1 declaration **specifically because it was derived by ancestry rather than hand-listed** (Discipline #76).

- [ ] **Run the census at every capture mark, on both stages.** The cathedral stage is new geometry and **new geometry is exactly where an un-enumerated emitter enters** — a torch, a brazier, a glowing rune on a wall. If the cathedral recipe ships emissive set-dressing, **that is not automatically a defect** (a lit environment is the point), but it **must be declared and classed** — INHERITED-BY-DESIGN is a legitimate class; INHERITED-AND-UNNOTICED is not.
- [ ] **`KingRig.stock_vfx_enabled` — routed to me at tranche 1, and I am routing it back to you with a decision.** You own `reincarnated-godot/` end to end, so the flip is yours to make; what you correctly escalated is that it changes *other scenes' behaviour*, and that is the part I am answering. **Flip the default to `false`, and make the throne-room / presentation scenes opt in explicitly.** Rationale: a default that ships the L-19 failure mode into every frame is a default that is wrong in the common case, and an opt-in at four call sites is cheaper than a confound in every capture forever. **If the opt-in surface turns out to be materially larger than a handful of scenes, stop and tell me** — that changes the arithmetic and I will take it back.

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
- [ ] Lifecycle `burst`.

### Row 4 — `single_target` (§ 3.1.6) — 90 skills / 77 kits

- [ ] Mint: projectile · **three visibly separated layers — (a) payload body, (b) trail, (c) impact residue on the target.**
- [ ] **This row has the cleanest Tier-1 evidence pair in T-A: two references supplying BOTH causality classes on identical delivery geometry.** Canonical Essence Drain is `magical-cause`; runner-up LE Javelin is `physical-cause` **with contact WITNESSED** (t ≈ 5.60 s, white burst on an enemy body, red streak leading in). **Cite the runner-up for physical-element parameterizations.**
- [ ] **Tier-1: tint all three layers; motif-swap the payload body** (orb → spear → shard → bolt).
- [ ] ⚑ **THE LOAD-BEARING BOUNDARY — and it constrains a dimension, not a colour.** Essence Drain's trail is **narrow enough that it does not read as a beam.** Javelin's flight streak spans **≈ 40 % of the crop width and reads as an elongated luminous LINE.** Under L-29(4), protecting the `single_target` / `line` boundary is load-bearing for archetype identity — **Essence Drain PROTECTS it; Javelin SOFTENS it.** **Measure your trail's aspect ratio and put it in `gate.json`.** You are minting `line` in this same tranche (Row 7); **the two rows must be distinguishable at the gameplay camera, and you are the only person who will ever see them side by side before a player does.** A cross-row separation measurement between Rows 4 and 7 is the single highest-value thing this tranche can produce that no single-row dispatch could.
- [ ] ⚠ **`reference_window` has a `t_end` for a reason.** Measured **t ≈ 0.40 – 0.90 s**. **Later segments of the Javelin clip show denser multi-projectile multi-hit behaviour that MUST NOT be read as base `single_target` grammar** — and you are minting `multi_projectile` in this tranche too, so the contamination risk is live in both directions.
- [ ] **Javelin's honest limits, carried forward:** the dark spear against dark terrain at t = 0.53 / 0.73 is **genuinely low-contrast** and identity is carried almost entirely by the wake — **a real risk in our dark-mood register**, and E-0's cathedral stage is where that risk becomes visible. The clip is **1280×500, horizontally letterboxed — vertical framing and vertical coverage CANNOT be assessed from it.** It is a geometry and phase-separation master, **not a camera-framing reference.**
- [ ] Lifecycle `burst` (travel + impact).

### Row 5 — `melee_arc` (§ 3.1.7) — 76 skills / 63 kits · `physical-cause`

- [ ] Mint: caster-origin, frontal, ground-plane · layers — **(a) a broad TRANSLUCENT pale crescent on the ground plane (radius ≈ 2× character height), (b) contact response on bodies inside it.** Reference coverage ≈ 12 % — mid-band against C-5.
- [ ] **Caster legible at the arc's origin and NOT occluded; terrain visible THROUGH the arc.** That is the **explicit correction of EoR failure #2** and it is an acceptance criterion.
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
- [ ] **RT-2 re-measured on CIEDE2000, not hue angle**, including a re-measure of the tranche-1 `neutral`/`wind` pair, with the ΔE(rendered) vs ΔE(added) fork test applied
- [ ] Mint note committed **before** minting, covering all six required items per row
- [ ] `KingRig.stock_vfx_enabled` default flipped to `false` with explicit opt-in at presentation scenes — **or** an escalation to KR if the opt-in surface is materially larger than a handful of scenes
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

- jack-ryan Gate-1 DESIGN-MODE: **PENDING.** He is in session on the X-6 methodology ruling + standing Gate-2 on the tranche-1 tags; this dispatch enters his queue on return.
- **E-0 and E-1 may proceed immediately** — they execute a landed gate verdict (§ 1.9) and a routed finding, and carry no design surface for Gate-1 to rule on.
- **Rows 1–7 begin on the Gate-1 record being filled in above.** If Gate-1 returns amendments, they apply under ADR-002 without escalation unless a § 1 design-law ruling is implicated.

---

## Completion record

*(to be appended by drax)*
