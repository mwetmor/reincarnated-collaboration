extends SceneTree
## C-9 T10-1b — THE SNOW LAB, MEASURED AND CAPTURED IN ONE RUN.
##
## One run and not two, for the reason shot_barrow.gd states: two runs differ in more than the
## thing under test, and attribution is a subtraction, so a subtraction between two runs
## measures the runs as well as the change.
##
## EVERY FRAME IS READ OUT OF A 1920x1080 SubViewport behind a small OS window. The window
## renders nothing that is kept, which is why a capture can run at 640x360 on screen and still
## be a 1080p deliverable -- and why the camera law reads its rows from the SubViewport. If
## `rows` ever comes back 360, every metre-per-pixel in this report is wrong by 3x and the
## number says so instead of the picture looking subtly off.
##
## NO FRAME EVER TOUCHES DISK. Frames go straight into ffmpeg's stdin through
## OS.execute_with_pipe. Measured before it was built on (tools/probe_pipe.gd): 40 frames in,
## 40 frames out of the decoder, correct codec, size and rate.

const SHOT := Vector2i(1920, 1080)
const FPS := 30.0
const DT := 1.0 / 30.0
const SHIP_QUAD_M := 0.18
const FFMPEG := "/opt/homebrew/bin/ffmpeg"

var vp: SubViewport
var scene: Node3D
var snow: SnowField
var out_dir := ""
var stills_only := false
var _rep := {}
var _enc := {}


func _init() -> void:
	Engine.physics_ticks_per_second = int(FPS)
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--out" and i + 1 < a.size():
			out_dir = a[i + 1]
		elif a[i] == "--stills-only":
			stills_only = true
	if out_dir == "":
		out_dir = "/tmp/claude-501/snowlab"
	DirAccess.make_dir_recursive_absolute(out_dir)
	_run.call_deferred()


func _run() -> void:
	var root := get_root()
	root.get_window().size = Vector2i(640, 360)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/snow_lab.tscn").instantiate()
	vp.add_child(scene)
	for i in 90:
		await process_frame
		await physics_frame
	snow = scene.snow
	scene.knight.set_physics_process(false)
	await _settle()

	_rep["shader_sanity"] = await _shader_sanity()
	if not bool(_rep["shader_sanity"]["ok"]):
		print("\nABORT: %s\n" % _rep["shader_sanity"]["verdict"])
		var bad := FileAccess.open("%s/snow_lab_report.json" % out_dir, FileAccess.WRITE)
		bad.store_string(JSON.stringify(_rep, "  "))
		bad.close()
		quit(3)
		return
	_rep["scene"] = scene.report()
	_rep["bones"] = scene.bone_heights()
	_rep["route"] = {}

	if stills_only:
		# visual iteration only: the stills, none of the measurements and no video. A full
		# measured run is ~25 minutes and the tile, the warp and the drift shapes are judged
		# by eye, so they get a path that does not pay for numbers nobody is reading yet.
		await _m_trail_and_stills()
		var sf := FileAccess.open("%s/snow_lab_report.json" % out_dir, FileAccess.WRITE)
		sf.store_string(JSON.stringify(_rep, "  "))
		sf.close()
		print("\nSTILLS ONLY -- no measurements taken\n")
		quit(0)
		return
	await _m_bases()
	await _m_sink()
	await _m_float()
	await _m_trail_and_stills()
	await _m_ink()
	await _m_cost()
	await _capture_walk()

	var f := FileAccess.open("%s/snow_lab_report.json" % out_dir, FileAccess.WRITE)
	f.store_string(JSON.stringify(_rep, "  "))
	f.close()
	print("\n===REPORT===\n%s\n===END===" % JSON.stringify(_rep, "  "))
	quit(0)


# =============================================================================
#  ACCEPTANCE: BASES — every obstacle ringed by >= 0.10 m of snow, all round
# =============================================================================
func _m_bases() -> void:
	var rows := []
	for o in scene.obstacle_list():
		var c: Vector3 = o["pos"]
		var r := snow.base_ring_min(Vector2(c.x, c.z), float(o["radius_m"]))
		r["class"] = _class_at(c)
		r["radius_m"] = snappedf(float(o["radius_m"]), 0.001)
		r["height_m"] = snappedf(float(o["height_m"]), 0.001)
		r["pass_ge_0.10"] = float(r["min_m"]) >= 0.10
		rows.append(r)
	_rep["bases"] = rows


func _class_at(c: Vector3) -> String:
	for p in scene.prop_rows():
		if (p["pos"] as Vector3).distance_to(c) < 1e-4:
			return String(p["class"])
	return "?"


