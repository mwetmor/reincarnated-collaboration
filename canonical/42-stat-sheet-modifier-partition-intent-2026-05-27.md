# 42 — Stat-Sheet Modifier Partition Intent (Wave 1 Cycle 13 — 2026-05-27)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — Wave 1 partition design INTENT canonical for Cycle 13 stat-sheet partition cycle; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Wave 1 partition design intent; 9-category × 11-slot affinity matrix operationalized + per-rarity grid + tier-restricted modifier surface + sample modifier enumerations + 6 principles + SC-4 5 methodology gates closure + minimum-viable trait integration + Wave 1 implementation guidance for rocket
**Authority:** Matt 2026-05-27 verbatim — "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope. No further Matt-creative-ratification gates on Cycle 13 progression."
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow Phase 2d spec-driven gear gen
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86 + 2026-05-27 amendments)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid + ~30-day seasonal duration framework
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker (Phase 2d entries reference this doc)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — Matt + gandalf Pattern-B session closeout (Block B substantive content)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` — Verdicts B.2/B.3/B.4 (load-bearing for partition intent)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md` — legolas SC-4 (5 methodology gates closure substrate)
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` — legolas SC-4 expansion; **Wave-1-informing:** 9-category architectural verification (confirms 9-cat × 11-slot is "architecturally sound and non-standard by design"; documents 3 specific cross-ARPG divergences — Crit split, Build-identity unique, Resistance-Penetration combined direction — none requiring amendment); **Wave-2-informing:** 5th Scaling-interaction synergy category candidate + Pass 1/Pass 2 empirical validation methodology for Discipline #32 first-do-no-harm; **Wave-4-informing:** Pattern 9 + Pattern 10 degenerate-state catalog candidates for sim detection methodology
- `canonical/story/off-hand-items-2026-05-24.md` — off-hand items operational definition (6 categories)
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR / INT / WIS / DEX)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational truth

---

## 0. TL;DR

Wave 1 partition design intent for Cycle 13 stat-sheet modifier partition cycle. Locks the **9-category × 11-slot affinity matrix** operationalized with weighted probability per slot per category (graduated affinity, not binary). Locks the **per-rarity × per-slot grid** for modifier count + categories rollable + added-skill content gate. Locks the **tier-restricted modifier surface** (~10-20% of modifier types tier-restricted to Epic+/Legendary+/Tier-1+2). Provides **sample modifier enumerations** per category per slot family (informs Wave 1 rocket implementation; not exhaustive). Locks the **6 principles** for partition discipline. Closes the **SC-4 5 methodology gates** (prefix/suffix binary ADOPTED; tag taxonomy DEFERRED to v1.1+; item-type domain LOCKED; skill-level affix slot restriction LOCKED; proc/trigger routing LOCKED HYBRID). Operationalizes the **minimum-viable trait integration** (55-entry pool absorbed via supporting chain per closeout § 2.1 Option C). Provides **Wave 1 implementation guidance** for rocket (main_weapon routing cleanup SC-1 embedded; cross-reference elrond seam; affinity matrix probability weight calibration approach; tier-restriction enforcement). Wave 1 close criterion = jack-ryan Gate-2 PASS on rocket implementation against this intent.

---

## 1. Architectural foundation cross-references

This doc operationalizes design intent grounded in the locked architectural foundation:

| Foundation doc | What it provides | Where this doc operationalizes |
|---|---|---|
| **Doc 38** (delivery strategy D1-D10) | Variant C engine-vs-game + isekai provisional + ~30-day seasonal | Composes with § 11 |
| **Doc 39** (QD-engine workflow Architecture B) | Phase 2d spec-driven gear gen substrate-bound | Wave 1 implements per Phase 2d (§ 9) |
| **Doc 40** (Cycle 13 architectural foundation, post-amendments) | 9-category char sheet surface (§ 3.6 + amendments); 11-slot taxonomy; capability toolkit (§ 3.3); D54/D55 added-skill rules; D33+D38+D51 content-compositional attunement; D80 gap-filling discipline | This doc IS the partition operationalization of § 3.6 architecture |
| **Doc 41** (L50 hybrid progression framework) | L1-L50 cap + content-tier-driven endgame; node-to-level-band mapping; 4 progression nodes | Per-rarity grid composes with tier mapping to player level bands per § 3 |
| **Closeout doc 2026-05-27** | Substantive content: 9-cat surface lock; 11-slot taxonomy; per-rarity grid; affinity matrix; 6 principles; T4 algorithm 3-cat taxonomy; content-compositional attunement; trait absorption | Source authority for all locks in this doc |
| **8-axis BC lock** | 68,040 cells; operational measurement coordinate system | Cohort-cross-cohesion validation (principle 6) operates on BC-axis cells |
| **8-model resource catalog** (closeout § 2.2) | Mana / Cooldown / Stamina / Rage / Energy / Channeled / Combo / Health-as-resource | Resource-model-gated principle 3; per-slot affinity matrix Resource category gates per kit class resource model |

**Authority basis:** Matt + gandalf Pattern-B session 2026-05-27 closeout § 3.1-3.3 + Verdicts B.2/B.3/B.4 (B.4 RATIFIED standalone in commit `c983173`; B.2/B.3 substantive content carried forward into this doc as operationalized intent per Matt's Cycle 13 autonomous-scope ratification 2026-05-27).

---

## 2. 9-category × 11-slot affinity matrix — operationalized

Per principle 1 (graduated affinity, not binary): **every slot CAN roll any category but with weighted probability per affinity tier.**

**Weighted probability tiers:**

| Affinity tier | Weighted probability per slot per category |
|---|---|
| **Primary** | ~50% (slot's dominant identity for that category) |
| **Secondary** | ~30% (slot rolls this regularly but not dominantly) |
| **Tertiary** | ~15% (slot rolls this occasionally) |
| **Off-affinity** | ~5% (slot rolls this rarely; preserves gap-filling capability) |

**Affinity tier weights are RELATIVE, not absolute percentages.** The 50/30/15/5 values above are RELATIVE per-tier weights to be NORMALIZED per slot during implementation per § 9.2 step 2 normalization procedure. The raw per-slot tier-weight sum is NOT 100% before normalization — because multiple categories share the same tier label (e.g., a slot may have 3 Primary categories at weight 50 each), raw sums range ~190-255 per slot across the matrix. Implementation MUST apply the per-slot normalization in § 9.2 step 2 (sum of normalized weights per slot = 1.0) before sampling. The specific distribution of categories across the 4 tiers varies per slot per affinity-matrix entry; the normalization step is what produces the per-slot probability distribution that sums to 1.0.

### 2.1 Full affinity matrix (9 categories × 11 slots)

Categories: (1) Damage / (2) Defense / (3) Resource / (4) Crit / (5) Speed / (6) Resistance-Penetration / (7) On-trigger / (8) Build-identity / (9) Utility-Meta-progression

Slots: Main-hand / Off-hand / Head / Chest / Hands / Feet / Legs / Amulet / Ring × 2 / Belt

| Slot | Damage | Defense | Resource | Crit | Speed | Res/Pen | On-trigger | Build-ID | Util/Meta |
|---|---|---|---|---|---|---|---|---|---|
| **Main-hand (main_weapon)** | **Primary** | Off | Tertiary | **Primary** | **Secondary** | Secondary | **Primary** | Tertiary | Off |
| **Off-hand (secondary_item)** | Secondary | Secondary | Secondary | Tertiary | Tertiary | Secondary | Secondary | **Primary** | Tertiary |
| **Head** | Tertiary | Secondary | Tertiary | Secondary | Off | **Primary** | Tertiary | **Primary** | Off |
| **Chest** | Tertiary | **Primary** | **Primary** | Off | Off | Secondary | Secondary | Secondary | Off |
| **Hands** | Secondary | Secondary | Tertiary | Secondary | **Primary** | Tertiary | Secondary | Tertiary | Off |
| **Feet** | Off | **Primary** | Secondary | Off | **Primary** | Secondary | Tertiary | Off | Off |
| **Legs** | Tertiary | **Primary** | Secondary | Off | Tertiary | **Primary** | Off | Tertiary | Off |
| **Amulet** | Secondary | Secondary | Secondary | Secondary | Off | **Primary** | Tertiary | **Primary** | Tertiary |
| **Ring × 2** | Secondary | Tertiary | Secondary | **Primary** | Secondary | **Primary** | Tertiary | Tertiary | Off |
| **Belt** | Tertiary | Secondary | **Primary** | Off | Tertiary | Tertiary | Secondary | Tertiary | **Primary** |

**Off-hand sub-table (per off-hand category per `canonical/story/off-hand-items-2026-05-24.md`):** the off-hand row above is the aggregate; specific categories skew differently:

| Off-hand category | Damage | Defense | Resource | Crit | Speed | Res/Pen | On-trigger | Build-ID | Util/Meta |
|---|---|---|---|---|---|---|---|---|---|
| Shield | Off | **Primary** | Off | Off | Off | **Primary** | Secondary | Secondary | Off |
| Tome | Off | Tertiary | **Primary** | Secondary | Secondary | Off | Secondary | Secondary | Off |
| Banner | Off | Off | Tertiary | Off | Off | Off | Secondary | **Primary** | Secondary |
| Focus | **Primary** | Off | Secondary | **Primary** | Off | Secondary | Secondary | Tertiary | Off |
| Horn | Off | Tertiary | Tertiary | Off | Off | Off | **Primary** | **Primary** | Off |
| Talisman | Tertiary | Tertiary | Off | Tertiary | Off | Tertiary | Tertiary | Secondary | **Primary** |
| Dual-wield-secondary | **Primary** | Off | Tertiary | **Primary** | **Secondary** | Tertiary | Secondary | Tertiary | Off |

**Matrix design rationale:**
- **Main-hand** = weapon-as-damage-engine identity (Damage + Crit + On-trigger triple-primary; Speed secondary for weapon-style differentiation)
- **Off-hand** = build-identity surface (varies per category; each off-hand provides a distinct identity vector)
- **Head** = sensory-cognitive locus (Res/Pen primary; Build-ID primary for class-distinctive helms)
- **Chest** = body-defense locus (Defense + Resource dual-primary; ARPG genre convention)
- **Hands** = action-execution locus (Speed primary for attack/cast cadence)
- **Feet** = movement locus (Defense dodge + Speed movement dual-primary)
- **Legs** = endurance locus (Defense + Res/Pen dual-primary; tank/sustain identity)
- **Amulet** = mystical-amplification locus (Res/Pen + Build-ID dual-primary per LE/PoE precedent for skill-level affixes)
- **Ring × 2** = stat-tuning locus (Crit + Res/Pen dual-primary; ARPG genre convention for "perfect roll" rings)
- **Belt** = utility-and-resource locus (Resource + Util/Meta dual-primary; belt slot in D4 is utility-flask analog)

**Substrate-led-discipline preservation:** the matrix is an INTENT anchor; rocket's Wave 1 implementation refines via per-slot probability calibration against generated kit content. If empirical signal shows certain categories consistently fail to land at primary-tier probability (~50%), the matrix iterates per cross-season learning D25.

### 2.2 Resource model gating (per principle 3)

The Resource category column in the affinity matrix is **gated by class resource model** (per 8-model catalog closeout § 2.2 + doc 40 § 6). Cross-resource rolls DO NOT APPEAR.

| Class resource model | Resource modifiers that can appear |
|---|---|
| Mana | mana max, mana regen, mana cost reduction |
| Cooldown | cooldown reduction (universal + per-skill) |
| Stamina | stamina max, stamina regen, stamina cost reduction |
| Rage / Fury | rage generation, rage decay, rage cap |
| Energy | energy generation, energy max |
| Channeled | channel efficiency, channel duration |
| Combo / Charges | combo retention, combo cap |
| Health-as-resource | HP-cost efficiency, HP regen on resource spend |

Hybrid resource models (closeout § 2.2 "hybrid models permitted per kit identity") roll modifiers from BOTH applicable model surfaces; specific hybrid-bin-to-model mapping is rocket Phase 2a kit composition work.

---

## 3. Per-rarity × per-slot grid

Per closeout § 3.2 + Verdict B.2 + doc 40 § 3.5 tier structure. Specific modifier counts + categories rollable + added-skill content gate.

| Rarity | Modifier count | Categories rollable | Added-skill content | T4-attunement annotation |
|---|---|---|---|---|
| **Common** | 1-2 | 1-3 (Damage / Defense / Resource only) | No | No |
| **Uncommon** | 2-3 | 1-6 (Damage / Defense / Resource / Crit / Speed / Res-Pen) | No | No |
| **Rare** | 3-4 | 1-6 + 9 (adds Util/Meta-progression) | No | No |
| **Epic** | 4-5 | 1-9 (full 9-category surface) | No | No |
| **Legendary T0** (early-game) | 4-5 + Epic-exclusion modifiers (D56) | 1-9 + legendary-exclusive modifier surface (capability toolkit slot) | Yes — chain-aligned (triggered-passive dominant per D55) | No |
| **Legendary T0.5** (mid-game) | Higher density (5-6 + capability + triggered-passive) | 1-9 + legendary-exclusive | Yes — chain-aligned | No |
| **Legendary T1** (endgame entry) | Higher density + T4-attunement annotation | 1-9 + legendary-exclusive + T4-attunement annotation (metadata) | Yes — **chain + T4-attuned** | **Yes (1 attunement)** |
| **Legendary T2** (endgame) | Highest density + T4-attunement annotation | Same + dual-attunement variants + rare true-active | Yes — chain + T4-attuned + rare true-active (weapon-only per D55) | **Yes (1-2 attunements)** |
| **Unique T0-T2** | Per tier (parallels legendary); signature-mod patterns | Same as legendary at tier | Per tier (same as legendary) | Per tier |
| **Set T1-T2** (endgame-only) | Per tier + set-bonus rank | Same as legendary at tier | Yes — chain + T4-attuned + set-cohesive | Yes (set-level attunement per D35) |

**Added-skill content gate (per D54 + D55):**
- **Added-skill triggered-passive:** LEGENDARY-EXCLUSIVE (all tiers); high probability on weapons; armor on-being-hit; other slots general passive
- **Added-skill true-active:** EXTREMELY RARE, WEAPONS ONLY (Tier-1+2 legendaries); roll probability ~0.5% per legendary weapon drop at Tier 1; ~1.5% at Tier 2
- **Rare/Epic NEVER roll added-skill content** (per D54/D55 + SC-4 cross-ARPG consensus that mechanic-adjusting / spatial-adjusting / axis-adjusting + added-skill modifiers are LEGENDARY-EXCLUSIVE in all 4 reference ARPGs)

**T4-attunement gate (per D33 + D51 amended):**
- **Tier 0 + Tier 0.5 legendaries:** chain-alignment annotation only (NO T4-attunement)
- **Tier 1 + Tier 2 legendaries:** chain + T4-attunement annotation (metadata; per content-compositional attunement closeout § 3.4)
- **All sets (T1 + T2):** chain + T4-attuned + set-cohesive (set-level T4 attunement per D35)

**Density gradient (per closeout § 3.2):** higher tier = higher density of modifiers (more rolls per gear instance). Density progression follows the modifier count column above. Density IS part of the rarity-power escalation pattern (per Pattern R1 quantity escalation per SC-4 § S2).

---

## 4. Tier-restricted modifier surface enumeration

Per principle 2 (tier-restricted modifiers): **~10-20% of modifier types are tier-restricted regardless of slot affinity.** Tier-restriction is a SEPARATE constraint from slot affinity — a slot may have primary affinity for a category, but specific modifier TYPES within that category may be tier-restricted.

### 4.1 Epic+ exclusive modifier types

Modifier types that ONLY roll on Epic or higher rarity (NOT on Common/Uncommon/Rare):

| Category | Modifier type | Rationale |
|---|---|---|
| Damage | % critical strike multiplier (crit bonus damage) | Higher-magnitude crit bonus is endgame-power-escalation; D4 / PoE2 precedent |
| Defense | % damage reduction (generic; non-element-specific) | Generic DR is high-leverage; reserve for Epic+ |
| Resource | % resource cost reduction (universal) | Universal cost reduction is power-density modifier; Epic+ only |
| Crit | % crit chance (above ~10% base) | High crit chance is endgame-power |
| Speed | % cooldown reduction (universal) | Universal CDR is high-leverage; Epic+ only |
| Res/Pen | % element penetration | Penetration is endgame-shape; Epic+ only |
| On-trigger | on-crit / on-element-cast triggers | Higher-order triggers are Epic+ only; on-hit triggers can roll Rare+ |
| Build-identity | class-intrinsic supporting-chain investment bonus | Class-identity modifiers are Epic+ for build-identity preservation |
| Util/Meta | currency drop rate / experience boost | Meta-progression modifiers are Epic+ only |

### 4.2 Legendary+ exclusive modifier types

Modifier types that ONLY roll on Legendary or higher rarity (NOT on Rare/Epic):

| Category | Modifier type | Rationale (per SC-4 finding 1 + closeout § 3.1 discipline lock) |
|---|---|---|
| Capability toolkit (cross-category) | Mechanic-adjusting | Cross-ARPG consensus: LEGENDARY-EXCLUSIVE in all 4 reference ARPGs |
| Capability toolkit (cross-category) | Spatial-adjusting | Same |
| Capability toolkit (cross-category) | Axis-adjusting (damage type or resource axis conversion) | Same |
| Added-skill triggered-passive | (all variants) | Per D54 + D55; weapon-dominant; armor on-being-hit; other slots general passive |
| On-trigger | on-block / on-dodge (defensive triggers tied to specific defensive mechanics) | Composes with capability-toolkit-as-legendary-exclusive |
| Build-identity | T4-attunement annotation | Per D33 + D51 amended; metadata only; Tier 1+2 only |

### 4.3 Tier-1+2 legendary exclusive modifier types

Modifier types that ONLY roll on Tier-1 or Tier-2 legendaries (NOT on Tier-0 or Tier-0.5 legendaries):

| Category | Modifier type | Rationale |
|---|---|---|
| Capability toolkit | Added-skill true-active (weapon-only; extremely rare per D55) | Endgame chase content; Tier-1 ~0.5%; Tier-2 ~1.5% |
| Build-identity | T4-attunement annotation | Per D33 + D51 amended; endgame-exclusive |
| Capability toolkit | Dual-capability rolls (2 capability toolkit slots on same gear instance) | Tier-2 endgame chase pattern; rare even on Tier-2 |
| Build-identity | Set-bonus rank (set items only; T1-T2 sets) | Per D48 endgame-only |

### 4.4 Tier-restricted modifier ratio audit

**Total estimated modifier surface (per Verdict B.3 + per-category estimate):**

| Source | Estimated count |
|---|---|
| 9-category numerical modifier surface (per Verdict B.3 32 modifier types) | ~32 baseline types |
| Capability toolkit modifier surface (legendary-exclusive) | ~5 capability categories × variants ≈ ~15-20 effective types |
| T4-attunement metadata + set-bonus rank | ~2 categories (Tier-1+2 only) |
| **TOTAL** | **~50 effective modifier types** |

**Tier-restricted fraction:**

| Restriction level | Estimated count | Fraction of total |
|---|---|---|
| Epic+ exclusive | ~9 modifier types | ~18% |
| Legendary+ exclusive | ~5 categories (~15-20 variants) | ~30-40% (capability toolkit dominates) |
| Tier-1+2 exclusive | ~4 modifier types | ~8% |
| **Overall tier-restricted** | **~18-23 of ~50 effective types** | **~35-45%** |

**Note:** the doc 40 § 3.6 architectural-intent figure was "~10-20%" tier-restricted; this enumeration arrives at ~35-45% when counting capability toolkit modifiers as separate types from the baseline 32 numerical modifiers. The architectural intent likely meant "~10-20% of the BASELINE 32 numerical modifier types are tier-restricted" (which yields the ~18% Epic+-exclusive count above). Capability toolkit is a SEPARATE surface that is wholly legendary-exclusive by design (per SC-4 finding 1 + D54). Rocket implementation should treat the two surfaces as architecturally distinct: baseline 32 numerical modifiers (with ~18% Epic+ tier-restricted) + capability toolkit (wholly legendary-exclusive; ~5 categories).

---

## 5. Sample modifier enumerations per category per slot family

Per dispatch § B item 5: 5-10 EXAMPLE modifiers per category per slot family (NOT exhaustive; informs Wave 1 implementation; rocket extends + jack-ryan critiques).

**Slot families** (groupings for sample enumeration purposes):
- Weapon (main-hand + dual-wield-secondary)
- Off-hand (per category)
- Armor (head / chest / hands / feet / legs)
- Accessory (amulet / ring / belt)

### 5.1 Damage category — sample modifiers per slot family

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +N flat physical damage; (2) +N flat elemental damage (per element); (3) +X% increased weapon damage; (4) +X% increased elemental damage (per element); (5) +X% increased spell damage; (6) +X% increased melee damage; (7) +X% increased ranged damage; (8) +X% damage vs. enemies above N% HP; (9) +X% damage vs. enemies below N% HP; (10) +X% damage on first hit |
| Off-hand | (1) +N flat elemental damage (per element); (2) +X% increased spell damage (tome / focus); (3) +X% damage if dual-wielding (dual-wield-secondary); (4) +X% damage while shield equipped (banner-buff); (5) +X% damage to summoned units (banner); (6) +X% damage if low-HP (talisman) |
| Armor | (1) +X% damage from gear-bound element (chest / hands); (2) +N flat damage to next melee attack (gloves); (3) +X% damage while moving (boots); (4) +X% damage if in cover-state (legs); (5) +X% damage on entering combat (chest); (6) +X% damage to bleeding enemies (gloves) |
| Accessory | (1) +N flat damage (per damage type); (2) +X% increased damage (universal); (3) +X% damage per nearby enemy (ring); (4) +X% damage if alone (amulet); (5) +X% damage per stack of [resource] (ring); (6) +X% damage if recently crit (belt) |

### 5.2 Defense category — sample modifiers per slot family

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% block chance (weapon-implicit for one-handed); (2) +X% parry chance (one-handed); (3) +N HP on kill (weapon-themed sustain) |
| Off-hand | (1) Shield: +N flat armor; +X% block chance; +X% block effectiveness; +N HP; (2) Tome: +N max HP / energy shield; (3) Banner: +X% all party defense; (4) Talisman: +X% chance to avoid one-shot |
| Armor | (1) +N flat armor (chest dominant; head/legs secondary); (2) +X% increased armor; (3) +X% increased HP; (4) +N HP regen per second; (5) +X% dodge chance (feet dominant); (6) +X% block chance (legs); (7) +X% damage reduction (Epic+); (8) +N HP on hit-taken; (9) +X% reduced damage from elites; (10) +X% reduced damage while stationary |
| Accessory | (1) +N max HP; (2) +X% increased HP; (3) +X% all elemental resists; (4) +X% chaos / unholy resist (amulet); (5) +N HP regen per second; (6) +X% reduced damage taken from afflicted enemies (belt) |

### 5.3 Resource category — sample modifiers per slot family

**Resource modifier surface gated by class resource model per § 2.2.**

| Slot family | Sample modifiers (per resource model — illustrative) |
|---|---|
| Weapon | (1) +X% mana on kill (Mana model); (2) +N stamina on kill (Stamina model); (3) +N rage per melee hit (Rage model); (4) +X% cooldown reduction on weapon-specific skill (Cooldown model) |
| Off-hand | (1) Tome: +N max mana / +X% mana regen; (2) Banner: +N party resource generation; (3) Focus: +X% cast speed (Mana/Cooldown model); (4) Horn: +X% party stamina regen (Stamina model) |
| Armor | (1) +N max resource (chest dominant); (2) +X% resource regen per second (chest / belt); (3) +X% resource cost reduction (per skill) (legs); (4) +N resource on hit-taken (chest); (5) +X% chance to refund resource on crit (gloves) |
| Accessory | (1) +N max resource; (2) +X% resource regen; (3) +X% cooldown reduction (Cooldown model); (4) +X% reduced channel cost (Channeled model); (5) +N combo retention (Combo model); (6) +X% HP-cost efficiency (HP-as-resource model) |

### 5.4 Crit category — sample modifiers per slot family

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% crit chance; (2) +X% crit multiplier (Epic+ exclusive); (3) +X% crit chance on element-cast; (4) +X% crit chance vs. low-HP enemies; (5) +X% crit multiplier vs. elites (Epic+); (6) +N flat damage on crit |
| Off-hand | (1) Focus: +X% spell crit chance / multiplier; (2) Dual-wield-secondary: +X% off-hand crit chance |
| Armor | (1) +X% crit chance on next attack after dodge (feet); (2) +X% crit chance while at full HP (legs); (3) +X% crit chance against bleeding enemies (gloves) |
| Accessory | (1) +X% crit chance (ring primary); (2) +X% crit multiplier (ring; Epic+); (3) +X% crit chance on element-cast (amulet); (4) +X% reduced crit damage taken (belt) |

### 5.5 Speed category — sample modifiers per slot family

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% attack speed; (2) +X% cast speed (caster weapons); (3) +X% projectile speed (ranged weapons); (4) +X% reload speed (firearm/crossbow weapons) |
| Off-hand | (1) Focus: +X% cast speed; (2) Dual-wield-secondary: +X% off-hand attack speed |
| Armor | (1) +X% movement speed (boots primary); (2) +X% attack speed (gloves primary); (3) +X% cast speed (gloves); (4) +X% cooldown reduction (legs / hands; Epic+); (5) +X% reduced action lag (gloves) |
| Accessory | (1) +X% movement speed (ring / belt); (2) +X% attack speed (ring); (3) +X% cast speed (amulet); (4) +X% cooldown reduction (amulet; Epic+); (5) +X% reduced movement-skill cooldown (belt) |

### 5.6 Resistance / Penetration category — sample modifiers per slot family

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% element penetration (per element; Epic+); (2) +X% armor penetration (Epic+); (3) +X% status duration on inflict (e.g., bleed/burn/chill duration) |
| Off-hand | (1) Shield: +X% all elemental resists; +X% chaos resist; (2) Focus: +X% element penetration (per gear-bound element; Epic+); (3) Tome: +X% spell penetration (Epic+) |
| Armor | (1) +X% all elemental resists (head / legs primary); (2) +X% per-element resist; (3) +X% chaos resist; (4) +X% status resistance (CC duration reduction); (5) +X% reduced damage from afflicted enemies; (6) +X% block effectiveness (legs) |
| Accessory | (1) +X% per-element resist (ring); (2) +X% all elemental resists (amulet primary); (3) +X% chaos resist; (4) +X% element penetration (ring; Epic+); (5) +X% status duration (CC inflict); (6) +X% reduced status duration on self (belt) |

### 5.7 On-trigger category — sample modifiers per slot family

**On-trigger surface is per D54: toolkit-only at legendary tier for high-tier triggers; lower-tier triggers (on-hit) can roll Rare+; on-crit / on-element-cast Epic+; on-block / on-dodge Legendary+.**

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% chance on hit to apply [status] (e.g., slow / bleed / burn); (2) +X% chance on crit to spawn [effect]; (3) on-kill: gain [resource]; (4) on-element-cast: [secondary effect] (Epic+); (5) on-crit: [chain effect] (Epic+); (6) Added-skill triggered-passive (legendary-exclusive per D55; HIGH PROBABILITY on weapons) |
| Off-hand | (1) Shield: on-block trigger (Legendary+); (2) Horn: on-rally trigger (party effect); (3) Banner: on-deploy trigger (zone effect) |
| Armor | (1) On-being-hit triggers (chest / legs primary per D55 armor on-being-hit pattern); (2) On-dodge trigger (feet; Legendary+); (3) On-block trigger (legs; Legendary+); (4) On-element-cast: gain [defensive buff] (head; Epic+); (5) Added-skill triggered-passive on armor (legendary; lower probability than weapons per D55) |
| Accessory | (1) On-kill: gain [buff stack] (ring); (2) On-crit: refund resource (ring); (3) On-element-cast: [amulet-themed effect]; (4) On-element-resist-trigger: gain [counter effect] (amulet); (5) On-low-HP: [survival mechanism] (belt) |

### 5.8 Build-identity category — sample modifiers per slot family

**Build-identity surface includes T4-attunement annotation (metadata; Tier-1+2 legendary + sets only) + set-bonus rank + class-intrinsic supporting-chain investment.**

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) T4-attunement annotation (Tier-1+2 legendary; metadata; per D33 + D51 amended); (2) Class-intrinsic supporting-chain investment bonus (Epic+); (3) Weapon-bound element gear-content fingerprint |
| Off-hand | (1) Banner: build-identity primary surface (banner-themed faction-display); (2) T4-attunement annotation (per category if T1+2); (3) Talisman: signature-mod patterns (Epic+); (4) Horn: party-buff theme (build-identity expression) |
| Armor | (1) Helm: class-themed signature modifier (Build-ID primary per § 2.1 matrix); (2) Set-bonus rank (set items only); (3) T4-attunement annotation (T1+2 legendary or all sets); (4) Chest: class-intrinsic supporting-chain investment surface |
| Accessory | (1) Amulet: skill-level affix (+N to class-themed skill; Build-ID primary per § 2.1); (2) Amulet T4-attunement annotation (T1+2); (3) Set-bonus rank (set items); (4) Belt: minor build-identity surface (utility-themed signature) |

**T4-attunement annotation specifics (per content-compositional model per D33 + D38 + D51 amended):** the annotation is METADATA recording generation-time alignment intent. It does NOT toggle any mechanic ON/OFF at consumption time. Gear's content (passives, weapon specs) IS the attunement. Magnitude IS the content quality. Spirit-guide projection surfaces synergy-score per closeout § 3.4 ("playing T4-A: projected KPM 75. Switching to T4-B: projected KPM 62. Net synergy score: T4-A composes 23% better with this gear").

### 5.9 Utility / Meta-progression category — sample modifiers per slot family

**Util/Meta is Epic+ exclusive per § 4.1.**

| Slot family | Sample modifiers (5-10 examples) |
|---|---|
| Weapon | (1) +X% magic find (Epic+); (2) +X% experience gain (Epic+; weapon implicit on certain weapon types) |
| Off-hand | (1) Talisman: +X% currency drop rate (Util/Meta primary); (2) Talisman: +X% rare-find chance; (3) Banner: +X% party currency drop rate |
| Armor | (1) Rare on chest: +X% experience gain (Epic+); (2) Rare on legs: +X% magic find (Epic+) |
| Accessory | (1) Belt: +X% currency drop rate (Util/Meta primary per § 2.1); (2) Belt: +X% experience gain; (3) Belt: +X% magic find; (4) Belt: +X% rare-find chance; (5) Ring: +X% magic find (Epic+); (6) Amulet: +X% experience gain (Epic+) |

---

## 6. Six locked principles (per closeout § 3.3)

1. **Graduated affinity, not binary** — every slot CAN roll any category but with weighted probability per affinity tier (primary ~50% / secondary ~30% / tertiary ~15% / off-affinity ~5%). Off-affinity rolls preserve gap-filling capability (per principle 4); they are NOT bugs.

2. **Tier-restricted modifiers** — ~10-20% of the BASELINE 32 numerical modifier surface is tier-restricted (Epic+/Legendary+/Tier-1+2). Capability toolkit is wholly LEGENDARY-EXCLUSIVE (per SC-4 finding 1 cross-ARPG consensus + D54). Tier-restriction is a SEPARATE constraint from slot affinity.

3. **Resource-model-gated** — Resource category modifiers map by class resource model (per 8-model catalog § 2.2). Cross-resource rolls DO NOT APPEAR (mana-using class never rolls stamina-regen modifiers; etc.).

4. **Gap-filling discipline (D80)** — spirit guide surfaces gap-fill opportunities; stat-sheet partition + acquisition curve calibration incorporate gap-filling discipline. Off-affinity (~5%) rolls are the structural mechanism that enables gap-filling; the spirit guide's projection surface is the player-facing mechanism that surfaces it.

5. **No-skill-modifier rule** — gear NEVER modifies existing chain-node skills (no +levels-to-Fireball; no +X% Fireball damage on gear). The capability toolkit ADDS new triggered-passives + rare true-actives only (per D54/D55). Skill-level affixes on helms + amulets (per Verdict B.3 + SC-4 Gate 4) are the SOLE exception, and only for class-intrinsic skill-rank boosts (not per-skill modifiers).

6. **Cross-cohesion validation** — Wave 1 partition cycle MUST validate affinity matrix supports build-diversity via spot-check simulation across cohort archetypes (per D61 + D84 + Discipline #26). Specifically: gamora runs spot-check sim on representative kits from each of the 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding) against the affinity matrix to confirm that build-diversity emerges naturally and no cohort is structurally locked out of any progression node.

**Cross-cutting discipline composition:**
- Principle 1 (graduated affinity) + Principle 4 (gap-filling) compose: off-affinity rolls ARE the gap-filling mechanism at structure layer; spirit guide surfaces gap-fill at experience layer
- Principle 2 (tier-restricted) + Principle 5 (no-skill-modifier) compose: capability toolkit is legendary-exclusive AND only-adds-new-content; never modifies-existing
- Principle 3 (resource-model-gated) + Principle 6 (cross-cohesion validation) compose: validation must confirm resource-gating doesn't break build-diversity (no resource model class is locked out of any progression node)

---

## 7. SC-4 5 methodology gates closure

Per Verdict B.4 RATIFIED standalone in commit `c983173` + closeout § 3.3. Cross-reference how doc 42 closes each of the 5 gates surfaced in legolas SC-4 research (`agentic_orchestration/research/cycle-13/2026-05-27-arpg-modifier-partitioning-landscape.md`).

| Gate | Closure | This doc's location |
|---|---|---|
| **Gate 1 — Prefix/suffix binary** | **ADOPTED** — prefix-offense / suffix-defense partition (per LE/PoE2/D4/GD consensus; SC-4 § S6 principle 1) | § 5.x sample enumerations follow prefix/suffix split implicitly: Damage/Crit/Speed/On-trigger/Util-Meta are offensive prefix surface; Defense/Resource/Res-Pen are defensive suffix surface; Build-identity is meta layer crossing both. Rocket implementation should carry the binary as a schema field per SC-4 Gate 1 (cannot be retrofitted easily). |
| **Gate 2 — Tag taxonomy** | **DEFERRED to v1.1+** — v1 adopts D4/LE flat-pool weighting (P2 simpler) per Verdict B.3 + SC-4 § S4 P2 archetype. PoE2-style tag-based weighting (P1) deferred to v1.1+ if pool size grows beyond manageable. | § 2.1 affinity matrix uses weighted-probability-per-affinity-tier (primary/secondary/tertiary/off-affinity) NOT spawn-weight-per-tag. Per-slot pool eligibility is derived from affinity matrix (which slot × category combinations roll which modifiers). Per Verdict B.4 + closeout: tag taxonomy not required for v1. |
| **Gate 3 — Item-type domain assignment** | **LOCKED per 11-slot taxonomy** | § 2.1 affinity matrix (9 categories × 11 slots) IS the item-type domain assignment. § 2.2 resource-model-gated assignment additionally constrains Resource category. § 5 sample enumerations operationalize per-slot-family. |
| **Gate 4 — Skill-level affix slot restriction** | **LOCKED — no +levels-to-skills on gear (per principle 5 no-skill-modifier rule)** | Capability toolkit ADDS new skills only (per D54/D55); does NOT modify existing chain-node skills. EXCEPTION: skill-level affixes on helms + amulets per Verdict B.3 + SC-4 Gate 4 + LE precedent — but ONLY for class-intrinsic skill-rank boosts (not per-skill modifiers). § 5.8 Build-identity samples include this surface. |
| **Gate 5 — Proc/trigger routing** | **LOCKED HYBRID — capability-toolkit-legendary-exclusive boundary** (per SC-4 Finding 1 cross-ARPG consensus per Verdict B.4) | Per § 5.7: triggered-effect NUMERICAL modifiers (e.g., "X% chance to slow on hit") roll in normal affix pool at Rare+/Epic+ (numerical-trigger surface). ADDED-SKILL TRIGGERED-PASSIVES are legendary-exclusive per D54/D55 (capability-toolkit-style). Rejects pure-GD pattern (all triggers in normal pool — too complex for v1) AND pure-LE-Idol pattern (separate item system — no v1 idol-equivalent). Adopts capability-toolkit-as-legendary-exclusive boundary per cross-ARPG consensus. |

**All 5 methodology gates CLOSED via Verdicts B.2 + B.3 + B.4 + this doc's operationalization.** Discipline #18 methodology consultation gate satisfied at structural layer; numerical calibration (magnitude bands per modifier tier; specific weights per affinity tier) fires per gamora SC-7 consultation post-Wave-1 per #18.2.

---

## 8. Minimum-viable trait integration (per Verdict D.1)

Per closeout § 2.1 Option C (supporting chain absorbs class identity) + Verdict D.1 Path (c) PARTIAL.

**Cycle 13 (THIS CYCLE) — Minimum-viable trait integration scope:**

| Component | Specification |
|---|---|
| **Trait pool size** | 55 entries (5 traits per archetype × 11 archetypes per `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch G archetype count) |
| **Per-archetype trait composition** | 1 element-tagged + 1 mechanic-tagged + 2 stat-flavored + 1 ability-flavored |
| **Trait surface location** | Class-intrinsic supporting chain (T3-only; per D83 supporting chain architecture; closeout § 2.1 Option C) |
| **Floor implementation** | L1 floor ONLY (per Cycle 13 minimum-viable; L12/L25/L38 floors DEFERRED to Cycle 14+) |
| **Gear-affix trait surface** | Element/mechanic-gated extensions to per-slot affix pools (extends § 2.1 affinity matrix to include trait-affix entries; gating against `secondary_elements` per `class_schema.py:46-47`) |
| **Rocket D8 work-unit specifications** | `config/traits/` YAML schema + loader + class_generator integration + L1 floor implementation; minimum-viable 55-entry pool authored by gandalf as design-spec input to D8 |
| **Sequencing** | gandalf trait-vocabulary design dispatch fires Wave 0/parallel; rocket D8 lands BEFORE Wave 1 partition cycle completion (avoids partition rework risk per GAP 5 audit); D9 element/mechanic-gating lands during Wave 4 (gear gen implementation) |

