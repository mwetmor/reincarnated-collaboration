# Unity Asset Store — Initial VFX Survey

**Date:** 2026-05-20
**Phase:** 1 — Reconnaissance
**Sources:** Unity Asset Store individual pack pages (via WebFetch); Unity Asset Store search results (via WebSearch)
**Total packs cataloged:** 22

---

## Summary

The Unity Asset Store VFX/Particles/Spells category contains approximately 502 packs as of this survey date. The major publishers producing ARPG-quality VFX are: Hovl Studio, Archanor VFX, kripto289, Piloto Studio, SineVFX, and Gabriel Aguiar Prod.

**Key findings:**
1. Fire VFX coverage is excellent — multiple high-quality packs at every price point including a well-regarded free entry (Fire & Spell Effects, 266 reviews).
2. Axis 4 (defensive) — aura/shield/buff packs exist and are cataloged, but the dedicated defensive-profile VFX category is shallower than offensive VFX.
3. Axis 2A (proxy) — only one pack found explicitly covering summon/proxy spawn VFX (VFX Graph - Summon Creatures Vol.1); it requires URP/HDRP (no Built-in support) which constrains pipeline.
4. Axis 1 (mobility) — exactly one specialized movement VFX pack found (Ultimate Movement FX). This is a potential procurement gap.
5. Style register concern: several high-review packs (kripto289 Realistic Effects Pack 4) are realistic-register, which may not match the ChatGPT→Meshy→Mixamo stylized output. This needs style-coherence verification in Phase 2.
6. URP compatibility is broadly available but not universal — Built-in-only packs exist (SineVFX Aura and Ground Effects) and VFX Graph packs require URP/HDRP.

---

## Catalog by BC Axis Coverage

### Axis 2 — Damage Geometry

**Best multi-geometry coverage packs:**
- RPG VFX Bundle (Hovl Studio, $48) — 51 reviews, covers all 5 bins, Built-in+URP+HDRP
- 70 Fantasy Spells Effects Pack (GAPH, $16) — 32 reviews, 70 confirmed spells
- Elemental Spells Full Pack VFX (PixPlays Studio, $36) — 13 reviews, 24 spells across 4 elements + multiple geometry types

**Best single-geometry depth:**
- Aoe Spell Vfx Set (XAL, $10) — AOE-specific but low adoption
- MOBA / ARPG Effect Pack (Kalamona, $19) — 231 reviews, ARPG-specific design

### Axis 4 — Defensive Profile (aura/shield/buff)

- Auras Buffs and Shields (Piloto Studio, $15) — 5 reviews, 5 stars, full tri-pipeline
- Magic Auras, Buffs and Shields VFX Pack (Piloto Studio, $25) — larger pack, recent release
- Magic Buffs and Auras VFX (Piloto Studio, $15) — newest of Piloto buff family
- Aura and Ground Effects (SineVFX, $20) — Built-in only (pipeline constraint)
- Ultimate Aura VFX Pack (Hovl Studio, $17) — recent Hovl aura-specific pack

### Axis 2A — Proxy Density

- VFX Graph - Summon Creatures Vol.1 (Gabriel Aguiar Prod, $12) — URP/HDRP only; tiger/phoenix/dragon summon effects

**Assessment:** This axis is the most VFX-starved relative to need. One pack found. Phase 2 should specifically target summon/totem/minion spawn VFX.

### Axis 1 — Engagement / Mobility

- Ultimate Movement FX — Dash, Blink & Speed Trails (TvitchiVFX, $30) — URP only, 35 favorites, low adoption
- Action RPG FX (Archanor VFX, $20) — includes portal effects which approximate teleport VFX

**Assessment:** Mobility VFX is a relative gap. One specialized pack found.

---

## Pack Detail Cards

### Pack 1: RPG VFX Bundle — Hovl Studio
- **URL:** https://assetstore.unity.com/packages/vfx/particles/spells/rpg-vfx-bundle-133704
- **Price:** $48 | **License:** Single Entity | **Reviews:** 51 | **Favorites:** 1714
- **Render pipeline:** Built-in + URP + HDRP
- **Keywords:** VFX / Magic / Effects / Fire / Spell / Projectiles / Shield / Lightning / Stylized / RPG
- **BC coverage:** Axis 2 all 5 bins; Axis 4 mitigator (shield)
- **Style:** Stylized | **Element coverage:** Fire / lightning / neutral
- **Assessment:** Hovl Studio flagship bundle. Best multi-axis single-pack option. High adoption and broad pipeline support. Dependency on Hovl support package ($5) is minor. Requires Phase 2 asset-count + asset-type deep audit.

