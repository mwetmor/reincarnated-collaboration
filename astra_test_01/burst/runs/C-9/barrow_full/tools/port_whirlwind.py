#!/usr/bin/env python3
"""C-9 R-C9-128: PORT the 3D clean-room whirlwind (reincarnated-godot scripts/wwcr_whirlwind.gd + wwcr_pose.gd) into the
painted Barrow, EXACTLY as made -- the same ribbon, sparks, scuffs, sheds, scour, residue, timings and radii -- with only
the binding changed. Every edit below is an exact-text replacement that must match once (assert), so the port can be
re-derived from the source at any time and the diff to the source is this file. drax.

  python3 tools/port_whirlwind.py        writes godot/scripts/whirlwind_fx.gd and godot/scripts/whirlwind_pose.gd

What changes, and why (nothing else does):
  1. SCALE. The source was made on a 1.85 m king (H_STAND). Every LENGTH is multiplied by s = H_char / 1.85 (the
     character's own standing height, measured off its rest skeleton at bind). Times, rates, alphas, colours, counts
     are untouched. Length constants become vars of the same name set in bind_to; literal lengths in the code get * _s.
  2. GROUND. The source floor was y = 0; the Barrow's is not flat. Every absolute height becomes anchor.y + height.
  3. THE RIG SPIN. The source rotated its own rig (`_rig.rotate_y`). knight.gd re-seats his rig every physics frame, so
     the spin is applied as an ABSOLUTE yaw (= _spin) in _process and again after knight.gd in _physics_process.
     _spin starts at his current yaw, so the source's bearing convention (sin spin, cos spin) holds unchanged.
  4. THE BLADE. The source bound a Greatsword node. Here the "blade" is a proxy node seated each frame on the rig's own
     weapon_r bone (the grip), its long axis along forearm -> hand; the source's _reseat_blade then drives it radial
     and level exactly as before. The blade length 1.5150 m is the source's, scaled.
  5. THE POSE. wwcr_pose.gd's bone names (UpperArm/LowerArm/Spine) mapped to this rig's (Arm/ForeArm/the spine bone
     whose parent is Hips).
  6. NO LIGHT NODES. The Barrow cannot take a dynamic light: Compatibility sRGB-encodes each light's pass before it
     adds them, and the first build's fire OmniLight3D "summed hot on the web" (paint_stack.gd, LANE B). Measured again
     here: the source's ArcLight (2.2 energy, 2.6 m) turned the WHOLE painted frame white for the channel. So the
     ArcLight node is kept (the source drives it, unchanged) but never shown; its position, colour and energy are
     copied each frame to an additive, unlit, soft ground POOL of the light's own range -- the white pool the source's
     light laid on its floor (harness_logs/wwcr_2026-08-25-lap2). The 24 spark lights stay dark (sparks need contact
     targets, and the Barrow has none).
  8. THE ARC IS 150 DEGREES AT ANY FRAME RATE. The source keeps TRAIL_SAMPLES = 10 frames of blade history and says
     why: "10 samples at 60 fps and 900 deg/s spans ~150 deg of arc -- an ARC, never a closed ring". Counted in
     frames, a 30 fps phone frame doubles it to 300 deg, nearly the closed ring the source forbids. So the window is
     the same 10 samples' TIME, 10/60 s: as many samples as fit in it (at least 2).
  9. THE SPIN FROM THE CLIP (the dark knight: wl_e1 final_k_eor's eor_spin_start / eor_spin_loop, recipe (a) -- one
     frame of idle turned rigidly CCW). When `spin_from_clip` is set the clip owns the body: the effect does not turn
     the rig, does not pose the arms (the source's WWCRPose) and does not re-seat the weapon; the blade is the real
     weapon -- the grip at weapon_r, the tip at the weapon head read off weapon_r (`blade_head_local`, the mesh's
     farthest point from the grip at bind) -- and _spin is that head's bearing about him, unwrapped, so every
     bearing the source derives from _spin (wobble, cross-section, sheds, contacts, scuffs, scour) follows the
     weapon he actually swings.
 10. TWO BLADES (R-C9-133: the arena barbarian is dual wield, a blade in each hand). A second instance reads the other
     hand (`grip_bone` weapon_l) with `ribbon_only` set: its own ribbon and the sheds off its own apex, and NONE of
     the once-per-character layers (the onset ring, contacts and sparks, scuffs, scour, the arc pool, the rig spin) --
     those stay single, on the first instance, so the neutral discrete layers are the same count as one blade's.
 11. THE SCOUR, RE-MEASURED FOR THIS VENUE -- the source's own instruction ("VENUE-COUPLED: re-measure if the venue
     moves"). Its rule: a mark must sit 0.0847 in luma below the floor (6/255 after two overlaps at alpha 0.15), and
     on its Cathedral tile (luma 0.178) that made SCOUR_VALUE_MUL 0.12, a near-black mark. On the Barrow's snow
     (luma 0.934, the median under him in the film, the same measure) the same rule gives a mark of luma 0.849:
     SCOUR_VALUE_MUL = (0.934 - 0.0847) / luma(SCUFF_COLOR 0.601) = 1.413 -- scoured snow, a shade under the snow,
     where 0.12 laid black blots.
 12. WARMED UNDER THE VEIL (the Fire Ball's lesson). Measured on the page before it: the first Eye of Reckoning
     froze the frame for 1688 ms cold and 164 ms warm -- every layer's pipeline compiled at its first draw. warm(on,
     at) draws each layer once (the two ribbon strips in their real vertex format, one quad of every pool, the
     ground pool) a few frames in front of the camera while the page's veil is still up; whirlwind_channel.gd runs
     it and the veil waits on it.
  7. DRAW ORDER. The Barrow paints its world in a post pass; a transparent effect drawn before it is painted over (the
     crater skin's lesson). Every material of the effect takes PaintStack.AFTER_POST_PRIORITY, as spell_fx, the Fire
     Ball, the crater and the eye glow do.
"""
import pathlib
import re

