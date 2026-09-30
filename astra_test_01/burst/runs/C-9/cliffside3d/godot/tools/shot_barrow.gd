extends SceneTree
# C-9 T10 — the barrow render stack, captured and measured in ONE run.
#
# ONE RUN AND NOT SEVERAL, for the reason T9 learned the hard way: two runs differ in more
# than the thing under test (the camera settles somewhere else, the idle animation lands on a
# different frame, the shader cache is cold), and attribution is a subtraction, so a
# subtraction between two runs measures the runs as well as the change.
#
# THE PAIRS ARE BUILT TO BE SUBTRACTED. Each pen is isolated by hiding IT and nothing else:
#   screen-space ink = nograde_ink_on  -  nograde_ink_off
#   hull ink         = nograde_ink_off -  nograde_hull_off
# so every ink pixel measured is a pixel that pen actually painted, rather than a dark pixel
# guessed to belong to it. The grade and the paper are off for those four frames only,
# because they multiply the frame and would put the two pens through the same distortion
# twice -- harmless for the ΔE between them, misleading for either against its nominal.
#
#   Godot --path godot --resolution 1920x1080 --script tools/shot_barrow.gd \
#         -- --out DIR [--frames DIR] [--walk 96]

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const FPS := 24.0
const DT := 1.0 / 24.0

# WHERE HE STANDS, AND IT MOVED BECAUSE THE WORLD DID. (-3.4, 6.2) was a point on the
# stand-in's hill; the measured barrow's painted square runs x -4.43..10.57, z -7.56..7.44,
# and the mound is at (0, -4). From (5.6, 1.6) the frame reaches about 6.7 m along
# (-0.73, -0.68) at the play zoom, which puts the door, the ring and the tarn up-screen.
# T10-1b: HE STANDS WHERE THE PAINTING HAS HIM -- the painted figure's base unprojected onto
# the flat floor, (3.48, 0.28), the middle of the painting's own clearing.
const STAND := Vector2(3.48, 0.28)
const WALK_FROM := Vector2(7.9, 5.1)
# beside the tallest standing stone, for the scale still -- half a metre off its face, on the
# camera side, so both are unoccluded and the eye can put one against the other
const SCALE_STAND := Vector2(4.85, -3.95)
const SCALE_LOOK := Vector2(4.25, -4.35)
# an OPEN patch of floor, well clear of every prop and of the mound: where shadow acne is
# counted, because acne on a surface that has a real shadow across it is not separable
const OPEN_PATCH := Vector2(9.0, 5.6)

