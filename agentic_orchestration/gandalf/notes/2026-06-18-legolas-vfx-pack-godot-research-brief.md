# Legolas Mode-A Research Commission — VFX Asset Packs for the Godot GPUParticles3D Pipeline

**STATUS:** ACTIVE COMMISSION (Legolas Mode-A analytical research; Matt-authorized 2026-06-18)
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-18 — "launch a Legolas research run to gather all of the top contenders for VFX packs which may either be native to Godot or be available for a similar break-down and re-assemble in godot style pipeline. Legolas should make recommendations but provide many links so that I can review them myself … we need both POE/Diablo register and also 400+ character uniqueness, breadth of combinatory choice catalogue."
**Mode:** A (analytical research; read-only; web + prior-art synthesis). NOT a Mode-B catalogue crawl.
**Findings home:** `agentic_orchestration/legolas/research/2026-06-18-godot-vfx-packs/` (synthesis + a flat `links.md` of every URL, grouped by pack) per your OP. Deliver as text; gandalf persists.
**Companion docs (read for context, do NOT re-derive):**
- `agentic_orchestration/gandalf/pushback/2026-06-17-pixel-vfx-into-godot-register-conflict.md` — the LOCKED-register ruling that governs this whole search.
- `canonical/story/style-register.md` — the locked register-2 decision.
- `agentic_orchestration/gandalf/notes/2026-06-17-legolas-modular-procgen-godot-research-brief.md` + `agentic_orchestration/legolas/research/2026-06-17-godot-procgen/findings.md` — the SEPARATE Synty-environment research (already complete; do not duplicate).
- `agentic_orchestration/gandalf/notes/2026-06-18-scene-scoring-rubric-opportunity-memo.md` — the genre-register calibration-ladder dive your register reads feed.
- Prior VFX research to reconcile against (pre-Godot-pivot): `agentic_orchestration/legolas/research/ue-fab-cosmograph-vfx-survey-2026-06-06/`.

---

## 0. Why this research

The project rebuilds combat VFX as **Godot 4.x `GPUParticles3D`** systems for a solo ARPG. The locked aesthetic target is **PoE / Diablo 2–4 register**, composited over **stylized-low-poly-3D (Synty) environments**. We need a base VFX library — Godot-native where possible, harvestable-into-Godot where the high-register look demands it — that can drive **400+ procedurally-generated kits per season**, each reading as visually distinct. This commission scouts **all the top contender packs and the Unity/Unreal→Godot harvest-and-rebuild tooling**, evaluated for register-fit, parametric controllability, slot coverage, and licensing-at-scale. It is **options-and-fit with many links for Matt's own review** — not a single buy recommendation (top-N per category, with reasoning, is the deliverable).

## 1. The framing that governs the ENTIRE search (read this first)

Three locked constraints shape every evaluation. An option that violates them is flagged, not silently dropped.

### 1a. The register is LOCKED — and it is STYLIZED, not photoreal

Per the 2026-06-17 ruling: the register is **register-2 = stylized-low-poly-3D (Synty), premium-lit**, and the **locked VFX strategy is "S-tier `GPUParticles3D` juice + dramatic GI lighting"** (a body-anchored particle bloom already scored VFX-presence 5/5). **Pixel-art / hand-drawn-flipbook VFX are RULED OUT** — they collide with smooth 3D Synty and read as "two games stapled together." That boundary is closed; do not surface pixel/2D-flipbook packs as candidates.

**The critical nuance — register-fit is a TWO-SIDED boundary, and it is your headline evaluation axis:**
- **Under-shoot** (pixel / flat / low-fidelity) → collision (already ruled out).
- **Over-shoot** (gritty-photoreal / hyper-realistic VFX) → ALSO a potential collision. Synty environments are *stylized-clean-low-poly*. A photoreal volumetric fireball over flat-shaded polygon walls reads as mismatched the same way pixel does, on the other side.
- **The Goldilocks target:** *stylized* VFX that carry **PoE/D2-register JUICE** — additive/HDR bloom, multi-layer compositing, flowmap/noise churn, ember/residual layering, element-legible color, readable cast→impact motion — **that composite naturally over stylized-low-poly geometry.** D2 and PoE are themselves stylized-painterly, NOT photoreal; that is the reference point. "Juicy and legible and layered," not "realistic."

