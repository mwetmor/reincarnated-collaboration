extends Node3D
class_name SnowField
## C-9 T10-1b — THE SNOW HE STEPS THROUGH. A real 3D snow layer over a FLAT walkable floor.
##
## Matt's three notes this answers (R-C9-74):
##   1. "stay away from non-flat ground"      -> the COLLISION floor is a flat plane. Always.
##   2. "the 3D objects and their sparsity seems at odds with the painted ground"
##                                            -> the ground gains a 3D register of its own:
##                                               snow banks against every object, so the
##                                               stone and the floor are one surface, not a
##                                               model standing on a painting.
##   4. "it seems like you should step through snow piles but none exist"
##                                            -> 0.12 m of snow he is submerged in to the
##                                               ankle, drifts he wades to the knee, and a
##                                               trail he leaves behind him.
##
## IT IS VISUAL ONLY, and that is a design commitment, not an omission:
##   - this node adds NO collision shape of any kind;
##   - it never touches the body's velocity or speed;
##   - the drifts are not obstacles. He walks through a 0.6 m drift at full walk speed.
## The walkable floor stays flat so combat reads, exactly per note 1.
##
## ─────────────────────────────────────────────────────────────────────────────
## THE HEIGHT FUNCTION, in one place, because the shader and the measurement must agree
##
##   D(x,z)   undisturbed depth above the floor  = base * edge + drift + ripple   [baked]
##   p(x,z,t) how pressed down it is, 0..1                                        [stamped]
##   b(x,z,t) the berm pushed up at a track's edge, 0..1                          [stamped]
##
##   H = mix(D, residual, p)  +  berm_frac * b * D
##
## The berm scales with D because the snow in a berm CAME from the channel: ploughing a
## 0.5 m drift throws up a real bank, walking over 0.12 m of crust barely pushes a lip.
## One expression, evaluated in snow_h() in the shader and in depth_at() on the CPU.
##
## ─────────────────────────────────────────────────────────────────────────────
## FOUR THINGS THAT ARE THE WAY THEY ARE BECAUSE THE OBVIOUS WAY IS WRONG
##
## 1. THE FIELD TEXTURE CARRIES ITS OWN GRADIENT (channels B,A), baked. The obvious thing
##    is to take central differences of a height texture in the fragment shader. Do not: the
##    derivative of a BILINEAR interpolant is piecewise constant per texel and DISCONTINUOUS
##    across every texel boundary. At 512 px over 20 m a texel is 0.039 m, which at the play
##    camera is ~3 px -- so the snow would facet every three pixels, and those facets are
##    exactly what the ink pass' crease term is built to find. Baking the gradient from the
##    pre-blur float field and letting the GPU filter THE GRADIENT instead gives a normal
##    that is smooth because it is interpolated, not differentiated.
##
## 2. THE TRAIL DECAYS ON THE GPU, FOR FREE, because the texture stores WHEN each pixel was
##    stamped and the shader subtracts. Decaying a 640x640 float image on the CPU every
##    frame is ~400k GDScript ops per frame and is not affordable; decaying it in a
##    ping-pong SubViewport is affordable but then the CPU cannot read it, and the
##    measurements below need to read it. Storing the stamp TIME costs nothing in either
##    direction. The channel is full float32 (FORMAT_RGBAF) and not half: a half float at
##    t = 300 s resolves to 0.25 s, and wrapping the clock to keep half precision lets a
##    long-dead track RESURRECT one wrap period later.
##
## 3. NO ALPHA IS WRITTEN, ANYWHERE. A spatial shader that assigns ALPHA turns the material
##    transparent, and a transparent surface drops out of the depth and normal buffers --
##    which are the two buffers the ink pass reads, so the snow would silently stop being
##    outlined and stop occluding anything. ALBEDO, ROUGHNESS, NORMAL only.
##
## 4. THE DISPLACED MESH NEEDS A CUSTOM AABB. The geometry is a flat PlaneMesh pushed up in
##    the vertex shader, so its computed AABB is FLAT and Godot frustum-culls it against a
##    volume the snow is not in. It survives at the play camera and vanishes when you tilt.
##    custom_aabb is extended to the tallest drift plus headroom.
## ─────────────────────────────────────────────────────────────────────────────

const PS := preload("res://scripts/paint_stack.gd")

# --- the area, the floor, the wind ------------------------------------------------
## Metres of snow over the flat floor, in the open. Matt's ankle depth.
@export var base_depth_m := 0.12
## What is left under a boot once he has stood on it.
##
## NOT 0.016, AND THE DIFFERENCE IS THE WHOLE "does he sink in" QUESTION. At 0.016 m the
## measurement passed -- boot 0.12 m below the UNDISTURBED surface -- and the close-up showed
## him standing on top of the snow with the whole boot, sole included, in plain view. Both were
## right: he was standing in his own print, which had been pressed to bare ground, so the
## surface HE was in contact with was the floor. The acceptance asks about the undisturbed
## surface and Matt asks about the picture, and only one of those was being answered.
##
## 0.035 m is about 30% of the base depth: unmistakably "pressed down to near the floor" per
## R-C9-74 note 3, while still leaving the boot a third of its sink inside its own print -- and
## the snow immediately outside the print is at full depth, which is what actually reads.
@export var residual_m := 0.035
## The last metres of the field ramp the depth to 0, so the field's edge meets the floor
## tangentially. A 0.12 m cliff at the rim is a genuine depth discontinuity and the ink pass
## is right to draw it.
@export var edge_fade_m := 0.9

# --- drifts: obstacle skirts and tails -------------------------------------------
## Skirt height as a fraction of the obstacle's height -- a 2.71 m stone banks more than a
## 0.54 m rock, which is what "shaped by wind" looks like from above.
@export var skirt_h_frac := 0.15
@export var skirt_h_min_m := 0.12
@export var skirt_h_max_m := 0.38
## How far out from the obstacle's radius the skirt reaches before it is gone.
@export var skirt_w_m := 0.62
## The leeward tail: the skirt's reach multiplied, downwind only.
@export var tail_stretch := 2.7
## The windward side is scoured, so the same skirt is SHORTER into the wind.
@export var windward_squash := 0.72
## How deep the scour hollow is on the windward flank, as a fraction of the skirt height.
@export var scour_frac := 0.16

# --- drifts: the open ground ------------------------------------------------------
## Long low ridges lying ALONG the wind, as wind-driven snow actually forms.
@export var windrow_count := 10
@export var windrow_h_m := Vector2(0.28, 0.55)
@export var windrow_len_m := Vector2(3.0, 7.0)
@export var windrow_w_m := Vector2(0.55, 0.95)
## Isolated rounded piles.
@export var pile_count := 15
@export var pile_h_m := Vector2(0.25, 0.62)
@export var pile_r_m := Vector2(0.45, 0.95)
## Open ground is a REQUIREMENT, not a leftover: this is a combat floor. Placed features
## reject each other and every obstacle inside this radius, and the achieved open fraction
## is reported by bake_report().
@export var feature_clear_m := 1.4
@export var field_seed := 91127
## Surface life, an order of magnitude below the ankle. NOT terrain: a sum of four long
## sines, so it is smooth by construction and has no fractal detail to grow contours from.
@export var ripple_m := 0.010
@export var ripple_scale_m := 1.7

