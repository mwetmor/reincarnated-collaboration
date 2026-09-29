extends SceneTree
# C-9 R-C9-66 (T7-A): the deliverable captures.
#
#   (a) the game camera at the bridge and the plateau  -> for the 2D side-by-side
#   (b) occlusion: the stand-in against real projected geometry AND against prop cards --
#       behind a tree, in front of a bridge post
#   (c) a camera orbit, +/-15 deg yaw and a little zoom -> where the projection holds
#   plus a COVERAGE map: geometry the painting never covered, measured in pixels.
#
#   Godot --path godot --resolution 1920x1080 --script tools/capture.gd -- [--out D]
#
# Needs a real window. Movie frames land in <out>/mp4frames as f_%04d.jpg -- JPEG, not
# PNG, because 280 frames of 1920x1080 PNG is 1 GB of scratch on a disk another run is
# watching, and the frames exist only long enough for ffmpeg to read them.

const SPOTS := {
	"plateau": Vector2(2285.62, 2407.32),
	"bridge": Vector2(3459.88, 1027.18),
}
# props.json's own anchors, and paths CHOSEN BY MEASUREMENT (tools/probe_occl.gd), which
# rendered the stand-in at 84 positions around six props and counted how much of his own
# silhouette each card takes away. The first, guessed path walked straight up the fall
# line at the tree and hid 1-3% of him at every step -- correct 3D and a useless picture,
# because this hillside climbs toward the camera faster than a person is tall, so a walker
# below a tree is FARTHER but does not overlap it on screen, and a walker above it overlaps
# it and is nearer. The card can only hide what is behind its plane. Crossing the trunk at
# 60 px above the anchor does: 57.2% of him goes behind it.
const OCCLUDERS := {
	"tree": {"px": Vector2(1896.0139860139861, 2765.0), "asset": "tree_living_a",
			 "axis": "x", "from": -230.0, "to": 190.0, "at": -60.0,
			 "zoom": 1.5, "aim": Vector2(1896.0, 2640.0)},
	# and the post the other way: he walks UP to bridge_post_1 and takes it out of sight.
	# 35 px above its anchor is where 87.8% of it goes behind him -- measured, same probe,
	# after a second defect was cleared: ground_at had no collision mask, so once the
	# walker was near the sample point the ray hit HIS OWN CAPSULE and stood him on his
	# shoulder. The first post path was chosen against those poisoned depths.
	"post": {"px": Vector2(2996.0, 1247.0), "asset": "bridge_post_1",
			 "axis": "y", "from": 200.0, "to": 0.0, "at": 0.0,
			 "zoom": 1.9, "aim": Vector2(2996.0, 1255.0)},
}

