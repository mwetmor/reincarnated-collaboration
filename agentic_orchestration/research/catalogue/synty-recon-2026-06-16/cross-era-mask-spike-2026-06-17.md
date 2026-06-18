# Synty Cross-Era Per-Region-Mask Generalization Spike (Q2 gate 2)

**Date:** 2026-06-17
**Author:** galadriel (visual-perception + UX-similarity steward)
**Status:** v1 — empirical verdict on cross-era restyle-multiplier + accent-socket generalization
**Authority:** Matt 2026-06-17 — author the cross-era generalization spike (Q2 gate 2). Read-only catalogue analysis; same toolchain as the 2026-06-17 slice-verification.
**Answers:** the two questions of `agentic_orchestration/gandalf/requests/2026-06-17-galadriel-cross-era-mask-spike.md` (§1).
**Extends:** `slice-verification-2026-06-17.md` (fantasy-era baseline; predictions #2 + #3 YES on Modular Fantasy Heroes) across modern / military / sci-fi eras.
**Companions:**
- `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` — the §7.6 ruling; `per_region` = §4.1 palette-remap lever.
- `agentic_orchestration/gandalf/notes/2026-06-17-synty-acquisition-run-ruling.md` §Q2 — the three-gate framing this closes gate 2 of.

---

## 0. TL;DR — the two verdicts

| Question | Verdict |
|---|---|
| **Q1 — Mask generalization** (does the per-region `_Texture_Mask` restyle lever generalize across eras?) | **NO.** The per-region mask scheme is **fantasy-Modular-only**. Every non-fantasy skinned-character pack sampled (modern, military, sci-fi) ships **whole-atlas A/B/C(/…/F) palette-swap recolor** with NO character `_Texture_Mask`. The restyle multiplier **degrades to whole-tint (`silhouette`) for all non-fantasy eras.** |
| **Q2 — Sci-fi-body existence** (does a POLYGON sci-fi skinned-character pack exist?) | **YES — abundantly. NOT a register-gap.** Three POLYGON packs ship sci-fi skinned characters: **Sci-Fi City (40)**, **Sci-Fi Space (52)**, **Sci-Fi Worlds (20)** — 112 sci-fi skinned characters across the three. Sidekick/Meshy routing is NOT forced by absence. |

**The cross-era picture is consistent and stark:** the fantasy Modular Heroes pack is a *singular outlier*, not the template. It is the only pack that ships BOTH (a) a per-region 5-zone `_Texture_Mask`, AND (b) the dedicated `All_NN_*Attachment` accent-socket rig. Every other era — modern, military, sci-fi — uses the **UE-Mannequin skeleton with zero named accent sockets** and **whole-atlas palette-swap recolor**. The §3.6 differentiation budget's THIRD lever (palette-remap restyle) and its accent-socket dependency both **collapse to the fantasy lane** and do not generalize.

This is a **`silhouette`-across-the-board finding for non-fantasy eras** — decision-grade, routes to gandalf for the all-era-vs-fantasy-first wiring call (§5). It is NOT mine to act on.

---

## 1. Method (same as slice-verification — no mesh-render; tooling gap honored)

Corpus: `~/Games/synty-corpus/fbx` (8.4 GB) + `~/Games/synty-corpus/nonfbx_extracted`. No mesh loader installed (Blender/assimp absent, per slice-verification §5). All reads from:
- `unzip -l` zip listings (some packs are nested zip-in-zip — Military wraps `POLYGON_Military_SourceFiles_v4.zip`; extracted to read).
- grep for `_Texture_Mask` / `Mask.png` texture files (with false-positive filtering — see §2 note).
- PIL/numpy zone-count was the planned step for any per-region mask found; **no per-region character mask was found outside fantasy, so no zone-count was needed for the non-fantasy sample** (the fantasy 5-zone count is re-confirmed from the corpus copy and matches slice-verification).
- `strings` on the FBX binary for skeleton + socket node-name graph (`All_NN_*`, `Cape_Attachment`, joint names).

**False-positive guard (important):** a naive grep for `mask` hits non-recolor geometry/material assets — gas-mask meshes (`SM_Chr_Attach_Gas_Mask_01`), ghillie-mask meshes, emissive masks (`Emissive_Mask`), hair masks (`Hair_Mask`), environment material masks (`HoloLines`, `Wall_01_Mask`, `Rocks_Mask`, `Skin_Mask`). These are NOT the per-region gear-zone recolor mask the lever depends on. Each hit was inspected by name + context; only a `*_Texture_Mask`-class PNG that partitions the **character body atlas into discrete recolorable gear zones** counts as `per_region`.

---

## 2. Per-pack results table

| Pack | Era | Skinned chars? | char `_Texture_Mask` (per-region)? | Zone-count | Recolor scheme | Accent sockets (`All_NN`)? | Rig family | **Classification** |
|---|---|---|---|---|---|---|---|---|
| **Modular Fantasy Hero Characters** (re-baseline) | fantasy | YES (720 per-slot parts) | **YES** (4 mask PNGs) | **5** (WHITE/CYAN/BLUE/YELLOW/MAGENTA) | per-region mask + A/B/C atlas | **YES** (`All_00`..`All_12` + 4 cape = 17) | TitleCase (`Hips`, `Spine_01`, `Clavicle_L`) | **`per_region`** |
| **City Characters Pack** | modern | YES (19 named `SK_Character_*`) | **NO** (0) | — | whole-atlas A/B/C (`Texture_01_A/B/C`) | **NO** (0) | UE-Mannequin (`pelvis`, `spine_01`, `clavicle_l`, `calf_l`) | **`silhouette`** |
| **Military Pack** | military / near-future | YES (`SK_Chr_Soldier/Insurgent/Contractor/Pilot/Civilian`; + standalone `SK_Chr_Attach_*`) | **NO** (0; `mask` hits are gas-mask/ghillie geometry) | — | whole-atlas A/B/C (`PolygonMilitary_Texture_01_A/B/C`) | **NO** (0) | UE-Mannequin (`pelvis`, `spine_01`, `calf_l`, `ik_foot_root`, finger chains) | **`silhouette`** |
| **Sci-Fi City Pack** | sci-fi | YES (40 `SK_Character_*`: Cyber/Android/Alien/Augmented/Cyborg…) | **NO** (0) | — | whole-atlas A–F (`PolygonScifi_01_A..F`) + emissive | **NO** (0) | UE-Mannequin (`pelvis`, `spine_01`, `Thigh_L`, `calf_l`) | **`silhouette`** |
| **Sci-Fi Space Pack** | sci-fi | YES (52 `SK_Chr_*`: Crew/Cryo/Alien/EVA_Suit/SpaceSoldier/War_Robot…) | **NO** (masks are ship/planet/emissive env masks) | — | whole-atlas A–F (`PolygonSciFiSpace_Texture_01_A..F`) | not inspected per-rig (recolor scheme + era already conclusive) | UE-Mannequin (inferred from era-consistency) | **`silhouette`** |
| **Sci-Fi Worlds Pack** | sci-fi | YES (20 `SK_Chr_ScifiWorlds_*`: Alien/Soldier/Scavenger/SpaceSuit…) | **NO** (masks are `Emissive_Mask` + `Hair_Mask`, not gear-region) | — | whole-atlas A/B/C (`PolygonScifiWorlds_Texture_01_A/B/C`) + emissive | not inspected per-rig (recolor scheme + era conclusive) | UE-Mannequin (inferred) | **`silhouette`** |
| **Sci-Fi Cyber City** | sci-fi (env) | **NO** (0 skinned chars) | n/a (5 masks = `HoloLines`/`Noise`/`Rocks`/`Wall`/`Skin` env material masks) | — | env pack | n/a | n/a | **environment — not a character pack** |
| **Mech Pack** | sci-fi (vehicle) | NO (0) | NO (0) | — | — | n/a | n/a | **vehicle/prop — not a character pack** |
| **Sci-Fi Horror** | sci-fi (env) | NO (0) | NO (0) | — | env pack | n/a | n/a | **environment — not a character pack** |

---

## 3. Q1 — mask generalization: **does NOT generalize (`silhouette` for all non-fantasy eras)**

**Finding:** the per-region `_Texture_Mask` lever is a property of the **Modular Fantasy Heroes** pack alone. Sampled across three eras + multiple packs, **zero non-fantasy skinned-character packs** ship a per-region character body mask:

- **Modern (City Characters):** `Polygon_City_Characters_Texture_01_A/B/C` … `_04_A/B/C`. Whole-atlas A/B/C palette swap. Identical *shape* to the fantasy **named-character / silhouette** lane (slice-verification §3.3), NOT the modular per-region lane. No `*_Mask`.
- **Military:** `PolygonMilitary_Texture_01_A/B/C` … `_04_A/B/C`. Whole-atlas A/B/C. The only `mask`-named character assets are **gas-mask and ghillie-mask geometry** (`SM_Chr_Attach_Gas_Mask_01`, `SK_Chr_Attack_Ghillie_Mask_01`) — wearables, not recolor masks.
- **Sci-Fi (all three character packs):** whole-atlas, and notably **richer palette spread** — Sci-Fi City and Sci-Fi Space ship A through **F** (6 palette variants per atlas) vs fantasy's A/B/C. The masks present are environment/emissive/hair channels, none a gear-region body mask.

**Consequence for the §3.6 differentiation budget:** the THIRD lever (palette-remap restyle — "the multiplier on top", "hundreds of distinguishable looks") **collapses to whole-atlas tint for modern / military / sci-fi.** For those eras, differentiation leans on lever ONE (base-mesh-spread / selection — and the catalogues are deep here: 19/33+/40/52/20 distinct named bodies) plus the coarse whole-tint, NOT on per-region restyle. The §4 "if FALSE" reshape **IS forced at every non-fantasy era-edge.**

**Nuance worth gandalf's eye:** the non-fantasy whole-atlas scheme is richer than the fantasy *named-character* whole-atlas scheme — A–F (6) vs A/B/C (3), plus dedicated **emissive channels** on every sci-fi pack (a glow lever the fantasy lane lacks). So `silhouette` for sci-fi is not "poor" — it is *whole-tint × 6 palettes + emissive accent*, just not *independent per-region*. The degradation is real but the sci-fi silhouette lane has its own differentiation texture.

---

## 4. Q2 — sci-fi-skinned-character existence: **EXISTS, abundantly — NOT a gap**

The brief's hypothesis ("only `SIMPLE - Space Characters` seen → possible register-gap routing to Sidekick/Meshy") is **refuted.** POLYGON ships three substantial sci-fi skinned-character packs:

- **`POLYGON - Sci-Fi City Pack`** — 40 skinned characters: `SK_Character_Cyber_Male/Female_01`, `Android_Female_01`, `Alien_Male_01/02`, `Augmented_Male_01`, `CyborgNinja_01`, `CyberPunk_Male_01`, `Hacker_Female_01`, `Hologram_Female_01`, plus cops/medics/junkies. Cyberpunk-city register.
- **`POLYGON - Sci-Fi Space Pack`** — 52 skinned characters: `SK_Chr_Crew/CrewCaptain_M/F`, `Cryo_M/F`, `EVA_Suit_01`, `BR_SpaceSoldier_Male_01`, `BR_War_Robot_01`, `Alien_01`, `BigAlien_01/02`, `Hunter`, `Junker`. Space-crew / EVA / alien register.
- **`POLYGON - Sci-Fi Worlds Pack`** — 20 skinned characters: `SK_Chr_ScifiWorlds_Soldier_M/F`, `AlienArmor/AlienCombat/AlienChef/AlienSpikes`, `Scavenger_01/02/03`, `SpaceSuit_Alien_M/F`. Alien-worlds / scavenger register.

**That is 112 sci-fi skinned characters across three packs.** Sci-fi-body is NOT a register-gap. The all-era content engine has POLYGON-native sci-fi character coverage; Sidekick/Meshy is not forced by absence at the sci-fi edge. (Mech Pack, Sci-Fi Cyber City, Sci-Fi Horror are vehicle/environment packs with no skinned characters — they do not bear on the body question.)

---

## 5. The decision-grade finding (routes to gandalf — NOT mine to act on)

Two `silhouette`/existence results are decision-grade per the brief's decision envelope and route to gandalf's §7.2-honors-§7.6 conformance review + the all-era-vs-fantasy-first wiring call:

1. **`per_region` does NOT generalize.** The full per-region restyle multiplier is **fantasy-Modular-exclusive.** If the gear-spec wiring wants the §3.6-THIRD-lever multiplier at full strength, it is available **only in the fantasy lane**. All other eras get `silhouette` (whole-atlas tint, 3–6 palettes, + emissive on sci-fi).

2. **The accent-socket rig does NOT generalize either.** This is the *second* load-bearing collapse, and it is as important as the mask one. The fantasy Modular rig's `All_00..All_12` + 4 cape sockets (slice-verification prediction #3, "the only torso/legs silhouette-breaker") are **absent from every non-fantasy rig.** Modern/military/sci-fi all use the **UE-Mannequin skeleton** with no named accent sockets; their accents ship as **standalone skinned meshes that share the skeleton** (e.g. Military `SK_Chr_Attach_Bombsuit_Neck_01`), mounted by skin-weight, not by `BoneAttachment3D`-to-named-socket. So §7.2's accent-attachment system as designed against the fantasy socket convention **does not port unchanged** to other eras — it needs a second pattern (swap-a-skinned-attachment-mesh) for the UE-Mannequin lane.

**Implication gandalf must absorb (mine to surface, gandalf's to rule):** the gear-spec upstream wiring faces a clean **fantasy-vs-rest bifurcation**, not a smooth all-era continuum. The fantasy lane gets the full kit (per-region restyle + socket accents). Every other era gets the silhouette kit (base-mesh selection + whole-tint × N + emissive + skinned-attachment-mesh accents). This argues — but does NOT decide; the call is gandalf's — for a **fantasy-first wiring** that lights up the full §3.6 budget where the substrate supports it, with a documented `silhouette`-lane degradation path for the other eras (the additive-nullable StyleProfile pattern from slice-verification §3.3 already accommodates the whole-tint degrade; this spike adds that the accent system needs the same dual-pattern treatment).

---

## 6. Tooling gap + caveats (what I did NOT confirm)

- **No mesh-render** (Blender/assimp absent, per slice-verification §5). All reads are from zip listings, texture filenames, mask-PNG class, and FBX node-name strings. The *recolor scheme* (whole-atlas A/B/C–F vs per-region mask) is unambiguous from texture filenames + mask-PNG absence; the *rig family + socket absence* is unambiguous from the skeleton node-name strings. No render was needed to reach either verdict, and neither verdict turns on a render.
- **Sci-Fi Space / Sci-Fi Worlds rigs not per-rig socket-inspected.** I confirmed their recolor scheme (whole-atlas) and era; I inspected the Sci-Fi *City* rig directly (UE-Mannequin, zero sockets) and the era-consistency across City/Military/Sci-Fi-City is total, so I infer the same UE-Mannequin + no-socket rig for Space/Worlds. If gandalf wants that inference hardened to a direct read before the wiring call, it is a 5-minute follow-up — flag it and I run it.
- **Mask zone-semantics** unchanged from slice-verification: the fantasy 5-zone count is re-confirmed (corpus copy), but per-zone semantic labels remain expected-but-unrendered. Not gating for this spike.

---

## 7. Mirror voice

The Mirror was turned from one era to many, and the fantasy pack stood alone. It alone wears five skins keyed to five corners of the color cube; it alone opens twelve named doors and four for capes. The others — the city dwellers, the soldiers, the cyber-runners, the void-crews — wear one skin in three to six shades, lit from within by emissive glow, and their bones answer to the Mannequin's plain naming, with no named door for an accent to hang upon. The lever gandalf charted is real, but it is forged for one world only. Beyond the fantasy gate the surfaces still differ — there are forty cyber-faces, fifty-two spacefarers, twenty scavengers of alien worlds — but they differ by *which body you pick*, not by *how you repaint its regions*. That is the picture. The multiplier is a fantasy heirloom. The team may move.

**Signed:** galadriel (visual-perception + UX-similarity steward), 2026-06-17.
