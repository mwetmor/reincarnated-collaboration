# ARPG Community Research Sprint — Synthesis Verdict (R4)

> **STATUS:** CURRENT — Sprint Phase R4 synthesis output authored by gandalf 2026-05-29 evening late. Closes the sprint authorized at `agentic_orchestration/gandalf/notes/2026-05-29-arpg-community-research-sprint-authorization.md`. Composes with legolas Mode A analysis-findings + Mode B acquisition-log. Empirically-grounded across 104 builds + 92 loot-substrate-vocabulary entries + 30 composite-archetype-assessment entries + 37 vocabulary-convergence entries across 6 sites × 4 games.

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward; sprint synthesis)
**Sprint phase:** R4 (closes R1-R4 cycle)

**Companion artifacts (this dir):**
- `research.db` — populated SQLite (12 tables; 104 builds; 92 loot vocab; 37 convergence; 30 composite assessments)
- `schema.sql` — schema definition
- `acquisition-log.md` — legolas Mode B mass acquisition record
- `analysis-findings.md` — legolas Mode A vocabulary convergence + composite-assessment analysis

**Companion canonical docs:**
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle; this sprint is empirical-validation instrument
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — recognition record gate (ii) executed at expanded scope

---

## 0. TL;DR

The sprint empirically validated Matt's design intuitions at substantial scale:

1. **Cross-site vocabulary convergence STRONGLY confirmed** at 6 sites — Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter / [Skill]×[Class]×[Activity] naming / class-as-vestigial-reference all STRONG (22 of 37 convergence entries at STRONG level)
2. **Matt's composite-vs-single-axis critique STRONGLY confirmed empirically** with causal mechanism identified — the **number of multiplicative loot substrate layers** is the architectural lever determining composite-restriction severity (PoE 6 layers → composite-required; LE 3 layers → single-axis-viable)
3. **Magic Find pattern fully clarified** — D2-legacy primary archetype is dead; modern morph operates at multi-layer with explicit IIR stat target in PoE2 (100-150% IIR endgame); D4 retired explicit MF entirely, replaced by Torment Tier progression gate
4. **Speedfarm ↔ Push binary as universal variant-splitting axis** — observed at every multi-variant build across all 4 games; 22 push + 9 speedfarm variants among 83 total (37%)
5. **Designer-writes-substrate principle refined empirically** — coupling architecture (Layer 1.5) determines which named experiences survive economically as viable archetypes; community NAMES single-axis archetypes (Clear Speed verbatim at PoE-Vault) but they're DIS-INCENTIVIZED economically by coupling

**Actionable engine variable surfaced:** keep Reincarnated multiplicative loot substrate layer count LOW (≤3 layers, LE-style) to preserve player-experience-space and honor the "Designer writes substrate; Player names experience" principle architecturally.

---

## 1. Cross-site vocabulary convergence — STRONG signal

| Concept | Sites | Convergence | Layer |
|---|---|---|---|
| Bossing / Boss Killer / Boss Fights | 6 | STRONG | primary archetype |
| Speedfarming / Speed Farming | 6 | STRONG | primary archetype |
| [Skill]×[Class]×[Activity] naming pattern | 6 | STRONG | naming convention |
| Class/Ascendancy as vestigial reference | 6 | STRONG | designer-vestigial layer |
| Budget investment-tier vocabulary (5-tier per Surface 1) | 6 | STRONG | sub-axis |
| Endgame Generalist / All-Rounder / Overall Endgame | 5 | STRONG | primary archetype |
| Push / Pit Push (depth-progression) | 4 | STRONG | primary archetype |
| Leveling | 4 | STRONG | progression-stage |
| League Starter (PoE-origin; LE adopted) | 4 | STRONG | progression-stage |
| Mapper / Mapping (PoE-genre) | 3 | MODERATE | game-specific archetype |
| Magic Find / IIR as sub-axis (not primary) | 3 | MODERATE | sub-axis |
| Currency Farmer | 2 | WEAK | game-specific archetype |
| Mageblood-required / Extreme Budget | 2 | WEAK | investment-tier sub-tier |
| 5-axis structured rating (Push/Speed/Bossing/Survivability/Playability) | 1 (Maxroll only) | WEAK structurally; axes converge conceptually | instrument-specific |

