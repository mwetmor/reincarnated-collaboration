extends SceneTree
# C-9 T10: WHY IS THERE NO GROUND.
#
# The barrow's props, its snow, its sky and the barbarian all render; the terrain does not,
# and everything stands in mid-air over a sky gradient. Four candidate causes, and they are
# distinguished by four renders of the SAME mesh rather than by reasoning about winding
# order -- which I have already reasoned about twice and got a "should render" both times.
#
#   1. it is not in the tree, or not visible, or on a layer the camera does not see
#   2. it is somewhere else (wrong transform, wrong height, AABB elsewhere)
#   3. it is backface-culled (winding)
#   4. its MATERIAL draws nothing (the world shader, on this mesh, for some reason the props
#      do not share -- they use the same shader and they are fine, so this is the least
#      likely and therefore the one worth a control)
#
# Each render isolates one. The screen position where the mesh SHOULD be is computed from
# the camera's own unproject, and a physics ray down the view axis says whether anything is
# there at all -- collision is built from the same arrays as the render mesh, so if the ray
# hits and the pixel is sky, the geometry exists and the DRAW is what is failing.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_terrain.gd -- --out DIR

const SHOT := Vector2i(960, 540)

var out := ""
var source := "stand_in"          # or heightfield_authored / heightfield_marigold
var report := {}


