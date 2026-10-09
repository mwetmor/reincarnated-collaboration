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
var floe_red := false     # --floe-red: the floes' projection taken AFTER the bob (world-anchored paint: P9c's RED input)
var floe_null := ""       # --floe-null bobt|rigid|static (s54, R-C9-335): P9c discriminator; bob driven by a uniform ph_t
var floe_ids := false     # --floe-ids (s56, R-C9-336): after every controlled-time marker shot, a per-floe ID shot (floe_idN)
var floe_solo := false    # --floe-solo (s56): every non-floe GeometryInstance3D hidden for the marker / ID / hide_floe shots (extends s31 A1)
var floe_wallclock := false   # --floe-wallclock (s60, C-7): ph_t = engine seconds at each shot, on the s53 schedule (0.5 s / 0.7 s wall)
var floe_pairs := 1       # --floe-pairs N: N marker pairs (m0, m1 0.5 s apart), pairs 0.7 s apart (R-C9-197 pre-registration)
var t_ready_us := 0       # R-C9-201: ready_done as this tool sees it (the perf trace's zero)
var idle := false         # --idle: perf with him STANDING at <view> (R-C9-276 report-only water-cost view)
var loop_arg := ""        # --loop "u,v;u,v;...": absolute walk waypoints (R-C9-272: the default loop is not reachable on rp4)
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
	idle = a.has("--idle")
	if a.has("--loop"):
		loop_arg = a[a.find("--loop") + 1]
	if a.has("--floe-null"):
		floe_null = a[a.find("--floe-null") + 1]
	floe_ids = a.has("--floe-ids")
	floe_solo = a.has("--floe-solo")
	floe_wallclock = a.has("--floe-wallclock")
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
	t_ready_us = Time.get_ticks_usec()      # R-C9-201: the trace's zero (the scene's ready_done, seen by this tool)
	return true


func _pilot_sea() -> Array:
	"""the WATER meshes of the pilot sea (ground_sea), not the '_above_water' land split off them (R-C9-232)"""
	var out := []
	for mi in scene._meshes(scene.nodes["ground_sea"]):
		if not String((mi as Node).name).ends_with("_above_water"):
			out.append(mi)
	return out


