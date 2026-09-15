# Finding — 2026-09-15 — VFX workflow architecture (Gate-1, pre-fire)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Severity:** **BLOCK** — on *chartering a run against this document as written*. Not on the design.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-15-vfx-workflow-architecture/03-architecture.md` v2.3 (PROPOSAL, 173 lines), and the Q79 packet that carries it
**Author under review:** gandalf (ARCHITECT / SPEC-AUTHOR)
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 4 (decisions-log as truth) · 5 (severity matters)
**Disciplines cited:** #1, #41, #73, #75 cl. 2, #75 cl. 6, #80 · **ADR-002** (tiered approval), **ADR-004** (cross-seam handoff), **ADR-006** (read-only default)

---

## 0. Verdict in one paragraph

The re-scope Matt ordered was executed cleanly: the generator coupling is genuinely gone (four residues, all cosmetic or declared, § W-1), the five treatments are derived from the six skills rather than from the emitted corpus, and E0 as a £0 falsification-first step is the correct application of Principle 2. The Astra red-team fold is thorough — 28 ⟲ marks, none decorative, and all four of Astra's "omitted rulings Matt needs" were promoted to forks. **The architecture is good. The instrument it is measured by, the ledger it is filed against, and the arithmetic of its gates are not.** Six BLOCKs follow. Every one has a cheap path forward and none of them is a design objection. The single sentence that summarises all six: **this document is an architecture presented in the costume of a charter, and it is measured by instruments that do not exist or that document their own inability to perform the measurement.**

---

## 1. BLOCK findings

### BLOCK-1 — There is no charter, and the run this would extend is HALTED with my own BLOCK undisposed

**What I found.** `03-` names no run, no ledger, no image budget, no HALT taxonomy and no FAIL predicate. The C-3 charter's entire VFX scope is, verbatim, *"one frost bolt on the cast"*; its § 0 exit predicate was declared met at **R-C3-21** (2026-09-13T04:34); everything after **R-C3-22** ran charter-less on direct Matt instruction, the narrowest of which is *"Ok, a small balance was added. Go ahead and see if you can complete the matrix."* The run's `halts[]` still carries **H-C3-2** — my own Gate-2 BLOCK — with status *"Q78(a) explicit ruling still owed at C-4."* The queue row still reads *"Rule (a) FIRST, before any cell is judged."* No C-4 session has occurred. Matt's own instruction at **R-C3-123(4)** was to *"check everything is canonized, write a SESSION HAND-OFF doc, and plan the basic concept of the VFX session to begin afterwards in fresh context"* — there is no 2026-09-15 hand-off doc; the most recent is 2026-09-12.

Simultaneously, `mechanical-process.md § 1` invariant 6 makes **"any medium or bar change" a HALT-to-Matt condition**, and `03-` § 0 sets roughly ten bars wholesale (field boundary ≤ 10 %, aura attachment ≤ 1 px, four-cast white ≤ 2 %, matte halo ≤ 1 px, +2 ms p95, ±15 % deformation, ~12 assets/treatment, extents ±10 %, pivots ≤ 1 px, residue 15–25 %) under a blanket "proposed project gate" stamp.

**Rationale.** This is the *same* failure family as H-C3-2, which gandalf conceded at **R-C3-22** in his own words: *"my resource-vs-integrity distinction was an in-run reinterpretation of a rule the run does not own — exactly the 'the run decides' failure § 8 forbids."* Discipline #73: the state changed and the record did not follow. A third workstream opened on a halted ledger whose BLOCK is undischarged compounds it.

