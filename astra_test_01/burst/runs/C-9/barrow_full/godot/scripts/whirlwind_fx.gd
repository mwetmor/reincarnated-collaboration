extends Node3D
class_name BarrowWhirlwind
# ============================================================================
# C-9 R-C9-128 PORT (drax, 2026-10-01): reincarnated-godot scripts/wwcr_whirlwind.gd, EXACTLY as made, rebound to
# the painted Barrow's characters by tools/port_whirlwind.py -- read that file's docstring for the six binding
# changes; everything else below is the source, comments and all.
# ============================================================================
# ============================================================================
# wwcr_whirlwind.gd — the `whirlwind` archetype VFX binding.
# drax, S2 CLEAN-ROOM mint (WW-AB), 2026-08-24.
#
# Minted from sealed spec § 3.1.12 + the `ww-native-eor1` measured semantics
# block alone. Mint note (math, provenance, clean-room declaration):
#   reincarnated-collaboration/agentic_orchestration/drax/notes/
#     2026-08-24-s2-whirlwind-cleanroom-mint-note.md
#
# ---------------------------------------------------------------------------
# THE ONE IDEA THIS FILE IS BUILT AROUND
# ---------------------------------------------------------------------------
# Measuring the two references side by side turns L-19 from a taste judgement
# into a number. Eye of Reckoning and D3 Whirlwind occupy the SAME footprint
# (~1.9x standing character height). They differ in what fills it:
#
#   EoR  -> the outer radius carries a SURFACE.       (action-DECORATING)
#   D3   -> the outer radius carries CONSEQUENCES.    (action-CAUSED)
#
# So: the only lit, tinted, continuous thing in this effect is a ribbon
# generated FROM THE BLADE'S ACTUAL POSITION. Everything at larger radius is
# discrete, brief, and neutral. That is `TRAIL-BOUNDED` made concrete, and it
# is why this file has no disc, no decal, no radial gradient and no billboard
# sphere in it. The absence is the design.
#
# ---------------------------------------------------------------------------
# NUMBERS — provenance is marked on every one
# ---------------------------------------------------------------------------
#   SPIN_UP_S / SPIN_DOWN_S   MEASURED  (ww-native-eor1.semantics)
#   R_ENGAGE = 1.9 * H_STAND  MEASURED  (ww-native-eor1.semantics; re-measured
#                                        off the native frames this session)
#   R_TRAIL                   MEASURED  off our own rig (wwcr_rig_probe.gd)
#   OMEGA_DEG                 AUTHORED  (cadence coverage is ABSENT corpus-wide;
#                                        measurement from Donor A aliases at
#                                        29.97 fps — mint note § 4.2)
#   WINDUP_S + the whole windup treatment
#                             AUTHORED  (windup coverage is ZERO corpus-wide —
#                                        mint note § 4.1). NOT reference-backed.
#
# ---------------------------------------------------------------------------
# CONSTRAINTS DISCHARGED IN THIS FILE
# ---------------------------------------------------------------------------
#   C-1  every additive/emissive mesh sets SHADOW_CASTING_SETTING_OFF and the
#        pooled contact light sets shadow_enabled = false. Both vendor packs
#        drop a black blob otherwise.
#   C-3  captures are gated on stage albedo 0.085 (see wwcr_stage.gd).
#   C-4  lifecycle class `sustained` with the measured ramp pair.
#   C-5  contact sparks are capped at 0.35 m / 0.12 s so they stay under the
#        occlusion ceiling.
# ============================================================================

# ---------------------------------------------------------------------------
# MEASURED constants
# ---------------------------------------------------------------------------
## Standing character height. king_rig.gd:64 TARGET_HEIGHT — the rig ENFORCES
## this by scaling the body FBX to it. Do NOT substitute the composite AABB
## (2.116 m): that is the cape in its un-skinned bind pose and it would inflate
## R_ENGAGE by 14 %.
const H_STAND := 1.85
## MEASURED: ww-native-eor1 — "radius 150-160 px at 1080p ~ 1.9x standing
## character height, constant". Re-measured off the native frames this session
## (caster ~80 px, field radius ~180 px) => the ratio is on the RADIUS.
const R_ENGAGE_M := 1.9 * H_STAND        # 3.5150 m
## MEASURED off our rig: shoulder_off 0.2141 + arm 0.6308 + blade 1.5150.
const R_TRAIL_M := 2.3598
const R_GRIP_SWEEP_M := 0.8449
## MEASURED: ww-native-eor1.semantics.spin_up_s / spin_down_s, at 60 fps from
## unmodified native pixels. Two INDEPENDENT rates — that is why there are two
## numbers, and why release decays at the release rate instead of retracing.
const SPIN_UP_S := 0.70
const SPIN_DOWN_S := 0.80

# ---------------------------------------------------------------------------
# AUTHORED constants — every one of these is my invention, not a reference
# ---------------------------------------------------------------------------
## AUTHORED. 2.5 rev/s; 2 blade passes per rev => 5 contact ticks/s.
const OMEGA_DEG := 900.0
## AUTHORED. Anticipation window preceding the measured spin-up.
const WINDUP_S := 0.25
## AUTHORED. Blade fraction the ribbon covers: the outer 20 % only. Keeps the
## lit surface a thin annulus arc instead of a filled disc, and keeps luminance
## away from the caster's body.
const TRAIL_INNER_FRAC := 0.80
## AUTHORED. Ribbon history. 10 samples at 60 fps and 900 deg/s spans ~150 deg
## of arc — an ARC, never a closed ring. A closed ring would be a field, so this
## is a TRAIL-BOUNDED guard, not a perf knob.
const TRAIL_SAMPLES := 10
## AUTHORED. Sweep plane and its helical wobble. Chosen to satisfy the
## disjoint-band inequality below.
const SWEEP_Y_M := 1.20
const SWEEP_WOBBLE_M := 0.08
## MEASURED: Hips bone sits at 0.9088 m. The trail band is [1.02, 1.38] m, so
## trail and lower body are DISJOINT BY 0.111 m. This is THE DEFECT TO CORRECT
## ("renders over the caster's lower body") turned into an inequality that can
## be checked instead of admired.
const LOWER_BODY_TOP_M := 0.9088
## AUTHORED, C-5 bounded.
const SPARK_SIZE_M := 0.35
const SPARK_LIFE := 0.12
const SCUFF_LIFE := 0.22
const MAX_SPARKS := 24
const MAX_SCUFFS := 16
## NEVER TINTED. Dust is dust. Neutrality is what stops the outer radius from
## summing into a tinted ring.
##
## ⚑ UNTOUCHED BY 4a, AND DELIBERATELY SO. Charter R-9 rules that `NEVER TINTED`
## constrains HUE and that darkening this colour would be a VALUE change — but
## 4a is a MOTION landing and colour is 4b/4c, judged by Matt's eye at CP#1
## against a MOVING reference (R-3). A motion change and a colour change landing
## together would arrive at his eye as one undifferentiated "it looks better",
## which is not a verdict on either.
const SCUFF_COLOR := Color(0.62, 0.60, 0.56)

# ---------------------------------------------------------------------------
# ⚑ 4a — SPIN-FOLLOWING SCUFFS. AUTHORED, VFX-depth run Wave 1 (charter R-3).
#
# THE DEFECT: a scuff was spawned at a point on the engagement ring and then sat
# there, perfectly still, for its whole 0.22 s life. A blade travelling at
# 900 deg/s throws air; air that does not move is not evidence of a sweep, it is
# a decal that blinks. The outer radius was being spent in quanta — correct —
# but the quanta carried no information about the ROTATION that caused them.
#
# ⚑ AND THE POSITION CHANNEL IS THE ONLY ONE A SCUFF HAS. MEASURED THIS SESSION,
# not recalled from a doc string: a QuadMesh whose material sets
# `billboard_mode = BILLBOARD_ENABLED` with `billboard_keep_scale` at its
# default DISCARDS the instance scale. Two identical quads at scale 1.0 and
# scale 3.0, rendered through a SubViewport in this Godot (4.6.3.stable),
# lit exactly 156 px each — ratio 1.0000, where a kept scale would have given
# 9.0. So `_age_pools`' `mi2.scale` write below has never rendered, on the
# scuffs OR on the sparks. It is LEFT IN PLACE (removing it changes no pixel and
# would muddy this landing's diff) and it is RECORDED HERE, because a line whose
# effect is imagined is exactly what this file's own header warns about: "the
# prose kept porting when the code did not."
#
# THE MOTION: at spawn the scuff takes the sweep's own tangential direction and
# a FRACTION of the blade's tangential speed, then decays exponentially. The
# direction is the derivative of the bearing the spawn used, so its SIGN is tied
# to `_spin` / OMEGA_DEG by construction and cannot disagree with the rotation:
#
#   bearing(s) = ( sin s, 0,  cos s )      <- where the pass threw it
#   d/ds       = ( cos s, 0, -sin s )      <- where the sweep was HEADING
#
# THE ARITHMETIC, at full channel weight, shown so the numbers can be argued
# with instead of admired:
#   omega        = 900 deg/s = 15.7080 rad/s
#   v_blade      = omega * R_ENGAGE = 15.7080 * 3.515 = 55.22 m/s
#   v0           = 0.10 * v_blade                     =  5.522 m/s
#   travel       = v0 * TAU * (1 - exp(-LIFE/TAU))
#                = 5.522 * 0.09 * (1 - exp(-0.22/0.09)) = 0.4538 m   <- CONTINUOUS
#
# ⚑ AND THE RUN MEASURED 0.5036 m, WHICH IS 11 % MORE. THAT IS NOT A DEFECT AND
#   IT IS NOT NOISE — it is the quadrature term, and it reconciles EXACTLY. The
#   loop integrates position at the pre-decay velocity, i.e. a LEFT Riemann sum
#   at dt = 1/60 s, which necessarily overshoots the integral of a decaying
#   exponential. Closed form, 14 steps (0.22 s / (1/60) = 13.2, so 14 partial):
#
#       v0 * dt * (1 - exp(-N*dt/TAU)) / (1 - exp(-dt/TAU))
#         with N = 14  ->  0.503620381752 m
#       selfcheck's runtime measurement  ->  0.503620386123657 m
#
#   Agreement to nine significant figures; the residue is single-precision. The
#   `scuff_travel_predicted_m` key is therefore the CONTINUOUS-TIME value and is
#   labelled as such here, so that nobody later reads an 11 % gap between two
#   selfcheck keys as drift when it is two different (both correct) integrals.
#
#   arc          = 0.5036 / 3.515 = 8.2 deg of the ring
#   ON SCREEN at the judging camera (player_lock k=0.665, 81.9 px/m measured):
#                = 41 px of travel over 14 frames, for a 0.22 m (18 px) quad.
#
# ⚑ WEIGHT-SCALED, NOT CONSTANT. `_w` multiplies the rate, so a scuff thrown
# during spin-up drifts slower than one at full song. That is the coherence the
# ruling actually asks for — "consistent with the rotation" is a statement about
# the CURRENT rotation, not about OMEGA_DEG.
#
# ⚑ THE FALSIFIER, PRE-REGISTERED BEFORE MATT LOOKS: if the dust reads as
# SLIDING — skating outward on ice, detached from the ground — the fraction is
# too high. If it still reads as blinking decals, it is too low. Both are one
# constant, and both are his eye's call at CP#1, not mine.
# ---------------------------------------------------------------------------
const SCUFF_ENTRAIN_FRAC := 0.10
const SCUFF_DRAG_TAU := 0.09

