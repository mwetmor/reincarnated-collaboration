extends "res://scripts/arena/arena_body3d.gd"
## C-9 BV2F ARENA (R-C9-348) -- A DRESSED MONSTER in 3D: kc2_play/src/kc2p_monster.gd's behaviour on a billboard.
##
## Everything it shows comes from the snapshot, the event stream or the fight's own per-body state, READ ONLY
## (KP-264: nothing on a timer of its own) -- the same rules as KC2's 2D view:
##   position  the snapshot (x_m, y_m), lifted to the barrow ground under it
##   attack    `cast_start` -> the slot's state, release ON the tick; the windup only against the oracle's schedule
##   death     `death` -> the death clip, last frame held, then a fade
##   p05       the pack's `emerge` clip warped onto [spawn_t_s, emerge_until_t_s] (the rise out of the ground)
##   hit       a flash on the oracle's `hit`
##   loco      moved since the last tick -> run (walk / crawl), else idle; facing = the step's bearing, else the player

const Kc2RtQuant = preload("res://kc2/kc2_runtime/sim/kc2rt_quant.gd")

const DEATH_FADE_S := 0.6
const MOVE_EPS_M := 1e-4
const MELEE_WORDS: PackedStringArray = ["attack", "claw", "bite", "swipe", "impale", "gore", "butt", "peck",
	"charge", "taillash", "slash", "punch", "slam"]
const PROJ_WORDS: PackedStringArray = ["bolt", "hurl", "rift", "breath", "lob", "throw", "spit"]
const AREA_WORDS: PackedStringArray = ["area", "nova", "drain", "aura", "roar", "rift"]

var actor_id: int = 0
var record: String = ""
var radius_m: float = 0.62
var hp: float = 0.0
var hp_max: float = 1.0
var champion: bool = false
var label: String = ""
var released: bool = false
var stationary: bool = false
var emerging: bool = false
var pos_m: Vector2 = Vector2.ZERO
var tick_pos_m: Vector2 = Vector2.INF
var last_tick: int = -1
var moving: bool = false
var dying: bool = false
var gone_at_s: float = -1.0
var hold_ticks_left: int = 0
var ticks_per_s: float = 12.25
var true_height_m: float = 1.9
var slot_state_cache: Dictionary = {}
var session = null
var stationary_row: bool = false
var pred_certain: bool = false
var _body_cds: Dictionary = {}


func setup_monster(sess, a: Dictionary, entry: Dictionary) -> void:
	session = sess
	setup_body(String(entry["kit"]), float(entry.get("factor", 1.0)))
	actor_id = int(a["id"])
	record = String(a.get("record_path", ""))
	radius_m = float(a.get("body_radius_m", 0.62))
	champion = bool(a.get("is_hero", false))
	if a.get("name", null) != null:
		label = String(a["name"])
	ticks_per_s = float(sess.fight.ticks_per_s)
	stationary_row = float(sess.fight.roster.run_speed(record)) <= 0.0
	var m := J.kit_meta(kit)
	var hm: Variant = m.get("h_model_m", null)
	true_height_m = (float(hm) if hm != null else 1.9) * factor
	J.prefetch(kit, [_loco_state(false), _loco_state(true)])
	_build_ground_marks()
	play_loop(_loco_state(false))
	if record.contains("summon") and J.has_state(kit, "emerge"):
		play_oneshot("emerge")


func _loco_state(mv: bool) -> String:
	if mv:
		for s in ["run", "walk", "crawl"]:
			if J.has_state(kit, s):
				return s
	return "idle" if J.has_state(kit, "idle") else String((J.kit_meta(kit).get("states", {}) as Dictionary).keys()[0])


