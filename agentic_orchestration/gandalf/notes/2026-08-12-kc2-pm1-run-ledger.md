# KC2-PM1 run ledger — player movement-while-channeling, sim-side, new baton

> **Charter:** Matt's run prompt, 2026-08-12 session (verbatim intent below). **Conductor:** gandalf (`RUN-CONDUCTOR`).
> **Commissioning lineage:** SB-1 ledger rows R-CPB-4 (motion wire-blocked scene-side, ROUTED to engine) + PM-1 (parallel sim lap commissioned on Matt's word). The R-CPB-5 generosity law binds **presentation**, not this sim lap.
> **Launch word:** Matt, 2026-08-12 — *"Please run to baton completion. If you have a matt question/decision, send it here."* Fork-sheet leans adopted as rulings by that word; **all veto-open**; commitment questions route to the live terminal.

---

## Matt design intent (verbatim, rides the run)

> "the character needs to have directional motion while spinning. I think it may make sense to have the direction of movement always be towards the largest group of enemies or most bosses as these were the goals that I had while playing the scene in GD."

## L-0 — Launch pins (2026-08-12)

| pin | value |
|---|---|
| **Baseline baton (FROZEN forever)** | `reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` @ sha256 `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` — re-verified from bytes at launch (GL-6). Never overwritten; new baton = SIBLING file + own digest. |
| **Engine repo** | HEAD `12e76958`; porcelain 2,789 lines = the FG-17 baseline on record (SB-1 ledger A2-1). |
| **Seam boundary** | This run touches `~/Games/reincarnated-engine/` ONLY. `reincarnated-godot/` belongs to the parallel SB-1 session (A2b cell in flight) — zero collision by construction. |
| **Emission machinery located** | `export/kc2_baton_emit.py` + `export/kc2_run_adapter.py` (star-lord lineage); phase-E sim scripts `simulation/scripts/gamora_kc2_*` (gamora seam); factory-spine landing `e386f529` (meta). |
| **Law vocabulary inherited** | SB-1 charter: GL-6 digest-verify · GL-12 no fabrication · FG-10 determinism (digest ×2, layer declared). |
| **Matt interface** | live terminal, this session — commitment questions sent as they arise; no scheduled checkpoint (run ends at HALT-with-numbers). |

## R-PM1 — Rulings at launch (fork sheet presented; Matt's run word adopts leans; ALL VETO-OPEN)

| id | ruling |
|---|---|
| **R-PM1-1** | **Move speed while channeling = FULL** (`move_speed_fraction = 1.0`, one named constant, declared in receipt). Decisive basis: the reference scene (GD Eye of Reckoning) was played by Matt at full speed; the player-model mirrors the play it models. Genre split named honestly: D3 WW baseline is reduced-speed (Hurricane rune restores full) — training-memory, not probe-verified; R-CPB-3b covered rev rates only. |
| **R-PM1-2** | **DRIVE-THROUGH with rolling re-target** — target the cluster, drive through it, re-target rolling; no stop-at-edge (orbiting-vacuum anti-pattern). Pre-named consequence: a moving player drags the 2.400 m engage ring — baseline dwells become chases; that delta IS a finding, not a defect. |
| **R-PM1-3** | **Policy parameters = gamora reasoning-boundaries**, two riders: (a) objective shape expresses Matt's verbatim intent (score ≈ pack size + β·boss-weight, β declared); (b) **hysteresis is load-bearing, not tuning** — target-flapping between near-equal clusters renders as drunk-walk jitter in any future scene. All values seeded, deterministic, declared in the emission receipt. |
| **R-PM1-4** | **SAME scenario + seed as E-s09-cp150** — single-variable experiment; the diff is the finding. Honesty rider: same seed ≠ identical downstream streams (kill order + RNG consumption diverge once the player moves); comparison is RUN-LEVEL (total ticks, kill curve, path length, deaths, wave pacing), never tick-by-tick. Fold rider: **channel stays on 100% of ticks** — movement is the ONLY delta this lap. |
| **R-PM1-5** | **Empty-target policy = HOLD** at current position when zero live targets — the player-model gets no oracle knowledge of the spawn schedule; emitter pre-positioning (crucible memory) is a later policy beat if the findings say idle-time matters. |

## Laws (from the charter, binding)

1. E-s09-cp150 FROZEN — sibling baton, own digest (GL-6).
2. Determinism: policy deterministic (seeded, no wall-clock); emission digest reproduces ×2 EXACTLY (FG-10, layer declared).
3. **NO balance tuning** — policy will change clear pacing; deliverable = comparative findings vs pinned baseline; tuning is a later beat on those numbers.
4. Wire schema: player gains knots/path spans like any actor; schema delta DECLARED in the receipt (the scene consumer needs it named). `heading_rad` stays DECLARED-NON-SEMANTIC (R-CPA-4: the body performs the channel; travel direction derivable from path).
5. Seams: gamora writes ALL engine code this run (Matt's charter word); if `export/` files need amendment for the player-path carrier, edits are minimal + documented in `export/MIGRATION.md` per ADR-004 + flagged for star-lord in the landing note.
6. Conductor writes no production code; verification from own seat at landing (CL-10).

## Target-state (decidable)

New sibling baton emitted + digest ×2 exact + policy asserts green + comparative findings note + this ledger updated → **HALT to Matt with the numbers** BEFORE any scene-side consumption is commissioned (rendering = SB-1 machinery, separate beat on Matt's word).

---

*Ledger opened by gandalf (`RUN-CONDUCTOR`), 2026-08-12, at Matt's run word.*
