extends SceneTree
# Loads a GLB the way join1_render/scripts/render_cells.gd does (GLTFDocument.append_from_file + generate_scene(st), no
# editor import) and dumps, per named animation, every track's key count, key times and interpolation type.
func _initialize():
	process_frame.connect(_run, CONNECT_ONE_SHOT)

func _run():
	var a := OS.get_cmdline_user_args()
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(a[0], st)
	if err != OK:
		push_error("load failed %d" % err); quit(1); return
	var root: Node = doc.generate_scene(st)
	var aps := root.find_children("*", "AnimationPlayer", true, false)
	var ap: AnimationPlayer = aps[0]
	var res := {"godot": Engine.get_version_info()["string"], "state_bake_fps": st.get("bake_fps"), "anims": {}}
	for nm in a[2].split(","):
		if not ap.has_animation(nm):
			res["anims"][nm] = "missing"; continue
		var an: Animation = ap.get_animation(nm)
		var tr := {}
		for i in an.get_track_count():
			var times := []
			for k in an.track_get_key_count(i):
				times.append(an.track_get_key_time(i, k))
			tr[str(an.track_get_path(i)) + "|" + str(an.track_get_type(i))] = {"times": times, "interp": an.track_get_interpolation_type(i)}
		res["anims"][nm] = {"length": an.length, "tracks": tr}
	var f := FileAccess.open(a[1], FileAccess.WRITE); f.store_string(JSON.stringify(res)); f.close()
	root.free()
	quit(0)
