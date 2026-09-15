# Astra design session 3 — red-team of the synthesis

> **STATUS:** RECORD — gandalf-conducted consult, 2026-09-15. Same channel; the v1 synthesis + Legolas probe 2 staged. **Note:** the red-team ran against synthesis v1 (generator-coupled); Matt re-scoped the goal the same hour and v2 removed the generator coupling, so the § 1/§ 4 items on coverage denominators, `VfxSkillSpec` over emitted schemas and the sixth treatment are moot. Every build-time, image-side, and coherence correction was folded into v2.1 (⟲ marks). Answer verbatim; prompt appended.

---

## 1. Where the synthesis misrepresents you

| Synthesis wording | Correction |
|---|---|
| §0: **“The drawings were never the problem”** | S1 §1 explicitly rejected that conclusion. Some drawings supplied useful forms; others contained haze, ambiguous boundaries, or unsuitable silhouettes. The system made those defects consequential. |
| §0: **“Coherence is the layer stack.”** | My claim was **coherence through shared construction**: geometry, material, silhouette proportions, timing, density, and inherited assets. A common stack is necessary discipline, not sufficient evidence of coherence. |
| §1: **“F3/F5/F9 system + brief”** | S1 classified F5 as **model + brief, exposed by system**. Exact background obedience and emissive-edge preservation remain model risks. |
| §2.3: **“premultiply exactly once at runtime”** | S2 specified conversion exactly once **if using a premultiplied runtime path**. Ordinary straight-alpha MIX is also legitimate. The synthesis turns a conditional requirement into a universal conversion. |
| §4: **“baseline subtracted explicitly; gate ≤ 2 %”** | S2 required total coverage, baseline coverage, and newly introduced white to be reported separately. Subtraction must not silently convert failure of the total-crop gate into a pass. If the background exceeds 2%, approve a separate attributable-VFX budget. |
| §6: **“one TOOLING burst ≤ 40 min”** | S2 bounded **E1’s exporter amendment**, assuming drax’s fixture and existing exporter. General family work may require multiple separately specified bursts; TOOLING stays serial and glue does not modify it concurrently. Those qualifications disappeared. |
| V10: **“reference corpus (53 % at six families)”** | S2 explicitly withheld the coverage claim pending reconciliation. L1 reports **53.3% for six reference archetypes**, not six families; its family columns contain unresolved inconsistencies. Restore three denominators: valid emitted, all emitted including unresolved, and reference skills. |
| §2.2, F1: **“a head that translates”** for `single_target` | S2 required delivery resolution because `single_target` may be instantaneous. Geometry supplies a family candidate, not permission to invent travel. |
| §2.2, F10: **“F7 with reversed radius”** | S2 specified inward flow, persistence, and gameplay-owned victim motion. Reversing a burst radius is one construction technique, not a complete vortex grammar. |

Also restore S2’s opening qualification: **all unattributed tolerances are proposed project gates**. I proposed ±10%, one pixel, and the asset budgets; I did not establish their production yield.

## 2. What breaks at build time

### Step 1 — Resolve the family contract

**First failure:** glue tries to merge the two emissions without a verified identity/revision join, then fills geometry or mechanics from prose.

**Smallest prevention:** day one produces:

- Separate, versioned readers for each source schema.
- A resolution report: resolved, missing, conflicting, unsupported.
- One explicitly synthetic F1 fixture with typed units and provenance.
- Production bindings only where authoritative gameplay data resolves every required field.

The 603 null geometries remain unresolved. `spatial_geometry_type` cannot generally reconstruct delivery semantics; prose effects cannot become executable parameters. Join seasons/classes only through an owner-confirmed key and revision relationship. Conflicts block registration. Registered aliases remain explicit; `projectile → single_target` must not smuggle in unspecified speed.

The engineering owner chooses authoritative mechanics. Matt approves presentation choices over that truth.

### Step 2 — Build the grey room

**First failure:** “mode of the production grammar scene” assumes the scene already exists. Building eleven families, deterministic scrubbing, a target simulator, capture passes, and exporter integration will not fit one 40-minute burst.

**Smallest prevention:** drax first builds one reusable **F1 production component** with:

- A minimal release/contact/cancel event interface.
- An explicit effect-age clock.
- Grey/painted material substitution.
- A fixture host with Keeper, one dummy, the real ground, and deterministic event replay.
- Reset-and-replay seeking to a selected tick.

A GPU particle simulation is not made seekable merely by adding an `AnimationPlayer` scrubber. Replay from a known reset before each capture. Additional dummies and behavior cases arrive with their families.

