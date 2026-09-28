extends SceneTree
# C-9 R-C9-61: does each skin FACE THE WAY IT IS TRAVELLING?
#
# Matt, on the live route: "With the Meshy version, E and W are inverted."
#
# My earlier facing check compared all three skins at ONE direction (east), saw them
# agree, and concluded the convention was fine. Agreement at a single direction cannot
# distinguish "all correct" from "all mirrored" from "two wrong in the same way" -- and
# an E/W swap with N/S intact is precisely a sign error, which a one-direction check is
# blind to by construction. So this walks every direction and captures every skin.
#
# Needs a real window (no --headless): the dummy renderer returns null textures.
#
# Writes user://facing/<skin>_<dir>.png, a per-skin contact sheet, and
# user://facing_probe.json recording which direction the Keeper reported for each
# input combination -- so a disagreement between "what I pressed" and "what the body
# thinks it is doing" shows up as itself rather than as a facing bug.

const OUT := "user://facing"
const SETTLE := 22
const INSET_SRC := Vector2i(260, 300)
const ZOOM := 3

# The eight inputs, and the direction each is EXPECTED to produce. The expectation is
# recorded so the capture can be read without re-deriving it, and so a mismatch between
# input and reported facing is visible.
const WALKS := [
	{"dir": "E", "keys": ["move_right"]},
	{"dir": "W", "keys": ["move_left"]},
	{"dir": "N", "keys": ["move_up"]},
	{"dir": "S", "keys": ["move_down"]},
	{"dir": "NE", "keys": ["move_right", "move_up"]},
	{"dir": "NW", "keys": ["move_left", "move_up"]},
	{"dir": "SE", "keys": ["move_right", "move_down"]},
	{"dir": "SW", "keys": ["move_left", "move_down"]},
]

# What each direction must look like, in camera terms, taken from the KEEPER -- the
# shipped character, and therefore the definition of correct. screen_x > 0 is "faces
# screen-right"; toward_camera > 0 is "faces out of the screen".
#   Keeper E faces right, W faces left, N shows her back, S shows her face.
const EXPECT := {
	"E":  {"sx": 1, "tc": 0}, "W":  {"sx": -1, "tc": 0},
	"N":  {"sx": 0, "tc": -1}, "S": {"sx": 0, "tc": 1},
	"NE": {"sx": 1, "tc": -1}, "NW": {"sx": -1, "tc": -1},
	"SE": {"sx": 1, "tc": 1},  "SW": {"sx": -1, "tc": 1},
}
const MIN_COMPONENT := 0.18      # below this the axis is "not strongly either way"
const MAX_HAFT_DEG := 20.0       # the haft must read as upright
const MAX_GRIP_MISS_PX := 15.0   # ...and pass through the fist, not beside it
const MIN_HEAD_ABOVE_PX := 40.0  # ...head end uppermost, not inverted

var fails := 0
var report := {"note": "C-9 R-C9-61 facing + weapon probe", "skins": []}


func _check(ok: bool, what: String) -> void:
	if not ok:
		fails += 1
	print(("    PASS  " if ok else "    FAIL  ") + what)


