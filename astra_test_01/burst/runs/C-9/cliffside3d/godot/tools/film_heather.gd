extends SceneTree
# C-9 T10-1d -- HIM, WADING THROUGH A HEATHER PATCH IN THE WIND.
#
# Run under Movie Maker (tools/film_heather.sh): the engine steps at a fixed 24 fps and writes
# every frame straight into ONE movie file -- no frame dump -- which the shell script encodes to
# MP4 and deletes. The heather's wind and push run on the snow's clock, and the snow's clock
# runs on the fixed step, so the film is deterministic.
#
#   0-1.5 s  the patch in the wind with NOBODY in it -- the sway measured clean (he is hidden)
#   1.5-2 s  he stands at the patch's edge
#   2-8 s    he wades through it: stems bend away from his stride and flatten
#   8-10 s   he stands on the far side; the track stays parted
#   10-13 s  TIME-LAPSE x20 (labelled): the snow's clock runs 58 s in 3 s, the trail refills,
#            and the stems come back up with it
#
# The patch is chosen, not placed: the heather clump with the most heather within 1 m, near
# the clearing, and the crossing direction that passes the most heather and no collider.

const SETTLE := 80
const T_EMPTY := 36
const T_WIND := 48
const T_WADE_MAX := 240
var wade_end := -1
const T_HOLD := 48
const T_LAPSE := 72
const LAPSE_S_PER_FRAME := 0.8
var scene
var k
var frame := 0
var start := Vector2.ZERO
var finish := Vector2.ZERO
var centre := Vector2.ZERO
var label: Label
var report := {}


func _initialize() -> void:
	scene = load("res://scenes/barrow.tscn").instantiate()
	root.add_child(scene)


func _process(_delta: float) -> bool:
	frame += 1
	if frame < SETTLE:
		return false
	if frame == SETTLE:
		_setup()
		return false
	var f := frame - SETTLE
	if f < T_EMPTY:
		k.visible = false
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
	elif f < T_WIND:
		k.visible = true
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
	elif wade_end < 0:
		# HE WADES UNTIL HE IS THROUGH (armed walk through heather is ~0.5 m/s, measured; a
		# fixed 4 s left him mid-patch), capped at 10 s
		var p := Vector2(k.global_position.x, k.global_position.z)
		if p.distance_to(finish) > 0.25 and f < T_WIND + T_WADE_MAX:
			k.drive_dir(_canvas_dir_to(finish), false, 1.0 / 24.0)
		else:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
			wade_end = f
			report["wade_s"] = snappedf(float(f - T_WIND) / 24.0, 0.01)
	elif f < wade_end + T_HOLD:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		if f == wade_end + T_HOLD - 1:
			report["press_along_path_after_wade"] = _press_along_path()
	elif f < wade_end + T_HOLD + T_LAPSE:
		k.drive_dir(Vector2.ZERO, false, 1.0 / 24.0)
		scene.snow.advance_clock(LAPSE_S_PER_FRAME)
		label.visible = true
		label.text = "time-lapse x20   +%d s" % int(float(f - wade_end - T_HOLD) * (LAPSE_S_PER_FRAME + 1.0 / 24.0))
	else:
		report["press_along_path_after_timelapse"] = _press_along_path()
		report["ended_at_xz"] = [snappedf(k.global_position.x, 0.01), snappedf(k.global_position.z, 0.01)]
		report["frames"] = {"empty": [0, T_EMPTY], "stand": [T_EMPTY, T_WIND], "wade": [T_WIND, wade_end],
							"hold": [wade_end, wade_end + T_HOLD], "timelapse": [wade_end + T_HOLD, wade_end + T_HOLD + T_LAPSE]}
		print("[film] ", JSON.stringify(report))
		return true
	return false


func _press_along_path() -> Dictionary:
	"""THE PUSH, READ AT ITS SOURCE: the press the heather's vertex shader sees at every clump
	within 0.6 m of his line -- max of the trail at the clump and 0.85x at four taps 0.26 m out,
	the shader's own rule -- and the tip travel that gives (push_amp x press)."""
	var ps := []
	var reach := 0.26
	for q in _heather_points():
		var qv: Vector2 = q
		if Geometry2D.get_closest_point_to_segment(qv, start, finish).distance_to(qv) > 0.6:
			continue
		var pc: float = scene.snow.press_at(qv)
		var arm := maxf(maxf(scene.snow.press_at(qv + Vector2(reach, 0)), scene.snow.press_at(qv - Vector2(reach, 0))),
						maxf(scene.snow.press_at(qv + Vector2(0, reach)), scene.snow.press_at(qv - Vector2(0, reach))))
		ps.append(maxf(pc, 0.85 * arm))
	ps.sort()
	if ps.is_empty():
		return {"clumps": 0}
	var pushed := ps.filter(func(x): return x > 0.1).size()
	return {"clumps": ps.size(), "pushed_gt_0.1": pushed,
			"press_p50": snappedf(ps[ps.size() / 2], 0.01), "press_max": snappedf(ps[-1], 0.01),
			"tip_travel_cm_at_max": snappedf(ps[-1] * 26.0, 0.1)}


