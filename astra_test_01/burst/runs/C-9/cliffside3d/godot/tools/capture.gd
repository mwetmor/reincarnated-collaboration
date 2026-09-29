extends SceneTree
# C-9 R-C9-66 (T7-A): the deliverable captures.
#
#   (a) the game camera at the bridge and the plateau  -> for the 2D side-by-side
#   (b) a stand-in walking BEHIND and IN FRONT of a scenery piece -> true occlusion
#   (c) a camera orbit, +/-15 deg yaw and a little zoom -> where the projection holds
#   plus a COVERAGE map: geometry the painting never covered.
#
#   Godot --path godot --resolution 1920x1080 --script tools/capture.gd -- --v4 [--out D]
#
# Needs a real window. Frames for the MP4 land in <out>/mp4frames as f_%04d.png.

const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),
	"bridge": Vector2(3459.88, 1027.18),
}
# a painted tree the walkable path runs past; the knight is put behind and in front of
# it along the VIEW direction, which on this camera is up-screen and down-screen
const OCCLUDER_PX := Vector2(1896.01, 2765.0)
const OCCLUDER_NAME := "tree_living_a"

const SHOT_SIZE := Vector2i(1920, 1080)

var out_dir := ""
var scene
var report := {}
var _vp: SubViewport
var _shot_cam: Camera3D


func _initialize():
	out_dir = ProjectSettings.globalize_path("user://capture")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/mp4frames")
	# CAPTURE THROUGH A FIXED SUBVIEWPORT, not through the window.
	#
	# --resolution is a request the window manager may clamp: one run came back 1920x972
	# because a menu bar took the rows, and an orthographic camera sized in METRES then
	# renders the world 10% small without saying so. The live 2D route has the mirror of
	# the same trap -- it stretches in canvas_items mode, so a 1728-wide window scales the
	# whole scene by 0.9 -- which means a side-by-side taken from two clamped windows
	# compares two different scales and neither is the one that ships.
	#
	# A SubViewport is exactly the size it is told to be.
	_vp = SubViewport.new()
	_vp.size = SHOT_SIZE
	_vp.own_world_3d = false          # the same world, so this is the same scene
	_vp.transparent_bg = false
	_vp.msaa_3d = Viewport.MSAA_4X
	_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(_vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 40:
		await process_frame
	# a camera in the capture viewport that mirrors the game camera exactly
	_shot_cam = Camera3D.new()
	_shot_cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	_shot_cam.keep_aspect = Camera3D.KEEP_HEIGHT
	_shot_cam.near = scene.cam.near
	_shot_cam.far = scene.cam.far
	_shot_cam.cull_mask = scene.cam.cull_mask
	_vp.add_child(_shot_cam)
	_shot_cam.current = true
	print("[cap] capture viewport %s" % str(_vp.size))
	report["knight_scale"] = scene.knight._figure_scale if scene.knight != null else 0.0

	await _view_a()
	await _view_b()
	await _view_c()
	await _movie()

	var f := FileAccess.open(out_dir + "/capture.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[cap] -> ", out_dir)
	quit(0)


func _shot(name: String) -> void:
	# mirror the game camera, then size for THIS viewport's height, not the window's
	_shot_cam.global_transform = scene.cam.global_transform
	_shot_cam.size = float(SHOT_SIZE.y) / 100.617553710938 \
		* (scene.cam.size / (float(scene._view_height()) / 100.617553710938))
	await process_frame
	await process_frame
	_vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, name])


func _hide_knight(on: bool) -> void:
	if scene.knight != null:
		scene.knight.visible = not on


func _view_a() -> void:
	print("[a] the game camera at the named spots")
	for name in SPOTS:
		scene.look_at_canvas(SPOTS[name])
		_hide_knight(true)
		await _shot("a_%s_3d" % name)
		scene.set_plate(false)
		await _shot("a_%s_grey" % name)
		scene.set_plate(true)
		scene.show_void(true)
		await _shot("a_%s_void" % name)
		scene.show_void(false)
		_hide_knight(false)
		await _shot("a_%s_3d_knight" % name)
	report["view_a"] = SPOTS.keys()