func _initialize():
	DirAccess.make_dir_recursive_absolute(OUT)
	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	var keeper = scene.find_child("Keeper", true, false)
	var skin = keeper.get_node_or_null(^"CharacterSkin")
	if skin == null:
		print("FAIL: no CharacterSkin")
		quit(1)
		return
	for i in SETTLE:
		await physics_frame
	var home: Vector2 = keeper.global_position

	for idx in 3:
		await _select(skin, idx)
		var sname: String = String(skin.call("skin_name"))
		var slug := _slug(sname)
		var rows := []
		var shots := []
		for w in WALKS:
			keeper.global_position = home
			for k in w.keys:
				Input.action_press(k)
			for i in SETTLE:
				await physics_frame
				await process_frame
			var got := String(keeper.facing)
			var cell := _cell(keeper, idx)
			if cell == null:
				print("    (no cell for %s %s)" % [sname, w.dir])
				continue
			var shown := _on_dark(cell)
			shown.save_png("%s/%s_%s.png" % [OUT, slug, w.dir])
			shots.append(shown)
			var row := {"pressed": w.dir, "keeper_facing": got, "agrees": got == w.dir}
			print("  %-26s pressed %-3s  keeper says %-3s  %s"
				% [sname, w.dir, got, "ok" if got == w.dir else "MISMATCH"])
			_check(got == w.dir, "%s: the body reports the direction pressed" % w.dir)
			if idx == 2:
				var k3 = keeper.get_node_or_null(^"Knight3D")
				var fc: Dictionary = k3.call("facing_check")
				var wc: Dictionary = k3.call("weapon_check")
				row["facing"] = fc
				row["weapon"] = wc
				var e: Dictionary = EXPECT[w.dir]
				for axis in [["sx", "screen_x", "faces screen-%s"],
							 ["tc", "toward_camera", "faces %s the camera"]]:
					var want: int = int(e[axis[0]])
					var got_v: float = float(fc.get(axis[1], 0.0))
					if want == 0:
						continue
					var label: String = (axis[2] % ("right" if want > 0 else "left")) \
						if axis[0] == "sx" else (axis[2] % ("toward" if want > 0 else "away from"))
					_check(sign(got_v) == want and absf(got_v) >= MIN_COMPONENT,
						"%s: %s (%s = %+.3f)" % [w.dir, label, axis[1], got_v])
				if bool(wc.get("ok", false)):
					_check(float(wc["haft_deg_from_vertical"]) <= MAX_HAFT_DEG,
						"%s: haft is upright (%.1f deg from vertical, max %.0f)"
						% [w.dir, wc["haft_deg_from_vertical"], MAX_HAFT_DEG])
					_check(float(wc["grip_miss_px"]) <= MAX_GRIP_MISS_PX,
						"%s: haft passes through the fist (%.1f px off, max %.0f)"
						% [w.dir, wc["grip_miss_px"], MAX_GRIP_MISS_PX])
					_check(float(wc["head_above_fist_px"]) >= MIN_HEAD_ABOVE_PX,
						"%s: the axe HEAD is up (%.0f px above the fist, min %.0f)"
						% [w.dir, wc["head_above_fist_px"], MIN_HEAD_ABOVE_PX])
			rows.append(row)
			for k in w.keys:
				Input.action_release(k)
			for i in 4:
				await physics_frame
		_sheet(shots, "%s/SHEET_%s.png" % [OUT, slug])
		report["skins"].append({"skin": sname, "slug": slug, "directions": rows})

	await _select(skin, 0)
	report["ends_on"] = String(skin.call("skin_name"))
	var f := FileAccess.open("user://facing_probe.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	report["fails"] = fails
	print("sheets in ", ProjectSettings.globalize_path(OUT), "   ends on ", report["ends_on"])
	print("=== facing + weapon probe: %s (%d failures) ===" % ["PASS" if fails == 0 else "FAIL", fails])
	quit(1 if fails > 0 else 0)


func _slug(s: String) -> String:
	var out := ""
	for c in s.to_lower():
		out += c if (c >= "a" and c <= "z") or (c >= "0" and c <= "9") else ""
	return out


func _select(skin, idx: int) -> void:
	# Through the KEY, not the method -- the same reason probe_chartest.gd does: the
	# one defect this test family has actually caught lived in the input path.
	for i in 8:
		var n: String = String(skin.call("skin_name"))
		if (idx == 0 and n.begins_with("Keeper")) \
			or (idx == 1 and n.find("sprites") >= 0) \
			or (idx == 2 and n.find("3D") >= 0):
			return
		var ev := InputEventKey.new()
		ev.physical_keycode = KEY_K
		ev.keycode = KEY_K
		ev.pressed = true
		Input.parse_input_event(ev)
		await process_frame
		var up := InputEventKey.new()
		up.physical_keycode = KEY_K
		up.keycode = KEY_K
		up.pressed = false
		Input.parse_input_event(up)
		await process_frame


func _cell(keeper, idx: int) -> Image:
	"""The character's OWN cell, not a crop of the game view.

	The first version cropped the viewport around the player's screen position,
	computed through get_canvas_transform(). It produced eight handsome photographs
	of scenery with no character in them -- the crop ran, saved a file, and answered
	a question about the terrain. Every skin already renders into a clean 512x512
	cell with a transparent background: the 3D skin IS a SubViewport, and the two
	sprite skins have the frame texture in hand. Reading that is both exact and the
	same image the scene composites, so there is nothing left to mis-locate."""
	if idx == 2:
		var k3 = keeper.get_node_or_null(^"Knight3D")
		if k3 != null:
			var vp: SubViewport = k3.call("viewport")
			if vp != null:
				return vp.get_texture().get_image()
		return null
	var spr: AnimatedSprite2D = keeper.get_node_or_null(
		^"AnimatedSprite2D" if idx == 0 else ^"KnightSprite")
	if spr == null or spr.sprite_frames == null:
		return null
	if not spr.sprite_frames.has_animation(spr.animation):
		return null
	var tex: Texture2D = spr.sprite_frames.get_frame_texture(spr.animation, spr.frame)
	return null if tex == null else tex.get_image()


func _on_dark(img: Image) -> Image:
	# Composite onto a flat ground so a transparent cell is reviewable by eye, and
	# scale down: eight 512 cells side by side is 4096 px of contact sheet.
	var out := Image.create(img.get_width(), img.get_height(), false, Image.FORMAT_RGBA8)
	out.fill(Color(0.10, 0.11, 0.14))
	var src := img
	if src.get_format() != Image.FORMAT_RGBA8:
		src.convert(Image.FORMAT_RGBA8)
	out.blend_rect(src, Rect2i(Vector2i.ZERO, src.get_size()), Vector2i.ZERO)
	out.resize(320, 320, Image.INTERPOLATE_LANCZOS)
	return out


func _sheet(shots: Array, path: String) -> void:
	if shots.is_empty():
		return
	var w: int = shots[0].get_width()
	var h: int = shots[0].get_height()
	var sheet := Image.create(w * shots.size(), h, false, Image.FORMAT_RGBA8)
	sheet.fill(Color(0.06, 0.06, 0.08))
	for i in shots.size():
		sheet.blit_rect(shots[i], Rect2i(0, 0, w, h), Vector2i(i * w, 0))
	sheet.save_png(path)
