extends SceneTree
## C-9 -- WHERE THE CLIFFSIDE FIRE BOLT SPENDS ITS TIME (the coordinator's diagnosis, before any port). drax.
##
## Run in a SCRATCH COPY of C-7's cliffside_v45 (the live /playtest/cliffside/ source is identical for
## keeper.gd, the kit and its scripts), never in C-7 itself:
##   Godot --path <copy> --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --script <this> -- --out FILE.json [--kit fire_bolt_e1_B] [--casts 6]
##
## The scene as the page plays it; the keeper cycled to the kit by the page's own Tab action; casts by
## the page's own "cast" action, spaced CAST_GAP_S. Vsync off and the frame rate uncapped, so a frame's
## time is its cost.
##
## PASS T (timing): every frame -- its time, the process and physics times, draw calls, node, resource
##   and object counts, the phase (projectile live, impacts alive). Nothing else runs in these frames.
## PASS W (walk): one more cast, and every frame of it every visible CanvasItem is walked -- classes,
##   unique materials, shaders, textures, summed sprite area against the screen (overdraw), lights.
##   Its frame times are NOT used (the walk itself costs time).

const CAST_GAP_S := 3.2
const PRE_S := 2.0
const WALK_S := 2.6

var out_file := ""
var kit_name := "fire_bolt_e1_B"
var casts := 6
var scene
var keeper
var actors: Node
var rows: Array = []
var cast_at: Array = []
var walk_rows: Array = []
var stamps: Array = []
var stamping := false


func _stamp(kind: String) -> void:
	if stamping:
		stamps.append([Engine.get_process_frames(), kind, Time.get_ticks_usec()])


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_file = args[i + 1]
		elif args[i] == "--kit" and i + 1 < args.size():
			kit_name = args[i + 1]
		elif args[i] == "--casts" and i + 1 < args.size():
			casts = int(args[i + 1])
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_VIEWPORT
	root.content_scale_size = Vector2i(1920, 1080)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	keeper = scene.find_child("Keeper", true, false)
	actors = keeper.get_parent()
	keeper.vfx_force_touch_device = true
	var names: Array = []
	for k in keeper.VFX_KITS:
		names.append(String(k["name"]))
	var idx := names.find(kit_name)
	if idx < 0:
		print("[diag] HALT: no kit %s in %s" % [kit_name, str(names)])
		quit(2)
		return
	for i in idx:
		Input.action_press("vfx_cycle")
		await physics_frame
		Input.action_release("vfx_cycle")
		await physics_frame
		await physics_frame
	for i in 60:
		await process_frame
	RenderingServer.viewport_set_measure_render_time(root.get_viewport_rid(), true)
	physics_frame.connect(_stamp.bind("phys"))
	process_frame.connect(_stamp.bind("proc"))
	RenderingServer.frame_pre_draw.connect(_stamp.bind("pre"))
	RenderingServer.frame_post_draw.connect(_stamp.bind("post"))
	var base_nodes := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	var base_objects := int(Performance.get_monitor(Performance.OBJECT_COUNT))
	var base_resources := int(Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT))
	# ---- PASS T
	stamping = true
	var t0 := Time.get_ticks_usec()
	stamps.append([Engine.get_process_frames(), "t0", t0])
	var last := t0
	var next_cast := PRE_S
	var done := 0
	var end_s := PRE_S + CAST_GAP_S * float(casts)
	var pressed := false
	while true:
		await process_frame
		var now := Time.get_ticks_usec()
		var t := float(now - t0) / 1e6
		if t >= end_s:
			break
		if pressed:
			Input.action_release("cast")
			pressed = false
		if done < casts and t >= next_cast:
			Input.action_press("cast")
			pressed = true
			cast_at.append(t)
			done += 1
			next_cast += CAST_GAP_S
		rows.append(_row(t, now - last, done))
		last = now
	stamping = false
	var after_nodes := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	# ---- PASS W
	Input.action_press("cast")
	await process_frame
	Input.action_release("cast")
	var w0 := Time.get_ticks_usec()
	while float(Time.get_ticks_usec() - w0) / 1e6 < WALK_S:
		await process_frame
		var w := _walk()
		w["t_since_cast"] = snappedf(float(Time.get_ticks_usec() - w0) / 1e6, 0.001)
		w["nodes"] = int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
		w["phase"] = _phase()
		walk_rows.append(w)
	for i in 240:
		await process_frame
	var settled_nodes := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify({"kit": kit_name, "renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"window": [DisplayServer.window_get_size().x, DisplayServer.window_get_size().y],
		"base": {"nodes": base_nodes, "objects": base_objects, "resources": base_resources},
		"nodes_after_timing": after_nodes, "nodes_settled_after_walk": settled_nodes,
		"cast_at_s": cast_at, "rows": rows, "walk": walk_rows, "stamps": stamps}))
	f.close()
	print("[diag] %s: %d frames, %d casts, %d walk frames -> %s" % [kit_name, rows.size(), cast_at.size(), walk_rows.size(), out_file])
	quit(0)


