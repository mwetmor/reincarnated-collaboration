extends SceneTree
## C-9 T10-2 step 4 -- THE FILM FOR MATT'S LOOK: him, armed as installed, in the assembled Barrow.
##
## Run under Movie Maker (tools/film_painted.sh): the engine steps at a fixed 24 fps and writes
## every frame straight into ONE movie file (no frame dump), which the shell script encodes to MP4
## and deletes. The snow's clock and the heather's wind run on the fixed step: deterministic.
##
##   he walks the TARN PATH up to the ring (the frozen tarn on his left)
##   crosses the arena at a run
##   walks THROUGH ring_m55's painted shadow (a tall stone: the sun darkens him in it; his own
##     shadow on the painting merges with the painted one and does not stack on it)
##   walks PAST THE DOOR along the front of the cutting
##   and SLASHES beside ring_p55
##
## Every waypoint is checked against the painted light map as he passes: the report says where
## the shadow was and what the light at his feet read.

const SETTLE_MIN := 72               # at least this many frames of settling (trimmed by film_painted.sh)
var settle_end := -1                 # the frame the action starts: the trim, printed in the report
const DT := 1.0 / 24.0
const HOLD_IN := 12
const HOLD_OUT := 30
const SHADOW_STONE := "ring_m55"
const SLASH_STONE := "ring_p55"

var scene
var k
var frame := 0
var legs: Array = []
var leg_i := 0
var wp_i := 0
var phase := "settle"
var t_phase := 0
var report := {"legs": [], "lit_at_feet": []}
var shadow_frames := 0
var best_d := INF
var stall := 0
var in_shadow_min := 1.0


func _initialize() -> void:
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)


func _lit_at(uv: Vector2) -> float:
	var lit: Texture2D = scene._paint_tex.get("lit")
	var img := lit.get_image()
	var x := (uv.x - PaintedWorld.U0) * PaintedWorld.PPM * 0.5
	var y := (PaintedWorld.V1 - uv.y) * PaintedWorld.PPM * sin(deg_to_rad(PaintedWorld.PITCH_DEG)) * 0.5
	if x < 0 or y < 0 or x >= img.get_width() or y >= img.get_height():
		return -1.0
	return img.get_pixel(int(x), int(y)).r


func _shadow_route(id: String) -> Array:
	"""Three points through the stone's cast shadow, found in the painted light map: in at the
	shadow's far end, along it to 0.45 m past its centroid toward the stone, out to the north.

	SEARCHED ONLY DOWN-SUN OF THE STONE, 0.5-2.6 m out along +u, -1.2..+0.6 m in v (the sun's ground
	direction is (0.98, -0.21) in (u, v)). The first search took every dark cell within 3 m, and
	the ground BEHIND a 2.7 m stone is the stone on screen -- its own shadow side, 164 px tall --
	so the centroid slid onto the stone and the route ran into its collider."""
	var base: Vector2 = scene.world_to_uv((scene.nodes[id] as Node3D).global_position)
	var acc := Vector2.ZERO
	var n := 0
	for j in 19:
		for i in 22:
			var p := base + Vector2(0.5 + 0.1 * i, -1.2 + 0.1 * j)
			if _lit_at(p) < 0.2:
				acc += p
				n += 1
	var c := acc / maxf(float(n), 1.0)
	report["shadow"] = {"stone": id, "stone_base_uv": [snappedf(base.x, 0.01), snappedf(base.y, 0.01)],
						"shadow_centroid_uv": [snappedf(c.x, 0.01), snappedf(c.y, 0.01)], "shadow_cells_0.1m": n}
	# ALONG IT, not across: in from its far (down-sun) end, toward the stone, then out north past
	# the stone's sunlit side. Across its 0.7 m width he was in it for 0.46 s (the first film);
	# along its length he stays in it long enough to be seen darkened
	var sdir := Vector2(0.978, -0.208)
	var deep := c - sdir * 0.45
	return [c + sdir * 1.0, deep, deep + Vector2(0.15, 1.2)]