# --- the trail --------------------------------------------------------------------
## Seconds for a track to fill in completely. Linear, so "how much is left" is legible:
## at 1/3 of this it is 2/3 there. Matt's line is readable at 20 s, gone by 60 s.
@export var trail_refill_s := 60.0
@export var boot_len_m := 0.22
@export var boot_w_m := 0.090
## The soft rim of a print. Wider than it sounds on purpose -- see the ink note in _stamp().
@export var boot_rim_m := 0.030
@export var berm_w_m := 0.16
## How much of the displaced depth stands up as a berm.
@export var berm_frac := 0.38
## He re-stamps a foot only after it has travelled this far, which is what makes a line of
## separate prints instead of one smeared trench.
@export var stamp_stride_m := 0.19
## Deeper than this and he is PLOUGHING: the track becomes a continuous channel his legs
## sweep, not a line of prints.
@export var plough_depth_m := 0.22
@export var plough_w_m := 0.46
@export var plough_step_m := 0.08
@export var plough_berm_mult := 1.9

# --- material ---------------------------------------------------------------------
@export var tile_m := 3.6
## Domain warp that breaks the tile's grid, in metres. Free: it reuses the mottle fetch.
@export var detile_warp_m := 0.30
@export var snow_tile: Texture2D
## Pressed snow is denser, so it is cooler and a little darker. This is what makes the track
## read from the play camera at all -- a pure height change in white-on-white does not.
@export var press_tint: Color = Color(0.775, 0.815, 0.885)
@export var press_tint_amt := 0.72
@export var snow_bright := 1.0
# --- the ramp's band edges, for THIS sun -------------------------------------------
# THE RAMP CODE IS THE PROJECT'S ONE RAMP. These are its PARAMETERS, which are already
# per-material everywhere else in the stack (the character gets wash_scale 2.6, the ground
# wash_amp 0.11). They are moved here for a measured reason.
#
# paint_stack's winter_sun says it outright: "a slope tipped 12 degrees toward the sun renders
# at sRGB 1.062 -- PAST WHITE, clipped ... That is why the first snowfield had no form: its
# whole top end was flat against the ceiling." The shipped band edges (e0 0.47, e1 0.70) were
# derived for a 17-DEGREE sun, where flat ground gives N.L = 0.29 and lands at raw 0.65 --
# right on e1, so a slope moves ACROSS a band edge and changes value.
#
# At 55 degrees flat ground gives N.L = 0.82 and lands at raw 0.91, which is deep inside the
# top band. So is every slope tilted toward the sun. Flat snow and the lit face of a drift
# then render IDENTICALLY, and a drift can only be seen where it turns AWAY from the sun --
# which is why the first frames showed the drifts as one-sided stains rather than as piles.
#
# Solved rather than eyeballed. Flat ground sits at raw = 0.5 + 0.5*sin(55) = 0.911; a flank
# tilted 20 deg toward the sun at 0.983, one tilted 20 deg away at 0.787. The first setting
# (e1 0.945 / soft 0.055 / m1 0.56) put flat at 0.60 and the away-flank at 0.56 -- four points
# apart, so the drifts read only by their bright crests and the whole field went cold and dark.
# At e1 0.90 / soft 0.075 / m1 0.60 the same three surfaces land at 0.60, 0.86 and 1.00: the
# away-flank is clearly darker, flat ground keeps the warm cream, and the crest is the
# brightest thing in the frame.
#
# e1 placed just above flat ground restores the crossing: away-flank -> mid, flat -> upper
# mid, lit flank -> top. e0 is left far below so that the DEEP band stays reserved for cast
# shadows (att multiplies raw before the bands), which keeps the stones' shadows dark.
@export var band_e0 := 0.55
@export var band_e1 := 0.90
@export var band_soft := 0.075
@export var band_m0 := 0.10
@export var band_m1 := 0.60
@export var band_m2 := 1.00

# --- resolution -------------------------------------------------------------------
## The field must be bigger than the frame. The play camera sees 10.7337 m of HEIGHT at 47
## degrees of yaw and 52.95 of pitch, so its footprint on the ground is a parallelogram whose
## world-xz bounding box is about 23 m across -- a 20 m field shows its own rim in the corners.
@export var field_px := 512
@export var trail_px := 1024
@export var grid_quad_m := 0.18
## Drifts casting shadows costs a SECOND full geometry pass over the whole grid. Measured, not
## assumed: see the cost_attribution table in the run report.
## ON: measured at +0.05 ms at the shipped 0.18 m quad (48k triangles), which is affordable
## and is most of what makes a drift read as a pile rather than as a pale patch.
@export var cast_shadows := true
## 4 taps == central differences of the trail in both axes (7 fetches total); 2 == forward
## differences (5 fetches). The trail's gradient is the only thing differenced at run time.
@export var normal_taps := 4

# --- kicked snow ------------------------------------------------------------------
@export var puffs := true
@export var puff_pool := 10
@export var puff_amount := 13
@export var spray_amount := 46

# --- ink control ------------------------------------------------------------------
## THE CONTROL FOR THE INK MEASUREMENT. A hard step of this many metres is cut across the
## field, which MUST make the ink pass draw. An instrument that reports "no line" on smooth
## snow has proved nothing until it reports "line" on a step.
@export var debug_step_m := 0.0
@export var debug_step_x := 0.0

var area := Rect2(-10, -10, 20, 20)
var floor_y := 0.0
var wind_dir := Vector2(0.62, 0.78)

var _obstacles: Array = []
# BOTH FIELDS LIVE IN PackedFloat32Array AND NOT IN Image, and that is a measured decision.
# A plough stamp touches ~1900 pixels; through Image.get_pixel/set_pixel, which allocate and
# unpack a Color per access, that cost 5.7 ms on one frame -- a spike twice the whole snow
# budget, on the exact frames he is wading, which is the shot. Indexed float access plus one
# PackedFloat32Array.to_byte_array() memcpy at upload time is the same arithmetic without the
# per-pixel object churn. The Image is rebuilt around the buffer only to hand it to the GPU.
var _field_buf: PackedFloat32Array    # 4/px: D metres, edge, dD/dx, dD/dz
var _field_tex: ImageTexture
var _trail_buf: PackedFloat32Array    # 4/px: press, stamp time s, berm, spare
var _trail_tex: ImageTexture
var _mat: ShaderMaterial
var _mesh_inst: MeshInstance3D
var _t := 0.0
var _trail_dirty := false
var _max_drift := 0.0
var _bake := {}

var _body: Node3D
var _skel: Skeleton3D
var _bones := {}
var _last_stamp := {}                 # foot name -> Vector2 xz of last print
var _last_plough := Vector2.INF
var _prev_foot := {}
var _puffs: Array[GPUParticles3D] = []
var _puff_i := 0
var _flake: Texture2D

