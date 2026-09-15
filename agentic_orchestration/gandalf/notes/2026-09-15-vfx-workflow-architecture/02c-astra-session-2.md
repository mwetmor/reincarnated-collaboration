# Astra design session 2 — co-designing the VFX workflow architecture

> **STATUS:** RECORD — gandalf-conducted consult, 2026-09-15. Same channel as session 1 (`codex exec -p astra-burst --ephemeral -s read-only`, gpt-6-astra HIGH), with session 1, the conductor prior, Legolas probe 1, the engine geometry palette and three images staged; 99,568 tokens; no images generated. Answer verbatim; prompt appended.

---

## 1. The loop — one table, like scene-builder § 3

**Build B as three versioned contracts: resolved skill mechanics → runtime grammar → painted primitives and shared materials.** The image model supplies appearance; the approved runtime blockout supplies placement, motion, timing, and occupied size.

All tolerances below are **proposed project gates**, unless explicitly attributed to a measured reference. They become canon through the experiments and Matt’s rulings.

### Bringing one grammar family online

| Step | Who | What the image model receives — images by role | What it returns | Accepting gate — measurable | Matt checkpoint |
|---|---|---|---|---|---|
| **1. Resolve the family contract** | Conductor glue | None | No image call. A family manifest, supported geometry variants, exemplar skills, required mechanics, and explicit unresolved fields | Every parameter has a source, unit, and owner. Unsupported or ambiguous variants are listed as blocked | No new checkpoint unless the proposed behavior changes a skill’s identity |
| **2. Build the VFX grey room** | drax | None | A Godot family scene using grey bodies, trajectory guides, target dummies, footprint overlays, and an event timeline | First cast works; hit/expiry/cancel events agree with the fixture within one 60 Hz tick; footprint error ≤10%; required targeting cases pass | **Three-second clip at gameplay speed**, followed by the live scene if aim, attachment, or movement needs judgment |
| **3. Approve structure and capture guides** | Matt → conductor glue | None during approval. Tooling then prepares **edit target**, **approved VFX reference**, and **scene/scale reference** | Approved blockout manifest; timestamped body masks, anchors, and scene captures | Blockout hash, camera, BH conversion, timestamps, and guide coordinates agree exactly | Matt approves size, timing, direction, ownership, and readable phases before painting |
| **4. Establish the family’s painted appearance** | Astra **GENERATE**, EDIT mode | **1:** approved runtime silhouette at a named instant over the scene; **2:** relevant VFX chunk_A exemplar; **3:** native-size and scale board | One paint-over solving one appearance problem | Body bounds within ±10% of the approved envelope; attachment error ≤1 native px after registration; protected scene restored externally | **Actual-size still**, paired with the grey instant. For the first family, this is a provisional register decision |
| **5. Produce only missing primitives** | Astra **GENERATE** | **1:** isolated geometry guide; **2:** approved family/element appearance; **3:** scene placement and native-grid board | One isolated body, material object, or density asset per call | Extraction and registration contract in §6 passes; one diagnosed retry per candidate | Native enlargement plus its actual-size scene placement; no requirement to approve every reused asset again |
| **6. Extract, register, and compile** | Astra **TOOLING**, then **CHECK** | Normally none; CHECK receives native assets, matte composites, and registration overlays | Versioned native assets, metadata, derived masks, palette indices, and validation report | Exact palette/index format; valid alpha; pivots and endpoints pass; unknown schema keys rejected; no unexplained resizing | Exceptions only: a matte or reduction defect that changes the approved appearance |
| **7. Assemble and prove the moving effect** | drax + conductor glue | None | Runtime grammar using the accepted assets; single/four-cast captures; event and performance traces | Geometry, timing, termination, layer budgets, and class-specific QA pass | **Clips over bright dirt and foliage**, then **live playtest**. Matt judges the moving assembly |
| **8. Freeze and publish the family internally** | Astra **PACK**; conductor records ruling | None | Family package, approved presets, asset hashes, schema versions, regression fixture, and review packet | Clean import; no missing resources; cold first cast and repeated casts pass; exact reviewed build identified | Matt’s ruling identifies the accepted build and remaining exclusions |

**Burst boundary:** every TOOLING burst is one separately specified unit of ≤40 minutes. TOOLING remains serial; conductor glue does not modify lane tooling while it runs. A family can require multiple bounded bursts. That is different from promising all eleven families in one burst.

### Adding one skill to an existing family

| Step | Who | What the image model receives — images by role | What it returns | Accepting gate — measurable | Matt checkpoint |
|---|---|---|---|---|---|
| **1. Bind emitted data** | Conductor glue | None | Skill binding to an approved family variant, element treatment, and response class | Required mechanics resolved; valid units; no unsupported geometry fallback | Only unresolved identity or commitment-class decisions |
| **2. Preview with existing assets** | drax/runtime fixture | None | Grey/painted toggle of the new skill | Size, timing, targets, attachments, and cancellation pass the family fixture | Three-second clip; live review for a materially new targeting behavior |
| **3. Fill a genuine alphabet gap** | Astra **GENERATE → CHECK**, only if needed | **1:** missing primitive’s guide; **2:** approved element exemplar; **3:** actual scene placement | Normally **zero images**; otherwise one primitive and at most one diagnosed retry | Existing primitives cannot express the required distinction; new asset passes §6 | Actual-size comparison with its nearest accepted sibling |
| **4. Register and regress** | Astra **PACK**; conductor glue; Matt | None | Skill package plus single/four-cast comparison | No register tripwire; supported grammar unchanged; approved performance budget maintained | Final clip or live scene; ruling attached to the skill version |

## 2. The VFX grey room — spec

### What it renders

The grey room is a **mode of the production Godot grammar scene**, using substitute materials and debug overlays. Approving a separate animation made by conductor glue would leave the runtime untested.

It contains:

- The fixed cliffside camera and Keeper at **130 screen px per BH**.
- A neutral target dummy with visible feet, torso, hit point, and collision boundary.
- Three additional dummies for chain, fan, pierce, and density tests.
- Mid-grey effect bodies, dark material-object placeholders, and lighter secondary geometry.
- Separate outlines for **gameplay footprint**, **body envelope**, and **light envelope**.
- Origin socket, ground anchor, travel path, aim point, and attachment markers.
- A scrub timeline showing gameplay events and visual phases separately.
- A toggle between the real ground and neutral grey backing. Matt’s main review uses the real ground.

Labels report **body extent in BH**, footprint dimensions, speed, active duration, and phase timestamps. Canvas dimensions are storage metadata, not the size specification.

### Ownership and aiming

Every variant declares one aim rule:

- **Release-locked:** snapshot aim at release; subsequent cursor motion does not steer it.
- **Owner-tracking:** origin follows the owner; direction follows the specified aim policy.
- **Ground-locked:** placement stays at the accepted ground point.
- **Target-tracking:** attachment follows a named target until a specified termination event.
- **Event-linked:** chain endpoints and hop order come from actual gameplay events.

The renderer does not select targets, resolve hits, or move the player. The grey-room fixture supplies those events through the same interface the game will use.

### First blockout: F1 fire projectile

These are **experiment fixture values**, not inferred Blackwater Cocktail mechanics.

| Phase | Absolute clip time | Duration | Grey-room behavior |
|---|---:|---:|---|
| Context | 0.00–0.25 s | 0.25 s | Keeper and dummy visible; no effect |
| Anticipation | 0.25–0.40 s | 0.15 s | Small socket gather; aim locks at release |
| Travel | 0.40–0.90 s | 0.50 s | Projectile crosses a calibrated 4 BH path at 8 BH/s; body long axis 1.2 BH |
| Contact onset | 0.90–0.917 s | ≤1 tick | Confirmed contact; impact reaches its peak envelope |
| Main decay | 0.917–1.10 s | 0.183 s | Impact area reaches half peak approximately four ticks after peak |
| Residue | 1.10–1.70 s | 0.60 s | Low-value fragments/patch; no active damage implied |
| Clear tail | 1.70–3.00 s | 1.30 s | Effect gone; fixture remains visible |

