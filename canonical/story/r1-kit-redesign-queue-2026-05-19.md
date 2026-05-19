# R1 Kit-Redesign Queue — Catalogue Pathology Surfaced by R1 Disposition Sequence

**Status:** Canonical-story doc. Authored by gandalf 2026-05-19 under autonomous-operation authority (Matt directive 2026-05-19; protocol § 4.0).

**Trigger:** gamora's R1 retune sprint v2 (engine commit `2546180`) demonstrated 0/51 boss kills across the shipped class catalogue under the disposition-1 corrected (kills-only) semantic. Inspection of representative classes confirmed the failure is kit-architectural, not modifier-tuning. The disposition-3 encounter recalibration (`R1-blocker-3-disposition-2026-05-19.md`) makes the gate REACHABLE for well-designed kits; this doc captures the kit pathology pattern that disposition-3 cannot fix and frames the redesign work for VS2a/VS2b roadmap consumption.

**Authority:** gandalf authors the queue + design criteria (gandalf seam: design / canonical / architectural). Implementation of the queue (catalogue regeneration with kit-redesign rules) is rocket seam. Sequencing into VS2a/VS2b is knight-rider + Matt at roadmap-commit time. **This doc surfaces the queue; it does NOT commit Matt or rocket to a sprint timeline. That decision lives in the normal roadmap process.**

**Position in the R-batch sequencing:** The kit-redesign work is **downstream of R3 (per-skill range + AI behavior schema migration; rocket + star-lord + elrond; 2-4 wk)** — R3 is the schema prerequisite that enables the kit-redesign to express what it needs to express ("lightning mage with 10m primary attack" requires the per-skill range field). The queue this doc captures becomes operationally consumable AFTER R3 lands.

---

## § 0 — TL;DR

51 of 51 shipped classes failed the R1 per-tier gate after two dispositions corrected the gate's semantic (kills-only) and calibrated the encounter to genre norms (HP, armor, duration). The remaining failure is the catalogue's: shipped classes were converged under an aggregate-WR gate that masked per-tier failures, so the catalogue contains kits that are mathematically convergent but mechanically incoherent. Specifically:

**Three pathology patterns identified:**

1. **Archetype-mechanic mismatch (severity HIGH).** Classes named "lightning_mage", "fire_mage", "shadow_mage" — archetype tags implying ranged spellcaster — composed entirely of `range_m = 2.0` skills. The lightning_mage candidate `class_0016` (highest-int in catalogue at 155) has FIVE skills all at melee range. **A "ranged caster" with no ranged skill cannot kite a boss; cannot exploit positioning; cannot survive the boss's melee damage; cannot achieve the kill rate the archetype tag implies.**

2. **Boss-DPS-floor structural insufficiency (severity HIGH).** Classes saturate the engine modifier ceiling (4.0) under the weighted convergence binary search and still fail boss kill rate. At modifier 4.0, lower tiers (swarm/magic/elite) blow ceilings by 100-300 percentage points — meaning the class is mathematically a glass cannon at low tiers but lacks the burst architecture (sustained damage windows, energy-cycling, cooldown management) to penetrate boss armor. Affects ~10 of 51 classes including `class_0008` (physical_grappler at modifier 4.0), `class_0018` + `class_0045` (shadow_mage at modifier 4.0), `class_0033` + `class_0044` (holy_caster at modifier 1.4-3.5).

3. **Defensive-layer absence (severity MEDIUM).** Most class kits contain 1 defensive skill (shield self-buff) and 4 damage skills. Against a boss at melee range (the de-facto reality due to pattern 1), a 6-second shield on an 8-second cooldown is structurally insufficient. Comparison genre kits (D2 Sorceress Energy Shield + Telekinesis; PoE Aurabot variants; D4 Necromancer Bone Storm) carry multi-layer survival systems including positional escape mechanics. The catalogue's defensive layer is single-vector.

**The redesign queue:**

- **~20-30 classes** require partial kit redesign (range diversity injection; one ranged skill on each "caster" or "mage" tagged class; one positional-shape skill on each "controller" tagged class)
- **~10 classes** require deep kit redesign (rebuild defensive layer; redistribute energy-cycling; align archetype description to actual kit composition)
- **~5-10 classes** are kit-acceptable post-disposition-3 and don't require redesign

These categories materialize CLEARLY post-sprint-v3; the sprint output is the operational signal for queue partition. This doc captures the design framework; the per-class assignment to categories happens after sprint v3 closes.

---

## § 1 — Evidence base

### § 1.1 — Empirical signal from sprint v2

Per `output/R1-class-retune-2026-05-19/summary.md`:

- 51 classes evaluated
- 51 classes failed boss tier (boss_kill_rate = 0.000 across the entire catalogue)
- 50 classes failed mini-boss tier (mini_boss_kill_rate = 0.000)
- 35 classes passed elite tier (68.6% pass rate)
- 12 classes passed magic tier (23.5%)
- 15 classes passed swarm tier (29.4%)
- 0 classes passed all 5 tiers

**Modifier saturation pattern (10 of 51 classes):**

| Class | Archetype | Modifier | Swarm | Magic | Elite | Mini-Boss | Boss | Pattern |
|---|---|---|---|---|---|---|---|---|
| class_0008 | physical_grappler | 4.00 | 1.00 (fail) | 1.00 (fail) | 1.00 (fail) | 0.000 (fail) | 0.000 (fail) | Modifier-saturated; kit cannot scale to boss-DPS threshold |
| class_0018 | shadow_mage | 4.00 | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | Modifier-saturated AND lower tiers also fail — totally broken kit |
| class_0019 | physical_warrior | 2.05 | 1.00 (fail) | 1.00 (fail) | 1.00 (fail) | 0.400 (pass) | 0.000 (fail) | Modifier 2× yields mini-boss kill but boss unreachable |
| class_0033 | holy_caster | 1.43 | 1.00 (fail) | 1.00 (fail) | 1.00 (fail) | 0.533 (pass) | 0.000 (fail) | Same pattern |
| class_0038 | experimental | 1.43 | 1.00 (fail) | 1.00 (fail) | 1.00 (fail) | 0.533 (pass) | 0.000 (fail) | Same pattern |
| class_0045 | shadow_mage | 4.00 | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | 0.000 (fail) | Same as 0018 |
| class_0060 | holy_controller | 4.00 | 0.500 (fail) | 0.500 (fail) | 0.500 (pass) | 0.000 (fail) | 0.000 (fail) | Modifier saturated; kit still cannot DPS |

The shadow_mage at modifier 4.0 with WR = 0.0 across every tier (including swarm, where a class at 4× damage SHOULD trivially clear pack monsters) is the most extreme kit pathology in the catalogue — the kit fails BOTH burst (cannot kill boss) AND sustained damage (cannot kill swarm at maximum modifier). This is a "kit cannot DPS at any modifier" diagnosis, the deepest tier of kit-broken.

### § 1.2 — Kit composition inspection (class_0016 — representative)

`class_0016`: "Chartbound Stormscribe", lightning_mage, range_profile "close", int=155, vit=64.

| Skill | Role | Geometry | range_m | Damage | Cooldown |
|---|---|---|---|---|---|
| skill_000369 | primary_attack | melee_strike | **2.0** | 625 | 0.8s |
| skill_000370 | burst_damage | chain_lightning | **2.0** | 2500 | 6.4s |
| skill_000371 | area_damage | chain_lightning | **2.0** | 1500 | 6.0s |
| skill_000372 | damage_over_time | circle | **2.0** | 750 + 2s shock | 5.0s |
| skill_000373 | defensive | self_buff | 0.0 | 1000 shield, 6.8s duration | 8.2s |

**Every damage skill is at 2m range.** The kit is structurally identical to a melee fighter despite the `lightning_mage` archetype tag. A genre-comparable "lightning mage" (e.g., Lightning Tendrils Wizard in D3, Storm Brand in PoE, Lightning Sorc in D4 Last Epoch lineage) operates at 10-25m with chain-lightning skills that genuinely propagate across distance. The catalogue's "chain_lightning" geometry is here at 2m, meaning it's a melee skill with chain-flavor naming — not a propagating-across-distance ranged skill.

**The same pattern holds for the catalogue's other "mage" classes** (visual inspection of the summary table shows hybrid_mage, fire_mage, shadow_mage, lightning_mage, water_mage, earth_mage entries all at modifier 0.05 floor with similar tier patterns — they ARE all glass cannons at melee range without the kiting tools to survive). This is a generation-time decision (geometry pool weighting) that produced kit compositions semantically inconsistent with the archetype tags.

### § 1.3 — Why this is not a per-class tuning issue

R1 sprint v2 attempted exactly the per-class tuning fix: weighted convergence binary search across 51 classes, applying the kills-only semantic to align the gate with player-experience semantic. The mathematical limit is hard: a kit with all skills at 2m range against a boss with 86.4% armor and 110k HP in 120s simply cannot deal enough damage REGARDLESS of modifier value. The modifier sweep proves this — at modifier 4.0 the kit STILL fails boss.

**Per-class modifier tuning is the WRONG lever for the WRONG problem.** The right lever is kit redesign at the catalogue layer.

