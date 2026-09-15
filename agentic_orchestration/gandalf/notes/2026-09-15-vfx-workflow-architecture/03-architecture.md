# VFX workflow architecture — the synthesis (proposal for Matt's ruling)

> **STATUS:** PROPOSAL v2 — gandalf (ARCHITECT / SPEC-AUTHOR), 2026-09-15. **Re-scoped on Matt's correction** (verbatim: *"Constraining our VFX production pipeline around a content generator we haven't ran in months before we even know if we can develop a VFX workflow at all is illogical."*). **GOAL = develop a workflow that can generate VFX similar to the 6 selected VFX, within a register similar to our 2D scene.** Nothing in this document depends on the content generator, the emitted corpus, or the engine's geometry palette; everything generator-adjacent from v1 is parked in `04-parked-generator-coupling.md` and constrains nothing here. Inputs: dossier `00-`, prior `01-`, Astra sessions `02a-`/`02c-` (+ `02d-` red-team), Legolas probes 1 + 2. Not canon until Matt rules § 7.

## 0. TL;DR

**The drawings were never the problem; the system around them was.** Both lanes that held share one shape — *the image model supplies a still; something else supplies time; structure is approved before paint; the anchor enters through the canvas; coherence is structural* — and the VFX breadth test had none of it. The workflow below is that shape applied to six effects:

> **Grammar lives in the runtime. Primitives live in sheets. The anchor is a still. Time is never inferred from sheet order. Coherence is the layer stack.**

- **Time owner:** Godot itself. The Hades layer stack (additive painted body + black MIX duplicate of the same sheet + flash + floor light + decal) is expressible natively as sibling `GPUParticles2D` on one texture (`CanvasItemMaterial.particles_animation` + `blend_mode` + `light_mode`; `PointLight2D` for the floor light) — Legolas probe 2, VERIFIED. Movie Maker mode bakes deterministic alpha PNG sequences, so flipbook-vs-runtime is a per-effect **dial**, not a fork.
- **Four motion grammars cover the six skills** (§ 2.2), each a timeline of events moving painted primitives; parameters (range, speed, radius, duration, hop count) hand-entered per skill from the source game — **six hand-authored skill specs, no engine dependency.**
- **Still owner:** Astra paints a small primitive alphabet (≈ 8 shared shapes + 2–4 per element, five elements) against an **anchor package derived from the scene itself**, on a fixed scale contract, one primitive per call, three images per brief.
- **Structure before paint:** a **VFX grey room** — grey bodies moving in the live cliffside with a target dummy and an aim rule — **Matt sees a 3-second clip before any painting**; the approved instant becomes both the size/timing spec and the paint-over guide.
- **First step is £0** (E0: prove the stack natively on one painted disc; bake it round-trip; spin a primitive; find the stepped-time point), then E1 (procedural vs painted, one fire projectile, ≤ 8 images), then E2 (fire × ice, projectile × field — one language, ≤ 12 images), then the six.

## 1. Diagnosis — why two lanes held and one did not

| # | Invariant | Scene lane | Character lane | VFX breadth test |
|---|---|---|---|---|
| I1 | **Structure before paint, and Matt sees the structure** in motion over the real scene | grey room (R-C3-55a) | dope sheet = spec (R-21) | none — the sheet was the first artifact |
| I2 | **An explicit owner for time.** The image model supplies stills; *time is never inferred from sheet order* | engine (parallax, particles) | video model + oracle cut | rows of a grid asked to be time (F4) |
| I3 | **Register enters through the canvas** — an anchor image in every brief | chunk_A as IMAGE 2 | the seed as composite base | `references: []`, 400 words of prohibition (F8) |
| I4 | **Isolation, registration, scale by construction** | dress-then-isolate; ±25 % vs projected chart | one scale + one translation per clip | black void by prohibition (F5); size off a 256-px cell (F3) |
| I5 | **Coherence is structural** — shared construction inherited before any new drawing; one layer stack applied identically | one anchor, one exporter | one seed | six unrelated sheets + a style card (F11) |
| I6 | **Separate coverage, material and emitted light** (Astra) | objects as coloured isolated sprites | — | the flask lost to highlights (F6) |
| I7 | **Judge the assembled effect at actual size and density** (Astra) | Matt plays every version | Matt's eye on every loop | judged last, on the live build (F9) |

