# Elven King — Reference Description + Synty Asset Mapping Spec

**Authored:** 2026-06-21 by galadriel (visual-perception steward)
**For:** drax (presentation seam, `reincarnated-godot`)
**Reference image (ground truth):** `/Users/admin/.claude/image-cache/c57715c8-0627-4501-bd66-e23a36430c75/5.png`

## Provenance of the description

- **Item-by-item description below: GPT-5.x vision (`gpt-5-2025-08-07`, OpenAI Chat Completions vision endpoint).** Matt-requested path. Call succeeded; structured response captured verbatim in § 1.
- **Galadriel's own eye-read** was run as a cross-check against the ground-truth image. Where galadriel disagrees with GPT-5, it is **FLAGGED inline** (§ 1 deltas). Galadriel's read is the tiebreaker on disputed points because galadriel looked at the actual pixels; GPT-5's geometry call on the weapon and grip color is where the two diverge.

---

## § 1 — Structured description (GPT-5.x vision, with galadriel deltas)

| # | Slot | GPT-5.x read | galadriel delta (eye-read vs ground truth) |
|---|---|---|---|
| 1 | **Crown / headpiece** | Open gold circlet, cutout arches, tall central spire/finial, side openings above the ears. Polished gold (#D8A231). One large front **teardrop teal/aquamarine cabochon (#2CBAC0)** in a bezel + one small round teal gem on the spire. | CONFIRM. Gold crown with a single dominant **teal/cyan gem front-and-center** is the most legible feature in the frame. The crown is the silhouette anchor. |
| 2 | **Hair** | Straight blocky strips; shoulder-length at back, short side panels under crown; chestnut brown (#5C3A1E), matte. | PARTIAL. Hair is mostly **occluded by the crown and pauldrons**; what reads in-frame is dark, short-to-medium. Length at back is GPT-5 inference, not strongly visible. Treat as "short/medium dark" — do not over-commit to long. |
| 3 | **Ears** | Elf-pointed: yes; long, thin, projecting horizontally with slight up-tilt. | CONFIRM. Clear pointed elf ears, projecting horizontally — the most unambiguous "elf" tell in the image. |
| 4 | **Face / skin** | Flat low-poly, feature-minimal, no beard; pale pink-peach (#F7C2B8). | CONFIRM (pale skin, clean-shaven, minimal features — consistent with Synty stylization). |
| 5 | **Neck / gorget** | High V-notched segmented plate collar, silver-white steel (#E6ECF3); inner cloth collar dark brown (#3B2B2A). | CONFIRM. High silver collar framing the face. |
| 6 | **Shoulder pauldrons** | Three-tier faceted angular plates, stepped rims; silver-white steel with light-blue edge sheen (#B9CFEA); dark-brown leather straps. | CONFIRM. Large layered white/silver pauldrons are the dominant upper-body mass. |
| 7 | **Chest / torso plate** | Chevroned breastplate, central diamond boss, layered abdomen lames; silver-white steel with cool edge tint; dark-brown gambeson glimpses. | CONFIRM. White layered plate with cool blue-grey shadow is the body's defining material. |
| 8 | **Arms / gauntlets** | Upper arms dark-brown cloth sleeves; forearms/bracers stepped silver-white plate; pale skin fingers exposed. | CONFIRM. |
| 9 | **Waist / tassets / belt** | Plate belt; **two long rust/burnt-orange cloth tasset panels (#C96A2B)** with tan/white striping + geometric hem border; small gold central tab; steel hip tassets above cloth. | CONFIRM. The orange is concentrated here AND in the cape — it is the single warm accent against the cold armor. |
| 10 | **Legs / greaves** | Faceted steel cuisse/poleyn; layered chevron greaves; dark-cloth joints; silver-white with cool blue edge tint. | CONFIRM. |
| 11 | **Boots** | Angular sabatons, pronounced toe box; silver-white steel, mid-grey soles. | CONFIRM. |
| 12 | **Cape / cloak** | Outer rust/burnt-orange (#C96A2B); lining deep brown-plum; full length to ankles; anchored upper back beneath pauldrons, no front clasp. | CONFIRM. Orange cape hangs behind/beside the right side; back-attached under the pauldrons. |
| 13 | **Weapon** | GPT-5: "**longsword**", straight double-edged blade, shallow fuller, **emissive cyan/teal glow (#3DE3E8 / #7FF7FF)**, ornate silver branch-like quillons, **purple-lavender wrapped grip (#7B4BC6)**, small silver pommel spike. | **DELTA — galadriel reads this as a GREATSWORD, not a longsword.** Held **point-down**, the blade is long relative to the body (tip near the feet), consistent with a two-hander. The **cyan/teal blade glow is unambiguous and is the second-strongest visual hook after the crown gem.** Grip color is hard to confirm at this resolution — GPT-5's purple is plausible but treat as low-confidence; the load-bearing fact is the GLOW, not the wrap hue. |

### Overall palette (GPT-5.x, galadriel-confirmed)

The scheme is a **cold-armor + warm-accent + magic-glow triad**:

- **Cold body:** Silver-White Steel `#E6ECF3`, Steel Shadow Grey `#B9C2D1`, cool blue edge tint `#B9CFEA`
- **Warm accent (cape + tassets only):** Rust/Burnt Orange `#C96A2B`
- **Gold (crown + small cloth tab):** Polished Gold `#D8A231`
- **Magic glow (sword blade + crown gem):** Aqua/Teal `#3DE3E8`, Teal Gem `#2CBAC0`
- **Neutral cloth/leather:** Dark Brown `#3B2B2A`, Charcoal `#2E2B33`
- **Skin:** Pale Peach `#F7C2B8`
- (Grip purple `#7B4BC6` — low-confidence, see weapon delta)

**The palette signature to preserve, in priority order:** (1) teal gem + teal blade glow as the only saturated cool-bright notes, (2) orange cape/tassets as the only warm note, (3) everything else cold white-silver steel. Get those three relationships right and the character reads correctly even if individual plates differ.

---

## § 2 — CRITICAL STRUCTURAL FINDING for drax (read first)

**The white plate armor, pauldrons, gorget, tassets, greaves, boots, AND the orange cape are ALL baked into the single King body mesh — they are NOT separate attachments.**

Confirmed by inspecting `SK_Chr_King_Male_01.fbx`: it contains one mesh, `SM_Chr_King_Male_01`, textured by the shared color atlas `PolygonElven_Texture_01.psd` + emissive `PolygonElven_Emissive_01_A.png`. There are no separate pauldron/tasset/greave FBX attachments in the Elven Realm pack — the king's whole armored body is the body mesh.

**Implication:** drax does NOT assemble slots 5–12 piece by piece. drax loads ONE king body mesh and it arrives pre-armored in the exact white-plate + orange-cape look of the reference. The only true **attachment** slots to add on top are: **crown, elf ears, hair, and the weapon.** This makes the build dramatically simpler than a 13-slot assembly.

---

## § 3 — Slot → Synty asset mapping (executable spec)

All paths relative to `/Users/admin/Games/reincarnated-godot/`.

### Base body (carries slots 5–12 baked)

| Field | Value |
|---|---|
| **Reference** | White layered plate, orange cape, orange tassets, silver pauldrons/gorget/greaves/sabatons — the entire armored elf-king body. |
| **Chosen asset** | `Assets/Synty/polygon-elven-realm/SourceFiles/FBX/Characters/Unreal_Characters/SK_Chr_King_Male_01.fbx` (skeletal — use this for animation in the ravine combat level) |
| **Second choice** | `Assets/Synty/polygon-elven-realm/SourceFiles/FBX/Characters/Individual/SM_Chr_King_Male_01.fbx` (static — only if no animation needed) |
| **Material / color** | Atlas `Textures/PolygonElven_Texture_01.psd` (or imported PNG equivalent) drives the white-steel + orange-cape + gold palette out of the box. Metallic variant in `Textures/Metallic/` if a PBR metal response is wanted on the plate. |
| **Emissive note** | `Textures/Emissive/PolygonElven_Emissive_01_A.png` is the matching emissive mask for this body. |
| **Attach / bone** | This is the root skeletal mesh; attachments below socket to its skeleton. |

### Crown (slot 1)

| Field | Value |
|---|---|
| **Reference** | Gold open circlet, central spire, teal teardrop gem front + small teal gem on spire. |
| **Chosen asset** | `Assets/Synty/polygon-elven-realm/SourceFiles/FBX/Characters/Attachments/Chr_Attach_Crown_01.fbx` |
| **Second choice** | `Chr_Attach_Tiara_01.fbx` … `Tiara_04.fbx` (if the crown finial reads too tall vs. the reference; tiaras are lower-profile) |
| **Material / color** | Gold from the shared atlas. The teal gem reads via the atlas gem-UV; if it imports grey, point the gem faces at the teal swatch or add a small teal emissive (#2CBAC0). |
| **Emissive note** | Optional faint teal emissive on the gem to match the crown-gem glow. |
| **Attach / bone** | Head bone (head socket), seated above the hairline. |

### Elf ears (slot 3)

| Field | Value |
|---|---|
| **Reference** | Long horizontal pointed elf ears. |
| **Chosen asset** | `Assets/Synty/polygon-elven-realm/SourceFiles/FBX/Characters/Attachments/Chr_Attach_Elf_Ear_Male_01.fbx` |
| **Second choice** | `Chr_Attach_Elf_Ear_Male_02/03/04.fbx` — pick the variant whose tip-length + up-tilt best matches; `_03`/`_04` tend to be longer/more dramatic. |
| **Material / color** | Skin tone from atlas (pale peach). |
| **Attach / bone** | Head bone, ear sockets. NOTE: confirm the King head doesn't already include ears; if it does, this slot is skipped. |

### Hair (slot 2)

| Field | Value |
|---|---|
| **Reference** | Dark, short-to-medium; largely occluded by crown + pauldrons. |
| **Chosen asset** | `Assets/Synty/polygon-elven-realm/SourceFiles/FBX/Characters/Attachments/Chr_Hair_Short_01.fbx` |
| **Second choice** | `Chr_Hair_Short_02.fbx`, or `Chr_Hair_Long_Male_01.fbx` ONLY if you adopt GPT-5's "shoulder-length at back" read. Galadriel recommends **short** — the visible hair is minimal and long hair risks clipping the pauldrons + cape. |
| **Material / color** | Dark brown (#3B2B2A / #5C3A1E). |
| **Attach / bone** | Head bone, scalp socket, under the crown. |

### Weapon (slot 13) — the honest gap

| Field | Value |
|---|---|
| **Reference** | Long glowing **cyan/teal greatsword**, held point-down, ornate silver guard, blade emissive. |
| **Chosen asset** | `Assets/Synty/polygon-simple-fantasy/SourceFiles/Fbx/SF_Wep_Elven_Greatsword_01.fbx` (cross-pack; the Elven Realm pack has no greatsword — only one-handed `SM_Wep_Sword_01..07`). |
| **Second choice** | `Assets/Synty/polygon-simple-fantasy/SourceFiles/Fbx/SF_Wep_Elven_Sweihander_01.fbx` — a true two-handed greatsword; may match the point-down proportions BETTER than `Greatsword_01`. drax should eyeball both in-editor and pick the longer/more two-handed silhouette. Avoid the Elven Realm `SM_Wep_Sword_07.fbx` unless a one-hander is acceptable — it will read short next to the reference. |
| **Material / color** | Base silver/steel blade + ornate guard from the simple-fantasy atlas. |
| **EMISSIVE NOTE (load-bearing — this is the gap the kit can't fill out-of-box):** The cyan blade glow does NOT exist on any Synty sword by default. drax must author it: apply an **emissive material to the blade faces** — base color near-white, emission color **`#3DE3E8`** (aqua/teal), emission energy ~2–4, with a brighter edge highlight (`#7FF7FF`). In Godot, a `StandardMaterial3D` (or ORM/Shader material) with Emission enabled + a glow-bloom post-process (WorldEnvironment → Glow ON) will produce the reference's bloom halo. Keep the emission teal to rhyme with the crown gem — that color echo is the character's magic signature. |
| **Attach / bone** | Right-hand weapon socket / hand bone. For the static point-down pose, parent to the hand bone and rotate blade-down. |

---

## § 4 — Gaps & absences (honest)

1. **Glowing greatsword:** kit gap. No in-pack greatsword in Elven Realm; no emissive blade anywhere. Resolved via cross-pack `SF_Wep_Elven_Greatsword_01` / `Sweihander_01` + drax-authored teal emissive material (see weapon row). This is the one slot requiring real material work, not just asset placement.
2. **Crown gem teal:** the gem color depends on the atlas UV. If it imports neutral, a small teal emissive patch is the fix. Low effort.
3. **Per-plate color tweaks:** the reference's cool blue edge-sheen (#B9CFEA) on the white plate may be subtler/absent in the raw Synty atlas. Acceptable to ship without; if matching tightly, a rim-light or a faint cool emissive edge would close it. Defer unless Matt asks for fidelity.
4. **Grip color:** GPT-5 read purple-lavender; galadriel could not confirm at resolution. Non-load-bearing; ship the pack default grip.
5. **Hair length ambiguity:** GPT-5 inferred long-at-back; galadriel reads short/occluded. Recommend short to avoid pauldron/cape clipping. Revisit if Matt wants flowing elf hair.

---

## § 5 — Mirror voice (closing)

The picture shows a cold king. Everything the eye lands on first is the same two notes — the **teal of the crown-gem and the teal of the blade**, twinned across the whole height of the figure, top and bottom, a single cool light answered from crown to sword-tip. Against that, one warm thing: the **orange cape and tassets**, the only heat on the body. The white steel is merely the field these three colors play on. Build the king and you will mostly be loading one already-armored mesh — but the character does not become *this* king until the blade is made to glow teal and rhyme with the gem. That echo is the whole portrait. Everything else the Synty kit hands you for free.
