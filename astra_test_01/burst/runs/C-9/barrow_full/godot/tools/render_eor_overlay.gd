extends SceneTree
## C-9 R-C9-146 follow-on (lane EOR2, drax): THE EYE OF RECKONING AS A 2D ARENA OVERLAY ATLAS, for kc2_play.
## The Barrow's effect (scripts/eor_kc2_fx.gd, the node pool, R-C9-143/146 final) with NO knight: its steel is driven
## from the eor3 pack's own sockets (main_tip / main_grip per frame per direction, port model frame), so the arc
## and the sparks sit on the mace the cells draw. Two passes, two render layers:
##   UNDER  bed + haze (ground-plane, under the actor): transparent background, ppm_GD (= ppm_render / 2),
##          1024 x 1024, anchor (512, 576). Direction-independent: rendered once (on S).
##   OVER   sparks + embers (over the actor; R-C9-152: no cuts): MIX-blended, rendered on a TRANSPARENT viewport;
##          ppm_render, 1536 x 1536, anchor (768, 832); a body-sized capsule (r 0.28 m, h 1.85 m) writes DEPTH ONLY,
##          a holdout so what is behind his body does not draw over his sprite.
## Clock: --fixed-fps 480 (the 16/rev grid is 9 steps, the 30 fps grid 16). Timeline per direction:
##   t = 0 begin (channel begin) -> eor_spin_start sockets to 0.2 s -> eor_spin_loop sockets (0.3 s/rev) ->
##   release at 0.2 + 1.2 s -> 0.8 s fade. Captures: start 7 @ 30 fps; the loop window [0.2, 1.4) at 16/rev plus its
##   crossfade tail [0.10625, 0.2); end 25 @ 30 fps. Frames written raw; the packer crossfades and declares.
##   Godot --path . --fixed-fps 480 --rendering-method gl_compatibility --rendering-driver opengl3_angle
##     --script tools/render_eor_overlay.gd -- --tint red|original --pack <eor3 pack root> --out <raw dir>
const STEP_HZ := 480
const PPM := 151.33680669505316
const PITCH_DEG := 52.9535411256029
const LOOP_REVS := 4
const REV_S := 0.3
const START_S := 0.2
const END_S := 0.8
const FADE_TAIL_STEPS := 5                    # loop frames crossfaded into the start's tail (0.09375 s)
const UNDER_LAYER := 2
const OVER_LAYER := 4
const DIRS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]

var tint := "red"
var out_dir := ""
var idx: Dictionary
var vp_under: SubViewport
var vp_over: SubViewport
var fx = null
var dir_i := 0
var step := -1
var pending: Array = []                       # [step_to_capture_at, name] -- captured one step later
var tips_start: Array
var grips_start: Array
var tips_loop: Array
var grips_loop: Array
var radius_m := 0.0
var height_m := 0.0
var released := false
var log_rows: Array = []


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	tint = String(a[a.find("--tint") + 1])
	out_dir = String(a[a.find("--out") + 1])
	var pack := String(a[a.find("--pack") + 1])
	idx = JSON.parse_string(FileAccess.get_file_as_string(pack + "/matrix_index.json"))
	DirAccess.make_dir_recursive_absolute(out_dir)
	# weapon truth from the sockets: mean |main_tip.xy| and mean main_tip.z over the S loop
	var s := 0.0
	var z := 0.0
	var tl: Array = idx["cells"]["eor_spin_loop/S"]["sockets_m"]["main_tip"]
	for p in tl:
		s += Vector2(float(p[0]), float(p[1])).length()
		z += float(p[2])
	radius_m = s / tl.size()
	height_m = z / tl.size()
	vp_under = _viewport(Vector2i(1024, 1024), 1024.0 / (PPM * 0.5), (576.0 - 512.0) / (PPM * 0.5), UNDER_LAYER, true)
	vp_over = _viewport(Vector2i(1536, 1536), 1536.0 / PPM, (832.0 - 768.0) / PPM, OVER_LAYER, true)
	var cap := MeshInstance3D.new()
	var cm := CapsuleMesh.new()
	cm.radius = 0.28
	cm.height = 1.85
	cap.mesh = cm
	cap.position = Vector3(0.0, 0.925, 0.0)
	# R-C9-152: the over layer is MIX-blended now (sparks, embers), so it renders on a TRANSPARENT viewport and the
	# holdout writes DEPTH ONLY -- no colour, no alpha -- drawn first (priority -100)
	var hs := Shader.new()
	hs.code = "shader_type spatial;\nrender_mode unshaded, blend_add, depth_draw_always, cull_back, shadows_disabled;\nvoid fragment() { ALBEDO = vec3(0.0); ALPHA = 0.0; }\n"
	var bm := ShaderMaterial.new()
	bm.shader = hs
	bm.render_priority = -100
	cap.material_override = bm
	cap.layers = OVER_LAYER
	root.add_child(cap)
	print("[eor_overlay] tint=%s radius=%.4f height=%.4f" % [tint, radius_m, height_m])
	_next_dir()


