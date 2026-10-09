extends Node3D
# ============================================================================
# eor_kc2_fx.gd — C-9 R-C9-143 (lane EOR2, drax, 2026-10-02). THE EYE OF RECKONING THAT MATT WATCHED, PORTED.
#
# ⚑ SOURCE: reincarnated-godot scripts/kc2_player_channel.gd (sha256 e8c0c4ac3cdd...2f5dda3, last touched
#   34dcd41 2026-08-13 "A2f item 1: THE RAISE") + scripts/kc2_etch.gdshader (sha256 bbff4063...881e898), the
#   whirlwind drawn in Matt's reference clip ww7-gate2-cadence-ab-plk0665-1920x1080.mp4 (rendered by
#   scripts/run_ww7_gate2_clip.sh -> kc2_cpb_clip.gd; SEGMENT B = `--undulate on`, the shipped default).
#   R-C9-128 ported scripts/wwcr_whirlwind.gd instead -- the S2 clean-room mint, which has no smoke and no disc by
#   design. That was the wrong source; this file is the right one. The wwcr port stays behind ?eorfx=wwcr.
#
# ⚑ WHAT IS PORTED: ONLY WHAT DRAWS. The source file is 4,217 lines; ~3,300 of them are the player's body
#   (assembly, channel pose, IK, occlusion and sole laws) and the arena wire. None of that moves here: the Barrow
#   has its own dark knight and his own spin clip (Matt, R-C9-143: "the animation of the warlord looks good").
#   The VFX layers, their constants, comments, seeds, gradients and hashes are copied VERBATIM below; every place
#   the Barrow forces a difference carries a "C-9 EOR2 PORT n" note, and the list is here:
#
#   LAYER MAP (visual element in the clip -> source -> here)
#     light-grey cloudy haze, ~3 m disc      SmokeHaze  `_smoke`      src 3400-3462 -> `_smoke`      (GPUParticles3D, smoke_05_a)
#     its dark ground half, soft edge        SmokeDarkBed `_smoke_bed` src 3481-3536 -> `_smoke_bed`  (ArrayMesh disc)
#     red-orange arcs at the steel's reach,  THE CUTS   `_build_etch` src 2849-3011, `cut_layout_at` 3024-3081,
#       white-hot heads, sword + claw          `_cut_mesh`/`_cut_ribbon` 3210-3279, `_drive_cuts` 3606-3647,
#                                              kc2_etch.gdshader -> the same functions here + data/vfx/eor_kc2/kc2_etch.gdshader
#     thin streak sparks flying off          Sparks_0..2 `_sparks` src 3339-3397, `emitter_open` 3667-3680 -> same
#     orange ember flecks off the hammer     HammerTrail `_trail` src 3282-3336 -> `_trail`
#     the one thermal ramp all four share    `palette_*` src 415-515 -> verbatim
#     (warm OmniLight "ForgeLight")          src 2738-2746 -> NOT PORTED (PORT 6)
#
#   C-9 EOR2 PORT 1  THE CLOCK. Source: revolutions = sim tick x tick_period / player_rev_period_s, a perfectly
#                    uniform spin of a pinned body. Here: revolutions = the mace head's ACCUMULATED BEARING since the
#                    cast, / TAU -- his clip spins him (0.300 s/rev, one closed CCW turn per loop), so a cut born at
#                    `birth` revs still sits at `a0 + TAU * birth`, i.e. exactly where his steel was. That identity is
#                    the reason the source's cuts are world-fixed; it is kept, not approximated. After release the
#                    clock runs on at the clip's measured rate so the last cuts and sparks finish their lives.
#   C-9 EOR2 PORT 2  THE STATION. Source: the body is pinned (R-CPB-4); the bed, haze emitter and cuts sit at one
#                    point. He WALKS while channelling here (the GD packet: canUseWhileMoving), so those non-spinning
#                    layers ride his ground position -- translation only, never his yaw. The haze particles keep the
#                    source's world coords, so when he walks they drift behind him as smoke does. The smoke's floor
#                    (bed + haze) is the SNOW SURFACE under him (snow_field floor_y + depth_at): his origin is the
#                    ground beneath ~0.3 m of snow, and the source's floor is the surface the body visibly stands on.
#                    The cuts and sparks keep their heights from his feet, as the source measured them.
#   C-9 EOR2 PORT 3  THE SPIN FRAME. Source: the spark ring is a child of the spinning body holder. Here its yaw is
#                    set every frame from the head's bearing so the hammer sits at the SAME body-frame angle the source
#                    measured (contact band angle -0.981523709878878 rad, a2f shot-B manifest): the three emitters keep
#                    their source bearings relative to the steel (146.2 / 105.2 / 49.2 deg ahead of it).
#   C-9 EOR2 PORT 4  WEAPON TRUTH, BY THE SOURCE'S OWN RULE. The source never types a radius: the cuts and the
#                    sparks sit at the MEASURED reach of the weapon (`measure_contact_band`, frac 0.99;
#                    `measure_weapon_sweep`). Here the same two rules run on the dark knight's mace. His pose is
#                    NOT frozen (the source's was), so they run over 12 phases of his spin loop -- the source's own
#                    `phases` default, from A2b when its pose still moved -- sampled from the clip's bone tracks, and
#                    the ring is drawn at the MEAN, as the source says. No character-height scaling: the source has
#                    none, so every other length below is the source's metres.
#   C-9 EOR2 PORT 5  DAMAGE TRUTH. Source: the smoke disc reaches the wire's `circle_sweep.radius_m`, 3.000 m. The
#                    Barrow carries no EoR damage radius, so the source's number is kept: 3.000 m.
#   C-9 EOR2 PORT 6  NO LIGHT NODE. The source's ForgeLight (warm OmniLight3D, energy 1.15) is not built: a light
#                    node whites the Barrow out on the phone renderer (whirlwind_fx.gd PORT 6). Every layer of this
#                    effect is unshaded, so the light only warmed his body and the floor under the bed.
#   C-9 EOR2 PORT 7  DRAW ORDER. Everything draws after the Barrow's paint post pass (PaintStack.AFTER_POST_PRIORITY)
#                    or the paint covers it. The source's one ordering rule is kept inside that: the bed draws FIRST
#                    (source render_priority -8 -> AFTER_POST), every other layer after it (source 0 -> AFTER_POST + 1).
#   C-9 EOR2 PORT 8  NO GLOW. The source's HOT is an HDR claim -- a 9.0 core bloomed by the arena's glow pass
#                    (kc2_arena.gd, threshold 1.0). The Barrow's environment has glow OFF and a linear tonemap
#                    (PaintStack.barrow_environment; not this lane's), and the phone renderer has no HDR buffer. The
#                    shader and every energy are unchanged; the core clips to white and does not bloom. Not
#                    compensated -- named, and shown side by side in the R-C9-143 stills.
#   C-9 EOR2 PORT 9  THE LIFECYCLE. Source: the aura is gated by one wire bit that is on for the whole clip, and it
#                    pops. Here a cast BEGINS (instant, as the source: the haze restarts with its own 5.5 s preprocess,
#                    "the bed exists before frame one") and RELEASES: births and emission stop, the cuts finish their
#                    0.45 rev on PORT 1's clock, and the haze and the bed fade out over FADE_OUT_S. 0.80 s is AUTHORED
#                    -- the old port's spin-down, so the channel stays busy exactly as long as it did.
#   C-9 EOR2 PORT 10 THE SPARKS' LAUNCH SPEED. Source: v = TAU * r / player_rev_period_s -- the steel's own speed.
#                    His steel turns at the clip's 0.300 s/rev, so that is the period used; 0.36 stays in the
#                    declarations, which describe the source.
#   C-9 EOR2 PORT 11 THE EMBERS' HEAD POINT. Source: 0.93 up the weapon's AABB along its haft, in grip space. The
#                    mace here is bone-driven (weapon_r), so: 0.93 along the mace's own pommel->head extent on the
#                    grip->head axis, in the bone's space -- the same fraction of the same steel.
#   C-9 EOR2 PORT 12 WARM-UP. Every layer drawn once under the veil (warm()), or the first cast compiles its
#                    shaders and the particle process materials mid-spin (whirlwind_fx.gd PORT 12).
#   C-9 EOR2 PORT 13 THE BEARING is the mace head's (the vertex farthest from the grip), not the per-frame centroid of
#                    the contact band: re-sweeping every mace vertex every frame is a cost the phone should not pay.
#                    The two are measured against each other once (report.bearing_head_vs_band_deg).
#   C-9 EOR2 PORT 14 THE MACE, THROUGH ITS SKIN. His mace is a skinned mesh (every vertex weight 1.0 to weapon_r) in
#                    metres under a skeleton in centimetres. Its vertices go to weapon_r's space by the skin's own bind
#                    pose. (The R-C9-128 port's `_weapon_head_local` used the bone's rest instead and folded the mace to
#                    a point -- the skeleton's origin seen from his hand; that is why this file does not take it.)
#   C-9 EOR2 PORT 17 VENUE RETINT: PERCEIVED CONTRAST HELD, NOT ABSOLUTE LUMA (conductor ruling on R-C9-143, the
#                    same kind of call as whirlwind_fx.gd PORT 11). Matt asked for "light smoke particles" (R-C9-128),
#                    and the source haze reads light grey because it sits over a 0.42-luma tile; ported unchanged onto
#                    0.96 snow it measured 0.44 -- soot. So on snow the haze is translucent kicked-up snow powder, a cool
#                    white with a faint blue-grey in its shadowed core, and the dark bed is a soft trodden-snow shadow
#                    in the Barrow's OWN shadow colour (sampled off his film: sRGB 0.647/0.700/0.832 under the standing
#                    stones). Kept from the source: every alpha stop of the haze (the cloud-is-variance law), the bed's
#                    soft-edge profile and radius. Changed: the haze's four colour stops, the bed's colour, and the bed's
#                    peak alpha (0.86 -> SNOW_BED_ALPHA, so it reads as a shadow and not a hole). The arc, heads, sparks
#                    and embers are untouched; they never read the smoke's colours.
#   C-9 EOR2 PORT 18 THE BANDS. The source haze is 2.3 m camera-facing quads (x0.9..2.6) on the floor: each one cuts
#                    the ground along a screen-horizontal line, which the source's dark tile hid and white snow does
#                    not. Neither ruled option removes it without a bigger change: a lift clear of the surface is
#                    ~1.8 m at this camera's 53 deg pitch (half a 6 m quad x cos 53), which floats the "low pool" above
#                    his waist; no-depth-test draws the haze over his body and mace (the source keeps "the hammer and
#                    the head clear"). The smaller change is SOFT PARTICLES on the haze material -- proximity fade over
#                    HAZE_SOFT_M -- which dissolves exactly the intersection and nothing else. Written out in
#                    kc2_haze_ember.gdshader (PORT 20), which draws the haze on BOTH variants: the StandardMaterial's
#                    own proximity fade at 0.80 m erased the haze on snow (measured 0.858 inside vs 0.856 outside).
#   C-9 EOR2 PORT 19 THE CUT POOL AS A MULTIMESH (conductor ruling: the R-C9-89 draw budget). The source draws each
#                    live stroke as its own node, 2 surfaces each (~7.65 live x 2 ~ 15 draws). Here ONE MultiMesh holds
#                    every stroke: its mesh is all 12 variants merged, each vertex tagged with its variant (COLOR.b);
#                    each instance carries its yaw and height (transform) and (variant, stroke_age) (custom data);
#                    data/vfx/eor_kc2/kc2_etch_mm.gdshader drops every vertex not of the instance's variant. 2 draws.
#                    Same layout function, same meshes, same fragment; additive blending makes the sheath/core order
#                    immaterial. ⚑ OPEN: it matches the pool exactly in isolation but draws no arc in the Barrow,
#                    so the DEFAULT is still the source's node pool; ?eorcuts=mm selects the MultiMesh.
#   C-9 EOR2 PORT 20 THE RED EYE (R-C9-146, Matt: "the cloud's transparent edges running intermittently red hot").
#                    `eortint=original` draws the PORT 17 snow-powder haze exactly. `eortint=red` (his default) draws
#                    the SAME haze through data/vfx/eor_kc2/kc2_haze_ember.gdshader: the low-alpha rim band of each
#                    puff runs red-hot (the source ramp's orange knee -> red crawl), on and off per particle with a
#                    seeded phase that also travels around the disc, so it crawls instead of pulsing; the core stays
#                    light. Same quad, same draw (one mix; the ember COVERS inside its rim mask -- red
#                    ADDED over white snow clipped to yellow-white and read as lightning in the first render). The clock is
#                    PORT 1's revolutions, not TIME. The sparks and the ember flecks shift toward red on this variant
#                    (their ramp sampled from EMBER_RED_SHIFT along the source's own ramp). THE ARC (the cuts) IS THE
#                    SOURCE'S WHITE-HOT -> ORANGE -> RED ON BOTH VARIANTS. (Supersedes the bind_to note that both
#                    tints draw the same: that was true until R-C9-146.)
#   ⚑ C-9 EOR2 PORT 21 / R-C9-152 (Matt, on the live Barrow): "The whirlwind is good but remove all of the red VFX
#                    from it.. instead just color the smoke a bit red while leaving it translucent and add some spark
#                    particles to it." SUPERSEDES PORT 19's role, PORT 20's rims and red shift, and the arc:
#                    - THE ARC CUTS ARE NOT BUILT (ARC_CUTS = false; the code stays, unbuilt, as the record).
#                    - THE RIM EMBER IS OFF (gain 0 on every variant); the haze shader stays for its soft fade.
#                    - THE HAZE takes a SLIGHT dusty-red tint on its colour stops only (alphas, overlap, soft fade
#                      unchanged): SMOKE_RED_STRENGTHS, ?eorsmoke=1|2|3 (default 2). eortint=red (his default) =
#                      the tinted haze; eortint=original = the untinted PORT 17 haze.
#                    - SPARKS: the source's three emitters and ember flecks on the SOURCE ramp (white-hot -> orange,
#                      no red shift), plus a FOURTH emitter riding the mace head, so sparks are thrown off its path.
#                      All sparks and embers MIX-blended, not added: warm-white ADDED over 0.96 snow is invisible
#                      (the same finding as the rims), mixed it reads as a spark. PORT 21b: the four spark emitters draw
#                      a generated soft streak instead of spark_04_a (a faint lightning tendril, mostly empty in a streak).
#                    - THE BED stays the soft trodden-snow shadow.
# ============================================================================

