extends SceneTree
# Conductor capture tool: cast one kit east in the real scene headless and dump every G1 event log + target/layer facts.
var cycles = int(OS.get_environment("KIT_CYCLES"))
func _init():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	keeper.global_position = Vector2(3760, 640)
	keeper.vfx_force_touch_device = true
	for i in cycles:
		Input.action_press("vfx_cycle"); await physics_frame; Input.action_release("vfx_cycle"); await physics_frame; await physics_frame
	Input.action_press("move_right"); await physics_frame; await physics_frame; Input.action_release("move_right")
	for f in 12: await physics_frame
	Input.action_press("cast"); await physics_frame; Input.action_release("cast")
	var logs = []
	for f in 110:
		await physics_frame
		for n in _all(root):
			if "events" in n and n.get("events") is Array and not logs.has(n): logs.append(n)
	var out = {"targets": [], "walls": null, "effects": []}
	for t in get_nodes_in_group("vfx_targets"): out.targets.append({"name": t.name, "layer": t.get("collision_layer"), "pos": [t.global_position.x, t.global_position.y]})
	var walls = scene.find_child("Walls", true, false)
	if walls: out.walls = {"class": walls.get_class(), "layer": walls.get("collision_layer"), "children": walls.get_child_count()}
	for n in logs:
		var ev = []
		for e in n.get("events"): ev.append(e)
		out.effects.append({"node": n.name, "script": str(n.get_script().resource_path) if n.get_script() else "", "pos": [n.global_position.x, n.global_position.y] if n is Node2D else null, "events": ev})
	print("PROBE_EVENTS=" + JSON.stringify(out))
	quit()
func _all(n: Node) -> Array:
	var acc = [n]
	for c in n.get_children(): acc += _all(c)
	return acc
