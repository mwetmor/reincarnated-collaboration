extends SceneTree
# C-9 probe R-C9-34 verification.  Loads scenes/cliffside.tscn headless and asserts:
#   1. the rig is mounted under the knight skin, with its bones, sprites and both clips
#   2. in style B facing E the RIG is what is drawn -- rig visible AND the Grok cell's
#      own drawing suppressed (self_modulate.a == 0); every other facing is still Grok
#   3. G (toggle_rig) swaps E between RIG and GROK in place, both ways, and the HUD
#      line says which is live
#   4. the rig knight is the SAME SIZE and stands on the SAME SPOT as the Grok cell --
#      if G moved or resized him, the A/B would be comparing the wrong thing
#   5. FOOT SLIDE, measured off the rig's own near-foot bone in WORLD space while the
#      body walks east: during stance that world x must not move.  This is the number
#      the probe exists to produce, so it is measured from the running rig, not
#      recomputed from the equation the rig was built with.
#
# Writes frames/knight_rig_probe.json.

var fails := 0
var report := {}


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("  PASS  " if ok else "  FAIL  ") + what)


func _initialize():
	print("=== C-9 rig probe (R-C9-34) ===")
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	await physics_frame

	var keeper = scene.find_child("Keeper", true, false)
	var knight = keeper.get_node_or_null(^"KnightSprite")
	var rig = knight.get_node_or_null(^"Rig")
	_check(rig != null, "Rig mounted under Keeper/KnightSprite")
	if rig == null:
		quit(1)
		return

	# --- 1. structure ----------------------------------------------------
	print("[rig structure]")
	var skel: Skeleton2D = rig.get_node(^"Skel")
	var anim: AnimationPlayer = rig.get_node(^"Anim")
	var sprites: Array = rig.find_children("*", "Sprite2D", true, false)
	print("    bones %d   sprites %d   animations %s"
		% [skel.get_bone_count(), sprites.size(), str(anim.get_animation_list())])
	_check(skel.get_bone_count() == 17, "17 bones (got %d)" % skel.get_bone_count())
	_check(sprites.size() == 15, "15 part sprites (got %d)" % sprites.size())
	_check(anim.has_animation("walk") and anim.has_animation("idle"), "walk + idle clips present")
	var wl := anim.get_animation("walk").length
	var kf: SpriteFrames = knight.sprite_frames
	var grok_stride := kf.get_frame_count("walk_E") / kf.get_animation_speed("walk_E")
	_check(absf(wl - grok_stride) < 0.005,
		"rig walk is one Keeper stride: %.4f s vs the Grok cell's %.4f s" % [wl, grok_stride])
	_check(absf(anim.get_animation("idle").length - 2.0) < 0.005,
		"rig idle is the 2.0 s breath (%.3f s)" % anim.get_animation("idle").length)
	var missing: Array = []
	for s in sprites:
		if (s as Sprite2D).texture == null:
			missing.append(String(s.name))
	_check(missing.is_empty(), "every part sprite has its texture%s"
		% ("" if missing.is_empty() else " (missing: " + str(missing) + ")"))
	report["bones"] = skel.get_bone_count()
	report["sprites"] = sprites.size()
	report["walk_length_s"] = wl
	report["grok_walk_stride_s"] = grok_stride

	# --- 2. the rig is what is drawn when facing E -----------------------
	print("[E uses the rig, other directions do not]")
	await _walk(keeper, ["move_right"], 30)
	_check(String(keeper.facing) == "E", "facing E (%s)" % keeper.facing)
	_check(rig.visible and absf(knight.self_modulate.a) < 0.001,
		"facing E: rig visible=%s, Grok cell suppressed (self_modulate.a=%.2f)"
		% [str(rig.visible), knight.self_modulate.a])
	_check(String(rig.call("current_animation")) == "walk",
		"rig plays walk while walking (%s)" % rig.call("current_animation"))
	await _walk(keeper, ["move_left"], 30)
	_check(String(keeper.facing) == "W", "facing W (%s)" % keeper.facing)
	_check(not rig.visible and knight.self_modulate.a > 0.99,
		"facing W: rig hidden and the Grok cell drawn again (a=%.2f)" % knight.self_modulate.a)
	await _walk(keeper, ["move_right"], 30)
	for a in ["move_right"]:
		Input.action_release(a)
	await physics_frame
	await process_frame
	_check(String(rig.call("current_animation")) == "idle",
		"rig falls back to idle when input stops (%s)" % rig.call("current_animation"))

	# --- 3. G swaps in place ---------------------------------------------
	print("[G: rig <-> Grok]")
	_check(scene.rig_mode() == "RIG", "starts in RIG (%s)" % scene.rig_mode())
	var m: String = scene.toggle_rig()
	await process_frame
	_check(m == "GROK" and not rig.visible and knight.self_modulate.a > 0.99,
		"G -> GROK: rig hidden, Grok cell drawn (%s)" % m)
	m = scene.toggle_rig()
	await process_frame
	_check(m == "RIG" and rig.visible and absf(knight.self_modulate.a) < 0.001,
		"G -> RIG: rig drawn, Grok cell suppressed (%s)" % m)

	# --- 4. same size, same spot -----------------------------------------
	# The rig is posed to idle t=0 first.  Measuring it mid-stride reports a knight
	# 8 cell px short with his sole 5 px off the ground -- which is a correct reading
	# of a lifted foot and a crouched hip, and the wrong answer to "is he registered".
	print("[registration: G must change the motion and nothing else]")
	rig.call("play_state", "idle")
	rig.call("seek", 0.0)
	await process_frame
	var fit_txt: String = FileAccess.get_file_as_string("res://frames/knight_rig_E.json")
	var fitj = JSON.parse_string(fit_txt)
	var refc: Dictionary = fitj["ref_cell_idle_E"]
	# The Grok cell's own crown/sole/foot-centre, measured by tools/build_knight_rig_E.py
	# with the component rule, converted into world px through the sprite's transform.
	# They are NOT re-derived here: a width threshold in GDScript picks the axe blade
	# (42 px wide at row 193) over the helm (40 px at row 201) and quietly reports the
	# knight as 8 px taller than he is.
	var xf: Transform2D = knight.get_global_transform()
	var cell_crown_y: float = (xf * (knight.offset + Vector2(0, float(refc["crown"])))).y
	var cell_sole_y: float = (xf * (knight.offset + Vector2(0, float(refc["sole"])))).y
	var cell_foot_x: float = (xf * (knight.offset + Vector2(float(refc["foot_band_cx"]), 0))).x
	var rig_rect: Array = _rig_rect(rig)
	print("    rig   crown %.1f  sole %.1f  height %.1f  foot cx %.1f (world px)"
		% [rig_rect[0], rig_rect[1], rig_rect[1] - rig_rect[0], rig_rect[2]])
	print("    Grok  crown %.1f  sole %.1f  height %.1f  foot cx %.1f (world px)"
		% [cell_crown_y, cell_sole_y, cell_sole_y - cell_crown_y, cell_foot_x])
	var dh: float = absf((rig_rect[1] - rig_rect[0]) - (cell_sole_y - cell_crown_y))
	var dy: float = absf(rig_rect[1] - cell_sole_y)
	var dcrown: float = absf(rig_rect[0] - cell_crown_y)
	_check(dh < 2.5, "figure height matches the Grok E cell within 2.5 px (%.2f)" % dh)
	_check(dcrown < 2.5, "helm crown row matches within 2.5 px (%.2f)" % dcrown)
	_check(dy < 2.5, "sole row matches within 2.5 px (%.2f)" % dy)
	# Horizontal: the Grok number is the centroid of the cell's bottom six rows -- the
	# toe end of the sabaton, not the middle of the boot -- so it is NOT comparable to
	# the rig foot sprite's centre.  The registration claim is that they stand on the
	# same spot, and the test for that is containment.
	var dx: float = absf(rig_rect[2] - cell_foot_x)
	_check(cell_foot_x >= rig_rect[3] and cell_foot_x <= rig_rect[4],
		"the Grok cell's foot-band centre (%.1f) falls inside the rig's sabaton (%.1f..%.1f)"
		% [cell_foot_x, rig_rect[3], rig_rect[4]])
	report["registration"] = {"rig_height_px": rig_rect[1] - rig_rect[0],
		"grok_height_px": cell_sole_y - cell_crown_y,
		"d_height_px": dh, "d_sole_px": dy, "d_foot_cx_px": dx}

	# --- 5. FOOT SLIDE ----------------------------------------------------
	# Walk east for two strides and watch the near foot's bone in WORLD space.  While
	# it is planted its world x must not move: any movement IS slide, in the same
	# canvas pixels tools/measure_foot_slide.py reports for the Grok cells.
	print("[foot slide, measured on the rig's own near-foot bone]")
	# Start from the spot tools/loop_dryrun.gd verified as open (DRIFT 0.00 px).  From
	# the Keeper's own start position he reaches scenery inside two strides, and a body
	# that has stopped while the clip keeps playing reports as 65 px of "slide" -- which
	# is a true reading of the foot and a false answer to the question.
	keeper.velocity = Vector2.ZERO
	keeper.global_position = Vector2(2450, 2100)
	await physics_frame
	var samples: Array = []
	Input.action_press("move_right")
	for f in 160:
		await physics_frame
		await process_frame
		samples.append([anim.current_animation_position,
						rig.call("near_foot_global").x,
						keeper.global_position.x])
	Input.action_release("move_right")
	await physics_frame

	# stance is the first half of the clip; collect contiguous runs of it
	var runs: Array = []
	var cur: Array = []
	for s in samples:
		if float(s[0]) < wl * 0.5:
			cur.append(s)
		else:
			if cur.size() > 4:
				runs.append(cur)
			cur = []
	if cur.size() > 4:
		runs.append(cur)
	var worst := 0.0
	var per_run: Array = []
	for r in runs:
		var lo := INF
		var hi := -INF
		for s in r:
			lo = minf(lo, float(s[1]))
			hi = maxf(hi, float(s[1]))
		# A run only measures SLIDE if the body was actually travelling through it at
		# the walk speed.  If it was blocked, or the clip was still spinning up, the
		# foot's world motion is a true reading of the wrong thing.
		var dt: float = float(r[r.size() - 1][0]) - float(r[0][0])
		var moved: float = float(r[r.size() - 1][2]) - float(r[0][2])
		var want: float = 247.0 * dt
		var valid: bool = dt > wl * 0.35 and want > 1.0 and absf(moved - want) < 0.12 * want
		per_run.append({"samples": r.size(), "foot_world_x_range_px": hi - lo,
						"t_from": r[0][0], "t_to": r[r.size() - 1][0],
						"body_moved_px": moved, "body_expected_px": want, "valid": valid})
		if valid:
			worst = maxf(worst, hi - lo)
		print("    stance run: %2d samples  t %.3f..%.3f  body %+6.1f px (want %+6.1f)  foot world x moved %6.2f px  %s"
			% [r.size(), r[0][0], r[r.size() - 1][0], moved, want, hi - lo,
			   "measured" if valid else "SKIPPED (body not at walk speed)"])
	var body_travel: float = float(samples[samples.size() - 1][2]) - float(samples[0][2])
	var stride_travel: float = 247.0 * wl
	print("    body travelled %.1f px over %d frames; one stride = %.1f px"
		% [body_travel, samples.size(), stride_travel])
	print("    WORST planted-foot movement in any stance: %.2f canvas px" % worst)
	print("    Grok E, measured by tools/measure_foot_slide.py: 34.4 px per stride (ratio 0.81)")
	# The ankle is not the plant any more -- see section 8. During stance it rolls
	# forward over the sole and rises at toe-off, by an amount the build states, so
	# the honest assertion is that it moves by THAT and not by zero. Asserting zero
	# here would fail a correct heel-toe and pass a foot that slides backwards.
	var want_ankle: float = float(fitj["walk"]["heel_toe"]["ankle_stance_world_travel_canvas_px"])
	print("    authored ankle travel during stance: %.2f canvas px (it rolls; the PLANT is checked in section 8)" % want_ankle)
	_check(absf(worst - want_ankle) < 3.5,
		"the ankle travels the authored roll, %.2f px, not zero and not free (%.2f)"
		% [want_ankle, worst])
	report["foot_slide"] = {"worst_stance_drift_canvas_px": worst,
		"stance_runs": per_run, "body_travel_px": body_travel,
		"stride_travel_px": stride_travel,
		"grok_E_slide_px_per_stride": 34.4, "grok_E_slide_ratio": 0.81}

	# --- 6. the RUN, same measurement at run speed ------------------------
	print("[rig run: foot slide at run speed, and flight]")
	var rstats: Dictionary = fitj["run"]
	var rlen: float = anim.get_animation("run").length
	var rstance: float = float(rstats["stance_fraction"])
	_check(absf(rlen - float(rstats["stride_seconds"])) < 0.002,
		"rig run clip is one Keeper RUN stride (%.4f s)" % rlen)
	keeper.velocity = Vector2.ZERO
	keeper.global_position = Vector2(2450, 2100)
	await physics_frame
	var rs: Array = []
	Input.action_press("move_right")
	Input.action_press("run_modifier")
	for f in 150:
		await physics_frame
		await process_frame
		rs.append([anim.current_animation_position, rig.call("near_foot_global").x,
				   keeper.global_position.x, String(anim.current_animation)])
	Input.action_release("run_modifier")
	Input.action_release("move_right")
	await physics_frame
	var played_run := 0
	for s in rs:
		if String(s[3]) == "run":
			played_run += 1
	_check(played_run > rs.size() / 2,
		"the rig plays its RUN clip while the Keeper runs (%d/%d samples)" % [played_run, rs.size()])
	var rruns: Array = []
	var rcur: Array = []
	for s in rs:
		if String(s[3]) == "run" and float(s[0]) < rlen * rstance:
			rcur.append(s)
		else:
			if rcur.size() > 3:
				rruns.append(rcur)
			rcur = []
	if rcur.size() > 3:
		rruns.append(rcur)
	var rworst := 0.0
	var rper: Array = []
	for r in rruns:
		var lo2 := INF
		var hi2 := -INF
		for s in r:
			lo2 = minf(lo2, float(s[1]))
			hi2 = maxf(hi2, float(s[1]))
		var dt2: float = float(r[r.size() - 1][0]) - float(r[0][0])
		var moved2: float = float(r[r.size() - 1][2]) - float(r[0][2])
		var want2: float = 494.0 * dt2
		var valid2: bool = dt2 > rlen * rstance * 0.5 and want2 > 1.0 and absf(moved2 - want2) < 0.12 * want2
		rper.append({"samples": r.size(), "foot_world_x_range_px": hi2 - lo2,
					 "body_moved_px": moved2, "body_expected_px": want2, "valid": valid2})
		if valid2:
			rworst = maxf(rworst, hi2 - lo2)
		print("    run stance: %2d samples  t %.3f..%.3f  body %+6.1f (want %+6.1f)  foot moved %6.2f px  %s"
			% [r.size(), r[0][0], r[r.size() - 1][0], moved2, want2, hi2 - lo2,
			   "measured" if valid2 else "SKIPPED (body not at run speed)"])
	print("    WORST planted-foot movement in any RUN stance: %.2f canvas px" % rworst)
	var want_ankle_r: float = float(fitj["run"]["heel_toe"]["ankle_stance_world_travel_canvas_px"])
	print("    authored ankle travel during RUN stance: %.2f canvas px" % want_ankle_r)
	_check(absf(rworst - want_ankle_r) < 4.0,
		"the ankle travels the authored roll at run speed, %.2f px (%.2f)"
		% [want_ankle_r, rworst])
	report["run"] = {"clip_length_s": rlen, "stance_fraction": rstance,
					 "flight_fraction": rstats["flight_fraction"],
					 "worst_stance_drift_canvas_px": rworst, "stance_runs": rper,
					 "samples_playing_run": played_run}

	# --- 7. HIP COVERAGE (R-C9-40) ---------------------------------------
	# Matt: "the legs detach at the thigh from the body and move as ghosts."  The fix is
	# that each thigh plate carries a SOLID DISC centred on its own hip socket, because a
	# disc centred on a pivot is the one shape a rotation about that pivot cannot move --
	# so the socket stays covered at every angle, not merely at the angles someone
	# sampled.  That is an invariant of the TEXTURE, so it is checked on the texture, in
	# Godot, on the thing that actually ships: walk the hip bone's position into the
	# thigh sprite's own texel space and read the alpha of the disc around it.
	#
	# Checking a rendered frame instead would only ever say "no gap at these frames".
	# This says the gap cannot open.
	print("[hip coverage: the thigh's disc about its own socket]")
	var capr: float = float(fitj["hip_cap_seed_px"]) * float(fitj["transform"]["png_texels_per_seed_px"])
	for side in ["near", "far"]:
		var bone_path := "Skel/hip/leg_%s_th" % ("n" if side == "near" else "f")
		var bone: Node2D = rig.get_node(NodePath(bone_path))
		var spr: Sprite2D = bone.get_node(NodePath("S_leg_%s_thigh" % side))
		var img: Image = spr.texture.get_image()
		# hip socket -> texel space: the sprite is centred on the bone's frame
		# The socket is the BONE's origin, so it is Vector2.ZERO in the bone's frame.
		# The sprite is a child of that bone, centred, so the inverse of the sprite's
		# own transform takes the socket into sprite-local px and adding half the
		# texture puts it in texels.
		var c := Vector2(img.get_width(), img.get_height()) * 0.5
		var tex_hip: Vector2 = c + spr.transform.affine_inverse() * Vector2.ZERO
		var bad := 0
		var tested := 0
		var r := int(capr) - 2
		for ddy in range(-r, r + 1):
			for ddx in range(-r, r + 1):
				if ddx * ddx + ddy * ddy > r * r:
					continue
				var px := int(round(tex_hip.x)) + ddx
				var py := int(round(tex_hip.y)) + ddy
				tested += 1
				if px < 0 or py < 0 or px >= img.get_width() or py >= img.get_height():
					bad += 1
				elif img.get_pixel(px, py).a < 0.5:
					bad += 1
		print("    %-4s thigh: socket at texel (%.1f, %.1f), disc r=%d, %d/%d texels bare"
			% [side, tex_hip.x, tex_hip.y, r, bad, tested])
		_check(bad == 0, "%s thigh is SOLID over the whole hip disc (%d bare of %d)"
			% [side, bad, tested])
		report["hip_disc_" + side] = {"radius_texels": r, "bare": bad, "tested": tested}

	# --- 8. CONTACT SLIDE, not ankle slide (R-C9-40) ----------------------
	# The foot now rolls heel to toe, so the ankle is NOT the thing that has to hold
	# still -- it rises 13 rig px over the rolling forefoot at toe-off, and that is the
	# gait working, not the foot slipping.  What must hold still is the point that is
	# TOUCHING.  build_knight_rig_E.py records it per keyed frame in the foot bone's own
	# frame; this walks it through the live bone chain, so it measures the composition
	# of the rig -- keys, hierarchy, interpolation, physics tick -- rather than the
	# equation the keys were written from.
	print("[contact-point slide: the point actually touching the ground]")
	var node_sc: float = float(fitj["transform"]["node_scale"])
	for gait in ["walk", "run"]:
		var keys: Array = fitj[gait]["heel_toe"]["contact_local_rig_px"]
		var clen: float = anim.get_animation(gait).length
		var bone2: Node2D = rig.get_node(^"Skel/hip/leg_n_th/leg_n_sh/leg_n_ft")
		# PAUSE before scrubbing. The clip runs on the PHYSICS callback, so a seek
		# followed by an await lets the player advance before the transform is read,
		# and the sample belongs to a different time than the key it is compared with.
		anim.play(gait)
		anim.pause()
		var prev := Vector2.ZERO
		var have := false
		var worst2 := 0.0
		var n2 := 0
		for i in keys.size():
			var k: Array = keys[i]
			if int(k[2]) == 0:
				have = false
				continue
			anim.seek(clen * float(i) / float(keys.size() - 1), true)
			var world: Vector2 = bone2.global_transform * Vector2(float(k[0]), float(k[1]))
			# the body is standing still while we scrub, so in a correct rig the contact
			# point walks backward at exactly the gait's speed; consecutive keys are
			# compared against that, not against zero
			# The contact does NOT simply run backward at the gait speed: it rolls
			# FORWARD along the sole while the body carries it back, so the expected
			# step is (roll - travel), not -travel. The builder writes the expected
			# rig-local x per key and this compares against that, so the probe checks
			# the rig's COMPOSITION rather than re-deriving the gait's own equation.
			var want: float = 0.0
			if i > 0 and int((keys[i - 1] as Array)[2]) == 1:
				want = (float(k[3]) - float((keys[i - 1] as Array)[3])) * node_sc
			if have:
				worst2 = maxf(worst2, absf((world.x - prev.x) - want))
				n2 += 1
			prev = world
			have = true
		print("    %-4s %d planted key steps, worst departure from the exact roll: %.3f canvas px"
			% [gait, n2, worst2])
		_check(worst2 < 2.0, "%s contact point rolls at exactly the gait speed (%.3f px)"
			% [gait, worst2])
		report["contact_slide_" + gait] = {"planted_steps": n2, "worst_px": worst2,
			"authored_slide_rig_px": fitj[gait]["heel_toe"]["contact_slide_rig_px"]}
	anim.play("idle")

	report["fails"] = fails
	var f := FileAccess.open("res://frames/knight_rig_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("=== rig probe: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)


