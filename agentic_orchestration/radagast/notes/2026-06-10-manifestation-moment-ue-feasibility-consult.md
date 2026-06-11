# Manifestation Moment ("Grassy Knoll") — UE 5.7 Feasibility Assessment + Recommended Architecture + Implementation Plan

> **STATUS:** CURRENT (PC-seam design-feasibility consult — radagast Pattern A-deep-class artifact; Fable-5 first-run)
>
> **Verdict up front: BUILDABLE.** The scene as canonically defined is achievable in UE 5.7 on the existing project substrate. Most subsystems sit on proven in-project empirical anchors (mantis spike GREEN + WS3.1 close). The single biggest risk is the **spirit-form ambiguous→defined transformation continuum** (§ 2.4/§ 2.5 of the creation-moment canon) — the one subsystem carrying the scene's emotional payload with zero in-project empirical anchor. Spike candidates S2–S4 below de-risk it.

**Date:** 2026-06-10
**Author:** radagast (PC-side design steward)
**Commission:** `agentic_orchestration/gandalf/notes/2026-06-10-radagast-fable5-manifestation-moment-consult-commission.md` (gandalf, Matt-authorized)
**Audience:** Matt + Mac-gandalf (design review); David-H (sequencing input); mantis (spike-candidate consumer); Sam (audit trail)
**Gate disposition:** design-generation artifact for Matt + Mac-gandalf review per commission § Authority; no dispatch is being fired, so Sam Gate-1 is not invoked at this artifact.
**Companion artifact (this session):** `agentic_orchestration/radagast/notes/2026-06-10-consultation-mac-gandalf-cosmograph-spatial-layout-contract.md` (cross-host consultation per drift-discipline § 6.2 — engine-emit contract proposal in § 6.7 below is cross-cutting)

---

## 0. Canonical-source-consultation declaration

### Read IN FULL this session

| # | Doc | Why |
|---|---|---|
| 1 | `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (all 919 lines: § 1–§ 10 base + § 11 Tal Rasha addendum + § 12 elicitation-cascade addendum) | THE authoritative scene definition |
| 2 | `canonical/story/2026-06-05-cosmograph-pivot.md` (§ 0–§ 10 incl. 2026-06-06 § 9 + 2026-06-09 § 10 amendments) | Substrate architecture; lookup-not-generation runtime boundary; primitive-as-glyph register; UE 3D port forward-reference § 10.6 |
| 3 | `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` | Founding architecture; ownership boundaries; drift-discipline § 6 |
| 4 | `agentic_orchestration/gandalf/notes/2026-06-10-ue-manifestation-moment-mvp-framing-brief.md` | MVP first-slice scoping + falsifiable floor + open questions addressed to me (§ 4) |
| 5 | `agentic_orchestration/gandalf/notes/2026-06-10-kit-to-star-sign-assignment-spec.md` | The `kit_star_sign_assignments.json` schema v1.1 contract (injective Branch A binding) |
| 6 | `agentic_orchestration/david-h/notes/2026-06-10-ws3-1-wave-close.md` | WS3.1 sequencer-asset close (just landed; directly relevant) |
| 7 | `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/spike-findings-report.md` | Spike OVERALL GREEN; per-criterion verdicts |
| 8 | `…/criterion-3-7-stretch-3d-cosmograph.md` | Niagara point-cloud cosmograph empirical FPS + LOD architecture |
| 9 | `…/criterion-3-2-meshy-ue-import.md` | Meshy→UE import path; skeleton convention; Interchange/Slate constraint; T-pose constraint |
| 10 | `…/criterion-3-4-niagara-json.md` | Niagara JSON parameter-binding path (production-validated) |
| 11 | `…/criterion-3-6-taa-tsr.md` | TSR/TAA 60 FPS empirical + ARPG config |
| 12 | `agentic_orchestration/mantis/notes/2026-06-10-niagara-add-emitter-windowed-verification.md` | Niagara authoring tooling state; DDC-warm prerequisite; `create_niagara_system_from_spec` workaround |
| 13 | `agentic_orchestration/dispatches/2026-06-10-david-h-ws3-materialization-cinematic-sequencer-commission.md` | WS3 cinematic structure (4-phase transformation; acceptance criteria) |
| 14 | `agentic_orchestration/gandalf/notes/2026-06-10-radagast-fable5-manifestation-moment-consult-commission.md` | This commission |
| 15 | `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` (mantis) | Live UE project state; launch flags; TODO gates |

### Read in TARGETED SECTIONS (declared honestly as partial)

| Doc | Sections read |
|---|---|
| `canonical/00-ground-state.md` | TL;DR + § 1 current-truth table (oracle navigation per its own protocol) |
| `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md` | § 0–§ 3 (5 DataTable schemas + ingestion path + acceptance criteria) |
| `agentic_orchestration/dispatches/2026-06-10-gandalf-substrate-registry-sidecar-design-spec.md` | § 0–§ 2.1 (schema head + seam ownership) |
| `agentic_orchestration/dispatches/2026-06-10-gandalf-experiential-axes-sidecar-design-spec.md` | § 0–§ 2.1 (schema head + seam ownership) |

### Consumed via canonical absorption (NOT re-read this session; declared)

- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` — its § 4.1/§ 4.2 commitments are absorbed verbatim into cosmograph-pivot § 10 + creation-moment § 11, both read in full above.
- `canonical/story/2026-06-06-atomic-substrate-registry.md`, `canonical/17` spirit guide, `canonical/38` D1–D10 — consumed via their load-bearing absorption into the creation-moment doc § 3 composition table + ground-state § 1 rows + criterion 3.6's D1-mitigation citation. Where a claim below leans on one of these, I cite the absorbing doc.

