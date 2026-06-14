# Finding — 2026-06-14 — gamora-we-throughput-proof-gate2

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** WARN (clears to PASS on two doc-line annotations — both within jack-ryan ADR-002 doc-only approve authority; neither gates the W-E close)
**Target:** commit `02e2a6f` (gamora W-E throughput proof)
**Developer:** gamora

---

**Provenance (scribe note — gandalf):** this finding was authored by the **jack-ryan DEV-MODE sub-agent** (agentId `ab86be35f2f8a7f77`), invoked by gandalf on 2026-06-14 as the Gate-2 half of the W-E close critique pair, with a conclusion-free brief (the sub-agent was not told gandalf's verdict, preserving two-witness independence). The sub-agent ran **read-only** and could not write to disk; this file is gandalf's **faithful verbatim transcription** of jack-ryan's returned verdict, captured for the durable close-record KR consumes. The text below — from "Pre-finding verification note" through "References" — is jack-ryan's, unedited. It composes with the gandalf design-half (`agentic_orchestration/gandalf/notes/2026-06-14-we-close-design-endorse-and-wf-search-substrate-precondition.md`) and Matt's ratification (2026-06-14, "Do all three").

---

## Pre-finding verification note (jack-ryan)

Now the picture is complete and the push question resolves benignly. `02e2a6f` (the W-E build) IS on the remote — but it was pushed by Matt as part of a later batch (HEAD/remote tip is `7fd8792`, dated 00:51, authored by mwetmor, carrying rocket D5 work that post-dates the W-E build). The W-E build did NOT self-push; subsequent commits (gamora aef031f/bec1561/258d038, rocket d583f64/7fd8792) accumulated and the whole run was pushed together at the close. The push is Matt-gated as the W-D-close doc required — not a scope violation by the build under review. This is consistent with autonomous-run discipline: the build committed, the push happened later under authorization.

I have everything. Rendering the Gate-2 verdict.

---

## Gate-2 Finding — W-E throughput proof (commit `02e2a6f`, gamora)

**Reviewer:** jack-ryan · **Severity: WARN** (clears to PASS on two doc-line annotations) · **Target:** `02e2a6f` · **Developer:** gamora
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log/oracle as truth), #5 (severity). **Disciplines:** #1, #1.1, #2/#2.1, #3, #11, #12.

