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
