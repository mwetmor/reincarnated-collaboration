extends "res://scripts/barrow_full.gd"
## C-9 VFX BAKE-OFF, LANE B -- THE METEOR, 3D FIRST, IN THE PAINTED BARROW. drax.
##
## The painted Barrow exactly as barrow_full builds it (this extends a byte copy of barrow_full.gd;
## the only edited copies are painted_world.gd and paint_stack.gd, each with one marked LANE B
## addition), with:
##   HER (the sorceress, always) -- her Fire Ball stays spell_fx.gd's placeholder; the placeholder
##     Meteor is switched off and MeteorFx (meteor_fx.gd) is hers instead;
##   HIM standing by near the impact (bystander_knight.gd: knight.gd, no input), so the fire lights
##     "nearby dynamic things (her, him)";
##   the impact's camera shake (MeteorFx.shake_px), added to the play camera after it follows her.
##
## MODES (desktop: -- --meteor-<mode>; the web page: ?meteor=<mode>):
##   film    the shot for Matt: her cast from the call to the burn's end; `--slow` at quarter speed.
##           Run under Movie Maker (tools/film.sh); prints the trim frame.
##   perf    the budget (R-C9-89): idle, the COLD first cast, 20 casts with the effect and the same
##           20 casts with it off (the control), frame by frame: wall-clock frame time, the renderer's
##           own CPU and GPU times, draw calls, the effect's own script time. One JSON line.
##   stills  a few frames of one cast, saved as PNG for looking at (work/stills).

const HER_UV := Vector2(-2.2, 0.6)
const HIM_FROM_TARGET_UV := Vector2(1.9, 0.75)
var meteor: MeteorFx
var him: CharacterBody3D
var _him_saved := {}
var lane_b := {}
var _rec: Dictionary = {}
var _rec_on := false
var _last_us := 0


func _character_choice() -> String:
	return "sorceress"


func _ready() -> void:
	await super()
	await _lane_b_setup()
	var args := OS.get_cmdline_user_args()
	var mode := PaintStack.web_query("meteor")
	for m in ["film", "perf", "stills"]:
		if ("--meteor-" + m) in args:
			mode = m
	print("[meteor_b] ready mode=%s renderer=%s web=%s warm_ms=%s setup=%s" % [mode if mode != "" else "play",
		RenderingServer.get_current_rendering_method(), str(PaintStack.is_web()), str(meteor.report.get("warm_ms")),
		JSON.stringify(meteor.report.get("setup", {}))])
	match mode:
		"film":
			_film_mode()
		"perf":
			_perf_mode()
		"stills":
			_stills_mode()


func _lane_b_setup() -> void:
	# HER PLACEHOLDER METEOR OFF (spell_fx keeps the Fire Ball); lane B's is MeteorFx
	if spell_fx != null:
		spell_fx.casts_by_slot.erase("chop")
	await _build_him()
	# NO SCENE LIGHT REACHES THE EFFECT'S LAYER (it is unshaded: on Compatibility a lit layer would
	# also cost the shadowed suns' additive passes)
	sun.light_cull_mask &= ~MeteorFx.FX_LAYER
	if paint_sun != null:
		paint_sun.light_cull_mask &= ~MeteorFx.FX_LAYER
	meteor = MeteorFx.new()
	meteor.name = "MeteorFx"
	add_child(meteor)
	meteor.setup(knight, _read_json("res://data/sockets_sorceress.json"), sun, fbm, Callable(self, "_ground_y_at"))
	place_shot()
	await meteor.warm_up(knight.global_position)
	lane_b["meteor_setup"] = meteor.report.get("setup", {})
	lane_b["warm_ms"] = meteor.report.get("warm_ms")


func _ground_y_at(p: Vector3) -> float:
	if snow != null:
		return snow.surface_y(Vector2(p.x, p.z))
	var uv := world_to_uv(p)
	return floor_y_at(uv.x, uv.y)


