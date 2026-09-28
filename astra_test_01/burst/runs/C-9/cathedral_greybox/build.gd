extends Node
# Cathedral arena GREY BOX renderer. Reads build_target.json (geometry, canvas, out dir, passes)
# so v1 and v2 share one renderer and neither overwrites the other's inputs.
#
# Plate law (cathedral_spec.json, MEASURED): ppm 100.617553710938 px/m, pitch 52.9535411256029 deg,
# yaw 45 deg -- camera from the SOUTH-EAST looking NORTH-WEST (R-C9-45 cl.1).
# World: X = east, Y = north, Z = up.  Godot: (x, z, -y).
#
# LAYERS (R-C9-53). A box carries f=1 (FADE: a prop that fades around the player) or v=1 (VAULT:
# the overhead/near layer). Neither is in the plate -- the plate must carry the floor BEHIND a
# fading prop, or the fade reveals nothing.
#   guide / id / height : boxes with no f and no v   (the plate)
#   fade                : boxes with f=1             (piers + the occluding west-wall bays)
#   vault               : boxes with v=1             (ribs and cells, seen from the camera)

var target: Dictionary
var spec: Dictionary
var geom: Dictionary
var canv: Dictionary
var legend: Array = []
var meshes: Array[MeshInstance3D] = []
var cls_of: PackedInt32Array = PackedInt32Array()
var layer_of: PackedInt32Array = PackedInt32Array()   # 0 plate, 1 fade, 2 vault
var world: Node3D
var cam: Camera3D
var vp: SubViewport
var sun: DirectionalLight3D
var env: Environment
var PPM: float
var d3: Vector3
var r3: Vector3
var u3: Vector3

func _load(p: String) -> Dictionary:
	var f := FileAccess.open(p, FileAccess.READ)
	assert(f != null, "missing " + p)
	return JSON.parse_string(f.get_as_text())

func _ready() -> void:
	target = _load("res://build_target.json")
	spec = _load("res://cathedral_spec.json")
	geom = _load("res://" + String(target["geometry"]))
	canv = _load("res://" + String(target["canvas"]))
	legend = geom["legend"]
	DirAccess.make_dir_recursive_absolute(String(target["out_dir"]))

	PPM = float(spec["projection"]["ppm_plate"])
	var a := deg_to_rad(float(spec["projection"]["alpha_deg"]))
	var ca := cos(a)
	var sa := sin(a)
	var s2 := sqrt(2.0)
	d3 = Vector3(-ca / s2, -sa, -ca / s2)
	r3 = Vector3(1.0 / s2, 0.0, -1.0 / s2)
	u3 = Vector3(-sa / s2, ca, -sa / s2)

	_build_world()
	await _render_all()
	get_tree().quit()

func _build_world() -> void:
	var tile: int = int(canv["tile_px"])
	vp = SubViewport.new()
	vp.size = Vector2i(tile, tile)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
	vp.use_taa = false
	vp.use_debanding = false
	vp.transparent_bg = false
	vp.positional_shadow_atlas_size = 0
	add_child(vp)

	world = Node3D.new()
	world.name = "CathedralGreyBox"
	vp.add_child(world)

	env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1)
	env.ambient_light_energy = 0.78
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.tonemap_white = 1.0
	env.ssao_enabled = false
	env.ssil_enabled = false
	env.sdfgi_enabled = false
	env.glow_enabled = false
	env.fog_enabled = false

	var attrs := CameraAttributesPractical.new()
	attrs.auto_exposure_enabled = false

	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(tile) / PPM
	cam.near = 1.0
	cam.far = 3000.0
	cam.environment = env
	cam.attributes = attrs
	world.add_child(cam)

	# the sun: WEST, low (F-S1 / R-C9-44). No shadows: a guide's walkable floor must stay the
	# brightest and CALMEST surface in the image (brief sec 4). The sunset's real effect on the
	# floor ships as the separate FLOOR LIGHT guide (R-C9-53 cl.2), computed, never baked here.
	sun = DirectionalLight3D.new()
	sun.light_energy = 0.55
	sun.shadow_enabled = false
	sun.rotation = Vector3(deg_to_rad(-22.0), deg_to_rad(-90.0), 0.0)
	world.add_child(sun)

	var unit := BoxMesh.new()
	unit.size = Vector3.ONE

	for b in geom["boxes"]:
		var p: Array = b["p"]
		var s: Array = b["s"]
		var mi := MeshInstance3D.new()
		mi.mesh = unit
		var t := Transform3D.IDENTITY
		if b.has("ry"):
			t = t.rotated(Vector3.UP, float(b["ry"]))
		t = t.scaled_local(Vector3(float(s[0]), float(s[2]), float(s[1])))
		t.origin = Vector3(float(p[0]), float(p[2]), -float(p[1]))
		mi.transform = t
		world.add_child(mi)
		meshes.append(mi)
		cls_of.append(int(b["c"]))
		layer_of.append(3 if b.has("o") else (2 if b.has("v") else (1 if b.has("f") else 0)))

	for d in geom["discs"]:
		var p2: Array = d["p"]
		var rr := float(d["r"])
		var dep := float(d["depth"])
		var cone := CylinderMesh.new()
		cone.top_radius = rr
		cone.bottom_radius = 0.18
		cone.height = dep
		cone.radial_segments = 64
		var mi2 := MeshInstance3D.new()
		mi2.mesh = cone
		mi2.position = Vector3(float(p2[0]), float(p2[2]) - dep * 0.5, -float(p2[1]))
		world.add_child(mi2)
		meshes.append(mi2)
		cls_of.append(int(d["c"]))
		layer_of.append(0)

	print("built ", meshes.size(), " mesh instances")

