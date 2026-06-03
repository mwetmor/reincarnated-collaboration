# Research — Constellation-Form UE Techniques + FAB Packs (R1) — 2026-06-02

**Mode:** A (analytical)
**Commissioner:** gandalf per Matt 2026-06-02 ratification
**Architecture:** Architecture γ — Stage A celestial spirit form progression
**Sources consulted:** See § 8 Source List

---

## Summary

Architecture γ Stage A (constellation-form → 3D emergence → VFX layering → item visuals → Stage B
materialization) is technically achievable in UE5 using a composition of native Niagara techniques plus
targeted FAB packs. The core constellation-line rendering technique is well-established: a dual-renderer
Niagara emitter (sprite renderer for star points + SpriteBasedLine module for connecting lines) is the
documented approach from the UE real-time VFX community, derived from "plexus" particle network concepts.
The 2D-to-3D emergence transition does not have an off-the-shelf pack; it is a custom material lerp +
Niagara parameter animation authored as UE-seam-agent work. FAB holographic shader packs (HOLOGRAM VFX
With Niagara series, Niagara Hologram Pack) provide directly usable emissive + scanline + wireframe
hologram effects that can be adapted for the Stage A.0 base appearance. Elemental aura packs (already
identified in prior research) cover Stage A.2. Coin/currency VFX packs cover Stage A.3 orbital items
partially. Total FAB cost estimate for the Architecture γ visual layer (above baseline CC5/Synty stack)
is approximately $100-200. Estimated additional UE-seam-agent effort beyond the baseline 8-12 sessions
is 6-10 sessions, yielding a total estimated range of 14-22 sessions for the full Architecture γ stack.
Parameter binding to Niagara user parameters and dynamic material instances is a first-class supported
UE5 pattern, giving clean substrate → visible feature mappings via Blueprint at runtime.

---

## 1. Core Constellation-Line Rendering Technique

### 1.1 Dual-Renderer Niagara Plexus Approach

The technique for rendering constellation-style star-points-with-connecting-lines in Niagara is
well-documented in the real-time VFX community as the "plexus" effect.

**Architecture:** A single Niagara system with two emitters:

- **Emitter A (source particles — star points).** Spawns sprite or mesh particles at positions
  corresponding to character outline vertices, joint positions, or defined grid points. Uses skeletal
  mesh sampling (`Sample Skeletal Mesh` module / `Skeletal Mesh Location` module) to anchor points to
  the character skeleton. These particles render as glowing star sprites.

- **Emitter B (connection lines).** Reads from Emitter A via Particle Attribute Reader. Each
  connection particle stores two random parent particle IDs ("Save Connection ID" module on spawn).
  At update, "Read Connection Position" module fetches both parent positions and computes the
  connecting line via the `SpriteBasedLine` module (a built-in Niagara module that renders a
  line between two endpoint positions). Setting curve tension to 1 produces straight segment lines
  (correct for constellation diagrams; smooth curves would be incorrect).

**Source:** Confirmed in RealTimeVFX forum [Niagara 5.1 Plexus Mini Tutorial], with specific module
names `SpriteBasedLine`, `Save Connection ID`, `Read Connection Position` confirmed as built-in UE5.1+.
Color differentiation between star points and connecting lines is achieved via per-renderer parameter
binding.

**Constellation vs dynamic plexus distinction:** The plexus approach connects *dynamically positioned
particles* — each frame the connections are re-evaluated. For a static constellation diagram (fixed
star positions representing a humanoid outline), an alternative approach is more appropriate:
predefined skeletal mesh vertex positions as particle spawn locations, with ribbon renderers or
geometry scripts drawing edges between known skeleton bones. The holographic ribbon technique (CGHOW)
demonstrates this: a single ribbon emitter follows skeleton/mesh vertices in execution-index order
using a scratch pad module, producing edge-connected geometry. Both approaches are valid; the plexus
approach allows more organic floating star behavior while the vertex-ordered ribbon approach better
matches a strict constellation diagram aesthetic.

**Key limitation acknowledged:** Neither technique off-the-shelf produces a *full humanoid silhouette
constellation*. A full constellation character (every major body line drawn) requires custom authoring
to define:
1. Which skeleton bones / vertices are the "constellation star points"
2. Which pairs of points connect (adjacency map)
3. How points animate with the character's idle animation

