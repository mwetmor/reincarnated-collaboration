extends SceneTree
## BV2F PT (R-C9-268 item 2): P10 HITCH TRACE -- PH's ph_life.gd `perf` walk, reproduced step for step (same preroll,
## same 4-point loop round <view>, vsync off, uncapped), logging EVERY frame: wall ms, time since ready_done, his uv,
## and the engine's own counters -- pipeline compilations by kind (Godot 4.4+ monitors), objects/primitives/draw calls
## in frame, video memory -- so a deterministic hitch can be named. Read-only on the level.
##   Godot --path . --resolution 1920x1080 --script res://tools/bv2f/pt_hitch_trace.gd -- <scene> <OUT> <view uv:U,V>
var scene
var out_dir := ""
var view := ""
var t_ready_us := 0
const MON := {
	"pc_canvas": Performance.PIPELINE_COMPILATIONS_CANVAS, "pc_mesh": Performance.PIPELINE_COMPILATIONS_MESH,
	"pc_surface": Performance.PIPELINE_COMPILATIONS_SURFACE, "pc_draw": Performance.PIPELINE_COMPILATIONS_DRAW,
	"pc_spec": Performance.PIPELINE_COMPILATIONS_SPECIALIZATION,
	"objects": Performance.RENDER_TOTAL_OBJECTS_IN_FRAME, "prims": Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME,
	"draws": Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME, "vmem_mb": Performance.RENDER_VIDEO_MEM_USED,
	"tex_mb": Performance.RENDER_TEXTURE_MEM_USED, "t_process_ms": Performance.TIME_PROCESS,
	"t_physics_ms": Performance.TIME_PHYSICS_PROCESS, "nodes": Performance.OBJECT_NODE_COUNT,
	"orphans": Performance.OBJECT_ORPHAN_NODE_COUNT, "static_mb": Performance.MEMORY_STATIC}


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	out_dir = a[1]
	view = a[2]
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load(a[0]).instantiate()
	root.add_child(scene)
	_run()


func _sample() -> Dictionary:
	var d := {}
	for k in MON:
		var v := float(Performance.get_monitor(MON[k]))
		d[k] = v / 1048576.0 if k.ends_with("_mb") else (v * 1000.0 if k.begins_with("t_") else v)
	return d


func _run() -> void:
	var waited := 0
	while not scene.ready_done and waited < 4000:
		await process_frame
		waited += 1
	scene.set_hud_visible(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	if scene.snowfall != null:
		scene.snowfall.visible = false
		scene.snowfall.emitting = false
	t_ready_us = Time.get_ticks_usec()
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	var k = scene.knight
	k.set_physics_process(false)
	var p := view.substr(3).split(",")
	var c: Vector2 = scene.world_to_uv(scene.uv_to_world(float(p[0]), float(p[1])))
	var loop := [c + Vector2(4.0, 1.0), c + Vector2(0.0, 5.0), c + Vector2(-4.0, 1.0), c + Vector2(0.0, -3.0)]
	scene.place_knight(loop[3].x, loop[3].y, "N")
	var wi := 0
	var dt := 1.0 / 60.0
	var rows := []
	var tp := Time.get_ticks_usec()
	var prev := _sample()
	for i in 180 + 900:
		if i >= 180 and scene.knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await process_frame
		var tq := Time.get_ticks_usec()
		var s := _sample()
		var uv: Vector2 = scene.knight_uv()
		var row := {"i": i, "ms": snappedf(float(tq - tp) / 1000.0, 0.001), "t_s": snappedf(float(tq - t_ready_us) / 1e6, 0.001),
					"uv": [snappedf(uv.x, 0.01), snappedf(uv.y, 0.01)], "wp": wi}
		for key in s:
			row[key] = snappedf(s[key], 0.01)
			if key.begins_with("pc_"):
				row["d_" + key] = s[key] - prev[key]
		rows.append(row)
		prev = s
		tp = tq
	var f := FileAccess.open(out_dir.path_join("hitch_trace.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"view": view, "frames": rows}))
	f.close()
	var big := []
	for r in rows:
		if float(r["ms"]) > 25.0:
			big.append(r)
	print("[hitch] ", JSON.stringify(big))
	quit(0)
