extends Node
## C-9 (c) -- THE FIRE BALL'S BUDGET, measured the coordinator's way: each effect judged by its DELTA
## against a matched CONTROL (the same cast with the effect off). drax.
##
## In the scene itself, so the page and the desktop measure alike: ?perf=fb on the page (the console gets
## one "[perf_fb] {...}" line), -- --perf fb on desktop (the same line, and user://perf_fb.json).
## She stands; every GAP_S she casts the FIRE BALL by the same try_strike the SLASH key calls. Casts
## alternate ON (the baked Fire Ball) and OFF (spell_fx.fx_off: the strike, no effect), the first ON
## -- the COLD first cast, straight after load. Every frame: its interval (the time between two process
## steps: on the page, one requestAnimationFrame to the next), the draw calls in it, the Fire Ball
## node's own physics time. Per cast: the window from the input to GAP_S later.

const GAP_S := 3.6
var gap_s := GAP_S
var strike := "slash"             # "chop" for lane A's Meteor (?perf=ma / mac): gap 6 s (the fall and the 3 s burn)
const WAIT_S := 3.0
var wait_s := WAIT_S                 # ?perfwait=N: the first cast N s after the level is ready

var scene
var casts := 20
var first_on := true              # "fbc": the first (cold) cast is the CONTROL, to see what the scene itself costs cold
var rows: Array = []                 # [t_us, dt_ms, draw_calls, fx_us, cast_n]
var cast_log: Array = []
var _t0 := 0
var _last := 0
var _next := 0.0
var _n := 0
var _done := false


var _ph := 0
var _pre := 0
var _split := [0.0, 0.0, 0.0]          # the last frame: physics, process, draw (ms)
var _last_proc := 0


func start(p_scene, n_casts: int, p_first_on := true, p_strike := "slash") -> void:
	strike = p_strike
	if strike == "chop":
		gap_s = 6.0
	scene = p_scene
	casts = n_casts
	first_on = p_first_on
	# the frame split, by the engine's own signals (as tools/perf_cast.gd): physics = the first
	# physics_frame to process_frame; process = process_frame to frame_pre_draw; draw = to frame_post_draw
	get_tree().physics_frame.connect(func(): if _ph == 0: _ph = Time.get_ticks_usec())
	get_tree().process_frame.connect(func():
		_last_proc = Time.get_ticks_usec()
		_split[0] = float(_last_proc - _ph) / 1000.0 if _ph != 0 else 0.0)
	RenderingServer.frame_pre_draw.connect(func():
		_pre = Time.get_ticks_usec()
		_split[1] = float(_pre - _last_proc) / 1000.0)
	RenderingServer.frame_post_draw.connect(func():
		_split[2] = float(Time.get_ticks_usec() - _pre) / 1000.0
		_ph = 0)


func _process(_dt: float) -> void:
	if scene == null or _done or not bool(scene.ready_done):
		return
	# a player cannot cast under the warming veil (it takes the input): on the page the clock starts at its lift
	if _t0 == 0 and scene.get("veil") != null and bool(scene.veil.visible):
		return
	var now := Time.get_ticks_usec()
	if _t0 == 0:
		_t0 = now
		_last = now
		var pw := PaintStack.web_query("perfwait")
		wait_s = float(pw) if pw != "" else WAIT_S
		_next = wait_s
		scene.place_knight(1.5, -1.5, "E")
		return
	var fb = (scene.spell_fx.fire_ball if strike == "slash" else scene.spell_fx.meteor_a) if scene.spell_fx != null else null
	var mfx = scene.get("meteor_fx")
	var fx_us := int(fb.last_us) if fb != null else 0
	if strike == "chop" and mfx != null:
		# the MIX (or lane B): B's own node (MIX v2's cinders step inside it), plus A's fall (the first mix)
		# or A's burst (MIX v2), each its own node
		fx_us = int(mfx.last_update_us) + (int(mfx.proj_a.last_us) if mfx.proj_a != null else 0) \
			+ (int(mfx.burst_a.last_us) if mfx.get("burst_a") != null else 0) \
			+ (int(mfx.crater.last_us) if mfx.get("crater") != null else 0) \
			+ (int(mfx.crater4.last_us) if mfx.get("crater4") != null else 0)
	var trail: int = int(scene.snow.trail_uploads) if scene.snow != null else 0
	rows.append([now - _t0, float(now - _last) / 1000.0,
		RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),
		fx_us, _n, snappedf(_split[0], 0.1), snappedf(_split[1], 0.1), snappedf(_split[2], 0.1), trail,
		String(scene.knight._clip) if "_clip" in scene.knight else "", scene.knight.attacking()])
	_last = now
	var t := float(now - _t0) / 1e6
	if _n < casts and t >= _next and not scene.knight.attacking():
		var on := (_n % 2 == 0) == first_on
		scene.spell_fx.fx_off = not on
		if scene.get("meteor_fx") != null:
			scene.meteor_fx.enabled = on      # the mix's (and lane B's) own control switch
		var ok: bool = scene.knight.try_strike(strike)
		cast_log.append({"n": _n + 1, "on": on, "ok": ok, "t_us": now - _t0})
		_n += 1
		_next = t + gap_s
	elif _n >= casts and t >= _next:
		_done = true
		_report()


