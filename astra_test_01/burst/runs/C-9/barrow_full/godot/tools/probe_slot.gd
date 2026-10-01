extends SceneTree
## C-9 R-C9-117 -- ONE SLOT, PROVED: the painted Barrow launched with the select page's params, the character stood,
## walked, and both strikes thrown, stills at the play camera. drax.
##   Godot --path godot --resolution 1920x1080 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --fixed-fps 60 --script tools/probe_slot.gd -- --as-web --c <who> [--armor X] [--hold X] [--fb c75] \
##         [--meteor mix4] [--fall 2.4] --out DIR
## Writes DIR/stand.png, walk.png, attack.png (the SLASH strike at 0.55 of its clip), chop.png, and DIR/slot.json:
## the slot, its model, gear stack, the clips the tree plays, whether the tree is valid and any script error.


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := String(args[args.find("--out") + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	for f in 30:
		await process_frame
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	var k = scene.knight
	scene.place_knight(-1.0, -0.5, "S")
	k.facing = "S"
	for f in 40:
		await physics_frame
	var rep := {"who": scene.who, "slot": scene.slot, "slot_report": scene.slot_report,
		"model": String(k.cfg.get("model", "?")), "gear_stack": k.gear_stack, "gear_stacks": k.gear_stack_count(),
		"armed": k.armed(), "roles": k._roles, "character": scene.report.get("character", {})}
	await _shot(scene, out_dir.path_join("stand.png"))
	if args.has("--portrait"):
		# the select page's card: the play camera's own angle and light, zoomed 3x on the character (park_camera)
		scene.park_camera(k.global_position + Vector3(0, 1.0, 0), 3.2)
		for f in 4:
			await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var w := img.get_width()
		var h := img.get_height()
		img.get_region(Rect2i(w / 2 - 330, h / 2 - 440, 660, 880)).save_png(out_dir.path_join("portrait.png"))
		scene.unpark_camera()
		for f in 6:
			await process_frame
		if args.has("--portrait-only"):
			quit(0)
			return
	for f in 40:
		k.drive_dir(Vector2(1, 0.3).normalized(), false, 1.0 / 60.0)
		await physics_frame
	await _shot(scene, out_dir.path_join("walk.png"))
	for f in 30:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
		await physics_frame
	for which in ["attack", "chop"]:
		var role := "attack" if which == "attack" else "chop"
		var ok: bool = k.try_strike("slash" if which == "attack" else "chop")
		rep["strike_" + which] = ok
		for f in 36:
			await physics_frame
		await _shot(scene, out_dir.path_join(which + ".png"))
		for f in 260:
			await physics_frame
	var bt = k._tree.tree_root if k._tree != null else null
	var bad := []
	if bt != null:
		for nm in bt.get_node_list():
			var n = bt.get_node(nm)
			if n is AnimationNodeAnimation and not k._anim.has_animation((n as AnimationNodeAnimation).animation):
				bad.append(String(nm))
	rep["tree_bad_nodes"] = bad
	rep["clips"] = Array(k._anim.get_animation_list()) if k._anim != null else []
	var f2 := FileAccess.open(out_dir.path_join("slot.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify(rep, " "))
	f2.close()
	print("[slot] ", JSON.stringify({"who": rep["who"], "slot": rep["slot"], "model": rep["model"], "armed": rep["armed"],
		"strikes": [rep.get("strike_attack"), rep.get("strike_chop")], "tree_bad": bad.size()}))
	quit(0)


func _shot(scene, path: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	var sp: Vector2 = scene.cam.unproject_position(scene.knight.global_position + Vector3(0, 1.0, 0))
	var x := clampi(int(sp.x) - 300, 0, img.get_width() - 600)
	var y := clampi(int(sp.y) - 330, 0, img.get_height() - 600)
	img.get_region(Rect2i(x, y, 600, 600)).save_png(path)
