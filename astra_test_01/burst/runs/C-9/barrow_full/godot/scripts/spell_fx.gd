extends Node3D
## C-9 -- HER TWO SPELLS, AS A PLACEHOLDER, and labelled one on screen (the coordinator: "a minimal
## placeholder VFX is fine and should be labelled as such"). drax.
##
## knight.gd has no release event (so_d7/scene_pkg/README.md, "what knight.gd lacks", item 3), so
## this watches the strike from outside: the frame a strike starts (attacking() rising, and which
## one from _strike_anim), the clip's own release time from her slot (casts.<clip>.release_s:
## Fire Ball 0.9333 s, Meteor 1.6333 s since her v2 package), and the socket from sockets_sorceress.json (the bone's
## world origin + its +Y x along_bone_m x the live figure scale). The animation runs on the physics
## tick (knight.gd), so the clock here does too.
##   FIRE BALL (SLASH): an ember orb leaves her LEFT palm along her facing, 9 m/s for 0.9 s, with
##     a trail of sparks, and bursts where it stops.
##   METEOR (CHOP): an ember falls out of the sky onto a point 3.5 m ahead of her and bursts there.
## Unshaded, alpha-mixed, drawn AFTER the post pass (PaintStack.AFTER_POST_PRIORITY): a transparent
## drawn before it is painted out by the pass's screen copy (the falling-snow lesson).

const ORB_SPEED := 9.0
const ORB_LIFE := 0.9
const METEOR_AHEAD := 3.5
const METEOR_FALL_S := 0.45
# MIXED, NOT ADDED: an additive ember over the painting's near-white snow saturates to white -- the
# first frames showed pale blobs, no fire -- so the colours are laid on with alpha, saturated
const EMBER := Color(1.0, 0.42, 0.08, 0.6)
const CORE := Color(1.0, 0.78, 0.30, 0.95)

var k                                  # her knight.gd node
var casts_by_slot := {}                 # "attack" / "chop" -> {clip, release_s, socket}
var sockets := {}
var _t := -1.0
var _slot := ""
var _fired := false
var _fx: Array = []                     # live effects: {kind, node, vel, age, life, ...}
var _mat_core: StandardMaterial3D
var _mat_ember: StandardMaterial3D
var report := {"fired": []}
# THE FIRE BALL IS REAL (C-9 (c)): cliffside's fire_bolt_e1_B, baked -- fire_ball_fx.gd. The Meteor
# below stays the placeholder until Matt picks one of the two being built.
var fire_ball = null
var _fb_group := -1
# LANE A'S METEOR (?meteor=a; desktop: -- --meteor a): meteor_a_fx.gd, the painted kit baked. Lane B stays the default.
var meteor_a = null
var _ma_group := -1
var fx_off := false              # the budget's CONTROL cast: the strike with no effect at all


func setup(knight, cfg: Dictionary, sockets_json: Dictionary) -> void:
	k = knight
	sockets = sockets_json
	var casts: Dictionary = cfg.get("casts", {})
	for clip in casts:
		if String(clip).begins_with("_"):
			continue
		var c: Dictionary = casts[clip]
		casts_by_slot[String(c["slot"])] = {"clip": String(clip), "release_s": float(c["release_s"]),
			"socket": String(c["socket"])}
	_mat_core = _mat(CORE)
	_mat_ember = _mat(EMBER)
	report["casts"] = casts_by_slot
	var fb = load("res://scripts/fire_ball_fx.gd").new()
	fb.name = "FireBall"
	add_child(fb)
	var sc = get_parent()
	if fb.setup(sc, sc.cam):
		fire_ball = fb
		fb.warm_up()
	report["fire_ball"] = fb.report
	if wants_meteor_a():
		# LANE A FOR REFERENCE: its full atlas is NOT in her pack (Matt's mix ships only A's fall); on the
		# page it comes as its own pack, meteor_a.pck, fetched only for ?meteor=a
		meteor_a_pending = true
		_load_meteor_a(sc)


var meteor_a_pending := false


func _load_meteor_a(sc) -> void:
	if not FileAccess.file_exists("res://data/vfx/meteor_a/meteor_a.json") and OS.has_feature("web"):
		var base := str(JavaScriptBridge.eval("document.baseURI", true))
		var url := base.get_base_dir() + "/meteor_a.pck" if not base.ends_with("/") else base + "meteor_a.pck"
		var http := HTTPRequest.new()
		add_child(http)
		http.download_file = "user://meteor_a.pck"
		http.request(url)
		var res: Array = await http.request_completed
		http.queue_free()
		report["meteor_a_pack"] = {"url": url, "result": int(res[0]), "http": int(res[1]),
			"loaded": ProjectSettings.load_resource_pack("user://meteor_a.pck") if int(res[0]) == HTTPRequest.RESULT_SUCCESS and int(res[1]) == 200 else false}
	var ma = load("res://scripts/meteor_a_fx.gd").new()
	ma.name = "MeteorA"
	add_child(ma)
	if ma.setup(sc, sc.cam):
		meteor_a = ma
		ma.warm_up()
	report["meteor_a"] = ma.report
	meteor_a_pending = false


static func wants_meteor_a() -> bool:
	var q := PaintStack.web_query("meteor")
	var args := OS.get_cmdline_user_args()
	var i := args.find("--meteor")
	if q == "" and i >= 0 and i + 1 < args.size():
		q = String(args[i + 1])
	return q.to_lower() == "a"