SRC = pathlib.Path("/Users/admin/Games/reincarnated-godot/scripts")
OUT = pathlib.Path(__file__).resolve().parent.parent / "godot/scripts"


def sub(s, a, b, count=1):
    n = s.count(a)
    assert n == count, (n, count, a[:80])
    return s.replace(a, b)


w = (SRC / "wwcr_whirlwind.gd").read_text()
w = sub(w, "class_name WWCRWhirlwind\n", """class_name BarrowWhirlwind
# ============================================================================
# C-9 R-C9-128 PORT (drax, 2026-10-01): reincarnated-godot scripts/wwcr_whirlwind.gd, EXACTLY as made, rebound to
# the painted Barrow's characters by tools/port_whirlwind.py -- read that file's docstring for the six binding
# changes; everything else below is the source, comments and all.
# ============================================================================
""")
# 1. lengths -> scaled vars
LEN = ["R_ENGAGE", "R_TRAIL", "R_GRIP_SWEEP", "SWEEP_Y", "SWEEP_WOBBLE", "LOWER_BODY_TOP", "SPARK_SIZE",
       "ARC_LIGHT_RANGE", "ONSET_SIZE", "RESIDUE_RISE_MIN", "RESIDUE_RISE_MAX", "SCOUR_Y"]
ARR = ["SHED_SIZE_CLASSES", "RESIDUE_SIZE_CLASSES", "SCOUR_SIZE_CLASSES"]
for n in LEN:
    w, k = re.subn(r"^const %s := " % n, "const %s_M := " % n, w, flags=re.M)
    assert k == 1, n
for n in ARR:
    w, k = re.subn(r"^const %s: Array\[float\] = " % n, "const %s_M: Array[float] = " % n, w, flags=re.M)
    assert k == 1, n
