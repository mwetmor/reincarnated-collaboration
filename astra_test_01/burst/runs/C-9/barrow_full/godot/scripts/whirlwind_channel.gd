extends Node
## C-9 R-C9-128: THE WHIRLWIND AS A CHANNEL. Binds the port (whirlwind_fx.gd: reincarnated-godot wwcr_whirlwind.gd,
## exactly as made) to a Barrow character and times it the way the source harness did (wwcr_stage.gd: begin at
## T_BEGIN 0.30, release at T_RELEASE 2.60 -- a 2.30 s channel, then the measured 0.80 s spin-down). A tap gives that
## channel; holding the key (or the button) keeps it up until release. He moves while channelling (Matt; the GD packet:
## canUseWhileMoving, turn rate x0.35 during the channel).
##
## Two ways to spin, one effect:
##   "clip"  the character carries a rigid spin clip (the dark knight: final_k_eor's eor_spin_start + eor_spin_loop;
##           the barbarian's great maul set will carry one by the same recipe): the knight plays it (eor_begin /
##           eor_end on slot_knight.gd), and the effect reads the weapon head off weapon_r.
##   "rig"   no spin clip: the effect turns the rig itself, as the source did (rotate_y at OMEGA_DEG), and poses the
##           arms out (whirlwind_pose.gd).
## drax.
const CHANNEL_S := 2.30
const TURN_RATE_MUL := 0.35                  # the GD packet: the turn rate while channelling
## the source harness's default element ("wind", Matt's "original") and the dark knight's Eye of Reckoning RED (the GD
## packet: pfx_eyeofreckoning_spinredfx_01). set_element keeps only the HUE and builds its own ramp (+18.9 / +19.4 /
## +50.5 deg), so the red is given at 345 deg: the apex and body land at 4 deg (red), the tail at 35 deg (ember).
const TINTS := {"original": Color(0.72, 0.95, 0.82), "red": Color(1.0, 0.15, 0.3625)}   # red = hsv(345 deg, 0.85, 1.0)

var fx = null                                # the first blade's instance: every layer
var fxs: Array = []                          # every blade's instance (R-C9-133: two for the dual-wield barbarian)
var tips: Array = ["weapon_r"]
var tint := "original"
var mode := "rig"
var action := "attack"
var _t := -1.0
var _k: Node = null
var _proxy: Node3D
var _tau0 := -1.0
## C-9 R-C9-143 (lane EOR2): WHICH EFFECT the dark knight's Eye of Reckoning draws. ?eorfx= (page) / --eorfx (desktop):
##   ""      (the default) eor_kc2_fx.gd -- the effect Matt watched: reincarnated-godot kc2_player_channel.gd's VFX
##           layers (smoke haze + dark bed, the cut pattern, three spark emitters, the ember garnish), exactly as made
##   "wwcr"  whirlwind_fx.gd -- R-C9-128's port of wwcr_whirlwind.gd, kept for comparison
## Only for a character carrying the EoR spin clip (_eor_ok) with one blade; the barbarian's whirlwind binds as before.
var kind := "wwcr"


func setup(scene: Node3D, k: Node, tint_name: String, spin_mode: String, hold_action: String,
		tip_bones: Array = ["weapon_r"]) -> void:
	_k = k
	tips = tip_bones
	mode = spin_mode
	action = hold_action
	var sk: Skeleton3D = k.get("_skel")
	var rig: Node3D = k.get("_rig")
	# his standing height off the rest skeleton: the top of the head (head_end, else Head) over his feet
	var top := sk.find_bone("head_end")
	if top < 0:
		top = sk.find_bone("Head")
	var h: float = (sk.global_transform * sk.get_bone_global_rest(top).origin).y - rig.global_transform.origin.y
	tint = tint_name if TINTS.has(tint_name) else "original"
	if mode == "clip" and bool(k.get("_eor_ok")) and tips.size() == 1 and Slots.arg("eorfx") != "wwcr":
		kind = "kc2"
		var kf = load("res://scripts/eor_kc2_fx.gd").new()
		kf.name = "EorKc2"
		scene.add_child(kf)
		kf.bind_to(rig, sk, k, _weapon_head_local(k, sk, String(tips[0])), tint, scene.get("snow"))
		fxs.append(kf)
	for ti in (tips.size() if kind == "wwcr" else 0):
		var proxy := Node3D.new()
		proxy.name = "WhirlwindBlade%d" % ti
		scene.add_child(proxy)
		var f = load("res://scripts/whirlwind_fx.gd").new()
		f.name = "Whirlwind%d" % ti
		f.process_physics_priority = 100     # after knight.gd re-seats his rig
		f.grip_bone = String(tips[ti])
		f.ribbon_only = ti > 0               # the second blade: its ribbon and its sheds; the rest once
		if mode == "clip":
			f.spin_from_clip = true
			f.blade_head_local = _weapon_head_local(k, sk, String(tips[ti]))
		scene.add_child(f)
		f.bind_to(rig, sk, proxy, h, k)
		f.set_element(TINTS[tint])
		fxs.append(f)
	fx = fxs[0]
	name = "WhirlwindChannel"
	_scene = scene
	_warm = WARM_FRAMES
	process_priority = 10                    # after the effect's own _process (it clears the ribbons when idle)


## C-9 PORT 12: every layer drawn once under the veil before the first channel (the page's first cast froze 1688 ms
## cold without it); warm_veil.gd waits on `warmed`
const WARM_FRAMES := 8
var warmed := false
var _warm := 0
var _scene: Node3D