Failure attribution (Astra S1): F1/F2/F6/F10/F11 system-side; F3/F5/F9 system + brief; F7/F8 brief; F4 model + system. The route order the research recommended (procedural → hybrid → video → sheets) was skipped; procedural was never run (F10).

## 2. The workflow — three contracts

### 2.1 Contract I — the skill spec (six hand-authored files)

One `VfxSkillSpec` per selected skill, written by the conductor from the source game and Matt's intent — **no field is read from the generator**:

`skill_id · source_game + skill name · grammar (§ 2.2) · element treatment (§ 2.3) · response_class (strike / field / aura_loop / material) · mechanics {origin socket; aim rule; range / speed / radius / count / hop count; travel or ballistic params; active duration + tick schedule; termination} · presentation {primitive bindings; body extents in BH; phase envelopes; enabled layers} · provenance (source-game observation or Matt ruling per field)`.

Aim rules (one per skill): release-locked · owner-tracking · ground-locked · target-tracking · event-linked (chain). The renderer never selects targets or infers grammar from a name; the grey-room fixture supplies hits, targets and expiry through the same interface a game would.

| Skill | Grammar | Treatment | Response | Mechanics to enter (from the source game) |
|---|---|---|---|---|
| Frozen Orb (D2) | **G1 projectile** + scheduled child emission (orbiting bolt emitter; shards on expiry) | ice | strike | speed, range, emission schedule, shard count, expiry burst radius |
| Blackwater Cocktail (GD) | **G2 thrown arc → ground field** | fire + **material flask** | material → field | apex/flight time, target range, pool radius, burn duration, tick |
| Poisonous Concoction (PoE) | **G2 thrown arc → ground field** | poison + material flask | material → field | as above; cloud vs pool density |
| Lightning Blast (LE) | **G3 instant bolt / chain** (single hop) | lightning | strike | instant, range, width, optional chain count |
| Zeus chain (Hades) | **G3 instant bolt / chain** (N hops) | lightning (Hades dialect) | strike per hop | hop count, hop delay, link lifetime, target order = events |
| Healing Hands (LE) | **G4 self-aura loop** | holy | aura_loop (support preset) | radius, duration, pulse period, stack/refresh |

### 2.2 Contract II — four runtime grammars (the time owner)

Grammar = a Godot 2D template: a timeline of events (anticipation → onset → peak → decay → residue, or activation → active ticks → deactivation) that moves painted primitives with engine transforms. Direction is runtime rotation, never baked facings (Hades; the D2 control case bakes 8/16/32 directions and ships 366 of 684 missiles single-direction). *(The corpus taxonomy in `corpus.db` — 18 motion signatures, 27 archetypes — is reference for naming these; it is not a constraint. Full eleven-family table parked in `04-`.)*

| Grammar | The one moving thing | Time band | Dial |
|---|---|---|---|
| **G1 Projectile (+ emitter)** | a head that translates + a trail that lags; optional scheduled child emissions | `strike_fast_v1` at confirmed contact | runtime (head sprite, optional 3–4-frame boil loop, `trail_enabled` / `Line2D`); **burst interior = flipbook** |
| **G2 Thrown arc → field** | `screen = project(ground(t)) − up·height(t)`; landing accent; then a decal + a loop that breathes for a fixed duration | ballistic + landing + `field_v1` (**to be measured**) | runtime; flask = upright RGB material sprite, tilt ≤ 10°, no tumble unless commissioned |
| **G3 Instant bolt / chain** | a link primitive drawn N times between N event-supplied point pairs (N = 1 for a single bolt) | event-driven; `strike_fast_v1` per contact, centrally budgeted | runtime, necessarily |
| **G4 Self-aura loop** | owner-anchored ring/dome loop + floor light; pulse per tick | `aura_loop_v1` (**to be measured**) | runtime loop |

