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
## CONTROLS (KC2's): hold LMB = move to the cursor (Shift+LMB = stand), LMB click = Blitz, hold RMB = Eye of Reckoning,
## 1 potion, 2 Vire's Might, 3 War Cry, 4 Rune of Rush (numpad too), Z zoom, N bars, R restart, C / F12 capture, Esc quit.

const ArenaSession = preload("res://scripts/arena/arena_session.gd")
const Kc2PlayRecorder = preload("res://kc2/kc2_runtime/play/kc2play_recorder.gd")
const Kc2RtViewContract = preload("res://kc2/kc2_runtime/sim/kc2rt_view_contract.gd")
const Kc2RtPackOfRecord = preload("res://kc2/kc2_runtime/kc2rt_pack_of_record.gd")
const J = preload("res://scripts/arena/arena_art.gd")
const Monster3D = preload("res://scripts/arena/arena_monster3d.gd")
const Warlord3D = preload("res://scripts/arena/arena_warlord3d.gd")
const ArenaHud = preload("res://scripts/arena/arena_hud.gd")
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
func _move_proxy(want: Vector2, delta: float) -> Vector2:
	var d := want - player_pos_m
	var s := d + Vector2.ZERO
	var disp: Vector3 = scene.u_hat * s.x - scene.v_hat * s.y
	var vy := proxy.velocity.y - GRAVITY * delta
	proxy.velocity = Vector3(disp.x / maxf(delta, 1e-6), vy, disp.z / maxf(delta, 1e-6))
	proxy.move_and_slide()
	if proxy.is_on_floor():
		proxy.velocity.y = 0.0
	return world_to_m(proxy.global_position)


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
	scene.cam.size = base * (float(scene.PPM) / KC2_GD_PPM if zoomed_out else 1.0)
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
				# a record with no JOIN-1 pack: KC2 draws it as a labelled TOKEN, and so does this view
				no_pack[String(entry.get("family", rec))] = true
				t = Token3D.new()
			t.setup_monster(session, a, entry)
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
	if topdown:
		var c := T + Vector2(0.0, -2.0)
		scene.set_topdown(Vector2(c.x, -c.y), 62.0)
	else:
		scene.look_at_world(scene.aim_for(proxy.global_position))
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
		print("[arena] quit timer: wave %d, running %s, terminal '%s', actors %d, kits %s, no-pack %s, blocked stops %d" % [
			int(snap.get("wave", 0)) if not snap.is_empty() else 0, str(running),
			String(session.terminal) if session != null else "-", actors.size(), str(kits_seen.keys()),
			str(no_pack.keys()), n_blocked_stops])
		quit_arena()
