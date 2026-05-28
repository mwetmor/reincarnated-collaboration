# C-Hybrid Cell-and-Curation Architecture — Design Call Synthesis

> **STATUS:** CURRENT (load-bearing as of 2026-05-28) — Captures the 3-Layer + Cosmetic Surface architecture, autonomy × focus + gear-orientation experiential matrix, anti-cannibalization disciplines, 6-pattern skill point investment framework, Layer 2-derived → cosmetic semantic pathway, and Discipline #48 candidate proposal. Synthesizes ~13 design-dialog refinements from Cycle 14 close. Locks architectural direction for Cycle 14 v1 MVP + Cycle 15+ deferred implementation.

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward) — Matt + gandalf Pattern-B design call
**Status:** ACTIVE — design dialog closed; canonical commitments locked; Cycle 14 v1 MVP scope confirmed; Cycle 15+ deferred items enumerated
**Authority:** Matt 2026-05-28 — Pattern-B design call across ~13 refinements; each refinement caught architectural drift before commit; integrated W-α7+ scope ratified

**Companion docs:**
- `canonical/29-design-overview.md` (strategic anchor)
- `canonical/37-form-bias-diagnosis-and-recovery.md` (form-bias / no-classes precedent)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (post-no-classes redactions; per-kit chain count)
- `canonical/48-cycle-14-class-roster-2026-05-27.md` (VESTIGIAL — preserved-for-comparison class roster)
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (player-surface design; Loadout vs Sample)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 v1 BC-target intent; 22-cell roster; substrate-led skew)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system STR/INT/WIS/DEX)
- `canonical/story/skill-system-2026-05-24.md` (skill composition + T4 alteration)
- `canonical/story/no-classes-architectural-recommitment-2026-05-27.md` (companion; class concept retirement)
- `canonical/story/seasonal-hero-h-5-hybrid-spec-2026-05-27.md` (seasonal hero selection)
- `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` (D6 pre-locked success criteria)
- `canonical/story/phase-7-2-layer-joint-gate-spec-2026-05-27.md` (Phase 7 gate architecture)
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (Phase 5 cohesion judge)
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (Wave A / Wave B / F-C prompt architecture)
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` (no-classes recommitment record)
- `agentic_orchestration/gandalf/notes/2026-05-28-scaffold-drift-case-7-cell-label-class-leak-verdict.md` (case 7 R5-Plus scope)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#41-#47; #48 candidate)

---

## 0. TL;DR

The Cycle 14 design call surfaced and refined a substantial architectural framework. ~13 design refinements caught architectural drift before commit. Captured commitments:

| Layer | Locked |
|---|---|
| **Architecture** | 3-Layer + Cosmetic Surface: BC coordinate space (Layer 1) + per-kit kit-design (Layer 2-base) + derived experiential dimensions (Layer 2-derived) + cosmetic surface (LLM names/lore; minimal gameplay impact in story-light design) |
| **C-Hybrid curation** | Season-of-seasons generation → algorithmic overlap analysis → as-is + conglomerate kit selection → gauntlet re-validation → faction-pair pre-design on full pool → seasonal partitioning |
| **Experiential differentiator** | Autonomy × focus + gear-orientation matrix as load-bearing experiential dimension in story-light design |
| **Cosmetic semantic pathway** | Layer 2-derived experiential positions feed into LLM cosmetic naming as semantic inputs (pirate-faction sub-cluster emergence from loot+movement positions) |
| **Anti-cannibalization** | Strict cell-coverage non-overlap + Collection immutability + Thematic distinctness at cell-authoring |
| **Skill point investment** | 6-pattern framework (active damage scaling / passive effect scaling / threshold unlocks / QoL modifiers / synergy bonuses / resource economy modifiers); Patterns 1+2 Cycle 14 MVP; Patterns 3-6 canonical-locked for Cycle 15+ |
| **Algorithmic discipline** | Algorithmic primary + designer-oversight-bounded; designer time ~10-15× reduced from manual-curation alternative |
| **Discipline #48 candidate** | Architectural Scope Completeness Audit (pre-ratification surface-completeness check; catches scope gaps before architectural commits) |
| **Cycle 15+ deferred** | Substrate-signal research for Layer 1 BC axis expansion + Pattern 3-6 detailed implementation + C-Hybrid algorithm implementation + spirit guide marginal value pass + LLM naming refinement |

Genre positioning: **mechanically-focused ARPG (D2/D3/PoE lineage) + gacha-influenced collection accumulation (Court of Forms) + autonomy × focus matrix as experiential differentiator + story-light: cosmetic surface for collection density without narrative-coupling commitment.**

This is the canonical architecture for Cycle 14 v1 + Cycle 15+ evolution.

---

## 1. The 3-Layer + Cosmetic Surface Architecture

### 1.1 Layer 1 — BC coordinate space (substrate-derivable mechanical identity)

**Current state:** 5 axes per `canonical/story/v1-bc-target-intent-2026-05-24.md`:
- range (melee / medium / ranged)
- tempo (low / med / high)
- amplitude (spiky / variable / flat)
- attribute (STR / DEX / INT / WIS)
- proxy-density (none / light / heavy)

Total coordinate space: 3 × 3 × 3 × 4 × 3 = **324 cells**. v1 covers ~22-25 cells (~7%). v1 cell roster author-curated, substrate-informed.

**Candidate expansion via substrate-signal research (Cycle 16+; Discipline #18 territory):**

Additional axes the substrate may have signal for:

| Candidate axis | Sub-dimensions | Substrate signal source |
|---|---|---|
| `target_breadth` | single / cleave / aoe | Weapon shape (sweep vs thrust) |
| `damage_application` | DoT / direct / hybrid | Weapon-form (bleed/poison-DoT vs blunt-impact vs spell-burn) |
| `initiative_direction` | reactive / hybrid / proactive | Weapon-form (parry-daggers vs throwing-weapons) |
| `trait_family / lineage_cultural_emphasis` | Cultural-tradition mechanical biases | Lineage data (samurai vs ancestor-spirits vs pyromantic) |
| `supporting_theme` | Cluster cohesion + thematic coupling | Phase 5 PM-1 cluster emergence (partial capture exists) |

Expansion from 5 → 8-10 BC axes is meaningful architectural commit; coordinate space grows from 324 → ~2916+ cells; each cell more specialized. Cycle 16+ design call territory with legolas Mode A consultation per Discipline #18.

### 1.2 Layer 2-base — Per-kit kit-design (mechanical choices)

Non-substrate-derivable mechanical inputs that vary within a BC envelope:

- Skill composition (which skills selected from cell's available pool; chain layout)
- Resource model (cooldown-based / mana-based / hybrid)
- Trait pool emphasis (intrinsic pool composition; rank-stacking choices)
- Gear-affix distribution (element/mechanic-gated affixes; rolls per kit instance)

### 1.3 Layer 2-derived — Experiential dimensions (computed from Layer 1 + 2-base)

Properties that EMERGE from BC anchor + kit-design choices; computable from existing engine output:

| Layer 2-derived axis | What varies | Source data |
|---|---|---|
| **Autonomy (gear-independence)** | % of effective performance from skills+traits vs gear-specific modifiers; high autonomy = gear-choice freedom (MF / Movement / Burst / Defensive); low autonomy = build-defined gear-locked | Run kit through gauntlet with N gear loadouts; measure performance variance |
| **Focus intensity** | Resource-management complexity + cooldown-rotation density + reactive-demand frequency + combo-buildup requirements; spans chill set-and-forget through tight-rotation high-APM | Resource count + interaction complexity; cooldown CV / optimal-window-size; reactive-event rate per minute; stack max-required |
| **Combat tempo** | Sustain ratio (regen vs cost); burst availability; cycle frequency | Resource economy parameters; skill cooldown distribution |
| **Play-pattern emergence** | Reactive/proactive; target-breadth (single/AoE); telegraph dependency | Gauntlet sim telemetry; skill mechanic metadata |

**These are derived, not stored separately as axes.** Computed at scoring/curation time from existing engine output. No new instrumentation needed.

### 1.4 Cosmetic Surface (minimal gameplay impact in story-light design)

Story-light recognition (Matt 2026-05-28): without extensive narrative coupling, the following elements are COSMETIC rather than experiential at gameplay layer:

- LLM-generated theme + name (Phase 5 Wave A faction names + Wave B per-kit names)
- Named-personage allocation rarity tag (Sketch F)
- Faction-cluster lore text + relationship narrative (F-C)
- Seasonal element flavor naming (element mechanics are Layer 1; element NAMES are cosmetic)

**Gameplay-relevant vs cosmetic distinction:**
- Gameplay-relevant: Layer 1 + Layer 2-base + Layer 2-derived (mechanical experience)
- Cosmetic: cosmetic surface (Court collection flavor, UI polish)

---

## 2. C-Hybrid Curation Framework

### 2.1 Five-stage workflow

| Stage | Owner | Description |
|---|---|---|
| **1. Generation phase** | Engine (per Strategy A seasonal rotation) | Run N seasons of generation; each season produces 18-50 kit instances |
| **2. Overlap analysis** | Algorithmic + designer review | Analyze cross-season kit population for patterns, redundancies, emergent themes, gaps |
| **3. Curation** | Algorithmic primary; designer review at threshold | Select year-of-content kit pool: as-is BC-hero kits + conglomerate kits; per-BC multiplicity decision via algorithmic distinctness scoring |
| **4. Gauntlet re-validation** | Gauntlet sim | Full curated pool runs through gauntlet; balance + viability verified before shipping |
| **5. Faction-pair + seasonal partitioning** | Algorithmic G-B + LLM F-C | G-B substrate-distance + F-C inter-faction LLM fires on full year-of-content pool; partitioning into seasonal releases |

### 2.2 Within-BC multiplicity rule

**Multiple distinct kits at the same BC coordinate ARE allowed when experientially distinct.** This is fundamentally different from Strategy D within-cell tree expansion (which would re-create class taxonomy):

- WRONG (Strategy D within-cell tree expansion): one kit at a cell gets MORE skill chains over time → cell becomes generalist "Magician" → no-classes violation by accumulation
- RIGHT (C-Hybrid within-BC kit multiplicity): multiple DISTINCT kits share a BC coordinate; each retains specialized identity; gated by experiential distinctness scoring

3-kit max per BC coordinate. Each must be EXPERIENTIALLY DISTINCT (algorithmic distinctness score above threshold).

### 2.3 Distinctness scoring (within-BC mechanical multiplicity)

Score composite distance on Layer 2-base + Layer 2-derived. **Layer 1 is shared by definition for same-BC kits; cosmetic surface alone does NOT count toward mechanical multiplicity.**

Two kits at same BC + same Layer 2-base + different cosmetic surface = SKIN VARIANTS, not mechanically distinct kits. The 3-kit-per-BC max applies to mechanically-distinct kits (Layer 2-distinct).

Composite distance formula authored at Cycle 15+ legolas Mode A consultation per Discipline #18 hotspot.

### 2.4 Cross-BC cell distinctness

When deciding whether to author a NEW cell at a NEW BC coordinate (Strategy A-revised audit cycle):

- PRIMARY: BC coordinate distance metric (Layer 1 distance)
- SECONDARY: Layer 2-derived + non-Layer-1 tiebreakers

### 2.5 Algorithmic discipline (primary operating mode)

Per-axis distinctness vectors computed from existing engine output (gauntlet sim telemetry + Phase 5 LLM outputs + per-kit metadata). Composite scoring on Layer 2-base + Layer 2-derived dimensions. Greedy max-coverage selection per BC coordinate (≤3 mechanically + experientially distinct kits).

**Designer oversight (BOUNDED):**

- ONE-TIME: metric formulation + weight calibration (~1-2 days; Cycle 15+ legolas Mode A consultation per Discipline #18)
- PER-RELEASE: edge-case review + release approval (~1 day max; NOT routine curation)
- PERIODIC: drift audit every N releases (~half day)

Designer time per release ~10-15× reduced from manual-curation alternative.

---

## 3. Autonomy × Focus + Gear-Orientation Matrix

### 3.1 The matrix as experiential differentiator

In story-light design, the autonomy × focus + gear-orientation matrix is the **load-bearing experiential differentiator**. It compensates for the absence of narrative variance by providing meaningful player-experiential variance.

Three matrix dimensions:

- **Autonomy spectrum**: high autonomy = gear-choice freedom (MF / Move / Burst / Defensive); low autonomy = build-defined gear-locked
- **Focus spectrum**: high focus = engaged APM (tight rotations, reactive demands); low focus = chill set-and-forget
- **Gear-orientation**: which gear-affix profile the kit optimizes against (loot-focused / speed-running / boss-killing / multi-encounter)

### 3.2 Within-BC kit multiplicity via matrix positions

Example: AOE Fire Mage cell could host three mechanically distinct kits at different matrix positions:

| Kit variant | Autonomy | Focus | Gear-orientation |
|---|---|---|---|
| **Chill MF burner** | High | Low | Loot-focused |
| **Engaged burst rotation** | Low | High | Boss-killing |
| **Balanced midfield** | Medium | Medium | Multi-encounter |

Three DIFFERENT EXPERIENTIAL KITS at the same BC coordinate. Player chooses based on mood/goal. Three-kit-per-BC max maps cleanly to autonomy × focus combinations.

### 3.3 The directive (Matt 2026-05-28 verbatim)

> "Some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses."

This is the bounded-viability-with-specialization design directive. The autonomy × focus + gear-orientation matrix operationalizes it.

**Empirical evidence requirement:** Path α delivered cross-path DPS parity at 1.24× (target ≤1.5×) at calibrated character profile. Per-encounter-type bounded-viability (T2 + T4 BVV harness targets) verified at Option B (now integrated into W-α7+ scope). Multi-investment-profile verification (W-α7+ scope) verifies the directive holds across player investment choices.

### 3.4 Genre framing

Mechanically-focused ARPG (D2/D3/PoE lineage) + gacha-influenced collection accumulation (Court of Forms; per `project_earth_meta_layer.md`) + autonomy × focus matrix as experiential differentiator + story-light: cosmetic surface for collection density without narrative-coupling commitment.

This is a distinct genre position. Most gacha games lean heavy on story for retention; most ARPGs (D2/D3) skip story for gameplay. Reincarnated is mechanical-ARPG + light-gacha-collection. The cosmetic layer provides accumulation distinctness without committing to story development.

---

## 4. Layer 2-Derived → Cosmetic Layer Semantic Pathway

### 4.1 The composition

The mechanical Layer 2-derived dimensions feed into LLM cosmetic naming as semantic inputs, producing thematically coherent kit naming + faction sub-clusters that emerge from mechanical reality rather than from author-imposed taxonomy.

```
Mechanical layer (Layer 1 + Layer 2-base + Layer 2-derived)
    │
    │  feeds into ↓
    │
