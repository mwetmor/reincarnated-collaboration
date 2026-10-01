extends "res://scripts/knight.gd"
## C-9 R-C9-117 -- HIS knight.gd (the page's own, unchanged) reading a variant character slot: the freed champion.
## The champion carries no weapon (R-C9-105), so he is never armed and his unarmed SLASH / CHOP play the champion
## body's JOIN moves (whirlwind, war cry). The clipless nodes are filled as hers are (he has no unarmed strafe).
var slot_path := ""


func _read_cfg() -> Dictionary:
	if slot_path == "":
		return super()
	var j = JSON.parse_string(FileAccess.get_file_as_string(slot_path)) if FileAccess.file_exists(slot_path) else null
	return j if typeof(j) == TYPE_DICTIONARY else {}


func _build_anim_tree() -> void:
	super()
	_fill_clipless()


func _apply_clip_set() -> void:
	super()
	_fill_clipless()


func _fill_clipless() -> void:
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
