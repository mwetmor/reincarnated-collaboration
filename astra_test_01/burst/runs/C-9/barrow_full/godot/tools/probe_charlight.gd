extends SceneTree
## C-9 R-C9-139 -- HOW BRIGHT IS THE CHARACTER: the painted Barrow at the play camera, the character idle at four headings,
## a BEAUTY frame (as played: the pen, the grade) and a MASK frame (every character ramp mesh unshaded magenta, the post
## pass hidden) so the character's own pixels can be counted apart from the painting. drax.
##   Godot --path godot --resolution 1920x1080 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --fixed-fps 60 --script tools/probe_charlight.gd -- --as-web --c <who> [--charlight a|b|c] [--ref cliff] \
##         --out DIR --tag NAME [--full]
## --ref cliff  THE CLIFFSIDE'S CHARACTER LIGHT on the same pose and camera (cliffside3d world.gd build_lights +
##              cliffside3d.gd _take_over_environment, painted mode): the character's OWN materials back
##              (PaintStack.restore_character), the Barrow sun masked off her layer, a "Sunset" key masked to CHAR_LAYER
##              (energy 1.15, colour 1.0/0.76/0.52, from screen-left low: d_local 0.92/-0.34/0.18 in the camera's yaw
##              frame, no shadow) and the ambient 1.0/0.93/0.86 x 0.40. The painting around her is irrelevant here.
## --full       also save the whole 1920x1080 beauty frame (for the outside-the-silhouette world diff)
## Writes DIR/<tag>_<who>_h<H>_beauty.png, _mask.png (600 x 600 around her), DIR/<tag>_<who>.json.

const SPOT := Vector2(-1.0, -0.5)
const HEADINGS := ["S", "E", "N", "W"]
const CHAR_LAYER := 4


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := String(args[args.find("--out") + 1])
	var tag := String(args[args.find("--tag") + 1]) if args.has("--tag") else "cur"
	var ref := String(args[args.find("--ref") + 1]) if args.has("--ref") else ""
	var full := args.has("--full")
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
	if scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
		scene.snowfall.emitting = false
	var k = scene.knight
	var rep := {"who": scene.who, "slot": scene.slot, "tag": tag, "ref": ref, "charlight": scene.charlight,
		"renderer": RenderingServer.get_current_rendering_method(), "spot_uv": [SPOT.x, SPOT.y], "headings": {}}
	if ref == "cliff":
		rep["ref_rig"] = _cliff_rig(scene)
	scene.place_knight(SPOT.x, SPOT.y, "S")
	var who := String(scene.who)
	var dirs := {"S": Vector2(0, 1), "E": Vector2(1, 0), "N": Vector2(0, -1), "W": Vector2(-1, 0)}
	for h in HEADINGS:
		# TURNED BY WALKING: a tool setting `facing` at rest does not turn the rig here (the yaw reads the last
		# travel direction), so she takes a few steps toward the heading, stops, and is put back on the spot
		for f in 12:
			k.drive_dir(dirs[h], false, 1.0 / 60.0)
			await physics_frame
		for f in 60:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
			await physics_frame
		scene.place_knight(SPOT.x, SPOT.y, h)
		for f in 40:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
			await physics_frame
		var sp: Vector2 = scene.cam.unproject_position(k.global_position + Vector3(0, 1.0, 0))
		var w := root.get_texture().get_width() if root.get_texture() != null else 1920
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var x := clampi(int(sp.x) - 300, 0, img.get_width() - 600)
		var y := clampi(int(sp.y) - 330, 0, img.get_height() - 600)
		var base := out_dir.path_join("%s_%s_h%s" % [tag, who, h])
		img.get_region(Rect2i(x, y, 600, 600)).save_png(base + "_beauty.png")
		if full:
			img.save_png(base + "_full.png")
		# THE MASK: the character's ramp meshes (and their restored originals) unshaded magenta, the pen hidden
		var keep := {}
		for ent in scene._char_saved.get("meshes", []):
			var mi: MeshInstance3D = ent["mi"]
			keep[mi] = mi.material_override
			var m := StandardMaterial3D.new()
			m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			m.albedo_color = Color(1, 0, 1)
			mi.material_override = m
		var post_vis: bool = scene.post_q.visible
		scene.post_q.visible = false
		for f in 3:
			await process_frame
		await RenderingServer.frame_post_draw
		var mimg := root.get_texture().get_image()
		mimg.get_region(Rect2i(x, y, 600, 600)).save_png(base + "_mask.png")
		if full:
			mimg.save_png(base + "_fullmask.png")
		for mi in keep:
			(mi as MeshInstance3D).material_override = keep[mi]
		scene.post_q.visible = post_vis
		for f in 3:
			await process_frame
		rep["headings"][h] = {"crop": [x, y, 600, 600]}
	var f2 := FileAccess.open(out_dir.path_join("%s_%s.json" % [tag, who]), FileAccess.WRITE)
	f2.store_string(JSON.stringify(rep, " "))
	f2.close()
	print("[charlight-probe] ", JSON.stringify({"who": who, "tag": tag, "ref": ref, "charlight": scene.charlight}))
	quit(0)


func _cliff_rig(scene) -> Dictionary:
	PaintStack.restore_character(scene._char_saved)
	# restore_character puts the meshes back on their OWN materials; the probe's mask swap reads the "ramp" entry's
	# mi only, and reapplies whatever material_override it found -- so the restored originals survive the mask pass
	scene.sun.light_cull_mask &= ~CHAR_LAYER
	scene.paint_sun.light_cull_mask &= ~CHAR_LAYER
	var key := DirectionalLight3D.new()
	key.name = "CliffSunset"
	key.light_energy = 1.15
	key.light_color = Color(1.0, 0.76, 0.52)
	key.light_cull_mask = CHAR_LAYER
	key.shadow_enabled = false
	scene.add_child(key)
	var b: Basis = scene.cam.global_basis
	var right := Vector3(b.x.x, 0, b.x.z).normalized()
	var back := Vector3(b.z.x, 0, b.z.z).normalized()
	var d := (right * 0.92 + Vector3.UP * -0.34 + back * 0.18).normalized()
	key.look_at_from_position(Vector3.ZERO, d, Vector3.UP)
	var env: Environment = scene.env_node.environment
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1.0, 0.93, 0.86)
	env.ambient_light_energy = 0.40
	return {"key": "energy 1.15 colour (1.0, 0.76, 0.52) cull CHAR_LAYER no shadow", "dir": [d.x, d.y, d.z],
		"ambient": "(1.0, 0.93, 0.86) x 0.40", "materials": "the character's own (PaintStack.restore_character)"}