const PAL_SRC := "reincarnated-godot scripts/kc2_player_channel.gd @ 34dcd41"
const SPARK_TEX_RES := preload("res://data/vfx/eor_kc2/spark_04_a.png")
const HAZE_EMBER_SHADER_RES := preload("res://data/vfx/eor_kc2/kc2_haze_ember.gdshader")   # PORT 20
const SMOKE_TEX_RES := preload("res://data/vfx/eor_kc2/smoke_05_a.png")
const ETCH_SHADER_RES := preload("res://data/vfx/eor_kc2/kc2_etch.gdshader")
const ETCH_MM_SHADER_RES := preload("res://data/vfx/eor_kc2/kc2_etch_mm.gdshader")   # PORT 19

# ---- the source's measured anchors (a2f shot-B manifest, the clip's own build) ----------------------------------
const SRC_HAMMER_BEARING_RAD := -0.981523709878878   # contact_band.angle_rad: where the steel sits in the body frame
const SRC_CONTACT_RADIUS_M := 2.20034735019359       # for the report only: the source hammer's reach
const SRC_WIRE_RADIUS_M := 3.000
# C-9 EOR2 PORT 16: the source hammer's contact band half-extent (a2f manifest, 16 of 1,958 vertices at reach, a flat
# head 0.30 m tall). His mace's 0.99 band is a SPIKE TIP -- 0.0075 m half-extent, which would draw every cut as a
# 1.6 mm hairline -- so the rule's radius and height are his, and the stroke's THICKNESS is the source's number:
# the stroke Matt watched (core 0.0329 m, sheath 0.0954 m half-width).
const SRC_CONTACT_HALF_EXTENT_M := 0.149611979722977                     # tracks.circle_sweep.radius_m  (PORT 5)
const SRC_DRAWN_HEIGHT_M := 1.7097
# C-9 EOR2 PORT 15: the source's ember emitter hangs off its Weapon node, whose GLOBAL scale is 1.910876
# (WEAPON_SCALE 1.95 x body 0.979937, measured by building the source body headless). A world-space GPUParticles3D
# takes its emitter's scale into the emission sphere, the launch speed and the quad, so the source's embers were
# drawn 1.91x their constants. The mount here carries that one measured number, and nothing of his skeleton's
# centimetre scale (0.0115), which would shrink them to dust.
const SRC_EMBER_SCALE := 1.910876

# ---- C-9 EOR2 PORT 9 / 12 ----------------------------------------------------------------------------------------
const FADE_OUT_S := 0.80
const FADE_IN_S := 0.10                               # = slot_knight.gd EOR_FADE_S: the bed arrives as his spin does
const MEASURE_PHASES := 12                            # PORT 4: the source's `phases` default
# ---- C-9 EOR2 PORT 21 (R-C9-152) ----------------------------------------------------------------------------------
const ARC_CUTS := false                              # Matt: "remove all of the red VFX" -- the etch is not built
# the haze's slight red: each colour stop lerped this far toward SMOKE_RED (linear) -- ?eorsmoke=1|2|3
const SMOKE_RED := Color(0.84, 0.46, 0.32)           # a dusty brick red, not fire, not blood (0.78/0.36/0.30 read mauve over the blue bed)
const SMOKE_RED_STRENGTHS := [0.18, 0.30, 0.45]
const SMOKE_RED_DEFAULT := 1                         # index: 0.30
# C-9 (Matt via the conductor, 2026-10-09): the HAZE more transparent. One multiplier on the haze's alpha only (the
# StandardMaterial's albedo alpha and the ember shader's "fade"); the dark bed, the cuts, the sparks and the embers are
# untouched. ?eorsmokea=0.4|0.6|0.8|1.0 (desktop: -- --eorsmokea 0.8); 1.0 = the look before this change, exactly.
const SMOKE_OPACITY_CHOICES := {"0.4": 0.4, "0.6": 0.6, "0.8": 0.8, "1.0": 1.0, "1": 1.0}
const SMOKE_OPACITY_DEFAULT := 0.6
var _smoke_opacity_k := -1.0
# the fourth spark emitter, on the mace head: the source's _sparks() with these
const HEAD_SPARK_AMOUNT := 32
const HEAD_SPARK_LIFETIME_S := 0.35
const HEAD_SPARK_QUAD := Vector2(0.07, 0.50)         # the source's 0.045 x 0.30 streak barely shows at the Barrow camera

# ---- C-9 EOR2 PORT 17: the snow retint (AUTHORED against the Barrow's measured snow and shadow) --------------------
# Haze stops, LINEAR (vertex colours are linear; the source's 0.205 shows as sRGB ~0.49): the source's alpha stops,
# cool white at the light end, blue-grey in the shadowed core.
const SNOW_HAZE_C0 := Color(0.84, 0.87, 0.92)        # birth (source 0.215, 0.205, 0.235; alpha 0 kept)
const SNOW_HAZE_C16 := Color(0.80, 0.84, 0.90)       # 0.16 of life (source 0.205, 0.195, 0.225; alpha 0.30 kept)
const SNOW_HAZE_C70 := Color(0.62, 0.67, 0.78)       # 0.70, the shadowed core (source 0.105, 0.100, 0.128; 0.22 kept)
const SNOW_HAZE_C1 := Color(0.58, 0.63, 0.75)        # death (source 0.070, 0.066, 0.085; alpha 0 kept)
# The bed: the Barrow's own snow-shadow colour, sRGB (0.647, 0.700, 0.832) sampled off his film -> linear.
const SNOW_BED_COLOR := Color(0.376, 0.448, 0.658)
const SNOW_BED_ALPHA := 0.45                         # source 0.86 over tile; a shadow on snow, not a hole
# ---- C-9 EOR2 PORT 18 ----------------------------------------------------------------------------------------------
const HAZE_SOFT_M := 0.35                            # proximity fade: where a haze quad meets the snow, it dissolves
                                                     # (0.80 measured erasing a ground-hugging haze at this pitch)
# ---- C-9 EOR2 PORT 19 ----------------------------------------------------------------------------------------------
const CUT_VARIANT_CODES := 16.0                      # COLOR.b = (id + 0.5) / 16; 12 ids used
# ---- C-9 EOR2 PORT 20 (R-C9-146): eortint=red -- AUTHORED, every one named --------------------------------------
const EMBER_RIM_LO := 0.02        # smoke_05_a alpha where a puff's rim band starts (its max alpha is 0.84)
const EMBER_RIM_HI := 0.35        # ...and where the puff is dense enough to stay light
const EMBER_DUTY := 0.07          # fraction of each cycle a particle's rim runs hot
const EMBER_RATE := 0.5           # cycles per revolution (~1.7 Hz at his 0.300 s/rev)
const EMBER_WAVES := 2.0          # lobes of the crawl around the disc
const EMBER_JITTER := 0.35        # per-particle seeded phase spread
const EMBER_GAIN := 0.75   # the ember covers this much of what is under it, at full rim (0.55 read pink, 0.90 worms)
const EMBER_RIM_R_IN := 0.58     # the puff's outer radial band (0 = its centre, 1 = its quad edge)
const EMBER_RIM_R_OUT := 0.92
const EMBER_RED_SHIFT := 0.30     # sparks + embers: their ramp starts this far along the source ramp (past the knee)

# ⚑ THE SPIN RATE — R-CPB-3. Kept for the declarations (they describe the source); the clip's own period drives the
#   clock and the sparks here (PORT 1, PORT 10).
const player_rev_period_s := 0.36

# ============================================================================
# FROM HERE TO `_hash2`, THE SOURCE'S VFX CONSTANTS AND FUNCTIONS, VERBATIM (comments and all) unless a PORT note says.
# ============================================================================

# --- the aura (R-CPB-2) ------------------------------------------------------
# Three emitters. The hammer LEADS at offset 0 (the sparks come off the steel);
# two unseen strikers TRAIL it. The offsets are deliberately NOT evenly spaced —
# 120/120/120 would read as a rotating tripod, which is a shape, and a shape is
# the thing R-BR-17's discriminator keeps out of a core beat.
# ⚑ LAYER ONE — THE ETCH (R-CPB-7). Matt's ruling, five ratified properties:
#   CONTINUOUS · DENSE · PERSISTENT · SHARP-EDGED · HOT. It is the DOMINANT
#   element of the aura from this cell forward; the particle families below are
#   accents around it.
const ETCH_CONTACT_FRAC := 0.99   # of max radius: which vertices ARE "the steel at reach"
const ETCH_CORE_FRAC := 0.22      # core half-width, as a fraction of the contact band's half-extent
const ETCH_SHEATH_MULT := 2.9     # the bloom sheath, as a multiple of the core
const ETCH_PLANES := 3            # crossed ribbons through the stroke's axis
const ETCH_TAIL_TAPER := 0.42     # the stroke thins as it cools
const ETCH_CORE_ENERGY := 9.0     # HDR at the steel
const ETCH_TAIL_ENERGY := 0.30    # HDR one full persistence back
const ETCH_SHEATH_ENERGY_FRAC := 0.22   # the sheath is the halo, never the line

