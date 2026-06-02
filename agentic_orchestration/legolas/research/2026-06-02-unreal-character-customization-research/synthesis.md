# Research — Unreal Character Customization Architecture — 2026-06-02

**Mode:** A (analytical)
**Commissioner:** gandalf (per Matt 2026-06-02 ratification)
**Commissioned for:** Manifestation Milestone Phase 1 (MM-P1) design session preparation
**Sources consulted:** See § 9 Source List

---

## Summary

Unreal Engine has two native paths for 1000+ character customization at scale: MetaHuman Crowds (photorealistic, scalable to tens of thousands via LOD instancing, experimental in UE5.6+) and the Mutable plugin (Beta in UE5.5+, generates dynamic skeletal meshes at runtime with mesh-merge and draw-call optimization). MetaHuman is unsuitable for fantasy/stylized aesthetics without significant external sculpting overhead. Reallusion Character Creator 5 ($299 perpetual) is the strongest external pipeline candidate — it exports CC5-rigged characters with a skeleton structurally compatible with MetaHuman, supports stylized/fantasy morphing via ActorMIXER, and integrates with UE5.7 via a free Auto Setup plugin. Synty Studios' Sidekick system (free starter + ~$200/pack) offers a lower-fidelity but highly modular low-poly fantasy kit that is Unreal Mannequin-compatible and ships with a character creator tool. Arbitrary 3D gear integration is well-supported in Unreal via Skeletal Mesh Socket attachment across all candidate approaches. Recommended primary stack: CC5 (character foundation) + Mutable (runtime customization layer) + FAB VFX aura packs (elemental spirit signatures).

---

## 1. Survey of Candidate Products

### 1.1 MetaHuman + MetaHuman Crowds (Epic Games)

**What it is.** MetaHuman is Epic's free in-engine system for creating photorealistic digital humans. As of UE5.6, MetaHuman Creator is embedded inside Unreal Engine rather than running as an external web tool. The MetaHuman Crowds plugin (experimental, shipping in UE5.6+, formalized in UE5.8 preview) handles large-scale rendering via a hybrid LOD/instancing architecture.

**Scale.** The Crowds plugin "scales from tens to thousands of characters." The 2020 Matrix Awakens demo placed 35,000 MetaHumans in a city scene using vertex-animated static meshes. At full LOD (close camera distance), simultaneous high-fidelity MetaHumans are realistically limited to a handful (2-5) on consumer hardware before frame rate impact; the LOD system automatically degrades distant characters to instanced skeletal meshes, making true crowd scale feasible. No published benchmark for exact 1000-character simultaneous full-LOD rendering exists in available documentation — crowd scale operates precisely because NOT all characters are full-LOD at once.

**Customization range.** Morph targets for facial features, skin color adjustment, body type variation — all supported. However, morphs are constrained to human proportions: no exaggerated features, no snouts/horns/beaks, no non-human skeletons. Hair via Groom assets or hair cards.

**Art style.** Hard constraint: MetaHuman is photorealistic by design. Stylized character creation requires exporting the mesh to Blender/ZBrush, performing custom sculpting to alter proportions, and re-importing via Mesh-to-MetaHuman. This workflow is documented but explicitly "rounds off sharp stylization" and "makes faces less distinctive." Not suitable for fantasy/isekai/spirit-form aesthetics without significant per-character art labor.

**Gear integration.** MetaHuman uses the standard UE Mannequin-compatible skeleton with defined sockets. Arbitrary 3D gear (weapons, armor) can be attached via socket attachment nodes in Blueprint. The FAB "Fantasy Modular Armor Sets" product is explicitly designed for MetaHumans (documented as "prepared for tall normal weight metahumans for both male and female").

**Rigging.** Human bone structure, shared skeleton convention with UE5 Mannequin. CC5 characters now share the same facial control structure and skeleton as MetaHuman (as of CC5 2025 release), making animation interchange bidirectional.

**Cost.** FREE. MetaHuman Creator, MetaHuman Crowds plugin, LODSync component, all zero-cost as part of Unreal Engine.

**License.** Unreal Engine EULA; royalty-free for commercial products under $1M gross revenue threshold (standard Epic royalty schedule above).

**Performance.** Crowds system uses Mass for simulation; Nanite or dynamic LOD for rendering. LOD architecture prunes joints per level rather than rebuilding hierarchy. "You are never paying for more detail than you need at any given moment."

**Workflow.** UE5.6+ fully in-engine authoring. Auto Setup from Reallusion bridges CC characters to MetaHuman-compatible skeletons.

**Spirit/ethereal VFX compatibility.** MetaHuman characters accept Niagara VFX aura effects attached via component or Blueprint. Translucent/ethereal rendering requires custom material and Niagara setup (not built-in) but is feasible.

---

### 1.2 Mutable Plugin (Epic Games — built-in UE5.5+)

**What it is.** Mutable is an Unreal Engine plugin (Beta in UE5.5, UE5.6, UE5.7) that generates dynamic skeletal meshes, materials, and textures at runtime or in-editor. Acquired by Epic from Anticto; included as a free built-in plugin.

**Scale.** No documented hard limit on number of characters. The system generates characters in the background using CPU resources and working memory, then behaves as a standard pre-generated skeletal mesh once done. Mesh merging reduces draw calls: 50 modular-component characters = 50 draw calls (vs 150 without merge). Suitable for large-scale NPC populations.

**Customization range.** Mesh toggling (clothing, accessories, armor layers), texture swap/bake, morph target baking, UV layout management, hidden geometry removal (z-fighting prevention), cloth simulation data merging, physics asset merging. Color via material parameters. Supports data-driven UI via data tables.

