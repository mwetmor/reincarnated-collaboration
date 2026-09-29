extends SceneTree
# C-9 T10: the barrow assets on the authored ground, at the game camera, with him for scale.
#
# THIS IS A GEOMETRY AND SCALE CHECK, NOT A LOOK TEST, and the distinction matters for how
# the stills are read. The render-stack drax owns the painted-albedo / soft-ramp / ink-edge
# stack; this uses plain materials and one directional light, because a still that mixed my
# placement with their shader would not tell either of us which half was wrong. What these
# frames answer is: are the assets the right SIZE next to him, are they standing the right
# way round, and does the authored ground carry them.
#
# It does not touch scenes/barrow.tscn or any shader. It builds its own scene from
# BarrowHeightfield plus barrow_assets.json plus barrow_scene_a.json, which is exactly the
# data the render stack will read.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_barrow_t10.gd -- --out DIR

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PITCH_COS := 0.602462407085
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)

var out_dir := ""
var ground := "res://data/height_a_authored.png"
var gmeta := "res://data/height_a_authored.json"
var world: BarrowHeightfield
var root3: Node3D
var vp: SubViewport
var cam: Camera3D
var report := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--derived" :
			ground = "res://data/height_a_marigold.png"
			gmeta = "res://data/height_a_marigold.json"
	DirAccess.make_dir_recursive_absolute(out_dir)

	root3 = Node3D.new()
	root.add_child(root3)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.72, 0.76, 0.82)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.82, 0.86, 0.95)
	env.ambient_light_energy = 0.55
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	root3.add_child(we)
	var sun := DirectionalLight3D.new()
	sun.light_energy = 1.25
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 60.0
	# the concept's own low winter sun, upper left
	sun.rotation = Vector3(deg_to_rad(-26.0), deg_to_rad(128.0), 0.0)
	root3.add_child(sun)

	world = BarrowHeightfield.new(ground, gmeta)
	var gm := StandardMaterial3D.new()
	gm.albedo_color = Color(0.93, 0.94, 0.96)
	gm.roughness = 0.95
	world.build_terrain(root3, gm)
	report["ground"] = world.report

	var assets = null
	if FileAccess.file_exists("res://data/barrow_assets.json"):
		assets = JSON.parse_string(FileAccess.get_file_as_string("res://data/barrow_assets.json"))
	if typeof(assets) != TYPE_DICTIONARY:
		# Say so rather than letting JSON.parse_string log "Unknown error getting token" and
		# leaving a null that quietly drops every Tripo asset from the scene.
		push_warning("[t10] no barrow_assets.json -- run 40_normalise.py first; only the "
					 + "procedural assets will be placed")
		assets = null
	var scene = JSON.parse_string(FileAccess.get_file_as_string("res://data/barrow_scene_a.json"))
	var key := "height_a_authored" if ground.ends_with("authored.png") else "height_a_marigold"
	var placed := {}
	var missing := {}
	for inst in scene["instances"][key]:
		var an := String(inst["asset"])
		var path := ""
		if an == "heather":
			path = "res://models/barrow/heather.glb"
		elif an == "birch":
			path = "res://models/barrow/birch_proc.glb"
		elif an == "raven":
			path = "res://models/barrow/raven.glb"
		elif assets != null and assets["models"].has(an):
			path = String(assets["models"][an]["glb"])
		if path == "" or not ResourceLoader.exists(path):
			missing[an] = int(missing.get(an, 0)) + 1
			continue
		var n: Node3D = (load(path) as PackedScene).instantiate()
		root3.add_child(n)
		n.rotation = Vector3.ZERO
		var ab := _aabb(n)
		if ab.size.y <= 0.0:
			n.queue_free()
			continue
		# the same two-frame rule as T9: SIZE unrotated, PLACEMENT after the turn
		var spec = assets["models"].get(an, {}) if assets != null else {}
		var ys := 1.0 / PITCH_COS if bool(spec.get("pitch_correct", false)) else 1.0
		var target := float(inst.get("height_m", 1.0))
		var s: float = target / maxf(ab.size.y * ys, 1e-6)
		n.scale = Vector3(s, s * ys, s)
		n.rotation = Vector3(0.0, deg_to_rad(float(spec.get("yaw_deg", 0.0))), 0.0)
		ab = _aabb(n)
		var xz: Array = inst["scene_xz"]
		var h := world.height_at(float(xz[0]), float(xz[1]))
		var c := ab.position + ab.size * 0.5
		n.global_position = Vector3(float(xz[0]) + n.global_position.x - c.x,
									h + n.global_position.y - ab.position.y,
									float(xz[1]) + n.global_position.z - c.z)
		for m in n.find_children("*", "MeshInstance3D", true, false):
			(m as MeshInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		placed[an] = int(placed.get(an, 0)) + 1
	report["placed"] = placed
	report["missing"] = missing
	print("[t10] placed %s ; missing %s" % [JSON.stringify(placed), JSON.stringify(missing)])

	# HIM, at true scale, on the ground, as the ruler -- behind a flag, because he is the
	# one part of this scene that expects the cliffside's own setup around him, and a probe
	# that hangs waiting for him tells you nothing about the assets.
	var want_knight := not OS.get_cmdline_user_args().has("--no-knight")
	print("[t10] terrain and props done; knight=%s" % want_knight)
	if not want_knight:
		await _shoot()
		quit(0)
		return
	var k: CharacterBody3D = preload("res://scripts/knight.gd").new()
	root3.add_child(k)
	await process_frame
	await process_frame
	k.set_physics_process(false)
	if k.has_method("set_gear_stack"):
		k.set_gear_stack(k.gear_stack_count() - 1)
	k.set_figure_scale(1.0)
	k.facing = "NE"
	k.state = "idle"
	k._drive()
	k.global_position = Vector3(0.0, world.height_at(0.0, 0.5) + 0.02, 0.5)
	for i in 8:
		await physics_frame
		await process_frame

	await _shoot()
	quit(0)


func _shoot() -> void:
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = 0.05
	cam.far = 400.0
	vp.add_child(cam)
	cam.current = true

	for shot in [["wide", Vector2(0.0, -1.0), 1.0], ["door", Vector2(0.0, -4.0), 1.9],
				 ["him", Vector2(0.0, 0.6), 2.6]]:
		var aim: Vector2 = shot[1]
		var zoom: float = float(shot[2])
		var h := world.height_at(aim.x, aim.y)
		var tgt := Vector3(aim.x, h, aim.y)
		cam.size = (float(SHOT.y) / PPM) / zoom
		cam.global_transform = Transform3D(Basis(RIGHT, UP, -FWD), tgt - FWD * 90.0)
		for i in 6:
			await process_frame
		vp.get_texture().get_image().save_png("%s/t10_%s.png" % [out_dir, String(shot[0])])
		print("[t10] shot %s" % String(shot[0]))

	var f := FileAccess.open(out_dir + "/t10_shots.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()


func _aabb(n: Node3D) -> AABB:
	"""The node's bounds in ITS OWN space, without asking for a global transform.

	Reading global_transform on a node that is not yet inside the tree returns identity and
	logs `Condition "!is_inside_tree()" is true` -- once per instance here -- and identity
	is a perfectly usable wrong answer: every model comes out sized against an AABB that
	silently belongs to a different space. Walking the parent chain from the mesh up to `n`
	gives the same box and never depends on when the node joined the tree."""
	var out := AABB()
	var first := true
	for m in n.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		if mi.mesh == null:
			continue
		var x := Transform3D.IDENTITY
		var cur: Node = mi
		while cur != null and cur != n:
			if cur is Node3D:
				x = (cur as Node3D).transform * x
			cur = cur.get_parent()
		var ab: AABB = x * mi.get_aabb()
		out = ab if first else out.merge(ab)
		first = false
	return out
