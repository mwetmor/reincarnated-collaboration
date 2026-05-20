# QD-Engine End-to-End Workflow

**Status:** CANONICAL — architectural workflow post substrate-as-cohesion-only recommitment 2026-05-21
**Author:** gandalf
**Companions:**
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` (vision)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (operational 8-axis spec)
- `canonical/story/substrate-design-supplement-2026-05-21.md` (substrate-as-cohesion architecture)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` (execution plan)

---

## 0. TL;DR

The QD-engine workflow operates in **8 phases** from archive-state inspection to final shipped content. The architectural recommitment 2026-05-21 establishes that **mechanical generation is substrate-agnostic + BC-target-driven; substrate/element/theme identity coalesces post-generation in the cohesion phase.** This document maps every phase with its inputs, actions, outputs, and expected outcomes.

**Phases:**

| Phase | Name | Owner seam | What it does |
|---|---|---|---|
| 1 | Archive State Inspection | gamora | Identify sparse BC cells |
| 2 | Generation (BC-Target-Driven) | rocket | Compose mechanical kit for target cell |
| 3 | Convergence + Measurement | gamora | Run sim; measure 8-axis BC coordinates |
| 4 | Mechanical Archive Insertion | gamora | Pareto / crowding / Mahalanobis gate insertion |
| 5 | Cohesion Coalescence | gandalf (cohesion) / rocket (LLM call) | Assign substrate/element/theme post-generation |
| 6 | Visual Coalescence | galadriel | CV-pipeline visual identity assignment |
| 7 | Joint-Gate Evaluation | gandalf + jack-ryan + Matt | Discipline #18 mechanical AND cohesion AND visual pass |
| 8 | Profile Assembly + Export | rocket + star-lord | Filter by profile config; format and ship |

---

