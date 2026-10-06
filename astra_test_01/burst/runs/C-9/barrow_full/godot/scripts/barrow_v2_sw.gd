extends "res://scripts/barrow_full.gd"
## C-9 Phase 2 lane BS, R-C9-159 -- BARROW_V2, THE SOUTH-WEST SECTION, AS A LEVEL OF THE V1 BARROW.
##
## Matt, on the first SW proof: the boat, the seams, "the overall quality ... not exactly the same as ...
## barrow v1", "many elements are missing 3D and physics such as plants blowing in the wind and the water
## moving". The conductor's diagnosis: barrow_v2 was built OUTSIDE v1's engine. So this level IS v1's engine:
## it extends barrow_full.gd and inherits ALL of it -- his rig and controls, v1's camera (orthographic,
## pitch 52.95354, YAW 47), the winter sun and the two-sun painted light, paint_stack's pen and paper, the
## SnowField with his footprints and puffs, BarrowHeather's sprays with their gust wind, the snowfall.
## It replaces only what is the PLACE: the ground, the props, the fence -- read from data/barrow_v2_sw/
## (barrow_v2/tools/v2sw_prep.py) and from barrow_v2's own layout and section data, in barrow_v2's sim frame
## (Godot X = x east, Z = y south, Y = up: only the camera turned).
##
## THREE LOOKS, one build:
##   v2_mode "guide"  the GROUND ONLY for the painter: the terrain, the ice, the stream, the water dark --
##                    the models are SHADOW-ONLY (their shadows fall on the ground, their bodies are not
##                    there), no plants, no pen. The painting covers ground only (R-C9-159 clause 2).
##   v2_mode "lit"    the same, white and lit by the sun alone: the painting's direct-sun share (his shadow
##                    darkens only where the painter painted sun -- PaintedWorld's lit map).
##   painted          the play level: the ground wears the painting through the fixed camera (PaintedWorld,
##                    reframed to this section's paint frame); every model wears its OWN bake on its own UVs;
##                    the water is an animated painted-style shader; the plants are v1's 3D sprays; the snow is
##                    v1's field. Launch: scenes/barrow_v2_sw.tscn.

const V2_DATA := "res://data/barrow_v2_sw/"
@export var v2_mode := "play"
var lvl := {}
var sec := {}
var v2 := {}                                   # barrow_v2 layout_v2.json
var v2_root := ""
var ground_meshes: Array = []                  # every surface that wears the ground painting
var floe_mesh: MeshInstance3D
var water_meshes: Array = []
var model_meshes := {}                         # glb key -> [MeshInstance3D]
var water_mat: ShaderMaterial
const LAGOON_Z := -1.30


func _read_json(path: String) -> Dictionary:
	if path == LAYOUT_JSON:
		path = V2_DATA + "level.json"
	return super._read_json(path)


func _v2_path(rel: String) -> String:
	if v2_root == "":
		v2_root = ProjectSettings.globalize_path("res://").path_join("../../barrow_v2").simplify_path()
	return v2_root.path_join(rel)


func _load_v2() -> void:
	if not sec.is_empty():
		return
	lvl = layout
	sec = super._read_json(V2_DATA + "section.json")
	v2 = JSON.parse_string(FileAccess.get_file_as_string(_v2_path("layout_v2.json")))


# --- the ground ---------------------------------------------------------------------------
func _hf_mesh(H: PackedFloat32Array, rows: int, cols: int, x0: float, z0: float, ppm_h: float, cut: Rect2,
		tex: Texture2D, uv_rect: Rect2, nm: String) -> MeshInstance3D:
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	verts.resize(rows * cols)
	uvs.resize(rows * cols)
	for j in rows:
		for i in cols:
			var x := x0 + float(i) / ppm_h
			var z := z0 + float(j) / ppm_h
			verts[j * cols + i] = Vector3(x, H[j * cols + i], z)
			uvs[j * cols + i] = (Vector2(x, z) - uv_rect.position) / uv_rect.size
	var idx := PackedInt32Array()
	var sea_cut := float(lvl["sea_z"]) - 0.6
	for j in rows - 1:
		for i in cols - 1:
			var a := j * cols + i
			var b := a + 1
			var c := a + cols
			var d := c + 1
			if H[a] < sea_cut and H[b] < sea_cut and H[c] < sea_cut and H[d] < sea_cut:
				continue
			if cut.size.x > 0.0:
				var xa := x0 + float(i) / ppm_h
				var za := z0 + float(j) / ppm_h
				if xa >= cut.position.x and xa + 1.0 / ppm_h <= cut.end.x and za >= cut.position.y and za + 1.0 / ppm_h <= cut.end.y:
					continue
			idx.append_array(PackedInt32Array([a, b, c, b, d, c]))
	var nrm := PackedVector3Array()
	nrm.resize(rows * cols)
	for t in range(0, idx.size(), 3):
		var p0 := verts[idx[t]]
		var fn := (verts[idx[t + 2]] - p0).cross(verts[idx[t + 1]] - p0)
		for q in 3:
			nrm[idx[t + q]] += fn
	for v in nrm.size():
		nrm[v] = nrm[v].normalized() if nrm[v].length() > 0.0 else Vector3.UP
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = nrm
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.name = nm
	mi.mesh = am
	mi.material_override = _guide_mat(tex)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	ground_meshes.append(mi)
	return mi


