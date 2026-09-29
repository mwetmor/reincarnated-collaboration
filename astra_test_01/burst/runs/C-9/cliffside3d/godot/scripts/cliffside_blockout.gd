extends Node3D
## cliffside_blockout.gd — CHECKPOINT 1 of the cliffside HITL build (gandalf plan
## `agentic_orchestration/gandalf/notes/2026-09-13-cliffside-scene-hitl-plan.md`,
## ruling R-C3-42). A GREYBOX: primitives + flat colours only, no art assets.
##
## Run (windowed; SubViewport readback needs a Metal surface):
##   /Applications/Godot.app/Contents/MacOS/Godot --path ~/Games/reincarnated-godot \
##     --resolution 640x360 res://scenes/cliffside_blockout.tscn -- --out /abs/dir
##
## Writes into --out: the renders listed in the checkpoint-1 task, `work/` clean
## plates (proxy hidden) for the PIL composites, and `blockout_meta.json`
## (camera numbers, measured silhouettes, projected ground points).
##
## CAMERA: the ratified GD `player_lock` construction, transplanted from
## `scripts/wr2_playback.gd:_pl_build_lock` via `scripts/kc2_cpb_clip.gd:_playerlock_pose`
## (constants below copied verbatim, pin checked at k = 1). The dolly k scales the
## offset vector only — rotation, lens and anchor are untouched.
##
## k IS SOLVED BY MEASUREMENT, NOT FORMULA: a proxy-only mask pass (4x supersampled,
## transparent background, MSAA) is rendered through the same camera and the
## capsule's projected silhouette height is read off the image; k is iterated until
## that height equals the target fraction of a 1080-row frame.

# ---- player_lock operands (verbatim from kc2_cpb_clip.gd:312-325) -------------
const PL_PITCH_DEG := 52.95354112560294
const PL_FOV_V_DEG := 31.78610183061007
const PL_FOCAL_PX_1080 := 1896.5577238618157
const PL_GX_PLAYER := 54.47290422329346
const PL_ANCHOR_FX := 0.5010416666666667
const PL_ANCHOR_FY := 0.5509259259259259
const PL_ASPECT := 16.0 / 9.0
const PL_YAW_DEG := 47.0
const PL_PIN_OFFSET := Vector3(14.7262048721313, 28.3970108032227, 13.7826108932495)
const PL_PIN_Z_PLAYER_M := 34.8165340347471
const PL_PIN_TOL_M := 1.0e-4   # float32 Vector3 in this build; kc2's 1e-5 is on its own print

const RES := Vector2i(1920, 1080)
const MASK_SS := 4
const PROXY_H := 1.75
const PROXY_R := 0.30
const GROUND_Y := 0.02          # path surface height; the follow point sits on it
const RUNGS := [0.120, 0.125, 0.130]
const FG_BIT := 1               # foreground (path, landmass, rocks, bridge)
const BG_BIT := 16              # background depth bands + sky card (proxies use bits 2, 4, 8)

# ---- palette (sRGB) ----------------------------------------------------------
const C_PATH := Color(0.76, 0.62, 0.45)
const C_CLIFF := Color(0.55, 0.55, 0.56)
const C_NEAR_ROCK := Color(0.30, 0.30, 0.32)
const C_BRIDGE := Color(0.45, 0.28, 0.14)
const C_FALLS_OUT := Color(1.0, 0.0, 1.0)
const C_VALLEY := Color(0.45, 0.47, 0.22)
const C_FOREST := Color(0.33, 0.13, 0.10)
const C_RUINS := Color(0.91, 0.80, 0.50)
const C_SKY_TOP := Color(1.00, 0.55, 0.20)   # orange (top of card = toward the unseen horizon)
const C_SKY_BOT := Color(0.45, 0.25, 0.62)  # violet (bottom of card)
const C_SKY_ID := Color(0.62, 0.36, 0.55)
const C_PROXY := Color(0.20, 0.85, 0.95)
const HAZE := Color(0.93, 0.62, 0.50)
const HAZE_MAX := 0.7

# ---- layout (metres, LOCAL screen-aligned frame: +x = screen right, -z = screen up) ----
const PATH_CTRL := [
	Vector2(-17.0, 15.5), Vector2(-11.5, 12.0), Vector2(-6.5, 7.5), Vector2(-1.5, 2.0),
	Vector2(3.5, -2.5), Vector2(8.0, -7.0), Vector2(12.5, -11.8), Vector2(16.5, -16.3),
]
const LIP := 1.2                 # rock lip between path far edge and the cliff edge
const CLIFF_DROP := 40.0
const NEAR_W := 30.0             # landmass width beyond the path's near edge
const CHASM_LEN := 10.0
const CHASM_END_TAIL := 3.0      # path after the chasm
const PLANKS := 6
const FALLS_OUT_INDEX := 3
const BRIDGE_W := 3.0
# background band tuning (see _build_background header)
const VALLEY_W_FAR := 45.0
const DEP_FOREST := [45.5, 42.0]
const DEP_RUINS := [40.6, 39.9]

# ---- v2 (R-C3-44): the vista plateau juts TOWARD the camera ------------------
# Matt accepted the 12.5 % rung at checkpoint 1; v2 reuses that k and the ortho
# px/m verbatim (they are rulings now, not re-solved). `--v2` switches layout and
# render set; without it the file builds and renders v1 exactly as before.
const K_ACCEPTED := 0.541385974272702          # R-C3-44, rung 12.5 %
const PPM_ACCEPTED := 100.617553710938         # v1 measured, plateau proxy, screen-x
const V2_BAY_BEFORE := 14.0                   # near-side landmass removed over s_plat-14 .. s_plat+9
const V2_BAY_AFTER := 9.0
const V2_PROM_SKEW := 0.7                      # tilts the promontory axis from lower-right to nearly screen-down (its tip face looks at the camera)
const V2_PROM := [[-2.0, -7.0], [7.0, -7.0], [9.0, -5.0], [9.0, 5.0], [7.0, 7.0], [-2.0, 7.0]]   # (along, across) m
const V2_SPAWN_ALONG := 5.0
const V2_CUT_DEPTH := 7.0                      # chunk guides keep cliff face down to 7 m below the rim

# ---- v3 (R-C3-48): continuous massif to 20 m; padded canvas; depth-below-rim map; scene data ----
# Layout, camera and px/m are v2's. The ortho canvas keeps v2's top-left origin (so every v2
# canvas coordinate is still valid) and is rendered at the padded size, not padded afterwards,
# because faces continuing to 20 m project below v2's 3980-row edge.
const V3_CUT_DEPTH := 20.0
const V3_CANVAS := Vector2i(5376, 4096)
const V3_MASSIF_TOP := -20.0                   # the bay is a notch in rock, not a slot through it

# ---- v4 (R-C3-54 / R-C3-55): organic geometry from scripts/cliffside_v4_layout.py ----------
# The shapes (rim polygons, fluted walls to 40 m, boulder meshes, top-surface zone texture) are
# designed in Python in this file's LOCAL frame and read from --layout; this file builds, lights and
# renders them. Camera, k, px/m and the canvas top-left are v3's, pinned (not re-derived from bounds).
const V4_UMIN := -23.2673988342285
const V4_VMAX := 18.5067100524902

var _out := ""
var _mats: Array = []            # [{mat, lit_color, id_color, gradient}]
var _vp: SubViewport
var _cam: Camera3D
var _mvp: SubViewport
var _mcam: Camera3D
var _light: DirectionalLight3D
var _env: Environment
var _level: Node3D
var _sky: MeshInstance3D
var _pts: PackedVector2Array     # resampled centreline (local)
var _ss: PackedFloat32Array      # arc length at each sample
var _L := 0.0
var _s_plat := 0.0
var _s_c0 := 0.0
var _s_c1 := 0.0
var _proxies: Array = []         # [{name, ground(world), layer_bit}]
var _offset1 := Vector3.ZERO     # k = 1 offset (pinned)
var _fwd := Vector3.ZERO
var _meta := {}
var _v2 := false
var _v3 := false
var _v4 := false
var _layout_path := ""
var _layout := {}
var _v4_spawn := Vector2.ZERO
var _plateau_inner := PackedVector2Array()
var _boxes: Array = []            # [{name, cls, center(xz), size, yaw}]
var _planks: Array = []           # [{index, falls_out, corners(xz)}]
var _bridge_ab: Array = []
var _prom_o := Vector2.ZERO
var _prom_a := Vector2.ZERO
var _prom_b := Vector2.ZERO


## C-9 R-C9-66 (T7-A): a VERBATIM copy of reincarnated-godot/scripts/cliffside_blockout.gd
## at v4.2 (22e1241), with one addition: `build_only`. Set it before add_child() and the
## node builds the geometry and stops, instead of running the capture pipeline.
##
## Copied rather than imported because the dispatch builds in runs/C-9/cliffside3d/ and
## the live repo stays untouched; copied VERBATIM rather than re-implemented because the
## whole premise of the test is that the painting and the geometry share one camera, and
## a re-implementation is a second camera that merely resembles the first.
var build_only := false
var layout_override := ""


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			_out = args[i + 1]
		if args[i] == "--v2":
			_v2 = true
		if args[i] == "--v3":
			_v2 = true
			_v3 = true
		if args[i] == "--v4":
			_v4 = true
		if args[i] == "--layout" and i + 1 < args.size():
			_layout_path = args[i + 1]
	if layout_override != "":
		_layout_path = layout_override
	if _out == "":
		_out = ProjectSettings.globalize_path("user://cliffside_blockout")
	DirAccess.make_dir_recursive_absolute(_out + "/work")
	_build_camera_law()
	_build_viewports()
	_build_env()
	_level = Node3D.new()
	_level.name = "Level"
	_level.rotation = Vector3(0.0, deg_to_rad(PL_YAW_DEG), 0.0)   # local +Z == hb (toward camera)
	add_child(_level)
	if _v4:
		_build_v4()
	else:
		_build_path_and_landmass()
		_build_near_rocks()
	_build_bridge()
	_build_proxies()
	_build_background()
	if build_only:
		return
	if _v4:
		_run_v4.call_deferred()
	elif _v3:
		_run_v3.call_deferred()
	elif _v2:
		_run_v2.call_deferred()
	else:
		_run.call_deferred()


