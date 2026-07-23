# REPLICA-1 G2 — Trace-Emitter Slice (facts for the conductor)

**Author:** named-gamora (simulation seam), 2026-07-22. **Gate:** G2 of the REPLICA-1 run.
**Authority:** gandalf `RUN-CONDUCTOR`; charter `2026-07-22-replica-1-godot-sim-window-run.md`
(RL-1, RL-2); schema spec `2026-07-22-replica1-frame-schema-spec.md` (`replica-frame/v1`).
This file reports FACTS only (no verdict word — the conductor synthesizes).

## HEAD attestation + site-drift check

- Engine HEAD at build: **`2f43045`** (`2f430457461509378c1bd0c20425e6ac7b06a077`) — the SPEC
  grounding-head. No HEAD movement was required to build (Shape B lands as a normal Gate-2 commit on
  this head per RL-2).
- **Site-drift: NONE.** HEAD == the grounding-head the spec's §5 file:line map is anchored to, so
  every cited site is at its cited line. Verified the 8 key sites (design note §1 table): resolver
  per-target loop :2278-2304, flat per-target loop :2316-2328, player cast geo/skill_idx :4106/:4132,
  tick counter/clock :4816/:4817, DoT tick `e.hp -= _dot` :4776, coverage-pressure player-bleed,
  telegraph mint/buffer, `run_spatial_fight` roster build. All match. The §5 map was directly usable.

## What was built (Build 1 — in-engine emitter, Shape B, observability-only)

Engine `simulation/` seam, three artifacts (COMMIT-NEVER-PUSH):
- **NEW** `src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py` — the
  `ReplicaFrameSink` NDJSON writer (`replica-frame/v1`). Header/tick/on_hit/dot/death/telegraph/
  decision/footer methods; full-precision float serialization; fail-loud non-finite guard.
