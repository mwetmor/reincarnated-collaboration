extends "res://scripts/barrow_v2_greybox.gd"
## barrow_v2 TRUE-3D, SECTION SW proof (R-C9-158, lane BS, drax).
##
## The BX blockout everywhere, EXCEPT inside the section box (data/section_sw/section.json, built by
## tools/section_sw_build.py), where the stepped heightfield gives way to a real coast built from the model kit:
## a chained cliff of cliffplain faces with bites and spurs, the layout's cave cliff and stair cliff, a rock spit,
## a shingle beach with the wreck on it, a lagoon of fast ice with dark leads and pressure ridges, sea floes off
## the cliff, a frozen stream, cairns, standing stones, driftwood, pebbles, rust heather and dry grass.
##
## TWO LOOKS (paint_mode):
##   "guide"   plain lit, every model in its own texture -- the render the painter paints over (v1 method);
##   "painted" THE PAINTING IS THE WORLD (barrow_full PaintedWorld, ported to zero yaw): every static surface
##             wears the stitched paint-over through the fixed camera -- a fragment's painting pixel is analytic:
##                 px = (x - sx0) * ppm ;  py = (sin(a) * z_sim - cos(a) * h - sy0) * ppm
##             unlit (the painting is the light), times ONE term: the hero's shadow, in the painter's shadow colour
##             (a paint sun lights only the painted layer and only the hero casts for it). The hero keeps the
##             real sun and the ambient.

const LAYER_PAINTED := 1 << 10
const LAYER_HERO := 1 << 1
var paint_mode := "guide"
var paint_path := ""
var sec: Dictionary = {}
var hero: Node3D
var hero_anim: AnimationPlayer
var static_root: Node3D
var _sun_a: DirectionalLight3D
var _sun_b: DirectionalLight3D

const PAINT_SHADER := """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_disabled, fog_disabled;
uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform vec4 frame = vec4(-57.5, -4.0, 100.617553710938, 0.0);   // sx0, sy0 (metres of screen), ppm
uniform vec2 size_px = vec2(7936.0, 4864.0);
uniform vec2 sc = vec2(0.798, 0.6026);                            // sin(pitch), cos(pitch)
uniform vec3 outside = vec3(0.93, 0.94, 0.96);
uniform vec3 shadow_mul = vec3(0.42, 0.48, 0.66);
varying vec3 w;
void vertex() { w = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	vec2 uv = vec2((w.x - frame.x) * frame.z, (sc.x * w.z - sc.y * w.y - frame.y) * frame.z) / size_px;
	bool inside = uv.x >= 0.0 && uv.y >= 0.0 && uv.x <= 1.0 && uv.y <= 1.0;
	ALBEDO = inside ? texture(paint_tex, uv).rgb : outside;
}
void light() {
	DIFFUSE_LIGHT += mix(vec3(1.0), shadow_mul, clamp(1.0 - ATTENUATION, 0.0, 1.0));
}
"""


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("paint="):
			paint_mode = "painted"
			paint_path = a.substr(6)
	layout = JSON.parse_string(FileAccess.get_file_as_string(ProjectSettings.globalize_path("res://").path_join("../layout_v2.json").simplify_path()))
	sec = JSON.parse_string(FileAccess.get_file_as_string(ProjectSettings.globalize_path("res://data/section_sw/section.json")))
	static_root = Node3D.new()
	static_root.name = "Static"
	add_child(static_root)
	_build_env2()
	# the BX blockout, minus what the section rebuilds (in memory only; layout_v2.json is untouched)
	var skip: Array = sec["skip_models"]
	var keep_models := []
	for m in layout["models"]:
		if not skip.has(m["id"]):
			keep_models.append(m)
	layout["models"] = keep_models
	var bx: Dictionary = sec["box"]
	var kinds: Array = sec["skip_blob_kinds_in_box"]
	var keep_blobs := []
	for b in layout["sculpt"]["blobs"]:
		var c: Array = b["c"]
		var inb := float(c[0]) > float(bx["x0"]) and float(c[0]) < float(bx["x1"]) and float(c[1]) > float(bx["y0"]) and float(c[1]) < float(bx["y1"])
		if inb and kinds.has(String(b["k"])):
			continue
		if String(b["k"]) == "ripple":
			continue
		keep_blobs.append(b)
	layout["sculpt"]["blobs"] = keep_blobs
	_build_terrain_cut()
	_build_section_terrain()
	_build_sculpt()
	_build_models()
	_build_features()
	_build_stair_ledge()
	_build_section()
	# everything built so far is the static world: move it under static_root
	for ch in get_children():
		if ch == static_root or ch is WorldEnvironment or ch is DirectionalLight3D:
			continue
		ch.reparent(static_root)
	_build_hero()
	_build_camera()
	if paint_mode == "painted":
		_apply_paint()
	print("[sw] built: mode %s; models %d loaded, missing %s" % [paint_mode, model_report["loaded"], str(model_report["missing"])])


