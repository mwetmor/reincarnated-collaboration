# Session 5 — Validation Architecture Spec

**STATUS:** DRAFT — Matt-authorized 2026-06-12 (Pattern B session, architecture cascade); fires after Sessions 1-4 implementation; closes all 4 hypothesis-only loops + validates BUILD SPEC assumptions
**Author:** gandalf
**Date:** 2026-06-12
**Grounding docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — PRIMARY (§ 4.1, 4.4, hypothesis test sections)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md` — T4 catalog
- `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` — companion modifier vector validation
- `agentic_orchestration/gandalf/notes/2026-06-12-session-3-core-combat-mechanics-spec.md` — Axes 2B, 3A, 3B, cognitive load metric
- Session 5 dependency: requires Sessions 1-4 engine implementations to be present before hypothesis tests run

**Produces:**
1. Multi-difficulty gauntlet spec — gamora seam (L1/L13/L26/L39 enemy scaling)
2. Content-type scenario definitions — gamora seam (Speedfarm / Push modes)
3. Per-fight mechanic attribution measurement design — gamora seam
4. Balance validation protocol for companion system — gamora + rocket seam
5. 5 hypothesis test specifications with pass/fail criteria

---

## 0. Design mandate

Session 5 closes the hypothesis loops. The four HYPOTHESIS-ONLY categories (cognitive load, power-plane validity, variant-axis, experiential axes) cannot be tested until the engine gaps they depend on are built. Session 5 builds the engine gaps (multi-difficulty gauntlet, content-type scenarios, attribution measurement) and runs the tests.

**The closed loop:** Sessions 1-4 produce specs → gamora/rocket implement → Session 5 validates → findings feed back to Sessions 1-4 open questions.

**Matt's role in Session 5:** Matt is present as inspection partner per the design-call agreement. Session 5 does not run as an unsupervised pipeline pass — Matt reviews hypothesis test results and rules on whether pass/fail criteria were correctly specified or need revision.

---

## 1. Multi-difficulty gauntlet design (gamora seam)

### 1.1 Four difficulty levels

| Level | Code | Enemy HP multiplier | Enemy damage multiplier | Enemy mechanics |
|---|---|---|---|---|
| Tutorial | L1 | × 0.25 | × 0.50 | None (basic auto-attack only) |
| Baseline | L13 | × 1.00 | × 1.00 | Current gauntlet enemy set (no change) |
| Hard | L26 | × 2.50 | × 1.75 | + AoE attacks + periodic shield phase |
| Endgame | L39 | × 5.00 | × 2.50 | + Phase transitions + CC skills + immune phases |

The level code (L1, L13, L26, L39) maps to the hypothesis doc's "power-plane validity" naming convention. L13 is the existing baseline; levels above and below bracket it.

### 1.2 Enemy mechanics for L26 and L39

**L26 additions:**
- AoE attacks: enemy gains 1-2 AoE skills (geometry = AoE_burst; 35% of enemy HP-based damage in 5m radius; 8s cooldown each)
- Shield phase: enemy activates a damage absorption shield at 60% HP; absorbs up to 30% of its remaining HP as incoming damage before breaking; lasts max 6 seconds

**L39 additions (adds to L26 mechanics):**
- Phase transitions: enemy enters Phase 2 at 50% HP (speed +20%; damage +15%) and Phase 3 at 25% HP (+1 additional AoE skill; immune_phase fires)
- CC skills: enemy gains 1 CC skill (slow or root; applied to player; 2.5s duration; 12s cooldown)
- Immune phases: at Phase 3 entry and at 10% HP, enemy becomes immune to the player's dominant damage type for 4 seconds (forces damage-type diversity to complete the fight)

**Implementation note (gamora):** L26 and L39 enemy mechanics use existing fight_engine infrastructure applied to enemy Combatant objects. AoE skills: enemy gains skills in its skill list with geometry = AoE_burst. Shield phase: fight_engine adds `damage_absorption_remaining: float` field to Combatant (additive — not a structural change). Phase transitions: threshold_events on enemy (same as ProxyCombatant threshold_events; gamora may reuse the interface). CC skills: enemy uses same CC effect system as player kit. Immune phases: `immune_element_temporary: str | None` field on Combatant; set at Phase 3 entry; cleared after 4 seconds.

### 1.3 Gauntlet configuration spec (gamora interface)

```python
@dataclass
class DifficultyConfig:
    level: int                    # 1, 13, 26, or 39
    hp_multiplier: float
    damage_multiplier: float
    enemy_mechanics: list[str]    # ["aoe_attacks", "shield_phase", "phase_transitions", "cc_skills", "immune_phases"]

