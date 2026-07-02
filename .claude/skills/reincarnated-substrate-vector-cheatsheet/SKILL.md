---
name: reincarnated-substrate-vector-cheatsheet
description: Use this skill when working on BC axes, substrate-vector queries, axis discovery (P2), multimodal clustering (P3), cluster semantic labeling (P4), cohesion-judge calibration (P5), design-spec-as-math handoffs (gandalf → rocket/elrond/gamora), engine simulation work touching BC measurement, or telemetry/sidecar analysis on BC dimensions. Quick-reference for the 8 BC axes (engagement profile, damage geometry, proxy density, control density, damage tempo, damage amplitude variance, defensive profile, resource economy) with bin counts + bin labels + operational definitions + hybrid archetype cross-axis captures. Total 68,040 cells. Authoritative source remains canonical/reap-die-rise-engine/qd-engine-bc-axes-lock-2026-05-20.md.
version: 0.1.0
---

# reincarnated-substrate-vector-cheatsheet — Cross-cutting Reference Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-substrate-vector-cheatsheet` (per doc 38 § 4 step 2 + Skill Creator pass).

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring; primary BC-axes designer)
**Authoritative source:** `canonical/reap-die-rise-engine/qd-engine-bc-axes-lock-2026-05-20.md` (8-axis locked operational specification)
**Pattern:** universal quick-reference; load when design-spec-as-math, dispatch authoring, or methodology work touches BC axes
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-hive-mind-protocol`; `reincarnated-critique-pair-gate-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** quick-reference condensation of the 8 Behavior Characteristic (BC) axes. Bin counts, bin labels, operational definitions, total cell count. Loaded by agents working on substrate-vector queries, axis discovery (P2), multimodal clustering (P3), cohesion-judge calibration (P5), design-spec-as-math handoffs, dispatch authoring touching substrate.

**IS NOT:** the substantive lock spec (that's `qd-engine-bc-axes-lock-2026-05-20.md`; ALWAYS the canonical source). NOT the multi-dim convergence algorithm spec (that's `multi-dim-convergence-algorithm-2026-05-21.md`). NOT the substrate-as-cohesion architecture (`substrate-design-supplement-2026-05-21.md`). NOT a replacement for reading the source when authoring substrate-touching work.

---

## 1. The 8 BC axes — quick-reference

| # | Axis | Bins | Bin labels |
|---|---|---|---|
| 1 | **Engagement profile** | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | **Damage geometry** | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 2A | **Proxy density** | 3 | solo / proxy-light / proxy-heavy |
| 2B | **Control density** | 3 | damage-pure / mixed / control-pure |
| 3A | **Damage tempo** | 3 | low / medium / high |
| 3B | **Damage amplitude variance** | 3 | flat / variable / spiky |
| 4 | **Defensive profile** | 4 | tank / mitigator / dodger / glass |
| 5 | **Resource economy** | 7 | HP-economy / charge-stack / damage-taken-converts / starved / overflow / generator-spender / steady |

**Total cells:** 6 × 5 × 3 × 3 × 3 × 3 × 4 × 7 = **68,040**

**Coverage:** ~1.5% occupancy at 1,000-season archive (sparse but functional per QD research at 8-10 axes).

---

## 2. Operational definitions (per-axis quick form)

### Axis 1 — Engagement profile (composite: range × mobility)
- **Range component:** mean weighted skill range, weighted by skill damage contribution. Thresholds: melee ≤ 3.0 tiles; mid 3.0–8.0; ranged > 8.0
- **Mobility component:** total movement-skill displacement per minute fight time. Threshold: high ≥ 30 tiles/min from movement skills; low < 30

### Axis 2 — Damage geometry
- Per-skill geometry tags; aggregated by damage contribution
- Bins: single-target (one entity per cast); small-AOE (radius ≤ 3); large-AOE (radius > 3); chain (per-target chain); multi-spawn (proxy or summon volume)

### Axis 2A — Proxy density
- Count of active proxies/minions/totems during typical combat
- Bins: solo (0 proxies); proxy-light (1-3); proxy-heavy (≥ 4)

### Axis 2B — Control density
- Ratio of control-effect uptime to damage-uptime
- Bins: damage-pure (control < 20%); mixed (20-60%); control-pure (> 60%)

### Axis 3A — Damage tempo
- Hits-per-second (damage-event rate) across kit
- Bins: low (< 2 events/sec); medium (2–6); high (> 6)

### Axis 3B — Damage amplitude variance
- Coefficient of variation across damage instances
- Bins: flat (CV < 0.3); variable (CV 0.3–0.7); spiky (CV ≥ 0.7)

### Axis 4 — Defensive profile
- Composite of HP buffer / DR / dodge-chance / iframe-uptime
- Bins: tank (high HP + DR); mitigator (high DR, moderate HP); dodger (high dodge + iframe); glass (low all)

### Axis 5 — Resource economy
- Resource-flow shape
- Bins: HP-economy (cost-life kits); charge-stack (stacking-resource kits); damage-taken-converts (rage/CWDT); starved (resource-limited); overflow (resource-abundant); generator-spender (two-resource); steady (single-resource, continuous flow)

---

