extends SkeletonModifier3D
# CONTROL for ik_probe4: rotate the left thigh 45 deg. If THIS is invisible when read, the
# reading is broken, not the IK.
func _process_modification() -> void:
	var sk := get_skeleton()
	var b := sk.find_bone("LeftUpLeg")
	sk.set_bone_pose_rotation(b, sk.get_bone_pose_rotation(b) * Quaternion(Vector3.RIGHT, deg_to_rad(45.0)))