func _phase() -> Dictionary:
	var proj := 0
	var draining := 0
	var impacts := 0
	var others := 0
	for c in actors.get_children():
		if c.is_in_group("vfx_g1_pool"):
			if c.get("active"):
				proj += 1
			elif c.get("draining") == true:
				draining += 1
		elif String(c.scene_file_path).contains("impact"):
			impacts += 1
		elif c.is_in_group("fire_mote_pool") and c.get("busy"):
			others += 1
	return {"proj": proj, "drain": draining, "impacts": impacts, "motes_busy": others}


func _row(t: float, dt_us: int, cast_n: int) -> Dictionary:
	var vp := root.get_viewport()
	var r := {"t": snappedf(t, 0.0001), "dt_ms": snappedf(float(dt_us) / 1000.0, 0.001),
		"process_ms": snappedf(Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0, 0.001),
		"physics_ms": snappedf(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0, 0.001),
		"render_cpu_ms": snappedf(RenderingServer.viewport_get_measured_render_time_cpu(root.get_viewport_rid()), 0.001),
		"render_gpu_ms": snappedf(RenderingServer.viewport_get_measured_render_time_gpu(root.get_viewport_rid()), 0.001),
		"dc_canvas": vp.get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS, Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),
		"dc_total": int(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)),
		"objs_in_frame": int(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_OBJECTS_IN_FRAME)),
		"pipe_canvas": int(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_PIPELINE_COMPILATIONS_CANVAS)),
		"tex_mem_mb": snappedf(float(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TEXTURE_MEM_USED)) / 1048576.0, 0.01),
		"nodes": int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT)),
		"objects": int(Performance.get_monitor(Performance.OBJECT_COUNT)),
		"resources": int(Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT)),
		"physics_frame": Engine.get_physics_frames(), "process_frame": Engine.get_process_frames(), "time_scale": Engine.time_scale,
		"cast": cast_n}
	r.merge(_phase())
	return r


func _walk() -> Dictionary:
	var classes := {}
	var mats := {}
	var shaders := {}
	var shader_paths := {}
	var texs := {}
	var area := 0.0
	var area_add := 0.0
	var visible_items := 0
	var lights := 0
	for n in actors.find_children("*", "CanvasItem", true, false):
		var ci := n as CanvasItem
		if not ci.is_visible_in_tree():
			continue
		# only the effect's own items: under a projectile, an impact or a mote pool, or a contact light
		var owner_kind := ""
		var p: Node = ci
		while p != null and p != actors:
			if p.is_in_group("vfx_g1_pool"):
				owner_kind = "projectile"
			elif String(p.scene_file_path).contains("impact"):
				owner_kind = "impact"
			elif p.is_in_group("fire_mote_pool"):
				owner_kind = "motes"
			p = p.get_parent()
		if owner_kind == "":
			continue
		visible_items += 1
		var cn := owner_kind + ":" + ci.get_class()
		classes[cn] = int(classes.get(cn, 0)) + 1
		var m := ci.material
		if m == null and ci.use_parent_material and ci.get_parent() is CanvasItem:
			m = (ci.get_parent() as CanvasItem).material
		var additive := false
		if m != null:
			mats[m.get_instance_id()] = true
			if m is ShaderMaterial and (m as ShaderMaterial).shader != null:
				var sh := (m as ShaderMaterial).shader
				shaders[sh.get_instance_id()] = true
				shader_paths[sh.resource_path if sh.resource_path != "" else "(runtime Shader.new)"] = int(shader_paths.get(sh.resource_path if sh.resource_path != "" else "(runtime Shader.new)", 0)) + 1
				additive = sh.code.contains("blend_add")
			elif m is CanvasItemMaterial:
				additive = (m as CanvasItemMaterial).blend_mode == CanvasItemMaterial.BLEND_MODE_ADD
		var tex: Texture2D = null
		var rect := Rect2()
		if ci is Sprite2D:
			tex = (ci as Sprite2D).texture
			if tex != null:
				rect = (ci as Sprite2D).get_rect()
		elif ci is AnimatedSprite2D:
			var asp := ci as AnimatedSprite2D
			if asp.sprite_frames != null and asp.sprite_frames.has_animation(asp.animation):
				tex = asp.sprite_frames.get_frame_texture(asp.animation, asp.frame)
				if tex != null:
					rect = Rect2(Vector2.ZERO, tex.get_size())
		elif ci is Polygon2D:
			var poly := (ci as Polygon2D).polygon
			if poly.size() > 2:
				var a := 0.0
				for i in poly.size():
					a += poly[i].cross(poly[(i + 1) % poly.size()])
				rect = Rect2(Vector2.ZERO, Vector2(sqrt(absf(a) * 0.5), sqrt(absf(a) * 0.5)))
		elif ci is PointLight2D:
			lights += 1
		if tex != null:
			texs[tex.get_instance_id()] = true
		if rect.size.x > 0.0 and ci is Node2D:
			var gt := (ci as Node2D).get_global_transform_with_canvas()
			var px := absf(rect.size.x * rect.size.y * gt.get_scale().x * gt.get_scale().y)
			area += px
			if additive:
				area_add += px
	return {"visible_effect_items": visible_items, "classes": classes, "unique_materials": mats.size(),
		"unique_shaders": shaders.size(), "shader_sources": shader_paths, "unique_textures": texs.size(),
		"quad_area_px2": snappedf(area, 1.0), "quad_area_additive_px2": snappedf(area_add, 1.0),
		"quad_area_over_screen": snappedf(area / (1920.0 * 1080.0), 0.001), "light2d": lights}
