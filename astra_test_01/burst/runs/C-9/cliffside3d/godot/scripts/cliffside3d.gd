extends Node3D
## C-9 R-C9-66 (T7-A) — THE CLIFFSIDE IN TRUE 3D, by camera-projection painting.
##
## The approved H1 cliffside was PAINTED OVER GUIDES rendered from a 3D grey box, so
## the painting and the geometry already share one camera. This projects the approved
## plate back onto that geometry from that same camera. From the game camera the result
## should be the 2D scene pixel for pixel; away from it, it is real 3D — a character
## occludes and is occluded, light is real, and the camera can move.
##
## THE GAME CAMERA IS ORTHOGRAPHIC, and that is not a simplification. The live 2D route
## is a 1920x1080 window scrolling 1:1 over the 5376x4096 ortho canvas (parallax.json:
## limits 2,55 - 5378,4151, view 1920x1080, no zoom). So the 2D "camera" IS the ortho
## canvas camera. Building the 3D game camera as a perspective follow-cam would have
## been a different camera that merely resembles it, and the whole premise of the test
## is that there is only ONE camera. The projector and the view therefore share a frame
## exactly, which is what makes view (a) a like-for-like comparison rather than a
## resemblance.
##
## THE PROJECTION IS LINEAR because that camera is orthographic. No perspective divide,
## no projector frustum: a world point's canvas pixel is
##     x_px = (dot(w, right) - UMIN) * PPM
##     y_px = (VMAX - dot(w, up))   * PPM
## with UMIN/VMAX the v4 pinned frame and PPM the accepted 100.6176 px/m. Those four
## numbers and the basis are read from the BUILDER ITSELF at runtime, not transcribed.

const PPM := 100.617553710938          # cliffside_blockout.PPM_ACCEPTED
const CANVAS := Vector2i(5376, 4096)
const V4_UMIN := -23.2673988342285
const V4_VMAX := 18.5067100524902
const VIEW := Vector2i(1920, 1080)
const FG_BIT := 1                      # the builder's foreground layer
const CHAR_LAYER := 4                  # the character's own visual layer; lights use it

var blockout: Node3D
var level: Node3D
var cam: Camera3D
var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD
var plate_on := true
var _fg: Array[MeshInstance3D] = []
var _proj_mat: ShaderMaterial
var report := {}


func _ready() -> void:
	_build_geometry()
	_read_frame()
	_make_projector()
	_apply_projector()
	_build_camera()
	await _build_world()
	print("[c3d] %d fg meshes | %s" % [_fg.size(), JSON.stringify(report)])


var knight: CharacterBody3D
var _fg_depth := 0.0


func _build_world() -> void:
	report["collision_bodies"] = CliffWorld.add_collision(_fg, self)
	await get_tree().physics_frame
	await get_tree().physics_frame
	var space := get_world_3d().direct_space_state
	# the foreground's own depth, taken at the spawn, so the background cards are placed
	# relative to the thing they sit behind rather than to an arbitrary origin
	var g := CliffWorld.ground_at(space, Vector2(2285.62, 2407.32), right, up, fwd)
	_fg_depth = 20.0 if g.is_empty() else absf((g["position"] as Vector3).dot(fwd) - cam.global_position.dot(fwd))
	report["fg_depth_m"] = snappedf(_fg_depth, 0.01)
	# PROPS ARE ON. The previous session left them out because the cards would not render
	# over the projected terrain, and read that as a depth problem it could not close. It
	# was not a depth problem: the projector shader wrote ALPHA, which made the ENTIRE
	# painted terrain a TRANSPARENT surface -- no depth written, sorted per object -- and
	# the cards, whose shader also wrote ALPHA, joined that same list and lost the sort to
	# meshes the size of a cliff. Both writes are gone; see the note on the projector
	# shader. Measured in tools/probe_card2.gd, confirmed in tools/probe_card3.gd.
	report["props"] = CliffWorld.build_props(self, space, "res://props", right, up, fwd)
	# The backdrop goes just behind the FARTHEST terrain, measured from the meshes rather
	# than picked: every real surface must still win the depth test against it.
	var far_edge := -1e9
	for mi in _fg:
		var ab: AABB = mi.global_transform * mi.get_aabb()
		for c in 8:
			far_edge = maxf(far_edge, ab.get_endpoint(c).dot(fwd))
	report["terrain_far_edge_m"] = snappedf(far_edge, 0.01)
	report["plate_backdrop"] = CliffWorld.build_plate_backdrop(self,
		load("res://plate/plate_v4.png"), Vector2(CANVAS.x, CANVAS.y),
		right, up, fwd, far_edge + 2.0)
	report["background"] = CliffWorld.build_background(self, "res://layers",
		"res://data/parallax.json", right, up, fwd, far_edge + 2.0)
	report["lights"] = CliffWorld.build_lights(self, space, "res://props",
		right, up, fwd, 47.0)
	_build_knight(space)
	look_at_canvas(_aim_px)          # the background exists now; place it for this aim