### Pack 2: Fire & Spell Effects — Digital Ruby
- **URL:** https://assetstore.unity.com/packages/vfx/particles/fire-explosions/fire-spell-effects-36825
- **Price:** FREE | **Reviews:** 266 | **Favorites:** 3347
- **Render pipeline:** Built-in + URP + HDRP
- **Keywords:** flamethrower / meteor / swarm / burn / ring / wall / strike / sparks / smoke
- **BC coverage:** Axis 2 small-AOE + large-AOE + projectile; fire element dominant
- **Style:** Stylized | **Element coverage:** Fire primary
- **Assessment:** Best free fire VFX option. Exceptional adoption (266 reviews is very high for free asset). Geometry keywords align well with fire element kit needs. Worth including in procurement baseline.

### Pack 3: Magic Arsenal — Archanor VFX
- **URL:** https://assetstore.unity.com/packages/vfx/particles/spells/magic-arsenal-20869
- **Price:** $30 | **Reviews:** 246 | **Favorites:** 3411
- **Render pipeline:** Built-in + URP (no HDRP)
- **Keywords:** FX / particles / missile / explosion / fire / magic / spell / elemental
- **BC coverage:** Axis 2 single-target + small-AOE + large-AOE + chain; multi-element
- **Style:** Stylized | **Element coverage:** Fire / lightning / neutral / arcane
- **Assessment:** High-adoption Archanor pack. No HDRP support is minor constraint for Reincarnated (mobile target). Updated Dec 2024 — active maintenance.

### Pack 4: Elemental Spells Full Pack VFX — PixPlays Studio
- **URL:** https://assetstore.unity.com/packages/vfx/particles/spells/elemental-spells-full-pack-vfx-297318
- **Price:** $36 | **Reviews:** 13 | **Favorites:** 288
- **Render pipeline:** Built-in + URP (no HDRP)
- **Content confirmed:** 24 elemental spells of Water / Earth / Wind / Fire types. Shield / AOE / Projectile / Aura / Blast / Beam spell types.
- **BC coverage:** Axis 2 all 5 bins; Axis 1 all engagement types (beam/blast for ranged; AOE for mid-range)
- **Style:** Stylized | **Element coverage:** Fire / water / earth / wind — the 4 canonical rotating elements
- **Assessment:** Best element diversity of any single pack found. Explicitly covers all 4 core elements with multiple geometry types per element. Low review count reflects recent release (Dec 2025) not quality. High priority for Phase 2 deep audit.

### Pack 5: Magic Effects FREE — Hovl Studio
- **URL:** https://assetstore.unity.com/packages/vfx/particles/spells/magic-effects-free-247933
- **Price:** FREE | **Reviews:** 55 | **Favorites:** 3570
- **Render pipeline:** Built-in + URP + HDRP
- **Content:** Magic circles / explosions / sparks / portals / slashes / hit effects
- **BC coverage:** Axis 2 small-AOE + projectile; aura
- **Style:** Stylized | **Element coverage:** Neutral / arcane
- **Assessment:** Free sampler from Hovl Studio. Useful for pipeline validation without procurement cost.

### Pack 6: Action RPG FX — Archanor VFX
- **URL:** https://assetstore.unity.com/packages/vfx/particles/action-rpg-fx-38222
- **Price:** $20 | **Reviews:** 26 | **Favorites:** 883
- **Render pipeline:** Built-in + URP (no HDRP)
- **Content:** Portal / loot / particle impact effects — ARPG top-down visual language
- **BC coverage:** Axis 2 small-AOE + large-AOE + projectile; Axis 1 mobility (portal)
- **Style:** Stylized | **Element coverage:** Neutral / arcane / physical
- **Assessment:** ARPG-specific design intent. Portal effects serve teleport/blink geometry. Updated Sep 2024.

### Pack 7: Auras Buffs and Shields — Piloto Studio
- **URL:** https://assetstore.unity.com/packages/vfx/particles/auras-buffs-and-shields-233838
- **Price:** $15 | **Rating:** 5 stars / 5 reviews | **Favorites:** 89
- **Render pipeline:** Built-in + URP + HDRP
- **Content:** Stylized aura / buff / shield particle systems. Cartoon aesthetic.
- **BC coverage:** Axis 4 tank + mitigator; Axis 2B mixed (status indicators)
- **Style:** Stylized/cartoon | **Element coverage:** Neutral / arcane
- **Assessment:** Solid small pack for defensive profile VFX. Full pipeline support. 5-star rating (small sample).

