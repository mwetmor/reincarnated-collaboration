extends Node3D
## C-9 Phase 2 lane BX: the barrow_v2 'Fjord Headland' GREYBOX, built at run time from
## ../layout_v2.json (the validated sim-frame layout; tools/validate_layout_v2.py).
##
## Frames: sim +x east, +y SOUTH, z up  ->  Godot X = x, Y = z, Z = y.
## Camera: orthographic, pitch 52.9535411256029 deg, ZERO yaw (it sits south of its target and
## looks north), keep_height, size = viewport_rows / ppm.  Default ppm = the arena PLATE scale
## (100.617553710938 px/m: a 19.1 x 13.4 m window at 1080 rows); Z toggles ZOOM-GD (ppm 75.668,
## the 25.4 x 17.9 m window the stills and the film use).
##
## Controls: WASD / arrows walk the grey 1.9 m capsule (6 m/s, Shift 9 m/s), Z toggles the zoom,
## L toggles the anchor labels.  Nothing here blocks the capsule: the sim floor is an open plane.

const ALPHA_DEG := 52.9535411256029
const PPM_PLATE := 100.617553710938
const H_FIG_M := 1.9
const FRACTION_ZOOM_GD := 0.0802
const VIEW_H := 1080.0
const EXT := {"x0": -62.0, "x1": 66.0, "y0": -74.0, "y1": 62.0}   # must match tools/render_ground_and_plan.py

const KIND_RGB := {
	"mound": Color(0.66, 0.64, 0.55), "door": Color(0.25, 0.18, 0.12), "standing_stone": Color(0.47, 0.47, 0.46),
	"wreck": Color(0.45, 0.31, 0.19), "mast": Color(0.33, 0.22, 0.14), "rock": Color(0.50, 0.50, 0.49),
	"hall": Color(0.33, 0.26, 0.20), "gable": Color(0.38, 0.27, 0.19), "palisade": Color(0.40, 0.31, 0.22),
	"cliff": Color(0.58, 0.55, 0.50), "cave": Color(0.05, 0.05, 0.06), "fallen_stone": Color(0.62, 0.61, 0.57),
	"grave_marker": Color(0.45, 0.41, 0.38), "driftwood": Color(0.56, 0.45, 0.32), "beam": Color(0.18, 0.15, 0.13),
}

var layout: Dictionary = {}
var cam: Camera3D
var walker: Node3D
var labels: Array = []
var zoom_gd := false
var ppm := PPM_PLATE
var free_cam := false          # the capture runner drives the camera directly
var cam_target := Vector2.ZERO  # sim-frame metres


static func ppm_gd() -> float:
	return FRACTION_ZOOM_GD * VIEW_H / (H_FIG_M * cos(deg_to_rad(ALPHA_DEG)))


static func g(p) -> Vector3:
	return Vector3(float(p[0]), 0.0, float(p[1]))


func _ready() -> void:
	var path := ProjectSettings.globalize_path("res://").path_join("../layout_v2.json").simplify_path()
	var txt := FileAccess.get_file_as_string(path)
	layout = JSON.parse_string(txt)
	if layout == null or layout.is_empty():
		push_error("barrow_v2: cannot read layout at " + path)
		return
	_build_environment()
	if layout.has("sculpt"):
		_build_terrain()
		_build_sculpt()
	if layout.has("models"):
		_build_models()
	else:
		_build_ground()
	_build_features()
	_build_stair()
	_build_labels()
	_build_walker()
	_build_camera()
	print("[bv2] built: %d features, floor %.1f m2, ppm %.4f (plate), ppm_gd %.4f" % [
		layout["features"].size(), float(layout["floor"]["area_m2"]), PPM_PLATE, ppm_gd()])


# ---------------------------------------------------------------- materials / meshes
func _mat(c: Color, unshaded := false) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = c
	m.roughness = 0.95
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	if unshaded:
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	return m


func _poly2(poly: Array) -> PackedVector2Array:
	var out := PackedVector2Array()
	for p in poly:
		out.append(Vector2(float(p[0]), float(p[1])))
	return out


