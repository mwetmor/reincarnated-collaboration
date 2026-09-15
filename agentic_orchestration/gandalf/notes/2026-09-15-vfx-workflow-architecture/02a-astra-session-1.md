# Astra design session 1 — the image model's honest role in a painted-2D VFX pipeline

> **STATUS:** RECORD — gandalf-conducted consult, 2026-09-15. Channel: `codex exec -p astra-burst --ephemeral -s read-only` (gpt-6-astra, HIGH), workdir `~/astra-burst/consult/vfx-arch/`, five evidence PNGs attached, 115,180 tokens, no images generated. Prompt: `s1/prompt.md` (copied below the answer). Astra's answer is verbatim.

---

## 1. Why the two lanes held and the VFX lane did not — your reading

**I agree with the diagnosis, but would weaken its claims about what is impossible and strengthen its contracts around what must be deterministic.** The scene lane supplied geometry and visible context. The character lane eventually supplied motion from another source. The VFX lane asked a picture to supply appearance, animation, material separation, scale, and skill semantics simultaneously.

My understanding here comes from the supplied evidence and the exposed tool interface. I do not have private access to the image model’s internal process or independent memories of the earlier bursts.

### The five invariants

I would put them in this order:

1. **Structure before paint.** Decide what the skill does, to whom, where, and when. Approve that in motion over the real scene.
2. **Coherence through shared construction.** Decide which geometry, assets, materials, and timing behaviors are inherited before commissioning a new drawing.
3. **Visible register and geometry references.** Give the image model an approved appearance and an explicit spatial task.
4. **Deterministic isolation, registration, and scale.** The final asset pipeline must enforce these, even when an image edit helps obtain them.
5. **An explicit owner for time.** Runtime, simulation, video, or authored animation owns temporal correspondence. A generated image may propose key states.

Two amendments matter:

- Replace **“time is never drawn”** with **“time is never inferred from sheet order.”** Drawn animation works. Six well-chosen drawings with deliberate holds can work. These particular generated rows did not establish reliable correspondence or adequate motion.
- Replace **“EDIT preserves the object reliably”** with **“EDIT has worked well enough for these props, followed by validation.”** Character lesson 1 already records unchanged regions being repainted. A visible guide constrains the model; an external mask or compositor enforces a boundary.

I would add two invariants:

- **Separate coverage, material, and emitted light.** A dark flask, translucent smoke, flame body, and glow cannot safely share one luminance-to-alpha rule.
- **Judge the assembled effect at its actual size and density.** A successful sheet is an asset-source result. It is not a successful skill.

### F1–F11: where the failures belong

“Model-side” below means unreliable as a production guarantee, not incapable of ever producing a good example.

| Failure | Primary responsibility | My reading |
|---|---|---|
| **F1 — one grammar** | **System**, reinforced by brief | Four phase slots and a bolt/impact runtime cannot express orbit emission, jumping chains, or owner-following auras. The briefs also explicitly requested similar radial impacts. |
| **F2 — no targeting** | **System** | Targets, aim rules, collision, ownership, and chain selection are executable behavior. No sheet can supply them. |
| **F3 — too small** | **System + brief** | Cell dimensions describe storage, not visible extent. The model also varies occupancy. Missing projected-size references and late runtime review made that variation consequential. |
| **F4 — time from rows** | **Model + system** | The model does not reliably track persistent parts through a generated sequence. However, similar travel frames are not inherently wrong: translation can supply most projectile motion. The missing spinning/emission behavior needed a separate specification. |
| **F5 — haze** | **Model + brief**, exposed by system | Exact background and palette obedience failed. The subject wording encouraged luminous atmosphere while demanding none. The system then depended on that contradiction resolving perfectly. |
| **F6 — dark flask lost** | **System** | Dark objects can be greyscale. They cannot survive a pipeline that treats darkness as transparency or sends everything through an emissive material. Color alone would not fix that. |
| **F7 — copied flask instructions** | **Brief** | Zeus’s flask glass and fuse instructions are plainly unrelated. They compete with the intended subject. |
| **F8 — no reference** | **Brief/workflow** | The model had prose descriptions of a register, but no actual project example. |
| **F9 — white particles, disc, first-cast defect** | **System + brief** | Particle color and first-cast lifecycle are runtime defects. Frozen Orb’s white disc was explicitly requested. The original builder also explicitly preserved white. |
| **F10 — route comparison skipped** | **System/process** | The route that could have disproved the need for sheets was never compared. |
| **F11 — no coherence mechanism** | **System**, exposed by model variability | Independent generation creates independent design decisions. Shared ramps alone cannot unify silhouette, timing, particle density, and targeting. |

The five PNGs support a narrower conclusion than “the drawings are not the problem”:

- Frozen Orb supplies useful crystalline planes, shards, and broken rings. Its white disc and white-centered bodies also reproduce instructions that v0.2 later withdrew.
- BWC supplies recognizable flask/fire/pool ideas, but the fog and dark-body ambiguity make it a poor extraction source.
- The six-kit capture shows small local ornaments in similar locations. A still cannot establish their timing; Matt’s playtest supplies that evidence.
- The anchor and playtest contain many bright stones, yellow flowers, leaf highlights, and fine ground marks. Tiny bright particles compete directly with that texture.

I checked the supplied PNGs: Frozen Orb contains **10,779 distinct RGB colors**, with **61.1% exact-black pixels**; BWC contains **5,573 colors**, with **0% exact black**. These counts include small color differences; they are not perceptual band counts. They demonstrate that even the visually successful image did **not** enforce “exactly five values.” That belongs in export tooling.

## 2. What image_gen / EDIT reliably does and does not do for EFFECTS specifically

### (a) Emissive subjects, key plates, and clean mattes

**I don’t know whether a green or magenta plate will hold consistently for these emissive subjects. Test it.** Prop isolation is encouraging evidence, not proof for flame tips or translucent gas.

Haze is not logically unavoidable. The task can depict the **shape representing emission** while leaving illumination to the runtime. That distinction should be visible in the reference.

A useful prompt formulation is:

> Paint one opaque, banded flame-body sprite. Match the attached body-only flame reference. Preserve its filled silhouette and internal holes. The surrounding area is empty transparency. Light spill is a separate runtime layer.

This is a clearer representational task than “burning oil with absolutely no glow.”

**My provisional ranking for reusable body sprites:**

| Rank | Route | Qualification |
|---|---|---|
| **1, conditional** | Direct genuine RGBA output: body-only sprite | Best route if this tool produces usable alpha. Inspect the actual channel and recomposite it. A transparent-looking preview is insufficient. |
| **2** | Approved body → EDIT onto a supplied flat key plate → deterministic keying | Closest to the successful prop method. Likely useful for opaque flame shapes, shards, and flasks. Emissive edge preservation remains unproven. |
| **3** | Generate the body directly on a flat key plate | One fewer call, but appearance and background separation must succeed together. Use a plate color absent from the subject. |
| **4** | Black plate → controlled extraction | Good for bright masks and additive-only emission. Poor as a universal matte method for dark material or smoke. |
| **5** | Unspecified background → EDIT removes it afterward | Leaves the first call free to mix background, glow, and subject. Extraction may then require inventing the missing boundary. |

For green poison, use magenta if keying. For violet lightning, use green. Neither choice guarantees clean translucent edges.

There is a mathematical limitation here:

`observed color = alpha × foreground + (1 − alpha) × background`

Knowing the background does not uniquely recover both foreground color and alpha. Signed subtraction can retain bright and dark differences, but it does not automatically recover a portable foreground. I have not seen this project’s “signed-cut” implementation, so I cannot assess its particular assumptions.

**For poison gas:** paint a bounded puff silhouette and interior density pattern; derive opacity and erosion separately. Do not demand a photographically translucent gas plume and then expect an exact matte.

**For BWC:** split flask, flame, smoke, oil, and emission before extraction. Do not spend repeated calls trying to rescue them through one threshold.

### (b) Can EDIT animate?

**It can propose a later state. I would not entrust a 6–12-step production sequence to recursively editing the previous output.**

The likely failure is cumulative reinterpretation: shard count changes, holes migrate, contours thicken, and the pivot creeps. “20% farther out” is understandable as intent, but is not a geometric transform applied to persistent shard objects.

Outpainting has a useful difference: the neighbor can remain a literal spatial boundary. Temporal editing usually asks the model to replace the very pixels whose identity must persist.

Conditions I would use:

1. **One fixed canvas, pivot, and framing.**
2. **The original approved state in every call.**
3. **A target-state guide generated by tooling.** Move the actual shard cutouts outward, shrink the actual core, and show that result.
4. **One change at a time.** First displacement; separately erosion or breakup.
5. **A small number of independently anchored states.** Start with three: compact, expanded, spent.
6. **Externally preserve anything that must remain pixel-identical.**

A ruler helps scale. A numbered grid helps slot assignment. Neither supplies temporal identity.

I would keep onion-skin references **beside the editable image**, or as clearly separated supporting inputs. A ghost inside the paint region may become a second luminous contour or motion trail.

For the proposed test, compute the “20% outward, 30% smaller” guide yourself. Ask EDIT to repair painted planes around the transformed geometry. If the transformed image already looks good in motion, omit EDIT.

Also distinguish **radius smaller by 30%** from **area smaller by 30%**. Those are substantially different core changes.

### (c) A primitive alphabet

**Yes: this is a promising use of the model. Its runtime composability is the part that needs testing.**

I would begin with:

- **8–12 shared primitives** across the whole system.
- **2–4 distinctive additions per element.**
- **One production primitive per generation/edit call.**
- An optional **2×2 concept board** for choosing related forms, followed by isolated production assets.

