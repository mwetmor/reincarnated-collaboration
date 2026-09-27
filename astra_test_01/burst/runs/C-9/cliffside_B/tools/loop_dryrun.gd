extends SceneTree
# C-9: headless dry run for the walk-loop video.  Walks the same closed octagon the
# recorder walks, from each candidate start, and reports the drift between the start
# and the end.  A closed octagon (E SE S SW W NW N NE, equal legs) returns to its own
# start EXACTLY unless collision ate part of a leg -- so drift IS the collision check,
# and it costs one headless run instead of a wasted 12 s capture.
#   LOOP_STARTS="x,y;x,y;..."   LOOP_SECONDS=<per leg>

const LEGS := [
	["move_right"], ["move_right", "move_down"], ["move_down"], ["move_left", "move_down"],
	["move_left"], ["move_left", "move_up"], ["move_up"], ["move_right", "move_up"],
]


func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var per := 1.25
	if OS.get_environment("LOOP_SECONDS") != "":
		per = float(OS.get_environment("LOOP_SECONDS"))
	var frames := int(round(per * 60.0))     # physics ticks per leg
	var starts := OS.get_environment("LOOP_STARTS")
	if starts == "":
		starts = "2400,2200;2200,2300;1900,2400;2600,2000"
	print("leg %.2f s = %d physics frames, %.0f px at walk_px_s" % [per, frames, per * 247.0])
	for s in starts.split(";"):
		var xy := s.split(",")
		var start := Vector2(float(xy[0]), float(xy[1]))
		keeper.velocity = Vector2.ZERO
		keeper.global_position = start
		await physics_frame
		var placed: Vector2 = keeper.global_position
		var minp: Vector2 = placed
		var maxp: Vector2 = placed
		for leg in LEGS:
			for a in leg:
				Input.action_press(a)
			for f in frames:
				await physics_frame
				minp = Vector2(minf(minp.x, keeper.global_position.x), minf(minp.y, keeper.global_position.y))
				maxp = Vector2(maxf(maxp.x, keeper.global_position.x), maxf(maxp.y, keeper.global_position.y))
			for a in leg:
				Input.action_release(a)
			await physics_frame
		var drift = placed.distance_to(keeper.global_position)
		print("  start %-14s placed %-20s end %-20s DRIFT %7.2f px   bbox %.0fx%.0f"
			% [s, str(placed), str(keeper.global_position), drift, maxp.x - minp.x, maxp.y - minp.y])
	quit()
