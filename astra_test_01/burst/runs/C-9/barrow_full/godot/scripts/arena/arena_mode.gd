extends Node3D
## C-9 BV2F ARENA (R-C9-345/347/348) -- THE KC2 WAVE FIGHT, BROUGHT TO BARROW_V2.
##
## The same fight: the KC2 runtime UNMODIFIED (sim + play/driver layer, referenced through res://kc2/kc2_runtime),
## the pack of record, waves 151-160, the graded rules PLAY runs, every monster the waves bring, the warlord as the only
## hero with KC2's controls and kit. What changes (R-C9-348): the six spawn points sit on barrow_v2's features
## (arena_session.gd), the crucible's floor-hazard pools are dropped, the doorways + wreck hull + gable rubble are
## impassable blockers, and the player walks barrow_v2's own ground.
##
## This node is the KC2 view's ROOT (kc2_play/src/kc2p_main.gd), re-hosted in the 3D scene:
##   input -> intents -> one sim tick (at the model's 12.25 Hz, frames accumulate into ticks) -> view.
## The view may post INTENTS and nothing else, as KC2's. The one difference in kind: the player's planar motion between
## ticks goes through a capsule on barrow_v2's walk colliders (the terrain, the bounds walls, the models, the blockers),
## where KC2's view tested its polygon mask; the sim samples that position at each tick boundary exactly as it sampled
## KC2's, and a sim correction still SNAPS him.
##
## CONTROLS (KC2's): hold LMB = move to the cursor (Shift+LMB = stand), LMB click = Charge (blitz), hold RMB = Whirlwind
## (eye_of_reckoning), 1 Potion, 2 Might (vires_might), 3 Battle Cry (war_cry), 4 Haste (rune_of_rush) (numpad too), Z zoom, N bars, R restart, C / F12 capture, Esc quit.

const ArenaSession = preload("res://scripts/arena/arena_session.gd")
const Kc2PlayRecorder = preload("res://kc2/kc2_runtime/play/kc2play_recorder.gd")
const Kc2RtViewContract = preload("res://kc2/kc2_runtime/sim/kc2rt_view_contract.gd")
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")
const J = preload("res://scripts/arena/arena_art.gd")
const Monster3D = preload("res://scripts/arena/arena_monster3d.gd")
const Warlord3D = preload("res://scripts/arena/arena_warlord3d.gd")
const ArenaHud = preload("res://scripts/arena/arena_hud.gd")
const ArenaNumbers = preload("res://scripts/arena/arena_numbers.gd")
var numbers = null
const Token3D = preload("res://scripts/arena/arena_token3d.gd")

const GEOM := "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json"
const FEEL_ONLY := true
const KC2_GD_PPM := 75.66840334752658          # KC2's ZOOM-GD px per metre: Z switches the barrow camera to it
const CAP_R := 0.35
const CAP_H := 1.8
const GRAVITY := 18.0
## ORTHO CAMERA, SO A CARD MAY SLIDE ALONG THE VIEW RAY WITHOUT MOVING ON SCREEN: every billboard is drawn this far
## toward the camera from its ground point, so the part of the strip below the feet (shadow, cloak, a big body's
## lower half) is not cut off where the screen-facing card dips into the ground behind it.
const CARD_TOWARD_CAM_M := 2.0
const EOR_TOWARD_CAM_M := 1.5
## R-C9-363: THE PAINTED PLATE (level.json frame.envelope, the site_ph3 painting): the camera's view never leaves it,
## and the player never stands within PLATE_MARGIN_M of its edge (the walk map's boundary).
const PLATE_U := Vector2(-33.57573954303182, 32.57573954303182)
const PLATE_V := Vector2(-28.633937157286354, 22.36993715728635)
const PLATE_MARGIN_M := 1.5
## ⚑ R-C9-365 (Matt: "do not worry about any fixes for this right now ... at the very end"): the R-C9-363 camera clamp,
##   zoom cap and plate boundary are UNWIRED behind this flag (false). The R-C9-364 mist stopgap was never written.
const EDGE_FIXES_R_C9_363 := false

var scene = null                    # the barrow scene (bv2f_arena.gd)
var session = null
var recorder = null
var T := Vector2.ZERO               # the fight centre in barrow sim = KC2 (0, 0)
var sea_z := -4.5
var seed_used: int = 0
var running := false
var fight_started := false
var fatal := ""
var accum := 0.0
var sim_hz := 12.25
var intents: Dictionary = {}
var snap: Dictionary = {}
var pending_presses: Array = []
var last_events: Array = []
var player_pos_m := Vector2.ZERO    # KC2 frame
var move_target_m: Variant = null
var proxy: CharacterBody3D = null
var warlord = null
var actors: Dictionary = {}         # actor id -> Monster3D
var actors_root: Node3D = null
var hud = null
var zoomed_out := false
var show_bars := true
var shots := 0
var debug_on := false
var n_blocked_stops := 0
var waves_seen: Dictionary = {}
var kits_seen: Dictionary = {}
var no_pack: Dictionary = {}
var no_pack_records: Dictionary = {}    # R-C9-356: record -> {family, n, waves, r_body, placeholder}
var placeholder_table: Dictionary = {}  # record -> row (data/arena/placeholder_bodies.json)
const PLACEHOLDER_JSON := "res://data/arena/placeholder_bodies.json"
var _by_type: Dictionary = {}
var _names: Dictionary = {}
const NAMES_JSON := "res://data/arena/display_names.json"


## R-C9-357: the generic on-screen name of a record (display only): its kit's name, else its type's, else "Creature".
func display_name(rec: String, kit: String, champion: bool) -> String:
	if _names.is_empty():
		var j: Variant = JSON.parse_string(FileAccess.get_file_as_string(NAMES_JSON)) if FileAccess.file_exists(NAMES_JSON) else null
		_names = j if typeof(j) == TYPE_DICTIONARY else {"_none": true}
	var nm := ""
	if kit != "" and (_names.get("by_kit", {}) as Dictionary).has(kit):
		nm = String(_names["by_kit"][kit])
	if nm == "":
		var ty := String(placeholder_table.get(rec, {}).get("type", "")) if placeholder_table.has(rec) else ""
		if ty == "":
			ty = String(J.record_entry(rec).get("family", J.record_entry(rec).get("type_id", "")))
		nm = String((_names.get("by_type", {}) as Dictionary).get(ty, "Creature"))
	return nm + (String(_names.get("champion_suffix", " Champion")) if champion else "")


## The oracle's own body radius for a record (ge_fold.r_body = actorRadius x scale; 0.5 the oracle's fallback).
func _r_body(rec: String) -> float:
	var ge = session.fight.get("ge_fold")
	if ge != null and (ge.r_body as Dictionary).has(rec):
		return float(ge.r_body[rec])
	return 0.5


