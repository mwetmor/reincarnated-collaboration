extends SceneTree
# C-9 T7-A diagnostic round 3 -- the confirming test.
#
# HYPOTHESIS. The projector shader assigns ALPHA. In Godot 4 a spatial shader that writes
# ALPHA (without depth_draw_always / depth_prepass_alpha / an alpha-scissor material) is
# classified TRANSPARENT: it renders in the alpha pass, WRITES NO DEPTH, and is sorted
# per-OBJECT against every other transparent surface. So the 14 terrain meshes are
# transparent, and a prop card -- whose own shader also assigns ALPHA -- is in the same
# list, loses the per-object sort to them, and is painted over. Not a depth tie. A sort.
#
# PREDICTIONS, each falsifiable here:
#   1. strip `ALPHA = 1.0;` from the PROJECTOR only, leave the card material verbatim
#      -> the card draws, and draws the same pixels as an opaque card does.
#   2. the projected plate is unchanged by that strip (ALPHA=1 is the default)
#      -> pixel-identical against the current build.
#   3. with the ORIGINAL projector, biasing the card toward the camera makes it appear at
#      some threshold -- the previous session measured ~80 m -- because the bias moves it
#      up the per-object sort, not because it wins a depth test.

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PROP_PX := Vector2(1896.0139860139861, 2765.0)
const PITCH_COS := 0.602462407085

var out_dir := ""
var scene
var vp: SubViewport
var shot_cam: Camera3D
var lines: Array[String] = []
var card: MeshInstance3D
var tex: Texture2D
var _home := Vector3.ZERO


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://probe_card3")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)

	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 60:
		await process_frame
	shot_cam = Camera3D.new()
	shot_cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	shot_cam.keep_aspect = Camera3D.KEEP_HEIGHT
	shot_cam.near = scene.cam.near
	shot_cam.far = scene.cam.far
	shot_cam.cull_mask = scene.cam.cull_mask
	vp.add_child(shot_cam)
	shot_cam.current = true
	if scene.knight != null:
		scene.knight.visible = false
	scene.look_at_canvas(PROP_PX)
	_mirror()

	tex = load("res://props/assets/tree_living_a.png")
	_make_card()
	card.material_override = CliffWorld.card_material(tex)   # THE SHIPPED CARD, verbatim
	card.visible = false
	for i in 12:
		await process_frame
	var base_orig := vp.get_texture().get_image()
	base_orig.save_png(out_dir + "/A_plate_alpha.png")

	card.visible = true
	for i in 12:
		await process_frame
	var with_card_orig := vp.get_texture().get_image()
	say("[3] with the ORIGINAL projector (assigns ALPHA)")
	say("    shipped card, no bias            %8d px" % _diff(base_orig, with_card_orig))

	# --- prediction 3: the sort threshold -------------------------------------
	var fwd: Vector3 = scene.fwd
	var row := []
	for b in [0.0, 2.0, 5.0, 10.0, 20.0, 40.0, 60.0, 80.0, 100.0]:
		card.global_position = _home - fwd * b
		for i in 6:
			await process_frame
		var n := _diff(base_orig, vp.get_texture().get_image())
		row.append("%.0fm:%d" % [b, n])
	say("    bias toward camera ->            %s" % ", ".join(row))
	card.global_position = _home

	# --- prediction 1 + 2: strip ALPHA from the projector ----------------------
	var sh: Shader = scene._proj_mat.shader
	var patched: String = sh.code.replace("ALPHA = 1.0;", "")
	if patched == sh.code:
		say("    !! could not strip ALPHA from the projector")
	sh.code = patched
	card.visible = false
	for i in 20:
		await process_frame
	var base_fix := vp.get_texture().get_image()
	base_fix.save_png(out_dir + "/B_plate_noalpha.png")
	say("")
	say("[1,2] with ALPHA stripped from the PROJECTOR (card material untouched)")
	say("    plate differs from before by      %8d px   (expect 0: ALPHA=1 is the default)"
		% _diff(base_orig, base_fix))
	card.visible = true
	for i in 12:
		await process_frame
	var with_card_fix := vp.get_texture().get_image()
	with_card_fix.save_png(out_dir + "/C_card_over_fixed_plate.png")
	say("    shipped card, no bias             %8d px   (expect ~119141, the opaque count)"
		% _diff(base_fix, with_card_fix))

	# and the card with ITS alpha stripped too, for completeness
	var m2: ShaderMaterial = card.material_override
	m2.shader.code = m2.shader.code.replace("\tALPHA = 1.0;\n", "")
	for i in 12:
		await process_frame
	say("    + ALPHA stripped from the card    %8d px" % _diff(base_fix, vp.get_texture().get_image()))

	_write()
	quit(0)


func _make_card() -> void:
	var right: Vector3 = scene.right
	var up: Vector3 = scene.up
	var fwd: Vector3 = scene.fwd
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var anc := Vector2(328.013986013986, 561.0)
	var w := float(tex.get_width())
	var h := float(tex.get_height())
	var centre_px := PROP_PX - anc + Vector2(w, h) * 0.5
	var hit := CliffWorld.ground_at(space, PROP_PX, right, up, fwd)
	var h_world := (h / PPM) / PITCH_COS
	card = MeshInstance3D.new()
	card.name = "ProbeCard"
	var qm := QuadMesh.new()
	qm.size = Vector2(w / PPM, h_world)
	card.mesh = qm
	card.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	scene.add_child(card)
	var flat := right
	flat.y = 0.0
	flat = flat.normalized()
	var base: Vector3 = hit["position"] if not hit.is_empty() else CliffWorld.canvas_to_plane(PROP_PX, right, up)
	card.global_transform = Transform3D(Basis(flat, Vector3.UP, flat.cross(Vector3.UP)),
		base + Vector3.UP * (h_world * 0.5 * (1.0 - anc.y / maxf(h, 1.0)) + 0.05)
		+ flat * ((centre_px.x - PROP_PX.x) / PPM))
	_home = card.global_position


func _mirror() -> void:
	shot_cam.global_transform = scene.cam.global_transform
	shot_cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _diff(a: Image, b: Image) -> int:
	var n := 0
	for y in a.get_height():
		for x in a.get_width():
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			if absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b) > 0.02:
				n += 1
	return n


func _write() -> void:
	var f := FileAccess.open(out_dir + "/probe_card3.txt", FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	f.close()
	print("[probe3] -> ", out_dir)
