# Dispatch — 2026-07-26 — gamora — G-5 WAVE 0: universal liveness-gate (the honesty gate)

**From:** knight-rider
**To:** gamora (simulation seam, SOLO)
**Approved by:** Matt 2026-07-25 (G-4 ruled in-session; G-5 key-program charter ACCEPTED-with-amendments by gandalf PRIME REVIEW same date, routed to KR for wave dispatch)
**Estimated effort:** S–M (charter size class; no hours invented — cost your own work per charter §6.3 item 4)
**Acceptance:** all five clauses of charter build-queue row 0, verbatim, reproduced in § Acceptance below
**Tag intent:** `gamora/v-g4-liveness-gate-1`
**Push:** COMMIT-NEVER-PUSH (ADR-006 default; no push authorization on this dispatch)

---

## Context

Gamora's own C2 re-measurement (SESSION 73, tag `gamora/v-f8-cc-2`) established that **4,696 of 5,116 = 91.8%** of chill landings arrive on a defender already at `hp ≤ 0`, with `burn` control at 92.5% and the pre-arm frame at 93.1%. Rocket's read of the same fact for hard CC is worse in kind: a lockout budget fitted to raw `landed:` counters would run **~12×** the realized one.

Matt ruled it G-4(2) — verbatim: *"agree on Liveness-gate at application, but we need this for everything else too, right?"* — and that "everything else too" is what makes the gate **universal** rather than a chill patch. The charter states the consequence plainly (§2, Wave 0): *"Wave 0 is not an improvement; it is the precondition for the program's arithmetic being true."*

This wave **fronts the entire G-5 key program**. Per charter §6.2, Wave 0 is the program's single-point prerequisite: L0-CLOSE, KEY-NUM, and the G-3 control-payload calibration all sit behind it. It is dispatched **solo** for one reason, stated in the charter and binding here: *"It changes the meaning of every counter downstream. Landing it beside other work makes the byte-identical-outcomes test unreadable."* Do not pick up adjacent work in this session.

---

## Ruling citations (authority for every clause below)

1. **`agentic_orchestration/gandalf/notes/2026-07-25-gd-grill-sheet.md` — RULING LEDGER, G-4 entry.** The operative ruling text. Reproduced here because every ambiguity in this dispatch resolves against it:

   > **G-4 RULED: (2) liveness-gate at application — UNIVERSAL.** Matt: "agree on Liveness-gate at application, but we need this for everything else too, right?" — ratified as the universal effect-application boundary rule: dead defenders receive nothing; no counter ever counts a corpse (all families: chill/slow/DoT/freeze/stun/procs). **Two exemptions:** (1) on-death payloads exempt BY DIRECTION (emission-from-corpse ≠ application-to-corpse; PoE-era signature element, GD census on-death rows); (2) intentional corpse-consumers exempt BY FLAG (`targets_corpse` on the effect — D2 Corpse Explosion is the canonical future case). **Forward-only:** pre-gate telemetry `landed:` counters stay poisoned; historical-season analyses must bracket or discard them (goes in the charter). G-4 remains the HARD PREREQUISITE to the G-3 calibration run.

2. **`agentic_orchestration/gandalf/notes/2026-07-25-g5-key-program-charter-draft.md` §1 build-queue row 0** — the five-clause exit test.
3. **Same charter, §2 WAVE 0** — entry/exit/why-solo, and the fidelity grade this wave enables.
4. **Same charter, §4 rider R-1** — forward-only telemetry poisoning. *"Any analysis crossing the gate boundary that does not declare which side it reads is invalid. This is the discipline, not a footnote."*
5. **Same charter, §6.2** — critical path; Wave 0 as single-point prerequisite.
6. **2026-06-20 `is_control != hard` ruling** — untouched by this wave. Do not re-litigate.

---

## Required reading before starting

- The two charter/grill-sheet files cited above (read the G-4 ledger entry and charter §1 row 0 / §2 Wave 0 / §4 R-1 / §6.2 in full — not just the excerpts here)
- Your own `simulation/AGENT_STATE.md` SESSION 73 § C2 — the `attempt_on_corpse:` / `landed_on_corpse:` instrumentation you already built is the measurement rig for this wave's exit test. Do not rebuild it.
- `simulation/MIGRATION.md` — the C2 correction of record lives there; this wave amends the same doc
- `jack-ryan` Gate-2 finding `agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md` (C2 section) — the epistemic standard this wave inherits
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 (math-before-code), #2 + #2.1 (smoke-test vs full-regen, resource-scaling rehearsal), #11 (attribution / reproduce-before-touching), #12 (semantic-shifting)

---

## Math-before-code (Discipline #1 — REQUIRED; this wave is not exempt)

A math note lands **before** the first line of gate code. It must state, at minimum:

1. **The predicate.** What "dead" means at application time, as an expression over combatant state, and read **when the effect arrives** — not after the call (your own C2 finding: *"a post-call read cannot answer 'already dead when it arrived'"*).
2. **The gate's position in the resolution order**, per application class, with the RNG-draw consequence made explicit (see Q-1 below — this is the load-bearing one).
3. **Semantic-shift register (Discipline #12).** Every behavior this gate changes that is not "a counter goes down." Name them numbered, as you did with shifts #1–#4 in the F8 note.
4. **The two exemption predicates**, each as an expression, with the direction/flag distinction spelled out — including which side of the boundary a self-targeted on-death effect falls on.
5. **Acceptance rows** mapping each of the five exit clauses to the artifact that satisfies it.

Line numbers live in the math note and **nowhere else** (your C3 structural fix — it holds here).

---

## Cross-seam contract change? (Principle 6 gate — knight-rider's answer, authored here)

**YES.** Two surfaces cross the seam boundary:

- **The forward-only telemetry marker (R-1)** — a new marker on emitted season/fight telemetry declaring which side of the gate a run sits on. Consumers are star-lord (export/telemetry) and every downstream analysis. This is an added field on a cross-seam fixture.
- **`targets_corpse`** — the exemption flag is declared *on the effect*, and the effect/ailment registry is not gamora's seam (see Q-3 below). Even the read-side default is a contract.

**Therefore the Acceptance criteria below MUST and DO include a round-trip clause.** `MIGRATION.md` is mandatory for this dispatch per ADR-004.

---

## Scope

- [ ] Math note landed **before** code (Discipline #1)
- [ ] Universal liveness predicate at **effect application**, applied across **all effect classes** — damage, ailments (chill/slow/freeze/stun/root/silence/sunder), DoT, HoT/healing credit, procs, and buff/debuff application to a defender
- [ ] Exemption path (a): **on-death payloads, BY DIRECTION** — emission-from-corpse is legal; application-to-corpse is not
- [ ] Exemption path (b): **intentional corpse-consumers, BY FLAG (`targets_corpse`)** — read-side implemented with an explicit, config-named default (no silent default; Pattern P7 stays rejected)
- [ ] Forward-only telemetry marker emitted on post-gate runs (R-1)
- [ ] `MIGRATION.md` amended — cross-seam impact per Principle 6 gate above
- [ ] Smoke gate passes before any full frame (Discipline #2 / #2.1)
- [ ] Full-frame re-run using the existing C2 `attempt_on_corpse:` / `landed_on_corpse:` instrumentation
- [ ] `AGENT_STATE.md` updated at session end
- [ ] Tag: `gamora/v-g4-liveness-gate-1`
- [ ] Submit to `agentic_orchestration/qa/pending/` for jack-ryan Gate 2 (see below)

---

## Acceptance criteria (charter §1 row 0, all five clauses — verbatim, plus this dispatch's process clauses)

- [ ] **Clause 1 — outcomes:** smoke season shows **fight outcomes byte-identical**. (If this proves unsatisfiable, see Q-1; do not silently relax it — halt and route.)
- [ ] **Clause 2 — counters:** `landed:` counters **strictly decrease**
- [ ] **Clause 3 — the headline:** corpse-share of chill applications **91.8% → 0.0% exact** (not "≈0", not "<1%" — exact zero, measured with the C2 rig)
- [ ] **Clause 4 — coverage:** **grep shows no application-class call site bypassing the predicate.** Publish the enumeration; a bypass found later is a Gate-2 finding
- [ ] **Clause 5 — exemptions:** **both exemptions unit-tested** — including a negative test per path (an on-death payload that must still fire; a `targets_corpse` effect that must still land; and a non-flagged effect on the same corpse that must not)
- [ ] **Clause 5b — forward-only marker present** on post-gate telemetry
- [ ] **Rig discrimination proven by ablation** — reverting the gate must fail a named subset of the new tests, and you state which ones pass and why (your F8 standard; jack-ryan will apply it)
- [ ] **Round-trip smoke:** a production-path season fixture is emitted post-gate and read at the gamora → star-lord telemetry boundary; the forward-only marker and any `landed_on_corpse:` keys are checked for presence and shape at the consumer side. Field-presence check published in `MIGRATION.md`.
- [ ] **Forward-only discipline stated in writing** (R-1): the marker's semantics, and the explicit statement that **pre-gate `landed:` counters stay poisoned and are not corrected**. No retroactive correction is performed or implied.
- [ ] **Gate 2 required:** submit the tagged commit to `agentic_orchestration/qa/pending/` for **jack-ryan DEV-MODE review with BLOCK authority**. **Do not self-clear this gate.** Knight-rider confirms closure; the downstream Wave-1 G-3 calibration and both §3 conversion loops fire on that confirmation, not on your tag.

---

## Smoke-test vs full-regen discipline (Disciplines #2, #2.1)

- Smoke gate fires **first** and must pass before any full frame is launched. No parallel regens of the same seed.
- Declare peak memory and verify against host RAM before the full frame (Discipline #1.1). The 64-cell/arm full frame you ran at C2 is the sizing precedent — state the projection, don't assume it carries.
- The smoke gate must itself include resource scaling (#2.1), not only correctness.
- Archive both smoke and full-frame JSON under `agentic_orchestration/gamora/notes/` with the date prefix, per your existing convention.

---

## Out of scope — explicit non-goals

- **No Wave-1 resolver primitives.** B1 (proc chance + ICD), B4 (stacking classes), B7 (invulnerability window — the `damage_resolver.py:1270` B13 deferral **stays deferred** in this wave), B9 (count operator). The charter permits KR to overlap B1/B4/B7/B9 with Wave 0; **this dispatch declines that overlap**, because the byte-identical-outcomes test is unreadable beside other landings (charter §2, "Why solo"). They get their own dispatch.
- **No G-3 control-role payload work.** No touching the 133 `"control"` placeholder instances, no resolver branch for control tokens, no freeze/stun registry reversal. G-3 rides a rocket-led dispatch; Wave 0 is its hard prereq, not its vehicle.
- **No telemetry backfill.** Pre-gate `landed:` counters stay poisoned. Do not correct, re-derive, annotate-in-place, or migrate historical seasons. The gate is forward-only by ruling.
- **No re-litigation of the 2026-06-20 `is_control != hard` ruling.**
- **No kill-resolution reordering.** That was G-4 option 3 and it was not the ruling. The gate is at application.
- **No scope into the `M_min=0.06` combined floor** or other SESSION-73 "NOT closed here" items.
- **No push to remote.**

---

## Open questions for the agent to resolve (document your answer in the math note)

- **Q-1 (LOAD-BEARING — resolve before writing code; escalate if it fights the exit clauses).** Does the gate short-circuit **before** the application roll (consuming no RNG draw) or **after** (roll, then discard)? These are not equivalent. Short-circuiting before the draw shifts every downstream RNG stream and would make **Clause 1 (byte-identical outcomes)** unsatisfiable; roll-then-discard preserves stream alignment and satisfies Clause 1 while still satisfying Clause 2 and Clause 3. Clauses 1 and 2 are only jointly satisfiable under one of these readings. **If your reading makes them mutually unsatisfiable, HALT and route to knight-rider — do not relax a clause on your own authority.**
- **Q-2.** Does the gate cover **attacker-side** on-hit effects triggered by a hit that lands on a corpse (`damage_resolver.py:1152/1164/1173` append to `attacker.active_effects`)? The ruling's plain reading is that the gate is *application-to-defender* — the attacker is not a corpse and is not "receiving nothing." But the ruling also says "no procs." State your reading, name it as a semantic shift if it changes attacker state, and flag it to knight-rider if you judge it genuinely two-way.
- **Q-3 (SEAM BOUNDARY).** `targets_corpse` is declared *on the effect*, and the ailment/effect registry (`config/ailments.yaml`, effect registry) is not gamora's seam. Implement the **read side** with an explicit named default; do **not** unilaterally edit a rocket-owned registry schema. Record the write-side requirement in `MIGRATION.md` as an owed item for rocket, and flag it to knight-rider for Wave-1 dispatch routing.
- **Q-4.** Does a **self-targeted on-death effect** — applied by the dying entity to itself, which is now dead — fall under exemption (a) by direction, or is it gated? The ruling distinguishes emission-from-corpse from application-to-corpse; a self-targeted on-death payload is both. State your reading; this is the one exemption case the ruling does not resolve on its face.
- **Q-5 (SCOPE WIDTH).** "Universal" spans more than one application path: `damage_resolver.py` (`_try_apply_ailment` at `:1595`, appends at `:1690`/`:1753`), `effect_resolver.py` (tick-side DoT/HoT), and the spatial-gauntlet path (`spatial_gauntlet/spatial_engine.py`, which carries its own liveness reads at `:2519`/`:2563` and its own effect appends at `:3024`/`:3101`/`:3105`/`:3944`). Clause 4's grep is the arbiter. State which engines are in frame and run the byte-identity test **per engine** — the two paths will not share one report.

---

## References

- `agentic_orchestration/gandalf/notes/2026-07-25-gd-grill-sheet.md` (RULING LEDGER, G-4)
- `agentic_orchestration/gandalf/notes/2026-07-25-g5-key-program-charter-draft.md` (§1 row 0, §2 Wave 0, §4 R-1, §6.2)
- `agentic_orchestration/qa/findings/2026-07-25-gate2-gamora-f8-cc-wiring.md` (C2 — the corpse-chill re-measurement standard)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 73 (the C2 instrumentation and archive)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (C2 correction of record; amended by this wave)
- Prior tags: `gamora/v-f8-cc-1`, `gamora/v-f8-cc-2`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #1.1, #2, #2.1, #11, #12)

---

## Gate status at authoring

- **Design-side pre-fire:** satisfied. gandalf PRIME REVIEW ACCEPTED the charter 2026-07-25; charter §2 waves are *"written to be lifted into dispatches verbatim,"* and Wave 0 is lifted verbatim here.
- **Process-side Gate 1 (jack-ryan DESIGN-MODE):** **not run.** Knight-rider's recommendation: a Gate-1 pass on **Q-1 alone** is cheap and worth it, because Q-1 is the one question that can make two ruled exit clauses mutually unsatisfiable. Matt's call whether to spend it; gamora may fire without it and route Q-1 if it bites.
- **Gate 2 (jack-ryan DEV-MODE, BLOCK authority):** **REQUIRED.** Non-waivable. Closure confirmed by knight-rider, not self-cleared.