func _build_him() -> void:
	var k: CharacterBody3D = load("res://scripts/bystander_knight.gd").new()
	k.name = "Him"
	k.setup(right, up, fwd, 1.0)
	add_child(k)
	await get_tree().physics_frame
	k.set_figure_scale(1.0)
	k.set_gear_stack(int(layout["knight"].get("gear_stack", 4)))
	him = k
	_him_saved = PaintStack.adopt_character(k, fbm, PaintStack.INK, {
		"wash_scale": 2.6, "wash_amp": 0.13, "band_soft": 0.075})
	if PaintStack.is_compatibility():
		# THE WEB PATH, as barrow_full gives her (built after it ran): one pen (his hull hidden), the
		# ambient inside the sun's pass (hers, copied: the environment's is already zeroed), the
		# colour-space corrections
		for e in _him_saved.get("inks", []):
			var hm = e.get("mi")
			if hm is Node3D and is_instance_valid(hm):
				(hm as Node3D).visible = false
		var amb = null
		for e in _char_saved.get("meshes", []):
			var m := (e["mi"] as MeshInstance3D).material_override as ShaderMaterial
			if m != null:
				amb = m.get_shader_parameter("ambient_in_light")
				break
		for e in _him_saved.get("meshes", []):
			var m := (e["mi"] as MeshInstance3D).material_override as ShaderMaterial
			if m != null and amb != null:
				m.set_shader_parameter("ambient_in_light", amb)
		lane_b["him_web_colour"] = PaintStack.web_color_space(k)


func _rig_fwd(k) -> Vector3:
	var fa: Array = k.cfg.get("forward_axis", [0.0, 0.0, 1.0])
	var f: Vector3 = k._rig.global_transform.basis * Vector3(float(fa[0]), 0.0, float(fa[2]))
	f.y = 0.0
	return f.normalized() if f.length() > 1e-4 else Vector3.FORWARD


func _face_toward(k, want: Vector3) -> String:
	"""The facing (of the eight) whose rig forward -- the direction her Meteor is aimed along --
	lies closest to `want` on the ground: measured, not assumed from the compass letters."""
	var best := "E"
	var bd := -2.0
	for f in ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]:
		k.facing = f
		k._drive()
		var d := _rig_fwd(k).dot(want.normalized())
		if d > bd:
			bd = d
			best = f
	k.facing = best
	k._drive()
	return best


func nudge_right() -> void:
	"""ONE STEP TO THE RIGHT, by the input she reads, then back to her mark. knight.gd turns her by her
	last MOVE direction whenever it sees any speed (its _drive), not by `facing`: placed facing east with
	no step taken, her stale move direction (screen down) won at the strike, and the first stills aimed
	the Meteor down the screen. A real step sets it."""
	Input.action_press("move_right")
	for i in 5:
		await get_tree().physics_frame
	Input.action_release("move_right")
	for i in 20:
		await get_tree().physics_frame
	place_shot()


func place_shot() -> void:
	"""THE SHOT: her in the arena, her Meteor aimed screen-right (the target 3.5 m ahead of her on open
	sunlit snow, the whole fall on screen), him 2 m beyond the target, turned toward it."""
	place_knight(HER_UV.x, HER_UV.y, "E")
	lane_b["her_facing"] = _face_toward(knight, u_hat)
	var target: Vector3 = knight.global_position + _rig_fwd(knight) * MeteorFx.AHEAD
	var tuv := world_to_uv(target)
	lane_b["target_uv"] = [snappedf(tuv.x, 0.01), snappedf(tuv.y, 0.01)]
	if him != null:
		var huv := tuv + HIM_FROM_TARGET_UV
		him.global_position = uv_to_world(huv.x, huv.y, floor_y_at(huv.x, huv.y) + 0.03)
		him.velocity = Vector3.ZERO
		lane_b["him_facing"] = _face_toward(him, target - him.global_position)
		lane_b["him_uv"] = [snappedf(huv.x, 0.01), snappedf(huv.y, 0.01)]
	look_at_world(_camera_aim())


