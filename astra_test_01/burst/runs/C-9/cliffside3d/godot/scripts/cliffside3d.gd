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
const PITCH_COS := 0.602462407085      # the guide camera's pitch: a vertical metre spends this on screen

var blockout: Node3D
var level: Node3D
var cam: Camera3D
var right := Vector3.RIGHT
var up := Vector3.UP
var fwd := Vector3.FORWARD
var plate_on := true
var _fg: Array[MeshInstance3D] = []
var _proj_mat: ShaderMaterial
var _proj_mat_lit: ShaderMaterial
var lit := false
var _terrain_ink: Array[MeshInstance3D] = []
var report := {}

# --- T9: the world built the way the character was built ----------------------
const ALBEDO_PLATE := "res://plate/plate_v4_albedo.png"
const PROPS3D_MANIFEST := "res://data/props3d.json"
var _albedo_tex: Texture2D = null          # null until the repaint lands
var _albedo_on := true                     # honoured only in lit mode
var _props3d_on := true                    # honoured only in lit mode
var _props3d: Dictionary = {}              # prop name -> Node3D of the real model
var _props3d_report: Dictionary = {}
var _post_boxes: Array[MeshInstance3D] = []   # the blockout's 1.20 m rail-post boxes
var _ink_skipped: Array[String] = []          # meshes with a rim: the outline pass cannot serve them
var _ink_built := false                       # the outline is built once, not once per L press


func _ready() -> void:
	_build_geometry()
	_read_frame()
	_relief_walls()
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
	_build_props3d(space)
	report["props3d"] = _props3d_report
	_build_knight(space)
	look_at_canvas(_aim_px)          # the background exists now; place it for this aim
	if knight != null:
		var steps0: Array = knight.cfg.get("scale_steps", [])
		var want0: float = float(knight.cfg.get("scale_default_painted", _fig_painted))
		for i in steps0.size():
			if absf(float(steps0[i]) - want0) < 1e-6:
				_size_step = i
		knight.set_figure_scale(want0)
	_build_hud()


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
	_fig_painted = fs


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


# --- T9-1c: real relief on the cliff walls -------------------------------------
const RELIEF_AMPLITUDE_M := 2.5
const RELIEF_TAPER_M := 3.0