func _build_env2() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.12, 0.17, 0.23)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.86, 0.92)
	env.ambient_light_energy = 0.32
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR if paint_mode == "painted" else Environment.TONE_MAPPER_FILMIC
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	_sun_a = DirectionalLight3D.new()
	_sun_a.rotation_degrees = Vector3(-48.0, -35.0, 0.0)
	_sun_a.light_energy = 0.85
	_sun_a.shadow_enabled = true
	_sun_a.directional_shadow_max_distance = 120.0
	add_child(_sun_a)
	if paint_mode == "painted":
		_sun_a.light_energy = 1.05
		_sun_a.light_cull_mask = 0xFFFFF & ~LAYER_PAINTED
		_sun_b = DirectionalLight3D.new()
		_sun_b.rotation_degrees = _sun_a.rotation_degrees
		_sun_b.light_cull_mask = LAYER_PAINTED
		_sun_b.shadow_enabled = true
		_sun_b.shadow_caster_mask = LAYER_HERO
		_sun_b.directional_shadow_max_distance = 60.0
		add_child(_sun_b)


# ---------------------------------------------------------------- terrain: BX outside the box, the section inside
func _hf_mesh(H: PackedFloat32Array, rows: int, cols: int, x0: float, y0: float, ppm_h: float, cut: Dictionary, tex_img: Image, uvf: Callable) -> MeshInstance3D:
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	verts.resize(rows * cols)
	uvs.resize(rows * cols)
	for j in rows:
		for i in cols:
			var x := x0 + float(i) / ppm_h
			var y := y0 + float(j) / ppm_h
			verts[j * cols + i] = Vector3(x, H[j * cols + i], y)
			uvs[j * cols + i] = uvf.call(Vector2(x, y))
	var idx := PackedInt32Array()
	var sea_cut := float(layout["sea"]["z_m"]) - 0.6
	for j in rows - 1:
		for i in cols - 1:
			var a := j * cols + i
			var b := a + 1
			var c := a + cols
			var d := c + 1
			if H[a] < sea_cut and H[b] < sea_cut and H[c] < sea_cut and H[d] < sea_cut:
				continue
			if not cut.is_empty():
				var xa := x0 + float(i) / ppm_h
				var ya := y0 + float(j) / ppm_h
				var xb := xa + 1.0 / ppm_h
				var yb := ya + 1.0 / ppm_h
				if xa >= float(cut["x0"]) and xb <= float(cut["x1"]) and ya >= float(cut["y0"]) and yb <= float(cut["y1"]):
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
	var gm := StandardMaterial3D.new()
	gm.albedo_texture = ImageTexture.create_from_image(tex_img)
	gm.roughness = 1.0
	gm.cull_mode = BaseMaterial3D.CULL_DISABLED
	var mi := MeshInstance3D.new()
	mi.mesh = am
	mi.material_override = gm
	add_child(mi)
	return mi


