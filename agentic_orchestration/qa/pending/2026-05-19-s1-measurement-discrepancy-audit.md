# Finding — 2026-05-19 — VS2a S1 first-batch measurement discrepancy audit

**Reviewer:** jack-ryan (DEV-MODE; Gate 2)
**Severity:** BLOCK (on the PASS claim, not on the work)
**Target:** `rocket/v1.22-s1-first-batch-regen` (intermediate seam tag, engine repo)
**Developer:** rocket
**Principles applied:** Review Process Principles #1 (evidence-grounded), #3 (separation of description from prescription)

---

## 1. Finding: TRANSPOSITION REFUTED — methodology conflation CONFIRMED

The 0.130 and 0.240 figures rocket reported in the S1 first-batch validation gate for season_100001 are rocket's own convergence-pipeline measurements — they appear in rocket's AGENT_STATE.md convergence summary table (lines 34–44) and are reproduced verbatim in the dispatch completion record validation gate table. **These are convergence-time kill rate estimates, not canonical R1 sprint outputs.**

**Evidence chain:**

- **Source of 0.130 / 0.240:** AGENT_STATE.md `## STATE (2026-05-19 — VS2a S1 first-batch regen COMPLETE)` convergence summary table, columns `boss_kr` and `mini_kr`, rows class_0002 and class_0007. These are population estimates computed by the generation-time convergence pipeline at floor modifier (N=30 fights per matchup; production cardinality NOT used; disposition-3 calibration NOT applied).

- **What gamora's canonical R1 sprint found:** `output/R1-sprint-s1-firstbatch-2026-05-19/per_class_results.json` — all 11 classes: `boss_kill_rate: 0.0`, `mini_boss_kill_rate: 0.0` (except class_0005 at `mini_boss_kill_rate: 0.4`). Summary: `n_pass: 0`, `pass_rate: 0.0`. The 0.0 boss and mini-boss rates reflect structural kit failure against production-calibrated encounter difficulty.

- **What the validation_report.json shows:** Season_100001's own `validation_report.json` uses `convergence_winrate` entries only. **No `boss_kill_rate` or `mini_boss_kill_rate` fields exist in the file.** The 0.130 / 0.240 figures in rocket's gate table have no backing file in the season output — they were extracted by rocket directly from the convergence loop's in-memory state during generation, not from a post-hoc measurement artifact that can be independently audited.