The first impact envelope is **3 BH wide**, subject to Matt’s grey-room judgment. This is not a 3 BH minimum for every strike.

For persistent families, the timeline becomes:

`anticipation → activation → active interval with ticks → deactivation → optional harmless residue`

Active duration and tick spacing come from resolved gameplay mechanics. The preview may use a short, explicitly labelled fixture lifetime; it must also demonstrate cancellation and a longer hold.

### What Matt judges

In the three-second clip:

1. Can he tell where it originates, where it goes, and what it hits?
2. Is its body large enough against this ground?
3. Does contact read as a distinct event?
4. Does its duration suggest the correct gameplay behavior?
5. Does the ground component stay with the right owner or location?

In the live scene:

- Aim while moving.
- Reverse direction during a cast or channel.
- Walk through and away from a field.
- Lose a target during a chain.
- Cancel, recast, and cast immediately after scene load.

### Turning approval into drawing specifications

The approved capture emits two related artifacts.

**A. Primitive size/timing specification**

For each instance at each important phase:

`primitive slot · timestamp · native occupied bounds · screen bounds/BH · pivot · attachments · plane · transform · palette state · lifetime`

This establishes which forms must survive at native size and how far they will rotate, bend, stretch, or erode.

**B. Paint-over guide**

A registered scene capture with the selected body silhouette substituted in grey. Labels and arrows go on a separate reference board so they cannot become painted ornament.

The initial paint-over instants are:

| Instant | Why it is useful |
|---|---|
| **Mid-travel: 0.65 s** | The head, trailing direction, body scale, and internal planes are readable without contact clutter |
| **First full contact body: approximately 0.917 s, flash disabled** | Defines the actual impact silhouette rather than asking the model to paint a white flash |
| **Six ticks after contact: approximately 1.00 s, only if needed** | Tests whether breakup needs a distinctive spent shape; otherwise derive it from the accepted body |
| **Field: after activation has settled, before the next tick** | Defines the persistent field’s normal appearance rather than its exceptional entry burst |
| **Chain: a frame with two consecutive links visible** | Exposes joins, endpoint widths, and target attachment |
| **Melee: maximum extension of the approved sweep** | Fixes reach and the trailing contour at the instant where deformation is most demanding |

**Do not commission every instant automatically.** Begin with the one exposing the family’s unique visual problem. Runtime transformations remain the source of the other states.

## 3. The anchor package ("VFX chunk_A") and the element bootstrap

### The package

The package contains **three approved constructions: directional, radial, and ground-bound**. It records their appearance both as isolated bodies and as runtime composites.

Use these exact image roles and starting sizes:

| Image(s) | Size | Production method |
|---|---:|---|
| `scene_anchor_source.png` | **1536×1024** | Supplied chunk_A, unchanged. Its green void is excluded from placement and measurement |
| `scene_context.png` | **1536×1024** | Unscaled gameplay crop of the approved scene with Keeper at 130 px, target dummy, and usable ground |
| `guide_directional.png`, `guide_radial.png`, `guide_ground.png` | **1536×1024 each** | Captures of approved runtime blockout instants; flash and atmosphere disabled |
| `anchor_directional.png`, `anchor_radial.png`, `anchor_ground.png` | **1536×1024 each** | Astra paint-overs of those scene captures. Only the designated body region is accepted; tooling restores the scene outside it |
| `body_directional.png` | **128×128 native** | Isolated, registered, quantized production body |
| `body_radial.png`, `body_ground.png` | **256×256 native each** | Isolated production exemplars; reusable sub-primitives may be extracted with recorded coordinates |
| `native_directional_8x.png` | **1024×1024** | Nearest enlargement of the accepted 128×128 asset |
| `native_radial_4x.png`, `native_ground_4x.png` | **1024×1024 each** | Nearest enlargements of the accepted 256×256 assets |
| `layer_stack.png` | **1536×1024** | Tool-assembled board: body; optional material/underlay; halo; floor light; assembled result. Three constructions in rows |
| `scale_and_attachment.png` | **1536×1024** | Tool-assembled native and actual-size previews, Keeper, pivots, footprint, and occupied bounds |
| `palette_and_roles.png` | **1024×256** | Tool-generated palette bands and examples distinguishing index, alpha, density, and RGB material |

That is **17 images**. Source working images, masks, and manifests remain in provenance; they are not all supplied to every generation call.

The **final anchor composites are recomposed runtime captures** after extraction and palette conversion. A beautiful source paint-over that the renderer cannot reproduce is not an accepted anchor.

A normal production brief receives three images selected from this package:

1. Its specific geometry/edit guide.
2. The relevant approved appearance exemplar.
3. The scene/scale board.

### Grid and projection

Start with an **effect art step of three screen pixels** at the reference camera. Matt decides whether that reads too retro in E1.

- A 52-native-pixel occupied body becomes approximately 156 screen px, or **1.2 BH**.
- A 130-native-pixel assembled width becomes 390 screen px, or **3 BH**.
- Large effects expand their arrangement or mesh extent; they do not silently enlarge the apparent brush size.

Keep yaw **47°** and pitch **52.95°** in the camera calibration. Apply the selected **0.58 ground squash**, within the allowed 0.5–0.62 range, only to unprojected ground geometry. Do not additionally apply pitch as another squash.

Ground-plane rotation occurs **before projection**. Upright bodies are positioned from projected ground anchors and remain upright. Already projected scene paint-overs are never projected again.

### Bootstrap order

**First: fire, F1 projectile.** It tests asymmetric painted motion, saturated bodies against ochre dirt, erosion, and a visible trail without initially combining flask materials, ballistic travel, and a persistent field.

The package develops in two stages:

1. **E1:** directional anchor and provisional shared construction.
2. **E2:** radial contact exemplar plus ground-bound exemplar; confirm that the same construction survives a second grammar and element.

Then derive treatments in this order:

| Order | Treatment | Inherits | Distinctive additions |
|---|---|---|---|
| **1** | Fire | Initial approved construction | Hooked tongue; material flask when the thrown skill is built |
| **2** | Ice | Same scale, layers, band hierarchy, phase discipline | Faceted shard, broken crown, angular frost puff |
| **3** | Poison | Same construction and field boundaries | Viscous lobe, bounded density puff, poison flask treatment |
| **4** | Lightning | Same construction and endpoint rules | Branch junction and narrow prong |
| **5** | Holy | Same construction; support response preset | Folded ray/petal and interrupted seal |
| **6** | **Shadow, proposed sixth treatment** | Same construction and density limits | Hooked wisp and hollow husk |

**Naming seam:** the supplied six-kit test contains five treatments: ice, fire, poison, lightning twice, and holy. The local emitted corpus instead contains eight `canonical_element` values: earth, wind, water, fire, lightning, physical, shadow, and holy. Therefore `visual_treatment_id` must be separate from `canonical_element`. Ice and poison require explicit bindings; do not silently rename engine elements. Shadow is my proposed sixth bootstrap treatment, pending the conductor’s intended roster.

Elements 2–6 begin as **tool-recoloured versions of the same three constructions**. Astra then adds the listed silhouettes while retaining the parent’s plane sizes, negative-space proportions, edge treatment, and layer behavior. The resulting elements must remain distinguishable with glow disabled; palette alone is insufficient.

Matt approves:

- The first moving fire construction after E1.
- The directional/radial/ground package and fire–ice coherence after E2.
- Each subsequent treatment on the same three constructions, shown beside its parent.
- A material flask in motion before accepting the corresponding thrown skill.

## 4. The primitive alphabet — the build list

Legolas’s eleven entries are **functional slots**, not eleven compulsory new drawings. His decal appears again among the five constants; the dark duplicate and victim response need no new sheet. Orbit reuses a head, and whirlwind reuses a wedge. [Primitive derivation](evidence/research/vfx-grammar-and-authoring-split-findings.md)

### Common asset rules