func _build_knight(space: PhysicsDirectSpaceState3D) -> void:
	var k: CharacterBody3D = preload("res://scripts/knight.gd").new()
	k.name = "Knight"
	# FIGURE SCALE is not 1. The painted world and the painted character disagree about
	# how big a person is: walkable.json says the figure stands 151 canvas px, and a
	# 1.80 m body seen at 52.95 deg through a 100.6 px/m orthographic camera projects to
	# about 125. The art is the authority on how big a character looks in this world, so
	# the body is scaled to the art rather than the art second-guessed. The exact factor
	# is FITTED by measurement in tools/fit_figure.gd and written to data/figure.json;
	# this is the fallback until that has run.
	var fs := 1.0
	if FileAccess.file_exists("res://data/figure.json"):
		var j = JSON.parse_string(FileAccess.get_file_as_string("res://data/figure.json"))
		if typeof(j) == TYPE_DICTIONARY:
			fs = float(j.get("figure_scale", 1.0))
	k.setup(right, up, fwd, fs)
	add_child(k)
	knight = k
	var g := CliffWorld.ground_at(space, Vector2(2285.62, 2407.32), right, up, fwd)
	if not g.is_empty():
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	report["knight_scale"] = fs


# --- geometry: the builder, verbatim -----------------------------------------
func _build_geometry() -> void:
	var src: GDScript = preload("res://scripts/cliffside_blockout.gd")
	blockout = src.new()
	blockout.name = "Blockout"
	blockout.build_only = true
	blockout.layout_override = _stage_layout()
	# Set the version HERE rather than relying on --v4 on the command line. The builder
	# reads its mode from OS.get_cmdline_user_args(), which a double-clicked .app does
	# not supply: it would fall through to v1 geometry and project the v4 plate onto it,
	# producing a scene that renders cleanly and is the wrong shape. The mode is a
	# property of this scene, not of how it was launched.
	blockout._v4 = true
	add_child(blockout)
	level = blockout.get_node_or_null(^"Level")
	assert(level != null, "the builder produced no Level node")
	for m in level.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if (mi.layers & FG_BIT) != 0:
			_fg.append(mi)
	# The builder also makes the greybox BACKGROUND bands and a capsule proxy. Both are
	# replaced here -- the bands by the painted parallax cards, the proxy by the knight --
	# so they are hidden rather than left to show through the painting.
	for m in blockout.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if (mi.layers & FG_BIT) == 0:
			mi.visible = false
	for v in blockout.find_children("*", "SubViewport", true, false):
		(v as SubViewport).render_target_update_mode = SubViewport.UPDATE_DISABLED
	_take_over_environment()


func _take_over_environment() -> void:
	"""The builder's environment is for a GREYBOX and is wrong for a painting.
	
	It sets depth fog at density 0.7 from 40 m to 900 m, to separate its grey background
	bands -- and an orthographic camera is parked far enough back to clear the geometry,
	so every surface in the scene sits deep inside that range. The first capture came out
	uniformly brighter and warmer than the live 2D (mean RGB 178/117/89 against
	134/88/60) and no gamma fitted it, because it was not a colour-space error at all:
	it was 200 m of haze over the whole plate.
	
	The painting ALREADY CONTAINS its haze -- the painter put it there, at the depths
	they chose. Re-fogging it applies the same atmosphere twice. So: fog off, linear
	tonemap, no ambient on the plate. The builder's directional light goes too; lighting
	here is built for the character alone."""
	for we in blockout.find_children("*", "WorldEnvironment", true, false):
		(we as WorldEnvironment).queue_free()
	for dl in blockout.find_children("*", "DirectionalLight3D", true, false):
		(dl as DirectionalLight3D).queue_free()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 0)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1.0, 0.93, 0.86)
	env.ambient_light_energy = 0.40       # reaches the CHARACTER only: the plate and the
	                                      # prop cards are unshaded, so ambient cannot touch
	                                      # them. The one lit thing in the scene is the one
	                                      # thing this fills in.
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.tonemap_white = 1.0
	env.fog_enabled = false
	env.ssao_enabled = false
	env.glow_enabled = false
	var we2 := WorldEnvironment.new()
	we2.name = "Env"
	we2.environment = env
	add_child(we2)