func _viewport(px: Vector2i, size_m: float, v_off: float, mask: int, transparent: bool) -> SubViewport:
	var vp := SubViewport.new()
	vp.size = px
	vp.transparent_bg = transparent
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	vp.msaa_3d = Viewport.MSAA_4X
	root.add_child(vp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = size_m
	cam.near = 0.1
	cam.far = 200.0
	cam.cull_mask = mask
	cam.v_offset = v_off
	var b := Basis.from_euler(Vector3(-deg_to_rad(PITCH_DEG), 0.0, 0.0))
	cam.transform = Transform3D(b, b.z * 60.0)   # 60 m back along the view ray, looking at the ground origin
	var env := Environment.new()
	env.background_mode = Environment.BG_CLEAR_COLOR if transparent else Environment.BG_COLOR
	env.background_color = Color(0, 0, 0, 0 if transparent else 1)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR   # the Barrow's (PaintStack.barrow_environment)
	cam.environment = env
	vp.add_child(cam)
	return vp


func _g(p: Array) -> Vector3:
	"""port model frame (x screen-right, y toward camera, z up) -> Godot (X right, Y up, Z toward camera)"""
	return Vector3(float(p[0]), float(p[2]), float(p[1]))


func _next_dir() -> void:
	if fx != null:
		fx.queue_free()
		fx = null
	if dir_i >= DIRS.size():
		var f := FileAccess.open(out_dir + "/render_log.json", FileAccess.WRITE)
		f.store_string(JSON.stringify({"tint": tint, "radius_m": radius_m, "height_m": height_m, "rows": log_rows}, " "))
		f.close()
		print("[eor_overlay] done")
		quit(0)
		return
	var d: String = DIRS[dir_i]
	tips_start = idx["cells"]["eor_spin_start/" + d]["sockets_m"]["main_tip"]
	grips_start = idx["cells"]["eor_spin_start/" + d]["sockets_m"]["main_grip"]
	tips_loop = idx["cells"]["eor_spin_loop/" + d]["sockets_m"]["main_tip"]
	grips_loop = idx["cells"]["eor_spin_loop/" + d]["sockets_m"]["main_grip"]
	fx = load("res://scripts/eor_kc2_fx.gd").new()
	root.add_child(fx)
	fx.bind_synthetic(radius_m, height_m, REV_S, tint, UNDER_LAYER, OVER_LAYER)
	step = -24                                    # a few settle steps before t = 0
	released = false
	pending = []


func _polar_lerp(a: Vector3, b: Vector3, w: float) -> Vector3:
	var ba := atan2(a.x, a.z)
	var bb := ba + wrapf(atan2(b.x, b.z) - ba, -PI, PI)
	var r := lerpf(Vector2(a.x, a.z).length(), Vector2(b.x, b.z).length(), w)
	var ang := lerpf(ba, bb, w)
	return Vector3(sin(ang) * r, lerpf(a.y, b.y, w), cos(ang) * r)


func _steel_at(t: float) -> Array:
	"""[tip, grip] at clip time t (start clip, then the loop), interpolated between the cells' samples."""
	var tips: Array
	var grips: Array
	var u: float
	if t < START_S:
		u = t / START_S * float(tips_start.size() - 1)
		tips = tips_start
		grips = grips_start
		var i0 := clampi(int(floor(u)), 0, tips.size() - 2)
		var w0: float = u - float(i0)
		return [_polar_lerp(_g(tips[i0]), _g(tips[i0 + 1]), w0), _polar_lerp(_g(grips[i0]), _g(grips[i0 + 1]), w0)]
	u = fposmod(t - START_S, REV_S) / REV_S * float(tips_loop.size())
	var i := int(floor(u)) % tips_loop.size()
	var j := (i + 1) % tips_loop.size()
	var w: float = u - floor(u)
	return [_polar_lerp(_g(tips_loop[i]), _g(tips_loop[j]), w), _polar_lerp(_g(grips_loop[i]), _g(grips_loop[j]), w)]


func _process(_dt: float) -> bool:
	if fx == null:
		return false
	# captures requested one step ago (the viewport has drawn that step now)
	for c in pending:
		_save(String(c))
	pending = []
	step += 1
	var t := float(step) / float(STEP_HZ)
	var st: Array = _steel_at(maxf(t, 0.0))
	var tip: Vector3 = st[0]
	var grip: Vector3 = st[1]
	var ax := (tip - grip).normalized()
	fx.syn_head = tip
	fx.syn_axis = ax
	fx.syn_ember = tip - ax * 0.117               # PORT 11 on the cells: 0.93 of the mace = 0.117 m back from its head
	if step == 0:
		fx.begin()
	var rel_step := int(round((START_S + LOOP_REVS * REV_S) * STEP_HZ))
	if step == rel_step and not released:
		fx.end()
		released = true
	if step < 0:
		return false
	var d: String = DIRS[dir_i]
	# start: 7 frames at 30 fps (t = 0 .. 0.2, both ends) -- the body's eor_spin_start t_s
	if step % 16 == 0 and step <= 96:
		pending.append("start/%s/%02d" % [d, step / 16])
	# the loop window [0.2, 1.4) at 16 per rev + its crossfade tail before 0.2
	var g := step - 96
	if g % 9 == 0 and g >= -9 * FADE_TAIL_STEPS and g < 9 * 16 * LOOP_REVS:
		pending.append("loop/%s/%s%03d" % [d, "m" if g < 0 else "", absi(g / 9)])
	# end: 25 frames at 30 fps from the release (0 .. 0.8 s)
	var e := step - rel_step
	if e >= 0 and e % 16 == 0 and e <= 16 * 24:
		pending.append("end/%s/%02d" % [d, e / 16])
	if e > 16 * 24 + 2:
		log_rows.append({"dir": d, "revs_at_release": fx.get("_end_revs"), "state": fx.state_name()})
		dir_i += 1
		_next_dir()
	return false


func _save(name: String) -> void:
	var parts := name.split("/")
	var seg := parts[0]
	var d := parts[1]
	var leaf := parts[2]
	var od := "%s/over/%s/%s" % [out_dir, seg, d]
	DirAccess.make_dir_recursive_absolute(od)
	vp_over.get_texture().get_image().save_png("%s/%s.png" % [od, leaf])
	if d == "S":
		var ud := "%s/under/%s" % [out_dir, seg]
		DirAccess.make_dir_recursive_absolute(ud)
		vp_under.get_texture().get_image().save_png("%s/%s.png" % [ud, leaf])
