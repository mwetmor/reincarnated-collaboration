# 16 — Project Roadmap (forward-looking)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Last updated:** 2026-05-21 (gandalf — QD-engine rebuild chapter added as next-major-initiative; VS2a/VS2b superseded by rebuild plan)

**Stewardship:** Forward-looking roadmap stewardship sits with **gandalf** (story + design steward) — the WHY/WHAT. **Knight-rider** feeds the IS-vs-IS-STATED drift signal as a mechanical input. Mechanical updates by gandalf directly; recommendations touching locked design positions route through Matt via decisions-log Gate-1.

**Companion docs (this doc's purpose: only what's active or upcoming):**
- **`16a-roadmap-shipped-log.md`** — historical record of what's shipped, sub-progress, closed decisions
- **`16b-roadmap-archive-restructures.md`** — meta-history of roadmap restructures + scope migrations

**Strategic anchor:** `29-design-overview.md` answers "what is Reincarnated as a finished game?" When in doubt about scope, consult file 29. When in doubt about engine queue specifics, consult file 28.

---

## 🌟 Major architectural commitment (2026-05-21) — QD-engine rebuild

After the recompose-validation hive (closed 2026-05-20) verdict — CANNOT REJECT NULL; kit-composition pathology IS the load-bearing problem — Matt committed to the architectural answer: **rebuild the engine as a Quality-Diversity (QD) optimizer with substrate-as-cohesion architecture.**

**Canonical document stack (read in order):**

1. `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — vision (QD-engine + 4 profiles + IDC meta-principle)
2. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — operational spec (8 BC axes × 68,040 cells)
3. `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architecture (substrate identity is post-generation coalescence, NOT generation constraint)
4. `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — 8-phase workflow with Profile A/B/C/D touchpoints
5. `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — 8-phase execution plan (P0-P7; 24-37 weeks)

**Audit deliverables synthesized into rebuild plan:**

- Legolas Phase 1 substrate-sufficiency audit (`agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/`)
- Jack-ryan legacy constraint audit (`agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/`) — 62 constraints, 12 HIGH-risk
- Rocket Alt A substrate-generalization study (`agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/`) — Pattern-A generalizes universally

**Knight-rider activation dispatch:** `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md`

**Matt-resolved decisions (D1-D6 + post-protocol refinements):**

| ID | Decision |
|---|---|
| D1 | Unity render pipeline: URP |
| D2 | Phase 0 element scope: 7 elements (fire/water/earth/wind/lightning/holy/shadow) |
| D3 | Cohesion-BC sequenced post-cipher migration |
| D4 | BC Axis 2 measurement: all fights, fight-context-tagged |
| D5 | Foundation validator: 7-substrate |
| D6 | Vision-layer geometry gaps documented for v1.1; do not block P0 |
| Substrate-as-cohesion architectural recommitment | Generation substrate-agnostic; cohesion-judge assigns substrate/element/theme post-generation |
| Shadow = trade-off (cohesion theme) | ARPG canon: D2 Necro, D3 WD, D4 Necro Sever, PoE Blood Magic; Solo Leveling shadow extraction |
| Physical = warcry/shout exception (cohesion theme) | D2/D3/D4 Barbarian canonical |
| Holy = aura self-amplification primary | D2 Paladin, D3 Crusader, PoE Guardian canonical |
| Reincarnated-game Unity production initiative | New repo at `~/Games/reincarnated-game/`; Meshy 6 pipeline replaces Mixamo for humanoids |
| Dual-render Profile A | Pixi.js 2D (existing demo) + Unity 3D (reincarnated-game); missing sprites acceptable |
| Kit-redesign queue CANCELED | Contradicts QD-engine philosophy; 12-archetype list preserved as P7 W7.2 reference roster |
| § 2.8 Skill tree node population P1 W1.13 (NEW WORKSTREAM) | Procedural per-class-per-season ~120-node trees; multi-dim convergence over node-subset × coefficients × modifier; resolves Pattern-A compression mathematically |
| § 2.9 Gauntlet architecture | Single implementation (true multi-monster positional swarms); PackProxy ×8 retired; P7 certification is archive query, NOT gauntlet re-execution |

**Phase plan (P0-P7; estimated 24-37 weeks total):**

