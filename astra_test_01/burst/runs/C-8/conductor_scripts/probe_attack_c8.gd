extends SceneTree
# Conductor proof (C-8, attack port): for each of the eight facings, face that way, press attack (F),
# and check that the attack_<DIR> cell plays, that the figure does not move while attacking,
# and that it returns to idle on release. Also checks that cast/jump cannot start mid-attack.
func _initialize():
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var keeper = scene.find_child("Keeper", true, false)
	var anim = keeper.get_node("AnimatedSprite2D")
	var start = Vector2(2285.62, 2407.32)
	var tests = [["S", ["move_down"]], ["SW", ["move_down", "move_left"]], ["W", ["move_left"]], ["NW", ["move_up", "move_left"]], ["N", ["move_up"]], ["NE", ["move_up", "move_right"]], ["E", ["move_right"]], ["SE", ["move_down", "move_right"]]]
	for t in tests:
		keeper.global_position = start
		await physics_frame
		# face the direction first
		for a in t[1]:
			Input.action_press(a)
		for f in 10:
			await physics_frame
		for a in t[1]:
			Input.action_release(a)
		await physics_frame
		var p0 = keeper.global_position
		Input.action_press("attack")
		var seen = {}
		var frames_seen = {}
		for f in 40:
			await physics_frame
			seen[anim.animation] = true
			frames_seen[anim.frame] = true
		# try to interrupt with cast + jump mid-attack
		Input.action_press("cast")
		Input.action_press("jump")
		await physics_frame
		await physics_frame
		var during_interrupt = anim.animation
		Input.action_release("cast")
		Input.action_release("jump")
		for f in 10:
			await physics_frame
		var moved = p0.distance_to(keeper.global_position)
		Input.action_release("attack")
		var after = ""
		for f in 20:
			await physics_frame
			after = anim.animation
		print("ATK ", t[0], " anims ", seen.keys(), " distinct_frames ", frames_seen.size(), " moved ", moved, " interrupt_anim ", during_interrupt, " after_release ", after, " expect attack_", t[0], " -> idle_", t[0])

	# ------------------------------------------------------------------
	# A2: the whirlwind TRAVELS at walk pace. Two legs per direction --
	#   (a) WALK leg: the direction held alone, no attack. The reference
	#       distance, measured rather than assumed, because walkable-ground
	#       collision can shorten either leg and only a same-ground comparison
	#       is honest.
	#   (b) SPIN leg: the same direction held WITH attack. Must cover about the
	#       same ground, must still be playing attack_<DIR>, and must never
	#       exceed the walk leg (run_modifier is ignored during attack, so a
	#       spin leg LONGER than the walk leg would mean run speed leaked in).
	# Also re-asserts the stationary case: attack held, no direction, 0.0 px.
	# ------------------------------------------------------------------
	var legs = 40
	for t in tests:
		# (a) walk
		keeper.global_position = start
		for a in t[1]:
			Input.action_press(a)
		await physics_frame
		var wp0 = keeper.global_position
		for f in legs:
			await physics_frame
		var walked = wp0.distance_to(keeper.global_position)
		var walk_anim = anim.animation
		for a in t[1]:
			Input.action_release(a)
		for f in 5:
			await physics_frame

		# (b) spin-walk
		keeper.global_position = start
		await physics_frame
		Input.action_press("attack")
		for a in t[1]:
			Input.action_press(a)
		await physics_frame
		var sp0 = keeper.global_position
		var spin_anims = {}
		var spin_frames = {}
		for f in legs:
			await physics_frame
			spin_anims[anim.animation] = true
			spin_frames[anim.frame] = true
		var spun = sp0.distance_to(keeper.global_position)
		for a in t[1]:
			Input.action_release(a)
		# (c) stationary while still holding attack
		await physics_frame
		var st0 = keeper.global_position
		for f in 20:
			await physics_frame
		var stationary_drift = st0.distance_to(keeper.global_position)
		Input.action_release("attack")
		for f in 15:
			await physics_frame

		var ratio = (spun / walked) if walked > 0.0 else -1.0
		print("A2 ", t[0], " walked ", walked, " spun ", spun, " ratio ", ratio,
			" spin_anims ", spin_anims.keys(), " spin_distinct_frames ", spin_frames.size(),
			" stationary_drift ", stationary_drift, " walk_anim ", walk_anim,
			" after ", anim.animation, " expect ratio ~1.0, attack_", t[0], ", drift 0.0")
	quit()