func _setup() -> void:
	k = scene.knight
	scene.set_hud_visible(false)
	scene.set_crucible_visible(false)
	var shadow: Array = _shadow_route(SHADOW_STONE)
	var sb: Vector2 = scene.world_to_uv((scene.nodes[SLASH_STONE] as Node3D).global_position)
	var slash_at := sb + Vector2(-1.2, -0.35)
	report["slash"] = {"stone": SLASH_STONE, "stone_uv": [snappedf(sb.x, 0.01), snappedf(sb.y, 0.01)],
					   "at_uv": [snappedf(slash_at.x, 0.01), snappedf(slash_at.y, 0.01)]}
	# [name, run, waypoints]
	legs = [
		["the tarn path", false, [Vector2(-1.0, -10.0), Vector2(-0.2, -7.0)]],
		["across the arena", true, [Vector2(-2.5, -1.0), shadow[0] + Vector2(0.6, -0.9)]],
		["through the painted shadow", false, [shadow[0], shadow[1], shadow[2]]],
		["past the door", false, [Vector2(-2.2, 8.2), Vector2(0.0, 8.35), Vector2(2.4, 8.2)]],
		["to the stone", false, [slash_at]],
	]
	scene.place_knight(-1.9, -12.6, "N")
	report["start_uv"] = [-1.9, -12.6]


func _process(_delta: float) -> bool:
	frame += 1
	if settle_end < 0:
		if frame >= SETTLE_MIN and scene.ready_done:
			settle_end = frame
			report["trim_frames"] = settle_end
			_setup()
		return false
	t_phase += 1
	var here: Vector2 = scene.knight_uv()
	var lit := _lit_at(here)
	if frame % 6 == 0:
		report["lit_at_feet"].append([frame - settle_end, snappedf(here.x, 0.01), snappedf(here.y, 0.01), snappedf(lit, 0.02)])
	if phase == "settle":
		phase = "hold_in"
		t_phase = 0
	if phase == "hold_in":
		k.drive_dir(Vector2.ZERO, false, DT)
		if t_phase >= HOLD_IN:
			phase = "walk"
			t_phase = 0
			report["legs"].append({"leg": legs[0][0], "from_frame": frame - settle_end})
		return false
	if phase == "walk":
		var leg: Array = legs[leg_i]
		var wps: Array = leg[2]
		var target: Vector2 = wps[wp_i]
		if leg_i == 2 and lit < 0.3:
			shadow_frames += 1
			in_shadow_min = minf(in_shadow_min, lit)
		# A WAYPOINT IS REACHED, OR IT IS PASSED BY: within 0.22 m walking (0.35 running), or no
		# nearer for a second -- logged, so a waypoint he could not reach is in the report, not hidden
		var d := here.distance_to(target)
		if d < best_d - 0.005:
			best_d = d
			stall = 0
		else:
			stall += 1
		if d < (0.35 if leg[1] else 0.22) or stall > 24:
			if stall > 24:
				report.get_or_add("waypoints_passed_by", []).append({"leg": leg[0], "target": [snappedf(target.x, 0.01), snappedf(target.y, 0.01)],
					"closest_m": snappedf(best_d, 0.01)})
			best_d = INF
			stall = 0
			wp_i += 1
			if wp_i >= wps.size():
				report["legs"][-1]["to_frame"] = frame - settle_end
				report["legs"][-1]["end_uv"] = [snappedf(here.x, 0.01), snappedf(here.y, 0.01)]
				wp_i = 0
				leg_i += 1
				if leg_i >= legs.size():
					phase = "face"
					t_phase = 0
					return false
				report["legs"].append({"leg": legs[leg_i][0], "from_frame": frame - settle_end})
				return false
			target = wps[wp_i]
		k.drive_dir(scene.canvas_dir_uv(here, target), bool(leg[1]), DT)
		if t_phase > 24 * 40:
			print("[film] HALT: stuck on leg %s at %s %s" % [leg[0], str(here), JSON.stringify(report)])
			quit(4)
			return true
		return false
	if phase == "face":
		# a step's worth toward the stone, to turn him to it; then the slash
		var sb: Vector2 = scene.world_to_uv((scene.nodes[SLASH_STONE] as Node3D).global_position)
		if t_phase < 3:
			k.drive_dir(scene.canvas_dir_uv(here, sb), false, DT)
		else:
			k.drive_dir(Vector2.ZERO, false, DT)
		if t_phase == 8:
			report["slash"]["fired"] = k.try_attack()
			report["slash"]["frame"] = frame - settle_end
			phase = "slash"
			t_phase = 0
		return false
	if phase == "slash":
		k.drive_dir(Vector2.ZERO, false, DT)
		if t_phase > 24 + HOLD_OUT and not k.attacking():
			report["through_the_shadow"] = {"frames_with_lit_under_0.3": shadow_frames,
				"seconds": snappedf(float(shadow_frames) / 24.0, 0.01), "least_lit_at_his_feet": snappedf(in_shadow_min, 0.02)}
			report["frames_after_settle"] = frame - settle_end
			report["seconds"] = snappedf(float(frame - settle_end) / 24.0, 0.01)
			print("[film] ", JSON.stringify(report))
			return true
		return false
	return false
