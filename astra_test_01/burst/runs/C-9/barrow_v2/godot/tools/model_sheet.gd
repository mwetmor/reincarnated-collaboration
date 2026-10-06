extends SceneTree
## barrow_v2 MODEL SHEET at EXACTLY the game camera (lane BX, R-C9-156 check for Matt).
##   godot --path godot --resolution 900x700 --script tools/model_sheet.gd -- <spec.json> <out_dir>
## For each tile in spec: one model alone, fitted to its slot size exactly as the scene places it, on a 1 m ground
## grid with a 1 m reference cube; orthographic camera, pitch = layout camera.pitch_deg (52.9535411256029), yaw 0,
## the same sun/ambient as the V-views. Writes <out_dir>/<id>.png and <out_dir>/tiles.json (ortho size, ppm, and the
## pixel of the hero's ground anchor so a JOIN-1 cell can be composited at the same ppm).

var spec: Dictionary
var out_dir := ""
var i := 0
var wait := 0
var sv: SubViewport
var cam: Camera3D
var holder: Node3D
var results := []
var pitch := 52.9535411256029
const VW := 900
const VH := 700


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	spec = JSON.parse_string(FileAccess.get_file_as_string(args[0]))
	out_dir = args[1]
	pitch = float(spec["camera"]["pitch_deg"])
	sv = SubViewport.new()
	sv.size = Vector2i(VW, VH)
	sv.own_world_3d = true
	sv.msaa_3d = Viewport.MSAA_4X
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.87, 0.89)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.86, 0.92)
	env.ambient_light_energy = 0.32
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	var we := WorldEnvironment.new()
	we.environment = env
	sv.add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -35.0, 0.0)
	sun.light_energy = 0.85
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 120.0
	sv.add_child(sun)
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.rotation_degrees = Vector3(-pitch, 0.0, 0.0)     # zero yaw, looking north (-Z), as the V-views
	cam.near = 0.5
	cam.far = 800.0
	sv.add_child(cam)
	cam.make_current()


func _mat(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = c
	m.roughness = 0.95
	return m


func _aabb_of(n: Node, xf: Transform3D) -> AABB:
	var out := AABB()
	var first := true
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		out = t * (n as MeshInstance3D).mesh.get_aabb()
		first = false
	for ch in n.get_children():
		var b := _aabb_of(ch, t)
		if b.size == Vector3.ZERO:
			continue
		out = b if first else out.merge(b)
		first = false
	return out


func _build(tile: Dictionary) -> void:
	if holder != null:
		holder.queue_free()
	holder = Node3D.new()
	sv.add_child(holder)
	var W := float(tile["W"])
	var D := float(tile["D"])
	var H := float(tile["H"])
	# the model, fitted per axis exactly as barrow_v2_greybox.gd's _place_box does (base at 0, footprint centred)
	var doc := GLTFDocument.new()
	var st := GLTFState.new()
	if doc.append_from_file(String(tile["glb"]), st) == OK:
		var model: Node3D = doc.generate_scene(st)
		var ab := _aabb_of(model, model.transform.affine_inverse())
		var hm := Node3D.new()
		var sc := Vector3(W / maxf(ab.size.x, 1e-3), H / maxf(ab.size.y, 1e-3), D / maxf(ab.size.z, 1e-3))
		hm.transform = Transform3D(Basis.from_scale(sc), Vector3.ZERO)
		model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
		hm.add_child(model)
		holder.add_child(hm)
	# ground + 1 m grid
	var gx0 := -W / 2.0 - 5.0
	var gx1 := W / 2.0 + 5.0
	var gz0 := -D / 2.0 - 4.0
	var gz1 := D / 2.0 + 5.0
	var gp := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(gx1 - gx0, gz1 - gz0)
	gp.mesh = pm
	gp.material_override = _mat(Color(0.93, 0.93, 0.91))
	gp.position = Vector3((gx0 + gx1) / 2.0, 0.0, (gz0 + gz1) / 2.0)
	holder.add_child(gp)
	var lm := _mat(Color(0.55, 0.57, 0.62))
	for xi in range(int(floor(gx0)), int(ceil(gx1)) + 1):
		var b := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(0.03, 0.01, gz1 - gz0)
		b.mesh = bm
		b.material_override = lm
		b.position = Vector3(xi, 0.006, (gz0 + gz1) / 2.0)
		holder.add_child(b)
	for zi in range(int(floor(gz0)), int(ceil(gz1)) + 1):
		var b2 := MeshInstance3D.new()
		var bm2 := BoxMesh.new()
		bm2.size = Vector3(gx1 - gx0, 0.01, 0.03)
		b2.mesh = bm2
		b2.material_override = lm
		b2.position = Vector3((gx0 + gx1) / 2.0, 0.006, zi)
		holder.add_child(b2)
	# 1 m reference cube, right of the model's front
	var cube := MeshInstance3D.new()
	var cm := BoxMesh.new()
	cm.size = Vector3.ONE
	cube.mesh = cm
	cube.material_override = _mat(Color(0.25, 0.45, 0.85))
	cube.position = Vector3(W / 2.0 + 2.0, 0.5, D / 2.0 + 1.5)
	holder.add_child(cube)
	# camera: zero yaw, the game pitch; ortho size frames the model (ppm = VH / size)
	var a := deg_to_rad(pitch)
	var size := maxf((H * cos(a) + (D + 6.0) * sin(a)) * 1.15, (W + 9.0) * float(VH) / float(VW) * 1.05)
	cam.size = size
	var tgt := Vector3(0.0, H * 0.35, D * 0.15)
	cam.position = tgt + Vector3(0.0, sin(a), cos(a)) * 300.0
	tile["ortho_size_m"] = size
	tile["ppm"] = float(VH) / size
	tile["hero_ground_m"] = [-W / 2.0 - 2.0, D / 2.0 + 1.5]


func _process(_d: float) -> bool:
	var tiles: Array = spec["tiles"]
	if i >= tiles.size():
		var f := FileAccess.open(out_dir.path_join("tiles.json"), FileAccess.WRITE)
		f.store_string(JSON.stringify({"camera": {"projection": "orthographic", "pitch_deg": pitch, "yaw_deg": 0.0, "viewport_px": [VW, VH]}, "tiles": results}, "  "))
		f.close()
		print("[sheet] %d tiles" % results.size())
		return true
	var t: Dictionary = tiles[i]
	if wait == 0:
		_build(t)
	wait += 1
	if wait < 6:
		return false
	var hp := Vector3(float(t["hero_ground_m"][0]), 0.0, float(t["hero_ground_m"][1]))
	t["hero_anchor_px"] = [cam.unproject_position(hp).x, cam.unproject_position(hp).y]
	var img := sv.get_texture().get_image()
	img.save_png(out_dir.path_join("%s.png" % t["id"]))
	results.append(t)
	print("[sheet] %s size %.2f ppm %.3f" % [t["id"], float(t["ortho_size_m"]), float(t["ppm"])])
	i += 1
	wait = 0
	return false