func _relief_walls() -> Dictionary:
	"""Give the cliff faces normals that mean something.

	THE DISPLACEMENT IS ALONG THE VIEW DIRECTION, NOT THE SURFACE NORMAL, and that is the
	whole reason this can be done without disturbing anything. Under an orthographic camera
	a point's screen position is (dot(w, right), dot(w, up)); `fwd` is orthogonal to both,
	so moving a vertex along it changes NEITHER. The silhouette is untouched to the pixel,
	and the projector -- which maps world to canvas through those same two axes -- keeps
	painting every vertex exactly the texel it painted before. What changes is depth, and
	the normals that follow from it. That is the entire content of T9-1c.

	Displacing along the surface normal would have been the obvious move and would have
	slid the paint across the rock, which is the one thing the whole test forbids.

	The wall is not the single flat face I called it in the T9-0 report: it is 73,630
	triangles in 38 bands. Its defect is that it is an EXTRUDED OUTLINE, so every normal is
	horizontal and a low key can only graze it. The existing vertices are dense enough --
	about 0.3 m across, 1 m down -- to carry metre-scale relief without subdivision, which
	also means the topology, and so the boundary edges, are untouched.

	Tapered to zero at the top and bottom of each wall: the top edge is shared with the flat
	landmass surface, and pushing it back along the view would open a crack at the rim."""
	var out := {}
	# --no-relief leaves the walls as the builder made them, so the same capture tool can
	# shoot the before and the after without two builds of the app.
	if OS.get_cmdline_user_args().has("--no-relief"):
		report["relief"] = {"disabled": true}
		return out
	var relief: Image = null
	if ResourceLoader.exists("res://data/relief_v4.png"):
		relief = (load("res://data/relief_v4.png") as Texture2D).get_image()
	if relief == null:
		report["relief"] = {"error": "no relief_v4.png"}
		return out
	var rw := float(relief.get_width())
	var rh := float(relief.get_height())
	for mi in _fg:
		if not String(mi.name).ends_with("_wall"):
			continue
		var m := mi.mesh
		var arrays := m.surface_get_arrays(0)
		var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var lo := 1e9
		var hi := -1e9
		for v in verts:
			lo = minf(lo, v.y)
			hi = maxf(hi, v.y)
		var moved := 0
		var maxd := 0.0
		var sum := 0.0
		var xf := mi.global_transform
		for i in verts.size():
			var w: Vector3 = xf * verts[i]
			var cx := (w.dot(right) - V4_UMIN) * PPM / float(CANVAS.x) * rw
			var cy := (V4_VMAX - w.dot(up)) * PPM / float(CANVAS.y) * rh
			if cx < 0.0 or cy < 0.0 or cx >= rw or cy >= rh:
				continue
			var g: float = relief.get_pixel(int(cx), int(cy)).r * 2.0 - 1.0
			# zero at the rim and at the foot, full in between
			var taper: float = clampf((verts[i].y - lo) / RELIEF_TAPER_M, 0.0, 1.0) \
				* clampf((hi - verts[i].y) / RELIEF_TAPER_M, 0.0, 1.0)
			var d: float = g * RELIEF_AMPLITUDE_M * taper
			if absf(d) > 0.0005:
				moved += 1
				maxd = maxf(maxd, absf(d))
				sum += absf(d)
			# fwd is a world direction; the mesh is in its own space
			verts[i] = verts[i] + (xf.basis.inverse() * (fwd * d))
		arrays[Mesh.ARRAY_VERTEX] = verts
		arrays[Mesh.ARRAY_NORMAL] = null        # recomputed from the new surface
		arrays[Mesh.ARRAY_TANGENT] = null
		var nm := ArrayMesh.new()
		nm.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		var st := SurfaceTool.new()
		st.create_from(nm, 0)
		st.generate_normals()
		mi.mesh = st.commit()
		out[String(mi.name)] = {"vertices": verts.size(), "displaced": moved,
			"max_abs_m": snappedf(maxd, 0.001),
			"mean_abs_m": snappedf(sum / maxf(float(moved), 1.0), 0.001)}
	report["relief"] = {"amplitude_m": RELIEF_AMPLITUDE_M, "taper_m": RELIEF_TAPER_M,
						"walls": out}
	return out


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
	# THE LIT TWIN. Same projection, same void fill, same everything -- but SHADED, so the
	# painted plate becomes ALBEDO under a real sun instead of carrying its own light.
	# `unshaded` is a render_mode and cannot be switched at run time, so it is two
	# materials and the L key swaps them. The plate already has its light painted in, so
	# this DOUBLE-LIGHTS by construction; that is what T9-0 exists to look at.
	var sh_lit := Shader.new()
	sh_lit.code = sh.code.replace("render_mode unshaded, cull_back, depth_draw_opaque;",
		"render_mode cull_back, depth_draw_opaque;").replace(
		"\t\tALBEDO = c.rgb;\n\t}", "\t\tALBEDO = c.rgb;\n\t}\n\tROUGHNESS = 0.94;\n\tMETALLIC = 0.0;")
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
	_proj_mat_lit = ShaderMaterial.new()
	_proj_mat_lit.shader = sh_lit
	for pnm in ["plate", "axis_right", "axis_up", "ppm", "umin", "vmax", "canvas"]:
		_proj_mat_lit.set_shader_parameter(pnm, _proj_mat.get_shader_parameter(pnm))
	# T9-1b: THE ALBEDO PLATE, and it goes on the LIT PROJECTOR ONLY.
	#
	# Not on `_proj_mat`, because painted mode must stay the thing Matt played. And not on
	# the plate BACKDROP either, which is a separate quad built in _build_world with its own
	# explicit load: the backdrop carries the 7.35% of this frame that is painted plate with
	# no geometry under it -- the chasm's cloud bank and the haze on its far lip -- and its
	# shader is `unshaded` in both modes (world.gd:410), so that paint is never double-lit
	# and has nothing to be relieved of. De-lighting a cloud only flattens it.
	if ResourceLoader.exists(ALBEDO_PLATE):
		_albedo_tex = load(ALBEDO_PLATE)
		print("[c3d] albedo plate found: %s" % ALBEDO_PLATE)
	else:
		print("[c3d] no albedo plate at %s -- lit mode uses the painted plate" % ALBEDO_PLATE)


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


