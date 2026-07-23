# REPLICA-1 G3 — Godot Sim-Window Playback Scene (facts for the conductor)

**Author:** named-drax (presentation seam), 2026-07-22. **Gate:** G3 of the REPLICA-1 run.
**Authority:** gandalf `RUN-CONDUCTOR`; charter `2026-07-22-replica-1-godot-sim-window-run.md`
(RL-1–RL-3); schema spec `2026-07-22-replica1-frame-schema-spec.md` (`replica-frame/v1`, §7
zero-derivation renderer LAW). Upstream data: gamora G2 slice
`2026-07-22-replica1-g2-emitter-slice.md` (40 NDJSON fights + manifest, UNTRACKED/regenerable).
This file reports FACTS only (no verdict word — the conductor synthesizes).

## What was built (G3 — the playback scene; a WINDOW, not a port)

Godot 4.6.3-stable / Forward+ (Metal). A SEPARATE flat-arena scene at SIM coordinates
(1 sim m = 1 Godot m) — it does NOT touch the ravine level (whose geometry would falsify
positions). The scene DESERIALIZES the sim's emitted per-tick frames and DERIVES NOTHING:
no damage roll, no target choice, no cooldown/energy/cadence, no death decision, no
hit/miss/collision/dodge. The ONLY derivation is pose interpolation between tick N and N+1
for display smoothness (spec §7 MAY-list). Exactness is by construction — there is no second
combat implementation.

Repo `~/Games/reincarnated-godot/` — **commit `90d79c5`** (COMMIT-NEVER-PUSH; repo is 7 ahead
of origin/main, unpushed pending conductor/Matt push authorization). 7 files, +1468 lines:

- `scripts/replica_trace.gd` — `ReplicaTrace` loader/model. Pure deserialization of one
  NDJSON fight: header (roster + arena frame) + per-tick full frames (indexed for
  random-access seek) + events grouped by tick. Zero gameplay derivation.