## R-C9-356: a record with no art drawn with an existing kit, scaled so its radius is the record's: the kit's own
## reference radius (its mapped records' actorRadius / factor, the median) -> factor = r_body(rec) / r_ref.
func _placeholder_entry(rec: String) -> Dictionary:
	if placeholder_table.is_empty():
		var j: Variant = JSON.parse_string(FileAccess.get_file_as_string(PLACEHOLDER_JSON)) if FileAccess.file_exists(PLACEHOLDER_JSON) else null
		placeholder_table = {"_loaded": true}
		if typeof(j) == TYPE_DICTIONARY:
			_by_type = (j as Dictionary).get("by_type", {})
			for r_any in ((j as Dictionary).get("rows", []) as Array):
				placeholder_table[String((r_any as Dictionary)["record"])] = r_any
	var kit := ""
	if placeholder_table.has(rec):
		kit = String((placeholder_table[rec] as Dictionary)["placeholder_kit"])
	else:
		var ty := String(J.record_entry(rec).get("family", ""))
		kit = String(_by_type.get(ty, ""))
	if kit == "":
		return {}
	if J.kit_meta(kit).is_empty():
		return {}
	var refs: Array = []
	for rr_any in (J.index().get("record_map", {}) as Dictionary).values():
		var rr: Dictionary = rr_any
		if String(rr.get("kit", "")) == kit and rr.get("actorRadius_m", null) != null and float(rr.get("factor", 0.0)) > 0.0:
			refs.append(float(rr["actorRadius_m"]) * float(rr.get("roster_scale", 1.0)) / float(rr["factor"]))
	refs.sort()
	var r_ref: float = float(refs[refs.size() / 2]) if not refs.is_empty() else 0.75
	return {"kind": "kit", "kit": kit, "factor": clampf(_r_body(rec) / maxf(r_ref, 0.05), 0.3, 4.0), "placeholder": true}
var eor_t0_tick := 0
var autopilot := ""                 # "--arena-auto" smoke mode (no human): see _auto()
## smoke/evidence instruments (command-line only; unset in play): timed captures, a quit timer, a top-down view
var shot_dir := ""
var shot_every_s := 0.0
var quit_after_s := 0.0
var topdown := false
var _wall_s := 0.0
var _next_shot_s := 0.0
var _f0 := -1


static func _arg(args: PackedStringArray, key: String, dflt: String) -> String:
	var i := args.find(key)
	return String(args[i + 1]) if i >= 0 and i + 1 < args.size() else dflt


func setup(sc) -> void:
	scene = sc
	debug_on = OS.get_environment("BV2F_ARENA_DEBUG") == "1"
	var args := OS.get_cmdline_user_args()
	if "--arena-auto" in args:
		autopilot = "on"
	shot_dir = _arg(args, "--arena-shot-dir", "")
	shot_every_s = float(_arg(args, "--arena-shot-every", "0"))
	quit_after_s = float(_arg(args, "--arena-quit-s", "0"))
	topdown = "--arena-topdown" in args
	sea_z = float((scene.sim as Dictionary).get("sea_z", -4.5))
	var cl := CanvasLayer.new()
	cl.layer = 5
	add_child(cl)
	hud = ArenaHud.new()
	hud.set_anchors_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cl.add_child(hud)
	hud.bind(self)
	actors_root = Node3D.new()
	actors_root.name = "ArenaActors"
	add_child(actors_root)
	numbers = ArenaNumbers.new()
	numbers.name = "DamageNumbers"
	add_child(numbers)
	numbers.setup(scene.cam)
	_build_proxy()
	if not J.ok():
		_fatal("JOIN-1 art index missing: " + J._index_error)
		return
	seed_used = int(Time.get_unix_time_from_system()) & 0x7fffffff
	_boot()


# --------------------------------------------------------------------------------------------- the session
func _boot() -> void:
	fatal = ""
	session = ArenaSession.new()
	if not session.open(Kc2RtPackOfRecord.MODEL_DIR, Kc2RtPackOfRecord.MODEL_DIGEST, GEOM, seed_used, "ZOOM-GD", true):
		_fatal("SESSION OPEN FAILED\n" + String(session.load_error))
		return
	if not session.fold_ok:
		_fatal("BARROW FOLD REFUSED\n" + String(session.fold.get("error", "")))
		return
	session.driver.banner_placement_m = Vector2.ZERO      # as kc2p_main: the banner at the start (= the fight centre)
	T = Vector2(float(session.arena_cfg["fight_centre_sim"][0]), float(session.arena_cfg["fight_centre_sim"][1]))
	_build_blockers()
	_build_prop_colliders()
	await get_tree().physics_frame                 # the blockers' shapes are in the space before the walk map is cast
	_build_walk_map()
	player_pos_m = session.fight.player_pos
	move_target_m = null
	_place_proxy(player_pos_m)
	intents = Kc2RtViewContract.empty_intents()
	recorder = Kc2PlayRecorder.new()
	var out := "user://telemetry/barrow-arena-%s-%d.jsonl" % [session.run_id, seed_used]
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://telemetry"))
	if not recorder.open(ProjectSettings.globalize_path(out), session.header(FEEL_ONLY)):
		_fatal("RECORDER FAILED\n" + String(recorder.last_error))
		return
	for c in actors_root.get_children():
		c.queue_free()
	actors.clear()
	if warlord != null:
		warlord.queue_free()
	warlord = Warlord3D.new()
	warlord.name = "Warlord"
	actors_root.add_child(warlord)
	warlord.setup()
	running = true
	fight_started = autopilot != ""
	accum = 0.0
	pending_presses = []
	snap = session.snapshot()
	_render(0.0)
	print("[arena] open: seed %d, runtime %s, fight centre %s, spawn points %s, pools dropped %d, telemetry %s" % [
		seed_used, _runtime_digest().substr(0, 12), str(T), _anchors_line(), int(session.fold.get("pools_dropped", -1)),
		ProjectSettings.globalize_path(out)])


func _runtime_digest() -> String:
	var j: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://kc2/kc2_runtime/MANIFEST.json"))
	return String((j as Dictionary).get("tree_digest", "?")) if typeof(j) == TYPE_DICTIONARY else "?"


func _anchors_line() -> String:
	var parts := []
	var sp: Dictionary = session.board.spawn_points
	var ks := sp.keys()
	ks.sort()
	for k in ks:
		parts.append("%s(%.2f,%.2f)" % [k, float(sp[k]["x"]) + T.x, float(sp[k]["y"]) + T.y])
	return " ".join(parts)


func _fatal(msg: String) -> void:
	fatal = msg
	running = false
	push_error("[arena] " + msg)


func _close_recording(why: String) -> void:
	if recorder != null and recorder.open_ok and session != null:
		var r: Dictionary = session.report()
		r["closed_by"] = why
		recorder.close(r)