For **every** pack, return a **register-fit-to-Synty verdict**: `stylized-clean | stylized-gritty | semi-real | photoreal`, and `under / ON / over` for the stylized-low-poly target. This is the axis the existing PoE/Diablo-register framing in the mobile brief does NOT capture, and it is the one most likely to determine fit.

### 1b. "400+ uniqueness" is a PARAMETRIC-AXIS problem, not an asset-count problem

We do NOT want 400 hand-authored hero effects (does not scale to procedural generation), and we do NOT want random recombination of a few assets (reads as asset-flip). Uniqueness-that-scales = **substrate-DRIVEN parametric variance**: each kit's VFX is a deterministic function of its substrate identity, so two kits that differ in substrate *visibly* differ in VFX in a way the player can READ. Our player-legible substrate axes:
- **element** → hue + texture/material
- **geometry / form** (16-type geometry palette: projectile / beam / area / orb / cone / nova / etc.) → silhouette + motion-shape
- **tier** → scale + emission intensity + layer count
- **archetype** (damage / support / control / hybrid) → cast behavior

**Therefore the scale-critical evaluation axis is: how many INDEPENDENT parametric knobs does each pack expose?** A pack with one-click *recolor only* gives us element-variance but nothing for form/tier. A pack exposing **color + scale + emission + shape/noise + lifecycle-timing** lets us project *four* substrate dimensions onto VFX variance — that is what turns ~30 base assets into hundreds of *meaningfully-distinct* (not just shuffled) spells. Report the **parametric-axis inventory** per pack: which of {color/hue · scale · emission/intensity · shape/noise-texture · lifecycle/timing · trail/sub-emitter params} are author-exposed, and via what mechanism (tool script / shader uniform / recolor script / particle-material). This is the same manifest discipline the gear pipeline already uses (element→hue/finish manifest) — the VFX manifest is its sibling.

### 1c. Scale = 400+ kits/season auto-assigned by an LLM → LICENSE is load-bearing

VFX are auto-assigned across hundreds of kits per season in a commercial product. **Licensing terms are a first-class evaluation axis, not a footnote.** For every pack: CC0 vs commercial-perpetual vs per-seat vs per-title vs royalty; and for any Unity/Unreal pack we'd *harvest* (import to extract textures/meshes, rebuild emitters in Godot), whether the EULA permits **cross-engine reference-capture + asset extraction for a port** (most "you own the art" licenses do, but cross-engine is an edge case — flag explicitly). CC0 native-Godot packs have **zero** licensing friction at auto-assignment scale; weight that heavily in recommendations.

**Evaluate every option against:** *register-fit-to-Synty · parametric-axis count · slot coverage · license-at-scale · Godot-native-or-harvest-cost.*

## 2. Research questions, by category

### Category 1 — Godot-NATIVE VFX packs (the zero-friction backbone) — HIGHEST PRIORITY
- The backbone strategy: a Godot-native pack needs no porting, runs as `GPUParticles3D` immediately, and (if CC0) carries no per-kit licensing. Find **all** serious contenders, not just the obvious.
- **Verify and position the two seed candidates** (do not assume — confirm current state, license, Godot version, parametric controls, and coverage):
  - **Binbun — Godot Effects Collection Vol. 1** (binbun3d.itch.io) — claimed CC0, Godot 4.x native, tool-script color/emission control, noise-driven shapes. The mobile brief proposes it as the parametric backbone. Confirm CC0 status, coverage list, and the actual parametric-axis inventory.
  - **Bukkbeek — EffectBlocks** (bukkbeek.itch.io/effectblocks) — claimed Godot 4.x native, 60+ effects, decals/ground/residual strength. Confirm license (NOT confirmed CC0), coverage, parametric controls.
