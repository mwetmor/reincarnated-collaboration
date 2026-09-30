extends SceneTree
# THE IMPORT BAKE, both paths (T12_11: the slash's file fidelity). After nb_join/film/j_fps_probe.gd (the JOIN lane's
# instrument, copied here so nothing in that lane is written): the RUNTIME path (GLTFDocument.append_from_file +
# generate_scene, GLTFState.bake_fps) and the EDITOR import (load() of the imported res:// GLB, animation/fps) --
# per named animation, every rotation track's key times AND VALUES as Godot holds them, for the offline comparison
# with the GLB's own curve.
#   godot --headless --path <lab> --script tools/bake_probe.gd -- <abs glb> <res:// glb> <out.json> <clip,clip>
func _initialize():
	process_frame.connect(_run, CONNECT_ONE_SHOT)

func _dump(ap: AnimationPlayer, clips: PackedStringArray) -> Dictionary:
	var out := {}
	for nm in clips:
		if not ap.has_animation(nm):
			out[nm] = "missing"; continue
		var an: Animation = ap.get_animation(nm)
		var tr := {}
		for i in an.get_track_count():
			if an.track_get_type(i) != Animation.TYPE_ROTATION_3D:
				continue
			var times := []; var vals := []
			for k in an.track_get_key_count(i):
				times.append(an.track_get_key_time(i, k))
				var q: Quaternion = an.track_get_key_value(i, k)
				vals.append([q.x, q.y, q.z, q.w])
			tr[String(an.track_get_path(i).get_concatenated_subnames())] = {"times": times, "vals": vals, "interp": an.track_get_interpolation_type(i)}
		out[nm] = {"length": an.length, "tracks": tr}
	return out

func _run():
	var a := OS.get_cmdline_user_args()
	var clips: PackedStringArray = a[3].split(",")
	var res := {"godot": Engine.get_version_info()["string"]}
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(a[0], st)
	if err != OK:
		push_error("load failed %d" % err); quit(1); return
	var root: Node = doc.generate_scene(st)
	res["runtime_bake_fps"] = st.get("bake_fps")
	res["runtime"] = _dump(root.find_children("*", "AnimationPlayer", true, false)[0], clips)
	root.free()
	var ps: PackedScene = load(a[1])
	var inst: Node = ps.instantiate()
	res["editor"] = _dump(inst.find_children("*", "AnimationPlayer", true, false)[0], clips)
	inst.free()
	var f := FileAccess.open(a[2], FileAccess.WRITE); f.store_string(JSON.stringify(res)); f.close()
	quit(0)