LLM cosmetic layer (Phase 5 Wave A + Wave B + F-C)
    │
    │  produces ↓
    │
Thematic naming + faction sub-clusters per autonomy × focus position
```

### 4.2 Position-to-thematic mapping examples (illustrative)

| Autonomy × Focus position | Gear-orientation | Likely thematic cluster |
|---|---|---|
| High autonomy + low focus + loot-focused | MF gear flexibility | **Pirate / treasure-hunter / freebooter / scoundrel** family |
| High autonomy + low focus + movement-focused | Speed gear flexibility | **Wanderer / outrider / vagabond** family |
| High autonomy + low focus + COMBINED loot+movement | MF + speed flexibility | **Pirate captain / sky-corsair / raider** sub-faction (combinatorial) |
| High autonomy + high focus + speed-focused | Speed-focused engaged play | **Blitz / vanguard / lightning-strike** family |
| Low autonomy + high focus + boss-killing | Boss-gear specialist | **Artisan-of-war / focused-strike / dueling-master** family |
| Mid autonomy + mid focus + balanced | Flexible | **Journeyman / wanderer / errant** family |
| High autonomy + high focus + multi-encounter | All-purpose engaged | **Champion / paragon / virtuoso** family |

These thematic clusters aren't gandalf-imposed — they're EMERGENT from the autonomy × focus + gear-orientation positions kits occupy. The LLM naming + faction-sub-cluster naming take these positions as semantic prompts.

### 4.3 Sub-faction emergence

Within a Phase 5 cluster faction, kits that share autonomy × focus + gear-orientation positions form natural sub-faction clusters. This permits cluster-faction breadth (e.g., "Coastal Confederation") with internal sub-faction diversity (e.g., "Stormrunner Pirates" + "Merchant Patrol" + "Beachhead Defenders" all within one faction).

### 4.4 Algorithm implementation

1. Compute per-kit autonomy + focus + gear-orientation vectors from gauntlet sim telemetry
2. Within each Phase 5 cluster, sub-cluster by autonomy × focus position
3. Pass sub-cluster identity as semantic input to LLM naming prompts
4. LLM Wave A names faction with cohesive theme; Wave B names kits with sub-faction-consistent identity
5. F-C generates inter-faction relationships informed by sub-faction thematic positions

### 4.5 Story-emergence-from-mechanics principle

Story-light design relies on this pathway. The "narrative" emerges from mechanical-to-semantic mapping; the player perceives thematic coherence across the Court through this composition, not through authored narrative content.

Cross-season thematic recurrence: same autonomy × focus position across seasons can produce thematically resonant kits (multiple seasons of "pirate"-themed forms accumulating in the Court).

---

## 5. Anti-Cannibalization Disciplines

### 5.1 Three disciplines preserving Court value monotonicity

The Court of Forms accumulates spirits across seasons. To ensure collection value grows rather than diminishes, three architectural disciplines apply:

### 5.2 Discipline 1 — Strict cell-coverage non-overlap

Audit cycles author new cells only at UNCOVERED BC coordinate regions. Existing cells remain authoritative for their coordinate regions. The engine's emergent variance discovery is constrained: it can only suggest cells for regions not yet covered.

The 324-cell BC coordinate space has ~90%+ headroom (v1 covers ~7%). Ample room for genuinely new specialized cells without overlapping existing ones.

Within-cell variance discoveries do NOT become "refinements" of existing cells. Within-cell variance lives at per-kit instance layer (Layer 2-base + Layer 2-derived), not at canonical chain layer.

### 5.3 Discipline 2 — Collection immutability

Collected spirits in the Court are snapshots at collection time. Engine evolution doesn't modify or invalidate past collections.

A spirit collected in S1 always exists in the Court as she was when collected — her skills, gear, traits, lore are frozen at that moment. Later engine state changes (audit cycles, substrate evolution, new cells, balance updates) don't reach backward into the Court.

This is how Genshin, Honkai, FGO handle collected characters. The collection is the player's persistent achievement; the live game can evolve without depreciating past collection effort.

### 5.4 Discipline 3 — Thematic distinctness requirement at cell-authoring

Each new cell must have clear thematic differentiation from all existing cells, not just BC-coordinate differentiation.

Audit cycle adding a new cell at a slightly different BC coordinate from an existing cell — REJECTED if thematic space overlaps too much. The audit discipline asks: "is this a genuinely distinct identity that a player would experience as different, or just a BC coordinate refinement of an existing identity?"

Genre precedent: Diablo III's 7 classes are each thematically distinct. Final Fantasy XIV's White Mage and Scholar are both healers but mechanically distinct (regen-and-shield vs fairy-pet-and-burst). Both exist because they're experienced differently, not because they're at different stat-coordinates.

### 5.5 Court value accrues monotonically under these disciplines

Numerical accumulation under steady cadence:
- ~50 cells × ~10 seasons × ~1.5 forms per cell (instance variance) = ~750 distinct collectible spirits
- Of those, ~240 carry named-personage allocation (Sketch F ~32%)
- Each carries unique LLM-derived identity (cluster faction + relationships + season theme + thematic naming per matrix position)
- All preserved via collection immutability

Gacha-tier accumulation density. Each new spirit ADDS to value without diminishing any prior spirit.

---

## 6. Skill Point Investment — 6-Pattern Framework

### 6.1 The framework

Skill point investment enables player-agency within the kit's substrate-anchored identity. Six pattern types compose:

| Pattern | Description | Genre lineage |
|---|---|---|
| **Pattern 1** | Active skill nodes: scale damage / add effects per point invested | D2 / D3 active skill scaling |
| **Pattern 2** | Passive skill nodes: scale multiplicative or additive effects per point invested | D2 / D3 passive scaling |
| **Pattern 3** | Threshold unlocks: discrete benefits at point thresholds (5pt / 10pt / 15pt tiers) | D2 synergy thresholds; D4 paragon glyph thresholds |
| **Pattern 4** | QoL modifiers: cooldown / cast / range / AoE radius / projectile count per point | PoE quality bonuses; D3 ancient affixes |
| **Pattern 5** | Synergy bonuses: cross-skill investment compounding ("+X% fire skill damage per point in this passive") | D2 synergies; PoE keystone-modifier chains |
| **Pattern 6** | Resource economy modifiers: scale cost / regen / cooldown | D2 mastery passives; PoE flask charges |

### 6.2 NODE_MAX investment limits

Per `reincarnated-loadout/src/data/cycle13Types.ts` and per-skill emitter architecture:

- **Passive nodes**: max 5 points
- **Active nodes**: max 15 points
- **T4 nodes**: max 1 point (binary)

### 6.3 Cycle 14 MVP scope (Patterns 1+2 implementation)

Per W-α7+ integrated scope (ratified 2026-05-28 Matt design call):

**In Cycle 14:**
- Pattern 1 (active skill damage scaling per point) implementation
- Pattern 2 (passive skill effect scaling per point) implementation
- Multi-investment-profile calibration (Path α parity verified at multiple investment levels, not just W-α3 fixed profile)
- BVV harness update for investment-profile coverage
- Wave 5 re-fire under MVP investment-aware architecture
- Per-encounter-type bands integrated (was Option B Gate-3 D2; integrated to avoid double calibration)
- BASE_DAMAGE_L50 value recalibration under integrated architecture

**Canonical-locked for Cycle 15+ deferred implementation:**
- Pattern 3 (threshold unlocks)
- Pattern 4 (QoL modifiers)
- Pattern 5 (synergy bonuses)
- Pattern 6 (resource economy modifiers)

### 6.4 Skill point investment as player-agency dial within autonomy × focus matrix

Skill point investment becomes the mechanism that LETS the player adjust their kit's experiential position within the matrix:

- Invest in Pattern 6 nodes → shifts toward HIGH AUTONOMY (kit becomes self-sustaining)
- Invest in Pattern 4 cooldown reduction → shifts toward LOW FOCUS (kit becomes sustained without tight rotation)
- Invest in Pattern 5 synergy bonuses → shifts toward HIGH FOCUS (more interactions to track)
- Invest in Pattern 3 threshold-unlock effects → adds AoE / pierce / chain → shifts gear-orientation flexibility

Same generated kit can occupy different matrix positions based on player investment choices. The Court of Forms accumulates KITS; player choice within each kit shapes its lived experiential position.

### 6.5 T4 system reconciliation (engine clarification per rocket 2026-05-28)

The engine has TWO T4 concepts with naming collision:

**Per-chain T4 capstone (per_skill_emitter.py):**
- Always passive-mode (cooldown 0.0; "passive enhancement")
- One per chain; 3 per kit total
- DAMAGE_MULTIPLIER[(4, role)] represents passive enhancement contribution

**T4 alteration (mechanic_alteration.py):**
- Kit-wide modifier (one per kit)
- Three manifestations: T4_active OR rank2_passive OR rank3_passive
- T4_active branch currently unreachable in production (placeholder for archetype signaling)

Parallel non-conflicting systems. Naming collision is artifact; not legacy drift. Future Cycle 15+ work may activate T4_active manifestation via archetype signaling.

---

## 7. Path α Architectural Recognition

### 7.1 Path α delivered and what became scaffold

**Path α delivered cross-path DPS parity at 1.24×** (target ≤1.5×) at fixed character profile. The structural root cause of 79× / 365× cross-path divergence (independent SC-6b + SC-7 calibration anchors) is architecturally resolved.

**Path α work status:**

| Path α work | Status |
|---|---|
| W-α1 Unified damage formula refactor | ✅ KEEP — architectural foundation |
| W-α2 KPM ceiling=None | ✅ KEEP — engine cleanup |
| W-α3 Phase 1 Unified calibration loop infrastructure | ✅ KEEP — reusable for multi-profile calibration |
| W-α4 BVV harness infrastructure | ⚠️ KEEP infrastructure; multi-profile updates required |
| W-α5 Jack-ryan canonical retirements + Discipline #47 | ✅ KEEP — durable; #47 first-firing was framework success |
| W-α3 Phase 2 Calibrated BASE_DAMAGE_L50 values | ❌ SCAFFOLD — superseded by integrated W-α7+ recalibration |
| scale_factor = 0.664063 | ❌ SCAFFOLD — recomputed under integrated calibration |
| 1.24× cross-path parity (empirical) | ⚠️ EMPIRICAL WAYPOINT — re-verified across multi-profile space |

### 7.2 The discipline recognition

Solving the symptom (cross-path divergence) and the root cause (missing investment scaling architecture) in parallel produces double calibration work + scaffold-drift risk surface at the seam.

The integrated W-α7+ scope reframe (ratified Matt 2026-05-28) handles both in single integrated pass:
- Investment scaling formula design + implementation
- Per-encounter-type bands (was Option B; now integrated)
- BASE_DAMAGE_L50 recalibration
- Multi-profile × multi-encounter-type calibration
- Single Wave 5 re-fire

Net: ~14-22 days Cycle 14 v1 close from W-α7+ ratification (vs ~16-25 days sequential approach).

### 7.3 Per-tier ratio preservation

The W-α3 Phase 2 calibration preserved per-tier ratios across recalibration:

| Tier transition | Multiplier (locked across calibration changes) |
|---|---|
| T1 → T2 | 1.5× |
| T1 → T3 | 2.17× |
| T1 → T4 | 4.0× |

Per-tier ratios encode skill-power-progression design intent. Likely to preserve across W-α7+ recalibration as well. Per-path ratio (physical:spell = 2.34× at base) likely stays close, compensating for downstream formula asymmetry.

Absolute base value magnitudes WILL shift under integrated W-α7+ recalibration to absorb investment scaling multipliers.

---

## 8. Algorithmic Discipline + Designer Oversight

### 8.1 Operational mode

**Algorithmic discipline (PRIMARY):**
- Per-axis vectors from existing engine output (gauntlet sim telemetry + Phase 5 LLM outputs + per-kit metadata)
- Composite scoring on Layer 2-base + Layer 2-derived dimensions
- Mechanical multiplicity threshold = Layer 2 variance ≥ τ_mechanical
- Greedy max-coverage selection per BC coordinate (≤3 mechanically distinct kits per coordinate)
- Cosmetic surface variance permitted on top of mechanical kits (skin variants for collection density)
- Algorithmic faction-pair (G-B substrate-distance) on full curated pool
- Algorithmic seasonal partitioning of curated pool

**Designer oversight (BOUNDED):**
- ONE-TIME: metric formulation + weight calibration (~1-2 days; Cycle 15+ legolas Mode A consultation per Discipline #18)
- PER-RELEASE: edge-case review + release approval (~1 day max; NOT routine curation)
- PERIODIC: drift audit every N releases (~half day)

### 8.2 The cost calculus

Designer time per release ~10-15× reduced from manual-curation alternative. ~1-2 days designer judgment per release becomes ~1 day max edge-case review + approval; specialization curation is algorithmic.

This preserves Matt's design directive without committing to recurring Matt-level scope creep.

### 8.3 Discipline #18 hotspot acknowledgment

Distinctness metric formulation is a math hotspot requiring legolas Mode A consultation for both within-BC and cross-BC metrics before production lock. Cycle 15+ design pass. Composes with the substrate-signal research for Layer 1 expansion.

---

## 9. Discipline #48 Candidate — Architectural Scope Completeness Audit

### 9.1 The upstream root cause recognition (Matt 2026-05-28)

The 13 architectural concerns caught in Cycle 14 design dialog share structural shape:

- Architectural commit was about to fire against incomplete scope documentation
- Matt's ad-hoc audit caught the gap
- Reframe under cleaner scope produced better architecture

The framework caught these AT THE DESIGN DIALOG LAYER (framework working well), but COST was sustained design dialogue across many exchanges to surface scope completeness reactively.

**Upstream root cause:** no discipline that enforces scope-completeness audit BEFORE architectural commits.

### 9.2 Discipline #48 proposed framing

Before ratifying any architectural canonical doc OR major calibration/refactor dispatch, perform scope-completeness audit enumerating dependent mechanical surfaces with classification:

| Classification | Meaning | Action |
|---|---|---|
| **IN-SCOPE** | Covered explicitly by the doc/dispatch | None |
| **INTENTIONALLY OUT-OF-SCOPE** | Boundary explicitly documented; this work doesn't touch | None |
| **KNOWN-GAP** | Surface exists; not yet designed; flagged for future resolution | Explicit resolution path required before commit |
| **UNKNOWN** | Surface might exist but isn't enumerated | Resolve via legolas Mode A / rocket clarification before ratification; UNKNOWN blocks ratification |

### 9.3 Composition with existing disciplines

| Discipline | What it catches | When it fires |
|---|---|---|
| #18 | Methodology gaps at math hotspots | Pre-execution; methodology consultation |
| #39 | Scaffold-with-pending-decision | After scaffold exists; flag for retirement |
| #40 | Empirical surfacing of deferred design | When empirical signal lands |
| #42 | Load-bearing assumptions in framing | At sub-agent dispatch consumption |
| #44 | Framing-refusal authority | When sub-agent finds dispatch unworkable |
| #47 | BLOCK authority on design-target decisions | At Gate-X with design-affecting findings |
| **#48 (candidate)** | **Scope-completeness BEFORE architectural commit** | **Pre-ratification audit** |

#48 fires earlier than the others. Front-loads design rigor; saves mid-cycle scope-expansion penalty.

### 9.4 Path α counterfactual under #48

If Discipline #48 had been in place during Path α design call:

```
PATH α SCOPE-COMPLETENESS AUDIT (pre-ratification):

