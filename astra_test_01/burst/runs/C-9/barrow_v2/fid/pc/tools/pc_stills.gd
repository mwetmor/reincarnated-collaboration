extends SceneTree
## BV2F 0.1 (lane PT, drax): v1 play-camera stills for PH's positive-control crops.
## A copy of barrow_full/godot/tools/capture_painted.gd's init + _stills (v1, unchanged in method:
## the painted scene, 1920x1080 SubViewport, MSAA 4x, HUD/overlay/crucible off, him placed, 30
## frames standing, settle 4, shot) with SIX NAMED VIEWS instead of v1's four. Run from a CLONE of
## barrow_full (never barrow_full itself):
##   Godot --path <clone>/godot --resolution 640x360 --script tools/pc_stills.gd -- --out DIR
## Writes DIR/<view>.png and DIR/views.json (where he stood, the camera's position/aim/size).

const PLAY := Vector2i(1920, 1080)
const DT := 1.0 / 60.0
# name, where he stands (u, v) in v1's layout, facing, what it shows (v1 layout anchors cited)
const VIEWS := [
	["start", Vector2(-3.0, -15.0), "N", "layout knight.spawn_uv (-3,-15), facing N: the path in"],
	["barrow_door", Vector2(0.0, 7.2), "N", "v1's own still 'door' spot: the cutting, lintel at (0,10.6), mound (0,13)"],
	["mere", Vector2(-11.0, -5.0), "W", "on the tarn: regions.ice centre (-13.5,-5), axes 12x9 m (v1 has a tarn, not a mere)"],
	["stone_ring", Vector2(0.0, 1.0), "S", "regions.arena centre (0,1) inside the ring r 9 at (0,2)"],
	["outcrop_field", Vector2(13.0, -6.0), "E", "east outcrops (17,-12) (18,-3) (17,6) (10,-15); reach_box u max 15.17"],
	["shore", Vector2(-15.5, -7.0), "W", "the tarn's W/SW rim: shore_rock (-19.2,-2.4)..(-16.2,-9.8); reach_box u min -19.17"],
]

var out_dir := ""
var vp: SubViewport
var scene
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		print("[pc_stills] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	scene.skip_character = false
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 3000:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[pc_stills] HALT: the scene never finished building")
		quit(3)
		return
	rep["launch_line"] = scene._paint_launch_line()
	print("[pc_stills] " + rep["launch_line"])
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	rep["renderer"] = {"method": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	var k = scene.knight
	var out := {}
	for s in VIEWS:
		scene.place_knight(float(s[1].x), float(s[1].y), String(s[2]))
		for i in 30:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		await _settle(4)
		await _shot(String(s[0]))
		var at: Vector2 = scene.knight_uv()
		var cam: Camera3D = scene.cam
		var o: Vector3 = cam.global_position
		var fwd: Vector3 = -cam.global_transform.basis.z
		out[String(s[0])] = {"knight_uv": [snappedf(at.x, 0.001), snappedf(at.y, 0.001)], "facing": s[2], "shows": s[3],
			"camera": {"position_world": [snappedf(o.x, 0.001), snappedf(o.y, 0.001), snappedf(o.z, 0.001)],
				"forward_world": [snappedf(fwd.x, 0.0001), snappedf(fwd.y, 0.0001), snappedf(fwd.z, 0.0001)],
				"projection": "orthogonal", "ortho_size_m": snappedf(cam.size, 0.0001),
				"centre_ground_uv": _centre_uv(cam)},
			"png": String(s[0]) + ".png", "px": [PLAY.x, PLAY.y]}
	rep["views"] = out
	rep["_what"] = "BV2F 0.1 v1 play-camera stills (lane PT): barrow_full at HEAD, the painted scene, 1920x1080, MSAA 4x"
	var f := FileAccess.open(out_dir.path_join("views.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(rep, " "))
	f.close()
	print("[pc_stills] -> %s" % out_dir)
	quit(0)


func _centre_uv(cam: Camera3D) -> Array:
	# the ground point under the frame's centre (y = 0 plane)
	var c := Vector2(PLAY.x * 0.5, PLAY.y * 0.5)
	var o := cam.project_ray_origin(c)
	var d := cam.project_ray_normal(c)
	if absf(d.y) < 1e-6:
		return []
	var p := o + d * (-o.y / d.y)
	var uv: Vector2 = scene.world_to_uv(p)
	return [snappedf(uv.x, 0.001), snappedf(uv.y, 0.001)]


func _settle(n := 8) -> void:
	for i in n:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	if img.get_width() != vp.size.x or img.get_height() != vp.size.y:
		print("[pc_stills] SIZE MISMATCH %s" % nm)
	img.save_png(out_dir.path_join(nm + ".png"))
	print("[pc_stills] %s.png %dx%d" % [nm, img.get_width(), img.get_height()])