# --- playing it ----------------------------------------------------------------
const CAM_OFFSET := Vector2(-2, -55)      # the 2D route's own camera offset from the player
const FADE_STEPS := [0.35, 0.50, 1.0]
var _fade_step := 0
var _fig_painted := 1.25177951388889
var _size_step := 0
var _yaw := 0.0
var _hud: Label


func _process(dt: float) -> void:
	if knight == null:
		return
	# THE CAMERA FOLLOWS HIM. It did not: look_at_canvas was called once at build and the
	# view never moved again, so walking two seconds in any direction left the frame. The
	# offset is the 2D route's own, so the player sits where the 2D puts him.
	_yaw = clampf(_yaw + (Input.get_action_strength("orbit_right")
		- Input.get_action_strength("orbit_left")) * 45.0 * dt, -25.0, 25.0)
	look_at_canvas(CliffWorld.canvas_of(knight.global_position, right, up) + CAM_OFFSET, _yaw)
	fade_state = CliffWorld.update_fade(self, character_box(),
		knight.global_position.dot(fwd), fwd, dt, fade_enabled)
	_update_hud()


func _build_hud() -> void:
	"""One line along the bottom, in the 2D route's register: a dark strip, small light
	mono. It is the only thing on screen that is not the painting, so it stays one line."""
	var layer := CanvasLayer.new()
	layer.name = "HUD"
	add_child(layer)
	var bar := ColorRect.new()
	bar.color = Color(0.055, 0.043, 0.063, 0.72)
	bar.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bar.offset_top = -26.0
	bar.offset_bottom = 0.0
	layer.add_child(bar)
	_hud = Label.new()
	_hud.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_hud.offset_top = -24.0
	_hud.offset_bottom = -2.0
	_hud.offset_left = 10.0
	_hud.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	_hud.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_hud.add_theme_font_size_override("font_size", 14)
	_hud.add_theme_color_override("font_color", Color(0.90, 0.88, 0.84))
	layer.add_child(_hud)
	_update_hud()


func _update_hud() -> void:
	if _hud == null:
		return
	var n := 0
	var total := 0
	var nm := "-"
	if knight != null:
		n = knight.gear_stack
		total = knight.gear_stack_count()
		var names: Array = knight.cfg.get("gear_stack_names", [])
		if n < names.size():
			nm = String(names[n])
	var f: float = CliffWorld.fade_min
	var fs := "off" if f >= 0.999 else ("%d%%" % int(round(f * 100.0)))
	_hud.text = ("Arrows/WASD move  ·  Shift run  ·  Space/click attack  ·  "
		+ "G gear (%d/%d: %s)  ·  F tree fade (%s)  ·  L world (%s)  ·  [ ] size (%.2f)  ·  Q/E camera  ·  P plate"
		% [n + 1, total, nm, fs, "lit" if lit else "painted",
		   knight._figure_scale if knight != null else 1.0])


