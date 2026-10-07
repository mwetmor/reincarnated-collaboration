extends SceneTree
## BV2F LV 0.2 -- play-camera frame proof. Markers only, unpainted, unlit.
## Builds layout_v2's anchors + floor + key features in v1's world through frame.gd (the twin), and renders them
## through v1's OWN camera law (barrow_full.gd:_build_camera: orthographic, pitch 52.95354, yaw 47, look_at).
##   godot --path fid/lv/godot --resolution 1600x1400 --script frame_render.gd -- <layout_v2.json> <out_dir> <yaw_deg> <tag>
## yaw_deg 47 = the fix; 0 = R-C9-159 (site unrotated, camera at 47) as the negative control.

const F := preload("res://frame.gd")
const STANDOFF := 200.0
var L := {}
var out_dir := ""
var yaw := 47.0
var tag := "fixed"
var cam: Camera3D
var frames := 0
var mats := {}


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	L = JSON.parse_string(FileAccess.get_file_as_string(a[0]))
	out_dir = a[1]
	yaw = float(a[2])
	tag = a[3]
	var we := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.10, 0.11, 0.13)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	we.environment = env
	root.add_child(we)
	_build()
	_camera()


func W(x: float, y: float, z: float = 0.0) -> Vector3:
	return F.sim_to_world(x, y, z, yaw)


func _mat(c: Color) -> StandardMaterial3D:
	var k := c.to_html()
	if not mats.has(k):
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.albedo_color = c
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		if c.a < 1.0:
			m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mats[k] = m
	return mats[k]


func _pts(arr) -> PackedVector2Array:
	var p := PackedVector2Array()
	for q in arr:
		p.append(Vector2(float(q[0]), float(q[1])))
	return p


func _fill(poly: PackedVector2Array, z: float, c: Color, nm: String) -> void:
	var idx := Geometry2D.triangulate_polygon(poly)
	if idx.is_empty():
		push_warning("triangulate failed: " + nm)
		return
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in idx:
		st.add_vertex(W(poly[i].x, poly[i].y, z))
	var mi := MeshInstance3D.new()
	mi.name = nm
	mi.mesh = st.commit()
	mi.material_override = _mat(c)
	root.add_child(mi)


func _ribbon(pl: PackedVector2Array, wid: float, z: float, c: Color, closed := false) -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var n := pl.size()
	var segs := n if closed else n - 1
	for i in segs:
		var a := pl[i]
		var b := pl[(i + 1) % n]
		var d := (b - a)
		if d.length() < 1e-6:
			continue
		var nn := Vector2(-d.y, d.x).normalized() * wid * 0.5
		var v := [W(a.x + nn.x, a.y + nn.y, z), W(b.x + nn.x, b.y + nn.y, z), W(b.x - nn.x, b.y - nn.y, z), W(a.x - nn.x, a.y - nn.y, z)]
		for k in [0, 1, 2, 0, 2, 3]:
			st.add_vertex(v[k])
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = _mat(c)
	root.add_child(mi)


func _prism(poly: PackedVector2Array, z0: float, z1: float, c: Color, nm: String) -> void:
	_fill(poly, z1, c, nm + "_top")
	var dark := c.darkened(0.35)
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var n := poly.size()
	for i in n:
		var a := poly[i]
		var b := poly[(i + 1) % n]
		var v := [W(a.x, a.y, z0), W(b.x, b.y, z0), W(b.x, b.y, z1), W(a.x, a.y, z1)]
		for k in [0, 1, 2, 0, 2, 3]:
			st.add_vertex(v[k])
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = _mat(dark)
	root.add_child(mi)


func _label(txt: String, x: float, y: float, z: float, c: Color, size := 96) -> void:
	var l := Label3D.new()
	l.text = txt
	l.position = W(x, y, z)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	l.fixed_size = false
	l.pixel_size = 0.03
	l.font_size = size
	l.outline_size = 18
	l.modulate = c
	l.outline_modulate = Color(0, 0, 0)
	root.add_child(l)


func _arrow(cx: float, cy: float, compass_deg: float, length: float, c: Color, z := 0.3) -> void:
	# compass = atan2(x, -y) (layout frame): direction (sin, -cos)
	var t := deg_to_rad(compass_deg)
	var d := Vector2(sin(t), -cos(t))
	var a := Vector2(cx, cy)
	var b := a + d * length
	_ribbon(PackedVector2Array([a, b]), 0.9, z, c)
	var s := Vector2(-d.y, d.x)
	_ribbon(PackedVector2Array([b, b - d * 3.0 + s * 2.2]), 0.9, z, c)
	_ribbon(PackedVector2Array([b, b - d * 3.0 - s * 2.2]), 0.9, z, c)