# THE CUT PATTERN — R-CPB-12. Five clauses, all Matt-ruled, all constants.
const CUT_PERSIST_REVS := 0.45    # clause 1, inside the ruled 0.40-0.50 band
const CUT_SEED := 20260813        # clause 5: THE declared seed. One number.
const CUT_PER_REV := 17           # cut births per revolution — DERIVED (R-CPB-15; the source's table, src 148-191)
const CUT_DENSITY_TARGET := 11.0  # cuts/rev — the RATIFIED density (R-CPB-15)
const CUT_DENSITY_TOL := 0.5      # the band R-CPB-15 states, in cuts/rev
# ⚑ THE JITTER IS BIN-BOUNDED ON PURPOSE. Each slot's birth stays inside its own
#   1/CUT_PER_REV bin, so births are strictly increasing in time and can never
#   reorder — which is what lets the pool assignment be `g mod POOL` with no
#   bookkeeping, and what makes the layout comparable across builds.
const CUT_JITTER := 0.55          # +/- of a bin, seeded per stroke
const CUT_ARC_REVS_LO := 0.055    # a cut's own drawn length, low  (19.8 deg)
const CUT_ARC_REVS_HI := 0.140    # ...and high                    (50.4 deg)
const CUT_VERT_BAND_M := 0.36     # clause 3: the vertical band, centred on contact height
const CUT_VERT_LEVELS := 5        # above / high / at / low / below
const CUT_VARIANTS := 6           # pre-built stroke meshes PER CLASS
const CUT_POOL := 24              # stroke nodes. Asserted never to overflow.
const CUT_SEG_PER_REV := 288      # segment density, if a stroke spanned a whole rev
# CLAW family (clause 2) — "as if a hand with different sized fingers laser-
# scraped the metal".
const CLAW_LINES_LO := 3
const CLAW_LINES_HI := 4
const CLAW_GAP_M := 0.040         # vertical stacking between the fingers
const CLAW_WIDTH_LO := 0.26       # per-line half-width, as a fraction of the sword core
const CLAW_WIDTH_HI := 0.62
const CLAW_STAGGER_REVS := 0.030  # per-line leading/trailing edge offset, max

# ⚑ THE UNDULATION — R-CPB-14. The shipped default (SEGMENT B of Matt's clip) is ON, and only ON is ported: the
#   stationary A2d cadence was segment A, the comparison's reference half, not the effect.
const CUT_UNDULATE_DEFAULT := true
const CUT_EPOCH_LEN_LO := 5
const CUT_EPOCH_LEN_HI := 13
# The silence after a sequence ends, in REVOLUTIONS (NOTE-38: revs, never
# seconds — retuning the spin must not retune the cadence).
#       silence <= CUT_EPOCH_GAP_HI_REVS + (1 + CUT_JITTER) / CUT_PER_REV
#       dark    <= max(silence - CUT_PERSIST_REVS, 0) revs
const CUT_EPOCH_GAP_LO_REVS := 0.10
const CUT_EPOCH_GAP_HI_REVS := 0.40
const CUT_EPOCH_WALK_MAX := 20000

# ⚑ THE PARTICLE SEEDS — the second clock, found by the FG-10 gate. One declared base, one offset per emitter.
const FX_SEED := 20260813
const FX_SEED_SMOKE := 11
const FX_SEED_TRAIL := 23
const FX_SEED_SPARK := 37        # + the emitter index


# Pin a particle system to a declared seed. Called on EVERY GPUParticles3D this
# file builds; there is no second place they are constructed.
static func _pin_seed(p: GPUParticles3D, offset: int) -> void:
	p.use_fixed_seed = true
	p.seed = FX_SEED + offset

# ⚑ THE THERMAL RAMP — R-CPB-13's IMPLEMENTATION LAW, AND IT IS ONE BLOCK.
#   ONE RAMP AND FOUR CONSUMERS (sword, claw, bursts, embers); `PAL_TAIL` alone reverts the red extension
#   everywhere. SMOKE IS DELIBERATELY NOT A CONSUMER. R-CPB-13: "Smoke stays OUT (darkness, not heat)."
const PAL_HEAD := Color(1.00, 0.97, 0.90)   # white-hot, at the steel
const PAL_MID := Color(1.00, 0.42, 0.06)    # orange, at the knee
const PAL_TAIL := Color(0.98, 0.07, 0.02)   # RED, in the crawl  <-- THE REVERT POINT
const PAL_KNEE_AT := 0.56         # where the knee sits on the DECAYED age axis
const PAL_GAMMA := 0.55           # BELOW 1: fast off the steel, then a long crawl
const CUT_MID_ENERGY := 1.70      # HDR at the orange knee
const CUT_TAIL_FADE := 0.28       # the last fraction, smoothstepped to nothing
const PAL_SAMPLES := 32


#   a = life^PAL_GAMMA                        (gamma < 1 => fast, then a crawl)
#   a < knee : head -> mid                    (white-hot into orange)
#   a >= knee: mid  -> tail                   (orange into RED, in the crawl)
static func palette_rgb(life: float) -> Color:
	var a: float = pow(clampf(life, 0.0, 1.0), PAL_GAMMA)
	if a < PAL_KNEE_AT:
		return PAL_HEAD.lerp(PAL_MID, a / maxf(PAL_KNEE_AT, 1e-4))
	return PAL_MID.lerp(PAL_TAIL, (a - PAL_KNEE_AT) / maxf(1.0 - PAL_KNEE_AT, 1e-4))


static func palette_knee_life() -> float:
	return pow(PAL_KNEE_AT, 1.0 / PAL_GAMMA)


static func palette_gradient(alpha_head: float, alpha_tail: float, shift: float = 0.0) -> Gradient:
	# C-9 EOR2 PORT 20: `shift` > 0 (eortint=red only) samples the ramp from `shift` onward -- the same ramp, entered
	# hotter-red; 0 is the source exactly
	var ts: Array[float] = []
	for i in PAL_SAMPLES:
		# even on the DECAYED axis, which is dense exactly where the ramp is steep
		ts.append(pow(float(i) / float(PAL_SAMPLES - 1), 1.0 / PAL_GAMMA))
	ts.append(palette_knee_life())          # the corner gets its own stop
	ts.sort()
	var offs := PackedFloat32Array()
	var cols := PackedColorArray()
	var last := -1.0
	for t in ts:
		if t - last < 1e-7:                 # a duplicate stop is not a stop
			continue
		last = t
		var c := palette_rgb(shift + (1.0 - shift) * t)
		c.a = lerpf(alpha_head, alpha_tail, t)
		offs.append(t)
		cols.append(c)
	# assigned wholesale, never add_point()ed onto the two default stops a fresh
	# Gradient is born with — those would survive at 0 and 1 and paint the head
	# black
	var g := Gradient.new()
	g.offsets = offs
	g.colors = cols
	return g

# LAYER ONE-b constants (the EMBER GARNISH). These touch the garnish and NOTHING else.
const TRAIL_HEAD_FRAC := 0.93     # up the weapon: where the head is (PORT 11)
const TRAIL_AMOUNT := 110         # was 260, when this layer had to carry the streak alone
const TRAIL_LIFETIME_S := 0.20    # ~0.56 of a revolution: a streak, not a ring
const TRAIL_SPREAD_M := 0.09
const TRAIL_QUAD_M := 0.11        # was 0.16 — garnish does not compete with the line

# LAYER TWO constants (discrete contact bursts).
const SPARK_EMITTER_OFFSETS_DEG := [0.0, -41.0, -97.0]
const SPARK_LIFETIME_S := 0.42
const SPARK_EMITTER_Y_M := 0.85   # the source's `Vector3(radius, 0.85, 0.0)`, named here only so the report can cite it
# ⚑ THE SMOKE BED (R-CPB-2 + R-CPB-5c). Matt asked for "cloudy/smoky DARKNESS" as the contrast bed under the sparks.
# ⚑ AND ITS EDGE IS SOFT ON PURPOSE, WHICH IS A LAW AND NOT A LOOK (R-CPB-5b). The falloff STRADDLES the radius —
#   full density inside, gone outside, exactly HALF at it — and there is no locatable line anywhere in it.
# ⚑ GL-15: THE BED AND THE HAZE ARE ONE READ, NOT TWO. The dark ground bed carries the extent and the soft edge; the
#   particle haze carries the CLOUD.
const SMOKE_INNER_FRAC := 0.0         # the bed is a DISC now, not a ring: "filling the disc"
const SMOKE_TOP_M := 1.25             # below the torso: the hammer and the head stay clear
const SMOKE_AMOUNT := 170             # see _smoke(): more than this SATURATES into a plate
const SMOKE_LIFETIME_S := 5.5
const SMOKE_EDGE_SOFT_FRAC := 0.22    # the falloff band, +/- of the wire radius
const SMOKE_BED_ALPHA := 0.86
const SMOKE_BED_COLOR := Color(0.031, 0.029, 0.038)
const SMOKE_BED_RINGS := 56
const SMOKE_BED_SEGMENTS := 96
const SMOKE_BED_LIFT_M := 0.02        # off the floor, so the bed is not z-fighting it

# ============================================================================
# state
# ============================================================================
enum S { IDLE, SUSTAIN, FALLING }
var _state: int = S.IDLE
var tint := "red"
var report: Dictionary = {}
var fx: Node3D                                 # the aura assembly root (source name kept)
var smoke_root: Node3D                         # does NOT spin: a bed is not a rotor
var spark_root: Node3D                         # turns with his steel (PORT 3)
var etch_root: Node3D                          # does NOT spin — R-CPB-12
var _emitters: Array[GPUParticles3D] = []
var _trail_node: GPUParticles3D
var _head_spark_root: Node3D                  # PORT 21: the fourth emitter's frame, on the mace head
var _head_sparks: GPUParticles3D
var _trail_mount: Node3D
var _ember_local := Vector3.ZERO
var _haze: GPUParticles3D
var _haze_mat: StandardMaterial3D
var _haze_ember: ShaderMaterial                # PORT 20: eortint=red draws the haze with this instead
var _bed: MeshInstance3D
var _bed_mat: StandardMaterial3D
var _cut_lib: Array = []
var _cut_nodes: Array = []
var _cut_mats: Array = []
var _cut_ready := false
var _cut_mm := false                          # PORT 19 MultiMesh: ?eorcuts=mm (OPEN); default = the source's node pool
var _mm: MultiMesh
var _mmi: MultiMeshInstance3D
var _mm_mats: Array = []                      # [sheath, core] ShaderMaterial on the merged mesh's two surfaces
var _cut_r := 0.0
var _cut_y := 0.0
var _cut_a0 := 0.0
var _spark_r := 0.0
var _wire_r := SRC_WIRE_RADIUS_M
var _rig: Node3D
var _skel: Skeleton3D
var _k: Node = null
var _wb := -1
var _head_local := Vector3.ZERO               # the mace head in weapon_r's space (PORT 14: through the skin)
var _mace_cache := PackedVector3Array()
var _rev_period := 0.30                       # the clip's measured loop length, s/rev (PORT 1, PORT 10)
var _revs := 0.0                              # PORT 1: the accumulated head bearing since the cast, in revolutions
var _end_revs := INF                          # no birth at or after this (PORT 9)
var _prev_b := 0.0
var _fade := 0.0                              # 0..1, the haze and the bed (PORT 9)
var _fall_t := 0.0
var _vfx := true                              # set_vfx_visible: the perf CONTROL hides every layer
var _warming := false
# ---- the 2D arena overlay atlas (tools/render_eor_overlay.gd): the same effect, driven from the eor3 cells' sockets
var synthetic := false
var syn_station := Vector3.ZERO
var syn_head := Vector3.ZERO                  # the mace head (main_tip), world
var syn_ember := Vector3.ZERO                 # the ember point, world
var syn_axis := Vector3.UP                    # grip -> head, world
var _snow: Node = null                        # PORT 2: the snow field, whose surface is the floor he visibly stands on


# ============================================================================
# binding
# ============================================================================
func bind_to(rig: Node3D, skel: Skeleton3D, knight: Node, head_local: Vector3, tint_name: String, snow: Node = null) -> void:
	_snow = snow
	_rig = rig
	_skel = skel
	_k = knight
	report["channel_head_local_r_c9_128"] = str(head_local)   # whirlwind_channel._weapon_head_local: NOT used (PORT 14)
	# ⚑ THE TINT (R-C9-128's ?eortint). The source arc is ALREADY red-orange: white-hot -> orange -> RED, R-CPB-13's
	#   ratified red extension, and it is what Matt's clip shows. So both "red" (the default) and "original" draw the
	#   source's ramp, unchanged -- there is nothing to tint toward that the source does not already carry, and
	#   inventing a second ramp would be authoring, not porting. The value is recorded so the page reports it.
	#   ⚑ SUPERSEDED BY R-C9-146 (PORT 20): "red" now runs the haze's rims red-hot and shifts the sparks and embers
	#   red; "original" is the light haze. The ARC is the source ramp on both.
	tint = tint_name
	_wb = skel.find_bone("weapon_r")
	_head_local = _farthest_from_grip(_mace_points())
	report["head_local"] = str(_head_local)
	var loop := _loop_animation()
	if loop != null:
		_rev_period = loop.length
	var band := measure_band_over_loop()
	report["band"] = band
	if bool(band.get("measured", false)):
		_spark_r = float(band["radius_m"])
	_build_aura(band)
	set_physics_process(false)
	process_priority = 10                       # after his AnimationTree has posed him this frame


## THE ARENA OVERLAY (C-9 R-C9-146 follow-on, kc2_play): the same effect with no knight. The render tool supplies the
## steel (head, ember point, haft axis) per frame from the eor3 cells' own sockets, and the weapon-truth numbers the
## sockets give (radius = mean |main_tip.xy| over the loop, height = mean main_tip.z). Under (bed, haze) and over
## (cuts, sparks, embers) go to separate render layers; the haze soft-fades against a flat ground (no floor drawn).
func bind_synthetic(radius_m: float, height_m: float, rev_period_s: float, tint_name: String,
		under_layer: int, over_layer: int) -> void:
	synthetic = true
	tint = tint_name
	_rev_period = rev_period_s
	_spark_r = radius_m
	var band := {"measured": true, "radius_m": radius_m, "height_m": height_m, "half_extent_m": SRC_CONTACT_HALF_EXTENT_M,
		"basis": "synthetic: the eor3 cells' main_tip sockets"}
	report["band"] = band
	_build_aura(band)
	if _haze_ember != null:
		_haze_ember.set_shader_parameter("ground_mode", 1.0)
		_haze_ember.set_shader_parameter("ground_y", 0.0)
	for n in smoke_root.find_children("*", "VisualInstance3D", true, false):
		(n as VisualInstance3D).layers = under_layer
	for root in [spark_root, etch_root, _trail_mount, _head_spark_root]:
		if root == null:
			continue
		for n in (root as Node).find_children("*", "VisualInstance3D", true, false):
			(n as VisualInstance3D).layers = over_layer
	process_priority = 10


func _loop_animation() -> Animation:
	var anim: AnimationPlayer = _k.get("_anim") if _k != null else null
	if anim == null:
		return null
	var nm := "eor_spin_loop" if anim.has_animation("eor_spin_loop") else "eor_spin"
	return anim.get_animation(nm) if anim.has_animation(nm) else null


# ============================================================================
# C-9 EOR2 PORT 4: the source's two weapon-truth rules, run on his mace over his spin loop.
#
# `measure_weapon_sweep` (src 2427) -> radius = max horizontal distance from the spin axis to any weapon vertex,
#   at each phase; the ring at the MEAN.
# `measure_contact_band` (src 2539) -> of the vertices within ETCH_CONTACT_FRAC of that max: the mean height and the
#   half-extent (the stroke's thickness comes from it). Averaged over the phases the same way.
# The bone poses come off the loop clip's own tracks (rest where a bone has none), composed up the parent chain --
# the source's `_bone_global_from_locals`, which needs no processed frame either.
# ============================================================================
func measure_band_over_loop() -> Dictionary:
	var out := {"measured": false, "basis": ""}
	if _skel == null or _wb < 0:
		out["basis"] = "NO weapon_r bone -- there is no steel to measure"
		return out
	var pts := _mace_points()
	out["verts_total"] = pts.size()
	if pts.is_empty():
		out["basis"] = "no mace vertices in his gear"
		return out
	var loop := _loop_animation()
	var anim: AnimationPlayer = _k.get("_anim")
	var tr := {}                                  # bone index -> [pos track, rot track, scale track]
	if loop != null:
		var root_node: Node = anim.get_node_or_null(anim.root_node)
		for ti in loop.get_track_count():
			var p := loop.track_get_path(ti)
			if p.get_subname_count() < 1 or root_node == null:
				continue
			if root_node.get_node_or_null(NodePath(String(p.get_concatenated_names()))) != _skel:
				continue
			var bi := _skel.find_bone(String(p.get_concatenated_subnames()))
			if bi < 0:
				continue
			if not tr.has(bi):
				tr[bi] = [-1, -1, -1]
			match loop.track_get_type(ti):
				Animation.TYPE_POSITION_3D: tr[bi][0] = ti
				Animation.TYPE_ROTATION_3D: tr[bi][1] = ti
				Animation.TYPE_SCALE_3D: tr[bi][2] = ti
	var sk_basis := _skel.global_transform.basis
	var sk_off := _skel.global_transform.origin - _rig.global_transform.origin
	var radii := []
	var heights := []
	var halves := []
	var head_vs_band := []
	for ph in MEASURE_PHASES:
		var t := (loop.length * float(ph) / float(MEASURE_PHASES)) if loop != null else 0.0
		var wx := _bone_pose_at(loop, tr, _wb, t)
		var to_rig := Transform3D(sk_basis, sk_off) * wx
		var r_max := 0.0
		var qs: Array[Vector3] = []
		for p in pts:
			var q: Vector3 = to_rig * p
			qs.append(q)
			r_max = maxf(r_max, Vector2(q.x, q.z).length())
		var n := 0
		var sy := 0.0
		var sx := 0.0
		var sz := 0.0
		var y_lo := 1e9
		var y_hi := -1e9
		for q in qs:
			if Vector2(q.x, q.z).length() < r_max * ETCH_CONTACT_FRAC:
				continue
			n += 1
			sy += q.y
			sx += q.x
			sz += q.z
			y_lo = minf(y_lo, q.y)
			y_hi = maxf(y_hi, q.y)
		if n < 3:
			continue
		radii.append(r_max)
		heights.append(sy / float(n))
		halves.append(0.5 * (y_hi - y_lo))
		var hd: Vector3 = to_rig * _head_local
		head_vs_band.append(rad_to_deg(wrapf(atan2(hd.x, hd.z) - atan2(sx / n, sz / n), -PI, PI)))
	if radii.is_empty():
		out["basis"] = "fewer than 3 vertices at reach in every phase -- the cuts REFUSE rather than guess a radius"
		return out
	var mean := func(a: Array) -> float:
		var s := 0.0
		for v in a:
			s += float(v)
		return s / float(a.size())
	out["measured"] = true
	out["phases"] = radii.size()
	out["radius_m"] = mean.call(radii)
	out["radius_min_m"] = radii.min()
	out["radius_max_m"] = radii.max()
	out["height_m"] = mean.call(heights)
	out["half_extent_m"] = mean.call(halves)
	out["bearing_head_vs_band_deg"] = mean.call(head_vs_band)
	out["loop_s"] = loop.length if loop != null else 0.0
	out["basis"] = ("PORT 4: the source's measure_contact_band (frac %.2f) and measure_weapon_sweep, on the dark "
		+ "knight's mace (%d vertices, weapon_r space), over %d phases of %s (%.3f s/rev), bone poses composed from the "
		+ "clip's own tracks. Ring at the MEAN reach.") % [ETCH_CONTACT_FRAC, pts.size(), radii.size(),
		"his spin loop" if loop != null else "his REST pose (no loop clip!)", _rev_period]
	return out


func _bone_pose_at(loop: Animation, tr: Dictionary, bone: int, t: float) -> Transform3D:
	var xf := Transform3D()
	var i := bone
	while i >= 0:
		var rest := _skel.get_bone_rest(i)
		var pos := rest.origin
		var rot := rest.basis.get_rotation_quaternion()
		var scl := rest.basis.get_scale()
		if loop != null and tr.has(i):
			var ix: Array = tr[i]
			if int(ix[0]) >= 0:
				pos = loop.position_track_interpolate(int(ix[0]), t)
			if int(ix[1]) >= 0:
				rot = loop.rotation_track_interpolate(int(ix[1]), t)
			if int(ix[2]) >= 0:
				scl = loop.scale_track_interpolate(int(ix[2]), t)
		xf = Transform3D(Basis(rot).scaled(scl), pos) * xf
		i = _skel.get_bone_parent(i)
	return xf


func _mace_points() -> PackedVector3Array:
	"""Every vertex of the mace he holds in weapon_r, in that bone's own space. C-9 EOR2 PORT 14: through the SKIN's
	bind pose for weapon_r (`skin.get_bind_pose(i) * v`), and only the vertices the skin gives to weapon_r. The mace
	is a skinned mesh in METRES under a skeleton in CENTIMETRES (scale 0.0115); `rest.affine_inverse() * v` -- the
	R-C9-128 port's way -- reads metres as centimetres and folds the whole mace onto one point."""
	if not _mace_cache.is_empty():
		return _mace_cache
	var out := PackedVector3Array()
	var pieces: Dictionary = (_k.get("gear") as Dictionary).get("_pieces", {})
	for nm in pieces:
		var s := String(nm)
		if not (s.contains("mace") or s.contains("maul") or s.contains("hammer") or s.contains("axe") or s.contains("sword")):
			continue
		if not (pieces[nm] is Array):
			continue
		for mi in (pieces[nm] as Array):
			var m := mi as MeshInstance3D
			if m == null or m.mesh == null or m.skin == null:
				continue
			var bi := -1
			for b in m.skin.get_bind_count():
				if String(m.skin.get_bind_name(b)) == "weapon_r" or m.skin.get_bind_bone(b) == _wb:
					bi = b
			if bi < 0:
				continue
			var bind := m.skin.get_bind_pose(bi)
			for si in m.mesh.get_surface_count():
				var arr: Array = m.mesh.surface_get_arrays(si)
				var vs: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
				var bones = arr[Mesh.ARRAY_BONES]
				var ws = arr[Mesh.ARRAY_WEIGHTS]
				var per: int = (bones as PackedInt32Array).size() / maxi(vs.size(), 1) if bones != null else 0
				for vi in vs.size():
					if per > 0:
						var wsum := 0.0
						for j in per:
							if int(bones[vi * per + j]) == bi:
								wsum += float(ws[vi * per + j])
						if wsum < 0.5:
							continue
					out.append(bind * vs[vi])
	_mace_cache = out
	return out


func _farthest_from_grip(pts: PackedVector3Array) -> Vector3:
	"""The mace head: its vertex farthest from the grip (weapon_r's origin), in weapon_r's space."""
	var best := Vector3.ZERO
	var bd := -1.0
	for p in pts:
		var d := p.length_squared()
		if d > bd:
			bd = d
			best = p
	return best


