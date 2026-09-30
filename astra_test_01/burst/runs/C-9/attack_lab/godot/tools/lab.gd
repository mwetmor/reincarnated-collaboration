extends SceneTree
# ATTACK LAB. One action, one starting state, one rung of the elimination ladder:
#   --action=slash|chop|bash|block   --from=idle|run   --rung=R0..R6   [--film --out=DIR]
# Quarter speed: the tree is advanced by hand, 1/96 s per frame, and film is encoded at
# 24 fps. MANUAL advance, because in PHYSICS callback mode a slow render lets several
# physics steps run per captured frame and the film would silently skip.
const DT := 1.0 / 96.0
const RIGHT := Vector3(0.681998491287231, 0.0, -0.731353580951691)
const UP := Vector3(-0.583728015422821, 0.60246217250824, -0.54433536529541)
const FWD := Vector3(-0.440612882375717, -0.798147439956665, -0.410878270864487)
const SCALE := 1.10
const LEAD_IDLE := 48
const LEAD_RUN := 96
const TAIL := 48
const BLOCK_HOLD := 1.5

var A := {}
var k: CharacterBody3D
var skel: Skeleton3D
var tree: AnimationTree
var ref_skel: Skeleton3D
var ref_anim: AnimationPlayer
var ref_root: Node3D
var frames := []
var cams := []
var svs := []
var mf := 0

func _initialize() -> void:
	# WATCHDOG. A SceneTree script whose coroutine dies on an error never reaches quit(), and
	# this one runs under the SHARED heavy lock: on 2026-09-29 a null load killed stance.gd
	# mid-await and it held the lock for ten minutes with the integration build queued behind
	# it. A timer on the main loop fires whether or not the coroutine is alive.
	create_timer(float(OS.get_environment("LAB_WATCHDOG_S")) if OS.has_environment("LAB_WATCHDOG_S") else 240.0).timeout.connect(func(): push_error("LAB WATCHDOG: quitting a hung script"); quit(4))
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--"):
			var kv: PackedStringArray = a.substr(2).split("=", true, 1)
			A[kv[0]] = kv[1] if kv.size() > 1 else "1"
	var action: String = String(A.get("action", "slash"))
	var from: String = String(A.get("from", "idle"))
	var rung: String = String(A.get("rung", "R6"))
	var film: bool = A.has("film")
	_build_world()
	k = load("res://scripts/knight.gd").new()
	k.setup(RIGHT, UP, FWD, SCALE)
	root.add_child(k)
	for i in 6: await process_frame
	k.set_physics_process(false)
	skel = k._skel
	tree = k._tree
	tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	k.set_gear_stack(int(A.get("stack", str(k.gear_stack_count() - 1))))
	k.global_position = Vector3(0, 0.02, 0)
	k.velocity = Vector3.ZERO
	k.facing = "E"
	_build_ref()
	var clip: String = _clip_for(action)
	ref_anim.play(clip)
	ref_anim.seek(0.0, true, true)
	var rest_h: float = ref_skel.get_bone_rest(ref_skel.find_bone("RightHand")).origin.length()
	ref_anim.seek(float(k._clip_len.get(clip, 1.0)) * 0.5, true, true)
	var mid: Vector3 = ref_skel.get_bone_global_pose(ref_skel.find_bone("RightHand")).origin
	ref_anim.seek(0.0, true, true)
	var start: Vector3 = ref_skel.get_bone_global_pose(ref_skel.find_bone("RightHand")).origin
	print("[lab] reference check: RightHand moves %.2f rig units between t=0 and mid-clip (0 = NOT POSED)"
		% (mid - start).length())
	_apply_rung(rung, action)
	if film:
		_build_cams()
	print("[lab] %s from %s, rung %s, clip '%s' (%.3f s), armed=%s, scale %.2f"
		% [action, from, rung, clip, float(k._clip_len.get(clip, 0.0)), str(k.armed()), SCALE])
	# ---- lead-in -----------------------------------------------------------------
	var lead: int = 0 if action == "idle" else (LEAD_RUN if from == "run" else LEAD_IDLE)
	for i in lead:
		await _frame(Vector2(1, 0) if from == "run" else Vector2.ZERO, from == "run", "lead", clip, film)
	# ---- the action --------------------------------------------------------------
	var t0 := frames.size()
	if action == "idle":
		for i in int(float(k._clip_len.get("idle_armed", 6.0)) / DT):
			await _frame(Vector2.ZERO, false, "act", clip, film)
	elif rung == "R0" or rung == "R1":
		await _raw_action(clip, film)
	else:
		if action == "block":
			k.set_block(true)
			for i in int(BLOCK_HOLD / DT):
				await _frame(Vector2.ZERO, false, "block", clip, film)
			k.set_block(false)
		else:
			var fired: bool = k.try_strike(action)
			if not fired:
				print("[lab] *** strike '%s' did not fire ***" % action)
		var guard := 0
		while (k.attacking() or guard < 8) and guard < int(12.0 / DT):
			await _frame(Vector2.ZERO, false, "act", clip, film)
			guard += 1
	for i in TAIL:
		await _frame(Vector2.ZERO, false, "tail", clip, film)
	_summarise(action, from, rung, clip, t0)
	quit(0)