**Modularity.** High: any skeletal mesh can be a Mutable source object. External gear packs can be imported as Mutable components if authored against a shared skeleton. The CustomizableObject / CustomizableObjectInstance pattern is extensible.

**Art style.** Agnostic — Mutable operates on whatever meshes you feed it. Works equally with photorealistic, stylized, low-poly, or hand-drawn-style assets.

**Gear integration.** Yes, explicitly supports "weapons, vehicles, and other props" beyond characters. External 3D items integrate as additional mesh components in the CustomizableObject graph.

**Rigging.** Works with any skeleton; merges animation data from multiple parts. Merged mesh uses the skeleton of the main mesh component.

**Cost.** FREE — included with Unreal Engine 5.5+.

**License.** Unreal Engine EULA (same as engine).

**Performance.** Background generation with LOD management at runtime; texture streaming with on-demand generation. Beta status means production shipping is flagged with caution advisories in official docs. Use-caution advisory for shipped products (Beta).

**Workflow.** Editor plugin; Blueprint API; Customizable Object graph editor. UE5.7 docs available. Free Mutable Sample Project on FAB (released Feb 2025) demonstrates character + weapon customization.

**Spirit/ethereal VFX.** Mutable handles mesh and texture; VFX aura layers are additive Niagara components separate from Mutable, composable.

---

### 1.3 Reallusion Character Creator 5 (CC5)

**What it is.** CC5 is standalone character creation software (Windows), launched August 27, 2025. Exports rigged characters to Unreal Engine 5 via free Auto Setup plugin (All-in-One, supporting UE5.7+). CC5 is the successor to CC4; the skeleton adds 10 bones aligned to UE5 key structures and shares facial control structure with MetaHuman.

**Scale.** CC5 itself is an authoring tool, not a runtime system. For 1000+ characters: ActorMIXER (Pro plugin) enables randomized character generation at scale from a pool of source characters. You author a source pool once; ActorMIXER generates variant outputs non-destructively. Runtime deployment in Unreal uses CC5 exports as standard skeletal meshes, scaled via UE's own crowd/instancing systems (MetaHuman Crowds, Mutable, or standard instancing).

**Customization range.** Broad: gender, hair (layered system), facial features (extensive morph sliders), skin color, body type (HD morphs adding anatomical detail without altering bone), tattoos (via texture layering), stylized or realistic. New HD character base supports up to 16x more mesh detail than CC4. ActorMIXER blends up to 6 source characters' heads, bodies, or individual features. Stylized content packs available in Reallusion Content Store (anime, fantasy creatures morph pack, stylized character morphs starter pack).

**Art style.** Capable of both photorealistic and stylized. Superior to MetaHuman for stylized/fantasy work per community consensus (documented in Reallusion forum CC5 vs MetaHumans thread, Feb 2026). Fantasy Creatures CC Morph Pack (12 morph sliders, 12 CC Projects) available separately. Stylized Character Morphs pack available. Not primarily anime/chibi — tends toward semi-realistic proportions; heavy stylization requires morph pack additions.

**Gear integration.** CC5 characters export with a CC skeleton. Clothing and gear in CC5 are "CC Components" (ccCloth, ccShoes, ccGloves formats). External 3D gear (arbitrary weapons/armor) can be imported into CC5 as Props or attached via socket in Unreal after export. The Auto Setup plugin handles shader assignment and character setup in UE. Arbitrary gear not authored in CC5 attaches in UE via socket attachment on exported CC5 skeleton bones — same mechanism as any UE skeletal mesh.

**Rigging.** CC5 skeleton + MetaHuman-compatible facial structure. Auto Setup for UE5.7 automates shader assignment, control rig setup, and Live Link configuration. UE5 export preset available in CC5 export dialog.

**Cost.** Software: $299 perpetual (CC5 standalone) or $499 Deluxe Bundle (includes ActorMIXER Pro + Core Library of 44 HD scanned heads + HD Ultimate Morphs). Subscription option available from $29/month (2026 Reallusion pricing). Content Store add-ons sold separately (typical pack prices $20-$150; Extended License for mass character output in commercial games adds ~50% to per-item price vs Standard License). Auto Setup plugin: free.

**License.** Software EULA: royalty-free, unlimited projects with perpetual purchase. Content Store items: Standard License = one character output per commercial game title; Extended License = unlimited character mass output for commercial games. For 1000+ character scenario, Extended Licenses required per content item used. This adds material cost per content pack above base software price.

**Workflow.** CC5 → Export with UE5 preset → Import to Unreal → Auto Setup plugin automates shaders + rig → deploy as standard skeletal mesh. For motion: iClone Live Link streams animation to UE in real time.

**Spirit/ethereal VFX.** CC5 handles mesh/texture/rig only. Ethereal/translucent spirit-form rendering requires custom Unreal material (translucent, subsurface, or unlit with emissive) applied to CC5-exported mesh in UE. Niagara VFX aura components attach via Blueprint separately.

---

### 1.4 Synty Studios — POLYGON Modular Fantasy Hero Characters + Sidekick System

**What it is.** Two distinct Synty product lines:

(a) **POLYGON Modular Fantasy Hero Characters** — low-poly modular asset pack, 720 modular parts + 120 premade characters. Available on Synty Store and FAB.