- Coordinates below are **native canvas coordinates**, with origin at top-left.
- **Index** means a greyscale value-index map plus independent alpha.
- **Self-lit** means internal value structure follows the energy form, so rotating it does not rotate a painted sun highlight.
- **Ambient material** means restrained, non-directional material planes suitable for rotation.
- **Scene-lit** means the approved camera view carries the scene’s upper-left lighting; rotation is restricted.
- Starting deformation limits: **±15% transverse stretch**, unless a row specifies less. Larger changes require another primitive or mesh layout.
- Geometry length and radius are runtime parameters. Repetition and segment placement preserve stroke width.

### Eleven family slots

| Primitive | Role class | Painted or procedural | Working canvas → native px | Pivot / attachment points | Plane; projection baked? | Allowed runtime deformation | Light rule | Encoding |
|---|---|---|---|---|---|---|---|---|
| **P01 Head/core** | Banded body | Painted | 1024² → 128² | Centre `(64,64)`; tail `(32,64)`; nose `(96,64)` | Camera-facing; no ground projection baked | Translate, rotate 360°, uniform scale within approved range; modest axial stretch | Self-lit | Index |
| **P02 Tapered streak / wisp** | Banded body | Painted | 1536×1024 → 192×128 | Head `(168,64)`; tail `(24,64)` | Camera-facing; no | Extend by a ribbon mesh; preserve width and endpoint caps; controlled curvature | Self-lit | Index |
| **P03 Field body** | Ground patch | Painted | 1024² → 256² | Centre `(128,128)`; footprint in metadata | Ground; no | Patch placement, rotation before projection, overlap and erosion; no arbitrary bitmap enlargement | Self-lit or ambient, specified per treatment | Index |
| **P04 Residue/decal** | Ground patch | Painted | 1024² → 256² | Centre `(128,128)`; footprint | Ground; no | Rotate, tile by overlap, coverage erosion; no luminous inflation | Ambient ground material | Index with material ramp |
| **P05 Chain link / arc** | Banded body | Painted | 1536×1024 → 192×128 | A `(24,64)`, B `(168,64)`; endpoint tangents `+X`; restored end strips | Camera-facing connection between projected anchors; no | Piecewise bend and repeat; stretch middle ≤15%; endpoints fixed | Self-lit | Index |
| **P06 Broken ring segment** | Banded body | Painted | 1024² → 256² | Polar centre `(128,128)`; segment endpoints and tangents recorded | Ground by default; no | Place segments at changing radius; preserve band thickness; rotate before projection | Self-lit | Index |
| **P07 Wedge / slash / impact tooth** | Banded body | Painted | 1024² → 128² | Root `(16,64)`; tip `(112,64)`; inner/outer sweep attachments | Ground for footprint sweeps; camera-facing variant explicitly declared; no | Sweep, trim, repeat, modest bend; no unrestricted elastic warping | Self-lit | Index |
| **P08 Beam middle** | Banded body | **Procedural initially** | Generated at native 192×64; review at 1536×512 | A `(16,32)`, B `(176,32)`; protected repeat boundaries | Camera-facing ribbon; no | Tile to length, bend to a supplied path, preserve width | Self-lit | Index |
| **P09 Beam cap** | Banded body | **Procedurally derived from P01** | 1024² review → 128² | Centre `(64,64)`; beam join `(32,64)` | Camera-facing; no | Translate and rotate; no independent width drift | Self-lit | Index |
| **P10 Inward swirl** | Banded body | **Procedural arrangement of P02/P06** | 1024² review → 256² nominal layout | Centre `(128,128)`; orbital attachment paths | Ground path with optional upright pieces; no | Shrinking radius, angular motion, scheduled erosion | Inherits components | Index |
| **P11 Lane segment** | Ground patch | Painted | 1536×1024 → 192×128 | A `(24,64)`, B `(168,64)`; cross-section edges | Ground; no | Repeat to length; rotate before projection; overlap seams; fixed cross-section width | Self-lit or ambient by treatment | Index |

P08 becomes painted only if the procedural banded strip fails beside P05/P07. P09 and P10 receive new drawings only when their reused construction demonstrably lacks identity.

### Shared support assets and five constants

| Primitive / operation | Role class | Painted or procedural | Canvas → native | Pivot / attachments | Plane; projection baked? | Allowed deformation | Light rule | Encoding |
|---|---|---|---|---|---|---|---|---|
| **S01 Bounded puff** | Density | Painted | 1024² → 128² | Centre `(64,64)`; base `(64,112)` | Upright/camera-facing variant; no | Translate, ≤15% reshape, density modulation and erosion | Ambient density; emission separate | Density/index data plus coverage alpha |
| **S02 Mote / spark** | Banded body | Procedural | 256² review → 16² | Centre `(8,8)` | Camera-facing; no | Translate, rotate, short streak extension | Self-lit | Index |
| **C1 Cast/contact flash** | Emission-only | Procedural | 256² review → 64² mask | Centre `(32,32)` or event socket | Camera-facing; no | Short radial envelope; bounded scale | Emitted light | Runtime RGB + alpha |
| **C2 Halo / floor-light mask** | Emission-only | Procedural | 256² → 128² mask | Body centre or projected ground anchor | Halo camera-facing; floor light ground; no | Envelope scaling; bounded intensity; floor projection once | Emitted light | Scalar mask + runtime RGB |
| **C3 Residual decal** | Ground patch | **Alias of P04** | P04 | P04 | P04 | P04 | P04 | P04 |
| **C4 Dark duplicate** | Banded body, derived | Procedural duplicate | Same native asset as its source | Exactly the source’s pivot | Inherits source | Identical transform; approved small expansion only | Separation layer | Source alpha + dark runtime colour |
| **C5 Victim response** | Emission-only response operation | Procedural; **no asset** | N/A | Confirmed hit target | Inherits target; N/A | Target tint only; camera response handled centrally | Response colour | Runtime RGB; no source sheet |

This is **eight initial painted family assets plus one shared puff**, with the other slots derived or procedural. It is compatible with a roughly ten-asset shared layer without pretending the Hades count proves a universal ceiling.

### Per-element additions

The following profile references fully specify canvas, pivot, plane, and deformation. Each addition inherits its profile unless its row overrides it.

| Profile | Role; canvas → native | Pivot / attachments | Plane; baked? | Deformation; light; encoding |
|---|---|---|---|---|
| **T — tongue/petal** | Banded body; 1024² → 64² | Base `(32,56)`, tip `(32,8)` | Upright; no | Lean ±15°, stretch ±15%; self-lit; Index |
| **J — junction/crown** | Banded body; 1024² → 128² | Centre `(64,64)`; authored branch endpoints | Camera-facing; no | Rotate, translate, modest stretch; self-lit; Index |
| **D — density puff** | Density; 1024² → 128² | Centre `(64,64)`, base `(64,112)` | Upright; no | S01 rules; ambient; independent density and coverage |
| **M — flask** | Opaque object; 1024² → 128² | Base `(64,112)`, neck `(64,24)`, throw socket `(64,64)` | Upright camera view; **view/shading baked** | Translate; tilt ≤10°; no full spin or ground squash; scene-lit; **RGB RGBA** |
| **R — shard/husk** | Opaque object; 1024² → 128² | Centre `(64,64)`, base `(64,104)` | Camera-facing; no directional projection baked | Rotate only with ambient material planes; no elastic stretch; material Index + alpha |
| **G — seal/patch** | Ground patch; 1024² → 256² | Centre `(128,128)` | Ground; no | P03 rules; self-lit/ambient as declared; Index |
| **W — long wisp/prong** | Banded body; 1536×1024 → 192×128 | P02 attachments | Camera-facing; no | P02 rules; self-lit; Index |