func _process(dt: float) -> void:
	super(dt)
	# THE IMPACT'S SHAKE, on top of the camera that follows her
	if meteor != null and cam != null and meteor.shake_px != Vector2.ZERO:
		cam.global_position += (right * meteor.shake_px.x + up * meteor.shake_px.y) / PPM
	if _rec_on:
		_record_frame()


func _build_fx_label() -> void:
	"""What is on screen, said: the Meteor is lane B's; the Fire Ball is still the placeholder."""
	var layer := CanvasLayer.new()
	layer.name = "FxLabel"
	layer.layer = 21
	add_child(layer)
	var l := Label.new()
	l.text = "METEOR: LANE B (3D FIRST)  ·  FIRE BALL: PLACEHOLDER"
	l.add_theme_font_size_override("font_size", 20)
	l.add_theme_color_override("font_color", Color(1.0, 0.86, 0.6, 0.9))
	l.add_theme_color_override("font_outline_color", Color(0.1, 0.07, 0.05, 0.9))
	l.add_theme_constant_override("outline_size", 6)
	l.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	l.offset_left = -720.0
	l.offset_right = -24.0
	l.offset_top = 20.0
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	layer.add_child(l)


func _lit_at_world(p: Vector3) -> float:
	var lit: Texture2D = _paint_tex.get("lit")
	if lit == null:
		return -1.0
	var img := lit.get_image()
	var uv := world_to_uv(p)
	var k := float(img.get_width()) / PaintedWorld.GUIDE_PX.x
	var x := (uv.x - PaintedWorld.U0) * PaintedWorld.PPM * k
	var y := ((PaintedWorld.V1 - uv.y) * PaintedWorld.PPM * sin(deg_to_rad(PaintedWorld.PITCH_DEG)) - p.y * PaintedWorld.PPM * cos(deg_to_rad(PaintedWorld.PITCH_DEG))) * k
	if x < 0 or y < 0 or x >= img.get_width() or y >= img.get_height():
		return -1.0
	return img.get_pixel(int(x), int(y)).r


# --- film -----------------------------------------------------------------------------------------
func _film_mode() -> void:
	"""Under Movie Maker at a fixed step: settle, then her Meteor from the start of the cast to the
	burn's end and a beat after. `--slow`: the whole action at quarter speed."""
	var slow := "--slow" in OS.get_cmdline_user_args() or PaintStack.web_query("slow") != ""
	set_hud_visible(false)
	await nudge_right()
	for i in 45:
		await get_tree().process_frame
	var target: Vector3 = knight.global_position + meteor.facing_dir() * MeteorFx.AHEAD
	print("[film] %s" % JSON.stringify({"trim_frames": Engine.get_process_frames(), "slow": slow,
		"lit_at_target": _lit_at_world(target)}))
	for i in 8:
		await get_tree().process_frame
	Engine.time_scale = 0.25 if slow else 1.0
	# SMOOTH SLOW MOTION: her animation runs on the physics tick, so at quarter speed the tick runs 4x
	# as often -- one physics step per rendered frame, as at play speed -- or she would move every 4th
	Engine.physics_ticks_per_second = 240 if slow else 60
	knight.try_strike("chop")
	var t := 0.0
	var hold := 0.0
	while true:
		await get_tree().process_frame
		t += get_process_delta_time()
		if t > 1.0 and meteor.active_count() == 0 and not knight.attacking():
			hold += get_process_delta_time()
			if hold > 0.45:
				break
		if t > 12.0:
			break
	print("[film] %s" % JSON.stringify({"done": true, "casts": meteor.report["casts"], "impacts": meteor.report["impacts"]}))
	get_tree().quit()