### Prior radagast notes touching character/VFX/Mutable

**None exist.** `agentic_orchestration/radagast/notes/` was empty at session start — this is the first substantive radagast file artifact. No prior-self to consult; declared for completeness.

---

## 1. Scene understanding (restated for shared-understanding confirmation)

### 1.1 What the manifestation moment IS

The player's first creation moment is a **scene, not a menu**: the player's Earth avatar — an ordinary, modern-day human, the persistent Earth Self — stands on a hill on Earth at night, beside an **ambiguous spirit form** (a translucent, luminescent, roughly-humanoid mist: the spirit-guide-in-becoming). Overhead is the **celestial sphere**, and the celestial sphere IS the cosmograph — in-fiction reality, not metaphor. Star-signs render as constellations on the sphere's interior surface (kit-as-constellation, Branch A 1:1 kit↔star-sign binding); primitive-group anchors render as large, monochromatic, atmospheric **rune-glyphs** "drawn by light only" (Tal Rasha register); the deeper 3D nebula context lives beyond the sphere as visual depth.

The player selects their spirit through one of two convergent paths (Path L lasso / Path I drop-ingredients), unified post-§ 12 under the **spirit-guide-driven elicitation cascade + cycling-preview UX**: the guide asks "What is most important for your journey this season?"; the player cycles text options on the iPad surface; the sky responds with illumination/zoom; commits cascade 3–5 layers; the engine resolves a **nearest-kit-centroid LOOKUP** (never runtime generation); the spirit form transforms continuously toward the matched kit as composition progresses.