- **Cast wide for OTHER Godot-native VFX packs** across Godot Asset Library, itch.io, and other marketplaces: any 3D `GPUParticles`-based spell/combat/magic VFX collections. For each: coverage, Godot 4.x version, license, cost, parametric-axis inventory, register-fit verdict, and **links (store + video/gallery)**.

### Category 2 — Unity VFX packs worth HARVESTING (the high-register anchor + the Unity→Godot flow)
- The harvest model: buy for the *art* (textures, flipbooks, trail/beam meshes, noise maps), rebuild emission as Godot `GPUParticles3D`. Unity behavior (Shuriken graphs, shaders) does NOT port.
- **Verify and position the seed candidate:** **Hovl Studio — RPG VFX Bundle** (Unity Asset Store) — claimed closest off-the-shelf PoE/D2–4 match, one-click recolor script, broad slot coverage. Confirm current contents, price, EULA cross-engine-extraction terms, **and critically give a register-fit-to-Synty verdict** (is it stylized-gritty that composites over Synty, or photoreal that over-shoots? — §1a).
- **Cast wide:** other top-rated Unity ARPG/magic/spell VFX packs in the PoE/Diablo register (e.g. other Hovl packs, Kvél, Archanor, SungJ, Gabriel Aguiar-adjacent commercial packs, etc.). For each: coverage, price, EULA cross-engine terms, parametric/recolor controls, **register-fit verdict**, harvest-cost estimate, and links.

### Category 3 — Unreal Engine / Fab VFX packs worth harvesting (we HAVE a UE seam)
- The team has a UE 5.7 seam (mantis) — UE packs are harvestable too (textures/meshes extract; Niagara behavior does not port to Godot, same as Unity).
- Reconcile against the prior `ue-fab-cosmograph-vfx-survey-2026-06-06` (pre-Godot-pivot) — what from it is still relevant to a *Godot-harvest* (not UE-native) use?
- Top Fab / UE Marketplace ARPG/magic VFX in PoE/Diablo register: coverage, price, license/extraction terms, **register-fit verdict**, harvest cost, links. Flag whether UE→Godot harvest is meaningfully harder than Unity→Godot (it generally is — note why).

### Category 4 — The Unity/Unreal → Godot VFX HARVEST-AND-REBUILD tooling + workflow landscape
- This is the "Unity→Godot VFX flow" Matt named. Survey the *tooling*, not just packs:
  - **Texture/flipbook extraction** approaches (walking a `.unitypackage` / pack `Textures/` folder; `.unitypackage` unpackers; AssetRipper-class tools and their license/legitimacy posture).
  - **Mesh conversion** (FBX→glTF via Blender CLI for trail/beam/impact-cone meshes; pivot/origin cleanup).
  - **Any existing Unity→Godot VFX porting guides, community pipelines, plugins, or converters** (note the `synty-godot-converter` exists for meshes — is there any VFX-specific analog?).
  - **Godot `GPUParticles3D` + `ParticleProcessMaterial` / custom-shader rebuild** references — community tutorials on reproducing additive/HDR/flowmap VFX in Godot specifically.
- Deliver this as a **workflow synthesis** (the reusable parse pipeline), with links — it is built once and reused per pack.

### Category 5 — Slot-coverage + parametric-control map (the composability matrix)
- The composition model: `cast (origin flash) → travel (projectile + trail) → impact (hit burst) → residual (ground flame / scorch decal / smoke)`, plus `ground-AoE · beam · nova/area · buff/debuff aura · portal · loot-beam · decal`.
- Build a **slot × pack** coverage grid: which packs populate which slots, so coverage gaps (and over-purchase) are visible. Cross-pack mixing is the multiplier (~6 casts × 8 travels × 10 impacts × 5 residuals ≈ hundreds), so coverage breadth per slot matters more than raw count.
- Note for each pack its **parametric-axis inventory** (§1b) in the same grid.

### Category 6 — Register characterization + MANY links (for Matt's review AND the rubric ladder)
- Matt will review packs himself — so for **every** candidate, collect **multiple links**: store/product page, a video/turntable if one exists, and a still-gallery. Group them in a flat `links.md` by pack.
- Per pack, a **qualitative register read** (stylized-clean / stylized-gritty / semi-real / photoreal; clean vs detailed; bloom-heavy vs flat) — this feeds the genre-register calibration ladder (the rubric dive), where pack reference frames may later be scored by galadriel's CV instrument onto the same T0–T3 scale as PoE/D2/D4/Last-Epoch exemplars.

## 3. What good looks like (deliverable)

An **options matrix** — each pack × { engine/format (Godot-native | Unity-harvest | UE-harvest) · what-it-actually-contains · slot coverage · **parametric-axis inventory** · **register-fit-to-Synty verdict** · Godot-4.x-native-or-harvest-cost · license-at-scale (CC0 | commercial | per-seat | per-title | royalty; cross-engine-extraction OK?) · cost · **links (store + video + gallery)** }. Plus:
- A short narrative **synthesis**.
- **Top-3 Godot-native** + **Top-3 Unity-harvest** + **Top-2 UE-harvest** candidates, each with reasoning tied to the §1 axes.
- A **slot × pack coverage grid** (Category 5).
- The **harvest-pipeline workflow synthesis** (Category 4), with links.
- A flat **`links.md`** — every URL, grouped by pack, for Matt's own review.

NOT a single adoption call (the team decides). Options + fit + many links, with the register-fit and license-at-scale verdicts explicit for each.

## 4. Constraints + context
- **Engine:** Godot 4.x. Runtime target: `GPUParticles3D` + `ParticleProcessMaterial`/custom-shader.
- **Register:** register-2 stylized-low-poly-3D (Synty), premium-lit. **Stylized PoE/D2 JUICE, not photoreal** (§1a). Pixel/2D-flipbook RULED OUT.
- **Scale:** 400+ kits/season, LLM auto-assigned → license + parametric-axis count are load-bearing (§1b, §1c).
- **Substrate axes the VFX must express:** element (hue/texture) · geometry/form (silhouette/motion) · tier (scale/emission/layering) · archetype (cast behavior).
- **Read-only.** License + IP flags matter — confirm commercial-use AND cross-engine-extraction terms for anything purchasable/harvestable.

## 5. Out of scope
- **The critic-in-the-loop LOOP architecture itself** (swap-consistency, modality decomposition, multi-view verification, MCP live-editor wiring) — that is the rubric-ladder dive + a separate tooling thread, not this research.
- **Synty modular-ENVIRONMENT packs / procedural assembly** — already researched (`2026-06-17-godot-procgen/findings.md`). This run is VFX only.
- **Pixel-art / 2D-flipbook VFX** — register-ruled-out (do not surface).
- **The buy/adoption decision** — you surface options + fit + links; the team (and Matt) decide.

---

**Signed:** gandalf, 2026-06-18.
**For:** commissioning a Legolas Mode-A scan of the Godot VFX-pack option space — Godot-native backbones, Unity/Unreal harvest anchors, and the harvest-and-rebuild tooling — framed throughout by **register-fit-to-stylized-Synty** (two-sided: pixel under-shoots, photoreal over-shoots, stylized-juicy is the target), **parametric-axis count** (the substrate-mapping capacity that makes 400+ kits *meaningfully* distinct), and **license-at-scale** — so the team can choose a register-coherent, scale-viable VFX library, with many links for Matt's own review.