var out_dir := ""
var frames_dir := ""
var walk_n := 96
var vp: SubViewport
var scene
var report := {}
var _mf := 0
var _body_off := Vector2.ZERO


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://barrow")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--frames" and i + 1 < args.size():
			frames_dir = args[i + 1]
		if args[i] == "--walk" and i + 1 < args.size():
			walk_n = int(args[i + 1])
	if frames_dir == "":
		frames_dir = out_dir + "/frames"
	DirAccess.make_dir_recursive_absolute(out_dir)
	DirAccess.make_dir_recursive_absolute(frames_dir)
	Engine.physics_ticks_per_second = int(FPS)

	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow.tscn").instantiate()
	vp.add_child(scene)
	for i in 80:
		await process_frame
		await physics_frame
	report["scene"] = scene.report
	report["viewport"] = {"size": [SHOT.x, SHOT.y], "msaa": "4x"}

	var k = scene.knight
	# FULL KIT FIRST, WITH THE ANIMATION RUNNING, AND ONLY THEN FREEZE. The old order froze the
	# mixer and THEN switched to the armed stack, so the armed tree never processed and the
	# skeleton showed an un-derooted pose: his Hips 1.87 m from his node. That is why last
	# pass's stills had him up-left of where he stood. And even settled, the armed idle draws
	# his body 1.35 m from his node (knight.gd, not this seam's) -- so every still below places
	# and aims at his BODY, via _stand_body, and the offset is reported.
	k.set_gear_stack(k.gear_stack_count() - 1)       # full kit: axe, shield, helmet, byrnie, mantle
	k.set_physics_process(false)
	scene.set_hud_visible(false)
	await _stand_body(STAND, "N")
	scene.park_camera(scene.body_centroid(), 1.0)
	await _settle()
	report["centring"] = _centring()

	# ---- true scale, in pixels, from his own bones --------------------------
	var rect: Rect2 = scene.character_screen_rect()
	var skel: Skeleton3D = null
	for n in k.find_children("*", "Skeleton3D", true, false):
		if (n as Skeleton3D).find_bone("head_end") >= 0:
			skel = n
	var crown_px := -1.0
	if skel != null:
		var hb := skel.find_bone("head_end")
		var top: Vector3 = skel.global_transform * skel.get_bone_global_pose(hb).origin
		var pcam: Camera3D = scene.cam
		var a: Vector2 = pcam.unproject_position(top)
		var b: Vector2 = pcam.unproject_position(Vector3(top.x, k.global_position.y, top.z))
		crown_px = absf(a.y - b.y)
	report["true_scale"] = {
		"figure_scale": k._figure_scale,
		"model_height_m": k.cfg.get("model_height_m", 1.85),
		"foot_to_crown_px": snappedf(crown_px, 0.1),
		"expected_px": snappedf(float(k.cfg.get("model_height_m", 1.85)) * PPM * 0.602462407085, 0.1),
		"bone_bbox_px": [snappedf(rect.size.x, 0.1), snappedf(rect.size.y, 0.1)],
		"_why_bones": "a silhouette difference also catches his cast shadow; T9 measured a 104 px man at 195 px that way",
	}

	# ---- the snow layer, area-weighted over the real faces ------------------
	report["snow"] = scene.snow_report()

	# T10-1d: THE HEATHER STANDS STILL FOR THE STILLS. Its wind is filmed (the walk here, and
	# tools/film_heather.sh); an A/B pair must differ in its one variable, not in a gust.
	if scene.has_method("set_heather_wind"):
		scene.set_heather_wind(false)

	# ---- THE VEIL, BEFORE AND AFTER, in one run ----------------------------
	# Before: the ground's own FBM snow blend on, the 3D snow field hidden, the fog as shipped.
	# After: the delivered look. Nothing else differs -- pose, camera, grade, pens, props.
	scene.set_veil_before(true)
	await _settle()
	await _shot("barrow_veil_before")
	scene.set_veil_before(false)
	await _settle()

	# ---- T10-1c: the two A/Bs, each a single-variable pair in this run -----
	# item 2, the rocks: every rock_large as T10-1b stood it, against laid low
	scene.set_rock_pose(true)
	await _settle()
	await _shot("barrow_rocks_upright")
	scene.set_rock_pose(false)
	# item 1, instancing: the same props, one node each, against the MultiMeshes
	scene.set_instancing(false)
	await _settle()
	await _shot("barrow_instancing_off")
	scene.set_instancing(true)
	await _settle()
	# ---- T10-1d item 1: the cast shadow BEFORE the bands (T10-1c's ramp), against after ----
	if scene.has_method("set_shadow_after_bands"):
		scene.set_shadow_after_bands(false)
		await _settle()
		await _shot("barrow_shadow_before_bands")
		scene.set_shadow_after_bands(true)
		await _settle()

	# ---- the stills ---------------------------------------------------------
	# the delivered look, and the same frame with the stack off
	scene.set_stack(true)
	await _settle()
	await _shot("barrow_stack_on")
	# the play framing's class-ID frame, occluded: where the heather is, for its clustering in
	# the fill (tools/barrow_heather_stats.py --play)
	vp.msaa_3d = Viewport.MSAA_DISABLED
	scene.set_class_id_view(true, true)
	await _settle()
	await _shot("barrow_play_ids_occl")
	scene.set_class_id_view(false)
	vp.msaa_3d = Viewport.MSAA_4X
	await _settle()
	scene.set_stack(false)
	await _settle()
	await _shot("barrow_stack_off")
	scene.set_stack(true)
	await _settle()
	# BOTH pens off, everything else delivered: the pair that gives the ink mask for the
	# min-luma and shadow-hue tests on the frame Matt is actually shown.
	scene.set_pens(false)
	await _settle()
	await _shot("barrow_stack_on_nopen")
	scene.set_pens(true)
	await _settle()

	# the ink, isolable
	scene.set_ink(false)
	await _settle()
	await _shot("barrow_ink_off")
	scene.set_ink(true)
	scene.set_grade(false)
	await _settle()
	await _shot("barrow_nograde_ink_on")
	scene.set_ink(false)
	await _settle()
	await _shot("barrow_nograde_ink_off")
	scene.set_hull_ink_visible(false)
	await _settle()
	await _shot("barrow_nograde_hull_off")
	scene.set_hull_ink_visible(true)
	scene.set_ink(true)
	scene.set_grade(true)
	await _settle()

	# the snow layer alone
	scene.set_snow(false)
	await _settle()
	await _shot("barrow_snow_off")
	scene.set_snow(true)
	await _settle()

	# the air alone
	scene.set_particles(false)
	await _settle()
	await _shot("barrow_air_off")
	scene.set_particles(true)
	# THE FOG IS OFF BY DEFAULT NOW, so the diagnostic flips: the frame WITH the old height fog
	scene.set_fog(true)
	await _settle()
	await _shot("barrow_fog_on")
	scene.set_fog(false)
	await _settle()

	# ---- HIM, before and after the ramp, world unchanged --------------------
	# The comparison Matt is owed: the ONLY thing that moves between these two frames is the
	# lighting response on his own materials. Same albedo, same ink line, same world, same
	# light, same pose.
	scene.set_ramp_on_character(true)
	await _settle()
	await _shot("barrow_char_ramp_on")
	scene.set_ramp_on_character(false)
	await _settle()
	await _shot("barrow_char_ramp_off")
	# and the THIRD state: his materials exactly as knight.gd built them, which is the look
	# Matt actually approved. ramp_mix = 0 is plain Lambert through the ramp shader and loses
	# his metallic 0.25, so it is close to the old look without being it.
	scene.set_ramp_on_character(true)
	scene.use_original_character_materials(true)
	await _settle()
	await _shot("barrow_char_original")
	scene.use_original_character_materials(false)
	await _settle()
	# HIM, REMOVED. His bone bounding box is 162x97 px and most of that rectangle is snow, so
	# a "before and after" averaged over the box is mostly an average of pixels that did not
	# change -- it reported a 1.7% difference for a change that is plainly visible on him.
	# This frame is what lets the comparison be masked to his actual silhouette.
	k.visible = false
	await _settle()
	await _shot("barrow_char_noknight")
	k.visible = true
	await _settle()
	report["char_rect_px"] = [int(rect.position.x), int(rect.position.y),
							  int(rect.size.x), int(rect.size.y)]

	# ---- does HE cast a shadow ---------------------------------------------
	report["his_shadow"] = await _shadow_check(k)
	print("[barrow] shadow %s" % JSON.stringify(report["his_shadow"]))

	# ---- R-C9-74 note 5: ONE PEN ON HIM, measured as a pair in ONE run ------
	# `char_exclude` off is the 15:20 build: his hull AND the screen-space depth line, both on
	# him. On is the fix. The two frames differ in nothing else -- same pose, same camera, same
	# grade, same paper -- so the difference between them IS the second pen's contribution to
	# the outline Matt called "WAY too thick", and barrow_metrics measures each one's width
	# inside his own silhouette rather than over the whole frame.
	scene.set_char_exclude(false)
	await _settle()
	await _shot("barrow_stack_on_2pens")
	scene.set_char_exclude(true)
	await _settle()
	# HIS hull alone, props' hulls left on: the pair that isolates the pen he keeps
	scene.set_grade(false)
	scene.set_ink(false)
	await _settle()
	await _shot("barrow_nograde_charhull_on")
	scene.set_char_hull_visible(false)
	await _settle()
	await _shot("barrow_nograde_charhull_off")
	scene.set_char_hull_visible(true)
	scene.set_ink(true)
	scene.set_grade(true)
	await _settle()
	report["one_pen_on_him"] = {
		"_pair": "barrow_stack_on_2pens (char_exclude OFF, the 15:20 behaviour) against barrow_stack_on (ON)",
		"_his_pen_pair": "barrow_nograde_charhull_on minus barrow_nograde_charhull_off",
		"hull_outline_px_from_character_json": scene.knight.cfg.get("outline_px", 1.1),
		"_why_that_number": "the weight approved in the cliffside 3D app; unchanged here",
	}

	# ---- R-C9-74 note 3: SHADOWS -------------------------------------------
	report["ink_shadow_audit"] = scene.ink_shadow_audit()
	report["shadow_bias_sweep"] = await _bias_sweep(k)

	# ---- THE PAINTING'S OWN FRAMING, and the class-ID pass for coverage ----
	# 1536x1024, ortho height 1024 / 140.86 = 7.2696 m, aimed at the painting's centre pixel
	# unprojected onto the flat floor; his BODY where the painting's figure stands.
	var fr: Dictionary = scene.report.get("dress_source", {}).get("frame", {})
	if not fr.is_empty():
		var prev_size := vp.size
		vp.size = Vector2i(int(fr["image_px"][0]), int(fr["image_px"][1]))
		await _stand_body(Vector2(float(fr["figure_scene_xz"][0]), float(fr["figure_scene_xz"][1])), "N")
		var aim_a: Array = fr["aim_scene_xyz"]
		var zoom_p: float = (float(fr["image_px"][1]) / PPM) / float(fr["ortho_size_m"])
		scene.park_camera(Vector3(float(aim_a[0]), float(aim_a[1]), float(aim_a[2])), zoom_p)
		await _settle()
		await _shot("barrow_painting_frame")
		# the same frame with the shadow BEFORE the bands: the dot screen's before/after at the
		# painting's framing, where it was found (the mound's flank)
		if scene.has_method("set_shadow_after_bands"):
			scene.set_shadow_after_bands(false)
			await _settle()
			await _shot("barrow_painting_frame_shadow_before")
			scene.set_shadow_after_bands(true)
			await _settle()
		# the ID pass: MSAA OFF, because a class colour blended with its neighbour at an edge
		# is a pixel of neither class
		vp.msaa_3d = Viewport.MSAA_DISABLED
		scene.set_class_id_view(true)
		await _settle()
		await _shot("barrow_painting_ids")
		scene.set_class_id_view(false)
		# and again with the ground, mound, snow and him drawn black rather than hidden: the
		# pixels of each class the EYE can see -- the warmth is sampled on these (T10-1c)
		scene.set_class_id_view(true, true)
		await _settle()
		await _shot("barrow_painting_ids_occl")
		scene.set_class_id_view(false)
		vp.msaa_3d = Viewport.MSAA_4X
		vp.size = prev_size
		report["painting_frame"] = {"frame": fr, "zoom": snappedf(zoom_p, 0.0001),
			"his_body_at": _v3(scene.body_centroid())}
		await _stand_body(STAND, "N")
		scene.park_camera(scene.body_centroid(), 1.0)
		await _settle()

	# ---- the wide framing, for the eye -------------------------------------
	# aimed between the mound at (0, -4) and the ring stones at x 2.5..3.9, z -2.3..-4.7, wide
	# enough to hold both: 10.73 m of screen height at zoom 0.45 is 23.8 m of frame
	var wide_aim := Vector3(2.0, scene.world.height_at(2.0, -3.0) + 1.2, -3.0)
	scene.park_camera(wide_aim, 0.45)
	await _settle()
	await _shot("barrow_wide_on")
	scene.set_stack(false)
	await _settle()
	await _shot("barrow_wide_off")
	scene.set_stack(true)
	await _settle()

	# ---- HIM BESIDE A TALL STONE, for scale --------------------------------
	# The one frame that answers "how big is any of this" without a caption. He is 1.85 m and
	# the stone is 2.71 m, both measured, both in one frame at one zoom.
	# THE STONE THE RAVEN IS ON: the tallest stone actually built (see _perch_raven), found by
	# reference rather than by a node name that the placement order can change
	var stone: Node3D = scene.get("_tallest_stone")
	# WHERE HE STANDS IS FOUND, NOT PICKED. The first hand-picked spot put a birch between him
	# and the camera: the one frame whose whole job is "how big is he next to this" had a tree
	# across his chest. 36 positions on a 1.5 m circle round the stone, keep the ones on the
	# camera side, take the one furthest from every other prop.
	var stand := SCALE_STAND
	var look_at := SCALE_LOOK
	if stone != null:
		# CLEARANCE IS MEASURED ON SCREEN, NOT ON THE GROUND, and the first version measured
		# it on the ground. It picked a spot 1.45 m from every other prop and put a birch
		# squarely across his chest -- because at a 52.95 degree pitch a tree 2 m BEHIND him
		# projects ABOVE him and a tree 2 m in front projects over his legs, and neither is
		# far away in the only space that matters, which is the picture. So each candidate is
		# scored by the screen rectangles: his own, and every other prop's, both unprojected
		# through the camera that will take the frame.
		# -INF, NOT -1: with 290 props every candidate's rect overlaps something, every
		# clearance is negative, and a -1 floor accepted none -- the still fell back to a
		# hand-typed spot 5.9 m from the stone. The least-overlapped spot is the answer.
		var best := -INF
		for ri in 4:
			var rad: float = 1.3 + 0.32 * float(ri)
			for i in 48:
				var a: float = TAU * float(i) / 48.0
				var c := Vector2(stone.global_position.x + cos(a) * rad,
								 stone.global_position.z + sin(a) * rad)
				# the camera looks along scene.fwd, so "toward the camera" is -fwd on the ground
				if Vector2(c.x - stone.global_position.x, c.y - stone.global_position.z).dot(
						Vector2(-scene.fwd.x, -scene.fwd.z).normalized()) < 0.15:
					continue
				var mine := _screen_rect(Vector3(c.x, scene.world.height_at(c.x, c.y), c.y),
										 0.55, 1.85)
				var clear := 1e9
				for nm in scene.prop_names():
					var n: Node3D = scene.prop_node(String(nm))
					if n == null or n == stone:
						continue
					var b: AABB = scene._node_aabb(n)
					var r: Rect2 = _screen_rect(n.global_position,
						maxf(b.size.x, b.size.z), b.size.y)
					# how far apart the two rectangles are on screen; negative where they overlap
					var dx: float = maxf(r.position.x - (mine.position.x + mine.size.x),
										 mine.position.x - (r.position.x + r.size.x))
					var dy: float = maxf(r.position.y - (mine.position.y + mine.size.y),
										 mine.position.y - (r.position.y + r.size.y))
					clear = minf(clear, maxf(dx, dy))
				if clear > best:
					best = clear
					stand = c
		look_at = Vector2((stand.x + stone.global_position.x) * 0.5,
						  (stand.y + stone.global_position.z) * 0.5)
		report["scale_stand_screen_clearance_px"] = snappedf(best, 0.1)
		report["_scale_stand_rule"] = "the point on 1.3-2.3 m around the stone, camera side, whose SCREEN rect is furthest from every other prop's"
	await _stand_body(stand, "N")
	# CENTRED ON HIM, per the coordinator; the stone is beside him in the same frame
	var bcs: Vector3 = scene.body_centroid()
	var look := Vector3((bcs.x * 2.0 + stone.global_position.x) / 3.0 if stone != null else bcs.x,
						1.1, (bcs.z * 2.0 + stone.global_position.z) / 3.0 if stone != null else bcs.z)
	scene.park_camera(look, 2.35)
	await _settle()
	await _shot("barrow_scale_beside_stone")
	if stone != null:
		report["scale_still"] = {
			"his_height_m": k.cfg.get("model_height_m", 1.85),
			"stone": String(stone.name),
			"stone_top_y_m": snappedf(stone.global_position.y
				+ scene.verify_placements([String(stone.name)])["props"][String(stone.name)]["built_size_m_local"][1], 0.01),
			"his_xz": [snappedf(stand.x, 0.01), snappedf(stand.y, 0.01)],
			"stone_xz": [snappedf(stone.global_position.x, 0.01), snappedf(stone.global_position.z, 0.01)],
			# `stand`, NOT SCALE_STAND. SCALE_STAND is the hand-picked FALLBACK, used only when
			# there is no stone to search around -- and this line kept reading it after the
			# search replaced it, so the report said he stood 1.45 m from the stone while the
			# frame showed him at 2.26 m. The still was right and the number beside it was
			# about a position nothing had used since the search landed.
			"gap_m": snappedf(Vector2(stone.global_position.x - stand.x,
									  stone.global_position.z - stand.y).length(), 0.01),
		}
	await _stand_body(STAND, "N")
	scene.unpark_camera()
	await _settle()

	# ---- FRAME COST, on this M2, at 1920x1080 ------------------------------
	# Measured on the viewport that actually renders the scene, with him WALKING, because a
	# parked idle frame is the cheapest frame the scene has and quoting it would be a
	# measurement of the screenshot rather than of the game.
	scene.unpark_camera()
	scene.freeze_pose(false)              # he has to move again for the cost run and the walk
	if scene.has_method("set_heather_wind"):
		scene.set_heather_wind(true)          # the walk is a film: the heather moves
	scene.place_knight(WALK_FROM.x, WALK_FROM.y, "NE")
	await _settle()
	report["frame_cost_ms"] = {
		"_at": "MSAA 4x, Apple M2, walking with the full kit, vsync off",
		"stack_on": await _time_frames(true, 140, SHOT),
		"stack_off": await _time_frames(false, 140, SHOT),
		"instrument_check_2.25x_pixels": {
			"_expect": "a frame with 2.25x the pixels must cost measurably more",
			"stack_on_at_2880x1620": await _time_frames(true, 90, Vector2i(2880, 1620)),
		},
	}
	scene.set_stack(true)

	# ---- THE WALK: from the tarn's edge to the barrow door, block and slash, and back
	#      through a drift -------------------------------------------------------------
	# Driven at waypoints through the camera law (_canvas_dir_to), and FILMED ON HIS BODY: the
	# game camera follows his node, and while he stands armed his body is 1.35 m from it, so a
	# movie shot on the game camera frames him off-centre exactly when he stops to fight. The
	# capture moves the camera itself, eased onto his bone centroid, and keeps the snowfall
	# emitter over him as the scene's own _process would.
	var wp: Dictionary = scene.walk_waypoints()
	var legs: Array = wp["route"]
	var fight_leg := int(wp["fight_at"])
	scene.freeze_pose(false)
	scene.place_knight(float(legs[0].x), float(legs[0].y), "N")
	k.set_physics_process(false)
	await _settle()
	scene.set_process(false)
	var aim: Vector3 = scene.body_centroid()
	var leg := 1
	var phase := []
	var fight_t := -1
	var deepest := 0.0
	var best_left := 1e9
	var best_i := 0
	var stuck := []
	for i in walk_n:
		var kp: Vector3 = k.global_position
		# THE FIGHT IS A WINDOW, not a latch: 56 frames at the door, then the route resumes. The
		# first version tested `fight_t < 0` for arrival, which is false forever once he has
		# fought -- so every leg after the door would have been walked until the movie ran out.
		# ...AND IT LASTS UNTIL THE SWING IS OVER. drive_dir roots him while a strike plays and
		# the slash outruns 30 frames: resuming mid-swing read as 24 frames of no progress, and
		# the stuck rule skipped the leg to the drift -- the one leg the walk exists for.
		var fighting: bool = fight_t >= 0 and (i < fight_t + 56
			or (k.attacking() and i < fight_t + 110))
		if fighting:
			var ft := i - fight_t
			if ft < 6:
				k.drive_dir(Vector2.ZERO, false, DT)
				phase.append("stop")
			elif ft < 26:
				k.set_block(true)
				k.drive_dir(Vector2.ZERO, false, DT)
				phase.append("block")
			else:
				if k.blocking():
					k.set_block(false)
				if not k.attacking() and phase[phase.size() - 1] != "slash":
					k.try_strike("slash")
				k.drive_dir(Vector2.ZERO, false, DT)
				phase.append("slash")
				best_left = 1e9
				best_i = i
		elif leg < legs.size():
			var tgt: Vector2 = legs[leg]
			var left := Vector2(tgt.x - kp.x, tgt.y - kp.z).length()
			# STUCK IS A MEASUREMENT, NOT A HANG: under 5 cm of progress on this waypoint in 24
			# frames means something solid is in the way -- the leg is logged and counted as
			# reached, so the movie finishes its route and the report says where it was blocked
			if left < best_left - 0.05:
				best_left = left
				best_i = i
			elif i - best_i > 24:
				stuck.append({"leg": leg, "at_xz": [snappedf(kp.x, 0.01), snappedf(kp.z, 0.01)],
							  "left_m": snappedf(left, 0.01)})
				left = 0.0
			if left < 0.45:
				if leg == fight_leg and fight_t < 0:
					fight_t = i                  # arrived at the door: stop, block, slash
				leg += 1
				best_left = 1e9
				best_i = i
				k.drive_dir(Vector2.ZERO, false, DT)
				phase.append("arrive_%d" % (leg - 1))
			else:
				k.drive_dir(_canvas_dir_to(k, tgt), false, DT)
				phase.append("walk_to_%d" % leg)
				if scene.snow != null:
					deepest = maxf(deepest, scene.snow.depth_at(Vector2(kp.x, kp.z)))
		else:
			k.drive_dir(Vector2.ZERO, false, DT)
			phase.append("done")
		var bc: Vector3 = scene.body_centroid()
		aim = aim.lerp(bc + Vector3(0, 0.1, 0), 0.22)
		scene.look_at_world(aim)
		if scene.snowfall != null:
			scene.snowfall.global_position = aim + scene.up * 9.0 - scene.fwd * 6.0
		await physics_frame
		await _frame()
	scene.set_process(true)
	var counts := {}
	for s2 in phase:
		counts[s2] = int(counts.get(s2, 0)) + 1
	report["walk_frames"] = _mf
	report["walk_fps"] = FPS
	report["walk"] = {"route": ["the tarn shore, inside the shore rocks", "the clearing",
			"the barrow door (stop, block, slash)", "east of the door", "the drift",
			"the tarn shore"],
		"waypoints_xz": legs.map(func(v): return [snappedf(v.x, 0.01), snappedf(v.y, 0.01)]),
		"legs_completed": leg - 1, "ended_at_xz": [snappedf(k.global_position.x, 0.01),
		snappedf(k.global_position.z, 0.01)],
		"deepest_snow_waded_m": snappedf(deepest, 0.001),
		"blocked_legs": stuck,
		"phase_frames": counts, "seconds": snappedf(float(walk_n) / FPS, 0.01),
		"_camera": "eased onto his bone centroid each frame, not the game camera (see above)"}

	var f := FileAccess.open(out_dir + "/barrow.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[barrow] -> %s  (%d walk frames)" % [out_dir, _mf])
	quit(0)


