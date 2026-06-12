# S6 — Meshy Image-to-3D Generic-Human Avatar Pipeline Spike

> **STATUS:** CURRENT (mantis spike findings — Manifestation Moment Phase-1 spike wave, Track A)
> **Verdict up front: PROVED, FULLY API-AUTOMATABLE.** All three legs (image-gen → image-to-3D → rig) ran end-to-end via the Meshy OpenAPI with zero manual web-app steps. The reference image meets the design intent (ordinary contemporary human, A-pose, empty hands, zero fantasy). The rigged GLB carries a 24-joint Hips-rooted Mixamo-convention skeleton — the same convention the proven Crusader→UE import path consumes. **Risk R1 (manual web-app rig) is RETIRED for this model class by the rigging API.** One residual gap: Meshy ships walking/running animations but NO idle; the MVP calm-idle need is closed downstream (Mixamo/UE retarget onto the standard skeleton), not in this pipeline.

**Date:** 2026-06-11
**Author:** mantis (UE 5.7 seam, PC-resident)
**Spike:** S6 per `agentic_orchestration/radagast/notes/2026-06-10-manifestation-moment-ue-feasibility-consult.md` § 5 row S6 + non-spike risk R1
**Dispatched by:** david-h (Matt-authorized 2026-06-11)
**Spec:** `agentic_orchestration/gandalf/notes/2026-06-10-ue-manifestation-moment-mvp-framing-brief.md` § 2
**Scope:** pipeline proof ONLY (no customization, no multiple avatars, no scene work). STOPPED before UE import per dispatch (another mantis lane owns the editor this wave).
**Import leg (follow-up, 2026-06-11):** UE import COMPLETE — see § 8. `SK_EarthAvatar` staged at `/Game/Characters/EarthAvatar/`, 24-joint Hips-rooted skeleton + material + textures, persisted + verified. Imported the FBX twin (bridge has no GLB/Interchange handler; FBX is the Crusader-proven path; same rigged asset).

---

## 0. TL;DR per leg

| Leg | Status | Tool | Credits |
|---|---|---|---|
| 1. Image-gen (reference image) | **PROVED** | Meshy text-to-image (`gpt-image-2`, `pose_mode: a-pose`) | 9 |
| 2. Image-to-3D (GLB out) | **PROVED** | Meshy image-to-3d (`input_task_id` chained, `pose_mode: a-pose`) | 30 |
| 3. Rig (skeleton + anim) | **PROVED — API, not manual** | Meshy rigging (`input_task_id` chained) | 5 |
| **Total** | | | **44 credits** (~$2.20 @ ~$0.05/cr) |

Balance: 666 → 622 (44 consumed, confirmed via `/balance`). Within budget.

---

## 1. What proved, what changed vs the prior empirical anchor

### 1.1 The image-gen leg — Meshy text-to-image (provenance + capability both satisfied)

**Host image-gen capability check (done first, per dispatch):** the ONLY image/3D API key on this host is `MESHY_API_KEY` (in `reincarnated-collaboration/.env`). No OpenAI / Stability / Replicate / fal / Gemini / HF keys in env, dotfiles, or repos; no image-gen CLIs on PATH. So the available image-gen capability on this host IS Meshy's hosted text-to-image endpoint.

This is **both** the available-capability path AND the substrate-grounded path: the image is generated in-pipeline and passed to image-to-3D (`input_task_id` chain), preserving the image-pass-through-to-Meshy provenance the dispatch + D7 require. The dispatch explicitly allowed Meshy text-to-image as a substitute that does NOT violate pipeline intent. **D7: PASS by construction** — no Crusader, no raw-LLM player-facing surface; the asset is image→3D substrate-grounded.

Model used: `gpt-image-2` (strongest prompt adherence for the load-bearing negatives "empty hands / no props / no fantasy"). `nano-banana` (3 cr) / `nano-banana-2` (6 cr) are cheaper alternatives if cost matters at corpus scale.