At confirm, the **materialization cinematic** (§ 2.5; = WS3's `LS_Materialization_Cinematic`) fires: the spirit form solidifies through four phases (concretization → racial embodiment → elemental attunement → weapon instantiation), the selected constellation may visually descend into the spirit, the Earth avatar reacts, and the scene transitions into gameplay onboarding.

**Target player experience:** awe, identity-crystallization, the weight of a new beginning — "a moment of quiet possibility before transformation." The sky is the dominant compositional element; the mundane-human-beside-the-becoming is the visual story; the falsifiable floor is Matt's integrative judgment: *"this feels like a meaningful, mythic creation moment."*

### 1.2 Deltas between the commission framing and canon (CANON WINS — flagged for Mac-gandalf)

1. **Where manifestation happens.** The commission frames the scene as "the moment the player's reincarnated character manifests **in the new world**." Canon (§ 2.1): the scene is on **Earth** — the spirit form manifests beside the Earth avatar on the Earth hill; the crossing into the new world happens at the scene's *exit* (transition to gameplay onboarding, § 2.5 step "transitions into gameplay onboarding"). The knoll is the **departure threshold, not the arrival**. This matters architecturally: the environment is Earth-pastoral (mundane register), not new-world-fantastical, and the in/out transitions are asymmetric (quiet entry, threshold-crossing exit). Canon wins; assessed accordingly below.
2. **Set-piece vs interactive surface.** The commission's "narrative-experiential set-piece" framing is true of the confirm-time materialization cinematic, but canon makes the scene as a whole an **interactive creation surface** (cascade + cycling-preview + dual-path). The MVP framing brief correctly slices the *static scene + atmosphere* first; I preserve that slicing — but feasibility below covers the full canonical scene so nothing is silently dropped.
3. **"Bound to a star-sign"** — confirmed exactly per Branch A (kit binds 1:1 to star-sign; `kit_star_sign_assignments.json` v1.1 enforces injectivity). No delta.
4. **Naming.** "Grassy knoll" appears in the MVP brief; canon § 2.1 says "a hill on Earth." Same thing; no delta — noted only so future search hits both.

---

## 2. UE 5.7 feasibility assessment, by subsystem

Difficulty scale: **LOW** (proven in-project or trivial) / **MODERATE** (industry-standard, not yet proven in-project) / **HIGH** (no proven pattern at the required quality; spike before commit).

### 2.1 The manifesting player-form / avatar

**Three distinct bodies are in play — they have different answers:**

**(a) Earth avatar (modern human, idle).** Difficulty: **LOW–MODERATE.** The pipeline is proven end-to-end for the Crusader (criterion 3.2 PASS: GLB → interactive Interchange import → clean Mixamo-convention skeleton, Hips root, ~24 bones → Meshy-baked idle plays natively). Per Matt's no-Crusader constraint the MVP needs one new generic modern-day human via image-gen → Meshy **image-to-3D**. Honest gaps: (i) the **image-to-3D + rig path is NOT yet proven in-project** — criterion 3.1 used *text-to-3D*, and the Crusader was a Meshy-provided biped; (ii) the rig step lives in the Meshy **web app only** (API returns zero skeleton — criterion 3.2 Session 1 empirical), so a one-time manual rig/export step per asset is on the critical path; (iii) the reference image MUST be T-pose/A-pose, no items in hands, no secondary entities (Matt 2026-06-07 constraint). All known, all cheap — see spike S6.

**(b) Ambiguous spirit form.** Difficulty: **MODERATE.** This is **not a Mutable use-case at this scene** (pushback registered below, § 3.1). The canonical register — "luminescent mist-cloud roughly humanoid, translucent, soft edges, subtle internal motion" — is a **Niagara + material** problem, not a mesh-customization problem: a hidden/ghosted base humanoid mesh sampled by a Niagara Skeletal Mesh Data Interface emitter (particles drift on/near the surface) + a translucent emissive Fresnel material at low opacity. Industry-standard pattern; zero in-project anchor yet (spike S2).

**(c) The defined final form (matched kit's avatar).** Difficulty: **MODERATE at vertical-slice scale; pipeline-bound at corpus scale.** Per the lookup-not-generation boundary (cosmograph-pivot § 4.1), final-form meshes are **pre-generated offline assets** (engine identity → Meshy pipeline → UE import), resolved at runtime by kit_id. For the vertical slice: 3 hand-built kit forms (the 3 hand-curated anchor kits — Duskweaver↔Mula, Cannonade Cleric↔Krittika, Stonefist↔Hercules — are the natural picks). At 37-kit or ~1000-kit scale this becomes an asset-pipeline workstream with the manual Meshy-web-app rig step as the bottleneck; that's a later-slice production problem, not a scene-feasibility problem. Flagged, not designed here (scope guard).

**The transformation continuum (ambiguous → partially-defined → defined, § 2.4 "continuously responsive").** Difficulty: **HIGH at full generality; MODERATE as staged registers.** True topological morphing between arbitrary Meshy meshes is **not feasible** (no shared topology/UVs across independently generated meshes — this is a structural property of the asset pipeline, not a UE limitation). The honest architecture is **staged register transitions**: the spirit form's *ambiguous* and *partial* states live entirely in the Niagara + material domain (color saturation via user parameters, silhouette sharpening via particle tightness + opacity, weapon-outline hints via a secondary emitter), and the *defined* state is a **mesh reveal** (final-form mesh dissolves in via material-parameter dissolve while the particle body hands off — particles converge to the mesh surface and extinguish). The player reads continuous becoming; the implementation is discrete underneath. This is the scene's emotional payload and its biggest unproven surface — spikes S2/S3/S4.

### 2.2 The cosmograph night-sky

Difficulty: **MODERATE** — the strongest empirical base of any subsystem, with one honest gap.

**What's proven (criterion 3.7, Session 3):** `NS_CosmographPointCloud` Niagara CPU-sprite point cloud at 100 / 1,000 / **15,000** stars all at ~92 FPS uncapped (sprite-only stack) on the RTX 4060 Ti; `SetNiagaraArrayVector` position ingestion from JSON validated as the production API; LOD architecture designed (Level 0 = centroids / 1 = 300 / 2 = full) and confirmed *not required* for PC 60 FPS at sprite-only cost; Spawn Burst placement gotcha documented (Emitter Spawn, not Emitter Update).

**What's NOT proven:** the spike rendered a **freestanding point cloud at ±35…±240 UU bounds orbited by a free camera** — not a **sphere-interior sky viewed from ground POV at sky scale**. Unproven: TSR temporal stability on small bright additive sprites near the horizon during sphere rotation ("twirl the sky" = the whole starfield moves — a TSR ghosting stress case the idle-anim 3.6 test does not cover); sprite angular-size tuning at sphere-radius distance; the full effects stack (ribbon constellation edges + emissive star material + rune glyphs + nebula backdrop) which criterion 3.7 explicitly carved out. Spike S1.

**Approach per layer (recommendation + rejected alternatives in § 3.2):**
- **Stars:** Niagara point cloud with positions projected onto the sphere interior surface — NOT a skybox texture (the sky must respond per-cluster to cycling-preview attention, brighten/dim per ingredient-drop, and support lasso resolution; baked textures can't), NOT per-star static meshes (draw-call explosion at 1,000+).
- **Constellation figures (kit layer):** Niagara ribbon emitter for edges (criterion 3.7 Emitter B architecture; untested → S1 includes it).
- **Rune-glyph anchors (Tal Rasha layer):** per cosmograph-pivot § 10.6 forward-reference — SplineMesh + emissive material for strokes + Niagara particle-based atmospheric diffusion for the halo. For the MVP slice, the framing brief's decision-point stands; my recommendation: include **one** placeholder rune in the MVP scene (cheap: one spline + one emissive material + one diffuse halo sprite emitter) — the mythic register of the sky is materially carried by the glyph layer, and testing it in 3D early is one of the cheapest high-information moves available.
- **Nebula context beyond sphere:** MVP = HDRI/static skybox backdrop beyond the sphere radius (cheap, controllable). Production = VDB volumetric via Heterogeneous Volumes (free FAB asset already identified by legolas survey; never placed in-project → optional spike S7).
- **Sphere rotation ("twirl"):** rotate the star-position container (Niagara system transform or a parent scene component), never the camera — preserves the ground-anchored POV that makes the sky feel like sky.

### 2.3 The manifestation VFX (Niagara)

Difficulty: **MODERATE**, with a **tooling prerequisite**, not a capability question.

The beat decomposes into four Niagara problems, all standard-pattern: (i) **ambient spirit-form body** (skeletal-mesh-surface sampling — S2); (ii) **coalescence** at materialization (particles attracted to final-form mesh surface positions — Skeletal Mesh DI + curl-noise-damped attraction; the classic "form coalesces from motes" pattern — S3); (iii) **constellation-descent** (§ 2.5: ribbon/beam from the selected constellation's sky position down into the spirit's chest — a Niagara ribbon with a spline-following velocity field; straightforward); (iv) **element-tinted aura** on the defined form (criterion 3.4's validated JSON→`SetNiagaraVariableLinearColor` binding path carries element color directly from kit data — proven).

**Tooling state (load-bearing):** db-lyon `add_emitter_to_system` crashed headless (`NiagaraHandlers.cpp:595`, null-RHI precondition) and windowed verification is blocked on **cold shader DDC** — resolution is Matt running the editor interactively once (5–10 min, one-time; documented in the windowed-verification note § 6). The documented `create_niagara_system_from_spec` workaround means VFX authoring can proceed regardless (mantis Option A recommendation, which I endorse). All mantis windowed launches must use `-noraytracing -unattended -nosplash` (AGENT_STATE flags). **D7 check:** the manifestation beat is visual; the only text/voice surfaces are spirit-guide narration (templated per § 12.9) and UI copy — no runtime LLM anywhere in this subsystem. PASS by construction.

### 2.4 Lighting / atmosphere / the knoll threshold environment

Difficulty: **LOW–MODERATE tech; the bar is art-direction, not capability.**

The canonical tension: a **night exterior where the sky is the dominant light source** while two ground figures stay readable. Pure emissive-sky Lumen lighting at night is noisy and hard to art-direct; the recommended hybrid (§ 3.4) is a low-intensity directional "moonlight" key + a skylight fed from the cosmograph's cubemap capture + a local soft glow light parented to the spirit form (which beautifully motivates ground-figure readability *diegetically* — the becoming itself lights the scene). Known traps, all manageable: auto-exposure will fight the bright-sky/dark-ground composition (lock exposure manually); translucent spirit-form material sorting against additive sky sprites (test in S2); foliage wind on the knoll grass is trivially cheap (landscape grass + simple wind). TSR at 60 FPS is proven on this hardware (criterion 3.6) with the ARPG config documented (motion blur off, History SP 100, ghost rejection 2, per-bone motion vectors). The real gate is the MVP brief's falsifiable-floor #5 (Matt's mythic-weight judgment) — which is exactly why the static-scene-first slicing is right.

One MVP-fairness note (answers framing-brief § 4 question): for the #5 judgment to be *fair*, the lighting/atmosphere pass must be at least "deliberate" even where assets are placeholder — a placeholder mesh under intentional lighting reads mythic; a good mesh under default lighting never will. Budget the lighting pass as first-class MVP scope, not polish.

### 2.5 Animation + sequencer orchestration of the beat

Difficulty: **LOW for orchestration (proven); MODERATE for the transformation keyframing.**

WS3.1 just closed GREEN: `LS_Materialization_Cinematic` exists on disk, persists across editor restarts, with the canonical **4-master-track + audio-sections structure** (CameraCut + Transform + Event + single Audio master carrying both music/SFX and spirit-guide-voice as *sections* — the master-track idempotency constraint Sam's WARN-WS3-1-A locked in; any audio work here must use `add_section`, never a second Audio master). db-lyon Sequencer actions are validated 7/7. The remaining orchestration work is already phase-planned (WS3.2–3.5): bind the Transform track to an actual spirit-form actor (currently unbound — WS3.2 entry-gate), keyframe the 4-phase transformation, spawn + bind a CineCameraActor (WS3.4), integrate templated voice placeholders (WS3.3, D7-compliant: templated TTS placeholder or silent caption per WARN-D).

**The architecturally honest observation:** the 4-phase transformation is **not purely a Transform-track problem** — concretization/racial/elemental/weapon phases are mostly *material-parameter and Niagara-parameter* animations (dissolve values, saturation, emitter activation) plus a mesh-visibility swap, with transform keys playing a supporting role. The Sequencer needs **material-parameter tracks and/or Event-track-driven Blueprint calls** as the primary animation surface for WS3.2. The Event track placeholder from WS3.1 anticipated exactly this; the WS3.2 dispatch author should scope it explicitly. Camera: for the MVP and the cinematic both, **authored framing** (fixed or gently-rotatable look-up), not free-look — awe is a composition property, and free-look hands the composition to chance (answers framing-brief § 4).

**Transitions in/out:** IN — from the Earth-avatar pre-scene if Q4(a) lands, else from title flow; a slow look-up tilt (ground → sky) is the natural establishing move and doubles as the sky's reveal. OUT — § 2.5's optional camera fly-out into the nebula context, then cut to onboarding; the fly-out is cheap (camera rail through the sphere shell) and is the one place the player ever leaves the ground POV, which is precisely what makes the threshold-crossing read. Both are Sequencer work on the proven stack. Gameplay-onboarding content beyond the cut is out of scope (scope guard).

---

## 3. Recommended technical architecture (per subsystem, with the why + rejected alternative)

### 3.1 Avatar + spirit form

| Decision | Recommendation | Rejected alternative + why |
|---|---|---|
| Earth avatar asset | Image-gen → Meshy image-to-3D (T-pose ref) → web-app rig → GLB → interactive Interchange import (per MVP brief § 2) | Crusader reuse — Matt-prohibited; CC5/MetaHuman — manual art authoring per character fights the substrate-driven pipeline (criterion 3.2 fallback note), and MVP needs exactly one neutral human |
| Spirit form (ambiguous) | Niagara skeletal-mesh-surface emitter over a hidden base humanoid + translucent emissive Fresnel ghost material | **Mutable — REJECTED at this scene (pushback).** Nothing in canon selects Mutable; the project has not chosen it (substrate-led: don't pre-impose); Mutable solves *parametric mesh customization*, but the spirit form is *not a mesh being customized* — it's a luminous becoming. Mutable re-enters only if Earth-avatar customization (Q4a) lands later, as a separate decision |
| Transformation continuum | Staged register transitions: Niagara/material states for ambiguous+partial; dissolve-in mesh reveal w/ particle handoff for defined | True progressive mesh morph — infeasible across independently-generated Meshy meshes (no shared topology); chasing it would burn the schedule on an invisible distinction |
| Final-form resolution | Runtime mesh-swap from pre-imported per-kit assets keyed by kit_id (lookup-not-generation per cosmograph-pivot § 4.1) | Runtime generation of any kind — violates the engine-pregenerates/game-selects boundary AND D7 |

### 3.2 Cosmograph sky

| Decision | Recommendation | Rejected alternative + why |
|---|---|---|
| Star layer | Niagara point cloud (proven `NS_CosmographPointCloud` lineage), positions on sphere interior surface via `SetNiagaraArrayVector`, per-cluster brightness/color user-parameter arrays for cycling-preview response | Skybox texture — cannot respond per-cluster to attention/commit/lasso; static meshes per star — draw-call cost with zero benefit |
| Sphere geometry | Logical sphere (positions projected to radius R around the scene origin), rotated via container transform for "twirl" | Physical inverted-sphere mesh with star material — couples star data to UVs, fights per-star data binding, and LOD becomes texture work |
| Rune anchors | SplineMesh + emissive strokes + Niagara halo diffusion (per cosmograph-pivot § 10.6); ONE placeholder rune in MVP | Defer entirely — cheap to include one, and the Tal Rasha register in 3D is the highest-information unknown in the sky's mythic read; full 6→7-group curation stays deferred per Pattern B |
| Nebula context | MVP: HDRI/static backdrop beyond sphere. Production: VDB Heterogeneous Volume (free FAB asset) | Niagara volumetric from day one — cost/complexity before the scene feeling validates |
| LOD | Adopt criterion 3.7 LOD architecture from day one for production (Level 0/1/2), even though PC sprite-only doesn't need it — mobile (D8) + full effects stack will | No-LOD — contradicts criterion 3.7's own production caveat |

### 3.3 Manifestation VFX

| Decision | Recommendation | Rejected alternative + why |
|---|---|---|
| Authoring path | `create_niagara_system_from_spec` (documented db-lyon workaround) until `add_emitter_to_system` windowed verification closes; `-noraytracing` flag standing | Blocking VFX work on the windowed verification — mantis Option A already argued this correctly; I concur |
| Coalescence | Skeletal Mesh DI surface-attraction emitter (motes converge to final-form surface) + curl noise | Pre-rendered VFX flipbook — fights per-kit element tinting and camera freedom |
| Element binding | Criterion 3.4's validated JSON→Niagara parameter path (`SetNiagaraVariableLinearColor` etc.) fed from DT_Kit | Hand-authored per-element systems — doesn't scale past the vertical slice and ignores a proven data path |

### 3.4 Lighting / environment

Hybrid rig: low-intensity moonlight directional key + skylight (cosmograph cubemap capture) + spirit-form glow as diegetic fill; manual exposure lock; Lumen ON but with the sky contribution art-directed rather than emissive-driven. Rejected: pure-emissive Lumen night (noisy, hard to direct); fully baked lighting (kills the spirit-form's dynamic glow + sky response). Knoll: landscape + grass + wind, horizon low, composition sky-dominant per canon.

### 3.5 Sequencer / animation

Continue the WS3 stack exactly as closed: `LS_Materialization_Cinematic` 4-master-track structure; **add material-parameter/Event-driven animation as the primary WS3.2 surface** (transform keys secondary); audio always as sections within the single Audio master; CineCameraActor authored framing; templated-voice placeholders (D7). Rejected: rebuilding the cinematic as Blueprint-timeline logic — Sequencer is validated, authorable via db-lyon, and gives the cinematic to non-programmer iteration.

---

## 4. Implementation plan / sequencing (phased, with dependencies)

**Phase 0 — prerequisites (mostly Mac-side / Matt; all already in flight or named):**
P0.1 Matt warms shader DDC (one-time interactive editor open; unblocks all windowed Niagara work). P0.2 Path A completion: engine push of the two sidecars + PC clones of `reincarnated-engine` / `reincarnated-loadout` (Mac-side scheduling per WS3.1 wave-close § 4.1) → unblocks WS1. P0.3 Pattern-B scope-lock with Matt per framing-brief § 4 (rune-in-MVP / camera / spirit-form fidelity / art-finish bar — recommendations supplied in § 2–§ 3 above).

**Phase 1 — static scene slice (the MVP brief's falsifiable floor; can fire NOW, independent of WS1):**
P1.1 Knoll environment + lighting rig (§ 3.4) — first-class scope. P1.2 Earth avatar pipeline (spike S6 IS this work: image-gen → Meshy → rig → import; parallelizable with P1.1). P1.3 Sky: Niagara point cloud projected on sphere interior, **scaffold star positions** (flagged § 7), one placeholder rune, HDRI nebula backdrop (folds spike S1). P1.4 Static ambiguous spirit form (folds spike S2). P1.5 Assemble + Matt #5 mythic-weight judgment. **Gate: #5 PASS before any interaction-layer commissioning** (recognition-validate-commit).

**Phase 2 — data binding (gates on P0.2; mostly already commissioned as WS1):**
P2.1 WS1 five DataTables ingest (DT_Kit / DT_KitStarSign / DT_StarSign / DT_PrimitiveFamily / DT_ExperientialAxis). P2.2 Substrate-accurate star positions replace P1.3 scaffold — **requires the cosmograph spatial-layout contract that does not yet exist** (§ 6.7; consultation filed). P2.3 Element-tint + identity fields wired from DT_Kit into spirit form + VFX.

**Phase 3 — materialization cinematic completion (gates on WS1 GREEN per WS3 phase-partition; spirit-form actor from Phase 1 satisfies the WS3.2 binding need):**
P3.1 WS3.2 4-phase transformation (material/Niagara-parameter-first keyframing + mesh reveal; folds spikes S3/S4). P3.2 WS3.3 voice sections (templated, into existing Audio master via `add_section`). P3.3 WS3.4 camera composition + in/out transitions (look-up establish; nebula fly-out exit). P3.4 WS3.5 end-to-end + criterion #9 data-binding verification.

**Phase 4 — interaction layers (separate commission; explicitly post-#5-validation):** cascade UI (iPad text surface), cycling-preview sky response, lasso, convergence pacing — out of this consult's build scope by design.

**Dependency spine:** P0.1 → S2/S3/S4 (windowed Niagara). P0.2 → WS1 → Phase 2 → Phase 3 fire-gate. Phase 1 depends on nothing upstream — **it is the highest-leverage immediately-fireable work.**

---

## 5. Risks, unknowns, and Mantis spike candidates

| ID | Spike | What it proves | Cost | Risk if skipped |
|---|---|---|---|---|
| **S1** | **Sphere-interior sky render** — project tier-2 (1,000-star) data onto sphere interior; ground POV; rotate sphere; add ribbon edges + emissive star material + HDRI backdrop; measure TSR stability + FPS at full stack | The scene's sky actually works AS A SKY (criterion 3.7 tested a freestanding cloud, not this); TSR vs rotating starfield ghosting; sprite sizing at sky distance | CHEAP–MODERATE (0.5–1 session; free assets) | Sky reads as particle effect, not heavens; TSR smearing on twirl discovered late |
| **S2** | **Ambiguous spirit-form register** — hidden base mesh + Skeletal Mesh DI mist emitter + ghost material, in the night lighting rig | "Luminescent mist-cloud, roughly humanoid" reads at the canonical register; translucency-vs-additive sorting against the sky | CHEAP (0.5 session; gated on P0.1 DDC warm) | The scene's central figure fails its Q5 art direction with no early signal |
| **S3** | **Coalescence VFX** — particles converge to a target skeletal-mesh surface (use Crusader as TARGET mesh — internal test only, not the shipped avatar, honoring the no-Crusader constraint's player-facing intent) | The materialization beat's core visual mechanism | MODERATE (1 session; gated on P0.1) | The confirm-time payoff — the game's namesake moment — is unproven until WS3.2 is mid-flight |
| **S4** | **Ambiguous→defined handoff** — Niagara extinguish + dissolve-in mesh reveal, no visible pop, driven by one scalar timeline parameter | The staged-register transformation architecture (§ 3.1) holds; gives WS3.2 its keyframing surface | MODERATE (0.5–1 session; composes with S2+S3) | WS3.2 discovers the transform-track-only assumption is wrong mid-commission |
| **S5** | **Night-exterior lighting register** — hybrid rig (§ 3.4) vs pure-emissive comparison on the knoll; exposure lock; figure readability | The mythic-weight judgment is judged against deliberate light | CHEAP (0.5 session; can fold into Phase 1 P1.1) | #5 judgment fails for lighting reasons misattributed to assets |
| **S6** | **Meshy image-to-3D generic-human pipeline** — image-gen (T-pose, empty hands) → image-to-3D → web-app rig → UE import | The ONLY unproven leg of the avatar pipeline (text-to-3D and Crusader-GLB legs are proven; image-to-3D+rig end-to-end is not) | CHEAP (~0.5 session + a few Meshy credits + one manual rig step) | MVP avatar slips on a pipeline surprise that $2 of credits would have caught |
| **S7** (optional) | **VDB nebula in-scene** — Heterogeneous Volume placement + perf beyond the sphere | Production nebula path cost | CHEAP (0.5 session) | None for MVP (HDRI suffices); informs WS2 fidelity budget |

**Priority order: S6 + S5 + S1 (Phase-1-critical, all cheap) → S2 → S3 → S4** (transformation chain, gated on P0.1). The S2–S4 chain is where the single biggest risk lives; everything else is schedule-risk, not feeling-risk.

**Non-spike risks register:** (R1) Meshy web-app manual rig step is unautomatable today — corpus-scale form library needs a pipeline answer later (out of scope; flagged). (R2) WS1 critical path runs through Mac-side Path A scheduling — PC-seam cannot self-unblock (already tracked at WS3.1 wave-close). (R3) Cold-DDC windowed launches stall from SSH (documented; P0.1 retires it). (R4) The 6-group (cosmograph-pivot § 10.3) vs 7-anchor (creation-moment § 12.3) cluster-region structure is unreconciled pending Pattern B — sky spatial layout work must scaffold one; I scaffold **7 per § 12.3** (later canon) and flag it (§ 7). (R5) Audio/music is human-composed per D7 and entirely unscoped — the mythic register leans hard on score; flag for Matt's planning, not for this seam.

---

## 6. Cross-cutting data contracts the scene depends on

Per commission § 6 this list feeds the Mac-side generation↔sim↔UE-emit forward-architecture effort. Status legend: ✅ exists / 🟡 exists-but-not-yet-on-PC / ❌ does not exist.

| # | Contract | Status | Notes |
|---|---|---|---|
| 6.1 | `kit_star_sign_assignments.json` (schema **v1.1**, injective per Branch A) — loadout `public/kit-space/` | 🟡 | v1.0 shipped; v1.1 spec authored (gandalf 2026-06-10) + implementer script landed (`rocket/scripts/kit_to_star_sign_injective_assignment.py`); confirm v1.1 emission + PC availability via loadout clone. Consumer: DT_KitStarSign |
| 6.2 | `faction_assignments.json` (active kit list, 37 kits) | ✅ | Kit-list source-of-truth per v1.1 spec § 2.1. PC availability gated on loadout clone (Path A) |
| 6.3 | Per-kit JSON records (`kit-space/kits/<kit_id>.json`) — identity, element, T4, substrate_trace, skills | ✅ | Feeds DT_Kit; identity fields fill § 12.9 narration template blanks; element_primary feeds VFX tint via the criterion-3.4-validated binding path |
| 6.4 | Zodiac substrate corpus (`corpus.yaml`, N=423, 26 traditions; `cultural_sensitivity.flag_level`) | ✅ | Feeds DT_StarSign; the star-sign set the sky renders. Meta-repo-resident — already on PC |
| 6.5 | Substrate-registry sidecar (20 Layer-0 families) | 🟡 | Spec authored + rocket emit closed Mac-side (commit `02c2b0c`); **engine push + PC clone pending (Path A)**. Feeds DT_PrimitiveFamily → sky cluster regions |
| 6.6 | Experiential-axes sidecar (7 axes; 1 PROPOSED-PLAYTEST-PENDING) | 🟡 | gamora emit closed (`84bed90`); same Path A gate. Feeds DT_ExperientialAxis → Tier-1 anchors 4–7 |
| 6.7 | **Cosmograph spatial-layout contract** — per-star-sign position on the celestial sphere (unit-vector or lat/long) + cluster-region assignment (7 regions per § 12.3) + per-kit constellation figure geometry (member stars + edges) | ❌ | **Does not exist anywhere.** /forge holds a 2D web layout; the spike used synthetic positions; canon defers spatial layout (§ 12.13) but the UE scene cannot render a substrate-truthful sky without it. Recommendation (cross-cutting → consultation note filed to Mac-gandalf, companion artifact): **engine emits placement; UE renders** — substrate-led at the rendering layer demands positions derive from data, not from UE-side aesthetics. This is the load-bearing missing contract for Phase 2 |
| 6.8 | **Kit-form asset-resolution contract** — kit_id → final-form mesh asset reference (the manifested avatar the spirit becomes) | ❌ | Lookup-not-generation requires pre-built per-kit assets and a registry mapping. Vertical slice: hand-built for the 3 anchor kits. Production: needs an asset-pipeline sidecar (offline Meshy pipeline output manifest). Flag for forward-architecture |
| 6.9 | **Spirit-guide narration template registry** — § 12.9 templated voice lines with named blanks (anchor, kit identity, output primitives) | ❌ | Templates exist as canon prose, not as a data contract. D7-compliant by construction (human-authored templates; narrow blanks filled from 6.3 fields). Small, but the WS3.3 voice sections + cascade narration both consume it — worth a one-page schema |
| 6.10 | Earth-avatar reference image + asset (MVP: one generic human) | ❌ (by design) | Produced by the S6/P1.2 pipeline, not by the engine. Listed for completeness — NOT an engine emit |

**Contracts NOT needed for this scene** (scope guard, named to prevent drift): ability-spec JSON (combat — criterion 3.4's domain), PCG room-layout (criterion 3.5 — deferred), gear/loot schemas.

---

## 7. Scaffold register (Discipline #40 — every assumed/placeholder value, auditable)

| # | Scaffold | Value assumed here | Locked by |
|---|---|---|---|
| 1 | Sphere radius | Order-of-10⁴ UU class (far enough for sky parallax read, near enough for "reachable" feel per § 2.6) — number deliberately NOT committed | S1 empirical + art direction |
| 2 | Star positions (Phase 1) | Synthetic spherical-Fibonacci projection of spike-lineage cluster data — **flagged placeholder, never faked-as-substrate** | Contract 6.7 + Phase 2 |
| 3 | Cluster-region count | **7** per § 12.3 canonical anchor list (vs 6-group § 10.3 scaffold) | Pattern B reconciliation (R4) |
| 4 | Star-distribution algorithm | Spherical Fibonacci (vs Poisson-disk) | § 5.4 trigger of creation-moment doc (WS2 perf + visual evidence) |
| 5 | Rune-in-MVP | ONE placeholder rune included (my recommendation at framing-brief § 4 decision-point) | Matt Pattern-B scope-lock |
| 6 | Camera model (MVP + cinematic) | Authored framing, gently rotatable look-up; no free-look | Matt Pattern-B scope-lock |
| 7 | Spirit-form base mesh | Generic hidden humanoid (any clean biped; UE5 Mannequin acceptable as hidden emitter source) | S2 + Q5 art direction |
| 8 | Transformation architecture | Staged registers (not true morph) | S4 empirical |
| 9 | Vertical-slice kit set | The 3 hand-curated anchor kits (Duskweaver / Cannonade Cleric / Stonefist) | Matt confirmation |
| 10 | Lighting rig | Hybrid moonlight + skylight + diegetic spirit-glow; manual exposure | S5 + Matt #5 judgment |
| 11 | Nebula (MVP) | HDRI/static backdrop | S7 optional → WS2 |
| 12 | Voice (WS3.3) | Templated TTS placeholder or silent caption (WARN-D inheritance) | Canonical voice-character lock § 12.13 |
| 13 | FPS budget full-stack | 60 FPS PC target assumed holdable with LOD headroom (sprite-only evidence + ~30% GPU margin observed) | S1 full-stack measurement |
| 14 | S3 coalescence target mesh | Crusader as internal test target only (not player-facing) | Matt — flag if even internal use is unwanted |
| 15 | "Knoll" environment register | Pastoral-mundane Earth (per § 1.2 delta #1 — NOT new-world-fantastical) | Mac-gandalf confirmation of delta reading |

---

## 8. Sign-off

**Authored:** radagast 2026-06-10, per gandalf Fable-5 commission (Matt-authorized), first radagast file artifact.
**Scope honored:** this scene + immediate near-neighbors only; interaction layers, combat, loadout, broader Earth-Self loop all explicitly untouched.
**Disciplines:** D7 verified at every text/voice surface (§ 2.3, § 3.5, 6.9); substrate-led at rendering layer (no UE pattern pre-imposed that canon hasn't chosen — Mutable pushback § 3.1, star-positions-from-data § 6.7); recognition-validate-commit (Phase-1 #5 gate before interaction commissioning); Discipline #40 (§ 7 register); #21/#22 (no sleep framing; workstream-relative sequencing only).
**Cross-host:** consultation note to Mac-gandalf filed as companion artifact (cosmograph spatial-layout emit contract — cross-cutting per drift-discipline § 6.2).
**Empirical-evidence criteria gating re-engagement:** Matt #5 mythic-weight judgment on the assembled Phase-1 scene; S1–S6 spike findings; Path A completion for Phase 2+.

**End of consult.**