# ============================================================================
# CAMERA LAW — wr2_playback.gd:_pl_build_lock, line for line
# ============================================================================
func _build_camera_law() -> void:
	var yaw := deg_to_rad(PL_YAW_DEG)
	var p := deg_to_rad(PL_PITCH_DEG)
	var hb := Vector3(sin(yaw), 0.0, cos(yaw))
	var fwd: Vector3 = (-hb * cos(p) + Vector3.DOWN * sin(p)).normalized()
	var upc: Vector3 = (-hb * sin(p) + Vector3.UP * cos(p)).normalized()
	var rgt: Vector3 = fwd.cross(upc)
	assert(absf(fwd.dot(upc)) < 1.0e-6, "player_lock basis is not orthogonal")
	var zp: float = PL_FOCAL_PX_1080 / PL_GX_PLAYER
	var thv: float = tan(deg_to_rad(PL_FOV_V_DEG) * 0.5)
	var thh: float = thv * PL_ASPECT
	var ndx: float = 2.0 * PL_ANCHOR_FX - 1.0
	var ndy: float = 1.0 - 2.0 * PL_ANCHOR_FY
	var xc: float = ndx * thh * zp
	var yc: float = ndy * thv * zp
	_offset1 = -(rgt * xc + upc * yc + fwd * zp)
	_fwd = fwd
	var pin_delta: float = (_offset1 - PL_PIN_OFFSET).length()
	var zp_delta: float = absf(zp - PL_PIN_Z_PLAYER_M)
	print("[cliff] player_lock k=1 offset (%.10f, %.10f, %.10f) |pin delta| %s m  zp delta %s m" % [
		_offset1.x, _offset1.y, _offset1.z, str(pin_delta), str(zp_delta)])
	if pin_delta >= PL_PIN_TOL_M or zp_delta >= PL_PIN_TOL_M:
		push_error("[cliff] PIN FAIL — offset does not match pl_audit.json")
	_meta["pin"] = {"offset_k1": [_offset1.x, _offset1.y, _offset1.z], "pin_delta_m": pin_delta,
		"zp_delta_m": zp_delta, "ok": pin_delta < PL_PIN_TOL_M and zp_delta < PL_PIN_TOL_M}


func _place_cam(cam: Camera3D, ground: Vector3, k: float) -> void:
	var off := _offset1 * k
	cam.fov = PL_FOV_V_DEG
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = 0.3
	cam.far = 4000.0
	cam.look_at_from_position(ground + off, ground + off + _fwd, Vector3.UP)


func _build_viewports() -> void:
	_vp = SubViewport.new()
	_vp.size = RES
	_vp.msaa_3d = Viewport.MSAA_4X
	_vp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	add_child(_vp)
	_cam = Camera3D.new()
	_vp.add_child(_cam)
	_cam.current = true
	_mvp = SubViewport.new()
	_mvp.size = RES * MASK_SS
	_mvp.msaa_3d = Viewport.MSAA_4X
	_mvp.transparent_bg = true
	_mvp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	add_child(_mvp)
	_mcam = Camera3D.new()
	_mvp.add_child(_mcam)
	_mcam.current = true


func _build_env() -> void:
	_env = Environment.new()
	_env.background_mode = Environment.BG_COLOR
	_env.background_color = Color(0, 0, 0)
	_env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	_env.ambient_light_color = Color(1.0, 0.95, 0.9)
	_env.ambient_light_energy = 0.45
	_env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	# depth haze toward the sunset: begins beyond the foreground (the follow camera's
	# ground is 19-30 m away), so it only separates the background bands. Off in the ID pass.
	_env.fog_enabled = true
	_env.fog_mode = Environment.FOG_MODE_DEPTH
	_env.fog_light_color = HAZE
	_env.fog_density = HAZE_MAX
	_env.fog_depth_begin = 40.0
	_env.fog_depth_end = 900.0
	_env.fog_depth_curve = 0.4
	_env.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = _env
	add_child(we)
	_light = DirectionalLight3D.new()
	_light.light_energy = 1.05
	_light.shadow_enabled = true
	_light.directional_shadow_max_distance = 120.0
	add_child(_light)
	# light travels from screen upper-left toward lower-right and down (local frame)
	var d_local := Vector3(0.62, -0.78, 0.55).normalized()
	var basis := Basis(Vector3.UP, deg_to_rad(PL_YAW_DEG))
	var d_world: Vector3 = basis * d_local
	_light.look_at_from_position(Vector3.ZERO, d_world, Vector3.UP)


# ============================================================================
# MATERIALS
# ============================================================================
func _mat(c: Color, id_c: Color = Color(-1, 0, 0)) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = c
	m.roughness = 1.0
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	_mats.append({"mat": m, "id": c if id_c.r < 0.0 else id_c, "vcol": false})
	return m


func _set_id_mode(on: bool) -> void:
	for e in _mats:
		var m: StandardMaterial3D = e["mat"]
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED if on else BaseMaterial3D.SHADING_MODE_PER_PIXEL
		if e.get("tex", false):
			# zone-textured top: the texture carries both the lit albedo and the ID colours
			m.albedo_color = Color(1, 1, 1)
			m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST if on else BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		elif e["vcol"]:
			m.vertex_color_use_as_albedo = not on
			m.albedo_color = e["id"] if on else Color(1, 1, 1)
		else:
			m.albedo_color = e["id"] if on else (e["lit"] if e.has("lit") else m.albedo_color)
	_light.visible = not on


# ============================================================================
# GEOMETRY HELPERS (local frame)
# ============================================================================
func _add_mesh(st: SurfaceTool, m: Material, nm: String, meta: Dictionary = {}) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = nm
	st.set_material(m)
	mi.mesh = st.commit()
	for key in meta:
		mi.set_meta(key, meta[key])
	_level.add_child(mi)
	return mi


func _quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> void:
	var n := (b - a).cross(d - a).normalized()
	if n.y < -0.01 or (absf(n.y) <= 0.01 and false):
		n = -n
	for v in [a, b, c, a, c, d]:
		st.set_normal(n)
		st.add_vertex(v)


func _wall(st: SurfaceTool, p: Vector2, q: Vector2, y0: float, y1: float, out_dir: Vector2) -> void:
	var a := Vector3(p.x, y1, p.y)
	var b := Vector3(q.x, y1, q.y)
	var c := Vector3(q.x, y0, q.y)
	var d := Vector3(p.x, y0, p.y)
	var n := Vector3(out_dir.x, 0.0, out_dir.y).normalized()
	for v in [a, b, c, a, c, d]:
		st.set_normal(n)
		st.add_vertex(v)


func _catmull(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)


func _sample_centreline() -> void:
	var dense: Array = []
	var n := PATH_CTRL.size()
	for i in n - 1:
		var p0: Vector2 = PATH_CTRL[maxi(i - 1, 0)]
		var p1: Vector2 = PATH_CTRL[i]
		var p2: Vector2 = PATH_CTRL[i + 1]
		var p3: Vector2 = PATH_CTRL[mini(i + 2, n - 1)]
		for j in 40:
			dense.append(_catmull(p0, p1, p2, p3, float(j) / 40.0))
	dense.append(PATH_CTRL[n - 1])
	# resample uniformly at 0.5 m
	var acc := [0.0]
	for i in range(1, dense.size()):
		acc.append(acc[i - 1] + (dense[i] - dense[i - 1]).length())
	_L = acc[acc.size() - 1]
	_pts = PackedVector2Array()
	_ss = PackedFloat32Array()
	var s := 0.0
	var idx := 1
	while s <= _L + 1e-4:
		while idx < acc.size() - 1 and acc[idx] < s:
			idx += 1
		var t: float = (s - acc[idx - 1]) / maxf(acc[idx] - acc[idx - 1], 1e-6)
		_pts.append((dense[idx - 1] as Vector2).lerp(dense[idx], clampf(t, 0.0, 1.0)))
		_ss.append(s)
		s += 0.5


func _c(s: float) -> Vector2:
	# centreline point at arc length s, linearly extrapolated beyond both ends
	if s <= 0.0:
		return _pts[0] + _tan(0.0) * s
	if s >= _L:
		return _pts[_pts.size() - 1] + _tan(_L) * (s - _L)
	var f := s / 0.5
	var i := int(floor(f))
	i = clampi(i, 0, _pts.size() - 2)
	return _pts[i].lerp(_pts[i + 1], f - float(i))


func _tan(s: float) -> Vector2:
	var i := clampi(int(round(clampf(s, 0.0, _L) / 0.5)), 1, _pts.size() - 2)
	return (_pts[i + 1] - _pts[i - 1]).normalized()


func _nfar(s: float) -> Vector2:
	var t := _tan(s)
	return Vector2(t.y, -t.x)      # upper-left side for a lower-left -> upper-right path


func _plateau(s: float) -> float:
	var d := absf(s - _s_plat)
	if d <= 5.0:
		return 1.0
	if d >= 8.5:
		return 0.0
	return 1.0 - smoothstep(5.0, 8.5, d)


func _w0(s: float) -> float:
	return 7.5 + 1.4 * sin(0.33 * s + 0.6)


func _far_off(s: float) -> float:
	if _v2:
		return _w0(s) * 0.5
	return _w0(s) * 0.5 + _plateau(s) * 4.0


func _near_off(s: float) -> float:
	if _v2:
		return _w0(s) * 0.5
	return _w0(s) * 0.5 + _plateau(s) * 1.0


func _in_bay(s: float) -> bool:
	return _v2 and s > _s_plat - V2_BAY_BEFORE and s < _s_plat + V2_BAY_AFTER


func _prom_pt(along: float, across: float) -> Vector2:
	return _prom_o + _prom_a * along + _prom_b * across