**Composition with supporting chain absorption:**
- Supporting chain (T3-only) carries the class-intrinsic trait surface
- Trait pool (55 entries) distributes across chains roughly evenly (~2 traits per chain per Verdict A.2 chain count 3-4)
- Per-class trait pool composition emerges from substrate-led Wave 2 generation per Verdict A.5
- Trait-affix surface is SEPARATE from 32-modifier-type stat-sheet surface per Verdict B.3 note — traits compose ADDITIVELY with the 9-category surface

**Cycle 14+ (DEFERRED — empirical-evidence triggers per closeout § 8):**
- Floor implementation at L12/L25/L38 (per `project_trait_architecture.md` full spec) — gates on first-cycle player-experience signal showing per-level-band trait commitment is meaningful
- Trait-pool expansion to 10 per class (current 5 is minimum-viable; full design intent is 5-10 band) — gates on cohesion-judge audit showing 5-per-archetype is too thin
- Phase 5 cohesion-judge integration for trait-thematic-coherence validation — gates on Phase 5 cohesion calibration landing (Cycle 14)
- Trait rank calibration (max rank 4, per-rank scaling) — gates on first-cycle telemetry showing rank scaling is meaningful
- G3 gear-affix trait export gap fix — NON-BLOCKING per rocket audit; deferred to Cycle 14+