# ---------------------------------------------------------------------------------
func _clip_for(action: String) -> String:
	var role: String = {"slash": "attack", "chop": "chop", "bash": "bash", "block": "block", "idle": "idle"}[action]
	return String(k._roles.get(role, ""))

func _apply_rung(rung: String, action: String) -> void:
	# R0 raw clip / R1 +grip morphs / R2 +arm layers / R3 +wrist lock (clip data) /
	# R4 +load-time de-root / R5 +axe_edge seek() (none in the game path) / R6 +OneShot fades
	var bt := tree.tree_root as AnimationNodeBlendTree
	var n: int = int(rung.substr(1))
	if n < 1:
		for m in ["grip_R", "grip_L", "helmet_on"]:
			k._set_morph(m, false)
	if n < 2:
		tree.set("parameters/blend/blend_amount", 0.0)
		k._layer_on = false
	if n < 6:
		for os_name in ["os_slash", "os_chop", "os_bash"]:
			if bt.has_node(os_name):
				var o := bt.get_node(os_name) as AnimationNodeOneShot
				o.fadein_time = 0.0
				o.fadeout_time = 0.0

func _raw_action(clip: String, film: bool) -> void:
	# THE CLIP ALONE: the tree switched off, the AnimationPlayer playing the clip straight
	# through, the body where it stands. Whatever this shows, the clip does on its own.
	tree.active = false
	var ap: AnimationPlayer = k._anim
	ap.active = true
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.play(clip)
	ap.seek(0.0, true, true)
	var n: int = int(round(float(k._clip_len.get(clip, 1.0)) / DT))
	for i in n + 1:
		await _frame(Vector2.ZERO, false, "act", clip, film, ap)
	tree.active = true
	ap.active = false

func _frame(dir: Vector2, run: bool, phase: String, clip: String, film: bool, ap: AnimationPlayer = null) -> void:
	if ap != null:
		ap.advance(DT if frames.size() > 0 else 0.0)
		k._drive(DT)
	else:
		k.drive_dir(dir, run, DT)
		tree.advance(DT)
	# a foot-locked knight's modifiers must run on THIS step, at THIS dt -- left in IDLE mode
	# they would run once per rendered frame on wall-clock time, and the film would not match
	# the numbers
	if k._foot_lock != null:
		if skel.modifier_callback_mode_process != Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL:
			skel.modifier_callback_mode_process = Skeleton3D.MODIFIER_CALLBACK_MODE_PROCESS_MANUAL
		skel.advance(DT)
		skel.notification(Skeleton3D.NOTIFICATION_UPDATE_SKELETON)
	var pos: float = _clip_pos(clip, ap)
	# seek() on an AnimationPlayer with no current animation does NOTHING -- the first pass
	# of this compared every frame against the REST pose and called it "the raw clip".
	if ref_anim.current_animation != clip:
		ref_anim.play(clip)
	ref_anim.seek(clamp(pos, 0.0, float(k._clip_len.get(clip, 1.0))), true, true)
	frames.append(_sample(phase, pos))
	if film:
		await RenderingServer.frame_post_draw
		_shoot()
	else:
		await process_frame