- **R8 A/B transposition hypothesis (gamora's hypothesis) — REFUTED.** `output/R8-ab-run-2026-05-19/inverted/season_099002/validation_report.json` contains no `boss_kill_rate` or `mini_boss_kill_rate` fields at all, and its per-class modifiers (0.0509–1.0) bear no correspondence to the 0.130 / 0.240 figures. **The numbers did not come from season_099002.** They came from season_100001's own convergence pipeline run.

**Revised finding:** This is not a cross-season transposition (099002 → 100001). It is a **methodology conflation**: rocket treated convergence-time kill rate samples (computed at floor modifier during the generation pipeline, N=30 per matchup, not disposition-3 calibrated) as equivalent to canonical R1 sprint kill rate measurements. The same season, different methodology, different result.

---

## 2. Root cause: methodology conflation — not copy-paste

Root cause is (b) — a methodology gap, not (a) a copy-paste from another session.

The generation pipeline's convergence loop produces per-class kill rate estimates as a side-effect of running fights during modifier convergence. These estimates are at floor modifier (typically 0.0509), with N=30 fights per tier, **without** the disposition-3 encounter recalibration that gamora's canonical R1 sprint applies. Rocket captured these convergence-time estimates in the AGENT_STATE.md convergence summary and treated them as meeting the § 2.4 gate criteria.

The canonical R1 sprint (`scripts/r1_class_retune_sprint.py`, gamora-authored) uses `fights_per_matchup=30` but **with** disposition-3 calibration applied, a different convergence target, and a different modifier endpoint (post-convergence, not floor). The two methodologies produce structurally different outputs. At floor modifier with weak kits against standard encounters, some kill rates appear nonzero. At disposition-3 calibration with post-convergence modifiers, the same kits show boss WR = 0.0 system-wide because the structural pathology is exposed by the calibrated tier difficulty.

Rocket's convergence summary table in AGENT_STATE.md is correctly labeled "Convergence summary" — but when copied into the validation gate table, the source-methodology distinction was dropped. The gate reported "PASS (2/11; class_0002: 0.130, class_0007: 0.240)" without identifying these as convergence-time estimates rather than R1 sprint measurements. **This is the specific failure point.**

---

## 3. Discipline violations

- **Discipline #11 (Empirical inspection over assumption)** — VIOLATED. The gate required canonical R1 sprint results. Rocket used convergence-time side-channel estimates without running the canonical measurement script.

- **Discipline #10 (Attribution clarity — change one thing, measure one thing)** — VIOLATED in aggregate. The S1 gate was supposed to measure post-regeneration kit quality under canonical R1 conditions. By using convergence-time estimates, rocket measured kit quality under a different condition (floor modifier, pre-disposition-3) and attributed the result to the gate.

- **Discipline #2 (Smoke-test vs full for milestones)** — proximate analog. Convergence-time kill rates are the functional equivalent of a smoke-level measurement. Using smoke-level data to report milestone-level gate results violates the spirit of this discipline.

- Engineering discipline #6 is **not** violated — tagging was correctly marked intermediate (`rocket/v1.22-s1-first-batch-regen`, seam-level, not milestone).

**How it was missed:** The dispatch § 2.4 specified "boss_kr ≥ 0.10 on ≥ 1 class" as a criterion **without explicitly specifying the measurement instrument**. Rocket had available kill rate estimates from the convergence pipeline and used them. **The dispatch's ambiguity on instrument allowed the conflation.** This is a process gap, not purely a rocket error.

---

## 4. Process fix recommendation

Four concrete changes, ranked by impact:

**Fix 1 (highest): Gate criterion must specify instrument, not just threshold.** The § 2.4 gate criteria must read: "boss_kr ≥ 0.10 on ≥ 1 class AS MEASURED BY canonical R1 sprint (`scripts/r1_class_retune_sprint.py`)." Threshold-only criteria invite instrument substitution. Every S1 validation gate entry must include a provenance line: *"Measured via: `<script>` run at commit X on season Y, output at path Z."* Without this line, a gate entry is incomplete.

**Fix 2: Convergence-time kill rate estimates must be labeled as provisional, not gate-eligible.** The AGENT_STATE.md convergence summary table is appropriate for design archaeology. It must carry a header: "Convergence-time estimates — NOT canonical R1 sprint measurements — NOT gate-eligible." This prevents a future agent from promoting these values to a gate table.

**Fix 3: Gate 2 audit before knight-rider tag-fires any first-batch validation gate PASS.** For S1 first-batch (and any subsequent batch), knight-rider must surface the gate completion record to jack-ryan before firing a PASS tag. A 15-minute read of the per_class_results.json vs the gate table would have caught this before the discrepancy required gamora to surface it post-hoc.

**Fix 4: Dispatch author (knight-rider) is responsible for instrument specification.** Dispatches that include measurement-gated acceptance criteria must name the measurement script and output file path, not just the threshold. **This is a knight-rider authoring responsibility, not a developer responsibility.** The VS2a S1 dispatch's § 2.4 is the failure point of origin.

---

## 5. Trust scope: not systemic — but targeted prior-record audit warranted

This is **not a systemic pattern** in the sense of deliberate falsification or repeated cross-season transposition. The mechanism is a methodology conflation — a specific, identifiable error type tied to the S1 first-batch context where convergence-time estimates were structurally available and the gate instrument was underspecified.

However, the same error class — using a convenient in-pipeline proxy metric instead of the canonical measurement instrument — could recur in any context where (a) convergence-time estimates are available and (b) the gate criterion doesn't name the instrument. This is worth a targeted audit of prior completion records, not a full rocket reliability investigation.

**Recommended targeted audit (knight-rider to execute):**

- R8 A/B completion record: did rocket cite any kill rate or balance figures without naming the source script?
- R1 sprint completion records (R1 v2, v3): these are gamora-authored, not rocket-authored — not affected.
- R3 backfill: scope was structural (field backfill), not balance measurement — low risk of this error class.
- R7 parity report: check whether any parity figures cite convergence-time estimates vs canonical script output.

Rocket's convergence work (AGENT_STATE.md convergence summary, schema deliverables, MIGRATION.md entries) appears structurally sound across the record reviewed. **The error is localized to the kill rate gate methodology, not to generation or schema work.**

---

## 6. BLOCK disposition

The `rocket/v1.22-s1-first-batch-regen` tag should **NOT** be promoted to a first-batch PASS milestone until:

1. The canonical R1 sprint is run against season_100001 — **gamora has already done this**; output exists at `output/R1-sprint-s1-firstbatch-2026-05-19/per_class_results.json`
2. The gate table in the dispatch completion record is updated to reflect the canonical R1 sprint results (criteria 1 and 2: FAIL)
3. The first-batch PASS/FAIL determination is re-evaluated under the correct data

**Based on gamora's canonical R1 sprint: criteria 1 and 2 FAIL. The S1 first-batch does NOT currently meet the § 2.4 validation gate.** This is the expected outcome for a first-pass R8-inversion regen of a broken catalogue — the S1 sprint's purpose is to iterate until the threshold is achieved, not to gate-pass on first regen. The gate result being FAIL is not a catastrophic finding; it is the correct starting state for a 2–3 week iterative sprint. **The BLOCK is on the incorrect PASS claim, not on the work quality.**

**Escalation required:** This finding goes to knight-rider for dispatch amendment (§ 2.4 instrument specification) and completion record correction. Matt review warranted given the BLOCK severity and the process fix recommendations that affect future dispatch authoring standards.

---

## References

- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-kit-redesign-sprint.md` § 2.4 + Completion record
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` lines 32–56 (convergence summary + gate table)
- `reincarnated-engine/output/R1-sprint-s1-firstbatch-2026-05-19/per_class_results.json` (gamora canonical R1 sprint — authoritative)
- `reincarnated-engine/output/S1-first-batch-2026-05-19/season_100001/validation_report.json` (no kill rate fields present)
- `reincarnated-engine/output/R8-ab-run-2026-05-19/inverted/season_099002/validation_report.json` (cross-season transposition hypothesis — refuted)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` Disciplines #2, #10, #11

---

*Filed 2026-05-19 by jack-ryan (DEV-MODE Gate 2). The PASS claim was structurally incorrect, the work was not. The dispatch authoring is the failure point of origin; the methodology was conflated downstream. Process fixes target both ends. Knight-rider routes to Matt for BLOCK approval + future-dispatch standard adoption.*
