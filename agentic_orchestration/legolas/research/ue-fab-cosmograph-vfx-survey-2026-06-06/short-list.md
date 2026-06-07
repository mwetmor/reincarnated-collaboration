# UE FAB Cosmograph VFX Asset Survey — Short-List
# 2026-06-06

**Mode:** A (analytical)
**Commissioner:** gandalf / mantis (criterion 3.7 STRETCH support)
**Parent dispatch:** `agentic_orchestration/dispatches/2026-06-06-mantis-ue-architecture-validation-spike.md` § 9
**Cross-reference:** `agentic_orchestration/legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md`
**Discipline anchor:** #11 empirical-first — UE version compatibility claims are cited verbatim from source; inference vs confirmed claim is explicitly flagged per asset.

---

## Survey Summary

Nine assets shortlisted across five target classes (nebula Niagara VFX, cosmic dust / stardust particles, lens flare / bloom, skybox space textures, constellation-line aesthetics). The free Epic Niagara Examples Pack (UE5.7 native, confirmed) is the mandatory first-install before any paid asset is acquired — it covers the non-cosmic VFX foundation and its Niagara systems are open and composable. The cosmic-register gap in that free pack is real: no nebula, no stardust, no stellar effects are included, creating clear acquisition targets.

**Key finding on UE 5.7 compatibility:** FAB blocks direct fetch (403), preventing verbatim version-string extraction from listing pages for most assets. Where a verbatim version string was obtained from a third-party mirror (psdly.co.uk: "4.27 And 5.0 – 5.7" for LENS FLARE VFX), it is marked CONFIRMED-VERBATIM. For assets where version string was not extractable, best-available evidence is cited and marked accordingly. Mantis MUST verify version strings at install-time on PC via the Epic Launcher "Supported Engine Versions" field before integration.

**Substrate-led flag:** None of these assets distort substrate-derived star positions. All are decorative atmospheric layers on top of the procedural Niagara point cloud. The cosmograph architecture stays substrate-led — positions remain UMAP-derived; these assets add atmospheric register only.

**Critical gap:** Space Nebula and Starfield V2/V3 (Isara Tech) — a user post from 2026 asked "When will there be an update for version 5.7?" with no developer response found. This asset is flagged RED for 5.7 compatibility until mantis verifies on PC.

---

## Short-List

---

### Asset 1 — Epic Niagara Examples Pack (UE5.7)

| Field | Value |
|---|---|
| **Asset name** | Niagara Examples Pack |
| **Creator / seller** | Epic Games |
| **FAB URL** | https://www.fab.com/listings/0e188eca-4e54-4fb2-a9ed-d8b8a565e600 |
| **Price** | FREE |
| **Cost classification** | FREE |

**UE 5.7 compatibility:** CONFIRMED. The pack was released by Epic specifically for UE5.7 (source: Unreal Engine official news, February 2026: "Discover over 50 free Niagara systems ready to use in Unreal Engine 5.7"). It is the first release of the Niagara Examples Pack initiative.

**Contents:** 50+ Niagara systems covering explosions, ballistic impacts, sparks, fire, smoke, mist, weapon buffs/debuffs, Animation-Notify footsteps, pings, markers, lightning, hit dissolves, trails. Scalability groups assigned per emitter for multi-platform performance.

**Cosmic-register coverage:** NONE. Confirmed gap: no nebula, no stardust, no stellar, no space-themed effects are included in this release. Epic stated the pack will be updated over time — cosmic content may arrive in future updates but is not present now (June 2026).

**Composability with procedural Niagara cosmograph:** FULL. All systems are standard open Niagara assets; no closed-system behavior. Systems can be placed alongside a 100-star Niagara point cloud without conflict.

**Acquisition + integration handoff note for mantis:** Download from FAB directly via Epic Launcher (UE5.7 engine, add to project). Install first before any paid packs. Use as baseline VFX library. Do NOT expect cosmic/stellar effects — treat as foundation layer only.

---

### Asset 2 — VDB Nebula for Unreal Engine 5.3+ (Arghanion's Puzzlebox)

