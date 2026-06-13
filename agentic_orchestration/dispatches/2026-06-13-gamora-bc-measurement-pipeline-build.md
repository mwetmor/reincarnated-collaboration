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

---

## Completion record (gamora, 2026-06-13 SESSION 4 — FULL-CORPUS BC-MEASUREMENT RUN)

**Status: COMPLETE. Run fired CLEAN over all 96 kits.** The corpus-shape blocker (Session 3) is resolved — rocket's simulatable sibling corpus drove `from_player_class → simulate_fight(measure_bc=True)` straight from disk, 96/96, 0 round-trip failures.

### Artifacts
- **MEASURED bins (star-lord consume shape):** `reincarnated-engine/src/reincarnated/simulation/output/bc_measured_bins.json` — 96 records, 96 unique `kit_id`s, `season_id=kse_20260613_002`, all validate against `ExportKitBCMeasuredBin` (Discipline #8 PASS 96/96).
- **Math note (Discipline #1, authored BEFORE the run):** `reincarnated-engine/src/reincarnated/simulation/math/bc-measurement-corpus-gauntlet-2026-06-13.md` — opponent-panel design + divergence framing + pre-registered expectations.
- **Run script:** `reincarnated-engine/scripts/gamora_bc_measurement_full_corpus_2026_06_13.py` — deterministic, $0, ~2.0s wall, 768 fights (8/kit, sequential per Discipline #3).

### Run parameters
- **Panel (math note § 1–2, EMPIRICALLY derived):** two boss-tier opponents per kit — `boss/brute/physical` (seed 1; avoidance surface + eHP denominator) + `boss/brute/fire` (seed 2; elemental eHP/output diversity). 4 fights each, seeds 300+i / 400+i.
- **Why boss-tier:** `standard`/`elite` opponents die to the kits' opening burst before landing a single attack → 0 incoming damage → eHP clamps to tank-ceiling for everyone → Axis-4 meaningless. Only a boss-tier opponent survives to exercise the defensive surface (16+ incoming attempts, real damage taken). This is the load-bearing panel decision.

### Per-kit MEASURED distribution
- **Axis-4 (defensive profile):** glass 94, mitigator 2, dodger 0, tank 0.
- **Axis-3B (amplitude variance):** spiky 81, variable 8, flat 7, deferred 0.

### MEASURED-vs-PREDICTED divergence (FK join — the load-bearing signal for rocket Items 7/8)
- **Axis-4 match: 23/96 (24%).** Confusion is near-total collapse to `glass`: tank→glass 24, mitigator→glass 24, dodger→glass 23, glass→glass 23.
- **Axis-3B match: 31/96 (32%).** Collapse toward `spiky`: flat→spiky 28, variable→spiky 27, spiky→spiky 26.
- **HEADLINE SUBSTRATE FINDING — Axis-4 ordering is INVERTED, not merely collapsed.** Mean measured eHP_ratio per PREDICTED bin: tank 0.982 < mitigator 1.029 < dodger 1.091 < **glass 1.202**. Rocket's intent is tank > glass (defensive_vitality_scale 1.8→0.55); the simulation produces glass > tank. The inversion is **panel-scale-INVARIANT** (the `hp/damage_taken` ratio ordering holds under any uniform damage scaling): predicted-glass kits have BOTH the highest raw HP (mean 17,329 vs tank's 14,985) AND the lowest damage taken (12,187 vs tank's 14,534). Root cause is substrate-intrinsic: rocket's `defensive_vitality_scale` intent label did not translate into differentiated — and in fact inverted — simulated defensive capability. `shield_buffer_est`/`regen_per_sec_est` are nonzero on only 24 kits each and at magnitudes that do not move the eHP ratio. **This is report-don't-force (Discipline #11): I did NOT re-tune the panel to manufacture the 24/24/24/24 target — that would be forcing.** The bin-collapse magnitude is partly panel-strength (a softer panel lifts all ratios), but the ORDERING INVERSION is the panel-invariant substrate signal Items 7/8 must consume.
- **No dodger reached** despite 24 `is_dodge_built` kits — measured avoidance maxes at ~0.27 (< 0.40 edge) against the physical panel. The dodge intent is not realized as ≥0.40 measured avoidance.

### Deferred-evaluation pool
- **EMPTY (all bins measured).** 0 Axis-3B deferred (hit-triple present on every fight), 0 deferred-dodger-candidates (avoidance measurable on every kit — the physical panel populates the `did_hit`-gated denominator), 0 records with `measurement_basis != "measured"`. The Session-2 deferred routing (dodger + Axis-3B) is fully resolved by the kernel emission + the survivable physical panel.

### Charge-stack + companion coverage (the previously-missing coverage) — CONFIRMED CLEAN
- **Charge-stack kits: 12/12 measured cleanly** (`s1010-rep-0000..0011`; FK `substrate_trace.charge_stack` is a nested dict carrying `predicted_axis5_bin` — 6 charge-stack + 6 generator-spender per report.json).
- **Companion kits: 6/6 measured cleanly** (player-kit corpus carries 6 `npc`/`monster`-tagged companions). NOTE: report.json lists `companion_records: 12` — the other 6 appear to be companion-OF relationship records not present as player kits in the simulatable corpus. Flagged for rocket/KR to confirm the 6-vs-12 split is expected (companion records ≠ companion player-kits).

### Seam property (flagged for handoff per rocket)
The kit-space emitter mints its own `kit_<primary>_NNNNNN` id and DROPS the source id. The MEASURED↔PREDICTED join is therefore NOT a shared `kit_id` — it runs `MEASURED(source_id) → corpus kit's kit_space_kit_id FK → data/kit_space/kits/<FK>.json substrate_trace`. Verified bijective (96 unique FKs, all resolve, all carry the provider tuple). **Future representative corpora MUST carry the `kit_space_kit_id` FK the same way** — do NOT key off the bare `substrate_trace` tuple (rocket found 3 collisions across 96).

### Discipline compliance
- #1 math-before-code: panel-design math note authored + committed before the run.
- #2 smoke→full: smoke-scale per kit (8 fights); milestone-validation full corpus.
- #3 sequential: no parallel fights, no parallel re-runs of the corpus.
- #4 right tool: fixed-panel driver, NOT the production KPM gauntlet (wrong tool for a defensive-profile measurement).
- #8 boundary validation: 96/96 against `ExportKitBCMeasuredBin`.
- #11 report-don't-force: divergence + ordering-inversion reported, not tuned away.
- #12 semantic clarity: avoidance over avoidable/physical surface (emission note § 2.2) carried forward; panel-relative eHP vs substrate-intrinsic ordering-inversion distinguished explicitly.

### For jack-ryan (Gate-2 folds into post-run acceptance, per Matt)
Gate `3136fd7` (pipeline build) + this run together. The pipeline is proven: brownfield invariant held (commit `3136fd7` md5 a2bc98b5 = clean HEAD), 96/96 schema-valid, deferred pool empty, deterministic re-run byte-stable. The divergence + ordering-inversion are FINDINGS (rocket Items 7/8 input), not pipeline defects. No locked-edge change, no telemetry-schema change, no new generation primitive.

**Auto-commit (gamora seam). NO push (Matt's keystone-close gate).** This run feeds rocket Items 7/8 → gandalf Gate 1; MEASURED bins are load-bearing.