const SHADER := """
shader_type spatial;
render_mode specular_disabled, cull_back;
""" + PS.RAMP_UNIFORMS + """
uniform sampler2D field_tex : filter_linear, repeat_disable;
uniform sampler2D trail_tex : filter_linear, repeat_disable;
uniform sampler2D snow_tex : source_color, hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D mottle_noise : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform vec2 area_min;
uniform vec2 area_size;
uniform float floor_y;
uniform float base_depth_m = 0.12;
uniform float residual_m = 0.016;
uniform float berm_frac = 0.38;
uniform float refill_s = 60.0;
uniform float now_s = 0.0;
uniform float tile_m = 3.6;
uniform float detile_warp_m = 0.30;
uniform float wind_c = 1.0;
uniform float wind_s = 0.0;
uniform vec3 press_tint : source_color = vec3(0.775, 0.815, 0.885);
uniform float press_tint_amt = 0.72;
uniform float snow_bright = 1.0;
uniform float mottle_amp = 0.10;
uniform float mottle_scale = 0.085;
uniform float trail_texel_m = 0.031;
uniform float nrm_tap_mult = 1.6;
uniform float taps_4 = 1.0;
varying vec3 v_world;
varying vec2 v_uv;
varying float v_press;
""" + PS.RAMP_BODY + """

// ONE definition of the snow's height, shared with depth_at() on the CPU.
// Returns metres above the floor; hands back press and berm so the caller need not refetch.
float snow_h(vec2 uv, out float p, out float b, out vec4 f) {
	// `f` is handed BACK rather than refetched by the caller: fragment() needs the baked
	// gradient in f.ba as well as the depth in f.r, and a second texture(field_tex, v_uv)
	// there is a duplicate full-screen fetch for data this function already had.
	f = texture(field_tex, uv);
	vec4 t = texture(trail_tex, uv);
	float fade = clamp(1.0 - (now_s - t.g) / max(refill_s, 1e-3), 0.0, 1.0);
	p = clamp(t.r * fade, 0.0, 1.0);
	b = clamp(t.b * fade, 0.0, 1.0);
	return mix(f.r, residual_m, p) + berm_frac * b * f.r;
}

void vertex() {
	// PlaneMesh UV runs 0..1 across the plane, so it IS the field lookup with no maths.
	v_uv = UV;
	float p, b;
	vec4 f;
	float h = snow_h(UV, p, b, f);
	VERTEX.y += h;
	v_press = p;
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	float p, b;
	vec4 f;
	float hc = snow_h(v_uv, p, b, f);
	float D = f.r;
	// THE NORMAL, ANALYTICALLY. grad H = gradD*(1-p) - (D - residual)*grad p
	//                                   + berm_frac*(D*grad b + b*gradD)
	// gradD comes BAKED out of the field texture (channels B,A) -- see note 1 in the header.
	// grad p and grad b are the only things differenced here, and they are differenced over
	// more than a texel so the taps land in different texels of the trail image.
	vec2 gD = f.ba;
	vec2 o = vec2(trail_texel_m * nrm_tap_mult) / area_size;
	vec2 pxy = vec2(0.0);
	vec2 bxy = vec2(0.0);
	// THE TRAIL TAPS ARE SKIPPED WHERE THERE IS NO TRAIL, and that is the single biggest
	// saving in this shader. The snow covers 95% of the play frame (measured: 1,970,726 of
	// 2,073,600 pixels), so every fetch here is very nearly a full-screen fetch -- 0.26 ms
	// each. But a trail is a line a man walked: it is a fraction of a per cent of the field,
	// and the other 99% was paying four fetches to difference a field that is zero on both
	// sides. Branching is worth it because the two cases are LARGE COHERENT REGIONS on screen
	// rather than a fine interleave, so a GPU quad is almost never split between them.
	if (p + b > 0.0005) {
		vec4 ign;
		float px, bx, py, by;
		snow_h(v_uv + vec2(o.x, 0.0), px, bx, ign);
		snow_h(v_uv + vec2(0.0, o.y), py, by, ign);
		if (taps_4 > 0.5) {
			float pxm, bxm, pym, bym;
			snow_h(v_uv - vec2(o.x, 0.0), pxm, bxm, ign);
			snow_h(v_uv - vec2(0.0, o.y), pym, bym, ign);
			float sx = 2.0 * trail_texel_m * nrm_tap_mult;
			pxy = vec2((px - pxm) / sx, (py - pym) / sx);
			bxy = vec2((bx - bxm) / sx, (by - bym) / sx);
		} else {
			float sx = trail_texel_m * nrm_tap_mult;
			pxy = vec2((px - p) / sx, (py - p) / sx);
			bxy = vec2((bx - b) / sx, (by - b) / sx);
		}
	}
	vec2 gH = gD * (1.0 - p) - (D - residual_m) * pxy + berm_frac * (D * bxy + b * gD);
	// +z in UV is +z in world for a PlaneMesh laid on xz, so gH is (dH/dx, dH/dz).
	vec3 wn = normalize(vec3(-gH.x, 1.0, -gH.y));
	// NORMAL is VIEW SPACE in a Godot 4 fragment shader; v_world stays world for the wash.
	NORMAL = normalize((VIEW_MATRIX * vec4(wn, 0.0)).xyz);

	// ONE mottle fetch doing TWO jobs: the low-frequency value break, and the domain warp
	// that breaks the tile's own grid. A proper de-tile blends a second sample at another
	// scale, which is another full-screen fetch (~0.26 ms measured); reusing this one is free.
	float m = texture(mottle_noise, v_world.xz * mottle_scale).r;
	// THE WARP MUST BE LOW-FREQUENCY AND SMALL, and the first attempt was neither. At
	// mottle_scale 0.33 the noise repeats every 3 m and its fourth octave carries 0.37 m
	// detail; warping a 3.6 m tile by +-0.45 m of THAT compresses and stretches the painted
	// streaks within a single streak's width, and the snow came back as brain coral -- a
	// worse artefact than the tiling it was there to hide. The warp is a WANDER, so its noise
	// must be coarser than the thing it displaces, not finer.
	vec2 warp = vec2(m - 0.5, 0.5 - m) * detile_warp_m;
	// THE TILE IS TURNED TO FACE THE WIND, and this is the difference between snow and cloth.
	// snow.png is painted with directional drift streaks. Sampled on the world axes they run
	// at whatever angle the world happens to use and CROSS the baked windrows, and two
	// regular diagonal patterns crossing is exactly what woven canvas looks like -- which is
	// what the first frame came back as. Rotated onto wind_dir the painted streaks and the 3D
	// drifts are the same weather blowing the same way.
	vec2 wp = vec2(v_world.x * wind_c - v_world.z * wind_s,
				   v_world.x * wind_s + v_world.z * wind_c);
	vec3 base = texture(snow_tex, (wp + warp) / tile_m).rgb * snow_bright;
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	// pressed snow reads cooler and slightly darker, which is what makes the track visible
	base = mix(base, base * press_tint, clamp(p, 0.0, 1.0) * press_tint_amt);
	ALBEDO = base;
	ROUGHNESS = 1.0;
	// NO ALPHA. See note 3 in the header.
}

void light() {
	// THE SAME RAMP AS THE WORLD AND AS HIM. Not a snow lighting model; the project's one
	// lighting model, applied to snow.
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, ATTENUATION, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix);
}
"""


