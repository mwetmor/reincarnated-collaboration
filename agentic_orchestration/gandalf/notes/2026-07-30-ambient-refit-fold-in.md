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

## Scope 4 VERDICT + Scope 5 (cell AMB-HUE — Matt directives 2026-07-30, post-rise review)

- **RISE VERDICT (Matt, verbatim): "rise is perfect."** Consequences, ruled by the conductor from
  that eye-verdict: (a) the 36–73% design-arithmetic shortfall is CLOSED — no velocity boost; the
  shipped magnitude IS the accepted state; (b) **R-10 falls for the ambient layers** — its
  falsifiable objection ("a rise at −50° smears against the floor") was put in front of the owner's
  eye and did not manifest. R-10 is AMENDED, not deleted: the ground-plane law survives as lineage
  with an eye-dated exception for ambient (`vh_brief_ambient.gd` contract comment amended by drax
  in the AMB-HUE cell — the seam that executed the suspension closes it, on the conductor's ruling,
  veto-open to Matt as all rulings are).
- **Matt directive (verbatim): change the color to "dark purple, rising into a lighter purple-blue
  hue."** Colors were HELD in AMB-REFIT/AMB-RISE as Matt-accepted state; Matt has now explicitly
  reopened them. Design note (conductor): under the rise, particle AGE ≈ HEIGHT — so a
  color-over-lifetime ramp (dark purple at birth/floor → lighter purple-blue at death/top) IS the
  height gradient Matt described, with no positional shader needed. Thematically this moves the
  ambient from fire-adjacent warmth into the arcane/necrotic register — correct for the crypt and
  for the *Reap. Die. Rise.* death-faith frame — and buys color separation from the frozen warm
  torch flames for free (ambient legible AS ambient, flame legible AS flame; Diablo dungeons run
  exactly this cool-room/warm-source split).
