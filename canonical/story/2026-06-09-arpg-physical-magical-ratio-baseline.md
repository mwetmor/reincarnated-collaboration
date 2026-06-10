# ARPG Physical / Magical / Hybrid Damage-Source Ratio — Empirical Baseline

> **STATUS:** CURRENT (load-bearing empirical baseline; reference for engine-generation tuning decisions)

**Date:** 2026-06-09
**Author:** gandalf (story-and-design steward) — with legolas methodology attestation
**Authority:** Matt 2026-06-09 directive to re-establish empirical baseline after prior research was lost
**Source-of-truth:** `agentic_orchestration/legolas/research/2026-06-09-arpg-physical-magical-ratio/synthesis.md` (full Legolas Mode A synthesis with per-game data + methodology notes + classification ambiguity dispositions)
**Companion docs:**
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (substrate primitive — element-family taxonomy this ratio applies to)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` (Pattern 6 substrate-led discipline at axis level; this baseline operates at element-family ratio layer)
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md` § Observation 2 (the misread that triggered this baseline rediscovery)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` (three-path routing: physical / magical / hybrid — the architectural framework this ratio measures against)

---

## 0. TL;DR

Across 8 ARPGs surveyed (Diablo II, Diablo III, Diablo IV, Path of Exile 1, Path of Exile 2, Last Epoch, Lost Ark, Torchlight 2), the genre-historical damage-source distribution is:

| Category | Central estimate | Plausible range |
|---|---|---|
| **Physical-primary** | 37-40% | 32-47% |
| **Magical-primary** | 47-52% | 40-60% |
| **Hybrid / Summon** | 13-18% | 10-25% |

**Recommended Reincarnated target band:** **38-45% physical** (central 40%).

**Watch flags:**
- **> 48% physical** → suggests warrior-archetype over-representation; investigate substrate skew
- **< 32% physical** → suggests caster over-representation; investigate substrate gap

**Current corpus position (as of 2026-06-09):** 43% physical → **within spec at upper boundary** of target band. Not urgent. Worth monitoring as corpus grows.

---

## 1. Why this doc exists

The previous gandalf-side research on this ratio was lost (Matt observation 2026-06-09: "you lost the docs on the actual historical average"). This caused a discipline failure during /forge Phase 3 close routing — the 43% physical observation was initially misread as imbalance requiring corpus-rebalance, when in fact it sits within ARPG genre-historical range.

**This doc protects against future re-loss.** Empirical baseline lives here in canonical/story/ with cross-reference to the full Legolas synthesis. Future engine-generation tuning decisions read this baseline; future corpus-composition observations are evaluated against this baseline; future "corpus rebalance" framings get checked against this baseline before commission authoring.

---

## 2. The baseline

### 2.1 Headline empirical finding

Per Legolas Mode A synthesis (commit `d83d5c5`; full data at source-of-truth path above):

| Category | Central estimate | Plausible range | Definition (Discipline #25) |
|---|---|---|---|
| **Physical-primary** | 37-40% | 32-47% | Build's primary damage numbers scale from weapon damage, attack speed, physical damage multipliers, or physical-tagged bleed/hemorrhage. Includes ranged physical (projectile builds scaling from weapon damage). |
| **Magical-primary** | 47-52% | 40-60% | All elemental and spell-based paths bundled (fire / cold / lightning / arcane / chaos / aether / vitality / necrotic / void / holy-light / dark-demonic / spell-scaling poison). Minion/summoner folded into magical-primary as sub-category. |
| **Hybrid** | 13-18% | 10-25% | Builds meaningfully scaling BOTH physical and magical simultaneously as co-equal scaling paths (not incidental procs). |

### 2.2 Per-game variance summary

The 32-47% physical-primary range across the 8-game survey reflects real per-game variance, not measurement noise:

| Game | Physical-primary % | Notes |
|---|---|---|
| **Diablo III** | ~26-28% | Outlier LOW (5 of 7 classes are spell-primary by design) |
| **Path of Exile 1** | ~28-33% | Long-running; rich archetype data; spell-leaning |
| **Last Epoch** | ~30-35% | Modern ARPG with clear damage-path taxonomy |
| **Diablo II** | ~33-38% | Classical reference; balanced classes |
| **Torchlight 2** | ~35-40% | Mid-range |
| **Path of Exile 2** | ~35-42% | Early-access; volatile; central estimate fuzzy |
| **Diablo IV** | ~43-47% | Upper-band (current meta; Barbarian/Rogue/Spiritborn dominance) |
| **Lost Ark** | ~45-48% | Upper-band (structural class-design bias toward physical/martial) |

**Inter-game variance is meta-sensitive.** A single over-tuned spell build (e.g., D3 Necromancer Death Nova in Season 35) can shift the effective ladder split by 10-15 percentage points in a given patch. Treat the central 37-40% as a moving target informed by patch cycles, not a fixed law.

---

## 3. Recommended Reincarnated target band

### 3.1 Target band: 38-45% physical (central 40%)

Reincarnated should generate kit corpora landing in the **38-45% physical band** with central target ~40%. Reasoning:

1. **Mid-range central avoids the high-variance edges** (D3 spell-heavy outlier; Lost Ark warrior-heavy outlier)
2. **40% central preserves narrative breadth** — physical kits read as "the warrior baseline"; magical kits read as "elementally flavored / spell-casting"; 40/50/10 split gives both narrative weight without either dominating
3. **Slight tilt above pure-PoE numbers (~30%)** acknowledges Diablo-lineage influence on Reincarnated's design DNA
4. **38-45% band is wide enough to accommodate** per-cycle generation variance + future content expansions

### 3.2 Watch flags

| Threshold | Signal | Action |
|---|---|---|
| **> 48% physical** | Warrior-archetype over-representation; substrate skew toward physical-damage-scaling outputs | Investigate substrate composition; consider engine-generation tuning to broaden caster archetypes |
| **< 32% physical** | Caster over-representation; physical-archetype substrate gap | Investigate weapon-substrate richness (physical kits depend on weapon-substrate variety); consider physical-substrate enrichment |
| **Hybrid > 25%** | Hybrid over-representation; suggests boundary between physical and magical is too permeable | Investigate three-path routing implementation (canonical 47); hybrid should be exception not default |
| **Hybrid < 10%** | Hybrid under-representation; missing meaningful cross-path builds | Investigate hybrid scaling parameters; doc 47 § 4 routing logic may be too strict |

### 3.3 Current corpus position

**As of 2026-06-09 (PROVISIONAL 1000-kit corpus per /forge Phase 3 baseline):**
- Physical: 43% → **upper boundary of target band; within spec**
- Magical: ~47% (per inferred distribution; not directly measured at this layer)
- Hybrid: ~10% (per inferred distribution)

**Disposition:** no urgent action. Watch for upward drift past 48% in future generation cycles.

---

## 4. Discipline #25 — semantic classification ambiguity

The ratio measurement depends on per-build classification, which has inherent ambiguity at boundary cases. Per Legolas synthesis, the main ambiguous cases:

| Case | Disposition (per Legolas methodology) |
|---|---|
| **Bleed / DoT** | Physical IF scales from weapon damage (D4 Barbarian Rend, D2 Whirlwind). Magical IF DoT procs from a spell (D3 Wizard Hydra). PRIMARY scaling path classifies. |
| **Conversion builds** (physical → fire, etc.) | Classified by SCALING PATH, not output element. PoE Molten Strike of the Zenith stacks physical → converts to fire → CLASSIFIED PHYSICAL. |
| **Minion / Summoner** | Folded into magical-primary sub-category. Minion-damage-scaling, not weapon-damage-scaling. |
| **Poison** | Magical when scaling from spell/cast mechanics (D2 Sorc Poison Nova, D3 Witch Doctor Jade Harvester). Physical when scaling from weapon/physical damage. |
| **Void (Last Epoch)** | Magical-primary; void is discrete magical damage type with dedicated spell-scale modifiers. |
| **Holy (D2 Paladin, Lost Ark Paladin)** | Magical-primary; scales from spell/aura power. |

**Reincarnated implication:** when classifying kit corpus against this baseline, apply the same PRIMARY-scaling-path-determines-classification rule. Doc 47 three-path routing aligns naturally — kits declare `damage_scaling_type: physical | magical | hybrid` at generation; classification flows from that field.

---

## 5. Known data gaps

Per Legolas synthesis:
- **PoE Ninja raw ladder data** not extractable (JS-rendered; all PoE figures from curated tier lists rather than true ladder snapshots)
- **Grim Dawn** returned 403 (excluded from survey)
- **PoE2 Early Access** data too volatile for stable genre baseline use
- **PoE figures** are curated-tier-list-based rather than empirical-ladder-based

**Future research triggers** (worth re-firing Legolas Mode A):
- PoE Ninja becomes scrape-able (JS rendering tooling improves)
- PoE2 stabilizes (post-1.0 release)
- Major ARPG genre shift (new flagship release substantially changes meta)
- Iteration on Reincarnated corpus surfaces target-band insufficiency (e.g., 40% physical feels wrong at playtest; revisit baseline)

---

## 6. Discipline observation worth tracking

The /forge Phase 3 close-routing process surfaced a discipline pattern worth flagging:

**Substrate-vs-genre-baseline questions require target-vs-watch-flag structure, NOT just min-max range.**

The iteration during /forge Phase 3 close-routing went:
1. Iteration 1 — "43% physical is imbalance; corpus-rebalance" (wrong direction; treated substrate-imbalance generically)
2. Iteration 2 — "43% is genre-correct; may need to push UP toward 50-55%" (wrong magnitude; treated range as flat — push to mid)
3. Iteration 3 (per this baseline) — "43% is within spec at upper boundary; central is 37-40%; watch flag at 48%" (correct)

Iteration 2's "push UP toward 50-55%" treated the 40-55% range I had recollected as flat — assumed mid was 47.5%. But the actual structure is: central 37-40% + plausible 32-47% + watch-flag at 48%. The structure matters — central, target band, watch flags are different operationally than "min-max range."

**Candidate Discipline #18.2 amendment (jack-ryan territory):** at substrate-vs-genre-baseline math hotspots, methodology consultation should produce target-vs-watch-flag structure, not min-max range. The discipline gap surfaced through this baseline rediscovery; worth jack-ryan ratification consideration at future cycle.

---

## 7. Cross-references for downstream consumers

This baseline applies when:

| Workstream | How it consumes |
|---|---|
| **Engine generation cycles** (rocket; substrate enrichment) | Validate per-cycle generated kit composition against 38-45% physical target; flag if outside band |
| **Corpus-rebalance commissions** (gandalf design-spec → elrond/rocket) | Use this baseline as the canonical reference for what "rebalance" means; rebalance direction informed by current vs target band + watch flags |
| **Cycle 15+ Pattern B on substrate composition** (Matt + gandalf) | This baseline is the empirical anchor for engine-generation tuning decisions |
| **Drax /forge cosmograph rendering** | Physical-anchor cluster size reflects substrate-truth; do NOT visually normalize against this ratio (substrate-honesty per Discipline #59 + Elrond Hotspot A) |
| **Future Legolas Mode A re-fires** | Re-establish baseline when one of the future-research triggers fires (§ 5) |
| **Future canonical decisions-log entries** | Reference this baseline if architectural commitments around substrate composition land |

---

## 8. Maintenance protocol

This doc is **CURRENT** while:
- ARPG genre composition holds at surveyed levels
- Reincarnated corpus continues operating within or near target band
- No major paradigm shift in ARPG damage-source taxonomy

**Re-fire Legolas Mode A research** (and amend this doc) when:
- A new major ARPG release substantially shifts the genre central estimate
- PoE Ninja becomes scrape-able (replace curated-tier-list data with ladder-snapshot data)
- Reincarnated iteration surfaces target-band insufficiency
- 12+ months elapse since last research-fire (cyclical refresh discipline)

**Update this doc** (without re-firing research) when:
- Reincarnated corpus position changes substantially (update § 3.3)
- Downstream consumer adds new use case (extend § 7 cross-reference table)
- Discipline #18.2 amendment ratifies (extend § 6 or remove if amendment supersedes)

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt direction to author canonical-story baseline doc following Legolas Mode A research close.

**Authority:** gandalf design-side authorship + legolas methodology attestation; Matt 2026-06-09 commissioned the underlying research + authorized canonical capture to prevent re-loss.

**Status:** load-bearing empirical baseline; informational reference for future engine-generation tuning + corpus-composition observations.

**Composition with prior canonical commitments:** all preserved (atomic-substrate-registry 2026-06-06 + canonical 47 damage scaling architecture + legacy categorical cleanup audit 2026-05-22 + drax Phase 3 close report; this baseline composes natively as informational reference).

**End of baseline doc.**