# ---------------------------------------------------------------------------
# ⚑ LAP-2 T-3 — LUMINANCE-DOMINANT APEX, DEEP TAIL, SATURATED BODY.
#   Families FF-01, FF-02, FF-12 + protocol A-1. X-1 #2/#6, X-2 #2/#5.
#
# THE DEFECT, and gandalf's C-1 ruling on how to read it. X-2 named it "cool
# effect on warm scene vs hot effect on cool scene", and the tempting fix — make
# the effect warm — is RULED OUT and I am building the ruled version. The
# reference's arrangement worked because THE EFFECT OWNED THE HIGH-LUMINANCE END
# and the scene owned the low. Teal against maroon-magenta is already
# near-complementary; that is a gift. Our defect is the VALUE ORDERING: we handed
# the luminance to the room. Restore the ordering, keep the hue. D2's Blizzard
# and PoE's Ice Nova both put a WHITE apex on an unambiguously cold effect,
# because apex is a statement about LUMINANCE, not about temperature.
#
# ⚑ THE RAMP IS DERIVED FROM THE ELEMENT'S OWN HUE, NOT PASTED FROM THE SPEC'S
#   TABLE, AND THAT IS A TIER-1 CALL I AM MAKING DELIBERATELY. The spec gives
#   three literal RGB triples for wind. Pasting them would make this file's
#   palette correct for exactly one element and silently wrong for the other four
#   — `set_element` is the Tier-1 recolour seam and the whole point of it is that
#   fire/water/earth come out of the same code.
#
# ⚑ AND CONVERTING THE SPEC'S TRIPLES TO HSV TO GET THE (S, V) PAIRS TURNED UP
#   SOMETHING THE TABLE DOES NOT SAY ABOUT ITSELF: ALL THREE BANDS SIT AT A
#   DIFFERENT HUE FROM THE ELEMENT THEY DESCRIBE.
#
#     element wind = (0.72, 0.95, 0.82)  ->  H 146.09 deg  S 0.242  V 0.950
#     spec apex    = (0.92, 1.00, 0.98)  ->  H 165.00 deg  S 0.080  V 1.000
#     spec body    = (0.24, 0.90, 0.74)  ->  H 165.45 deg  S 0.733  V 0.900
#     spec tail    = (0.05, 0.26, 0.34)  ->  H 196.55 deg  S 0.853  V 0.340
#
#   So the table encodes a ramp that sits ~19 deg cyan-ward of the element and
#   then drops a further ~31 deg toward blue as it dies. My first build held the
#   element hue rigid on the reading that "restore the ordering, KEEP THE HUE"
#   forbade any drift — and it rendered a visibly greener body (b = 0.53 against
#   the table's 0.74). That is not what the spec asked for.
#
#   ⚑ THE RULING SURVIVES THE OFFSETS AND IS NOT WEAKENED BY THEM. "Keep the hue"
#   was ruled AGAINST WARMING — against answering "cool effect on warm scene" by
#   making the effect warm. A 19-50 deg drift inside the teal family is a
#   different thing entirely, and it is what gandalf's OWN TABLE does; refusing
#   it in the ruling's name would have been obeying the sentence while disobeying
#   the artifact it was written about.
#
#   So the offsets are constants MEASURED OUT OF THE SPEC'S TRIPLES rather than
#   invented, applied to whatever hue the element hands in. Wind reproduces the
#   table exactly; fire/water/earth get the same RELATIONSHIP instead of wind's
#   colours. Set the three to zero and you get the rigid-hue reading back — which
#   is one line if Matt's eye at the lap gate wants it.
#
# ⚑ A DARK TAIL IS IMPOSSIBLE UNDER ADDITIVE BLENDING. This is the technical crux
#   and the reason the ribbon is now TWO surfaces. ADD can only lighten; adding a
#   low-saturation teal onto a warm mid-value floor makes a washed neutral, which
#   is precisely why the current arc has neither hue contrast nor value contrast.
#   Both surfaces are rebuilt every frame FROM THE SAME `_hist`, so anchoring and
#   `physical-cause` are untouched — there is still exactly one arc and it is
#   still generated from where the blade actually is.
#
# ⚑ AND THE TWO SURFACES USE OPPOSITE SHADING MODES ON PURPOSE, BECAUSE OF A
#   GODOT FACT THAT DECIDES THIS DESIGN: in `SHADING_MODE_UNSHADED` the fragment
#   output is `vec4(albedo, alpha)` and EMISSION IS DROPPED ENTIRELY. So:
#     * BODY is UNSHADED + MIX. It must NOT emit — it is shadowed air — and
#       unshaded MIX gives exactly lerp(dst, vertex_colour, vertex_alpha), which
#       is the one blend that can put a value BELOW the floor's into the frame.
#     * CORE is PER_PIXEL + ADD with `emission_operator = MULTIPLY`, so
#       EMISSION = white * energy * ALBEDO and the per-vertex apex->body ramp
#       still rides the vertex colour while the ENERGY can exceed 1.0 and reach
#       the HDR range the FILMIC tonemap and the glow pass actually respond to.
#       Under unshaded, `emission_energy_multiplier` on this material would have
#       been a second `mi.scale` — a line whose effect is imagined.
# ---------------------------------------------------------------------------
## Newest fraction of the age range carried by the ADD core. Spec: ~35 %.
const CORE_AGE_FRAC := 0.35
## HDR headroom for the core. Criterion (a) wants the brightest 1 % of effect
## pixels at >= 2.2x the annular scene median; the arc currently measures < 1.0,
## i.e. DIMMER THAN THE ROOM.
const CORE_EMISSION := 5.0
## The body is a MIX surface and its alpha is what lets it darken. It fades in
## over only the OLDEST 12 % of its span — a long alpha fade would hand the tail
## back its transparency and undo the value contrast the whole split exists for.
const BODY_ALPHA_MAX := 0.85
const BODY_FADE_FRAC := 0.12
## Inner-edge alpha as a fraction of the outer edge. The tip moves fastest so it
## glows most (physically right) AND it keeps luminance off the caster's body
## (the mint's motive). The two coincide, which is how you know it is the right
## ramp rather than a cosmetic one.
const CORE_INNER_ALPHA_FRAC := 0.18
const BODY_INNER_ALPHA_FRAC := 0.55
# ---------------------------------------------------------------------------
# ⚑ THE TAPER NEEDED A FLOOR, AND FINDING OUT WHY COST TWO ROUNDS OF TUNING
#   CONSTANTS THAT WERE NEVER THE PROBLEM.
#
# The mint's taper is `inner.lerp(outer, 1.0 - pow(age, 0.75))`, so the width
# fraction IS `age^0.75` — and at the oldest sample age = 0, WHICH MAKES THE
# RIBBON EXACTLY ZERO WIDTH THERE. That was right when the ribbon was one ADD
# surface whose tail only had to fade out. It is fatal now: T-3 asks the tail to
# be a VISIBLE dark band ("deepens through a strong teal into a dark blue-green
# that reads as shadowed moving air"), and a band with no area cannot be seen,
# cannot be measured, and cannot move a percentile.
#
# It presented as criteria (b) and (c) sitting at roughly half their bars while
# (a) and (e) passed with margin — the apex was fine, the dark end simply had no
# pixels to be dark IN. I raised body alpha and re-cut the arc light twice before
# LOOKING AT A CROP OF THE FRAME, which answered it in one glance: the arc ended
# in a bright teal point, not a dark tail. Two rounds of tuning against a
# geometry defect, and the instrument that settled it was my own eye on a 2x
# crop — one call, and it should have been the FIRST one.
#
# So the width tapers to a FLOOR rather than to nothing. The taper still reads as
# speed (a constant width reads as cloth — the mint's reason stands); it just no
# longer erases the band this treatment is about.
# ---------------------------------------------------------------------------
const TAPER_MIN_FRAC := 0.45
## Ramp bands as (S, V), and the per-band HUE OFFSET IN DEGREES from the
## element's own hue. All six numbers are read out of the spec's three wind
## triples (see the block above), never invented — for the wind element this
## reproduces gandalf's table to within float rounding.
const RAMP_APEX_SV := Vector2(0.080000, 1.000000)
const RAMP_BODY_SV := Vector2(0.733333, 0.900000)
const RAMP_TAIL_SV := Vector2(0.852941, 0.160000)
const RAMP_APEX_DH := 18.91
const RAMP_BODY_DH := 19.37
const RAMP_TAIL_DH := 50.47
# ---------------------------------------------------------------------------
# ⚑ ONE SPEC VALUE IS OVERRIDDEN, AND THE REASON IS A MEASUREMENT: THE SPEC'S
#   "DARK" TAIL IS BRIGHTER THAN THE ROOM IT IS SUPPOSED TO BE SHADOW AGAINST.
#
# The table's tail is `Color(0.05, 0.26, 0.34)`, V = 0.34, described as "a dark
# blue-green that reads as SHADOWED MOVING AIR". Its Rec.709 luma is
#
#     0.2126*0.05 + 0.7152*0.26 + 0.0722*0.34 = 0.2213
#
# and the Cathedral's measured non-effect scene median at this pin is 0.178.
# The tail is 24 % BRIGHTER THAN THE FLOOR. Under MIX it therefore LIGHTENS the
# tile it lies on, which is the exact inverse of the treatment's stated purpose.
#
# ⚑ AND IT STAYED INVISIBLE UNTIL I MEASURED THE SIGN OF THE DELTA RATHER THAN
#   ITS MAGNITUDE. Three passes masked the effect region with |dL| and read
#   healthy numbers back — and every pixel in that mask was BRIGHTENING. Signed,
#   the frame said it in one line: FOUR pixels in 1920x1080 got darker. A surface
#   whose entire job is to put a value BELOW the floor's into the frame was
#   putting nothing below the floor at all, and an absolute-value instrument
#   reported that as a working effect. Same shape as the crop that could not see
#   the aim difference: the check ran, and the check was not the check.
#
# So V drops 0.34 -> 0.16 (luma 0.104, i.e. 0.58x the floor rather than 1.24x).
# Hue and saturation are the spec's, untouched. Licensed by the spec's own "drax
# may tune within the criterion", and it is criterion (b) — P95/P20 >= 4.0 —
# that binds: at V = 0.34 that ratio cannot exceed ~2.8 no matter what the apex
# does, because the effect region contains no dark pixels to divide by.
#
# ⚑ NOT A DEFECT IN THE SPEC'S REASONING, AND WORTH SAYING SO. The palette was
#   authored against the ramp's INTERNAL logic — S up, V down as the air ages —
#   which is right, and the hue ruling it serves is right. What the table could
#   not carry without the venue in hand is the Cathedral's MEASURED floor
#   luminance. This constant is therefore VENUE-COUPLED: if the venue changes it
#   must be re-measured, not re-used. Flagged to gandalf; Matt's eye at the lap
#   gate is the arbiter, and reverting is one number.
# ---------------------------------------------------------------------------
## T-3b / FF-12. One arc light riding the ribbon apex. Shadows off (C-1 house
## rule, already in force in this file for every additive surface and the pooled
## contact light).
const ARC_LIGHT_RANGE_M := 2.6
const ARC_LIGHT_ENERGY := 2.2

# ---------------------------------------------------------------------------
# ⚑ THE `TRAIL-BOUNDED` GUARD, AMENDED — NOT DELETED AND NOT BYPASSED.
#
# `set_element()` used to assert `_tinted_nodes.size() == 2`. That count was
# never the property; it was a PROXY for the property, and the property is:
#
#     ⚑ NO TINTED SURFACE MAY BE CONTINUOUS OR PERSISTENT AT OR BEYOND R_ENGAGE.
#
# That clause is what stops this archetype becoming Eye of Reckoning — EoR spends
# its outer radius on a SURFACE (action-decorating); this row spends it on
# CONSEQUENCES (action-caused). The lap-2 spec adds three tinted families that
# are all perfectly compatible with the clause and all fatal to the count, so the
# count has to go and the clause has to be said out loud. A proxy that blocks
# correct work while still admitting the failure it was written against is worse
# than the clause stated outright.
#
# ⚑ FIVE NAMES, EACH WITH ITS JUSTIFICATION, AND THE LIST IS A CEILING RATHER
#   THAN AN EQUALITY. The check is MEMBERSHIP — a sixth tinted family fails
#   loudly, exactly as a third one used to. It does not require all five to
#   exist, because they are landed across several commits and a guard that fails
#   on a treatment not yet built is a guard that gets commented out.
#
# ⚑ AND THE CLAUSE IS ENFORCED, NOT JUST RESTATED. Where it is mechanically
#   checkable it is checked (`_trail_bounded_check`): the two CONTINUOUS families
#   are blade-generated and therefore bounded by R_TRAIL = 2.3598 m, which is
#   asserted to be strictly inside R_ENGAGE = 3.5150 m; every DISCRETE family's
#   lifetime is asserted under a 1.6 s ceiling so "brief" is a number rather than
#   an adjective. Where it is not mechanically checkable it is comment-documented
#   at the family's own construction site.
#
# ⚑ NOT ON THE LIST, AND DELIBERATELY:
#   * `ScuffPuff` — NEVER TINTED. `SCUFF_COLOR` is byte-untouched (R-9's
#     hue-vs-value ruling intact). Neutrality is what stops the outer radius
#     summing into a tinted ring, and it is why the scuffs may live AT R_ENGAGE
#     at all.
#   * `FloorScour` (T-6) — same lane. Neutral, unlit, non-emissive, MIX, and it
#     is the one family that IS persistent at R_ENGAGE. It is admissible for
#     exactly the reason the clause is about TINT: an untinted floor mark is
#     abrasion, and abrasion is a consequence. A tinted one would be a decal.
#   * `ArcLight` / the pooled contact lights — LIGHTS ARE NOT SURFACES. They
#     carry the element colour and always have (the mint's contact light does);
#     they are named here so that the omission is a decision on the record rather
#     than an oversight, and both ride inside R_TRAIL.
# ---------------------------------------------------------------------------
const TINTED_ALLOW_LIST := {
	"TrailRibbonCore":
		"CONTINUOUS. Blade-generated, rebuilt every frame from _hist, bounded by "
		+ "R_TRAIL < R_ENGAGE. The newest ~35% of the arc's age range.",
	"TrailRibbonBody":
		"CONTINUOUS. Same _hist, same bound, same frame. The remaining age range, "
		+ "darkening as it ages. Co-located with the core by construction.",
	"ContactSpark":
		"DISCRETE + BRIEF (0.12 s). Phase-locked to a blade pass, spawned on the "
		+ "target's silhouette EDGE. Quanta are evidence; continuity is a field.",
	"ShedQuantum":
		"DISCRETE + BRIEF (<= 0.90 s). Thrown off the ribbon apex on the seeded "
		+ "gust stream and during FALLING breakup. Never a surface, never a ring.",
	"RecipientResidue":
		"DISCRETE + BRIEF (<= 1.40 s) + ACTOR-ATTACHED. Air still moving where a "
		+ "body was struck. Not a status effect, and gone well inside 2.0 s after "
		+ "the effect ends (R-20e: the reference's ignition cast is unobservable, "
		+ "so nothing here commits the skill to persistent per-victim state).",
}
## "Brief" as a number. Every DISCRETE tinted family's lifetime is asserted under
## this, so the clause's second half cannot rot into an adjective.
const TINTED_DISCRETE_LIFE_CEIL_S := 1.6

# ---------------------------------------------------------------------------
# ⚑ LAP-2 T-4 — LIFECYCLE PHASES + ARRHYTHMIC GUST TEXTURE. FF-11, FF-08.
#   X-2 #3/#9, X-1 #7. "An event, not a loop."
#
# The state machine already existed (WINDUP -> RISING -> SUSTAIN -> FALLING ->
# IDLE) and was VISUALLY UNDIFFERENTIATED — X-2 cites cf_100 and cf_115 as
# identical frames. The arc's measured event CV is 0.10: a metronome.
#
# ---------------------------------------------------------------------------
# ⚑ PARTIAL REFUSAL, T-4 ONSET ACCENT — AND WHAT IS BUILT INSTEAD.
#
# The spec asks for "one-shot pale RING-POP at SWEEP_Y, expanding ~0.6*R_ENGAGE
# -> ~1.05*R_ENGAGE over 0.12-0.18 s, apex colour, ADD."
#
# ⚑ I REFUSE THAT LINE AS WRITTEN, because as written it is a TINTED CONTINUOUS
#   SURFACE AT 1.05 * R_ENGAGE — and the clause T-3 restates two sections
#   earlier, in the same document, says: no tinted surface may be CONTINUOUS or
#   PERSISTENT AT OR BEYOND R_ENGAGE. Not "continuous AND persistent". A brief
#   ring is still a ring. It is also not on the five-name allow-list, and a
#   sixth name invented by the builder to admit his own surface is precisely the
#   dissolution gandalf pre-registered as the veto condition on the amendment.
#   And of all possible shapes, "a lit tinted ring around the caster at the
#   engagement radius" is the LITERAL Eye-of-Reckoning failure this archetype's
#   header says the absence of is the design.
#
# ⚑ WHAT I BUILD INSTEAD IS THE PERCEPTUAL REQUIREMENT, NOT THE MECHANISM. The
#   spec's own "what the player sees" is "the spin STARTS with a pale ring-snap
#   at the caster's waist height" — and a dense one-shot BURST OF DISCRETE QUANTA
#   thrown outward from 0.6*R_ENGAGE to 1.05*R_ENGAGE over the same 0.15 s reads
#   as a ring-snap at 82 px/m while being discrete, brief, and already
#   allow-listed as `ShedQuantum`. Same silhouette, same timing, same colour,
#   same criterion — and it does not require the guard to be widened by the one
#   person the guard exists to constrain.
#
#   Criterion T-4(a) is untouched by the substitution: it measures luminous AREA
#   against the sustain mean over 6-12 frames, which is a statement about the
#   burst, not about whether the burst is one mesh or twenty-eight.
#
#   Flagged for gandalf. If the conductor rules the continuous ring in, it is a
#   sixth allow-list entry plus a re-reading of the clause — and that is his call
#   to make explicitly, not mine to make silently by building it.
# ---------------------------------------------------------------------------
## ⚑ A DEDICATED, SEEDED GENERATOR — NOT THE GLOBAL RNG. Renders must stay
## bit-reproducible AND independent of every other draw consumer in the frame.
## This file already reasons about RNG sequence position (see `_fire_scuff`,
## whose `randf()` is a no-op kept only so the GLOBAL sequence does not shift);
## a gust stream drawing from that same global sequence would make this clip's
## reproducibility hostage to any future line anywhere that draws once.
const RNG_SEED := 20260825
## Poisson event process. Exponential inter-arrivals give CV = 1.0 BY
## CONSTRUCTION — squarely inside the 0.45-1.15 authoring band, and derived
## rather than tuned toward. FF-08's trip-flag (CV < 0.25) cannot fire on it.
const GUST_RATE_MIN := 8.0
const GUST_RATE_MAX := 14.0
const GUST_SURGE_MIN := 1.30
const GUST_SURGE_MAX := 1.70
const GUST_SURGE_TAU := 0.055
const GUST_QUANTA_MIN := 2
const GUST_QUANTA_MAX := 4
## The onset burst. See the refusal block above for why this is quanta and not a
## ring surface.
const ONSET_QUANTA := 32
const ONSET_SIZE_M := 0.62
const ONSET_LIFE := 0.19
const ONSET_R0_FRAC := 0.60
const ONSET_R1_FRAC := 1.05
## Shed quanta (the T-5 family; the pool is built here because T-4's gust stream
## and FALLING breakup are its first two consumers).
## ⚑ W1 F-2 BINDS: `mi.scale` renders NOTHING under BILLBOARD_ENABLED. Size
## spread must therefore come from DISTINCT `QuadMesh.size` VALUES ACROSS THE
## POOL — five classes — or from count. Never from a runtime scale write.
const SHED_SIZE_CLASSES_M: Array[float] = [0.10, 0.16, 0.24, 0.34, 0.46]
const SHED_PER_CLASS := 12
const SHED_LIFE_MIN := 0.35
const SHED_LIFE_MAX := 0.90
const SHED_DRAG_TAU := 0.16
const SHED_ENTRAIN_FRAC := 0.14