(b) **Sidekick Modular Characters** — higher-fidelity modular system with a dedicated Character Creator Tool plugin (Unity + UE5.3+). Free Starter Pack available on FAB; additional packs sold separately. Fantasy Knights pack: 119 Fantasy Knight parts + 90+ human base parts, $199.99. Tool ships with every Sidekick pack.

**Scale.** POLYGON is a static mesh/skeletal mesh kit — scale is only limited by standard UE instancing. Sidekick Character Creator Tool supports baking completed characters into single optimized prefabs (combining skinned mesh renderers) for performance-friendly deployment.

**Customization range.** POLYGON: 720 modular parts combinable via shader color customization. Sidekick: head/face/hair/torso/limbs/attachment points (shoulder, elbow, knee, hip, back); facial blend shapes for expressions; body blend shapes for proportions; dynamic joints for cloth/hair/cape physics.

**Art style.** POLYGON: low-poly, stylized, fantasy-heroic. Clear isekai-genre visual compatibility. Sidekick: slightly higher fidelity than POLYGON but still clearly stylized/low-to-medium-poly. Both are stylistically distinct from photorealistic — strong genre compatibility with spirit-form / fantasy aesthetic.

**Gear integration.** POLYGON: weapons included in 720 parts (axes, daggers, maces, shields, staffs, swords); attached to skeleton joints as parent. Sidekick: attachment slot system supports head, face, back, shoulder, elbow, knee, hip gear items; cross-pack mixing supported ("combine Sidekick themes to create endless characters"). External third-party gear: not explicitly documented; would require manual socket definition on shared UE5 Mannequin skeleton.

**Rigging.** POLYGON: skeleton compatible with Mecanim (Unity) and UE4.22+ Mannequin. Sidekick: fully rigged to UE5 Mannequin skeleton (UE5.3-5.7 listed). NOTE: Synty Fantasy Knights pack documentation shows Unity-only support — the Sidekick packs on the Synty Store appear Unity-primary, with Unreal support via the FAB listing for the free starter pack. Confirm per-pack UE5 support before purchasing non-starter Sidekick packs.

**Cost.** POLYGON Modular Fantasy Hero Characters: $149.99 one-time. Sidekick free starter: free. Individual Sidekick packs: ~$199.99/pack. Synty all-access subscription: $30/month (unlocks 130+ packs). FAB standard license included with purchase; commercial use permitted.

**License.** Synty Store license: 5 seats per copy; royalty-free commercial use for games. No per-character mass output restriction documented (unlike Reallusion CC content).

**Workflow.** Asset import to UE project; Sidekick Character Creator Tool runs as editor extension; character baked to single mesh for deployment. No external authoring software required for Sidekick workflow within UE.

**Spirit/ethereal VFX.** No built-in spirit/VFX support. Niagara aura effects attach via Blueprint to completed characters same as any UE skeletal mesh.

---

### 1.5 Daz3D + Daz to Unreal Bridge

**What it is.** Daz Studio (free) with Genesis 9/8 figure system, exported to Unreal via free Daz to Unreal Bridge plugin (GitHub: daz3d/DazToUnreal).

**Scale.** Not designed for crowd-scale. Daz characters are monolithic (high-poly hero characters). Runtime generation of 1000+ Daz characters is not the intended use case. Performance at scale would require aggressive LOD reduction and instancing — feasible but not a documented use case.

**Customization range.** Broad: Genesis 9 supports gender, body shape, skin tone, facial morphs, hair, clothing layers. Large content ecosystem. However: licensed content requires per-item Interactive License for commercial game use.

**Art style.** Primarily photorealistic/semi-realistic. Fantasy content available but tends toward "dark fantasy" or "realistic-heroic" rather than stylized/anime/isekai. Limited stylized/anime range compared to CC5.

**Gear integration.** Modular approach: export body, then outfits/hair separately and combine in Unreal. Bridge supports multi-piece export. External 3D gear attaches via UE socket system.

**Rigging.** Genesis 9 skeleton; UE4/UE5 retargeting possible but may require retargeting pass. Not natively UE5 Mannequin-aligned.

**Cost.** Daz Studio: free. Bridge plugin: free. Content: per-item purchase ($10-$60/character; $5-$30/outfit). Interactive License: $50 per content item for commercial game deployment. For 1000+ characters using varied purchased content, Interactive License cost at scale is prohibitive ($50/item × number of unique content items used).

**License.** Daz Interactive License required per content item for commercial games. Per-item cost model does not scale economically to 1000+ character scenarios using diverse purchased content.

**Assessment.** Not recommended for the MM-P1 scenario due to cost structure at scale, photorealistic aesthetic bias, and limited stylized/fantasy range.

---

### 1.6 Mixamo (Adobe — Free)

**What it is.** Free Adobe service for auto-rigging and animation. Library of ~300 pre-rigged character models and 2000+ animations. Exports FBX for Unreal import.

**Scale.** Characters are individual FBX exports; no crowd or mass-generation system. Feasible for a small set of hero characters but not for 1000+ unique character generation.

**Customization range.** Minimal character customization — characters are pre-made, not morphable at import. Auto-rigger applies to custom meshes but does not add morph sliders or customization UI.

**Art style.** Mixed — includes stylized and semi-realistic characters. Some fantasy/game-style characters available. Limited selection compared to dedicated character creation tools.

**Gear integration.** Mixamo Mannequin skeleton is compatible with UE5 Mannequin via retargeting. Gear attaches via socket system.

**Rigging.** Mixamo skeleton; retargeting to UE5 Mannequin is well-documented.

**Cost.** Free, royalty-free for commercial use. Characters and animations can be used in commercial games embedded in a project (not sold standalone).