func _notification(what: int) -> void:
	if what == NOTIFICATION_PREDELETE:
		_close_recording("tree_exit")


func quit_arena() -> void:
	_close_recording("quit")
	get_tree().quit()


# --------------------------------------------------------------------------------------------- frames
## KC2 frame <-> barrow world. barrow sim (x, y) = (u, -v); KC2 = barrow sim - T.
func ground_h(m: Vector2) -> float:
	var s := m + T
	return maxf(float(scene.floor_y_at(s.x, -s.y)), sea_z)


func to_world(m: Vector2, lift := 0.0) -> Vector3:
	var s := m + T
	return scene.uv_to_world(s.x, -s.y, ground_h(m) + lift)


func world_to_m(p: Vector3) -> Vector2:
	var uv: Vector2 = scene.world_to_uv(p)
	return Vector2(uv.x, -uv.y) - T


func _sim_to_world(s: Vector2, h: float) -> Vector3:
	return scene.uv_to_world(s.x, -s.y, h)


# --------------------------------------------------------------------------------------------- the player's body
func _build_proxy() -> void:
	proxy = CharacterBody3D.new()
	proxy.name = "ArenaPlayerCapsule"
	proxy.collision_layer = 0
	proxy.collision_mask = int(scene.TERRAIN_BIT)
	var cs := CollisionShape3D.new()
	var cap := CapsuleShape3D.new()
	cap.radius = CAP_R
	cap.height = CAP_H
	cs.shape = cap
	cs.position = Vector3(0, CAP_H * 0.5, 0)
	proxy.add_child(cs)
	add_child(proxy)


func _place_proxy(m: Vector2) -> void:
	proxy.global_position = to_world(m, 0.03)
	proxy.velocity = Vector3.ZERO


## Move the capsule toward `want` (KC2 frame) by physics; return where it ended (KC2 frame).
## R-C9-353 (Matt: "the player character gets sucked into the viking ship and cannot get out"). CAUSE, measured by
## scripts/arena/arena_blocker_probe.gd: the wreck lies in a basin 4.2 m below the plateau behind a 60-70 deg bank (and
## its hull blocker was smaller than the ship). The capsule slid off the bank's lip, dropped to the shore ice, and could
## not climb a face steeper than its 45 deg floor -- a pit (8 of 9 standing starts round the wreck never got back).
## FIX: THE WALK MAP, the KC2 view's walkable-mask rule rebuilt from barrow_v2's own colliders. At load, one ray per
## WALK_CELL_M cell straight down onto the walk colliders (terrain, models, bounds, blockers) gives the surface height
## and its normal. A cell is FLOOR if its normal is within WALK_MAX_DEG of up. A step is taken only onto floor whose
## height is within WALK_STEP_M of the floor he stands on -- so he never steps onto a bank, a cliff face or a rock top,
## and never off a lip. Physics still does the motion (walls, the slide); a slide that ends off the map is undone.
const WALK_CELL_M := 0.25
const WALK_MAX_DEG := 40.0        # 5 deg under the capsule's 45 deg floor_max_angle
const WALK_STEP_M := 0.30
const WALK_STEP_UP_M := 0.60         # most height change accepted between the cell he is on and the one he steps to
const WALK_X0 := -42.0            # the level's sim extent (level.json sim.heightfield.extent_sim_m)
const WALK_Y0 := -36.0
const WALK_NX := 336
const WALK_NY := 288
var walk_hgt := PackedFloat32Array()   # surface height per cell (NAN = nothing below)
var walk_ok := PackedByteArray()       # 1 = floor
var walk_reach := PackedByteArray()    # 1 = reachable from the start over floor steps
var walk_built_ms := 0
var n_ledge_refusals := 0


func walk_h(m: Vector2) -> float:
	var s := m + T
	return float(scene.floor_y_at(s.x, -s.y))


func _build_walk_map() -> void:
	if not walk_ok.is_empty():
		return
	var t0 := Time.get_ticks_msec()
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var q := PhysicsRayQueryParameters3D.new()
	q.collision_mask = int(scene.TERRAIN_BIT)
	q.collide_with_areas = false
	walk_hgt.resize(WALK_NX * WALK_NY)
	walk_ok.resize(WALK_NX * WALK_NY)
	var cmax := cos(deg_to_rad(WALK_MAX_DEG))
	for j in WALK_NY:
		# the ray sits OFF the cell centre: centres fall on the heightmap's own vertices (8 per metre), where a ray
		#   returns an edge's normal -- a regular grid of false "steep" cells across flat ground
		var y := WALK_Y0 + (float(j) + 0.5) * WALK_CELL_M + 0.0371
		for i in WALK_NX:
			var x := WALK_X0 + (float(i) + 0.5) * WALK_CELL_M + 0.0529
			var top: Vector3 = scene.uv_to_world(x, -y, 40.0)
			q.from = top
			q.to = top - Vector3(0.0, 60.0, 0.0)
			var hit: Dictionary = space.intersect_ray(q)
			var k := j * WALK_NX + i
			if hit.is_empty():
				walk_hgt[k] = NAN
				walk_ok[k] = 0
			else:
				walk_hgt[k] = float((hit["position"] as Vector3).y)
				walk_ok[k] = 1 if (hit["normal"] as Vector3).y >= cmax else 0
	# R-C9-363: THE FIGHT BOUNDARY -- no floor within PLATE_MARGIN_M of the painted plate's edge
	var n_edge := 0
	for j in (WALK_NY if EDGE_FIXES_R_C9_363 else 0):
		for i in WALK_NX:
			var k := j * WALK_NX + i
			if walk_ok[k] == 0:
				continue
			var cx := WALK_X0 + (float(i) + 0.5) * WALK_CELL_M
			var cv := -(WALK_Y0 + (float(j) + 0.5) * WALK_CELL_M)
			if cx < PLATE_U.x + PLATE_MARGIN_M or cx > PLATE_U.y - PLATE_MARGIN_M or cv < PLATE_V.x + PLATE_MARGIN_M or cv > PLATE_V.y - PLATE_MARGIN_M:
				walk_ok[k] = 0
				n_edge += 1
	if EDGE_FIXES_R_C9_363:
		print("[arena] walk map plate boundary: %d cells off" % n_edge)
	# keep-outs (barrow_arena.json walk_keepout): low ground he could get into and not out of -- the wreck's basin
	var n_keep := 0
	for ko_any in (session.arena_cfg.get("walk_keepout", []) as Array):
		var ko: Dictionary = ko_any
		var kc := Vector2(float(ko["centre_sim"][0]), float(ko["centre_sim"][1]))
		var kr := float(ko["radius_m"])
		var kh := float(ko["below_h_m"])
		for j in WALK_NY:
			for i in WALK_NX:
				var k := j * WALK_NX + i
				if walk_ok[k] == 0 or is_nan(walk_hgt[k]):
					continue
				var c := Vector2(WALK_X0 + (float(i) + 0.5) * WALK_CELL_M, WALK_Y0 + (float(j) + 0.5) * WALK_CELL_M)
				if c.distance_to(kc) <= kr and walk_hgt[k] < kh:
					walk_ok[k] = 0
					n_keep += 1
	print("[arena] walk map keep-outs: %d cells" % n_keep)
	# what he can REACH from the start, over floor steps (4-neighbour flood fill): the probe's and the report's measure
	walk_reach.resize(WALK_NX * WALK_NY)
	walk_reach.fill(0)
	var k0 := _cell(Vector2.ZERO)
	if k0 >= 0 and walk_ok[k0] == 1:
		var stack := PackedInt32Array([k0])
		walk_reach[k0] = 1
		while not stack.is_empty():
			var k := stack[stack.size() - 1]
			stack.resize(stack.size() - 1)
			var ci := k % WALK_NX
			var cj := k / WALK_NX
			for dd in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
				var ni: int = ci + dd.x
				var nj: int = cj + dd.y
				if ni < 0 or nj < 0 or ni >= WALK_NX or nj >= WALK_NY:
					continue
				var nk := nj * WALK_NX + ni
				if walk_reach[nk] == 1 or walk_ok[nk] == 0 or absf(walk_hgt[nk] - walk_hgt[k]) > WALK_STEP_M:
					continue
				walk_reach[nk] = 1
				stack.append(nk)
	walk_built_ms = Time.get_ticks_msec() - t0
	var n := 0
	for v in walk_ok:
		n += int(v)
	var nr := 0
	for v in walk_reach:
		nr += int(v)
	print("[arena] walk map: %d x %d cells @ %.2f m, %d floor (%.0f m2), %d reachable from the start (%.0f m2), built in %d ms" % [
		WALK_NX, WALK_NY, WALK_CELL_M, n, float(n) * WALK_CELL_M * WALK_CELL_M, nr, float(nr) * WALK_CELL_M * WALK_CELL_M,
		walk_built_ms])