# =============================================================================
#  ACCEPTANCE: SINK — boot 0.08..0.15 m under the base surface; knee-deep in a drift
# =============================================================================
func _m_sink() -> void:
	var open: Dictionary = scene.shallowest_open(7.0)
	var deep: Dictionary = scene.deepest_drift(7.0)
	_rep["route"]["open_xz"] = [snappedf(open["xz"].x, 0.01), snappedf(open["xz"].y, 0.01)]
	_rep["route"]["drift_xz"] = [snappedf(deep["xz"].x, 0.01), snappedf(deep["xz"].y, 0.01)]
	_rep["route"]["drift_depth_m"] = snappedf(deep["depth_m"], 0.001)

	# --- in BASE snow ---
	# a spot with the base depth and no drift, so "base snow" is what is measured
	var basep := _find_base_spot()
	scene.place_knight(basep.x, basep.y, "NE")
	await _settle()
	var bh: Dictionary = await _planted_bones(70)
	var D := snow.depth_at(basep)
	var sole: float = float(bh.get("sole_y", 0.0))
	_rep["sink_base"] = {
		"at_xz": [snappedf(basep.x, 0.01), snappedf(basep.y, 0.01)],
		"undisturbed_depth_m": snappedf(D, 0.001),
		"sole_above_floor_m": snappedf(sole, 0.001),
		# THE ACCEPTANCE NUMBER: how far the boot is below the surrounding snow surface.
		# Measured against the UNDISTURBED surface, because the snow he is standing on is
		# pressed by definition -- measuring against the pressed surface would report the
		# residual and always pass.
		"boot_below_surface_m": snappedf(D - sole, 0.001),
		"pressed_surface_above_floor_m": snappedf(snow.surface_y(basep) - 0.0, 0.001),
		"ankle_stance_m": bh.get("ankle_stance_m", null),
		"knee_stance_m": bh.get("knee_stance_m", null),
		"is_on_floor": bh.get("is_on_floor", null),
		"LeftFoot": bh.get("LeftFoot", null), "RightFoot": bh.get("RightFoot", null),
		"pass_0.08_to_0.15": (D - sole) >= 0.08 and (D - sole) <= 0.15,
	}

	# --- in a DRIFT: does it reach his knees ---
	var dp: Vector2 = deep["xz"]
	scene.place_knight(dp.x, dp.y, "NE")
	await _settle()
	var bh2: Dictionary = await _planted_bones(70)
	var D2 := snow.depth_at(dp)
	var knee: float = float(bh2.get("knee_stance_m", 0.0))
	var ankle: float = float(bh2.get("ankle_stance_m", 0.0))
	_rep["sink_drift"] = {
		"at_xz": [snappedf(dp.x, 0.01), snappedf(dp.y, 0.01)],
		"undisturbed_depth_m": snappedf(D2, 0.001),
		"knee_stance_m": snappedf(knee, 0.001),
		"ankle_stance_m": snappedf(ankle, 0.001),
		"depth_as_frac_of_knee": snappedf(D2 / maxf(knee, 1e-6), 0.001),
		"max_drift_in_field_m": snow.bake_report().get("max_drift_m", null),
		"sole_y": bh2.get("sole_y", null),
		"is_on_floor": bh2.get("is_on_floor", null),
		"LeftFoot": bh2.get("LeftFoot", null), "RightFoot": bh2.get("RightFoot", null),
		"LeftLeg": bh2.get("LeftLeg", null), "RightLeg": bh2.get("RightLeg", null),
		"reads": ("knee or above" if D2 >= knee * 0.85
			else ("mid-shin" if D2 >= (ankle + knee) * 0.5 else "below mid-shin")),
		"pass_knee_deep": D2 >= knee * 0.85,
	}


func _shader_sanity() -> Dictionary:
	"""IS THE SNOW ACTUALLY RENDERING WITH THE SNOW SHADER? Run before anything is measured.

	Godot paints a shader that failed to compile in MAGENTA and carries on: the frame renders,
	the scene runs, no exception is raised, and every downstream number is about a flat
	untextured surface instead of about snow. That happened in this lab -- a comment lost its
	'//' and the run reported 0.24% inked, 3.71 ms and a passing grade, all of it measured on
	Godot's error material. So the shader is CHECKED, by looking at what the snow renders as,
	and the run ABORTS rather than reporting.

	Judged on saturated magenta specifically, not on 'is it white': the snow is legitimately
	near-white but the grade, the shadow ramp and the blue-violet shadows move it around, and a
	whiteness test would have to be loose enough to let magenta through."""
	scene.set_follow(false)
	scene.park_camera(Vector3.ZERO, 1.0)
	scene.knight.visible = false
	await _settle()
	var img := await _grab()
	var b := _bytes(img)
	var n := img.get_width() * img.get_height()
	var magenta := 0
	var sum := [0.0, 0.0, 0.0]
	for i in n:
		var o := i * 4
		if b[o] > 128 and b[o + 2] > 128 and b[o + 1] < 90:
			magenta += 1
		sum[0] += b[o]
		sum[1] += b[o + 1]
		sum[2] += b[o + 2]
	scene.knight.visible = true
	scene.set_follow(true)
	scene.unpark_camera()
	var frac := float(magenta) / float(n)
	return {
		"magenta_frac": snappedf(frac, 0.000001),
		"mean_rgb": [snappedf(sum[0] / n, 0.1), snappedf(sum[1] / n, 0.1),
					 snappedf(sum[2] / n, 0.1)],
		"ok": frac < 0.01,
		"verdict": ("snow shader compiled" if frac < 0.01
			else "SNOW IS RENDERING MAGENTA -- the shader failed to compile. Every number "
				+ "below would be about Godot's error material. Fix the shader and re-run."),
	}


