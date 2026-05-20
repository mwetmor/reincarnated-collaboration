# Dispatch — Gamora Counterfactual Math: R2 Convergence + ST Damage Multiplier (math-before-code investigation)

**Authored by:** gandalf, 2026-05-19, post-wind-down session with Matt
**Authority:** Matt directive 2026-05-19 evening: *"actually, please draft it now for the current knight-rider to dispatch to gamora"* + amendment: *"It may make sense to also draft a hypothesis test regarding ST skill damage multiplier"*; autonomous-operation continues per protocol § 4.0; in-session gandalf design-stewardship
**Status:** 🟢 **READY TO FIRE.** May be fired by knight-rider (when re-activated) OR by gandalf under hive-iteration mode (`agentic_orchestration/gandalf/requests/2026-05-19-gandalf-iterate-with-gamora-on-counterfactual-math.md`). Math-first investigation; **conditional implementation + validation downstream IF math validates a lever** per Matt directive 2026-05-19: *"If proven true, why don't we add an engine update and run to validate?"*
**Owner:** gamora (under gandalf design-stewardship if hive-iteration mode is active)
**Scope:** **Two parallel hypothesis experiments + conditional implementation + validation** — (1) R2-as-canonical convergence target counterfactual; (2) ST-damage-multiplier counterfactual. Both analyzed from existing telemetry; complementary levers; shared methodology. **If either H rejects null at sufficient strength → implement the validated lever in code → validate empirically.**
**Estimated effort:**
  - Math-only phases (A–D): 6–10 hours focused gamora analytical work
  - Implementation phase (E): 4–8 additional hours if ST mult lever validates; 16+ hours if R2-as-canonical (file as HELD dispatch if exceeds bound)
  - Validation phase (F): 2–4 hours
  - **Total: 12–22 hours if everything runs end-to-end; 6–10 if math alone wind-downs the iteration**
**Discipline anchors:** #1 (math-before-code), #11 (empirical inspection over assumption), #2 (smoke-test vs full-regen), #18 (named constants in code)

---

## § 0 — TL;DR

**Two parallel math-before-code experiments to resolve which lever (if any) actually fixes the boss-tier collapse pathology.** Both use existing telemetry — no new sims, no code changes, no convergence runs.

### Experiment 1 — R2 Counterfactual Convergence

**Matt's architectural critique:** the engine **tunes** classes against the 1D PackProxy gauntlet (×8 AOE multiplier; non-spatial) but **gates** them against the R2 spatial sub-gauntlet (8 actual entities; geometry-aware). Tuning against an approximation while validating against reality is structurally counterproductive. The "saturate-low + collapse-boss" pathology, the kit-redesign queue, the AOE-skew architectural finding, the Option A floor-widening proposal — these may all be **artifacts of measuring against the wrong gauntlet** rather than fundamental kit properties.

**The experiment:** from existing R2 spatial telemetry (51 classes × 3 scenarios × 30 fights), analytically derive: *"if R2 had been the convergence target instead of 1D PackProxy, what modifier would each class have converged to under per-tier WR targets?"*

### Experiment 2 — ST Damage Multiplier Counterfactual

**Matt's secondary hunch:** *"I suspect that ST skill damage may need a slight increase but I'm not certain."* The architectural asymmetry between AOE (×8 PackProxy) and ST (×1) may not be best addressed by *reducing* AOE leverage — it may be addressed by *raising* ST per-cast damage. This decouples the levers: ST can carry boss-tier damage without changing AOE's swarm-clearing behavior.

**The experiment:** from existing 1D R1 retune sprint v3 data (51 classes × 12-fight gauntlet), analytically derive: *"what ST damage multiplier value K produces per-tier all-tier-pass for ≥ 60% of classes under current 1D PackProxy convergence?"* Sweep K from 1.0 to 2.5; find the smallest K that produces per-tier convergence at the population level.

### What's at stake — joint interpretation

| Experiment 1 result | Experiment 2 result | Architectural implication |
|---|---|---|
| Strong-reject null (≥80%) | (any) | **R2-as-canonical is the surgical fix.** Boss collapse is a 1D measurement artifact. Kit-redesign queue mostly unnecessary. |
| Moderate (60-80%) | Slight K (1.1-1.3) suffices | **Either lever works.** Matt picks based on engineering cost: R2 architecture ($$$) vs ST mult tuning ($). |
| Cannot reject (<60%) | Large K (>1.5) needed | **Both levers needed.** Catalogue has structural pathology that neither lever alone resolves. Kit-redesign queue + architectural change. |
| Cannot reject | Cannot reject (no K works) | **Deepest fix required.** Kit-quality + generation-rules pass. R8-inversion regeneration with AOE share reduction. |

**The two experiments are complementary, not exclusive.** Running both in one gamora session resolves the architectural-lever question with high confidence at minimal engineering cost.

---

## § 1 — Required reading (in order)