func _centroid(poly: PackedVector2Array) -> Vector2:
	var s := Vector2.ZERO
	for p in poly:
		s += p
	return s / max(1, poly.size())


func _feat(id: String) -> Dictionary:
	for f in L["features"]:
		if f["id"] == id:
			return f
	return {}


func _build() -> void:
	# sea, land, shore ice, floor
	_fill(PackedVector2Array([Vector2(-95, -95), Vector2(95, -95), Vector2(95, 95), Vector2(-95, 95)]), -7.5, Color(0.12, 0.22, 0.36), "Sea")
	_fill(_pts(L["land"]["polygon"]), -0.05, Color(0.42, 0.44, 0.40), "Land")
	_fill(_pts(L["shore_ice"]["polygon"]), -0.4, Color(0.62, 0.78, 0.86), "ShoreIce")
	_fill(_pts(L["floor"]["polygon"]), 0.0, Color(0.86, 0.84, 0.78), "Floor")
	_ribbon(_pts(L["floor"]["polygon"]), 0.5, 0.03, Color(0.15, 0.15, 0.15), true)
	# coastline = the cliff lip (red-orange)
	_ribbon(_pts(L["land"]["cliff_lip"]), 1.0, 0.05, Color(0.95, 0.35, 0.10))
	# mere, stream, path, stone circle
	_fill(_pts(L["mere"]["polygon"]), 0.04, Color(0.35, 0.60, 0.85), "Mere")
	_ribbon(_pts(L["stream"]["polyline"]), float(L["stream"]["width_m"]), 0.06, Color(0.25, 0.50, 0.90))
	_ribbon(_pts(L["path"]["polyline"]), 1.0, 0.05, Color(0.65, 0.52, 0.35))
	var sc: Array = L["stone_circle"]["centre"]
	var ring := PackedVector2Array()
	for i in 48:
		var t := TAU * i / 48.0
		ring.append(Vector2(float(sc[0]), float(sc[1])) + Vector2(cos(t), sin(t)) * float(L["stone_circle"]["radius_m"]))
	_ribbon(ring, 0.5, 0.07, Color(0.4, 0.4, 0.4), true)
	# key features (prisms in their real heights)
	var keys := {"barrow_mound": Color(0.45, 0.50, 0.38), "barrow_forecourt": Color(0.6, 0.6, 0.6), "barrow_door": Color(0.85, 0.15, 0.15),
		"wreck_hull": Color(0.55, 0.32, 0.18), "wreck_mast": Color(0.40, 0.25, 0.14), "longhall": Color(0.35, 0.27, 0.22),
		"hall_porch": Color(0.70, 0.45, 0.25), "hall_great_door": Color(0.85, 0.15, 0.15), "fallen_gable": Color(0.80, 0.55, 0.20),
		"sea_cave_mouth": Color(0.05, 0.05, 0.05), "stair_wall_rock": Color(0.50, 0.46, 0.42)}
	for id in keys:
		var f := _feat(id)
		if f.is_empty():
			push_warning("missing feature " + id)
			continue
		var z0 := float(f.get("z_bottom_m", 0.0))
		var z1 := float(f.get("z_top_m", 1.0))
		if id == "barrow_mound":
			z1 = 1.0     # footprint only: the mound's cap would hide the door at this pitch
		_prism(_pts(f["footprint"]), z0, z1, keys[id], id)
	# stair flight + landings
	var S: Dictionary = L["stair"]
	_fill(_pts(S["flight"]["polygon"]), -3.6, Color(0.95, 0.90, 0.30), "StairFlight")
	_fill(_pts(S["top_landing"]["polygon"]), 0.08, Color(0.95, 0.80, 0.20), "StairTop")
	if S.has("bottom_landing") and S["bottom_landing"].has("polygon"):
		_fill(_pts(S["bottom_landing"]["polygon"]), -7.2, Color(0.80, 0.70, 0.20), "StairLedge")
	var fp := _pts(S["flight"]["polygon"])
	var foot := (fp[2] + fp[3]) * 0.5
	var topm := (fp[0] + fp[1]) * 0.5
	_ribbon(PackedVector2Array([foot, topm]), 0.6, 0.2, Color(0.1, 0.1, 0.1))
	# facing arrows (layout faces_deg) for the deliverer openings, and the stair's climb direction
	for id in ["barrow_door", "hall_great_door", "sea_cave_mouth", "hall_porch"]:
		var f := _feat(id)
		if f.has("faces_deg"):
			var c := _centroid(_pts(f["footprint"]))
			_arrow(c.x, c.y, float(f["faces_deg"]), 9.0, Color(1.0, 0.1, 0.6), 0.4 if id != "sea_cave_mouth" else -0.2)
	_arrow(foot.x, foot.y, float(S["axis_compass_deg_up"]), 9.0, Color(0.1, 0.1, 0.1), 0.3)
	# anchors: disc ring, pillar, label
	for p in L["anchors"]["points"]:
		var x := float(p["x"])
		var y := float(p["y"])
		var dr := PackedVector2Array()
		for i in 64:
			var t := TAU * i / 64.0
			dr.append(Vector2(x, y) + Vector2(cos(t), sin(t)) * 8.0)
		_ribbon(dr, 0.6, 0.1, Color(0.85, 0.62, 0.10), true)
		var cyl := MeshInstance3D.new()
		var cm := CylinderMesh.new()
		cm.top_radius = 1.0
		cm.bottom_radius = 1.0
		cm.height = 3.0
		cyl.mesh = cm
		cyl.material_override = _mat(Color(0.85, 0.62, 0.10))
		cyl.position = W(x, y, 1.5)
		root.add_child(cyl)
		_label(String(p["id"]), x, y, 5.0, Color(1.0, 0.85, 0.3), 128)
	# start crosshair
	_ribbon(PackedVector2Array([Vector2(-3, 0), Vector2(3, 0)]), 0.5, 0.12, Color(0, 0, 0))
	_ribbon(PackedVector2Array([Vector2(0, -3), Vector2(0, 3)]), 0.5, 0.12, Color(0, 0, 0))
	_label("start", 0, 0, 4.0, Color(1, 1, 1), 96)
	# feature labels
	var lab := {"barrow_door": "barrow door", "wreck_hull": "wreck", "longhall": "hall", "hall_great_door": "great door",
		"fallen_gable": "gable", "sea_cave_mouth": "cave", "barrow_mound": "mound"}
	for id in lab:
		var f := _feat(id)
		var c := _centroid(_pts(f["footprint"]))
		_label(lab[id], c.x, c.y, float(f.get("z_top_m", 1.0)) + 3.0, Color(0.8, 0.95, 1.0), 80)
	var mc := _centroid(_pts(L["mere"]["polygon"]))
	_label("mere", mc.x, mc.y, 3.0, Color(0.7, 0.9, 1.0), 80)
	_label("stair", topm.x, topm.y, 3.0, Color(1.0, 0.95, 0.4), 80)
	var sl: Array = L["stream"]["polyline"]
	_label("stream", float(sl[1][0]), float(sl[1][1]), 3.0, Color(0.7, 0.85, 1.0), 72)