func _build_props3d(space: PhysicsDirectSpaceState3D) -> void:
	"""T9-1a: the slice's props as REAL MODELS, standing on the terrain at TRUE scale.

	A card is a photograph of a prop with the painter's light baked into it. Lit, it keeps
	that light and takes the sun's as well, which is why T9-0 recorded the props reading
	'flat and dark next to a lit figure'. These stand up, catch the same sun he catches,
	and throw their own shadows.

	TRUE SCALE is the point and it is not free. The four painted post cards are 104-110
	canvas px; the blockout post they stand on is 1.20 m, which is 72.7 px. Measured in
	tools/probe_t9_scale.gd: the worst stub of painted post left standing above a true-scale
	model is 37.3 px. That is why the albedo repaint takes the painted posts out -- and why
	the blockout's own post boxes are hidden here, since a modelled post occupies the space
	they were standing in.

	Scale is set from the MODEL'S OWN AABB against a target in metres, never from whatever
	the exporter wrote: Meshy shipped this run a 0.01 object scale and it read as a correct
	model until something was measured next to it."""
	_props3d_report = {"manifest": PROPS3D_MANIFEST, "built": 0, "missing": [], "props": {}}
	if not FileAccess.file_exists(PROPS3D_MANIFEST):
		_props3d_report["status"] = "no manifest -- cards everywhere"
		return
	var data = JSON.parse_string(FileAccess.get_file_as_string(PROPS3D_MANIFEST))
	if typeof(data) != TYPE_DICTIONARY:
		_props3d_report["status"] = "manifest unreadable"
		return
	var models: Dictionary = data.get("models", {})
	var insts: Dictionary = data.get("instances", {})
	var props := get_node_or_null(^"Props")
	if props == null:
		_props3d_report["status"] = "no Props node"
		return
	var holder := Node3D.new()
	holder.name = "Props3D"
	add_child(holder)

	var flat := right
	flat.y = 0.0
	flat = flat.normalized()
	var n_axis := flat.cross(Vector3.UP)
	var grounds := {}

	for pname in insts:
		var inst: Dictionary = insts[pname]
		var mid := String(inst.get("model", ""))
		if not models.has(mid):
			_props3d_report["missing"].append("%s: no model '%s'" % [pname, mid])
			continue
		var spec: Dictionary = models[mid]
		var path := String(spec.get("glb", ""))
		if not ResourceLoader.exists(path):
			_props3d_report["missing"].append("%s: %s not on disk" % [pname, path])
			continue
		var card := props.get_node_or_null(NodePath(pname)) as MeshInstance3D
		if card == null:
			_props3d_report["missing"].append("%s: no card to replace" % pname)
			continue
		var anchor_px: Vector2 = card.get_meta("anchor_px")

		var node: Node3D = (load(path) as PackedScene).instantiate()
		node.name = pname
		holder.add_child(node)
		# TWO AABBs, IN TWO FRAMES, FOR TWO DIFFERENT QUESTIONS -- and using one for both
		# is wrong in a way that renders perfectly.
		#   SIZE is measured UNROTATED. Godot's AABB is world-axis-aligned, so a square post
		#   turned 45 degrees reports a box sqrt(2) wider than the post is: forcing THAT to
		#   the blockout's 0.22 m would build a post 0.156 m thick.
		#   PLACEMENT is measured AFTER the turn, because where a prop's centre and its
		#   lowest point land is a fact about the turned object.
		node.rotation = Vector3.ZERO
		var ab := _node_aabb(node)
		if ab.size.y <= 0.0 or ab.size.x <= 0.0:
			_props3d_report["missing"].append("%s: empty AABB" % pname)
			node.queue_free()
			continue
		# UN-FORESHORTEN. The model sheets were drawn from the painted sprites, and a
		# sprite's vertical extent is the object's height times cos(pitch) = 0.602 -- so the
		# painter drew squat objects and the generator faithfully built squat models. The
		# rail post is the check, because it is the one prop whose true size is known
		# independently (cliffside_blockout.gd:659): scaled to 1.20 m tall it is 0.402 m
		# thick as built and 0.242 m after this stretch, against the blockout's 0.220. The
		# stump and the snag agree. The rope does NOT and is flagged false in the manifest:
		# it was drawn from 25 degrees above by instruction rather than copied off a sprite,
		# and a flat object's screen height is its depth times sin(pitch).
		var ys := 1.0 / PITCH_COS if bool(spec.get("pitch_correct", false)) else 1.0
		var axis := String(spec.get("axis", "height"))
		var target := float(spec.get("height_m", 1.0))
		var s: float = target / (ab.size.y * ys if axis == "height"
								 else maxf(ab.size.x, ab.size.z))
		node.scale = Vector3(s, s * ys, s)
		ab = _node_aabb(node)
		# a forced cross-section, where the blockout has its own number for one
		var wm = spec.get("width_m", null)
		var pre_w := maxf(ab.size.x, ab.size.z)
		if wm != null and pre_w > 0.0:
			var k: float = float(wm) / pre_w
			node.scale = Vector3(node.scale.x * k, node.scale.y, node.scale.z * k)
		node.rotation = Vector3(0.0, deg_to_rad(float(spec.get("yaw_deg", 0.0))
											   + float(inst.get("yaw_deg", 0.0))), 0.0)
		ab = _node_aabb(node)

		var base: Vector3
		var perch := String(inst.get("perch_on", ""))
		if perch != "":
			# The raven stands on a POST, not on the ground under it, and the post is
			# 1.20 m now instead of the card's 1.72 -- so a perch height is not optional
			# decoration, it is the difference between a bird on a rail and a bird in
			# the air. The perch's ground is looked up rather than read out of `grounds`:
			# reading the cache makes this depend on the manifest's key ORDER, which is a
			# dependency nothing declares and nothing checks, and which fails silently by
			# putting the bird on the floor.
			var pc := props.get_node_or_null(NodePath(perch)) as MeshInstance3D
			var ppx: Vector2 = pc.get_meta("anchor_px") if pc != null else anchor_px
			var ph := CliffWorld.ground_at(space, ppx, right, up, fwd)
			base = (ph["position"] if not ph.is_empty()
					else CliffWorld.canvas_to_plane(ppx, right, up)) \
				   + Vector3.UP * float(inst.get("perch_height_m", 1.2))
		else:
			var hit := CliffWorld.ground_at(space, anchor_px, right, up, fwd)
			base = hit["position"] if not hit.is_empty() else CliffWorld.canvas_to_plane(anchor_px, right, up)
			grounds[pname] = base
		# plant it: AABB bottom on the ground point, AABB centre over the anchor
		var c := ab.position + ab.size * 0.5
		node.global_position = base + Vector3(node.global_position.x - c.x,
											  node.global_position.y - ab.position.y,
											  node.global_position.z - c.z)
		for m in node.find_children("*", "MeshInstance3D", true, false):
			var mi := m as MeshInstance3D
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
			mi.layers = FG_BIT
		node.visible = false                       # painted mode is the default
		_props3d[pname] = node
		var fin := _node_aabb(node)
		_props3d_report["props"][pname] = {
			"model": mid, "target_m": target, "axis": axis,
			"aabb_m": [snappedf(fin.size.x, 0.001), snappedf(fin.size.y, 0.001),
					   snappedf(fin.size.z, 0.001)],
			"canvas_px_tall": snappedf(fin.size.y * PITCH_COS * PPM, 0.1),
			"card_canvas_px_tall": snappedf((card.mesh as QuadMesh).size.y * PITCH_COS * PPM, 0.1),
			"pitch_corrected": bool(spec.get("pitch_correct", false)),
			"width_before_override_m": snappedf(pre_w, 0.001),
			"width_forced_m": wm,
			"scale_applied": snappedf(s, 0.0001)}
		_props3d_report["built"] += 1

	for m in level.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		# MATCHED BY SIZE, because the NAME IS NOT THERE. The builder asks for all four
		# boxes to be called "bridge_post"; Godot keeps the name for the first and gives
		# the other three "@MeshInstance3D@9", "@10", "@11" -- it does not append a number
		# to the requested name, it DISCARDS the requested name. So `begins_with` found
		# exactly one of four and reported "blockout_post_boxes: 1", and `contains` found
		# the same one: the second guess failed for the first guess's reason, because both
		# guessed at a name instead of looking. Three grey boxes would have been left
		# standing inside three of the new posts.
		#
		# The meta does not separate them either -- posts and planks both carry
		# class "bridge". Their SIZE does, and it is the thing that makes them rail posts:
		# cliffside_blockout.gd:659 builds them 0.22 x 1.20 x 0.22.
		var bm := mi.mesh as BoxMesh
		if bm != null and absf(bm.size.y - 1.2) < 1e-3 \
				and absf(bm.size.x - 0.22) < 1e-3 and absf(bm.size.z - 0.22) < 1e-3:
			_post_boxes.append(mi)
	_props3d_report["blockout_post_boxes"] = _post_boxes.size()
	_props3d_report["status"] = "ok"