**Reference image verdict (visually inspected):** clean pass on every design-intent criterion — ordinary contemporary adult human; full-body front-facing; clear silhouette on plain grey studio bg; A-pose with arms away from body; both hands empty/open and visibly holding nothing; contemporary casual clothing (navy tee, khaki chinos, white sneakers); neutral expression; zero fantasy/props/accessories; full head-to-feet figure with margin (ideal for image-to-3D). This is exactly the canonical "mundane human vs the becoming" contrast.

### 1.2 The image-to-3D leg

`POST /openapi/v1/image-to-3d` chained from the text-to-image task via `input_task_id` (no need to host the image publicly — Meshy resolves it internally). Params: `ai_model: latest`, `should_texture: true`, `pose_mode: a-pose`, `target_polycount: 50000`, `target_formats: [glb, fbx]`. Single-pass (no preview/refine split in the current image-to-3D API). Output: textured GLB (8.0 MB) + FBX (12.4 MB). glTF magic header verified (`glTF`).

### 1.3 The rig leg — THE finding that updates Risk R1

The 2026-06-06 spike (criterion 3.1/3.2, Session 1) found **rigging was web-app-only** (text-to-3D API returned zero skeleton; a human had to open Meshy web app, click Rig Character, export UE preset). Radagast carried that forward as **non-spike risk R1** ("Meshy web-app manual rig step is unautomatable today").

