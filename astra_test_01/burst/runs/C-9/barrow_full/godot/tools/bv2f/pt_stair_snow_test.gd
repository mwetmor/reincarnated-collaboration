extends SceneTree
## BV2F lane PT, DEV-22 (R-C9-216): THE STAIR SNOW TEST -- LV's art level (scenes/bv2f_barrow_v2.tscn, read live), LV's
## static tread snow strips hidden, the DEV-22 tread snow built (scripts/bv2f/stair_snow.gd), him walked from the shelf
## up the stair (LV's route ramp, from the level itself) to the landing; stills at the foot, mid-climb and at the top,
## looking back over his prints. Movie Maker film when run with --write-movie (fixed 24 fps).
##   Godot --path godot --resolution 1920x1080 --fixed-fps 24 [--write-movie OUT.avi] --script res://tools/bv2f/pt_stair_snow_test.gd -- --out DIR

const DT := 1.0 / 24.0
const SETTLE_MIN := 72
const STAIR_SNOW := preload("res://scripts/bv2f/stair_snow.gd")

var scene
var k
var snow: SnowField
var out_dir := ""
var frame := 0
var phase := "settle"
var t_phase := 0
var route: Array = []
var wi := 0
var best := INF
var stall := 0
var shots := {}
var report := {"route_uv": [], "reached": [], "skipped": [], "stills": []}


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	for i in a.size():
		if a[i] == "--out" and i + 1 < a.size():
			out_dir = a[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load("res://scenes/bv2f_barrow_v2.tscn").instantiate()
	# HARD GUARD (conductor, after PID 78315): a scene whose script failed to load (LV's bv2f_level.gd mid-edit had a parse
	# error -> the root came up a bare Node3D with no ready_done) is fatal NOW, not a per-frame error for 85 minutes
	if scene.get_script() == null or not ("ready_done" in scene):
		printerr("[stair_snow] FATAL: the scene's script did not load (bv2f_level.gd parse error?) -- quitting")
		quit(1)
		return
	root.add_child(scene)


func _shot(name: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	img.save_png(out_dir.path_join(name + ".png"))
	report["stills"].append({"name": name, "frame": frame, "knight_uv": [snappedf(scene.knight_uv().x, 0.01), snappedf(scene.knight_uv().y, 0.01)]})


func _setup() -> void:
	k = scene.knight
	for fn in ["set_hud_visible", "set_overlay", "set_crucible_visible"]:
		if scene.has_method(fn):
			scene.call(fn, false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	# the sim -> world mapping the prep assumed (stair_snow_prep.py) against the Level node's own transform
	var sx := 3.0
	var sy := 15.0
	var sz := -2.0
	var w: Vector3 = scene.level.to_global(Vector3(sx, sz, sy))
	var c47 := cos(deg_to_rad(47.0))
	var s47 := sin(deg_to_rad(47.0))
	var want := Vector3(sx * c47 + sy * s47, sz, -sx * s47 + sy * c47)
	report["sim_to_world_err_m"] = snappedf(w.distance_to(want), 0.0001)
	# LV's static tread snow strips (slabs.stair_snow) give way to the 3D tread snow
	if scene.nodes.has("stair_snow"):
		(scene.nodes["stair_snow"] as Node3D).visible = false
		report["lv_stair_snow_hidden"] = true
	snow = STAIR_SNOW.build(scene, k, scene.fbm, scene.WIND)
	report["dev22"] = snow.get_meta("dev22") if snow != null else "BUILD FAILED"
	# the climb: LV's ramp (route.ramp: centre, downhill dir, length along), sim -> uv (u = x, v = -y)
	var R: Dictionary = scene.sim["route"]["ramp"]
	var c := Vector2(float(R["c_sim"][0]), float(R["c_sim"][1]))
	var d := Vector2(float(R["dir_sim"][0]), float(R["dir_sim"][1]))
	var half := float(R["along"]) * 0.5
	var pts := [c + d * (half + 1.6), c + d * (half - 0.3), c, c - d * (half - 0.6), c - d * (half + 1.4)]
	for p in pts:
		route.append(Vector2(p.x, -p.y))
	report["route_uv_plan"] = route.map(func(q): return [snappedf(q.x, 0.01), snappedf(q.y, 0.01)])


func _process(_delta: float) -> bool:
	frame += 1
	if scene == null or not is_instance_valid(scene) or scene.get_script() == null:
		return true
	if frame > 4800:   # a scene that never becomes ready (a script error) must not hold the heavy lock
		push_error("[stair_snow] gave up at frame %d in phase %s" % [frame, phase])
		return true
	if phase == "settle":
		if scene.get("ready_done") == true and frame >= SETTLE_MIN:
			_setup()
			scene.place_knight(route[0].x, route[0].y, "N")
			phase = "hold_in"
			t_phase = 0
		return false
	if phase == "hold_in":
		k.drive_dir(Vector2.ZERO, false, DT)
		t_phase += 1
		if t_phase == 10:
			_shot("stair_foot_before")
		if t_phase >= 18:
			phase = "walk"
			wi = 1
			best = INF
		return false
	if phase == "walk":
		var at: Vector2 = scene.knight_uv()
		var wp: Vector2 = route[wi]
		var dd := at.distance_to(wp)
		if dd < best - 0.02:
			best = dd
			stall = 0
		else:
			stall += 1
		if dd < 0.5 or stall > 96:
			(report["reached"] if dd < 0.5 else report["skipped"]).append([wi, [snappedf(at.x, 0.01), snappedf(at.y, 0.01)], frame])
			if wi == 2 and not shots.has("mid"):
				shots["mid"] = true
				_shot("stair_mid_climb")
			wi += 1
			best = INF
			stall = 0
			if wi >= route.size():
				phase = "hold_out"
				t_phase = 0
				return false
			wp = route[wi]
		k.drive_dir(scene.canvas_dir_uv(at, wp), false, DT)
		if frame % 6 == 0:
			report["route_uv"].append([snappedf(at.x, 0.01), snappedf(at.y, 0.01), snappedf(k.global_position.y, 0.01)])
		return false
	if phase == "hold_out":
		k.drive_dir(Vector2.ZERO, false, DT)
		t_phase += 1
		if t_phase == 20:
			_shot("stair_top_prints_below")
		if t_phase >= 36:
			report["frames"] = frame
			var f := FileAccess.open(out_dir.path_join("stair_snow_test.json"), FileAccess.WRITE)
			f.store_string(JSON.stringify(report, " "))
			f.close()
			print("[stair_snow] " + JSON.stringify({"reached": report["reached"].size(), "skipped": report["skipped"], "sim_err": report.get("sim_to_world_err_m")}))
			return true
	return false
