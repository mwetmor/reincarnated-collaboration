# Synty Slice Verification — Predictions #2 (UV-region separability) + #3 (accent-rig sockets)

**Date:** 2026-06-17
**Author:** galadriel (visual-perception + UX-similarity steward)
**Status:** v1 — empirical verdict on the gear-spec resumption gate
**Authority:** Matt-authorized read-only asset-inspection task in the Synty gear-substrate workstream; knight-rider orchestrating (hive mode). NO asset modified.
**Answers:** the slice-verification checklist (§ 6.3) and predictions #2 + #3 (§ 9) of `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md`. This is the empirical gate that resumes gandalf's deferred design session (§ 4 of that record).
**Companion:** elrond's catalogue work in this same recon dir (`pack-manifest.jsonl`, `full-fbx-variant-manifest.jsonl`, `sidekick-modularity.md`).

---

## 0. TL;DR — the two verdicts

| Prediction | Verdict | Strength |
|---|---|---|
| **#2 — UV-region separability** (per-region recolor via mask) | **YES** | strong, on the Modular Fantasy Heroes pack; **load-bearing CAVEAT** for page-1 named-character packs (§ 3.3) |
| **#3 — accent-rig sockets** (bone-attachment accents) | **YES** | strong; the rig ships a dedicated, named, canonical socket set |

**Both predictions hold.** The "one shader, N palette profiles" lever is real on the modular pack — Synty already ships it themselves (A/B/C palette variants of one UV atlas, plus a per-region RGB mask). The accent-attachment system is real — the rig exposes 12 named attachment sockets (`All_00`..`All_12`) plus 4 cape sockets, and the pack ships standalone accent parts that mount to them.

**The one caveat gandalf must rule on (§ 3.3 below):** the per-region mask scheme is a property of the **Modular Fantasy Heroes** pack, NOT a universal Synty guarantee. Page-1 named-character packs (Adventure, Fantasy Kingdom, Samurai) use a coarser **whole-atlas palette-swap** recolor (no per-region mask). This bifurcates the restyle lever by lane and feeds gandalf's §7.6 StyleProfile output-shape decision directly.

---

## 1. Reference set / what was inspected

- **Modular pack (richest signal):** `/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-modular-fantasy-heroes/Source_Files/`
  - `FBX/ModularCharacters.fbx` (16.6 MB shared rig) — skeleton + socket inspection
  - `FBX/StaticMeshes/` — 720 per-slot part FBX, slot histogram
  - `FBX/MaterialList_PolygonFantasyHeroCharacters.txt` — material/shader assignment
  - `Textures/` — 4 base atlases × A/B/C palette variants + 4 `_Texture_Mask` RGB masks
- **Page-1 downloaded packs:** `~/Games/synty-corpus/fbx/` — Adventure (`1462397`), Fantasy Kingdom (`1485355`), Samurai (`1624702`); FBX listing + texture-scheme inspection via `unzip -l`.

**Tooling:** Blender/assimp/pyassimp were NOT installed and could not be cleanly added; this is a reported gap (§ 5). All verdicts were reached without a mesh-loader by analyzing (a) the mask PNGs with PIL+numpy, (b) binary-FBX plaintext node-name strings for the skeleton/socket graph, (c) the per-slot FBX filename taxonomy, and (d) `unzip -l` listings. The evidence is sufficient and decision-grade; no render was produced (see § 5 caveat).

---

## 2. Prediction #3 — accent-rig sockets: **YES (strong)**

`ModularCharacters.fbx` (the shared rig) exposes a complete humanoid skeleton AND a dedicated, named accent-socket set extracted from the FBX node graph:

**Canonical attachment sockets (Synty `All_NN_` convention):**
```
All_00_HeadCoverings        All_06_Shoulder_Attachment_Left
All_01_Hair                 All_07_Elbow_Attachment_Right
All_02_Head_Attachment      All_08_Elbow_Attachment_Left
All_03_Chest_Attachment     All_09_Hips_Attachment
All_04_Back_Attachment      All_10_Knee_Attachement_Right   [sic — Synty's spelling]
All_05_Shoulder_Attachment_Right   All_11_Knee_Attachement_Left
                            All_12_Extra
Cape_Attachment_01 .. _04   (4 dedicated cape sockets)
```
Plus convenience aliases on the rig: `Head_Attachment`, `Chest_Attachment`, `Back_Attachment`, `Shoulder_Attachment_L/R`, `Elbow_Attachment_L/R`, `Hips_Attachment`, `Knee_Attachment_L/R`.