---

## 9. Wave 1 implementation guidance for rocket

Concrete next-steps for rocket Wave 1 implementation against this design intent.

### 9.1 Main_weapon routing cleanup (SC-1 embedded)

Per doc 40 § 3.6 partition cycle scope item 7 + closeout § 10 sidecar SC-1.

**Problem:** 13 of 35 forms had off-hand-category items as main_weapon (substrate curation pollution per prior Cycle 12 capture). Three compound root causes:
1. Substrate curation pollution (off-hand items mis-categorized as main_weapon at substrate-acquisition)
2. Layer 2 substrate-binding not filtering by category
3. Secondary_item routing not firing

**Wave 1 cleanup work (cross-reference elrond seam per SC-1):**
- **elrond:** substrate curation pass on weapon_knowledge_entries; flag off-hand-category items currently routed as main_weapon; relabel per `canonical/story/off-hand-items-2026-05-24.md` 6-category taxonomy
- **rocket:** Layer 2 substrate-binding filter implementation — when generating a main_weapon-eligible kit cell, filter substrate query to exclude off-hand-category items; when generating secondary_item, route to off-hand-category items only
- **rocket:** secondary_item routing firing — ensure secondary_item generation actually fires per kit (not skipped) per `canonical/story/off-hand-items-2026-05-24.md` per-cell off-hand usage table
- **jack-ryan Gate-2:** verify post-cleanup main_weapon distribution shows zero off-hand-category items; verify secondary_item population matches per-cell off-hand usage table

