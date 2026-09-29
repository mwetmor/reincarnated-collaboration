extends SceneTree
# C-9 T7-A: WHERE DOES THE LIVE 2D PUT ITS PARALLAX LAYERS, on screen, at a given canvas
# point? Measured from the running scene rather than re-derived from Parallax2D's formula
# -- the 3D side has to match what the 2D DOES, and a second derivation of the same rule
# is a second rule that merely resembles the first.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_2d_layers.gd -- --out D
#
# Reports, per spot and per layer, the SCREEN-PIXEL rect of the layer sprite, taken from
# get_global_transform_with_canvas(). Two spots 1000 px apart also give the drift law by
# measurement: d(screen)/d(camera) should come out as (1 - scroll_scale).

const CAM_OFFSET := Vector2(-2, -55)
const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),
	"bridge": Vector2(3459.88, 1027.18),
	"probe_a": Vector2(2285.62, 2407.32),
	"probe_b": Vector2(3285.62, 1407.32),
}
const LAYERS := ["Layer_sky", "Layer_far_ruins", "Layer_forest_valley", "Layer_mist"]

var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize():
	var out := ProjectSettings.globalize_path("user://ref2d")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	for n in ["AnimatedSprite2D", "KnightSprite", "Knight3D", "ContactShadow"]:
		var c = keeper.get_node_or_null(NodePath(n))
		if c != null:
			c.visible = false
	var hud = keeper.get_node_or_null(^"CharacterSkin")
	if hud != null:
		for cl in hud.find_children("*", "CanvasLayer", true, false):
			(cl as CanvasLayer).visible = false
	for i in 20:
		await physics_frame

	var rows := {}
	for name in SPOTS:
		keeper.global_position = SPOTS[name] - CAM_OFFSET
		for i in 12:
			await physics_frame
			await process_frame
		if name in ["plateau", "bridge"]:
			root.get_texture().get_image().save_png("%s/%s_2d.png" % [out, name])
		var ct: Transform2D = root.get_final_transform()
		say("")
		say("== %s  canvas %s   window %s" % [name, str(SPOTS[name]), str(root.get_visible_rect().size)])
		say("   canvas xform origin %s  scale %s" % [str(ct.origin), str(ct.get_scale())])
		var per := {}
		for ln in LAYERS:
			var node = scene.get_node_or_null(NodePath(ln))
			if node == null:
				say("   %-20s MISSING" % ln)
				continue
			var spr := node.get_node_or_null(^"Sprite2D") as Sprite2D
			var t: Transform2D = spr.get_global_transform_with_canvas()
			var sz: Vector2 = spr.texture.get_size() * spr.scale
			say("   %-20s z=%d scroll_scale=%s  screen top-left %s  size %s" %
				[ln, node.z_index, str(node.scroll_scale), str(t.origin), str(sz)])
			per[ln] = {"z": node.z_index, "scroll_scale": node.scroll_scale.x,
					   "screen_tl": [t.origin.x, t.origin.y], "size": [sz.x, sz.y],
					   "node_pos": [node.position.x, node.position.y],
					   "scroll_offset": [node.scroll_offset.x, node.scroll_offset.y]}
		# where a plate pixel lands, for the 1:1 check
		var fg = scene.get_node_or_null(^"Foreground_0")
		if fg != null:
			var tf: Transform2D = (fg as Node2D).get_global_transform_with_canvas()
			say("   %-20s screen top-left %s   (the plate: 1:1 with the canvas)" %
				["Foreground_0", str(tf.origin)])
			per["plate"] = {"screen_tl": [tf.origin.x, tf.origin.y]}
		rows[name] = per

	# the drift law, measured over a 1000 px move
	say("")
	say("== drift, probe_a -> probe_b (camera moved +1000, -1000 canvas px)")
	for ln in LAYERS:
		var a = rows["probe_a"][ln]["screen_tl"]
		var b = rows["probe_b"][ln]["screen_tl"]
		var s: float = rows["probe_a"][ln]["scroll_scale"]
		say("   %-20s d_screen (%+8.2f, %+8.2f)   expected (1-s)*d = (%+8.2f, %+8.2f)" %
			[ln, b[0] - a[0], b[1] - a[1], (1.0 - s) * 1000.0, (1.0 - s) * -1000.0])
	var pa = rows["probe_a"]["plate"]["screen_tl"]
	var pb = rows["probe_b"]["plate"]["screen_tl"]
	say("   %-20s d_screen (%+8.2f, %+8.2f)   expected (-1000, +1000)" %
		["Foreground_0", pb[0] - pa[0], pb[1] - pa[1]])

	var f := FileAccess.open(out + "/layers_2d.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(rows, " "))
	f.close()
	var g := FileAccess.open(out + "/layers_2d.txt", FileAccess.WRITE)
	g.store_string("\n".join(lines) + "\n")
	g.close()
	print("[ref2d] -> ", out)
	quit(0)