| Field | Value |
|---|---|
| **Asset name** | [FREE Project] VDB Nebula for Unreal Engine 5.3+ |
| **Creator / seller** | Arghanion's Puzzlebox |
| **FAB URL** | https://www.fab.com/listings/668b1f95-9db2-4a7b-b2d2-46a626890fcf |
| **Price** | FREE (coupon code VDBNEBULA100 for 100% discount on Gumroad mirror) |
| **Cost classification** | FREE |

**UE 5.7 compatibility:** INFERRED from "5.3+" designation. The FAB listing explicitly states "Unreal Engine 5.3+" which covers 5.3, 5.4, 5.5, 5.6, 5.7. No explicit 5.7 test confirmation found in sources. VDB rendering in UE5 is a first-class engine feature (Heterogeneous Volumes) that has been stable since 5.3 with no known breaking changes in 5.5-5.7. Risk: LOW. Mantis should verify at install-time.

**Contents:** VDB (OpenVDB format) nebula asset from The Pixel Lab. Includes material shader setup and scene setup. VDB file provided standalone. Tutorial materials for importing, configuring materials, optimizing.

**Rendering approach:** Heterogeneous Volumes / VDB volume rendering (UE5 native Heterogeneous Volumes actor). Not Niagara-based. Renders as a 3D volumetric mesh-like object in world space.

**Composability with procedural Niagara cosmograph:** HIGH. VDB actor renders in world space as a volumetric object. A Niagara 100-star point cloud placed in the same scene will composite naturally on top of / inside the nebula volume. This is the standard UE5 scene layering pattern. No architectural conflict.

**Substrate-led flag:** CLEAR. VDB is purely decorative atmospheric fill. It does not assign positions or identities to stars; it occupies space around the Niagara point cloud.

**Acquisition + integration handoff note for mantis:** Add to project from FAB. Place a Heterogeneous Volumes actor in the test scene. Assign the VDB material. Adjust density + color to taste as atmospheric backdrop. Niagara point cloud emitter goes on top as a separate component. No plugin dependency — VDB rendering is native UE5.

---

### Asset 3 — Cosmic Forge Skybox Collection Pack (Arghanion's Puzzlebox)

| Field | Value |
|---|---|
| **Asset name** | Cosmic Forge Skybox Collection Pack |
| **Creator / seller** | Arghanion's Puzzlebox |
| **FAB URL** | https://www.fab.com/listings/d03ee571-d83a-42b4-bf03-b54c1484d7c1 |
| **Price** | Not confirmed from available sources (advertised at 40% discount; base price unknown). Individual volumes available separately. |
| **Cost classification** | PAID (price unconfirmed — mantis verify on FAB before acquisition) |

**UE 5.7 compatibility:** INFERRED. This is an HDR skybox texture + Blueprint Material Setup project. The Blueprint Material system has not had breaking changes between UE5.3 and 5.7. Individual volumes on the marketplace show UE5.x compatibility listings. No explicit 5.7 test found in sources. Risk: LOW for the texture/material layer; Blueprint setup may need minor updates.

**Contents:** 30 HDR skybox textures combined with alpha maps. Starfields included for depth layering. Animated nebula cubemap. Blackhole Blueprint. Blueprint Material Setup supporting up to 2 simultaneous HDRIs, 2 starfields, Flow Map animation for main cubemap. Customization parameters: Brightness, Saturation, Intensity, independent rotation of 2nd skybox, Sun Disk Mask.

**Rendering approach:** HDR CUBEMAP + Blueprint Material. Renders via the sky sphere / HDRI Backdrop actor in UE5. Not Niagara-based.

**Composability with procedural Niagara cosmograph:** HIGH. Sky sphere / HDRI Backdrop renders at infinite distance as the environment backdrop. Niagara point cloud (100 stars at mid-distance) and VDB nebula (mid-distance volumetric) composite cleanly in front of the skybox. Standard UE5 layering.

**Substrate-led flag:** CLEAR. Skybox is background environment only. Does not assign or move star positions.

**Acquisition + integration handoff note for mantis:** Add to project from FAB. Use as the far-background sky sphere. Pair with VDB nebula (Asset 2) at mid-distance and Niagara point cloud at near-foreground. Confirm Blueprint Material compiles in UE5.7 at first launch — if shader recompile is needed, that is expected and normal for cross-version assets.