func _build_terrain_cut() -> void:
	var hf: Dictionary = layout["sculpt"]["heightfield"]
	var H := FileAccess.get_file_as_bytes(ProjectSettings.globalize_path("res://" + String(hf["file"]).trim_prefix("godot/"))).to_float32_array()
	var ex: Dictionary = hf["extent_sim_m"]
	var img := Image.load_from_file(ProjectSettings.globalize_path("res://data/ground_colour.png"))
	var bx: Dictionary = sec["box"]
	var cut := {"x0": float(bx["x0"]) + 0.01, "x1": float(bx["x1"]) - 0.01, "y0": float(bx["y0"]) + 0.01, "y1": float(bx["y1"]) - 0.01}
	var mi := _hf_mesh(H, int(hf["shape"][0]), int(hf["shape"][1]), float(ex["x0"]), float(ex["y0"]), float(hf["px_per_m"]), cut, img, _uv)
	mi.name = "TerrainBX"
	var sea_z := float(layout["sea"]["z_m"])
	var sm := _mat(Color(0.11, 0.17, 0.23))
	sm.roughness = 0.35
	_prism([[-160, -160], [160, -160], [160, 160], [-160, 160]], sea_z, sea_z, sm, false, false).name = "Sea"


func _build_section_terrain() -> void:
	var t: Dictionary = sec["terrain"]
	var H := FileAccess.get_file_as_bytes(ProjectSettings.globalize_path("res://" + String(t["file"]))).to_float32_array()
	var bx: Dictionary = sec["box"]
	var img := Image.load_from_file(ProjectSettings.globalize_path("res://" + String(sec["ground"]["file"])))
	var x0 := float(bx["x0"])
	var y0 := float(bx["y0"])
	var wx := float(bx["x1"]) - x0
	var wy := float(bx["y1"]) - y0
	var uvf := func(p: Vector2) -> Vector2: return Vector2((p.x - x0) / wx, (p.y - y0) / wy)
	var mi := _hf_mesh(H, int(t["shape"][0]), int(t["shape"][1]), x0, y0, float(t["px_per_m"]), {}, img, uvf)
	mi.name = "TerrainSection"


# the stair cliff (a Tripo model) carries its own carved flight and the terrain carries the flush top landing: only
# the BX bottom landing (the cave's sea-level ledge) is built here
func _build_stair_ledge() -> void:
	var S: Dictionary = layout["stair"]
	_prism(S["bottom_landing"]["polygon"], float(S["flight"]["z_bottom_m"]) - 0.6, float(S["bottom_landing"]["z_m"]), _mat(Color(0.50, 0.48, 0.45)))


# ---------------------------------------------------------------- the section's coast, ice and detail
func _vcol_mat() -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.vertex_color_use_as_albedo = true
	m.roughness = 0.9
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m


func _build_section() -> void:
	var I: Dictionary = sec["instances"]
	var G: Dictionary = sec["glb"]
	for kind in ["cliff", "crag", "cairn", "stone_tall", "stone_mid"]:
		for it in I[kind]:
			var node := _load_glb(String(G[kind]))
			if node == null:
				continue
			var sz: Array = it["size"]
			var h := _place_box(node, Vector2(float(it["pos"][0]), float(it["pos"][1])), float(it["z"]), float(it["yaw"]), Vector3(float(sz[0]), float(sz[1]), float(sz[2])))
			if it.has("lean"):
				h.rotate_object_local(Vector3.RIGHT, deg_to_rad(float(it["lean"])))
			model_report["loaded"] += 1
	for it in I["log"]:
		var node2 := _load_glb(String(G["log"]))
		if node2 == null:
			continue
		var a: Array = it["a"]
		var b: Array = it["b"]
		_place_beam(node2, Vector3(float(a[0]), float(a[2]), float(a[1])), Vector3(float(b[0]), float(b[2]), float(b[1])), float(it["th"]))
		model_report["loaded"] += 1
	_build_lagoon_water()
	_build_floes()
	_build_ridges()
	_build_scatter()
	_build_stream()