| Element treatment | Primitive | Profile | Painted or procedural | Distinctive requirement |
|---|---|---|---|---|
| **Fire — 2** | Hooked fire tongue | T | Painted | Broad base, one hook, two strong internal openings at most |
|  | Oil flask | M | Painted | Dark glass and pale reflection remain opaque; flame/fuse is separate |
| **Ice — 3** | Faceted shard | R | Painted | Broad facets, restrained ambient shading; no rotating upper-left hotspot |
|  | Broken frost crown | J | Painted | Uneven crystalline teeth around open centre |
|  | Angular frost puff | D | Painted | Chunked, brittle breakup; no soft photographic mist |
| **Poison — 3** | Viscous lobe | T | Painted | Heavy rounded tip and neck; upward movement remains runtime-owned |
|  | Lobed density puff | D | Painted | Few large density islands and preserved holes |
|  | Poison flask | M | Derived from approved flask with a separate material treatment; paint repair only if needed | Contents/reflections use a material palette, independently of green emission |
| **Lightning — 2** | Branch junction | J | Painted | Unequal branch angles; endpoint locations restored by tooling |
|  | Needle prong | W | Painted | Fast taper and short angular reversals; no glass/flask instructions |
| **Holy — 2** | Folded ray/petal | T | Painted | Broad folded plane, restrained ornament |
|  | Interrupted seal | G | Painted | Open arcs and clear ground footprint; supports a quiet loop |
| **Shadow — proposed 2** | Hooked wisp | W | Painted | Broad dark body and pale saturated edge; opacity independent of darkness |
|  | Hollow husk | R | Painted | One large negative-space opening; material body remains readable without glow |

**Flasks belong to thrown alchemical skills, not to elements generally.** Blackwater Cocktail and Poisonous Concoction need them; ordinary fire, poison fields, lightning, ice, and holy effects do not inherit a flask slot.

The initial budget is **2–4 additions per treatment**, with review when a treatment approaches roughly twelve unique painted assets. That is a procurement checkpoint, not a rule that forces unlike verbs into the same drawing.

## 5. The grammar template contract

### The missing seam: emitted data is not yet a complete runtime specification

A read-only check of the local **411-kit / 3,612-skill corpus** found:

- `canonical_element`, `role`, `energy_cost`, and `cooldown_seconds` on every skill.
- **No `effect_category` field**.
- `effects` on **603 skills**, as prose strings.
- No top-level `aoe_radius`, range, projectile count, or duration fields.
- **603 null/absent geometries**.
- The persisted alias `chain_lightning`, plus the unregistered `projectile`, `roll`, and `persistent_zone` values.

These findings narrow the dossier’s claim that the necessary fields already exist. [Local kit corpus](/Users/admin/Games/reincarnated-engine/data/kit_space/kits)

Introduce a **resolved presentation spec**. Conductor glue assembles it from authoritative gameplay data and approved bindings; it does not infer mechanics from prose.

```text
VfxSkillSpec
  schema_version
  skill_id
  source_revision
  geometry_type_raw
  geometry_type_normalized
  family_id + variant_id
  canonical_element
  visual_treatment_id + palette_version
  response_class
  mechanics
    origin / aim / target policy
    footprint / range / width / count
    travel or owner-motion parameters
    active duration / tick schedule / termination
  presentation
    primitive bindings
    body extents in BH
    phase envelopes
    allowed layers and budgets
  provenance
    source path or approved override for every resolved field
```

Missing mechanics may have **explicit fixture values in experiments**. They block production registration until resolved.

### Common parameter sources

| Template input | Engine-emitted source | Resolution rule |
|---|---|---|
| Family candidate | `geometry_type` | Normalize only registered aliases. Retain raw value for diagnostics |
| Element identity | `canonical_element` | Exact lookup; never infer from skill name |
| Visual treatment | Explicit presentation binding | May express ice, poison, material subtype, etc.; does not change canonical mechanics |
| Response class | `effect_category` where actually supplied; otherwise typed gameplay semantics and an approved binding | Separate `strike`, `field`, `aura_loop`, `channel`, `support`, and `material`. “Holy” is an element, not a time class |
| Significance tier | `role` | `primary_attack`: ordinary strike; `burst_damage`: strong-strike candidate; `damage_over_time`: field/tick candidate; `sustain`: support candidate. Geometry and actual effects must agree |
| Recast interval | `cooldown_seconds` | Feeds recast/density tests. **Not** projectile lifetime, cast time, or field duration |
| Resource significance | `energy_cost` | Retained for review and optional approved tier selection. No direct “more energy = more white” formula |
| Damage/heal/burn/slow semantics | Typed `effects[]` where available | Present prose lists are supporting evidence, not executable parameters |
| Footprint and reach | `aoe_radius`, range, width, count fields **where a typed source actually exists** | Require units and conversion. Otherwise obtain the resolved collider/runtime parameters |
| Target order, collision, spawn, expiry | Runtime gameplay events | Authoritative during playback; renderer cannot invent them |

### Family mapping

**S** = approved strike envelope. **F** = field envelope. **A** = aura/loop envelope. **C** = channel envelope. The latter three require new measured reference bands, described below.

| Family / variant | Accepted engine geometry | Parameters and their sources | Time model | Validation and rejection | Default shared behavior |
|---|---|---|---|---|---|
| **F1 Projectile** | `single_target`, `multi_projectile`, `fork`, `ricochet_bounce` | Geometry selects variant. Resolved range, speed, count, spread, pierce policy, split condition, child count, bounce policy; runtime release/hit/split/bounce events | Anticipation from action; travel from gameplay; **S only at confirmed strike contact** | Reject missing speed/range or required count; reject unspecified fork/bounce behavior. `single_target` needs delivery resolution if it might be instantaneous | Low halo/floor light, tinted motes; strike response at contact; flash only for strong contact |
| **F2 Self/body-attached** | `self_buff`, `aura` | Owner ID/socket; resolved radius, duration, stack state, tick events; `effects`/role distinguish healing, defence, and damage | **A**; optional activation accent; no strike decay imposed on loop | Reject missing owner; missing expiry/indefinite-until-stop policy; ground ring must follow owner separately from upright component | Restrained halo/floor light and motes; healing/defence: flash, dark duplicate, hit-stop, shake, scorch **off** |
| **F3 Ground field** | `ground_targeted_circle` | Resolved target point, `aoe_radius`, active duration, tick events, stack/refresh policy | **F**; activation may contain a separately classified strike | Reject missing radius/duration/refresh behavior; no visual hazard after gameplay expiry | Floor light, restrained halo, optional density; harmless residual decal only when specified |
| **F4 Displacement** | `teleport`, `blink`, `defensive_dash`, `dash_attack`, `leap_strike` | Runtime owner trajectory and start/end; resolved duration/path/height; contact or landing events | Action/movement clock; S on a damaging arrival only | Blink has no connecting travel body. Defensive movement cannot inherit damaging hits. Renderer never moves owner | Streak or origin/arrival accent; contact flash/response only for confirmed damaging variants |
| **F5 Placed delegate** | `totem` | Resolved delegate ID, placement, lifetime, spawn/despawn events; delegate owns attack bindings | Spawn accent plus **A/F** persistence; delegate attacks use their own families | Reject missing delegate binding. Trap arming/triggering needs an explicit delegate subtype; never infer it from `totem` alone | Restrained spawn light; no automatic recurring flash, shake, or scorch |
| **F6 Chain hop** | `chain` | Runtime ordered target/endpoint events; resolved maximum hops, hop delay, link lifetime, repeat-target policy | Event-driven hops; **S** for each small contact, centrally budgeted | Reject absent hop/target contract; restore endpoints; target loss follows gameplay’s stop/retarget event | Link halo; small target tint; at most one strong flash/response per cast response window |
| **F7 Contact/radial** | `circle`, `ring`, `ground_slam`, `melee_strike` | Resolved origin, radius, propagation/contact events; melee contact socket; slam landing event | **S** after wind-up/contact; point-strike subtype has no expanding radius | `melee_strike` cannot invent a ground nova. Ring requires radius/thickness; slam requires ground contact; propagation must agree with hit schedule | Strike light/halo; flash for strong contact; decal only for ground-impact subtypes |
| **F8 Cone/sweep** | `cone`, `melee_arc`; `whirlwind` parameterisation | Resolved reach, aperture, start/end angles, owner/weapon attachment, sweep time, sustained flag, hit events | Burst cone/melee: action sweep + S contacts. Sustained breath: **C**. Spin: **A/C** | Reject absent aperture/reach; reject cone made from unrelated projectiles; sweep must match weapon/attack reach | Body/halo/floor light; no flash per swept frame; impacts centrally budgeted |
| **F9 Beam/channel** | `beam_channel` | Runtime origin/endpoints and channel state; resolved width/range, tracking rule, tick events | **C**; entry, sustain, snap-off | Reject missing channel-stop event or endpoint policy; caps remain attached; no linger implying continued damage | Restrained sustained halo/light; contact accents; flash/hit-stop/shake off per tick |
| **F10 Vortex** | `vortex_pull` | Resolved centre/radius, duration, inward path envelope; gameplay supplies affected-target motion | **F/A**, optional separately declared S collapse | Reject outward nova substituted for pull; never animate victims independently of gameplay | Inward body flow, floor light, restrained density; no recurring strike response |
| **F11 Lane** | `placed_lane`; `line` with resolved delivery mode | Resolved endpoints, width, duration or propagation speed, hit schedule | Static lane: **F**. Moving front: action clock + S contacts. Instant line: S | Reject ambiguous `line`. If it resolves to a traveling piercing head, bind **F1** explicitly. `placed_lane` remains stationary | Ground body/light, optional residue; flash only on a separately declared strong impact |
| **Orbit — F1 parameterisation** | `orbit` | Anchor ID, radius, angular speed, payload count, phase spacing, duration, tick events; all resolved | **A** orbital motion with event-driven contacts | Reject missing anchor/count; owner death/cancel clears children; moving emitter versus owner orbit must be explicit | Reuse heads and light; no flash for each revolution |
| **Whirlwind — F8 parameterisation** | `whirlwind` | Owner attachment, radius, angular speed, active interval, hit cadence | **A/C**, with action enter/exit | Do not rotate the character sprite merely because the effect sweeps; geometry and owner animation are separate | Reuse wedge/streak; continuous response budget |
| **Mortar arc — F1 ballistic + F3 landing** | **No dedicated engine geometry** | Explicit delivery binding on a compatible skill; target point, flight duration, visual apex, payload material, authoritative landing and field spec | Ballistic travel; landing accent; **F** persistence | Reject production binding without actual delayed landing semantics. A visual lob cannot conceal an instant field activation | Flask/material body; optional trail; landing light; field defaults after landing |