func _initialize() -> void:
	out = ProjectSettings.globalize_path("user://probe_terrain")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
		if args[i] == "--source" and i + 1 < args.size():
			source = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)

	var vp := SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var scene = preload("res://scripts/barrow_world.gd").new()
	scene.skip_character = true
	scene.terrain_source = source
	vp.add_child(scene)
	for i in 50:
		await process_frame
		await physics_frame

	# either builder's node: BarrowStandIn names it Terrain, BarrowHeightfield BarrowGround
	var terr := scene.get_node_or_null(^"Terrain") as MeshInstance3D
	if terr == null:
		terr = scene.get_node_or_null(^"BarrowGround") as MeshInstance3D
	report["source"] = source
	report["terrain_node_name"] = "none" if terr == null else String(terr.name)
	var cam: Camera3D = scene.cam
	if terr == null:
		report["FATAL"] = "no node named Terrain under the scene root"
		for c in scene.get_children():
			report.get_or_add("children", []).append("%s (%s)" % [c.name, c.get_class()])
		_write()
		return

	# --- 1 + 2: is it there, and where -------------------------------------
	var ab: AABB = terr.get_aabb()
	var gab: AABB = terr.global_transform * ab
	report["terrain_node"] = {
		"in_tree": terr.is_inside_tree(),
		"visible": terr.visible,
		"visible_in_tree": terr.is_visible_in_tree(),
		"layers": terr.layers,
		"cast_shadow": terr.cast_shadow,
		"global_origin": _v(terr.global_transform.origin),
		"scale": _v(terr.global_transform.basis.get_scale()),
		"aabb_pos": _v(ab.position), "aabb_size": _v(ab.size),
		"surfaces": terr.mesh.get_surface_count(),
		"material_override": str(terr.material_override),
		"extra_cull_margin": terr.extra_cull_margin,
	}
	var arrs := terr.mesh.surface_get_arrays(0)
	var vv: PackedVector3Array = arrs[Mesh.ARRAY_VERTEX]
	var nn = arrs[Mesh.ARRAY_NORMAL]
	var ii = arrs[Mesh.ARRAY_INDEX]
	report["terrain_arrays"] = {
		"vertices": vv.size(),
		"normals": 0 if nn == null else (nn as PackedVector3Array).size(),
		"indices": 0 if ii == null else (ii as PackedInt32Array).size(),
		"first_vertex": _v(vv[0]),
		"mid_vertex": _v(vv[vv.size() / 2]),
		"first_normal": "none" if nn == null else _v((nn as PackedVector3Array)[0]),
	}
	report["camera"] = {
		"pos": _v(cam.global_position),
		"size_m": snappedf(cam.size, 0.0001),
		"near": cam.near, "far": cam.far,
		"cull_mask": cam.cull_mask,
		"fwd": _v(-cam.global_transform.basis.z),
		"up": _v(cam.global_transform.basis.y),
	}
	# where the mesh's own centre lands on screen, and how deep it is
	var centre := gab.get_center()
	var cfwd := -cam.global_transform.basis.z
	report["where_it_should_be"] = {
		"aabb_centre_world": _v(centre),
		"screen_px": _v2(cam.unproject_position(centre)),
		"depth_from_camera_m": snappedf((centre - cam.global_position).dot(cfwd), 0.01),
		"is_behind_camera": (centre - cam.global_position).dot(cfwd) < 0.0,
		"near_far": [cam.near, cam.far],
		"_frame_is": [SHOT.x, SHOT.y],
	}
	# and does a ray down the view axis hit the collision built from the same arrays
	var space := scene.get_world_3d().direct_space_state
	var aim := Vector3(0.0, scene.world.height_at(0.0, 0.0), 0.0)
	var q := PhysicsRayQueryParameters3D.create(aim - cfwd * 200.0, aim + cfwd * 200.0)
	q.collision_mask = 0xFFFFFFFF
	var hit := space.intersect_ray(q)
	report["ray_down_view_axis"] = {} if hit.is_empty() else {
		"hit": str(hit.get("collider")), "position": _v(hit["position"]),
		"normal": _v(hit["normal"]),
	}

	# --- 3 + 4: four renders of the same mesh ------------------------------
	scene.set_hud_visible(false)
	scene.park_camera(aim + Vector3(0, 1.4, 0), 0.30)
	scene.set_particles(false)
	await _settle(vp)

	var plain := StandardMaterial3D.new()
	plain.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	plain.albedo_color = Color(1.0, 0.0, 0.8)
	var plain_nocull := StandardMaterial3D.new()
	plain_nocull.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	plain_nocull.albedo_color = Color(0.0, 1.0, 0.4)
	plain_nocull.cull_mode = BaseMaterial3D.CULL_DISABLED
	var flipped := StandardMaterial3D.new()
	flipped.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	flipped.albedo_color = Color(1.0, 0.85, 0.0)
	flipped.cull_mode = BaseMaterial3D.CULL_FRONT

	var keep := terr.material_override
	for spec in [["as_built", keep], ["unshaded_magenta", plain],
				 ["unshaded_nocull_green", plain_nocull], ["unshaded_cullfront_yellow", flipped]]:
		terr.material_override = spec[1]
		await _settle(vp)
		var img: Image = vp.get_texture().get_image()
		img.save_png("%s/terr_%s.png" % [out, String(spec[0])])
		report.get_or_add("renders", {})[String(spec[0])] = _mean(img)
		print("[terr] %-26s %s" % [String(spec[0]), JSON.stringify(report["renders"][String(spec[0])])])
	terr.material_override = keep
	_write()


func _mean(img: Image) -> Dictionary:
	var n := 0
	var s := Vector3.ZERO
	for y in range(0, img.get_height(), 4):
		for x in range(0, img.get_width(), 4):
			var c := img.get_pixel(x, y)
			s += Vector3(c.r, c.g, c.b)
			n += 1
	return {"mean_srgb": [snappedf(s.x / n, 0.001), snappedf(s.y / n, 0.001),
						  snappedf(s.z / n, 0.001)]}


func _v(v: Vector3) -> Array:
	return [snappedf(v.x, 0.001), snappedf(v.y, 0.001), snappedf(v.z, 0.001)]


func _v2(v: Vector2) -> Array:
	return [snappedf(v.x, 0.1), snappedf(v.y, 0.1)]


func _settle(vp: SubViewport) -> void:
	for i in 6:
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _write() -> void:
	var f := FileAccess.open(out + "/probe_terrain.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[terr] -> %s/probe_terrain.json" % out)
	quit(0)