func _guide_mat(tex: Texture2D, vcol := false) -> Material:
	var m := StandardMaterial3D.new()
	if tex != null:
		m.albedo_texture = tex
	m.vertex_color_use_as_albedo = vcol
	m.roughness = 1.0
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	if v2_mode == "lit":
		var sm := ShaderMaterial.new()
		sm.shader = _lit_shader()
		return sm
	return m


static var _lit_sh: Shader


func _lit_shader() -> Shader:
	if _lit_sh == null:
		_lit_sh = Shader.new()
		_lit_sh.code = """shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_disabled, fog_disabled;
void fragment() { ALBEDO = vec3(1.0); }
void light() { DIFFUSE_LIGHT += vec3(ATTENUATION * step(0.06, dot(NORMAL, LIGHT))); }
"""
	return _lit_sh


func _img_tex(path: String) -> ImageTexture:
	var img := Image.load_from_file(path)
	img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


func _build_ground() -> void:
	_load_v2()
	report["ground"] = {}
	var bx: Dictionary = sec["box"]
	var box := Rect2(float(bx["x0"]), float(bx["y0"]), float(bx["x1"]) - float(bx["x0"]), float(bx["y1"]) - float(bx["y0"]))
	# the BX heightfield outside the section box (its own ground colour), the section's inside
	var hf: Dictionary = v2["sculpt"]["heightfield"]
	var H := FileAccess.get_file_as_bytes(_v2_path(String(hf["file"]))).to_float32_array()
	var ex: Dictionary = hf["extent_sim_m"]
	var ext := Rect2(float(ex["x0"]), float(ex["y0"]), float(ex["x1"]) - float(ex["x0"]), float(ex["y1"]) - float(ex["y0"]))
	_hf_mesh(H, int(hf["shape"][0]), int(hf["shape"][1]), ext.position.x, ext.position.y, float(hf["px_per_m"]),
		box.grow(-0.01), _img_tex(_v2_path("godot/data/ground_colour.png")), ext, "TerrainBX")
	var t: Dictionary = sec["terrain"]
	var H2 := FileAccess.get_file_as_bytes(V2_DATA + "terrain.f32").to_float32_array()
	_hf_mesh(H2, int(t["shape"][0]), int(t["shape"][1]), box.position.x, box.position.y, float(t["px_per_m"]),
		Rect2(), _img_tex(ProjectSettings.globalize_path(V2_DATA + "ground.png")), box, "TerrainSection")
	_build_water()
	_build_floes()
	_build_stream()
	_build_ledge()
	_build_fence()
	report["ground"]["v2"] = {"box": [box.position.x, box.position.y, box.size.x, box.size.y], "mode": v2_mode}


func _build_water() -> void:
	var sea := float(lvl["sea_z"])
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(0.10, 0.16, 0.22)
	m.roughness = 1.0
	var big := PackedVector3Array([Vector3(-160, sea, -160), Vector3(160, sea, -160), Vector3(160, sea, 160), Vector3(-160, sea, 160)])
	water_meshes.append(_poly_mesh(big, m, "Sea"))
	# the lagoon: bounded south by the spit's centreline (the spit's ridge hides the edge)
	var A := Vector2(-41.5, 26.8)
	var D := Vector2(-0.94, 0.34)
	var a14 := A + D * -14.0
	var a42 := A + D * 42.0
	var lag := PackedVector3Array([Vector3(-80, LAGOON_Z, -14), Vector3(-27, LAGOON_Z, -14), Vector3(a14.x, LAGOON_Z, a14.y), Vector3(a42.x, LAGOON_Z, a42.y)])
	water_meshes.append(_poly_mesh(lag, m, "Lagoon"))


func _poly_mesh(pts: PackedVector3Array, mat: Material, nm: String) -> MeshInstance3D:
	var p2 := PackedVector2Array()
	for p in pts:
		p2.append(Vector2(p.x, p.z))
	var tri := Geometry2D.triangulate_polygon(p2)
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in tri:
		st.set_normal(Vector3.UP)
		st.set_uv(Vector2(pts[i].x, pts[i].z))
		st.add_vertex(pts[i])
	var mi := MeshInstance3D.new()
	mi.name = nm
	mi.mesh = st.commit()
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	return mi


func _build_floes() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var k := 0
	for f in sec["floes"]:
		var p2 := PackedVector2Array()
		for q in f["poly"]:
			p2.append(Vector2(float(q[0]), float(q[1])))
		var tri := Geometry2D.triangulate_polygon(p2)
		if tri.is_empty():
			continue
		var top := float(f["top"])
		var bot := float(f["bot"])
		var ph := fposmod(float(k) * 0.6180339, 1.0)      # the floe's bob phase, in the vertex colour's alpha
		k += 1
		var ctop := Color(0.80, 0.88, 0.95).lerp(Color(0.95, 0.96, 0.98), float(f["snow"]))
		ctop.a = ph
		var cside := Color(0.52, 0.68, 0.80, ph)
		for i in tri:
			st.set_color(ctop)
			st.set_normal(Vector3.UP)
			st.add_vertex(Vector3(p2[i].x, top, p2[i].y))
		for i in p2.size():
			var a := p2[i]
			var b := p2[(i + 1) % p2.size()]
			var e := (b - a).normalized()
			var n := Vector3(e.y, 0, -e.x)
			for v in [Vector3(a.x, bot, a.y), Vector3(b.x, bot, b.y), Vector3(b.x, top, b.y), Vector3(a.x, bot, a.y), Vector3(b.x, top, b.y), Vector3(a.x, top, a.y)]:
				st.set_color(cside)
				st.set_normal(n)
				st.add_vertex(v)
	# the pressure ridges and the brash, as small blocks in the same mesh (static: they are ground)
	var rng := RandomNumberGenerator.new()
	rng.seed = 159
	for r in sec["ridges"]:
		var s: Array = r["size"]
		var ro: Array = r["rot"]
		var bas := Basis.from_euler(Vector3(deg_to_rad(float(ro[0])), deg_to_rad(float(ro[1])), deg_to_rad(float(ro[2])))).scaled_local(Vector3(float(s[0]), float(s[1]), float(s[2])))
		_box_into(st, Transform3D(bas, Vector3(float(r["pos"][0]), float(r["z"]), float(r["pos"][1]))), Color(0.84, 0.90, 0.96, rng.randf()))
	for q in sec.get("brash", []):
		var r3 := float(q[3])
		var bas2 := Basis(Vector3.UP, deg_to_rad(float(q[4]))).scaled(Vector3(r3 * 1.2, 0.12, r3))
		_box_into(st, Transform3D(bas2, Vector3(float(q[0]), float(q[2]), float(q[1]))), Color(0.88, 0.92, 0.97, rng.randf()))
	floe_mesh = MeshInstance3D.new()
	floe_mesh.name = "Floes"
	floe_mesh.mesh = st.commit()
	var m := StandardMaterial3D.new()
	m.vertex_color_use_as_albedo = true
	m.roughness = 1.0
	floe_mesh.material_override = _guide_mat(null, true) if v2_mode == "lit" else m
	floe_mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(floe_mesh)


