extends "res://scripts/knight.gd"
## C-9 -- THE SORCERESS, THROUGH knight.gd UNCHANGED (the painted Barrow's ?c=sorceress). drax.
##
## knight.gd reads its occupant from ONE file, res://data/character.json, and nothing else about
## her: her slot (so_d7/scene_pkg/character_sorceress.json, in character.json's own shape: her
## model, clips by role, gear stacks, staff layers, casts) is read by overriding the one method that
## opens it. Every line of knight.gd runs as it does for him -- the file stays the installed byte
## copy (T12_9, ea761ba8).

const SORCERESS_CHARACTER := "res://data/character_sorceress.json"


func _read_cfg() -> Dictionary:
	if not FileAccess.file_exists(SORCERESS_CHARACTER):
		push_error("sorceress: no character slot at %s" % SORCERESS_CHARACTER)
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(SORCERESS_CHARACTER))
	return j if typeof(j) == TYPE_DICTIONARY else {}


# --- the one thing knight.gd's tree cannot take from her slot, filled from outside ----------------
# GODOT 4.6: AN AnimationNodeAnimation NAMING NO CLIP MAKES THE WHOLE AnimationTree INVALID, and an
# invalid tree applies NO pose at all -- no error printed, the clips' positions still advancing. She
# has no block and no strafe, so knight.gd's a_block and a_strafe name "" -- and her tree stood her
# frozen in one pose: the walk advancing, LeftUpLeg unmoved over 30 frames, the Fire Ball's forearm
# unmoved (godot/tools/_dbg: bisected to those two nodes; each pointed at a clip she has, the legs
# moved 0.63 rad and the forearm 1.74). Both nodes are only ever blended at weight 0 for her (no
# block key does anything without a block role; no strafe role engages), so her idle there is inert.
# Re-applied after every clip-set change: _apply_clip_set writes the "" back.
var clipless_filled: Array = []


func _build_anim_tree() -> void:
	super()
	_fill_clipless_nodes()


func _apply_clip_set() -> void:
	super()
	_fill_clipless_nodes()


func _fill_clipless_nodes() -> void:
	if _tree == null or _anim == null:
		return
	var bt := _tree.tree_root as AnimationNodeBlendTree
	if bt == null:
		return
	var fallback := String(_roles.get("idle", "idle"))
	if not _anim.has_animation(fallback):
		return
	for nm in bt.get_node_list():
		var n = bt.get_node(nm)
		if n is AnimationNodeAnimation:
			var an := String((n as AnimationNodeAnimation).animation)
			if an == "" or not _anim.has_animation(an):
				(n as AnimationNodeAnimation).animation = fallback
				if not clipless_filled.has(String(nm)):
					clipless_filled.append(String(nm))


# --- her physics step, timed (tools/perf_cast.gd reads it; two clock reads a tick) ------------------
var _diag_phys_us := -1


func _physics_process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	super(dt)
	_diag_phys_us = Time.get_ticks_usec() - t0


func diag_take() -> Dictionary:
	"""The last physics step's own time (knight.gd's _physics_process, which drives the tree's
	parameters, the feet and the releases), once: -1 after it is read."""
	if _diag_phys_us < 0:
		return {}
	var d := {"phys_us": _diag_phys_us}
	_diag_phys_us = -1
	return d


# --- her spells need the staff (so_d7/scene_pkg README, GEAR; the coordinator's gate, key half) ---------
# knight.gd has no unarmed state without an attack: it binds a missing attack to idle, so an unarmed
# slash would still strike -- and spell_fx would throw the Fire Ball at its release time.
func try_strike(which: String) -> bool:
	return super(which) if armed() else false
