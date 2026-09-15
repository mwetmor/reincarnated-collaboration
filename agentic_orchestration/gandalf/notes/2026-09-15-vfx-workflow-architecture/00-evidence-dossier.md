# VFX workflow architecture — evidence dossier (what worked, what failed, why)

> **STATUS:** WORKING — gandalf (DRIFT-CRITIC → ARCHITECT), 2026-09-15. Input to the Astra design sessions and the Legolas probes; the synthesis lands in `03-architecture.md` in this folder. Every claim carries a ledger id (`astra_test_01/burst/runs/C-3/ledger.json` / C-2 / C-1) or a doc path. Survey-mode: § 1–§ 4 are what IS; § 5 is the diagnosis.

## 0. The question

Matt (2026-09-15): review what worked in the scene-generation and character/animation workflows, compare with what is failing in the VFX workflow, and design the VFX architecture most likely to produce **overall coherent effects that align with the scene register**. Three lanes, same image model (`gpt-6-astra`, HIGH), same conductor, same host — two held, one did not.

## 1. The three lanes side by side

| | **Scene** (cliffside, C-3 lap 2) | **Character** (Keeper matrix, C-2 → C-3) | **VFX** (six-kit breadth test, C-3) |
|---|---|---|---|
| Canon state | CANON (R-C3-102/119) | method stands; verdict owed (Q78) | closed as tooling/register proof, **not** skill fidelity (R-C3-123) |
| What the image model was asked for | **one still**, painted by outpainting against painted neighbour strips; later **isolated objects** on green | **one still** (master seed), turnaround by derived geometry; **paint-over** of cut frames | **24 frames in one 6×4 grid**, greyscale, "each row a phase in time" |
| Motion / time source | none needed (static painting; parallax = engine) | **video model** (Grok i2v from the still) → oracle cut → matte | **the image model itself** (row = time) + the builder's one hard-coded timeline |
| Structure-before-paint | **grey room** (drax blockout; Matt sees it before any paint, R-C3-55a); walkable/depth/ID masks; size chart projected | **dope sheet = spec** (R-21); Muybridge oracle; derived geometry per direction; bands committed before loops | **none** — the sheet was the first artifact; no blockout, no size/timing spec, no target in the scene |
| Register anchor in every brief | chunk_A passed as IMAGE 2 every paint burst | master seed (loops inherit the seed's register pixel-for-pixel, R-33) | **no reference image** (`references: []`) — register carried by prose only |
| Scale contract | Keeper 130 px = 12.5 %; ±25 % against the *projected* size chart (R-C3-68/73) | 240-px canvas, per-sheet scale lock, registration one scale + one translation per clip | 256-px cells, "must read at 64 px"; **in scene 0.3–0.6 BH** vs a 1–1.5 BH band (R-C3-107/108); rescued by `pixel_scale` / `phase_scale` knobs after the fact |
| Matt checkpoint | every geometry step (plan checkpoints 1–5); notes ledgered verbatim | every loop, by eye; gates re-derived from what the eye passes (R-48) | only at the end, on the live web build (R-C3-123) |
| Instrument | DP seam metric + conductor eyeball (metric blind at strip inner edges, R-C3-54) | idle/walk bands; falsified as a model of the eye, then re-derived (R-47/48) | Hades oracle bands O1–O10 (T3s) — measured the **body of one impact frame set**; nothing measured grammar, size in scene, or targeting |
| Iterations | v3 → v15, one note-set per version | idle ×3, walk ×2, then video | Frozen Orb v1 → v3; five other kits one drive each |
| Outcome | "meets expectations and is now canon"; iPhone "exceptionally well" | "Wow! The walk is perfect!!!" (R-55) | "all a variant of the same projectile… no targets… too small" |

## 2. What worked — scene (ledger R-C3-42…119)

1. **Blockout first, paint second, and Matt sees the blockout.** The grey room (drax) fixed geometry, walkable, depth and IDs before a single painted pixel; the organic-rules ruling (R-C3-54/55) happened on the grey room, cheaply. The paint could not drift the geometry because the geometry was a mask the paint had to fill.
2. **Context in the canvas, not in the prose.** Chunk paint is EDIT-mode outpainting against 256-px painted neighbour strips: seam error fell 31.3 → 1.8–3.0 /255 (R-C3-45/46/47). Prompt-only strips failed. The model continues what it can *see* far better than what it is *told*.
3. **One style anchor image in every brief** (chunk_A as IMAGE 2). Register held across 17 chunks + 16 panels + dressing + isolation.
4. **Registration by construction.** Dress-then-isolate on green (R-C3-62/64): the model dresses the crop, then an EDIT replaces ground with `#00ff00`, objects unchanged; placement = the diff bbox. Diff-only extraction failed 7/7; isolation succeeded because the model does *replace background* reliably and *preserve object* reliably.
5. **A projected size chart in the image** (IMAGE 3) — scale is enforced by a visible ruler, then gated ±25 % against the projected nominal size (R-C3-68/73). Size was never a prose instruction.
6. **Engine owns what engines are good at**: parallax, y-sort, fade, glows, particles, swarms (T3k…T3r). Paint is static; motion is runtime. The scene *feels* alive (embers, flies, flicker) without a single painted animation frame.
7. **Instrument + eyeball, and the eyeball is admitted.** The DP metric was blind at inner edges; the conductor eyeballed every join band (R-C3-54). Numbers gate; eyes still rule.
8. **Small loop, one version per note-set**, rejected attempts kept as lineage (12-step loop, scene-builder § 3).

## 3. What worked — character (C-2 R-28…R-55; C-3 P1–P6)

1. **Separation of register from motion.** The image model holds identity + register in ONE still (the master seed); the **video model supplies motion** (Grok i2v); the oracle cuts the cycle; the matte trims. Drawn frame-sequences from the image model failed twice with numbers (idle amplitude 0.47–0.68 %H vs floor 1.96; walk with four scales in one cycle and "doesn't look like walking at all", R-39/41) — then the video walk passed by eye at first sight (R-55).
2. **Spec before pixels** — dope sheet = spec (R-21); a measured floor oracle (Muybridge plates 2 + 13, R-22); bands committed with region lists before any loop was judged.
3. **The seed is the base of every composite** (edit-canvas re-renders slot 0 every time, up to 139 RGB; C-2 lesson 1) — never a sheet's own frame.
4. **Object-boundary masks** for paint-over (the staff split; C-2 lesson 2 → per-part masks). The model repaints *regions*; region edges must be object edges.
5. **Language is the amplitude lever, not px** (C-2 lesson 3): "numeric px deltas do not move amplitude; exaggeration LANGUAGE is the lever."
6. **Gates re-derived from the eye's passes** (R-47/48) — the instrument is subordinate to the ruling eye, and is corrected by it.
7. **First-party geometry references** for spatial construction the text keeps losing (the E strap, R-15/R-34).

## 4. What failed — VFX (ledger R-C3-88…123; notes 2026-09-15)

| # | Failure | Evidence | Which working-lane invariant it violates |
|---|---|---|---|
| F1 | **One grammar for six skills.** Frozen Orb (orbit-emitter), Blackwater Cocktail (thrown arc → burning pool), Poisonous Concoction (thrown flask → pool), Lightning Blast (instant chain), Zeus (chain that jumps), Healing Hands (self aura) all became cast → bolt → impact → residual | R-C3-123 (1); T3t schema has exactly four phases; `keeper.gd` spawns bolt + impact only; captures `drax/captures/2026-09-15-web-playtest-v6/live_cast_six_kits_sheet.png` — six identical radial stars at the cow | scene § 2.6: the engine owns motion — but here the runtime had ONE motion and the sheet was asked to imply the rest |
| F2 | **No targets, no targeting.** Impacts only exist against the cow; the six skills' *aim* semantics (self, ground-point, nearest, chain) never existed in the scene | R-C3-123 (2) | scene § 2.1: no blockout — the "grey room" of a VFX is a target and a firing rule, and it was never built |
| F3 | **Too small, discovered last.** Travel orb 0.3 BH, impact 0.5 BH vs 1–1.5 BH band; rescued by ×3 pixel_scale and ×2 phase_scale after the sheet existed; Matt still reads them as too small in scene | R-C3-107/108, notes 06:15Z, R-C3-123 (3) | scene § 2.5: no size chart in the image; character § 3.2: no spec before pixels |
| F4 | **Time was asked of the image model.** "Row 2 — TRAVEL (6 frames) … frames vary so they loop": the model produced six near-identical orbs with a slightly different streak (the sheet at `CS-vfx-frozenorb-sheets-v2/frozenorb_sheets_v2.png`); rows are *poses*, not *motion* | the sheet; oracles R-C3-19 double-peak (earlier frost); style-card v0 § 2 wanted 60 fps holds — a 6-frame row cannot carry that | character § 3.1: motion must come from a motion source; the image model holds a still |
| F5 | **Grey haze from the model on light-emitting subjects.** Fire / holy / poison sheets came back on a grey atmosphere under a hard black-void rule (BWC v2: 0 % black pixels, median L 86); ice and lightning sat on black | notes 05:10Z / 05:30Z / 05:50Z; `CS-vfx-bwc-sheets-v2/bwc_sheets_v2.png` | scene § 2.4: isolation must be *by construction* (green plate + EDIT replace), not by prose prohibition. The model does not obey "no glow"; it does obey "replace the background with flat green" |
| F6 | **A dark-bodied object cannot live in a greyscale tinted-light sheet.** The glass flask is near haze luminance and is lost to highlights; the pool/flame survive | notes 05:30Z (FINDING) | one sheet was carrying two different kinds of thing (an *object* and a *light*); the scene lane keeps objects as coloured isolated sprites |
| F7 | **Template contamination in briefs.** The BWC prose ("The flask glass is drawn MID GREY…", "pure WHITE only for the tiniest fuse spark and the very centre of the flame cores") was copied verbatim into the Healing Hands, Zeus, Lightning and Poison briefs | `briefs/C-3/CS-vfx-{healing,zeus,lightning,pconc}-sheets.task.json` | scene briefs were generated per chunk from a grid with per-chunk context; VFX briefs were one prose block with the skill name substituted |
| F8 | **No reference image in any VFX brief** (`references: []`). The register lived in ~400 words of prohibition ("NO glow, NO haze, NO bloom…") | the six task files | scene § 2.3: one anchor image per brief |
| F9 | **Particles rendered white; flash a large white disc; first cast never impacts.** Builder/runtime defects found only on the live build | R-C3-121, notes 06:45Z, T3v | scene § 2.8: one version per note-set — the VFX lane shipped six kits in one batch with no per-kit eye |
| F10 | **The recommended route order was skipped.** Oracle research ranked (c) procedural Godot → (d) hybrid → (b) video glow-only → (a) image sheets masks-only; R-C3-90 ruled a (c)-vs-(d) A/B on a frost bolt; R-C3-98 superseded it with the breadth test, which went straight to (a)+(d). **(c) was never run** | `legolas/research/2026-09-14-vfx-oracles/findings.md` § 5; R-C3-90 (4); R-C3-98/99 | the character lane *did* run its route order (drawn loops → failed → video) and let the failure pick the method |
| F11 | **Coherence had no mechanism.** Six kits, six independent drives, six ramps; nothing shared but the layer stack and the cell size | kits_v5…v8; one `element_class` field added last (T3v) | Hades: 112 of 126 god variants share one tinted sheet (oracles § 1) — coherence is *structural* (shared primitives + one stack), not a prose rule |

**What did NOT fail:** the register on sheets that came off true black (Frozen Orb v2, Lightning, Zeus) is right — hard edges, 4 bands, painted-pixel; the tooling chain (sheet → cut → tint ramp → kit → picker → web) works six times over (R-C3-104/111/122); the v0.2 legibility rules measured true (no white cores; halo + floor light). **The drawings are not the problem. The system around the drawings is.**

## 5. Diagnosis — the five invariants the working lanes share, and the VFX lane lacked

1. **Structure before paint, and Matt sees the structure.** Scene: grey room. Character: dope sheet + derived geometry. VFX: nothing — the equivalent (a *timed blockout* of each skill in the scene: target, aim rule, size, phases, durations — grey shapes moving) was never built. Matt's own hand-off step 2 (size-and-timing by video before any sheet) is exactly this.
2. **The image model supplies a STILL; something else supplies TIME.** Scene: engine (parallax/particles). Character: video model + oracle cut. VFX: the sheet rows were asked to be time. This is the deepest cause of F1/F4 — a row of six poses is not an effect; an effect is a *timeline over shapes*.
3. **Register enters through the canvas, not the prose** — an anchor image in every brief; context painted into the input (neighbour strips; the seed as composite base). VFX briefs had zero images and 400 words of prohibition.
4. **Isolation and scale are enforced by construction** — green plate + EDIT replace; projected size chart in-image; registration = diff bbox. VFX asked for black voids by prohibition (F5) and read size off a 256-px cell (F3).
5. **Coherence is structural, not stylistic.** The scene has one anchor chunk and one exporter; the character has one seed. Hades has one shared sheet per family, tinted. The VFX lane had six unrelated sheets and hoped a style card would hold them together.

Corollary for the architecture: **grammar lives in the runtime; primitives live in sheets; the anchor is a still; time is never drawn.**

## 6. Substrate facts (what the image model reliably does / does not do — observed, this run)

- DOES: paint a coherent still in-register when an anchor image is in the input · continue painted context (outpaint) · replace a background with a flat key colour while preserving the object (isolation) · re-paint a region with pose held (LABEL/edit) · draw crisp painted-pixel shapes at 5 values on black when the subject is *not* a light-emitter (ice, lightning).
- DOES NOT (reliably): obey "no glow / no haze" for fire / holy / poison subjects (F5) · produce true frame-to-frame motion in a grid (six poses ≠ six frames; F4) · hold scale across separately generated sheets (walk cycle four scales, C-2 lesson 4) · keep a dark object legible in a light-value sheet (F6) · read size from a cell (F3).
- UNKNOWN (Astra to answer): whether a green/magenta plate holds for emissive subjects the way it held for props · whether EDIT mode can *animate* — take frame N as canvas and paint frame N+1 with a motion instruction (the scene lane's outpaint, along time) · whether the model can paint a **primitive alphabet** (tongue, shard, ring, arc, mote, pool tile, chain link, wisp) as isolated sprites with a shared anchor, and what count is stable · whether an "effect sheet" should be RGB (coloured per element) rather than greyscale-tinted, given the tint-ramp already exists · what an image model's best contribution to *motion* is (key poses for a sim to interpolate? masks for a shader? nothing?).

## 7. Engine facts the architecture must consume

- The engine already emits a **geometry** per skill from a 26-type palette (`generation/geometry_derivation.py` `VALID_GEOMETRY_TYPES`): `ground_targeted_circle, circle, self_buff, single_target, vortex_pull, multi_projectile, beam_channel, teleport, ring, aura, line, cone, melee_strike, ground_slam, melee_arc, chain, ricochet_bounce, dash_attack, totem, defensive_dash, blink, fork, whirlwind, leap_strike, orbit, placed_lane`. The BC axis 2 (damage geometry) bins these into single-target / small-AOE / large-AOE / chain / multi-spawn.
- Emitted kits carry per skill: `canonical_element`, `effect_category`, `role`, `energy_cost`, `cooldown_seconds`, `effects[]` (damage / burn / …), `color_value`; the kit carries `dominant_element` + `color_palette`. **A VFX grammar template can be selected and parameterised from fields the engine already emits** — that is the coherence lever the breadth test never touched.
- The Godot runtime today (T3i/T3o/T3t/T3u/T3v): staff-tip socket + `release_index`; bolt = `Area2D` moving along the facing; impact on collision/range; layer stack (body, dark duplicate, additive glow, floor light, flash, decal, hit-stop, shake, tinted particles); Tab picker; `element_class` strike/field/holy.
- Scene register (canon): D2 weight + Bastion painted-scene pole + H1 line; Keeper 130 px; camera yaw 47° / pitch 52.95°; effects rotated at runtime and ground-squashed Y ≈ 0.5–0.62; hue is NOT the legibility carrier over painted ground — brightness/halo/floor light is (v0.2).

## 8. Questions this dossier hands forward

To **Astra** (sessions 1–3): § 6 UNKNOWNs; which of the five invariants its image_gen/edit can serve directly; what the image model's honest role in an effect pipeline is; candidate architectures; red-team.
To **Legolas** (probes): the grammar taxonomy + coverage of the 26-type palette; how painted-2D ARPGs author effects (flipbook / shared primitives / sim → sheet / procedural) and what carries coherence; procedural / simulated motion sources runnable on this host.
To **Matt** (forks, after synthesis): routed through `03-architecture.md`.

— gandalf, 2026-09-15