# =============================================================================
#  THE INTERFACE THE BARROW CALLS
# =============================================================================
func setup(a: Rect2, fy: float, obstacles: Array, wind: Vector2) -> void:
	"""Bake the drift field and build the mesh. `a` is metres in xz, `obstacles` is
	[{pos: Vector3, radius_m: float, height_m: float}], `wind` is the direction the wind
	BLOWS TOWARD (tails form on the far side of an obstacle from it)."""
	area = a
	floor_y = fy
	_obstacles = obstacles.duplicate()
	wind_dir = wind.normalized() if wind.length() > 1e-6 else Vector2(0.62, 0.78)
	# idempotent: the ink CONTROL re-bakes the same field with a hard step cut into it, and a
	# second setup() that left the first mesh in the scene would measure two snow layers
	if _mesh_inst != null:
		_mesh_inst.queue_free()
		_mesh_inst = null
	for p in _puffs:
		p.queue_free()
	_puffs.clear()
	_puff_i = 0
	_bake_field()
	_make_trail()
	_build_mesh()
	if puffs:
		_build_puffs()


func track(body: Node3D) -> void:
	"""Carve the snow under this body's feet. Finds the Skeleton3D and the foot bones by
	name from the rig itself -- see _bind_feet() for why the names are read and not assumed."""
	_body = body
	_skel = _find_skel(body)
	_bind_feet()


func bake_report() -> Dictionary:
	return _bake.duplicate(true)


# =============================================================================
#  THE FIELD BAKE  (CPU, once, in setup)
# =============================================================================
func _bake_field() -> void:
	var t0 := Time.get_ticks_usec()
	var n := field_px
	var h := PackedFloat32Array()
	h.resize(n * n)
	h.fill(0.0)
	var mx := area.size.x / float(n)     # metres per pixel
	var mz := area.size.y / float(n)
	var w := wind_dir
	var perp := Vector2(-w.y, w.x)
	var feats := []

	# --- obstacle skirts and leeward tails ---
	for ob in _obstacles:
		var pos: Vector3 = ob["pos"]
		var r := float(ob.get("radius_m", 0.4))
		var oh := float(ob.get("height_m", 1.0))
		var hs := clampf(skirt_h_frac * oh, skirt_h_min_m, skirt_h_max_m)
		var ws: float = skirt_w_m + r * 0.6
		var reach: float = r + ws * tail_stretch + 0.2
		_scatter(h, n, mx, mz, Vector2(pos.x, pos.z), reach, func(o: Vector2) -> float:
			var along := o.dot(w)
			var across := o.dot(perp)
			var stretch: float = tail_stretch if along > 0.0 else windward_squash
			var a2 := along / stretch
			var d := sqrt(a2 * a2 + across * across)
			var t := (d - r) / ws
			if t >= 1.0:
				return 0.0
			var v := hs * (1.0 - _smoother(t))
			# the windward scour: a shallow hollow just upwind of the skirt, which is what
			# tells the eye the pile was BUILT by wind rather than dropped there
			if along < 0.0:
				var sd := (d - r) / ws
				if sd > 0.35 and sd < 1.9:
					v -= hs * scour_frac * sin((sd - 0.35) / 1.55 * PI)
			return v
		)
		feats.append({"c": Vector2(pos.x, pos.z), "r": r + 0.4})

	# --- windrows: long, low, lying ALONG the wind ---
	var rng := RandomNumberGenerator.new()
	rng.seed = field_seed
	var placed := 0
	var tries := 0
	while placed < windrow_count and tries < 400:
		tries += 1
		var c := _rand_pt(rng)
		var ln := rng.randf_range(windrow_len_m.x, windrow_len_m.y)
		var wd := rng.randf_range(windrow_w_m.x, windrow_w_m.y)
		var hg := rng.randf_range(windrow_h_m.x, windrow_h_m.y)
		if not _clear_of(c, maxf(ln, wd) * 0.5, feats):
			continue
		var ang := rng.randf_range(-0.30, 0.30)
		var wl := w.rotated(ang)
		var wp := Vector2(-wl.y, wl.x)
		var sinu := rng.randf_range(0.18, 0.40)
		var sfreq := rng.randf_range(0.55, 1.05)
		_scatter(h, n, mx, mz, c, ln * 0.5 + wd + 0.3, func(o: Vector2) -> float:
			var al := o.dot(wl)
			var ac := o.dot(wp) - sin(al * sfreq) * sinu
			var ta := absf(al) / (ln * 0.5)
			var tc := absf(ac) / (wd * 0.5)
			if ta >= 1.0 or tc >= 1.0:
				return 0.0
			return hg * (1.0 - _smoother(tc)) * (1.0 - _smoother(ta * ta))
		)
		feats.append({"c": c, "r": maxf(ln, wd) * 0.5})
		placed += 1
	_bake["windrows_placed"] = placed

	# --- loose piles ---
	var piles := 0
	tries = 0
	while piles < pile_count and tries < 500:
		tries += 1
		var c := _rand_pt(rng)
		var pr := rng.randf_range(pile_r_m.x, pile_r_m.y)
		var ph := rng.randf_range(pile_h_m.x, pile_h_m.y)
		if not _clear_of(c, pr, feats):
			continue
		var sq := rng.randf_range(0.7, 1.4)
		var rot := rng.randf_range(0.0, PI)
		var ra := Vector2(cos(rot), sin(rot))
		var rb := Vector2(-ra.y, ra.x)
		_scatter(h, n, mx, mz, c, pr * maxf(sq, 1.0 / sq) + 0.25, func(o: Vector2) -> float:
			var u := o.dot(ra) / sq
			var v := o.dot(rb) * sq
			var t := sqrt(u * u + v * v) / pr
			if t >= 1.0:
				return 0.0
			return ph * (1.0 - _smoother(t))
		)
		feats.append({"c": c, "r": pr})
		piles += 1
	_bake["piles_placed"] = piles

	# --- a light blur, so nothing a feature's bbox did can show as an edge ---
	h = _blur(h, n, 2)

	# --- the base depth, the edge taper and the ripple; then the gradient ---
	var Dv := PackedFloat32Array()
	Dv.resize(n * n)
	var edge := PackedFloat32Array()
	edge.resize(n * n)
	_max_drift = 0.0
	var k1 := TAU / ripple_scale_m
	var k2 := TAU / (ripple_scale_m * 1.73)
	for j in n:
		var z := area.position.y + (float(j) + 0.5) * mz
		for i in n:
			var x := area.position.x + (float(i) + 0.5) * mx
			var e := _edge_at(x, z)
			var rip := ripple_m * 0.25 * (
				sin(x * k1) + sin(z * k1 * 0.87 + 1.7)
				+ sin((x * 0.71 + z * 0.70) * k2 + 0.4)
				+ sin((x * 0.70 - z * 0.71) * k2 * 1.31 + 2.6))
			var d: float = h[j * n + i]
			if debug_step_m > 0.0 and x >= debug_step_x:
				d += debug_step_m
			var Dd: float = maxf((base_depth_m + rip) * e + d * e, 0.0)
			Dv[j * n + i] = Dd
			edge[j * n + i] = e
			if d > _max_drift:
				_max_drift = d

	_field_buf = PackedFloat32Array()
	_field_buf.resize(n * n * 4)
	for j in n:
		var jm: int = maxi(j - 1, 0)
		var jp: int = mini(j + 1, n - 1)
		for i in n:
			var im: int = maxi(i - 1, 0)
			var ip: int = mini(i + 1, n - 1)
			var dDdx: float = (Dv[j * n + ip] - Dv[j * n + im]) / (float(ip - im) * mx)
			var dDdz: float = (Dv[jp * n + i] - Dv[jm * n + i]) / (float(jp - jm) * mz)
			var o := (j * n + i) * 4
			_field_buf[o] = Dv[j * n + i]
			_field_buf[o + 1] = edge[j * n + i]
			_field_buf[o + 2] = dDdx
			_field_buf[o + 3] = dDdz
	_field_tex = ImageTexture.create_from_image(Image.create_from_data(
		n, n, false, Image.FORMAT_RGBAF, _field_buf.to_byte_array()))

	# --- what got built, in numbers, so "open ground" is a measurement not a hope ---
	var above := 0
	var deep := 0
	var tot := n * n
	var hsum := 0.0
	for v in Dv:
		hsum += v
		if v > base_depth_m + 0.05:
			above += 1
		if v > plough_depth_m:
			deep += 1
	_bake["field_px"] = n
	_bake["m_per_px"] = snappedf(mx, 0.0001)
	_bake["drifted_frac"] = snappedf(float(above) / float(tot), 0.0001)
	_bake["open_frac"] = snappedf(1.0 - float(above) / float(tot), 0.0001)
	_bake["wade_frac"] = snappedf(float(deep) / float(tot), 0.0001)
	_bake["mean_depth_m"] = snappedf(hsum / float(tot), 0.0001)
	_bake["max_drift_m"] = snappedf(_max_drift, 0.001)
	_bake["bake_ms"] = snappedf((Time.get_ticks_usec() - t0) / 1000.0, 0.1)


