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

- *(open — R1–R5 pending Matt; G1 fired at charter time.)*

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22.
