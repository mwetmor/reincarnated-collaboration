# Unity Asset Store — Armor Catalogue
# Priority 2 (Mode B — Catalogue Crawl)

**Date:** 2026-05-22
**Mode:** B (catalogue crawl)
**Commissioner:** gandalf (dispatch 2026-05-22-legolas-unity-asset-catalogue-armor-meshy.md)
**Total armor category size:** 159 assets in 3D/Props/Clothing/Armor (plus additional armor under Humanoids)
**Scope:** Publisher-representative enumeration focusing on humanoid-rigged and modular-equip armor packs

---

## Preliminary Note on Armor Category Taxonomy

The Unity Asset Store splits armor across two category trees:

1. **3D > Props > Clothing > Armor** — 159 results. Primarily standalone armor mesh props and partial armor pieces. These are NOT always rigged.

2. **3D > Characters > Humanoids** — Modular character packs that include armor as rigged layers on top of a humanoid skeleton. This is the category relevant for runtime armor equipping.

Both must be surveyed. The dispatch is primarily interested in the second category (skinned armor for character equipping) but both are documented.

---

## Publisher A: Magic Pig Games / Infinity PBR — Armor Pack 1

**Product:** Armor Pack 1 - Fantasy RPG
**URL:** https://assetstore.unity.com/packages/3d/props/clothing/armor/armor-pack-1-fantasy-rpg-135427
**Price:** $50
**Pipeline:** Built-in + URP + HDRP (all three confirmed)
**Style:** Fantasy RPG, modular armor, PBR materials, leather + plate types
**Rigged:** Yes — "Rigged" listed in keywords; designed for Infinity PBR Humans/Elves/Half-Orcs humanoid characters
**Content:** 5 different armor models, each modular with individual parts that can be turned on/off; 20 unique texture variants; Substance Painter source files included
**File size:** 1.7 GB

**Assessment:** This is the most explicitly armor-as-equippable-layer pack on the Asset Store. The modular design (individual parts toggleable) is the runtime swap pattern. However, the skeleton it is designed for is "Infinity PBR Humans/Elves/Half-Orcs" — this is Infinity PBR's own character rig, which may or may not map cleanly to Unity's standard Humanoid Avatar without remapping. Verification required before commitment.

**Body-part coverage:**
- Chest: Yes (plate, leather cuirass variants)
- Helmet: Yes
- Gauntlets: Yes
- Legs: Yes
- Boots: Yes (implied by "full armor" modular)
- Pauldrons: Yes (implied)
- Cloak: Unknown — not mentioned

**URP flag:** Confirmed.
**Pre-purchase verification required:** Confirm skeleton compatibility with Unity Humanoid Avatar before $50 commit. The "Infinity PBR rig" may require their specific character base mesh to work correctly.

---

## Publisher B: Polytope Studio — Lowpoly Modular Armors Series

**Register:** Low-poly medieval fantasy; consistent with the Polytope Studio MEDIEVAL FANTASY SERIES
**Style:** Low-poly, PBR materials; matches low-poly aesthetic common in mobile/indie RPGs
**Pipeline:** Built-in + URP (HDRP not supported — this is a confirmed limitation across the series)

| Pack | Price | Notes |
|---|---|---|
| Lowpoly Modular Armors — MEDIEVAL FANTASY SERIES | $49.99 | Base armor pack in series |
| Lowpoly Modular Armors Expansion Pack 01 | ~$30–49 (est.) | Extended armor variants |
| Lowpoly Modular Armors Expansion Pack 02 | ~$30–49 (est.) | Further extensions |
| Lowpoly Modular Armors Bundle | $102.99 | All three above bundled |

**Content:** Modular low-poly armor for humanoid characters. The "Humanoids" category placement implies skeleton-rigged; however, the specific skeleton type is not confirmed in available documentation. File size is small (42.8 KB for bundle = unusual; likely these are extension assets that depend on a base character asset from Polytope Studio).

**Critical constraint:** The bundle is an "Extension Asset." This means it depends on Polytope Studio's base character asset for the rig to function. Standalone use for arbitrary humanoid characters may require manual skeleton remapping.

