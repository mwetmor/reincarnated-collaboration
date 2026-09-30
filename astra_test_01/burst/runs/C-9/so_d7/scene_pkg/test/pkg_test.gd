extends Node3D
## SCRATCH test of the sorceress SCENE PACKAGE (so_d7/scene_pkg): does her staff behave, per state, when the layers are built
## the way knight.gd builds them from character_sorceress.json -- against the reference staff_layer.gd?
## Two copies of her, both loaded at RUNTIME from so_d7/export (nothing imported): A through a knight.gd-shaped tree built from
## the package JSON (upper_armed = the "up" Blend2, its filter from the LOCOMOTION clips' tracks; arm_layer_armed_R = a filtered Blend2 over locomotion; arm_layer_armed with an EMPTY filter; each strike
## with strike_release's filtered Blend2 inside it, held at 1 for the clips in guard_throughout); B through staff_layer.gd.
## For each state, every 1/30 s: weapon_r's world transform in A against B (angle, position), the staff's tilt from vertical in
## A, and the VFX sockets at each cast's release_s. env PKG = scene_pkg dir, EXP = so_d7/export dir, OUT = json.
const Staff := preload("res://staff_layer.gd")
var pkg: Dictionary
var socks: Dictionary
var A_root: Node3D; var A_ap: AnimationPlayer; var A_tree: AnimationTree; var A_skel: Skeleton3D; var A_body: MeshInstance3D
var B_root: Node3D; var B: Node

func _load(path: String) -> Node3D:
	var doc := GLTFDocument.new(); var st := GLTFState.new()
	assert(doc.append_from_file(path, st) == OK, path)
	return doc.generate_scene(st)

func _char(exp: String, pieces: Array) -> Node3D:
	var who := _load(exp + "/so-body.glb"); add_child(who)
	var skel: Skeleton3D = who.find_children("*", "Skeleton3D", true, false)[0]
	for p in pieces:
		var src := _load(exp + "/" + String(p) + ".glb")
		for m in src.find_children("*", "MeshInstance3D", true, false):
			var mi := m as MeshInstance3D
			if mi.mesh == null or mi.skin == null: continue
			var local := mi.transform; var skin := mi.skin
			mi.owner = null; mi.get_parent().remove_child(mi); skel.add_child(mi)
			mi.transform = local; mi.skin = skin; mi.skeleton = NodePath("..")
		src.queue_free()
	return who

func _filter(b2: AnimationNodeBlend2, act: Animation, bones: Array) -> int:
	var n := 0
	for i in act.get_track_count():
		var pth: NodePath = act.track_get_path(i)
		if String(pth.get_concatenated_subnames()) in bones:
			b2.set_filter_path(pth, true); n += 1
	return n

