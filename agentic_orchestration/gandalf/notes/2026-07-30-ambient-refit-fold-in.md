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