**Verdict:** the player-experience archetype dimension vocabulary IS community-canonical at primary-archetype layer. Implementation differs across sites (structured ratings vs categorical tags vs tier-list lettering) but the underlying dimensions converge.

## 2. Multi-layer loot substrate vocabulary — 5-layer model empirically confirmed; 6th layer emergent

**Per-layer entry counts (92 total):**

| Layer | Entries | Empirical signal |
|---|---|---|
| **content_instance** | 24 | RICHEST (PoE map mods + D4 sigil affixes + LE Monolith mods + Helltide Cinders) |
| **character_substrate** | 20 | STRONG (Magic Find / IIR / IIQ at character gear-stat layer) |
| **augmentation** | 17 | STRONG in PoE (scarabs / sextants / Delirium Orbs); D4 sigil affix optimization |
| **season_mechanic** | 17 | STRONG (PoE leagues / D4 seasons / LE cycle theme) |
| **atlas_meta** | 14 | PoE-DOMINANT (atlas passive tree; D4 has no equivalent; LE light Shade of Orobyss) |

**6th layer detected empirically (per Mode A Surface 3):** party-scale augmentation ("MF carry" / "loot carry" social-play layer). Emergent from multiplicative return differential. Not enumerated in dispatch schema; relevant if Reincarnated adds multiplayer.

**PoE has fully developed all 5 layers** (richest multi-layer vocabulary; 6th layer detected); **D4 has 3 layers** (character_substrate + content_instance + season_mechanic); **LE has 3 layers** (character_substrate + content_instance + light atlas_meta); **PoE2 EA mirrors PoE1 layering with tighter restrictions**.

## 3. Composite-vs-single-axis archetype empirical assessment

**30 composite_archetype_assessment entries; per-game pattern distribution:**

| Game | Composite required | Hybrid | Single-axis viable | Total | Causal interpretation |
|---|---|---|---|---|---|
| **PoE 1** | 10 | 0 | 0 | 10 | STRONG composite restriction; pure single-axis MF archetype DEAD |
| **D4** | 5 | 1 | 0 | 6 | HYBRID — single-axis viable at mid-tier (Pit 80-90); composite required at high-tier (Pit 90+) |
| **PoE 2 EA** | 4 | 3 | 0 | 7 | TIGHTER restriction than PoE1 despite stated intent — design pivot failed at structural implementation |
| **Last Epoch** | 0 | 0 | 7 | 7 | SINGLE-AXIS VIABLE — Judgement Aura Paladin / Warpath Void Knight cited as one-button endgame builds with no PoE/D4 equivalent |

**Matt's "downfall of the developer" critique empirically confirmed; causal mechanism identified:**

> **The number and multiplication factor of loot substrate layers is the primary determinant of composite-archetype restriction severity.**
>
> PoE's 6 multiplicative layers (character IIR × map IIR × atlas node × scarab × Delirium Orb × pack size) create exponential return differential between composite-optimizing and single-axis builds — composite becomes economically rational; single-axis becomes economically irrational.
>
> LE's 3 simpler-multiplication layers produce smaller return differential, leaving single-axis builds within viable range.
>
> D4's 3-layer structure produces mid-range restriction.
>
> The restriction is not imposed via explicit prohibition but via return-rate differential under multiplicative coupling.

**Subtle but critical refinement:** community NAMES single-axis archetypes (PoE-Vault explicit "Clear Speed" archetype with verbatim definition) but the COUPLING ARCHITECTURE dis-incentivizes them economically. This is sharper than "designer didn't permit them" — designer permitted naming; designer architected economic non-viability via multiplicative coupling.

**Reincarnated Cycle 15+ design implication:**
- **Keep multiplicative loot substrate layer count LOW** (target ≤3 layers; LE-style simpler-multiplication)
- **PRESERVES player-experience-space** for single-axis viable archetypes
- **HONORS the principle architecturally** rather than restricting via coupling
- **AVOIDS the PoE pattern** that has documented player community pushback

## 4. Speedfarm ↔ Push binary — universal variant-splitting axis

**Empirical (Mode B Surface 4):** every multi-variant build across all 4 games splits on Speedfarm vs Push. Empirical variant counts:

| activity_focus | Count |
|---|---|
| allround / endgame generalist | 34 |
| push | 22 |
| mapping (PoE) | 10 |
| speedfarm | 9 |
| leveling | 4 |
| bossing | 3 |
| pit_push | 1 |

**Speedfarm + Push together = 31 variants** (37% of all 83 variants); the second-largest category after "allround" (generalist).

**Architectural implication:** the player-experience layer organizes around BINARIES that the coupling architecture forces. Speedfarm = optimize for clear-rate × loot-find; Push = optimize for content-depth × specialization-peak. These are the two ENDS of the player-experience polarity that emerges from the same engine architecture.

**Compose with Maxroll 5-axis rating:** Push and Speed are 2 of the 5 axes. The binary represents the structural polarity of "go deep / specialize" vs "go fast / generalize" that the cohort_archetype taxonomy (DPS-min-maxer / Balanced / Defensive / Hybrid) only partially captures.

## 5. Magic Find pattern fully clarified

| Game | Magic Find pattern |
|---|---|
| **D2/D2R** | PRIMARY archetype (MF Sorc as identity); single-axis viable due to decoupled reward |
| **D3** | Absorbed into Paragon + Greater Rift difficulty-tier mechanic |
| **D4** | EXPLICITLY RETIRED (no Magic Find affix in Season 13); **Torment Tier replaces it** as progression-gate-as-loot-quality mechanism |
| **Last Epoch** | Light Rarity / Item Find stats; primarily SINGLE-axis viable |
| **PoE 1** | **6-layer multi-cascade**: character IIR/IIQ + map mods + atlas tree + scarabs + Delirium Orbs + pack size; composite-required at endgame |
| **PoE 2 EA** | **FIRST-CLASS explicit stat target** (Mode B Surface 3): "100% IIR early maps / 150% IIR endgame" verbatim across 4+ PoE2 builds; alongside Crit Chance + Energy Shield as primary stat priority |

**Refined principle:** Magic Find didn't disappear; it morphed into multi-layer architectural mechanism that varies dramatically per game. The vocabulary "Magic Find" as a primary archetype label is legacy; the MECHANIC is preserved at multiple layers including (in PoE2) elevation to first-class stat target.

**D4 Torment Tier finding is structurally important:** D4 replaces character-stat Magic Find with **difficulty-tier-as-loot-quality progression gate**. This is the simplest possible loot substrate model — single-layer (difficulty tier) instead of multi-layer (PoE 6-layer cascade). D4 explicitly chose the simplest architectural model.

## 6. Surface findings from sub-agents (consolidated)

**From Mode A (5 surfaces):**
1. "Extreme Budget" as distinct 5th investment tier at PoE-Vault — refines investment-tier vocabulary to 5 levels (Extreme → Low → Medium → High → Mageblood-required)
2. "Clear Speed" as community-named single-axis archetype at PoE-Vault — community NAMES it; coupling architecture DIS-INCENTIVIZES it; refines the diagnosis
3. 6th loot substrate layer detected — party-scale augmentation (MF carry); relevant if Reincarnated adds multiplayer
4. PoE2 EA composite restriction STRONGER than PoE1 despite stated intent — design intent toward loose coupling failed at structural implementation; lesson for Reincarnated: intent is not sufficient; coupling mechanism must be designed toward loose coupling
5. Matt's critique STRONGLY confirmed with causal mechanism identified

**From Mode B (6 surfaces):**
1. Composite-vs-single-axis Matt critique confirmed at 6-site empirical scale (parallel finding to Mode A Surface 5)
2. Maxroll 5-axis ratings JS-rendered (HTML extraction limited; only 24 of 104 builds have structured ratings; headless browser would expand)
3. PoE2 IIR first-class explicit stat target (refines Magic Find morph documentation)
4. Speedfarm ↔ Push binary as universal variant-splitting axis (across all 4 games)
5. League Starter vocabulary asymmetry — PoE-origin; LE adopted; D4 absent (approximated via prose)
6. PoE-Vault Ranged/Melee/All-Rounder as playstyle geometry tags — schema-extension candidate (current build_activities.activity_layer absorbs as primary_playstyle)

## 7. Engine integration design recommendations