**License.** Commercial use permitted; cannot redistribute as standalone assets.

**Assessment.** Useful as supplementary source for animations and a small number of pre-made character starting points. Not viable as primary system for 1000+ character generation.

---

### 1.7 FAB Marketplace — Character System Plugins

Several FAB products offer Blueprint-native runtime character customization systems:

**Modular Character Customization** (FAB listing de3a5153): Modular part editor with material, transform, and lighting parameters per part; each part saved as independent asset mountable via single function call. UE Blueprint native.

**Modular Character System (Multiplayer / Replicated)** (FAB listing 9deb1166): Runtime player customization (hats, outfits, hair color); fully replicated for multiplayer (Dedicated + Listen + Standalone); UE5.5-5.7.

**ModuFusion: Character Customization Unleashed** (FAB listing 33b5c144): Dynamic head/body/limb/accessory interchange; 6 Blueprints + 8 C++ classes; network optimized; UE5.5-5.7. No character art included — framework only.

**Xandra Character Creator** (FAB listing e73afadb): In-game character creation with age, weight, body/face shape, colors, makeup, piercings, horns; UE5 Mannequin skeleton default (Beta v3.3); runtime NPC population. Standard Edition ($unknown; ~$30-60 based on comparable products); Deluxe Edition (~$100-150) includes 50+ modular assets. Includes C++ code.

**Character Customizer** (FAB listing d2992e16): Character customization with crowd spawning/optimization system; 44 tintable clothes meshes; easy random NPC generation; slot-based save/load at runtime.

**Note on FAB plugin pricing:** Direct FAB listing pages returned 403 errors during research. Prices cited above are estimates from third-party sources; verify on FAB before purchasing.

**Assessment of FAB plugins.** These are framework systems — they manage runtime customization logic but supply little or no character art. They pair well with a content pipeline (CC5 or Synty assets) but are not standalone solutions for the full MM-P1 scenario.

---

### 1.8 FAB Marketplace — Modular Gear Packs

**Fantasy Modular Armor Sets** (FAB; prepared for MetaHuman male/female): 21 armor sets × 6 parts each = 126 separate pieces; heavy/medium/light weight class categories; color-tinting system; 6-part breakdown (head, shoulder, chest, arms, legs, feet). Each piece and set mixable.

**POLYGON Modular Fantasy Hero Characters** weapon set: Axes, daggers, maces, shields, staffs, swords — parented to skeleton joints.

**Modular Characters, Gear and Inventory Items** (FAB listing ef645080): Combined modular character + gear system.

**Key principle for arbitrary gear integration.** Unreal Engine's Skeletal Mesh Socket system supports attaching arbitrary static meshes or skeletal meshes to any named socket on any skeleton. Standard workflow: define sockets on the character's skeleton bones (e.g., "weapon_r" on the right hand bone, "back_socket" on spine); any gear item (static mesh) can then be attached via Blueprint's `AttachToComponent` call with the socket name. This is engine-native, works with MetaHuman/CC5/Synty/any skeleton, and requires no special integration with the character system beyond socket naming convention consistency.

---

### 1.9 FAB VFX Packs — Spirit / Elemental / Aura

**Elemental Auras VFX Pack** (FAB listing 5aa665cc): 10 unique elemental character aura effects (3x Fire, 3x Electric, 2x Ice, 3x Mystic, 2x Dark Mist). Material instances with Color, Emissive Lighting, Opacity, and flow parameters. UE4.27-5.7.

**Character Aura Pack V2** (FAB listing c8ac7f18, Feb 2025 update): Niagara-based aura effects including Dash Aura variants and Lightning Aura effects. Character-specific; parameterized.

**Magic Aura Bundle Niagara** (FAB listing 84b6a0ff): Niagara aura bundle.

**Ultimate Character VFX V2** (FAB listing 63810c36): Advanced overlays + Niagara effects.

**50+ Free Niagara Systems** (Epic Games, UE5.7): Epic released 50+ free Niagara effect templates in UE5.7 including aura-style effects.

**Assessment.** Spirit-form / elemental VFX is well-served by FAB Niagara packs. The Elemental Auras VFX Pack covers fire, electric, ice, mystic, and dark mist — partial overlap with canonical-7+1 elements. Custom per-element signatures would require either purchasing multiple packs or authoring custom Niagara systems (feasible but represents UE-seam-agent effort). Translucent/ethereal character rendering (Stage A celestial spirit form) requires custom material on the character mesh — not a VFX pack concern but a shader concern.

---

## 2. Per-Question Analysis

### Question A: Is there a product that delivers character customization ON Unreal, ideally with modular character pack(s) included or available?

**Finding:** No single product delivers both a complete customization framework AND a full fantasy character pack at the required scale. The closest candidates:

1. **Mutable (free, built-in)** — customization framework without art content.
2. **Synty Sidekick system** — ships with both a character creator tool AND modular fantasy art, but Unreal version support needs per-pack verification; art quality is stylized-low-poly.
3. **MetaHuman + MetaHuman Crowds** — framework + photorealistic art, but art style incompatible with fantasy/isekai aesthetic.
4. **Xandra Character Creator (Deluxe Edition)** — ships with 50+ modular assets + creation system + C++ code; Unreal-native; but asset library is modest and aesthetics may not match.

**A is insufficient on its own for fantasy aesthetics at the quality level the four-stage MM-P1 flow requires.** A framework + separate art pipeline is the correct architecture.

---

### Question B: What modular character pack best composes with the customization framework?

