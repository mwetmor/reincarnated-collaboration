extends SceneTree
# Conductor CAPTURE probe (C-8 whirlwind). Separate from probe_whirlwind_c8.gd,
# which asserts; this one only produces frames for Matt to look at.
#
# ⚑ IT SAVES ON RENDER FRAMES, NOT PHYSICS FRAMES, AND THAT IS THE WHOLE POINT.
#
# The first capture pass awaited `physics_frame` and saved every second one.
# Measured afterwards: 190 files containing 50 DISTINCT images, in repeat runs
# of up to 4 -- the windowed renderer was running at roughly a quarter of the
# physics rate, so three quarters of the clip was duplicated stills.
#
# That is not merely a cosmetic flaw in the clip. The whirlwind turns at
# 2.5 rev/s; at ~7.5 effective fps that is THREE SAMPLES PER REVOLUTION, which
# is below the Nyquist limit for the rotation. A correctly clockwise spin
# sampled three times a turn ALIASES and can read as anticlockwise to the eye.
# So a judgement about rotation direction made from such a clip is worthless in
# either direction -- including a judgement that the direction is now correct.
#
# `process_frame` fires once per rendered frame, so one save per fire is one
# save per distinct image by construction.
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
	var start = Vector2(2285.62, 2407.32)
	keeper.global_position = start
	for f in 20:
		await process_frame

	# --- leg 1: stationary spin, ~2.5 s -----------------------------------
	Input.action_press("attack")
	for f in 150:
		await process_frame
		shot()
	# --- leg 2: spin while walking a square, ~3.0 s ------------------------
	for leg in [["move_right", 45], ["move_down", 45], ["move_left", 45], ["move_up", 45]]:
		Input.action_press(leg[0])
		for f in int(leg[1]):
			await process_frame
			shot()
		Input.action_release(leg[0])
	# --- leg 3: release and let it spin down --------------------------------
	Input.action_release("attack")
	for f in 60:
		await process_frame
		shot()

	print("CAP frames %d  anim %s  pos %s" % [n, anim.animation, keeper.global_position])
	quit()