- **MODIFIED** `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — the default-off
  hooks (see below).
- **NEW** `src/reincarnated/simulation/math/replica1-frame-emitter-2026-07-22.md` — design note
  (Discipline #1, authored BEFORE code; frames the semantic choices §3/§4/§5).

Engine hooks (ALL default-off; `frame_sink=None` → byte-identical existing behavior):
- `SpatialFightEngine.__init__` gains `frame_sink=None` → `self._frame_sink` (same default-off
  pattern as `telemetry_writer` / `_trace_decisions` / `emit_telegraphs`).
- `_apply_skill_damage(...)` gains `on_hit=None`, invoked per resolved target INSIDE BOTH per-target
  loops (resolver :2278-2304 + flat :2316-2328) with attacker/target/dmg/delivered/element/hp-after/
  lethal/skill_idx/geometry. Threaded through ALL 5 call sites (player cast + E4 commit + channel +
  mob-attack + ally-attack) via `self._frame_on_hit(_tick_counter, elapsed)`.
- `run()` emits: header at fight start (roster complete, pre-loop); per-tick full frame at loop
  BOTTOM (after all mutation, before the ++); death-by-diff at loop bottom (catches non-hit deaths);
  DoT `damage` event at the DoT tick site (HG-3, geometry="dot"); telegraph field-for-field at the
  mint site; decision-trace (aim-line) at the trace site; footer at fight end.
- `run_spatial_fight(...)` gains `frame_sink=None`; threaded into the engine ctor; asserts
  `n_fights==1` when a sink is present (single-fight → one file per fight; fail-loud on misuse).

**Observability-only proof (Discipline #11):** a `git diff` line-review of `spatial_engine.py`
found NOT ONE line of combat-logic change — every added line is the sink closure, a None-guard, a
pure-read capture, or a comment/docstring. No hook draws RNG or mutates HP/pos/is_alive/energy/any
accumulator. No wall-clock field anywhere (byte-purity, spec §6).

## Semantic choices (Discipline #12, framed — not buried)

1. **Death channel = hit-paired + diff-derived (design note §3).** Hit-kills emit the `death` INLINE
   at the true flip site via the lethal `on_hit`/`dot` (co-occurs with the `damage` floater, spec
   §3.2). All OTHER deaths (non-event DoT, coverage-pressure, boss/ally paths) are caught by a single
   `is_alive` DIFF at loop bottom — same flip-tick timing, complete coverage, robust vs the 7
   scattered mutation sites. A per-tick reported-id `set` prevents double-emit. Deaths are complete
   regardless of source.
2. **`fight_id` OMITTED from the header; `fight_key` substituted (design note §5).** Spec §1 lists
   `fight_id = make_fight_id()`, but that returns `str(uuid.uuid4())` (`spatial_telemetry.py:431`) —
   **non-deterministic**, which would BREAK the spec's own §6 byte-identity determinism gate (the
   load-bearing acceptance criterion). Resolved in favor of the invariant: the header carries the
   deterministic `fight_key = "<kit>__<arm>__<comp>__seed<seed>"` (== the filename) that the renderer
   actually needs; the DB UUID is not needed (the ref set writes no telemetry). If a UUID is ever
   wanted for cross-ref, it must be seeded/derived (`uuid5`) to preserve byte-identity.

## Build 2 — the ref-set emission driver

`agentic_orchestration/gamora/notes/2026-07-22-replica1-emit-refset.py` (collab notes, NOT engine
source; COMMIT-NEVER-PUSH). Reuses the ablation runner's frame machinery VERBATIM (file-path module
load of `2026-07-22-tier3-w3prime-gate.py` → the SAME selection→formation→scenario→cell build), then
filters the pair set to the 5 ref-set kits. Each fight configured IDENTICALLY to its ablation-gate
cell. `player_gather_primitive` OFF, decision traces ON, SEQUENTIAL. corpus.db READ-ONLY.

Ref-set kit → gate cell resolution (frame-derived, not hardcoded):
- `d2-bowazon` → I|high, volley-fan, cell `endgame_bc_ranged_high_flat_dex_none`
- `poe1-kinetic-fusillade` → IV|high, volley-fan, same cell
- `poe1-caustic-arrow` → II|high, swarm, same cell
- `d2-poison-javazon` → I|high, swarm, same cell
- `poe1-frost-blades` → IV|low, volley-fan, cell `endgame_bc_melee_high_flat_dex_none`

Output: `agentic_orchestration/gamora/notes/replica1-frames/` — 40 NDJSON (naming per spec §4) +
`manifest.json` (grid + engine hash + schema_version). **Directory is UNTRACKED (regenerable;
Discipline #3) — NOT staged.**

## Verification gates (results)

1. **Determinism (spec §6 gate):** `--dup-check` emitted `d2-bowazon__blind__encounter__seed20260722`
   TWICE → `filecmp.cmp(shallow=False)` = **True (byte-identical)**. The side-effect-free reader does
   not perturb the RNG; same seed → same fight → same frame bytes.
2. **Inertness:** with `frame_sink=None`, `d2-bowazon/blind/seed20260722` reproduced the sealed
   ablation cell (`I|high|d2-bowazon|encounter|20260722`, seal
   `2026-07-22-aware-fighter-ablation-seal.json`) EXACTLY:
   - intake `10334.753710727` == sealed (bit-equal, |Δ|<1e-9)
   - elapsed_s `5.600000000` == sealed · mobs_killed `40/40` == sealed · winner `player` == sealed.
   Zero combat-logic change confirmed empirically.
3. **Burst spot-check (BLIND bowazon, seed 20260722):** the mass-AOE burst tick found by the trace
   investigation IS PRESENT and renders as required — **tick 51: 25 `damage` events (25 `lethal=true`)
   + 25 `death` events at ONE tick.** The invariant N-lethal-damage == N-death holds at EVERY tick
   across the trace (co-occurrence, spec §3.1/§3.2). Roster = 41 entities (1 player + 40 mobs).
4. **DoT spot-check (caustic-arrow / poison-javazon):** mob HP visibly DECLINES across tick frames —
   shown via the authoritative tick-frame `hp` field (spec HG-3 fallback). BUT **zero `geometry=dot`
   events fired** — see the mechanism finding below. Mob-death pairing is COMPLETE: across all 16
   DoT-labeled traces, every one of the 40 (or 16 on the bricked seed) mob deaths has ≥1 paired
   `damage` event (unpaired = 0). The DoT hook CONTRACT was unit-proven sound (a populated
   `active_effects` DoT → `geometry=dot` damage event + paired death; non-finite guard fails loud) —
   it is correct code, dormant only because the ref-set cells carry no DoT.
5. **Engine test suite:** `simulation/` spatial tests **36/36 PASS**; broader
   spatial/fight/resolver/combat/aura/economy sweep **210 passed, 0 failed** (no regression).

## MECHANISM FINDING (Discipline #11 — for the conductor + drax + Matt)

**The ref-set "kit_ids" are LABELS for the ablation gate's neutral BC-cells, NOT the actual PoE/D2
kit content.** The gate maps each label to a BC-cell (e.g. `poe1-caustic-arrow` →
`endgame_bc_ranged_high_flat_dex_none`) and builds a SYNTHETIC martial player class for that cell via
`_build_martial_player_class` (skills named "Wind Chain A/B/C", geometries point/circle/cone/line/
none, all `element: null`). Consequence: **the DoT-labeled cells carry NO `active_effects` DoT** — 0
tick-slots with ailments across every DoT-labeled trace. So HG-3's `geometry=dot` event legitimately
never fires: there is no DoT in the ref-set-as-configured. The caustic-arrow / poison-javazon HP
decline the autopsy wants Matt to SEE is real and rendered — but it arrives via discrete `circle`/
`point` per-hit `damage` events (fast-cadence martial casts), not DoT ticks. The tick-frame `hp`
renders it faithfully either way.

Implication for G3/G4: the reference set faithfully shows the ablation gate's ENGAGEMENT-GEOMETRY
autopsy (blind-clears-vs-aware-bricks on direct kits; aware-clears-more on the swarm-formation
"DoT-labeled" cells) — which is what the gate actually measured. It does NOT show elemental DoT
floaters, because the gate cells have no elemental DoT. If Matt wants to autopsy REAL caustic-arrow
DoT visuals, that requires emitting a DIFFERENT cell population (real per-kit content with populated
`active_effects`), a NEW prereg pinning its own head — not a change to this emitter (the DoT hook is
already built + proven; it would fire on such content). Flagged, not patched.

## 40-fight emission stats

- 40 files, **21.38 MB total**, mean **521.9 KB/fight**, file range 428–571 KB.
- Ticks: min 43, max 109, mean 62.2. Total `damage` events **1406**; `death` events **1416**
  (1406 mob + ~10 player deaths on bricked seeds); `dot` events **0** (mechanism finding above);
  telegraph events 0 (ref-set kits are player-offense-led — no mob area-attack resolved);
  decision events = one per player decision tick (aim-line overlay populated).
- Per kit×arm outcome (player=clear, monster=brick), all 4 seeds each:
  - `d2-bowazon`: blind 4-clear / aware 4-brick · `poe1-kinetic-fusillade`: blind 4-clear / aware 4-brick
  - `poe1-caustic-arrow`: blind 3-clear+1-brick / aware 4-clear · `d2-poison-javazon`: blind 3+1 / aware 4-clear
  - `poe1-frost-blades`: blind 4-clear / aware 4-clear (aware slower: 109 vs 75 ticks)
  This reproduces the gate's clear-guard mismatch directions exactly.

## Artifact paths (absolute)

- Emitter sink: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py`
- Engine hooks: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`
- Design note: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/replica1-frame-emitter-2026-07-22.md`
- Driver: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-replica1-emit-refset.py`
- Frames (UNTRACKED): `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/replica1-frames/` (40 NDJSON + manifest.json)
- This slice report: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-22-replica1-g2-emitter-slice.md`

## Deviations from spec letter (Discipline #11 register)

- **`fight_id` UUID omitted** → `fight_key` deterministic tuple substituted (spec §1 vs §6 tension
  resolved for byte-identity; see semantic choice #2). No renderer impact.
- **HG-3 DoT `damage` event built + proven but dormant** on the ref set (no DoT in the neutral-cell
  content; mechanism finding). Deliverable-unless-expensive per RL-1(ii) was satisfied: the hook is
  cheap + built; it has no DoT to emit on THIS cell population.
- **`threat_tier` = null** in the header roster (not retained on `SpatialEntity`; design note §7).
  Honest null, not fabricated. Renderer keys visuals off `element`/`geometry` per spec §7.
