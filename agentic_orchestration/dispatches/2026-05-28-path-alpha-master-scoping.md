# DISPATCH — Path α Master Scoping (Root-Cause Damage Formula Refactor; Bounded-Viability-with-Specialization)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipients:** rocket (W-α1) + gamora (W-α2 + W-α3) + gandalf (W-α4) + jack-ryan (W-α5 + Gate-1 of this master dispatch)
**Pattern:** Pattern B master scoping (~10-15d realistic; ~4-6 weeks Cycle 14 v1 close including ~2-4 anticipated scaffold-drift cases)
**Status:** PENDING — fires jack-ryan Gate-1 on receipt; per-stream dispatches authored post Gate-1 PASS
**Authority:** Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL — Path α RATIFIED; both β paths REJECTED

---

## 0. AUTHORITY + CONTEXT

**Matt 2026-05-28 verbatim design directive (LOAD-BEARING — captures the design intent that was implicit but never explicitly canonicalized prior):**

> *"some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses."*

**Design principle name: bounded-viability-with-specialization.**

**Matt 2026-05-28 ratification verbatim — Path α RATIFIED; Path β-NARROW REJECTED; Path β-FULL Gate-6 Option 6 REJECTED.** Full ratification record at `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28".

**Empirical evidence anchoring:**

| Encounter type | INT/WIS KPM | STR/DEX KPM | Cross-path ratio |
|---|---|---|---|
| boss | (saturates engine cap 600.0) | **0.0** | ∞ |
| mini_boss | (saturates engine cap 600.0) | **0.0** | ∞ |
| elite_pack | (~365) | **~1.5** | **365×** |
| (Other 3 encounter types) | (saturates cap on 4/6 total) | (variable; trending dominated) | wide |

Source telemetry: `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` + `boss-hp-rebase-empirical-dps-telemetry.json` + (per-encounter-type aggregation Matt cited; specific source telemetry to be verified by gamora during W-α4 harness authoring).

**Cycle 14 current engine state produces INVERSE of bounded-viability-with-specialization design directive.** STR/DEX are strictly-dominated; INT/WIS are strictly-dominant. No specialization spread; no per-encounter trade-offs.

---

## 1. PATH α SCOPE

### 1.1 Three architectural commits

1. **Damage formula refactor (W-α1):** unified or recalibrated damage formulas across 4 damage-scaling paths (STR-physical, DEX-physical, INT-magical, WIS-faith per doc 47 § 3) such that BASE DPS at L50 is comparable within ~1.5× variance.
2. **KPM ceiling raise or remove (W-α2):** the current 600.0 ceiling hides over-tuning at INT/WIS saturation. Empirical surface required.
3. **Unified calibration pass (W-α3):** replaces SC-6b (`base_physical_damage_l50`) + SC-7 (`BASE_SPELL_DAMAGE_L50`) binary-search calibrations with a single reference target tied to encounter HP scaling + boss HP factor range.

### 1.2 Operationalized design targets (5 criteria)

These are the validation criteria. Path α close-criterion = simultaneous satisfaction of all 5:

| # | Target | Validation method |
|---|---|---|
| 1 | Base DPS variance ≤1.5× across 4 damage paths | Population-DPS sweep at L50 vs unified calibration target |
| 2 | Every kit produces non-zero KPM on every encounter type | Per-kit-per-encounter-type gauntlet sim sweep; 18 kits × 6 encounter types = 108 cells; zero count = 0 |
| 3 | No kit saturates ceiling on any encounter type | KPM ceiling raised/removed; saturation_count = 0 |
| 4 | Specialization variance: each kit ~1.5-2× cohort median on 1-2 encounter types | Per-kit specialization profile; each kit has 1-2 encounter types ≥1.5× cohort median + ≤2× cohort median |
| 5 | No kit performs <30% of cohort median on any encounter type | Per-kit-per-encounter floor: kit_KPM / cohort_median_KPM ≥ 0.30 |

W-α4 authors the validation framework + canonical doc encoding these 5 targets.

### 1.3 Anticipated scaffold-drift cases (Matt 2026-05-28 forecast: ~2-4 cases)

Per Matt's forecast, Path α refactor likely surfaces additional architectural truths:
- **T4 capstone scaling** — current T4 skill values may inherit two-path divergence
- **Gear scaling** — gear affixes may be calibrated against pre-refactor damage formulas
- **Monster HP curves** — boss HP factor range was rebased once at case 8 v2.1; monster HP curves L1-L50 may need parallel rebase against new damage formulas
- **Defense formulas** — armor/resistance computations may be calibrated against old DPS targets
- **Resource model interactions** — mana/stamina costs may be tuned against old damage output
- **Attribute scaling** — STR/DEX/INT/WIS scaling tables may need parallel adjustment

Each surfaced case follows Gate-N → Matt cadence per established pattern. Matt re-evaluation hook applies at 6-week boundary.

### 1.4 Out of scope

- Spirit Guide gameplay subsystem — gamora seam ownership but not damage formula territory
- Element / anchor balance beyond damage formulas — rocket seam ownership but not damage formula territory
- Player-surface work (drax demo + loadout) — gated on Path α close; do not fire D13 P1-P9 framework
- Phase 7 2-layer joint-gate band table infrastructure — preserved as historical instrumentation; new design-target validation harness supersedes
- Cycle 15 Option 6 damage/HP% metric — REJECTED per Matt; not deferred-and-pursued
- Wave 5 production season cascade — does not re-fire until Path α close + design targets met

---

## 2. WORK-STREAM DECOMPOSITION + SEQUENCING

### 2.1 W-α4 fires FIRST as load-bearing input

**Owner:** gandalf (design-target canonical write) + gamora (validation harness)
**Sequence:** lands BEFORE W-α1/W-α2/W-α3 fire — design targets must be canonicalized before damage formula refactor or calibration work commits.

**Sub-streams:**
- **W-α4-gandalf (canonical write; ~1-2d):** new canonical doc capturing bounded-viability-with-specialization design directive verbatim + 5 operationalized design targets + per-encounter-type validation framing. Cross-references doc 47 § 3 (4 damage paths) + Matt 2026-05-28 ratification. Path β rejection rationale documented. Discipline #45 vocabulary lock applied. Context: gandalf had prior Path β-narrow recommendation that Matt REJECTED — W-α4-gandalf is gandalf re-engaging on the architectural-honesty path.
- **W-α4-gamora (validation harness; ~1-2d):** simulation-side validation harness implementing all 5 design targets as automated checks; outputs per-kit-per-encounter-type profile + saturation count + specialization profile + floor check. Hooks into existing gauntlet sim + season generation pipeline. Math note (Discipline #1) required.

**Coordination:** gandalf canonical write completes BEFORE gamora harness implementation locks (harness validates against canonical-defined targets).

### 2.2 W-α1 + W-α2 + W-α3 fire PARALLEL post W-α4 design-target lock

**W-α1 — Damage formula refactor:**
- **Owner:** rocket (foundation seam; element/anchor)
- **Scope:** unified or recalibrated damage formulas across 4 damage-scaling paths. Architectural choice (unified vs recalibrated) is rocket's seam discretion; output must satisfy W-α4 design target #1 (≤1.5× base DPS variance).
- **Effort:** ~3-5d (includes math note + smoke testing)
- **Math note required at:** `~/Games/reincarnated-engine/src/reincarnated/generation/math/path-alpha-damage-formula-refactor-2026-05-28.md` (or appropriate location)
- **MIGRATION.md:** cross-seam touch if simulation seam affected; standard ADR-004
- **Tag:** `rocket/v1.8-path-alpha-damage-formula-refactor-1` (subject to rocket's tag-protocol seam discretion)
- **Coordination dependency:** W-α4 design targets locked; W-α2 KPM ceiling raised so empirical signal not artificially capped during validation

**W-α2 — KPM ceiling raise/remove:**
- **Owner:** gamora (simulation seam; gauntlet_sim.py)
- **Scope:** raise or remove 600.0 ceiling per gamora seam discretion. If raised, new value derived empirically from post-refactor population DPS distribution; if removed, gate semantics updated. Discipline #44 framing-refusal applies if surfacing requires Matt re-engagement.
- **Effort:** ~0.5-1d
- **Math note required (Discipline #1)** capturing the choice + rationale + empirical anchor
- **Tag:** `gamora/v2.2-path-alpha-kpm-ceiling-1`

**W-α3 — Unified calibration pass:**
- **Owner:** gamora (simulation seam; calibration loops)
- **Scope:** replace `sc7_calibration_loop.py` SC-7 binary search + SC-6b uncalibrated baseline with single unified calibration pass tied to encounter HP scaling + boss HP factor range. May retire `sc7_calibration_loop.py` per gamora seam discretion or extend with W-α3 mode.
- **Effort:** ~2-3d
- **Math note required** capturing new calibration architecture + reference target derivation
- **MIGRATION.md:** § v1.40 or next available capturing SC-6b + SC-7 retirement / supersession
- **Tag:** `gamora/v2.3-path-alpha-unified-calibration-1`
- **Coordination dependency:** W-α1 damage formula architectural commit lands; W-α3 calibrates against new formulas
- **Reference-target micro-dependency on W-α2 (jack-ryan Gate-1 Amendment 1):** Reference target lock requires W-α2 ceiling signal (W-α3 harness authors in parallel; reference target value does not commit until W-α2 empirical ceiling output lands). Discipline #1 math-before-code: reference target derivation must be grounded in uncapped empirical signal, not artifact-capped data.

**Sequential micro-dependency:** within the parallel post-W-α4 fan-out, W-α1 → W-α3 chains (W-α3 calibrates W-α1 output); W-α2 fires independently in parallel (but W-α3 reference target lock awaits W-α2 ceiling signal per Amendment 1).

### 2.3 W-α5 fires PARALLEL throughout

**Owner:** jack-ryan (canonical-write seam)
**Sub-streams:**
- **W-α5a (canonical retirements; ~0.25d):** decisions-log entries for Path α RATIFICATION + Path β rejection rationale (β-narrow + β-FULL Option 6); **Cycle 15 D2 Option 6 retraction per Discipline #40 case (c) — FOURTH ITERATION** of canonical-lock retraction on Phase 7 doc (per jack-ryan Gate-1 Amendment 2). Prior iterations: 1st `ec7f6c1` § 3.4-3.7 (Option F Phase 1); 2nd `8c7b67b` §§ 3.8-3.10 (Option F Track 1); 3rd `a4fba64` §§ 3.11-3.13 (case 8 canonical scaffold resolution); 4th THIS DISPATCH (Cycle 15 D2 Option 6 forward-link retraction at § 3.13). 6-step procedure compliance required including cross-reference audit obligation. Cite Discipline #40 case (c) explicitly in commit message + procedure record.
- **W-α5b (Phase 7 doc lifecycle; ~0.25d):** Phase 7 canonical doc LOAD-BEARING → HISTORICAL transition; § 3.13 cross-reference back to Path α successor doc (W-α4-gandalf canonical write). Per Amendment 2: this is the §§ 3.11-3.13 closure completion of the 4th iteration retraction loop.
- **W-α5c (engineering-disciplines.md amendments; optional ~0.25d):** Discipline #39 framework maturation: "case-register distinction between scaffold-drift catches and canonical scaffold resolutions" + "documented scaffolds may expose adjacent architectural truths at their resolution gates"; new bounded-viability-with-specialization framework discipline candidate. **NOTE per Gate-1 INFO:** Discipline #46 already exists (DB anti-materialization, landed 2026-05-27); jack-ryan confirms next available discipline number at authoring time before committing number (likely #47).

**Coordination:** jack-ryan parallel to W-α1/W-α2/W-α3 execution; W-α5b can begin only after W-α4-gandalf canonical write lands (cross-reference target exists)

### 2.4 Wave 5 RE-FIRE at Path α close

Post W-α1 + W-α2 + W-α3 + W-α4 + W-α5 all landed, gamora re-runs full production season under new engine state + design-target validation harness. **Acceptance: all 5 W-α4 design targets simultaneously satisfied across all 18 kits × 6 encounter types.**

### 2.5 Cycle 14 v1 tag at Path α close

**Cycle 14 v1 tag = `v1-cycle-14-bounded-viability-substrate-led`** (revised from prior `v1-cycle-14-no-classes-substrate-led` — new framing reflects bounded-viability-with-specialization design directive as Cycle 14 architectural commit).

Matt ratifies v1 tag at Path α close.

---

## 3. CYCLE 14 V1 CLOSE RE-TRAJECTORY

| Phase | Effort | Calendar |
|---|---|---|
| W-α4 canonical + harness lock | ~2-3d sequential (gandalf canonical → gamora harness) | Days 1-3 |
| W-α1 + W-α2 + W-α3 parallel fan-out | ~3-5d (W-α1 longest pole; W-α3 chains) | Days 3-8 |
| Wave 5 re-fire + validation | ~0.5d | Day 8-9 |
| jack-ryan canonical retirements (parallel throughout) | ~0.75d total | Days 3-9 |
| Buffer for ~2-4 scaffold-drift cases | ~2-5d additional | Days 9-14 |
| Matt v1 ratification | < 0.1d | Day 14 |

**Realistic estimate: ~10-15d total (2-3 weeks).** Per Matt's directive: ~4-6 weeks accounting for unforeseen surface area. Matt re-evaluation hook fires at 6-week boundary if scaffold-drift case #9+ extends further.

**Per CLAUDE.md addendum:** Path α RATIFICATION is the cycle-level authorization. Sub-stream work-products auto-commit per work-stream owner's seam discretion. Push pattern: per-workstream pushes after each Wave-stream closes + smoke PASS. No per-commit Matt re-asking.

---

## 4. GATE-1 ACCEPTANCE CRITERIA (jack-ryan DESIGN-MODE)

Jack-ryan reviews this master scoping dispatch per Pattern B + Cycle 14 cadence. Specific concerns to surface or rule out:

- **W-α4 canonical write content adequacy** — does the proposed canonical doc (bounded-viability-with-specialization + 5 design targets + per-encounter-type validation + Path β rejection rationale) capture enough for downstream W-α1/W-α2/W-α3 to commit cleanly?
- **W-α4 → W-α1/W-α2/W-α3 sequential dependency** — does design-target canonical lock truly need to land first, or can rocket damage formula refactor begin with Matt-directive-as-spec while gandalf canonicalizes?
- **W-α1 architectural-choice latitude** — rocket has discretion between "unified" vs "recalibrated" damage formulas. Is that latitude appropriate, or should jack-ryan + gandalf+ rocket triple-Gate-1 the architectural choice before fire?
- **W-α3 reference-target framing** — "tied to encounter HP scaling + boss HP factor range" — adequate? Does W-α3 need to consume W-α2 KPM ceiling output before locking reference target?
- **Anticipated scaffold-drift framing** — 6 candidate areas listed at § 1.3. Should master scoping commit to "any case #9+ fires Gate-7"? Or framework auto-handles via existing Gate-N cadence?
- **Cycle 15 commitments retraction** — Cycle 15 D2 Option 6 was Matt-RATIFIED at Gate-5; Path α RATIFICATION REVERSAL retroactively retracts. W-α5a captures decisions-log retraction. Adequate handling?
- **Path β-narrow re-evaluation hook framing** — at 6-week boundary, Matt re-evaluates extend further vs ship β-narrow as v1 partial close + Path α as Cycle 15. Should this hook have a more specific trigger (e.g., explicit scaffold-drift count > 4)?
- **Discipline #45 vocabulary lock** — "bounded-viability-with-specialization" is new design-vocabulary; ensure no conflict with existing canonical vocabulary; W-α4-gandalf authoring locks it canonically

Return form per Gate-1 cadence: PASS / PASS-WITH-AMENDMENTS / BLOCK. If amendments, list specific in-place edits before per-stream dispatches fire.

---

## 5. RISKS + COMPLICATIONS

- **W-α1 architectural-choice latitude is high.** Unified vs recalibrated is a substantial design decision; gandalf-rocket-jack-ryan coordination may surface as a parallel design call within Path α (Gate-Pα-1?)
- **Anticipated scaffold-drift surface is broad.** 6 candidate areas listed; each may fire Gate-N → Matt cadence. Cycle 14 calendar may expand beyond 4-6 weeks Matt forecast.
- **Wave 5 re-fire smoke may surface 4th-or-5th scaffold-drift case at design-target #5 floor (no kit <30% cohort median).** Per-kit DPS variance may produce floor violations even under unified formulas if specialization-by-design pushes some kits below 30% on weak-encounter types. Validation criterion may need refinement during W-α4 lock.
- **Cycle 15 retroactive retraction is substantive.** Matt D2 Gate-5 was RATIFIED + canonicalized at Phase 7 § 3.13 jack-ryan canonical retraction third iteration. W-α5b retirement of that record requires care.
- **Drax workstreams remain DEFERRED for 4-6 weeks.** Player-surface work (loadout sample data, image pipeline, Court accumulation, Meshy embed) cannot fire until Path α close. Communication to drax via dispatch deferral records.

---

## 6. URGENCY

**Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing.** Each day of pre-fire delay shifts close-trajectory.

Fire ASAP on jack-ryan Gate-1 PASS. Per CLAUDE.md addendum + Matt 2026-05-23 hive-mind decision-routing directive: seam owners decide in-scope work; Matt is LAST-RESORT escalation. Per-stream dispatches authored after Gate-1 PASS; fan-out parallel post W-α4 design-target lock.

---

**KR signature:** authored per Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL + verbatim design directive locking bounded-viability-with-specialization design principle. Path β-narrow + Path β-FULL both REJECTED. Path α architectural-honesty path RATIFIED. Q10 quality > timeline + "ship-the-novel-engine-with-the-fun/balanced-game" directly drive. Re-evaluation hook at 6-week boundary preserves optionality.