func _cell(m: Vector2) -> int:
	var s := m + T
	var i := int(floor((s.x - WALK_X0) / WALK_CELL_M))
	var j := int(floor((s.y - WALK_Y0) / WALK_CELL_M))
	if i < 0 or j < 0 or i >= WALK_NX or j >= WALK_NY:
		return -1
	return j * WALK_NX + i


## May he step from `a` to `b` (KC2 frame)? Floor cell, and a height change he could walk.
## `feet_y` (his capsule's actual height) is the reference when given: the cell he stands in is sampled at one point,
## and comparing cell to cell could leave a pocket whose only open neighbour is the diagonal he came in by.
func walk_step_ok(a: Vector2, b: Vector2, feet_y: float = NAN) -> bool:
	if walk_ok.is_empty():
		return true
	var kb := _cell(b)
	if kb < 0 or walk_ok[kb] == 0:
		return false
	var ka := _cell(a)
	if ka == kb:
		return true
	var ref: float = feet_y
	if is_nan(ref):
		if ka < 0 or is_nan(walk_hgt[ka]):
			return true
		ref = walk_hgt[ka]
	# down: at most WALK_STEP_M (a drop he could climb back); up: WALK_STEP_UP_M (the capsule decides if it can climb)
	var dh: float = walk_hgt[kb] - ref
	return dh <= WALK_STEP_UP_M and -dh <= WALK_STEP_M


func _move_proxy(want: Vector2, delta: float) -> Vector2:
	var old_tf := proxy.global_transform
	var old_m := world_to_m(old_tf.origin)
	# R-C9-359 (Matt: "makes you stick to it instead of slide around it"): a refused step is not dropped -- it is
	# PROJECTED along the boundary (the first of the step's directions turned 25 / 50 / 75 deg either way, scaled by
	# the cosine, that the map allows), so he glides along an edge as he does along a wall
	var fy := old_tf.origin.y
	if want.distance_to(old_m) > 1e-5 and not walk_step_ok(old_m, want, fy):
		n_ledge_refusals += 1
		want = _slide(old_m, want - old_m, fy)
	var d := want - player_pos_m
	var s := d + Vector2.ZERO
	var disp: Vector3 = scene.u_hat * s.x - scene.v_hat * s.y
	var vy := proxy.velocity.y - GRAVITY * delta
	proxy.velocity = Vector3(disp.x / maxf(delta, 1e-6), vy, disp.z / maxf(delta, 1e-6))
	proxy.move_and_slide()
	if proxy.is_on_floor():
		proxy.velocity.y = 0.0
	var new_m := world_to_m(proxy.global_position)
	if new_m.distance_to(old_m) > 1e-5 and not walk_step_ok(old_m, new_m, fy):
		# the physics slide ended off the map: back, then the projected step along the edge, if there is one
		n_ledge_refusals += 1
		var alt := _slide(old_m, new_m - old_m, fy)
		proxy.global_transform = old_tf
		proxy.velocity = Vector3.ZERO
		if alt.distance_to(old_m) > 1e-5:
			var k := _cell(alt)
			var h: float = walk_hgt[k] if k >= 0 and not is_nan(walk_hgt[k]) else old_tf.origin.y
			proxy.global_position = scene.uv_to_world((alt + T).x, -(alt + T).y, maxf(h, old_tf.origin.y - 0.3) + 0.02)
			return alt
		return old_m
	return new_m


const SLIDE_ANGLES_DEG := [25.0, -25.0, 50.0, -50.0, 75.0, -75.0]


func _slide(a: Vector2, step: Vector2, feet_y: float = NAN) -> Vector2:
	for ang_d in SLIDE_ANGLES_DEG:
		var ang := deg_to_rad(float(ang_d))
		var d := step.rotated(ang) * cos(ang)
		if walk_step_ok(a, a + d, feet_y):
			return a + d
	return a


