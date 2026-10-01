extends SceneTree
## C-9 R-C9-118 -- where things are: the ground basis, every placement's world bounds and class, for choosing impact
## spots (snow, ice, earth, a standing stone, a plant clump). drax.  -> DIR/spots.json
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out := String(args[args.find("--out") + 1])
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var pl := []
	for e in scene.layout["placements"]:
		var id := String(e["id"])
		if not scene.nodes.has(id):
			continue
		var n: Node3D = scene.nodes[id]
		var b: AABB = scene._node_aabb(n)
		var wb: AABB = n.global_transform * b
		pl.append({"id": id, "class": String(e.get("class", "")), "kind": String(e["kind"]), "pos": [wb.get_center().x, wb.position.y, wb.get_center().z],
			"size": [wb.size.x, wb.size.y, wb.size.z]})
	var f := FileAccess.open(out, FileAccess.WRITE)
	f.store_string(JSON.stringify({"u_hat": [scene.u_hat.x, scene.u_hat.y, scene.u_hat.z], "v_hat": [scene.v_hat.x, scene.v_hat.y, scene.v_hat.z],
		"placements": pl, "spawn": [scene.knight.global_position.x, scene.knight.global_position.z]}, " "))
	f.close()
	print("[spots] ", pl.size())
	quit(0)
