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
const MODEL := "res://models/T8-barbarian.glb"
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
	var out := {}
	for clip in ["walk", "run"]:
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		anim.play(clip)
		var prev := [Vector3.ZERO, Vector3.ZERO]
		var steps := []
		var net := Vector3.ZERO
		for i in n + 1:
			var t: float = a.length * float(i) / float(n)
			anim.seek(t, true, true)
			await process_frame
			var p := []
			for b in idx:
				p.append(skel.global_transform * skel.get_bone_global_pose(b).origin)
			var s: int = 0 if p[0].y <= p[1].y else 1
			if i > 0:
				var d: Vector3 = p[s] - prev[s]
				d.y = 0.0
				steps.append(d.length())
				net += d
			prev = p
		# MEDIAN per-frame travel, not the sum. A planted foot moves at a constant rate, so
		# the median is that rate; the sum is contaminated by the two frames per cycle where
		# the stance foot swaps and the "previous position" belongs to a foot that was
		# swinging. Median x frames is the same quantity with those two frames outvoted.
		steps.sort()
		var med: float = steps[steps.size() / 2]
		var per_cycle_model: float = med * float(n)
		var per_cycle_world: float = per_cycle_model * SCALE
		var speed_m: float = per_cycle_world / a.length
		var speed_px: float = speed_m * PPM
		var back := net.normalized()
		say("")
		say("%s: %d frames, %.4f s per cycle" % [clip, n, a.length])
		say("   per-frame stance travel: median %.4f, min %.4f, max %.4f (metres)"
			% [med, steps[0], steps[-1]])
		say("   stride per cycle  %.4f m (model)  ->  %.4f m (world, x%.5f)"
			% [per_cycle_model, per_cycle_world, SCALE])
		say("   speed              %.3f m/s  =  %.1f canvas px/s across screen" % [speed_m, speed_px])
		say("   his BACKWARD axis %s   so FORWARD is %s"
			% [str(back.snappedf(0.001)), str((-back).snappedf(0.001))])
		out[clip] = {"frames": n, "cycle_s": a.length,
					 "stride_model_m": snappedf(per_cycle_model, 0.0001),
					 "stride_world_m": snappedf(per_cycle_world, 0.0001),
					 "speed_m_s": snappedf(speed_m, 0.001),
					 "speed_canvas_px_s": snappedf(speed_px, 0.1),
					 "forward_axis": [snappedf(-back.x, 0.001), 0.0, snappedf(-back.z, 0.001)]}
	say("")
	say("the Keeper's own, for comparison: walk 247 px/s, run 494 px/s")
	say("   walk  %.1f px/s  = %.2fx the Keeper" % [out["walk"]["speed_canvas_px_s"], out["walk"]["speed_canvas_px_s"] / 247.0])
	say("   run   %.1f px/s  = %.2fx the Keeper" % [out["run"]["speed_canvas_px_s"], out["run"]["speed_canvas_px_s"] / 494.0])
	var f := FileAccess.open(ProjectSettings.globalize_path("user://stride.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " "))
	f.close()
	print("-> ", ProjectSettings.globalize_path("user://stride.json"))
	quit(0)