decl = "\n# C-9 PORT: every length, scaled to the character in bind_to (s = H_char / H_STAND)\nvar _s := 1.0\n"
decl += "".join("var %s: float = %s_M\n" % (n, n) for n in LEN)
decl += "".join("var %s: Array = %s_M.duplicate()\n" % (n, n) for n in ARR)
decl += "var _blade_len := 1.5150\nvar _anchor_y := 0.0\nvar _spin_on := false\nvar _k: Node = null\n"
w = sub(w, "signal contact(target: Node3D, point: Vector3)\n", "signal contact(target: Node3D, point: Vector3)\n" + decl)
w = sub(w, """func bind_to(rig: Node3D, skel: Skeleton3D, blade: Node3D) -> void:
	_rig = rig
	_skel = skel
	_blade = blade
	_rng.seed = RNG_SEED
	_pose = WWCRPose.new()
	_pose.name = "WWCRPose"
	skel.add_child(_pose)
""", """func bind_to(rig: Node3D, skel: Skeleton3D, blade: Node3D, h_char: float = H_STAND, knight: Node = null) -> void:
	_rig = rig
	_skel = skel
	_blade = blade
	_k = knight
	_rng.seed = RNG_SEED
	# C-9 PORT 1: every length scaled to this character
	_s = h_char / H_STAND
	for n in %s:
		set(n, float(get(n + "_M")) * _s)
	for n in %s:
		var a: Array = []
		for v in (get(n + "_M") as Array):
			a.append(float(v) * _s)
		set(n, a)
	_blade_len = 1.5150 * _s
	_pose = preload("res://scripts/whirlwind_pose.gd").new()
	_pose.name = "WWCRPose"
	skel.add_child(_pose)
""" % (LEN, ARR))
# 3. the spin: absolute yaw over knight.gd's per-frame seat
w = sub(w, """	if _rig and _w > 0.0:
		_spin += deg_to_rad(OMEGA_DEG) * _w * delta
		_rig.rotate_y(deg_to_rad(OMEGA_DEG) * _w * delta)
""", """	if _rig and _w > 0.0:
		_spin += deg_to_rad(OMEGA_DEG) * _w * delta
	_apply_spin()
""")
w = sub(w, """func _advance_state(delta: float) -> void:""", """func _physics_process(_dt: float) -> void:
	# C-9 PORT 3: knight.gd re-seats his rig every physics frame; this node runs after it (process_physics_priority)
	_apply_spin()


func _apply_spin() -> void:
	if _rig == null:
		return
	var channel := _state != S.IDLE
	if channel and not _spin_on:
		# the spin starts from where he faces, so the source's bearing (sin spin, cos spin) is his
		_spin_on = true
		_spin = float(_k.get("_yaw_cur")) if _k != null else _rig.global_transform.basis.get_euler().y
		var fl = _k.get("_foot_lock") if _k != null else null
		if fl != null:
			fl.release_all()
			fl.enabled = false
	elif not channel and _spin_on:
		# hand the heading back: his own yaw smoothing turns him to his facing from where the spin left him
		_spin_on = false
		if _k != null:
			_k.set("_yaw_cur", _spin)
			var fl2 = _k.get("_foot_lock")
			if fl2 != null:
				fl2.enabled = true
		return
	if not channel:
		return
	var gx := _rig.global_transform
	_rig.global_transform = Transform3D(Basis(Vector3.UP, _spin).scaled(gx.basis.get_scale()), gx.origin)


func _advance_state(delta: float) -> void:""")
# 4. the blade: a proxy on weapon_r, its axis forearm -> hand (re-seated radial by the source's own _reseat_blade)
w = sub(w, """	_clock += delta
	_reseat_blade()
""", """	_clock += delta
	_seat_proxy()
	_reseat_blade()
""")
w = sub(w, """func _blade_segment() -> Array:""", """var _b_grip := -1
var _b_hand := -1
var _b_fore := -1


func _seat_proxy() -> void:
	\"\"\"C-9 PORT 4: the blade proxy sits on the rig's own weapon mount (weapon_r, else RightHand), its long axis
	along forearm -> hand -- the weapon as the clip holds it, before the source's _reseat_blade levels it.\"\"\"
	if _skel == null or _blade == null:
		return
	if _b_hand < 0:
		for i in _skel.get_bone_count():
			var nm := String(_skel.get_bone_name(i))
			if nm == "weapon_r":
				_b_grip = i
			elif nm.ends_with("RightHand"):
				_b_hand = i
			elif nm.ends_with("RightForeArm"):
				_b_fore = i
		if _b_grip < 0:
			_b_grip = _b_hand
	var sx := _skel.global_transform
	var grip := sx * _skel.get_bone_global_pose(_b_grip).origin
	var hand := sx * _skel.get_bone_global_pose(_b_hand).origin
	var fore := sx * _skel.get_bone_global_pose(_b_fore).origin
	var ax := (hand - fore)
	if ax.length() < 1e-5:
		ax = Vector3.UP
	ax = ax.normalized()
	var side := ax.cross(Vector3.UP)
	if side.length() < 1e-4:
		side = Vector3.RIGHT
	side = side.normalized()
	_blade.global_transform = Transform3D(Basis(side, ax, side.cross(ax).normalized()).orthonormalized(), grip)
	_anchor_y = _rig.global_transform.origin.y


func _blade_segment() -> Array:""")
w = sub(w, "	var tip := grip + axis * 1.5150\n", "	var tip := grip + axis * _blade_len\n")
# the pose by preload, not by class name (a new class_name needs the editor's class cache; the web export has none)
w = sub(w, "var _pose: WWCRPose\n", "var _pose\n")
# 2. ground: absolute heights -> anchor.y + height
w = sub(w, "		p.y = SWEEP_Y + _rng.randf_range(-0.07, 0.07)\n", "		p.y = _anchor_y + SWEEP_Y + _rng.randf_range(-0.07, 0.07) * _s\n")
w = sub(w, "		p.y = SCOUR_Y\n", "		p.y = _anchor_y + SCOUR_Y\n")
w = sub(w, "		edge.y = SWEEP_Y * 0.85\n", "		edge.y = _anchor_y + SWEEP_Y * 0.85\n")
w = sub(w, "		p.y = 0.03\n", "		p.y = _anchor_y + 0.03 * _s\n")
# 1. literal lengths in the code
w = sub(w, "		var a: float = (float(i) / float(ONSET_QUANTA)) * TAU + _rng.randf_range(-0.09, 0.09)\n",
        "		var a: float = (float(i) / float(ONSET_QUANTA)) * TAU + _rng.randf_range(-0.09, 0.09)\n")  # radians: unscaled
