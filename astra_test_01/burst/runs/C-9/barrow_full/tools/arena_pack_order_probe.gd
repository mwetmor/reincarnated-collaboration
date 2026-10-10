extends SceneTree
## Run with --path an EMPTY folder, --main-pack index.pck, and -- --as-web --pack-dir <web export>.
## An export mirror's loose files must never mask a missing packed dependency.

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var at := args.find("--pack-dir")
	if at < 0 or at + 1 >= args.size():
		push_error("PACK_ORDER: --pack-dir is required")
		quit(1)
		return
	var scene = load("res://scripts/arena/bv2f_arena.gd").new()
	var stamp: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://kc2/bundle/BUNDLE_STAMP.json"))
	for nm in stamp["kit_packs"]:
		if not ProjectSettings.load_resource_pack(String(args[at + 1]).path_join(String(nm))):
			push_error("PACK_ORDER: could not mount %s" % nm)
			scene.free()
			quit(1)
			return
	var selected: bool = scene.call("_select_web_paint")
	var expected := "res://data/bv2f/site_ph4/painted_web/manifest.json"
	var bundle_error: String = load("res://scripts/arena/arena_paths.gd").verify_bundle()
	var ok: bool = selected and scene.PILOT_MANIFEST == expected and FileAccess.file_exists(expected) and bundle_error == ""
	print("PACK_ORDER: %s; selected %s; bundle %s" % ["PASS" if ok else "FAIL", scene.PILOT_MANIFEST, "intact" if bundle_error == "" else bundle_error])
	scene.free()
	quit(0 if ok else 1)
