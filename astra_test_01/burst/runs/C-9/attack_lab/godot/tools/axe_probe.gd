extends SceneTree
# HOW IS THE AXE HELD? Matt: "the axe is still held tilted towards the character instead of at
# a battle stance". Measured, per clip, in the CHARACTER'S frame (skeleton space: forward +Z,
# up +Y, his right -X -- the manifest's facing/his_right, and the stride probe's forward):
#   tilt      the haft's angle from vertical (grip -> head; 0 = head straight up)
#   lean      the haft's forward and outboard components (outboard = to his right)
#   head      the axe head's offset from the fist: outboard (+) / inboard (-), forward, up
#   edge      the blade edge's heading vs his facing: 0 = forward, +90 = outboard, -90 = inboard
# The axe is rigidly skinned to RightHand, so its geometry is fixed in the HAND's frame
# (bind pose x vertex), found once by PCA; each frame the hand's pose carries it.
const SAMPLE_FPS := 24.0
var k: CharacterBody3D
var skel: Skeleton3D
var ap: AnimationPlayer
var hb := -1
var H := Vector3.ZERO      # haft axis, hand-local, grip -> head
var E := Vector3.ZERO      # edge direction, hand-local, perpendicular to H
var head_l := Vector3.ZERO # head point, hand-local
var grip_l := Vector3.ZERO # where the haft passes the fist, hand-local
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)

func _initialize() -> void:
	create_timer(300.0).timeout.connect(func(): push_error("WATCHDOG"); quit(4))
	k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	skel = k._skel
	ap = k._anim
	hb = skel.find_bone("RightHand")
	_axe_geometry()
	(k._tree as AnimationTree).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var out := {}
	for clip in ["idle_armed", "walk_armed", "run_armed", "block", "attack", "attack_chop", "shield_bash"]:
		out[clip] = _clip(clip)
	# CANDIDATE READY POSES: every strike frame that already meets the acceptance -- haft 30-60
	# deg from vertical leaning forward AND out, head outboard of the fist, edge within 45 deg of
	# his facing. Early frames first: a PRE-SWING ready pose, not a frame mid-swing.
	for clip in ["attack", "attack_chop", "shield_bash"]:
		var ok := []
		for r in (out[clip]["rows"] as Array):
			if float(r["tilt"]) >= 30.0 and float(r["tilt"]) <= 60.0 and float(r["fwd"]) > 0.0 and float(r["out"]) > 0.0 \
					and float(r["head_out"]) > 0.0 and absf(float(r["edge"])) <= 45.0:
				ok.append("%.2fs(t%.0f e%+.0f)" % [float(r["t"]), float(r["tilt"]), float(r["edge"])])
		print("[axe] %-12s frames meeting the acceptance: %d -> %s" % [clip, ok.size(), " ".join(ok.slice(0, 14))])
	for clip in ["attack", "attack_chop", "shield_bash"]:
		var line := ""
		var rows: Array = out[clip]["rows"]
		var step: int = 2 if clip != "attack_chop" else 6
		for i in range(0, mini(rows.size(), 60 if clip != "attack_chop" else 130), step):
			var r: Dictionary = rows[i]
			line += " %.2f:t%.0f/f%+.1f/o%+.1f/e%+.0f" % [float(r["t"]), float(r["tilt"]), float(r["fwd"]), float(r["out"]), float(r["edge"])]
		print("[axe] %-12s timeline t:tilt/fwd/out/edge%s" % [clip, line])
	var f := FileAccess.open(OS.get_environment("LAB_OUT") if OS.has_environment("LAB_OUT") else "/tmp/axe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(out, " ")); f.close()
	quit(0)

func _axe_geometry() -> void:
	var mi: MeshInstance3D = (k.gear["_pieces"]["axe"] as Array)[0]
	var sk: Skin = mi.skin
	var bind := Transform3D()
	for i in sk.get_bind_count():
		if String(sk.get_bind_name(i)) == "RightHand":
			bind = sk.get_bind_pose(i)
	var verts: PackedVector3Array = mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]
	var pts := []
	var c := Vector3.ZERO
	for v in verts:
		var p: Vector3 = bind * v
		pts.append(p); c += p
	c /= float(pts.size())
	# PCA by power iteration on the covariance: the haft is the long axis
	var cov := Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO)
	var xx := 0.0; var xy := 0.0; var xz := 0.0; var yy := 0.0; var yz := 0.0; var zz := 0.0
	for p in pts:
		var d: Vector3 = p - c
		xx += d.x * d.x; xy += d.x * d.y; xz += d.x * d.z; yy += d.y * d.y; yz += d.y * d.z; zz += d.z * d.z
	var ax := Vector3(1, 1, 1).normalized()
	for it in 60:
		ax = Vector3(xx * ax.x + xy * ax.y + xz * ax.z, xy * ax.x + yy * ax.y + yz * ax.z, xz * ax.x + yz * ax.y + zz * ax.z).normalized()
	# the edge marker, in hand-local (its BoneAttachment3D follows the hand's global pose)
	var mk: Node3D = (k.gear["_pieces"]["_markers_axe"] as Dictionary)["axe_edge"]
	var edge_l: Vector3 = mk.transform.origin
	# orient the axis grip -> head: the head is the end the edge marker is on
	if (edge_l - c).dot(ax) < 0.0:
		ax = -ax
	H = ax
	var lo := 1e9; var hi := -1e9
	for p in pts:
		var s: float = (p - c).dot(H)
		lo = minf(lo, s); hi = maxf(hi, s)
	var perp: Vector3 = (edge_l - c) - (edge_l - c).dot(H) * H
	E = perp.normalized()
	head_l = c + H * (edge_l - c).dot(H)          # the head: level with the edge along the haft
	grip_l = c + H * (-c).dot(H)                  # the haft point nearest the hand bone's origin
	var s_: float = skel.global_transform.basis.get_scale().x
	print("[axe] haft %.3f m long; hand origin %.3f m from the haft axis; grip at %.3f m of %.3f..%.3f along it (head end %.3f)"
		% [(hi - lo) * s_, ((-c) - (-c).dot(H) * H).length() * s_, (-c).dot(H) * s_, lo * s_, hi * s_, (edge_l - c).dot(H) * s_])
	# how the haft sits IN THE FIST: angle to the hand bone's own axis (its local +Y runs along
	# the bone, toward the fingers); a fist grips a haft about 90 deg to it
	# WHICH local axis runs along the hand? Measure it rather than assume +Y: the direction from
	# the forearm bone to the hand bone, expressed in the hand's own frame, at rest.
	var fa := skel.find_bone("RightForeArm")
	var gh: Transform3D = skel.get_bone_global_rest(hb)
	var gf: Transform3D = skel.get_bone_global_rest(fa)
	var along_l: Vector3 = (gh.basis.inverse() * (gh.origin - gf.origin)).normalized()
	print("[axe] the hand's own axis (forearm -> hand, in hand-local) = %s; hand +Y is %.1f deg from it"
		% [str(along_l.snappedf(0.001)), rad_to_deg(along_l.angle_to(Vector3(0, 1, 0)))])
	print("[axe] in the fist: haft is %.1f deg from the forearm line through the fist (90 = square across the fist)"
		% rad_to_deg(H.angle_to(along_l)))