func _box_into(st: SurfaceTool, xf: Transform3D, col: Color) -> void:
	var c := [Vector3(-.5, -.5, -.5), Vector3(.5, -.5, -.5), Vector3(.5, .5, -.5), Vector3(-.5, .5, -.5),
			  Vector3(-.5, -.5, .5), Vector3(.5, -.5, .5), Vector3(.5, .5, .5), Vector3(-.5, .5, .5)]
	var faces := [[0, 1, 2, 3], [5, 4, 7, 6], [4, 0, 3, 7], [1, 5, 6, 2], [3, 2, 6, 7], [4, 5, 1, 0]]
	for f in faces:
		var p := []
		for i in f:
			p.append(xf * (c[i] as Vector3))
		var n: Vector3 = ((p[1] as Vector3) - (p[0] as Vector3)).cross((p[2] as Vector3) - (p[0] as Vector3)).normalized()
		for tri in [[0, 1, 2], [0, 2, 3]]:
			for i in tri:
				st.set_color(col)
				st.set_normal(-n)
				st.add_vertex(p[i])


func _build_stream() -> void:
	var R: Array = sec["stream"]["ribbon"]
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in R.size() - 1:
		var a := Vector3(float(R[i][0]), float(R[i][2]), float(R[i][1]))
		var b := Vector3(float(R[i + 1][0]), float(R[i + 1][2]), float(R[i + 1][1]))
		var d := b - a
		d.y = 0
		d = d.normalized()
		var s := Vector3(-d.z, 0, d.x)
		var wa := float(R[i][3]) * 0.5
		var wb := float(R[i + 1][3]) * 0.5
		for v in [a - s * wa, b - s * wb, b + s * wb, a - s * wa, b + s * wb, a + s * wa]:
			st.set_color(Color(0.64, 0.78, 0.90))
			st.set_normal(Vector3.UP)
			st.add_vertex(v)
	var mi := MeshInstance3D.new()
	mi.name = "Stream"
	mi.mesh = st.commit()
	var m := StandardMaterial3D.new()
	m.vertex_color_use_as_albedo = true
	m.roughness = 1.0
	mi.material_override = _guide_mat(null, true) if v2_mode == "lit" else m
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	ground_meshes.append(mi)


func _build_ledge() -> void:
	# the cave's sea-level ledge (the layout's bottom landing): ground, painted with it
	var S: Dictionary = v2["stair"]
	var poly: Array = S["bottom_landing"]["polygon"]
	var p2 := PackedVector2Array()
	for p in poly:
		p2.append(Vector2(float(p[0]), float(p[1])))
	var tri := Geometry2D.triangulate_polygon(p2)
	var z1 := float(S["bottom_landing"]["z_m"])
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in tri:
		st.set_normal(Vector3.UP)
		st.add_vertex(Vector3(p2[i].x, z1, p2[i].y))
	var mi := MeshInstance3D.new()
	mi.name = "CaveLedge"
	mi.mesh = st.commit()
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(0.50, 0.48, 0.45)
	mi.material_override = _guide_mat(null) if v2_mode == "lit" else m
	add_child(mi)
	ground_meshes.append(mi)