func _edge_at(x: float, z: float) -> float:
	var dl := x - area.position.x
	var dr := area.position.x + area.size.x - x
	var dt := z - area.position.y
	var db := area.position.y + area.size.y - z
	var d := minf(minf(dl, dr), minf(dt, db))
	return _smoother(clampf(d / maxf(edge_fade_m, 1e-3), 0.0, 1.0))


func _rand_pt(rng: RandomNumberGenerator) -> Vector2:
	var pad: float = edge_fade_m + 1.0
	return Vector2(
		rng.randf_range(area.position.x + pad, area.position.x + area.size.x - pad),
		rng.randf_range(area.position.y + pad, area.position.y + area.size.y - pad))


func _clear_of(c: Vector2, r: float, feats: Array) -> bool:
	for f in feats:
		if c.distance_to(f["c"]) < r + float(f["r"]) + feature_clear_m:
			return false
	return true


func _scatter(h: PackedFloat32Array, n: int, mx: float, mz: float,
		c: Vector2, reach: float, fn: Callable) -> void:
	"""Evaluate a feature ONLY inside its own bounding box. Gathering -- every pixel asking
	every feature -- is field_px^2 * feature_count and takes tens of seconds in GDScript for
	a result that is zero almost everywhere."""
	var i0: int = maxi(int(floor((c.x - reach - area.position.x) / mx)), 0)
	var i1: int = mini(int(ceil((c.x + reach - area.position.x) / mx)), n - 1)
	var j0: int = maxi(int(floor((c.y - reach - area.position.y) / mz)), 0)
	var j1: int = mini(int(ceil((c.y + reach - area.position.y) / mz)), n - 1)
	for j in range(j0, j1 + 1):
		var z := area.position.y + (float(j) + 0.5) * mz
		for i in range(i0, i1 + 1):
			var x := area.position.x + (float(i) + 0.5) * mx
			var v: float = fn.call(Vector2(x, z) - c)
			if v != 0.0:
				h[j * n + i] = h[j * n + i] + v


func _blur(src: PackedFloat32Array, n: int, r: int) -> PackedFloat32Array:
	if r <= 0:
		return src
	var tmp := PackedFloat32Array()
	tmp.resize(n * n)
	var inv := 1.0 / float(2 * r + 1)
	for j in n:
		var row := j * n
		for i in n:
			var s := 0.0
			for k in range(-r, r + 1):
				s += src[row + clampi(i + k, 0, n - 1)]
			tmp[row + i] = s * inv
	var out := PackedFloat32Array()
	out.resize(n * n)
	for j in n:
		for i in n:
			var s := 0.0
			for k in range(-r, r + 1):
				s += tmp[clampi(j + k, 0, n - 1) * n + i]
			out[j * n + i] = s * inv
	return out


static func _smoother(t: float) -> float:
	t = clampf(t, 0.0, 1.0)
	return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# =============================================================================
#  THE TRAIL
# =============================================================================
func _make_trail() -> void:
	_trail_buf = PackedFloat32Array()
	_trail_buf.resize(trail_px * trail_px * 4)
	for k in trail_px * trail_px:
		_trail_buf[k * 4 + 1] = -1.0e6      # stamp time far in the past == dead
	_trail_tex = ImageTexture.create_from_image(Image.create_from_data(
		trail_px, trail_px, false, Image.FORMAT_RGBAF, _trail_buf.to_byte_array()))
	_last_stamp.clear()
	_last_plough = Vector2.INF


func clear_trail() -> void:
	_make_trail()
	if _mat != null:
		_mat.set_shader_parameter("trail_tex", _trail_tex)


func _uv_of(xz: Vector2) -> Vector2:
	return Vector2((xz.x - area.position.x) / area.size.x,
				   (xz.y - area.position.y) / area.size.y)


