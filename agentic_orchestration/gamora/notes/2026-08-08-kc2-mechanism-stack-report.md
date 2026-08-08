# KC2-SIM Phase C — mechanism-stack build report (gamora seam)

**Run:** KC2-SIM (autonomous, desirable-run pattern). **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora (simulation seam). **Phase:** C — build, spec §§ 1–10 + § 12 + § 13.
**Spec (frozen, consumer-signed):** `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`.
**Charter:** `gandalf/notes/2026-08-07-kc2-sim-run-charter.md`. **Ledger disciplines applied:**
L-16 (geometry family, Phase-C BINDING) · L-29 (eHP chain + array-lookup law).
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/kc2-mechanism-stack-2026-08-08.md`.
**Commit state:** ENGINE commits are mine and are made (four laps). **This report is UNCOMMITTED**
per charter § 4.7 — the conductor commits at gate close.

**Status: COMPLETE for §§ 1–10.** All acceptance criteria implemented and tested. Seven items are
raised as `CONDUCTOR-DECISION-NEEDED` (§ 6 below); one AC limb **misses its pinned target and is
reported as a finding rather than tuned** (AC-10.4 p06-ON), per charter § 4.2.

---

## § 1 — Implementation map (spec § → file)

All paths under `~/Games/reincarnated-engine/`.

| Spec § | Mechanism | File | Key surfaces |
|---|---|---|---|
| § 0, § 1.2–1.4, § 3, § 5, § 7, § 8 | fixture constants of record | `src/reincarnated/simulation/kc2/fixture.py` | `Cited` (value + spec cite + grade), `AURA_RESERVES`, `OUT_OF_MODEL`, `V_REF_M_PER_S` |
| § 1 | channel state machine | `src/reincarnated/simulation/kc2/channel.py` | `ChannelMachine`, `ChannelState`, `tick_period_s`, `ticks_per_s`, `compose_damage_basis`, `SoulfireTick`, `ChannelRun.ticks_in_hold` / `.ticks_including_tail` |
| § 2 | moving circle + L-16 family | `src/reincarnated/simulation/kc2/disc.py` | `MovingDisc.resolve_tick`, `DiscTelegraph`, `reconstruct_hits_from_telegraph`, `selects_eor_spin`, `EOR_SPIN_FAMILY`/`EOR_SPIN_SHAPE` |
| § 2.3 | telegraph value-set growth | `src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py:440`, `:489` (pre-edit line nos.) | `VALID_FAMILIES + "eor_spin"`, `VALID_SHAPES + "disc"` |
| § 3, § 5 | drain, reservation, sustain | `src/reincarnated/simulation/kc2/energy.py` | `DrainUnit`, `drain_rate_per_s`, `charge_per_tick`, `ReservationLedger`, `EnergyModel.run_channel`, `SoulfireCostTerm`, `soulfire_sustain_upper_bound_per_s`, `DryOut` |
| § 9 | devotion envelope (no procs) | `src/reincarnated/simulation/kc2/devotion.py` | `SEVEN_POWERS`, `ENVELOPE_DISCLOSURE` (verbatim), `proc_damage_events()`, `ulzaads_duty_cycle_bounds` |
| § 6, § 6.2b, § 10.7 | opposition eHP + wave scaling | `src/reincarnated/simulation/kc2/opposition.py` | `additive_M` / `multiplicative_M`, `bio_life`, `recompute_ehp`, `kubacabra_phase_chain`, `ArrayLookupLaw`, `WaveScaling`, `load_wave160_board`, `encounter_tier_profile` |
| § 10 | wave engine | `src/reincarnated/simulation/kc2/wave_engine.py` | `first_wave_fought`, `content_tier`/`reward_tier`, `count_bounds`, `expected_counts(_over)`, `roll_wave`, `arrival_schedule`, `Arena`, `cycle_time`, `IGNORE_GAME_BALANCE` |
| § 11.3 surfaces (star-lord consumes) | composition harness | `src/reincarnated/simulation/kc2/run.py` | `EVENT_COLUMNS` (24, § 11.4 order), `EVENT_TYPES` (13), `HP_AFTER_REQUIRED`, `simulate_wave`, `KC2Run.validate()`, `out_of_model_manifest()` |
| cross-seam | migration | `src/reincarnated/simulation/MIGRATION.md` (new top entry) | value-set growth, emitter surfaces, vendored SHAs, the two join laws |
| § 4, § 7, § 8 | **nothing built** — dissolved / excluded | guards in `tests/test_kc2_channel_disc.py` | RF absent, `block_chance == 0.0`, retaliation named out-of-model |

**COMPOSE, not double-build (charter § 9):** `opposition.encounter_tier_profile()` reads the Lane-2
tier profiles from `spatial_gauntlet/wr3_encounter_ai.py` at HEAD rather than restating aggro,
distress-call or pursuit numbers. No parallel encounter surface was created.

---

## § 2 — Acceptance-criteria table (every AC in §§ 1–10)

Legend: **PASS** = implemented and asserted green · **PASS (reported)** = green, with a finding
attached · **MISS (FINDING)** = target not reproduced; reported, not tuned.

### § 1 — channel machine

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-1.1 | 100 % AS ⇒ 0.16 s, 375 ± 1 over 60 s | **PASS** | 375 exactly; inter-tick delta 0.16 s ± 1e-9 |
| AC-1.2 | 196 % AS ⇒ 0.0816 s, 735 ± 1 | **PASS** | 735 exactly; `ticks_per_s` = 12.25 EXACT |
| AC-1.3 | tail ≤ 0.25 s after release, never later | **PASS** | overhang ≤ 0.25; last tick ≤ `effect_expiry` |
| AC-1.4 | `tick_period` invariant under every expressible gear config (A2) | **PASS** | period is a pure function of AS; no machine state |
| AC-1.5 | 3.01 m zero, 2.99 m one tick; radius invariant | **PASS** | plus invariance across rank / elapsed / target count |
| AC-1.6 | flat ∈ [324, 344], weapon 64 %, **no fire emitted** | **PASS** | `emitted_fire == 0.0`, `converted_fire == 138.0` |
| AC-1.7 | Soulfire on 0.2 s, typed Lightning | **PASS** | tick sets disjoint; 0.2/0.08163 = 2.45 |

### § 2 — moving circle

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-2.1 | hit/no-hit reconstructed from the telegraph ALONE | **PASS** | FP 0 / FN 0, with a degenerate-predictor tripwire (raises if TP or TN is 0) |
| AC-2.2 | disc centre == player position at the same tick | **PASS** | exact float equality over a 20-sample curved path |
| AC-2.3 | turn rate 0.35 × idle while CHANNELLING | **PASS** | 1.0 in IDLE and TAIL |
| L-16 (BINDING) | own family + own shape; never nova's | **PASS** | `eor_spin`/`disc`; additive growth; coverage 1.0 at r < 3.0 vs the nova's measured gaps; dual-family selector published |

### § 3 — energy drain

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-3.1 | usable ceiling reproduces 1594 from 2576 | **PASS** | derived from the 7-row ledger; MO-1 exact |
| AC-3.2 | band 86–117 below ceiling, never floors | **PASS (reported)** | transit, not equilibrium: `depth(t) = 14.4 + 1.03t`; enters 69.63 s (closed form 69.51), leaves 99.67 (99.61); 0 dry-outs. **Soulfire declared-separate; its headroom is negative — finding E-5** |
| AC-3.3 | flipping `drain_unit` changes exactly one derived quantity | **PASS** | 176.4 → 14.4; identical tick grid and sample count in both arms |
| AC-3.4 | dry-out emits a distinct reason code; fixture yields zero | **PASS** | 0 on fixture terms; the starved arm fires, so the zero is a measurement |

### § 5 — auras / reservation

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-5.1 | 1594 given max 2576 with the fixture aura set | **PASS** | |
| AC-5.2 | deactivating an aura returns exactly its reserve | **PASS** | recomputed sum, not a decrement; Divine Mandate returns 0 (exclusive ≠ reserving) |
| AC-5.3 | out-of-model set named in provenance | **PASS** | 13 named entries incl. Ascension + the three triggered buffs |
| MO-2 | 982 **derived**, not hard-coded | **PASS** | 7 cited rows sum to 982; superseded 624 enumeration absent from the live table |

### § 6 — pack opposition

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-6.1 | spawned records ⊆ P-E6 roster, weighted as emitted | **PASS** | `roll_wave` picks exactly one weighted alternative per point from the emission |
| AC-6.2 | body count reproduces § 10.5 to the integer over 151–170 | **PASS (reported)** | champions **63.00 EXACT**; regulars p06-OFF 286.83 inside T-2. p06-ON limb → AC-10.4b |
| AC-6.3 | concurrent bosses are not capped | **PASS** | no concurrency cap exists in the model; `survivalevent.lua` L548 ignores the engine's boss limit on every spawn |
| AC-6.4 | every monster carries its source record path | **PASS** | on board entries and on emitted actors; resolved bio carried too |
| AC-6.5 | chain reproduces F1/F2 within ±0.05 %; **multiplicative must FAIL** | **PASS** | F1 −0.0039 %, F2 +0.0016 %; multiplicative M 28.696 vs 10.02 (×2.864) asserted to fail; p04 inside its declared ±5 % band (−4.33 %) |

### § 10 — wave engine

| AC | Claim | Result | Evidence |
|---|---|---|---|
| AC-10.1 | `first_wave_fought == label + 1` for every offer | **PASS** | {0,50,100,150,180}; non-offer labels raise |
| AC-10.2 | content tier `ceil(w/10)`, rewardTier `floor(w/10)`, allowed to differ | **PASS** | 151 → 16/15; checked across all 200 waves |
| AC-10.3 | wave 160: exactly one nemesis on p01/p02/p03 over 1,000 rolls, marginals within sampling error, zero trash | **PASS** | 10/5/2 distinct draws; all marginals within 4 SE; trash count 0 over 1,000 rolls |
| AC-10.4 | 292.0 ± 5.5 regulars p06-OFF; **63.0 champions**; 316.5 p06-ON | **PASS / MISS** | champions **63.00 EXACT**; p06-OFF **286.83** (Δ −5.17, inside ±5.5). **p06-ON 306.83 vs 316.5 — Δ −9.67, OUTSIDE T-2's ±6.01 → FINDING E-2** |
| AC-10.5 | life scaling while fighting 160 = 322 (not 324, not 168) | **PASS** | plus offTotal +43 / offPhys −21 at 160; 965 / +125 while fighting 200; decade wall binds at 172 |
| AC-10.6 | p05 staggered 3 s from t+4 s; p01–p04 at t=0; p06 only when toggled | **PASS** | wave 151 p05 = [4.0, 7.0, 10.0, 13.0]; wave 160 has no p05; p06 disappears when toggled off |
| AC-10.7 | minimum cycle time ≥ pinned floor, EMERGING from geometry | **PASS** | traversal `(d − 3.0)/v` is the binding term; a small arena drops the total below the floor, proving the floor is not a hidden addend |

### § 9 — devotion envelope

| AC | Claim | Result |
|---|---|---|
| AC-9.1 | **no** proc damage events | **PASS** (`proc_damage_events() == []`, sum 0.0) |
| AC-9.2 | disclosure block verbatim and complete | **PASS** (14 clause probes) |
| AC-9.3 | no ICD modelled for Assassin's Mark or Maul | **PASS** (`cooldown_s is None`, not `0.0`) |

### §§ 4 / 7 / 8 — dissolved and excluded (acceptance NON-requirements, guards only)

| Row | Result |
|---|---|
| § 4 RF | **no RF tests beyond an A1-regression guard**; no RF mechanism exists in `kc2/` |
| § 7 block | `block_chance == 0.0` guard only; no block model built |
| § 8 retaliation | named in `OUT_OF_MODEL` so its absence cannot read as a measured zero |

---

## § 3 — Test summary

| File | Tests | Covers |
|---|---:|---|
| `tests/test_kc2_channel_disc.py` | 21 | AC-1.1…1.7, AC-2.1…2.3, L-16 ×4, dissolved-row guards ×3 |
| `tests/test_kc2_energy_devotion.py` | 17 | AC-3.1…3.4, AC-5.1…5.3, AC-9.1…9.3, decomposition, MO-2 derivation |
| `tests/test_kc2_opposition_wave_engine.py` | 26 | AC-6.1…6.5, AC-10.1…10.7, lookup-law family + boundary + decade wall, F-2 regression guard, rank-HP ban |
| `tests/test_kc2_run_surfaces.py` | 14 | `hp_after` non-null + exact reconciliation, `run_tick` monotonic run-wide, `fight_tick` nullable, no per-actor HP tracks, geometry family on damage rows |
| **total new** | **78** | all green |

**Regression posture.** The value-set growth touched four pre-existing scope-guardrail tests
(`test_br2_resolve_truth_1` ×2, `test_br2_trace_stage_1`, `test_wr3_stage2c`). Each was **AMENDED,
NOT DELETED**, per BR-2's own rule — the retention limb is untouched and a named-additions limb is
added, so a third addition has to argue for itself in the same place.

**Pre-existing failures, verified before amending anything:** `git stash`-and-rerun at HEAD
`ebf13240` reproduced **2 failures, test-ID for test-ID** —
`test_wr2_d_nova_telegraph::test_the_minted_telegraph_carries_the_DERIVED_duration_under_the_arm`
and `::test_the_minted_telegraph_carries_the_MEASURED_0_750_off_the_arm_H_M2_f`. Both are BR-2's
own carried failures (the nova moved from `"circle"` to `"star"` and these tests select on the old
value); neither is touched by this work. Targeted blast-radius run after the amendment:
**220 passed / 2 failed**, the same two.

**FULL-SUITE RESULT: launched, STILL IN FLIGHT at report time — see § 8.** Stated plainly rather
than omitted: `pytest tests/ -q` was started and had not returned when this report was written. The
regression evidence this report stands on is the **targeted blast-radius run (315 passed / 2
pre-existing failures)** plus the stash-and-rerun baseline, which is smoke-grade per Discipline #2.
Full-suite confirmation is a milestone-validation step and is the conductor's to re-run at gate
close.

---

## § 4 — Vendored data (byte-identical; SHA-256 recorded)

Copied into `reincarnated-engine/data/kc2/`. **Source of record remains the meta-repo emissions**;
these are copies and `diff -q` confirmed byte identity at vendor time.

| file | sha256 | source |
|---|---|---|
| `t20_wave160_board_ehp.csv` | `01160fd0b24d57b3d89e2713ef978288d4c5aefd1b7522b1e7404d47381a94e0` | `legolas/scratch/2026-08-08-kc2-ehp-composition/` |
| `halt9_survival_wave_scaling_full.csv` | `fe01a472f381dfa15ca1beb11a515d06cfe86d5a5934a3e0183229a05d4bf04b` | `legolas/scratch/2026-08-08-kc2-halt-bundle/` |
| `halt9_survival_scalars.csv` | `177212de29a776f692d1779c3d036e615f2a39660f0ce1cec89079ab7365d436` | `legolas/scratch/2026-08-08-kc2-halt-bundle/` |
| `u8_survival_wave_scaling.csv` | `558ad3f6be3748eec2e9b130791b0871f36ab60feb7b0d3259b832bdbd038204` | `legolas/scratch/2026-08-07-u8-tierwave/` |
| `pe6_crucible_waves.csv` | `9dbc4bb34c3919cbe8ed5f379f31e3eb294a8c3b89e0cf2f4e1873c85cac7b6d` | `legolas/scratch/2026-08-07-pe6-crucible/` |
| `pe6_crucible_wave_pools.csv` | `587e49155b8c1772617fe077d263583a046fab8cd0f3a36ea4472a64a484d8bf` | `legolas/scratch/2026-08-07-pe6-crucible/` |

`s4_waves_full.json` (12.7 MB nested) was read but **not vendored** — the flat pools CSV carries the
per-wave-per-spawn-point grain the sim consumes at 1/10th the weight, and the sim's join is against
the flat form.

---

## § 5 — Deviations, declared

| # | Deviation | Why, and where it is recorded |
|---|---|---|
| D-1 | **Tick emission phase**: ticks fire at `t = k·T` for **k ≥ 1** (period-elapsed), not k ≥ 0 | `timeBetweenAttacks` names the interval *between* applications. Press-inclusive yields exactly one more tick; both sit inside AC-1.1/1.2's ±1, so the choice is declared, not fitted. Math note § B.2 |
| D-2 | **Two tick counts are named separately** (`ticks_in_hold` vs `ticks_including_tail`) rather than one total | The AC's "60 s hold emits 735" counts the hold window; the tail adds up to 3 more. A single ambiguous total silently inflates a graded count. Math note § B.3 |
| D-3 | **Per-tick damage does not target the sheet's 43,691–59,761** | HALT-4 is PARTIAL (ORDER-1 favoured, 3.2 % signal under a ~20 % un-enumerated remainder). The gap is reported by a test; no coefficient is introduced. Finding E-6 |
| D-4 | **Energy is integrated on the TICK GRID**, not at a fixed sample rate | A 10 Hz sampler aliased against 12.25 Hz ticks. Corrected, and the math note is **amended in place (§ D.3a)** rather than silently edited |
| D-5 | **`contact_distance_m` is a declared piloting parameter** (default 1.0 m) | The harness previously closed to exactly `radius`, i.e. onto the `<=` boundary, where float rounding produced 6,000 ticks and zero hits. Declared under § 9.5's `piloting_parameters` error-bar class, not papered over with an epsilon |
| D-6 | **`shape = "disc"` is a new enum value** rather than reusing `"circle"` | Spec § 2.3 is explicit; and `"circle"` already carries the blizzard's per-drop scatter primitive. Argued in MIGRATION § 2 and in `disc.py`'s header |
| D-7 | § 5.2's **624** reserve enumeration is implemented **nowhere** | It is the superseded read; § 3.2's 982 = 982 is the closed one. Carrying both is how a closed HALT re-opens by accident |

---

## § 6 — `CONDUCTOR-DECISION-NEEDED`

| # | Item | Quantified consequence | Sim's current behaviour |
|---|---|---|---|
| **E-1** | **Do Tip-the-Scales leech instances STACK?** 2.0 s duration on a 1.0 s cooldown admits two concurrent. § 3.2 says "100/s while up" and does not adjudicate. | Non-stacking: net **−1.03/s** (the spec's own sustain story). Stacking: net **+98.97/s** — the draw-down band becomes unreachable from the drain side, and it is the only reading under which the naive Soulfire 100/s is nearly admissible. | Non-stacking, on the § 3.2 citation |
| **E-2** | **`ignoreGameBalance` is in the § 10.5 count model and ABSENT from the source-of-record emission.** 74/632 pools are exempt (all boss pools; only 18 of 96 base-game ones), and `pe6_crucible_wave_pools.csv` carries no such column. | Wave 160 **requires** it (else p01/p02/p03 spawn 2 nemeses each and AC-10.3 fails). Applying § 10.8's declarations costs exactly **4.0 bodies** over 151–170 — which is the entire distance between AC-10.4's p06-ON limb being inside T-2 (310.83) and outside it (306.83 vs 316.5). | Declared override table from § 10.8 + default `False`; `WaveRoll.pools_on_default_exemption` reports the default count |
| **E-3** | **Wave-160 modified body count = 8 against the spec's `≤ 7`.** 3 nemeses (exempt) + 2 at p04 (additives) + 3 p06 champions. | Raw = 3 + 1 + 1 = **5**, which closes on the measured max-simultaneous census **exactly**. The modified figure exceeds the stated bound by one body. Candidate reconciliations exist (p04 exempt; hero placement capped at 1) but adopting one would be fitting. | Reports 8; flagged |
| **E-4** | **Internal spec tension**: § 10.4's *"≤ 1 monster per hero placement"* vs § 10.5 fact 5's *"hero placements spawn THREE heroes each"*. | Fact 5 is the branch that reproduces the pinned **63.0 expected champions EXACTLY**; § 10.4's sentence is honoured only in its regular-roster limb (roster_n = 0 ⇒ zero regulars). | Fact 5 implemented |
| **E-5** | **Soulfire's separate cost term is OVER-CONSTRAINED, not merely unmeasured.** `S ≤ 100u − 176.4 + 75.37(1−d)/d` returns **−1.03 at d = 0.5, −57.56 at d = 0.8, −76.40 at d = 1.0** (u = 1). | There is **no admissible positive value** at any channel duty cycle ≥ 0.5, against a naive max-rank read of 100/s. This is § 3.1's declared "magnitude tension" as a number, and AC-3.2's FINDING clause is the right destination. | `effective_per_s = 0.0`, grade `UNADJUDICATED`, never folded into `drain_rate_per_s`; bound exposed as a function |
| **E-6** | **The component damage arithmetic does not reach the sheet band** (HALT-4 PARTIAL). | The composed flat [324, 344] sits far below the sheet's 43,691–59,761 per hit; closing it needs the un-enumerated ~20 % remainder plus the resolved application order. | Reports the gap; a test pins it so nobody quietly closes it with a coefficient |
| **E-7** | ⚑ **Spec-internal conflict on `waves[].life_modifier_pct`.** § 11.4's inline comment reads *"324 at wave 160 — F-2 guard"*; § 10.7's array-lookup law and **AC-10.5 explicitly** say *"322 while fighting wave 160: not 324"*. The comment reads pre-L-29. | If star-lord's emitter takes the § 11.4 comment, the two seams disagree by **one scaling cell on every opposition HP in the baton** (+0.62 % on `G`, systematic same-signed — the exact signature L-29 used to *reject* the 324 cell). | Sim emits **322**, per the law and the AC; recorded in MIGRATION § 5 and in a test docstring. **Checked against star-lord's emitter at `68e2e372`: `life_modifier_pct` is a pass-through dataclass field, and the only literal 324 is in a synthetic wave-43 test fixture — so the seams agree TODAY and the risk is that the comment is taken later, not that it has been.** Recommend the conductor strike the § 11.4 comment |

---

## § 7 — Engine commits made (this seam, this phase)

| lap | commit | scope |
|---|---|---|
| 1 | `8b0d6b5c` | §§ 1–2: math note, `kc2/{__init__,fixture,channel,disc}.py`, telegraph value-set growth, 4 guardrail amendments, 21 tests |
| 2 | `9d44b00b` | §§ 3/5/9: `kc2/{energy,devotion}.py`, math-note § D.3a correction, 17 tests |
| 3 | `409ce8a6` | §§ 6/10: `kc2/{opposition,wave_engine}.py`, `data/kc2/` (6 vendored CSVs), 26 tests |
| 4 | `9ebc3ca1` | § 11.3 surfaces: `kc2/run.py`, MIGRATION.md entry, AGENT_STATE checkpoint, 14 tests |
| 4a | `c5f9f74b` | checkpoint: lap-4 hash filled (placeholder → real; **not** an amend) |
| 4b | `874302d5` | housekeeping: four unused imports dropped from `kc2/` |

**Seam boundaries verified per commit:** every one of the five touches only
`src/reincarnated/simulation/`, `tests/` and `data/kc2/`. Nothing in `export/`, `telemetry/`,
`llm/`, `generation/`, `element/`, `anchor/`, `foundation/` or the engine's internal `canonical/`.
*(Star-lord's `68e2e372` baton emitter is interleaved in the log between my laps 2 and 3 — his seam,
his commit.)*

**Not pushed** (ADR-006 / charter § 6 — push is Matt's word at run end). **Gate-2 REQUIRED and NOT
self-cleared** (charter § 3, G-C condition).

---

## § 8 — Full-suite status, stated honestly

`pytest tests/ -q` was launched against the completed stack and **had not returned when this report
was written.** It is not reported as green and it is not reported as failing; it is reported as
unfinished, because a suite that has not returned is not evidence either way.

What the build's regression posture *does* rest on, all of it executed:

| run | result |
|---|---|
| KC2's own four files | **78 passed** |
| KC2 + 7 blast-radius files (telegraph schema, BR-2 cells, WR3 stage-2c/W-1/W-2, nova telegraph) | **315 passed / 2 failed** |
| the 2 failures, at HEAD `ebf13240` via `git stash` + rerun, **before** any guardrail was amended | **same 2, test-ID for test-ID** (`test_wr2_d_nova_telegraph::…DERIVED_duration…`, `::…MEASURED_0_750…`) |

Per Discipline #2 this is smoke-grade evidence and is the right grade for a build lap; the full
suite is milestone validation and is the conductor's to re-run at gate close. If it surfaces
anything, the most likely candidates are consumers of `TelegraphSpec.VALID_FAMILIES` /
`VALID_SHAPES` that enumerate without a default arm — which is precisely the D-F4 action MIGRATION
§ 0 puts on consumers, and which would be a *finding about the growth*, not a defect in the
mechanisms.

---

## § 9 — What the next phase inherits

**Ready for G-D (calibration), in the order charter § 3 pre-registers it:**

- **MO-1…MO-5 (direct-binding):** ceiling 1594/2576 and reservation 982 are derived and green;
  HP-max 20,005 and the ~7.0 s cycle floor are carried as pinned constants with the floor emerging
  from geometry. MO-3 (s2 in-combat 1477) is reachable from `EnergyModel.run_channel` — the
  trajectory passes 117 below the ceiling at t ≈ 99.7 s of continuous channelling.
- **s1 ramp 1→93 (BINDING):** the wave engine instantiates every wave in the band; the count model
  and the array-lookup law both hold at the N=1 boundary (clamped, declared).
- **s2 one-sided inequality (INFORMATIVE tripwire):** waves 151–160 instantiate, wave 160 rolls
  honestly, and the opposition board floor is the corrected ≈ 9.4 M rather than the superseded
  ≈ 4.1 M — so any TTK comparison starts from the post-HALT-10 number.
- **Full-ladder runs (reported, unbound):** waves 1–200 are addressable; the 171 decade wall is in
  the scaling join and binds while fighting 172.

**Pre-registered G-D re-open hooks already wired:** a damage-side misfit at exactly-one-cell
granularity re-opens the array-lookup law (L-29(b)) — `WaveScaling` has no scalar path, so testing
the alternative is a one-line change to `ArrayLookupLaw.label_for` and nothing else. HALT-7 (boss
skill rank binding) and HALT-4's residual enumeration remain unfired contingencies.

**What G-D must NOT be allowed to do:** close any of E-1…E-7 by choosing the value that fits. Each
one is stated with its mechanism and its sensitivity so the conductor can rule it on evidence.