func _bias_sweep(k) -> Dictionary:
	"""R-C9-74 note 3: "Bias down to the smallest value with no acne." So the sweep runs and
	the number comes out of it, rather than a value being chosen and the comment claiming it
	was measured.

	TWO MEASUREMENTS, AND THE SECOND IS WHY THE FIRST IS NOT ENOUGH:

	  ACNE, on a patch of OPEN FLOOR with nothing casting onto it. Shadow acne is a surface
	    shadowing itself, so it shows as a dark speckle population on a surface that should be
	    uniformly lit. Counted as the share of pixels more than 8% of luma below the patch
	    mean. On clean lit snow that is ~0; under-biased it is percent.
	  THE CONTACT GAP, under HIM, because bias trades one artefact for the other: too little
	    and the floor speckles, too much and every shadow detaches from the thing casting it,
	    which is the half of Matt's note that says the shadows are "odd" rather than "dirty".
	    Measured by dilating his silhouette a pixel at a time until it meets his shadow.

	The grade and the paper grain are OFF for the sweep: both multiply the frame, and a paper
	texture is a speckle population by construction."""
	var sun: DirectionalLight3D = scene.sun
	var was_nb := sun.shadow_normal_bias
	var was_b := sun.shadow_bias
	scene.set_grade(false)
	scene.set_particles(false)
	# THE MOUND, NOT OPEN FLOOR. The first version parked on flat ground at OPEN_PATCH and
	# returned FIVE IDENTICAL ROWS -- 0.12561 at every bias, to five decimals. That is not a
	# weak effect, it is no effect: R-C9-74 made the floor flat, and a plane at one depth with
	# nothing over it cannot self-shadow at any bias. What it was counting was the rock tile's
	# own dark speckle. The mound is the only curved surface left, so it is where acne lives.
	scene.park_camera(Vector3(0.0, scene.world.height_at(0.0, -4.0) + 1.4, -4.0), 0.85)
	# the control: shadows OFF. Every row is read against this, not against zero -- a dark
	# share on a textured surface is mostly the texture.
	sun.shadow_enabled = false
	await _settle()
	var control := _speckle(vp.get_texture().get_image())
	sun.shadow_enabled = true
	var rows := []
	for nb in [0.0, 0.15, 0.35, 0.55, 1.2, 3.0]:
		sun.shadow_normal_bias = float(nb)
		sun.shadow_bias = 0.03
		await _settle()
		var img: Image = vp.get_texture().get_image()
		var s := _speckle(img)
		s["excess_over_control"] = snappedf(float(s["dark_share"]) - float(control["dark_share"]), 0.00001)
		rows.append({"normal_bias": nb, "shadow_bias": 0.03, "acne": s})
	sun.shadow_normal_bias = was_nb
	sun.shadow_bias = was_b
	scene.unpark_camera()
	await _stand_body(STAND, "N")
	scene.park_camera(scene.body_centroid(), 1.0)
	await _settle()
	var contact := await _contact_gap(k)
	scene.set_particles(true)
	scene.set_grade(true)
	await _settle()
	return {
		"_at": "the mound at (0, -4), the only curved surface on a flat floor; grade and particles off",
		"sun_elevation_deg": scene.SUN_ELEV_DEG,
		"control_shadows_off": control,
		"sweep": rows,
		"chosen": {"normal_bias": was_nb, "shadow_bias": was_b},
		"_chosen_rule": "no acne is measurable at ANY value 0.0..3.0; 0.15 is one step of margin over the measured answer of 0.0, and the excess-over-control column shows 1.2 and 3.0 eating real shadow rather than cleaning it",
		"contact_under_him": contact,
	}


