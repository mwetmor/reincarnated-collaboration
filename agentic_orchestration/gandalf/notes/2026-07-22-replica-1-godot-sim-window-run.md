# REPLICA-1 — Godot Sim-Window Run (charter + ruling ledger)

**Conductor:** gandalf `RUN-CONDUCTOR`. **Chartered:** 2026-07-22, on Matt's verbatim directive:
*"Let's speed to run a live godot rendered exact auto-attacking replica of the sim so that I can
see it and we can push improvements back into the battle sim, iteratively. But DON'T cut corners,
only recommend to me the removal of steps towards the above path which are unnecessary."*
**Predecessor:** aware-fighter ablation gate (CLOSED (a), L-32 in
`2026-07-22-tier3-encounter-geometry-run-state.md`). Desirable-run-pattern fit: bounded substrate
(engine fight traces + one Godot scene) · decidable target-state (§2) · forks pre-drained (§3
removal table, Matt rules) · authority-resident (this charter's author conducts).

## §1 Thesis — WINDOW, not port (the no-corner-cut architecture)

The battle sim remains the SOLE combat truth. The engine emits **per-tick semantic frames**
(positions, actions, damage events, deaths); Godot **renders** them and derives NOTHING — no
physics, no damage math, no targeting, no cooldowns. Renderer may interpolate POSE between ticks
for smoothness; every gameplay EVENT is trace-sourced. Exactness is therefore achieved **by
construction**, not by verification-after-the-fact: there is no second combat implementation that
could diverge. "Auto-attacking" = the sim's own policy fights (it already does); "live" = real-time
in-engine playback with pause/step/speed scrub — plus a v2 socket-stream upgrade on the SAME frame
schema if wanted.

The iteration loop this enables (Matt's stated purpose): watch → flag a wrongness → targeted sim
experiment / sim change → re-emit trace → re-watch. Improvements land SIM-SIDE; the window never
forks the truth.

## §2 Target-state (decidable)

Matt watches, in Godot on the Mac, at real-time with a working scrubber (pause / step / 0.25–4×):
**the ablation gate's own mismatch cells** — `d2-bowazon`, `poe1-kinetic-fusillade`,
`poe1-caustic-arrow`, `d2-poison-javazon`, `poe1-frost-blades` — **BOTH arms (BLIND and AWARE) at
gate seeds**, rendered from engine-emitted traces with: entity positions per tick · who targets
whom · skill fires · damage numbers · deaths · HP bars. Determinism attested (same seed → same
trace → same playback). Acceptance is Matt's OWN inspection verdict: he can SEE bowazon full-clear
under BLIND and brick under AWARE, and say why. That closes the loop his two directives share —
the replica's first reference set IS the visual autopsy of today's gate.

## §3 The full standing ladder + the five removal recommendations (Matt rules; veto-open)

The standing path to "real combat in Godot" (serial-emission endgame map §6–§7) contains steps that
do NOT serve a sim-window. Per Matt's instruction, removals are RECOMMENDED, not silently taken:

| # | Standing step | Rec | Why removal is safe (not a cut corner) |
|---|---|---|---|
| R1 | Drax bundle loader before replica | **REMOVE from this path** (stays on the game path) | Traces carry every render-needed datum (archetype/element/skill ids inline). The loader serves generated-content presentation, not sim windowing. |
| R2 | VFX grammar contract before replica | **DEFER** — v1 uses a placeholder legibility kit (element-colored primitives keyed by delivery_class) | Exactness lives in positions + events, not particles. The grammar remains the launch-scope system; the placeholder mapping is ~dozens of lines and disposable. |
| R3 | Golden-trace parity battery | **DEFER** until a Godot-native combat port is ever chartered | Playback has no second implementation to verify — there is literally nothing to test. The battery becomes load-bearing only if combat logic is ever ported. |
| R4 | Godot-native combat reimplementation | **OUT of this path entirely** | Window-not-port. The sim stays sole truth; a native port is a later product fork with its own gate (R3 revives there). |
| R5 | Live socket streaming in v1 | **SEQUENCE to v2** — file-replay first, same schema | Replay gives the identical visual result PLUS a free scrubber (better for inspection than a live feed); the socket upgrade later reuses the schema with zero rework. |

Everything not in this table is load-bearing and fires: schema → emitter → playback → watch.

## §4 Gates

- **G1 — Frame-schema contract** (gandalf, named sub-agent): versioned semantic frame schema
  GROUNDED in what the sim already computes (one-truth; substrate-led — read the engine loop first,
  spec second). Deliverable: `2026-07-22-replica1-frame-schema-spec.md`.
- **G2 — Trace emitter** (gamora, engine `simulation/` seam): capture + NDJSON/JSON writer per G1.
  Observability only — ZERO combat-logic changes in the same commits; determinism check (same seed
  twice → byte-identical trace); normal Gate-2 rides.
- **G3 — Playback scene** (drax, `reincarnated-godot/`): flat arena at SIM coordinates (1 sim
  meter = 1 Godot meter — NOT the ravine level, whose geometry would falsify positions),
  isometric-ARPG camera, proxy entities + HP bars + damage floaters + death states, scrubber.
  Zero-derivation rule enforced: renderer consumes frames, never computes gameplay.
- **G4 — Matt watch session + loop protocol**: reference set (§2) rendered; observations →
  targeted sim experiments → re-emit → re-watch. G4 is the product.

**Fallback (honorable, pre-registered):** if live playback stalls on any Godot obstacle, batch MP4
renders from the SAME traces via drax's existing walkthrough harness — Matt still watches the exact
replica this cycle; interactivity follows.

## §5 Matt interface

Removal rulings R1–R5 (now, veto-open — silence past the next session-boundary = adopted as
recommended) · G4 watch session (the point) · red-flag pings only in between.

## Ruling ledger

- **R1–R5:** pending Matt (veto-open; silence past the next session-boundary = adopted as recommended).
- **RL-1 (2026-07-22) — G1 DELIVERED + RATIFIED.** `2026-07-22-replica1-frame-schema-spec.md`
  (`replica-frame/v1`, commit `71dba6b7`): NDJSON one-file-per-fight; self-contained full tick-frames
  (random-access scrub); per-hit `damage` events (the mass-AOE burst renders as N floaters + N deaths
  in one tick); `TelegraphSpec` serialized field-for-field; byte-identical determinism gate (no
  wall-clock fields); zero-derivation renderer contract (§7); 8-gap honest register. **Ratification
  corrections (conductor `DRIFT-CRITIC`):** (i) ref set = gate seeds ×4 {20260722..25} — §4's "6
  seeds" is a slip; and G2 emits ENCOUNTER composition first (5 kits × 2 arms × 4 seeds = **40
  fights**; matched_baseline re-emission is cheap if later wanted); (ii) HG-3 DoT `damage` event
  elevated should→**deliverable-unless-expensive** — caustic-arrow + poison-javazon ARE mismatch
  cells; Matt's autopsy needs the floater story; tick-frame `hp` stays the honorable fallback.
- **RL-2 (2026-07-22) — Shape B AUTHORIZED; frozen-head flag DISSOLVED.** G1's cross-gate flag (the
  in-engine `frame_sink` moves HEAD past `2f43045`) is moot: the ablation gate CLOSED at L-32 with
  the engine untouched; no re-run pends; any future AWARE variant = NEW prereg pinning its own head
  (L-32 design law). The emitter lands as a normal gamora Gate-2 commit on main — observability-only,
  default-off, zero combat-logic change in the same commits. **G2 FIRED** (named gamora, background).
  Veto-open.
