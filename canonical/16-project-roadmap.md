# 16 — Project Roadmap (post-demo1)

**Last updated:** 2026-05-16 (Day 4 — drift-absorption pass under new stewardship model; form-bias workstream framed; Stage A7 scope-overlap question surfaced; cadence-strategy scheduling call documented)

**Stewardship (locked 2026-05-16 Day 4):** Forward-looking roadmap stewardship sits with **gandalf** (story + design steward) — the WHY/WHAT: story/design priority, strategic re-orientation, sequencing recommendations, scope changes. **Knight-rider** feeds the IS-vs-IS-STATED drift signal as a mechanical input. Mechanical updates (stage completion, timeline updates, cross-reference adds) authored by gandalf directly; recommendations that touch locked design positions still route through Matt via the standard decisions-log Gate-1 flow.

**Prior:** 2026-05-11 (full rebuild — post-demo1-ship state; pre-rebuild content was framed pre-demo1 with stale priority order and timeline)

## 📐 Strategic anchor: file 29

**`29-design-overview.md`** is the project's scope-and-architecture anchor. It answers "what is Reincarnated as a finished game?" and frames the two engines + four-track work model. **This document operationalizes file 29's strategy into concrete sequencing.** When in doubt about scope, consult file 29. When in doubt about engine queue specifics, consult file 28.

## 🎉 Status snapshot (2026-05-16)

**Demo1 v1.2 shipped.** Live at https://reincarnated-demo.vercel.app — playable on desktop + mobile. **Loadout app v0.8** shipped (gear wiring + encounter analytics + skill-gate fix) — separate ARPG-style loadout product; preview deploys on Vercel; origin remote configured 2026-05-16. **Engine telemetry-tier-1** shipped (`v1.3-telemetry-tier1`) — duration_seconds, heals_received, potions_used persisted to fight rows; schema V2.0.

| Component | State |
|---|---|
| Engine 1 (Content Generation) | Functionally complete for demo-scale generation; **Stage A2 ~30% complete** (B10.1, B10.2, B10.4 swarm-calibration shipped; B14.5 V1 primary-loop architecture locked); remaining gaps tracked in file 28 |
| Engine 2 (World Generation) | Not started; demo1 served as a minimum-viable prototype |
| Demo1 | v1.2 shipped to Vercel; 6+ engine-compensating overrides documented for removal per file 28 |
| Loadout app (reincarnated-loadout) | v0.8-gear-wiring shipped (intermediate + milestone tags on origin); built against real telemetry post-tier-1 |
| Production seasons | 5 (seeds 1001-1005) shipped against current engine; new seasons regenerate after Track A engine fixes land |
| Substrate Realignment workstream | **NEW — surfaced 2026-05-14** (see workstream section below); design framework crystallizing via canonical/story/ corpus + form-bias-cadence-strategy doc in flight |

**Current focus when project resumes:** Track A engine maturation — closing the file 28 queue, with the Substrate Realignment workstream interleaving as cadence locks land.

**Team topology (updated 2026-05-16):** 9 entities — knight-rider (orchestrator), gamora / rocket / star-lord (engine seams), drax (loadout/demo presentation), jack-ryan (technical/process QA), **gandalf** (story + design steward, generative-side critique), **legolas** (research + catalogue crawl), **elrond** (data steward — external/cross-cutting layers). Authority tiers per `agentic_orchestration/AGENTS.md`. Three new agents added Day 3 (2026-05-16) per CHANGELOG.

## 🛤️ The four-track work model (per file 29)

The project is organized into four parallel/sequential tracks rather than a linear waterfall:

| Track | Status | What it is |
|---|---|---|
| **Track A — Engine 1 maturation** | In-flight, ongoing | Close the file 28 queue; iterate engine + demo regeneration cycles |
| **Track B — Engine 2 prototyping** | Intermittent, demo-driven | Validate Engine 2 design slices before committing to full build |
| **Track C — Engine 2 build** | Future | Full town + acts + dungeons + quests + NPCs to shippable quality |
| **Track D — Integration + ship** | Future | Combine engines into Reincarnated v1.0 (the full game) |

Tracks are not strictly sequential. Track A is the active line of work; Track B prototypes may interleave when specific Engine 2 design questions need empirical input.

---

## 🎯 Track A engine queue — concrete sequencing

File 28 holds the full engine queue. This section maps file 28's items to a concrete ship order. **The queue is grouped into 7 stages with interleaved playtest cycles** (restructured 2026-05-12 after cohesion audit — see "Restructure note" below).

> **Restructure note (2026-05-12):** The original sequence (Stage A1 bug-fixes → Stage A2 content quality → Stages A3-A8) was reorganized. Engine bug fixes A1/A1b/A2/A4 fold into the ARPG-genre sprint (formerly Stage A3, now Stage A2) since that sprint regenerates all seasons anyway — avoids double-regen. Stage numbering shifts down by one for items after the original A2. **Playtest cycles interleaved between major stages** since most progression-design feel questions (skill tree UI, body-swap moment tension, doppelganger feel, set collection satisfaction, Spirit Guide coaching effectiveness) cannot be validated from JSON/telemetry alone — they need real playtest data.

### Stage A1 — Pre-sprint design + small fixes (~5-8 hrs) ✅ COMPLETE 2026-05-12

**Shipped on `stage-a2` branch (5 commits):**

| Commit | Content |
|---|---|
| `b67d2e4` | D1 rubric + pool pre-scored (148 entries) + selector Phase B/C |
| `79989fa` | D1 pool locked: +7 wind words, organic earth downgrade, web recategorized |
| `4f5cd93` | B6 kit composition templates + A4 decision documented |
| `1aa99b5` | B6/B13/B14/B15 forward-compat schema additions; `season_manifest_version` 1.2 → 1.3 |

**D1 element naming closed:**
- Rubric: 5 properties × 2 points + Genre Precedent +1 bonus; allow-list ≥8 / eligible 5-7 / quarantine ≤4
- Pool state: 155 entries (84 allow-list / 36 eligible / 35 quarantine); wind expanded to 17 primary-wind allow-list entries (parity with fire); organic earth downgraded; web recategorized to earth flex
- Selector Phase B (runtime filter + scoring weight) + Phase C (novel-word LLM mini-call) operational

**B6 templates documented:** 14 archetypes (4 mages + 4 controllers + hybrid_mage + hunter + 3 physical + rogue) with kit size / AOE share / element distribution / chain count + depth / cross-chain rule / required roles / geometry bias / special constraints. Same-family-distinct-secondary rule enforced.

**A4 shield scaling locked:** HoT-style `damage_modifier` scaling (Option B).