## Walls down every edge of a closed top polygon, normals outward.
func _poly_walls(walls: SurfaceTool, poly: PackedVector2Array, y0: float, y1: float = 0.0) -> void:
	var area := 0.0
	for i in poly.size():
		var p0 := poly[i]
		var p1 := poly[(i + 1) % poly.size()]
		area += p0.x * p1.y - p1.x * p0.y
	for i in poly.size():
		var p0 := poly[i]
		var p1 := poly[(i + 1) % poly.size()]
		var d := p1 - p0
		if d.length() < 1e-4:
			continue
		var nrm := Vector2(d.y, -d.x) if area > 0.0 else Vector2(-d.y, d.x)
		_wall(walls, p0, p1, y0, y1, nrm)


# ============================================================================
# PATH + LANDMASS (+ chasm cut)
# ============================================================================
func _build_path_and_landmass() -> void:
	_sample_centreline()
	_s_plat = _L * 0.45
	_s_c1 = _L - CHASM_END_TAIL
	_s_c0 = _s_c1 - CHASM_LEN
	print("[cliff] path centreline length %.2f m; plateau s=%.2f; chasm s=[%.2f, %.2f]" % [_L, _s_plat, _s_c0, _s_c1])
	_meta["layout"] = {"path_length_m": _L, "plateau_s_m": _s_plat, "chasm_s_m": [_s_c0, _s_c1]}
	var m_path := _mat(C_PATH)
	var m_cliff := _mat(C_CLIFF)
	var pieces := [[-7.0, _s_c0], [_s_c1, _L + 8.0]]
	var path_pieces := [[0.0, _s_c0], [_s_c1, _L]]
	for pi in pieces.size():
		var s0: float = pieces[pi][0]
		var s1: float = pieces[pi][1]
		var st := SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		var walls := SurfaceTool.new()
		walls.begin(Mesh.PRIMITIVE_TRIANGLES)
		var poly := PackedVector2Array()
		var s := s0
		while s < s1 - 1e-4:
			var sn := minf(s + 0.5, s1)
			var fa := _c(s) + _nfar(s) * (_far_off(s) + LIP)
			poly.append(fa)
			s = sn
		var fend := _c(s1) + _nfar(s1) * (_far_off(s1) + LIP)
		poly.append(fend)
		var n1 := _c(s1) - _nfar(s1) * (_near_off(s1) + NEAR_W)
		var n0 := _c(s0) - _nfar(s0) * (_near_off(s0) + NEAR_W)
		poly.append(n1)
		var b0 := _s_plat - V2_BAY_BEFORE
		var b1 := _s_plat + V2_BAY_AFTER
		if _v2 and b0 > s0 and b1 < s1:
			# the bay: near-side landmass cut back to a 1.2 m rim so the promontory has void in front
			poly.append(_c(b1) - _nfar(b1) * (_near_off(b1) + NEAR_W))
			var sb := b1
			while sb > b0 - 1e-4:
				poly.append(_c(sb) - _nfar(sb) * (_near_off(sb) + LIP))
				sb -= 0.5
			poly.append(_c(b0) - _nfar(b0) * (_near_off(b0) + NEAR_W))
		poly.append(n0)
		_poly_walls(walls, poly, -CLIFF_DROP)
		if _v3 and pi == 0:
			# continuous rock under the bay: the landmass footprint WITHOUT the bay, from -20 m to the drop
			var base := PackedVector2Array()
			var sq := s0
			while sq < s1 - 1e-4:
				base.append(_c(sq) + _nfar(sq) * (_far_off(sq) + LIP))
				sq = minf(sq + 0.5, s1)
			base.append(fend)
			base.append(n1)
			base.append(n0)
			var bst := SurfaceTool.new()
			bst.begin(Mesh.PRIMITIVE_TRIANGLES)
			for ti in Geometry2D.triangulate_polygon(base):
				bst.set_normal(Vector3.UP)
				bst.add_vertex(Vector3(base[ti].x, V3_MASSIF_TOP, base[ti].y))
			_poly_walls(bst, base, -CLIFF_DROP, V3_MASSIF_TOP)
			_add_mesh(bst, m_cliff, "massif_base_under_bay", {"class": "cliff_rock"})
		var tris := Geometry2D.triangulate_polygon(poly)
		if tris.is_empty():
			push_error("[cliff] landmass polygon %d failed to triangulate" % pi)
		for ti in tris:
			st.set_normal(Vector3.UP)
			st.add_vertex(Vector3(poly[ti].x, 0.0, poly[ti].y))
		_add_mesh(st, m_cliff, "landmass_top_%d" % pi, {"class": "cliff_rock"})
		_add_mesh(walls, m_cliff, "landmass_walls_%d" % pi, {"class": "cliff_rock"})
		# the dirt path on top of it
		var ps0: float = path_pieces[pi][0]
		var ps1: float = path_pieces[pi][1]
		var pst := SurfaceTool.new()
		pst.begin(Mesh.PRIMITIVE_TRIANGLES)
		s = ps0
		while s < ps1 - 1e-4:
			var sn2 := minf(s + 0.5, ps1)
			var a := _c(s) + _nfar(s) * _far_off(s)
			var b := _c(sn2) + _nfar(sn2) * _far_off(sn2)
			var c := _c(sn2) - _nfar(sn2) * _near_off(sn2)
			var d := _c(s) - _nfar(s) * _near_off(s)
			_quad(pst, Vector3(a.x, GROUND_Y, a.y), Vector3(b.x, GROUND_Y, b.y), Vector3(c.x, GROUND_Y, c.y), Vector3(d.x, GROUND_Y, d.y))
			s = sn2
		_add_mesh(pst, m_path, "path_%d" % pi, {"class": "path"})
	if _v2:
		_build_promontory(m_path, m_cliff)


func _build_promontory(m_path: Material, m_cliff: Material) -> void:
	var t := _tan(_s_plat)
	_prom_o = _c(_s_plat)
	_prom_a = (-_nfar(_s_plat) + (-t) * V2_PROM_SKEW).normalized()
	_prom_b = Vector2(_prom_a.y, -_prom_a.x)
	# back corners sit ON the path centreline (s_plat -/+ 7) so the promontory never pokes past the far lip
	var poly := PackedVector2Array()
	poly.append(_c(_s_plat - 7.0))
	for q in V2_PROM.slice(1, 5):
		poly.append(_prom_pt(float(q[0]), float(q[1])))
	poly.append(_c(_s_plat + 7.0))
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for ti in Geometry2D.triangulate_polygon(poly):
		st.set_normal(Vector3.UP)
		st.add_vertex(Vector3(poly[ti].x, 0.0, poly[ti].y))
	_add_mesh(st, m_cliff, "vista_promontory_top", {"class": "cliff_rock"})
	var walls := SurfaceTool.new()
	walls.begin(Mesh.PRIMITIVE_TRIANGLES)
	_poly_walls(walls, poly, -CLIFF_DROP)
	_add_mesh(walls, m_cliff, "vista_promontory_cliff_face", {"class": "cliff_rock"})
	# dirt plateau top, inset by the rim lip
	var inner := PackedVector2Array()
	inner.append(_c(_s_plat - 5.8))
	for q in [[6.4, -5.8], [7.9, -4.3], [7.9, 4.3], [6.4, 5.8]]:
		inner.append(_prom_pt(float(q[0]), float(q[1])))
	inner.append(_c(_s_plat + 5.8))
	_plateau_inner = inner
	var pst := SurfaceTool.new()
	pst.begin(Mesh.PRIMITIVE_TRIANGLES)
	for ti in Geometry2D.triangulate_polygon(inner):
		pst.set_normal(Vector3.UP)
		pst.add_vertex(Vector3(inner[ti].x, GROUND_Y, inner[ti].y))
	_add_mesh(pst, m_path, "vista_plateau_top", {"class": "path"})
	_meta["v2_promontory"] = {"origin_local": [_prom_o.x, _prom_o.y], "axis_local": [_prom_a.x, _prom_a.y],
		"outline_along_across_m": V2_PROM.slice(1, 5), "back_corners": "path centreline at s_plat -/+ 7 m", "bay_s_m": [_s_plat - V2_BAY_BEFORE, _s_plat + V2_BAY_AFTER]}


func _box(center_local: Vector3, size: Vector3, yaw_local: float, m: Material, nm: String, meta: Dictionary = {}) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	mi.material_override = m
	mi.name = nm
	mi.position = center_local
	mi.rotation = Vector3(0.0, yaw_local, 0.0)
	_boxes.append({"name": nm, "cls": String(meta.get("class", "")), "c": Vector2(center_local.x, center_local.z),
		"size": size, "yaw": yaw_local, "falls_out": bool(meta.get("falls_out", false)), "index": int(meta.get("plank_index", -1))})
	for key in meta:
		mi.set_meta(key, meta[key])
	_level.add_child(mi)
	return mi


func _yaw_of(dir: Vector2) -> float:
	# local yaw that maps a box's local +X onto `dir` (x, z)
	return atan2(-dir.y, dir.x)


func _build_near_rocks() -> void:
	var m := _mat(C_NEAR_ROCK)
	# a rock wall run on the near side, then scattered boulders
	var wall_runs := [[3.0, 12.0, 3.2], [25.5, 31.0, 2.4]]
	for r in wall_runs:
		var s: float = r[0]
		while s < float(r[1]) - 0.1:
			var sn := minf(s + 1.8, float(r[1]))
			var sm := (s + sn) * 0.5
			if _in_bay(sm):
				s = sn
				continue
			var p := _c(sm) - _nfar(sm) * (_near_off(sm) + 1.4)
			var hgt: float = float(r[2]) * (0.8 + 0.25 * sin(sm * 2.1))
			_box(Vector3(p.x, hgt * 0.5 - 0.3, p.y), Vector3(sn - s + 0.25, hgt, 1.6), _yaw_of(_tan(sm)), m, "near_rockwall", {"class": "near_rock"})
			s = sn
	var boulders := [[15.0, 2.2, 1.8], [17.5, 3.4, 1.2], [33.0, 1.8, 2.0], [1.0, 2.6, 1.4], [37.0, 3.0, 1.5]]
	for b in boulders:
		var sb: float = b[0]
		if (sb > _s_c0 - 0.5 and sb < _s_c1 + 0.5) or _in_bay(sb):
			continue
		var p2 := _c(sb) - _nfar(sb) * (_near_off(sb) + float(b[1]))
		var sz: float = b[2]
		_box(Vector3(p2.x, sz * 0.45, p2.y), Vector3(sz, sz * 1.1, sz * 0.9), sb * 0.7, m, "near_boulder", {"class": "near_rock"})


