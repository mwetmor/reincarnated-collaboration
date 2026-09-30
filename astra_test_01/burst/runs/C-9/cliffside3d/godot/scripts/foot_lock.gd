extends SkeletonModifier3D
## FOOT LOCKING THROUGH TRANSITIONS (coordinator's design call, 2026-09-29).
##
## The armed idle is a footwork clip and the three strikes start in three different stances,
## so a crossfade into or out of any of them drags a planted foot up to 1.8 m across the
## ground in 0.1 s (attack_lab). No clip data can fix that: the idle's own feet are anywhere
## within 0.83 m of each other depending on phase. So the feet are held instead.
##
##   At a transition start, every foot that is PLANTED is locked where it stands (world
##   position AND orientation). While the body blends at its normal speed, leg IK keeps it
##   there. After the transition's own fade, the lock is RELEASED over RELEASE_S: the target
##   travels from the lock to wherever the animation now wants the foot -- and if that is
##   more than STEP_MIN_M away it travels on a parabola, so a long move reads as a STEP
##   (lift, travel, plant) and not a glide. When the target reaches the animated foot the IK
##   hands back with nothing to pop.
##
## A foot in the air when the transition starts (mid-stride from a run) is not locked; it is
## already moving and keeps swinging. A lock the body pulls out of reach releases at once.
##
## Three modifiers, in this order under the Skeleton3D:
##   FootLock (this)   reads the ANIMATED pose, runs the state machine, places targets/poles
##   TwoBoneIK3D x2    the engine's own solver, one per leg so each has its own influence
##   FootLock.Orient   holds the locked foot's world ORIENTATION, so the toe stays too
##
## TwoBoneIK3D DOES NOTHING WITHOUT A POLE NODE (Godot 4.6.3, attack_lab ik_probe4: 0.000 m of
## movement with no pole or with a pole direction, exactly onto the target with a pole node).
## The pole is placed off the animated knee, so the knee bends the way the clip bends it.

const HOLD_DEFAULT_S := 0.10
const RELEASE_S := 0.20
const STEP_MIN_M := 0.04        # a move shorter than this blends; longer ones lift
const LIFT_PER_M := 0.35        # step height per metre of travel ...
const LIFT_MAX_M := 0.25        # ... capped
const TRAVEL_START := 0.15      # a STEP lifts first: horizontal travel waits for this much of it
const TRAVEL_SPAN := 0.70       # ... and is done by TRAVEL_START + TRAVEL_SPAN; the rest plants
const PLANTED_H_M := 0.07       # toe joint within this of the ground -> "planted" (reported)
const FAST_SWING_MS := 2.5      # a foot moving faster than this is mid-stride: left to swing
const REACH := 0.985            # fraction of full leg length before a lock gives way

enum { FREE, LOCKED, RELEASING }

var knight: Node3D
var enabled := true
var ik := {}            # side -> TwoBoneIK3D
var tgt := {}           # side -> Node3D (IK target, top level)
var pole := {}          # side -> Node3D (IK pole, top level)
var st := {}            # side -> per-foot state Dictionary
var bones := {}         # side -> {up, leg, foot, toe}
var leg_len := {}       # side -> full leg length, rig units
var _pending: Dictionary = {}
var _window := 0.0              # time left in the current transition: free feet that LAND in it lock
var reach_releases := 0         # locks the body pulled out of reach (diagnostic)
var landings := 0               # free feet planted on landing (diagnostic)
var last_us := 0        # cost of the last planner pass, microseconds
var events := []        # (kind, per-foot decisions) for the lab to read


func setup(k: Node3D, sk: Skeleton3D) -> void:
	knight = k
	for side in ["L", "R"]:
		var p := "Left" if side == "L" else "Right"
		var b := {"up": sk.find_bone(p + "UpLeg"), "leg": sk.find_bone(p + "Leg"),
				  "foot": sk.find_bone(p + "Foot"), "toe": sk.find_bone(p + "ToeBase")}
		bones[side] = b
		leg_len[side] = sk.get_bone_rest(int(b["leg"])).origin.length() + sk.get_bone_rest(int(b["foot"])).origin.length()
		var t := Node3D.new(); t.name = "FootLockTarget" + side; t.top_level = true
		var q := Node3D.new(); q.name = "FootLockPole" + side; q.top_level = true
		k.add_child(t); k.add_child(q)
		tgt[side] = t; pole[side] = q
		var s := TwoBoneIK3D.new()
		s.name = "FootIK" + side
		s.setting_count = 1
		s.set_root_bone_name(0, p + "UpLeg")
		s.set_middle_bone_name(0, p + "Leg")
		s.set_end_bone_name(0, p + "Foot")
		sk.add_child(s)
		s.set_target_node(0, s.get_path_to(t))
		s.set_pole_node(0, s.get_path_to(q))
		s.influence = 0.0
		s.active = false
		ik[side] = s
		st[side] = {"mode": FREE, "t": 0.0, "hold": 0.0, "u": 0.0, "lock": Vector3.ZERO, "lock_rot": Quaternion(),
					"from": Vector3.ZERO, "from_rot": Quaternion(), "shown": Vector3.INF, "shown_toe": Vector3.INF,
					"shown_rot": Quaternion(), "prev_toe": Vector3.INF, "want_rot": Quaternion(), "lift": 0.0}
	var o := Orient.new()
	o.name = "FootLockOrient"
	o.lock = self
	sk.add_child(o)


