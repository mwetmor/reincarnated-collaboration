# VFX workflow architecture — the synthesis (proposal for Matt's ruling)

> **STATUS:** PROPOSAL — gandalf (ARCHITECT / SPEC-AUTHOR), 2026-09-15. Synthesis of the evidence dossier (`00-`), the pre-registered prior (`01-`), Astra design sessions 1 + 2 (`02a-`, `02c-`), and Legolas probes 1 + 2 (`legolas/research/2026-09-15-vfx-grammar-and-authoring-split/`, `…/2026-09-15-vfx-motion-sources-and-tooling/`). Session 3 (Astra red-team of this document) is appended as `02d-` and its accepted corrections are folded in place with `⟲` marks. **Not canon until Matt rules the § 8 forks**; on ruling, it becomes `canonical/reap-die-rise-game/painted-2d-pipeline/vfx-workflow.md` in the shape of `scene-builder-workflow.md`.

## 0. TL;DR

**The drawings were never the problem; the system around them was.** Both lanes that held share one shape — *the image model supplies a still; something else supplies time; structure is approved before paint; the anchor enters through the canvas; coherence is structural* — and the VFX lane had none of it. The architecture that follows is that shape applied to effects:

> **Grammar lives in the runtime. Primitives live in sheets. The anchor is a still. Time is never inferred from sheet order. Coherence is the layer stack.**

Concretely — three versioned contracts, one loop:

1. **`VfxSkillSpec`** — a *resolved* presentation spec per skill, assembled from emitted data + approved bindings (the emitted corpus is not yet a complete spec: two schemas, neither whole — § 2.1).
2. **Runtime grammar families** — eleven Godot 2D templates (F1–F11) plus three parameterisations (orbit, whirlwind, mortar-arc), each a timeline of events moving painted primitives, sharing one **invariant layer stack that Godot expresses natively** (`CanvasItemMaterial` particles + ADD/MIX/PREMULT blend modes; `PointLight2D` floor light). Flipbook-vs-runtime is a per-grammar **dial**, not a fork: *bake where internal shape changes and duration is fixed; compose where extent, direction, count or duration are data-driven* (Movie Maker mode bakes alpha PNG sequences deterministically).
3. **A painted primitive alphabet** — eight painted family assets + one shared painted puff + procedural constants, then 2–4 distinctive additions per element treatment, every one drawn against an **anchor package** derived from the scene itself, on a fixed scale contract (Keeper 130 px; 3-screen-px art step; 64 native px ≈ 1.5 BH).

The loop is the scene-builder's loop with a **VFX grey room** in step 2: a mode of the production Godot grammar scene with grey bodies, target dummies, aim rule and a scrubbed timeline — **Matt sees it as a 3-second clip before any painting** — and the approved instant becomes both the size/timing spec and the paint-over guide. The image model's contribution is bounded to what it has evidence of doing well: *designing painted shapes inside a visible, executable contract.*

First step is £0: prove the layer stack natively on one painted disc, bake it round-trip, spin a primitive 360°, and find the stepped-time point. Then E1 (procedural vs painted, one fire projectile, ≤ 8 images) and E2 (fire × ice, projectile × field — one language, ≤ 12 images).

## 1. Diagnosis — why two lanes held and one did not

The dossier's five invariants, amended by Astra (S1 § 1) and confirmed by the corpus (L1 § 2.2). These are the design constraints; every architecture element below cites the one it serves.

