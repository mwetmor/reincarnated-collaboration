extends Node3D
## C-9 BV2F ARENA (R-C9-348) -- a body whose record has NO JOIN-1 pack: KC2 draws it as a labelled TOKEN
## (kc2_play/src/kc2p_token.gd: the body's own radius, a lunge + flash on the swing tick, a death fade, a
## "NO PACK · family" plate), and so does this view -- a capsule of the record's radius, in 3D.

const LUNGE_S := 0.18
const LUNGE_M := 0.45
const FADE_S := 0.6

var actor_id: int = 0
var record: String = ""
var radius_m: float = 0.62
var hp: float = 0.0
var hp_max: float = 1.0
var champion: bool = false
var label: String = ""
var released: bool = false
var pos_m: Vector2 = Vector2.ZERO
var dying: bool = false
var hold_ticks_left: int = 0
var true_height_m: float = 1.7
var clock_s: float = 0.0
var _lunge_dir := Vector2.ZERO
var _lunge_t := -1.0
var _flash_t := -1.0
var _die_t := -1.0
var _mi: MeshInstance3D = null
var _mat: StandardMaterial3D = null
var lunge_offset_m := Vector2.ZERO


func setup_monster(_sess, a: Dictionary, entry: Dictionary) -> void:
	actor_id = int(a["id"])
	record = String(a.get("record_path", ""))
	radius_m = float(a.get("body_radius_m", 0.62))
	champion = bool(a.get("is_hero", false))
	label = "Creature"                         # replaced by arena_mode.display_name (R-C9-357); no record name shown
	var cm := CapsuleMesh.new()
	cm.radius = radius_m
	cm.height = maxf(true_height_m, radius_m * 2.0 + 0.1)
	_mat = StandardMaterial3D.new()
	_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_mat.albedo_color = Color(0.55, 0.16, 0.20, 0.85)
	_mi = MeshInstance3D.new()
	_mi.mesh = cm
	_mat.render_priority = 125      # after the paint post pass (paint_stack.gd POST_PRIORITY 120)
	_mi.material_override = _mat
	_mi.position = Vector3(0, cm.height * 0.5, 0)
	_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_mi)


func sync_actor(a: Dictionary, _body: Dictionary, _player_m: Vector2, _wave_s: float, _tick: int) -> void:
	hp = float(a.get("hp", 0.0))
	hp_max = maxf(1.0, float(a.get("hp_max", 1.0)))
	released = String(a.get("state", "")) == "ENGAGE"
	pos_m = Vector2(float(a["x_m"]), float(a["y_m"]))


func on_cast_start(_slot_key: String, aim: Vector2) -> void:
	var d := aim - pos_m
	_lunge_dir = d.normalized() if d.length() > 1e-6 else Vector2.ZERO
	_lunge_t = clock_s


func on_hit() -> void:
	_flash_t = clock_s


func on_death() -> void:
	if dying:
		return
	dying = true
	_die_t = clock_s


func faded_out() -> bool:
	return dying and clock_s >= _die_t + FADE_S


func advance_monster(dt: float) -> void:
	clock_s += dt
	var al := 0.85
	if dying:
		al *= clampf(1.0 - (clock_s - _die_t) / FADE_S, 0.0, 1.0)
	elif not released:
		al = 0.0
	var c := Color(0.55, 0.16, 0.20, al)
	if _flash_t >= 0.0 and clock_s - _flash_t < 0.16:
		c = Color(1.0, 0.9, 0.8, al)
	_mat.albedo_color = c
	lunge_offset_m = Vector2.ZERO
	if _lunge_t >= 0.0 and clock_s - _lunge_t < LUNGE_S:
		lunge_offset_m = _lunge_dir * LUNGE_M * sin(PI * (clock_s - _lunge_t) / LUNGE_S)