func _build_fence() -> void:
	"""THE WALKABLE FLOOR IS THE LAYOUT'S (v6): one collider slab at y = 0 under it and a wall on every
	floor edge -- except where the stair's flush landing opens off it, which is fenced on its own edges."""
	var body := StaticBody3D.new()
	body.name = "FloorBody"
	body.collision_layer = TERRAIN_BIT
	body.collision_mask = 0
	add_child(body)
	var cs := CollisionShape3D.new()
	var bxs := BoxShape3D.new()
	bxs.size = Vector3(200, 2, 200)
	cs.shape = bxs
	cs.position = Vector3(0, -1.0, 0)
	body.add_child(cs)
	var fl: Array = lvl["floor_polygon_xz"]
	var land := PackedVector2Array()
	for p in lvl["stair_landing_xz"]:
		land.append(Vector2(float(p[0]), float(p[1])))
	var n := 0
	for i in fl.size():
		var a := Vector2(float(fl[i][0]), float(fl[i][1]))
		var b := Vector2(float(fl[(i + 1) % fl.size()][0]), float(fl[(i + 1) % fl.size()][1]))
		var mid := (a + b) * 0.5
		if Geometry2D.is_point_in_polygon(mid, land) or _dist_poly(mid, land) < 0.25:
			continue
		_wall(body, a, b)
		n += 1
	for i in land.size():
		var a2 := land[i]
		var b2 := land[(i + 1) % land.size()]
		var m2 := (a2 + b2) * 0.5
		var inside := false
		for j in fl.size():
			if Vector2(float(fl[j][0]), float(fl[j][1])).distance_to(m2) < 0.3:
				inside = true
		if not inside and not Geometry2D.is_point_in_polygon(m2 + (m2 - _centroid2(land)).normalized() * -0.3, _poly2(fl)):
			_wall(body, a2, b2)
			n += 1
	report["ground"]["fence_walls"] = n


func _centroid2(p: PackedVector2Array) -> Vector2:
	var c := Vector2.ZERO
	for q in p:
		c += q
	return c / float(p.size())


func _poly2(a: Array) -> PackedVector2Array:
	var o := PackedVector2Array()
	for p in a:
		o.append(Vector2(float(p[0]), float(p[1])))
	return o


func _dist_poly(p: Vector2, poly: PackedVector2Array) -> float:
	var best := INF
	for i in poly.size():
		var q := Geometry2D.get_closest_point_to_segment(p, poly[i], poly[(i + 1) % poly.size()])
		best = minf(best, q.distance_to(p))
	return best


func _wall(body: StaticBody3D, a: Vector2, b: Vector2) -> void:
	var d := b - a
	var cs := CollisionShape3D.new()
	var bx := BoxShape3D.new()
	bx.size = Vector3(d.length() + 0.3, 3.0, 0.3)
	cs.shape = bx
	cs.position = Vector3((a.x + b.x) * 0.5, 1.5, (a.y + b.y) * 0.5)
	cs.rotation = Vector3(0, -atan2(d.y, d.x), 0)
	body.add_child(cs)


func _build_mound() -> void:
	pass


func _build_bounds() -> void:
	report["bounds"] = {"what": "the floor fence (_build_fence)"}


func _build_overlay() -> void:
	pass


func _build_crucible() -> void:
	pass


func floor_y_at(_u: float, _v: float) -> float:
	return 0.0


# --- the props: the section's coast kit + the layout's placed models -----------------------
var _glb_cache := {}


func _glb(key: String) -> Node3D:
	var path := key
	if path.begins_with("runs/"):
		path = _v2_path("../../" + path.substr(5))
	elif not path.begins_with("res://") and not path.begins_with("/"):
		path = _v2_path(path)
	if not _glb_cache.has(path):
		if path.begins_with("res://"):
			var ps: PackedScene = load(path)
			_glb_cache[path] = ps.instantiate() if ps != null else null
		else:
			var doc := GLTFDocument.new()
			var st := GLTFState.new()
			if doc.append_from_file(path, st) != OK:
				push_error("barrow_v2_sw: cannot load %s" % path)
				_glb_cache[path] = null
			else:
				_glb_cache[path] = doc.generate_scene(st)
	var n = _glb_cache[path]
	return (n as Node3D).duplicate() if n != null else null


func _aabb_local(n: Node, xf: Transform3D) -> AABB:
	var out := AABB()
	var first := true
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		out = t * (n as MeshInstance3D).mesh.get_aabb()
		first = false
	for ch in n.get_children():
		var b := _aabb_local(ch, t)
		if b.size == Vector3.ZERO:
			continue
		out = b if first else out.merge(b)
		first = false
	return out


