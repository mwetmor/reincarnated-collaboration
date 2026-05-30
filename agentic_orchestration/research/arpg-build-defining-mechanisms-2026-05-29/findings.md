# ARPG Build-Defining Mechanisms — Research Findings

> **STATUS:** CURRENT — Authored by legolas Mode A 2026-05-29 evening late per gandalf research commission. Inline-return content captured to disk by gandalf for durability. Composes with `mechanisms.csv` structured extract (31 mechanisms × 9 games) + commissioning brief in gandalf in-thread conversation.

**Date:** 2026-05-29 evening late
**Author:** legolas (research scout; Mode A analytical research)
**Commissioner:** gandalf (story-and-design steward); ultimate consumer Matt
**Companion artifacts:**
- `mechanisms.csv` — 31-row structured extract (pipe-delimited; one row per mechanism)
- gandalf in-thread research brief (commissioning specification)

---

## § 0 TL;DR

The ARPG genre does NOT converge on "passive tree capstone node" as the canonical build-defining mechanism. The genre distributes build-defining power across **7 distinct mechanism families**. The T4 capstone abstraction is a real design choice, but it is closest in lineage to a **minority family** (PoE Keystones + PoE Ascendancy capstones), not the dominant pattern.

The dominant genre-canonical build-defining mechanism is **extractable/imbue-able power** (D2 Runewords, D3 Kanai's Cube, D4 Legendary Aspects, D4 Tempering): powers discovered, extracted, and assembled into slots, decoupled from the character's tree. The second-strongest family is **intra-skill transformation trees** (LE Skill Trees, PoE Support Gem links, Lost Ark Tripods): mechanisms that live inside a skill's own transformation space, not at the periphery of a passive tree.

Three mechanism families exist in the genre for which Reincarnated has no current equivalent: (1) extractable/imbue-able power slot, (2) proc-attached celestial powers (Grim Dawn Devotions), (3) class-combo combinatorial identity. Reincarnated's T4 MECHANICAL STRATEGY slot is architecturally novel in combining keystone-swap + ascendancy-choice + support-gem philosophy into one unified layer.

---

## § 1 Per-game mechanism enumeration

Full enumeration in `mechanisms.csv` (31 mechanisms × 9 games). Summary count:

| Game | Mechanisms enumerated | Primary crystallization moment |
|---|---|---|
| Path of Exile 1 | 9 | 6-link acquisition; Ascendancy completion |
| Path of Exile 2 EA | 2 (new) + ~3 inherited | Spirit reservation lock-in; Ascendancy |
| Diablo 2 / D2R | 3 | Runeword acquisition (Enigma/Infinity totemic) |
| Diablo 3 | 3 | Class Set 6-piece completion |
| Diablo 4 | 5 | Legendary Aspect assembly |
| Last Epoch | 4 | Skill specialization tree completion |
| Grim Dawn | 2 | Dual Mastery selection (permanent) |
| Lost Ark | 4 | Class engraving + general engraving stack |
| Wolcen | 1 | Gate of Fates path alignment |

**Per-character simultaneous build-defining mechanism count: 3–5 (genre tendency).** D2 and GD are the strongest 1–2-mega-moment outliers; PoE is the 5–8 outlier; all others cluster at 3–5.

---

## § 2 Seven mechanism families (cross-game pattern)

### Family A — Intra-skill transformation
Mechanism lives *inside* the skill; modifies how the skill operates.
**Members:** LE Skill Specialization Tree (20 pts/skill); PoE Support Gem Links (5 supports stack); LA Tripod (3 tiers per skill); PoE2 Meta Gem (Cast on X).
**Shared properties:** internal to skill namespace; transformation possible (not just amplification); early-mid accessible; highly respec-able.

### Family B — Extractable / imbue-able power **(DOMINANT BY GAME COVERAGE)**
Power is discovered, extracted/stored, then imbued onto a different slot. Power is portable.
**Members:** D2 Rune Words; D3 Kanai's Cube; D4 Legendary Aspect (Codex); D4 Tempering.
**Shared properties:** power is portable/transferable; item-slot-coupled; acquired via drops or crafting; build identity = which power set is assembled.
**Coverage: D2 + D3 + D4 — three of the most commercially successful ARPGs all center their build-defining moments here.**

### Family C — Class-identity combo
Two or more class/archetype selections combine to create emergent build identity.
**Members:** GD Dual Mastery; D3 Class Set 6-piece; LA Class Engraving; PoE Ascendancy Class.
**Shared properties:** defines archetype rather than amplifying pre-existing one; often permanent or near-permanent; early-to-mid decision with endgame consequences.

### Family D — Passive-tree capstone node
Terminal node on a passive/devotion tree; binary unlock with large effect and trade-off or cost.
**Members:** PoE Keystone Passive; PoE Ascendancy Capstone Node; GD Devotion Celestial Power (terminal); D4 Paragon Legendary Glyph (level 51).
**Shared properties:** requires investment path to reach; binary unlock at terminal; large effect.
**This is the closest analog family to Reincarnated's T4 capstone model. Represented in 3 of 9 games as a primary mechanism.**

### Family E — Item-slot anchor (unique/mythic)
A specific unique item, when equipped, transforms the entire build around its properties.
**Members:** Mageblood; Headhunter; Enigma; Infinity; Tyrael's Might; The Grandfather.
**Shared properties:** single slot; build wraps around the item's presence; extreme rarity; Mageblood-tier acquisition.

### Family F — Consumable / inventory-resident passive
Items held in inventory (not gear slots) that provide passive bonuses; trade-off is space.
**Members:** D2 Charms; LE Idols; LE Blessing.
**Shared properties:** spatial trade-off; additive bonuses; mostly quantitative with occasional build-enabling exceptions.

### Family G — Proc-attached celestial / secondary effect
An effect attached to a specific skill as a secondary chance-to-proc trigger.
**Members:** GD Devotion Celestial Power (linked); PoE Watcher's Eye conditional mod; D3 Legendary Gem secondary (Rank 25 unlock).
**Shared properties:** conditional trigger; secondary to primary attack; adds layered behavior.

---

## § 3 Mathematical-property summary

| Family | Typical Magnitude Pattern | Stackability | Trigger | Scales With Investment |
|---|---|---|---|---|
| A (intra-skill) | Transformative (type change) OR +20–50% multiplicative per support | Additive within family; "more" multiplicative | Always-on or trigger-linked | Gem level / node point count |
| B (extractable/imbue) | Fixed power set; aspect scales with item stat | Single per slot; no double-up | Always-on (imprinted) | Flat or scales with item power |
| C (class-combo) | Large flat bonus or mechanic unlock | Single-instance | Always-on when complete | Scales with class mechanic count |
| D (capstone-node) | Binary two-sided mechanic swap; +25–50% large bonus typical | Single-instance | Always-on (allocated) | Flat OR scales with adjacent investment |
| E (item-slot anchor) | Large unique effect not otherwise achievable | Single per slot | Always-on or on-kill | Does not scale — power is fixed per item tier |
| F (consumable / inventory) | +1 skill / +% resist / flat stats | Additive unlimited up to inventory space | Always-on (held) | Scales with count |
| G (proc-attached) | Chance-to-proc new skill on attack | Single attachment per skill (GD) | Proc-on-event | Scales with attached skill's attack frequency |

---

## § 4 Investment-tier coupling analysis

**Day-1 accessible:** PoE Support Gem linking; LE Skill Specialization Tree; GD Dual Mastery; LA Class Engraving direction; D4 Aspects via Codex.

**Mid-game crystallization:** PoE Keystone; PoE Ascendancy; D3 Class Set; D4 Paragon; GD Devotion path.

**Endgame-only / Mageblood-tier:** PoE Mageblood / Headhunter; PoE Awakened Gems; D2 Enigma / Infinity; D4 Mythic Uniques; D3 Legendary Gems max-rank.

**Single-shot transformations** (one acquisition = instant build transformation): D2 Enigma / Infinity; PoE Mageblood; D3 Class Set 6pc; GD Dual Mastery; PoE Keystone.

**Progressive crystallizations** (multiple investments build toward crystallization): PoE Support Gem leveling; LE Skill Tree node clusters; D4 Glyph leveling; GD Devotion path; D4 Masterworking milestones.

---

## § 5 Architectural verdict on T4 abstraction

**VERDICT: T4 capstone node is genre-canonical but minority-family. Real but partial.**

Family D (passive-tree capstone) is present in PoE Keystones, PoE Ascendancy capstones, D4 Paragon Legendary Glyphs, GD Devotion terminal nodes. Legitimate genre pattern. **But only 3 of 9 games center build identity on it primarily.**

The dominant family by game coverage is Family B (extractable/imbue-able power) — D2, D3, D4 all center build identity there. **The community-canonical "build came online" moment in those games is an ITEM acquisition or POWER assembly event, not a tree allocation event.**

### Cheapest empirical refutation tested

If T4 were the canonical dominant pattern, we would expect all major games to center build identity on tree-terminal nodes:
- D2: No passive tree capstone of note → build identity = Runewords + skill tree
- D3: Primary crystallization = Class Set 6pc (Family C) — not a tree node
- D4: Primary crystallization = Legendary Aspect assembly (Family B) — not a tree node
- LE: Primary = skill specialization tree completion (Family A — intra-skill)
- GD: Primary = Dual Mastery selection (Family C — class-combo)
- Only PoE makes capstone nodes a central element. **NOT refuted in 5 of 6 non-PoE cases. Confidence: high.**

### Three architectural patterns suggesting alternatives

**Pattern 1 — Item-slot-based build-defining (Families B + E):** Build crystallization most commonly fires at the moment a specific item is equipped or a specific power is imprinted. D2 = "Enigma moment"; D4 = "assembling the right Aspect combination."

**Pattern 2 — Intra-skill transformation (Family A):** Build identity can crystallize INSIDE the skill's own transformation space. LE: "when I hit the 15th skill point on this node path." Architecturally distinct from T4 — investment and effect live in the same namespace (the skill).

**Pattern 3 — Class-combo combinatorial (Family C):** Build identity emerges from the COMBINATION of two systems. GD = 66 combinations from 9 masteries.

---

## § 6 Closest-genre-analog mapping for Reincarnated T4 strategies

| Reincarnated T4 Strategy | Closest Genre Analog | Family |
|---|---|---|
| Primary T4: DIRECT_DAMAGE_AMPLIFICATION universal slot | D3 Legendary Gem (Bane of the Trapped) | gem_slot (Family D) |
| Proc-on-condition strategy | GD Devotion Celestial Power | proc_attachment (Family G) |
| Resource-loop alteration strategy | PoE Keystone (Eldritch Battery, Eternal Youth) | passive_tree_node (Family D) |
| Scope expansion strategy | PoE Support Gems (Chain / Fork / Pierce / Spell Echo) | skill_link (Family A) |
| Damage-type conversion strategy | LE Skill Tree type-conversion + PoE Conversion Keystones | intra_skill_tree + passive_tree_node |
| Temporal / burst-window strategy | LA Class Engraving (Igniter) | class_engraving (Family C) |
| Defensive architecture shift | PoE Keystones (CI; Acrobatics; Ghost Reaver) | passive_tree_node (Family D) |
| Minion/companion behavior strategy | D3 Marauder Set 6pc + Kanai's Cube minion powers + LE skill tree minion transformation | Multiple families |
| Aura/persistent effects strategy | PoE Watcher's Eye + PoE2 Spirit Gems | item_affix + resource_allocation |

---

## § 7 Gap analysis (Reincarnated absences)

### Gap 1 — Extractable/imbue-able power slot (Family B) — MOST SIGNIFICANT
No equivalent to D3 Kanai's Cube (extract a power from any item; keep 3 simultaneously) or D4 Legendary Aspects (power extracted to Codex; portable; re-imprinted onto any compatible slot). The genre's most-beloved build crystallization mechanism family — the one that produced Enigma, Infinity, Aspect assembly — is absent from Reincarnated's current architecture.

### Gap 2 — Proc-attached secondary trigger (Family G, GD-style)
No equivalent to GD Devotion Celestial Powers: attach a proc skill to any primary skill, with proc firing on hit/crit/event. "Layered behavior stacking."

### Gap 3 — Class-combo combinatorial identity (Family C)
No equivalent to GD dual mastery: combining two class trees where synergy between them IS the build identity, and the design space is combinatorial (N × N – N combinations from N classes). Spirit-swap is closest analog but is temporal/sequential rather than simultaneous-synergy.

### Gap 4 — Item-slot-anchor uniques (Family E)
Reincarnated appears to lack a Mageblood/Enigma-class item: a single unique item whose acquisition transforms how a fundamental system works for all builds.

### Gap 5 — Inventory-resident spatial trade-off (Family F)
No equivalent to D2 Charms or LE Idols.

---

## § 8 Where Reincarnated is genuinely novel

**Novel 1 — T4 MECHANICAL STRATEGY cycling slot.** The 6 Layer 2 strategies represent something more nuanced than PoE Keystones (binary trait swaps without a governing taxonomy). A "mechanical strategy" that cycles through 6+ distinct options per character build is closer to PoE Keystone + Ascendancy + support gem philosophy unified into one architectural slot. No single game does this in one unified abstraction layer.

**Novel 2 — Seasonal spirit identity as compositional build substrate.** If the seasonal spirit's element, role, and mechanic are baked into the substrate from which T4 emerges, the build-defining mechanism is the COMPOSITION of (seasonal spirit × T4 strategy × skill geometry). Closest genre analog is GD dual mastery emergent synergy, but Reincarnated's seasonal-rotation mechanism adds a temporal dimension GD lacks.

---

## § 9 Three actionable signals for gandalf / Matt

1. **Family B gap is the most significant.** No extractable/portable power mechanism exists in Reincarnated. Whether a spirit-kit's gear slot or a future "extract and reimprint" mechanic could fill this gap is a design question.

2. **Intra-skill transformation (Family A) is underweighted.** LE's "skill tree comes online" moment happens inside the skill's own transformation space. Reincarnated's skill geometry + T4 partially approximates this, but per-skill depth of LE's 20-node trees is not currently replicated. Whether some of the 15 proposed Layer 2 T4 strategies should be partially reimagined as intra-skill properties (attached to specific skills rather than character-wide) is worth evaluating.

3. **T4 is architecturally novel in one respect the genre does not have.** The MECHANICAL STRATEGY cycling model — a single slot that can be one of 6 (or 21) distinct strategic archetypes — is not found in any single mechanism in the genre. Worth preserving.

---

## § 10 Sources cited

(35+ sources spanning game wikis, build-guide sites, official manifestos, community analysis. Per-mechanism source URLs in `mechanisms.csv` source_url column. Headline sources include: PoE Wiki, D4 Wiki, LE Wiki, GD Wiki, Wolcen Wiki, Maxroll D4/PoE/LE/D3, Icy-Veins D4/LE, PoE-Vault, lastepochtools.com, Mobalytics, Battle.net Arreat Summit archive, GGG forum, Lost Ark community sources.)

---

**Sign-off:** legolas (research scout) per gandalf Mode A commission 2026-05-29 evening late. Findings inline-returned to gandalf at completion; gandalf captured to this file for durability. CSV artifact at `mechanisms.csv` provides structured machine-readable extract.

**For gandalf:** integrate findings into research.db schema extension + update HTML synthesis doc § 11 + § 12 + § 15 + new "Architecture-beyond-T4" section + assess T4 implications + report to Matt.