**The dial rule** (probe 2): *bake a flipbook where the shape changes internally and the duration is fixed; compose at runtime where extent, direction, count or duration vary.* Movie Maker (`--write-movie out.png --fixed-fps N`, `Rendering > Transparent Background`, `use_fixed_seed`) makes it reversible.

**Time bands:** `strike_fast_v1` (Hades, measured: peak 0–1 frames, half in 2–7, residue 0.3–1.0 s) and `strike_splash_v1` exist; **`field_v1` and `aura_loop_v1` must be measured** (their own lap) — until then, named Matt-approved fixture envelopes. ⟲ This dissolves the deferred "hybrid oracle" fork (R-C3-118/120): Hades strike bands + CoM/Slormancer legibility rules, each **scoped by class**.

**The invariant layer stack — shared implementations, not every switch on:** body (index-tinted) · halo · floor light (`PointLight2D`) · dark duplicate (same sheet, MIX black — an *approved per-preset option*, not a default) · contact flash ≤ 0.1 s (strong strikes only) · residual decal · centrally arbitrated hit-stop/shake · victim tint. Presets: ordinary strike (flash off) · strong strike · field/aura tick (flash, hit-stop, shake, dark duplicate **off**) · healing tick (no white flash, scorch, shake, hit-stop) · material object (alpha-blended; lit by separate emission). Effect-age clock + event timestamps drive lifecycles (shader `TIME` is not a lifecycle clock). **No second effect system** (Effekseer rejected).

### 2.3 Contract III — the painted primitive alphabet (the still owner)

**Scale contract:** Keeper = 130 screen px = 1 BH; effect art step **3 screen px** (Matt rules it in motion at E1); 64 native px ≈ 1.5 BH; a 3–6 BH burst = 130–260 native px of *assembled* extent, never a silently enlarged brush. Camera yaw 47° / pitch 52.95° in calibration; **0.58 ground squash once, to unprojected ground geometry only**; ground rotation before projection; upright bodies never squashed; paint-overs of projected captures never projected again.

**Encoding:** greyscale **value-index + independent alpha** (index 0 may be opaque; no threshold makes dark pixels transparent; `white_core_keep` removed); RGB + material palette only for opaque material objects (the flasks). **Light rule:** emissive bodies self-lit (rotation must not rotate a painted highlight); material objects scene-lit, rotation restricted; ambient planes for shards.

**Build list** (Astra S2 § 4 over Legolas § 1.4 — slots, not compulsory drawings):

| Painted shared (8 + 1) | Procedural / derived |
|---|---|
| P01 head/core 128² · P02 tapered streak/wisp 192×128 · P03 field body 256² · P04 residue/decal 256² · P05 chain link 192×128 (endpoint strips restored by tooling) · P06 broken ring segment 256² · P07 wedge/impact tooth 128² · S01 bounded puff 128² (density + coverage) | S02 mote/spark 16² · C1 flash mask · C2 halo/floor-light mask · C4 dark duplicate (source alpha) · C5 victim tint (no asset) |

Per-element additions, 2–4 each, on profiles T tongue/petal · J junction/crown · D density puff · M flask (RGB, scene-lit) · R shard/husk · G seal/patch · W long wisp/prong: **fire** hooked tongue, oil flask · **ice** faceted shard, broken frost crown, angular puff · **poison** viscous lobe, lobed puff, poison flask (derived from the fire flask with its own material palette) · **lightning** branch junction, needle prong · **holy** folded ray/petal, interrupted seal. Flasks belong to the two thrown skills, not to elements. Review at ~12 unique painted assets per treatment (Hades per-god median 12.5, range 4–26 — an order of magnitude, not a cap).

