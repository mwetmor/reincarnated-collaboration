extends SceneTree
# C-9 T7-A: where does the stand-in RENDER, against where he is PLACED?
# Replicates the capture's own sequence for one step and reports both, so the answer is
# not inferred from a picture at two different scales.
const PPM := 100.617553710938
const AIM := Vector2(2996.0, 1210.0)
const ZOOM := 1.9
const PUT := Vector2(2996.0, 1213.3)
var vp: SubViewport
var sc: Camera3D
var scene
var base: Image

func _initialize():
	vp = SubViewport.new(); vp.size = Vector2i(1920, 1080); vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED; vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	sc = Camera3D.new(); sc.projection = Camera3D.PROJECTION_ORTHOGONAL
	sc.keep_aspect = Camera3D.KEEP_HEIGHT; sc.near = scene.cam.near; sc.far = scene.cam.far
	sc.cull_mask = scene.cam.cull_mask
	vp.add_child(sc); sc.current = true
	var k = scene.knight
	k.set_physics_process(false)
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, PUT, scene.right, scene.up, scene.fwd)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
	k.facing = "N"; k.state = "walk"; k._drive(); k._place_pollaxe()
	scene.look_at_canvas(AIM, 0.0, ZOOM)
	sc.global_transform = scene.cam.global_transform
	sc.size = 1080.0 / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
	for i in 6: await process_frame
	print("window height reported by scene: %d" % scene._view_height())
	print("scene.cam.size %.4f   shot cam size %.4f   (expect %.4f)" %
		[scene.cam.size, sc.size, 1080.0 / PPM / ZOOM])
	print("body global_position %s" % str(k.global_position))
	print("  unproject(body origin)   -> screen %s" % str(sc.unproject_position(k.global_position)))
	var rig = k.get_node_or_null(^"Rig")
	if rig == null:
		for c in k.get_children():
			if c is Node3D and not (c is CollisionShape3D):
				rig = c
				break
	print("  rig node '%s' global_position %s" % [str(rig.name), str((rig as Node3D).global_position)])
	print("  unproject(rig origin)    -> screen %s" % str(sc.unproject_position((rig as Node3D).global_position)))
	# and the pixels
	k.visible = false
	for i in 4: await process_frame
	base = vp.get_texture().get_image()
	k.visible = true
	for i in 4: await process_frame
	var img := vp.get_texture().get_image()
	var x0 := 1 << 20; var y0 := 1 << 20; var x1 := -1; var y1 := -1; var n := 0
	for y in 1080:
		for x in 1920:
			var a := img.get_pixel(x, y); var b := base.get_pixel(x, y)
			if absf(a.r-b.r)+absf(a.g-b.g)+absf(a.b-b.b) > 0.02:
				n += 1; x0 = mini(x0,x); y0 = mini(y0,y); x1 = maxi(x1,x); y1 = maxi(y1,y)
	print("  rendered silhouette bbox screen x %d..%d y %d..%d  (%d px)" % [x0, x1, y0, y1, n])
	print("  its foot centre -> canvas (%.1f, %.1f)   placed at %s" %
		[AIM.x + (float(x0+x1)*0.5 - 960.0)/ZOOM, AIM.y + (float(y1) - 540.0)/ZOOM, str(PUT)])
	quit(0)