func _ready() -> void:
	var dir := OS.get_environment("PKG"); var exp := OS.get_environment("EXP")
	pkg = JSON.parse_string(FileAccess.get_file_as_string(dir + "/character_sorceress.json"))
	socks = JSON.parse_string(FileAccess.get_file_as_string(dir + "/sockets_sorceress.json"))
	var gm: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(dir + "/gear_manifest_sorceress.json"))
	var pieces := []
	for p in gm["pieces"]: pieces.append(String(p["piece"]))
	A_root = _char(exp, pieces); B_root = _char(exp, pieces)
	B_root.position = Vector3(10, 0, 0)
	A_ap = A_root.find_children("*", "AnimationPlayer", true, false)[0]
	A_skel = A_root.find_children("*", "Skeleton3D", true, false)[0]
	for mi in A_root.find_children("*", "MeshInstance3D", true, false):
		if (mi as MeshInstance3D).find_blend_shape_by_name("grip_R") >= 0: A_body = mi
	_build_A()
	B = Staff.new(); add_child(B); B.setup(B_root, true)
	await get_tree().process_frame
	var out := {"states": {}, "pieces": pieces, "layers": {}}
	var roles: Dictionary = pkg["clips_armed"]
	var states := {"idle": roles["idle"], "walk": roles["walk"], "run": roles["run"], "fireball": roles["attack"], "meteor": roles["chop"],
		"hit": pkg["roles_knight_lacks"]["hit"], "death": pkg["roles_knight_lacks"]["death"]}
	for st in states:
		var clip := String(states[st])
		var T := A_ap.get_animation(clip).length
		var rows := []
		var worst_ang := 0.0; var worst_pos := 0.0; var tilt_max := 0.0
		var n := int(round(T * 30.0))
		for i in n + 1:
			var t := minf(T * i / n, T)
			_pose_A(st, clip, t)
			B.play(clip, t); B.evaluate()
			var ga := A_skel.global_transform * A_skel.get_bone_global_pose(A_skel.find_bone("weapon_r"))
			var bskel: Skeleton3D = B_root.find_children("*", "Skeleton3D", true, false)[0]
			var gb := bskel.global_transform * bskel.get_bone_global_pose(bskel.find_bone("weapon_r"))
			gb.origin -= B_root.position
			var ya := ga.basis.y.normalized(); var yb := gb.basis.y.normalized()
			var za := ga.basis.z.normalized(); var zb := gb.basis.z.normalized()
			var ang := rad_to_deg(maxf(ya.angle_to(yb), za.angle_to(zb)))
			worst_ang = maxf(worst_ang, ang); worst_pos = maxf(worst_pos, (ga.origin - gb.origin).length())
			tilt_max = maxf(tilt_max, rad_to_deg(ya.angle_to(Vector3.UP)))
		var rec := {"clip": clip, "T": T, "samples": n + 1, "A_vs_staff_layer_deg": snappedf(worst_ang, 0.001),
			"A_vs_staff_layer_m": snappedf(worst_pos, 0.00001), "A_staff_tilt_max_deg": snappedf(tilt_max, 0.01)}
		if st in ["fireball", "meteor"]:
			var rs := float(pkg["casts"][clip]["release_s"])
			_pose_A(st, clip, rs)
			var sk := String(pkg["casts"][clip]["socket"])
			rec["release_s"] = rs
			rec["socket_at_release"] = {sk: _socket(sk), "main_tip": _socket("main_tip")}
		out["states"][st] = rec
		print("[pkg] %-8s %-14s T %.4f: vs staff_layer.gd worst %.3f deg / %.5f m; staff tilt max %.2f deg%s" % [st, clip, T, worst_ang, worst_pos, tilt_max,
			("  | %s at release %s" % [pkg["casts"][clip]["socket"], str(rec["socket_at_release"])]) if rec.has("socket_at_release") else ""])
	var f := FileAccess.open(OS.get_environment("OUT"), FileAccess.WRITE); f.store_string(JSON.stringify(out, " ")); f.close()
	get_tree().quit()

func _socket(name: String) -> Array:
	var sd: Dictionary = socks[name]
	var g := A_skel.global_transform * A_skel.get_bone_global_pose(A_skel.find_bone(String(sd["bone"])))
	var p := g.origin + g.basis.y.normalized() * float(sd.get("along_bone_m", 0.0))
	return [snappedf(p.x, 0.0001), snappedf(p.y, 0.0001), snappedf(p.z, 0.0001)]

