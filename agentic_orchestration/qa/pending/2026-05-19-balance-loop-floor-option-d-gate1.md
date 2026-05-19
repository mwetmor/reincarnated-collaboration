# Gate 1 Review — Balance-Loop Floor Option D — 2026-05-19

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate 1 — pre-decisions-log)
**Disposition:** APPROVE WITH AMEND
**Work item:** `2026-05-19-balance-loop-floor-option-d-gate1`
**Developer under review:** gamora (investigation); knight-rider to route to Matt for Trigger A approval

---

## § 1 — Discipline #12 semantic-shift surface

### What changes semantically

The floor change `low=0.05 → low=0.01` is a 4-line LOC change with a non-trivial semantic surface. Three distinct semantic layers are touched:

**Layer 1 — Convergence status semantics.** A class that exits today as `status=failed, modifier=0.0509` would exit as `status=converged, modifier=0.01–0.04`. This flips the gate outcome. "Converged" has historically meant "the kit was balanced within the search range." Post-Option-A, it means "the kit was balanced somewhere in [0.01, 4.0], including extreme-suppression territory." The design record should acknowledge this is a widened definition of "converged," not a correction of a prior definition.

**Layer 2 — Implicit floor-as-quality-signal.** Gamora correctly surfaces this in § 5.1: the floor partly served as an exposure mechanism for kit pathology. A class that cannot converge above 0.05 is a signal that the kit has structural over-power. Option A converts that signal from a visible failure to a converged-but-suppressed state. This is the most consequential semantic shift. It is not wrong — extreme suppression IS a valid convergence state — but it is a design decision, not a mechanical fix, and should be framed that way in the decisions-log entry.

**Layer 3 — Downstream consumers of modifier values.** I read lines 60-73 and confirmed `DOPPELGANGER_MODIFIER_FLOOR = 0.30` at line 62. This is a separate constant with a separate purpose: it prevents doppelganger timeout artifacts. A class converging at modifier=0.02 would still be evaluated by the doppelganger gate at `DOPPELGANGER_MODIFIER_FLOOR=0.30` — the doppelganger deliberately does not use the converged modifier. **No breakage here.** The doppelganger gate is insulated from the floor change.

The `MODIFIER_LOW_THRESHOLD=0.30` recompose trigger (line 70) is also unaffected — it fires on `eval_modifier < 0.30`, which remains true for floor-locked classes regardless of whether the floor is 0.05 or 0.01.

**Are there downstream consumers that assume `modifier ≥ 0.05`?** No consumer hard-codes this assumption in the constants block (lines 60-73). The constants in that block are decoupled from each other by documented purpose. The one risk is in tests: gamora's investigation does not report whether any test explicitly asserts `modifier ≥ 0.05`. This is a smoke gate I add below.

**Telemetry / decisions-log range assumptions.** Prior decisions-log entries and telemetry interpretations that use "floor-locked = modifier ≈ 0.0509" as a diagnostic signal will need a terminology update. Specifically: the phrase "modifier at floor" will no longer have a single stable meaning — it will mean 0.0101 (post-Option-A) for newly-run seasons, while historical seasons still show 0.0509. Any dashboard or query using `modifier < 0.06` as a floor-lock filter must be updated to `modifier < 0.02` post-Option-A. MIGRATION.md note is not optional here — it is a concrete consumer change requirement for star-lord's telemetry work.

**Cross-seam: star-lord.** Gamora's § 6.3 notes the telemetry value distribution shifts — the `final_modifier` field schema is unchanged but values in the [0.01, 0.05) range will appear for the first time. Existing queries that assume the modifier distribution starts at 0.05 will misread these new values. For Option B's `recompose_outcome` new enum value: confirmed as a schema-adjacent change requiring MIGRATION.md entry and star-lord notification before Option B ships.

**Verdict on Discipline #12:** the shift is real, it is bounded, and it is manageable — but it must be named explicitly as a design decision, not treated as a transparent 4-line fix. The decisions-log entry framing in § 5 below must do this work.

---

## § 2 — Discipline #15/#18 implicit-pillar finding

Gamora's investigation confirms what gandalf § 9.8 surfaced: `low=0.05` appears at four independent sites (lines 767, 891, 1247, 1941) with no named constant and no module-level documentation of its design rationale. The partial rationale in the line 756-757 comment ("Floor 0.05 (not 0.20): high-armor/high-HP archetypes need very low modifiers") is function-scoped, not module-level, and covers only one of the four sites.