func _node_aabb(n: Node3D) -> AABB:
	var out := AABB()
	var first := true
	for m in n.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var ab: AABB = mi.global_transform * mi.get_aabb()
		out = ab if first else out.merge(ab)
		first = false
	return out


func use_albedo_plate(on: bool) -> void:
	_albedo_on = on
	_apply_lit_sources()


func use_props3d(on: bool) -> void:
	_props3d_on = on
	_apply_lit_sources()


func albedo_plate_in_use() -> String:
	if _albedo_tex == null:
		return "<none: painted plate>"
	return ALBEDO_PLATE if (lit and _albedo_on) else "res://plate/plate_v4.png"


func props3d_report() -> Dictionary:
	return _props3d_report


func _apply_lit_sources() -> void:
	"""Which plate the lit projector samples, and which props are standing.

	Both are honoured ONLY in lit mode. Painted mode is the state Matt has played and
	nothing here may reach it."""
	var want_albedo: bool = lit and _albedo_on and _albedo_tex != null
	if _proj_mat_lit != null:
		_proj_mat_lit.set_shader_parameter("plate",
			_albedo_tex if want_albedo else _proj_mat.get_shader_parameter("plate"))
	var want_3d: bool = lit and _props3d_on
	var props := get_node_or_null(^"Props")
	for pname in _props3d:
		(_props3d[pname] as Node3D).visible = want_3d
		if props != null:
			var card := props.get_node_or_null(NodePath(pname)) as MeshInstance3D
			if card != null:
				card.visible = not want_3d
	for mi in _post_boxes:
		mi.visible = not want_3d


