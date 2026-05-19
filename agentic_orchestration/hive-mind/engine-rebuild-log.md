# Engine-Rebuild Hive Log

**Created:** 2026-05-19 by knight-rider at hive activation (second hive-mind invocation).
**Status:** **APPEND-ONLY.** No edits to prior entries; corrections appended as new entries.
**Authority:** Operating under `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` (mechanics inherited from `canonical/story/archived/hive-mind-protocol-2026-05-17.md`).
**Mission canonical:** `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` (seven workstreams; hypothesis-test design).
**Diagnosis canonical:** `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`.
**Purpose:** Continuous-broadcast channel for the engine-rebuild hive. Every seam contributes entries continuously. Every entry timestamped + authored.

**Entry types (per protocol § 4.2):** STATE / QUESTION / DECISION / FRICTION / OBSERVATION / TAG / HANDOFF / AMENDMENT / REQUEST.

**Reply latency target:** in-hive entries that require response — 30–60 min during active hours; next-active-window for out-of-hours.

**Operating mode:** **AUTONOMOUS** per engine-rebuild protocol § 4.0. No L3-to-Matt escalation during operation. SME agents decide within seams; gandalf decides cross-cutting design / canonical / architectural; knight-rider decides orchestration / sequencing. Matt re-enters only at wind-down.

**Hive log commit discipline (inherited per protocol § 4.2 amendment 2026-05-18):** before staging this file, `git fetch origin` + inspect `git log --oneline -5 -- agentic_orchestration/hive-mind/engine-rebuild-log.md`; if remote has new entries, `git pull --rebase` first; then stage by explicit path + commit.

---

## 2026-05-19 — Activation

### [2026-05-19 04:26Z] STATE — knight-rider — Engine-rebuild hive ACTIVATED

Hive-mind mode reactivated for the **engine-rebuild session** per `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`. This is the **second hive-mind activation** (first was 2026-05-17 Phase-1 P1 substrate expansion, mission completed + archived). Mechanics inherited from the 2026-05-17 protocol §§ 3–11; mission scope distinct.

**Activation trigger:** Matt directive 2026-05-19 to knight-rider via `agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md` (gandalf-authored under autonomous-operation authority).

**Mission scope (seven workstreams):**

| # | Workstream | Owner | Size | First-fire? |
|---|---|---|---|---|
| **R1** | Per-tier balance targets | gamora | 1–2 wk | ⭐ Fire first |
| **R3** | Per-skill range + AI behavior schema migration | rocket + star-lord + elrond | 2–4 wk | ⭐ Fire first (foundation) |
| **R7** | AI catalogue source of truth | rocket + star-lord | 2–3 wk | ⭐ Fire first (parallel with R3) |
| **R8** | Season-as-emergent-output A/B | rocket + star-lord + gandalf | 1–2 wk | ⭐ Fire first (parallel; independent surface) |
| **R5** | Demo AI parity audit | drax | 1 wk | Queued behind R3 |
| **R2** | 2D spatial sub-gauntlet | gamora + star-lord | 3–5 wk | Queued behind R3 |
| **R4** | Demo collision + leash + range | drax | 2–3 wk | Queued behind R3 |

**Total elapsed:** ~8 weeks parallel (with class-retuning sprint following R1).

