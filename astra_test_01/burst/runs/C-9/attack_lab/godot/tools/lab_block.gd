extends SceneTree
# BLOCK: press -> raise -> hold -> release -> lower -> guard, measured every 1/96 s.
#   time to full guard  press -> the shield hand within 2 cm (body frame) of the block's PEAK
#                       pose AND the block blended fully in
#   raise visibly plays how many 1/24 s game frames the hand spends rising, and how far
#   hold                the hand's drift while held
#   back to guard       release -> the block blend fully out
const DT := 1.0 / 96.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	var cs := CollisionShape3D.new(); var box := BoxShape3D.new(); box.size = Vector3(600, 1, 600)
	cs.shape = box; cs.position = Vector3(0, -0.5, 0); ground.add_child(cs); root.add_child(ground)
	var k: CharacterBody3D = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, 1.10)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	var tree: AnimationTree = k._tree
	var skel: Skeleton3D = k._skel
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(k.gear_stack_count() - 1)
	k.global_position = Vector3(0, 0.02, 0)
	var patched: bool = tree.tree_root.has_node("ts_block")
	var hb := skel.find_bone("LeftHand")
	var hand := func() -> Vector3:
		return k.global_transform.affine_inverse() * (skel.global_transform * skel.get_bone_global_pose(hb).origin)
	for i in 96:
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel)
	var guard: Vector3 = hand.call()
	# the PEAK pose's hand, in the body frame: the raw block clip at its peak, blended fully
	var peak_hand := Vector3.ZERO
	var rows := []
	k.set_block(true)
	var t := 0.0
	for i in int(1.5 / DT):
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel); t += DT
		rows.append([t, (hand.call() as Vector3), k._block_w, float(tree.get("parameters/a_block/current_position")),
					 String(k.get("_block_phase")) if patched else "-"])
	peak_hand = rows[-1][1]
	var full := -1.0
	for r in rows:
		if full < 0.0 and float(r[2]) >= 0.999 and ((r[1] as Vector3) - peak_hand).length() <= 0.02:
			full = float(r[0])
	# rising frames at 24 fps: hand height increasing between consecutive game frames
	var rising := 0
	var travel := 0.0
	for i in range(4, rows.size(), 4):
		var dy: float = (rows[i][1] as Vector3).y - (rows[i - 4][1] as Vector3).y
		var d: float = ((rows[i][1] as Vector3) - (rows[i - 4][1] as Vector3)).length()
		if float(rows[i][0]) <= maxf(full, 0.0) + 0.001 and d > 0.004:
			rising += 1
			travel += d
	var hold_lo := Vector3(1e9, 1e9, 1e9); var hold_hi := -hold_lo
	for r in rows:
		if float(r[0]) >= 1.0:
			hold_lo = hold_lo.min(r[1]); hold_hi = hold_hi.max(r[1])
	var hold_drift: float = (hold_hi - hold_lo).length()
	k.set_block(false)
	var back := -1.0
	var t2 := 0.0
	var low_frames := 0
	var prev: Vector3 = hand.call()
	for i in int(1.5 / DT):
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel); t2 += DT
		if i % 4 == 3:
			var h: Vector3 = hand.call()
			if (h - prev).length() > 0.004: low_frames += 1
			prev = h
		if back < 0.0 and k._block_w <= 0.001:
			back = t2
	print("[block] %s | block clip at %.3f s when pressed-and-held 1.5 s; peak hand %.3f m above guard's"
		% ["PATCHED" if patched else "SHIPPED", float(rows[-1][3]), peak_hand.y - guard.y])
	print("[block] time to full guard: %s | raise plays over %d game frames (1/24 s), hand travels %.3f m | hold drift %.4f m | back to guard %.3f s after release, lower over %d game frames"
		% ["%.3f s" % full if full >= 0.0 else "NEVER", rising, travel, hold_drift, back, low_frames])
	var line := ""
	for i in range(0, mini(rows.size(), 40), 2):
		line += "%.3f:%s:w%.2f:y%.3f " % [float(rows[i][0]), String(rows[i][4]), float(rows[i][2]), (rows[i][1] as Vector3).y]
	print("[block] first 0.4 s: " + line)
	# A STRIKE DURING A BLOCK: after the strike, is he back in guard, or holding the shield up?
	k.set_block(true)
	for i in 48:
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel)
	var fired: bool = k.try_strike("slash")
	var g := 0
	while (k.attacking() or g < 12) and g < 2000:
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel); g += 1
	for i in 48:
		k.drive_dir(Vector2.ZERO, false, DT); tree.advance(DT); _mods(k, skel)
	print("[block] strike during a held block: fired=%s; 0.5 s after the strike -> block weight %.3f, phase '%s' (want 0.000, off)"
		% [str(fired), k._block_w, String(k.get("_block_phase")) if patched else "-"])
	quit(0)

func _mods(k, skel: Skeleton3D) -> void:
	if k._foot_lock != null:
		if skel.modifier_callback_mode_process != Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL:
			skel.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
		skel.advance(1.0 / 96.0)
		skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