func _build_lagoon_water() -> void:
	# the lagoon's water (LAG_Z), bounded on the south by the spit's centreline (the spit's ridge hides its edge)
	var A := Vector2(-41.5, 26.8)
	var D := Vector2(-0.94, 0.34)
	var poly := [[-80, -14], [-27, -14], [A.x + D.x * -14.0, A.y + D.y * -14.0], [A.x + D.x * 42.0, A.y + D.y * 42.0]]
	var m := _mat(Color(0.10, 0.16, 0.22))
	m.roughness = 0.3
	_prism(poly, -1.30, -1.30, m, false, false).name = "LagoonWater"


func _build_floes() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for f in sec["floes"]:
		var p2 := PackedVector2Array()
		for q in f["poly"]:
			p2.append(Vector2(float(q[0]), float(q[1])))
		var tri := Geometry2D.triangulate_polygon(p2)
		if tri.is_empty():
			continue
		var top := float(f["top"])
		var bot := float(f["bot"])
		var sn := float(f["snow"])
		var ctop := Color(0.80, 0.88, 0.95).lerp(Color(0.95, 0.96, 0.98), sn)
		var cside := Color(0.52, 0.68, 0.80)
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
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = _vcol_mat()
	mi.name = "Floes"
	add_child(mi)


func _mm(mesh: Mesh, n: int) -> MultiMeshInstance3D:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	mm.mesh = mesh
	mm.instance_count = n
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	var m := _vcol_mat()
	mmi.material_override = m
	add_child(mmi)
	return mmi


func _rock_mesh(seg: int, rings: int, seed: int) -> Mesh:
	var sp := SphereMesh.new()
	sp.radius = 1.0
	sp.height = 2.0
	sp.radial_segments = seg
	sp.rings = rings
	var st := SurfaceTool.new()
	st.create_from(sp, 0)
	st.deindex()
	var arrs := st.commit_to_arrays()
	var vv: PackedVector3Array = arrs[Mesh.ARRAY_VERTEX]
	var r := RandomNumberGenerator.new()
	r.seed = seed
	var jit := {}
	for i in vv.size():
		var k := "%.3f,%.3f,%.3f" % [vv[i].x, vv[i].y, vv[i].z]
		if not jit.has(k):
			jit[k] = 1.0 + r.randf_range(-0.2, 0.15)
		vv[i] = vv[i] * jit[k]
	var st2 := SurfaceTool.new()
	st2.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in vv.size():
		st2.add_vertex(vv[i])
	st2.generate_normals()
	return st2.commit()


func _build_ridges() -> void:
	var R: Array = sec["ridges"]
	var bm := BoxMesh.new()
	bm.size = Vector3.ONE
	var mmi := _mm(bm, R.size())
	mmi.name = "PressureRidges"
	for i in R.size():
		var r: Dictionary = R[i]
		var s: Array = r["size"]
		var ro: Array = r["rot"]
		var bas := Basis.from_euler(Vector3(deg_to_rad(float(ro[0])), deg_to_rad(float(ro[1])), deg_to_rad(float(ro[2])))).scaled_local(Vector3(float(s[0]), float(s[1]), float(s[2])))
		mmi.multimesh.set_instance_transform(i, Transform3D(bas, Vector3(float(r["pos"][0]), float(r["z"]), float(r["pos"][1]))))
		mmi.multimesh.set_instance_color(i, Color(0.78, 0.87, 0.94).lerp(Color(0.93, 0.95, 0.98), float(i % 5) / 4.0))