# ============================================================================
# THE AURA — R-CPB-2 (source `_build_aura`, src 2648). The arena's ribbon and the ForgeLight are not here (PORT 6).
# ============================================================================
func _build_aura(band: Dictionary) -> void:
	var wire_r: float = _wire_r
	fx = Node3D.new()
	fx.name = "ChannelFX"
	fx.top_level = true
	add_child(fx)
	fx.visible = false

	# --- the smoke bed: does NOT spin ---------------------------------------
	smoke_root = Node3D.new()
	smoke_root.name = "SmokeBed"
	fx.add_child(smoke_root)
	# GL-15: ONE read, TWO halves. The bed carries the extent and the soft edge;
	# the haze carries the cloud. Neither is a second damage source.
	_bed = _smoke_bed(wire_r)
	smoke_root.add_child(_bed)
	_haze = _smoke(wire_r)
	smoke_root.add_child(_haze)

	# --- the spark ring: turns WITH his steel (PORT 3) ----------------------
	spark_root = Node3D.new()
	spark_root.name = "SparkRing"
	fx.add_child(spark_root)
	var r: float = _spark_r if _spark_r > 0.05 else 0.0
	for i in SPARK_EMITTER_OFFSETS_DEG.size():
		var pivot := Node3D.new()
		pivot.name = "SparkPivot_%d" % i
		pivot.rotation.y = deg_to_rad(float(SPARK_EMITTER_OFFSETS_DEG[i]))
		spark_root.add_child(pivot)
		var e := _sparks(r, i)
		pivot.add_child(e)
		_emitters.append(e)

	# --- LAYER ONE: THE ETCH (R-CPB-7) ---------------------------------------
	var etch: Dictionary = _build_etch(band) if ARC_CUTS else {"built": false, "removed": "R-C9-152 (PORT 21)"}

	# --- LAYER ONE-b: the EMBER GARNISH off the hammer head (PORT 11) ---------
	var head_pt := Vector3.ZERO if synthetic else _ember_point()
	_ember_local = head_pt
	_trail_mount = Node3D.new()
	_trail_mount.name = "EorKc2EmberMount"
	_trail_mount.top_level = true
	add_child(_trail_mount)
	var t := _trail()
	t.emitting = false
	_trail_mount.add_child(t)
	_trail_node = t

	# PORT 21: the FOURTH spark emitter, on the mace head (the source's _sparks(), at the head, continuous)
	_head_spark_root = Node3D.new()
	_head_spark_root.name = "HeadSparkRoot"
	_head_spark_root.top_level = true
	add_child(_head_spark_root)
	_head_sparks = _sparks(r, SPARK_EMITTER_OFFSETS_DEG.size())
	_head_sparks.name = "Sparks_head"
	_head_sparks.position = Vector3.ZERO
	_head_sparks.amount = HEAD_SPARK_AMOUNT
	_head_sparks.lifetime = HEAD_SPARK_LIFETIME_S
	(_head_sparks.draw_pass_1 as QuadMesh).size = HEAD_SPARK_QUAD
	_head_spark_root.add_child(_head_sparks)

	report["channel_fx"] = {
		"source": PAL_SRC, "etch": etch, "spark_radius_m": r, "spark_radius_basis": "PORT 4 (weapon truth, mean reach)",
		"smoke_radius_m": wire_r, "smoke_radius_basis": "PORT 5 (the source's wire radius, kept)",
		"source_contact_radius_m": SRC_CONTACT_RADIUS_M, "source_drawn_height_m": SRC_DRAWN_HEIGHT_M,
		"trail_head_point_bone_space": [head_pt.x, head_pt.y, head_pt.z], "rev_period_s": _rev_period,
		"emitters": SPARK_EMITTER_OFFSETS_DEG.size(), "tint": tint, "ember_mount_scale": SRC_EMBER_SCALE,
		"tint_basis": ("R-C9-146 / PORT 20: red = haze rims run red-hot + sparks/embers shifted %.2f along the ramp; "
			+ "original = the light haze; the arc is the source ramp on both") % EMBER_RED_SHIFT,
	}
	_set_priorities()
	_apply_fade(0.0)


func _ember_point() -> Vector3:
	"""C-9 EOR2 PORT 11: TRAIL_HEAD_FRAC of the way from the mace's pommel end to its head end, along grip -> head."""
	var ax := _head_local.normalized()
	if ax.length() < 0.5:
		return Vector3.ZERO
	var lo := INF
	var hi := -INF
	for p in _mace_points():
		var d := p.dot(ax)
		lo = minf(lo, d)
		hi = maxf(hi, d)
	if not is_finite(lo):
		return _head_local
	return ax * (lo + (hi - lo) * TRAIL_HEAD_FRAC)


func _set_priorities() -> void:
	"""C-9 EOR2 PORT 7: after the paint post pass; the bed first, as the source ordered it."""
	var after := PaintStack.AFTER_POST_PRIORITY
	_bed_mat.render_priority = after
	for m in [(_haze.draw_pass_1 as QuadMesh).material, (_trail_node.draw_pass_1 as QuadMesh).material]:
		(m as Material).render_priority = after + 1
	for e in _emitters + [_head_sparks]:
		((e.draw_pass_1 as QuadMesh).material as Material).render_priority = after + 1
	for pair in _cut_mats:
		for m in (pair as Array):
			(m as Material).render_priority = after + 1
	for m in _mm_mats:
		(m as Material).render_priority = after + 1


# ============================================================================
# THE CUTS — R-CPB-7's five properties, R-CPB-12's five clauses (source `_build_etch`, src 2849). The arena's
# station becomes his (PORT 2); `_cut_a0` is set at each cast from where his steel is (PORT 1).
# ============================================================================
func _build_etch(band: Dictionary) -> Dictionary:
	var out := {"built": false}
	if not bool(band.get("measured", false)):
		out["refusal"] = ("NO CONTACT BAND — %s. The cuts are not drawn at a guessed radius."
			% String(band.get("basis", "?")))
		return out
	var sh := ETCH_SHADER_RES as Shader
	_cut_r = band["radius_m"]
	_cut_y = band["height_m"]
	# C-9 EOR2 PORT 16: the stroke's thickness from the SOURCE's measured band (see the constant)
	var core_w: float = SRC_CONTACT_HALF_EXTENT_M * ETCH_CORE_FRAC
	var sheath_w: float = core_w * ETCH_SHEATH_MULT

	# --- the MESH LIBRARY: built once, never rebuilt, never mutated -----------
	_cut_lib = []
	var lib_tris := 0
	for cls in 2:
		var row: Array = []
		for v in CUT_VARIANTS:
			var m := _cut_mesh(cls, v, _cut_r, core_w, sheath_w)
			row.append(m)
			for si in m.get_surface_count():
				lib_tris += (m.surface_get_arrays(si)[Mesh.ARRAY_INDEX]
					as PackedInt32Array).size() / 3
		_cut_lib.append(row)

	# ⚑ NOT A CHILD OF THE SPINNING FRAME. See the header: the cuts do not spin.
	etch_root = Node3D.new()
	etch_root.name = "Etch"
	fx.add_child(etch_root)
	_cut_nodes = []
	_cut_mats = []
	# ⚑ DEFAULT IS THE SOURCE'S NODE POOL until the MultiMesh draws in the live scene: isolated, the MultiMesh matched
	#   the pool pixel for pixel (max diff 0 over 2,871 lit px); in the Barrow it drew no arc (2026-10-02, open).
	#   ?eorcuts=mm (--eorcuts mm) selects it for that work.
	_cut_mm = Slots.arg("eorcuts") == "mm"
	if _cut_mm:
		_build_cut_multimesh()
	# --- the POOL: CUT_POOL nodes, each with its own two materials (the source's; ?eorcuts=pool) ---------
	for i in (0 if _cut_mm else CUT_POOL):
		var mi := MeshInstance3D.new()
		mi.name = "Cut_%02d" % i
		mi.mesh = (_cut_lib[0] as Array)[0]
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.extra_cull_margin = _cut_r * 2.0
		mi.visible = false
		var pair: Array = []
		for shell in [
				{"e": ETCH_CORE_ENERGY * ETCH_SHEATH_ENERGY_FRAC,
					"t": ETCH_TAIL_ENERGY * ETCH_SHEATH_ENERGY_FRAC, "sharp": 1.15},
				{"e": ETCH_CORE_ENERGY, "t": ETCH_TAIL_ENERGY, "sharp": 2.6}]:
			var mat := ShaderMaterial.new()
			mat.shader = sh
			mat.set_shader_parameter("head_energy", float(shell["e"]))
			mat.set_shader_parameter("tail_energy", float(shell["t"]))
			mat.set_shader_parameter("edge_sharpness", float(shell["sharp"]))
			mat.set_shader_parameter("stroke_age", 0.0)
			mat.set_shader_parameter("core_color", PAL_HEAD)
			mat.set_shader_parameter("mid_color", PAL_MID)
			mat.set_shader_parameter("tail_color", PAL_TAIL)
			mat.set_shader_parameter("mid_energy", CUT_MID_ENERGY
				* (1.0 if shell["sharp"] > 2.0 else ETCH_SHEATH_ENERGY_FRAC))
			mat.set_shader_parameter("mid_at", PAL_KNEE_AT)
			mat.set_shader_parameter("decay_gamma", PAL_GAMMA)
			mat.set_shader_parameter("tail_fade", CUT_TAIL_FADE)
			pair.append(mat)
		mi.set_surface_override_material(0, pair[0])
		mi.set_surface_override_material(1, pair[1])
		etch_root.add_child(mi)
		_cut_nodes.append(mi)
		_cut_mats.append(pair)
	_cut_ready = true

	out["built"] = true
	out["radius_m"] = _cut_r
	out["height_m"] = _cut_y
	out["persist_revs"] = CUT_PERSIST_REVS
	out["core_half_width_m"] = core_w
	out["measured_half_extent_m_not_used"] = band["half_extent_m"]
	out["sheath_half_width_m"] = sheath_w
	out["planes"] = ETCH_PLANES
	out["library_meshes"] = 2 * CUT_VARIANTS
	out["draw"] = "multimesh (2 draws)" if _cut_mm else "node pool (2 draws per live stroke)"
	out["library_triangles"] = lib_tris
	out["pool"] = CUT_POOL
	out["undulating"] = CUT_UNDULATE_DEFAULT
	out["alive_expected"] = CUT_PERSIST_REVS * float(CUT_PER_REV)
	return out


