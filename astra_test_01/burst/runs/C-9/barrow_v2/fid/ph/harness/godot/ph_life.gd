extends SceneTree
## BV2F lane PH (galadriel) -- P9 (life) and P10 (performance) probes. Read-only on the level; writes only to OUT.
##
##   Godot --path . --resolution 1920x1080 --script <abs>/ph_life.gd -- life <scene> <OUT> <view> [--no-wind]
##       a STATIC play camera at <view> (v1: "uv:U,V"; a v2 level: "xz:X,Z"), him absent, falling snow hidden:
##         f0.png, f1.png        two frames 0.5 s apart (the wind as shipped, or held with --no-wind: the RED input)
##         hide_heather.png      the heather shadow-only (its pixels = the heather mask)
##         hide_water.png, hide_water_b.png   the water meshes hidden, 0.5 s apart (the static painted sea: RED)
##         floe_m0/m1.png, hide_floe.png   (a level with floe_mesh) the floes wearing a 8 px CHECKER MARKER instead
##                               of the painting, 0.5 s apart, and the floes hidden: texture drift vs silhouette motion
##   Godot --path . --resolution 1920x1080 --script <abs>/ph_life.gd -- perf <scene> <OUT> <view> [--burn-ms N]
##       vsync off, uncapped; him walking a 4-point loop around <view>; EVERY frame's wall time for 900 frames
##       -> perf.json {p50, p99, max, frames}. --burn-ms N busy-waits N ms per frame: the constructed RED input.
var scene
var mode := ""
var out_dir := ""
var view := ""
var no_wind := false
var floe_red := false
var floe_pairs := 1        # --floe-pairs N: N marker pairs (m0, m1 0.5 s apart), pairs 0.7 s apart (R-C9-197 pre-registration)     # --floe-red: the floes' projection taken AFTER the bob (world-anchored paint: P9c's RED input)
var burn_ms := 0.0
var vp: SubViewport
var rep := {}


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	mode = a[0]
	var sp: String = a[1]
	out_dir = a[2]
	view = a[3]
	no_wind = a.has("--no-wind")
	floe_red = a.has("--floe-red")
	if a.has("--floe-pairs"):
		floe_pairs = int(a[a.find("--floe-pairs") + 1])
	if a.has("--burn-ms"):
		burn_ms = float(a[a.find("--burn-ms") + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load(sp).instantiate()
	scene.skip_character = (mode == "life")
	if mode == "life":
		vp = SubViewport.new()
		vp.size = Vector2i(1920, 1080)
		vp.own_world_3d = true
		vp.msaa_3d = Viewport.MSAA_4X
		vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(vp)
		vp.add_child(scene)
		_life()
	else:
		root.add_child(scene)
		_perf()


func _aim() -> Vector3:
	var p := view.substr(3).split(",")
	if view.begins_with("uv:"):
		return scene.uv_to_world(float(p[0]), float(p[1]))
	return Vector3(float(p[0]), 0.0, float(p[1]))


func _ready_scene() -> bool:
	var waited := 0
	while not scene.ready_done and waited < 4000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[ph] HALT: the scene never finished building")
		quit(3)
		return false
	scene.set_hud_visible(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	if scene.snowfall != null:
		scene.snowfall.visible = false
		scene.snowfall.emitting = false
	return true


func _settle(n := 10) -> void:
	for i in n:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 2:
		await process_frame
	vp.get_texture().get_image().save_png(out_dir.path_join(nm + ".png"))
	print("[ph] %s.png" % nm)


func _wait_s(s: float) -> void:
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(s * 1000.0):
		await process_frame


func _life() -> void:
	if not await _ready_scene():
		return
	if no_wind and scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	scene.park_camera(_aim(), 1.0)
	await _settle(30)
	await _shot("f0")
	var t0 := Time.get_ticks_msec()
	await _wait_s(0.5)
	await _shot("f1")
	rep["dt_ms"] = Time.get_ticks_msec() - t0
	var hs := {}
	for mmi in scene._heather_mmi:
		hs[mmi] = (mmi as GeometryInstance3D).cast_shadow
		(mmi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY
	if scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	await _settle()
	await _shot("hide_heather")
	await _shot("hide_heather_b")
	for mmi in hs:
		(mmi as GeometryInstance3D).cast_shadow = hs[mmi]
	if "water_meshes" in scene and not (scene.water_meshes as Array).is_empty():
		for w in scene.water_meshes:
			(w as Node3D).visible = false
		await _settle()
		await _shot("hide_water")
		await _wait_s(0.5)
		await _shot("hide_water_b")         # the sea with its motion layers gone, 0.5 s on: P9b's RED pair
		for w in scene.water_meshes:
			(w as Node3D).visible = true
	# BV2F pilot (bv2f_pilot.gd DEV-5): the sea is ground_sea's meshes wearing water_mat_pt; the floes are the
	# blobs_shore_ice__* placements, each with its own projected PAINTED material (rest-pose UVs)
	if "water_mat_pt" in scene and scene.water_mat_pt != null:
		var sea: Array = scene._meshes(scene.nodes["ground_sea"])
		for w in sea:
			(w as Node3D).visible = false
		await _settle()
		await _shot("hide_water")
		await _wait_s(0.5)
		await _shot("hide_water_b")
		for w in sea:
			(w as Node3D).visible = true
		var fl: Array = []
		for id in scene.nodes:
			if String(id).begins_with("blobs_shore_ice__"):
				fl += scene._meshes(scene.nodes[id])
		if not fl.is_empty():
			# P9c marker (R-C9-196 re-instrumentation), plate-space (projected paint), 1024 x 640 texels = 4 plate px each:
			#   R = 0.95 everywhere -> the floe's SILHOUETTE (alpha against hide_floe's R, sub-pixel under MSAA)
			#   G = band-limited simplex noise (aperiodic, ~16 px features) -> the floe's TEXTURE (no checker periodicity)
			var nz := FastNoiseLite.new()
			nz.noise_type = FastNoiseLite.TYPE_SIMPLEX
			nz.seed = 196
			nz.frequency = 0.22
			var nimg := nz.get_image(1024, 640, false, false, true)
			var img := Image.create(1024, 640, false, Image.FORMAT_RGB8)
			for y in 640:
				for x in 1024:
					img.set_pixel(x, y, Color(0.95, 0.05 + 0.9 * nimg.get_pixel(x, y).r, 0.5))
			var chk := ImageTexture.create_from_image(img)
			var saved := {}
			for mi in fl:
				var m := (mi as MeshInstance3D).material_override as ShaderMaterial
				if m == null or saved.has(m):
					continue
				saved[m] = [m.get_shader_parameter("paint_tex"), m.shader]
				m.set_shader_parameter("paint_tex", chk)
				# R-C9-197 (calibration.md § 31 A1): the marker keeps the floe's own (opaque) shader; the SEA meshes are hidden
				# for the marker shots instead, so no waterline can occlude the bobbing silhouette (the depth-test-off variant
				# drew no marker at all: § 31 A1 evidence)
				var code: String = m.shader.code
				if floe_red:
					var vw := "	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;\n"
					var bob := "vec3(0.03 * sin(TIME * 0.5 + bob_phase * 6.2831), 0.035 * sin(TIME * 0.9 + bob_phase * 6.2831) + 0.015 * sin(TIME * 2.1 + bob_phase * 6.2831 * 1.7), 0.03 * cos(TIME * 0.43 + bob_phase * 6.2831))"
					assert(code.count(vw) == 1)
					var sh := Shader.new()
					sh.code = code.replace(vw, "	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz + %s;   // PH RED: projection follows the bob\n" % bob)
					m.shader = sh
			rep["floes_pilot"] = {"meshes": fl.size(), "materials": saved.size(), "floe_red": floe_red}
			var sea_h: Array = scene._meshes(scene.nodes["ground_sea"]) if floe_pairs > 1 else []
			for w in sea_h:
				(w as Node3D).visible = false
			await _settle()
			for k in floe_pairs:
				var sfx := "" if k == 0 else "_%d" % k
				if k > 0:
					await _wait_s(0.7)
				await _shot("floe_m0" + sfx)
				await _wait_s(0.5)
				await _shot("floe_m1" + sfx)
			for m in saved:
				m.set_shader_parameter("paint_tex", saved[m][0])
				m.shader = saved[m][1]
			for mi in fl:
				(mi as Node3D).visible = false
			await _settle()
			await _shot("hide_floe")
			for w in sea_h:
				(w as Node3D).visible = true
			for mi in fl:
				(mi as Node3D).visible = true
	if "floe_mesh" in scene and scene.floe_mesh != null:
		var fm := scene.floe_mesh as MeshInstance3D
		var mat := fm.material_override as ShaderMaterial
		var img := Image.create(256, 256, false, Image.FORMAT_RGB8)
		for y in 256:
			for x in 256:
				var on := ((x / 8) + (y / 8)) % 2 == 0
				img.set_pixel(x, y, Color(0.95, 0.95, 0.95) if on else Color(0.1, 0.1, 0.1))
		var saved = mat.get_shader_parameter("paint_tex")
		mat.set_shader_parameter("paint_tex", ImageTexture.create_from_image(img))
		await _settle()
		await _shot("floe_m0")
		await _wait_s(0.5)
		await _shot("floe_m1")
		mat.set_shader_parameter("paint_tex", saved)
		fm.visible = false
		await _settle()
		await _shot("hide_floe")
		fm.visible = true
	rep["view"] = view
	rep["no_wind"] = no_wind
	var f := FileAccess.open(out_dir.path_join("life.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[ph] life done -> %s" % out_dir)
	quit(0)


func _perf() -> void:
	if not await _ready_scene():
		return
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	var k = scene.knight
	k.set_physics_process(false)
	var c: Vector2 = scene.world_to_uv(_aim())
	var loop := [c + Vector2(4.0, 1.0), c + Vector2(0.0, 5.0), c + Vector2(-4.0, 1.0), c + Vector2(0.0, -3.0)]
	scene.place_knight(loop[3].x, loop[3].y, "N")
	var wi := 0
	var dt := 1.0 / 60.0
	for i in 180:
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await process_frame
	var n := 900
	var times := PackedFloat64Array()
	var t_prev := Time.get_ticks_usec()
	for i in n:
		if scene.knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		if burn_ms > 0.0:
			var b0 := Time.get_ticks_usec()
			while Time.get_ticks_usec() - b0 < int(burn_ms * 1000.0):
				pass
		await process_frame
		var t := Time.get_ticks_usec()
		times.append(float(t - t_prev) / 1000.0)
		t_prev = t
	var s := Array(times)
	s.sort()
	var total := 0.0
	for x in s:
		total += float(x)
	rep = {"scene": scene.scene_file_path, "view": view, "burn_ms": burn_ms, "frames": n, "mean_ms": total / n,
		"p50_ms": s[int(n * 0.5)], "p99_ms": s[int(n * 0.99)], "max_ms": s[n - 1],
		"render": [root.get_texture().get_width(), root.get_texture().get_height()],
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	var f := FileAccess.open(out_dir.path_join("perf.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[ph] perf ", JSON.stringify(rep))
	quit(0)