## Called by knight.gd when a strike, a block or their fade-outs START. `hold_s` is that
## transition's own fade: the feet stay put for as long as the body is blending.
func transition(kind: String, hold_s: float) -> void:
	_pending = {"kind": kind, "hold": hold_s}


## Locomotion has taken over: hand every foot back quickly, as a short step, not a pop.
func release_all(release_s := 0.12) -> void:
	for side in st.keys():
		var f: Dictionary = st[side]
		if int(f["mode"]) != FREE:
			_start_release(f, release_s)


func _start_release(f: Dictionary, release_s := RELEASE_S) -> void:
	f["from"] = f["shown"] if f["shown"] != Vector3.INF else f["lock"]
	f["from_rot"] = f["shown_rot"]
	f["u"] = 0.0
	f["rel"] = release_s
	f["mode"] = RELEASING


func _process_modification_with_delta(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	var sk := get_skeleton()
	if sk == null or knight == null:
		return
	# NOTHING TO DO most frames: no transition pending, none running, both feet free. The IK
	# modifiers are already inactive; skip the pole placement too (5 us -> ~1 us a frame).
	if _pending.is_empty() and _window <= 0.0 and int(st["L"]["mode"]) == FREE and int(st["R"]["mode"]) == FREE:
		last_us = Time.get_ticks_usec() - t0
		return
	var xf := sk.global_transform
	var sc: float = xf.basis.get_scale().x
	var ground_y: float = knight.global_position.y
	var fwd: Vector3 = (xf.basis * Vector3(0, 0, 1)).normalized()
	for side in ["L", "R"]:
		var b: Dictionary = bones[side]
		var f: Dictionary = st[side]
		var ank: Vector3 = xf * sk.get_bone_global_pose(int(b["foot"])).origin
		var arot: Quaternion = (xf.basis.orthonormalized() * sk.get_bone_global_pose(int(b["foot"])).basis.orthonormalized()).get_rotation_quaternion()
		var hip: Vector3 = xf * sk.get_bone_global_pose(int(b["up"])).origin
		var knee: Vector3 = xf * sk.get_bone_global_pose(int(b["leg"])).origin
		var d: Vector3 = knee - (hip + ank) * 0.5
		if d.length() < 0.02:
			d = fwd
		(pole[side] as Node3D).global_position = knee + d.normalized() * 0.6
		# a new transition: lock what is planted, where it is SHOWN (continuity through
		# back-to-back transitions -- a foot mid-release is locked where it is drawn)
		if enabled and not _pending.is_empty() and side == "L":
			_window = float(_pending["hold"]) + RELEASE_S
		if enabled and not _pending.is_empty():
			var shown: Vector3 = f["shown"] if f["shown"] != Vector3.INF else ank
			var toe: Vector3 = f["shown_toe"]
			var prev: Vector3 = f["prev_toe"]
			var h: float = (toe.y - ground_y) if toe != Vector3.INF else 1.0
			var v: float = ((toe - prev).length() / maxf(dt, 1e-4)) if (toe != Vector3.INF and prev != Vector3.INF) else 0.0
			# LOCK EVERY FOOT THAT IS NOT MID-STRIDE, planted or not. The first version locked only
			# planted feet and never engaged from idle: the Axe Stance is footwork, its feet are down
			# in 10 of 147 frames, and at a transition they were 0.08-0.77 m up at 1.0-1.7 m/s. A
			# footwork foot held for the fade pauses for two or three frames and then steps; a run
			# stride (5-7.6 m/s, measured) is left to finish its swing -- frozen, it would hitch.
			var planted: bool = h <= PLANTED_H_M
			if v <= FAST_SWING_MS:
				f["mode"] = LOCKED
				f["t"] = 0.0
				f["hold"] = float(_pending["hold"])
				f["lock"] = shown
				f["lock_rot"] = f["shown_rot"] if f["shown"] != Vector3.INF else arot
			events.append([String(_pending["kind"]), side, "planted" if planted else "raised", snappedf(h, 0.001), snappedf(v, 0.01),
						   "LOCK" if v <= FAST_SWING_MS else "swing"])
			if events.size() > 32:
				events.pop_front()
		var mode: int = int(f["mode"])
		if enabled and mode == FREE and _window > 0.0 and f["shown_toe"] != Vector3.INF and f["prev_toe"] != Vector3.INF:
			var ht: float = (f["shown_toe"] as Vector3).y - ground_y
			var falling: bool = (f["shown_toe"] as Vector3).y <= (f["prev_toe"] as Vector3).y
			if ht <= PLANTED_H_M and falling:
				# PLANT ON LANDING: a foot left to finish its stride locks where it touches down,
				# instead of landing and then following the blend across the ground
				f["mode"] = LOCKED
				f["t"] = 0.0
				f["hold"] = maxf(0.05, _window - RELEASE_S)
				f["lock"] = f["shown"]
				f["lock_rot"] = f["shown_rot"]
				mode = LOCKED
				landings += 1
		var target := ank
		if mode == LOCKED:
			f["t"] = float(f["t"]) + dt
			target = f["lock"]
			f["want_rot"] = f["lock_rot"]
			var reach: float = float(leg_len[side]) * sc * REACH
			if (hip - target).length() > reach:
				reach_releases += 1
				_start_release(f)
				mode = RELEASING
			elif float(f["t"]) >= float(f["hold"]):
				_start_release(f)
				mode = RELEASING
		if mode == RELEASING:
			var rel: float = float(f.get("rel", RELEASE_S))
			f["u"] = minf(1.0, float(f["u"]) + dt / maxf(rel, 1e-4))
			var u: float = float(f["u"])
			var from: Vector3 = f["from"]
			var dist: float = Vector2(ank.x - from.x, ank.z - from.z).length()
			var s: float
			var up_m := 0.0
			if dist < STEP_MIN_M:
				s = u * u * (3.0 - 2.0 * u)            # a short move just blends
			else:
				# A STEP: the foot lifts FIRST (a sine over the whole window), travels in the middle
				# (smoothstep over TRAVEL_SPAN, starting at TRAVEL_START), and plants at the end.
				# The first version rose no faster than it moved, so a long step skimmed the floor.
				var w: float = clampf((u - TRAVEL_START) / TRAVEL_SPAN, 0.0, 1.0)
				s = w * w * (3.0 - 2.0 * w)
				up_m = minf(LIFT_MAX_M, LIFT_PER_M * dist) * sin(PI * u)
			target = Vector3(lerpf(from.x, ank.x, s), lerpf(from.y, ank.y, u * u * (3.0 - 2.0 * u)), lerpf(from.z, ank.z, s)) + Vector3.UP * up_m
			f["want_rot"] = (f["from_rot"] as Quaternion).slerp(arot, s)
			if u >= 1.0:
				f["mode"] = FREE
				mode = FREE
		var s_ik: TwoBoneIK3D = ik[side]
		if mode == FREE:
			s_ik.active = false
			s_ik.influence = 0.0
		else:
			(tgt[side] as Node3D).global_position = target
			s_ik.active = true
			s_ik.influence = 1.0
	_pending = {}
	_window = maxf(0.0, _window - dt)
	last_us = Time.get_ticks_usec() - t0


## Runs AFTER both IK modifiers: holds a locked foot's world orientation, and records where
## every foot is finally SHOWN (post-IK) -- which is what the next transition locks, and
## what the lab measures.
class Orient:
	extends SkeletonModifier3D
	var lock          # the FootLock -- untyped: it has no class_name to type it with
	var last_us := 0

	func _process_modification() -> void:
		var t0 := Time.get_ticks_usec()
		var sk := get_skeleton()
		if sk == null or lock == null:
			return
		var xf := sk.global_transform
		var xb := xf.basis.orthonormalized()
		for side in ["L", "R"]:
			var b: Dictionary = lock.bones[side]
			var f: Dictionary = lock.st[side]
			if int(f["mode"]) != 0:
				var fb: int = int(b["foot"])
				var par: int = sk.get_bone_parent(fb)
				var pg: Quaternion = sk.get_bone_global_pose(par).basis.orthonormalized().get_rotation_quaternion()
				var want_skel: Quaternion = xb.get_rotation_quaternion().inverse() * (f["want_rot"] as Quaternion)
				sk.set_bone_pose_rotation(fb, (pg.inverse() * want_skel).normalized())
			f["prev_toe"] = f["shown_toe"]
			f["shown"] = xf * sk.get_bone_global_pose(int(b["foot"])).origin
			f["shown_toe"] = xf * sk.get_bone_global_pose(int(b["toe"])).origin
			f["shown_rot"] = (xb * sk.get_bone_global_pose(int(b["foot"])).basis.orthonormalized()).get_rotation_quaternion()
		last_us = Time.get_ticks_usec() - t0