func _planted_bones(frames: int) -> Dictionary:
	"""Bone heights at their PLANTED extreme, taken as the minimum over N idle frames.

	A single sample catches whatever the idle clip was doing on that frame, and the idle clip
	lifts one leg: measured live, LeftFoot read 0.459 m and RightFoot 0.349 m on the same frame,
	so "the ankle" was anywhere in a 0.11 m band depending on when you looked -- and the sink
	acceptance has a 0.07 m window. The minimum over a cycle is the foot on the ground."""
	var acc := {}
	for i in frames:
		scene.knight.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await process_frame
		var h: Dictionary = scene.bone_heights()
		for k in h:
			if h[k] is bool or h[k] is String:
				acc[k] = h[k]
			elif acc.has(k):
				acc[k] = minf(float(acc[k]), float(h[k]))
			else:
				acc[k] = h[k]
	for k in acc:
		if acc[k] is float:
			acc[k] = snappedf(float(acc[k]), 0.001)
	acc["_sampled_frames"] = frames
	return acc


func _find_base_spot() -> Vector2:
	"""A spot carrying the BASE depth and nothing else: within 1 cm of base_depth_m, at least
	2 m clear of every obstacle. Searched rather than authored, because where the open ground
	is depends on the field seed."""
	var best := Vector2.ZERO
	var bd := 1e9
	var x := -8.0
	while x <= 8.0:
		var z := -8.0
		while z <= 8.0:
			var p := Vector2(x, z)
			var ok := true
			for o in scene.obstacle_list():
				var c: Vector3 = o["pos"]
				if p.distance_to(Vector2(c.x, c.z)) < float(o["radius_m"]) + 2.0:
					ok = false
					break
			if ok:
				var e: float = absf(snow.depth_at(p) - snow.base_depth_m)
				if e < bd:
					bd = e
					best = p
			z += 0.5
		x += 0.5
	return best


# =============================================================================
#  ACCEPTANCE: nothing floats and nothing is buried
# =============================================================================
func _m_float() -> void:
	var rows := []
	for p in scene.prop_rows():
		var lo := INF
		var hi := -INF
		for n in (p["node"] as Node3D).find_children("*", "MeshInstance3D", true, false):
			var mi := n as MeshInstance3D
			if mi.mesh == null or String(mi.name).ends_with("_ink"):
				continue
			var a: AABB = mi.global_transform * mi.mesh.get_aabb()
			lo = minf(lo, a.position.y)
			hi = maxf(hi, a.position.y + a.size.y)
		rows.append({
			"class": p["class"],
			"base_lowest_vertex_y": snappedf(lo, 0.001),
			"top_y": snappedf(hi, 0.001),
			"height_m": snappedf(hi - lo, 0.001),
			"target_height_m": snappedf(float(p["height_m"]), 0.001),
			# negative == sunk into the floor, positive == floating above it
			"gap_to_floor_m": snappedf(lo - 0.0, 0.001),
		})
	_rep["standing"] = rows


