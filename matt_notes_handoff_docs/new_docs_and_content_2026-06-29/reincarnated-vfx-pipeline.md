# Reap. Die. Rise. — VFX Pipeline: The 2.5D Diablo/PoE Look in Godot (Canonical)

**Project:** Reap. Die. Rise. (ARPG / roguelite, Godot 4.7)
**Scope:** How to achieve the Diablo 3 / Path of Exile VFX look at the game's **fixed 2.5D camera angle**, in Godot, on a **mobile floor**, validated from **both** viewpoints the game uses (the 2.5D gameplay camera **and** the front-facing inventory portrait). Feeds the **VFX-translation agent** and the **camera-correct Judge**.
**Status:** Research-backed (Julian Love's Diablo 3 VFX talk + modern UE/Unity breakdowns + Godot node specifics). Recipes are starting points — verify exact built-in behavior on the pinned 4.7 version.

Tags: **[LOOK]** = defines the signature aesthetic (don't skip). **[2.5D]** = camera-angle-specific rule. **[PERF]** = mobile-floor constraint. **[DECISION]/[RECOMMENDATION]/[OPEN]** as in the other docs.

---

## 0. How to read this document

The signature look lives in **§1–§2** (two techniques) and the code in **§9**. The 2.5D-specific discipline is **§3–§6**. The dual-viewpoint answer is **§7**. Everything else is performance, harvesting, and pipeline integration. If you build only two things first: the **layered-noise shader (§9)** and the **billboard-mode discipline (§3)**.

---

## 1. The two techniques that DEFINE the look (get these right first)

These are the difference between "an ARPG's spells" and "generic engine particles." Both come from the canonical Diablo 3 approach.

### 1.1 [LOOK] Alpha Composite (premultiplied alpha), NOT pure additive
The single most important blend choice for an ARPG. In a busy fight, **dozens of effects stack on screen**; pure additive blending makes everything converge to a white blob. Translucent/mix blending can't pop as strongly emissive. **Alpha Composite** ("Blend-Add") effectively places a black background behind the emissive part, so each effect stays distinct even in chaos.
- **Tradeoff:** if an effect uses custom-colored noises with per-channel alpha, texture-packing may not be viable — author colors as material inputs instead.

### 1.2 [LOOK] Layered scrolling noise on VERY few particles
How Diablo gets rich, organic, morphing energy **without** thousands of particles:
- Take **one** noise texture, sample it at **three different UV scales** (e.g., 0.5 / 1.0 / 2.0), each layer **scrolling at a different speed**.
- **Multiply** the three layers together, then multiply by a **soft shape mask** (texture 4) that gives the blob a defined silhouette.
- Apply the result to **~7 particles**, not hundreds. The complexity is in the *shader*, not the particle count.
- **Critical:** randomize scroll-speed and UV offset **per particle** to prevent phasing and pattern recognition.

The three failure modes to avoid:
1. **Broken morphing motion** from improper scroll speeds — clamp each layer's effective speed to **> 0 and ≤ ~1**.
2. **Phasing** from imprecise octaves (UV scales too close).
3. **"Black eating the motion"** — not enough mid-tones around the shape edges; boost mids so edges don't crush to black.

This is the **signature**. It's also the cheapest path to the look (few particles, one shader) — which is exactly right for the mobile floor.

---

## 2. [DECISION] The look = a fixed recipe, applied per effect
Every energetic effect (cast flashes, orbs, projectiles' cores, impacts) is built from the same kit: **Alpha-Composite blend + layered-noise shader (few particles) + a soft shape mask + an HDR-bright color that the bloom/glow picks up.** Color and shape mask vary per effect; the technique is constant. This is what makes a *family* of effects read as one game's VFX language.

---

## 3. [2.5D] Billboard-mode discipline (the core camera-angle lever)

The fixed high camera (~45–60° pitch, looking down) is **not neutral** — effects must be authored to read **from above**. Godot's GPUParticles3D draw-pass supports the billboard modes that map each effect type to how it should face:

| Effect type | Billboard mode | Why (at the 2.5D angle) |
|---|---|---|
| Orbs, cast bursts, energy cores, impact flashes | **Billboard** (face camera) | Reads identically from any angle — safe for volumetric/radial effects. Auto-faces *whatever* camera renders (works in gameplay AND the inventory viewport). |
| **AoE telegraphs, ground fire, frost patches, magic circles, scorch** | **Horizontal / Y-billboard (flat on ground)** | Lies flat on the XZ plane — reads **perfectly** from a top-down angle. **This is the workhorse for ARPG ground effects.** |
| Pillars, walls of flame, upright beams | **Vertical billboard** | Stays upright on Y, rotatable toward camera. |
| Projectiles, shockwave rings, anything with real geometry | **Mesh mode** | Renders a 3D mesh; needed for travel projectiles and ground shockwaves. |

**[2.5D] The rule that prevents the classic mistake:** the camera sees the **floor**, so **every effect needs a ground-plane-readable component.** A purely-vertical effect (a side-on bloom, an upright flame with no ground footprint) looks great in a free-orbit preview and **disappears in-game**. Cast/impact/AoE all need a flat-on-ground element (horizontal billboard or decal) in addition to any camera-facing flash.

---

## 4. [2.5D] Decals for ground state (your secret weapon)

Godot's **Decal node** (4.0+) projects textures onto the ground in real-time, **without mesh generation**, and can move every frame. For an ARPG at a top-down angle, decals are ideal for:
- Scorch marks, blood, frost-on-ground, residual stains (persistent ground state).
- Static AoE zone indicators.

They conform to terrain, read cleanly from above, and add **no geometry overdraw** — a real perf win on mobile.

**[OPEN/limitation] Godot decals don't yet support custom materials/shaders or native animation** (the node exposes albedo/normal/PBR-mask textures only; the custom-decal-material proposal is still open). **Workaround:**
- **Static** ground marks (scorch, stains) → **Decal** (cheap, conforms).
- **Animated** ground effects (pulsing AoE telegraph, swirling ground fire) → **horizontal-billboard particle** or a **flat mesh with a scrolling shader** instead of a decal.

---

## 5. [2.5D] The per-slot VFX model at the gameplay angle

Mapping the composable slot model (**cast → travel → impact → residual**) to the 2.5D camera:

- **Cast** (at the caster): camera-facing **billboard** burst + the layered-noise shader (§9). Reads from any angle.
- **Travel** (projectile across the ground): **mesh-mode** particle or billboarded sprite **+ a trail** (`trail_enabled`, `trail_sections`, `trail_section_subdivisions`). The trail must **hug the XZ plane** (read along the ground from above), not trail vertically.
- **Impact** (where it lands): a camera-facing **flash** **+** a **horizontal-billboard or decal footprint** on the ground. The ground footprint is what actually reads at the angle — a side-on impact bloom vanishes from above.
- **Residual** (lingering): **Decal** for static scorch/stain; **horizontal-billboard particle** for animated lingering fire/smoke.

**Every slot carries a ground-plane component.** That is the per-slot expression of the §3 rule.

---

## 6. [2.5D] The ground shockwave (a specific recipe)

The Diablo "impact shockwave" (expanding ring distortion) = a **flat mesh ring/torus lying on the ground (XZ) with a distortion/dissolve shader**, which reads perfectly top-down. Build-or-harvest:
- Harvestable commercial-free reference: **gameidea.org "Godot Explosion VFX (Stylized)"** ships separate shaders for **core, cloud, residual smoke, shockwave, and spark** — usable in commercial projects without credit. Its shockwave is a low-poly torus + ripple-distortion shader; lift the shockwave material and apply it to a ground-oriented ring.
- Tutorial reference: GDNotes catalogs a "shockwave impact distortion shader" for Godot.

---

## 7. [DECISION] The dual-viewpoint solution (front inventory + 2.5D gameplay)

The game judges content from **two** cameras: the **front-facing inventory portrait** and the **2.5D gameplay angle**. How VFX handles each:

### 7.1 Gameplay spell VFX → validate from the 2.5D camera ONLY
Spell effects are **transient and camera-relative**. Billboards auto-face the gameplay camera; ground effects lie flat. The inventory screen does **not** show live spell effects, so **spell VFX carry no dual-viewpoint burden** — author and validate them from the fixed gameplay camera only.

### 7.2 Gear-attached VFX → ONE asset that reads in BOTH viewports
The dual-viewpoint burden falls on **gear/character-attached** VFX: an enchant glow, a flaming weapon, the **soul-conduit weapon's aura**. These must look right **both** in the front-facing inventory portrait **and** at the gameplay angle. The clean solution:
- **Use camera-facing billboards + the layered-noise shader** for enchant glows/auras. Billboards face *whatever* camera is rendering, so the same asset reads in both views automatically — **never bake an enchant VFX into a fixed orientation.**
- **Render the inventory item in a SubViewport** with its own front-on camera. The same VFX, viewed from the front, re-faces that camera and just works — **one VFX asset, both viewports, no double authoring.**

**[RECOMMENDATION]** Treat "does this gear-attached VFX read from the front portrait AND the 2.5D angle?" as a required Judge check (§12). Treat spell VFX as 2.5D-only.

---

## 8. [DECISION] Geometry/units note (shared with the build-architecture doc)
VFX anchor points (cast origin, weapon socket auras, impact-on-ground markers) must speak the canonical convention: **Godot Y-up, -Z-forward, 1 unit = 1 m, ground = XZ plane, character pivot at feet/base.** A VFX whose ground component assumes a different up-axis will float or sink. This is the same camera+geometry contract the content engine reads (see build-architecture §3 / the format-and-geometry seam).

---

## 9. The signature layered-noise ShaderMaterial (starting-point code)

A Godot 4 **spatial** shader for the draw-pass mesh (a QuadMesh) of a `GPUParticles3D`. Camera-facing billboard + Alpha-Composite (premultiplied alpha) + three-layer scrolling noise + soft shape mask. This is the §1 technique in code.

> **Godot blend-mode translation (important):** the Diablo "Blend-Add / Alpha Composite" maps to Godot's **`render_mode blend_premul_alpha`**. Premultiplied alpha adds emissive RGB where bright while alpha composites the (black) background — so stacked spells stay distinct instead of blowing to white. Output **premultiplied** ALBEDO (color × alpha) with `unshaded`. HDR brightness (>1.0) feeds the WorldEnvironment **glow** for bloom.

```glsl
shader_type spatial;
render_mode blend_premul_alpha, unshaded, depth_draw_never, cull_disabled, shadows_disabled, depth_test_disabled;

// --- Signature Diablo/PoE energy look ---
// One noise texture sampled at 3 UV scales, each scrolling at a different rate,
// multiplied together, masked by a soft shape, output as premultiplied-alpha (Alpha Composite).

uniform sampler2D noise_tex : repeat_enable, filter_linear;          // single tiling noise
uniform sampler2D shape_mask : repeat_disable, filter_linear;        // RGB white, A = soft silhouette
uniform vec3  energy_color : source_color = vec3(0.4, 0.7, 1.0);     // per-effect color
uniform float brightness = 2.0;                                      // >1.0 = HDR -> blooms
uniform float scroll_speed = 0.30;                                   // global pace
uniform vec3  uv_scales = vec3(0.5, 1.0, 2.0);                       // the three octaves
uniform float mid_boost = 2.0;                                       // lift mids so edges don't crush to black

varying float v_seed;

// cheap per-instance hash for per-particle variation (prevents phasing)
float hash11(float p){ p = fract(p*0.1031); p *= p+33.33; p *= p+p; return fract(p); }

void vertex() {
    // Camera-facing billboard built by hand (works in ANY viewport: 2.5D gameplay cam AND inventory front cam).
    MODELVIEW_MATRIX = VIEW_MATRIX * mat4(
        INV_VIEW_MATRIX[0], INV_VIEW_MATRIX[1], INV_VIEW_MATRIX[2], MODEL_MATRIX[3]);
    // Re-apply per-particle scale from the model matrix (avoids the known billboard-scale quirk).
    float sx = length(MODEL_MATRIX[0].xyz);
    float sy = length(MODEL_MATRIX[1].xyz);
    MODELVIEW_MATRIX = MODELVIEW_MATRIX * mat4(
        vec4(sx,0,0,0), vec4(0,sy,0,0), vec4(0,0,1,0), vec4(0,0,0,1));
    v_seed = hash11(float(INSTANCE_ID) + 1.0);
}

void fragment() {
    // per-particle offset + speed (keep effective speed > 0 and <= ~1)
    vec2  off = vec2(v_seed, hash11(v_seed * 7.0));
    float spd = scroll_speed * clamp(0.5 + v_seed, 0.5, 1.0);

    float n1 = texture(noise_tex, UV * uv_scales.x + off      + TIME * spd * 0.50).r;
    float n2 = texture(noise_tex, UV * uv_scales.y + off.yx   + TIME * spd * 0.85).r;
    float n3 = texture(noise_tex, UV * uv_scales.z - off      + TIME * spd * 1.30).r;

    // multiply layers; boost mids so motion survives near the shape edges
    float n = clamp(n1 * (n2 * mid_boost) * (n3 * mid_boost), 0.0, 1.0);

    float mask = texture(shape_mask, UV).a;   // soft silhouette
    float a    = n * mask;

    vec3 col = energy_color * brightness * a; // PREMULTIPLIED by alpha
    ALBEDO = col;                              // unshaded -> used directly
    ALPHA  = a;                                // composites cleanly when stacked
}
```

**Ground / AoE variant (don't billboard):** for flat ground effects, **skip the billboard vertex block** and instead orient the QuadMesh flat on XZ (rotate −90° on X so it lies on the ground), keep the same fragment shader. The effect then reads as a top-down magic circle / ground fire. For *static* ground marks use a **Decal** instead (§4).

**Authoring inputs (what the VFX-translation agent provides):** a single tiling **noise texture**, a **soft shape mask** (alpha = silhouette), an **energy color**, and brightness/speed values. That's the whole contract for an energy effect.

**[OPEN] Verify on 4.7:** the exact behavior of `blend_premul_alpha` + `unshaded`, the billboard-scale interaction (historical GPUParticles3D bug #74897), and `INSTANCE_ID` availability in the draw-pass shader. Treat the code as a recipe to validate, not gospel.

---

## 10. [PERF] Performance budget (the mobile floor)

Overdraw is the ARPG killer — and it bites **hardest at this camera** because stacked effects can fill the screen. (Confirmed pattern: particle VFX covering the screen temporarily tanks performance.) Discipline:
- **[PERF] Texture-driven over simulation.** The §1 approach (few particles, rich shader) is *both* the look and the perf answer. Diablo's richness is shader complexity on ~7 particles, not particle count. Default to few-particles-rich-shader; reserve high counts for rare set-pieces.
- **[PERF] Decals over geometry** for ground state (no mesh overdraw).
- **[PERF] Cap GPUParticles3D `amount` per effect**, and define a **per-slot mobile tier** (mobile gets fewer particles / simpler shader variants; PC scales up). Tie this to the build-architecture performance budget.
- **[PERF] Alpha-Composite also helps perf-perception** — it keeps dense scenes legible, so you need *fewer* particles to read clearly than if you were fighting additive blowout.
- **[PERF]** Watch the **billboard-scale quirk** (#74897) when scaling billboarded particles; the §9 vertex block re-applies scale to work around it.
- Use the GPUParticles **Visibility Rect/AABB** so off-screen systems don't process.

---

## 11. Harvest-and-relicense list (feeds the VFX-translation agent)

Starting points to **re-author to spec** (Move A "harvest ingredients" → Move B "agent re-authors as reusable `.tscn`"), per the existing asset-gap pipeline:

| Source | What it gives | License note |
|---|---|---|
| **iHoshiii/Godot-VFX** | Particle effects + shaders for Godot 4, built for action games | Verify repo license before shipping |
| **haowg/GODOT-VFX-LIBRARY** | Same category — action-game particle/shader collection | Verify repo license |
| **gameidea.org "Godot Explosion VFX (Stylized)"** | Core/cloud/smoke/**shockwave**/spark shaders | Commercial use, **no credit required** |
| **Bukkbeek EffectBlocks** | 100+ low-poly stylized 3D effects (Blender→Godot) | **Audit shader licenses** — an earlier plasma shader was a non-commercial shadertoy derivative (since removed). Confirm any harvested shader's provenance. |
| **godotshaders.com** | Free flipbook/fire/energy shader snippets | Per-snippet license; check each |

**[DECISION] License audit is a required step** for every harvested shader/texture before it ships — the EffectBlocks plasma-shader incident is the cautionary case. This is the same discipline already in the asset-gap pipeline.

**Flipbook note:** for pre-rendered fire/smoke/explosion sheets, Godot supports flipbooks via `CanvasItemMaterial.particles_animation` (2D) or a flipbook shader (the godotshaders snippet); if a sheet has a black background, set blend to Add (or alpha-to-transparency in an editor). Flipbooks are good for *complex* effects (smoke, fire) where the layered-noise shader isn't enough.

---

## 12. [DECISION] How this feeds the pipeline (VFX-translation agent + camera-correct Judge)

**VFX-translation agent — input/output contract (extends the asset-gap doc):**
- **Input:** reference (video / Niagara params / text intent) + the effect's **slot** (cast/travel/impact/residual) + **color/shape** intent.
- **Output:** a reusable Godot **`.tscn`** = `GPUParticles3D` (correct **billboard mode** per §3) + draw-pass mesh + **ShaderMaterial** (the §9 recipe or a flipbook) + any **Decal**/ground component required by §5, authored to the **mobile tier** by default.

**Camera-correct Judge — validate from the ACTUAL viewpoints (the key discipline):**
- **Spell VFX:** score rendered from the **2.5D gameplay camera**, at **mobile screen scale**. The question: *does it read clearly (silhouette, ground footprint, not blown out) in a busy scene from the top-down angle?*
- **Gear-attached VFX:** score from **BOTH** the **front inventory portrait** (SubViewport) **and** the **2.5D angle** — must read in both.
- This is the same principle as the content/geometry seam: **the validation viewpoint must equal the runtime viewpoint(s).** A VFX judged from a free/arbitrary camera will pass the preview and fail in-game. Repoint the Judge to the real cameras at mobile scale **before** anything reaches the live build.

---

## 13. Open questions & one-paragraph summary

**[OPEN]**
- Does the content engine currently *render* VFX for the Judge, or emit data only? (Determines whether "repoint the Judge to the 2.5D + front cameras" is a config change or new capability.)
- Is the gameplay camera strictly fixed-angle, or player-rotatable/zoomable? Fixed-angle lets you optimize ground-readability hard; rotatable relaxes silhouette constraints but demands all-sides readability (opposite trade — would change §3/§5 rules).
- Exact per-slot mobile particle caps — tune in profiling.

**Summary.** The Diablo/PoE look in Godot = **Alpha Composite (premultiplied-alpha) blend** + **layered scrolling noise on ~7 particles** (the signature, §9) + **billboard-mode discipline** (horizontal/ground for AoE & impacts, billboard for orbs/flashes, mesh for projectiles/shockwaves) + **Decals for static ground marks**. The 2.5D rule that prevents the classic failure: **every slot needs a ground-plane-readable component, because the camera sees the floor.** Dual viewpoint: **gameplay spell VFX validate from the 2.5D camera only; gear-attached VFX use camera-facing billboards + a front-facing inventory SubViewport so one asset reads in both views.** Keep it **texture-driven, few-particles, mobile-tiered** (overdraw is the ARPG killer at this angle), harvest-and-relicense existing libraries (auditing licenses), and **repoint the Judge to score from the real cameras at mobile scale** so content is validated against what the player actually sees.