func _build_A() -> void:
	for n in A_ap.get_animation_list(): A_ap.get_animation(n).loop_mode = Animation.LOOP_NONE
	A_ap.stop()
	A_tree = AnimationTree.new(); A_ap.get_parent().add_child(A_tree); A_tree.anim_player = A_tree.get_path_to(A_ap)
	var bt := AnimationNodeBlendTree.new()
	var loco := AnimationNodeAnimation.new(); loco.animation = "idle"
	var seek := AnimationNodeTimeSeek.new()
	bt.add_node("loco", loco); bt.add_node("seek", seek); bt.connect_node("seek", 0, "loco")
	# arm_layer_armed: the left-arm slot, action present, filter EMPTY -> a pass-through
	var al: Dictionary = pkg["arm_layer_armed"]
	var carry := AnimationNodeAnimation.new(); carry.animation = String(al["action"])
	var blend := AnimationNodeBlend2.new(); blend.filter_enabled = true
	_filter(blend, A_ap.get_animation(String(al["action"])), al["bones"])
	bt.add_node("carry", carry); bt.add_node("blend", blend)
	bt.connect_node("blend", 0, "seek"); bt.connect_node("blend", 1, "carry")
	# VARIANT up: knight.gd's upper_armed slot holding the spine (its filter from the LOCOMOTION clips' tracks, _apply_upper)
	var upb := AnimationNodeBlend2.new(); upb.filter_enabled = true
	var ua: Dictionary = pkg.get("upper_armed", {})
	var up_clip := AnimationNodeAnimation.new(); up_clip.animation = String(ua.get("walk", "idle"))
	var nup := 0
	if not ua.is_empty():
		for c in ["idle", "walk", "run"]:                     # knight.gd's _apply_upper: paths from the LOCOMOTION clips
			nup += _filter(upb, A_ap.get_animation(c), ua["bones"])
	bt.add_node("up_clip", up_clip); bt.add_node("up", upb)
	bt.disconnect_node("blend", 0)
	bt.connect_node("up", 0, "seek"); bt.connect_node("up", 1, "up_clip"); bt.connect_node("blend", 0, "up")
	print("[pkg] upper_armed: up filter %d paths (%s)" % [nup, str(ua.get("bones", []))])
	# arm_layer_armed_R: blend_r over locomotion
	var ar: Dictionary = pkg["arm_layer_armed_R"]
	var guard_r := AnimationNodeAnimation.new(); guard_r.animation = String(ar["action"])
	var blend_r := AnimationNodeBlend2.new(); blend_r.filter_enabled = true
	var nr := _filter(blend_r, A_ap.get_animation(String(ar["action"])), ar["bones"])
	bt.add_node("guard_r", guard_r); bt.add_node("blend_r", blend_r)
	bt.connect_node("blend_r", 0, "blend"); bt.connect_node("blend_r", 1, "guard_r")
	# a strike: its clip inside rel (filtered to strike_release.bones, the pose held), over the top at full weight
	var sr: Dictionary = pkg["strike_release"]
	var a_s := AnimationNodeAnimation.new(); a_s.animation = "cast_fireball"
	var s_seek := AnimationNodeTimeSeek.new()
	var g_s := AnimationNodeAnimation.new(); g_s.animation = String(sr["pose"])
	var rel := AnimationNodeBlend2.new(); rel.filter_enabled = true
	var ns := _filter(rel, A_ap.get_animation(String(sr["pose"])), sr["bones"])
	var over := AnimationNodeBlend2.new()
	bt.add_node("a_s", a_s); bt.add_node("s_seek", s_seek); bt.add_node("g_s", g_s); bt.add_node("rel", rel); bt.add_node("over", over)
	bt.connect_node("s_seek", 0, "a_s"); bt.connect_node("rel", 0, "s_seek"); bt.connect_node("rel", 1, "g_s")
	bt.connect_node("over", 0, "blend_r"); bt.connect_node("over", 1, "rel")
	bt.connect_node("output", 0, "over")
	A_tree.tree_root = bt; A_tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL; A_tree.active = true
	print("[pkg] A: blend_r %d tracks (%d bones), rel %d tracks (%d bones), left slot %d bones (a pass-through)" % [nr, ar["bones"].size(), ns, sr["bones"].size(), al["bones"].size()])

func _pose_A(st: String, clip: String, t: float) -> void:
	var bt := A_tree.tree_root as AnimationNodeBlendTree
	var strike := st in ["fireball", "meteor"]
	var lacking := st in ["hit", "death"]
	if strike:
		(bt.get_node("a_s") as AnimationNodeAnimation).animation = clip
		A_tree.set("parameters/s_seek/seek_request", t)
		A_tree.set("parameters/rel/blend_amount", 1.0 if clip in pkg["strike_release"]["guard_throughout"] else 0.0)
		A_tree.set("parameters/over/blend_amount", 1.0)
	else:
		(bt.get_node("loco") as AnimationNodeAnimation).animation = clip
		A_tree.set("parameters/seek/seek_request", t)
		A_tree.set("parameters/over/blend_amount", 0.0)
	# the guard slot rides locomotion only: 1 for idle/walk/run; the hit/death clips play raw (knight.gd has no role for them)
	A_tree.set("parameters/blend_r/blend_amount", 0.0 if (strike or lacking) else float(pkg["arm_layer_armed_R"].get("weight", 1.0)))
	A_tree.set("parameters/blend/blend_amount", 1.0)
	# knight.gd's upper chain plays the idle ROLE clip in idle, the upper_armed clips in walk/run
	var ua2: Dictionary = pkg.get("upper_armed", {})
	(bt.get_node("up_clip") as AnimationNodeAnimation).animation = (String(ua2.get(clip, clip)) if clip in ["walk", "run"] else clip)
	A_tree.set("parameters/up/blend_amount", 1.0 if (not ua2.is_empty() and not strike and not lacking) else 0.0)
	A_tree.advance(0.0)
	if A_body:
		A_body.set_blend_shape_value(A_body.find_blend_shape_by_name("grip_R"), 1.0)