func _build_scatter() -> void:
	var P: Array = sec["pebbles"]
	var mmi := _mm(_rock_mesh(7, 4, 5), P.size())
	mmi.name = "Shingle"
	var pal := [Color(0.50, 0.49, 0.47), Color(0.42, 0.40, 0.38), Color(0.60, 0.58, 0.55), Color(0.47, 0.42, 0.37), Color(0.36, 0.35, 0.35)]
	for i in P.size():
		var p: Array = P[i]
		var r := float(p[3])
		var bas := Basis(Vector3.UP, deg_to_rad(float(p[4]))).scaled(Vector3(r * 1.3, r * 0.55, r))
		mmi.multimesh.set_instance_transform(i, Transform3D(bas, Vector3(float(p[0]), float(p[2]) + r * 0.15, float(p[1]))))
		mmi.multimesh.set_instance_color(i, pal[int(float(p[5]) * 4.99)])
	var Hh: Array = sec["heather"]
	var mh := _mm(_rock_mesh(9, 5, 9), Hh.size())
	mh.name = "Heather"
	var hp := [Color(0.48, 0.24, 0.14), Color(0.56, 0.31, 0.17), Color(0.40, 0.22, 0.15), Color(0.60, 0.40, 0.24)]
	for i in Hh.size():
		var h: Array = Hh[i]
		var r2 := float(h[3])
		var b2 := Basis(Vector3.UP, float(i) * 1.7).scaled(Vector3(r2 * 1.2, r2 * 0.45, r2))
		mh.multimesh.set_instance_transform(i, Transform3D(b2, Vector3(float(h[0]), float(h[2]) + r2 * 0.2, float(h[1]))))
		mh.multimesh.set_instance_color(i, hp[int(float(h[4]) * 3.99)])
	var Bb: Array = sec.get("brash", [])
	var mb := _mm(_rock_mesh(6, 3, 21), Bb.size())
	mb.name = "Brash"
	for i in Bb.size():
		var q: Array = Bb[i]
		var r3 := float(q[3])
		mb.multimesh.set_instance_transform(i, Transform3D(Basis(Vector3.UP, deg_to_rad(float(q[4]))).scaled(Vector3(r3 * 1.2, 0.12, r3)), Vector3(float(q[0]), float(q[2]), float(q[1]))))
		mb.multimesh.set_instance_color(i, Color(0.86, 0.91, 0.96))
	var Gg: Array = sec["grass"]
	var blades := 0
	for g in Gg:
		blades += int(g[4])
	var cone := CylinderMesh.new()
	cone.top_radius = 0.0
	cone.bottom_radius = 0.035
	cone.height = 1.0
	cone.radial_segments = 4
	cone.rings = 1
	var mg := _mm(cone, blades)
	mg.name = "DryGrass"
	var rr := RandomNumberGenerator.new()
	rr.seed = 158
	var k := 0
	for g in Gg:
		for j in int(g[4]):
			var hh := float(g[3]) * rr.randf_range(0.6, 1.1)
			var tilt := Basis(Vector3.UP, rr.randf() * TAU) * Basis(Vector3.RIGHT, rr.randf_range(0.1, 0.45))
			var off := Vector3(rr.randf_range(-0.12, 0.12), 0, rr.randf_range(-0.12, 0.12))
			var base := Vector3(float(g[0]), float(g[2]), float(g[1])) + off
			var bas3 := tilt.scaled_local(Vector3(1.0, hh, 1.0))
			mg.multimesh.set_instance_transform(k, Transform3D(bas3, base + tilt * Vector3(0, hh * 0.5, 0)))
			mg.multimesh.set_instance_color(k, Color(0.80, 0.66, 0.40).lerp(Color(0.66, 0.52, 0.30), rr.randf()))
			k += 1


func _build_stream() -> void:
	var R: Array = sec["stream"]["ribbon"]
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in R.size() - 1:
		var a := Vector3(float(R[i][0]), float(R[i][2]), float(R[i][1]))
		var b := Vector3(float(R[i + 1][0]), float(R[i + 1][2]), float(R[i + 1][1]))
		var d := (b - a)
		d.y = 0
		d = d.normalized()
		var s := Vector3(-d.z, 0, d.x)
		var wa := float(R[i][3]) * 0.5
		var wb := float(R[i + 1][3]) * 0.5
		var ca := Color(0.64, 0.78, 0.90)
		for v in [a - s * wa, b - s * wb, b + s * wb, a - s * wa, b + s * wb, a + s * wa]:
			st.set_color(ca)
			st.set_normal(Vector3.UP)
			st.add_vertex(v)
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = _vcol_mat()
	mi.name = "Stream"
	add_child(mi)