# ---------------------------------------------------------------------------
# ⚑ LAP-2 T-2 — ATTACHED WIND-RESIDUE PERSISTENCE. FF-10. X-2 #1, X-1 #1 adjacent.
#   "The effect leaves the caster."
#
# X-2's sentence is the whole treatment: "the reference effect is ON THE VICTIMS,
# the render's is only ON THE CASTER." A struck skeleton keeps a curl of
# disturbed air on it after the arc has gone.
#
# ⚑ THE QUANTA ARE NOT REPARENTED TO THE MOB, AND THAT IS DELIBERATE RATHER THAN
#   LAZY. The spec says "parented to the mob, so it tracks if T-1 moves it", and
#   TRACKING is right — but `wwcr_stage.gd` registers the C-8 census BY ANCESTRY:
#   "everything under this root is AUTHORED, everything else in the viewport is
#   INHERITED." A quantum reparented under a mob would leave the authored subtree
#   and be enumerated as an INHERITED emitter — a HALT condition on galadriel's
#   gate, halting on a node this very file created. So the quanta stay children
#   of the effect and CARRY A HOST REFERENCE instead: each frame the position is
#   recomputed as host.origin + offset + rise. It tracks the flinch exactly as
#   reparenting would, and the census still tells the truth about who authored it.
#
# ⚑ C-2 / R-20e MAGNITUDE DISCIPLINE, AS A HARD BOUND AND NOT A PREFERENCE.
#   This is AIR STILL MOVING WHERE A BODY WAS STRUCK, not a status effect.
#   Nothing here may commit the skill to persistent per-victim state, because the
#   reference clip fades in mid-burn and its ignition cast is UNOBSERVABLE — that
#   identity question is not this lap's to settle. So the ceiling is ASSERTED,
#   not hoped: RESIDUE_LIFE_MAX = 1.40 s, and the last possible spawn is the last
#   contact, which cannot occur below _w = 0.35, i.e. t = 3.12 s on this channel.
#   Extinction by 3.12 + 0.15 + 1.40 = 4.67 s against an effect-end of 3.40 s —
#   1.27 s of margin on the spec's "gone by 2.0 s after the effect ends", and
#   `_trail_bounded_check` asserts the ceiling so a later edit cannot spend that
#   margin without the guard saying so.
# ---------------------------------------------------------------------------
const RESIDUE_PER_CONTACT_MIN := 4
const RESIDUE_PER_CONTACT_MAX := 7
const RESIDUE_LIFE_MIN := 0.70
const RESIDUE_LIFE_MAX := 1.40
## Staggered spawn — they must not all appear on one frame, and (the same
## constant read from the other end) must not extinguish together.
const RESIDUE_STAGGER_MAX := 0.15
const RESIDUE_RISE_MIN_M := 0.30
const RESIDUE_RISE_MAX_M := 0.60
## Size classes. `mi.scale` is a no-op under billboards (W1 F-2), so distinct
## `QuadMesh.size` values are the only channel size variation has.
const RESIDUE_SIZE_CLASSES_M: Array[float] = [0.13, 0.19, 0.26]
const RESIDUE_PER_CLASS := 30
## One burst per FLINCH, not per contact. The stage's T-1 refractory is 0.35 s;
## a burst on every one of the ~5 contacts a mob takes would read as a permanent
## aura, and "permanent per-victim state" is precisely the C-2 line.
const RESIDUE_REFRACTORY_S := 0.35

# ---------------------------------------------------------------------------
# ⚑ LAP-2 T-5 — CROSS-SECTION VARIATION. FF-03. X-1 #8, X-2 #6/#8.
#   "The arc stops being the same shape twice."
#
# X-2's evidence is specific and damning: cf_100 and cf_115 are IDENTICAL. The
# ribbon's width profile repeats exactly every revolution, so the arc is the same
# object rotating rather than air being disturbed.
#
# ⚑ THE NON-REPETITION HAS TO BE BUILT INTO THE FREQUENCIES, NOT SPRINKLED ON AS
#   NOISE, AND THIS IS THE ONE PLACE IN THIS TREATMENT WHERE THE ARITHMETIC
#   ACTUALLY DECIDES THE OUTCOME.
#
# One revolution is TAU radians of `_spin`. A width term `sin(_spin * f)` repeats
# every revolution IF AND ONLY IF f is an integer — so an "obvious" f of 1, 2 or
# 3 would produce a profile that is beautifully varied WITHIN a revolution and
# byte-identical BETWEEN revolutions, which is the exact defect X-2 measured,
# reproduced by a line that looks like the fix for it.
#
# So the two terms use deliberately non-integer, mutually incommensurate f:
#
#     f1 = 0.7333   -> period 1.3636 revolutions;  phase advance per rev
#                      = 0.7333 * TAU = 4.607 rad = -1.676 rad (mod TAU)
#     f2 = 1.6180   -> period 0.6180 revolutions;  phase advance per rev
#                      = 1.6180 * TAU = 10.166 rad = +3.883 rad (mod TAU)
#
# Both advances are large fractions of a full cycle, and their ratio is
# irrational to the precision that matters, so the summed profile does not return
# to itself on any revolution the 3.5 s window contains. Criterion (b) asks for
# >= 8 % RMS difference at matched rotational phase between consecutive
# revolutions; the phase advances above put the two terms most of a cycle apart
# after one revolution, which is far more than 8 % of the amplitude.
#
# Both f are BELOW 2, i.e. slower than two cycles per revolution — the spec's
# "low-frequency noise term". A high-frequency term would make the ribbon ripple
# like a flag, which is a different (and wrong) read.
#
# ⚑ THE INNER FRACTION IS STORED PER SAMPLE, NOT RECOMPUTED AT DRAW TIME. The
#   width a sample had is a fact about WHEN THE BLADE WAS THERE. Recomputing it
#   in `_rebuild_ribbon` from the CURRENT `_spin` would make the whole stored arc
#   breathe in unison every frame — a pulsing crescent, not a varying
#   cross-section — and it would repeat per revolution again for good measure.
#
# ⚑ TRAIL_SAMPLES AND THE OPEN-ARC GUARD ARE UNTOUCHED. Width varies; angular
#   span does not. The arc must stay an arc — a closed ring is a field, and the
#   guard exists for that reason and not for perf.
# ---------------------------------------------------------------------------
const XSEC_F1 := 0.7333
const XSEC_F2 := 1.6180
const XSEC_PH1 := 1.30
const XSEC_PH2 := 2.90
## Amplitude on TRAIL_INNER_FRAC. 0.80 +/- 0.075 spans [0.725, 0.875], i.e. a
## blade-width fraction of [0.275, 0.125] — a 2.2:1 ratio between the widest and
## narrowest cross-section. Clamped so the ribbon can neither invert nor swallow
## the caster's inner radius.
const XSEC_AMP := 0.075
const XSEC_MIN := 0.70
const XSEC_MAX := 0.90

# ---------------------------------------------------------------------------
# ⚑ LAP-2 T-6 — ENVIRONMENT AFTERMATH. FF-06. X-1 #3, X-2 #4. "The floor
#   remembers."
#
# X-1 dim 5's measurement: frame c0208 is IDENTICAL to c0001. A 900 deg/s blade
# sweeps a room for three and a half seconds and the room ends exactly as it
# began. That is the "affecting nothing, LEAVING NOTHING" half of the sentence
# both blind passes converged on.
#
# ⚑ WIND-NATIVE TRANSLATION: ABRASION, NOT BURNING. The reference leaves blood
#   and char because the reference is fire on flesh. Tier-1 identity law says
#   principles transfer and content does not, so what a wind sweep leaves is
#   SCOURED TILE — dust scrubbed off the stone along the path the edge took.
#
# ⚑ AND THIS IS THE ONE FAMILY IN THE FILE THAT IS PERSISTENT AT R_ENGAGE, SO
#   THE GUARD CLAUSE HAS TO BE READ CAREFULLY RATHER THAN WAVED AT. The clause
#   is: no TINTED surface may be continuous or persistent at or beyond R_ENGAGE.
#   The scour is:
#     * NEUTRAL — `SCUFF_COLOR` family, darkened. Byte-untouched hue; R-9's
#       hue-vs-value ruling intact, and value is exactly what a scour is.
#     * UNLIT and NON-EMISSIVE — MIX blend, unshaded, no emission. It cannot
#       contribute to the "lit tinted ring" failure because it emits nothing.
#     * NOT ELEMENT-PARAMETERISED — `set_element` does not touch it, so it does
#       not appear in `_tinted_nodes` and a fire whirlwind scours the same grey.
#   It is therefore admissible for precisely the reason the clause is written
#   about TINT: an untinted floor mark is a CONSEQUENCE, and consequences at the
#   outer radius are what this archetype is supposed to spend it on. A tinted one
#   would be a decal, and a decal is Eye of Reckoning.
#
# ⚑ IT IS ALSO THE ONE FAMILY THAT DELIBERATELY BREAKS "BRIEF". The mint's
#   header says everything at larger radius is "discrete, brief, and neutral".
#   The scour is discrete and neutral and NOT brief — no lifetime expiry inside
#   the capture window, because "the floor remembers" is the entire treatment and
#   a scour that fades is a scour that did not happen. Stated here rather than
#   absorbed, because a future reader finding a non-expiring quad in this file
#   should meet the reason before they meet the code.
#
# ⚑ VALUE ARITHMETIC, done because the first attempt at this in T-3 taught me
#   that "dark" is a claim about a MEASURED FLOOR and not about a number:
#   the Cathedral's non-effect scene median at this pin measures 0.178, and
#   SCUFF_COLOR (0.62, 0.60, 0.56) has luma 0.601 — three times BRIGHTER than
#   the tile. Laid as-is it would be a chalk mark. Scaled by SCOUR_VALUE_MUL =
#   0.34 it lands at luma 0.204... still above. At 0.22 it is 0.132, i.e. 0.74x
#   the floor, and at alpha 0.16 a single pass moves the tile by
#   0.16 * (0.178 - 0.132) = 0.0074 in luma = 1.9/255.
#
#   ⚑ AND THE FIRST BUILD OF THIS TREATMENT MEASURED 3.5/255 AGAINST A 6/255
#   BAR, WITH THE AREA LEG PASSING (5,319 px against 2,500). I had reasoned that
#   "passes accumulate" and left it there. They do accumulate — MIX over MIX
#   compounds as 1-(1-a)^n — but at SCOUR_VALUE_MUL 0.22 and 3 marks per pass the
#   AVERAGE tile in the annulus was covered about twice, and two covers of a mark
#   only 0.046 luma below the tile is 3.5/255. The defect was not the mechanism,
#   it was that I checked the mechanism and not the DEPTH.
#
#   Re-derived, and this time solved rather than hoped: at n overlaps of alpha a,
#   dL = (1 - (1-a)^n) * (floor - mark). Requiring dL >= 6/255 = 0.0235 at the
#   n = 2 the geometry actually delivers, with a = 0.15, gives
#   (floor - mark) >= 0.0235 / 0.2775 = 0.0847, i.e. mark luma <= 0.093. So
#   SCOUR_VALUE_MUL drops 0.22 -> 0.12 (mark luma 0.072, 0.40x the tile), alpha
#   goes 0.12-0.18, and marks per pass 3 -> 4 with the arc spread tightened
#   0.30 -> 0.22 rad so adjacent passes overlap instead of tiling.
#
#   "Slightly darker than tile" is the spec's phrase and 0.40x is more than
#   slightly — but the criterion is the binding instrument and, as in T-3, the
#   phrase was written without the venue's measured floor luminance in hand.
#   VENUE-COUPLED: re-measure if the venue moves. Matt's eye at the lap gate.
# ---------------------------------------------------------------------------
## Marks per blade pass, spread across the swept bearing so a pass lays a short
## ARC of tile rather than a single dot.
const SCOUR_PER_PASS := 4
const SCOUR_ARC_SPREAD_RAD := 0.22
const SCOUR_SIZE_CLASSES_M: Array[float] = [0.52, 0.68, 0.86]
const SCOUR_MAX := 72
const SCOUR_ALPHA_MIN := 0.12
const SCOUR_ALPHA_MAX := 0.18
## Darkening applied to SCUFF_COLOR. See the value arithmetic above — this is the
## factor that puts the mark BELOW the measured tile instead of above it.
const SCOUR_VALUE_MUL := 0.12
## Just clear of the fight tile (`fight_tile_top_offset_m` 0.0081) and of the
## scuff plane (0.03), so it z-fights with neither.
const SCOUR_Y_M := 0.016
## C-9 PORT 11: the venue -- the Barrow's snow luma (film median under him) and the source's required depth
const BARROW_FLOOR_LUMA := 0.934
const SCOUR_DEPTH_LUMA := 0.0847

enum S { IDLE, WINDUP, RISING, SUSTAIN, FALLING }

signal contact(target: Node3D, point: Vector3)

# C-9 PORT: every length, scaled to the character in bind_to (s = H_char / H_STAND)
var _s := 1.0
var R_ENGAGE: float = R_ENGAGE_M
var R_TRAIL: float = R_TRAIL_M
var R_GRIP_SWEEP: float = R_GRIP_SWEEP_M
var SWEEP_Y: float = SWEEP_Y_M
var SWEEP_WOBBLE: float = SWEEP_WOBBLE_M
var LOWER_BODY_TOP: float = LOWER_BODY_TOP_M
var SPARK_SIZE: float = SPARK_SIZE_M
var ARC_LIGHT_RANGE: float = ARC_LIGHT_RANGE_M
var ONSET_SIZE: float = ONSET_SIZE_M
var RESIDUE_RISE_MIN: float = RESIDUE_RISE_MIN_M
var RESIDUE_RISE_MAX: float = RESIDUE_RISE_MAX_M
var SCOUR_Y: float = SCOUR_Y_M
var SHED_SIZE_CLASSES: Array = SHED_SIZE_CLASSES_M.duplicate()
var RESIDUE_SIZE_CLASSES: Array = RESIDUE_SIZE_CLASSES_M.duplicate()
var SCOUR_SIZE_CLASSES: Array = SCOUR_SIZE_CLASSES_M.duplicate()
var _blade_len := 1.5150
var _dt_avg := 1.0 / 60.0
## C-9 PORT 9
var spin_from_clip := false
## C-9 PORT 10
var grip_bone := "weapon_r"
var ribbon_only := false
var blade_head_local := Vector3.ZERO
var _prev_b := 0.0
var _clip_spin_on := false
var _anchor_y := 0.0
var _spin_on := false
var _k: Node = null

var element_color: Color = Color(0.62, 0.80, 1.00)

var _state: int = S.IDLE
var _w := 0.0                  # normalized channel weight, 0..1
var _windup_t := 0.0
var _spin := 0.0               # accumulated blade phase, radians
var _rig: Node3D
var _skel: Skeleton3D
var _blade: Node3D
var _pose
var _targets: Array = []
var _last_phase := 0.0

var _ribbon: MeshInstance3D            # TrailRibbonCore — ADD, per-pixel, emissive
var _ribbon_mesh: ImmediateMesh
var _ribbon_mat: StandardMaterial3D
var _ribbon_body: MeshInstance3D       # TrailRibbonBody — MIX, unshaded, darkening
var _ribbon_body_mesh: ImmediateMesh
var _ribbon_body_mat: StandardMaterial3D
var _arc_light: OmniLight3D            # T-3b / FF-12
var _hist: Array = []          # of {inner:Vector3, outer:Vector3, t:float}
## T-3 ramp, derived from the element's hue in `set_element`.
var _c_apex: Color = Color.WHITE
var _c_body: Color = Color.WHITE
var _c_tail: Color = Color.BLACK
## Driven by the T-4 gust stream; modulates the core emission AND the arc light
## from one place rather than two, so a surge cannot brighten the ribbon without
## brightening what the ribbon casts.
var _gust_boost := 1.0
## T-4 / T-5 state.
var _rng := RandomNumberGenerator.new()
var _shed: Array = []          # of {mi, t, life, vel, onset:bool}
var _shed_mat: StandardMaterial3D
var _scour: Array = []         # T-6. NO lifetime — see the T-6 block.
var _scour_mat: StandardMaterial3D
var _scour_next := 0
var _meas_scour_laid := 0
var _residue: Array = []       # of {mi, t, life, delay, host, off, rise, curl}
var _residue_mat: StandardMaterial3D
var _residue_cool: Dictionary = {}   # host instance id -> refractory countdown
var _meas_residue_alive_max := 0
var _meas_residue_hosts_max := 0
var _gust_next := 0.0          # seconds until the next Poisson event
var _onset_fired := false
## MEASURED AT RUNTIME. The gust stream's realised inter-arrival statistics —
## reported so the CV the render actually exhibits is a number in the manifest
## rather than a property claimed from the fact that the code says "exponential".
var _gust_n := 0
var _gust_sum := 0.0
var _gust_sum_sq := 0.0
var _gust_last_t := 0.0
var _clock := 0.0
var _gust_gate_frames := 0
var _gust_rate_sum := 0.0

var _sparks: Array = []
var _scuffs: Array = []
var _spark_mat: StandardMaterial3D
var _scuff_mat: StandardMaterial3D
var _tinted_nodes: Array = []  # the TRAIL-BOUNDED allow-list; asserted == 2 kinds

# runtime measurement of what the lit surface ACTUALLY occupied
var _logged_seat := false
var _vfx_visible := true
var _meas_y_lo := INF
var _meas_y_hi := -INF
var _meas_r_lo := INF
var _meas_r_hi := -INF
## 4a. Largest distance any scuff quantum actually travelled from its spawn.
var _meas_scuff_travel_max := 0.0
## T-5. Peak simultaneous shed quanta — the census criterion's floor, measured
## in the effect rather than inferred from the pool size.
var _meas_shed_alive_max := 0
## T-5. The width band the running effect actually cut, as inner-fraction.
var _meas_xsec_lo := INF
var _meas_xsec_hi := -INF


