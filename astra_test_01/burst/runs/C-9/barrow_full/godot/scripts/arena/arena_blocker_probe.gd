extends SceneTree
## C-9 BV2F ARENA (R-C9-353) -- THE BLOCKER PROBE. Matt: "the player character gets sucked into the viking ship and
## cannot get out." For every blocker in data/arena/barrow_arena.json (and the wreck MODEL's own footprint), the
## player's capsule walks AT it from 8 bearings for 3 s through the arena's own motion code (arena_mode._move_proxy,
## the physics the game uses), then walks BACK to where he started for 3 s. A start is used only if he can stand there
## (after a 0.25 s settle his capsule is within 0.6 m of the walk surface: not inside a model, the mound or the sea).
## A trial FAILS if he ends the approach inside the blocker / the wreck footprint, or cannot get back within 1 m of
## his start. No sim ticks run (the fight is not started).
##   Godot --headless --path . --script res://scripts/arena/arena_blocker_probe.gd

const SPEED := 5.4
const APPROACH_S := 3.0
const AWAY_S := 3.0
const DT := 1.0 / 60.0

var main = null
var arena = null
var trials: Array = []
var ti := -1
var phase := ""
var t := 0.0
var target := Vector2.ZERO
var start_m := Vector2.ZERO
var fails := 0
var n_skipped := 0
var rows: Array = []


func _init() -> void:
	main = (load("res://scenes/bv2f_arena.tscn") as PackedScene).instantiate()
	root.add_child(main)
	process_frame.connect(_f)


func _boxes() -> Array:
	var out: Array = []
	for b_any in (arena.session.arena_cfg["blockers"] as Array):
		var b: Dictionary = b_any
		out.append({"id": String(b["id"]), "c": Vector2(float(b["centre_sim"][0]), float(b["centre_sim"][1])),
			"size": Vector2(float(b["size_m"][0]), float(b["size_m"][1])), "deg": float(b["axis_deg"])})
	return out


static func _inside(p: Vector2, bx: Dictionary) -> bool:
	var d: Vector2 = p - (bx["c"] as Vector2)
	var a := deg_to_rad(float(bx["deg"]))
	var along := d.dot(Vector2(cos(a), sin(a)))
	var across := d.dot(Vector2(-sin(a), cos(a)))
	return absf(along) <= (bx["size"] as Vector2).x * 0.5 and absf(across) <= (bx["size"] as Vector2).y * 0.5


func _f() -> void:
	if arena == null:
		arena = main.get("arena")
		return
	if arena.session == null or arena.snap.is_empty():
		return
	if trials.is_empty() and ti < 0:
		var boxes := _boxes()
		# the wreck MODEL's footprint (level.json sim.models.wreck: 13 x 4.63 m at the hull probe's angle)
		boxes.append({"id": "wreck_model_footprint", "c": Vector2(-27.1, -2.9), "size": Vector2(13.0, 4.63), "deg": 32.471})
		for bx in boxes:
			for k in 16:
				trials.append({"box": bx, "bearing": TAU * float(k) / 16.0})
		ti = 0
		_start()
		return
	for _i in 4:                                  # 4 physics-sized steps per frame: the probe runs ~4x real time
		_step()
		if ti >= trials.size():
			break
	if ti >= trials.size():
		print("[blocker_probe] %d trials: %d run, %d skipped (no standing or reachable start), %d FAIL" % [trials.size(), trials.size() - n_skipped, n_skipped, fails])
		for bx in _boxes() + [{"id": "wreck_model_footprint", "c": Vector2(-27.1, -2.9), "size": Vector2(13.0, 4.63), "deg": 32.471}]:
			var nin := 0
			for k in arena.walk_reach.size():
				if arena.walk_reach[k] == 0:
					continue
				var c := Vector2(arena.WALK_X0 + (float(k % arena.WALK_NX) + 0.5) * arena.WALK_CELL_M,
					arena.WALK_Y0 + (float(k / arena.WALK_NX) + 0.5) * arena.WALK_CELL_M)
				if _inside(c, bx):
					nin += 1
			print("[blocker_probe] %-26s reachable cells inside: %d" % [String(bx["id"]), nin])
		for r in rows:
			print("[blocker_probe] " + String(r))
		quit(0 if fails == 0 else 3)