func _uv(p: Vector2) -> Vector2:
	return Vector2((p.x - EXT["x0"]) / (EXT["x1"] - EXT["x0"]), (p.y - EXT["y0"]) / (EXT["y1"] - EXT["y0"]))


## A vertical prism over a sim-frame footprint, flat-shaded with explicit normals.
func _prism(poly: Array, z0: float, z1: float, mat: Material, uv_top := false, sides := true) -> MeshInstance3D:
	var p2 := _poly2(poly)
	var idx := Geometry2D.triangulate_polygon(p2)
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in idx:
		st.set_normal(Vector3.UP)
		if uv_top:
			st.set_uv(_uv(p2[i]))
		st.add_vertex(Vector3(p2[i].x, z1, p2[i].y))
	if sides and z1 - z0 > 0.001:
		var ccw := 0.0
		for i in p2.size():
			ccw += p2[i].x * p2[(i + 1) % p2.size()].y - p2[(i + 1) % p2.size()].x * p2[i].y
		for i in p2.size():
			var a := p2[i]
			var b := p2[(i + 1) % p2.size()]
			var e := (b - a).normalized()
			var n2 := Vector2(e.y, -e.x) if ccw > 0.0 else Vector2(-e.y, e.x)
			var n := Vector3(n2.x, 0.0, n2.y)
			for v in [Vector3(a.x, z0, a.y), Vector3(b.x, z0, b.y), Vector3(b.x, z1, b.y),
					Vector3(a.x, z0, a.y), Vector3(b.x, z1, b.y), Vector3(a.x, z1, a.y)]:
				st.set_normal(n)
				if uv_top:
					st.set_uv(_uv(Vector2(v.x, v.z)))
				st.add_vertex(v)
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = mat
	add_child(mi)
	return mi


# ---------------------------------------------------------------- the world
func _build_environment() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.20, 0.27, 0.34)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.86, 0.92)
	env.ambient_light_energy = 0.32
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -35.0, 0.0)
	sun.light_energy = 0.85
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 120.0
	add_child(sun)


func _build_ground() -> void:
	var img_path := ProjectSettings.globalize_path("res://data/ground_colour.png")
	var img := Image.load_from_file(img_path)
	var tex := ImageTexture.create_from_image(img)
	var gm := StandardMaterial3D.new()
	gm.albedo_texture = tex
	gm.roughness = 1.0
	gm.cull_mode = BaseMaterial3D.CULL_DISABLED
	gm.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	var foot := float(layout["land"]["z_cliff_foot_m"])
	# the sea, then the shore ice shelf, then the headland (its top textured; its sides are the cliff)
	var sea_z := float(layout["sea"]["z_m"])
	_prism([[-140, -140], [140, -140], [140, 140], [-140, 140]], sea_z, sea_z, _mat(Color(0.20, 0.27, 0.34)), false, false)
	_prism(layout["shore_ice"]["polygon"], float(layout["shore_ice"]["z_m"]) - 0.4, float(layout["shore_ice"]["z_m"]), gm, true)
	var land := _prism(layout["land"]["polygon"], foot, 0.0, gm, true)
	land.name = "Headland"
	# the cliff faces get their own colour: a second, untextured skirt 2 cm proud of the lip
	var lip: Array = layout["land"]["cliff_lip"]
	var cm := _mat(KIND_RGB["cliff"])
	for i in lip.size() - 1:
		var a := Vector2(float(lip[i][0]), float(lip[i][1]))
		var b := Vector2(float(lip[i + 1][0]), float(lip[i + 1][1]))
		var st := SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		var e := (b - a).normalized()
		var n := Vector3(-e.y, 0, e.x)
		for v in [Vector3(a.x, foot, a.y), Vector3(b.x, foot, b.y), Vector3(b.x, -0.05, b.y),
				Vector3(a.x, foot, a.y), Vector3(b.x, -0.05, b.y), Vector3(a.x, -0.05, a.y)]:
			st.set_normal(n)
			st.add_vertex(v + n * 0.02)
		var mi := MeshInstance3D.new()
		mi.mesh = st.commit()
		mi.material_override = cm
		add_child(mi)


func _build_features() -> void:
	for f in layout["features"]:
		if String(f.get("render", "prism")) == "sculpt":
			continue
		var kind: String = f["kind"]
		var col: Color = KIND_RGB.get(kind, Color(0.5, 0.5, 0.5))
		if kind == "mound":
			var s: Dictionary = f["shape"]
			var mi := MeshInstance3D.new()
			var sm := SphereMesh.new()
			sm.radius = 1.0
			sm.height = 2.0
			sm.radial_segments = 48
			sm.rings = 24
			mi.mesh = sm
			mi.material_override = _mat(col)
			mi.position = Vector3(float(s["centre"][0]), 0.0, float(s["centre"][1]))
			mi.rotation.y = -deg_to_rad(float(s["rot_deg"]))
			mi.scale = Vector3(float(s["semi_axes_m"][0]), float(s["rise_m"]), float(s["semi_axes_m"][1]))
			add_child(mi)
			continue
		if kind == "mast":
			var c := _centroid(f["footprint"])
			var mi2 := MeshInstance3D.new()
			var cy := CylinderMesh.new()
			cy.top_radius = 0.16
			cy.bottom_radius = 0.25
			cy.height = float(f["z_top_m"])
			mi2.mesh = cy
			mi2.material_override = _mat(col)
			mi2.position = Vector3(c.x, cy.height / 2.0, c.y)
			mi2.rotation_degrees = Vector3(0, 0, -14)
			add_child(mi2)
			continue
		_prism(f["footprint"], float(f["z_bottom_m"]), float(f["z_top_m"]), _mat(col))


# ---------------------------------------------------------------- R-C9-149a: the sculpted terrain + dressing
func _build_terrain() -> void:
	var hf: Dictionary = layout["sculpt"]["heightfield"]
	var path := ProjectSettings.globalize_path("res://").path_join("../" + String(hf["file"]).trim_prefix("godot/")).simplify_path()
	path = ProjectSettings.globalize_path("res://" + String(hf["file"]).trim_prefix("godot/"))
	var bytes := FileAccess.get_file_as_bytes(path)
	var H := bytes.to_float32_array()
	var rows: int = int(hf["shape"][0])
	var cols: int = int(hf["shape"][1])
	var ppm_h: float = float(hf["px_per_m"])
	var ex: Dictionary = hf["extent_sim_m"]
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	verts.resize(rows * cols)
	uvs.resize(rows * cols)
	for j in rows:
		for i in cols:
			var x := float(ex["x0"]) + float(i) / ppm_h
			var y := float(ex["y0"]) + float(j) / ppm_h
			verts[j * cols + i] = Vector3(x, H[j * cols + i], y)
			uvs[j * cols + i] = _uv(Vector2(x, y))
	var idx := PackedInt32Array()
	var sea_cut := float(layout["sea"]["z_m"]) - 0.2
	for j in rows - 1:
		for i in cols - 1:
			var a := j * cols + i
			var b := a + 1
			var c := a + cols
			var d := c + 1
			if H[a] < sea_cut and H[b] < sea_cut and H[c] < sea_cut and H[d] < sea_cut:
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
	var img := Image.load_from_file(ProjectSettings.globalize_path("res://data/ground_colour.png"))
	var gm := StandardMaterial3D.new()
	gm.albedo_texture = ImageTexture.create_from_image(img)
	gm.roughness = 1.0
	gm.cull_mode = BaseMaterial3D.CULL_DISABLED
	var mi := MeshInstance3D.new()
	mi.mesh = am
	mi.material_override = gm
	mi.name = "Terrain"
	add_child(mi)
	var sea_z := float(layout["sea"]["z_m"])
	var sm := _mat(Color(0.19, 0.26, 0.33))
	sm.roughness = 0.35
	_prism([[-140, -140], [140, -140], [140, 140], [-140, 140]], sea_z, sea_z, sm, false, false)


var _protos := {}
var _mats := {}


func _proto(kind: String, variant: int) -> Mesh:
	var key := "%s_%d" % [kind, variant]
	if _protos.has(key):
		return _protos[key]
	var m: Mesh
	if kind == "box":
		var bx := BoxMesh.new()
		bx.size = Vector3(2, 2, 2)
		m = bx
	else:
		var sp := SphereMesh.new()
		sp.radius = 1.0
		sp.height = 2.0
		var seg := {"rock": [7, 4], "slab": [8, 3], "crown": [8, 5], "blob": [14, 7], "tall": [6, 6]}
		var sg: Array = seg.get(kind, [10, 5])
		sp.radial_segments = sg[0]
		sp.rings = sg[1]
		var st := SurfaceTool.new()
		st.create_from(sp, 0)
		st.deindex()
		var arrs := st.commit_to_arrays()
		var vv: PackedVector3Array = arrs[Mesh.ARRAY_VERTEX]
		if kind != "blob":
			var r := RandomNumberGenerator.new()
			r.seed = 1000 + variant * 31 + kind.length()
			var jit := {}
			for i in vv.size():
				var k := "%.3f,%.3f,%.3f" % [vv[i].x, vv[i].y, vv[i].z]
				if not jit.has(k):
					jit[k] = 1.0 + r.randf_range(-0.22, 0.18)
				vv[i] = vv[i] * jit[k]
		var st2 := SurfaceTool.new()
		st2.begin(Mesh.PRIMITIVE_TRIANGLES)
		for i in vv.size():
			st2.add_vertex(vv[i])
		if kind == "blob":
			st2.index()
		st2.generate_normals()
		m = st2.commit()
	_protos[key] = m
	return m


func _cmat(rgb: Array) -> StandardMaterial3D:
	var key := "%.2f_%.2f_%.2f" % [snappedf(float(rgb[0]), 0.02), snappedf(float(rgb[1]), 0.02), snappedf(float(rgb[2]), 0.02)]
	if not _mats.has(key):
		_mats[key] = _mat(Color(float(rgb[0]), float(rgb[1]), float(rgb[2])))
	return _mats[key]


func _build_sculpt() -> void:
	var sc: Dictionary = layout["sculpt"]
	var n := 0
	for b in sc["blobs"]:
		var mi := MeshInstance3D.new()
		mi.mesh = _proto(String(b["proto"]), n % 6)
		mi.material_override = _cmat(b["rgb"])
		var r: Array = b["r"]
		var bas := Basis(Vector3.UP, -deg_to_rad(float(b["rot"]))).scaled(Vector3(float(r[0]), float(r[2]), float(r[1])))
		mi.transform = Transform3D(bas, Vector3(float(b["c"][0]), float(b["cz"]), float(b["c"][1])))
		add_child(mi)
		n += 1
	var unit_box := BoxMesh.new()
	unit_box.size = Vector3.ONE
	for bm in sc["beams"]:
		var a := Vector3(float(bm["a"][0]), float(bm["a"][2]), float(bm["a"][1]))
		var b := Vector3(float(bm["b"][0]), float(bm["b"][2]), float(bm["b"][1]))
		var dvec := b - a
		var ln := dvec.length()
		if ln < 0.01:
			continue
		var z := dvec / ln
		var x: Vector3
		if bm.has("xh"):
			x = Vector3(float(bm["xh"][0]), 0, float(bm["xh"][1]))
			x = (x - z * x.dot(z)).normalized()
		else:
			x = Vector3.UP.cross(z)
			x = Vector3.RIGHT if x.length() < 0.05 else x.normalized()
		var y := z.cross(x).normalized()
		var mi2 := MeshInstance3D.new()
		mi2.mesh = unit_box
		mi2.material_override = _cmat(bm["rgb"])
		mi2.transform = Transform3D(Basis(x * float(bm["w"]), y * float(bm["t"]), z * ln), (a + b) / 2.0)
		add_child(mi2)
	print("[bv2] sculpt: %d blobs, %d beams, %d prototypes, %d materials" % [sc["blobs"].size(), sc["beams"].size(), _protos.size(), _mats.size()])


# ---------------------------------------------------------------- R-C9-155: MODEL SLOTS (the v1 method)
var _glb_cache := {}
var model_report := {"loaded": 0, "placeholders": 0, "missing": []}


func _resolve(p: String) -> String:
	var bv2 := ProjectSettings.globalize_path("res://").path_join("..").simplify_path()
	if p.begins_with("runs/"):
		return bv2.path_join("../..").path_join(p.substr(5)).simplify_path()
	return bv2.path_join(p).simplify_path()


func _load_glb(p: String) -> Node3D:
	if p == "" or p == "<null>":
		return null
	var path := _resolve(p)
	if not FileAccess.file_exists(path):
		if not model_report["missing"].has(p):
			model_report["missing"].append(p)
		return null
	if not _glb_cache.has(path):
		var doc := GLTFDocument.new()
		var st := GLTFState.new()
		if doc.append_from_file(path, st) != OK:
			model_report["missing"].append(p + " (load failed)")
			return null
		_glb_cache[path] = doc.generate_scene(st)
	return (_glb_cache[path] as Node3D).duplicate()


func _aabb_of(n: Node, xf: Transform3D) -> AABB:
	var out := AABB()
	var first := true
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		var a := t * (n as MeshInstance3D).mesh.get_aabb()
		out = a
		first = false
	for ch in n.get_children():
		var b := _aabb_of(ch, t)
		if b.size == Vector3.ZERO:
			continue
		out = b if first else out.merge(b)
		first = false
	return out


func _place_box(model: Node3D, pos: Vector2, z: float, yaw_deg: float, size: Vector3) -> Node3D:
	# size = (w along local X, h, d along local Z); the model's AABB is fitted per axis, its base on z
	var ab := _aabb_of(model, Transform3D.IDENTITY.inverse() * model.transform.affine_inverse())
	var holder := Node3D.new()
	var sc := Vector3(size.x / maxf(ab.size.x, 1e-3), size.y / maxf(ab.size.y, 1e-3), size.z / maxf(ab.size.z, 1e-3))
	holder.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(yaw_deg)) * Basis.from_scale(sc), Vector3(pos.x, z, pos.y))
	model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
	holder.add_child(model)
	add_child(holder)
	return holder


func _place_beam(model: Node3D, a: Vector3, b: Vector3, th: float, fit_height := false) -> void:
	var ab := _aabb_of(model, model.transform.affine_inverse())
	var holder := Node3D.new()
	var d := b - a
	var ln := d.length()
	if fit_height:
		var s := ln / maxf(ab.size.y, 1e-3)
		holder.transform = Transform3D(Basis(Vector3.UP, randf() * TAU).scaled(Vector3(s, s, s)), a)
		model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
	else:
		var k := 0
		if ab.size.y > ab.size[k]:
			k = 1
		if ab.size.z > ab.size[k]:
			k = 2
		var z := d / maxf(ln, 1e-3)
		var x := Vector3.UP.cross(z)
		x = Vector3.RIGHT if x.length() < 0.05 else x.normalized()
		var y := z.cross(x).normalized()
		var axes := [x, y, z]
		var cols := [Vector3.ZERO, Vector3.ZERO, Vector3.ZERO]
		var others := [0, 1, 2]
		others.erase(k)
		cols[k] = z * (ln / maxf(ab.size[k], 1e-3))
		cols[others[0]] = x * (th / maxf(ab.size[others[0]], 1e-3))
		cols[others[1]] = y * (th / maxf(ab.size[others[1]], 1e-3))
		holder.transform = Transform3D(Basis(cols[0], cols[1], cols[2]), (a + b) / 2.0)
		model.position = -(ab.position + ab.size / 2.0)
	holder.add_child(model)
	add_child(holder)


const SLOT_RGB := {"building": Color(0.45, 0.33, 0.22, 0.6), "porch": Color(0.55, 0.38, 0.22, 0.6), "ruin": Color(0.30, 0.24, 0.20, 0.6),
	"portal": Color(0.5, 0.5, 0.48, 0.6), "wreck": Color(0.45, 0.32, 0.2, 0.6), "prop": Color(0.3, 0.25, 0.2, 0.7),
	"stones": Color(0.5, 0.5, 0.48, 0.7), "debris": Color(0.45, 0.36, 0.26, 0.7), "palisade": Color(0.4, 0.3, 0.2, 0.7),
	"grove": Color(0.8, 0.78, 0.72, 0.6)}


func _placeholder_box(sid: String, kind: String, pos: Vector2, z: float, yaw_deg: float, size: Vector3, opening: Dictionary) -> void:
	var m := StandardMaterial3D.new()
	m.albedo_color = SLOT_RGB.get(kind, Color(0.5, 0.5, 0.5, 0.6))
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	var holder := Node3D.new()
	holder.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(yaw_deg)), Vector3(pos.x, z, pos.y))
	var bx := BoxMesh.new()
	bx.size = size
	var mi := MeshInstance3D.new()
	mi.mesh = bx
	mi.material_override = m
	mi.position = Vector3(0, size.y / 2.0, 0)
	holder.add_child(mi)
	if opening.has("w") and opening.has("h"):
		var ob := BoxMesh.new()
		ob.size = Vector3(float(opening["w"]), float(opening["h"]), 0.15)
		var om := MeshInstance3D.new()
		om.mesh = ob
		om.material_override = _mat(Color(0.05, 0.04, 0.04), true)
		om.position = Vector3(0, float(opening["h"]) / 2.0, size.z / 2.0 + 0.05)
		holder.add_child(om)
	add_child(holder)
	model_report["placeholders"] += 1


func _slot_label(sid: String, pos: Vector2, h: float, status: String) -> void:
	var lb := Label3D.new()
	lb.text = "%s\n[%s]" % [sid, status.split(" ")[0]]
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lb.no_depth_test = true
	lb.fixed_size = true
	lb.pixel_size = 0.0007
	lb.font_size = 44
	lb.outline_size = 12
	lb.modulate = Color(0.1, 0.15, 0.35)
	lb.outline_modulate = Color(1, 1, 1, 0.85)
	lb.position = Vector3(pos.x, h + 0.6, pos.y)
	add_child(lb)
	labels.append(lb)


func _build_models() -> void:
	for m in layout["models"]:
		var sid: String = m["id"]
		var kind: String = m["kind"]
		var glb_slot: String = str(m.get("glb", ""))
		var insts: Array = m.get("instances", [])
		var pos := Vector2(float(m["pos"][0]), float(m["pos"][1]))
		var sz: Dictionary = m["size_m"]
		if insts.is_empty():
			var node := _load_glb(glb_slot)
			if node != null:
				_place_box(node, pos, float(m["z"]), float(m["godot_rot_y_deg"]), Vector3(float(sz["w_local_x"]), float(sz["h"]), float(sz["d_local_z"])))
				model_report["loaded"] += 1
			elif String(m.get("placeholder", "massing")) != "procedural":
				_placeholder_box(sid, kind, pos, float(m["z"]), float(m["godot_rot_y_deg"]),
					Vector3(float(sz["w_local_x"]), float(sz["h"]), float(sz["d_local_z"])), m.get("opening", {}))
		else:
			for ins in insts:
				var g: String = str(ins.get("glb", glb_slot))
				if String(ins["type"]) == "box":
					var ip := Vector2(float(ins["pos"][0]), float(ins["pos"][1]))
					var s3 := Vector3(float(ins["size_m"][0]), float(ins["size_m"][2]), float(ins["size_m"][1]))
					var node2 := _load_glb(g)
					if node2 != null:
						_place_box(node2, ip, float(ins["z"]), float(ins["godot_rot_y_deg"]), s3)
						model_report["loaded"] += 1
					elif String(m.get("placeholder", "massing")) != "procedural":
						_placeholder_box(sid, kind, ip, float(ins["z"]), float(ins["godot_rot_y_deg"]), s3, {})
				else:
					var a := Vector3(float(ins["a"][0]), float(ins["a"][2]), float(ins["a"][1]))
					var b := Vector3(float(ins["b"][0]), float(ins["b"][2]), float(ins["b"][1]))
					var node3 := _load_glb(g)
					if node3 != null:
						_place_beam(node3, a, b, float(ins["thickness_m"]), String(ins.get("fit", "")) == "height")
						model_report["loaded"] += 1
					else:
						var bm := BoxMesh.new()
						bm.size = Vector3.ONE
						var mi := MeshInstance3D.new()
						mi.mesh = bm
						mi.material_override = _mat(SLOT_RGB.get(kind, Color(0.5, 0.5, 0.5)))
						var zz := (b - a).normalized()
						var xx := Vector3.UP.cross(zz)
						xx = Vector3.RIGHT if xx.length() < 0.05 else xx.normalized()
						var yy := zz.cross(xx).normalized()
						var th := float(ins["thickness_m"])
						mi.transform = Transform3D(Basis(xx * th, yy * th, zz * (b - a).length()), (a + b) / 2.0)
						add_child(mi)
						model_report["placeholders"] += 1
		_slot_label(sid, pos, float(sz["h"]) + float(m["z"]), String(m["status"]))
	print("[bv2] models: %d GLB instances loaded, %d placeholders, missing %s" % [model_report["loaded"], model_report["placeholders"], str(model_report["missing"])])


func _centroid(poly: Array) -> Vector2:
	var c := Vector2.ZERO
	for p in poly:
		c += Vector2(float(p[0]), float(p[1]))
	return c / float(poly.size())


func _build_stair() -> void:
	var S: Dictionary = layout["stair"]
	var stone := _mat(Color(0.55, 0.53, 0.49))
	_prism(S["top_landing"]["polygon"], float(S["flight"]["z_bottom_m"]) - 0.3, 0.0, stone)
	_prism(S["bottom_landing"]["polygon"], float(S["flight"]["z_bottom_m"]) - 0.3, float(S["bottom_landing"]["z_m"]), stone)
	var fl: Array = S["flight"]["polygon"]   # W_top, E_top, E_foot, W_foot
	var top_mid := (Vector2(float(fl[0][0]), float(fl[0][1])) + Vector2(float(fl[1][0]), float(fl[1][1]))) / 2.0
	var foot_mid := (Vector2(float(fl[3][0]), float(fl[3][1])) + Vector2(float(fl[2][0]), float(fl[2][1]))) / 2.0
	var d2 := (foot_mid - top_mid).normalized()
	var along := Vector3(d2.x, 0, d2.y)
	var across := Vector3.UP.cross(along)
	var n: int = int(S["flight"]["n_steps"])
	var rise := float(S["flight"]["step_rise_m"])
	var tread := float(S["flight"]["step_tread_m"])
	var w := float(S["width_m"])
	var z_bot := float(S["flight"]["z_bottom_m"]) - 0.3
	# R-C9-149a: a ROUGH-CUT rock stair -- still straight and 3 m wide, but every tread is its own hewn
	# block (width, set-back, tilt and tone jittered a little); the walkable ramp under the nosings is unchanged.
	var rng := RandomNumberGenerator.new()
	rng.seed = 149
	for k in n:
		var top_z := -float(k + 1) * rise + rng.randf_range(-0.025, 0.02)
		var h := top_z - z_bot
		var bm := BoxMesh.new()
		bm.size = Vector3(w + rng.randf_range(-0.25, 0.05), h, tread + rng.randf_range(0.0, 0.06))
		var mi := MeshInstance3D.new()
		mi.mesh = bm
		var tone := rng.randf_range(-0.05, 0.05)
		mi.material_override = _mat(Color(0.56 + tone, 0.53 + tone, 0.48 + tone))
		var c2 := top_mid + d2 * (tread * (float(k) + 0.5))
		var off := Vector3(across.x, 0, across.z) * rng.randf_range(-0.08, 0.08)
		var bas := Basis(across, Vector3.UP, along).rotated(Vector3.UP, deg_to_rad(rng.randf_range(-2.5, 2.5)))
		mi.transform = Transform3D(bas, Vector3(c2.x, z_bot + h / 2.0, c2.y) + off)
		add_child(mi)


func _build_labels() -> void:
	for a in layout["anchors"]["points"]:
		var lb := Label3D.new()
		lb.text = "%s  %s" % [a["id"], String(a["delivered_by"]).split(" (")[0]]
		lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		lb.no_depth_test = true
		lb.fixed_size = true
		lb.pixel_size = 0.0009
		lb.font_size = 64
		lb.outline_size = 16
		lb.modulate = Color(0.25, 0.12, 0.0)
		lb.outline_modulate = Color(1, 1, 1, 0.85)
		lb.position = Vector3(float(a["x"]), 0.2, float(a["y"]))
		add_child(lb)
		labels.append(lb)
		var dot := MeshInstance3D.new()
		var cy := CylinderMesh.new()
		cy.top_radius = 0.25
		cy.bottom_radius = 0.25
		cy.height = 0.02
		dot.mesh = cy
		dot.material_override = _mat(Color(0.55, 0.30, 0.05), true)
		dot.position = Vector3(float(a["x"]), 0.011, float(a["y"]))
		add_child(dot)
	var start := MeshInstance3D.new()
	var sc := CylinderMesh.new()
	sc.top_radius = 0.35
	sc.bottom_radius = 0.35
	sc.height = 0.02
	start.mesh = sc
	start.material_override = _mat(Color(0.1, 0.1, 0.1), true)
	start.position = Vector3(0, 0.011, 0)
	add_child(start)


func _build_walker() -> void:
	walker = Node3D.new()
	var mi := MeshInstance3D.new()
	var cap := CapsuleMesh.new()
	cap.radius = 0.32
	cap.height = H_FIG_M
	mi.mesh = cap
	mi.material_override = _mat(Color(0.60, 0.59, 0.57))
	mi.position = Vector3(0, H_FIG_M / 2.0, 0)
	walker.add_child(mi)
	var nose := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(0.18, 0.18, 0.4)
	nose.mesh = bm
	nose.material_override = _mat(Color(0.3, 0.3, 0.3))
	nose.position = Vector3(0, 1.55, -0.35)
	walker.add_child(nose)
	add_child(walker)


func _build_camera() -> void:
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.rotation_degrees = Vector3(-ALPHA_DEG, 0.0, 0.0)
	cam.near = 0.5
	cam.far = 400.0
	add_child(cam)
	cam.make_current()
	set_zoom(false)
	place_camera(Vector2.ZERO)


func set_zoom(gd: bool) -> void:
	zoom_gd = gd
	ppm = ppm_gd() if gd else PPM_PLATE
	cam.size = VIEW_H / ppm     # size is fixed in METRES of the 1080-row frame: the window is resolution-free


## Centre the view on a sim-frame ground point (zero yaw: the camera sits due south and above).
func place_camera(t: Vector2) -> void:
	cam_target = t
	var a := deg_to_rad(ALPHA_DEG)
	var dist := 150.0
	cam.position = Vector3(t.x, 0.0, t.y) + Vector3(0.0, sin(a), cos(a)) * dist


func set_walker(p: Vector2, heading: Vector2 = Vector2.ZERO) -> void:
	walker.position = Vector3(p.x, 0.0, p.y)
	if heading.length() > 0.001:
		walker.rotation.y = atan2(-heading.x, -heading.y)


func _unhandled_input(ev: InputEvent) -> void:
	if ev is InputEventKey and ev.pressed and not ev.echo:
		if ev.keycode == KEY_Z:
			set_zoom(not zoom_gd)
		elif ev.keycode == KEY_L:
			for lb in labels:
				lb.visible = not lb.visible


func _process(delta: float) -> void:
	if free_cam or walker == null:
		return
	var v := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		v.x -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		v.x += 1
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		v.y -= 1
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		v.y += 1
	if v.length() > 0:
		v = v.normalized() * (9.0 if Input.is_key_pressed(KEY_SHIFT) else 6.0)
		var p := Vector2(walker.position.x, walker.position.z) + v * delta
		set_walker(p, v)
	place_camera(Vector2(walker.position.x, walker.position.z))