const SHOT_SIZE := Vector2i(1920, 1080)
const PPM := 100.617553710938

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
	# --resolution is a request the window manager may clamp: this Mac returns 1726x971,
	# and an orthographic camera sized in METRES then renders the world 10% small without
	# saying so. The live 2D route has the mirror of the same trap -- it stretches in
	# canvas_items mode, so the same clamp scales the whole scene by 0.899 -- which means a
	# side-by-side from two clamped windows compares two different scales and neither is
	# the one that ships. Both sides now go through a SubViewport that is exactly the size
	# it is told to be (the 2D side: chartest/tools/shot_2d_fixed.gd).
	_vp = SubViewport.new()
	_vp.size = SHOT_SIZE
	_vp.own_world_3d = false          # the same world, so this is the same scene
	_vp.transparent_bg = false
	_vp.msaa_3d = Viewport.MSAA_4X
	_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(_vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50:
		await process_frame
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
	report["props"] = scene.report.get("props", {})
	report["background"] = scene.report.get("background", [])

	await _view_a()
	await _view_b()
	await _view_c()
	await _movie()

	var f := FileAccess.open(out_dir + "/capture.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[cap] -> ", out_dir)
	quit(0)


func _mirror() -> void:
	_shot_cam.global_transform = scene.cam.global_transform
	_shot_cam.size = float(SHOT_SIZE.y) / PPM \
		* (scene.cam.size / (float(scene._view_height()) / PPM))


func _shot(name: String) -> Image:
	_mirror()
	for i in 4:
		await process_frame
	var img := _vp.get_texture().get_image()
	img.save_png("%s/%s.png" % [out_dir, name])
	return img


func _ne(a: Color, b: Color) -> bool:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02


func _small() -> Image:
	"""A frame at 480x270, for counting. Occlusion is a ratio, and a ratio does not need
	two million pixels -- but it does need every sample framed identically, which is why
	the camera is set before the four renders and not between them."""
	for i in 3:
		await process_frame
	var img := _vp.get_texture().get_image()
	img.resize(480, 270, Image.INTERPOLATE_NEAREST)
	return img


func _hide_knight(on: bool) -> void:
	if scene.knight != null:
		scene.knight.visible = not on


func _count_magenta(img: Image) -> int:
	var n := 0
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if c.r > 0.85 and c.g < 0.18 and c.b > 0.85:
				n += 1
	return n


func _view_a() -> void:
	print("[a] the game camera at the named spots")
	var cov := {}
	for name in SPOTS:
		scene.look_at_canvas(SPOTS[name])
		_hide_knight(true)
		await _shot("a_%s_3d" % name)
		scene.set_plate(false)
		await _shot("a_%s_grey" % name)
		scene.set_plate(true)
		scene.show_void(true)
		var v := await _shot("a_%s_void" % name)
		scene.show_void(false)
		cov[name] = {"void_px": _count_magenta(v),
					 "void_pct_of_view": snappedf(100.0 * float(_count_magenta(v))
						/ (float(SHOT_SIZE.x) * float(SHOT_SIZE.y)), 0.001)}
		_hide_knight(false)
		await _shot("a_%s_3d_knight" % name)
	report["view_a"] = SPOTS.keys()
	report["coverage_void"] = cov
	print("    coverage void: %s" % JSON.stringify(cov))


func _view_b() -> void:
	"""Occlusion, twice over.

	FIRST against real projected geometry -- the bridge and its abutment, the blockout's
	own triangles wearing the approved painting -- which is what the previous session
	could show. SECOND against PROP CARDS, which is what it could not: the stand-in walks
	BEHIND a painted tree and IN FRONT of a painted bridge post, and the depth buffer does
	the work a y-sort does in 2D.

	Positions are swept rather than asserted. Which canvas point puts a walker behind a
	tree is a property of the terrain and the card, so the sweep records BOTH depths at
	every step and the record says which is in front; it is not a claim about a picture."""
	var k = scene.knight
	if k == null:
		return
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	k.visible = true

	# --- (b1) the bridge, as before ------------------------------------------
	var rows := []
	var base := Vector2(3118.09, 1321.77)
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
	report["view_b_geometry"] = {"occluder": "bridge + south abutment (projected geometry)",
								 "swept": rows}

	# --- (b2) the props ------------------------------------------------------
	#
	# HOW MUCH the card hides is COUNTED, not eyeballed. Four renders per step --
	#   A body on/props off   B body off/props off  -> the silhouette is where A != B
	#   C body on/props on    D body off/props on   -> hidden is where C == D
	# -- so the number in the record is the share of the stand-in's own pixels a prop takes
	# away. Comparing a card's ORIGIN depth with a body's FOOT depth answers a different
	# question and answered it wrongly once already: it called every step of the first tree
	# sweep "in front of the card" while the trunk was in fact clipping a tenth of him.
	k.set_physics_process(false)     # pinned: a sample must be where it is put, not where
	                                 # eight frames of gravity slid it down the slope
	var props = scene.get_node_or_null(^"Props")
	var out := {}
	for tag in OCCLUDERS:
		var spec: Dictionary = OCCLUDERS[tag]
		var card: MeshInstance3D = null
		if props != null:
			for c in props.get_children():
				var mi := c as MeshInstance3D
				if mi != null and mi.name == String(spec["asset"]):
					card = mi
					break
		var sw := []
		var anchor: Vector2 = spec["px"]
		var n := 9
		for step in n:
			var u: float = float(spec["from"]) + (float(spec["to"]) - float(spec["from"])) \
				* float(step) / float(n - 1)
			var off := Vector2(u, float(spec["at"])) if String(spec["axis"]) == "x" \
				else Vector2(float(spec["at"]), u)
			var px := anchor + off
			var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
			if g.is_empty():
				sw.append({"step": step, "canvas_px": [px.x, px.y], "ground": "no hit"})
				continue
			k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
			k.velocity = Vector3.ZERO
			k.facing = "E" if String(spec["axis"]) == "x" else "N"
			k.state = "walk"
			k._drive()
			k._place_pollaxe()
			scene.look_at_canvas(spec["aim"], 0.0, spec["zoom"])
			for i in 4:
				await process_frame
			# ONE CARD, not the whole Props node. Hiding all 49 makes the denominator
			# "every prop pixel in frame" -- the burning snag, two stumps, a rope coil and
			# a second post -- so the stand-in covering bridge_post_1 entirely scored 4.3%
			# and read as nothing happening. The question is about THIS prop.
			var toggle: Node3D = card if card != null else props
			# MIRROR FIRST. The four counting renders used to go through _small(), which
			# does not set the shot camera -- only _shot() does -- so the first step of each
			# prop was counted through the PREVIOUS view's camera and came back sil 0,
			# props 0: a clean zero from an instrument pointed somewhere else.
			_mirror()
			toggle.visible = false
			var A := await _small()
			k.visible = false
			var B := await _small()
			toggle.visible = true
			var Dm := await _small()
			k.visible = true
			var C := await _shot("b_%s_step%d" % [tag, step])
			# BOTH DIRECTIONS, because occlusion has two of them and the sweep past the
			# post reads as "nothing happened" if only one is counted. At the last step the
			# stand-in hides bridge_post_1 ENTIRELY -- which is why no post can be seen
			# where he stands, and why "0% of him hidden" is the right answer and half the
			# answer. The card is 38 px wide and he is not.
			var sil := 0        # his own pixels
			var hid := 0        #   ... that a prop takes away
			var psil := 0       # the props' pixels
			var phid := 0       #   ... that he takes away
			var Cs := C.duplicate()
			Cs.resize(480, 270, Image.INTERPOLATE_NEAREST)
			for y in 270:
				for x in 480:
					var pa: Color = A.get_pixel(x, y)
					var pb: Color = B.get_pixel(x, y)
					var pc: Color = Cs.get_pixel(x, y)
					var pd: Color = Dm.get_pixel(x, y)
					if _ne(pa, pb):
						sil += 1
						if not _ne(pc, pd):
							hid += 1
					if _ne(pd, pb):
						psil += 1
						if not _ne(pc, pa):
							phid += 1
			var kd: float = k.global_position.dot(scene.fwd)
			sw.append({"step": step, "canvas_px": [snappedf(px.x, 0.1), snappedf(px.y, 0.1)],
					   "knight_depth_m": snappedf(kd, 0.01),
					   "silhouette_px": sil, "hidden_by_props_px": hid,
					   "hidden_pct": snappedf(100.0 * float(hid) / maxf(float(sil), 1.0), 0.1),
					   "props_px": psil, "props_hidden_by_knight_px": phid,
					   "props_hidden_pct": snappedf(100.0 * float(phid) / maxf(float(psil), 1.0), 0.1)})
		out[tag] = {"asset": spec["asset"], "anchor_px": [anchor.x, anchor.y],
					"card_origin_depth_m": snappedf(card.global_position.dot(scene.fwd), 0.01)
						if card != null else 0.0,
					"measured_at_px": [480, 270], "swept": sw}
		print("    %s: he is hidden %% %s" % [tag, str(sw.map(func(r): return r.get("hidden_pct", -1)))])
		print("    %s: props hidden %% %s" % [tag, str(sw.map(func(r): return r.get("props_hidden_pct", -1)))])
	k.set_physics_process(true)
	report["view_b_props"] = out


func _view_c() -> void:
	print("[c] orbit: where the projection holds and where it smears")
	var frames := 0
	var seq := []
	_hide_knight(false)
	for i in 121:
		var t := float(i) / 120.0
		var yaw := 15.0 * sin(t * TAU)
		var zoom := 1.0 + 0.25 * sin(t * TAU * 0.5)
		scene.look_at_canvas(SPOTS["bridge"], yaw, zoom)
		_mirror()
		await process_frame
		await process_frame
		frames += 1
		if i in [0, 30, 60, 90]:
			var nm := "c_yaw_%+03d" % int(round(yaw))
			_vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
			seq.append({"yaw_deg": snappedf(yaw, 0.1), "zoom": snappedf(zoom, 0.01), "file": nm})
	# the coverage void OFF AXIS, which is where it can appear at all: at the play camera
	# there is nothing uncovered, because the play camera is the camera the plate was
	# painted through. This is the honest place to measure what the projection lacks.
	scene.look_at_canvas(SPOTS["bridge"], 15.0, 1.0)
	scene.show_void(true)
	var v := await _shot("c_void_yaw15")
	scene.show_void(false)
	var n := _count_magenta(v)
	scene.set_void_fill(false)
	await _shot("c_yaw15_nofill")
	scene.set_void_fill(true)
	await _shot("c_yaw15_filled")
	scene.look_at_canvas(SPOTS["bridge"])
	report["view_c"] = {"orbit_samples": frames, "stills": seq,
						"yaw_range_deg": [-15, 15], "zoom_range": [0.75, 1.25],
						"void_at_yaw15_px": n,
						"void_at_yaw15_pct": snappedf(100.0 * float(n)
							/ (float(SHOT_SIZE.x) * float(SHOT_SIZE.y)), 0.001)}
	print("    void at yaw 15: %d px" % n)


var _mf := 0


func _frame() -> void:
	_mirror()
	await process_frame
	await process_frame
	# JPEG: the frames live only until ffmpeg has read them, and 280 PNGs is a gigabyte.
	_vp.get_texture().get_image().save_jpg("%s/mp4frames/f_%04d.jpg" % [out_dir, _mf], 0.92)
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
	for spot in SPOTS:
		scene.look_at_canvas(SPOTS[spot])
		for i in 26:
			await _frame()
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	# (b) the walk into the bridge, continuous
	var base := Vector2(3118.09, 1321.77)
	scene.look_at_canvas(base + Vector2(0, -20), 0.0, 1.6)
	for step in 44:
		var px := base + Vector2(-40.0, 150.0 - float(step) * 6.5)
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		if not g.is_empty():
			k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.05
		k.facing = "NE"
		k.state = "walk"
		k.play("c_walk")
		await physics_frame
		await _frame()
	# (b2) across the tree, then onto the bridge past the post -- the same paths the
	# measured sweep uses, so the movie shows the frames the record carries numbers for
	k.set_physics_process(false)
	for tag in OCCLUDERS:
		var spec: Dictionary = OCCLUDERS[tag]
		scene.look_at_canvas(spec["aim"], 0.0, spec["zoom"])
		var anchor: Vector2 = spec["px"]
		var horiz := String(spec["axis"]) == "x"
		for step in 44:
			var u: float = float(spec["from"]) + (float(spec["to"]) - float(spec["from"])) \
				* float(step) / 43.0
			var off := Vector2(u, float(spec["at"])) if horiz else Vector2(float(spec["at"]), u)
			var g := CliffWorld.ground_at(space, anchor + off, scene.right, scene.up, scene.fwd)
			if not g.is_empty():
				k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
			k.facing = "E" if horiz else "N"
			k.state = "walk"
			k._drive()
			k._place_pollaxe()
			await physics_frame
			await _frame()
	k.set_physics_process(true)
	# (c) the orbit
	for i in 121:
		var tt := float(i) / 120.0
		scene.look_at_canvas(SPOTS["bridge"], 15.0 * sin(tt * TAU),
							 1.0 + 0.25 * sin(tt * TAU * 0.5))
		await _frame()
	report["movie_frames"] = _mf
	print("[movie] %d frames" % _mf)