func _clip_pos(clip: String, ap: AnimationPlayer) -> float:
	if ap != null:
		return ap.current_animation_position
	var key := ""
	for kv in [["attack", "a_slash"], ["attack_chop", "a_chop"], ["shield_bash", "a_bash"], ["block", "a_block"]]:
		if clip == String(kv[0]):
			key = String(kv[1])
	if key == "":
		return 0.0
	return float(tree.get("parameters/%s/current_position" % key))

# ---------------------------------------------------------------------------------
const BONES := ["Hips", "Spine", "Spine01", "Spine02", "Head", "LeftArm", "LeftForeArm", "LeftHand",
				"RightArm", "RightForeArm", "RightHand", "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase",
				"RightUpLeg", "RightLeg", "RightFoot", "RightToeBase", "LeftShoulder", "RightShoulder"]

func _sample(phase: String, pos: float) -> Dictionary:
	var s := {"phase": phase, "clip_pos": pos, "body": k.global_position}
	var g_scale: float = skel.global_transform.basis.get_scale().x
	var r_scale: float = ref_skel.global_transform.basis.get_scale().x
	var dev := 0.0
	var dev_bone := ""
	var rots := {}
	for bn in BONES:
		var b: int = skel.find_bone(bn)
		var rb: int = ref_skel.find_bone(bn)
		if b < 0 or rb < 0:
			continue
		var gp: Transform3D = skel.get_bone_global_pose(b)
		var rp: Transform3D = ref_skel.get_bone_global_pose(rb)
		var d: float = (gp.origin - rp.origin).length() * g_scale
		if d > dev:
			dev = d
			dev_bone = bn
		rots[bn] = [gp.basis.get_rotation_quaternion(), rp.basis.get_rotation_quaternion()]
	s["dev_m"] = dev
	s["dev_bone"] = dev_bone
	s["rots"] = rots
	for bn in ["Hips", "LeftToeBase", "RightToeBase", "RightHand", "LeftHand"]:
		s[bn] = skel.global_transform * skel.get_bone_global_pose(skel.find_bone(bn)).origin
		s["ref_" + bn] = ref_skel.get_bone_global_pose(ref_skel.find_bone(bn)).origin * g_scale
	s["axe"] = _piece_point("axe", "RightHand")
	return s

func _piece_point(piece: String, bone: String) -> Vector3:
	# the piece's own vertex 0, posed through its one-bone skin -- exact for a rigid bind
	var pcs: Dictionary = k.gear.get("_pieces", {})
	var arr = pcs.get(piece, null)
	if not (arr is Array) or (arr as Array).is_empty():
		return Vector3.INF
	var mi: MeshInstance3D = (arr as Array)[0]
	var sk: Skin = mi.skin
	if sk == null:
		return Vector3.INF
	var v: Vector3 = (mi.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX] as PackedVector3Array)[0]
	for i in sk.get_bind_count():
		var bn2: String = String(sk.get_bind_name(i))
		var b2: int = skel.find_bone(bn2)
		if b2 >= 0 and bn2 == bone:
			return skel.global_transform * (skel.get_bone_global_pose(b2) * sk.get_bind_pose(i)) * v
	return Vector3.INF

# ---------------------------------------------------------------------------------
func _summarise(action: String, from: String, rung: String, clip: String, t0: int) -> void:
	var out := {"action": action, "from": from, "rung": rung, "clip": clip, "frames": frames.size()}
	# 1. POSE POP: excess angular speed the game shows over the raw clip at the same clip
	#    time, per bone, in degrees per 1/24 s. A clip's own fast swing is in BOTH and
	#    cancels; something the runtime added is left over.
	var pop := 0.0
	var pop_at := -1
	var pop_bone := ""
	var pop_phase := ""
	for i in range(t0 + 1, frames.size()):
		var a: Dictionary = frames[i - 1]["rots"]
		var b: Dictionary = frames[i]["rots"]
		for bn in b.keys():
			if not a.has(bn):
				continue
			var ga: float = rad_to_deg((a[bn][0] as Quaternion).angle_to(b[bn][0] as Quaternion))
			var ra: float = rad_to_deg((a[bn][1] as Quaternion).angle_to(b[bn][1] as Quaternion))
			var ex: float = (ga - ra) * (1.0 / 24.0) / DT
			if ex > pop:
				pop = ex
				pop_at = i
				pop_bone = String(bn)
				pop_phase = String(frames[i]["phase"])
	out["pose_pop_deg_per_24th"] = snappedf(pop, 0.1)
	out["pose_pop_where"] = "%s, frame %d (%s, %.2f s into the action)" % [pop_bone, pop_at, pop_phase, float(pop_at - t0) * DT]
	# 2. ROOT: the hips' horizontal offset from the body, and how fast it changes. A rooted
	#    one-shot should move the hips only as the clip does.
	var root_step := 0.0
	var root_at := -1
	var drift_min := 1e9
	var drift_max := -1e9
	for i in range(t0 + 1, frames.size()):
		var h0: Vector3 = frames[i - 1]["Hips"] - frames[i - 1]["body"]
		var h1: Vector3 = frames[i]["Hips"] - frames[i]["body"]
		var r0: Vector3 = frames[i - 1]["ref_Hips"]
		var r1: Vector3 = frames[i]["ref_Hips"]
		h0.y = 0.0; h1.y = 0.0; r0.y = 0.0; r1.y = 0.0
		# excess over the raw clip's own hip motion, in mm per 1/24 s
		var ex2: float = absf((h1 - h0).length() - (r1 - r0).length()) * 1000.0 * (1.0 / 24.0) / DT
		if ex2 > root_step:
			root_step = ex2
			root_at = i
	out["root_excess_mm_per_24th"] = snappedf(root_step, 0.1)
	out["root_excess_where"] = "frame %d (%s, %.2f s)" % [root_at, String(frames[maxi(root_at, 0)]["phase"]), float(root_at - t0) * DT]
	# 3. DEVIATION from the raw clip, rig space, at FULL one-shot weight only -- where the
	#    game is supposed to be showing the clip and nothing else
	var dev_full := 0.0
	var dev_full_bone := ""
	var dev_all := 0.0
	for i in range(t0, frames.size()):
		var f: Dictionary = frames[i]
		dev_all = maxf(dev_all, float(f["dev_m"]))
	var n_act := 0
	for i in range(t0, frames.size()):
		if String(frames[i]["phase"]) != "act":
			continue
		n_act += 1
	var fin: float = 0.10 if rung == "R6" else 0.0
	var fout: float = 0.25 if rung == "R6" else 0.0
	var clip_len: float = float(k._clip_len.get(clip, 1.0))
	for i in range(t0, frames.size()):
		var f2: Dictionary = frames[i]
		var cp: float = float(f2["clip_pos"])
		if String(f2["phase"]) == "act" and cp > fin + 0.02 and cp < clip_len - fout - 0.02:
			if float(f2["dev_m"]) > dev_full:
				dev_full = float(f2["dev_m"])
				dev_full_bone = String(f2["dev_bone"])
	out["deviation_at_full_weight_m"] = snappedf(dev_full, 0.0001)
	out["deviation_at_full_weight_bone"] = dev_full_bone
	out["deviation_anywhere_m"] = snappedf(dev_all, 0.0001)
	# 4. FEET: world travel of a foot the RAW clip has planted, mm per 1/24 s
	var skate := 0.0
	var skate_at := -1
	for foot in ["LeftToeBase", "RightToeBase"]:
		var lo := 1e9
		for i in range(t0, frames.size()):
			lo = minf(lo, (frames[i]["ref_" + foot] as Vector3).y)
		for i in range(t0 + 1, frames.size()):
			var ra0: Vector3 = frames[i - 1]["ref_" + foot]
			var ra1: Vector3 = frames[i]["ref_" + foot]
			var planted: bool = ra1.y <= lo + 0.03 and ra0.y <= lo + 0.03 and (ra1 - ra0).length() * (1.0 / 24.0) / DT < 0.004
			if not planted:
				continue
			var w: float = ((frames[i][foot] as Vector3) - (frames[i - 1][foot] as Vector3)).length() * 1000.0 * (1.0 / 24.0) / DT
			if w > skate:
				skate = w
				skate_at = i
	out["planted_foot_skate_mm_per_24th"] = snappedf(skate, 0.1)
	out["skate_where"] = "frame %d (%s, %.2f s)" % [skate_at, String(frames[maxi(skate_at, 0)]["phase"]), float(skate_at - t0) * DT]
	# 5. WEAPON: hand to axe distance, which a rigid bind holds constant
	var dmin := 1e9
	var dmax := 0.0
	for i in range(t0, frames.size()):
		var ax: Vector3 = frames[i]["axe"]
		if ax == Vector3.INF:
			continue
		var dd: float = (ax - (frames[i]["RightHand"] as Vector3)).length()
		dmin = minf(dmin, dd)
		dmax = maxf(dmax, dd)
	out["axe_hand_distance_m"] = [snappedf(dmin, 0.0001), snappedf(dmax, 0.0001)]
	# FADE WINDOWS: how far each foot travels in the world while the one-shot fades in and
	# while it fades out. A crossfade between two stances whose feet are in different places
	# cannot avoid moving the feet by the difference; this is that distance, and its speed.
	var clip_len2: float = float(k._clip_len.get(clip, 1.0))
	var fin2: float = 0.10 if rung == "R6" else 0.0
	var fout2: float = 0.25 if rung == "R6" else 0.0
	for win in [["fade_in", 0.0, fin2 + 0.02], ["fade_out", clip_len2 - fout2 - 0.02, clip_len2 + 0.30]]:
		var tot := 0.0
		var peak := 0.0
		for foot in ["LeftToeBase", "RightToeBase"]:
			var d0 := 0.0
			for i in range(t0 + 1, frames.size()):
				var tt2: float = float(i - t0) * DT
				if tt2 < float(win[1]) or tt2 > float(win[2]):
					continue
				var st: float = ((frames[i][foot] as Vector3) - (frames[i - 1][foot] as Vector3)).length()
				d0 += st
				peak = maxf(peak, st / DT)
			tot = maxf(tot, d0)
		out[String(win[0]) + "_foot_travel_m"] = snappedf(tot, 0.001)
		out[String(win[0]) + "_foot_peak_m_s"] = snappedf(peak, 0.01)
	# WIND-UP CREEP: median world travel of the lower foot while the clip is well inside its
	# full-weight window. For a rooted strike this should be ~0; a linear de-root turns a
	# lunge into a constant slide and shows up here.
	var creep := []
	for i in range(t0 + 1, frames.size()):
		var f5: Dictionary = frames[i]
		var cp5: float = float(f5["clip_pos"])
		if String(f5["phase"]) != "act" or cp5 < 0.3 or cp5 > minf(2.8, clip_len2 - fout2 - 0.1):
			continue
		var lft: Vector3 = f5["LeftToeBase"]
		var rgt: Vector3 = f5["RightToeBase"]
		var foot2: String = "LeftToeBase" if lft.y <= rgt.y else "RightToeBase"
		creep.append(((f5[foot2] as Vector3) - (frames[i - 1][foot2] as Vector3)).length() * 1000.0 * (1.0 / 24.0) / DT)
	creep.sort()
	out["windup_lower_foot_mm_per_24th_median"] = snappedf(float(creep[creep.size() / 2]) if creep.size() > 0 else -1.0, 0.1)
	var trace := []
	for i in range(maxi(t0 - 2, 1), mini(t0 + 16, frames.size())):
		var f4: Dictionary = frames[i]
		var p4: Dictionary = frames[i - 1]
		var hr: Vector3 = (f4["Hips"] as Vector3) - (f4["body"] as Vector3)
		var hp: Vector3 = (p4["Hips"] as Vector3) - (p4["body"] as Vector3)
		trace.append("%3d %-4s clip %.3f | hips rel (%.3f, %.3f, %.3f) step %5.1f mm | RToe step %5.1f mm (raw %4.1f) | dev %.3f m %s"
			% [i - t0, String(f4["phase"]), float(f4["clip_pos"]), hr.x, hr.y, hr.z, (hr - hp).length() * 1000.0,
			   ((f4["RightToeBase"] as Vector3) - (p4["RightToeBase"] as Vector3)).length() * 1000.0,
			   ((f4["ref_RightToeBase"] as Vector3) - (p4["ref_RightToeBase"] as Vector3)).length() * 1000.0,
			   float(f4["dev_m"]), String(f4["dev_bone"])])
	out["trace_fade_in"] = trace
	var dir: String = String(A.get("out", ProjectSettings.globalize_path("user://")))
	DirAccess.make_dir_recursive_absolute(dir)
	var f3 := FileAccess.open("%s/%s_%s_%s.json" % [dir, action, from, rung], FileAccess.WRITE)
	f3.store_string(JSON.stringify(out, " "))
	f3.close()
	print("[lab] RESULT ", JSON.stringify(out))