| Phase | Name | Duration | Critical work |
|---|---|---|---|
| P0 | Constraint removal + drift cleanup | 3-4 weeks | 12 HIGH-risk LCs resolved; B6 energy-type fix; archetype refactor; foundation validator (7-substrate); W0.9 gauntlet migration |
| P1 | Substrate enrichment | 5-8 weeks | Ability schema extensions; HP-econ + charge-stack + damage-converts substrate; W1.13 skill tree node population |
| P2 | BC measurement infrastructure | 3-4 weeks | All 8 axes operational; Discipline #17 calibration |
| P3 | MAP-Elites archive implementation | 2-3 weeks | Pareto / crowding / Mahalanobis / hypervolume / KL gates |
| P4 | Sim extensions for deferred bins | 4-6 weeks | Proxy / dodger sub-cases / charge / damage-converts / channel mechanics |
| P5 | Theme coalescence + cohesion-BC + visual-BC | 3-5 weeks | LUCB1; joint-gate (Discipline #18); cipher migration coordination |
| P6 | Profile assembly layer | 2-3 weeks | All 4 profiles (A/B/C/D); coreset + submodular packaging |
| P7 | Validation gauntlet + production cutover | 2-3 weeks | Reference-archetype certification via archive query; Profile A ship |

**Profile A near-term ship windows:**
- P3 reduced-cell-space ship (~11-16 weeks): 25,920 cells; missing summoners/stealth/blood-magic/charge-stack/damage-converts archetypes
- P4 full-cell-space ship (~15-22 weeks): 68,040 cells; full ARPG archetype roster

**Parallel reincarnated-game initiative:** Multi-month Unity 3D production; Meshy 6 pipeline; ships independently of QD-engine rebuild timeline.

**Queued assessment (does not block P0):** Monster thematic depth (Legolas + Galadriel + Gandalf synthesis; per `agentic_orchestration/dispatches/2026-05-21-monster-thematic-depth-assessment.md`)

**Stewardship under rebuild:** Knight-rider orchestrates the QD-rebuild hive autonomously per protocol § 7. Gandalf decides cross-cutting design; jack-ryan critique-pair gating; Matt approves structural changes + production cutover only.

---

## 🎉 Where we are right now (2026-05-21 close; pre-rebuild)

| Component | State |
|---|---|
| Demo1 v1.2 | Shipped to Vercel (`reincarnated-demo.vercel.app`); desktop + mobile |
| Loadout app | v0.8 shipped; built against real telemetry post-tier-1 |
| Engine telemetry-tier-1 | Shipped (`v1.3-telemetry-tier1`); schema V2.0 |
| Engine Stage A2 | **~40% complete** — B10.1/B10.2/B10.4/B11/B14.5 V1 shipped; B6/B7/B12/B13/B14/B16 in flight or queued |
| VS2a (Gauntlet + Geometry + First Catalogue) | In-flight; arena topology + B11 + movement-speed-baseline + Pimen first VFX shipped today; B6 + B10 V2 + character-track gate ship |
| VS2b (Substrate Realignment + Full Catalogue) | In-flight in parallel; Stage 1 (embodiment-axis) + Stage 2 (grouping-layer) shipped today; Stage 3 (cipher migration) dispatched |
| Production seasons | 5 (1001-1005) against current engine; regen after VS2a/VS2b ships |

**Active focus:** VS2a + VS2b in parallel (Matt-locked 2026-05-16). See dedicated sections below.

**Team:** 9 entities — knight-rider (orchestrator), gamora / rocket / star-lord (engine seams), drax (presentation), jack-ryan (technical/process QA), gandalf (story + design steward), legolas (research + catalogue), elrond (data steward). Authority tiers + viability gate per `agentic_orchestration/AGENTS.md`.

---

## 🛤️ The four-track work model

| Track | Status | What it is |
|---|---|---|
| **Track A — Engine 1 maturation** | Active | Close the file 28 queue; iterate engine + demo regeneration cycles |
| **Track B — Engine 2 prototyping** | Intermittent | Validate Engine 2 design slices before committing to full build |
| **Track C — Engine 2 build** | Future | Town + acts + dungeons + quests + NPCs to shippable quality |
| **Track D — Integration + ship** | Future | Reincarnated v1.0 — the full game |

Track A is the active line. **The two near-term VS2 milestones below are the operational focus.**

---

## 🎯 VS2a — Gauntlet + Geometry + First Catalogue Integration

**Strategic frame.** Player drops into a Diablo/PoE-style room sequence, fights tier-diverse encounters with new geometry shapes, sees real VFX on hits, moves at coherent speed. **Playtest-validatable slice ANCHORED TO END-GAME BALANCE STATE** (Matt verdict reversal 2026-05-16 Day 4 close per `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"). The gauntlet shows the player what end-of-progression feels like; sim and demo agree on the same values; what the player feels IS what the engine balanced for. VS2a does NOT cover early-game pacing (that's Playtest Cycle 1 post-Stage-A2-closeout).

**Estimated working effort:** ~3-4 months from VS2a kickoff (mid-May 2026). Drax is the binding-constraint seam.

### Scope — what gates VS2a ship

| Item | Owner | Status |
|---|---|---|
| Movement-speed baseline **(end-game-anchored per Matt verdict reversal 2026-05-16 Day 4 close)** | rocket + drax + gamora | ✅ Option-B values locked (player 8.0 m/s; trash 5.75; fast 7.5; AI_SPEED_MULTIPLIER 0.719). Rocket schema-default-update pending; drax demo MS pending engine-emitted JSON consumption (precondition: Stage B export-DTO fix); **gamora Gate 3b sim consumption NOW VS2a-GATING** (was post-VS2a tight follow) |
| Room/hallway arena topology (replaces single-ellipse) | drax | ✅ Shipped (drax/v0.12) — Diablo/PoE square rooms 15-45m + hallways 6-10m; per-room aggro |
| B11 — Geometry palette expansion (16 → 25 active types) | rocket + gamora + drax | ✅ Generator (rocket) + sim (gamora) + demo (drax/v0.15) all shipped today |
| B11 GREEN-list element VFX (11/13 elements; first Pimen integration) | drax + elrond | In flight; Pimen ingest pipeline shipping iteratively (drax v0.13–v0.17) |
| **B6 — Class kit composition + Hierarchical Skill Tree** | rocket (pre-work) + gamora (main) | Pre-work dispatch authored (energy-type-aware tier assignment); main work depends on pre-work |
| **B6 skill-tree UI surface** | drax (dispatch not yet authored) | 🔴 **CRITICAL gap** — engine emits tree data; demo has no surface to render it. Per P6 forward audit. |
| **B10 V2 — Sequential-room semantics with HP carryover** | gamora | Sim-side gauntlet structure; visual now matches via drax room/hallway ship |
| **Character rendering for player combatants** | drax (dispatch authored today) | chierit Elementals zip archives acquired; per-class character rendering. Closes P6.d. |
| **Pool × VFX-catalogue mapping audit (Drift-14 closure)** | legolas + gandalf + rocket | 🔴 **VS2a-GATING** per Matt verdict 2026-05-17 (*"I really don't want to ship any more canonically biased seasonal themes"*). Commission at `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md`. ~1.5-2 days work; closes Substrate Realignment Stage 1 player-facing canonical-bias gap at the per-season vocabulary surface. Folds into VS2a regen cycle. |
| **Environment tileset catalogue sweep + VS2a pack selection (Drift-15 closure)** | legolas + gandalf + Matt + drax | 🔴 **VS2a-GATING** per Matt direct catch 2026-05-17 (*"the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls... This could REALLY make the difference in the demo"*). Commission at `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`. Closes the FOURTH P6 instance — environment third visual axis was implicit-deferred without being named as a deferred axis. Track A legolas Mode B environment-tileset sweep ~5-8h; Track B gandalf framework ~2h; Track C Matt selection ~30 min; Track D drax integration ~3-5 days (separate downstream dispatch). |
| Demo regen on a single season **(post-pool-cull)** | star-lord + gamora | After all above land — INCLUDING Drift-14 pool cull |

### Out of scope for VS2a (deferred)

B7, B12 full audit, B13, B14, B16. Substrate Realignment work and full Pimen integration are explicitly in VS2b.

**Explicit non-coverage (end-game-anchor framing).** VS2a is deliberately framed as an **end-game playtest** per the 2026-05-16 Day-4 verdict reversal (see `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"). The gauntlet ships end-game-balance state (player 8.0 m/s, fast-monster 7.5, AI_SPEED_MULTIPLIER 0.719); sim and demo agree on the same values via engine-emitted JSON. **VS2a does NOT validate early-game progression feel** — that question is deferred to **Playtest Cycle 1 (post-Stage-A2-closeout)**, after B12 full audit lands and player MS becomes an earned axis of gear investment. Playtest reports on VS2a must not claim early-game pacing coverage.

### Seam allocation

| Seam | VS2a work | Capacity |
|---|---|---|
| gamora | B6 main; B10 V2 sequential-room; **Gate-3b sim MS extension (NOW VS2a-GATING per 2026-05-16 Day-4 verdict reversal)** | Modifier-clamp gate complete; B11 sim shipped; B6 next; Gate-3b sequenced behind rocket schema + star-lord export DTO fix |
| rocket | B11 generator (shipped); B6 pre-work; MS schema (shipping) | B11 + Stage 1 + Stage 2 shipped today; B6 pre-work next |
| drax | B11 demo (shipped); Pimen ingest + first VFX integration; MS implementation; character-track ingest; B6 skill-tree UI (open) | **Most loaded.** |
| elrond | Pimen curation pipeline; subset selection | Pipeline in flight |
| star-lord | V2 CLI flag + regen; telemetry support for B6 convergence | Sequenced queue (Stage 2 vocab → V2.4 → V2 regen → Stage 3) |

### Ship trigger

Single regenerated season demonstrates: updated gauntlet (B6 kits + B10 V2 sequential rooms) + new geometry palette (B11 + 11 GREEN-list element VFX) + **end-game-anchored movement-speed baseline** (player 8.0 / fast-monster 7.5 / multiplier 0.719 per `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"; sim + demo agree via engine-emitted JSON) + first Pimen integration + chierit character rendering — all without override compensation.

### Design watch-items (gandalf)

- **Telegraph-art convention** still implicit. When B13 lands (post-VS2a) we need an explicit decision: primitive-rendered (circle/cone/line) vs vendor-sourced. **Recommend primitive-rendered** with locked color/opacity in HD-2D-pixel register. PoE precedent.
- **VFX scene composition** — `gandalf-drax-vfx-scene-needs-spec.md` filed; drax consumes when first Pimen integration matures past proof-of-concept.
- **chierit per-archetype mapping** — chierit ships 10 element-mapped characters; Reincarnated has ~14 class archetypes. Need decision: element-only mapping (Fire Knight covers fire_warrior + fire_mage) vs per-archetype with placeholders.

---

## 🎯 VS2b — Substrate Realignment + Full Catalogue Integration (parallel to VS2a)

**Strategic frame.** Structural realignment closing the form-bias gap: the engine stops pretending its substrate is the player's vocabulary. ARPG mechanics stay; isekai narrative skin lands; LLM no longer sees canonical-four.

**🔴 Matt-locked constraint (2026-05-16):** *"All Substrate Realignment S1–S3 + embodiment-axis + Pimen full integration projects move as quickly as possible and in parallel so that as soon as demo VS2a ships, VS2b is right behind it, waiting as a ticket."* VS2b ships within 2-4 weeks of VS2a.

**Estimated working effort:** ~3-6 months, mostly parallel with VS2a.

### Scope — what gates VS2b ship

| Item | Owner | Status |
|---|---|---|
| **S1 — embodiment-axis additive field** on Loadout schema | rocket | ✅ Shipped today (rocket/v1.3-form-bias-stage-1-embodiment-axis) |
| **S2 — abstract pair-structure (grouping layer)** alongside canonical-four | rocket | ✅ Shipped today (form-bias Stage 2) |
| Grouping-layer vocabulary v1.1 lock (gandalf spec) | gandalf | ✅ Locked + decisions-log entry committed |
| Form-bias Stage 1+2 fields wired into `_class_to_dict` serializer | star-lord | ✅ Shipped today |
| **Cipher-migration paths-audit** (48 sites; 26 LEAK-RISK; 18 newly-surfaced) | star-lord | ✅ Complete + R11(d) recorder fail-loud shipped |
| **Stage 2 cosmological-vocabulary** (per-season vocabulary generator) | star-lord | In-flight (HOLD-on-prior gates Stage 3) |
| **S3 — cipher migration (engine side)** — LLM hides canonical-four; export packet additive fields; manifest parallel structure | star-lord | Dispatch authored; sequenced behind Stage 2 vocab + V2.4 telemetry + V2 regen |
| **S3 — cipher migration (drax side)** — gear display + fallback resolver hardening | drax (dispatch not yet authored) | 6 loadout app sites identified; sequenced behind star-lord Stage 3 |
| **Embodiment-narrative display surface** (loadout first, demo second) | drax (dispatch not yet authored) | 🟡 **OPEN DESIGN NEED** — see watch-items below |
| **Character-track ingest pipeline** (chierit Elementals) | drax | Dispatch authored today; closes P6.d |
| **Full Pimen catalogue integration** | drax + elrond | Curation pipeline in flight |

### Parallel-execution risks

| Risk | Severity | Mitigation |
|---|---|---|
| **Drax bandwidth saturation** | 🔴 | Defer non-gating loadout polish; split drax workload across loadout (lower-stakes) + demo (higher-stakes) |
| **Catalogue experiment timing** for S3 cipher-width | 🟡 | If experiment slips, VS2b ships S1+S2+display+Pimen without S3; S3 lands as VS2c |
| Regen budget (two regens in window) | 🟡 | VS2a regens season_001003; VS2b regens season_001005; preserves comparability |
| Decisions-log gate on canonical-four supersession | 🟡 | Knight-rider drafts supersession when Q4 amendment lands |
| Playtest cohesion (two parallel ships) | 🟢 | Combined VS2a+VS2b playtest cycle — same player walks through both regen seasons |

### Design watch-items (gandalf)

- **Embodiment-narrative display first surface.** I want a tight first surface that does ONE thing well (per-class portrait + 2-line narrative beat tied to `embodiment_tag`) rather than a sprawling display that does many things weakly. Diablo class-select screen is the right reference: portrait + voice line + one paragraph.
- **S3 LLM hide-the-cipher** is the highest-payoff structural moment of VS2b. Defend hard against any "ship S1/S2 + display without S3" compromise unless catalogue experiment slips badly.
- **Character roster gap** — see VS2a chierit per-archetype mapping decision; same call serves both VS2a + VS2b display surfaces.

### Ship trigger

Fresh regenerated season demonstrates: cipher migration (LLM no longer sees canonical-four labels; per-season vocabulary fully drives surface) + embodiment-axis populated + embodiment-narrative display in loadout + Pimen full integration. Ships as soon as VS2a is validated AND VS2b's parallel work is complete.

---

## 📋 What comes after VS2a + VS2b

**Stage A2 closeout** — items deferred from VS2a return to Stage A2 sprint: B7 (gear-percentile variance gate), B12 full audit (boots/gloves/belt + +% MS affixes + hard-cap), B13 (active mobility + telegraphs + i-frames — **reduced scope** post-narrow-slice; see below), B14 (multi-band convergence sim), B16 (loot drop architecture). ~6-10 weeks after VS2a/VS2b close.

**🟢 B13 scope reduction (2026-05-17 L3 narrow-slice decision).** Per gandalf L3 briefing `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 (binding per Matt standing delegation), a *narrow slice* of B13 was folded into Phase-1 P1 as Deliverable 28 (universal dodge mechanic + enemy-AOE telegraph indicators + elite-tier reactive escape AI + cross-doc updates). This covers **~25% of original B13 scope.** Remaining B13 estimate: **~2.5-3 weeks at Stage A2 closeout** (down from 3-4 weeks per `16a-roadmap-shipped-log.md` line 86). Remaining B13-proper scope: 5 defensive mobility geometries as kit-pool additions (`roll` / `defensive_dash` / `strafe_mode` / `blink` / `dodge_stance`); mini-boss + boss strategic/anticipatory/substrate-coherent escape AI; archetype-emergence observability; mobility role-tagging in generator; full B13 trait-pool extension surface. See `canonical/32-progression-design.md` § 12.5 Amendment 2026-05-17 for narrow-slice locks + B13-proper open items.

**Stage A2 forward-audit (gandalf) watch-items** — per `canonical/story/p6-forward-audit-2026-05-16.md`:
- B6 skill-tree UI surface decomposition (CRITICAL — same as VS2a gap above)
- B12 full audit visual/UX axes (boots/gloves/belt UI; +% MS VFX; cap UX)
- B13 telegraph-art convention decision
- B16 loot visual presentation layer (drop animation; loot beams; rarity colors; tooltips; auto-pickup feedback) — **Drift-12 candidate**

**🎮 Playtest Cycle 1** — post-Stage-A2 closeout (~1-2 weeks). Skill tree UI comprehensibility, gauntlet density feel, mobility geometries, telegraphs, mobile-first auto-pickup, loot drop density.

**Stage A3** — B9 series (traits + skill points + reset + Spirit Guide build coach). ~4-6 weeks. Design fully resolved 2026-05-12 in file 32.

**🎮 Playtest Cycle 2** — post-A3 (~1-2 weeks). Trait acquisition pacing, skill point allocation, body-swap UX, doppelganger feel.

**Stage A4** — B5 (legendary gear abilities) + B15 (Seasonal Sets). ~2-4 weeks engine + 1 week demo.

**🎮 Playtest Cycle 3** — post-A4 (~1 week). Set collection chase, legendary novelty, form library trophy feel.

**Stage A5** — Small balance items B1, B2 (~2-3 hrs combined, opportunistic).

**Stage A6** — Category C deep-cuts (multi-target dispatch / knockback consumer / convergence reshape). **DEFERRED** unless playtest demands.

**Stage A7** — Progression system implementation (XP, leveling, stats, body-swap pool, doppelganger encounters, end-game quest, ilvl, form library ascension). ~5-7 weeks. Design fully resolved 2026-05-12 in file 32 + 33.

**🎮 Playtest Cycle 4** — post-A7 (~2 weeks). Full progression arc; multi-band class feel; body-swap meta-weight; mobile-first cohesion. Phase 0 ship-readiness assessment.

**🟡 Stage A7 scope-overlap with Substrate Realignment** — open question: does Stage A7 absorb embodiment-narrative integration, or does Substrate Realignment workstream own that into Stage A7's deliverables? **Gandalf recommendation: (c) — workstream owns it; cleanest seam ownership.** Matt decides when Stage A7 sequencing activates.

**For full per-stage scope detail, see `16a-roadmap-shipped-log.md` § "Stage detail (forward reference)".**

---

## 🧭 Substrate Realignment workstream — orthogonal to tracks A/B/C/D

**Why a workstream and not a track.** Tracks are strategic-architecture cuts (engine 1 / engine 2 / build / ship). Substrate Realignment is *engine implementation*, but a parallel slice with its own cadence driver (form-bias work, not the file-28 queue). It modifies the engine substrate (Track A), affects generation (Track A output), is consumed by demo + loadout (Track A consumers), and would inherit into Engine 2 (Track C).

**Why it exists.** Doc 37 named the project's structural bias toward humanoid form — implementation-vs-intent drift (Discipline #13a). The project name *Reincarnated*, the Spirit Guide module, and the originating isekai premise all carried non-humanoid intent that drifted humanoid via implementation defaults. **Structural realignment to realize latent design intent, not a pivot.**

**Stage status (as of 2026-05-16 Day 4 close):**

| Stage | What it adds | Status |
|---|---|---|
| **S1** Embodiment-axis additive field | ✅ Shipped (rocket Stage 1) |
| **S2** Grouping-layer (abstract pair-structure) | ✅ Shipped (rocket Stage 2) |
| **S3** Hide canonical-four from LLM (cipher migration) | Dispatched; HOLD-on-prior (star-lord queue) |
| **S4+** Embodiment-as-narrative-skin display; multi-seam consumer cleanup | Pending; couples to VS2b display + Stage A7 |

**Decisions-log locks (2026-05-16):** strategic-axis explicit-hybrid; three-layer model (substrate / grouping / vocabulary); cipher-width Outcome 2 + Foundation L2 + per-season vocabulary coupling β; cadence Option II (four-stage backbone); four sub-locks deferred to catalogue-track empirical gates; Disciplines #13a/#13b/#14 codified.

**Canonical references:**
- `canonical/37-form-bias-diagnosis-and-recovery.md` — origin diagnosis
- `canonical/story/form-bias-cadence-strategy.md` — strategic-axis lock + decision framework
- `canonical/story/pre-llm-substrate-inventory.md` — 53-item catalogue in 5 clusters
- `canonical/story/embodiment-narrative-layer.md` — embodiment as narrative skin
- `canonical/story/engine-generic-meta-structure.md` — three-layer model (L1 / L2 / L3)
- `canonical/story/p6-forward-audit-2026-05-16.md` — implicit-axis sweep for upcoming milestones

---

## 🔁 Track A landing rhythm

Each stage cycles through: decisions land → engine work lands → **single-season** regen → demo override cleanup → smoke test → tag (partial-then-promote).

**Single-season-per-playtest rule (LOCKED 2026-05-12).** Regenerate AT MOST ONE LLM-generated season per playtest cycle. Cost math: ~$8/season post-Stage-A2; 1 season × 4 cycles ≈ $32 vs 5 seasons × 4 cycles ≈ $160. A single regen exercises all new engine changes; other 4 seasons remain at prior baseline for comparison. **Exceptions** require explicit budget call (cross-season meta-progression validation; pre-ship Phase 0 closure sweep).

**Refactor vs rewrite (LOCKED 2026-05-12).** Track A is a REFACTOR of the existing engine, NOT a rewrite. Core insights (convergence pattern, dimensional generation, fit_for_class scoring, LLM call pipeline, telemetry) are foundational and proven. Most B-items are ADDITIVE. B14 is the riskiest piece but operates on existing primitives. 5 production seasons + demo1 v1.2 prove the architecture; throwing it away discards validated knowledge. **Risk mitigation:** `v1.2-pre-stage-a2` tag as restore point; `scripts/capture-regression-baseline.py` snapshots before Stage A2 begins; per-stage tagged releases enable incremental rollback.

---

## 🛣️ Tracks B / C / D (downstream)

**Track B prototypes** (intermittent; spin up when an open Engine 2 decision needs empirical input or quiet Track A stretch creates capacity):
- Town/hub prototype — blocked on hub-form decision (Diablo town vs Hades run-hub)
- Quest chain prototype
- Dungeon generation prototype — blocked on validation method (CV-based vs feature-tagged)
- Body-swap interaction prototype — blocked on spirit-swap mechanics
- Multi-NPC dialogue prototype

**Demo strategy (LOCKED 2026-05-12):** demo1 (Pixi.js) incrementally refactored per Track A stage — NOT rebuild from scratch, NOT defer-to-Unity. Unity migration deferred to production-polish phase. Each Track A stage adds UI/UX to demo1; 4 interleaved playtest cycles validate subjective qualities.

**Track C — Engine 2 build.** Cannot start before: hub form decided, dungeon validation method decided, final act count locked (3 acts already locked 2026-05-11).

**Track D — Integration + ship.** Reincarnated v1.0. Far-future.

---

## ❓ Open design decisions (forward-looking only)

For full lock history, see `16a-roadmap-shipped-log.md` § "Closed/locked decisions reference."

### 🔴 High-impact, blocks Substrate Realignment closeout

- **Cipher width** (Options A/B/C). **PARTIALLY RESOLVED 2026-05-16** via Outcome 2 lock (single classical-element-anchored grouping); residual experiment-pending nuance lives at form-bias-cadence-strategy doc Q4. Catalogue-mapping experiment dispatched 2026-05-16.
- **Foundation layer placement** (L1 substrate vs L2 cosmology). **RESOLVED 2026-05-16** — Foundation L2-decoupled. Implementation: rocket dispatch when capacity permits.

### 🔴 High-impact, blocks VS2a ship

- **B6 skill-tree UI surface decomposition** — drax dispatch needed before B6 engine work ships. Rendering shape (vertical / horizontal / radial), node icon strategy, unlock-feedback affordance.
- **chierit per-archetype mapping decision** — element-only or per-archetype with fallbacks.

### 🔴 High-impact, blocks VS2b display

- **Embodiment-narrative display first surface** — gandalf recommendation: per-class portrait + 2-line narrative beat tied to `embodiment_tag`, loadout-first.

### 🔴 High-impact, blocks Engine 2 (Track C) commitment

- **Hub form:** Diablo-style town vs Hades-style run-hub. Prototype both via Track B before committing.
- **Dungeon validation method:** CV-based vs feature-tagged. Highest-risk item; prototype both early in Track B.

### 🟡 Medium-impact, designable at any time

- **D1 rubric humanoid-fantasy screening** (Flag A) — empirical test needed before D1 pool reconsideration. Per Outcome 2 lock, scope conditional on Flag A AMBIGUOUS verdict; Q1+Q4 surgical amendments completed today.
- **Pimen acquisition decisions** — three-track viability gate PASSED; full crawl complete; Matt-level call on which packs to acquire and when. 21-row visual-inspection queue deferred.
- **Per-season vocabulary coupling (α/β/γ)** — **β chosen 2026-05-16** as default; α/γ residuals at catalogue experiment.
- **Spirit-swap mechanics layer** — duration / friction / earth-self vulnerability / cross-season persistence / rift availability. Game-implementation layer needs this; doesn't block Tracks A or B.
- **Cross-season meta-progression depth** — smuggling capacity, meta-currency, accumulated-knowledge effects.
- **Geospatial mechanics roadmap** — B11 + B13 add motion-AOE + active-mobility; summoner geometry eventually needs richer positional model.

### 🟢 Low-impact, resolve when convenient

- Item type breadth (gems / runes / consumables)
- Body-swap visual transition design (game-feel, not blocking)
- Aura stacking rules (B5)
- Validity matrix expansion (element × non-mana cross-combinations)
- Audio scope **(closed 2026-05-16)** — Phase 1+ per `canonical/story/audio-strategy-phase0.md`

---

## 🛠️ Polish / small work (opportunistic, between stages)

| Item | Effort |
|---|---|
| `base_mana` / `base_stamina` telemetry write gap | 3-line fix; do when adjacent code is touched |
| `seasonal_element_name` column NULL despite substitutions table populated | Investigate by-design vs write-gap |
| Element-system PR #1 cleanup (stale May 7 branch) | 2 min |
| Phase 1 stranded TrialBoss commit cleanup | 2 min |

---

## 🏔️ Far-future (months / years out)

- **VFX pipeline progression** — Pixi.js (demo1) → Unity port for production polish + better mobile deployment
- **Trial dungeon structure** — playable trial room rendering, not just generation
- **Form-library / spirit-swap UX** — player-facing body-swap layer; gated on mechanics decisions above
- **Game lifecycle progression** — acts, seasons, story
- **Audio pipeline production** — Phase 1+; AI-music-generator workflow (Matt's) is Phase-0 strategy
- **Multiplayer / co-op** — out of scope for Phase 0 seasonal play indefinitely; envisioned for Earth meta-layer rift events post-Phase 0
- **Static seasonal themes / variety polish** — addressable once Engine 2 produces themed maps + lore arcs
- **Open-source release of engines** — if they prove robust, post-ship consideration

---

## 🎯 Rough timeline

Side-project pace with father-son cadence. **All estimates are working time, not calendar time.**

| Phase | Working effort |
|---|---|
| VS2a (in-flight) | ~3-4 months from kickoff (~mid-May 2026) |
| VS2b (in-flight, parallel) | ~3-6 months, mostly overlapping VS2a |
| Stage A2 closeout (B7, B12 full, B13, B14, B16) | ~6-10 weeks after VS2a/VS2b |
| Playtest Cycle 1 | ~1-2 weeks |
| Stage A3 (B9 series) | ~4-6 weeks |
| Playtest Cycle 2 | ~1-2 weeks |
| Stage A4 (B5 + B15) | ~3-5 weeks |
| Playtest Cycle 3 | ~1 week |
| Stage A5 (B1, B2) | ~2-3 hrs, opportunistic |
| Stage A7 (progression implementation) | ~5-7 weeks |
| Playtest Cycle 4 | ~2 weeks |
| Track B prototyping | Intermittent |
| Track C build | Months |
| Track D ship | Months |

**Cumulative Track A working effort** from today: ~9-15 months to Phase 0 ship-readiness.

---

## 🔗 Doc cross-references

**Strategic anchors + engine queue:**
- `29-design-overview.md` — strategic anchor (scope, two-engine architecture, four-track model)
- `28-engine-arpg-rebalance-design.md` — the engine queue this roadmap operationalizes
- `30-engine-explainer-current.md` / `31-engine-explainer-future.md` — engine state baselines
- `32-progression-design.md` / `33-progression-skeleton.md` — Stage A7 spec
- `09-geometry-palette-discussion.md` — palette decisions
- `17-gear-and-spirit-guide-design.md` — gear + Spirit Guide
- `19-llm-call-map.md` — LLM call topology
- `34-monster-design-phase0-vs-production.md` — monster design distinction

**Substrate Realignment workstream:**
- `37-form-bias-diagnosis-and-recovery.md` — origin diagnosis
- `37-engine-and-game-two-products.md` — two-products framing

**Canonical story (gandalf) — L2 project cosmology + design framework:**
- `canonical/story/cosmology-reincarnated.md`, `court-of-forms.md`, `naming-triad.md`, `style-register.md`, `enemy-visual-legibility.md`, `embodiment-narrative-layer.md`, `engine-generic-meta-structure.md`, `spirit-guide-voice.md`
- `canonical/story/trial-moment-ritual.md`, `passage-moment-ritual.md`, `ascension-moment-ritual.md`
- `canonical/story/season-feel-rubric.md`, `drift-audit.md`, `engine-balance-stewardship.md`
- `canonical/story/pre-llm-substrate-inventory.md`, `form-bias-cadence-strategy.md`
- `canonical/story/p6-forward-audit-2026-05-16.md` — forward-audit pattern P6
- `canonical/story/movement-speed-baseline.md`, `arena-room-hallway-system.md`, `spatial-data-jsonschema.md`, `audio-strategy-phase0.md`

**Orchestration:**
- `agentic_orchestration/AGENTS.md` — 9-entity team topology + authority tiers + viability gate
- `agentic_orchestration/GOVERNANCE.md` — founding ADRs
- `agentic_orchestration/REVIEW_PROCESS.md` — Gate-1 / Gate-2 + 5 principles
- `agentic_orchestration/CHANGELOG.md` — team-level event log

**Historical / shipped:**
- `16a-roadmap-shipped-log.md` — what's shipped, sub-progress, closed decisions
- `16b-roadmap-archive-restructures.md` — meta-history of roadmap restructures

---

## 📝 How to update this doc

This is the **forward-looking** roadmap. Update when:

- A milestone (VS2a / VS2b / Stage AN) closes → move sub-items to `16a-roadmap-shipped-log.md`; update status snapshot
- A new milestone enters scope → add forward section here
- An open decision closes → strike from "Open design decisions"; append to `16a` § "Closed/locked decisions reference"
- Estimates shift materially → update timeline

**Don't rewrite history here.** Closed decisions and shipped sub-items live in `16a`. Restructure events live in `16b`. This doc stays terse and forward-looking.

**Update the "Last updated" date** at the top whenever this doc is touched substantively.