## 3. Hybrid archetypes (cross-axis cell capture)

Hybrid archetypes captured by cross-axis cell-address rather than dedicated bins:

| Archetype | Axis combination |
|---|---|
| **Absorber** (Energy Shield caster) | Axis 4 (mitigator) × Axis 5 (overflow or HP-economy) |
| **Regenerator** (Werebear, Jungle Fortitude) | Axis 4 (tank) × Axis 5 (HP-economy or steady) |
| **Thorns** (D3 Crusader thorns) | Axis 2 (single-target or chain) × Axis 4 (tank) |
| **Reflection** (player-side reflect) | Axis 2 (single-target) × Axis 4 (mitigator) |
| **Self-harmer** (Blood Magic) | Axis 5 (HP-economy) × Axis 4 (any) |
| **Mind-control / charm** | Axis 2A (proxy-light or proxy-heavy via charmed) × Axis 2B (control-pure) |
| **Damage-taken-converts** (CWDT, berserker rage-on-hit) | Axis 5 (damage-taken-converts bin) |
| **Charge-stack** (PoE Frenzy stacker) | Axis 5 (charge-stack bin) × Axis 3A (variable per charge state) |
| **Charge-up-and-release** (PoE Charged Dash, bow-draw) | Axis 3A (low tempo) × Axis 3B (spiky variance) |

---

## 4. When to load this skill

| Trigger | Load |
|---|---|
| Authoring a dispatch touching substrate queries | Always |
| P2 axis discovery work (statistical methodology) | Always |
| P3 multimodal clustering work | Always |
| P4 cluster semantic labeling | Always |
| P5 cohesion-judge calibration | Always |
| Design-spec-as-math handoff (gandalf → rocket/elrond) | Always |
| Engine simulation work touching BC measurement | Always |
| Telemetry/sidecar analysis on BC dimensions | Always |
| Routine work not touching BC | Optional |

---

## 5. Companion architecture

The 8-axis BC archive is one of three archive systems:

| Archive | Owner | What lives there |
|---|---|---|
| **Mechanical BC** (this cheatsheet) | gandalf | Simulator-measurable kit identity dimensions |
| **Cohesion BC** | gandalf | LLM-judge-measured thematic coherence (LUCB1 / information bottleneck) |
| **Visual BC** | galadriel | CV-pipeline-measured visual similarity |

All three use the same MAP-Elites machinery; different judges; feed independently into profile-specific assembly.

---

## 6. Substrate dependencies + scope

**Mechanical BC archive depends on:**
- Skill metadata: `movement_displacement_per_cast`, geometry tags, control-effect classifications, resource-type flags
- Sim telemetry: per-skill damage attribution, hit timing, control-effect uptime, resource consumption
- Some bins are SIM-DEFERRED (e.g., charge-stack, damage-taken-converts) pending engine extensions per § 5 of source doc

**Out of scope for this cheatsheet** (consult source docs):
- Discovered axes from P2 axis discovery (those EMERGE from the substrate; this is the PRE-IMPOSED-axis-archive)
- Multi-dim convergence algorithm (consult `multi-dim-convergence-algorithm-2026-05-21.md`)
- Cohesion BC archive details
- Visual BC archive details

---

## 7. Discipline cross-reference

When working with BC axes:
- **Discipline #1** — math-before-code on measurement methodology
- **Discipline #11** — empirical inspection of bin assignments on sample weapons / kits
- **Discipline #17** — calibration-sweep on threshold values
- **Discipline #18** — methodology-before-execution at P2/P3 math hotspots when DISCOVERING axes (vs the locked PRE-IMPOSED 8 axes here)

---

## 8. Update protocol for this skill

This skill evolves when:
- BC axes lock spec amends (axis added/removed/bin changes)
- New hybrid archetype patterns surface (extend § 3)
- Companion-archive details change
- Measurement methodology amendments land

Authored / maintained by **gandalf** (cross-cutting Stream 3 owner + primary BC-axes designer).

**Reconciliation log:**
- **2026-06-13 (jack-ryan):** § 2 Axis 3A + Axis 3B bin edges corrected to match the LOCKED source (`qd-engine-bc-axes-lock-2026-05-20.md` § 3.5 / § 3.6). Cheatsheet carried stale numbers: Axis 3B CV edges read 0.2/0.6 → corrected to lock's **0.3/0.7** (flat CV<0.3 / variable 0.3–0.7 / spiky CV≥0.7); Axis 3A tempo medium read 2–8 → corrected to lock's **2–6** (low <2 / medium 2–6 / high >6). Drift surfaced by gamora's BC-measurement math note + star-lord; gandalf confirmed the lock is authoritative and routed the reconciliation. No lock change — the cheatsheet was the divergent copy.

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author)
**For:** the universal quick-reference for the 8 BC axes (bin counts, labels, operational definitions, hybrid archetype cross-axis captures, total 68,040 cells). Authoritative source for full operational spec remains `canonical/reap-die-rise-engine/qd-engine-bc-axes-lock-2026-05-20.md`. Loaded by agents working on substrate-vector queries, axis discovery, clustering, cohesion-judge calibration, design-spec-as-math handoffs.