func set_lit(on: bool) -> void:
	"""T9-0: the world lit the way the character is lit.

	Four things move together, because any one of them alone answers nothing:
	  the TERRAIN takes the shaded projector and starts casting and receiving shadows;
	  the SUN stops being masked to the character and lights everything, with shadows on --
	    it is the same direction the painting's own key implies, which build_lights already
	    derived, so the light does not move when the mode does;
	  the PROPS take the shaded card, or a lit man stands among unlit cardboard;
	  the CHARACTER drops to TRUE SCALE 1.0, because a world modelled at true size and a
	    figure at the painting's 1.25178 metric is the mismatch this test is about.
	Painted mode restores all four, so everything already play-tested is untouched."""
	lit = on
	for mi in _fg:
		mi.material_override = _proj_mat_lit if on else _proj_mat
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if on \
			else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var sun := get_node_or_null(^"Lights/Sunset") as DirectionalLight3D
	if sun != null:
		sun.light_cull_mask = 0xFFFFF if on else CHAR_LAYER
		sun.shadow_enabled = on
		sun.light_energy = 1.35 if on else 1.15
		sun.directional_shadow_max_distance = 120.0
	var props := get_node_or_null(^"Props")
	if props != null:
		for c in props.get_children():
			var mi := c as MeshInstance3D
			if mi == null or not mi.has_meta("tex"):
				continue
			var keep: float = float((mi.material_override as ShaderMaterial).get_shader_parameter("fade"))
			mi.material_override = CliffWorld.card_material_lit(mi.get_meta("tex")) if on \
				else CliffWorld.card_material(mi.get_meta("tex"))
			(mi.material_override as ShaderMaterial).set_shader_parameter("fade", keep)
	if knight != null:
		# each mode has its own default size until Matt picks one with [ and ]
		var steps: Array = knight.cfg.get("scale_steps", [])
		var want: float = float(knight.cfg.get("scale_default_lit", 1.0)) if on \
			else float(knight.cfg.get("scale_default_painted", _fig_painted))
		_size_step = 0
		for i in steps.size():
			if absf(float(steps[i]) - want) < 1e-6:
				_size_step = i
		knight.set_figure_scale(want)
	_set_terrain_ink(on)
	# LAST, and after the card swap above: _apply_lit_sources decides which props are
	# standing, and set_lit's own loop has just handed every card a fresh material. Run in
	# the other order and the cards it re-materialised are the ones this hides.
	_apply_lit_sources()
	_update_hud()


