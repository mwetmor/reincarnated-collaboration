# AMBIENT-REFIT fold-in — Matt directive (LR/presentation session, 2026-07-30)

> **Authorization:** Matt, in-session: *"Ok, I like it… Can we fold in the particle refit?"* — after
> approving the SCENEWRIGHT recipe (2026-07-30). Matt also declared session intent: the baton is
> nearly ready; the presentation session begins preparing its work here. Reference watch he is
> reviewing: `reincarnated-godot/tmp/wr2/wr3_after_pre_boss_B_74000802.mp4`, which he is
> *"very ready to see fully baked."*
> **Conductor for this cell:** gandalf (LR/presentation session). This is presentation-seam work
> Matt allocated here directly; it does not touch WR3 run conduction (charter session). Recorded
> so the charter session's ledger can cross-reference; zero WR1/WR2/WR3 ruling numbers consumed.

## The cell (drax): AMB-REFIT

Discharges the OWED item drax named twice (WR1-ROOMS §7.3; WR2 after-baton render note ~line 201):
the promoted ambient's emission extents are authored for the 17.5 m race stage; in the 37.5 m room
it dresses the middle and not the edges (0.50% vs 3.02% in-room coverage, ratio = 17.5²/37.5²).

**Matt's design intent (the acceptance standard, his words):** lessen the ambient's prominence in
the bright center, and use that lessened center as the sample extended across the room generally —
today it is distracting in the center and relatively absent outside it.

**Recipe (Matt-approved):**
1. Emission extents ×k (k = 37.5/17.5 = 2.143) in the `vfx/ambient/pp/*.tres` process materials,
   **counts HELD, sprite scale HELD** — the per-area dilution to ~0.22× IS the lessening; no
   sample-then-tile second step needed. Count trim only after the eye sees it.
2. `L5_CentrePool` quieted specifically (count/albedo) until the lit center matches the room-wide
   read — prominence is density × illumination; quiet the one layer living in the bright spot.
