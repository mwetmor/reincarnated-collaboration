extends SceneTree
func _initialize():
	print("before: Engine.physics_ticks_per_second = %d" % Engine.physics_ticks_per_second)
	Engine.physics_ticks_per_second = 24
	print("after : Engine.physics_ticks_per_second = %d" % Engine.physics_ticks_per_second)
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 40: await process_frame
	var k = scene.knight
	print("knight get_physics_process_delta_time() = %.6f  (1/%.1f)" %
		[k.get_physics_process_delta_time(), 1.0 / k.get_physics_process_delta_time()])
	print("Engine now = %d" % Engine.physics_ticks_per_second)
	# and how far does one tick actually move him?
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var g := CliffWorld.ground_at(space, Vector2(1666.0, 2705.0), scene.right, scene.up, scene.fwd)
	k.set_physics_process(false)
	k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
	k.velocity = Vector3.ZERO
	for i in 6: await physics_frame
	var a := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	for i in 24:
		k.drive_dir(Vector2(1, 0), false, 1.0 / 24.0)
		await physics_frame
	var b := CliffWorld.canvas_of(k.global_position, scene.right, scene.up)
	print("24 drive_dir calls moved him %.1f canvas px  (one second at 201.7 px/s would be 201.7)"
		% (b - a).length())
	quit(0)
