extends SceneTree
# C-9 R-C9-69: how fast does the barbarian walk, and which way does he face?
#
# BOTH FROM THE CLIPS, not from a number anyone chose. The clips are in-place, so the
# ground moves under him: the STANCE foot -- whichever is lower at a given frame -- travels
# backwards at exactly the speed he would move forwards. Integrating that travel over one
# cycle gives the distance per cycle, and its NET DIRECTION is the model's own backward
# axis, so the same measurement answers "which way does he face" without a guess about
# what the exporter did with Blender's -Y.
#
#   Godot --headless --path godot --script tools/probe_stride.gd
const MODEL := "res://models/gear/nb-body.glb"
const SCALE := 1.25178
const PPM := 100.617553710938
const FEET := ["LeftToeBase", "RightToeBase"]

var lines: Array[String] = []
func say(s): print(s); lines.append(str(s))

func _initialize():
	var glb := (load(MODEL) as PackedScene).instantiate()
	root.add_child(glb)
	await process_frame
	var skel: Skeleton3D = null
	var anim: AnimationPlayer = null
	for n in glb.find_children("*", "", true, false):
		if n is Skeleton3D: skel = n
		elif n is AnimationPlayer: anim = n
	anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var idx := []
	for f in FEET:
		idx.append(skel.find_bone(f))
	# WHAT UNIT ARE BONE POSES IN? Not metres, necessarily: a rig exported from a
	# centimetre scene carries its own unit and the importer puts the compensating scale on
	# the Skeleton3D, so get_bone_global_pose returns pose units. Reading a 138 m walk
	# stride is what that looks like. Measure the factor against the one length that IS in
	# metres -- the mesh AABB -- instead of assuming 1 or 100.
	var mesh: MeshInstance3D = null
	for n2 in glb.find_children("*", "MeshInstance3D", true, false):
		mesh = n2
		break
	var top_m: float = mesh.get_aabb().position.y + mesh.get_aabb().size.y
	var he := skel.find_bone("head_end")
	anim.play("idle")
	anim.seek(0.0, true, true)
	await process_frame
	var top_pose: float = skel.get_bone_global_pose(he).origin.y if he >= 0 else 0.0
	var top_world: float = (skel.global_transform * skel.get_bone_global_pose(he).origin).y
	# NO UNIT FACTOR. Poses come back in the rig's own units -- 188.7 for a head that is
	# 1.85 m up, so the rig is in centimetres -- and dividing by a factor estimated from a
	# bone TIP against a mesh TOP carries that estimate's error into the speed. The
	# skeleton's own global transform converts exactly, so the feet are read in metres and
	# there is nothing to estimate.
	say("head_end: pose %.4f  ->  world %.4f m   (mesh top %.4f m)" % [top_pose, top_world, top_m])
	say("")
	say("GROUNDING -- deepest foot in each clip the scene uses, world metres above the root")
	for clip in ["idle", "walk", "run", "idle_armed", "walk_armed", "run_armed",
				 "strafe_L_armed", "block", "shield_guard_L", "attack", "attack_chop", "shield_bash"]:
		if not anim.has_animation(clip): continue
		var a0 := anim.get_animation(clip)
		var n0 := mini(int(round(a0.length * 24.0)), 40)
		anim.play(clip)
		var lo := 1e9
		for i in n0 + 1:
			anim.seek(a0.length * float(i) / float(maxi(n0, 1)), true, true)
			await process_frame
			for b in idx:
				lo = minf(lo, (skel.global_transform * skel.get_bone_global_pose(b).origin).y)
		say("   %-18s deepest foot %+.4f m" % [clip, lo])
	say("")
	var out := {}
	for clip in ["walk", "walk_armed", "run", "run_armed", "run_armed_locked", "strafe_L_armed"]:
		if not anim.has_animation(clip):
			say("%s: NOT IN THIS BUILD" % clip); continue
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		anim.play(clip)
		var prev := [Vector3.ZERO, Vector3.ZERO]
		var rows := []
		var prev_h := 1e9
		var prev_s := -1
		for i in n + 1:
			var tt: float = a.length * float(i) / float(n)
			anim.seek(tt, true, true)
			await process_frame
			var pp := []
			for b in idx:
				pp.append(skel.global_transform * skel.get_bone_global_pose(b).origin)
			var s: int = 0 if pp[0].y <= pp[1].y else 1
			var h: float = pp[s].y
			if i > 0 and s == prev_s:
				var d: Vector3 = pp[s] - prev[s]
				d.y = 0.0
				rows.append([d.length(), h, prev_h, d])
			prev = pp
			prev_h = h
			prev_s = s
		# CONTACT-FILTERED, because the median over ALL frames is not the stance rate. A
		# 60-frame retargeted run holds four gait cycles and is airborne or swinging for
		# most of them, so the plain median lands on a SWINGING foot -- which reported the
		# retargeted run at 1.179 m/s against its author's 4.33, and turned its forward
		# axis round to point backwards. A foot on the ground is one at the bottom of its
		# own range whose height is not changing, on BOTH frames of the pair.
		var lo := 1e9
		for r in rows: lo = minf(lo, float(r[1]))
		var steps := []
		var net := Vector3.ZERO
		for r in rows:
			if float(r[1]) <= lo + 0.03 and float(r[2]) <= lo + 0.03 \
					and absf(float(r[1]) - float(r[2])) <= 0.010:
				steps.append(float(r[0]))
				net += r[3]
		if steps.is_empty():
			say("%s: NO CONTACT PAIRS -- cannot measure" % clip); continue
		steps.sort()
		var med: float = steps[steps.size() / 2]
		# the stance rate IS the speed: while a foot is planted the ground goes by at
		# exactly the rate he would travel. No cycle counting, which is the other thing
		# that went wrong -- "stride per cycle" assumes the clip is one cycle and these
		# are not.
		var speed_m: float = med * 24.0 * SCALE
		var speed_px: float = speed_m * PPM
		var back := net.normalized()
		say("")
		say("%s: %d frames, %.4f s, %d contact pairs of %d" % [clip, n, a.length, steps.size(), rows.size()])
		say("   stance travel per frame: median %.4f, min %.4f, max %.4f m (contact only)"
			% [med, steps[0], steps[-1]])
		say("   speed              %.3f m/s  =  %.1f canvas px/s  (at figure scale %.5f)" % [speed_m, speed_px, SCALE])
		say("   his BACKWARD axis %s   so FORWARD is %s"
			% [str(back.snappedf(0.001)), str((-back).snappedf(0.001))])
		var fwd_deg: float = rad_to_deg(atan2(-back.x, -back.z))
		say("   forward is %+.1f deg off the model's +Z" % fwd_deg)
		out[clip] = {"frames": n, "length_s": a.length, "contact_pairs": steps.size(),
					 "stance_median_m_per_frame": snappedf(med, 0.0001),
					 "speed_m_s": snappedf(speed_m, 0.001),
					 "speed_canvas_px_s": snappedf(speed_px, 0.1),
					 "forward_deg_off_Z": snappedf(rad_to_deg(atan2(-back.x, -back.z)), 0.1),
					 "forward_axis": [snappedf(-back.x, 0.001), 0.0, snappedf(-back.z, 0.001)]}
	var f := FileAccess.open(ProjectSettings.globalize_path("user://stride_armed.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("-> ", ProjectSettings.globalize_path("user://stride_armed.json"))
	quit(0)
