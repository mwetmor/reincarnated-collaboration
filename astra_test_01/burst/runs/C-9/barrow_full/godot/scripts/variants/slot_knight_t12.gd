extends "res://scripts/variants/knight_t12_11.gd"
## C-9 R-C9-117 (WEB ONLY) -- the INSTALLED T12_11 knight (attack_lab/staged/t12_11/knight.gd, byte copy 86141f65)
## reading a variant slot: the T12_11, F25L and F40L axe holds. Nothing here reaches cliffside3d.
var slot_path := ""


func _read_cfg() -> Dictionary:
	if slot_path == "":
		return super()
	var j = JSON.parse_string(FileAccess.get_file_as_string(slot_path)) if FileAccess.file_exists(slot_path) else null
	return j if typeof(j) == TYPE_DICTIONARY else {}