## 1. The full workflow — visual flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                    PHASE 1 — ARCHIVE STATE INSPECTION                  │
│  Input:  current mechanical-BC archive state                            │
│  Action: identify sparse cells; compute novelty + diversity needs       │
│  Output: BC-target queue (cells to fill, ranked by priority)            │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    PHASE 2 — GENERATION (BC-TARGET-DRIVEN)             │
│  Input:  BC-target coordinate [Axis1..Axis5 bin assignments]            │
│  Action: compose mechanical kit (skills + gear + traits) targeting BC   │
│          ┌─ substrate-AGNOSTIC mechanic pool                            │
│          ├─ role-shape constraints (damage/control/support/hybrid)      │
│          └─ BC-target as composition objective                          │
│  Output: candidate kit composition (substrate-blind)                    │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│              PHASE 3 — CONVERGENCE + MECHANICAL MEASUREMENT            │
│  Input:  candidate kit composition                                      │
│  Action: run simulation; converge modifier; measure 8 BC axes           │
│          ┌─ Axis 1 — Engagement profile (range × mobility)              │
│          ├─ Axis 2 — Damage geometry (single/AOE/chain/multi-spawn)     │
│          ├─ Axis 2A — Proxy density                                     │
│          ├─ Axis 2B — Control density                                   │
│          ├─ Axis 3A — Damage tempo                                      │
│          ├─ Axis 3B — Damage amplitude variance                         │
│          ├─ Axis 4 — Defensive profile                                  │
│          └─ Axis 5 — Resource economy                                   │
│  Output: kit + 8-axis BC coordinate + per-tier WR + convergence data    │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  PHASE 4 — MECHANICAL ARCHIVE INSERTION                │
│  Input:  kit + 8-axis BC coordinate                                     │
│  Action: math gates determine archive disposition                       │
│          ┌─ Pareto dominance check                                      │
│          ├─ Crowding distance / hypervolume contribution                │
│          ├─ Mahalanobis distance (duplicate detection)                  │
│          ├─ Information gain (KL) for novelty score                     │
│          └─ Eviction rules if cell at capacity                          │
│  Output: kit ACCEPTED (in archive) or REJECTED                          │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │ (if ACCEPTED)
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  PHASE 5 — COHESION COALESCENCE                        │
│  Input:  accepted kit + mechanical-BC coordinate                        │
│  Action: LLM cohesion-judge assigns thematic identity                   │
│          ┌─ analyze mechanical signature (BC profile)                   │
│          ├─ infer substrate-thematic fit (shadow/holy/physical/etc.)    │
│          ├─ infer element-thematic fit (fire/water/earth/...)           │
│          ├─ LUCB1 best-arm-identification across theme candidates       │
│          └─ commit theme + flavor (name, description, lore)             │
│  Output: kit + cohesion-BC coordinate (substrate + element + theme)     │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  PHASE 6 — VISUAL COALESCENCE                          │
│  Input:  kit + cohesion-BC coordinate                                   │
│  Action: galadriel CV pipeline assigns visual identity                  │
│          ┌─ match cohesion theme to VFX library                         │
│          ├─ assign visual style register compliance score               │
│          ├─ generate or select 3D model (via ChatGPT→Meshy→Mixamo)      │
│          └─ apply VFX to rig anchor points                              │
│  Output: kit + visual-BC coordinate (style/color/silhouette/etc.)       │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│              PHASE 7 — JOINT-GATE EVALUATION (Discipline #18)          │
│  Input:  kit + mechanical-BC + cohesion-BC + visual-BC coordinates      │
│  Action: ALL three layers must pass joint-gate                          │
│          ┌─ mechanical-BC pass (per-tier WR within contract)            │
│          ├─ cohesion-BC pass (thematic coherence ≥ threshold)           │
│          ├─ visual-BC pass (style register compliance ≥ threshold)      │
│          └─ profile-specific gate (per active profile config)           │
│  Output: kit SHIPPED-WORTHY or HELD                                     │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │ (if SHIPPED-WORTHY)
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│              PHASE 8 — PROFILE ASSEMBLY + EXPORT                       │
│  Input:  ship-worthy kits + active profile config (A/B/C/D)             │
│  Action: assemble + format + export per profile                         │
│          ┌─ Profile A (Reincarnated) — coreset for Phase 0 ship         │
│          ├─ Profile B (B2B SaaS) — customer-curated subset              │
│          ├─ Profile C (mod-pack) — submodular best-K packaging          │
│          └─ Profile D (solo-dev) — dev-customized subset                │
│  Output: shippable content packs in profile-appropriate formats         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase-by-phase detail

### Phase 1 — Archive State Inspection

**Owner:** gamora (engine simulation seam)
**Frequency:** Continuous during active generation campaigns

**Inputs:**
- Current mechanical-BC archive state (filled cells + their occupants)
- Profile-specific targeting hints (e.g., Profile A wants reduced-cell-space; Profile B has customer-specific BC preferences)
- Novelty / diversity metrics from prior generation cycles

**Engine actions:**
1. Enumerate cells in 8-axis archive (68,040 total cells)
2. Compute per-cell occupancy (0..N entries; capacity ~5-10 per cell)
3. Identify sparse regions via crowding distance + hypervolume contribution analysis
4. Rank cells by *fill priority*:
   - High priority: empty cells in dense-neighborhood regions (diversity exploration)
   - High priority: cells with low-quality entries that could be replaced
   - Lower priority: already-saturated cells
5. Apply profile filter (Profile A excludes deferred bins → reduced-cell-space of 25,920)
6. Generate BC-target queue (top N candidates to attempt)

**Outputs:**
- Ordered BC-target queue: `[(cell_coord_1, priority_1), (cell_coord_2, priority_2), ...]`
- Each entry: 8-tuple `(eng_bin, geo_bin, proxy_bin, ctrl_bin, tempo_bin, var_bin, def_bin, econ_bin)`

**Expected outcome:**
- Generation engine has clear targets to attempt
- No wasted generation on already-saturated cells
- Profile A's reduced-cell-space respected (deferred bins not targeted pre-P4)

**Math gate engagement:**
- Pareto / crowding / hypervolume reads archive state (read-only at this phase)
- No archive mutation here

---

### Phase 2 — Generation (BC-Target-Driven)

**Owner:** rocket (engine generation seam)
**Frequency:** Per BC-target attempt

**Inputs:**
- Target BC coordinate (from Phase 1)
- **Substrate-agnostic mechanic pool** (the master mechanic library; no substrate-tagging)
- Role-shape registry (damage / control / support / hybrid role definitions)
- Generation seed (RNG state for reproducibility)

**Engine actions:**

1. **Decompose BC-target into composition objectives:**
   - Engagement bin → range + mobility constraints on skills
   - Geometry bin → damage delivery shape requirements
   - Proxy bin → proxy entity count constraint
   - Control bin → CC budget fraction
   - Tempo bin → damage event rate target
   - Variance bin → per-event magnitude variance target
   - Defensive bin → eHP and avoidance requirements
   - Economy bin → resource pattern target

2. **Compose kit from mechanic pool to satisfy objectives:**
   - Pick skills matching range / geometry / tempo objectives
   - Pick defensive layer matching defensive bin requirements
   - Pick resource mechanism matching economy bin requirements
   - Mix-and-match across mechanic categories (no substrate-tagging influences picks)

3. **Apply role-shape constraints:**
   - Damage role → skills ≥ X damage budget
   - Control role → skills ≥ Y control budget
   - Hybrid → mixed budget

4. **Generate kit candidate:** complete skill set + gear + traits ready for simulation

**Critical principle:** **Substrate is NOT an input to this phase.** The mechanic pool is unified; mechanics are not pre-tagged with substrate identity. Generation is purely BC-target-driven.

**Outputs:**
- Candidate kit composition: `{skills: [...], gear: [...], traits: [...], modifier_init: 1.0}`
- Generation telemetry (which mechanics were picked, why)

**Expected outcome:**
- Kit composition targets the BC-cell address mechanically
- No archetype-lock-in; same BC-target can be approached via different mechanic combinations
- Cross-mechanic hybrids natural and frequent

**Hybrid examples (now natural, not exceptional):**
- Tank-eHP + warcry-amplification + high-damage = "vampiric warrior" mechanical signature
- Dodger-evasion + HP-cost + chain-damage = "shadow blade" mechanical signature
- Mitigator-shield + multi-spawn-damage + steady-economy = "aura caster" mechanical signature

(Themes assigned in Phase 5; mechanics generated agnostic to theme in Phase 2)

---

### Phase 3 — Convergence + Mechanical Measurement

**Owner:** gamora (engine simulation seam)
**Frequency:** Per candidate kit

**Inputs:**
- Candidate kit composition (from Phase 2)
- Per-tier WR targets (swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini-boss 0.35-0.55; boss 0.30-0.45)
- Telemetry instrumentation (per-tick resource pool; per-event source-tagged damage; etc.)

**Engine actions:**

1. **Run simulation across all 5 tiers** (swarm / magic / elite / mini-boss / boss)
2. **Modifier search:**
   - Adjust scalar (or multi-dim) modifier to converge per-tier WR within targets
   - Stop when convergence criteria met OR max iterations exceeded
3. **Capture telemetry per fight:**
   - Damage events with source attribution (cast / reactive / proxy / environmental)
   - Resource pool over time
   - HoT recovery, shield-pool tracking, mitigation events
   - Movement-skill displacement
   - Proxy entity lifecycle
   - Hit-by-hit damage application (for avoidance_rate)
4. **Compute 8 BC axes from convergence telemetry:**
   - **Axis 1 (Engagement):** mean weighted skill range + movement-displacement per minute
   - **Axis 2 (Geometry):** damage-weighted argmax over per-skill geometry (including reactive sources)
   - **Axis 2A (Proxy density):** mean count of player-allied proxy entities (origin-agnostic)
   - **Axis 2B (Control density):** CC-tagged skill weights / total skill weights
   - **Axis 3A (Tempo):** mean damage events per second
   - **Axis 3B (Variance):** CV of per-event damage magnitudes
   - **Axis 4 (Defensive):** eHP_effective_ratio + avoidance_rate
   - **Axis 5 (Economy):** mean_resource_fraction + variance + hp_cost_fraction + charge_stack_check + damage_to_resource_check

**Outputs:**
- Kit + per-tier WR results
- Kit + 8-axis BC coordinate (each axis → assigned bin)
- Convergence metadata (modifier found, iterations used, smoke-test vs full)

**Expected outcome:**
- Kit either converges within per-tier WR contract OR fails convergence
- BC coordinate is stable + measurable from telemetry (Discipline #11: equilibrium-state-conditioned)
- Discipline #17 calibration validates threshold values

**Math gate engagement:**
- Discipline #17 empirical calibration (thresholds validated against reference archetypes in P2 W2.10 + P7 W7.3)
- Discipline #11 elaboration (equilibrium-state-conditioned signals only)

**Failure handling:**
- If convergence fails → kit rejected at this phase; no archive insertion
- If convergence succeeds → proceed to Phase 4

---

### Phase 4 — Mechanical Archive Insertion

**Owner:** gamora (archive logic)
**Frequency:** Per converged kit

**Inputs:**
- Kit + 8-axis BC coordinate (from Phase 3)
- Current archive state at that BC cell
- Pareto / crowding / Mahalanobis / hypervolume / KL parameters

**Engine actions:**

1. **Identify target cell** from BC coordinate
2. **Pareto dominance check** vs existing entries in cell:
   - If new entry dominates ≥1 existing → existing dominated entries are eviction candidates
   - If new entry is dominated by ≥1 existing → reject as inferior
   - If non-dominated → consider for insertion
3. **Crowding distance / hypervolume contribution computation:**
   - Score new entry's contribution to diversity within cell + neighborhood
   - High contribution = more valuable
4. **Mahalanobis distance vs cell entries:**
   - If distance < ε (duplicate threshold) → reject as duplicate
   - Otherwise → unique entry candidate
5. **KL divergence / information gain:**
   - Score new entry's novelty contribution to archive distribution
6. **Cell capacity check:**
   - If cell at capacity → evict lowest-hypervolume-contribution entry
   - If cell has room → insert directly
7. **Insertion decision:** ACCEPTED, REJECTED-DUPLICATE, REJECTED-DOMINATED, REJECTED-CAPACITY

**Outputs:**
- Archive disposition: ACCEPTED / REJECTED-{reason}
- If accepted: archive state mutated (new entry added; possibly evicted entry removed)

**Expected outcome:**
- Archive grows in diversity over time
- Sparse cells fill (priority targets from Phase 1)
- Dominated entries replaced; duplicates excluded
- Math gates produce stable signal at 1.5% coverage (8D archive)

**Discipline engagement:**
- Discipline #7 (capture decision telemetry) — every insertion/rejection logged with reason
- Discipline #2 (smoke-test vs full-regen) — math gates run on smoke-test telemetry where appropriate

---

### Phase 5 — Cohesion Coalescence

**Owner:** gandalf (cohesion-BC spec + judge prompts) + rocket (LLM integration) + star-lord (LUCB1)
**Frequency:** Per archive-accepted kit (Phase 4 → Phase 5 pipeline)

**Inputs:**
- Accepted kit + mechanical-BC coordinate (8-axis)
- Substrate identity reference docs (cohesion-layer thematic prompts; NOT mechanic constraints)
- Element thematic library
- Cohesion-BC archive state

**Engine actions:**

1. **Mechanical signature presentation:**
   - Format kit's BC coordinate + skill list as prompt input
   - "This kit has: close-fast engagement, large-AOE geometry, high-tempo, spiky variance, tank defense, HP-economy. Skills: [...]. Mechanics: [...]."

2. **LLM cohesion-judge inference:**
   - Substrate-thematic fit: which substrate (shadow / holy / physical / fire / water / earth / wind / lightning / etc.) best matches this mechanical signature?
   - Element-thematic fit: which canonical element resonates with these mechanics?
   - Archetype-recognition: which ARPG-canonical archetype does this evoke? (D2 Hammerdin / D3 Crusader / PoE Cyclone Slayer / etc.)
   - Flavor: name, description, lore-hook

3. **LUCB1 best-arm identification across theme candidates:**
   - N theme candidates evaluated
   - Confidence bounds tracked per candidate
   - Stop when best candidate identified with PAC bounds (δ = 0.05)

4. **Cohesion-BC coordinate assignment:**
   - Substrate label
   - Element label
   - Theme / archetype fit score
   - Flavor signature

**Critical principle:** **Substrate identity ONLY assigned here, never as generation input.** The substrate label "shadow" is what the cohesion-judge calls a kit whose mechanical signature happens to match shadow-thematic profile (HP-economy, trade-off mechanics, etc.). The kit was NOT generated as shadow — it was generated as mechanical-BC-target, and earned the shadow label at coalescence.

**Outputs:**
- Kit + cohesion-BC coordinate
- Theme commitment with PAC-bound confidence
- Cohesion-judge metadata (which mechanical features drove which theme attribution)

**Expected outcome:**
- Substrate / element / theme assigned post-hoc based on mechanical evidence
- Cohesion-BC archive populates with thematic diversity
- IDC (Information-Deferred-to-Coalescence) principle in operation

**Hybrid kit handling:**
- Kit with vampiric (shadow) + warrior (physical) mechanics → cohesion-judge may pick shadow-physical hybrid theme
- Cross-substrate hybrid themes are natural (D2 Necromancer Bone Spear = shadow + physical; this is the model)

---

### Phase 6 — Visual Coalescence

**Owner:** galadriel (visual perception + style register)
**Frequency:** Per cohesion-themed kit

**Inputs:**
- Kit + cohesion-BC coordinate (theme + substrate + element)
- VFX library (Unity Asset Store packs + free baselines + future Mixamo-animated 3D models)
- Style register lock (visual coherence target — pixel / hand-drawn / vector / HD raster / hybrid)

**Engine actions:**

1. **Theme-to-VFX matching:**
   - Cohesion theme (shadow + close-fast + tank) → search VFX library for shadow-aligned visual assets
   - Element-thematic VFX selection (fire effects for fire theme; ice for water; etc.)

2. **Meshy 6 animation matching** (3D production via reincarnated-game/; Meshy 6 supersedes Mixamo per 2026-05-21 research):
   - For humanoid characters: Meshy 6 Animation API (500+ game-ready motions integrated with Rigging API)
   - For non-humanoid creatures: Claude+Blender custom rigging fallback
   - Pick animations matching engagement profile (close-fast → fast-melee animations; ranged-slow → stationary-cast animations)
   - Anchor VFX to Meshy-standard rig points (hands / weapon / body / ground)

3. **Visual style register compliance:**
   - CV pipeline scores asset coherence with locked style register
   - Reject assets that drift the visual style

4. **Visual-BC coordinate computation:**
   - Color profile dimension
   - Silhouette profile dimension
   - VFX signature dimension
   - Other galadriel-defined visual BC dimensions

**Outputs:**
- Kit + visual-BC coordinate
- Selected visual assets (VFX + animations + 3D model reference)
- Visual style register compliance score

**Expected outcome:**
- Kit has full visual identity matching its cohesion theme
- Style register coherence preserved
- Two output paths supported: Pixi.js 2D (reincarnated-demo) + Unity 3D (reincarnated-game)

**Dual-render handling:**
- Pixi.js 2D path: sprite-based visualization; if exact sprite missing, accept fallback (per Matt 2026-05-21)
- Unity 3D path: full ChatGPT → Meshy → Mixamo → VFX pipeline; archetypes get bespoke 3D production over time

---

### Phase 7 — Joint-Gate Evaluation (Discipline #18)

**Owner:** gandalf + jack-ryan + Matt (for ratification)
**Frequency:** Per fully-coordinated kit

**Inputs:**
- Kit + mechanical-BC coordinate
- Kit + cohesion-BC coordinate
- Kit + visual-BC coordinate
- Profile-specific gate thresholds (Profile A may have different thresholds than Profile B)

**Engine actions:**

1. **Mechanical-BC gate:**
   - Per-tier WR within contract bounds
   - BC coordinate stable + reproducible
   - Archive insertion successful

2. **Cohesion-BC gate:**
   - Thematic coherence score ≥ threshold
   - Theme commitment with PAC bounds
   - No thematic drift (shadow-kit doesn't accidentally get holy theme)

3. **Visual-BC gate:**
   - Style register compliance ≥ threshold
   - VFX coherent with theme
   - Galadriel approval signal

4. **Joint-gate determination:** ALL three layers must pass
   - PASS → kit is SHIPPED-WORTHY
   - FAIL on any layer → kit is HELD; routed back to relevant phase for re-evaluation or excluded

5. **Profile-specific override:** profiles can adjust gate thresholds (Profile B customer may relax visual gate if focused on mechanical-cohesion only)

**Outputs:**
- Joint-gate verdict: SHIPPED-WORTHY / HELD-{reason}
- Per-layer verdict telemetry (which gate failed if HELD)

**Expected outcome:**
- Only kits passing ALL three layers ship
- Joint-gate becomes the canonical ship criterion
- Discipline #18 ratified in P5 W5.6 of QD-rebuild

---

### Phase 8 — Profile Assembly + Export

**Owner:** rocket (profile filtering) + star-lord (export pipeline)
**Frequency:** Per shipment campaign

**Inputs:**
- Pool of SHIPPED-WORTHY kits (from Phase 7)
- Active profile config (A / B / C / D)
- Coreset / submodular parameters (per profile)

**Engine actions per profile:**

**Profile A — Reincarnated Phase 0:**
1. Filter shipped-worthy kits → solo-only proxy bin + currently-supported defensive bins + currently-supported economy bins
2. Coreset selection: smallest subset preserving BC coverage
3. Format as Reincarnated season packs
4. Export to reincarnated-engine output + drax demo integration

**Profile B — B2B SaaS:**
1. Apply customer-specific BC preferences (weighted by customer config)
2. Submodular optimization: best K seasons for customer
3. Format as customer-deliverable packs
4. Export to per-customer endpoint

**Profile C — Mod-pack exporter:**
1. Target game/genre customization parameters
2. Filter for genre-aligned BC subsets
3. Format as mod-pack deliverables
4. Export to mod-pack distribution

**Profile D — Solo-dev:**
1. Apply solo-dev BC subset preferences
2. Format as dev-friendly artifact bundles
3. Export to dev-customizable directory

**Outputs:**
- Per-profile shippable content
- Export metadata + provenance tracking

**Expected outcome:**
- Each profile produces appropriate output for its deployment target
- Profile A near-term ship via reduced-cell-space at P3 (~11-16 weeks) or full-cell-space at P4 (~15-22 weeks)
- Other profiles ship when their target customers / mod-makers / devs engage

---

## 3. Cross-phase data flow

```
Phase 1 ─┬─→ Phase 2 (BC-target) ─→ Phase 3 (kit + 8-axis) ─→ Phase 4 (archive ACCEPT/REJECT)
         │                                                            │
         │                                                  (if ACCEPT)
         │                                                            ▼
         │                                                  Phase 5 (cohesion) ─→ Phase 6 (visual)
         │                                                                              │
         │                                                                              ▼
         │                                                                      Phase 7 (joint-gate)
         │                                                                              │
         │                                                                  (if SHIPPED-WORTHY)
         │                                                                              ▼
         │                                                                       Phase 8 (export)
         │                                                                              │
         └──────────────────────────────────────────────────────────────────────────────┘
                                          (archive state feeds back into Phase 1 inspection)
```

**Feedback loops:**
- Phase 1 reads from archive (Phases 4 + 5 + 6 writes)
- Phase 4 may evict entries → Phase 1 re-prioritizes
- Phase 7 HELD verdicts may route back to relevant Phase for retry or exclusion

---

## 4. What's NEW under substrate-as-cohesion-only architecture

Compared to pre-2026-05-21 framing:

| Pre-recommitment | Post-recommitment |
|---|---|
| Substrate identity files constrain mechanic generation | Substrate identity files are cohesion-layer reference docs only |
| Generation per-substrate (water_mage, fire_mage, etc.) | Generation per-BC-target (substrate-agnostic mechanic pool) |
| Substrate mechanic-locked at generation | Substrate label coalesces at Phase 5 cohesion-judge |
| Mechanical and thematic identity coupled | Mechanical and thematic identity decoupled (IDC) |
| 7 substrate-archetype-like identities | 1 unified mechanic pool; 7 thematic labels assignable to any kit by cohesion-judge |

**This recommitment honors:**
- The recompose-hive empirical finding (archetype-lock IS the load-bearing pathology)
- Matt's anti-archetype-lock instinct surfaced 2026-05-21
- The IDC meta-principle (Information-Deferred-to-Coalescence) at full purity
- The architectural test ("does this design choice influence mechanical generation or only thematic coalescence?")

---

## 4.5 Profile flag positioning — where A/B/C/D act in the workflow

**The four profile flags (A Reincarnated / B B2B SaaS / C Mod-pack / D Solo-dev) act at FIVE points in the workflow.** Each touchpoint is explicit; the flag's expected behavior varies by phase.

### Profile-flag touchpoints

```
                ┌─────────── PROFILE FLAG ENTRY (config selected) ───────────┐
                │                                                              │
                ▼                                                              │
PHASE 1 ─→ [TOUCHPOINT 1: BC-target queue filter]                              │
                │                                                              │
                ▼                                                              │
PHASE 2 ─→ generation (substrate-agnostic)                                     │
                │                                                              │
                ▼                                                              │
PHASE 3 ─→ measurement (profile-blind)                                         │
                │                                                              │
                ▼                                                              │
PHASE 4 ─→ archive insertion (profile-blind)                                   │
                │                                                              │
                ▼                                                              │
PHASE 5 ─→ [TOUCHPOINT 2: cohesion theme preferences]                          │
                │                                                              │
                ▼                                                              │
PHASE 6 ─→ [TOUCHPOINT 3: visual style register per profile]                   │
                │                                                              │
                ▼                                                              │
PHASE 7 ─→ [TOUCHPOINT 4: joint-gate thresholds per profile]                   │
                │                                                              │
                ▼                                                              │
PHASE 8 ─→ [TOUCHPOINT 5: assembly + export per profile]                       │
                │                                                              │
                ▼                                                              │
              SHIPPED CONTENT (profile-appropriate format)                     │
```

**Profile-blind phases:** Phases 2, 3, 4 are profile-AGNOSTIC. Generation + measurement + archive insertion operate identically regardless of active profile. This preserves architectural separation: the engine produces a unified archive; profiles consume it differently.

### Touchpoint 1 — Phase 1 BC-target queue filter

**Where the profile flag acts:** Phase 1 generates BC-target queue; profile filter narrows the queue.

| Profile | Behavior at Touchpoint 1 |
|---|---|
| **A — Reincarnated** | Reduced-cell-space pre-P4 (excludes proxy-light/heavy, dodger sub-cases, HP-economy, charge-stack, damage-converts). Operational cells = 25,920. Post-P4: full 68,040. |
| **B — B2B SaaS** | Customer config provides BC weighting (e.g., "customer wants 70% damage-pure / 30% mixed control density"). Filter applies customer-specific bin emphasis. |
| **C — Mod-pack** | Target game/genre customization (e.g., "fire-focused mod-pack" filters to fire-themed cells via cohesion-BC; "PoE-style mod-pack" filters to PoE-archetype-cells). |
| **D — Solo-dev** | Dev-customizable filter; dev specifies which BC cells they're interested in via config UI. |

**Implementation:** profile config provides a `cell_filter(cell_coord) → bool` predicate. Phase 1 applies before ranking by fill priority.

### Touchpoint 2 — Phase 5 cohesion theme preferences

**Where the profile flag acts:** Phase 5 cohesion-judge sees theme candidates; profile may bias selection.

| Profile | Behavior at Touchpoint 2 |
|---|---|
| **A — Reincarnated** | Theme library aligned with Reincarnated narrative arc (substrate identities per Reincarnated lore; spirit guide voice; Earth-Self meta-layer themes). |
| **B — B2B SaaS** | Customer-specified theme library. E.g., customer is making a sci-fi ARPG → "fire" becomes "plasma", "shadow" becomes "void", element labels remapped per customer brand. |
| **C — Mod-pack** | Target game's theme conventions. E.g., PoE mod-pack uses PoE's gem terminology; D2 mod-pack uses D2's class naming. |
| **D — Solo-dev** | Dev provides theme library; dev's IP, dev's flavor. |

**Implementation:** profile config provides `theme_library` and `theme_remapping` parameters to cohesion-judge prompts. LLM call adjusts accordingly. Same mechanical kit can be themed as "Fire Mage" (Profile A), "Plasma Caster" (Profile B sci-fi customer), or "Cinder-walker of the Inner Forge" (Profile C PoE-style mod).

### Touchpoint 3 — Phase 6 visual style register

**Where the profile flag acts:** Phase 6 galadriel CV pipeline; visual asset selection adapts to profile.

| Profile | Behavior at Touchpoint 3 |
|---|---|
| **A — Reincarnated** | Locked visual style register (per galadriel's earlier style decision: hand-drawn / pixel / vector / HD-raster — Matt confirms). Dual-render targets: Pixi.js (reincarnated-demo) + Unity (reincarnated-game). |
| **B — B2B SaaS** | Customer-specified style register. Customer may want realistic HD; another customer wants stylized cartoon. Visual library filters accordingly. |
| **C — Mod-pack** | Target game's visual conventions. PoE mod-pack uses PoE asset style; D2 mod-pack uses D2 asset style. |
| **D — Solo-dev** | Dev-provided style register; dev's asset library. |

**Implementation:** profile config provides `style_register` lock + `visual_library` source. Phase 6 enforces compliance; rejects assets outside profile's style.

### Touchpoint 4 — Phase 7 joint-gate thresholds

**Where the profile flag acts:** Phase 7 Discipline #18 joint-gate; per-profile threshold relaxation.

| Profile | Behavior at Touchpoint 4 |
|---|---|
| **A — Reincarnated** | Strictest joint-gate. All three layers (mechanical + cohesion + visual) must pass with high thresholds. This is the canonical ship gate. |
| **B — B2B SaaS** | Customer-tunable thresholds. Customer may relax visual gate if they're providing their own visual layer; may relax cohesion gate if they're providing their own narrative. |
| **C — Mod-pack** | Target-game's threshold expectations. Mod-pack consumers may accept lower visual fidelity for higher mechanical novelty. |
| **D — Solo-dev** | Dev-customizable thresholds. Solo-dev may relax any gate for prototyping; tighten for shipping. |

**Implementation:** profile config provides per-layer threshold parameters: `mechanical_threshold`, `cohesion_threshold`, `visual_threshold`, plus optional `bypass_gates: [list of layers]`. Joint-gate evaluates per profile.

### Touchpoint 5 — Phase 8 assembly + export

**Where the profile flag acts:** Phase 8 final formatting and shipment.

| Profile | Behavior at Touchpoint 5 |
|---|---|
| **A — Reincarnated** | Coreset selection for Phase 0 ship; format as Reincarnated season packs; export to reincarnated-engine `output/` + drax demo integration (Pixi.js) + Unity asset bundles (reincarnated-game). |
| **B — B2B SaaS** | Submodular optimization: best K seasons for customer per K-budget. Customer-specified export format (JSON / Unity bundle / Unreal asset / custom API endpoint). Per-customer endpoint delivery. |
| **C — Mod-pack** | Submodular best-K packaging; format as mod-pack for target game (e.g., PoE mod-pack format; D2 mod format). Distribution-platform-appropriate (Nexus / mod community / itch.io). |
| **D — Solo-dev** | Dev-friendly artifact bundles (e.g., JSON + asset manifest); export to dev-customizable directory. |

**Implementation:** profile config provides `assembly_strategy` (coreset / submodular / direct) + `export_format` + `export_destination` parameters. Phase 8 dispatches per profile.

### Profile flag implementation pattern (config schema)

Each profile is a YAML config defining behavior at all 5 touchpoints:

```yaml
# profile-A-reincarnated.yaml (example)
name: "Profile A — Reincarnated"

# Touchpoint 1 — BC-target queue filter
cell_filter:
  axis_2A_proxy_density:
    pre_P4: ["solo"]      # exclude proxy-light/proxy-heavy
    post_P4: ["solo", "proxy-light", "proxy-heavy"]
  axis_4_defensive:
    pre_P4: ["tank", "mitigator", "glass", "dodger-evasion-only"]
    post_P4: ["tank", "mitigator", "dodger", "glass"]
  axis_5_economy:
    pre_P4: ["starved", "overflow", "generator-spender", "steady"]
    post_P4: ["all bins"]

# Touchpoint 2 — Cohesion theme library
theme_library: "reincarnated_canonical"
theme_remapping:
  shadow: "shadow"  # no remap; Reincarnated uses canonical element names
  fire: "fire"
  # ...
spirit_guide_voice: "reincarnated_canonical"
narrative_arc: "earth_self_meta_layer"

# Touchpoint 3 — Visual style register
style_register: "[locked by galadriel — see galadriel/style-register.md]"
visual_library:
  pixi_2d: "reincarnated-demo/assets/"
  unity_3d: "reincarnated-game/assets/"
dual_render: true

# Touchpoint 4 — Joint-gate thresholds
mechanical_threshold: 0.85
cohesion_threshold: 0.80
visual_threshold: 0.80
bypass_gates: []  # no bypasses for Profile A

# Touchpoint 5 — Assembly + export
assembly_strategy: "coreset"
coreset_epsilon: 0.10
export_format: "reincarnated_season_pack"
export_destinations:
  - "reincarnated-engine/output/"
  - "reincarnated-demo/season-data/"   # Pixi.js path
  - "reincarnated-game/season-data/"   # Unity path
```

```yaml
# profile-B-b2b-saas.yaml (example schema; per-customer instantiated)
name: "Profile B — B2B SaaS [customer: example-customer-1]"

cell_filter:
  customer_weighting: {axis_2: {large_AOE: 2.0, chain: 1.5}, ...}

theme_library: "customer_provided"
theme_remapping:
  fire: "plasma"
  shadow: "void"
  # ... per customer brand

style_register: "customer_provided_realistic_HD"
visual_library:
  source: "customer_asset_bucket"

mechanical_threshold: 0.85
cohesion_threshold: 0.70  # relaxed; customer provides narrative
visual_threshold: 0.60  # relaxed; customer provides visual layer
bypass_gates: ["visual"]  # customer doesn't need our visual layer

assembly_strategy: "submodular"
submodular_K: 20  # customer wants 20 best seasons
export_format: "customer_api_format"
export_destinations:
  - "customer_endpoint_url"
```

### Profile-flag expected behavior summary

| Aspect | Profile A | Profile B | Profile C | Profile D |
|---|---|---|---|---|
| Cell-space at ship | Reduced→Full (P3→P4) | Customer-defined | Genre-defined | Dev-defined |
| Theme library | Reincarnated canonical | Customer-provided | Target-game-aligned | Dev-provided |
| Style register | Galadriel-locked | Customer-specified | Target-game-aligned | Dev-customizable |
| Joint-gate strictness | Strictest (all 3 layers) | Customer-tunable | Mod-community-defined | Dev-customizable |
| Assembly | Coreset | Submodular K | Submodular K | Direct |
| Export format | Reincarnated season packs | Customer API | Mod-pack distribution format | Dev artifact bundles |
| Render targets | Pixi.js 2D + Unity 3D | Customer-chosen | Target-game's renderer | Dev's renderer |

**Key principle:** profiles configure CONSUMPTION of the unified archive. They DO NOT influence generation (Phase 2). The same archive serves all four profiles via different consumption-side filters.

---

## 5. Phase ownership matrix

| Phase | Primary owner | Secondary owners | Critique-pair |
|---|---|---|---|
| 1 Archive State Inspection | gamora | rocket (BC-target consumption) | jack-ryan reviews algorithmic correctness |
| 2 Generation | rocket | gandalf (substrate-cohesion reference doc author) | gandalf reviews archetype-recognition; jack-ryan reviews regression |
| 3 Convergence + Measurement | gamora | rocket (skill metadata propagation) | gandalf reviews measurement correctness vs ARPG canon |
| 4 Mechanical Archive Insertion | gamora | star-lord (persistence) | jack-ryan reviews math gate implementation |
| 5 Cohesion Coalescence | gandalf | rocket (LLM integration); star-lord (LUCB1) | jack-ryan reviews bias; Matt approves theme prompt library |
| 6 Visual Coalescence | galadriel | drax (rendering); gandalf (style alignment) | gandalf + galadriel joint critique |
| 7 Joint-Gate Evaluation | gandalf + jack-ryan | Matt (ratification) | Discipline #18 ratification gate |
| 8 Profile Assembly + Export | rocket + star-lord | gandalf (per-profile config) | jack-ryan reviews export integrity |

---

## 6. Phase × QD-rebuild Phase mapping

The 8 workflow phases map to the QD-rebuild's 8 execution phases (P0-P7) per protocol:

| Workflow phase | QD-rebuild build phase | When |
|---|---|---|
| Phase 1 Archive State Inspection | P3 (MAP-Elites archive) | ~10-13 weeks in |
| Phase 2 Generation (BC-target) | P0 W0.2 (archetype refactor) + P1 W1.1 (schema) + P2 W2.X (BC tagging) | P0 + P1 + P2 |
| Phase 3 Convergence + Measurement | P2 (BC measurement infrastructure) | ~10-13 weeks in |
| Phase 4 Mechanical Archive Insertion | P3 (MAP-Elites archive) | ~10-13 weeks in |
| Phase 5 Cohesion Coalescence | P5 (theme coalescence) | ~18-27 weeks in |
| Phase 6 Visual Coalescence | P5 (visual-BC) + reincarnated-game Unity init (parallel) | ~18-27 weeks + multi-month Unity |
| Phase 7 Joint-Gate Evaluation | P5 W5.6 (Discipline #18 ratification) | ~18-27 weeks in |
| Phase 8 Profile Assembly + Export | P6 (profile assembly) + P7 (cutover) | ~20-33 weeks in |

---

## 7. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — § 5 math gates; § 6 dependency chain; § 8 engineering roadmap
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis spec; § 5 sim deferral matrix
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architecture rationale + ARPG canon grounding
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — phase-by-phase rebuild execution
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1, #2, #7, #11, #13a/#13b, #17, #18

---

## 8. Maintenance protocol

This document is v1.0 (initial 2026-05-21). Revisions:
- Threshold or algorithm changes → v1.X minor
- Phase restructuring → v2.0 major

Living doc; updated as rebuild progresses and empirical findings refine the model.

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine in motion, end-to-end.