### What I found
The BUILD is **sound and the headline numbers reproduce exactly** from the JSON — I re-derived every one independently: unit wall-clock Σ(room×9) = 0.341 s; 1,836 fights / 11.6 s at 34 survivors; 1.77% of the 104k flag; 340/6.315 = 53.8× ≈ "~54×." Config is genuinely commit-grade for the *fight* (`fight_events_sample_rate=1.0`, events emitted + counted, JIT warm-up discarded). Pre-registration is real — the math note authored the acceptance criterion (A: hard fight-count; B: tolerable wall-clock), the per-room projection model, AND the FAIL/negative-surface clause **before** the run (#2, #11 satisfied, not papered). Scope is clean: only harness + output + math-note touched, **zero engine-behavior files** (#12 holds), no tag, did not cross W-F. The push is Matt-gated — `02e2a6f` reached the remote only inside a later batch (tip `7fd8792`, authored by Matt), not self-pushed.

### Two WARNs (neither blocks the W-E close)

**WARN-1 — "boss-weighted s/fight = 6.31 ms" is mislabeled.** The figure is the *flat arithmetic mean* of the 6 per-room ms/fight values (identical to 4 decimals: `sum/6 = 6.315`). It is NOT boss-weighted. The boss tail IS correctly counted at full weight in the *unit cost* (0.341 s) and the *batch* — the numbers that actually gate — because those sum per-room wall-clock. Only the per-fight headline reduces to a plain average. The gate is unaffected; the label overstates. **Rationale:** Discipline #11 (diagnose, don't average the tail away) — the note *claims* this discipline for the per-fight number while the number is in fact the averaged form.

**WARN-2 — measurement gap: the proof times the fight, not the identity-mint.** A commit-grade unit is "one `CommitGradeVerdict`," but the harness times `run_spatial_fight` only. The 8-axis reduction that actually mints the verdict (`spatial_bc_measurement.measure_kit_spatial` → 8 `measure_axisN` passes over the ~1,200–4,500 emitted events/cell, then `mint_commit_grade_verdict`) is **never in the timed path**. The post-1D-delete architecture pays sim **+** reduction per survivor; the proof bounds only the sim half. Likely small, but unmeasured — so the bound is a lower bound on the true commit-grade cost, not the whole cost. **Rationale:** REVIEW_PROCESS #4 — the oracle/wave define commit-grade as mint-of-identity (oracle §6.2 cond.4); a throughput proof of "commit-grade batch" should time what mints.

### Action
- [ ] Developer (gamora): add one annotation line in the math note + JSON renaming `boss_weighted_ms_per_fight` to `flat_mean_ms_per_fight` (or note "= unweighted per-room mean; the boss weighting lives in the unit/batch sums"). Clears WARN-1. Within my ADR-002 doc-only approve authority.
- [ ] Developer (gamora): add one math-note line scoping the proof as **fight-execution cost only**, noting the 8-axis reduction is unmeasured and asserting (or deferring to W-F) that it is sub-dominant. Clears WARN-2. The 11 s figure has ~440× headroom to the 5-hr reference, so the gate verdict is robust even if reduction doubles per-unit cost.
- [ ] Matt: no decision needed for the close; WARN→PASS is doc-only. The "BOUNDED + TOLERABLE" disposition stands.

### Verdict
**WARN, converging to PASS.** The throughput question is answered correctly at the gating level (A + B both genuinely PASS; the affordability claim is sound with large headroom). Both WARNs are honesty/completeness refinements on the *characterization*, not errors in the *result*. This banks the §4.3 #2 datum for the W-F 1D-delete decision. Consistent with my role on the critique pair — I'd endorse the W-E close once the two doc-lines land; they fall inside my approve authority, so no Matt ratify is required for the WARN-clear itself.

### References
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/we-throughput-proof-2026-06-13.md` (math note; §1 per-room model, §6.1 headline)
- `~/Games/reincarnated-engine/output/we-throughput-proof-2026-06-13.json` (`commit_grade_unit.boss_weighted_ms_per_fight` = 6.315; `batch_projections`)
- `~/Games/reincarnated-engine/scripts/gamora_we_throughput_proof_2026_06_13.py` (`time_room` L131–149 — times `run_spatial_fight`; no reduction call)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_bc_measurement.py` L376–421 (`measure_kit_spatial` + `mint_commit_grade_verdict` — the untimed reduction)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` L381 (104k flag), L1388 (the `*0.34` 1D-basis the comparison rests on — verified per-fight, correct comparator)
- `~/Games/reincarnated-collaboration/canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` §5 (W-E exit gate), §4.3 #2
- `~/Games/reincarnated-collaboration/agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` L69 (push Matt-gated — confirms `02e2a6f` was not self-pushed)

---

## gandalf close-note (scribe, non-jack-ryan)

**Disposition at capture (2026-06-14):** Matt **ratified the W-E close** via "Do all three" (2026-06-14). The critique pair converged: jack-ryan Gate-2 = WARN→PASS (above, doc-only) + gandalf design = ENDORSE. The two WARNs route to **gamora** as the two W-E doc-lines (async; should land before W-F cites the §4.3 #2 datum; within jack-ryan's doc-only authority — no Matt ratify needed for the WARN-clear). The **W-F search-substrate precondition** the gandalf half surfaced (the reduced-spatial inner-loop substrate is unbuilt; the 1D-delete strands the recompose loop) is now the named milestone **M1.3.5** with its discrimination-floor acceptance spec authored (`agentic_orchestration/gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md`); routed to **KR** to sequence into a batch **before W-F**.
