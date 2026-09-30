"""Apply the foot-lock integration to a knight.gd (lab copy and production candidate alike)."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
lab = "--lab" in sys.argv

def rep(old, new, tag):
    global t
    assert old in t, "anchor missing: " + tag
    t = t.replace(old, new, 1)

rep('const CharGear := preload("res://scripts/gear.gd")',
    'const CharGear := preload("res://scripts/gear.gd")\nconst FootLock := preload("res://scripts/foot_lock.gd")', "preload")

rep('var _block_lower_rate := 1.0', '''var _block_lower_rate := 1.0
## FOOT LOCK -- see scripts/foot_lock.gd
var _foot_lock: Node = null
var _strike_anim := ""        # the playing strike's AnimationNodeAnimation, e.g. "a_slash"
var _strike_len := 0.0
var _strike_out_sent := false
var _was_moving := false''', "state")

rep('''	_build_anim_tree()''', '''	_build_anim_tree()
	_add_foot_lock()''', "ready")

rep('''		_blocking = false
		_tree.set("parameters/%s/request" % node, AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)''',
'''		_blocking = false
		_tree.set("parameters/%s/request" % node, AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
		# the feet stay where they stand while the body blends into the strike
		_strike_anim = "a_" + which
		_strike_len = float(_clip_len.get(String(_roles.get(role, "")), 0.0))
		_strike_out_sent = false
		_foot_transition("strike_in", float((_tree.tree_root as AnimationNodeBlendTree).get_node(node).get("fadein_time")))''', "strike")

rep('''		_block_req_frame = Engine.get_physics_frames()''', '''		_block_req_frame = Engine.get_physics_frames()
		_foot_transition("block_in", _block_fade_s())''', "block_in")

rep('''	elif _block_phase == "lower" and pos <= _block_t0 + 1e-3:
		_tree.set("parameters/ts_block/scale", 0.0)
		_block_phase = "off"''', '''	elif _block_phase == "lower" and pos <= _block_t0 + 1e-3:
		_tree.set("parameters/ts_block/scale", 0.0)
		_block_phase = "off"
		_foot_transition("block_out", _block_fade_s())''', "block_out")

rep('''	if _strafing:
		want = strafe_px_s()
	elif attacking() or _blocking:
		want = 0.0                       # a strike roots him, and so does a brace''',
'''	if _strafing:
		want = strafe_px_s()
	elif attacking() or _blocking:
		want = 0.0                       # a strike roots him, and so does a brace
	_foot_lock_tick(want)''', "tick")

rep('''func _block_tick() -> void:''', '''func _add_foot_lock() -> void:
	"""Leg IK that holds planted feet through strike and block transitions (foot_lock.gd).
	Off with `"foot_lock": false` in character.json; needs TwoBoneIK3D (Godot 4.6+)."""
	if _skel == null or not bool(cfg.get("foot_lock", true)) or not ClassDB.class_exists("TwoBoneIK3D"):
		return
	_foot_lock = FootLock.new()
	_foot_lock.name = "FootLock"
	_skel.add_child(_foot_lock)
	_foot_lock.setup(self, _skel)%s


func _foot_transition(kind: String, hold_s: float) -> void:
	if _foot_lock != null:
		_foot_lock.transition(kind, hold_s)


func _block_fade_s() -> float:
	return float((cfg.get("transitions", {}) as Dictionary).get("block_fade_s", float(cfg.get("block_fade_s", 0.12))))


func _foot_lock_tick(want: float) -> void:
	"""Two events drive_dir can see that set_block and try_strike cannot: a strike's FADE-OUT
	starting (the body blends back to guard -- the feet hold again), and locomotion taking
	over (the walk owns the feet -- any lock is handed back as a short step)."""
	if _foot_lock == null or _tree == null:
		return
	if attacking() and _strike_anim != "" and not _strike_out_sent:
		var fout := float((cfg.get("transitions", {}) as Dictionary).get("attack_fade_out_s", 0.25))
		var pos: float = float(_tree.get("parameters/%%s/current_position" %% _strike_anim))
		if _strike_len > 0.0 and pos >= _strike_len - fout:
			_strike_out_sent = true
			_foot_transition("strike_out", fout)
	var moving: bool = want > 0.0 and not attacking()
	if moving and not _was_moving:
		_foot_lock.release_all()
	_was_moving = moving


func _block_tick() -> void:''' % ('''
	if OS.has_environment("LAB_FOOTLOCK") and OS.get_environment("LAB_FOOTLOCK") == "0":
		_foot_lock.enabled = false      # LAB ONLY: same instrument, no locking''' if lab else ''), "helpers")
p.write_text(t); print("foot-lock integrated:", p.name, "(lab switch)" if lab else "")
