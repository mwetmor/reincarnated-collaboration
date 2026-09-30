extends "res://scripts/fire_ball_fx.gd"
## C-9 (d) -- LANE A'S METEOR (?meteor=a): the painted kit, BAKED from its own runtime and played by the Fire
## Ball's flipbook player (one atlas, one shader, one MultiMesh draw, warmed under the veil). drax.
##
## THE KIT: meteor_e1, exported by the frozen cliffside exporter -- the VF-met head and trail on the fl6 travel
## layers (flame dance, core, halo, smear, motes), its impact the burst template cut from VF-met-impact-01 (50
## pieces), and its ring (VF-met-ring-01) and burn (C-5 VF-prim-fire-pool-01) in the kit's own material
## (godot/tools/meteor_extras.gd). Baked by godot/tools/bake_meteor.gd, packed by tools/meteor_bake_pack.py,
## proven by godot/tools/proof_meteor.gd (take/build/meteor_a_proof.json).
##
## THE CAST, from her release (1.6333 s): the flare at her staff crown (the kit's muzzle puff, turned up)
## and the kit's cast floor at her feet; the RING at the landing point, 3.5 m ahead on the ground; the FALL,
## 0.7 s (the kit's 42 ticks), steeply from above -- the baked east-flying travel turned to the fall's screen
## angle (70 degrees below the horizontal), its 480 px path ending at the burst's anchor; the IMPACT upright
## there, its floor light on the snow, and a small camera shake; the BURN, 3 s, on the ground. The ring and
## the burn are ground quads whose projection is the baked frame, as the floor lights are.

const MDATA := "res://data/vfx/meteor_a/"
const AHEAD_M := 3.5
const FALL_DEG := 70.0
# the slot layout, back to front: the ground first, so the burst draws over its own ring and burn
const M_RING := 0
const M_BURN := 1
const M_CAST_FLOOR := 2
const M_IMPACT_FLOOR := 3
const M_MOTES := 4               # 8 of them
const M_PUFF := 12
const M_TRAVEL := 13
const M_IMPACT := 14
const M_HALO := 15
const M_SLOTS := 16
const SHAKE_S := 0.3
const SHAKE_M := 0.05

var _shake_t := -1.0


func setup(p_scene, p_cam: Camera3D) -> bool:
	data_dir = MDATA
	meta_file = "meteor_a.json"
	slots = M_SLOTS
	return super(p_scene, p_cam)


func released(g: int, socket: Vector3, dir: Vector3, feet: Vector3) -> void:
	if g < 0 or casts[g].is_empty():
		return
	var c: Dictionary = casts[g]
	var d := Vector3(dir.x, 0.0, dir.z).normalized()
	var ground := _ground_at(feet + d * AHEAD_M)
	var gdy := float(meta["timing"]["ground_dy_below_burst"])
	var anchor := ground + Vector3.UP * (gdy / PXH)
	var L := float(meta["timing"]["impact_dx"])
	var a := deg_to_rad(FALL_DEG)
	var start: Vector3 = anchor - scene.u_hat * (L * cos(a) / PPM) + Vector3.UP * (L * sin(a) / PXH)
	c["state"] = "flight"
	c["tick"] = 0
	c["clock"] = 0.0
	c["socket"] = socket
	c["feet"] = feet
	c["ground"] = ground
	c["anchor"] = anchor
	c["start"] = start
	c["theta"] = _screen_angle((anchor - start).normalized()) if (anchor - start).length() > 1e-4 else a
	report["fired"].append({"socket": [snappedf(socket.x, 0.01), snappedf(socket.y, 0.01), snappedf(socket.z, 0.01)],
		"target": [snappedf(ground.x, 0.01), snappedf(ground.y, 0.01), snappedf(ground.z, 0.01)],
		"screen_deg": snappedf(rad_to_deg(float(c["theta"])), 0.1), "impact_set": c["set"]})


func _ground_at(p: Vector3) -> Vector3:
	return Vector3(p.x, _surface_y(p), p.z)


func _screen_angle(d: Vector3) -> float:
	# the screen angle of a WORLD direction, through the camera's own axes (a vertical component counts)
	var b := cam.global_transform.basis
	var sx := d.dot(b.x.normalized())
	var sy := -d.dot(b.y.normalized())
	return atan2(sy, sx)


func _tick_windup(g: int, c: Dictionary) -> void:
	var t := clampf((float(c["clock"]) * 60.0 - 1.0) / float(int(c["release_ticks"]) - 1), 0.0, 1.0)
	var n: int = (fidx["halo"] as Array).size()
	var i := clampi(int(round(t * float(n - 1))), 0, n - 1)
	var at: Vector3 = (c["socket_fn"] as Callable).call()
	_put(g * slots + M_HALO, "halo", i, at + _toward(HALO_TOWARD_M), 0.0, 1.0)


