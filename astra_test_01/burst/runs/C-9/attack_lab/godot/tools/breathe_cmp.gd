extends SceneTree
# Breathe: source rig vs merged body rig, on measures that do not care about placement or the
# 1.088 rig-scale ratio -- each foot relative to the HIPS, and the foot-to-foot distance.
# If the merge preserved the pose, the source's numbers x1.088 are the merged numbers.
func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("LAB WATCHDOG"); quit(4))
	var src := await _rig("res://models/axe_breathe.glb")
	var mer := await _rig("res://models/gear/nb-body.glb")
	var sname: String = String((src[1] as AnimationPlayer).get_animation_list()[0])
	var A := _series(src, sname)
	var B := _series(mer, "idle_armed")
	for key in ["feet_apart", "L_from_hips", "R_from_hips", "hips_h"]:
		var a: Array = A[key]; var b: Array = B[key]
		print("%-12s SOURCE %.3f..%.3f (range %.3f)  x1.088 -> %.3f..%.3f | MERGED %.3f..%.3f (range %.3f)"
			% [key, a.min(), a.max(), a.max() - a.min(), a.min() * 1.088, a.max() * 1.088, b.min(), b.max(), b.max() - b.min()])
	print("frame-0 pose, left leg bone GLOBAL directions (source vs merged, deg apart):")
	var line := ""
	for bn in ["Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot"]:
		line += "%s %.1f  " % [bn, _dir_deg(src, sname, mer, "idle_armed", bn)]
	print("  " + line)
	quit(0)

func _rig(path: String) -> Array:
	var ps := ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	var r := ps.instantiate()
	root.add_child(r)
	await process_frame
	await process_frame
	var sk: Skeleton3D = r.find_children("*", "Skeleton3D", true, false)[0]
	var ap: AnimationPlayer = r.find_children("*", "AnimationPlayer", true, false)[0]
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.active = true
	return [sk, ap]

func _series(rig: Array, clip: String) -> Dictionary:
	var sk: Skeleton3D = rig[0]; var ap: AnimationPlayer = rig[1]
	var s: float = sk.global_transform.basis.get_scale().x
	var a := ap.get_animation(clip)
	ap.play(clip)
	var o := {"feet_apart": [], "L_from_hips": [], "R_from_hips": [], "hips_h": []}
	for i in 97:
		ap.seek(a.length * float(i) / 96.0, true, true)
		var h: Vector3 = sk.get_bone_global_pose(sk.find_bone("Hips")).origin * s
		var l: Vector3 = sk.get_bone_global_pose(sk.find_bone("LeftToeBase")).origin * s
		var r: Vector3 = sk.get_bone_global_pose(sk.find_bone("RightToeBase")).origin * s
		(o["feet_apart"] as Array).append((l - r).length())
		(o["L_from_hips"] as Array).append((l - h).length())
		(o["R_from_hips"] as Array).append((r - h).length())
		(o["hips_h"] as Array).append(h.y - minf(l.y, r.y))
	return o

func _dir_deg(ra: Array, ca: String, rb: Array, cb: String, bn: String) -> float:
	var out := []
	for pair in [[ra, ca], [rb, cb]]:
		var sk: Skeleton3D = pair[0][0]; var ap: AnimationPlayer = pair[0][1]
		ap.play(String(pair[1])); ap.seek(0.0, true, true)
		var b := sk.find_bone(bn)
		var kids := sk.get_bone_children(b)
		var tip: Vector3 = sk.get_bone_global_pose(kids[0]).origin if kids.size() > 0 else sk.get_bone_global_pose(b).origin + Vector3.UP
		var d: Vector3 = (sk.global_transform.basis * (tip - sk.get_bone_global_pose(b).origin)).normalized()
		out.append(d)
	return rad_to_deg((out[0] as Vector3).angle_to(out[1]))