**Mortar decision:** it is a composition, not F12. Its flight uses separate ground position and visual height:

`screen_position(t) = project(ground_position(t)) − screen_up × height_px(t)`

A fixture can use `height_px(t) = 4 × apex_px × u × (1−u)`. Production uses the gameplay trajectory or its approved visual representation. The material flask stays upright unless additional tumble views are commissioned.

**Frozen Orb requires another explicit composition:** a traveling F1 emitter plus scheduled child emissions. An orbiting child-emission attachment may be used if the approved behavior calls for it. The name “Frozen Orb” must not automatically select owner-centred `orbit`.

### Time bands

- **`strike_fast_v1`:** selected Hades strike onset peaks in 0–1 frames; half-area/energy in approximately 2–7 frames; low-value residue may persist 0.3–1.0 s.
- **`strike_splash_v1`:** retain the observed exception where the body peaks about six frames after the initial flash. Do not fail every splash against the bolt/pillar envelope.
- **`field_v1` — must be measured:** activation rise, active-area stability, tick modulation, stacking, expiry, and harmless residue.
- **`aura_loop_v1` — must be measured:** activation, loop period, amplitude, owner-following behavior, stack transitions, and deactivation.
- **`channel_v1` — must be measured:** onset, sustained width/energy variation, tick accents, tracking, and snap-off.
- **`action_motion_v1` — must be measured/approved:** melee sweep and displacement timing relative to action events.

Existing field/beam footage contains partial and censored observations. It does not establish production loop bands. Until measured, use **named, Matt-approved fixture envelopes** and label their provenance accordingly. [Timing measurements](evidence/research/vfx-oracles-findings.md)