# --------------------------------------------------------------------------------------------- the blockers
func _build_blockers() -> void:
	var old: Node = scene.get_node_or_null("ArenaBlockers")
	if old != null:
		return                                  # built once; a restart keeps them
	var body := StaticBody3D.new()
	body.name = "ArenaBlockers"
	body.collision_layer = int(scene.TERRAIN_BIT)
	body.collision_mask = 0
	scene.add_child(body)
	for b_any in (session.arena_cfg.get("blockers", []) as Array):
		var b: Dictionary = b_any
		var c := Vector2(float(b["centre_sim"][0]), float(b["centre_sim"][1]))
		var sz: Array = b["size_m"]
		var z: Array = b["z_m"]
		var phi := deg_to_rad(float(b["axis_deg"]))
		# the box's local X = its 'along' axis, at sim angle phi; sim (x, y) -> world u_hat*x - v_hat*y
		var ax_w: Vector3 = (scene.u_hat * cos(phi) - scene.v_hat * sin(phi)).normalized()
		var bx := BoxShape3D.new()
		bx.size = Vector3(float(sz[0]), float(z[1]) - float(z[0]), float(sz[1]))
		var cs := CollisionShape3D.new()
		cs.shape = bx
		var basis := Basis(ax_w, Vector3.UP, ax_w.cross(Vector3.UP).normalized() * -1.0)
		cs.transform = Transform3D(basis.orthonormalized(), _sim_to_world(c, (float(z[0]) + float(z[1])) * 0.5))
		cs.name = String(b["id"])
		body.add_child(cs)
		if debug_on:
			var mi := MeshInstance3D.new()
			var bm := BoxMesh.new()
			bm.size = bx.size
			mi.mesh = bm
			var mat := StandardMaterial3D.new()
			mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			mat.albedo_color = Color(1.0, 0.2, 0.2, 0.35)
			mat.render_priority = 127
			mi.material_override = mat
			mi.transform = cs.transform
			body.add_child(mi)
	if debug_on:
		_build_debug_marks()


func _build_debug_marks() -> void:
	var root := Node3D.new()
	root.name = "ArenaDebug"
	scene.add_child(root)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = Color(0.1, 1.0, 1.0)
	mat.no_depth_test = true
	mat.render_priority = 127
	for pid in (session.arena_cfg["anchors"] as Dictionary).keys():
		var a: Array = session.arena_cfg["anchors"][pid]["sim"]
		var s := Vector2(float(a[0]), float(a[1]))
		var im := ImmediateMesh.new()
		im.surface_begin(Mesh.PRIMITIVE_LINE_STRIP, mat)
		for i in 65:
			var ang := TAU * float(i) / 64.0
			var q := s + Vector2(cos(ang), sin(ang)) * 8.0
			im.surface_add_vertex(_sim_to_world(q, maxf(float(scene.floor_y_at(q.x, -q.y)), sea_z) + 0.1))
		im.surface_end()
		im.surface_begin(Mesh.PRIMITIVE_LINES, mat)
		for k in 40:
			var q0 := s.lerp(T, float(k) / 40.0)
			var q1 := s.lerp(T, float(k + 1) / 40.0)
			im.surface_add_vertex(_sim_to_world(q0, maxf(float(scene.floor_y_at(q0.x, -q0.y)), sea_z) + 0.1))
			im.surface_add_vertex(_sim_to_world(q1, maxf(float(scene.floor_y_at(q1.x, -q1.y)), sea_z) + 0.1))
		im.surface_end()
		var mi := MeshInstance3D.new()
		mi.mesh = im
		root.add_child(mi)
		var lb := Label3D.new()
		lb.text = String(pid)
		lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		lb.no_depth_test = true
		lb.pixel_size = 0.02
		lb.font_size = 48
		lb.modulate = Color(0.1, 1.0, 1.0)
		lb.render_priority = 127
		lb.position = _sim_to_world(s, maxf(float(scene.floor_y_at(s.x, -s.y)), sea_z) + 1.0)
		root.add_child(lb)


# --------------------------------------------------------------------------------------------- input
func handle_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and not e.echo:
		var k := (e as InputEventKey).keycode
		match k:
			KEY_ESCAPE:
				quit_arena()
				return
			KEY_Z:
				_toggle_zoom()
				return
			KEY_N:
				show_bars = not show_bars
				return
			KEY_C, KEY_F12:
				_shot()
				return
			KEY_R:
				_restart()
				return
	if not running:
		return
	if not fight_started:
		if (e is InputEventMouseButton and e.pressed) or (e is InputEventKey and e.pressed and (e as InputEventKey).keycode == KEY_SPACE):
			fight_started = true
			accum = 0.0
			pending_presses = []
		return
	if e is InputEventMouseButton and e.pressed and (e as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		pending_presses.append({"skill_id": "blitz", "aim_m": _cursor_arr()})
	if e is InputEventKey and e.pressed and not e.echo:
		var kc := (e as InputEventKey).keycode
		var sid := ""
		if kc in [KEY_1, KEY_KP_1]:
			sid = "potion"
		elif kc in [KEY_2, KEY_KP_2]:
			sid = "vires_might"
		elif kc in [KEY_3, KEY_KP_3]:
			sid = "war_cry"
		elif kc in [KEY_4, KEY_KP_4]:
			sid = "rune_of_rush"
		if sid != "":
			pending_presses.append({"skill_id": sid, "aim_m": _cursor_arr()})


## The cursor on the ground: the camera ray through the mouse, met with the horizontal plane through his feet.
func _cursor_m() -> Vector2:
	var cam: Camera3D = scene.cam
	var mp := get_viewport().get_mouse_position()
	var o := cam.project_ray_origin(mp)
	var n := cam.project_ray_normal(mp)
	var y0 := proxy.global_position.y
	if absf(n.y) < 1e-6:
		return player_pos_m
	var t := (y0 - o.y) / n.y
	return world_to_m(o + n * t)


func _cursor_arr() -> Array:
	var c := _cursor_m()
	return [c.x, c.y]


func _toggle_zoom() -> void:
	zoomed_out = not zoomed_out
	var base := float(scene._view_height()) / float(scene.PPM)
	var want := base * (float(scene.PPM) / KC2_GD_PPM if zoomed_out else 1.0)
	# R-C9-363: never a view larger than the painted plate in either axis
	var p := deg_to_rad(float(scene.PL_PITCH_DEG))
	var asp := float(scene._view_width()) / maxf(1.0, float(scene._view_height()))
	var pw := (PLATE_U.y - PLATE_U.x)
	var ph := (PLATE_V.y - PLATE_V.x) * sin(p)
	scene.cam.size = minf(want, minf(ph, pw / asp) * 0.98) if EDGE_FIXES_R_C9_363 else want
	scene._sync_post_scale()


func _shot() -> String:
	var img := get_viewport().get_texture().get_image()
	if img == null:
		return ""
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://captures"))
	var p := ProjectSettings.globalize_path("user://captures/barrow_arena_%d_%03d.png" % [Time.get_ticks_msec(), shots])
	img.save_png(p)
	shots += 1
	print("[arena] capture -> ", p)
	return p


func _restart() -> void:
	_close_recording("restart")
	running = false
	seed_used = (seed_used + 7919) & 0x7fffffff
	_boot()


# --------------------------------------------------------------------------------------------- the loop
func _process(delta: float) -> void:
	_instruments(delta)
	if session == null:
		return
	if running and fight_started:
		_frame(delta)
	elif warlord != null:
		warlord.advance(delta)
	_render(delta)


func _frame(delta: float) -> void:
	if autopilot != "":
		_auto()
	elif Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not Input.is_key_pressed(KEY_SHIFT):
		move_target_m = _cursor_m()
	# ---- the F1 rider: the player integrates AT RENDER RATE (through barrow_v2's colliders) ----
	var speed: float = session.fight.v_ref_speed
	var tgt: Variant = move_target_m
	var charging: bool = session.driver.charge_to != null
	if charging:
		tgt = session.driver.charge_to
		speed = session.driver.charge_speed
	if tgt != null:
		var t: Vector2 = tgt
		var to := t - player_pos_m
		var step := speed * delta
		var want := t if to.length() <= step else player_pos_m + to.normalized() * step
		var got := _move_proxy(want, delta)
		var made := (got - player_pos_m).length()
		var asked := (want - player_pos_m).length()
		player_pos_m = got
		if (t - player_pos_m).length() <= 0.05:
			move_target_m = null
			if charging:
				session.driver.charge_arrived()
		elif asked > 1e-4 and made < asked * 0.25:
			# blocked by barrow_v2 (a wall, a model, a blocker): he STOPS, as KC2's view stops on a refusal
			n_blocked_stops += 1
			if debug_on and n_blocked_stops % 50 == 1:
				var col := proxy.get_last_slide_collision()
				print("[arena] blocked at %s (barrow sim %s) asked %.3f made %.3f by %s" % [str(player_pos_m), str(player_pos_m + T),
					asked, made, str(col.get_collider().get_parent().name) + "/" + str(col.get_collider().name) if col != null else "-"])
			move_target_m = null
			if charging:
				session.driver.charge_arrived()
	else:
		player_pos_m = _move_proxy(player_pos_m, delta)       # gravity only: settle on the ground
	accum += delta
	var period := 1.0 / sim_hz
	var guard := 0
	while accum >= period and running and guard < 8:
		accum -= period
		guard += 1
		_one_tick()


func _one_tick() -> void:
	sim_hz = session.fight.ticks_per_s
	session.fight.player_pos = player_pos_m
	intents["move_target_m"] = null if move_target_m == null else \
		[float((move_target_m as Vector2).x), float((move_target_m as Vector2).y)]
	intents["channel_held"] = _channel_held()
	intents["skill_pressed"] = pending_presses
	intents["toggle_zoom"] = false
	intents["restart"] = false
	pending_presses = []
	var term: String = session.step(intents)
	if session.fight.player_pos != player_pos_m:
		player_pos_m = session.fight.player_pos
		move_target_m = null
		_place_proxy(player_pos_m)
	snap = session.snapshot()
	waves_seen[int(snap.get("wave", 0))] = true
	last_events = session.stream.events.duplicate(true)
	recorder.tick(session.stream, snap, session.fight)
	_consume_events(last_events)
	hud.consume_events(last_events)
	if term != "":
		running = false
		recorder.close(session.report())
		print("[arena] RUN OVER: %s at wave %d, tick %d (waves seen %s; kits %s; no-pack families %s; blocked stops %d)" % [
			term, int(session.fight.terminal_wave), int(session.fight.run_tick), str(waves_seen.keys()),
			str(kits_seen.keys()), str(no_pack.keys()), n_blocked_stops])


func _channel_held() -> bool:
	if autopilot != "":
		return _auto_channel
	return Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)


