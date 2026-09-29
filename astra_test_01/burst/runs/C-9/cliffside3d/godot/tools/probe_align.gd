extends SceneTree
# C-9 T7-A: does a prop card land where props.json says it lands, on screen?
#
# The "in front of a post" sweep put the stand-in at the post's own anchor x and the
# pictures show them side by side, not overlapping. Either the card is off, or the body
# is, or both are right and the eye is reading a different post. unproject_position turns
# each into a screen pixel and canvas coordinates turn that back into the frame
# props.json is written in, so the three can be compared as numbers.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_align.gd

const PPM := 100.617553710938
const V4_UMIN := -23.2673988342285
const V4_VMAX := 18.5067100524902
const PROBE := ["bridge_post_1", "bridge_post_0", "tree_living_a", "stump_a", "rock_a"]


func _initialize() -> void:
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	var right: Vector3 = scene.right
	var up: Vector3 = scene.up
	var data = JSON.parse_string(FileAccess.get_file_as_string("res://props/props.json"))
	var assets := {}
	for a in data["assets"]:
		assets[String(a["name"])] = a
	var want := {}
	for inst in data["instances"]:
		want[String(inst["asset"])] = Vector2(float(inst["position"][0]), float(inst["position"][1]))
	var props = scene.get_node_or_null(^"Props")

	print("%-22s %-20s %-20s %-20s" % ["prop", "anchor (props.json)", "card centre -> canvas",
		 "expected centre"])
	for n in PROBE:
		var card: MeshInstance3D = null
		for c in props.get_children():
			if (c as MeshInstance3D).name == n:
				card = c
				break
		if card == null:
			continue
		var a = assets[n]
		var anc := Vector2(float(a["anchor"][0]), float(a["anchor"][1]))
		var tex: Texture2D = load("res://props/" + String(a["file"]))
		var w := float(tex.get_width())
		var h := float(tex.get_height())
		var got := _canvas_of(card.global_position, right, up)
		# where the sprite's centre sits on the canvas in the 2D: anchor - anchor_offset + size/2
		var expect: Vector2 = (want[n] as Vector2) - anc + Vector2(w, h) * 0.5
		print("%-22s %-20s %-20s %-20s   tex %dx%d anc %s  dx %+.1f" %
			[n, str(want[n]), "(%.1f, %.1f)" % [got.x, got.y],
			 "(%.1f, %.1f)" % [expect.x, expect.y], int(w), int(h), str(anc), got.x - expect.x])

	# and the stand-in, at the post's own anchor x
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var k = scene.knight
	k.set_physics_process(false)
	var px := Vector2(2996.0, 1213.3)
	var g := CliffWorld.ground_at(space, px, right, up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	await process_frame
	var kc := _canvas_of(k.global_position, right, up)
	print("")
	print("stand-in placed at canvas %s  ->  origin lands at canvas (%.1f, %.1f)" % [str(px), kc.x, kc.y])

	# WHERE HIS PIXELS ARE, which is not the same question as where his origin is. A GLB
	# whose mesh is not centred on its own origin puts the body somewhere the placement
	# code never named -- and the "in front of a post" sweep put him at the post's exact
	# canvas x and measured 0% of the post covered.
	var vp := SubViewport.new()
	vp.size = Vector2i(1920, 1080)
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var sc := Camera3D.new()
	sc.projection = Camera3D.PROJECTION_ORTHOGONAL
	sc.keep_aspect = Camera3D.KEEP_HEIGHT
	sc.near = scene.cam.near
	sc.far = scene.cam.far
	sc.cull_mask = scene.cam.cull_mask
	vp.add_child(sc)
	sc.current = true
	scene.look_at_canvas(Vector2(2996.0, 1210.0), 0.0, 1.9)
	sc.global_transform = scene.cam.global_transform
	sc.size = 1080.0 / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
	var holder = scene.get_node_or_null(^"Props")
	var post: MeshInstance3D = null
	for c in holder.get_children():
		if (c as MeshInstance3D).name == "bridge_post_1":
			post = c
	for pass_i in 3:
		k.visible = (pass_i == 1)
		post.visible = (pass_i == 2)
		if pass_i != 2:
			post.visible = false
		for i in 5:
			await process_frame
		if pass_i == 0:
			_base = vp.get_texture().get_image()
		else:
			var img := vp.get_texture().get_image()
			var x0 := 1 << 20
			var y0 := 1 << 20
			var x1 := -1
			var y1 := -1
			var n := 0
			for y in 1080:
				for x in 1920:
					var a := img.get_pixel(x, y)
					var b := _base.get_pixel(x, y)
					if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02:
						n += 1
						x0 = mini(x0, x); y0 = mini(y0, y)
						x1 = maxi(x1, x); y1 = maxi(y1, y)
			# screen -> canvas: at the game camera the two are 1:1 about the aim
			var aim := Vector2(2996.0, 1210.0)
			var z := 1.9
			var who := "stand-in" if pass_i == 1 else "bridge_post_1"
			print("%-14s screen bbox x %d..%d  y %d..%d  (%d px)   canvas x %.0f..%.0f  y %.0f..%.0f" %
				[who, x0, x1, y0, y1, n,
				 aim.x + (float(x0) - 960.0) / z, aim.x + (float(x1) - 960.0) / z,
				 aim.y + (float(y0) - 540.0) / z, aim.y + (float(y1) - 540.0) / z])
	quit(0)


var _base: Image


func _canvas_of(w: Vector3, right: Vector3, up: Vector3) -> Vector2:
	return Vector2((w.dot(right) - V4_UMIN) * PPM, (V4_VMAX - w.dot(up)) * PPM)


# appended: where does the BODY actually land on screen, against where it is placed?