w = sub(w, "Vector3.UP * _rng.randf_range(0.0, 0.35),", "Vector3.UP * _rng.randf_range(0.0, 0.35) * _s,")
w = sub(w, "		+ Vector3.UP * _rng.randf_range(0.10, 0.85)\n", "		+ Vector3.UP * _rng.randf_range(0.10, 0.85) * _s\n")
w = sub(w, """	var jitter := Vector3(_rng.randf_range(-0.09, 0.09),
		_rng.randf_range(-0.07, 0.07), _rng.randf_range(-0.09, 0.09))""", """	var jitter := Vector3(_rng.randf_range(-0.09, 0.09),
		_rng.randf_range(-0.07, 0.07), _rng.randf_range(-0.09, 0.09)) * _s""")
w = sub(w, "		+ Vector3.UP * _rng.randf_range(0.05, 0.55),\n", "		+ Vector3.UP * _rng.randf_range(0.05, 0.55) * _s,\n")
w = sub(w, """		var jitter := Vector3(_rng.randf_range(-0.16, 0.16),
			_rng.randf_range(-0.10, 0.34), _rng.randf_range(-0.16, 0.16))""", """		var jitter := Vector3(_rng.randf_range(-0.16, 0.16),
			_rng.randf_range(-0.10, 0.34), _rng.randf_range(-0.16, 0.16)) * _s""")