Those are proposed budget limits, not measured model capacities. I do not know a universal count at which consistency fails. A single call with six related sparks is easier than six unrelated subjects with different material and projection rules.

A practical shared alphabet might include:

- Tapered streak.
- Broken ring segment.
- Curved slash.
- Compact impact wedge.
- Mote.
- Puff silhouette.
- Wisp.
- Ground patch.

Element additions carry specific shape language: crystalline shard, hooked flame tongue, viscous lobe, branching electrical junction.

Use a row or grid for **review and packing after acceptance**. Do not make grid layout another requirement of every production call.

Some primitives need engineering assistance:

- **Ring and arc:** provide exact inner/outer contours if thickness matters.
- **Chain segment:** provide endpoint positions, tangent directions, and allowable width. Exact endpoint pixels should be restored by tooling.
- **Pool tile:** “seamless” in prose is insufficient. Supply opposite-edge context or assemble overlapping patches that do not require perfect tiling.
- **Smoke:** provide separate coverage/density semantics.
- **Ice shard:** keep the painted material inside a stable silhouette; runtime owns its trajectory.

### (d) Greyscale-then-tint versus colored-per-element

**Default to greyscale value-indexed bodies with independent alpha, plus shared palette ramps. Keep material objects separate.**

The crucial distinction is **value index versus opacity**:

- Alpha says where the object exists.
- The value/index map selects a palette band.
- Emission strength says how much light it contributes.

A dark band must be allowed to remain fully opaque.

Greyscale reuse gives stronger coherence because a palette correction updates every consumer of the same asset. It does not itself guarantee legibility: size, negative space, halo, floor light, and overlap still matter.

Use colored assets, or additional material masks, when spatial color relationships cannot be represented by one ramp:

- Dark glass with pale reflections.
- Oil with warm flame and cool reflected light.
- Metal, stone, organic matter, or alchemical contents.
- A deliberately multicolored signature effect.

**F6 does not prove RGB is mandatory.** A greyscale flask with real alpha and a material-specific ramp can work. Full-color RGBA is simply the straightforward initial treatment.

White source pixels can remain legitimate **index data** if they map to a saturated pale band. What must disappear is the rule that automatically preserves them as rendered white.

### (e) Best contribution to motion

Rank **1 = best**, assuming reusable gameplay effects and amortized runtime tooling:

| Image contribution / motion source | Coherence across skills | Painted-register fidelity | Marginal cost per skill |
|---|---:|---:|---:|
| **Painted masks/primitives + procedural transforms and erosion** | **1** | **1** | **2** |
| **No generated motion assets; fully procedural shapes** | **2** | **3** | **1** |
| **A few painted key states + explicit runtime transitions** | **3** | **2** | **3** |
| **Painted still → video → cut/matte/retime** | **4** | **4** | **4** |

These are architecture judgments, not benchmark results.

Important qualifications:

- Key poses do not come with a correspondence map. Crossfading two painted silhouettes can produce double edges. Prefer discrete swaps, moving persistent pieces, or guided deformation.
- Erosion changes coverage; it does not create convincing flame advection or a chain jumping between targets. Those need motion rules.
- Video may be useful for a special smoke flourish or background emission. The character walk result does not establish control over a 67 ms strike.
- Procedural motion should use authored curves and constrained variation. Unrestricted noise will create the “rendered noise” failure.

### (f) Capabilities and controls worth using—or refusing to assume

