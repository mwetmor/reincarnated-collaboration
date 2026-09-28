extends Node
# CA-guides-v1 -- cathedral arena GREY BOX: builds the 3D scene from the authored
# geometry.json and renders the ortho plate in tiles under the plate projection law.
#
# The law (cathedral_spec.json, MEASURED): ppm 100.617553710938 px/m, pitch alpha
# 52.9535411256029 deg, yaw 45 deg -- camera from the SOUTH-EAST looking NORTH-WEST (R-C9-45).
# World: X = east, Y = north, Z = up.  Godot: (x, z, -y).

const OUT_DIR := "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/ca_tiles"

var spec: Dictionary
var geom: Dictionary
var canv: Dictionary
var meshes: Array[MeshInstance3D] = []
var cls_of: PackedInt32Array = PackedInt32Array()
var legend: Array = []
var world: Node3D
var cam: Camera3D
var vp: SubViewport
var sun: DirectionalLight3D
var env: Environment

var PPM: float
var ALPHA: float
var d3: Vector3
var r3: Vector3
var u3: Vector3

func _load(p: String) -> Dictionary:
	var f := FileAccess.open(p, FileAccess.READ)
	assert(f != null, "missing " + p)
	return JSON.parse_string(f.get_as_text())

func _ready() -> void:
	spec = _load("res://cathedral_spec.json")
	geom = _load("res://geometry.json")
	canv = _load("res://canvas.json")
	legend = geom["legend"]
	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	PPM = float(spec["projection"]["ppm_plate"])
	ALPHA = deg_to_rad(float(spec["projection"]["alpha_deg"]))
	var ca := cos(ALPHA)
	var sa := sin(ALPHA)
	var s2 := sqrt(2.0)
	# plan NW = (-1,+1)/sqrt2 in (east,north)  ->  godot (-1/sqrt2, ., -1/sqrt2)
	d3 = Vector3(-ca / s2, -sa, -ca / s2)
	r3 = Vector3(1.0 / s2, 0.0, -1.0 / s2)          # NE, screen right
	u3 = Vector3(-sa / s2, ca, -sa / s2)            # screen up

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
	cam.far = 1600.0
	cam.environment = env
	cam.attributes = attrs
	world.add_child(cam)

	# the sun: WEST, low (F-S1 / R-C9-44). No shadows: a guide's walkable floor must stay the
	# brightest and CALMEST surface in the image (brief sec 4), and raking shadow would put
	# high-frequency detail exactly there. Face differentiation comes from the directional term.
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
		mi.position = Vector3(float(p[0]), float(p[2]), -float(p[1]))
		mi.scale = Vector3(float(s[0]), float(s[2]), float(s[1]))
		world.add_child(mi)
		meshes.append(mi)
		cls_of.append(int(b["c"]))

	for d in geom["discs"]:
		var p: Array = d["p"]
		var rr := float(d["r"])
		var dep := float(d["depth"])
		var cone := CylinderMesh.new()
		cone.top_radius = rr
		cone.bottom_radius = 0.18
		cone.height = dep
		cone.radial_segments = 64
		var mi2 := MeshInstance3D.new()
		mi2.mesh = cone
		mi2.position = Vector3(float(p[0]), float(p[2]) - dep * 0.5, -float(p[1]))
		world.add_child(mi2)
		meshes.append(mi2)
		cls_of.append(int(d["c"]))

	print("built ", meshes.size(), " mesh instances")

func _col8(a: Array) -> Color:
	return Color8(int(a[0]), int(a[1]), int(a[2]))

func _flat(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = c
	m.disable_ambient_light = true
	m.disable_receive_shadows = true
	m.cull_mode = BaseMaterial3D.CULL_BACK
	return m

func _lit(c: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	m.albedo_color = c
	m.roughness = 1.0
	m.metallic = 0.0
	m.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
	m.disable_receive_shadows = true
	m.cull_mode = BaseMaterial3D.CULL_BACK
	return m

func _set_pass(which: String) -> void:
	var mats := {}
	for e in legend:
		var idx := int(e["index"])
		var name := String(e["name"])
		if which == "id":
			mats[idx] = _flat(_col8(e["rgb"]))
		elif which == "guide":
			if name == "void_outside_frame" or name == "opening_to_outside":
				mats[idx] = _flat(Color8(0, 255, 0))
			else:
				mats[idx] = _lit(_col8(e["guide_grey"]))
	if which == "height":
		var sh: Shader = load("res://height.gdshader")
		var sm := ShaderMaterial.new()
		sm.shader = sh
		for i in meshes.size():
			meshes[i].material_override = sm
		env.background_color = Color8(255, 255, 0)
		sun.light_energy = 0.0
		return
	for i in meshes.size():
		meshes[i].material_override = mats[cls_of[i]]
	if which == "id":
		env.background_color = _col8(legend[0]["rgb"])
		sun.light_energy = 0.0
	else:
		env.background_color = Color8(0, 255, 0)
		sun.light_energy = 0.55

func _place_camera(screen_cx: float, screen_cy: float) -> void:
	var BIG := 700.0
	cam.transform = Transform3D(Basis(r3, u3, -d3),
		r3 * (screen_cx / PPM) - u3 * (screen_cy / PPM) - d3 * BIG)

func _render_all() -> void:
	var ox: float = float(canv["origin_screen_px"][0])
	var oy: float = float(canv["origin_screen_px"][1])
	for which in ["guide", "id", "height"]:
		_set_pass(which)
		for t in canv["tiles"]:
			var o: Array = t["origin_px"]
			var s: Array = t["size_px"]
			var cx := ox + float(o[0]) + float(s[0]) * 0.5
			var cy := oy + float(o[1]) + float(s[1]) * 0.5
			_place_camera(cx, cy)
			await RenderingServer.frame_post_draw
			await RenderingServer.frame_post_draw
			var img := vp.get_texture().get_image()
			var path := "%s/%s_%s.png" % [OUT_DIR, which, String(t["name"])]
			img.save_png(path)
			print("wrote ", path)
	# the grey box itself, as a Godot asset
	var packed := PackedScene.new()
	for m in meshes:
		m.owner = world
	cam.owner = world
	sun.owner = world
	packed.pack(world)
	ResourceSaver.save(packed, "res://cathedral_greybox.tscn")
	print("saved res://cathedral_greybox.tscn")