# ---------------------------------------------------------------- the hero (the v1 Barrow's warlord body)
func _build_hero() -> void:
	var path := _resolve("runs/C-9/barrow_full/godot/models/warlord/wl_body.glb")
	var doc := GLTFDocument.new()
	var st := GLTFState.new()
	if doc.append_from_file(path, st) != OK:
		push_error("hero load failed")
		return
	var rig: Node3D = doc.generate_scene(st)
	hero = Node3D.new()
	hero.name = "Hero"
	add_child(hero)
	hero.add_child(rig)
	# a skinned mesh's AABB is its bind data, not the posed body: measure the SKELETON's rest pose instead
	var sk := _find_skel(rig)
	var lo := 1e9
	var hi := -1e9
	if sk != null:
		var to_rig := Transform3D.IDENTITY
		var n: Node = sk
		while n != rig and n != null:
			if n is Node3D:
				to_rig = (n as Node3D).transform * to_rig
			n = n.get_parent()
		for i in sk.get_bone_count():
			var y := (to_rig * sk.get_bone_global_rest(i).origin).y
			lo = minf(lo, y)
			hi = maxf(hi, y)
	var tall := (hi - lo) * 1.1 if hi > lo else 1.9
	var s := 1.9 / maxf(tall, 0.01)
	rig.scale = Vector3.ONE * s
	rig.position = Vector3(0, -lo * s if hi > lo else 0.0, 0)
	print("[sw] hero rest height %.3f -> scale %.4f" % [tall, s])
	_set_layers(hero, LAYER_HERO)
	hero_anim = _find_anim(rig)
	if hero_anim != null:
		for n in ["run", "walk"]:
			if hero_anim.has_animation(n):
				hero_anim.get_animation(n).loop_mode = Animation.LOOP_LINEAR
		hero_anim.play("idle" if hero_anim.has_animation("idle") else hero_anim.get_animation_list()[0])
	hero.visible = false


func _find_skel(n: Node) -> Skeleton3D:
	if n is Skeleton3D:
		return n
	for c in n.get_children():
		var r := _find_skel(c)
		if r != null:
			return r
	return null


func _find_anim(n: Node) -> AnimationPlayer:
	if n is AnimationPlayer:
		return n
	for c in n.get_children():
		var r := _find_anim(c)
		if r != null:
			return r
	return null


func _set_layers(n: Node, bits: int) -> void:
	if n is VisualInstance3D:
		(n as VisualInstance3D).layers = bits
	for c in n.get_children():
		_set_layers(c, bits)


func set_hero(p: Vector2, heading: Vector2, anim: String) -> void:
	if hero == null:
		return
	hero.visible = true
	hero.position = Vector3(p.x, 0.0, p.y)
	if heading.length() > 0.001:
		hero.rotation.y = atan2(heading.x, heading.y)
	if hero_anim != null and hero_anim.has_animation(anim) and hero_anim.current_animation != anim:
		hero_anim.play(anim)


# ---------------------------------------------------------------- the painting worn by the world
func _apply_paint() -> void:
	var img := Image.load_from_file(paint_path)
	img.generate_mipmaps()
	var tex := ImageTexture.create_from_image(img)
	var sh := Shader.new()
	sh.code = PAINT_SHADER
	var m := ShaderMaterial.new()
	m.shader = sh
	var F: Dictionary = sec["frame"]
	var a := deg_to_rad(float(F["pitch_deg"]))
	m.set_shader_parameter("paint_tex", tex)
	m.set_shader_parameter("frame", Vector4(float(F["sx0_m"]), float(F["sy0_m"]), float(F["ppm"]), 0.0))
	m.set_shader_parameter("size_px", Vector2(float(F["size_px"][0]), float(F["size_px"][1])))
	m.set_shader_parameter("sc", Vector2(sin(a), cos(a)))
	_paint_all(static_root, m)


func _paint_all(n: Node, m: Material) -> void:
	if n is GeometryInstance3D:
		(n as GeometryInstance3D).material_override = m
		(n as VisualInstance3D).layers = LAYER_PAINTED
	for c in n.get_children():
		_paint_all(c, m)


func _process(_delta: float) -> void:
	pass