**Out of scope (per protocol § 2.2 + § 6):**
- R6 Host-Calibration Protocol (Pattern-B parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`)
- Pattern-B commercial-direction work (Crate response, Last Epoch data, etc. — file in PARKED thread; do NOT pull focus)
- Visual benchmark beyond galadriel's in-flight Track-C deliverable
- Pitch-to-life portrait work (paused)
- Phase-1 P1 re-work (foundation already shipped 2026-05-17 → archived)

**Pre-activation safety verified:**
- ✅ Database backups confirmed (Matt 2026-05-19, per launch dispatch § 2 Step 1)
- ✅ Engine-rebuild solutions canonical committed (`d49c587` — gandalf, 2026-05-19)
- ✅ Engine-rebuild protocol canonical committed (`d49c587`)
- ✅ Pattern-B PARKED thread committed (`d49c587`)
- ✅ Launch dispatch committed (`d49c587`)
- ✅ Pre-rebuild baseline tagged + pushed across all 4 repos (see TAG entry below)

**Engineering disciplines remain operative.** Load-bearing for this rebuild (per protocol § 9):
- Discipline #1 (math-before-code) → R1 per-tier math + R2 spatial combat math
- Discipline #11 (live-state verification) → R7 parity test
- Discipline #13 (implicit-pillar drift) → R3 schema migration coherence across seams
- Pattern P7 (silent-default convergence) → R7 catalogue consumers must iterate, not fall back to defaults

**Companion artifacts authored at activation:**
- `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md` (the seven-workstream executable plan)
- `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md` (seam × workstream; cross-workstream DAG)
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild.md` (activation-day digest)

### [2026-05-19 04:26Z] TAG — knight-rider — `hive-rebuild/v0.0-pre-engine-rebuild` baselines created + pushed

Pre-engine-rebuild rollback baselines tagged + pushed to origin in all four repos under standing launch-authority push (per launch dispatch § 2 Step 1, ADR-006 amendment):

| Repo | SHA | Tag pushed |
|---|---|---|
| reincarnated-collaboration | `d49c587` | ✅ origin |
| reincarnated-engine | `89f83c2` | ✅ origin |
| reincarnated-demo | `59b933031` | ✅ origin |
| reincarnated-loadout | `ec73ea7` | ✅ origin |

Rollback to baseline is now durable across machines. Per protocol § 4.7 (inherited), rollback is a normal operation, not a failure response.

### [2026-05-19 04:26Z] DECISION — knight-rider — First-fire batch: R1 + R3 + R7 + R8 (parallel)

Per launch dispatch § 2 Step 4 and engine-rebuild solutions doc § 9 sequencing:

- **R1 (gamora)** — independent + cheapest; no upstream dependencies; closes Axis 2 (the playtest-explanatory gap). Fires first.
- **R3 (rocket + star-lord + elrond)** — foundation for R2/R4/R5/R7. Fires first; everything else depends on it.
- **R7 (rocket + star-lord)** — shares schema work with R3. Fires in parallel.
- **R8 (rocket + star-lord + gandalf)** — touches generation pipeline (not the simulation gauntlet). Independent surface; fires in parallel.

R2, R4, R5 queue behind R3 (per protocol § 5.5–§ 5.7 activation requirements — they need R3 schema fields available).

Class-retuning sprint follows R1 organically (in-scope per protocol § 2.1; not separately tracked).

### [2026-05-19 04:26Z] HANDOFF — knight-rider → gamora — R1 dispatch READY

Dispatch at `agentic_orchestration/dispatches/2026-05-19-gamora-R1-per-tier-balance-targets.md`.

**Gamora:** read engine-rebuild protocol + engine-rebuild solutions doc § 2 + this hive-log entry; acknowledge in hive log; begin R1.

**Per-tier targets are PRE-CONFIRMED by gandalf** per solutions doc § 10 question 1 (autonomous-operation resolution). No further confirmation needed. The proposed target table stands as authored (swarm 0.72, magic 0.62, elite 0.52, mini-boss 0.45, boss 0.38; boss floor 0.30 per Diablo II precedent).

**Expected outcome path:** baseline measurement → per-tier failure-rate test (Test 1) → class-retuning sprint → post-retune convergence test (Test 2) → playtest validation (Test 3). Hypothesis-test pass thresholds in dispatch.

**Authority for in-flight tuning judgment:** gamora L1 within seam; gandalf consult if per-tier targets need revision under empirical evidence (protocol § 4 design-input route).

### [2026-05-19 04:26Z] HANDOFF — knight-rider → rocket + star-lord + elrond — R3 dispatch READY

Dispatch at `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md`.

**Rocket + star-lord + elrond:** read engine-rebuild protocol + engine-rebuild solutions doc § 4 + this hive-log entry; acknowledge in hive log; begin R3.

**Joint ownership per coordination matrix:**
- **Rocket** owns per-skill range + AI behavior schema fields + catalogue authorship
- **Star-lord** owns export + telemetry surface for the new fields
- **Elrond** owns backfill migration tooling for the 5 shipped seasons

**MIGRATION.md is REQUIRED** per ADR-004 — this is a cross-seam contract change affecting all consumer surfaces (R2, R4, R5, R7). Authored concurrently by producing seam (rocket) per protocol § 4.4 (inherited 2026-05-17 § 6.2).

**Schema design draft:** rocket authors as L1 in-seam authority; routes to gandalf for design-input consult if a substrate identity declaration is touched (protocol § 2.3 scope-creep table; ESCALATE row).

### [2026-05-19 04:26Z] HANDOFF — knight-rider → rocket + star-lord — R7 dispatch READY

Dispatch at `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-R7-ai-catalogue-source-of-truth.md`.

**Rocket + star-lord:** read engine-rebuild protocol + engine-rebuild solutions doc § 7 + this hive-log entry; acknowledge in hive log; begin R7.

**Option A (catalogue as single source of truth) is PRE-CONFIRMED by gandalf** per solutions doc § 10 question 4. Parity-test infrastructure built now alongside the schema work — cheaper than retrofitting.

**Shared schema with R3:** coordinate via MIGRATION.md cadence. Rocket leads schema; star-lord leads parity-test infrastructure. Jack-ryan consult on parity-test discipline (Pattern P7 silent-default watch).

### [2026-05-19 04:26Z] HANDOFF — knight-rider → rocket + star-lord + gandalf — R8 dispatch READY

Dispatch at `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`.

**Rocket + star-lord + gandalf:** read engine-rebuild protocol + engine-rebuild solutions doc § 8 + this hive-log entry; acknowledge in hive log; begin R8.

**Inversion scope PRE-CONFIRMED by gandalf** per solutions doc § 10 question 2: **Option 1 (full inversion as default + opt-in `--theme-input` flag).** Partial inversion rejected (doesn't actually test the hypothesis).

**A/B run scope PRE-CONFIRMED by gandalf** per question 3: **3 inverted + 3 baseline seasons at seed parity.** If signal is ambiguous, extend to 5+5 second-pass.

**Per-seam authorship:**
- **Rocket** owns the generation-pipeline modifications + the CLI flag surface (`--theme-input`, `--no-coalesce`)
- **Star-lord** owns LLM-call orchestration + cost telemetry
- **Gandalf** owns the post-convergence theme-coalescence prompt + cohesion judging protocol + final disposition decision (commit-to-emergent-default OR revert-to-input-driven OR partial)

**Hypothesis tests (per solutions doc § 8):**
- Test 1 cohesion (within 0.5 of baseline)
- Test 2 mechanical variety (≥ baseline)
- Test 3 LLM cost (≥ 75% reduction)
- Test 4 substrate-identity invariance (discovery test)
- Test 5 multi-shot stability (≥ 70% Jaccard)

R8 is a **science experiment**, not a re-architecture commitment. Either pass or fail is valuable.

### [2026-05-19 04:26Z] STATE — knight-rider — R2 + R4 + R5 QUEUED behind R3

Per protocol § 5.5–§ 5.7 activation requirements:

- **R5 (drax)** — gated on R3 shipping at least the AI behavior fields. Knight-rider authors `2026-05-19-drax-R5-demo-ai-parity.md` when R3 partial-completion checkpoint lands (~week 3 estimate).
- **R2 (gamora + star-lord)** — gated on R3 shipping (per-skill range data). Knight-rider authors `2026-05-19-gamora-plus-star-lord-R2-spatial-sub-gauntlet.md` when R3 ships (~week 4 estimate).
- **R4 (drax)** — gated on R3 shipping (per-skill range + aggro/leash fields). Knight-rider authors `2026-05-19-drax-R4-demo-collision-leash-range.md` when R3 ships (~week 4 estimate).

**Drax is NOT idle during the gate.** drax continues in-flight loadout/demo work (per `AGENT_STATE.md` rhythm) until R5/R4 activation; R5 + R4 are additive, not displacing.

### [2026-05-19 04:26Z] OBSERVATION — knight-rider — Pattern-B remains parked

Per protocol § 6 + launch dispatch § 3 (autonomous decision authority): Pattern-B signals (Crate response, Last Epoch Paradox Classes data drop, Director re-engagement, etc.) that arrive during the rebuild are **filed to** `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md` and surfaced informationally in next state-of-hive. **They do NOT pull focus from engine-rebuild scope.** R6 enters dispatch cycle in a future batch when Pattern-B resolves.

### [2026-05-19 04:26Z] STATE — knight-rider — Jack-ryan continuous-observation rhythm requested

Jack-ryan: please establish continuous-observation rhythm for engine-rebuild scope per protocol § 4.5 (inherited 2026-05-17 § 7). Specific watchpoints per protocol § 9:

- **Discipline #1 (math-before-code)** → R1 per-tier math (must precede gamora's implementation); R2 spatial combat math (must precede gamora + star-lord's sub-gauntlet build)
- **Discipline #11 (live-state verification)** → R7 parity test (gold-standard for parity claim)
- **Discipline #13 (implicit-pillar drift)** → R3 schema migration coherence across rocket + star-lord + elrond + downstream consumers
- **Pattern P7 (silent-default convergence)** → R7 catalogue consumers must iterate registry, not fall back to defaults
- **MIGRATION.md authoring** → concurrent with R3 producing-seam work (rocket)

BLOCK authority retained; use sparingly per protocol § 4.5. First response is surfacing concern via OBSERVATION; BLOCK only if seam doesn't engage.

### [2026-05-19 04:26Z] STATE — knight-rider — Galadriel sub-agent restriction in effect

Per protocol § 7 (NEW constraint): galadriel does NOT invoke sub-agents during the engine-rebuild hive session. If galadriel's work requires research-scout or capture-pipeline-adjacent task that exceeds her seam, she surfaces the REQUEST via this hive log; gandalf or knight-rider commissions the sub-agent under their authority.

**Galadriel's Track-C visual-benchmark work continues independently** of the rebuild (it's the probation exit criterion per 2026-05-18 disposition decision).

Knight-rider will author the amendment to galadriel's agent definition (`.claude/agents/galadriel.md`) at the first stable point during the hive — flagged as a follow-on activation task.

---

## 2026-05-19 — jack-ryan activation + Gate 1: R1 math note review

### [2026-05-19] OBSERVATION — jack-ryan — Engine-rebuild scope read; watchpoints established; continuous-observation active

**Severity: INFO**

Scope read complete. All required documents consumed in order:
- `hive-mind-protocol-engine-rebuild-2026-05-19.md` (full — §§ 0-10; § 4.5 jack-ryan continuous-observation operative)
- `engine-rebuild-2026-05-19-gap-solutions-and-tests.md` (full — seven workstreams, hypothesis tests, CLI surface)
- `engine-vs-demo-fight-integrity-gap-2026-05-18.md` (full — five axes; architectural diagnosis)
- `engine-rebuild-log.md` (activation block through gamora R1 STATE entry)
- `scope-of-work-engine-rebuild.md` (full)
- `coordination-matrix-engine-rebuild.md` (full — concurrent-edit hot-spots noted)
- All four first-fire dispatches (R1, R3, R7, R8)
- `engineering-disciplines.md` (full — all 17 disciplines; R11(b); P7; P6.a; Discipline #14)
- `decisions-log.md` (recent decisions; context confirmed)

**Watchpoints document established:** `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md`

**Watchpoint summary (29 watchpoints across 8 categories):**

| Category | WPs | Risk | Key exposure |
|---|---|---|---|
| WP-R1-A: Discipline #1 for R1 math | 2 | HIGH | Math note before balance_loop.py; boss n-shot strategy |
| WP-R1-B: Pattern P7 for R1 | 2 | HIGH | No silent aggregate-mean pass; per-tier failure to telemetry |
| WP-R3-A: Discipline #13a for R3 schema drift | 4 | HIGH | Field naming drift across 4 seams; MIGRATION.md concurrency; validator fail-loud |
| WP-R7-A: Discipline #11 for R7 parity test | 4 | HIGH | Parity-test spec before harness; consumer audit coverage; Test 2 intentional-break |
| WP-R8-A: Methodology for R8 | 4 | MEDIUM | Judging protocol before A/B run; scale anchoring; Discipline #14 for coalescence prompt |
| WP-MIGRATION: MIGRATION.md cadence | 5 | HIGH | R3 generation + export; R7 cross-repo contract; R8 LLM surface |
| WP-XSEAM: Cross-seam contract vigilance | 3 | HIGH | balance_loop concurrent edit; monster JSON three-seam; R7 source before R5 consumer |
| WP-HIVELOG + WP-TAG | 3 | MEDIUM/LOW | Fetch-before-commit discipline; tag namespace; no smoke-only milestone tags |

**Pre-existing concerns surfaced at activation (all INFO or WARN — no BLOCK):**

1. [INFO] Gamora's math note is committed and awaiting Gate 1 review. Scope read confirmed this prior to authoring watchpoints. Gate 1 review follows this entry (see below).
2. [WARN] MIGRATION.md for R3 not yet authored. This is expected (schema design doc not yet committed either) but is the highest-risk MIGRATION gap — four downstream workstreams depend on it. WP-MIGRATION-1 is the operative watchpoint.
3. [WARN] R7 parity-test spec not yet authored. WP-R7-A-1 is operative.
4. [WARN] R8 gandalf methodology docs (theme-coalescence prompt + cohesion-judging protocol) not yet authored. WP-R8-A-1 is operative.
5. [INFO] R3, R7, R8 seams have not yet acknowledged in hive log. This is normal at dispatch time; WP-R3-A-4 watches for extended silence.

**Continuous-observation rhythm established.** Jack-ryan will file OBSERVATION entries in the hive log at each workstream milestone tag + when any watchpoint trigger fires. BLOCK authority retained; first response to any watchpoint trigger is OBSERVATION, not BLOCK.

**Decisions-log entry:** deferred to first workstream ship. Engine-rebuild activation itself is captured in the hive log + protocol + scope-of-work artifacts; a separate decisions-log entry would be redundant until first hypothesis test passes. Re-evaluate at `hive-rebuild/v0.3-r1-hypothesis-test-passed`.

---

### [2026-05-19] OBSERVATION — jack-ryan — Gate 1 review: R1 per-tier math note

**Severity: INFO (all checklist items pass; one observation surfaced)**

**Target:** `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md`
**Developer:** gamora
**Disciplines applied:** Discipline #1 (math-before-code), Pattern P7 (silent-default), R11(b) (cross-seam round-trip)

**Gate 1 review — gamora § 11 checklist:**

- [x] **§ 2.3 floor/ceiling as operative gate:** correct. Floor/ceiling as hard bounds with target as optimizer aim is the right semantics. The asymmetric bands (boss ±0.08/0.07; mini-boss ±0.10) are appropriate given the single-slot variance analysis in § 4. The ceiling as operative constraint (class with boss WR 0.60 fails) is load-bearing — without ceiling enforcement the optimizer could trivialize the tier and the gate would miss it.

- [x] **§ 3.3 all-tiers-evaluate + full failure report:** the decision to evaluate all 5 tiers and report all failures (not early-exit on first) is correct for the class-retuning sprint use case. The sprint needs to know whether a failing class fails only boss or also mini-boss — early-exit would systematically under-report. Evaluate-all is the right choice.

- [x] **§ 4.2 N=60 for single-slot tiers:** the variance analysis is sound. At N=30, the 95% CI half-width of ±0.174 for boss WR spans the entire [0.30, 0.45] band and both sides — making the convergence gate noise-dominated. At N=60, ±0.123 — a class genuinely at WR 0.38 will not false-fail the floor with 95% probability. This is the minimum statistical tractability threshold. The cost rationale (16.7% additional fight volume; ~8s to smoke-test) is acceptable.

- [x] **§ 4.3 rolling median for single-slot tiers — semantic check:** the 3-iteration rolling median is a variance-suppression technique, not a semantic change to what is being measured. The median WR over 3 iterations at the same modifier level approximates "what is this class's true WR at this modifier, given noise" — which is exactly what the convergence signal should measure. It does NOT change what convergence means; it reduces the signal noise. Discipline #12 (semantic-shifting fixes) is not triggered. **One implementation caution:** gamora's math note notes that "when to reset the window on modifier change" is an implementation decision. Jack-ryan flags this as a low-risk but non-trivial implementation detail — the reset behavior must be conservative (reset on modifier change, not on convergence-iteration count). If the window is NOT reset on modifier change, the median will incorporate WR observations at different modifier levels, which IS a semantic issue. The note should be explicit. This is an INFO observation, not a BLOCK — the note acknowledges the detail; gamora should document the reset-on-modifier-change behavior in the implementation comment.

- [x] **§ 5.2 fail-loud requirement:** satisfies Pattern P7 prevention. Three specific requirements are met: (1) WARNING log on per-tier failure naming tier + observed WR + band + reason; (2) no silent re-tune; (3) telemetry capture of `ConvergenceGateResult` at every evaluation. Cite: engineering-disciplines Pattern P7 prevention mechanism (R11(d) complement: "cross-seam recorders/persistors that drop input should emit a counter or log entry on every drop rather than silently continuing").

- [x] **§ 6.2 MIGRATION.md triggering — is this a cross-seam contract change?** YES. `per_tier_win_rates`, `per_tier_pass`, `convergence_gate_passed`, `failing_tiers`, `aggregate_wr_legacy` are new fields on `ClassBalanceResult` crossing the gamora→star-lord boundary. MIGRATION.md is required per ADR-004. The gamora math note correctly identifies this. Additive-nullable column design (all new columns NULL for legacy rows) is the correct additive choice. Round-trip smoke is required per R11(b). Gamora has correctly flagged all three: MIGRATION.md required, star-lord coordination required, round-trip smoke required.

- [x] **§ 6.3 round-trip smoke — R11(b) correctly triggered?** YES. `per_tier_win_rates` is a new cross-seam contract field. Gamora's note explicitly designates a round-trip smoke at § 9 implementation checklist. R11(b) is satisfied in the math note; it must also be satisfied in the completion record.

- [x] **§ 7 genre precedent — boss-0.30 floor grounded?** YES. Three comparators cited with specific tuning rationale (Diablo II Uber Tristram ~30-40% first-attempt, PoE pinnacle bosses ~30-50% at minimum viable spec, Grim Dawn celestials ~1-in-3 minimum viable). The 0.30 floor is the genre-convergent minimum — not conservative, not arbitrary.

**GATE 1 RESULT: PASS.** Gamora may proceed to baseline measurement run and `balance_loop.py` implementation.

**One implementation-time observation (INFO, not blocking):**

The rolling median window reset behavior (§ 4.3) should be explicitly documented in the implementation comment when gamora writes `_evaluate_convergence_gate()`. Specifically: the rolling median window must reset whenever the binary-search modifier changes (not just when the iteration counter resets). If the window bridges across modifier changes, the median will mix WR observations at different modifier levels, which conflates "noise at one modifier level" with "change in WR due to modifier change." This is the implementation detail the math note leaves open — gamora resolves it as L1. WP-R1-A watchpoints updated to note this detail was surfaced.

**WP-R1-A-2 closure note:** N=60 strategy with rolling median documented. Boss-tier n-shot strategy watchpoint satisfied by the math note. WP-R1-A-2 can be closed when implementation matches spec.

**Cite:** Discipline #1 (math-before-code); Discipline #12 (semantic-shifting fixes — explicitly NOT triggered here); Pattern P7 (satisfied); R11(b) (correctly triggered and designated).

---

## End of activation block

Hive is **ACTIVE** as of 2026-05-19 04:26Z. Next entries follow append-only protocol; specialist seams pick up dispatches at session-open and acknowledge here.

Daily state-of-hive cadence: knight-rider authors `state-of-hive-YYYY-MM-DD-engine-rebuild.md` at end of each active day (per protocol § 4.3 inherited).

Wind-down trigger: Matt's explicit declaration. Engine-rebuild completion → continuation onto VS2a → VS2b → Stage A2 per Matt directive 2026-05-19 (launch dispatch § 6.5).

---

## 2026-05-19 — gamora R1 activation

### [2026-05-19] STATE — gamora — R1 dispatch read; math note authored; Discipline #1 satisfied

R1 dispatch at `agentic_orchestration/dispatches/2026-05-19-gamora-R1-per-tier-balance-targets.md` read in full. All required reading consumed:
- Engine-rebuild protocol (§ 4.0 autonomous-operation, § 4.5 jack-ryan continuous-observation, § 5.1 R1 activation requirements)
- Solutions doc § 2 (R1 specification + hypothesis tests) + § 10 Q1 (per-tier targets pre-confirmed)
- Hive log (activation block; knight-rider HANDOFF to gamora)
- `balance_loop.py:1907-1936` (existing `_compute_convergence_winrate` — the call site to be replaced)
- `AGENT_STATE.md` (D11 cycle closed; no prior R1 work in flight)
- Engineering disciplines (Discipline #1, #2, Pattern P7, R11(b))

**Per-tier math note authored.** Path: `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md`

**Key decisions resolved in the math note (gamora L1 authority):**

1. **Tolerance semantics:** floor/ceiling are the operative gate; target is the optimizer's aim. A tier passes iff `floor <= observed_WR <= ceiling`. Asymmetric bands: swarm/magic/elite ±0.07/0.08; mini-boss ±0.10; boss ±0.08/0.07.

2. **Early-exit semantics:** evaluate ALL 5 tiers per convergence call; report ALL failures. No early-exit. Rationale: the class-retuning sprint needs the full per-tier failure profile, not just the first failing tier.

3. **N-shot strategy for single-slot tiers:** N=60 fights for boss and mini-boss (double the default N=30). Reduces 95% CI half-width from ±0.174 to ±0.123 for boss at target WR 0.38. Additionally: 3-iteration rolling median for single-slot tier WR during binary-search to suppress oscillation.

4. **Pattern P7 remediation:** fail-loud on every per-tier miss (WARNING log naming tier, observed WR, expected band, failure reason). Aggregate-mean preserved as a legacy diagnostic field only — no code path may accept convergence based on aggregate mean alone.

5. **Telemetry cross-seam impact:** per-tier WR crosses the gamora→star-lord boundary. New fields on `ClassBalanceResult`: `per_tier_win_rates`, `per_tier_pass`, `convergence_gate_passed`, `failing_tiers`, `aggregate_wr_legacy`. MIGRATION.md required (concurrent with code change). Round-trip smoke required per R11(b).

6. **Genre precedent:** boss-0.30 floor grounded in Diablo II / Path of Exile / Grim Dawn boss-tier design norms (~30% win rate for build-designed-for-content at minimum viable spec).

7. **Baseline measurement plan:** documented as plan; NOT executed. Runs next session (after jack-ryan Gate 1 review of math note). Output path: `reincarnated-engine/output/R1-baseline-measurement-2026-05-19/baseline-per-tier-distribution.json`.

**`balance_loop.py` is NOT modified in this session.** Modification is gated on jack-ryan Gate 1 review of the math note.

**Jack-ryan:** Gate 1 review of `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md` is now open. Review checklist is in § 11 of the math note. Key focus: floor/ceiling operative semantics (§ 2.3), N=60 single-slot variance strategy (§ 4.2), rolling median semantic-shift question (§ 4.3), R11(b) cross-seam round-trip smoke requirement (§ 6.3).

**Tag:** `gamora/v1.4-r1-math-note-1` applied to engine repo (intermediate seam tag; not pushed per ADR-006 default; no milestone yet).

**AGENT_STATE.md updated.** Next session: jack-ryan Gate 1 → baseline measurement run → `balance_loop.py` modification → tag `hive-rebuild/v0.1-r1-baseline-measurement-captured`.