# =============================================================================
#  ACCEPTANCE: TRAIL — contrast measurable at 20 s, gone by 60 s
#  and the three deliverable stills, which come off the same walk
# =============================================================================
func _m_trail_and_stills() -> void:
	var deep: Dictionary = scene.deepest_drift(7.0)
	var dp: Vector2 = deep["xz"]
	var start := dp + (Vector2(-0.62, -0.78) * 3.2)     # upwind of the drift
	var finish := dp + (Vector2(0.62, 0.78) * 3.2)
	snow.clear_trail()
	scene.place_knight(start.x, start.y, "NE")
	scene.set_follow(false)
	# the camera is PARKED for the trail measurement: a following camera moves the trail across
	# the frame between captures, and a difference between two frames of different framing
	# measures the camera
	scene.park_camera(Vector3(dp.x, 0.0, dp.y) + scene.up * (55.0 / 100.617553710938), 1.0)
	await _settle()

	# (1) FRESH SNOW -- the deliverable still, WITH him in it, because that is the picture
	_save(await _grab(), "still 1 - fresh snow")
	# HE IS HIDDEN FOR EVERY MEASURED FRAME, including the reference, and the puffs with him.
	# With him visible the noise floor between two captures of an "unchanged" frame came back at
	# mean 0.0015 with a MAX of 0.87 -- his idle animation breathing, which is a bigger
	# per-pixel change than the track being measured. The noise floor was measuring the man.
	scene.knight.visible = false
	snow.puffs = false
	await _settle()
	var ref := await _grab()
	var ref_l := _luma(ref)
	var ref2_l := _luma(await _grab())
	var noise := _trail_metric(ref_l, ref2_l, _all_px(ref))

	# walk him through the drift and out the far side (he is invisible but still walking)
	var guard := 0
	while guard < 400:
		guard += 1
		var rem: float = scene.walk_toward(finish, guard > 90, DT)
		await physics_frame
		await process_frame
		if rem <= 0.0:
			break
	for i in 6:
		scene.knight.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	# out of shot as well as invisible, so his shadow is not in the comparison either
	var away := dp + Vector2(0.62, 0.78) * 16.0
	scene.knight.global_position = Vector3(away.x, 0.03, away.y)
	await _settle()

	# (2) THE TRAIL AT t0. Its pixel set is defined HERE, once, and reused at 20/40/60 s.
	var t0 := await _grab()
	var t0_l := _luma(t0)
	var trail_px_set := _changed_px(ref_l, t0_l, 0.012)
	var d0 := _trail_metric(ref_l, t0_l, trail_px_set)
	var noise_on_set := _trail_metric(ref_l, ref2_l, trail_px_set)

	# THE CLOCK IS ADVANCED, NOT SIMULATED. The trail's age lives in the texture and the shader
	# subtracts it from now_s, so 20 s later is one frame away instead of 600.
	snow.advance_clock(20.0)
	await _settle()
	var d20 := _trail_metric(ref_l, _luma(await _grab()), trail_px_set)

	snow.advance_clock(20.0)
	await _settle()
	var d40 := _trail_metric(ref_l, _luma(await _grab()), trail_px_set)

	snow.advance_clock(20.0)      # 60 s total
	await _settle()
	var d60 := _trail_metric(ref_l, _luma(await _grab()), trail_px_set)

	# he comes back for the deliverable stills, which are pictures and not measurements
	scene.knight.visible = true
	snow.puffs = true
	snow.advance_clock(-55.0)     # back to just-ploughed for still 2
	scene.knight.global_position = Vector3(finish.x, 0.03, finish.y)
	await _settle()
	_save(await _grab(), "still 2 - just ploughed")
	snow.advance_clock(40.0)
	await _settle()
	_save(await _grab(), "still 3 - 40 s later")

	_rep["trail"] = {
		"_metric": "mean |luma difference| from the fresh-snow frame, over the "
			+ "%d pixels the track changed at t0 (|dL| > 0.012). " % trail_px_set.size()
			+ "Camera parked; he is hidden and out of shot for every measured frame, "
			+ "reference included.",
		"noise_floor_whole_frame": noise,
		"noise_floor_on_trail_px": noise_on_set,
		"t0": d0, "t20": d20, "t40": d40, "t60": d60,
		"refill_s": snow.trail_refill_s,
		"trail_px": trail_px_set.size(),
		"t20_over_noise": ("inf (noise floor is exactly 0.0)"
			if float(noise_on_set["mean_abs"]) == 0.0
			else snappedf(float(d20["mean_abs"]) / float(noise_on_set["mean_abs"]), 0.1)),
		"t60_over_noise": ("0 / 0 (both exactly 0.0)"
			if float(noise_on_set["mean_abs"]) == 0.0
			else snappedf(float(d60["mean_abs"]) / float(noise_on_set["mean_abs"]), 0.1)),
		"pass_measurable_at_20s": float(d20["mean_abs"])
			> float(noise_on_set["mean_abs"]) * 8.0,
		"pass_gone_by_60s": float(d60["mean_abs"])
			<= maxf(float(noise_on_set["mean_abs"]) * 3.0, 1e-5),
	}

	# (4) THE CLOSE-UP OF HIS FEET, at the same play camera, zoomed in
	snow.clear_trail()
	var basep := _find_base_spot()
	scene.place_knight(basep.x, basep.y, "NE")
	await _settle()
	# a few steps so there are prints beside him, then stop with his feet in shot
	for i in 60:
		scene.walk_toward(basep + Vector2(0.62, 0.78) * 1.6, false, DT)
		await physics_frame
		await process_frame
	for i in 8:
		scene.knight.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	# aimed at the stance FOOT, pulled back to 0.30 (3.2 m of height) so both boots and the
	# prints behind them are in frame even when the shield covers one of them
	var fp: Vector3 = scene.stance_foot_pos()
	var back: Vector2 = -Vector2(0.62, 0.78) * 0.55
	scene.park_camera(fp + Vector3(back.x, 0.05, back.y), 0.30)
	await _settle()
	_save(await _grab(), "still 4 - feet in the snow")
	scene.unpark_camera()
	scene.set_follow(true)


static func _all_px(img: Image) -> PackedInt32Array:
	var n := img.get_width() * img.get_height()
	var out := PackedInt32Array()
	out.resize(n)
	for i in n:
		out[i] = i
	return out


static func _changed_px(a: PackedFloat32Array, b: PackedFloat32Array,
		thr: float) -> PackedInt32Array:
	var out := PackedInt32Array()
	for i in a.size():
		if absf(b[i] - a[i]) > thr:
			out.append(i)
	return out