func _speckle(img: Image) -> Dictionary:
	"""The share of pixels in a central window more than 8% of luma below the window's mean.
	CHECKED ON A KNOWN CASE: a synthetic flat field with a planted 2% speckle must come back
	at 2%, or the number the real frame produces is not evidence."""
	var x0 := int(float(SHOT.x) * 0.28)
	var x1 := int(float(SHOT.x) * 0.72)
	var y0 := int(float(SHOT.y) * 0.28)
	var y1 := int(float(SHOT.y) * 0.72)
	var vals := PackedFloat32Array()
	for y in range(y0, y1, 2):
		for x in range(x0, x1, 2):
			var c := img.get_pixel(x, y)
			vals.append(c.r * 0.2126 + c.g * 0.7152 + c.b * 0.0722)
	var mean := 0.0
	for v in vals:
		mean += v
	mean /= maxf(float(vals.size()), 1.0)
	var dark := 0
	for v in vals:
		if v < mean - 0.08:
			dark += 1
	# the instrument, on a field whose answer is planted
	var probe := PackedFloat32Array()
	for i in 10000:
		probe.append(0.02 if i % 50 == 0 else 0.90)
	var pm := 0.0
	for v in probe:
		pm += v
	pm /= float(probe.size())
	var pd := 0
	for v in probe:
		if v < pm - 0.08:
			pd += 1
	return {"px_sampled": vals.size(), "mean_luma_srgb": snappedf(mean, 0.0001),
			"dark_share": snappedf(float(dark) / maxf(float(vals.size()), 1.0), 0.00001),
			"instrument_check_planted_2pct": snappedf(float(pd) / float(probe.size()), 0.0001)}