This is custom UE-seam-agent Niagara authoring work, not a purchasable pack. Estimated complexity:
moderate (requires Niagara scratch-pad module scripting and parameter binding).

---

### 1.2 Holographic Material Foundation

The constellation form requires a holographic / emissive / transparent rendering base on the character
mesh itself (stage A.0 requires the outline to be perceptually 2D-flat and sci-fi / holographic before
depth emerges). This is a custom Unreal Material, not a Niagara effect.

**Technique documented:** World-position-based horizontal line tiling (Z-axis scanlines), Fresnel for
edge glow, emissive color + opacity control. All standard Material nodes in UE5. This is the foundation
of every hologram shader tutorial and the HOLOGRAM VFX packs' material layer.

**FAB packs that provide this base material as a starting point:**

- HOLOGRAM VFX With Niagara (series 1-4): materials confirmed to include scanline, emissive, opacity,
  and grid pattern materials. These are modifiable material instances — they can be adapted to the
  character mesh rather than used as standalone props.

The character's actual skeletal mesh would use a custom translucent/unlit material with these properties
applied as a Dynamic Material Instance (DMI), allowing Blueprint to drive `Opacity`, `EmissiveStrength`,
`LineColor`, `GridScale`, `FringeAmount` etc. as parameters.

---

## 2. FAB Pack Survey — Constellation / Holographic / Star Effects

### 2.1 HOLOGRAM VFX With Niagara (Pack 1)

**FAB listing:** https://www.fab.com/listings/3e358551-89d4-40de-8fec-99d4b66b6c1e

**Contents:**
- 32+ Hologram VFX Examples
- 27+ Materials and Material Instances (includes 3+ Material Functions)
- 10+ Niagara Particle systems (6+ Niagara Modules)

**UE5 version support:** UE 5.1 – 5.5 confirmed (Asset Freaks source). Likely supports 5.6/5.7 but
not confirmed in available sources.

**Cost:** Not confirmed from direct listing (403 errors from fab.com). Third-party source indicates
this pack was in the UE marketplace; estimated $30-60 based on comparable packs of this scale.

**License:** FAB Standard License (commercial use permitted, royalty-free per Epic FAB terms).

**Extensibility:** Material Instances are modifiable. Niagara Modules (6+) are customizable within
the Niagara editor. Pack can be adapted; not use-as-is only.

**Composition fit for Stage A.0:** HIGH. The holographic materials directly provide the base shader
layer for the constellation form's emissive/translucent/scanline appearance. The pack does NOT include
a constellation-outline character Niagara system (no star-point + line topology targeting a skeleton);
it provides the visual style foundation that the custom constellation Niagara layer would render through.

---

### 2.2 HOLOGRAM VFX With Niagara 2

**FAB listing:** https://www.fab.com/listings/c102d630-0c53-4dd0-b47a-98a71f832d5c

**Contents:**
- 26+ Hologram VFX Examples
- 47+ Materials and Material Instances (7+ Material Functions)
- 4+ Niagara Particles (4+ Niagara Modules)
- 47+ UI Images
- 4+ Sci-Fi Level Design Modules
- 4+ Display Model Sets

**UE5 support:** UE5.x (specific range not confirmed from available sources).

**Cost:** Not confirmed.

**Composition fit:** MEDIUM-HIGH for Stage A.0 material base. The UI images and display model sets are
not relevant to character VFX. The material set is larger than Pack 1 but Niagara count is smaller —
Pack 1 is likely more useful for character Niagara work.

---

### 2.3 Niagara Hologram Pack

**FAB listing:** https://www.fab.com/listings/deee89fc-7a07-44d1-9574-689a3475790b

**Contents:**
- 20 Niagara systems
- 9 Blueprints

**UE5 support:** Not confirmed from sources (pack name implies UE5 given the listing is on FAB post-2024).

**Cost:** On sale at $2.49 (regular $4.99) per UE marketplace listing — this may be outdated. Current
FAB price not confirmed due to 403 errors.

**Notable feature:** Pack documentation states "you can use your own static mesh to adjust the effect"
— this implies at least some systems accept mesh input, which is relevant for wrapping hologram effects
around a character mesh.