func _process(_dt: float) -> void:
	if _warm <= 0:
		return
	_warm -= 1
	# AT HIM, at the sweep height -- not in front of the camera (the crater's way): measured on the page, a warm
	# draw 5 m before the lens left the ribbon's first real draw still stalling (154 ms warm, 1281 ms cold); the
	# lit core takes its pipeline from the lights where it is drawn, so it is warmed where it will be drawn
	var rig: Node3D = _k.get("_rig")
	var at := rig.global_transform.origin + Vector3(0.0, 1.2, 0.0)
	for f in fxs:
		f.warm(_warm > 0, at)
	if _warm == 0:
		warmed = true
		_apply_off(PaintStack.web_query("wwoff") if PaintStack.web_query("wwoff") != "" else Slots.arg("wwoff"))


func _apply_off(spec: String) -> void:
	"""?wwoff=ribbon,pool,shed,scuff,scour,residue,spark -- a DIAGNOSTIC: those layers never drawn (cull layer 0), to
	find which one a cost belongs to. Not a look; not on the select page."""
	if spec == "" or kind != "wwcr":
		return
	var off := spec.split(",")
	for f in fxs:
		var nodes := []
		if off.has("ribbon"):
			nodes.append_array([f.get("_ribbon"), f.get("_ribbon_body")])
		if off.has("pool") and f.get("_pool") != null:
			nodes.append(f.get("_pool"))
		for pair in [["shed", "_shed"], ["scuff", "_scuffs"], ["scour", "_scour"], ["residue", "_residue"], ["spark", "_sparks"]]:
			if off.has(pair[0]):
				for e in (f.get(pair[1]) as Array):
					nodes.append(e["mi"])
		for n in nodes:
			if n != null:
				(n as VisualInstance3D).layers = 0
	print("[ww] diagnostic: layers off ", spec)


func _weapon_head_local(k: Node, sk: Skeleton3D, bone: String) -> Vector3:
	"""The weapon head in the grip bone's own space: the farthest vertex from the grip of the weapon mesh held in
	THAT hand (a vertex counts for the grip bone it is nearer, weapon_r or weapon_l), at bind (the rest pose the skin
	was bound in). Read once; the clip keys the weapon bone through every spin key, so the head follows."""
	var wb := sk.find_bone(bone)
	var other := sk.find_bone("weapon_l" if bone == "weapon_r" else "weapon_r")
	var orest := sk.get_bone_global_rest(other).origin if other >= 0 else Vector3(INF, INF, INF)
	if wb < 0:
		return Vector3.ZERO
	var rest := sk.get_bone_global_rest(wb)
	var pieces: Dictionary = (k.get("gear") as Dictionary).get("_pieces", {})
	var best := Vector3.ZERO
	var best_d := -1.0
	for nm in pieces:
		if not (String(nm).contains("mace") or String(nm).contains("maul") or String(nm).contains("hammer")
				or String(nm).contains("axe") or String(nm).contains("sword")):
			continue
		if not (pieces[nm] is Array):
			continue                                  # gear.gd's _markers_* entries
		for mi in (pieces[nm] as Array):
			var m := mi as MeshInstance3D
			if m == null or m.mesh == null:
				continue
			for si in m.mesh.get_surface_count():
				var arr: PackedVector3Array = m.mesh.surface_get_arrays(si)[Mesh.ARRAY_VERTEX]
				for v in arr:
					var p: Vector3 = m.transform * v           # skeleton space at bind
					var d := p.distance_to(rest.origin)
					if p.distance_to(orest) < d:
						continue                              # the other hand's weapon
					if d > best_d:
						best_d = d
						best = p
	if best_d <= 0.0:
		return Vector3.ZERO
	return rest.affine_inverse() * best


func press() -> bool:
	if fx == null or fx.state_name() != "IDLE":
		return false
	for f in fxs:
		f.begin()
	_t = CHANNEL_S
	if mode == "clip" and _k.has_method("eor_begin"):
		_k.eor_begin()
	_turn(true)
	return true


func busy() -> bool:
	return fx != null and fx.state_name() != "IDLE"


func channelling() -> bool:
	return _t >= 0.0


func _turn(slow: bool) -> void:
	var tr: Dictionary = (_k.get("cfg") as Dictionary).get("transitions", {})
	if slow:
		_tau0 = float(tr.get("turn_tau_s", 0.12))
		tr["turn_tau_s"] = _tau0 / TURN_RATE_MUL
	elif _tau0 > 0.0:
		tr["turn_tau_s"] = _tau0
	(_k.get("cfg") as Dictionary)["transitions"] = tr


func _physics_process(dt: float) -> void:
	if _t < 0.0:
		return
	_t -= dt
	if _t <= 0.0:
		if Input.is_action_pressed(action):
			_t = 0.0001                      # held: the channel stays up
		else:
			for f in fxs:
				f.end()
			_t = -1.0
			if mode == "clip" and _k.has_method("eor_end"):
				_k.eor_end()
			_turn(false)


func report() -> Dictionary:
	if fx == null:
		return {}
	if kind == "kc2":
		return {"fx": "kc2", "tint": tint, "mode": mode, "tips": tips, "channel_s": CHANNEL_S,
			"weapon_head_local": str(fx.get("_head_local")), "kc2": fx.report}
	return {"fx": "wwcr", "tint": tint, "mode": mode, "h_char": float(fx.get("_s")) * 1.85, "scale": fx.get("_s"),
		"r_engage": fx.get("R_ENGAGE"), "r_trail_source": fx.get("R_TRAIL"),
		"tips": tips, "weapon_head_local": fxs.map(func(f): return str(f.get("blade_head_local"))), "channel_s": CHANNEL_S}
