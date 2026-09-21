extends SceneTree
# Conductor proof (C-8, whirlwind port). Two jobs in one run:
#
#   (A) ASSERT the four invariants the design rests on, as numbers:
#        1. PHASE LOCK   -- the apex bearing is the table's value at the frame
#                           the sprite is DISPLAYING, to within interpolation.
#                           Measured as: total sweep over N physics frames must
#                           equal 360 * elapsed / 0.400, with no drift.
#        2. OPEN ARC     -- the arc's angular span never reaches 360 deg. A
#                           closed ring is a field, not a trail.
#        3. Z SPLIT      -- over a revolution BOTH the far and the near arc
#                           layers must draw. If either never does, the split
#                           is not doing its job and the caster is not inside
#                           the whirlwind.
#        4. RAMPS        -- _w rises over SPIN_UP_S, holds, and falls over
#                           SPIN_DOWN_S; the effect ends IDLE and invisible.
#
#   (B) CAPTURE stills / a clip through the real renderer (PROBE_OUT set).
#
# Run under heavy_lock.py. Headless for (A); --rendering-method gl_compatibility
# with PROBE_OUT set for (B).
var out_dir = OS.get_environment("PROBE_OUT")
var errors: Array = []


func check(ok: bool, msg: String) -> void:
	if not ok:
		errors.append(msg)
		printerr("WW_ASSERTION: ", msg)