**Anchor package ("VFX chunk_A"):** three approved constructions — directional (G1), radial (contact burst), ground-bound (G2 field) — each as (a) a paint-over of a *runtime blockout instant over the real scene*, (b) the isolated, registered, quantised native body, (c) a nearest enlargement; plus tool-assembled layer-stack, scale/attachment and palette/roles boards (17 images; a production brief receives **three**: geometry/edit guide, approved exemplar, scene/scale board). **The accepted anchor is the recomposed runtime capture, not the raw paint-over.** Elements 2–5 begin as tool-recoloured versions of the same three constructions, then receive their distinctive silhouettes; they must remain distinguishable with glow disabled. Bootstrap order: fire (G1) → ice → poison → lightning → holy.

**Brief discipline** (Astra S1 § 6 / S2 § 6 — three complete templates exist: fire tongue, chain link, blockout paint-over): one production primitive per call; one edit objective; one diagnosed retry then change representation; three images with stated roles; asset role stated first; exporter responsibilities stated; retry criteria on usefulness (bounds ±10 %, pivot ≤ 1 native px, interior openings survive reduction, no external haze). Never ask for exact RGB, alpha topology, twelve frames from percentages, a matte across mixed material, or a runtime fix by more emphatic prose. Haze fix is representational: *"paint the opaque banded body representing the emission; light spill is a separate runtime layer"* — not a plate colour.

**Extraction contract:** genuine RGBA first, channel-inspected (≥ 99 % of declared solid interior at α ≥ 0.98; ≤ 1 native-px fringe over black/white/dirt/foliage); fallback = one diagnosed EDIT onto a flat key plate (green; magenta for green subjects) + deterministic keying; if both fail, split the asset. Recompose over the *exact original capture* with the recorded transform (no tight-bbox pivot, no recentering). Straight-alpha PNG; premultiply once at runtime.

## 3. The loop

| Step | Who | Matt sees |
|---|---|---|
| 1 Write the skill spec (§ 2.1) | conductor | identity questions only |
| 2 **VFX grey room** — a mode of the production grammar scene in the cliffside: grey bodies, dark material placeholders, target dummy (+3 for chain/density), footprint / body / light envelopes, origin socket, aim rule, scrub timeline, labels in BH | drax against gandalf spec | **3-second clip at gameplay speed** — origin → path → hit legible? big enough? contact a distinct event? duration right? ground component follows its owner? — then live: aim while moving, reverse mid-cast, walk through a field, lose a chain target, cancel, cold first cast |
| 3 Approve structure; tooling captures guides (timestamped body masks, anchors, scene captures; blockout hash + camera + BH conversion) | Matt → glue | — |
| 4 **Paint-over of the approved instant** (mid-travel; first full contact body, flash disabled; field after activation settles; chain frame with two links) | Astra GENERATE (EDIT) | actual-size still beside the grey instant |
| 5 Produce only the *missing* primitives, one per call | Astra GENERATE | native enlargement + actual-size placement |
| 6 Extract, register, compile (§ 2.3 contract) | Astra TOOLING → CHECK | exceptions only |
| 7 Assemble the moving effect; single + four-cast captures; event + perf traces | drax + glue | **clips over bright dirt and foliage, then live playtest** |
| 8 Freeze + publish the package (presets, hashes, regression fixture) | Astra PACK; ruling ledgered | ruling names the accepted build |

Adding a later skill to a proven grammar: spec → preview with existing assets (grey/painted toggle) → fill a genuine alphabet gap only if the existing primitives cannot express the distinction (normally **zero images**) → regress against tripwires.

## 4. Coherence QA

Three measured outputs — body/coverage (index bands, silhouette, attachments, native feature size), light-only (halo + floor envelopes), final composite (readability, clipping, four-cast accumulation) — the oracle consuming runtime coverage masks, not brightness diffs. Class gates: strike vs the named Hades subtype; field boundary ≤ 10 %, activation/expiry within one tick, no residue presented as hazard; aura attachment ≤ 1 native px, no drift, calm-loop area modulation ≤ 15 %. **After-compositing white:** `V > 0.95 ∧ S < 0.20` over the combat crop and over effect pixels, flash on/off, baseline reported separately; gate ≤ 2 % of the crop at four simultaneous casts (CoM/Slormancer 0.1 % is the aspiration). Halo/floor lifts (+.16–.41 / +.07–.09) are reference observations — on bright ochre choose the lower safe gain, never clip to hit an imported number.

