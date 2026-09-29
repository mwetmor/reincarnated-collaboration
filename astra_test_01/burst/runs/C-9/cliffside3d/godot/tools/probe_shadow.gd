extends SceneTree
# C-9 R-C9-74 note 3 — THE SHADOW BIAS SWEEP, ON A SURFACE THAT CAN ACTUALLY ACNE.
#
# THE FIRST SWEEP RETURNED FIVE IDENTICAL ROWS and I nearly quoted them. normal_bias 0.0,
# 0.25, 0.55, 1.2 and 3.0 all reported a dark-pixel share of 0.12561 -- the same number to
# five decimal places, which is not "the bias does not matter much", it is THE FRAME DID NOT
# CHANGE AT ALL. The sweep was parked over open FLAT floor, and R-C9-74 had just made the
# floor flat: a plane at a single depth, with no caster over it, has nothing to self-shadow
# and cannot produce acne at any bias. The 12.6% it was counting was the rock tile's own dark
# speckle, which is a property of the texture and moves for no shadow setting whatever.
#
# So the sweep runs where acne lives: THE MOUND, a curved surface that turns through the
# light, and the standing stones, which are the only other non-planar geometry in the scene.
# And the instrument is checked against a case whose answer is known -- shadows switched OFF
# entirely must report a dark share of ~0, or the number is about the texture again.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_shadow.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)
const MOUND := Vector2(0.0, -4.0)

var out_dir := ""
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("user://shadow")
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 70:
		await process_frame
		await physics_frame
	var k = scene.knight
	k.set_physics_process(false)
	scene.freeze_pose(true)
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.state = "idle"
	scene.set_hud_visible(false)
	# grade and paper OFF: both multiply the frame and the paper grain IS a speckle population
	scene.set_grade(false)
	scene.set_particles(false)
	scene.set_pens(false)
	scene.place_knight(4.2, -0.3, "NE")

	var sun: DirectionalLight3D = scene.sun
	var rep := {"_at": "the mound at (0, -4) and the ring, grade/particles/pens off",
				"sun_elevation_deg": scene.SUN_ELEV_DEG}

	# the control: shadows OFF. Whatever dark share this reports is the SURFACE, not acne,
	# and every row below has to be read against it rather than against zero.
	scene.park_camera(Vector3(MOUND.x, scene.world.height_at(MOUND.x, MOUND.y) + 1.4, MOUND.y), 0.85)
	sun.shadow_enabled = false
	await _settle()
	var control := _speckle(vp.get_texture().get_image())
	sun.shadow_enabled = true
	rep["control_shadows_off"] = control

	var rows := []
	for nb in [0.0, 0.15, 0.35, 0.55, 1.2, 3.0]:
		sun.shadow_normal_bias = float(nb)
		await _settle()
		var s := _speckle(vp.get_texture().get_image())
		s["excess_over_control"] = snappedf(float(s["dark_share"]) - float(control["dark_share"]), 0.00001)
		rows.append({"normal_bias": nb, "shadow_bias": sun.shadow_bias, "acne": s})
	rep["sweep_normal_bias"] = rows

	# and the other half of the trade: the gap between him and his own shadow, at each bias
	var gaps := []
	scene.unpark_camera()
	scene.place_knight(4.2, -0.3, "NE")
	scene.park_camera(scene._aim_for(scene.knight.global_position), 1.0)
	for nb in [0.0, 0.15, 0.35, 0.55, 1.2, 3.0]:
		sun.shadow_normal_bias = float(nb)
		gaps.append({"normal_bias": nb, "contact": await _contact(k)})
	rep["contact_gap_by_bias"] = gaps

	var f := FileAccess.open(out_dir + "/shadow_sweep.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[shadow] control %.5f | rows %s" % [float(control["dark_share"]),
		JSON.stringify(rows.map(func(r): return [r["normal_bias"], r["acne"]["excess_over_control"]]))])
	print("[shadow] gaps %s" % JSON.stringify(gaps.map(func(g): return [g["normal_bias"], g["contact"]["gap_px"]])))
	quit(0)


