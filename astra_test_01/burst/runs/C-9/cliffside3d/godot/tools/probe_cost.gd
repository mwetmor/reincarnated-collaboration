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
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--tag" and i + 1 < args.size():
			tag = args[i + 1]
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
	# (per-asset "hide:<asset>" and "lod:<px>" diagnostics are kept in _diag for the next
	# budget question; the reported run measures the delivered configuration)
	var res := {}
	for rep in 2:
		for s in states:
			var diag := String(s[4]) if s.size() > 4 else ""
			_diag(diag, true)
			var r := await _time(bool(s[1]), bool(s[2]), bool(s[3]), 140, SHOT)
			_diag(diag, false)
			if not res.has(s[0]):
				res[s[0]] = []
			res[s[0]].append(r["ms_per_frame"])
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
		out["states"][nm] = {"ms": a, "mean_ms": snappedf((float(a[0]) + float(a[1])) * 0.5, 0.01),
							 "spread_ms": snappedf(absf(float(a[0]) - float(a[1])), 0.01)}
	out["instrument_check_2.25x_pixels_ms"] = chk["ms_per_frame"]
	var props: Dictionary = scene.report.get("props", {})
	out["prop_triangles"] = props.get("triangles", -1)
	out["density"] = scene.report.get("density", {})
	var f := FileAccess.open(out_dir + "/cost_%s.json" % tag, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("[cost] %s %s" % [tag, JSON.stringify(out["states"])])
	print("[cost] %s instrument 2.25x: %.2f ms" % [tag, float(chk["ms_per_frame"])])
	quit(0)


func _diag(which: String, on: bool) -> void:
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
	match which:
		"no_shadows":
			scene.sun.shadow_enabled = not on
		"no_density_inks":
			var dr: Node3D = scene.get("_density_root")
			if dr != null:
				for mi in dr.find_children("*_ink", "MeshInstance3D", true, false):
					(mi as MeshInstance3D).visible = not on


func _time(stack: bool, snow_on: bool, density_on: bool, n: int, res: Vector2i) -> Dictionary:
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
	var t0 := Time.get_ticks_usec()
	for i in n:
		scene.knight.drive_dir(Vector2(0.28, -0.96), false, DT)
		await process_frame
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	Engine.physics_ticks_per_second = prev_ticks
	vp.size = prev
	return {"ms_per_frame": snappedf(ms, 0.01)}