static func _luma(img: Image) -> PackedFloat32Array:
	var b := _bytes(img)
	var n := img.get_width() * img.get_height()
	var out := PackedFloat32Array()
	out.resize(n)
	const K := 1.0 / 255.0
	for i in n:
		var o := i * 4
		out[i] = (b[o] * 0.2126 + b[o + 1] * 0.7152 + b[o + 2] * 0.0722) * K
	return out


func _trail_metric(ref: PackedFloat32Array, now: PackedFloat32Array,
		mask: PackedInt32Array) -> Dictionary:
	"""Mean |luma difference| from the fresh-snow frame OVER THE TRAIL'S OWN PIXELS.

	The first version averaged over the WHOLE 1920x1080 frame, and a trail is a few per cent of
	a frame, so the number it produced was the trail's contrast divided by how much sky was in
	shot: 0.0058 at t0 against a 0.0015 noise floor. That is a ratio of 3.9 on a track that is
	plainly visible, and it fails a threshold test for a reason that has nothing to do with the
	snow. The denominator is now the set of pixels the track actually changed, defined ONCE
	from the t0 frame and reused at every later time, so the series measures the track FADING
	rather than the track SHRINKING -- which is the acceptance's actual claim."""
	var sum := 0.0
	var mx := 0.0
	for i in mask:
		var d: float = absf(now[i] - ref[i])
		sum += d
		if d > mx:
			mx = d
	var n: int = maxi(mask.size(), 1)
	return {"mean_abs": snappedf(sum / float(n), 0.000001),
			"max_abs": snappedf(mx, 0.0001), "px": mask.size()}


static func _bytes(img: Image) -> PackedByteArray:
	"""RGBA8 bytes. Image.get_pixel allocates and unpacks a Color per call, and a 1920x1080
	frame is 2.07 million of them -- three frames of that through get_pixel is minutes of
	GDScript per measurement. Indexed bytes are the same arithmetic without the allocation."""
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	return img.get_data()


func _region_diff(a: Image, b: Image) -> Dictionary:
	"""Mean and max absolute luma difference over the whole frame. Whole-frame rather than a
	hand-drawn box: a box has to be placed, and a box placed where the trail is guarantees the
	answer it is testing for."""
	var w := a.get_width()
	var h := a.get_height()
	var ba := _bytes(a)
	var bb := _bytes(b)
	var step := 2
	var n := 0
	var sum := 0.0
	var mx := 0.0
	var over := 0
	const K := 1.0 / 255.0
	for y in range(0, h, step):
		var row := y * w
		for x in range(0, w, step):
			var o := (row + x) * 4
			var la := (ba[o] * 0.2126 + ba[o + 1] * 0.7152 + ba[o + 2] * 0.0722) * K
			var lb := (bb[o] * 0.2126 + bb[o + 1] * 0.7152 + bb[o + 2] * 0.0722) * K
			var d := absf(la - lb)
			sum += d
			if d > mx:
				mx = d
			if d > 0.012:
				over += 1
			n += 1
	return {"mean_abs": snappedf(sum / float(maxi(n, 1)), 0.000001),
			"max_abs": snappedf(mx, 0.0001),
			"frac_over_0.012": snappedf(float(over) / float(maxi(n, 1)), 0.000001),
			"samples": n}