Use an explicit effect-age clock and event timestamps. Godot’s shader `TIME` is affected by time scale and does not stop with scene pause, so it is unsuitable as the sole lifecycle clock. [Godot 4.6 CanvasItem shader documentation](https://docs.godotengine.org/en/4.6/tutorials/shaders/shader_reference/canvas_item_shader.html)

### Concrete layer defaults and T3 amendments

**Shared stack means shared implementations, not all switches on.**

- **Ordinary strike:** body, low halo, brief floor light, small target tint; flash off.
- **Strong strike:** permits one ≤0.1 s contact flash; optional hit-stop/shake through a central response controller.
- **Field/aura/channel ticks:** flash, hit-stop, shake, and dark duplicate off by default.
- **Healing tick:** small palette pulse or mote, optional target tint; **no white flash, scorch, shake, or hit-stop**.
- **Material object:** alpha-blended material body; light comes from separate emission.
- **Dark duplicate:** deliberate per-preset option, never inherited merely because the legacy kit enabled it.

Amend T3t/T3u/T3v with:

1. A versioned primitive manifest and grammar binding replacing mandatory four-phase sheet assumptions.
2. A palette lookup that removes `white_core_keep`.
3. Independent alpha, density, material, and emission handling.
4. Explicit rendering planes and projection state.
5. Explicit phase-size metadata replacing unexplained `phase_scale` multipliers.
6. Class/role response presets replacing `element_class: strike/field/holy`.
7. Runtime grammar scenes instead of unconditional bolt/impact scene generation.
8. Central hit-stop/shake arbitration; simultaneous effects cannot independently fight over `Engine.time_scale`.

Legacy tint arrays and the v3 tint object require separate, tested migrations. An unversioned hybrid JSON fails validation. The supplied schema and v3 file are not interchangeable specifications.

## 6. Brief templates and the extraction contract

### Brief i — per-element body primitive: fire tongue

**Asset role**  
`fire_tongue_A`: banded body with independent coverage alpha. Runtime adds illumination.

**Already approved**  
F1 fire construction; three-screen-pixel art step; upright tongue profile T; broad painted planes; parent palette and layer preset. The tongue appears approximately 1.1 BH tall at maximum extension.

**Input image roles**

1. **Edit target:** `fire_tongue_guide.png`, 1024×1024, a 16× nearest enlargement of a 64×64 native guide.
2. **Appearance reference:** approved fire directional anchor, with its body-only native inset.
3. **Scene/scale reference:** Keeper at 130 px beside this tongue’s actual-size runtime placement.

**One requested visual change**  
Paint one broad-based, hooked flame tongue inside the guide. Use three broad value regions and one clear interior opening. Preserve the heavy base and narrowing tip. The form should remain recognisable with the light layer disabled.

**Canvas and registration**

- Working canvas: 1024×1024.
- Native canvas: 64×64.
- Occupied guide: approximately `x=12…52`, `y=8…56`.
- Base attachment: `(32,56)` native.
- Tip guide: near `(32,8)`.
- Upright; no ground squash baked.
- Surrounding area: genuine transparency.

**Exporter responsibility**  
Native reduction, band quantization, alpha validation, base restoration, palette lookup, and runtime halo/floor light. Source white is an index candidate, not rendered white.

**Acceptance and retry**  
Occupied bounds ±10%; base error ≤1 native px; interior opening survives native reduction; no external haze in the body asset. Return one candidate. One diagnosed retry for a named defect.

### Brief ii — grammar primitive: chain link with endpoint restoration

**Asset role**  
`chain_link_A`: banded connection body, independent alpha, reusable across element treatments.

**Already approved**  
F6 hop timing and target order; camera-facing links between projected target sockets; native link width; shared body/halo separation.

**Input image roles**

1. **Edit target:** 1536×1024 guide, an 8× enlargement of a 192×128 native canvas. It contains approved endpoint strips and a guided centre path.
2. **Appearance reference:** approved directional body and existing chain junction, if available.
3. **Scene/scale reference:** two target dummies with this link placed at actual size, including a second adjoining link.

**One requested visual change**  
Paint the middle connection as two or three broad angular bends. Match the endpoint widths and value ordering. Carry the same painted plane through the connection without introducing a separate impact star at either end.

**Canvas and registration**

- Native endpoint A: `(24,64)`.
- Native endpoint B: `(168,64)`.
- Endpoint tangent at both joins: `+X`.
- Preserve the supplied endpoint strips at `x=20…28` and `x=164…172`.
- Middle silhouette remains within the supplied width envelope.
- Genuine transparency outside the connection.

**Exporter responsibility**  
Restore the original endpoint strips **pixel-for-pixel**, including alpha and index values. Quantize the middle to the same palette. Register attachment coordinates. Test straight, bent, short, and repeated assemblies.

**Acceptance and retry**  
Endpoint-strip hashes match exactly; joins have no gap or width step greater than one native pixel; middle occupancy stays within its envelope; no endpoint stars. Return one candidate and allow one diagnosed retry.

### Brief iii — paint-over of a blockout instant

**Asset role**  
`fire_contact_anchor_A`: in-scene appearance proposal for the body at one approved contact instant. It is an appearance target, not a flattened runtime asset.

**Already approved**  
F1 contact at `t=0.90 s`; first full body at `t≈0.917 s`; 3 BH peak width; ground footprint, target position, camera, and timing. The runtime flash is disabled in this capture.

**Input image roles**

1. **Edit target:** `contact_0p917_scene.png`, 1536×1024, showing the grey contact silhouette over the approved dirt.
2. **Appearance reference:** approved fire directional body and its native enlargement.
3. **Structure/scale reference:** the same instant as an ID-mask board, Keeper at 130 px, footprint outline, pivot, and intended native extent.

**One requested visual change**  
Replace the grey contact body with a broken, outward-reaching fire shape. Use broad hooked planes and open gaps that preserve the silhouette’s directional bias. The target, floor, and Keeper establish scale and remain outside the accepted edit.

**Canvas and registration**

- Return the same 1536×1024 framing.
- Retain the supplied contact pivot and occupied envelope.
- Depict the designated body only; the guide already establishes its projection.
- Runtime supplies the flash, soft halo, floor illumination, and target response.

**Exporter responsibility**  
Restore the original scene outside the allowed body region. Produce a separate isolated body request from the accepted proposal. Preserve the capture’s coordinate transform through isolation and reduction.

**Acceptance and retry**  
Envelope ±10%; contact pivot ≤1 native px; no terrain detail incorporated into the isolated body; reassembled body matches the approved proposal’s placement. One candidate, one diagnosed retry.

### Extraction and registration contract

**1. Test actual RGBA first.**

Inspect the returned file, not its preview:

- An alpha channel exists.
- Empty margins are actually transparent.
- Opaque body interiors remain opaque, including dark bands.
- Transparent-looking checkerboards or painted backgrounds are absent from RGB content.
- Declared holes remain holes.
- Recomposition over black, white, bright dirt, and foliage produces no fringe wider than one native pixel.

For a hard body, propose **≥99% of the declared solid interior at alpha ≥0.98**. Density assets use their own coverage/density contract rather than this opacity gate.

**2. Choose the keying fallback by failure class.**

If genuine alpha fails, use **one diagnosed EDIT onto a supplied flat key plate**, followed by deterministic keying:

- Green for subjects without green.
- Magenta for green poison.
- Preserve the original canvas and registration.
- Restore fully opaque interiors independently of luminance.
- Inspect edge colour contamination on both light and dark backgrounds.

A single keyed image does not uniquely recover translucent foreground colour and alpha. For smoke, request a bounded coverage/density asset. For emission-only masks, a black plate can be appropriate. It is not the general flask extraction route.

If RGBA and the one fallback both fail, change representation or split the asset. Do not spend the experiment repeatedly demanding a better matte from the same mixed subject.

**3. Keep value index, alpha, density, and emission separate.**

For a four-band body:

- Store exact index levels, for example `0, 85, 170, 255`, identically in RGB.
- Alpha stores coverage.
- Index zero may be fully opaque.
- Density, when required, occupies a separately declared channel/file.
- Emission intensity is a material/instance parameter.

No threshold converts dark body pixels to transparency. No source level is automatically preserved as rendered white.

**4. Quantize deterministically.**

Reduce to the native canvas, then quantize visible colour/index regions. Use coverage-aware reduction before the final hard-edge decision; **nearest-neighbour is the enlargement/display rule**, not necessarily the correct initial downsampling filter.

Use nearest sampling and lossless import for index textures. Material RGB assets receive a separately approved palette, rather than being forced through an energy ramp.

**5. Record complete metadata.**

Each primitive records:

`asset_id · version · source hash · native dimensions · occupied bounds · pivot · attachments/tangents · role · plane · projection_baked · art_step · deformation limits · palette/material binding · alpha convention · lineage`

Cropping or atlas trimming must preserve the original pivot offset.

Use straight-alpha PNGs at interchange. A premultiplied runtime path must convert exactly once and declare its blend mode; mixing conventions fails the composite tests. Godot 4.6 exposes both ordinary alpha and premultiplied-alpha CanvasItem blending. [Godot blending modes](https://docs.godotengine.org/en/4.6/tutorials/shaders/shader_reference/canvas_item_shader.html)

**6. Recompose over the original.**

Place the extracted body over the **exact original capture** using the recorded transform:

- No manual recentering.
- No tight-bbox-derived pivot.
- No silent rescaling.
- Protected scene pixels restored exactly.
- Pivot discrepancy ≤1 native px.
- Body envelope discrepancy ≤10%.
- Inspect edge strips and internal holes at native and scene size.

After Matt accepts the recomposition, that runtime composite becomes the anchor. Future regression compares against it, rather than an unattainable raw paint-over.

## 7. Coherence QA — how we know it is one language

### Measure three outputs separately

1. **Body/coverage pass:** index bands, silhouette, area, attachments, and native feature size.
2. **Light-only pass:** halo and floor-light envelope.
3. **Final composite:** actual readability, saturation, clipping, occlusion, and simultaneous-cast accumulation.

The oracle must consume runtime coverage/ID masks where available. A brightness-difference mask misses dark flasks, dark residues, and holes.

### Class-specific measures

| Class | Measurements | Initial gate / reference treatment |
|---|---|---|
| **Strike** | Release/contact alignment; rise; half-area and half-energy; visible life; residue; peak BH; speed | Named Hades strike subtype, not one universal curve. Fast strike: 0–1-frame rise and approximately 2–7-frame half-life; explicit exceptions retained |
| **Field** | Gameplay radius versus visible boundary; activation; stable occupancy; tick amplitude; refresh; expiry | Boundary error ≤10%; activation/expiry aligned within one tick; no residual presented as active hazard. Reference amplitude/lifetime bands still to be measured |
| **Aura-loop** | Owner/foot attachment; loop continuity; occupied-area variation; stack transitions; cancellation | Attachment error ≤1 native px; no cumulative drift; no undeclared restart pop. Proposed calm-loop area modulation ≤15% around its approved envelope |
| **Channel** | Origin/end alignment; width; tracking lag; tick accents; sustained energy; snap-off | Endpoint error ≤1 native px after projection; width ±10%; cessation of active beam within one tick of stop, followed only by declared decay |
| **All classes** | Palette identity; band count in source index data; feature size; peak footprint; layer budget; final white coverage | Three-screen-pixel starting art step; approved palette versions; zero unregistered material/plane changes |

The art-step check concerns the **source shape grid**. Arbitrary rotations produce different raster edge patterns; that is judged in the motion fixture rather than falsely requiring every rotated sprite to form perfect 3×3 screen blocks.

### After-compositing white coverage

Use one fixed near-white classifier, initially:

`HSV V > 0.95 and S < 0.20`

Report:

- Near-white pixels / **full fixed combat crop**.
- Near-white pixels / **effect-covered pixels**.
- Baseline scene near-white coverage.
- Pixels newly pushed into near-white by VFX.
- Flash-enabled and flash-disabled results.

**Initial gate:** no near-white body colours by palette construction; final combat-crop near-white coverage **≤2%**, including four simultaneous casts. The measured approximately 0.1% from readable reference combat is an aspiration, not an interchangeable effect-pixel threshold.

If the clean background itself exceeds 2%, report that separately and establish an attributable-VFX budget; do not silently subtract it and claim the full-frame gate passed.

Halo lift **+0.16–0.41** and floor lift **+0.07–0.09** remain reference observations. On bright ochre, choose the lower safe gain or another approved separation treatment rather than clipping to satisfy an imported brightness increment. Measure the actual scene transfer. [Legibility findings](evidence/research/chronicon-com-slormancer-findings.md)

### Matt’s fixture

Every accepted family retains the same review fixture:

- Bright dirt and foliage locations.
- One cast.
- Four simultaneous casts, both synchronized and staggered.
- Keeper moving across the effects.
- A dummy partly overlapping the ground body.
- Body-only toggle.
- Eight directions for directional families.
- A cold first cast, repeated casts, and cancellation.

Matt rules on:

- “These belong to the same world.”
- “The grammar reads before the glow.”
- “The element remains identifiable.”
- “The effect is large enough without obscuring the fight.”
- “The world response adds weight.”
- “The motion preserves painted planes rather than exposing stretched stickers.”

### Month-six tripwires

A new skill triggers review if it:

- Introduces a new palette, art step, material mode, or layer preset.
- Needs more than ±15% deformation of a supposedly reusable primitive.
- Exceeds the family’s approved BH or light envelope.
- Adds white through overlapping saturated layers.
- Requires recurring flash/hit-stop to feel readable.
- Restarts a loop on refresh or leaves an orphan ground component.
- Adds one-off assets without demonstrating why the alphabet is insufficient.
- Uses unsupported geometry or lacks parameter provenance.
- Passes a still but fails direction changes or four-cast playback.
- Increases four-cast frame time by more than **2 ms at p95**, or breaks the agreed target frame rate on the Mac mini.

For the host, start with pooled instances, capped particles, small native textures, and no full-screen simulation. Profile the actual scene. A process-memory budget and renderer choice should be recorded with the first performance baseline; the 8 GB host is not permission to consume all available memory.

Coverage reporting keeps three separate denominators: **valid emitted skills, all emitted skills including unresolved records, and banded reference skills**. The reported 88% emitted coverage at six families cannot certify the absent melee/movement half. The probe’s reference-family coverage cells need reconciliation before reuse as a planning claim.

## 8. The first two experiments

### E1 — procedural versus painted, one motion

**Question:** does painting the moving body add enough register fidelity to justify B’s authoring and extraction cost?

**Motion:** the F1 fire projectile in §2, with one fixed seed, path, timing, footprint, impact schedule, palette, light stack, and particle budget.

- **A:** procedural head, streak, and impact wedge with banded materials.
- **B:** painted equivalents bound to the same motion.
- Both use the approved grey-room envelope.
- Display without flash first, then with the common response preset.
- Frozen Orb v3 may appear as a historical reference, but it is not the controlled comparator.

**Image budget: at most eight outputs, including edits.**

| Allocation | Maximum |
|---|---:|
| Directional in-scene anchor paint-over | 1 |
| Isolated head | 1 |
| Tapered streak | 1 |
| Fire tongue | 1 |
| Impact wedge | 1 |
| Diagnosed repairs or key-plate fallback edits | 3 |
| **Total** | **8** |

Do not spend all eight automatically. No flask, field, chain, or extra animation sequence is hidden inside E1.

**Tooling budget: one Astra TOOLING burst, ≤40 minutes.** Scope: minimal primitive manifest support, native conversion/alpha checks, registered guide export, and capture measurements for this fixture. It amends the existing exporter sufficiently for E1, not the entire production architecture. drax implements the small runtime fixture against this spec; conductor runs imports and captures. If the bounded tooling scope does not fit, reduce the experiment or report the blocker rather than hiding another tooling burst.

**Technical pass gates**

- Both variants follow the same events within one tick.
- Body/impact extents remain within ±10% of the approved guides.
- Pivot/attachment error ≤1 native px.
- No matte halo wider than one native px.
- No missing first impact.
- Final four-cast near-white gate passes.
- No unexplained body pumping, stretched highlights, or endpoint gaps.
- Four-cast performance meets the established host baseline.

**Matt’s ruling**

Show five short, order-randomized A/B comparisons across dirt, foliage, and direction changes. Ask him to select the one that better belongs in the scene, then name the defect in the loser.

- **Retain B:** painted is preferred in at least four of five comparisons, reaches Matt’s register bar, and passes the technical gates.
- **Choose C as the default:** procedural reaches the bar and is preferred or visually indistinguishable in at least four of five comparisons. Painting has not demonstrated sufficient value.
- **Abandon B’s primitive-only default:** the painted forms lose their register under the required motion after the permitted repair, or require a fresh drawing for each ordinary pose. Test a small authored key-state route next.
- **No architecture winner:** both fail the bar or the fixture is defective. Fix the diagnosed cause; do not count that as evidence for B.

### E2 — two grammars × two elements, one language

**Prerequisite:** E1 supports B.

**Matrix**

| | Fire | Ice |
|---|---|---|
| **F1 Projectile** | Accepted E1 construction | Same grammar, ice treatment and distinctive head/shards |
| **F3 Ground field** | Ground patch plus upright fire tongues | Same field mechanics, frost crown/shards and angular density |

The field is **directly ground-placed** in E2. Mortar/flask delivery remains a later test so coherence is not confounded with a new material and trajectory.

**Image budget: ≤12.**

- Fire radial and ground anchor paint-overs: **2**.
- Missing shared field body and decal: **2**.
- Ice shard, crown/head treatment, and angular puff: **3**.
- Up to **5** diagnosed repairs, extraction fallbacks, or missing-body isolation outputs.
- Total cap: **12**, including every EDIT.

Tool-generated palette variants, composites, contact sheets, and clips do not consume image calls.

**Fixture**

1. Four individual three-second clips at identical scale.
2. The same four effects on bright dirt and foliage.
3. A mixed four-cast scene with synchronized peaks.
4. A mixed four-cast scene with staggered timing.
5. Keeper walking through the field and behind foreground dressing.
6. Body-only and full-stack toggles.

**Measures**

- Shared art step, band ordering, alpha/material rules, and layer preset versions.
- Correct F1 versus F3 timing classes.
- Field boundary and expiry agreement.
- No elemental treatment changing gameplay reach.
- Near-white coverage after composition.
- Stable frame time and resource cleanup.
- Element and grammar identification from actual-size motion, including a brief glow-disabled comparison.

**Matt’s ruling**

He gives three separate verdicts:

1. **One language:** do all four belong together and to this scene?
2. **Distinct identities:** are fire and ice recognisable without relying on a large glow?
3. **Correct verbs:** is a traveling strike clearly different from a persistent field?

E2 passes only if all three hold. If a cell passes only after receiving its own unrelated layer stack or brush scale, coherence has failed even if that cell is attractive.

## 9. Risks, and the forks only Matt can rule

| Commitment-class decision | Recommendation | Reason |
|---|---|---|
| **Register: effect pixel scale** | Start at a three-screen-pixel art step and rule it in motion during E1 | It gives painted planes enough structure without imposing a pixel grid on the scene |
| **Medium: production default** | Choose B provisionally, with E1’s explicit exit to C or authored key states | Runtime grammars offer reuse, but painted deformation must earn its place |
| **Bar: still quality versus gameplay quality** | Make the actual-size moving assembly and four-cast fixture the acceptance surface | Asset beauty does not establish readability, timing, or coherence |
| **Register: white and glow** | Keep bodies white-free and reserve tightly budgeted white for strong contact flashes | This preserves saturated form under simultaneous casts |
| **Register: separation treatment** | Use restrained halo/floor light by default, with dark underlay as an approved exception | Bright dirt limits additive headroom, and one universal separation trick will not cover every material |
| **Identity: common construction versus elemental sameness** | Preserve the layer/grid discipline while allowing 2–4 distinctive additions per treatment | Shared rendering can unify unlike silhouettes without reducing elements to recolours |
| **Roster: the sixth treatment** | Use shadow as the sixth bootstrap candidate; confirm the canonical binding separately | It is present in the emitted corpus and tests dark bodies with independent alpha |
| **Skill fidelity: flask and lob** | Keep the flask and ballistic delivery for the alchemical skills that depend on them | They carry the cast’s identity; a ground flare alone would omit the throw |
| **Animation spend: difficult material rotation** | Begin with an upright translated flask and buy tumble views only if Matt requires tumbling | Full rotation of scene-lit painted glass needs additional representation |
| **Time register: continuous fields and loops** | Approve temporary fixture envelopes, then measure dedicated field/aura/channel bands | Strike measurements cannot define persistent magic |
| **Signature flourish** | First test a restrained world response—brief floor light and one characteristic residual motion | It can add project identity without attaching an unapproved ornamental motif to every spell |
| **Spend: alphabet expansion** | Review additions at roughly twelve unique painted assets per treatment; permit exceptions for distinct verbs | Hades supports the order of magnitude, not a hard universal cap |
| **Scope: genre coverage** | Require a melee sweep and a displacement fixture before declaring the architecture broadly complete | The present emitted corpus hides the very families most likely to stress attachments and deformation |
| **Host/performance bar** | Preserve native scene quality and reduce secondary particles/light overdraw first | Body silhouette and gameplay information are the highest-value pixels |

**Engineering blockers are not artistic forks:** missing mechanics, unresolved element bindings, unregistered geometry values, and T3 schema drift must be made explicit and fixed at their owning seam. Matt should rule the appearance, medium, bar, and spend of a concrete preview—not be asked to choose a plausible default for missing engine truth.
---

## Appendix — the prompt

### Design consultation, session 2 of 3 — design the VFX workflow architecture with me

You are Astra (`gpt-6-astra`), continuing the consultation. Session 1 is in `./evidence/astra-session-1-answer.md` — your own answer; build on it, do not restate it. Two new inputs arrived since:

1. **`./evidence/research/vfx-grammar-and-authoring-split-findings.md`** — Legolas's probe. Headlines: the grammar taxonomy already exists in our substrate (`corpus.db`: 18 motion signatures, 27 voted archetypes, 7 delivery classes, 1,135 banded reference skills); **eleven grammar families** cover the emitted corpus (6 → 88 %, 10 → 99.5 %) but only 53 % of the *reference* corpus at six because **nine engine geometries (the whole melee/motion half) have never been emitted**; Hades `Fx.sjson` measured: 5,141 FX entries → 1,152 sheets, 66 % own no asset; per-god sheets 4–26, median 12.5, over a shared ~46-root particle alphabet; § 1.4 derives **11 grammar-specific painted primitives + 5 shared constants**; H-A supported; H-B bounded as "≤ ~12 per element + a shared ~10-sheet constant layer, and the invariant layer stack is what makes one register."
2. **`./evidence/01-conductor-prior.md`** — the conductor's pre-registered prior (written before reading you). Your session 1 confirmed A-1, A-5, A-6; partially A-2 (you ranked genuine RGBA first, plate second, and said "test it"); refined A-3 (greyscale value-index + independent alpha as default, colour for material objects); refined A-4 (a VFX chunk_A *package*, not the Frozen Orb sheet). Legolas confirmed L-1 on the emitted corpus and refuted it on the reference corpus; confirmed L-2 strongly.

Also in `./evidence/`: `engine_geometry_palette.txt` (the 26 `VALID_GEOMETRY_TYPES`), the dossier, the style card, the scene-builder canon (the shape the VFX canon doc must eventually take), the oracle numbers, the T3t schema, the images.

**Your task: co-design the architecture.** Take your architecture **B** (shared painted primitives + runtime grammars) as the base, fold in the Legolas numbers and the conductor's prior where they are right, and produce a build-ready design. The conductor will synthesise this with the probes into the canon proposal for Matt; you are the image-side and pipeline-design authority in that synthesis. Constraints: Godot 4.6 2D runtime built by drax against a spec; lane tooling bursts ≤ 40 min each (you build them); image calls ≤ 12 per experiment; Mac mini 8 GB host; scene register and camera fixed (Keeper 130 px = 12.5 %; yaw 47° / pitch 52.95°; ground squash 0.5–0.62 for ground-plane geometry only); the existing layer-stack tooling (T3t/T3u/T3v) may be amended, not assumed correct (you found the schema drift).

Answer in Markdown under these exact headings.

#### 1. The loop — one table, like scene-builder § 3
A numbered step table for **bringing one grammar family online** and a second, shorter table for **adding one skill to an existing family**. Columns: step · who (Astra burst type / drax / conductor glue / Matt) · what the image model receives (list images by role) · what it returns · accepting gate (measurable) · Matt checkpoint (what he sees, in what form — still, clip, live scene). Include the **VFX grey room** (the moving blockout) as an explicit step, and the "paint-over of a runtime silhouette at a specific instant" move where it belongs.

#### 2. The VFX grey room — spec
What the blockout renders (grey shapes, timeline, target dummy, aim rule, size in BH, phases with durations), how it is built (Godot scene vs conductor script vs tooling burst), what Matt judges on it and in what form (a 3-second clip? live in the playtest?), and how the *approved* blockout becomes (a) the size/timing spec the primitives are drawn to and (b) the paint-over guide. State the frame(s) you would ask to paint over and why those instants.

#### 3. The anchor package ("VFX chunk_A") and the element bootstrap
Exactly what images are in the package, at what sizes, and how each is produced (which is painted over the scene crop, which is isolated, which is a native-grid enlargement). The order: which element and which grammar family first, and how elements 2–6 derive from element 1 so they inherit register but keep identity. What Matt approves and when.

#### 4. The primitive alphabet — the build list
Merge Legolas § 1.4 (11 family primitives + 5 shared constants) with your session-1 alphabet. For every primitive: name · role class (opaque object / banded body / density / ground patch / emission-only) · **painted or procedural** · canvas & native px · pivot / attachment points · rendering plane (upright / ground / camera-facing) · projection baked? · allowed runtime deformation · light-direction rule · greyscale value-index or RGB. Mark the per-element additions (2–4 each) and say which elements need a material object (the flask).

#### 5. The grammar template contract
Per family F1–F11 (plus orbit and whirlwind as parameterisations, and **mortar_arc** — decide whether it is F1 with a ballistic Y + F3 landing, or its own family): the parameters the template takes and which **engine-emitted field** supplies each (`geometry_type`, `canonical_element`, `effect_category`, `role`, `cooldown_seconds`, `energy_cost`, `effects[]`, `aoe_radius`/range/count where they exist); the time model (which phases use Hades strike bands, which use field/loop/aura bands — name the band sets that do not yet exist and must be measured); what the template validates and **rejects** rather than defaulting to a projectile; which shared constants it enables by default (your "healing ticks should not inherit a strike's flash" rule, made concrete).

#### 6. Brief templates and the extraction contract
Three complete example briefs in the shape you asked for in session 1 § 6: (i) a per-element body primitive (fire tongue), (ii) a grammar primitive (chain link with endpoint restoration), (iii) a paint-over of a blockout instant. Then the extraction/registration contract: RGBA-first with the alpha channel test; the keying fallback and when it is chosen; value-index vs alpha; palette quantisation; pivot metadata; the recomposition-over-original registration test.

#### 7. Coherence QA — how we know it is one language
What is measured (oracle bands by class — strike / field / aura-loop / channel — and the after-compositing white-coverage check), what Matt judges and in what fixture (your "one and four simultaneous casts on bright dirt and foliage"), and the tripwires that say the register has drifted when a new skill is added in month six.

#### 8. The first two experiments
E1 (≤ 8 images, ≤ 1 tooling burst): the procedural-vs-painted A/B on one motion, with pass/fail gates that would make us abandon B. E2 (coherence): two grammars × two elements, one language — the fixture, the measure, and the ruling Matt gives.

#### 9. Risks, and the forks only Matt can rule
List the decisions that are commitment-class (register, medium, bar, spend) and for each give **one** recommendation with a one-line reason — the conductor will present them to Matt as forks with your lean beside his.

Single Markdown document; no preamble.
