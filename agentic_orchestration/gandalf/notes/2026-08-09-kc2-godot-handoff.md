# KC2 → Godot — THE HANDOFF: one baton, one specified run, build the scene from this file alone

**Date:** 2026-08-09
**Author:** gandalf (RUN-CONDUCTOR of the KC2-SIM run; this note written as SCENEWRIGHT/SPEC-AUTHOR)
**Audience:** drax (Godot presentation seam) + the next session that builds the scene
**Charter discharge:** this is the artifact the run existed to hand over — charter
`2026-08-07-kc2-sim-run-charter.md` § 1: *the next session builds the Godot presentation from the
baton alone.*

---

## 1 · The artifact

| | |
|---|---|
| **Baton of record** | `reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` |
| **SHA-256** | `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` — **verify before you load; a different digest is a different measurement** |
| **Size / counts** | 1.066 MB (your signed budget ≈ 22 MB) · 344 actors · 20 waves · 1,900 event rows · 3,732 track samples · 1,003 path knots |
| **Run encoded** | `E-s09-cp150` — EoR Warlord kit, checkpoint-150 start, waves 151–170 fought, terminal `arena_tier_exhausted` @ 171 (ADMISSIBLE-BY-DECLARATION per R-KC2-13, declared in provenance) |
| **Gates** | 66/66 green at emit — VALIDATOR 32/32 · G-STATS · G-E 33/33, `calibration_grade: FULL`, clean tree |
| **Provenance pin** | spec `d1a0ad19…` · charter commit `a761c357` · ledger commit `db299fd5` · engine `29abeb3` |
| **Reference loader** | `export/baton_v1_stub_consumer.py` (`consume_file()`) — the stub is the executable reading of every rule below |