func _stamp(centre: Vector2, fwd: Vector2, half_len: float, half_wid: float,
		rim: float, berm_mult: float) -> void:
	"""Press an oriented ellipse into the trail image and push a berm up around it.

	THE RIM IS AS TIGHT AS THE INK BUDGET ALLOWS (boot_rim_m, 3 cm). It began at 6 cm for the
	reason below, which is real; but a 6 cm ramp out of a 22 cm print means full-depth snow does
	not resume until 8 cm from the boot's side, and at the play camera's 53 degree rake that is
	a visible moat of shallow snow around each boot. The measured ink cost of tightening it to
	3 cm was 0.31% of snow pixels against a 1% budget, so the budget paid for it. A print
	whose wall falls 0.12 m over 2 cm is very nearly a STEP, and a step is what the ink
	pass' second-difference depth term exists to find: the predicted second difference goes
	from 3e-3 m at a 5 cm wall to 6e-2 m at a 2 cm one, and the threshold is 3e-2 m. So a
	hard-edged footprint inks a black outline round every print -- which looks deliberate
	for about one second and then reads as a rash of holes. Soft rim, and the track reads by
	COLOUR (press_tint) as much as by shape."""
	var f := fwd.normalized() if fwd.length() > 1e-5 else Vector2(0, 1)
	var s := Vector2(-f.y, f.x)
	var reach: float = maxf(half_len, half_wid) + rim + berm_w_m
	var mpp := area.size.x / float(trail_px)
	var mppz := area.size.y / float(trail_px)
	var i0: int = maxi(int(floor(((centre.x - reach) - area.position.x) / mpp)), 0)
	var i1: int = mini(int(ceil(((centre.x + reach) - area.position.x) / mpp)), trail_px - 1)
	var j0: int = maxi(int(floor(((centre.y - reach) - area.position.y) / mppz)), 0)
	var j1: int = mini(int(ceil(((centre.y + reach) - area.position.y) / mppz)), trail_px - 1)
	if i1 < i0 or j1 < j0:
		return
	# hoisted out of the inner loop: reciprocals, and the two squares that were pow(x, 2.0)
	var inv_l := 1.0 / maxf(half_len, 1e-4)
	var inv_w := 1.0 / maxf(half_wid, 1e-4)
	var inv_rim := 1.0 / maxf(rim * inv_w, 1e-4)
	var inv_refill := 1.0 / maxf(trail_refill_s, 1e-3)
	var hw := maxf(half_wid, 1e-4)
	var bw := maxf(berm_w_m, 1e-4)
	var inv_bspan := 1.0 / (bw * 1.5)
	for j in range(j0, j1 + 1):
		var z := area.position.y + (float(j) + 0.5) * mppz
		var row := j * trail_px
		for i in range(i0, i1 + 1):
			var x := area.position.x + (float(i) + 0.5) * mpp
			var ox := x - centre.x
			var oz := z - centre.y
			var al := absf(ox * f.x + oz * f.y) * inv_l
			var ac := absf(ox * s.x + oz * s.y) * inv_w
			# normalised elliptical distance: 1.0 at the boot's own edge
			var e := sqrt(al * al + ac * ac)
			var press := 1.0 - _smoother((e - 1.0) * inv_rim)
			# the berm rides just OUTSIDE the print, peaking a little past the rim
			var bt: float = (e - 1.0) * hw - rim * 0.4
			var berm := 0.0
			if bt > -bw * 0.5 and bt < bw:
				# a raised cosine, not a sine call: same shape, no transcendental per pixel
				var u := clampf((bt + bw * 0.5) * inv_bspan, 0.0, 1.0)
				berm = berm_mult * 4.0 * u * (1.0 - u)
			if press <= 0.002 and berm <= 0.002:
				continue
			var o := (row + i) * 4
			var fade := clampf(1.0 - (_t - _trail_buf[o + 1]) * inv_refill, 0.0, 1.0)
			# REBASE THE OLD VALUE TO NOW instead of keeping its old timestamp. Taking a max
			# on the raw amplitude and then writing the new time would RESET the age of an
			# old faint print to zero and make it bright again.
			_trail_buf[o] = maxf(_trail_buf[o] * fade, clampf(press, 0.0, 1.0))
			_trail_buf[o + 2] = maxf(_trail_buf[o + 2] * fade, clampf(berm, 0.0, 1.0))
			_trail_buf[o + 1] = _t
	_trail_dirty = true


# =============================================================================
#  THE FEET
# =============================================================================
func _find_skel(n: Node) -> Skeleton3D:
	if n is Skeleton3D:
		return n
	for c in n.get_children():
		var r := _find_skel(c)
		if r != null:
			return r
	return null


func _bind_feet() -> void:
	"""READ THE BONE NAMES OFF THE RIG. The Meshy 24-bone rig is not a Mixamo rig wearing
	its names: it has NO finger bones, its neck is lower-case `neck` where everything else
	is CamelCase, and its spine runs Hips -> Spine02 -> Spine01 -> Spine, so the name that
	LOOKS like the root of the spine is the one nearest the shoulders. Assuming any of that
	gets a silent -1 out of find_bone and a track that never stamps."""
	_bones.clear()
	if _skel == null:
		push_error("SnowField.track: no Skeleton3D under %s" % _body)
		return
	var want := {"L": ["LeftFoot", "LeftToeBase"], "R": ["RightFoot", "RightToeBase"]}
	for side in want:
		for nm in want[side]:
			var idx := _skel.find_bone(nm)
			if idx < 0:
				push_warning("SnowField: no bone '%s' on this rig" % nm)
			else:
				_bones[side + ("_toe" if nm.ends_with("ToeBase") else "_foot")] = idx
	_bake["bones_bound"] = _bones.keys()
	_bake["bone_count"] = _skel.get_bone_count()


func _foot_pos(key: String) -> Vector3:
	var idx: int = _bones.get(key, -1)
	if idx < 0:
		return Vector3.INF
	return _skel.global_transform * _skel.get_bone_global_pose(idx).origin


func _physics_process(dt: float) -> void:
	# THE RIG'S AnimationPlayer RUNS ON THE PHYSICS CALLBACK (knight.gd sets
	# ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS), so the bone poses are only fresh here. Reading
	# them in _process samples whatever last frame left behind.
	_t += dt
	if _mat != null:
		_mat.set_shader_parameter("now_s", _t)
	if _skel == null or _bones.is_empty():
		return
	var fwd := Vector2(0, 1)
	if _body != null:
		var b := _body.global_transform.basis
		fwd = Vector2(-b.z.x, -b.z.z)
	for side in ["L", "R"]:
		var fp := _foot_pos(side + "_foot")
		var tp := _foot_pos(side + "_toe")
		if fp == Vector3.INF:
			continue
		var contact_y: float = fp.y if tp == Vector3.INF else minf(fp.y, tp.y)
		var here := Vector2(fp.x, fp.z) if tp == Vector3.INF \
			else Vector2((fp.x + tp.x) * 0.5, (fp.z + tp.z) * 0.5)
		var lift := contact_y - floor_y
		if lift > 0.13:
			continue
		var last: Variant = _last_stamp.get(side, null)
		if last != null and here.distance_to(last) < stamp_stride_m:
			continue
		_last_stamp[side] = here
		var D := depth_at(here)
		var deep: bool = D > plough_depth_m
		_stamp(here, fwd, boot_len_m * 0.5, boot_w_m * 0.5, boot_rim_m,
			plough_berm_mult if deep else 1.0)
		if puffs:
			_puff(Vector3(here.x, floor_y + minf(D, 0.5) * 0.5, here.y), fwd, D, deep)
		if deep:
			_plough(here, fwd, D)