def run_difficulty_gauntlet(
    kit_corpus: list[PlayerClass],
    difficulty: DifficultyConfig,
    n_fights_per_kit: int = 60,
) → dict[str, DifficultyGauntletResult]:
    # Returns results keyed by kit_id
```

The gauntlet runs all 400 in-band kits at the given difficulty; each kit vs the standard 3-enemy set (boss, elite, standard) × 20 each = 60 fights per kit.

### 1.4 Multi-difficulty regression anchor

Golden master at L13 remains the primary regression anchor. L26 and L39 results are NOT regression-anchored (they're intended to vary as enemy mechanics are tuned). L1 is a sanity check (all 400 kits should win >90% at L1).

---

## 2. Content-type scenario definitions (Speedfarm vs Push)

### 2.1 Speedfarm mode

**Design intent:** player is farming weaker content repeatedly for loot/resources. Fights are fast; build optimizes for speed-clear efficiency. Value proposition: burst kits dominate; sustained kits are penalized by time pressure.

**Speedfarm scenario config:**
- Enemy HP: × 0.50 of L13 baseline (enemies are weaker; they should die quickly)
- Enemy damage: × 0.75 of L13 baseline
- Fight time cap: 8 seconds. Any fight not resolved in ≤8 seconds is scored as a "slow clear" (partial win; not a loss; WR calculation method: `fast_clear_rate = fights_resolved_in_8s / total_fights`)
- Enemy mechanics: none beyond basic auto-attack
- Metric: `fast_clear_rate` AND `mean_fight_duration_s` (two-metric evaluation)

**Speedfarm winner profile:** burst tempo kits (Axis 3A = burst), glass cannon builds, Ravager/Striker labels, MOMENTUM_CASCADE T4 (Cascade bursts short fights).

### 2.2 Push mode

**Design intent:** player is pushing their limits; content is harder than they can comfortably clear. Fights are long; build optimizes for survival + sustained output. Value proposition: sustained kits and defensive kits excel; burst kits run out of steam.

**Push mode scenario config:**
- Enemy HP: × 3.0 of L13 baseline (enemies are much tougher)
- Enemy damage: × 2.0 of L13 baseline
- Fight time cap: none (fights run to resolution)
- Enemy mechanics: L26 mechanics (AoE + shield phase) apply
- Metric: `win_rate` (standard WR) AND `survival_rate` (fights survived regardless of outcome)

**Push winner profile:** sustained tempo kits, sustain Axis 4, DEFENSIVE_TRADEOFF T4, SACRIFICE_ASCENDANCY (HP economy), Warden/Sentinel labels.

### 2.3 Implementation (gamora seam)

```python
@dataclass
class ContentTypeConfig:
    mode: str                     # "speedfarm" | "push"
    enemy_hp_multiplier: float
    enemy_damage_multiplier: float
    fight_time_cap_s: float | None
    enemy_mechanics: list[str]