**Matt's fixture, every effect:** bright dirt + foliage; one cast; four casts synchronised + staggered; Keeper walking through; a dummy overlapping the ground body; body-only toggle; eight directions; cold first cast, repeat, cancel. Rulings: *same world · grammar reads before the glow · element identifiable · large enough without obscuring the fight · world response adds weight · painted planes, not stretched stickers.* Tripwires for any later addition: new palette / art step / material mode / layer preset; > ±15 % deformation of a reusable primitive; exceeds the approved BH or light envelope; adds white via overlap; needs recurring flash to read; one-off asset without a demonstrated gap; passes a still but fails direction changes or four-cast playback; four-cast frame time +2 ms p95 on the Mac mini.

## 5. What changes vs the breadth test (T3t/T3u/T3v amendments)

Versioned primitive manifest + grammar binding replace the four-phase sheet · palette lookup, `white_core_keep` removed · alpha / density / material / emission independent · explicit rendering plane + projection state per asset · phase-size metadata replaces `phase_scale` · response presets replace `element_class` · runtime grammar scenes replace unconditional bolt/impact generation · central hit-stop/shake arbitration · effect-age clock · tested migration for legacy tint arrays vs the v3 tint object · cast-ready gate for the first cast · tinted particles (T3v) · flash alpha.

## 6. Experiments (gates pre-registered)

**E0 — £0, no images, ~half a day** (probe 2 experiments 1–4): (a) layer-stack proof — one 128-px greyscale painted disc; sibling `GPUParticles2D` ADD (hue-modulated) + MIX black beneath at ~1.05×; 0.1 s quickflash; `PointLight2D`; 3 s decal — *does one painted shape read as a finished effect at our register?* (b) bake round-trip — alpha PNGs via Movie Maker → Spritesheet Generator → flipbook; A/B vs live — *is the dial real?* (c) rotation survival — spin a painted head 360° — *where does paint read as a rotating drawing?* (d) stepped time — `fixed_fps` 30/15/12/8 — *where is our Guilty Gear point?* Renderer check first: the web playtest runs GL Compatibility, where `emit_particle()` is unsupported — E0 confirms the stack on Compatibility or a renderer decision is a fork. **Pixel FX Designer ($14.96) only after E0.**

**E1 — procedural vs painted, one motion.** G1 fire projectile on the grey-room fixture (context 0.25 s → anticipation 0.15 → travel 0.5 s over 4 BH at 8 BH/s, body 1.2 BH → contact ≤ 1 tick → half-peak ~4 ticks → residue 0.6 s; impact envelope 3 BH, Matt-judged). A = procedural head/streak/wedge with banded materials; B = painted equivalents bound to the *same* events, seed, palette, light stack. ≤ 8 images (anchor paint-over 1 · head 1 · streak 1 · tongue 1 · wedge 1 · repairs/fallbacks 3); one TOOLING burst ≤ 40 min; drax builds the fixture. Gates: same events within one tick; extents ±10 %; pivots ≤ 1 native px; matte halo ≤ 1 px; first impact present; four-cast white ≤ 2 %; perf baseline. **Matt's ruling** on five order-randomised A/B pairs: painted preferred ≥ 4/5 and at the bar → **retain painted primitives**; procedural at the bar and ≥ 4/5 preferred/indistinguishable → **procedural becomes default**; painted loses register under required motion after the permitted repair → **test authored key states**; both fail → fix the fixture, no evidence either way.

