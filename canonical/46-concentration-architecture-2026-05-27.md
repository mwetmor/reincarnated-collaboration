# 46 — Concentration Architecture: Stat Bounds + Capability Density + Set Keying + Cohesion Layering

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — foundational architectural commitment for Cycle 14 sidecar; remediation of capability-soup pattern surfaced by Cycle 13 empirical inspection; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Cycle 14 sidecar foundation; 9 architectural layers locked across one Pattern-B design conversation (continuing the same-day 2026-05-27 session); composes with docs 38 / 39 / 40 / 41 / 42-45 architectural foundation
**Authority:** Matt + gandalf Pattern-B session 2026-05-27 (extending the morning Cycle 13 pre-launch design session); Matt 2026-05-27 verbatim "yes, draft it. all 9 layers locked" after iterative architectural design conversation against empirical Cycle 13 mechanical season output
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation; this doc amends D9 / D33 / D38 / D51 / D54 / D55 / D56 + adds new discipline candidates
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid progression framework + ~30-day seasonal duration
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — 9-category × 11-slot affinity matrix + per-rarity grid
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — T4 algorithm Phases 1-2 (3-category taxonomy + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan)
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — T4 Phase 3 scope-dimension
- `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` — Wave 4 Track A spec-driven gear gen
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — morning session closeout
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` — empirical reference table that surfaced the capability-soup pattern this doc remediates

---

## 0. TL;DR

Cycle 13 empirical inspection of the 16-character mechanical season surfaced a **capability-soup architecture** — 22 mechanic-alterations per endgame character (11 capability_modifiers + 11 triggered_passives, many redundant; sets per-character bespoke not cross-class shareable; many "passive" legendaries are stat modifiers disguised as skills; T4 strategies catastrophically uniform with 100% Category C ELEMENT_CONVERSION). This violates the **concentration discipline** that every successful ARPG generation converges on: 2-6 mechanic-altering items per character with stat affixes on the rest.

This doc locks **9 architectural layers** that compose into the concentration discipline:

1. **Stat-range bounds** (prerequisite — defines bounded vs unbounded stat dimensions)
2. **Affix migration** (`general_passive_*` entries move OUT of legendary, INTO Magic/Rare/Epic stat affixes)
3. **Capability scope reduction** (legendary capabilities are LOCAL — slot-bound / trigger-bound / skill-specific / item-family / state-conditioned; drop character_wide + chain_wide as legendary scopes — those are T4 territory)
4. **Trigger-condition vocabulary expansion** (~50+ trigger conditions across action / defense / resource / state / enemy-state / environmental / skill-conditioned / combo / positional / element / timer families)
5. **Concentration probability table by tier** (Common-Rare: 0% capability; Epic: 0% cap / ~25% triggered_passive; Legendary T0-T0.5: ~30-50% capability OR triggered_passive XOR; T1: ~75% both; T2: 100% both with T4-attunement; Sets replace individual capability)
6. **Cohesion-judge layered architecture** (CORE identity from chain composition weighted toward lower tiers; endgame T4 + legendary/set themes as ADDITIVE nod; identity must work at L1 with no gear)
7. **Compositional synergy scan amendment** (Pass 1 thematic seeds ENCOURAGED including cross-element / cross-mechanic combinations; Pass 2 redundancy FILTERED via same-pattern_id dedup + same-trigger-window cap)
8. **Set keying to T4 strategy × element clusters** (sets keyed to (Cat A × Cat B/C × primary element + secondary element); ~12-20 named sets per season; cross-character shareability; retire per-character bespoke pattern)
9. **Class-agnostic spec-driven per-drop generation** (drops use spec keyed to substrate; class/build relevance emerges from spec match, not smart-loot filtering; composes with D21 Option A calibrated rate)

**The architectural through-line: concentration over distribution. Identity = chain composition + T4 + 4-6 build-defining items + stat-affix support. Gear amplifies; gear does not constitute.**

---

## 1. Architectural through-line — concentration over distribution

### 1.1 Core principle

> **Identity emerges from chain composition + T4 selection + 4-6 build-defining items. Other equipment is stat-affix support. Mechanic-alteration is CONCENTRATED to specific items + the T4 layer, NOT distributed across all 11 equipped slots.**

### 1.2 Empirical motivation

Cycle 13's mechanical season produced 16 characters with **~22 mechanic-alterations per endgame loadout** (11 capability_modifiers + 11 triggered_passive entries, many of the latter being stat boosts disguised as skills). The empirical reference table at `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` showed:

- **str_01 heavy_barbarian**: 4 damage-reflection effects firing on overlapping trigger windows (reflect / reflect / thorns / counter) — pure mechanical redundancy
- **wis_04 storm_caller**: 2 counter_on_block + 2 move_speed passives — duplicate template stacking
- **dex_04 twin_blade_fencer**: 2 speed_boost_on_dodge + 2 defense_aura — same pattern
- **Sets per-character bespoke** (set_id derived from character_id) — not cross-class shareable

This matches the **Diablo 4 aspect-soup pattern** that D4 spent multiple patches trying to mitigate. Cycle 13 reproduced the failure mode by construction.

### 1.3 Genre canon — concentration is the universal pattern

Across every successful ARPG generation:

| Game | Mechanic-alteration concentration | Stat-affix distribution |
|---|---|---|
| **Diablo 1** | Uniques carry ONE distinctive effect | Prefix/suffix on rare items |
| **Diablo 2 (LoD)** | 2-4 build-defining uniques/runewords/sets | 6-7 rare/magic slots |
| **Diablo 3 (post-patch)** | 6-piece set bonus = build identity; sets REPLACE individual legendary powers | 2-3 player-chosen legendary slots + stat-affix support |
| **Diablo 4 (post-patch)** | Aspects became SKILL-SPECIFIC; some retired | Reduced scope through patches |
| **Path of Exile** | 2-4 unique items player-chosen + 2-3 cluster jewels + skill gems | Most slots = rare with stat affixes |
| **Last Epoch** | 4-5 idols with specific small alterations + 1-3 unique items | Most gear = stat affixes |
| **Grim Dawn** | 1-2 effects per Mythical legendary + set bonuses | Affix-based rares |
| **Lost Ark** | 6 engraving slots (hard cap) | Gear = stat affixes |

**The convergent pattern across the genre: 2-6 mechanic-altering items per character. Everything else = stat support.** This doc adopts that convergence as Reincarnated v1 canonical architecture.

### 1.4 Isekai genre alignment

In the isekai genre Reincarnated lives in, identity emerges from intrinsic class abilities + skill progression, NOT from gear stacking:

- **Mushoku Tensei**: Rudeus's identity = spell-school mastery + technique combination; equipment mostly mundane
- **KonoSuba**: each character has 1-3 defining abilities; equipment is cosmetic/situational
- **Slime**: Rimuru's powers come from absorbed skills; equipment rare relic style (1-2 effects)
- **Solo Leveling**: Jin-Woo's identity = shadow-monarch class progression; gear is supportive
- **Fate Grand Order**: servants have 3 Noble Phantasms + skills + passives; gear is conceptual extension

The "every slot has multiple effects" pattern is genre-incongruent. The concentration architecture is genre-aligned.

---

## 2. Layer 1 — Stat-range bounds (the prerequisite)

### 2.1 Why this is the foundational layer

Without bounded stat ranges, the algorithm produces magnitudes against an unbounded distribution. Stacking effects compound into overflow. Every subsequent layer (capability density, cohesion, set design) operates on numerical magnitudes — those magnitudes must be bounded for the architecture to balance.

This layer is the **prerequisite for everything else**. Cycle 13 produced its capability-soup because this layer wasn't authored before Cycle 13's algorithm fired.

### 2.2 Bounded stats (require explicit max cap)

| Stat | Lower bound | Upper bound | Reasoning |
|---|---|---|---|
| **Crit chance** | 0% | 95% | 5% miss buffer (PoE/D2 convention); D4 went 100% post-patch and broke balance |
| **Crit multiplier (damage)** | 100% | 500% | Crits cannot be the only damage source; cap prevents one-shot RNG |
| **Movement speed bonus** | 0% | 100% | Baseline 100% movement + bonus; PoE caps ~50-100%; D4 similar |
| **Cooldown reduction** | 0% | 75% | D2/D3 capped 60-75%; uncapped breaks rotation pacing |
| **Resource cost reduction** | 0% | 80% | Composes with cooldown reduction caps |
| **Attack speed bonus** | 0% | 200% | Baseline 100% + up to 2× bonus |
| **Cast speed bonus** | 0% | 200% | Same shape as attack speed |
| **Damage reduction (DR%)** | 0% | 90% | D2 capped 50%; D3 mitigated via armor formula |
| **Element resistance** | -100% | 80% | D2 max-resist cap convention; negative ranges allow vulnerability |
| **Status resistance / duration** | -50% | 200% | Negative = vulnerable; positive = resistant |
| **Penetration (armor / element)** | 0% | 75% | Composes inversely with target's resistance cap |
| **Life steal** | 0% | 30% | D2 capped; uncapped breaks tanky archetypes |
| **Block chance** | 0% | 75% | Shield + skill investment; D2 max-block convention |
| **Dodge chance** | 0% | 75% | Composes with armor / DR |
| **Magic find / drop quantity** | 0% | 500% | Diablo lineage; cap prevents drop-rate breaks |

### 2.3 Unbounded stats (scale with progression node)

| Stat | Scaling source |
|---|---|
| **Raw HP** | Player level + gear-tier baseline + chain investment |
| **Raw mana / energy / stamina / rage / etc.** | Same — per resource model from doc 41 |
| **Raw damage (flat)** | Same |
| **Raw armor** | Same — converted to DR% via formula with cap from § 2.2 |
| **Raw regeneration** | Same |

### 2.4 Compositional integrity rules

- Multiple stat affixes contributing to the same bounded stat (e.g., 3 sources of +5% crit) compose ADDITIVELY but cap at the bound (§ 2.2)
- Stats above cap (overflow) are wasted — not preserved as "stored" capacity
- Unbounded stats compose additively without cap; balance comes from the spec at generation time per balance-as-property (D1)
- Negative bounds (resistances, status resistance) allow vulnerability design space

### 2.5 Implementation discipline

- Stat-range bounds enforced at generation time (rocket Wave 4 Track A amendment in `gear_instance_generator.py`)
- Stat-range bounds enforced at runtime (drax loadout app + future combat layer): stats above cap render as "at cap" with overflow indicator
- Cohesion-judge LLM at Phase 5 references the cap when narrating ("this build is at the crit cap of 95%")

---

## 3. Layer 2 — Affix migration

### 3.1 Core insight (Matt 2026-05-27)

Many "passive" legendaries in the Cycle 13 data are **stat modifiers disguised as triggered_passive skills**. They belong on Magic/Rare/Epic gear as partition affixes, not as legendary capability content.

### 3.2 Migration table

| Currently as legendary triggered_passive | Migrate to | Rolls on rarity tier |
|---|---|---|
| `general_passive_crit_boost` (+5% crit chance) | Crit-category partition affix | Magic+ |
| `general_passive_resource_regen` (+8% resource regen) | Resource-category partition affix | Magic+ |
| `general_passive_defense_aura` (+5% DR) | Defense-category partition affix | Rare+ |
| `general_passive_move_speed` (+6% movement) | Speed-category partition affix | Magic+ |
| `general_passive_cooldown_reduce` (-5% cooldown) | Speed-category partition affix | Rare+ |
| `general_passive_element_affinity` (+8% gear-element damage) | Damage-category partition affix | Rare+ |
| `general_passive_on_kill_regen` (+3% resource on kill) | On-trigger-category partition affix | Epic+ (trigger-conditioned) |

### 3.3 Discrimination criterion

The boundary between **stat affix** and **legendary mechanic-altering content**:

| Pattern type | Examples | Rarity destination |
|---|---|---|
| **Pure stat boost** (numerical modifier; always-on) | crit_boost, resource_regen, defense_aura, move_speed, cooldown_reduce, element_affinity | Magic+ / Rare+ partition affix |
| **Trigger-conditioned stat boost** (numerical modifier; fires only on event) | on_kill_regen, speed_boost_on_dodge, element_resist_on_hit | Epic+ partition affix (trigger-conditioned tier-restricted) |
| **Mechanic-altering effect** (changes HOW something works; not just magnitude) | thorny_on_hit, chain_lightning_on_hit, freeze_on_crit, on_kill_explosion, reflect_on_being_hit, shield_on_low_hp, counter_on_block, curse_on_hit, geometric_aoe_on_hit, cleanse_on_cc, stun_on_being_hit | Legendary capability content |

### 3.4 Implementation discipline

Algorithm amendment in `gear_instance_generator.py` (rocket Wave 4 Track A scope):
- Pure stat boosts NEVER roll on legendary triggered_passive field; they're rolled as partition affixes per slot affinity matrix per doc 42
- Trigger-conditioned stat boosts roll on Epic+ partition affixes with the trigger condition as a sub-property
- ONLY genuine mechanic-altering effects fire as legendary triggered_passive content

### 3.5 Quantitative impact

For str_01 heavy_barbarian's current loadout: removing the 4 `general_passive_*` entries reduces the mechanical-alteration surface from 22 to ~14-16. Compounded with § 4 capability scope reduction + § 6 concentration table, expected per-character endgame mechanical surface drops to ~6-8 — within genre canon range.

---

## 4. Layer 3 — Capability scope reduction

### 4.1 Core amendment

Doc 40 § 3.3 capability toolkit categories included "multiplicative (numerical multiplier on matching T4 path)" + "mechanic-adjusting" + "spatial-adjusting" + "axis-adjusting" + added-skill variants. The IMPLEMENTATION extended capability scope to **character_wide** and **chain_wide** — making each legendary capability a near-T4-scale alteration.

**Amendment**: legendary capabilities are LOCAL alterations. Drop character_wide + chain_wide as legendary capability scope. Reserve those for T4 ONLY.

### 4.2 New scope categories for legendary capabilities

| Scope | What it alters | Example |
|---|---|---|
| **Slot-bound** | Only the slot's primary function | Weapon's attack geometry/range; shield's block mechanic; armor's defense reaction |
| **Trigger-bound** | Fires only in specific event-window | On-block (with this shield); on-being-hit (in this armor slot); on-cast (with this weapon) |
| **Skill-specific** | Alters ONE specific skill within a chain | "Your [Fireball/Charge/Whirlwind] also [chills/stuns/pulls]" — keyed to specific skill_id |
| **Item-family** | Within-family interaction | Shield-bash with this shield; arrow-bind with this bow; ritual-cast with this focus |
| **Conditional-state** | Active only in specific player state | While at <25% HP; while channeling; while moving; while stationary; while combo-built-up |

### 4.3 What's reserved for T4 (NOT legendary capability scope)

- **Character-wide alterations** — class-mechanical changes affecting all skills, all chains, all combat
- **Chain-wide alterations** — chain-level multiplier or element conversion or addition
- **Parallel-chain reach** — cross-chain alterations
- Per doc 43 T4 algorithm 3-category taxonomy: Category A (character-wide) + Category B (chain-multiplicative) + Category C (chain-element-conversion-or-addition) are T4 territory

### 4.4 Genre alignment

This amendment matches the **Diablo 4 post-patch aspect refinement** (aspects became more skill-specific over patches because broad-scope aspects produced soup) and **PoE's cluster jewel pattern** (small-scope passives clustered into jewel slots; not character-wide).

### 4.5 Implementation discipline

Algorithm amendment in `gear_instance_generator.py`:
- Legendary capability candidates filtered by scope: only slot-bound / trigger-bound / skill-specific / item-family / conditional-state
- Capability scope_preference annotation field constrained to these 5 values (drop "character_wide" / "chain_wide" from legendary scope vocabulary)
- T4-attunement annotation (doc 40 D33 + D51) continues to carry chain_alignment + t4_target_intent — that's metadata about which T4 strategy the capability supports, NOT scope of effect

---

## 5. Layer 4 — Trigger-condition vocabulary expansion

### 5.1 Core insight

Current capability vocabulary uses 4-5 trigger conditions (on-attack / on-being-attacked / on-crit / on-kill). Each is a differentiation axis. Expanding the vocabulary multiplies design space without increasing density.

### 5.2 Expanded trigger condition catalog

| Family | Conditions |
|---|---|
| **Action-triggered** | on-hit / on-crit / on-cast / on-channel-end / on-channel-tick / on-finish |
| **Defense-triggered** | on-being-hit / on-block / on-dodge / on-CC / on-being-low-HP / on-cleanse |
| **Resource-triggered** | at-full-resource / spending-resource / empty-resource / on-resource-tick / on-resource-pop |
| **State-conditioned** | while-low-HP / while-full-HP / while-channeling / while-moving / while-stationary / while-buffed |
| **Enemy-state-conditioned** | vs-low-HP / vs-stunned / vs-elemental-resistant / vs-elite / vs-boss / vs-grouped |
| **Environmental** | in-fire-aura / in-water / near-allies / isolated / in-objective-area / in-encounter-special-zone |
| **Skill-conditioned** | using-T1-skills / using-T2-of-chain-X / using-specific-skill / after-T4-effect |
| **Combo-conditioned** | after-N-skills / on-combo-completion / on-skill-rotation-cycle / on-combo-break |
| **Positional** | while-flanking / while-behind-target / in-line-of-sight / in-melee-of / kiting-away |
| **Element-conditioned** | when-casting-fire / when-hitting-cold-immune / on-element-overlap / on-secondary-element |
| **Timer-conditioned** | every-N-seconds / first-N-seconds-of-combat / on-cooldown-tick / on-encounter-start |

### 5.3 Diversification discipline

The algorithm samples capability + triggered_passive from this expanded vocabulary with **per-character diversity constraints**:
- No two legendaries in a single loadout share the same trigger condition family (e.g., not 2 on-being-hit effects on different slots)
- Stat-affix partition modifiers (post-Layer 2 migration) can still share families freely — diversity discipline applies only to mechanic-altering content

### 5.4 Implementation discipline

Algorithm amendment in `gear_instance_generator.py` + capability template library:
- Template library carries the full trigger vocabulary with capability-category tags
- Per-loadout diversity filter applied at generation time
- Cohesion-judge LLM at Phase 5 uses trigger family for thematic synthesis (e.g., a build heavy on while-channeling triggers might narrate as "ritual-focused")

---

## 6. Layer 5 — Concentration probability table by tier

### 6.1 Core principle

**Not every legendary slot has a capability.** Capability density scales with rarity tier. Per-character at typical endgame: ~4-6 mechanic-altering effects (build-defining) + 5-7 stat-support legendaries with no capability.

### 6.2 Probability table

| Tier | Capability probability | Triggered passive probability | Stat affixes |
|---|---|---|---|
| **Common** | 0% | 0% | Full stat surface; ~1-2 affixes per slot |
| **Magic** | 0% | 0% | Full stat surface; ~2-3 affixes per slot |
| **Rare** | 0% | 0% | Full stat surface; ~3-4 affixes per slot + 1-2 affixes from "epic-and-up-only" affix list |
| **Epic** | 0% | ~25% (trigger-conditioned only; per Layer 2 § 3.3 boundary) | Full stat surface + Epic-exclusive trigger-conditioned affixes |
| **Legendary T0** | ~30% | ~50% | Capability OR triggered_passive (XOR — never both on same slot); full stat surface |
| **Legendary T0.5** | ~50% | ~50% | Capability OR triggered_passive (XOR); full stat surface + density boost |
| **Legendary T1** | ~75% | ~75% | Capability + possibly triggered_passive (both possible but rare); full stat surface + T4-attunement annotation |
| **Legendary T2** | 100% | 100% | Capability + triggered_passive both; chain + T4-attuned; full stat surface at highest density |
| **Set T1** | Set-piece REPLACES individual capability | Set-piece REPLACES individual triggered_passive | Stat surface preserved; 2pc + 4pc set bonus tags |
| **Set T2** | Same — set-piece replaces individual | Same | Highest stat density; set bonus tags |

### 6.3 Expected endgame loadout composition

For a typical endgame player with mixed gear acquisition:

| Slot type | Likely composition | Mechanical surface |
|---|---|---|
| Main weapon + secondary item | Legendary T1 or T2 OR set | 2 mechanic-altering items |
| Chest + helm + 1-2 of (hands/feet/legs) | Mix of legendary T1/T2 + epic | 2-4 mechanic-altering items |
| Remaining armor + accessory slots | Epic / Rare / set-piece-stat-only | 0-2 mechanic-altering items |
| **Total mechanic-altering** | | **4-6 items** (within genre canon) |

### 6.4 Set composition exception

When a player commits to a 4-piece set (per doc 40 § 3.5 + Block B1d): the 4 set slots have **NO individual capability/triggered_passive** — those are REPLACED by the 2pc + 4pc set bonuses. This is the genre-canonical "set replaces individual legendary powers" pattern (Diablo 3 lineage).

### 6.5 Gauntlet sim representative loadout discipline (Matt 2026-05-27)

> **The gauntlet sim's representative loadout should reflect a top-15% endgame-engaged player (per doc 40 D18 + § 4.1 85th-percentile target). That player has acquired full T1 legendary baseline AND has committed to set pieces where their T4-strategy-aligned set exists.**

The current Cycle 13 `gear_representative` pattern equips full T1 legendary across all 11 slots. This is the BASELINE — but it doesn't exercise the set bonus mechanic that's central to endgame build identity (per Layer 8 set keying to T4 strategy clusters).

**Amendment**: `gear_representative` composes as:
1. **Baseline**: Legendary T1 across all 11 slots
2. **Set replacement**: where a 4-piece set exists matching the character's T4-strategy × element cluster (per Layer 8), the matching 4 slots are REPLACED with set_t1 pieces — preserving the set bonus mechanic + 4pc T4-strategy amplification
3. **Result**: typical representative = 4 set pieces + 7 T1 legendaries

This produces a more realistic endgame representative for gauntlet sim validation. The set bonus mechanic gets empirical exercise. The remaining 7 T1 slots carry capability/triggered_passive per the concentration probability table (§ 6.2). Mechanical surface remains within genre canon (~5-8 effects: 1 set bonus + 4-6 individual capability/triggered).

**Implementation discipline**: gauntlet sim `representative_loadout_construction` in `season_generation_pipeline.py` (Cycle 14 Wave 1 amendment) reads the character's T4 strategy tuple, identifies matching set per Layer 8 keying, replaces T1 in those 4 slots with set_t1 pieces. Math note must capture this composition shift.

**Composition with Layer 9 (class-agnostic drops)**: drops still emit class-agnostically per Layer 9; this discipline only affects the BASELINE REPRESENTATIVE loadout for gauntlet sim validation (which represents an idealized 85th-percentile player). Actual player play involves variable drop acquisition; gauntlet sim represents the convergence point.

### 6.5 Implementation discipline

Algorithm amendment in `gear_instance_generator.py`:
- Per-rarity capability/triggered_passive probability gate per § 6.2 table
- XOR enforcement at T0/T0.5 (legendary has one or the other; never both)
- Stat-surface partition modifier rolls per doc 42 affinity matrix unchanged across all tiers (every gear instance has its stat affixes per rarity-appropriate count)
- Set pieces flagged as "individual-capability-replaced" — only set bonus content fires

---

## 7. Layer 6 — Cohesion-judge layered architecture

### 7.1 Core insight (Matt 2026-05-27)

> **The cohesion-judge LLM produces a CORE thematic identity weighted toward LOWER-tier chain nodes (which every player has from L1) + an OPTIONAL ENDGAME NOD that weaves in T4 / legendary / set themes if/when they manifest. The core identity must stand alone. Endgame content adds richness but cannot be load-bearing.**

This is the player-experience-preservation discipline: a casual player who never reaches endgame, never unlocks a T4 node, chooses a different T4 path, or never loots legendary/set items STILL has a thematically coherent character. Endgame content amplifies; it never defines.

### 7.2 Cohesion judge weighting architecture

| Layer | Source | Weight in identity narrative |
|---|---|---|
| **Tier 1 chain nodes (the foundational layer)** | Chain composition T1 mechanic-altering passives + actives | **HIGHEST** — these are present from L1 + early game |
| **Tier 2 chain nodes** | Chain T2 mechanic-altering content | **HIGH** — present from ~L15-30 |
| **Tier 3 chain nodes** | Chain T3 mechanic-altering content | **MEDIUM** — present from ~L30-45 |
| **T4 capstone (when unlocked)** | Specific T4 strategy player selected | **MEDIUM-LOW** — additive nod; identity should work without it |
| **Legendary/Set gear (when acquired)** | Capability + triggered_passive + set bonus content | **LOW** — vague nod weaving; identity should work without it |

### 7.3 Three core disciplines

**A. Identity-without-gear test**: at L1 with no equipped gear, the cohesion-judge LLM produces a thematically coherent character name + flavor + identity narrative. Test: would a player who only plays the first week of a season still recognize their character archetype?

**B. T4-choice-independence test**: the same character at L50 with different T4 strategies unlocked produces VARIATIONS of the same identity, NOT different identities. Test: a fire-pyromancer with RESOURCE_CONVERSION T4 and the same fire-pyromancer with TRADE_OFF T4 are recognizably the same character with different specializations.

**C. Endgame-nod-additivity test**: equipping a tier 1+2 legendary or set piece ADDS to the character's narrative ("the pyromancer now bears Phoenix's Mark") without REPLACING it. Test: removing the legendary returns the character to their core identity without breaking it.

### 7.4 LLM call architecture (Phase 5 territory; Cycle 14 implementation)

Cohesion-judge LLM call structure (per AI-tell discipline D7 + OP § 3.3 honor AI-tell line):

**Templated input structure** (the LLM does NOT see raw chain content; sees structured fields):
- CORE_LAYER: chain composition (T1+T2+T3 mechanic-altering content) — load-bearing for identity
- ENDGAME_LAYER: T4 strategy + tier 1+2 legendary capabilities + set bonus if applicable — additive nod
- SUBSTRATE_CONTEXT: BC cell + element + cohort + resource model
- THEMATIC_REGISTRY: genre-appropriate thematic vocabulary (isekai conventions per doc 38; archetypal naming per skill-system-2026-05-24)

**Templated output structure** (LLM fills narrow blanks):
- character_name: 2-4 word archetypal name (e.g., "Storm-Bound Reaver")
- core_identity_narrative: 1-2 sentence character identity, FOUNDED on CORE_LAYER content
- endgame_nod_narrative (optional): 1 sentence weaving ENDGAME_LAYER if present
- per-skill thematic flavor naming
- spirit-guide narration hooks

**Anti-pattern guard**: the LLM does NOT generate identity from gear stack. If the prompt structure suggests "describe this character based on their gear," the prompt is malformed.

### 7.5 Implementation discipline

- Cohesion-judge LLM call structure authored in Cycle 14 Phase 5 work (rocket Phase 5 + gandalf design-spec)
- Test fixtures verify all three disciplines (§ 7.3) at calibration time
- Spirit-guide voice (D28-D32 data-oracle) composes with layered cohesion — projections reference CORE identity primarily

---

## 8. Layer 7 — Compositional synergy scan amendment

### 8.1 Core insight (refined per Matt 2026-05-27 design conversation)

The compositional synergy scan locked in doc 43 § 8 (two-pass: resolve + preserve) was originally framed for T4 generation. **It extends to legendary capability + triggered_passive generation with a refined framing**:

- **Pass 1 (resolve)** = ENCOURAGE thematic seeds (apparent contradictions that the cohesion-judge LLM can synthesize into richer identity)
- **Pass 2 (preserve)** = FILTER redundancy (same-pattern_id stacking; same-trigger-window saturation)

The "first-do-no-harm discipline" candidate #7 from the morning session 2026-05-27 closeout applies here directly.

### 8.2 Pass 1 — thematic seeds ENCOURAGED

When the algorithm generates a capability or triggered_passive for a slot, it checks whether the candidate produces a **thematic seed** in combination with the kit's existing T4 + chain + element + other gear:

| Thematic seed pattern | Example | Action |
|---|---|---|
| **Cross-element combination** | fire-element kit + freeze_on_crit weapon → "explosive frost-fire" potential | SCORE BOOST — encourage |
| **Cross-mechanic synergy** | RESOURCE_CONVERSION mana→HP + life_steal_on_hit weapon → "blood-magic vampire" | SCORE BOOST |
| **Tension-resolution** | HP-cost mechanic + life_steal in chain → completion synergy | SCORE BOOST |
| **Cross-chain composition** | parallel chain with cold passive + fire T4 → thermal-shock identity | SCORE BOOST |

### 8.3 Pass 2 — redundancy FILTERED

When the algorithm generates a capability or triggered_passive, it checks for redundancy with existing slots:

| Redundancy pattern | Example | Action |
|---|---|---|
| **Same pattern_id duplication** | reflect_on_being_hit on head + reflect_on_being_hit on hands | REJECT — generate alternative |
| **Same trigger-window saturation** | 3+ effects firing on on_being_hit family | DOWNGRADE or REJECT |
| **Same effect-category duplication** | 2+ damage-reflection effects (reflect / thorns / counter) on same trigger | REJECT alternate slot's candidate |

### 8.4 Per-loadout diversity constraints

- **Hard dedup**: no two equipped legendaries have the same pattern_id (refl ect_on_being_hit can appear once per loadout, not twice)
- **Soft trigger-window cap**: no more than 2 effects per trigger-window family (on_being_hit / on_block / on_crit / on_kill / on_cast)
- **Effect-category dedup**: same effect-category (e.g., damage-reflection) capped at 2 instances regardless of pattern_id variance

### 8.5 Implementation discipline

Algorithm amendment in `gear_instance_generator.py` + per-loadout assembly:
- Per-loadout state tracker (pattern_ids equipped + trigger-windows occupied + effect-categories present)
- Generation candidate filter against per-loadout state
- Cohesion-judge LLM at Phase 5 receives per-loadout dedup/cap metrics + uses them in synthesis ("this character avoids the damage-reflection cliché by limiting it to one well-chosen item")

---

## 9. Layer 8 — Set keying to T4 strategy × element clusters

### 9.1 Core amendment (Matt 2026-05-27)

Sets are currently keyed per-character (set_id derived from character_id; e.g., `S1_endgame_dex_01_dagger_assassin_set`). This produces unique-per-character sets with no cross-class shareability.

**Amendment**: sets are keyed to **(Category A strategy × Category B/C strategy × primary element + secondary element if applicable)** — the same dimensional space the T4 algorithm operates in. Any character with a matching T4 strategy tuple can collect and benefit from the set.

### 9.2 Set keying mathematics

| Keying dimension | Range |
|---|---|
| Category A strategy | 4 options (RESOURCE_CONVERSION / TRADE_OFF / DEFENSIVE_CONVERSION / DEFENSIVE_TRADEOFF) |
| Category B/C strategy | ~4-5 options (Category B multiplicative + Category C ELEMENT_CONVERSION + Category C DUAL_ELEMENT_ADDITION + variants per primary element) |
| Primary element | 4 options (fire / water / earth / wind for v1 substrate) |
| Secondary element (for DUAL_ELEMENT_ADDITION only) | 3 options (the other 3 elements) |

**Total potential set keys**: 4 × 4 × 4 + 4 × 4 × 4 × 3 (for DUAL_ELEMENT cases) ≈ 256 distinct combinations theoretically.

**Practical season scope**: ~12-20 named sets per season covering meaningful T4 strategy × element clusters; many theoretical combinations cluster thematically.

### 9.3 Named set examples

| Set name (Phase 5 LLM-generated) | Set key | Characters benefiting |
|---|---|---|
| **Tempest-Bound Set** | RESOURCE_CONVERSION + ELEMENT_CONVERSION + wind | Any wind-element character running this T4 combo |
| **Iron Maiden Set** | DEFENSIVE_CONVERSION + ELEMENT_CONVERSION + earth | Any earth-element with this combo |
| **Frost-Reaper Set** | RESOURCE_CONVERSION + DUAL_ELEMENT_ADDITION + fire→cold | Fire-element + DUAL_ELEMENT with cold secondary |
| **Phoenix-Cycle Set** | RESOURCE_CONVERSION + Category B multiplicative + fire | Fire-element + multiplicative Category B |
| **Holy-Aegis Set** | DEFENSIVE_CONVERSION + ELEMENT_CONVERSION + water | Water-element with this combo (paladin/cleric archetypes) |

### 9.4 Cross-class shareability discipline

A set works for ANY character whose T4 strategy tuple matches the set's key:
- **dex_01 dagger_assassin** (wind / RESOURCE_CONVERSION / ELEMENT_CONVERSION) and **dex_04 twin_blade_fencer** (wind / RESOURCE_CONVERSION / ELEMENT_CONVERSION) BOTH benefit from "Tempest-Bound Set"
- The set's set_bonus content is keyed to amplifying the T4 strategy, not to the character archetype
- Mechanically: 2pc bonus + 4pc bonus tags reference T4 strategy amplification (composes with content-compositional attunement per doc 40 D33+D38+D51 amendment from morning session)

### 9.5 Composition with Legendary T2

| Tier | T4-attunement / amplification scope |
|---|---|
| Legendary T1 | Content composes with player's specific T4 candidate (chain + scope alignment per Block B1) |
| Legendary T2 | Same but higher density + capability toolkit at higher rate |
| **Set T1** | **Set bonus amplifies T4 strategy CLUSTER (broader than specific T4 candidate; serves multiple characters with matching strategy)** |
| **Set T2** | **Same with strongest amplification + 4pc set bonus** |

Sets pick up where T2 leaves off — they're the mechanical conversion's broader expression across characters who share the strategy.

### 9.6 Implementation discipline

Algorithm amendment in `set_generator.py` (new module; Cycle 14 rocket sidecar):
- Per-season set generation pass produces ~12-20 named sets keyed to T4 strategy × element clusters
- Each set has 4-piece composition (per doc 40 § 3.5 + Block B1d 4-piece lock)
- Set pieces drop in pool with rarity-appropriate frequencies
- Player collects toward sets that match their T4 strategy (or alts/trade)

### 9.7 Retirement of per-character bespoke set pattern

The current per-character set_id pattern (`S1_endgame_<char_id>_set`) is RETIRED. Existing Cycle 13 mechanical season data with per-character set_ids is preserved for diagnostic reference but not used as architectural reference.

---

## 10. Layer 9 — Class-agnostic spec-driven per-drop generation

### 10.1 Core amendment (Matt 2026-05-27)

Per session 2026-05-27 Block C lock (D21 Option A — calibrated drop rate, NOT smart-loot pity), Reincarnated rejected hidden smart-loot mechanics. This layer clarifies what fills the gap.

**Lock**: drops use class-agnostic spec-driven per-drop generation. Spec is keyed to substrate (BC cell + element + cohort + T4 strategy clusters); class/build relevance emerges from spec match, not from filtering.

### 10.2 Drop architecture

| Step | Mechanism |
|---|---|
| **Drop event** | Player kill / objective completion / random drop event |
| **Drop spec** | Substrate-keyed spec: e.g., "endgame T1 legendary [slot]" or "set piece for [T4-strategy-cluster]" |
| **Per-drop generation** | Substrate-led per-drop generation at drop-time against spec |
| **Naturally deduped** | Each instance has unique affix rolls + capability picks + triggered_passive picks; no two drops are identical instances |
| **Class-agnostic** | Drop can be relevant or not to current character; player evaluates each |

### 10.3 What this enables

For a fire-pyromancer running RESOURCE_CONVERSION + ELEMENT_CONVERSION at endgame:

| Drop probability band | Type | Use case |
|---|---|---|
| ~70% | Irrelevant gear (different element/cohort) | Vendor / trade / alt-character material |
| ~20% | Relevant-element gear (fire) but wrong T4 strategy | Partially usable; alt-T4 future seed; multi-T4 build path |
| ~10% | Directly aligned (fire + RESOURCE_CONVERSION + ELEMENT_CONVERSION) | Directly slots into current build |

These probability bands are calibration parameters tuned per D18 + D21 against engagement curve. PoE/D2-canonical model.

### 10.4 What this preserves

- **Transparent acquisition** (no hidden smart-loot mechanics; D21 Option A lock)
- **Honest discovery** ("did I get something rare/relevant?" satisfaction preserved)
- **Cross-character/trade economy** (irrelevant drops have value as alt-character seeds or trade material)
- **Substrate-led discipline** (specs come from substrate; drops sample against specs)
- **Composes with balance-as-property** (each drop is a generation event against spec)

### 10.5 What this prevents

- **Smart-loot resentment** (D3/D4 community complaint pattern about hidden mechanics)
- **Reverse-pity gaming** (player optimizing acquisition behavior to manipulate hidden filters)
- **Filter-curation drift** (no need to maintain smart-loot weighting tables that bias drops away from genuine substrate)

### 10.6 Implementation discipline

Algorithm amendment in drop pipeline (Cycle 14 territory):
- Drop event triggers spec generation against substrate
- Spec generated against player's current node (per progression framework doc 41) + drop pool restriction per content tier (D50)
- Per-drop generation against spec at drop-time
- Drop emitted with unique instance ID
- No smart-loot filter applied; class-agnostic by construction

---

## 11. How the 9 layers compose

The 9 layers interlock into the concentration architecture:

```
LAYER 1 (stat-range bounds) — prerequisite; bounds everything numerical
   ↓