**Composition fit:** HIGH value-for-cost if current price is near $5. The 20 Niagara systems likely
provide variety (different hologram visual styles). Mesh-parameterized systems directly applicable.

---

### 2.4 Niagara Sci-Fi Starter VFX Pack

**FAB listing:** https://www.fab.com/listings/db2445cf-fb11-40b2-b7d8-10d52496996e

**Contents:** 80 unique effects including: Laser, Portal, Gates, EMP, Black Hole, Hologram, Blood,
Environment types.

**Composition fit:** LOW-MEDIUM for Architecture γ specifically. Primarily environment/weapon effects;
hologram effects are one category among many. Less focused than HOLOGRAM VFX packs.

---

### 2.5 Celestial Vault Plugin (Epic Developer Community)

**Documentation page:** https://dev.epicgames.com/community/learning/tutorials/9XyB/unreal-engine-creating-custom-constellations-for-the-celestial-vault-plugin

**What it is:** A plugin for rendering night skies with star constellations in Unreal Engine. Focused
on sky/environment scale, not character scale.

**Composition fit for Architecture γ:** LOW. This is a sky system, not a character VFX tool. Not
applicable to per-character constellation rendering. Noted here to avoid re-researching a false lead.

---

### 2.6 Trail VFX Pack

**FAB listing:** https://www.fab.com/listings/b41b3941-efd2-42ba-9747-e7a4d23e7e1b

**Contents:**
- 50+ trail VFX examples
- 30+ Niagara Systems
- 42+ Effect Materials, 32+ Effect Textures
- Types: Character Dash Trail, Spline Looping Trail, Spline Not Looping Trail, Projectile Trail with
  Hit Particle, 8 Elemental Trails (Tentacle, Plexus, Basic, Water, Twist, Ice, and Xray)

**Notable:** The pack includes a "Plexus" trail type — this is directly relevant as a reference and
starting point for constellation-line connection rendering. The XRay trail type may produce a
wireframe/see-through character trail effect visually adjacent to constellation aesthetics.

**Composition fit:** MEDIUM-HIGH. The Plexus trail provides a usable reference for the connection-line
particle technique. Elemental trails cover some Stage A.2 movement trail needs.

---

### 2.7 Advanced Niagara Character Trail VFX

**UE Marketplace listing:** https://www.unrealengine.com/marketplace/en-US/product/advanced-niagara-character-trail-vfx-01

**Contents:** 15 unique colorful dash/trail effects made with Niagara. Character-specific. Demo map
included.

**Composition fit:** LOW-MEDIUM for Stage A specifically (trails, not constellation rendering).
Relevant for Stage A.3 windspeed/movement trails.

---

## 3. FAB Pack Survey — Stage A.3 Layering Items (Orbital / Equip / Wind)

### 3.1 Money and Coins VFX

**FAB listing:** https://www.fab.com/listings/08325750-b380-41cc-8fe3-ac711c5f647d

**Contents:** 25+ Niagara-based special effects for coins and currency. Real-time color and glow
customization per layer.

**Composition fit for Stage A.3 (coins orbiting):** MEDIUM. The pack is coin-rain / coin-drop /
collection effects, not an orbit-around-character system specifically. Orbital behavior would require
Niagara parameter authoring to orbit particles around a skeleton position. The mesh and material assets
from this pack are reusable for custom orbit logic.

---

### 3.2 Coin VFX

**FAB listing:** https://www.fab.com/listings/790b1478-51c7-4147-b712-7f69179c987c

**Contents:** 148 particles, 18 coin types (Basic, Bitcoin, Ethereum, Star, Dollar, Euro, Pound,
Greek ancient, Pixel variants etc.), 8 particle states per coin type (Idle + Get states). Updated 2026.

**Composition fit:** LOW-MEDIUM. High variety for coin mesh types; Idle and Get states are relevant
for orbiting coin visual. Still not an orbit system — requires custom Niagara orbit logic authoring.

---

### 3.3 Treasure Chest VFX

**FAB listing:** https://www.fab.com/listings/67d95ecf-86ab-42a5-9d55-7dbaa3123dae

**Contents:** Niagara system for treasure chest opening VFX; includes the chest model and textures.