func _clip(clip: String) -> Dictionary:
	var a := ap.get_animation(clip)
	var n: int = maxi(int(round(a.length * SAMPLE_FPS)), 1)
	ap.play(clip)
	var rows := []
	for i in n + 1:
		ap.seek(a.length * float(i) / float(n), true, true)
		rows.append(_pose(a.length * float(i) / float(n)))
	var med := func(key: String) -> float:
		var v := rows.map(func(r): return float(r[key])); v.sort(); return float(v[v.size() / 2])
	var rng := func(key: String) -> String:
		var v := rows.map(func(r): return float(r[key])); v.sort(); return "%.0f..%.0f" % [float(v[0]), float(v[-1])]
	var o := {"tilt": med.call("tilt"), "fwd": med.call("fwd"), "out": med.call("out"),
			  "head_out": med.call("head_out"), "head_fwd": med.call("head_fwd"), "head_up": med.call("head_up"),
			  "edge": med.call("edge"), "tilt_range": rng.call("tilt"), "edge_range": rng.call("edge"), "rows": rows}
	print("[axe] %-12s tilt %5.1f deg (%s) | haft leans fwd %+.2f out %+.2f | head vs fist: out %+.3f fwd %+.3f up %+.3f m | edge %+6.1f deg (%s)"
		% [clip, float(o["tilt"]), String(o["tilt_range"]), float(o["fwd"]), float(o["out"]), float(o["head_out"]),
		   float(o["head_fwd"]), float(o["head_up"]), float(o["edge"]), String(o["edge_range"])])
	return o

func _pose(t: float) -> Dictionary:
	var g: Transform3D = skel.get_bone_global_pose(hb)
	var s_: float = skel.global_transform.basis.get_scale().x
	var h: Vector3 = (g.basis * H).normalized()
	var e: Vector3 = (g.basis * E).normalized()
	var head: Vector3 = g * head_l
	var fist: Vector3 = g * grip_l
	var d: Vector3 = (head - fist) * s_
	var eh := Vector2(e.dot(R), e.dot(F))
	return {"t": t, "tilt": rad_to_deg(h.angle_to(U)), "fwd": h.dot(F), "out": h.dot(R),
			"head_out": d.dot(R), "head_fwd": d.dot(F), "head_up": d.dot(U),
			"edge": rad_to_deg(atan2(eh.x, eh.y)), "fist": fist * s_, "head": head * s_}