1. **This dispatch in full** (~10 min)
2. **`reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`** — the R2 spatial damage resolution code; particularly the comment *"Does not reproduce the full armor/resistance/crit chain from fight_engine.py (the 1D engine handles that for balance convergence). This is the spatial POSITIONING substrate — fidelity in hits-per-tick, not exact damage numbers."* This caveat is load-bearing for the analytical work below.
3. **`reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py`** — the three scenario definitions (open_arena, chokepoint_corridor, boss_with_adds) with exact dimensions + spawn positions
4. **`output/R2-sprint-2026-05-19/per_class_results.json`** — the existing R2 sprint output (51 classes × 3 scenarios)
5. **`output/R2-sprint-2026-05-19/R2-1d-vs-2d-delta.md`** — 1D vs 2D per-class WR comparison
6. **`output/R1-sprint-v3-2026-05-19/sprint-v3-summary.md`** — the current 1D-converged per-tier WR baseline (0/51 kit-acceptable; 0/51 boss kills under disposition-3 calibration)
7. **`reincarnated-engine/src/reincarnated/simulation/balance_loop.py`** — particularly `PACK_PROXY_SIZE = 8` and the 12-fight gauntlet composition; the convergence binary search code
8. **`canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`** — gandalf's original architectural diagnosis (the 5-axis gap framing)
9. **`canonical/story/r1-firstbatch-fail-disposition-2026-05-19.md`** if it exists, or **`agentic_orchestration/matt-briefing-2026-05-19-s1-firstbatch-fail-disposition.md`** — the S1 failure arc and Option A briefing context

---

## § 2 — Scope: Experiment 1 — R2 Counterfactual Convergence

### § 2.1 — The question

For each of the 51 shipped classes (seasons 002011-015), compute: **what modifier would the class have converged to under per-tier WR targets if R2 spatial sub-gauntlet were the convergence target instead of 1D PackProxy gauntlet?**

Per-tier WR targets (R1 disposition; canonical):

| Tier | Target | Floor | Ceiling |
|---|---|---|---|
| swarm | 0.72 | 0.65 | 0.80 |
| magic | 0.62 | 0.55 | 0.70 |
| elite | 0.52 | 0.45 | 0.60 |
| mini-boss | 0.45 | 0.35 | 0.55 |
| boss | 0.38 | 0.30 | 0.45 |

### § 2.2 — Mapping R2 scenarios to per-tier targets

R2 only has 3 scenarios. They proxy for tier coverage as follows:

| R2 scenario | Tier proxy | Notes |
|---|---|---|
| `open_arena` (8 swarm mobs in 50×50) | **swarm tier** | Direct mapping; 8 actual entities at individual HP |
| `chokepoint_corridor` (8 swarm in 10×50 with bottleneck) | **swarm tier (variant)** | Tests geometric exploitation; same entity model |
| `boss_with_adds` (1 boss + 2 elite at 30×30) | **boss tier** (with elite adds as flavor) | Direct mapping; win = boss_killed |

**Gap acknowledged:** R2 does NOT have explicit magic / elite / mini-boss scenarios. For this counterfactual, **focus on the two tiers R2 measures (swarm + boss) and report per-class hypothetical modifier derived from those two tiers alone.** Magic/elite/mini-boss tier convergence is out of scope for this investigation; flag this as a follow-on if R2 emerges as canonical convergence target candidate.

### § 2.3 — The analytical model

R2 spatial telemetry already records per-class per-scenario per-fight outcomes. Specifically (per `spatial_engine.py`):

- `geo_hits_actual` — actual hits per geometry type (cone, circle, line, point) per fight
- `geo_hits_max_possible` — denominator for hit-fraction (alive mobs at cast time)
- Total damage dealt + skills fired count per fight
- Per-scenario WR aggregate

**Analytical derivation per class per tier:**

```
For class C, scenario S (swarm or boss):
  observed_WR_at_modifier_M = R2_telemetry[C][S].win_rate

  # The hit-fraction tells us per-cast spatial efficiency
  hits_per_cast_by_geometry = {
    g: geo_hits_actual[g] / geo_hits_max_possible[g] for g in geometries
  }

  # From kit JSON: per-skill base damage + geometry type
  # From R1 sprint v3 per_class_results.json: current 1D-converged modifier M
  # Compute theoretical kit DPS at modifier M in R2:
  kit_DPS_R2(M) = sum over skills s:
    base_damage(s) × hits_per_cast(geometry_of_s) × M / cooldown(s) × hit_rate × variance_avg

  # Scenario WR is approximately monotone in DPS vs scenario HP/timeout:
  # WR_swarm(DPS) = f(DPS, 8 × swarm_HP, 120s)
  # WR_boss(DPS) = f(DPS, boss_HP × 0.40, 240s, boss_armor)

  # Solve for M* such that:
  # WR_swarm(kit_DPS_R2(M*)) ∈ [0.65, 0.80] AND WR_boss(kit_DPS_R2(M*)) ∈ [0.30, 0.45]
```