LAYER 2 (affix migration) — reduces "stat-as-skill" noise; cleans rarity tier responsibilities
   ↓
LAYER 3 (capability scope reduction) — capabilities are LOCAL; T4 is GLOBAL
   ↓
LAYER 4 (trigger vocabulary) — expands differentiation axes without increasing density
   ↓
LAYER 5 (concentration probability) — not every legendary has capability; tier-scaled
   ↓
LAYER 6 (cohesion layering) — identity from chain composition; gear amplifies, never constitutes
   ↓
LAYER 7 (synergy scan refined) — thematic seeds ENCOURAGED; redundancy FILTERED
   ↓
LAYER 8 (set keying) — sets amplify T4 strategy clusters; cross-class shareable
   ↓
LAYER 9 (class-agnostic drops) — spec-driven per-drop generation; transparent discovery
```

**Together they produce**: a typical endgame loadout has ~4-6 mechanic-altering items (build-defining) + 5-7 stat-support legendaries + T4 capstone selected via player chain investment + 0-1 active set bonus (4-piece commitment). Total mechanical surface: ~5-8 mechanic-alterations per character at endgame. Within genre canon. Coherent for cohesion-judge LLM synthesis at Phase 5.

---

## 12. Cycle 14 sidecar scope mapping

Cycle 14 = Phase 5 cohesion coalescence per Q9 Pattern A. This doc's 9 layers integrate into Cycle 14 as follows:

| Layer | Cycle 14 work-unit | Owner(s) |
|---|---|---|
| **Layer 1 (stat-range bounds)** | Wave 0 / Wave 1: stat-range bounds canonical authoring + algorithm enforcement | gandalf (canonical) + rocket (algorithm) + jack-ryan (Gate-2) |
| **Layer 2 (affix migration)** | Wave 1 partition cycle: `general_passive_*` → partition affix migration | rocket + gandalf design-spec + jack-ryan Gate-2 |
| **Layer 3 (capability scope reduction)** | Wave 1 partition cycle: capability scope category amendment in `gear_instance_generator.py` | rocket + gandalf design-spec |
| **Layer 4 (trigger vocabulary)** | Wave 1 partition cycle: capability template library expansion | rocket + gandalf design-spec + legolas Mode A research (cross-ARPG trigger vocabulary research) |
| **Layer 5 (concentration probability)** | Wave 1 partition cycle: per-rarity capability/triggered_passive probability gate | rocket + jack-ryan Gate-2 |
| **Layer 6 (cohesion layering)** | Wave 2-3 Phase 5 cohesion-judge LLM architecture: layered cohesion prompt structure | gandalf design-spec + star-lord LLM integration + rocket call architecture |
| **Layer 7 (synergy scan refined)** | Wave 1 partition cycle: compositional synergy scan extension to legendary capability gen | rocket + gandalf + gamora methodology consultation (Discipline #18) |
| **Layer 8 (set keying)** | Wave 1 sidecar: new `set_generator.py` module with T4-strategy-aligned set keying | rocket + gandalf design-spec + elrond substrate input |
| **Layer 9 (class-agnostic drops)** | Wave 2: drop pipeline class-agnostic spec generation | rocket + star-lord drop event pipeline |

**Estimated Cycle 14 wall-clock**: ~3-5 weeks given the scope (Phase 5 cohesion + 9-layer remediation). Comparable to Cycle 13.

---

## 13. Doc 40 amendments required

This doc requires amendments to doc 40 (Cycle 13 architectural foundation) to keep canon coherent:

| Doc 40 decision | Amendment | In-doc-40 anchor |
|---|---|---|
| **D9** (capability toolkit: single capability per legendary, not all simultaneously) | Refined: capability scope LOCAL per Layer 3; tier-density per Layer 5 | doc 40 § 3.7 D9 inline amendment |
| **D33** (Tier 1+2 legendaries carry T4-attunement) | Refined: T4-attunement is metadata (per Block B1 content-compositional); sets ALSO carry T4-strategy-cluster keying per Layer 8 | doc 40 § 6.7 D33 inline amendment (composes with morning closeout § 3.4 amendment) |
| **D38** (T4-attuned gear specifics deferred) | RESOLVED: content-compositional attunement (morning 2026-05-27 lock) + set keying to strategy clusters (this doc Layer 8) + class-agnostic per-drop generation (Layer 9) | doc 40 § 6.7 D38 inline amendment (composes with morning closeout § 3.4 amendment) |
| **D49 + D50 + D52** (4-tier legendary + drop pool restriction) | Preserved; this doc adds tier-density probability table per Layer 5 | doc 40 § 3.7 D49 / D50 / D52 inline amendments |
| **D51** (T4-attunement reserved tier 1+2) | Refined: tier 1+2 legendaries + ALL sets carry T4-strategy-cluster keying; non-attuned content retains base value (consistent with content-compositional) | doc 40 § 3.7 D51 inline amendment (composes with morning closeout § 3.4 D51 AMENDMENT line in § 6.7) |
| **D54** (capability toolkit at all 4 tiers) | Amended: capability density scales with tier per Layer 5 (not flat across all 4 tiers); set pieces replace individual capability per Layer 5.4 | doc 40 § 3.7 D54 inline amendment |
| **D55** (triggered-passive high prob on weapons; true-actives weapons-only) | Preserved; tier-density per Layer 5; D55 weapons-only enforcement added per the violation surfaced in Cycle 13 empirical inspection (true_active_secondary_skill on off-hand slots) | doc 40 § 3.7 D55 inline amendment |
| **D56** (legendary modifier-surface expansion) | Preserved; clarified: scope of mechanic-altering content is LOCAL (Layer 3) | doc 40 § 3.7 D56 inline amendment |

Doc 40 amendment authoring is **Cycle 14 Wave 0 / Wave 1 gandalf canonical work**.

**✅ LANDED 2026-05-27 (Cycle 14 SC-2):** all amendments above were filed in-place at doc 40 per § 0.1 amendment-pass-record. Bidirectional cross-references are operational. See `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 0.1.2 for the doc 46 inheritance amendment index.