# =============================================================================
#  ACCEPTANCE: INK — <= 1% of snow-surface pixels drawn as line,
#  and a CONTROL that proves the instrument can see a line at all
# =============================================================================
func _m_ink() -> void:
	snow.clear_trail()
	var deep: Dictionary = scene.deepest_drift(7.0)
	var dp: Vector2 = deep["xz"]
	scene.set_follow(false)
	scene.park_camera(Vector3(dp.x, 0.0, dp.y), 1.0)
	# he is moved out of frame: the acceptance is about the SNOW's pixels, and his hull pen is
	# a different pen drawn by a different pass
	scene.knight.global_position = Vector3(dp.x + 20.0, 0.03, dp.y + 20.0)
	await _settle()

	var out := {}
	for op in ["second", "first"]:
		scene.set_ink_operator(op)
		await _settle()
		out[op] = await _ink_once()
	# --- THE CONTROL ---
	# A hard step cut across the field. This MUST ink under either operator: it is a genuine
	# depth discontinuity, which is the thing the pass exists to draw. If the control comes
	# back at zero the instrument is blind and the smooth-snow number above means nothing --
	# this pass has already drawn 0 px in a 2-megapixel frame once, cleanly, from a collapsed
	# sampling span, and read as a threshold that needed loosening.
	scene.rebake_snow(0.22, dp.x)
	await _settle()
	var ctrl := {}
	for op in ["second", "first"]:
		scene.set_ink_operator(op)
		await _settle()
		ctrl[op] = await _ink_once()
	scene.rebake_snow(0.0, 0.0)
	scene.set_ink_operator("second")
	await _settle()

	_rep["ink"] = {
		"_metric": "inked = pixels inside the snow mask where |ink_on - ink_off| > 0.02 luma. "
			+ "The mask is the snow rendered flat magenta with NOTHING hidden and THE SAME "
			+ "vertex displacement, so the obstacles still occlude and the mask edge is the "
			+ "drift silhouette. Obstacle pixels are excluded by the magenta test, so an "
			+ "object's own line is not charged to the snow.",
		"_operators": "HEAD's POST_SHADER uses the FIRST difference (|d11-d00| plus a planar "
			+ "prediction); the integration session's live file uses the SECOND difference. "
			+ "The Barrow will ship the second. Both measured; see snow_lab.gd's note.",
		"_control_note": "The CONTROL is judged on the EXTRA inked pixels, not on the "
			+ "fraction. A 0.22 m step is one line across the frame: at ~1 px wide over a "
			+ "1080-row frame that is order 1e3 pixels, which against a ~2e6-pixel snow mask "
			+ "is 0.05% -- so a fraction test cannot distinguish 'the instrument saw the line' "
			+ "from 'the instrument saw nothing'. The delta can.",
		"smooth_snow": out,
		"control_hard_step_0.22m": ctrl,
		"control_extra_inked_px": {
			"second": int(ctrl["second"]["inked_px"]) - int(out["second"]["inked_px"]),
			"first": int(ctrl["first"]["inked_px"]) - int(out["first"]["inked_px"]),
		},
		"pass_le_1pct_second": float(out["second"]["inked_frac_of_snow"]) <= 0.01,
		"pass_control_draws_second":
			(int(ctrl["second"]["inked_px"]) - int(out["second"]["inked_px"])) > 300,
	}
	scene.set_follow(true)
	scene.unpark_camera()


func _ink_once() -> Dictionary:
	scene.begin_snow_mask()
	await _settle()
	var mask := await _grab()
	scene.end_snow_mask()
	await _settle()
	scene.set_ink(false)
	await _settle()
	var a := await _grab()
	scene.set_ink(true)
	await _settle()
	var b := await _grab()

	var w := mask.get_width()
	var h := mask.get_height()
	var bm := _bytes(mask)
	var ba := _bytes(a)
	var bb := _bytes(b)
	var msk := 0
	var inked := 0
	const K := 1.0 / 255.0
	for y in h:
		var row := y * w
		for x in w:
			var o := (row + x) * 4
			# GREEN, judged on bytes: the flat mask colour. Green because Godot paints a
			# failed shader MAGENTA -- see begin_snow_mask. The MSAA edge of the mask is
			# EXCLUDED by requiring r and b to be low: a partially-covered edge pixel blends
			# toward the sky and would be counted as snow while carrying the sky's own
			# outline, the one place this instrument could manufacture its own answer.
			if bm[o + 1] > 128 and bm[o] < 90 and bm[o + 2] < 90:
				msk += 1
				var la := (ba[o] * 0.2126 + ba[o + 1] * 0.7152 + ba[o + 2] * 0.0722) * K
				var lb := (bb[o] * 0.2126 + bb[o + 1] * 0.7152 + bb[o + 2] * 0.0722) * K
				if absf(la - lb) > 0.02:
					inked += 1
	return {"snow_px": msk, "inked_px": inked,
			"inked_frac_of_snow": snappedf(float(inked) / float(maxi(msk, 1)), 0.000001),
			"inked_pct": snappedf(100.0 * float(inked) / float(maxi(msk, 1)), 0.0001)}


# =============================================================================
#  ACCEPTANCE: FRAME COST — the snow's own cost must be <= 3 ms
# =============================================================================
func _m_cost() -> void:
	scene.set_follow(true)
	var basep := _find_base_spot()
	scene.place_knight(basep.x, basep.y, "NE")
	await _settle()
	_rep["frame_cost_ms"] = {
		"_at": "MSAA 4x, Apple M2, walking with the full kit, vsync off, 1920x1080 SubViewport, snow at its shipped defaults (0.18 m quad, 4 taps, casts shadows, 34x34 m field)",
		"_instrument": "WALL CLOCK over N frames. RenderingServer.viewport_get_measured_"
			+ "render_time_gpu() returns EXACTLY 0.00 on this build -- an unimplemented "
			+ "counter, not a fast frame -- so it is not used. The loop does NOT await "
			+ "physics_frame: physics is at 24-30 Hz for deterministic capture and awaiting it "
			+ "would gate every measurement at 1/fps and report the tick rate three times.",
		"snow_on": await _time(true, 150, SHOT),
		"snow_off": await _time(false, 150, SHOT),
		"instrument_check_2.25x_pixels": {
			"_expect": "a frame with 2.25x the pixels must cost measurably more, or the "
				+ "number is not about rendering",
			"snow_on_at_2880x1620": await _time(true, 90, Vector2i(2880, 1620)),
		},
	}
	var on: float = float(_rep["frame_cost_ms"]["snow_on"]["ms_per_frame"])
	var off: float = float(_rep["frame_cost_ms"]["snow_off"]["ms_per_frame"])
	_rep["frame_cost_ms"]["snow_cost_ms"] = snappedf(on - off, 0.01)
	_rep["frame_cost_ms"]["pass_le_3ms"] = (on - off) <= 3.0
	await _m_cost_attribution(off)