func _mat(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	m.albedo_color = c
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	m.no_depth_test = false
	m.disable_receive_shadows = true
	m.render_priority = PaintStack.AFTER_POST_PRIORITY
	m.billboard_mode = BaseMaterial3D.BILLBOARD_DISABLED
	return m


func socket_point(name: String) -> Vector3:
	var s: Dictionary = sockets.get(name, {})
	var skel: Skeleton3D = k._skel
	if s.is_empty() or skel == null:
		return k.global_position + Vector3(0, 1.2, 0)
	var bi := skel.find_bone(String(s["bone"]))
	if bi < 0:
		return k.global_position + Vector3(0, 1.2, 0)
	var t: Transform3D = skel.global_transform * skel.get_bone_global_pose(bi)
	return t.origin + t.basis.y.normalized() * float(s.get("along_bone_m", 0.0)) * float(k._figure_scale)


func facing_dir() -> Vector3:
	var fa: Array = k.cfg.get("forward_axis", [0.0, 0.0, 1.0])
	var f: Vector3 = k._rig.global_transform.basis * Vector3(float(fa[0]), float(fa[1]), float(fa[2]))
	f.y = 0.0
	return f.normalized() if f.length() > 1e-4 else Vector3.FORWARD


func _physics_process(dt: float) -> void:
	if k == null:
		return
	var att: bool = k.attacking()
	if att and _t < 0.0:
		_t = 0.0
		_slot = {"a_slash": "attack", "a_chop": "chop"}.get(String(k._strike_anim), "")
		_fired = false
		var c0: Dictionary = casts_by_slot.get(_slot, {})
		if _slot == "attack" and fire_ball != null and not c0.is_empty() and not fx_off:
			# the halo runs from here to the release, at the socket the ball leaves from
			_fb_group = fire_ball.cast_started(socket_point.bind(String(c0["socket"])),
				int(round(float(c0["release_s"]) * float(Engine.physics_ticks_per_second))))
		if _slot == "chop" and meteor_a != null and not c0.is_empty() and not fx_off:
			_ma_group = meteor_a.cast_started(socket_point.bind("main_tip"),     # the staff's crown
				int(round(float(c0["release_s"]) * float(Engine.physics_ticks_per_second))))
	elif not att:
		if _t >= 0.0 and not _fired and _fb_group >= 0 and fire_ball != null:
			fire_ball.abandon(_fb_group)
		if _t >= 0.0 and not _fired and _ma_group >= 0 and meteor_a != null:
			meteor_a.abandon(_ma_group)
		_fb_group = -1
		_ma_group = -1
		_t = -1.0
	if _t >= 0.0:
		_t += dt
		var c: Dictionary = casts_by_slot.get(_slot, {})
		if not c.is_empty() and not _fired and _t >= float(c["release_s"]) and fx_off:
			_fired = true
		if not c.is_empty() and not _fired and _t >= float(c["release_s"]):
			_fired = true
			var at := socket_point(String(c["socket"]))
			if _slot == "attack" and fire_ball != null:
				fire_ball.released(_fb_group, at, facing_dir(), k.global_position)
				_fb_group = -1
			elif _slot == "attack":
				_spawn_orb(at, facing_dir())
			elif _slot == "chop" and meteor_a != null:
				meteor_a.released(_ma_group, socket_point("main_tip"), facing_dir(), k.global_position)
				_ma_group = -1
			else:
				_spawn_meteor(k.global_position + facing_dir() * METEOR_AHEAD)
			report["fired"].append({"clip": c["clip"], "at_s": snappedf(_t, 0.001),
				"socket": c["socket"], "from": [snappedf(at.x, 0.01), snappedf(at.y, 0.01), snappedf(at.z, 0.01)]})
	_step(dt)


func _sphere(r: float, m: Material) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = r
	sm.height = r * 2.0
	sm.radial_segments = 12
	sm.rings = 6
	mi.mesh = sm
	mi.material_override = m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return mi


func _sparks(amount: int, one_shot: bool, speed: Vector2, life: float, size: float) -> CPUParticles3D:
	var p := CPUParticles3D.new()
	p.amount = amount
	p.one_shot = one_shot
	p.explosiveness = 1.0 if one_shot else 0.0
	p.lifetime = life
	p.local_coords = false
	p.direction = Vector3.UP
	p.spread = 180.0
	p.initial_velocity_min = speed.x
	p.initial_velocity_max = speed.y
	p.gravity = Vector3(0, -3.0, 0)
	p.scale_amount_min = 0.6
	p.scale_amount_max = 1.4
	var q := QuadMesh.new()
	q.size = Vector2(size, size)
	var m := _mat(EMBER).duplicate() as StandardMaterial3D
	m.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	m.billboard_keep_scale = true
	q.material = m
	p.mesh = q
	p.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return p


func _spawn_orb(at: Vector3, dir: Vector3) -> void:
	var n := Node3D.new()
	add_child(n)
	n.global_position = at
	n.add_child(_sphere(0.13, _mat_core))
	n.add_child(_sphere(0.22, _mat_ember))
	var trail := _sparks(48, false, Vector2(0.2, 0.8), 0.35, 0.07)
	n.add_child(trail)
	trail.emitting = true
	_fx.append({"kind": "orb", "node": n, "vel": dir * ORB_SPEED, "age": 0.0, "life": ORB_LIFE})


func _spawn_meteor(target: Vector3) -> void:
	var n := Node3D.new()
	add_child(n)
	var from := target + Vector3(-1.4, 7.5, -1.0)
	n.global_position = from
	n.add_child(_sphere(0.18, _mat_core))
	n.add_child(_sphere(0.32, _mat_ember))
	var trail := _sparks(60, false, Vector2(0.2, 1.0), 0.4, 0.09)
	n.add_child(trail)
	trail.emitting = true
	_fx.append({"kind": "meteor", "node": n, "vel": (target - from) / METEOR_FALL_S, "age": 0.0,
		"life": METEOR_FALL_S})


func _burst(at: Vector3, big: bool) -> void:
	var n := Node3D.new()
	add_child(n)
	n.global_position = at
	var flash := _sphere(0.25, _mat_core.duplicate())
	n.add_child(flash)
	var sp := _sparks(70 if big else 40, true, Vector2(2.5, 6.0) if big else Vector2(1.5, 3.5), 0.55, 0.1 if big else 0.07)
	n.add_child(sp)
	sp.emitting = true
	_fx.append({"kind": "burst", "node": n, "flash": flash, "age": 0.0, "life": 0.7,
		"grow": 1.6 if big else 1.0})


func _step(dt: float) -> void:
	var keep := []
	for e in _fx:
		e["age"] += dt
		var n: Node3D = e["node"]
		if e["kind"] == "orb" or e["kind"] == "meteor":
			n.global_position += e["vel"] * dt
			if e["age"] >= e["life"] or (e["kind"] == "meteor" and n.global_position.y <= 0.05):
				_burst(n.global_position, e["kind"] == "meteor")
				n.queue_free()
				continue
		elif e["kind"] == "burst":
			var a: float = clampf(e["age"] / 0.3, 0.0, 1.0)
			var fl: MeshInstance3D = e["flash"]
			fl.scale = Vector3.ONE * lerpf(0.4, 3.6 * float(e["grow"]), a)
			var m := fl.material_override as StandardMaterial3D
			m.albedo_color = Color(CORE.r, CORE.g, CORE.b, CORE.a * (1.0 - a))
			if e["age"] >= e["life"]:
				n.queue_free()
				continue
		keep.append(e)
	_fx = keep