**That is no longer true.** The current Meshy API (meshy-5/-6 era) exposes `POST /openapi/v1/rigging` (5 credits). I ran it chained from the image-to-3D task (`input_task_id`); it completed `SUCCEEDED` with zero manual intervention. Empirical proof the output is genuinely rigged (parsed the GLB's glTF JSON chunk):

| GLB | skins | joints | animations | skeleton root + convention |
|---|---|---|---|---|
| `earth_avatar.glb` (pre-rig i23d) | 0 | 0 | 0 | static mesh (1 node) — as expected |
| `earth_avatar_rigged.glb` | 1 | **24** | 1 (`baselayer`) | **`Hips`-rooted, Mixamo-convention** (`Hips`, `LeftUpLeg`, `LeftLeg`, `LeftFoot`, `LeftToeBase`, `RightUpLeg`...) |
| `anim_walking_withSkin.glb` | 1 | 24 | 1 (`walking_man`) | same skeleton |

The 24-joint Hips-rooted Mixamo-convention skeleton **matches the convention the criterion-3.2 Crusader→UE Interchange import path already consumes cleanly**. So the proven UE import leg applies directly to this asset — no new import-path risk introduced.

**R1 disposition: RETIRED for this model class** (clean single forward-facing textured humanoid). Caveat held honestly: the API docs flag pose-estimation failure for non-forward-facing / unclear-limb / untextured / >300k-face inputs; our `pose_mode: a-pose` + forward-facing + textured reference satisfies all constraints, which is *why* it worked. Corpus-scale kit-form avatars (radagast contract 6.8) that are non-humanoid or occluded-limb may still hit the manual path — but the **generic-human MVP avatar is fully automatable**.

---

## 2. The residual gap — idle animation (and how it closes)

Meshy rigging ships `basic_animations` = **walking + running only** (each as withSkin GLB/FBX + armature-only GLB). **No idle, no T-pose/A-pose rest clip.** The MVP need is exactly a *calm standing idle* (per framing brief § 2 step 3 + dispatch).

This is NOT a blocker and NOT a manual-rig gap — the rig itself is done. The idle clip is a downstream animation-retarget step, trivial because the skeleton is standard Mixamo convention:

- **Path A (recommended): Mixamo idle retarget.** Upload `earth_avatar_rigged.fbx` (or the GLB) to Mixamo, apply any "Idle"/"Breathing Idle" animation, export — Mixamo's auto-rigger recognizes this exact skeleton. OR download a generic Mixamo idle and retarget in UE (the bone names already match Mixamo, so UE IK Retargeter setup is minimal).
- **Path B (in-UE): UE5 retarget.** Import the rigged FBX/GLB, build an IKRig on the Hips-rooted skeleton, retarget any humanoid idle (UE Mannequin idle or marketplace) — the Mixamo-convention names make the chain mapping near-automatic.
- **Path C (degenerate MVP): the `baselayer` clip.** The rigged GLB already carries a `baselayer` clip; for a first assembly pass even a static rest pose reads as "standing on the knoll." Idle polish can follow.

**Recommendation:** Path A (Mixamo idle) is the cheapest faithful idle; it is a ~2-minute human step (one upload, pick "Idle", export) OR fully scriptable later. For the immediate MVP scene assembly, Path C unblocks instantly and Path A/B layer the calm-idle feel.

---

## 3. The import step — what david-h's UE-import lane needs

STOPPED before UE import per dispatch. The UE-import lane should consume:

1. **Primary import asset:** `earth_avatar_rigged.glb` (14.2 MB; skinned, 24-joint Hips-rooted skeleton, Mixamo convention). FBX equivalent `earth_avatar_rigged.fbx` (15.6 MB) if the Interchange/FBX path is preferred — criterion 3.2 used FBX for the Crusader.
2. **Import path: identical to the proven Crusader path** (criterion 3.2: interactive Interchange import → clean skeleton, Hips root). No new path risk — same skeleton convention verified.
3. **Idle:** not in the GLB; apply Mixamo/UE idle retarget post-import (§ 2). For first composition pass, the static rest is acceptable.
4. **Naming / staging-as-persistent-actor (operator-framing heads-up):** manifestation is a RECURRING jump-in/jump-out transition (Warframe Operator model), so the Earth avatar is a **persistent reusable scene actor asset**, not a one-shot cinematic prop. Recommend importing as a reusable `SK_EarthAvatar` skeletal mesh + a dedicated `Skeleton` asset under a stable content path (e.g. `/Game/Characters/EarthAvatar/`) so the same asset is referenced across repeated manifestation transitions — avoid burying it inside a one-shot cinematic folder.
5. **Constraint:** no Crusader in any player-facing capacity (this avatar replaces it). Honored — the Crusader was not used anywhere in this pipeline.

---

## 4. Artifacts on disk (exact paths + sizes)

Staged under the UE project tree at:
`C:\dev\reincarnated-unreal\Reincarnated\RawAssets\EarthAvatar_S6\`
(WSL: `/mnt/c/dev/reincarnated-unreal/Reincarnated/RawAssets/EarthAvatar_S6/`)

| File | Bytes | Role |
|---|---|---|
| `earth_avatar_reference_0.png` | 2,009,879 | The generated reference image (image-gen leg output) |
| `earth_avatar.glb` | 8,014,492 | Image-to-3D output GLB, **un-rigged** (static, 0 joints) |
| `earth_avatar.fbx` | 13,050,364 | Image-to-3D output FBX, un-rigged |
| `earth_avatar_rigged.glb` | 14,237,892 | **Rigged GLB — 24-joint Mixamo skeleton — PRIMARY import asset** |
| `earth_avatar_rigged.fbx` | 16,362,876 | Rigged FBX (alt import path) |
| `anim_walking_withSkin.glb` | 14,250,672 | Meshy walking anim (skinned) |
| `anim_walking_withSkin.fbx` | 16,387,196 | Meshy walking anim (FBX) |
| `anim_walking_armature.glb` | 65,328 | Walking anim, armature-only |
| `anim_running_withSkin.glb` | 14,246,056 | Meshy running anim (skinned) |
| `anim_running_withSkin.fbx` | 16,378,988 | Meshy running anim (FBX) |
| `anim_running_armature.glb` | 60,712 | Running anim, armature-only |
| `s6_pipeline.py` | — | The driver (text-to-image → image-to-3d → rigging chain; re-runnable per step) |
| `s6_state.json` | — | Task IDs + credit ledger |
| `t2i_request.json` / `t2i_result.json` | — | Image-gen request + raw response (incl. exact prompt) |
| `i23d_request.json` / `i23d_result.json` | — | Image-to-3D request + raw response |
| `rig_request.json` / `rig_result.json` | — | Rigging request + raw response (output URLs) |

**Note on git:** `reincarnated-unreal` is NOT a git repository on this host (verified — no `.git` anywhere under the tree). Deliverable #2's "committed if git-tracked" condition is therefore not met; assets are staged on disk only. If the UE project should be version-controlled (or the raw-asset staging mirrored into the collab repo), flag for david-h/Matt — that is a repo-setup decision outside this spike's scope.

---

## 5. Scaffold register (Discipline #40)

| # | Scaffold / assumption | Value used | Locked by |
|---|---|---|---|
| 1 | Image-gen model | `gpt-image-2` (9 cr) for prompt adherence; `nano-banana` (3 cr) cheaper alt | Cost/quality call at corpus scale |
| 2 | Reference-image prompt | Single hand-authored prompt (see `t2i_request.json`) — one human, generic | Design intent (gandalf brief § 2); not substrate-derived (this avatar is a placeholder, not engine-emitted) |
| 3 | `pose_mode` | `a-pose` at both text-to-image and image-to-3d | Rigging-friendliness (criterion 3.2 A/T-pose constraint) |
| 4 | `target_polycount` | 50,000 | Matches criterion 3.1 range (30k–80k); UE-import-proven band |
| 5 | `height_meters` (rig) | 1.75 | Generic adult human default; rescale at UE import if needed |
| 6 | Idle animation | NOT produced here; downstream Mixamo/UE retarget (§ 2) | Animation-retarget step (out of pipeline scope) |
| 7 | Single avatar | Exactly one generic human | Dispatch scope (no multiples, no customization) |

---

## 6. Recommendations

1. **Update Risk R1** in radagast's consult (§ 5 non-spike risks): the rigging API retires R1 for the generic-human / clean-forward-facing-humanoid class. Keep R1 flagged ONLY for corpus-scale non-humanoid / occluded-limb kit-form avatars (contract 6.8). Routed to radagast/Sam as a finding, not self-edited (their doc).
2. **UE-import lane (david-h to coordinate after S5/S1 close):** consume `earth_avatar_rigged.glb` via the proven Crusader Interchange path; import as a **persistent reusable `SK_EarthAvatar`** under `/Game/Characters/EarthAvatar/` (operator-model reusability), NOT inside a cinematic folder.
3. **Idle:** apply a Mixamo "Idle" retarget post-import (§ 2 Path A) — cheap, faithful, and the Mixamo-convention skeleton makes it near-trivial. Path C (rest pose) unblocks first-assembly immediately.
4. **Corpus-scale forward note:** the full text-to-image → image-to-3d → rigging chain is now API-scriptable (44 cr/avatar; `s6_pipeline.py` is the seed). This materially improves the contract-6.8 kit-form asset-pipeline outlook vs the manual-rig assumption — flag for forward-architecture, but verify non-humanoid kit forms separately (the API's humanoid/forward-facing constraints are real).

---

## 7. Sign-off

**Authored:** mantis 2026-06-11. Spike S6 — all three legs PROVED, fully API-automatable, R1 retired for this model class, idle gap closes downstream.
**Scope honored:** pipeline proof only; no customization/multiples/scene work; STOPPED before UE import (editor owned by another mantis lane this wave).
**Disciplines:** D7 verified (image→Meshy substrate-grounded; no Crusader; no raw-LLM surface); #11 empirical (glTF chunk parsed to prove skeleton, not assumed); #40 scaffold register (§ 5); #41 substrate-led (avatar is a flagged placeholder, not faked-as-final).
**Cross-host finding:** R1 update routed to radagast/Sam (their consult doc; not self-edited).
**Push:** committed in collab repo; NOT pushed (wave-close push is david-h's, accumulated).

**End of S6 findings.**

---

## 8. Import leg (follow-up) — UE import: PASS

> **Added 2026-06-11 by mantis.** Editor lane FREE (S5/S1 closed); david-h dispatched the final leg. Headless `-nullrhi` per environment constraint (windowed crashes on DXGI from SSH/WSL). Import completed, persisted, verified.

### 8.1 Result — PASS

The rigged generic-human avatar is imported and staged as a **persistent reusable skeletal mesh** at `/Game/Characters/EarthAvatar/SK_EarthAvatar` (operator-model reusability — NOT cinematic-bound). All verification checks pass; assets persisted to disk.

### 8.2 Interchange surprise — bridge has no GLB/glTF factory; FBX twin used (same rigged asset)

**The proven Crusader path is FBX-via-`UFbxFactory`, not GLB-via-Interchange.** The UE_MCP_Bridge import handlers (`import_skeletal_mesh` / `import_static_mesh` / `import_animation` / `import_texture`) are ALL `UFbxFactory`-based and force `Task->Factory = FbxFactory` — they will not ingest a `.glb` (UE routes GLB through the Interchange glTF pipeline, which the bridge does not expose a handler for; `create_interchange_pipeline` exists but only spawns a pipeline *asset*, it is not an import path). The MeshyTest Crusader precedent on disk (`SK_Crusader_Idle` + Skeleton + Materials + Textures) was itself an **FBX** import.

So I imported **`earth_avatar_rigged.fbx`** — the FBX twin of the GLB. Both are the same Meshy-rigged asset (identical 24-joint Hips-rooted Mixamo skeleton; § 1.3 parsed the GLB, the FBX carries the same rig). This IS the proven path; the dispatch's "GLB via Interchange" framing was the format-aspiration, the deterministic bridge route is the FBX. No new import risk — exactly the format that produced the clean Crusader skeleton.

If a true GLB/Interchange import is wanted later (provenance-purity: import the literal GLB artifact), it needs either (a) a new bridge handler that runs `ImportAssetTasks` with NO forced factory (lets Interchange auto-select the glTF pipeline), or (b) a windowed/Python-console Interchange import. Flagged for forward-architecture, NOT a blocker for the MVP.

### 8.3 Verification (all empirical via bridge + on-disk)

| Check | Method | Result |
|---|---|---|
| Skeletal mesh created | `import_skeletal_mesh` → `importedAssets` | PASS — `/Game/Characters/EarthAvatar/SK_EarthAvatar` (1 asset, created:true) |
| 24-joint skeleton | `get_skeleton_info` | **PASS — boneCount 24, root `Hips` (index 0, parentIndex -1)** — matches § 1.3 glTF-chunk finding exactly |
| Skeleton asset bound | `get_mesh_info.skeletonPath` | PASS — `SK_EarthAvatar_Skeleton` |
| Material imported | `get_mesh_info.materialSlots` | PASS — 1 slot `Material_1`, `isDefaultFallback:false` (real material, not stand-in) |
| Textures imported | on-disk | PASS — `texture_0` + `texture_0_ncl1_1` (7.5 MB each) |
| Scale sanity | `get_mesh_info.heightM` | PASS — **1.75 m** (= rig `height_meters` scaffold; clean 1:1, no rescale needed) |
| Geometry sanity | `get_mesh_info` | vertexCount 97,962; lodCount 1; bounds half-height 87.5 cm (175 cm humanoid) |
| Persist on disk | `save_all_dirty` + `find` | PASS — see § 8.4 |

`list_bones` returned WARN (param-shape mismatch in my verify script); irrelevant — `get_skeleton_info` is the authoritative bone source and gave 24 + Hips root.

### 8.4 Asset paths (Content Browser + on-disk, sizes)

Content path: `/Game/Characters/EarthAvatar/`
On-disk: `C:\dev\reincarnated-unreal\Reincarnated\Content\Characters\EarthAvatar\`

| Content Browser | On-disk `.uasset` | Bytes | Role |
|---|---|---|---|
| `SK_EarthAvatar` | `SK_EarthAvatar.uasset` | 24,389,515 | **Skeletal mesh — primary persistent reusable asset** |
| `SK_EarthAvatar_Skeleton` | `SK_EarthAvatar_Skeleton.uasset` | 6,715 | 24-joint Hips-rooted Mixamo skeleton |
| `SK_EarthAvatar_PhysicsAsset` | `SK_EarthAvatar_PhysicsAsset.uasset` | 27,679 | Auto-generated physics asset |
| `Material_1` | `Material_1.uasset` | 5,508 | Skin/body material (slot 0) |
| `texture_0` | `texture_0.uasset` | 7,539,610 | Base color texture |
| `texture_0_ncl1_1` | `texture_0_ncl1_1.uasset` | 7,539,645 | Second texture map (normal/secondary) |

Import + verify driver: `spike-s5-s1/s6-import-earth-avatar.js` (re-runnable; `bReplaceExisting` on).

### 8.5 What the idle-retarget (downstream) will need

NOT done here per dispatch (render-judgment session needed first). When it fires:
- **Target skeleton:** `/Game/Characters/EarthAvatar/SK_EarthAvatar_Skeleton` (24-joint Hips-rooted Mixamo convention — IK Retargeter chain mapping is near-automatic; bone names already Mixamo).
- **Source idle:** Mixamo "Idle"/"Breathing Idle" (Path A, § 2) OR UE Mannequin idle via IKRig. The Meshy walking/running anims (`anim_walking_withSkin.fbx` etc.) can be retargeted onto this same skeleton via `import_animation` (skeletonPath = the skeleton above) — note `import_animation` is FBX-only too, so feed the `.fbx` anim twins, not the `.glb`.
- **No idle in the import:** the FBX carried the mesh + skeleton + (Meshy `baselayer`/static) — no calm-idle clip. Idle is a separate retarget step. Path C (rest pose) reads as "standing on the knoll" for first assembly.
- **Scale:** 1.75 m imported clean — no rescale needed before placement into LV_ManifestationKnoll (P1.5 assembly, gated on render session).

### 8.6 What Sam's Gate-2 should look at

1. **FBX-not-GLB substitution** (§ 8.2) — confirm acceptable that the literal imported artifact is the FBX twin, not the GLB named in the dispatch. They are the same Meshy-rigged asset; FBX is the bridge-supported + Crusader-proven format. If provenance-purity wants the literal GLB, that is a new-bridge-handler forward item, not an MVP blocker.
2. **`reincarnated-unreal` is not git-tracked on this host** (§ 4 note carries forward) — the imported `.uasset` files are staged on disk only, not committed. Only the collab-repo deliverables (this note + AGENT_STATE.md + the driver script under the UE tree) are git-relevant, and the driver script lives under the non-git UE tree. Collab-repo commit covers the findings note + AGENT_STATE.md.
3. **Scope honored:** no Mixamo idle retarget; no placement into LV_ManifestationKnoll (both downstream/P1.5, render-session-gated).

**Import leg signed off:** mantis 2026-06-11. PASS — `SK_EarthAvatar` persistent reusable skeletal mesh, 24-joint Hips-rooted skeleton, material + textures, 1.75 m clean scale. Headless `-nullrhi` (DXGI windowed constraint honored). Disciplines: #11 empirical (skeleton/material/disk all verified, not assumed); #41 substrate-led (imported the real rigged asset faithfully; flagged the FBX-vs-GLB format reality honestly rather than papering it); #40 (FBX-twin substitution registered as a scaffold-equivalent).
