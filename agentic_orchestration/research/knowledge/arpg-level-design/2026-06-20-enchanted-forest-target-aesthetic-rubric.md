# Enchanted-Forest Target Aesthetic — Scoreable Rubric (GPT-5.4 independent read)

**Status:** SCORING REFERENCE — the shared target rubric for the enchanted-forest ravine build. galadriel (CV similarity pipeline), drax (builder), and gandalf (design director) each score the built Godot scene against this BEFORE the Matt Gate (and consequently before any ravine carve).
**Authored:** 2026-06-20. Commissioned by gandalf per Matt directive; the description is an INDEPENDENT GPT-5.4 vision read of the reference image, NOT gandalf's own (the point is a cross-model, single shared reference that reduces single-reviewer bias).
**Provenance:** OpenAI `gpt-5.4` (Responses API, vision) describing the official Synty **POLYGON Enchanted Forest** marketing render (the asset biome we build with). Source image: Matt-attached reference, 2026-06-20.
**Use in sequence:** build the at-grade patterned scene → score ≥ threshold against §5 → Matt Gate → only then carve the ravine down 7-10 tiles.

---

## How to consume this

- **galadriel:** turn §5 dimensions into CV-approximable metrics (color histogram vs the §2 palette, emissive/glow-pixel presence, fog gradient front-to-back, silhouette density, value-distribution). Score 0-1 per dimension × weight → composite.
- **drax:** build to §3 (signature elements MUST be present) + §2 (lighting/palette) + §6 (avoid every anti-pattern). The §6 list literally enumerates the prior-run failures (pale walls, gold metal, flat daylight, no glow) — do not reproduce them.
- **gandalf:** judge §1/§4 (does it READ as the target — mood, enclosure, depth hierarchy) as the human NV-style call.
- **Threshold for the Matt Gate hand-off:** composite ≥ 0.75 AND zero §6 auto-fail signals present. (gandalf-proposed; Matt adjudicates the actual gate.)

---

## GPT-5.4 verbatim output

## 1. One-paragraph target description
A stylized low-poly fantasy forest ravine at night/twilight, built from dense layered vegetation and oversized mushroom forms, with a strong "enchanted" read driven by green underlighting, cyan-blue bioluminescent accents, misty atmospheric depth, and warm mushroom-cap highlights. The scene is not open or pastoral; it is enclosed, vertical, humid, and visually packed, with dark framing tree trunks and rock masses surrounding a glowing central chasm/stream area. The mood is magical and mysterious rather than scary: deep cool shadows, luminous fog, small floating spore/firefly particles, and emissive mushrooms/crystals/stream elements create a soft fantasy glow inside a heavily overgrown jungle-forest composition.

## 2. Palette & lighting (measurable)
- **Dominant hues**
  - Deep blue-green shadow base: **teal-black / forest teal** `#0B1F22` to `#123A3A`
  - Mid foliage greens: **moss / fern green** `#3E6B3F`, `#567C45`, `#2F5E4A`
  - Emissive green core light: **acid green / enchanted lime** `#63F06A` to `#8DFF7A`
  - Cool magical accents: **cyan-blue / electric blue** `#51CFFF`, `#4B7BFF`, `#74E6FF`
  - Warm contrast accents: **amber / orange mushroom glow** `#D88A38`, `#F0B15A`
  - Rock/soil neutrals remain subdued: **muted brown-violet / dark stone** `#4A3A3A`, `#40344E`
- **Value range**
  - Shadows should be **very dark** overall: roughly **5–20% value** in edge/frame areas.
  - Midtones should sit mostly in **20–45% value**.
  - Bright emissive/fog highlights should spike to **80–100% value**, but occupy a **small area** of the frame (roughly **5–15%**).
- **Saturation character**
  - Base environment: **moderately saturated** dark greens/blues.
  - Emissive accents: **high saturation**, especially green and cyan.
  - Warm oranges are present but limited, functioning as spot contrast rather than dominant color.
