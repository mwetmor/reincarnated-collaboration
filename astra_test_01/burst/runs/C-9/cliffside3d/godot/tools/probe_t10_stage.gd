extends SceneTree
# Where does shot_barrow_t10 stop? Print between every stage, output to a file, no pipe.
func _initialize() -> void:
	print("[stage] 1 start")
	var root3 := Node3D.new(); root.add_child(root3)
	print("[stage] 2 node added")
	var w := BarrowHeightfield.new("res://data/height_a_authored.png",
								   "res://data/height_a_authored.json")
	print("[stage] 3 heightfield loaded")
	var gm := StandardMaterial3D.new()
	var t0 := Time.get_ticks_msec()
	w.build_terrain(root3, gm)
	print("[stage] 4 terrain built in %d ms" % (Time.get_ticks_msec() - t0))
	var scene = JSON.parse_string(FileAccess.get_file_as_string("res://data/barrow_scene_a.json"))
	print("[stage] 5 scene json: %s" % (scene != null))
	var n := 0
	for inst in scene["instances"]["height_a_authored"]:
		var an := String(inst["asset"])
		var path := ""
		if an == "heather": path = "res://models/barrow/heather.glb"
		elif an == "birch": path = "res://models/barrow/birch_proc.glb"
		elif an == "raven": path = "res://models/barrow/raven.glb"
		if path == "" or not ResourceLoader.exists(path): continue
		var node: Node3D = (load(path) as PackedScene).instantiate()
		root3.add_child(node); n += 1
	print("[stage] 6 placed %d instances" % n)
	var vp := SubViewport.new(); vp.size = Vector2i(1920, 1080); vp.own_world_3d = false
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	print("[stage] 7 viewport added")
	for i in 3: await process_frame
	print("[stage] 8 three frames done")
	quit(0)