func _plough(here: Vector2, fwd: Vector2, D: float) -> void:
	"""A CHANNEL, not a line of prints. Separate prints are what walking on 0.12 m of crust
	leaves; wading a 0.5 m drift leaves one trench his legs swept, with the snow that was in
	it standing up along both edges."""
	if _last_plough == Vector2.INF or here.distance_to(_last_plough) > 2.0:
		_last_plough = here
		return
	if here.distance_to(_last_plough) < plough_step_m:
		return
	var seg := here - _last_plough
	var steps: int = maxi(int(ceil(seg.length() / (plough_w_m * 0.35))), 1)
	# k starts at 1: k == 0 is the previous stamp's own centre, already in the buffer, and
	# re-stamping it doubles the per-frame pixel cost for no change to the picture
	for k in range(1, steps + 1):
		var c: Vector2 = _last_plough + seg * (float(k) / float(steps))
		_stamp(c, fwd, plough_w_m * 0.5, plough_w_m * 0.5, boot_rim_m * 1.5,
			plough_berm_mult * clampf(D / maxf(plough_depth_m, 1e-3), 1.0, 2.6))
	_last_plough = here


# =============================================================================
#  THE CPU MIRROR OF THE HEIGHT FUNCTION  (the instrument, per PaintStack's precedent:
#  it samples THE VERY IMAGES THE GPU SAMPLES, not a re-implementation that can disagree)
# =============================================================================
func _bilinear4(buf: PackedFloat32Array, n: int, uv: Vector2) -> Array:
	"""Bilinear on the SAME BUFFER THE GPU SAMPLES, in the same 4-channel layout, so the
	measurement cannot disagree with the picture about how deep the snow is. (PaintStack's
	own precedent: its snow measurement samples the very image the shader samples rather
	than a re-implementation of the same formula.)"""
	var x := clampf(uv.x * float(n) - 0.5, 0.0, float(n - 1))
	var y := clampf(uv.y * float(n) - 0.5, 0.0, float(n - 1))
	var i0 := int(floor(x))
	var j0 := int(floor(y))
	var i1: int = mini(i0 + 1, n - 1)
	var j1: int = mini(j0 + 1, n - 1)
	var fx := x - float(i0)
	var fy := y - float(j0)
	var oa := (j0 * n + i0) * 4
	var ob := (j0 * n + i1) * 4
	var oc := (j1 * n + i0) * 4
	var od := (j1 * n + i1) * 4
	var out := []
	for c in 4:
		var top: float = lerpf(buf[oa + c], buf[ob + c], fx)
		var bot: float = lerpf(buf[oc + c], buf[od + c], fx)
		out.append(lerpf(top, bot, fy))
	return out


func depth_at(xz: Vector2) -> float:
	"""Undisturbed depth D above the floor, metres. This is what 'how deep is the snow here'
	means for the sink and base-ring measurements."""
	if _field_buf.is_empty():
		return 0.0
	return _bilinear4(_field_buf, field_px, _uv_of(xz))[0]


func surface_y(xz: Vector2) -> float:
	"""The snow surface, metres in world y, INCLUDING the trail -- the same expression
	snow_h() evaluates on the GPU."""
	if _field_buf.is_empty():
		return floor_y
	var uv := _uv_of(xz)
	var f := _bilinear4(_field_buf, field_px, uv)
	var t := _bilinear4(_trail_buf, trail_px, uv)
	var fade := clampf(1.0 - (_t - t[1]) / maxf(trail_refill_s, 1e-3), 0.0, 1.0)
	var p := clampf(t[0] * fade, 0.0, 1.0)
	var b := clampf(t[2] * fade, 0.0, 1.0)
	return floor_y + lerpf(f[0], residual_m, p) + berm_frac * b * f[0]


func press_at(xz: Vector2) -> float:
	if _trail_buf.is_empty():
		return 0.0
	var t := _bilinear4(_trail_buf, trail_px, _uv_of(xz))
	return clampf(t[0] * clampf(1.0 - (_t - t[1]) / maxf(trail_refill_s, 1e-3), 0.0, 1.0), 0.0, 1.0)


func base_ring_min(centre: Vector2, radius_m: float, samples := 64) -> Dictionary:
	"""The acceptance on object bases: at least 0.10 m of snow ALL ROUND, so no hard line
	shows where the object meets the ground. Reported as the ring's min, not its mean --
	a mean of 0.30 m hides one bare sector, and one bare sector is the whole defect."""
	var lo := INF
	var hi := -INF
	var sum := 0.0
	var lo_ang := 0.0
	for k in samples:
		var a := TAU * float(k) / float(samples)
		var p := centre + Vector2(cos(a), sin(a)) * (radius_m + 0.06)
		var d := depth_at(p)
		sum += d
		if d < lo:
			lo = d
			lo_ang = rad_to_deg(a)
		hi = maxf(hi, d)
	return {"min_m": snappedf(lo, 0.001), "max_m": snappedf(hi, 0.001),
			"mean_m": snappedf(sum / float(samples), 0.001),
			"min_at_deg": snappedf(lo_ang, 0.1)}


func clock() -> float:
	return _t


func advance_clock(s: float) -> void:
	"""Jump the field's own clock forward without simulating the frames between. The trail's
	age is read out of the texture against this clock, so a 40-second-later still costs one
	frame instead of 1200."""
	_t += s
	if _mat != null:
		_mat.set_shader_parameter("now_s", _t)