# ---------------------------------------------------------------------------------
func _build_world() -> void:
	var ground := StaticBody3D.new()
	ground.collision_layer = CliffWorld.TERRAIN_BIT
	ground.collision_mask = 0
	var cs := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(400, 1, 400)
	cs.shape = box
	cs.position = Vector3(0, -0.5, 0)
	ground.add_child(cs)
	var mi := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(400, 400)
	mi.mesh = pm
	var sm := ShaderMaterial.new()
	var sh := Shader.new()
	# a WORLD-SPACE checker, 0.5 m squares: a foot that skates is a foot that crosses lines
	sh.code = "shader_type spatial;\nrender_mode unshaded;\nvarying vec3 wp;\nvoid vertex(){ wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz; }\nvoid fragment(){ vec2 c = floor(wp.xz / 0.5); float m = mod(c.x + c.y, 2.0); ALBEDO = mix(vec3(0.42,0.40,0.36), vec3(0.58,0.56,0.51), m); }"
	sm.shader = sh
	mi.material_override = sm
	ground.add_child(mi)
	root.add_child(ground)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-50, 30, 0)
	root.add_child(sun)
	var we := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.16, 0.17, 0.19)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.8, 0.8, 0.8)
	we.environment = env
	root.add_child(we)

func _build_ref() -> void:
	# A PRISTINE copy of the clips. _deroot_all mutates the Animation resource in place,
	# and a resource loaded from the same file is SHARED -- so the reference is loaded with
	# the cache bypassed, or it would silently be the de-rooted clip too.
	var ps := ResourceLoader.load(String(k.cfg.get("model", "")), "", ResourceLoader.CACHE_MODE_IGNORE_DEEP) as PackedScene
	ref_root = ps.instantiate()
	ref_root.visible = false
	root.add_child(ref_root)
	for n in ref_root.find_children("*", "", true, false):
		if n is Skeleton3D and ref_skel == null:
			ref_skel = n
		elif n is AnimationPlayer and ref_anim == null:
			ref_anim = n
	ref_anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL

func _build_cams() -> void:
	for i in 2:
		var sv := SubViewport.new()
		sv.size = Vector2i(960, 1080)
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(sv)
		var c := Camera3D.new()
		c.projection = Camera3D.PROJECTION_ORTHOGONAL
		c.size = 3.6
		c.near = 0.1
		c.far = 400.0
		sv.add_child(c)
		c.current = true
		# the label is burned in HERE: this machine's ffmpeg has no drawtext filter
		var lab := Label.new()
		lab.text = (String(A.get("label", "")) + "\nplay camera") if i == 0 else "side camera"
		lab.position = Vector2(18, 14)
		lab.add_theme_font_size_override("font_size", 26)
		lab.add_theme_color_override("font_color", Color(1, 1, 1))
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0, 0, 0, 0.6)
		sb.content_margin_left = 10; sb.content_margin_right = 10
		sb.content_margin_top = 6; sb.content_margin_bottom = 6
		lab.add_theme_stylebox_override("normal", sb)
		sv.add_child(lab)
		svs.append(sv)
		cams.append(c)

func _shoot() -> void:
	var tgt: Vector3 = k.global_position + Vector3(0, 1.0, 0)
	(cams[0] as Camera3D).look_at_from_position(tgt - FWD * 60.0, tgt, UP)
	var face: Vector3 = k.canvas_velocity_to_world(Vector2(1, 0))
	face.y = 0.0
	var side: Vector3 = face.normalized().cross(Vector3.UP)
	(cams[1] as Camera3D).look_at_from_position(tgt + side * 60.0, tgt, Vector3.UP)
	var img := Image.create(1920, 1080, false, Image.FORMAT_RGB8)
	for i in 2:
		var im: Image = (svs[i] as SubViewport).get_texture().get_image()
		im.convert(Image.FORMAT_RGB8)
		img.blit_rect(im, Rect2i(0, 0, 960, 1080), Vector2i(960 * i, 0))
	var d: String = String(A.get("out", "/tmp")) + "/frames"
	if mf == 0:
		DirAccess.make_dir_recursive_absolute(d)
	img.save_jpg("%s/f_%05d.jpg" % [d, mf], 0.9)
	mf += 1