- `scripts/replica_playback.gd` — scene root (one-script procedural build, same pattern as
  the existing `render_arena_room.gd`). Builds: flat 44×44 grid arena (4 m/8 m gridlines +
  origin E/N axis markers, distance aid); proxy primitives (player = cyan capsule + facing
  nub; mobs = cylinders scaled by `entity_radius_m`); HP bars synced from the tick-frame
  `hp` field (authoritative — DoT-style drain renders here even without discrete events);
  damage floaters (the delivered number, tinted by the event's `element`); death flashes +
  corpse states (flatten/sink at the `death` event); commit-state rings (tint while
  committing/channeling); telegraph danger-zones (circle/cone/line, pulse through wind-up
  then vanish); decision-trace aim-line overlay (player → chosen target, toggleable);
  orbit camera; full scrubber; fight picker + A/B swap.
- `scenes/replica_playback.tscn` — minimal scene (root Node3D + script).
- `scripts/run_replica_mp4.sh` — MP4 fallback (charter §4) via Godot `--write-movie` +
  ffmpeg. PROVEN end-to-end.
- `scripts/check_replica_all_fights.gd` + `scripts/check_replica_controls.gd` — reusable
  headless regression verifies (used for verification 3 + 4 below).

## HOW MATT WATCHES (exact launch steps — G4)

### Live playback (the point — interactive, on the Mac with a window)
1. Open a terminal.
2. Launch the scene (no editor needed):
   ```
   /Applications/Godot.app/Contents/MacOS/Godot --path ~/Games/reincarnated-godot \
       scenes/replica_playback.tscn
   ```
   It opens on BLIND bowazon seed 20260722 by default. To start on a specific fight, append
   `-- --fight replica-<kit>__<arm>__encounter__seed<seed>.ndjson` (bare `--` then the arg).
   If the frames dir ever moves, override with `-- --frames-dir <absolute path>`.
3. On screen: top-left shows the fight metadata (`FIGHT n/40  kit | arm=… seed=… | encounter |
   40 mobs (+1 player) | N ticks / N.Ns`) and the live clock line (`tick / total  sim-clock  speed
   PLAYING|PAUSED  alive  aim/tele state`). A controls panel (top) and a seek bar (bottom) are drawn.

**Every control (keyboard + mouse):**
- `SPACE` — play / pause
- `→` / `←` — single-tick step forward / back (forces pause)
- `↑` / `↓` — speed up / down through **0.25× · 0.5× · 1× · 2× · 4×** (1× = real time = 10 ticks/s)
- **seek bar** (bottom, drag) — jump to any tick (random-access; frames are self-contained)
- `5` — convenience jump straight to **burst tick 51**
- `[` / `]` — previous / next fight (cycles all 40 in the manifest)
- `B` / `N` — A/B quick-swap to **B**LIND / aware(**N**) of the SAME kit+seed (the autopsy pair)
- `A` — toggle the decision-trace **aim-line** overlay (player → chosen target; the AWARE detour tell)
- `T` — toggle **telegraph** danger-zones (none fire on this ref set — see gaps)
- `R` — restart the current fight from tick 0
- **right-drag** — orbit the camera · **mouse wheel** — zoom · `H` — toggle the help panel · `ESC` — quit

Recommended autopsy path: start on bowazon (default), press `5` to see the BLIND burst clear,
then press `N` to swap to AWARE and watch the same kit+seed brick (aim-line `A` on shows the detour).

### MP4 fallback (charter §4 — if live playback ever stalls; also proven now)
```
bash ~/Games/reincarnated-godot/scripts/run_replica_mp4.sh
```
Renders bowazon BLIND then AWARE (seed 20260722) to
`~/Games/reincarnated-godot/harness_logs/replica_mp4_2026-07-22/*.mp4` (git-ignored). Pass fight
basenames as args to render others. Same `replica_playback.gd` scene drives both — no second
implementation.

## Verification results (1–5)

1. **BLIND bowazon seed20260722 — burst + full-clear:** tick 51 renders **25 damage floaters +
   25 death-flashes in ONE tick** (green = the `wind` element carried by the damage/death events);
   fight full-clears by tick 55 (5.5 s, 0 mobs alive at final frame). Confirmed at the loader level
   (`check_replica_all_fights.gd`: tick51 damage=25/death=25, final mobs_alive=0) AND by Metal eye
   capture (the green death-flash mass + "150" delivered-damage floaters over the cluster).
2. **AWARE same kit+seed — bricks, visibly different:** no mass-clear burst; mobs dwell-clump around
   the player; **player DIES**; 12 mobs still alive at final tick 54. Confirmed at the loader level
   (final mobs_alive=12, player_alive=false) AND by Metal eye capture (swarm clumped on a live player,
   trickle floaters, no burst) — the gate direction (aware bricks on bowazon) is visibly reproduced.
3. **All 40 manifest entries load + play, ZERO parse errors:** `check_replica_all_fights.gd` →
   40/40 loaded clean, total parse_errors=0, total_ticks=2490, damage_events=1406, death_events=1416
   (matches the G2 slice stats exactly).
4. **Scrubber:** `check_replica_controls.gd` → step forces pause · step +1/−1 math correct
   (10→11→10) · speed range 0.25×..4× present · seek-to-tick-51 lands on tick 51 · A/B swap
   blind→aware preserves kit+seed · next-fight cycles. ALL PASS.
5. **Headless smoke:** the scene loads + auto-plays to the final tick with **0 errors, 0 warnings,
   0 leaked instances** (verified on BLIND bowazon 56 ticks AND frost-blades AWARE 109 ticks —
   the longest fight). Metal capture path also confirmed (3 eye-verify PNGs + 1 MP4 rendered clean).

## Schema gaps found (reported, NOT patched — spec §7 discipline)

These are the SAME facts gamora's G2 slice already flagged (mechanism finding); confirming they
manifest on the render side and are shown as sim reality, not papered over:

- **Roster `element` is null on every entity** (player + all 40 mobs) across all 40 fights. The
  sim's authoritative element channel is the per-hit `damage` event (`element:"wind"` etc.), which
  the renderer DOES consume (floater + death-flash tint). Mob proxy body color therefore falls back
  to a stable per-entity-id hash hue for legibility — this is a DISPLAY key only (spec §7 permits
  proxy color choice), NOT a fabricated roster element. If a typed-element roster population ever
  enters the window, the proxies would color by roster element automatically (the code checks roster
  element first). **No emitter change requested** — this is the neutral-BC-cell content the gate
  measured; showing null-element martial casts is faithful.
- **`dot` events = 0 and `telegraph` events = 0** on this ref set (per G2: neutral cells carry no
  `active_effects` DoT; player-offense-led → no mob area-attack resolves). DoT-style HP drain still
  renders faithfully via the authoritative tick-frame `hp` (spec HG-3 fallback). The renderer's
  DoT-floater path (keys off a `geometry:"dot"` damage event) and the telegraph danger-zone path are
  BUILT and will fire if a DoT-bearing / area-attack population is ever emitted — untested-LIVE only
  because the ref set contains none (new-prereg territory per RL-3, not a G3 change).

No NEW schema gap beyond what G2 already registered. The frame schema carried every render-needed
datum; nothing was missing that forced a compute.

## Deviations from the brief (Discipline #11 register)

- **Element-color keying adapted to the null-roster-element reality.** The brief said "mobs keyed by
  element color". Since roster element is uniformly null (G2 mechanism finding), mob BODY color uses
  a stable id-hash hue (legibility), while the element the sim DOES emit (on damage/death events) is
  rendered as floater/death-flash tint. This honors "render what's there; fabricate nothing" — the
  window shows element exactly where the sim provides it. Flagged, not silently substituted.
- **Two extra reusable verify harnesses committed** (`check_replica_all_fights.gd`,
  `check_replica_controls.gd`) beyond the scene itself — they ARE the evidence for verifications 3+4
  and match the repo's `check_*` convention. Not scope creep; they are the verification instruments.
- **`project.godot` auto-strip reverted, not committed.** Godot stripped the `[rendering]` LOD line
  on launch (known repo behavior); `git restore project.godot` applied per the repo's off-screen
  render rule. Not a G3 change.
- **No `// TODO(drax)` engine-gap debt.** Nothing on the render side compensates for an engine gap;
  the null-element / no-DoT facts are sim reality shown faithfully (charter §0), not overrides.

## Artifact paths (absolute)

- Loader: `/Users/admin/Games/reincarnated-godot/scripts/replica_trace.gd`
- Scene script: `/Users/admin/Games/reincarnated-godot/scripts/replica_playback.gd`
- Scene: `/Users/admin/Games/reincarnated-godot/scenes/replica_playback.tscn`
- MP4 fallback harness: `/Users/admin/Games/reincarnated-godot/scripts/run_replica_mp4.sh`
- Verifies: `/Users/admin/Games/reincarnated-godot/scripts/check_replica_all_fights.gd`,
  `/Users/admin/Games/reincarnated-godot/scripts/check_replica_controls.gd`
- AGENT_STATE entry: `/Users/admin/Games/reincarnated-godot/AGENT_STATE.md` (2026-07-22 section)
- This slice report:
  `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-07-22-replica1-g3-playback-slice.md`
- Godot commit: `90d79c5` (unpushed)