| # | Invariant | Scene lane | Character lane | VFX breadth test |
|---|---|---|---|---|
| I1 | **Structure before paint, and Matt sees the structure** (in motion, over the real scene) | grey room, R-C3-55a | dope sheet = spec, R-21 | none — the sheet was the first artifact |
| I2 | **An explicit owner for time.** The image model supplies stills; runtime, sim, video or authored animation owns temporal correspondence. *Time is never inferred from sheet order* (S1's amendment of "never drawn") | engine (parallax, particles) | video model + oracle cut | rows of a grid asked to be time (F4) |
| I3 | **Register enters through the canvas** — an anchor image in every brief; context painted into the input | chunk_A as IMAGE 2 | the seed as composite base | `references: []`, 400 words of prohibition (F8) |
| I4 | **Isolation, registration and scale enforced by construction** (plate + EDIT; projected size chart; recomposition over the original) | dress-then-isolate; ±25 % vs projected chart | one scale + one translation per clip | black void by prohibition (F5); size read off a 256-px cell (F3) |
| I5 | **Coherence is structural** — shared construction inherited before any new drawing; a fixed layer stack applied identically | one anchor, one exporter | one seed | six unrelated sheets + a style card (F11) |
| I6 | **Separate coverage, material and emitted light** (S1 addition) — a dark flask, a flame body, a puff and a glow cannot share one luminance→alpha rule | objects as coloured isolated sprites | — | the flask lost to highlights (F6) |
| I7 | **Judge the assembled effect at actual size and density** (S1 addition) — a successful sheet is an asset-source result, not a successful skill | Matt plays every version | Matt's eye on every loop | judged last, on the live build (F9) |

Failure attribution (S1 § 1): F1/F2/F6/F10/F11 **system-side**; F3/F5/F9 system + brief; F7/F8 brief; F4 model + system. The corpus adds the structural cause of F1: **the emitted corpus is projectile-and-field shaped because nine engine geometries (the melee/motion half) have never been emitted** (L1 § 1.2) — a cross-seam finding, § 9.

## 2. The architecture — three contracts

### 2.1 Contract I — `VfxSkillSpec` (resolved presentation spec)

**Why it exists.** Two emission artifacts, neither a complete spec (verified 2026-09-15):

| Artifact | Has | Lacks |
|---|---|---|
| `reincarnated-engine/data/kit_space/kits/*.json` (411 kits, 3,612 skills) | `geometry_type` (603 null), `spatial_geometry_type`, `canonical_element`, `role`, `cooldown_seconds`, `energy_cost`, `tier`, `chain_id`, prose `effects[]` | `effect_category`; typed radius / range / count / duration; typed effect params |
| `reincarnated-engine/seasons/*/classes/class_*.json` | `effect_category`, `canonical_pair_ref`, structured `effects[{name, params}]`, `color_value` | any geometry field |

Plus 87 emitted skills carrying `roll` / `persistent_zone` / `projectile` — values `VALID_GEOMETRY_TYPES` rejects with no alias (L1 § 1.2).

**The contract** (S2 § 5, adopted): conductor glue assembles, per skill, `schema_version · skill_id · source_revision · geometry_type_raw + normalized · family_id + variant_id · canonical_element · visual_treatment_id + palette_version · response_class · mechanics {origin/aim/target policy; footprint/range/width/count; travel or owner-motion; active duration/tick schedule/termination} · presentation {primitive bindings; body extents in BH; phase envelopes; allowed layers + budgets} · provenance (source path or approved override for every field)`. **Missing mechanics get explicit fixture values in experiments and block production registration until resolved** — the renderer never infers targeting or grammar from a skill name (S1 § 6 "what not to ask").

Two bindings are deliberately separate from the engine's vocabulary: **`visual_treatment_id ≠ canonical_element`** (the engine emits eight elements — earth, wind, water, fire, lightning, physical, shadow, holy; "ice" and "poison" are treatments bound explicitly, never renamed engine elements) and **`response_class ≠ element`** (`strike / field / aura_loop / channel / support / material` — "holy" is an element, not a time class; replaces T3v's `element_class: strike/field/holy`).

### 2.2 Contract II — runtime grammar families (the time owner)

**Source of truth for the taxonomy:** `agentic_orchestration/research/curated/corpus.db` (`motion_signature_registry` ×18, `vfx_archetype` ×27, `delivery_class` ×7) — read, not rebuilt (L1 § 1.0). Folded to eleven families (L1 § 1.3) + three parameterisations (S2 § 5):