func state_for_slot(slot_key: String) -> String:
	if slot_state_cache.has(slot_key):
		return slot_state_cache[slot_key]
	var rel_states: Array = J.states_with_role(kit, "oneshot_release")
	var entry: Dictionary = {}
	for s_any in session.fight.roster.slots_for(record):
		if String((s_any as Dictionary).get("_slot_key", "")) == slot_key:
			entry = s_any
			break
	var skill_path := String(entry.get("skill", ""))
	if skill_path == "" and slot_key.contains("|"):
		skill_path = slot_key.get_slice("|", slot_key.get_slice_count("|") - 1)
	var skill := skill_path.get_file().get_basename().to_lower()
	var cls := String(entry.get("skill_class", "")).to_lower()
	if cls == "":
		var ec := String(entry.get("extent_carrier", "")).to_lower()
		if ec.contains("projectile"):
			cls = "projectile"
		elif ec.contains("radius") or bool(entry.get("is_telegraph", false)):
			cls = "radius"
		elif bool(entry.get("is_weapon_swing", false)):
			cls = "weapon"
		else:
			cls = cls_hint(skill_path)
	var pick := ""
	for st in rel_states:
		for tok in String(st).split("_"):
			if tok.length() < 4 or tok in ["attack", "cast"]:
				continue
			if skill.contains(tok):
				pick = String(st)
				break
		if pick != "":
			break
	if pick == "":
		var words: PackedStringArray = MELEE_WORDS
		if cls.contains("projectile"):
			words = PROJ_WORDS
		elif cls.contains("radius") or cls.contains("aura") or cls.contains("buff") or cls.contains("summon") \
				or cls.contains("nova") or (cls.contains("area") and not cls.contains("weapon")):
			words = AREA_WORDS
		pick = _first_named(rel_states, words)
	if pick == "":
		pick = _first_named(rel_states, MELEE_WORDS)
	if pick == "" and not rel_states.is_empty():
		pick = String(rel_states[0])
	slot_state_cache[slot_key] = pick
	return pick


static func _first_named(states: Array, words: PackedStringArray) -> String:
	for st in states:
		for w in words:
			if String(st).contains(w):
				return String(st)
	return ""


static func cls_hint(skill_path: String) -> String:
	var p := skill_path.to_lower()
	if p.contains("attackprojectile"):
		return "projectile"
	if p.contains("attackradius") or p.contains("buff") or p.contains("aura") or p.contains("summon"):
		return "radius"
	if p.contains("attackmelee") or p.contains("attackweapon"):
		return "weapon"
	return ""


func swing_after_s() -> float:
	var n: int = int(session.fight.swing_ticks_of(record))
	return float(n) / ticks_per_s if n > 0 else 1.0


func on_cast_start(slot_key: String, aim: Vector2) -> void:
	if dying:
		return
	var to := aim - pos_m
	if to.length() > 1e-6:
		dir = J.dir_of(to)
	var st := state_for_slot(slot_key)
	if st == "":
		return
	release_now(st, swing_after_s())


func on_hit() -> void:
	flash()


func on_death() -> void:
	if dying:
		return
	dying = true
	if J.has_state(kit, "death"):
		play_oneshot("death", true)
	gone_at_s = clock_s + (clip_T("death") if J.has_state(kit, "death") else 0.0) + DEATH_FADE_S


func faded_out() -> bool:
	return dying and clock_s >= gone_at_s


## One snapshot row + the body dict (read-only) + the player position (all in the KC2 frame).
func sync_actor(a: Dictionary, body: Dictionary, player_m: Vector2, wave_s: float, tick: int) -> void:
	hp = float(a.get("hp", 0.0))
	hp_max = maxf(1.0, float(a.get("hp_max", 1.0)))
	released = String(a.get("state", "")) == "ENGAGE"
	var p := Vector2(float(a["x_m"]), float(a["y_m"]))
	var moved := Vector2.ZERO
	if tick != last_tick:
		if tick_pos_m != Vector2.INF:
			moved = p - tick_pos_m
			moving = moved.length() > MOVE_EPS_M
		tick_pos_m = p
		last_tick = tick
	pos_m = p
	if dying:
		return
	stationary = bool(body.get("stationary", false)) or stationary_row
	_body_cds = body.get("slot_cooldowns", {})
	var te: Variant = body.get("emerge_until_t_s", null)
	emerging = te != null and wave_s < float(te)
	if emerging:
		if J.has_state(kit, "emerge"):
			var t0 := float(body.get("spawn_t_s", wave_s))
			if a_mode != "window" or a_state != "emerge":
				var lag := wave_s - t0
				play_window("emerge", clock_s - lag, clock_s - lag + (float(te) - t0))
		else:
			play_loop("idle" if J.has_state(kit, "idle") else _loco_state(false))
		return
	if a_mode == "window" and a_state == "emerge":
		a_mode = ""
	if stationary:
		moving = false
	if not stationary:
		if moving:
			if moved != Vector2.ZERO:
				dir = J.dir_of(moved)
		elif released:
			var to := player_m - pos_m
			if to.length() > 1e-3 and not busy():
				dir = J.dir_of(to)
	if windup_overdue(2.5 / ticks_per_s):
		abandon_windup()
	if busy():
		return
	# the oracle's own swing schedule (read-only), as kc2p_monster: (a) the PLAY law phi + j*n ...
	var phi := int(body.get("phi", -1))
	if body.get("ge_A", null) == null and phi >= 0 and released and not moving and bool(body.get("can_swing", true)):
		var n: int = int(session.fight.swing_ticks_of(record))
		var k: int = int(session.fight.run_tick)
		var d: float = float(session.fight._dist_to_player(body))
		if n > 0:
			var next_k: int = phi + n * int(ceil(float(k + 1 - phi) / float(n)))
			var sk0 := _predict_slot(next_k - int(session.fight._wave_start_tick), d)
			var st0 := state_for_slot(sk0) if sk0 != "" else ""
			var t_until0 := float(next_k - k) / ticks_per_s
			if st0 != "" and t_until0 <= rel_s(st0) + 1e-6:
				begin_windup(st0, t_until0, swing_after_s())
				return
	# ... (b) the engagement fold's `ge_A.swing_ready` while in Attack mode
	var A: Variant = body.get("ge_A", null)
	if A != null and released and not moving:
		var Ad: Dictionary = A
		if String(Ad.get("mode", "")) == "A" and Ad.get("S", null) != null:
			var k_now: int = int(session.fight.run_tick) - int(session.fight._wave_start_tick)
			var ready_k := int(Ad.get("swing_ready", -1))
			if ready_k > k_now:
				var sk := String((Ad["S"] as Dictionary).get("_slot_key", ""))
				var st := state_for_slot(sk)
				var t_until := float(ready_k - k_now) / ticks_per_s
				if st != "" and t_until <= rel_s(st) + 1e-6:
					begin_windup(st, t_until, swing_after_s())
					return
	play_loop(_loco_state(moving))