**Primary recommendation: Reallusion Character Creator 5 as the art-generation pipeline.**

CC5 is not a pack but a tool that generates export-ready UE5 skeletal meshes. This is architecturally superior to a static pack for the MM-P1 scenario because:
- ActorMIXER generates unique character variants non-destructively from a source pool
- The CC5 Deluxe Bundle's 44 scanned heads + HD morphs provides immediate human diversity
- Fantasy/stylized content packs extend the range (Fantasy Creatures Morph Pack, Stylized Character Morphs)
- MetaHuman-compatible skeleton means animation assets from the broad UE ecosystem apply
- Extended License structure means content items used for mass character output require per-item Extended License (adds cost; see § 5)

**Secondary recommendation (lower fidelity, simpler workflow): Synty Studios Sidekick**

If a lower-poly stylized aesthetic is acceptable (and for an isekai/spirit-form aesthetic it may well be), the Sidekick system plus Fantasy Knights pack delivers an immediately usable UE5-native solution at $199.99 for the fantasy knights pack + free starter. Key caveat: the Synty Store product page for Fantasy Knights listed Unity-only UE compatibility — verify UE5 support on the specific FAB listing for Sidekick Fantasy Knights before purchase.

**POLYGON Modular Fantasy Hero Characters ($149.99)** is a strong third option for a pure low-poly JRPG-adjacent visual aesthetic — 720 parts, 120 premade characters, weapons included.

---

### Question C: Would arbitrary 3D-created items (weapons, armor, other gear) integrate with the chosen system?

**Yes, universally.** Unreal Engine's Skeletal Mesh Socket system supports arbitrary gear attachment regardless of character system:

- Define named sockets on skeleton bones in Persona (the UE mesh editor)
- Any static mesh or skeletal mesh can be attached to any socket via Blueprint's `AttachToComponent` node
- No system-specific integration required beyond matching socket name conventions
- The Fantasy Modular Armor Sets (FAB) is explicitly authored for MetaHuman/UE skeleton sockets
- CC5 exports use a UE5-standard skeleton with well-defined bone names
- Synty Sidekick uses UE5 Mannequin skeleton, which has standard socket name conventions

**Integration constraint:** Gear from different art styles (e.g., realistic armor from FAB + Synty low-poly character base) will have visual style mismatches. Within a consistent art style, arbitrary gear integration is trivially supported.

---

## 3. MM-P1 Four-Stage Flow Analysis

### Stage A — Celestial Spirit Gallery (VFX Surface 1)

**Requirement:** Spirit-form / ethereal / translucent character visualization; per-element aura signatures; gallery/deck browse pattern.

**Asset needs:**
- Character meshes: Could use CC5-generated characters or Synty characters as the base forms
- Translucent/ethereal rendering: Custom Unreal material (translucent blend mode, emissive, potentially subsurface scattering) applied to character mesh — not a separate product; UE-seam-agent authors this material
- Aura VFX: Elemental Auras VFX Pack (fire, ice, electric, mystic, dark mist) covers ~5/8 canonical primaries; custom Niagara for remaining elements
- Gallery/deck UI: Web-side (drax) or UE Widget — not a character customization asset concern

**Assessment:** Feasible. Spirit-form rendering requires custom UE material work (not a purchased asset). Elemental aura VFX is well-covered by existing FAB products. The ~3 canonical elements not covered by the Elemental Auras pack require either additional VFX packs or custom Niagara authoring.

### Stage B — Materialization (period-appropriate clothing)

**Requirement:** Selected character appears in tattered period clothing; cloth physics; period-appropriate materials.

