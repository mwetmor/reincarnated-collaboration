extends SceneTree
## Empty --path + --main-pack Windows PCK; no loose project assets allowed.
## On this Mac only, pre-load the unchanged pinned Mac extension to exercise
## the packed scene. --reference-probe switches through the fight's public API.

var scene = null
var counts := {"MeshInstance3D": 0, "CollisionShape3D": 0, "MultiMeshInstance3D": 0}

func _initialize() -> void:
	call_deferred("_run")

func _count(node: Node) -> void:
	for key in counts:
		if node.is_class(key):
			counts[key] += 1
	for child in node.get_children():
		_count(child)

func _fail(message: String) -> void:
	push_error("NATIVE_SCENE: FAIL; " + message)
	quit(1)

func _run() -> void:
	if OS.get_name() == "macOS":
		var lib := "/Users/admin/Games/reincarnated-godot/kc2_runtime/native/bin/libkc2rt_contact.macos.arm64.dylib"
		if FileAccess.get_sha256(lib) != "74360ffae1a434ba0de85708009c8129c6b39c4ca03898a3e4be01641e27467f":
			_fail("Mac probe extension differs from pin")
			return
		var status := GDExtensionManager.load_extension("/Users/admin/Games/reincarnated-godot/kc2_runtime/native/kc2rt_contact.gdextension")
		if status not in [GDExtensionManager.LOAD_STATUS_OK, GDExtensionManager.LOAD_STATUS_ALREADY_LOADED]:
			_fail("Mac probe extension could not load")
			return
	if ProjectSettings.get_setting("rendering/renderer/rendering_method") != "forward_plus":
		_fail("native renderer changed")
		return
	var Paths = load("res://scripts/arena/arena_paths.gd")
	var error: String = Paths.verify_bundle()
	if error != "":
		_fail(error)
		return
	var legacy := "/Users/admin/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv"
	if FileAccess.get_sha256(legacy) != "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e":
		_fail("legacy packed table alias failed")
		return
	scene = load("res://scenes/bv2f_arena.tscn").instantiate()
	root.add_child(scene)
	var deadline := Time.get_ticks_msec() + 120000
	while (scene.arena == null or not scene.arena.running) and Time.get_ticks_msec() < deadline:
		if scene.arena != null and scene.arena.fatal != "":
			_fail(scene.arena.fatal)
			return
		await process_frame
	if scene.arena == null or not scene.arena.running:
		_fail("scene startup timed out")
		return
	var arena = scene.arena
	if scene.PILOT_MANIFEST != "res://data/bv2f/site_ph4/painted/manifest.json":
		_fail("did not select full native painting")
		return
	if not arena.hero_3d or arena.hero3d == null or arena.enemy_vfx == null or not arena.enemy_vfx.ok:
		_fail("3D hero or enemy VFX missing")
		return
	_count(scene)
	if counts["MeshInstance3D"] < 100 or counts["CollisionShape3D"] < 10 or arena.walk_reach.count(1) < 100:
		_fail("native geometry/collisions/walk map incomplete: " + JSON.stringify(counts))
		return
	var stamp: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(Paths.STAMP))
	var Art = load("res://scripts/arena/arena_art.gd")
	var decoded := 0
	for kit in stamp["kit_sources"]:
		var meta: Dictionary = Art.kit_meta(kit)
		if meta.is_empty() or meta.get("cells", {}).is_empty():
			_fail("missing kit " + kit)
			return
		var cell: Dictionary = meta["cells"].values()[0]
		var image: Image = Paths.load_image(Art.root_of(kit) + cell["file"])
		if image == null:
			_fail("could not decode native kit " + kit)
			return
		decoded += 1
	if OS.get_cmdline_user_args().has("--reference-probe"):
		if not arena.session.fight.select_contact_solver("gdscript"):
			_fail("reference solver selection refused")
			return
	arena.autopilot = "channel"
	arena.fight_started = true
	var before: int = int(arena.snap.get("tick", 0))
	var position: Vector2 = arena.player_pos_m
	var start := Time.get_ticks_msec()
	while Time.get_ticks_msec() - start < 10000:
		await process_frame
	var after: int = int(arena.snap.get("tick", 0))
	if after <= before or arena.player_pos_m.distance_to(position) < 0.1:
		_fail("fight/movement did not advance")
		return
	var result := {"renderer_setting": "forward_plus", "painting": scene.PILOT_MANIFEST,
		"geometry": counts, "walk_reachable_cells": arena.walk_reach.count(1),
		"decoded_full_resolution_kits": decoded, "hero": "3d", "enemy_vfx_sets": arena.enemy_vfx.sets.size(),
		"solver": arena.session.fight.contact_solver, "ticks_advanced": after - before,
		"distance_m": arena.player_pos_m.distance_to(position), "platform_executed": OS.get_name()}
	print("NATIVE_SCENE: PASS; " + JSON.stringify(result))
	var args := OS.get_cmdline_user_args()
	var at := args.find("--evidence-dir")
	if at >= 0 and at + 1 < args.size():
		var directory := args[at + 1]
		DirAccess.make_dir_recursive_absolute(directory)
		var file := FileAccess.open(directory.path_join("native_probe.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify(result, "\t"))
		file.close()
		if DisplayServer.get_name() != "headless":
			var image := root.get_texture().get_image()
			image.save_png(directory.path_join("native_probe.png"))
	arena._close_recording("native package probe")
	quit(0)
