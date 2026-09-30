extends SceneTree
# C-9 T10-1b — FRAME COST, ATTRIBUTED. One run, every addition toggled in place.
#
# The coordinator asked for each addition's cost SEPARATELY -- the snow, the density, the
# asset swap -- against a 16.7 ms budget at 1080p with the stack on. Two of those are toggles
# inside one scene (the snow field, the density root), so they are measured as a subtraction
# WITHIN one run: same pose, same walk, same shader cache. The swap is a change of FILES, so
# it is the difference between two runs of this same probe, before and after, and is quoted
# with the run-to-run spread beside it so the reader can see whether it clears the noise.
#
# THE STATES ARE MEASURED ABAB, not AABB. This is an 8 GB M2 shared with other sessions and
# its clocks move over a minute; measuring every state twice, interleaved, puts any drift into
# the spread rather than into one state's number.
#
# THE INSTRUMENT IS CHECKED on a known case, the same way shot_barrow checks it: a frame with
# 2.25x the pixels must cost measurably more, or the number is not about rendering.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_cost.gd -- --out DIR [--tag T]

const SHOT := Vector2i(1920, 1080)
const DT := 1.0 / 24.0
var out_dir := ""
var tag := "run"
var only: PackedStringArray = []     # --only a,b,c: measure just these states (a lever hunt)
# --reps N: interleaved passes over the states (default 2, ABAB). On a machine other sessions
# are also rendering on, 2 is not enough: one pass can land on another run's frame burst.
# The MEDIAN is reported beside the mean for that reason.
var reps := 2
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--tag" and i + 1 < args.size():
			tag = args[i + 1]
		if args[i] == "--only" and i + 1 < args.size():
			only = String(args[i + 1]).split(",")
		if args[i] == "--reps" and i + 1 < args.size():
			reps = maxi(int(args[i + 1]), 2)
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("user://cost")
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	# T10-1d: both heather representations built, one drawn -- stems vs cards in one run
	if "--heather-ab" in args:
		scene.heather_ab = true
	# ...and which heather: "stems" (T10-1d), "blobs" (T10-1c's), for the before/after
	var hi := args.find("--heather")
	if hi >= 0 and hi + 1 < args.size():
		scene.heather_mode = args[hi + 1]
	vp.add_child(scene)
	for i in 80:
		await process_frame
		await physics_frame
	var k = scene.knight
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	scene.set_hud_visible(false)
	scene.place_knight(7.9, 5.1, "NE")
	for i in 20:
		await process_frame

	var has_snow: bool = scene.has_method("set_snowfield_visible") and scene.get("snow") != null
	var has_density: bool = scene.has_method("set_density_visible") and scene.get("_density_root") != null
	var states := [["stack_on", true, true, true], ["stack_off", false, true, true]]
	if has_snow:
		states.append(["stack_on_no_snow", true, false, true])
	if has_density:
		states.append(["stack_on_no_density", true, true, false])
	# DIAGNOSTIC STATES, to find where an addition's cost goes rather than to report it:
	# the sun's shadows off, and the dressing's hull pens off
	states.append(["diag_no_shadows", true, true, true, "no_shadows"])
	if has_density:
		states.append(["diag_no_density_inks", true, true, true, "no_density_inks"])
	# T10-1c: the same props drawn one node each -- the "before" of instancing, same content --
	# and the per-asset split in both modes, and the instanced pens alone
	if scene.has_method("set_instancing"):
		states.append(["stack_on_nodes", true, true, true, "nodes"])
		states.append(["stack_on_nodes_no_density", true, true, false, "nodes"])
		states.append(["diag_no_instanced_pens", true, true, true, "no_mm_pens"])
		for a in ["rock_large", "rock_small", "juniper", "heather", "birch"]:
			states.append(["asset_inst_no_" + a, true, true, true, "asset:" + a])
			states.append(["asset_nodes_no_" + a, true, true, true, "nodes+asset:" + a])
	# T10-1c, the rest of the pass, each as a subtraction in the same run: the heather clumps'
	# bodies, the heather blades drawn two-sided, the rocks laid low (vs upright), the feather
	if scene.has_method("set_heather_cores_visible"):
		states.append(["diag_no_heather_cores", true, true, true, "no_cores"])
		# the blades drawn the OTHER way from how the scene ships them (two-sided if it ships
		# one-sided, and back): the cost of the switch, whichever way it is set -- T10-1c's
		# tussocks only; it swaps in the world shader, which the T10-1d sprays do not use
		if String(scene.get("heather_mode")) == "blobs":
			states.append(["diag_heather_sides_flipped", true, true, true, "heather_sides_flipped"])
	if scene.has_method("set_rock_pose"):
		states.append(["diag_rocks_upright", true, true, true, "rocks_upright"])
	if has_snow:
		states.append(["diag_no_feather", true, true, true, "no_feather"])
	if scene.has_method("set_heather_cores_visible"):
		states.append(["diag_heather_blades_noshadow", true, true, true, "heather_blades_noshadow"])
	states.append(["diag_lod4", true, true, true, "lod:4"])
	# T10-1d: the shadow before the bands (T10-1c's ramp); the heather's wind and push off;
	# the new kit per asset; and, when built with --heather-ab, the cards drawn instead
	if scene.has_method("set_shadow_after_bands"):
		states.append(["diag_shadow_before_bands", true, true, true, "shadow_before"])
	if scene.has_method("set_heather_wind"):
		states.append(["diag_heather_wind_off", true, true, true, "wind_off"])
		states.append(["diag_heather_push_off", true, true, true, "push_off"])
	for a2 in ["outcrop_a", "heather_base", "dead_tree", "boulder", "rocks", "stump", "skull"]:
		states.append(["asset_inst_no_" + a2, true, true, true, "asset:" + a2])
	if bool(scene.get("heather_ab")):
		states.append(["heather_as_cards", true, true, true, "rep:cards"])
	# where the heather's cost is: its shading (an unshaded flat material in its place) vs its
	# geometry and passes
	states.append(["diag_heather_flat_shaded", true, true, true, "heather_flat"])
	if not only.is_empty():
		states = states.filter(func(s): return String(s[0]) in only)
	# (per-asset "hide:<asset>" and "lod:<px>" diagnostics are kept in _diag for the next
	# budget question; the reported run measures the delivered configuration)
	var res := {}
	var res_gpu := {}
	var res_retry := {}
	for rep in reps:
		for s in states:
			var diag := String(s[4]) if s.size() > 4 else ""
			_diag(diag, true)
			var r := await _time(bool(s[1]), bool(s[2]), bool(s[3]), 140, SHOT)
			_diag(diag, false)
			if not res.has(s[0]):
				res[s[0]] = []
				res_gpu[s[0]] = []
				res_retry[s[0]] = []
			res[s[0]].append(r["ms_per_frame"])
			res_gpu[s[0]].append(r["gpu_ms"])
			res_retry[s[0]].append(int(r["attempts"]) - 1 + (1000 if int(r["undrawable_frames"]) > 0 else 0))
	scene.set_stack(true)
	if has_snow:
		scene.set_snowfield_visible(true)
	if has_density:
		scene.set_density_visible(true)
	var chk := await _time(true, true, true, 90, Vector2i(2880, 1620))
	var out := {"tag": tag, "_at": "1920x1080 MSAA 4x, walking in full kit, vsync off, ABAB x2",
				"has_snow": has_snow, "has_density": has_density, "states": {}}
	for nm in res:
		var a: Array = res[nm]
		var srt := a.duplicate()
		srt.sort()
		var tot := 0.0
		for v in a:
			tot += float(v)
		var med: float = float(srt[srt.size() / 2]) if srt.size() % 2 == 1 \
			else (float(srt[srt.size() / 2 - 1]) + float(srt[srt.size() / 2])) * 0.5
		var g: Array = res_gpu[nm].duplicate()
		g.sort()
		out["states"][nm] = {"ms": a, "mean_ms": snappedf(tot / float(a.size()), 0.01),
							 "median_ms": snappedf(med, 0.01),
							 "spread_ms": snappedf(float(srt[-1]) - float(srt[0]), 0.01),
							 "gpu_ms": res_gpu[nm], "gpu_median_ms": g[g.size() / 2],
							 "retakes": res_retry[nm]}
	out["instrument_check_2.25x_pixels_ms"] = chk["ms_per_frame"]
	out["instrument_check_retakes"] = int(chk["attempts"]) - 1
	out["_undrawable"] = "retakes: a sample re-taken because the window could not draw (occluded); 1000+ = still undrawable after 3"
	var props: Dictionary = scene.report.get("props", {})
	out["prop_triangles"] = props.get("triangles", -1)
	out["instancing"] = scene.report.get("instancing", {})
	out["density"] = scene.report.get("density", {})
	var f := FileAccess.open(out_dir + "/cost_%s.json" % tag, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("[cost] %s %s" % [tag, JSON.stringify(out["states"])])
	print("[cost] %s instrument 2.25x: %.2f ms" % [tag, float(chk["ms_per_frame"])])
	quit(0)


func _diag(which: String, on: bool) -> void:
	if which == "nodes":
		scene.set_instancing(not on)
		return
	if which == "no_mm_pens":
		scene.set_instanced_pens_visible(not on)
		return
	if which.begins_with("nodes+asset:"):
		scene.set_instancing(not on)
		scene.set_asset_visible(which.substr(12), not on)
		return
	if which.begins_with("asset:"):
		scene.set_asset_visible(which.substr(6), not on)
		return
	if which.begins_with("lod:"):
		vp.mesh_lod_threshold = float(which.substr(4)) if on else float(scene.LOD_THRESHOLD_PX)
		return
	if which.begins_with("hide:"):
		var asset := which.substr(5)
		var dr: Node3D = scene.get("_density_root")
		if dr != null:
			for c in dr.get_children():
				if String((c as Node).name).begins_with(asset + "_"):
					(c as Node3D).visible = not on
		return
	if which.begins_with("rep:"):
		scene.set_heather_representation(which.substr(4) if on else "stems")
		return
	match which:
		"heather_flat":
			for m in scene._mmis:
				if String(m.get_meta("asset", "")) != "heather":
					continue
				var gi := m as GeometryInstance3D
				if on:
					gi.set_meta("_mat", gi.material_override)
					var sm := StandardMaterial3D.new()
					sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
					sm.albedo_color = Color(0.5, 0.3, 0.1)
					gi.material_override = sm
				elif gi.has_meta("_mat"):
					gi.material_override = gi.get_meta("_mat")
		"shadow_before":
			scene.set_shadow_after_bands(not on)
		"wind_off":
			scene.set_heather_wind(not on)
		"push_off":
			scene.set_heather_push(not on)
		"no_cores":
			scene.set_heather_cores_visible(not on)
		"heather_sides_flipped":
			# the blades' shared material on the other culling shader while `on`, then back to
			# the one the scene was built with
			var two_now: bool = bool(scene.heather_two_sided) != on
			var code: String = PaintStack.WORLD_SHADER.replace("cull_back", "cull_disabled") if two_now \
				else PaintStack.WORLD_SHADER
			for m in scene._mmis:
				if String(m.get_meta("asset", "")) == "heather" and String(m.get_meta("part", "")) != "core":
					((m as GeometryInstance3D).material_override as ShaderMaterial).shader = PaintStack._shader(code)
		"rocks_upright":
			scene.set_rock_pose(on)
		"heather_blades_noshadow":
			for m in scene._mmis:
				if String(m.get_meta("asset", "")) == "heather" and String(m.get_meta("part", "")) != "core":
					(m as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF if on \
						else GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		"no_feather":
			scene.snow.material().set_shader_parameter("feather_m", 0.0 if on else scene.snow.feather_m)
		"no_shadows":
			scene.sun.shadow_enabled = not on
		"no_density_inks":
			var dr: Node3D = scene.get("_density_root")
			if dr != null:
				for mi in dr.find_children("*_ink", "MeshInstance3D", true, false):
					(mi as MeshInstance3D).visible = not on


func _time(stack: bool, snow_on: bool, density_on: bool, n: int, res: Vector2i) -> Dictionary:
	# A FRAME THE WINDOW CANNOT DRAW IS NOT RENDERED, and times as 7-11 ms (T10-1d: a full run's
	# 2.25x check read 10.9 against 17.1 at 1080p; single passes read 7.0 among 16.5s). On macOS
	# an OCCLUDED window cannot draw -- someone working at the Mac covers it -- and every
	# viewport in it is skipped. So a sample with any such frame is thrown away and re-taken,
	# up to three times, and the count is reported.
	for attempt in 3:
		var r := await _time_once(stack, snow_on, density_on, n, res)
		if int(r["undrawable_frames"]) == 0:
			r["attempts"] = attempt + 1
			return r
	var r2 := await _time_once(stack, snow_on, density_on, n, res)
	r2["attempts"] = 4
	return r2


func _time_once(stack: bool, snow_on: bool, density_on: bool, n: int, res: Vector2i) -> Dictionary:
	scene.set_stack(stack)
	if scene.has_method("set_snowfield_visible"):
		scene.set_snowfield_visible(snow_on)
		# SNOW OFF MEANS ALL OF IT: hidden AND not processing. Hiding the mesh alone left the
		# stamping and the 16 MB trail upload running in the "off" state, so the snow's cost
		# came out short by exactly its CPU side.
		if scene.get("snow") != null:
			scene.snow.set_physics_process(snow_on)
			scene.snow.set_process(snow_on)
	if scene.has_method("set_density_visible"):
		scene.set_density_visible(density_on)
	var prev := vp.size
	vp.size = res
	var prev_ticks := Engine.physics_ticks_per_second
	Engine.physics_ticks_per_second = 240
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	scene.place_knight(7.9, 5.1, "NE")
	for i in 40:
		scene.knight.drive_dir(Vector2(0.28, -0.96), false, DT)
		await process_frame
	# GPU TIME TOO (T10-1c): wall-clock per frame is what the player gets, and it is also what
	# every other session on this machine can move -- a run next door put 1-4 ms of spread into
	# single states. The viewport's measured GPU time is the renderer's own clock for THIS
	# viewport's passes; reported beside the wall clock, not instead of it.
	var rid := vp.get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(rid, true)
	var gpu := 0.0
	var gpu_n := 0
	var t0 := Time.get_ticks_usec()
	var undrawable := 0
	for i in n:
		scene.knight.drive_dir(Vector2(0.28, -0.96), false, DT)
		await process_frame
		if not DisplayServer.window_can_draw():
			undrawable += 1
		var g := RenderingServer.viewport_get_measured_render_time_gpu(rid)
		if g > 0.0:
			gpu += g
			gpu_n += 1
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	Engine.physics_ticks_per_second = prev_ticks
	vp.size = prev
	return {"ms_per_frame": snappedf(ms, 0.01), "undrawable_frames": undrawable,
			"gpu_ms": snappedf(gpu / float(maxi(gpu_n, 1)), 0.01) if gpu_n > 0 else -1.0}