func _view_b() -> void:
	"""Occlusion against REAL PROJECTED GEOMETRY.
	
	The occluder is the bridge and its abutment rock -- part of the painted plate, on the
	blockout's own triangles -- and not a prop card, because the prop cards do not render
	over the projected terrain (see the note in cliffside3d._build_world). That makes
	this the honest demonstration available: the thing in front of the character is a
	piece of the approved painting, standing where the geometry it was painted from
	stands, and the depth test is doing the work that a y-sort does in 2D.
	
	Positions are swept along the path rather than guessed: which canvas point puts a
	walker behind the abutment is a property of the terrain, not something to assert."""
	var k = scene.knight
	if k == null:
		return
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var rows := []
	var base := Vector2(3118.09, 1321.77)          # the south abutment deck start
	for step in 7:
		var px := base + Vector2(-40.0, 150.0 - float(step) * 50.0)
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		if g.is_empty():
			rows.append({"step": step, "canvas_px": [px.x, px.y], "ground": "no hit"})
			continue
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
		k.velocity = Vector3.ZERO
		k.facing = "NE"
		k.state = "walk"
		k.play("c_walk")
		for i in 8:
			await physics_frame
			await process_frame
		scene.look_at_canvas(base + Vector2(0, -20), 0.0, 1.6)
		await _shot("b_step%d" % step)
		rows.append({"step": step, "canvas_px": [px.x, px.y],
					 "knight_depth_m": snappedf(k.global_position.dot(scene.fwd), 0.01)})
	report["view_b"] = {"occluder": "bridge + south abutment (projected geometry)",
						"swept": rows}


func _view_c() -> void:
	print("[c] orbit: where the projection holds and where it smears")
	var frames := 0
	var seq := []
	# a slow sweep out to +/-15 deg and back, with a breath of zoom, sampled for the MP4
	for i in 121:
		var t := float(i) / 120.0
		var yaw := 15.0 * sin(t * TAU)
		var zoom := 1.0 + 0.25 * sin(t * TAU * 0.5)
		scene.look_at_canvas(SPOTS["bridge"], yaw, zoom)
		await process_frame
		await process_frame
		frames += 1
		if i in [0, 30, 60, 90]:
			var nm := "c_yaw_%+03d" % int(round(yaw))
			_vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
			seq.append({"yaw_deg": snappedf(yaw, 0.1), "zoom": snappedf(zoom, 0.01), "file": nm})
	scene.look_at_canvas(SPOTS["bridge"])
	report["view_c"] = {"orbit_samples": frames, "stills": seq,
						"yaw_range_deg": [-15, 15], "zoom_range": [0.75, 1.25]}


var _mf := 0


func _frame() -> void:
	_shot_cam.global_transform = scene.cam.global_transform
	_shot_cam.size = float(SHOT_SIZE.y) / 100.617553710938 \
		* (scene.cam.size / (float(scene._view_height()) / 100.617553710938))
	await process_frame
	await process_frame
	_vp.get_texture().get_image().save_png("%s/mp4frames/f_%04d.png" % [out_dir, _mf])
	_mf += 1


func _movie() -> void:
	"""One sequence covering (a), (b) and (c), in that order, at 24 fps.
	
	Recorded rather than assembled from the stills so the walk and the orbit are
	continuous: a cut between two held frames would hide exactly the thing the orbit is
	meant to show, which is WHEN the projection starts to smear rather than whether it
	does at 15 degrees."""
	print("[movie] recording")
	var k = scene.knight
	if k != null:
		k.visible = true
	# (a) the two named spots, held
	for spot in SPOTS:
		scene.look_at_canvas(SPOTS[spot])
		for i in 30:
			await _frame()
	# (b) the walk into the bridge, continuous
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var base := Vector2(3118.09, 1321.77)
	scene.look_at_canvas(base + Vector2(0, -20), 0.0, 1.6)
	for step in 48:
		var px := base + Vector2(-40.0, 150.0 - float(step) * 6.0)
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		if not g.is_empty():
			k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
		k.facing = "NE"
		k.state = "walk"
		k.play("c_walk")
		await physics_frame
		await _frame()
	# (c) the orbit
	for i in 121:
		var tt := float(i) / 120.0
		scene.look_at_canvas(SPOTS["bridge"], 15.0 * sin(tt * TAU),
							 1.0 + 0.25 * sin(tt * TAU * 0.5))
		await _frame()
	report["movie_frames"] = _mf
	print("[movie] %d frames" % _mf)