func _window(c: Dictionary) -> Array:
	var out := []
	var a := int(c["t_us"])
	var b := a + int(gap_s * 1e6)
	for r in rows:
		if int(r[0]) > a and int(r[0]) <= b:
			out.append(r)
	return out


func _stats(frames: Array) -> Dictionary:
	if frames.is_empty():
		return {}
	var dts := []
	var dcs := []
	var fx := 0.0
	for r in frames:
		dts.append(float(r[1]))
		dcs.append(int(r[2]))
		fx += float(r[3])
	dts.sort()
	var s := 0.0
	for d in dts:
		s += d
	return {"frames": dts.size(), "mean_ms": snappedf(s / dts.size(), 0.001), "p95_ms": snappedf(dts[int(0.95 * (dts.size() - 1))], 0.01),
		"max_ms": snappedf(dts[-1], 0.01), "over_20ms": dts.filter(func(d): return d > 20.0).size(),
		"over_33ms": dts.filter(func(d): return d > 33.4).size(), "dc_max": dcs.max(), "fx_script_mean_ms": snappedf(fx / dts.size() / 1000.0, 0.0001)}


func _report() -> void:
	var per := []
	var on_frames := []
	var off_frames := []
	for c in cast_log:
		var w := _window(c)
		var st := _stats(w)
		st["n"] = c["n"]
		st["on"] = c["on"]
		var top := w.duplicate()
		top.sort_custom(func(a, b): return float(a[1]) > float(b[1]))
		st["top_frames_ms_after_input"] = top.slice(0, 4).map(func(r): return [int((int(r[0]) - int(c["t_us"])) / 1000), snappedf(float(r[1]), 0.1),
			"phys/proc/draw of the frame before", r[5], r[6], r[7], "trail tiles sent", r[8], "clip", r[9], "attacking", r[10]])
		per.append(st)
		if int(c["n"]) > 1:
			(on_frames if bool(c["on"]) else off_frames).append_array(w)
	var on := _stats(on_frames)
	var off := _stats(off_frames)
	var idle := _stats(rows.filter(func(r): return int(r[0]) < int(cast_log[0]["t_us"]) - 200000 and int(r[0]) > 1000000) if not cast_log.is_empty() else [])
	var out := {"who": scene.who, "renderer": RenderingServer.get_current_rendering_method(), "web": PaintStack.is_web(),
		"adapter": RenderingServer.get_video_adapter_name(), "window_px": [get_viewport().get_visible_rect().size.x, get_viewport().get_visible_rect().size.y],
		"gap_s": gap_s, "strike": strike, "idle": idle, "cold_first_cast": per[0] if not per.is_empty() else {},
		"warm_on": on, "warm_off_control": off,
		"delta_mean_ms": snappedf(float(on.get("mean_ms", 0.0)) - float(off.get("mean_ms", 0.0)), 0.001),
		"delta_dc_peak": int(on.get("dc_max", 0)) - int(off.get("dc_max", 0)), "per_cast": per,
		"fire_ball": scene.spell_fx.fire_ball.report if scene.spell_fx != null and scene.spell_fx.fire_ball != null else {}}
	var allr := rows.duplicate()
	allr.sort_custom(func(a, b): return float(a[1]) > float(b[1]))
	out["worst_frames_s_since_ready"] = allr.slice(0, 6).map(func(r): return [snappedf(float(r[0]) / 1e6, 0.01), snappedf(float(r[1]), 0.1), "phys/proc/draw", r[5], r[6], r[7], "dc", r[2]])
	if scene.veil != null:
		var v: Dictionary = scene.veil.report
		out["veil"] = v
		var lift_us := 0      # the clock (rows, casts) starts at the veil's lift: every row is after it
		var after := rows.filter(func(r): return int(r[0]) > lift_us)
		after.sort_custom(func(a, b): return float(a[1]) > float(b[1]))
		out["worst_frames_after_veil"] = after.slice(0, 4).map(func(r): return [snappedf(float(r[0]) / 1e6, 0.01), snappedf(float(r[1]), 0.1), "draw", r[7]])
	out["clock_zero"] = "the veil's lift" if scene.veil != null else "the level ready"
	out["first_cast_s_since_ready"] = snappedf(float(cast_log[0]["t_us"]) / 1e6, 0.01) if not cast_log.is_empty() else -1
	print("[perf_fb] " + JSON.stringify(out))
	if not PaintStack.is_web():
		var f := FileAccess.open("user://perf_fb.json", FileAccess.WRITE)
		f.store_string(JSON.stringify(out, " "))
		f.close()
		get_tree().quit()
