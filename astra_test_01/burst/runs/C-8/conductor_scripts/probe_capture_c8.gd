extends SceneTree
# Conductor CAPTURE probe (C-8 whirlwind). Produces frames for Matt to look at.
# It asserts nothing about gameplay -- probe_attack_c8.gd and
# probe_whirlwind_c8.gd do that, headlessly. This one only has to produce a
# clip that is honestly sampled and actually contains the effect.
#
# ---------------------------------------------------------------------------
# ⚑ TWO THINGS THIS SCRIPT EXISTS TO GET RIGHT, BOTH LEARNED THE HARD WAY.
#
# 1. IT SAVES ON RENDER FRAMES AT A FIXED TIMESTEP, NOT ON PHYSICS FRAMES.
#    The first capture pass awaited `physics_frame` and saved every second one.
#    Measured afterwards: 190 files holding 50 DISTINCT images, in repeat runs
#    of up to 4 -- the windowed renderer ran at about a quarter of the physics
#    rate. The whirlwind turns at 2.5 rev/s, so that is ~3 SAMPLES PER
#    REVOLUTION: below Nyquist for the rotation. A correctly-turning spin
#    sampled three times a turn ALIASES and can read the wrong way round. Any
#    direction judgement from such a clip is worthless IN EITHER DIRECTION --
#    including a judgement that the direction is now correct.
#    Run with `--fixed-fps 60` and one save per `process_frame`: one save per
#    distinct image, at a known 1/60 s apart.
#
# 2. IT DOES NOT USE THE INPUT SYSTEM AT ALL, AND THAT IS DELIBERATE.
#    A capture must be windowed (it needs a real renderer), and a windowed run
#    loses focus; Godot then releases every simulated action. Observed three
#    times, each worse than the last: a full 390-frame capture of the character
#    STANDING IDLE that looked like a finished clip; then a drop at captured
#    frame 106 despite re-pressing every frame; then a drop at frame 28 even
#    with `InputEventAction` injection plus `window_move_to_foreground()`.
#    The press cannot be made reliable from inside the process it is racing.
#
#    So the capture drives the keeper DIRECTLY: it holds the attack state, the
#    animation and the VFX itself, and translates the body by hand for the
#    walking leg. What that gives up is coverage of the INPUT GATE -- which is
#    not this script's job and is already asserted, headlessly and
#    deterministically, by probe_attack_c8.gd (8/8 directions, walk/spin ratio,
#    stationary drift). Conflating the two is what produced the idle clip.
# ---------------------------------------------------------------------------
var out_dir = OS.get_environment("PROBE_OUT")
var n := 0


func shot() -> void:
	if out_dir != "":
		root.get_texture().get_image().save_png(out_dir + "/cap_%04d.png" % n)
		n += 1


func _initialize():
	Engine.physics_ticks_per_second = 60
	Engine.max_fps = 60
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var anim = keeper.get_node("AnimatedSprite2D")
	var ww = keeper.get_node_or_null("Whirlwind")
	if ww == null:
		printerr("CAP_ASSERTION: no Whirlwind node -- run whirlwind_patch.py first")
		quit(1)
		return
	var start = Vector2(2285.62, 2407.32)
	keeper.global_position = start
	for f in 10:
		await process_frame

	# Take the keeper off input entirely and hold the attack state by hand.
	keeper.set_physics_process(false)
	keeper.state = "attack"
	keeper.facing = "S"
	keeper._play_state()
	ww.begin()
	await physics_frame
	if anim.animation != "attack_S" or ww.state_name() == "IDLE":
		printerr("CAP_ASSERTION: spin did not engage (anim=%s ww=%s)"
			% [anim.animation, ww.state_name()])
		quit(1)
		return

	# --- leg 1: stationary spin, 2.5 s ------------------------------------
	for f in 150:
		await process_frame
		shot()

	# --- leg 2: spin while travelling a square, 3.0 s ----------------------
	# Translated by hand at the keeper's own walk_speed. The INPUT-driven
	# version of this (direction changes, phase-preserving cell switch, walk
	# pace, walkable ground) is what probe_attack_c8.gd asserts; here it only
	# has to look like a man walking while spinning.
	var step: float = float(keeper.walk_speed) / 60.0
	for dir in [Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT, Vector2.UP]:
		for f in 45:
			await process_frame
			keeper.global_position += dir * step
			shot()

	# --- leg 3: release and let it spin down -------------------------------
	ww.end()
	for f in 60:
		await process_frame
		shot()

	print("CAP frames %d  anim %s  ww %s  pos %s  drift-from-start %.2f px"
		% [n, anim.animation, ww.state_name(), keeper.global_position,
			start.distance_to(keeper.global_position)])
	quit()
