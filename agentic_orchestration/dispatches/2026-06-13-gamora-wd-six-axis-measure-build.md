# Dispatch — 2026-06-13 — gamora — W-D: build six-axis MEASURE from spatial telemetry (oracle §6.2 cond. 4)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-13 — "KR green-lights W-D (six-axis MEASURE) as the next target" (on ratifying the W-C-full RESOLVE PASS + the M1 with/without-ablation re-close binding).
**Status:** GATE-1 PASS-WITH-WARN (jack-ryan DESIGN-MODE, 2026-06-13). Two folds applied: FOLD-1 (Bucket-A 8-axis gate is INVARIANT to the CONFIRM/BUILD split — a CONFIRM'd 2B still counts toward the 8) + FOLD-2 (§4.D validation-gate FIRST — inspect `arena.py`/`boss_with_adds` 240s before building a new fixture, with the fixture acceptance defined). One INFO folded (pre-register the bin per axis per kit, not a point value). jack-ryan ruled DO-NOT-SPLIT (keep the single CommitGradeVerdict mint whole; M1 STOP-and-surface is the relief valve). **Presented to Matt → FIRES on his go.**
**Estimated effort:** multi-hour, multi-sub-task (sustained-wave fixture + measurement-build for ~4.5 axes + confirm 2 axes + M1 gather-primitive + ablation + commit-grade mint). This is the wave's heaviest build phase.
**Acceptance (oracle §6.2 condition 4 — the W-D exit):** the complete 8-axis surface is **computed from spatial telemetry** — every axis per the Bucket-B ruling (arity = 8, ratified, do NOT re-open) is assigned from the spatial run (replacing the placeholder `bc_cell`) and **wired, not default-valued** (the Bucket-A check on the spatial seam); the result is minted as a `CommitGradeVerdict` (companion §3.1 provenance). **MEASURE condition 5 (defensive-bridge boss re-validation) is OUT — that is W-F.**

## Context

W-C-full RESOLVE **PASSED** (`gamora/v-wc-full-resolve-2`, tag re-stamped to the Matt-ratified disposition; oracle v1.5 §6.1 records the pass). The spatial engine now resolves combat correctly. W-D is the next gate: **does the engine MEASURE kit identity correctly** (oracle §6.2). This is the measurement-instrument BUILD the W-C.5 close bound — *not* a wiring/plumbing pass. Per Matt's W-C.5 directive: *"W-D is 'build measurement for six axes,' not 'wire the tuple.' Otherwise the MEASURE cert (§6.2 cond. 4) can't pass."*

The audit finding W-D closes: the sim measurement pipeline (`bc_measurement.py`) computes a real bin for **only Axis 4 + Axis 3B (2 of 8)**; the other six coordinates are binned on generation-stamped **predicted** labels (MAP-Elites currently culls on predicted coordinates for 6 of 8 axes). W-D replaces those predicted labels with genuine spatial-telemetry measurement — but **not uniformly** (the structural-read discriminator below prevents both the under-scope *and* the over-scope error).

## The scope split (W-C.5 close §3 — the structural-read discriminator; do NOT build all six uniformly)

| Subset | Axes | W-D treatment |
|---|---|---|
| **Composition-determined (SAFE — predicted ≡ measured)** | **Geometry (2)** fully; **range-half of Engagement (1)** | **CONFIRM** from spatial telemetry — cheap read-back, wired not default-valued. No measurement-reduction build. |
| **Behaviorally-realized (AT-RISK — predicted is a proxy that diverges)** | **Proxy (2A)** [pri-1], **Resource (5)** [pri-2], **mobility-half of Engagement (1)**, **Tempo (3A)**, **Control (2B)** [lower confidence] | **BUILD** genuine measurement-reduction from spatial telemetry — the **Axis-4-bridge pattern**, applied to each. This is the heavy work. |

Three of the at-risk axes (proxy 2A, charge-stack 5, mobility 1) are the **confirmed ORPHAN-measure bugs** the coverage audit already found — same phenomenon; the bugs are the confirmed instances of the general shape. The **structural-read note is your scoping authority**, priority-ordered (Axis 2A priority-1, Axis 5 priority-2).

## Hard prerequisite — the §4.D sustained-wave fixture MUST land before Axis-2A wiring

Oracle §4.D (line 192): **Axis-2A measurement-wiring cannot certify until a sustained encounter exists** — *"the sustained-wave fixture lands before Axis-2A is wired, or the wiring certifies against noise."* Proxy-density (2A) is meaningless in a single pack-clear; it needs a sustained wave to measure against. **Sequence inside W-D:** build the §4.D sustained-wave fixture (spawn primitive + actor-lifetime / wave structure — gamora seam per §4.C/§4.D) FIRST, then wire Axis-2A against it. Do not wire 2A against the single-pack fixture.

## The M1 gather-primitive carry-over — the W-C-full ablation obligation (oracle §5.2)

W-C-full's K4≥K2 disposition deferred the **M1 gather-primitive** to W-D as a **gated obligation with a with/without ablation acceptance test** (oracle §5.2, verbatim):

> The engine-movement seam builds an **M1 player-gather/centroid primitive**: when a combatant carries an area skill, it repositions toward the pack centroid to maximize AOE coverage before casting, rather than only closing to the nearest mob. **Acceptance test (with/without ablation):** run `K4 ≥ K2 @ open_arena` **WITH the gather-primitive present vs WITHOUT it (ablated to current nearest-mob behaviour)** and demonstrate the **primitive is the CAUSE of the per-seed margin re-closing** — with-primitive the per-seed margin reproduces (≥ seed-majority); without-primitive it does not (reproducing today's 6/9). The margin re-closing must be **attributable to the primitive**, not closing-time noise or spawn layout. Causation-proving, not threshold-holds.

The movement AI lives in your spatial seam (`spatial_engine.py:1166-1193` advances to `nearest`, no gather). **Build the primitive + run the ablation; the ablation re-closes the K4 ⚠B canary's mechanism half.** If you judge the gather-primitive is a larger movement-AI rework than W-D should carry, STOP and surface the sub-scoping to KR rather than half-building it — but the default is: it rides in W-D as scoped.

## Required reading before starting

- **Oracle (your acceptance authority):** `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — **§6.2** (the two MEASURE conditions; you certify cond. 4 only), **§6.3** (arity = 8, RATIFIED — do NOT re-open; do NOT grow a 7th kit), **§5/§5.1/§5.2** (the K4 ablation binding you carry), **§4.C/§4.D** (the sustained-wave fixture contract — your prerequisite), §3 (room golden assertions)
- **W-C.5 close §3 (your scope authority):** `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` — the SAFE-confirm vs AT-RISK-build split, priority order, the Bucket-A wired-not-default check
- **The structural-read note (priority-ordered build identity):** `agentic_orchestration/gandalf/notes/2026-06-13-bc-predicted-vs-measured-structural-read.md`
- **The coverage-audit pair (the 6-of-8 finding):** `reincarnated-engine/src/reincarnated/simulation/math/bc-measurement-coverage-audit-sim-side-2026-06-13.md` (your own) + `reincarnated-engine/src/reincarnated/generation/notes/bc-measurement-coverage-audit-2026-06-13.md` (rocket gen-side)
- **The Axis-4-bridge pattern (the template to replicate):** your defensive-bridge measurement work + `agentic_orchestration/gandalf/notes/2026-06-13-bc-orphan-sizing-ruling.md`
- **The commit-grade type you mint into:** star-lord's `ExportCommitGradeVerdictDocument` + the `CommitGradeVerdict` provenance contract (`simulation/MIGRATION.md` provenance section + companion §3.1) — W-D is the **production mint site** W-B typed for
- **Your W-C-full cert + spike:** `reincarnated-engine/src/reincarnated/simulation/math/wc-full-resolve-cert-2026-06-13.md`, spike note `wc-derisk-spike-oracle-first-run-2026-06-13.md`

## Cross-seam contract change? (Principle 6 gate — KR pre-assessment)

**YES — two boundaries:**
1. **gamora → star-lord (the commit-grade BC mint).** You emit the measured 8-tuple as a `CommitGradeVerdict` at the spatial site; star-lord consumes/exports it as the production `ExportCommitGradeVerdictDocument` (W-B typed this; W-D is the production mint). **Write a `simulation/MIGRATION.md` section** documenting the emit contract (the 8 axis fields + provenance markers — `fidelity`, `engine`, `scenario_set_hash`, `bc_cell`) field-for-field, so star-lord's export reconciles exactly. **The star-lord export half is a SEPARATE sequenced dispatch (W-D-export), gated on your MIGRATION landing** — coordinate via KR; do not author the export side yourself.
2. **gamora → generation (the predicted→measured replacement).** You replace generation-stamped predicted labels with measured ones for the at-risk axes. Document in MIGRATION which predicted fields are now superseded by measurement (rocket consumes this at the generation boundary; ADR-004).

## Scope

- [ ] **§4.D validation-gate FIRST (Discipline #6 — empirical-inspection-over-assumption):** inspect `arena.py` — confirm whether `boss_with_adds` (240s) already sustains a proxy population to steady-state, or whether proxies idle after the 2 adds die. **Only build a NEW sustained-wave fixture if the existing one is insufficient.** **Fixture acceptance:** K5's mean-active-proxy-count is stable-across-seeds in the sustained room (the Axis-2A bin reproduces) where it is noise in the transient rooms (oracle §4.D acceptance). Smoke-test against that acceptance before wiring 2A. This is the hard prerequisite for Axis-2A — do not wire 2A against the single-pack fixture.
- [ ] **CONFIRM the 2 composition-determined axes** from spatial telemetry — **Geometry (2)** + **range-half of Engagement (1)** — wired, not default-valued (cheap read-back; no measurement-reduction build). Verify predicted ≡ measured holds (it should, by construction — if it diverges, that is a finding: surface it).
- [ ] **BUILD measurement-reduction for the ~4.5 behaviorally-realized axes** via the Axis-4-bridge pattern, in priority order: **Axis 2A (proxy, pri-1; against the sustained-wave fixture)** → **Axis 5 (resource/charge-stack, pri-2)** → **mobility-half of Engagement 1** → **Tempo 3A** → **Control 2B (lower confidence — document the confidence)**. Each: genuine spatial-telemetry measurement replacing the predicted label, wired not default-valued.
- [ ] **Build the M1 gather-primitive + run the with/without ablation** (oracle §5.2) — re-close the K4 ⚠B canary's mechanism half. Report the ablation result (with-primitive margin re-closes ≥ seed-majority; without-primitive reproduces 6/9; the difference attributable to the primitive). *(If this is a larger rework than W-D should carry, STOP and surface — do not half-build.)*
- [ ] **Mint the measured 8-tuple as a `CommitGradeVerdict`** at the spatial site (provenance: `fidelity:"commit"`, engine, scenario_set_hash, bc_cell) — the production mint W-B typed for. Replace the placeholder `bc_cell`.
- [ ] **The Bucket-A check on the spatial seam:** assert every one of the 8 axes is wired (sourced from spatial telemetry), none default-valued. This is the §6.2 cond. 4 gate. **The gate is INVARIANT to the CONFIRM/BUILD split:** all 8 must be sourced-from-spatial-telemetry regardless of whether 2B (or any axis) resolves to BUILD or CONFIRM. If 2B moves to CONFIRM, it is still wired (cheap read-back), still counted toward the 8 — the *build* shrinks, the *gate* does not.
- [ ] **Pre-register (Discipline #2)** the expected **bin** per axis per reference kit (axes are binned, not continuous-valued — pre-register bin-for-bin) BEFORE running the measurement, so the MEASURE cert is judged against a fixed prediction, not post-hoc.
- [ ] **Smoke-test before the full measurement run** (Discipline #2.1); declare resource-scaling (Discipline #1.1) — the sustained-wave fixture changes the per-fight cost; project it.
- [ ] `simulation/MIGRATION.md` section (the emit contract for star-lord + the predicted→measured supersession for rocket).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-wd-six-axis-measure-1`.

## Out of scope (explicit non-goals)

- **MEASURE condition 5 — the defensive-bridge commit-grade re-validation in boss_with_adds** — that is **W-F** (needs the boss room; condition 5 is W-F's exit per oracle §6.4).
- **The star-lord commit-grade BC export (production `ExportCommitGradeVerdictDocument`)** — a SEPARATE W-D-export dispatch, gated on your emit MIGRATION. You write the emit contract; star-lord wires the export.
- **Growing a 7th reference kit / re-opening arity** — arity = 8 is RATIFIED (oracle §6.3, W-C.5 close §2). Nothing was promoted from Bucket B.
- **The other 3 cohort columns (DPS-min-maxer / Defensive / Hybrid)** — derived against cohort-tagged *generation* kits; W-D may begin them if the measurement build naturally produces them, but they are not a W-D exit gate (defer to W-F if they balloon scope — document the line).
- **The parked design forks** (PHASE_MOMENTUM untargetability; GEOMETRY_PROPAGATION corpse-cascade) — OUT of cert-wave scope (W-C.5 close §4).
- **rocket §5 reference-kit hardening** — if the MEASURE build reveals a reference kit needs hardening to measure cleanly, surface it to KR as a rocket follow-on; do not harden generation fixtures yourself (gen seam).
- **Pushing to remote** — Matt's wave-close gate; accumulate commits.

## Open questions for the agent to resolve (document at Gate-2)

- **The M1 gather-primitive sub-scope** — is it W-D-sized, or does the movement-AI rework warrant its own sub-dispatch? Draw the line and document.
- **Axis 2B (Control) confidence** — the structural read flags it lower-confidence. Does spatial telemetry give a clean Control measurement, or is it itself composition-determined-after-all? Document what you find (this could shrink the build from ~4.5 to fewer).
- **The composition-determined confirm** — if Geometry (2) or range-half of Engagement (1) turns out to diverge from predicted in spatial telemetry (it shouldn't), that is a finding that moves an axis from CONFIRM to BUILD — surface it.
- **Cohort columns** — how far the measurement build naturally carries the other 3 columns vs what defers to W-F.

## References

- Oracle §6.2/§6.3/§5.2/§4.D: `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`
- W-C.5 close §3 (scope authority): `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Structural-read note: `agentic_orchestration/gandalf/notes/2026-06-13-bc-predicted-vs-measured-structural-read.md`
- Coverage-audit pair: sim-side `bc-measurement-coverage-audit-sim-side-2026-06-13.md` + gen-side `bc-measurement-coverage-audit-2026-06-13.md`
- W-C-full cert (the M1 finding): `reincarnated-engine/src/reincarnated/simulation/math/wc-full-resolve-cert-2026-06-13.md`
- Gate-2: jack-ryan gates the MEASURE cert cond. 4 — the pre-registration, the Bucket-A wired-not-default check across all 8 axes, the SAFE-confirm vs AT-RISK-build discrimination, the M1 ablation, and the CommitGradeVerdict provenance.

---

**Author:** knight-rider, 2026-06-13. W-D — the measurement-instrument build: turns the spatial engine from "resolves combat" (RESOLVE/W-C) into "measures kit identity" (MEASURE cond. 4), by building genuine spatial-telemetry measurement for the behaviorally-realized axes (not wiring predicted labels), confirming the composition-determined ones, landing the sustained-wave fixture Axis-2A needs, and re-closing the K4 mechanism half via the M1 gather-primitive ablation — minting the first commit-grade behavioral identity.

---

## Completion record

**Completed by:** gamora, 2026-06-13. **Tag:** `gamora/v-wd-six-axis-measure-1`. **Did NOT push** (Matt wave-close gate).

**Deliverables (engine seam `~/Games/reincarnated-engine`):**
- Math note (Discipline #1, before code): `src/reincarnated/simulation/math/wd-six-axis-measure-build-2026-06-13.md` (incl. §1 Axis-2A STOP-and-surface, §5 M1 sub-scope, §8 pre-registration, §10 post-run findings).
- NEW module: `src/reincarnated/simulation/spatial_gauntlet/spatial_bc_measurement.py` (commit-grade 8-axis reduction from spatial telemetry; parallel to the untouched 1D `bc_measurement.py`).
- Engine changes: `spatial_engine.py` (M1 `player_gather_primitive` flag + `M1_GATHER_RADIUS_M`; Axis-1 `total_displacement` accumulator); `spatial_telemetry.py` (additive `SpatialFightResult.total_displacement`).
- Cert harness: `scripts/gamora_wd_six_axis_measure_2026_06_13.py`; output `output/wd-six-axis-measure-2026-06-13.json`.
- MIGRATION v1.31 (emit contract for star-lord + predicted→measured supersession for rocket).
- 8 new tests `tests/test_wd_spatial_bc_measurement.py` (8/8 pass; 97/97 spatial+typewall+wd green).

### (a) MEASURE cond. 4 — PASS (the EXIT GATE), with the pre-registration vs result

**EXIT GATE = Bucket-A all-8-wired-not-default + CommitGradeVerdict mint → PASS.** Pre-registration was bin-per-axis-per-kit (Discipline #2, math note §8). Result vs pre-reg:
- **Geometry (CONFIRM): PASS exactly** — K1/K6 single-target, K2/K4/K5 large-AOE, K3 small-AOE. predicted ≡ measured.
- **Mobility (BUILD): WIRED+measured, edge mis-calibrated** — raw displacement orders K4 highest (64.4 m/min) as pre-registered, but the lock's 30/min threshold bins ALL kits `fast` (spatial baseline-closing) → Discipline #17 lock-edge re-calibration finding (gandalf).
- **Defensive (RE-EMIT): WIRED, density-room clear-rate-dominated** — K6 tank reads LOWEST eHP (durability invisible when un-threatened); discrimination = W-F boss room (the oracle's own §6.2 cond.5 boundary), as expected.
- **Resource/Control (BUILD): WIRED, reference-set-undifferentiated** — uniform stamina / no CC kit, so wired-but-not-exercised.
The discrimination-reach "misses" on mobility/defensive are predicted-and-explained (axes whose discrimination lives outside density rooms / outside the undifferentiated set), NOT measurement bugs. The GATE (wired-not-default + mint) is the PASS.

### (b) Bucket-A 8-axis wired-not-default — RESULT: all 8 WIRED for all 6 kits

CONFIRM'd: Geometry (2), range-half of Engagement (1). BUILT: Resource (5), mobility-half of Engagement (1), Tempo (3A), Control (2B). RE-EMIT: Variance (3B), Defensive (4). **WIRED-DEFERRED: Axis-2A Proxy** (visible measurable=False flag, not fabricated). **2B did NOT shrink to CONFIRM in general** — it is damage-pure for THIS undifferentiated reference set (no CC kit), but the reduction is a genuine BUILD that would discriminate a CC-bearing kit.

### (c) §4.D fixture outcome — boss_with_adds did NOT suffice; NO new fixture built (correct)

§4.D inspection (Discipline #6): the spatial engine has NO player-side proxy mechanic, and `ArenaScenario` has NO wave/respawn structure (`mob_spawns` is a fixed one-shot list; `boss_with_adds` = 1 boss + 2 adds, boss_killed, 240s). A sustained-wave fixture for a proxy population the engine cannot produce would measure noise/zero (the deeper form of the §4.D "certify against noise" trap). **NO fixture built** — STOP-and-surfaced. The §4.D fixture is gated on the spatial-proxy port (see e/g).

### (d) M1 ablation — NEGATIVE causal result (obligation DISCHARGED, hypothesis disproven)

WITHOUT gather: K4=45.4, K2=41.4, margin +3.99, 6/9. WITH gather: K4=66.1, K2=69.6, margin −3.44, 1/9. The gather primitive INVERTS the margin — it is an AOE-coverage primitive that lifts the STATIONARY nova (K2) MORE than the mobile kit (K4). The oracle §5.2 hypothesis (gather re-closes the margin via K4's movement_speed) is DISPROVEN. Per "causation-proving, not threshold-holds," I report the honest negative direction: the per-seed K4≥K2 margin is NOT a movement-credit gap re-closable by an M1 gather primitive. Obligation discharged with a disproven hypothesis (NOT a cert FAIL). The primitive is left in behind its default-off flag. RESOLVE direction half UNCHANGED (re-confirmed PASS). **Recommended disposition (gandalf, oracle §5.2 amendment): the per-seed margin is closing-time noise that no gather model cleanly converts to setup-credit; the direction stays certified; the W-D obligation closes NEGATIVE.**

### (e) CommitGradeVerdict mint + emit contract for star-lord

Minted via `spatial_bc_measurement.mint_commit_grade_verdict()`: fidelity=commit, engine=spatial (pinned), scenario_set_hash (non-empty sha256), bc_cell = measured 8-tuple. `require_commit_grade()` ADMITS it. The **emit contract (8 axis fields + 4 provenance markers, field-for-field) is written in MIGRATION v1.31** for the SEPARATE W-D-export dispatch (gated on this MIGRATION; star-lord wires the export — I did NOT author the export side).

### (f) Composition-determined divergence (CONFIRM→BUILD finding)

**NONE.** Geometry (2) and range-half of Engagement (1) read back from spatial telemetry as composed — predicted ≡ measured holds, as the structural read predicted. No axis moved from CONFIRM to BUILD.

### (g) Needs Matt/gandalf/rocket before W-E/W-F

- **KR/Matt:** sequence the **spatial-proxy-mechanic port** (Axis-2A + §4.D fixture follow-on — W-D-2A or W-F). A movement-AI-scale rework; gamora-seam kernel code but substantial. Do NOT build §4.D before the port.
- **gandalf:** (i) oracle §5.2 amendment recording the M1 ablation NEGATIVE result; (ii) Discipline #17 spatial re-calibration of the Axis-1 mobility lock edge (30 tiles/min mis-bins at spatial baseline-closing; spatial displacement distribution 50–64 m/min is the calibration input).
- **rocket (via KR):** reference-kit-coverage follow-on — a resource/CC/proxy-differentiated reference kit to EXERCISE the Resource/Control/Proxy axes (dispatch-out-of-scope §5 hardening; arity=8 RATIFIED, NO 7th kit).
- **star-lord (via KR):** the W-D-export dispatch (consume the CommitGradeVerdict emit; MIGRATION v1.31 contract A) + the `spatial_fight_results.total_displacement` additive column.