func _setup() -> void:
	k = scene.knight
	k.set_gear_stack(k.gear_stack_count() - 1)
	scene.set_hud_visible(false)
	if scene.has_method("set_heather_wind"):
		scene.set_heather_wind(true)
		scene.set_heather_push(true)
	_choose_patch()
	scene.place_knight(start.x, start.y, "NE")
	scene.park_camera(Vector3(centre.x, 0.35, centre.y), 1.9)
	var layer := CanvasLayer.new()
	root.add_child(layer)
	label = Label.new()
	label.position = Vector2(24, 20)
	label.add_theme_font_size_override("font_size", 22)
	label.add_theme_color_override("font_color", Color(0.12, 0.09, 0.07))
	label.visible = false
	layer.add_child(label)
	report["patch_centre_xz"] = [snappedf(centre.x, 0.01), snappedf(centre.y, 0.01)]
	report["from_xz"] = [snappedf(start.x, 0.01), snappedf(start.y, 0.01)]
	report["to_xz"] = [snappedf(finish.x, 0.01), snappedf(finish.y, 0.01)]


func _heather_points() -> Array:
	var out := []
	for rt in [scene._props_root, scene._density_root]:
		for c in rt.get_children():
			var rec: Dictionary = scene._place_report.get(String(c.name), {})
			if String(rec.get("asset", "")) == "heather":
				out.append(Vector2((c as Node3D).global_position.x, (c as Node3D).global_position.z))
	return out


func _choose_patch() -> void:
	"""The crossing he can WALK that passes the most heather: every heather clump within 9 m
	of the clearing and off the mound is a candidate centre, crossed in 16 directions over
	3.0 m; a crossing must clear every collider by his capsule and a margin (0.42 m) and stay
	off the ice. The painted heather hugs its rocks -- by design, it is what the painting
	does -- so the densest clumps have no straight way through; the most heather ON a clear
	line is the honest pick."""
	var hp := _heather_points()
	var cols: Array = scene._collider_list()
	var cc: Vector2 = scene.COMBAT_C
	var best_hits := 0
	var n_cands := 0
	for p in hp:
		var c: Vector2 = p
		if c.distance_to(cc) > 9.0 or c.distance_to(scene.MOUND_XZ) < scene.MOUND_R + 0.6:
			continue
		n_cands += 1
		for i in 16:
			var a := TAU * float(i) / 16.0
			var d := Vector2(cos(a), sin(a))
			var s0 := c - d * 1.5
			var s1 := c + d * 1.5
			var ok := true
			for col in cols:
				if Geometry2D.get_closest_point_to_segment(col["p"], s0, s1).distance_to(col["p"]) < float(col["r"]) + 0.42:
					ok = false
					break
			if not ok or scene._splat_w_fast(s0.x, s0.y)[4] > 0.2 or scene._splat_w_fast(s1.x, s1.y)[4] > 0.2:
				continue
			var hits := 0
			for q in hp:
				if Geometry2D.get_closest_point_to_segment(q, s0, s1).distance_to(q) < 0.6:
					hits += 1
			if hits > best_hits:
				best_hits = hits
				start = s0 - d * 0.6
				finish = s1 + d * 0.6
				centre = c
	report["candidates"] = n_cands
	report["heather_along_the_crossing"] = best_hits
	if best_hits == 0:
		report["_"] = "no walkable crossing found"


func _canvas_dir_to(target: Vector2) -> Vector2:
	"""As tools/shot_barrow.gd: a ground target back through the camera law into the canvas
	direction knight.gd drives on."""
	var p: Vector3 = k.global_position
	var d := Vector2(target.x - p.x, target.y - p.z)
	if d.length() < 1e-5:
		return Vector2.ZERO
	var r := Vector2(scene.right.x, scene.right.z)
	var lz := Vector2(sin(deg_to_rad(47.0)), cos(deg_to_rad(47.0)))
	var det: float = r.x * lz.y - r.y * lz.x
	if absf(det) < 1e-9:
		return Vector2(0.62, -1.0).normalized()
	var a: float = (d.x * lz.y - d.y * lz.x) / det
	var b: float = (r.x * d.y - r.y * d.x) / det
	return Vector2(a, b * sin(deg_to_rad(scene.PL_PITCH_DEG))).normalized()