3. FORBIDDEN: scaling the `GPUParticles3D` node (2.14× sprites — drax's own prior refusal stands).

**Verification riders:** VOID-1 re-fires WITH the leak control (extents now approach walls; zeros
count only if the control still bleeds) · LSTAT-2 stage datum stationary · M-EYE: verdict
deliverable is MOTION — the WR3 watch re-rendered same seed/leg/tier/arm/camera with the refit
ambient in the room the fight renders in, plus before/after plates.

## Scope 2 (same cell, Matt follow-up directive): overhead AI-STATE tags on enemy combatants

**Matt verbatim:** *"I think maybe the only thing missing is the AI state that we are planning to
put above the enemy combatant NPCs."*

- Billboard state tag above each ENEMY combatant, driven ONLY from what the trace states — never
  an invented label. Sources on `replica-frame/v1` (+WR3 additions): `commit_state` (idle /
  wind-up / recovery once Mechanism C2 emits them), movement `intent`, `decision` events,
  `telegraph` (tell-in-progress). Missing/dark fields print as absent, not as a default state —
  the drax §0 discipline (a missing conditional key and a zero are different statements).
- Presentation: short word + color chip, legible at 720p from the `arena_full` camera stand-off;
  consistent anchor height above the capsule; declared an INSTRUMENT OVERLAY (owner-eye
  legibility layer), not final game UI — same class as the existing frame banners/readouts.
- Player gets NO tag in this pass (Matt named enemy combatants only).

**Guards:** traces READ-ONLY · race-lineage `tmp/vmur*` untouched (evidence) · frozen
`kit_replica_level.gd` discipline per WR1-ROOMS §7.1 · collision check at cell start (`git status`
on reincarnated-godot; HALT if another cell's uncommitted work sits on ambient/playback surfaces) ·
godot repo commits local, NOT pushed (conductor pushes after Matt's eye) · presentation-layer
change ONLY — zero fight/trace semantics.

## Scope 3 (follow-on cell CAM-LOCK — Matt directive 2026-07-30; relay-on-return, SendMessage unavailable)

**Matt:** when the player moves across the map, the camera must be locked onto the player's
motion, ARPG-style. Confirmed grammar (conductor, genre-cited): **HARD translation lock** —
player pinned at screen anchor, fixed offset/pitch/zoom, ZERO easing/lag/deadzone (D2/D3/D4,
PoE 1/2, Grim Dawn, Last Epoch). No follow-cam smoothing: threat assessment is radial and cursor
aim is screen-relative; easing breaks both.

- New playback mode `--cam player_lock`: camera transform authored frame-by-frame from the
  player's trace position + fixed offset vector; genre-typical pitch (~45–55°, drax picks against
  the room's read); zoom fixed at a distance where the 12 m nova footprint fits the frame with
  margin. Renders the SAME watch (seed 74000802, same leg/tier/arm) as a variant alongside the
  judge-cam deliverable — two cameras, two jobs (instrument vs game-feel; `arena_full` remains
  the grading camera of record).
- **Declared consequence:** wall-adjacent play frames past the wall into void. Genre-native
  answer adopted: deliberate darkness beyond the wall line (the Diablo dungeon reading). VOID-1
  polices unintended light only; deliberate black passes by construction. A cheap beyond-wall
  darkness treatment is in scope if needed to sell it; a full outer-world dress is NOT.
- Fires as CAM-LOCK immediately on AMB-REFIT's return (same surfaces, single-writer — no parallel
  launch), rendering with the refit ambient + AI-state tags already in place.

### Scope-3 amendment (Matt directive, same day): operands are MEASURED, not genre defaults

Matt's sharpening: the locked camera must reproduce the decision surface he experienced in the GD
play session ("what's within X meters of me in every direction"), exactly. GD engine constants are
not extractable and GD's zoom is player-controlled anyway — so the fixture's EFFECTIVE camera is
being measured from Matt's own footage by cell **GAL-CAM** (galadriel, in flight, parallel-safe:
read-only, no godot writes): pitch via the nova-ring ellipse (known-radius ground circle, the
GAL-3 anchor), px/m from the two banked anchors, the visible-meters box around the player's
measured screen anchor, zoom band if it drifted. **CAM-LOCK consumes GAL-CAM's note as its
camera operands** (match the visible-ground box, not an offset/pitch guess); genre-typical pitch
in the scope above is superseded by the measurement where the measurement is clean.

## LANDING — AMB-REFIT ✓ (2026-07-30; note `drax/notes/2026-07-30-amb-refit.md` `020bb78e`; godot `8c6de28` LOCAL)

- **Complaint measured before anything moved (new instrument AMB-EVEN, VOID-1's mask convention):**
  Matt's sentence was UNDERSTATED — rings 2–4 read exactly 0.000%; 77.4% of the room received not
  one ambient pixel. After: 5.030%→1.510% ring 0 (the lessening), 0.000%→0.608%/0.100% rings 2–3
  (the extension). Recipe held to the letter: extents ×2.142857 X/Z only (Y held — per-AREA 0.2178),
  counts/sprite/node scale HELD; L5 quieted ×0.3968, magnitude SOLVED by ablation, not guessed.
- **VOID-1 re-fired WITH control:** AFTER 0 px CONTAINED; 26 m-extents control 566 px LEAK — the
  zero counts. LSTAT-2 +0.068%; the 4,521 px stage delta proven NOT the cell's (reverted-vs-applied
  render diff 0/921,600 px — feeds the non-determinism flag below).
- **Scope-2 refusal ADOPTED (conductor):** trace `decision` records carry NO subject field —
  `intent: evade` on a boss-targeted record is the PLAYER's evade; painting it on the boss renders
  the inverse of the fight. Enemy tags ship from enemy-stated data only; player-intent data shows
  as `player target` in player cyan. Also: first render DISCARDED for a two-statements-one-slot
  bug (TELL overwrote the commit word on the exact tell-during-commit window WR3 exists to show);
  fixed as a second slot. Both refusals are the discipline working.
- **Watch deliverable:** `reincarnated-godot/tmp/ambfit/ambfit_wr3_after_pre_boss_B_74000802.mp4`
  (same seed/leg/tier/arm/camera; original byte-untouched, sha `910063d1…`).
- **⚑ FORK ROUTED TO MATT (drax correctly refused to take it):** ring 4 (outer 5.25 m wall band)
  is still 0.000% — inherited arithmetic: the ambient was authored at 72% fill of its own stage and
  ×k preserves the fraction exactly. (A) keep 72% — walls stay clean/dark, torches own them;
  (B) raise fill ~90% — sparse coverage into the wall band, "across the room generally" in full.
  Conductor lean: B — a field that stops 5 m short of the walls reads as an invisible fence once
  seen. Matt rules at the eye.
- **⚑ FLAG (not ruled):** L7 stage frozen in CODE but not in RENDER — byte-stable within a
  session, drifts across days with no code change. PC-LIGHT settle-variance axis lineage
  (PROVISION-CAL §2.9: settle-count variance is the discriminating axis, not byte-identity).
  Routed: joint galadriel+drax instrument diagnosis, wave tail.
- **CAM-LOCK:** single-writer now free; HOLDS for GAL-CAM's operands (in flight), then fires.

## Scope 4 (cell AMB-RISE — Matt directives 2026-07-30, post-landing review)

- **Wall-band fork RULED (Matt): Option A STANDS "so far"** — current fill fraction accepted; the
  outer band stays dark. Fork remains re-openable at his eye; no fill change ships.
- **Matt directive (verbatim intent):** make the ambient particles *"perpetually rise in the same
  way that the torch flame VFX does."*
- **Recipe:** sample the rise character (initial +Y velocity, variance, damping, lifetime/fade
  feel) FROM the frozen torch flame VFX — parameters copied as reference, flame sources untouched
  (they are Matt-verdicted perfect, WR1-ROOMS §7.1 freeze discipline). Apply per layer with seam
  judgment: embers/motes carry the full rise; ground mist may take a gentler lift if a full
  fire-rise reads as steam — drax judges at the eye, declares per layer. Perpetual = continuous
  emission, fade-in at floor / fade-out at height, no pop-in. AMB-REFIT's extents/counts/L5
  quieting HELD (Matt-accepted state).
- **Riders:** AMB-EVEN re-run (rising particles shift ring residency — declare the delta, expect
  it) · VOID-1 with control (height changes the wall-adjacency picture) · LSTAT-2 · M-EYE motion:
  verdict deliverable is a SHORT room-ambient clip (cheap iteration on motion character), NOT a
  full watch re-render — the next full watch (CAM-LOCK) carries the accepted rise.
- **Sequencing:** AMB-RISE takes the godot tree now; CAM-LOCK queues behind it (needs GAL-CAM's
  operands regardless, still in flight).

## LANDING — AMB-RISE ✓ (2026-07-30; note `drax/notes/2026-07-30-amb-rise.md` `59eb9032`; godot `45b51bf` LOCAL atop `8c6de28`)

- **The complaint was understated again: the layers were not rising at all.** Measured pre-rise
  vertical travel 0.000–0.046 m over 5–6.5 s lives — velocity exhausted in 0.13–0.40 s, then
  parked for 93–98% of life. Layers named *drift* and *mist*; arithmetic said *parked*. After:
  0.25–1.78 m per layer, every layer below the torch embers' Matt-verdicted 4.60 m precedent.
- **Recipe = the flame's grammar as arithmetic, validated by inversion** (solving the flame's own
  (h, T) returns its authored constants: 0.549/1.047 vs 0.550/1.050). Rise = positive Y gravity
  mostly cancelling drag, not an impulse. ONLY motion parameters moved; in `gravity` only Y —
  extents/counts/scale/albedo/lifetime all HELD (Matt-accepted state; holding lifetime holds
  density by construction). Load-bearing edit: `direction` — the old vectors WERE the draught
  (layers pointed sideways); now (0,1,0) with the draught surviving as lateral gravity lean.