def run_content_type_scenario(
    kit_corpus: list[PlayerClass],
    config: ContentTypeConfig,
    n_fights_per_kit: int = 60,
) → dict[str, ContentTypeResult]:
```

---

## 3. Per-fight mechanic contribution attribution (5-property empirical validation)

### 3.1 Design goal

Empirically verify that skills assigned BUILD_DEFINING_CANONICAL (P-score = 1) in generation actually contribute disproportionately to fight outcomes. If a T4 capstone is assigned BUILD_DEFINING_CANONICAL on P1 but contributes < 5% of fight damage, the scoring was wrong.

### 3.2 Attribution tracking additions (gamora seam)

FightResult additions (alongside proxy contribution fields from Session 2 § 3.5):

```python
# Per-mechanic contribution tracking (additive to FightResult):
t4_capstone_damage_pct: float = 0.0          # T4 capstone skill's share of total fight damage
t4_capstone_utility_events: int = 0          # CC events, buff events, state transitions from T4
proxy_contribution_pct: float = 0.0          # proxy damage as % of total (player + proxy) damage
companion_wr_delta: float = 0.0              # WR delta vs no-companion baseline (companion pairings only)
skill_damage_distribution: dict[str, float] = {}  # per skill_id → % of total fight damage
cc_events_total: int = 0                     # total CC events applied in fight
t4_mechanic_state_activations: int = 0       # how many times the T4 state machine activated (Resonance activations, Cascade fires, Ascendancy activations, etc.)
```

### 3.3 P1-P5 empirical validation methodology

For each of the 400 in-band kits, after running the L13 gauntlet:
1. Extract `t4_capstone_damage_pct` and `t4_mechanic_state_activations` across 60 fights
2. Compare kits where `t4_capstone_damage_pct ≥ 0.30` (T4 is dominant contributor) vs kits where `t4_capstone_damage_pct < 0.10` (T4 is negligible)
3. Verify whether BUILD_DEFINING_CANONICAL P1 assignments correctly predict the high-contribution group

**P1 empirical validation pass/fail:**
- PASS: kits with T4 capstone P1 = BUILD_DEFINING_CANONICAL have mean `t4_capstone_damage_pct ≥ 0.20` across corpus
- FAIL: mean `t4_capstone_damage_pct < 0.10` for BUILD_DEFINING_CANONICAL kits → T4 capstone strategies are not empirically build-defining; loop back to Session 1 for magnitude adjustment

**P2 empirical validation (multiplicative composition):**
- Kits with T4 strategies in ELEMENT family should show `skill_damage_distribution` multiplicative compounding: ELEMENT_CONVERSION_MONO × chain damage > sum of individual skill contributions
- PASS: ELEMENT kits show ≥ 30% above additive baseline when chain damage is summed

### 3.4 Proxy contribution empirical validation

For proxy-family T4 kits:
- `proxy_contribution_pct` should be ≥ 0.15 (proxy contributes at least 15% of total fight damage or utility)
- For PROXY_SOVEREIGNTY kits: proxy contribution ≥ 0.20 (sovereignty proxy is a full combatant)
- FAIL threshold: proxy_contribution_pct < 0.05 for proxy-primary kits → proxy is a bystander, not a participant; gamora investigates fight_engine proxy action dispatch

---

## 4. Companion modifier balance validation protocol

### 4.1 Validation scale

- 400 in-band player kits × ~100 valid companion pairings per faction/binding gating = ~40,000 modifier applications
- Run as a dedicated balance pass (separate from standard gauntlet)

### 4.2 Validation metrics per pairing

For each (player_kit, companion_kit) pair:
1. Run player_kit at L13 with companion modifier applied: `wr_with_companion`
2. Run player_kit at L13 without companion modifier: `wr_no_companion` (from gauntlet baseline)
3. Compute: `companion_wr_delta = wr_with_companion - wr_no_companion`

### 4.3 Pass/fail criteria

| Criterion | Pass | Fail / Action |
|---|---|---|
| Max WR delta per pairing | ≤ +0.10 (10 WR points) | Reduce dominant modifier by 20%; rerun |
| Min WR delta per pairing | ≥ -0.05 (companion should not actively hurt) | Investigate negative-contribution companions; check modifier signs |
| Mean WR delta across valid pairings | 0.03 – 0.07 (2-7 WR point average benefit) | If < 0.03: companion system is negligible; revise modifier caps upward. If > 0.07: system too strong; reduce caps. |
| Cap compliance | All modifiers within type caps (Session 2 § 6.2) | Rocket modifier assignment bug; flag + fix |
| Faction filter compliance | Player and companion faction match | Rocket faction assignment bug |

### 4.4 Convergence item balance validation

For companion pairings with a valid convergence item (Session 1 § 4):
- Run the pairing with convergence item equipped vs without
- `convergence_item_wr_delta` should be ≤ +0.10 (convergence item adds at most 10 WR points)
- Pass: all 21×21 valid pairs produce convergence_item_wr_delta ≤ 0.10
- Fail: any pair produces > 0.10 → revise that pair's convergence effect magnitude

---

## 5. Five hypothesis tests — specifications

### Hypothesis Test 1: Power-plane validity

**Question:** Does the 400-kit in-band corpus remain within an acceptable performance band across all difficulty levels (L1, L13, L26, L39)?

**Setup:**
- Run all 400 in-band kits at L1, L13, L26, L39 (4 × 60 = 240 fights per kit; ~96,000 total fights)
- Measure WR at each difficulty level

**Pass criteria:**
- L1: ≥ 400/400 kits have WR ≥ 0.85 (tutorial is not a challenge; all kits should win)
- L26: ≥ 360/400 kits (90%) have WR ≥ 0.25 (kits are still viable at hard difficulty; not demolished)
- L39: ≥ 320/400 kits (80%) have WR ≥ 0.10 (kits struggle at endgame but are not helpless)
- Power-plane coherence: for ≥ 90% of kits, L39_WR ≥ L26_WR × 0.50 (L39 is harder but not a cliff; no kit goes from 60% at L26 to 2% at L39)

**Fail criteria / action:**
- If > 10% of kits fall below L26 WR 0.25: enemy scaling at L26 is too aggressive; reduce HP multiplier by 10% and retest
- If > 20% of kits have cliff performance (L39_WR < L26_WR × 0.40): L39 immune phase duration or damage multiplier is too punishing; reduce and retest
- Matt reviews and rules on scaling revisions

**Relationship to investment profile:** high-investment kits (Session 4 § 5) are expected to show wider WR spread at L26/L39. The test distinguishes high-investment "correctly scales with gear" (expected) from "broken at all gear tiers" (fail).

---

### Hypothesis Test 2: Variant-axis (Speedfarm ↔ Push mode diversity)

**Question:** Do different kit archetypes excel in Speedfarm vs Push? Is the kit space genuinely diverse across content types?

**Setup:**
- Run all 400 in-band kits in Speedfarm config and Push config (60 fights per kit per config; 120 fights per kit total)
- Rank kits by Speedfarm metric (`fast_clear_rate`) and Push metric (`win_rate`)

**Pass criteria:**
- Top-10 Speedfarm kits and Top-10 Push kits share ≤ 4 kits in common (≤ 40% overlap)
- Axis 3A = Burst kits have mean Speedfarm fast_clear_rate ≥ 10% above Axis 3A = Sustained mean (burst kits genuinely better at Speedfarm)
- Axis 4 = Sustain kits have mean Push win_rate ≥ 10% above Axis 4 = Glass_canon mean (sustain kits genuinely better at Push)

**Fail criteria / action:**
- Top-10 overlap > 4 kits: variant diversity not achieved; investigate whether Speedfarm config is differentiated enough (time cap may need lowering; enemy HP may need further reduction)
- No stat-significant archetype differentiation: content-type scenarios are not pulling different kit archetypes to the top; revisit scenario design
- Matt reviews and rules

---

### Hypothesis Test 3: Experiential axes — BC axis behavioral distinctiveness

**Question:** Do kits in different BC axis bins actually produce meaningfully different fight experiences in telemetry?

**Setup:**
- For each BC axis with ≥ 2 bins, compare fight telemetry between the highest and lowest bins
- Axes to test: Axis 1 (close vs long range), Axis 2 (single_target vs AoE), Axis 2B (HIGH vs LOW control_density), Axis 3A (burst vs sustained), Axis 4 (glass_canon vs sustain)

**Pass criteria per axis:**
- Axis 1 (range): close_range kits have mean fight_duration ≤ 0.85 × long_range fight_duration (close kits end fights faster on average)
- Axis 2 (geometry): AoE kits have mean `enemies_hit_per_skill_use` ≥ 1.5× single_target kits
- Axis 2B (control density): HIGH CC kits have mean `cc_events_per_fight` ≥ 3× LOW CC kits
- Axis 3A (tempo): burst kits have mean `t4_capstone_damage_pct` in first 3s ≥ 40%; sustained kits ≤ 20%
- Axis 4 (defense): sustain kits have mean `player_hp_remaining_pct` at fight end ≥ 1.5× glass_canon kits

**Fail criteria / action:**
- Any axis pair shows no significant behavioral difference (< 10% separation on its metric): the BC axis may not be capturing the intended experiential dimension; session produces a finding for Matt and gandalf to revisit the axis definition
- Matt reviews per-axis results and rules on whether the axis definitions are sufficiently capturing distinct experiences

---

### Hypothesis Test 4: 5-property empirical validation (BUILD_DEFINING_CANONICAL)

**Question:** Do T4 capstone mechanics assigned BUILD_DEFINING_CANONICAL actually dominate fight outcomes empirically?

**Setup:**
- Run 400 in-band kits at L13 (standard gauntlet); collect `t4_capstone_damage_pct` and `t4_mechanic_state_activations`
- Compare BUILD_DEFINING_CANONICAL (P1=1) T4 kits vs T4 strategies with lower P-scores (proxy-family kits where proxy contributes rather than capstone directly)

**Pass criteria:**
- Mean `t4_capstone_damage_pct` across kits with T4 strategies in COMBAT family (MOMENTUM_CASCADE, RESONANCE_LOOP, NETWORK_AMPLIFIER, ELEMENTAL_ECHO) ≥ 0.20 (T4 capstone contributes ≥ 20% of fight damage on average)
- Mean `t4_mechanic_state_activations` ≥ 3 per fight for state-machine T4 strategies (RESONANCE_LOOP, MOMENTUM_CASCADE, TEMPORAL_CHARGE)
- For proxy-family T4 kits: `proxy_contribution_pct` ≥ 0.15 (proxy IS the build-defining contribution)

**Fail criteria / action:**
- COMBAT-family T4 `t4_capstone_damage_pct` < 0.10: capstone is negligible; magnitude adjustments needed; loop to Session 1
- `t4_mechanic_state_activations` = 0-1 per fight: state machine is not being triggered in standard fights; either eligibility gates are too restrictive OR the mechanics require player skill to trigger and the sim's optimal-rotation assumption doesn't model it (which is the cognitive load hypothesis — see Test 5)
- Matt reviews and rules on magnitude / gate revisions

---

### Hypothesis Test 5: Cognitive load — simulation vs play divergence

**Question:** Do high-cognitive-load kits (RESONANCE_LOOP, TEMPORAL_CHARGE) perform better in simulation (optimal execution always) than they would in real play?

**Simulation-side test:**
- Compare WR of HIGH cognitive_load kits vs LOW cognitive_load kits at L13
- Hypothesis: HIGH cognitive_load kits have ≥ 5% higher sim WR due to perfect execution

**Pass criteria (simulation side only):**
- HIGH cognitive_load bin kits: mean L13 WR ≥ mean LOW cognitive_load WR + 0.05 (5 WR points advantage for optimal execution)
- RESONANCE_LOOP kits specifically: mean `t4_mechanic_state_activations` ≥ 4 per fight (sequence fires consistently in sim)

**The real-play divergence (Session 5 cannot measure this; flags for future work):**
- Sim assumes perfect timing; real players miss the 3s RESONANCE_LOOP window, under-charge TEMPORAL_CHARGE, etc.
- The divergence between sim WR and real-play WR for HIGH cognitive_load kits is the "execution complexity penalty"
- Measuring this requires the UE demo instrumentation (out of Session 5 scope; flagged to galadriel/drax as a future measurement requirement)

**Session 5 output:** documents the expected sim/play divergence hypothesis; produces the simulation side of the measurement. Real-play validation is gated on demo instrumentation.

---

## 6. Session 5 open questions

| # | Question | Priority |
|---|---|---|
| 1 | L39 immune_phase damage type selection: which of the player's damage types becomes immune? Highest-damage type? Random? Rotating? | HIGH — affects L39 balance significantly |
| 2 | Speedfarm 8-second fight cap: is 8 seconds the right threshold? Depends on current mean fight duration at L13. What's the baseline mean fight duration? | HIGH — gamora should report this; calibrate from data |
| 3 | Power-plane test fight count: 240 fights per kit (4 difficulties × 60 fights) = 96,000 total fights. Estimated runtime? Acceptable? | MEDIUM — gamora pre-flight compute estimate needed |
| 4 | Companion balance validation fight count: ~40,000 modifier applications at 60 fights each = 2.4M fights. This may be too expensive. Subsample to 20 fights per pairing? | HIGH — scale question; Matt + gamora alignment needed |
| 5 | P1-P5 empirical validation: the P-score framework is production-side (rocket assigns at generation). Is score assignment reviewable at validation time? Or is it implicit in kit record fields? | MEDIUM — telemetry question; star-lord seam |
| 6 | Convergence item compatibility matrix: 21×21 = 441 pairs; only N valid pairs (Session 1 open question #4 unresolved). How many valid pairs are expected? Must be resolved before convergence item validation is scoped. | HIGH — Session 1 blocking dependency |
| 7 | Cognitive load sim/play divergence: is galadriel's visual perception instrumentation sufficient to measure this, or does it require a dedicated gameplay telemetry stream in the UE demo? | LOW — future work scoping |

---

## 7. Session 5 sequencing and session context

| Gate | Required completion before Session 5 runs |
|---|---|
| Session 1 T4 implementation (gamora + rocket) | T4 capstone state machines must exist for Test 4 |
| Session 2 gamora kernel handoff complete | ProxyCombatant must exist for proxy contribution tracking |
| Session 3 Layer 2 + cognitive_load (rocket) | cognitive_load scores must be in kit records for Test 5 |
| Session 4 kit identity + generation (rocket) | investment_profile, faction fields must be in kit records |
| Companion modifier vector (gamora) | companion modifier application must exist for companion balance validation |

Sessions 3 and 4 can run in parallel with Sessions 1 and 2 implementations. Session 5 is the final gate — it does not fire until all four seam implementations land.

**Matt's inspection role in Session 5:** Matt reviews each hypothesis test result and has BLOCK authority on pass/fail criteria revisions. A hypothesis test that fails is not a project failure — it is information. Matt's ruling on what the failure means determines whether to adjust the engine or revise the hypothesis.

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 5 validation architecture spec. Final session of the 5-session cascade; gates all hypothesis loop closures.
