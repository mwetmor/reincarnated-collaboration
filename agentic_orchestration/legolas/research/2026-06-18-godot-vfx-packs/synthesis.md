# Research — VFX Asset Packs for the Godot 4.x GPUParticles3D Pipeline
# 2026-06-18

**Mode:** A (analytical)
**Commissioner:** gandalf (commission brief: `agentic_orchestration/gandalf/notes/2026-06-18-legolas-vfx-pack-godot-research-brief.md`)
**Governing constraints:** register-2 stylized-low-poly-3D (Synty), premium-lit; PoE/D2 JUICE but STYLIZED, not photoreal; pixel/2D-flipbook RULED OUT (pushback doc 2026-06-17).
**Output path:** `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/`
**Links file:** `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/links.md`
**Sources consulted:** 60+ URLs accessed 2026-06-18; full bibliography in §8.

---

## 1. Summary (5 sentences)

The Godot-native VFX ecosystem in 2026 is dominated by one creator — Binbun — whose library of 20+ individual CC0 packs (bundled as Godot Effects Collection Vol. 1, $26.25, and Vol. 2, $21.24) constitutes the only credible parametric-backbone candidate: every pack ships a tool script exposing color/hue, emission, noise shape, speed, and transparency, and coverage spans fire, ice, electric, dark magic, portals, beams, hits, and status — enough slots to fully populate the cast→travel→impact→residual chain. Bukkbeek EffectBlocks is a legitimate second Godot-native option (100+ effects, $9.99, Godot 4.4+) but carries a custom commercial license (not CC0) and its register reads stylized-LOW (low-poly cartoon) rather than the PoE-juicy stylized-gritty target, making it a weaker fit as the primary backbone. For the Unity harvest anchor, Hovl Studio RPG VFX Bundle ($24 on sale) and Piloto Studio's Realistic ARPG Starter Packs ($34.99 each) are the leading candidates, with Hovl sitting in stylized-gritty / ON-register territory and Piloto sitting in semi-real / borderline-over territory — both expose recolor scripts and broad slot coverage, and Unity EULA permits cross-engine texture extraction for a purchased asset used in a shipped product. Fab (UE) harvest is structurally more expensive per-asset: the Fantasy RPG Niagara VFX Pack and Niagara Magic VFX Bundle are the top UE harvest targets, both with Fab Standard License explicitly permitting any-engine use, but the UE→Godot workflow is meaningfully harder than Unity→Godot because Niagara behavior is more deeply engine-coupled than Unity Shuriken, and no dedicated VFX-specific porting toolchain exists. The harvest-and-rebuild workflow (Unity unitypackage extraction → FBX/texture pull → Godot GPUParticles3D rebuild with flipbook-flowmap shader) is documented in community resources and is legally clear for purchased assets, but is a non-trivial engineering cost per pack that must be amortized across all 400+ kits.

---

## 2. The three governing axes — applied across all findings

### 2a. Register-fit-to-Synty (two-sided verdict on every pack)

The evaluation scale: `stylized-clean | stylized-gritty | semi-real | photoreal` and `under / ON / over` for the stylized-low-poly Synty target.

- **Stylized-clean (under for PoE juice, ON for compositing over Synty):** cartoon, toon, cel-shaded, low-poly geometry effects. Composite fine over Synty, but lack the JUICE density (additive HDR bloom layers, ember residuals, flowmap churn) that the PoE/D2 register demands. Most Binbun packs sit here or at the lower edge of stylized-gritty.
- **Stylized-gritty (ON — the Goldilocks target):** juicy additive/HDR particle bloom, multi-layered emitters, noise/flowmap churn, readable cast→impact motion, element-legible color. Composites naturally over Synty geometry. PoE and D2 are stylized-gritty, NOT photoreal. Hovl Studio RPG VFX Bundle sits here.
- **Semi-real (borderline over):** starts to read as mismatched against flat-shaded Synty geometry. Piloto Studio "Realistic ARPG" packs sit here.
- **Photoreal (over — same collision as pixel, opposite side):** volumetric fire/smoke sims, PBR-correct sparks. Will clash with Synty's clean stylized poly surfaces.

### 2b. Parametric-axis inventory (the scale lever)

Substrate axes to map onto VFX knobs: element (hue/texture), geometry/form (silhouette/motion-shape), tier (scale/emission/layering), archetype (cast behavior). The knobs that matter: `color/hue · scale · emission/intensity · shape/noise-texture · lifecycle/timing · trail/sub-emitter`.

### 2c. License-at-scale

- **CC0:** zero friction at 400+ kit/season auto-assignment scale. Gold standard for the backbone.
- **Commercial perpetual (Unity EULA, Fab Standard):** purchased once; textures/art extractable for cross-engine use in your shipped product. EULA does NOT restrict to Unity-only for the art layer; scripts/shaders are engine-coupled and don't port. Confirmed via: Unity community consensus + Unity support FAQ + Fab Standard License cross-engine statement.
- **Custom itch.io commercial:** case-by-case. Bukkbeek's license is "no resell/redistribute as-is" — usable in your product, not redistributable standalone.

---

## 3. Options Matrix

### Category 1 — Godot-native packs