**Core skeleton joints present** (humanoid, riggable): `Root, Hips, Spine/Neck, Head, Clavicle_L/R, Shoulder_L/R, Elbow_L/R, Hand_L/R` (+ leg chain).

**The sockets are matched by standalone accent parts** in `StaticMeshes/` that mount to them — counts:
- ShoulderAttach L/R: 21 variants each · BackAttachment: 15 · HelmetAttachment: 13 · HipsAttachment: 12 · KneeAttach L/R: 11 each · ElbowAttach L/R: 6 each.

**Verdict:** the rig supports bone-attachment accents at exactly the silhouette-breaking points gandalf named (shoulder, back, helmet, knee, elbow, hips) plus cape. This satisfies § 3.6 ("accents SECOND — the only torso/legs silhouette-breaker") and resolves the §7.2 rocket acceptance hook ("build the accent-attachment system IF § 4 step 2 confirms rig sockets" → **confirmed, build it**). Maps cleanly to a Godot `BoneAttachment3D` / UE `SocketName` per the L4 neutrality principle.

---

## 3. Prediction #2 — UV-region separability: **YES (strong, with a lane caveat)**

### 3.1 The mask scheme (the lever)

The Modular Fantasy Heroes pack ships 4 RGB `_Texture_Mask` textures (1024×1024). Binary-snapping each pixel per-channel and tallying across all four masks yields a clean **discrete 5-key region palette** — the standard Synty per-region mask scheme:

| Region key | RGB | channels | coverage (all masks) |
|---|---|---|---|
| WHITE | (255,255,255) | R+G+B | 86.46% |
| CYAN | (0,255,255) | G+B | 11.08% |
| BLUE | (0,0,255) | B | 1.72% |
| YELLOW | (255,255,0) | R+G | 0.43% |
| MAGENTA | (255,0,255) | R+B | 0.31% |

These are pure RGB-corner keys (not a smooth gradient atlas) — i.e. the mask **partitions the surface into discrete recolorable zones**, each addressable by a shader that tests the mask channel and applies a per-region tint. This is exactly the ≥3-zone separability prediction #2 requires; **5 discrete zones observed**, comfortably above the ≥3 threshold. The zones map to the canonical Synty register: primary surface / secondary surface / metal / leather-trim / accent (precise semantic per-zone labeling needs a render to confirm visually — § 5 caveat — but the *count and discreteness* are unambiguous from the mask data).

### 3.2 Synty already ships the "N palette profiles" multiplier

The 4 base atlases each ship as **A / B / C palette variants**. Comparing `Texture_01_A/B/C`:
- **Occupancy overlap A&B / A = 1.000** — identical UV layout (the texels are in the same places).
- **Mean color diff A→B = 11.4/255, A→C = 24.1/255** — only the *colors* differ.

That is the definition of "one UV atlas, N palettes." **Synty themselves treat restyle-by-palette as the differentiation model** — gandalf's architecture is not inventing the lever, it is generalizing Synty's own shipped pattern. The MaterialList confirms every modular part is assigned `Slot: FantasyHero (Uses custom shader)` — i.e. a single shared custom shader consumes the mask + atlas, which is precisely the "one master ShaderMaterial + N StyleProfiles" target of §7.2.

**Verdict (modular pack):** per-region recolor via mask-driven shader is **confirmed real**. The L2 restyle leaf can be built against a 5-region mask with a per-region palette in the StyleProfile.

### 3.3 LOAD-BEARING CAVEAT — the mask scheme is pack-class-specific

The per-region `_Texture_Mask` scheme is a property of the **Modular Fantasy Heroes** pack. The page-1 named-character packs do **NOT** ship it:
- **Adventure pack:** ships whole-atlas variants — `PolyAdventureTexture_01`, `_Dark_01`, `_Snow_01`, and skin-tone whole-swaps `Characters_Black/Brown/White`. No `*_Mask` texture.
- **Fantasy Kingdom pack:** grep for `mask` → zero hits.

So those packs offer **coarser, whole-atlas palette-swap recolor**, not independent per-region tint. **This bifurcates the restyle lever by lane:**

| Lane | Source packs | Recolor granularity | StyleProfile shape implication |
|---|---|---|---|
| **Per-slot lane** | Modular Fantasy Heroes | per-region (5 zones) mask-driven | StyleProfile = palette-PER-REGION (rich, the §3.6 multiplier) |
| **Silhouette lane** | Adventure / Fantasy Kingdom / Samurai (named characters) | whole-atlas palette-swap | StyleProfile = palette-as-WHOLE-tint (coarse) OR fall back to selection-as-differentiation |

