extends SceneTree
# C-9 T9-1a: NORMALISE EACH PROP MODEL'S YAW BY MEASURING IT AGAINST THE PAINTING.
#
# The generator delivers models yawed, and "yawed 90 degrees" is a fact about the T6
# bake-off's outputs, not a promise about these five. A prop at the wrong yaw renders
# perfectly and is simply facing the wrong way: invisible on a square post, invisible on a
# coil of rope, and the whole bird on a raven.
#
# The yaw is measured THROUGH THE GAME CAMERA'S OWN BASIS and compared against the PAINTED
# SPRITE, because the sprite is what the guide camera saw of that prop standing in that
# place -- it is the ground truth for "how this thing looks from here", and it needs no
# algebra relating a turntable's axes to the cliff's. Getting that algebra wrong is exactly
# the kind of mistake that renders cleanly.
#
# Orthographic and unshaded: this measures a SHAPE, and a shaded render would put the
# renderer's light into the comparison.
#
#   Godot --path godot --resolution 512x512 --script tools/probe_props3d.gd -- --out DIR [--step 15]

const S := Vector2i(512, 512)

var out_dir := ""
var step := 15
var report := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--step" and i + 1 < args.size():
			step = int(args[i + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)

	# The cliff camera's basis. These are CONSTANTS of the v4 frame -- cliffside3d.gd prints
	# them in its build report on every run, under "basis" -- and they are taken as
	# constants rather than by standing up the builder, which needs a --layout this probe
	# has no business supplying just to read three vectors off it.
	var right := Vector3(0.681998491287231, 0.0, -0.731353580951691)
	var up := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
	var fwd := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
	report["basis"] = {"right": [right.x, right.y, right.z], "up": [up.x, up.y, up.z],
					   "fwd": [fwd.x, fwd.y, fwd.z],
					   "_source": "cliffside3d.gd build report; v4 frame constants"}

	var vp := SubViewport.new()
	vp.size = S
	vp.own_world_3d = true
	vp.transparent_bg = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = 0.01
	cam.far = 200.0
	vp.add_child(cam)
	cam.current = true

	var dir := DirAccess.open("res://models/props")
	var names := []
	if dir != null:
		for f in dir.get_files():
			if f.ends_with(".glb"):
				names.append(f.get_basename())
	names.sort()
	report["models"] = {}

	for nm in names:
		var node: Node3D = (load("res://models/props/%s.glb" % nm) as PackedScene).instantiate()
		var pivot := Node3D.new()
		vp.add_child(pivot)
		pivot.add_child(node)
		await process_frame
		await process_frame
		var ab0 := _aabb(pivot)
		report["models"][nm] = {
			"raw_aabb_m": [snappedf(ab0.size.x, 0.0001), snappedf(ab0.size.y, 0.0001),
						   snappedf(ab0.size.z, 0.0001)],
			"meshes": node.find_children("*", "MeshInstance3D", true, false).size(),
			"tris": _tris(node), "step_deg": step}
		# centre the model on the pivot so a yaw turns it in place
		node.position = -ab0.get_center()
		for m in node.find_children("*", "MeshInstance3D", true, false):
			var mat := StandardMaterial3D.new()
			mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			mat.albedo_color = Color(0, 0, 0)
			(m as MeshInstance3D).material_override = mat
		var r: float = maxf(maxf(ab0.size.x, ab0.size.y), ab0.size.z)
		cam.size = r * 1.35
		cam.global_transform = Transform3D(Basis(right, up, -fwd), fwd * -r * 4.0)
		var y := 0
		while y < 360:
			pivot.rotation = Vector3(0.0, deg_to_rad(float(y)), 0.0)
			for i in 3:
				await process_frame
			vp.get_texture().get_image().save_png("%s/%s_yaw%03d.png" % [out_dir, nm, y])
			y += step
		pivot.queue_free()
		await process_frame
		print("[props3d] %s %s" % [nm, JSON.stringify(report["models"][nm])])

	var f := FileAccess.open(out_dir + "/props3d_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	quit(0)


func _tris(n: Node3D) -> int:
	var t := 0
	for m in n.find_children("*", "MeshInstance3D", true, false):
		var mesh := (m as MeshInstance3D).mesh
		if mesh == null:
			continue
		for s in mesh.get_surface_count():
			var arr := mesh.surface_get_arrays(s)
			var idx = arr[Mesh.ARRAY_INDEX]
			if idx != null:
				t += idx.size() / 3
			else:
				t += (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size() / 3
	return t


func _aabb(n: Node3D) -> AABB:
	var out := AABB()
	var first := true
	for m in n.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var ab: AABB = mi.global_transform * mi.get_aabb()
		out = ab if first else out.merge(ab)
		first = false
	return out