| Family | Engine geometries | The one moving thing | Time band | Default dial |
|---|---|---|---|---|
| F1 Projectile | `single_target, multi_projectile, fork, ricochet_bounce` | a head that translates + a trail that lags | S at confirmed contact | runtime (head sprite, optional 3–4-frame boil loop, `trail_enabled`/`Line2D`) |
| F2 Self / body-attached | `self_buff, aura` | owner-anchored loop | **A** (to be measured) | runtime loop + `PointLight2D` |
| F3 Ground field | `ground_targeted_circle` (+ `persistent_zone` once aliased) | a decal + a loop that breathes/tiles for a rolled duration | **F** (to be measured) | runtime (patch + shader erosion/scroll) |
| F4 Displacement | `teleport, blink, defensive_dash, dash_attack, leap_strike` (+ `roll` once aliased) | owner silhouette streak + arrival flare | action clock; S only on damaging arrival | runtime |
| F5 Placed delegate | `totem` | nothing — the delegate carries its own grammar | spawn accent + A/F | — |
| F6 Chain hop | `chain` | a link drawn N times between N event-supplied point pairs | event-driven; S per small contact, centrally budgeted | runtime, necessarily |
| F7 Contact / radial | `circle, ring, ground_slam, melee_strike` | a radius that animates (ring) / a point contact (strike) | S | **flipbook** for the burst interior (Hades `RadialNova` = Book ×16) |
| F8 Cone / sweep | `cone, melee_arc`; whirlwind as parameterisation | an aperture that opens / a wedge that sweeps | action sweep + S; sustained = **C** | runtime |
| F9 Beam / channel | `beam_channel` | tileable mid + two caps, length = runtime distance | **C** (to be measured) | runtime, necessarily |
| F10 Vortex | `vortex_pull` | F7 with reversed radius | F/A (+ declared S collapse) | runtime |
| F11 Lane | `placed_lane`; `line` only with resolved delivery mode | a segment tiled to length | static = F; moving front = action + S | runtime |
| Orbit | `orbit` | anchor + revolve transform; payload = an F1 head | A + event contacts | F1 parameterisation |
| Whirlwind | `whirlwind` | owner rotation + swept F8 wedge | A/C | F8 parameterisation |
| **Mortar arc** | *no engine geometry* — explicit delivery binding | `screen = project(ground(t)) − up·height(t)`; landing → F3 | ballistic + landing accent + F | **composition F1 + F3**, not a twelfth family (S2 § 5 mortar decision) |

**Frozen Orb** is likewise an explicit composition (travelling F1 emitter + scheduled child emissions) — the name must not auto-select owner-centred `orbit` (S2).

**The dial rule** (L2 Q3b): *bake a flipbook where the shape changes internally and the duration is fixed; compose at runtime where extent, direction, count or duration are data-driven.* Every parameter our generator rolls is on the runtime side by construction. Movie Maker mode (`--write-movie out.png --fixed-fps N` + `Rendering > Transparent Background` + `use_fixed_seed`) makes the dial reversible: any procedural effect bakes to an alpha PNG sequence for a paint pass and re-imports as a flipbook (L2 Q3a, VERIFIED).

**Validation rejects, never defaults to a projectile** (S2 § 5 per-family rules): missing speed/range/count; unspecified fork/bounce; missing owner/expiry; ambiguous `line`; `melee_strike` inventing a ground nova; a visual lob concealing an instant field; defensive movement inheriting damaging hits.

**Time bands by class** — `strike_fast_v1` (Hades: peak 0–1 frames, half in 2–7, residue 0.3–1.0 s) and `strike_splash_v1` (body peaks ~6 frames after flash) exist; **`field_v1`, `aura_loop_v1`, `channel_v1`, `action_motion_v1` must be measured** — until then, named Matt-approved fixture envelopes with provenance labels. ⟲ This dissolves the deferred "hybrid oracle" fork (R-C3-118/120): the Hades strike bands and the CoM/Slormancer legibility rules are both adopted, *scoped by class*, and the persistent classes get their own measured bands rather than borrowed strike bands.

