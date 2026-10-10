extends "res://scripts/bv2f/bv2f_pilot.gd"
## C-9 BV2F ARENA (R-C9-345/347/348) -- the full painted barrow_v2 site (bv2f_pilot.gd on site_ph3, inherited unchanged:
## the same level, paint, camera -- ortho, pitch 52.95354, yaw 47 -- light, water, heather and snow) HOSTING the KC2
## wave fight (scripts/arena/arena_mode.gd). A THIN SCENE THAT EXTENDS THE WALK: scenes/bv2f_pilot_painted.tscn is not
## touched and its default behaviour is unchanged; this scene (scenes/bv2f_arena.tscn) differs only by
##   * the site pinned to site_ph3 (the arena's coordinates are that level's),
##   * no 3D knight (skip_character): the hero is the KC2 warlord, driven by the KC2 controls,
##   * the walk's own HUD hidden and its keys (R/H/N/...) handed to the fight.


func _init() -> void:
	# the arena is laid out on site_ph3's level: pin it whatever BV2F_PILOT says
	pilot_set = "site_ph3"
	PILOT_PX = PILOT_WINDOWS["site_ph3"]
	PILOT_REL = "../bv2f/%s/painted/" % pilot_set
	PILOT_MANIFEST = "res://data/bv2f/%s/painted/manifest.json" % pilot_set
	PILOT_LEVEL_DIR = "res://data/bv2f/%s/level/" % pilot_set
	BV2F_DATA = PILOT_LEVEL_DIR


var arena: Node3D = null


func _ready() -> void:
	await super._ready()
	set_hud_visible(false)
	# R-C9-353 (Matt: the load "stays ... in the bottom-right corner ... where all you see is the lack of map"): the
	# pilot's shader warm-up ends parked on the LAST view of its grid (the window's far corner), and the fight's
	# session then loads for seconds in front of it. So: the camera goes to the warlord's start NOW, under a plain
	# "loading the fight" card, and two frames are presented before the session opens.
	var j: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/arena/barrow_arena.json"))
	if typeof(j) == TYPE_DICTIONARY:
		var t: Array = (j as Dictionary)["fight_centre_sim"]
		set_process(false)
		look_at_world(aim_for(uv_to_world(float(t[0]), -float(t[1]), floor_y_at(float(t[0]), -float(t[1])))))
	var card := CanvasLayer.new()
	card.layer = 120
	var lb := Label.new()
	lb.text = "Loading the fight..."
	lb.add_theme_font_size_override("font_size", 28)
	lb.add_theme_color_override("font_color", Color(1, 0.93, 0.8))
	lb.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	lb.set_anchors_preset(Control.PRESET_CENTER)
	lb.position = Vector2(-120, -20)
	card.add_child(lb)
	add_child(card)
	await get_tree().process_frame
	await get_tree().process_frame
	arena = load("res://scripts/arena/arena_mode.gd").new()
	arena.name = "Arena"
	add_child(arena)
	arena.setup(self)
	card.queue_free()
	print("[bv2f_arena] site %s, arena %s" % [pilot_set, "up" if arena.fatal == "" else "REFUSED: " + String(arena.fatal)])


func _unhandled_input(e: InputEvent) -> void:
	if arena != null:
		arena.handle_input(e)


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST and arena != null:
		arena._close_recording("window_closed")
