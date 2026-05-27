# Block C Calibration Scaffolding — Math-Before-Code Handoff to Gamora

> **STATUS:** CURRENT — design-spec-as-math handoff per Discipline #18 + OP § 3.2 Mathematical Layer routing. Companion artifact to `2026-05-27-cycle-13-pre-launch-design-session-closeout.md`.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27
**Pattern:** design-spec-as-math handoff (gandalf authors structure; gamora calibrates numerics)
**Authority basis:** Matt 2026-05-27 — "Math before code. Let's see if we can collaborate to find a scaffolding which gamora can use to build off of."
**Composes with:**
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 (multi-T4 architecture + D60 + D84 sim methodology)
- `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + ~30-day seasonal duration — Wave 0 authoring)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8-axis BC operational truth)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #18 (methodology consultation at math hotspots) + amendment 18.2 (consultation timing at extension hotspots)

---

## 0. Purpose + framing

Per balance-as-property (D1), simulation validates content at generation time. The validation gate is **playable-AND-in-band per progression node × cohort archetype × BC cell**. This doc provides the formal scaffolding gamora consumes to calibrate the validation gate empirically.

**Substrate-led split:**
- **gandalf produces** (this doc): vector dimensions, function signatures, cohort archetype identities, discipline gates, composition rules
- **gamora produces** (post-handoff): numerical targets per dimension, calibrated brackets per cell × node × cohort, cell-difficulty-adjustment formula

**Cycle 13 v1 scope:** calibrate against **endgame-reference-encounter** (L45-50+ progression node only); multi-node calibration is post-scaling-formulas work (Cycle 14+).

---

## 1. Scaffold 1 — Power vector P_node (GAP 1)

### 1.1 Formal definition

> **P_node = (KPM_target, HP_target, defensive_uptime_target, resource_flow_quality_target, skill_rotation_coherence_target)**

Power level is a 5-dimensional vector across mechanically-independent dimensions, NOT a scalar.

### 1.2 Dimension definitions

| Dimension | Definition | Measurement source |
|---|---|---|
| **KPM_target** | Kills-per-minute against progression-node-appropriate content; cohort-archetype-conditional | Gauntlet sim per cohort |
| **HP_target** | Player HP scaled to progression-node mob damage profile; ensures survivability against typical incoming damage | Gauntlet sim mob damage logs |
| **defensive_uptime_target** | % of encounter time at >50% HP; ensures player isn't in death-spiral as default state | Gauntlet sim HP-over-time |
| **resource_flow_quality_target** | Player not idle-waiting for resource regen more than X% of rotation; ensures skills usable when needed | Gauntlet sim resource-state-over-time |
| **skill_rotation_coherence_target** | Player has meaningful skill-choice at each rotation moment (not single-button spam OR analysis-paralysis) | Cohesion-judge metric extended |

### 1.3 Node identity mapping (per L50 hybrid framework lock 2026-05-27)

| Node | Level band | Content tier (per D50) | Engagement window (~3-4 week season) |
|---|---|---|---|
| **Early game** | L1-15 | T0 dominant | First ~1 week |
| **Mid game** | L15-30 | T0.5 dominant | Week 2 |
| **Endgame start** | L30-45 | T1 dominant (T0+0.5 still drop) | Week 3 |
| **Endgame** (85% target node) | L45-50+ | T1+T2 (all tiers in drop pool per D50) | Week 3-end + endgame phase |

### 1.4 Anchored intent (gamora calibrates specifics)

| Node | KPM intent | HP intent | Defense uptime | Resource flow | Rotation coherence |
|---|---|---|---|---|---|
| Early | ~20-30 | Survivable vs early mobs | ≥70% | Sustainable; skills mostly available | Coherent — small rotation pattern |
| Mid | ~40-55 | Higher per scaling | ≥75% | Sustainable with active management | Emerging rotation depth |
| Endgame start | ~60-70 | Scaling to endgame mobs | ≥75% | Active resource economy meaningful | Full rotation depth emerging |
| Endgame (85% target) | ~75+ | Endgame mob calibrated | ≥80% | Active management critical | Full rotation depth |

**Note: KPM numbers are anchors gamora refines via simulation.** What's LOCKED is the dimensional structure + monotonic-progression intent (each dimension rises across nodes; defense uptime stays high throughout per playability-AND-in-band per D61).

### 1.5 Cycle 13 v1 calibration scope

**Per session lock**: Cycle 13 calibrates against endgame-reference-encounter (P_endgame only). Per-level scaling formulas required for early/mid/endgame-start node calibration; deferred to Cycle 14+ or scaling-implementation cycle.

---

## 2. Scaffold 2 — Cohort archetype vector C_archetype (GAP 4)

### 2.1 Formal definition

> **C_archetype = (point_allocation_preference, stat_preference_vector, rotation_style, risk_tolerance, resource_management_style)**

Cohort archetype defines the player's PLAY STRATEGY. Different cohorts have different acceptable performance bands for the same content.

### 2.2 Dimension definitions + 4 cohort identities

| Dimension | Spectrum | DPS-min-maxer | Balanced | Defensive | Hybrid |
|---|---|---|---|---|---|
| **point_allocation_preference** | Concentration ↔ Spread | Concentration (max 1-2 chains) | Moderate (max 2 chains partial-fill) | Spread (3 chains partial) | Variable per substrate vote |
| **stat_preference_vector** (Offense, Defense, Utility) | weighting tuple | (0.7, 0.15, 0.15) | (0.45, 0.35, 0.20) | (0.20, 0.55, 0.25) | (0.40, 0.40, 0.20) baseline |
| **rotation_style** | Burst ↔ Sustain | Burst | Mixed | Sustain | Variable |
| **risk_tolerance** | Low-HP play ↔ Safe play | High (low-HP for damage bonuses) | Moderate | Low (maintains high HP) | Moderate |
| **resource_management_style** | Aggressive ↔ Conservative | Aggressive (spend-spend-spend) | Adaptive | Conservative (sustain-pool) | Adaptive |

### 2.3 Per-cohort KPM expectation against P_node

| Cohort | Expected KPM vs P_node KPM_target | Expected defensive_uptime vs P_node |
|---|---|---|
| **DPS-min-maxer** | 110-130% of KPM_target | 60-70% of defense_uptime_target |
| **Balanced** | 95-105% of KPM_target | 95-105% of defense_uptime_target |
| **Defensive** | 70-85% of KPM_target | 110-120% of defense_uptime_target |
| **Hybrid** | 85-110% (variable; substrate-led) | 85-110% (variable; substrate-led) |

### 2.4 Hybrid cohort discipline

**Hybrid is substrate-led** — specific hybrid identities emerge from kit composition; cohort assignment is per-kit at sim time. Composes with doc 40 D84 hybrid cohort + edge-case sampling methodology.

### 2.5 Scaling-independence

Scaffold 2 is fully scaling-independent. **FULL LOCK at session.** No deferral. Gamora consumes immediately.

---

## 3. Scaffold 3 — WR-bracket function W(cell, node, cohort) (GAP 7)

### 3.1 Formal definition

> **W(cell, node, cohort) → (WR_lower, WR_upper)**

Where:
- **cell** = BC-axis cell identity per 8-axis lock (68,040 cells; v1 scope ~22 cells per `v1-bc-target-intent-2026-05-24.md`)
- **node** = progression node per Scaffold 1 (Cycle 13 v1: endgame only)
- **cohort** = cohort archetype per Scaffold 2 (or substrate-led hybrid)

### 3.2 Functional structure

```
W(cell, node, cohort):
  base_bracket = node_baseline_bracket[node]
  cohort_adjustment = cohort_wr_modifier[cohort]
  cell_difficulty_adjustment = f(cell_BC_features, content_difficulty[node])

  return (
    WR_lower = base_bracket[0] * cohort_adjustment * cell_difficulty_adjustment,
    WR_upper = base_bracket[1] * cohort_adjustment * cell_difficulty_adjustment
  )