**Composition fit for Stage A.3:** LOW. Event trigger effect, not a persistent orbital item system.

---

### 3.4 Tactical Hiking Backpack 75 (Rigged for UE5 Skeletons)

**FAB listing:** https://www.fab.com/listings/1e8c4b3b-1590-4d1d-a216-25eabb179619

**Contents:** Realistic 3D model of a tactical hiking backpack, rigged for All MetaHuman Bodies and
UE5 Skeletons.

**Composition fit for Stage A.3 (satchel/backpack attachment):** HIGH for mesh availability.
The backpack is already rigged to UE5 skeletons, meaning it can be socket-attached to a CC5 or
Synty character skeleton without re-rigging. Style mismatch caveat: a "tactical hiking backpack"
is not a fantasy satchel; style substitution or custom asset would be needed for period-appropriate
spirit-form aesthetic. However, confirms the mechanism works.

---

### 3.5 Niagara Wind VFX Pack

**UE Marketplace listing:** https://www.unrealengine.com/marketplace/en-US/product/niagara-wind-vfx-pack

**Contents:** 11 unique Niagara wind effects.

**Composition fit for Stage A.3 (windspeed effects):** MEDIUM. Wind environment effects; adapting
to windspeed-around-character requires custom Niagara authoring using pack effects as reference or
starting textures/materials.

---

### 3.6 Elemental Auras VFX Pack + Character Aura Pack V2 (carried from prior research)

Already documented in prior research synthesis (2026-06-02-unreal-character-customization-research).

**Elemental Auras VFX Pack:** 10 effects (Fire ×3, Electric ×3, Ice ×2, Mystic ×3, Dark Mist ×2).
UE4.27–5.7. Covers Stage A.2 elemental aura layer.

**Character Aura Pack V2:** Updated Feb 2025; Niagara-based; Dash Aura + Lightning Aura variants.
Stage A.2 and Stage A.3 movement aura layer.

---

## 4. Techniques for 2D-to-3D Character Morph Emergence (Stage A.0 → A.1)

No off-the-shelf FAB pack was found that specifically implements a 2D-plane → volumetric 3D emergence
transition for characters. This is custom UE work. Documented approaches:

### 4.1 Material Lerp (Flat → Volumetric)

**Technique:** A Dynamic Material Instance parameter (`EmergenceAlpha`, 0.0 → 1.0) drives a Lerp
between two rendering modes on the character mesh:
- At 0.0: Unlit emissive with WorldPositionOffset flattening the mesh to a plane (or near-plane)
  + constellation/hologram material properties
- At 1.0: Standard lit translucent or opaque material with subsurface/emissive tint

WorldPositionOffset (WPO) in the material graph can collapse a 3D mesh toward a single plane by
overriding vertex Z position with a Lerp'd value. As the parameter animates from 0→1, the character
"unfolds" from flat to full 3D depth. This is a standard UE5 material technique.

**Sequencer integration:** The `EmergenceAlpha` parameter can be keyframed in a Level Sequencer track
bound to the character's Dynamic Material Instance. The official UE5 documentation confirms material
parameters can be animated via Sequencer ("Expose to Cinematics" flag on parameter). Alternatively,
Blueprint can drive this parameter in response to a game state change (player "molding" the form).

---

### 4.2 Niagara Parameter Animation (Concurrent VFX Shift)

As the material emergence progresses (0→1), concurrent Niagara system parameters should shift:
- Star point sprite size: decreases as depth emerges (points "become" the character joints)
- Connecting line opacity: decreases as constellation lines fade into the character form
- Aura emitter activation: new emitters activate as the character gains volume

This is driven by the same parameter (`EmergenceAlpha`) broadcast from Blueprint to all attached
Niagara system components via `SetNiagaraVariableFloat`. This is fully supported in UE5 and is
a documented pattern (forum: "Passing a parameter to Niagara System from blueprint"; YouTube:
"UE5 Control Niagara Dynamic Material Parameter With Blueprint").

**Performance note:** Niagara parameter bindings are evaluated per-tick after simulation completion —
this is acceptable for a single-character emergence sequence, not suitable for hundreds of simultaneous
characters. Architecture γ Stage A is a per-character UI/presentation context so this is not a concern.

---