---

### Asset 4 — 8K HDRI Galaxy Backgrounds (Mathew81)

| Field | Value |
|---|---|
| **Asset name** | 8K HDRI Galaxy Backgrounds — Space & Nebula 360° Skybox Pack |
| **Creator / seller** | Mathew81 |
| **FAB URL** | https://www.fab.com/listings/b9a10a63-7c02-4964-824e-e04632786076 |
| **Price** | Not confirmed from available sources. The related "22x 8K HDR Starfields" pack is listed at "from $9.99" — this pack is likely in the same range. Mantis verify on FAB. |
| **Cost classification** | PAID (likely $9.99–$19.99; verify) |

**UE 5.7 compatibility:** INFERRED engine-agnostic. Source quote: "Perfect for Unity, Unreal Engine, and all major 3D tools." Format: 32-bit .HDR equirectangular files — pure texture assets with no engine-specific code. HDRI textures are engine-version-agnostic; they import via the standard UE Texture Import pipeline which has not changed in 5.x. Risk: NONE for the textures themselves. The UE project wrapping may need recompile.

**Contents:** 10 true 8K (8192×4096) HDRI maps in 32-bit .HDR format; 2:1 equirectangular ratio (360° spherical). Galaxy, nebula, and deep space environments. Described as "professionally rendered (not AI-generated or upscaled)."

**Rendering approach:** Pure HDR texture files. Used via HDRI Backdrop actor or as Sky Light cubemap source. No Niagara systems; no code.

**Composability with procedural Niagara cosmograph:** FULL. Texture-only assets; zero architectural coupling. Import texture, use as HDRI Backdrop / SkyLight source. Niagara point cloud and VDB nebula layer on top.

**Substrate-led flag:** CLEAR. Background textures only.

**Acquisition + integration handoff note for mantis:** Import .HDR files into UE5.7 project via Content Browser drag-drop or Import. Set as HDRI Backdrop or Sky Light source. No plugin or Blueprint required. Consider as an alternative backdrop to Asset 3 (Cosmic Forge) if the Cosmic Forge Blueprint setup has 5.7 friction.

---

### Asset 5 — LENS FLARE VFX | Advanced Sprite-Based Lens Flares

| Field | Value |
|---|---|
| **Asset name** | LENS FLARE VFX | ADVANCED SPRITE BASED LENS FLARES |
| **Creator / seller** | Not confirmed by name from available sources |
| **FAB URL** | https://www.fab.com/listings/0e920fbc-fb78-4331-a4e1-878dc3504bad |
| **Price** | $29.99 (source: psdly.co.uk mirror, confirmed) |
| **Cost classification** | PAID — $29.99 |

**UE 5.7 compatibility:** CONFIRMED-VERBATIM from third-party mirror (psdly.co.uk URL title text): "LENS FLARE VFX | ADVANCED SPRITE BASED LENS FLARES (4.27 And 5.0 – 5.7)". This is the verbatim version range claim. This is the most strongly confirmed 5.7 compatibility in this short-list.

**Contents:** Sprite-based photorealistic lens flare solution. Core elements: HDR chromatic ghosts, starburst patterns, halo rings, spectral dispersions, anamorphic streaks, hexagonal bokeh artifacts. V1.1 adds single Ghosts up to 8 elements, FOV correction, UV distortions for streak gradients. Rating: 4.8 / 5 (23 reviews).

**Rendering approach:** World-space sprite-based particles. Both world-space and screen-space material variants included. GPU-based (V1.1 update: "fully GPU based"). Not a post-process volume lens flare — sprites are placed per light source in world space, meaning each of the 100 cosmograph stars can have its own configurable lens flare sprite instance.

**Composability with procedural Niagara cosmograph:** HIGH. Sprite-based system: a lens flare actor/component is attached to each Niagara star particle (or driven from star positions). Per-star brightness parameters can be exposed as Niagara User Parameters driving the flare intensity. This is a direct composability fit for the cosmograph criterion 3.7 use case (per-star brightness elevation).