func _build_bridge() -> void:
	var m := _mat(C_BRIDGE)
	var mf := _mat(C_FALLS_OUT)
	var a := _c(_s_c0)
	var b := _c(_s_c1)
	var span := (b - a).length()
	var dir := (b - a) / span
	var seg := span / float(PLANKS)
	var yaw := _yaw_of(dir)
	var planks_meta: Array = []
	for i in PLANKS:
		var mid := a + dir * (seg * (float(i) + 0.5))
		var falls := i == FALLS_OUT_INDEX
		_box(Vector3(mid.x, GROUND_Y - 0.09, mid.y), Vector3(seg - 0.08, 0.18, BRIDGE_W), yaw,
			mf if falls else m, "bridge_plank_%d%s" % [i, "_falls_out" if falls else ""],
			{"class": "bridge_plank_falls_out" if falls else "bridge", "falls_out": falls, "plank_index": i})
		planks_meta.append({"index": i, "falls_out": falls, "length_m": seg - 0.08, "width_m": BRIDGE_W})
	var side := Vector2(dir.y, -dir.x)
	_bridge_ab = [a, b, dir, side]
	for endp in [a, b]:
		for sgn in [-1.0, 1.0]:
			var pp: Vector2 = endp + side * (BRIDGE_W * 0.5 + 0.15) * sgn
			_box(Vector3(pp.x, 0.6, pp.y), Vector3(0.22, 1.2, 0.22), yaw, m, "bridge_post", {"class": "bridge"})
	_meta["bridge"] = {"span_m": span, "segments": PLANKS, "falls_out_index": FALLS_OUT_INDEX, "planks": planks_meta}


# ============================================================================
# PROXIES (1.75 m capsules; each on its own render layer so a follow shot can
# isolate the one it follows)
# ============================================================================
func _build_proxies() -> void:
	var m := _mat(C_PROXY)
	var plat := _c(_s_plat) + _nfar(_s_plat) * 1.5
	if _v2:
		plat = _prom_pt(V2_SPAWN_ALONG, 0.0)
	if _v4:
		plat = _v4_spawn
	var defs := [
		["start", _c(4.0)],
		["plateau", plat],
		["bridge_approach", _c(_s_c0 - 2.5)],
	]
	for i in defs.size():
		var pl: Vector2 = defs[i][1]
		var mi := MeshInstance3D.new()
		var cm := CapsuleMesh.new()
		cm.radius = PROXY_R
		cm.height = PROXY_H
		mi.mesh = cm
		mi.material_override = m
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.layers = 1 << (1 + i)
		mi.name = "proxy_" + String(defs[i][0])
		mi.position = Vector3(pl.x, GROUND_Y + PROXY_H * 0.5, pl.y)
		_level.add_child(mi)
		var gw: Vector3 = _level.transform * Vector3(pl.x, GROUND_Y, pl.y)
		_proxies.append({"name": defs[i][0], "ground": gw, "bit": 1 << (1 + i), "local": [pl.x, GROUND_Y, pl.y]})


# ============================================================================
# BACKGROUND DEPTH BANDS
#
# ⚑ GEOMETRY FACT THAT DRIVES THIS SECTION: at pitch 52.95 deg and vertical FOV
#   31.79 deg the TOP edge of the frame looks 37.06 deg BELOW the horizon. The true
#   horizon is never in frame. So a band "150-300 m out" can only be seen if it
#   also sits far BELOW the path. Band elevations are therefore SOLVED: each
#   band edge is dropped until it sits at a chosen depression angle as seen from
#   the plateau follow camera (k = 12.5 % rung). Distances "out" are measured
#   along screen-up (local -z) beyond the cliff edge above the plateau.
# ============================================================================
func _band_y(cam_local: Vector3, z_local: float, depression_deg: float) -> float:
	var horiz := absf(cam_local.z - z_local)
	return cam_local.y - horiz * tan(deg_to_rad(depression_deg))


func _slab(z_near: float, z_far: float, y_near: float, y_far: float, x0: float, x1: float, m: Material, nm: String, cls: String) -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	_quad(st, Vector3(x0, y_far, z_far), Vector3(x1, y_far, z_far), Vector3(x1, y_near, z_near), Vector3(x0, y_near, z_near))
	_add_mesh(st, m, nm, {"class": cls})


func _build_background() -> void:
	var n_before := _level.get_child_count()
	# plateau camera at the 12.5 % rung, estimated k for placement only (bands are
	# far; +-5 % in k moves their angles by well under a degree)
	var k_est := 0.527
	var plat_local: Array = _proxies[1]["local"]
	var inv := _level.transform.affine_inverse()
	var cam_w: Vector3 = (_proxies[1]["ground"] as Vector3) + _offset1 * k_est
	var cam_l: Vector3 = inv * cam_w
	var cliff_z: float = float(plat_local[2]) - 9.0     # cliff edge above the plateau, approx.
	var bands := {}
	# valley floor: 40 m below, parallel to the cliff (strip in the path-perpendicular frame)
	var m_val := _mat(C_VALLEY)
	var u: Vector2 = (PATH_CTRL[PATH_CTRL.size() - 1] - PATH_CTRL[0]).normalized()
	var wn := Vector2(u.y, -u.x)
	var o: Vector2 = PATH_CTRL[0]
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var w_near := -60.0
	var w_far := VALLEY_W_FAR
	var u0 := -120.0
	var u1 := 170.0
	var yv := -CLIFF_DROP
	var A := o + u * u0 + wn * w_near
	var B := o + u * u1 + wn * w_near
	var C := o + u * u1 + wn * w_far
	var D := o + u * u0 + wn * w_far
	_quad(st, Vector3(D.x, yv, D.y), Vector3(C.x, yv, C.y), Vector3(B.x, yv, B.y), Vector3(A.x, yv, A.y))
	# a few low valley mounds so the floor has form
	_add_mesh(st, m_val, "band_valley_floor", {"class": "valley", "band": 1})
	for i in 9:
		var mp := o + u * (-10.0 + 13.0 * float(i)) + wn * (32.0 + 6.0 * sin(float(i) * 1.7))
		_box(Vector3(mp.x, yv + 1.5, mp.y), Vector3(5.0 + 2.0 * sin(i), 3.0 + float(i % 3), 4.0), float(i), m_val, "valley_mound", {"class": "valley", "band": 1})
	bands["valley"] = {"y_m": yv, "w_from_path_line_m": [w_near, w_far], "note": "flat, 40 m below the path, parallel to the cliff"}
	# charred forest: 150-300 m out, solved to 44.0 -> 41.0 deg depression at the plateau camera
	var m_for := _mat(C_FOREST)
	var zf0 := cliff_z - 150.0
	var zf1 := cliff_z - 300.0
	var yf0 := _band_y(cam_l, zf0, DEP_FOREST[0])
	var yf1 := _band_y(cam_l, zf1, DEP_FOREST[1])
	_slab(zf0, zf1, yf0, yf1, -500.0, 500.0, m_for, "band_charred_forest", "forest")
	var n_trees := 70
	for i in n_trees:
		var fx := -380.0 + 760.0 * fmod(float(i) * 0.6180339, 1.0)
		var fz := lerpf(zf0 + 10.0, zf1 - 10.0, fmod(float(i) * 0.4142, 1.0))
		var fy := lerpf(yf0, yf1, (fz - zf0) / (zf1 - zf0))
		var th := 10.0 + 8.0 * fmod(float(i) * 0.731, 1.0)
		_box(Vector3(fx, fy + th * 0.5, fz), Vector3(2.5, th, 2.5), float(i), m_for, "burnt_trunk", {"class": "forest", "band": 2})
	bands["charred_forest"] = {"z_out_m": [150.0, 300.0], "y_m": [yf0, yf1], "depression_deg_at_plateau_cam": DEP_FOREST}
	# destroyed temple ruins: ~400 m out, a few broken columns + walls
	var m_ru := _mat(C_RUINS)
	var zr0 := cliff_z - 380.0
	var zr1 := cliff_z - 430.0
	var yr0 := _band_y(cam_l, zr0, DEP_RUINS[0])
	var yr1 := _band_y(cam_l, zr1, DEP_RUINS[1])
	_slab(zr0, zr1, yr0, yr1, -600.0, 600.0, m_ru, "band_ruins_ground", "ruins")
	var ruins := [
		[-40.0, 0.2, 8.0, 42.0, 8.0], [-18.0, 0.3, 8.0, 30.0, 8.0], [4.0, 0.25, 8.0, 48.0, 8.0],
		[26.0, 0.4, 8.0, 22.0, 8.0], [48.0, 0.3, 8.0, 36.0, 8.0],             # colonnade (one broken short)
		[-80.0, 0.6, 46.0, 18.0, 6.0], [85.0, 0.5, 38.0, 26.0, 6.0],          # broken walls
		[-8.0, 0.8, 60.0, 9.0, 12.0], [120.0, 0.35, 9.0, 14.0, 9.0], [-130.0, 0.45, 9.0, 27.0, 9.0],
	]
	for r in ruins:
		var rz := lerpf(zr0, zr1, float(r[1]))
		var ry := lerpf(yr0, yr1, float(r[1]))
		_box(Vector3(float(r[0]), ry + float(r[3]) * 0.5, rz), Vector3(float(r[2]), float(r[3]), float(r[4])), 0.0, m_ru, "ruin_block", {"class": "ruins", "band": 3})
	bands["temple_ruins"] = {"z_out_m": [380.0, 430.0], "y_m": [yr0, yr1], "depression_deg_at_plateau_cam": DEP_RUINS}
	# sky backdrop: camera-facing card at the far plane (1500 m along forward), orange -> violet
	var sky_m := StandardMaterial3D.new()
	sky_m.vertex_color_use_as_albedo = true
	sky_m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	sky_m.cull_mode = BaseMaterial3D.CULL_DISABLED
	sky_m.disable_fog = true
	_mats.append({"mat": sky_m, "id": C_SKY_ID, "vcol": true})
	var p := deg_to_rad(PL_PITCH_DEG)
	var yaw := deg_to_rad(PL_YAW_DEG)
	var hb := Vector3(sin(yaw), 0.0, cos(yaw))
	var upc: Vector3 = (-hb * sin(p) + Vector3.UP * cos(p)).normalized()
	var rgt: Vector3 = _fwd.cross(upc)
	var ctr: Vector3 = cam_w + _fwd * 1500.0
	var hh := 1500.0 * tan(deg_to_rad(PL_FOV_V_DEG) * 0.5) * 1.25
	var hw := hh * PL_ASPECT * 1.25
	var sst := SurfaceTool.new()
	sst.begin(Mesh.PRIMITIVE_TRIANGLES)
	var tl := ctr - rgt * hw + upc * hh
	var tr := ctr + rgt * hw + upc * hh
	var br := ctr + rgt * hw - upc * hh
	var bl := ctr - rgt * hw - upc * hh
	var verts := [[tl, C_SKY_TOP], [tr, C_SKY_TOP], [br, C_SKY_BOT], [tl, C_SKY_TOP], [br, C_SKY_BOT], [bl, C_SKY_BOT]]
	for v in verts:
		sst.set_color(v[1])
		sst.set_normal(-_fwd)
		sst.add_vertex(v[0])
	sst.set_material(sky_m)
	_sky = MeshInstance3D.new()
	_sky.name = "band_sky_backdrop"
	_sky.mesh = sst.commit()
	_sky.set_meta("class", "sky")
	_sky.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_sky)   # world space, not level-local
	bands["sky"] = {"distance_along_forward_m": 1500.0, "note": "camera-facing card, gradient orange (top, toward the horizon above frame) -> violet (bottom)"}
	_meta["bands"] = bands
	_sky.layers = BG_BIT
	for ci in range(n_before, _level.get_child_count()):
		(_level.get_child(ci) as VisualInstance3D).layers = BG_BIT
	# store lit colours for the ID toggle
	for e in _mats:
		if not e["vcol"]:
			e["lit"] = (e["mat"] as StandardMaterial3D).albedo_color