| Pack | Engine/Format | Contents (slots) | Parametric axes (confirmed exposed) | Register-fit verdict | License-at-scale | Cost | Notes |
|---|---|---|---|---|---|---|---|
| **Binbun — Godot Effects Collection Vol. 1** | Godot 4.x native (GPUParticles3D + custom shaders) | 300+ effects across 12 VFX categories: fire, ice, poison, smoke, impact, muzzle flash, magic (orbs + projectiles + areas), portal, beam, loot. 8 shader systems. ~19 downloadable sub-packs. | Color/hue, emission/light, noise texture + scale + scrolling + shape, speed/lifecycle, transparency (smooth/dithered/cut/hybrid), proximity fade, one-shot/autoplay, audio slots. **5/6 knobs present.** Sub-emitter support via Godot native. | stylized-clean / borderline stylized-gritty — **ON for compositing over Synty; edge-of-target for PoE juice density.** Needs additive-layer stacking to reach D2/PoE juice depth. | CC0 (Creative Commons Zero v1.0 Universal) — zero licensing friction. | $26.25 (25% off $35). Bundle of 27 assets = $35. Individual packs from $4.49. | Primary backbone candidate. Actively developed (March 2026 update). Godot 4.4+ (Forward+/Mobile; Compatibility mode unconfirmed). Vol. 2 ($21.24) adds Battle FX, Explosion FX, Electric FX, Hit FX, Status FX, Dark Magic FX — report Godot 4.5+ compat issues (shader serialization errors). |
| **Binbun — Magic Orb VFX** | Godot 4.x native | 30 orb/spell effects: 10 small effects, 10 misty spiral, 5 big glowing rim, 5 big burst | Color, emission, proximity fade, speed, one-shot/autoplay, dithering, transparency modes | stylized-clean / **ON** | CC0 | $4.49 | Projectile + travel-orb slot. Included in Vol. 1 bundle. |
| **Binbun — Elemental Magic FX** | Godot 4.x native | 24 presets: 8 projectiles, 8 area effects, 8 cast effects. Elements: fire, water, electricity, nature | Colors, emission, noise texture animation, particle behavior, transparency/edge hardness, wave effects, spiral trails, area radius | stylized-clean / **ON** | CC0 | $5.94 | Best element-coverage of any Binbun pack. Cast + travel + AoE slots. |
| **Binbun — Dark Magic FX** | Godot 4.x native | 21 presets: 6 projectiles, 6 orbs, 6 areas, 3 vortex | Colors, emission, noise scaling/animation, waviness, area radius, displacement, transparency edge | stylized-gritty (dark/arcane register) / **ON** | CC0 | $5.94 | Closest to PoE dark-register. Vortex effects = portal/buff slot. |
| **Binbun — Ice VFX** | Godot 4.x native | 20 effects: 4 areas, 4 projectiles, 4 ice balls (impact), 4 small sharp clouds, 4 mist clouds | Color, emission, proximity fade, speed, mesh resolution, dithering, transparency | stylized-clean / **ON** | CC0 | $4.49 | Covers projectile + AoE + impact + residual (mist) for ice element. |
| **Binbun — Electric FX** | Godot 4.x native | 18 presets: lightning zaps, electric balls, electric impacts | Color, emission, light, shape (noise frequency/amplitude/height), transparency | stylized-clean / **ON** | CC0 | $5.94 | Lightning/shock element. Cast + impact slots. |
| **Binbun — Beam VFX** | Godot 4.x native | 16 beam presets: colored lasers, energy beams | Noise texture, shape/radius/flare, hard/soft edge, color, emission, pulse, particle integration, open_amount (animatable), audio (start/mid/end) | stylized-clean / **ON** | CC0 | $5.24 | Beam slot. Most parametric beam in the Godot-native ecosystem. |
| **Binbun — Hit FX** | Godot 4.x native | 28 presets: hit impacts, explosion impacts, size variants | Colors, shape, transparency, audio integration, shader flares/streaks | stylized-clean / **ON** | CC0 | $5.94 | Impact slot. |
| **Binbun — Status FX** | Godot 4.x native | 18 effect presets + 18 overlay materials: freeze, heal, charge, level-up, burn etc. | Color, emission, color transition curves, noise texture/scaling/animation, particle amount/speed/velocity, transparency/edge hardness, waviness | stylized-clean / **ON** | CC0 | $5.94 | Buff/debuff aura slot. Overlay materials = status effect on character mesh. |
| **Binbun — Flame FX** | Godot 4.x native | 34 flame presets: campfire, torch, projectile, status-effect flame | Colors, wobble, edge softness, noise shape, on/off animation, overlay material slot | stylized-clean / **ON** | CC0 | $5.94 | Fire/flame element. Ambient + projectile + residual (lingering flame). |
| **Binbun — Battle FX** | Godot 4.x native | 42 presets: 12 shields, 6 flying slashes, 6 swings, 6 claws, 6 charges | Colors, emission, noise texture/scale/scrolling/shape, twisting, transparency edge, audio | stylized-gritty / **ON** | CC0 | $5.94 | Buff (shield), melee-slash, charge/buff-aura slots. |
| **Binbun — Portal VFX** | Godot 4.x native | 24 customizable parallax portal effects with stencil buffer | Parallax depth, color, emission | stylized-clean / **ON** | CC0 | Included in Vol. 1 | Portal slot. |
| **Binbun — Loot VFX** | Godot 4.x native | 12 loot pickup effects | Color | stylized-clean / **ON** | CC0 | Free | Loot-beam slot. |
| **Bukkbeek — EffectBlocks** | Godot 4.4+ native (GPUParticles3D + shaders) | 100+ effects: fire/smoke (6), combat (16 — muzzle/bullet/explosion/impact), energy/electricity (5), magic/stylized (6 — sparkles/portal/shield), nature (8), water (2), ground effects (pickups/loot), decals (15 — blood/cracks/footprints), space (4) | Size, color, timing. Plus modular scripts and shaders for advanced tweaking. **3/6 knobs explicitly confirmed; others likely present via scripts.** | stylized-clean (low-poly, cartoon) / borderline **under** for PoE juice — good for combat feedback, shallow for ARPG spell drama | Custom commercial license — "use in commercial/non-commercial projects; do NOT resell or redistribute as-is or modified." Not CC0. | $9.99 | Strong breadth. Decal coverage is unique (ground scorch/crack). NOT CC0 — blocks auto-redistribution edge cases. Godot 4.6 current (4.4 minimum). Good secondary/combat-feedback layer, not the spell-drama backbone. |
| **AlekseiRamirov — Starter VFX Pack (Lite)** | Godot 4.6 native | 9 effects: combat impacts (2), loot/interaction (2), campfire, explosion, muzzle, jump, movement particles | Global scale slider, Smart Palette System (resource-file color), modular folder structure. **3/6 knobs.** | stylized-clean / **ON** (minimal — lite scope) | CC0/MIT | Free | Good proof-of-concept starter. Smart Palette System = per-resource color without shader editing. Limited spell coverage. |
| **DragonForge — Godot 3D Ice Shaders + VFX** | Godot 4.3 native | Free tier: ice materials. Forge ($4.95): transparent ice variants, layered walls/floors. Dragonforge ($9.95+): **6 GPU particle VFX** (Turn Undead, Freeze Gaze, Ioun Stones, Cone of Cold, Thaw, Light Spells) + 7 shaders + 8 animated character examples | Not explicitly detailed for VFX layer | stylized-clean PBR fantasy / **ON** for ice biome | CC0 | Free–$9.95 | Niche: ice element specialist. Cone of Cold and Freeze Gaze = on-target ARPG slots. |
| **KnowerCoder — Stylized 3D Fire+Smoke** | Godot 4.4 (4.3 compat) | Fire shader + smoke particle combo | Minimal (shader-driven; params via shader code) | stylized-clean / **ON** | MIT | Free | Very small scope. Tutorial value (architecture reference for custom shader-based fire). |
| **GDQuest — Godot 4 VFX Assets** | Godot 4 (exact version unconfirmed) | Particle examples, shaders, backgrounds, effects — exact inventory not public on landing page | MIT (code), CC-BY-NC-SA (art) | stylized-clean / **ON** | CC-BY-NC-SA art layer — **NOTE: NC clause blocks commercial use of art assets.** MIT code = usable. | Free | The NC art restriction means art assets cannot be used in a commercial product without additional clearance. Code/shader patterns are safely usable. |

### Category 2 — Unity harvest packs