- **Per-layer judgment declared:** L1/L6 full rise (1.78/1.60 m); L3 budget-limited 0.71 m (emits
  high already); L2 mist GENTLER LIFT 0.25 m (half-metre sprites at ash speed = boiler room, not
  crypt — the brief's named risk, real); L5 gentlest +0.27 m for a MEASURED reason: its 4.5 m
  emission SPHERE already reached 3.80 m — over the 3.17 m wall — before this cell (AMB-REFIT's
  "Y held" could never apply to a sphere; inherited, now on record).
- **⚑ R-10 SUSPENDED, NOT REPEALED (routed to Matt's eye):** `vh_brief_ambient.gd` enforces
  `flatness = 1.0 # (R-10)` — standing derived law: "ambient volume belongs on the ground plane;
  at −50° a rise smears against the floor." Matt's directive negates it; executed knowingly and
  declared. R-10's falsifiable objection is exactly what the verdict clip tests. His eye rules.
- **⚑ Rises land at 36–73% of design arithmetic** (held `lifetime_randomness` shortens effective
  lives). NOT compensated, deliberately — the eye rules before velocities are scaled to a number.
  If Matt wants more: one constant per layer.
- **Instrument discipline:** AMB-RISE-1 (image-correlation velocity) DISCARDED by its own torch
  control (0.02 vs 0.74 m/s — steady-state envelope is stationary; it measured the shape, not the
  particles; kept as the record of a rejected instrument). AMB-RISE-2 (`capture_aabb()` probe)
  passed its flame control at 3.3% and measured the flames untouched to four decimals — the frozen
  VFX proven untouched by MEASUREMENT, not only hash.
- **Riders:** AMB-EVEN shift declared not tuned (rings 1–2 gain, ring 0 falls — no
  re-concentration; ring 4 stays 0.000%, Option A exactly as ruled; sitting-noise bound declared) ·
  VOID-1 0 px CONTAINED with a THIS-axis control (v0 ×6 → 9 px LEAK over the wall — the zero
  counts) · LSTAT-2 Δ 0.000000, **and the L7 stage reproduced bit-for-bit across a day boundary —
  narrows AMB-REFIT's non-determinism flag: not a simple per-day rewrite.**
- **Verdict deliverables (M-EYE, motion):** `tmp/ambrise/clips/AMBRISE_eyelevel_BEFORE_top_AFTER_bottom.mp4`
  (18 s, the one to watch) · judge-cam twin · `tmp/ambrise/plates/PLATE_streaks_ZOOM.png` (fastest
  read: round dots before, streaks after).
- **CAM-LOCK now fully unblocked** (godot tree free + GAL-CAM operands landed) — fires next,
  carrying the rise + refit + AI-state tags into the full watch.

## LANDING — GAL-CAM ✓ (2026-07-30; note `galadriel/notes/2026-07-30-gal-cam-fixture-camera.md`
`88170009`; operands `galadriel/captures/2026-07-30-gal-cam/godot-spec.json`)

- **Headline overturns a shared assumption: the GD fixture camera is a PINHOLE, not orthographic**
  (horizontal ground scale grows 55% top→bottom; ortho rejected at every measured row, 1,582 frame
  pairs/row, 73 windows across 1h53m). Pitch 52.96° [45.3–62.3]; player-row scale 54.47 px/m;
  player anchor (962, 595) = +55 px below centre; zoom NO-DRIFT (±10% floor).
- **The decision surface is ASYMMETRIC: ±17.6 m horizontal · +15.2 m far / −7.0 m near** — and
  **the 12 m nova does not fit inside it**: ~30% of the ring's circumference (the down-screen arc)
  was never on Matt's display, under the skill bar then off-frame. The referent player answered
  novas partially blind on the near side. **Sharpens the perception-clamp flag already routed to
  the WR3 ledger** — the clamp is not a disk, it is this measured asymmetric box.
- **GAL-3 SUPERSESSION (provenance, verdicts intact):** the banked px/m anchors were orthographic
  values; death-2 re-derives **1.390 m (was 1.257, +10.5%)** — still 23% inside the ≤1.804 m
  window M-12b rests on and inside GAL-3's own [0.96, 1.61] band. **Every threshold verdict
  survives.** ROUTED to the charter session via this pushed bank (touches the R-WR1-13 / G-B
  probe operand's provenance, not its verdict; galadriel per discipline did not touch the hive
  log). Charter session disposes whether the grading record gains an erratum line.
- **CAM-LOCK operand law:** the §4 decision-surface framing is assumption-free — CAM-LOCK frames
  to the measured visible-meters box; the pinhole family (godot-spec.json arrays, centre pitch
  52.95°) sets the projection; least-settled operand is the FAR extent (pinhole-vs-ortho moves it
  48%) — CAM-LOCK verifies framing against the `surface-overlay.jpg` evidence, not against a
  single trusted number. Discipline note carried: the 2% pitch-insensitivity from GAL-3 does NOT
  transfer (that was a ratio; this is not).
- Two instrument failures committed-not-hidden (trail-riding blobs; a self-failed falsifiability
  check); three CANNOT-ANSWER rows with leverage quantified. The Mirror behaving as built.

**Answered for the record (Matt's three questions):** camera/perception stats are NOT in the
battle sim (no camera, no perception model — the pilot reacts to trace-level truth); adding the
camera scene-side CANNOT move geometry (trace-driven playback, view transform only, no feedback
path). **Flagged to the WR3 charter session, not ruled here:** the sim-side twin — a
perception-radius clamp on the pilot (Mechanism K reacting only to screen-visible events at the
measured camera) is a fidelity refinement candidate; today's pilot is better-informed than the
referent player was. Mechanism-K territory ⇒ that run's ledger decides.