```

### 3.3 Anchored intent — node_baseline_bracket (gamora refines)

| Node | base_bracket (illustrative) | Reasoning |
|---|---|---|
| Early game | (0.55, 0.85) | Forgiving WR floor; cap prevents trivial content |
| Mid game | (0.50, 0.80) | Moderate floor |
| Endgame start | (0.45, 0.75) | Tightening floor; meaningful challenge |
| Endgame (85% target) | (0.40, 0.70) | Tightest floor; aspirational reaches but doesn't trivialize |

### 3.4 Cohort WR modifiers (illustrative; gamora calibrates)

| Cohort | WR modifier |
|---|---|
| DPS-min-maxer | × 1.0-1.1 (high damage compensates) |
| Balanced | × 1.0 (baseline) |
| Defensive | × 0.85-0.95 (trades WR for safety; lower acceptable floor) |
| Hybrid | × 1.0 (substrate-led; emergent) |

### 3.5 Cell-difficulty-adjustment — the math hotspot inside the scaffold

This maps BC-axis features (engagement profile / damage geometry / proxy density / control density / damage tempo / damage amplitude variance / defensive profile / resource economy per 8-axis lock) to expected encounter difficulty multipliers.

**This is the substantive math hotspot.** Routing per OP § 3.2:
- **gandalf**: design intent + axis-weight rationale + composition rules
- **gamora**: simulation calibration + multiplier formula
- **legolas Mode A**: external-literature research — ARPG difficulty-cell-mapping methodology (PoE Atlas mods, D4 Nightmare Dungeon mods, LE Monolith mods)
- **elrond**: statistical priors from substrate — do BC-axis cells produce naturally-clustered difficulty bands

---

## 4. Compose-rules — Steps 1-8 calibration loop

The three scaffolds compose into a calibration loop:

| Step | Action | Owner |
|---|---|---|
| **1. Generate** | Generation produces a kit in some cell at some progression-node difficulty | rocket Phase 2 |
| **2. Sim** | Sim runs the kit against node-appropriate content under each cohort archetype's play strategy (per Scaffold 2 dimensions) | gamora gauntlet sim |
| **3. Measure** | Per cohort simulation produces observed WR for kit × content × cohort triple | gamora telemetry |
| **4. Bracket** | WR-bracket function W(cell, node, cohort) returns acceptable range | Scaffold 3 calc |
| **5. Test per cohort** | If observed_WR ∈ [WR_lower, WR_upper] → kit in-band for that cohort | gamora gate |
| **6. Aggregate** | Kit ships if in-band for at least N cohorts (N is calibration parameter — substrate-voted) | gamora aggregate gate |
| **7. Failure handling** | If kit fails aggregate → T4-failure-handling Option F fires (doc 40 § 8.1 + 2026-05-27 lock) | rocket T4 algorithm |
| **8. Secondary validation** | Power vector P_node tracks: kit's KPM / HP / defensive uptime / resource flow / rotation coherence all must satisfy P_node intents per playability-AND-in-band per D61 | gamora playability gate |

**Substrate-led-discipline payoff:** numerical targets aren't pre-imposed. Engine generates; sim measures; W-bracket defines acceptability; whatever passes IS the season's content (per Q10 ratified framing brief).

---

## 5. Math hotspot routing summary

Per OP § 3.2 Mathematical Layer routing:

| Hotspot | Owner | Output |
|---|---|---|
| Design-spec-as-math (this doc) | gandalf | Scaffolds + composition rules ✓ |
| Simulation math + numerical calibration | gamora | Per-node targets; calibrated brackets; multiplier formula |
| External-literature methodology research | legolas Mode A | ARPG cohort-archetype definition methodology; ARPG WR-bracket calibration methodology; cell-difficulty-mapping literature |
| Statistical priors from substrate | elrond | Cohort emergence from kit composition data; BC-axis-cells natural difficulty banding |
| Telemetry capture for empirical refinement | star-lord | Per-fight outcome data; cross-season learning input |
| Gate-1 critique on scaffold + Gate-2 on gamora outputs | jack-ryan | Methodology critique + calibration verification |

---

## 6. Composition with locked architecture

### 6.1 With doc 40 § 8 multi-T4 architecture

- T4-failure-handling Option F fires when kit fails aggregate gate (Step 7)
- Multi-T4 sim methodology (D84 hybrid cohort + edge-case sampling) operates per Scaffold 2 + Scaffold 3
- Phase 4 sim cycling through all T4 configurations operates per Step 1-8 loop

### 6.2 With doc 40 § 3 spec-driven gear gen

- Content-compositional attunement (D33+D38+D51 amendment) means gear synergy contributes to P_node values measured in Step 3
- Synergy-score projection in Step 5 informs spirit-guide voice (D28)

### 6.3 With doc 40 § 8.7 + D61 playability criterion

- Playable-AND-in-band gate composes Step 5 WR-bracket + Step 8 P_node secondary validation
- Degenerate-state detection (Block D GAP 3 8-pattern catalog) fires as part of Step 8

### 6.4 With L50 hybrid progression framework (doc 41 — Wave 0)

- Node identities (Scaffold 1 § 1.3) map to level bands
- ~3-4 week engagement window bounds D18 85th-percentile cumulative target
- Per-level scaling formulas (deferred) are gamora math input for multi-node calibration

---

## 7. Handoff to gamora — Discipline #18 + amendment 18.2

Per Discipline #18 (methodology consultation at math hotspots) + amendment 18.2 (consultation timing at extension hotspots — fires AFTER baseline, not before):

**Gamora methodology consultation dispatch fires post-Wave-1** (after stat-sheet partition cycle lands the modifier surface gamora's sim consumes).

**Consultation inputs (from this doc):**
- P_node 5 vector dimensions ✓
- C_archetype 5 vector dimensions + 4 cohort identities + hybrid-as-substrate-led ✓
- W(cell, node, cohort) function signature + anchored intent + cell-difficulty-adjustment math hotspot ✓
- Compose-rules Steps 1-8 ✓
- Cycle 13 v1 endgame-reference-encounter scope constraint ✓

**Consultation outputs (gamora produces):**
- Per-node calibrated targets for each P_node dimension (endgame only for Cycle 13 v1)
- Per-cohort simulation strategy implementations
- Calibrated brackets per cell × node × cohort (endgame node × ~22 v1 cells × 4 cohorts = ~88 bracket calcs for Cycle 13 v1)
- Cell-difficulty-adjustment formula (math hotspot collaboration with legolas Mode A + elrond)
- Production implementation of Steps 1-8 calibration loop

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — design-spec-as-math handoff complete; gamora methodology consultation dispatches post-Wave-1 with this doc as input
**Composes with:** session closeout doc (`2026-05-27-cycle-13-pre-launch-design-session-closeout.md`); doc 40 § 8 + § 3; doc 41 (Wave 0 authoring); 8-axis BC lock; engineering disciplines #18 + amendment 18.2

**For:** the formal scaffolding gamora consumes to calibrate the Cycle 13 v1 mechanical season gen validation gate empirically. Math before code per Matt 2026-05-27 lock. Substrate-led-discipline preserved at numerical-calibration layer; design intent expressed at structural layer.

**Signed:** gandalf
