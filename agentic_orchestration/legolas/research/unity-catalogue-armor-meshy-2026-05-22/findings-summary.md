# Findings Summary — Unity Asset Catalogue + Meshy Armor Capability

**Date:** 2026-05-22
**Steward:** legolas (research scout; Mixed Mode A + Mode B; bounded sub-agent run)
**Commissioned by:** Matt, via gandalf-routed dispatch
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-unity-asset-catalogue-armor-meshy.md`
**Note:** This summary file was returned as agent output text during the commission run (sub-agent output constraints prevented direct write); materialized to disk by gandalf 2026-05-22 evening for canonical reference.

---

## Headline Finding 1 — Meshy Armor Capability

Meshy CAN generate all armor categories. The capability splits on usage pattern:

**Baked armor (armor geometry is part of the character mesh):** Fully supported. Meshy generates an armored character, rigs it, exports with Unity Humanoid Avatar-compatible bone weights. This is the clean path for Profile A where each spirit has its own visual model. Zero additional pipeline work beyond what weapons already require.

**Standalone armor piece for runtime equip-swap:** NOT directly supported by Meshy's rigging API. The API documentation is explicit: "currently only works well with standard humanoid (bipedal) assets with clearly defined limbs and body structure." A standalone chest plate has no bipedal anatomy — pose estimation fails, piece exits as static mesh. Rigid attachment works for helmets, pauldrons, gauntlets, and boots (anchor to Head, LeftShoulder, LeftHand, LeftFoot bones respectively). Body armor (chest pieces) requires Asset Store pre-rigged packs or manual Blender skinning. Cloth items (cloaks, full robes) additionally require Unity's Cloth component or Obi Cloth ($55) for physics simulation.

**Decision gate for drax / rocket:** Profile A must confirm — is armor BAKED (spirit-specific visual, no runtime swap) or EQUIPPABLE (gear slot that updates visual)? Baked = $0 additional procurement. Equippable = $80–$130 additional plus skeleton-mapping verification work.

---

## Headline Finding 2 — 15-Archetype Coverage Situation

12 of 15 archetypes have serviceable Asset Store options in the medieval-heroic-European register.

**3 archetypes have NO Asset Store option found:**
1. Censer / thurible (#13) — zero dedicated packs found across 3,545 weapon assets
2. Holy symbol / icon (#14) — zero dedicated packs found
3. War-trumpet / horn (#15) — zero dedicated packs found

These three are Meshy-generation candidates. Critically, all three are held-prop weapons (rigid attach to RightHand bone) — no skinning required. Meshy generates them as static props, pipeline identical to all other weapons. Cost is negligible within existing Meshy Pro subscription.

**4 archetypes have thin or fragmented coverage:**
- Crossbow (#6): one dedicated stylized pack (Stylized Fantasy Crossbows) but no major multi-archetype bundle coverage
- Blunderbuss (#7): one period-accurate prop ($9.95, flintlock); Blink Muskets & Pistols likely covers — confirm inclusion
- Throwing knives (#8): scattered (Synty Samurai has shuriken/kunai; chakram isolated at $17.99); no dedicated throwing-knife pack
- Orb / sphere (#10): found in prop packs (Mega Fantasy Props, RPG Crystal Kit), not weapon category; easy to source, price range $10–30

---

## Headline Finding 3 — Aesthetic Register Density

The Asset Store is heavily concentrated in one register: medieval-heroic-European. This register has redundant coverage at every price point from $0 (KayKit Weapons Bits) to $350 (Synty Fantasy Kingdom).

Other registers:
- **Ancient-East-Asian:** Synty Samurai ($29.99) covers swords/spears/throwing. Magical archetypes (wand, staff, censer, horn) absent in all East-Asian packs found.
- **Dark-grim-European:** Synty Dungeon Realms ($199.99) covers melee family. Magical archetypes absent.
- **South-Asian / Mesoamerican / African / fictional-hybrid:** NO Asset Store coverage found for any of these registers.

**Implication for multi-genre engine:** Any engine profile operating outside medieval-European will rely on Meshy for register-gap-fill more heavily than Asset Store procurement. The score-don't-filter principle applies — procure what the Asset Store has, generate what it doesn't.

---

## Headline Finding 4 — Tier Budget Summary

**Tier 1 (minimum viable for Reincarnated Profile A, baked armor path):** ~$140–$180

- Blink 100+ Stylized Weapons Bundle Vol. 1 ($69.99) + Vol. 2 ($69.99) = $139.98
- Orb / sphere prop pack: $10–30
- Meshy gap-fill for censer, holy symbol, horn: $0 (Pro subscription)
- Armor (baked path): $0

The Blink bundles are the Tier 1 anchor. They match the project's stylized register, cover approximately 12–13 of 15 archetypes, and have confirmed URP + Built-in + HDRP tri-pipeline support.

**Tier 2 (multi-register: add Ancient-East-Asian + Dark-grim-EU):** +$230 → total ~$380–$420
- Synty Samurai: $29.99 (URP confirmed)
- Synty Dungeon Realms: $199.99 (URP verify before commit)

**Tier 3 (comprehensive):** +$600 → total ~$1,000+
- Synty Fantasy Kingdom + Pure Poly 900 Weapons + Polytope Modular Armors bundle

**SyntyPass note at Tier 3:** Synty Samurai + Dungeon Realms + Fantasy Kingdom + Knights Pack purchased individually = ~$580. SyntyPass at $30/month × 12 months = $360 for all 130+ Synty packs. SyntyPass is the economically superior path at Tier 3 scale.

---

## Key Pre-Purchase Verification Items

1. **Synty Fantasy Kingdom ($349.99):** Native URP or manual-conversion-required? Manual conversion = engineering time cost beyond price.
2. **Synty Dungeon Realms ($199.99):** Same URP question. "Tutorial available for URP conversion" implies not natively URP out-of-box.
3. **Bretwalda Rigged Armour Collection ($30):** URP compatibility — 2018 pack, shader upgrade likely needed.
4. **Infinity PBR Armor Pack 1 ($50):** Skeleton matches Unity Humanoid Avatar, or requires Infinity PBR's own character base mesh?
5. **Polytope Studio Modular Armors Bundle ($102.99):** Extension asset — which base character asset is required?

---

## Consumption-Readiness Flags (for drax — G5-LITE)

| Asset | Ready? | Flag |
|---|---|---|
| Blink Stylized Bundles | Yes — FBX static props, full tri-pipeline | GREEN |
| Synty Samurai Pack | Yes with caveat | YELLOW — confirm URP |
| Synty Dungeon Realms | Likely yes | YELLOW — confirm URP |
| Infinity PBR Armor Pack 1 | Needs skeleton check | YELLOW — rig verify |
| Bretwalda Rigged Armour Collection | 2018 pack | YELLOW — URP shader verify |
| Meshy-generated props (censer, horn, holy symbol) | Yes — standard static prop | GREEN |

---

## Cross-Reference Map

| Consumer | Relevant finding |
|---|---|
| **gandalf** (Profile A pipeline doc) | Meshy baked armor is clean; swappable armor needs work. Tier 1 = $140–$180. Three archetypes are Meshy-only. |
| **Matt** (procurement) | Tier 1/2/3 budget table in `procurement-recommendation.md`. SyntyPass favorable at Tier 3 scale. |
| **drax** (G5-LITE) | Armor pattern decision (baked vs. swappable) is load-bearing for integration design. Consumption-readiness flags above. |
| **rocket** (W1.15-LITE) | Armor not confirmed substrate dimension yet. Baked armor = no new engine work. Swappable armor = new gear slot + Skinned Mesh Renderer swap system needed. |
| **knight-rider** (W1.7 / W1.7b) | Three weapon archetypes are Meshy-only (censer, holy symbol, horn). Procurement sequence detailed in `procurement-recommendation.md` (5-step). |

---

## Related artifacts (this directory)

- `meshy-armor-capability.md` — Priority 1 full findings; armor pattern A-D analysis
- `weapons-catalogue.md` — Priority 2 weapons enumeration; publisher-organized; per-archetype coverage matrix
- `armor-catalogue.md` — Priority 2 armor enumeration; body-part-coverage matrix
- `procurement-recommendation.md` — Tier 1/2/3 budget framing; 5-step procurement sequence; pre-purchase verification list

---

**Signed (research):** legolas (research scout; Mode A + Mode B mixed; commission complete)
**Materialized to disk by:** gandalf, 2026-05-22 evening
**For:** Profile A asset-pipeline-meshy-swap canonical doc finalization; Matt procurement decisions; drax G5-LITE Unity integration scoping; knight-rider protocol v1.3 → v1.4 W1.7 amendment.
