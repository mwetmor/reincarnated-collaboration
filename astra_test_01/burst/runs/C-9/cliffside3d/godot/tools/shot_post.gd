extends SceneTree
# C-9 T7-A: the "in front of a post" stills, at the framing the MEASUREMENT used.
#
# tools/probe_occl.gd found the place where the stand-in takes bridge_post_1 out of sight
# -- 35 px above its anchor, 87.8% of the post covered -- with the camera framing BOTH the
# prop and the body: aim at their midpoint, zoom 1.15. capture.gd framed the post alone at
# zoom 1.9 and the body came back 174 silhouette px out of ~2500, behind the abutment rock
# and out of the story. Same scene, same placement, same depths to the centimetre; only
# the camera differed. So the camera that made the measurement makes the picture.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_post.gd -- --out D
const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const ANCHOR := Vector2(2996.0, 1247.0)
const ASSET := "bridge_post_1"
const STEPS := [200.0, 140.0, 90.0, 35.0, 0.0]
var vp: SubViewport
var sc: Camera3D
var scene

func _initialize():
	var out := ProjectSettings.globalize_path("user://post")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)
	vp = SubViewport.new(); vp.size = SHOT; vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50: await process_frame
	sc = Camera3D.new(); sc.projection = Camera3D.PROJECTION_ORTHOGONAL
	sc.keep_aspect = Camera3D.KEEP_HEIGHT; sc.near = scene.cam.near; sc.far = scene.cam.far
	sc.cull_mask = scene.cam.cull_mask
	vp.add_child(sc); sc.current = true
	var k = scene.knight
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var holder = scene.get_node_or_null(^"Props")
	var card: MeshInstance3D = null
	for c in holder.get_children():
		if (c as MeshInstance3D).name == ASSET: card = c
	var rows := []
	for i in STEPS.size():
		var px: Vector2 = ANCHOR + Vector2(0.0, STEPS[i])
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		if g.is_empty(): continue
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
		k.velocity = Vector3.ZERO
		k.facing = "N"; k.state = "walk"; k.play("c_walk")
		for j in 6:
			await physics_frame
			await process_frame
		scene.look_at_canvas((ANCHOR + px) * 0.5 + Vector2(0, -90), 0.0, 1.15)
		_mirror()
		card.visible = false
		var A := await _grab()
		k.visible = false
		var B := await _grab()
		card.visible = true
		var D := await _grab()
		k.visible = true
		var C := await _grab()
		C.save_png("%s/post_step%d.png" % [out, i])
		var sil := 0; var hid := 0; var psil := 0; var phid := 0
		for y in SHOT.y:
			for x in SHOT.x:
				var qa := A.get_pixel(x, y); var qb := B.get_pixel(x, y)
				var qc := C.get_pixel(x, y); var qd := D.get_pixel(x, y)
				if _ne(qa, qb):
					sil += 1
					if not _ne(qc, qd): hid += 1
				if _ne(qd, qb):
					psil += 1
					if not _ne(qc, qa): phid += 1
		var r := {"step": i, "offset_px": STEPS[i],
				  "canvas_px": [px.x, snappedf(px.y, 0.1)],
				  "knight_depth_m": snappedf(k.global_position.dot(scene.fwd), 0.01),
				  "card_origin_depth_m": snappedf(card.global_position.dot(scene.fwd), 0.01),
				  "silhouette_px": sil, "hidden_by_card_px": hid,
				  "post_px": psil, "post_hidden_by_knight_px": phid,
				  "post_hidden_pct": snappedf(100.0 * float(phid) / maxf(float(psil), 1.0), 0.1)}
		rows.append(r)
		print("  +%3.0f px: he is %6d px, %d hidden by the post | post %5d px, %5d covered (%.1f%%)"
			% [STEPS[i], sil, hid, psil, phid, r["post_hidden_pct"]])
	var f := FileAccess.open(out + "/post.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"asset": ASSET, "anchor_px": [ANCHOR.x, ANCHOR.y],
		"framing": "aim at the midpoint of prop and body, zoom 1.15", "swept": rows}, " "))
	f.close()
	print("[post] -> ", out)
	quit(0)

func _ne(a: Color, b: Color) -> bool:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02

func _mirror() -> void:
	sc.global_transform = scene.cam.global_transform
	sc.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))

func _grab() -> Image:
	for i in 4: await process_frame
	return vp.get_texture().get_image()