### 9.2 Affinity matrix probability weight calibration approach

Per § 2.1 affinity matrix + principle 1 graduated affinity.

**Implementation pattern for rocket:**
1. **Schema:** add per-slot per-category affinity-tier field (primary / secondary / tertiary / off-affinity) per § 2.1 matrix
2. **Sampling (with per-slot normalization):** when rolling modifier for slot S, sample category C with probability per affinity tier:
   - For each category C in 9-category surface, compute raw weight: `raw_weight(S, C) = tier_value(S, C)` where `tier_value` returns 50 / 30 / 15 / 5 for primary / secondary / tertiary / off-affinity respectively (per § 2.1 matrix lookup)
   - **Compute per-slot raw sum:** `raw_sum(S) = sum(raw_weight(S, C) for C in 9 categories)`. Empirically this varies per slot (range ~190-255 across the matrix in § 2.1) because multiple categories share tier labels per slot
   - **Normalize:** `normalized_weight(S, C) = raw_weight(S, C) / raw_sum(S)`. Per-slot `sum(normalized_weight(S, C) for C in 9 categories) = 1.0` by construction
   - **Sample:** draw category C from the normalized distribution; the 50/30/15/5 tier values are therefore RELATIVE weights, not absolute per-category probabilities (a primary-tier category in a slot with many primaries gets a smaller absolute probability than a primary-tier category in a slot with only one primary — this is the intended graduated-affinity behavior)