w = sub(w, "		var edge: Vector3 = t.global_transform.origin - to_t * 0.42\n", "		var edge: Vector3 = t.global_transform.origin - to_t * 0.42 * _s\n")
w = sub(w, "		lt.omni_range = 1.1\n", "		lt.omni_range = 1.1 * _s\n")
w = sub(w, "		q2.size = Vector2(0.22, 0.22)\n", "		q2.size = Vector2(0.22, 0.22) * _s\n")
# 6. no light nodes: the spark lights never shown; the ArcLight copied to a ground pool and never shown
w = sub(w, """	_rebuild_ribbon()
	_tick_contacts(delta)
""", """	_rebuild_ribbon()
	_arc_to_pool()
	_tick_contacts(delta)
""")
w = sub(w, """func _trail_window() -> int:""", """var _pool: MeshInstance3D
var _pool_mat: StandardMaterial3D
## C-9 PORT 6: the pool's peak, additive, per unit of the source light's energy -- set by eye against the source's
## lap2 film (its floor pool under the tip at full channel), the one AUTHORED number this port adds
const POOL_GAIN := 0.11


func _arc_to_pool() -> void:
	\"\"\"C-9 PORT 6: the source's ArcLight, never shown (a light node whites the Barrow out on the phone renderer);
	its position, colour and energy laid on the ground as an additive soft pool of its own range.\"\"\"
	if _arc_light == null:
		return
	if _pool == null:
		var q := QuadMesh.new()
		q.size = Vector2.ONE * ARC_LIGHT_RANGE * 2.0
		_pool_mat = StandardMaterial3D.new()
		_pool_mat.albedo_texture = _soft_radial_texture()
		_pool_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		_pool_mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		_pool_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		_pool_mat.disable_receive_shadows = true
		_pool_mat.render_priority = PaintStack.AFTER_POST_PRIORITY
		_pool = MeshInstance3D.new()
		_pool.name = "ArcPool"
		_pool.mesh = q
		_pool.material_override = _pool_mat
		_pool.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_pool.rotation = Vector3(-PI * 0.5, 0.0, 0.0)
		add_child(_pool)
	var on := _arc_light.visible and _arc_light.light_energy > 0.0
	_pool.visible = on
	if on:
		var p := _arc_light.global_position
		_pool.global_position = Vector3(p.x, _anchor_y + 0.02 * _s, p.z)
		var c := _arc_light.light_color
		var g: float = POOL_GAIN * _arc_light.light_energy
		_pool_mat.albedo_color = Color(c.r * g, c.g * g, c.b * g, 1.0)
	_arc_light.visible = false


func _trail_window() -> int:""")
w = sub(w, """		lt.light_energy = 0.0
		lt.shadow_enabled = false                                        # C-1
""", """		lt.light_energy = 0.0
		lt.visible = false
		lt.shadow_enabled = false                                        # C-1
""")
# 7. draw after the paint post pass
w = sub(w, """	_build_ribbon()
	_build_pools()
	set_element(element_color)
""", """	_build_ribbon()
	_build_pools()
	# C-9 PORT 7: drawn after the Barrow's paint post pass, or the paint covers it
	for m in [_ribbon_mat, _ribbon_body_mat, _spark_mat, _scuff_mat, _shed_mat, _scour_mat, _residue_mat]:
		if m != null:
			(m as Material).render_priority = PaintStack.AFTER_POST_PRIORITY
	set_element(element_color)
""")
# 8. the arc window in time (10 samples at 60 fps)
w = sub(w, """func _trail_window() -> int:
	if _state == S.FALLING:
		return maxi(2, int(ceil(float(TRAIL_SAMPLES) * _w)))
	return TRAIL_SAMPLES""", """func _trail_window() -> int:
	# C-9 PORT 8: the source's 10 samples are 10/60 s of blade; held in TIME, so a 30 fps frame keeps the 150 deg arc
	var n := maxi(2, int(round(float(TRAIL_SAMPLES) * (1.0 / 60.0) / maxf(_dt_avg, 1e-4))))
	if _state == S.FALLING:
		return maxi(2, int(ceil(float(n) * _w)))
	return n""")
w = sub(w, """	_clock += delta
	_seat_proxy()""", """	_clock += delta
	_dt_avg = lerpf(_dt_avg, clampf(delta, 1.0 / 240.0, 0.1), 0.1) if delta > 0.0 else _dt_avg
	_seat_proxy()""")
# 9. the spin from the clip
w = sub(w, "var _blade_len := 1.5150\n", "var _blade_len := 1.5150\nvar _dt_avg := 1.0 / 60.0\n## C-9 PORT 9\nvar spin_from_clip := false\nvar blade_head_local := Vector3.ZERO\nvar _prev_b := 0.0\nvar _clip_spin_on := false\n")
w = sub(w, """	if _pose:
		_pose.sweep_w = clampf(_w * 1.6, 0.0, 1.0)
		_pose.windup_w = _windup_t
""", """	if _pose:
		_pose.sweep_w = 0.0 if (spin_from_clip or ribbon_only) else clampf(_w * 1.6, 0.0, 1.0)
		_pose.windup_w = 0.0 if (spin_from_clip or ribbon_only) else _windup_t
""")
w = sub(w, """	if _rig and _w > 0.0:
		_spin += deg_to_rad(OMEGA_DEG) * _w * delta
	_apply_spin()
""", """	if spin_from_clip:
		pass                                 # C-9 PORT 9: _spin is read off the weapon head in _seat_proxy
	elif _rig and _w > 0.0:
		_spin += deg_to_rad(OMEGA_DEG) * _w * delta
	if not spin_from_clip:
		_apply_spin()
""")
w = sub(w, """func _physics_process(_dt: float) -> void:
	# C-9 PORT 3: knight.gd re-seats his rig every physics frame; this node runs after it (process_physics_priority)
	_apply_spin()""", """func _physics_process(_dt: float) -> void:
	# C-9 PORT 3: knight.gd re-seats his rig every physics frame; this node runs after it (process_physics_priority)
	if not spin_from_clip:
		_apply_spin()""")
