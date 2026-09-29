extends SceneTree
# IN-PLACE OR ROOT MOTION? An in-place clip's hips return to where they started; a
# travelling clip's do not. The distinction decides whether the scene may move the body
# under the clip at all, and no amount of stance-foot measurement can tell them apart --
# a correctly grounded foot in a travelling clip is STATIONARY, which reads as "no stride".
const MODEL := "res://models/gear/nb-body.glb"
const SCALE := 1.25178
const PPM := 100.617553710938
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
	var hips := skel.find_bone("Hips")
	print("  clip                  hips net travel   per-frame     implied speed   verdict")
	for clip in ["walk", "run", "idle_armed", "walk_armed", "run_armed", "run_armed_locked",
				 "strafe_L_armed", "block", "shield_bash", "attack_chop"]:
		if not anim.has_animation(clip): continue
		var a := anim.get_animation(clip)
		var n := int(round(a.length * 24.0))
		anim.play(clip)
		anim.seek(0.0, true, true)
		await process_frame
		var p0: Vector3 = skel.global_transform * skel.get_bone_global_pose(hips).origin
		var mx := 0.0
		var last := p0
		for i in n + 1:
			anim.seek(a.length * float(i) / float(n), true, true)
			await process_frame
			var p: Vector3 = skel.global_transform * skel.get_bone_global_pose(hips).origin
			var d := p - p0; d.y = 0.0
			mx = maxf(mx, d.length())
			last = p
		var net := last - p0; net.y = 0.0
		var spd: float = net.length() * SCALE / a.length
		print("  %-20s %8.4f m       %7.4f m    %6.3f m/s = %6.1f px/s   %s" %
			[clip, net.length(), net.length() / float(n), spd, spd * PPM,
			 "ROOT MOTION" if net.length() > 0.25 else "in place (max excursion %.3f m)" % mx])
	quit(0)