func _m_cost_attribution(off: float) -> void:
	"""WHERE THE MILLISECONDS ARE. One variable at a time, from the same state each time.

	The shipped build costs ~4.7 ms against a 3 ms budget, so this exists to find out WHAT to
	spend the reduction on rather than to guess. The dominant suspect is TRIANGLE SIZE, not
	fetch count: 192,200 triangles over the ~1.97 million pixels the snow covers is about 10
	pixels per triangle, and under MSAA 4x almost every 2x2 shading quad then straddles a
	triangle edge -- so the GPU shades several fragments per pixel. That is a geometry problem
	wearing a shader problem's clothes, and fetch removal cannot fix it. So quad size is swept
	across a real range instead of nudged."""
	var rows := {}
	for q in [0.09, 0.13, 0.18, 0.25]:
		snow.grid_quad_m = q
		scene.rebake_snow(0.0, 0.0)
		await _settle()
		var tris: int = int(snow.bake_report().get("tris", 0))
		var ms: float = float((await _time(true, 120, SHOT))["ms_per_frame"]) - off
		rows["quad_%.2f_m" % q] = {
			"cost_ms": snappedf(ms, 0.01), "tris": tris,
			"px_per_tri": snappedf(1970000.0 / maxf(float(tris), 1.0), 0.1),
			"casts_shadow": false, "taps": 4}
	# the two non-geometry levers, measured at the quad size the sweep favours
	snow.grid_quad_m = 0.18
	scene.rebake_snow(0.0, 0.0)
	snow.set_normal_taps(2)
	await _settle()
	rows["quad_0.18_m_2_taps"] = {"cost_ms": snappedf(
		float((await _time(true, 120, SHOT))["ms_per_frame"]) - off, 0.01),
		"tris": snow.bake_report().get("tris", null), "taps": 2, "casts_shadow": false}
	snow.set_normal_taps(4)
	snow.set_cast_shadows(true)
	await _settle()
	rows["quad_0.18_m_casts_shadow"] = {"cost_ms": snappedf(
		float((await _time(true, 120, SHOT))["ms_per_frame"]) - off, 0.01),
		"tris": snow.bake_report().get("tris", null), "taps": 4, "casts_shadow": true}
	snow.set_cast_shadows(false)
	_rep["cost_attribution"] = {
		"_baseline_off_ms": snappedf(off, 0.01),
		"_note": "cost_ms is (snow on) - (snow off) at 1920x1080, same start, trail cleared "
			+ "before every row",
		"_budget_ms": 3.0,
		"variants": rows,
	}
	# restored to the module's defaults before the capture, so the deliverable video is the
	# configuration the module ships with and not whatever the last sweep row left behind
	snow.grid_quad_m = SHIP_QUAD_M
	snow.set_normal_taps(4)
	snow.set_cast_shadows(true)      # the module's shipped default; +0.05 ms at this quad
	scene.rebake_snow(0.0, 0.0)
	await _settle()


func _time(snow_on: bool, n: int, res: Vector2i, reset := true) -> Dictionary:
	# EVERY ROW STARTS FROM THE SAME STATE, and the first sweep did not. Two things made the
	# rows incomparable, and the second is self-inflicted:
	#   - he ends each row somewhere else, so the next row walks different ground;
	#   - the trail GROWS across the sweep, and the fragment shader's trail-tap early-out means
	#     cost is a function of how much trail is on screen. The optimisation made the
	#     measurement state-dependent.
	# Unreset, the sweep reported 2 taps costing MORE than 4 (8.20 ms against 4.77) -- an
	# ordering that is impossible for strictly fewer fetches, which is how the confound
	# announced itself rather than quietly shifting the numbers.
	if reset:
		snow.clear_trail()
		scene.place_knight(-2.0, -6.0, "NE")
		await _settle()
	# HIDDEN, not removed: hiding changes exactly one thing about the frame. And the snow is
	# hidden rather than having its shader neutralised, because a neutralised shader still
	# rasterises 300k triangles and that cost would land on the "off" side.
	snow.set_visible_snow(snow_on)
	var prev := vp.size
	if res != vp.size:
		vp.size = res
	var prev_ticks := Engine.physics_ticks_per_second
	Engine.physics_ticks_per_second = 240
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	var target := Vector2(6.0, 6.0)
	for i in 40:                                  # warm: shader compiles land in these frames
		scene.walk_toward(target, false, DT)
		await process_frame
	var t0 := Time.get_ticks_usec()
	for i in n:
		scene.walk_toward(target, false, DT)
		await process_frame
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	Engine.physics_ticks_per_second = prev_ticks
	vp.size = prev
	snow.set_visible_snow(true)
	return {"ms_per_frame": snappedf(ms, 0.01), "fps": snappedf(1000.0 / maxf(ms, 1e-3), 0.1),
			"frames": n, "render_px": [res.x, res.y], "snow": snow_on}