3. **Per-modifier sampling within category:** once category C selected for slot S, sample specific modifier type from C's pool eligible for S per tier-restriction rules (per § 4)
4. **Magnitude sampling:** per modifier tier (per § 3 grid + per gear rarity), sample numeric magnitude within band (magnitude bands DEFERRED to gamora sim calibration per § 9.4 below)

### 9.3 Tier-restriction enforcement

Per § 4 + principle 2 tier-restricted modifiers.

**Implementation pattern for rocket:**
1. **Schema:** per modifier type, declare `tier_restriction` field (one of: `none` | `epic_plus` | `legendary_plus` | `tier_1_2_legendary_plus`)
2. **Gear gen filter:** when generating gear at rarity R, filter eligible modifier pool to those whose `tier_restriction` allows R:
   - `none` → all rarities
   - `epic_plus` → Epic + Legendary tiers
   - `legendary_plus` → Legendary tiers only
   - `tier_1_2_legendary_plus` → Tier-1 + Tier-2 legendary tiers + all sets
3. **Capability toolkit branching:** capability toolkit is a SEPARATE generation path (not in the baseline 32 modifier surface); per D54 it fires at all legendary tiers (tier 0/0.5/1/2); per § 4.3 dual-capability rolls + true-active rolls are tier-1+2 exclusive
4. **T4-attunement annotation:** at legendary tier 1+2 + all sets, add T4-attunement annotation field with chain-alignment intent + T4-target-intent (metadata only; not a runtime toggle per D33 + D51 amended)