# C-9 EOR2 PORT 19: the twelve library meshes merged into ONE two-surface mesh (each vertex tagged with its variant
# id in COLOR.b), drawn by one MultiMesh of CUT_POOL instances. The library itself is untouched (the node pool and
# the warm-up still use it).
func _build_cut_multimesh() -> void:
	var merged := ArrayMesh.new()
	for si in 2:                                  # 0 sheath, 1 core -- the library's own surface order
		var verts := PackedVector3Array()
		var cols := PackedColorArray()
		var uvs := PackedVector2Array()
		var uv2s := PackedVector2Array()
		var idx := PackedInt32Array()
		for cls in 2:
			for v in CUT_VARIANTS:
				var id := cls * CUT_VARIANTS + v
				var a: Array = ((_cut_lib[cls] as Array)[v] as ArrayMesh).surface_get_arrays(si)
				var base := verts.size()
				verts.append_array(a[Mesh.ARRAY_VERTEX])
				for c in (a[Mesh.ARRAY_COLOR] as PackedColorArray):
					cols.append(Color(c.r, c.g, (float(id) + 0.5) / CUT_VARIANT_CODES, c.a))
					# ⚑ THE MULTIMESH READS UV / UV2, NOT COLOR: on the Compatibility renderer a MultiMesh without
					#   per-instance colours hands the vertex shader a COLOR that is not the mesh's (measured: the
					#   tagged MultiMesh row drew NOTHING beside the node pool's 12 strokes). UV = (age, rim), the
					#   same two numbers COLOR.r/.g carry; UV2.x = the variant id, exact.
					uvs.append(Vector2(c.r, c.g))
					uv2s.append(Vector2(float(id), 0.0))
				for i in (a[Mesh.ARRAY_INDEX] as PackedInt32Array):
					idx.append(base + i)
		var arr := []
		arr.resize(Mesh.ARRAY_MAX)
		arr[Mesh.ARRAY_VERTEX] = verts
		arr[Mesh.ARRAY_COLOR] = cols
		arr[Mesh.ARRAY_TEX_UV] = uvs
		arr[Mesh.ARRAY_TEX_UV2] = uv2s
		arr[Mesh.ARRAY_INDEX] = idx
		merged.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	_mm = MultiMesh.new()
	_mm.transform_format = MultiMesh.TRANSFORM_3D
	_mm.use_custom_data = true
	_mm.mesh = merged
	_mm.instance_count = CUT_POOL
	_mm.visible_instance_count = 0
	var reach := _cut_r + 1.0
	_mm.custom_aabb = AABB(Vector3(-reach, -1.0, -reach), Vector3(2.0 * reach, _cut_y + CUT_VERT_BAND_M + 2.0, 2.0 * reach))
	_mmi = MultiMeshInstance3D.new()
	_mmi.name = "Cuts"
	_mmi.multimesh = _mm
	_mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_mm_mats = []
	for shell in _cut_shells():
		_mm_mats.append(_cut_material(ETCH_MM_SHADER_RES, shell))
	merged.surface_set_material(0, _mm_mats[0])
	merged.surface_set_material(1, _mm_mats[1])
	etch_root.add_child(_mmi)


func _cut_shells() -> Array:
	return [{"e": ETCH_CORE_ENERGY * ETCH_SHEATH_ENERGY_FRAC,
			"t": ETCH_TAIL_ENERGY * ETCH_SHEATH_ENERGY_FRAC, "sharp": 1.15},
		{"e": ETCH_CORE_ENERGY, "t": ETCH_TAIL_ENERGY, "sharp": 2.6}]


func _cut_material(sh: Shader, shell: Dictionary) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("head_energy", float(shell["e"]))
	mat.set_shader_parameter("tail_energy", float(shell["t"]))
	mat.set_shader_parameter("edge_sharpness", float(shell["sharp"]))
	mat.set_shader_parameter("core_color", PAL_HEAD)
	mat.set_shader_parameter("mid_color", PAL_MID)
	mat.set_shader_parameter("tail_color", PAL_TAIL)
	mat.set_shader_parameter("mid_energy", CUT_MID_ENERGY
		* (1.0 if shell["sharp"] > 2.0 else ETCH_SHEATH_ENERGY_FRAC))
	mat.set_shader_parameter("mid_at", PAL_KNEE_AT)
	mat.set_shader_parameter("decay_gamma", PAL_GAMMA)
	mat.set_shader_parameter("tail_fade", CUT_TAIL_FADE)
	return mat


# ============================================================================
# THE LAYOUT — one function, and everything reads it (source `cut_layout_at`, src 3024). Its argument is now
# REVOLUTIONS directly (PORT 1); the stationary branch is not ported (segment A was the comparison's reference).
# One addition: no birth at or after `_end_revs` (PORT 9: a released channel inscribes nothing new).
# ============================================================================
func cut_layout_at(revs: float) -> Array:
	var out: Array = []
	if not _cut_ready:
		return out
	# ---- THE UNDULATING CADENCE (R-CPB-14) ---------------------------------
	# ⚑ THE WALK STARTS AT EPOCH ZERO ON EVERY CALL, AND THAT IS THE POINT.
	var s := 0.0                   # this epoch's start, in revs
	var n := 0                     # global birth index, across all epochs
	var k := 0
	while s <= revs and k < CUT_EPOCH_WALK_MAX:
		var lk := _epoch_len(k)
		var occ: float = float(lk) / float(CUT_PER_REV)
		if s + occ >= revs - CUT_PERSIST_REVS:
			for i in lk:
				var g: int = n + i
				var birth: float = s + (float(i) + 0.5 + _cut_jitter(k, g)) / float(CUT_PER_REV)
				var age: float = revs - birth
				if age < 0.0 or age >= CUT_PERSIST_REVS or birth >= _end_revs:
					continue
				out.append(_cut_row(k, g, k, i, birth, age))
		n += lk
		s += occ + _epoch_gap_revs(k)
		k += 1
	return out


func _cut_row(k: int, g: int, rev: int, slot: int, birth: float, age: float) -> Dictionary:
	var level: int = _cut_h(0x2C93, k, g) % CUT_VERT_LEVELS
	return {
		"g": g, "rev": rev, "slot": slot, "epoch": k,
		"claw": absi(g) % 2,
		"variant": _cut_h(0x51ED, k, g) % CUT_VARIANTS,
		"level": level,
		"y_off_m": (float(level) / float(CUT_VERT_LEVELS - 1) - 0.5) * CUT_VERT_BAND_M,
		"birth_revs": birth, "age_revs": age,
		"age_frac": age / CUT_PERSIST_REVS,
		# ⚑ THE ANGLE IS NOT A FREE PARAMETER. A cut is a mark left where the
		#   steel was, so its angle is the head's angle AT ITS BIRTH.
		"angle_rad": fposmod(_cut_a0 + TAU * birth, TAU),
		"pool": absi(g) % CUT_POOL,
	}


static func _cut_h(salt: int, k: int, g: int) -> int:
	if k < 0:
		return _hash2(CUT_SEED ^ salt, g)
	return _hash2(_hash2(CUT_SEED ^ salt, k), g)


func _cut_jitter(k: int, g: int) -> float:
	return (float(_cut_h(0, k, g) % 10000) / 10000.0 - 0.5) * CUT_JITTER


static func _epoch_len(k: int) -> int:
	return CUT_EPOCH_LEN_LO + _hash2(CUT_SEED ^ 0x1E90, k) % (CUT_EPOCH_LEN_HI - CUT_EPOCH_LEN_LO + 1)


static func _epoch_gap_revs(k: int) -> float:
	return lerpf(CUT_EPOCH_GAP_LO_REVS, CUT_EPOCH_GAP_HI_REVS,
		float(_hash2(CUT_SEED ^ 0x6A17, k) % 10000) / 10000.0)


# ============================================================================
# ONE STROKE MESH (source `_cut_mesh`, src 3210). Two surfaces: 0 the bloom sheath, 1 the crisp core.
# ============================================================================
func _cut_mesh(cls: int, variant: int, r: float, core_w: float, sheath_w: float) -> ArrayMesh:
	var m := ArrayMesh.new()
	var h := _hash2(CUT_SEED ^ 0x7A11, cls * 131 + variant)
	var arc_revs: float = lerpf(CUT_ARC_REVS_LO, CUT_ARC_REVS_HI,
		float(h % 1000) / 1000.0)
	for shell in [sheath_w, core_w]:
		var verts := PackedVector3Array()
		var cols := PackedColorArray()
		var idx := PackedInt32Array()
		if cls == 0:
			_cut_ribbon(verts, cols, idx, r, 0.0, 0.0, arc_revs, shell, 0.0)
		else:
			var lines: int = CLAW_LINES_LO + int((h >> 10) % (CLAW_LINES_HI - CLAW_LINES_LO + 1))
			for j in lines:
				var hj := _hash2(CUT_SEED ^ 0x3B0D, (cls * 131 + variant) * 17 + j)
				var lead: float = CLAW_STAGGER_REVS * float(hj % 1000) / 1000.0
				var tail: float = CLAW_STAGGER_REVS * float((hj >> 10) % 1000) / 1000.0
				var w: float = shell * lerpf(CLAW_WIDTH_LO, CLAW_WIDTH_HI,
					float((hj >> 20) % 1000) / 1000.0)
				var y: float = (float(j) - 0.5 * float(lines - 1)) * CLAW_GAP_M
				_cut_ribbon(verts, cols, idx, r, y, lead,
					maxf(arc_revs - lead + tail, 0.02), w, lead)
		var arr := []
		arr.resize(Mesh.ARRAY_MAX)
		arr[Mesh.ARRAY_VERTEX] = verts
		arr[Mesh.ARRAY_COLOR] = cols
		arr[Mesh.ARRAY_INDEX] = idx
		m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	return m


func _cut_ribbon(verts: PackedVector3Array, cols: PackedColorArray, idx: PackedInt32Array,
		r_center: float, y: float, a_lead: float, arc_revs: float, half_w: float,
		age0: float) -> void:
	var rows := [-1.0, -0.5, 0.0, 0.5, 1.0]
	var per_ring := rows.size()
	var seg: int = maxi(6, int(round(CUT_SEG_PER_REV * arc_revs)))
	var arc := TAU * arc_revs
	var a0 := -TAU * a_lead
	for p in ETCH_PLANES:
		# planes are spread over 180 deg, not 360: a ribbon is two-sided, so a
		# fourth plane at 180 would be a duplicate of the first.
		var psi := PI * float(p) / float(ETCH_PLANES)
		var base := verts.size()
		for i in (seg + 1):
			var u := float(i) / float(seg)
			var ang := a0 - arc * u
			var sa := sin(ang)
			var ca := cos(ang)
			var centre := Vector3(sa * r_center, y, ca * r_center)
			var radial := Vector3(sa, 0.0, ca)                 # outward, in the ring's plane
			var d := (radial * cos(psi) + Vector3.UP * sin(psi)).normalized()
			var w: float = half_w * lerpf(1.0, ETCH_TAIL_TAPER, u)
			var age: float = (age0 + arc_revs * u) / CUT_PERSIST_REVS
			for j in per_ring:
				var t: float = rows[j]
				verts.append(centre + d * (t * w))
				cols.append(Color(clampf(age, 0.0, 1.0), absf(t), 0.0, 1.0))
			if i < seg:
				for j in (per_ring - 1):
					var a := base + i * per_ring + j
					var b := a + per_ring
					idx.append_array([a, b, a + 1, a + 1, b, b + 1])


# LAYER ONE-b — the EMBER GARNISH (source `_trail`, src 3282). Rides the hammer head; emits in WORLD space
# so what it leaves behind is where the steel actually was.
func _trail() -> GPUParticles3D:
	var p := GPUParticles3D.new()
	p.name = "HammerTrail"
	_pin_seed(p, FX_SEED_TRAIL)
	p.amount = TRAIL_AMOUNT
	p.lifetime = TRAIL_LIFETIME_S
	p.explosiveness = 0.0
	p.randomness = 0.25
	p.local_coords = false
	p.transform_align = GPUParticles3D.TRANSFORM_ALIGN_Z_BILLBOARD
	p.emitting = true               # CONTINUOUS — that is the layer's whole job

	var m := ParticleProcessMaterial.new()
	m.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
	m.emission_sphere_radius = TRAIL_SPREAD_M
	m.direction = Vector3(0.0, 1.0, 0.0)
	m.spread = 12.0
	m.initial_velocity_min = 0.0
	m.initial_velocity_max = 0.35
	m.gravity = Vector3(0.0, -1.2, 0.0)
	m.damping_min = 2.0
	m.damping_max = 4.0
	m.scale_min = 0.6
	m.scale_max = 1.0
	var sc := CurveTexture.new()
	var cu := Curve.new()
	cu.add_point(Vector2(0.0, 1.0))
	cu.add_point(Vector2(1.0, 0.05))
	sc.curve = cu
	m.scale_curve = sc
	# ⚑ THE EMBER GARNISH IS THE FOURTH CONSUMER of the one ramp (R-CPB-13).
	m.color_ramp = GradientTexture1D.new()
	(m.color_ramp as GradientTexture1D).gradient = palette_gradient(0.85, 0.0, _red_shift())
	p.process_material = m

	var q := QuadMesh.new()
	q.size = Vector2(TRAIL_QUAD_M, TRAIL_QUAD_M)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX            # PORT 21 (source: ADD)
	mat.vertex_color_use_as_albedo = true
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	mat.albedo_texture = SPARK_TEX_RES
	q.material = mat
	p.draw_pass_1 = q
	return p