func _pilot_floes() -> Array:
	"""the BOBBING floes: blobs_shore_ice__* placements (Phase 2'), and the 'floe_N' pieces split out of the ice_floes_bob
	slab group (R-C9-232; its original mesh is hidden)"""
	var out := []
	for id in scene.nodes:
		if String(id).begins_with("blobs_shore_ice__"):
			out += scene._meshes(scene.nodes[id])
	if scene.nodes.has("ice_floes_bob"):
		for n in (scene.nodes["ice_floes_bob"] as Node).get_parent().find_children("floe_*", "MeshInstance3D", true, false):
			out.append(n)
	return out


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
		var sea: Array = _pilot_sea()
		for w in sea:
			(w as Node3D).visible = false
		await _settle()
		await _shot("hide_water")
		await _wait_s(0.5)
		await _shot("hide_water_b")
		for w in sea:
			(w as Node3D).visible = true
		# F-4 (calibration.md § 38): a GEOMETRY mask in this camera -- the sea meshes flat pure green, the floes flat pure red,
		# unshaded, one frame; P9 flow's water mask and floe exclusion come from it (no cross-time differences)
		var gm := StandardMaterial3D.new()
		gm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		gm.albedo_color = Color(0, 1, 0)
		var rm := StandardMaterial3D.new()
		rm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		rm.albedo_color = Color(1, 0, 0)
		var geo_saved := {}
		for w in sea:
			geo_saved[w] = (w as GeometryInstance3D).material_override
			(w as GeometryInstance3D).material_override = gm
		for mi in _pilot_floes():
			geo_saved[mi] = (mi as GeometryInstance3D).material_override
			(mi as GeometryInstance3D).material_override = rm
		await _settle()
		await _shot("geo_mask")
		for mi in geo_saved:
			(mi as GeometryInstance3D).material_override = geo_saved[mi]
		var fl: Array = _pilot_floes()
		rep["pilot_water"] = {"sea_meshes": sea.size(), "floe_meshes": fl.size()}
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
				if floe_null != "":
					# s54 (R-C9-335). bobt: the shipped bob with TIME -> uniform ph_t (same geometry path, controlled time).
					# rigid/static: NO shader bob; each floe NODE is translated by the bob's own world displacement wd(ph_t)
					# and the projection is compensated (v_world -= ph_off = wd), so the texture is attached BY CONSTRUCTION
					# (truth: drift 0). static: rigid with t1 = t0 (no motion).
					var c2: String = m.shader.code
					var blk0 := c2.find("	float ph = bob_phase * 6.2831;")
					var blk1 := c2.find("	VERTEX += inverse(mat3(MODEL_MATRIX)) * wd;\n")
					assert(blk0 > 0 and blk1 > blk0)
					var bob_blk := c2.substr(blk0, blk1 + "	VERTEX += inverse(mat3(MODEL_MATRIX)) * wd;\n".length() - blk0)
					var nb: String
					if floe_null == "bobt":
						nb = bob_blk
					else:
						nb = "	v_world -= ph_off;   // PH s54 null: node moved by wd, projection held at rest\n"
					c2 = c2.replace(bob_blk, nb)
					if floe_null == "bobt":
						c2 = c2.replace("TIME", "ph_t")     # the bob, and the RED's projection bob when --floe-red
					c2 = c2.replace("uniform float his_shadow_on = 1.0;\n", "uniform float his_shadow_on = 1.0;\nuniform float ph_t = 0.0;\ninstance uniform vec3 ph_off = vec3(0.0);\n")
					var sh2 := Shader.new()
					sh2.code = c2
					m.shader = sh2
			rep["floes_pilot"] = {"meshes": fl.size(), "materials": saved.size(), "floe_red": floe_red, "floe_null": floe_null}
			var sea_h: Array = _pilot_sea() if floe_pairs > 1 else []
			for w in sea_h:
				(w as Node3D).visible = false
			var solo_h := []
			if floe_solo:
				var fset := {}
				for mi in fl:
					fset[mi] = true
				for gi in scene.find_children("*", "GeometryInstance3D", true, false):
					if not fset.has(gi) and (gi as Node3D).visible:
						(gi as Node3D).visible = false
						solo_h.append(gi)
				rep["floe_solo_hidden"] = solo_h.size()
			await _settle()
			var rest := {}
			for mi in fl:
				rest[mi] = (mi as Node3D).global_position
			var nul_t := []
			for k in floe_pairs:
				var sfx := "" if k == 0 else "_%d" % k
				if floe_null != "":
					var nt0 := 1.0 + 1.2 * float(k)
					var nt1 := nt0 if floe_null == "static" else nt0 + 0.5
					var tm0 := 0
					if floe_wallclock:
						if k > 0:
							await _wait_s(0.7)
						tm0 = Time.get_ticks_msec()
						nt0 = float(tm0) / 1000.0
					_null_set(fl, saved, rest, nt0)
					await _settle()
					await _shot("floe_m0" + sfx)
					if floe_ids:
						await _id_shot(fl, "floe_id0" + sfx, rest, nt0)
					if floe_wallclock:
						while Time.get_ticks_msec() - tm0 < 500:
							await process_frame
						nt1 = nt0 if floe_null == "static" else float(Time.get_ticks_msec()) / 1000.0
					nul_t.append([nt0, nt1])        # s60: logged AFTER the wall-clock t1 is taken (the C-7 run logged a stale t1)
					_null_set(fl, saved, rest, nt1)
					await _settle()
					await _shot("floe_m1" + sfx)
					if floe_ids:
						await _id_shot(fl, "floe_id1" + sfx, rest, nt1)
					continue
				if k > 0:
					await _wait_s(0.7)
				await _shot("floe_m0" + sfx)
				await _wait_s(0.5)
				await _shot("floe_m1" + sfx)
			if floe_null != "":
				for mi in fl:
					(mi as Node3D).global_position = rest[mi]
				rep["floe_null_times"] = nul_t
			for m in saved:
				m.set_shader_parameter("paint_tex", saved[m][0])
				m.shader = saved[m][1]
			for mi in fl:
				(mi as Node3D).visible = false
			await _settle()
			await _shot("hide_floe")
			for gi in solo_h:
				(gi as Node3D).visible = true
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
	if loop_arg != "":
		loop = []
		for pt in loop_arg.split(";"):
			var xy := pt.split(",")
			loop.append(Vector2(float(xy[0]), float(xy[1])))
	if idle:
		scene.place_knight(c.x, c.y, "S")
	else:
		scene.place_knight(loop[3].x, loop[3].y, "N")
	var wi := 0
	var dt := 1.0 / 60.0
	var pre := PackedFloat64Array()
	var tp := Time.get_ticks_usec()
	for i in 180:
		if not idle:
			k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, dt)
		await process_frame
		var tq := Time.get_ticks_usec()
		pre.append(float(tq - tp) / 1000.0)
		tp = tq
	var n := 900
	var kpos := []            # R-C9-272: the knight's (u, v) every frame of the window -- the walk-validity trace
	var times := PackedFloat64Array()
	var t_prev := Time.get_ticks_usec()
	var t_win0 := t_prev
	for i in n:
		if not idle:
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
		var ku: Vector2 = scene.knight_uv()
		kpos.append([snappedf(ku.x, 0.001), snappedf(ku.y, 0.001), wi])
	var s := Array(times)
	s.sort()
	var total := 0.0
	for x in s:
		total += float(x)
	rep = {"scene": scene.scene_file_path, "view": view, "burn_ms": burn_ms, "frames": n, "idle": idle, "mean_ms": total / n,
		"p50_ms": s[int(n * 0.5)], "p99_ms": s[int(n * 0.99)], "max_ms": s[n - 1],
		"render": [root.get_texture().get_width(), root.get_texture().get_height()],
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	var f := FileAccess.open(out_dir.path_join("perf.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	# R-C9-201: the frame-time TRACE aligned to the load timeline (ms; zero = ready_done as this tool sees it)
	var tr := {"t_ready_since_engine_start_ms": float(t_ready_us) / 1000.0, "window_start_rel_ready_ms": float(t_win0 - t_ready_us) / 1000.0,
		"preroll_frames_ms": Array(pre), "window_frames_ms": Array(times), "knight_uv_wp": kpos,
		"loop": loop.map(func(q): return [q.x, q.y])}
	var f2 := FileAccess.open(out_dir.path_join("trace.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify(tr))
	f2.close()
	print("[ph] perf ", JSON.stringify(rep))
	quit(0)


func _bob_wd(t: float, phase: float) -> Vector3:
	var ph := phase * 6.2831
	return Vector3(0.03 * sin(t * 0.5 + ph), 0.035 * sin(t * 0.9 + ph) + 0.015 * sin(t * 2.1 + ph * 1.7), 0.03 * cos(t * 0.43 + ph))


func _null_set(fl: Array, saved: Dictionary, rest: Dictionary, t: float) -> void:
	"""s54: bobt -> ph_t = t on the (shared) floe materials; rigid/static -> each floe node at rest + wd(t, its phase),
	ph_off = wd (the projection held at rest)"""
	for m in saved:
		(m as ShaderMaterial).set_shader_parameter("ph_t", t)
	if floe_null == "bobt":
		return
	for mi in fl:
		var phase := float((mi as Node).get_meta("bob_phase", 0.0))
		var wd := _bob_wd(t, phase)
		(mi as Node3D).global_position = rest[mi] + wd
		(mi as GeometryInstance3D).set_instance_shader_parameter("ph_off", wd)


func _id_color(j: int) -> Color:
	"""s56: floe j -> a flat unshaded colour from 6 x 6 x 2 levels (R, G in {0, 51, ..., 255}; B in {0, 255}); decoded by
	nearest palette entry, MSAA-blended edge px rejected by distance"""
	var r := j % 6
	var g := (j / 6) % 6
	var b := (j / 36) % 2
	return Color8(r * 51, g * 51, b * 255)


func _id_shot(fl: Array, nm: String, rest: Dictionary, t: float) -> void:
	"""the ID shot at the SAME pose: in bobt (vertex bob, which a StandardMaterial lacks) each node is placed at rest + wd(t)
	for the shot (the rigid pose s55 showed image-identical) and put back after; rigid/static nodes are already there"""
	if floe_null == "bobt":
		for mi in fl:
			(mi as Node3D).global_position = rest[mi] + _bob_wd(t, float((mi as Node).get_meta("bob_phase", 0.0)))
	var keep := {}
	for j in fl.size():
		var mi := fl[j] as GeometryInstance3D
		keep[mi] = mi.material_override
		var sm := StandardMaterial3D.new()
		sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sm.albedo_color = _id_color(j + 1)
		mi.material_override = sm
	await _settle(2)
	await _shot(nm)
	for mi in keep:
		(mi as GeometryInstance3D).material_override = keep[mi]
	if floe_null == "bobt":
		for mi in fl:
			(mi as Node3D).global_position = rest[mi]
	await _settle(2)