### 9.4 Magnitude band calibration approach

Per § 3 per-rarity grid + Verdict B.4 magnitude bands.

**Magnitude bands are STARTING ESTIMATES.** Specific per-modifier magnitude bands per gear tier (per Verdict B.4 starting estimates: Common → no explicit; Uncommon → +5-10%; Rare → +10-20%; Epic → +20-30%; Legendary T0 → +25-35% + capability; Legendary T0.5 → +30-40%; Legendary T1 → +35-50% + capability + triggered-passive + T4-attunement; Legendary T2 → +40-60% + dual-capability + rare true-active + dual-T4-attunement).

**Gamora SC-7 methodology consultation** fires post-Wave-1 per Discipline #18 + #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before). Wave 1 ships with starting-estimate magnitude bands; Cycle 14+ iterates per gauntlet sim findings + balance band per multi-node calibration D27.

### 9.5 Cross-cohesion validation execution (principle 6)

**Wave 1 partition cycle close criterion includes principle 6 cross-cohesion validation:**
- gamora runs spot-check sim on representative kits from each of 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding) against rocket's affinity-matrix implementation
- Validation criterion: build-diversity emerges naturally (no cohort is structurally locked out of any progression node); resource-model-gating doesn't break build-diversity (no resource model is structurally disadvantaged); off-affinity rolls preserve gap-filling capability (occasional but present)
- Pass criterion per principle 6 + Discipline #26 playability-and-in-band