w = sub(w, """func _reseat_blade() -> void:
""", """func _reseat_blade() -> void:
	if spin_from_clip:
		return                               # C-9 PORT 9: the clip holds the real weapon; nothing re-seats it
""")
w = sub(w, """	var sx := _skel.global_transform
	var grip := sx * _skel.get_bone_global_pose(_b_grip).origin""", """	var sx := _skel.global_transform
	if spin_from_clip and blade_head_local != Vector3.ZERO:
		# C-9 PORT 9: the real weapon -- the grip at weapon_r, the tip at its head -- and _spin the head's bearing
		var wx := sx * _skel.get_bone_global_pose(_b_grip)
		var g0 := wx.origin
		var hd := wx * blade_head_local
		var ax9 := hd - g0
		_blade_len = ax9.length()
		ax9 = ax9.normalized()
		var side9 := ax9.cross(Vector3.UP)
		if side9.length() < 1e-4:
			side9 = Vector3.RIGHT
		side9 = side9.normalized()
		_blade.global_transform = Transform3D(Basis(side9, ax9, side9.cross(ax9).normalized()).orthonormalized(), g0)
		var c9 := _rig.global_transform.origin
		_anchor_y = c9.y
		var b := atan2(hd.x - c9.x, hd.z - c9.z)
		var live := _state != S.IDLE
		if live and not _clip_spin_on:
			_spin = b
		elif live:
			_spin += wrapf(b - _prev_b, -PI, PI)
		_clip_spin_on = live
		_prev_b = b
		return
	var grip := sx * _skel.get_bone_global_pose(_b_grip).origin""")
# 10. two blades: the grip bone is a parameter; a ribbon-only instance skips every once-per-character layer
w = sub(w, "var spin_from_clip := false\n", "var spin_from_clip := false\n## C-9 PORT 10\nvar grip_bone := \"weapon_r\"\nvar ribbon_only := false\n")
w = sub(w, """		for i in _skel.get_bone_count():
			var nm := String(_skel.get_bone_name(i))
			if nm == "weapon_r":
				_b_grip = i
			elif nm.ends_with("RightHand"):
				_b_hand = i
			elif nm.ends_with("RightForeArm"):
				_b_fore = i""", """		var side := "Left" if grip_bone.ends_with("_l") else "Right"
		for i in _skel.get_bone_count():
			var nm := String(_skel.get_bone_name(i))
			if nm == grip_bone:
				_b_grip = i
			elif nm.ends_with(side + "Hand"):
				_b_hand = i
			elif nm.ends_with(side + "ForeArm"):
				_b_fore = i""")
w = sub(w, """func _fire_onset() -> void:
""", """func _fire_onset() -> void:
	if ribbon_only:
		return                               # C-9 PORT 10: once per character
""")
w = sub(w, """func _tick_contacts(_delta: float) -> void:
""", """func _tick_contacts(_delta: float) -> void:
	if ribbon_only:
		return                               # C-9 PORT 10: contacts, sparks, scuffs and scour once per character
""")
w = sub(w, """	var on := _arc_light.visible and _arc_light.light_energy > 0.0""", """	var on := _arc_light.visible and _arc_light.light_energy > 0.0 and not ribbon_only""")
w = sub(w, """func _apply_spin() -> void:
	if _rig == null:
		return""", """func _apply_spin() -> void:
	if _rig == null or ribbon_only:
		return""")
