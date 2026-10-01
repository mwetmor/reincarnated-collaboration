extends Node3D
## R-C9-98 probe: does Godot load the body's under_battlemage morph, and does setting it move vertices?
func _ready() -> void:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	var err := doc.append_from_file(OS.get_environment("GS_BODY"), st)
	var who := doc.generate_scene(st); add_child(who)
	for m in who.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null: continue
		var names := []
		for i in mi.get_blend_shape_count(): names.append(String(mi.mesh.get_blend_shape_name(i)))
		print("[probe] mesh ", mi.name, " blend shapes ", names, " skin ", mi.skin != null)
		var am := mi.mesh as ArrayMesh
		if am and am.get_blend_shape_count() > 0:
			var bs := am.surface_get_blend_shape_arrays(0)
			var base: PackedVector3Array = am.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
			for k in bs.size():
				var v: PackedVector3Array = bs[k][Mesh.ARRAY_VERTEX]
				var mx := 0.0; var n := 0
				for i in range(0, v.size(), 7):
					var d := (v[i] - base[i]).length()
					if d > 1e-5: n += 1
					mx = max(mx, d)
				print("[probe] shape ", k, " ", am.get_blend_shape_name(k), " sampled moved ", n, " max ", mx, " (mode ", am.blend_shape_mode, ")")
	get_tree().quit()