- **RL-3 (2026-07-22) — G2 DELIVERED + conductor-verified; synthesis.** Engine `1564e2f` (Shape B
  emitter: 362-line sink module + 98 hook lines in `spatial_engine.py`, observability-only,
  default-off) + collab `40d9b97b` (driver + slice report; 40 frames + manifest UNTRACKED,
  regenerable). Verification: determinism byte-identical (dup-emit filecmp True) · inertness
  bit-equal vs the sealed gate cell (intake |Δ|<1e-9, elapsed 5.6 s, 40/40) · burst PRESENT —
  conductor re-counted BLIND bowazon seed-20260722: **tick 51 = 25 damage / 25 lethal / 25 death in
  one tick**, 56 tick-frames · tests green (spatial 36/36; 210-sweep 0 fail) · per-cell clear-guard
  directions reproduce the gate exactly. **Mechanism finding ACCEPTED (Disc #11):** ref-set kit_ids
  are LABELS on the gate's neutral BC-cells (synthetic martial kits built from canon coordinates) —
  this population has NO elemental DoT, so `dot` events are legitimately 0; the caustic/poison
  aware-clears-more story is engagement-geometry (swarm dwell), and the DoT channel stands
  unit-proven, dormant until a DoT-bearing population enters the window (new prereg territory, not
  an emitter change). HG-3's watch-promise amended accordingly. Deviations RATIFIED: deterministic
  `fight_key` replaces UUID (resolves spec §1-vs-§6 byte-identity tension the right way);
  `threat_tier` honest null. Provenance nuance NOTED: frame headers record `engine_git_hash=2f43045`
  (emission preceded the emitter commit) — honest as the COMBAT-substrate hash (bit-equal proven);
  post-`1564e2f` emissions self-record correctly. **G3 FIRED** (named drax, playback scene) ∥
  **Gate-2 FIRED** (named jack-ryan on `1564e2f`, BLOCK authority). Engine commit unpushed pending
  Gate-2 + Matt push authorization. Veto-open.
- **RL-4 (2026-07-22) — Gate-2 PASS on `1564e2f`** (jack-ryan finding
  `qa/findings/2026-07-22-gate2-replica1-frame-emitter.md`, commit `c6eee0e0`; no WARN, no BLOCK).
  Zero combat-logic change confirmed by full line review (+98 diff: every added line
  sink-closure/None-guard/pure-read/comment; on_hit blocks sit post-mutation); inertness proven by
  construction (14/14 `_frame_sink` refs guarded; corroborates gamora's bit-equal attestation);
  determinism scan clean (no wall-clock/uuid/random; `_finite()` fails loud); seam-fit idiomatic;
  210-sweep independently re-run green. Two INFO notes only (RL-3 ratified deviations logged;
  harmless dead-store `:4819` — tidy on next touch, no re-commit). **Engine `1564e2f`
  Gate-2-CLEARED; engine push queued on Matt authorization** (not load-bearing for G4 — frames are
  local). G3 remains in flight.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22.