The function `f(DPS, HP, timeout)` is approximately a sigmoid in DPS, anchored by the empirical R2 observations. Calibrate it from the data points we have.

### § 2.4 — Methodology

1. **Extract R2 spatial telemetry** from `output/R2-sprint-2026-05-19/per_class_results.json`. Per class, capture per-scenario WR + per-geometry hits-per-cast empirical data.

2. **Extract current 1D-converged modifier** per class from R1 retune sprint v3 results (`output/R1-class-retune-2026-05-19/per_class_results.json`). This is the existing modifier M each class converged to under 1D PackProxy convergence.

3. **Calibrate the DPS-to-WR sigmoid** per scenario type. Use the existing R2 observations as anchor points: at the current modifier M, each class achieved some swarm WR and boss WR in R2. This is one data point per class per scenario. With 51 classes, we have 51 anchor points per scenario, sufficient to fit a sigmoid model.

4. **Solve for hypothetical R2-converged modifier M\*** per class. For each class, find M\* such that:
   - WR_swarm_predicted(M\*) lands in [0.65, 0.80]
   - WR_boss_predicted(M\*) lands in [0.30, 0.45]
   - If no single M\* satisfies both → report the unsatisfiability and per-tier WR at the closest M\*

5. **Compare M\* against current M** per class. Output:
   - Histogram of M\* across 51 classes
   - Per-class: M (1D-converged), M\* (R2-converged), Δ
   - Per-class: WR_swarm_1D, WR_swarm_R2_at_M, WR_swarm_R2_at_M\*
   - Per-class: WR_boss_1D, WR_boss_R2_at_M, WR_boss_R2_at_M\*
   - Aggregate: % of classes that achieve all-tier-pass under M\* convergence

### § 2.5 — Calibration notes (Discipline #1 anchoring)

The analytical model has approximations. Document each one explicitly:

- **R2 simplified damage chain.** Per `spatial_engine.py` comment, R2 doesn't reproduce armor/resistance/crit/substrate matrix. The DPS-to-WR sigmoid calibration must acknowledge this. Use the actual 1D damage formula (`compute_damage_scaling` + armor mitigation + resistance + crit + per-hit variance) when computing kit_DPS, but anchor the WR sigmoid to R2 empirical observations.

- **Mob spread variance.** R2 spawns mobs at fixed positions per scenario. The "hits-per-cast" empirical data reflects this fixed spread. In a hypothetical R2-convergence regime, mob spread might be randomized; document this assumption.

- **Single-modifier scaling.** This counterfactual assumes the SAME single-modifier convergence loop, just against R2 outcomes instead of 1D. It does NOT assume per-tier-modifier scaling (that would be a different architecture).

- **2-tier convergence only.** The output is honest about what R2 can measure. magic/elite/mini-boss tiers are out of scope for this counterfactual; flag for follow-on if R2 emerges as canonical.

### § 2.6 — Hypothesis tests (math-before-code discipline)

Frame the math experiment as testing two hypotheses:

**Hypothesis 1 (the architectural critique):** The boss-tier collapse pathology is an artifact of 1D PackProxy convergence; under R2 convergence, most classes would satisfy per-tier targets including boss-tier WR ≥ 0.30.

- **REJECT NULL if:** ≥ 60% of 51 classes have hypothetical M\* such that WR_boss_predicted(M\*) ∈ [0.30, 0.45] AND WR_swarm_predicted(M\*) ∈ [0.65, 0.80]
- **STRONG REJECT NULL if:** ≥ 80% satisfy both
- **CANNOT REJECT NULL if:** < 60% satisfy both

**Hypothesis 2 (the catalogue-quality counter-hypothesis):** Even under R2 convergence, the catalogue retains structural kit-quality pathology; some/most classes cannot satisfy per-tier targets at any modifier.

- **CONFIRM if:** > 40% of classes have NO M\* that satisfies both swarm + boss targets simultaneously
- **REJECT if:** < 20% are unsatisfiable

The two hypotheses are testable from the same data analysis. Report both outcomes explicitly.

---

## § 2B — Scope: Experiment 2 — ST Damage Multiplier Counterfactual

### § 2B.1 — The question

**For each candidate ST damage multiplier K (sweeping from 1.0 to 2.5 in 0.05 steps): how many of 51 shipped classes satisfy all per-tier targets under current 1D PackProxy convergence?** Find the smallest K that produces ≥ 60% pass rate. Report whether such K exists in the "slight increase" range (1.0 < K ≤ 1.3) or requires a larger value.

### § 2B.2 — The lever being tested

The ST damage multiplier K is a hypothetical per-cast multiplier applied to **non-AOE skill geometries only**. Definitions:

- **ST geometries (K-eligible):** `point`, `single_target`, `melee_strike`, `ranged_physical`, `projectile` (and any others NOT in `AOE_GEOMETRIES` set per `b6_archetype_templates.py`)
- **AOE geometries (NOT K-eligible):** the 16 geometries in `AOE_GEOMETRIES` (cone, circle, line, melee_arc, ground_slam, ground_targeted_circle, beam_channel, whirlwind, dash_attack, leap_strike, chain_lightning, ricochet_bounce, vortex_pull, ring, multi_projectile, fork)