func _predict_slot(kw: int, d: float) -> String:
	var f = session.fight
	var cds: Dictionary = _body_cds
	for s_any in f.live_slots(record):
		var sd: Dictionary = s_any
		if d > float(f._slot_reach(sd)):
			continue
		var key := String(f.cooldown_key(sd))
		var cd_k: int
		if cds.has(key):
			cd_k = int(cds[key])
		else:
			var delay: float = float(f.slot_field(sd, "delay_s"))
			cd_k = Kc2RtQuant.half_to_even_ticks(delay, float(f.ticks_per_s)) if delay > 0.0 else 0
		if kw < cd_k:
			continue
		var chance: float = float(f.slot_field(sd, "chance_pct"))
		pred_certain = not (chance > 0.0 and chance < 100.0) and not String(sd.get("slot", "")).begins_with("special")
		return String(sd.get("_slot_key", ""))
	return ""


func advance_monster(dt: float) -> void:
	advance(dt)
	if dying:
		var t_end := gone_at_s - DEATH_FADE_S
		alpha_mult = clampf(1.0 - (clock_s - t_end) / DEATH_FADE_S, 0.0, 1.0) if clock_s > t_end else 1.0
	elif not released:
		# NOT YET IN THE FIGHT (before its enter tick): no body, only the pulsing arriving ring (KC2's 2D rule)
		alpha_mult = 0.0
	else:
		alpha_mult = 1.0
	if _ring != null:
		_ring.visible = not released and not dying
		var ph := 0.5 + 0.5 * sin(clock_s * 10.0)
		(_ring.material_override as StandardMaterial3D).albedo_color.a = 0.35 + 0.45 * ph
	if _shadow != null:
		_shadow.visible = released and not dying


var _ring: MeshInstance3D = null
var _shadow: MeshInstance3D = null


## The ground marks under a body (presentation only): a soft shadow disc of the body's own radius once it is in the
## fight, and the arriving ring before its enter tick (KC2's 2D "ARRIVING -- can't be hit yet" marker, in 3D).
func _build_ground_marks() -> void:
	var tm := TorusMesh.new()
	tm.inner_radius = radius_m * 1.15
	tm.outer_radius = radius_m * 1.35
	tm.rings = 32
	tm.ring_segments = 6
	var rm := StandardMaterial3D.new()
	rm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	rm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	rm.albedo_color = Color(0.70, 0.90, 1.0, 0.7)
	_ring = MeshInstance3D.new()
	_ring.mesh = tm
	rm.render_priority = PRIORITY_MARKS
	_ring.material_override = rm
	_ring.scale = Vector3(1.0, 0.05, 1.0)
	_ring.position = Vector3(0.0, 0.05, 0.0)
	_ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_ring)
	var cm := CylinderMesh.new()
	cm.top_radius = radius_m
	cm.bottom_radius = radius_m
	cm.height = 0.01
	cm.radial_segments = 24
	var sm := StandardMaterial3D.new()
	sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	sm.albedo_color = Color(0, 0, 0, 0.22)
	_shadow = MeshInstance3D.new()
	_shadow.mesh = cm
	sm.render_priority = PRIORITY_MARKS
	_shadow.material_override = sm
	_shadow.position = Vector3(0.0, 0.03, 0.0)
	_shadow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_shadow)
