# 16a — Roadmap Shipped Log

**Purpose:** Historical record of what's shipped, sub-progress detail, closed/locked decisions. Companion to `16-project-roadmap.md` (forward-looking).

**Stewardship:** gandalf appends to this doc when sub-items close. Append-only by convention; corrections via strike-through rather than deletion.

**Last appended:** 2026-05-16 (Day 4 close — restructure capture; today's shipped sub-items folded in)

---

## ✅ Stage A1 — Pre-sprint design + small fixes (~5-8 hrs)

**Status:** COMPLETE 2026-05-12. Shipped on `stage-a2` branch (5 commits).

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
- B6: `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- B13: `cast_time`, `damage_resolution_time`, `i_frame_window`
- B14: `convergence_report` (nested band fields)
- B15: `set_id`, `set_position`, `set_piece_count_required`
- All default to None/[]/{} — existing 5 seasons load without regen

**Absorbed into Stage A2:**
- A1 combo cost clamp → B6 generator refactor side-effect
- A1b focus cost calibration → B6 generator refactor side-effect
- A2 per-skill geometry dimensions → B11 geometry palette expansion
- A4 shield magnitude scaling → A4 decision locked (HoT-style); implementation in B6 sim cleanup

---

## 🚧 Stage A2 — In-progress sub-shipped log

Stage A2 is the coordinated ARPG-genre sprint (B6 + B7 + B10 + B11 + B12 + B13 + B14 + B14.5 + B16). Multiple sub-items have shipped against this stage; remaining items return to scope after VS2a/VS2b ship.

### Sub-items shipped

| Sub-item | Tag | Shipped |
|---|---|---|
| B10.1 — Tier structure + Model B gauntlet | `v1.3-b10-1-structure` | 2026-05-13 |
| B10.2 — PackProxy + swarm composition (later superseded by B10.4 Option 2 framing) | `v1.3-b10-2-pack-proxy` | 2026-05-14 |
| B14.5 V1 — Recompose-first primary loop (canonical pattern locked) | folded into related tags | 2026-05-12 |
| B10.4 — Swarm calibration / convergence binary-search refactor (Option 2) | `v1.3-b10-4-swarm-calibration` | 2026-05-16 |
| Telemetry tier-1 extension (cross-seam; star-lord) | `v1.3-telemetry-tier1` | 2026-05-16 |
| **Form-bias Stage 1 — embodiment-axis additive fields** (rocket) | `rocket/v1.3-form-bias-stage-1-embodiment-axis` | 2026-05-16 |
| **Form-bias Stage 2 — grouping-layer (abstract pair-structure)** (rocket) | (intermediate) | 2026-05-16 |
| **Form-bias Stage 1+2 fields wired into `_class_to_dict` serializer** (star-lord) | `4bbc906` | 2026-05-16 |
| **Grouping-layer vocabulary v1.1 lock** (gandalf) | `ea3a1c3` | 2026-05-16 |
| **B11 — Geometry palette expansion (generator side; 16 → 25 active types)** (rocket) | `ec31682` | 2026-05-16 |
| **B11 — Sim-side geometry resolution (9 new types + 4 Track-4 collapses)** (gamora) | `0278fba` + `gamora/v1.3-modifier-clamp-gate` | 2026-05-16 |
| **B11 — Demo render integration** (drax) | `drax/v0.15` | 2026-05-16 |
| **Modifier-clamp gate** (gamora) — surface+flag for anomalous modifiers (Discipline #10) | `7a382f3` | 2026-05-16 |
| **V2.1 per-fight emission gap fix** (gamora) | `df717a8` | 2026-05-16 |
| **Spatial-data persistence for class_fight_loadouts** (star-lord) | `0149bfa` | 2026-05-16 |
| **Recorder fail-loud-on-silent-drop** (star-lord; Drift-12 / Pattern P7 prevention) | `9baa4f8` | 2026-05-16 |
| **Cipher-migration paths-audit** (star-lord; 48 sites; 26 LEAK-RISK; 18 newly-surfaced) | `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` | 2026-05-16 |
| **Pimen ingest pipeline + bundle archive support + ELEMENT_SLOT_MAP real-mapping fix** (drax) | `drax/v0.13`, `v0.14` | 2026-05-16 |
| **Room/hallway arena topology** (drax; supersedes single-ellipse) | `drax/v0.12-room-hallway-geometry-system` | 2026-05-16 |
| **Pimen first VFX integration proof-of-concept** (drax; 5-pack) | `drax/v0.11` | 2026-05-16 |
| **Pimen bundle-matcher corrections** (drax; per-animation-subfolders + bundle_folder_hint) | `drax/v0.16` | 2026-05-16 |
| **Wave-4 pack-composition tuning** (rocket; per-room-variant range-profile bias) | `3c898a3` | 2026-05-16 |
| **Wave-4 small-room range-profile filter** (drax; TS port of rocket engine rule) | `drax/v0.17` | 2026-05-16 |

### Sub-items remaining for Stage A2 closeout (post-VS2a/VS2b)

| Sub-item | Scope | Estimate |
|---|---|---|
| **B6** Class kit composition + Hierarchical Skill Tree + energy-type-aware tier assignment | Element distribution, geometry mix, AOE coverage, role coverage per archetype; tree structure (4 tiers × 2-4 chains); hierarchical unlock gates; cross-chain asymmetry. B6 pre-work (rocket) — energy-type-aware tier bounds; main (gamora). | ~3-5 weeks engine + 1-2 weeks balance re-tune + 1-2 weeks rocket pre-work |
| **B7** Gear-percentile variance check | Pass/fail gate at 50th/75th/95th/99th; runs at endgame L50 | ~1-2 days engine |
| **B10 V2** Sequential-room semantics | HP carryover between encounters; required for AOE differential goal | ~7-12 hours engine; targets VS2a |
| **B12 full audit** | Boots/gloves/belt gear slots + +% MS affixes + hard-cap design | ~1.5-2.5 weeks |
| **B13** Active mobility + telegraphs + i-frames + emergence observability | 5 new defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance); cast_time + damage_resolution_time + i_frame_window fields; demo telegraphs + asymmetric indicator scaling | ~3-4 weeks engine + demo + regen |
| **B14** Multi-band convergence simulator | 3-band act-aligned discrete convergence at L17/L33/L50; 9 runs per class; per-band optimal distributions; recompose-first failure handling | ~2-3 weeks engine |
| **B16** Loot drop architecture | Drop event + per-band rarity tables + per-monster-tier multipliers + smart-loot 70/30 + ilvl tracking + drop pool + telemetry; demo: drops render + auto-pickup with rarity filter | ~1.5-2.5 weeks engine + demo |

**Co-dependency notes:**
- B6 alone (kit composition rules) without B10 → balance loop pushes back to single-target through convergence pressure
- B6 + B10 without B11 → kit-variety crunch on heavy-AOE archetypes
- B11 alone → richer palette but generator doesn't know how to use it
- B7 (variance gate) needs the restructured gauntlet (B10) to test against
- B16 needs B10 (monster tiers) + B12 full gear slot list; B14's variance check needs B16's actual drops

### Stage A2 yellow-flag investigations (resolved)

- **Modifier range 0.09–0.52 — RESOLVED 2026-05-16 by gamora investigation.** Not a tuning defect, not a regression, not Option 2's fault. Root cause: sim-side combat mechanics (rage starts at 0 / mana starts full; physical miss ~15% / elemental always hits; armor ~18.6% vs resistance ~0%). Generation produces equivalent power budgets; sim produces different effective DPS. File-29 0.85-1.15 target band was a design aspiration for when B14.5 is fully operational; never calibrated against actual sim. **Mitigation: declare 0.09-0.52 as the B10.4 Option 2 calibration epoch (current mean |mod−1.0| ≈ 0.82); progress tracking target ≈ 0.50 after B6 pre-work + B14.5 V2.** Math: `reincarnated-engine/simulation/math/modifier-range-root-cause.md`; findings: `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md`; commit `436edc4`.
- **Tier-1 telemetry coverage gap — RESOLVED 2026-05-16.** Coverage was ~3.4% on existing seasons; star-lord investigation found code-path divergence in fight_engine bypassing Tier-1 writes from gamora's regen loop. V2.1 per-fight emission gap fix (`df717a8`) addresses the engine path; V2 CLI flag + V2-mode regen dispatch sequenced to validate end-to-end.

---

## 🔒 Closed/locked decisions reference

Decisions listed here are settled — recorded here so they're not re-litigated. For full decisions-log text, see `~/Games/reincarnated-engine/design/decisions/decisions-log.md`.

### Architecture + strategic

- **Math engine as project spine** (2026-05-07)
- **Convergence pattern as QA mechanism** (2026-05-07)
- **Three.js for prototype, Unity for production** (2026-05-07) — later updated 2026-05-12: demo1 is Pixi.js; Unity deferred to production-polish phase
- **Father-son project framing** (2026-05-07)
- **Canonical pairing replaces "encryption key"** (2026-05-07)
- **Bounded scope discipline for Phase 0/1** (2026-05-07)
- **NullRecorder pattern for telemetry** (2026-05-07)
- **Two-engine architecture** (Engine 1 content gen + Engine 2 world gen) — file 29
- **Shaped-balance philosophy** (composition first, numbers last) — file 29
- **Dimensional generation** (Option C with five axes)
- **Engine + game two-products framing** (2026-05-15) — `canonical/37-engine-and-game-two-products.md` + `engine-generic-meta-structure.md`; L1 / L2 / L3 separation; supports B2B licensing claim

### Gameplay design

- **Body swap mechanic gates on Trial defeat** (2026-05-07; superseded 2026-05-08 by spirit-swap and form library framing — Trial defeat granting access preserved; framing refined)
- **Canonical element palette** — physical / fire / wind / water / earth / hybrid; no expansion, no per-season rotation. **Under live re-examination via Substrate Realignment workstream;** operative until form-bias-cadence-strategy Q4 supersedes via decisions-log entry.
- **Geometry palette revised 2026-05-11** — 25 active types via B11; un-defers whirlwind/dash_attack/leap_strike; parameter-expansion over type proliferation. See canonical/09 § "Revision 2026-05-11" + "Revision 2026-05-11 (B13 extension)".
- **B9 endgame baseline** — level 50, 120-point skill budget, per-skill cap 15, kit size 10-15, trait floors 1/12/25/38
- **B9c reset model** — strict during play, paid endgame
- **B5 hotbar pattern** — 7th slot for granted abilities (not replace-existing)
- **Solo gameplay for Phase 0 seasonal play** — multiplayer envisioned for post-Phase-0 Earth meta-layer rift events
- **3 acts locked** (2026-05-11) — per-act bands A1: L1-17, A2: L18-33, A3: L34-50

### 2026-05-16 cluster (Day 3-4 — the largest single-day landing)

- **View A locked as AOE balance philosophy** — multi-dimensional divergence framework (floor / ceiling / experienced-cost-parity); movement-modeling abstraction limitation named; Stage A2 sim extension scheduled. B10.2 "Convergence = full fidelity" SUPERSEDED.
- **B10.4 Option 2 modifier baseline declared the operational calibration epoch** (mean |mod-1.0| ≈ 0.82); file 29 0.85–1.15 band reclassified as full-system aspirational target
- **B10.2 Two-Gauntlet Pattern superseded** — Option 2 (exclude pack fights from convergence binary search) is the canonical pattern
- **Court of Forms canonical** — 8 structural commitments + meaning-of-the-arc statement
- **Enemy visual legibility canonical**
- **Style register locked: HD-2D-shaped pixel-art** — operational precision rules + score-don't-filter catalogue principle
- **Naming triad locked** — anchor → spirit name → embodiment-flavored name; player-facing labels Trial / Mirror / Passage
- **research.db retired** — `scripts/db.py` deleted; elrond is data steward for external data; catalogue.db is successor
- **Pimen catalogue full crawl complete + viability gate PASSED** — three-track review (gandalf design / elrond structural / drax wiring); 46 distinct packs catalogued
- **Form-bias strategic-axis locked as explicit-hybrid Phase-0** — ARPG-canon-primary at substrate-mechanical layer + Isekai-canon-primary at narrative-skin and convergence layers; Position C reaffirmed; four catalogue-track sub-locks explicitly deferred
- **Form-bias architecture lands as three-layer model** — substrate / grouping / vocabulary; cipher-width framework explicit with width itself deferred to catalogue-mapping experiment
- **Four form-bias sub-locks explicitly deferred** to catalogue-track empirical gates — cipher-width, Foundation layer placement, D1 rubric reconsideration, per-season vocabulary coupling policy
- **Disciplines #13a (implementation-vs-intent drift), #13b (outcome attribution opacity), #14 (internal-vs-generative schema separation) codified** in engineering-disciplines.md; terminology lock formalized
- **Form-bias migration cadence — Option II (Parallelized) locked** as the staged sequence; four-stage backbone + per-stage gate definitions
- **Ailment-damage-signatures deferral made indefinite** (post-B14.5 V1 doppelganger gate re-run HIGH signal); demoted from engineering queue to design-polish queue
- **Cipher-width sub-lock resolution — Outcome 2** (single classical-element-anchored grouping) + Foundation L2 + per-season vocabulary coupling β + D1 reconsideration scope conditional on Flag A
- **D1 reconsideration scope — bounded entry-by-entry review** (per Flag A AMBIGUOUS verdict); Q1 process-exception + Q4 syllable-cap surgical amendments queued
- **Movement-speed baseline locked (Option A — SUPERSEDED same day by Option B verdict reversal)** — ~~player base 5.75 m/s + mid-VS2a 7.5 m/s~~ + late 8.0 m/s; monster trash 5.75 m/s + ~~fast archetypes 6.6-7.5 m/s~~; PIXELS_PER_METER=48; ~~AI_SPEED_MULTIPLIER=0.767 (VS2a)~~; range-profile MS variance dropped; design family D3/D4/Last-Epoch
  - **→ SUPERSEDED 2026-05-16 Day 4 evening by Option B verdict reversal:** VS2a default rebased to **end-game-anchored** values per Matt direct directive (*"No point playing a game which is not ran through the sim"*). Operational values: player 8.0 m/s; monster trash 5.75 m/s (unchanged); fast archetypes 7.5 m/s (top of locked range); **AI_SPEED_MULTIPLIER=0.719** (5.75/8.0). Sim consumption (gamora Gate 3b) moved from "post-VS2a tight follow" to **VS2a-gating**. See `canonical/story/movement-speed-baseline.md` § "Verdict Reversal" + decisions-log Option-B supersession entry (drafted; in flight via knight-rider). VS2a framing change: end-game playtest, not mid-game playtest; early-game pacing deferred to Playtest Cycle 1.
- **Spatial-data JSON-schema locked** — hybrid architecture (continuous-coordinate at combatant + shape-descriptor at floor + tile-grid forward-compat); unit meters; PIXELS_PER_METER=48 preserved; per-encounter dimension library (32.7×14m trash / 28×28m elite / 40×24m boss / 50×30m act-boss); `movement_profile` enum (6 initial values); 6-step implementation cascade
- **DPS-floor for `wind_controller` templates — DEFERRED** with re-evaluation gate (three-condition trigger: post-regen modifier >3.0 / clamp-gate >2 control classes / playtester feedback)
- **VS2a arena adopts Diablo/PoE interior room model** — square rooms (15-45m, 30m default) + rectangular hallways (6-10m wide); per-room aggro state machine (dormant → active → cleared); Door Mode B (free traversal); no cross-room aggro. Supersedes single-ellipse `clampToEllipse`.
- **Grouping-layer vocabulary locked** — form-bias Stage 2 Layer-2 cipher abstract pair-structure labels (ignition / suffusion / bulwark / displacement / impact); thermal + positional axis pair-structure; impact as non-pair Foundation slot; GROUPING_LAYER_VERSION v1.0 → v1.1
- **Geometry type collapses confirmed** — 4 canonical-09 types collapsed to behavioral flags (projectile_homing → flag, aura_directional → cone+falloff, melee_cleave → sweep_shape, iframe_dash → i_frame_window metadata); B13 animation primitives deferred; VS2a B11 GREEN list locked at 11/13 elements; acid deprioritized (Pimen-SPF); void deferred (Pixogen license); Discipline #13a remediation

---

## 📋 Stage detail (forward reference)

Per-stage scope detail for B-items beyond Stage A2 closeout. These are forward-reference; updated when stages activate.

### Stage A3 — Trait + skill-point + reset architecture (B9 series)

Layers on top of B6 (Stage A2). Cannot ship before Stage A2.

| Item | Scope |
|---|---|
| **B9a** Trait architecture | Per-class trait pool (5-10 traits); varied acquisition floors (1, 12, 25, 38); per-rank power curves calibrated so all traits reach similar power at character level 50; endgame-baseline framing |
| **B9b** Skill point distribution | 120-point endgame budget; variable 10-15 skill kit per archetype; per-skill cap 15 (allows ~8 maxable, forces specialization); per-skill scaling coefficient engine-determined |
| **B9c** Build reset mechanism | Strict during play: free reset only under specific triggers (struggling → Spirit Guide guided reset; body swap; end-game; refused body swap; Spirit Guide proactive at act-transition). Paid endgame reset |

**Decisions still open:** struggling heuristic tuning; Spirit Guide build-coach UI surfacing; divergence-heuristic threshold for proactive act-transition reset.

### Stage A4 — Legendary gear abilities (B5) + Seasonal Sets (B15)

**Engine work:** schema additions to gear (legendary-only): `granted_ability` on weapons (7th hotbar slot), `aura` on armor/shields/accessories (passive tick), `on_hit` on weapons (chance proc), `cast_on_attack` (deterministic Nth-attack trigger). Generator gates which abilities fit which slots. Convergence loop accounts for legendary builds.

**Demo work:** hotbar handling for 7th slot, aura ticking, VFX + audio for granted abilities, tooltip surfacing.

**Decisions still open:** Aura stacking rules — cap on simultaneous tickable auras? Power budget shift — legendary stat decrease to compensate for granted-ability power; how much?

### Stage A5 — Small balance items

- **B1** WIS-on-heal multiplier — currently 0.002 (30% bonus at 151 WIS); raise to 0.005 (75% bonus) or keep as utility-stat design? ~30 min
- **B2** Per-skill ailment chance scaling — currently flat 0.35; design: high-cost ults → 100%, mid → 35%, low spam → <0.35. ~1-2 hrs

### Stage A6 — Category C deep-cuts (deferred)

| Item | Scope | Trigger to commit |
|---|---|---|
| **C1** Multi-target dispatch in sim | Engine becomes n-vs-m aware; `resolve_skill` accepts defender list; convergence loop becomes density-aware | If demo's invented pack semantics create concrete engine-demo divergence pain |
| **C2** Knockback consumer in sim | Engine has knockback as stub; needs positional consumer | Trivial follow-on if C1 ships |
| **C3** Convergence-target reshaping for horde | Density-aware convergence (kills/minute, time-to-clear-wave) vs current binary 50% win rate | Only meaningful if C1 ships |

### Stage A7 — Progression system implementation

Design FULLY RESOLVED 2026-05-12. All 12 sections of file 32 LOCKED. Sections: progression philosophy / character level curve / stat point progression / ability acquisition UX + Hierarchical Skill Tree / gear progression + Seasonal Sets / enemy + monster scaling / Character-Enemy-Monster alignment validation / engine simulation update (Option β multi-band) / death penalty + body-swap pool dynamics / per-act content scaling / quest as XP / movement + mobility + active evasion.

**Scope:** XP curve (smooth polynomial level^2.0-2.5); stat auto-allocation per class identity; Hierarchical Skill Tree UI; trait acquisition floor unlocks + auto-rank with character level; multi-band Spirit Guide build coach (consumes per-band optimal_distribution from B14); Spirit Guide proactive act-transition reset (>30% divergence trigger); body-swap pool tracking; doppelganger encounter integration (Trial alternative path); end-game quest for doppelganger-path reward reclaim; cross-season smuggling integration; loot economy validation simulation; ilvl tracking on gear; auto-pickup with rarity filter; form library ascension at season end (≤1 per season).

---

## 🧭 Navigation (when sitting down to work)

**Engine work:**
1. Pick the next stage. VS2a + VS2b are the active milestones; remaining Stage A2 items return post-VS2.
2. Resolve pending decisions for that stage before code. Forward-looking roadmap (`16-project-roadmap.md` § Open design decisions) lists what's open.
3. Reference file 28 for full item specs, cost breakdowns, sub-item details.
4. Reference file 31 for target-state projection; file 30 for current-state.
5. Follow the landing rhythm (`16-project-roadmap.md` § Track A landing rhythm).

**Demo work post-engine-stage:**
1. Reference file 28 § "Demo-side override removal plan" — canonical map of demo override → engine queue item.
2. Remove the overrides this stage retires.
3. Verify engine-faithful behavior (file 28 § "Verification rubric").
4. Regenerate seasons + replace `/public/assets/seasons/`.
5. Smoke test the 5-season playthrough.

---

## 📚 Memory cross-references

For deeper context on specific items, see memory files in `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/`:

- `project_reincarnated_engine.md` — engine state + architectural direction
- `project_engine_state_findings.md` — empirical findings, recurring lessons, accumulating concerns
- `project_design_intent.md` — spirit-swap, trial room, class scoping intent
- `project_geometry_palette.md` — geometry palette decisions (Phase 3 + B11)
- `project_role_orientation_taxonomy.md` — Phase 2 role decision
- `project_progression_concept.md` — Priority 14 historical sketch (superseded by B9 series + file 32 / 33)
- `project_gear_and_spirit_guide.md` — Priority 02 gear architecture + Spirit Guide engine API
- `project_earth_meta_layer.md` — Earth Self meta-layer design intent (far-future)
- `project_pet_system.md` — pet system design intent (deferred to focused later sprint)
- `user_role.md` — owner role + project framing
