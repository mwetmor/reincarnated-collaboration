extends SkeletonModifier3D
class_name BarrowWhirlwindPose
# C-9 R-C9-128 PORT (drax): reincarnated-godot scripts/wwcr_pose.gd, its bone names mapped to the Barrow's rigs by
# tools/port_whirlwind.py (UpperArm -> Arm, LowerArm -> ForeArm, Spine -> the spine bone whose parent is Hips).
const BONE_MAP := {"LeftUpperArm": "LeftArm", "LeftLowerArm": "LeftForeArm", "RightUpperArm": "RightArm",
	"RightLowerArm": "RightForeArm"}
# ============================================================================
# wwcr_pose.gd — drax, S2 `whirlwind` CLEAN-ROOM mint (WW-AB).
#
# The BODY half of the archetype. Spec § 3.1.12: "the CHARACTER rotates and the
# payload is the character's own weapons." So the pose is not decoration around
# the move — the pose IS the move, and the VFX is generated from where it puts
# the blade.
#
# Two poses, blended by two independent weights owned by wwcr_whirlwind.gd:
#
#   sweep_w  0..1   the two-hand horizontal sweep. Arms come forward and lock,
#                   so the blade describes a constant-radius circle about the
#                   caster's own vertical axis (the anchor's "rigidly
#                   player-centred ... constant" clause).
#
#   windup_w 0..1   the ANTICIPATION pose. AUTHORED-NOT-REFERENCED — windup
#                   coverage for this archetype is ZERO across the whole corpus
#                   (see mint note § 4.1). Torso counter-rotates AGAINST the
#                   spin and the root drops. It is a wind-BACK, deliberately not
#                   an opacity ramp or a charge glow: those are what the negative
#                   anchor does, and they would change the causality class from
#                   physical-cause to magical-cause.
#
# Derivation, not euler-guessing: the humanoid rest frame was probed
# (scripts/wwcr_rest_probe.gd) and every arm bone's limb axis is local +Y. So a
# target pose is expressed as a WORLD DIRECTION for the limb, and the local
# rotation is solved as the quaternion carrying the bone's current global +Y
# onto that direction. Re-derives itself if the rig changes.
# ============================================================================

## Blend weight for the two-hand horizontal sweep pose.
var sweep_w: float = 0.0
## Blend weight for the AUTHORED anticipation pose.
var windup_w: float = 0.0
## Character forward in rig-local space. Probed: this rig's held blade points +Z.
var forward_local: Vector3 = Vector3(0, 0, 1)

# --- the sweep pose, expressed as limb world-directions in RIG-LOCAL space ---
# Upper arms come up to just below horizontal and slightly outboard; lower arms
# continue almost straight so the grip sits at (shoulder_off + arm_len) from the
# body axis. That is what makes R_GRIP_sweep = 0.845 m and R_TRAIL = 2.36 m
# actually true at runtime rather than only on paper (mint note § 3).
const UPPER_DROP := -0.22      # downward component of the upper-arm direction
const UPPER_SPREAD := 0.30     # outboard (±X) component
const LOWER_DROP := -0.10      # lower arm continues nearly straight
const LOWER_SPREAD := 0.14

# --- the AUTHORED anticipation pose ---
const WINDUP_TORSO_DEG := -28.0   # counter-rotation AGAINST the spin direction
const WINDUP_LEAN_DEG := 9.0      # slight forward crouch

var _bones := {}
var _ready_done := false
var _logged := false


func _process_modification() -> void:
	var skel := get_skeleton()
	if skel == null:
		return
	if not _ready_done:
		for n in ["Hips", "Spine", "Chest", "UpperChest",
				"LeftUpperArm", "LeftLowerArm", "RightUpperArm", "RightLowerArm"]:
			_bones[n] = skel.find_bone(String(BONE_MAP.get(n, n)))
		# the first spine bone above the hips (this rig: Spine02)
		var hi := skel.find_bone("Hips")
		for i in skel.get_bone_count():
			if skel.get_bone_parent(i) == hi and String(skel.get_bone_name(i)).contains("Spine"):
				_bones["Spine"] = i
		_ready_done = true

	if sweep_w <= 0.001 and windup_w <= 0.001:
		return

	if not _logged:
		_logged = true
		print("[wwcr-pose] _process_modification IS RUNNING sweep_w=%.3f windup_w=%.3f" % [sweep_w, windup_w])
	var f := forward_local.normalized()
	var right := f.cross(Vector3.UP).normalized()

	# ---- arms: solve each limb toward its target world direction ----
	_aim(skel, "RightUpperArm", (f + Vector3.UP * UPPER_DROP - right * UPPER_SPREAD), sweep_w)
	_aim(skel, "RightLowerArm", (f + Vector3.UP * LOWER_DROP - right * LOWER_SPREAD), sweep_w)
	_aim(skel, "LeftUpperArm", (f + Vector3.UP * UPPER_DROP + right * UPPER_SPREAD), sweep_w)
	_aim(skel, "LeftLowerArm", (f + Vector3.UP * LOWER_DROP + right * LOWER_SPREAD), sweep_w)

	# ---- AUTHORED anticipation: torso winds BACK against the spin, body sinks ----
	if windup_w > 0.001:
		var si: int = _bones.get("Spine", -1)
		if si >= 0:
			var t := skel.get_bone_pose(si)
			var q := Quaternion(Vector3.UP, deg_to_rad(WINDUP_TORSO_DEG) * windup_w) \
				* Quaternion(right, deg_to_rad(WINDUP_LEAN_DEG) * windup_w)
			t.basis = Basis(q) * t.basis
			skel.set_bone_pose(si, t)


# Solve the LOCAL rotation that carries this bone's current global +Y onto
# `target_dir_local`, then blend it in by `w`.
func _aim(skel: Skeleton3D, bone: String, target_dir_local: Vector3, w: float) -> void:
	if w <= 0.001:
		return
	var i: int = _bones.get(bone, -1)
	if i < 0:
		return
	var gp := skel.get_bone_global_pose(i)
	var cur := (gp.basis * Vector3.UP).normalized()
	var tgt := target_dir_local.normalized()
	if cur.dot(tgt) > 0.9999:
		return
	# delta expressed in skeleton space, then pulled into the bone's PARENT space
	# so it composes with whatever the animation already did.
	var delta := Quaternion(cur, tgt)
	delta = Quaternion.IDENTITY.slerp(delta, clampf(w, 0.0, 1.0))
	var parent := skel.get_bone_parent(i)
	var parent_basis := (skel.get_bone_global_pose(parent).basis if parent >= 0 else Basis())
	var local_delta := parent_basis.inverse() * Basis(delta) * parent_basis
	var pose := skel.get_bone_pose(i)
	pose.basis = local_delta * pose.basis
	skel.set_bone_pose(i, pose)
	# the child limb is aimed next and reads its own global pose, which is stale
	# until the chain below this bone is refreshed.
	skel.force_update_bone_child_transform(i)