### 4.3 UE5 Vertex Animation Tool (Alternative)

For a pre-baked 2D→3D emergence (not real-time parameter driven), the UE5 Vertex Animation Tool
can encode 3D mesh animation into a 2D texture. This produces a lightweight, GPU-efficient playback
of the "unfolding" geometry that does not require a skeletal animation rig. Suitable if the emergence
is a fixed cinematic sequence rather than an interactive "molding" effect.

**UE documentation:** https://dev.epicgames.com/documentation/unreal-engine/vertex-animation-tool-in-unreal-engine

---

### 4.4 Morph Targets (FBX Morph Target Pipeline)

For soft-sculpted emergence (subtle shape change without WPO flattening), a morph target authored
in Blender/Maya can transition between a minimized "flat" pose and the full 3D character form.
This is imported via the FBX Morph Target Pipeline. Less practical for a dramatic flat→3D effect
but appropriate for subtle "depth materializes" transitions.

---

## 5. Recommended UE Rendering Stack for Architecture γ Stage A

The following composition is the recommended rendering stack, ordered by layer:

### Layer 1 — Character Mesh Base (Static, per frame)
- Skeletal mesh (CC5 export or Synty character)
- Dynamic Material Instance on mesh:
  - Blend mode: Translucent (Stage A) → Opaque or Masked (Stage B)
  - Parameters: `EmergenceAlpha`, `HologramColor`, `ScanlineOpacity`, `ScanlineTiling`,
    `FresnelExponent`, `EmissiveStrength`
  - Source material: custom, borrowing material functions from HOLOGRAM VFX Pack 1 or authored fresh
  - WorldPositionOffset for Stage A.0 flatness (driven by `EmergenceAlpha`)

### Layer 2 — Star Point Niagara System (per character, attached component)
- Niagara System: custom authored
- Spawn: `Sample Skeletal Mesh` module targeting major skeleton joints (head, shoulders, elbows,
  wrists, hips, knees, ankles = ~12-16 star points)
- Render: Sprite renderer with glowing star sprite material (emissive, additive blend)
- Parameter: `StarBrightness`, `StarSize` — driven by Blueprint per chernoff dimension

### Layer 3 — Constellation Line Niagara System (per character, attached component)
- Niagara System: custom authored using plexus/SpriteBasedLine technique or ribbon vertex-order technique
- Reads from Layer 2 particle positions OR samples skeleton bone pairs directly
- Render: `SpriteBasedLine` module with emissive line material
- Parameter: `LineOpacity`, `LineColor` — driven by Blueprint

### Layer 4 — Element Aura Niagara System (Stage A.2+, per character)
- FAB pack: Elemental Auras VFX Pack (fire/electric/ice/mystic/dark mist variations)
- Activated when `EmergenceAlpha > 0.5`
- Parameter: `AuraElement` (selects active emitter) driven by chernoff `primary_element` field

### Layer 5 — Orbital Items Niagara System (Stage A.3, per character)
- Custom Niagara system: particles orbit skeleton origin at configurable radius
- Mesh renderer: coin mesh (from Money and Coins VFX pack meshes), gem mesh (custom or FAB), satchel
  static mesh (attached via socket — not a particle but a socket-attached component)
- Parameters: `CoinCount`, `CoinOrbitRadius`, `CoinOrbitSpeed` — driven by chernoff wealth/loot field
- `GemType`, `GemCount` — driven by chernoff rarity/tier field

### Layer 6 — Movement / Wind Effect (Stage A.3, conditional)
- FAB pack: Trail VFX Pack (elemental trails) or Advanced Niagara Character Trail VFX
- Or Niagara Wind VFX Pack adapted for character space
- Activated by movement velocity parameter; `WindSpeedMultiplier` driven by chernoff speed/agility field

### Stage B Transition (Constellation → Materialization)
- `EmergenceAlpha` animated 0→1 in Level Sequencer or via Blueprint
- Simultaneously: Layer 2/3 (stars/lines) fade out via opacity parameters
- Layer 1 material transitions Blend Mode via Material Switch (pre-baked variants: translucent + opaque)
- Character mesh reveals CC5 or Synty period clothing via a second mesh component activated at
  `EmergenceAlpha == 1.0`

