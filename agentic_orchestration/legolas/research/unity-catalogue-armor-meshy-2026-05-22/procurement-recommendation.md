# Procurement Recommendation — Tier 1 / Tier 2 / Tier 3
# Priority 2 (Mode B — Catalogue Crawl)

**Date:** 2026-05-22
**Mode:** B (findings + procurement framing)
**Commissioner:** gandalf (dispatch 2026-05-22-legolas-unity-asset-catalogue-armor-meshy.md)
**Note:** This file provides budget framing and procurement shortlists. All procurement decisions are Matt's. This document is scoping inputs, not approved spend.

---

## Tier 1 — Minimum Viable Catalogue

**Scope:** Cover the 15 weapon archetypes in the dominant aesthetic register (medieval-European-heroic) with one visual style, plus baseline armor capability for Profile A.

**Style lock for Tier 1:** Blink "Stylized RPG Weapons" series — this is the closest to Reincarnated's locked style register (HD-2D Octopath-coded painterly + cel-shaded fantasy) available on the Asset Store. Low-to-medium poly with hand-painted-adjacent stylization.

### Tier 1 Asset Store shortlist (weapons)

| Pack | Price | Archetype coverage | URP? |
|---|---|---|---|
| Blink 100+ Stylized Weapons Bundle Vol. 1 | $69.99 | Swords (#1), daggers (#2), maces (#4), bows (#5), staves (#11), and supplemental types (~8–9 of 15) | Yes |
| Blink 100+ Stylized Weapons Bundle Vol. 2 | $69.99 | Scythes, muskets (#7), spellbooks/wands (#9/#12), spears (#3), daggers (#2) (~additional 3–4 archetypes) | Yes |

**Combined Blink Bundles:** $139.98. Estimated coverage: 12–13 of 15 archetypes in the medieval-heroic-European / stylized register.

### Tier 1 Meshy gap-fill (weapons)

Three archetypes not covered by Asset Store procurement:
- **Censer / thurible (#13):** Meshy text-to-3D prompt: "ornate bronze censer on a chain, fantasy holy equipment, T-pose prop orientation, plain background, stylized game asset" → static mesh → rigid attach to hand bone
- **Holy symbol / icon (#14):** Meshy prompt: "fantasy holy symbol on a pole/staff, radiant divine icon, stylized game asset" → static mesh → rigid attach
- **War-trumpet / horn (#15):** Meshy prompt: "ornate war horn / trumpetlike brass instrument, fantasy warrior, stylized game asset" → static mesh → rigid attach

**Orb / sphere (#10):** Found in prop packs not weapon packs; source from Mega Fantasy Props Pack or RPG Fantasy Crystal Kit (both on Asset Store, estimated $10–30 each).

**Tier 1 total weapons estimate:** ~$140–180 (Blink bundles + 1–2 prop packs for orbs)

### Tier 1 Asset Store shortlist (armor)

| Pack | Price | Coverage | URP? |
|---|---|---|---|
| Blink Free Modular Character (validation only) | FREE | Starter armor, baseline humanoid; use to test pipeline | Yes |
| Bretwalda Rigged Armour Collection | $30 | Rigged medieval armor collection; unknown body-part scope but 4 stars / 172 favorites | UNCONFIRMED — verify URP before commit |

**Tier 1 armor decision point:** For Profile A where armor is BAKED INTO the character model (Meshy Pattern A — no runtime swap), **no armor Asset Store purchase is required**. Armor is generated with the character by Meshy. Tier 1 armor spend is only needed if runtime armor swapping is a Profile A requirement.

**Tier 1 total armor (Pattern A — baked):** $0 additional
**Tier 1 total armor (Pattern B — swappable):** $30 (Bretwalda) + $50 (Infinity PBR Armor Pack 1 for plate variants) = $80, after URP verification

### Tier 1 total

| Component | Low estimate | High estimate |
|---|---|---|
| Weapons (Blink bundles + orb prop pack) | $140 | $180 |
| Armor (Pattern A baked) | $0 | $0 |
| Armor (Pattern B swappable) | $80 | $80 |
| Meshy-generated gap-fill items (censer, holy symbol, horn) | $0 (covered by Meshy Pro subscription) | $0 |
| **Tier 1 total (baked armor path)** | **$140** | **$180** |
| **Tier 1 total (swappable armor path)** | **$220** | **$260** |

---

## Tier 2 — Multi-Aesthetic Catalogue

**Scope:** Cover 2–3 aesthetic registers with meaningful depth. Profile A medieval-heroic-EU (Tier 1) + Ancient-East-Asian + Dark-grim-EU.

### Additional Tier 2 procurement

| Pack | Price | Register added | URP? | Notes |
|---|---|---|---|---|
| Synty POLYGON Samurai Pack | $29.99 | Ancient-East-Asian: swords (katana/odachi), spears (naginata), throwing (shuriken/kunai), bo staff | Built-in + URP | Covers archetypes 1,2,3,8 in East-Asian register; 245 total assets |
| Synty POLYGON Dungeon Realms | $199.99 | Dark-grim-EU: swords, daggers, maces, spears (81 weapons); +69 character attachments (helmet, shoulder armor) | Verify before commit | Also provides rigid-attachment armor for Dark register |
| Infinity PBR Weapons & Armor PBR Pack #1 | $60 | Grimdark-realistic-EU: PBR realistic weapons + armor — different register from Blink; relevant for future profiles | Yes | Style mismatch for Reincarnated Profile A; useful for multi-profile engine substrate |
| EpiXR Japanese Samurai Weapons (PBR) | $19.99 | Ancient-East-Asian (realistic PBR variant) | Not confirmed | Complements Synty Samurai in realistic register |

**Tier 2 additions total:** $30 + $200 + $60 + $20 = ~$310 additional over Tier 1

**Tier 2 total:** $450–$590 (Tier 1 + Tier 2 additions)

**Tier 2 register coverage:**
- Medieval-heroic-European: deep (Blink bundles, 12–13 archetypes)
- Ancient-East-Asian: moderate (Synty Samurai covers swords/spears/throwing; magical archetypes still absent)
- Dark-grim-European: moderate (Dungeon Realms covers melee family; magical archetypes absent)
- South-Asian / Mesoamerican / African: none

---

## Tier 3 — Comprehensive Catalogue

**Scope:** Maximum viable coverage from Asset Store alone; add volume (Pure Poly 900) + Synty Fantasy Kingdom (comprehensive single-pack breadth) + armor depth.

### Additional Tier 3 procurement over Tier 2

| Pack | Price | Value-add | URP? |
|---|---|---|---|
| Synty POLYGON Fantasy Kingdom | $349.99 | 183 weapon assets (broadest single-pack 15-archetype coverage); 69 character attachments; all asset types in one coherent aesthetic | Verify before commit |
| Pure Poly 900 Low Poly Fantasy RPG Weapons | $99.95 | 900 weapons — maximum per-archetype variation depth for procedural selection | Yes |
| Polytope Studio Lowpoly Modular Armors Bundle | $102.99 | Modular low-poly armor for medieval register; extension asset | Built-in + URP |
| Fantasy Staffs Pack (Anatoly Valovoy) | $79 | 72 staff variants — deep caster staff (#11) variation if needed | Not confirmed |

**Tier 3 additions total:** $350 + $100 + $103 + $79 = ~$632 additional over Tier 2

**Tier 3 total:** ~$1,082–$1,222

**Tier 3 notable consideration:** The Synty SyntyPass subscription ($30/month) provides access to all Synty packs. If Tier 3 procurement includes Synty Fantasy Kingdom ($350) + Dungeon Realms ($200) + Samurai ($30) + Knights ($100 est.), the subscription pays off in 3 months. For a game in active development over 12+ months, SyntyPass is economically superior to individual Synty pack purchases.

**SyntyPass economics for Tier 3:**
- One-time Synty packs (FK + Dungeon + Samurai + Knights): ~$580
- SyntyPass @ $30/month × 6 months: $180 — 70% cost reduction for equivalent coverage plus 120+ additional packs
- Recommended: SyntyPass over individual Synty purchases at Tier 3 scale

---

## URP Compatibility Verification List — Top 10–15 Priority Packs

These packs require URP verification before commit. Sorted by spend magnitude and risk.

| Pack | Price | URP status | Verification note |
|---|---|---|---|
| Synty POLYGON Fantasy Kingdom | $349.99 | Partially confirmed ("URP conversion tutorial available") | HIGH PRIORITY — largest single spend; confirm native URP vs. manual conversion required |
| Synty POLYGON Dungeon Realms | $199.99 | Not confirmed | HIGH PRIORITY |
| Infinity PBR Weapons & Armor PBR Pack #1 | $60 | Confirmed | Low risk |
| Polytope Studio Lowpoly Modular Armors Bundle | $102.99 | Built-in + URP confirmed; HDRP absent | Medium — confirm URP behavior in current Unity version |
| Bretwalda Rigged Armour Collection | $30 | Not confirmed (2018 release) | MEDIUM PRIORITY — 2018 pack; older URP conversion may be manual |
| Synty POLYGON Samurai Pack | $29.99 | "Built-in + URP" confirmed | Low risk |
| Fantasy Staffs Pack | $79 | Not confirmed | Medium — verify before commit |
| Infinity PBR Weapons & Armor PBR Pack #2 | $60 | Confirmed (mostly) | Low risk |
| EpiXR Japanese Samurai Weapons | $19.99 | Not confirmed | Medium |
| Blink 100+ Bundle Vol. 1 | $69.99 | Confirmed | Low risk |
| Blink 100+ Bundle Vol. 2 | $69.99 | Confirmed | Low risk |

---

## Meshy Gap-Fill Recommendations — Density-Routing

Twelve weapon archetypes and all armor categories have Asset Store options. Three weapon archetypes and two armor categories have NO satisfactory Asset Store option.

### Meshy generation candidates — weapons

| Archetype | Reason for Meshy routing | Suggested prompt approach |
|---|---|---|
| Censer / thurible (#13) | Zero Asset Store packs found in crawl | "Ornate bronze censer thurible on chain, holy fantasy equipment, stylized, plain background, front view" |
| Holy symbol / icon (#14) | Zero Asset Store packs found in crawl | "Fantasy divine holy symbol staff, radiant icon on handle, paladin equipment, stylized game asset, T-pose" |
| War-trumpet / horn (#15) | Zero Asset Store packs found in crawl | "Fantasy war horn instrument, ornate brass, fantasy warrior's trumpet, stylized game asset, side view" |

For each of these, Meshy generates a static prop mesh. These archetypes are held props (hand-bone rigid attachment) — they do NOT require skinning. The weapon pipeline is identical to all other weapons: Meshy generates, texture bakes, export FBX, rigid attach to RightHand bone in Unity. Meshy generation cost is negligible (covered by existing Pro subscription).

### Meshy generation candidates — weapons (thin coverage, consider Meshy supplemental)

| Archetype | Asset Store status | Meshy supplemental value |
|---|---|---|
| Crossbow (#6) | Fragmented (Stylized Fantasy Crossbows exists but no major pack) | Low — one dedicated pack exists; procure from AS first |
| Blunderbuss (#7) | Very thin (flintlock prop exists @ $9.95) | Medium — Blink Muskets & Pistols likely covers; verify inclusion |
| Throwing knives (#8) | Fragmented (shuriken / chakram scattered across packs) | Medium — Synty Samurai has shuriken; consider Meshy for non-Asian throwing knife variants |
| Orb / sphere (#10) | In prop packs, not weapon packs | Low — source from Mega Fantasy Props Pack; Meshy only if stylistic mismatch |
| Tome / grimoire (#12) | One pack (Blink Spellbooks & Wands) has spellbooks; no dedicated tome | Low — Blink pack covers; Meshy for non-spellbook tome variants |

### Meshy generation candidates — armor

| Category | Reason for Meshy routing | Pattern |
|---|---|---|
| Cloak / cape | No pre-rigged cloth-sim cape found on AS | Bake into character mesh (Pattern A); apply Unity Cloth component for simulation |
| Full robe (caster-archetype armor) | Only one pack (o3n Hooded Robe) found; style match uncertain | Bake into character via Meshy (knight in robe = standard Meshy generation) |
| East-Asian armor (lamellar, samurai armor) | No dedicated armor packs in East-Asian register | Bake into Meshy-generated character for that register |
| Dark-grim armor pieces (bone armor, dark plate) | No dedicated dark register armor packs found | Bake into Meshy-generated characters or rigid-attach from Synty Dungeon Realms attachments |

---

## Pipeline Decision: Baked Armor vs. Swappable Armor

This is the load-bearing decision for Profile A armor procurement.

**Option A — Baked armor (recommended for Reincarnated Phase 0):**
- Each spirit/archetype has a Meshy-generated character model with armor baked in
- No runtime swap; armor is part of the visual identity of the spirit
- Zero additional armor procurement cost
- Meshy handles all armor categories (Pattern A fully works)
- URP pipeline unchanged from weapon pipeline

**Option B — Swappable armor (relevant if gear-as-substrate dimension includes visual armor change):**
- Armor equip changes visual appearance at runtime (sword swap AND chest swap visible)
- Requires Skinned Mesh Renderer approach: pre-skinned armor from Asset Store OR manual Blender skinning
- Additional procurement: $30–$80 for Asset Store pre-rigged packs + skeleton mapping verification effort
- Cloth armor (cloak, robe) still requires engineering work regardless (Obi Cloth or Unity Cloth)
- Relevant to the gear-as-substrate design in gear-as-substrate-2026-05-21.md IF armor is a substrate visual dimension

Per `memory/project_gear_and_spirit_guide.md` and gear-as-substrate design: gear is currently defined as weapons only in the 15-archetype catalogue. Armor is not yet confirmed as a substrate visual dimension. If armor lands as a substrate dimension post-W1.15-LITE, the swappable armor path becomes relevant. For Phase 0 and W1.13 / W1.15-LITE scope, baked armor (Option A) is the correct path.

---

## Budget Summary Table

| Tier | Weapons (AS) | Armor (AS) | Meshy gap-fill | Total |
|---|---|---|---|---|
| **Tier 1 — MVS (baked armor)** | $140–180 | $0 | $0 (Meshy Pro covers) | **$140–180** |
| **Tier 1 — MVS (swappable armor)** | $140–180 | $80 | $0 | **$220–260** |
| **Tier 2 — Multi-register (baked)** | $450–490 | $0 | $0 | **$450–490** |
| **Tier 2 — Multi-register (swappable)** | $450–490 | $80 | $0 | **$530–570** |
| **Tier 3 — Comprehensive** | ~$830–900 | $103 | $0 | **~$933–1,003** |
| **Tier 3 with SyntyPass (12mo)** | ~$540 (non-Synty AS) + $360 (SyntyPass 12mo) | $103 | $0 | **~$1,003** |

Note: SyntyPass economics favor Tier 3 only; for Tier 1 / Tier 2, individual pack purchases are more economical.

---

## Recommended Procurement Sequence

**Step 1 (immediate, $0):** Download Blink Free Modular Character and validate the Unity Humanoid Avatar + armor swap + URP pipeline works end to end. This zero-cost validation eliminates skeleton-mismatch risk before any spend.

**Step 2 (Tier 1 weapons, ~$140):** Purchase Blink 100+ Stylized Weapons Bundle Vol. 1 ($69.99) and Vol. 2 ($69.99). These two packs together cover approximately 12–13 of the 15 archetypes in the project's target stylized register. Verify the three gap archetypes (censer, holy symbol, horn) via Meshy generation at no additional cost.

**Step 3 (gap-fill orbs, ~$10–30):** Source orbs/spheres from Mega Fantasy Props Pack or RPG Fantasy Crystal Kit for archetype #10.

**Step 4 (armor decision gate):** Confirm with Matt whether armor is baked (Option A, no additional spend) or swappable (Option B, $30–80 additional). If swappable: verify Bretwalda Rigged Armour Collection URP compatibility, then purchase.

**Step 5 (Tier 2 gate — when multi-register is needed):** Add Synty Samurai ($29.99, East-Asian) after verifying URP. Add Synty Dungeon Realms ($199.99, grimdark) after verifying URP. Total Tier 2 gate spend: ~$230 additional.

**Defer to Tier 3 decision:** Synty Fantasy Kingdom ($349.99), Pure Poly 900 ($99.95), Polytope Studio armor bundle ($102.99). These are depth-of-variation purchases relevant when content volume demands are higher than Phase 0 needs.
