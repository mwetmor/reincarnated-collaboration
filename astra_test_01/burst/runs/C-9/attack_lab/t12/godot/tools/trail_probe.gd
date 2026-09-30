extends SceneTree
# T12_11 STRIKE TRAIL PROBE -- each strike fired through the scene's tree (guard_accept.gd's way: a
# settled guard, the one-shot, drive_dir with no input), the knight's StrikeTrail stepped by hand after
# every tree step (trail_auto off). Two passes per strike:
#   GAME   1/PROBE_GAME_HZ s steps (default 60, the game's physics tick): per frame the clip position, the
#          trail's alpha, its samples; the edge line of every strike's own trail spec (named by its clip) and
#          of the exploration candidates (the shield's rim diameters) in world space; and the trail's strip
#   FINE   1/192 s steps, no trail: the TRUE continuous sweep of the same edge lines -- what the eye
#          would see at 192 fps -- for the coverage measure (nb_d2 scratch analysis)
# env: KNIGHT, KNIGHT_CHARACTER, PROBE_OUT, PROBE_STRIKES (default slash,chop,bash), PROBE_GAME_HZ (default 60)
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
var k
var skel: Skeleton3D
var tree: AnimationTree
var edges := {}
var out_edges := {}

func _initialize() -> void:
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(4000, 1, 4000)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	k = load(OS.get_environment("KNIGHT") if OS.has_environment("KNIGHT") else "res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.trail_auto = false
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel; tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var spec: Dictionary = k.cfg.get("strike_trail", {})
	var clips: Dictionary = spec.get("clips", {})
	# the candidate edge lines: every clip's own, plus the shield's two diameters for the bash
	edges["axe"] = {"bone": "weapon_r", "edge": clips["attack"]["edge"]}
	for cn in clips:
		edges[cn] = {"bone": String(clips[cn]["bone"]), "edge": clips[cn]["edge"]}
	var cand: Dictionary = spec.get("_candidates_shield", {})
	for nm in cand:
		edges["shield_" + nm] = {"bone": "LeftHand", "edge": cand[nm]}
	out_edges = edges
	var out := {"strikes": {}, "trail_spec": spec, "edges": out_edges}
	var strikes: PackedStringArray = (OS.get_environment("PROBE_STRIKES") if OS.has_environment("PROBE_STRIKES") else "slash,chop,bash").split(",")
	for key in strikes:
		var game := _fire(key, 1.0 / (float(OS.get_environment("PROBE_GAME_HZ")) if OS.has_environment("PROBE_GAME_HZ") else 60.0), true)
		var fine := _fire(key, 1.0 / 192.0, false)
		out["strikes"][key] = {"game": game, "fine": fine}
		print("[trail] %s: %d game frames, %d fine; clip %s" % [key, game["rows"].size(), fine["rows"].size(), game.get("clip", "?")])
	var f := FileAccess.open(OS.get_environment("PROBE_OUT") if OS.has_environment("PROBE_OUT") else "/tmp/trail_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out)); f.close()
	quit(0)

func _step(dt: float, with_trail: bool) -> void:
	k.drive_dir(Vector2.ZERO, false, dt)
	tree.advance(dt)
	skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	if with_trail:
		k.trail_step(dt)

func _pt(bone: String, p: Array) -> Vector3:
	var b := skel.find_bone(bone)
	return skel.global_transform * (skel.get_bone_global_pose(b) * Vector3(float(p[0]), float(p[1]), float(p[2])))

func _v(p: Vector3) -> Array:
	return [snappedf(p.x, 0.00001), snappedf(p.y, 0.00001), snappedf(p.z, 0.00001)]

func _fire(key: String, dt: float, with_trail: bool) -> Dictionary:
	k.set_block(false)
	for i in int(2.0 / dt): _step(dt, with_trail)
	k.global_position = Vector3(0, 0.03, 0); k.velocity = Vector3.ZERO
	for i in 4: _step(dt, with_trail)
	var out := {"dt": dt, "rows": []}
	if not k.try_strike(key):
		print("[trail] %s: try_strike refused" % key)
		return out
	var ended := -1
	var n_max := int(14.0 / dt)
	for i in n_max:
		_step(dt, with_trail)
		var active: bool = bool(tree.get("parameters/os_%s/active" % key))
		var pos: float = float(tree.get("parameters/a_%s/current_position" % key))
		var row := {"i": i, "active": active, "pos": pos}
		if active:
			out["clip"] = String((tree.tree_root as AnimationNodeBlendTree).get_node("a_" + key).animation)
		for nm in edges:
			var e: Dictionary = edges[nm]
			row[nm] = [_v(_pt(String(e["bone"]), e["edge"][0])), _v(_pt(String(e["bone"]), e["edge"][1]))]
		if with_trail and k._trail != null:
			row["alpha"] = float(k._trail.alpha)
			row["n_samples"] = (k._trail.samples as Array).size()
			row["fade_t"] = float(k._trail.fade_t)
			var strip := []
			for q in (k._trail.last_pts as Array):
				strip.append([_v(q[0]), _v(q[1]), snappedf(float(q[2]), 0.0001)])
			row["strip"] = strip
		out["rows"].append(row)
		if not active and ended < 0:
			ended = i
		if ended >= 0 and i - ended > int(0.5 / dt):
			break
	for i in 6: _step(dt, with_trail)
	return out