func _consume_events(evs: Array) -> void:
	for e_any in evs:
		var e: Dictionary = e_any
		var ev := String(e.get("event", ""))
		if ev in ["channel_on", "channel_off", "player_death"] or (ev == "cast_start" and int(e.get("actor_id", -1)) == 0):
			if ev == "channel_on":
				eor_t0_tick = int(session.fight.run_tick)      # R-C9-352: the source clock starts at the cast's tick
			warlord.on_event(e)
			continue
		if ev == "cast_start":
			var t = actors.get(int(e.get("actor_id", 0)), null)
			if t != null:
				t.on_cast_start(String(e.get("skill_id", "")), Vector2(float(e.get("aim_x_m", 0.0)), float(e.get("aim_y_m", 0.0))))
		elif ev == "hit" and int(e.get("dst_id", 0)) != 0:
			var t2 = actors.get(int(e["dst_id"]), null)
			if t2 != null:
				t2.on_hit()
				# R-C9-367: the numbers the warlord DEALS, over the body hit (NUM-POP style)
				if int(e.get("src_id", -1)) == 0 and numbers != null:
					numbers.show_hit(to_world(t2.pos_m) + Vector3.UP * (float(t2.true_height_m) * 0.5),
						float(e.get("amount", 0.0)), String(e.get("damage_type", "physical")), bool(e.get("crit", false)),
						int(e["dst_id"]))
		elif ev == "death" and int(e.get("actor_id", 0)) != 0:
			var t3 = actors.get(int(e["actor_id"]), null)
			if t3 != null:
				t3.on_death()


