extends SceneTree
# T9-1c: the ortho depth residual against the pinned reference.
#
# The UNDISPLACED build reproduces ortho_canvas_v4_2_depth_mm.png byte-identically -- the
# previous session verified that at 0.0000 mm and 0.0000% mask disagreement. So the residual
# against the reference IS the difference the displacement makes, and it can be measured
# without re-deriving the reference's own encoding: raycast the same canvas grid in both
# builds and difference the hit depths. Run twice, with and without --no-relief.
const PPM := 100.617553710938
const STEP := 8          # canvas pixels between samples
func _initialize():
	var out := ProjectSettings.globalize_path("user://depth.json")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size(): out = args[i + 1]
	var scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60: await process_frame
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var rows := []
	var hits := 0
	for y in range(0, 4096, STEP):
		for x in range(0, 5376, STEP):
			var g := CliffWorld.ground_at(space, Vector2(x, y), scene.right, scene.up, scene.fwd)
			if g.is_empty():
				rows.append(1e9)
			else:
				rows.append((g["position"] as Vector3).dot(scene.fwd))
				hits += 1
	var f := FileAccess.open(out, FileAccess.WRITE)
	f.store_string(JSON.stringify({"step": STEP, "samples": rows.size(), "hits": hits, "depth": rows}))
	f.close()
	print("[depth] %d samples, %d hits -> %s" % [rows.size(), hits, out])
	quit(0)