func _sparks(radius: float, idx: int) -> GPUParticles3D:
	var p := GPUParticles3D.new()
	p.name = "Sparks_%d" % idx
	_pin_seed(p, FX_SEED_SPARK + idx)
	p.amount = 40
	p.lifetime = SPARK_LIFETIME_S
	p.explosiveness = 0.0
	p.randomness = 0.55
	p.local_coords = false          # the trail stays where it was thrown
	p.transform_align = GPUParticles3D.TRANSFORM_ALIGN_Z_BILLBOARD_Y_TO_VELOCITY
	p.position = Vector3(radius, SPARK_EMITTER_Y_M, 0.0)
	p.emitting = false              # the gate opens in _process, per revolution

	var m := ParticleProcessMaterial.new()
	m.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	m.emission_box_extents = Vector3(0.04, 0.10, 0.04)
	# tangential: +Z in the pivot's local frame is the direction of travel
	m.direction = Vector3(0.0, 0.25, 1.0)
	m.spread = 26.0
	# C-9 EOR2 PORT 10: his steel's period, not the source's 0.36
	var v: float = TAU * maxf(radius, 0.4) / _rev_period
	m.initial_velocity_min = v * 0.35
	m.initial_velocity_max = v * 0.85
	m.gravity = Vector3(0.0, -7.5, 0.0)
	m.damping_min = 1.5
	m.damping_max = 3.5
	m.scale_min = 0.55
	m.scale_max = 1.25
	var sc := CurveTexture.new()
	var cu := Curve.new()
	cu.add_point(Vector2(0.0, 1.0))
	cu.add_point(Vector2(1.0, 0.15))
	sc.curve = cu
	m.scale_curve = sc
	# ⚑ R-CPB-13: THE BURSTS NOW DIE RED, BECAUSE THEY READ THE SAME RAMP.
	var gt := GradientTexture1D.new()
	gt.gradient = palette_gradient(1.0, 0.0, _red_shift())
	m.color_ramp = gt
	p.process_material = m

	var q := QuadMesh.new()
	q.size = Vector2(0.045, 0.30)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX            # PORT 21 (source: ADD)
	mat.vertex_color_use_as_albedo = true
	mat.disable_receive_shadows = true
	# PORT 21b: a generated STREAK, not spark_04_a -- that texture is a faint lightning tendril (mean alpha 0.07), and
	#   squeezed into a 0.045 x 0.30 m streak quad it is mostly empty: the source's sparks never read as sparks
	mat.albedo_texture = _streak_texture()
	q.material = mat
	p.draw_pass_1 = q
	return p


static var _streak_cache: ImageTexture = null


static func _streak_texture() -> ImageTexture:
	"""PORT 21b: a soft streak, 16 x 64: a bright core, gaussian across (sigma 0.30 of the half-width), tapered along
	(full over the middle, smoothstepped to nothing in the last 20 % at each end). White: the ramp colours it."""
	if _streak_cache != null:
		return _streak_cache
	var w := 16
	var h := 64
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	for y in h:
		var v := (float(y) + 0.5) / float(h)
		var along := smoothstep(0.0, 0.2, v) * (1.0 - smoothstep(0.8, 1.0, v))
		for x in w:
			var u := ((float(x) + 0.5) / float(w) - 0.5) * 2.0
			var across := exp(-(u * u) / (2.0 * 0.30 * 0.30))
			img.set_pixel(x, y, Color(1.0, 1.0, 1.0, clampf(across * along, 0.0, 1.0)))
	_streak_cache = ImageTexture.create_from_image(img)
	return _streak_cache


func _smoke(outer_r: float) -> GPUParticles3D:
	var p := GPUParticles3D.new()
	p.name = "SmokeHaze"
	_pin_seed(p, FX_SEED_SMOKE)
	p.amount = SMOKE_AMOUNT
	p.lifetime = SMOKE_LIFETIME_S
	p.preprocess = SMOKE_LIFETIME_S   # the bed exists before frame one
	p.randomness = 0.7
	p.local_coords = false
	p.position = Vector3(0.0, 0.10, 0.0)
	p.emitting = false                # PORT 9: restarted at each cast

	var m := ParticleProcessMaterial.new()
	m.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_RING
	m.emission_ring_axis = Vector3.UP
	m.emission_ring_radius = outer_r
	m.emission_ring_inner_radius = outer_r * SMOKE_INNER_FRAC
	m.emission_ring_height = 0.30
	m.direction = Vector3(0.0, 1.0, 0.0)
	m.spread = 14.0
	m.initial_velocity_min = 0.04
	m.initial_velocity_max = 0.18
	m.gravity = Vector3.ZERO
	m.angular_velocity_min = -22.0
	m.angular_velocity_max = 22.0
	m.scale_min = 0.9
	m.scale_max = 2.6
	# ⚑ LOW PER-PARTICLE ALPHA IS WHAT MAKES IT CLOUDY. Cloud is VARIANCE, and variance comes from overlap: at 0.26
	#   each, the density is wherever the quads happen to stack. The DARKNESS is the bed's job; the haze's job is to
	#   stop the bed being a disc.
	# C-9 EOR2 PORT 17: the colours are the snow retint; the ALPHAS are the source's, stop for stop
	# PORT 21: eortint=red lerps each colour stop toward SMOKE_RED by the chosen strength (alphas untouched)
	var k := _smoke_red()
	var c0 := SNOW_HAZE_C0.lerp(SMOKE_RED, k)
	var c16 := SNOW_HAZE_C16.lerp(SMOKE_RED, k)
	var c70 := SNOW_HAZE_C70.lerp(SMOKE_RED, k)
	var c1 := SNOW_HAZE_C1.lerp(SMOKE_RED, k)
	var g := Gradient.new()
	g.set_color(0, Color(c0.r, c0.g, c0.b, 0.0))
	g.set_color(1, Color(c1.r, c1.g, c1.b, 0.0))
	g.add_point(0.16, Color(c16.r, c16.g, c16.b, 0.30))
	g.add_point(0.70, Color(c70.r, c70.g, c70.b, 0.22))
	var gt := GradientTexture1D.new()
	gt.gradient = g
	m.color_ramp = gt
	p.process_material = m

	var q := QuadMesh.new()
	q.size = Vector2(2.3, 2.3)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	mat.vertex_color_use_as_albedo = true
	mat.disable_receive_shadows = true
	mat.no_depth_test = false
	# C-9 EOR2 PORT 18: soft particles -- the quad fades out where it meets the snow, so it draws no line there
	mat.proximity_fade_enabled = true
	mat.proximity_fade_distance = HAZE_SOFT_M
	mat.albedo_texture = SMOKE_TEX_RES
	q.material = mat
	_haze_mat = mat
	# C-9 EOR2 PORT 18 / 20: BOTH variants draw the haze through kc2_haze_ember.gdshader -- one haze, the ember gain 0
	#   on "original". (The StandardMaterial above is the source's material, kept as the record; its own proximity
	#   fade measured erasing the haze on snow: 0.858 luma inside the disc against 0.856 outside.)
	var em := ShaderMaterial.new()
	if em != null:
		em.shader = HAZE_EMBER_SHADER_RES
		em.set_shader_parameter("albedo_tex", SMOKE_TEX_RES)
		em.set_shader_parameter("proximity_fade_distance", HAZE_SOFT_M)
		em.set_shader_parameter("ember_mid", PAL_MID)
		em.set_shader_parameter("ember_tail", PAL_TAIL)
		em.set_shader_parameter("ember_gain", 0.0)            # PORT 21: the rim ember is off (R-C9-152)
		em.set_shader_parameter("rim_lo", EMBER_RIM_LO)
		em.set_shader_parameter("rim_hi", EMBER_RIM_HI)
		em.set_shader_parameter("duty", EMBER_DUTY)
		em.set_shader_parameter("rate", EMBER_RATE)
		em.set_shader_parameter("waves", EMBER_WAVES)
		em.set_shader_parameter("jitter", EMBER_JITTER)
		em.set_shader_parameter("rim_r_in", EMBER_RIM_R_IN)
		em.set_shader_parameter("rim_r_out", EMBER_RIM_R_OUT)
		q.material = em
		_haze_ember = em
	p.draw_pass_1 = q
	# the bed is a low pool, not a column
	p.visibility_aabb = AABB(Vector3(-outer_r * 1.6, -0.2, -outer_r * 1.6),
		Vector3(outer_r * 3.2, SMOKE_TOP_M + 0.6, outer_r * 3.2))
	return p


# THE DARK BED (source `_smoke_bed`, src 3481) — the ground half of the smoke read; owns the SOFT EDGE (R-CPB-5b).
func _smoke_bed(outer_r: float) -> MeshInstance3D:
	var lo := outer_r * (1.0 - SMOKE_EDGE_SOFT_FRAC)
	var rim := outer_r * (1.0 + SMOKE_EDGE_SOFT_FRAC)
	var verts := PackedVector3Array()
	var cols := PackedColorArray()
	var idx := PackedInt32Array()
	# C-9 EOR2 PORT 17: the Barrow's snow-shadow colour at SNOW_BED_ALPHA; the profile (lo, rim, smoothstep) is the source's
	var bc := SNOW_BED_COLOR
	verts.append(Vector3.ZERO)
	cols.append(Color(bc.r, bc.g, bc.b, SNOW_BED_ALPHA))
	for i in SMOKE_BED_RINGS:
		var r: float = rim * float(i + 1) / float(SMOKE_BED_RINGS)
		var a: float = SNOW_BED_ALPHA * (1.0 - smoothstep(lo, rim, r))
		for j in SMOKE_BED_SEGMENTS:
			var th: float = TAU * float(j) / float(SMOKE_BED_SEGMENTS)
			verts.append(Vector3(sin(th) * r, 0.0, cos(th) * r))
			cols.append(Color(bc.r, bc.g, bc.b, a))
	for j in SMOKE_BED_SEGMENTS:
		idx.append_array([0, 1 + j, 1 + ((j + 1) % SMOKE_BED_SEGMENTS)])
	for i in (SMOKE_BED_RINGS - 1):
		var b0 := 1 + i * SMOKE_BED_SEGMENTS
		var b1 := b0 + SMOKE_BED_SEGMENTS
		for j in SMOKE_BED_SEGMENTS:
			var j2 := (j + 1) % SMOKE_BED_SEGMENTS
			idx.append_array([b0 + j, b1 + j, b0 + j2, b0 + j2, b1 + j, b1 + j2])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_COLOR] = cols
	arr[Mesh.ARRAY_INDEX] = idx
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)

	var mi := MeshInstance3D.new()
	mi.name = "SmokeDarkBed"
	mi.mesh = mesh
	mi.position = Vector3(0.0, SMOKE_BED_LIFT_M, 0.0)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	mat.vertex_color_use_as_albedo = true
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.disable_receive_shadows = true
	# ⚑ THE BED DRAWS FIRST, AND IT HAS TO BE SAID EXPLICITLY (source: render_priority -8; PORT 7 sets it).
	mi.material_override = mat
	_bed_mat = mat
	return mi