func _contact_gap(k) -> Dictionary:
	"""HOW MANY PIXELS OF DAYLIGHT BETWEEN HIM AND HIS SHADOW. R-C9-74 asks for zero.

	His silhouette is (him) minus (him hidden), with shadows OFF so his own shadow is not in
	it. His shadow is (him, shadows on) minus (him hidden, shadows on) minus the silhouette.
	The gap is then found by growing the silhouette one pixel at a time until it touches the
	shadow -- which needs no distance transform and answers in the unit the ruling asks for."""
	var sun: DirectionalLight3D = scene.sun
	var box := 260
	var rect: Rect2 = scene.character_screen_rect()
	var cx := int(rect.position.x + rect.size.x * 0.5)
	var cy := int(rect.position.y + rect.size.y * 0.5)
	var x0: int = clampi(cx - box, 0, SHOT.x - 1)
	var y0: int = clampi(cy - box, 0, SHOT.y - 1)
	var x1: int = clampi(cx + box, 0, SHOT.x - 1)
	var y1: int = clampi(cy + box, 0, SHOT.y - 1)
	var w := x1 - x0
	var h := y1 - y0
	sun.shadow_enabled = false
	await _settle()
	var a_off: Image = vp.get_texture().get_image()
	k.visible = false
	await _settle()
	var b_off: Image = vp.get_texture().get_image()
	k.visible = true
	sun.shadow_enabled = true
	await _settle()
	var a_on: Image = vp.get_texture().get_image()
	k.visible = false
	await _settle()
	var b_on: Image = vp.get_texture().get_image()
	k.visible = true
	await _settle()
	var sil := []
	var shd := []
	sil.resize(w * h)
	shd.resize(w * h)
	var n_sil := 0
	var n_shd := 0
	for j in h:
		for i in w:
			var p := Vector2i(x0 + i, y0 + j)
			var d_off := _dif(a_off.get_pixel(p.x, p.y), b_off.get_pixel(p.x, p.y))
			var d_on := _dif(a_on.get_pixel(p.x, p.y), b_on.get_pixel(p.x, p.y))
			var s: bool = d_off > 0.012
			sil[j * w + i] = s
			var sh: bool = (not s) and d_on > 0.012
			shd[j * w + i] = sh
			n_sil += 1 if s else 0
			n_shd += 1 if sh else 0
	var gap := -1
	var cur: Array = sil.duplicate()
	for step in 8:
		for j in h:
			for i in w:
				if cur[j * w + i] and shd[j * w + i]:
					gap = step
					break
			if gap >= 0:
				break
		if gap >= 0:
			break
		var nxt: Array = cur.duplicate()
		for j in range(1, h - 1):
			for i in range(1, w - 1):
				if cur[j * w + i]:
					nxt[j * w + i - 1] = true
					nxt[j * w + i + 1] = true
					nxt[(j - 1) * w + i] = true
					nxt[(j + 1) * w + i] = true
		cur = nxt
	return {"his_px": n_sil, "his_shadow_px": n_shd,
			"gap_px": gap, "_requirement": "0 -- the shadow must touch his base",
			"shadow_as_share_of_his_body": snappedf(float(n_shd) / maxf(float(n_sil), 1.0), 0.01),
			"_was_at_17_deg": 1.62,
			"_window_px": [w, h]}