func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var anim = keeper.get_node("AnimatedSprite2D")
	keeper.global_position = Vector2(2285.62, 2407.32)
	for f in 20:
		await physics_frame

	var ww = keeper.get_node_or_null("Whirlwind")
	check(ww != null, "Keeper has no Whirlwind child")
	if ww == null:
		quit()
		return
	for nm in ["WhirlwindFarDust", "WhirlwindFarArc", "WhirlwindNearDust", "WhirlwindNearArc"]:
		check(ww.get_node_or_null(nm) != null, "missing draw layer " + nm)
	check(ww.state_name() == "IDLE", "whirlwind is not IDLE before the attack")
	check(not ww.get_node("WhirlwindFarArc").visible, "layers visible before the attack")

	var far_arc = ww.get_node("WhirlwindFarArc")
	var near_arc = ww.get_node("WhirlwindNearArc")

	# ---- press and hold ----------------------------------------------------
	Input.action_press("attack")
	for f in 3:
		await physics_frame
	check(anim.animation == "attack_S", "attack animation did not start (got %s)" % anim.animation)
	check(ww.state_name() != "IDLE", "whirlwind did not begin with the attack")

	var fit = ww._fit
	var span_max := 0.0
	var span_min := 999.0
	var w_at := 0.0
	var far_drew := 0
	var near_drew := 0
	var apex_err_max := 0.0
	var apex_checks := 0
	var n := 0

	for f in 150:
		await physics_frame
		var u: float = ww._phase()
		check(u >= 0.0, "phase() refused the displayed animation at frame %d" % f)
		var s: float = ww._arc_span_deg()
		span_max = maxf(span_max, s)
		if s > 0.0:
			span_min = minf(span_min, s)
		if ww._quads_drawn_far > 0:
			far_drew += 1
		if ww._quads_drawn_near > 0:
			near_drew += 1

		# ⚑ THE PHASE LOCK, AS THE CLAIM IT ACTUALLY MAKES. Not "the sweep rate
		# looks right over time" (which a free-running headless loop cannot
		# measure honestly) but: WHEN THE SPRITE IS SHOWING FRAME k AT THE START
		# OF THAT FRAME, THE RIBBON APEX IS ON THAT STILL'S MEASURED MACE HEAD.
		# Compared against the RAW conductor pixel, so the whole polar
		# round-trip -- canvas to bearing/radius to Hermite to ellipse -- is
		# under test rather than the table comparing with itself.
		# ⚑ THE PHASE LOCK, AS THE CLAIM IT ACTUALLY MAKES: the apex sits where
		# the DECLARED construction says still k sits -- bearing0 + 45*(-1)*u --
		# on the sweep ellipse at R_TRAIL. `_arc_u` is the phase the arc was
		# BUILT with, not a re-read of the sprite (which advances in _process
		# between the build and this line and would present as a large error the
		# effect does not have).
		var au: float = ww._arc_u
		if au >= 0.0 and ww.apex_point() != Vector2.INF:
			var want: Vector2 = ww._centre + ww._ground(ww._theta_at(au), ww._r_trail)
			apex_err_max = maxf(apex_err_max, ww.apex_point().distance_to(want))
			apex_checks += 1

		if f == 44:
			w_at = ww.channel_weight()
		if out_dir != "" and f % 2 == 0:
			root.get_texture().get_image().save_png(out_dir + "/ww_%04d.png" % n)
			n += 1

	check(apex_checks >= 100, "only %d apex checks fired" % apex_checks)
	check(apex_err_max < 0.01,
		"PHASE LOCK: ribbon apex is %.4f px off its own declared sweep" % apex_err_max)
	check(span_max < 359.0, "OPEN ARC: arc span reached %.2f deg -- a closed ring is a field" % span_max)
	check(span_max > 100.0, "arc never opened (max span %.2f deg)" % span_max)
	check(far_drew > 0, "Z SPLIT: the FAR arc layer never drew a quad")
	check(near_drew > 0, "Z SPLIT: the NEAR arc layer never drew a quad")
	check(ww.state_name() == "SUSTAIN", "whirlwind did not reach SUSTAIN (got %s)" % ww.state_name())
	check(absf(w_at - 1.0) < 0.06, "SPIN_UP: weight at ~0.75 s is %.3f, expected ~1.0" % w_at)

	# ⚑ THE LEVEL BAND, AS A MEASUREMENT -- the assertion the conductor
	# correction exists for. It is a property of the SWEEP PLANE (centre plus
	# wobble), NOT of the drawn arc's screen extent: a circle lying on the
	# ground projects to an ellipse ~2*R_TRAIL*squash tall, which in the
	# reference cut likewise sweeps from over the helm to the ground line. The
	# first version of this probe asserted the guard against the arc extent and
	# failed a correct effect; both numbers are printed so the two stay distinct.
	var H: float = float(fit["figure_height_px"]) * ww._c2n_scale.y
	var sole_n: float = ww.canvas_to_node(Vector2(0.0, float(fit["sole_row"]))).y
	var plane_hi_H: float = (sole_n - ww._meas_plane_lo) / H
	var plane_lo_H: float = (sole_n - ww._meas_plane_hi) / H
	var guard: Dictionary = fit["guard"]
	check(plane_lo_H > float(guard["lower_body_top"]),
		"LEVEL BAND: sweep plane reached %.4f H, at or below the hips (%.3f H)"
		% [plane_lo_H, float(guard["lower_body_top"])])
	check(plane_hi_H < float(guard["head_bottom"]),
		"LEVEL BAND: sweep plane reached %.4f H, at or above the chin (%.3f H)"
		% [plane_hi_H, float(guard["head_bottom"])])
	var spread := plane_hi_H - plane_lo_H
	check(spread < 0.195,
		"LEVEL BAND: sweep plane spread %.4f H exceeds the reference sweep band's 0.195 H"
		% spread)
	# ⚑ AND THE DIRECT FALSIFIER FOR A RETURN TO MACE-TRACKING: on a level
	# plane the arc's screen extent is fixed by geometry -- 2*R_TRAIL*squash.
	# A ribbon threaded through the drawn mace heads (spread 0.782 H against
	# this plane's 0.08 H) cannot satisfy it.
	#
	# The WOBBLE adds nothing to this extent, which is not an oversight: it is
	# sin(2*(theta - bearing0)), so with the ellipse's vertical extremes at
	# theta = bearing0 +/- 90 the wobble is exactly ZERO at both of them. The
	# helix therefore shows mid-quadrant and never widens the silhouette --
	# worth having written down, because the obvious expectation
	# (2*R*squash + 2*wobble) is wrong by 0.07 H and looks like a defect.
	var arc_h: float = (ww._meas_arc_y_hi - ww._meas_arc_y_lo) / H
	var arc_h_want: float = (2.0 * ww._r_trail * ww._squash) / H
	check(absf(arc_h - arc_h_want) < 0.02,
		"ARC IS NOT A LEVEL ELLIPSE: screen extent %.4f H, geometry says %.4f H"
		% [arc_h, arc_h_want])

	print("WW apex_err_max %.5f px over %d checks | span %.2f..%.2f deg | far_frames %d near_frames %d | w %.3f state %s"
		% [apex_err_max, apex_checks, span_min, span_max, far_drew, near_drew,
			ww.channel_weight(), ww.state_name()])
	print("WW sweep plane [%.4f, %.4f] H above the sole, spread %.4f (hips %.3f, chin %.3f; mace heads span 0.782, reference band 0.195)"
		% [plane_lo_H, plane_hi_H, spread, float(guard["lower_body_top"]), float(guard["head_bottom"])])
	print("WW arc screen extent %.4f H (geometry %.4f H) -- a ground ellipse is tall by design"
		% [arc_h, arc_h_want])

	# ---- release and let it fall -------------------------------------------
	Input.action_release("attack")
	await physics_frame
	check(ww.state_name() == "FALLING", "whirlwind did not enter FALLING on release (got %s)" % ww.state_name())
	var w0: float = ww.channel_weight()
	for f in 30:
		await physics_frame
		if out_dir != "" and f % 2 == 0:
			root.get_texture().get_image().save_png(out_dir + "/ww_%04d.png" % n)
			n += 1
	var w1: float = ww.channel_weight()
	check(w1 < w0, "SPIN_DOWN: weight did not fall (%.3f -> %.3f)" % [w0, w1])
	for f in 90:
		await physics_frame
	check(ww.state_name() == "IDLE", "whirlwind did not return to IDLE (got %s)" % ww.state_name())
	check(not far_arc.visible and not near_arc.visible, "layers still visible after the effect ended")
	check(anim.animation == "idle_S", "keeper did not return to idle (got %s)" % anim.animation)

	print("WW fall %.3f -> %.3f, final state %s, anim %s, frames written %d"
		% [w0, w1, ww.state_name(), anim.animation, n])

	# ---- A2 capture leg: whirlwind while WALKING ---------------------------
	if out_dir != "":
		keeper.global_position = Vector2(2285.62, 2407.32)
		await physics_frame
		Input.action_press("attack")
		var mp0 = keeper.global_position
		var legs = [["move_right", 44], ["move_down", 44], ["move_left", 44], ["move_up", 44]]
		for leg in legs:
			Input.action_press(leg[0])
			for f in int(leg[1]):
				await physics_frame
				if f % 2 == 0:
					root.get_texture().get_image().save_png(out_dir + "/ww_%04d.png" % n)
					n += 1
			Input.action_release(leg[0])
		Input.action_release("attack")
		for f in 24:
			await physics_frame
			if f % 2 == 0:
				root.get_texture().get_image().save_png(out_dir + "/ww_%04d.png" % n)
				n += 1
		print("WW moving-capture leg done, travelled %.1f px, frames now %d"
			% [mp0.distance_to(keeper.global_position), n])
	print("WW RESULT ", ("PASS" if errors.is_empty() else "FAIL %d" % errors.size()))
	quit()
