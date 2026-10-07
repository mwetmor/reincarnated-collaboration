extends SceneTree
## BV2F lane LV, R-C9-188/189: the WALKABILITY instrument of the barrow_v2 art level (scenes/bv2f_barrow_v2.tscn).
## Driven by fid/lv/tools/lv_walkability.py (which writes the spec and reads the result); not a paint-pipeline tool.
##   Godot --path godot --resolution 640x360 --script tools/bv2f/walk_check.gd -- --out DIR --spec SPEC.json
##
## Three measurements, all against the level's own COLLIDERS (what a body stands on), never its meshes:
##  1. SURVEY: for each spec sample (u, v) a ray straight down from 1.0 m above the expected floor (scene.floor_y_at),
##     the hit height and normal; whether a body's middle there is inside any collider (intersect_point); the clear
##     headroom straight up; for each cross-section point, the free run sideways at knee and chest height.
##  2. DRIVE: v1's OWN knight (scripts/knight.gd, unmodified: its capsule, its move_and_slide, its gravity, its default
##     floor_max_angle) walked by drive_dir -- exactly as barrow_full.gd's own frame-cost walk drives him -- through the
##     spec's waypoints from inside the cave to the clifftop; his position every physics frame.
##  3. STILLS: a top-down and a play-camera still of the route with the driven track drawn on it (a check overlay).
const PLAY := Vector2i(1920, 1080)
const DT := 1.0 / 60.0
var vp: SubViewport
var scene


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := ""
	var spec_p := ""
	for i in args.size():
		if args[i] == "--out":
			out_dir = args[i + 1]
		if args[i] == "--spec":
			spec_p = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	var spec: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(spec_p))
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_barrow_v2.tscn").instantiate()
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	scene.set_hud_visible(false)
	var k: CharacterBody3D = scene.knight
	var out := {"what": "walk_check.gd (R-C9-188/189): colliders surveyed + v1's knight driven"}
	# --- his body, read off the running node (the citation is the object, not the source text) ---
	var cap: CapsuleShape3D = null
	for ch in k.get_children():
		if ch is CollisionShape3D and (ch as CollisionShape3D).shape is CapsuleShape3D:
			cap = (ch as CollisionShape3D).shape
	out["knight"] = {"class": k.get_class(), "script": String(k.get_script().resource_path), "capsule_radius_m": cap.radius, "capsule_height_m": cap.height,
		"floor_max_angle_deg": rad_to_deg(k.floor_max_angle), "floor_snap_length_m": k.floor_snap_length, "max_slides": k.max_slides,
		"floor_constant_speed": k.floor_constant_speed, "floor_stop_on_slope": k.floor_stop_on_slope, "collision_mask": k.collision_mask,
		"step_height_m": cap.radius * (1.0 - cos(k.floor_max_angle)),
		"_step": "no step-up code in knight.gd: an edge is climbed only while the capsule's contact normal is within floor_max_angle of up -> h <= r (1 - cos(floor_max_angle))"}
	k.set_physics_process(false)
	scene.park_camera(scene.uv_to_world(0.0, 0.0), 1.0)
	for i in 4:
		await physics_frame
	var space: PhysicsDirectSpaceState3D = k.get_world_3d().direct_space_state
	var mask: int = k.collision_mask
	# --- 1. SURVEY ---
	var survey := []
	for s in spec["samples"]:
		var u := float(s[0])
		var v := float(s[1])
		var zf: float = scene.floor_y_at(u, v)
		var top: Vector3 = scene.uv_to_world(u, v, zf + 1.0)
		var q := PhysicsRayQueryParameters3D.create(top, scene.uv_to_world(u, v, zf - 3.0), mask)
		var h := space.intersect_ray(q)
		var rec := {"uv": [u, v], "hit": not h.is_empty()}
		if not h.is_empty():
			var p: Vector3 = h["position"]
			var n: Vector3 = h["normal"]
			rec["z"] = p.y
			rec["slope_deg"] = rad_to_deg(acos(clampf(n.dot(Vector3.UP), -1.0, 1.0)))
			var pq := PhysicsPointQueryParameters3D.new()
			pq.collision_mask = mask
			var inside := false
			for hz in [0.3, 0.9, 1.5]:
				pq.position = p + Vector3.UP * hz
				if not space.intersect_point(pq, 1).is_empty():
					inside = true
			rec["body_blocked"] = inside
			var uq := PhysicsRayQueryParameters3D.create(p + Vector3.UP * 0.05, p + Vector3.UP * 15.0, mask)
			var uh := space.intersect_ray(uq)
			rec["headroom_m"] = 15.0 if uh.is_empty() else (uh["position"] as Vector3).y - p.y
		survey.append(rec)
	out["survey"] = survey
	# cross-section side runs: from the section's centre, at 0.4 m and 1.2 m above its floor, both ways along `across`
	var sides := []
	for sec in spec.get("sections", []):
		var c: Array = sec["centre"]
		var a: Array = sec["across"]
		var zf2: float = scene.floor_y_at(float(c[0]), float(c[1]))
		var q2 := PhysicsRayQueryParameters3D.create(scene.uv_to_world(float(c[0]), float(c[1]), zf2 + 1.0), scene.uv_to_world(float(c[0]), float(c[1]), zf2 - 3.0), mask)
		var h2 := space.intersect_ray(q2)
		var z0 := zf2 if h2.is_empty() else (h2["position"] as Vector3).y
		var rec2 := {"id": sec["id"], "centre": c, "z": z0}
		for hz in [0.4, 1.2]:
			for sgn in [-1.0, 1.0]:
				var p0: Vector3 = scene.uv_to_world(float(c[0]), float(c[1]), z0 + hz)
				var p1: Vector3 = scene.uv_to_world(float(c[0]) + sgn * float(a[0]) * 8.0, float(c[1]) + sgn * float(a[1]) * 8.0, z0 + hz)
				var hh := space.intersect_ray(PhysicsRayQueryParameters3D.create(p0, p1, mask))
				rec2["free_%s_%.1f" % ["neg" if sgn < 0.0 else "pos", hz]] = 8.0 if hh.is_empty() else p0.distance_to(hh["position"])
		sides.append(rec2)
	out["sections"] = sides
	# --- 2. DRIVE ---
	var wps: Array = spec["waypoints"]
	scene.freeze_pose(false)
	scene.place_knight(float(wps[0][0]), float(wps[0][1]), "S")
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	var track := []
	var wi := 1
	var t := 0.0
	var stuck_t := 0.0
	var last := k.global_position
	var reached := false
	var max_t := float(spec.get("drive_timeout_s", 90.0))
	while t < max_t:
		var kuv: Vector2 = scene.knight_uv()
		var tgt := Vector2(float(wps[wi][0]), float(wps[wi][1]))
		if kuv.distance_to(tgt) < float(spec.get("waypoint_radius_m", 0.5)):
			wi += 1
			if wi >= wps.size():
				reached = true
				break
			tgt = Vector2(float(wps[wi][0]), float(wps[wi][1]))
		k.drive_dir(scene.canvas_dir_uv(kuv, tgt), false, DT)
		await physics_frame
		t += DT
		var gp := k.global_position
		track.append([snappedf(kuv.x, 0.001), snappedf(kuv.y, 0.001), snappedf(gp.y, 0.001), k.is_on_floor(), wi])
		if gp.distance_to(last) < 0.002:
			stuck_t += DT
			if stuck_t > 3.0:
				break
		else:
			stuck_t = 0.0
		last = gp
	out["drive"] = {"reached_last_waypoint": reached, "time_s": snappedf(t, 0.001), "waypoint_index": wi, "waypoints": wps, "frames": track.size(),
		"stuck_3s": stuck_t > 3.0, "end_uv": [scene.knight_uv().x, scene.knight_uv().y], "end_z": k.global_position.y}
	out["track"] = track
	# --- 3. STILLS: the track drawn (a magenta ribbon 0.12 m over his feet), him back on the stair for scale ---
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	var step := 3
	for i in range(0, track.size() - step, step):
		var a3: Vector3 = scene.uv_to_world(float(track[i][0]), float(track[i][1]), float(track[i][2]) + 0.12)
		var b3: Vector3 = scene.uv_to_world(float(track[i + step][0]), float(track[i + step][1]), float(track[i + step][2]) + 0.12)
		var d := (b3 - a3)
		if d.length() < 1e-4:
			continue
		var side := d.cross(Vector3.UP).normalized() * 0.12
		V.append_array(PackedVector3Array([a3 - side, b3 - side, b3 + side, a3 - side, b3 + side, a3 + side]))
		for j in 6:
			N.append(Vector3.UP)
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = V
	arr[Mesh.ARRAY_NORMAL] = N
	var am := ArrayMesh.new()
	if V.size() > 0:
		am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var rib := MeshInstance3D.new()
	rib.mesh = am
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = Color(1, 0, 1)
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	rib.material_override = m
	rib.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	scene.add_child(rib)
	rib.top_level = true
	var st: Array = spec["stills"]["him_uv"]
	scene.place_knight(float(st[0]), float(st[1]), "W")
	for i in 20:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	var pa: Array = spec["stills"]["play_aim"]
	scene.park_camera(scene.uv_to_world(float(pa[0]), float(pa[1]), float(pa[2])), 1.0)
	for i in 8:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
	vp.get_texture().get_image().save_png("%s/route_play.png" % out_dir)
	var td: Array = spec["stills"]["topdown"]
	vp.size = Vector2i(int(td[3]), int(td[4]))
	scene.sun.shadow_enabled = false
	scene.set_topdown(Vector2(float(td[0]), float(td[1])), float(td[2]))
	for i in 8:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
	vp.get_texture().get_image().save_png("%s/route_topdown.png" % out_dir)
	out["stills"] = {"route_play.png": {"aim": pa, "him_uv": st, "px": [PLAY.x, PLAY.y]}, "route_topdown.png": {"centre_uv": [td[0], td[1]], "height_m": td[2], "px": [td[3], td[4]]}}
	var f := FileAccess.open("%s/walk_check.json" % out_dir, FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("[walk] reached=%s t=%.2f s frames=%d samples=%d" % [str(reached), t, track.size(), survey.size()])
	quit(0)