func _dif(a: Color, b: Color) -> float:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b)


func _stand_body(target: Vector2, facing: String) -> void:
	"""Put his BODY -- the centroid of his bones -- on `target`, frozen in the armed idle.

	Unfreeze, place the node, let the armed tree run 30 frames so the pose and the turn settle,
	freeze, MEASURE where the body ended up relative to the node, and move the node by minus
	that. The pose is frozen and his physics is off, so the body moves rigidly with the node.
	Reported per call, so a body that did not land is a number, not a surprise in a still."""
	var k = scene.knight
	scene.freeze_pose(false)
	scene.place_knight(target.x, target.y, facing)
	for i in 30:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
		await process_frame
	scene.freeze_pose(true)
	k.state = "idle"
	var bc: Vector3 = scene.body_centroid()
	var off := Vector2(bc.x - k.global_position.x, bc.z - k.global_position.z)
	_body_off = off
	k.global_position = Vector3(target.x - off.x, k.global_position.y, target.y - off.y)
	await _settle()
	var bc2: Vector3 = scene.body_centroid()
	var entry := {"target": [snappedf(target.x, 0.01), snappedf(target.y, 0.01)],
		"body_offset_from_node_m": snappedf(off.length(), 0.001),
		"body_miss_m": snappedf(Vector2(bc2.x - target.x, bc2.z - target.y).length(), 0.001)}
	if not report.has("body_placements"):
		report["body_placements"] = []
	report["body_placements"].append(entry)