# 11. the scour's value re-derived for the Barrow's snow by the source's own rule
w = sub(w, """	_scour_mat.albedo_color = Color(SCUFF_COLOR.r * SCOUR_VALUE_MUL,
		SCUFF_COLOR.g * SCOUR_VALUE_MUL, SCUFF_COLOR.b * SCOUR_VALUE_MUL)""", """	# C-9 PORT 11: the source's rule (floor - 0.0847) on the Barrow's snow, not its Cathedral tile
	var svm: float = (BARROW_FLOOR_LUMA - SCOUR_DEPTH_LUMA) / (0.2126 * SCUFF_COLOR.r + 0.7152 * SCUFF_COLOR.g + 0.0722 * SCUFF_COLOR.b)
	_scour_mat.albedo_color = Color(SCUFF_COLOR.r * svm, SCUFF_COLOR.g * svm, SCUFF_COLOR.b * svm)""")
w = sub(w, "const SCOUR_Y_M := 0.016\n", "const SCOUR_Y_M := 0.016\n## C-9 PORT 11: the venue -- the Barrow's snow luma (film median under him) and the source's required depth\nconst BARROW_FLOOR_LUMA := 0.934\nconst SCOUR_DEPTH_LUMA := 0.0847\n")
# 12. warm every layer's pipeline under the veil
w = sub(w, """func _trail_window() -> int:""", """func warm(on: bool, at: Vector3) -> void:
	\"\"\"C-9 PORT 12: draw every layer once, in its real format, at `at` (in front of the camera, under the veil).\"\"\"
	_ribbon_mesh.clear_surfaces()
	_ribbon_body_mesh.clear_surfaces()
	if on:
		for m in [_ribbon_mesh, _ribbon_body_mesh]:
			(m as ImmediateMesh).surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
			# a real-sized strip (12 vertices, 1.2 m, level, faint): a sub-pixel strip drew nothing and warmed nothing
			for i in 12:
				(m as ImmediateMesh).surface_set_color(Color(1, 1, 1, 0.04))
				(m as ImmediateMesh).surface_add_vertex(to_local(at + Vector3(0.1 * float(i), 0.0, 0.25 * float(i % 2))))
			(m as ImmediateMesh).surface_end()
	for arr in [_sparks, _shed, _scuffs, _scour, _residue]:
		if (arr as Array).is_empty():
			continue
		var mi: MeshInstance3D = (arr as Array)[0]["mi"]
		mi.global_position = at
		mi.transparency = 0.5 if on else 0.0
		mi.visible = on
	if _shed.size() > 0:
		var mo: MeshInstance3D = _shed[_shed.size() - 1]["mi"]       # an onset quantum (its own size class)
		mo.global_position = at
		mo.transparency = 0.5 if on else 0.0
		mo.visible = on
	if _arc_light != null:
		_arc_light.global_position = at
		_arc_light.light_energy = 0.01 if on else 0.0
		_arc_light.visible = on
		_arc_to_pool()


func _trail_window() -> int:""")
(OUT / "whirlwind_fx.gd").write_text(w)

p = (SRC / "wwcr_pose.gd").read_text()
p = sub(p, "class_name WWCRPose\n", """class_name BarrowWhirlwindPose
# C-9 R-C9-128 PORT (drax): reincarnated-godot scripts/wwcr_pose.gd, its bone names mapped to the Barrow's rigs by
# tools/port_whirlwind.py (UpperArm -> Arm, LowerArm -> ForeArm, Spine -> the spine bone whose parent is Hips).
const BONE_MAP := {"LeftUpperArm": "LeftArm", "LeftLowerArm": "LeftForeArm", "RightUpperArm": "RightArm",
	"RightLowerArm": "RightForeArm"}
""")
p = sub(p, """			_bones[n] = skel.find_bone(n)
""", """			_bones[n] = skel.find_bone(String(BONE_MAP.get(n, n)))
		# the first spine bone above the hips (this rig: Spine02)
		var hi := skel.find_bone("Hips")
		for i in skel.get_bone_count():
			if skel.get_bone_parent(i) == hi and String(skel.get_bone_name(i)).contains("Spine"):
				_bones["Spine"] = i
""")
(OUT / "whirlwind_pose.gd").write_text(p)
print("ported:", OUT / "whirlwind_fx.gd", len(w.splitlines()), "lines;", OUT / "whirlwind_pose.gd", len(p.splitlines()), "lines")