# ============================================================================
# RENDER + MEASURE
# ============================================================================
func _render(vp: SubViewport) -> Image:
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	for i in 4:
		await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	vp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	return img


func _measure(pi: int, k: float, ortho_ppm: float = 0.0) -> Dictionary:
	if ortho_ppm > 0.0:
		var g: Vector3 = _proxies[pi]["ground"]
		_mcam.projection = Camera3D.PROJECTION_ORTHOGONAL
		_mcam.size = float(RES.y) / ortho_ppm
		_mcam.keep_aspect = Camera3D.KEEP_HEIGHT
		_mcam.near = 1.0
		_mcam.far = 200.0
		_mcam.look_at_from_position(g - _fwd * 60.0, g - _fwd * 60.0 + _fwd, Vector3.UP)
	else:
		_mcam.projection = Camera3D.PROJECTION_PERSPECTIVE
		_place_cam(_mcam, _proxies[pi]["ground"], k)
	_mcam.cull_mask = _proxies[pi]["bit"]
	var img: Image = await _render(_mvp)
	var r := img.get_used_rect()
	var top_a := 0.0
	var bot_a := 0.0
	for x in range(r.position.x, r.end.x):
		top_a = maxf(top_a, img.get_pixel(x, r.position.y).a)
		bot_a = maxf(bot_a, img.get_pixel(x, r.end.y - 1).a)
	var h_ss: float = float(r.size.y - 2) + top_a + bot_a
	var ss := float(MASK_SS)
	return {
		"height_px_1080": h_ss / ss,
		"height_frac": h_ss / float(RES.y * MASK_SS),
		"bbox_px_1080": [r.position.x / ss, r.position.y / ss, r.end.x / ss, r.end.y / ss],
		"mask_rows_4x": r.size.y,
	}


func _persp_ppm(g: Vector3) -> Dictionary:
	var b := _cam.global_transform.basis
	var r := Vector3(b.x.x, 0.0, b.x.z).normalized()
	var fh := Vector3(-b.z.x, 0.0, -b.z.z).normalized()
	var dx := (_cam.unproject_position(g + r * 0.5) - _cam.unproject_position(g - r * 0.5)).length()
	var dy := absf(_cam.unproject_position(g + fh * 0.5).y - _cam.unproject_position(g - fh * 0.5).y)
	var up := absf(_cam.unproject_position(g + Vector3.UP * 0.5).y - _cam.unproject_position(g - Vector3.UP * 0.5).y)
	return {"screen_x_px_per_m": dx, "screen_y_px_per_ground_m": dy, "screen_y_px_per_vertical_m": up,
		"ground_world": [g.x, g.y, g.z]}


## Orthographic canvas of the FOREGROUND (layer FG_BIT only), same basis as
## player_lock, transparent background, one image. Bounds are the path +
## cliff lip + near-side rock band over s in [-4, L+4], projected onto the
## camera's right/up axes.
func _ortho_canvas(ppm: float, file: String, mask_cut_y: float = NAN, pad: Vector2i = Vector2i.ZERO, depth_encode: bool = false) -> Dictionary:
	_place_cam(_cam, _proxies[1]["ground"], 1.0)
	var b := _cam.global_transform.basis
	var rgt := b.x
	var upc := b.y
	var fwd := -b.z
	var umin := INF
	var umax := -INF
	var vmin := INF
	var vmax := -INF
	var dsum := 0.0
	var n := 0
	var s := -4.0
	while s <= _L + 4.0:
		var far := _c(s) + _nfar(s) * (_far_off(s) + LIP + 1.0)
		var near := _c(s) - _nfar(s) * (_near_off(s) + 7.0)
		for q in [Vector3(far.x, 0.0, far.y), Vector3(near.x, 0.0, near.y), Vector3(near.x, 4.0, near.y), Vector3(far.x, 1.3, far.y)]:
			var w: Vector3 = _level.transform * q
			umin = minf(umin, w.dot(rgt))
			umax = maxf(umax, w.dot(rgt))
			vmin = minf(vmin, w.dot(upc))
			vmax = maxf(vmax, w.dot(upc))
			dsum += w.dot(fwd)
			n += 1
		s += 1.0
	if _v2:
		for q in V2_PROM:
			for yy in [0.0, -(V2_CUT_DEPTH + 2.0)]:
				var w2: Vector3 = _level.transform * Vector3(_prom_pt(float(q[0]), float(q[1])).x, yy, _prom_pt(float(q[0]), float(q[1])).y)
				umin = minf(umin, w2.dot(rgt))
				umax = maxf(umax, w2.dot(rgt))
				vmin = minf(vmin, w2.dot(upc))
				vmax = maxf(vmax, w2.dot(upc))
	if _v4:
		umin = V4_UMIN
		vmax = V4_VMAX
	var W := int(ceil((umax - umin) * ppm))
	var H := int(ceil((vmax - vmin) * ppm))
	var uc := (umin + umax) * 0.5
	var vc := (vmin + vmax) * 0.5
	if pad != Vector2i.ZERO:
		# same top-left as the unpadded canvas; extend right/bottom
		W = pad.x
		H = pad.y
		uc = umin + float(W) * 0.5 / ppm
		vc = vmax - float(H) * 0.5 / ppm
	var dc := dsum / float(n)
	var ovp := SubViewport.new()
	ovp.size = Vector2i(W, H)
	ovp.msaa_3d = Viewport.MSAA_4X
	ovp.transparent_bg = true
	ovp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	add_child(ovp)
	var ocam := Camera3D.new()
	ovp.add_child(ocam)
	ocam.current = true
	ocam.projection = Camera3D.PROJECTION_ORTHOGONAL
	ocam.keep_aspect = Camera3D.KEEP_HEIGHT
	ocam.size = float(H) / ppm
	ocam.near = 1.0
	ocam.far = 260.0
	ocam.cull_mask = FG_BIT
	var pos := rgt * uc + upc * vc + fwd * (dc - 80.0)
	ocam.look_at_from_position(pos, pos + fwd, Vector3.UP)
	var masking := not is_nan(mask_cut_y)
	var saved := []
	if depth_encode:
		# metres below rim (rim = y 0 for every face in this level) -> millimetres, 16 bits in R (hi) G (lo),
		# B = 255 marks "a surface was hit". Albedo is pre-linearised so the viewport's linear->sRGB output
		# lands on the exact bytes; verified on read-back by the chunk script (B == 255, gradients).
		ovp.msaa_3d = Viewport.MSAA_DISABLED
		var dsh := Shader.new()
		dsh.code = "shader_type spatial;\nrender_mode unshaded, cull_disabled, fog_disabled;\nvarying float wy;\nvoid vertex() { wy = (MODEL_MATRIX * vec4(VERTEX, 1.0)).y; }\nvec3 s2l(vec3 c) { return mix(c / 12.92, pow((c + vec3(0.055)) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }\nvoid fragment() { float mm = clamp(floor(max(0.0, -wy) * 1000.0 + 0.5), 0.0, 65534.0); float hi = floor(mm / 256.0); float lo = mm - hi * 256.0; ALBEDO = s2l(vec3(hi / 255.0, lo / 255.0, 1.0)); }\n"
		var dmat := ShaderMaterial.new()
		dmat.shader = dsh
		for ch in _level.get_children():
			if ch is GeometryInstance3D and (ch as VisualInstance3D).layers == FG_BIT:
				saved.append([ch, (ch as GeometryInstance3D).material_override])
				(ch as GeometryInstance3D).material_override = dmat
	if masking:
		ovp.msaa_3d = Viewport.MSAA_DISABLED
		var sh := Shader.new()
		sh.code = "shader_type spatial;\nrender_mode unshaded, cull_disabled, fog_disabled;\nuniform float cut_y;\nvarying float wy;\nvoid vertex() { wy = (MODEL_MATRIX * vec4(VERTEX, 1.0)).y; }\nvoid fragment() { if (wy < cut_y) { discard; } ALBEDO = vec3(1.0); }\n"
		var smat := ShaderMaterial.new()
		smat.shader = sh
		smat.set_shader_parameter("cut_y", mask_cut_y)
		for ch in _level.get_children():
			if ch is GeometryInstance3D and (ch as VisualInstance3D).layers == FG_BIT:
				saved.append([ch, (ch as GeometryInstance3D).material_override])
				(ch as GeometryInstance3D).material_override = smat
	var old_sd := _light.directional_shadow_max_distance
	var old_fog := _env.fog_enabled
	_light.directional_shadow_max_distance = 200.0
	_env.fog_enabled = false      # the haze is a perspective depth cue; the canvas is the paint guide
	var img: Image = await _render(ovp)
	_light.directional_shadow_max_distance = old_sd
	_env.fog_enabled = old_fog
	for sv in saved:
		(sv[0] as GeometryInstance3D).material_override = sv[1]
	img.save_png(_out + "/" + file)
	var proxies_px := {}
	for pr in _proxies:
		var gp := ocam.unproject_position(pr["ground"])
		proxies_px[pr["name"]] = [gp.x, gp.y]
	var chk := ocam.unproject_position(_level.transform * Vector3(0.0, 0.0, 0.0))
	var keypts := {}
	if _v2:
		for q in V2_PROM:
			var pp := _prom_pt(float(q[0]), float(q[1]))
			var tag := "%s_%s" % [str(q[0]), str(q[1])]
			keypts["rim_" + tag] = _xy(ocam.unproject_position(_level.transform * Vector3(pp.x, 0.0, pp.y)))
			keypts["cut_" + tag] = _xy(ocam.unproject_position(_level.transform * Vector3(pp.x, -V2_CUT_DEPTH, pp.y)))
		var sp := _prom_pt(V2_SPAWN_ALONG, 0.0)
		keypts["keeper_spawn"] = _xy(ocam.unproject_position(_level.transform * Vector3(sp.x, GROUND_Y, sp.y)))
		for sv2 in [4.0, 8.0, 12.0, _s_plat - 4.0, _s_plat]:
			var cp := _c(sv2)
			keypts["path_centre_s%.1f" % sv2] = _xy(ocam.unproject_position(_level.transform * Vector3(cp.x, GROUND_Y, cp.y)))
	ovp.queue_free()
	return {"file": file, "size_px": [W, H], "px_per_m_screen_x": ppm,
		"px_per_ground_m_screen_y": ppm * sin(deg_to_rad(PL_PITCH_DEG)),
		"px_per_vertical_m_screen_y": ppm * cos(deg_to_rad(PL_PITCH_DEG)),
		"ortho_size_m": float(H) / ppm, "proxy_ground_canvas_px": proxies_px,
		"camera_pos": [pos.x, pos.y, pos.z], "tiles": "single image (viewport limit not reached)",
		"level_origin_canvas_px": [chk.x, chk.y], "key_points_canvas_px": keypts,
		"frame": {"rgt": [rgt.x, rgt.y, rgt.z], "upc": [upc.x, upc.y, upc.z], "umin": umin, "vmax": vmax}}