The fixture instantiates the production component; it need not be embedded inside that component. This preserves the important part of my recommendation without turning debugging UI into runtime architecture.

**The ≤40-minute boundary holds only for the explicitly scoped Astra exporter work after these prerequisites exist.** If the prerequisite contract is missing, report the blocker; do not hide fixture construction inside TOOLING.

**Renderer decision before E0:** retain Compatibility as the acceptance baseline while web playtest remains required. Godot 4.6 web export requires it. Manual `emit_particle()` and particle trails are unavailable there. [Renderer support](https://docs.godotengine.org/en/4.6/tutorials/rendering/renderers.html), [manual emission](https://docs.godotengine.org/en/4.6/classes/class_gpuparticles2d.html#class-gpuparticles2d-method-emit-particle).

The layer design remains expressible in native Godot, but **“all sibling GPUParticles2D” is not the implementation contract**:

- Authoritative heads, links, and scheduled child emissions use pooled sprites/nodes.
- Trails use `Line2D` or a ribbon mesh.
- Decorative particles use the tested Compatibility subset.
- GPU sub-emitters are excluded from the baseline until separately demonstrated on the installed build. Frozen Orb’s scheduled children must not depend on them.

E0 must exercise the actual browser export as well as desktop Compatibility. A Forward+ success does not clear that gate.

### Step 3 — Capture guides

**First failure:** the retained “original capture” contains the grey body. When the painted silhouette develops holes or shrinks, recomposition reveals grey, not the original terrain.

**Smallest prevention:** capture, at the **same frozen scene state**:

1. **Clean plate:** selected effect and its world responses disabled.
2. **Grey guide:** selected body visible, flash/halo/floor light disabled.
3. **Masks:** editable region, body coverage, primitive IDs, and protected foreground occluders.
4. **Manifest:** tick/event state, seeds, source/build hashes, viewport dimensions, camera transform, crop origin, native-to-screen transform, pivot, attachments, plane/projection state, sampling and colour-space settings.
5. **Separate annotation board:** rulers and arrows never enter the editable body image.

Restore protected pixels from the clean plate, including pixels revealed inside new holes. Preserve foreground occlusion separately. **Pixel-exact scene restoration is achievable through copying; pixel-exact recovery of an unknown translucent foreground from a flattened picture is not.**

### Step 4 — Paint the approved instant

**First failure:** the first brief requests an “approved VFX exemplar” before one exists. It may also ask one flattened contact image to become several independently moving assets.

**Smallest prevention:** declare the first fire paint-over **provisional**, using the approved scene/scale evidence and one selected project-owned body candidate. E1’s recomposed moving result establishes the directional anchor.

Each paint-over names one selected body/plane. A whole-contact appearance proposal remains a design target; isolation is a separate counted output. Occluded or unseen portions require a new commission, not a claim of faithful extraction.

### Step 5 — Produce missing primitives

**First failure:** the eight-item list becomes a purchase order before reuse is tested, or a projected ground paint-over is treated as a freely rotating ground-plane primitive.

**Smallest prevention:** commission only the slots needed by the current fixture. Every brief declares permitted orientation, deformation, and projection state. A screen-projected ground exemplar either gets constrained use or a separately authored unprojected production asset; “do not squash twice” does not solve arbitrary rotation.

Count every isolation and EDIT against the image cap.

### Step 6 — Extract, register, compile

**First failure:** the E0 tint demonstration is mistaken for the production material implementation. Multiplying greyscale by a hue is not a four-entry palette lookup, especially when index zero must map to an opaque dark colour.

**Smallest prevention:** prove a four-band, independently alpha-masked test texture through the actual shared `ShaderMaterial`. Carry flipbook UV selection, palette lookup, erosion, blend mode, and unshaded behavior there when required. `CanvasItemMaterial` supplies useful blend/animation facilities, but custom behavior requires a shader; these are not two material objects automatically stacked on one item. [CanvasItemMaterial](https://docs.godotengine.org/en/4.6/classes/class_canvasitemmaterial.html).

Restore endpoints externally; preserve atlas offsets; disable trimming initially. Do not premultiply index values before palette lookup.

**Bake failure:** `transparent_bg` changes the viewport background; it does not remove terrain, Keeper, dummies, or debug overlays. [Movie Maker transparency](https://docs.godotengine.org/en/4.6/tutorials/animation/creating_movies.html).

Add separate **review** and **bake** visibility configurations using the same effect component. Bake only the chosen local body layer on transparency. Keep floor lighting, victim tint, hit-stop, and shake live; retain separate emission/decal layers where their blending demands it.

A flattened mixture of additive light and opaque coverage is not generally a portable straight-alpha sprite over arbitrary backgrounds. E0 must test the chosen layer representation over multiple backgrounds, not merely replay a baked screenshot over its original ground.

Fixed seeds are necessary, not a complete determinism contract. Record events, clocks, RNG state, warm-up, frame-zero policy, and engine/renderer version. Compare two repeated bakes before claiming repeatability.

### Step 7 — Assemble and measure

**First failure:** a 30 fps recording conceals a 60 Hz contact error, while a prewarmed review conceals the cold-first-cast defect.

**Smallest prevention:** keep gameplay/event validation at 60 Hz; capture at sufficient temporal resolution to inspect its one-tick gate. Test lower-rate artistic holds separately. Particle `fixed_fps` alone does not step sprite transforms, shaders, and lights together.

Run genuinely cold and repeated casts, mixed simultaneous/staggered effects, cancellation, and browser performance. In E0, compare the proposed normal preset **without** a dark duplicate against the optional duplicate treatment; otherwise the architecture passes using an exception its production default omits.

### Step 8 — Freeze and publish

**First failure:** asset hashes are frozen while shared shaders, presets, exporter behavior, or fixture events remain mutable.

**Smallest prevention:** the accepted package pins the entire dependency set and supported parameter ranges. Changing a shared dependency invalidates affected acceptance records. Clean import, cold cast, cancellation, and the retained mixed-effects fixture must pass for the exact published build.

## 3. The image-side claims you would not sign

These include my own optimistic recommendations.

| Claim | What would earn my signature |
|---|---|
| **“The image model’s contribution is bounded to what it has evidence of doing well.”** | E1 must show useful **native, moving, extracted assets within the total call budget**. Attractive source images do not establish that narrower capability. |
| **Genuine RGBA first** as a dependable production route | Keep it first as an experiment. E1 must retain opaque dark interiors, thin tips, declared holes, and clean multi-background composites after reduction. E2 must separately validate density assets. Neither clears material glass automatically. |
| **One key-plate EDIT recovers emissive bodies** | Demonstrate a failed-alpha candidate repaired without losing tips, contaminating edges, or incorporating terrain. A fallback never exercised remains unproved. Translucent gas requires explicit coverage/density representation, not an asserted exact key. |
| **Three reference images hold register across eight family assets plus 2–4 additions per treatment** | E2 establishes only its tested four cells. Later additions must be compared against the **fixed original anchor and nearest sibling**, not only the latest descendant. Record first-pass acceptance, repairs, and representation changes. Three images are an input discipline, not a measured capacity. |
| **±10% bounds / ≤1 px attachment gates are achievable** | Separate raw model compliance from exporter-enforced compliance. Restore known attachment pixels and metadata deterministically. Reject candidates that meet the numbers only through destructive clipping or unapproved distortion. Report intervention cost; success after unlimited repair does not validate the budget. |
| **A paint-over can be isolated while preserving the approved appearance** | E1 must show guide → proposal → isolated native body → runtime recomposition, with protected pixels identical and no terrain baked into the sprite. The raw proposal remains provisional until that chain passes. |
| **“Self-lit” painting survives rotation and deformation** | E0 needs an asymmetric project-owned head with visible planes—not merely a symmetric disc. E1 must pass required directions, curvature, and stretch with no rotating-highlight or sticker read. No suitable existing asset means the relevant E0 claim waits for E1. |
| **Tool recolouring plus 2–4 silhouettes makes treatments distinguishable without glow** | E2 needs unlabeled identification at actual size and in mixed casts. Add a common-palette diagnostic to establish that shape/motion contributes identity. Repeat across all treatments; fire versus ice is an unusually easy pair and cannot certify fire/poison or holy/lightning. |
| **Movie Maker permits a paint pass and therefore makes the dial reversible** | E0 can prove capture/reimport only. An image-model paint pass needs separately budgeted, independently guided key states and a correspondence/boil test. L2 explicitly found no image-model-over-simulation precedent. Retaining procedural source enables reauthoring; edited pixels do not reconstruct it. |
| **E0 proves internal shape change** | Baking records existing motion; it cannot manufacture missing advection or breakup. Show an internally changing source first. If E1 exposes moving stickers, test authored states under the declared exit instead of calling a bake the remedy. |

The ≥99% opaque-interior gate also needs an **independently declared interior mask**. Selecting only the already-opaque pixels would make it circular.

## 4. The forks (§ 8) — your one-word rulings and dissents

| Fork | Conductor recommendation | My ruling | Dissent / qualification |
|---|---|---|---|
| V1 | B provisionally | **B** | Preserve the technical gates and explicit exits. |
| V2 | 3 screen px | **Three** | A starting source-art step, judged under rotation in motion. |
| V3 | E0 → grey room → E1 → E2 | **Reorder** | Build the minimal shared runtime/fixture spine and lock renderer constraints before E0. |
| V4 | Dissolve into class bands | **Dissolve** | Fixture envelopes remain labeled provisional until measured. |
| V5 | Six named treatments | **Provisional** | Fire/ice first; retain shadow as a candidate. Artistic treatment bindings are distinct from missing engine truth. |
| V6 | Keep flask + lob | **Keep** | Only where authoritative delayed-landing semantics support them. |
| V7 | White-free bodies; halo/floor default | **Keep** | The stated dark-duplicate objection is wrong: a dark underlay can create headroom; its cost is ground occlusion and register. |
| V8 | No video-generation spend | **No** | No production spend now; replace universal impossibility claims with the probe’s “none found/tested.” |
| V9 | Pixel FX Designer after E0 | **Defer** | E0 passing alone establishes no authoring gap. Buy only against a named task and acceptance test. |
| V10 | Reference denominator; melee/displacement required | **Reference** | Delete the erroneous 53%-at-six-families number and retain all three coverage reports. |
| V11 | World response before motif | **Response** | Keep it subordinate to gameplay readability. |
| V12 | drax; production-scene mode | **Drax** | One production component in a fixture host is sufficient; a universal grey-room editor is not required first. |

**Omitted rulings Matt needs:**

- **Acceptance platform — Compatibility.** Keep browser/native visual parity as the bar, or explicitly change the web-playtest commitment.
- **Failure priority — Readability.** When register, density, and performance conflict, preserve body/footprint information before secondary glow and particles; specify target frame rate alongside the +2 ms tripwire.
- **Indecisive E1 — Inconclusive.** A 3–2 result currently has no exit. Pre-register a bounded follow-up or stop; do not default silently to B.
- **Expansion — Review.** Roughly twelve assets remains a review trigger, never automatic permission to expand or a hard cap.

## 5. Coherence — the one failure mode you most expect

**Approved local exceptions accumulate into global drift.**

Every new treatment is judged against its nearest recent parent. Each remains within the same nominal grid, palette schema, and stack, yet plane proportions, negative space, particle density, loop emphasis, and silhouette ornament gradually change. Six months later every individual approval is defensible and the library no longer belongs together.

E2 passing does not prevent this: it tests a tiny, deliberately coordinated sample.

The tripwire should be **comparison against a frozen cross-family reference set**, including mixed playback of the new effect with old ones. Require the original anchor version, approved parameter envelopes, and comparison captures on every addition; changing a shared preset reruns all affected fixtures.

§3 already reviews new palettes, materials, presets, deformation, and unjustified assets. §4 carries useful per-family checks. **Neither explicitly requires this cross-vintage comparison**, and neither catches cumulative silhouette or density drift inside unchanged schema values. My S2 should have made that obligation explicit.

## 6. The three changes you would make to the synthesis before it goes to Matt

1. **§2.1, §3 steps 1–2, §6 E0 — replace the implied ready-made runtime with explicit prerequisites.**

   **Old:** “conductor glue assembles” → “VFX grey room” → “E0 … ~half a day.”

   **New:** “Before E0: versioned source readers produce a blocked/resolved report and one synthetic F1 spec; drax implements the reusable F1 event-driven component and deterministic fixture host; pin installed Godot version and Compatibility/browser acceptance. Use pooled nodes and ribbons for required event emission/trails. E0 estimates exclude these prerequisites. E1’s ≤40-minute TOOLING scope covers only the named exporter amendment.”

2. **§2.3 extraction, §3 step 3, §6 E0(b) — replace ‘original capture’ and whole-effect bake language with a capture/pass contract.**

   **Old:** “Recompose over the exact original capture” and “any procedural effect bakes … and re-imports.”

   **New:** “Retain synchronized clean plate, grey guide, body/ID/occluder masks, and complete transforms. Restore protected pixels externally. Bake selected local layers in an effect-only visibility configuration; preserve live world response and separate blend semantics. No trimming initially. Verify repeatability and multi-background reconstruction. Paint-over animation remains a separate unproved authoring step.”

3. **§0, §4, §6, V10 — restore hypothesis status and prevent acceptance drift.**

   **Old:** “The drawings were never the problem”; “Coherence is the layer stack”; unconditional tolerances; “53% at six families.”

   **New:** “Useful drawings failed within an incomplete system. Coherence requires shared construction and repeated comparison. Numeric tolerances and image budgets are provisional gates whose yield E1/E2 must establish. Every addition compares against frozen original anchors and a mixed cross-family fixture. Report total and attributable white separately. Withhold family-coverage percentages pending reconciliation; retain valid-emitted, all-emitted, and reference denominators.”
---

## Appendix — the prompt

### Design consultation, session 3 of 3 — red-team the synthesis

You are Astra (`gpt-6-astra`), closing the consultation. The conductor has synthesised your sessions 1 and 2 (`./evidence/astra-session-1-answer.md`, `./evidence/astra-session-2-answer.md`), the two Legolas probes, and his own prior into **`./evidence/03-architecture-synthesis.md`** — the proposal that goes to Matt. Read it first, in full.

One input is new to you: **`./evidence/research/vfx-motion-sources-and-tooling-findings.md`** (Legolas probe 2). Its headlines: Godot native is the motion source (`CanvasItemMaterial` `particles_animation` + `blend_mode` ADD/MIX/PREMULT_ALPHA + `light_mode` express the Hades stack as sibling `GPUParticles2D` on one texture; `GPUParticles2D` has `fixed_fps`, `preprocess`, `use_fixed_seed`, `amount_ratio`, trails); Movie Maker mode bakes deterministic alpha PNG sequences (`--write-movie out.png --fixed-fps N`, `Rendering > Transparent Background`); flipbook-vs-runtime is a per-grammar dial; EmberGen is Windows-only; no hosted video model returns alpha; `emit_particle()` is not supported on the Compatibility renderer (the web playtest runs GL Compatibility); Pixel FX Designer is the only paid tool clearing every fence.

**Your task: break the synthesis before Matt rules on it.** You are now the DRIFT-CRITIC, judging a document that carries your own recommendations — be harder on those than on the conductor's. Answer in Markdown under these exact headings.

#### 1. Where the synthesis misrepresents you
Any place `03-architecture-synthesis.md` states your session-1/2 position inaccurately, over-claims it, or drops a qualification you attached. Quote the synthesis line, state the correction.

#### 2. What breaks at build time
Walk the § 3 loop step by step as the person who will execute the TOOLING bursts and write the briefs. For each step: the first concrete thing that goes wrong, why, and the smallest change that prevents it. Pay particular attention to: (a) the grey room as "a mode of the production grammar scene" — what does drax actually build first, and does the ≤ 40-min TOOLING burst boundary hold? (b) the `VfxSkillSpec` resolution against two emission schemas that disagree — what does conductor glue do on day one with 603 null geometries and prose effects? (c) the Compatibility-renderer constraint on the web playtest vs `GPUParticles2D` features (`emit_particle`, sub-emitters) — does the layer stack still express natively on GL Compatibility, and does E0 need a renderer decision first? (d) Movie Maker baking with `transparent_bg` on a scene that also draws the real ground for Matt's review — how is the effect isolated for the bake? (e) the paint-over-of-a-blockout-instant: what the guide capture must contain so the extraction can restore the scene pixel-exactly.

#### 3. The image-side claims you would not sign
Every statement in the synthesis about what image_gen / EDIT will do that you consider unproven or optimistic — genuine RGBA quality at this register, plate keying of emissive bodies, the 3-image packet holding register across 8 painted family assets + 2–4 per treatment, the ±10 % / ≤ 1 px gates being achievable, "elements remain distinguishable with glow disabled" from tool-recolour + 2–4 silhouettes. For each: what E0/E1/E2 would have to show for you to sign it, or what gate to add.

#### 4. The forks (§ 8) — your one-word rulings and dissents
For V1–V12, give your own one-word ruling beside the conductor's recommendation, and a one-line dissent wherever you differ. Add any fork Matt must rule that the list omits.

#### 5. Coherence — the one failure mode you most expect
If E2 passes and the system still produces incoherent effects by month six, what will have caused it? Name the tripwire that should have caught it and whether § 4/§ 3 already carries it.

#### 6. The three changes you would make to the synthesis before it goes to Matt
Ranked. Concrete edits (section, old → new), not themes.

Single Markdown document; no preamble; no restatement of the architecture. Be short where you agree; be exact where you don't.