# --- stills ---------------------------------------------------------------------------------------
func _stills_mode() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--out")
	var out := String(args[i + 1]) if i >= 0 and i + 1 < args.size() else "user://stills"
	DirAccess.make_dir_recursive_absolute(out)
	await nudge_right()
	for f in 40:
		await get_tree().process_frame
	var ts: Array = [0.03, 0.2, 0.35, 0.5, 0.62, 0.72, 0.8, 0.84, 0.88, 0.95, 1.1, 1.5, 2.2, 3.0, 3.6]
	var ai := args.find("--at")
	if ai >= 0 and ai + 1 < args.size():
		ts = Array(String(args[ai + 1]).split(",")).map(func(x): return float(x))
	knight.try_strike("chop")
	var wait := true
	while wait:
		await get_tree().process_frame
		wait = meteor.report["casts"].is_empty()
	var t := 0.0
	var k := 0
	var shots := []
	while k < ts.size():
		await get_tree().process_frame
		t += get_process_delta_time()
		if t >= float(ts[k]):
			await RenderingServer.frame_post_draw
			var img := get_viewport().get_texture().get_image()
			var p := "%s/still_%02d_t%.2f.png" % [out, k, float(ts[k])]
			img.save_png(p)
			shots.append(p)
			k += 1
	var target: Vector3 = knight.global_position + meteor.facing_dir() * MeteorFx.AHEAD
	var tpx := cam.unproject_position(target)
	var hpx := cam.unproject_position(knight.global_position)
	print("[stills] %s" % JSON.stringify({"shots": shots, "lit_at_target": _lit_at_world(target),
		"casts": meteor.report["casts"], "target_px": [tpx.x, tpx.y], "her_px": [hpx.x, hpx.y],
		"viewport": [get_viewport().get_visible_rect().size.x, get_viewport().get_visible_rect().size.y], "lane_b": lane_b}))
	get_tree().quit()


# --- perf -----------------------------------------------------------------------------------------
func _record_frame() -> void:
	var now := Time.get_ticks_usec()
	var rid := get_viewport().get_viewport_rid()
	if _last_us > 0:
		(_rec["ms"] as Array).append(float(now - _last_us) / 1000.0)
		(_rec["t"] as Array).append(float(now - int(_rec["t0"])) / 1000.0)
		(_rec["gpu"] as Array).append(RenderingServer.viewport_get_measured_render_time_gpu(rid))
		(_rec["cpu"] as Array).append(RenderingServer.viewport_get_measured_render_time_cpu(rid))
		(_rec["dc"] as Array).append(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME))
		(_rec["fx_us"] as Array).append(meteor.last_update_us)
		(_rec["phase"] as Array).append(int(_rec["cur_phase"]))
	_last_us = now


func _rec_start() -> void:
	# PLAIN ARRAYS: a Packed*Array read out of a Dictionary is a copy -- appending to it records nothing
	# (the first perf run: 0 frames)
	_rec = {"ms": [], "t": [], "gpu": [], "cpu": [], "dc": [], "fx_us": [], "phase": [],
		"t0": Time.get_ticks_usec(), "cur_phase": 0, "events": []}
	_last_us = 0
	_rec_on = true


func _event(kind: String, phase: int) -> void:
	(_rec["events"] as Array).append({"kind": kind, "phase": phase,
		"t": float(Time.get_ticks_usec() - int(_rec["t0"])) / 1000.0})