func _stage_layout() -> String:
	"""Put the layout and its zones texture somewhere the BUILDER can open them.
	
	The builder reads both with Image.load_from_file and FileAccess on a real path, which
	is right for an editor run and impossible in an exported .app: res:// lives inside
	the pck and globalize_path hands back a filename that is not on disk. The app built,
	passed every asset fence -- the files ARE in the pck -- and then failed at launch on
	`Error opening file data/v4_zones.png`, which is what "present but not openable"
	looks like. Copying them out to user:// once costs a few hundred kB and makes the
	exported app behave like the editor run it was verified in."""
	var dst := "user://cliff3d"
	DirAccess.make_dir_recursive_absolute(dst)
	# The JSON travels as a FILE (the export preset includes *.json) and the PNG does
	# not: Godot imports images to .ctex, so res://data/v4_zones.png does not exist in an
	# exported build even though the asset fence passed -- the fence matched the string
	# inside the .import entry, which is next to the file and is not the file. So the
	# image is taken through the resource loader and written back out.
	var json_out: String = dst + "/v4_layout.json"
	if not FileAccess.file_exists(json_out):
		var data := FileAccess.get_file_as_bytes("res://data/v4_layout.json")
		if data.is_empty():
			push_error("c3d: cannot read res://data/v4_layout.json")
		var fh := FileAccess.open(json_out, FileAccess.WRITE)
		fh.store_buffer(data)
		fh.close()
	var png_out: String = dst + "/v4_zones.png"
	if not FileAccess.file_exists(png_out):
		var tex: Texture2D = load("res://data/v4_zones.png")
		if tex == null:
			push_error("c3d: cannot load res://data/v4_zones.png")
		else:
			tex.get_image().save_png(png_out)
	return ProjectSettings.globalize_path(dst + "/v4_layout.json")


func _read_frame() -> void:
	# The guide camera's basis, taken from the BUILDER's own _place_cam rather than
	# recomputed from the player_lock constants. Two derivations of one camera is the
	# one thing this test cannot afford: the premise is that the painting and the
	# geometry share a camera, so the projector must use theirs, not a copy of theirs.
	var probe := Camera3D.new()
	add_child(probe)
	blockout._place_cam(probe, Vector3.ZERO, 1.0)
	var b := probe.global_transform.basis
	right = b.x
	up = b.y
	fwd = -b.z
	probe.queue_free()
	report["basis"] = {"right": [right.x, right.y, right.z], "up": [up.x, up.y, up.z],
					   "fwd": [fwd.x, fwd.y, fwd.z]}


# --- the projector ------------------------------------------------------------
func _make_projector() -> void:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
// UNLIT. The plate is a PAINTING: it already carries its own light, its own ambient
// occlusion and its own time of day. Lighting it again would double every shadow the
// painter put there. The character is lit instead -- that is the only thing in this
// scene that is not already painted.
//
// AND IT NEVER ASSIGNS `ALPHA`, WHICH IS LOAD-BEARING AND WAS THE BUG.
//
// This shader used to end every branch with `ALPHA = 1.0;`, which reads as a statement
// that the surface is opaque and is the opposite instruction to Godot. A spatial shader
// that WRITES ALPHA at all is classified TRANSPARENT (unless it also carries
// depth_draw_always, depth_prepass_alpha, or is a scissored BaseMaterial3D). A
// transparent surface WRITES NO DEPTH and is sorted per-OBJECT, back to front, against
// every other transparent surface. So the whole painted terrain -- 14 meshes -- was
// being drawn in the alpha pass with an empty depth buffer, and a prop card (whose own
// shader also wrote ALPHA) joined the same list, lost the per-object sort to meshes the
// size of a cliff, and was painted over. Measured, tools/probe_card2.gd: every variant
// that writes ALPHA draws 0 px; every variant that does not draws 119141 px, the same
// count an opaque StandardMaterial3D gives. It was never a depth tie -- that is why
// disabling the depth TEST did not help either, and why the previous session found that
// only ~80 m of forward bias brought a card back: 80 m is where the card's sort key
// passes the terrain's, not where it wins a depth test.
//
// Removing the write costs nothing visible: ALPHA defaults to 1.0, and the plate
// re-renders to within 7 px of 2,073,600 (0.0003%) of the version that wrote it.
render_mode unshaded, cull_back, depth_draw_opaque;