**Where K would be applied in the architecture (analytical only — not implementing):** as a multiplier on `damage_multiplier` field for skills with non-AOE geometry, OR as a `_ROLE_MAGNITUDE_MULTIPLIERS` adjustment that effectively up-weights ST-leaning roles. The math is methodology-neutral — Experiment 2 just answers "what value of K resolves per-tier convergence?"

**Why this lever is interesting (Matt's intuition):**

Current architecture: `AOE × PackProxy_8 / ST × 1` creates a ~5.3:1 swarm-damage advantage for AOE that the single modifier scalar cannot bridge to boss-tier requirements. The asymmetric levers:

| Lever | Acts on | Effect | Side effect |
|---|---|---|---|
| **Reduce AOE share** (`_AOE_SHARES`) | Kit composition (future regen only) | Fewer AOE skills per kit | Existing catalogue unaffected; mage/controller identity weakened |
| **Reduce PackProxy multiplier** | 1D gauntlet damage scaling | Smaller AOE advantage at swarm | Changes "balanced" semantics; cascade re-converge |
| **★ Increase ST damage multiplier (K)** | Per-cast damage for ST skills | ST per-cast damage rises; boss DPS rises at same modifier | AOE unchanged; swarm saturation pattern unchanged |
| **Promote R2 to canonical convergence** (Exp 1) | Convergence target itself | Removes 1D approximation entirely | 2-4 wk engineering investment |

**Matt's hunch is that K is the most surgical lever** because it directly addresses the boss-side undersupply without touching swarm-side oversupply. If K = 1.2 produces all-tier convergence, that's a 20% per-cast bump on ST skills — minimally invasive, no architectural change, no kit-redesign cascade.

### § 2B.3 — The analytical model

Existing data: R1 retune sprint v3 (`output/R1-sprint-v3-2026-05-19/per_class_results.json`) has per-class per-tier WR at each class's current 1D-converged modifier M. Each class JSON has its skill list including geometry types.

**Per-class derivation per candidate K:**

```
For class C at current modifier M, candidate ST multiplier K:
  For each skill s in kit:
    if geometry(s) ∉ AOE_GEOMETRIES:
      adjusted_per_cast(s) = base_per_cast(s) × K
    else:
      adjusted_per_cast(s) = base_per_cast(s) × 1.0  # AOE unchanged

  # Recompute per-tier WR with adjusted ST damage at SAME modifier M
  # (not re-converging — testing the effect at current convergence point)
  WR_swarm(C, M, K) = f(adjusted_kit_DPS_vs_swarm_pack_proxy, swarm_HP × 8, 120s)
  WR_magic(C, M, K)
  WR_elite(C, M, K)
  WR_miniboss(C, M, K)
  WR_boss(C, M, K)

  # Determine per-tier pass under R1 disposition targets
  all_tier_pass(C, M, K) = all per-tier WRs in their respective bands
```

**Sweep K from 1.0 to 2.5 in 0.05 steps. For each K, compute population pass rate (% of 51 classes with all_tier_pass = True). Find K\* = smallest K producing pass rate ≥ 60%.**

### § 2B.4 — Methodology

1. **Extract per-class per-skill data** from shipped season JSONs (`output/standard-demo-regen-2026-05-17/season_002011-015/classes/*.json`) AND from R1 retune sprint v3 per_class_results.json. Capture:
   - Per-class current modifier M
   - Per-skill: base_magnitude, role, geometry_type, geometry, damage_multiplier, cooldown
   - Per-class current per-tier WR

2. **Classify each skill** as ST (non-AOE-geometry) or AOE (AOE-geometry). Use the same `AOE_GEOMETRIES` frozenset from `b6_archetype_templates.py` (16 geometries).

3. **For each candidate K:** recompute per-class kit DPS as the sum over skills:
   ```
   kit_DPS(K, modifier=M) = Σ_skills [ base_dmg(s) × geometry_mult(s) × multiplier(s, K) × M / cooldown(s) ] × hit_rate × variance_avg × crit_mult
   ```
   where `multiplier(s, K) = K if ST geometry, 1.0 if AOE geometry`.

4. **Compute per-tier WR at this kit DPS** using the same DPS-to-WR sigmoid calibrated in Experiment 1 (shared calibration; no duplication). For non-swarm tiers (magic, elite, miniboss, boss), DPS includes no PackProxy mult (1v1 fights). For swarm tier, AOE portion gets ×8.

5. **Per-tier pass check** against R1 disposition target bands.

6. **Population-level analysis** at each K: % of 51 classes that achieve all-tier-pass. Plot pass-rate vs K. Identify:
   - K\* (smallest K producing ≥ 60% pass rate)
   - K\*\* (smallest K producing ≥ 80% pass rate)
   - K\*\*\* (smallest K producing ≥ 95% pass rate)
   - If no K in [1.0, 2.5] produces ≥ 60%, report as "no slight-bump suffices"

### § 2B.5 — Hypothesis tests (Experiment 2)

**Hypothesis 3 (Matt's hunch):** A slight ST damage multiplier increase (K ∈ [1.1, 1.3]) produces all-tier-pass for ≥ 60% of classes under current 1D PackProxy convergence.

- **REJECT NULL if:** K\* exists in [1.0, 1.3]; population pass rate ≥ 60%
- **STRONG REJECT NULL if:** K\* exists in [1.0, 1.2]; population pass rate ≥ 80%
- **CANNOT REJECT NULL if:** K\* requires > 1.3, OR no K in [1.0, 2.5] produces ≥ 60%

**Hypothesis 4 (depth of lever required):** Some K value (within or beyond the slight range) produces population pass rate ≥ 60%.

- **REJECT NULL if:** K\* exists in [1.0, 2.5]
- **CANNOT REJECT NULL if:** No K in [1.0, 2.5] produces ≥ 60% — implies the catalogue has structural pathology beyond per-skill damage scaling

### § 2B.6 — Joint interpretation matrix (Experiments 1 + 2 combined)

After both experiments complete, classify the joint outcome:

| Exp 1 verdict | Exp 2 verdict | Joint interpretation | Recommended next dispatch |
|---|---|---|---|
| Strong-reject H1 (R2 fixes it ≥80%) | Slight K suffices | **Both levers work independently** | Matt picks based on cost; recommend R2-as-canonical (architectural cleanliness) |
| Strong-reject H1 | Large K needed (>1.3) | **R2 is the cleanest fix** | Move to R2-as-canonical integration dispatch |
| Cannot reject H1 (<60%) | Slight K suffices (≤1.3) | **K is the surgical fix** | Move to ST multiplier rollout dispatch (per-skill or per-role implementation) |
| Cannot reject H1 | Large K needed (>1.3) | **Two-lever combination** | Both R2 + K applied together; sequence as Matt approves |
| Cannot reject H1 | No K in [1.0, 2.5] works | **Catalogue has deeper pathology** | Kit-redesign queue is the actual fix; AOE share reduction in generation rules |

---

## § 3 — Napkin assumptions these experiments replace with empirical data

The gandalf framing of these experiments relied on several napkin-math assumptions during conversation with Matt. **Gamora should explicitly replace each one with empirical data per the table below.** The acceptance criteria's per-class results section (§ 5.3) must show actual values, not the napkin defaults.

### Assumptions REPLACED by Experiment 1 (R2 counterfactual)

| Napkin assumption | Empirical replacement | Source data |
|---|---|---|
| "Hypothetical 100%-ST kit at 12 skills, 6s avg cooldown" | **Each class's actual kit composition** — real number of skills per class, per-skill cooldown, per-skill role, per-skill geometry | `output/standard-demo-regen-2026-05-17/season_*/classes/class_*.json` |
| "AOE hits ~5-7 of 8 mobs in 2D" | **Actual hits-per-cast measured by R2 telemetry** per geometry type per class | `output/R2-sprint-2026-05-19/per_class_results.json` (geo_hits_actual / geo_hits_max_possible) |
| "DPS-to-WR sigmoid is approximately monotone" | **Empirically-fitted sigmoid** from 51 calibration points (51 classes × 2 scenarios) | Calibrated in § 2.4 step 3 |
| "Hit rate ~0.85 average" | **Per-class dex-derived accuracy/dodge values** | Class JSON `stat_distribution` + `compute_damage_scaling` |
| "Variance multiplier ~0.85" | **Sigmoid empirical fit absorbs variance noise** via 30-fight-per-class WR aggregates | R2 sprint fight count |
| "Substrate matrix neutral (×1.0)" | **Actual attacker_substrate vs target_substrate** per class-monster pair; ±25% only for holy↔shadow | `resistance_matrix.py` `_MATRIX_OVERRIDES` + per-class element + per-monster element |
| "Resistance neutral (0% boss resistance)" | **Actual per-monster resistance rolls** per class element | Monster JSON `elemental_resistances` field per scenario monster |
| "Boss HP 64k (calibrated)" | **Actual disposition-3 calibration constants** as used in R1 sprint v3 | `balance_loop.py` BOSS_HP_DIFFICULTY_MULTIPLIER etc. |

### Assumptions REPLACED by Experiment 2 (ST multiplier counterfactual)

| Napkin assumption | Empirical replacement | Source data |
|---|---|---|
| "100% ST kit" (idealized) | **Actual per-class AOE/ST geometry mix** | Each class's skill list with `geometry` field classified against `AOE_GEOMETRIES` frozenset |
| "All skills at burst_damage role mult ×1.0" | **Actual per-skill role + role multiplier** per `_ROLE_MAGNITUDE_MULTIPLIERS` | Class JSON `skills[].role` field |
| "Slight K ∈ [1.1, 1.3]" framing | **Full sweep K ∈ [1.0, 2.5] in 0.05 steps** to find smallest K satisfying per-tier population pass rate | Parametric sweep over R1 sprint v3 data |
| "≥ 60% pass rate threshold" | **Population pass-rate function of K** — full curve, not single threshold | Reported as monotonic curve in deliverable § 4 (aggregate findings) |
| "20% increase is 'slight'" framing | **Honest reporting of K\* value** — gamora reports exactly what K achieves what pass rate; "slight" framing is gandalf's hypothesis to test, not gamora's conclusion | Gamora reports K\*, K\*\*, K\*\*\* (per § 2B.4) without rhetorical framing |

### Assumptions that REMAIN as approximations (acknowledged limitations)

These are NOT replaced by either experiment. The deliverable should explicitly flag them:

| Approximation | Reason it remains | Mitigation if relevant |
|---|---|---|
| **R2 doesn't reproduce full damage chain** (no armor/resistance/crit in spatial_engine per its docstring) | R2 was a positioning-measurement layer, not a full damage sim | Calibrate sigmoid using observed WR (which DOES reflect those mechanics through the 1D-converged modifier the kits ran with) |
| **R2 spawn positions fixed** | Engineering simplification; positions hardcoded in `arena.py` | Document the assumption; flag for follow-on if Exp 1 strongly rejects null |
| **R2 only measures 2 tiers** (swarm + boss; no explicit magic/elite/mini-boss scenarios) | R2 sub-gauntlet scope per engine-rebuild | Exp 1 reports only swarm+boss outcome; gap acknowledged |
| **Modifier search range [0.05, 4.0]** | Current balance loop constraint | If Exp 1 hypothetical R2-converged modifier falls outside this range, flag explicitly |
| **R1 disposition-3 target bands** (per-tier WR targets) | Established by gandalf disposition; not under test here | If outcomes change materially under different target bands, gamora notes this as a follow-on consideration |
| **Per-class power_tier fixed at value in shipped data** | This is the existing catalogue; not regenerating | Both experiments use existing per-class power_tier (no synthetic shifts) |

**Discipline note:** any time gamora's math invokes a default or fallback value (e.g., "assume 6s cooldown when missing"), this must be flagged in the methodology section. **No silent defaults per Pattern P7.**

---

## § 4 — Cross-seam contract change? (ADR-004 / Principle 6 gate)

**NO.** Both experiments are analytical math against existing data. No code changes, no schema migrations, no MIGRATION.md required, no round-trip smoke needed.

**Follow-on dispatches** (NOT this dispatch) would have cross-seam contract implications:
- If Experiment 1 strong-rejects-null → R2-as-canonical convergence integration dispatch (significant cross-seam work; 2-4 weeks rocket + gamora + star-lord)
- If Experiment 2 produces viable K → ST damage multiplier rollout dispatch (modest cross-seam work; per-skill or per-role implementation; 3-5 days rocket)

**This dispatch produces evidence only.** Both experiments are math-only.

---

## § 5 — Acceptance criteria

Deliverable: math note at `reincarnated-engine/design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md` (or similar; gamora's call on naming). Sections required:

1. **§ 1 — TL;DR.** One-paragraph summary of findings: did Hypothesis 1 reject the null? At what strength?

2. **§ 2 — Methodology.** Document the DPS-to-WR sigmoid calibration approach. Show the calibration data points (51 classes × 2 scenarios). Document approximations + their expected impact.

3. **§ 3 — Per-class results table.** 51 rows: class_id, archetype, 1D-converged modifier M, hypothetical R2-converged modifier M\*, WR_swarm_at_M\*, WR_boss_at_M\*, all-tier-pass-under-M\*? (Y/N).

4. **§ 4 — Aggregate findings.** Histogram of M\* distribution. % of classes that achieve all-tier-pass under M\* convergence. Comparison to 1D current state.

5. **§ 5 — Hypothesis test verdicts.** Explicit pass/fail per Hypothesis 1 and Hypothesis 2. Include the data supporting each verdict.

6. **§ 6 — Architectural implication.** Honest interpretation: does the boss-collapse pathology survive R2 convergence, or is it a 1D measurement artifact?

7. **§ 7 — Follow-on recommendations.** If Hypothesis 1 strong-rejects null, recommend dispatch for actual R2 convergence integration. If Hypothesis 2 confirms, recommend kit-redesign queue continuation. If results are ambiguous, propose clarifying experiments.

8. **§ 8 — Math note appendix.** Any auxiliary calculations, sigmoid fitting details, approximation impact analyses.

**Acceptance tag:** `vs2a/v0.X-r2-counterfactual-convergence-math` (gamora picks X; suggested 0.15 or 0.16 to slot before Option A landing).

---

## § 6 — Out of scope (explicit non-goals)

- **NOT** rewriting balance_loop.py to use R2 as convergence target
- **NOT** adding magic/elite/mini-boss scenarios to R2 (out-of-scope for this investigation)
- **NOT** re-running R2 with new sims (use existing telemetry only)
- **NOT** redesigning kits or modifying archetype templates
- **NOT** changing PackProxy multiplier
- **NOT** Option A / Option B / kit-redesign queue execution (those are separate dispatches; this informs whether they're necessary)
- **NOT** making any decision about the architectural direction; this dispatch only PROVIDES the evidence to inform that decision

---

## § 7 — Open questions (for gamora to resolve under L1 autonomous authority)

1. **DPS-to-WR sigmoid fit methodology.** Logistic regression vs piecewise linear vs empirical-CDF interpolation. Gamora's choice; document the chosen approach.

2. **Variance handling.** R2 ran 30 fights per scenario per class; per-class WR has ~σ ≈ 0.09 sampling noise. Should hypothesis tests use point estimates or confidence intervals? Gamora's call.

3. **Mob spread randomization assumption.** R2 spawn positions are fixed; counterfactual could assume randomization. Default: use empirical R2 hits-per-cast (treats fixed spawn as canonical); document if departing.

4. **Boss-with-adds scenario complexity.** Boss_with_adds has 1 boss + 2 elite adds. Counterfactual treats this as "boss tier" but the adds are technically a hybrid. Gamora may choose to (a) treat the scenario WR as boss-tier proxy directly, or (b) decompose into boss-only DPS analysis subtracting add damage. Both defensible; document choice.

5. **Cross-tier modifier solution.** If no single M\* satisfies both swarm AND boss tier targets, report the failure honestly. Document the M\* that minimizes total per-tier deviation as the "best-effort" landing.

6. **Per-archetype patterns.** Mage/caster/controller archetypes have different geometry distributions per `_AOE_SHARES`. Aggregate results by archetype if patterns emerge.

---

## § 8 — Activation gate

**FIRES IMMEDIATELY** upon knight-rider session activation. No upstream dependency. The data is on disk; the methodology is laid out; gamora can begin immediately.

If knight-rider has other dispatches queued (Option A HELD, etc.), this one **does not block them**. They can run in parallel. This dispatch's findings INFORM the Option A decision (and others) but don't gate Option A's firing if Matt approves Option A independently.

---

## § 9 — Authority + autonomous-operation framing

**Authored under gandalf design-stewardship.** Per autonomous-operation protocol § 4.0:

- Specialist L1 in-seam decisions: gamora owns methodology choices (sigmoid fit, variance handling, assumption documentation) per § 6 open questions
- Cross-seam L2 via knight-rider: not applicable for this dispatch (math-only; no cross-seam coordination required)
- Gandalf L2-equivalent on cross-cutting design: gandalf is available for consultation on Hypothesis 1 / Hypothesis 2 framing if gamora wants design input mid-investigation
- Matt re-entry: not required; this is autonomous-operation work. Matt re-enters at his discretionary wind-down

**Decisions-log entry:** gamora may file an entry at `reincarnated-engine/design/decisions/decisions-log.md` at completion if the findings are dispositive. Knight-rider routes per ADR-002.

---

## § 10 — Why this matters (motivation summary for gamora)

Matt's architectural critique landed this evening in conversation:

> *"If the goal of the gauntlet is to tune the classes to ARPG balanced, then simulating with a 'false' 8x pack proxy and non-spatial gauntlet but yet gating on the actual ARPG true pack, true spatial gauntlet seems counterproductive."*

The critique is sharp. The engine currently:
- **TUNES** classes against 1D PackProxy gauntlet (×8 AOE multiplier; non-spatial; approximation)
- **GATES** classes against R2 spatial sub-gauntlet (8 actual entities; geometry-aware; reality)

This structural mismatch may be the underlying cause of the engine-rebuild boss-collapse diagnosis. The kit-redesign queue (30-40 broken classes), the AOE-skew architectural finding, the Option A floor widening, the R1 disposition-3 calibration that couldn't move boss WR — these may all be downstream symptoms of measuring against the wrong gauntlet.

**This dispatch tests whether that critique is empirically supported.** No code changes. No new sims. Just analytical math against existing telemetry to derive what convergence WOULD have produced under R2 instead of 1D.

If Matt's critique is right, this resolves the entire boss-collapse pathology without architectural surgery. If it's not right, we have hard evidence that the catalogue genuinely needs kit-redesign queue work and Option A landing.

**Discipline #1 — math-before-code.** The math costs ~4-8 gamora hours. The code (R2-as-convergence-target implementation) would cost 2-4 weeks. Doing the math first is the discipline.

---

## § 11 — Cross-references

- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — the 5-axis gap diagnosis that motivated engine-rebuild
- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` — the kit-redesign queue this experiment may invalidate
- `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` — the S1 arc + Option A motivation
- `agentic_orchestration/dispatches/HELD-2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` — Option A HELD dispatch (not gated on this experiment but informed by it)
- `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` — gandalf's comprehensive run review with decision tree
- `output/R2-sprint-2026-05-19/` — the existing R2 spatial sub-gauntlet telemetry (the data this experiment analyzes)
- `output/R1-class-retune-2026-05-19/` — the existing 1D-converged modifier data
- `output/R1-baseline-measurement-2026-05-19/` — the pre-engine-rebuild per-tier WR baseline

---

*Filed 2026-05-19 by gandalf, per Matt directive. Math-before-code in the spirit of Discipline #1. The architectural critique is sharp; the math resolves whether it's correct; the engine waits for the data to speak. Mithrandir signs the dispatch.*

---

## Completion record

**Phase:** A (methodology only)  
**Completed:** 2026-05-19  
**By:** gamora  
**Methodology doc:** `reincarnated-engine/design/working-agreement/r2-st-counterfactual-methodology-2026-05-19.md`

### Phase A outcome: COMPLETE with critical blockers identified

**Executed:**
- All 5 input files verified on disk (§ 1)
- 51 classes extracted: R1 modifier + per-tier WR + skill composition (§ 2)
- DPS-to-WR sigmoid calibration assessed: NOT POSSIBLE from available data (§ 3)
- Napkin assumptions replaced with empirical data where feasible (§ 4)
- All 4 methodology open questions resolved under L1 authority (§ 5)
- Phase B readiness assessed with blockers documented (§ 6)

**Critical finding (empirical, not methodological):**  
R2 `boss_with_adds_wr = 0.000` for all 51 classes. This replicates R1 1D `boss_wr = 0.000` for all 51 classes. Boss-tier collapse is NOT a 1D PackProxy measurement artifact for this catalogue — it persists in the full R2 spatial context at the same severity. The kit-redesign queue finding (38/51 kit-broken) is corroborated, not undermined, by R2 data.

**Secondary finding (data quality):**  
`d1_swarm_wr` and `d1_boss_wr` fields in R2 per_class_results.json are synthetic zeros (not real 1D WR data). `get_1d_wr_for_class()` reads a list-format `reference_gauntlet.json` expecting a dict, returns 0.0 default for all classes. This field is non-functional and must not be used in downstream analysis.

**Blockers for Phase B:**
1. HIGH: Boss sigmoid cannot be fit (WR=0 universally); Experiment 1 boss M* derivation is blocked
2. MEDIUM: Swarm WR bimodal (0 or 1 only); threshold estimate only, not sigmoid slope
3. LOW: Per-geometry hit_fraction not in per_class_results.json (in telemetry DB only)

**Phase B is viable for Experiment 2 (ST multiplier sweep)** using R1 1D per-tier WR + linearization model.  
**Phase B Experiment 1 requires methodology reframe** per § 6.3 of methodology doc.

**Routing:** Methodology doc → gandalf review → Phase B authorization if approved.

---

## Completion record — Phase B.2 (R2 modifier sweep — proper H1 test)

**Phase:** B.2 (multi-modifier R2 sweep per knight-rider amendment § 8.3 + Matt directive)
**Completed:** 2026-05-19
**By:** gamora
**Math note:** `reincarnated-engine/design/working-agreement/r2-modifier-sweep-phase-b2-2026-05-19.md`
**Sim output:** `reincarnated-engine/output/R2-modifier-sweep-2026-05-19/`
**Script:** `reincarnated-engine/scripts/r2_modifier_sweep_phase_b2.py`

### Phase B.2 outcome: COMPLETE

**Executed:**
- Math note written before simulation (Discipline #1)
- Smoke test: 5 classes × 6 modifiers × 3 scenarios × 5 fights = 450 fights — PASS
- Full sweep: 49 classes × 6 modifiers × 3 scenarios × 30 fights = 26,460 fights
- M* derivation: per-class joint satisfiability computed for all 49 classes
- H1 + H2 hypothesis verdicts produced
- Joint matrix re-evaluated
- AGENT_STATE.md + CHANGELOG updated

**H1 verdict: CANNOT_REJECT_NULL.** 0/49 classes achieve joint M* satisfiability.
**H2 verdict: CONFIRMED.** 49/49 classes unsatisfiable.
**Joint matrix: Row 5 — catalogue has deeper pathology.**

**Key finding (NEW vs Phase A):**
22/49 classes (44.9%) CAN achieve boss kills at modifier ≥ 0.50–2.0. Boss-kill capability is modifier-dependent, not universally absent. However, both WR surfaces (swarm + boss) are binary step functions — the narrow target bands [0.65, 0.80] and [0.30, 0.45] are architecturally unreachable under 30-fight cardinality + current R2 calibration. Joint satisfiability = 0 is a combination of kit-quality pathology (27/49) and binary WR surface structure (22/49).

**Simplification:** Option (b) — R2 simplified damage chain accepted. No modifications to spatial_engine.py.
**No production catalogue changes. No balance_loop code changes. No telemetry DB writes.**

**Routing:** gamora → knight-rider → gandalf for Phase B.2 verdict review + Phase E gate disposition.