func _cast_run(n: int, phase: int, fx_on: bool) -> void:
	"""n Meteors back to back, as fast as her clip allows (its length is its cooldown): the burn of one
	overlaps the next cast, the heaviest steady state the effect has."""
	meteor.enabled = fx_on
	_rec["cur_phase"] = phase
	var casts0: int = meteor.report["casts"].size()
	var imp0: int = meteor.report["impacts"].size()
	for c in n:
		while knight.attacking():
			await get_tree().process_frame
		await get_tree().process_frame
		knight.try_strike("chop")
		_event("cast", phase)
		var rel_seen := false
		var imp_seen := false
		var t := 0.0
		while t < MeteorFx.T_IMPACT + 1.625 + 0.15:
			await get_tree().process_frame
			t += get_process_delta_time()
			if not rel_seen and t >= meteor.release_s:
				rel_seen = true
				_event("release", phase)
			if rel_seen and not imp_seen and t >= meteor.release_s + MeteorFx.T_IMPACT:
				# (the first harness keyed this by the loop index, which is 0 in every one-cast call: only
				# the first impact of each phase was logged)
				imp_seen = true
				_event("impact", phase)
	# the rest of the effect's life -- the same wait with the effect off, so both windows match
	var t2 := 0.0
	while t2 < MeteorFx.BURN_S + 0.15 or meteor.active_count() > 0:
		await get_tree().process_frame
		t2 += get_process_delta_time()
		if t2 > 6.0:
			break
	lane_b["phase_%d_casts" % phase] = meteor.report["casts"].size() - casts0
	lane_b["phase_%d_impacts" % phase] = meteor.report["impacts"].size() - imp0


func _perf_mode() -> void:
	var args := OS.get_cmdline_user_args()
	var oi := args.find("--out")
	var out := String(args[oi + 1]) if oi >= 0 and oi + 1 < args.size() else ""
	set_hud_visible(false)
	if not PaintStack.is_web():
		Engine.max_fps = 0
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	RenderingServer.viewport_set_measure_render_time(get_viewport().get_viewport_rid(), true)
	await nudge_right()
	for i in 60:
		await get_tree().process_frame
	_rec_start()
	# 0: idle, her standing
	_rec["cur_phase"] = 0
	for i in 240:
		await get_tree().process_frame
	# 1: THE COLD FIRST CAST -- the first Meteor this process has drawn (warmed at load, never cast)
	await _cast_run(1, 1, true)
	# 2 and 3, INTERLEAVED: 19 more casts with the effect (20 in all) and 20 with it off -- the control,
	# her animation and all -- alternating, so any drift in the machine (the first run's idle frames were
	# 1.4 ms slower than its later control frames) falls on both alike. Every cast window is the same
	# length, the effect's whole life (the call to the burn's end).
	for c in 39:
		var on := c % 2 == 1
		await _cast_run(1, 2 if on else 3, on)
	_rec_on = false
	var res := _perf_summary()
	res["lane_b"] = lane_b
	res["renderer"] = RenderingServer.get_current_rendering_method()
	res["web"] = PaintStack.is_web()
	res["viewport"] = [get_viewport().get_visible_rect().size.x, get_viewport().get_visible_rect().size.y]
	res["render_px"] = [_render_px().x, _render_px().y]
	res["window"] = [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y]
	res["vsync"] = DisplayServer.window_get_vsync_mode()
	print("[meteor_perf] " + JSON.stringify(res))
	if out != "":
		var f := FileAccess.open(out, FileAccess.WRITE)
		if f != null:
			var full := res.duplicate(true)
			full["frames"] = {"ms": _rec["ms"], "t": _rec["t"], "gpu": _rec["gpu"],
				"cpu": _rec["cpu"], "dc": _rec["dc"], "fx_us": _rec["fx_us"], "phase": _rec["phase"]}
			full["events"] = _rec["events"]
			f.store_string(JSON.stringify(full))
			f.close()
	get_tree().quit()


static func _stats(a: Array) -> Dictionary:
	if a.is_empty():
		return {}
	var s := a.duplicate()
	s.sort()
	var tot := 0.0
	for x in s:
		tot += float(x)
	return {"n": s.size(), "mean": snappedf(tot / s.size(), 0.001), "p50": snappedf(float(s[s.size() / 2]), 0.001),
		"p95": snappedf(float(s[mini(s.size() - 1, int(s.size() * 0.95))]), 0.001),
		"p99": snappedf(float(s[mini(s.size() - 1, int(s.size() * 0.99))]), 0.001),
		"max": snappedf(float(s[s.size() - 1]), 0.001)}