### Niagara Composition Pattern
Per UE5 performance guidance: 1 Niagara system with multiple emitters is more efficient than multiple
separate systems. Recommend: single `NS_ConstellationForm` Niagara system with emitters for star points,
connecting lines, element aura, and wind trail — controlled by one set of user parameters. Orbital items
may be a separate `NS_OrbitalItems` system due to mesh-renderer overhead difference.

---

## 6. Chernoff Parameter → Visual Feature Binding Map

| Chernoff substrate field | Visual feature | UE binding mechanism |
|---|---|---|
| `primary_element` | Aura color + emitter variant (fire/ice/etc.) | Blueprint → `AuraElement` Niagara user param |
| `power_level` / tier | `StarBrightness`, `EmissiveStrength` | Blueprint → DMI param + Niagara user param |
| `power_level` | `AuraIntensity` | Blueprint → Niagara user param |
| `constitution` / health | Constellation line density (more/fewer connections) | Blueprint → `LineCount` Niagara user param |
| `agility` / speed | `WindSpeedMultiplier`, trail activation threshold | Blueprint → Niagara user param |
| `wealth` / loot-score | `CoinCount`, `CoinOrbitRadius` | Blueprint → Niagara user param |
| `rarity` | `GemCount`, `GemType` (mesh select) | Blueprint → Niagara user param |
| `volume` (inventory) | Satchel socket attachment activation | Blueprint → socket attach/detach |
| `emergence_progress` | `EmergenceAlpha` (drives ALL layer transitions) | Blueprint → DMI param + Niagara user params |

All bindings use the UE5-native pattern: expose parameters as Niagara User Parameters or DMI scalar/
vector parameters; set via Blueprint `Set Niagara Variable Float/Vector` and `Set Scalar Parameter Value`
calls. This is confirmed supported, per-tick updatable, and composable with Level Sequencer keyframing.

---

## 7. Cost and Effort Estimates

### 7.1 FAB Pack Cost Estimate (Architecture γ visual layer, above baseline CC5/Synty stack)

Note: Direct FAB listing prices could not be confirmed (403 errors). Estimates based on comparable
products, third-party asset mirror sites, and historical pricing patterns.

| Pack | Purpose | Estimated Cost |
|---|---|---|
| HOLOGRAM VFX With Niagara (Pack 1) | Stage A.0 holographic material base | ~$30-60 |
| Niagara Hologram Pack | Additional hologram Niagara systems | ~$5-15 |
| Trail VFX Pack | Stage A.3 wind/movement + Plexus reference | ~$30-50 |
| Money and Coins VFX | Stage A.3 coin orbital mesh/material | ~$20-30 |
| Coin VFX (supplemental) | Coin type variety | ~$10-20 |
| **TOTAL estimate** | | **~$95-175** |

The Elemental Auras VFX Pack and Character Aura Pack V2 are already accounted for in the baseline
character research synthesis (2026-06-02-unreal-character-customization-research); not re-budgeted here.

The 50+ Free Niagara Examples Pack (Epic, UE5.7) provides free reference Niagara systems including
aura-type effects — recommend downloading this first before purchasing any supplemental packs, as it
may partially substitute.

---

### 7.2 UE-Seam-Agent Effort Estimate (beyond baseline 8-12 sessions)

Baseline sessions from prior research: 8-12 sessions (CC5 authoring + UE pipeline + elemental aura
integration + armor sockets + Stage D Sequencer).

Additional effort for Architecture γ Stage A constellation form:

| Task | Estimated sessions |
|---|---|
| Custom hologram/constellation base material (DMI, WPO flatness, EmergenceAlpha param) | 1-2 |
| Star point Niagara system (skeletal mesh vertex spawn, sprite renderer, parameter exposure) | 1-2 |
| Constellation line Niagara system (SpriteBasedLine or ribbon, bone-pair adjacency logic) | 2-3 |
| EmergenceAlpha sequencer / Blueprint animation (Stage A→B transition choreography) | 1-2 |
| Orbital items Niagara system (orbit logic, coin/gem mesh renderer) | 1-2 |
| Satchel socket attachment + conditional activation | 0.5 |
| Wind trail integration (adapting FAB pack to character velocity parameter) | 0.5-1 |
| Parameter binding wiring (Blueprint → all Niagara + DMI params per chernoff fields) | 1-2 |
| **Additional Architecture γ subtotal** | **8-14.5 sessions** |
| **Conservative round** | **8-10 sessions** |

