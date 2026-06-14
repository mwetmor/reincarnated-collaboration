# Run A / Run B — launch prompts (parallel autonomous batch)

**Type:** session-launch prompts for the two parallel autonomous runs.
**Date:** 2026-06-13
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-13.
**Composition:** mechanism + topology in `agentic_orchestration/gandalf/notes/2026-06-13-autonomous-run-mechanism-spec.md`; density contract in `...-density-design-contract-4C-4D-proxy-port.md`.

---

## Who leads — NOT KR

The runs are **build** runs, and KR does not write code. So each run is **specialist-led**, not KR-led:
- **Run A → `claude --agent gamora`** (simulation seam)
- **Run B → `claude --agent rocket`** (generation + foundation seam)

KR's orchestration is **already done** (dispatches authored, topology set, oracle amended). KR is **not** a running session during the runs; KR **re-engages at the close** to drive the critique-pair Gate (jack-ryan Gate-2 + gandalf design + Matt ratify). Firing a KR session to "watch" the specialists would re-introduce the retired wake-up-loop / orchestrator-poll anti-pattern.

## Launch (two terminals, same engine clone)

```bash
# Terminal 1 — Run A
cd ~/Games/reincarnated-engine && claude --agent gamora

# Terminal 2 — Run B
cd ~/Games/reincarnated-engine && claude --agent rocket
```

**Git isolation:** both sessions are in the same `~/Games/reincarnated-engine` clone on `main`, but they write **disjoint file sets** (gamora = `simulation/`, `spirit_guide/`; rocket = `generation/`, `element/`, `anchor/`, `foundation/`). With add-by-name staging discipline (never `git add -A`), there is **no content collision** — only git-index timing, which git serializes. Same-tree is fine. Worktree isolation (`git worktree add` per session) is optional belt-and-suspenders if you prefer.

---

## Prompt A — paste into the gamora session

```
Session-start per your OP (§1). You are executing autonomous Run A (gamora/simulation seam) of a parallel batch — mechanism + topology in agentic_orchestration/gandalf/notes/2026-06-13-autonomous-run-mechanism-spec.md. Three units; checkpoint-commit after each:

1. W-E throughput MEASURE — build the throughput axis per the cert oracle canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md and the W-D close agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md. This is the wave critical path.
2. Displacement-histogram emit — emit the per-kit spatial displacement HISTOGRAM (distribution, not mean) from the W-D run per agentic_orchestration/gandalf/notes/2026-06-13-mobility-lock-edge-recalibration-PENDING.md. Capture on the CURRENT movement AI — do NOT touch movement-AI rework (that is D4, a later batch; running it here invalidates the histogram). This unblocks gandalf's lock-edge re-cal.
3. Your 2 W-D Gate-2 doc-lines — the math-note "§8 was stricter than the oracle" reconciliation line + the JSON measure_cond4_pass:true annotation beside prereg_pass:false/ablation_pass:false, per W-D close D1, clearing the Gate-2 WARN->PASS.

Mechanism: auto-commit each unit as you finish it (incremental checkpoint); do NOT push (Matt gates push); do NOT cross any Gate-2 or 1D-delete boundary — the W-E close returns to the critique pair. If a unit blocks, checkpoint what is done, surface the blocker, and continue to the next independent unit. Signal done when the three units are checkpointed.
```

## Prompt B — paste into the rocket session

```
Session-start per your OP (§1). You are executing autonomous Run B (rocket/generation+foundation seam) of a parallel batch — mechanism + topology in agentic_orchestration/gandalf/notes/2026-06-13-autonomous-run-mechanism-spec.md. Two units; checkpoint-commit after each. Do D6 FIRST (it greens the test collection D5 needs to validate against):

1. D6 grouping-vocab loader fix — execute agentic_orchestration/dispatches/2026-06-13-rocket-grouping-vocab-loader-fix.md. Root cause is in your seam: foundation/grouping_vocabulary_loader.py cannot find the doc moved to canonical/story/historical/ in 93b8427 -> 9 test modules fail at collection. Fix the loader path (or fallback to historical/). Confirm the 9 modules collect green.
2. D5 reference-kit coverage — execute agentic_orchestration/dispatches/2026-06-13-rocket-reference-kit-coverage.md (resource/CC-differentiated reference kit; the instrument for Axis-5 resource-economy + Control discrimination). Arity STAYS 8 — no 7th kit unless/until Bucket-B promotes proxy-density.

Mechanism: auto-commit each unit (incremental checkpoint); do NOT push (Matt gates); do NOT cross Gate-2 — closes return to the critique pair. Validate D5's kit against the now-green test collection. If a unit blocks, checkpoint, surface, continue. Signal done when both units are checkpointed.
```

---

**Signed:** gandalf, 2026-06-13
**For:** the two paste-ready launch prompts (Run A = gamora, Run B = rocket — specialist-led, not KR-led) + launch commands + git-isolation note, for the parallel autonomous batch. D4/proxy-port held for a later batch.