### 9.6 Implementation sequencing within Wave 1

Recommended sub-wave structure for Wave 1 partition cycle:

| Sub-wave | Work-unit | Owner | Gate |
|---|---|---|---|
| **W1.0 — Pre-execution gandalf trait dispatch** | 55-entry trait pool authoring at `canonical/story/v1-trait-vocabulary-minimum-viable-2026-05-XX.md` | gandalf | Trait pool delivered to rocket as design-spec input |
| **W1.1 — SC-1 main_weapon routing cleanup** | elrond substrate curation pass + rocket Layer 2 filter + secondary_item routing | elrond + rocket | jack-ryan Gate-2 PASS on routing distribution |
| **W1.2 — Schema extension** | Per-slot affinity-tier field + per-modifier tier-restriction field + T4-attunement annotation field | rocket (+ elrond if schema crosses substrate boundary) | jack-ryan Gate-1 critique on schema |
| **W1.3 — Affinity matrix implementation** | Per § 2.1 matrix; per-slot per-category sampling per § 9.2 pattern | rocket | jack-ryan Gate-2 PASS on sampling distribution |
| **W1.4 — Tier-restriction enforcement** | Per § 9.3 filter pattern; capability toolkit branching | rocket | jack-ryan Gate-2 PASS on tier-restriction discipline |
| **W1.5 — Magnitude bands (starting estimates)** | Per § 9.4 starting estimates per Verdict B.4 | rocket | jack-ryan Gate-2 PASS on magnitude band schema |
| **W1.6 — Trait integration (D8 ONLY)** | D8: per-class intrinsic trait pool integration into supporting chain (minimum-viable per Verdict D.1 Path (c) PARTIAL). **D9 (element/mechanic-gating on gear-affix trait surface) is Wave 4 scope per § 8 sequencing text — NOT included in W1.6.** | rocket | jack-ryan Gate-2 PASS on D8 trait integration |
| **W1.7 — Cross-cohesion validation (principle 6)** | gamora spot-check sim per § 9.5 | gamora + jack-ryan | jack-ryan Gate-2 PASS on validation criteria |
| **W1.8 — Wave 1 close** | Aggregate Wave 1 close criterion per § 10 | jack-ryan | Wave 1 close decision |