func _perf_summary() -> Dictionary:
	var ms: Array = _rec["ms"]
	var t: Array = _rec["t"]
	var ph: Array = _rec["phase"]
	var out := {"phases": {}, "windows": {}, "note": "ms = wall-clock frame time (vsync off on the desktop); gpu/cpu = the renderer's own measured times; dc = draw calls in the frame; fx_us = MeteorFx._process"}
	var names := {0: "idle", 1: "cold_first_cast", 2: "casts_2_to_20_fx_on", 3: "casts_1_to_20_fx_off_control"}
	for p in names:
		var a_ms := []
		var a_gpu := []
		var a_cpu := []
		var a_dc := []
		var a_fx := []
		for i in ms.size():
			if ph[i] == p:
				a_ms.append(ms[i])
				a_gpu.append((_rec["gpu"] as Array)[i])
				a_cpu.append((_rec["cpu"] as Array)[i])
				a_dc.append((_rec["dc"] as Array)[i])
				a_fx.append(float((_rec["fx_us"] as Array)[i]) / 1000.0)
		out["phases"][names[p]] = {"frame_ms": _stats(a_ms), "gpu_ms": _stats(a_gpu), "render_cpu_ms": _stats(a_cpu),
			"draw_calls": _stats(a_dc), "fx_script_ms": _stats(a_fx), "over_20ms": a_ms.filter(func(x): return float(x) > 20.0).size()}
	# THE WINDOWS: the frames within 150 ms after each event (and the one before it)
	for e in _rec["events"]:
		var key := "%s_%s" % [names[int(e["phase"])], String(e["kind"])]
		if not out["windows"].has(key):
			out["windows"][key] = {"n_events": 0, "max_frame_ms": 0.0, "max_dc": 0, "worst_event_t": 0.0}
		var w: Dictionary = out["windows"][key]
		w["n_events"] = int(w["n_events"]) + 1
		for i in ms.size():
			if t[i] >= float(e["t"]) - 20.0 and t[i] <= float(e["t"]) + 150.0:
				if ms[i] > float(w["max_frame_ms"]):
					w["max_frame_ms"] = snappedf(ms[i], 0.01)
					w["worst_event_t"] = snappedf(float(e["t"]), 0.1)
				w["max_dc"] = maxi(int(w["max_dc"]), (_rec["dc"] as Array)[i])
	var on_all := []
	var off_all := []
	for i in ms.size():
		if ph[i] == 1 or ph[i] == 2:
			on_all.append(ms[i])
		elif ph[i] == 3:
			off_all.append(ms[i])
	var son := _stats(on_all)
	var soff := _stats(off_all)
	out["fx_cost_ms_per_frame"] = snappedf(float(son.get("mean", 0.0)) - float(soff.get("mean", 0.0)), 0.001)
	var g_on := []
	var g_off := []
	for i in ms.size():
		if ph[i] == 1 or ph[i] == 2:
			g_on.append((_rec["gpu"] as Array)[i])
		elif ph[i] == 3:
			g_off.append((_rec["gpu"] as Array)[i])
	out["fx_gpu_ms_per_frame"] = snappedf(float(_stats(g_on).get("mean", 0.0)) - float(_stats(g_off).get("mean", 0.0)), 0.001)
	out["dc_peak_on_minus_off"] = int(_stats(on_all.map(func(_x): return 0)).get("max", 0))
	var dmax_on := 0
	var dmax_off := 0
	for i in ms.size():
		var d: int = (_rec["dc"] as Array)[i]
		if ph[i] == 1 or ph[i] == 2:
			dmax_on = maxi(dmax_on, d)
		elif ph[i] == 3:
			dmax_off = maxi(dmax_off, d)
	out["dc_peak_on_minus_off"] = dmax_on - dmax_off
	out["dc_peak"] = {"fx_on": dmax_on, "fx_off": dmax_off}
	return out