# ============================================================================
# per frame (source `apply_tick`, src 3564, on PORT 1's clock)
# ============================================================================
func begin() -> void:
	if _state != S.IDLE:
		return
	_state = S.SUSTAIN
	_revs = 0.0
	_end_revs = INF
	_fall_t = 0.0
	_prev_b = _head_bearing()
	_cut_a0 = _prev_b                            # the steel's own angle at the cast (source: band angle at tick 0)
	_place_station()
	_place_embers()
	fx.visible = _vfx
	_haze.restart()                              # PORT 9: with its own preprocess -- "the bed exists before frame one"
	_haze.emitting = true
	_trail_node.emitting = true
	_trail_node.visible = _vfx
	_head_sparks.emitting = true
	_head_sparks.visible = _vfx


func end() -> void:
	if _state == S.SUSTAIN:
		_state = S.FALLING
		_end_revs = _revs
		_fall_t = 0.0
		_haze.emitting = false
		_trail_node.emitting = false
		_head_sparks.emitting = false


func state_name() -> String:
	return ["IDLE", "SUSTAIN", "FALLING"][_state]


func channel_weight() -> float:
	return _fade


## The perf CONTROL (perf_fireball.gd, the source's "novfx" condition): every layer hidden, the clock still running.
func set_vfx_visible(v: bool) -> void:
	_vfx = v
	if fx != null:
		fx.visible = v and _state != S.IDLE
	if _trail_node != null:
		_trail_node.visible = v
	if _head_sparks != null:
		_head_sparks.visible = v


func _process(dt: float) -> void:
	if _warming or _state == S.IDLE:
		return
	_place_station()
	_place_embers()
	var b := _head_bearing()
	_place_head_sparks(b)
	if _state == S.SUSTAIN:
		_revs += wrapf(b - _prev_b, -PI, PI) / TAU
		_fade = minf(1.0, _fade + dt / FADE_IN_S)
	else:
		# PORT 9: released -- the clock runs on at his measured rate; the haze and the bed fade
		_revs += dt / maxf(_rev_period, 1e-3)
		_fall_t += dt
		_fade = maxf(0.0, 1.0 - _fall_t / FADE_OUT_S)
	_prev_b = b
	_apply_fade(_fade)
	if _haze_ember != null:
		_haze_ember.set_shader_parameter("ember_clock", _revs)
		_haze_ember.set_shader_parameter("ember_centre", smoke_root.global_position)
	# PORT 3: the spark ring turns with his steel, the hammer at the source's body-frame angle
	spark_root.rotation.y = b - SRC_HAMMER_BEARING_RAD
	var on := _state == S.SUSTAIN
	for i in _emitters.size():
		var want: bool = on and emitter_open(i, _revs)
		if _emitters[i].emitting != want:
			_emitters[i].emitting = want
	_drive_cuts(_revs, true)
	if _state == S.FALLING and _fall_t >= FADE_OUT_S and _revs - _end_revs >= CUT_PERSIST_REVS:
		_state = S.IDLE
		fx.visible = false
		_drive_cuts(_revs, false)


func _red_shift() -> float:
	return 0.0                                     # PORT 21: no red shift -- the source ramp (R-C9-152)


func _smoke_red() -> float:
	if tint != "red":
		return 0.0
	var q := Slots.arg("eorsmoke")
	var i := (int(q) - 1) if q in ["1", "2", "3"] else SMOKE_RED_DEFAULT
	return float(SMOKE_RED_STRENGTHS[i])


func _smoke_opacity() -> float:
	if _smoke_opacity_k < 0.0:
		var q := Slots.arg("eorsmokea")
		_smoke_opacity_k = float(SMOKE_OPACITY_CHOICES[q]) if SMOKE_OPACITY_CHOICES.has(q) else SMOKE_OPACITY_DEFAULT
	return _smoke_opacity_k


func _apply_fade(f: float) -> void:
	var k := _smoke_opacity()                      # the HAZE only; the bed below keeps f
	_haze_mat.albedo_color = Color(1.0, 1.0, 1.0, f * k)
	if _haze_ember != null:
		_haze_ember.set_shader_parameter("fade", f * k)
	_bed_mat.albedo_color = Color(1.0, 1.0, 1.0, f)


func _place_station() -> void:
	"""C-9 EOR2 PORT 2: the non-spinning layers stand where he stands -- his ground position, never his yaw."""
	if synthetic:
		fx.global_transform = Transform3D(Basis(), syn_station)
		return
	var o := _rig.global_transform.origin
	fx.global_transform = Transform3D(Basis(), o)
	# the smoke's floor is the SNOW he stands in, not the ground under it (his origin is floor_y; the snow is up to
	# ~0.3 m deep): the bed at the source's 0.02 m lift and the haze's lower half would otherwise be buried
	if _snow != null and _snow.has_method("depth_at"):
		var top: float = float(_snow.get("floor_y")) + float(_snow.depth_at(Vector2(o.x, o.z)))
		smoke_root.position.y = maxf(top - o.y, 0.0)


func _place_embers() -> void:
	"""C-9 EOR2 PORT 15: the ember mount at the mace's ember point, +Y along grip -> head (the source's haft axis),
	scaled by the source emitter's own measured scale."""
	if synthetic:
		var ys := syn_axis.normalized()
		var xs := ys.cross(Vector3.UP)
		if xs.length() < 1e-4:
			xs = Vector3.RIGHT
		xs = xs.normalized()
		_trail_mount.global_transform = Transform3D(
			Basis(xs, ys, xs.cross(ys).normalized()).orthonormalized().scaled(Vector3.ONE * SRC_EMBER_SCALE), syn_ember)
		return
	var wx := _skel.global_transform * _skel.get_bone_global_pose(_wb)
	var g := wx.origin
	var hd := wx * _head_local
	var y := (hd - g).normalized()
	if y.length() < 0.5:
		y = Vector3.UP
	var x := y.cross(Vector3.UP)
	if x.length() < 1e-4:
		x = Vector3.RIGHT
	x = x.normalized()
	var bs := Basis(x, y, x.cross(y).normalized()).orthonormalized().scaled(Vector3.ONE * SRC_EMBER_SCALE)
	_trail_mount.global_transform = Transform3D(bs, wx * _ember_local)


func _place_head_sparks(b: float) -> void:
	"""PORT 21: the fourth emitter at the mace head, its frame turned as the source's pivots are -- local +X radial
	(outward), +Z the source's 'direction of travel' axis -- so its sparks leave the head the way the source's leave
	their pivots."""
	var hd: Vector3
	if synthetic:
		hd = syn_head
	else:
		hd = _skel.global_transform * _skel.get_bone_global_pose(_wb) * _head_local
	# the source pivot at bearing beta has local +X at beta: rotation.y = beta - PI/2
	_head_spark_root.global_transform = Transform3D(Basis(Vector3.UP, b - PI * 0.5), hd)


func _head_bearing() -> float:
	"""C-9 EOR2 PORT 13: the bearing of the mace head about his spin axis (atan2(x, z), the source's convention)."""
	if synthetic:
		return atan2(syn_head.x - syn_station.x, syn_head.z - syn_station.z)
	var o := _rig.global_transform.origin
	var hd := _skel.global_transform * _skel.get_bone_global_pose(_wb) * _head_local
	return atan2(hd.x - o.x, hd.z - o.z)


# Position, age and reveal every live cut (source `_drive_cuts`, src 3606). Pure in `revs`.
func _drive_cuts(revs: float, on: bool) -> void:
	if not _cut_ready:
		return
	var live := {}
	if on:
		for row in cut_layout_at(revs):
			var r: Dictionary = row
			var k: int = r["pool"]
			if live.has(k):
				continue
			live[k] = r
	if _cut_mm:
		# PORT 19: the live strokes in pool-slot order (deterministic), one instance each; the rest not drawn
		var keys := live.keys()
		keys.sort()
		for n in keys.size():
			var r: Dictionary = live[keys[n]]
			var xf := Transform3D(Basis(Vector3.UP, float(r["angle_rad"])), Vector3(0.0, _cut_y + float(r["y_off_m"]), 0.0))
			_mm.set_instance_transform(n, xf)
			_mm.set_instance_custom_data(n, Color(float(int(r["claw"]) * CUT_VARIANTS + int(r["variant"])),
				float(r["age_frac"]), 0.0, 0.0))
		_mm.visible_instance_count = keys.size()
		return
	# ⚑ EVERY SLOT IS WRITTEN EVERY TICK, INCLUDING THE DARK ONES.
	for i in CUT_POOL:
		var mi: MeshInstance3D = _cut_nodes[i]
		var vis: bool = live.has(i)
		var want_mesh: Mesh = (_cut_lib[0] as Array)[0]
		var yaw := 0.0
		var y := _cut_y
		var age := 1.0
		if vis:
			var r: Dictionary = live[i]
			want_mesh = (_cut_lib[int(r["claw"])] as Array)[int(r["variant"])]
			yaw = float(r["angle_rad"])
			y = _cut_y + float(r["y_off_m"])
			age = float(r["age_frac"])
		if mi.mesh != want_mesh:
			mi.mesh = want_mesh
		mi.rotation.y = yaw
		mi.position.y = y
		for mat in (_cut_mats[i] as Array):
			(mat as ShaderMaterial).set_shader_parameter("stroke_age", age)
		if mi.visible != vis:
			mi.visible = vis


# ⚑ THE BROKEN RING, AND IT IS A PURE FUNCTION OF THE CLOCK (source `emitter_open`, src 3667, on revolutions:
#   rev = floor(revs), phase = frac(revs) -- the source's t_s / player_rev_period_s, PORT 1).
static func emitter_open(idx: int, revs: float) -> bool:
	var rev := floori(revs)
	var ph: float = fposmod(revs, 1.0)
	var h := _hash2(idx * 7919, rev)
	var bursts := 1 + int(h % 2)                       # once or twice this circle
	for k in bursts:
		var hk := _hash2(idx * 7919 + 131 * (k + 1), rev)
		var start := float(hk % 1000) / 1000.0
		var span := 0.10 + float((hk >> 10) % 130) / 1000.0   # 0.10 .. 0.23 of a circle
		var d: float = fposmod(ph - start, 1.0)
		if d < span:
			return true
	return false


static func _hash2(a: int, b: int) -> int:
	var x := (a * 73856093) ^ (b * 19349663)
	x = (x ^ (x >> 13)) * 1274126177
	return absi(x ^ (x >> 16))


# ============================================================================
# C-9 EOR2 PORT 12: WARM-UP. Every layer drawn once, at him, under the veil: the haze restarted (its preprocess
# path), all three spark emitters and the embers emitting, two cut slots (sword + claw) shown mid-life.
# ============================================================================
func warm(on: bool, _at: Vector3) -> void:
	_warming = on
	if on:
		_place_station()
		_place_embers()
		fx.visible = true
		_apply_fade(0.04)
		if not _haze.emitting:
			_haze.restart()
		_haze.emitting = true
		for e in _emitters:
			e.emitting = true
		_trail_node.emitting = true
		_head_sparks.emitting = true
		if _cut_ready and _cut_mm:
			for i in 2:                          # a sword and a claw instance, mid-life
				_mm.set_instance_transform(i, Transform3D(Basis(), Vector3(0.0, _cut_y, 0.0)))
				_mm.set_instance_custom_data(i, Color(float(i * CUT_VARIANTS), 0.5, 0.0, 0.0))
			_mm.visible_instance_count = 2
		elif _cut_ready:
			for i in 2:
				var mi: MeshInstance3D = _cut_nodes[i]
				mi.mesh = (_cut_lib[i] as Array)[0]
				mi.position.y = _cut_y
				mi.visible = true
				for mat in (_cut_mats[i] as Array):
					(mat as ShaderMaterial).set_shader_parameter("stroke_age", 0.5)
	else:
		fx.visible = false
		_haze.emitting = false
		for e in _emitters:
			e.emitting = false
		_trail_node.emitting = false
		_head_sparks.emitting = false
		_drive_cuts(0.0, false)
		_apply_fade(0.0)
