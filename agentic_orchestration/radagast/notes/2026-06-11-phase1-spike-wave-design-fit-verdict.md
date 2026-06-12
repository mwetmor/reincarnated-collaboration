# Phase-1 Spike Wave — Design-Fit Verdict (S6 + S5 + S1)

> **STATUS:** CURRENT (PC-seam design-fit verdict — radagast Pattern A-deep; reviews mantis Phase-1 spike-wave outputs against the radagast feasibility consult + gandalf design-fit ratification + the now-canonical Avatar/Hall-of-Heroes framing)
>
> **Top-line: all three spikes clear design-fit.** S6 PASS (exceeds spec — R1 retired). S5 PASS-with-notes (authoring-complete, one fairness-gate caveat). S1 PASS-with-notes (architecturally sound; the deviation that needs a ruling — 6 vs 7 cluster caps — is **acceptable**; reasoning below). **No CONCERN, no BLOCK-equivalent.** The single thing that gates the #5 mythic-weight judgment is now environmental (the DXGI render-surface gate), not design.

**Date:** 2026-06-11
**Author:** radagast (PC-side design steward)
**Reviews:**
- `agentic_orchestration/mantis/notes/2026-06-11-s6-meshy-image-to-3d-avatar-spike.md` (incl. § 8 import leg)
- `agentic_orchestration/mantis/notes/2026-06-11-s5-night-lighting-register-spike.md`
- `agentic_orchestration/mantis/notes/2026-06-11-s1-sky-from-ground-celestial-sphere-spike.md`
**Yardsticks:**
- `agentic_orchestration/radagast/notes/2026-06-10-manifestation-moment-ue-feasibility-consult.md` (§ 3 architecture, § 5 spike specs, § 7 scaffold register)
- `agentic_orchestration/gandalf/notes/2026-06-10-radagast-manifestation-design-fit-review-and-cosmograph-contract-response.md` (S5 co-critical re-weight § 2.4; Avatar framing § 4)
- `canonical/story/2026-06-11-avatar-projection-and-hall-of-heroes-framing.md` (Matt-confirmed; § 4 build constraints — the authoritative operator-framing yardstick, landed via this session's pull)
**Dispatched by:** david-h (Matt-authorized 2026-06-11)
**Gate disposition:** design-fit verdict, not a code gate. Sam owns the Gate-2 technical/process verdict in parallel; the two compose.

---

## 0. Operator-framing compliance — the cross-cutting yardstick, checked FIRST

The HEADS-UP david-h flagged is now hardened canon: `2026-06-11-avatar-projection-and-hall-of-heroes-framing.md` § 4 makes two build constraints binding — (4.1) manifestation is a **recurring** transition (the creation scene is the *ceremonial maximal case* of a reusable jump-in, NOT a one-shot cinematic); (4.2) the knoll is a **returnable hub that starts sparse**, NOT a disposable creation-flow level.

**All three spikes COMPLY, and visibly so — mantis read the constraint correctly and built to it.** Evidence, per spike:

- **S5** built `LV_ManifestationKnoll` as a **reusable persistent-realm level**, explicitly "NOT baked into `LS_Materialization_Cinematic` or any one-shot sequence" (S5 § 1). This is exactly § 4.2's "the knoll scene IS the embryonic hub; do not architect it as a disposable creation-flow level." Direct compliance.
- **S1** placed the sky **into that same reusable level**, with the twirl as a **container-transform** (`CelestialSphere_Sky` actor rotation), never baked into a sequence. The sky is a hub property, not a cinematic prop. Compliant.
- **S6** imported the avatar as a **persistent reusable `SK_EarthAvatar`** under a stable `/Game/Characters/EarthAvatar/` path, with the operator-model reusability called out in the findings (S6 § 3.4, § 8.1) — "avoid burying it inside a one-shot cinematic folder." Compliant, and the path choice is correct: a character asset under `/Game/Characters/` is referenceable across every projection, which is precisely the recurring-transition requirement.

**Ruling: operator-framing compliance — PASS across all three.** Nothing in the outputs hardens a one-shot-cinematic assumption. The reusable-level + persistent-character-asset + container-transform-twirl choices are the *correct* primitives for § 4.1's "core transform reusable as the routine jump-in at reduced ceremony." This is the single most important thing to get right at spike stage and mantis got it right without it being spelled out in the spike spec — it came through the dispatch HEADS-UP and was honored. Credit where due.

---

## 1. Per-spike verdicts

### 1.1 S6 — Meshy image-to-3D avatar pipeline — **PASS (exceeds spec)**

S6 was specced (consult § 5) to prove "the ONLY unproven leg of the avatar pipeline" — image-to-3D + rig end-to-end. It proved that AND retired a standing risk I had carried as unmitigable. Specifics:

- **Design-fit against consult § 2.1(a) + § 3.1 row 1:** exact match. Image-gen (T-pose/A-pose, empty hands, no fantasy) → image-to-3D → rig → UE import as a clean Hips-rooted 24-joint Mixamo-convention skeleton — the convention the proven Crusader path consumes. The reference-image verdict (S6 § 1.1: ordinary contemporary human, A-pose, empty hands, zero fantasy) **satisfies the canonical "mundane human vs the becoming" contrast** (creation-moment § 2.1; my consult § 1.1). This is the visual story of the scene and the asset reads it correctly.
- **R1 RETIRED — the headline.** My consult § 5 non-spike risk R1 said "Meshy web-app manual rig step is unautomatable today." That was true on the 2026-06-06 empirical anchor (text-to-3D API returned zero skeleton). The current rigging API (`POST /openapi/v1/rigging`, 5 cr) ran chained with **zero manual steps** and mantis proved the rig by parsing the glTF JSON chunk (24 joints, Hips root) — not assuming it (Discipline #11 empirical, done right). **R1 disposition accepted: RETIRE for the clean-forward-facing-humanoid class; keep it flagged ONLY for corpus-scale non-humanoid / occluded-limb kit-forms.** The implications for the 6.8 contract economics are large enough to route to Mac-gandalf — § 3 below.
- **Cost discipline:** 44 credits / ~$2.20 for the full chain. The consult predicted "a few Meshy credits." On-spec.
- **Idle gap — correctly classed as non-blocking.** Meshy ships walking/running but no idle. mantis classed this as a downstream retarget step (Mixamo or UE IKRig onto the standard skeleton), not a pipeline gap. **Concur — and the design read matters here:** for the #5 judgment, a static rest pose (S6 § 2 Path C) reads as "standing on the knoll" and is acceptable for first assembly, but a **calm breathing idle is first-class for the mythic-weight judgment**, not polish. A perfectly-still figure reads as a mannequin / paused game; subtle breathing reads as a *person on the threshold*. This is the same logic as my § 2.4 lighting-fairness note applied to animation. Route to P1.5 (§ 6) as a "do the Mixamo idle retarget before the #5 judgment if the render session has the headroom; Path C if it doesn't" — not a blocker either way, but named.

**S6 verdict: PASS, exceeds spec. No fixes required.** One forward item (GLB bridge handler, § 4) and one routing (6.8 economics to Mac-gandalf, § 3).

### 1.2 S5 — night-exterior lighting register — **PASS-with-notes (authoring-complete; #5-fairness caveat)**

S5 built the hybrid rig I specced (consult § 3.4) faithfully and added the comparison arm gandalf's re-weight called for.

- **Design-fit against consult § 3.4:** exact. `RigA_Moonlight` (low cool directional key) + `RigA_Skylight` (ambient sky fill) + `RigA_SpiritGlow` (diegetic point light where the becoming stands) + **manual exposure lock** (`AEM_Manual`, the load-bearing trap-fix my § 2.4 flagged — auto-exposure fighting the bright-sky/dark-ground composition). All four pillars landed. The diegetic-glow-motivates-readability logic (the becoming lights the scene in-fiction) is preserved.
- **gandalf's S5 co-critical re-weight (§ 2.4 of his review) — honored structurally.** He raised S5 from "cheap, can fold into P1.1" to "the #5 gate is VOID without deliberate lighting." mantis built **Rig B** (pure-emissive comparison, hidden by default, toggleable) so the A/B is renderable in one session. This is the right instrument for the co-critical judgment: it lets Matt see *why* the hybrid rig is the recommendation rather than asserting it. Good.
- **The caveat — and it is a design caveat, not a fix:** S5 is **authoring-complete but render-unevidenced.** Every lighting value in the scaffold register (moonlight 0.6 lux, skylight 0.4, glow 2200, exposure brightness 0.03 / bias −2.0) is a *deliberate placeholder*, not a *judged* value. The fairness criterion my own consult set (§ 2.4: "for #5 to be fair, the lighting pass must be at least 'deliberate'") is **half-met**: the lighting is deliberate in *intent and structure*, but the actual EV/intensity tuning happens only in the render session. **This does not threaten the #5 judgment's validity — it gates it.** The render session IS the lighting pass; #5 cannot fire before it (more in § 6).

**S5 verdict: PASS-with-notes.** Note 1: lighting values are deliberate-as-structure, render-tuned-as-final — the #5 judgment must follow the tuning, not the authoring. Note 2: see § 6 for what the render session must cover.

### 1.3 S1 — sky-from-ground celestial sphere — **PASS-with-notes (architecture sound; the 6-vs-7 deviation RULED acceptable)**

S1 is the partial-pass, and it is partial in exactly the honest way the spike was meant to be — the architecture proved; the render-evidence and array-binding are gated.

- **Design-fit against consult § 3.2:** strong. Logical sphere (positions at radius R, NOT a physical inverted mesh — my § 3.2 rejected-alternative is respected), 1,000 stars on the interior surface via spherical-Fibonacci, twirl as **container transform** (rotate the starfield, never the camera — my § 2.2 / § 3.2 requirement, honored), nebula as static backdrop beyond R (MVP path per my § 3.2), `NS_CelestialSphere` duplicated from the proven `NS_CosmographPointCloud` GREEN lineage. All the load-bearing architecture choices match the consult. The `M_StarSprite_Emissive` (Unlit + Additive, per-star vertex color) is the right material register for "stars," and `M_ConstellationLine_Emissive` stubs the ribbon-edge layer.
- **THE DEVIATION TO RULE ON — 6 cluster caps, not 7.** mantis built 6 element-cluster caps (S1 § 1.1, scaffold #3). My consult § 7 scaffold-register row #3 locked the scaffold at **7** per creation-moment § 12.3. So this is a deviation from my register. **Ruling: ACCEPTABLE — built correctly, flagged correctly, and gandalf's contract design makes the count a non-issue.** Reasoning:
  1. mantis did NOT silently deviate. S1 scaffold #3 explicitly states "tier-2 data is 6-cluster, so this spike is 6" and cross-references "NB consult R4 flags 6-group vs 7-anchor unreconciled." The deviation is *substrate-honest*: the tier-2 spike cluster data that exists today IS 6-cluster; projecting it as 7 would have been **faking a region that has no data behind it** — a Discipline #41 (substrate-led) violation worse than the deviation. mantis chose the substrate-truthful count over my scaffold number, with the flag. That is the correct instinct.
  2. **The count is provisional on BOTH sides.** My #7 was the later-canon scaffold pending the R4 Pattern-B reconciliation (6-group cosmograph-pivot § 10.3 vs 7-anchor creation-moment § 12.3). gandalf's review § 2.5 confirmed "7 is the right *scaffold*" but explicitly held the **reconciliation as his to resolve at the design layer**, and § 3.4 of his contract response makes `cluster_region_id` an **opaque identifier, NOT a 1-of-N enum** — the contract is *count-agnostic by construction*. So neither the contract nor the sky build is hostage to 6-vs-7; the re-projection happens when contract 6.7 + the 7-anchor canon land (S1 § 5 step 4 already registers this).
  3. **Player consequence of the deviation at this stage: zero.** This is a render-feeling spike on placeholder positions that will be *entirely re-projected* from substrate-truthful kit→constellation placement once contract 6.7 exists. The cluster count of the throwaway scaffold has no bearing on whether the sky reads as a sky. The thing S1 is actually testing (sphere-interior read, TSR-under-twirl, sprite sizing at sky distance) is count-independent.
  - **Disposition:** deviation accepted; scaffold-register row #3 carries a reconciliation note (6-built / 7-canonical-scaffold / count-agnostic-contract / re-project on 6.7) rather than a correction. No fix to mantis. The 6-vs-7 reconciliation remains gandalf's design-layer call (his § 2.5) — NOT a PC-seam decision, NOT mine to resolve. Flagged in § 3 routing for visibility, not for action.
- **The two gates are honest and correctly classed.** Gate A (position-array binding) is genuinely BP/windowed — the bridge `set_niagara_parameter` has no array support and the duplicated emitter exposes 0 user params (the Session-3 spike set positions *inside* the emitter, not via exposed array user-params as the design doc had projected). This is a real tooling finding, surfaced not papered. Gate B (render measurements) is the same DXGI gate as S5. **ZERO render evidence** is the honest state, and it is the right honest state — mantis did not fabricate a screenshot or claim a TSR result it could not measure.

**S1 verdict: PASS-with-notes.** Note 1: 6-vs-7 deviation ruled acceptable (substrate-honest, count-agnostic contract, throwaway positions). Note 2: the two gates are real and correctly classed; the sky is architecturally proved but **experientially unproved** — the falsifiable read ("sky full of stars WITH DEPTH, not a particle effect," S1 § 2 Gate B) is exactly the thing only the render session can answer.

---

## 2. The DXGI gate — what it does to the Phase-1 / P0.1 dependency spine

This is the most consequential finding of the wave and it reshapes my consult's Phase-0 framing. **Ruling: my P0.1 framing is SUPERSEDED and must be re-stated.**

- **My consult § 4 P0.1 said:** "Matt warms shader DDC (one-time interactive editor open; unblocks all windowed Niagara work)." I framed the windowed blocker as **cold DDC** (inherited from the 2026-06-10 windowed-verification note). The wave proved that framing **wrong** (S5 § 2, AGENT_STATE ENVIRONMENT LEARNING): the DDC is warm enough that the editor reaches PostEngineInit and the bridge binds in ~22s. The actual windowed blocker is **`DXGI_ERROR_NOT_CURRENTLY_AVAILABLE` at viewport creation** — the SSH/WSL session has no GPU-attached interactive Windows desktop, so DXGI cannot acquire a swap-chain for the editor window.
- **What this changes about the dependency spine:**
  1. **The gate is no longer "Matt does a one-time DDC warm and then mantis can do windowed work autonomously."** It is "**any render-surface work requires Matt at the PC console (or an RDP/console-attached session) — full stop, recurring.**" DDC-warming was a one-time unblock; DXGI is a *standing constraint on the SSH/WSL invocation model itself.* That is a meaningfully different shape: the render-surface work cannot be delegated to an autonomous SSH-invoked mantis session ever, under the current connection model.
  2. **Headless authoring is UNAFFECTED.** Everything proved this wave (level, lights, materials, Niagara system creation, avatar import, persistence) ran clean headless `-nullrhi -nosound`. So the *authoring* half of every spike is autonomous; only the *render/measure/judge* half needs Matt-at-console. This is actually a clean seam — it cleaves the work along exactly the line where Matt's #5 judgment lives anyway.
  3. **The S2→S3→S4 transformation chain gating is REVISED.** My consult gated S2/S3/S4 on "P0.1 DDC warm (windowed Niagara)." Re-stated: S2/S3/S4 **authoring** (Niagara system + emitter + material creation via `create_niagara_system_from_spec`) can proceed headless and autonomous; their **visual validation** (does the mist read as "luminescent becoming"? does coalescence read? does the handoff hide the pop?) is render-surface work → Matt-at-console. The chain is not blocked from *starting*; it is blocked from *being judged*. Same shape as S1/S5. **The biggest-risk surface (transformation continuum) can be built blind and must be judged sighted** — which raises the value of getting Matt's first console session to also smoke-test the S2 register early, so the highest-risk subsystem gets its first visual signal soonest.

- **Design-stewardship read:** this is not a crisis — it is a clarification that converts a fuzzy "warm the DDC sometime" prerequisite into a sharp, recurring, well-understood gate ("render judgment = Matt at console"). The whole Phase-1 architecture already routes the only irreducible-human-judgment (#5 mythic-weight) through Matt. The DXGI finding just means *all* render evidence batches at that same console session. That is operationally cleaner, not worse.

---

## 3. What the render session must cover — to maximally unblock

Matt's single desktop/console session (or RDP) should batch **every render-gated item across all three spikes** so one console sitting clears the entire Phase-1 visual-evidence backlog. Sequenced by leverage:

1. **S1 Gate A first (BP array-binding) — it is a prerequisite for S1 Gate B being meaningful.** Until `BP_CelestialSphere` loads the R8000 JSON and binds the position arrays, the sky renders the *original spike's ±67 UU cloud*, not the sphere (S1 § 2 Gate A). Measuring TSR/FPS/sprite-size on the wrong geometry is wasted. So: expose `StarPositions`/`StarColors` array user-params on the emitter, author the BP (the proven `BP_CosmographTest` pattern), bind. This is windowed Niagara-stack work — needs the console session anyway.
2. **S1 Gate B (the falsifiable sky read):** TSR stability under sphere twirl (the stress case criterion 3.6's idle-anim test never covered — small bright additive sprites near the horizon during rotation); full-stack FPS vs 60 (stars + ribbon edges + emissive material + nebula together; criterion 3.7 only measured sprite-only); **sprite angular-size + R tuning** — the load-bearing read is "sky WITH DEPTH, not a particle effect." Report the landed R back to scaffold #2 (8,000 is the low-end starting knob; `gen-sphere-stars.js` regenerates at a new R in ~1s).
3. **S5 Rig A vs Rig B judgment:** toggle `RigB_SpiritGlowOnly` on / Rig A off, screenshot both from `Cam_GroundLookUp`, judge figure readability + mythic register, fine-tune `AutoExposureBias` once the EV reads at night. **This is the lighting pass that makes the #5 judgment fair** (gandalf's co-critical re-weight) — it must happen before #5, not after.
4. **S6 idle (if headroom):** Mixamo "Idle"/"Breathing Idle" retarget onto `SK_EarthAvatar_Skeleton` before the figure is judged — a still mannequin reads paused; a breathing figure reads present. Path C (rest pose) if the session runs short. Named as "do-if-headroom," not a gate.
5. **HIGH-VALUE ADD — smoke the S2 register early if the session has any room left.** The transformation continuum (S2→S3→S4) is the single biggest *feeling*-risk in the whole scene (my consult § 5; gandalf endorsed). It has zero in-project anchor. Getting even a rough first look at "does the ambiguous spirit-form mist read as a luminous becoming under the S5 night rig" in this *same* console session would de-risk the highest-stakes subsystem soonest. Not required for #5 (the spirit form is placeholder `RigA_SpiritGlow` at P1.5), but the highest-information optional thing Matt could glance at while the editor is open.

**The four-phase legibility note for whoever scopes WS3.2 later (gandalf § 2.4):** the materialization's four phases (concretization → racial → elemental → weapon) must read as **four distinct heartbeats, not a continuous blur** — "now the body; now the blood; now the element; now the weapon." A smooth crossfade reads as a loading bar. Not a Phase-1 item; flagged here so it is on record before the transformation chain is keyframed.

---

## 4. FBX-not-GLB substitution + the missing GLB bridge handler

**Ruling: FBX substitution ACCEPTABLE. Confirmed.** The dispatch named "GLB via Interchange"; mantis imported the **FBX twin** because the UE_MCP_Bridge import handlers are all `UFbxFactory`-based with no glTF/Interchange factory exposed (S6 § 8.2). Three reasons this is fine, not a compromise:

1. **Same asset.** `earth_avatar_rigged.fbx` and `.glb` are the same Meshy-rigged output — identical 24-joint Hips-rooted Mixamo skeleton (S6 § 1.3 parsed the GLB chunk; § 8.3 verified the FBX import gives boneCount 24 + Hips root — *they match exactly*). Nothing about the player-facing result differs.
2. **FBX is the PROVEN path.** The criterion-3.2 Crusader import that established the clean-skeleton pipeline was itself an FBX import (`SK_Crusader_Idle`). The dispatch's "GLB via Interchange" was format-aspiration; the deterministic, already-validated bridge route is FBX. mantis took the proven path and flagged the aspiration honestly rather than forcing an unvalidated Interchange route headless.
3. **D7 / substrate-led intact.** The asset is still image→Meshy substrate-grounded; the format of the import twin is a pipeline-mechanics detail, not a provenance question.

**Forward item (NOT an MVP blocker):** a true literal-GLB/Interchange import — if ever wanted for provenance-purity (importing the exact GLB artifact rather than its FBX twin) — needs either (a) a new bridge handler that runs `ImportAssetTasks` with no forced factory (letting Interchange auto-select the glTF pipeline), or (b) a windowed/Python-console Interchange import. **Route to mantis as a backlog forward-item, not a fix.** My design-stewardship view: this is low-priority — the FBX twin is functionally and provenance-equivalent. It only matters if a future asset arrives GLB-only with no FBX twin, which the current Meshy pipeline never produces (it emits both). Park it; don't build it speculatively.

---

## 5. Durability gap — `reincarnated-unreal` is NOT git-tracked

mantis flagged this in S6 § 4, § 8.6, and AGENT_STATE: the UE project has no `.git` anywhere under the tree; all `.uasset` artifacts (the `SK_EarthAvatar` import, `LV_ManifestationKnoll`, `NS_CelestialSphere`, materials, the spike driver scripts under the UE tree) are **disk-only, no version control.**

**Design-stewardship view (recommendation only — the decision routes to Matt / david-h, this is NOT my call):**

- **This is a real durability gap and it is growing.** As of this wave there is now non-trivial *authored UE state* on disk with no history, no remote, no rollback: a reusable hub level, an imported character asset, a Niagara sky system, lighting rigs, materials, and re-runnable driver scripts. Until this wave the UE project was mostly bridge-plumbing + a sequencer stub; now it holds Phase-1 scene-assembly substrate. The cost of a disk loss just went from "annoying" to "re-run several spikes."
- **Two mitigations exist and they have different weights.** (a) The **driver scripts are the cheap insurance** — `s6_pipeline.py`, `gen-sphere-stars.js`, `s5-night-lighting.js`, `s1-celestial-sphere.js`, `s6-import-earth-avatar.js` are all re-runnable and *most* of the authored state is reconstructable from them (this is genuinely good discipline from mantis — the scene is largely code-reproducible). (b) But re-runnable scripts are NOT a substitute for version control of the *binary `.uasset` outputs* + the imported textures + the Meshy raw assets (44 credits of Meshy spend lives in `RawAssets/EarthAvatar_S6/` with no backup).
- **My recommendation:** UE projects are git-trackable with **Git LFS** for the binary `.uasset`/texture/`.umap` blobs (industry-standard for UE-on-git; the alternative is Perforce, which is heavier than this project needs at solo-dev scale). The asymmetry worth naming for Matt: *every other seam in this ecosystem is version-controlled and the UE seam — which now holds the entire player-facing manifestation scene — is not.* That is the kind of single-host durability gap that is invisible until a disk event makes it catastrophic. I would not let it grow another wave without a decision.
- **Scope honesty:** repo-setup is outside PC-seam *design* authority — this is a david-h/Matt infrastructure decision. I am recommending, not deciding. Routing it in § 7.

---

## 6. What P1.5 assembly still needs + #5-judgment-validity check

**P1.5 (assemble the static scene + Matt #5 mythic-weight judgment) still needs, in order:**

1. The render-console session (§ 3) — without it, P1.5 cannot be *seen*, only assembled.
2. **S1 Gate A bound** — so the sky is the sphere, not the spike cloud (else #5 judges placeholder geometry).
3. **S5 lighting tuned** (Rig A/B judged, exposure-bias fine-tuned) — so #5 judges deliberate light, not deliberate-as-structure-only light (gandalf's co-critical gate).
4. **S6 avatar placed** in `LV_ManifestationKnoll` replacing `FigureStandIn`, ideally with the Mixamo idle (§ 1.1) — so #5 judges the real mundane-human-vs-becoming contrast, not a test biped.
5. **S2 spirit form** — at minimum the placeholder `RigA_SpiritGlow` stands in for the becoming's *position/light*; the actual S2 mist register is a later spike but the glow placeholder is enough for the *static-scene* #5 read (the spirit form's full register is what S2 proves, and S2 is gated after S6/S5/S1 per my priority order).

**#5-judgment-validity check (my own "fairness" criterion from consult § 2.4) — does anything in the outputs threaten it?**

- **Nothing in the outputs threatens validity; one thing GATES it (correctly).** The fairness criterion is: "a placeholder mesh under intentional lighting reads mythic; a good mesh under default lighting never will." The outputs *honor* this — they built deliberate lighting structure and a deliberate avatar. The gate is that the lighting must be **render-tuned** (not just authored) before #5 fires, and the avatar should ideally **breathe** (idle) rather than stand frozen. Both are render-session items, both already named. **So #5 is not at risk of being *unfairly negative* — the wave did its job of making the scene judgeable-when-lit.** The one residual risk to flag: if the render session is rushed and #5 is judged on *un-tuned* exposure (the 0.03/−2.0 scaffold values, never validated against an actual rendered frame), a real lighting bug could be misattributed to the *scene concept* failing — which is exactly the failure my § 2.4 warned against. **Mitigation: #5 must follow exposure-tuning in the same session, never precede it.** This is the one sequencing discipline that protects the judgment's validity.

---

## 7. Routing

### To Mac-gandalf (cross-cutting — consultation note; drift-discipline § 6.2)
- **6.8 kit-form asset-resolution contract economics shifted by R1 retirement.** The S6 finding that the *full* text-to-image → image-to-3d → **rigging** chain is now API-scriptable (44 cr/avatar, `s6_pipeline.py` is the seed) materially improves the corpus-scale form-library outlook I flagged as a manual-rig bottleneck in consult § 2.1(c) + contract 6.8. **BUT the retirement is bounded** — the Meshy rigging API's pose-estimation works *because* the input is clean/forward-facing/textured/humanoid; non-humanoid or occluded-limb kit-forms (a quadruped, a winged form, a form with a weapon fused to the silhouette) may still hit the manual path or fail pose-estimation entirely. The contract-6.8 forward-architecture spec should now assume **"humanoid kit-forms are fully API-pipelineable; non-humanoid forms need separate validation"** rather than the blanket "manual rig step is the bottleneck" I originally wrote. This is gandalf's contract-design territory (he owns 6.8 per his review § 3.8) — routing the economics update, not specifying it.
- **6-vs-7 cluster reconciliation (R4) — visibility only, no action requested.** S1 built 6 (substrate-truthful to tier-2 data); my scaffold said 7; gandalf's contract made it count-agnostic. The reconciliation remains gandalf's design-layer call (his review § 2.5). Flagging that the spike landed on 6 so the reconciliation has the empirical datapoint.

### To Matt (decisions)
- **Render-console session** (§ 3) — the recurring DXGI gate means render evidence + the #5 judgment require Matt at the PC console / RDP. This is now a standing constraint on the SSH-invocation model, not a one-time DDC warm. Batch all of § 3 into one sitting.
- **UE-project version-control decision** (§ 5) — recommendation: git + Git LFS for the now-substantial authored UE state. Routes to Matt/david-h as infrastructure; I recommend not letting it grow another wave undecided.

### To mantis (forward items — NOT fixes; no rework on the spike outputs)
- GLB/Interchange bridge handler (§ 4) — backlog forward-item, low priority; FBX twin is functionally + provenance-equivalent. Build only if a GLB-only asset ever arrives without an FBX twin (current Meshy pipeline never produces that).
- S1 re-projection (§ 1.3) — when contract 6.7 + 7-anchor canon land, re-project the sphere from substrate-truthful kit→constellation placement (retires scaffolds #1 + #3). Already on mantis's TODO.

### To david-h (sequencing)
- The render-console session is the Phase-1 critical path now. Everything authorable headless is done; everything remaining is render-gated to that one Matt-at-console sitting. Sequence accordingly.

### To Sam (Gate-2 compose)
- This verdict is the design-fit track; Sam owns the technical/process Gate-2 (FBX substitution, git-tracking, scope-honored). My design-fit verdict and Sam's process verdict compose — no conflict surfaced; the FBX and git findings are flagged in both registers from different angles (Sam: process/durability; me: design-equivalence + stewardship-recommendation).

---

## 8. Discipline citations (load-bearing)

- **#41 substrate-led:** the load-bearing reason the 6-vs-7 deviation is *acceptable* — mantis chose the substrate-truthful count (6, the data that exists) over my scaffold number (7), with the flag. Faking 7 would have been the worse discipline failure. Also: no value faked-as-substrate in any spike's scaffold register.
- **#11 empirical:** S6 proved the rig by parsing the glTF chunk (24 joints, not assumed) and verified the import by bridge introspection (boneCount/material/textures/scale all checked, not claimed). S1/S5 honestly reported ZERO render evidence rather than fabricating it. This is the discipline working.
- **#40 scaffold register:** all three spikes carry complete registers; every placeholder is auditable. The FBX-twin substitution is registered as a scaffold-equivalent (S6 § 8.6).
- **D7 (AI-tell line):** verified clean across the wave — avatar is image→Meshy substrate-grounded (no raw-LLM surface, no Crusader); no text/voice surface touched.
- **recognition-validate-commit:** the #5 mythic-weight judgment remains the empirical gate before interaction-layer commissioning; the DXGI finding routes that judgment through Matt-at-console but does not change the gate's existence or position.
- **#21 / #22:** no sleep framing, no time-of-day projection; all sequencing is workstream-relative (render session, post-6.7, when-contract-lands).

---

## 9. Sign-off

**Verdicts:** S6 PASS (exceeds spec — R1 retired). S5 PASS-with-notes (authoring-complete; #5 must follow exposure-tuning). S1 PASS-with-notes (architecture sound; 6-vs-7 deviation RULED acceptable; render-evidence honestly absent).
**Operator-framing compliance:** PASS across all three — reusable level + persistent character asset + container-transform twirl; nothing hardened into a one-shot cinematic. Mantis honored the canonical § 4 build constraints.
**No CONCERN. No BLOCK-equivalent.** The Phase-1 critical path is now a single Matt-at-console render session (DXGI-gated), which clears the entire visual-evidence backlog and enables the #5 judgment.
**Empirical-evidence criteria gating re-engagement:** the render-console session (S1 Gate A+B, S5 Rig A/B + exposure tune, S6 idle, optional S2 smoke); Matt #5 mythic-weight judgment AFTER exposure-tuning (validity discipline); contract 6.7 landing for the S1 substrate re-projection.
**Cross-host:** 6.8-economics update + 6-vs-7 datapoint routed to Mac-gandalf via consultation (drift-discipline § 6.2).
**Authored:** radagast 2026-06-11, Pattern A-deep design-fit verdict. NOT pushed (david-h wave-close push).

**End of verdict.**

---

## ADDENDUM — 2026-06-11 (Meshy ≠ main-character scope correction)

**Trigger:** Matt scope correction landed after this verdict committed, captured at `agentic_orchestration/gandalf/notes/2026-06-11-asset-pipeline-scope-correction-meshy-vs-modular.md`. The correction narrows a framing this verdict carried in § 1.1 (R1-retirement implications) and § 7 (the Mac-gandalf 6.8-economics routing). **Spike verdicts themselves are UNAFFECTED** (Matt verbatim) — S6 PASS, S5 PASS-with-notes, S1 PASS-with-notes all stand exactly as written. Only the *form-library / 6.8-economics extrapolation* is re-scoped below.

**What changed (Matt verbatim intent via gandalf):** the Meshy image→3D→rig pipeline serves the **bestiary** — enemies, monsters, bosses, maybe an NPC or two — **not** the player-character surface. The main-character pipeline is the already-decided **modular character combo pack** built for character creation. S6's *avatar* was a valid spike subject (it proved the pipeline's legs end-to-end on the clean-humanoid class), but the **shipped player-character surface rides the modular pack, not Meshy.**

**Re-scoping the framings this verdict carried:**

1. **§ 1.1 "R1 RETIRED" — re-scope the win from form-library to BESTIARY corpus.** The retirement is correct and stands — the full text-to-image → image-to-3D → rigging chain is API-scriptable with zero manual steps. But the *value* is **bestiary-corpus economics, not player-form-library economics.** Where § 1.1 read the win as "keep flagged ONLY for corpus-scale non-humanoid kit-forms," re-read it as: ~$2.45/form fully-API-automatable is the **monster/boss/Rift-enemy/seasonal-mob number** — and for *that* corpus it is genuinely excellent (cheap trial-boss gallery, third-faction Rift enemy variety, seasonal mob population). The "kit-form" / player-form-library reading is withdrawn. R1's retirement does not improve player-form economics because player forms never rode Meshy.

2. **§ 7 Mac-gandalf routing — the 6.8 repricing I routed is WITHDRAWN as stated.** My routed framing ("humanoid kit-forms are fully API-pipelineable; non-humanoid forms need separate validation") assumed player kit-forms ride Meshy. They do not. gandalf's "400 survivors × $2.45" 6.8 repricing is withdrawn at the source; player-facing character surfaces ride the modular-pack pipeline and 6.8 economics must be computed against **modular-pack composition**, not Meshy credits. **What I still correctly route to Mac-gandalf:** the bestiary-corpus economics datapoint (Meshy chain is API-clean at ~$2.45/form for the monster/boss/enemy corpus) — that remains a real, useful input for whatever bestiary-scale asset-resolution contract work follows. The non-humanoid validation caveat still applies, but now scoped to the **bestiary** (a quadruped boss, a winged Rift enemy may hit the manual path), not to player kit-forms.

3. **The seasonal-spirit-form boundary is OPEN — do not pre-commit (Matt rules when 6.8 fires).** Which pipeline serves the **seasonal spirit forms** (the forms the player projects into in the Hall of Heroes) is unresolved: humanoid/near-humanoid forms → likely modular pack (character-creation surface); non-humanoid/fantastical forms (slime-class, beast-class isekai staples) → may exceed modular-pack coverage and need Meshy or a hybrid. The hall's emotional weight (each form recognizably the life lived) makes this a **design-significant boundary, not a cost optimization.** This verdict pre-commits neither way; Matt rules at 6.8.

**Unaffected and re-affirmed:** the S6 design-fit verdict (clean-humanoid pipeline proved end-to-end, R1 retired, FBX-twin substitution accepted, D7-clean image→Meshy provenance) stands without qualification. The avatar-as-spike-subject was the right spike. The operator-framing compliance, S5/S1 verdicts, DXGI gate analysis, version-control recommendation, and render-session sequencing (§ 0, 2, 3, 5, 6) are entirely untouched by this correction — they concern scene assembly, not asset-pipeline sourcing.

**Addendum authored:** radagast 2026-06-11, dispatched by david-h. NOT pushed (david-h wave-close push).
