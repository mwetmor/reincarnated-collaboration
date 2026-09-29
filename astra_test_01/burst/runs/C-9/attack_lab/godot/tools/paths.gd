extends SceneTree
func _initialize() -> void:
	create_timer(120.0).timeout.connect(func(): quit(4))
	for p in ["res://models/gear/nb-body.glb", "res://models/axe_breathe.glb"]:
		var ps := ResourceLoader.load(p, "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
		var r := ps.instantiate()
		root.add_child(r)
		await process_frame
		for n in r.find_children("*", "AnimationPlayer", true, false):
			var ap := n as AnimationPlayer
			var nm: String = String(ap.get_animation_list()[0])
			var a := ap.get_animation(nm)
			var kinds := {}
			for i in a.get_track_count():
				kinds[a.track_get_type(i)] = int(kinds.get(a.track_get_type(i), 0)) + 1
			print("%s | player root '%s' | clip '%s' | track0 '%s' | types %s | fps-ish %.1f"
				% [p.get_file(), str(ap.root_node), nm, str(a.track_get_path(0)), str(kinds),
				   float(a.track_get_key_count(0) - 1) / maxf(a.length, 1e-6)])
	quit(0)
