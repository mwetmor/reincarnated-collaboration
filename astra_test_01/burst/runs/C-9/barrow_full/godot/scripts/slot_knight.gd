extends "res://scripts/sorceress_knight.gd"
## C-9 R-C9-117 -- ANY CHARACTER SLOT through her knight (sorceress_knight.gd: knight.gd unchanged, the clipless
## nodes filled, the strikes gated on armed()): the battle mage's two sets and the dark knight. drax.
## slot_path is set before setup(); knight.gd reads the occupant from it and from nothing else.
var slot_path := ""


func _read_cfg() -> Dictionary:
	if slot_path == "":
		return super()
	if not FileAccess.file_exists(slot_path):
		push_error("slot: no character slot at %s" % slot_path)
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(slot_path))
	return j if typeof(j) == TYPE_DICTIONARY else {}


# --- R-C9-128: THE EYE OF RECKONING ------------------------------------------------------------------------------
# The dark knight's spin is a CLIP (wl_e1 final_k_eor: eor_spin_start 0.200 s accelerating, then eor_spin_loop
# 0.300 s, one CCW revolution that closes exactly; recipe (a), in place). It plays OVER the whole tree while he
# channels -- he keeps moving (the GD packet: canUseWhileMoving), the body is the spin's. The channel and the effect
# are whirlwind_channel.gd + whirlwind_fx.gd (the port); this block only plays the clip. BASH has no use on a man
# with no shield, so its key and button carry the Eye of Reckoning (the button relabelled by barrow_full).
const EOR_LOOPS := 40                        # 0.2 + 40 x 0.3 = 12.2 s of spin: the longest a held channel lasts
const EOR_FADE_S := 0.10
var whirl_channel = null
var _eor_ok := false
var _eor_w := 0.0
var _eor_on := false


func try_strike(which: String) -> bool:
	if which == "bash" and whirl_channel != null:
		if not armed():
			return false                         # the Eye of Reckoning is the mace's, as attack and the war cry are
		return whirl_channel.press()
	return super(which)


func _build_anim_tree() -> void:
	super()
	_eor_inject()


func _apply_clip_set() -> void:
	super()
	_eor_inject()


func _eor_inject() -> void:
	"""eor_chan = start + EOR_LOOPS x loop, one Animation, and a Blend2 over the tree's output."""
	if _anim == null or _tree == null or _strikes.is_empty():
		return
	# Godot's glTF import takes a "_loop" suffix as the loop flag and strips it: eor_spin_loop arrives as eor_spin
	var loop_nm := "eor_spin_loop" if _anim.has_animation("eor_spin_loop") else "eor_spin"
	if not (_anim.has_animation("eor_spin_start") and _anim.has_animation(loop_nm)):
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null or bt.has_node("eor_blend"):
		return
	if not _anim.has_animation("eor_chan"):
		var st := _anim.get_animation("eor_spin_start")
		var lp := _anim.get_animation(loop_nm)
		var a := Animation.new()
		a.length = st.length + lp.length * EOR_LOOPS
		var paths := {}
		for src in [st, lp]:
			for ti in (src as Animation).get_track_count():
				paths[str((src as Animation).track_get_path(ti)) + "|" + str((src as Animation).track_get_type(ti))] = [
					(src as Animation).track_get_path(ti), (src as Animation).track_get_type(ti),
					(src as Animation).track_get_interpolation_type(ti)]
		for key in paths:
			var spec: Array = paths[key]
			var nt := a.add_track(int(spec[1]))
			a.track_set_path(nt, spec[0])
			a.track_set_interpolation_type(nt, int(spec[2]))
			var si := st.find_track(spec[0], int(spec[1]))
			if si >= 0:
				for ki in st.track_get_key_count(si):
					a.track_insert_key(nt, st.track_get_key_time(si, ki), st.track_get_key_value(si, ki))
			var li := lp.find_track(spec[0], int(spec[1]))
			if li >= 0:
				for n in EOR_LOOPS:
					var off := st.length + lp.length * n
					for ki in lp.track_get_key_count(li):
						a.track_insert_key(nt, off + lp.track_get_key_time(li, ki), lp.track_get_key_value(li, ki))
		var lib := _anim.get_animation_library("")
		if lib == null:
			lib = AnimationLibrary.new()
			_anim.add_animation_library("", lib)
		lib.add_animation("eor_chan", a)
	var last := String(_strikes.back())
	var an := AnimationNodeAnimation.new()
	an.animation = "eor_chan"
	bt.add_node("eor_anim", an, Vector2(1400, 280))
	bt.add_node("eor_seek", AnimationNodeTimeSeek.new(), Vector2(1400, 190))
	bt.add_node("eor_blend", AnimationNodeBlend2.new(), Vector2(1550, 100))
	bt.disconnect_node("output", 0)
	bt.connect_node("eor_seek", 0, "eor_anim")
	bt.connect_node("eor_blend", 0, last)
	bt.connect_node("eor_blend", 1, "eor_seek")
	bt.connect_node("output", 0, "eor_blend")
	_tree.set("parameters/eor_blend/blend_amount", 0.0)
	_eor_ok = true


func eor_begin() -> void:
	if not _eor_ok:
		return
	_tree.set("parameters/eor_seek/seek_request", 0.0)
	_eor_on = true


func eor_end() -> void:
	_eor_on = false


func _physics_process(dt: float) -> void:
	super(dt)
	if _eor_ok:
		_eor_w = move_toward(_eor_w, 1.0 if _eor_on else 0.0, dt / EOR_FADE_S)
		_tree.set("parameters/eor_blend/blend_amount", _eor_w)
