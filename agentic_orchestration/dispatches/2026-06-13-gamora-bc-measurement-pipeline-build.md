# Dispatch — 2026-06-13 — gamora — BC-measurement pipeline build (keystone middle link)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-13 — the BC-measurement build is a COST DISCOVERY inside the already-authorized "BC-measurement keystone," NOT a scope amendment. KR fires; Matt's only gate in the whole sequence is the eventual push-to-remote.
**Status:** **GATE-1 PASS-WITH-INFO (jack-ryan, 2026-06-13) — FIRED.** Two INFO items folded into the math-note section below (confirm live bin counts; pre-register smoke expected-cells); both are math-note refinements gamora absorbs at execution, not dispatch rewrites. No BLOCK. Cleared to execute.
**Estimated effort:** ~1–2 days (gamora's own read, 2026-06-13 confirmation pass)
**Acceptance:** A runnable pipeline that consumes a generated kit corpus, runs it through the gauntlet sim, reduces per-fight telemetry to per-kit MEASURED Axis 4 (defensive profile, 4 bins) and Axis 3B (damage amplitude variance, 3 bins) scalars, and assigns each kit a bin against the LOCKED edges. Emits a per-kit MEASURED-bin record in a format star-lord's exports can consume. Smoke-validated on a small corpus subset before any full run.

## Context

This is the load-bearing middle link of the BC-measurement keystone (rocket generation → gamora simulation → **BC measurement** → rocket measurement-time items). KR's ground-truth pass 2026-06-13 (confirmed by you) established that this pipeline **does not exist** — the `bc_target_*` modules in `generation/` are TARGET-composition (rocket's seam), not measurement. The dispatch `2026-06-12-rocket-generation-handoff.md` (line 15, line 56) wrote "MEASURED BC bins come from the BC pipeline downstream of simulation" as if it existed; it does not. Building it is the corrected next move.

Three downstream consumers are HELD on your MEASURED bins:
- rocket Item 7 (`investment_profile`) — reads MEASURED Axis 4 / Axis 3B (rocket dispatch § 7)
- rocket Item 8 (vestigial-label reachability report) — § 2.3 rules read MEASURED BC bins (rocket dispatch § 8)
- gandalf's vestigial-label reachability gate + investment-profile assignment

**Sequencing call (KR, this session):** this BC-build goes BEFORE your other long pole (the T4-mechanic implementation — 4 new strategies + Q1/Q4/Q5 locks + Q6/Q7 convergence/bridge). Rationale: shorter pole, unblocks the reachability + cognitive-load gates, and validates the measurement plumbing before the heavier T4 block lands on your seam. T4-mechanic is the NEXT gamora dispatch, not this one.

## Required reading before starting

- This dispatch's anchor: `agentic_orchestration/dispatches/2026-06-12-rocket-generation-handoff.md` §§ 7–8, lines 15, 56, 90, 94, 172 (held-criteria)
- **Locked measurement methodology:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — §§ 3.6 (Axis 3B), 3.7 (Axis 4); plus lines 104, 133, 453–545 (damage-weighted argmax; avoidance_rate; eHP_effective; deferred-evaluation pool + telemetry-signal gaps). **This doc is the methodology anchor — the math note ANCHORS to it, it does not re-derive bins from scratch.**
- Your own confirmation findings 2026-06-13 (BC pipeline = build task; Season 001010 = fresh-generate target; live-wiring follow-ons gated on same run)
- `src/reincarnated/simulation/MIGRATION.md` (existing `damage_received` / Axis-4 raw event; the upstream signal you measure FROM)

## Math-before-code (Discipline #1 — REQUIRED before any code)

Author a math note in `simulation/math/` specifying the **effect-budget weighting formula** — this is the load-bearing unknown you flagged. It must:
1. Anchor explicitly to lock §§ 3.6 / 3.7 (cite the bin edges; do not redefine them — edges are LOCKED, 68,040 cells).
2. Define the per-fight → per-kit aggregation: how raw telemetry events (damage dealt/received, avoidance, mitigation, regen) reduce to per-kit Axis 4 and Axis 3B scalars, weighted by effect budget.
3. **Telemetry-signal availability audit (load-bearing):** lock doc lines 511–545 flag that some signals may not be cleanly measurable by the current sim — per-hit damage-application logs, HoT-recovery-distinct-from-mitigation, avoidance tags. Confirm which signals the current telemetry already emits vs. which require new emission. **Any missing signal → star-lord MIGRATION (see cross-seam below).** Bins that cannot be cleanly measured route to the lock doc's deferred-evaluation pool — that is substrate evidence, not a build failure; report, do not force.
4. Bin-assignment procedure against the locked edges.

**Gate-1 INFO items (jack-ryan, fold into the math note):**
- **(i) Confirm live bin counts against the lock, do not inherit this dispatch's numbers.** This dispatch states Axis 4 = 4 bins / Axis 3B = 3 bins (from lock §§ 3.7/3.6) — confirm those counts against the live lock doc + substrate-vector cheatsheet in the math note before building the bin-assignment procedure. If a dispatch number is stale, the bin-assignment inherits the error. One-line confirmation step.
- **(ii) Pre-register smoke expected-cells (Discipline #2 strengthening).** For the glass-cannon + tank smoke fixtures, WRITE the expected Axis-4 / Axis-3B landing cells in the math note BEFORE running — a pre-registered prediction, not an after-the-fact assertion. Smoke PASS = the fixtures land in the pre-registered cells.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**YES.** Two boundaries:
- **gamora → star-lord (emit):** the per-kit MEASURED-bin record is a new export-consumable structure. Write the emit-side `MIGRATION.md` section documenting the record shape. star-lord authors the consume-side MIGRATION once your emit schema lands (star-lord seam work, auto-commit-eligible — telemetry is internal-to-engine, not an external-system write). KR has flagged star-lord; they pick up consume-side after your schema is defined.
- **telemetry-read (possible):** if the signal audit (math note step 3) finds missing raw signals, that emission is a star-lord telemetry MIGRATION — flag it to KR with the exact field list and gamora proceeds on available signals, routing the un-measurable bins to deferred-evaluation pool.

## Smoke-test expectation (Discipline #2)

Smoke on a small corpus subset (a handful of kits with known/expected profiles — e.g., a glass-cannon and a tank archetype) before any full corpus run. Verify bin assignment lands in the expected Axis 4 / 3B cells. No parallel full runs of the same corpus; tag intermediate states.

## Out of scope (do NOT touch)

- T4-mechanic implementation (the other long pole — NEXT dispatch, not this one)
- The rocket generation RUN (rocket's seam — produces the corpus this consumes)
- The weapon/substrate BC clustering / duplicate-detection line (Cycle 14/15 — DIFFERENT work; do not conflate)
- Changing the locked BC axis edges or vocabulary (lock doc wins; flag conflicts to gandalf)
- Generation-side `bc_target_*` modules (rocket's seam)

## Tag intent

`gamora/v-bc-measure-pipeline-<n>` (seam-prefixed intermediate). No milestone tag without Matt approval. Push-to-remote is Matt's gate — accumulate commits; KR coordinates the push at keystone-close.

## Gate-2

jack-ryan gates the implementation commits per seam protocol after the pipeline + smoke land.

---

**Author:** knight-rider, 2026-06-13. Anchors: rocket-generation-handoff dispatch §§ 7–8; qd-engine-bc-axes-lock §§ 3.6/3.7 + deferred-pool note; gamora 2026-06-13 confirmation findings.