uniform sampler2D plate : source_color, filter_linear_mipmap;
uniform vec3 axis_right;
uniform vec3 axis_up;
uniform float ppm;
uniform float umin;
uniform float vmax;
uniform vec2 canvas;
uniform vec4 void_color : source_color = vec4(0.10, 0.09, 0.13, 1.0);
uniform float show_void = 0.0;   // 1.0 paints uncovered geometry, for the coverage report
uniform float void_fill = 1.0;   // 0.0 leaves the flat dark, for the before/after

varying vec3 world_pos;

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

vec3 fill_void(vec2 uv) {
	// NEAREST PAINTED TEXEL, searched in the PROJECTOR'S OWN SPACE rather than on screen.
	//
	// A void is a place the guide camera could not see, so the painter left no paint
	// there: a surface facing away, or the inside of a chasm lip. From the play camera
	// those are slivers at silhouette edges -- a texel or two of geometry that the paint
	// stops just short of -- and a flat dark reads there as a seam. Growing the nearest
	// paint outward closes the seam with the colour of the surface it belongs to.
	//
	// Rings outward at LOD 0, and LOD 0 on purpose: a coarser mip averages in the RGB of
	// texels whose alpha is zero, which is whatever the painter left under paint nobody
	// was meant to see -- the same undefined colour that turned the chasm magenta once
	// already. Reach stops at 64 texels. Beyond that a void is not a seam but a genuinely
	// unpainted region, and inventing 200 texels of rock there would be painting, not
	// filling; those keep the flat dark and stay visible in the coverage map.
	if (void_fill < 0.5) return void_color.rgb;
	vec2 p = clamp(uv, vec2(0.0), vec2(1.0));
	vec2 texel = vec2(1.0) / canvas;
	for (int ring = 0; ring < 7; ring++) {
		float r = exp2(float(ring));               // 1, 2, 4 ... 64 texels
		vec3 acc = vec3(0.0);
		float wsum = 0.0;
		for (int i = 0; i < 12; i++) {
			float a = 6.28318530718 * float(i) / 12.0;
			vec2 q = clamp(p + vec2(cos(a), sin(a)) * r * texel, vec2(0.0), vec2(1.0));
			vec4 s = texture(plate, q);
			if (s.a >= 0.02) { acc += s.rgb; wsum += 1.0; }
		}
		if (wsum > 0.0) return acc / wsum;
	}
	return void_color.rgb;
}

