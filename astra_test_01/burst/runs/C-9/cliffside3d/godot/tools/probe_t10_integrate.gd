extends SceneTree
# C-9 T10 integration — DOES THE REAL BARROW ACTUALLY LOAD, AND DOES EVERY PROP STAND ON IT.
#
# Headless, no pixels, no lock: this is the cheap check that has to pass before a capture is
# worth the twelve minutes it costs. It answers four questions that all have a plausible-
# looking wrong answer:
#
#   1. WHICH GROUND IS UNDER THE SCENE. `terrain_source.kind` must read back
#      heightfield_authored. The fallback to the stand-in is one line in a JSON and the
#      resulting scene looks finished.
#   2. DID THE 70 PLACEMENTS LAND. Counted per asset against the list, with the skips named.
#   3. DO THE PROPS STAND ON THE GROUND. verify_placements, on three instances chosen to be
#      different kinds of wrong if the pipeline is wrong: a tall stone (pitch stretch), the
#      lintel (the across axis) and a birch (the forced width).
#   4. ARE THE FOUR LOOK KEYS FREE.
#
#   Godot --headless --path godot --script tools/probe_t10_integrate.gd -- --out DIR

var out_dir := ""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("user://t10")
	DirAccess.make_dir_recursive_absolute(out_dir)

	var t0 := Time.get_ticks_msec()
	var scene = load("res://scenes/barrow.tscn").instantiate()
	root.add_child(scene)
	for i in 30:
		await process_frame
		await physics_frame
	var build_ms := Time.get_ticks_msec() - t0

	var rep: Dictionary = scene.report.duplicate(true)
	rep["scene_build_ms_wall"] = build_ms

	# --- 3. the three instances, by the numbers -----------------------------
	# CHOSEN FOR WHAT THEY WOULD CATCH, not for being convenient. A tall stone is the tallest
	# thing the pitch stretch touches, so a stretch that ran twice or not at all is a 66% or
	# 40% error on it. The lintel is the only asset sized by its ACROSS axis. The birch is the
	# only one with a forced non-uniform width.
	var want := ["stone_tall", "lintel", "birch"]
	var names: Array = scene.prop_names()
	var pick := []
	for w in want:
		for n in names:
			if String(n).begins_with(w + "_"):
				pick.append(n)
				break
	rep["three_instance_check"] = scene.verify_placements(pick)

	# EVERY prop's base gap, summarised -- three instances are the report, but a fourth that
	# floats is still a floating rock, and a max over all of them costs nothing.
	rep["all_prop_base_gaps"] = scene.verify_placements(names)["props"]
	var worst := -1e9
	var worst_nm := ""
	var n_float := 0
	for nm in rep["all_prop_base_gaps"]:
		var g = rep["all_prop_base_gaps"][nm].get("base_gap_m", null)
		if g == null:
			continue
		if float(g) > 0.0 and not bool(rep["all_prop_base_gaps"][nm].get("perched_by_design", false)):
			n_float += 1
		if bool(rep["all_prop_base_gaps"][nm].get("perched_by_design", false)):
			continue
		if float(g) > worst:
			worst = float(g)
			worst_nm = String(nm)
	rep["base_gap_summary"] = {"props": (rep["all_prop_base_gaps"] as Dictionary).size(),
		"floating_above_ground": n_float, "worst_gap_m": snappedf(worst, 0.001),
		"worst_prop": worst_nm,
		"_pass": "floating_above_ground == 0"}
	rep.erase("all_prop_base_gaps")

	rep["snow"] = scene.snow_report()

	var f := FileAccess.open(out_dir + "/t10_integrate.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[t10] ground=%s placed=%s floating=%d worst_gap=%.3f -> %s"
		% [JSON.stringify(rep.get("terrain_source", {}).get("kind", "?")),
		   JSON.stringify(rep.get("props", {}).get("placed", -1)),
		   n_float, worst, out_dir])
	quit(0)
