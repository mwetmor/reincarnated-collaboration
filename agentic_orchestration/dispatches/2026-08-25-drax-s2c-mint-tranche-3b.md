# Dispatch — 2026-08-25 — drax — Step-2 VFX mint, TRANCHE 3B (the five linear/beam rows) + the P-BEAM fork

**Status:** PENDING — **GATED on P-BEAM (§ 0) resolving. P-BEAM is IN THIS DISPATCH; it is not a separate errand.**
**From:** knight-rider (Step-2 build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Approved by:** Matt, 2026-08-25 (launch prompt — go-word for tranche-3 authoring + fire)
**Pattern:** B (dedicated session)
**Sibling:** `2026-08-25-drax-s2c-mint-tranche-3a.md` (the eight beam-pack-independent rows). **3A does not wait on this dispatch.**

---

## Why these five are one dispatch

**All five are primitive `line` or line-derived. All five carry the C-2 orientation contract. All five are beam-pack-adjacent.** They share one dependency and one failure mode, so they share one pre-flight.

They also contain **two distinctness pairs the tier ordering would have split** (see the 3A sequencing ruling): `beam_channel` ↔ `chain` (**T2 vs T3**), and `fork` / `ricochet_bounce` ↔ the already-minted `multi_projectile`.

---

## § 0 — ⚑ P-BEAM: THE LOADING ≠ CAPTURING FORK. RESOLVE IT BEFORE ANY CAPTURE.

gandalf's brief, verbatim: ***"resolve BEFORE capture, never discover after."*** So this is § 0, with a **pre-registered decision rule** — not a judgement you make under pressure with four rows already minted.

### The evidence, cited not re-derived

`drax/notes/2026-08-24-s2b-mint-note.md:1127-1142` — **RT-5 cleared the Binbun `beam_vfx` pack for LOADING. Loading is not CAPTURING.** Three renders of **one identical `laser_vfx_01` arm** produced **three different frames**: pass 2 vs pass 3 differed by **2,680 px** against ~39,800 authored px — **~6.7 % of the authored mask drifting between renders of the same thing.**

Contributing structure: **2 `GPUParticles3D` unpinnable to the stage clock**; **7 `ShaderMaterial`s** classify only as `shader?` **UNKNOWN**.

Your own conclusion, and it is correct: **a payload that differs from ITSELF by 2,680 px supports no Tier-1 claim.**

⚑ **State the general form, because it is why this is § 0 and not a footnote:** a Tier-1 claim is *"recolour moves colour and ONLY colour."* That is a **difference measurement**. If the same arm rendered twice already differs by 6.7 % of its own mask, **the instrument's noise floor exceeds the effect it is built to detect** — every recolour comparison on this pack is uninterpretable, and it would come back **green-looking**. This is exactly the tranche-1 method-defect class (*"a control must control everything that moves"*) arriving from inside a vendor asset instead of from the animation clock.

### The decision rule — PRE-REGISTERED, binary, and it is not yours to soften

Run the **self-identity determinism probe** first: **three renders of one identical arm, fx-on, no parameter change, both stages.**

| Outcome | Ruling |
|---|---|
| ⚑ **Diff = 0 at the STRICTEST screen, across all three passes: ZERO differing pixels at the `px ≥ 4` threshold AND `maxdiff = 0`** — i.e. **byte-identity of the fx arm.** *(Gate-1 M2, folded 2026-08-25: the earlier wording — "exactly 0 lit px" — did not name its OPERATOR, and your own instrument reports three numbers on the same comparison (`maxdiff` 214, `px ≥ 12` = 2,680, `px ≥ 4` = 6,972). A pack could return 0 at `≥12` and drift at `≥4` — a plausible number arriving through the SCREEN instead of the asset, which is the exact shape § 0 exists to stop. #64: a field whose name does not determine its referent declares it at the site.)* **This bar is not invented: the matched CONTROL frames on this same rig were ALREADY byte-identical** (`drax/notes/2026-08-24-s2b-mint-note.md:1127-1142`) — **zero is a demonstrated property of this instrument, not an aspiration.** ⚑ **Report all three figures (`maxdiff`, `px ≥ 12`, `px ≥ 4`) on EVERY pass regardless of verdict** — both screens, exact-bound and by-value. | **PACK CLEARED FOR CAPTURING.** Proceed to rows. **Record the receipt.** |
| **Any non-zero diff, at any magnitude** | **PACK DEMOTED TO LOADING-ONLY.** **Author native** for the beam body / travelling payload. The pack may be used as **visual reference and non-scored dressing ONLY** — never as a measured surface. |

⚠ **There is no third branch, and specifically: "small enough to ignore" is not a branch.** A drifting payload does not fail *loudly*; it produces a plausible number. **That is the whole hazard class this wave has now hit five times.**

⚑ **The legal escape hatch, pre-registered so a future lap does not have to re-argue this** *(Gate-1)*: **a third branch becomes admissible ONLY when a bar is DERIVED in `#80 cl. 2(a)`'s construction** — `bar := floor_mean + k·floor_sd` over the **inert/negative frames on the region actually scored**, with **`k` fixed a priori**. **Never as a literal, and never after seeing the probe's number.** Nobody has computed that construction on this pack, so today a third branch could only *be* a literal — which is the thing #80 cl. 2 convicts.

⚠ **The pin attempt is legitimate and is the FIRST thing to try** — if the 2 `GPUParticles3D` can be put on the stage clock the way you fixed the rig/mob `AnimationPlayer` drift at tranche 1, the pack may well clear. **Try it. But the probe adjudicates, not the attempt.** A pin that "should work" and a diff of 0 are different facts.

⚠ **The 7 `shader?` UNKNOWN materials are a SECOND, independent question and must not be laundered by a clean determinism probe.** Determinism says the render repeats; it does **not** say the shader responds to a tint parameter. **For any row scoring a Tier-1 claim on a pack shader, state how the tint enters that shader — or the row's Tier-1 criterion is `UNEVALUABLE`, not PASS** (#80 cl. 2(a); the emptiness-sweep shape applied to a parameter path instead of a pixel region).

### Cost gate

- [ ] **If the fork lands on AUTHOR-NATIVE, HALT and surface to knight-rider before authoring.** Native beam authoring across five rows is a materially different cost class from pack selection, and **it may re-open the 3A/3B split** (I would rather re-sequence than have you absorb a scope change silently). **This is a cheap circuit-breaker and I would rather pay it than not.**
- [ ] ⚑ **DO NOT REBUILD THE UID CACHE** (C-7's actual hazard — the pack resolves **only** via `uid://` because its internal resource paths point at the `.gdignore`d nested tree). RT-5 verified the cache byte-identical before/after its probe; **hold that property.** This binds **even if** the fork demotes the pack — a broken cache breaks more than these five rows.

---

## Required reading

**Identical to 3A's list** (`dispatches/2026-08-25-drax-s2c-mint-tranche-3a.md` § Required reading) — **read it there, do not re-derive** — with these row substitutions and one addition:

- **Your five rows: § 3.1.14 · § 3.1.18 · § 3.1.20 · § 3.1.21 · § 3.1.24**
- **ADD:** `drax/notes/2026-08-24-rt5-beam-vfx-preflight.md` — **RT-5 returned `LOADS`**: 18/19 pack scenes load and instantiate clean; the single failure is the vendor showcase scene, which **no T-A row consumes**. The C-7 *mechanism* was measured and is not the one that is live. **RT-5 is necessary and NOT sufficient — § 0 is the sufficiency test.**

**3A's ⚑ OBJECT LAW section binds here too.** Read it. It is why the criteria below name artifacts rather than judgements.

**Quarantine status, P0-b constraints (C-1 · C-2 · C-3 · C-4 · C-5 · C-7 · C-8), Math-before-code, and the ten standing pre-flight checks: all carried VERBATIM from `agentic_orchestration/dispatches/2026-08-25-drax-s2c-mint-tranche-3a.md`** *(full path repeated here per Gate-1 I4, because THIS is where those constraints actually bind)*. ⚑ **3A is the SINGLE TEXT: if 3A is amended, 3B inherits the amendment.** They are law for every remaining row in the wave and re-stating them here would only create two texts that can drift apart. **C-2 is live on every row in this dispatch** — this is the tranche where it binds hardest.

---

## Scope — the five rows

### ⚑ R-1 — `beam_channel` (§ 3.1.14) — 23 skills / 21 kits · `hybrid` · ⚠ **P-BEAM GATES THIS ROW HARDEST**

- [ ] Mint: caster-to-target **sustained** beam · primitive `line` · layers — **(a) beam body, (b) origin flare, (c) PERSISTENT CONTACT MARKER ON THE TARGET** (burn + smoke that survives on the body).
- [ ] ⚑ **C-2 IS MANDATORY AND EXPLICIT ON THIS ROW — the spec states it as a contract, not a preference:** beam-class assets are authored along **−Z**; *"mounted at identity in front of a camera looking down that axis, a beam is photographed **END-ON** and reads as a **BLOB**."* **T-A requires an explicit aim-vector → yaw contract on this row — never a default transform.** **Assert realized yaw against the aim vector in `gate.json`. Capture at ≥ 3 distinct aim vectors.**
- [ ] **L-19 `hybrid` — magical body, PHYSICAL CONSEQUENCE. The persistent contact marker is the discriminator over the alternatives:** *the beam leaves a mark on the thing it touched.* **Build the marker and measure its persistence past beam-off.** Without it the row is an aura pointed sideways.
- [ ] ⚑ **THIS IS THE ONE ARCHETYPE IN T-A WITH A *MEASURED* PARAMETERIZABILITY RECEIPT rather than an argued one** — the identical beam geometry survives two radically different MTX treatments **inside this same corpus** (`Stygian` black-flame and `Shaper` celestial-white). **Identity lives in GEOMETRY, not texture. `P = 5` is earned, not asserted.** Tint body + flare + contact marker; **motif-swap the beam's internal texture freely.**
  ⚠ **And that receipt is exactly what P-BEAM protects.** A geometric-invariance claim measured on a payload that differs from itself by 6.7 % is not a receipt. **If § 0 demoted the pack, this row's Tier-1 claim must be re-earned on the native asset — do not carry the pack's receipt across to it.**
- [ ] **Lifecycle `sustained` — THE DEFINING PROPERTY**, and the axis L-29(4) separates this row from `line` (already minted, tranche 2, whose class is `travelling burst`). **C-4 measured the class spread at > 5×; two lifecycle classes cannot share one VFX selection.** ⚑ **Cross-row check against the minted `line`: prove the pair separates on lifecycle, not on colour.**
- [ ] **Third-highest element-commitment in the referent corpus (57 %).** Tier-1 `PAYLOAD-CARRIED`. Coverage windup/active/impact **Y**.

### ⚑ R-2 — `chain` (§ 3.1.18) — 17 skills / 16 kits · `magical-cause`

- [ ] Mint: **hop-to-hop DISCRETE segments** · primitive `line` · **orientation contract applies PER SEGMENT (C-2)** · layers — **(a) the inter-target segment, (b) ENDPOINT FLASHES that preserve the hop rhythm.**
- [ ] ⚑ **R-1/R-2 IS THE DISTINCTNESS PAIR, AND THE SPEC STATES THE FAILURE IN ONE LINE: *"If a minted chain reads as a sustained beam, the archetype has been lost."*** **Hop-discreteness is the archetype's WHOLE identity** (`motion = chain_hop`) and the canonical is the **only** candidate whose notes record *"endpoint flashes preserving the hop rhythm rather than reading as one continuous sweep."*
  **The object:** a **paired capture with R-1 at identical camera**, plus a **per-frame authored-pixel timeline along the target chain** — `chain` must show **discrete on/off per hop**; `beam_channel` must show **continuous presence**. **Put both timelines in one `gate.json` record.** *"They are distinguishable"* is a routing statement.
- [ ] ⚑ **THE DESIGN WARNING SPECIFIC TO THIS ROW, and it is where Tier-1 buys the most in all of T-A:** `chain` is the **MOST element-committed archetype in the referent corpus — 94 % of members carry an explicit per-skill element, 12 of 17 lightning** (§ 4.2.3). **Tier-1 must ship the FULL live slot set for this archetype or it will read as "the lightning one," and a water or shadow chain will feel like a mistake rather than a variant.** **This is the row where skipping Tier-1 is most visible. Do not ship a partial slot set here.**
- [ ] **Confound register:** ⚠ **no non-PoE tie existed** — the single non-PoE option (Torchlight: Infinite) is `full_lifecycle = 0` and explicitly noisy, **so C-1 had nothing to break. Concentration RECORDED, not laundered.** Link bot-blocked — **not absence.**
- [ ] **Tier-1 `PAYLOAD-CARRIED`.** Lifecycle `burst` (hop rhythm). Coverage windup/active/impact **Y**.

### R-3 — `placed_lane` (§ 3.1.20) — 9 skills / 9 kits · `physical-cause`

- [ ] Mint: world-placed lane with vertical extent · primitive `line` · **C-2 applies** · layers — **(a) a bright base along the lane, (b) darker upper wisps, (c) BRIGHT END PILLARS.**
- [ ] ⚑ **THE T-A AUTHORING CONSTRAINT — contributed by the judge, binding regardless of which reference you open: at our locked camera, ANY lane with vertical extent must be authored NON-OPAQUE.** The runner-up's pattern is the target — *bright base, darker upper wisps, not a completely opaque screen* — and **C-5's 67 % occlusion ceiling is the reason. An opaque lane at this camera DELETES THE FIGHT BEHIND IT.** **Measure peak occlusion against the ceiling and put it in `gate.json`.**
- [ ] ⚑ **ENDPOINT LEGIBILITY IS *THE* HARD READABILITY PROBLEM for a lane at a fixed isometric camera — *where does the wall stop?* — and this canonical is the ONLY candidate that solves it explicitly** (*"bright end pillars"*). **The pillars are the selection reason. Build them and measure endpoint contrast**, or the row has lost what it was picked for.
- [ ] **Tier-1: `FIELD-CARRIED` at the lane body, `PAYLOAD-CARRIED` at the end pillars. Tint both; DO NOT RAISE OPACITY.** (The two clauses interlock: opacity is the one property this row cannot spend.)
- [ ] **C-7 beam-pack fragility applies — § 0 governs.** Lifecycle `sustained` (placed, persistent). Coverage windup/active/impact **Y**.

### R-4 — `ricochet_bounce` (§ 3.1.21) — 9 skills / 8 kits · `physical-cause`

- [ ] Mint: multi-segment travelling path **with a RETURN LEG** · primitive `line` · layers — **(a) payload body, (b) per-leg trail, (c) per-bounce contact response.**
- [ ] ⚑ **THE COMPLETE RETURN LEG IS THE SELECTION REASON: *"a ricochet that does not come back is a `multi_projectile` with extra steps."*** `multi_projectile` is **already minted** (tranche 2). **Cross-row check: prove the return leg is what separates them, and measure it** — path-segment count and the terminal leg's direction reversal, in `gate.json`.
- [ ] ⚠ **`R = 4` docked — Manifest Armour procs can mask contacts** in the general footage. `class=frame-external`, **nameable and discountable**: the final training-dummy segment is the reference **precisely because it deliberately exposes the individual path legs** with the procs out of the way. ⚠ **`t_start` is END-RELATIVE, not absolute** — the dossier locates the isolated three-ricochet demonstration in the **FINAL ~5 SECONDS** of the clip. **Do not read an absolute timestamp into it.**
- [ ] **The training-dummy segment is the best authoring reference in the corpus for a multi-segment path.** Use it.
- [ ] **Tier-1 `TRAIL-BOUNDED`: motif-swap the thrown body, tint the leg trails. LEG COUNT and BOUNCE RANGE are ENGINE parameters** — varying them demonstrates the wrong axis. Lifecycle `burst` (multi-leg). **Both finalists are non-PoE, so C-1 is satisfied either way.**

### R-5 — `fork` (§ 3.1.24) — 5 skills / 5 kits · `physical-cause`

- [ ] Mint: forward-biased split · primitive `line` · layers — **(a) the parent payload, (b) THE BRANCH POINT, (c) the child payloads.**
- [ ] ⚑ **THE BRANCH POINT IS THE ARCHETYPE'S IDENTITY: *"if a minted fork's split is not legible, it is a `multi_projectile`."*** — which is **already minted**. **Cross-row check with R-4 and the minted `multi_projectile`: three archetypes in this family separate on *where the payloads come from*** (one origin fanning / one body splitting mid-flight / one body bouncing and returning). **Measure branch-point legibility explicitly** — authored-pixel density at the split versus along the child legs.
- [ ] **Cite the runner-up (PoE Celestial Tornado Shot) for the BRANCH-POINT AUTHORING SPECIFICALLY** — it carries the cleanest split-NODE read.
- [ ] ⚠ **`R = 4` docked — rapid fire obscures the branch points. ISOLATED CASTS ARE THE REFERENCE FRAMES**, not the sustained-fire segments. *(Same contamination shape as tranche 2's Javelin `t_end` — and it bit in both directions there.)*
- [ ] **Tier-1 `PAYLOAD-CARRIED` — second-most element-committed archetype in the referent corpus (80 %). Tier-1 buys a lot here.** L-19: *a solid arrow shattering into arrows is a plausible physical manifestation*; forward bias is correct for `prim = line`. Lifecycle `burst`.

---

## Acceptance criteria

- [ ] ⚑ **§ 0 P-BEAM resolved FIRST**, with the three-pass self-identity probe receipt filed and the fork ruling recorded **before any row capture**. **A demotion to author-native HALTS to knight-rider before authoring.**
- [ ] **All five rows minted**, "must NOT" clauses **measured, not asserted**.
- [ ] **C-2 asserted on every row**: realized yaw vs aim vector in `gate.json`, **captured at ≥ 3 distinct aim vectors.** *(Per segment on `chain`.)*
- [ ] **E-1 fx-off control arms on every row × every stage; `00-pre`/`08-post` diff exactly 0.**
- [ ] **E-0 two-stage law; per-stage cohorts never pooled; stage-adequacy reported.**
- [ ] **Both screens — exact-bound AND by-value — on every criterion.**
- [ ] **`authored ∩ region` emptiness sweep as PRE-FLIGHT across all five rows**; disjoint regions return **UNEVALUABLE, never PASS.**
- [ ] ⚑ **Any Tier-1 claim resting on a pack `ShaderMaterial` states how the tint enters that shader, or returns `UNEVALUABLE`.**
- [ ] **C-8 emitter census at every mark, both stages**, `fx` + `rt` in the declaration key.
- [ ] **Four cross-row separation records** in `gate.json`, each with its object named: **R-1↔R-2** (continuity timeline), **R-1↔ minted `line`** (lifecycle), **R-4↔ minted `multi_projectile`** (return leg), **R-5↔ minted `multi_projectile`** (branch point).
- [ ] **`placed_lane` peak occlusion vs the 67 % ceiling; endpoint-pillar contrast.**
- [ ] ⚑ **`chain` ships the live element slot set — DERIVED, then shipped against** *(Gate-1 W4: "the FULL set" is an UNBOUNDED PREDICATE per #76 cl. 1 — "full" is unauditable unless the set is derived)*. **Derive the live slot set from the named artifact, report the derived set WITH its source, then ship against that derived set.** The 94 %-commitment figure is what makes this the row where the set must be complete; it is not what defines the set.
- [ ] **Mint note committed BEFORE the first effect node exists**; RESULTS appended after.
- [ ] **Confound-register delta in both directions**, routed to gandalf via the mint note, **spec not patched.**
- [ ] **UID cache byte-identical before/after** — verify and report.
- [ ] **Tag:** `drax/v0.1-s2c-mint-tranche-3b`. **Commit auto-fires. DO NOT PUSH** — 3A's push clause applies verbatim.

---

## Quality criterion

**Game-quality goal this dispatch serves:** **that five line-shaped archetypes do not collapse into one line-shaped archetype.** Every row here is primitive `line` or line-derived; four of the five must be told apart from something already minted. The player-facing question is whether a beam, a chain, a wall, a ricochet and a fork read as **five different decisions** at the gameplay camera — or as *"a glowing line happened"* five times. **That is `single_target`-vs-`line` (tranche 2's load-bearing boundary) at five-way scale, and it is why they are one dispatch.**

**Refutation conditions** (surface to knight-rider — **do not absorb**):

- ⚑ **P-BEAM's probe returns non-zero and the temptation is to call it small.** It is not small; it is 6.7 % against a Tier-1 claim that is a difference measurement. **Surface it.**
- Acceptance criteria can pass without advancing the quality goal — e.g. all five minted, none proven distinct from its neighbour.
- An alternative execution serves five-way distinctness better than the one specified.
- This dispatch contradicts a canonical anchor.
- The dispatch pre-commits to a decision Matt has not ratified, or introduces an undeclared scaffold (#40) or pre-authored taxonomy (#41).
- **A row's spec-asserted Tier-1 axis proves wrong in authoring** — surface it; a silent re-classification is the defect.

---

## Out of scope

- ❌ **The eight 3A rows** — separate dispatch, fires independently.
- ❌ **`whirlwind`** — WW-AB clean-room, separate session, quarantine binding.
- ❌ **Re-minting `line`, `multi_projectile`, or any tranche-1/2 row.** They are **comparison objects here, not build targets.**
- ❌ **A UID-cache rebuild.** Binding even if § 0 demotes the pack.
- ❌ **Any engine edit.** Not your seam.
- ❌ **Sealed spec § 5 / L-36 / L-37 / Tier-2 law** — HALT signal.
- ❌ **Patching the sealed spec** — route to gandalf via the mint note.

---

## ⛑ Concurrency posture *(Gate-1 M3, folded 2026-08-25 — identical text in 3A)*

**3A and 3B may run serially in one session or in parallel sessions.** Both auto-commit and tag the **same `reincarnated-godot` tree**, and the WW-AB clean-room session may be live in it as well — **three sessions, one working tree.**

If parallel — or if the WW-AB session is live in this tree — **#62(a) binds:**

- **Stage by explicit pathspec. Never `git add -A` or `git add .`**
- **Verify `git diff --cached --name-status` against the paths you named, before every commit**
- **Tag only commits whose full contents you authored**

⚠ **A tag that carries a sibling session's work — committed or uncommitted — is a DEFECTIVE SEAL even when every file in it is correct.** The seal's claim is not "these files are good"; it is "this is what I made." Also: the WW-AB quarantine is only a quarantine if it does not arrive as a staged file.

---

## Push clause — READ IT, IT OVERRIDES THE STANDING PATTERN

⚑ **DO NOT PUSH `reincarnated-godot`. Commit only.**

*(Added 2026-08-25 after Gate-1. **This section was MISSING from 3B entirely** — 3A carried it and 3B did not, while both mint to the same repo. That is precisely the two-sessions-opposite-instructions-on-one-repo shape the CLAUDE.md conflict rule was written to close, and it was one dispatch away from firing again. Recording the omission rather than quietly patching it: a silent fix teaches nobody.)*

The standing *"push as you go"* pattern covers **`reincarnated-collaboration` + `reincarnated-engine` ONLY**. `reincarnated-godot` is **outside** it by the pattern's own scope boundary, and Matt's launch prompt left the extension question **unfilled** (`[Matt — pick one: (a) … / (b) …]`). **An unfilled bracket is not a choice, so the conservative default holds: fresh ask at seal.**

**Per the CLAUDE.md conflict rule, the per-dispatch push clause GOVERNS over any standing workstream pattern.** This clause is the narrower and more recent instruction. **It wins.** The posture is recorded in the wave record, not only here.

Knight-rider requests the push at seal time. **If you believe a push is needed, HALT and ask — do not resolve it yourself in either direction.**

---

## References

Identical to 3A's reference list, **plus** `drax/notes/2026-08-24-rt5-beam-vfx-preflight.md` and `drax/notes/2026-08-24-s2b-mint-note.md:1127-1142` (the P-BEAM evidence).

---

## Gate record

**Gate 1 (jack-ryan, DESIGN-MODE):** *pending — see appended record before firing.*

## Completion record

*(drax appends here — **and updates the Status header**, per the CLAUDE.md conflict rule.)*

---

## ⚑ GATE 1 — jack-ryan, 2026-08-25 — **PASS-WITH-FINDINGS. CLEARED TO FIRE.**

Four mandatory edits (documentation-only, approved directly under ADR-002 — fold and go, no second round), four advisories, five INFO. **All folded before this dispatch was fired; each fold is marked in place with its finding ID.**

**M1** — 3A's "zero beam-pack dependency" was asserted as an *observation*; it is now enforced as a **CONSTRAINT** in Out-of-scope. It is the premise the 8/5 split rests on.
**M2** — 3B § 0's "diff = exactly 0 lit px" named no **operator**; now byte-identity at the strictest screen (`px ≥ 4` AND `maxdiff = 0`), all three figures reported every pass.
**M3** — neither dispatch stated a **concurrency posture** while three sessions can touch one `reincarnated-godot` tree; #62(a) now binds explicitly in both.
**M4** — 3A's MP4 criterion was satisfiable by four clips that show nothing; the numeric series is now **part of the same deliverable**.

**Verified at source by jack-ryan** (so silence elsewhere is not read as ratification, #80 cl. 3(a)): every spec §-heading incl. T2/T3 tier stamps and every skill/kit count in both dispatches; `f119bd8` and `45a0dc15` both on `origin`; the P-BEAM figures; the tranche-2 Row-4/Row-7 clause verbatim; #76 cl. 2, #79, #80 cl. 1/2(a); WARN-1's true home. **NOT checked:** galadriel gate-procedure section numbers, charter L-ruling numbers, § 4.2.3 element-commitment percentages.

**The four conductor rulings: three ratified as authored, one ratified with a correction that runs in the conductor's favour.**

- **8+5 split — SOUND, and it stands on the spec rather than on precedent.** The tier stamps were re-derived independently: `dash_attack` § 3.1.11 **T2** / `blink` § 3.1.15 **T3**; `beam_channel` § 3.1.14 **T2** / `chain` § 3.1.18 **T3**. A tier split *does* separate both pairs — a fact about the spec, not a preference. The tranche-2 clause is corroboration that could be deleted without weakening the argument.
- **RT-6 / `vortex_pull` — CORRECT, and the lane finding cuts FOR the ruling, not against it.** Ground was conceded that did not need conceding: the kinematics conflict lives in the *player-directed* lane, and X-2 is player→monster. **Precedent is the only live hazard — which is exactly what was named.** Refusing to set engine law is inside conductor scope in a way that setting it is not; ruling the other way would have been the ADR-002 escalation. *(The one defect — "routed as its own decision" routing nowhere — is fixed: the destination is now named at R-8.)*
- **Object-law carry — LEGITIMATE, and NOT the #77 shape.** The discriminator: #79's harm is a *number* asserted without a referent, laundering through hops. Here the file and path were named, the operative text quoted, the status disclosed as an unratified candidate filed against the author's own dispatch — **and each of the four MP4s is independently derived from its own row's spec criterion.** The candidate is motivation; the spec is authority. ⚑ **jack-ryan is explicitly NOT ruling on either candidate here** — Gate-1 finds the *use* legitimate; the candidates stay live at `qa/pending/`, read unchanged as **#2 above #1**, and neither ships as a number until filed.
- **P-BEAM binary — RIGHT, and better-founded than it was argued.** It was framed as a threshold nobody derived. **It is not: zero is the MEASURED property of the control arm on this same rig**, so the rule asks the pack to do what the harness already demonstrably does.

**Standing Gate-2 pre-declaration:** every `file:line` and clause citation in the mint note will be spot-derived (#79 standing effect), and **the four MP4-plus-series pairs are the first thing opened.**

**Knight-rider's own fold-in beyond Gate-1:** 3B was found to have **no push clause at all** while 3A had one, both minting to the same repo. Added, with the omission recorded rather than silently patched.