- **Recipe:** per-layer `color` + `color_ramp` (gradient over lifetime) in `vfx/ambient/pp/*.tres`
  — dark purple base, lighter purple-blue at ramp end; **existing alpha keys PRESERVED to the
  digit** (the 0→visible→0 ramps are the no-pop guarantee); motion parameters, extents, counts,
  sprite scales, lifetimes ALL HELD (rise is Matt-verdicted perfect — nothing else moves). Exact
  hues are drax's to pick against the room's read at the eye; Matt's sentence is the standard.
  Per-layer judgment declared as always (L6 embers stop being fire-born and become arcane motes —
  declare it; if any layer's hue fights the torch-glow band, declare that too).
- **Riders:** M-EYE short room clip (cheap iteration — same pattern as AMB-RISE; the next full
  watch carries the accepted hue) · LSTAT-2 · VOID-1 re-fire only if luma moved materially
  (purple-blue at higher value could change wall-adjacency luma; drax judges, declares) ·
  AMB-EVEN only if the mask convention keys on hue (declare either way).
- **Sequencing:** CAM-LOCK holds the godot tree (in flight; no relay path — SendMessage
  unavailable on this host). AMB-HUE fires on CAM-LOCK's return. CAM-LOCK's watch therefore
  carries the WARM ambient — declared, expected; once Matt verdicts the hue clip, the player_lock
  re-render with accepted hue is mechanical (scripted harness, same trace).

## LANDING — CAM-LOCK ✓ (2026-07-30; note `drax/notes/2026-07-30-cam-lock.md` `4d167f4a`; godot `3449169` LOCAL, ahead 3)

- **`--cam player_lock` shipped: HARD translation lock** — camera = player ground position + a
  constant vector, evaluated on the same interpolated position the proxy draws at, same frame;
  no spring/deadzone/look-ahead. Full watch rendered (same seed/leg/tier/arm) carrying refit +
  risen ambient + AI-state tags.
- **Framing verdict: MATCH against GAL-CAM's own data, not against trusted numbers.** Ray-cast
  from the actual Camera3D onto the floor vs `rings.json`/`surface.json`: anchor error
  (−0.0004, −0.0009) px @1080p; decision box within 0.03 m on all four sides (FAR — the
  least-settled operand — +15.211 vs +15.244); 12 ring-row checks 1.6–12 m, worst on-frame
  residual 0.69 px = 0.012 m of ground. Depth derived from the measured scale field
  (z = focal/g_x = 34.8165 m) per GAL-CAM §6's coupled-pair warning — then reproduced three of
  galadriel's independent rig numbers to 0.01–0.04% with none used as inputs.
- **Declared non-honors:** bearing is NOT measurable (GD's world is authored TO its camera) —
  judge camera's 47° adopted so both watches share orientation · 12 m nova does NOT fit, kept
  (fidelity, per charter) · beyond-wall darkness treatment NOT built — measured unnecessary
  (worst-case wall clearance 0.500 m at tick 858; beyond-wall already pure black by construction).
- **⚑ TWO ITEMS AT MATT'S EYE:** (1) captions rendered 2.13× their accepted screen size under the
  new lens; HELD to accepted pixels via derived k=0.46959 (geometry deliberately not scaled);
  plate `PLATE_tags_worldheld_vs_screenheld.jpg`; reversal is one constant. (2) the inherited
  frame banner eats the bottom ~28% of frame — which under player_lock is the NEAR decision
  surface (the −7.0 m band). Drax refused as out of scope, correctly. Conductor note: GAL-CAM
  measured the referent's OWN skill bar occluding the near arc — so a bottom occlusion is
  arguably period-correct — but the banner is an instrument overlay, not a skill bar; whether it
  slims, moves, or stands under player_lock is Matt's call at the watch.
- **⚑ Non-determinism flag NARROWED to closure-shape:** null test (identical script, two
  launches) 8,341–8,658 px/frame speckle vs reverted-vs-applied 8,838–8,931 — indistinguishable.
  The drift is a **per-launch GPU particle seed made visible by AMB-RISE**, not a stage rewrite.
  Joint galadriel+drax diagnosis item largely discharged by this null; remaining question is only
  whether byte-stability is wanted at all (instrument-side seed pin) — wave tail, low priority.
- **Watch deliverables:** `tmp/camlock/camlock_wr3_after_pre_boss_B_74000802.mp4` (THE fully-baked
  watch, warm ambient — hue verdict pending) · `tmp/camlock/clips/SBS_judge_vs_playerlock_18s-38s.mp4`
  (two-cameras-two-jobs, side by side) · framing plates under `tmp/camlock/plates/`.
- **AMB-HUE unblocked** — fires now; godot tree free at `3449169`.

## Scope 6 (Matt directives 2026-07-30, post-CAM-LOCK review) — rulings + WALL-READ + BEAUTY-CORNER

- **CAM-LOCK verdict (Matt): "the cam lock looks right."** Camera accepted.
- **Banner ruling (Matt):** the bottom-of-frame text banner (confirmed: that is what "frame
  banner" meant) **STANDS** — it is documentation instrumentation during sim representation,
  slated for removal in a more final version. The 28%-near-surface occlusion item is CLOSED.
  (Caption-size k item not addressed — remains at his eye, non-blocking.)
- **⚑ NEW QUESTION (Matt): why are the inside faces of the walls BLACK in these versions?** He
  normally sees bricks; noticed at the zoomed (player_lock) camera; says it predates today.
  Diagnosis cell **WALL-READ** fired (galadriel, read-only, parallel-safe under AMB-HUE's
  single-writer hold). Conductor hypotheses to test, not assume: (H1) light starvation — the
  PC-LIGHT fix DELETED the false sun (CEILING-1, only-deletion-worked); interior wall faces may
  receive no torch light (omni radius short of the walls); (H2) material/mesh — inward faces
  unlit-material, culled backfaces, or a different wall construction in the WR1 37.5 m room vs
  the scenes where bricks read; (H3) exposure/tonemap band. Evidence-only output; the FIX (if
  lighting) folds into BEAUTY-CORNER below — same surface.
- **Matt directive — the "beautiful corner" (his framing: one corner of the sim representation
  constructed close to the end-game artistic look; canonical ARPG / especially Grim Dawn).**
  Three elements named for ultra-think + scene adoption:
  1. **Player-circle ground sheen + character detail pop** — conductor read: the LANTERN GRAMMAR
     (D1 light-radius lineage; GD/PoE player-attached light). Decomposes: (a) player-attached
     OmniLight3D following the proxy; (b) ground material specular/roughness response (Synty
     floors are flat-albedo, roughness ~1 — sheen requires a floor-material pass); (c) character
     fill/rim from the same or a dedicated light. Matt's own intuition ("lit center follows the
     character") IS mechanism (a). Fork for Matt: player light REPLACES the static lit center vs
     layers on top (GD does both). With AMB-HUE's cool purple room: a WARM player light = the
     living soul carrying light through the crypt of the dead — thematically load-bearing for RDR.
  2. **Shadows** — per-light shadow casting on torch omnis + the player light. Matt's observation
     ("shadows grow in clarity/contrast as light sources are passed") is exactly per-torch
     shadow-casting behavior. Synty legibility claim is correct: contact shadow anchors +
     silhouette separation. Offline render = cost acceptable. Constants (softness, which torches
     cast) are drax's at the eye.
  3. **Near-imperceptible haze growing in the shadows** — Godot 4 Forward+ VolumetricFog at very
     low density (+per-light fog energy → torch shafts); faint fog reads against dark, vanishes
     against bright — the "grows in the shadows" behavior falls out of tonemapping for free.
     Riders: VOID-1 (fog must not glow past walls), LSTAT-2 authorized-delta (lighting change is
     the POINT — stage datum moves by design, declared not smoothed).
- **Sequencing:** AMB-HUE holds the tree (in flight) → hue verdict clip to Matt → BEAUTY-CORNER
  charters after WALL-READ evidence returns + Matt rules the forks (player-light fork; element
  scoping). Wall fix folds into BEAUTY-CORNER if lighting-class.

## LANDING — WALL-READ ✓ (2026-07-30; note `galadriel/notes/2026-07-30-wall-read.md` `db9bf563`)

- **Answer: nothing happened to the walls — a second, untextured wall was built in front of
  them.** `wr2_playback.gd::_dress_wall_faces()` (landed 2026-07-29, WR2-ENCGEO, first
  trace-playback commit) fills the R-WR1-21 band with four untextured BoxMesh slabs (albedo
  0.115/0.118/0.132 — 9.3% of brick reflectance, 10.8× darker, 183× flatter), seated at the kit
  wall's exact height, totally occluding the masonry from interior cameras. Splits on HARNESS,
  not lighting/kit/date: `wr1_level`/`kit_replica` paths → bricks (Matt's memory correct);
  `wr2_playback` watches → black (every WR2/WR3 watch since 2026-07-29).
- H1 refuted twice (slabs are the CLOSEST surface to all twelve omnis; pclight's certified frame
  shows lit brick); H3 refuted as cause, named aggravator (0.0% true black). **Fix class:
  MATERIAL** — give the slabs the kit wall's own material. **Must PRECEDE BEAUTY-CORNER lighting**
  (judging shadows/haze against a false black band = vacuum-tuning). Rider flag: south-wall
  blackout measures azimuth from world-origin `ring_center` — breaks under room translation.

## Scope 7 (Matt rulings 2026-07-30) — BEAUTY-CORNER arms ruled + NUM-POP chartered

- **Player-light fork → BAKE-OFF (Matt):** A/B at his eye, same segment, comparative clips:
  **Arm A** = conductor lean — warm player-carried OmniLight3D layered over DIMMED static center
  ("both", GD grammar; warm-in-cool-purple carries the soul-carries-firelight read, veto-open);
  **Arm B** = static-lit center as-is (no carried light) — the baseline his eye compares against.
- **Shadows → GREEN-LIT with a sharpened acceptance standard (Matt):** shadows must carry a HIGH
  level of detail — specifically ARMOR PIECES on characters/monsters must read in the cast
  silhouette. Operationally: high shadow-map/atlas resolution (offline render — spend freely),
  bias tuned against acne/peter-panning, and the acceptance check is an armor-silhouette read at
  the eye, not a generic "has shadows" check.
- **Fog → GREEN-LIT per conductor specs** (low-density VolumetricFog + per-light energy; VOID-1
  no-glow-past-walls rider; LSTAT-2 authorized-delta declared).
- **Captions ruling (Matt):** mostly fine as-is, BUT **damage numbers get the juice pass —
  larger, bold, POP, and a fun anime-style font** ("really show the feel of combat"). Cell
  **NUM-POP**: floating combat-text treatment — size up, bold weight, outline/contrast for pop,
  spawn-pop animation (scale-punch + settle, the anime hit-number grammar), anime-style display
  font. **Font sourcing discipline:** check LOCAL assets first (Fantasy Warrior HUD pack — may
  bundle display fonts — and any Synty/project font assets); if nothing suitable, route a short
  OFL-licensed font shortlist to Matt for pick + download authorization (no unauthorized network
  fetch).
- **Sequencing:** AMB-HUE (in flight) → hue verdict → **WALL-FIX + NUM-POP** (one small drax
  cell — same `wr2_playback` surface: slab material + azimuth flag + damage numbers) →
  **BEAUTY-CORNER** (bake-off arms + armor-detail shadows + fog) on true brick.

## LANDING — AMB-HUE ✓ (2026-07-30; note `drax/notes/2026-07-30-amb-hue.md` `e02fcb4e`; godot `2c48854` LOCAL, ahead 4)

- **Shipped:** one hue spine across all five layers, authored in DISPLAY space: birth 284°/0.86
  sat/0.30 val (dark violet) → death 256°/0.52/0.95 (lighter blue-violet); measured at the
  rise-verdict camera 274.0°, 68% violet / 32% blue, zero magenta/red. Alpha keys byte-identical
  (Gradient carries RGBA per key — the alpha ramp IS the fourth channel; no collision existed).
  Hue moved out of `color` → neutral grey albedo, making L5's ×0.62 quieting structural.
- **Load-bearing finding: rev 1 was arithmetically clean and RENDERED PINK.** Frozen
  `TONE_MAPPER_FILMIC` is per-channel and saturates ≈1.2 — the ramp's B=2.6 blew the top to
  white. The invariant was wrong: Matt rules on DISPLAYED color, not emitted. Rev 3 inverts the
  tonemap per channel. (Two instrument hypotheses died to their own controls; the third error was
  the seam's own, caught and named.)
- **⚑ DECLARED, AT MATT'S EYE: ambient is 42.7% dimmer** — physics, not a bug: blue carries 7.2%
  of Rec.709 luma; saturated purple CANNOT match orange at equal alpha. Falls hardest in ring 0
  (the centre Matt asked quieted — partially aligned with intent). Levers if too dim:
  desaturate toward white (= the rev-1 failure mode) or raise the frozen alpha keys — his call.
- L6 embers now read as arcane motes (declared). No layer fights the torch band — key/fill were
  ALREADY cool blue; the warm ambient was the last element on the wrong side (the cool-room/
  warm-source split now complete). **R-10 contract comment amended** (proven comments-only by
  stripped-source compare: +58 comments, 0 code) — the eye-dated ambient exception is now in the
  source, closing the Scope-4 conductor ruling.
- Riders: AMB-EVEN re-run (keys on luma) · VOID-1 0 px, ×8 control did not trip — honestly
  declared as not proving detection on this axis · LSTAT-2 Δ 0.000000.
- **Verdict deliverables:** `tmp/ambhue/clips/AMBHUE_eyelevel_BEFORE_top_AFTER_bottom.mp4` (the
  one to watch) · judge-cam twin · `tmp/ambhue/plates/PLATE_ramp_as_displayed.png` (fastest read).
- **WALL-FIX + NUM-POP unblocked** — tree free at `2c48854`; fires next per Scope-7 sequence.

## Scope 8 (Matt rulings 2026-07-30) — hue ACCEPTED · HAND-OFF manifest · path to live

- **AMB-HUE VERDICT (Matt): "the ambient hue looks good."** Purple spine ACCEPTED as shipped —
  the declared 42.7% dimming stands, no lever pulled (no desaturation, no alpha-key raise).
- **Matt directive: fold all remaining additions into the HAND-OFF.** Iteration compresses: after
  WALL-FIX+NUM-POP returns, ONE remaining cell (BEAUTY-CORNER) folds bake-off + armor-grade
  shadows + fog, then ONE integrated full watch — THE hand-off deliverable — carries the entire
  accepted stack. Per-element M-EYE loops end; Matt judges at the hand-off watch (element
  before/after plates ride along as fallback; each element independently peelable — one
  constant/toggle each). Sole exception: the player-light BAKE-OFF still delivers its A/B pair
  (Matt explicitly asked for the comparison).
- **HAND-OFF MANIFEST — the presentation stack the baton render inherits (all Matt-verdicted
  unless marked):** ambient refit (extents ×2.14, Option A fill) ✓ · perpetual rise ("perfect",
  R-10 amended) ✓ · purple hue spine ✓ · `--cam player_lock` on the measured GD decision surface
  ("looks right") ✓ · AI-state tags (subject-field discipline) ✓ · bottom banner stands
  (documentation) ✓ · brick wall band [WALL-FIX in flight] · anime damage numbers [NUM-POP in
  flight] · player-light bake-off winner + shadows (armor-silhouette standard) + shadow-haze fog
  [BEAUTY-CORNER pending] · caption-size k (non-blocking, at his eye at the hand-off watch).
- **PATH TO LIVE (two lanes, honestly split):**
  *Lane 1 — this session (the catching surface):* (1) WALL-FIX+NUM-POP returns [in flight];
  (2) possible one font pick if the disk lacks a display font; (3) BEAUTY-CORNER fires on true
  brick, returns; (4) Matt: bake-off arm pick + hand-off watch verdict; (5) the INTEGRATED
  hand-off watch renders (current wr3 trace); (6) godot push authorization (commits local,
  ahead 5 — one word).
  *Lane 2 — the baton itself (charter session's lane, not conducted here):* WR1 re-emission at
  the pinned post-`bef1f55` hash + wave grading/closeout. When the baton lands, this scene swaps
  its input trace for the baton trace — MECHANICAL by design (the harness is trace-driven; view
  transform only, no feedback path). The same accepted stack rendering the canonical baton
  fight = **the scene live**.

## Scope 9 (Matt 2026-07-30) — NUM-POP verdicted · two new beautiful-room systems

- **NUM-POP VERDICT (Matt): "The damage numbers look great now."** ACCEPTED — banked ahead of the
  cell's formal return notification (Matt watched the deliverable directly; wall-band verdict not
  yet spoken, pending his eye / the cell report).
- **Matt directive — two beautiful-room systems, ultra-thought and translated:**
  1. **Per-room floor-mapped skylight ("grandiosity light").** Genre lineage: D3 cathedral
     god-rays, GD Steps-of-Torment skylight pools. Godot mechanism: tight SpotLight3D from high
     above + **light projector mask** (window-lattice / oculus / crack motif) so the FLOOR
     receives a patterned pool — and the BEAUTY-CORNER fog makes the shaft itself visible for
     free (per-light fog energy; the two features are one system). **Unique per room:**
     seed-driven selection of motif mask, azimuth, pool position, temperature — deterministic
     from room index + level seed. Grandiosity mechanism named: the shaft implies architecture
     above the frame (D3's trick — the light source sells height you never render).
     **Lineage guard:** this is NOT the deleted false sun (CEILING-1 was an unbounded
     directional with a falloff defect); this is bounded, motivated, localized light. Conductor
     temperature lean: COLD pale shafts — three-temperature grammar completes: warm torches
     (local fire), warm player light (the living soul), cold skylight (the distant world above).
     Thematically load-bearing for RDR: light from the living world breaking into the crypt —
     Rise rendered as lighting.
  2. **Per-room cleanliness/disrepair + doorway dirt-bleed.** Mechanism: seeded dressing pass —
     Godot Decal nodes (stains/mud/cracks) + scattered Synty rubble/debris meshes; per-room
     `disrepair` scalar drives density; **doorway overlap** = decal density gradient falling off
     with distance from the door into the next room (reads as tracked traffic; rooms become
     CONNECTED, not stamped). Wayfinding bonus: rooms become memorable by state. Narrative
     bonus (conductor): if disrepair deepens along the traversal path, the gradient IS the
     descent — the seasonal-journey-as-descent pattern rendered as dirt. Asset discipline:
     local-first (Synty dungeon packs carry debris/cracked-floor variants); no fetches.
- **Scoping + sequencing (per the Scope-8 fold-directive):** skylight is LIGHTING-family → folds
  into **BEAUTY-CORNER** (fires on WALL-FIX+NUM-POP's confirmed return; bake-off + shadows +
  fog + skylight — fog/shaft synergy argues for same-cell). Cleanliness/dirt is DRESSING-family →
  new cell **ROOM-DRESS** behind it. Both land in the single integrated hand-off watch; both
  per-element peelable. Seed convention (conductor): room-unique features derive from
  room index + level seed — deterministic, reproducible, no per-room authoring debt.

## LANDING — WALL-FIX + NUM-POP ✓ (2026-07-30; note `drax/notes/2026-07-30-wall-fix-num-pop.md` `4515c8ff`; godot `ec9acbc` LOCAL, ahead 5)

- **WALL-FIX:** brick sourced from the BUILT wall mesh (`Brick_Small_01.png`), not the kit table.
  BoxMesh's 3×2 UV atlas killed `uv1_scale` → world triplanar, period read at runtime off the
  module's own UV (2.3195×3.0142 m/tile). Course SIZE matches; world-locked phase cannot honestly
  match — declared. Atlas kits detected + refused world-UV tiling (rainbow-quilt defect). Band
  |grad| 0.274→2.445, luma 13.22→39.87 (masonry control 4.328 same frame). **Azimuth rider fixed
  to room-root; preservation MEASURED: 0/921,600 px, byte-identical.**
- **NUM-POP (Matt-ACCEPTED, Scope 9):** 6×14 px → 46×101 (76× ink); size DERIVED from screen
  target (8.5/10.5% frame height) through the live camera — both cameras land the same em. Pop:
  0.35→1.40×→1.0 over 0.150 s ease-out. All other captions HELD; banner STANDS.
- **⚑ FONT = PLACEHOLDER (logged every run):** Fantasy Warrior HUD ships sprites, NO fonts; best
  local OFL face (LT Museum Bold) lacks U+25C6. **Shortlist to Matt (all OFL): Bangers (drax +
  conductor lean) · Luckiest Guy · Titan One · Bowlby One SC** — one pick + one download
  authorization; swap is one constant.
- **⚑ Flags:** south wall now observable → renders as unshaded flat plate in TRANSLATED rooms
  (design call, not patched — BEAUTY-CORNER-adjacent) · beyond-wall glow rim (mean 0.69/255) on
  a correctly-brighter wall, declared not smoothed.
- **Deliverables:** `tmp/wallnum/clips/WALLNUM_BEFORE_top_AFTER_bottom.mp4` (watch) ·
  `plates/PLATE_numbers_before_vs_after.png` (fastest read) + playerlock hit-window clip, wall
  plate, pop zoom strip, voidcheck plate. **Wall-band verdict pending Matt's eye** (numbers
  already accepted). **BEAUTY-CORNER unblocked — fires now.**

## Scope 10 (Matt 2026-07-30) — wall band accepted · WALLTOP question · font preview routing

- **Wall-band VERDICT (Matt): "the walls look right now"** — brick band ACCEPTED (triplanar
  phase honesty absorbed without objection).
- **⚑ NEW QUESTION (Matt): why is there a LIGHTER SHADOW on top of the walls before the dark
  void?** He reasserts a standing agreement: **DAYLIGHT on the walltop before the void shadow at
  the edges** (lineage: the PROVISION-CAL S14 cold sky-leak surface — PC-EXIT §3.3 left it OPEN
  at the conductor's refusal to call a split metric; Matt's sentence today is the ruling of
  record: walltop daylight AGREED). The wallnum render shows a lighter-gray band instead.
  Diagnosis cell **WALLTOP-READ** fired (galadriel, read-only, parallel-safe under
  BEAUTY-CORNER's tree hold). Hypotheses to TEST: (H1) harness split AGAIN — the walltop
  daylight treatment lives in the `wr1_level`/`kit_replica`/`walltop_level` path and was never
  ported to `wr2_playback`'s dressing (same root as the black-wall finding); (H2) the band
  slabs' own TOP faces (now brick-triplanar) reading as the lighter band; (H3) the declared
  beyond-wall glow rim being misread as a band; (H4) S14 treatment present but crushed/altered
  by the accepted lighting stack (purple ambient dimming, tonemap). Fix class routes: lighting →
  fold into BEAUTY-CORNER's surface at integration; dressing → ROOM-DRESS rider.
- **Fonts — preview routing (no downloads yet):** all four are Google Fonts specimen pages —
  Matt previews in-browser with custom text (type a damage number). Pick + one word = download
  authorization; swap is one constant (banked at WALL-FIX+NUM-POP landing).
- **FONT RULED (Matt): "go with Bangers."** Download AUTHORIZED and executed same-turn:
  `Bangers-Regular.ttf` (verified TrueType, 93 KB) + `OFL.txt` license staged at
  `agentic_orchestration/drax/assets/fonts/bangers/` (godot tree locked by BEAUTY-CORNER —
  single-writer; the next drax cell moves the file in and flips the one font constant, retiring
  the logged PLACEHOLDER). Diamond-glyph note carried: Bangers may also lack U+25C6 — the
  FontVariation fallback chain from WALL-FIX+NUM-POP handles it; drax verifies at swap.

## LANDING — WALLTOP-READ ✓ (2026-07-30; note `galadriel/notes/2026-07-30-walltop-read.md` `116c4b29`)

- **The lighter band and the dark void are TWO HALVES OF ONE PAINTED STRIP:** the 0.45 m wall-top
  void cap (`walltop_void.gdshader`), **`render_mode unshaded` by construction** — a constant
  warm stone tint ramped to pure black across its outer half. All four conductor hypotheses
  refuted; H5 survives (unshaded by construction). The inversion, one frame: the unlit painted
  band reads **3.31× brighter** than the walltop surface that IS lit.
- **The remembered daylight was NEVER DELIVERED, anywhere:** the S14 sky-leak Key moves 510,495
  px (floor 89.4%, wall faces 53.3%) and **0.00% of walltop-cap pixels** — no light reaches an
  unshaded surface; there is no walltop-daylight function to port (both level paths load the
  same shader, both ARE in `wr2_playback`'s path — the harness-split lean was WRONG this time,
  refuted by measurement). Matt's ruling exists; its delivery never did.
- **Fix class: LIGHTING → integration surface** (`_build_walltop_cap_mat()` kit_replica:1610 /
  walltop_level:598 + the shader's `render_mode` line). **Fork routed to Matt:** (A — conductor
  lean) author the daylight INTO the cap's ramp — cold sky-lit stone on the inner half falling
  to void black on the outer — delivers "daylight, then void" exactly, no Key change, no relit
  geometry; (B) make the cap shaded — lands at ~14.8 (dark; retires the complaint, not the
  ruling) unless the S14 Key (0.06, Matt-ruled) is raised, which is his call, not ours.
- Fix rides the next drax cell (BEAUTY-CORNER in flight; fold at integration alongside the
  Bangers swap). **"22.8 sky" referent still awaiting Matt's pointer** (Scope 10 candidates).

## Scope 11 (Matt 2026-07-30) — walltop Option A · sky ruling HELD · SKY-2 layout · werewolf shadows

- **Walltop fork RULED (Matt): Option A** — daylight authored INTO the cap ramp (cold sky-lit
  stone inner half → void black outer half). Rides the integration cell.
- **Sky-light ruling HELD (Matt): "I'll hold my ruling of the sky light as I'm unsure of the
  options."** The "22.8 sky" lean stays UNBANKED as a ruling; context resolved to the skylight-
  options domain (he has seen a skylight circle — "it's great!" — evidently from in-progress
  BEAUTY-CORNER output). Action: when BEAUTY-CORNER returns, present the skylight OPTIONS
  properly labeled (incl. whatever variant "22.8" names) for his single sitting ruling.
- **SKY-2 directives (Matt verbatim intent; execute AFTER his sky ruling):**
  1. The skylight CIRCLE moves UP to the top half of the room.
  2. A set of small, almost-linear skylight beams "as if through shutters" near the BOTTOM half
     (where the circle sits today).
  3. **Refraction-dust particles** as an ultra-soft beam from above on BOTH patterns (the
     god-ray dust grammar — motes living only inside the light volumes; D3 cathedral lineage).
  4. **Parallax drift:** all patterns move "ever slightly" across the floor as character/camera
     move — "perspective vs movement change." Conductor translation, honesty declared: the
     view-dependent shaft shimmer is PHYSICAL (volumetric fog scattering is view-dependent —
     free); the floor-pattern slide is a STYLIZATION (a fixed ceiling opening's pool does not
     move with the observer) — implemented as a tiny projector-offset keyed to camera/player
     position (one parallax factor constant, subtle), the genre's depth-cue trick. Declared as
     stylized, veto-open.
- **Werewolf shadows (Matt asks; "the only character who may not wear armor — unsure"):** answer
  routes through BEAUTY-CORNER's return — standing carried flag says the current roster has NO
  rig binding (proxies), so the werewolf body (52-bone, 0.0000° retarget, R-PC-4 caster body)
  may need to be PLACED to be shadow-shown. If so: **WOLF-SHADOW rider** on the integration
  cell — the werewolf posed at a torch for a cast-silhouette portrait. Design note (conductor):
  an unarmored werewolf is the BEST shadow test we own — no armor to carry the read means the
  silhouette itself (ears, muzzle, claws, fur tufts) does ALL the legibility work; if the shadow
  system sells an unarmored wolf, it sells anything.

## LANDING — BEAUTY-CORNER ✓ (2026-07-30; note `drax/notes/2026-07-30-beauty-corner.md` `ff147a6a`; godot `5b05947` LOCAL, ahead 6)

- **E1 bake-off DELIVERED, at Matt's eye:** `tmp/beauty/clips/BAKEOFF_armB_left_armA_right.mp4`.
  Arm A (warm carried omni, energy 5.2/range 9 m/shadow-casting, parented to the body node —
  parenting IS the same-frame guarantee; static center dimmed 45%): +26% luma within 2 m of the
  player, near/far gradient +38% steeper, room-wide DARKER (43.9 vs 46.9). Floor roughness
  0.900→0.640 floor-tiles-only (separate cache key — shared key would have sheened the walls);
  value = lit-area maximum on a measured ladder (0.35 = the plastic signature, area collapses).
- **E2 shadows:** subset rule DIED TO ITS OWN CONTROL (corners-only → zero shadowed px at room
  center) — all twelve torches cast; 8192 atlas; bias swept 0.028; SSAO contact anchoring
  declared; stalk/ring/nub forced no-cast (9 m stalk would have laid a 15 m black bar).
  **⚑ ARMOR-SILHOUETTE REALITY: the watch CANNOT answer Matt's standard — combatants are
  capsules.** Answered on a rigged probe (King male): legs/greave taper/tasset hem/sword-arm
  read; pauldrons do NOT at a wall torch — **5.11× projection stretch from a 2.30 m lamp
  (GEOMETRY, not rig; same figure under the 15 m skylight reads at 1.14×).** Consequence:
  wall-torch shadows carry mass, SKYLIGHT shadows carry armor detail — the standard is met under
  the skylight; near-lamp stretch is physics.
- **E3 fog:** VOID-1 failed three times before 0 px CONTAINED (global→bounded FogVolume→box
  height→froxel bleed); two tripping controls earn the zero; inherited luma void-mask declared
  WRONG for fog at room scale — geometric mask built.
- **E4 skylight:** two-rooms plate delivered; rooms 0/1 share a motif (seeded pigeonhole,
  declared). LSTAT-2 all declared not smoothed: E3 +32.9%, all-on +35.3%, contrast RISES 60.3
  vs 58.1 (fog costs contrast, shadows give it back); E4 stage delta +0.000% (localization as a
  number). Frozen L7 stage 0/921,600 px.
- South wall left flagged WITH REASON (shading it breaks the void-black dissolve guarantee —
  design conflict, not a patch). One protected-dir write declared (`tmp/wr2/pl_audit.json`,
  untracked scratch; camlock twin intact).
- **At Matt's eye:** bake-off pick (A vs B) · integrated preview `BEAUTY_BEFORE_top_AFTER_bottom.mp4`
  · plates E2 armor silhouette / E1 sheen ladder / E3 haze / E4 two-rooms. **INTEGRATE-PREP cell
  fires now** (tree free): Bangers swap · walltop Option A · WOLF-SHADOW portrait · labeled
  SKY-OPTIONS board for the held sky ruling (incl. locating the "22.8" referent).

## Scope 12 (Matt ruling 2026-07-30) — BAKE-OFF RULED: **Arm A**

- **Matt verbatim: "Ruling: Arm A - warm carried light over a dimmed center."** The player-light
  fork (Scope 6/7) CLOSES. Arm A ships in the hand-off stack: warm player-carried OmniLight3D
  (energy 5.2 / range 9 m, parented to the body node — parenting IS the same-frame guarantee),
  static center dimmed to 45%, floor roughness 0.640 floor-tiles-only (separate cache key).
  Presence traded for ambience, ruled at his eye against the A/B pair. Veto-open clause on the
  warmth survives per standing law.
- **HAND-OFF MANIFEST update:** E1 moves from "bake-off pending" → **ACCEPTED (Arm A)**. Thematic
  read now canon: the soul carries firelight through dead purple air — the warm-in-cool grammar
  (GD lineage) is the player's own signature in the three-temperature lighting system.
- *(Shadow-casting flag on the carried omni: amended by Scope 13 below — the light stands
  unchanged; its shadow authorship transfers to the unified author.)*

## Scope 13 (Matt directive 2026-07-30) — UNIFIED SHADOW GRAMMAR (the Grim Dawn observation)

- **Matt verbatim intent:** all characters + monsters share the SAME shadow direction/height-depth;
  passing light sources (torches) MAGNIFIES the shadow's contrast (maybe slight height increase).
  Observed in the GD saved playtest clip. Conductor asked to ultra-think/research and decide.
- **Conductor ruling (senior-designer read, veto-open): Matt has described GD's actual
  architecture, and our own E2 measurements already voted for it.** Grim Dawn's engine uses ONE
  scene directional light as the sole character-shadow author; torch point lights are
  non-shadow-casting local illumination. The contrast magnification near torches is **EMERGENT,
  not authored**: the shadow's darkness is ~constant (occlusion of the directional), but the torch
  brightens the surrounding floor → the shadow/surround luminance RATIO rises → the shadow pops.
  No second shadow, no direction fight, near-zero cost. Our E2 finding is the same physics from
  the other side: 2.30 m torch = 5.11× projection stretch (smear); 15 m skylight = 1.14×
  (armor detail reads). Multi-torch casting was fighting the grammar Matt wants.
- **SHADOW-UNIFY spec (drax cell, queued behind INTEGRATE-PREP — single-writer):**
  1. **One shadow author:** scene-level cool DirectionalLight3D (sky family; angle set for
     ~1.1–1.2× shadow-length ratio, matching the measured skylight read). Every combatant,
     every room: same azimuth, same proportion. *(Tint/angle final trim composes with the HELD
     sky ruling; the ROLE is ruled now.)*
  2. **All twelve torches: `shadow_enabled = false`** — retires E2's all-twelve casting.
     Light stays; contrast magnification becomes emergent. Kills the 5.11× smear class and
     the 8192-atlas spend.
  3. **Arm A carried omni: `shadow_enabled = false`** (spec amendment) — the warm light becomes
     the CONTRAST ENGINE of this directive: it brightens the floor ring around the player, so the
     player's unified shadow gains contrast exactly where the eye lives. No swinging self-shadow.
  4. **"Slight height increase" near torches: HELD as an optional stylization lever.** Test
     emergent-only first; if Matt's eye wants the height kick after the watch, a subtle
     proximity-keyed secondary is the fallback. Don't fake geometry before measuring the honest
     mechanism (the E2 subset-rule lesson).
- **SHADOW-CAL galadriel cell (read-only, parallel-safe, fires now):** measure the GD fixture
  footage (GAL-CAM's own capture corpus) for (a) shadow azimuth constancy across the clip,
  (b) shadow-length ratio, (c) shadow-vs-surround contrast delta during torch passes, (d) any
  secondary lobe / length change near torches. Returns become SHADOW-UNIFY's acceptance targets —
  we tune to the referent's numbers, not to memory.
- **Werewolf rider composes:** the unified (high, cool) author is precisely the light that carries
  anatomy detail — the unarmored wolf silhouette test rides on the correct light by construction.

## LANDING — INTEGRATE-PREP ✓ (2026-07-30; note `drax/notes/2026-07-30-integrate-prep.md` `50e333d2`; godot `ec40cdc` LOCAL, ahead 7)

- **P1 BANGERS ✓:** font + OFL carried byte-identical; PLACEHOLDER retired. First render FAILED
  (un-imported `.ttf`) and NUM-POP's own fallback warning caught it — the guard earned its keep.
  At equal cap height Bangers is +27% ink / 15% narrower (both safe directions); solver landed
  `font_size 135 / outline 27` — IDENTICAL to the accepted state, no compensating constant.
  U+25C6 absent from Bangers (cmap-read) — fallback chain load-bearing, named. An analytic
  outline model was discarded for failing on the already-accepted face.
- **P2 WALLTOP OPTION A ✓:** `unshaded` retained; cold sky uniform across the cap + warm
  room-bounce at inner lip only. Chroma sRGB (0.49, 0.59, 0.85) @ `sky_level 0.62` → cap linear
  R:B 2.029 → 0.303 (S14 direction). Dissolve guarantee STRUCTURAL (`lum` untouched → outer lip
  = stone × 0.0). ⚑ First whole-frame reading uninterpretable (null test: ablation 0.54× noise
  floor) — only the masked cap-band measurement attributes. Declared divergence from galadriel's
  value metric, with reason (hers targeted the make-it-shaded lever, not the ruled paint).
- **P3 WOLF-SHADOW ✓:** BL walk clip frozen at stride phase 0.34 + arm-raise 0.55, loaded via
  VHCaster (R-PC-8 exclusion, facing fix, albedo repair carried). Ratios RE-DERIVED for the
  body's own 1.80 m: torch **4.60×**, skylight **1.136×** — not inherited from the armoured
  probe. *(Conductor note: rendered under the pre-Scope-13 architecture; under the unified
  grammar the SKYLIGHT orbit is the canonical read — and it is the flattering one.)*
- **P4 "22.8" LOCATED ✓: `SKY_ENERGY_REF` ×3 rung** of BEAUTY-CORNER's ladder, on disk as
  `tmp/beauty/SKY_22.8.mp4`. **Matt's lean is for the value ALREADY SHIPPING** (tile B on the
  board). Six-tile labeled board delivered; no variant shipped.
- Refusals honored: cap `world_uv_period` declined (masonry ≠ daylight, one-variable law);
  SKY-2 not built (frozen behind the sky ruling per Scope 11).
- Guard catches: `--import` deleted a `[rendering]` LOD line from `project.godot` — restored
  bit-exact, not committed; frozen L7 stage moved −0.418 luma / 127,657 px — authorized,
  declared, peelable.
- **At Matt's eye** (`~/Games/reincarnated-godot/tmp/integ/`): `plates/PLATE_SKY_OPTIONS_board.png`
  + `clips/SKYOPTIONS_cycle_ABCDEF.mp4` (the held sky ruling's decision surface) ·
  `clips/WOLF_skylight_1.14x_orbit.mp4` + `WOLF_torch_4.60x_orbit.mp4` +
  `plates/PLATE_wolf_shadow_two_conditions.png` · `plates/PLATE_walltop_before_after.png` ·
  `plates/PLATE_numbers_bangers_swap.png`.
- **Tree free → SHADOW-UNIFY (Scope 13) fires next**; SKY-2 + ROOM-DRESS remain gated on the
  sky ruling.

## Scope 14 (Matt rulings 2026-07-30) — SKY RULED (B/22.8 + full SKY-2 spec) · walltop re-diagnosed · crit red

- **SKY RULING CLOSES (Matt): option B — `SKY_ENERGY_REF` ×3 (22.8), the shipped value** — WITH
  amendments that fold the Scope-11 SKY-2 directives into a complete spec:
  1. **Circle moves to the TOP HALF of the room** (per Scope 11 #1, reaffirmed).
  2. **Four or five cold pale-blue pools near the BOTTOM HALF** — same hue and energy family as
     the circle; these are the shutter-slat pattern (linear pools; "slat-beams descend to the
     ground slats").
  3. **BEAM LAW (Matt, emphatic): the dust-particle light-up is a BEAM, not a glow.** Particles
     lit DIRECTIONALLY along the shaft axis (diagonally-downward shafts — reading
     diagonally-upward from the floor), forming a CLEARLY LIT circle-beam descending onto the
     ground circle and slat-beams descending onto the ground slats. **The beam CANNOT diffuse
     outwards** — crisp bounded shaft volume, dust living only inside it, apex at ceiling, foot
     exactly on its floor pool (the D4-cathedral / GD light-well column grammar, not a fog bloom).
  4. **Parallax: the whole pattern (shaft + pool together) tilts ever-slightly** as the player/
     camera moves (Scope-11 stylization clause carries: one subtle constant, declared).
- **WALLTOP RE-DIAGNOSED (Matt): the failure is BAND MISMATCH, not tone.** Three bands currently
  read on the cap (a shadow band atop the wall ≠ the portion between it and the void ≠ an "odd
  totally daylight-bright strip"). Ruling: **the ENTIRE non-void cap portion goes UNIFORM
  daylight-bright** — one tone, no warm inner-lip bounce, no intermediate band — then the void
  dissolve. (WALLTOP-2: the Option-A paint was directionally right — "daylight bright is best" —
  but must be ONE band; the structural dissolve guarantee stays.)
- **BANGERS ACCEPTED (Matt): "Bangers look great."** Amendment: **CRIT damage numbers render
  RED** (CRIT-RED). Rider: discover whether the playback trace carries a crit flag; if the trace
  cannot distinguish crits, declare it honestly and flag to the charter session (crit labelling
  is already a wave-inherited item, BQ-4 family) — do NOT fake crits scene-side.
- **Shadow-angle question (Matt: "which angle are we using? can we replicate Grim Dawn's?"):**
  answered inline — no unified angle EXISTS yet (current build: torches + skylight all cast;
  Scope 13 retires that); SHADOW-CAL is measuring GD's actual azimuth + length ratio from the
  fixture footage NOW, and SHADOW-UNIFY will set the DirectionalLight3D to the measured values —
  including matching the SCREEN-SPACE shadow direction at our camera (world azimuth chosen so
  the shadow reads at the same screen angle GD's does at its camera). Yes: replicable exactly.
- **Sequencing:** tree free at `ec40cdc` → **SKY-2 + WALLTOP-2 + CRIT-RED** fire as one drax
  cell NOW; **SHADOW-UNIFY queues behind it** (needs SHADOW-CAL's returns anyway); ROOM-DRESS
  after; then the ONE integrated hand-off watch.

## Scope 15 (Matt ruling 2026-07-30) — BEAM IMPLEMENTATION → BAKE-OFF (mesh-shaft vs fog)

- **Matt converts the beam-implementation choice from measured-pick to A/B AT HIS EYE:**
  **Arm MESH** = mesh-shaft with additive gradient shader (the GD light-well / D4 cathedral-column
  technique), shaft + pool moving as ONE COUPLED BODY under the parallax tilt — Matt's stated
  interest ("I would like to see the mesh-shaft…"). **Arm FOG** = volumetric fog attempting to
  hold a crisp non-diffusing edge. Same room, same pattern layout, same segment, comparative
  clips — the bake-off grammar from the player-light fork (Scope 7) reapplied.
- **Conductor injection status: SendMessage unavailable on this host (third confirmation) —
  queue-behind declared.** The in-flight SKY-2 cell runs its charter (pick by measurement, both
  candidates probed); on its landing, whichever arm lacks render-grade material gets a short
  **BEAM-BAKEOFF** follow-up render so both arms reach Matt's eye as clips. The beam law binds
  BOTH arms (apex-foot coupling, no outward diffusion, dust inside only); the parallax coupling
  clause binds both.
- Standing note: the measured pick still gets DECLARED (which arm the numbers favor and why) —
  Matt rules with the measurement in hand, per bake-off precedent.

## Scope 16 (Matt ruling 2026-07-30) — CENTER LIGHT RETIRED · character-as-light-source · WOLF-WARMTH test body

- **Matt ruling: the static center-of-room light RETIRES ENTIRELY.** The player character IS the
  light source. Amends the Scope-12 Arm A spec: "static center dimmed to 45%" → **static center
  REMOVED (0%)**; the warm carried omni (energy 5.2 / range 9 m, parented) becomes the sole
  player-side room-fill. HAND-OFF MANIFEST E1 entry amends accordingly.
- **Testing configuration (Matt): the WEREWOLF stands at room center carrying its own light
  source** — the wolf's warmth REPLACES what the center light had been providing. Wolf body =
  the R-PC-4 caster (52-bone, 0.0000° retarget, albedo repaired, VHCaster load path from
  INTEGRATE-PREP P3). Wolf's carried light: same warm family as the player's; energy/range
  scaling is the cell's to measure (does one wolf-omni at center reproduce the retired center
  light's floor luma?) — declared, veto-open.
- **Grammar recognition (conductor, banked for the record):** this completes the thematic
  inversion the session has been walking toward — **rooms are dark; the LIVING glow.** Torches
  = fixed local fire, skylight = the distant living world, and now every warm pool that moves
  is a soul. The *Reap. Die. Rise.* read writes itself: light is carried by the living through
  the dead air, not installed in it. (Extension question — do MONSTERS generally carry light,
  or only the player + chosen bodies? — NOT ruled; parked as a design fork for after the
  testing config is at Matt's eye.)
- **Composition with Scope 13:** wolf's carried omni is non-shadow-casting like the player's;
  BOTH bodies become contrast engines for the unified directional shadow — the wolf at center
  is simultaneously the shadow-detail test body (anatomy silhouette) and the warmth source.
  One placement, two acceptance reads.
- **Routing:** SKY-2 cell in flight (queue-behind; no injection possible) → **CENTER-RETIRE +
  WOLF-WARMTH fold into SHADOW-UNIFY's charter** (it is the lighting-architecture cell: one
  directional author + non-casting torches + non-casting carried omnis + center retired + wolf
  placed at center). SHADOW-UNIFY still gated on SHADOW-CAL returns + tree free.

## Scope 16-b (Matt confirmation 2026-07-30) — D1-esque carried-light path CONFIRMED, empirical fallback named

- **Matt verbatim: "we will try this more-D1-esque character lighting path, and if we need to
  warm up the room with more light, then we will after we see it."** The Scope-16 ruling is
  confirmed WITH its escape hatch pre-named: the fallback criterion is EMPIRICAL — his eye on
  the rendered testing config (wolf at center, player carrying, no installed warm fill). If the
  room reads too dead, warm fill returns as a measured lever, not a reversion (candidate levers,
  banked for that day: raise carried-omni range/energy; per-torch energy up; a faint GD-style
  legibility whisper as the LAST resort — it is the vestigial form this path exists to surpass).
- Lineage note carried: rig = Grim Dawn's (carried warm omni, non-casting, one directional
  author); role = Diablo 1's (the room has no warm fill unless a living body stands in it).
  D1's third layer (light-radius-as-stat/itemization) remains a PARKED wave-scale fork —
  engine-touching, not scene-side; unlocked but not opened.

## LANDING — SKY-2 + WALLTOP-2 + CRIT-RED ✓ (2026-07-30; note `drax/notes/2026-07-30-sky2-walltop2-critred.md` `ae735944`; godot `8d66ac3` LOCAL, ahead 8)

- **P1 SKY-2 ✓ — BEAM IS MESH, decided by measurement (Scope 15 bake-off disposition):** froxel
  fog lost on its own numbers — no beam silhouette (room-wide plateau across half the frame),
  12.5 px quantisation floor, 90% temporal reprojection smearing any moving pattern. Shipped
  mesh edge 4–7 px (10–90%) on a 13 px core; "cannot diffuse outwards" is STRUCTURAL (samples
  outside the cone don't exist; the ray-march integral IS the chord — zero at boundary by
  arithmetic). **Fog did not lose a beauty contest; it failed to form a beam at all** — the
  Scope-15 A/B render of the fog arm is one short cell away IF Matt wants the failure on screen;
  conductor lean: the measurement stands. E3's ambience fog untouched.
- Layout measured in SCREEN terms (top-half = screen statement, projected through the actual
  camera): **the old pool was in the bottom half exactly as Matt said** (−0.737 on the screen-up
  axis); all four rooms now circle-top / 4–5 slats-bottom; per-room seeding preserved by
  appending slat draws. Apex-foot coupling IoU **0.963** (vs 0.000 for all three alternative
  projector conventions); parallax EXACT — one transform chain carries lamp + shaft + dust
  (+0.4800 m slide both patterns; cannot decouple). Tilt raised 14°→24° for the ruled diagonal
  read; cost declared (pool irradiance ×0.886 — geometry consequence, not an energy re-tune).
  VOID-1 0 px contained (control trips at 484,326 px).
- **⚑ FORK TO MATT (§1.6, the honest failure): the CIRCLE-beam is a SLAB** — 6.93 m wide ×
  3.01 m tall (aspect 0.43) because the room has no ceiling above the wall course and lamp
  height is welded to the LOCKED 22.8 energy; slats read as proper columns (3.84). Options:
  **(A)** accept the wide low circle-beam as a large oculus honestly rendered — conductor-visible
  default, what ships; **(B)** narrow the aperture so it reads as a column, accepting a smaller
  pool (Matt has seen and liked the current pool); **(C)** let beams rise above the wall line,
  accepting deliberate light in the void (retires a containment guarantee that cost E3 three
  failures). Conductor lean: **A** — an oculus and light-wells is a coherent cathedral pairing;
  B shrinks a verdicted pool; C spends a guarantee for geometry.
- **P2 WALLTOP-2 ✓ — the Scope-14 diagnosis OVERTURNED by measurement:** shadows/SSAO, fog,
  skylight each move exactly ZERO cap pixels. The bands were `Brick_Small_01`'s own mortar
  coursing (texture swings 3.73×, cap swung 4.07×). Flattened: contrast 4.12× → **1.03×**, one
  uniform band at L 56.89 vs Matt's L 57.04 daylight referent; dissolve 0 px above 1/255
  outboard (glow off). No screen-space pass ever touched the unshaded cap — the conductor's
  SSAO suspicion was wrong, named here.
- **P3 CRIT-RED ✓ — the trace CAN tell:** `crit` on 100% of damage events (145/10,581
  battery-wide, all ×1.5); exactly ONE crit in this watch (t = 36.300 s) renders red. Mob-dealt
  crit rate measured 0/1,424 — red can only appear on a dealt number. Pop untouched (a colour
  was ruled, a colour was shipped).
- **⚑ FLAG CARRIED TO SHADOW-UNIFY:** a projector spot with `shadow_enabled = false` renders
  ZERO light in Godot — if Scope 13 naively switches the skylight spots' shadows off, THE POOLS
  VANISH. SHADOW-UNIFY must reconcile: skylight spots keep shadows on (localized casters inside
  beam footprints) OR the pools re-author as unlit decals/meshes; the "one directional author"
  principle applies to COMBATANT shadows — the cell decides the mechanism and declares it.
- Three drax constructions died to their own renders, on record with numbers (single-surface
  sample halved the circle; divide-and-clamp saturated 2.80% of pixels white; a Godot-4.6
  `DEPTH_TEXTURE` removal fell back silently to `blend_mix`, caught by picture before log).
  Guards all clean; LSTAT-2 L7 stage +0.450710 authorized/declared/peelable.
- **At Matt's eye** (`~/Games/reincarnated-godot/tmp/sky2/`): `clips/SKY2_room_judge_motion.mp4`
  (THE one to watch) · `clips/SKY2_playerlock_crossing_beams.mp4` · `clips/CRITRED_t36.3.mp4` ·
  `clips/WTSWEEP.mp4` · `plates/PLATE_walltop2_before_after.png` (fastest read) ·
  `plates/PLATE_crit_red_vs_normal.png`.
- **Tree free at `8d66ac3` → SHADOW-UNIFY next** (still gated on SHADOW-CAL returns; charter now
  carries Scope 13 + Scope 16/16-b + the pools-vanish flag).

## Scope 17 (Matt ruling 2026-07-30) — BEAM-REAL: the church-window reference spec

- **Matt verdict on the shipped beams: too bright · not pinned to the ground lighting · too
  thick.** His reference — real photographs of church-window light shafts — yields three laws:
  1. **Ground pool: as we have it** (verdicted, untouched).
  2. **GAP LAW: a nearly TRANSPARENT space between the ground pool and the beam** — the beam's
     lower terminus is NOT the floor.
  3. **UPPER-AIR LAW: the beam begins ABOVE a person's height and extends upward toward the
     (out-of-view) windows** — the visible shaft is the upper-air segment, fading toward an
     implied source beyond the frame.
- **Conductor spec translation (BEAM-REAL cell):** (a) INTENSITY down — the beam is a whisper,
  not a glare (additive gain re-tuned; the LOCKED 22.8 lamp energy governs the POOL, not the
  mesh gain — separate constants, no energy re-tune); (b) lower terminus lifts to ~2.2 m+ with
  a soft fade — the near-transparent gap is the signature realism cue; (c) THINNER — beam
  cross-section DECOUPLES from pool width (real shafts read narrower than their scattered
  ground pools; stylization declared): the pool Matt likes stays full-size, the shaft slims;
  (d) beams extend UP past the wall course, fading out — toward implied windows above.
- **⚑ FORK DISPOSITION: the §1.6 A/B/C fork DISSOLVES into this spec.** The slab problem was a
  full-height floor-coupled beam; with the gap law + decoupled cross-section + upper-air
  extension, the circle-beam becomes a thin upper-air shaft — B's cost (shrinking the liked
  pool) is avoided by decoupling; C's mechanism (rising past the wall line) is ADOPTED with its
  cost DECLARED: beam meshes will overlay the void-black region above the walls — shafts
  descending out of darkness. The VOID-1 containment guarantee AMENDS: additive beam meshes are
  air-visuals (they light no surfaces); the no-light-past-walls guarantee continues to bind
  LIGHTING (projector spots, pools), while beam volumes above the wall line are an authorized,
  declared, peelable exception. Veto-open at the watch.
- Apex-foot coupling law amends to POOL-AXIS coupling: shaft axis still lands its (invisible)
  foot on the pool center (IoU machinery repurposed as an axis check) — the gap is a fade, not
  a displacement; parallax one-transform-chain law unchanged.
- **Sequencing:** tree free at `8d66ac3` → **BEAM-REAL fires NOW**; SHADOW-UNIFY still gated on
  SHADOW-CAL (in flight); fog-failure render offer stands but is MOOT unless Matt asks (mesh is
  now doubly confirmed as the only implementation that can honor the gap law — fog cannot
  hold a floating lower terminus).

## Scope 18 (Matt directive 2026-07-30) — BATON-PREP: Stage-2 final lap began; take the baton, render the sim as THE scene

- **Timing recognition (why now):** the WR1 run's Stage-2 FINAL LAP just began in the charter
  session — the baton emission spec is STILL AMENDABLE. A scene render-need found now = one
  rider on that run's ledger; found after close = a re-emission. The window is the lap.
- **BATON-CENSUS fired (legolas, read-only, parallel-safe):** NEEDS-vs-CARRIES table over the
  wave's actual Stage-2 emissions vs the scene's render needs — (1) telegraph GEOMETRY
  (shape/radius/origin/windup — the frigidring 12 m nova decal); (2) skill flavor labels
  (element+mechanic per event); (3) per-frame status states (freeze/CC); (4) projectile/travel
  vs aim-line-only; (5) combatant identity (kit/monster id + hero slot); (6) schema diff vs G-5
  baseline. Gaps route to the charter session via pushed bank — the established cross-session
  mechanism.
- **Scene-side prep ledger (this session's lane, sequenced):**
  1. **TELL-DRESS cell (chartered, queued):** ground-decal telegraph renderer — the one big
     UNBUILT scene piece for boss legibility (D3/Lost Ark decal grammar: shape decal grows over
     windup, keyed to telegraph events). The frigidring as a cold pale-blue expanding ring drops
     straight into the temperature grammar (cold = hostile/distant register). Gated on
     BATON-CENSUS row 1 (geometry present or rider filed).
  2. **SHADOW-UNIFY** (gated on SHADOW-CAL) — the lighting architecture must be settled before
     the baton watch, or the boss fight gets judged under a rig we're about to replace.
  3. **Input-swap verification:** confirm the harness takes the baton trace path as pure config
     (mechanical swap, no code) — rides TELL-DRESS's cell as a checklist item.
  4. **⚑ ROSTER FORK (Matt's, opens when the baton lands):** trace actors → BODIES. Today's
     combatants are capsules; the werewolf caster (Scope 16 center placement) is the only rigged
     body staged. Which body renders the player? The boss? Capsules-with-beautiful-room for
     baton lap 1 vs bodies-first? His call when he sees the census + what the trace names.
- **Sequencing:** BEAM-REAL (in flight) → SHADOW-UNIFY (on SHADOW-CAL return) → TELL-DRESS
  (on census) → ROOM-DRESS → the ONE integrated hand-off watch ON THE BATON TRACE — Lane 1 and
  Lane 2 converge at that watch: the accepted stack rendering the canonical fight = the scene
  live.

## Scope 17-b (Matt signal 2026-07-30, mid-flight) — BEAM-REAL smoke frame: "exactly what I want"

- **Matt, on a BEAM-REAL SMOKE frame (room 3, seed 74001000, cam=eye): "the first render is
  looking like exactly what I want!"** Frame banner constants — **`narrow=0.300 · base=2.40 ·
  top=11.00 · gain=0.300`, beam+dust on** — are hereby the EYE-APPROVED REFERENCE SET: if the
  cell's final tuning drifts from these values, the drift must be declared against this banked
  set at landing (his eye liked THIS one). Not a final verdict (M-EYE motion rule stands for
  the landing watch); banked as the strongest possible mid-flight signal.
- Conductor read of the frame, for the record: all three Scope-17 laws visible at once — thin
  cold shaft descending OUT OF THE VOID BLACK above the wall line (the amended VOID-1 exception
  earning its keep as an image), lower terminus fading ~2.4 m up with clean air beneath, cool
  floor circle waiting below, torch-warm walls wrapping it. The cold/warm temperature grammar
  reads in a single still.
- No injection possible (SendMessage down, standing); signal reaches the cell via this bank if
  it reads the note late, else via conductor at landing reconciliation.
- **CAVEAT (Matt, follow-up): the signal is at `cam=eye` — he has NOT yet seen it at the ARPG
  camera angle.** The reference-set bank stands, but the BINDING verdict waits on the judge/
  player_lock deliverables (which the cell's charter already requires — the 47°-pitch watch is
  the acceptance surface, per M-EYE). Known physics rider for that view: beam visibility is
  view-dependent for fog but NOT for additive mesh — geometry is, though: at the steep ARPG
  pitch the upper-air shaft occupies less frame height and the void-overlay segment may crop;
  the landing must show the shafts READ at the game camera, not only at eye level.

## LANDING — BATON-CENSUS ✓ (2026-07-30; note `legolas/notes/2026-07-30-baton-census.md`; pushed by this bank)

- **Headline: the schema is baton-ready for the fight the traces CONTAIN — and NOT for the boss
  the wave NOW BUILDS.** The four freshest Stage-2/2b artifacts (18:37–21:01) contain ZERO
  `.jsonl` — newest emission (16:45) predates the Stage-2b mechanics. A scene certified against
  the existing traces certifies against a boss that no longer exists.
- **⚑⚑ THREE RIDERS ROUTED TO THE CHARTER SESSION (WR1 Stage-2 final lap — the amendable
  window is NOW; this pushed bank is the routing artifact, and Matt is asked to relay verbatim):**
  1. **`primordian_icearmor` has NO emission channel** — state lives in `mob._wr3_icearmor`, a
     plain attribute NOT in `combatant_state.active_effects` (the only thing `_ailments()`
     reads). A 25% absorb + 28% outgoing-cold buff runs INVISIBLY. **Not recoverable post-hoc —
     without this rider the baton costs a re-emission regardless.** Fix: route through
     `active_effects` or a `buffs:[]` block.
  2. **`chillbane_blizzard` emits `shape:"circle"`** — downstream it would be painted AND SCORED
     as a nova (`wr2_playback.gd:2435` tests circle unqualified → corrupts `_nova_verdicts`,
     the statistic the run is GRADED on; silent). Fix: a `family` string on telegraph events
     (`nova|blizzard|wave|melee`).
  3. **`attack_id` absent on damage/dot events** — hit→telegraph unjoinable (nova's own hit
     carries `skill_idx:-1`). Fix: carry `attack_id` on damage/dot.
- **NEEDS-vs-CARRIES (full table in the census note):** telegraph geometry CARRIES (19 fields;
  real nova: circle/12.0 m/wind_up 2.32 s/damage 218) — but only point+circle ever emitted,
  orientation/half_angle/width 100% null, tells are MOB-SIDE ONLY · skill flavor
  CARRIES-PARTIALLY (element null everywhere except impact `damage.element`; mechanic = substring
  sniff on `attack_id`) · status CARRIES as `ailments[]` (CC = `action_lock` 1.3 s, NOT `freeze`
  — Gate-2 H-1 fidelity honored in the schema itself; zero occurrences in fresh batteries, the
  player escaped all 114 novas; consumer reads it 0 times) · projectile/travel ABSENT (one
  telegraph + one damage; the 14 m/s ring crossing is sub-tick solved — scene must animate
  expansion from telegraph fields, declared stylization-of-truth) · identity CARRIES-PARTIALLY
  (**`is_boss` false for the boss on 100% of traces**; consumer already workarounds by
  id-prefix+max_hp) · wave additions: decision/telegraph event types, crit (player-only
  structurally), hp_provenance, per-frame ai_state in 5 files.
- **TELL-DRESS charter GROWS (scene-side obligations regardless of riders):** qualified
  family/shape handling (blizzard ≠ nova even if the rider lands — defense in depth) · `rect`
  shape support (primordian_wave emits it; today's `else` branch merely HAPPENS to build the
  right BoxMesh) · ailment rendering (`action_lock` body language — the first time the scene
  shows CC) · ring-expansion animation from `origin/radius_m/wind_up_s/fire_tick` · boss
  identification hardening until `is_boss` is fixed · player tells: none exist (mob-side
  grammar; consistent with ARPG convention — enemy tells telegraph, player attacks resolve).
- **Certification law banked:** the scene's baton certification happens against a POST-Stage-2b
  trace or not at all; the 15:33/16:45 traces are development fixtures from here on.
- **✓ RIDERS LANDED (Matt confirmation, 2026-07-30): "the stage 2c flight was stopped and
  re-launched with your requests folded in."** The charter session absorbed all three riders
  into the re-launched Stage-2c flight — the census fired inside the window it was fired to
  hit (icearmor emission channel, telegraph `family`, damage `attack_id` now inbound in the
  baton schema). Consequences: TELL-DRESS may RELY on the three fields (defense-in-depth
  handling stays per its charter — reliance ≠ trust without checking); the certification law
  updates to **post-Stage-2c trace**; the `is_boss` fourth-rider suggestion remains
  outstanding (not confirmed in scope — consumer workaround stands until seen in a real
  Stage-2c emission).

## Scope 19 (Matt directives 2026-07-30) — ONE SKY DIRECTION · fog-unlit comparison (post-BEAM-REAL)

- **SKY-ALIGN (Matt): all skylight shafts share ONE direction.** Drax "keeps making two skylight
  angles"; Matt wants every shaft (circle + all slats, all rooms) descending from the SAME
  implied direction. Design grounding: the sun is at infinity — real church-window beams are
  PARALLEL; two angles read as two suns. Composes with Scope 13 (one directional shadow author)
  into a single law: **the sky has ONE direction in this world** — shadow azimuth and shaft lean
  derive from the same vector (SHADOW-CAL's measured GD angle is the natural candidate for
  both; final direction Matt's at the watch). Per-room pattern LAYOUT stays unique (seeded);
  DIRECTION becomes global.
- **FOG-UNLIT COMPARISON (Matt): a version where the volumetric fog is NOT lit by the window
  skylights at all** — just mesh beams + floor pools, E3 haze staying neutral. A/B at his eye
  vs current (skylight-lit fog). Mechanism: exclude the sky projector spots from fog
  contribution (per-light fog-energy zero) — the warm torch fog-lighting stands unless he says
  otherwise; only the SKY-fog interaction toggles.
- **Routing:** BEAM-REAL in flight (no injection; standing) → both items fold into
  **SHADOW-UNIFY's charter** (it is the one-direction cell by construction: directional author
  + shaft alignment + fog-light exclusion toggle + center-retire + wolf + pools-vanish
  reconciliation). Its deliverables now include the fog-unlit A/B pair.

## LANDING — BEAM-REAL ✓ (2026-07-30; note `drax/notes/2026-07-30-beam-real.md` `f0cb00ef`; godot `6c9e3dd` LOCAL, ahead 9)

- **The three church-window laws, measured in:** gain 0.72→**0.26** (beam p99/pool p99
  2.033→**1.024** — the shipped beam had been TWICE the pool's brightness; total added light
  −18.5× at the grading camera) · cross-section **0.30 of pool** (~1.0–1.4 m shaft under a
  7.41 m pool; recovered 0.2845 in image space) · lower terminus **2.493 m** (50% fade 3.251 m;
  **0.69 m of clear air over a 1.80 m body**) · upper terminus **10.633 m — 7.63 m past the
  wall course**, fading toward the implied windows · dust 0.85/260→**0.10/110** · lamp 22.8
  UNTOUCHED (separate constant, verified by code path).
- **Scope 17-b reconciliation (eye-approved set narrow=0.300 base=2.40 top=11.00 gain=0.300):**
  narrow 0.300 ✓ · base 2.493 (≈) · top 10.63 (≈) · **gain 0.26 vs 0.300 — small declared
  drift, dimmer**, driven by the p99 ratio landing at 1.024 (beam ≈ pool parity). Within the
  approved family; the metric had to be p99 — peak is flat across the whole ladder because the
  brightest pixel is always a dust mote (a peak ladder would have said dimming does nothing).
- **§1.6 fork DISSOLVED by measurement:** circle aspect 0.81→**7.87** within one instrument —
  a COLUMN, taller than the SKY-2 slats (prior 0.43/3.84 figures not comparable — different
  method; within-instrument gains ×9.7, ×8.1).
- **VOID-1 split three ways, the zero earned:** lighting moves 0 void px (both cameras); beam
  overlay 0 px at the grading pose, 14,833 px (3.03% of void) at a low pose — the authorized
  air-visual exception, quantified; ablation present-but-silent vs absent BIT-IDENTICAL
  (0/921,600, max Δ 0) → the mesh lights nothing, proven not asserted. Pool-axis coupling
  0.000000 m geometric, 0.0035 m image-space, containment 0.9997; parallax unchanged;
  **LSTAT-2 NO DELTA** (L7 bit-identical, re-run rather than argued).
- **⚑ ERRATUM ROUTED:** SKY-2's IoU 0.963 was measured through an inherited shader defect
  (perspective ray reconstruction under an ortho rig; fixed via `PROJECTION_MATRIX[3][3]`,
  0.013% px delta) — **verdict survives, precision figure must not be re-quoted.**
- Four honest failures on record with numbers (ortho ray defect caught by 1,350 px below the
  beam's own cut-off; a `--nosky` reference that re-aimed 6 m caught as negative additive px,
  first pool reference wrong ~5×; void mask measuring its own antialiasing, eroded 2 px; a
  wrong axis-test formulation discarded).
- **⚑ TWO ITEMS AT MATT'S EYE beyond the verdict:**
  1. **Narrowing cost:** the aperture's fine structure (oculus ring/spokes, individual slits)
     no longer resolves INSIDE the shaft — one contiguous run; it fully resolves on the
     untouched pool. `SKY_BEAM_NARROW` is one constant if he wants some back.
  2. **The money shot cannot exist at `player_lock`:** the camera frames ~12 m of ground; the
     beam lives 2.4–11 m up — body and beam NEVER co-frame at the game camera (verified on the
     real render). The gap-over-body read is staged on the probe (`BEAMREAL_gap_over_body.mp4`)
     and declared as staged. At gameplay pitch the shafts read as environment (the GD grammar —
     shafts live at room edges/background). **If Matt wants beam-over-head at the game camera,
     that is a CAMERA fork, not a beam change.**
- SHADOW-UNIFY flags carried: pools-vanish (unchanged) + the fixed shaft shader is now
  projection-aware (safe under any future camera work).
- **At Matt's eye** (`~/Games/reincarnated-godot/tmp/beamreal/`): **watch first**
  `clips/BEAMREAL_before_after_watch.mp4` (SKY-2 vs BEAM-REAL, beam the only variable) ·
  `clips/BEAMREAL_playerlock_watch.mp4` (**the ARPG-angle read his 17-b caveat waits on**) ·
  `clips/BEAMREAL_room_watch_motion.mp4` · gap-over-body pair (staged, declared) ·
  `plates/PLATE_beam_before_after.png` (fastest) · `PLATE_gap_measured.png` · `PLATE_pool_axis.png`.
- **Tree free at `6c9e3dd` → SHADOW-UNIFY next, still gated on SHADOW-CAL** (in flight).

## Scope 20 (Matt rulings 2026-07-30) — BEAM-FIX: five adjustments after the BEAM-REAL watch

1. **Camera defect (Matt): the clips are NOT at the correct GD camera angle.** All future beam
   verdict clips render at the CAM-LOCK-verified rig (the GAL-CAM measured pinhole family /
   `--cam player_lock` Matt verdicted "looks right") — the cell must state ON-FRAME which
   camera each clip uses and verify against the CAM-LOCK operands, not against memory.
2. **⚑ PARALLAX RETIRED (veto exercised):** "it doesn't look good to have the angle of the
   lights adjust as the camera moves. Let's make them static now." The Scope-11 #4 stylization
   (declared veto-open at birth) is VETOED — beams/pools/dust become WORLD-STATIC. The
   one-transform-chain coupling machinery stays (shaft+pool+dust one body); only the
   camera/player-keyed offset dies. The system worked as designed: stylization declared →
   seen in motion → vetoed cleanly.
3. **Floor pools LOST in the after version (Matt: "what happened to them?")** — DIAGNOSE
   FIRST, fix second: the pools were charter-untouched in BEAM-REAL, so their absence in the
   watch is either a real regression (the `--nosky`-re-aim bug family / peel path leaking into
   the shipped render), a pools-vanish landmine trip, or a brightness-perception effect of the
   beam dimming. Name the mechanism with a measurement, restore the pools, and prove
   restoration against the SKY-2 landed state.
4. **ONE SUN (reaffirms Scope 19 SKY-ALIGN, now EXECUTES):** all shafts from one shared
   direction "as the sun does on earth." BEAM-FIX picks a PROVISIONAL single direction
   (declared on-frame, veto-open); SHADOW-UNIFY may re-derive the final vector from
   SHADOW-CAL's measured GD angle so shadow azimuth + shaft lean stay one vector (Scope 19 law).
5. **SUPER IMPORTANT (Matt): beams must be LONGER — extending WELL BEYOND the upper bound of
   the frame at the proper GD camera.** The 10.63 m top is insufficient; the acceptance check
   is SCREEN-SPACE: at the CAM-LOCK rig, every shaft's upper terminus exits the frame top (no
   visible beam-end in-frame). This dissolves the co-frame concern from the BEAM-REAL landing
   the right way — the beam doesn't need to share a frame with the body's head; it needs to
   have no visible end.
- **Routing:** BEAM-FIX (drax) fires NOW on the free tree (`6c9e3dd`); SHADOW-UNIFY remains
  gated on SHADOW-CAL and inherits the final-direction unification.

## LANDING — SHADOW-CAL ✓ (2026-07-30; note `galadriel/notes/2026-07-30-shadow-cal.md` `536a3fa9`; pushed by this bank)

- **Headline: the Scope-13 conclusion SURVIVES ("emergent, not authored"); the conductor's
  stated mechanism INVERTS.** Measured: the GD shadow interior is NOT pinned — it is
  **MULTIPLICATIVE, ρ ≈ 0.50 of local floor luminance** (0.482 on an 81.9-luma floor, 0.565 on
  38.1). The RATIO holds; the ABSOLUTE hole deepens on bright floors (42.4 vs 16.6 luma). Same
  destination, different build instruction.
- **SHADOW-UNIFY acceptance target (replaces the pinned-interior framing):** a multiplicative
  shadow at **ρ ≈ 0.50 of local floor luminance**, verified NOT to clamp to a fixed dark value
  in dim rooms; acceptance test = same figure on a bright and a dim tile, ρ within ~10%. If
  that holds, Arm-A's contrast magnification is free — no proximity lever.
- **Azimuth: direction class established, degrees structurally unanswerable from this corpus.**
  Up-screen-and-left at the fixture camera (two verified segmentations +142.7°/+107.3°;
  whole-session left-dark asymmetry median dA +0.0922, n=556, p=5.07×10⁻⁸, synthetic controls
  passed). A single frame cannot separate figure-sprite from up-screen shadow — degeneracy is
  structural, not effort-bound. ⚑ Block-wise the SIGN FLIPS (one 700-s block 88.7% left-dark,
  another significantly right-dark) — either GD's azimuth differs per area (their choice, not
  binding on us) or terrain defeats the control; ROUTED, NOT RULED. Our one-sun law (Scope 19)
  is MATT'S aesthetic ruling and stands regardless.
- **⚑ PROVENANCE GUARD:** Scope 13's "~1.1–1.2× length ratio matching the measured skylight
  read" is OUR OWN E2 number — the referent's ratio is CANNOT-ANSWER (the fixture player is a
  modded werewolf with a VFX plume; height denominator untrustworthy). Fine to ship; must never
  be quoted as referent-anchored.
- (d) Height-kick near torches: CANNOT-ANSWER — the Scope-13 decision to HOLD that lever is now
  evidence-backed rather than prudent.
- **The corpus is exhausted (measured, not asserted):** 75.4% of frames carry an open UI panel;
  zones volumetric-fogged; ZERO torch-pass segments in 1h53m (the 581 warm sources near the
  player are his own aura/VFX). **MATT-ACTION (optional, ~60 seconds, the only remaining
  instrument): one deliberate GD capture — one zone, ONE torch, walk in and out TWICE, panels
  closed, non-fog zone** — turns (c)/(d) into two-significant-figure numbers and gives (a)/(b)
  proper n. Refinement, not a gate: SHADOW-UNIFY proceeds on ρ≈0.50 + direction-class +
  provisional azimuth (veto-open at the watch).
- Instrument discipline: four failures committed not hidden (SC-4 died to its random-azimuth
  null; SC-8's guard decided its answer; plate harvest 0/56 windows for a measured reason;
  estimator chosen BY a control, −4.2% bias vs naive +30%). `sc_cam.py` reproduced GAL-CAM's
  scale field to 0.04% with independent inputs.
- **Gate state: SHADOW-UNIFY's measurement gate is DISCHARGED** (targets in hand); it queues
  behind BEAM-FIX (tree) and inherits: ρ-multiplicative target, direction-class azimuth
  (provisional exact vector, veto-open), one-vector unification with shaft lean (Scope 19/20),
  pools-vanish fix, fog-unlit A/B, center-retire + wolf placement (Scope 16), our-number
  provenance on the length ratio.

## Scope 21 (Matt ruling 2026-07-30) — BEAM-CONE: cones of light, opening to the floor

- **Beam height VERDICTED GOOD** (Scope-20 #5 satisfied at Matt's eye — banked mid-BEAM-FIX on
  the smoke evidence he's watching; formal reconciliation at the cell's landing).
- **SHAPE LAW (Matt): beams are perceived as CONES OF LIGHT, opening TOWARD THE FLOOR** —
  narrow aloft, widening downward, **the cone's circular end pinning EXACTLY to the circle of
  light on the floor (radius/diameter match)**. Slat-beams: cones of "almost no width" — thin
  blades pinning exactly to their floor slats.
- **Amends BEAM-REAL's uniform 0.30 cross-section:** the shaft re-couples to the pool AT THE
  FLOOR END (cone base = pool circle) and tapers UPWARD (the ~0.30 narrowness now lives at the
  top). Composition with the Scope-17 GAP LAW, conductor reading (veto-open): the cone's
  GEOMETRY pins to the pool — the near-floor portion of the cone stays nearly transparent via
  the fade envelope, so the eye completes the cone onto its pool without the beam ever sitting
  opaque on the ground. Perceived pinning through a transparent base; if his eye wants the base
  more present, the fade floor is one constant.
- **Aperture-structure note dissolves for slats:** Scope-20's "fine structure lost in the
  shaft" concern — the cone law inherently restores per-slat blade identity (one near-zero-width
  cone PER slat, not one contiguous run).
- **Routing:** BEAM-FIX in flight (no injection; standing) → **BEAM-CONE fires as a focused
  geometry cell on BEAM-FIX's landing**, BEFORE SHADOW-UNIFY (keep the cosmology cell clean of
  in-flight geometry churn). One-sun parallelism (Scope 19/20) binds the cones' AXES; pool-axis
  coupling law now upgrades to pool-BASE identity.

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

## Scope 22 (Matt rulings 2026-07-31) — BATON-RENDER authorized: casting delegated, werewolf locked, Fantasy Rivals boss

Matt, on the ARCHITECT completeness pass for the baton-render run:

1. **Fork A resolved: option (a), authority DELEGATED** — *"(a), and you and Drax may choose; no
   need to hold on my verdict."* The orbit-board M-EYE hold is WAIVED for casting — gandalf +
   drax cast the roster; Matt sees the cast in the rendered watch, veto-open as always.
2. **Player body LOCKED: the werewolf** (52-bone SK rig, 0.0000° retarget, albedo repaired).
3. **Boss body: cast from POLYGON Fantasy Rivals** — *"it would be really great if it could be
   one of the larger skeletons/rigs"* from
   `matt_notes_handoff_docs/recent-synty-packs/fantasy-rivals`.
4. **Two-lap law (Matt's prior message, adopted as charter structure):** *"Render phase 1 first
   if phase 2c hasn't yet completed, then render 2c afterwards."* Lap 1 = phase-1 g5 traces
   (30 on disk, engine ≥ `bef1f55`); Lap 2 = re-render on rider-bearing Stage-2c traces once
   confirmed on disk (`wr3_stage2c.json` landed Jul 31 00:18; per-fight replay traces with
   icearmor/`family`/`attack_id` riders NOT yet located — Lap-2 gate verifies).

**Pack inventory (conductor recon, on-disk verified):** 20 boss-class rigs (`SK_Character_*` +
`SK_BR_Character_*`), Unreal-convention mirror set present, 4 texture families A–D **each with an
EMISSIVE map** + `FantasyRivals_Texture_Elemental_Emissive.png`. Large-rig candidates:
ElementalGolem · FortGolem · MechanicalGolem · Troll · BarbarianGiant · RedDemon · EvilGod ·
SpiritDemon · AncientQueen.

**Conductor's casting lean (drax holds final say at rig-quality check, per delegation):**
**SK_BR_Character_ElementalGolem_01** — (i) large mass sells the 12.0 m nova telegraph and the
2.32 s wind-up body language at the GD camera; (ii) the dedicated Elemental emissive channel lets
the boss GLOW COLD PALE-BLUE — the icearmor/blizzard kit, the Scope-14 cold floor pools, and the
"rooms are dark; the living glow" grammar all converge on one body (boss = cold emissive glow vs
werewolf = warm carried light: the temperature grammar becomes the fight's readability axis);
(iii) golem gait tolerates trace-driven locomotion better than humanoid gaits (foot-slide reads
as mass, not error). Fallbacks in order: FortGolem, SpiritDemon. Adds (if trace fields any):
dark-fantasy skeletons (Light/Heavy armor), already scene-proven in arena_*.tscn.

**Routing:** new cell **RIVAL-CAST** (drax) — import pack into the godot tree per the R-PC-2
Synty asset-home convention, rig-compat + retarget check on the lean (fallback chain on failure),
cold-emissive tint pass, casting verdict banked. Single-writer queue: BEAM-FIX (in flight) →
BEAM-CONE → RIVAL-CAST → SHADOW-UNIFY (unify then validates the shadow grammar + temperature
grammar on BOTH cast bodies) → TELL-DRESS → ROOM-DRESS → **LAP-1 WATCH** → LAP-2 (2c re-render).
Full run charter: `gandalf/notes/2026-07-31-baton-render-run-charter.md` (BR-1).

## Scope 23 (Matt ruling 2026-07-31) — BEAM-GRADE: gradient reversed — opacity emanates from the ground, full transparency at frame top

Matt, verbatim: *"I think we may want to reverse my lean before as when they are less translucent
up high in the camera view they can be a bit distracting. Let's have a gradient fade,
starting/emanating from the ground lighting towards complete translucent transparency as they
approach the top of the camera."*

- **The law:** beam opacity is MAXIMUM at the base — emanating from the ground lighting (the
  floor pools/slats the cones pin to) — and fades MONOTONICALLY to **complete transparency by
  the top of the camera view**. The old top-presence lean (visible upper shafts) is REVERSED by
  its author; the eye-approved reference set's upper-gain figures (top=11.00 territory) are
  SUPERSEDED at the top end — declared drift, not silent.
- **Composition with Scope 21 (cone law):** one unified rule falls out — **opacity ∝ proximity
  to the floor**, exactly co-varying with the cone's width. Base = widest AND most present;
  upward = narrowing AND vanishing. The beam becomes a single readable object: light standing
  on its pool, dissolving into the dark air above.
- **Composition with Scope 17 (gap law):** the gap-over-body clearance survives — the gradient's
  maximum sits at the beam BASE (perceptual pinning through the transparent fade base stands);
  "emanating from the ground lighting" reads as the pool being the SOURCE of the beam's
  presence, which is precisely the pinning Scope 21 demanded.
- **Composition with Scope 20 #5 (past frame top):** the geometric extension stands, but the
  screen-space acceptance ("no visible beam-end in-frame") is now satisfied by TRANSPARENCY
  rather than by extension alone — the fade IS the no-end guarantee. Upper-air "implied windows"
  reading (Scope 17) is henceforth carried by beam DIRECTION alone, not visible upper shafts.
- **Frame-referenced vs world-referenced fade (in-cell decision, conductor lean):** Matt's words
  are camera-referenced ("top of the camera"), but Scope 20 #2 ruled lights WORLD-STATIC — a
  screen-keyed opacity would reintroduce camera-coupled dynamics the staticity veto killed.
  **Lean: world-height fade, constants calibrated so transparency completes at the world height
  corresponding to frame top at the CAM-LOCK camera.** Same look at the locked framing, zero
  swim. Veto-open.
- **Routing:** ABSORBED INTO BEAM-CONE (no injection into in-flight BEAM-FIX; standing pattern).
  BEAM-CONE's charter is now: cone geometry (Scope 21) + reversed opacity gradient (Scope 23) as
  ONE shader surface. Gate G-1 (BR-1) gains a second clause: **G-1b — measured beam opacity at
  frame-top row ≈ 0** (tolerance named in-cell); pool-BASE identity check unchanged.

## LANDING — BEAM-FIX ✓ (2026-07-31; note `drax/notes/2026-07-30-beam-fix.md` `73ef50ff`; godot LOCAL `65cafec`, ahead 10)

All five Scope-20 rulings discharged at the CAM-LOCK camera, identity printed on every frame:

1. **CAMERA FIXED** — root cause one line: the deliverables script passed the INSTRUMENT pose
   (`arena_full`: 58 m / −41° / fov 40 / 17.05 px/m) for the two clips Matt watched. All verdict
   clips now at CAM-LOCK; rig re-verifies against GAL-CAM's published surface every run (anchor
   err −0.000/−0.001 px; worst box residual 0.032 m).
2. **PARALLAX RETIRED** — constants removed (not zeroed); staticity **0 px of 921,600, max
   channel Δ 0** across 22.6 m observer travel (before: 257,918 px). One-transform-chain
   coupling kept; pool-axis ≤ 4 µm on all 8 patterns.
3. **POOLS — MEASURED ANSWER to Matt's "what happened to them?":** the lamp's floor pool is
   **bit-identical between arms (0 px differ)**. What vanished is the **beam's own additive
   light lying on the floor — 71.4% of all light inside the pool footprint before, 7.1% after**
   (footprint added-luma ×3.25 darker). **The cause is the gap law itself** (Scope 17, Matt-ruled)
   lifting the beam base to 2.4 m. Lever proposed NOT applied: `SKY_ENERGY_REF` stays LOCKED at
   22.8 (partial ~30, full restoration ~74). **Conductor ruling R-BF-1 (veto-open): DEFER the
   lever** — Scope 23's reversed gradient puts MAXIMUM beam opacity at the base, which is exactly
   the light that left the footprint; BEAM-CONE re-measures footprint added-luma after
   cone+gradient land. Decision rule: if pool presence still deficient vs the SKY-2 accepted
   state, apply the partial lever (22.8→30) and re-measure; the full lever (~74) re-opens SKY-2's
   accepted brightness and is Matt's, not the run's.
4. **ONE SUN EXECUTED** — before-arm measurement: rooms 1 and 3 (the boss room) genuinely held
   TWO suns (47.999994° = 2× tilt). After: **0.000000° deviation on all 8 patterns.** Direction
   provisional/veto-open: az 137° / el 66°. Pool centres exact to 1 µm.
5. **LONGER BEAMS PASSED, screen-space** — frame-top census at 8 player positions incl. both
   worst cases: before 6 FAIL (11 visible ends) → **after 8 PASS / 0 FAIL** (top 11.0→32.0 m).
   Gain 0.26→0.22 restores p99 parity to exactly BEAM-REAL's accepted 1.024; VOID-1 A/C clean,
   B declared (35,363 px = 53.57% of void crossed by beam air-visual); LSTAT-2 NO DELTA.

**Reconciliation with Scopes 21/23 (banked while BEAM-FIX flew):** BEAM-FIX solved the apex
limit by turning the shaft into a **parallel PRISM** ("a cone cannot be lengthened past its own
apex" — sun at infinity ⇒ parallel rays; two rulings, one geometry change). **Scopes 21+23
supersede the SHAPE:** cone opening to the floor, apex-ward opacity → 0 by frame top — the
apex problem dissolves via TRANSPARENCY, not geometric extension. Carried forward from BEAM-FIX
into BEAM-CONE regardless of shape: the one-sun AXIS discipline (all beam axes parallel at the
provisional sun vector), the 8-position frame-top census instrument (now checks opacity≈0, G-1b),
camera-identity-on-frame law, and the new record law that **any intensity metric must name its
camera** (p99 parity 1.024 at CAM-LOCK vs 1.656 at judge pose, same gain).

**Overturns banked:** BEAM-REAL's "money shot cannot exist at player_lock" is FALSE (body and
beam co-frame at the game camera; P1 beam base row 343 vs player anchor row 397); BEAM-REAL's
pool-axis 0.000000 was a one-room measurement. **Three drax instrument failures committed-not-
hidden** (global-vs-room-local axis foot; ±lean_dir sign error exposed by impossible unanimity;
identity line reading an off-tree builder).

**At Matt's eye:** (1) the price of "no visible beam-end": beam covers up to **20% of the frame,
crosses 53.6% of the void** at the game camera — flagged, but Scope 23's fade is expected to
shrink exactly this; judge in motion AFTER BEAM-CONE's clips. (2) **Disk hazard: `tmp/beamfix/`
is 4.8 GB; the sandbox refused deletion for BOTH drax and the conductor.** One-command prune for
Matt (keeps clips/plates/keyframes/measurement peels):
`cd ~/Games/reincarnated-godot/tmp/beamfix/frames && rm -rf _ba _wk BR_lock_*.png BF_lock_*.png WALKBR_*.png WALK_*.png`

**Deliverables:** `tmp/beamfix/clips/BEAMFIX_before_after_watch_CAMLOCK.mp4` (watch first) ·
`BEAMFIX_room_walk_CAMLOCK.mp4` (three rulings in one motion) · `plates/PLATE_pools_diagnosis.png`
(fastest read).

**Routing:** BEAM-CONE FIRES NOW (Scope 21 geometry + Scope 23 gradient as one shader surface +
R-BF-1 pools re-measure). Then RIVAL-CAST → SHADOW-UNIFY per BR-1 §3.

## LANDING — BEAM-CONE ✓ (2026-07-31; note `drax/notes/2026-07-31-beam-cone.md` `902909ac`; godot LOCAL `811c320`, ahead 11; relaunch r2 — r1 stalled pre-edit at the stream watchdog, tree verified clean)

All five gates PASS; Scope 21 + Scope 23 live as one shader surface:

- **G-1 cone-base == pool: PASS** at ±5% pre-named tolerance — construction residual 0.000000 m;
  image-space 0.61%/0.91% at working levels; the 2%-level divergence ATTRIBUTED (rim
  stylisations `mask_gamma`/`edge_power`, which the pool never carries; peeled → 0.52%, slope
  93.8% of geometric), not thresholded away. **Slat law fell out free** — `beam_narrow` 1.00
  restores one sub-cone per slit, each pinned to its own floor slat.
- **G-1b frame-top opacity: PASS 8/8** — 0.000–0.928/255, zero pixels over 1 luma at row 0.
- **Staticity 0 px / VOID-1 crossing 53.60% → 0.00% / frame coverage 21.5% → 13.8%** (8-position
  range 4.0–18.3%) — **Matt's Scope-23 instinct measured true: the distraction figure went to
  zero.** LSTAT-2 NO DELTA (declared limit: L7 stage builds no skylight).
- **Pools (R-BF-1) — HALF RESTORED, decision rule fired as written:** Scope 23 alone
  0.379× → 0.556× of the SKY-2 accepted state (beam share 17.0% → 43.5%); partial lever
  `SKY_ENERGY_REF` 22.8 → 30 bought 0.622×; gain re-laddered (0.19) holding p99 parity 1.014.
  **OPEN AT MATT'S EYE: floor pools sit at 62% of the accepted brightness.** If his eye wants
  them fully back, the full lever (~74) is his one-word call (it re-opens SKY-2's accepted
  brightness); if the dimmer floor reads right under the new cones, nothing moves.

**Overturns banked:**
1. **The conductor's world-height fade lean is REFUTED by arithmetic** — at CAM-LOCK the frame
   top is a slanted plane (18.47 m near edge → 1.68 m far edge; no single world height works —
   the far edge would need 1.68 m, below the 2.40 m gap-law base). Shipped as **world × screen**
   — the two factors Matt's sentence names; screen half reads the CAMERA (not observer), so
   staticity survives. Declared cost: appearance not camera-invariant, peelable in one constant.
   Conductor accepts the overturn — the cell's arithmetic beats the conductor's lean; that is
   what veto-open leans are FOR.
2. BEAM-FIX's topology census PASS/FAIL superseded by G-1b (under Scope 23 a beam can never
   touch row 0 — "FAIL" there is the new law working); retained as diagnostic.
3. **`SKY_ENERGY_REF` is no longer 22.8** (now 30, per the R-BF-1 pre-registered rule; reverts
   in one line, paired with `SKY_SHAFT_ENERGY` 0.19 → 0.14).
4. Inherited defect fixed: legacy arms read LIVE constants (BEAM-FIX's "before" ran BEAM-REAL
   geometry at BEAM-FIX gain); every arm now reads its own frozen constant.

**Disk hazard CLOSED:** deletion worked this session; the published prune executed — beamfix
4.8 GB → 232 MB, free 13 → 17 GB, clips/plates/keyframes/peels verified intact. **Matt's
one-command item is WITHDRAWN.**

**Deliverables:** `tmp/beamcone/clips/BEAMCONE_before_after_watch_CAMLOCK.mp4` (watch first) ·
`BEAMCONE_room_walk_CAMLOCK.mp4` · plates `PLATE_pools_remeasure.png` / `PLATE_frame_top_G1b.png`
/ `PLATE_cone_base_G1.png` (136 MB total).

**Routing:** RIVAL-CAST fires now (BR-1 §3 cell #3). SHADOW-UNIFY next.

## LANDING — RIVAL-CAST ✓ (2026-07-31; note `drax/notes/2026-07-31-rival-cast.md` `e8aefafd`; godot LOCAL `b80d7d9`, ahead 12)

**CAST: `SK_BR_Character_ElementalGolem_01` — G-2 PASS, no fallback walked.** The strongest
possible compatibility result: the golem's rest pose is byte-identical to the werewolf's to four
decimals (head 1.6940 / hips 0.8763 / foot 0.0811) — **the boss IS the player's skeleton.**
Retarget 51 bones / 39 profile, rest-Δ 0.0000° mean AND max; 24-phase animation battery zero
inversion / zero collapse / zero non-finite. L6 law deliberately NOT applied (not needed in the
in-memory path; the werewolf's own import lacks it; one word away if ever needed).

- **Scale — pack-level finding:** NO Fantasy Rivals rig is natively boss-large (nine candidates
  span 1.79–2.05 m; the lean is 1.0015× the werewolf). "One of the larger rigs" is unreachable
  by selection — shipped **×1.5077 uniform → 2.75 m, 1.528× the player** (0.915× the masonry
  course). Veto-open.
- **Emissive:** tint READ from `SKY_COLOR` (0.620, 0.740, 1.000), not typed — boss glow and
  floor pools are one cold family by construction. Energy 0.50 off a five-rung ladder, 0.00%
  saturated, 102.6-point B−R separation against the warm floor. The temperature grammar is live.
- **Import was a verification, not a copy** — the pack has lived in the R-PC-2 home since the
  2026-06-21 ingest. GOVERNANCE FLAG (minor): two asset-home conventions coexist; the charter
  cited the minority form; drax followed the live majority. Convention unification = queue row,
  not a run item.
- Two drax instrument failures written down (a PASS scored on a 10/93-track unretargeted clip;
  a tint selector calling 96.6% of its bbox "the boss") — both caught in-cell, pre-verdict.

**Deliverable:** `tmp/rivalcast/clips/RIVALCAST_orbit_watch.mp4` (14 s, one revolution ending on
CAM-LOCK, boss cycling idle→walk→swipe beside the werewolf).

**Two items routed, not ruled:**
1. **Boss head enters the beam base** — 2.75 m boss vs the 2.40 m gap terminus (sized for a
   1.8 m body). Conductor lean: DO NOT move the gap law yet — cold emissive crossing a cold beam
   is the same temperature family and may read as intentional; and raising the terminus re-dims
   the floor pools (the exact 71.4% mechanism), coupling this to the pools-at-62% eye item.
   **One packaged brightness decision at the SHADOW-UNIFY landing, judged in motion.**
2. **The player reads as a dark silhouette at the game camera** — not texture (atlas means
   106/105/103): the carried lamp sits INSIDE the torso, lighting the floor and not the body.
   Routed to SHADOW-UNIFY as a charter item: in the D1 grammar the carried light must make the
   CARRIER readable — the hero is never the darkest thing in the room.

**Routing:** SHADOW-UNIFY fires now (BR-1 §3 cell #4) — the full cosmology cell, validated on
both cast bodies.

## LANDING — SHADOW-UNIFY ✓ (2026-07-31; note `drax/notes/2026-07-31-shadow-unify.md` `2045f1d2`; godot LOCAL `97cac6d`, ahead 13)

**G-3 PASS, all three clauses:**
- **One author:** 71 Light3D in the built level → **1 directional author, 0 non-directional**,
  8 sky spots alive at `shadow_opacity=0`. Key aimed by `sun_travel_dir()` — the SAME expression
  the beams are graded against: **one-sun deviation 0.000000°** across shadows AND shafts.
- **ρ spread 9.6%** (0.8623 dim / 0.9496 bright) vs inherited 10.2% FAIL; shadow-area span
  collapsed **478× → 1.14×** (the inherited state had 92 px vs 43,935 px shadows in ONE room).
- **Pools survive:** the landmine is REAL and was measured — `shadow_enabled=false` on sky spots
  costs the pool **56.3% of its p99**; shipped `shadow_opacity=0` instead: 1.028×/1.035×, inside
  the named ±10%.

**★ THE FINDING THE GATE WAS HIDING (spec question, routed):** ρ = 1 − author-share of local
floor light, so a DEEPER shadow NECESSARILY widens within-room bright-vs-dim spread. Reaching
SHADOW-CAL's ρ≈0.50 at ≤10% spread requires bright:dim floor ratio ≤1.11; ours is 1.47 (the
inhomogeneity is the cold sky pools, not the torches — dimming torches buys nothing).
**SHADOW-CAL's 0.482/0.565 pair was BETWEEN-SCENE; the G-3 gate re-used it as a within-room
check — the gate mis-composed two measurements.** Consequence: the shipped shadow is FAINT
(ρ~0.86–0.95, the deepest rung that passes the spread clause). The gate PASSED as registered;
the DEPTH question goes to Matt's eye: `UNIFIED_KEY_ENERGY` 1.00 (shipped, uniform-but-faint) vs
3.50 (matches the referent's absolute-contrast band, fails the spread clause the finding just
discredited). **Conductor lean, veto-open: the referent look wins — GD's shadows are READ-ABLY
deep, and a ~15% within-room ρ spread is likely imperceptible while a 14%-dark shadow is
functionally invisible; the spread clause should be re-derived from a within-room referent
measurement, not discarded silently.** Judged in motion at Matt's eye.

**Silhouette fix SHIPPED:** lamp +0.72 m camera-side at h 1.42 m (out of the torso). Hero luma
vs his pool **1.016× → 1.540×**; sub-floor-dark pixels 11.9% → 2.9%. Boss 1.73× baseline (its
unlit half declared — the cold emissive reads on the lit side). Carrier fill built, measured
+0.6%, honestly NOT shipped.

**Other gates:** staticity 0 px / LSTAT-2 NO DELTA; declared deltas: floor +2.3% luma and
**temperature inversion −44.84 → +17.11 B−R (warm→cold)** — at Matt's eye. **Fog-unlit A/B
verdict-shape:** it is a POOL-EDGE decision, not a beam decision — since the beam became a mesh,
un-lighting the fog changes only the haze skirt around the pools, nothing above 2 m.

**Boss-head-in-beam: captured, not ruled** (gap law untouched, crossing on film). Five drax
instrument failures on record — the best: the ρ census was reading DUST as shadow (unseeded
GPUParticles3D broke the NULL at 20,757 px; caught by the control, as designed).

**Deliverables:** `tmp/shadowunify/clips/SHADOWUNIFY_before_after_watch_CAMLOCK.mp4` (first) ·
`SHADOWUNIFY_fight_walk_CAMLOCK.mp4` (torch pass-by + boss beam-crossing + both readable) ·
`SHADOWUNIFY_fog_unlit_AB_CAMLOCK.mp4` · `plates/PLATE_shadow_rho_G3.png`.

**Packaged brightness decision NOW AT MATT'S EYE (one sitting, all in motion):** (1) shadow
depth 1.00 vs 3.50 · (2) floor pools at 62% · (3) boss head crossing the 2.40 m beam base ·
(4) room temperature inversion · (5) fog-unlit A/B. Five couplings, one lighting state — rule
them together off the SHADOW-UNIFY clips.

**Routing:** TELL-DRESS fires now (BR-1 §3 cell #5) — none of the five eye items block decal
work; any ruling lands as one-constant changes.

## LANDING — TELL-DRESS ✓ (2026-07-31; note `drax/notes/2026-07-31-tell-dress.md` `619c7c77`; godot LOCAL `30f83fc`, ahead 14; only file touched: `wr2_playback.gd`)

All five gates PASS:
- **T-1 radius truth:** declared 12.000 m → measured 11.939 m (−0.51%), per-azimuth local scale
  (no global px/m — at 53° pitch one number IS the error); 5 azimuths eaten by the arena wall
  excluded by geometry, counted.
- **T-2 timing:** nova 69/70 frames (−1); achieved by moving decals off `create_tween` onto the
  PLAYBACK CLOCK (trace time, not wall time — the right master for a sim render).
- **T-3 legibility:** rim/floor median ×3.355 — via the pre-authorised escalation: cold-on-cold
  DID fail against the cold pools, so the shipped rim is a SKY_COLOR-cold core + **0.14 m warm
  danger lip** — the one warm accent in the cold family, and it is the danger channel.
  Both bands inside true radius (the lit outer edge IS `radius_m`).
- **T-4 no regression, EARNED:** first pass failed at 393,347 px; three non-deterministic authors
  (tween numerals, unseeded dust, room ambient) peeled AT THE AUTHOR → final 29 px vs NULL
  floor 1. LSTAT-2 unchanged.
- **T-5 qualified switch:** rect renders (inherited centred-box semantics CORRECTED to run from
  the caster); unknown family → magenta fallback + warning; neither enters `_nova_verdicts` —
  the `:2435` corruption hazard is closed.

**Ring grammar shipped:** static rim = the WHERE; a front band travelling 0→radius over
`wind_up_s`, arriving at the rim exactly at `fire_tick` = the WHEN; 0.32 s shock burst. The
telegraph teaches its own timing — a first-time viewer can read when it will fire.

**⚑ CHARTER CORRECTION — R-BR-6 (conductor ruling, veto-open):** BR-1 §1 S-1 pinned Lap-1 to
`kitcal_g5/g5/traces/` — **that battery contains ZERO telegraph events** (it is the pre-telegraph
G-5 baseline). Telegraphs + the only `action_lock` frames live in `kitcal_g5/wr2_battery_after/`
(post-`bef1f55`, same phase-1 era, pre-2c). The g5 pin was the CONDUCTOR'S drafting choice, not a
Matt ruling — Matt's two-lap law distinguishes phase-1 vs 2c, not batteries. **S-1 is RE-PINNED
to `wr2_battery_after` traces** (R-BR-4 feature-coverage selection is unsatisfiable from g5).
Proven fixture: seed 74000806 — nova at 414.80, `action_lock` ticks 33–45, 2 crits, death 23.8 s.
Flagged at Matt's eye with this bank; his veto reverts one line.

**At Matt's eye (with the standing five):** (6) the decal lifts the floor inside the ring ×2.02
for 2.3 s — legibility over ambience as ruled; retreats on one constant.

**Deliverables:** `tmp/telldress/clips/TELLDRESS_before_after_watch_CAMLOCK.mp4` (first) ·
`TELLDRESS_nova_cycle_CAMLOCK.mp4` · `TELLDRESS_action_lock_x3slow_CAMLOCK.mp4` ·
`TELLDRESS_synthetic_shapes_CAMLOCK.mp4` · `plates/PLATE_T1_radius_truth.png`.

**Routing:** ROOM-DRESS fires now (BR-1 §3 cell #6). Then LAP-1 WATCH on the re-pinned substrate.

## LANDING — ROOM-DRESS ✓ (2026-07-31; note `drax/notes/2026-07-31-room-dress.md` `ab2105cc`; godot LOCAL `78043af`, ahead 15)

All four gates PASS:
- **D-1 clearance:** 0 props in the fight envelope (min 2.286 m vs the WHOLE 60-trace battery,
  not just the fixture — the law generalises to any Lap-1 fight); envelope = union of swept
  capsules, not a bounding box (a box would have forbidden 22.5×24.6 m of the arena). Telegraph
  disc: 0 footprints AND 0 camera-occlusion strips inside 12.0 m (the occlusion test is
  directional — a prop hides 0.7548 m of floor per metre of height along the camera bearing).
- **D-2 rooms distinguishable:** collapsed guardroom (131 props, the only cobwebs) / silted
  works (97, broad-flat) / boneyard (65, few-tall) / **boss stage 172 in 11 groups**; doorway
  bleed 152 pieces over 6 thresholds. Four registers, one old place.
- **D-3 zero lighting drift:** LSTAT-2 byte-identical · staticity 0 px · cold-pool footprint
  1.000023× · beam share identical to 3 decimals · zero constants touched — the five-item eye
  package reaches Matt EXACTLY as SHADOW-UNIFY left it.
- **D-4 perf:** +4.09% median frame time vs +25% budget (draw calls 323→543).

**Two eye-riders banked (join the package):**
1. **The clearance law's price is visible:** CAM-LOCK locks to the player; the player lives
   inside the envelope; therefore dressing sits at the frame periphery and the fought floor is
   bare. That is the law WORKING (D1/GD fight-floors are bare for readability) — lever is the
   2.00 m margin if Matt wants dressing closer.
2. **Dressing reads by silhouette, not brightness** (prop-to-floor contrast 1.0262×) — a SIXTH
   rider on the shadow-depth clause: if Matt rules `UNIFIED_KEY_ENERGY` 3.50, the dressing gains
   contrast for free; drax honestly did NOT pre-brighten to hide the coupling.

**Deliverables:** `tmp/roomdress/clips/ROOMDRESS_before_after_watch_CAMLOCK.mp4` (first) ·
`ROOMDRESS_four_room_walk_CAMLOCK.mp4` · `plates/PLATE_D2_four_rooms.png` / `PLATE_D1_clearance.png`.

**Routing:** **LAP-1 WATCH fires now** (BR-1 §3 cell #7) — the integrated deliverable.

## LANDING — LAP-1 WATCH ✓ (2026-07-31; note `drax/notes/2026-07-31-lap1-watch.md`; godot LOCAL `be576c7`, ahead 16) — **BR-1 TARGET T-1 DELIVERED**

**G-4 PASS: 11 PRESENT / 1 PARTIAL**, every item frame-stamped. Seed 74000806 unchanged from the
conductor's pick; all four feature classes on screen.

- **Boss-ID (R-BR-1) triple-verified:** max-HP ∧ id-prefix ∧ roster-tier all agree —
  **`boss&quest_slith_wightmirecave01_0`, 14,812 HP: PRIMORDIAN, THE FORGOTTEN ONE.** The watch
  renders the very boss whose Grim Dawn fight is the run-family's acceptance fixture (R-KC1-22).
  `is_boss` reads FALSE on the correct actor, exactly as the ruling predicted.
- In-situ re-verification: TELL-DRESS radius 11.953 m (better than banked), burst −1 frame;
  one-sun shadows on BOTH bodies; staticity 3 px over two launches; LSTAT sha unchanged; zero
  lighting edits (shaders byte-identical to banked).
- **The one PARTIAL:** werewolf in-motion readability 1.288× vs the 1.540× static standard.
- **Worst declared debt — the player MOONWALKS:** heading faces the boss 97.9% of ticks while
  velocity points away; 93.2% of moving ticks are backwards on forward-only clips (median
  4.18 m/s lateral slide). The strafe/backpedal clips exist ON DISK, unretargeted. **Fix folds
  into the next drax write-cell** (strafe retarget + velocity-vs-heading blend).

**R-BR-7 (conductor ruling, veto-open) — Arm-A default drift:** `wr2_playback.gd::_pl_arm`
defaults to "B" (NO carried lamp), against Matt's standing Scope-12 ruling. LAP-1 WATCH rendered
correctly (flag passed, arm printed on-frame); but TELL-DRESS + ROOM-DRESS clips were cut on the
rejected B baseline. Ruling: the default FLIPS to "A" in the next drax write-cell (implements a
standing Matt ruling — not a new lighting decision); until then every render passes the flag
explicitly. **Consequence for the sitting: judge lighting off SHADOW-UNIFY + LAP-1 clips (Arm A);
the TELL-DRESS/ROOM-DRESS gates are arm-internal and stand.** Drax's restraint (did not move the
default with the package open) was correct.

**Lap-2 gate G-5 CHECKED — OPEN, riders 1/3:** newest on-disk wr3 batteries (`wr3_battery_after_s11`
+ `_s11_det`, 220 traces censused) carry `attack_id` but **zero files with `family` or
`icearmor`**; `wr3_stage2c/` holds only the report JSON, no traces. Per the charter's honorable
fallback: **Lap 1 IS the deliverable; Lap 2 parks armed**, firing when full-rider traces land
(one census command re-checks). Strafe retarget + R-BR-7 default flip ride with it.

**Eye-package CONSOLIDATED (one sitting, all in motion):** ① shadow depth 1.00 vs 3.50 (conductor
leans 3.50; dressing contrast rides free) · ② pools at 62% (full lever = SKY_ENERGY_REF→~74) ·
③ boss head crossing the 2.40 m beam base (lean: leave it) · ④ room temperature inversion ·
⑤ fog-unlit A/B (pool-edge decision only) · ⑥ decal floor-lift ×2.02 for 2.3 s · ⑦ numerals
cover >50% of the hero for ~1.9 s (charter §14.17's question at watch scale) · ⑧ R-BR-6 substrate
re-pin + R-BR-7 arm default (both veto-open rubber-stamps).

**THE WATCH:** `tmp/lap1watch/clips/LAP1_WATCH_full_fight_CAMLOCK.mp4` (27.80 s) ·
`LAP1_WATCH_highlights_CAMLOCK.mp4` (nova/action-lock/crit/death, ×1 + ×0.5) ·
`plates/PLATE_G4_checklist.png`.

---

## Scope 24 — MOB BODIES (Matt ruling, 2026-07-31, post-LAP-1-WATCH review)

Matt verbatim: *"The enemy combatants which are not bosses (I'm unsure if they are trash/pack/etc)
do not have skeletons, rigs, characters or animations. They are still geometric blobs. Please
ensure they are skinned and animated with their movements and attacks."*

**Binding:** every non-boss actor in a rendered trace gets a skinned, rigged, animated body —
movement locomotion AND attack animations. No geometric proxies in any Matt-facing render from
this scope forward. Substrate note: the newest batteries enumerate the non-boss cast directly
(`trash__none`, `champion__none`, `mixed_pack__none` traces per seed) — the cast list is
countable before casting. Bodies: Fantasy Rivals pack (20 SK rigs, R-PC-2 asset home) + the
scene-proven L6 registry; drax holds rig-quality say per R-BR-5's pattern.

## Scope 25 — BOSS/COMBAT VFX BAKE-OFF + STRIKE-CONNECT (Matt ruling, 2026-07-31)

Matt verbatim (compressed, full text in session): boss skills/attacks must NOT render as
geometric shapes — *"the boss monster has VFX as this is probably the 100% most important part
of the bake-off."* He wants **phase-1 AND 2c scenes with VFX bake-offs**: arms = (a) VFX from
catalogues in the asset folders, (b) VFX created by drax via Murzak/MCP, (c) **combinations of
both** — try different combinations. Sequencing law: if 2c is consumable before phase-1 VFX work
begins, phase-1 VFX may be skipped; otherwise phase-1 VFX work fires (it supports phase 2).
Census at banking: 2c traces NOT on disk → **phase-1 VFX work fires.**

**Strike-connect sub-ruling:** boss hand-attacks and werewolf claw-attacks must VISIBLY connect —
prefer farther-reaching attack animations where they exist; swipes must cross the target body.
On top: **physical claw & strike VFX attached to the melee animations** ("for juice") — both
combatants.

## Scope 26 — BEAM BASE-PIN 100% + GRADUAL GRADIENT (Matt ruling, 2026-07-31)

Matt verbatim (compressed): beams getting better; two updates. **(#1)** beams pinned **100%** to
the ground shape — slat-beams currently cover only ~5–10% of the length of the ground-lit slats;
circle has the same defect, milder. The beam's base footprint must equal the lit floor shape,
full length/full disc. **(#2)** extend the non-transparent blue light/particles HIGHER and make
the solid→transparent gradient **much more gradual** — current falloff reads near-instant, wrong.
Solid at the floor, gradual fade, transparent by frame top (Scope 23's endpoint law unchanged;
the CURVE between endpoints is what changes).

## Ruling — Lap-2c PRE-RATIFIED (Matt, 2026-07-31)

Matt verbatim: *"Lap2c is completing the owner-eye render right now, and I have
PRE_RATIFIED/CERTIFIED it for use within your scene here. Please review what's available now and
switch now if you can; if not, keep an eye out for the rendering that you need to swap to phase
2c and save yourself time."*

**G-5 status change: the gate's Matt-authorization clause is now PRE-CLEARED** — when rider-bearing
2c traces land on disk, the swap fires WITHOUT a fresh Matt halt (schema spot-check still applies).
Census at banking (2026-07-31): newest emissions Jul 30 16:45; `wr3_stage2c/` report-only; 0 files
with `family`/`icearmor` anywhere under `kitcal_g5/`. **Re-census at every cell boundary.**

**Cell sequence for the fix lap (conductor sequencing, veto-open):**
1. **MOB-CAST** (Scope 24) — + carries the two standing debts: R-BR-7 Arm-A default flip +
   moonwalk strafe retarget (velocity-vs-heading blend).
2. **BEAM-PIN2** (Scope 26) — small, independent; lands before the bake-off so audition clips
   carry corrected beams.
3. **VFX-BAKEOFF** (Scope 25) — the most important surface, cut LAST so Matt judges VFX arms
   against the fully-dressed scene (skinned cast + pinned beams), not against blobs and
   mis-pinned light. If 2c traces land mid-lap → swap substrate at the next cell boundary
   (PRE-RATIFIED above).

Rationale for VFX-last despite VFX-most-important: the bake-off is a JUDGMENT surface — M-EYE
verdicts on VFX arms are contaminated if every clip also contains known-wrong cast/beam defects.
Dress the stage before the audition.

---

## LANDING — MOB-CAST ✓ (drax, 2026-07-31; godot `a0bfb88` LOCAL; landing note `drax/notes/2026-07-31-mob-cast.md`, meta `36395eb7`)

**Scope 24 PASS — the blobs are bodies.** Census widened to the whole battery of record (450
traces): **7 mob kinds over 3 roster tiers** (fixture shows only 3). Cast table banked in the
landing note: Primordian ×1.5077/2.75 m · Thundersnout→Pig_Butcher 2.30 m · Eastmire
Warrior→Troll 2.15 m · Deepmire Vanguard→Medusa 2.00 m · Deepmire Evocator→ForestWitch 2.00 m ·
Eastmire Herder→Big_Ork 1.65 m · Walking Dead→MutantGuy 1.65 m. Ladder: swarm 1.65 < player
1.80 < elite 2.00–2.30 < boss 2.75. **Scale keys off roster `tier`, not max-HP** — on 270
non-boss files the max-HP actor is a zombie/troll/boar; the naive reading ships a 2.75 m Walking
Dead. R-BR-1 ∧ `tier=="boss"` agree 180/180 where a boss exists. NO-BLOB: 4/4 rigged, zero
capsules, no code path returns a proxy. Import 9/9 clean, 0 non-finite samples.

**R-BR-7 PASS both directions** (no-flag → `E1 ARM A`; `--playerlight B` still reachable).
**Moonwalk PASS:** player 5.88% → **100.00%** velocity-octant match (boss 97.48→100, escort
84.34→100, 0 unserved, 1,310 moving frames).

**Instruments caught pre-ship:** (1) left/right inversion in drax's own new blend code — `+Z`-forward
Synty bodies have LEFT on `+X`; first sign choice would have shipped confident wrong-way strafes
on all 7 off-axis labels; (2) emissive mask renders nothing on 7/8 bodies (golem 49.11% verts,
rest 0.00%) → replaced with mask-free cold glow, A/B'd +13.49 B−R (21.28% of warm bias);
(3) SIGSEGV from mutating a playing AnimationPlayer's library (LAP-1 latent, 3 clips hid it).

**Debts (named, not hidden):** sprint-strafe gait gap (87.7% of off-axis frames one gait rung
slow — octant right); one generic swing on every body (goblin idle-fidget swipe is the tree's
only attack-shaped clip — **Scope 25 owns per-body strikes**); 4/7 bodies parade-verified not
fight-verified; shadow gate NOT re-measured on the five-body scene (**BEAM-PIN2 or VFX-BAKEOFF
must re-check SHADOW-UNIFY's one-author law**); AGENT_STATE no MOB-CAST entry; `tmp/mobcast/`
~1.6 GB unpruned.

**WATCH:** `tmp/mobcast/clips/MOBCAST_full_fight_CAMLOCK.mp4` (27.80 s) · escort closeup ×0.5 ·
`MOBCAST_full_fight_WIDE.mp4` (CAM-LOCK loses escorts at 6.51 m median separation — framing
question for Matt) · `MOBCAST_cast_parade.mp4` (verifies the 4 kinds the fixture never shows).

## FINDING — single-writer collision + `family` dropped at the seam (2026-07-31)

**F-BR-1 (process):** a concurrent drax cell from run WR3-KITE-COMMIT (`8fafc73`, 09:24 — the
owner-eye render Matt announced as "Lap2c is completing… right now") committed mid-MOB-CAST in
the shared godot tree, carrying MOB-CAST's in-progress `wr2_playback.gd`/`wr2_actor_rig.gd` edits
(provenance declared in good faith from both ends; no history rewritten; coupled files kept
together — the right call). **Root cause is structural: two Matt-authorized runs share one godot
working tree.** Drax's recommendation stands as a queue row: `git worktree` per write-cell makes
the collision impossible. Routed to knight-rider/jack-ryan as process finding; BR-1 mitigation
meanwhile: conductor checks godot `git log` freshness at every cell boundary (this entry is that
check firing).

**F-BR-2 (substrate, gate-G-5-critical):** the WR3 cell measured that **`TelegraphSpec.family`
is minted engine-side and then DROPPED at `ReplicaFrameSink.telegraph()`** — 0 occurrences in
13,573 records; the sink builds its record key-by-key and never copies `family` across. Fourth
instance of the emitter's own named defect class. **Consequence: NO future trace can carry
`family` until the engine seam is fixed** — G-5's 3-rider census would wait forever on a field
the pipeline cannot emit. **G-5 amended (conductor, veto-open):** swap criterion becomes
rider-bearing 2c traces with `attack_id` + `icearmor` present; `family` served by TELL-DRESS's
ladder rung (b) substring sniff (already carrying the discriminator; 47.2% of that battery's
circles are the blizzard) until the seam fix lands engine-side. Cell-boundary census at MOB-CAST
close: still zero `icearmor` anywhere under `kitcal_g5/`; newest dirs report-only.

---

## LANDING — BEAM-PIN2 ✓ (drax, 2026-07-31; godot `d472c1a` LOCAL; landing note `drax/notes/2026-07-31-beam-pin2.md`, meta `d5faef06`+`95a3fb96`)

**Scope 26 #1 base pin — root cause was structural, not tuning: the beam did not EXIST at the
floor.** Scope 17's gap law clipped below 2.40 m; lowest drawn cross-section was 84% of pool
width, carried 1.07 m sideways by the lean. G-1 passed at 0.0000% because it extrapolated to y=0
where nothing was drawn and never measured slat LENGTH — a gate measuring the wrong shadow of the
question. AFTER: **slats 100.00% length / 97.67% width** (from 77.5/76.4); circle 89.88% length /
77.49% width (from 68.0/60.0) — residual attributed structurally (chord→0 at silhouette; pool
carries bounce+sheen a volume can't; ×4 gain buys only 1.9 pts). Geometric clause printed every
build: ratio 1.0000, displacement 0.0000 m. **Declared cost: Scope 17's gap law + the
"player walks UNDER the beam" shot are RETIRED by Scope 26.**

**Scope 26 #2 gradient — the constant was never what fell:** at optical depth 0.34 the beam never
saturated, so cone WIDTH authored the falloff. Shipped density 0.90 / pow 0.60 / gain 0.175
(p99 parity held) / motes ×2.1. Profile after (own-peak): circle 0.571/0.689/0.942/0.685/0.023 ·
slats 0.684/0.761/0.861/0.525/0.011 — frame-top law holds (G-1b 8/8).

**Shadow gate on the five-body scene (MOB-CAST debt): PASS all three clauses, BETTER than
two-body** — ρ spread 3.06% (was 9.6%), 71 lights / 1 directional author / 0 non-directional,
pools bit-identical to BEAM-CONE.

**Finding — fog is the last lever on "solid at the floor":** E3 room fog eats ~45% of the shaft
below the 3.006 m wall course despite the shaft's `fog_disabled`; with fog peeled the same build
is MONOTONE from the floor (1.000/0.975/0.896/0.651/0.022). Out of scope, unfixed → **Matt eye
item** (composes with the standing fog-unlit A/B fork, item ⑤).

**F-BR-1b (process, push side):** the concurrent WR3 run's 09:25 push published godot
`65cafec..49209b6` — **BEAM-FIX through LAP-1 WATCH are on origin/main**; every BR-1 landing's
"LOCAL, not pushed" is stale through no fault of its author. Not remediated (undo = force-push).
Verified at cell boundary: origin/main = `49209b6`; still local-only = `a0bfb88` (MOB-CAST) +
`d472c1a` (BEAM-PIN2). **Matt's push-authorization ask now covers only these two.**

**Debts:** fog attenuation (Matt fork) · circle 89.88% · AGENT_STATE missing two entries ·
topo-vs-base-slice gate variant choice for a future cell. Disk healthy (148 MB).

**WATCH:** `tmp/beampin2/clips/BEAMPIN2_before_after_watch_NOHUD_CAMLOCK.mp4` +
`BEAMPIN2_gradient_tilt_BEFORE_AFTER.mp4` · plates G26a/G26b.

**Cell-boundary census:** zero new `.jsonl` since 07:00; zero `icearmor` anywhere → VFX-BAKEOFF
cuts on the **phase-1 substrate** per Matt's sequencing law ("do the phase 1 work as it will
support phase 2").

---

## LANDING — VFX-BAKEOFF ✓ (drax, 2026-07-31; godot `fd21756` LOCAL; landing note `drax/notes/2026-07-31-vfx-bakeoff.md`, meta `ec3695f7`)

**Scope 25 delivered — four arms, no self-verdict, Matt judges.** Single-writer held (opened
`d472c1a`/origin `49209b6`, no foreign commits). Cell-boundary census: 2c still report-only,
zero `icearmor` → phase-1 substrate per Matt's law.

**Catalogue census (arm a):** 10 Binbun categories staged, 230 effect scenes reachable, 26/27
shortlist USABLE (gate refuses any `.tscn` that doesn't load AND own a draw-capable node).
Honest negatives: `addons/vfx_library`'s 32 effects are ALL 2D (unusable in the 3D fight);
vaportrail + yparticles3d GDExtension binaries absent. Ten per-pack `class_name VFXController`
collisions resolved via merged per-file tree, 92 byte-conflicts all → incumbent, all printed.

**Arms (all 3/3 element coverage, 0 spawn fails):** `A_cat` pure catalogue · `B_mcp` pure
Murzak/MCP (113/113 wire calls OK) · `C_combo` catalogue+MCP same-event · `C2_combo` MCP burst +
catalogue flash lead. Control: pixel-diff Δ190–236 at damage beats across all ten pairs — the
arms GENUINELY differ; combos distinct from each other. **THE JUDGMENT SURFACE:
`tmp/vfxbakeoff/clips/VFXBO_QUAD_4arms_NOHUD_CAMLOCK.mp4` + `VFXBO_BEATS_QUAD_halfspeed.mp4`.**

**Strike-connect — the planned fix was the wrong fix, measured first:** surface gap 0.000 m on
all 39 strikes (the sim already touches); NO displacement invented. Real defect: 9/11 strike
clips addressed `Skeleton3D:pelvis` and bound ZERO tracks — inert. Post-retarget-bake the
werewolf's swing reach 0.8493 → 1.7671 m (×2.08), crossing the boss surface 1.267 m.
**Strike-cross 35/40 = 87.50%** (5 misses are cone-AoE secondary victims a hand-swing correctly
can't reach). Per-body: 41 own-clip swings, 0 generic fallbacks — honestly: incumbent wins 5/8
bodies because Fantasy Rivals + werewolf packs ship ZERO animation FBX.

**F-BR-4 (process):** the standing SIMPLE-asset gate is **RED — 900 violations** (simple-dungeons
516 · simple-town 384); last PASS 2026-06-20, unrun since. Not this run's to fix → queue row to
knight-rider/jack-ryan alongside F-BR-1's worktree row.

**F-BR-5 (Matt fork):** the guard cannot see `polygon-simple-fantasy`, which holds
`Animations_Melee.fbx` — the tree's ONLY real melee animation bundle, exactly what Scope 25
wanted, NOT used. **Needs Matt's ruling: is retargeted SIMPLE *animation* (mesh never on screen)
inside the POLYGON-only intent?** If YES, a small follow-cell upgrades the 5/8 incumbent-winning
bodies with real melee clips.

**Self-caught pre-verdict:** stale global-pose cache (Δ0.000000 vs 0.988433), two wrong
hypotheses recorded, `apply_particle_preset` silently stomping node config while returning OK
47× (standing Murzak hazard, banked), `--import` stripping `[rendering]` (restored, NO-DELTA).

**Debts:** staticity bar holdable-not-held · `tmp/vfxbakeoff/` ~8.2 GB (prune sandbox-denied —
Matt one-command or next cell) · nova identical across arms by construction (TELL-DRESS owns it) ·
AGENT_STATE 3 behind · MCP lab editor left running.

**Fix-lap CLOSE:** Scopes 24/25/26 all delivered. Godot local-only chain now THREE:
`a0bfb88` + `d472c1a` + `fd21756`. Lap-2c swap stays armed (PRE-RATIFIED; census at every
boundary; F-BR-2 sniff amendment governs `family`).

---

## G-5 OPENS — the 2c baton lands (Matt handoff, 2026-07-31 evening-session)

Matt verbatim: *"The above seed is provided by the battle simulation session as the handed-off
baton!"* Substrate: **`tmp/wr3acc/traces/boss__FULL__seed74000909.jsonl`** (462 frames; accepted
fight per Matt: never touches a wall, dips to 65% HP, 0.57 pools taken; W-2 dormant→alert boss
wake on screen). Census: `attack_id` ×66 · `icearmor` ×121 · **`family` ×9 / 9 telegraphs** ·
`dormant` ×175 / `alert` ×5. **Riders 3/3 — exceeds even the pre-F-BR-2 criterion; the sniff
amendment is unneeded on THIS trace.** Reference clip: `tmp/wr3acc/clips/WR3ACC_full_74000909.mp4`
(36 s). Godot head now `0601a04` (WR3-ACC seed-selection cell, other session). **PUSH AUTHORIZED
standing** (Matt: "feel free to push now and as you go") — all BR-1 godot commits published;
F-BR-1's push clause is mooted going forward.

## Scope 27 — BEAM V3: one issue + three tweaks (Matt ruling, 2026-07-31)

1. **(ISSUE) Slat direction disjoint:** floor-lit slats face diagonal-RIGHT while their beams
   face diagonal-LEFT — "very bad disjoint look." Beams and floor slats must share one direction.
   (Suspect class: the ±lean sign family MOB-CAST caught in blend code — same genus, light side.)
2. Beams too opaque overall — MORE transparent/translucent across their ENTIRE height.
3. **Frame-top law REVERSED (supersedes Scope 23's endpoint + G-1b):** beam tops must NOT be
   visible inside CAM-LOCK — "at least some small level of opaque light energy can be seen at
   the top and slightly above the cam-lock view." Light must feel like it comes from above frame.
4. No tightening-to-a-point in view: plenty of cone width stretching far up toward the crypt
   ceiling where sun would enter. (Composes with 3: the visible cone segment reads as a shaft
   continuing upward, not a spike terminating.)

## Scope 28 — VFX verdict + the Unity-translation direction (Matt ruling, 2026-07-31)

Bake-off verdict: **no arm wins outright; lean C/C2** (C vs C2 indistinguishable at his eye).
Two named misses: **(a) swipe-feel** — "I don't feel the player character's swings which is very
sad for a werewolf fantasy"; **(b) the boss AoR Ultimate has no VFX** (now "star-geometry" in
the 2c clip, with new attacks/skills to cover). Direction to ultra-think (conductor): purchasing
**Unity VFX packs and translating them** (Blender / MCP-node additions / our OWN MCP
disassembler) — catalogue VFX are "best assets so far but likely far too few and not quite the
correct ARPG register/feel." Purchase = Matt commitment-boundary; exploration + scouting fires
now. Conductor's decomposition: swipe-FEEL is partly juice MECHANICS (hit-stop, impact flash,
camera impulse), not particles — routed as JUICE sub-scope of the restage.

## Scope 29 — Grim Dawn screen-size parity (Matt ruling, 2026-07-31)

Player/monsters/boss "appear far smaller within the screen than the Grim Dawn" equivalents; make
them "exactly the same." Conductor's method ruling (veto-open): this is a CAMERA question, not a
body-scale question — bodies are meters-true against level geometry (MOB-CAST ladder banked);
the fix is dolly/framing within the GAL-CAM pinhole family. Measure first: galadriel computes
hero/boss screen-height fraction in GD reference captures vs our CAM-LOCK renders; drax closes
the gap to tolerance; overlay verifies.

## Shadow question (Matt asks "why am I not seeing shadows on characters — do I need to rule?")

**YES — this is standing fork ① (shadow depth).** Shipped `UNIFIED_KEY_ENERGY=1.00` renders
character shadows near-invisible by construction; pool-projector shadows ship `shadow_opacity=0`
(pools-vanish reconciliation). The 3.50 arm is the visible-shadow arm (conductor lean). BEAM-V3
cell cuts a character-shadow A/B (1.00 vs 3.50, same beat) so the ruling lands on evidence.

## Prune policy (Matt: "we must prune… without losing data we need")

`tmp/*/frames/` = 15 GB of the 21 GB, ALL regenerable (per-cell RUNBOOK/scripts re-render from
traces + scene). Data of record = clips + plates + traces + measure scripts + landing notes
(small, all referenced by ledger). Conductor's rm was sandbox-DENIED (second occurrence) → one
Matt command: `cd ~/Games/reincarnated-godot/tmp && rm -rf */frames`. Superseded-generation
clips (beamfix/beamcone/sky2/ambrise/ambhue/beauty/integ/wr1/wr2 …) are candidates for a second
pass ONLY after Matt confirms review-done per surface.

**Fix-lap-2 cell sequence:** 1) **BEAM-V3** (Scope 27 + shadow A/B) — drax write-cell;
galadriel **GD-PARITY measure** (Scope 29) + legolas **VFX-pack scouting** (Scope 28) run
parallel read-only. 2) **LAP-2C RESTAGE** on 74000909 — full dressed stage, C2-lean VFX interim,
W-2 dormant→alert rendering, new-skill telegraph mapping via `family` (native!), JUICE sub-scope,
GD-parity camera if measured. 3) VFX-UNITY spike gated on Matt's purchase ruling.

---

## LANDING — VFX-SCOUT ✓ (legolas, 2026-07-31; findings `legolas/research/2026-07-31-unity-vfx-translation-scout.md`, meta `f538ef6a`)

**License gate GREEN:** current Asset Store EULA (2024-12-04) has NO engine restriction — §2.2.1(a)
grant is engine-agnostic; §2.2.1(e)+§6 expressly permit modification; reverse-engineering clause
scoped to Services SDKs only (extraction is inside the grant). **Binding constraint for our MCP
idea: §2.2.1.1(g) forbids AI/ML training inputs → the disassembler must be a DETERMINISTIC
PARSER, never a generator** — honored from design day one.

**Shortlist:** ① **Polygon Arsenal (Archanor, $40, Shuriken/Built-in)** — ships `Ground Slam`,
`Nova (9 types)`, `Melee & Sword (14 types)` + `Cleave`: Matt's two named misses BY NAME; 1,383
prefabs, 100+ custom meshes, low-poly register (look lives in MESHES → ports losslessly).
② Magic Arsenal ($30) second. ③ Epic Toon FX under-register, skip. **Ranking inversion vs June:
Hovl moved look into Shader Graph (untranslatable) — excluded.** Translatability is a property
of the PACK: art-carried translates, shader-carried doesn't.

**Feasibility:** `.unitypackage` = gzipped tar; `.prefab` = plain YAML; Godot 4.3+ imports FBX
NATIVELY (Blender off the critical path — no Shuriken importer exists, its real jobs are
flipbook baking + pivot repair). **No Shuriken→Godot translator exists anywhere** (Unidot omits
ParticleSystem) — if wanted, we build it; ~14/23 Shuriken modules map cleanly (flagged as
inference).

**Native-Godot pool EXHAUSTED, measured:** AssetLib = zero ARPG content packs; Matt already owns
~the entire native pool (49 Binbun packs / 390 scenes — the rejected bake-off sampled a
near-complete library, making his verdict decisive); both hero needs score literal ZERO against
installed assets. Exception: **Binbun `Battle FX` (~$6, claws/swings/flying slashes) NOT
installed — cheapest swipe shot, worth taking regardless.**

**Pre-purchase check (free, 5 min):** Polygon Arsenal's live WebGL demo — do Nova + Ground Slam
read HEAVY or clean-and-light? The one register judgment a product page can't settle.
Caveats: itch.io HTTP 521 all run (Binbun pricing unverified); Gabriel Aguiar not properly
surveyed — flagged, not guessed.

**→ Matt purchase decisions queued:** D-VFX-1 Polygon Arsenal $40 (after WebGL check) ·
D-VFX-2 Binbun Battle FX ~$6 (unconditional lean YES) · D-VFX-3 Magic Arsenal $30 (defer until
Arsenal-1 verdict lands at the eye).

---

## R-BR-8 — SHADOW DEPTH RULED: 3.50 (MATT-SIGNED, 2026-07-31)

Matt verbatim: *"on shadows - go with 3.5"*. `UNIFIED_KEY_ENERGY` 1.00 → **3.50** becomes the
shipped default. Standing fork ① CLOSED. Implementation: next godot write-cell (2c restage) —
BEAM-V3 was in flight when the ruling landed and completes as chartered (its A/B remains the
evidence artifact). Character shadows become visible by construction; pools survival at 3.50 to
be re-verified at implementation (pools-vanish landmine check rides along).

## D-VFX-1 EXECUTED — Polygon Arsenal PURCHASED (Matt, 2026-07-31); download blocked on Unity-Editor-only delivery

Matt purchased Polygon Arsenal; Asset Store offers only "Open in Unity" (no direct download —
Asset Store delivery requires the Unity Editor's Package Manager; there is no browser download
link by design). **Unblock path (Matt host-level, one-time):** install Unity Hub + a free
Personal-license LTS editor (minimal, no platform modules), sign in with the purchasing account,
empty 3D project, Package Manager → My Assets → Polygon Arsenal → Download/Import. The
`.unitypackage` lands at `~/Library/Unity/Asset Store-5.x/` (or imported files under the
project's `Assets/PolygonArsenal/`). Everything downstream (untar, FBX/PNG harvest, YAML parse)
is ours and needs Unity never again — though keeping the editor enables the Option-C flipbook
bake harness later. Disk: Matt pruned further; headroom ample.

---

## LANDING — GD-PARITY ✓ (galadriel, 2026-07-31; note `galadriel/notes/2026-07-31-gd-parity-measure.md`, meta `eb170b51`) — CONDUCTOR'S CAMERA-ONLY RULING OVERTURNED

**The camera is exonerated by identity: our camera IS Grim Dawn's camera** — CAM-LOCK reproduces
GAL-CAM §4's decision surface to the metre (−17.660/+17.587/+15.211/−7.020 vs GD-derived
−17.66/+17.57/+15.21/−7.02). With the camera equal on both sides, screen size IS world size —
a dolly divides out of the ratio it's asked to fix. Scope 29's method ruling (camera-only)
is OVERTURNED by measurement; instrument self-validated (reads 2.74 m on a 2.75 m rig).

**The gap: werewolf 5.69% of frame vs GD 14.77% — 2.59× short.** Decomposition 1.29× × 2.10×:
the 2.10× is `wr2_playback.gd:1541 RIG_PLAYER_H := 1.80` — **a HUMAN height applied to a
werewolf rig.** GD's Lycanthropy doubles the silhouette; our transformation changed the mesh
and kept the height. Galadriel's closing line, banked verbatim: *"We built the world to the
metre and then put a man's height on a wolf."* Boss÷player proportion is ALREADY GD-correct
(1.46 both sides). Camera levers priced and rejected at k=2.59: decision surface ±17.6→±6.8 m,
frigidring (10 m) entirely off-screen = undodgeable telegraph, escort band unfittable.

**Decision fork (routed):**
- **D1 — werewolf form multiplier ~2.1× (conductor rules IN-RUN, veto-open): fold into the 2c
  restage as a graded A/B** — one constant, no geometry cost, 0.78× of GD parity, gradeable
  against this note's numbers. Fantasy-correct (Lycanthropy convention) AND composes with
  Matt's "I don't feel the swings" — a wolf at man-height cannot loom.
- **D2 / world-scale (MATT):** full "exactly the same" requires the WHOLE cast ×~2.6 with the
  1.46 ratio preserved — boss → ~7 m in a room with 3.0 m wall courses and a 2.40 m beam base:
  metric-truth vs architecture collides head-on. The honest full resolution is a STAGE-scale
  question (ARPGs oversize architecture relative to bodies), not a body hack — SCENEWRIGHT
  territory, Matt's ruling, informed by the D1 A/B at his eye.
- **CANNOT-ANSWER carried:** GD boss reference is occluded in all 313 corpus shots (21.6%
  indicative only) — NO boss-rig tuning against that row until re-measured. Threat-inversion
  guard: D1 alone makes the player (3.78 m) outgrow the boss (2.75 m) — the A/B must show Matt
  this consequence explicitly before any default flips.