# --------------------------------------------------------------------------------------------- the view
func _render(delta: float) -> void:
	if session == null or snap.is_empty():
		return
	var tick: int = int(snap.get("tick", 0))
	var wave_s: float = float(snap.get("wave_elapsed_s", 0.0))
	var body_by_vid: Dictionary = {}
	var enter_by_vid: Dictionary = {}
	for b_any in session.fight.bodies:
		var bd: Dictionary = b_any
		if bd.has("_vid"):
			body_by_vid[int(bd["_vid"])] = bd
			enter_by_vid[int(bd["_vid"])] = int(bd.get("enter_tick", 0))
	var wave_local: int = roundi(wave_s * float(session.fight.ticks_per_s))
	var seen := {}
	for a_any in (snap.get("actors", []) as Array):
		var a: Dictionary = a_any
		var id := int(a["id"])
		seen[id] = true
		var t = actors.get(id, null)
		if t == null:
			var rec := String(a.get("record_path", ""))
			var entry := J.record_entry(rec)
			if String(entry.get("kind", "")) == "kit" and not J.kit_meta(String(entry["kit"])).is_empty():
				kits_seen[String(entry["kit"])] = true
				t = Monster3D.new()
			else:
				# a record with no JOIN-1 pack (KC2 draws a token). R-C9-356: a PLACEHOLDER body from an existing kit
				# (data/arena/placeholder_bodies.json), scaled to the record's own sim radius; a token only if none
				var fam := String(entry.get("family", rec))
				no_pack[fam] = true
				var nr: Dictionary = no_pack_records.get(rec, {"family": fam, "n": 0, "waves": {}, "r_body": _r_body(rec),
					"placeholder": ""})
				nr["n"] = int(nr["n"]) + 1
				(nr["waves"] as Dictionary)[int(snap.get("wave", 0))] = true
				var ph := _placeholder_entry(rec)
				if not ph.is_empty():
					nr["placeholder"] = String(ph["kit"])
					no_pack_records[rec] = nr
					t = Monster3D.new()
					entry = ph
				else:
					no_pack_records[rec] = nr
					t = Token3D.new()
			t.setup_monster(session, a, entry)
			# R-C9-357: never a Grim Dawn name or a file name on screen
			t.label = display_name(rec, String(J.record_entry(rec).get("kit", entry.get("kit", ""))) if String(J.record_entry(rec).get("kind", "")) == "kit" else "", bool(a.get("is_hero", false)))
			actors_root.add_child(t)
			actors[id] = t
		t.hold_ticks_left = int(enter_by_vid.get(id, 0)) - wave_local
		t.sync_actor(a, body_by_vid.get(id, {}), player_pos_m, wave_s, tick)
	for k_any in actors.keys():
		var m = actors[k_any]
		if not seen.has(int(k_any)):
			if not m.dying:
				m.on_death()
			if m.faded_out():
				m.queue_free()
				actors.erase(k_any)
				continue
		m.advance_monster(delta)
		m.position = to_world(m.pos_m + (m.lunge_offset_m if m is Token3D else Vector2.ZERO)) \
			- (scene.fwd * CARD_TOWARD_CAM_M if not (m is Token3D) else Vector3.ZERO)
	if warlord != null:
		warlord.sync(player_pos_m, session.driver)
		warlord.advance(delta)
		warlord.position = proxy.global_position - scene.fwd * CARD_TOWARD_CAM_M
		# R-C9-352: the source clock -- revolutions = (sim ticks since the cast + the frame's fraction of a tick) x
		#   tick period / the source's 0.36 s per revolution; it runs on after the release so the cuts finish
		var tp := 1.0 / maxf(float(session.fight.ticks_per_s), 1e-6)
		var revs := (float(int(session.fight.run_tick) - eor_t0_tick) * tp + (accum if running and fight_started else 0.0)) / 0.36
		# the smoke's floor is the SNOW surface he visibly stands on (eor_kc2_fx PORT 2's rule; synthetic binding skips it)
		var st: Vector3 = proxy.global_position
		var sn = scene.get("snow")
		if sn != null and sn.has_method("depth_at"):
			st.y = maxf(st.y, float(sn.get("floor_y")) + float(sn.depth_at(Vector2(st.x, st.z))))
		# ...and, like the cards, slid along the ortho view ray toward the camera (the same pixels on screen), so the
		# flat bed disc is not cut where the snow rises behind him
		warlord.drive_eor(st - scene.fwd * EOR_TOWARD_CAM_M, revs, scene.u_hat, scene.v_hat)
	if topdown:
		var c := T + Vector2(0.0, -2.0)
		scene.set_topdown(Vector2(c.x, -c.y), 62.0)
	else:
		var aim: Vector3 = scene.aim_for(proxy.global_position)
		if EDGE_FIXES_R_C9_363:
			aim = _clamp_to_plate(aim)
		scene.look_at_world(aim)
		if scene.snowfall != null:          # the walk scene's _process does this for the knight (R-C9-362)
			scene.snowfall.global_position = aim + scene.up * 9.0 - scene.fwd * 6.0
		_snow_feet(delta)
	hud.queue_redraw()


# --------------------------------------------------------------------------------------------- smoke autopilot
## `-- --arena-auto`: NO HUMAN. Holds the channel and walks toward the nearest released body, so a headless-free
## windowed smoke can carry the fight through the waves. Only ever posts intents (move target + channel level).
var _auto_channel := false
var _auto_rest := false
var _auto_blocked_seen := 0
var _auto_home_until := 0.0
var _auto_side := true
var _auto_detour := Vector2.ZERO


func _auto() -> void:
	var best := Vector2.INF
	var bd := INF
	for a_any in (snap.get("actors", []) as Array):
		var a: Dictionary = a_any
		if String(a.get("state", "")) != "ENGAGE":
			continue
		var p := Vector2(float(a["x_m"]), float(a["y_m"]))
		var d := p.distance_to(player_pos_m)
		if d < bd:
			bd = d
			best = p
	# energy hysteresis: the channel drains it and a dry-out ends the run (the runtime's rule)
	var ef: float = float(session.fight.energy) / maxf(1.0, float(session.fight.energy_usable_ceiling))
	if ef < 0.15:
		_auto_rest = true
	elif ef > 0.45:
		_auto_rest = false
	_auto_channel = bd < 4.0 and not _auto_rest
	if n_blocked_stops != _auto_blocked_seen:
		_auto_blocked_seen = n_blocked_stops
		if _wall_s >= _auto_home_until:
			# walled off: sidestep (alternating sides) for a second, then carry on (no pathing here, as in the fight)
			var want := (best if best != Vector2.INF else Vector2.ZERO) - player_pos_m
			var side := Vector2(-want.y, want.x).normalized() * (1.0 if _auto_side else -1.0)
			_auto_side = not _auto_side
			_auto_detour = player_pos_m + side * 4.0 - want.normalized() * 1.0
			_auto_home_until = _wall_s + 1.0
	if _wall_s < _auto_home_until:
		move_target_m = _auto_detour
	else:
		move_target_m = null if best == Vector2.INF or bd < 1.5 else best
	var hp: float = float(session.fight.player_hp)
	var hpm: float = maxf(1.0, float(session.fight.player_hp_max))
	if not pending_presses.is_empty():
		return
	if hp / hpm < 0.5 and float(session.driver.cd_left.get("potion", 0.0)) <= 0.0:
		pending_presses.append({"skill_id": "potion", "aim_m": [player_pos_m.x, player_pos_m.y]})
	elif bd < 5.0 and float(session.driver.cd_left.get("war_cry", 0.0)) <= 0.0:
		pending_presses.append({"skill_id": "war_cry", "aim_m": [player_pos_m.x, player_pos_m.y]})


func _instruments(delta: float) -> void:
	if _f0 < 0:
		_f0 = Engine.get_process_frames()
	_wall_s += delta
	if autopilot != "" and session != null and not running and String(session.terminal) != "" and quit_after_s > 0.0:
		quit_after_s = minf(quit_after_s, _wall_s + 2.0)     # the smoke ends 2 s after RUN OVER / cleared
	if shot_dir != "" and shot_every_s > 0.0 and _wall_s >= _next_shot_s and _wall_s > 1.0:
		_next_shot_s = _wall_s + shot_every_s
		var img := get_viewport().get_texture().get_image()
		if img != null:
			DirAccess.make_dir_recursive_absolute(shot_dir)
			var w := int(snap.get("wave", 0)) if not snap.is_empty() else 0
			img.save_png(shot_dir.path_join("arena_%05.1fs_w%d.png" % [_wall_s, w]))
	if quit_after_s > 0.0 and _wall_s >= quit_after_s:
		quit_after_s = 0.0
		print("[arena] frames %d in %.1f s = %.1f fps average" % [Engine.get_process_frames() - _f0, _wall_s, float(Engine.get_process_frames() - _f0) / maxf(_wall_s, 1e-3)])
		for rk in no_pack_records.keys():
			var nr2: Dictionary = no_pack_records[rk]
			print("[arena] no-art record %s family %s n %d waves %s r_body %.3f placeholder %s" % [rk, nr2["family"], int(nr2["n"]),
				str((nr2["waves"] as Dictionary).keys()), float(nr2["r_body"]), String(nr2["placeholder"])])
		print("[arena] quit timer: wave %d, running %s, terminal '%s', actors %d, kits %s, no-pack %s, blocked stops %d" % [
			int(snap.get("wave", 0)) if not snap.is_empty() else 0, str(running),
			String(session.terminal) if session != null else "-", actors.size(), str(kits_seen.keys()),
			str(no_pack.keys()), n_blocked_stops])
		quit_arena()