**The invariant layer stack — shared implementations, not every switch on** (S2 § 5; L2 § 1.2): body (index-tinted) · halo · floor light (`PointLight2D`) · optional dark duplicate (same sheet, MIX black — a *deliberate per-preset option*, never inherited) · contact flash (≤ 0.1 s, strong strikes only) · residual decal · centrally-arbitrated hit-stop/shake (no two effects fighting over `Engine.time_scale`) · victim tint. Presets: ordinary strike (flash off) · strong strike · field/aura/channel tick (flash, hit-stop, shake, dark duplicate **off**) · healing tick (no white flash, scorch, shake or hit-stop) · material object (alpha-blended, lit by separate emission). Godot expresses the whole stack natively — sibling `GPUParticles2D` on one texture with `particles_animation` + `blend_mode`, `light_mode` excluding the additive body from the 2D light pass (L2 VERIFIED). **No second effect system** (Effekseer rejected: two blend/timing/tint models = a coherence cost).

### 2.3 Contract III — the painted primitive alphabet (the still owner)

**Scale contract** (S1 § 4, S2 § 3): Keeper = 130 screen px = 1 BH; effect **art step 3 screen px** (Matt rules it in motion at E1); 64 native px ≈ 1.5 BH; a 3–6 BH burst = 130–260 native px of *assembled* extent, never a silently enlarged brush. Camera yaw 47° / pitch 52.95° in calibration; **0.58 ground squash applied once, to unprojected ground geometry only**; ground-plane rotation before projection; upright bodies never squashed; already-projected paint-overs never projected again. Canvas dimensions are storage metadata, not the size spec.

**Encoding rule** (S1 § 2d): greyscale **value-index map + independent alpha** by default (index 0 may be fully opaque; no threshold converts dark pixels to transparency; no source level auto-preserved as rendered white — `white_core_keep` removed); RGB + material palette only for opaque material objects (the flask) or deliberately multicoloured signatures. Store exact index levels (e.g. 0/85/170/255) identically in RGB; density in a separate declared channel where needed.

**Light rule** (S2 § 4; L2 constraint 1): emissive bodies are **self-lit** (value structure follows the energy form, so rotation does not rotate a painted sun highlight); material objects are **scene-lit** with rotation restricted (flask: tilt ≤ 10°, upright, no tumble unless commissioned); ambient material planes for shards that rotate.