**Body-part coverage:**
- Not itemized in accessible documentation; the "modular" label implies per-piece design (helmet, chest, shoulders, legs, boots)
- Shoulder armor (×7) confirmed in Dungeon Realms equivalent content

**URP flag:** Confirmed compatible. HDRP not supported — relevant only if project moves to HDRP.

**Aesthetic register:**
- `tech_level`: medieval
- `tone`: heroic
- `cultural_lineage`: European

---

## Publisher C: Bretwalda Games — Rigged Armour Collection

**Product:** Rigged Armour Collection
**URL:** https://assetstore.unity.com/packages/3d/characters/humanoids/humans/rigged-armour-collection-132263
**Price:** $30
**Pipeline:** Not confirmed in crawl — requires verification
**Style:** Medieval/fantasy (category: Humanoids > Humans)
**Rigged:** Yes — "Rigged" is in the title; 24 screenshots visible in gallery
**Reviews:** 4-star rating, 172 favorites (respectable adoption for a niche armor pack)
**File size:** 548.3 MB (2018 release; Unity 2018.2.12 original)

**Assessment:** The title explicitly claims rigging. The category placement (Humanoids > Humans) suggests skinned to a humanoid skeleton. 4-star / 172 favorites is the strongest adoption signal in the rigged-armor category. The 2018 release date is a concern for render pipeline support — verify URP compatibility before purchase. At $30, this is the price-point leader for dedicated rigged armor.

**Body-part coverage:** Not itemized in available documentation; 24 screenshots suggests meaningful variety (likely multiple armor sets or pieces).

**URP flag:** UNCONFIRMED — older pack (2018). High priority verification item.

---

## Publisher D: Blink — Free Modular Character (with armor)

**Products:** 
- FREE — Modular Character — Fantasy RPG Human Male (free)
- Modular Character — Fantasy RPG Human Male ($39.99)

**Pipeline:** Built-in + URP + HDRP (confirmed)
**Style:** Stylized fantasy RPG, PBR materials
**Rigged:** Yes — humanoid rig with armor as modular layers

The free version provides a baseline modular character with "starter armor" included; the paid version extends with more armor pieces. The Blink ecosystem (these characters + the Stylized RPG Weapons series) creates a stylistically coherent weapon+character substrate.

**Body-part coverage:** Implied modular by "Modular Character" title; specific armor piece list not confirmed.

**Assessment:** The free tier provides a zero-cost validation path for the modular armor pattern. Recommended as the first procurement step to test Unity Humanoid Avatar + armor swap workflow before committing to paid packs.

**URP flag:** Confirmed.

---

## Publisher E: Synty Studios — POLYGON Dungeon Realms (Character Attachments)

Per weapons-catalogue.md, POLYGON Dungeon Realms ($199.99) includes 69 character attachments:
- Shoulder Armor (×7)
- Helmets (multiple — specific count not extracted)
- Faceplates (×2), Masks (×4), Hoods, Hats, Headwraps
- Horns, Feathers, Ears (decorative)

**Note:** These are attachment props (rigid attachment to bone anchor), not skinned armor pieces. They work for the rigid-attachment pattern: helmet parented to head bone, shoulder armor parented to shoulder bone. They do NOT include skinned chest pieces or cloth-simulation cloaks.

**Body-part coverage for skinned armor:** None — these are rigid attachments only.

**URP flag:** Built-in + URP per Samurai pack; verify for Dungeon Realms.

---

## Armor Body-Part Coverage Matrix