# ---------------------------------------------------------------------------
# binding
# ---------------------------------------------------------------------------
func bind_to(rig: Node3D, skel: Skeleton3D, blade: Node3D, h_char: float = H_STAND, knight: Node = null) -> void:
	_rig = rig
	_skel = skel
	_blade = blade
	_k = knight
	_rng.seed = RNG_SEED
	# C-9 PORT 1: every length scaled to this character
	_s = h_char / H_STAND
	for n in ['R_ENGAGE', 'R_TRAIL', 'R_GRIP_SWEEP', 'SWEEP_Y', 'SWEEP_WOBBLE', 'LOWER_BODY_TOP', 'SPARK_SIZE', 'ARC_LIGHT_RANGE', 'ONSET_SIZE', 'RESIDUE_RISE_MIN', 'RESIDUE_RISE_MAX', 'SCOUR_Y']:
		set(n, float(get(n + "_M")) * _s)
	for n in ['SHED_SIZE_CLASSES', 'RESIDUE_SIZE_CLASSES', 'SCOUR_SIZE_CLASSES']:
		var a: Array = []
		for v in (get(n + "_M") as Array):
			a.append(float(v) * _s)
		set(n, a)
	_blade_len = 1.5150 * _s
	_pose = preload("res://scripts/whirlwind_pose.gd").new()
	_pose.name = "WWCRPose"
	skel.add_child(_pose)
	_build_ribbon()
	_build_pools()
	# C-9 PORT 7: drawn after the Barrow's paint post pass, or the paint covers it
	for m in [_ribbon_mat, _ribbon_body_mat, _spark_mat, _scuff_mat, _shed_mat, _scour_mat, _residue_mat]:
		if m != null:
			(m as Material).render_priority = PaintStack.AFTER_POST_PRIORITY
	set_element(element_color)


## Hide every VFX layer while leaving the POSE and the ROTATION running.
##
## This is the control condition for the occlusion gate. Comparing "effect on"
## against "no whirlwind at all" measures the caster's own pose and rotation
## and reports it as occlusion — the first run of the gate scored 7.65 % on a
## frame where the effect was entirely off, which is how the flaw surfaced.
## The only valid baseline is: same pose, same rotation, no VFX.
func set_vfx_visible(v: bool) -> void:
	if _ribbon:
		_ribbon.visible = v
	if _ribbon_body:
		_ribbon_body.visible = v
	if _arc_light:
		# ⚑ A LIGHT MUST BE DARKENED, NOT JUST HIDDEN — `visible=false` on an
		#   OmniLight3D does stop it lighting, but the energy is zeroed too so the
		#   control cannot be re-lit by a later `_rebuild_ribbon` early-return
		#   path that touches visibility without touching energy.
		_arc_light.visible = false
		_arc_light.light_energy = 0.0
	for s in _scour:
		if not v:
			(s["mi"] as MeshInstance3D).visible = false
	for s in _residue:
		if not v:
			(s["mi"] as MeshInstance3D).visible = false
			s["t"] = 0.0
	for s in _shed:
		if not v:
			(s["mi"] as MeshInstance3D).visible = false
			s["t"] = 0.0
	for s in _sparks:
		if not v:
			(s["mi"] as MeshInstance3D).visible = false
			(s["light"] as OmniLight3D).light_energy = 0.0
	for s in _scuffs:
		if not v:
			(s["mi"] as MeshInstance3D).visible = false
	_vfx_visible = v


func register_target(n: Node3D) -> void:
	if n != null and not _targets.has(n):
		_targets.append(n)


func begin() -> void:
	if _state == S.IDLE:
		_state = S.WINDUP
		_windup_t = 0.0


func end() -> void:
	if _state != S.IDLE:
		_state = S.FALLING


func channel_weight() -> float:
	return _w


func state_name() -> String:
	return ["IDLE", "WINDUP", "RISING", "SUSTAIN", "FALLING"][_state]


# ---------------------------------------------------------------------------
# TIER-1 element parameterization.
#
# ⚑ AMENDED AT LAP-2 T-3. This used to assert `_tinted_nodes.size() == 2`. The
#   count was a PROXY; the clause is the guard. See the TINTED_ALLOW_LIST block.
#   The three bands of the T-3 ramp are DERIVED from the hue handed in here, so
#   fire/water/earth get the same value ordering wind does rather than a palette
#   hard-coded for one element.
# ---------------------------------------------------------------------------
func set_element(c: Color) -> void:
	element_color = c
	# T-3: apex / body / tail as (S, V) + a per-band hue offset, applied to the
	# ELEMENT'S OWN HUE. `fposmod` because a band can push past 1.0 and Godot's
	# from_hsv does not wrap for you.
	var hue := c.h
	_c_apex = Color.from_hsv(fposmod(hue + RAMP_APEX_DH / 360.0, 1.0),
		RAMP_APEX_SV.x, RAMP_APEX_SV.y)
	_c_body = Color.from_hsv(fposmod(hue + RAMP_BODY_DH / 360.0, 1.0),
		RAMP_BODY_SV.x, RAMP_BODY_SV.y)
	_c_tail = Color.from_hsv(fposmod(hue + RAMP_TAIL_DH / 360.0, 1.0),
		RAMP_TAIL_SV.x, RAMP_TAIL_SV.y)
	_tinted_nodes.clear()
	if _ribbon_mat:
		# Albedo WHITE so the per-vertex ramp passes through unmultiplied; the
		# tint lives in the vertex colours, which is what lets one surface carry
		# a gradient at all. Emission stays WHITE because EMISSION_OP_MULTIPLY
		# multiplies it BY the albedo — writing the element colour into both
		# would square the tint and desaturate the apex toward the hue's corner.
		_ribbon_mat.albedo_color = Color.WHITE
		_tinted_nodes.append("TrailRibbonCore")
	if _ribbon_body_mat:
		_ribbon_body_mat.albedo_color = Color.WHITE
		_tinted_nodes.append("TrailRibbonBody")
	if _spark_mat:
		_spark_mat.albedo_color = c
		_spark_mat.emission = c
		_tinted_nodes.append("ContactSpark")
	if _residue_mat:
		# Apex colour: this is air off the LEADING EDGE that struck the body, so
		# it carries the leading edge's register — pale and fast, not the pastel.
		_residue_mat.albedo_color = _c_apex
		_tinted_nodes.append("RecipientResidue")
	if _shed_mat:
		# ⚑ APEX COLOUR, NOT ELEMENT COLOUR. Shed air came off the leading edge,
		#   so it carries the leading edge's value — pale, near-white. Tinting it
		#   the pastel element colour would put the DIMMEST register of the ramp
		#   on the family that is furthest from the caster, which is the value
		#   ordering T-3 exists to undo, one lane along.
		_shed_mat.albedo_color = _c_apex
		_tinted_nodes.append("ShedQuantum")
	for s in _sparks:
		var lt: OmniLight3D = s["light"]
		lt.light_color = c
	# Scuff puffs are NOT touched. Deliberately. See SCUFF_COLOR.
	_trail_bounded_check()


# ---------------------------------------------------------------------------
# ⚑ THE `TRAIL-BOUNDED` CLAUSE, ENFORCED. Not the count it used to stand in for.
#
#     NO TINTED SURFACE MAY BE CONTINUOUS OR PERSISTENT AT OR BEYOND R_ENGAGE.
#
# Three legs, and each one fails loudly:
#   (1) MEMBERSHIP — every tinted family must be on the named allow-list. A
#       sixth family trips this exactly as a third one used to trip the count.
#       The list is a CEILING, not an equality: families land across several
#       commits, and a guard that fails on a treatment not yet built is a guard
#       that gets commented out.
#   (2) CONTINUITY — the two continuous families are blade-generated, so their
#       radius is R_TRAIL by construction. Asserted strictly inside R_ENGAGE.
#   (3) BRIEFNESS — every discrete tinted family's lifetime is under a stated
#       ceiling, so "brief" is a number rather than an adjective.
# ---------------------------------------------------------------------------
func _trail_bounded_check() -> void:
	for nm in _tinted_nodes:
		assert(TINTED_ALLOW_LIST.has(nm),
			"TRAIL-BOUNDED violated (membership): '%s' is a tinted surface that is " % nm
			+ "not on the named allow-list %s. " % str(TINTED_ALLOW_LIST.keys())
			+ "The clause: no tinted surface may be CONTINUOUS or PERSISTENT at or "
			+ "beyond R_ENGAGE. Add it to the list WITH its justification, or keep "
			+ "it neutral like SCUFF_COLOR — do not delete this check.")
	# (2) the continuous families are bounded by the blade, not by an authored radius
	assert(R_TRAIL < R_ENGAGE,
		"TRAIL-BOUNDED violated (continuity): the continuous tinted surfaces are "
		+ "blade-generated and therefore reach R_TRAIL = %.4f m, which is not " % R_TRAIL
		+ "inside R_ENGAGE = %.4f m." % R_ENGAGE)
	# (3) every discrete tinted family is brief, by the number and not by adjective
	assert(SPARK_LIFE <= TINTED_DISCRETE_LIFE_CEIL_S,
		"TRAIL-BOUNDED violated (briefness): ContactSpark life %.3f s exceeds the "
		% SPARK_LIFE + "%.3f s ceiling." % TINTED_DISCRETE_LIFE_CEIL_S)
	assert(RESIDUE_LIFE_MAX <= TINTED_DISCRETE_LIFE_CEIL_S,
		"TRAIL-BOUNDED violated (briefness): RecipientResidue life %.3f s exceeds "
		% RESIDUE_LIFE_MAX + "the %.3f s ceiling. This family is ACTOR-ATTACHED, "
		% TINTED_DISCRETE_LIFE_CEIL_S
		+ "so a long lifetime is not a slow fade — it is per-victim STATE, which "
		+ "R-20e forbids this lap from committing the skill to.")
	assert(SHED_LIFE_MAX <= TINTED_DISCRETE_LIFE_CEIL_S,
		"TRAIL-BOUNDED violated (briefness): ShedQuantum life %.3f s exceeds the "
		% SHED_LIFE_MAX + "%.3f s ceiling." % TINTED_DISCRETE_LIFE_CEIL_S)


# ---------------------------------------------------------------------------
# per-frame
# ---------------------------------------------------------------------------
func _process(delta: float) -> void:
	_advance_state(delta)
	if _pose:
		_pose.sweep_w = 0.0 if (spin_from_clip or ribbon_only) else clampf(_w * 1.6, 0.0, 1.0)
		_pose.windup_w = 0.0 if (spin_from_clip or ribbon_only) else _windup_t

	# THE CHARACTER ROTATES. The payload is the character's own weapons —
	# spec § 3.1.12. The VFX is downstream of the body, never a substitute
	# for it.
	if spin_from_clip:
		pass                                 # C-9 PORT 9: _spin is read off the weapon head in _seat_proxy
	elif _rig and _w > 0.0:
		_spin += deg_to_rad(OMEGA_DEG) * _w * delta
	if not spin_from_clip:
		_apply_spin()

	_clock += delta
	_dt_avg = lerpf(_dt_avg, clampf(delta, 1.0 / 240.0, 0.1), 0.1) if delta > 0.0 else _dt_avg
	_seat_proxy()
	_reseat_blade()
	_sample_blade(delta)
	_tick_gusts(delta)
	_tick_residue(delta)
	_rebuild_ribbon()
	_arc_to_pool()
	_tick_contacts(delta)
	_age_pools(delta)


func _physics_process(_dt: float) -> void:
	# C-9 PORT 3: knight.gd re-seats his rig every physics frame; this node runs after it (process_physics_priority)
	if not spin_from_clip:
		_apply_spin()


func _apply_spin() -> void:
	if _rig == null or ribbon_only:
		return
	var channel := _state != S.IDLE
	if channel and not _spin_on:
		# the spin starts from where he faces, so the source's bearing (sin spin, cos spin) is his
		_spin_on = true
		_spin = float(_k.get("_yaw_cur")) if _k != null else _rig.global_transform.basis.get_euler().y
		var fl = _k.get("_foot_lock") if _k != null else null
		if fl != null:
			fl.release_all()
			fl.enabled = false
	elif not channel and _spin_on:
		# hand the heading back: his own yaw smoothing turns him to his facing from where the spin left him
		_spin_on = false
		if _k != null:
			_k.set("_yaw_cur", _spin)
			var fl2 = _k.get("_foot_lock")
			if fl2 != null:
				fl2.enabled = true
		return
	if not channel:
		return
	var gx := _rig.global_transform
	_rig.global_transform = Transform3D(Basis(Vector3.UP, _spin).scaled(gx.basis.get_scale()), gx.origin)


func _advance_state(delta: float) -> void:
	match _state:
		S.WINDUP:
			_windup_t += delta / WINDUP_S
			if _windup_t >= 1.0:
				_windup_t = 1.0
				_state = S.RISING
		S.RISING:
			# ⚑ T-4 ONSET. Fired on the FIRST RISING frame — the spec's "the spin
			#   STARTS with a pale ring-snap". Once, latched, so a re-entry to
			#   RISING (which this state machine cannot currently do, but a future
			#   recast structure might) cannot stutter it.
			if not _onset_fired:
				_onset_fired = true
				_fire_onset()
			_windup_t = maxf(0.0, _windup_t - delta / 0.18)
			# MEASURED ramp, against the scaled process clock so slow-motion and
			# pause affect the effect exactly as they affect the game.
			_w += delta / SPIN_UP_S
			if _w >= 1.0:
				_w = 1.0
				_state = S.SUSTAIN
		S.FALLING:
			_w -= delta / SPIN_DOWN_S
			if _w <= 0.0:
				_w = 0.0
				_state = S.IDLE
				# ⚑ T-4 DECAY. The ribbon must NOT switch off. Whatever history is
				#   still standing on the last frame becomes drifting quanta, so
				#   the arc's final act is fragmentation rather than a cliff — and
				#   the last quanta outlive the ribbon's final frame by up to
				#   SHED_LIFE_MAX. Criterion (c) measures exactly this.
				_shed_remaining_history()
		_:
			pass


# ---------------------------------------------------------------------------
# Layer A — the weapon-trail highlight.
#
# The ribbon is NOT authored at a radius. It is rebuilt every frame from where
# the blade actually is, so a tinted surface physically cannot drift away from
# its cause. That is the cheapest possible enforcement of `physical-cause`, and
# it survives future animation changes for free.
#
# Note what is deliberately NOT driven by the channel weight: the RADIUS. The
# radius comes from the bone. A radius that grew with the ramp would be an
# expanding surface — the exact EoR failure, and the single most natural bug to
# introduce here.
# ---------------------------------------------------------------------------
func _sample_blade(_delta: float) -> void:
	if _blade == null or _w <= 0.0:
		if _w <= 0.0:
			_hist.clear()
		return
	var seg := _blade_segment()
	var grip: Vector3 = seg[0]
	var tip: Vector3 = seg[1]
	# ⚑ T-5. The cross-section this sample was cut at, keyed on `_spin` — see the
	#   T-5 block for why the frequencies are non-integer and why the value is
	#   STORED rather than recomputed at draw time.
	var xf: float = _xsec_inner_frac()
	var inner: Vector3 = grip.lerp(tip, xf)
	# AUTHORED helical wobble — the blade of a real sweep does not stay level.
	# Gentle undulation, NOT a corkscrew. At sin(2*spin) with 900 deg/s the
	# wobble completed a full cycle inside the 10-sample history and the ribbon
	# read as a broad scarf rather than a blade arc — the apparent thickness was
	# vertical wobble, not ribbon width. One slow cycle per revolution instead.
	var wob := sin(_spin) * SWEEP_WOBBLE * _w
	inner.y += wob
	tip.y += wob
	# RIGID PLAYER-ANCHORING, and this is the line that implements it.
	# History is stored RELATIVE TO THE CASTER'S POSITION, then re-anchored to
	# the caster's CURRENT position at draw time. Store it in world space
	# instead and a moving caster leaves old samples behind — which is exactly
	# the "elastic trail" the anchor forbids ("rigidly player-centred; no lag,
	# no elastic trail, no lean into movement vector"). Rotation is NOT
	# factored out, because the arc sweeping round the caster is the effect.
	var anchor := _rig.global_transform.origin
	_hist.push_back({"inner": inner - anchor, "outer": tip - anchor, "xf": xf})
	_meas_xsec_lo = minf(_meas_xsec_lo, xf)
	_meas_xsec_hi = maxf(_meas_xsec_hi, xf)
	# MEASURED AT RUNTIME, not asserted: the actual Y band the lit surface
	# occupies, and its actual radius. The mint note's disjoint-band claim is
	# only worth something if the running effect is checked against it.
	for y in [inner.y, tip.y]:
		_meas_y_lo = minf(_meas_y_lo, y - anchor.y)
		_meas_y_hi = maxf(_meas_y_hi, y - anchor.y)
	var rr := Vector2(tip.x - anchor.x, tip.z - anchor.z).length()
	_meas_r_lo = minf(_meas_r_lo, rr)
	_meas_r_hi = maxf(_meas_r_hi, rr)
	# ⚑ T-4 DECAY. The history window SHRINKS during FALLING, and each sample it
	#   drops is converted into a drifting quantum instead of vanishing. That is
	#   what makes the arc break into fragments rather than dim uniformly — and it
	#   is why criterion (c)'s "no single frame-to-frame drop > 35 %" is
	#   achievable at all: a ribbon that is still 10 samples long at _w = 0.02 and
	#   then gone is a cliff no alpha ramp can soften.
	var win := _trail_window()
	while _hist.size() > win:
		var dropped: Dictionary = _hist.pop_front()
		if _state == S.FALLING:
			_shed_from_sample(dropped, anchor)