---

## 14. Discipline candidates (jack-ryan ratification queue)

This doc surfaces additional engineering-discipline candidates:

| # | Candidate | Source |
|---|---|---|
| **#33** | **Stat-range bounds discipline** | Layer 1 — bounded stats must have explicit caps; unbounded stats scale with progression; algorithm enforces at generation time + runtime |
| **#34** | **Concentration discipline** | Layer 5 — mechanic-alteration is concentrated to 2-6 build-defining items per character; rest is stat support; genre canon |
| **#35** | **Layered cohesion discipline** | Layer 6 — cohesion-judge LLM weights lower-tier chain nodes heavier; endgame content is additive nod, not foundational; identity must work at L1 without gear |
| **#36** | **Substrate-as-keying-source discipline** | Layer 8 — design surfaces (sets, legendary capabilities, drops) are keyed to substrate dimensions (BC cells + elements + T4 strategies), not to character-specific identifiers |
| **#37** | **Class-agnostic drop discipline** | Layer 9 — drops are spec-driven against substrate; class/build relevance emerges from spec match, not from filtering; rejects smart-loot hidden mechanics |

Composes with the 32 disciplines + amendments already in `engineering-disciplines.md` (#1-#32). Jack-ryan ratification fires as Cycle 14 SC-2 expansion.

---

## 15. Operational notes per seam

### 15.1 To rocket (generation seam)

Layer 1-5 + 7-8-9 implementations land in rocket Wave 4 Track A amendment + new `set_generator.py` module + drop pipeline (substantial Cycle 14 scope; ~2-3 weeks dedicated work). Math notes per Discipline #1 required for each layer's algorithm change.

### 15.2 To gamora (simulation seam)

Stat-range bounds (Layer 1) provide numerical constraints the gauntlet sim must respect at runtime. Concentration discipline (Layer 5) means typical character has fewer mechanic-alterations to simulate — gauntlet sim becomes more tractable empirically. Methodology consultation per Discipline #18 + #18.2 may be required for empirical re-calibration of WR-bracket ranges after concentration discipline lands.

### 15.3 To star-lord (telemetry + LLM seam)

Layer 6 cohesion-judge LLM call architecture lands in star-lord Phase 5 LLM integration work. AI-tell line discipline (D7) + OP § 3.3 critical: templated structure with LLM filling narrow blanks; not raw LLM dialogue generating identity from gear stack.

### 15.4 To drax (player surface seam)

Stat-range bounds (Layer 1) render in loadout app as cap indicators ("at crit cap"). Concentration discipline (Layer 5) means fewer mechanical effects to display per character — loadout page surface becomes cleaner. Layered cohesion (Layer 6) drives spirit-guide narrative voice + character display.

### 15.5 To elrond (substrate seam)

Set keying to substrate dimensions (Layer 8) means substrate provides cluster definitions for set generation. Substrate-led discipline preserved. T4 strategy × element clusters are substrate-curatable inputs.

### 15.6 To legolas (research seam)

Mode A research dispatches for Cycle 14:
- **Trigger condition vocabulary research** (Layer 4) — ARPG community catalog of trigger conditions across PoE / D2/D3/D4 / LE / GD / Lost Ark
- **Set design pattern research** (Layer 8) — D2 runeword patterns + D3 set pieces + LE set design + PoE unique pattern research
- **Cohesion-judge LLM call architecture research** (Layer 6) — best practices for layered narrative generation under AI-tell discipline

### 15.7 To jack-ryan (discipline + critique-pair seam)

Discipline candidates #33-#37 queued for SC-2 ratification. Gate-1 critique-pair throughput for Cycle 14: ~6-8 cycles estimated (this doc + doc 40 amendments + Layer 1-9 implementation Gate-1s + Phase 5 cohesion-judge Gate-1).

### 15.8 To knight-rider (orchestration seam)

Cycle 14 scope-doc authoring should consume this doc as architectural foundation. Wave structure proposal:

| Wave | Scope |
|---|---|
| Wave 0 | Cycle 14 scope-doc + doc 40 amendments + sidecar dispatches |
| Wave 1 | Stat-range bounds canonical + algorithm enforcement + affix migration + capability scope reduction + concentration probability table + trigger vocabulary expansion + synergy scan extension |
| Wave 2 | Set generator new module + class-agnostic drop pipeline |
| Wave 3 | Phase 5 cohesion-judge LLM architecture (layered cohesion) + spirit-guide data-oracle integration |
| Wave 4 | T4-attuned gear cohesion + acquisition curve calibration (D21 specifics) |
| Wave 5 | Gauntlet sim re-calibration + cohesion validation against full architecture |

Cycle 14 wind-down: Phase 5 cohesion layer complete; characters have narrative identity + naming + spirit-guide projections + acquisition curve calibrated. Sets working class-agnostically. Capability density within genre canon.

---

## 16. Cross-references

### 16.1 Canonical docs

- `canonical/00-ground-state.md` — register doc 46 as new CURRENT entry; foundational architecture
- `canonical/02-roadmap.md` — add doc 46 to companion docs; Cycle 14 scope expansion entry
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — amendments queued per § 13
- `canonical/41-progression-framework-2026-05-27.md` — composes (L50 hybrid framework + this concentration architecture)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — Layer 1 stat-range bounds extends the partition cycle
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — Layer 7 synergy scan extends T4 algorithm synergy scan
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — Layer 6 cohesion layering composes with T4 scope dimension
- `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` — Layers 2/3/5/7 amend Wave 4 Track A scope

### 16.2 Operational + agent docs

- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — morning session closeout; this doc continues the same-day Pattern-B design conversation
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` — empirical reference that surfaced the capability-soup pattern
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` — Block C scaffolding composes (substrate-led discipline + Q10 amendment)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — discipline candidates #33-#37 queued; Discipline #18 + #18.2 referenced

### 16.3 Decisions-log

Cycle 14 launch will produce decisions-log entries for the architectural commitments here. Not yet logged.

---

## 17. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — foundational architectural commitment for Cycle 14 sidecar; 9 layers locked
**Composition:** with doc 38 (delivery strategy keystone), doc 39 (engine workflow), doc 40 (Cycle 13 architectural foundation; amendments queued per § 13), doc 41 (L50 hybrid progression framework), docs 42-45 (Cycle 13 wave intent canonical docs), session closeout + Block C scaffolding + legendary T1 + T4 reference table from same-day Pattern-B session 2026-05-27

**For:** the concentration architecture (9 layers — stat bounds + affix migration + capability scope reduction + trigger vocabulary + concentration probability table + cohesion layering + synergy scan refined + set keying to T4 strategy clusters + class-agnostic drops) that remediates the capability-soup pattern empirically surfaced by Cycle 13 mechanical season + composes with all locked architecture into Reincarnated v1 Cycle 14 sidecar foundation. Identity = chain composition + T4 + 4-6 build-defining items + stat-affix support. Gear amplifies; gear does not constitute.

**Signed:** gandalf (story-and-design steward)