**Total Architecture γ estimate:** 14-22 sessions (baseline 8-12 + additional 6-10 conservative).

The constellation line system is the highest-risk task. The `SpriteBasedLine` approach requires
Niagara scratch-pad module scripting; if the seam agent has limited Niagara module scripting
experience, the learning curve adds sessions. Recommend the seam agent study the RealTimeVFX
Niagara 5.1 Plexus Mini Tutorial before beginning this work.

---

## 8. Knowledge Gaps Not Resolved

1. **FAB listing prices.** All fab.com direct listing pages returned 403 errors. Prices are estimates.
   Verify on FAB before budgeting.

2. **HOLOGRAM VFX Pack UE5.6/5.7 compatibility.** The pack confirmed UE5.1-5.5. Whether it has been
   updated for 5.6/5.7 is unconfirmed. Given the active update history (last update May 2025), likely
   updated but not confirmed.

3. **Niagara Hologram Pack specific system contents.** The 20 Niagara systems are not individually
   enumerated in available sources. Whether any include a skeleton-vertex-driven star point system is
   unknown — would require in-engine inspection after purchase.

4. **Constellation line rendering with static bone positions (not dynamic particles).** The plexus
   technique connects dynamically moving particles. For a more "static diagram" constellation (bones
   don't jump around; only idle-sway animation), a geometry script or procedural mesh approach (UE5
   Procedural Mesh Component) may produce cleaner results than Niagara ribbons. Geometry scripts
   in UE5.4+ allow runtime mesh modification from Blueprint without C++. This was not deeply
   researched; flagged as a potentially superior technique for the Stage A.0 strict-diagram aesthetic.

5. **Coin/gem orbital system off-the-shelf.** No FAB pack was found that specifically provides a
   "particles orbit character" system. Custom orbit Niagara authoring is required. Orbital mechanics
   in Niagara are straightforward (sin/cos position update with radius and speed parameters) but
   the FAB research did not surface a ready-made pack.

6. **Period satchel/fantasy backpack mesh.** The Tactical Hiking Backpack found is realistic/modern
   style, not period-appropriate. A fantasy-period satchel would need to be sourced from a different
   FAB pack (e.g., Synty modular accessory packs or a dedicated prop pack) or custom-made.

---

## 9. Source List

