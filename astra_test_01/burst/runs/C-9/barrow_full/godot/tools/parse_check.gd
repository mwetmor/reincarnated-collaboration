extends SceneTree
# Loads every script this sandbox uses and asks whether it can INSTANTIATE. load() alone is not
# the check: a script with a parse error still loads as a (broken) resource, non-null, and the
# first version of this file printed PARSE_BAD=0 directly under a "Parse Error" line.
func _initialize() -> void:
	var bad := 0
	for p in ["res://scripts/paint_stack.gd", "res://scripts/world.gd", "res://scripts/gear.gd",
			  "res://scripts/knight.gd", "res://scripts/barrow_full.gd", "res://tools/capture_blockout.gd"]:
		var s = load(p)
		if s == null or not (s as Script).can_instantiate():
			print("PARSE_FAIL %s" % p)
			bad += 1
	print("PARSE_BAD=%d" % bad)
	quit(0)