**E2 — two grammars × two elements, one language.** Fire/ice × G1 projectile / G2 field (field placed directly; the flask + lob comes with the real BWC so coherence is not confounded with a new material and trajectory). ≤ 12 images. Fixture: four 3-second clips at one scale; dirt + foliage; four-cast synchronised + staggered; Keeper through the field and behind dressing; body-only / full-stack toggles. **Matt's three verdicts:** one language? · distinct identities without the glow? · a travelling strike clearly unlike a persistent field? A cell that passes only with its own layer stack or brush scale fails coherence even if it is pretty.

**E3 — the six.** Frozen Orb (G1 + emitter, ice) · Blackwater Cocktail (G2 + flask, fire) · Poisonous Concoction (G2 + flask, poison) · Lightning Blast (G3 ×1, lightning) · Zeus (G3 ×N, lightning) · Healing Hands (G4, holy) — each through the § 3 loop, each judged in Matt's fixture beside the others. The goal is met when the six read as one language over the cliffside and each is recognisably its source skill.

## 7. Forks for Matt — ELICITOR, one recommendation each

| # | Fork | **Recommendation** | Options / tradeoffs |
|---|---|---|---|
| V1 | **Route** | **painted primitives + runtime grammars, provisionally**, with E1's pre-registered exits to procedural-default or authored key states | guided key-state animation (image-heavy, per-sequence cost, boil risk) · fully procedural (cheapest; "vector graphics" risk) |
| V2 | **Effect art step** | **3 screen px**, ruled in motion at E1 | 2 px finer but nearer the scene grid; 4 px reads retro (the CrossCode pole you declined) |
| V3 | **Sequencing** | **E0 → grey room + dummies → E1 → E2 → the six**; no sheet before a grey-room clip is approved | skip E0 (saves half a day; forfeits the cheapest falsification of the stack thesis) |
| V4 | **Hybrid oracle (R-C3-118/120)** | **dissolve into class bands** — Hades strike bands + CoM/Slormancer legibility, scoped per class; measure `field_v1` / `aura_loop_v1` as their own lap | one blended oracle (mis-scores fields against strike curves, as CAST already did at R-C3-106) |
| V5 | **Flask + lob for the two thrown skills** | **keep** — upright RGB flask, tilt ≤ 10°, ballistic composition; tumble views only if you want tumbling | a ground flare alone omits the throw (skill identity lost) |
| V6 | **White and separation** | bodies white-free; white only as ≤ 0.1 s strong-contact flash; **halo + floor light default, dark duplicate an approved exception** | dark duplicate as default (Hades) — costs additive headroom on ochre |
| V7 | **Video-generation spend for VFX** | **no** — no alpha, no keyable plate, no shipped precedent; a clip is at most a *watched* timing/shape oracle | the $20 six-still bake-off stays a character-lane question |
| V8 | **Pixel FX Designer ($14.96)** | **after E0**, for primitive authoring only | before: buys output the consuming stack has not proved |
| V9 | **Renderer for E0/E1** | **Forward+ for the review fixture, Compatibility parity checked before web redeploy** (sub-emitters / `emit_particle` differ) | Compatibility-only from the start (constrains the stack to what the web build can run) |
| V10 | **Grey-room ownership** | **drax builds it as a mode of the production grammar scene** against a gandalf SCENEWRIGHT spec | conductor-glue mock (leaves the runtime untested) |
| V11 | **Signature flourish** | first a restrained world response (brief floor light + one characteristic residual motion) | an ornamental motif on every spell now |

## 8. Provenance

Dossier `00-` · prior `01-` · scorecard `02b-` · Astra S1 `02a-` · S2 `02c-` · S3 red-team `02d-` · Legolas `…/2026-09-15-vfx-grammar-and-authoring-split/` (taxonomy + authoring split; its emitted-corpus coverage analysis is parked) · `…/2026-09-15-vfx-motion-sources-and-tooling/` · prior research 2026-09-14/15 · C-3 ledger R-C3-81…123. Parked generator coupling: `04-parked-generator-coupling.md`.

— gandalf (ARCHITECT / SPEC-AUTHOR), 2026-09-15
