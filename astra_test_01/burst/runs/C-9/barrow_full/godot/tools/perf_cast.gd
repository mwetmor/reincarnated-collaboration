extends SceneTree
## C-9 -- HER CAST START, TIMED (the coordinator: "her CAST START spikes a frame to 33.8 ms on desktop
## (22.9 on the web) about 140 ms after the cast input, with NO effect in the scene at all ... find it
## and fix it; measure it the same way (control casts, before and after)"). drax.
##
##   Godot --path godot --resolution 1920x1080 --script tools/perf_cast.gd -- --c sorceress \
##         --out FILE.json [--casts 10] [--no-fx] [--as-web]
##
## The painted Barrow as the page plays it, in the ROOT viewport (the page's own render path), vsync
## off and the frame rate uncapped so a frame's time is its cost. She stands, then casts SLASH and CHOP
## alternately every CAST_GAP_S by the same try_strike the keys call, at the start of a physics step.
## --no-fx turns her placeholder spell_fx off (a CONTROL cast: the strike with no effect at all).
##
## EVERY FRAME, split by the engine's own signals: physics (the physics_frame signal to the
## process_frame signal: every node's physics step, her AnimationTree included -- it runs on the
## physics callback), process (process_frame to frame_pre_draw), draw (frame_pre_draw to
## frame_post_draw, the swap included), and the gap to the next frame. INSIDE the physics step: her
## own _physics_process (sorceress_knight.gd's timer around knight.gd's), and the AnimationTree's
## `mixer_applied` stamp. EVENTS: the tree's `caches_cleared`, the player's `animation_list_changed`,
## Forward+'s pipeline compilations (RenderingServer's counters), and the node/resource counts.

const CAST_GAP_S := 3.0
const PRE_S := 3.0

var out_file := ""
var casts := 10
var no_fx := false
var no_trail_upload := false   # --no-trail-upload: the snow never re-uploads its trail map (a diagnosis switch)
var scene
var k
var stamps: Array = []
var events: Array = []
var cast_log: Array = []
var stamping := false


func _st(kind: String) -> void:
	if stamping:
		stamps.append([Engine.get_process_frames(), kind, Time.get_ticks_usec()])


func _ev(kind: String) -> void:
	events.append([Time.get_ticks_usec(), Engine.get_process_frames(), Engine.get_physics_frames(), kind])


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		var a := String(args[i])
		if a == "--out" and i + 1 < args.size():
			out_file = String(args[i + 1])
		elif a == "--casts" and i + 1 < args.size():
			casts = int(args[i + 1])
		elif a == "--no-fx":
			no_fx = true
		elif a == "--no-trail-upload":
			no_trail_upload = true
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 4000:
		await process_frame
		waited += 1
	if not scene.ready_done or scene.knight == null:
		print("[perf_cast] HALT: the scene never finished building")
		quit(3)
		return
	k = scene.knight
	print("[perf_cast] who=%s renderer=%s web=%s adapter=%s" % [scene.who, RenderingServer.get_current_rendering_method(),
		PaintStack.is_web(), RenderingServer.get_video_adapter_name()])
	if no_fx and scene.spell_fx != null:
		scene.spell_fx.set_physics_process(false)
		scene.spell_fx.process_mode = Node.PROCESS_MODE_DISABLED
	if no_trail_upload and scene.snow != null:
		scene.snow.set_process(false)
	scene.place_knight(1.5, -1.5, "E")
	if k._tree != null:
		k._tree.caches_cleared.connect(_ev.bind("tree_caches_cleared"))
		k._tree.mixer_applied.connect(_st.bind("tree_applied"))
		k._tree.animation_list_changed.connect(_ev.bind("tree_animation_list_changed"))
	if k._anim != null:
		k._anim.animation_list_changed.connect(_ev.bind("player_animation_list_changed"))
		k._anim.caches_cleared.connect(_ev.bind("player_caches_cleared"))
	physics_frame.connect(_st.bind("phys"))
	process_frame.connect(_st.bind("proc"))
	RenderingServer.frame_pre_draw.connect(_st.bind("pre"))
	RenderingServer.frame_post_draw.connect(_st.bind("post"))
	var t0 := Time.get_ticks_usec()
	stamping = true
	stamps.append([Engine.get_process_frames(), "t0", t0])
	var next_cast := PRE_S
	var done := 0
	var end_s := PRE_S + CAST_GAP_S * float(casts)
	var last_pipes := _pipes()
	var last_nodes := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	var last_res := int(Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT))
	while true:
		await physics_frame
		var t := float(Time.get_ticks_usec() - t0) / 1e6
		if t >= end_s:
			break
		if done < casts and t >= next_cast:
			var which := "slash" if done % 2 == 0 else "chop"
			var ok: bool = k.try_strike(which)
			cast_log.append({"n": done + 1, "which": which, "ok": ok, "us": Time.get_ticks_usec(),
				"process_frame": Engine.get_process_frames(), "physics_frame": Engine.get_physics_frames()})
			_ev("cast_" + which)
			done += 1
			next_cast += CAST_GAP_S
		# her own physics time, measured by sorceress_knight.gd's timer (the previous step)
		if k.has_method("diag_take"):
			var d: Dictionary = k.diag_take()
			if not d.is_empty():
				stamps.append([Engine.get_process_frames(), "her_phys_us", int(d.get("phys_us", 0))])
		var p := _pipes()
		if p != last_pipes:
			_ev("pipelines %s" % JSON.stringify(_diff(p, last_pipes)))
			last_pipes = p
		var nn := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
		var rr := int(Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT))
		if nn != last_nodes or rr != last_res:
			_ev("nodes %d->%d resources %d->%d" % [last_nodes, nn, last_res, rr])
			last_nodes = nn
			last_res = rr
	stamping = false
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify({"who": scene.who, "renderer": RenderingServer.get_current_rendering_method(),
		"web_branches": PaintStack.is_web(), "adapter": RenderingServer.get_video_adapter_name(),
		"window": [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y], "no_fx": no_fx, "no_trail_upload": no_trail_upload,
		"casts": cast_log, "events": events, "stamps": stamps}))
	f.close()
	print("[perf_cast] %d casts, %d stamps, %d events -> %s" % [cast_log.size(), stamps.size(), events.size(), out_file])
	quit(0)


func _pipes() -> Dictionary:
	return {"canvas": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_CANVAS),
		"mesh": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_MESH),
		"surface": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_SURFACE),
		"draw": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_DRAW),
		"specialization": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_SPECIALIZATION)}


func _diff(a: Dictionary, b: Dictionary) -> Dictionary:
	var o := {}
	for key in a:
		if int(a[key]) != int(b.get(key, 0)):
			o[key] = int(a[key]) - int(b.get(key, 0))
	return o