func _set_terrain_ink(on: bool) -> void:
	"""The character's ink line, on the terrain. The outline pass offsets VERTEX along the
	normal in MODEL space, and these meshes are already in world metres, so the width is
	the same 1.1 output px the figure uses -- no per-mesh scale to undo. Built once, then
	shown and hidden."""
	if not _ink_built and on:
		_ink_built = true
		var sh := Shader.new()
		sh.code = """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled;
uniform float width_model = 0.011;
uniform vec4 line_color : source_color = vec4(0.055, 0.043, 0.063, 1.0);
void vertex() { VERTEX += normalize(NORMAL) * width_model; }
void fragment() { ALBEDO = line_color.rgb; }
"""
		var mat := ShaderMaterial.new()
		mat.shader = sh
		mat.set_shader_parameter("width_model", 1.1 / PPM)
		for mi in _fg:
			# ONLY ON CLOSED MESHES, and this is the T9 defect, not a refinement.
			#
			# An inflate-and-cull-front outline works because the hull's BACK faces are
			# hidden by the real mesh everywhere except at its silhouette. That argument
			# needs the mesh to have an inside. The cliff walls are open, single-sided
			# extruded skirts: their faces all point one way, so from the far side the hull
			# is not a rim around the surface, it IS the surface -- drawn flat, unshaded,
			# 1 cm proud of the real one, and winning the depth test.
			#
			# Measured: 348,743 pixels of the lit bridge frame, 16.8% of it, were EXACTLY
			# RGB(14,11,16) -- this shader's own line_color -- and turning the pass off took
			# near-black from 18.99% to 3.37%. That is 15.62 of the 18.99 points that T9-0
			# raised as double-lighting, that T9-1c tried to fix with real cliff normals,
			# and that T9-1b was commissioned to fix with an albedo repaint. None of them
			# could move it: an unshaded pass drawn over the top is not lighting, which is
			# exactly why shadows off, sun doubled and relief all measured as no-change.
			#
			# THE TEST IS "DOES THIS SURFACE HAVE A BOUNDARY", and the cheap substitute
			# for it does not work. The first version summed area-weighted face normals and
			# called a mesh closed when they cancelled -- which the cliff walls do, because
			# each is a skirt running ALL THE WAY AROUND its landmass and so faces outward
			# in every horizontal direction at once. It scored near_landmass_wall at 0.001,
			# "closed", and skipping the two meshes it did flag changed the frame by nothing
			# at all. Isolated one ink mesh at a time (tools/probe_ink.gd),
			# near_landmass_wall_ink paints 161,277 px -- 7.78% of the frame -- and every
			# other ink mesh paints zero.
			#
			# A tube is the case that breaks the outline and the case that cancels: no
			# thickness, so cull_front removes the near shell instead of hiding anything,
			# and what is left is the INSIDE of the far shell, inflated 1 cm, unoccluded,
			# flat. Boundary edges are what distinguishes a tube from a box, so that is
			# what gets counted.
			if _has_boundary(mi.mesh):
				_ink_skipped.append(String(mi.name))
				continue
			var o := MeshInstance3D.new()
			o.name = mi.name + "_ink"
			o.mesh = mi.mesh
			mi.add_child(o)
			o.global_transform = mi.global_transform
			o.material_override = mat
			o.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			_terrain_ink.append(o)
	if on and not _ink_skipped.is_empty():
		report["terrain_ink_skipped_open_meshes"] = _ink_skipped
	for o in _terrain_ink:
		o.visible = on


