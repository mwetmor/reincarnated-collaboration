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
