# TSF6-TRACK-A run charter (RATIFIED by standing rulings — TSR-5 "TSF-6 Track-A run charters IMMEDIATELY post-probe" + TSR-6a/6b/6c, Matt 2026-07-23; probe filed `576456a0` 2026-07-23; launched 2026-07-24)

**Date:** 2026-07-24 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executes:** gamora (sim seam)
**Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`) — fit test §2
**Sequencing:** parallel-safe with GD-SLICE run (gamora vs elrond seams, no shared writes — TSR-5 ruling)

---

## §0 Intent (the owner's question, one sentence)

Answer the **parameter-fidelity rung** of Matt's sim-fidelity hypothesis (TSF-6 rung a): configured with Grim Dawn's ACTUAL primary-source monster parameters (.arz body + controller fields), does the engine's simulation reproduce the parameter-implied spatial behaviors — aggro onset, pursuit, leash — and where a mechanism has no sim home, what exactly is the mechanism delta?

**Rubric-law note (KFL-27 lesson, applied at charter):** the owner's question is rung (a) ONLY. Rung (b) behavior-fidelity belongs to Track B (Matt plays GD on his PC under agentic capture; separate charter; vision-model mini bake-off at that time — TSR-6a amendment). **No outcome of this run supports a "sim twins GD" claim** — the VERIFIED claim ceiling is "parameter-faithful in the tested classes, mechanism-delta named in the rest." Predicate-diff vs this §0: the gap register (G4) is load-bearing coverage, not decoration — a run that only reports the PASS cells has narrowed the rubric.

## §1 Substrate (bounded, frozen at launch)

| Item | Role |
|---|---|
| zombie_a01 body + controller ground truth (probe §1: `ViewDistance` 15.0, `InnerViewDistance` 4.0, `SightAngerRate` 3.0 / `InnerSightAngerRate` 12.0, `MaxPursuitDistance` 75.0, `PursuitTime` 10000 ms, `fleeDistance` 16.0 + `FleeBehavior='NeverFlee'`, `WanderDistance` 4.0, `characterRunSpeed` 1.0, `actorRadius` 0.4, `distressCallRange` 16.0) | the GD profile under test |
| `gameengine.dbr` constants (probe §4: `meleeRange` 1.25, `moderateRange` 9.0, `longRange` 15.0, speed caps) | unit-pin substrate |
| gamora's blind-hero machinery (`policy_config: [["distance", 1.0]]`) | the hero-side instrument |
| `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md` | frozen evidence source — values consumed from the note; NO .arz re-parse in this run |

## §2 Fit test

- **F1:** YES — 2 scenarios × enumerable parameter classes (aggro pair, pursuit/leash pair, flee, wander) ≤ 12 cells.
- **F2:** YES — every cell PASS / FAIL / **BLOCKED-MECHANISM** vs pre-registered criterion; exit = cells + gap register + verdict.
- **F3:** YES — forks pre-drained: TSR-6a (run gate = rung a), TSR-6b (anvil + kite-line), TSR-6c (pin principle + provisional-K allowance); difficulty/topology/cadence conductor-pinned (below).
- **F4:** YES — the sim-fidelity instrument is conductor authority (TSF-6 is gandalf's fork slate); gamora owns the executing sim seam.

→ gandalf conducts; gamora executes; KR not engaged (single-seam).

## §3 Step 0 — the unit pin (G1, before ANY scenario runs)

Derive **K** (GD world-units → sim distance-units) ONCE from engine-internal anchors: GD `meleeRange` = 1.25 wu ↔ the sim's melee-engagement distance (gamora names the sim-side constant), cross-checked against `moderateRange` = 9.0 ↔ the sim's mid-band. This is the **provisionally-pinned K** the TSR-6c ruling authorizes (DBR-internal derivation suffices to LAUNCH; Matt's Track-B capture session later upgrades K to externally-anchored). **Log the derivation + chosen K in the run note, veto-open, BEFORE scenario results exist. No post-hoc refitting** (preregistration law, §5.1 of the pattern).

## §4 Scenarios + pre-registered gates

**ANVIL (TSR-6b arm 1):** hero stationary; monster spawn-distance sweep across the K·`InnerViewDistance` and K·`ViewDistance` boundaries.

- **G2a:** no aggro beyond K·15.0 (+10% tol).
- **G2b:** aggro onset by K·15.0 −10% as spawn distance decreases.
- **G2c (finding-class, ungated):** inner-vs-outer anger-rate asymmetry (12.0 vs 3.0) observed / absent / no-mechanism.

**KITE-LINE (TSR-6b arm 2):** hero recedes at fixed speed ratio; monster pursues from aggro.

- **G3a:** pursuit sustained inside K·`MaxPursuitDistance` (75.0 wu).
- **G3b:** disengage/return at K·75.0 ±10% **OR** `PursuitTime` 10000 ms ±10% — whichever mechanism the sim keys on; the report names which (GD carries both; TrinityCore #25833 is the cautionary precedent for hardcoding one).
- **G3c (finding-class):** `FleeBehavior='NeverFlee'` honored (no flee at low HP in-scenario).

**G4 — the GAP REGISTER (load-bearing):** for EVERY substrate parameter class (aggro radii, anger rates, pursuit distance, pursuit time, flee, wander, distress-call), one row: sim-mechanism-home EXISTS (→ tested, cell result) or ABSENT (→ BLOCKED-MECHANISM, named delta). This register + cells + verdict = the run report.

**BLOCKED-MECHANISM law (the honorable fallback):** the sim was built for bounded balance fights, not open-field aggro — some GD parameter classes may have NO sim home (leash, anger accumulation, distress propagation). **Absence is a finding, not a failure.** The hypothesis answer "parameter-faithful in classes {X}; mechanism-delta in classes {Y}" is a COMPLETE, honest rung-(a) answer. **No mechanism gets built mid-run to force a PASS** — mechanism work is a next-lap charter (no silent scope growth). Scenario harness/config code in gamora's seam is normal experiment tooling and fine.

**Conductor-pinned decision rules (veto-open, pinned pre-launch):** (i) difficulty = **Normal** (base DBR ≈ Normal; multiplied tiers out of scope); (ii) **flat-open topology** (pathfinding residuals quarantined from parameter gates); (iii) cadence fields **OUT of scope** this run (movement/aggro only — the animation-vs-logic-time flag stands for the adapter lap).

## §5 Matt interface

- **Pre-run:** nothing on your hands — all substrate landed.
- **In-run:** red-flag pings only; rulings ledger TFL-1..n, veto-open.
- **At end:** parameter-fidelity verdict + gap register → feeds the TSF-6 hypothesis dossier alongside Track B (your PC capture session, separately scheduled, your timing). jack-ryan Gate-2 on the run report (findings-class).

---

## §6 Run status (conductor ledger)

- **2026-07-24 — chartered + gamora commissioned** (background; report lands at `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md`).
- **2026-07-24 — RUN EXECUTED, conductor-verified — RUN DONE** (gamora report `8015f535`; engine `70c1d4d` = unit-pin math note + `tsf6_track_a_harness.py`, 481 insertions, both byte-verified). **G1 PASS:** K = **1.60** pinned pre-scenario per §3 (GD `meleeRange` 1.25 wu ↔ sim melee null-guard 2.0; derivation logged veto-open, no post-hoc refit) + **K-nonlinearity finding**: K_mid 0.889 / K_long 0.933 vs K_melee 1.60 — no single linear K spans the range bands; carried forward as a Track-B calibration delta. **ANVIL (G2a/G2b): BLOCKED-MECHANISM** — the sim has NO aggro-onset concept: `aggro_radius_m` is a dead field (`spatial_engine.py:1124`), mobs pursue from tick 0 at every spawn distance 4→100; graded per the §4 law (absence = finding, evidence attached). **KITE-LINE G3b: PASS-on-distance** — leash fires at dist_from_spawn **120.17 vs K·75.0 = 120.0 (+0.15%)**, distance-keyed (D2/PoE return-to-spawn semantics; trigger `:1706`); pursuit-TIME mechanism absent — report names the mechanism per the gate's either/or. **G4 gap register (7 rows): 1 PARAMETER-FAITHFUL** (pursuit-distance/leash) **/ 1 PARTIAL** (flee — fear-marker-driven `:1711`, no HP-threshold flee) **/ 5 BLOCKED-MECHANISM** (aggro radii, anger rates, pursuit time, wander, distress-call) — every row now carries its GD primary-source parameter values. Verdict honors the §0 ceiling: *parameter-faithful in the leash class; mechanism-delta named in the rest* — no "sim twins GD" claim. **Forward fork NAMED-not-chartered** (commitment boundary per §4 BLOCKED-MECHANISM law): where does encounter-spatial behavior live — sim-side mechanism build (the gap register is now a GD-parameterized worklist) vs Godot-presentation-side encounter AI. Matt rules at a future window. jack-ryan Gate-2 on the report (findings-class) rides the standing queue.

---

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-24.
