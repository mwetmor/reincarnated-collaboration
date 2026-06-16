# Finding — 2026-06-16 — M1.3.5 reduced-spatial search substrate (Gate-2 close)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-WARN (verdict: PASS — WARN doc-lines clear under my ADR-002 doc-only authority; no BLOCK)
**Target:** tag `gamora/v1.0-m1-3-5-reduced-substrate` (→ `457026e`); chain `b7014a2` → `7d2c263` → `457026e` → `1a4c6ae`, all on `main`, NOT pushed
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log/contract as truth), #5 (severity); Disciplines #1, #2/#2.1, #11, #12; design contract §4/§5/§6

## What I found

The build is sound and earns PASS. I verified the four load-bearing claims independently rather than trusting the close summary.

**1. Math-before-code (Discipline #1) — CLEAN.** `b7014a2` (03:24) contains ONLY the 176-line math note (no code in the diff). The pre-registration in §4 — drift metric, PASS criterion `drift_1D > drift_reduced AND drift_reduced ≤ DRIFT_HOLD_FLOOR=0.0`, and the §4.5 negative-control-validity gate (1D MUST drift or the control is dead) — was ALL present in that first commit. §8 was an explicit placeholder ("filled after Steps 1+2 execute"); the result table and the hp=7500 fixture value were added only in the LAST commit `1a4c6ae`. The criterion was NOT back-fit to the result. Commit timestamps are strictly chronological (math 03:24 → ablation 03:38 → build 03:41 → close 03:43).

**2. Ablation validity (the decisive proof) — VALID, scrutinized hardest.** Three things had to hold and all do:
- *Negative control genuinely drifts.* The 1D arm (`_eval_1d_wr` → `run_batch` vs a single mob) reads delta(ST−AOE)=0.0, both geometries WR=1.0 → `aoe_defended=false` → drift=1.0. This is faithful, not rigged: 1D is structurally single-target and cannot represent a pack, so feeding it one mob is what 1D *is*. The poison reproduces because 1D cannot see pack-clear value. Control valid.
- *Treatment fed REAL geometry, not the degraded path.* The reduced arm (`_eval_reduced_wr`) calls `_inject_spatial_geometry` (harness L77/264) to translate the rich `geometry` field into the `spatial_geometry_type` the engine reads (`spatial_engine.py:311`). The ablation therefore did NOT run on the F1 keyword-heuristic fallback — the substrate arm read true geometry directly. The "holds AOE" result (WR(AOE)=1.0, WR(ST)=0.0, delta=−1.00, drift=0.0) is a true capability proof.
- *Fixture is a fair mid-band, not cherry-picked.* hp=7500/mod=0.4 sits in the intended WR-cliff regime where AOE clears 8 mobs and single-target cannot. The 1.0-vs-0.0 split is extreme but is the designed regime, not a degenerate artifact — single-target genuinely failing to clear a swarm is the expected physics. (See WARN-2 on the supporting evidence.)
- *Methodological note (in gamora's favor):* drift is NOT measured from a live recompose run — it is a DETERMINISTIC controlled-swap proxy that isolates the exact geometry_mix accept/reject decision (`delta < -RECOMPOSE_DELTA_FLOOR`). This is more decisive than a noisy single live run, and gamora correctly demotes the live-loop witness (F3, 0 swaps accepted in EITHER arm) to inconclusive corroboration — exactly as §4.5 pre-registered. Honest framing; no overclaim.

**3. Additivity (Discipline #12) — CONFIRMED byte-identical.** `457026e` touches only the new module, the new ON==OFF smoke, and an additive `__init__` export. It touches NO live path: no `balance_loop`, no `_evaluate_class`, no `_run_spatial_slot`, no `search_estimator`, no `spatial_engine` production read, no telemetry schema. Default-construct raises on `evaluate()` (`enabled=False` default). The locked `REDUCED_SUBSTRATE_TICK_SIZE=0.2` is a new constant distinct from the legacy `REDUCED_TICK_SIZE=0.5` (untouched). ON==OFF smoke 5/5 PASS, including `commit_grade_deterministic`, `balance_loop_non_adoption`, and locked-tick distinctness. 1D NOT deleted. No production default changed.

**4. F1 (field-mapping) — correctly characterized as a downstream-adoption precondition, NOT a blocker for this close.** Confirmed independently: `spatial_engine.py:311/316` reads `spatial_geometry_type`/`geometry_type`; a production `model_dump()` emits rich `geometry` and leaves both None → falls to the geometry-blind keyword heuristic (path 3). This is a real, PRE-EXISTING gap in the spatial-repoint adapter, not introduced by M1.3.5. Crucially (per finding 2), the ablation bypassed it by injecting real geometry, so the PASS is NOT hollow — the proof is "the substrate CAN defend AOE given real geometry." F1 is a hard W-F-*adoption* precondition (the adapter must thread real geometry into a field the engine reads, or adoption inherits the blindness), but it is out of scope for proving + staging the substrate. gamora did not patch it (correct — patching would be a Discipline #12 production semantic shift) and surfaced it cleanly. It does not block this close.

## Rationale

The build does exactly what the design contract §0/§5/§6 demanded and nothing more: it PROVES directional honesty via the §5(D) with/without ablation, LOCKS the Pareto config at the cheapest honest corner (tick=0.2, full packs), CLEARS the §6 cost target (~10.8× under commit-grade-2D), and STAGES the substrate flag-gated/OFF — adopting nothing. Every claimed gate (math-before-code, smoke-before-full, additivity, negative-control validity) was verified against the artifacts, not taken on report. Per REVIEW_PROCESS #5, the residual items below are doc-quality, not principle violations, so they are WARN/INFO and clear under my ADR-002 documentation-only authority; the build closes PASS.

## Action

- [x] jack-ryan: APPROVE close PASS (within ADR-002 — this is a within-seam build proven additive; doc-only WARNs cleared by me).
- [ ] gamora (WARN-1, doc-only): fix the stale fixture comment in `scripts/gamora_m1_3_5_substrate_build_2026_06_16.py` L213-220 — the prose says `hp=2500/dmg=80` then `hp=7500`; the executed constant is `_FIXTURE_SWARM_HP=7500.0` (JSON confirms `swarm_hp: 7500.0`). Stale comment only, no logic impact. Tidy at next touch; not gating.
- [ ] gamora (WARN-2, doc-only): the "robust band" claim (hp 6000–9000 × mod 0.3–0.5 all show the signature, §8.2 + harness L219) is asserted in prose but only the single locked cell is preserved in the committed JSON. The deterministic 1.0/0.0 split is defensible as the designed WR-cliff regime, but if the band-probe sweep was actually run, drop its output alongside `m1-3-5-substrate-build-2026-06-16.json` so the "mid-band, not knife-edge" claim is auditable rather than asserted. INFO-grade if the sweep was a reasoning estimate; WARN-grade if it was run and discarded.
- [ ] gandalf / Matt (NOT this gate — downstream W-F): F1 adapter fix is a hard precondition of ADOPTION. When W-F switches the recompose evaluator to this substrate, the adapter MUST thread real `geometry` into a field `_determine_geometry_type` reads (path 1 or 2), or the substrate inherits the keyword-heuristic blindness and the whole milestone is defeated. Tracked here as a separate gated step; does not block M1.3.5 close.

## References

- Math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/m1-3-5-reduced-substrate-build-2026-06-16.md`
- Substrate: `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/reduced_spatial_substrate.py`
- Ablation harness: `~/Games/reincarnated-engine/scripts/gamora_m1_3_5_substrate_build_2026_06_16.py` (L77 `_inject_spatial_geometry`, L247 `_eval_1d_wr`, L260 `_eval_reduced_wr`, L288 `_run_arm`)
- ON==OFF smoke: `~/Games/reincarnated-engine/scripts/gamora_m1_3_5_substrate_on_off_smoke_2026_06_16.py`; output `output/m1-3-5-substrate-on-off-smoke-2026-06-16.json`
- Ablation output: `~/Games/reincarnated-engine/output/m1-3-5-substrate-build-2026-06-16.json`
- F1 site: `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:280-334`
- Design contract: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md`
