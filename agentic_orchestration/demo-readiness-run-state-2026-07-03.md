# DEMO-READINESS UNATTENDED RUN — state board

> **STATUS:** LIVE RUN STATE (hive-mind state file). **Orchestrator:** knight-rider. **Fired:** 2026-07-03.
> **Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** (Gate-1 ✓ passed + folded).
> **Fire order:** `agentic_orchestration/gandalf/notes/2026-07-03-kr-relay-demo-readiness-run.md`.
> **Authorizations:** commits auto-fire · **push pattern ESTABLISHED — both repos at each wave closeout** · LLM spend no-cap (key errors out; spend logged per pass) · emission exercise Matt-authorized (spec §1-C).
> **Failure policy:** spec §7 — halt-loud; W2 degrade path; W3 pilot beat unconditional.
> **`gates-on:` semantics (spec §3):** dependents declare — `gates-on: X` = this row fires only after X closes.

## Preconditions

| # | Item | Status |
|---|---|---|
| 1 | jack-ryan batched decisions-log registration (G1–G10 + proxy-T4 four + Q6/Q7 six) | ✓ DONE — engine `a10a695`, unpushed; rides first wave-closeout push |
| 2 | Registry schema mini-pass (star-lord drafts → jack-ryan ratifies at W0/W1 boundary → THEN #8b writer) | ✓ **DONE — RATIFIED-WITH-AMENDMENTS** (jack-ryan, G9 no-Matt-gate): writer builds against draft **+ `generation_seed INTEGER`** (manifest.json source; PART-C seed leg — without it the run is described, not reproducible) **+ `in_band_count INTEGER`** (G2 measured output, queryable for W4/§8; JSON blob retained). Launch exclusions affirmed (no cost_usd/git_sha/FKs). Verdict relayed by KR with attribution. |
| 3 | Singleton-config smoke green before W3 (Phase-1 η live; CONVERGENCE+DUAL η=0.0) | ✓ **DONE** — rocket W0, 28/28 GREEN (`generation/notes/w0_prereqs_smoke_2026_07_03.py`; KR re-ran live, Disc #11) |

## Board

| Row | Owner | Dispatch | gates-on | Status |
|---|---|---|---|---|
| W0.rocket (knob · 2-type-decl · fixture · classifier · F-f consumer · singleton smoke) | rocket | `2026-07-03-rocket-w0-prereqs.md` | — | ✓ **DONE** (`rocket/v-demo-run-w0-1` @ `e57b9d8`; all six PASS; no refutation fired; generation-internal, no MIGRATION owed; KR Disc #11-verified incl. live smoke re-run 28/28) |
| W0.star-lord (export DDA-lock widen) + W1 (D.1 #1/#2/#3/#4/#5/#8a + G6 stub supersession) | star-lord | `2026-07-03-star-lord-w0-w1-pipeline-completion.md` | engine-tree-free ✓ | ✓ **DONE** (`star-lord/v-demo-run-w1-1` @ `cbd47b5`; MIGRATION v1.85; 202/202; six-type round-trip PASS w/ non-NULL counts; per-item flavor resumability VERIFIED (spec §11 Q1-iii); 60 stubs `_non_canonical` (G6); no refutation fired; KR Disc #11-verified tag+draft+MIGRATION on disk) |
| W0.gamora (DDA propagation sweep → NEW build-floor + both demo summoners re-cert) | gamora | `2026-07-03-gamora-w0-dda-propagation-sweep.md` | engine-tree-free ✓ | ✓ **DONE** (`gamora/v-demo-run-w0-dda-sweep-1` @ `87c47a6`; propagation-live floor CERTIFIED, factor ×0.6 conservative; anchors held by construction; both summoners RE-CERT WR 1.0 both shells, 136s margin; degeneracy CLEAN; #24 isolation verified; (b)-config NOT invoked — **run proceeds propagation-ON**; KR Disc #11-verified) |
| W1.#8b registry writer | star-lord | **KR sequencing call: folds into the W3 dispatch as step 0** (post-ratification; saves a chain slot; still satisfies Gate-1 #5 ratify-before-build) | registry-schema-ratified | HELD → rides W3 |
| Registry-schema ratification (fast pass, no Matt gate — G9) | jack-ryan | Pattern-A invocation at W0/W1 boundary | W1.#8a-draft ✓ | ✓ **DONE — RATIFIED-WITH-AMENDMENTS** (+`generation_seed`, +`in_band_count`; see precondition 2 row) |
| W2 Gate-1 critique-pair (jack-ryan + gandalf, parallel) | KR invokes | on `2026-07-03-rocket-gamora-w2-pairing-layer.md` | — (reviews dispatch text) | ✓ **CLEARED** (jack-ryan ENDORSE-WITH-FOLDS, E4 fold applied; gandalf ENDORSE ×5 NOTE) |
| W2 Phase 1 (CONVERGENCE + DUAL_PROXY classes + wiring) | rocket | `2026-07-03-rocket-gamora-w2-pairing-layer.md` | ~~W0.classifier · W0.2-type-decl-check · W0.fixture · Gate-1-pair-CLEAR~~ **ALL ✓** | ✓ **DONE** (`rocket/v-demo-run-w2-pairing-1` @ `6a7190b`; matrix/pools DERIVED byte-match 15/65/14×3 import-asserted; E0–E5 test-pinned; η non-vacuous (fixture draws CONVERGENCE 0.679, 1-type draws DUAL 0.615, E1 refused, solo None); round-trip smoke 6/6 GREEN w/ v/vi labels at bundle boundary + negative-mutation; generation MIGRATION W2 entry before tag; no refutation fired; KR Disc #11-verified incl. live smoke 6/6 + 26/26 tests) |
| W2 Phase 2 (cert + E4 sim-cost fold) | gamora | same dispatch | ~~W2.phase1~~ ✓ | ✓ **DONE** (`gamora/v-demo-run-w2-pairing-cert-1` @ `1ec8265`; **BOTH MEMBERS CERTIFIED** at propagation-live 0.6 floor — CONVERGENCE WR 1.0 both shells t 62.6s (merge pays ratified 0.8 tax, clears 300 singleton floor); DUAL WR 1.0 both cases, AQ4 in-band; fixture cert PASS, never-ships fence intact; **E4 PRICED→DEFERRED with named prerequisite** — ECHO-replay ally-attack channel absent from `_spawn_one_ally`, Mirror merge hollow, 2 pairs excluded from cert BY NAME (63/65 certified); seeds 54M+, next-free 55M+; no refutation fired; KR Disc #11-verified) |
| W3 THE EMISSION RUN (un-gate → pilot beat → full-spectrum → gauntlet → flavor split → assemble+register) | star-lord + rocket | `2026-07-03-rocket-star-lord-w3-emission-run.md` | ~~gates all ✓~~ | 🛑 **HALT-LOUD (Phase A refutation FIRED — first §7 invocation of the run):** proxy bins NOT emission-viable — structural gap, not config. Lifting `_DEFERRED_PROXY_BINS` composes proxy-heavy targets with **zero summon skills** → `proxies: []` (3 fatal blockers: Phase-4d stub `:756`, multi-spawn→multi_projectile map, no summon discriminator on PoolMechanic). `ProxySpawn` = RETIRED register reference, nothing to lift. No lift performed, no tag; finding `w3-ungate-refutation-fired-2026-07-03.md` @ engine `0a1706c`, collab `cc24556`. Criterion C unsatisfiable as written → **Matt scope-ruling required**. Critique pair FIRING on the finding; star-lord step-0 registry writer (ruling-independent) FIRING |
| W3 halt adjudication (critique pair on the refutation + options 1/2/3 + W0-vs-W3 evidence tension) | jack-ryan + gandalf (parallel, read-only) | KR invokes | W3.phaseA-halt | ✓ **DONE — verdicts folded** (jack-ryan: structural claim [AFFIRM] all 3 blockers line-verified; W0 #2 "PASS" [AMEND] — validated fixture/classifier layer not composer path, gap masked at W0, impact bounded; Option 3 rejected; C/G4 amendments Matt-gated [AFFIRM]. gandalf: refutation [ENDORSE]; **§5.2 hand-authored authority [CONTEST] — STRUCK by Matt 2026-07-02** ("balanced and pipeline emitted"), Option 2 = knowing reversal; G4 = two promises wearing one number; Option 3 rejected hard; lean = fire solo batch-1 now + Option 1 as follow-on. **Matt decision file:** `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`) |
| **KR run-disposition ruling:** W3 proceeds as **solo full-spectrum BATCH 1** (spec §4 batch mechanism — "one wide run or several registered batches; all batches register"). Criterion C **PARKED loudly, NOT amended** (amendment is Matt-gated per both critics); summoner emission = batch 2, gates on Matt's ruling. | KR | — | critique-pair-DONE | ✓ RULED |
| W3 step-0 registry writer (#8b — ruling-independent under all options; criterion F) | star-lord | Phase B step 0 ONLY, carved out | registry-schema-ratified ✓ | ✓ **DONE** (`star-lord/v-demo-run-w3-step0-registry-1` @ `dc00b2a`; `emission_runs` 17 cols + 2 amendments; idempotent create; **HALTED/PARTIAL state expressible — refutation check CLOSED**; 48/48 tests, zero regressions 4822 vs 4774 baseline; MIGRATION v1.86; KR Disc #11-verified incl. live 48/48) |
| **W3 BATCH 1 — solo full-spectrum emission** (pilot beat → full-spectrum SOLO → gauntlet → flavor split → assemble + register batch 1; criterion C PARKED in registry notes) | star-lord | Phase B under KR batch-1 disposition | W3.step0 ✓ · KR-disposition ✓ | 🔥 **GAUNTLET RUNNING** (pilot beat DONE: 10.65s/kit, 64% yield, 48.7MB RSS → N=100/cell = 1,800 candidates ≈ 5.3h, sizing note @ `ea753a3`; driver + 24/24 tests + MIGRATION v1.87 landed; `--dry-run-flavor` first pass — LLM flavor fires as follow-up step on confirmed survivors. **OPS FINDING + RECOVERY:** star-lord's in-session launch DIED when his agent session closed (log stopped 03:20; lesson: sub-agent-spawned long processes do not survive the sub-agent) — KR relaunched DETACHED (nohup, PID 65847, same seed 55000000, deterministic serial rerun, Disc #3 clean) + armed persistent monitor w/ hourly heartbeat + any-exit notification) |
| W4 verify + curate-prep (DRIFT-CRITIC · Gate-2 · G4 hypothesis test + tagging · offer-table verify · §8 shortlist) | gandalf · jack-ryan · gamora · KR | authored at W4 entry | W3 | HELD |
| gandalf run-window parallel authoring (label→glyph · Glance contract · Binder) | gandalf | NOT wave dependencies (Gate-1 #8) | — | parked to gandalf's own session cadence |

## B-series reconciliation (relay §board discipline)

- **B3** (`2026-07-02-star-lord-six-type-flavor-completion.md`) — **SUPERSEDED (G6)**: never fires; the ~60 null-name stubs marked non-canonical in W1; live remainder = W1 wiring + §8 curation rubric on new output.
- **B4** (`2026-07-02-rocket-star-lord-summoner-ungate-emission-run.md`) — **ABSORBED into this run**: necro-energy prereq = no-op (G4); DDA-lock widen → star-lord W0; F-f consumer → rocket W0; un-gate + run → W3.
- **B5** (`2026-07-02-gandalf-v2-roster-curation.md`) — **ABSORBED into W4** (§8 curation rubric; Matt picks — G7a).
- Phase-3 residuals (classifier · 2-summon fixture) → rocket W0.

## Wave-closeout ledger

*(appended per wave: what closed, commits, push SHA, board deltas)*

### W0 + W1 CLOSEOUT — 2026-07-03

- **W0 rocket** ✓ `e57b9d8` (all six PASS; singleton smoke GREEN 28/28 = precondition 3; no MIGRATION owed — generation-internal)
- **W0 star-lord + W1** ✓ `cbd47b5` (DDA-lock widened; six-type driver + wiring; MIGRATION v1.85; 202/202; per-item resumability VERIFIED; 60 stubs non-canonical per G6; #8b writer rides W3 step 0)
- **W0 gamora** ✓ `87c47a6` (propagation-live floor certified; both demo summoners RE-CERT PASS; degeneracy clean; propagation-ON stands)
- **Preconditions:** 1 ✓ `a10a695` · 2 ✓ RATIFIED-WITH-AMENDMENTS (+`generation_seed`, +`in_band_count`) · 3 ✓ smoke GREEN
- **W2 Gate-1 pair** ✓ CLEARED (jack-ryan ENDORSE-WITH-FOLDS → E4 folded; gandalf ENDORSE)
- **Failure-policy invocations:** ZERO (no halt, no degrade, no (b)-config)
- **Push:** both repos at this closeout (engine: `a10a695`→`87c47a6` chain + 3 tags; meta: orchestration chain)
- **Next:** W2 Phase 1 (rocket) fires — all gates ✓

### W2 CLOSEOUT — 2026-07-03

- **Phase 1 rocket** ✓ `6a7190b` (`rocket/v-demo-run-w2-pairing-1`): CONVERGENCE + DUAL_PROXY strategy classes live; matrix/pools DERIVED byte-match (15/65/14×3 import-asserted — spec drift breaks import); E0–E5 test-pinned (26 tests); η non-vacuous shown; round-trip smoke 6/6 GREEN with rule-v/vi labels at bundle boundary + negative-mutation proof; generation MIGRATION W2 entry before tag
- **Phase 2 gamora** ✓ `1ec8265` (`gamora/v-demo-run-w2-pairing-cert-1`): both members MAGNITUDE-CERTIFIED at the propagation-live floor; fixture cert PASS; sim MIGRATION ADVISORY (no schema change)
- **E4 disposition (Gate-1 fold honored):** priced FIRST, then deferred — ECHO player-skill-replay ally-attack channel absent from `_spawn_one_ally`; certifying Mirror pairs would be vacuous. 2 pairs excluded BY NAME (`{autonomous_caster, delayed_position_shadow}`, `{passive_fighter, delayed_position_shadow}`); **63/65 valid pairs certified**
- **PARKED (named prerequisite, rides closeout report):** ECHO-replay ally-attack channel — generation/sim mechanism addition (second per-tick skill-resolution channel replaying player rotation). Halt reason: absent mechanism; certifying against it would be a vacuous pass. W3 may emit Mirror-shaped kits — they merge STRIKER-only until this lands. Not a W3 blocker.
- **Failure-policy invocations:** ZERO (no stall, no degrade — W3 fires with FULL pairing η live)
- **Push:** both repos at this closeout (engine `6a7190b`→`1ec8265` + 2 tags; meta chain)
- **Next:** W3 THE EMISSION RUN — all gates ✓; rocket Phase A (un-gate) → star-lord Phase B (emission)