**Asset needs:**
- Period clothing assets: CC5 content store has period-appropriate clothing content (medieval, etc.) at additional cost; alternatively, FAB period clothing assets
- Cloth physics: UE native (Chaos Cloth) applies to any skeletal mesh with cloth data
- The single-character pipeline constraint (only one character maps fully from engine JSON per Matt's reduction) means only one full set of period garments needs to be sourced for MM-P1 mock

**Assessment:** Manageable for mock scope. One character's Stage B materialization requires one period outfit asset.

### Stage C — Customization

**Requirement:** Gender / hair / facial features / skin color / faction tattoos — modular, player-adjustable.

**Asset needs:**
- Character customization framework: Mutable plugin (free, UE-native) handles runtime parameter adjustment for CC5-exported meshes; or CC5's own morph sliders baked and exposed via Blueprint
- For MM-P1 mock scope: may not require full runtime Mutable integration — video performance mock could use pre-rendered or pre-baked variant selection
- Tattoos: Texture layer swap via Mutable or material decal in UE

**Assessment:** For production: Mutable + CC5 pipeline is the right architecture. For MM-P1 mock specifically: discrete variant selection (showing a few distinct customization choices) is sufficient without full runtime Mutable integration.

### Stage D — L50 Decked-Out Reveal (VFX Surface 2)

**Requirement:** Tier 2 Set + Legendary gear; skill auras + gear auras + faction tattoo glow; "boom" entrance.

**Asset needs:**
- Gear assets: Fantasy Modular Armor Sets (FAB, 21 sets × 6 parts) for armor; separate weapon pack
- Aura VFX: Character Aura Pack V2 or Ultimate Character VFX V2 for skill auras; Magic Aura Bundle for gear aura layer
- Faction tattoo glow: Emissive texture layer on character mesh (custom UE material)
- "Boom" entrance: UE Sequencer + Niagara burst effect (custom or from existing packs)

**Assessment:** The VFX packs cover the surface. Gear assets are well-supplied by FAB. The primary effort is UE Sequencer choreography for the entrance — a UE-seam-agent task.

---

## 4. Recommended Stack

### Primary Recommendation: CC5 + Mutable + FAB Gear/VFX

**Rationale:** Highest quality, broadest customization range, fantasy/stylized viable, MetaHuman-skeleton-compatible, robust commercial licensing for mass character output.

| Component | Product | Cost |
|---|---|---|
| Character authoring tool | Reallusion Character Creator 5 (perpetual) | $299 |
| Scale variety generation | ActorMIXER Pro (included in CC5 Deluxe) | Included in $499 bundle |
| UE export pipeline | Reallusion Auto Setup for UE (All-in-One) | Free |
| Runtime customization | Mutable Plugin (UE5.5+ built-in) | Free |
| Fantasy morph content | Fantasy Creatures CC Morph Pack + Stylized Morphs pack | ~$50-100 (estimated from store pattern) |
| Armor assets (Stage D) | Fantasy Modular Armor Sets (FAB) | ~$50-100 (price verify on FAB) |
| Weapon assets | Modular Fantasy Weapon Pack (FAB) | ~$30-50 (price verify on FAB) |
| Elemental aura VFX | Elemental Auras VFX Pack (FAB) | ~$30-50 (price verify on FAB) |
| Additional aura VFX | Character Aura Pack V2 (FAB) or Magic Aura Bundle | ~$20-40 |
| **Estimated total** | | **~$650-900 (software + content; verifiable on FAB)** |
| **CC5 Extended Licenses** | Per content item used for mass output in commercial game | $~10-20/item additional per content pack |

**Estimated UE-seam-agent effort for MM-P1 mock:**
- CC5 authoring + export of 1 hero character: 1-2 sessions
- Auto Setup configuration in UE: 0.5 sessions
- Custom translucent/spirit-form material (Stage A): 1 session
- Elemental aura VFX integration per element: 2-3 sessions (8 elements, ~2-3 effects each)
- Armor/weapon attachment socket setup (Stage D): 1 session
- UE Sequencer Stage D reveal choreography: 2-3 sessions
- Stage C mock variant setup: 1 session
- Total estimated: ~8-12 UE-seam-agent sessions for full MM-P1 mock

---

### Secondary Recommendation: Synty Sidekick + Mutable + FAB VFX

**Rationale:** Lower cost, simpler workflow, no external authoring software required, fully UE-native. Appropriate if Matt determines stylized/low-poly aesthetic is acceptable for the mock.

| Component | Product | Cost |
|---|---|---|
| Character art system | Synty Sidekick Starter Pack (FAB) | Free |
| Fantasy character parts | Synty Sidekick Fantasy Knights (verify UE5 support) | $199.99 |
| POLYGON base characters | POLYGON Modular Fantasy Hero Characters | $149.99 |
| Runtime customization | Mutable Plugin (UE5.5+ built-in) | Free |
| Elemental aura VFX | Elemental Auras VFX Pack (FAB) | ~$30-50 |
| Additional aura VFX | Character Aura Pack V2 | ~$20-40 |
| **Estimated total** | | **~$400-440** |

**Estimated UE-seam-agent effort:** ~5-7 sessions (no external authoring tool; simpler art pipeline; lower-fidelity result).

---

### Trade-off Matrix

| Dimension | CC5 + Mutable | Synty Sidekick + Mutable | MetaHuman Crowds |
|---|---|---|---|
| Art quality ceiling | High (film/game quality; stylized + realistic) | Medium (stylized low-poly) | Very high (photorealistic only) |
| Fantasy/isekai aesthetic fit | Good (morph packs needed) | Excellent (designed for it) | Poor (requires external sculpting) |
| Spirit-form / ethereal | Via custom UE material | Via custom UE material | Via custom UE material |
| Character variety at scale | High (ActorMIXER) | High (720+ modular parts) | High (Crowds plugin) |
| Workflow complexity | Medium (external tool + export) | Low (UE-native) | Medium (in-engine but complex rig) |
| Commercial license clarity | Moderate (Extended License per item) | Clean (5-seat flat license) | Clean (Epic EULA) |
| Gear integration (arbitrary) | Supported via UE sockets | Supported via UE sockets | Supported via UE sockets |
| Cost (estimated) | $650-900 | $400-440 | $0 (+ VFX packs) |
| Production risk | Medium (CC5 is stable; Mutable is Beta) | Low (stable tools) | Medium (Crowds is experimental) |
| UE-seam-agent sessions | 8-12 | 5-7 | 6-10 |

---

## 5. License and Commercial-Use Clearance

### Recommended stack (CC5 + Mutable + FAB):

- **CC5 software:** Perpetual license, royalty-free, unlimited projects. No royalty on characters generated with CC5.
- **CC5 content items (clothing, hair, morph packs):** Extended License required for mass character output in commercial games. Extended License is per-item, adds ~50-70% above Standard License price (community reports $13 Standard vs $20 Extended on typical items). Budget per-item Extended License for each content pack used.
- **Mutable:** Unreal Engine EULA, free, royalty structure per Epic standard terms.
- **FAB gear/VFX packs:** Standard FAB commercial license included with purchase; royalty-free for commercial products. No per-character restrictions documented.
- **Fantasy Modular Armor Sets:** Standard FAB commercial license.
- **Synty (secondary):** 5-seat license per copy; royalty-free commercial use; no per-character mass output restriction documented.

### Key license risk:

Reallusion's CC content Extended License requirement for "mass character output" commercial games is the primary licensing ambiguity for the MM-P1 scenario. "Mass output" in the Extended License context refers to using CC Component files to generate many characters; it does not restrict pre-authored exported FBX/UE skeletal meshes. If characters are pre-authored in CC5 and exported as finished UE assets (FBX), the license applies at export time — the game itself does not need a per-character license for the static FBX assets shipped in the game. Clarification directly from Reallusion may be warranted for the specific scenario before committing to CC5 content-heavy pipeline.

---

## 6. Knowledge Gaps Not Resolved

1. **MetaHuman Crowds maximum simultaneous full-LOD count.** No published benchmark found for "N fully-detailed MetaHumans at 60fps on target hardware." Documentation consistently says "tens to thousands" without hardware-specific floor figures. Resolved architecturally (crowd LOD system handles scale) but specific hardware budget is unknown.

2. **Mutable Beta stability for shipping.** Official docs explicitly caution against shipping with Beta-status plugin. Whether this will graduate to stable before MM-P1 work begins is unknown. Risk: API may change in subsequent UE versions.

3. **Synty Sidekick Fantasy Knights — Unreal Engine support confirmation.** Product page on Synty Store showed Unity-only compatibility. FAB starter pack lists UE5.3-5.7 support for the Sidekick system. Per-pack UE5 support for non-starter Sidekick packs needs FAB listing verification before purchase.

4. **FAB pack pricing.** Direct FAB listing pages returned 403 errors during research. Specific prices for Fantasy Modular Armor Sets, Modular Fantasy Weapon Pack, Elemental Auras VFX Pack, and Character Aura Pack V2 could not be confirmed. Estimates based on comparable FAB products.

5. **CC5 Extended License scope for pre-exported FBX.** Whether pre-authoring characters in CC5 and shipping FBX exports (not CC Component files) requires Extended License is ambiguous in current documentation. This affects the cost model materially.

6. **Reallusion content store fantasy character pack breadth.** The full catalog of CC5-compatible fantasy/stylized packs was not fully enumerated. The Fantasy Creatures Morph Pack and Stylized Character Morphs starter pack were identified; additional isekai-specific or spirit-form content was not found.

7. **Xandra Character Creator current pricing.** Website returned redirect loops; price not confirmed. Community reports suggest ~$30-100 depending on edition.

8. **UE5.8 MetaHuman Crowds production status.** Listed as experimental in available documentation; production stability for shipping projects not confirmed.

---

## 7. Composition with MM-P1 Chernoff Substrate

Per the three substrate dimensions in the MM-P1 vision (§ 3.4 of gandalf close-out):

1. **Visual features** (color values, aura specs, glow, spirit-form shape, cloth/material): CC5 morph sliders + custom UE materials handle color/glow/shape. Cloth via Chaos Cloth on any skeletal mesh.
2. **VFX features** (particle effects per element, elemental glows, skill auras, gear auras): FAB Niagara packs (Elemental Auras, Character Aura Pack V2) cover this surface. Custom Niagara for canonical-7+1 elements not covered by off-the-shelf packs.
3. **Sound features**: No sound assets identified in this research. Sound packs are a separate research scope (not in this commission).

The substrate-to-asset reference mapping (per MM-P1's chernoff substrate vision) would work as follows:
- Primary element → aura VFX pack effect parameter set
- Period + cultural-tradition → CC5 clothing content pack selection + UE material variation
- Register + tier → CC5 HD morph parameter values + armor set selection from FAB

This composition is architecturally clean. The challenge is authoring the per-element parameter mappings — a gandalf + UE-seam-agent design task, not an asset sourcing task.

---

## 8. Effort Estimate and Risk Summary

**CC5 + Mutable stack:**
- Software acquisition: 1 day (download + configure CC5 + Auto Setup)
- Hero character authoring in CC5: 2-5 hours per character
- UE pipeline setup (Auto Setup, socket definitions, material setup): 3-5 hours once
- Mutable CustomizableObject authoring for Stage C: 4-8 hours (Beta status adds uncertainty)
- VFX pack integration per element: 1-2 hours/element
- Stage D Sequencer choreography: 4-8 hours

**Key risks:**
1. Mutable Beta status — API may shift; consider deferring Mutable to production phase and using simpler variant selection for MM-P1 mock
2. CC5 Extended License ambiguity — resolve before heavy content investment
3. Elemental aura VFX coverage gap — 5/8 canonical primaries covered by off-the-shelf pack; 3 require additional sourcing or custom authoring
4. Fantasy/stylized range of CC5 base — semi-realistic proportions are CC5's default; achieving strong isekai aesthetic requires morph pack additions; these may not reach anime-stylized extremes without custom sculpting

---

## 9. Source List

- [MetaHuman Performance and Scalability Settings | Epic Developer Community](https://dev.epicgames.com/documentation/metahuman/performance-and-scalability-settings-for-metahumans)
- [MetaHuman 5.6 / 5.7: Pipeline Reference | James Roha, Medium (May 2026)](https://medium.com/@Jamesroha/metahuman-5-6-5-7-pipeline-reference-170d302b078e)
- [UE5.6 MetaHuman Crowd System Chapter 1 | Epic Developer Community](https://dev.epicgames.com/community/learning/tutorials/EkjW/unreal-engine-5-6-metahuman-crowd-sysytem-chapter-1-metahuman-setup)
- [UE5.8: Every Major New Feature Explained (MetaHuman Crowds) | Unreal University Blog](https://www.unreal-university.blog/unreal-engine-5-8-every-major-new-feature-explained-mesh-terrain-metahuman-crowds-lumen-upgrades-more/)
- [Platform Support and LOD Specifications for MetaHumans | Epic Developer Community](https://dev.epicgames.com/documentation/metahuman/platform-support-and-lod-specifications-for-metahumans?lang=en-US)
- [Does MetaHuman support stylized characters? | Epic Developer Community Forum](https://forums.unrealengine.com/t/does-metahuman-support-stylized-characters/213339)
- [Mutable Overview in Unreal Engine | UE5.7 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/mutable-overview-in-unreal-engine)
- [Mutable Quickstart Guide | UE5.7 Documentation](https://dev.epicgames.com/documentation/unreal-engine/mutable-quickstart-guide-for-unreal-engine?lang=en-US)
- [The Mutable Sample Project is now available | Unreal Engine](https://www.unrealengine.com/news/the-mutable-sample-project-is-now-available)
- [Deep Dive into Customizations With Mutable | Unreal Fest Orlando 2025](https://forums.unrealengine.com/t/talks-and-demos-deep-dive-into-customizations-with-mutable-unreal-fest-orlando-2025/2674040)
- [UE5 Mutable Character Customization Tutorial | Unreal University Blog](https://www.unreal-university.blog/unreal-engine-5-mutable-character-customization-tutorial-2/)
- [Working with Modular Characters in Unreal Engine | UE5.7 Documentation](https://dev.epicgames.com/documentation/unreal-engine/working-with-modular-characters-in-unreal-engine?lang=en-US)
- [Reallusion Officially Launches Character Creator 5 | Reallusion Magazine (Aug 2025)](https://magazine.reallusion.com/2025/08/27/reallusion-officially-launches-character-creator-5-powering-the-next-generation-of-hd-character-creation/)
- [Here's Character Creator 5 — MetaHuman-Friendly + ActorMIXER | Digital Production (Aug 2025)](https://digitalproduction.com/2025/08/28/heres-character-creator-5-now-in-hero-quality-maya-friendly-metahuman-friendly-and-armed-with-actormixer/)
- [Characters for Unreal: CC5 Meets MetaHuman | Reallusion Magazine (Feb 2026)](https://magazine.reallusion.com/2026/02/06/characters-for-unreal-character-creator-5-meets-metahuman/)
- [CC5 vs MetaHumans | Reallusion Community Forum](https://discussions.reallusion.com/t/cc5-vs-metahumans/14296)
- [Auto Setup for Unreal Engine | Reallusion](https://www.reallusion.com/auto-setup/unreal-engine/default.html)
- [UE Auto Setup All-in-One 2.0 — UE5.7 Support | Reallusion Forum](https://discussions.reallusion.com/t/ue-auto-setup-all-in-one-2-0-is-released-now-supporting-ue-5-7/16072)
- [CC5 Deluxe Bundle | Reallusion](https://www.reallusion.com/character-creator/cc5-deluxe.html)
- [Reallusion Content License Policy](https://www.reallusion.com/license/content.html)
- [2026 Reallusion Software Subscription Options | Reallusion Magazine (Jan 2026)](https://magazine.reallusion.com/2026/01/06/2026-reallusion-software-subscription-options-expanding-your-creative-freedom/)
- [Reallusion CC5 Perpetual Pricing | Reallusion](https://www.reallusion.com/plan-and-pricing/individual/perpetual)
- [Synty Studios — Sidekick Modular Characters Free Starter Pack | FAB](https://www.fab.com/listings/8d8e9639-d93f-4f1d-8932-32ae0ef14bca)
- [Synty Studios — Sidekick Fantasy Knights Pack](https://syntystore.com/products/fantasy-knights-sidekick-modular-character-pack)
- [Synty Studios — POLYGON Modular Fantasy Hero Characters](https://syntystore.com/products/polygon-modular-fantasy-hero-characters)
- [Daz to Unreal Bridge | Daz 3D](https://www.daz3d.com/daz-to-unreal-bridge)
- [Daz Interactive License Info](https://www.daz3d.com/interactive-license-info)
- [Mixamo FAQ — Licensing | Adobe Community](https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775)
- [ModuFusion: Character Customization Unleashed | FAB](https://www.fab.com/listings/33b5c144-c1ac-4fed-a989-bb8b329f6f05)
- [Modular Character System (Multiplayer/Replicated) | FAB](https://www.fab.com/listings/9deb1166-5428-44ba-a2c0-951df7b874d7)
- [Xandra Character Creator | FAB](https://www.fab.com/listings/e73afadb-ccd5-4c53-b0ca-db155efb5b70)
- [Elemental Auras VFX Pack | FAB](https://www.fab.com/listings/5aa665cc-9300-42c6-a140-eca1bafdb875)
- [Character Aura Pack V2 | FAB](https://www.fab.com/listings/c8ac7f18-ac93-4dbd-8bb1-16edf978bbba)
- [Fantasy Modular Armor Sets | UE Marketplace](https://www.unrealengine.com/marketplace/en-US/product/fantasy-modular-armor-sets)
- [Skeletal Mesh Sockets in Unreal Engine | UE5.7 Documentation](https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-sockets-in-unreal-engine)
- [Fab 2025 Year in Review | Unreal Engine](https://www.unrealengine.com/news/fab-2025-year-in-review)

---

*Research artifact authored: 2026-06-02*
*Legolas — Mode A analytical research*
*Output path: `agentic_orchestration/legolas/research/2026-06-02-unreal-character-customization-research/synthesis.md`*