func _cam_numbers(k: float) -> Dictionary:
	var off := _offset1 * k
	return {"k": k, "offset_m": [off.x, off.y, off.z], "stand_off_m": off.length(), "height_m": off.y}


func _run() -> void:
	# ---- solve k per rung, at the plateau proxy -----------------------------
	var rungs := []
	var k := 0.53
	for target in RUNGS:
		var it := []
		for n in 8:
			var mres: Dictionary = await _measure(1, k)
			var h: float = mres["height_frac"]
			it.append({"k": k, "height_frac": h})
			if absf(h - target) * RES.y < 0.05:
				break
			k = k * h / target
		var final: Dictionary = await _measure(1, k)
		var row := _cam_numbers(k)
		row["target_frac"] = target
		row["measured"] = final
		row["iterations"] = it
		rungs.append(row)
		print("[cliff] rung %.1f %%: k=%.6f stand-off %.4f m height %.4f m measured %.3f px (%.4f %%)" % [
			target * 100.0, k, row["stand_off_m"], row["height_m"], final["height_px_1080"], final["height_frac"] * 100.0])
	_meta["rungs"] = rungs
	var k125: float = rungs[1]["k"]
	# ---- follow shots at the 12.5 % rung ------------------------------------
	var shots := []
	for pi in _proxies.size():
		var g: Vector3 = _proxies[pi]["ground"]
		_place_cam(_cam, g, k125)
		var meas: Dictionary = await _measure(pi, k125)
		_cam.cull_mask = FG_BIT | BG_BIT | int(_proxies[pi]["bit"])
		var img: Image = await _render(_vp)
		var name_png := "%02d_follow_%s_k12p5.png" % [pi + 1, _proxies[pi]["name"]]
		img.save_png(_out + "/" + name_png)
		_cam.cull_mask = FG_BIT | BG_BIT
		var plate: Image = await _render(_vp)
		plate.save_png(_out + "/work/plate_%s_k12p5.png" % _proxies[pi]["name"])
		var gp := _cam.unproject_position(g)
		var shot := {"file": name_png, "position": _proxies[pi]["name"], "ground_world": [g.x, g.y, g.z],
			"ground_px": [gp.x, gp.y], "anchor_frac": [gp.x / RES.x, gp.y / RES.y], "silhouette": meas}
		if pi == 1:
			# a second ground point 1.4 m to screen-right of the plateau proxy (for the walk frame)
			var rgt := _cam.global_transform.basis.x
			var g2 := g + Vector3(rgt.x, 0.0, rgt.z).normalized() * 1.4
			var gp2 := _cam.unproject_position(g2)
			shot["beside_ground_px"] = [gp2.x, gp2.y]
		shots.append(shot)
		print("[cliff] %s  ground px (%.2f, %.2f)  silhouette %.3f px" % [name_png, gp.x, gp.y, meas["height_px_1080"]])
	# the 12.0 / 13.0 rung stills at the plateau
	for ri in [0, 2]:
		var kr: float = rungs[ri]["k"]
		_place_cam(_cam, _proxies[1]["ground"], kr)
		_cam.cull_mask = FG_BIT | BG_BIT | int(_proxies[1]["bit"])
		var imr: Image = await _render(_vp)
		var nr := "rung_plateau_%s.png" % ("12p0" if ri == 0 else "13p0")
		imr.save_png(_out + "/" + nr)
		rungs[ri]["file"] = nr
	_meta["shots"] = shots
	# ---- overview: offset x3, same angles, framed on the path's bbox centre --
	var lo := Vector2(INF, INF)
	var hi := Vector2(-INF, -INF)
	for pt in _pts:
		lo = Vector2(minf(lo.x, pt.x), minf(lo.y, pt.y))
		hi = Vector2(maxf(hi.x, pt.x), maxf(hi.y, pt.y))
	var mid := (lo + hi) * 0.5
	var gmid: Vector3 = _level.transform * Vector3(mid.x, GROUND_Y, mid.y)
	_place_cam(_cam, gmid, k125 * 3.0)
	_cam.cull_mask = 0xFFFFF
	var imo: Image = await _render(_vp)
	imo.save_png(_out + "/04_overview_x3.png")
	var ov := _cam_numbers(k125 * 3.0)
	ov["file"] = "04_overview_x3.png"
	ov["follow_point_local"] = [mid.x, GROUND_Y, mid.y]
	_meta["overview"] = ov
	# ---- far layers only, from the plateau follow camera ---------------------
	_place_cam(_cam, _proxies[1]["ground"], k125)
	_cam.cull_mask = BG_BIT
	var imfar: Image = await _render(_vp)
	imfar.save_png(_out + "/06_far_layers_only_plateau_k12p5.png")
	_meta["far_layers"] = {"file": "06_far_layers_only_plateau_k12p5.png", "camera": "plateau follow, k 12.5 % rung"}
	# ---- px/m of the 12.5 % follow render at the proxy, and across the frame --
	_place_cam(_cam, _proxies[1]["ground"], k125)
	var ppm := _persp_ppm(_proxies[1]["ground"])
	var rows := {}
	for ry in [0.0, 297.5, 595.0, 837.5, 1079.0]:
		var o3 := _cam.project_ray_origin(Vector2(962.0, ry))
		var n3 := _cam.project_ray_normal(Vector2(962.0, ry))
		var t := (GROUND_Y - o3.y) / n3.y
		rows["row_%d" % int(ry)] = _persp_ppm(o3 + n3 * t)
	_meta["ppm"] = {"perspective_at_plateau_proxy": ppm, "perspective_ground_at_rows_x962": rows}
	var ppm_x: float = ppm["screen_x_px_per_m"]
	print("[cliff] perspective px/m at plateau proxy: x %.4f  ground-depth (screen y) %.4f" % [ppm_x, ppm["screen_y_px_per_ground_m"]])
	# ---- ORTHO LEVEL CANVAS (foreground only), same yaw/pitch, px/m matched --
	var oc: Dictionary = await _ortho_canvas(ppm_x, "07_ortho_canvas_shaded.png")
	var om: Dictionary = await _measure(1, 0.0, ppm_x)
	oc["proxy_silhouette_plateau_ortho"] = om
	_meta["ortho_canvas"] = oc
	print("[cliff] ortho canvas %dx%d px at %.4f px/m; capsule in ortho %.3f px" % [oc["size_px"][0], oc["size_px"][1], ppm_x, om["height_px_1080"]])
	# ---- layer-ID pass at the plateau ----------------------------------------
	_set_id_mode(true)
	_env.ambient_light_energy = 0.0
	_env.fog_enabled = false
	_place_cam(_cam, _proxies[1]["ground"], k125)
	_cam.cull_mask = FG_BIT | BG_BIT | int(_proxies[1]["bit"])
	var imid: Image = await _render(_vp)
	imid.save_png(_out + "/05_layer_id_plateau_k12p5.png")
	await _ortho_canvas(ppm_x, "08_ortho_canvas_layer_id.png")
	_set_id_mode(false)
	var legend := {}
	for e in [["path", C_PATH], ["cliff_rock", C_CLIFF], ["near_rock", C_NEAR_ROCK], ["bridge", C_BRIDGE],
			["bridge_plank_falls_out", C_FALLS_OUT], ["valley", C_VALLEY], ["forest", C_FOREST],
			["ruins", C_RUINS], ["sky", C_SKY_ID], ["proxy", C_PROXY]]:
		var c: Color = e[1]
		legend[e[0]] = [c.r8, c.g8, c.b8]
	_meta["layer_id"] = {"file": "05_layer_id_plateau_k12p5.png", "legend_rgb8": legend}
	var f := FileAccess.open(_out + "/blockout_meta.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(_meta, "  "))
	f.close()
	print("[cliff] DONE -> %s" % _out)
	get_tree().quit()


func _xy(v: Vector2) -> Array:
	return [v.x, v.y]


func _run_v2() -> void:
	var tag := "v2"
	_meta["v2"] = {"ruling": "R-C3-44", "k": K_ACCEPTED, "px_per_m": PPM_ACCEPTED, "cut_depth_m": V2_CUT_DEPTH}
	var g: Vector3 = _proxies[1]["ground"]
	_place_cam(_cam, g, K_ACCEPTED)
	_cam.cull_mask = FG_BIT | BG_BIT | int(_proxies[1]["bit"])
	var img: Image = await _render(_vp)
	img.save_png(_out + "/02_follow_plateau_v2_k12p5.png")
	var gp := _cam.unproject_position(g)
	var meas: Dictionary = await _measure(1, K_ACCEPTED)
	_meta["follow_plateau_v2"] = {"file": "02_follow_plateau_v2_k12p5.png", "camera": _cam_numbers(K_ACCEPTED),
		"ground_px": _xy(gp), "silhouette": meas}
	var oc: Dictionary = await _ortho_canvas(PPM_ACCEPTED, "07_ortho_canvas_shaded_v2.png")
	var om: Dictionary = await _measure(1, 0.0, PPM_ACCEPTED)
	oc["proxy_silhouette_spawn_ortho"] = om
	await _ortho_canvas(PPM_ACCEPTED, "work/ortho_canvas_v2_fgmask_cut%dm.png" % int(V2_CUT_DEPTH), -V2_CUT_DEPTH)
	_set_id_mode(true)
	_env.ambient_light_energy = 0.0
	await _ortho_canvas(PPM_ACCEPTED, "08_ortho_canvas_layer_id_v2.png")
	_set_id_mode(false)
	_meta["ortho_canvas_v2"] = oc
	print("[cliff] v2: follow ground px (%.2f, %.2f) silhouette %.3f px; canvas %dx%d; ortho capsule %.3f px" % [
		gp.x, gp.y, meas["height_px_1080"], oc["size_px"][0], oc["size_px"][1], om["height_px_1080"]])
	var f := FileAccess.open(_out + "/blockout_meta_%s.json" % tag, FileAccess.WRITE)
	f.store_string(JSON.stringify(_meta, "  "))
	f.close()
	print("[cliff] DONE v2 -> %s" % _out)
	get_tree().quit()


# ============================================================================
# v3 RUN — padded canvas, depth map, scene data
# ============================================================================
var _fr_rgt := Vector3.ZERO
var _fr_upc := Vector3.ZERO
var _fr_umin := 0.0
var _fr_vmax := 0.0


func _cpx(local: Vector3) -> Array:
	var w: Vector3 = _level.transform * local
	return [snappedf((w.dot(_fr_rgt) - _fr_umin) * PPM_ACCEPTED, 0.01), snappedf((_fr_vmax - w.dot(_fr_upc)) * PPM_ACCEPTED, 0.01)]


func _poly_px(poly: PackedVector2Array, y: float) -> Array:
	var out := []
	for p in poly:
		out.append(_cpx(Vector3(p.x, y, p.y)))
	return out


func _box_foot(b: Dictionary, y: float, grow: float = 0.0) -> PackedVector2Array:
	var sz: Vector3 = b["size"]
	var th: float = b["yaw"]
	var ex := Vector2(cos(th), -sin(th)) * (sz.x * 0.5 + grow)
	var ez := Vector2(sin(th), cos(th)) * (sz.z * 0.5 + grow)
	var c: Vector2 = b["c"]
	return PackedVector2Array([c - ex - ez, c + ex - ez, c + ex + ez, c - ex + ez])


func _run_v3() -> void:
	_meta["v3"] = {"ruling": "R-C3-48", "k": K_ACCEPTED, "px_per_m": PPM_ACCEPTED, "cut_depth_m": V3_CUT_DEPTH,
		"canvas_px": [V3_CANVAS.x, V3_CANVAS.y], "massif_top_y_m": V3_MASSIF_TOP}
	var oc: Dictionary = await _ortho_canvas(PPM_ACCEPTED, "07_ortho_canvas_shaded_v3.png", NAN, V3_CANVAS)
	await _ortho_canvas(PPM_ACCEPTED, "work/ortho_canvas_v3_depth_rgba.png", NAN, V3_CANVAS, true)
	_set_id_mode(true)
	_env.ambient_light_energy = 0.0
	await _ortho_canvas(PPM_ACCEPTED, "08_ortho_canvas_layer_id_v3.png", NAN, V3_CANVAS)
	_set_id_mode(false)
	_meta["ortho_canvas_v3"] = oc
	var fr: Dictionary = oc["frame"]
	_fr_rgt = Vector3(fr["rgt"][0], fr["rgt"][1], fr["rgt"][2])
	_fr_upc = Vector3(fr["upc"][0], fr["upc"][1], fr["upc"][2])
	_fr_umin = fr["umin"]
	_fr_vmax = fr["vmax"]
	# ---- scene data (canvas px) ----------------------------------------------
	var walk := []
	for piece in [[0.0, _s_c0], [_s_c1, _L]]:
		var poly := PackedVector2Array()
		var sq: float = piece[0]
		while sq < float(piece[1]) - 1e-4:
			poly.append(_c(sq) + _nfar(sq) * _far_off(sq))
			sq = minf(sq + 0.5, float(piece[1]))
		poly.append(_c(piece[1]) + _nfar(piece[1]) * _far_off(piece[1]))
		var sr: float = piece[1]
		while sr > float(piece[0]) + 1e-4:
			poly.append(_c(sr) - _nfar(sr) * _near_off(sr))
			sr = maxf(sr - 0.5, float(piece[0]))
		poly.append(_c(piece[0]) - _nfar(piece[0]) * _near_off(piece[0]))
		walk.append({"id": "path_%d" % walk.size(), "kind": "path", "polygon_px": _poly_px(poly, GROUND_Y)})
	walk.append({"id": "plateau", "kind": "plateau", "polygon_px": _poly_px(_plateau_inner, GROUND_Y)})
	var blocked := []
	for bx in _boxes:
		if bx["cls"] == "near_rock":
			blocked.append({"id": "%s_%d" % [bx["name"], blocked.size()], "kind": "rock", "footprint_px": _poly_px(_box_foot(bx, 0.0), 0.0)})
		elif bx["name"] == "bridge_post":
			blocked.append({"id": "bridge_post_%d" % blocked.size(), "kind": "bridge_rail_post", "footprint_px": _poly_px(_box_foot(bx, 0.0), GROUND_Y)})
		elif String(bx["name"]).begins_with("bridge_plank_"):
			walk.append({"id": "bridge_plank_%d" % bx["index"], "kind": "bridge_deck", "falls_out": bx["falls_out"],
				"polygon_px": _poly_px(_box_foot(bx, GROUND_Y), GROUND_Y)})
	# implied rails: no rail mesh exists in the blockout (posts only); strips along both deck edges, post to post
	var a2: Vector2 = _bridge_ab[0]
	var b2: Vector2 = _bridge_ab[1]
	var sd: Vector2 = _bridge_ab[3]
	for sgn in [-1.0, 1.0]:
		var o1: Vector2 = sd * (BRIDGE_W * 0.5) * sgn
		var o2: Vector2 = sd * (BRIDGE_W * 0.5 + 0.3) * sgn
		blocked.append({"id": "bridge_rail_%s" % ("L" if sgn < 0 else "R"), "kind": "bridge_rail_implied",
			"footprint_px": _poly_px(PackedVector2Array([a2 + o1, b2 + o1, b2 + o2, a2 + o2]), GROUND_Y)})
	var sp: Array = _proxies[1]["local"]
	var scene := {"ruling": "R-C3-48", "units": "v3 ortho canvas px (5376x4096), origin top-left, y down",
		"px_per_m": {"screen_x": PPM_ACCEPTED, "screen_y_ground": PPM_ACCEPTED * sin(deg_to_rad(PL_PITCH_DEG))},
		"walkable": walk, "blocked": blocked,
		"spawn_feet_px": _cpx(Vector3(float(sp[0]), GROUND_Y, float(sp[2]))),
		"spawn_check_unproject_px": oc["proxy_ground_canvas_px"]["plateau"],
		"level_bounds_px": [0, 0, V3_CANVAS.x, V3_CANVAS.y]}
	var f2 := FileAccess.open(_out + "/work/scene_data_raw.json", FileAccess.WRITE)
	f2.store_string(JSON.stringify(scene, "  "))
	f2.close()
	var f := FileAccess.open(_out + "/work/blockout_meta_v3.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(_meta, "  "))
	f.close()
	print("[cliff] v3: canvas %s; spawn %s vs unproject %s; walkable %d, blocked %d" % [
		str(oc["size_px"]), str(scene["spawn_feet_px"]), str(oc["proxy_ground_canvas_px"]["plateau"]), walk.size(), blocked.size()])
	print("[cliff] DONE v3 -> %s" % _out)
	get_tree().quit()


# ============================================================================
# v4 — organic geometry (R-C3-54 / R-C3-55) read from scripts/cliffside_v4_layout.py
# ============================================================================
func _build_v4() -> void:
	_sample_centreline()
	_s_plat = _L * 0.45
	_s_c1 = _L - CHASM_END_TAIL
	_s_c0 = _s_c1 - CHASM_LEN
	_meta["layout"] = {"path_length_m": _L, "plateau_s_m": _s_plat, "chasm_s_m": [_s_c0, _s_c1]}
	var txt := FileAccess.get_file_as_string(_layout_path)
	if txt == "":
		push_error("[cliff] v4: cannot read --layout %s" % _layout_path)
		get_tree().quit(1)
		return
	_layout = JSON.parse_string(txt)
	var ld: Dictionary = _layout
	var sp: Array = ld["spawn_xz"]
	_v4_spawn = Vector2(float(sp[0]), float(sp[1]))
	# python replicates the centreline; check it agrees with this file's before trusting any shape
	var cl: Dictionary = ld["centreline"]
	var ba: Array = cl["bridge_a_xz"]
	var bb: Array = cl["bridge_b_xz"]
	var da := (_c(_s_c0) - Vector2(float(ba[0]), float(ba[1]))).length()
	var db := (_c(_s_c1) - Vector2(float(bb[0]), float(bb[1]))).length()
	print("[cliff] v4 centreline check: bridge a delta %.6f m, b delta %.6f m, L %.6f vs %.6f" % [da, db, _L, float(cl["L_m"])])
	if da > 1e-3 or db > 1e-3:
		push_error("[cliff] v4: python centreline does not match the .gd centreline")
	_meta["v4_centreline_check_m"] = [da, db]
	# ---- top surfaces: grassy rock / dirt path / rim verge zones from one texture ----------------
	var zd: Dictionary = ld["zones"]
	var zimg := Image.load_from_file(_layout_path.get_base_dir() + "/" + String(zd["file"]))
	zimg.generate_mipmaps()
	var ztex := ImageTexture.create_from_image(zimg)
	var m_top := StandardMaterial3D.new()
	m_top.albedo_texture = ztex
	m_top.albedo_color = Color(1, 1, 1)
	m_top.roughness = 1.0
	m_top.cull_mode = BaseMaterial3D.CULL_DISABLED
	m_top.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	_mats.append({"mat": m_top, "id": Color(1, 1, 1), "vcol": false, "tex": true})
	var zo: Array = zd["origin_xz"]
	var zs: Array = zd["size_m"]
	for top in ld["tops"]:
		var poly := PackedVector2Array()
		for q in top["polygon_xz"]:
			poly.append(Vector2(float(q[0]), float(q[1])))
		var tris := PackedInt32Array()
		if top.has("triangles"):
			# v4.2 (R-C3-87 (5)): explicit triangles pinned to v4.1's away from the patched rim (cliffside_v4_2_tris.py)
			for ti in top["triangles"]:
				tris.append(int(ti))
		else:
			tris = Geometry2D.triangulate_polygon(poly)
		if tris.is_empty():
			push_error("[cliff] v4: %s failed to triangulate (%d vertices)" % [top["name"], poly.size()])
		var st := SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		for ti in tris:
			var p := poly[ti]
			st.set_normal(Vector3.UP)
			st.set_uv(Vector2((p.x - float(zo[0])) / float(zs[0]), (p.y - float(zo[1])) / float(zs[1])))
			st.add_vertex(Vector3(p.x, 0.0, p.y))
		_add_mesh(st, m_top, String(top["name"]), {"class": "top_zones"})
		_meta["v4_top_%s" % top["name"]] = {"vertices": poly.size(), "triangles": tris.size() / 3}
	# ---- walls: fluted grids, smooth normals --------------------------------------------------------
	var m_cliff := _mat(C_CLIFF)
	for wall in ld["walls"]:
		var R := int(wall["rows"])
		var C := int(wall["cols"])
		var vv: Array = wall["verts"]
		var st := SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		for k in R * C:
			st.add_vertex(Vector3(float(vv[3 * k]), float(vv[3 * k + 1]), float(vv[3 * k + 2])))
		for r in R - 1:
			for i in C:
				var j := (i + 1) % C
				var a := r * C + i
				var b := r * C + j
				var c := (r + 1) * C + j
				var d := (r + 1) * C + i
				for idx in [a, b, c, a, c, d]:
					st.add_index(idx)
		st.generate_normals()
		_add_mesh(st, m_cliff, String(wall["name"]), {"class": "cliff_rock"})
	# ---- outcrops: faceted boulder meshes, flat normals ----------------------------------------------
	var m_rock := _mat(C_NEAR_ROCK)
	for oc in ld["outcrops"]:
		var tv: Array = oc["tris"]
		var st := SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		for k in tv.size() / 3:
			st.add_vertex(Vector3(float(tv[3 * k]), float(tv[3 * k + 1]), float(tv[3 * k + 2])))
		st.generate_normals()
		_add_mesh(st, m_rock, String(oc["name"]), {"class": "near_rock"})


func _run_v4() -> void:
	_meta["v4"] = {"ruling": "R-C3-54 / R-C3-55", "k": K_ACCEPTED, "px_per_m": PPM_ACCEPTED, "cut_depth_m": V3_CUT_DEPTH,
		"canvas_px": [V3_CANVAS.x, V3_CANVAS.y], "frame_pinned": {"umin": V4_UMIN, "vmax": V4_VMAX}, "layout": _layout_path}
	var oc: Dictionary = await _ortho_canvas(PPM_ACCEPTED, "07_ortho_canvas_shaded_v4.png", NAN, V3_CANVAS)
	await _ortho_canvas(PPM_ACCEPTED, "work/ortho_canvas_v4_depth_rgba.png", NAN, V3_CANVAS, true)
	_set_id_mode(true)
	_env.ambient_light_energy = 0.0
	await _ortho_canvas(PPM_ACCEPTED, "08_ortho_canvas_layer_id_v4.png", NAN, V3_CANVAS)
	_set_id_mode(false)
	_env.ambient_light_energy = 0.45
	_meta["ortho_canvas_v4"] = oc
	var fr: Dictionary = oc["frame"]
	_fr_rgt = Vector3(fr["rgt"][0], fr["rgt"][1], fr["rgt"][2])
	_fr_upc = Vector3(fr["upc"][0], fr["upc"][1], fr["upc"][2])
	_fr_umin = fr["umin"]
	_fr_vmax = fr["vmax"]
	# ---- bridge scene data (canvas px); paths and rocks come from the layout ------------------------
	var walk := []
	var blocked := []
	for bx in _boxes:
		if bx["name"] == "bridge_post":
			blocked.append({"id": "bridge_post_%d" % blocked.size(), "kind": "bridge_rail_post", "footprint_px": _poly_px(_box_foot(bx, 0.0), GROUND_Y)})
		elif String(bx["name"]).begins_with("bridge_plank_"):
			walk.append({"id": "bridge_plank_%d" % bx["index"], "kind": "bridge_deck", "falls_out": bx["falls_out"],
				"polygon_px": _poly_px(_box_foot(bx, GROUND_Y), GROUND_Y)})
	var a2: Vector2 = _bridge_ab[0]
	var b2: Vector2 = _bridge_ab[1]
	var sd: Vector2 = _bridge_ab[3]
	for sgn in [-1.0, 1.0]:
		var o1: Vector2 = sd * (BRIDGE_W * 0.5) * sgn
		var o2: Vector2 = sd * (BRIDGE_W * 0.5 + 0.3) * sgn
		blocked.append({"id": "bridge_rail_%s" % ("L" if sgn < 0 else "R"), "kind": "bridge_rail_implied",
			"footprint_px": _poly_px(PackedVector2Array([a2 + o1, b2 + o1, b2 + o2, a2 + o2]), GROUND_Y)})
	var ends := {"south_abutment_deck_start_px": _cpx(Vector3(a2.x, GROUND_Y, a2.y)), "north_abutment_deck_end_px": _cpx(Vector3(b2.x, GROUND_Y, b2.y))}
	# ---- follow-camera greybox views (player_lock, accepted k) at the layout's feet -----------------
	var follows := []
	var ld: Dictionary = _layout
	var fi := 0
	for ft in ld["feet"]:
		var lxz: Array = ft["local_xz"]
		var g: Vector3 = _level.transform * Vector3(float(lxz[0]), 0.0, float(lxz[1]))
		_place_cam(_cam, g, K_ACCEPTED)
		_cam.cull_mask = FG_BIT | BG_BIT
		var img: Image = await _render(_vp)
		var fn := "work/follow_v4_%d.png" % fi
		img.save_png(_out + "/" + fn)
		var gp := _cam.unproject_position(g)
		follows.append({"file": fn, "feet_canvas_px": ft["feet_px"], "ground_world": [g.x, g.y, g.z], "feet_view_px": [gp.x, gp.y]})
		fi += 1
	var scene := {"ruling": "R-C3-54 / R-C3-55", "units": "v4 ortho canvas px (5376x4096), origin top-left, y down",
		"walkable_bridge": walk, "blocked_bridge": blocked, "bridge_ends": ends, "follow_views": follows,
		"spawn_check_unproject_px": oc["proxy_ground_canvas_px"]["plateau"],
		"spawn_cpx": _cpx(Vector3(_v4_spawn.x, GROUND_Y, _v4_spawn.y))}
	var f2 := FileAccess.open(_out + "/work/scene_data_raw_v4.json", FileAccess.WRITE)
	f2.store_string(JSON.stringify(scene, "  "))
	f2.close()
	var f := FileAccess.open(_out + "/work/blockout_meta_v4.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(_meta, "  "))
	f.close()
	print("[cliff] v4: canvas %s; spawn cpx %s vs unproject %s; bridge %s; follows %d" % [
		str(oc["size_px"]), str(scene["spawn_cpx"]), str(scene["spawn_check_unproject_px"]), str(ends), follows.size()])
	print("[cliff] DONE v4 -> %s" % _out)
	get_tree().quit()