- **Lighting model**
  - **Primary read** is from **internal/environmental glow**, not broad sunlight.
  - **Key light direction:** diffuse/obscured top-back light from upper center/left, softened by canopy and fog; no hard noon shadows.
  - **Secondary key:** strong **green emissive up-light** from ravine/stream/chasm center and lower midground.
  - **Warm local lights:** underside/edges of giant mushroom caps emit or strongly catch warm amber light.
  - **Volumetrics/god-rays:** visible but soft; strongest around center-left and center depth, with beams catching fog rather than cutting sharply.
  - **Bioluminescent emissive sources:** glowing mushrooms, crystals/plants, stream/path streaks, and tiny blue-violet particles must be visible in multiple depth planes.
  - **Fog/haze:** cool green-cyan haze, medium density; background contrast should drop progressively with depth. Far background should lose edge clarity by roughly **30–50%** versus foreground.
  - **Vignette:** dark edge falloff is present and noticeable, especially corners and side walls; edges should read **10–25% darker** than focal center.

## 3. Signature elements checklist
- [CRITICAL] Dense **low-poly enchanted forest/jungle** vegetation with layered ferns and broadleaf ground cover
- [CRITICAL] **Large stylized mushroom caps** in multiple locations, including warm amber/orange-lit caps
- [CRITICAL] **Bioluminescent blue/cyan mushrooms or crystals** near ground and cliff edges
- [CRITICAL] A **glowing green ravine/stream/chasm** or luminous source in the lower-middle/central scene
- [CRITICAL] **Dark vertical tree trunks** acting as foreground/midground framing pillars
- [CRITICAL] **Atmospheric fog/haze** creating visible depth separation
- [CRITICAL] **Enclosed, overgrown composition**; the scene must feel crowded and immersive, not sparse
- [CRITICAL] **Rocky cliff/platform layers** with vegetation spilling over edges
- [SUPPORTING] Small **waterfall or trickling water** element with cool coloration
- [SUPPORTING] **Hanging vines/roots** bridging or dangling into the ravine
- [SUPPORTING] **Floating spore/firefly-like particles** in blue/violet/white
- [SUPPORTING] Warm-vs-cool color contrast: **amber mushrooms against teal/green environment**
- [SUPPORTING] At least one **natural bridge/overhang/platform crossover** above a glowing void or stream
- [SUPPORTING] **Background giant tree or stump forms** catching warm rim/top light

## 4. Composition & depth
Depth is built through a strong **foreground frame → midground hero ravine/platforms → hazy background forest** structure. The image should have **at least 4 readable depth planes**: (1) very dark foreground foliage/rock framing, (2) near-midground platforms/ferns/mushrooms, (3) central glowing ravine hero zone, and (4) softened background trunks/mushrooms/canopy. Focal hierarchy should prioritize the **green emissive central chasm/stream area**, then the **warm mushroom caps**, then the **blue glow accents** near the lower right and lower center. The eye is led by **curving terrain/stream lines**, repeated mushroom lights, vertical trunk spacing, and brightness contrast: darkest masses on edges, brightest glow in the center-lower middle, then a secondary read into upper center background through fog.

## 5. Weighted scoring rubric (THE KEY OUTPUT)

