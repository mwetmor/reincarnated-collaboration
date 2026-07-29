# PLUGIN PROVISIONING MENU — L7 VFX + L6 ANIMATION bake-offs

> ## RESEARCH ONLY — NOTHING INSTALLED.
> **Installation is Matt-gated, executed by drax in a provisioning prep cell.**
> No third-party code was executed. `~/Games/mcp-lab/` was not touched, listed or read.
> Four source-only repos were cloned to scratch **for reading**, never built, never run:
> `agentic_orchestration/legolas/research/2026-07-26-plugin-audit-scratch/` (4.9 MB;
> `Godot-AI-Particles`, `Godot-AI-Animation`, `mixamo-batcher`, `pro-addon`). Two release
> archives were downloaded to list their contents and then deleted. **The four clones remain
> — they are the evidence for the telemetry audit in §3 and I could not delete directories
> under my permissions; drax or Matt may remove them at will.**

**Author:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (`RUN-CONDUCTOR`), on Matt's
direct authorization · **Date:** 2026-07-26 · **Mode:** A (analytical)
**Target stack:** macOS 24.6.0 / Apple M2 / Godot **4.6.3.stable** Forward+/Metal, headless capture harness
**Governing laws:** L-C (verdicts expire — every version below is stamped with its read date),
L-D (never rank by catalogue count), L-J (contestant set frozen — nothing here is a new MCP contestant)

---

## §0 — How to read this, in five lines

- **The menu is not ranked.** Rows are ordered lap → alphabetical. Ranking is Matt's.
- **`extends-whom` is the load-bearing column.** Per the commission's rule: *editor-only tooling
  extends only the wires; runtime nodes and resources extend everyone.* **I found one complication
  and I am flagging it rather than smoothing it** — see §1.1.
- **Telemetry flag:** `CLEAN` = I read the source and found no outbound network. `FLAG` = it
  transmits, or its parent does. `UNKNOWN` = closed source or not read.
- **Every version has a pin mechanism.** Asset-Library rows carry the exact `download_commit`
  SHA the library itself serves — that is the strongest pin available for those.
- **Five rows have no license at all.** They are on the menu because they are on-target, and
  marked, because *no license = all rights reserved* and that is Matt's call, not mine.

---

## §1 — THE MENU

**45 rows.** Grouped **L7 → L6 → Layer 2 → Layer 3**, and **alphabetical within each group** (case-
insensitive). No preference ordering anywhere. `EW` = extends-whom (`ALL` = H + both wires ·
`WIRE` = the two MCP contestants · `ANY` = method-neutral CLI, therefore also H).

| # | Name | Layer | EW | Pinned version | License | Telem | Lap + brief | One-line note |
|---|---|---|---|---|---|---|---|---|
| 1 | **Compositor Lens Effects** (AL 5292) | 1 | **ALL** | AL commit `ff8fb933` | MIT | CLEAN | L7 ambient | Lens flare + god rays as a Godot 4 CompositorEffect |
| 2 | **GODOT-VFX-LIBRARY** (haowg) | 1 | **ALL** | `v1.0.0` (rel 2025-10-27) | MIT | CLEAN | L7 cast/aura/ambient | 35+ ready `.tscn` particle effects + 17 shaders, action-game framed; pure resources so H gets them too |
| 3 | **Godot Projectile Engine** | 1 | **ALL** | AL commit `53d9150a` | MIT | CLEAN | L7 cast | Pooled projectile manager; beta, 4.4-declared |
| 4 | **Godot Shaders Library** (Kelpekk, AL 4890) | 1 | WIRE | `v1.5` (rel 2026-07-20) | MIT | **FLAG** | L7 ambient/aura | In-editor browser for 2000+ godotshaders.com shaders — it fetches from the network on demand |
| 5 | **godot-4-VFX-assets** (GDQuest) | 1 | **ALL** | commit `HEAD` @ 2026-05-16 | MIT code / **CC-BY-NC-SA art** | CLEAN | L7 reference only | ★ Non-commercial art licence — study it, do not ship it |
| 6 | **Godot-particle-and-vfx-textures** (RPicster) | 1 | **ALL** | commit `HEAD` @ 2020-12-02 | CC0-1.0 | CLEAN | L7 cast/ambient | Soft-falloff sprite sheets — exactly what L7-V's i1→i2 round hand-generated in code |
| 7 | **proton_trail** | 1 | **ALL** | commit `HEAD` @ 2023-07-20 | MIT | CLEAN | L7 cast | 150★ 3D trail; three years cold, 4.x compat unverified |
| 8 | **Shader Previewer** (AL 4833) | 1 | WIRE | AL commit `ec60afda` | CC0 | CLEAN | L7 authoring aid | Live in-editor shader variable inspector; declares **4.6** |
| 9 | **Shader-Lib** (AL 2503) | 1 | WIRE | AL commit `c1c786f3` | MIT | CLEAN | L7 aura/ambient | Visual-shader node library, 4.2+; last touched 2024 |
| 10 | **TrailRenderer** (Hyrdaboo) | 1 | **ALL** | commit `HEAD` @ 2026-01-30 | MIT | CLEAN | L7 cast · L6 swing | Unity-style ribbon trail — the L6∩L7 overlap: sword-arc trails |
| 11 | **UniParticles3D** | 1 | **ALL** | AL commit `7b23c222` | MIT | CLEAN | L7 cast/ambient | Modular Unity-flavoured 3D particle system, 4.3-declared |
| 12 | **Vaportrail** (tcmug) | 1 | **ALL** | `v0.9` (rel 2026-01-27) | MIT | CLEAN | L7 cast · L6 swing | Curve-shaped, gradient-coloured 3D trail with camera alignment |
| 13 | **vkaParticleTool** (AL 2654) | 1 | WIRE | AL commit `7b4f638e` | MIT | CLEAN | L7 authoring aid | Inspector-dock multi-layer particle test panel; 4.2, 2024 |
| 14 | **YParticles3D** | 1 | **ALL** | `1.0` (rel 2026-05-31) | Unlicense | CLEAN | L7 cast/aura | Shuriken-style CPU particle GDExtension; ships macOS `.framework`, `compat_min 4.5` |
| 15 | **Advanced Model Import (4.6)** | 1 | WIRE | AL commit `39d00449` | MIT | CLEAN | L6 import | Bulk mesh/material extraction and replacement; explicitly targets **4.6+** |
| 16 | **Animation Library Unique-ifier** | 1 | WIRE | AL commit `358743c5` | MIT | CLEAN | L6 modular | Makes embedded animation libraries unique; declares **4.6** |
| 17 | **Animation Property Tracks – Batch Modification** | 1 | WIRE | AL commit `66c49eef` | MIT | CLEAN | L6 import | Bulk edit of loop/interp/update mode across many tracks |
| 18 | **fix_synty_anim_to_godot_with_autorigpro** | 1/3 | **ANY** | commit `HEAD` @ 2025-01-27 | GPL-3.0 | CLEAN | L6 retarget | ★ Purpose-built for **Synty→Godot** anim repackaging — but needs paid Auto-Rig Pro |
| 19 | **Godot4-OpenAnimationLibraries** | 1 | **ALL** | commit `HEAD` @ 2025-07-19 | **NONE** | CLEAN | L6 retarget | Ships working `BoneMap`/`SkeletonProfile` `.tres` files — a template set, no Synty map |
| 20 | **GodotHumanoidRetargetPlugin** (D3ZAX) | 1 | **ALL** | commit `HEAD` @ 2026-02-21 | **NONE** | CLEAN | L6 retarget | ★ Sole tool whose stated purpose *is* R4: retarget across **different rest poses**, Godot 4.6+ |
| 21 | **GodotIK** (monxa) | 1 | **ALL** | `v1.3.1` (rel 2025-06-07) | MIT | CLEAN | L6 foot-lock | 259★ 3D IK GDExtension w/ constraints + multi-chain; 21 open issues, 13 months cold |
| 22 | **godot-synty-tools** (hlarsen) | 1 | WIRE | commit `HEAD` @ 2026-05-08 | MIT (+donation note) | CLEAN | L6 import/retarget | ★ Has a **Base-Locomotion→SkeletonHumanoid3D** fixer — the exact 121-bone pack that inverted drax's character |
| 23 | **Import Replacer** | 1 | WIRE | AL commit `6677ca55` | MIT | CLEAN | L6 import | Post-import automation driven by tagged empties + custom props |
| 24 | **Mixamo Animation Batcher** | 1 | WIRE | AL commit `965fea4b` | MIT | CLEAN | L6 import/retarget | ★★ Batch `.import` `_subresources` patcher w/ `SkeletonProfileHumanoid` + rename + unmapped-track strip. **README: "Godot 4.6.2 (tested)"** |
| 25 | **Modifier Animation Baker** (TokageItLab) | 1 | WIRE | AL commit `ecb13e0f` | MIT | CLEAN | L6 foot-lock | Bakes modifier-IK output down to FK bone tracks — authored by a Godot animation maintainer |
| 26 | **Skeleton Poser (3D)** | 1 | WIRE | AL commit `aa1c5239` | LGPLv2 | CLEAN | L6 modular | Save/load/compose Skeleton3D poses; declares **4.6** |
| 27 | **synty-godot-converter** (DeniedWorks) | 1/3 | **ANY** | commit `HEAD` @ 2026-05-17 | **NONE** | CLEAN | L6/L7 materials | Python CLI: Synty `.unitypackage` → Godot **4.6+** with shader-mapped materials. 65★, no licence |
| 28 | **Unidot Importer** | 1 | WIRE | `v1.2.0.fbxbeta` @ 2024-11-12 | MIT | CLEAN | L6 walk/fight | ★ Only tool that reads Unity **AnimatorController** → Godot AnimationTree. **Self-declares 4.0–4.2 only** |
| 29 | **Unused Bone Track Remover** | 1 | WIRE | AL commit `137c897d` | MIT | CLEAN | L6 retarget | Strips tracks addressing bones absent from the target skeleton (the 21 `ik_*`/`*Proc_*`) |
| 30 | **`com.IvanMurzak.Godot.MCP.Animation`** | 2 | WIRE (W-MUR) | nuget **0.1.0** = tag `0.1.0` | Apache-2.0 | CLEAN¹ | L6 authoring only | 7 tools. Creates AnimationPlayer/Library/Animation/tracks/keys. **No import, no retarget, no AnimationTree** |
| 31 | **`…MCP.Beehave`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | none | 5 tools; wraps a third-party addon we do not have |
| 32 | **`…MCP.CSG`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | L5 (not L6/L7) | 6 tools |
| 33 | **`…MCP.Dialogic`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | none | 5 tools; wraps a third-party addon we do not have |
| 34 | **`…MCP.GridMap`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | L4/L5 (not L6/L7) | 7 tools |
| 35 | **`…MCP.Navigation`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | none | 6 tools |
| 36 | **`…MCP.Particles`** | 2 | WIRE (W-MUR) | nuget **0.1.0** = tag `0.1.0` = `69bdcdf4` | Apache-2.0 | CLEAN¹ | L7 — see note | ★★ 5 tools, **zero `ParticleProcessMaterial` reach.** Cannot author an effect (§3.2) |
| 37 | **`…MCP.PhantomCamera`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | L7 camera (marginal) | 7 tools; wraps a third-party addon we do not have. **R-6 forbids moving the judge** |
| 38 | **`…MCP.Terrain3D`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | none | 4 tools; wraps a **third-party** addon we do not have |
| 39 | **`…MCP.Tilemap`** | 2 | WIRE (W-MUR) | nuget **0.1.0** | Apache-2.0 | CLEAN¹ | none (2D) | 6 tools |
| 40 | **godot-mcp-pro extension mechanism** | 2 | — | **DOES NOT EXIST** | — | — | — | ★ No plugin/extension API. The 175-tool manifest is the ceiling (§3.3) |
| 41 | **Blender 5.2.0** (headless) | 3 | **ANY** | brew cask `blender` **5.2.0** | GPL | CLEAN | L6 retarget | The universal fallback retarget host; **row 18 cannot run without it** (row 27 is standalone Python) |
| 42 | **FBX2glTF** (godotengine fork) | 3 | **ANY** | `v0.13.1` @ 2023-06-13 | BSD + **FBX SDK EULA** | CLEAN | L6 import | ★ Release ships **macos-x86_64 only — no arm64.** Rosetta or self-build on M2 |
| 43 | **glTF-Transform CLI** | 3 | **ANY** | npm `@gltf-transform/cli@4.4.2` @ 2026-07-25 | MIT | CLEAN | L6 emit/inspect | Inspect/prune/weld/dedupe `.glb`; the neutral instrument for verifying an emit |
| 44 | **glTF-Validator** (Khronos) | 3 | **ANY** | commit `HEAD` @ 2025-12-30 | Apache-2.0 | CLEAN | L6 verification | Independent conformance check on emitted `.glb` — an *instrument*, not an authoring tool |
| 45 | **gltfpack / meshoptimizer** | 3 | **ANY** | `v1.2` @ 2026-06-30 (npm `gltfpack@1.2.0`) | MIT | CLEAN | L6 emit | Compresses/optimises the `.glb` the L6 pipeline emits; 8.1k★, pushed today |