### § 1.4 — Why disposition-3 (encounter recalibration) helps but doesn't resolve

The disposition-3 recalibration (boss HP 0.50x; boss armor 0.55x; boss duration 180s) brings boss effective-HP within reach for well-designed kits (forecast: 5-10 classes pass post-disposition-3). It does NOT rescue kits with the range-collapse pathology — a melee-range "mage" still cannot kite a boss; reducing boss HP from 110k to 55k still leaves a kit with no defensive layer against a melee-aggressive boss. The encounter recalibration is the engine-rebuild's contribution; kit redesign is the catalogue's contribution. Both are required for the full picture.

---

## § 2 — Definitions: kit-broken vs kit-mediocre vs kit-acceptable

Post-sprint-v3 (disposition-3 applied), each class falls into one of three categories based on observed per-tier pass pattern + modifier convergence:

### § 2.1 — KIT-ACCEPTABLE (forecast: 5-10 classes of 51)

Passes all 5 per-tier gates at modifier in [0.3, 1.5] under disposition-3 calibration. Kit composition is internally coherent (archetype tag matches kit's actual range profile; defensive layer is multi-vector; energy cycling permits sustained boss engagement). **No redesign required.** May warrant minor tuning iterations but not architectural change.

### § 2.2 — KIT-MEDIOCRE (forecast: 20-30 classes of 51)

Passes lower tiers (swarm + magic + elite) but fails boss and/or mini-boss kill rate under disposition-3 calibration. The kit composition has fixable issues — typically one of:
- Missing ranged damage skill (archetype implies ranged, kit is all-melee)
- Single defensive skill insufficient (genre comparable kits have 2+ defensive layers)
- Energy cost / cooldown architecture prevents sustained burst windows
- Primary attack damage / cooldown ratio doesn't scale with intelligence/dexterity stat investment

**Redesign scope:** partial kit redesign. Swap 1-2 skills with archetype-aligned alternatives. Adjust energy/cooldown for one burst window. Add positional-shape geometry where archetype implies it.

### § 2.3 — KIT-BROKEN (forecast: 10-15 classes of 51)

Fails multiple lower tiers AND boss/mini-boss tiers under disposition-3 calibration. Pattern: kit either (a) saturates modifier ceiling and still fails all tiers (shadow_mage 0018/0045 pattern), or (b) sits at modifier floor with multi-tier failures (extreme glass cannon archetype with no defensive layer, no DPS scaling), or (c) presents archetype-name pathology so severe that the kit's identity is wrong (lightning_mage at all-melee range is borderline kit-broken; a hypothetical "ranged hunter" with all melee skills WOULD be kit-broken in this category).

**Redesign scope:** deep kit redesign. Rebuild defensive layer (add disengage skill, replace single shield with multi-vector survival). Redistribute skill roles (primary + burst + sustained + AOE + defensive — not 4 damage + 1 defensive). Align archetype description to kit composition (rename archetype if redesign doesn't honor the tag; rebuild kit if redesign should honor the tag).

---

## § 3 — Redesign criteria (per category)

### § 3.1 — Range diversity criterion (HIGH priority)

Every class with `range_profile: medium` or `range_profile: long` MUST contain at least one damage skill with `range_m >= 8`. Every class with `range_profile: close` MAY remain all-melee but MUST contain at least one disengage or positional-escape skill (mobility skill, dash, blink, knockback-on-self, gap-create geometry).

**Genre canon:** D2 Sorc has Teleport. PoE Witch has Flame Dash. D4 Sorcerer has Teleport. Grim Dawn Spellbinder has Sigil/Devotion proc mobility. **No "caster" in any genre lineage operates without distance-management tooling.**

R3 schema migration is the prerequisite — the catalogue needs `range_m` per-skill field to express this criterion. Until R3 lands, the kit-redesign queue is documented but not executable.

### § 3.2 — Defensive layer criterion (HIGH priority)

Every class kit MUST contain at least two distinct survival mechanisms drawn from a defined palette:

- Shield/absorb (single duration; absorbs N damage)
- Healing (instant or HoT recovery)
- Damage reduction (resistance buff; defense uptime)
- Disengage / repositioning (movement skill; teleport; gap-create geometry)
- Crowd control (root/stun/slow on enemy that mitigates incoming damage by gating enemy attacks)

The current pattern (1 self-buff shield on 8s CD + 4 damage skills) is single-vector defensive — fails when the single mechanism is on cooldown. Two mechanisms allow alternation; three permits genre-canonical "defensive uptime" play patterns.

**Genre canon:** D2 Druid carries Cyclone Armor (absorb) + Heart of Wolverine (healing) + Werewolf Lycanthropy (HP increase). PoE Templar carries Determination (resistance) + Molten Shell (absorb) + Steelskin (instant absorb on hit) routinely. **One defensive skill is a building block; two+ is a layer.**

### § 3.3 — Burst-window architecture criterion (MEDIUM priority)

Every class MUST have a burst window every 4-8 seconds where sustained DPS spikes by ≥ 2.5× baseline. The burst window is typically: high-damage low-CD skill firing inside a buff-skill duration; or a multi-skill combo with cooldown alignment; or an energy-discharge pattern (build resource → spend resource for burst).

**Why:** boss kill structurally requires burst windows because effective DPS = baseline × armor_passthrough is too low to kill in time without compression. **Boss kill is about WHEN you deal damage, not just HOW MUCH.** Kits without burst windows are sustained-DPS classes that work against swarm/magic/elite but fail boss/mini-boss.

### § 3.4 — Archetype-description alignment criterion (MEDIUM priority)

The class `archetype_tag` must match the kit's actual composition pattern. Specifically:

- `*_mage` implies: at least 2 ranged damage skills (`range_m >= 8`), intelligence-stat-dominant scaling, mana energy
- `*_warrior` implies: at least 2 melee damage skills (`range_m <= 4`), strength/dexterity-stat-dominant scaling, stamina/rage energy
- `*_caster` implies: at least 1 ranged damage skill + 1 channel/ramp skill, intelligence/wisdom-dominant scaling, mana
- `*_controller` implies: at least 2 crowd-control skills (slow/root/stun applications), wisdom/intelligence-dominant scaling
- `hunter` implies: at least 2 ranged damage skills, dexterity-stat-dominant scaling
- `*_grappler` implies: at least 1 melee-pull or close-distance skill (gap-close geometry), strength-dominant
- `experimental` is exempt (intentionally unconventional)
- `hybrid_*` permits mixing but should explicitly compose two compatible patterns from above

This is design-time enforcement at the generation pipeline (rocket seam). Until enforced, the catalogue accumulates archetype-mismatched kits like class_0016. **R8 (season-as-emergent-output) provides an interesting alternative: if archetype emerges from converged kit composition, the mismatch can't happen because the tag is OUTPUT-FROM-KIT not INPUT-TO-KIT.** This is OBLIQUE EVIDENCE FOR R8 — captured in the disposition-3 doc § 9.5 cross-reference.

### § 3.5 — Energy-cycling pattern criterion (MEDIUM priority)

Every class's energy-cost / cooldown / damage triplet across the 5 skills MUST permit sustained engagement for at least 30 seconds without resource starvation. Empirically: total energy cost / (average mana regen × 30s) ≤ 1.2. If a class kit has total skill energy cost / sustained mana regen ratio > 1.2, the class will run out of mana mid-fight and stop dealing damage. This is what produces some of the "modifier 4.0 still failing every tier" classes — the kit can't keep its damage skills firing.

**Validation:** sprint v3 telemetry should capture per-class average mana/energy state across the fight (proxy for cycling viability). Star-lord telemetry surface could expose this without architectural change. Until then, kit-design-time validation against the formula.

---

## § 4 — Integration with R3 schema migration

R3 introduces:
- `range_m` per skill (currently exists but is set inconsistently — e.g., chain_lightning at 2.0)
- `preferred_behavior` on monsters (melee_aggressive / ranged_kite / cast_at_range / charge_then_melee)
- `aggro_radius_m`, `leash_distance_m`, `telegraph_window_seconds`
- `range_profile_redistribution` across the catalogue

**Kit redesign requires R3 to land first because:**
1. The range-diversity criterion (§ 3.1) needs `range_m` to be the OFFICIAL semantic field — not a default-set artifact
2. Validation that "lightning_mage class kit has at least one skill at range_m >= 8" requires the field to be authoritatively set by the geometry-type generator, not random
3. Per-skill range affects fight simulation outcomes — kit redesign needs the fight engine to honor range correctly before kit changes can be validated

**Sequencing:** R3 (rocket + star-lord + elrond; 2-4 wk) → VS2a kit-redesign sprint (rocket; 4-6 wk; co-design with gandalf for design criteria) → VS2b validation pass (gamora + jack-ryan; 1-2 wk).

This is roadmap-level work, NOT engine-rebuild work. The kit-redesign queue is gandalf's seam output; rocket's seam consumption; roadmap-committee (Matt + gandalf + rocket + knight-rider) sequencing.

---

## § 5 — Roadmap integration (proposed, NOT committed)

This is a roadmap-recommendation, not a roadmap-commitment. Matt + gandalf + rocket + knight-rider decide commit at the normal roadmap-review point.

### § 5.1 — VS2a (proposed: kit-redesign sprint)

After R3 ships, rocket leads a 4-6 week sprint:
- Audit the 51 shipped classes against criteria § 3.1-§ 3.5
- Categorize: kit-acceptable / kit-mediocre / kit-broken (per sprint v3 output)
- Redesign kit-mediocre classes (~20-30 classes; partial redesign per § 2.2)
- Redesign kit-broken classes (~10-15 classes; deep redesign per § 2.3)
- Regenerate (or hand-author + LLM-finish) the redesigned classes
- Re-run R1 sprint against the redesigned catalogue
- Expected outcome: 70-85% pass rate (the original R1 hypothesis-test threshold genuinely met at the catalogue level)

Co-design support from gandalf (criteria § 3, archetype-tag conventions, design pushback on pathology patterns). Validation support from gamora (R1 sprint re-run as the metric).

### § 5.2 — VS2b (proposed: validation pass)

After VS2a kit-redesign ships:
- Full R1 sprint against the redesigned catalogue
- Decisions-log entry capturing the redesign methodology + outcome
- Tag `vs2b-kit-redesign-validated` if R1 sprint achieves 70%+ pass rate
- If <70%, gandalf authors a further design disposition addressing the remaining pathology (likely architectural rather than per-class)

### § 5.3 — Alternative: R8 as kit-redesign substitute

R8 (season-as-emergent-output A/B; rocket + star-lord + gandalf; 1-2 wk) tests whether converged content can produce coherent themes WITHOUT theme-as-input. If R8 PASSES its hypothesis criteria, the lesson generalizes: **the catalogue's kit pathology is an artifact of theme-driving-generation. Inverting the pipeline (mechanic first, theme emerges) may produce more-coherent kits by construction.** In that case, VS2a kit-redesign becomes "convert catalogue generation pipeline to R8 inversion mode + regenerate from scratch" instead of "hand-redesign 30-40 classes." This is a strategically different shape of work — potentially faster but with higher uncertainty.

**The decision between the two paths (VS2a hand-redesign vs R8-inversion regeneration) is roadmap-level and depends on R8's A/B outcome.** This queue doc captures both alternatives so Matt + gandalf + rocket have the design surface to choose at commit time.

---

## § 6 — Rocket seam consultation (advisory; not binding)

Author's note (gandalf): rocket owns the catalogue. The kit-redesign work is rocket's seam by definition. This doc surfaces the design criteria gandalf judges necessary; rocket has L1 authority on implementation choices within those criteria. Specifically:

- HOW to redesign (hand-author vs LLM-redesign-with-criteria-prompt vs hybrid) is rocket's call
- WHICH classes to redesign first within the queue is rocket's call (informed by sprint v3 categorization)
- WHAT the new geometry-type / range / energy / role assignments should be for each redesigned skill is rocket's call (consulting gandalf design input where archetype-conventions are in question)
- WHEN VS2a fits into the roadmap is knight-rider + Matt decision

This doc is the design framework; rocket is the seam that builds against it.

---

## § 7 — Cross-references

- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` — disposition that authorizes this queue and frames the engine-side recalibration
- `reincarnated-engine/design/working-agreement/R1-structural-blockers-disposition-2026-05-19.md` — disposition-1 (kills-only semantic + HP calibration)
- `reincarnated-engine/design/working-agreement/R1-retuning-math-2026-05-19.md` — math notes (multi-section; armor curve + modifier impossibility + disposition math)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` — the parent canonical-story doc; R3 + R8 specifications relevant to kit-redesign sequencing
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — protocol § 2.3 scope-creep handling (kit redesign is correctly out-of-scope for the engine-rebuild and into VS2a/VS2b)
- `output/R1-class-retune-2026-05-19/summary.md` — gamora's sprint v2 per-class evidence
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` — full hive context

---

## § 8 — Provenance

Authored 2026-05-19 by gandalf concurrent with `R1-blocker-3-disposition-2026-05-19.md`. Under autonomous-operation authority (Matt directive 2026-05-19; protocol § 4.0). This doc is the canonical handoff from R1 (engine-rebuild seam) to VS2a/VS2b (catalogue + design seam).

**Inputs synthesized:** same as disposition-3 (R1 sprint v2 outputs; sample class JSONs; genre-canon references; math note + disposition predecessors).

*Filed 2026-05-19 by gandalf. The gate works. The encounter is honest. The catalogue carries pathology that the gate now surfaces clearly. The kit-redesign queue exists; the roadmap decides when to invest in it. Mithrandir signs.*