| Body part | Dedicated Asset Store coverage | Skinnable? | Notes |
|---|---|---|---|
| Helmet | Synty attachments (rigid), Infinity PBR Armor Pack 1, Polytope Studio series, Rigged Armour Collection | Rigid: many options. Skinned: Infinity PBR (verify skeleton) + Rigged Armour Collection | Well-covered for rigid; moderate for skinned |
| Chest plate | Infinity PBR Armor Pack 1, Polytope Studio series, Rigged Armour Collection | Skinned options exist; skeleton mapping verification required | Moderately served |
| Pauldrons / shoulder armor | Synty Dungeon Realms (rigid ×7), Infinity PBR, Polytope Studio | Rigid: good (Synty). Skinned: Infinity PBR (verify) | Rigid well-covered |
| Gauntlets | Infinity PBR, Polytope Studio, Rigged Armour Collection | Skinned options exist | Moderate |
| Greaves / boots | Infinity PBR, Polytope Studio | Skinned options exist | Moderate |
| Cloak / cape | o3n Male Hooded Robe ($? — not priced in crawl), general clothing packs | Static mesh only — cloth simulation requires Obi Cloth or Unity Cloth component | THIN — no pre-rigged cloth cape with physics found |
| Full robe | o3n Male Hooded Robe (closest match found) | Static mesh or manual cloth simulation setup | THIN |
| Full plate harness (complete set) | Infinity PBR Armor Pack 1 (best candidate) | Verified rigged; skeleton match needs verification | One dedicated option |

---

## Aesthetic Register Coverage for Armor

| Register | Coverage | Notes |
|---|---|---|
| Medieval-heroic-European (plate/leather) | GOOD — Infinity PBR, Polytope Studio, Rigged Armour Collection, Blink Modular Character | Multiple options across price points |
| Dark-grim-European (bone/dark plate) | SPARSE — some Dungeon Realms attachments; no dedicated dark armor pack found | Gap in grimdark register |
| Ancient-East-Asian (lamellar, samurai) | SPARSE — Synty Samurai has character attachments; no dedicated armor pack found | Gap |
| Mystical/robe/mage (full robe, caster armor) | THIN — o3n Male Hooded Robe (single option) | Gap for caster-class armor register |
| Sci-fi armor | Not scoped in this crawl | Out of scope per dispatch |

---

## Cloth Armor Handling — Supplemental Note

Cloaks, full robes, and soft cloth armor are a separate engineering problem from plate armor:

- **Unity built-in Cloth component:** Works on Skinned Mesh Renderers with cloth constraint setup. Included in Unity at no cost. Requires per-garment tuning.
- **Obi Cloth:** $55 on Unity Asset Store. More robust cloth simulation. Recommended for production-quality cloaks.
- **Physics-based approach tradeoff:** Both approaches require manual constraint painting on the cloth mesh. Not plug-and-play — engineering time required per garment.

**Implication for Reincarnated:** If cloaks and robes are a visual surface for spirit archetypes (e.g., caster staff archetype wears a robe), Meshy generates the robe geometry baked into the character (Pattern A — no problem) but the cloth does not simulate. For any register where robe/cloak silhouette simulation is visually load-bearing, Obi Cloth ($55) is the recommended engineering investment.

---

## Source URLs

- Infinity PBR Armor Pack 1: https://assetstore.unity.com/packages/3d/props/clothing/armor/armor-pack-1-fantasy-rpg-135427
- Polytope Studio Modular Armors: https://assetstore.unity.com/packages/3d/characters/humanoids/lowpoly-modular-armors-medieval-fantasy-series-229963
- Polytope Studio Bundle: https://assetstore.unity.com/packages/3d/characters/humanoids/lowpoly-modular-armors-bundle-medieval-fantasy-series-230383
- Bretwalda Rigged Armour Collection: https://assetstore.unity.com/packages/3d/characters/humanoids/humans/rigged-armour-collection-132263
- Blink Free Modular Character: https://assetstore.unity.com/packages/3d/characters/humanoids/humans/free-modular-character-fantasy-rpg-human-male-228952
- Blink Paid Modular Character: https://assetstore.unity.com/packages/3d/characters/humanoids/humans/modular-character-fantasy-rpg-human-male-201305
- Synty Dungeon Realms (character attachments): https://syntystore.com/products/polygon-dungeon-realms
- o3n Male Hooded Robe: https://assetstore.unity.com/packages/3d/characters/o3n-male-hooded-robe-108351
- Obi Cloth: https://assetstore.unity.com/packages/tools/physics/obi-cloth-81333