¹ *`CLEAN` on rows 30–39 means the extension package's own source has no network code — verified by
grep on two of ten and by construction on the rest. **They cannot run without the core `godot_mcp`
addon, whose compiled-in default is Cloud (Q46).** The flag on the family as a whole is inherited, not
intrinsic. See §4.*

Row 45 is a **negative finding recorded as a row** so it cannot be lost: the second half of Layer 2
was asked as a question and the answer is "there is nothing to provision."

### §1.1 — A complication in `extends-whom`, stated rather than smoothed

The commission's rule — *editor-only extends only the wires* — is right about the **affordance** and
approximately right about the **capability**. Two facts push against it:

1. **drax's own L6 probe ran `godot --headless --import` from a plain shell** (report §1.1, exit 0 in
   2.78 s). That *is* an editor process. Editor plugins load in it — Murzak's addon demonstrably does
   (L3 §4.2, 39/39 tools headless).
2. Several rows here are **thin GDScript wrapped in a dock**. Row 24 is 312 lines whose entire
   payload is `ConfigFile` edits to `.import` files plus one `EditorFileSystem.reimport_files()` call.

So the honest reading: an editor-only addon extends the wires **directly**, and extends H **at the
cost of writing a headless-editor driver, or of lifting its recipe**. For most rows that cost is
small and the recipe is the valuable part. **Matt should know that provisioning row 24 to the wires
and not to H would hand the wires a head start that is procedural, not capability-based** — which is
exactly the confound L-H exists to prevent. My recommendation, offered as a recommendation and not a
ruling: **provision editor-only L6 tooling to all three cells or to none.**

---

## §2 — Dossiers: Layer 1 (Godot addons)

Fields, every row: name · source · version + pin · licence · **4.6 evidence** · surface class ·
extends-whom · install · telemetry · maintenance · lap served. `unknown` is written where it is true.

### 2.1 · Mixamo Animation Batcher — **the closest thing on the internet to L6's named gap**

- **Source:** https://github.com/KarnesTH/mixamo-animation-batcher · AL asset 5079
- **Version / pin:** `1.0.0`; AL serves commit **`965fea4b79e5f9465b452c6f5d7c4e0aecc010e3`**. Repo
  has no tags — **the AL commit SHA is the only durable pin.** Last push 2026-04-23.
- **Licence:** MIT · **Surface:** editor-only (`EditorPlugin` + dock at Project→Tools)
- **Extends-whom:** WIRE directly; H via §1.1 · **Install:** copy `addons/mixamo_animation_batcher/`, enable
- **4.6 evidence:** README states verbatim **"Godot 4.6.2 (tested)"**. Strongest 4.6 claim of any L6 row.
- **Telemetry:** **CLEAN** — read in full; 312 lines of GDScript, no `HTTPRequest`, no URLs.
- **Maintenance:** 2★, 0 open issues, single author, 407 KB.
- **What it actually does — read from source, not the README:**
  ```gdscript
  skel["retarget/bone_map"]                                = _create_bone_map()
  skel["retarget/bone_renamer/unique_node/skeleton_name"]   = "Skeleton"
  skel["retarget/bone_renamer/rename_bones"]                = true
  skel["retarget/remove_tracks/unmapped_bones"]             = true
  ```
  …written into `<file>.fbx.import` `params/_subresources/nodes/PATH:Skeleton3D`, followed by one
  `EditorFileSystem.reimport_files(_fbx_files)`. **That is drax's R4 mechanical patch, implemented.**
- **Two gaps that matter, and I want them on the record before anyone treats this as a drop-in:**
  1. **It never sets `rest_fixer/fix_silhouette`.** drax R4: *"`fix_silhouette` is not optional and
     must match on both sides."* This addon would produce a technically-retargeted, silhouette-wrong result.
  2. **It hardcodes the animation key `"mixamo_com"`** for the `save_to_file` block. Synty clips are
     keyed by filename (`A_MOD_SWD_Attack_HeavyCombo01A_Neut`). The `save_to_file` half does not
     transfer without an edit; the retarget half does.
  3. Its `sample_bone_map.tres` is a Mixamo map (`Spine_01`, `Elbow_L`, `Thumb_01_L`). Synty needs
     `reincarnated-godot/addons/sidekick_creator/sidekick_bone_map.tres` substituted.
- **Serves:** L6 import/retarget. **Verdict: provision as a reference implementation, not as a tool.**
  Its 60 load-bearing lines are worth more than its dock.

### 2.2 · godot-synty-tools (hlarsen) — the 121-bone pack, by name

- **Source:** https://github.com/hlarsen/godot-synty-tools · **Pin:** no tags/releases → commit `HEAD` @ 2026-05-08
- **Licence:** MIT, with a non-binding "commercial donation note" prepended to the MIT text.
- **4.6 evidence:** **unknown.** No version claim in README, no CI, no releases. Recency (2026-05) is
  the only signal and recency is not evidence.
- **Surface:** editor-only · **Extends:** WIRE (+H per §1.1) · **Install:** copy addon, enable, Project→Tools
- **Telemetry:** CLEAN (no network code in a 154 KB GDScript addon; not exhaustively read)
- **Maintenance:** 4★, 0 issues, single author. **Its own README recommends a different tool**
  (`DeniedWorks/synty-godot-converter`) for the general case — an honest signal I am passing through unchanged.
- **Why it is on the menu:** its `Base Locomotion` feature is *"Create animations and animation libraries
  properly mapped to Godot's SkeletonHumanoid3D."* drax's probe found the **121-bone base-locomotion pack
  is the one that fails** — it inverts an 88-bone pack character (head at y = −1.628). This is the only
  tool found that names that specific pack.
- **Serves:** L6 import + retarget.

### 2.3 · GodotHumanoidRetargetPlugin (D3ZAX) — right problem, no licence

- **Source:** https://github.com/D3ZAX/GodotHumanoidRetargetPlugin · **Pin:** commit `HEAD` @ 2026-02-21
- **Licence:** **NONE DECLARED — all rights reserved.** A Matt call, not mine.
- **4.6 evidence:** repo description states *"Plugin for Godot **4.6 or above**"*. Self-claim, unverified.
- **Surface:** addon + models + `test_scene.tscn` (2.1 MB) — ships a demo project · **Extends:** likely ALL
  (runtime retarget node) but **unverified**
- **Telemetry:** CLEAN (not deeply read) · **Maintenance:** 0★, 0 issues, one author, one push.
- **Why on the menu:** its stated purpose is *"animation retarget for humanoid skeletons with
  **different rest pose** and different structures."* drax R4 measured our gap as **27.69° mean /
  179.97° max rest-rotation disagreement at 98.7% name agreement.** No other tool found names the
  rest-pose axis. Sibling repo `D3ZAX/Humanoid-Retarget-Godot-Compatible` is the Blender half.
- **Serves:** L6 retarget. **High relevance, lowest confidence on the menu.**

### 2.4 · Unused Bone Track Remover · Modifier Animation Baker · Anim Property Tracks Batch

Three small MIT editor tools that each hit one named L6 sub-problem:

| tool | pin | 4.6 evidence | what it hits |
|---|---|---|---|
| Unused Bone Track Remover | AL commit `137c897d…` | AL declares **4.0**; last push 2026-02-16 | The 21 `ik_*` / `*Proc_*` / `upperarm_proportion_*` tracks the 121-bone pack carries and an 88-bone target cannot host |
| Modifier Animation Baker (TokageItLab) | AL commit `ecb13e0f…` | AL declares **4.5**; author is a Godot animation-system maintainer | Bakes modifier-IK → FK bone tracks. The credible **foot-lock** route: solve with IK, bake, ship FK |
| Anim Property Tracks Batch Modification | AL commit `66c49eef…` | AL declares **4.5** | Bulk loop/interp/update-mode edits across 3,386 clips |

All three: editor-only · WIRE (+H per §1.1) · MIT · CLEAN · install by copying the addon folder.
All three: **maintenance is thin** (0–1★, single author, no CI). They are 100–300-line utilities;
that is both the risk and the mitigation.

### 2.5 · Unidot Importer — the AnimatorController answer, two years cold

- **Source:** https://github.com/V-Sekai/unidot_importer · AL 2427 · **Pin:** `v1.2.0.fbxbeta` @ 2024-11-12
- **Licence:** MIT · **935★, 28 open issues, last push 2024-11-12 (~20 months)**
- **4.6 evidence: NEGATIVE.** README states verbatim *"Currently supports Godot Editor versions
  **4.0 through 4.2**."* Our stack is 4.6.3.
- **Surface:** editor-only, and it **requires FBX2glTF** (row 42 — macOS x86_64 only) configured in
  Editor Settings. It is a *translator*: `.unitypackage`/`.prefab`/`.unity` → `.tscn`/`.tres`, and it
  is designed to be deleted afterwards (except `runtime/anim_tree.gd`).
- **Why it stays on the menu despite being cold:** drax's probe §8 recorded *"Four `.controller` files
  in the packs are Unity `AnimatorController` assets — unusable by Godot, but readable as Synty's
  intended state machine."* **Unidot is the only tool found that converts an AnimatorController into a
  Godot AnimationTree.** L6's brief includes *walk→fight transitions*. Synty already authored that
  state machine and it is sitting in the packs unread.
- **Serves:** L6 walk/fight/transition. **Recommendation: treat as an evidence source, not a
  dependency** — even if it will not run on 4.6, its `.controller` parser documents what Synty intended.