func _camera() -> void:
	# barrow_full.gd:_build_camera, verbatim law; target = the site's centre (only the target moves)
	var p := deg_to_rad(F.PL_PITCH_DEG)
	var y := deg_to_rad(F.PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = 122.0
	cam.near = 0.05
	cam.far = STANDOFF + 400.0
	root.add_child(cam)
	var tgt := W(4.0, -6.0, 0.0)
	cam.look_at_from_position(tgt - f * STANDOFF, tgt, Vector3.UP)
	cam.current = true


func _process(_d: float) -> bool:
	frames += 1
	if frames < 8:
		return false
	var img := root.get_texture().get_image()
	var png := out_dir.path_join("render_" + tag + ".png")
	img.save_png(png)
	# twin check: screen px of each anchor and of the start, straight from Godot's camera
	var rep := {"tag": tag, "yaw_deg": yaw, "viewport": [img.get_width(), img.get_height()], "ortho_size_m": cam.size,
		"cam_basis": {"right": [cam.global_transform.basis.x.x, cam.global_transform.basis.x.y, cam.global_transform.basis.x.z],
			"up": [cam.global_transform.basis.y.x, cam.global_transform.basis.y.y, cam.global_transform.basis.y.z]}, "screen_px": {}}
	rep["screen_px"]["start"] = [cam.unproject_position(W(0, 0, 0)).x, cam.unproject_position(W(0, 0, 0)).y]
	for p in L["anchors"]["points"]:
		var s := cam.unproject_position(W(float(p["x"]), float(p["y"]), 0.0))
		rep["screen_px"][p["id"]] = [s.x, s.y]
	var ws := {}
	for p in L["anchors"]["points"]:
		var v := W(float(p["x"]), float(p["y"]), 0.0)
		ws[p["id"]] = [v.x, v.y, v.z]
	rep["world_xyz_twin"] = ws
	var fh := FileAccess.open(out_dir.path_join("render_" + tag + ".json"), FileAccess.WRITE)
	fh.store_string(JSON.stringify(rep, " "))
	fh.close()
	print("[lv] wrote ", png)
	return true