### Pack 8: MOBA / ARPG Effect Pack — Kalamona
- **URL:** https://assetstore.unity.com/packages/vfx/particles/moba-arpg-effect-pack-120799
- **Price:** $19 | **Reviews:** 231 | **Favorites:** 183
- **Render pipeline:** Listed as 2018.1+ — likely Built-in (unconfirmed)
- **Content:** MOBA and ARPG visual effects — specific content not extractable from page
- **BC coverage:** Axis 2 all bins likely; Axis 1 all engagement types
- **Style:** Stylized | **Element coverage:** Unknown — needs Phase 2 deep audit
- **Assessment:** 231 reviews is exceptional for a $19 pack. MOBA/ARPG-specific design. Older pack (2018) but high adoption suggests durable quality. Small file size (6.7MB) raises question about content count — needs deep audit.

### Pack 9: VFX Graph — Summon Creatures Vol. 1 — Gabriel Aguiar Prod
- **URL:** https://assetstore.unity.com/packages/vfx/vfx-graph-summon-creatures-vol-1-250854
- **Price:** $12 | **Reviews:** insufficient | **Favorites:** 61
- **Render pipeline:** URP + HDRP only (no Built-in) — VFX Graph dependency
- **Content:** 8+ summon effects: tiger / phoenix / dragon creatures
- **BC coverage:** Axis 2A proxy-heavy spawn VFX; Axis 2 multi-spawn
- **Style:** Stylized | **Element coverage:** Neutral / nature / arcane
- **Assessment:** Only summon-specific VFX pack found. Pipeline constraint (VFX Graph = no Built-in). If project targets URP, this is the primary Axis 2A VFX option.

### Pack 10: Mesh Effects — kripto289
- **URL:** https://assetstore.unity.com/packages/vfx/particles/spells/mesh-effects-67803
- **Price:** $23 | **Reviews:** 221 | **Favorites:** 7347
- **Render pipeline:** HDR capable; Mobile + VR — likely Built-in + URP
- **Content:** Mesh-attached magical effects
- **BC coverage:** Axis 2 single-target + small-AOE; Axis 4 mitigator (body aura)
- **Style:** Stylized | **Element coverage:** Neutral / arcane / dark
- **Assessment:** Extremely high favorite count (7347) — persistent utility across many projects. Body/weapon-attached effects directly compatible with Mixamo bone anchoring.

---

## Publisher Quality Tiers

**Tier 1 — High confidence (multiple high-review packs):**
- Hovl Studio: RPG VFX Bundle (51 reviews), Magic Effects FREE (55 reviews)
- Archanor VFX: Magic Arsenal (246 reviews), Action RPG FX (26 reviews)
- kripto289: Mesh Effects (221 reviews), Realistic Effects Pack 4 (270 reviews), Magic Effects Pack 1 (70 reviews)

**Tier 2 — Moderate confidence:**
- Piloto Studio: Multiple aura/buff packs (small review counts but 2025 releases)
- GAPH: 70 Fantasy Spells (32 reviews)
- Kalamona: MOBA/ARPG Effect Pack (231 reviews — high confidence for Tier 2)

**Tier 3 — Low confidence (recent/unproven):**
- PixPlays Studio (recent release, low reviews)
- IndieImpulse Ultimate Elemental Magic VFX (very recent, no reviews)
- TvitchiVFX Ultimate Movement FX (no reviews)
- XAL Aoe Spell Vfx Set (no reviews)

---

## Critical Gaps Requiring Phase 2 Focus

1. **Lightning VFX** — No dedicated lightning-specific pack found. Realistic ARPG VFX Starter Pack - Lightning Spells exists ($38, Piloto Studio) but is in the realistic style register. Need lightning packs in stylized register.
2. **Earth/Stone VFX** — No dedicated earth element pack found. Elemental Spells Full Pack covers it but needs deep audit.
3. **Wind/Air VFX** — Same — no dedicated wind pack.
4. **Holy/Shadow VFX** — No packs covering the Phase-1 P1 substrate expansion elements (lightning/holy/shadow) except incidentally.
5. **Proxy/Summon spawn VFX** — Only one pack (VFX Graph - Summon Creatures) and it has a pipeline constraint.
6. **Mobility/movement VFX** — Only one pack (Ultimate Movement FX) and it has low adoption + URP-only.
7. **CC status effect VFX** — Freeze/stun/root/shock visual indicators not explicitly found as a dedicated pack. Piloto Studio's aura packs may cover this.
