extends SceneTree
# scratch: a parse gate. Godot can only load scripts through res://, which is why this file
# lives in the project at all. Deleted by the caller.
func _init() -> void:
	var bad := 0
	for p in ["res://scripts/paint_stack.gd", "res://scripts/world.gd", "res://scripts/gear.gd",
			  "res://scripts/knight.gd", "res://scripts/snow_field.gd",
			  "res://scripts/snow_lab.gd"]:
		var s = load(p)
		if s == null:
			print("PARSE_FAIL %s" % p)
			bad += 1
		else:
			print("ok %s" % p)
	print("PARSE_BAD=%d" % bad)
	quit(0)