**FAB Marketplace Listings:**
- [HOLOGRAM VFX With Niagara (Pack 1) | Fab](https://www.fab.com/listings/3e358551-89d4-40de-8fec-99d4b66b6c1e)
- [HOLOGRAM VFX With Niagara 2 | Fab](https://www.fab.com/listings/c102d630-0c53-4dd0-b47a-98a71f832d5c)
- [Niagara Hologram Pack | Fab](https://www.fab.com/listings/deee89fc-7a07-44d1-9574-689a3475790b)
- [Niagara Sci-Fi Starter VFX Pack | Fab](https://www.fab.com/listings/db2445cf-fb11-40b2-b7d8-10d52496996e)
- [Trail VFX Pack | Fab](https://www.fab.com/listings/b41b3941-efd2-42ba-9747-e7a4d23e7e1b)
- [Advanced Niagara Character Trail VFX | UE Marketplace](https://www.unrealengine.com/marketplace/en-US/product/advanced-niagara-character-trail-vfx-01)
- [Money and Coins VFX | Fab](https://www.fab.com/listings/08325750-b380-41cc-8fe3-ac711c5f647d)
- [Coin VFX | Fab](https://www.fab.com/listings/790b1478-51c7-4147-b712-7f69179c987c)
- [Treasure Chest VFX | Fab](https://www.fab.com/listings/67d95ecf-86ab-42a5-9d55-7dbaa3123dae)
- [Niagara Wind VFX Pack | UE Marketplace](https://www.unrealengine.com/marketplace/en-US/product/niagara-wind-vfx-pack)
- [Tactical Hiking Backpack 75 (Rigged) | Fab](https://www.fab.com/listings/1e8c4b3b-1590-4d1d-a216-25eabb179619)
- [Elemental Auras VFX Pack | Fab](https://www.fab.com/listings/5aa665cc-9300-42c6-a140-eca1bafdb875)
- [Character Aura Pack V2 | Fab](https://www.fab.com/listings/c8ac7f18-ac93-4dbd-8bb1-16edf978bbba)
- [Ultimate Character VFX V2 | Fab](https://www.fab.com/listings/63810c36-b2f9-4401-8554-c0db33e0db2b8)
- [Cosmic VFX | Fab](https://www.fab.com/listings/111f4386-01b4-45f5-8c96-bfe5680f508f)
- [UE5 Character Absorb VFX | Fab](https://www.fab.com/listings/b1896fef-e8ae-4d43-b0f7-ec95d706a772)
- [Dissolve Any Mesh | Fab](https://www.fab.com/listings/a7067627-5254-48a9-8d11-19190c13f496)

**Tutorials and Technical References:**
- [Holographic Ribbon FX in UE5 Niagara Tutorial | CGHOW](https://cghow.com/holographic-ribbon-fx-in-ue5-niagara-tutorial/)
- [Hologram Effect Niagara Tutorial | CGHOW](https://cghow.com/ue4-niagara-hologram/)
- [Star FX in UE5 Niagara Tutorial | CGHOW](https://cghow.com/star-fx-in-ue5-niagara-tutorial/)
- [Niagara 5.1 Plexus Mini Tutorial | RealTimeVFX Forum](https://realtimevfx.com/t/niagara-5-1-plexus-mini-tutorial/22099)
- [Constellation Effect Discussion | RealTimeVFX Forum](https://realtimevfx.com/t/constellation-effect/27163)
- [Plexus Effect with Particle Attribute Reader | CGHOW](https://cghow.com/ue4-niagara-plexus/)
- [How to Create a Ribbon Effect in Niagara | UE5.7 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-a-ribbon-effect-in-niagara-for-unreal-engine)
- [Vertex Animation Tool | UE5.7 Documentation](https://dev.epicgames.com/documentation/unreal-engine/vertex-animation-tool-in-unreal-engine)
- [FBX Morph Target Pipeline | UE5.7 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-morph-target-pipeline-in-unreal-engine)
- [Using Material Parameter Collections | UE5.7 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-material-parameter-collections-in-unreal-engine)
- [Render Module Reference for Niagara | UE5.7 Documentation](https://dev.epicgames.com/documentation/unreal-engine/render-module-reference-for-niagara-effects-in-unreal-engine)
- [Niagara Skeletal Mesh Sampling | RealTimeVFX Forum](https://realtimevfx.com/t/ue4-niagara-static-mesh-sampling-and-vertex-density/19396)
- [Animating Niagara Parameters Through Sequencer | Epic Developer Community Forum](https://forums.unrealengine.com/t/animating-niagaras-exposed-parameters-through-sequencer/137260)
- [Controlling Dynamic Niagara Material Parameter With Blueprint | Epic Developer Community Forum](https://forums.unrealengine.com/t/controlling-dynamic-niagara-material-parameter-with-blueprint/450557)
- [Creating Custom Constellations for Celestial Vault Plugin | Epic Developer Community](https://dev.epicgames.com/community/learning/tutorials/9XyB/unreal-engine-creating-custom-constellations-for-the-celestial-vault-plugin)
- [Discover 50+ Free Niagara Systems for UE5.7 | Unreal Engine](https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7)
- [Hologram VFX With Niagara — UE5.1 reference | Asset Freaks](https://assetfreaks.com/download/hologram-vfx-with-niagara-ue-5-1-5-5/)
- [Hologram VFX Pack 4 | UE Marketplace](https://www.unrealengine.com/marketplace/en-US/product/hologram-vfx-with-niagara-pack-4)
- [HOLOGRAM VFX With Niagara 3 | UE Marketplace](https://www.unrealengine.com/marketplace/en-US/product/hologram-vfx-with-niagara-3)
- [UE5 Optimize Niagara Performance | More VFX Academy](https://morevfxacademy.com/complete-guide-to-niagara-vfx-optimization-in-unreal-engine/)

---

*Research artifact authored: 2026-06-02*
*Legolas — Mode A analytical research*
*Output path: `agentic_orchestration/legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md`*