func _speckle(img: Image) -> Dictionary:
	"""The share of pixels in the central window more than 8% of luma below the window mean.
	Acne is a dark speckle population on a lit surface; so is a dark texture, which is why
	every row is read against the shadows-off control rather than against zero."""
	var x0 := int(float(SHOT.x) * 0.30)
	var x1 := int(float(SHOT.x) * 0.70)
	var y0 := int(float(SHOT.y) * 0.24)
	var y1 := int(float(SHOT.y) * 0.62)
	var vals := PackedFloat32Array()
	for y in range(y0, y1, 2):
		for x in range(x0, x1, 2):
			var c := img.get_pixel(x, y)
			vals.append(c.r * 0.2126 + c.g * 0.7152 + c.b * 0.0722)
	var mean := 0.0
	for v in vals:
		mean += v
	mean /= maxf(float(vals.size()), 1.0)
	var dark := 0
	for v in vals:
		if v < mean - 0.08:
			dark += 1
	return {"px_sampled": vals.size(), "mean_luma_srgb": snappedf(mean, 0.0001),
			"dark_share": snappedf(float(dark) / maxf(float(vals.size()), 1.0), 0.00001)}


func _contact(k) -> Dictionary:
	var box := 240
	var rect: Rect2 = scene.character_screen_rect()
	var cx := int(rect.position.x + rect.size.x * 0.5)
	var cy := int(rect.position.y + rect.size.y * 0.5)
	var x0: int = clampi(cx - box, 0, SHOT.x - 1)
	var y0: int = clampi(cy - box, 0, SHOT.y - 1)
	var w: int = clampi(cx + box, 0, SHOT.x - 1) - x0
	var h: int = clampi(cy + box, 0, SHOT.y - 1) - y0
	var sun: DirectionalLight3D = scene.sun
	sun.shadow_enabled = false
	await _settle()
	var a_off: Image = vp.get_texture().get_image()
	k.visible = false
	await _settle()
	var b_off: Image = vp.get_texture().get_image()
	k.visible = true
	sun.shadow_enabled = true
	await _settle()
	var a_on: Image = vp.get_texture().get_image()
	k.visible = false
	await _settle()
	var b_on: Image = vp.get_texture().get_image()
	k.visible = true
	await _settle()
	var sil := []
	var shd := []
	sil.resize(w * h)
	shd.resize(w * h)
	var n_sil := 0
	var n_shd := 0
	for j in h:
		for i in w:
			var d_off := _dif(a_off.get_pixel(x0 + i, y0 + j), b_off.get_pixel(x0 + i, y0 + j))
			var d_on := _dif(a_on.get_pixel(x0 + i, y0 + j), b_on.get_pixel(x0 + i, y0 + j))
			var s: bool = d_off > 0.012
			sil[j * w + i] = s
			var sh: bool = (not s) and d_on > 0.012
			shd[j * w + i] = sh
			n_sil += 1 if s else 0
			n_shd += 1 if sh else 0
	var gap := -1
	var cur: Array = sil.duplicate()
	for step in 8:
		for j in h:
			for i in w:
				if cur[j * w + i] and shd[j * w + i]:
					gap = step
					break
			if gap >= 0:
				break
		if gap >= 0:
			break
		var nxt: Array = cur.duplicate()
		for j in range(1, h - 1):
			for i in range(1, w - 1):
				if cur[j * w + i]:
					nxt[j * w + i - 1] = true
					nxt[j * w + i + 1] = true
					nxt[(j - 1) * w + i] = true
					nxt[(j + 1) * w + i] = true
		cur = nxt
	return {"his_px": n_sil, "his_shadow_px": n_shd, "gap_px": gap,
			"shadow_as_share_of_his_body": snappedf(float(n_shd) / maxf(float(n_sil), 1.0), 0.01)}


func _dif(a: Color, b: Color) -> float:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b)


func _settle() -> void:
	for i in 6:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame
