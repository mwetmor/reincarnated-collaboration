extends SceneTree
## BV2F lane PT (R-C9-191): THE PILOT WALK FILM for M2' -- him, armed as installed, in the painted pilot, on v1's film
## recipe (tools/film_painted.gd + film_painted.sh: Movie Maker, fixed 24 fps, one movie file, settling trimmed).
## He walks from the snow below the mere, along the shingle past the wreck, through the broken stone ring, up to the
## barrow door. Waypoints in (u, v); a waypoint he cannot reach in 4 s is skipped and reported (nothing is forced).
##   Godot --path godot --resolution 1920x1080 --fixed-fps 24 --write-movie OUT.avi --script res://tools/bv2f/pt_pilot_film.gd

const DT := 1.0 / 24.0
const SETTLE_MIN := 72
const HOLD_IN := 12
const HOLD_OUT := 36
const ROUTE := [Vector2(-10.0, 4.0), Vector2(-15.5, 1.5), Vector2(-13.0, -4.0), Vector2(-4.0, -2.5),
				Vector2(0.0, 1.0), Vector2(0.5, 7.0), Vector2(1.5, 13.6)]

var scene
var k
var frame := 0
var phase := "settle"
var t_phase := 0
var wi := 0
var best := INF
var stall := 0
var report := {"route_uv": [], "reached": [], "skipped": []}


func _initialize() -> void:
	scene = load("res://scenes/bv2f_pilot_painted.tscn").instantiate()
	root.add_child(scene)


func _process(_delta: float) -> bool:
	frame += 1
	if phase == "settle":
		if scene.ready_done and frame >= SETTLE_MIN:
			k = scene.knight
			scene.set_hud_visible(false)
			scene.set_overlay(false)
			scene.set_crucible_visible(false)
			for c in scene.get_children():
				if c is CanvasLayer:
					(c as CanvasLayer).visible = false
			scene.place_knight(ROUTE[0].x, ROUTE[0].y, "W")
			phase = "hold_in"
			t_phase = 0
			print("[film] {\"trim_frames\":%d}" % frame)
		return false
	if phase == "hold_in":
		k.drive_dir(Vector2.ZERO, false, DT)
		t_phase += 1
		if t_phase >= HOLD_IN:
			phase = "walk"
			wi = 1
			best = INF
		return false
	if phase == "walk":
		var at: Vector2 = scene.knight_uv()
		var wp: Vector2 = ROUTE[wi]
		var d := at.distance_to(wp)
		if d < best - 0.02:
			best = d
			stall = 0
		else:
			stall += 1
		if d < 0.6 or stall > 96:
			if d < 0.6:
				report["reached"].append([wi, [snappedf(at.x, 0.01), snappedf(at.y, 0.01)], frame])
			else:
				report["skipped"].append([wi, [snappedf(at.x, 0.01), snappedf(at.y, 0.01)], snappedf(d, 0.01)])
			wi += 1
			best = INF
			stall = 0
			if wi >= ROUTE.size():
				phase = "hold_out"
				t_phase = 0
				return false
			wp = ROUTE[wi]
		k.drive_dir(scene.canvas_dir_uv(at, wp), false, DT)
		if frame % 6 == 0:
			report["route_uv"].append([snappedf(at.x, 0.01), snappedf(at.y, 0.01)])
		return false
	if phase == "hold_out":
		k.drive_dir(Vector2.ZERO, false, DT)
		t_phase += 1
		if t_phase >= HOLD_OUT:
			report["frames"] = frame
			print("[film] " + JSON.stringify(report))
			return true
	return false