func _has_boundary(mesh: Mesh) -> bool:
	"""True if any edge belongs to exactly one triangle -- i.e. the surface has a rim.

	WELDED BY POSITION, not by index, and that is not a detail. Godot's BoxMesh -- every
	plank and every rail post here -- carries 24 vertices for 8 corners, because flat
	normals and per-face UVs need the corners split. Counting edges on INDICES therefore
	finds every edge used exactly once and calls a solid box open. The first version did
	precisely that and reported all fourteen meshes open, which switched the outline off
	across the entire scene: the frame's numbers came out right, for the wrong reason, and
	the style would have quietly left the build.

	Quantising to 0.1 mm welds the split corners back together and leaves genuinely
	separate vertices apart."""
	if mesh == null:
		return false
	var seen := {}
	for s in mesh.get_surface_count():
		var arr := mesh.surface_get_arrays(s)
		if arr.is_empty():
			continue
		var v: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var idx = arr[Mesh.ARRAY_INDEX]
		var n: int = idx.size() if idx != null else v.size()
		var weld := {}
		var canon := PackedInt32Array()
		canon.resize(v.size())
		for i in v.size():
			var q := Vector3i(roundi(v[i].x * 10000.0), roundi(v[i].y * 10000.0),
							  roundi(v[i].z * 10000.0))
			if not weld.has(q):
				weld[q] = weld.size()
			canon[i] = int(weld[q])
		var i2 := 0
		while i2 + 2 < n:
			for e in 3:
				var a: int = canon[idx[i2 + e] if idx != null else i2 + e]
				var b: int = canon[idx[i2 + (e + 1) % 3] if idx != null else i2 + (e + 1) % 3]
				if a == b:
					continue
				var k: int = (mini(a, b) << 32) | maxi(a, b)
				seen[k] = int(seen.get(k, 0)) + 1
			i2 += 3
	for k in seen:
		if int(seen[k]) != 2:
			return true
	return false


func step_size(d: int) -> void:
	"""[ and ]: 1.00 true, 1.10, 1.25178 sprite-matched. Matt picks his own size by playing
	rather than by being told one, which is the only way this particular question gets
	settled -- the painted world and the painted figure agree at 1.25178 and the blockout
	geometry is at true scale, so there is no single number that is right about both."""
	if knight == null:
		return
	var steps: Array = knight.cfg.get("scale_steps", [])
	if steps.is_empty():
		return
	_size_step = clampi(_size_step + d, 0, steps.size() - 1)
	knight.set_figure_scale(float(steps[_size_step]))
	_update_hud()


func cycle_fade() -> void:
	_fade_step = (_fade_step + 1) % FADE_STEPS.size()
	CliffWorld.fade_min = float(FADE_STEPS[_fade_step])
	settle_fade()
	_update_hud()


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
	elif e.is_action_pressed("gear_cycle") and knight != null:
		knight.cycle_gear()
		_update_hud()
	elif e.is_action_pressed("fade_cycle"):
		cycle_fade()
	elif e.is_action_pressed("lit_toggle"):
		set_lit(not lit)
	elif e.is_action_pressed("size_down"):
		step_size(-1)
	elif e.is_action_pressed("size_up"):
		step_size(1)