**Substrate-led flag:** CLEAR. Lens flares are driven by star positions from the Niagara point cloud; they do not reposition stars.

**Acquisition + integration handoff note for mantis:** Add to project from FAB. For the cosmograph 3D test: spawn one lens flare component per Niagara star particle (or use a decoupled sprite overlay driven by particle positions via Blueprint). Wire the flare intensity to a `StarBrightness` Niagara User Parameter. Test that 100 simultaneous flare instances remain within 60fps budget on PC.

---

### Asset 6 — Cinematic Lens Flares v4 (image-based + Niagara)

| Field | Value |
|---|---|
| **Asset name** | Cinematic Lens Flares (Version 4) |
| **Creator / seller** | Not confirmed by name from available sources |
| **FAB URL** | https://www.fab.com/listings/74825eda-ba0f-4e0e-abcc-133c6cec9c3c |
| **Price** | Not confirmed from available sources — mantis verify on FAB |
| **Cost classification** | PAID (price unconfirmed) |

**UE 5.7 compatibility:** NOT CONFIRMED from sources. Asset is actively updated (V4 is current; V3 had major Niagara integration overhaul). Given V4 was released in 2025 and is actively sold on FAB, strong likelihood of 5.7 support, but no verbatim version string extracted. Mantis must verify on FAB listing before acquisition.

**Contents:** Image-based lens flare implementation using convolution bloom + Niagara for performance. V4 adds Lens Ghost Fisheye toggle, Diffusion Noise controls, configurable Aperture shaping. Works with Lumen rasterized rendering and Path Tracer (separate non-Niagara version included for path tracer). Also works with forward renderer.

**Rendering approach:** Niagara-based at runtime (lens flare logic at reduced resolution for 100x performance speedup vs. post-process method). Requires Niagara Fluids Plugin enabled. High visual quality; cinematic-grade output.

**Composability with procedural Niagara cosmograph:** MEDIUM-HIGH. Niagara Fluids dependency is a plugin requirement (must be enabled before asset import). The flare system is designed for scene-level light sources, not per-particle per-star assignment; adapting it to 100 stars individually would require custom Blueprint wiring. Asset 5 (sprite-based) may be easier to wire per-star. However, the visual quality ceiling is higher.

**Note on priority:** If Asset 5 (sprite-based, confirmed 5.7) proves adequate for per-star flare quality, Cinematic Lens Flares v4 may be deferred to a polish pass. Recommend mantis evaluate Asset 5 first.

**Acquisition + integration handoff note for mantis:** Before purchasing, verify 5.7 compatibility on FAB listing "Supported Engine Versions" field. Enable Niagara Fluids Plugin in project settings. Evaluate whether per-star adaptation is feasible within criterion 3.7 spike time budget.

---

### Asset 7 — Niagara Constellations (SoerGame)

| Field | Value |
|---|---|
| **Asset name** | Niagara Constellations |
| **Creator / seller** | SoerGame |
| **FAB URL** | https://www.unrealengine.com/marketplace/en-US/product/niagara-constellations |
| **Price** | Not confirmed — also available as part of "Big Niagara Bundle" |
| **Cost classification** | PAID (price unconfirmed — verify on FAB) |

**UE 5.7 compatibility:** NOT CONFIRMED from sources. Original publication date: September 2021. No version update record found for 2024-2025. Rating: 3.7/5 (3 ratings) — low confidence. Risk: MEDIUM-HIGH for 5.7 compatibility. Mantis must check "Supported Engine Versions" on FAB listing before acquisition.

**Contents:** Niagara VFX including constellations, planets, galaxies, nebulae, constellation clusters, globular clusters, black holes, small universes, big bang, star track effects, meteor rain. Tagged: Constellation, Universe, Space, Particle.

**Rendering approach:** Niagara particle systems (confirmed — listed under Niagara VFX category).

**Composability with procedural Niagara cosmograph:** HIGH IF version-compatible. Open Niagara systems can be dropped into the same scene as the procedural 100-star point cloud. The constellation visual patterns in this pack are the closest FAB analogue to the cosmograph's procedural constellation lines.