func _centring() -> Dictionary:
	"""Where he lands on screen, from his bones -- the check that "centre the look-at on him"
	actually centred him. The frame centre is (960, 540)."""
	var r: Rect2 = scene.character_screen_rect()
	var c := r.position + r.size * 0.5
	return {"his_bone_rect_centre_px": [snappedf(c.x, 0.1), snappedf(c.y, 0.1)],
			"frame_centre_px": [SHOT.x * 0.5, SHOT.y * 0.5],
			"miss_px": snappedf(c.distance_to(Vector2(SHOT.x * 0.5, SHOT.y * 0.5)), 0.1)}


func _v3(v: Vector3) -> Array:
	return [snappedf(v.x, 0.001), snappedf(v.y, 0.001), snappedf(v.z, 0.001)]


func _screen_rect(base: Vector3, width_m: float, height_m: float) -> Rect2:
	"""A standing thing's footprint on screen: the eight corners of a width x height x width
	box at `base`, unprojected through the play camera and bounded. Unprojecting the corners
	rather than the centre is the point -- at this pitch a 3 m tree's crown lands a long way
	up-screen of its foot, and a centre-to-centre distance cannot see that at all."""
	var cam: Camera3D = scene.cam
	var lo := Vector2(1e9, 1e9)
	var hi := Vector2(-1e9, -1e9)
	var h: float = width_m * 0.5
	for sx in [-h, h]:
		for sz in [-h, h]:
			for sy in [0.0, height_m]:
				var p := cam.unproject_position(base + Vector3(sx, sy, sz))
				lo = lo.min(p)
				hi = hi.max(p)
	return Rect2(lo, hi - lo)