**Is naming alone sufficient?** Naming to `MODIFIER_SEARCH_FLOOR` is necessary and closes the immediate Discipline #18 gap. But two follow-ons should be captured in the decisions-log entry rather than left as institutional memory:

**Follow-on 1 — Module-level constants audit.** The four floor sites are the ones gamora found. The question is whether any other implicit numerical pillars exist in `balance_loop.py` that have the same pattern: hard-coded literal with no named constant, appearing at multiple sites, with load-bearing behavior. The line 767 comment references B10.4 §14.6 and a derivation math note — evidence that the constant has a design history, but that history is not accessible from the constant itself. A targeted audit of other hard-coded literals in `balance_loop.py` is warranted as a follow-on item (not blocking Option A). Suggested scope: grep for any float literal appearing at 2+ sites in the file.

**Follow-on 2 — Docstring content specification.** The `MODIFIER_SEARCH_FLOOR` constant's docstring should capture at minimum: (a) why 0.05 was chosen vs 0.20 in B10.4, (b) what breaks if it goes below 0.01 (simulation runtime? semantic validity?), (c) that four call sites reference it, and (d) the design decision number that changed it. This is the "design rationale in the constant" standard; without it, the next engineer to adjust the floor will face the same implicit-pillar problem in a different form.

Neither follow-on is blocking for Option A. Both should appear in the decisions-log entry as explicit non-gating action items so they don't evaporate.

---

## § 3 — Sequence audit: Option A first

Gamora argues A is the immediate stop-gap; B is the design-correct fix this week. The question from my angle is whether landing A first risks cementing the semantic shift in a way that makes B harder.

**Does A cement the shift before B lands?** Partially, but acceptably. Option A will produce converged seasons at modifier=0.01–0.04. If those seasons ship or are used for calibration before B lands, downstream agents (rocket, star-lord) will accumulate artifacts calibrated against the widened floor. Option B, when it lands, would produce *different* kit compositions for the same seeds (via DPS-aware recompose) — which means the Option-A-generated seasons may need to be regenerated post-Option-B to get design-correct outputs.

**Risk assessment: LOW for a time-boxed window.** The critical question is whether Option A seasons are treated as disposable diagnostics (which is the stop-gap framing) or as shippable artifacts. If knight-rider's dispatch for Option A explicitly states "Option-A seasons are diagnostic-only; not promotion candidates until Option B lands and seasons are regenerated under the correct mechanism," the cement risk is contained.

**Recommend an explicit temporal gate clause in the Option A approval:** any season generated during the Option-A window is tagged `diagnostic-only-floor-widened` and is not eligible for first-batch promotion until Option B lands. This is a process clause, not a code clause. Knight-rider enforces it.

**Does the sequence risk a roll-back scenario?** No. Option A is 4-line reversible at any point. If Option B investigation reveals the recompose re-conditioning cannot be achieved safely within the week, Option A can stand as a permanent widening (it is semantically defensible on its own). The decisions-log entry should state this explicitly: Option A is independently valid; Option B is the preferred end-state but does not gate Option A's validity.

---

## § 4 — Test-coverage / smoke recommendations

Before Option A lands (post-Matt approval), knight-rider should require the following smoke gates from gamora:

**Smoke gate A1 — Floor-lock regression smoke.** Re-run one floor-locked class (recommend class_0001 from season_100002, fire_mage — the clearest over-power case) at the widened floor. Confirm `status=converged` and `modifier` lands in [0.01, 0.05). Confirm per-tier WR at the converged modifier is meaningfully in-band for lower tiers (swarm/magic/elite should drop below ceilings; boss may still be low — that is acceptable). This is a 1-class smoke (Discipline #2 cost: ~51s).

**Smoke gate A2 — Test-assertion audit.** Before the 4-line change lands, run `grep -n "0\.05\|modifier.*floor\|floor.*modifier\|low.*0\." balance_loop_test*.py` and any test files that import `balance_loop`. Confirm no test asserts `modifier >= 0.05` or encodes the floor value literally. If any such assertion exists, it is a Discipline #9 violation (test asserts magic number rather than deriving from spec) AND must be updated as part of Option A, not as a follow-on.

**Smoke gate A3 — Telemetry-recorder range check.** Confirm that star-lord's `spatial_fight_results` recorder and the `class_balance_results` writer do not have any range-validation guard that would reject or clip `modifier < 0.05`. This is a 5-minute read check, not a run; but it must be done before Option A lands, not discovered after.

**Smoke gate A4 (pre-Option-B gate) — Recompose lever delta at widened floor.** Before Option B implementation begins, run one smoke at modifier=0.025 for a floor-locked class and confirm lever deltas are non-zero. This validates the premise of Option B: that lever signal exists at the widened floor range. If deltas are still zero at 0.025, Option B's architecture assumption has a different failure mode than diagnosed and re-investigation is required before committing to the 25-50 LOC change.

---

## § 5 — Decisions-log entry framing

Suggested text for the decisions-log entry (knight-rider to finalize):

> **2026-05-19: Balance-loop modifier-search floor widened to 0.01 (Option A stop-gap); Option B (floor-lock recompose re-conditioning) authorized for this-week implementation.** The binary-search lower bound `low=0.05` was hard-coded at four sites in `balance_loop.py` with no named constant; R8-inverted pipeline produces kits that require modifier ~0.02-0.04 to converge, below the prior floor. Option A (4-line change: `low=0.05 → low=0.01`, promoted to `MODIFIER_SEARCH_FLOOR` named constant) is the validated stop-gap; classes converging at modifier < 0.05 now exit `status=converged` with extreme-suppression modifier rather than `status=failed`, which is a semantic shift per Discipline #12 (modifier range widens from [0.05, 4.0] to [0.01, 4.0]). Option-A-generated seasons are diagnostic-only until Option B lands; MIGRATION.md note required for telemetry consumers using modifier < 0.06 as a floor-lock filter. Option B (re-condition recompose trigger to detect floor-lock and retry via lower working modifier) is the design-correct follow-up; reversion path for Option A is reversible at any point.

---

## § 6 — BLOCK / amend / approve disposition

**Disposition: APPROVE WITH AMEND**

Gamora's investigation is methodologically sound. The diagnosis is well-evidenced (empirical confirmation at § 3, mechanism confirmation at § 4, structural root cause at § 4.4). The Option D recommendation is sequenced correctly. No Discipline #12 violation is being committed — the shift is being named and framed, which is exactly what the discipline requires.

**Amendments required before knight-rider routes to Matt:**

1. **Add "diagnostic-only" temporal gate** to the Option A dispatch: seasons generated under Option A floor are not promotion-eligible until Option B lands. Knight-rider to add this clause to the Trigger A approval request.

2. **Smoke gate A2 (test-assertion audit) is blocking for Option A.** The test audit must be done before the 4-line change lands, not as a follow-on. If any test encodes `modifier >= 0.05` literally, the code change and the test fix must land in the same commit.

3. **MIGRATION.md note is required at Option A landing.** This is not a follow-on. Telemetry consumers that query `modifier < 0.06` as a floor-lock signal will misinterpret historical vs new data without it.

4. **Smoke gate A4 (lever delta at 0.025) must be authored as a blocking acceptance criterion for Option B dispatch.** Not required before Option A, but must be named in the Option A decisions-log entry as a prerequisite for Option B kickoff.

**What I am not blocking:** the design intent concurrence is gandalf's lane. The runtime-overhead estimates for Option B (16-24% for floor-locked seasons) are gamora's domain assessment — I take them as informational. The LOC count (25-50 for Option B) is implementation-estimation by the developer; no process concern.

**Matt routing note:** this is a Discipline #12 semantic shift + a cross-seam telemetry impact. Both meet the escalation threshold per ADR-002. The amendments above are process-level; Matt's approval is for the design-intent concurrence that the widened floor is the correct fix direction. Knight-rider routes after gandalf concurs.

---

**Signed:** jack-ryan, DESIGN-MODE Gate 1, 2026-05-19.

**Files read for this review:**
- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md`
- `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 9
- `agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md`
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` lines 60-73, 755-769, 883-894, 1235-1262, 1933-1954
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

*Captured to qa/pending/ by knight-rider 2026-05-19 from jack-ryan's text return. Verbatim with file-path lint adjustments only.*