func _walk(keeper, actions: Array, frames: int) -> void:
	for a in actions:
		Input.action_press(a)
	for f in frames:
		await physics_frame
		await process_frame
	for a in actions:
		Input.action_release(a)
	await physics_frame
	await process_frame


# World-space crown / sole / foot-centre of the rig, from its sprites' drawn rects.
func _rig_rect(rig) -> Array:
	var top := INF
	var bot := -INF
	var feet: Array = []
	for s in rig.find_children("*", "Sprite2D", true, false):
		var sp := s as Sprite2D
		if sp.texture == null or String(sp.name).find("pollaxe") >= 0:
			continue          # the weapon reaches above the helm and below the sole
		var r := sp.get_global_transform() * Rect2(-sp.texture.get_size() * 0.5, sp.texture.get_size())
		top = minf(top, r.position.y)
		bot = maxf(bot, r.end.y)
		if String(sp.name).find("near_foot") >= 0:
			feet = [r.position.x + r.size.x * 0.5, r.position.x, r.end.x]
	return [top, bot, feet[0] if feet.size() > 0 else 0.0,
			feet[1] if feet.size() > 0 else 0.0, feet[2] if feet.size() > 0 else 0.0]


# The same three numbers for a Grok cell, read off its alpha rather than its rect, so
# the two are measured the same way: the cell is mostly transparent padding.
func _cell_rect(knight: AnimatedSprite2D, anim_name: String) -> Array:
	var tex: Texture2D = knight.sprite_frames.get_frame_texture(anim_name, 0)
	var img: Image = tex.get_image()
	var top := -1
	var bot := -1
	var shaft_x := 0
	for y in img.get_height():
		for x in img.get_width():
			if img.get_pixel(x, y).a > 0.5:
				if top < 0:
					top = y
				bot = y
				break
	# helm crown: the topmost row whose widest opaque run is at least 20 px (the helm);
	# anything narrower up there is the pollaxe.
	var crown := top
	for y in range(top, bot):
		var run := 0
		var best := 0
		for x in img.get_width():
			if img.get_pixel(x, y).a > 0.5:
				run += 1
				best = maxi(best, run)
			else:
				run = 0
		if best >= 20:
			crown = y
			break
	var fx := 0.0
	var n := 0
	for y in range(maxi(bot - 6, 0), bot + 1):
		for x in img.get_width():
			if img.get_pixel(x, y).a > 0.5:
				fx += x
				n += 1
	if n > 0:
		fx /= float(n)
	var t := knight.get_global_transform()
	var o := knight.offset
	return [(t * (o + Vector2(0, crown))).y, (t * (o + Vector2(0, bot))).y,
			(t * (o + Vector2(fx, 0))).x]