**Transparency.** The built-in skill explicitly allows asking for actual transparency. Current official API documentation also describes transparent PNG/WebP output, while noting consistency and precise-layout limitations. That establishes a supported route, not the alpha quality of this particular burst wrapper. Test the returned file. [Official image-generation documentation](https://developers.openai.com/api/docs/guides/image-generation)

**Layered outputs.** The exposed tool does not promise PSD layers or registered albedo/emission/normal passes. Requesting “separate layers” inside one picture may produce a diagram. Generate separate assets or derive channels from one accepted image.

**Multi-image conditioning.** This project should use it aggressively but clearly:

1. Edit target or geometry guide.
2. Approved VFX exemplar.
3. Scene-and-scale reference.

State each image’s role. Multiple unrelated inspirations introduce ambiguity.

**Masks.** The current built-in interface exposes references, not an explicit hard edit-mask parameter. Even API masks are described as guidance rather than exact boundaries. Use external compositing for exact preservation. [Official image-editing documentation](https://developers.openai.com/api/docs/guides/image-generation)

**Depth/normal hints.** A model can interpret a height guide or paint something resembling a normal map. I would not trust that output as geometrically correct surface data. Derive technical maps from actual geometry or accepted masks.

**Reference strength and seeds.** No numeric reference-strength control or seed is exposed in this session’s image tool. Do not design around undocumented knobs. Repeatability comes from retained assets, fixed guides, controlled transforms, and versioned references.

**Resolution.** Use **1024×1024** as a starting working canvas for one compact primitive, or **1536×1024** for a wide shape. These are practical starting points, not magic consistency sizes. Supply an enlarged preview of the intended native grid. Downsample, quantize, and validate deterministically.

**Useful underused task:** paint-over of a runtime-generated silhouette at a specific instant. That gives the model a concrete shape-design problem with scale and placement already settled.

## 3. What the *scene* lane's successes translate into for effects

| Scene success | What the model receives | What it returns | What enforces the result |
|---|---|---|---|
| **Grey room** | A captured instant from an approved moving blockout: caster, target, footprint, trajectory, pivot, and occupied region | One painted body or key state occupying that region | Runtime owns targeting/timing; exporter checks bounds |
| **Outpaint against neighbors** | An accepted arc/chain section adjoining a guided extension, or a target pose constructed from accepted pieces | Painted continuation or repaired joins | Tooling restores exact connection points and retained pixels |
| **Anchor image** | Approved `VFX chunk_A`, the relevant element sample, and the scene crop | A new primitive in that existing register | Comparison against retained exemplars at native and scene sizes |
| **Dress then isolate** | An approved in-scene effect design, cropped with its original framing | Body-only extraction on transparency or a flat key plate | Recomposition over the original crop tests registration and edge quality |
| **Projected size chart** | Keeper at 130 px, intended body bbox, ground footprint, and native-grid inset | A body designed for that occupied extent | Measured occupied bounds; one declared scale conversion |
| **Engine owns motion** | A still showing orientation, material role, and deformation limits | A reusable shard, tongue, streak, patch, or optional key state | Runtime supplies transforms, emission, erosion, collision, and ownership |
| **Instrument + eyeball** | Native-size asset, actual-size scene render, and marked defects | One targeted correction | Separate technical gates and Matt’s in-motion judgment |
| **One version per note-set** | Approved parent asset, unchanged references, and one explicit change list | One versioned candidate | Existing acceptance process and retained lineage |

Two translations have limits:

**Painting over the scene is excellent for finding an effect’s appearance, but can complicate extraction.** Flame spill, reflections, and smoke may become inseparable from the ground. For initial anchors, use an in-scene design pass. For routine production, use isolated primitives conditioned on that approved design.

**Temporal “neighbors” require persistent geometry.** If a chain endpoint or shard is meant to remain identical, copy it or transform it. Do not rely on the model to rediscover it.

For isolation, preserve the original canvas and pivot. Recomputing placement from a tight bbox on every frame will introduce animation jitter. The diff bbox is useful for locating a proposed edit; it is not proof that every changed pixel belongs to the effect.

## 4. Register coherence — how would YOU keep 15+ grammars × 6 elements reading as one language over that painted ground?

**I would separate grammar, element treatment, and material class, then make new skills inherit all three.** Ninety combinations should not imply ninety independent sheets.

### Image side: establish one approved VFX family

Create a **`VFX chunk_A` reference package** containing:

- Three approved shapes: directional, radial, and ground-bound.
- Their isolated body-only assets.
- Their assembled appearances over the actual ground.
- Keeper at the same scale.
- A native-grid enlargement.
- Explicit distinctions between body, halo, floor light, and optional dark material.

The first approved element becomes the parent visual construction. Other element anchors should be derived from the same underlying examples, then receive a small number of distinctive silhouettes.

**Do not use Frozen Orb’s entire sheet as the universal anchor.** That would carry its crystalline geometry, starbursts, white centers, and row conventions into unrelated elements. Use selected shapes as candidates, then establish an approved runtime appearance.

Keep the scene anchor in the package to establish painted weight, edge character, and detail restraint. Its tiny rocks and grass strokes are not the desired detail density of a fast-moving effect.

The Hades result supports reuse **within families**. It does not mean one universal sheet should serve every effect. The reported **112/126 families** should not become a quota or a claim that 89% of all Hades effects use one texture. [Supplied Hades findings](/Users/admin/astra-burst/consult/vfx-arch/evidence/research/vfx-oracles-findings.md)

### A scale contract that does not confuse cell size with effect size

Declare:

- Working-image dimensions.
- Native asset dimensions.
- Occupied body bounds.
- Pivot and attachment points.
- Intended screen extent in BH.
- Rendering plane: upright, ground, or camera-facing.
- Whether projection is already baked.
- Allowed runtime deformation.

At Keeper = **130 screen px**:

| Intended extent | Screen pixels |
|---|---:|
| 1 BH | 130 |
| 1.5 BH | 195 |
| 3 BH | 390 |
| 6 BH | 780 |

With a three-screen-pixel art step, an occupied width of **64 native pixels becomes 192 screen pixels**, approximately **1.48 BH**. A 3–6 BH burst needs roughly **130–260 native pixels across its assembled extent**, or multiple smaller primitives distributed across that space.

Therefore, “everything reads in a 64 px cell” and “bursts span 3–6 BH” cannot share one unexplained scale rule.

Choose an initial two- or three-screen-pixel art step by scene review, then keep it consistent within the approved family. Scale changes should not silently change the apparent brush size.

### Light direction and projection

**Do not paint every primitive with an upper-left highlight.**

- Opaque props and substantial material fragments should respect the scene’s upper-left lighting when their orientation is fixed.
- Emissive flame and electrical bodies should derive their value structure primarily from their own energy pattern.
- A shard with a baked upper-left highlight rotates that highlight when rotated at runtime. Use restrained ambient shading, a separate shading treatment, or a few orientation variants if this becomes visible.
- Ground rings receive ground projection. Upright flames and flask bodies should not be flattened by the same Y squash.

For ground geometry, define rotation in the ground plane and then apply projection. For already projected painted assets, avoid projecting them twice. Camera yaw **47°**, pitch **52.95°**, and squash **0.5–0.62** need an explicit coordinate convention; they are not interchangeable numbers.

### Runtime side: coherence must survive addition and overlap

Use a shared material stack with optional layers:

- Banded body with independent alpha.
- Halo and floor light.
- Optional dark material/underlay.
- Shared particle assets and budgets.
- Optional impact flash.
- Decal or residue where appropriate.
- Hit response selected by gameplay significance.

“Shared stack” should mean common implementations and defaults, not every layer enabled on every effect. Healing ticks should not inherit a strike’s flash, shake, and hit-stop.

Create explicit grammar behavior:

- **Frozen Orb:** traveling emitter; shards spawn around it according to a schedule.
- **BWC:** thrown object with separate ground position and visual height; landing creates a persistent pool.
- **Chain:** target-to-target connections driven by actual target selection.
- **Self aura:** owner-following ground and upright components.
- **Beam:** endpoints and width driven by the channel.
- **Melee arc:** attachment and sweep driven by the attack.

Reject unsupported geometry mappings during validation. Do not silently render them as projectiles.

### Use the measured rules with their original scope

I would retain v0.2’s **white-free bodies, halo/floor-light separation, and 3–6 BH burst ceiling**, with these qualifications:

- **3–6 BH is a burst envelope, not a minimum for every mote, bolt, or aura.**
- Hades’ **0–1-frame rise and 2–7-frame half-life** concern selected strikes. They are not mandatory for gathering, pools, channels, or summons.
- CoM/Slormancer’s **0.1% near-white** describes combat-crop coverage. Hades’ white-core fraction describes effect pixels. Keep both denominators explicit.
- The supplied measurements associate readable effects with halo and floor light; they do not isolate those as the sole cause.
- A **+0.16–0.41 brightness lift** cannot be applied blindly to already bright ochre ground without clipping. Calibrate the transfer in this scene.
- Measure white coverage **after compositing**. Several individually saturated additive layers can still accumulate into white.

The research’s “no dark duplicate” finding applies to the sampled effects, not a proven prohibition across an entire game. Treat the optional underlay as an artistic tool, not a historical argument.

### Concrete corrections suggested by the supplied schema and v3 JSON

The artifacts show unresolved contract differences:

- T3t expects a tint array; v3 supplies a tint object and additional fields. Version the schema and validate migrations.
- T3t explicitly preserves luminance ≥ **0.92** as white. V3 retains `white_core_keep: 0.92`.
- V3’s core `[0.88, 1.0, 1.0]` has saturation approximately **0.12**. If rendered directly, it falls within the oracle’s near-white classification.
- V3 has `dark_duplicate: true`; v0.2 made that optional. This deserves deliberate review, not automatic removal.
- Dropping `impact_00` was the correct response to the duplicated flash.
- V3 encodes **233 ms cast**, **200 ms travel loop**, **200 ms impact**, and **633 ms residual**, assuming the stated 60 Hz hold semantics. Those are playback durations, not a complete skill timeline.
- `640 px/s ÷ 130 = 4.92 BH/s`. That is below the Hades projectile band but close to the dossier’s derived D2 Frozen Orb speed. It may be appropriate for this skill.
- `element_class: "strike"` does not express an orbit-emitter grammar.

These are readings of [the schema](/Users/admin/astra-burst/consult/vfx-arch/evidence/t3t_effect_json_schema.txt) and [the v3 definition](/Users/admin/astra-burst/consult/vfx-arch/evidence/frozen_orb_v3_effect.json), not verification of the current renderer.

For month-six additions, require the same anchor versions, palette versions, native grid, grammar validation, and fixed scene review views. Reuse existing assets first; commission only the missing visual distinction.

## 5. Your three candidate architectures

All three need a runtime specification containing **targeting, ownership, geometry, size, event timing, and termination behavior**. The difference is how much appearance and temporal shape change the image model supplies.

The experiment budgets below include generated images and edits. Tooling may assemble previews without additional image-model calls.

### A. Guided painted key-state animation — most image-model-heavy

**What the model paints**

An approved initial state followed by 4–8 painted states, each conditioned on the original anchor and a tooling-generated pose guide. Separate assets for object, body, smoke, and light where necessary.

**What the runtime does**

Places the animation according to the grammar, schedules frame holds, moves persistent pieces, applies tint/light, and triggers transitions from gameplay events.

**How time is produced**

An explicit dope sheet selects states and holds. Runtime transforms fill only transitions that preserve identity. Arbitrary silhouette interpolation is excluded unless it passes a separate test.

**Where size/timing live**

The grammar definition and animation metadata. Each state shares a canvas/pivot; each declares expected extent at its timestamp.

**How a skill enters**

Approve a blockout, commission the minimum missing key states, inspect the resulting loop in scene, then register the animation against the grammar.

**Cheapest falsification experiment: ≤12 images, ≤1 tooling burst**

- 1 approved eight-shard burst.
- 5 recursively edited later states.
- 5 independently generated states using the original plus exact transformed guides.
- 1 targeted retry.
- One small harness supplies guides, frame holds, and side-by-side scene playback.

Proposed gates: pivot error ≤ **1 native pixel**, expected extent within **±10%**, all eight shards retained until their scheduled disappearance, and no visible unplanned size pumping. Matt judges motion at gameplay speed.

**Most expected failure**

Guided states still change shard identity or contour weight, producing boil. Recursive states drift more. The cost is paid per sequence and again when the shape design changes.

### B. Shared painted primitives + runtime grammars — my first build

**What the model paints**

A small body-only alphabet, a few element-specific silhouettes, and occasional signature key states. Opaque props are separate assets.

**What the runtime does**

Builds skills from reusable components: moving emitters, constrained particle arrangements, ribbons, target links, ground fields, attached auras, and shared materials.

**How time is produced**

Transforms, event schedules, controlled emission, palette stepping, and erosion. A distance field derived from the accepted mask controls geometric erosion; an optional painted pattern supplies irregularity.

**Where size/timing live**

A versioned grammar definition in BH and seconds, plus primitive metadata for pivots, material, native grid, projection, and deformation limits.

**How a skill enters**

Map its emitted engine fields to a validated grammar; preview with placeholders; reuse the alphabet; request a new primitive only when the existing library lacks the required silhouette.

**Cheapest falsification experiment: ≤8 images, ≤1 tooling burst**

- 1 anchor-design still.
- 4 isolated primitives: directional wedge, broken arc, flame tongue, puff.
- 1 separate flask.
- Up to 2 targeted repairs.

One bounded harness compares **procedural and painted versions of the same frost-bolt motion**, then reuses components in a fixed chain and a throw-to-pool demonstration. It need not implement the full 26-type palette.

Review on bright dirt and foliage, with one and four simultaneous casts. Keep geometry, timing, size, and light identical during the procedural/painted A/B.

Reject the primitive split if basic rotation/stretching destroys the painted planes, if the assets cannot be cleanly composited, or if ordinary new skills require several bespoke sequence frames.

**Most expected failure**

The system becomes attractive moving stickers: convincing translation but insufficient internal motion. Fire may require two or three tongue states; chain ribbons may require better joins. Add that complexity only where the demonstration exposes it.

**Why I would build this first**

It gives the image model a bounded task it has evidence of doing well: designing painted shapes. It makes gameplay distinctions explicit and amortizes art across skills. The harness begins with the skipped procedural baseline, so the contribution of paint is actually tested.

### C. Procedural geometry and materials — least image-model-heavy

**What the model paints**

Nothing required for production. Optionally one approved target still for visual comparison.

**What the runtime does**

Constructs ribbons, rings, wedges, puffs, shards, trails, and fields from authored geometry and shared materials. Uses the same targeting and grammar definitions as B.

**How time is produced**

Entirely procedural, using fixed curves and controlled randomness. Geometry and coverage can be quantized without quantizing actor translation.

**Where size/timing live**

Entirely in versioned grammar/material definitions.

**How a skill enters**

Select the grammar and element treatment; tune parameters inside approved ranges; review it in scene.

**Cheapest falsification experiment: 0–1 images, ≤1 tooling burst**

Build one frost-bolt and one persistent-field demonstration using authored polygons, banded fills, and the v0.2 lighting split. Render at matched extents and compare with existing accepted shape references.

Fail the hypothesis if the silhouette/timing are correct but Matt consistently reads the result as vector graphics, uniform triangles, or shader noise against the scene.

**Most expected failure**

Mechanical regularity: identical tapers, smooth curves, repetitive breakup, and insufficient painted asymmetry. It may still be completely adequate for motes, rings, and supporting layers.

## 6. What you need from the conductor to do your part well

### A brief with one visual responsibility

Give me the following, in this order:

1. **Asset role:** opaque object, banded body, smoke density, ground patch, or emission-only layer.
2. **What is already approved:** grammar, motion, scale, and material behavior.
3. **Input image roles:** edit target, VFX anchor, scene/scale reference.
4. **The one requested visual change.**
5. **Canvas, occupied bounds, pivot, and orientation.**
6. **What the exporter enforces.**
7. **Acceptance checks and the retry budget.**

A useful primitive brief would look like this:

> **Asset:** `fire_tongue_A`, body-only, independent alpha.  
> **IMAGE 1 — edit target:** approved silhouette enlarged 8× from a 64×64 native cell. Preserve the base attachment and outer silhouette.  
> **IMAGE 2 — appearance reference:** approved fire-body exemplar; match its three broad painted planes.  
> **IMAGE 3 — context:** scene crop with Keeper and the intended projected placement.  
> Paint one hooked tongue with a broad base and a clearly narrowing tip. Keep internal detail large enough to survive the supplied native-size preview. Surrounding area: genuine transparency.  
> The exporter owns palette quantization, native-grid conversion, pivot metadata, halo, and floor light.  
> Return one candidate. One diagnosed retry for a named visual defect.

The target guide should already contain the intended dimensions. Numeric instructions describe its meaning; they should not substitute for it.

### Reference packet

Use **three inputs by default**:

- Working canvas/guide.
- Approved relevant VFX exemplar.
- Scene-and-scale board.

Supply the actual images, not filenames mentioned only in prose. Include a 1:1 native preview as well as the enlarged version.

Use self-authored approved art as model references. The supplied research explicitly keeps third-party atlas samples study-only.

### Canvas and per-call caps

My starting limits:

- **One production primitive per call.**
- **One edit objective per call.**
- **One diagnosed retry**, then reconsider the representation or split the task.
- **Three key states before attempting six or twelve.**
- **1024×1024 working canvas** for compact assets; **1536×1024** for wide ones.
- Provide the native-grid guide at an integer enlargement.
- Leave explicit margins; roughly **12.5% per side** is a reasonable initial safe area, adjusted to the shape.

Packing, labels, exact cell cutting, palette enforcement, and registration are tooling tasks. They should not consume the image call’s instruction budget.

### What helped in the three supplied briefs

- Concrete subjects: crystals, glass, oily flame tongues, smoke puffs.
- Right-facing travel and left-facing trails.
- A stated small-size review.
- Explicit cell separation.
- BWC and Zeus explicitly withdrawing the white impact disc.
- Bounded calls and honest concern reporting.

### What hurt

**The requests were overloaded.** One call had to solve 24 drawings, four phases, temporal progression, loop closure, material identity, exact palette, exact background, exact grid, and register without a reference.

**Some instructions contradicted the desired outcome.**

- Frozen Orb explicitly asked for a white flash disc.
- BWC said its brightest impact value was pale grey while retaining instructions for white flame cores.
- “Exact five values” and “no anti-aliasing” were treated as something prose could enforce.
- Zeus asked for flask glass and fuse sparks.
- “A bolt that JUMPS” described a visual kink; it could not implement a target jump.

**The visual references were doing unintended work.** “1990s 16-bit” and game-name cues push toward generic retro sprites. The current register needs its own image anchor. Earthbound must remain absent from visual instructions; Secret of Evermore is a feel reference, not a sprite-rendering specification.

**“Read at 64 px” had no relationship to the Keeper.** It specified a thumbnail test without specifying the projected result.

**The retry criteria favored file appearance over usefulness.** A correctly arranged sheet could still have weak motion, wrong silhouette, inadequate scale, and no usable material separation.

### What not to ask me for

Do not ask the image model to:

- Guarantee exact RGB values, alpha topology, or pixel-identical preservation.
- Produce twelve registered animation frames from percentages in prose.
- Infer targeting or skill grammar from a skill name.
- Recover opaque black material and translucent glow with one brightness cut.
- Paint mathematically correct distance fields or normal maps.
- Invent unseen parts during isolation while claiming the object stayed unchanged.
- Decide scale from cell size.
- Repair an undefined runtime through increasingly emphatic prompts.

**Ask me to design and refine the painted shapes inside a visible, executable contract. That is the contribution I would trust enough to build around.**
---

## Appendix — the prompt

### Design consultation, session 1 of 3 — the image model's honest role in a painted-2D VFX pipeline

You are Astra — the same `gpt-6-astra` model that has been executing every GENERATE / EDIT / CHECK / TOOLING burst for this project's painted-2D pipeline (scene chunks, isolated props, character stills, paint-overs, greyscale effect sheets, and the Godot exporter tooling). This session is NOT a burst: no images are generated, nothing is written except your answer. You are being consulted as a peer designer who understands, from the inside, what `image_gen` and image EDIT can and cannot hold — and the conductor (gandalf, Claude) needs that knowledge to design a VFX workflow architecture. The project owner, Matt, asked for this explicitly: *"ask Astra for advice in designing the architecture, as it will have a high level of understanding of what will work with image gen and edit."*

Read everything in `./evidence/` first. `00-evidence-dossier.md` is the spine: what worked in the scene lane and the character lane, what failed in the VFX lane, with ledger ids. Look at the five PNGs (`img_*`): the good greyscale Frozen Orb sheet, the hazy Blackwater Cocktail sheet, the scene anchor chunk, the six kits as they render in the live scene, and the playtest scene itself. Read the three briefs you were given for those sheets, the style card (v0 → v0.2), the scene-builder canon, the two research findings (Hades oracle numbers; Children of Morta / Slormancer / Chronicon measurements), the T3t effect schema, and the Frozen Orb v3 `effect.json`.

Then answer, in Markdown, under these exact headings. Be specific and honest; say "I don't know" or "test it" where that is the truth. Numbers and concrete prompt/edit mechanics beat adjectives. This is design, not a pitch.

#### 1. Why the two lanes held and the VFX lane did not — your reading
Do you agree with the dossier's five invariants (§ 5)? What would you add, remove, or reorder from the image model's side? Which of the eleven failures (§ 4 F1–F11) are *model-side* (the model cannot do the thing), *brief-side* (the brief asked wrongly), or *system-side* (the wrong thing was asked of the model at all)?

#### 2. What image_gen / EDIT reliably does and does not do for EFFECTS specifically
Answer each of the dossier § 6 UNKNOWNs from your own understanding:
- (a) Will a flat key plate (`#00ff00` / `#ff00ff`) hold for **emissive** subjects (fire, holy light, poison gas) the way it held for props — or does the model insist on atmosphere around light? If haze is unavoidable, what is the *right* way to get a clean matte: draw on a plate and key; draw on black and signed-cut; draw the emissive body with **no** background instruction and let EDIT strip it afterwards; something else? Rank by reliability.
- (b) Can EDIT **animate**? I.e. take frame N as the canvas and paint frame N+1 with a motion instruction ("the same burst one step later: shards 20 % further out, core 30 % smaller") — the scene lane's outpainting-against-neighbours, applied along time. Does it hold shape identity and scale across 6–12 steps, or drift? What conditions make it hold (fixed canvas, a ghost of frame N left visible, a ruler, a numbered grid)?
- (c) A **primitive alphabet**: can the model paint a small set of isolated effect primitives per element — flame tongue, ice shard, ring, arc segment, mote, pool tile, chain link, wisp, smoke puff, spark — each on its own plate, in one register anchored by a reference still, such that they compose in a runtime? What count per element stays consistent? Should each be one image, one row, or one grid?
- (d) **Greyscale-then-tint vs coloured-per-element**: given the tint ramp already exists in the builder, which gives more coherent results across elements *and* better legibility over painted ground? Where does coloured-per-element become necessary (the dark glass flask, F6)?
- (e) What is the image model's **best contribution to MOTION**: key poses for a runtime to interpolate; masks/silhouettes for a shader to erode, scroll and posterise; a still for a video model to animate; nothing (motion fully procedural)? Rank for (i) coherence across skills, (ii) register fidelity, (iii) cost per skill.
- (f) Anything you know the model does well that this project has not used yet (transparent-background output, layered outputs, multi-image conditioning, depth/normal hints, reference-strength behaviours, seed/consistency tricks, resolution/grid sweet spots).

#### 3. What the *scene* lane's successes translate into for effects
For each scene-lane success in dossier § 2 (grey room; outpaint-against-neighbours; anchor image; dress-then-isolate; projected size chart; engine owns motion; instrument + eyeball; one version per note-set): what is its **VFX analogue**, concretely, in terms of what image the model would receive and what it would return?

#### 4. Register coherence — how would YOU keep 15+ grammars × 6 elements reading as one language over that painted ground?
The scene register is canon (D2 weight, Bastion painted pole, H1 line; Keeper 130 px; camera yaw 47° / pitch 52.95°; the anchor chunk). The measured legibility rules are in the style card v0.2 (no white cores; halo + floor light; 3–6 body-heights burst cap; shapes on their own pixel grid). What mechanism would you put in the *image* side and what in the *runtime* side so that a new skill added in month six still looks like the game? Consider: a per-element anchor still; a "VFX chunk_A"; a fixed cell/scale contract; drawing every primitive in the scene's own light direction; drawing primitives *on top of the anchor chunk* and isolating them afterwards; shared primitives tinted per element (Hades: 112 of 126 god variants share a sheet).

#### 5. Your three candidate architectures
Sketch three end-to-end architectures (image side + runtime side + how time is produced + how a new skill enters), from most-image-model-heavy to least. For each: what the model paints; what the runtime does; where the size/timing spec lives; the cheapest experiment (≤ 12 images, ≤ 1 tooling burst) that would falsify it; the failure you most expect. Say which ONE you would build first and why.

#### 6. What you need from the conductor to do your part well
Brief shape, reference images, plates, canvas sizes, per-call caps, what NOT to ask you for. Be blunt about briefs like the three in `./evidence/briefs/` — what in them helped, what hurt.

Write the answer as a single Markdown document. No preamble, no summary of the task back to me.
