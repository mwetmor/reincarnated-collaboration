# DISPATCH — W-α4-gandalf — Bounded-Viability-with-Specialization Canonical Write

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gandalf (design seam; canonical-story author; Tier-A; bounded-viability-with-specialization design-directive author)
**Pattern:** Pattern B canonical authoring (~1-2d)
**Status:** PENDING — fires on receipt (Gate-1 absorbed at master scoping level)
**Authority:** Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL — Path α RATIFIED; bounded-viability-with-specialization design directive LOCKED

---

## 0. CONTEXT REFRAME — RE-ENGAGEMENT POST PATH β-NARROW REJECTION

**You had prior Path β-narrow recommendation (in Matt-dialogue; precise context at `agentic_orchestration/gandalf/matt_conversations/` or in Matt's verbal dialogue).** Matt REJECTED Path β-narrow with explicit reasoning: shipping a "playable demo" preserving 365× cross-path imbalance VIOLATES the bounded-viability-with-specialization design directive.

**You are NOT in trouble.** Your Path β-narrow recommendation served a valid trade-off framing (Cycle 14 v1 close timeline vs architectural honesty). Matt's directive made design intent explicit — bounded-viability-with-specialization is the CANONICAL design principle, which had been implicit-but-not-explicitly-named. **Your W-α4 role: canonicalize this design directive + 5 operationalized design targets as the LOAD-BEARING input for all downstream Path α work.**

Path α now RATIFIED. Cycle 14 v1 close trajectory: ~4-6 weeks. **Quality > timeline (Q10) directly drives.** "Ship-the-novel-engine-with-the-fun/balanced-game" directly requires architectural honesty.

---

## 1. SCOPE — what gandalf authors

### 1.1 New canonical doc

**Path:** `canonical/<NN>-bounded-viability-with-specialization-design-directive-2026-05-28.md` (next available NN; check `canonical/00-ground-state.md` first-reads + recent commits for next doc number; suggested working number = 50 if 49 is the last numbered doc).

**Status:** CURRENT (LOAD-BEARING) — Path α architectural commit.

**Required sections:**

**§ 1 — Authority + provenance:**
- Matt 2026-05-28 design directive verbatim:
  > *"some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses."*
- Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL provenance — Path α RATIFIED; Path β-NARROW + Path β-FULL Option 6 REJECTED.
- Cross-reference to hive-mind state file § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28".

**§ 2 — Design principle name + framing:**
- **bounded-viability-with-specialization** as named design principle
- Three constitutive properties: (1) bounded viability (minimum floor); (2) specialization (designed peaks); (3) no strict dominance (no kit dominates all encounter types; no kit is strictly dominated)
- Genre positioning: ARPG specialization tradition (Diablo II builds; PoE archetypes; Last Epoch masteries) — every build has strengths AND weaknesses; no objectively-best build per encounter type
- Cross-reference to existing canonical docs: doc 47 § 3 (4 damage-scaling paths as mechanical partition); other relevant precedent docs you judge relevant

**§ 3 — Empirical evidence of design-violation in current engine state (Cycle 14 pre-Path-α):**
- Per-encounter-type aggregation findings (Matt 2026-05-28 forensic):
  - INT/WIS saturate 600 KPM ceiling on 4 of 6 encounter types (no measurable weaknesses)
  - STR/DEX produce 0.0 KPM on boss + mini_boss + ~1.5 KPM on elite_pack (catastrophic weakness; no strengths)
  - Cross-path ratio at elite_pack: 365× (worse than 79× population-median framing)
- Source telemetry: `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` + `boss-hp-rebase-empirical-dps-telemetry.json` + per-encounter-type aggregation (gamora to surface during W-α4-gamora harness implementation)
- Diagnosis: current engine produces INVERSE of design directive — strictly-dominant + strictly-dominated paths

**§ 4 — Operationalized design targets (5 criteria):**

For each target: name + numeric criterion + validation method + rationale.

1. **Base DPS variance ≤1.5× across 4 damage paths** — population-DPS sweep at L50 vs unified calibration target; ensures bounded viability floor.
2. **Every kit produces non-zero KPM on every encounter type** — per-kit-per-encounter-type gauntlet sweep; 18 kits × 6 encounter types = 108 cells; zero_count = 0; ensures no kit has zero strengths on any encounter type.
3. **No kit saturates ceiling on any encounter type** — KPM ceiling raised/removed per W-α2; saturation_count = 0; ensures no kit has zero weaknesses on any encounter type.
4. **Specialization variance: each kit ~1.5-2× cohort median on 1-2 encounter types** — per-kit specialization profile; designed peaks within bounded range; emergent imbalance ruled out.
5. **No kit performs <30% of cohort median on any encounter type** — per-kit-per-encounter floor; bounded-viability floor at 30% cohort median.

For each target, document the design rationale — why this specific threshold; what player-experience property it preserves.

**§ 5 — Per-encounter-type validation framing:**
- 6 encounter types canonical list (gandalf to enumerate from current engine canonical OR cross-reference to wherever encounter-type taxonomy lives; standard set likely: swarm / magic / elite_pack / mini_boss / boss / endgame_capstone)
- Validation harness specification at conceptual level (W-α4-gamora implements the harness against this spec)
- Per-kit profile output shape: 18 kits × 6 encounter types = 108-cell matrix; aggregated cohort medians + specialization profiles + saturation counts + floor violations

**§ 6 — Path β rejection rationale (for canonical record):**

**Path β-narrow rejected:**
- Description: "playable demo" preserving 365× cross-path imbalance
- Rejection reason: violates bounded-viability-with-specialization directive; ships a game where INT/WIS strictly dominate, defeating the specialization design intent
- Recognition: Path β-narrow served a valid Cycle 14 v1 close timeline framing; Path α represents architectural-honesty path that Q10 quality > timeline directly drives

**Path β-FULL Option 6 (damage/HP% metric replacement) rejected:**
- Description: replace KPM with damage_fraction_per_fight metric while preserving underlying damage formula imbalance
- Rejection reason: would replace gate metric while leaving underlying damage formula divergence intact; future systems (gear, T4, progression, balance) would all inherit the divergence
- Cross-reference: Cycle 15 D2 ratification (was: Matt-RATIFIED at Gate-5; retroactively retracted per Path α RATIFICATION REVERSAL; jack-ryan W-α5a Discipline #40 case (c) FOURTH iteration handles)

**§ 7 — Cycle 14 v1 architectural commit:**
- v1 tag revised: `v1-cycle-14-bounded-viability-substrate-led` (was: `v1-cycle-14-no-classes-substrate-led`)
- Architectural commit shape: damage formula refactor + KPM ceiling raise + unified calibration + per-encounter-type design-target validation framework
- Re-evaluation hook at 6-week boundary preserves optionality (Path β-narrow as Cycle 14 v1 partial close + Path α as Cycle 15 architectural close if scaffold-drift case #9+ extends further)

**§ 8 — Forward-link to Path α work-streams:**
- W-α1 rocket damage formula refactor
- W-α2 gamora KPM ceiling raise/remove
- W-α3 gamora unified calibration pass
- W-α4-gamora validation harness (sibling of this doc; sequential after W-α4-gandalf canonical lock)
- W-α5 jack-ryan canonical retirements (Path β rejection, Cycle 15 D2 retraction, Phase 7 doc lifecycle, Discipline candidate)
- Master scoping dispatch: `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md`

### 1.2 Cross-references to update

- `canonical/00-ground-state.md` — add this doc to first-reads + currents; Path α RATIFIED workstream registered
- `canonical/02-roadmap.md` — Cycle 14 v1 close trajectory updated to ~4-6 weeks; Path α active workstream; Cycle 15 Option 6 retroactively retracted
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 — cross-reference forward to bounded-viability-with-specialization (existing 4-damage-path mechanical partition is mechanical substrate; new design directive is architectural-experience layer)
- Discipline #45 vocabulary lock: confirm "bounded-viability-with-specialization" is new design-vocabulary; "specialization" + "bounded" each appear in prior canonical docs without conflict per jack-ryan Gate-1 ruling

### 1.3 Acceptance

- Canonical doc landed at `canonical/<NN>-...`
- Cross-references updated at ground-state + roadmap + doc 47
- Discipline #45 vocabulary grep audit confirms no conflict
- W-α4-gamora harness dispatch can author against locked canonical (signal: this doc commits + pushes; W-α4-gamora fires next)
- Tag: `gandalf/v1.X-w-alpha-4-bounded-viability-canonical-1` (gandalf seam-discretion on tag number)

**Auto-commit + auto-push per CLAUDE.md addendum + Cycle 14 per-workstream push pattern.**

---

## 2. REQUIRED READING

Authority + reframing:
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28" + § "CYCLE 14 RE-SCOPING"
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` (full master scoping; load-bearing context)
- Your own prior Path β-narrow recommendation at `agentic_orchestration/gandalf/matt_conversations/` (locate + reference for rejection-rationale § 6 authoring)

Empirical evidence:
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/boss-hp-rebase-empirical-dps-telemetry.json`
- Phase 7 doc current state for cross-reference (will retire to HISTORICAL post Path α): `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md`

Canonical context:
- `canonical/00-ground-state.md` (first-reads + currents to update)
- `canonical/02-roadmap.md` (workstream tracking)
- `canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (4 damage-scaling paths mechanical partition)
- `canonical/` numbered docs for next available doc number + style register

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #45 vocabulary lock (canonical doc author seam discipline)
- Discipline #46 (DB anti-materialization) already exists per jack-ryan Gate-1 INFO note; gandalf does not commit a new discipline number

---

## 3. OUT OF SCOPE — explicit

- **Do not author validation harness code.** W-α4-gamora's responsibility; sequential after your canonical write lock.
- **Do not author Path α work-stream dispatches (W-α1/W-α2/W-α3/W-α5).** KR authors per-stream dispatches post your canonical lock.
- **Do not retract Phase 7 doc.** Jack-ryan W-α5b handles lifecycle transition (LOAD-BEARING → HISTORICAL).
- **Do not modify Discipline #46 candidate framing in master scoping dispatch.** Already updated by KR post Gate-1 INFO.
- **Do not commit a new engineering-disciplines number.** Jack-ryan W-α5c confirms next available at authoring time.
- **Do not pre-author Cycle 15 commitments.** Cycle 15 scope undetermined post Path α; will be re-scoped at Path α close.

---

## 4. RISKS + COMPLICATIONS

- **Path β-narrow rejection narrative requires care.** Document the rejection without diminishing the trade-off framing that produced the recommendation. "Architectural honesty path" framing per Matt directive is the correct framing — your prior recommendation was valid within a different trade-off priority weighting.
- **Per-encounter-type taxonomy authority:** if 6 encounter types are not canonically named in a single existing doc, gandalf canonicalizes the list as part of § 5. Cross-reference to engine encounter catalog if exists.
- **Cycle 15 scope determination deferred:** Path α RATIFICATION retracts Cycle 15 D2 Option 6 commit; what fills Cycle 15 scope is post-Path-α determination, not gandalf W-α4 scope.

---

## 5. URGENCY

**W-α4-gandalf is the load-bearing first fire.** W-α4-gamora harness + W-α1/W-α2/W-α3 all gate on your canonical lock. ~1-2d expected. Fire ASAP.

Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing.

---

**KR signature:** authored per Matt 2026-05-28 Path α RATIFICATION + bounded-viability-with-specialization design-directive lock + master scoping § 2.1 W-α4 load-bearing-first sequencing. Gandalf re-engagement on architectural-honesty path post Path β-narrow rejection. Q10 quality > timeline + "ship-the-novel-engine-with-the-fun/balanced-game" directly drive.
