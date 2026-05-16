# Dispatch — 2026-05-16 — star-lord — Catalogue mapping + grouping derivation experiment (LLM templates + execution)

**From:** knight-rider
**To:** star-lord (LLM call infrastructure ownership — `src/reincarnated/llm/`)
**Approved by:** Matt at 2026-05-16 Day 4 (explicit LLM-budget authorization per ADR-006; ~$5-15 expected spend)
**Status:** PENDING
**Estimated effort:** ~1-2 sessions (templates ~30-60 min; execution ~30 min including 2 experiments; output capture ~15 min)
**Acceptance:** Both experiments execute cleanly; per-candidate JSON outputs captured to a structured artifact at `agentic_orchestration/research/experiments/2026-05-16-catalogue-mapping-and-grouping/`; gandalf is notified for findings review; cost logged per LLM ledger discipline.

## Context — why this exists

Gandalf authored a detailed experiment request at `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`. The experiment empirically resolves two architectural opens in the form-bias-cadence-strategy work:

1. **The α/β/γ per-season-vocabulary-coupling question** — can per-season vocabulary be reliably mapped onto the catalogue's deliverable VFX tag space? Determines whether vocabulary is generated free-form (validation-and-regenerate), in-prompt-constrained, or runtime-fallback-mapped.
2. **The multiple-canonical-groupings architecture question** — can the catalogue's tag space support multiple valid opposition groupings, or does the genre constraint (player-cognition ~5-7) force a single fixed grouping?

Findings shape gandalf's strategy doc Q4 + the cipher-width decision (Options A/B/C from the canonical-elements thread).

**Matt authorized the LLM budget at Day-4 mid-session.** This dispatch unlocks execution.

## Scope

The experiment design is in gandalf's request file. **Read it in full before starting.** This dispatch covers your seam-side work:

### Step 1 — Build prompt templates

Per gandalf's specs in the request file:

**Experiment 1 — α/β/γ mapping test prompt template:**
- Input: vocabulary word + available element categories (current catalogue substrate = Pimen 9: fire/water/earth/wind/ice/holy/dark/thunder/acid)
- Output: JSON with `chosen_tag`, `confidence`, `reasoning`, `alternatives_considered`, `preservation_quality`
- Use the exact prompt structure in gandalf's request § "Per-candidate LLM call"

**Experiment 2 — multiple-groupings derivation prompt template:**
- (Spec is in gandalf's request file § Experiment 2. Read and replicate faithfully — do NOT re-invent the prompt design; gandalf authored it deliberately with the three white-wizard filters built into the scoring rubric.)

### Step 2 — Execute Experiment 1

Per gandalf's spec:
- ~15-20 vocabulary candidates (full list in gandalf's request § "Candidate vocabulary list")
- 4 runs per candidate at different seeds
- Capture structured JSON output per run
- Total LLM calls: ~60-80; expected cost ~$3-7

### Step 3 — Execute Experiment 2

Per gandalf's spec. Total LLM calls + cost per gandalf's estimates in the request.

### Step 4 — Capture outputs

Structured artifact directory at `agentic_orchestration/research/experiments/2026-05-16-catalogue-mapping-and-grouping/`:

- `experiment-1-mapping-test-raw.jsonl` — one line per LLM run with full output
- `experiment-2-groupings-derivation-raw.jsonl` — same shape for Experiment 2
- `experiment-run-log.md` — execution timestamp + seed list + cost per experiment + any anomalies during runs
- `templates/` subdirectory with the prompt templates used (for reproducibility)

**Do NOT score the outputs.** Scoring is gandalf's job per the request file. Your job is mechanical execution + capture.

### Step 5 — Cost logging + completion

- Log total LLM cost per your LLM-ledger discipline (current empirical baseline ~$0.85-1.00/season; this experiment is ~$5-15; small relative to a regen but worth tracking)
- Update your `export/AGENT_STATE.md` with the experiment execution + cost
- Notify knight-rider + gandalf at completion

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` **end-to-end** (the experiment design — your specification source)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + § "Catalogue-based form-bias resolution path" (architectural context)
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` (full dialogue background)
- `canonical/story/pre-llm-substrate-inventory.md` (gandalf's substrate inventory — see Cluster B for catalogue-track dependencies)
- `reincarnated-engine/src/reincarnated/llm/` your own seam — wherever the Anthropic SDK integration lives (your call on which existing helper to reuse vs new template)
- `reincarnated-engine/canonical/19-llm-call-map.md` (call-site discipline)

## Constraints (per ADR-006 + LLM-ledger discipline)

- **Budget authorized: ~$5-15.** If actual cost trends >2× expected, pause and report to knight-rider before continuing.
- **Retries: 3 max, exponential backoff** per LLM ledger discipline.
- **No fabrication.** If an LLM call fails after 3 retries, log the failure and continue with the next candidate. Don't synthesize fake JSON.
- **No prompt design changes** without checking with gandalf — gandalf authored the prompt deliberately with the three white-wizard filters built into the scoring rubric.

## Cross-seam considerations

- **Gandalf:** owns experiment design (already filed) + findings review (post-execution). Coordinate completion with gandalf so findings review can begin immediately.
- **No code changes to `src/reincarnated/llm/`** unless template-reuse requires a small additive helper. If you need a new helper, write it; doesn't trigger MIGRATION.md unless it changes existing call-site contracts.
- **No telemetry schema changes.** Experiment outputs go to the `research/experiments/` subtree, not to `data/telemetry.db`.

## Out of scope

- Scoring the experiment outputs (gandalf's job)
- Authoring the prompt templates from scratch (gandalf authored them; you replicate)
- Modifying gandalf's experiment design (if you see an issue, surface to knight-rider before changing)
- Running a third experiment or expanding the candidate vocabulary (gandalf scoped it)
- LLM cost work beyond logging this experiment's cost

## Acceptance criteria

- [ ] Both prompt templates built and saved
- [ ] Experiment 1 executed (all candidates × 4 runs)
- [ ] Experiment 2 executed
- [ ] Outputs captured to `research/experiments/2026-05-16-catalogue-mapping-and-grouping/`
- [ ] Run log written with execution timestamps, seed list, cost per experiment, anomalies
- [ ] LLM cost logged in your ledger
- [ ] `export/AGENT_STATE.md` updated
- [ ] Knight-rider AND gandalf notified at completion

---

## Completion record

**Completed:**
**Output artifacts:**
**Total LLM cost:**
**Anomalies during runs:**
**Notes for gandalf (for findings review):**
**Notes for knight-rider:**
