extends SceneTree
## BV2F lane PH (R-C9-268 follow-up): NEW v1 RECORD-TIME stills for P11's v1rec-vs-v1head control under the § 48 (b) class
## exclusion. The recipe is barrow_full/godot/tools/v2sw_run.gd's `v1stills` mode COPIED unchanged in method (the source of
## section_v1cam/v1ref/V1_*.png): res://scenes/barrow_painted.tscn added to root, HUD + crucible off, him placed at
## (u - 1.5, v - 1.0) facing S, park_camera on (u, v), settle 10 + 30 frames, the ROOT window's texture saved (window
## 1920x1080). Only the VIEWS differ: non-ice views (no tarn in frame: the tarn ellipse (-13.5, -5) 12 x 9 m stays outside
## the 19.1 x 13.4 m frame), on snow, heather, rock and stones.
##   Godot --path . --resolution 1920x1080 --script <abs>/ph_v1rec_stills.gd -- OUT
const S := [["V1R_se", Vector2(8.0, -11.0)], ["V1R_e", Vector2(11.0, -1.0)], ["V1R_ne", Vector2(6.0, 7.0)],
	["V1R_nw", Vector2(-6.0, 8.0)], ["V1R_w", Vector2(-12.0, 9.0)]]
var scene
var out_dir := ""
var wait := 0
var k := 0
var settle := 10


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	out_dir = args[0]
	DirAccess.make_dir_recursive_absolute(out_dir)
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)


func _process(_delta: float) -> bool:
	if not scene.ready_done:
		return false
	if k >= S.size():
		var f := FileAccess.open(out_dir.path_join("views.json"), FileAccess.WRITE)
		var v := {}
		for s in S:
			v[s[0]] = {"png": s[0] + ".png", "centre_uv": [s[1].x, s[1].y], "knight_uv": [s[1].x - 1.5, s[1].y - 1.0], "facing": "S"}
		f.store_string(JSON.stringify({"_what": "PH v1 record-time stills (v2sw_run.gd v1stills recipe), non-ice views", "views": v}, " "))
		f.close()
		print("[ph_v1rec] done")
		return true
	if wait == 0:
		scene.set_hud_visible(false)
		scene.set_crucible_visible(false)
		var uv: Vector2 = S[k][1]
		scene.place_knight(uv.x - 1.5, uv.y - 1.0, "S")
		scene.park_camera(scene.uv_to_world(uv.x, uv.y))
	wait += 1
	if wait < settle + 30:
		return false
	root.get_texture().get_image().save_png(out_dir.path_join("%s.png" % S[k][0]))
	print("[ph_v1rec] still %s" % S[k][0])
	k += 1
	wait = 0
	return false