Sub-wave sequencing is illustrative; rocket + knight-rider may adjust per dependencies + Wave 1 dispatch authoring.

---

## 10. Wave 1 close criterion

Wave 1 closes when:

- [ ] SC-1 main_weapon routing cleanup complete (substrate curation + Layer 2 filter + secondary_item routing); jack-ryan Gate-2 PASS
- [ ] Schema extensions landed (per-slot affinity-tier + per-modifier tier-restriction + T4-attunement annotation); jack-ryan Gate-1 critique closed
- [ ] Affinity matrix implementation operational per § 2.1 + § 9.2; gear generation produces modifiers per affinity-tier weighted probability
- [ ] Tier-restriction enforcement operational per § 4 + § 9.3; Common/Uncommon/Rare/Epic NEVER roll legendary-exclusive modifier types
- [ ] Magnitude bands (starting estimates) operational per § 9.4 + Verdict B.4 per-tier bands
- [ ] Minimum-viable trait integration (55-entry pool + D8 supporting-chain integration + D9 element/mechanic-gating) operational per § 8
- [ ] Cross-cohesion validation per principle 6 + § 9.5; gamora spot-check sim PASS across 4 cohort archetypes; build-diversity emerges; no cohort structurally locked out
- [ ] jack-ryan Gate-2 PASS on aggregate Wave 1 close
- [ ] Wave 1 close unlocks Wave 2 (T4 algorithm Phases 1-2 implementation) — rocket fires Wave 2 against stat-sheet partition as substrate

**Wave 1 ready to feed Wave 2 T4 algorithm Phases 1-2 implementation when:** rocket's stat-sheet partition implementation produces gear instances whose modifier composition rocket's T4 algorithm can consume as input. Specifically, the gear instances must include the T4-attunement annotation metadata (Tier-1+2 legendary + sets) that the T4 algorithm consults for attunement-matching scoring + the capability toolkit slot content that the T4 algorithm composes with chain-specific effects per § 8.4 3-category taxonomy.

---

## 11. Composition with locked architecture

| Locked architectural element | How this doc composes |
|---|---|
| **Doc 38 D1-D10 delivery strategy** | Variant C engine-as-product: stat-sheet partition is per-product config (Reincarnated v1 ships with this 9-cat × 11-slot partition; future commercial profiles may config differently) |
| **Doc 39 Architecture B substrate-bound at Phase 2** | Phase 2d spec-driven gear gen consumes this partition intent; gear instances are substrate-bound (specific weapon/off-hand pulled per substrate filter) AND partition-bound (modifier surface per per-slot affinity matrix) |
| **Doc 40 § 3 spec-driven gear gen** | This doc operationalizes doc 40 § 3.6 architectural surface (9-cat × 11-slot + per-rarity grid + affinity matrix + 6 principles) |
| **Doc 40 § 6 T4-attuned gear (content-compositional)** | This doc operationalizes the T4-attunement annotation metadata at Tier-1+2 legendary + sets per D33 + D51 amended; per-rarity grid § 3 carries annotation field |
| **Doc 40 § 8 multi-T4 architecture (3-category taxonomy)** | Wave 1 partition cycle closes BEFORE Wave 2 T4 implementation per § 10; Wave 2 consumes the partition's gear-instances + T4-attunement annotations as input to T4 algorithm 3-category taxonomy (§ 8.4) |
| **Doc 41 L50 hybrid progression framework** | Per-rarity grid composes with tier mapping to player level bands per § 3 (T0 drops early L1-15; T0.5 mid L15-30; T1 endgame-start L30-45; T2 endgame L45-50+) per D50 + doc 41 § 2 |
| **8 BC axes (qd-engine-bc-axes-lock-2026-05-20.md)** | Cross-cohesion validation (principle 6) operates on BC-axis cells; cohort spot-check sim runs per-cell per cohort per § 9.5 |
| **8 resource models (closeout § 2.2)** | Resource category gated per class resource model per § 2.2 (principle 3); cross-resource rolls DO NOT APPEAR |
| **Block C calibration scaffolding** | Affinity matrix probability weight calibration (§ 9.2) + magnitude band calibration (§ 9.4) feed Block C Step 2 (sim) + Step 3 (measure) inputs |
| **6 disciplines #1.1 + #18 + #18.2 + #23 + #26 + #29** | This doc applies framing-audit at structural layer (Q1: load-bearing assumption is "9-cat × 11-slot is the correct architectural surface" — verified per Verdict B.3; Q2: refutation evidence = any of the 4 reference ARPGs runs a meaningfully different partition; verified per SC-4 cross-ARPG consensus; Q3: refine if needed — this doc operationalizes per consensus). Discipline #29 commitment-to-consequence: the affinity matrix + 6 principles ARE the v1 commitment; iteration is per-cycle, not per-session reversibility. |

---

## 12. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Wave 1 partition design intent canonical for Cycle 13 stat-sheet partition cycle
**Composition:** with doc 38 + doc 39 + doc 40 (post-2026-05-27 amendments) + doc 41 + closeout doc 2026-05-27 + Verdicts B.2/B.3/B.4 + legolas SC-4 research + 8-axis BC lock + 8-model resource catalog + Block C calibration scaffolding
**Authority:** Matt 2026-05-27 verbatim — autonomous Wave 0 → Wave 1 sequencing per ratified framing brief § 4.1
**Next gates:**
- jack-ryan Gate-1 critique on this doc (post-authoring; separate dispatch fires)
- Rocket Wave 1 implementation per § 9 guidance + sub-wave structure (post-Gate-1 close; separate dispatch fires)
- Gamora SC-7 methodology consultation post-Wave-1 per Discipline #18.2 (separate dispatch)

**For:** the Wave 1 partition design intent canonical for Cycle 13 stat-sheet modifier partition cycle. 9-category × 11-slot affinity matrix operationalized; per-rarity × per-slot grid LOCKED; tier-restricted modifier surface enumerated; sample modifier enumerations per category per slot family informing Wave 1 rocket implementation (not exhaustive; rocket extends); 6 principles LOCKED; SC-4 5 methodology gates CLOSED; minimum-viable trait integration (55-entry pool absorbed via supporting chain per Option C) operationalized; Wave 1 implementation guidance for rocket provided. Wave 1 close criterion = jack-ryan Gate-2 PASS on rocket implementation against this intent. Wave 1 ready to feed Wave 2 T4 algorithm Phases 1-2 implementation upon close. Authoritative source for CURRENT-status truth remains `canonical/00-ground-state.md`.

**Signed:** gandalf (story-and-design steward)