## The width term. Two incommensurate low-frequency sinusoids in `_spin`, summed
## and clamped. Weight-scaled so a spin-up arc is not already at full variation.
func _xsec_inner_frac() -> float:
	var v: float = 0.6 * sin(_spin * XSEC_F1 + XSEC_PH1) \
		+ 0.4 * sin(_spin * XSEC_F2 + XSEC_PH2)
	return clampf(TRAIL_INNER_FRAC + XSEC_AMP * v * _w, XSEC_MIN, XSEC_MAX)


var _b_grip := -1
var _b_hand := -1
var _b_fore := -1


func _seat_proxy() -> void:
	"""C-9 PORT 4: the blade proxy sits on the rig's own weapon mount (weapon_r, else RightHand), its long axis
	along forearm -> hand -- the weapon as the clip holds it, before the source's _reseat_blade levels it."""
	if _skel == null or _blade == null:
		return
	if _b_hand < 0:
		var side := "Left" if grip_bone.ends_with("_l") else "Right"
		for i in _skel.get_bone_count():
			var nm := String(_skel.get_bone_name(i))
			if nm == grip_bone:
				_b_grip = i
			elif nm.ends_with(side + "Hand"):
				_b_hand = i
			elif nm.ends_with(side + "ForeArm"):
				_b_fore = i
		if _b_grip < 0:
			_b_grip = _b_hand
	var sx := _skel.global_transform
	if spin_from_clip and blade_head_local != Vector3.ZERO:
		# C-9 PORT 9: the real weapon -- the grip at weapon_r, the tip at its head -- and _spin the head's bearing
		var wx := sx * _skel.get_bone_global_pose(_b_grip)
		var g0 := wx.origin
		var hd := wx * blade_head_local
		var ax9 := hd - g0
		_blade_len = ax9.length()
		ax9 = ax9.normalized()
		var side9 := ax9.cross(Vector3.UP)
		if side9.length() < 1e-4:
			side9 = Vector3.RIGHT
		side9 = side9.normalized()
		_blade.global_transform = Transform3D(Basis(side9, ax9, side9.cross(ax9).normalized()).orthonormalized(), g0)
		var c9 := _rig.global_transform.origin
		_anchor_y = c9.y
		var b := atan2(hd.x - c9.x, hd.z - c9.z)
		var live := _state != S.IDLE
		if live and not _clip_spin_on:
			_spin = b
		elif live:
			_spin += wrapf(b - _prev_b, -PI, PI)
		_clip_spin_on = live
		_prev_b = b
		return
	var grip := sx * _skel.get_bone_global_pose(_b_grip).origin
	var hand := sx * _skel.get_bone_global_pose(_b_hand).origin
	var fore := sx * _skel.get_bone_global_pose(_b_fore).origin
	var ax := (hand - fore)
	if ax.length() < 1e-5:
		ax = Vector3.UP
	ax = ax.normalized()
	var side := ax.cross(Vector3.UP)
	if side.length() < 1e-4:
		side = Vector3.RIGHT
	side = side.normalized()
	_blade.global_transform = Transform3D(Basis(side, ax, side.cross(ax).normalized()).orthonormalized(), grip)
	_anchor_y = _rig.global_transform.origin.y


func _blade_segment() -> Array:
	var gx := _blade.global_transform
	var grip := gx.origin
	# The Synty greatsword's long axis was probed as its local +Y (grip -> tip,
	# 1.5150 m). Measured, not assumed.
	var axis := (gx.basis * Vector3.UP).normalized()
	var tip := grip + axis * _blade_len
	return [grip, tip]


# Re-seat the blade into the horizontal sweep plane.
#
# king_rig seats the sword in the RIGHT-HAND BONE's local frame at a held-guard
# pitch, which is correct for walking around and wrong for a whirlwind: it
# leaves the blade near-vertical and the trail reads as a sail rather than a
# sweep. So during the channel the blade's long axis is driven RADIALLY OUTWARD
# and LEVEL, blended in by the channel weight so the transition is not a pop.
#
# The grip stays exactly where the hand is. The blade is re-oriented, never
# re-positioned — so the trail is still generated from a weapon that is still
# in the caster's hands, and `physical-cause` survives the override.
func _reseat_blade() -> void:
	if spin_from_clip:
		return                               # C-9 PORT 9: the clip holds the real weapon; nothing re-seats it
	if _blade == null or _w <= 0.001:
		return
	var gx := _blade.global_transform
	var grip := gx.origin
	var centre := _rig.global_transform.origin
	var radial := Vector3(grip.x - centre.x, 0.0, grip.z - centre.z)
	if radial.length() < 0.01:
		radial = _rig.global_transform.basis * Vector3(0, 0, 1)
	radial = radial.normalized()
	var up := Vector3.UP
	# NOTE the cross order. `up.cross(radial)` yields a LEFT-handed basis
	# (det = -1), and Basis.slerp on a det=-1 matrix produces garbage — it sent
	# the blade above the caster's head at r = 0.76 m in the first run. Caught
	# by the runtime band measurement in selfcheck(), which is exactly what that
	# measurement is for.
	var side := radial.cross(up).normalized()
	# columns: X = side, Y = long axis (radial, level), Z = up
	var target := Basis(side, radial, up).orthonormalized()
	var from := gx.basis.orthonormalized()
	_blade.global_transform = Transform3D(
		from.slerp(target, clampf(_w, 0.0, 1.0)).scaled(gx.basis.get_scale()), grip)
	if not _logged_seat and _w > 0.99:
		_logged_seat = true
		var seg := _blade_segment()
		print("[wwcr-diag] w=%.2f grip=%s tip=%s r_grip=%.3f r_tip=%.3f det=%.3f" % [
			_w, str(seg[0]), str(seg[1]),
			Vector2(seg[0].x - centre.x, seg[0].z - centre.z).length(),
			Vector2(seg[1].x - centre.x, seg[1].z - centre.z).length(),
			target.determinant()])


func _build_ribbon() -> void:
	# ---- CORE: ADD, PER_PIXEL, emissive. The newest ~35 % of the age range. ----
	_ribbon_mesh = ImmediateMesh.new()
	_ribbon = MeshInstance3D.new()
	_ribbon.name = "TrailRibbonCore"
	_ribbon.mesh = _ribbon_mesh
	# C-1: both vendor packs ship shadow-casting VFX geometry and drop a hard
	# black blob on the floor beside the effect. Everything additive we author
	# turns it off at mount time.
	_ribbon.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_ribbon_mat = StandardMaterial3D.new()
	# ⚑ PER_PIXEL, NOT UNSHADED, AND THE CHANGE IS THE POINT. Unshaded outputs
	#   vec4(albedo, alpha) and DROPS EMISSION — under it, this material's
	#   `emission_energy_multiplier = 2.0` was rendering nothing, which is the
	#   same class of imagined line as the `mi.scale` write in the 4a block. With
	#   PER_PIXEL + EMISSION_OP_MULTIPLY the emission is `white * energy * ALBEDO`,
	#   so the per-vertex apex->body ramp still rides the vertex colour AND the
	#   energy can exceed 1.0 into the HDR range the FILMIC tonemap and the glow
	#   pass respond to. That headroom is what criterion (a) is asking for.
	_ribbon_mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	_ribbon_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	_ribbon_mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_ribbon_mat.vertex_color_use_as_albedo = true
	# ⚑ MEASURED, NOT ASSUMED — see the sRGB block at TAPER_MIN_FRAC.
	_ribbon_mat.vertex_color_is_srgb = true
	_ribbon_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	# Depth test STAYS ON. The blade passing in front of the caster SHOULD be in
	# front of the caster — that is a physical fact, not the occlusion defect.
	# The defect is a surface covering the caster, and there is no such surface.
	_ribbon_mat.no_depth_test = false
	_ribbon_mat.disable_receive_shadows = true
	_ribbon_mat.disable_ambient_light = true
	_ribbon_mat.roughness = 1.0
	_ribbon_mat.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
	_ribbon_mat.emission_enabled = true
	_ribbon_mat.emission = Color.WHITE
	_ribbon_mat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
	_ribbon_mat.emission_energy_multiplier = CORE_EMISSION
	_ribbon.material_override = _ribbon_mat
	add_child(_ribbon)

	# ---- BODY: MIX, UNSHADED, darkening. The remaining age range. ------------
	_ribbon_body_mesh = ImmediateMesh.new()
	_ribbon_body = MeshInstance3D.new()
	_ribbon_body.name = "TrailRibbonBody"
	_ribbon_body.mesh = _ribbon_body_mesh
	_ribbon_body.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	# ⚑ RENDERED BEFORE THE CORE. Two co-located transparent surfaces are sorted
	#   by the renderer, and a MIX surface drawn AFTER an ADD one would overwrite
	#   the apex it is supposed to sit behind. Negative priority draws first.
	_ribbon_body.sorting_offset = -0.01
	_ribbon_body_mat = StandardMaterial3D.new()
	# ⚑ UNSHADED IS CORRECT HERE FOR THE SAME REASON IT WAS WRONG ABOVE: this
	#   surface MUST NOT EMIT. It is shadowed air. Unshaded MIX gives exactly
	#   lerp(dst, vertex_colour, vertex_alpha) — the one blend in this file that
	#   can put a value BELOW the floor's into the frame, which is the whole
	#   reason the ribbon was split.
	_ribbon_body_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_ribbon_body_mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	_ribbon_body_mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_ribbon_body_mat.vertex_color_use_as_albedo = true
	_ribbon_body_mat.vertex_color_is_srgb = true
	_ribbon_body_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_ribbon_body_mat.no_depth_test = false
	_ribbon_body_mat.disable_receive_shadows = true
	_ribbon_body.material_override = _ribbon_body_mat
	add_child(_ribbon_body)

	# ---- T-3b / FF-12: one arc light riding the apex ------------------------
	# ⚑ A LIGHT, NOT A SURFACE — so it is not on the tinted allow-list, and the
	#   omission is a decision on the record (see the allow-list block). It rides
	#   the NEWEST history sample, i.e. inside R_TRAIL, and it is what criterion
	#   (e) measures: the floor and the near flank of whichever skeleton the edge
	#   is passing must brighten as it goes by. Shadows off — C-1.
	_arc_light = OmniLight3D.new()
	_arc_light.name = "ArcLight"
	_arc_light.omni_range = ARC_LIGHT_RANGE
	_arc_light.light_energy = 0.0
	_arc_light.shadow_enabled = false
	_arc_light.visible = false
	add_child(_arc_light)


# ---------------------------------------------------------------------------
# ⚑ T-3. TWO SURFACES, ONE `_hist`, ONE FRAME.
#
# The split is a RENDERING split, not a geometric one. Both strips walk the same
# history array, apply the same taper and the same re-anchor, and are cut at one
# index — so there is still exactly ONE arc, it is still generated from where the
# blade actually is, and `physical-cause` and the rigid player-anchoring survive
# untouched. What differs is only which blend mode each age band is drawn with,
# because ADD cannot go dark and MIX cannot go bright.
#
# The two bands OVERLAP BY TWO SAMPLES at the cut. A single shared vertex row
# would leave a visible seam where an ADD strip ends and a MIX strip begins; two
# rows of overlap let the core's alpha fall to near-zero across the same span the
# body's is rising, so the handover happens inside a gradient instead of on an
# edge.
# ---------------------------------------------------------------------------
func _rebuild_ribbon() -> void:
	_ribbon_mesh.clear_surfaces()
	_ribbon_body_mesh.clear_surfaces()
	if _arc_light:
		_arc_light.visible = false
		_arc_light.light_energy = 0.0
	if not _vfx_visible or _hist.size() < 2 or _w <= 0.001:
		return
	var n := _hist.size()
	# re-anchor every stored sample to where the caster is NOW (see _sample_blade)
	var anchor := _rig.global_transform.origin
	var core_start := 1.0 - CORE_AGE_FRAC          # age at which the core begins
	# Index of the cut, and the two-sample overlap around it.
	var cut := int(floor(core_start * float(n - 1)))
	var body_hi := mini(n - 1, cut + 1)
	var core_lo := maxi(0, cut)

	# ---- BODY strip: oldest .. cut+1 ----------------------------------------
	if body_hi >= 1:
		_ribbon_body_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
		for i in range(body_hi + 1):
			var age := float(i) / float(n - 1)
			# normalized position INSIDE the body band: 0 = oldest, 1 = at the cut
			var tb: float = (age / core_start) if core_start > 0.0 else 1.0
			tb = clampf(tb, 0.0, 1.0)
			# ⚑ DARKENING, NOT ONLY ALPHA-FADING. The colour walks tail -> body as
			#   the sample gets NEWER, so the oldest air is the darkest thing in
			#   the effect region. That is what criterion (b)'s P95/P20 >= 4.0 is
			#   measuring, and an alpha-only fade cannot produce it.
			# ⚑ pow(tb, 1.8), NOT a linear lerp. Linear put the true tail colour on
			#   the single OLDEST sample — which is also the NARROWEST one — so the
			#   dark band existed on 63 pixels of a 1920x1080 frame. The exponent
			#   holds the tail colour across the oldest THIRD of the body span,
			#   which is what gives criterion (b)'s P20 something to be low ON.
			var col := _c_tail.lerp(_c_body, pow(tb, 1.8))
			# The alpha fade is deliberately SHORT (oldest 12 % only). A long fade
			# would hand the tail back its transparency and undo the value
			# contrast the split exists for.
			var fade: float = clampf(tb / BODY_FADE_FRAC, 0.0, 1.0)
			var a := BODY_ALPHA_MAX * _w * fade
			var h: Dictionary = _hist[i]
			var inner: Vector3 = h["inner"]
			var outer: Vector3 = h["outer"]
			# TAPER, WITH A FLOOR (see TAPER_MIN_FRAC): older samples narrow toward
			# the tip path, so the ribbon reads as a blade trail rather than a
			# crescent of constant width — but they no longer collapse to zero, or
			# the dark tail this surface exists to draw would have no area.
			var wf: float = TAPER_MIN_FRAC + (1.0 - TAPER_MIN_FRAC) * pow(age, 0.75)
			inner = inner.lerp(outer, 1.0 - wf)
			_ribbon_body_mesh.surface_set_color(
				Color(col.r, col.g, col.b, a * BODY_INNER_ALPHA_FRAC))
			_ribbon_body_mesh.surface_add_vertex(to_local(anchor + inner))
			_ribbon_body_mesh.surface_set_color(Color(col.r, col.g, col.b, a))
			_ribbon_body_mesh.surface_add_vertex(to_local(anchor + outer))
		_ribbon_body_mesh.surface_end()

	# ---- CORE strip: cut .. newest ------------------------------------------
	if core_lo <= n - 2:
		_ribbon_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
		for i in range(core_lo, n):
			var age2 := float(i) / float(n - 1)
			# normalized position INSIDE the core band: 0 = at the cut, 1 = newest
			var tc: float = (age2 - core_start) / maxf(1.0e-6, 1.0 - core_start)
			tc = clampf(tc, 0.0, 1.0)
			var col2 := _c_body.lerp(_c_apex, pow(tc, 0.7))
			# Broad rather than spiky: the apex is a BAND at the leading edge, not
			# a single hot vertex. Criterion (d) wants the intensity peak inside
			# the leading 25 % of the angular extent on >= 80 % of frames, and a
			# one-vertex spike is far more fragile to the sampler than a band is.
			var a2 := pow(tc, 0.8) * _w
			var h2: Dictionary = _hist[i]
			var inner2: Vector3 = h2["inner"]
			var outer2: Vector3 = h2["outer"]
			var wf2: float = TAPER_MIN_FRAC + (1.0 - TAPER_MIN_FRAC) * pow(age2, 0.75)
			inner2 = inner2.lerp(outer2, 1.0 - wf2)
			# Inner edge near-dark, outer edge bright: the tip moves fastest so it
			# glows most. Physically right, AND it keeps luminance off the caster's
			# body — the two motives coincide, which is how you know it is the right
			# ramp rather than a cosmetic one.
			_ribbon_mesh.surface_set_color(
				Color(col2.r, col2.g, col2.b, a2 * CORE_INNER_ALPHA_FRAC))
			_ribbon_mesh.surface_add_vertex(to_local(anchor + inner2))
			_ribbon_mesh.surface_set_color(Color(col2.r, col2.g, col2.b, a2))
			_ribbon_mesh.surface_add_vertex(to_local(anchor + outer2))
		_ribbon_mesh.surface_end()

	# ---- T-3b: the arc light rides the NEWEST sample -------------------------
	var newest: Dictionary = _hist[n - 1]
	var tip_w: Vector3 = anchor + (newest["outer"] as Vector3)
	_arc_light.global_position = tip_w
	_arc_light.light_color = _c_apex
	_arc_light.light_energy = ARC_LIGHT_ENERGY * _w * _gust_boost
	# ⚑ ONE SURGE, TWO SURFACES. The gust brightens the apex AND what the apex
	#   casts, from the same variable — an emission surge without a matching light
	#   surge would read as the ribbon getting brighter in a room that did not
	#   notice, which is the figure-ground defect T-3 is here to fix.
	_ribbon_mat.emission_energy_multiplier = CORE_EMISSION * _gust_boost
	_arc_light.visible = true


