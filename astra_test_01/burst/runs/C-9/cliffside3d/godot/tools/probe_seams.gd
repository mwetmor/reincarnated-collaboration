extends SceneTree
# C-9 T10 — OPEN EDGES IN THE BARROW GLBs, AS THEY ARE LOADED BY THE SCENE.
#
# The kit drax measured T-junction cracks along the UV seams (39_reduce.py decimated each UV
# island separately) and welded re-reductions are coming. This is the BEFORE, taken through
# the same definition so the after is comparable: weld vertices by POSITION, then count edges
# used by exactly one triangle. A closed solid has about zero; a shell split along its seams
# has one open edge per seam segment, twice.
#
# MEASURED ON THE IMPORTED MESH, not on the .glb file, because that is what renders. Godot's
# GLTF importer can itself split vertices (by normal, by UV), so a count taken off the file
# would be about the file and not about the thing on screen.
#
# The weld tolerance is 1e-5 m and it is stated because it IS the measurement: too loose and
# a genuine 0.1 mm gap welds shut and the count comes back clean; too tight and float noise
# from the exporter splits every shared vertex and everything reads as cracked.
#
#   Godot --headless --path godot --script tools/probe_seams.gd -- --out DIR

const WELD := 1e-5


func _initialize() -> void:
	var out_dir := ""
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("user://seams")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var rep := {"_defn": {
		"weld_tolerance_m": WELD,
		"open_edge": "an edge used by exactly ONE triangle after welding vertices by position",
		"_a_clean_solid": "about 200 (the kit drax's figure for a clean build)",
		"measured_on": "the IMPORTED mesh, which is what renders -- not the .glb file",
	}, "models": {}}
	for nm in ["stone_tall", "stone_mid", "stone_short", "lintel", "post",
			   "rock_large", "rock_small", "birch", "juniper", "heather", "raven"]:
		var path := "res://models/barrow/%s.glb" % nm
		if not ResourceLoader.exists(path):
			rep["models"][nm] = {"_": "not in the project"}
			continue
		var inst := (load(path) as PackedScene).instantiate()
		var tris := 0
		var open := 0
		var edges := 0
		for n in inst.find_children("*", "MeshInstance3D", true, false):
			var mi := n as MeshInstance3D
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				var arr := mi.mesh.surface_get_arrays(s)
				var v: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
				var ix = arr[Mesh.ARRAY_INDEX]
				if ix == null:
					continue
				# weld: quantise to the tolerance and key on the grid cell, so two vertices
				# that are the same point to within WELD land on the same id
				var ids := PackedInt32Array()
				ids.resize(v.size())
				var map := {}
				for i in v.size():
					var key := "%d|%d|%d" % [int(round(v[i].x / WELD)), int(round(v[i].y / WELD)),
											 int(round(v[i].z / WELD))]
					if not map.has(key):
						map[key] = map.size()
					ids[i] = int(map[key])
				var use := {}
				for t in range(0, ix.size(), 3):
					tris += 1
					for e in 3:
						var a: int = ids[ix[t + e]]
						var b: int = ids[ix[t + (e + 1) % 3]]
						var ek := "%d_%d" % [mini(a, b), maxi(a, b)]
						use[ek] = int(use.get(ek, 0)) + 1
				for ek in use:
					edges += 1
					if int(use[ek]) == 1:
						open += 1
		rep["models"][nm] = {"triangles": tris, "edges_after_weld": edges, "open_edges": open,
							 "open_share": snappedf(float(open) / maxf(float(edges), 1.0), 0.0001)}
		inst.queue_free()
	var f := FileAccess.open(out_dir + "/seams.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	var line := []
	for nm in rep["models"]:
		line.append("%s=%s" % [nm, rep["models"][nm].get("open_edges", "?")])
	print("[seams] open edges: %s" % ", ".join(line))
	quit(0)
