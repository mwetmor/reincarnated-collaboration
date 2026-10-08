extends SceneTree
## BV2F PT (R-C9-254) -- which heather sprays and reed cards the play camera SEES at a P10 view (PH's ph_life.gd perf
## loop: the four points around <view>), read-only on the scene. No images.
##   Godot --path . --resolution 1920x1080 --script res://tools/bv2f/pt_view_census.gd -- <scene> <OUT> uv:<u>,<v>
var scene
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	scene = (load(a[0]) as PackedScene).instantiate()
	root.add_child(scene)
	_run(a[1], a[2])

func _run(out: String, view: String) -> void:
	var w := 0
	while not scene.ready_done and w < 4000:
		await process_frame
		w += 1
	var p := view.substr(3).split(",")
	var c: Vector2 = scene.world_to_uv(scene.uv_to_world(float(p[0]), float(p[1])))
	var loop := [c + Vector2(4.0, 1.0), c + Vector2(0.0, 5.0), c + Vector2(-4.0, 1.0), c + Vector2(0.0, -3.0)]
	var rep := {"view": view, "points": []}
	for q in loop:
		scene.place_knight(q.x, q.y, "N")
		for i in 10:
			await process_frame
		var cam: Camera3D = root.get_viewport().get_camera_3d()
		var tot := 0
		var seen := 0
		var mmis := 0
		var mmis_seen := 0
		for mmi in scene._heather_mmi:
			var mm: MultiMesh = (mmi as MultiMeshInstance3D).multimesh
			mmis += 1
			var any := false
			for k in mm.instance_count:
				tot += 1
				if cam.is_position_in_frustum((mmi as Node3D).global_transform * mm.get_instance_transform(k).origin):
					seen += 1
					any = true
			if any:
				mmis_seen += 1
		var st = scene.get("stair_snow")
		var stair_seen := false
		var stair_quads := 0
		if st != null:
			var ar: Rect2 = st.area
			for corner in [ar.position, ar.position + Vector2(ar.size.x, 0), ar.end, ar.position + Vector2(0, ar.size.y), ar.get_center()]:
				if cam.is_position_in_frustum(Vector3(corner.x, 0.0, corner.y)):
					stair_seen = true
			stair_quads = int(round(ar.size.x / st.grid_quad_m)) * int(round(ar.size.y / st.grid_quad_m))
		var kp: Vector3 = scene.knight.global_position
		(rep["points"] as Array).append({"uv": [q.x, q.y], "knight_xz": [kp.x, kp.z], "heather_total": tot, "heather_in_frustum": seen,
			"heather_multimeshes": mmis, "heather_multimeshes_in_frustum": mmis_seen, "stair_in_view": stair_seen,
			"stair_quads": stair_quads, "knight_on_stair_area": st != null and (st.area as Rect2).has_point(Vector2(kp.x, kp.z))})
	var f := FileAccess.open(out.path_join("census.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[census] ", JSON.stringify(rep))
	quit(0)
