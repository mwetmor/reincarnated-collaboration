# Dispatch — 2026-05-19 — gamora — Balance-loop floor investigation (INVESTIGATION ONLY)

**Authority:** AUTONOMOUS L2-equivalent per VS2a hive pre-approval-batch § 4.5. **NO IMPLEMENTATION** without knight-rider + gandalf + (Trigger A) Matt approval.
**Triggering disposition:** `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 9 (gandalf re-disposition; substrate hypothesis WEAKENED; pivot to balance-loop floor investigation)
**Time-box:** 1-2 days, smoke-test mode (Discipline #2)
**Status:** ACTIVE — fires immediately

---

## § 1 — TL;DR

Three R8 inverted seasons (099002 brine / 100001 char / 100002 ember) show 60-80% of classes floor-locked at modifier=0.0509 — the binary-search lower bound in `balance_loop.py`. Substrate hypothesis is empirically weakened. **Investigate the floor mechanism. Propose options. Do not implement.** Gandalf + Matt approval gates any code change.

---

## § 2 — Required reading

1. `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 9 — full re-disposition; § 9.3 is the diagnostic frame; § 9.7 is the investigation scope you're executing
2. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` lines 64-73 (B14.5 V1 recompose-first constants); lines 767, 891, 1247, 1941 (`low, high = 0.05, 4.0` — the four hard-coded floor sites)
3. Three validation_report.json files:
   - `output/S1-retry-1-100002-2026-05-19/season_100002/validation_report.json` (8/10 floor-lock — ember)
   - `output/R8-ab-run-2026-05-19/inverted/season_099002/validation_report.json` (6/10 floor-lock — brine)
   - `output/S1-first-batch-2026-05-19/season_100001/validation_report.json` (8/11 floor-lock — char)
4. `project_iterative_dev_disciplines.md` — B14.5 V1 recompose-first architecture; MODIFIER_LOW_THRESHOLD=0.30 trigger semantics

---

## § 3 — Investigation scope (4 questions to answer, in this order)

### § 3.1 — Empirical (spot-check diagnosis)

**Question:** Are floor-locked classes *over-powered* at modifier=0.0509 (kits exceed target WR even at minimum modifier), or are they *under-powered* at floor (kits fail target WR everywhere including floor — different mechanism)?

**Method:**
1. Pick 1-2 floor-locked classes from season_100002 (the ember retry; rocket's STATE entry has them flagged at modifier=0.0509)
2. Run a smoke-mode `r1_class_retune_sprint.py` on those classes at modifier=0.0509 (the floor) — single tier or multi-tier as cheap; output to `output/R2-floor-investigation-2026-05-19/`
3. Report boss_kill_rate + mini_boss_kill_rate + per-tier WR for those classes at the floor modifier

**Diagnostic interpretation:**
- If WR > 0.5 at boss tier OR > 0.65 at mini_boss / 0.75 at elite / 0.85 at magic / 0.95 at swarm: **over-power-at-floor confirmed** — kits exceed all per-tier targets even at minimum modifier; floor is the constraint
- If WR is low across all tiers at floor: **diagnosis is wrong**; different mechanism (energy-cycle failure? defense-collapse? something else); pivot the investigation

### § 3.2 — Mechanism (code archaeology)

**Question:** Confirm the floor mechanism and check whether B14.5 V1's MODIFIER_LOW_THRESHOLD=0.30 recompose-trigger should have fired (and either did/didn't, or is mis-conditioned).

**Method:**
1. Read `balance_loop.py` lines 767, 891, 1247, 1941. Confirm all four sites have `low, high = 0.05, 4.0` (or equivalent). Document whether the four sites are truly the same constant or have drifted.
2. Read the B14.5 V1 recompose-first architecture (lines 64-73 + relevant surrounding code). Document:
   - What conditions cause MODIFIER_LOW_THRESHOLD=0.30 to trigger a recompose attempt?
   - Does it check `status="failed"` OR only check modifier value?
   - For these three seasons' floor-locked classes: based on the validation_report.json eval_modifier values, would the recompose-first trigger have fired?
3. If recompose-trigger SHOULD have fired but DIDN'T: that's a bug in B14.5 V1, not just an unnamed constant.

### § 3.3 — Options (resolution menu)

Propose 1-3 concrete options. For each:
- Description (what changes; what code/constants are touched)
- Implementation cost (LOC; touched files; cross-seam impact)
- Simulation-runtime risk (does it widen search space? slow convergence? introduce divergence?)
- Semantic-shift surface (Discipline #12 — what assumption breaks? what gets re-measured?)
- Expected effect on the three seasons (would it have unstuck their floor-lock?)

Candidate options (gandalf seeded these; you may add/remove/refine):

- **Option A — Widen the floor.** Change `low=0.05` to `low=0.01` (or wherever target WR can be hit). Cheapest. Lets binary search reach the modifier those R8-inverted kits need. Risk: floors lower than 0.01 hide kit pathology.
- **Option B — Re-condition the recompose-trigger.** Make MODIFIER_LOW_THRESHOLD=0.30 ALSO fire when `status=failed AND eval_modifier ≤ low_threshold + epsilon`. Lets B14.5 V1 catch floor-lock cases and re-author kits with lower damage density. More design-aligned (recompose addresses kit-shape; floor-widening just lets bad kits converge).
- **Option C — Lower per-tier target WRs.** If kits are over-power-at-floor, the per-tier targets may be too high. Per-tier targets are in `r1_class_retune_sprint.py` (swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini_boss 0.20-0.50; boss 0.30-0.45). Lower these globally OR per-tier so target WR is achievable at floor=0.05 with R8-inverted kits.
- **Option D (combined)** — A + B sequenced. Widen the floor as a stop-gap (today); re-condition recompose-trigger as the design-correct fix (this week).
- **(open)** — anything you surface that the menu missed

### § 3.4 — Recommendation

Your preferred option + reasoning. Cite empirical evidence from § 3.1 + mechanism evidence from § 3.2.

---

## § 4 — Time-box + smoke-test mode

**1-2 days max.** Smoke-test mode per Discipline #2 — no full regen required. The 1-2 floor-locked-class spot-check is the smoke. Full regen + 5-season validation would happen ONLY after Matt approves an option for implementation.

---

## § 5 — Acceptance criteria

- [ ] Empirical spot-check completed: per-tier WR for 1-2 floor-locked classes at modifier=0.0509 reported
- [ ] Mechanism analysis completed: balance_loop.py floor sites + recompose-trigger conditions documented
- [ ] 1-3 resolution options proposed with cost/risk/semantic-shift for each
- [ ] Recommendation with reasoning + cited empirical/mechanism evidence
- [ ] Discipline #15 follow-on noted: `low=0.05` should be promoted to a named constant with docstring regardless of option chosen (gandalf § 9.8)
- [ ] AGENT_STATE.md updated
- [ ] Hive log STATE entry at completion with summary table (option × cost × risk × recommendation)
- [ ] Surface to knight-rider for: gandalf review + Trigger A Matt approval gate

**NO TAG until Matt approves an option for implementation.** Investigation output is documentation only.

---

## § 6 — Out of scope (HARD)

- **No implementation of any option.** Investigation-only.
- **No retry of seed 100003 or 100004.** Those dispatches are WITHDRAWN per § 9.7.
- **No path-a hand-redesign activation.** Path-a is in reserve.
- **No new tags fired** until Matt approves a resolution option.

---

## § 7 — Cross-seam impact (informational; surface, don't implement)

- **Rocket:** if Option B is chosen, recompose-trigger re-conditioning touches B14.5 V1 logic — generation seam may need to surface kit-shape signals. Not your work to wire; surface the boundary.
- **Star-lord:** if any option lands, telemetry should observe the new floor (or recompose count) post-implementation. Not your work to wire; surface.
- **Knight-rider + gandalf:** review your investigation output; route Matt approval.

---

## § 8 — Authority + Matt re-entry

**AUTONOMOUS L2-equivalent per VS2a hive § 4.5.** You can:
- Read code freely (no restrictions)
- Run smoke-test scripts that consume existing data (no regen; no LLM calls; no telemetry writes that affect production state)
- Author the investigation report at `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md`
- File STATE entries; surface to knight-rider for routing

**You CANNOT:**
- Change `balance_loop.py` or any production code
- Run a season regen
- Fire any tag
- Approve any option for implementation

**Matt re-entry trigger (Trigger A):** activates when your recommendation lands and knight-rider + gandalf concur. Knight-rider routes to Matt with a design summary (cost / risk / semantic-shift / expected effect). Matt approves or amends. No code change until that gate.

---

## § 9 — References

- `canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md` § 9 + § 10 (gandalf re-disposition)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (the four floor sites + B14.5 V1 recompose-first)
- Three validation_report.json files (60/73/80% floor-lock data points)
- `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (rocket's floor-pin observations)
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` (rocket retry-1 systemic finding)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#2 smoke-test, #11 attribution, #12 semantic shift, #15 implicit-pillar drift)

---

*Authored 2026-05-19 by knight-rider under VS2a hive pre-approval-batch § 4.5. The substrate prior was the wrong abstraction. The floor is. The investigation continues at the right layer. Matt re-enters at the implementation gate.*

---

## Completion record

**Completed:** 2026-05-19
**Author:** gamora
**Authority:** AUTONOMOUS L2-equivalent per § 4.5

### Acceptance criteria

- [x] Empirical spot-check completed: per-tier WR for 8 floor-locked classes from season_100002 at modifier=0.0509 reported. Over-power-at-floor confirmed (7/8 classes exceed tier ceilings on swarm/magic/elite; dispatch diagnostic criteria all met).
- [x] Mechanism analysis completed: all four `low=0.05` floor sites documented (lines 767, 891, 1247, 1941). Recompose trigger fires correctly but lever signal is 0.0 at floor — structural, not a B14.5 V1 bug.
- [x] Resolution options proposed: Options A (widen floor), B (re-condition recompose), C (lower targets — rejected), D (A+B combined) with cost/risk/semantic-shift per option.
- [x] Recommendation: Option D (A as immediate stop-gap; B as design-correct fix this week).
- [x] Discipline #18 follow-on: `low=0.05` implicit-pillar promotion noted regardless of option chosen.
- [x] AGENT_STATE.md updated.
- [x] Hive log STATE entry filed with summary table.
- [x] Surfaced to knight-rider for gandalf review + Trigger A Matt approval.

### Key output

Investigation doc: `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md`

No code changes. No tags. No season regens. Investigation only per dispatch § 6.