# --------------------------------------------------------------------------------------------- R-C9-363: the plate
## The camera's centre clamped so the whole ortho view stays on the painted plate (any zoom, any aspect). Near an
## edge the camera stops and he walks off-centre.
func _clamp_to_plate(aim: Vector3) -> Vector3:
	var cam: Camera3D = scene.cam
	var p := deg_to_rad(float(scene.PL_PITCH_DEG))
	var t := aim.y / maxf(-float(scene.fwd.y), 1e-6)
	var g: Vector3 = aim + scene.fwd * t                  # the aim's ground point along the view
	var uv: Vector2 = scene.world_to_uv(g)
	var half_h := cam.size * 0.5                            # metres of screen height (KEEP_HEIGHT)
	var half_w := half_h * float(scene._view_width()) / maxf(1.0, float(scene._view_height()))
	var fu := half_w
	var fv := half_h / sin(p)                               # screen-up metres -> ground v metres
	var cu := clampf(uv.x, PLATE_U.x + fu, PLATE_U.y - fu) if PLATE_U.x + fu <= PLATE_U.y - fu else (PLATE_U.x + PLATE_U.y) * 0.5
	var cv := clampf(uv.y, PLATE_V.x + fv, PLATE_V.y - fv) if PLATE_V.x + fv <= PLATE_V.y - fv else (PLATE_V.x + PLATE_V.y) * 0.5
	return scene.uv_to_world(cu, cv)


# --------------------------------------------------------------------------------------------- R-C9-362: props
## Props the walk scene draws but gives no collider (the palisade's posts and gate, the standing stones, logs, the
## wreck's mast, the door posts): a player-only box on each, from its own mesh bounds -- only where a ray onto the
## prop's centre finds no collider at its top already.
const PROP_IDS := ["palisade", "ring_stones", "slope_stones", "ring_fallen", "logs", "wreck_mast", "door_post_L",
	"door_post_R", "sea_stacks", "crags"]
const PROP_MIN_H_M := 0.35
const PROP_SHRINK := 0.85
var n_prop_colliders := 0


func _build_prop_colliders() -> void:
	if scene.get_node_or_null("ArenaPropColliders") != null:
		return
	var body := StaticBody3D.new()
	body.name = "ArenaPropColliders"
	body.collision_layer = int(scene.TERRAIN_BIT)
	body.collision_mask = 0
	scene.add_child(body)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var q := PhysicsRayQueryParameters3D.new()
	q.collision_mask = int(scene.TERRAIN_BIT)
	for id_any in (scene.nodes as Dictionary).keys():
		var id := String(id_any)
		var base := id.split("__")[0].rstrip("0123456789_")
		if not PROP_IDS.has(base):
			continue
		var root: Node3D = scene.nodes[id]
		var meshes: Array = scene._meshes(root)
		if meshes.is_empty():
			continue
		var ab := AABB()
		var first := true
		for mi in meshes:
			var m3 := mi as MeshInstance3D
			if m3.mesh == null or not m3.visible:
				continue
			var b: AABB = m3.global_transform * m3.mesh.get_aabb()
			ab = b if first else ab.merge(b)
			first = false
		if first or ab.size.y < PROP_MIN_H_M:
			continue
		var c := ab.get_center()
		q.from = Vector3(c.x, ab.end.y + 2.0, c.z)
		q.to = Vector3(c.x, ab.position.y - 2.0, c.z)
		var hit: Dictionary = space.intersect_ray(q)
		if not hit.is_empty() and float((hit["position"] as Vector3).y) >= ab.end.y - 0.3:
			continue                                      # it already has a collider at its top
		var bx := BoxShape3D.new()
		bx.size = Vector3(maxf(0.2, ab.size.x * PROP_SHRINK), ab.size.y, maxf(0.2, ab.size.z * PROP_SHRINK))
		var cs := CollisionShape3D.new()
		cs.shape = bx
		cs.position = c
		cs.name = id
		body.add_child(cs)
		n_prop_colliders += 1
	print("[arena] prop colliders added: %d (player only)" % n_prop_colliders)


# --------------------------------------------------------------------------------------------- R-C9-362: the snow
## The walk scene's snow fields carve under the knight's foot bones (SnowField.track). The arena's warlord is a card,
## so his feet are stepped here: alternate left/right prints one stride apart along his motion, the field's own
## _stamp/_puff/_plough with its own constants (the same carve the knight's feet make).
var _snow_last := Vector2.INF
var _snow_side := 1.0
var no_snow_feet := "--arena-no-snowfeet" in OS.get_cmdline_user_args()   # perf A/B instrument only


func _snow_feet(_delta: float) -> void:
	if no_snow_feet:
		return
	var fields: Array = []
	for f in [scene.get("snow"), scene.get("stair_snow")]:
		if f != null and f.has_method("_stamp"):
			fields.append(f)
	if fields.is_empty() or proxy == null:
		return
	var w: Vector3 = proxy.global_position
	var here := Vector2(w.x, w.z)
	if _snow_last == Vector2.INF:
		_snow_last = here
		return
	var mv := here - _snow_last
	var stride: float = float(fields[0].get("stamp_stride_m"))
	if mv.length() < stride:
		return
	var fwd := mv.normalized()
	_snow_last = here
	_snow_side = -_snow_side
	var foot := here + Vector2(-fwd.y, fwd.x) * 0.12 * _snow_side
	for f in fields:
		var D: float = float(f.depth_at(foot))
		if D <= 0.0:
			continue
		var deep: bool = D > float(f.get("plough_depth_m"))
		f._stamp(foot, fwd, float(f.get("boot_len_m")) * 0.5, float(f.get("boot_w_m")) * 0.5, float(f.get("boot_rim_m")),
			float(f.get("plough_berm_mult")) if deep else 1.0)
		if bool(f.get("puffs")):
			f._puff(Vector3(foot.x, float(f.get("floor_y")) + minf(D, 0.5) * 0.5, foot.y), fwd, D, deep)
		if deep and f.has_method("_plough"):
			f._plough(foot, fwd, D)