**The build list** (S2 § 4, adopting L1 § 1.4's eleven functional slots as *slots*, not eleven compulsory drawings):

| Painted family assets (8) | Procedural / derived (6) | Shared painted (1) |
|---|---|---|
| P01 head/core 128² · P02 tapered streak/wisp 192×128 · P03 field body 256² · P04 residue/decal 256² (= C3) · P05 chain link 192×128 with restored endpoint strips · P06 broken ring segment 256² · P07 wedge/slash/impact tooth 128² · P11 lane segment 192×128 | P08 beam middle (procedural banded strip; painted only if it fails beside P05/P07) · P09 beam cap (derived from P01) · P10 inward swirl (arrangement of P02/P06) · S02 mote/spark 16² · C1 cast/contact flash mask · C2 halo/floor-light mask · C4 dark duplicate (the source's own alpha) · C5 victim response (no asset) | S01 bounded puff 128² (density + coverage) |

Per-element additions, 2–4 each, drawn on profiles T (tongue/petal) · J (junction/crown) · D (density puff) · M (flask, RGB, scene-lit) · R (shard/husk) · G (seal/patch) · W (long wisp/prong): fire — hooked tongue, oil flask; ice — faceted shard, broken frost crown, angular puff; poison — viscous lobe, lobed puff, poison flask (derived); lightning — branch junction, needle prong; holy — folded ray/petal, interrupted seal; sixth treatment (proposed **shadow** — present in the emitted corpus; tests dark bodies with independent alpha) — hooked wisp, hollow husk. **Flasks belong to thrown alchemical skills, not to elements.** Procurement checkpoint at ~12 unique painted assets per treatment (Hades median 12.5, range 4–26 — an order of magnitude, not a cap).

**The anchor package ("VFX chunk_A")** (S2 § 3): three approved constructions — directional, radial, ground-bound — each as (a) a paint-over of a *runtime blockout instant over the real scene*, (b) the isolated, registered, quantised native body, (c) a nearest-neighbour enlargement, plus a tool-assembled layer-stack board, a scale-and-attachment board and a palette/roles board — 17 images, of which a production brief receives **three**: its geometry/edit guide, the relevant approved exemplar, the scene/scale board. **The accepted anchor is the recomposed runtime capture, not the raw paint-over** — a beautiful paint-over the renderer cannot reproduce is not an anchor. Elements 2–6 begin as tool-recoloured versions of the same three constructions, then receive their distinctive silhouettes; they must remain distinguishable with glow disabled.

**Brief discipline** (S1 § 6, S2 § 6 — three complete templates exist: fire tongue, chain link, blockout paint-over): one production primitive per call; one edit objective per call; one diagnosed retry then change representation; three images with stated roles; asset role stated first (opaque object / banded body / density / ground patch / emission-only); what the exporter enforces stated; retry criteria on *usefulness* (bounds ±10 %, pivot ≤ 1 native px, interior openings survive reduction, no external haze) not file appearance. Never ask the model for exact RGB, alpha topology, twelve registered frames from percentages, targeting inferred from a name, a matte across mixed material, or a repair of an undefined runtime through more emphatic prose.

**Extraction contract** (S2 § 6): genuine RGBA first, channel-inspected (≥ 99 % of declared solid interior at α ≥ 0.98 for hard bodies; recomposition over black/white/dirt/foliage with ≤ 1 native-px fringe); fallback = one diagnosed EDIT onto a flat key plate (green; magenta for green subjects) + deterministic keying; if both fail, split the asset — never a third drive at the same mixed subject. Recompose over the *exact original capture* with the recorded transform (no tight-bbox pivot, no recentering, no silent rescale). Straight-alpha PNG at interchange; premultiply exactly once at runtime, blend mode declared.

## 3. The loop (bringing a family online → adding a skill)

Condensed from S2 § 1; the canon doc carries the full tables.

| Step | Who | Matt sees |
|---|---|---|
| 1 Resolve the family contract (`VfxSkillSpec` fields, variants, blocked items) | conductor glue | only identity-changing questions |
| 2 **VFX grey room** — a mode of the production grammar scene: grey bodies, dark material placeholders, target dummy (+3 for chain/fan/pierce/density), footprint / body / light envelopes, origin socket, aim rule, scrub timeline, real-ground toggle; labels in BH | drax against gandalf spec | **3-second clip at gameplay speed** (origin → path → hit legible? big enough? contact a distinct event? duration right? ground component follows its owner?), then live scene for aim-while-moving / reverse mid-cast / walk through a field / lose a chain target / cancel / cold first cast |
| 3 Approve structure; tooling captures guides (timestamped body masks, anchors, scene captures; blockout hash + camera + BH conversion recorded) | Matt → glue | — |
| 4 Establish the family's painted appearance — **paint-over of the approved instant** (mid-travel; first full contact body with flash disabled; field after activation settles; chain frame with two links; melee at max extension) | Astra GENERATE (EDIT) | actual-size still beside the grey instant |
| 5 Produce only the *missing* primitives, one per call | Astra GENERATE | native enlargement + actual-size placement |
| 6 Extract, register, compile (§ 2.3 contract) | Astra TOOLING → CHECK | exceptions only |
| 7 Assemble the moving effect; single + four-cast captures; event + perf traces | drax + glue | **clips over bright dirt and foliage, then live playtest** |
| 8 Freeze + publish the family package (presets, hashes, schema versions, regression fixture) | Astra PACK; ruling ledgered | ruling names the accepted build |

Adding a skill: bind emitted data → preview with existing assets (grey/painted toggle, 3-second clip) → fill a genuine alphabet gap only if the existing primitives cannot express the distinction (normally **zero images**) → register + regress against tripwires. Month-six coherence is *earned by reuse*: a new skill that needs a new palette, art step, material mode, layer preset, > ±15 % deformation, recurring flash to read, or a one-off asset without a demonstrated gap **triggers review** (S2 § 7 tripwires).

## 4. Coherence QA

Three measured outputs — body/coverage pass (index bands, silhouette, attachments, native feature size), light-only pass (halo + floor envelopes), final composite (readability, clipping, four-cast accumulation) — the oracle consuming runtime coverage/ID masks, not brightness diffs. Class-specific gates (S2 § 7): strike vs the named Hades subtype; field boundary ≤ 10 % / activation-expiry within one tick / no residual presented as hazard; aura attachment ≤ 1 native px, no drift, calm-loop area modulation ≤ 15 %; channel endpoints ≤ 1 px, width ±10 %, stop within one tick. **After-compositing white**: `V > 0.95 ∧ S < 0.20`, reported over the full combat crop *and* effect pixels, flash on/off, baseline subtracted explicitly; gate ≤ 2 % of the combat crop at four simultaneous casts (CoM/Slormancer's 0.1 % is the aspiration). Halo/floor lifts (+.16–.41 / +.07–.09) are reference observations; on bright ochre choose the lower safe gain — measure the transfer, never clip to satisfy an imported number.

**Matt's fixture, every family:** bright dirt + foliage; one cast; four casts synchronised and staggered; Keeper walking through; a dummy overlapping the ground body; body-only toggle; eight directions; cold first cast, repeat, cancel. Rulings: *same world · grammar reads before the glow · element identifiable · large enough without obscuring the fight · world response adds weight · painted planes, not stretched stickers.* Performance tripwire: four-cast frame time +2 ms p95 on the Mac mini.

## 5. What changes vs the breadth test (T3t/T3u/T3v amendments)

1. Versioned primitive manifest + grammar binding replace the mandatory four-phase sheet. 2. Palette lookup; `white_core_keep` removed. 3. Alpha, density, material, emission handled independently. 4. Explicit rendering plane + projection state per asset. 5. Explicit phase-size metadata replaces `phase_scale` multipliers. 6. Class/role response presets replace `element_class`. 7. Runtime grammar scenes replace unconditional bolt/impact generation. 8. Central hit-stop/shake arbitration. 9. Effect-age clock + event timestamps (shader `TIME` is not a lifecycle clock). 10. Legacy tint arrays and the v3 tint object get separate tested migrations; an unversioned hybrid fails validation. Plus the runtime defects already logged: first-cast warm-up (cast-ready gate), untinted particles (T3v), flash alpha.

## 6. Experiments (gates pre-registered)

**E0 — £0, no images, ~half a day (L2 "cheapest first experiments" 1–4).** (a) *Layer-stack proof*: one 128-px greyscale painted disc; sibling `GPUParticles2D` ADD (hue-modulated) + MIX black beneath at ~1.05×; 0.1 s quickflash; `PointLight2D` floor light; 3 s decal — does one painted shape read as a finished effect at our register? (b) *Bake round-trip*: `Rendering > Transparent Background` + `use_fixed_seed` + `--write-movie bake/fx.png --fixed-fps 30` → alpha PNGs → Spritesheet Generator → flipbook; A/B against live — is the dial real? (c) *Rotation survival*: spin one painted head 360° — where does paint read as a rotating drawing? (bounds H-A; the one thing the corpus never tests). (d) *Stepped time*: `fixed_fps` 30 → 15 → 12 → 8, `interpolate` off — where is our Guilty Gear Xrd point? **Pixel FX Designer ($14.96) only after E0 lands.**

**E1 — procedural vs painted, one motion (S2 § 8).** F1 fire projectile on the grey-room fixture (context 0.25 s → anticipation 0.15 → travel 0.5 s over 4 BH at 8 BH/s, body 1.2 BH → contact ≤ 1 tick → half-peak ~4 ticks → residue 0.6 s; impact envelope 3 BH, Matt-judged). A = procedural head/streak/wedge with banded materials; B = painted equivalents bound to the *same* events, seed, palette, light stack. ≤ 8 images (anchor paint-over 1 · head 1 · streak 1 · tongue 1 · wedge 1 · repairs/fallbacks 3); one TOOLING burst ≤ 40 min; drax builds the fixture. Technical gates: same events within one tick; extents ±10 %; pivots ≤ 1 native px; matte halo ≤ 1 px; first impact present; four-cast white ≤ 2 %; perf baseline. **Matt's ruling** on five order-randomised A/B pairs: painted preferred ≥ 4/5 and at the bar → **retain B**; procedural at the bar and preferred/indistinguishable ≥ 4/5 → **C becomes default**; painted loses register under required motion after the permitted repair → **abandon primitive-only B, test authored key states**; both fail → fix the fixture, no evidence for B.

**E2 — two grammars × two elements, one language.** Fire/ice × F1 projectile/F3 ground field (field directly placed; mortar/flask deferred so coherence is not confounded with a new material + trajectory). ≤ 12 images. Fixture: four 3-second clips at one scale; dirt + foliage; four-cast synchronised + staggered; Keeper through the field and behind dressing; body-only / full-stack toggles. **Matt's three verdicts:** one language? · distinct identities without the glow? · a travelling strike clearly unlike a persistent field? A cell that passes only with its own layer stack or brush scale fails coherence even if it is pretty.

## 7. What the consultation changed (scorecard, final)

A-1 confirmed · A-2 partial (RGBA-first; "paint the shape representing emission, light is a runtime layer" is the fix for haze, not a plate colour) · A-3 refined (value-index + alpha; F6 was a pipeline defect) · A-4 refined (package, not still; recomposed capture is the anchor) · A-5 confirmed · A-6 confirmed · L-1 confirmed on emitted / refuted on reference · L-2 confirmed strongly · L-3 **confirmed** (Godot native scores 29/30; EmberGen Windows-only; Blender at its stated minimum; Houdini 50 GB; Effekseer = second stack) · L-4 **confirmed** (no hosted RGBA video; every commercial endpoint returns opaque RGB; an effect *is* the transparency). Where the prior was wrong: coherence = layer stack not alphabet size; the grey room doubles as paint-over guide; the taxonomy is read not built; my own brief carried a third geometry vocabulary; the emitted data is not a complete spec.

## 8. Forks for Matt — ELICITOR, one recommendation each

| # | Fork | **Recommendation** | Options / tradeoffs |
|---|---|---|---|
| V1 | **Medium / route** | **B provisionally** (shared painted primitives + runtime grammars), with E1's pre-registered exits to C (procedural default) or authored key states | A (guided key-state animation): most image-model-heavy, per-sequence cost, boil risk · C: cheapest, "vector graphics" risk · B: bounded model task with evidence of success |
| V2 | **Effect art step** | **3 screen px**, ruled *in motion* at E1 | 2 px reads finer but nearer the scene grid; 4 px reads retro (CrossCode pole Matt declined) |
| V3 | **Sequencing** | **E0 (£0) → grey room + dummies → E1 → E2**; no sheet before a grey-room clip is approved | Skipping E0 saves half a day and forfeits the cheapest falsification of the stack thesis |
| V4 | **Hybrid oracle (R-C3-118/120)** | **Dissolve into class bands**: Hades strike bands + CoM/Slormancer legibility, scoped per class; measure `field/aura/channel/action` bands as their own lap | Keep as one blended oracle (mis-scores fields against strike curves, as CAST already did at R-C3-106) |
| V5 | **Treatment roster** | six treatments = fire · ice · poison · lightning · holy · **shadow**, with `visual_treatment_id` bound explicitly to engine elements (ice→water?, poison→?) — **rule the bindings** | a fifth-element-only roster; or the engine's eight literally |
| V6 | **Flask + lob for alchemical skills** | **keep** — upright translated flask (tilt ≤ 10°), mortar-arc composition; buy tumble views only if Matt wants tumbling | a ground flare alone omits the throw (skill identity lost) |
| V7 | **Register: white and separation** | bodies white-free; white only as ≤ 0.1 s strong-contact flash; **halo + floor light default, dark duplicate an approved exception** | dark duplicate default (Hades) — costs additive headroom on ochre ground |
| V8 | **Video-generation spend for VFX** | **NO** — no alpha, no keyable plate, no shipped precedent; video stays a *watched* timing/shape oracle at most | the $20 six-still bake-off stays a *character* question (Q-pending) |
| V9 | **Pixel FX Designer ($14.96)** | **after E0**, for primitive authoring only | before: buys output the consuming stack has not yet proved |
| V10 | **Coverage denominator** | plan against the **reference** corpus (53 % at six families) and treat the unemitted melee/motion half as engine debt to route — require a melee sweep + displacement fixture before calling the architecture complete | plan against emitted (88 %) and be surprised when melee lands |
| V11 | **Signature flourish** | first test a restrained world response (brief floor light + one characteristic residual motion) before any ornamental motif | attach a motif to every spell now (the death-faith "reap" candidate in style-card v0.1 is dead with the frame) |
| V12 | **Grey-room ownership** | drax builds it as a *mode of the production grammar scene* against a gandalf SCENEWRIGHT spec; not conductor glue | a separate mock leaves the runtime untested |

## 9. Cross-seam routing (engineering blockers, not artistic forks — route via KR)

- **rocket:** nine geometries never emitted (`melee_strike, melee_arc, ground_slam, dash_attack, whirlwind, leap_strike, aura, orbit, placed_lane` — 31 % of the reference corpus) · `roll` / `persistent_zone` / `projectile` values in 87 emitted skills with no validator alias · no typed radius/range/count/duration in `kit_space` skills · `geometry_type` null on 603 skills.
- **star-lord / rocket:** two emission schemas (`kit_space` vs `seasons/classes`) — which is the VFX-facing artifact, and can `effect_category` + structured `effects` + geometry land in one?
- **elrond:** Last Epoch — 37 corpus kits, zero banded rows (LE dossiers exist at `legolas/research/la-postcutoff-dossiers-2026-07-16/`); `mortar_arc` has zero archetype members (GD BWC banded as `ground_targeted_circle`, losing the arc).
- **jack-ryan:** Gate-1 on this proposal before any run charter; the E1/E2 gates are pre-registered here.

## 10. Provenance

Dossier `00-evidence-dossier.md` · prior `01-conductor-prior.md` · scorecard `02b-` · Astra S1 `02a-` (115 k tokens) · Astra S2 `02c-` (100 k) · Astra S3 red-team `02d-` · Legolas L1 `…/2026-09-15-vfx-grammar-and-authoring-split/findings.md` · L2 `…/2026-09-15-vfx-motion-sources-and-tooling/findings.md` · prior research 2026-09-14/15 (oracles, atlas, CoM/Slormancer/Chronicon, video-generation) · C-3 ledger R-C3-81…123 + notes · `corpus.db` tables · `geometry_derivation.py:42` · `kit_space/kits/*.json` · `seasons/season_000046/classes/`.

— gandalf (ARCHITECT / SPEC-AUTHOR), 2026-09-15