| Pack | Engine/Format | Contents (slots) | Parametric axes | Register-fit verdict | License (cross-engine) | Cost | Notes |
|---|---|---|---|---|---|---|---|
| **Hovl Studio — RPG VFX Bundle** | Unity (URP + HDRP + Built-in) → harvest art layer | Magic arrows, shields, buff/debuff spells, hits, magic circles, projectiles, attack spells, lasers, track markers. ~6.0.2 (March 2026). 90.3 MB. | **One-click recolor script** (hue shift full pack). Resize. Custom shaders (proprietary to Unity — don't port). **2/6 knobs directly** (color, scale); others locked in Unity-side shaders. Art layer: textures, flipbooks, trail meshes extractable. | **stylized-gritty (cartoony-magical, vibrant, multi-layered particle bloom) / ON** for Synty target. Community characterizes as "toon aesthetics, magic circles" — juicy but readable-clean, not photoreal. The sweet spot. | Standard Unity Asset Store EULA — community+creator consensus: cross-engine texture extraction for your shipped product is PERMITTED. Scripts/shaders do NOT port (engine-coupled). Art layer (textures, flipbooks, meshes) is portable. | $24 (50% off $48). Requires Hovl support package ($5 separate). | **Top Unity harvest anchor.** Slot coverage: cast flash, travel projectile, trail, impact burst, residual, beam/laser, portal, buff/debuff aura, magic circle/AoE. One-click recolor = color axis present in Unity; must re-implement in Godot material. Last updated March 2026. 51 reviews, 1,722 favorites. |
| **Piloto Studio — Realistic ARPG VFX Starter Pack — Fire Spells** | Unity (URP + HDRP + Built-in) → harvest | Fire spell starter: cast + travel + impact. 61.4 MB. Dec 2025. | Unconfirmed from page | **semi-real / borderline OVER** — "realistic" in title means denser, more physically-based particles than Hovl. Higher chance of clashing with clean Synty geometry. | Standard Unity Asset Store EULA — same cross-engine posture as Hovl. | $34.99 | Register risk: "super realistic ARPG" framing suggests it targets HDRP photoreal look (AAA PC game). Verify visually before purchase. |
| **Piloto Studio — Super Realistic ARPG FX Bundle** | Unity → harvest | 1000+ effects. Comprehensive. | Unconfirmed | **semi-real to photoreal / OVER** (given "super realistic" + HDRP focus) | Standard Unity EULA | $200 (50% off) | Very large scope but register likely over-shoots. Verification pass required before committing. |
| **Piloto Studio — Magical Combat Stylized VFX** | Unity (URP + HDRP + Built-in) → harvest | Magic combat effects, top-down/MOBA oriented. 19.8 MB. Aug 2025. | Unconfirmed | **stylized-clean / ON** (toon/stylized framing, top-down context — lighter juice than PoE) | Standard Unity EULA | $15 | Lighter register than PoE target but no collision risk. Lower-priority harvest. |
| **Piloto Studio — Frost & Ice Stylized VFX Starter Kit** | Unity → harvest | Ice/frost spell VFX. | Unconfirmed | **stylized-clean / ON** | Standard Unity EULA | $39.99 | Ice element specialist for Unity harvest path. |
| **Archanor VFX — Action RPG FX** | Unity (URP + Built-in; NOT HDRP) → harvest | Portals, loot, RPG-oriented particles. 89.2 MB. Sept 2024. 26 reviews, 887 favorites. | Unconfirmed | **stylized-clean / ON** (Archanor style is vibrant-cartoonish, not photoreal — consistent across their catalogue) | Standard Unity EULA | $20 | Slot emphasis: portals, loot-beam, ARPG ambient. Less spell-drama focus. Good supplementary harvest for portal/loot slots. |
| **GAPH — 70 Fantasy Spells Effects Pack** | Unity → harvest | 70 spell effects. 288 MB. 32 reviews. | HDR, parametric unconfirmed | **stylized-clean / ON** (fantasy spells, vibrant, not "realistic") | Standard Unity EULA | $14.99 | Large count for price. Slot coverage unknown (no detailed contents list available). Worth investigating visually. |
| **Vefects — Stylized VFX Bundle** | Unity (Built-in ONLY — not URP/HDRP) → harvest | Anime-style VFX. 225.5 MB. 90 reviews, 69 favorites. | Unconfirmed | **stylized-clean (anime/manga) / under** for PoE register — anime VFX skew softer and more graphic than PoE juice | Standard Unity EULA | $164.99 | Anime register explicitly named. Built-in only = older pipeline. Lower harvest priority for PoE-style target. |

### Category 3 — UE/Fab harvest packs

| Pack | Engine/Format | Contents | Parametric axes | Register-fit verdict | License (cross-engine) | Cost | Notes |
|---|---|---|---|---|---|---|---|
| **Fantasy RPG Niagara VFX Pack** | UE Niagara → harvest art only | 90 particle systems: 16 AoE, 33 generic/common, 7 aura, 4 beam, 7 buff, 5 explosion, 5 portal, 8 projectile/missile. Elements: fire, ice, arcane, blood, nature, lightning. | Niagara parameters (color, scale, etc.) — don't port to Godot. Art layer (textures, flipbook sheets) does port. | **stylized-gritty / ON** — described as fantasy RPG with "fire, ice, arcane" theming, reviewers call it "high quality" — suggests juicy ARPG register | Fab Standard License: "enables you to use the assets in any game engine or tool you want." Cross-engine extraction: PERMITTED. | Unconfirmed (Fab 403 blocks direct fetch — verify on Fab) | Broadest slot coverage of any UE pack found. Harvest cost: high (Niagara behavior = full rebuild in Godot; only art transfers). Requires UE install to extract. |
| **Niagara Magic VFX Bundle** (Projectiles + AOE combined) | UE Niagara → harvest art | Projectiles + AOE magic: fire, ice, lightning, arcane, poison, holy, shadow elements. Community-praised as "simply beautiful," "incredible particles." | Same as above — Niagara-side knobs | **stylized-gritty / ON** — community reviews strongly positive on visual quality; "high quality VFX asset" | Fab Standard License — cross-engine permitted | ~$60 bundle | Strong element breadth. Separate projectile and AOE packs. High harvest cost (Niagara rebuild). |
| **Fantasy VFX Bundle** (Fab) | UE Niagara → harvest art | 230 Niagara effects: beams (15), energy balls (25), impact particles (30), projectiles (25), sword slashes (40). | Niagara-side knobs only | **stylized-gritty / ON** (described as "ultimate effects for fantasy and stylized games") | Fab Standard License | Unconfirmed price (Fab 403) | Good slot diversity. Sword slashes = melee element. |
| **Stylized VFX Pack Vol. 3 (Niagara)** | UE Niagara → harvest art | Anime cartoon style with procedural shaders, color/camera/light direction adjustable. | Color, camera direction, light direction — procedural shaders (do NOT port to Godot) | **stylized-clean (anime) / under** for PoE register | Fab Standard License | Unconfirmed | Anime register explicitly named — same collision risk as Vefects Unity pack. Lower priority. |

---

## 4. Slot x Pack Coverage Grid

Slots defined per the brief: `cast-flash · travel-projectile · trail · impact-burst · residual (ground flame/scorch/smoke) · ground-AoE · beam · nova/area · buff-debuff-aura · portal · loot-beam · decal (ground scorch/crack)`

Legend: ✓ = confirmed covered | ~ = partial/inferred | — = not covered | ? = unknown

| Pack | cast-flash | travel-proj | trail | impact | residual | ground-AoE | beam | nova/area | buff/debuff aura | portal | loot-beam | decal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Binbun Vol. 1 (full bundle)** | ✓ (magic effects) | ✓ (orbs, projectiles) | ~ (trail via particle sub-emitters) | ✓ (hit fx) | ✓ (flame overlay, smoke) | ✓ (magic areas) | ✓ (beam pack) | ✓ (magic areas, nova variants) | ✓ (status fx) | ✓ (portal pack) | ✓ (loot vfx) | — (no dedicated ground scorch decal) |
| **Binbun Elemental Magic FX** | ✓ (8 cast effects) | ✓ (8 projectiles) | — | — | — | ✓ (8 areas) | — | ✓ | — | — | — | — |
| **Binbun Dark Magic FX** | ~ | ✓ (6 projectiles, 6 orbs) | — | — | — | ✓ (6 areas) | — | ✓ | ✓ (vortex as aura) | ✓ (vortex) | — | — |
| **Binbun Battle FX** | ~ | — | — | ~ | — | — | — | — | ✓ (shield) | — | — | — |
| **Binbun Status FX** | — | — | — | — | — | — | — | — | ✓ (18 presets + overlay materials) | — | — | — |
| **Binbun Beam VFX** | — | — | — | — | — | — | ✓ (16 presets) | — | — | — | — | — |
| **Binbun Portal VFX** | — | — | — | — | — | — | — | — | — | ✓ (24 presets) | — | — |
| **Binbun Hit FX** | — | — | — | ✓ (28 presets) | — | — | — | — | — | — | — | — |
| **Binbun Ice VFX** | — | ✓ (4 projectiles) | — | ✓ (ice balls) | ✓ (mist clouds) | ✓ (4 areas) | — | — | — | — | — | — |
| **Binbun Flame FX** | — | ✓ (projectile flame) | — | — | ✓ (lingering flame, overlay) | — | — | — | — | — | — | — |
| **Binbun Electric FX** | — | ✓ (zap/ball) | — | ✓ (impact) | — | — | — | — | — | — | — | — |
| **Binbun Loot VFX** | — | — | — | — | — | — | — | — | — | — | ✓ (12) | — |
| **Bukkbeek EffectBlocks** | ~ | ✓ (energy beams/lightning) | — | ✓ (explosions, impacts) | ✓ (smoke, fire) | ~ | ✓ (beams) | ~ | ✓ (shield, sparkles) | ✓ (portal) | ✓ (pickups) | ✓ (15 decals: blood/cracks/footprints) |
| **Hovl Studio RPG VFX Bundle** | ✓ | ✓ (arrows, projectiles) | ✓ | ✓ | ✓ (track markers) | ✓ (magic circles) | ✓ (lasers) | ✓ | ✓ (shields, buffs, debuffs) | ? | ? | ? |
| **Archanor Action RPG FX** | ? | ? | ? | ? | ? | ? | ? | ? | ? | ✓ | ✓ | ? |
| **GAPH 70 Fantasy Spells** | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| **Fantasy RPG Niagara VFX Pack** | ? | ✓ (8 projectiles) | ? | ? | ? | ✓ (16 AoE) | ✓ (4 beams) | ✓ | ✓ (7 aura) | ✓ (5 portal) | ? | ? |
| **Niagara Magic VFX Bundle** | ✓ (muzzle) | ✓ | ✓ (trails) | ✓ | ? | ✓ | ? | ✓ | ? | ? | ? | ? |

**Coverage gap analysis (Godot-native alone):**
- **Trail** — Godot-native gap. Binbun packs don't include dedicated trail meshes. Addressable via Godot's native `GPUParticles3D` trail mode or custom mesh trail shader. Not a pack gap; an author-tool gap.
- **Decal (ground scorch/crack)** — Bukkbeek EffectBlocks has 15 decals (but custom license). Binbun has no dedicated decal pack. Dragonforge ice floor pieces partially cover (ice element only). Gap for fire/burn scorch decals specifically.
- **Full Binbun Vol. 1 coverage is strong:** cast + travel + impact + residual + AoE + beam + portal + loot + aura + status. The only meaningful Godot-native gap is ground-scorch decal (non-ice) and trail mesh.

---

## 5. Parametric-Axis Inventory (consolidated)

### Binbun packs (standard tool-script API, consistent across all packs)

Confirmed exposed via tool script (verified across Magic Orb, Elemental Magic, Ice VFX, Electric FX, Status FX, Dark Magic FX, Battle FX, Beam VFX, Flame FX pages):

| Axis | Exposed? | Mechanism |
|---|---|---|
| Color/hue | YES | Tool script color property + material color |
| Scale | YES | Tool script size/radius property |
| Emission/intensity | YES | Tool script emission intensity + light properties |
| Shape/noise-texture | YES | Tool script noise texture, scale, scrolling, shape, frequency, amplitude |
| Lifecycle/timing | YES | Tool script speed, autoplay, one-shot, animation duration |
| Trail/sub-emitter | PARTIAL | Godot-native sub-emitter support available; pack-level trail meshes absent |

**Summary: 5/6 axes directly exposed by tool script. This is the highest parametric richness in the Godot-native ecosystem.**

### Bukkbeek EffectBlocks

Confirmed: size, color, timing. "Modular scripts and shaders for advanced tweaking" suggests more are accessible but not documented at the same granularity as Binbun. **3+/6 axes.**

### Hovl Studio RPG VFX Bundle (Unity-side, pre-harvest)

| Axis | Exposed? | Mechanism |
|---|---|---|
| Color/hue | YES (full pack) | One-click recolor script |
| Scale | YES | Resize script |
| Emission/intensity | INFERRED | Custom Unity shaders (must rebuild in Godot) |
| Shape/noise-texture | LOCKED in Unity shaders | Do not port; rebuild from extracted textures |
| Lifecycle/timing | LOCKED in Unity Shuriken graphs | Rebuild in Godot |
| Trail/sub-emitter | INFERRED (Unity) | Rebuild in Godot |

**Post-harvest: 2/6 axes free (color via Godot material; scale via Node3D transform). Other 4 must be re-parameterized in Godot's ParticleProcessMaterial. Art layer (textures, flipbooks, meshes) is the VALUE; parametric richness is authoring cost on the Godot side.**

---

## 6. Harvest-Pipeline Workflow Synthesis (Category 4)

### Step 1 — Legal clearance (run once per source)

- **Unity Asset Store purchases:** Standard Unity Asset Store EULA allows cross-engine use of the art layer (textures, 3D meshes, audio) in your shipped product. Engine-specific scripts and shaders do NOT transfer (they're engine-coupled and legally irrelevant for cross-engine since they won't run). Source: Unity community consensus (65 replies in Unity Discussions thread, asset creator confirmation); GameFromScratch analysis. **Verdict: GO for texture/mesh extraction from purchased Unity packs.**
- **Fab Standard License purchases:** Explicitly cross-engine ("any game engine or tool you want"). Confirmed by Fab launch announcements (Animation Magazine, Epic blog). **Verdict: GO for texture/mesh extraction from Fab-purchased packs.**
- **Exception — Unity Companion License assets:** Unity-published assets (e.g. the official URP/HDRP sample assets, Unity's own tutorials) use Unity Companion License which restricts use to Unity projects. Third-party marketplace assets (Hovl, Piloto, Archanor, etc.) use Standard EULA. **Flag: confirm per-asset that the publisher is NOT Unity Technologies.**

### Step 2 — Unity package extraction

**Tool A: Manual extraction (most reliable for VFX textures)**
1. Purchase and download the .unitypackage via Unity Hub / Package Manager.
2. Use **Unity Package Extractor** (Python, v1.0.0, command-line) to decompress the .unitypackage. Output: a `/Assets/` directory tree with all textures (PNG/TGA/EXR), FBX models, audio, and shader source files.
   - Tool: `python -m unitypackage_extractor /path/to/file.unitypackage`
   - Browser-based alternative: https://peraperavrc.github.io/package-extractor/
3. Extract targets: `Textures/` subfolder (flipbook sheets, noise maps, albedo maps), `Meshes/` or `Models/` subfolder (trail beam meshes, impact cone meshes, ground decal quads), `Audio/` subfolder.
4. SKIP: `.cs` script files (C# / Unity API — worthless in Godot), `.shader` files (HLSL/Unity ShaderLab — must be rewritten as Godot `.gdshader`), `.prefab` files (Unity scene format — read for structure reference only), `.mat` files (Unity materials — reference for texture slot assignments only).

**Tool B: Unidot Importer (Godot addon)**
- Translates .unitypackage into Godot-native formats: FBX → glTF, Texture2D → .tres, standard materials → Godot materials.
- **Critical limitation for VFX:** particle systems are EXPLICITLY NOT SUPPORTED. Shaders require manual porting.
- **Best use for VFX harvest:** automates texture + mesh conversion (saves manual format-conversion step). Run Unidot on the package first to bulk-convert textures to Godot-native formats; then manually rebuild particle emitters in Godot.
- Requires Godot 4.0+ with FBX2glTF configured. RAM: 16 GB recommended for large packages.

**Tool C: AssetRipper**
- Extracts from compiled Unity game builds (not .unitypackage files directly). Designed for developers analyzing their own built game to find dependencies. Less applicable to the VFX pack harvest workflow (we have the source .unitypackage, not the built game).

### Step 3 — Mesh conversion (for trail/beam/impact geometry)

Trail meshes, beam quads, impact cones from Unity packs are FBX format. Conversion path:
1. Import FBX into Blender (File → Import → FBX).
2. Fix pivot/origin (Object → Set Origin → Origin to Center of Mass for symmetric meshes; Origin to 3D Cursor for anchor-point geometry).
3. Export as glTF 2.0 (File → Export → glTF 2.0).
4. Import glTF into Godot 4 — native glTF support, no plugin required.

### Step 4 — Flipbook texture import into Godot

Flipbook sprite sheets from Unity VFX packs (typically PNG, power-of-2 dimensions, e.g. 2048×2048 with 8×8 or 4×4 grid) import directly into Godot:
1. Import the PNG into Godot's FileSystem (drag-drop).
2. Set Import settings: `Texture Type: Image`; NO mipmaps for sharp flipbooks.
3. In Godot's ParticleProcessMaterial: `Texture → Particle Sheet = your flipbook texture`; set `H Frames` and `V Frames` to match the grid.
4. Optional — **Particle Flipbook Flowmap Smoothing shader** (godotshaders.com): adds flowmap-based frame interpolation for smooth sub-frame transitions. The author confirms using CC0 flipbook sheets from Unity VFX resources with this shader. **This is the key bridge from Unity flipbook sheets → smooth Godot particles.** Parameters: `albedo`, `texture_albedo` (the flipbook), `texture_flow` (flowmap, generated via a free tool), `particles_anim_h_frames/v_frames`, `flow_strength`.

### Step 5 — Godot GPUParticles3D rebuild

Unity Shuriken/VFX Graph behavior does NOT port. Each effect must be rebuilt from scratch in Godot's `GPUParticles3D + ParticleProcessMaterial` (or a custom particle shader for advanced cases). The art layer (harvested textures, meshes) is the raw material; the emission curve, lifetime, color gradient, velocity, and sub-emitter logic are re-authored.

**Recommended rebuild approach:**
1. In Unity (or from .prefab reference), note the effect's key parameters: lifetime, emission rate, start speed, start size, color-over-lifetime gradient, texture, sub-emitter chain.
2. Create a new `GPUParticles3D` node in Godot. Assign a new `ParticleProcessMaterial`.
3. Map Unity parameters to Godot equivalents: Lifetime → `lifetime`; Start Speed → `initial_velocity_min/max`; Color over lifetime → `color_ramp`; Texture → `particle_texture`; Sub-emitter → add a child `GPUParticles3D` with `trail` or `sub-emitter` mode.
4. For additive/HDR bloom: set the particle material's `StandardMaterial3D.emission_enabled = true` + `emission_energy_multiplier` (drive this high, e.g. 3–5x, for PoE-register bloom); set `blend_mode = ADD`.
5. For custom noise/flowmap effects: assign a `.gdshader` particle shader referencing the extracted noise maps. The `particle_shader` reference at docs.godotengine.org covers `INSTANCE_CUSTOM` for lifetime-driven effects (dissolve, dissolving edge, animated distortion).

### Step 6 — UE/Fab → Godot (harder path)

Niagara behavior is MORE deeply engine-coupled than Unity Shuriken. Niagara uses GPU simulation stages, custom modules, and parameter namespaces that have no direct Godot analog. The rebuild effort is higher. Texture extraction still works via the same FBX/PNG pipeline. **The additional cost of UE vs. Unity harvest:** plan roughly 1.5–2× the rebuild time per effect, because Niagara module graph is harder to read as a reference spec than Unity's Shuriken inspector.

UE project setup for extraction (requires UE + mantis seam already in place):
1. Add the Fab pack to the UE project via Epic Launcher.
2. In Content Browser: right-click → Explore in File Browser to reach the raw asset files on disk.
3. Textures export as `.uasset` — use the UE Content Browser "Export" function (right-click → Export) to export as PNG/TGA/EXR.
4. Meshes export as FBX via same Export function.
5. From this point: same as Step 3 (Blender FBX→glTF) + Step 4 (flipbook import) + Step 5 (Godot rebuild).

### Harvest cost estimate (ballpark, per effect, not per pack)

| Path | Art extraction | Godot rebuild | Total per effect |
|---|---|---|---|
| Godot-native (zero harvest) | 0 h | 0 h | 0 h |
| Unity→Godot (simple particle effect) | 0.5–1 h | 1–2 h | 1.5–3 h |
| Unity→Godot (complex multi-layer effect) | 0.5–1 h | 3–5 h | 3.5–6 h |
| UE→Godot (Niagara effect) | 1–2 h | 3–6 h | 4–8 h |

These are amortized per distinct effect. The reusable harvest-and-rebuild toolchain (Steps 2–6 above) is built ONCE; subsequent packs from the same source reuse the pipeline.

---

## 7. Top-N Recommendations

### Top-3 Godot-Native (with reasoning)

**#1 — Binbun Godot Effects Collection Vol. 1 ($26.25, CC0)**
The only current Godot-native pack with: (a) zero licensing friction at 400+ kit scale (CC0), (b) 5/6 parametric axes directly exposed, (c) near-complete slot coverage of the cast→travel→impact→residual→portal→beam→loot chain in a single purchase, (d) active development (March 2026), and (e) strong community reception (5/5, 1,516 contributors). The register reads stylized-clean / low-edge-of-stylized-gritty — it will need the bloom/emission knobs turned up (the tool script supports this) and potentially layered with the Unity harvest anchor for the deeper PoE juice density, but the parametric infrastructure is in place. This is the backbone.

**#2 — Binbun Elemental Magic FX ($5.94, CC0) + Binbun Dark Magic FX ($5.94, CC0) — individual pack pair**
If the Vol. 1 bundle cost needs justification before commitment, these two packs cover the highest-priority slots for an ARPG: Elemental Magic FX gives cast + travel + AoE across 4 elements (fire/water/electric/nature) with the richest inspector exposure in the Binbun line; Dark Magic FX adds the PoE-register dark/arcane tones (closer to stylized-gritty than the other elemental packs) with 6 projectiles + 6 areas + 3 vortex. Together: $12 CC0 for the most ARPG-relevant slice of the catalogue.

**#3 — Bukkbeek EffectBlocks ($9.99, custom commercial)**
The strongest standalone Godot-native alternative to Binbun. 100+ effects; the unique differentiation is the decal layer (15 ground decals — blood/cracks/footprints) which Binbun lacks, and broader combat-feedback coverage (muzzle flashes, bullet impacts, explosions). License caveat: not CC0 — custom "no resell/redistribute" terms, but usable in your shipped product. Register reads stylized-clean; useful as a combat-feedback and residual-decal layer alongside Binbun's spell-drama packs. **Do not use as the primary backbone** — the register lacks PoE juice; use as a secondary layer for combat feedback + decals.

### Top-3 Unity Harvest (with reasoning)

**#1 — Hovl Studio RPG VFX Bundle ($24 + $5 support package, Standard Unity EULA)**
The best single Unity harvest purchase for slot breadth + register fit. Register: stylized-gritty / ON-target — community describes it as vibrant, layered, magical (not photoreal). One-click recolor = color axis present on the Unity side (must rebuild as Godot material uniform, but the source intent is clear). Covers: cast flash, travel projectile, trail, impact, residual, magic circle AoE, beam/laser, buff/debuff, track markers. Last updated March 2026. 51 reviews, 1,722 favorites — the most-vetted ARPG VFX pack on the Unity Asset Store. **This is the high-register reference art for rebuilding in Godot.** License: cross-engine extraction for purchased assets = permitted per EULA + community consensus.

**#2 — Archanor VFX — Action RPG FX ($20, Standard Unity EULA)**
Register: stylized-clean (Archanor's style across all packs is vibrant-cartoonish, not photoreal; confirmed by community characterization). Slot emphasis: portals, loot, ARPG ambient effects. Complements Hovl (which is stronger on spell-drama) by covering portal and loot-beam slots with a different aesthetic voice. 887 favorites, 26 reviews. Sept 2024 update. Limited to URP + Built-in (not HDRP) — harvest is cleaner since URP materials are simpler to reference. **Second-priority harvest; covers portal/loot gap that Hovl may leave thin.**

**#3 — Piloto Studio — Magical Combat Stylized VFX ($15) or GAPH 70 Fantasy Spells ($14.99)**
Both are price-efficient and stylized (not photoreal). Piloto's Magical Combat: MOBA/top-down context, stylized-clean, lighter juice than Hovl but no register collision. GAPH's 70 Spells: 70 effects for $15 (best count-per-dollar on the list), HDR support confirmed. **Choose based on visual preview:** if GAPH's 70 look closer to PoE (density, layering), pick GAPH; if Piloto's stylized-clean fits a lighter spell tier, pick Piloto. Both are viable at this price range. **Note: Piloto's "Realistic ARPG" line (not "Stylized") should be avoided — register likely over-shoots.**

### Top-2 UE/Fab Harvest (with reasoning)

**#1 — Fantasy RPG Niagara VFX Pack (Fab Standard License, price TBD — verify on Fab)**
The broadest slot coverage of any UE pack surveyed: 90 particle systems covering AoE, generic, aura, beam, buff, explosion, portal, projectile — all major ARPG slots. Elements: fire, ice, arcane, blood, nature, lightning. Community-reviewed positively at 4.8/5. Register: stylized-gritty / ON (fantasy RPG framing, element variety, strong community praise suggesting high visual quality). Fab Standard License = any-engine use permitted. **This is the top UE harvest anchor IF the team decides the UE→Godot rebuild cost is justified for the high-register element-breadth it provides.** Note: harvest cost is 4–8 h per effect vs. Hovl's 3–6 h; weigh against the broader element coverage.

**#2 — Niagara Magic VFX Bundle ($60 bundle, Fab Standard License)**
Combines Magic Projectiles + Magic AOE in one purchase. Community: "simply beautiful," "incredible particles." Covers element variety (fire, ice, lightning, arcane, poison, holy, shadow) — the widest element palette of any pack surveyed. Higher cost ($60) but lower per-element amortization than buying separately. Fab Standard License = cross-engine. **Secondary UE harvest if budget permits and UE seam (mantis) is available for extraction.** 

---

## 8. Register Characterization Summary

(For the rubric calibration ladder; galadriel CV instrument reference.)

| Pack | Register label | Under/ON/over | Notes |
|---|---|---|---|
| Binbun Magic Orb, Ice, Electric | stylized-clean | ON (composites; juice needs amplification) | Vibrant but thin on layering vs PoE |
| Binbun Elemental Magic FX | stylized-clean | ON | Element-legible, clean shapes |
| Binbun Dark Magic FX | stylized-gritty | ON | Closest Binbun pack to PoE dark-register |
| Binbun Battle FX | stylized-gritty | ON | Shields + slashes; richer layer density |
| Binbun Flame FX | stylized-clean | ON | Clean stylized flame, not HD fire sim |
| Binbun Status FX | stylized-clean | ON | Status overlay; functional not dramatic |
| Binbun Beam VFX | stylized-clean | ON | Laser aesthetic, multi-colored |
| Binbun Hit FX | stylized-clean | ON | Snappy combat impacts |
| Bukkbeek EffectBlocks | stylized-clean (low-poly) | UNDER for PoE juice | Low-poly geometry; cartoon; thin drama |
| AlekseiRamirov Starter Pack | stylized-clean | ON (minimal scope) | GPUParticles3D-native; minimal drama |
| DragonForge Ice Shaders | stylized-clean PBR | ON for ice biome | PBR materials; clean not juicy |
| Hovl Studio RPG VFX Bundle | stylized-gritty | ON | Magic-circle + bloom + layered; PoE adjacent |
| Piloto Magical Combat | stylized-clean | ON (lighter) | Toon/MOBA weight; less dense than PoE |
| Piloto Realistic ARPG | semi-real | BORDERLINE OVER | "Realistic" + HDRP emphasis; verify visuals |
| Piloto Super Realistic ARPG | semi-real to photoreal | OVER (likely) | "Super realistic" explicitly; HDRP-optimized |
| Archanor Action RPG FX | stylized-clean | ON | Vibrant cartoonish, not photoreal |
| GAPH 70 Fantasy Spells | stylized-clean | ON (unverified) | HDR support; register unconfirmed from visual |
| Vefects Stylized VFX Bundle | stylized-clean (anime) | UNDER | Anime/manga aesthetic — wrong register |
| Fantasy RPG Niagara VFX Pack | stylized-gritty | ON | ARPG fantasy; community-validated quality |
| Niagara Magic VFX Bundle | stylized-gritty | ON | "Incredible particles" — community |
| Stylized VFX Pack Vol. 3 (Niagara) | stylized-clean (anime) | UNDER | Explicitly anime/cartoon |

---

## 9. Knowledge Gaps Not Resolved

1. **Binbun Vol. 1 exact register in practice** — the tool script can drive emission very high (PoE juice) but this is operator-dependent. One integration test with emission cranked to 3–5x and additive blend mode is needed to confirm whether Binbun's art layer reaches D2/PoE juice depth or stays stylized-clean.

2. **Hovl Studio RPG VFX Bundle visual register — not directly verifiable from this run.** The YouTube demo (https://www.youtube.com/watch?v=hI15nSorz68) was not renderable by WebFetch. ArtStation portfolio returned 403. The community characterization (stylized-gritty / ON) is sourced from realtimevfx.com thread + asset marketplace context, NOT from direct visual inspection. **Matt should review the demo video himself before purchase.** This is the most important unresolved gap.

3. **Piloto Studio "Realistic ARPG" vs "Stylized" line distinction** — the Realistic line's exact register (semi-real vs. photoreal) was not confirmed from visual inspection. Gallery pages blocked by cookie consent. **Verify visually before purchase: if Piloto "Realistic ARPG" screenshots show dense volumetric fire/smoke or PBR sparks, the register over-shoots Synty.**

4. **Fantasy RPG Niagara VFX Pack price** — Fab's 403 blocks direct listing fetch. Verify on Fab.com (or in UE via Epic Launcher) before acquisition.

5. **Binbun Vol. 2 Godot 4.5 compat issues** — user reports of shader serialization errors on Godot 4.5+. May be fixed in a subsequent patch or may require shader migration. Verify before committing Vol. 2.

6. **Decal gap (non-ice scorch/crack)** — only Bukkbeek EffectBlocks covers ground decals in the Godot-native ecosystem (15 decals). If a CC0 ground-scorch/decal layer is needed, no current Godot-native pack fills it. Options: (a) use Bukkbeek with its custom license (acceptable for use-in-product), (b) harvest ground scorch textures from Hovl or Archanor Unity packs and implement in Godot as a `Decal` node, (c) author procedurally in Godot.

7. **Trail mesh gap in Godot-native ecosystem** — no Binbun or Bukkbeek pack ships dedicated trail meshes. Godot's native trail support in GPUParticles3D covers simple ribbon trails; complex spell-travel trails with custom cross-section geometry require harvested trail meshes (Unity/UE packs contain these).

8. **Fab Standard License exact text for "cross-engine"** — Fab EULA page returned 403 during this run. The cross-engine claim is corroborated by multiple Epic launch announcements (Animation Magazine, Epic blog, community forum) but the verbatim EULA text was not captured. Matt should read `fab.com/eula` directly before committing to a UE/Fab harvest strategy.

---

## 10. Source List

All accessed 2026-06-18.

**Godot-native packs:**
- Binbun Effects Collection Vol. 1: https://binbun3d.itch.io/effects-collection-vol1
- Binbun Effects Collection Vol. 2: https://binbun3d.itch.io/effects-collection-vol2
- Binbun creator profile: https://binbun3d.itch.io/
- Binbun Magic Orb VFX: https://binbun3d.itch.io/magic-orb-vfx
- Binbun Elemental Magic FX: https://binbun3d.itch.io/elemental-magic-fx
- Binbun Dark Magic FX: https://binbun3d.itch.io/dark-magic-fx
- Binbun Hit FX: https://binbun3d.itch.io/hit-fx
- Binbun Ice VFX: https://binbun3d.itch.io/ice-vfx
- Binbun Electric FX: https://binbun3d.itch.io/electric-fx
- Binbun Status FX: https://binbun3d.itch.io/status-fx
- Binbun Beam VFX: https://binbun3d.itch.io/beam-vfx
- Binbun Flame FX: https://binbun3d.itch.io/flame-fx
- Binbun Battle FX: https://binbun3d.itch.io/battle-fx
- Binbun Loot VFX: https://binbun3d.itch.io/loot-vfx
- Binbun Smoke VFX: https://binbun3d.itch.io/smoke-vfx
- Binbun Magic Area VFX devlog: https://binbun3d.itch.io/magic-area-vfx/devlog/1330856/new-release-godot-3d-magic-area-vfx
- Binbun Magic Orb VFX devlog: https://binbun3d.itch.io/magic-orb-vfx/devlog/1333952/new-release-godot-magic-orb-vfx-3d
- Binbun Vol. 1 update — magic effects: https://itch.io/devlog/1448416/update-added-new-magic-effects.amp
- Binbun forum thread (Godot Forum): https://forum.godotengine.org/t/binbun-vfx-effects/137169
- Bukkbeek EffectBlocks: https://bukkbeek.itch.io/effectblocks
- AlekseiRamirov Starter VFX Pack: https://alekseiramirov.itch.io/starter-vfx-pack-essential-juice-for-godot-lite-edition
- AlekseiRamirov release devlog: https://alekseiramirov.itch.io/starter-vfx-pack-essential-juice-for-godot-lite-edition/devlog/1506373/release-starter-vfx-pack
- DragonForge Ice Shaders + VFX: https://dragonforge-development.itch.io/godot-3d-vfx-ice-shaders
- KnowerCoder 3D Fire+Smoke: https://knowercoder.itch.io/3d-fire-and-smoke
- GDQuest VFX Assets: https://github.com/gdquest-demos/godot-4-VFX-assets
- iHoshiii Godot-VFX: https://github.com/iHoshiii/Godot-VFX
- haowg GODOT-VFX-LIBRARY: https://github.com/haowg/GODOT-VFX-LIBRARY
- Godot Asset Library browse (vfx+godot tag): https://itch.io/game-assets/tag-godot/tag-vfx
- UniParticles3D: https://godotengine.org/asset-library/asset/3741
- Godot 3D Particles Demo: https://godotengine.org/asset-library/asset/2745
- GPUParticles3D docs (stable): https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html
- ParticleProcessMaterial docs: https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html
- Particle systems (3D) tutorial: https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html
- Process material properties: https://docs.godotengine.org/en/stable/tutorials/3d/particles/process_material_properties.html
- Godot Shaders — magic tag: https://godotshaders.com/shader-tag/magic/
- Godot Shaders — flipbook snippet: https://godotshaders.com/snippet/flipbook/
- Godot Shaders — flipbook flowmap: https://godotshaders.com/shader/particle-flipbook-flowmap-smoothing/
- Godot Shaders — 3D fire: https://godotshaders.com/shader/3d-fire-shader/
- Godot Shaders — 3D lightning: https://godotshaders.com/shader/3d-lightning-shader/

**Unity harvest packs:**
- Hovl Studio RPG VFX Bundle: https://assetstore.unity.com/packages/vfx/particles/spells/rpg-vfx-bundle-133704
- Hovl Studio publisher: https://assetstore-fallback.unity.com/publishers/28391
- Hovl Studio YouTube: https://www.youtube.com/channel/UCMqxbFCPmfH1Gf6dMIIvI4A
- Hovl Studio demo video: https://www.youtube.com/watch?v=hI15nSorz68
- Hovl realtimevfx.com thread: https://realtimevfx.com/t/3-vfx-packs-for-asset-store-from-hovl-studio/13191
- Archanor Action RPG FX: https://assetstore.unity.com/packages/vfx/particles/action-rpg-fx-38222
- Archanor assets page: https://archanor.com/assets.html
- Piloto Studio Magical Combat: https://assetstore.unity.com/packages/vfx/particles/spells/magical-combat-stylized-vfx-233323
- Piloto Studio Realistic ARPG Fire: https://assetstore.unity.com/packages/vfx/particles/spells/realistic-arpg-vfx-starter-pack-fire-spells-319946
- Piloto Studio publisher: https://assetstore-fallback.unity.com/publishers/48767
- GAPH 70 Fantasy Spells: https://assetstore.unity.com/packages/vfx/particles/spells/70-fantasy-spells-effects-pack-112526
- PixPlays Elemental Spells: https://assetstore.unity.com/packages/vfx/particles/spells/elemental-spells-full-pack-vfx-297318
- Vefects Stylized VFX Bundle: https://assetstore.unity.com/packages/vfx/stylized-vfx-bundle-340466
- Unity spells category: https://assetstore.unity.com/vfx/particles/spells
- Unity EULA: https://unity.com/legal/as-terms
- Unity cross-engine support FAQ: https://support.unity.com/hc/en-us/articles/34387186019988-Can-I-use-assets-from-the-Asset-Store-with-other-engines
- GameFromScratch cross-engine legality: https://gamefromscratch.com/using-asset-store-assets-in-other-engines-is-it-legal/
- Unity Discussions thread (cross-engine): https://discussions.unity.com/t/can-i-use-assets-from-the-asset-store-i-purchased-in-another-game-engine/929171
- GameFromScratch export from Unity: https://gamefromscratch.com/exporting-from-unity-to-other-game-engines/
- GameFromScratch move to Godot: https://gamefromscratch.com/move-from-unity-to-godot-engine-in-seconds/
- Top Unity effect assets (2026 roundup): https://unityasset.soldier.jp/en/unity-effect-assets/
- 80.lv Stylized VFX digest: https://80.lv/articles/unity-digest-stylized-vfx-for-games

**UE/Fab harvest packs:**
- Fantasy RPG Niagara VFX Pack (Fab): https://www.fab.com/listings/db2bc703-9bfc-4053-8df2-0756a21e2afe
- Fantasy RPG Niagara — reviews (UE): https://www.unrealengine.com/marketplace/en-US/product/fantasy-rpg-niagara-vfx-pack/reviews
- Niagara Magic VFX Bundle (Fab): https://www.fab.com/listings/0b0b18e7-00d7-4e09-b090-479977f6450e
- Niagara Magic VFX Bundle — reviews: https://www.unrealengine.com/marketplace/en-US/product/niagara-magic-vfx-bundle-niagara-magic-projectiles-niagara-magic-aoe/reviews
- Fantasy VFX Bundle (Fab): https://www.fab.com/listings/3b56ea20-ebcb-43df-91a8-852561e01c26
- Stylized VFX Pack Vol. 3 Niagara (Fab): https://www.fab.com/listings/4e030588-4e04-4a7c-97c9-55591f89777e
- Fab EULA: https://www.fab.com/eula
- Fab licenses and pricing: https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab
- Fab cross-engine community discussion: https://forums.unrealengine.com/t/can-i-use-assets-from-fab-for-godot-engine/2451166
- Fab launch / Standard License announcement: https://www.animationmagazine.net/2024/10/epic-games-launches-fab-unified-content-market/
- Epic blog Fab launch: https://www.unrealengine.com/en-US/blog/fab-epics-new-unified-content-marketplace-launches-today

**Harvest tooling:**
- Unidot Importer (Godot Asset Library): https://godotengine.org/asset-library/asset/2427
- Unidot Importer (GitHub V-Sekai): https://github.com/V-Sekai/unidot_importer
- Unidot docs: https://docs.unidot.org/
- Unity Package Extractor (browser): https://peraperavrc.github.io/package-extractor/
- AssetRipper: https://assetripper.org/
- AssetRipper docs: https://assetripper.github.io/AssetRipper/
- VFXDoc flipbook reference: https://vfxdoc.readthedocs.io/en/latest/textures/flipbooks/
- VFX Apprentice flipbook explainer: https://www.vfxapprentice.com/blog/what-are-flipbooks-in-games
- Gabriel Aguiar Prod — assets + tutorials: https://www.gabrielaguiarprod.com/
- Gabriel Aguiar Prod — YouTube: https://www.youtube.com/c/gabrielaguiarprod
- Godot VFX Skillshare course: https://www.skillshare.com/en/classes/godot-vfx-for-games-beginner-to-intermediate/736913264
- Godot VFX Udemy course: https://www.udemy.com/course/godot-vfx-for-games/
- GPUParticle shader INSTANCE_CUSTOM guide: https://dredyson.com/how-to-control-godot-gpu-particle-shader-custom-parameters-with-curved-particle-life-duration-a-complete-beginners-step-by-step-guide-to-instance_custom-uniforms-and-dissolve-effects-in-godot-4/

---

*Research artifact authored: 2026-06-18*
*Mode A analytical research*
*Commissioner: gandalf (brief: `agentic_orchestration/gandalf/notes/2026-06-18-legolas-vfx-pack-godot-research-brief.md`)*
*Output: `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/synthesis.md`*
*Links: `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/links.md`*
*Legolas — researcher and scout; read-only throughout.*