Selection lineage, if you want it: the pick is slate top-1 under the Matt-ruled fidelity metric
(R-KC2-13 "E-1′ as leaned"; ledger L-78–L-79), veto window held open across three reports and run.
Its wall sits at w161 (+2 from the fixture's w159); the wall-magnitude divergence rides the
divergence ledger on the wire, never silently.

## 2 · Rider-1 declaration — VERBATIM, the boundary of what you are holding

> This baton underwrites scene geometry, wave composition, roster (with measured eHP + swing
> damage), player path, circle sweep, and wave/engage timing. It does NOT underwrite live threat
> resolution: monster attack-TIMING grammar (wind-up, recovery, telegraph, cadence, root-lock) is
> NAMED-ABSENT-DECLARED, arriving via the threat-grammar companion lap (Rider 2).
> Playtest-readiness is a downstream Godot-side milestone gate, judged at Matt's eye
> (desirable-run-pattern § 6 obs. 2 — the owner's eye as instrument of record), NOT this run's
> emit gate.

The same declaration rides the baton's own provenance block. Do not build attack wind-ups from
this file; there is nothing in it to build them from, **and that absence is declared, not missing.**

**Threat-grammar companions (feed the PLAYTEST milestone, not this handoff):**
`galadriel/notes/2026-08-08-kc2-threat-grammar-frames.md` (frame-level grammar; acceptance-envelope
discipline — build the tail first) · `legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary.md`
(DB-resident vs animation-baked timing boundary; `.anm` seam continuation from the Edition-III
intake).

## 3 · Consumer semantics that are NOT obvious from the field names

These are the rules a loader gets wrong if it "does the natural thing." Each is declared on the
wire (free-text `path_coverage` / `scatter_model` / provenance rows) and enforced by a
falsification test in the engine suite — the stub goes red if the wire stops declaring it.

1. **`actors[].path[]` is VERTEX-COMPLETE in VELOCITY vertices.** A knot is recorded at every
   change of the walked path's velocity — direction OR per-step travel (the arrival step is
   clipped at the engage ring and at exact patrol-node arrival: a speed change on an unchanged
   bearing). Linear interpolation between knots **IS** the sim's position function, not an
   approximation. Within a leg the speed is uniform; **never assume uniform speed across a leg
   boundary.**
2. **A 2-knot path is a measured straight walk** (61 of them — exactly the p05 ambush bodies,
   which take no patrol leg). It is not a subsample.
3. **A dwell is two knots at one place, two times.** 12 bodies wait 44–70 ticks at the engage ring
   before dying. Draw the wait.
4. **`spawn_tick` is LAST-STILL-TICK.** The body is **not on the board until
   `path[0].run_tick + 1`** — position at `path[0]` is defined (it is the spawn), membership of
   any geometry is UNDEFINED. **Do not hit-test at `path[0]`.** The spawn knot's `tick`/`t_s`
   disagreement (≤ 1 tick, one-signed) IS the measured spawn drip — do not snap it to the grid.
5. **Spawn scatter is a BOX, not a disc** — half-width `placement_extents_m` per axis (read the
   shape word from `scatter_model`, the magnitude from the typed field). An 8 m circle places
   72 of 344 bodies wrong. Two tier-17 bodies cross the box edge against the wire's single
   band-tier anchor — that is the `DIV-P01-TIER` provenance row, measured and declared, not a
   scatter defect (344/344 verified against tier-correct anchors).
6. **`tick` is wave-local; `run_tick` is the global clock.** The baton's tick period is the sim's
   exact float `0.0816326530612245` (= 1/12.25 under 196% AS) — use the wire's value, not a
   re-derivation; a "same" number written differently moves 20 of 344 spawn ticks.
7. **Summons carry NO path.** Out-of-model (R-L53-2) — an absence, not a gap. Do not fabricate
   motion for them.
8. **Player heading is `0` and DECLARED-NON-SEMANTIC** — EoR is a spin channel; heading is yours
   to drive from channel state. Monster spawn heading is the FACE-PLAYER-CAMP convention,
   declared as such.
9. **`crit` columns are NULL under `crit_model: NOT_MODELLED`** — null means not-modelled, never
   "measured zero crits." Defenses ship as DECLARED-COUNT-ONLY (+4, names NAMED-ABSENT).
10. **The divergence ledger rides `provenance.informative_rows`** (19 rows: 6 `DIVERGENCE` +
    13 `DECLARATION`, families overlap by design). Read it before judging any feel mismatch
    against the GD Crucible reference — every known departure is named there, including the wall
    position/magnitude tension (`DIV-F7-WALL`).

## 4 · Two countersigns asked of drax (your signed surface — ask and they land)

Per `reincarnated-engine/src/reincarnated/export/MIGRATION.md` `[2026-08-09b]`:

1. **The board-boundary rule** (§ 3.4 above) — constrains your loader.
2. **The BOX shape declaration** (§ 3.5) — un-breaks your spawn markers.

**Named, not taken** (first-class schema changes awaiting your signature): `scatter_shape`
Literal · first-class divergence-ledger field · `SCHEMA-PER-TIER-P01`. Also standing: **OBJ-1's
countersign is yours** — the seam-side re-law is closed and structural (`actors[].path[]` is
sim-recorded, vertex-complete; interpolation is the position function), the signature is not.

## 5 · What the run wants judged at your end

The endpoint is Matt's hands on the controller (Q52 ruling § 1.1: after baton → Godot render, the
sim's player model is discarded; Matt IS the player). The scene's job is **faithful reproduction
of the specified run first, perturbation later** — reproduce, then let the divergence ledger say
where reproduction was impossible or ruled away. Playtest-readiness is a milestone gate at Matt's
eye, not an emit gate, and the threat-grammar companions must land before that judgment is fair.

**Refs:** KC2 ledger L-78 … L-84 (`gandalf/notes/2026-08-07-kc2-sim-run-ledger.md`) · Q52 ruling
`gandalf/notes/2026-08-08-q52-ruling-and-riders.md` § 2 · spec
`gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 10–11 · star-lord
`2026-08-09-kc2-re-emit.md` · gamora `2026-08-09-kc2-clip-knot.md` + `2026-08-08-kc2-sim-knots.md`.