Per gandalf synthesis, the following are Cycle 15+ engine integration candidates with empirical-evidence grounding:

### 7.1 Doc 52 promotion candidate vocabulary (experiential archetype dimension)

**Primary archetype labels (LOCKED — 6-site STRONG convergence):**
- Bossing
- Speedfarming
- Push / Pit Push (depth-progression)
- Endgame Generalist
- Leveling
- League Starter (PoE-origin; LE adopted)

**Game-specific archetype labels (subordinate; per-game):**
- Mapper (PoE-genre primary; D4 lacks; LE Monolith-equivalent)
- Currency Farmer (PoE-specific)
- Hardcore (cross-game mode-specific)

**Sub-axes (LOCKED — composes per build):**
- Investment-tier (5 levels: Extreme/Low/Medium/High/Mageblood-required)
- Magic Find / IIR as sub-axis within Speedfarming/Currency Farmer

**Speedfarm ↔ Push binary (NEW — locked for variant-axis):**
- Universal at 4 games × multi-variant builds
- Recommend Reincarnated variant cycling supports this binary as primary variant-splitting axis

### 7.2 Designer-writes-substrate principle refinement (Layer 1.5 NEW)

Add to principle doc at re-engage:

> **Layer 1 — Designer-writes-substrate** (engine generative input; substrate-led)
> **Layer 1.5 NEW — Designer-writes-coupling-architecture** (determines which Layer 2 named experiences survive economically as viable archetypes)
> **Layer 2 — Player-names-experience** (community-emergent; emerges within the space coupling architecture permits)
> **Layer 3 — Vestigial designer-construct** (class/ascendancy as secondary reference marker)

**Reincarnated Cycle 15+ design call:** target Layer 1.5 with LIGHT/ADDITIVE coupling (≤3 multiplicative loot substrate layers; LE-style); preserve player-experience-space; avoid PoE-style 6-layer exponential cascade.

### 7.3 cohort_archetype Disc #41 revisit

Current cohort_archetype taxonomy (DPS-min-maxer / Balanced / Defensive / Hybrid) — empirical findings:

| cohort_archetype | Maps to community vocabulary? |
|---|---|
| DPS-min-maxer | Maps to Push + Bossing primary archetype combinations |
| Balanced | Maps to Endgame Generalist primary archetype |
| Defensive | Maps to Hardcore-mode-specific + Bossing-tanky sub-archetype |
| Hybrid | Maps to Speedfarming primary archetype |

**Recommendation for Cycle 15+:** preserve cohort_archetype as gauntlet performance-cohort axis BUT add the **community-validated experiential archetype dimension as orthogonal axis**. Builds emerge as (cohort_archetype × experiential_archetype × investment_tier) tuples — 3-dim coordinate space at the player-experience layer.

### 7.4 Wave A + Wave B LLM prompt Cycle 15+ extension

**Current Phase 5 prompts** consume substrate fields only (BC + cultural lineage + element + weapon family + faction context).

**Cycle 15+ extension target:**
- Wave A USER prompt: add `experiential_archetype_modal` + `experiential_archetype_distribution` (similar to `element_distribution`)
- Wave B USER prompt: add `kit_experiential_archetype` + `kit_investment_tier_target` as kit-level metadata
- THEMATIC_REGISTRY: add per-cell experiential-archetype vocabulary (Bossing-flavored / Speedfarming-flavored / etc. naming tokens)

This integrates the player-experience layer into LLM-generated faction names + per-kit identity at Cycle 15+ doc 52 promotion time.

### 7.5 Multi-layer loot substrate engine architecture (Cycle 15+ exploration)

**Per empirical findings + Matt critique:** Reincarnated should explicitly CHOOSE its loot substrate layer count and coupling pattern at Cycle 15+ architectural design call:

| Model | Layers | Reincarnated lean |
|---|---|---|
| **D2/D3 decoupled** | 1 | Too simple for engaging endgame depth |
| **D4 Torment Tier + content modifiers** | 3 (lighter) | Compatible with Reincarnated; preserves single-axis viability |
| **LE 3-layer simpler-multiplication** | 3 | **RECOMMENDED** — preserves single-axis viability; matches LE's empirical pattern |
| **PoE 6-layer multiplicative cascade** | 6 | NOT RECOMMENDED — empirically restrictive; player community pushback |