This is the single decision gandalf's §7.6 must absorb: **the StyleProfile output field set is not uniform across the catalogue.** The modular lane warrants per-region palette fields; the silhouette lane warrants a coarser whole-tint field (or relies on base-mesh selection + accents for variety, per § 3.6's "base-mesh spread FIRST"). Recommend the StyleProfile schema carry a per-region palette array that gracefully degrades to a single whole-tint entry when the bound mesh has no per-region mask (the additive-nullable pattern cd7cba3 cited in § 3.1 of the architecture record fits this exactly).

---

## 4. Prediction (bonus) — monolithic vs modular reality: **CONFIRMED**

- **Page-1 POLYGON packs = baked whole-character FBX.** One named character = one skinned mesh: `SK_Character_Human_Knight`, `SK_Character_Human_Viking`, `SK_Chr_King_01`, `SK_Character_Samurai_Ninja_01`, etc. No per-slot separation. (Capes ship as a separate `SK_Chr_King_Cape_01` FBX — a hint that even the named-character lane has *some* accent modularity, but the body is one baked mesh.)
- **Modular Fantasy Heroes = genuine per-slot parts.** 720 part FBX named `Chr_<Slot>_<Gender>_<NN>_Static.fbx`; slot histogram: Torso 58, Hips 58, Head 46, ArmUpper L/R 42, Leg L/R 40, ArmLower L/R 38, Hand L/R 36, plus the accent-attach families.

**Lane assignment for gandalf:** page-1 named packs feed the **silhouette library** (whole characters, select-and-restyle-coarse); Modular Fantasy Heroes feeds the **per-slot lane** (assemble + per-region restyle + socket accents). This is the catalogue-to-select-from discipline (§ 3.6) made concrete: two different substrate shapes, two different differentiation budgets.

---

## 5. Tooling gap + caveats (what I could NOT confirm)

- **No mesh loader installed.** Blender/assimp/pyassimp were absent and not cleanly installable in-session. I did NOT load geometry or produce a render. **Consequence:** I confirmed the mask's *region count and discreteness* (from the PNG) and the socket/skeleton *graph* (from FBX node-name strings), but I did NOT visually confirm (a) which UV island each mask zone covers on the body, nor (b) the precise semantic label per zone (which zone is "metal" vs "leather"). The *count* (5 ≥ 3) is decision-grade; the *per-zone semantic mapping* needs a render pass when a loader is available. This does NOT change either verdict — both are YES regardless — but gandalf should treat the per-zone semantic labels (primary/secondary/metal/leather/accent) as *expected-but-unrendered* until a Godot/Blender import confirms.
- **Socket transforms unverified.** I confirmed the sockets *exist as named bones*; I did not extract their local transforms (position/orientation). That is a build-time detail for the §7.2 accent system, not a gate question.
- **Recommended follow-up (not gating):** one Blender-headless or Godot-import render of a single modular character with each mask zone tinted a distinct hue, to lock the per-zone semantic labels for the manifest's substrate half (§7.1 elrond). Galadriel can run this once a loader lands; it is a distinctiveness-scoring-adjacent task already in my §7.4 hook.

---

## 6. What this unblocks (gandalf §7.6 + the resumption gate)

Both load-bearing geometry assumptions of the architecture record § 4 step 2 are **answered YES**. The resumption gate (§ 4) is cleared on the geometry-verification half (the catalogue-slice half is elrond's manifest, already in this dir). gandalf may resume the design session and rule on the StyleProfile output shape, carrying forward the one caveat from § 3.3:

> **StyleProfile output shape (the §7.6 decision):** per-region palette array (5 zones) for the modular lane, gracefully degrading to a single whole-tint for the silhouette lane. The lever (§3.6 palette-remap as multiplier) is REAL and Synty-native on the modular pack; on the named-character packs differentiation leans on base-mesh selection + the coarse whole-tint + cape/accent modularity.

Prediction #3 likewise greenlights the §7.2 accent-attachment system unconditionally.

---

## 7. Mirror voice

The Mirror was set on the meshes, and they showed their seams plainly. The modular pack is not one surface but five, each keyed by a pure corner of the color cube — white, cyan, blue, yellow, magenta — and Synty has already walked the path gandalf charted: one atlas, three palettes, the same texels wearing different skins. The rig opens twelve named doors for accents and four more for capes. The lever is real, and it was forged before we asked for it. The one shadow: the named-character packs wear a single skin, not five — the silhouette lane buys its variety by selection, not by mask. That is the picture. The team may move.

**Signed:** galadriel (visual-perception + UX-similarity steward), 2026-06-17.
