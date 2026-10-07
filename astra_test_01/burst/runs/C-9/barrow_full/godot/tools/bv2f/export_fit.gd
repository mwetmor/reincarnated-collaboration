extends SceneTree
## BV2F LV (R-C9-180 W2): every PLACED model instance of the level, as built -- its per-axis fit scale (bv2f_level.gd
## _place_box fits each model's AABB to its slot PER AXIS), the anisotropy (max/min axis scale), and its own scene
## footprint (convex hull of its vertices in the sim frame, x east / y south) + height (z min/max).
##   BV2F_VARIANT=v7c Godot --path godot --script tools/bv2f/export_fit.gd -- <out.json>
func _initialize() -> void:
	var out_p := OS.get_cmdline_user_args()[0]
	var vp := SubViewport.new()
	vp.size = Vector2i(320, 180)
	vp.own_world_3d = true
	root.add_child(vp)
	var scene = load("res://scenes/bv2f_barrow_v2.tscn").instantiate()
	scene.skip_character = true
	vp.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 1500:
		await process_frame
		w += 1
	var inv: Transform3D = scene.level.global_transform.affine_inverse()
	var rows := []
	# R-C9-181 (3): R11 read PER REGION of the one hall + porch mesh -- the porch region = the hall_porch slot footprint
	var porch_poly := PackedVector2Array()
	for m in scene.sim["models"]:
		if String(m["id"]) == "hall_porch":
			for q in m.get("r11_region_footprint", m["footprint"]):
				porch_poly.append(Vector2(float(q[0]), float(q[1])))
	for n in scene.level.find_children("*", "Node3D", true, false):
		if not (n as Node).has_meta("bv2f_fit"):
			continue
		var meta: Dictionary = (n as Node).get_meta("bv2f_fit")
		var pts := PackedVector2Array()
		var zlo := INF
		var zhi := -INF
		for mi in (n as Node).find_children("*", "MeshInstance3D", true, false):
			var m := mi as MeshInstance3D
			if String(m.name).ends_with("_ink") or m.mesh == null:
				continue
			var xf: Transform3D = inv * m.global_transform
			for si in m.mesh.get_surface_count():
				var vs: PackedVector3Array = m.mesh.surface_get_arrays(si)[Mesh.ARRAY_VERTEX]
				for k in range(0, vs.size(), 3):
					var p: Vector3 = xf * vs[k]
					pts.append(Vector2(p.x, p.z))
					zlo = minf(zlo, p.y)
					zhi = maxf(zhi, p.y)
		var region := {}
		if String(meta["slot"]) == "longhall" and porch_poly.size() >= 3:
			var zb := -INF
			var zp := -INF
			for mi2 in (n as Node).find_children("*", "MeshInstance3D", true, false):
				var m2 := mi2 as MeshInstance3D
				if String(m2.name).ends_with("_ink") or m2.mesh == null:
					continue
				var xf2: Transform3D = inv * m2.global_transform
				for si2 in m2.mesh.get_surface_count():
					for v in (m2.mesh.surface_get_arrays(si2)[Mesh.ARRAY_VERTEX] as PackedVector3Array):
						var p2: Vector3 = xf2 * v
						if Geometry2D.is_point_in_polygon(Vector2(p2.x, p2.z), porch_poly):
							zp = maxf(zp, p2.y)
						else:
							zb = maxf(zb, p2.y)
			region = {"porch_region_max_z_m": snappedf(zp, 0.001), "hall_body_region_max_z_m": snappedf(zb, 0.001),
				"porch_region": "the hall_porch slot r11_region_footprint: the porch strip along the wall through the build depth (layout_v7c)", "rule": "R11 per region (R-C9-181): porch roof = max z over the porch footprint; hall roof = max z over the rest of the build"}
		var hull := Geometry2D.convex_hull(pts)
		var hp := []
		for q in hull:
			hp.append([snappedf(q.x, 0.001), snappedf(q.y, 0.001)])
		var sc: Array = meta["fit_scale_xyz"]
		var mx := maxf(float(sc[0]), maxf(float(sc[1]), float(sc[2])))
		var mn := minf(float(sc[0]), minf(float(sc[1]), float(sc[2])))
		var row := meta.duplicate()
		row["anisotropy_max_over_min"] = snappedf(mx / maxf(mn, 1e-9), 0.0001)
		row["scene_footprint_sim_xy"] = hp
		row["z_min_m"] = snappedf(zlo, 0.001)
		row["z_max_m"] = snappedf(zhi, 0.001)
		row["height_m"] = snappedf(zhi - zlo, 0.001)
		if not region.is_empty():
			row["r11_regions"] = region
		rows.append(row)
	var f := FileAccess.open(out_p, FileAccess.WRITE)
	f.store_string(JSON.stringify({"variant": OS.get_environment("BV2F_VARIANT"), "instances": rows}, " "))
	f.close()
	print("[export_fit] %d instances -> %s" % [rows.size(), out_p])
	quit(0)