### 2.6 · synty-godot-converter (DeniedWorks) — 4.6+ by name, no licence

- **Source:** https://github.com/DeniedWorks/synty-godot-converter · **Pin:** commit `HEAD` @ 2026-05-17
- **Licence:** **NONE DECLARED.** 65★, 4 open issues, 907 KB.
- **4.6 evidence:** repo description: *"Convert Synty POLYGON asset packs to Godot **4.6+** with proper
  materials and custom shaders."* Ships `shaders/`, `shader_mapping.py`, `unity_parser.py`,
  `tres_generator.py`, `godot_converter.gd` — a Python CLI plus a GDScript half.
- **Surface:** **CLI** (+ a `.gd`) · **Extends: ANY** — a Python CLI is method-neutral, so it extends H
  as much as the wires. **That makes it one of the few Layer-1 rows that cannot bias the bake-off.**
- **Telemetry:** CLEAN (file listing + no network deps in `requirements-gui.txt`; source not exhaustively read)
- **Serves:** L6 import + L7 materials. `hlarsen` (row 22) recommends it over his own addon.

### 2.7 · The VFX resource libraries — the rows that extend everyone

**GODOT-VFX-LIBRARY** (haowg) — https://github.com/haowg/GODOT-VFX-LIBRARY · `v1.0.0` (rel
2025-10-27), push 2026-01-25 · **MIT** · 288★, 1 open issue, 1.9 MB · README badge **Godot 4.5+** ·
**pure-resources** (`effects/*.tscn`, `shaders/*.gdshader`) → **extends ALL THREE** · install = copy
`addons/` · **CLEAN** · L7 cast/aura/ambient. *35+ particle effects and 17+ shaders, self-described as
built for action games.* **This is the single highest-leverage L7 row**, because a `.tscn` effect is
equally loadable by a hand-authored GDScript pass, by Pro's `create_particles`, and by Murzak.

**Godot-particle-and-vfx-textures** (RPicster) — CC0-1.0, 362★, 10.7 MB, **last push 2020-12-02.**
Textures do not rot. L7-V §6 spent iteration i2 hand-generating *"a procedural soft-falloff sprite,
generated in code"* because the particles read as hard squares. **A CC0 texture set removes that entire
round from every cell equally.** pure-resources → ALL. CLEAN.

**godot-4-VFX-assets** (GDQuest) — **★ licence split: MIT code, CC-BY-**NC**-SA-4.0 art.** 127★, push
2026-05-16. Non-commercial art in a project with shipping ambitions is a trap. On the menu as
**reference-only**, and I would not put it in a cell that produces a shippable frame.

**YParticles3D** — Unlicense (public domain), `1.0` rel 2026-05-31, 3★. **GDExtension**, therefore
**runtime-nodes → ALL THREE.** I listed the release archive: it ships
`bin/macos/libyparticles3d.macos.editor.single.framework` **and** `…template_release…`, plus Linux and
Windows. `yparticles3d.gdextension` sets `compatibility_minimum = "4.5"` → should load on 4.6.3.
**Caveat: it is a *CPU* particle system.** L7-V's cost account found particle **area**, not count, is
the cost driver; a CPU system changes that arithmetic and would need re-benching, not inheritance.

**Trails — three options, one decision.** `Vaportrail` (MIT, `v0.9` rel 2026-01-27, curve shape +
gradient + camera alignment, 14★), `TrailRenderer` (MIT, push 2026-01-30, 73★, 46 MB repo),
`proton_trail` (MIT, 150★, **cold since 2023-07**). All runtime-nodes → **ALL THREE**. All CLEAN.
**Trails sit on the L6∩L7 seam**: drax measured the L6 blade tip travelling **3.347 m with a 46.7 m/s
peak step**. That is the canonical trail case and neither lap currently owns it.

### 2.8 · The rest of Layer 1, in one table

| Name | Pin | Lic | 4.6 evidence | Surface | EW | Telem | Maint | Serves |
|---|---|---|---|---|---|---|---|---|
| Godot Shaders Library (Kelpekk) | `v1.5` @ 2026-07-20 | MIT | AL declares 4.1; **push 2026-07-26** | editor-only | WIRE | **FLAG** — fetches godotshaders.com on demand | 28★, active | L7 |
| Shader-Lib (DigvijaysinhGohil) | AL `c1c786f3` | MIT | 4.2+; last mod 2024-10 | editor-only (visual-shader nodes) | WIRE | CLEAN | stale | L7 |
| Shader Previewer | AL `ec60afda` | CC0 | AL declares **4.6** | editor-only | WIRE | CLEAN | 2026-04 | L7 aid |
| Compositor Lens Effects | AL `ff8fb933` | MIT | *"4.4 upwards"* | runtime (CompositorEffect) | ALL | CLEAN | 2026-06 | L7 ambient |
| vkaParticleTool | AL `7b4f638e` | MIT | 4.2, 2024-03 | editor-only dock | WIRE | CLEAN | cold | L7 aid |
| UniParticles3D | AL `7b23c222` | MIT | 4.3, 2025-07 | runtime-nodes | ALL | CLEAN | superseded by YParticles3D (same author) | L7 |
| Godot Projectile Engine | AL `53d9150a` | MIT | 4.4, `0.6.0-beta` | runtime-nodes | ALL | CLEAN | 2025-08 | L7 cast |
| Advanced Model Import (4.6) | AL `39d00449` | MIT | title + AL declare **4.6** | editor-only | WIRE | CLEAN | 11★, 2026-02 | L6 import |
| Import Replacer | AL `6677ca55` | MIT | 4.4; push 2026-05-24 | editor-only | WIRE | CLEAN | 25★, active | L6 import |
| Animation Library Unique-ifier | AL `358743c5` | MIT | AL declares **4.6** | editor-only | WIRE | CLEAN | 2026-03 | L6 modular |
| Skeleton Poser (3D) | AL `aa1c5239` | **LGPLv2** | AL declares **4.6** | editor-only | WIRE | CLEAN | `0.1`, 2026-05 | L6 modular |
| Godot4-OpenAnimationLibraries | `HEAD` @ 2025-07-19 | **NONE** | 4.x generic | pure-resources (`.tres` BoneMaps + libraries) | ALL | CLEAN | 334★, 229 MB | L6 retarget |
| GodotIK (monxa) | `v1.3.1` @ 2025-06-07 | MIT | 4.3+; ships `libik.dylib` | runtime GDExtension | ALL | CLEAN | 259★, **21 open issues**, cold 13 mo | L6 foot-lock |
| fix_synty_anim_…autorigpro | `HEAD` @ 2025-01-27 | GPL-3.0 | Blender-side, engine-agnostic | Blender extension → `.glb` | ANY | CLEAN | 16★, cold | L6 retarget |

---

## §3 — Dossiers: Layer 2 (MCP-server-side)

### 3.1 · Murzak's ten-package family — all ten enumerated, first time

**This is the family L-C flagged: shipped 2026-07-20, ruled on 2026-07-23 without being seen.**
Enumerated from nuget's search index + all ten GitHub repos, read 2026-07-26.

| # | NuGet package id | Repo | Ver | Tag | Pushed | Tools (from README) |
|---|---|---|---|---|---|---|
| 1 | `com.IvanMurzak.Godot.MCP.Animation` | `IvanMurzak/Godot-AI-Animation` | 0.1.0 | `0.1.0` | 2026-07-20 | **7** — `animation-defaults` `-player-create` `-library-add` `-create` `-add-track` `-insert-key` `-get` |
| 2 | `…MCP.Particles` | `Godot-AI-Particles` | 0.1.0 | `0.1.0` = `69bdcdf4` | 2026-07-20 | **5** — `particles-defaults` `-create` `-configure` `-set-emitting` `-get` |
| 3 | `…MCP.GridMap` | `Godot-AI-GridMap` | 0.1.0 | `0.1.0` | 2026-07-20 | **7** — `gridmap-defaults` `-create` `-set-cell` `-clear-cell` `-clear` `-set-mesh-library` `-get` |
| 4 | `…MCP.CSG` | `Godot-AI-CSG` | 0.1.0 | `0.1.0` | 2026-07-20 | **6** — `csg-box-create` `-sphere-create` `-cylinder-create` `-combiner-create` `-set-operation` `-get` |
| 5 | `…MCP.Tilemap` | `Godot-AI-Tilemap` | 0.1.0 | `0.1.0` | 2026-07-20 | **6** — `tilemap-create` `-set-tileset` `-set-cell` `-erase-cell` `-clear` `-get-used-cells` |
| 6 | `…MCP.Navigation` | `Godot-AI-Navigation` | 0.1.0 | `0.1.0` | 2026-07-20 | **6** — `navigation-region-create` `-region-set-mesh` `-agent-create` `-agent-configure` `-link-create` `-get` |
| 7 | `…MCP.Terrain3D` | `Godot-AI-Terrain3D` | 0.1.0 | `0.1.0` | 2026-07-20 | **4** — `terrain3d-defaults` `-create` `-set-height` `-get-info` |
| 8 | `…MCP.Dialogic` | `Godot-AI-Dialogic` | 0.1.0 | `0.1.0` | 2026-07-20 | **5** — `dialogic-defaults` `-create-timeline` `-create-character` `-add-event` `-get-timeline` |
| 9 | `…MCP.Beehave` | `Godot-AI-Beehave` | 0.1.0 | `0.1.0` | 2026-07-20 | **5** — `beehave-defaults` `-create-tree` `-add-composite` `-add-leaf` `-get-tree` |
| 10 | `…MCP.PhantomCamera` | `Godot-AI-PhantomCamera` | 0.1.0 | `0.1.0` | 2026-07-20 | **7** — `phantomcamera-defaults` `-host-create` `-create` `-set-follow` `-set-look-at` `-set-priority` `-get` |

**Total from READMEs: 58 tools. The lab's `extension_catalog_summary.txt` declares 63.**
I did not read that artefact (mcp-lab is forbidden ground this run) and I am not asserting either
number is wrong — I am recording that **two independent counts of the same family disagree by five**,
which is precisely the L-D/L-B shape and should be settled on the wire, not on paper.

**Common properties, verified across the family:**
- **Licence: Apache-2.0**, all ten, consistent between GitHub and the nuspec.
- **Pin mechanism: `<PackageReference Version="0.1.0"/>`.** All ten carry git tag `0.1.0`. For
  Particles I diffed `0.1.0..HEAD`: **zero changes under `src/`** — four commits, all CI. `main` and
  the published package are source-identical. **The nuget version is a sound pin.**
- **Delivery: SOURCE-ONLY NuGet.** `IncludeBuildOutput=false`; the `.cs` ship under `src/` and are
  injected as `<Compile>` items into the consumer by an auto-imported `build/<PackageId>.props`. They
  compile **inside** the consumer project against the consumer's own GodotSharp. No bundled Godot, no
  DLL, no version lock. This is a genuinely good design and it is worth saying so.
- **Install cost, and it is not free:** *"Extensions dock"* / `godot-cli install-extension <id>` /
  hand-edited `<PackageReference>` — **and then a `dotnet build` of the consumer project.** The consumer
  must be a `Godot.NET.Sdk` (Mono/.NET) project. This confirms L3's P-E finding that L6/L7 need a
  sibling .NET project; it is not an optional convenience.