func _place(id: String, key: String, pos: Vector2, z: float, yaw_deg: float, size: Vector3, lean := 0.0) -> Node3D:
	var model := _glb(key)
	if model == null:
		return null
	var ab := _aabb_local(model, model.transform.affine_inverse())
	var holder := Node3D.new()
	holder.name = id
	var sc := Vector3(size.x / maxf(ab.size.x, 1e-3), size.y / maxf(ab.size.y, 1e-3), size.z / maxf(ab.size.z, 1e-3))
	holder.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(yaw_deg)) * Basis(Vector3.RIGHT, deg_to_rad(lean)) * Basis.from_scale(sc), Vector3(pos.x, z, pos.y))
	model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
	holder.add_child(model)
	props_root.add_child(holder)
	nodes[id] = holder
	built[id] = {"glb": key}
	for mi in _meshes(holder):
		(model_meshes.get_or_add(key, []) as Array).append(mi)
		if v2_mode in ["guide", "lit"]:
			(mi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY
	return holder


func _place_beam(id: String, key: String, a: Vector3, b: Vector3, th: float) -> void:
	var model := _glb(key)
	if model == null:
		return
	var ab := _aabb_local(model, model.transform.affine_inverse())
	var k := 0
	if ab.size.y > ab.size[k]:
		k = 1
	if ab.size.z > ab.size[k]:
		k = 2
	var d := b - a
	var ln := d.length()
	var zz := d / maxf(ln, 1e-3)
	var xx := Vector3.UP.cross(zz)
	xx = Vector3.RIGHT if xx.length() < 0.05 else xx.normalized()
	var yy := zz.cross(xx).normalized()
	var cols := [Vector3.ZERO, Vector3.ZERO, Vector3.ZERO]
	var others := [0, 1, 2]
	others.erase(k)
	cols[k] = zz * (ln / maxf(ab.size[k], 1e-3))
	cols[others[0]] = xx * (th / maxf(ab.size[others[0]], 1e-3))
	cols[others[1]] = yy * (th / maxf(ab.size[others[1]], 1e-3))
	var holder := Node3D.new()
	holder.name = id
	holder.transform = Transform3D(Basis(cols[0], cols[1], cols[2]), (a + b) / 2.0)
	model.position = -(ab.position + ab.size / 2.0)
	holder.add_child(model)
	props_root.add_child(holder)
	nodes[id] = holder
	built[id] = {"glb": key}
	for mi in _meshes(holder):
		(model_meshes.get_or_add(key, []) as Array).append(mi)
		if v2_mode in ["guide", "lit"]:
			(mi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY


# v1's own bakes of its kit (data/painted/bakes, on the same GLBs' UVs): one instance's bake each
const V1_BAKES := {"res://models/barrow/kit/cairn.glb": "bakes/cairn_1.bin", "res://models/barrow/kit/log.glb": "bakes/fallen_tree_log_A.bin",
				   "res://models/barrow/stone_tall.glb": "bakes/ring_m55.bin", "res://models/barrow/stone_mid.glb": "bakes/ring_m135.bin"}
# R-C9-159: THE WRECK, redone to sketch A (BVM-wreck2 -> Tripo -> normalised 17 x 10.03 x 6.42 m, uniform): half-sunk
# into the shingle and the shore ice, heeled toward the floor, set 0.9 m seaward of the slot so its beam stays off the
# floor and out of the p01 lane
const WRECK2 := {"glb": "godot/models/build/wreck2.glb", "pos": Vector2(-48.1, 13.3), "z": -2.1, "size": Vector3(17.0, 10.03, 6.42), "lean": 20.0}
const KIT := {"cairn": "res://models/barrow/kit/cairn.glb", "log": "res://models/barrow/kit/log.glb",
			  "stone_tall": "res://models/barrow/stone_tall.glb", "stone_mid": "res://models/barrow/stone_mid.glb"}


func _glb_key(kind: String) -> String:
	if KIT.has(kind):
		return KIT[kind]
	return String(sec["glb"][kind])


func _build_placements() -> void:
	_load_v2()
	var bx: Dictionary = sec["box"]
	var skip: Array = sec["skip_models"]
	var n := 0
	# the layout's placed models inside the section box (the wreck, the cave cliff, the stair cliff)
	for m in v2["models"]:
		if skip.has(m["id"]) or m.get("glb") == null or not (m.get("instances", []) as Array).is_empty():
			continue
		var p := Vector2(float(m["pos"][0]), float(m["pos"][1]))
		if p.x < float(bx["x0"]) or p.x > float(bx["x1"]) or p.y < float(bx["y0"]) or p.y > float(bx["y1"]):
			continue
		var sz: Dictionary = m["size_m"]
		var key := String(m["glb"])
		var z := float(m["z"])
		if m["id"] == "wreck" and FileAccess.file_exists(_v2_path(String(WRECK2["glb"]))):
			_place("wreck", String(WRECK2["glb"]), WRECK2["pos"], float(WRECK2["z"]), float(m["godot_rot_y_deg"]), WRECK2["size"], float(WRECK2["lean"]))
			n += 1
			continue
		var rot := float(m["godot_rot_y_deg"])
		if m["id"] == "cave_cliff" and sec.has("cave_override"):
			# R-C9-159: turned to face the v1 camera (section_sw_build.py's override, floor clearance checked there)
			var co: Dictionary = sec["cave_override"]
			p = Vector2(float(co["pos"][0]), float(co["pos"][1]))
			rot = float(co["godot_rot_y_deg"])
			sz = co["size_m"]
		_place(String(m["id"]), key, p, z, rot, Vector3(float(sz["w_local_x"]), float(sz["h"]), float(sz["d_local_z"])))
		n += 1
	var I: Dictionary = sec["instances"]
	for kind in ["cliff", "crag", "cairn", "stone_tall", "stone_mid"]:
		var i := 0
		for it in I[kind]:
			var sz2: Array = it["size"]
			_place("%s_%d" % [kind, i], _glb_key(kind), Vector2(float(it["pos"][0]), float(it["pos"][1])), float(it["z"]),
				float(it["yaw"]), Vector3(float(sz2[0]), float(sz2[1]), float(sz2[2])), float(it.get("lean", 0.0)))
			i += 1
			n += 1
	# the notch between the turned cave and the stair cliff (R-C9-159): one more face, so no bare talus shows there
	_place("cliff_notch_v1cam", _glb_key("cliff"), Vector2(7.4, 42.7), -8.4, -6.0, Vector3(5.0, 8.9, 3.2))
	var j := 0
	for it in I["log"]:
		var a: Array = it["a"]
		var b: Array = it["b"]
		_place_beam("log_%d" % j, _glb_key("log"), Vector3(float(a[0]), float(a[2]), float(a[1])), Vector3(float(b[0]), float(b[2]), float(b[1])), float(it["th"]))
		j += 1
		n += 1
	report["placements"] = {"models": n, "glbs": model_meshes.keys()}


# --- the painted level -------------------------------------------------------------------
func _frame_mat(m: ShaderMaterial) -> void:
	var F: Dictionary = lvl["frame"]["paint"]
	var p := deg_to_rad(PL_PITCH_DEG)
	var ppm := float(F["ppm"])
	m.set_shader_parameter("g_frame", Vector3(float(F["u0"]), float(F["v1"]), ppm))
	m.set_shader_parameter("g_px_per", Vector2(ppm * sin(p), ppm * cos(p)))
	m.set_shader_parameter("g_size", Vector2(float(F["size_px"][0]), float(F["size_px"][1])))


const FLOE_BOB := """
	// R-C9-159: the floes ride the swell -- a slow bob and a small sway per floe (its phase in COLOR.a)
	float ph = COLOR.a * 6.2831;
	VERTEX.y += (0.035 * sin(TIME * 0.9 + ph) + 0.015 * sin(TIME * 2.1 + ph * 1.7)) * step(VERTEX.y, -1.0);
	VERTEX.xz += vec2(0.03 * sin(TIME * 0.5 + ph), 0.03 * cos(TIME * 0.43 + ph)) * step(VERTEX.y, -1.0);
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
"""


func _dress_painted() -> void:
	var t0 := Time.get_ticks_msec()
	var loads := {}
	paint = {"manifest": V2_DATA + "painted/", "loads": loads, "ground_variant": "v2_ground_only"}
	var pdir := ProjectSettings.globalize_path(V2_DATA + "painted/")
	var painting := _img_tex(pdir.path_join("ground.png")) if FileAccess.file_exists(pdir.path_join("ground.png")) else null
	var lit: Texture2D = _img_tex(pdir.path_join("lit.png")) if FileAccess.file_exists(pdir.path_join("lit.png")) else null
	if painting == null:
		push_error("barrow_v2_sw: no ground painting at %s" % pdir)
		paint["error"] = "no painting"
		return
	var shadow_mul := Vector3(0.4188, 0.5479, 0.8918)          # v1's measured painter's shadow (linear)
	_paint_tex = {"painting": painting, "ground": painting, "lit": lit}
	var mat_ground := PaintedWorld.painted_material(painting, true, lit, shadow_mul, u_hat, v_hat)
	_frame_mat(mat_ground)
	var n := {"ground": 0, "floes": 0, "baked": 0, "baked_meshes": 0, "unbaked": []}
	for mi in ground_meshes:
		_paint_mesh(mi, mat_ground, false)
		n["ground"] += 1
	# THE FLOES wear the painting too, riding the swell (the painting slides with them by centimetres)
	var fm := ShaderMaterial.new()
	var code: String = PaintedWorld.PAINTED_SHADER
	code = PaintedWorld._swap(code, "	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;\n", FLOE_BOB, "floe bob")
	fm.shader = PaintedWorld._shader("v2_floes", code)
	fm.set_shader_parameter("paint_tex", painting)
	fm.set_shader_parameter("project_uv", true)
	fm.set_shader_parameter("painted_mark", PaintedWorld.PAINTED_MARK)
	PaintedWorld.bind_projection(fm, lit, shadow_mul, u_hat, v_hat)
	_frame_mat(fm)
	_paint_mesh(floe_mesh, fm, false)
	n["floes"] = 1
	# EACH MODEL WEARS ITS OWN BAKE, on its own UVs (one bake per model, shared by its instances): the painted
	# ALBEDO, lit by v1's ramp under the real sun. NOT unlit as v1's heroes: v1 baked each hero from the one
	# painting at its own placement, light and all; here one model stands at many yaws, so its light cannot be
	# painted in -- the sun lights it, it shades itself, and its cast shadow on the ground is in the painting.
	var bk: Dictionary = super._read_json(V2_DATA + "bakes/bakes.json")
	for key in model_meshes:
		var tex: Texture2D = null
		if bk.has(key):
			tex = _img_tex(ProjectSettings.globalize_path(V2_DATA + "bakes/" + String(bk[key])))
		elif V1_BAKES.has(key):
			var img := Image.new()
			img.load_png_from_buffer(FileAccess.get_file_as_bytes(PaintedWorld.DATA + String(V1_BAKES[key])))
			img.generate_mipmaps()
			tex = ImageTexture.create_from_image(img)
		if tex == null:
			n["unbaked"].append(key)
			continue
		var mat := PaintStack.world_material(fbm, Color(0.62, 0.60, 0.58), {"use_tex": true, "snow_amount": 0.0,
			"mottle_amp": 0.0, "hatch_amp": 0.0, "wash_amp": 0.06,
			"mesh_mark": PaintedWorld.PAINTED_MARK})      # the pen is IN the bake (as v1's plates): the post pass skips it
		mat.set_shader_parameter("albedo_tex", tex)
		mat.set_shader_parameter("tex_tint", Vector3(0.80, 0.79, 0.77))   # the bake is painted light-to-dark; the ramp adds the sun
		world_mats.append(mat)
		for mi in model_meshes[key]:
			(mi as MeshInstance3D).material_override = mat
			(mi as MeshInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
			n["baked_meshes"] += 1
		n["baked"] += 1
	# THE WATER: animated, painted-style, under the pen
	water_mat = _water_material(painting)
	for w in water_meshes:
		(w as MeshInstance3D).material_override = water_mat
		(w as MeshInstance3D).layers = PaintedWorld.LAYER_PAINTED
	# THE TWO SUNS (barrow_full._dress_painted, unchanged)
	var paint_layers := PaintedWorld.LAYER_PAINTED | PaintedWorld.LAYER_ON_PAINT
	var dyn := PaintedWorld.ALL_LAYERS & ~paint_layers
	sun.light_cull_mask = dyn
	sun.shadow_caster_mask = PaintedWorld.ALL_LAYERS
	paint_sun = sun.duplicate() as DirectionalLight3D
	paint_sun.name = "PaintSun"
	paint_sun.light_cull_mask = paint_layers
	paint_sun.shadow_caster_mask = dyn
	sun.get_parent().add_child(paint_sun)
	paint_sun.global_transform = sun.global_transform
	paint_sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	paint_sun.directional_shadow_max_distance = CAM_STANDOFF + 12.0
	paint_sun.shadow_blur = 0.6
	PaintStack.post_set(post_mat, "painted_exclude", 1.0)
	_v2_heather(lit, shadow_mul)
	_v2_snow(painting, lit, shadow_mul)
	var flake := PaintStack.make_flake_texture()
	snowfall = PaintStack.snowfall(flake, Vector3(46, 28, 46), 1700)
	snowfall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(snowfall)
	paint["pieces"] = n
	paint["files_ok"] = 0
	paint["ms"] = Time.get_ticks_msec() - t0
	report["painted"] = paint


func _v2_heather(lit: Texture2D, shadow_mul: Vector3) -> void:
	var hj = JSON.parse_string(FileAccess.get_file_as_string(V2_DATA + "heather.json"))
	var rows: Array = hj["rows"]
	var am := Vector3(1.2514, 1.0106, 0.5677)                  # v1's albedo_mul (manifest heather)
	heather_mat = PaintedWorld.heather_material(fbm, am, lit, shadow_mul, u_hat, v_hat)
	_frame_mat(heather_mat)
	heather_mat.set_shader_parameter("wind_dir", WIND.normalized())
	var by_var := []
	for v in BarrowHeather.VARIANTS:
		by_var.append([])
	for i in rows.size():
		by_var[int(fposmod(float(i) * 7.0 + 3.0, float(BarrowHeather.VARIANTS)))].append(i)
	var thin := []
	for v in BarrowHeather.VARIANTS:
		var mesh := BarrowHeather.spray_mesh(v)
		var ab := mesh.get_aabb()
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.use_custom_data = true
		mm.use_colors = true
		mm.mesh = mesh
		mm.instance_count = (by_var[v] as Array).size()
		for k in (by_var[v] as Array).size():
			var i: int = by_var[v][k]
			var r: Array = rows[i]
			var hh := float(r[2]) * (0.85 + 0.30 * fposmod(float(i) * 0.6180339, 1.0))
			var y := _ground_y(float(r[0]), float(r[1]))
			mm.set_instance_transform(k, Transform3D(Basis().scaled(Vector3.ONE * hh), Vector3(float(r[0]), y - 0.01, float(r[1]))))
			mm.set_instance_custom_data(k, Color(float(r[4]), float(r[5]), float(r[6]), 1.0))
			mm.set_instance_color(k, Color(1, 1, 1, 1))
			thin.append({"c": Vector2(float(r[0]), float(r[1])), "r": maxf(ab.size.x, ab.size.z) * hh * 0.4,
						 "feather": 0.18, "max_d": hh * HEATHER_SNOW_FRAC})
		var mmi := MultiMeshInstance3D.new()
		mmi.name = "Heather_%d" % v
		mmi.multimesh = mm
		mmi.material_override = heather_mat
		mmi.layers = PaintedWorld.LAYER_ON_PAINT
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(mmi)
		_heather_mmi.append(mmi)
	paint["heather"] = {"instances": rows.size(), "multimeshes": _heather_mmi.size()}
	paint["_thin_zones"] = thin


var _H2: PackedFloat32Array


func _ground_y(x: float, z: float) -> float:
	if _H2.is_empty():
		_H2 = FileAccess.get_file_as_bytes(V2_DATA + "terrain.f32").to_float32_array()
	var t: Dictionary = sec["terrain"]
	var bx: Dictionary = sec["box"]
	var ppm_h := float(t["px_per_m"])
	var nx := int(t["shape"][1])
	var ny := int(t["shape"][0])
	var fx := clampf((x - float(bx["x0"])) * ppm_h, 0.0, nx - 1.001)
	var fz := clampf((z - float(bx["y0"])) * ppm_h, 0.0, ny - 1.001)
	var i := int(fx)
	var j := int(fz)
	var ax := fx - i
	var az := fz - j
	var h00 := _H2[j * nx + i]
	var h10 := _H2[j * nx + i + 1]
	var h01 := _H2[(j + 1) * nx + i]
	var h11 := _H2[(j + 1) * nx + i + 1]
	return lerpf(lerpf(h00, h10, ax), lerpf(h01, h11, ax), az)


func _v2_snow(ground_tex: Texture2D, lit: Texture2D, shadow_mul: Vector3) -> void:
	var sn: Dictionary = lvl["snow"]
	var g: Dictionary = sn["grid"]
	var buf := FileAccess.get_file_as_bytes(V2_DATA + String(g["file"])).to_float32_array()
	var nx := int(g["nx"])
	var nz := int(g["nz"])
	var go: Array = g["origin_xz"]
	snow = SnowField.new()
	snow.name = "SnowField"
	snow.fbm_tex = fbm
	snow.field_px = int(sn["field_px"])
	snow.trail_px = int(sn["trail_px"])
	snow.windrow_count = 0
	snow.pile_count = 0
	snow.cast_shadows = false
	snow.depth_grid = {"origin": Vector2(float(go[0]), float(go[1])), "cell_m": float(g["cell_m"]),
					   "nx": nx, "nz": nz, "mul": buf.slice(0, nx * nz), "trod": buf.slice(nx * nz, 2 * nx * nz)}
	snow.thin_zones = paint.get("_thin_zones", [])
	paint.erase("_thin_zones")
	snow.shader_code_override = PaintedWorld.snow_shader_code()
	var ar: Array = sn["area_xz"]
	snow.setup(Rect2(float(ar[0]), float(ar[1]), float(ar[2]), float(ar[3])), 0.0, [], WIND)
	add_child(snow)
	if knight != null:
		snow.track(knight)
	var smat := snow.material()
	smat.set_shader_parameter("paint_tex", ground_tex)
	PaintedWorld.bind_projection(smat, lit, shadow_mul, u_hat, v_hat)
	_frame_mat(smat)
	snow.surface().layers = PaintedWorld.LAYER_ON_PAINT
	if heather_mat != null:
		BarrowHeather.bind_snow(heather_mat, snow, WIND)
	paint["snow"] = snow.bake_report()


# --- the water ----------------------------------------------------------------------------
const WATER_SHADER := """
shader_type spatial;
render_mode unshaded, cull_disabled, fog_disabled, specular_disabled;
// R-C9-159: the sea and the lagoon, MOVING, in the painting's own hand. The colour is the PAINTING's
// (projected through the fixed camera, as the ground's), so the painted water between the floes stays the
// painter's; over it, slow wash ripples drifting on the swell, a darker lead tone where the water is open,
// and FOAM RINGS that pulse round every floe's edge (the floes' distance field, water_sdf).
uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform sampler2D water_sdf : filter_linear, repeat_disable;     // R: metres to the nearest floe edge / 2
uniform vec4 sdf_rect = vec4(-70.0, -14.0, 96.0, 76.0);           // x0, z0, w, h (world xz)
uniform vec3 g_u_hat = vec3(0.681998, 0.0, -0.731354);
uniform vec3 g_v_hat = vec3(-0.731354, 0.0, -0.681998);
uniform vec3 g_frame = vec3(0.0, 0.0, 50.0);
uniform vec2 g_px_per = vec2(40.0, 30.0);
uniform vec2 g_size = vec2(2816.0, 3328.0);
uniform vec3 deep_col : source_color = vec3(0.13, 0.22, 0.31);
uniform vec3 crest_col : source_color = vec3(0.62, 0.72, 0.80);
uniform vec3 foam_col : source_color = vec3(0.92, 0.94, 0.96);
uniform float paint_mix = 0.75;
varying vec3 v_world;
vec2 guide_uv(vec3 p) {
	float u = dot(p, g_u_hat);
	float v = dot(p, g_v_hat);
	return vec2((u - g_frame.x) * g_frame.z, (g_frame.y - v) * g_px_per.x - p.y * g_px_per.y) / g_size;
}
void vertex() { v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	vec2 xz = v_world.xz;
	vec2 guv = guide_uv(v_world);
	bool inside = guv.x > 0.0 && guv.y > 0.0 && guv.x < 1.0 && guv.y < 1.0;
	vec3 base = mix(deep_col, inside ? texture(paint_tex, guv).rgb : deep_col, paint_mix);
	// the swell: two drifting wash layers, quantised into a few soft bands (a brush, not a gradient)
	float n1 = texture(noise_tex, xz * 0.045 + vec2(TIME * 0.012, TIME * 0.007)).r;
	float n2 = texture(noise_tex, xz * 0.11 + vec2(-TIME * 0.02, TIME * 0.016)).r;
	float sw = n1 * 0.6 + n2 * 0.4;
	float band = smoothstep(0.58, 0.64, sw) - smoothstep(0.70, 0.76, sw);
	vec3 col = base * (0.88 + 0.22 * smoothstep(0.35, 0.75, sw));
	col = mix(col, crest_col, band * 0.35);
	// fine ripple strokes: thin crests travelling across the wind
	float r = texture(noise_tex, vec2(xz.x * 0.35 + TIME * 0.05, xz.y * 0.9 - TIME * 0.03)).r;
	col = mix(col, crest_col, smoothstep(0.80, 0.86, r) * 0.45);
	// foam rings round the floes, breathing with the swell
	vec2 su = (xz - sdf_rect.xy) / sdf_rect.zw;
	float d = texture(water_sdf, su).r * 2.0;
	float pulse = 0.18 + 0.08 * sin(TIME * 1.3 + n1 * 9.0);
	float fn = texture(noise_tex, xz * 0.9 + vec2(TIME * 0.04, -TIME * 0.03)).r;
	// a broken lace of foam hugging the floe edge, its width breathing with the swell
	float lace = (1.0 - smoothstep(pulse * 0.5, pulse, d)) * smoothstep(0.42, 0.62, fn + 0.25 * (1.0 - d / max(pulse, 1e-3)));
	float inb = step(0.0, su.x) * step(su.x, 1.0) * step(0.0, su.y) * step(su.y, 1.0);
	col = mix(col, foam_col, clamp(lace, 0.0, 1.0) * 0.85 * inb);
	ALBEDO = col;
	ROUGHNESS = 0.0;
}
"""


func _water_material(painting: Texture2D) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = WATER_SHADER
	m.shader = sh
	m.set_shader_parameter("paint_tex", painting)
	m.set_shader_parameter("noise_tex", fbm)
	var sdf := ProjectSettings.globalize_path(V2_DATA + "water_sdf.png")
	if FileAccess.file_exists(sdf):
		m.set_shader_parameter("water_sdf", _img_tex(sdf))
	m.set_shader_parameter("g_u_hat", u_hat)
	m.set_shader_parameter("g_v_hat", v_hat)
	_frame_mat(m)
	return m