void fragment() {
	// The linear map above: world -> guide-camera plane -> canvas pixel -> UV.
	float x_px = (dot(world_pos, axis_right) - umin) * ppm;
	float y_px = (vmax - dot(world_pos, axis_up)) * ppm;
	vec2 uv = vec2(x_px / canvas.x, y_px / canvas.y);
	vec4 c = texture(plate, uv);
	bool outside = uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0;
	if (outside || c.a < 0.02) {
		// NO COVERAGE. The plate is a painting of what the guide camera could see, so
		// anything it could not see has no paint: surfaces that face away, and the
		// insides of the chasm. Discarding leaves a hole in the silhouette; filling
		// with a flat dark keeps the shape and reads as unpainted rock, which is the
		// honest thing for a test whose job is to find exactly these places.
		if (show_void > 0.5) { ALBEDO = vec3(1.0, 0.0, 1.0); }
		else { ALBEDO = fill_void(uv); }
	} else {
		ALBEDO = c.rgb;
	}
}
"""
	_proj_mat = ShaderMaterial.new()
	_proj_mat.shader = sh
	var tex: Texture2D = load("res://plate/plate_v4.png")
	_proj_mat.set_shader_parameter("plate", tex)
	_proj_mat.set_shader_parameter("axis_right", right)
	_proj_mat.set_shader_parameter("axis_up", up)
	_proj_mat.set_shader_parameter("ppm", PPM)
	_proj_mat.set_shader_parameter("umin", V4_UMIN)
	_proj_mat.set_shader_parameter("vmax", V4_VMAX)
	_proj_mat.set_shader_parameter("canvas", Vector2(CANVAS.x, CANVAS.y))


func _apply_projector() -> void:
	for mi in _fg:
		mi.material_override = _proj_mat
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


# --- the game camera ----------------------------------------------------------
func _build_camera() -> void:
	cam = Camera3D.new()
	cam.name = "GameCamera"
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	# The canvas at 100.6176 px/m -- which means the camera's vertical extent must follow
	# the ACTUAL viewport height, not a nominal 1080.
	#
	# It was written as 1080/PPM and that is a scale error waiting for a window manager:
	# a run whose window came back 972 rows tall rendered the whole world 10% small,
	# silently, because an orthographic camera's `size` is metres of screen height and
	# pixels-per-metre is that divided by however many pixels there turn out to be. The
	# live 2D route has no such exposure -- it scrolls a canvas at 1:1 whatever the
	# window is -- so a comparison against it would have been measuring the window.
	cam.size = float(_view_height()) / PPM
	cam.near = 0.05
	cam.far = 600.0
	cam.cull_mask = 0xFFFFF
	add_child(cam)
	cam.current = true
	look_at_canvas(Vector2(2285.62, 2407.32))


var _aim_px := Vector2(2285.62, 2407.32)   # the spawn; where the camera looks


func _view_height() -> int:
	var vp := get_viewport()
	var h: int = vp.get_visible_rect().size.y if vp != null else VIEW.y
	return h if h > 0 else VIEW.y


func look_at_canvas(px: Vector2, yaw_deg := 0.0, zoom := 1.0) -> void:
	"""Point the game camera at a CANVAS PIXEL -- the same coordinates the 2D route and
	walkable.json use, so a place named in one is the same place in the other."""
	var u := V4_UMIN + px.x / PPM
	var v := V4_VMAX - px.y / PPM
	var aim := right * u + up * v
	var f := fwd
	var r := right
	var u3 := up
	if absf(yaw_deg) > 1e-6:
		# Orbit about the WORLD vertical through the aim point, which is the only axis
		# that keeps the horizon level while the view turns.
		var q := Basis(Vector3.UP, deg_to_rad(yaw_deg))
		f = q * fwd
		r = q * right
		u3 = q * up
	cam.size = (float(_view_height()) / PPM) / zoom
	var pos := aim - f * 200.0
	cam.look_at_from_position(pos, aim, Vector3.UP)
	_aim_px = px
	# The painted backdrop is re-placed for THIS aim, by the law measured off the live 2D
	# (see CliffWorld.place_background). It is a compositing device, not geometry: an
	# orthographic camera cannot parallax, so the layers are moved by hand at exactly the
	# rate the 2D moves them.
	CliffWorld.place_background(self, px, aim, r, u3, f)


# --- the occluder fade ---------------------------------------------------------
var fade_enabled := true
var fade_state := {}


func character_box() -> Rect2:
	"""His screen footprint, in canvas pixels, from his COLLISION CAPSULE rather than his
	mesh: the capsule is declared by the character slot, so a swapped-in model gets the
	right box without this scene knowing anything about its skeleton."""
	if knight == null:
		return Rect2()
	var fs: float = knight._figure_scale
	var h: float = float(knight.cfg.get("model_height_m", 1.8)) * fs
	var r := 0.35 * fs
	var o := knight.global_position
	var lo := Vector2(1e9, 1e9)
	var hi := Vector2(-1e9, -1e9)
	for i in 8:
		var p := o + Vector3(r if (i & 1) else -r,
							 h if (i & 2) else 0.0,
							 r if (i & 4) else -r)
		var c := CliffWorld.canvas_of(p, right, up)
		lo = Vector2(minf(lo.x, c.x), minf(lo.y, c.y))
		hi = Vector2(maxf(hi.x, c.x), maxf(hi.y, c.y))
	return Rect2(lo, hi - lo)


func _process(dt: float) -> void:
	if knight == null:
		return
	fade_state = CliffWorld.update_fade(self, character_box(),
		knight.global_position.dot(fwd), fwd, dt, fade_enabled)


func settle_fade() -> void:
	"""Snap the ease to its target. The capture tools call this so a measurement is of the
	settled state and not of however far 0.2 s of easing had got by the frame it grabbed."""
	if knight == null:
		return
	fade_state = CliffWorld.update_fade(self, character_box(),
		knight.global_position.dot(fwd), fwd, 999.0, fade_enabled)


func set_fade_enabled(on: bool) -> void:
	fade_enabled = on
	settle_fade()


func canvas_to_world(px: Vector2, depth_m := 0.0) -> Vector3:
	return right * (V4_UMIN + px.x / PPM) + up * (V4_VMAX - px.y / PPM) + fwd * depth_m


func set_plate(on: bool) -> void:
	plate_on = on
	for mi in _fg:
		mi.material_override = _proj_mat if on else null


func show_void(on: bool) -> void:
	_proj_mat.set_shader_parameter("show_void", 1.0 if on else 0.0)


func set_void_fill(on: bool) -> void:
	"""Nearest-painted-texel fill for uncovered geometry. Off shows the flat dark the
	coverage report was measured against."""
	_proj_mat.set_shader_parameter("void_fill", 1.0 if on else 0.0)


func _unhandled_input(e: InputEvent) -> void:
	if e.is_action_pressed("plate_toggle"):
		set_plate(not plate_on)