func _start() -> void:
	var tr: Dictionary = trials[ti]
	var bx: Dictionary = tr["box"]
	var reach := maxf((bx["size"] as Vector2).x, (bx["size"] as Vector2).y) * 0.5 + 4.0
	var c: Vector2 = bx["c"]
	var s := c + Vector2(cos(tr["bearing"]), sin(tr["bearing"])) * reach
	start_m = s - arena.T
	arena.player_pos_m = start_m
	arena._place_proxy(start_m)
	target = c - arena.T
	phase = "settle"
	t = 0.0


func _step() -> void:
	var tr: Dictionary = trials[ti]
	var bx: Dictionary = tr["box"]
	if phase == "settle":
		arena.player_pos_m = arena._move_proxy(arena.player_pos_m, DT)
		t += DT
		if t >= 0.25:
			var s: Vector2 = start_m + arena.T
			var floor_y: float = float(arena.scene.floor_y_at(s.x, -s.y))
			var kk: int = arena._cell(start_m)
			if kk >= 0 and arena.walk_reach[kk] == 0:
				rows.append("%-26s bearing %3d  start %s  SKIPPED: not reachable from the fight centre" % [
					String(bx["id"]), int(round(rad_to_deg(float(tr["bearing"])))), str(s.snapped(Vector2(0.01, 0.01)))])
				n_skipped += 1
				ti += 1
				if ti < trials.size():
					_start()
				return
			if absf(float(arena.proxy.global_position.y) - floor_y) > 0.6 or arena.player_pos_m.distance_to(start_m) > 0.6:
				rows.append("%-26s bearing %3d  start %s  SKIPPED: cannot stand there (capsule y %.2f, walk surface %.2f)" % [
					String(bx["id"]), int(round(rad_to_deg(float(tr["bearing"])))), str(s.snapped(Vector2(0.01, 0.01))),
					float(arena.proxy.global_position.y), floor_y])
				n_skipped += 1
				ti += 1
				if ti < trials.size():
					_start()
				return
			phase = "in"
			t = 0.0
		return
	var goal: Vector2 = target if phase == "in" else start_m
	var to: Vector2 = goal - arena.player_pos_m
	var stp := SPEED * DT
	var want: Vector2 = goal if to.length() <= stp else arena.player_pos_m + to.normalized() * stp
	arena.player_pos_m = arena._move_proxy(want, DT)
	t += DT
	if phase == "in" and t >= APPROACH_S:
		tr["end_in"] = arena.player_pos_m + arena.T
		tr["inside"] = _inside(tr["end_in"], bx)
		tr["h_in"] = float(arena.proxy.global_position.y)
		phase = "out"
		t = 0.0
		tr["ledge0"] = int(arena.n_ledge_refusals)
	elif phase == "out" and t >= AWAY_S:
		var away: float = (arena.player_pos_m + arena.T).distance_to(tr["end_in"])
		var back: float = arena.player_pos_m.distance_to(start_m)
		var ok: bool = not bool(tr["inside"]) and back <= 1.0
		if not ok:
			fails += 1
		rows.append("%-26s bearing %3d  start %s (h %.2f)  end %s  inside %s  h %.2f  walked away %.2f m  %s" % [
			String(bx["id"]), int(round(rad_to_deg(float(tr["bearing"])))), str((start_m + arena.T).snapped(Vector2(0.01, 0.01))), arena.walk_h(start_m),
			str((tr["end_in"] as Vector2).snapped(Vector2(0.01, 0.01))), str(tr["inside"]), float(tr["h_in"]), away,
			("ok" if ok else "FAIL (%.2f m short of the start; ledge refusals %d; last contact %s)" % [back,
				int(arena.n_ledge_refusals) - int(tr["ledge0"]), _last_contact()])])
		ti += 1
		if ti < trials.size():
			_start()


func _last_contact() -> String:
	var c: KinematicCollision3D = arena.proxy.get_last_slide_collision()
	if c == null or c.get_collider() == null:
		return "-"
	var n: Node = c.get_collider() as Node
	return "%s/%s n=%s" % [str(n.get_parent().name) if n.get_parent() != null else "", str(n.name), str(c.get_normal().snapped(Vector3(0.01, 0.01, 0.01)))]