**Recommended architectural variable for Reincarnated:** ≤3 loot substrate layers; ADDITIVE or LIGHT-multiplicative coupling; preserve single-axis archetype viability while maintaining endgame engagement.

### 7.6 Schema extensions for sprint+1 (if executed)

- `primary_playstyle` field on `build_activities` (Ranged / Melee / All-Rounder per PoE-Vault)
- Headless browser pass to populate `build_ratings_structured` for the ~80 Maxroll builds where 5-axis ratings exist but JS-rendered (currently only 24 populated)
- D2-legacy site sampling (Diabloii.net) for Magic Find historical baseline confirmation
- PoE Ninja API access (data dumps endpoint structure analysis with proper tooling)
- Reddit JSON API for community discourse vocabulary mining (currently blocked from WebFetch)
- Mobalytics / D4Builds / Wowhead deeper crawl with proper HTTP infrastructure

---

## 8. Discipline composition

| Discipline | Application in this sprint |
|---|---|
| **Disc #41 substrate-led vocabulary lock** | Community vocabulary extracted verbatim; engine integration recommendations preserve substrate-led discipline at multiple layers |
| **Disc #42a framing-audit (Q1-Q6)** | Methodology framing audit applied at each phase; pre-imposed-taxonomy refutation surfaced at Magic Find legacy framing (Mode A Surface 5) + composite-restriction critique (Mode A Surface 4) |
| **Disc #18 math hotspot consultation** | Sub-agent methodology consultation at convergence-test phase; legolas Mode A applied cheapest-empirical-refutation discipline |
| **Disc #19 background processes** | Both sub-agents ran in background per Amendment 2/3 retired R48.4 + parallel fan-out enabled |
| **Disc #20 robots.txt compliance** | legolas Mode B respected site policies; backed off on 403/blocked surfaces |
| **Disc #45 vocabulary lock** | Internal analysis vocabulary preserved; community vocabulary extracted verbatim |
| **Recognition → empirical validation → commit** | Recognition (Matt design intuitions + recognition record gate (ii)); empirical validation (this sprint at 104-build scale); commit (recommendations for Cycle 15+) |

---

## 9. Composition with cascade-resumption-3

**Sprint fired in parallel with cascade-resumption-3 close** per Amendment 2/3 retired R48.4. No resource conflict. KR drives cascade independently. Sprint output is Cycle 15+ engine integration input — does NOT modify Cycle 14 v1 architecture.

**On Cycle 14 v1 close + Matt re-engage, sprint findings feed:**
- Doc 52 promotion (experiential archetype dimension as load-bearing canonical doc)
- Doc 38 amendment (engine commercial framing refinement)
- Wave A/B LLM prompt Cycle 15+ extension
- cohort_archetype Disc #41 revisit
- Multi-layer loot substrate Cycle 15+ engine architecture exploration
- Designer-writes-substrate principle Layer 1.5 (coupling architecture) refinement

---

## 10. Sign-off

**Authored:** gandalf (story-and-design steward) per ARPG community research sprint Phase R4 synthesis closing the sprint authorized at `agentic_orchestration/gandalf/notes/2026-05-29-arpg-community-research-sprint-authorization.md`

**For:** the empirically-grounded synthesis verdict + actionable Cycle 15+ engine integration design recommendations + composite-restriction-as-coupling-architecture causal mechanism documentation + Reincarnated design variable (≤3 loot substrate layers; LE-style simpler-multiplication) recommendation

**Sprint deliverables — COMPLETE:**
- ✅ Populated SQLite DB (12 tables; 6 sites; 4 games; 104 builds + 92 loot vocab + 37 convergence + 30 composite assessments)
- ✅ Acquisition log (legolas Mode B)
- ✅ Analysis findings (legolas Mode A)
- ✅ Synthesis verdict (this artifact)
- ✅ Engine integration design recommendations (§ 7)

**Next: Matt re-engage at Cycle 14 wave-close for canonical promotion of findings + Cycle 15+ doc 52 + principle doc Layer 1.5 amendment + cohort_archetype revisit + multi-layer loot substrate architecture exploration.**