# =============================================================================
#  THE 20-SECOND WALK, STRAIGHT INTO ffmpeg
# =============================================================================
func _capture_walk() -> void:
	snow.clear_trail()
	scene.set_follow(true)
	scene.unpark_camera()
	var deep: Dictionary = scene.deepest_drift(7.0)
	var dp: Vector2 = deep["xz"]
	var stone := Vector2.ZERO
	for p in scene.prop_rows():
		if String(p["class"]) == "stone_tall":
			stone = Vector2((p["pos"] as Vector3).x, (p["pos"] as Vector3).z)
	var w := Vector2(0.62, 0.78)          # the wind, and the drift's long axis
	var a := dp - w * 4.2                 # open snow, upwind
	var b := dp                           # the drift
	var c := dp + w * 3.0                 # out the far side
	var d := stone + (a - stone).normalized() * 1.6   # up to the stone
	scene.place_knight(a.x, a.y, "NE")
	await _settle()

	var out := "%s/snow lab walk.mp4" % out_dir
	_open_encoder(out)
	# 20 s at 30 fps. Each leg runs until it ARRIVES, capped, so the route is the route and
	# not a frame budget: he walks into the drift, RUNS through it, stops, walks to the stone,
	# then comes back along his own trail.
	var legs := [
		{"to": b, "run": false, "max": 130},   # walk into the drift
		{"to": c, "run": true,  "max": 110},   # run through it -- the plough and the spray
		{"to": c, "run": false, "max": 34, "stop": true},   # stop, in the channel
		{"to": d, "run": false, "max": 170},   # past the stone, through its skirt
		{"to": a, "run": false, "max": 210},   # back along his own trail
	]
	var frames := 0
	for leg in legs:
		var guard := 0
		while guard < int(leg["max"]):
			guard += 1
			if leg.get("stop", false):
				scene.knight.drive_dir(Vector2.ZERO, false, DT)
			elif scene.walk_toward(leg["to"], bool(leg["run"]), DT) <= 0.0:
				break
			await physics_frame
			await _emit()
			frames += 1
	# a beat at the end so the last frame is not mid-stride
	for i in 20:
		scene.knight.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await _emit()
		frames += 1
	_close_encoder()
	_rep["capture"] = {
		"mp4": out, "frames": frames, "fps": FPS,
		"seconds": snappedf(float(frames) / FPS, 0.01),
		"route_xz": {"open": [snappedf(a.x, 0.01), snappedf(a.y, 0.01)],
					 "drift": [snappedf(b.x, 0.01), snappedf(b.y, 0.01)],
					 "far_side": [snappedf(c.x, 0.01), snappedf(c.y, 0.01)],
					 "stone": [snappedf(d.x, 0.01), snappedf(d.y, 0.01)]},
		"encoder": "OS.execute_with_pipe -> ffmpeg rawvideo stdin; no frame written to disk",
		"stills": _rep.get("stills", []),
	}


func _open_encoder(path: String) -> void:
	var args := ["-y", "-loglevel", "error", "-f", "rawvideo", "-pixel_format", "rgba",
		"-video_size", "%dx%d" % [SHOT.x, SHOT.y], "-framerate", str(int(FPS)),
		"-i", "pipe:0", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
		"-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
	_enc = OS.execute_with_pipe(FFMPEG, args)
	if _enc.is_empty():
		push_error("ffmpeg pipe did not open")


func _emit() -> void:
	await process_frame
	if _enc.is_empty():
		return
	var img := vp.get_texture().get_image()
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	(_enc["stdio"] as FileAccess).store_buffer(img.get_data())


func _close_encoder() -> void:
	if _enc.is_empty():
		return
	(_enc["stdio"] as FileAccess).close()
	OS.delay_msec(2500)      # ffmpeg flushes the moov atom after EOF
	_enc = {}


# =============================================================================
func _settle() -> void:
	# drive_dir IS CALLED WITH ZERO, not merely awaited. knight.gd applies gravity and calls
	# move_and_slide inside drive_dir, and the capture sets set_physics_process(false) so that
	# nothing else calls it -- so a settle that only awaited frames left him hanging at the
	# +0.03 m spawn lift, and every sink number was 0.03 m short of the truth while still
	# landing inside the acceptance band. A measurement that passes for the wrong reason.
	for i in 14:
		scene.knight.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _grab() -> Image:
	for i in 3:
		await process_frame
	return vp.get_texture().get_image()


func _save(img: Image, nm: String) -> void:
	img.save_png("%s/%s.png" % [out_dir, nm])
	var l: Array = _rep.get("stills", [])
	l.append("%s.png" % nm)
	_rep["stills"] = l