func _tick_flight(g: int, c: Dictionary) -> void:
	var b: int = int(floor(float(c["clock"]) * 60.0 + 1e-4)) - 1
	var base := g * slots
	_collapse(base + M_HALO)
	var th: float = c["theta"]
	var start: Vector3 = c["start"]
	var anchor: Vector3 = c["anchor"]
	var L := float(meta["timing"]["impact_dx"])
	var alive := false
	# the fall: the kit's own distance at this tick, along the path
	var tr := _travel_at(b)
	if not tr.is_empty():
		var p: Vector3 = start.lerp(anchor, clampf(float(tr["dx"]) / L, 0.0, 1.0))
		_put(base + M_TRAVEL, "travel", _frame_of("travel", b), p + _toward(TRAVEL_BEHIND_M), th, 1.0)
		alive = true
	else:
		_collapse(base + M_TRAVEL)
	# the flare at the staff crown, turned up
	var pf := _frame_of("puff", b)
	if pf >= 0:
		_put(base + M_PUFF, "puff", pf, (c["socket"] as Vector3) + _toward(HALO_TOWARD_M), -PI * 0.5, 1.0)
		alive = true
	else:
		_collapse(base + M_PUFF)
	var als: Array = meta["floor_alpha"].get("cast_floor", [])
	if b >= 0 and b < als.size() and float(als[b]) > 0.0:
		_put_floor(base + M_CAST_FLOOR, "cast_floor", 0, feet_on_surface(c["feet"]), float(als[b]) / float(als[0]))
		alive = true
	else:
		_collapse(base + M_CAST_FLOOR)
	# the ring and the burn, on the ground at the landing point
	for spec in [["ring", M_RING], ["burn", M_BURN]]:
		var fi := _frame_of(String(spec[0]), b)
		if fi >= 0:
			_put_floor(base + int(spec[1]), String(spec[0]), fi, c["ground"], 1.0)
			alive = true
		else:
			_collapse(base + int(spec[1]))
	# the burst, upright at the anchor, its floor light on the snow; the shake on its first tick
	var imp_key := "impact_%d" % int(c["set"])
	var ii := _frame_of(imp_key, b)
	if ii >= 0:
		_put(base + M_IMPACT, imp_key, ii, anchor + _toward(BURST_TOWARD_M), 0.0, 1.0)
		alive = true
		if b == impact_tick:
			_shake_t = 0.0
		var fl := _frame_of("impact_floor", b)
		if fl >= 0:
			_put_floor(base + M_IMPACT_FLOOR, "impact_floor", fl, _ground_under(anchor), 1.0)
		else:
			_collapse(base + M_IMPACT_FLOOR)
	else:
		_collapse(base + M_IMPACT)
		_collapse(base + M_IMPACT_FLOOR)
	# the trail motes, by the kit's rule, from their births, turned with the fall
	var lat := float(meta["motes"]["lateral_px"])
	var rise := float(meta["motes"]["rise_px_s"])
	for mi in 8:
		var slot := base + M_MOTES + mi
		if mi >= births.size():
			_collapse(slot)
			continue
		var bb: Dictionary = births[mi]
		var age := float(b - int(bb["birth_tick"])) / 60.0
		var life := float(bb["life_s"])
		if age <= 0.0 or age >= life:
			_collapse(slot)
			continue
		var bt := _travel_at(int(bb["birth_tick"]))
		if bt.is_empty():
			_collapse(slot)
			continue
		var node0: Vector3 = start.lerp(anchor, clampf(float(bt["dx"]) / L, 0.0, 1.0))
		var off := Vector2(float(bb["origin_dx"]) - float(bt["dx"]), float(bb["origin_dy"]) - float(bt["dy"])).rotated(th)
		var ph := float(bb["phase"])
		off += Vector2(lat * (sin(ph + age * 8.0) - sin(ph)) * 0.5, -rise * age)
		var col: Array = bb["color"]
		_put_mote(slot, node0, off, float(bb["half_px"]), Color(float(col[0]), float(col[1]), float(col[2])), 1.0 - age / life)
		alive = true
	c["tick"] = b
	if not alive and b > impact_tick:
		casts[g] = {}
		_collapse_group(g)


func _step(dt: float) -> void:
	super(dt)
	# the small camera shake, from the impact: decaying, on the camera's own offsets (never its transform)
	if _shake_t >= 0.0 and cam != null:
		_shake_t += dt
		var k := maxf(0.0, 1.0 - _shake_t / SHAKE_S)
		cam.h_offset = SHAKE_M * k * sin(_shake_t * TAU * 23.0)
		cam.v_offset = SHAKE_M * k * sin(_shake_t * TAU * 17.0 + 1.3)
		if k <= 0.0:
			cam.h_offset = 0.0
			cam.v_offset = 0.0
			_shake_t = -1.0