# ---------------------------------------------------------------------------
# ⚑ T-4 — THE LIFECYCLE. Four functions, one per phase that had no read.
# ---------------------------------------------------------------------------

## The ribbon's history window. Constant everywhere except FALLING, where it
## contracts with the channel weight so the arc SHORTENS as it dies.
var _pool: MeshInstance3D
var _pool_mat: StandardMaterial3D
## C-9 PORT 6: the pool's peak, additive, per unit of the source light's energy -- set by eye against the source's
## lap2 film (its floor pool under the tip at full channel), the one AUTHORED number this port adds
const POOL_GAIN := 0.11


func _arc_to_pool() -> void:
	"""C-9 PORT 6: the source's ArcLight, never shown (a light node whites the Barrow out on the phone renderer);
	its position, colour and energy laid on the ground as an additive soft pool of its own range."""
	if _arc_light == null:
		return
	if _pool == null:
		var q := QuadMesh.new()
		q.size = Vector2.ONE * ARC_LIGHT_RANGE * 2.0
		_pool_mat = StandardMaterial3D.new()
		_pool_mat.albedo_texture = _soft_radial_texture()
		_pool_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		_pool_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		_pool_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		_pool_mat.disable_receive_shadows = true
		_pool_mat.render_priority = PaintStack.AFTER_POST_PRIORITY
		_pool = MeshInstance3D.new()
		_pool.name = "ArcPool"
		_pool.mesh = q
		_pool.material_override = _pool_mat
		_pool.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_pool.rotation = Vector3(-PI * 0.5, 0.0, 0.0)
		add_child(_pool)
	var on := _arc_light.visible and _arc_light.light_energy > 0.0 and not ribbon_only
	_pool.visible = on
	if on:
		var p := _arc_light.global_position
		_pool.global_position = Vector3(p.x, _anchor_y + 0.02 * _s, p.z)
		var c := _arc_light.light_color
		var g: float = POOL_GAIN * _arc_light.light_energy
		_pool_mat.albedo_color = Color(c.r * g, c.g * g, c.b * g, 1.0)
	_arc_light.visible = false


func warm(on: bool, at: Vector3) -> void:
	"""C-9 PORT 12: draw every layer once, in its real format, at `at` (in front of the camera, under the veil)."""
	_ribbon_mesh.clear_surfaces()
	_ribbon_body_mesh.clear_surfaces()
	if on:
		for m in [_ribbon_mesh, _ribbon_body_mesh]:
			(m as ImmediateMesh).surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
			# a real-sized strip (12 vertices, 1.2 m, level, faint): a sub-pixel strip drew nothing and warmed nothing
			for i in 12:
				(m as ImmediateMesh).surface_set_color(Color(1, 1, 1, 0.04))
				(m as ImmediateMesh).surface_add_vertex(to_local(at + Vector3(0.1 * float(i), 0.0, 0.25 * float(i % 2))))
			(m as ImmediateMesh).surface_end()
	for arr in [_sparks, _shed, _scuffs, _scour, _residue]:
		if (arr as Array).is_empty():
			continue
		var mi: MeshInstance3D = (arr as Array)[0]["mi"]
		mi.global_position = at
		mi.transparency = 0.5 if on else 0.0
		mi.visible = on
	if _shed.size() > 0:
		var mo: MeshInstance3D = _shed[_shed.size() - 1]["mi"]       # an onset quantum (its own size class)
		mo.global_position = at
		mo.transparency = 0.5 if on else 0.0
		mo.visible = on
	if _arc_light != null:
		_arc_light.global_position = at
		_arc_light.light_energy = 0.01 if on else 0.0
		_arc_light.visible = on
		_arc_to_pool()


func _trail_window() -> int:
	# C-9 PORT 8: the source's 10 samples are 10/60 s of blade; held in TIME, so a 30 fps frame keeps the 150 deg arc
	var n := maxi(2, int(round(float(TRAIL_SAMPLES) * (1.0 / 60.0) / maxf(_dt_avg, 1e-4))))
	if _state == S.FALLING:
		return maxi(2, int(ceil(float(n) * _w)))
	return n


## ⚑ THE ONSET. A one-shot burst of discrete quanta thrown outward from
## 0.6*R_ENGAGE to 1.05*R_ENGAGE over ~0.15 s at SWEEP_Y — the ring-SNAP the
## spec's player-facing sentence asks for, built from an allow-listed discrete
## family rather than from the tinted continuous ring the spec's implementation
## note asks for and the T-3 clause forbids. See the refusal block at RNG_SEED.
func _fire_onset() -> void:
	if ribbon_only:
		return                               # C-9 PORT 10: once per character
	if not _vfx_visible or _rig == null:
		return
	var origin := _rig.global_transform.origin
	var travel: float = (ONSET_R1_FRAC - ONSET_R0_FRAC) * R_ENGAGE
	# Near-linear: the burst must ARRIVE at 1.05*R_ENGAGE inside the window, so
	# the drag is long relative to the life rather than short.
	var v: float = travel / ONSET_LIFE
	for i in range(ONSET_QUANTA):
		# ⚑ EVENLY SPACED, THEN JITTERED HARD. My first build used +/-0.05 rad
		#   against a 0.224 rad spacing and the render came back as a DOTTED
		#   CIRCLE — mechanically regular, which is one step from the "UI-like
		#   annotation" X-1 dim 10 convicted the whole effect of. The jitter is
		#   now +/-0.09 rad on the bearing, +/-9 % on the start radius, +/-0.07 m
		#   in Y and 0.70-1.30 on the speed, so no two quanta share a spoke and
		#   the ring reads as a SNAP rather than as a widget.
		var a: float = (float(i) / float(ONSET_QUANTA)) * TAU + _rng.randf_range(-0.09, 0.09)
		var dir := Vector3(sin(a), 0.0, cos(a))
		var p := origin + dir * (R_ENGAGE * ONSET_R0_FRAC * _rng.randf_range(0.91, 1.09))
		p.y = _anchor_y + SWEEP_Y + _rng.randf_range(-0.07, 0.07) * _s
		_fire_shed(p, dir * v * _rng.randf_range(0.70, 1.30) + Vector3.UP * _rng.randf_range(0.0, 0.35) * _s,
			ONSET_LIFE * _rng.randf_range(0.75, 1.0), true)


## ⚑ THE GUST STREAM. A Poisson event process on a DEDICATED SEEDED generator.
##
## Exponential inter-arrivals have CV = 1.0 by construction — that is a property
## of the distribution, not a number I tuned toward, and it sits mid-band in the
## 0.45-1.15 authoring window with margin on both sides. The realised CV is
## MEASURED anyway and reported in `selfcheck()`, because "the code says
## exponential" and "the render exhibits CV 1.0" are different claims and only
## the second one is the criterion.
##
## ⚑ CONTACT TICKS ARE NOT IN THIS STREAM AND MUST NOT BE. Blade passes are
## physical truth — the spec says so and it is right. The arrhythmia lives in the
## gust/shed stream, which is what the reference corpus's CV was measured on.
func _tick_gusts(delta: float) -> void:
	if _w <= 0.20 or not _vfx_visible:
		_gust_boost = 1.0
		return
	# exponential relaxation of the surge back to unity
	_gust_boost = 1.0 + (_gust_boost - 1.0) * exp(-delta / GUST_SURGE_TAU)
	# ⚑ `lerpf` ALONE, NOT `lerpf(...) * _w`. My first build multiplied twice and
	#   the realised rate fell to 5.5 Hz at half weight — outside the spec's
	#   stated 8-14 band, on the reading that "scaled by _w" meant a second
	#   factor. The lerp IS the scaling.
	var rate: float = lerpf(GUST_RATE_MIN, GUST_RATE_MAX, _w)
	_gust_gate_frames += 1
	_gust_rate_sum += rate
	_gust_next -= delta
	while _gust_next <= 0.0:
		# inter-arrival: -ln(1-u)/rate. `randf()` is [0,1); 1-u is (0,1], so the
		# log is always finite — the open end is on the correct side.
		var iv: float = -log(1.0 - _rng.randf()) / maxf(rate, 0.001)
		_gust_next += iv
		_on_gust(iv)


## ⚑ THE INTERVAL RECORDED IS THE ONE THE PROCESS DREW, NOT `_clock` DIFFERENCED.
##   My first build measured `_clock - _gust_last_t`, and at 14 Hz against a
##   1/60 s step TWO GUSTS REGULARLY LAND IN ONE FRAME — those recorded dt = 0,
##   which dragged the mean to 0.0649 s (a 15.4 Hz rate the process never had)
##   and inflated the CV. An instrument quantised coarser than the thing it
##   measures does not report noise, it reports a DIFFERENT PROCESS. galadriel's
##   frame_forensics necessarily sees the frame-quantised stream — that is the
##   criterion and it is hers — but this file's own receipt should describe the
##   stream it actually generated.
func _on_gust(interval: float) -> void:
	if _gust_n > 0:
		_gust_sum += interval
		_gust_sum_sq += interval * interval
	_gust_last_t = _clock
	_gust_n += 1
	_gust_boost = _rng.randf_range(GUST_SURGE_MIN, GUST_SURGE_MAX)
	if _hist.size() < 1:
		return
	var anchor := _rig.global_transform.origin
	var newest: Dictionary = _hist[_hist.size() - 1]
	var apex: Vector3 = anchor + (newest["outer"] as Vector3)
	var n: int = _rng.randi_range(GUST_QUANTA_MIN, GUST_QUANTA_MAX)
	for _i in range(n):
		_shed_at_apex(apex)


## ⚑ SHED OFF THE RIBBON APEX — NOT off the engagement ring. The ring is 4a's
## scuffs, which stay neutral and stay in their own lane. Tangential velocity
## inherits the blade bearing DERIVATIVE, exactly as 4a does, so its sign is tied
## to `_spin`/OMEGA_DEG by construction and cannot disagree with the rotation.
func _shed_at_apex(apex: Vector3) -> void:
	var tangent := Vector3(cos(_spin), 0.0, -sin(_spin))
	var radial := Vector3(sin(_spin), 0.0, cos(_spin))
	var v0: float = deg_to_rad(OMEGA_DEG) * _w * R_TRAIL * SHED_ENTRAIN_FRAC
	var vel: Vector3 = tangent * v0 * _rng.randf_range(0.6, 1.25) \
		+ radial * v0 * _rng.randf_range(-0.05, 0.30) \
		+ Vector3.UP * _rng.randf_range(0.10, 0.85) * _s
	var jitter := Vector3(_rng.randf_range(-0.09, 0.09),
		_rng.randf_range(-0.07, 0.07), _rng.randf_range(-0.09, 0.09)) * _s
	_fire_shed(apex + jitter, vel,
		_rng.randf_range(SHED_LIFE_MIN, SHED_LIFE_MAX), false)


## A history sample dropped during FALLING becomes a drifting quantum at the
## place the blade actually was. `physical-cause` survives the breakup.
func _shed_from_sample(h: Dictionary, anchor: Vector3) -> void:
	if not _vfx_visible:
		return
	var p: Vector3 = anchor + (h["outer"] as Vector3)
	var tangent := Vector3(cos(_spin), 0.0, -sin(_spin))
	var v0: float = deg_to_rad(OMEGA_DEG) * maxf(_w, 0.15) * R_TRAIL * SHED_ENTRAIN_FRAC * 0.5
	_fire_shed(p, tangent * v0 * _rng.randf_range(0.4, 1.0)
		+ Vector3.UP * _rng.randf_range(0.05, 0.55) * _s,
		_rng.randf_range(SHED_LIFE_MIN, SHED_LIFE_MAX), false)


func _shed_remaining_history() -> void:
	if _rig == null:
		return
	var anchor := _rig.global_transform.origin
	for h in _hist:
		_shed_from_sample(h, anchor)
	_hist.clear()


# ---------------------------------------------------------------------------
# ⚑ T-2 — the residue burst. Fired on the SAME event `contact` is emitted on, so
#   the air and the flinch have one cause between them rather than two clocks
#   that happen to agree.
#
# The refractory here mirrors the STAGE's T-1 refractory (0.35 s) on purpose. The
# two are separate mechanisms in separate files — the stage owns the recipient's
# response and the effect owns the air — but they must gate on the same cadence
# or a mob will visibly gutter residue on a beat its body does not answer.
# ---------------------------------------------------------------------------
## ⚑ T-6. Lay a short arc of scour on the swept bearing. PROGRESSIVE by
## construction — one small arc per blade pass, never a pre-drawn ring — so the
## criterion's "marked area is monotonic non-decreasing during sustain" is a
## property of how it is built rather than something to be checked for.
##
## The marks are laid in WORLD space and left there. The caster translates at
## 3.5 m/s from t = 2.20, so the annulus sweeps a swath and the floor carries the
## PATH of the fight rather than a circle around wherever the caster stopped.
func _lay_scour(origin: Vector3, bearing: Vector3) -> void:
	if not _vfx_visible:
		return
	for i in range(SCOUR_PER_PASS):
		if _scour.size() == 0:
			return
		var s: Dictionary = _scour[_scour_next % _scour.size()]
		_scour_next += 1
		var da: float = (float(i) / maxf(1.0, float(SCOUR_PER_PASS - 1)) - 0.5) \
			* SCOUR_ARC_SPREAD_RAD
		var b2 := Vector3(bearing.x * cos(da) - bearing.z * sin(da), 0.0,
			bearing.x * sin(da) + bearing.z * cos(da))
		var p := origin + b2 * (R_ENGAGE * _rng.randf_range(0.93, 1.04))
		p.y = _anchor_y + SCOUR_Y
		var mi: MeshInstance3D = s["mi"]
		mi.global_position = p
		# yaw it so the marks do not tile into a visible grid — the quad is FLAT,
		# so this rotation is about the world Y and it renders (unlike the
		# billboarded families, where `rotation.y` is discarded).
		mi.rotation = Vector3(-PI * 0.5, 0.0, _rng.randf_range(0.0, TAU))
		mi.transparency = 1.0 - _rng.randf_range(SCOUR_ALPHA_MIN, SCOUR_ALPHA_MAX)
		if not mi.visible:
			_meas_scour_laid += 1
		mi.visible = true


func _fire_residue(host: Node3D, edge: Vector3) -> void:
	if not _vfx_visible or host == null:
		return
	var key := host.get_instance_id()
	if float(_residue_cool.get(key, 0.0)) > 0.0:
		return
	_residue_cool[key] = RESIDUE_REFRACTORY_S
	# The offset is stored RELATIVE TO THE HOST, taken at the contact frame, so
	# the curl stays where the blade actually hit rather than re-centring on the
	# mob every frame — and it travels when T-1 shoves the mob.
	var base_off: Vector3 = edge - host.global_transform.origin
	# ⚑ SIGN FROM THE BEARING DERIVATIVE, the same trick 4a uses: it is tied to
	#   `_spin`/OMEGA_DEG by construction and CANNOT disagree with the rotation.
	var curl_sign: float = signf(cos(_spin))
	if is_zero_approx(curl_sign):
		curl_sign = 1.0
	var n: int = _rng.randi_range(RESIDUE_PER_CONTACT_MIN, RESIDUE_PER_CONTACT_MAX)
	var placed := 0
	for s in _residue:
		if placed >= n:
			break
		if float(s["t"]) > 0.0 or float(s["delay"]) > 0.0:
			continue
		var jitter := Vector3(_rng.randf_range(-0.16, 0.16),
			_rng.randf_range(-0.10, 0.34), _rng.randf_range(-0.16, 0.16)) * _s
		s["host"] = host
		s["off"] = base_off + jitter
		s["rise"] = _rng.randf_range(RESIDUE_RISE_MIN, RESIDUE_RISE_MAX)
		s["curl"] = curl_sign * _rng.randf_range(1.1, 3.0)
		# ⚑ LIFETIMES SPREAD ACROSS THE BURST, not shared. The spec's reason is
		#   exact and it is perceptual: quanta that extinguish together read as a
		#   timer expiring; quanta that gutter out at different moments read as
		#   air dissipating.
		s["life"] = _rng.randf_range(RESIDUE_LIFE_MIN, RESIDUE_LIFE_MAX)
		s["delay"] = _rng.randf_range(0.001, RESIDUE_STAGGER_MAX)
		s["t"] = 0.0
		placed += 1


