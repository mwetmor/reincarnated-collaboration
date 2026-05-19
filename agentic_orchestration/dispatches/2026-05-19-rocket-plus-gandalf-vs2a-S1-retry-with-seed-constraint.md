# Dispatch — 2026-05-19 — rocket + gandalf — VS2a S1 first-batch RETRY with seed constraint

**Authority:** AUTONOMOUS — VS2a hive pre-approval-batch (Matt directive 2026-05-19); knight-rider authoring under autonomous-operation protocol § 4.0 + § 4.5
**Triggering disposition:** `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` (gandalf) — Option 1 + 4 SELECTED; 5-season regen authorization WITHDRAWN; retry under substrate prior
**Parallel audit:** `agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md` (jack-ryan) — methodology conflation CONFIRMED; transposition REFUTED; four process fixes recommended
**Supersedes (validation gate methodology):** the original S1 dispatch § 2.4 ambiguity on instrument is hereby corrected — see § 2.4-bis below
**Status:** ACTIVE — fires immediately

---

## § 1 — TL;DR

Regenerate one season at a time under R8 `inverted` pipeline, applying the substrate-archetypal-stance prior, until canonical R1 sprint PASS is achieved or the 3-seed budget is exhausted. If the budget is exhausted, path (a) hand-redesign activates automatically per the original S1 dispatch branch (a). Each retry is **serial** — no parallel regens (Discipline #3).

**Retry budget:** 3 seeds (100002 → 100003 → 100004), serial, ~$3.20 per seed = ~$9.60 worst case.
**Authoritative gate:** canonical R1 sprint by gamora (`scripts/r1_class_retune_sprint.py`); rocket's pre-write measurement is diagnostic only.
**Substrate prior:** prefer wind/ember/grit/brine-action; reject char/pall/miasma; reject aftermath/mourning anchor framing; reject if convergence_failures > 50%.

---

## § 2 — Required reading (rocket)

1. `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` — full disposition; § 2.3 substrate prior is the operational guidance.
2. `agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md` — methodology conflation finding; understand the convergence-vs-canonical distinction before writing the next completion record.
3. `reincarnated-engine/output/R1-sprint-s1-firstbatch-2026-05-19/per_class_results.json` — gamora's canonical sprint format; reference output for what the authoritative measurement looks like.
4. `agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-kit-redesign-sprint.md` — original S1 dispatch; § 2.4 gate criteria are reaffirmed with § 2.4-bis clarification below.

---

## § 2.4-bis — Gate methodology clarification (Discipline #11 + jack-ryan Fix 1 + Fix 4)

The original S1 dispatch § 2.4 specified threshold-only criteria. This led to methodology conflation (convergence-time vs canonical R1 sprint). The corrected gate methodology is:

**Criterion 1 (boss_kr ≥ 0.10 on ≥ 1 class)** — measured by canonical R1 sprint via `scripts/r1_class_retune_sprint.py` on the regenerated season, output at `output/R1-sprint-s1-retry-N-<seed>-<date>/per_class_results.json` where N is the retry number.

**Criterion 2 (mini_boss_kr ≥ 0.15 on ≥ 2 classes)** — same canonical R1 sprint instrument as Criterion 1; same output file.

**Criterion 3 (cohesion ≥ 4.0)** — gandalf cohesion judgment via R8 6-facet rubric.

**Criterion 4 (no template debris)** — rocket inspection of `classes.json` for "Unknown" leaks, all-lowercase entries, generic-template saturation; report results with source paths cited.

**Criterion 5 (substrate-identity invariant)** — rocket inspection of substrate-mode-of-action preservation under R8 § 9.5 strict read; report percentage with source paths cited.

**Rocket's pre-write measurement is diagnostic only.** Any number rocket reports in the completion record must cite:
- The exact script invocation (e.g., `python scripts/r1_class_retune_sprint.py --season-ids season_100002 --staging-dir output/S1-retry-1-2026-05-19/season_100002`)
- The output file path (e.g., `output/R1-sprint-s1-retry-1-100002-2026-05-19/per_class_results.json`)
- The commit SHA at which the script was run

**No completion-record number is gate-eligible without script + output-path + commit citation.** Convergence-time kill-rate estimates from the generation pipeline are NOT gate-eligible. Label them "Convergence-time estimates — NOT canonical R1 sprint measurements — NOT gate-eligible" in any reporting (per jack-ryan Fix 2).

---

## § 3 — Operational plan

### § 3.1 — Retry sequence (serial)

**Retry 1 — seed 100002:**

1. Run R8 inverted pipeline with seed 100002. Output to `output/S1-retry-1-100002-2026-05-19/season_100002/`.
2. Inspect anchor + cosmological-vocabulary after generation completes (before LLM-naming, if possible — or post-naming if not). If anchor reads aftermath/mourning OR element is char/pall/miasma/rime: re-roll. Increment to seed 100003. (Substrate prior reject condition.)
3. Inspect `validation_report.json::summary::convergence_failures`. If > 50% of classes have `convergence_status="failed"`: re-roll. Increment to seed 100003. (Pre-coalescence pathology reject condition.)
4. If both checks pass: STAGE the season for canonical R1 sprint. HANDOFF to gamora via hive log REQUEST. **Do NOT report rocket's pre-write numbers as gate-PASS.** Rocket may report pre-write numbers as diagnostic, prefixed with the disclaimer above.
5. AWAIT gamora canonical R1 sprint + gandalf cohesion judgment.
6. If both PASS: this retry is the surviving seed; STOP the retry sequence; HANDOFF to knight-rider for full 5-season regen authorization.
7. If either FAIL: increment to seed 100003 and resume at step 1.

**Retry 2 — seed 100003:** as Retry 1.

**Retry 3 — seed 100004:** as Retry 1.

**Fallback activation:** if Retry 3 also fails, path (a) hand-redesign activates per the original S1 dispatch branch (a). No further gandalf re-disposition. Rocket pivots. Gandalf consult cadence per original.

### § 3.2 — Substrate prior (gandalf § 2.3 verbatim)

**Prefer (likely damage-throughput-native):**
- wind-derived (gale, breath, scour)
- ember-derived (ignition, ash-DOT distinct from char-as-residue)
- grit-derived (impact, hardened, shear)
- brine-derived **if** anchor frames action rather than aftermath

**Avoid (likely aftermath/mourning-stance):**
- char-derived (battlefield-aftermath)
- pall-derived
- miasma-derived
- rime-derived

**Cautious (in-flight check):**
- mud, bog, salt, soot

**Soft constraint, not hard block.** Rocket may surface judgment if a particular seed-substrate composition reads as boss-throughput-viable even from the avoid list (e.g., "ruined siege engine still walks" framing on char). Surface to gandalf via hive log REQUEST.

### § 3.3 — Cost budget

~$3.20 per seed × 3 retries = ~$9.60 worst case before fallback. Acceptable.

---

## § 4 — Acceptance criteria

- [ ] Retry 1 (seed 100002) attempted under R8 inverted with substrate prior applied
- [ ] If Retry 1 rejected on substrate prior or convergence-failure threshold: rationale recorded in hive log STATE entry; retry incremented
- [ ] If Retry 1 staged: canonical R1 sprint dispatched to gamora; cohesion judgment dispatched to gandalf
- [ ] [serial-conditional] Retry 2 (seed 100003) if Retry 1 fails gate
- [ ] [serial-conditional] Retry 3 (seed 100004) if Retry 2 fails gate
- [ ] [conditional] Path (a) fallback activates if Retry 3 fails gate
- [ ] All measurement claims in any completion record carry script + output-path + commit citation (Discipline #11 enforcement)
- [ ] AGENT_STATE.md updated after each retry attempt
- [ ] Convergence summary table in AGENT_STATE labeled "Convergence-time estimates — NOT canonical R1 sprint measurements — NOT gate-eligible" (per jack-ryan Fix 2)
- [ ] Hive log STATE + HANDOFF entries at each retry boundary
- [ ] Knight-rider notified at retry conclusion (PASS or fallback activation)

**Tag plan:** `rocket/v1.23-s1-first-batch-retry-N-regen` (intermediate seam tag) where N = 1, 2, or 3 depending on which retry succeeds; OR no rocket tag and a CHANGELOG note if path-a fallback activates. Knight-rider fires on successful retry.

---

## § 5 — Out of scope

- 5-season regen on the surviving seed (separate dispatch; gated on this retry's PASS)
- R8 cohesion-judging protocol amendment (gandalf § 5.3 follow-on; deferred)
- Discipline ledger entry (jack-ryan audit follow-on)
- season_100001 prose retention as cohesion-5 anchor referent (gandalf already authored; no rocket work)
- Any work on R8 § 5b pipeline gap (`seasonal_dominant_element` write-back; separate)

---

## § 6 — Cross-seam HANDOFFs required from rocket

- **rocket → gamora:** for any retry that passes the substrate prior + convergence-failure threshold checks, file hive log REQUEST asking gamora to run `scripts/r1_class_retune_sprint.py` on the staged season. Output path expectations stated above.
- **rocket → gandalf:** for any retry that passes gamora's canonical R1 sprint PASS check, file hive log REQUEST asking gandalf for cohesion judgment per R8 6-facet rubric.
- **rocket → knight-rider:** at the end of each retry boundary, file STATE entry summarizing pass/fail status + reject reason if rejected.

---

## § 7 — Process fix enforcement (Discipline #11; jack-ryan audit recommendations)

Per jack-ryan's audit § 4:

- **Fix 1 (instrument specification):** § 2.4-bis above corrects this for the retry. Carries forward to future first-batch dispatches.
- **Fix 2 (convergence-time labeling):** rocket's AGENT_STATE.md convergence summary table must carry the header "Convergence-time estimates — NOT canonical R1 sprint measurements — NOT gate-eligible."
- **Fix 3 (Gate 2 audit before tag-fire):** knight-rider will NOT fire a retry-PASS tag without surfacing the gate completion record to jack-ryan (or a designated reviewer) for a 15-minute audit. This applies to `rocket/v1.23-s1-first-batch-retry-N-regen` when fired.
- **Fix 4 (knight-rider authoring responsibility):** acknowledged. This retry dispatch carries the instrument specification. Future first-batch dispatches must do the same.

---

## § 8 — Open questions for rocket (decisions allowed within seam authority)

- **Substrate-prior judgment calls** — L1 rocket. If a borderline substrate (mud/bog/salt/soot) produces an action-stance anchor, rocket may proceed without re-rolling. Document the judgment in the STATE entry.
- **Avoid-list override** — L1 rocket may surface to gandalf via hive log REQUEST. Do not proceed without gandalf disposition if overriding the avoid list.
- **Convergence-failure threshold** — soft at > 50%. If 50-60% is borderline, rocket may judge and proceed. Document.
- **Seed sequence beyond 100004** — out of scope; this dispatch caps at 3 retries.

---

## § 9 — References

- `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` (gandalf disposition — the basis of this dispatch)
- `agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md` (jack-ryan audit — the basis of § 2.4-bis + § 7)
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` lines 3950-4081 (cohesion + R1 + gamora REQUEST + gandalf disposition)
- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-kit-redesign-sprint.md` (original S1 dispatch; § 2.4 superseded by § 2.4-bis above)
- `reincarnated-engine/output/R1-sprint-s1-firstbatch-2026-05-19/per_class_results.json` (canonical R1 sprint reference output format)
- `reincarnated-engine/output/R8-ab-run-2026-05-19/inverted/season_099002/validation_report.json` (counter-evidence to brine-viable claim — 6/10 convergence_failures)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #3 serial-regen, #11 attribution, #15 drift-detection)

---

## § 10 — Autonomous-operation authority + Matt re-entry trigger

This dispatch fires immediately under VS2a hive pre-approval-batch authority. Matt re-entry triggers:

- **Trigger A — path (a) fallback activates** (all 3 retries fail): surface to Matt; the 4-6 week rocket fallback investment warrants re-confirmation.
- **Trigger B — substrate-prior override requested** (rocket surfaces an avoid-list seed for override): gandalf disposes first; if gandalf escalates, Matt sees it.
- **Trigger C — methodology audit surfaces a systemic finding** (jack-ryan parallel audit; already filed): knight-rider has a Matt briefing on deck; surfaces at natural wind-down.

Otherwise: autonomous execution continues. Matt's "do not stop unless I intervene" stands.

---

*Authored 2026-05-19 by knight-rider under VS2a hive pre-approval-batch authority. The disposition is gandalf's; the methodology fixes are jack-ryan's; the dispatch is the operational consolidation. The road to L1 ship continues, with sharper measurement discipline and a substrate-aware seed prior. The Battlefield Where Nothing Grew Back stays in the engine's anchor library; its kits do not.*
