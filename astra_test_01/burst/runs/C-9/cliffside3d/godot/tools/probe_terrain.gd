extends SceneTree
# C-9 T10: is BarrowHeightfield.build_terrain wound the right way round?
#
# The render-stack drax reports that [k, k+n+1, k+n+2, k, k+n+2, k+1] gives +Y right-hand
# normals -- the back-facing order that made its own terrain invisible. Checked rather than
# taken: build the mesh, read the surface's own normals, and ask whether they point UP.
# A ground whose normals point down renders black or vanishes under backface culling, and
# it does so silently.
func _initialize() -> void:
	var root3 := Node3D.new(); root.add_child(root3)
	var w := BarrowHeightfield.new("res://data/height_a_authored.png",
								   "res://data/height_a_authored.json")
	var mi := w.build_terrain(root3, StandardMaterial3D.new())
	var arr := (mi.mesh as ArrayMesh).surface_get_arrays(0)
	var norms: PackedVector3Array = arr[Mesh.ARRAY_NORMAL]
	var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
	var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
	var up_n := 0
	for nv in norms:
		if nv.y > 0.0: up_n += 1
	# the normals are supplied by normal_at(), so they are up by construction. The WINDING
	# is a separate fact: compute the face normal from the triangle's own vertex order.
	var up_f := 0
	var down_f := 0
	var i := 0
	while i + 2 < idx.size():
		var a := verts[idx[i]]
		var b := verts[idx[i + 1]]
		var c := verts[idx[i + 2]]
		var fn := (b - a).cross(c - a)
		if fn.y > 0.0: up_f += 1
		else: down_f += 1
		i += 3
	print("[terrain] supplied normals pointing up: %d of %d" % [up_n, norms.size()])
	print("[terrain] FACE WINDING: %d triangles wind up (+Y), %d wind down (-Y)" % [up_f, down_f])
	print("[terrain] verdict: %s" % ("WINDING IS BACKWARD -- faces point down" if down_f > up_f
		else "winding is correct -- faces point up"))
	quit(0)