## Per-frame: stagger in, rise, curl, gutter out, and TRACK THE HOST. The
## position is recomputed from the host every frame rather than integrated, which
## is what makes it follow the T-1 flinch without being reparented into the
## census's INHERITED set (see the T-2 block).
func _tick_residue(delta: float) -> void:
	for k in _residue_cool.keys():
		_residue_cool[k] = maxf(0.0, float(_residue_cool[k]) - delta)
	var alive := 0
	var hosts := {}
	for s in _residue:
		if float(s["delay"]) > 0.0:
			s["delay"] = maxf(0.0, float(s["delay"]) - delta)
			if float(s["delay"]) <= 0.0:
				s["t"] = s["life"]
			continue
		if float(s["t"]) <= 0.0:
			continue
		var host = s["host"]
		if host == null or not is_instance_valid(host):
			s["t"] = 0.0
			(s["mi"] as MeshInstance3D).visible = false
			continue
		s["t"] = float(s["t"]) - delta
		var mi: MeshInstance3D = s["mi"]
		if float(s["t"]) <= 0.0:
			mi.visible = false
			s["host"] = null
			continue
		alive += 1
		hosts[(host as Node3D).get_instance_id()] = true
		# age 0 -> 1 across the quantum's own life
		var age: float = 1.0 - clampf(float(s["t"]) / maxf(0.001, float(s["life"])), 0.0, 1.0)
		var off: Vector3 = s["off"]
		var ang: float = float(s["curl"]) * age
		# spiralling UP off the shoulders: the horizontal component rotates about
		# the host's own vertical while the whole thing rises.
		var rot := Vector3(off.x * cos(ang) - off.z * sin(ang), off.y,
			off.x * sin(ang) + off.z * cos(ang))
		rot.y += float(s["rise"]) * age
		mi.global_position = (host as Node3D).global_transform.origin + rot
		mi.visible = true
		mi.transparency = clampf(1.0 - pow(1.0 - age, 0.75), 0.0, 1.0)
	_meas_residue_alive_max = maxi(_meas_residue_alive_max, alive)
	_meas_residue_hosts_max = maxi(_meas_residue_hosts_max, hosts.size())


func _fire_shed(p: Vector3, vel: Vector3, life: float, onset: bool) -> void:
	if not _vfx_visible:
		return
	for s in _shed:
		if s["t"] > 0.0:
			continue
		if bool(s["onset"]) != onset:
			continue
		var mi: MeshInstance3D = s["mi"]
		mi.global_position = p
		mi.visible = true
		s["t"] = life
		s["life"] = life
		s["vel"] = vel
		return


# ---------------------------------------------------------------------------
# Layer B (contact) + Layer C (ground scuff).
#
# These are how the outer radius gets spent. Both are DISCRETE, BRIEF and
# PHASE-LOCKED to a blade pass. Continuity is what makes a field; quanta are
# what make evidence.
# ---------------------------------------------------------------------------
func _tick_contacts(_delta: float) -> void:
	if ribbon_only:
		return                               # C-9 PORT 10: contacts, sparks, scuffs and scour once per character
	if _w <= 0.35:
		_last_phase = fmod(_spin, PI)
		return
	var phase := fmod(_spin, PI)     # 2 blade passes per revolution
	if phase < _last_phase:
		_on_blade_pass()
	_last_phase = phase


func _on_blade_pass() -> void:
	var origin := _rig.global_transform.origin
	var bearing := Vector3(sin(_spin), 0, cos(_spin)).normalized()

	# --- Layer B: localized hit effects on contact. Spawned on the enemy's
	#     SILHOUETTE EDGE, never its centre, so the body it hits stays readable.
	#     "localized hit effects preserve the rotating silhouette without
	#     obscuring nearby enemies" (§ 3.1.12, itemized reference property).
	for t in _targets:
		if not is_instance_valid(t):
			continue
		var d: Vector3 = t.global_transform.origin - origin
		d.y = 0.0
		if d.length() > R_ENGAGE:
			continue
		var to_t := d.normalized()
		if to_t.dot(bearing) < 0.55:      # only what the blade actually swept past
			continue
		# the near edge of the target, not its middle
		var edge: Vector3 = t.global_transform.origin - to_t * 0.42 * _s
		edge.y = _anchor_y + SWEEP_Y * 0.85
		_fire_spark(edge)
		_fire_residue(t, edge)
		contact.emit(t, edge)

	# --- Layer C: the outer radius, spent in neutral quanta. This is the air a
	#     fast blade throws — evidence of the sweep, at a radius the blade
	#     itself cannot reach (R_ENGAGE 3.52 vs R_TRAIL 2.36). Discrete, brief,
	#     ground-hugging, and NEVER element-tinted.
	if _w > 0.55:
		var p := origin + bearing * R_ENGAGE
		p.y = _anchor_y + 0.03 * _s
		# 4a. The tangent to the sweep at the bearing that threw this quantum —
		# d/ds of `bearing`, so the sign follows _spin / OMEGA_DEG and cannot be
		# set independently of the rotation it is supposed to agree with.
		var tangent := Vector3(cos(_spin), 0.0, -sin(_spin))
		var v0: float = deg_to_rad(OMEGA_DEG) * _w * R_ENGAGE * SCUFF_ENTRAIN_FRAC
		_fire_scuff(p, tangent * v0)
		_lay_scour(origin, bearing)


func _build_pools() -> void:
	var soft := _soft_radial_texture()
	_spark_mat = StandardMaterial3D.new()
	_spark_mat.albedo_texture = soft
	_spark_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_spark_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	_spark_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_spark_mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	_spark_mat.emission_enabled = true
	_spark_mat.emission_energy_multiplier = 2.2
	_spark_mat.disable_receive_shadows = true

	_scuff_mat = StandardMaterial3D.new()
	_scuff_mat.albedo_texture = soft
	_scuff_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	# MIX, not ADD. Dust does not glow, and an additive outer ring would sum
	# into exactly the field this archetype must not have.
	_scuff_mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	_scuff_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_scuff_mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	_scuff_mat.albedo_color = SCUFF_COLOR
	_scuff_mat.disable_receive_shadows = true

	for i in range(MAX_SPARKS):
		var q := QuadMesh.new()
		q.size = Vector2(SPARK_SIZE, SPARK_SIZE)
		var mi := MeshInstance3D.new()
		mi.name = "ContactSpark%d" % i
		mi.mesh = q
		mi.material_override = _spark_mat
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF   # C-1
		mi.visible = false
		add_child(mi)
		var lt := OmniLight3D.new()
		lt.omni_range = 1.1 * _s
		lt.light_energy = 0.0
		lt.visible = false
		lt.shadow_enabled = false                                        # C-1
		mi.add_child(lt)
		_sparks.append({"mi": mi, "light": lt, "t": 0.0})

	# ---- T-4 / T-5: the shed-quantum pool --------------------------------
	# ⚑ SIZE SPREAD RIDES `QuadMesh.size` ACROSS THE POOL, NOT `mi.scale`.
	#   W1 F-2 measured it: BILLBOARD_ENABLED with `billboard_keep_scale` at its
	#   default DISCARDS the instance scale — two quads at scale 1.0 and 3.0 lit
	#   156 px each, ratio 1.0000 where a kept scale would have given 9.0. So a
	#   pool of one size with a runtime scale write would render as ONE size, and
	#   criterion T-5(a)'s "component-area spread IQR/median >= 0.5" would be
	#   structurally unreachable while the code looked like it varied.
	_shed_mat = StandardMaterial3D.new()
	_shed_mat.albedo_texture = soft
	_shed_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_shed_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	_shed_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_shed_mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	_shed_mat.disable_receive_shadows = true
	var shed_i := 0
	for cls in SHED_SIZE_CLASSES:
		for _k in range(SHED_PER_CLASS):
			var qs := QuadMesh.new()
			qs.size = Vector2(cls, cls)
			var mis := MeshInstance3D.new()
			mis.name = "ShedQuantum%d" % shed_i
			shed_i += 1
			mis.mesh = qs
			mis.material_override = _shed_mat
			mis.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF   # C-1
			mis.visible = false
			add_child(mis)
			_shed.append({"mi": mis, "t": 0.0, "life": 1.0,
				"vel": Vector3.ZERO, "onset": false})
	# The onset burst gets its own, larger, reserved slice of the same family —
	# same material, same name, so it is ONE tinted family on the allow-list.
	for _k2 in range(ONSET_QUANTA):
		var qo := QuadMesh.new()
		# ⚑ THREE SIZES ACROSS THE ONSET SLICE, cycling by index. Same W1 F-2
		#   reason as the main pool: identical quads plus a runtime scale write
		#   would render as one size, and a ring of 28 identical dots is exactly
		#   the widget read this burst has to avoid.
		var os: float = ONSET_SIZE * [0.78, 1.06, 1.34][_k2 % 3]
		qo.size = Vector2(os, os)
		var mio := MeshInstance3D.new()
		mio.name = "ShedQuantum%d" % shed_i
		shed_i += 1
		mio.mesh = qo
		mio.material_override = _shed_mat
		mio.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF       # C-1
		mio.visible = false
		add_child(mio)
		_shed.append({"mi": mio, "t": 0.0, "life": ONSET_LIFE,
			"vel": Vector3.ZERO, "onset": true})

	# ---- T-6: the floor-scour pool. NEUTRAL, UNLIT, PERSISTENT. -----------
	_scour_mat = StandardMaterial3D.new()
	# ⚑ ITS OWN FALLOFF, AND THE REASON IS THE CRITERION'S SHAPE. Every other
	#   family here uses `_soft_radial_texture()`, whose pow(a, 2.1) concentrates
	#   alpha at the centre and spends most of the quad's area on a dim rim. That
	#   is right for a SPARK. For a scour it is wrong twice over: perceptually a
	#   scrubbed patch of stone has an edge, and metrically the dim rim pixels
	#   count as "changed" while contributing almost nothing to the mean, which
	#   dragged my first measurement to 5.2/255 against a 6.0 bar while the AREA
	#   leg passed 3.7x over. A plateau raises the mean without touching alpha or
	#   the value, i.e. without making the mark darker than the venue justifies.
	_scour_mat.albedo_texture = _scour_texture()
	_scour_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	# MIX and DARKER THAN TILE. Additive is wrong here by definition: an abrasion
	# that adds light is a glow, and a glowing ring at R_ENGAGE is the failure the
	# whole archetype is defined against.
	_scour_mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	_scour_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	# ⚑ BILLBOARDING OFF — this one LIES ON THE GROUND. Every other quad family in
	#   this file billboards; a billboarded scour would stand up and face the
	#   camera, which is a sprite, not a mark on stone.
	_scour_mat.billboard_mode = BaseMaterial3D.BILLBOARD_DISABLED
	# C-9 PORT 11: the source's rule (floor - 0.0847) on the Barrow's snow, not its Cathedral tile
	var svm: float = (BARROW_FLOOR_LUMA - SCOUR_DEPTH_LUMA) / (0.2126 * SCUFF_COLOR.r + 0.7152 * SCUFF_COLOR.g + 0.0722 * SCUFF_COLOR.b)
	_scour_mat.albedo_color = Color(SCUFF_COLOR.r * svm, SCUFF_COLOR.g * svm, SCUFF_COLOR.b * svm)
	_scour_mat.disable_receive_shadows = true
	for i in range(SCOUR_MAX):
		var qc := QuadMesh.new()
		var cs: float = SCOUR_SIZE_CLASSES[i % SCOUR_SIZE_CLASSES.size()]
		qc.size = Vector2(cs, cs)
		var mic := MeshInstance3D.new()
		mic.name = "FloorScour%d" % i
		mic.mesh = qc
		mic.material_override = _scour_mat
		mic.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF        # C-1
		# lay it flat: QuadMesh is authored in XY facing +Z, so -90 deg about X
		# puts it in the XZ plane facing up.
		mic.rotation = Vector3(-PI * 0.5, 0.0, 0.0)
		mic.visible = false
		add_child(mic)
		_scour.append({"mi": mic})

	# ---- T-2: the recipient-residue pool ---------------------------------
	_residue_mat = StandardMaterial3D.new()
	_residue_mat.albedo_texture = soft
	_residue_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_residue_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	_residue_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_residue_mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	_residue_mat.disable_receive_shadows = true
	var res_i := 0
	for rcls in RESIDUE_SIZE_CLASSES:
		for _r in range(RESIDUE_PER_CLASS):
			var qr := QuadMesh.new()
			qr.size = Vector2(rcls, rcls)
			var mir := MeshInstance3D.new()
			mir.name = "RecipientResidue%d" % res_i
			res_i += 1
			mir.mesh = qr
			mir.material_override = _residue_mat
			mir.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF    # C-1
			mir.visible = false
			add_child(mir)
			_residue.append({"mi": mir, "t": 0.0, "life": 1.0, "delay": 0.0,
				"host": null, "off": Vector3.ZERO, "rise": 0.4, "curl": 0.0})

	for i in range(MAX_SCUFFS):
		var q2 := QuadMesh.new()
		q2.size = Vector2(0.22, 0.22) * _s
		var mi2 := MeshInstance3D.new()
		mi2.name = "ScuffPuff%d" % i
		mi2.mesh = q2
		mi2.material_override = _scuff_mat
		mi2.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF   # C-1
		mi2.visible = false
		add_child(mi2)
		_scuffs.append({"mi": mi2, "t": 0.0, "vel": Vector3.ZERO})    # 4a


func _fire_spark(p: Vector3) -> void:
	if not _vfx_visible:
		return
	for s in _sparks:
		if s["t"] <= 0.0:
			var mi: MeshInstance3D = s["mi"]
			mi.global_position = p
			mi.visible = true
			s["t"] = SPARK_LIFE
			return


func _fire_scuff(p: Vector3, vel: Vector3 = Vector3.ZERO) -> void:
	if not _vfx_visible:
		return
	for s in _scuffs:
		if s["t"] <= 0.0:
			var mi: MeshInstance3D = s["mi"]
			mi.global_position = p
			# ⚑ NO-OP UNDER BILLBOARDING — measured, see the 4a block. Left byte-
			# untouched so this landing's diff is the motion and nothing else; it
			# still consumes the same RNG draw, so the sequence does not shift.
			mi.rotation.y = randf() * TAU
			mi.visible = true
			s["t"] = SCUFF_LIFE
			s["vel"] = vel                                             # 4a
			s["p0"] = p                                                # 4a
			return