- **Telemetry, audited by grep on the two clones:** `Godot-AI-Particles` and `Godot-AI-Animation`
  contain **zero** `http(s)://`, `HttpClient`, `WebSocket`, `SignalR`, `telemetry`, `analytics`,
  `MachineName` or `ai-game.dev` references in `src/`. The only URL anywhere is `--url
  http://localhost:5300` in a CI test harness. **Intrinsically CLEAN.**
- **…but they inherit Q46 whole.** All ten declare `com.IvanMurzak.McpPlugin >= 6.10.0` and require the
  core `godot_mcp` addon to load at all. That addon's compiled-in default is Cloud and it transmits
  `machine_name` + `project_path_hash` to `ai-game.dev` before any tool call. **Installing an extension
  installs nothing new that phones home, and removes nothing that already does.**
- **4.6 EVIDENCE — the finding I would hand Matt first:** the extension CI matrix is
  ```
  - godot: "4.3.0"   - godot: "4.4.1"   - godot: "4.5.1"
  ```
  **There is no 4.6 leg in any of the ten.** Meanwhile the **core** `Godot-MCP` repo *does* test 4.6 and
  4.7 (issue #206, *"ci: add Godot 4.6 + 4.7 to the engine test matrix"*, closed 2026-06-23).
  **So the core is 4.6-tested and its extensions are not.** Our stack is 4.6.3. This is a real,
  named, unresolved compat risk and it applies to the whole family at once.
- **Maintenance:** created 2026-06-27→29, one release each (2026-06-28), all pushed 2026-07-20,
  **0 open issues across all ten**, 0–1★, 164–176 nuget downloads each. Single author. Six of the ten
  wrap **third-party addons we do not have** (Terrain3D, Dialogic, Beehave, PhantomCamera + Tilemap/
  Navigation are engine-native) — for those, installing the MCP wrapper is the *second* install.

### 3.2 · ★★ `Godot-AI-Particles` cannot author a VFX pass — read from source

This is the highest-consequence finding of the run and it changes what L7 should test.

The complete parameter surface of `particles-create` + `particles-configure`, verbatim from
`Tool_Particles.Configure.cs` and `Tool_Particles.Create.cs` at tag `0.1.0`:

> `dimension` · `name` · `parentPath` · `amount` · `lifetime` · `oneShot` · `explosiveness` ·
> `randomness` · `speedScale` · `preprocess` · `localCoords`

**That is all of it.** A grep across the entire `src/` tree for
`ProcessMaterial|DrawPass|Mesh|Material|Texture|Gradient|Curve` returns **zero hits.**

`Create` instantiates `new GpuParticles3D()`, applies those scalars, parents it, sets `Owner`, and
returns. **It attaches no `ParticleProcessMaterial` and no draw pass.**

Set against what L7-V actually did to arrive at its pass — procedural soft-falloff sprite, HDR peak
management against a 1.25 glow threshold, emission radius 0.38→0.24, `radial_accel` spread, upward
velocity cut to a quarter, sprite scale 1.70 m growing 2.1× over life, damping, lifetime curves —
**every single one of those parameters lives on `ParticleProcessMaterial` or the draw-pass mesh/material,
and this extension reaches none of them.**

**Consequence for the bake-off, stated as a consequence and not a verdict:** the charter's L7 line
reads *"field + `Godot-AI-Particles` + Pro's `create_particles`"*, which presents the two as
counterparts. **They are not counterparts.** `Godot-AI-Particles` can create an emitter and set its
count; it cannot make it look like anything. A W-MUR L7 cell provisioned with it would have to fall
back to `node-modify` with the ResourceRef shape from L3 §4.6 — the exact addressing that L3 found
**undiscoverable from the wire's own schemas** — for every material property. **That is the real L7
question for W-MUR, and it is not a question about the extension.**

### 3.3 · godot-mcp-pro 1.15.1 — no extension mechanism, and a clean network surface

- **Source:** https://github.com/youichi-uda/godot-mcp-pro (public repo = **addon only**)
- **Version:** `plugin.cfg` reads `version="1.15.1"`, description *"…expose 175 editor tools"* —
  **the addon's own manifest agrees with the lab's measured 175**, against the docs' 77. Repo
  description still says 162. Three numbers, two of which are wrong; the wire and `plugin.cfg` agree.
- **Licence: split, and the repo contradicts itself.** `LICENSE` is plain MIT + a trailing note:
  *"This license applies to the Godot editor plugin (`addons/godot_mcp/`). The MCP server (TypeScript)
  is distributed separately under a **proprietary** licence as part of the paid package."* README §License
  says flatly *"Proprietary."* GitHub classifies the repo `NOASSERTION`. **Addon MIT, server proprietary,
  $15 one-time.**
- **EXTENSION MECHANISM: NONE.** No plugin API, no extension registry, no add-on packages, nothing on
  npm (`godot-mcp-pro` is not a published npm package). The server ships as pre-built JavaScript inside
  the paid zip. **175 tools is the ceiling and there is nothing to provision.** Recorded as menu row 40.
- **Telemetry: CLEAN, and this is worth stating precisely.** I cloned the public addon (35 `.gd`
  files, 3.0 MB) and grepped for `https?://`, `HTTPRequest`, `HTTPClient`, `license_key`, `activation`,
  `telemetry`, `analytics`, `gumroad`. **Zero hits.** The only network code is
  `ws.connect_to_url("ws://127.0.0.1:%d")` over ports **6505–6514 — loopback only.**
  **Honest limit: the paid TypeScript server is closed-source and I could not audit it.** The addon
  half is clean; the server half is `UNKNOWN`.
- **★ The asymmetry Matt should see:** the **Apache-2.0 open-source** instrument (W-MUR) ships a
  compiled-in Cloud default that transmits machine name and project identity before any tool call.
  The **paid proprietary** instrument's open half is loopback-only with no telemetry at all. **The
  licence axis and the privacy axis run opposite here.** That is a fact about these two instruments,
  not a general law, and it belongs on the record when they are scored.
- **★★ And Pro's particle surface is the one that reaches the material.** From its README tool tables:
  ```
  Particle Tools (5):  create_particles · set_particle_material (ParticleProcessMaterial)
                       set_particle_color_gradient · apply_particle_preset (fire, smoke, sparks…)
                       get_particle_info
  AnimationTree (4):   create_animation_tree · get_animation_tree_structure · set_tree_parameter · …
  State Machine (3):   advanced state-machine management
  Animation (6):       list/create/add_track/set_keyframe/get_info/remove
  ```
  **Documented, not measured** — L-B says the manifest is right about *what exists* and silent about
  *how to call it*. But on paper Pro reaches `ParticleProcessMaterial`, colour gradients and named
  presets (**fire, smoke, sparks** — three of the five effects L7-V hand-built), and it has
  AnimationTree + state-machine tools that Murzak's Animation extension does not have at all.

---

## §4 — Q46-class telemetry findings, consolidated

| # | Component | Finding | Status |
|---|---|---|---|
| **T1** | Core `godot_mcp` addon (Murzak) | Compiled-in default is Cloud; transmits `machine_name` + `project_path_hash` + `project_name` to `wss://ai-game.dev/…` **before any tool call**. Mitigated only by four env vars set at launch. | **Open ruling Q46.** Confirmed unchanged: the repo's own GitHub description as of today reads *"…with cloud connection to ai-game.dev."* |
| **T2** | All ten `Godot-AI-*` extensions | **Intrinsically CLEAN** — no network code in their own source. **They inherit T1 whole**, because they cannot load without the core addon. | New finding. Extensions do not worsen Q46; they also do not escape it. |
| **T3** | `Godot Shaders Library` (menu row 4) | **FLAG.** Its entire function is browsing/downloading 2000+ shaders from **godotshaders.com** from inside the editor. Not covert, but it is an editor process making outbound requests during a measured cell. | New. Would need a network-quiet ruling before it enters a timed cell. |
| **T4** | `godot-mcp-pro` addon (public half) | **CLEAN.** Zero external URLs, zero HTTPRequest, loopback WebSocket only. | New, and it is exculpatory. |
| **T5** | `godot-mcp-pro` server (paid half) | **UNKNOWN — closed source, not auditable.** | Named as a gap, not as an accusation. |
| **T6** | Murzak addon self-write (L3 §4.12) | Still stands: on plugin load it writes 39 `SKILL.md` files into `<project>/.claude/skills`. **Adding extensions will grow that set** — each extension's `[AiTool]` family is auto-discovered and skill-generated. | Predicted, unverified. A provisioning cell should re-fingerprint after install. |
| **T7** | `~/.dotnet` escape (L3 §7) | Installing ten source-only NuGet packages means ten more `dotnet restore` operations. Unless `DOTNET_CLI_HOME` is redirected, the escape recurs and grows. | Carried forward; `env.sh` fix already known. |

**Nothing on this menu was found to phone home covertly.** T1 remains the only component that
transmits machine identity, it was already known, and it is already Matt's.

---

## §5 — Deliberately excluded, and why

| Candidate | Why excluded |
|---|---|
| **EasyIK** (AL 5324, MIT, 4.6, 2026-07) | Its own description: *"universal **2D** inverse kinematics."* L6 is 3D. Fresh and well-licensed and **wrong axis** — it would have looked like a strong row from the metadata alone. |
| **smix8/GodotAnimationRetargeting** (135★, MIT) | It is an **engine module**, not an addon — it requires recompiling Godot from source. That breaks the *"Godot 4.6.3.stable.official.7d41c59c4"* stack every measurement in this program is pinned to. Dead on arrival, not dead as software. |
| **RenIK** | The only live trace is `V-Sekai/godot-renik`, **0★, last push 2025-11-19, no README, no releases.** The commission named it as a seed; the seed did not germinate. Godot 4.4+ absorbed this territory into core `SkeletonModifier3D` / `LookAtModifier3D` / `RetargetModifier3D` / `SpringBoneSimulator3D` (all four confirmed present in stable class docs). **The successor to RenIK is the engine.** |
| **Mixamo Animation Retargeter** (AL 3429) | **GPLv3** + `v0.1` + last touched 2024-10 + superseded in every respect by row 24. A community fork exists (`ptupi/fix-retargeter`) with 0★ and no licence. |
| **Mixamo Root Motion Remover** (AL 4126) | Solves the inverse of our problem. Synty **already ships both regimes** (`_RM_` twin + in-place original, drax R5). Nothing to remove. |
| **Foot-IK repos** (`Star2578/godot-foot-ik`, `ownverseplay/Godot4.6.2-foot-ik-demo`, `SeaKrill/Godot-Foot-IK`) | 0–6★, all but one with **no licence**, all demo-projects rather than addons. Foot-lock has no maintained addon; the credible route is core `SkeletonModifier3D` + row 25's bake. |
| **`godotengine/FBX2glTF`** *as a primary path* | Kept on the menu (row 42) but **not recommended**: last release 2023-06-13, and the macOS artefact is **`FBX2glTF-macos-x86_64` only — no arm64**. On an M2 that is Rosetta or a self-build against the Autodesk FBX SDK EULA. **Godot 4.6's built-in ufbx already imports the corpus headlessly in 2.78 s** (drax §1.1). This is a fallback, not a route. |
| **`Karl0007/godot-mcp-pro`, `neondeex/GodotMCP-Pro-Free-Client`, `bahoz7/godot-mcp-pro-free-server`, `laishilong783/Godot-mcp-pro`** | Unofficial re-implementations / clones of a paid product. **L-J freezes the contestant set** — these would be new contestants wearing an incumbent's name. Excluded on governance, not on quality. |
| **`Intelli-verse-X-Unity-SDK`, `Godot Firebase`, `blockchain_sdk`, Matrix SDKs** | Search noise from the `unity`/`fire`/`IK` substring queries. Named so the exclusion is visible rather than silent. |
| **`Godot-AI-Tools-Template`** | The scaffold Murzak's ten extensions were generated from. Not a tool — but it is the honest answer to *"could we author our own extension?"*: **yes, and it is Apache-2.0 with a documented source-only recipe.** Out of scope for provisioning; on the record as an option. |

### Rows I am deliberately leaving on the menu despite a disqualifying-looking field

- **Rows 19, 20 and 27 have no licence at all** (`Godot4-OpenAnimationLibraries`,
  `GodotHumanoidRetargetPlugin`, `synty-godot-converter`). They are three of the most on-target
  Synty/rest-pose finds. *No licence = all rights reserved*, which is stricter than GPL. **I am not
  filtering them out; I am marking them.** (Score-don't-filter: an unlicensed tool can still be *read*
  for its method, which for rows 20 and 27 is most of their value.)
- **Row 28 self-declares 4.0–4.2** and I still listed it, because its `.controller` parser is the only
  thing that reads a Synty state machine and that is worth something even if the addon never loads.

---

## §6 — Open questions research alone could not settle

Each is a hands-on measurement, and each is named with the exact check that would settle it.

1. **Do any of the ten Murzak extensions load on Godot 4.6.3?** Their CI matrix stops at 4.5.1. The
   core addon tests 4.6/4.7; the extensions do not. **Check:** install one (Particles is smallest),
   `dotnet build`, boot headless, and assert the addon-load line the extensions' own CI asserts —
   `'[Godot-MCP] plugin loaded'` — then `tools/list` and diff against 39.
2. **58 or 63?** Two counts of the same family disagree. **Check:** install all ten in one lab project
   and enumerate the live manifest once. This is a ten-minute measurement that retires an L-D-shaped
   ambiguity permanently.
3. **Can W-MUR reach `ParticleProcessMaterial` at all?** §3.2 proves the *extension* cannot. It does
   not prove the *wire* cannot — `node-modify` with the ResourceRef shape might. **Check:** one call,
   `{"ProcessMaterial":{"instanceId":0,"resourcePath":"res://x.tres"}}`, then an independent disk read.
   **This single call decides whether W-MUR has an L7 cell worth running.**
4. **Does Pro's `apply_particle_preset` produce a judgeable effect, or a stub?** README claims fire /
   smoke / sparks presets. L-B says manifests describe existence, not behaviour. **Check:** call it,
   render it at the fixed ARPG camera, look.
5. **Does row 24's `.import` patch survive when `rest_fixer/fix_silhouette` is added and the bone map
   swapped to `sidekick_bone_map.tres`?** The addon omits the key drax's R4 calls mandatory. **Check:**
   patch one Synty clip both ways and run drax's `pose_gate.gd` (head-above-hips, 24 samples).
6. **Does `godot-synty-tools`'s Base-Locomotion fixer actually fix the 121-bone inversion?** It is the
   only tool that names that pack. **Check:** run it on `A_MOD_BL_Walk_F_Masc`, then the pose gate —
   drax's failing row is `head y −1.628 … −1.315`, so the pass/fail is unambiguous.
7. **Do the runtime GDExtensions (YParticles3D, GodotIK) actually load on 4.6.3/arm64?** Archive listing
   shows macOS `.framework` bundles exist; **it does not show the slice architecture.** `lipo -info` on
   the extracted binary settles it in one command.
8. **Does installing an extension change Murzak's `.claude/skills` write set (T6)?** Fingerprint the
   directory before and after.
9. **Which prebuilt effects in GODOT-VFX-LIBRARY survive the accumulator lockout?** L7-V established
   **SDFGI is the accumulator and glow is innocent.** A third-party effect could reintroduce a temporal
   accumulator (trails with feedback, screen-reading shaders). **Check:** double-render each candidate
   effect and `framediff`. Cheap, and it is a property of the asset, not the method.
10. **Is `com.IvanMurzak.GameDev.MCP.Server 9.2.2` (nuget, current) behaviourally different from the
    lab's 9.2.0?** And the core addon is now **v0.20.0** (published 2026-07-26) against the lab's
    **0.19.1**. **L-C says re-read every lap.** Two version bumps have landed under the lab since L3.

---

## §7 — Source list

**Read locally**
- `agentic_orchestration/drax/notes/2026-07-24-tcp-l3-murzak-standup-run-report.md`
- `agentic_orchestration/drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md`
- `agentic_orchestration/drax/notes/2026-07-25-tcp-l7v-vfx-arrival-report.md`
- `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md` (grepped: L-C, L-D,
  L-J, Q46, "extension family", "Godot-AI-Particles")

**NOT read — declared**
- Anything under `~/Games/mcp-lab/` (forbidden ground this run), including
  `evidence/extension_catalog_summary.txt`. **The 58-vs-63 discrepancy in §3.1 is a consequence of that
  boundary and I am naming it rather than hiding it.**

**Registries + APIs queried 2026-07-26**
- NuGet search index — `azuresearch-usnc.nuget.org/query?q=Godot-AI` and `?q=Murzak`
- Godot Asset Library API — `godotengine.org/asset-library/api/asset` (17 filter terms; per-asset detail
  for 27 ids). All `download_commit` SHAs in this document come from that API.
- GitHub REST via `gh` — repo metadata, releases, tags, contents, README, and issue search for 40+ repos
- npm registry — `@gltf-transform/cli`, `gltfpack`, `godot-mcp-pro` (absent)
- Homebrew API — `blender` cask 5.2.0
- `docs.godotengine.org` stable class index — existence checks for `RetargetModifier3D`,
  `SkeletonModifier3D`, `BoneMap`, `SkeletonIK3D`, `SpringBoneSimulator3D`, `LookAtModifier3D`

**Source read directly (cloned to scratch, never built or executed)**
- `IvanMurzak/Godot-AI-Particles` @ `881145cd` — all 11 `.cs`, `.csproj`, `.props`, CI matrix, e2e JSON
- `IvanMurzak/Godot-AI-Animation` @ HEAD — README tool table, e2e JSON, CI
- `KarnesTH/mixamo-animation-batcher` @ HEAD — `batcher.gd` (312 lines), `sample_bone_map.tres`
- `youichi-uda/godot-mcp-pro` @ HEAD — `plugin.cfg`, `websocket_server.gd`, `LICENSE`, 35 `.gd` grepped

**Primary vs secondary.** Everything load-bearing in §3 is **primary** — package source, `.csproj`,
CI workflow YAML, `plugin.cfg`, licence files. Version/licence/maintenance metadata is **primary**
(registry APIs). Godot-4.6 compatibility for Layer-1 rows is **secondary at best** — an Asset Library
`godot_version` field and a README claim are self-reported, and I have marked which rows have CI or an
explicit test claim behind them and which have only recency.

---

**Signed:** legolas, 2026-07-26. Read-only throughout. Nothing installed, nothing executed, nothing
under `~/Games/mcp-lab/` touched.

---

## VERDICT column — PC-VERDICT cell (2026-07-28) · **revised R2 (2026-07-28)**

**Status:** COMPLETE (R2)

**Cell:** PC-VERDICT (task #7) · **Run:** PROVISION-CAL · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Author:** legolas · **Boundary law:** LOADS? / REACHES?, **never BETTER.** Nothing below ranks a row.

**Revision R2 (2026-07-28, rider PC-VERDICT-R2).** The six rows this cell originally recorded as
`EXCLUDED(no-positive-control on <instrument>)` — 18 and 41–45 — now carry **measured** verdicts.
Matt authorised host provisioning (charter §8 **R-PC-10**), drax executed **PC-L3-INSTALL**
(`agentic_orchestration/drax/notes/2026-07-28-provision-cal-l3-install.md`, commit `eaebe49f`), and
every Layer-3 binary was installed and probed. The instrument gap that forced the exclusions is
**closed**; the exclusions are withdrawn on evidence, not re-argued. Everything else in this section
is unchanged from R1 except the tallies, which are recomputed below, and one added contradiction-log
entry (#13). §1 remains byte-frozen.

### How this is recorded, and why it is a separate table

The §1 menu table already carries nine columns. Adding a tenth would break it on any reasonable width,
so **the VERDICT is recorded here as a compact `row-id → verdict → evidence` table** rather than as a
column appended to §1. §1 itself is **unmodified** — it is the frozen substrate (charter §1) and this
cell does not edit frozen substrate.

**Enum discipline.** Every value below is drawn verbatim from the charter's closed enum:
`LOADS-CLEAN` · `LOADS-DIRTY(<what>)` · `FAILS-LOAD(<evidence>)` · `REACHES(<probe>)` ·
`REACHES-NOT(<probe>)` · `EXCLUDED(<reason>)` · `GATED-Q46`.

**Two axes, stated rather than collapsed.** The charter's T-1 asks for one verdict per row. The
battery measured two independent questions on some rows — *does it load* and *does it reach its named
target surface* — and they do not always agree (rows 2 and 3 load and cannot reach; row 22 loads
clean and does not move the number it was put on the menu to move). Where a row carries a measured
reach, the cell shows **the load verdict, then the reach verdict, joined by ` · `** — both drawn from
the same closed enum. Collapsing them to one value would destroy the finding. This is the convention
drax's own tier notes used; it is adopted here rather than re-invented.

**`REACHES-PARTIAL` is not in the enum and is not used.** PC-T3 recorded row 17 as
`REACHES-PARTIAL`; under charter law that resolves here into the two in-enum verdicts its own
measurement supports — `REACHES(<what did>)` · `REACHES-NOT(<what did not>)`.

**Evidence tags:** `[W1A]` PC-W1-A · `[W1B]` PC-W1-B · `[T12]` PC-T12 · `[T3]` PC-T3 · `[T4]` PC-T4 ·
`[L3I]` PC-L3-INSTALL (R2) · `[charter §N]`. Every tier note is committed; every verdict below traces
to one.

**`GATED-Q46`: zero rows.** Q46 was ruled **LOCAL-ONLY** mid-run (Matt, charter §6 R-PC-6) and its
verification clause was **discharged** by PC-T4's packet-quiet PASS (390 polls / 90 s, 9 sockets, 0
external). Tier 4 then executed in full. No row's evidence failed to fire because of the gate, so no
row retains `GATED-Q46`.

### The 45 verdicts

| # | Row | **VERDICT** | Evidence |
|---|---|---|---|
| 1 | Compositor Lens Effects | `LOADS-CLEAN` | Instantiates as a real `CompositorEffect`, attaches to a `Compositor` (`effects=1`), GLSL present; structural accumulator scan clean. Honest limit: no shippable `.tscn`, so check-9 rests on the structural detector alone `[T12 §3.1]` |
| 2 | GODOT-VFX-LIBRARY | `LOADS-DIRTY(uid-duplicate + screen-read shader)` · `REACHES-NOT(3D surface — 0/32 effect scenes contain any Node3D; 0/24 shaders are spatial)` | 32/32 effects paused-delta 0 at settle 90 **and** settle 4. Census: 34 CPUParticles2D, 1 GPUParticles2D, zero `*3D` types. Looked at at the fixed ARPG camera: a hard-pixel smear pinned to the canvas origin. Dirt: UID duplicate `vfx_test.tscn`/`vfx_demo.tscn`; `shaders/water.gdshader` declares and samples `hint_screen_texture` `[T12 §3.2, G1, G12]` |
| 3 | Godot Projectile Engine | `LOADS-DIRTY(requires-plugin-enable; autoload registers by UID)` · `REACHES-NOT(3D surface — zero *3D types anywhere in the addon)` | Enabled + reimported: `ProjectileEngine exists=true script=OK instantiable=true`. First-pass `LOAD-NULL` was an incomplete install, not the row failing (L-N). Autoload written as `*uid://bcvs3q3df6ql6`, which does not resolve under `--script` — `ERROR: Unrecognized UID` on every headless run `[T12 §3.3, G9]` |
| 4 | Godot Shaders Library | `LOADS-DIRTY(network-by-design)` | R-PC-5 **discharged**. Installed and probed in its own project, after all other work, outside every timed measurement. 4/4 assertions pass on 4.6.3. **Three** hosts, not the one the menu names, and `api.github.com/.../releases/latest` fires on a 2-second timer at plugin load with no user action. Measured quiescent in headless (cache dir never created over 12 s) `[T3 §6, T3-F5]` `[charter §6 R-PC-5]` |
| 5 | godot-4-VFX-assets (GDQuest) | `EXCLUDED(licence)` | CC-BY-NC-SA-4.0 art in a project with shipping ambitions. Not installed, not downloaded, not executed. Menu §2.7 already listed it reference-only `[T12 §3.8]` `[charter §5 folded lean]` |
| 6 | Godot-particle-and-vfx-textures | `LOADS-DIRTY(blend-source-blocks-the-import-pass)` | The row aborts the **whole project's** import pass on a Blender-less machine: **0/134** `.png.import` sidecars generated as shipped vs **134/134** with `materials/blend_file/` excluded. Post-exclusion 82/82 textures load at eight distinct sizes; structural scan clean `[T12 §3.4, G4]` |
| 7 | proton_trail | `LOADS-DIRTY(class_name collision on Point — row 10 publishes it into the global namespace)` | Genuinely 3D (`Node3D`/`MeshInstance3D`/`Camera3D`); demo scene instantiates. Co-installed with row 10 it emits `Parse Error: Class "Point" hides a global script class` on every load. The fault sits with row 10 (a global `class_name` landgrab), not here. Accumulator clean `[T12 §3.5, G3]` |
| 8 | Shader Previewer | `LOADS-CLEAN` | Compiles, enables, live control `ShaderPreviewer` found in the editor tree (4.6 `EditorDock` API) `[T3 §2.2]` |
| 9 | Shader-Lib | `LOADS-CLEAN` | 5/5 sampled `VisualShaderNode*` classes registered. **It has no `plugin.cfg` at all** — it cannot be enabled or disabled; it is present the moment the folder exists, and a headless GDScript pass can instantiate its nodes. The menu's `EW=WIRE` is measurably narrow `[T3 §2.3, T3-F2]` |
| 10 | TrailRenderer | `LOADS-DIRTY(C# samples unloadable on the STANDARD build; publishes class_name Point into the global namespace)` | GDScript runtime compiles and `TrailRenderer.new()` instantiates as a `Node3D` — capability present. Both sample scenes `LOAD-NULL`: 5 `.cs` files, and this is a non-Mono build. Accumulator clean `[T12 §3.6, G3, G5]` |
| 11 | UniParticles3D | `LOADS-CLEAN` | `class_name UniParticles3D extends Node3D` compiles and instantiates; **10/10 shaders are `shader_type spatial`** — it does reach the 3D surface, in the same "L7 particle library" brief where rows 2 and 3 do not. Paused-delta 0 both legs. Structural-scan `SubViewportContainer` hit is a false positive (editor-dock string compare) `[T12 §3.7]` |
| 12 | Vaportrail | `FAILS-LOAD(manifest path ≠ shipped framework name — the bundle ships as bin/macos/macos.framework/ while the manifest declares libvaportrail.macos.template_debug.framework; ClassDB.class_exists VaporTrail = false)` | Re-tiered from Tier 1 by drax — it ships a `.gdextension` + compiled framework, so the menu's "pure runtime node" classification is wrong. `lipo`: `x86_64 arm64` — **architecture is not the problem.** L-N: row 21 registers 4/4 classes in the same process, same run `[T12 §4.3, §4.0, G2]` |
| 13 | vkaParticleTool | `LOADS-CLEAN` | Compiles, enables, live control `ParticleControlPanel` in `CONTAINER_INSPECTOR_BOTTOM` `[T3 §2.2]` |
| 14 | YParticles3D | `FAILS-LOAD(declared macos.debug slice absent from the shipped archive — it ships editor.single + template_release.single and no template_debug; ClassDB.class_exists YParticles3D = false)` | `lipo`: both shipped frameworks are `x86_64 arm64`. **A packaging defect, not an architecture defect** — `lipo` alone would have passed this row. Every editor and `--script` run is a debug context. L-N control: row 21 `[T12 §4.2, §4.0, G2]` |
| 15 | Advanced Model Import (4.6) | `LOADS-CLEAN` | Compiles, enables, dock tab `Advanced Model Import` + control `BulkImporterDock` found live `[T3 §2.2]` |
| 16 | Animation Library Unique-ifier | `LOADS-CLEAN` | Compiles, enables; registers via `add_inspector_plugin` — no tree surface to find, and none claimed `[T3 §2.2]` |
| 17 | Animation Property Tracks – Batch Modification | `LOADS-DIRTY(zh-CN-only UI)` · `REACHES(per-animation loop-mode editing on a real Synty scene)` · `REACHES-NOT(per-track property edits — 0 of 95 tracks reachable; it counts TYPE_VALUE tracks only and the Synty corpus is 100% TYPE_POSITION_3D / TYPE_ROTATION_3D)` | Loads, docks, discovers real `AnimationPlayer`s, every call executes without error. Tab title `动画属性轨道批量修改`; no English string table, zero `tr()` calls, and an `_on_language_selected()` whose body is `pass`. The menu's "bulk edits across 3,386 clips" is half true `[T3 §2.5, §5.3, T3-F3, T3-F13]` |
| 18 | fix_synty_anim_to_godot_with_autorigpro | `LOADS-CLEAN` · `REACHES-NOT(arp-operator-absent — bpy.ops.arp.build_bones_list() does not resolve; Auto-Rig Pro is a paid addon and is not installed)` | **R2 — measured.** Installed into Blender's user extension repo and enabled headless on **Blender 5.2** despite the manifest declaring only `blender_version_min 4.2.0`: `enable=OK`, the operator `…retarget` polls `True`, the panel registers, the scene properties install. Reach fails at the **call**, not at the attribute — `hasattr(bpy.ops.arp, …)` returns `True` for anything (`bpy.ops` sub-namespaces are lazily constructed), and only the invocation resolves it: `AttributeError: Calling operator "bpy.ops.arp.build_bones_list" error, could not be found`. Row 41 is now satisfied, so the menu's own "cannot run without row 41" blocker is cleared `[L3I §7]` |
| 19 | Godot4-OpenAnimationLibraries | `EXCLUDED(licence)` | No licence declared = all rights reserved. Not installed, not downloaded, not executed `[T12 §3.8]` `[charter §5 folded lean]` |
| 20 | GodotHumanoidRetargetPlugin (D3ZAX) | `EXCLUDED(licence)` | No licence declared. Not installed, not downloaded, not executed. Its stated purpose (retarget across different rest poses) remains the menu's highest-relevance / lowest-confidence row and is now untested for a licence reason, not a technical one `[T12 §3.8]` |
| 21 | GodotIK (monxa) | `LOADS-CLEAN` | 4/4 declared classes register and instantiate on 4.6.3/arm64 — `GodotIK` (parent `SkeletonModifier3D`), `GodotIKEffector`, `GodotIKConstraint`, `GodotIKRoot`. **This row is the Tier-2 L-N control**: it proves the GDExtension load path works in the same process and the same run that rows 12 and 14 fail in `[T12 §4.1]` |
| 22 | godot-synty-tools (hlarsen) | `LOADS-CLEAN` · `REACHES-NOT(check 6 — the Base-Locomotion fixer does not resolve the 121-bone inversion: output gates at head y −1.615…−1.319 against a −1.628…−1.315 baseline, on both character conventions)` | Compiles, enables, live tool-menu item `Godot Synty Tools`. `process()` returned OK in 0.4 s and emitted its full library tree. Input provenance verified byte-identical to the clip that produced the charter's baseline. It never sets `retarget/remove_tracks/unmapped_bones` — which is what actually dissolves the inversion. Ships 16 correct Synty per-pack BoneMaps, independent of this verdict `[T3 §4, T3-F11, T3-F14]` |
| 23 | Import Replacer | `LOADS-CLEAN` | Compiles, enables; registers via `add_scene_post_import_plugin` — no tree surface `[T3 §2.2]` |
| 24 | Mixamo Animation Batcher | `LOADS-CLEAN` · `REACHES(check 5 — the stock patch FAILS the pose gate; the amended patch PASSES)` | Live tool-menu item `Mixamo Animation Batcher...`. Its own `_apply_import_settings()` was **called, not re-implemented**, across five single-variable configs. Stock: its `sample_bone_map.tres` matches **0/34** Synty bone names case-sensitively, so the retarget binds nothing and its own `remove_tracks/unmapped_bones` then deletes every track (91→0, 122→0). Amended (bone-map swap): PASS. **Only the bone-map swap is load-bearing**; `fix_silhouette` is amplitude, not shape. Both menu §2.1 gaps confirmed exactly as written `[T3 §3, T3-F6, T3-F7]` |
| 25 | Modifier Animation Baker | `LOADS-CLEAN` · `REACHES(dialog + bake kernel execute; declines FBX-imported libraries by design — needs a clip extracted to .res first)` | Live tool-menu item. `_make_dialog()` builds, `_bake_keys()` runs. Its two hard preconditions (a RESET animation; a non-`.import`-backed AnimationLibrary) are both absent from Synty content as imported, and it refuses with a clear message. A prerequisite, not a defect — and invisible from the menu row `[T3 §5.2, T3-F12]` |
| 26 | Skeleton Poser (3D) | `LOADS-DIRTY(ships a UID duplicate in its own example scene)` | Compiles, enables, three live controls found. Duplicate: `example_scene/pose_collection_snapshot.tres` vs `lizbot_poses_from_rest.tres` — the 6th standing import-warning source. A near-miss recorded rather than smoothed: its apparently-broken `add_autoload_singleton` path is **commented out** Godot template boilerplate and no verdict rests on it `[T3 §2.6, T3-F10]` |
| 27 | synty-godot-converter (DeniedWorks) | `EXCLUDED(licence)` | No licence declared. Not installed, not downloaded, not executed `[T12 §3.8]` |
| 28 | Unidot Importer | `LOADS-DIRTY(deps-not-shipped-installed)` | **It loads on 4.6.3 despite self-declaring 4.0–4.2** — compiles, enables, 3/3 live `add_tool_menu_item` calls land (the other two are commented out upstream). The dirt is what it needs and does not ship installed: two sibling addons (`vrm`, `Godot-MToon-Shader`) plus FBX2glTF (row 42, x86_64-only) configured in Editor Settings `[T3 §2.4]` |
| 29 | Unused Bone Track Remover | `LOADS-CLEAN` · `REACHES(46 of 46 unmapped-bone tracks removed from a real Synty clip)` | `_can_handle(AnimationPlayer) -> true`; 139 tracks → 93, and the removed set is precisely the `*Proc_*` / `upperarm_proportion_*` family named as the 121-bone pack's un-hostable leftovers. AL declares Godot 4.0; runs on 4.6.3 with no deprecation warning. Scope note: one animation at a time via the inspector, no batch mode — and per T3-F4 this is **not** equivalent to `remove_tracks/unmapped_bones` at import `[T3 §5.1, §4bis]` |
| 30 | `…MCP.Animation` | `LOADS-CLEAN` | Compiles into the consumer and registers **7** live tools (`-add-track` `-create` `-defaults` `-get` `-insert-key` `-library-add` `-player-create`) on `4.6.3.stable.mono`. README count 7 = live 7. No functional probe fired against this family; no reach verdict is claimed `[T4 §4.3, §4.5]` |
| 31 | `…MCP.Beehave` | `LOADS-CLEAN` | Registers **6** live tools, not the README's 5 (`-add-decorator` is new) and `beehave-create-tree` does not exist — it is `beehave-tree-create`. Wraps a third-party addon we do not have; no probe fired `[T4 §4.5]` |
| 32 | `…MCP.CSG` | `LOADS-CLEAN` | Registers **7** live tools, not the README's 6 (`csg-defaults` is new) `[T4 §4.5]` |
| 33 | `…MCP.Dialogic` | `LOADS-CLEAN` | Registers **5** live tools; two README names are wrong (`dialogic-add-event` → `-timeline-add-text`; `dialogic-get-timeline` → `-get`). Wraps a third-party addon we do not have `[T4 §4.5]` |
| 34 | `…MCP.GridMap` | `LOADS-CLEAN` | Registers **7** live tools; README count matches `[T4 §4.5]` |
| 35 | `…MCP.Navigation` | `LOADS-CLEAN` | Registers **7** live tools, not the README's 6 (`navigation-defaults` is new) `[T4 §4.5]` |
| 36 | `…MCP.Particles` | `LOADS-CLEAN` · `REACHES(particles-create emits a real GPUParticles3D that persists to disk with its scalars — amount=64, lifetime=1.5)` · `REACHES-NOT(ParticleProcessMaterial — none of the 63 extension tools reaches it; check 3 was satisfied by the CORE node-modify call, not by this row)` | Registers **5** live tools; parameter surface confirmed unchanged from the menu §3.2 source read. The independent disk read of `pct4_check3.tscn` shows the node this row created carrying `process_material = ExtResource(...)` **assigned by `node-modify`**. The menu §3.2 consequence stands on the wire `[T4 §4.5, §5.2, §5.3]` `[charter §8]` |
| 37 | `…MCP.PhantomCamera` | `LOADS-CLEAN` | Registers **7** live tools; README count matches. Wraps a third-party addon we do not have; R-6 forbids moving the judge, so no probe was warranted and none fired `[T4 §4.5]` |
| 38 | `…MCP.Terrain3D` | `LOADS-CLEAN` | Registers **6** live tools, not the README's 4 — and **two README-named tools do not exist** (`terrain3d-set-height`, `terrain3d-get-info`), replaced by `-get`, `-set-data-directory`, `-set-material`, `-set-region-size`. Wraps a third-party addon we do not have `[T4 §4.5]` |
| 39 | `…MCP.Tilemap` | `LOADS-CLEAN` | Registers **6** live tools; README count matches `[T4 §4.5]` |
| 40 | godot-mcp-pro extension mechanism | `EXCLUDED(the mechanism does not exist — there is nothing to provision)` | The menu recorded this as a negative finding held as a row so it could not be lost. PC-T4 confirmed the ceiling **on the wire**: `[MCP] Registered 174 commands`, `tools/list` over stdio returns **175**, and the manifest, `plugin.cfg` description and wire all agree at 175. No plugin API, no extension registry, nothing on npm. **Precision:** the *Pro tool surface* was separately probed under check 4 and reaches (see the note below the table) — that is W-PRO the contestant, which is not a menu row `[T4 §7.1]` `[menu §3.3]` |
| 41 | Blender 5.2.0 (headless) | `LOADS-CLEAN` · `REACHES(headless glb import — 3 objects / 2 meshes / 1 armature / 88 bones read out of a PC-T3 emit in 0.05 s)` | **R2 — measured.** `brew install --cask blender` served **exactly the menu pin 5.2.0 LTS** (hash `fbe6228777e7`, native arm64 on this M2); `blender --version` exit 0. `blender -b -P` imported `pct3/proj/emitted/lib_a.glb` and reported its contents. The PC-T12 evidence I declined to convert into a verdict in R1 remains true and remains a **different fact**: installing the cask does not populate Godot's `filesystem/import/blender/blender_path`, so that error is still live and still un-probed. R1's refusal was correct — the fact it withheld was Godot-side `[L3I §2]` `[T12 §3.4]` |
| 42 | FBX2glTF (godotengine fork) | `LOADS-DIRTY(rosetta — x86_64-only binary on an arm64 host)` · `REACHES(SK_Chr_Werewolf_01.fbx → werewolf01.glb, 1,291,784 B, 0.126 s wall)` | **R2 — measured.** The menu's arm64 claim is now settled by instrument rather than by release-page reading: `lipo -info` → `Non-fat file: … x86_64`, and **no arm64 artefact exists in either fork** (godotengine v0.13.1; facebookincubator upstream v0.9.7 @ 2019). Rosetta 2 is installed and functional here (`oahd` running, `arch -x86_64` succeeds), so a runnable macOS binary does exist — this is `LOADS-DIRTY`, explicitly **not** `FAILS-LOAD(no-macos-binary)`. Banked side-finding: row 44's instrument reports **1 error** on this output (`/meshes/0/primitives/0/attributes/TANGENT … not of unit length`) and a 52-joint skin against the Godot emits' 88 `[L3I §6, §6.1, §1.2]` |
| 43 | glTF-Transform CLI | `LOADS-CLEAN` · `REACHES(inspect on a PC-T3 emitted .glb — full report captured)` | **R2 — measured.** Installed at **exactly the menu pin `@gltf-transform/cli@4.4.2`**; `--version` → 4.4.2. `gltf-transform inspect lib_a.glb` exit 0: generator `Godot Engine v4.6.3.stable`, `extensionsUsed GODOT_single_root`, 8,424 vertices, 1 material, no textures, no animations. **Provisioning caveat that travels with this row and with 44/45:** the host's global npm prefix is root-owned (`/usr/local`, `root:wheel`), so all npm installs went to a confined prefix at `/Users/admin/Games/mcp-lab/pcl3/npm-global/bin/`. A consuming cell that types `gltf-transform` with no PATH change gets `command not found` `[L3I §3, §1.1]` |
| 44 | glTF-Validator (Khronos) | `LOADS-DIRTY(rosetta — x86_64-only binary on an arm64 host)` · `REACHES(validate — all eight PC-T3 emits, 0 errors each)` | **R2 — measured, and two menu facts corrected.** (a) **The npm route cannot satisfy this row at all:** `gltf-validator@2.0.0-dev.3.10` resolves and installs but has **`bin: null`** — it is a dart2js library with a JS API, and no `gltf-validator-cli` exists on the registry. This is a **release-binary** row, not an npm row, and my R1 instrument label ("npm CLI") was wrong. (b) The menu pins `commit HEAD @ 2025-12-30`; the newest *published* release is `2.0.0-dev.3.10 @ 2024-10-22`, over a year older — a HEAD pin implies a Dart build from source, which was not done. What is installed and probed is the release binary, `lipo`-confirmed x86_64-only with **no arm64 artefact in any of the 8 published releases**. ★ Its report on our own corpus is the run's highest-value banked finding — 0 errors in all eight emits, and one identical warning in every file: `NODE_SKINNED_MESH_NON_ROOT` `[L3I §5, §5.1]` |
| 45 | gltfpack / meshoptimizer | `LOADS-CLEAN` · `REACHES(pack lib_a.glb 1,144,920 B → 231,776 B; output re-validates at 0 errors)` | **R2 — measured.** No brew formula exists under either name (`brew search gltf` returns only `glfw` and `gltfquicklook`), so the npm route was used at **exactly the menu pin `gltfpack@1.2.0`**. Transform facts, recorded as facts about the transform and not as quality: the defaults are lossy on this asset — `maxUVs` 4 → **0**, `maxInfluences` 8 → **4**, `maxAttributes` 12 → 5, vertices 8,424 → 7,150, and the output declares `KHR_mesh_quantization` as required. Re-validated with row 44's instrument: 0 errors, 2 warnings (the input already carried 1) `[L3I §4]` |

### Tally (R2 — recomputed)

**Load axis — every one of the 45 rows carries exactly one load-axis verdict:**

| Verdict | N (R2) | N (R1) | Rows |
|---|---:|---:|---|
| `LOADS-CLEAN` | **27** | 23 | 1 · 8 · 9 · 11 · 13 · 15 · 16 · **18** · 21 · 22 · 23 · 24 · 25 · 29 · 30 · 31 · 32 · 33 · 34 · 35 · 36 · 37 · 38 · 39 · **41** · **43** · **45** |
| `LOADS-DIRTY` | **11** | 9 | 2 · 3 · 4 · 6 · 7 · 10 · 17 · 26 · 28 · **42** · **44** |
| `FAILS-LOAD` | **2** | 2 | 12 · 14 |
| `EXCLUDED` | **5** | 11 | 5 · 19 · 20 · 27 · 40 |
| `GATED-Q46` | **0** | 0 | — (ruled LOCAL-ONLY; verification discharged by the packet-quiet PASS) |

**The recount, stated precisely.** Six rows left `EXCLUDED` (18, 41, 42, 43, 44, 45) and **all six**
took a measured load verdict — **four** into `LOADS-CLEAN` (18, 41, 43, 45) and **two** into
`LOADS-DIRTY(rosetta)` (42, 44). 27 + 11 + 2 + 5 = 45. Row 18 is one of the four that **load clean**;
its `REACHES-NOT` sits on the reach axis and does not move the load count. (The rider's expectation of
"five" entering the load verdicts does not survive the recount: it matches the **reach** side, where
five of the six reach and row 18 does not.)

The remaining 5 `EXCLUDED` decompose as **4 on licence** (5, 19, 20, 27 — charter §5 folded lean) and
**1 on non-existence** (40). **Zero rows are now excluded on L-N.** The L-N exclusions were never a
property of the rows; they were a property of the host, and the host changed.

**Reach axis — 14 rows carry a measured reach verdict; the other 31 had no reach probe and none is claimed:**

| Verdict | N (R2) | N (R1) | Rows |
|---|---:|---:|---|
| `REACHES` | **10** | 5 | 17 (per-animation loop mode) · 24 (check 5, amended) · 25 (bake kernel) · 29 (46/46) · 36 (`particles-create`) · **41** (headless glb import) · **42** (FBX → glb) · **43** (inspect) · **44** (validate ×8) · **45** (pack + re-validate) |
| `REACHES-NOT` | **6** | 5 | 2 (3D surface) · 3 (3D surface) · **18** (arp operator absent) · 17 (per-track edits) · 22 (check 6) · 36 (`ParticleProcessMaterial`) |

Rows 17 and 36 appear on both lines: each has one probe that reaches and a distinct probe that does
not. That is the enum working, not a contradiction.

### ~~Unresolvable rows — 6, and exactly what each would need~~ → **RESOLVED IN R2. Zero remain.**

> **R2 annotation (2026-07-28).** All six rows below have been struck. They resolved **via host
> provisioning** — Matt authorised the installs (charter §8 **R-PC-10**) and drax's PC-L3-INSTALL
> cleared every instrument and fired every probe — **not** via the instrument I lacked at R1 and not
> by any re-reading of the R1 evidence. The R1 diagnosis therefore stands exactly as written: this was
> **a gap in tier coverage, not a property of the rows**, and the fix was a host mutation, not a
> verdict revision. The "What would settle it" column is left in place as the record of what was
> asked for; the added column records what was actually done. Live verdicts are in the table above.

Under **L-N** (clear the instrument before recording a NO) these six were recorded at R1 as
`EXCLUDED(no-positive-control on <instrument>)` rather than as a manufactured `FAILS-LOAD`. The
charter's four tiers (§3) address pure resources, runtime GDExtensions, editor-only plugins and the
Murzak/Pro family — **no tier owned Layer 3, the external host and CLI tools.** Five of the six were
the whole of Layer 3.

| # | Row | ~~Instrument never cleared~~ | ~~What would settle it~~ | **How it actually resolved (R2)** |
|---|---|---|---|---|
| 18 | ~~fix_synty_anim_to_godot_with_autorigpro~~ | ~~Blender-extension host~~ | ~~Blender present + the paid Auto-Rig Pro dependency resolved, then the extension installed and run on one Synty clip. Note the menu's own field: it cannot run without row 41~~ | Instrument cleared: extension installed + enabled + registered on Blender 5.2 → `LOADS-CLEAN`. Reach still fails, but now **as a measurement**: `REACHES-NOT(arp-operator-absent)` `[L3I §7]` |
| 41 | ~~Blender 5.2.0 (headless)~~ | ~~CLI invocation~~ | ~~`blender --version` (or the cask query), then one headless `--background --python-expr` round-trip. A positive control the same instrument can also fail~~ | Exactly this, executed: cask install → `--version` exit 0 → headless `-b -P` glTF import `[L3I §2]` |
| 42 | ~~FBX2glTF~~ | ~~binary execution~~ | ~~Fetch the pinned release, `lipo -info` the macOS artefact (settles the arm64 claim by measurement rather than by release-page reading), then one conversion~~ | Exactly this, executed: `lipo` confirms x86_64-only in both forks; conversion ran under Rosetta `[L3I §6]` |
| 43 | ~~glTF-Transform CLI~~ | ~~npm CLI invocation~~ | ~~`npx @gltf-transform/cli@4.4.2 inspect` on one of PC-T3's emitted `lib_*.glb` files~~ | Exactly this corpus, executed at the exact pin `[L3I §3]` |
| 44 | ~~glTF-Validator~~ | ~~npm CLI invocation~~ | ~~Same corpus: validate one emitted `.glb` and read the conformance report~~ | Resolved, **but not by the named route** — the npm package is a library (`bin: null`). Release binary used; all eight emits validated `[L3I §5]` |
| 45 | ~~gltfpack / meshoptimizer~~ | ~~npm CLI invocation~~ | ~~`gltfpack` one emitted `.glb` and confirm it re-loads~~ | Exactly this, executed at the exact pin; output re-validated at 0 errors `[L3I §4]` |

R1's closing prediction held: rows 43–45 shared a ready corpus at
`/Users/admin/Games/mcp-lab/pct3/proj/emitted/`, and **a single Layer-3 cell closed all five Layer-3
rows plus row 18** against artefacts that already existed.

**Row 18's remaining gate is a purchase, not a measurement.** Its only outstanding dependency is the
**Auto-Rig Pro** commercial Blender-Market addon — a Matt-queue purchase decision. No further probe
can move this row; row 41, its other blocker, is now satisfied. Nothing here is `EXCLUDED` and nothing
here awaits an instrument.

### One precision the table cannot carry: W-PRO is not row 40

Row 40 is *the Pro extension mechanism*, and it verdicts `EXCLUDED` because that mechanism does not
exist. **Pro's own tool surface is a different object and it was measured.** Under check 4, PC-T4
called `apply_particle_preset` three times (11/11 calls OK across two plans) and an independent disk
read of each saved `.tscn` shows it building and assigning a full `ParticleProcessMaterial` **plus** a
`Gradient` / `GradientTexture1D` colour ramp **in one call** — i.e. `REACHES`, measured, discharging
the menu §3.3 "documented, not measured" caveat. That verdict attaches to W-PRO the contestant, which
has no row on this menu, so it is recorded here rather than in the table. **The images themselves are
Matt's to judge and are not verdicted by anyone** — and per **M-EYE** (charter §8) the Matt-eye
checkpoint is owed in MOTION, not as the captured stills.

### Where the battery contradicted this document's own prior expectations

Recorded as fact, in the run's boundary (LOADS? / REACHES?), with no ranking implied.

1. **★ The menu called row 2 "the single highest-leverage L7 row." It is 2D.** Zero `Node3D` in 32
   effect scenes; 0/24 shaders spatial. Row 3, listed "L7 cast" with `EW=ALL`, is likewise 2D-only.
   The root cause is this document's own: **`EW=ALL` read loadability as reach.** The premise was
   right (all three cells would load these `.tscn` files equally) and the conclusion did not follow
   (all three would equally load something that cannot appear in a 3D scene). Conductor ruling R-PC-9
   follows from it `[T12 G1]` `[charter §8]`.
2. **★ Check 2 settles at 63, not 58 — and the READMEs were the wrong count.** Worse than a miscount:
   **three README-named tools do not exist** (`terrain3d-set-height`, `terrain3d-get-info`,
   `beehave-create-tree`) and two more are renamed. §3.1's tool tables were built from those READMEs.
   A plan authored from this document's §3.1 would have called tools that are not there `[T4 §4.5]`.
3. **★ The family's headline compat risk did not fire.** §3.1 flagged "no 4.6 leg in any of the ten"
   as *"a real, named, unresolved compat risk … it applies to the whole family at once."* Measured:
   **10/10 compile and register on 4.6.3.stable.mono.** The risk was correctly named and did not
   materialise `[T4 §4.3]`.
4. **Row 28 loads on 4.6.3 despite this document recording its 4.6 evidence as NEGATIVE** (README:
   "4.0 through 4.2"). A self-declared ceiling is not a measured one `[T3 §2.4]`.
5. **Row 24's stock patch fails worse than §2.1 predicted.** §2.1 forecast "a technically-retargeted,
   silhouette-wrong result." Measured: **zero-track animations** (91→0, 122→0) — the bone map matches
   0/34 Synty names case-sensitively, so nothing binds and the addon's own unmapped-track strip then
   deletes everything. And §2.1's recommendation — *"provision as a reference implementation, not as a
   tool"* — is confirmed and understated: the 60 load-bearing lines contain
   `retarget/remove_tracks/unmapped_bones`, the single key that dissolves the 121-bone inversion
   `[T3 §3, T3-F6]`.
6. **Row 12 is mis-tiered in §1.** Listed as a pure runtime node under Layer 1; it ships a
   `.gdextension` + compiled framework and was re-tiered to Tier 2, where it fails `[T12 §4]`.
7. **Row 9's `EW=WIRE` is measurably narrow.** It has no `plugin.cfg`; it cannot be enabled or
   disabled, and a headless GDScript pass can instantiate its nodes without an editor `[T3 T3-F2]`.
8. **Row 4's telemetry field understates the surface.** §2.8 reads "fetches godotshaders.com on
   demand." Measured: **three** hosts, and `api.github.com/.../releases/latest` fires automatically on
   a 2 s timer at plugin load with no user action `[T3 T3-F5]`.
9. **§0's "Five rows have no license at all" does not reconcile.** §5 names three (19, 20, 27); row 40
   carries a blank licence field for a different reason (the thing does not exist). Four at most.
   Charter §5's folded lean inherited the five. Named, not silently corrected — §1 is frozen substrate
   `[T12 G10]`.
10. **Rows 7 and 10 are mutually interfering as shipped**, which no per-row research could have seen:
    installing both breaks row 7's script on every load via a global `class_name Point` landgrab. A
    per-row menu has no column for pairwise interaction `[T12 G3]`.
11. **T6 is larger than §4 filed it.** Predicted "39 `SKILL.md` files, and adding extensions will grow
    that set." Measured **0 → 42 → 105 files, 708 KB, unasked, on by default** — and in
    `reincarnated-godot` that would collide with our own `.claude/` tree `[T4 §6]`.
12. **One correction inbound to my own PC-W1-B source read, from PC-T4's wire capture:**
    `project_path_hash_legacy` **is** sent at v0.20.1 — **six** identity fields observed on the
    handshake, not five. All six went to `localhost`; the ruling is unaffected `[T4 §2.4]`.
13. **★ §1 stars "macos-x86_64 only — no arm64" on row 42 but not on row 44; row 44 is x86_64-only
    too** — in **all 8 published Khronos releases** — and its npm namesake is not the CLI §1's pin
    implies but a dart2js **library** (`bin: null`), so row 44 is a release-binary row that deserves
    the same ★ `[L3I §5]`.

### Provenance and boundary

- Every verdict above is **synthesis from banked, committed evidence**. This cell installed nothing,
  executed nothing, launched no Godot, and touched neither `reincarnated-godot` nor `mcp-lab`. **That
  remains true at R2:** the six revised verdicts are adopted from drax's PC-L3-INSTALL measurements
  (`eaebe49f`), not re-run here. The installs were drax's; the enum conformance is mine.
- The only file modified by this cell is **this one**, and only by the addition of this section. §1
  and §§2–7 are byte-unchanged — **including at R2**, where the two row-44 menu-fact corrections and
  contradiction #13 are recorded here rather than applied to the frozen substrate.
- **No verdict expresses a preference.** Where a row loads and does not reach, both facts are
  recorded and neither is scored. BETTER is the L7 race's question, not this run's. Nothing in the R2
  Layer-3 evidence — the pack ratio, the lossy defaults, the tangent error, the 0-error corpus — is a
  quality judgement of any tool; each is a measured property of a transform.

**Status:** COMPLETE (R1 2026-07-28) · **REVISED R2 2026-07-28** — six L-N exclusions withdrawn on
measurement; load axis now 27 / 11 / 2 / 5 / 0; zero unresolvable rows remain.

**Signed:** legolas, 2026-07-28, cell PC-VERDICT · revised, cell PC-VERDICT-R2.