**Key qualification:** The constellations in this pack are likely pre-authored fixed-topology Niagara emitters — they are NOT dynamically driven by substrate-derived star positions. The cosmograph architecture requires the constellation line topology to derive from the procedurally generated 100-star positions (UMAP-derived). This pack is therefore a REFERENCE VISUAL / TECHNIQUE STUDY, not a drop-in replacement for the custom procedural constellation line system described in prior synthesis (2026-06-02, § 1).

**Substrate-led flag:** CONDITIONAL CONCERN. If mantis treats these pre-authored constellations as the cosmograph output, that violates substrate-led discipline (they impose a fixed aesthetic over the substrate-derived positions). Use as visual reference and technique study only.

**Acquisition + integration handoff note for mantis:** Verify 5.7 on FAB. If confirmed: acquire as a visual reference pack. Open the Niagara systems in-editor to study the star-point + connecting-line emitter architecture. Do not use these systems directly as cosmograph output — custom procedural system per prior synthesis § 1 is still required. The pack's existing constellation aesthetics can inform the visual styling choices for the custom system.

---

### Asset 8 — Niagara Galaxy (Niagara.VFX seller)

| Field | Value |
|---|---|
| **Asset name** | Niagara Galaxy |
| **Creator / seller** | Niagara.VFX (seller page: https://www.fab.com/sellers/Niagara.VFX) |
| **FAB URL** | https://www.fab.com/listings/1a252757-0a9d-4fe8-bd18-474a2a2bf707 |
| **Price** | $29.99 (source: FAB search result snippet) |
| **Cost classification** | PAID — $29.99 |

**UE 5.7 compatibility:** NOT CONFIRMED from sources. No explicit version string found. Described as "completely created within the Niagara ecosystem" — standard Niagara systems typically carry forward across minor UE versions without breaking, but code-plugin or custom module dependencies can break. Risk: LOW-MEDIUM. Mantis verify on FAB.

**Contents:** 2 Niagara Systems — galaxy vortex effect + clouds vortex effect. Each system commented to explain modules. Designed for space exploration games and virtual production.

**Rendering approach:** Pure Niagara particle systems (confirmed). GPU-simulated galaxy vortex. Real-time.

**Composability with procedural Niagara cosmograph:** HIGH. Both systems are standard open Niagara assets. Galaxy vortex can serve as background mid-distance atmospheric layer in the same scene as the 100-star Niagara point cloud. The "clouds vortex" variant provides a softer nebula-cloud analogue to the VDB approach from Asset 2.

**Substrate-led flag:** CLEAR. Galaxy vortex is background environmental fill. Does not interact with star positions.

**Acquisition + integration handoff note for mantis:** Verify 5.7 compatibility on FAB. If confirmed, add to project. In the criterion 3.7 scene, place galaxy vortex Niagara system as a mid-distance atmospheric layer. Measure FPS impact of adding it alongside the 100-star point cloud. Note: 2 Niagara systems vs. 1 VDB — expect different GPU pressure profiles; profile both.

---

### Asset 9 — Volumetric Nebula and Clouds (Sameek Kundu / Athian Games)

| Field | Value |
|---|---|
| **Asset name** | Volumetric Nebula and Clouds |
| **Creator / seller** | Sameek Kundu (Athian Games) |
| **FAB URL** | https://www.fab.com/listings/3c902769-c907-4901-bb98-dfd9e1c5cf53 |
| **Price** | $49.99 (source: ArtStation marketplace listing for same asset) |
| **Cost classification** | PAID — $49.99 |

**UE 5.7 compatibility:** NOT CONFIRMED from sources. Forum thread mentions user concern about moving from 5.3 to 5.6 "in what feels like a blink of an eye" with no developer response about 5.6/5.7 support captured. Asset uses GPU compute shaders — these CAN require recompilation or updates across major UE versions. Risk: MEDIUM. Mantis must verify on FAB listing before acquisition.

**Contents:** Plugin with GPU compute shaders for volumetric cloud and nebula rendering. Multiple professional noise algorithms: Perlin-Worley hybrid noise, Musgrave fractals, Simplex noise. Dynamic volumetric lighting using density raymarching materials. Blueprint-friendly interface. Data-asset customization system.

**Rendering approach:** Plugin-based; GPU compute shaders + raymarching. NOT Niagara-based — this is a separate volumetric rendering system. Produces higher-fidelity volumetric nebula than the VDB approach (Asset 2) but carries a plugin dependency and higher integration complexity.

**Composability with procedural Niagara cosmograph:** MEDIUM. Plugin-based renderer operates in world space and should be composable with Niagara particle systems in the same scene at the engine level. However, potential rendering order / depth-buffer interaction with Niagara translucent particles requires testing. Noted as the highest-integration-complexity asset on this short-list.

**Note on acquisition sequencing:** Asset 2 (VDB Nebula, FREE) should be evaluated first. If VDB quality is sufficient for criterion 3.7 STRETCH visual register, Asset 9 is deferred to a polish pass. Asset 9 is justified only if VDB quality is insufficient and volumetric fidelity is required to achieve "cosmos register" verdict.

**Acquisition + integration handoff note for mantis:** Verify 5.7 compatibility FIRST before purchase ($49.99). Enable plugin in UE5.7 project settings. Test composite with 100-star Niagara point cloud. Profile GPU memory impact (compute shaders + raymarching carry heavier GPU budget than VDB). Flag if integration risk exceeds available spike time.

---

## Excluded Assets and Rationale

| Asset | Exclusion reason |
|---|---|
| Space Nebula and Starfield V2/V3 (Isara Tech) | Forum post (April 2026): user asked "When will there be an update for version 5.7?" — no developer response. This is a C++ code plugin; if not updated for 5.7, it will not compile. Excluded pending developer confirmation. If Isara Tech confirms 5.7 support, re-evaluate as a STRETCH inclusion for a full procedural volumetric nebula renderer. |
| Volumetric Space Nebula Procedural Generator (Ambient GraphX) | Forum post on FAB shows "Coming soon to the FAB Marketplace" — not yet released. Last confirmed version range: 4.26–5.4. Excluded. |
| Niagara Solar System (various) | Covers crab nebula / cat eye nebula / helix nebula as Niagara systems but no version data confirmed. These are named-astronomical-object representations, not cosmograph-composable atmospheric fill. Low relevance to criterion 3.7. |
| Cosmic VFX (SoftTofuVFX) | Contents: Grenade, Meteor Explosion, Magic circle, Laser, Slash. Combat VFX. Not cosmograph-composable. Excluded. |
| Niagara Constellations (note, NOT excluded) | Retained as Asset 7 with explicit substrate-led qualification. |

---

## Asset Priority Sequence for Criterion 3.7 Build

Recommended acquisition and install order for mantis at criterion 3.7 spike time:

1. **Asset 1 (Epic Niagara Examples Pack, FREE)** — Install first, unconditionally. Foundation Niagara library.
2. **Asset 2 (VDB Nebula, FREE)** — Install immediately after. Provides nebula volumetric for zero cost. Evaluate if it achieves "cosmos register" at moderate effort.
3. **Asset 3 or 4 (Skybox)** — Choose one backdrop. Cosmic Forge (Asset 3) for UE Blueprint-driven parametric control; Mathew81 8K HDRI (Asset 4) as simpler fallback if Asset 3 has 5.7 friction.
4. **Asset 5 (LENS FLARE VFX, $29.99, confirmed 5.7)** — Per-star brightness elevation. Install if criterion 3.7 visual register evaluation requires per-star polish.
5. **Asset 7 (Niagara Constellations, verify version first)** — Visual reference study for constellation line technique. Acquire if version-confirmed; study the Niagara architecture.
6. **Asset 8 (Niagara Galaxy, $29.99, verify version first)** — Background galaxy vortex atmospheric. Optional; evaluate FPS impact.
7. **Asset 9 (Volumetric Nebula and Clouds, $49.99, verify version first)** — Only if Asset 2 VDB quality is insufficient. Highest integration complexity.
8. **Asset 6 (Cinematic Lens Flares v4, verify version first)** — Optional polish pass after criterion 3.7 baseline pass/fail determined.

**Maximum free-path cost:** $0 (Assets 1, 2 only — sufficient for a minimal criterion 3.7 smoke test of cosmos register).
**Minimal paid-path cost:** $29.99 (add Asset 5, lens flares, for per-star brightness elevation).
**Full short-list cost ceiling:** ~$130–$150 (all paid assets acquired), pending Matt authorization.

---

## Prior Synthesis Cross-Reference

The prior synthesis (2026-06-02-constellation-form-ue-techniques) covers:
- Holographic character materials (Stage A.0 — not relevant to criterion 3.7 cosmograph)
- Star-point + constellation-line Niagara technique (§ 1 — DIRECTLY relevant; the 100-star point cloud and constellation lines in criterion 3.7 use the same dual-renderer plexus pattern)
- Parameter binding patterns (§ 4, 6 — apply to cosmograph per-star brightness / color driving)

The 2026-06-02 synthesis does NOT cover: nebula volumetric assets, skybox space textures, lens flare packs for per-star elevation, or cosmic dust backgrounds. This survey fills those gaps.

**Composability of the two research bodies:** The criterion 3.7 scene is a superset of the Stage A constellation rendering minus the character mesh. Specifically:
- Star-point Niagara emitter (prior synthesis § 1 custom) provides the 100-star point cloud
- Constellation-line Niagara emitter (prior synthesis § 1 SpriteBasedLine technique) provides procedural lines
- Asset 2 (VDB nebula) provides volumetric atmospheric depth
- Asset 3 or 4 (skybox) provides infinite-distance backdrop
- Asset 5 (lens flares) provides per-star brightness elevation
- Elemental Auras VFX Pack (prior synthesis § 3.6) is NOT needed for criterion 3.7 (no character; pure cosmograph)

---

## Knowledge Gaps Not Resolved

1. **Exact prices for Assets 3, 6, 7 not confirmed.** FAB 403 blocks direct listing fetch. All three require price check on FAB before acquisition authorization request.

2. **UE 5.7 compatibility verbatim strings for Assets 2, 3, 4, 6, 7, 8, 9** not obtained directly from FAB listing pages. All are INFERRED from evidence. Mantis must check the "Supported Engine Versions" field on the FAB listing page in the Epic Launcher or web browser for each asset before install.

3. **Space Nebula and Starfield V2/V3 (Isara Tech) UE 5.7 status** unresolved. If developer confirms 5.7 support, this is a high-value addition: it is a fully procedural volumetric space renderer that can generate volume textures for Niagara. Would elevate the nebula volumetric from Assets 2/9.

4. **Niagara Constellations (Asset 7) version support history** is unclear — published 2021, no update record found. Low trust score.

5. **Lens flare per-star instancing cost** at 100 simultaneous stars is not benchmarked by any source. Mantis must profile on PC during criterion 3.7 test; this is the main FPS risk for lens flare assets.

---

## Source List

| Source | URL | Access date |
|---|---|---|
| Unreal Engine — 50+ Free Niagara Systems for UE5.7 | https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7 | 2026-06-06 |
| Creative Bloq — 50+ Free UE5 VFX systems (FAB URL extraction) | https://www.creativebloq.com/3d/video-game-design/grab-over-50-free-unreal-engine-5-vfx-systems | 2026-06-06 |
| 80.lv — Epic Shares 50+ Free Niagara for UE5.7 | https://80.lv/articles/epic-releases-over-50-free-niagara-systems-for-ue5-7 | 2026-06-06 |
| psdly.co.uk — LENS FLARE VFX mirror (version string source) | https://www.psdly.co.uk/lens-flare-vfx-advanced-sprite-based-lens-flares | 2026-06-06 |
| FAB listing — VDB Nebula (Arghanion) | https://www.fab.com/listings/668b1f95-9db2-4a7b-b2d2-46a626890fcf | 2026-06-06 |
| FAB listing — Space Nebula and Starfield V2 (V3) | https://www.fab.com/listings/fa195a46-e4f2-4c32-ba64-e09ab2835717 | 2026-06-06 |
| FAB listing — Volumetric Space Nebula Procedural Generator | https://www.fab.com/listings/c94e0b17-cf04-470e-ba93-5d2319a1c0d9 | 2026-06-06 |
| FAB listing — Niagara Solar System | https://www.fab.com/listings/77fafaef-eb9c-4cec-992d-369f330fbe68 | 2026-06-06 |
| FAB listing — Volumetric Nebula and Clouds | https://www.fab.com/listings/3c902769-c907-4901-bb98-dfd9e1c5cf53 | 2026-06-06 |
| FAB listing — Space Skybox Collection | https://www.fab.com/listings/6a05bcef-aad1-4733-980f-2eb0bd93079b | 2026-06-06 |
| FAB listing — Cinematic Lens Flares | https://www.fab.com/listings/74825eda-ba0f-4e0e-abcc-133c6cec9c3c | 2026-06-06 |
| FAB listing — LENS FLARE VFX | ADVANCED SPRITE BASED LENS FLARES | https://www.fab.com/listings/0e920fbc-fb78-4331-a4e1-878dc3504bad | 2026-06-06 |
| FAB listing — Niagara Constellations (SoerGame) | https://www.unrealengine.com/marketplace/en-US/product/niagara-constellations | 2026-06-06 |
| FAB listing — Niagara Galaxy | https://www.fab.com/listings/1a252757-0a9d-4fe8-bd18-474a2a2bf707 | 2026-06-06 |
| FAB listing — 8K HDRI Galaxy Backgrounds (Mathew81) | https://www.fab.com/listings/b9a10a63-7c02-4964-824e-e04632786076 | 2026-06-06 |
| FAB listing — Cosmic Forge Skybox Collection Pack | https://www.fab.com/listings/d03ee571-d83a-42b4-bf03-b54c1484d7c1 | 2026-06-06 |
| Epic Community Forums — Space Nebula and Starfield plugin thread (p8) | https://forums.unrealengine.com/t/space-nebula-and-starfield-plugin-v1-v2-v3-for-ue4/74138?page=8 | 2026-06-06 |
| Epic Community Forums — Volumetric Space Nebula (forum) | https://forums.unrealengine.com/t/volumetric-space-nebula/2104803 | 2026-06-06 |
| Epic Community Forums — Volumetric Nebula and Clouds plugin release | https://forums.unrealengine.com/t/volumetric-nebula-and-clouds-plugin-now-available-on-fab-marketplace/2589317 | 2026-06-06 |
| Epic Community Forums — Athian Games Volumetric Nebulae and Clouds | https://forums.unrealengine.com/t/athian-games-volumetric-nebulae-and-clouds/2578603 | 2026-06-06 |
| Epic Community Forums — Mathew81 8K HDR Starfields | https://forums.unrealengine.com/t/mathew81-22x-8k-hdr-starfields-deep-space-skybox-collection/2675943 | 2026-06-06 |
| Epic Community Forums — Mathew81 8K HDRI Galaxy Backgrounds | https://forums.unrealengine.com/t/mathew81-8k-hdri-galaxy-backgrounds-space-nebula-360-skybox-pack/2664047 | 2026-06-06 |
| Epic Community Forums — Arghanion Cosmic Forge Skybox Collection Pack | https://forums.unrealengine.com/t/arghanions-puzzlebox-cosmic-forge-skybox-collection-pack/2424302 | 2026-06-06 |
| Epic Community Forums — VDB Nebula (Arghanion) | https://forums.unrealengine.com/t/arghanions-puzzlebox-free-project-vdb-nebula-for-unreal-engine-5-3/2424406 | 2026-06-06 |
| 3dprojectmasters — Cosmic Forge Volumetric Nebulas | https://3dprojectmasters.com/products/cosmic-forge-volumetric-nebulas-unreal-engine-5 | 2026-06-06 |
| Arghanion Gumroad — VDB Nebula free | https://arghanion.gumroad.com/l/nrwoux | 2026-06-06 |
| Prior legolas synthesis — 2026-06-02-constellation-form-ue-techniques | `agentic_orchestration/legolas/research/2026-06-02-constellation-form-ue-techniques/synthesis.md` | 2026-06-02 |

---

*Research artifact authored: 2026-06-06*
*Legolas — Mode A analytical research*
*Output path: `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-06/short-list.md`*
*Commission: mantis UE architecture-validation spike § 9 (criterion 3.7 STRETCH parallel sub-step)*