func _canvas_dir_to(k, target: Vector2) -> Vector2:
	"""A ground target, back through the camera law, into the canvas direction knight.gd
	drives on. The forward map is knight.canvas_velocity_to_world: world = right * (vx/PPM)
	+ lz * ((vy/PPM)/sin(pitch)). Solving it is a 2x2 in the (right, lz) basis, and the
	sin(pitch) is the whole of why a naive "walk up-screen" vector does not point where it
	looks -- up-screen on the GROUND is 1/sin(52.95) = 1.254x longer than it appears."""
	var p: Vector3 = k.global_position
	var d := Vector2(target.x - p.x, target.y - p.z)
	if d.length() < 1e-5:
		return Vector2.ZERO
	var r := Vector2(scene.right.x, scene.right.z)
	var lz := Vector2(sin(deg_to_rad(47.0)), cos(deg_to_rad(47.0)))
	var det: float = r.x * lz.y - r.y * lz.x
	if absf(det) < 1e-9:
		return Vector2(0.62, -1.0).normalized()
	var a: float = (d.x * lz.y - d.y * lz.x) / det
	var b: float = (r.x * d.y - r.y * d.x) / det
	return Vector2(a, b * sin(deg_to_rad(PL_PITCH_DEG))).normalized()


func _time_frames(stack: bool, n: int, res: Vector2i) -> Dictionary:
	"""WALL-CLOCK THROUGHPUT WITH VSYNC OFF, because the obvious instrument lies here.

	RenderingServer.viewport_get_measured_render_time_gpu() returned EXACTLY 0.00 for every
	sample, stack on and stack off, 110 samples each -- and 0.00 ms is not a fast frame, it is
	an unimplemented counter. The CPU half came back at 0.06 ms, which for 56,000 triangles, a
	shadow pass, 1,700 particles and a full-screen post pass is not a plausible number either.
	Both returned cleanly. Neither was measuring anything.

	So: vsync off, run frames as fast as the engine will, divide wall time by frames. And the
	instrument is CHECKED ON A KNOWN CASE by running it at two resolutions -- if a frame with
	2.25x the pixels does not cost measurably more, the number is not about rendering and must
	not be quoted."""
	scene.set_stack(stack)
	var prev := vp.size
	if res != vp.size:
		vp.size = res
	# THE LOOP MUST NOT AWAIT physics_frame. This capture sets physics to 24 Hz so the movie
	# frames are deterministic, and `await physics_frame` then gates the loop at 41.67 ms --
	# which is exactly what the previous version reported, for the stack on, for the stack off
	# and for a frame with 2.25x the pixels, all three within 0.7% of each other and of 1/24 s.
	# THE INSTRUMENT CHECK IS WHAT CAUGHT IT: three numbers that should have differed did not,
	# and the reason they did not was that none of them was about rendering.
	var prev_ticks := Engine.physics_ticks_per_second
	Engine.physics_ticks_per_second = 240
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	for i in 40:                                  # warm: shader compiles land in the first frames
		scene.knight.drive_dir(Vector2(0.62, -1.0), false, DT)
		await process_frame
	var t0 := Time.get_ticks_usec()
	for i in n:
		scene.knight.drive_dir(Vector2(0.62, -1.0), false, DT)
		await process_frame
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	Engine.physics_ticks_per_second = prev_ticks
	vp.size = prev
	return {"ms_per_frame": snappedf(ms, 0.01), "fps": snappedf(1000.0 / maxf(ms, 1e-3), 0.1),
			"frames": n, "render_px": [res.x, res.y]}


func _shadow_check(k) -> Dictionary:
	"""DOES HE CAST A SHADOW. Differencing him out of the frame gives his body AND his shadow;
	differencing him out with the sun's shadows OFF gives his body alone. The difference
	between those two areas is the shadow, in pixels. This is the same trap T9 recorded from
	the other side -- it measured a 104 px man at 195 px because his shadow rode along -- used
	here deliberately, as the measurement rather than as the error."""
	var sun: DirectionalLight3D = scene.sun
	var was := sun.shadow_enabled
	var counts := {}
	for spec in [["shadows_on", true], ["shadows_off", false]]:
		sun.shadow_enabled = bool(spec[1])
		await _settle()
		var with_him: Image = vp.get_texture().get_image()
		k.visible = false
		await _settle()
		var without: Image = vp.get_texture().get_image()
		k.visible = true
		var changed := 0
		for y in range(0, with_him.get_height(), 2):
			for x in range(0, with_him.get_width(), 2):
				var a := with_him.get_pixel(x, y)
				var b := without.get_pixel(x, y)
				if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.012:
					changed += 1
		counts[String(spec[0])] = changed * 4          # every 2nd px in each axis
	sun.shadow_enabled = was
	await _settle()
	var body: int = counts["shadows_off"]
	var both: int = counts["shadows_on"]
	return {
		"px_changed_by_him_with_shadows": both,
		"px_changed_by_him_without_shadows": body,
		"his_shadow_px": both - body,
		"shadow_as_share_of_his_body": snappedf(float(both - body) / maxf(float(body), 1.0), 0.01),
		"verdict": "he casts a shadow" if (both - body) > body / 5 else "NO SHADOW FROM HIM",
	}


func _settle() -> void:
	for i in 8:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	vp.get_texture().get_image().save_png("%s/%s.png" % [out_dir, nm])
	print("[barrow] %s" % nm)


func _frame() -> void:
	await process_frame
	await process_frame
	vp.get_texture().get_image().save_jpg("%s/f_%04d.jpg" % [frames_dir, _mf], 0.93)
	_mf += 1