**Forward-compat schema additions** (14 new fields on `PlayerClass` + `Skill`):
- B6 fields: `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- B13 fields: `cast_time`, `damage_resolution_time`, `i_frame_window`
- B14 field: `convergence_report` (nested band fields)
- B15 fields: `set_id`, `set_position`, `set_piece_count_required`
- All default to None/[]/{} — existing 5 seasons load without regen

**Original Stage A1 scope** (preserved for historical reference):
- ~~D1 design session~~ ✅ closed (rubric + pool + selector shipped)
- ~~A3 `damage_formula.md` doc audit~~ — folded into ongoing B14 work
- ~~D3 anchor selector duplicate detection~~ — pending; small DB fix
- ~~D4 unnamed class fix~~ — pending; small bug

**Absorbed into Stage A2** (per restructure):
- A1 combo cost clamp → B6 generator refactor side-effect
- A1b focus cost calibration → B6 generator refactor side-effect
- A2 per-skill geometry dimensions → B11 geometry palette expansion
- A4 shield magnitude scaling → A4 decision locked (HoT-style); implementation in B6 sim cleanup

**Stage A1 closed:** D1 + B6 templates + A4 decision + forward-compat schemas all shipped. Stage A2 (starting with B14 multi-band convergence) is unblocked.

### Stage A2 — The coordinated ARPG-genre sprint + absorbed bug fixes — ~11-15 weeks

**Items:** B6 + B7 + B10 + B11 + B12 + B13 + B14 + **B14.5 (recompose-first iterative tuning loop — scope expanded 2026-05-12, V1 shipped 2026-05-12)** + **B16 (loot drop architecture — added 2026-05-12 per Matt's gap-catch)** + absorbed A1 / A1b / A2 / A4 fixes.

**Stage A2 sub-progress (updated 2026-05-16):**

| Sub-item | Status | Tag |
|---|---|---|
| B10.1 — Tier structure + Model B gauntlet | ✅ COMPLETE | `v1.3-b10-1-structure` |
| B10.2 — PackProxy + swarm composition | ✅ COMPLETE (later superseded by B10.4 Option 2 framing for AOE convergence — per decisions-log) | `v1.3-b10-2-pack-proxy` |
| **B10.4 — Swarm calibration / convergence binary-search refactor (Option 2)** | ✅ **COMPLETE 2026-05-16** — 10/10 converged, 1305 tests passed. **Not in original roadmap** — surfaced through B10.2 Two-Gauntlet supersession (decisions-log entry 2026-05-16). | `v1.3-b10-4-swarm-calibration` |
| B14.5 V1 — Recompose-first primary loop | ✅ V1 SHIPPED 2026-05-12 — canonical pattern locked for balance loops (per `project_iterative_dev_disciplines.md`); V2 planned post-B10.4 | (folded into related tags) |
| Telemetry tier-1 extension (star-lord; cross-seam) | ✅ COMPLETE 2026-05-16 — `duration_seconds` / `a_heals_received` / `a_potions_used` persisted; schema V2.0; supports B14 multi-band sim | `v1.3-telemetry-tier1` |
| B6 / B7 / B11 / B12 / B13 / B14 / B16 | Pending — original Stage A2 queue items remain in flight |

**🟡 Yellow flags surfaced during Stage A2 (2026-05-16; investigations queued, do not block tag releases):**

- **Modifier range 0.09–0.52 — RESOLVED 2026-05-16 by gamora investigation: not a tuning defect, not a regression, not Option 2's fault.** Root cause is sim-side combat mechanics; decomposition: rage starts at 0 / mana starts full (~1.5-2.0× short-fight advantage) + physical miss rate ~15% / elemental always hits (~1.18×) + armor ~18.6% reduction / elemental resistance ~0% (~1.23×) → combined ~3-5× DPS-per-modifier disadvantage for rage/physical archetypes (observed 5.5× in hybrid_mage/water vs physical_warrior/physical head-to-head; both have ~77k DPS at modifier=1.0). Generation produces equivalent power budgets; sim produces different effective DPS. **Important epistemic finding:** the file-29 0.85-1.15 target band was a design aspiration for when B14.5 is fully operational; never calibrated against actual sim. Not a useful regression baseline yet. **Mitigation: declare 0.09-0.52 as the B10.4 Option 2 calibration epoch (current mean |mod−1.0| ≈ 0.82); progress tracking target ≈ 0.50 after B6 pre-work (energy-type-aware tier assignment) + B14.5 V2 (energy-type levers in balance loop).** Decisions-log entry pending (calibration-epoch lock). Math derivation: `reincarnated-engine/simulation/math/modifier-range-root-cause.md`; findings summary: `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`; commit `436edc4` on engine main.
- **Tier-1 telemetry coverage ~3.4% on existing seasons.** Surfaced by drax during v0.7 encounter analytics work. 52,800 of 1,541,700 fight rows have Tier-1 columns populated, confined to the first 6 balance-loop iterations. Hypothesis: code-path divergence — fight_engine has a path that bypasses Tier-1 writes when called from gamora's regen loop. Dispatch authored: `2026-05-16-star-lord-tier1-coverage-investigation.md`. Operational consequence: drax's intended Damage × TTK projection is blocked until coverage is fixed and a fresh regen runs.

**This is the largest single stage and the architectural heart of Track A.** B6 + B10 + B11 + B7 + **B14** are **co-dependent** — landing any subset in isolation creates architectural mismatch (per file 29 strategic anchor; file 28 § B11 co-dependency note; file 31 Stage 10). **B12 (movement speed + gear slot audit)**, **B13 (active mobility + telegraphs + evasion + emergence observability)**, and **B14 (multi-band sim)** join this stage since they share the season-regen cycle and are foundational ARPG-feel infrastructure. B14 specifically is the multi-band convergence architecture that supports the "reject mid-game balance debt" anti-pattern locked in file 32 Section 1.

| Item | Scope | Estimate |
|---|---|---|
| **B6** Class kit composition with shaped-balance + **Hierarchical Skill Tree** + **energy-type-aware tier assignment (NEW 2026-05-16; B6 pre-work)** | Element distribution, geometry mix, AOE coverage, role coverage per archetype; replaces uniform-shaped class kits + wide-range damage_modifier; **per-band kit composition recomposition (via B14)**; **tree structure: 4 tiers × 2-4 chains with hierarchical unlock gates (≥3/5/8 ranks) + cross-chain asymmetry per element distribution**. **B6 pre-work added 2026-05-16 per gamora's modifier-range investigation findings:** rage/physical archetypes need ~1.5-2× higher tier bounds in generation templates to compensate for sim-mechanical disadvantages (rage starts at 0 / physical miss ~15% / armor mitigation ~18.6% vs resistance ~0%). Pre-work is a rocket dispatch authored separately; B6 main work (gamora) follows. | ~3-5 weeks engine + 1-2 weeks balance re-tune + **~1-2 weeks rocket pre-work** |
| ~~**B10.1**~~ ✅ Tier structure + Model B gauntlet (COMPLETE — `v1.3-b10-1-structure`) | Full tier vocabulary (swarm/magic/trash/elite/mini-boss/boss); stat tables per spec; `build_reference_gauntlet()` → 12-monster A3 tier-diverse pool (6 trash + 2 magic + 2 elite + 1 mini-boss + 1 boss); BESTIARY_DISTRIBUTION 44 total; "standard" deprecated. 1286/1286 tests. | shipped 2026-05-13 |
| ~~**B10.2**~~ ✅ Pack-proxy + swarm composition rules (COMPLETE — `v1.3-b10-2-pack-proxy`) | `PackProxy` entity: N=8, HP = N × swarm_HP, AOE deals N× damage (M3 Option A). Gauntlet: 6 swarm-pack slots replace 6 trash 1v1 (cost neutral). `_make_recompose_gauntlet()` isolates recompose loop from proxy distortion. 1286/1286 tests. Math: `design/b10-gauntlet-analysis.md` §12. | shipped 2026-05-14 |
| **B10 V2** Sequential-room semantics — **PROMOTED 2026-05-16 from deferred → IN SCOPE FOR DEMO VS2a** | Model A: class fights N mobs per room with HP carryover between encounters. Required for the spec's stated AOE differential goal ("balance loop sees AOE advantage"). V1 establishes the tier-diverse pool; V2 adds sequential-room mechanics + HP/resource carryover. ~3-4× regen cost increase vs V1. Cannot claim "full AOE differential achieved" until V2 ships. **Critical for VS2a — the "updated gauntlet" showcase undersells without sequential-room semantics.** | ~7-12 hours engine; targets VS2a window |
| **B11** Geometry palette expansion | 16 → 25 active types via 9 new AOE-coded geometries (3 un-defer + 6 add-new) + parameter expansions (collision_mode, angle_distribution, sweep_shape, damage_falloff) | ~3-4 weeks engine + demo |
| **B7** Gear-percentile variance check | Pass/fail gate at 50th/75th/95th/99th percentiles; catches "hunter with 2× legendary flat-damage items" pathology at generation time; **runs at endgame (L50) only per B14 architecture** | ~1-2 days engine |
| **B12** Movement speed + boots + gear slot audit | Engine emits `movement_speed` per class + monster tier (class-agnostic base; not stat-driven). Adds boots/gloves/belt gear slots. Boots primary affix = +% movement speed. Hard cap +25% from gear (proposed). Retires demo's `speedForProfile` workaround. | ~1.5-2.5 weeks engine + demo + regen |
| **B13** Active mobility + telegraphs + evasion + emergence observability | 5 new defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance) — 25 → 30 active palette. Engine `cast_time` + `damage_resolution_time` + `i_frame_window` fields. Demo: telegraphs + asymmetric indicator scaling (player 0.92× / enemy 1.08×) + i-frame respect. Engine archetype-emergence observability (surface kit-mobility composition per class for novel-archetype detection). | ~3-4 weeks engine + demo + regen |
| **B14** Multi-band convergence simulator | 3-band act-aligned discrete convergence at L17/L33/L50. **9 convergence runs per class** (was 1): 6 kit+variance + 3 doppelganger-validation. Per-band optimal distributions emitted in export packet. Recompose-first failure handling. Per-band gauntlet generation + per-band monster pools. Convergence cost ~3-5min → ~30-45min/season. Zero LLM call impact from sim. | ~2-3 weeks engine |
| **B14.5** Recompose-first iterative tuning loop (scope expanded 2026-05-12) | Nested-loop balance architecture realizing Section 1's "shaped balance over numeric balance" lock. Primary loop cycles skill-level levers (skill swaps, geometry mix, energy/cooldown values, AOE distribution targeting). Secondary loop cycles element-distribution variations. Architectural hooks for gear loadout cycling (post-Priority-02/B15) and trait fill cycling (post-B9a + gear-affix). damage_modifier as last-resort fallback only. Expected outcome: mean damage_modifier compresses substantially from current ~6× spread. CLI prompt at `canonical/36-b14-5-cli-prompt.md`. | ~1-2 weeks engine |
| **B16** Loot drop architecture (added 2026-05-12) | Drop event mechanism + per-band rarity tables (A1: 70/25/4/0.9/0.1; A2: 50/30/15/4/1; A3: 30/30/25/12/3) + per-monster-tier multipliers + smart-loot 70/30 + ilvl tracking + drop pool integration + telemetry hooks. Demo: drops render in world + auto-pickup with rarity filter. Prerequisite for B15 (Stage A4 sets). Defers cross-season smuggling integration + loot economy validation to Stage A7. | ~1.5-2.5 weeks engine + demo |

**Why co-dependent (in one sentence each):**
- B6 alone (kit composition rules) without B10 → balance loop pushes back to single-target through convergence pressure
- B6 + B10 without B11 → kit-variety crunch on heavy-AOE archetypes (controllers need 8-10 AOE slots from 7-geometry pool)
- B11 alone → richer palette but generator doesn't know how to use it for AOE skew
- B7 (variance gate) needs the restructured gauntlet (B10) to test against
- B16 (drop architecture) needs B10 (monster tiers) + B12 (full gear slot list) as prerequisites; B14's variance check needs B16's actual drops to validate gear scaling at multiple percentiles

**Absorbed bug fixes** (formerly Stage A1; now folded here since this stage regenerates all seasons anyway):
- A1 combo cost clamp (engine generator)
- A1b focus cost calibration (engine generator)
- A2 per-skill geometry dimensions (handled by B11)
- A4 shield magnitude scaling (engine sim cleanup) — already locked via Stage A1: Option B (HoT-style)

**Decisions to make first:**
- B6 — concrete kit composition templates per archetype — **already locked via Stage A1**; templates documented in commit 4f5cd93
- B11 — final geometry palette confirmed at 25 active types per 2026-05-11 expansion (+ 5 defensive mobility from B13 → 30 total); see canonical/09 § "Revision 2026-05-11" + "Revision 2026-05-11 (B13 extension)"
- B16 — per-band rarity table values (locked via canonical/32 § 5 Q5.1); per-monster-tier multipliers; smart-loot ratio (70/30 locked); engine-impl tuning may surface during Playtest Cycle 1

**Demo follow-on:** after Stage A2 lands — substantial demo1 incremental refactor. Add skill tree UI (Hierarchical Skill Tree visualization). Remove pack-grade stat overrides (B10 lands native swarm-tier). Update demo to consume per-skill geometry parameters (B11 `collision_mode`, `damage_falloff`, etc.). Add telegraph rendering + i-frame respect + asymmetric indicator scaling (B13). **Drops render in world + auto-pickup with rarity filter** (B16 + Section 5 Q5.9). Regenerate seasons. Smoke-test.

### 🎮 Playtest Cycle 1 — Post-Stage-A2 (~1-2 weeks)

After Stage A2 lands, the engine has shipped the ARPG-genre foundation: shaped-balance kit composition, hierarchical skill tree, multi-band sim, restructured gauntlet, new geometry palette, active mobility + telegraphs. **Critical subjective qualities to validate via family playtest** (cannot be measured from JSON/telemetry alone):

- Skill tree UI comprehensibility (Tier 1-4 chain progression readable?)
- Hierarchical unlock pacing feel (does Tier 2 unlocking at L10 / Tier 4 unlocking at L27 feel earned vs arbitrary?)
- Per-band gauntlet density feel (A1 vs A3 should feel meaningfully different)
- Cross-chain unlock asymmetry impact (single-element strict vs multi-element flexible)
- Telegraph rendering + i-frame visibility (player understands when to dodge?)
- **Loot drop density + tier distribution per band (B16) — drops feel right at A1/A2/A3?**
- **Smart-loot 70/30 effectiveness — drops actually fit class enough that auto-pickup-rare+ is useful?**
- Mobile-first loot density (auto-pickup with rarity filter solves friction?)
- New mobility geometries feel (roll/dash i-frames feel impactful?)

Insights captured into engine queue for Stage A3 + later adjustments. Playtest deliverable: documented findings + small fixes ticket list.

### Stage A3 — Trait + skill-point + reset architecture (B9 series) — ~4-6 weeks

**Layers on top of B6 (Stage A2).** Cannot ship before Stage A2 — B9's balance loop integration assumes the shaped-balance kit composition is the foundation.

| Item | Scope |
|---|---|
| **B9a** Trait architecture | Per-class trait pool (5-10 traits); varied acquisition floors (1, 12, 25, 38); per-rank power curves calibrated so all traits reach similar power at character level 50; endgame-baseline framing |
| **B9b** Skill point distribution | 120-point endgame budget; variable 10-15 skill kit per archetype; per-skill cap 15 (allows ~8 maxable, forces specialization); per-skill scaling coefficient engine-determined; optimal distribution = engine-balanced "meta build" |
| **B9c** Build reset mechanism | Strict during play: free reset only under specific triggers (struggling → Spirit Guide guided reset; body swap; end-game; refused body swap; **Spirit Guide proactive at act-transition** — new trigger per Section 7 Q7.3). Paid endgame reset post-completion |

**Decisions already locked:**
- Reset model: strict during play (Option A) + paid endgame
- Endgame baseline: level 50, 120 points (100 from level + 20 from quests/bosses), per-skill cap 15
- Trait acquisition floors: 1, 12, 25, 38 with max_trait_level=4
- Trait moment-of-acquisition: auto-unlock at floor + auto-rank with character level (Section 4 Q4.1)
- Skill rank cap: smooth scaling `min(15, floor(level/3.33))` (Section 4 Q4.3)

**Decisions still open:**
- Struggling heuristic — composite metric tuning needs playtest data; Phase 0 ships with simulation-average-only, Phase 1 adds cohort comparison if telemetry exists
- Spirit Guide build-coach UI surfacing — what "Strong/Solid/Marginal/Sidegrade/Downgrade" looks like for skill choices (vs the existing gear marginal-value pattern)
- Spirit Guide divergence-heuristic threshold for proactive act-transition reset recommendation (currently >30% SP would need to relocate — engine-impl tuning)

**Demo follow-on:** demo1 incremental refactor adds trait UI + skill point allocation UI + Spirit Guide build-coach surfacing. Substantial demo work (~1-2 weeks).

### 🎮 Playtest Cycle 2 — Post-Stage-A3 (~1-2 weeks)

After B9 series ships, the full progression-decision layer is in play. **Critical subjective qualities to validate:**

- Trait acquisition pacing (do level-12/25/38 floor unlocks feel earned?)
- Skill point allocation moment (is the 4/7/9 per-act SP rhythm satisfying?)
- Per-skill cap and rank investment progression feel
- Spirit Guide build-coach effectiveness (helpful vs annoying vs unnoticed?)
- Spirit Guide act-transition reset recommendation (proactively useful or invasive?)
- Body-swap mid-act UX (Trial body-swap full-reward path vs doppelganger partial path; decision moment tension)
- Doppelganger fight texture (does fighting your own mirror feel meaningfully different from boss fights?)

Playtest deliverable: documented findings + ticket list for Stage A4 and beyond.

### Stage A4 — Legendary gear abilities (B5) + Seasonal Sets (B15) — ~2-4 weeks engine + 1 week demo

**Independent of B6/B9** but architecturally significant. Adds genre-correct mechanical novelty to legendary tier.

**Engine work:** schema additions to gear (legendary-only): `granted_ability` on weapons (7th hotbar slot), `aura` on armor/shields/accessories (passive tick), `on_hit` on weapons (chance proc), `cast_on_attack` (deterministic Nth-attack trigger). Generator gates which abilities fit which slots. Convergence loop accounts for legendary builds.

**Demo work:** hotbar handling for 7th slot, aura ticking via existing active_effects pattern (Phase 8.0.2 architecture supports this), VFX + audio for granted abilities, tooltip surfacing.

**Decisions already locked (2026-05-10):**
- All legendaries grant abilities (variable richness: some procs, some full skills)
- 7th hotbar slot pattern (not replace-existing)
- Engine convergence runs gear-on with canonical loadout baseline

**Decisions still open:**
- Aura stacking rules — cap on simultaneous tickable auras?
- Power budget shift — legendary stat decrease to compensate for granted-ability power; how much?

**Demo follow-on:** demo1 incremental refactor adds set collection UI + completion tracking + legendary mechanical novelty surfacing.

### 🎮 Playtest Cycle 3 — Post-Stage-A4 (~1 week)

After B5 + B15 ship, the legendary/set-chase endgame is in play. **Critical subjective qualities to validate:**

- Set collection chase feel (does gathering your favorite class's seasonal set feel like a real goal?)
- Legendary mechanical novelty (granted abilities / auras / on-hit procs / cast-on-attack feel distinct from stat-stick legendaries?)
- Form library trophy accumulation (does ascending a set-wearing form feel meaningful?)
- Mobile-first auto-pickup with rarity filter polish — does the Spirit Guide review summary work?

Playtest deliverable: documented findings + ticket list for Stage A7 (full progression integration).

### Stage A5 — Small balance items (B1, B2) — ~2-3 hrs combined, opportunistic

Can land in any session. Often bundled with other stages because they touch overlapping balance code.

- **B1** WIS-on-heal multiplier — currently 0.002 (30% bonus at 151 WIS); raise to 0.005 (75% bonus) or keep as utility-stat design? Decision: ~30 min once made.
- **B2** Per-skill ailment chance scaling — currently flat 0.35; design: high-cost ults → 100%, mid → 35%, low spam → <0.35. Implementation: ~1-2 hrs.

### Stage A6 — Architectural deep-cuts (Category C) — deferred unless playtest demands

These are weeks of work each; only pursue if Track A maturation reveals concrete pain.

| Item | Scope | Trigger to commit |
|---|---|---|
| **C1** Multi-target dispatch in sim | Engine becomes n-vs-m aware; `resolve_skill` accepts defender list; convergence loop becomes density-aware | If demo's invented pack semantics create concrete engine-demo divergence pain |
| **C2** Knockback consumer in sim | Engine has knockback as stub; needs positional consumer | Trivial follow-on if C1 ships |
| **C3** Convergence-target reshaping for horde | Density-aware convergence (kills/minute, time-to-clear-wave) vs current binary 50% win rate | Only meaningful if C1 ships |

**Recommendation:** defer. The B11 chain_lightning/ricochet_bounce/fork geometries can ship without C1 via demo-side approximation (similar to Phase 9.5a AOE splash); engine-side cleaner but not blocking. Revisit after playtest cycles 1-3 inform whether divergence is painful.

### Stage A7 — Progression system design + implementation — ~4-6 weeks design + engine + demo

**The progression scaffold around B9's endgame math + the full Section 1-12 design from file 32.** B9 (Stage A3) built the endgame baseline (level 50, 120 skill points, trait floors 1/12/25/38). Stage A7 ships the surrounding XP/leveling mechanism, per-class stat allocation, multi-band sim (B14 — already in Stage A2), gear tier curves, trait acquisition UX, death penalty mechanics, per-act content scaling, quest-as-XP-source design, and Earth meta-layer hooks.

Full design discussion: **`32-progression-design.md`** (1402 lines, 54 LOCKED entries, all 12 sections resolved). Skeleton tracking decisions: **`33-progression-skeleton.md`**.

**Design status (as of 2026-05-12): all 12 sections RESOLVED.** Stage A7 implementation has its full architectural spec ready — no more design conversations needed before engineering work begins.

| # | Section | Status |
|---|---|---|
| 1 | Progression philosophy (XP-primary hybrid; body-swap-offered death) | ✅ LOCKED |
| 2 | Character level curve (smooth polynomial; hard cap L50) | ✅ LOCKED |
| 3 | Stat point progression (auto-allocate per class identity) | ✅ LOCKED |
| 4 | Ability acquisition UX + Hierarchical Skill Tree | ✅ LOCKED |
| 5 | Gear progression curve + Seasonal Sets | ✅ LOCKED (mostly Stage A4 territory) |
| 6 | Enemy / monster scaling (D2/PoE fixed-per-band) | ✅ LOCKED |
| 7 | Character-Enemy-Monster alignment validation | ✅ LOCKED via Stage A2 B14 + doppelganger validation |
| 8 | Engine simulation update (Option β multi-band) | ✅ LOCKED (B14 — Stage A2) |
| 9 | Death penalty + body-swap pool dynamics | ✅ LOCKED |
| 10 | Per-act content scaling (3 acts) | ✅ LOCKED |
| 11 | Quest as XP / skill-point source (Trial body-swap rewards) | ✅ LOCKED |
| 12 | Movement + mobility + active evasion (B12 + B13) | ✅ LOCKED (Stage A2) |

**Co-dependencies:**
- **Stage A2 (ARPG sprint, B6+B7+B10+B11+B12+B13+B14) is prerequisite.** Stage A7 builds player-facing progression on Stage A2's engine substrate.
- **Stage A3 (B9 series) is prerequisite.** Stage A7's player-facing trait acquisition / skill tree UX layers on B9 endgame math.
- **Stage A4 (B5 + B15) is co-relevant.** Set collection integrates with Stage A7's progression milestones.
- **Engine 2 prototyping (Track B) overlaps.** Quest generation (Section 11) is Engine 2 territory; Stage A7 specifies the engine-side interface (Trial body-swap rewards, end-game quest for doppelganger-path reclaim, etc.); Track B/C builds the quest content.

**Scope (per file 32 closures):**
- XP curve implementation (smooth polynomial level^2.0-2.5)
- Stat auto-allocation per class identity (engine generator integration)
- Hierarchical Skill Tree UI (demo1 incremental refactor)
- Trait acquisition floor unlocks + auto-rank with character level
- Multi-band Spirit Guide build coach (consumes per-band optimal_distribution from B14)
- Spirit Guide proactive act-transition reset recommendation (>30% divergence trigger)
- Body-swap pool tracking (within-season pool dynamics)
- Doppelganger encounter integration (Trial alternative path; engine class-as-Trial-boss reuse)
- End-game quest for doppelganger-path reward reclaim
- ~~Per-band tier-availability gear drop rates~~ → MOVED to B16 in Stage A2 (2026-05-12; Option A — ship full architecture in Stage A2)
- Cross-season smuggling integration (Section 5 Q5.6 — gear retains ilvl across seasons; capacity-limited stash on Earth Self)
- Loot economy validation simulation (old Priority 15 — walks a class L1→L50 + measures equipped-loadout fit; could promote to B17 if needed during A7)
- ilvl tracking on gear (PoE-pattern; cross-season smuggling support)
- Auto-pickup with rarity filter (mobile-first; already locked but lives here for full integration)
- Form library ascension at season end (≤1 per season)

**Estimated cost:**
- Engine implementation: ~3-4 weeks (XP curve + stat auto-allocation + body-swap pool tracking + end-game quest + per-band tier-availability + ilvl + Spirit Guide cross-phase coaching)
- Demo integration: ~2-3 weeks (skill tree UI + trait acquisition UX + body-swap moment UX + doppelganger encounter flow + Spirit Guide coaching surfacing)
- **Total: ~5-7 weeks** (slight increase from original 4-6 estimate due to absorbed Section 12.5 + body-swap pool UX work)

**Position in queue:** **After Stage A3 (B9 series) lands** because progression scaffolding layers on B9 endgame math. Stage A4 (B5 + B15) is independent — can overlap.

### 🎮 Playtest Cycle 4 — Post-Stage-A7 (~2 weeks)

After full progression system ships, the complete Reincarnated Phase 0 seasonal arc is playable end-to-end. **Critical subjective qualities to validate:**

- Full progression arc feel (L1 → L17 → L33 → L50)
- XP curve pacing (do acts feel right length?)
- Multi-band sim impact — do early/mid/late game class feel meaningfully different?
- Body-swap meta-progression weight (does choosing to ascend a specific form feel meaningful?)
- Death-body-swap decision tension (refuse-XP-loss vs accept-seasonal-class-loss + no-ascension)
- Doppelganger encounter feel (mirror match texture vs Trial boss texture)
- End-game quest doppelganger-path reclaim feel
- Form library acquisition trajectory (does collecting ascended spirits feel rewarding?)
- Cross-season smuggling impact (smuggled gear retaining ilvl across seasons)
- Mobile-first vertical-slice cohesion (auto-pickup + skill tree UI + body-swap UX all working together)

Playtest deliverable: comprehensive findings document; Phase 0 ship-readiness assessment; ticket list for any post-Phase-0 work (Earth meta-layer scoping if ready).

**🟡 Stage A7 scope-overlap question — Substrate Realignment workstream (open 2026-05-16):**

Stage A7 was design-resolved 2026-05-12 against file 32 + 33. The **Substrate Realignment workstream** (see new section below) surfaced 2026-05-14 with potential scope additions to A7: per-form gear-slot vocabulary lookups (per `embodiment-narrative-layer.md`), per-form stat-name display, per-form Spirit Guide coaching surfacing, per-form skill-tree visualization. Three reconciliation options:

- **(a)** Stage A7 ships at file-32 spec; embodiment-narrative becomes a separate post-A7 work item. Cleanest scope discipline; embodiment-narrative wait time longest.
- **(b)** Stage A7 absorbs embodiment-narrative integration. Significant scope expansion (likely +2-4 weeks on the estimate); single integrated ship.
- **(c)** Stage A7 narrows to NON-embodiment-narrative content; Substrate Realignment workstream owns embodiment-narrative integration into A7's deliverables (recommended; cleanest seam ownership). Stages from each workstream coordinate at A7's playtest cycle.

**Gandalf recommendation:** (c). Reasoning: embodiment-narrative is structurally a Substrate Realignment concern (per `pre-llm-substrate-inventory.md` Cluster A — the Position-C migration is a coordinated schema rename across rocket + star-lord + drax); folding it into Stage A7 conflates two distinct workstreams with different cadence drivers. Resolves at form-bias-cadence-strategy doc Q4 + Stage A7 scope-lock decision (Matt makes the call when Stage A7 sequencing activates, currently estimated ~6-12 months out).

---

## 🧭 Substrate Realignment Workstream (form-bias work) — NEW 2026-05-16

**Status:** Active. Surfaced 2026-05-14 via `canonical/37-form-bias-diagnosis-and-recovery.md`; design framework crystallizing through canonical/story/ corpus + `canonical/story/form-bias-cadence-strategy.md` (in flight via `2026-05-16-gandalf-form-bias-cadence-strategy.md` dispatch).
**Owner:** gandalf (story + design steward), with cross-seam implementation via knight-rider-authored dispatches per ADR-004.
**Workstream shape:** Cross-cutting; **NOT a new track**. Stages interleave with Track A; precise cadence locks downstream of the form-bias-cadence-strategy doc's Q4 deliverable.

### Why this is a workstream and not a track

Tracks A/B/C/D are the project's strategic-architecture cuts (engine 1 maturation / engine 2 prototyping / engine 2 build / integration + ship). The Substrate Realignment work is *orthogonal* to those cuts — it modifies the engine substrate (Track A), affects what gets generated (Track A output), is consumed by demo + loadout (Track A consumers), and would inherit into Engine 2 (Track C). It is *engine implementation*, but a parallel slice that has its own cadence driver (the form-bias-cadence-strategy doc, not the file-28 queue).

Adding "Track E" would imply parallel-to-Track-A; adding "Stage A8" would imply sequential-after-A7. Neither is right. The workstream interleaves with Track A stages — some Substrate Realignment stages gate Track A stages, others stage independently — and its visibility belongs at the roadmap level so the strategy-doc-level cadence is legible to the team.

### Why it exists

Doc 37 named the project's structural bias toward humanoid form and surfaced it as **implementation-vs-intent drift** (Discipline #13a candidate per terminology lock in `pre-llm-substrate-inventory.md` § 3). The project name *Reincarnated*, the Spirit Guide module, and the originating isekai premise all carried non-humanoid intent that drifted humanoid via implementation defaults. This is a structural realignment to realize latent design intent — **not a pivot.**

### Canonical references (in chronological order of authorship)

- `canonical/37-form-bias-diagnosis-and-recovery.md` — origin diagnosis; Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) and Position (ii) (cipher = resistance-translation only) locked
- `canonical/story/embodiment-narrative-layer.md` — embodiment narrative-skin architecture
- `canonical/story/engine-generic-meta-structure.md` — three-layer model (L1 engine substrate / L2 project cosmology / L3 per-content)
- `canonical/story/cosmology-reincarnated.md`, `canonical/story/court-of-forms.md`, `canonical/story/naming-triad.md`, `canonical/story/style-register.md`, `canonical/story/enemy-visual-legibility.md` — L2 project cosmology layer; consume the L1 substrate the workstream realigns
- `canonical/story/pre-llm-substrate-inventory.md` — 53 catalogued items in 5 clusters (humanoid-presupposing concentration / form-agnostic-but-named-humanoid / form-agnostic / embodiment-orthogonal / universal-LLM-drift); terminology lock for *drift / structural-presupposition / convergence-shape / skew*; rocket inventory pass at `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md`
- `canonical/story/form-bias-cadence-strategy.md` — **IN FLIGHT**; commission at `agentic_orchestration/dispatches/2026-05-16-gandalf-form-bias-cadence-strategy.md`; Q1-Q4 deliverable

### Empirical experiments parked against the workstream

- `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` — runs at cipher migration Stage 3 gate (resolves doc 37 § 6.5 residual-bias open question)
- `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` — runs alongside form-bias-cadence-strategy doc authoring; gates Q4 catalogue-track dependencies; dispatched 2026-05-16 with $5-15 LLM budget authorized

### Provisional stages (locks at form-bias-cadence-strategy doc Q4)

Per the staging discipline established in the canonical-elements thread (re-park decision 2026-05-16 Day 4):

| Stage | What it adds | Status | Track A coupling |
|---|---|---|---|
| **S1** Embodiment-axis added as optional field on Loadout schema | New field; non-breaking; verifies schema migration mechanically | Pending strategy doc | Can ship before or after Stage A2; does not gate Track A |
| **S2** Abstract pair-structure layer alongside canonical-four; generators receive both | Free measurement via comparison telemetry | Pending strategy doc | Best shipped during Stage A2 regen window (avoids extra regen) |
| **S3** Hide canonical-four from LLM (cipher migration per doc 37 § 6) | No-seed cosmology test runs at this gate | Pending strategy doc | Gates seasonal regeneration cycles after it ships (changes LLM prompt surface) |
| **S4+** Embodiment-as-narrative-skin in display; gear → augmentation rename; loadout/demo consumer cleanup | Multi-seam ADR-004 schema migration (rocket schema + star-lord export + drax demo + loadout) | Pending strategy doc | Couples to Stage A7 per scope-overlap question above |

Each stage is reversible. The staging discipline addresses the large-overhaul-scope concern.

### Engine items currently HELD pending workstream cadence

- **kit_anchor rename** (rocket) — small dispatch; held pending cadence choice
- **Embodiment-axis generation** (rocket) — pending cadence
- **Pair-structure layer** (rocket) — pending cadence
- **Mechanical-signature pool design** (rocket) — pending cadence
- **D1 element-name pool reconsideration** — held pending cipher architecture lock + Flag A rubric-screening empirical test (per substrate inventory § 12)
- **Engineering Disciplines #13 (implicit-pillar drift, split into #13a + #13b per terminology lock) and #14 (internal-vs-generative schema separation)** — held pending strategy doc

**Sub-call (gandalf, 2026-05-16):** the kit_anchor rename specifically may be unblockable EARLIER by accepting it ships with whatever label vocabulary survives the cadence decision (a small rename is cheap to redo). Decision deferred to knight-rider when capacity permits dispatch authoring.

### Form-bias-cadence-strategy session scheduling call (gandalf, 2026-05-16 — revised mid-session per Matt's VS2a+VS2b parallel mandate)

**Original recommendation (deferred-until-experiment) — SUPERSEDED.** The original call deferred the strategy doc until the catalogue-mapping experiment returned. Matt's 2026-05-16 directive — *"VS2b work must NOT be blocked or de-prioritized by VS2a; Substrate Realignment work moves as quickly as possible and in parallel so VS2b is right behind VS2a as a ready ticket"* — requires acceleration.

**Revised recommendation: strategy doc lands ASAP via path (b) — Q4 framework + decision-architecture lock immediately; Q4 catalogue-track-dependency resolutions marked "pending experiment" for the S3 cipher-width decision specifically.**

**Reasoning under the parallel-workstream mandate:**

- **S1 (embodiment-axis additive field)** does NOT depend on experiment findings. Can begin as soon as strategy doc Q4 framework locks S1's scope.
- **S2 (pair-structure layer alongside canonical-four)** does NOT depend on experiment findings. Generators receive both labels; free measurement via comparison telemetry. Can begin in parallel with S1.
- **S3 (hide canonical-four from LLM — cipher migration)** DOES depend on the experiment for Q4 cipher-width decision (Options A/B/C from canonical-elements thread). S3 waits; S1+S2 do not.
- **Embodiment-as-narrative-skin display work** (drax) does NOT depend on the experiment. Can begin once S1 lands.
- **Pimen full integration** does NOT depend on the experiment. Can begin as soon as elrond's curation pipeline produces consumable groupings.

Deferring the strategy doc would block S1+S2+display+Pimen full from starting in parallel with VS2a — violating the parallel-workstream mandate. Path (b) unblocks all of these immediately; only S3 waits for experiment Q4 input.

**Caveat to path (b):** strategy doc Q4 will explicitly mark cipher-width as "pending experiment" so no premature lock occurs. When experiment returns, the strategy doc gets a Q4 amendment landing the specific Options A/B/C choice. Knight-rider drafts the amendment-derived decisions-log entry at that point. This is honest framing — the doc is not pretending to know what the experiment will find.

**Experiment timing:** dispatched 2026-05-16 to star-lord with Matt's $5-15 LLM budget authorization. Execution timing depends on star-lord's queue; likely returns within 1-3 sessions.

### What this workstream unblocks when the strategy doc lands

- **Form-bias cadence options** (formerly framed as I/II/III in doc 37) can be reformulated against the strategic-axis lock (ARPG-canon-primary / Isekai-canon-primary / explicit-hybrid)
- **Engineering disciplines #13a, #13b, #14** can be codified in `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **Cipher migration dispatches** (rocket schema work, star-lord LLM-prompt-filter work, gamora doppelganger-gate validation under Position (ii), drax display-leak audit + body-swap UI work) can be scoped
- **D1 element-name pool stewardship** locks decision criteria
- **The catalogue-based form-bias resolution path** (Matt's 2026-05-16 design decision per CHANGELOG) crystallizes operationally

---

## 🎯 Demo Vertical Slice 2 — sequential milestone targets (NEW 2026-05-16)

The roadmap previously treated demo work as incremental refactor within each Track A stage. Matt's 2026-05-16 directive (gandalf stewardship of roadmap) splits the upcoming demo target into **two sequential ship milestones with parallel workstreams converging on each.**

**🔴 Critical constraint (Matt-locked 2026-05-16):** *"All of the Substrate Realignment S1–S3 cipher migration + embodiment-axis + Pimen full integration projects move as quickly as possible and in parallel (where feasible) so that as soon as demo VS2a ships, VS2b is right behind it, waiting as a ticket."* **VS2b work must NOT be blocked or de-prioritized by VS2a.** The two workstreams move in parallel; VS2b ships as a ready ticket within weeks (not months) of VS2a.

This constraint informs every sequencing decision in the rest of this section.

### VS2a — Gauntlet + Geometry + First Catalogue Integration

**Scope:**
- **B6** — Class kit composition with shaped-balance + Hierarchical Skill Tree (Stage A2). **2026-05-16: B6 now includes pre-work** — rocket dispatch for energy-type-aware tier assignment (rage/physical archetypes need ~1.5-2× higher tier bounds in templates to compensate for sim-mechanical disadvantage; per gamora's modifier-range investigation findings). B6 pre-work is rocket; B6 main is gamora; both gate VS2a ship.
- **B11** — Geometry palette expansion (16 → 25 active types; Stage A2)
- **B10 V2** — Sequential-room semantics with HP carryover (PROMOTED 2026-05-16 from deferred → in scope; critical for the "updated gauntlet" showcase)
- **First Pimen VFX integration** — drax ingest pipeline (RAR-unpack, frame-assembly, canvas metadata) + demo VFX consumption of a curated subset (~5-10 packs sufficient for one season's visual diversity)
- Demo regen on a single season (per single-season-per-playtest rule)

**Out of scope for VS2a (deferred to post-VS2a or to VS2b):**
- B7 (gear-percentile variance gate) — not demo-visible; defers
- B12 (movement speed / boots / gear slot audit) — defers; not visually load-bearing for VS2a
- B13 (active mobility + telegraphs + i-frames) — significant scope; defers
- B14 (multi-band sim) — defers; not demo-visible
- B16 (loot drop architecture) — defers
- Substrate Realignment work — explicitly in VS2b
- Full Pimen catalogue integration — explicitly in VS2b

**Estimated working effort:** ~3-4 months. Bottleneck = drax (Pimen ingest pipeline + B11 demo + VFX integration is sequential single-seam work). With aggressive parallelism: gamora ships B6 + B10 V2 in weeks 1-8; rocket supports B11 generator in weeks 4-10; drax builds ingest pipeline + B11 demo in weeks 1-12; integration + regen in weeks 10-16.

**Seam allocation:**

| Seam | VS2a work | Capacity note |
|---|---|---|
| gamora | B6 (engine kit composition + balance re-tune); B10 V2 (sequential-room semantics) | Currently has modifier-range investigation queued; B6 starts after that closes |
| rocket | B11 generator support (new geometry palette + parameter expansions) | No active dispatch; can begin immediately once dispatch authored |
| drax | B11 demo (geometry rendering); Pimen ingest pipeline (RAR-unpack, frame-assembly, canvas metadata); first VFX integration in demo | **Most loaded seam.** Currently has v0.7/v0.8/encounter-explainer + queued items |
| elrond | Pimen curation pipeline (already in flight); subset selection for VS2a integration | Pipeline work is already in flight |
| star-lord | Telemetry support for B6 convergence; no new schema lift | Minimal load |

**Ship trigger:** single regenerated season demonstrates updated gauntlet (B6 kit composition + B10 V2 sequential rooms) + new geometry palette (B11) + first VFX integration (Pimen subset) in play with no override compensation.

### VS2b — Substrate Realignment + Full Catalogue Integration (PARALLEL to VS2a, ships right behind)

**Scope:**
- **Substrate Realignment S1** — embodiment-axis added as optional Loadout field
- **Substrate Realignment S2** — abstract pair-structure layer alongside canonical-four; generators receive both labels
- **Substrate Realignment S3** — hide canonical-four from LLM (cipher migration per doc 37 § 6); no-seed cosmology test runs at this gate
- **Embodiment-as-narrative-skin in display** (loadout + demo) — per `embodiment-narrative-layer.md`
- **Full Pimen catalogue integration** — broader VFX coverage, character sprites where catalogue supports, multi-season visual diversity
- Demo regen on a fresh season (separate from VS2a's regen season to preserve comparability)

**Critical dependency:**
- form-bias-cadence-strategy doc Q4 lock for cipher-width decision — **S3 specifically**
- S1 + S2 + display + Pimen full do **NOT** depend on the strategy doc beyond Q4 framework; can begin immediately

**Estimated working effort:** ~3-6 months total. Most of this runs **in parallel with VS2a's 3-4 months**. Sequence: S1 ships in parallel with VS2a's B6/B10 V2; S2 ships in parallel with VS2a's B11/Pimen first integration; S3 implementation begins when experiment returns + strategy doc Q4 amendment lands (potentially mid-VS2a or post-VS2a depending on experiment timing); display + Pimen full integration ships in parallel with VS2a's final integration weeks.

**Target: VS2b ready as a ready-to-cut ticket within 2-4 weeks of VS2a ship.**

**Seam allocation (parallel to VS2a — same seams, different tasks):**

| Seam | VS2b work | Parallelism with VS2a |
|---|---|---|
| rocket | S1 schema (embodiment-axis field); S2 pair-structure (alongside canonical-four); S3 generator-side filter once Q4 lands | S1 + S2 can start IMMEDIATELY in parallel with VS2a (no rocket VS2a load until B11 generator work; even then schema work is in different files) |
| star-lord | Catalogue-mapping-and-grouping experiment execution (currently dispatched); S3 LLM prompt-filter work once Q4 lands | Experiment runs throughout; LLM prompt filter is small lift |
| drax | Embodiment-narrative display (loadout first as lower-stakes test, demo second); Pimen full integration (after VS2a first integration) | **Drax bandwidth is the binding constraint.** See risk section below. |
| elrond | Catalogue abstraction analysis (feeds Q4 cipher-width decision); Pimen full integration support | Catalogue analysis runs in parallel; full integration support kicks in toward end |
| gandalf | form-bias-cadence-strategy doc (path (b) — land immediately with Q4 framework + dependency-deferrals on cipher-width specifically) | IMMEDIATE — no VS2a load |
| gamora | S2 consumer adjustments in simulation seam (small lift; interleaves with B6) | Smaller than VS2a load; interleaves cleanly |

**Ship trigger:** fresh regenerated season demonstrates cipher migration (LLM no longer sees canonical-four labels; per-season vocabulary fully drives surface) + embodiment-axis populated on Loadout + embodiment-narrative display in loadout/demo + Pimen full integration. Ships as soon as VS2a is validated AND VS2b's parallel work is complete.

### Parallel-execution risks (gandalf, 2026-05-16)

The Matt-locked parallelism mandate is right for the work but creates real coordination risks:

**🔴 Risk 1 — drax bandwidth saturation.** Drax is currently in the most workstreams of any seam (loadout v0.5.2/v0.7/v0.7.1/v0.8 wave + encounter-explainer pending + queued items). Adding B11 demo + Pimen ingest pipeline + first VFX integration (VS2a) AND embodiment-narrative display + Pimen full integration (VS2b) likely saturates drax for ~4-6 months. Mitigations:
- Defer some current drax work to post-VS2a (e.g., loadout UI polish that doesn't gate VS2a)
- Split drax workload between loadout repo (lower-stakes embodiment-narrative test surface) and demo repo (higher-stakes VS2a integration)
- Pimen ingest pipeline + first VFX integration could potentially be partially handled by elrond on the curation side, reducing drax's pipeline-build load

**🟡 Risk 2 — catalogue experiment timing uncertainty.** S3 depends on Q4 cipher-width lock, which depends on experiment findings. If experiment returns slow (>3 months) or ambiguous, S3 implementation slips, and VS2b's "ready as a ticket right behind VS2a" guarantee weakens. Mitigation:
- Star-lord should be prompted to prioritize experiment execution (gandalf to flag if not happening on cadence)
- Strategy doc Q4 amendment process must be lightweight (gandalf authors amendment when experiment returns; knight-rider drafts derived decisions-log entry — both fast-turn)
- If experiment slips badly, VS2b can ship S1 + S2 + display + Pimen full WITHOUT S3 cipher migration; S3 lands as VS2c. Worth Matt's awareness as a contingency.

**🟡 Risk 3 — regen budget vs single-season-per-playtest rule.** VS2a regens one season for validation; VS2b regens another for validation. That's two regens within the parallel-workstream window. Per file 31 projection (~$5-10/season post-Stage-A2), each regen is non-trivial. Mitigation:
- VS2a regens season_001003 (or similar); VS2b regens season_001005 (or similar); different seasons preserve comparability across the demos
- Optional combined playtest cycle covering both VS2a and VS2b ships rather than two separate cycles

**🟡 Risk 4 — decisions-log gate on canonical-four lock supersession.** S3 requires the canonical-four lock (currently in "Closed/locked decisions" but flagged as under-re-examination) to be formally superseded via decisions-log entry. That's a Matt approval gate. Should not surprise the team at S3 implementation time; knight-rider drafts the supersession entry when strategy doc Q4 lands.

**🟢 Risk 5 — playtest cohesion.** Two parallel workstreams may produce a fragmented playtest experience if VS2a and VS2b are evaluated separately. Mitigation: plan a combined VS2a+VS2b playtest cycle where the same player session walks through VS2a-regen-season then VS2b-regen-season for comparison.

### Sequencing recommendation (gandalf, 2026-05-16)

**Immediate next actions to authorize parallel execution:**

1. **gandalf** authors `canonical/story/form-bias-cadence-strategy.md` (path (b) — immediate; Q4 framework with explicit cipher-width deferred)
2. **knight-rider** authors dispatch for **rocket** to begin Substrate Realignment S1 (embodiment-axis field addition) as soon as gandalf's strategy doc Q1 inventory framing lands
3. **knight-rider** authors dispatch for **gamora** on B6 once modifier-range investigation closes
4. **knight-rider** authors dispatch for **drax** on Pimen ingest pipeline (parallel to current drax wave; high-priority queue position)
5. **knight-rider** ensures **star-lord** executes catalogue-mapping experiment in next available session (this is the critical-path item for S3 timing)
6. **gandalf** monitors drax bandwidth; surfaces escalation to knight-rider + Matt if saturation begins to delay VS2b

**Decisions-log entries expected to follow:**
- Strategy doc Q4 framework lock (when gandalf doc lands)
- Substrate Realignment workstream formal scope-and-stages lock (when strategy doc lands)
- Canonical-four lock supersession (when strategy doc Q4 Cipher-Width amendment lands post-experiment)
- VS2a / VS2b milestone definitions (this section formalized into a decisions-log entry once Matt confirms; treat as locked-in-roadmap pending that formalization)

---

## 🔁 Track A landing rhythm

Each stage follows the same rhythm:

1. **Decisions land** (design session if needed)
2. **Engine work lands** (committed; tests pass)
3. **Season regeneration** — **ONE season at a time per playtest cycle** (see "Single-season-per-playtest rule" below)
4. **Demo override cleanup** (per file 28 § "Demo-side override removal plan" — remove the overrides this stage retires)
5. **Smoke test** (single regenerated season playthrough; verify no regressions vs prior baseline)
6. **Tag a partial-then-promote release** (per partial-tag protocol — `v*-partial` until verified)

The demo and engine repos cycle together. Engine maturation alone is not enough — each engine round closes loop with demo regeneration + override cleanup so the running artifact stays engine-faithful.

### ⚠️ Single-season-per-playtest rule (LOCKED 2026-05-12)

**Operational principle: regenerate AT MOST ONE LLM-generated season per playtest cycle.** A case can be made for multiple seasons later (e.g., when shipping toward Phase 0 closure or validating cross-season variety), but the baseline policy is **one season per cycle.**

**Rationale (cost math):**
- Current LLM cost baseline: ~$0.87/season
- Post-Stage-A2 (B14 multi-band + per-band monster pools + B15 sets): ~$5-10/season per file 31 projection
- 5 seasons × 4 playtest cycles × ~$8/season = **~$160 in LLM spend just on playtest regeneration**
- 1 season × 4 cycles × ~$8/season = **~$32 in LLM spend** — 5× cheaper

**Why this works:**
- A single regenerated season exercises ALL the new engine changes (kit composition, tree structure, multi-band convergence, gear/sets, mobility, etc.) — playtest signal is high per season
- Other 4 seasons remain at prior baseline for comparison reference
- Cross-season variety testing (when ready) gets a deliberate budget allocation, not casual burn

**Exceptions to the rule** (cases where multiple-season regen IS appropriate):
- Cross-season meta-progression validation (form library accumulation across seasons)
- Pre-ship Phase 0 closure sweep (validate full library + smuggling + body-swap)
- Specific design questions that need cross-season comparison

**Default = 1 per cycle.** Multi-season regen requires explicit justification and budget call.

### 🔧 Refactor vs rewrite decision (LOCKED 2026-05-12)

**Track A is a REFACTOR of the existing engine, NOT a rewrite from scratch.** All B-items extend existing infrastructure rather than replacing it.

**Why refactor:**
- Engine's core insights (convergence pattern, dimensional generation, fit_for_class scoring, LLM call pipeline, telemetry) are foundational and proven through 5 production seasons + demo1 family playtest
- Most B-items are ADDITIVE to existing schema (B6 tree generation; B9 traits + skill points; B11/B13 palette extensions; B12 gear slots + movement_speed; B15 sets)
- B14 multi-band convergence is the riskiest piece — significant refactor of convergence loop — but operates on existing primitives, not greenfield
- "Second system effect" makes rewrites typically 2-3× longer than estimated
- 5 production seasons + demo1 v1.2 prove the current architecture works; throwing it away is throwing away validated knowledge

**Risk mitigation:**
- Branch off main before Stage A2 starts
- Tag `v1.2-pre-stage-a2` on both engine + demo repos as the restore point
- Snapshot 5 production seasons (already in `engine-repo/exports/season_001001-005` + `demo-repo/public/seasons/season_001001-005`) — verify present pre-refactor
- Run `engine-repo/scripts/capture-regression-baseline.py` BEFORE Stage A2 begins — snapshots `exports/season_001001-005/` + `data/telemetry.db` + `research.db`; extracts per-class `balance_metadata` fingerprint (target_winrate / actual_winrate / convergence_iterations / final_modifier / converged); writes `baseline/v1.2-pre-stage-a2/` as regression test substrate
- Schema versioning via `season_manifest_version` already exists; bump on Stage A2 ship for forward-compat handling
- Stage A2's per-stage tagged releases (per landing rhythm above) make incremental rollback possible if any sub-stage breaks

**Legacy preservation:**
- **Git history + tags are sufficient** — main branch + `v1.2-pre-stage-a2` tag captures every commit
- **No separate `legacy-engine` branch needed** — creates maintenance burden + diverges from main; not worth the overhead
- **Production seasons are the artifact that matters** — preserve them in both repos as-is (already present)

---

## 🛣️ Track B — Engine 2 prototyping (intermittent) + Demo strategy

### Demo strategy (LOCKED 2026-05-12)

**Approach: incremental demo1 refactor with interleaved playtests, NOT a rebuild and NOT defer-to-Unity.**

- **Track A playtest demos** = demo1 (Pixi.js) incrementally refactored per Track A stage
- Each stage adds UI/UX to demo1 (skill tree visualization, body-swap moment flow, doppelganger encounter, set collection, etc.)
- 4 interleaved playtest cycles (post-A2 / post-A3 / post-A4 / post-A7) validate subjective qualities not measurable from JSON/telemetry alone
- **Unity migration deferred to production-polish phase** (far-future per "VFX pipeline progression" item); demo1 stays the playtest vehicle through Phase 0

**Rationale (vs alternatives):**
- ❌ Rebuild demo2 from scratch: significant work; second-system risk; demo1 foundation (sprites/VFX/HUD/mobile-desktop) is real reusable infrastructure
- ❌ Defer all demos until end + big Unity demo: 6+ months without playtest feedback = high risk of "shipped wrong thing"; many existing design directives came from family playtest insights; pulling that feedback loop = blind flying
- ✅ Demo1 incremental refactor + interleaved playtests: maintains playtest cadence; reuses existing foundation; allows Unity migration when production-polish phase arrives

### Track B prototypes (intermittent)

Demo1 served as Track B prototype phase 1 (proved: linear 7-room with packs/doors/breathers; LLM-flavored class+monster+gear; mobile + desktop deployment). Future Track B work — each prototype validates one slice of Engine 2 before committing:

| Prototype | Validates | Blocking decision |
|---|---|---|
| Town/hub prototype | Hub form (Diablo-style town vs Hades-style run-hub) | Hub form (currently TBD) |
| Quest chain prototype | Quest generation + per-act progression | None |
| Dungeon generation prototype | Procedural dungeon + thematic validation | Dungeon validation method (CV-based vs feature-tagged; currently TBD) |
| Body-swap interaction prototype | Spirit-swap mechanics layer (duration, friction, vulnerability) | Spirit-swap mechanics (currently TBD) |
| Multi-NPC dialogue prototype | NPC personality + dialogue trees + meta-NPC coordination | None |

**Track B timing:** intermittent; spin up a prototype when (a) an open design decision needs empirical input or (b) a quiet stretch of Track A creates capacity. May reuse demo1 codebase or fork a demo2 build.

---

## 🏗️ Track C — Engine 2 build (future)

After enough Track B prototyping validates the approach: full Engine 2 development. Town, acts, quests, dungeons, NPCs built to shippable quality. **Cannot start before:** hub form decided, dungeon validation method decided, final act count decided. Timing depends on Track B outcomes.

## 🚢 Track D — Integration and ship (future)

Combine Engine 1 + Engine 2 into a playable game. Final polish. Iterate on player experience. Ship **Reincarnated v1.0** — the full game, not the demo.

After ship: iterate on shipped game; add features; consider open-source release of engines if they prove robust.

---

## ❓ Open design decisions

These block specific tracks. Some are urgent; some are not. Recommended sequencing: resolve the 🔴 items before their dependent track starts.

### 🔴 High-impact, blocks Substrate Realignment workstream (see workstream section above)

- **Cipher width** (Options A/B/C from the parked canonical-elements thread). Re-parked under the three-layer-model reframe per `pre-llm-substrate-inventory.md` § 10 + § 11. Resolution lives inside the form-bias-cadence-strategy doc's Q4 deliverable; gates on the catalogue-mapping-and-grouping experiment.
- **Foundation layer placement** (L1 engine substrate vs L2 Reincarnated cosmology). Flag B from rocket inventory pass; `foundation/foundation.py:39-43` hard-codes 4-rotating + 1-physical. Maps onto Q5 of canonical-elements thread. Resolves at form-bias-cadence-strategy doc Q4 + Matt's call on layer ownership.

### 🔴 High-impact, blocks Engine 2 (Track C) commitment

- **Hub form: Diablo-style town vs Hades-style run-hub.** Prototype both via Track B before committing. (file 29 § "Open design decisions")
- **Dungeon validation method: CV-based vs feature-tagged.** Highest-risk item in proposal. Prototype both early in Track B; commit only after data. (file 29 § "Open design decisions")
- ~~**Final act count: 4, 5, or 6.**~~ → **LOCKED 2026-05-11: 3 acts** with per-act bands A1: L1-17, A2: L18-33, A3: L34-50. See file 32 § Section 10 / file 33 § "Act structure."

### 🟡 Medium-impact, designable at any time

- **ARPG ↔ Isekai canon push/pull.** Form-bias-cadence-strategy doc Q3 + Q4 deliverable; commission active. Strategic-axis lock (ARPG-canon-primary / Isekai-canon-primary / explicit-hybrid) lives here. See Substrate Realignment workstream above.
- **D1 rubric humanoid-fantasy screening.** Flag A from rocket inventory pass — empirical test needed before D1 pool reconsideration is scoped. See `pre-llm-substrate-inventory.md` § 12.
- **Pimen acquisition decisions.** Three-track viability gate PASSED 2026-05-16 (gandalf design / elrond structural / drax wiring). Full crawl complete; elrond curation pipeline pending. Cost analysis ready; Matt-level call on which packs to acquire and when. 21-row visual-inspection queue deferred (gandalf register-track inspection when acquisition prioritization activates).
- **Per-season-vocabulary-coupling (α/β/γ).** Surfaced 2026-05-16 (Day 4) by Matt. α = validation+regenerate; β = in-prompt constraint; γ = runtime fallback. Resolves at catalogue-mapping-and-grouping experiment findings (sibling to form-bias-cadence-strategy doc).
- **Multiple-canonical-groupings architecture.** Surfaced 2026-05-16 (Day 4). Substrate-wide / active-narrow pattern per three-layer model (engine-generic-meta-structure.md). Resolves at catalogue-mapping-and-grouping experiment findings.
- **Progression systems scope.** Which of skill trees / paragon endgame / gem-rune systems / crafting / multiple difficulty tiers / set bonuses are in scope? Trait + skill-point side largely resolved by B9 (Stage A4).
- **Spirit-swap mechanics layer.** Duration model (at-will / time-bound / charged / event-tied)? Form-shift cost / friction? Earth-self vulnerability (shared HP vs separate)? Past-character persistence across seasons? Rift encounter availability? Early-ascension strategic value? These don't block Tracks A or B but the eventual game-implementation layer needs them. See `../collaboration-handoff/06-trial-room-and-class-scoping.md` + `17-gear-and-spirit-guide-design.md` § "Cross-class smuggling".
- **Cross-season meta-progression depth.** Specific mechanics for gear smuggling capacity, meta-currency, accumulated-knowledge effects.
- **Geospatial mechanics roadmap.** Phase 3's `at_melee_range` boolean is the only geospatial state. B11 un-defers motion-AOE geometries (whirlwind, dash_attack, leap_strike) with light-touch position math; B13 active-mobility geometries (roll/dash/blink) extend this. Summoner geometry (historical "Phase 5" staged item) eventually needs richer positional model. No written design yet for what comes after the boolean.

### 🟢 Low-impact, resolve when convenient

- **Item type breadth.** Weapons + armor + accessories confirmed; gems/runes/consumables TBD.
- **Body-swap visual transition design.** Important for game feel but not blocking architecture.
- **Aura stacking rules (B5).** Cap on simultaneous tickable auras when multiple aura items equipped?
- **Validity matrix expansion (element × non-mana).** Cross-combinations like fire-rage warrior, wind-focus archer. Phase 4 candidate or post-B9 once traits expose elemental scaling explicitly.

### ✅ Closed/locked decisions (reference)

These decisions are settled; listed here so they're not re-litigated:

- **Two-engine architecture** (Engine 1 content gen + Engine 2 world gen) — file 29
- **Shaped-balance philosophy** (composition first, numbers last) — file 29
- **Dimensional generation** (Option C with five axes) — `../collaboration-handoff/10-decision-log-entry-dimensional-generation.md`
- **Canonical element palette** — physical / fire / wind / water / earth / hybrid; no expansion, no per-season rotation. Seasonal flavor substitution + sub-flavor emergence deliver variety. **⚠️ This lock is under live re-examination via the Substrate Realignment workstream** (cipher-width Options A/B/C; three-layer model); the lock remains operative until the form-bias-cadence-strategy doc Q4 supersedes it via decisions-log entry.
- **Geometry palette (revised 2026-05-11)** — 25 active types via B11; un-defers whirlwind/dash_attack/leap_strike per demo1 retired-blocker; parameter-expansion approach over type proliferation. See `09-geometry-palette-discussion.md` § "Revision 2026-05-11".
- **B9 endgame baseline** — level 50, 120-point skill budget, per-skill cap 15, kit size 10-15, trait floors 1/12/25/38.
- **B9c reset model** — strict during play, paid endgame.
- **B5 hotbar pattern** — 7th slot for granted abilities (not replace-existing).
- **Solo gameplay for Phase 0 seasonal play** — multiplayer envisioned for post-Phase-0 Earth meta-layer rift events (PVP / PVE; see `project_earth_meta_layer.md` memory + future `../collaboration-handoff/34-earth-meta-layer.md`).
- **View A locked as AOE balance philosophy** (2026-05-16) — per `canonical/story/engine-balance-stewardship.md`. Multi-dimensional divergence framework (floor / ceiling / experienced-cost-parity); movement-modeling abstraction limitation named; Stage A2 sim extension scheduled. B10.2 "Convergence = full fidelity" SUPERSEDED.
- **Court of Forms canonical** (2026-05-16) — 8 structural commitments + meaning-of-the-arc statement per `canonical/story/court-of-forms.md`.
- **Enemy visual legibility canonical** (2026-05-16) — per `canonical/story/enemy-visual-legibility.md`.
- **Style register locked: HD-2D-shaped pixel-art** (2026-05-16) — operational precision rules + score-don't-filter catalogue principle. See `canonical/story/style-register.md`.
- **Naming triad locked** (2026-05-16) — anchor → spirit name → embodiment-flavored name; player-facing labels Trial / Mirror / Passage. See `canonical/story/naming-triad.md`.
- **research.db retired** (2026-05-16) — `scripts/db.py` deleted; elrond is the new data steward for external data; catalogue.db is the successor.
- **Pimen catalogue full crawl complete + viability gate PASSED** (2026-05-16) — three-track review (gandalf design / elrond structural / drax wiring); 46 distinct packs catalogued; curation pipeline in flight via elrond.
- **Engine + game two-products framing** (2026-05-15) — per `canonical/37-engine-and-game-two-products.md` + `canonical/story/engine-generic-meta-structure.md`. L1 engine substrate / L2 project cosmology / L3 per-content separation; supports pitch-2026-05-18 B2B licensing claim.

---

## 🛠️ Polish / small work (opportunistic, between stages)

| Item | Source | Effort |
|---|---|---|
| `base_mana` / `base_stamina` telemetry write gap | Phase 1 finding | 3-line fix; do when adjacent code is touched |
| `seasonal_element_name` column on classes/abilities NULL despite substitutions table populated | 2026-05-08 forensics | Investigate by-design vs write-gap |
| Element-system PR #1 cleanup | Stale branch from May 7 | 2 minutes |
| Phase 1 stranded TrialBoss commit cleanup | Operational debt | 2 minutes |

---

## 🏔️ Far-future (months / years out)

Most won't materialize until Track A maturation completes and the engine produces fully ARPG-genre-correct content.

- **VFX pipeline progression:** Pixi.js (demo1) → continue iterating with Super Pixel Effects pack; longer-term Unity port for production polish + better mobile deployment. Three.js prototype path from original design is now superseded — demo1 proved Pixi for prototype, Unity for production
- **Trial dungeon structure / visual rendering:** the actual playable trial room, not just generation
- **Form-library / spirit-swap UX:** the player-facing layer of body-swap (gated on spirit-swap mechanics decisions above)
- **Game lifecycle progression:** acts, seasons, story
- **Audio pipeline production:** demo1 ships basic audio; production audio per-season-themed music ([file 26](./26-demo-audio-content-rd.md)) and richer SFX is future polish
- **Multiplayer / co-op:** *out of scope for Phase 0 seasonal play indefinitely; envisioned for Earth meta-layer rift events post-Phase 0* (PVP / PVE; see `project_earth_meta_layer.md` memory + future `../collaboration-handoff/34-earth-meta-layer.md`). File 27 captures earlier research
- **Static seasonal themes / variety polish:** how seasons feel meaningfully different beyond mechanical variety. Addressable once Engine 2 produces themed maps + lore arcs
- **Open-source release of engines:** if they prove robust and useful, post-ship consideration

---

## 🎯 Rough timeline

Side-project pace with father-son cadence. Timeline estimates are deliberately conservative. **All estimates are working time, not calendar time** — calendar can stretch significantly based on availability.

| Stage | Working effort | What lands |
|---|---|---|
| Stage A1 (pre-sprint design + small fixes) | ~5-8 hrs | D1 design session, A3 doc audit, D3, D4 |
| **Stage A2 (ARPG sprint — coordinated; absorbs A1/A1b/A2/A4 bug fixes)** | ~11-15 weeks | B6 + B10 + B11 + B7 + B12 + B13 + B14 + **B16** — kit composition + Hierarchical Skill Tree + gauntlet restructure + 9 new offensive geometries + 5 new defensive mobility geometries + variance gate + movement speed/boots/gear slot audit + telegraphs/i-frames/asymmetric indicators + archetype-emergence observability + multi-band convergence sim (3-band: L17/L33/L50) + **loot drop architecture (per-band rarity tables, smart-loot 70/30, ilvl tracking, drop event mechanism)**; substantial demo work + season regen |
| 🎮 Playtest Cycle 1 (post-A2) | ~1-2 weeks | Skill tree UI, gauntlet density, mobility geometries, telegraphs, mobile-first auto-pickup |
| Stage A3 (B9 series) | ~4-6 weeks | B9a + B9b + B9c — traits + skill points + reset + Spirit Guide build coach + act-transition proactive reset; substantial demo work |
| 🎮 Playtest Cycle 2 (post-A3) | ~1-2 weeks | Trait acquisition pacing, skill point allocation, Spirit Guide coaching, body-swap UX, doppelganger feel |
| Stage A4 (B5 legendary abilities + B15 Seasonal Sets) | ~2-4 weeks engine + 1 week demo | Legendary gear with granted_ability / aura / on_hit / cast_on_attack + class-specific seasonal sets (one per playable class per season; L50-only drops; 2/4/full-set bonuses; gather-your-favorite-set seasonal goal; trophy value for Earth meta-layer) |
| 🎮 Playtest Cycle 3 (post-A4) | ~1 week | Set collection chase, legendary novelty, form library trophy feel, auto-pickup polish |
| Stage A5 (small balance) | ~2-3 hrs | B1, B2 — interleaved with other stages |
| Stage A6 (Category C) | DEFERRED | Multi-target dispatch + knockback consumer + convergence reshape — only if playtest cycles 1-3 demand |
| Stage A7 (Progression system implementation) | ~5-7 weeks engine + demo | The scaffold around B9 endgame math — XP/leveling, stats, body-swap pool tracking, doppelganger encounters, end-game quest, ilvl, Spirit Guide cross-phase coaching, form library ascension. **Design FULLY RESOLVED 2026-05-12 in file 32 + 33.** After Stage A3 lands. See file 32 + file 33 |
| 🎮 Playtest Cycle 4 (post-A7) | ~2 weeks | Full progression arc; XP curve pacing; multi-band class feel; body-swap meta-weight; doppelganger feel; form library trajectory; mobile-first cohesion |
| Track B prototyping | Intermittent | Town/quest/dungeon/body-swap/dialogue slices |
| Track C build | Months | Full Engine 2 |
| Track D ship | Months | Reincarnated v1.0 |

**Cumulative Track A working effort:** ~29-42 weeks (Stages A1–A4 + A7 + 4 playtest cycles; A5 opportunistic; A6 deferred). Restructure 2026-05-12 folded bug fixes A1/A1b/A2/A4 into Stage A2 (avoids double-regen); progression-system implementation moved to Stage A7 (~5-7 weeks; design fully resolved in file 32). B16 (loot drop architecture) added to Stage A2 2026-05-12 (+1.5-2.5 weeks; Option A — full architecture, not stub). 4 interleaved playtest cycles (~5-7 weeks total) added since most progression-feel questions require playtest insights, not just JSON/telemetry.

**2026-05-16 milestone re-targeting:** Track A's near-term focus is now organized around the **Demo Vertical Slice 2 (VS2a + VS2b) milestones** (see dedicated section above). VS2a targets a subset of Stage A2 items + B10 V2 (promoted from deferred) + first Pimen integration (~3-4 months working effort). VS2b runs in parallel and ships right behind VS2a — Substrate Realignment S1–S3 + embodiment-narrative display + Pimen full integration (~3-6 months working effort, overlapping VS2a). Items NOT in VS2a (B7, B12, B13, B14, B16) defer to post-VS2a Stage A2 completion. Stage A3-A7 retain their original sequencing but downstream of the VS2 push.

After each stage closes: a regenerated 5-season demo1 baseline + an engine state matching file 31's projection more closely. **By end of Stage A4 (B5 legendary + B15 Seasonal Sets), demo1 is fully engine-faithful** (zero overrides per file 28 § "Demo-side override removal plan") and the engine has reached the file 31 future-state target for legendary content. **Stage A7 (progression system implementation) extends beyond that** — adds the player-facing XP/leveling, body-swap pool tracking, doppelganger encounters, and Spirit Guide cross-phase coaching layer on top of B14's multi-band sim from Stage A2.

---

## 🧭 How to navigate the engine queue

When sitting down to engine work:

1. **Pick the next stage.** A1 first if not done; otherwise the next sequential stage (A2 alongside A1; A3 only after decisions land; A4 only after A3 ships; etc.).
2. **Resolve pending decisions for that stage** before code. Each stage above lists its open decisions.
3. **Reference file 28** for full item specs, cost breakdowns, sub-item details.
4. **Reference file 31** for the target-state projection — what the engine should look like after that stage lands.
5. **Reference file 30** for current-state context — what the engine looks like right now.
6. **Follow the landing rhythm** — engine commit → season regen → demo override cleanup → smoke test → tag.

When sitting down to demo work post-engine-stage:

1. **Reference file 28 § "Demo-side override removal plan"** — canonical map of demo override → engine queue item.
2. **Remove the overrides this stage retires.**
3. **Verify engine-faithful behavior** matches expected (file 28 § "Verification rubric").
4. **Regenerate seasons + replace** `/public/assets/seasons/`.
5. **Smoke test** the 5-season playthrough.

---

## 📚 Memory cross-references

For deeper context on specific items, see the memory files in `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/`:

- `project_reincarnated_engine.md` — engine state + architectural direction
- `project_engine_state_findings.md` — empirical findings, recurring lessons, accumulating concerns
- `project_design_intent.md` — spirit-swap, trial room, class scoping intent
- `project_geometry_palette.md` — geometry palette decisions (Phase 3 + B11)
- `project_role_orientation_taxonomy.md` — Phase 2 role decision (damage / support / control / hybrid)
- `project_progression_concept.md` — Priority 14 (Traits-and-Skills) historical sketch; largely superseded by B9 series + file 32 / file 33 progression locks (2026-05-11/12)
- `project_gear_and_spirit_guide.md` — Priority 02 gear architecture + Spirit Guide engine API (now B5 + B12 + B15 in current naming)
- `project_earth_meta_layer.md` — Earth Self meta-layer design intent (2026-05-11 reveal; far-future implementation)
- `project_pet_system.md` — pet system design intent (2026-05-11; deferred to focused later sprint; near-term solved via auto-pickup with rarity filter)
- `user_role.md` — owner role + project framing

## 🔗 Doc cross-references

**Strategic anchors + engine queue:**

- **`29-design-overview.md`** — strategic anchor (scope, two-engine architecture, four-track model)
- **`28-engine-arpg-rebalance-design.md`** — the engine queue this roadmap operationalizes
- **`30-engine-explainer-current.md`** — engine as it ships today (current-state baseline for Track A)
- **`31-engine-explainer-future.md`** — engine target state after Track A closes
- **`32-progression-design.md`** — progression system design discussion (Stage A7 input; all 12 sections RESOLVED 2026-05-12)
- **`33-progression-skeleton.md`** — progression skeleton (immutable + decided only; Stage A7 deliverable spec)
- **`09-geometry-palette-discussion.md`** — palette decisions (2026-05-08 + Revision 2026-05-11)
- **`17-gear-and-spirit-guide-design.md`** — gear + Spirit Guide design (Priority 02 origin)
- **`19-llm-call-map.md`** — LLM call topology (per-season call inventory)
- **`34-monster-design-phase0-vs-production.md`** — monster design distinction

**Form-bias + Substrate Realignment workstream:**

- **`37-form-bias-diagnosis-and-recovery.md`** — origin diagnosis of humanoid-form structural bias; Position C + Position (ii) locked
- **`37-engine-and-game-two-products.md`** — engine + game two-products framing (numerical-prefix collision with file 37 form-bias doc is intentional; both 2026-05-15 era)

**Canonical story (gandalf) — L2 project cosmology + design framework:**

- **`canonical/story/cosmology-reincarnated.md`** — Wheel / Earth Self / Spirit Guide / seasonal descent / Rift / third-faction
- **`canonical/story/court-of-forms.md`** — Court framing (8 structural commitments)
- **`canonical/story/naming-triad.md`** — anchor → spirit name → embodiment-flavored name
- **`canonical/story/style-register.md`** — HD-2D-shaped pixel-art lock + score-don't-filter principle
- **`canonical/story/enemy-visual-legibility.md`** — enemy design legibility rules
- **`canonical/story/embodiment-narrative-layer.md`** — embodiment as narrative skin on mechanical substrate
- **`canonical/story/engine-generic-meta-structure.md`** — three-layer model (L1 / L2 / L3); pitch-supporting layer-separation
- **`canonical/story/spirit-guide-voice.md`** — voice spec for Spirit Guide character
- **`canonical/story/trial-moment-ritual.md`**, **`canonical/story/passage-moment-ritual.md`**, **`canonical/story/ascension-moment-ritual.md`** — moment-ritual canonical docs
- **`canonical/story/season-feel-rubric.md`** — rubric for evaluating season feel quality
- **`canonical/story/drift-audit.md`** — drift-7/8/9 identification; resolved via engine-balance-stewardship
- **`canonical/story/engine-balance-stewardship.md`** — locks View A, multi-dimensional divergence framework, movement-modeling limitation
- **`canonical/story/pre-llm-substrate-inventory.md`** — 53-item catalogue in 5 clusters; terminology lock; prerequisite for form-bias-cadence-strategy doc
- **`canonical/story/form-bias-cadence-strategy.md`** — **IN FLIGHT**; commission active

**Orchestration:**

- **`agentic_orchestration/AGENTS.md`** — 9-entity team topology + authority tiers + viability-gate workflow
- **`agentic_orchestration/GOVERNANCE.md`** — founding ADRs
- **`agentic_orchestration/REVIEW_PROCESS.md`** — Gate-1 / Gate-2 review process + 5 principles
- **`agentic_orchestration/CHANGELOG.md`** — team-level event log

**Historical / external:**

- **`../collaboration-handoff/22-three-js-demo-and-data-export.md`** — historical demo plan (largely superseded by demo1 ship)
- **`../family-review/demo1-progress-tracker.md`** — demo1 execution history
- **`pitch-2026-05-18/one-pager.md`** — marketing pitch (May 18 meeting); references engine licensing claim that engine-generic-meta-structure.md operationalizes

---

## 📝 How to update this doc

This roadmap should be revised when:

- A stage closes (move from "in-flight" to "complete"; update timeline; note the actual cumulative effort)
- A new stage is discovered (rare for Track A now that file 28's queue is fully scoped; common during Track B if a new prototype is needed)
- A decision lands (move it from "open" to "closed/locked")
- An estimate shifts materially (re-tune the timeline table)

**Don't rewrite history.** When a decision changes, add the new decision to "closed" and link to the supersession entry in the decisions log. Memory files retain the historical record.

**Update the "Last updated" date** at the top whenever the doc is touched substantively.