# =============================================================================
#  MESH + MATERIAL
# =============================================================================
func _build_mesh() -> void:
	var nx: int = maxi(int(round(area.size.x / grid_quad_m)), 8)
	var nz: int = maxi(int(round(area.size.y / grid_quad_m)), 8)
	var pm := PlaneMesh.new()
	pm.size = area.size
	pm.subdivide_width = nx - 1
	pm.subdivide_depth = nz - 1
	pm.orientation = PlaneMesh.FACE_Y
	_mesh_inst = MeshInstance3D.new()
	_mesh_inst.name = "SnowSurface"
	_mesh_inst.mesh = pm
	_mesh_inst.position = Vector3(area.position.x + area.size.x * 0.5, floor_y,
								  area.position.y + area.size.y * 0.5)
	# note 4: the vertex shader lifts the geometry and the computed AABB does not know it
	_mesh_inst.custom_aabb = AABB(
		Vector3(-area.size.x * 0.5, -0.2, -area.size.y * 0.5),
		Vector3(area.size.x, _max_drift + base_depth_m + 1.0, area.size.y))
	_mesh_inst.cast_shadow = (GeometryInstance3D.SHADOW_CASTING_SETTING_ON if cast_shadows
		else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
	_mesh_inst.material_override = _make_material()
	add_child(_mesh_inst)
	_bake["verts"] = nx * nz
	_bake["tris"] = (nx - 1) * (nz - 1) * 2


func _make_material() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = SHADER
	_mat = ShaderMaterial.new()
	_mat.shader = sh
	var fbm := PS.make_fbm_texture(512, 7411, 4)
	# load() and not PaintStack.load_tile(): load_tile does not exist in every version of
	# paint_stack.gd this module has to drop into, and a hard dependency on a helper that
	# appeared mid-run is a parse error in the Barrow rather than a missing texture here.
	var tile: Texture2D = snow_tile
	if tile == null and ResourceLoader.exists("res://textures/barrow/snow.png"):
		tile = load("res://textures/barrow/snow.png")
	_mat.set_shader_parameter("field_tex", _field_tex)
	_mat.set_shader_parameter("trail_tex", _trail_tex)
	_mat.set_shader_parameter("snow_tex", tile)
	_mat.set_shader_parameter("mottle_noise", fbm)
	_mat.set_shader_parameter("wash_noise", fbm)
	_mat.set_shader_parameter("area_min", area.position)
	_mat.set_shader_parameter("area_size", area.size)
	_mat.set_shader_parameter("floor_y", floor_y)
	_mat.set_shader_parameter("base_depth_m", base_depth_m)
	_mat.set_shader_parameter("residual_m", residual_m)
	_mat.set_shader_parameter("berm_frac", berm_frac)
	_mat.set_shader_parameter("refill_s", trail_refill_s)
	_mat.set_shader_parameter("now_s", _t)
	_mat.set_shader_parameter("tile_m", tile_m)
	_mat.set_shader_parameter("detile_warp_m", detile_warp_m)
	_mat.set_shader_parameter("wind_c", wind_dir.x)
	_mat.set_shader_parameter("wind_s", wind_dir.y)
	_mat.set_shader_parameter("press_tint", press_tint)
	_mat.set_shader_parameter("press_tint_amt", press_tint_amt)
	_mat.set_shader_parameter("snow_bright", snow_bright)
	for k in {"band_e0": band_e0, "band_e1": band_e1, "band_soft": band_soft,
			  "band_m0": band_m0, "band_m1": band_m1, "band_m2": band_m2}:
		_mat.set_shader_parameter(k, get(k))
	_mat.set_shader_parameter("trail_texel_m", area.size.x / float(trail_px))
	_mat.set_shader_parameter("taps_4", 1.0 if normal_taps >= 4 else 0.0)
	return _mat


func material() -> ShaderMaterial:
	return _mat


func set_cast_shadows(on: bool) -> void:
	cast_shadows = on
	if _mesh_inst != null:
		_mesh_inst.cast_shadow = (GeometryInstance3D.SHADOW_CASTING_SETTING_ON if on
			else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)


func set_normal_taps(n: int) -> void:
	normal_taps = n
	if _mat != null:
		_mat.set_shader_parameter("taps_4", 1.0 if n >= 4 else 0.0)


func surface() -> MeshInstance3D:
	"""The live mesh. Held rather than looked up by name: setup() is idempotent and the old
	mesh is queue_free()d, which does not take effect until the end of the frame -- so a
	get_node("SnowSurface") in the same frame as a re-bake can hand back the DEAD one, and a
	material pushed onto that is a material pushed onto nothing."""
	return _mesh_inst


func field_texture() -> Texture2D:
	return _field_tex


func trail_texture() -> Texture2D:
	return _trail_tex


func set_visible_snow(on: bool) -> void:
	"""For the A/B frame-cost measurement: the same scene, the same walk, the snow in and
	out. Hidden and not removed, so nothing else about the frame changes."""
	if _mesh_inst != null:
		_mesh_inst.visible = on
	for p in _puffs:
		p.visible = on


# =============================================================================
#  KICKED SNOW
# =============================================================================
func _build_puffs() -> void:
	_flake = PS.make_flake_texture(24)
	for i in puff_pool:
		var g := GPUParticles3D.new()
		g.name = "Puff%d" % i
		g.amount = spray_amount
		g.one_shot = true
		g.emitting = false
		g.explosiveness = 0.92
		g.lifetime = 1.1
		g.local_coords = false
		g.draw_order = GPUParticles3D.DRAW_ORDER_VIEW_DEPTH
		var pm := ParticleProcessMaterial.new()
		pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
		pm.emission_sphere_radius = 0.10
		pm.direction = Vector3(0, 1, 0)
		pm.spread = 55.0
		pm.initial_velocity_min = 0.45
		pm.initial_velocity_max = 1.7
		pm.gravity = Vector3(0, -2.6, 0)
		pm.damping_min = 0.7
		pm.damping_max = 1.6
		pm.scale_min = 0.35
		pm.scale_max = 1.0
		var curve := Curve.new()
		curve.add_point(Vector2(0.0, 0.25))
		curve.add_point(Vector2(0.25, 1.0))
		curve.add_point(Vector2(1.0, 0.0))
		var ct := CurveTexture.new()
		ct.curve = curve
		pm.scale_curve = ct
		var grad := Gradient.new()
		grad.set_color(0, Color(1, 1, 1, 0.85))
		grad.set_color(1, Color(0.93, 0.95, 1.0, 0.0))
		var gt := GradientTexture1D.new()
		gt.gradient = grad
		pm.color_ramp = gt
		g.process_material = pm
		var qm := QuadMesh.new()
		qm.size = Vector2(0.075, 0.075)
		var sm := StandardMaterial3D.new()
		sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		sm.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
		sm.albedo_texture = _flake
		sm.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
		sm.vertex_color_use_as_albedo = true
		sm.disable_receive_shadows = true
		qm.material = sm
		g.draw_pass_1 = qm
		add_child(g)
		_puffs.append(g)


func _puff(at: Vector3, fwd: Vector2, D: float, deep: bool) -> void:
	"""SMALL, NOT A BLIZZARD. amount scales with how much snow the boot actually displaced,
	so walking on the base leaves a wisp and a drift throws a spray."""
	if _puffs.is_empty():
		return
	var g: GPUParticles3D = _puffs[_puff_i]
	_puff_i = (_puff_i + 1) % _puffs.size()
	g.global_position = at
	var pm: ParticleProcessMaterial = g.process_material
	var scale_f := clampf(D / maxf(base_depth_m, 1e-3), 0.6, 4.0)
	g.amount = maxi(int(round(float(puff_amount) * scale_f)), 4)
	if deep:
		g.amount = maxi(g.amount, spray_amount)
		pm.direction = Vector3(fwd.x, 0.95, fwd.y).normalized()
		pm.spread = 42.0
		pm.initial_velocity_max = 2.5
		pm.emission_sphere_radius = 0.20
	else:
		pm.direction = Vector3(0, 1, 0)
		pm.spread = 58.0
		pm.initial_velocity_max = 1.35
		pm.emission_sphere_radius = 0.09
	g.restart()
	g.emitting = true


func _process(_dt: float) -> void:
	if _trail_dirty and _trail_tex != null:
		# coalesced to at most one upload per frame; stamps are gated by stamp_stride_m and
		# plough_step_m so this fires a handful of times a second, not sixty
		_trail_tex.update(Image.create_from_data(trail_px, trail_px, false,
			Image.FORMAT_RGBAF, _trail_buf.to_byte_array()))
		_trail_dirty = false


func upload_stats() -> Dictionary:
	return {"trail_mb": snappedf(float(trail_px * trail_px * 16) / 1048576.0, 0.01),
			"field_mb": snappedf(float(field_px * field_px * 16) / 1048576.0, 0.01),
			"trail_m_per_px": snappedf(area.size.x / float(trail_px), 0.0001)}