Dependent mechanical surfaces:
- BASE_DAMAGE_L50 calibration values: IN-SCOPE
- Cross-path damage formula unification: IN-SCOPE
- Per-tier damage ratios: IN-SCOPE (preserve from existing)
- Per-encounter-type gauntlet eligibility: KNOWN-GAP (Cycle 15 Option A
  deferred per Gate-3 D2; explicit deferral commitment)
- Skill point investment scaling: UNKNOWN — surface via rocket
  clarification before ratification
```

Rocket clarification fires; investment scaling gap surfaces; Path α design call EXPANDS scope to include investment scaling OR EXPLICITLY documents "Path α calibrates at no-investment-scaling profile; investment scaling architecture is Cycle 15+ work with explicit deferral commitment."

Either path is honest. The current path (calibrate at implicit fixed profile; discover gap mid-execution; reframe scope mid-cycle) is the most expensive path because it requires double-work.

### 9.5 Canonical capture path

Per Matt 2026-05-28 ratification (D2):
- Discipline #48 canonical write added to jack-ryan's batched canonical-write per D10 (joins #41-#46 + #47 batch)
- ~quarter day additional jack-ryan work
- Cycle 14 v1 ships with full discipline framework including #48
- Discipline #48 enforcement begins Cycle 15+

---

## 10. No-Classes Architecture Honored End-to-End

Per `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`:

- BC = substrate-anchored mechanical shape; not class taxonomy
- Kit = mechanical + experiential identity (Layer 1 + Layer 2-base + Layer 2-derived)
- Skin = cosmetic surface variant
- Multiplicity at BC by experiential distinctness, not class sub-trees

This architecture composes:
- Strategy D (within-cell tree expansion) explicitly REJECTED — would re-create class taxonomy by accumulation
- Within-BC kit multiplicity ONLY via experiential distinctness on Layer 2-base + Layer 2-derived
- Cell roster expansion via uncovered BC coordinate regions (Strategy A-revised)
- Cosmetic variance permits skin variants on top of mechanical kits
- Engine-as-research-partner + algorithmic-curation-partner composition

The no-classes recommitment is preserved through every architectural layer.

---

## 11. Engine-as-Research-Partner + Algorithmic-Curation-Partner

### 11.1 Division of labor

**Engine generates + validates + scores:**
- Per-season generation produces 18-50 kit instances per season (per Strategy A seasonal rotation)
- Phase 5 emergent clustering surfaces patterns
- Gauntlet sim validates mechanical viability + computes Layer 2-derived properties
- Phase 7 quality gates verify bounded-viability

**Algorithm curates by distinctness threshold:**
- Composite distinctness scoring on Layer 2-base + Layer 2-derived
- Greedy max-coverage selection per BC coordinate
- Algorithmic faction-pair on full curated pool
- Algorithmic seasonal partitioning

**Designer reviews edge cases + interprets patterns + approves releases:**
- ONE-TIME metric design (Cycle 15+ legolas-consulted; ~1-2 days)
- PER-RELEASE edge-case review + approval (~1 day max)
- PERIODIC drift audit (every N releases; ~half day)

### 11.2 Substrate-signal research as architectural feedback loop

What the engine surfaces informs Cycle 16+ BC axis expansion proposals. Substrate-derivable mechanical properties not yet in BC may be promoted to Layer 1 via systematic substrate-signal research (Discipline #18 territory; legolas Mode A consultation).

This positions the engine as a **generative-research partner** for design, not just a content factory. The engine's variance discovery becomes designer input; the designer's architectural decisions feed back into engine architecture.

---

## 12. Cycle 14 v1 MVP Scope + Cycle 15+ Deferred Items

### 12.1 Cycle 14 v1 MVP scope (lockable now)

Per W-α7+ integrated scope ratification:

| MVP item | Source |
|---|---|
| Path α architectural breakthrough (cross-path DPS parity at 1.24×) | Confirmed; values are SCAFFOLD pending integrated recalibration |
| 3-Layer architecture (Layer 1 + Layer 2-base + Layer 2-derived) | This doc § 1 |
| Cosmetic Surface (story-light recognition) | This doc § 1.4 |
| Patterns 1+2 skill point investment implementation | This doc § 6.3 |
| Per-encounter-type KPM bands (integrated with W-α7+) | Path α scope reframe |
| Multi-investment-profile calibration | W-α7+ scope |
| BVV harness update for investment-profile coverage | W-α7+ scope |
| Anti-cannibalization disciplines | This doc § 5 |
| No-classes architecture honored end-to-end | Companion no-classes recommitment |
| Disciplines #41-#48 canonical-batch | Jack-ryan canonical-write per D10 + D2 |
| C-Hybrid algorithmic discipline (architecture only) | This doc § 8 |

### 12.2 Cycle 15+ deferred items (canonical-locked)

| Deferred item | Cycle 15+ scope |
|---|---|
| Patterns 3-6 detailed implementation (threshold unlocks / QoL modifiers / synergy bonuses / resource economy modifiers) | Pattern-by-pattern design dialog + implementation |
| Substrate-signal research for Layer 1 BC axis expansion | Legolas Mode A consultation per Discipline #18 |
| C-Hybrid algorithm implementation (year-of-content curation pipeline) | Engine + algorithmic implementation |
| Spirit guide marginal value pass | Deferred from prior cycles |
| LLM naming refinement based on Cycle 14 v1 playtest feedback | Phase 5 evolution |
| T4_active manifestation activation (currently unreachable code) | Archetype signaling design |
| C-Hybrid distinctness metric formulation (composite distance formula) | Discipline #18 hotspot |
| Cross-BC cell distinctness metric formulation | Same hotspot |

### 12.3 Cycle 16+ deferred items (architecturally significant)

| Item | Notes |
|---|---|
| BC axis expansion proposal (5 → 8-10 axes) | Substrate-signal research outcome; major architectural commit |
| Investment scaling across all 6 patterns (full implementation) | Builds on Cycle 15 Pattern 3-6 deferred items |

---

## 13. Genre Positioning + Player Experience Properties

### 13.1 Mechanically-focused ARPG (D2/D3/PoE lineage)

Gameplay is the load-bearing experience. Player engagement comes from:
- Mechanical play-feel (Layer 1 + Layer 2-base base mechanics)
- Skill point investment + build choices (6-pattern framework)
- Gear-orientation flexibility (autonomy enables MF/Move/Burst/Defensive specialization)
- Focus intensity matching (player engagement spectrum)

### 13.2 Gacha-influenced collection accumulation (Court of Forms)

Court collection accumulates spirits across seasons. Genre-traditional gacha conventions:
- Collection immutability (snapshots at collection)
- Rarity tiers (named-personage allocation per Sketch F ~32%)
- Cosmetic variance per season
- Cross-season recurrence with thematic variation

### 13.3 Story-light design

No extensive narrative coupling. Story emerges from:
- Mechanical-to-semantic mapping (Layer 2-derived → cosmetic LLM naming)
- Sub-faction thematic emergence from autonomy × focus + gear-orientation positions
- Phase 5 LLM cohesion-judge faction narrative
- Substrate-anchored personage attribution (Sketch F)

No quest dialogue, NPC interactions, narrative arcs driving gameplay. Spirit Guide as voice-register companion (not story protagonist).

### 13.4 Player experience properties

| Property | How delivered |
|---|---|
| **Engagement choice** | Autonomy × focus matrix lets player match kit to mood/session |
| **Mechanical depth** | 6-pattern skill point investment + chain composition + trait pool + gear-affix |
| **Collection density** | ~750+ distinct spirits across ~50 cells × ~10 seasons under Layer 2-derived experiential differentiation + cosmetic variance |
| **Build crafting** | Within-BC multiplicity (≤3 kits per cell) + per-kit instance variation + skill point investment patterns |
| **Specialization niches** | Bounded viability floor + specialization peaks per kit (T2/T4 BVV targets) |
| **Player agency** | Skill point investment becomes the dial that adjusts kit position within autonomy × focus matrix |

This composes a distinct genre position: **mechanically-focused ARPG with gacha-influenced collection density, story-light architecture, and autonomy × focus matrix as load-bearing experiential differentiator.**

---

## 14. Pattern Observation — Discipline-of-Disciplines

Cycle 14 produced an unusual operational pattern: ~13 architectural concerns caught at design-dialog layer through Matt's careful pushback, each one refining the architecture toward something cleaner. The cumulative result is this canonical architecture.

The recognition of this pattern as ITSELF an architectural concern (the upstream root cause is insufficient documentation rigor) produced Discipline #48 candidate. The framework evolves to become better at preventing the catches it was designed to handle.

**This is a discipline-of-disciplines move**: the framework discipline catches issues reactively → recognize that pattern → propose pre-emptive discipline → framework becomes better at scope-completeness rigor.

Cycle 14 started with 8 disciplines; by close it has ~12+ disciplines plus this meta-discipline pattern. Each was forged in actual operational pressure during the cycle. None are theoretical.

---

## 15. Sign-off

**Status:** ACTIVE — design dialog closed; canonical commitments locked.

**Cycle 14 v1 close trajectory:** ~14-22 days from W-α7+ ratification (2026-05-28). Within Path α 4-6 week budget; at upper end of sustained-intensity threshold.

**Architectural integrity preserved through:**
- 3-Layer + Cosmetic Surface separation
- C-Hybrid curation workflow
- Anti-cannibalization disciplines
- Algorithmic primary + designer-oversight-bounded operational mode
- Story-light recognition (no narrative-coupling commitment)
- No-classes architecture honored end-to-end
- Discipline #48 candidate (scope-completeness audit pre-emptive)

**Subsystems composed:**
- Path α unified damage formula + multi-profile recalibration under W-α7+
- C-Hybrid curation framework
- Phase 5 LLM cosmetic layer (Wave A + Wave B + F-C)
- Earth Meta-Layer + Court of Forms collection accumulation
- Spirit Guide voice-register layer
- Gauntlet sim + Phase 7 quality gate

**For:** Cycle 14 v1 close ratification; Cycle 15+ entry design dialog reference; Cycle 16+ deferred items lockable now.

**Signed:** gandalf (story-and-design steward) — Matt + gandalf Pattern-B design call 2026-05-28
