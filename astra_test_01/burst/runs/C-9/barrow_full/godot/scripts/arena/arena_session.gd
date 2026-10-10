extends "res://kc2/kc2_runtime/play/kc2play_session.gd"
## C-9 BV2F ARENA (R-C9-345/347/348) -- THE KC2 PLAY SESSION, UNMODIFIED, WITH THE SPAWN POINTS MOVED TO BARROW_V2.
##
## This is a VARIANT SESSION SCRIPT: it inherits kc2_runtime/play/kc2play_session.gd and changes nothing in it. The
## runtime (sim + play/driver layer) is referenced in place through the gitignored symlink res://kc2/kc2_runtime ->
## reincarnated-godot/kc2_runtime, and the pack is the pack of record (kc2rt_pack_of_record.gd), digest-gated by the
## runtime's own loader.
##
## The stock `open()` runs ... fight.bind_wire -> configure_arm_from_pack -> select_contact_solver ->
## `_bind_summons()` -> fight.play_open(151, 160). `_bind_summons` is a method of this object, called after bind_wire
## and before play_open, so overriding it (super first, unchanged) is the seat for the barrow fold:
##   (1) board.spawn_points p01..p06 := the barrow_v2 anchors (data/arena/barrow_arena.json), in the KC2 frame;
##       the monster-to-point mapping is the data's, untouched (the board still rolls `wave|point` keys);
##   (2) the six crucible floor-hazard pools are DROPPED (arena.pools := []: the driver's D-LIFT pool tick then finds
##       none); the debug mouths go (aprons are already off under the graded rules, DR-11);
##   (3) the arena's player ring is opened to an unbounded square: the player's real bound is barrow_v2's own walk
##       colliders (the view moves him through physics, see arena_mode.gd), and the sim's tick-boundary check then
##       never disagrees with them.
## Under the arm PLAY runs (M0, GRADED_RULES) the arena fold is OFF (no wall, no avoidance pools) -- measured, and
## asserted below -- so nothing else in the sim reads the anchors' geometry.

const ARENA_JSON := "res://data/arena/barrow_arena.json"
const OPEN_RING_M := 500.0

var arena_cfg: Dictionary = {}
var fold: Dictionary = {}
var fold_ok: bool = false


func open(pack_dir: String, pack_digest: String, geom_path: String,
		seed: int, zoom: String, aprons: bool) -> bool:
	if super.open(pack_dir, pack_digest, geom_path, seed, zoom, aprons):
		return true
	# The pinned parent configures the graded arm, then requests the Mac native
	# solver before _bind_summons/play_open. Web and Windows x64 cannot load it. Resume
	# ONLY that specific platform-unavailable stop, choosing the runtime's exact
	# GDScript reference via its public switch. All earlier boot gates still bind;
	# no sealed source, graded configuration, or oracle refusal rule is changed.
	var platform := "%s.%s" % [OS.get_name(), Engine.get_architecture_name()]
	var portable := OS.has_feature("web") or platform == "Windows.x86_64"
	if not portable or fight == null:
		return false
	if not load_error.begins_with("PLAY-CONTACT-SOLVER: ORACLE:") \
			or not ("no native contact library is built for " + platform + " (") in load_error:
		return false
	if not fight.select_contact_solver("gdscript"):
		return false
	fight.contact_solver_note = "Barrow %s: explicitly selected the exact GDScript reference solver; Mac native library unavailable" % platform
	fight.last_error = ""
	load_error = ""
	fight.play_driver = driver
	_bind_summons()
	fight.play_open(WAVE_LO, WAVE_HI, MAX_TICKS)
	open_ok = true
	print("[arena] platform solver: " + fight.contact_solver_note)
	return true


func _bind_summons() -> void:
	super._bind_summons()
	fold = _barrow_fold()
	fold_ok = bool(fold.get("applied", false))
	if not fold_ok:
		push_error("[arena] BARROW FOLD REFUSED: " + String(fold.get("error", "?")))


func _barrow_fold() -> Dictionary:
	var out := {"applied": false}
	var j: Variant = JSON.parse_string(FileAccess.get_file_as_string(ARENA_JSON)) if FileAccess.file_exists(ARENA_JSON) else null
	if typeof(j) != TYPE_DICTIONARY:
		out["error"] = "no %s" % ARENA_JSON
		return out
	arena_cfg = j
	var T := Vector2(float(arena_cfg["fight_centre_sim"][0]), float(arena_cfg["fight_centre_sim"][1]))
	# ---- the arm's arena fold must be OFF, or the sim would read the anchors' geometry for a wall / pools ----
	if fight.walls_armed or fight.arena_avoidance:
		out["error"] = "the arm's arena fold is ARMED (walls %s, avoidance %s): the barrow anchors would move a wall" % [
			str(fight.walls_armed), str(fight.arena_avoidance)]
		return out
	# ---- (1) the spawn points ----
	var was: Dictionary = (board.spawn_points as Dictionary).duplicate(true)
	var anchors: Dictionary = arena_cfg["anchors"]
	var moved := {}
	for pid_any in was.keys():
		var pid := String(pid_any)
		if not anchors.has(pid):
			out["error"] = "barrow_arena.json has no anchor for %s" % pid
			return out
		var a: Dictionary = anchors[pid]
		var s := Vector2(float(a["sim"][0]), float(a["sim"][1])) - T
		board.spawn_points[pid] = {"x": s.x, "y": s.y}
		moved[pid] = {"kc2_was": [float(was[pid]["x"]), float(was[pid]["y"])], "kc2_now": [s.x, s.y],
			"barrow_sim": a["sim"], "feature": a.get("feature", "")}
	if anchors.size() != was.size():
		out["error"] = "barrow_arena.json names %d anchors, the board has %d" % [anchors.size(), was.size()]
		return out
	board.spawn_points_source = "barrow_v2 (R-C9-348): data/arena/barrow_arena.json, KC2 frame = barrow sim - %s" % str(T)
	# ---- (2) the hazards ----
	var n_pools := (arena.pools as Array).size()
	arena.pools = []
	var n_mouths := (arena.mouths as Array).size()
	arena.mouths = []
	# ---- (3) the player's ring: open (barrow_v2's colliders bound him) ----
	var r := OPEN_RING_M
	arena.ring = PackedVector2Array([Vector2(-r, -r), Vector2(r, -r), Vector2(r, r), Vector2(-r, r)])
	arena.obstructions = []
	arena.unwalked_spans = []
	out.merge({"applied": true, "fight_centre_sim": [T.x, T.y], "spawn_points": moved,
		"pools_dropped": n_pools, "mouths_dropped": n_mouths, "aprons_on": fight.aprons_on,
		"walls_armed": fight.walls_armed, "arena_avoidance": fight.arena_avoidance,
		"player_ring": "open square +-%d m (barrow_v2 walk colliders bound the player)" % int(r)}, true)
	return out


func header(feel_only: bool) -> Dictionary:
	var h: Dictionary = super.header(feel_only)
	h["barrow_arena"] = fold
	h["not_the_kc2_test"] = "R-C9-345/347/348: a FUN variant hosted in barrow_v2; no referent/oracle/seal/JOIN parity is claimed"
	return h