func _col8(a: Array) -> Color:
	return Color8(int(a[0]), int(a[1]), int(a[2]))

func _flat(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = c
	m.disable_ambient_light = true
	m.disable_receive_shadows = true
	return m

func _lit(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	m.albedo_color = c
	m.roughness = 1.0
	m.metallic = 0.0
	m.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
	m.disable_receive_shadows = true
	return m

# which layers a pass draws; everything else is hidden so it cannot occlude
const PASS_LAYERS := {"guide": [0], "id": [0], "height": [0],
	"fade": [1], "id_fade": [1], "vault": [2], "id_vault": [2], "arch": [3]}

func _set_pass(which: String) -> void:
	var want: Array = PASS_LAYERS[which]
	var flat_mats := {}
	var lit_mats := {}
	for e in legend:
		var idx := int(e["index"])
		var nm := String(e["name"])
		if nm == "void_outside_frame" or nm == "opening_to_outside":
			flat_mats[idx] = _flat(Color8(0, 255, 0))
			lit_mats[idx] = flat_mats[idx]
		else:
			flat_mats[idx] = _flat(_col8(e["rgb"]))
			lit_mats[idx] = _lit(_col8(e["guide_grey"]))
	var hs: Shader = load("res://height.gdshader")
	var hm := ShaderMaterial.new()
	hm.shader = hs
	for i in meshes.size():
		var vis: bool = want.has(layer_of[i])
		meshes[i].visible = vis
		if not vis:
			continue
		if which == "height":
			meshes[i].material_override = hm
		elif which.begins_with("id"):
			meshes[i].material_override = flat_mats[cls_of[i]]
		else:
			meshes[i].material_override = lit_mats[cls_of[i]]
	if which == "height":
		env.background_color = Color8(255, 255, 0)
		sun.light_energy = 0.0
	elif which.begins_with("id"):
		env.background_color = _col8(legend[0]["rgb"])
		sun.light_energy = 0.0
	else:
		env.background_color = Color8(0, 255, 0)
		sun.light_energy = 0.55

func _place_camera(screen_cx: float, screen_cy: float) -> void:
	var BIG := 1400.0
	cam.transform = Transform3D(Basis(r3, u3, -d3),
		r3 * (screen_cx / PPM) - u3 * (screen_cy / PPM) - d3 * BIG)

func _render_all() -> void:
	var ox: float = float(canv["origin_screen_px"][0])
	var oy: float = float(canv["origin_screen_px"][1])
	var out_dir := String(target["out_dir"])
	for which in target["passes"]:
		_set_pass(String(which))
		for t in canv["tiles"]:
			var o: Array = t["origin_px"]
			var s: Array = t["size_px"]
			_place_camera(ox + float(o[0]) + float(s[0]) * 0.5,
				oy + float(o[1]) + float(s[1]) * 0.5)
			await RenderingServer.frame_post_draw
			await RenderingServer.frame_post_draw
			var img := vp.get_texture().get_image()
			var path := "%s/%s_%s.png" % [out_dir, String(which), String(t["name"])]
			img.save_png(path)
		print("pass ", which, " done")
	for m in meshes:
		m.visible = true
		m.owner = world
	cam.owner = world
	sun.owner = world
	var packed := PackedScene.new()
	packed.pack(world)
	ResourceSaver.save(packed, String(target["tscn"]))
	print("saved ", String(target["tscn"]))