func _age_pools(delta: float) -> void:
	for s in _sparks:
		if s["t"] > 0.0:
			s["t"] -= delta
			var k: float = clampf(s["t"] / SPARK_LIFE, 0.0, 1.0)
			var mi: MeshInstance3D = s["mi"]
			var lt: OmniLight3D = s["light"]
			mi.scale = Vector3.ONE * (0.55 + 0.45 * k)
			lt.light_energy = 1.6 * k
			if s["t"] <= 0.0:
				mi.visible = false
				lt.light_energy = 0.0
	# ---- T-4 / T-5: shed quanta ------------------------------------------
	# Exponential drag, integrated before the decay is applied — the same
	# left-Riemann convention 4a uses, so the two families' travel numbers are
	# comparable rather than two different integrals wearing one name.
	var alive := 0
	for s in _shed:
		if s["t"] > 0.0:
			alive += 1
			s["t"] -= delta
			var mis: MeshInstance3D = s["mi"]
			var vs: Vector3 = s["vel"]
			mis.global_position += vs * delta
			s["vel"] = vs * exp(-delta / SHED_DRAG_TAU)
			# ⚑ FADE VIA `GeometryInstance3D.transparency`, NOT via `mi.scale` and
			#   NOT via a per-instance material. Scale is the known no-op under
			#   billboarding (W1 F-2); a per-instance material would be 88 material
			#   copies and 88 draw-call breaks. `transparency` is a per-instance
			#   alpha multiplier the renderer already carries. VERIFIED to render —
			#   see the fade measurement in the T-4 landing note; a second imagined
			#   line in this file would be the third of its kind.
			var kq: float = clampf(s["t"] / maxf(0.001, s["life"] as float), 0.0, 1.0)
			mis.transparency = clampf(1.0 - pow(kq, 0.55), 0.0, 1.0)
			if s["t"] <= 0.0:
				mis.visible = false
				s["vel"] = Vector3.ZERO
	_meas_shed_alive_max = maxi(_meas_shed_alive_max, alive)
	for s in _scuffs:
		if s["t"] > 0.0:
			s["t"] -= delta
			var k2: float = clampf(s["t"] / SCUFF_LIFE, 0.0, 1.0)
			var mi2: MeshInstance3D = s["mi"]
			# --- 4a: the quantum carries the sweep it came from -------------
			# Integrated before the drag is applied, so the first frame of life
			# moves at the spawn speed rather than at a speed already decayed.
			# `delta` is the stage's fixed 1/60 s, so this is deterministic and
			# the ON/OFF diff stays a valid comparison.
			var v: Vector3 = s["vel"]
			if v.length_squared() > 0.0:
				mi2.global_position += v * delta
				s["vel"] = v * exp(-delta / SCUFF_DRAG_TAU)
				# MEASURED AT RUNTIME, not asserted. The arithmetic in the 4a
				# block predicts 0.4539 m at full weight; this is what the
				# running effect actually reached, and selfcheck() reports it.
				_meas_scuff_travel_max = maxf(_meas_scuff_travel_max,
					(mi2.global_position - (s["p0"] as Vector3)).length())
			# ⚑ THIS LINE RENDERS NOTHING — MEASURED, see the 4a block above.
			# BILLBOARD_ENABLED discards instance scale unless
			# `billboard_keep_scale` is set, and it is not. Kept byte-identical:
			# turning it on would change apparent puff size, which is a SECOND
			# variable inside a landing whose whole purpose is to isolate motion.
			mi2.scale = Vector3.ONE * (1.4 - 0.6 * k2)
			if s["t"] <= 0.0:
				mi2.visible = false
				s["vel"] = Vector3.ZERO                                # 4a


# ---------------------------------------------------------------------------
# Self-check. Callable from the gate so the geometric claims in the mint note
# are machine-verified rather than asserted in prose.
# ---------------------------------------------------------------------------
func selfcheck() -> Dictionary:
	var band_lo := SWEEP_Y - SWEEP_WOBBLE
	var band_hi := SWEEP_Y + SWEEP_WOBBLE
	return {
		"H_STAND": H_STAND,
		"R_ENGAGE": R_ENGAGE,
		"R_TRAIL": R_TRAIL,
		"spin_up_s": SPIN_UP_S,
		"spin_down_s": SPIN_DOWN_S,
		"omega_deg_s": OMEGA_DEG,
		"trail_band_authored": [band_lo, band_hi],
		"lower_body_top": LOWER_BODY_TOP,
		"lower_body_clearance_m": band_lo - LOWER_BODY_TOP,
		"bands_disjoint": band_lo > LOWER_BODY_TOP,
		"tinted_surfaces": _tinted_nodes,
		# ⚑ `tinted_count_is_2` IS GONE, NOT SET TO false. The B-arm manifest
		#   recorded it as the receipt for R-9's assert passing; keeping the key
		#   while the property it names is deliberately no longer true would put a
		#   false receipt in the next manifest. The keys below are the amended
		#   guard's receipts and they say what they check.
		"trail_bounded_allow_list": TINTED_ALLOW_LIST.keys(),
		"trail_bounded_clause":
			"no tinted surface may be CONTINUOUS or PERSISTENT at or beyond R_ENGAGE",
		"tinted_all_on_allow_list": _tinted_all_allowed(),
		"tinted_continuous_families": ["TrailRibbonCore", "TrailRibbonBody"],
		"tinted_continuous_max_r_m": R_TRAIL,
		"tinted_continuous_inside_r_engage": R_TRAIL < R_ENGAGE,
		"tinted_discrete_life_ceil_s": TINTED_DISCRETE_LIFE_CEIL_S,
		# T-3 ramp, as DERIVED from the element hue at runtime — not as authored.
		"ramp_element_hue_deg": element_color.h * 360.0,
		"ramp_apex_rgb": [_c_apex.r, _c_apex.g, _c_apex.b],
		"ramp_body_rgb": [_c_body.r, _c_body.g, _c_body.b],
		"ramp_tail_rgb": [_c_tail.r, _c_tail.g, _c_tail.b],
		"ramp_apex_sv": [_c_apex.s, _c_apex.v],
		"ramp_body_sv": [_c_body.s, _c_body.v],
		"ramp_tail_sv": [_c_tail.s, _c_tail.v],
		"core_age_frac": CORE_AGE_FRAC,
		"core_emission_energy": CORE_EMISSION,
		"core_shading": "PER_PIXEL + EMISSION_OP_MULTIPLY (unshaded DROPS emission)",
		"body_shading": "UNSHADED + MIX (must not emit; the only blend that can go dark)",
		"body_alpha_max": BODY_ALPHA_MAX,
		"arc_light_range_m": ARC_LIGHT_RANGE,
		"arc_light_energy_at_full_w": ARC_LIGHT_ENERGY,
		# --- T-4: lifecycle + gust stream. Authored, then MEASURED. ----------
		"rng_seed": RNG_SEED,
		"rng_is_dedicated": true,
		"gust_rate_min_hz": GUST_RATE_MIN,
		"gust_rate_max_hz": GUST_RATE_MAX,
		"gust_process": "Poisson (exponential inter-arrivals) — CV = 1.0 BY CONSTRUCTION",
		"gust_events_measured": _gust_n,
		"gust_gate_frames": _gust_gate_frames,
		"gust_gate_seconds": float(_gust_gate_frames) / 60.0,
		"gust_rate_mean_authored": (_gust_rate_sum / maxf(1.0, float(_gust_gate_frames))),
		"gust_rate_realised": float(_gust_n) / maxf(1e-6, float(_gust_gate_frames) / 60.0),
		"gust_interval_mean_s": _gust_mean(),
		"gust_interval_cv_measured": _gust_cv(),
		"gust_cv_band": [0.45, 1.15],
		"gust_cv_in_band": _gust_cv() >= 0.45 and _gust_cv() <= 1.15,
		"ff08_trip_flag_would_fire": _gust_cv() < 0.25,
		"onset_quanta": ONSET_QUANTA,
		"onset_form": "DISCRETE BURST, not a ring surface — see the T-4 refusal block",
		"onset_r_m": [R_ENGAGE * ONSET_R0_FRAC, R_ENGAGE * ONSET_R1_FRAC],
		"onset_life_s": ONSET_LIFE,
		"onset_fired": _onset_fired,
		# --- T-5: shedding + cross-section. -----------------------------------
		"shed_size_classes_m": SHED_SIZE_CLASSES,
		"shed_size_area_ratio_max_min": (SHED_SIZE_CLASSES[SHED_SIZE_CLASSES.size() - 1]
			* SHED_SIZE_CLASSES[SHED_SIZE_CLASSES.size() - 1])
			/ (SHED_SIZE_CLASSES[0] * SHED_SIZE_CLASSES[0]),
		"shed_size_via": "QuadMesh.size across the pool — mi.scale is a NO-OP under BILLBOARD_ENABLED (W1 F-2)",
		"shed_pool": _shed.size(),
		"shed_life_s": [SHED_LIFE_MIN, SHED_LIFE_MAX],
		"shed_alive_max_measured": _meas_shed_alive_max,
		# --- T-5: cross-section variation. Authored, then MEASURED. -----------
		"xsec_freqs_cycles_per_rad": [XSEC_F1, XSEC_F2],
		"xsec_freqs_are_non_integer": (XSEC_F1 != round(XSEC_F1)) and (XSEC_F2 != round(XSEC_F2)),
		"xsec_phase_advance_per_rev_rad": [fmod(XSEC_F1 * TAU, TAU), fmod(XSEC_F2 * TAU, TAU)],
		"xsec_inner_frac_band_authored": [XSEC_MIN, XSEC_MAX],
		"xsec_inner_frac_measured": [_meas_xsec_lo, _meas_xsec_hi],
		"xsec_width_ratio_measured": ((1.0 - _meas_xsec_lo) / maxf(1.0e-6, 1.0 - _meas_xsec_hi)),
		"xsec_rev_over_rev_rms_pct_predicted": _xsec_rev_rms_pct(),
		"xsec_rev_over_rev_bar_pct": 8.0,
		"trail_samples_unchanged": TRAIL_SAMPLES,
		"arc_stays_open": OMEGA_DEG * (float(TRAIL_SAMPLES) / 60.0) < 360.0,
		# --- T-2: recipient residue. Authored bound, then MEASURED. -----------
		"residue_per_contact": [RESIDUE_PER_CONTACT_MIN, RESIDUE_PER_CONTACT_MAX],
		"residue_life_s": [RESIDUE_LIFE_MIN, RESIDUE_LIFE_MAX],
		"residue_life_ceiling_s": TINTED_DISCRETE_LIFE_CEIL_S,
		"residue_life_under_ceiling": RESIDUE_LIFE_MAX <= TINTED_DISCRETE_LIFE_CEIL_S,
		"residue_rise_m": [RESIDUE_RISE_MIN, RESIDUE_RISE_MAX],
		"residue_refractory_s": RESIDUE_REFRACTORY_S,
		"residue_pool": _residue.size(),
		"residue_attachment": "host-referenced, NOT reparented — keeps the C-8 census ancestry honest",
		# --- T-6: floor scour. NEUTRAL, UNLIT, PERSISTENT. --------------------
		"scour_per_pass": SCOUR_PER_PASS,
		"scour_pool": _scour.size(),
		"scour_laid_measured": _meas_scour_laid,
		"scour_alpha": [SCOUR_ALPHA_MIN, SCOUR_ALPHA_MAX],
		"scour_value_mul": SCOUR_VALUE_MUL,
		"scour_rgb": [SCUFF_COLOR.r * SCOUR_VALUE_MUL, SCUFF_COLOR.g * SCOUR_VALUE_MUL,
			SCUFF_COLOR.b * SCOUR_VALUE_MUL],
		"scour_luma": (0.2126 * SCUFF_COLOR.r + 0.7152 * SCUFF_COLOR.g
			+ 0.0722 * SCUFF_COLOR.b) * SCOUR_VALUE_MUL,
		"scour_is_tinted": false,
		"scour_is_emissive": false,
		"scour_expires": false,
		"scour_admissibility":
			"PERSISTENT at R_ENGAGE and admissible: the TRAIL-BOUNDED clause binds "
			+ "TINTED surfaces. This family is neutral (SCUFF_COLOR, darkened — hue "
			+ "byte-untouched, R-9 intact), unlit, non-emissive, MIX, and is not "
			+ "touched by set_element, so it never enters _tinted_nodes.",
		"residue_alive_max_measured": _meas_residue_alive_max,
		"residue_hosts_simultaneous_max_measured": _meas_residue_hosts_max,
		"arc_span_deg": OMEGA_DEG * (float(TRAIL_SAMPLES) / 60.0),
		"arc_is_open": OMEGA_DEG * (float(TRAIL_SAMPLES) / 60.0) < 360.0,
		# --- MEASURED at runtime (the claims above, checked against the run) ---
		"measured_trail_y": [_meas_y_lo, _meas_y_hi],
		"measured_trail_r": [_meas_r_lo, _meas_r_hi],
		"measured_clears_lower_body": _meas_y_lo > LOWER_BODY_TOP,
		"measured_clearance_m": _meas_y_lo - LOWER_BODY_TOP,
		# --- 4a: spin-following scuffs. Predicted, then MEASURED. ------------
		"scuff_entrain_frac": SCUFF_ENTRAIN_FRAC,
		"scuff_drag_tau_s": SCUFF_DRAG_TAU,
		"scuff_v0_at_full_w_ms": deg_to_rad(OMEGA_DEG) * R_ENGAGE * SCUFF_ENTRAIN_FRAC,
		"scuff_travel_predicted_m": (deg_to_rad(OMEGA_DEG) * R_ENGAGE * SCUFF_ENTRAIN_FRAC)
			* SCUFF_DRAG_TAU * (1.0 - exp(-SCUFF_LIFE / SCUFF_DRAG_TAU)),
		"scuff_travel_measured_max_m": _meas_scuff_travel_max,
		"scuff_arc_predicted_deg": rad_to_deg(
			((deg_to_rad(OMEGA_DEG) * R_ENGAGE * SCUFF_ENTRAIN_FRAC)
				* SCUFF_DRAG_TAU * (1.0 - exp(-SCUFF_LIFE / SCUFF_DRAG_TAU))) / R_ENGAGE),
		# ⚑ SCUFF_COLOR is byte-untouched by 4a and this is the receipt for it.
		"scuff_color_rgb": [SCUFF_COLOR.r, SCUFF_COLOR.g, SCUFF_COLOR.b],
		"scuff_is_tinted": false,
	}


## ⚑ CRITERION T-5(b), DERIVED RATHER THAN HOPED FOR. "Width profile at matched
## rotational phase across consecutive revolutions differs by >= 8 % RMS."
##
## For one sinusoidal term, sin(x + phi) - sin(x) = 2*sin(phi/2)*cos(x + phi/2),
## so the difference is itself a sinusoid of amplitude 2*|sin(phi/2)| where phi
## is that term's phase advance over one revolution (f * TAU). Two mutually
## incommensurate terms add in quadrature, so the RMS of the difference is
## sqrt((a1^2 + a2^2)/2) — and dividing by the MEAN WIDTH FRACTION (not by the
## amplitude) is what makes the answer comparable to the criterion's percentage.
##
## This is stronger evidence than a measurement off the render: it holds for
## EVERY pair of consecutive revolutions rather than for the two that happened to
## be sampled, and if anyone later rounds a frequency to an integer this number
## collapses toward zero and says so.
func _xsec_rev_rms_pct() -> float:
	var a1: float = 0.6 * 2.0 * absf(sin(fmod(XSEC_F1 * TAU, TAU) * 0.5))
	var a2: float = 0.4 * 2.0 * absf(sin(fmod(XSEC_F2 * TAU, TAU) * 0.5))
	var rms_v: float = sqrt((a1 * a1 + a2 * a2) * 0.5)
	var mean_width: float = 1.0 - TRAIL_INNER_FRAC
	return 100.0 * (XSEC_AMP * rms_v) / mean_width


func _gust_mean() -> float:
	if _gust_n < 2:
		return 0.0
	return _gust_sum / float(_gust_n - 1)


## Sample CV of the realised inter-arrival intervals. MEASURED, not claimed from
## the fact that the generator is exponential — those are two different
## statements and only the second one is what FF-08's instrument reads.
func _gust_cv() -> float:
	var n := _gust_n - 1
	if n < 2:
		return 0.0
	var m := _gust_sum / float(n)
	var var_ := maxf(0.0, _gust_sum_sq / float(n) - m * m)
	if m <= 0.0:
		return 0.0
	return sqrt(var_) / m


func _tinted_all_allowed() -> bool:
	for nm in _tinted_nodes:
		if not TINTED_ALLOW_LIST.has(nm):
			return false
	return true


# ⚑ T-6's falloff: a PLATEAU with a short soft rim, not a radial gradient. Flat
# out to 62 % of the radius, then a smooth shoulder to zero. See the call site.
func _scour_texture() -> ImageTexture:
	var n := 64
	var img := Image.create(n, n, false, Image.FORMAT_RGBAF)
	var c := (n - 1) * 0.5
	for y in range(n):
		for x in range(n):
			var d := Vector2(x - c, y - c).length() / c
			var a: float = 1.0
			if d > 0.62:
				a = clampf(1.0 - (d - 0.62) / 0.38, 0.0, 1.0)
				a = a * a * (3.0 - 2.0 * a)      # smoothstep shoulder
			if d > 1.0:
				a = 0.0
			img.set_pixel(x, y, Color(1, 1, 1, a))
	return ImageTexture.create_from_image(img)


# A soft radial falloff, generated rather than depended upon: an untextured
# QuadMesh renders as a hard-edged SQUARE, which reads as a UI artifact and not
# as a spark.
func _soft_radial_texture() -> ImageTexture:
	var n := 64
	var img := Image.create(n, n, false, Image.FORMAT_RGBAF)
	var c := (n - 1) * 0.5
	for y in range(n):
		for x in range(n):
			var d := Vector2(x - c, y - c).length() / c
			var a: float = clampf(1.0 - d, 0.0, 1.0)
			a = pow(a, 2.1)
			img.set_pixel(x, y, Color(1, 1, 1, a))
	return ImageTexture.create_from_image(img)