**Action.**
- [ ] gandalf: charter **Run C-5 (VFX)** on the C-3 charter's shape — § 1 authority table, § 3 forks-ruled (= Q79's answers), § 4 phase sequence (= § 6), § 5 tooling rows with acceptance clauses **that can go RED** (my #80 action from the 2026-09-13 Gate-2, still open), § 8 HALT list **restated verbatim** from `mechanical-process.md § 1.6`, its own `runs/C-5/ledger.json` and image budget.
- [ ] gandalf: write the R-C3-123(4) session hand-off doc.
- [ ] **Matt:** dispose Q78(a) before C-5 opens. An escalation that dies by supersession rather than by ruling is the defect the CLAUDE.md conflict-rule corollary was written to close.

---

### BLOCK-2 — The pre-registered gates are not decidable as written

This is Principle 1 / Discipline #1, and it is the finding the brief asked me to test hardest. Four sub-items; each is a one-line fix and each currently makes a gate un-adjudicable at the moment of ruling.

**(a) `strike_fast_v1` has no declared clock, and § 2.2b contradicts itself inside one bullet list.** The band is *"peak 0–1 frames, half in 2–7 frames, residue 0.3–1.0 s."* § 2.2b states, of the onset, *"the 0–1-frame onset (a runtime flash — **24 fps cannot represent 17 ms**)"* — 17 ms is 1/60 s, so a frame is 16.7 ms. Three clauses earlier the same section states *"2–7 strike frames = **80–300 ms**"* — which requires a frame of 40–43 ms, i.e. ~24 fps. Both statements are in § 2.2b. Arithmetic:

| frame = | 0–1 frames | 2–7 frames | E1's "half-peak ~4 ticks" |
|---|---|---|---|
| 1/60 s | 0–17 ms | **33–117 ms** | 67 ms |
| 1/24 s | 0–42 ms | **83–292 ms** | 167 ms |

§ 3 step 7 mandates validation *"at 60 Hz"*, which points at row 1. Row 1 makes § 2.2b's own video-fallback kill criterion #4 wrong in the direction that matters: at 24 fps a 33–117 ms decay is **0.8–2.8 video frames**, not the "2–7 video frames: marginal" the document argues from. E0-p's headline oracle gate ("half in 2–7 frames") and the fallback's feasibility argument both ride on an undeclared number.

**(b) The ≤ 2 % white gate has no denominator and no temporal rule — a 30× swing.** § 4 gates *"≤ 2 % of the crop at four simultaneous casts"*; "the crop" is defined nowhere in the document. Taking the fixture's own numbers (Keeper 130 screen px = 12.5 % of height ⇒ 1040 px tall; impact envelope 3 BH = 390 screen px):

- flash envelope area ≈ 119,459 screen px² ≈ **6.2 % of a 1848×1040 frame** — one cast, peak frame, already 3× over the gate;
- the same 0.1 s flash as a **clip-mean over a 3 s capture** ≈ **0.21 %** — ten times under the gate.

The same effect passes or fails by a factor of thirty depending on whether the gate is read peak-frame or clip-mean, and the document never says which. E1 compounds it: § 4 says *"four simultaneous"*, E1 says only *"four-cast white ≤ 2 %"* while the fixture mandates **both** synchronised and staggered casts.

**(c) The white predicate is background-dependent, which makes the gate non-comparable across the two mandated backgrounds.** `V > 0.95 ∧ S < 0.20` over the existing kit's flash (`alpha 0.55`) composited on saturated ochre dirt lands near V ≈ 0.82, S ≈ 0.22 — **below V and above S**, so the flash is invisible to the metric on dirt and counted on grey rock. § 4's ⟲ already caught half of this (report total / baseline / attributable separately) and then still states the gate as a single number, with the fallback *"if the clean background itself exceeds 2 % rule a separate attributable-VFX budget"* — i.e. the threshold is conditional on a quantity nobody has measured. **A gate whose threshold is determined after the experiment is not pre-registered.**

**(d) Unit drift, and an unstated comparand.** § 2.3 and § 2.2b say *"1 **native** px"*; E1's gate list says *"matte halo ≤ 1 px"*. At the project's live `pixel_scale = 3` (verified in `astra_test_01/burst/runs/C-3/vfx_kits/frozen_orb_v3/kit.json`) that is a **3× difference**. Separately, *"extents ±10 %"* never states whether the comparand is arm A vs arm B or asset vs spec, nor the alpha threshold at which an extent bbox is taken — and on a soft-edged burst the bbox moves substantially with that threshold.

**Action.**
- [ ] gandalf: declare the clock once (`strike_fast_v1` frames = 1/60 s or 1/24 s) and re-derive § 2.2b kill #4.
- [ ] gandalf: define the crop (pixels, origin), state peak-frame vs clip-mean, and state synchronised vs staggered for every white measurement.
- [ ] gandalf: **measure baseline white on the E0 fixture crop, both backgrounds, as a prerequisite**, then state the gate as attributable-VFX white with the baseline recorded — not as a conditional.
- [ ] gandalf: spell "native" on every px tolerance; define extent = bbox of the coverage mask at a stated alpha.

---

### BLOCK-3 — The scale contract is a function of `pixel_scale`, and V2 is sequenced after the spend it governs

**What I found.** § 2.3 states the contract as fact: *"Keeper = 130 screen px = 1 BH; effect art step **3 screen px** (Matt rules it in motion at E1); 64 native px ≈ 1.5 BH; a 3–6 BH burst = 130–260 native px."* Those figures are not independent — they are consequences of `pixel_scale = 3`, which is a live field in the shipped kit. Recomputed:

| `pixel_scale` | 1 BH | 3–6 BH | 64 native px |
|---|---|---|---|
| 2 | 65.0 native px | 195–390 native px | 0.98 BH |
| **3** | **43.3 native px** | **130–260 native px** ✓ | **1.48 BH** ✓ |
| 4 | 32.5 native px | 98–195 native px | 1.97 BH |

Only row 3 matches the document. **V2 asks Matt to choose between 2, 3 and 4 screen px.** Ruling 2 or 4 silently invalidates every native-px figure in § 2.3 and the entire build list — and § 2.3 sequences that ruling *"in motion at E1"*, i.e. **after E1's eight images have been painted at an assumed step.** The art step is not a finish for a decision; it is its premise.

**Related and equally arithmetic:** the build list gives **canvas** sizes (P01 head 128², P03 field body 256², P07 wedge 128²) while the spec gives **extents** in BH, and nothing binds them. § 3 step 6 forbids trimming (*"no trimming initially"*). At `pixel_scale 3`, E1's 1.2 BH body against a 128² canvas is a **0.41× non-integer downscale**; P03 at 3 BH is 0.51×; P07 at 1 BH is 0.34×. A non-integer downscale of a native-grid painting is precisely what destroys the art step. If the intent is that painted content occupies part of a padded canvas at 1:1, that is coherent — and it is stated nowhere, and a model asked for "a head, 128²" will fill the canvas. **This is F3's mechanism — *"size off a 256-px cell"* — reproduced by the document that diagnoses F3.**

E0-p compounds it a third time: step 3 flies pieces on *"per-piece velocity / rotation / **scale-down curves**"* and ends at *"residue fragments at 15–25 % of peak area"*, while § 5 retires `phase_scale` and § 4 makes *"> ±15 % deformation of a reusable primitive"* a tripwire. 15–25 % of peak area is a 0.39–0.50× linear scale if achieved by scaling — which trips § 4 on every burst — and is fine if achieved by erosion. The document does not say which, so the tripwire cannot be adjudicated.

**Action.**
- [ ] gandalf: **move the art-step ruling to E0**, where it is £0 — the project already owns sheets to test it on (`runs/C-3/vfx_kits/frozen_orb_v3/`). Or state plainly that E1 runs provisionally at 3 px and that a different ruling re-authors E1's eight images.
- [ ] gandalf: restate § 2.3's native-px figures **as a function of `pixel_scale`**, so V2 cannot be answered into an inconsistent contract.
- [ ] gandalf: declare, per primitive, the **painted extent in native px** separately from the canvas size.
- [ ] gandalf: state whether E0-p's residue is reached by erosion (allowed) or by scale (trips § 4), and quantise any piece scaling to integer native steps.

---

### BLOCK-4 — § 4's coherence QA is specified against an instrument that documents its own inability to perform it

**What I found.** The oracle `03-` means is `astra_test_01/burst/oracle/vfx_measure.py` — `measure(frames_dir, fps_or_durations, body_h_px=130, plate='alpha')`, returning O1/O2/O3/O4/O5/O6/O8/O10 against `oracle/vfx_reference_hades.json`. Its own docstring says, verbatim: **"A gameplay crop is not a black plate"** and **"RGB plate: unavailable."** § 4 asks it for exactly that. Specifically:

| § 4 asks for | Instrument status |
|---|---|
| attributable white over live dirt and foliage | explicitly out of contract; needs a clean-plate differencing path that does not exist |
| *"the oracle consuming **runtime coverage masks**"* | `measure()` has no coverage-mask or primitive-ID input. § 2.3's capture contract *produces* these masks; **nothing consumes them** |
| field boundary ≤ 10 %; activation/expiry **within one tick**; aura attachment ≤ 1 native px, no drift; calm-loop area modulation ≤ 15 % | none implemented; tick-accurate activation and attachment drift need **runtime event traces**, not frame sequences — a different instrument class |
| `field_v1` / `aura_loop_v1` bands | do not exist; reference file is **strike only**. `03-` concedes this and assigns it to *"their own lap"* — no owner, no lap |
| G1 projectile speed (O7), layer-stack budget (O9) | defined in the Legolas findings, **not implemented** |
| E0-p's O1/O3/O8 on a burst | implemented and correct — but `measure()` takes `plate='alpha'`, so the burst must first be Movie-Maker-baked with `transparent_bg`. § 2.2b step 3 does not state that dependency. Separately the **O3 band is stale**: R-C3-118's style card v0.2 replaced "white core" with "palest band," and V6 makes bodies white-free |

**Rationale.** This project's own standing law, restated three times in `CLAUDE.md` and once in my 2026-08-25 registry ratification (I-7): **the check running is not the check passing** — an instrument returning cleanly after it stopped answering the question. Four of § 4's gates would return a number from the wrong instrument or no number at all.

**Compounding, and a BLOCK in its own right: two live O-series with the same names.** `burst/oracles/` (canonised at `painted-2d-pipeline/00-system.md`) defines O1 = palette, O3 = motif-instance count, O8 = brush-grain band energy. The VFX oracles define O1 = phase envelope, O3 = white-core fraction, O8 = drawing-change rate. `03-` cites O1/O3/O8 **bare**. Both modules exist, both run clean, both return numbers, and a CHECK burst handed "run O1/O3/O8" reaches for the wrong one.

**Action.**
- [ ] gandalf: for each § 4 gate, name the instrument that produces it and the burst that builds it; mark the ones that do not exist as **UNBUILT** rather than as gates.
- [ ] gandalf: namespace the oracle IDs (`VO1` / `CO1`, or fully qualified) everywhere in § 2.2b and § 6.
- [ ] gandalf: state E0-p's bake dependency, and re-point the O3 gate at style card v0.2's "palest band."
- [ ] **Matt:** the `field_v1` / `aura_loop_v1` lap requires frames cut from source footage. That is the exact class with an **open** decision against it (`canonical/matt_decision_needed/2026-08-25-youtube-frame-extraction-sourcing-class.md`, alongside the Synty-licence retention item). `03-` cites neither. The deferred lap may not be an authorised lap.

---

### BLOCK-5 — The prerequisites are the entire build, they are budgeted at zero, and the seam they land on is chartered against the wrong repo

**What I found.** § 3 places four prerequisites *"outside every burst estimate"*: a reusable G1 event-driven production component, a deterministic fixture host, a pinned Godot version, and a Compatibility + browser parity lock. On disk:

- **The G1 component does not exist, and its opposite does.** `cliffside_v12/scripts/vfx_{fire,frost,holy,poison,lightning,arcane,frozen_orb}_bolt.gd` are **seven near-duplicate self-driving `Area2D` scripts**, each raycasting its own contact, hardcoding `520.0 * spell_scale` px/s and `650.0` px range, instantiating its own impact scene, freeing on a 0.4 s timer. No event interface, no effect-age clock, no material substitution, no reuse. Node census across the 16 VFX scenes: 14× `CPUParticles2D`, 16× `AnimatedSprite2D`, 16× `CanvasItemMaterial`, **0× `ShaderMaterial`**.
- **The fixture host does not exist.** `cliffside_v12/scenes/main.tscn` is a Keeper + Camera2D on a flat 20000² `Polygon2D` floor. No dummy, no real ground, no replay, no tick control, no event injection.
- **The shared `ShaderMaterial` does not exist** — and E0 is billed *"£0, no images"* while requiring it as a precondition for E0(a), E0-p step 3, § 2.2, § 2.3 and § 5. £0 is true of images; it is not true of the burst.
- **Version:** installed `4.6.3.stable.official.7d41c59c4`, no pin file.
- **Renderer:** the C-3 exports are already `gl_compatibility`. But `~/Games/reincarnated-godot/project.godot` — the repo drax's agent definition actually names — is `Forward Plus` on `sidekick_test.tscn`.

**Cross-seam charter conflict (Principle 3).** Two drax charters disagree. `.claude/agents/drax.md` + `AGENTS.md:140-157` give him `reincarnated-demo/`, `reincarnated-loadout/`, `reincarnated-godot/` (*"Forward+/Metal renderer"*) and mention `astra_test_01/` nowhere; `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md § 2` (CANON per R-C3-116/119) does charter him into this lane. The § 3 assignment is inside his **canon** charter and outside his **agent-definition** charter, and a cold `--agent drax` session reads the latter. `03-` never says which Godot project the fixture lives in — which decides whether V9's "lock Compatibility" is a no-op or a real renderer change to the repo drax owns.

**And a regeneration collision `03-` does not see.** `export/godot_import.py` (61 KB, frozen Astra TOOLING) **generates** `cliffside_*/scenes/*.tscn` and `scripts/*.gd`; that is how all 17 `cliffside_v*` trees were produced. If drax hand-authors the G1 component into that tree, the next PACK regenerates over it. § 3 correctly says *"the fixture instantiates the component"* but never says whether the component is exporter-generated (Astra) or hand-authored (drax). Two owners, one directory, regeneration routine.

**Action.**
- [ ] gandalf: price the prerequisites as a named work item with an owner and a **feasibility gate of its own** (deterministic reset-and-replay is not a given, and E0(b)'s two-bake comparison is unrunnable without it — today there is no gate that fires if it can't be achieved).
- [ ] gandalf: name the repo and the directory the fixture lives in, and rule exporter-generated vs hand-authored for the G1 component.
- [ ] knight-rider: reconcile `.claude/agents/drax.md` with `scene-builder-workflow.md § 2`. This is ADR-004 territory — a cross-seam handoff with two disagreeing charters and no MIGRATION note.
- [ ] gandalf: **the "grey room" word collision is load-bearing.** drax has built four versions of a *static terrain blockout guide for painting*. § 3 step 2's "VFX grey room" is a *moving fixture with a dummy, an aim rule and replay-to-tick* — a different artifact nobody has built. A dispatch saying "drax: build the grey room" resolves to the thing he already has.

---

### BLOCK-6 — Two ruled Matt decisions are reversed or re-disposed without citation

**(a) V6 inverts an accepted fork and presents the ruled position as the losing option.** **R-C3-90(2)**, verbatim, under "Matt accepts all VFX forks": *"effects use a **dark duplicate underlay + dark interior shapes**, optional thin stroke on bolts only - no full H1 contour."* `03-` § 2.2 demotes it to *"an **approved per-preset option**"*, turns it off in the field/aura preset, and V6 recommends *"halo + floor light default, **dark duplicate an approved exception**"* with the **ruled position listed in the Options column as the alternative** (*"dark duplicate as default (Hades)"*). The demotion's provenance is the conductor's own style-card v0.2 pass at R-C3-118 — a conductor ruling, whose only Matt-facing fork was the hybrid oracle. **A reader answering `V6 accept` would not know he is reversing himself.**

There is genuine evidence on both sides and Matt should see both: Legolas probe 1 calls the fixed layer stack *"the strongest single mechanism in the corpus"* and the dark duplicate *"the mechanism that lets an additive effect have a contour at all"* (56 of 78 dark sheets are the same sheet also drawn additive); the CoM probe measured **no dark edge on any of 6 samples**, legibility carried by halo +.16–.41 and floor light. V6 shows neither.

**(b) § 2.2 asserts a fork closed that § 7 asks open, drops Matt's procedural precondition, and collides with a second open file.** `03-` § 2.2: *"This **dissolves** the deferred 'hybrid oracle' (R-C3-118/120)."* It does not dissolve it — Hades timing bands + CoM/Slormancer legibility rules **is** the hybrid; class-scoping is a rider on option B. Meanwhile **R-C3-120** records Matt's order of operations verbatim: *"before ruling on the hybrid oracle, wants to SEE a VFX built to that spec - when one is finished, push it to Vercel to test"*, and **R-C3-123** defers it *"to the VFX session (size step first)."* `03-` carries neither. And `canonical/matt_decision_needed/2026-09-15-hybrid-vfx-oracle.md` is **STATUS: OPEN** with the opposite disposition — *"Recommendation (one): adopt the hybrid … Take the ruling **after the size/timing clips exist**"* — while the Q79 row says *"hybrid oracle DISSOLVED into class bands (closes R-C3-118/120)."* Two open Matt items, same day, same decision, incompatible words.

**Rationale.** Principle 4. The CLAUDE.md corollary is exact: *an escalation overtaken by events still requires a disposition; "resolved by supersession" is legitimate — silence is not.* Here the record says **closed**, which is worse than silence, and a downstream implementer reading § 2.2 will build against a decision Matt has not made.

**Action.**
- [ ] gandalf: quote R-C3-90(2) on V6's row and state that answering it reverses a prior acceptance; show both evidence sides.
- [ ] gandalf: change § 2.2's line from declarative to conditional; restore R-C3-120's precondition or state explicitly that it is being waived and why.
- [ ] gandalf: collapse `2026-09-15-hybrid-vfx-oracle.md` and the Q79 V4 row to **one** disposition in one file.

---

## 2. WARN findings

**WARN-1 — Generator smuggle: four residues, one of which is live.** Three are cosmetic or correctly neutralised: the name `VfxSkillSpec` (minted in 02c as a resolution layer over two emission schemas, now six hand-authored files), `response_class` (existed to absorb `effect_category`'s absence), and `corpus.db`'s 18 signatures / 27 archetypes (explicitly *"a naming reference, not a constraint"* — correct handling). **The live one is the naming seam.** 02c § 3 required `visual_treatment_id` to be kept separate from `canonical_element` because **ice and poison are not engine elements**. `03-` uses both as first-class "elements" — right for source-game skills — and neither `03-` nor `04-` records that the binding rule becomes load-bearing the moment a generator-emitted skill enters this pipeline. The five treatment names are about to be baked into asset filenames, and two of them the engine does not recognise. Park the binding rule properly in `04-`.

**WARN-2 — The generality claim is a tautology, and the tripwire that would have caught it was parked under the wrong reason.** Four grammars cover the six skills *because the six skills were drawn from four grammars*. None of the six is melee_strike, melee_arc, ground_slam, dash_attack, whirlwind or leap_strike — the 31 % of the reference corpus (356 skills) that Legolas probe 1 identified and flagged with its own warning: *"Read this result carefully — it has a trap in it."* `04-` § 5 parks *"the 'melee sweep + displacement fixture before calling it complete' requirement"* as generator coupling. **It is not generator coupling** — the six contain no melee and no displacement regardless of where their parameters come from, and attachment/deformation stress is a *runtime* claim. `03-` § 8's *"its coverage analysis is parked"* is over-broad: the emitted-411-kit curve is correctly parked; the reference-corpus curve (1,135 banded skills, 590 kits, 21 source games) touches no generator at all. E3's completion claim — *"the goal is met when the six read as one language"* — carries no coverage caveat, and `grep -ci melee` on `03-` returns 0.

Matt's own ratified bias ruling (2026-08-25, quoted in the feature registry header) is verbatim on this point: *"otherwise we build a skill that can **make a whirlwind**, not a skill that can **faithfully render any skill from a video**."* This is the same shape one level up.

**WARN-3 — "VERIFIED" in § 0 is a documentation-read tag, not an execution tag.** Legolas probe 2 defines VERIFIED as *"primary source fetched and read this session"*; **nothing in probe 2 ran on this host** except `system_profiler`. `03-` § 0 carries "Legolas probe 2, VERIFIED" into a TL;DR that also names the acceptance platform and the bake mechanism. Everything so tagged — the Hades stack via sibling `GPUParticles2D`, Movie Maker alpha PNGs, `transparent_bg` semantics, bake reproducibility, Compatibility + browser parity — is class-reference reading, untested here. (Probe 1's tags are genuinely first-hand — internal DB queries and a parsed 1.88 MB `Fx.sjson` — and `03-` underuses those relative to the probe-2 numbers it over-tags.)

**WARN-4 — The headline VERIFIED mechanism does not apply to the elements that carry the grammar.** `CanvasItemMaterial.particles_animation` applies **only** to `GPUParticles2D` / `CPUParticles2D`. `03-`'s own Compatibility ruling in the same sentence moves heads, links and children to **pooled sprites** and trails to `Line2D` — which need `AnimatedSprite2D`/`SpriteFrames` instead. `blend_mode` and `light_mode` survive (CanvasItem-wide); `particles_animation` does not. Separately, 02d raised that a `CanvasItemMaterial` and a custom shader *"are not two material objects automatically stacked on one item"*; `03-` folded the shader requirement and omitted the incompatibility, leaving every downstream *"through the shared `ShaderMaterial`"* resting on an unresolved question. **This should be an E0(a) gate and currently is not.**

**WARN-5 — V9 is posed on two premises that are precautions, not renderer facts, and is posed one level too low.** `emit_particle()` is genuinely Compatibility-excluded (class reference, quoted). **Trails:** probe 2 lists `trail_enabled`/`trail_lifetime`/`trail_sections` with no Compatibility caveat; the exclusion comes from Astra. **Sub-emitters:** no source calls it a renderer exclusion — Astra's words are *"excluded from the baseline until separately demonstrated on the installed build,"* a project precaution. `03-` resolves a live conflict between its two inputs silently and hardens a precaution into a technical fact on a row Matt is being asked to rule. And the real fork sits one level up: V9's premise is *"while the web playtest is a commitment"* — that commitment is what determines the renderer, which determines the pooled-sprite constraint, which shapes G1–G4. If the commitment is itself in play, a large part of the architecture relaxes.

**WARN-6 — Collision with the ratified VFX Feature-Family Registry, which `03-` cites nowhere.** The registry (`agentic_orchestration/gandalf/vfx-feature-registry.md`, born at VFX-DEPTH charter R-14, Matt-ratified, jack-ryan-ratified 2026-08-25) governs FF-01…FF-15 with measured routes and recorded disqualifications. My own ratification finding ruled *"the SPEC step may consume FF-01..FF-12 now."* `03-` is a VFX spec. Four live collisions:

- **FF-11 phrasing note, verbatim: *"the five named phases are ILLUSTRATIVE, NOT A REQUIRED INVENTORY. A two-phase effect satisfies the family."*** `03-` § 2.2 hard-wires *"anticipation → onset → peak → decay → residue"* into the runtime grammar template. The ratification warned in advance that graded as a five-item checklist this becomes **EXPECTED CONTENT** — the exact failure I-6 forbids one layer down.
- **FF-08's ratified trip law (`CV < 0.25` trips alone; 26 reference legs span CV 0.449–1.149, zero false-positive exposure).** G4 is *"pulse per tick"* at a fixed period; G2 has a fixed *"tick schedule"*; G3 a fixed *"hop delay"*. A fixed-period pulse is CV 0.000 exactly — the `OURS_blink` case the law was amended to catch. **Nothing in `03-` requires interval irregularity anywhere**, and § 4's tripwire list omits FF-08.
- **FF-05's route is disqualified** (`halo_area_ratio` *"cannot separate smoke from bloom"*; the scar arm, containing no smoke, reads highest). § 4 treats halo lift (+.16–.41) as a usable reference band. State whether it is re-derived from the CoM/Slormancer corpus (defensible) or leaning on the disqualified route (not).
- **FF-12's pre-named split trigger is live now.** It splits into self-luminance vs cast-contribution *"the first time a measured skill shows one without the other"* — and `03-`'s invariant layer stack separates body from `PointLight2D` **by construction**. That trigger should be executed, not inherited.

**WARN-7 — V12 re-poses a trade already in Matt's queue, with the opposite lean, uncited.** Q68 **G-4** (open since 2026-08-26): *"Body-alpha vs occlusion-gate trade — the budget's SIGN may be wrong (FF-15) … the referent smears the caster INTO the effect,"* conductor lean **(C) re-cut budget, figure may dissolve at peak** — and **R-25 ruled this trade is Matt's alone**. `03-` V12 recommends *"readability of body/footprint first"* with no reference to G-4, FF-15, or R-25. Related: **Q68 has been open three weeks and the VFX-DEPTH run is HALTED at CP#2-R.** Q79 now opens a third VFX-domain gate whose answers presuppose Q68 G-4 and Q78(a). Three open Matt gates on overlapping subject matter is a queue-discipline problem before it is a design problem.

**WARN-8 — The red-team's drops cluster non-randomly on the image-side proof obligations (02d § 3).** The build-time engineering corrections folded near-completely; the *"would not sign"* list folded at roughly half strength. The operative losses:

- **The ±10 % / ≤ 1 px *rejection* criterion is gone.** 02d required rejecting candidates that *"hit the numbers only through destructive clipping or unapproved distortion."* `grep -ci clipping` → 0, `distortion` → 0. Without it **the gate is satisfiable by damaging the asset**.
- **No flask / material-glass extraction gate and no density-asset gate.** 02d: *"E2 must separately validate density assets… neither route clears material glass automatically."* `grep -ci "density asset"` → 0, `glass` → 0 — against **two of the six skills** carrying an RGB material flask and poison needing *"cloud vs pool density."*
- Dropped, one clause each: *"if the prerequisite contract is missing, report the blocker; do not hide fixture construction inside TOOLING"*; *"occluded or unseen portions require a new commission, not a claim of faithful extraction"*; *"supported parameter ranges"* + *"clean import"* at freeze; *"a family may require multiple separately specified bursts"*; the art-step/rotation anti-false-positive clarification; the flash-on/off split in white reporting (which is the split that matters for V6).
- **RGBA-first was softened from experiment to contract.** 02d: *"Keep it first **as an experiment**."* `03-` states it as the extraction contract and transfers the unprovenness to the fallback.

**WARN-9 — E0-p reverses the red-team's § 3.9 without inheriting its instruments, and it is testing against a prior that predicts it fails.** Step 5 — *"≤ 2 guided key states painted over the **tooling-transformed piece arrangement**"* — is an image-model paint pass over machine-generated motion, exactly what 02d refused to sign without **separately budgeted key states, a correspondence test and a boil test**. `grep -ci correspondence` → 0; "boil" appears once, as a kill criterion on the **deprioritised video fallback**. So the boil test lives on the path that was demoted and is absent from the path Matt just ruled first. This is Discipline **#75 cl. 6** precisely: *a remedy does not inherit its predecessor's instrument.* (Mitigating: § 2.2b post-dates the red-team, so the obligation was un-inherited rather than knowingly discarded.)

And the prior is against it. Probe 2 § Q2(iii): *"the shape **inside** a burst must change between frames, and no transform produces that. **A nova is not a ring scaling up**"* — citing Hades shipping `Fx\RadialNova` as a flipbook, 16 entries off one sheet. E0-p step 3 is transforms over a static painted peak. gandalf's own pre-registered prior (`01-` § P4) said the same thing before any input returned: *"pure erosion of one silhouette may read as 'tech'."* `03-` files this as a *possible* kill; on its own evidence it is the *predicted* outcome, which means step 5 is doing the real work and the *"≤ 3 images"* headline has **zero slack** (1 peak + 2 key states = 3, with no repair line, while E1 budgets 3 repairs on 5 assets). If the peak plate fails RGBA extraction — a path `03-` marks *"unproved until exercised once"* — E0-p breaches its own cap on first contact.

**WARN-10 — No JUDGE step and no control for the unlabeled-identification tests.** § 2.3 and E2 both call for *"unlabeled"* distinguishability judgments with **no named reader and no known-bad control in the batch**, against `mechanical-process.md § 1` invariant 2 (*"JUDGE / TRANSCRIBE: separate instance; controls in every batch"*). This re-incurs the exact action I raised at `2026-09-13-run-C-3-gate2.md § 3` (#75 cl. 2) — *"that reader has no known-positive control"* — which is still open.

**WARN-11 — Unprovenanced fixture parameters, against the document's own rule.** § 2.1 requires *"provenance (source-game observation or Matt ruling per field)."* E1's parameters — 0.25 / 0.15 / 0.5 s, 4 BH at 8 BH/s, body 1.2 BH, 3 BH envelope — carry none, and they are the numbers both A/B arms run at. (For scale: the shipped Frozen Orb travels at `speed_px_s = 640` ≈ 4.9 BH/s, against E1's 8.) If they are wrong, both arms fail together and the experiment measures nothing about painted-vs-procedural.

**WARN-12 — Four ruled items narrowed, retired or re-opened without citation.** (a) **R-C3-123(2)** *"a **PACK OF PLACEHOLDER MONSTERS** (static, non-animated dummies) must be added to **the scene**"* → § 3 step 2's *"target dummy (+3 … as their grammars arrive)"* in a **fixture**. Pack→one, scene→fixture, uncited. (b) **R-C3-88**'s T3o Tab picker, which Matt named as *"the harness for comparing our own VFX"* and R-C3-99 reaffirmed, is replaced throughout by "Matt's fixture" with no statement that it is retired or subsumed. (c) **R-C3-90(3)** *"60 fps base with per-frame holds … **not on-2s**"* is re-opened as E0(d)'s *"stepped time — `fixed_fps` 30/15/12/8"*. Running it as a £0 probe is reasonable; presenting a closed question as open is not. (d) **R-C3-91**'s protection clause — *"no exploration may eliminate the pixel-art register/style combination"* — is not restated at V1/V2, the two rows where a route is being chosen.

**WARN-13 — The Astra design sessions are a de-facto new burst class with no rule row, and the architecture was co-designed with the generator.** `02a/02c/02d-` ran `codex exec -p astra-burst --ephemeral -s read-only`, 0 images — so not generations, and not interactive, and therefore not a breach of invariant 1. But they were not run through `lane/run_burst.py`, produce no receipt, no wrapper audit and no ledger entry, and have no `BURST_RULES` row or cap; `lane/audit.py` never saw them. Separately, `00-system.md § 0` names the lane's founding hazard as *"intent lived only in documents it wrote itself."* Three consults shaping the architecture is not a breach of invariant 4 (intent stays conductor-owned, and the anchor is declared provisional) — but it is intent sitting closer to the generator than the invariant contemplates, and it is undisclosed as such.

**WARN-14 — Host and budget items the document does not price.** (a) **Disk.** 20 GiB free of 460. § 2.2 mandates *two repeated bakes*; E0(b) *four backgrounds*; E2 *four 3-second clips*. At 1920×1080 RGBA, 3 s @ 60 Hz ≈ 180 frames ≈ **1.4 GB raw per bake** pre-compression, against a volume already carrying 17 `cliffside_v*` trees and 2,610 `harness_logs/` entries. (b) **The +2 ms p95 tripwire is unmeasurable as written** — V12 concedes the target frame rate is unstated — and the game tracker carries a live untested ceiling (*"iOS texture memory ~700 MB, `mist.png` 4340 px > 4096"*, older-device and Android caveats untested) that VFX atlases will land on top of. (c) **8 GB RAM** vs `measure()` is marginal, not blocking — it streams frames — but worth watching at E2's four-cast density. (d) Video decoding **is** available (`ffmpeg` at `/opt/homebrew/bin`), so E0-v was never decode-blocked; the V15 ruling moots it for effects regardless.

**WARN-15 — Unsourced or drifted numbers on rows Matt is being asked to rule.** (a) **Grok is stated at "~$0.42"**; the source files a price conflict it explicitly did not average — docs $0.05/s → **$0.30** vs third-party $0.07/s + $0.002/image → **$0.42** — and an unresolved gap that the CLI's video model is unpinned (`grok-imagine-video` vs `-1.5`, $0.48/$0.84). Real range **$0.30–$0.84**, up to 2× the stated fallback cost. (b) **Pixel FX Designer is $19.95, currently $14.96**; V8 carries only the sale price on a purchase fork. (c) **`strike_fast_v1`'s n is ~3** (E1 bolt, E2 splash, E3 victim flash, E4 pillar) and its source carries an **unresolved ⚠** — `LightningBoltZeusFx` shows 20 drawings / 0.33 s in data against ≈4 visible frames in footage. It is now a named reusable band and E0-p's pass/fail gate. (d) **The ~12-asset review trigger drops two caveats**: the per-god count is of sheets *whose path contains the god's name* (a soft lower bound), and probe 1's actual formulation is *"≤ ~12 per element **plus** a shared ~10-sheet cross-element constant layer,"* with *"the alphabet scales with grammar count per element, not with element count"* — which is the half that matters for V14, since `03-` runs four grammars and pins the trigger flat at 12. (e) **"The alphabet costs ~30 images for everything"** is asserted, not derived — 8 shared + 5 × (2–4) = 18–28 assets, and `03-`'s own rule that *"every isolation and EDIT counts against the image cap"* pushes the real figure materially higher. E0-p kill criterion #5 uses that figure as its denominator.

**WARN-16 — The 02b prior scorecard is stale and `03-` ships citing it.** L-3 and L-4 still read *"pending probe 2"*; the file's own header says *"Updated once when the remaining inputs land."* They landed. The instrument by which the conductor's prior was to be falsified was left un-closed while the thing it disciplines shipped — Discipline #73, the state changed and the record did not follow.

**WARN-17 — Where the ruling lands is unnamed.** `03-` says *"Not canon until Matt rules § 7"* and names no canonical destination, no decisions-log entry, and no Gate-1 — in a lane with a live precedent (**R-C3-117**, my Gate-1 BLOCK on the previous canon doc here, for an Authority line that paraphrased R-C3-102 and dropped its precondition). The Q79 reference column still points at **v2.1** while the doc is v2.3. Related and still open from the decisions-log 2026-09-15 entry: the *"Canonization precondition: Matt confirmation owed"* line is now likely **stale** (R-C3-119 records Matt ruling the scene CANON, R-C3-102 precondition satisfied) and was never updated; and the *"Reconciliation owed"* sweep across `style-register.md`, the game tracker, `ensemble-asset-pipeline-spec.md` and `pipeline-game.md` is outstanding — so R-C3-123(4)'s *"check everything is canonized"* is not currently satisfiable. **No new VFX/painted-2D entry appears under "Decisions to revisit."**

---

## 3. INFO findings

- **INFO-1.** § 2.3's *"Painted shared (8 + 1)"* lists eight items (P01–P07 + S01). 02c had nine (incl. P11 lane segment); P11 was correctly dropped for having no lane grammar among the six and the count was not adjusted. § 0's *"≈ 8 shared"* is now ≈ 7 painted + 1 puff.
- **INFO-2.** Fork numbers were silently remapped against Astra's V5–V12. The Astra column is correctly aligned to Astra's *answers* in every row checked, but a reader comparing "V7" across the two documents gets different questions. Astra's V5 (sixth treatment) and V10 (coverage denominator / melee) have no `03-` row at all.
- **INFO-3.** `04-parked-generator-coupling.md:10` preserves the *"6 families → 88 % emitted / 53 % reference"* figure that 02d § 1 told the team to **delete** (it is 53.3 % for six reference *archetypes*). Parking is not correcting; if the coupling is ever re-opened, the error re-opens with it.
- **INFO-4.** E0(a)'s *"3 s decal"* sits outside both the strike residue band (0.3–1.0 s) and 02c's own F1 fixture (*"Clear tail 1.70–3.00 s — Effect gone"*), while § 4 gates *"no residue presented as hazard."* Probably an inherited stack-proof parameter rather than an F1 value; nothing says so.
- **INFO-5.** Response classes went six → four (channel absent, support demoted to a preset). Justified — no channel skill among the six — and declared nowhere; § 4 correspondingly drops 02c's Channel class gates (endpoint ≤ 1 px, width ±10 %, cessation within one tick).
- **INFO-6.** Commit hygiene from the 2026-09-13 Gate-2 is open and compounding: ~1,290 untracked `.mp4`/`.png` (540 MB) under `runs/C-3/` with no ignore rule; `tests/t0c_summary.json`, `t0c_suite_output.txt` and `briefs/K3p-pack-walk-xv2.task.json` still dirty; ledger `ts` still mixes local and `Z`. `03-` adds per-effect clean plates, grey guides, masks, manifests, 60 Hz captures, four-cast clips and baked alpha PNG sequences on top of that.
- **INFO-7 — credit where it is due, and it is substantial.** Four things in this document are better than the lane's own precedent and should survive every revision: **(a)** E0 as a £0, no-images falsification step placed *before* any spend (Principle 2, correctly applied); **(b)** V13's *"3–2 → INCONCLUSIVE … never a silent default to B"* — a pre-registered refusal to let an indecisive result become a quiet decision; **(c)** § 4's frozen cross-family reference set + mixed-vintage playback, which names the drift failure mode honestly and builds the tripwire for it in advance; **(d)** the medium-change exit (E1's "procedural default", i.e. effects with no painted asset) correctly routed to Matt as a fork rather than taken by the conductor, per `mechanical-process.md § 1` invariant 5. `03-` also **corrects its own input** in one place — *"particle `fixed_fps` does not step sprites/shaders/lights together"* is more careful than probe 2 and, as far as I can establish, right.

---

## 4. Assessment of § 7's forks (the question asked: are these the right forks, well-posed, one recommendation each?)

**Mechanically clean.** Fourteen open rows, each with exactly one recommendation and an Astra one-word ruling; V15 correctly struck as ruled with its ruling carried inline. Format is not the problem.

**Five rows are not well-posed as written.**

| Fork | Defect |
|---|---|
| **V2** art step | Arithmetically, only one of its three options is consistent with the § 2.3 contract it is presented beside (BLOCK-3). And it is sequenced *after* the eight images it governs. |
| **V4** hybrid oracle | The body asserts it closed; the table asks it open; Matt's own precondition (R-C3-120) is absent; a second **OPEN** file gives the opposite disposition (BLOCK-6b). |
| **V6** white / dark duplicate | Reverses an accepted Matt fork (R-C3-90(2)) and lists the ruled position as the alternative, with neither evidence side shown (BLOCK-6a). |
| **V9** acceptance platform | Two of its three premises are project precautions hardened into renderer facts (WARN-5), and the real fork — whether the web-playtest commitment stands — sits one level above it. |
| **V12** failure priority | Re-poses Q68 **G-4**, a trade **R-25 ruled is Matt's alone**, with the opposite lean and no citation of G-4, FF-15 or R-25 (WARN-7). |

**Five forks are missing, and four of them are the expensive ones.**

1. **Genre coverage / what "complete" means.** Does the goal end at six projectile-field-chain-aura skills, or does it require a melee-sweep or displacement cell? This is the tautology in WARN-2 and the tripwire parked under the wrong reason in `04-` § 5. It is the single largest unstated scope question in the document and Matt should rule it explicitly.
2. **The prerequisite budget.** The dominant cost item in the whole workstream (BLOCK-5) is presented as a given, not a fork, with no ceiling — while the only numbers Matt sees are ≤ 3, ≤ 8 and ≤ 12 images. The document reads cheap and is not.
3. **A workstream-level stop criterion.** Every fork is about *how* to proceed. E1's *"both fail → fix the fixture"* assumes the fixture is at fault. There is no row that says what happens if E1 and E2 both fail — whether the six ship in a simpler register, or the workstream stops.
4. **The 3–6 BH extent cap.** It is exposed nowhere, it is an unratified conductor call from style-card v0.2, and it is the direct answer to Matt's complaint at **R-C3-123(3)** that *"the VFX are likely too small vertically and horizontally."* Shipping an unratified **cap** as the response to an **under-size** complaint needs its own row.
5. **E0-p's image budget.** *"≤ 3 images"* has zero slack and no repair line while E1 budgets three repairs on five assets (WARN-9). Either budget ≤ 4, or state that a failed extraction kills the probe.

**One fork is near-mooted and should be marked.** V7 (video as a shipping frame source for whole effects) is constrained by V15's ruling and by probe 2's actual finding, which is *"no hosted RGBA/alpha video-generation endpoint was **found**"* — a search result, not the experimental negative that *"none found or tested"* implies. Nothing was tested.

---

## 5. Severity summary

| Count | Severity | Gist |
|---|---|---|
| 6 | **BLOCK** | no charter on a halted ledger · gates not decidable · scale contract is pixel_scale-dependent and mis-sequenced · § 4 measured by an instrument that cannot measure it · prerequisites are the build and cost zero · two ruled decisions reversed uncited |
| 17 | **WARN** | generality tautology · VERIFIED over-tagged · registry collisions (FF-08 / FF-11 / FF-05 / FF-12) · red-team's image-side obligations dropped · E0-p against a prior that predicts failure · no JUDGE control · unprovenanced fixture params · four ruled items narrowed · unsourced numbers · stale scorecard · unnamed canon destination |
| 7 | **INFO** | count drift · fork renumbering · uncorrected 53 % · decal band · class count · commit hygiene · **credit (four genuinely strong moves)** |

**Gate-1 verdict: BLOCK** — on chartering a run against `03-` as written. The BLOCKs are cheap: declare one clock, define one crop, restate the scale contract as a function of `pixel_scale`, name the instrument behind each § 4 gate, price the prerequisites, and cite the two rulings being reversed. None of that changes the design. **The design should go to Matt; this document should not go to a builder.**

**Approval authority (ADR-002).** Everything above is documentation and design-record correction, which is mine to approve directly. Three items **escalate to Matt**: Q78(a) disposition (BLOCK-1), the V4/V6 re-dispositions of his own rulings (BLOCK-6), and the frame-extraction sourcing class that gates the `field_v1` lap (BLOCK-4). One item routes to **knight-rider**: the drax charter conflict (BLOCK-5).

---

## 6. References

**Under review**
- `agentic_orchestration/gandalf/notes/2026-09-15-vfx-workflow-architecture/03-architecture.md` (v2.3)
- `…/00-evidence-dossier.md` · `…/01-conductor-prior.md` · `…/02b-prior-scorecard.md` · `…/02a-`, `…/02c-`, `…/02d-astra-session-{1,2,3}.md` · `…/04-parked-generator-coupling.md`

**Inputs verified against**
- `agentic_orchestration/legolas/research/2026-09-15-vfx-grammar-and-authoring-split/findings.md`
- `agentic_orchestration/legolas/research/2026-09-15-vfx-motion-sources-and-tooling/findings.md`
- `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md` · `…/2026-09-15-video-generation-alternatives/`

**Canon and ruled decisions**
- `astra_test_01/burst/runs/C-3/ledger.json` (R-C3-88/90/91/98/99/106/113/114/115/118/119/120/123; H-C3-1, H-C3-2)
- `agentic_orchestration/gandalf/notes/2026-09-13-astra-burst-lane-run-C-3-charter.md`
- `canonical/reap-die-rise-game/painted-2d-pipeline/{mechanical-process,00-system,scene-builder-workflow}.md`
- `agentic_orchestration/gandalf/vfx-feature-registry.md` (FF-01…FF-15; I-1…I-7)
- `canonical/matt_decision_needed/README.md` (Q68, Q78, Q79) · `…/2026-08-26-vfx-depth-lap2R-superseding-gate.md` · `…/2026-09-15-hybrid-vfx-oracle.md` · `…/2026-08-25-youtube-frame-extraction-sourcing-class.md`
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (2026-09-15 entry, Active)

**Prior findings of mine this one continues**
- `agentic_orchestration/qa/findings/2026-09-13-run-C-3-gate2.md` (H-C3-2; actions #75 cl. 2 and #80 still open)
- `agentic_orchestration/qa/findings/2026-08-25-vfx-registry-ratification.md` (FF-01…FF-12 consumable at SPEC; I-7 INSPECT-ONLY routes; FF-11 illustrative-phases note)

**Instruments inspected**
- `astra_test_01/burst/oracle/vfx_measure.py` · `astra_test_01/burst/runs/C-3/vfx_kits/frozen_orb_v3/kit.json` (`pixel_scale: 3`, `phase_scale`, `white_core_keep: 0.92`, `ground_squash: 0.58`)
- `astra_test_01/burst/runs/C-3/cliffside_v12/` (`project.godot` = `gl_compatibility`; 7 duplicated `vfx_*_bolt.gd`; 0 `ShaderMaterial`) · `~/Games/reincarnated-godot/project.godot` (`Forward Plus`)
- `astra_test_01/burst/BURST_RULES.md` · `astra_test_01/burst/export/{effect_kit,godot_import}.py`

— jack-ryan, Gate-1, 2026-09-15