| Dimension | Weight | 1.0 match vs 0.0 match |
|---|---:|---|
| Overall palette match | 14% | **1.0:** Frame is dominated by dark teal/green with cyan-blue and limited amber accents in similar proportions; **0.0:** palette is daylight-neutral, brown-only, gray, or lacks green/cyan magical contrast. |
| Emissive magic presence | 12% | **1.0:** Multiple visible emissive sources (green core glow + blue/cyan accents + some warm mushroom glow) create clear magical read; **0.0:** no glow, or only one weak emissive point with no scene-wide effect. |
| Lighting structure | 10% | **1.0:** Scene reads as low-key, center-lit by internal glow with soft top/back ambient and no flat even illumination; **0.0:** broad uniform lighting or strong direct sun dominates. |
| Fog/atmospheric depth | 10% | **1.0:** Clear depth fade with green-cyan haze, reduced background contrast, and mild volumetric shafts; **0.0:** crisp visibility front-to-back with no haze gradient. |
| Vegetation density | 10% | **1.0:** Ground, ledges, and platforms are heavily covered with layered ferns/plants across most of frame; **0.0:** sparse dressing, exposed empty ground, or large unbroken surfaces. |
| Mushroom signature | 10% | **1.0:** Oversized stylized mushrooms are prominent in several planes, including warm-lit caps and smaller glowing clusters; **0.0:** mushrooms absent, tiny, or visually insignificant. |
| Composition enclosure | 9% | **1.0:** Dark trunks/rocks frame the scene and create an enclosed ravine/jungle chamber feel; **0.0:** scene is open, wide, skyline-heavy, or lacks side framing. |
| Depth-plane readability | 8% | **1.0:** At least 4 distinct planes are legible via scale, overlap, value, and fog; **0.0:** scene reads flat with little overlap or scale progression. |
| Ravine/vertical layering | 8% | **1.0:** Terrain includes cliffs/ledges/bridges over a luminous lower area, creating stacked vertical traversal feel; **0.0:** mostly flat ground plane with no layered drop-offs. |
| Cool-vs-warm accent balance | 7% | **1.0:** Amber highlights are present but subordinate to cool green/cyan ambience; **0.0:** no warm contrast at all, or warm tones overpower the enchanted cool base. |
| Particle/micro-magic detail | 6% | **1.0:** Small floating spore/firefly lights and tiny bioluminescent details enrich the air and ground; **0.0:** no particulate or micro-magical detail visible. |
| Low-poly silhouette/style fidelity | 6% | **1.0:** Clean faceted stylized forms with readable low-poly silhouettes and simple material response; **0.0:** realistic/high-frequency textures, noisy normals, or non-Synty silhouette language. |

## 6. Anti-patterns (auto-fail signals)
- **Flat even daylight** or strong clear-sky sun reading; scene no longer feels nocturnal/enchanted.
- **No visible emissive glow** from mushrooms/stream/crystals/plants.
- **Sparse vegetation** with large empty ground patches or obvious undecorated terrain.
- **Open meadow or generic forest** composition instead of enclosed ravine/chamber layering.
- **Missing oversized mushrooms** or mushrooms reduced to minor props.
- **No atmospheric fog/haze**, causing background and foreground to read equally sharp.
- **Neutral gray/brown color dominance** without teal-green/cyan magical palette.
- **Hard realistic materials/textures** that break the clean low-poly Synty look.
- **Urban/man-made/metallic/concrete props** that overpower the organic biome read.
- **Overbright white bloom everywhere** that washes out color separation instead of concentrated magical emissive hotspots.

---

## gandalf note — what this changes about the build

1. **The "enchanted" read is EMISSIVE-LED, not lighting-led.** The prior run fought to light pale walls correctly; the target says the scene is lit *from within* — glowing mushrooms, glowing stream, spore motes — over a very dark (5-20% value) base. Build the glow first, the key light second.
2. **Our trough-water rule gains a job:** the §3-CRITICAL "glowing green ravine/stream" + §5 "Emissive magic presence (12%)" means the 50% shiny water in the undulation troughs should carry the cyan/green bioluminescent glow — the water IS one of the primary emissive sources, not just a reflective surface. That marries undulation + water + the emissive-magic score into one move.
3. **Density is scored (10%).** The target is "visually packed." Sparse dressing auto-fails. The combat islands stay readable (matte, telegraph-clear) but the ravine rim, ledges, and margins must be densely overgrown.
4. **Anti-patterns = the prior-run failure list.** Pale untextured surfaces, gold/metallic, flat daylight, gray-brown dominance — all named. This rubric, scored honestly, would have failed every prior round at the gate. That is the point.
