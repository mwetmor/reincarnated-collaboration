extends SceneTree
# OPTION B, measured: a STATIC right-arm guard pose (the shield's recipe) with weapon_r only
# finishing the angle. Every frame of every armed clip is a candidate arm pose; for each, the
# smallest turn of the haft out of the fist's channel that puts the axe at a guard (the grid of
# guard_search.gd, with the predicate checked at that frame), and where the fist is.
const F := Vector3(0, 0, 1)
const U := Vector3(0, 1, 0)
const R := Vector3(-1, 0, 0)
const SOURCES := ["walk_armed", "idle_armed", "run_armed", "run_armed_L", "run_armed_R", "strafe_L_armed", "strafe_R_armed", "block", "shield_bash", "attack", "attack_chop", "walk", "idle", "run"]
func _initialize() -> void:
	create_timer(600.0).timeout.connect(func(): print("[static] WATCHDOG"); quit(4))
	var k = load("res://scripts/knight.gd").new()
	k.setup(Vector3.RIGHT, Vector3.UP, Vector3.FORWARD, 1.0)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	k.set_gear_stack(k.gear_stack_count() - 1)
	for i in 4: await process_frame
	var skel: Skeleton3D = k._skel
	var ap: AnimationPlayer = k._anim
	(k._tree as AnimationTree).active = false
	for c in skel.get_children():
		if c is SkeletonModifier3D: (c as SkeletonModifier3D).active = false
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	var s_: float = skel.global_transform.basis.get_scale().x
	var hb := skel.find_bone("RightHand"); var wb := skel.find_bone("weapon_r"); var chb := skel.find_bone("Spine")
	var Wr: Transform3D = skel.get_bone_rest(wb)
	var guards := []
	for tilt in [35.0, 40.0, 45.0, 50.0, 55.0]:
		for az in [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]:
			var h: Vector3 = (F * cos(deg_to_rad(az)) + R * sin(deg_to_rad(az))) * sin(deg_to_rad(tilt)) + U * cos(deg_to_rad(tilt))
			guards.append([h, tilt, az])
	var rows := []
	for clip in SOURCES:
		var a := ap.get_animation(clip)
		var n: int = int(round(a.length * 12.0))
		ap.play(clip)
		for i in n + 1:
			var t: float = a.length * float(i) / float(maxi(n, 1))
			ap.seek(t, true, true)
			var hg: Transform3D = skel.get_bone_global_pose(hb)
			var ch_w: Vector3 = (hg.basis.orthonormalized() * (Wr.basis * Vector3.UP)).normalized()   # the channel, in the world
			var best := 1e9; var bt := 0.0; var baz := 0.0
			for g in guards:
				var d: float = rad_to_deg((g[0] as Vector3).angle_to(ch_w))
				if d < best: best = d; bt = float(g[1]); baz = float(g[2])
			var cg: Transform3D = skel.get_bone_global_pose(chb)
			var fist: Vector3 = ((hg * Wr).origin - cg.origin) * s_
			rows.append({"clip": clip, "t": t, "defl": best, "tilt": bt, "az": baz, "ffwd": fist.dot(F), "fout": fist.dot(R), "fup": fist.dot(U)})
	var front := rows.filter(func(r): return float(r["ffwd"]) >= 0.10 and float(r["fup"]) <= 0.10 and float(r["fup"]) >= -0.55)
	front.sort_custom(func(a, b): return float(a["defl"]) < float(b["defl"]))
	print("[static] %d candidate arm poses (12 fps over %d clips); %d with the fist in front of him between the belly and the chest; the best 12:" % [rows.size(), SOURCES.size(), front.size()])
	for r in front.slice(0, 12):
		print("[static]   %-15s t=%.3f  haft out of the channel %5.1f deg for a guard at tilt %2.0f az %2.0f | fist fwd %+.2f out %+.2f up %+.2f m of the chest"
			% [String(r["clip"]), float(r["t"]), float(r["defl"]), float(r["tilt"]), float(r["az"]), float(r["ffwd"]), float(r["fout"]), float(r["fup"])])
	var per := {}
	for r in rows:
		var c := String(r["clip"])
		if not per.has(c) or float(r["defl"]) < float(per[c]["defl"]): per[c] = r
	var line := ""
	for c in SOURCES: line += " %s %.0f" % [c, float(per[c]["defl"])]
	print("[static] lowest turn needed, per clip, any frame:%s" % line)
	quit(0)
