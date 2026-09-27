extends Node2D
# C-9 probe R-C9-34: the East-facing knight as a 2D PUPPET RIG.
#
# WHAT THIS IS.  scenes/knight_rig_E.tscn is a Skeleton2D/Bone2D puppet whose sprites
# are pieces cut straight out of the painted still (artifacts/seeds/seed_E.png) by
# tools/build_knight_rig_E.py.  Nothing here is repainted or re-generated: every pixel
# on screen is the painter's, moved.  That is the whole point of the probe -- the Grok
# clips drift (the helm and visor change between frames of one clip), and a rig cannot,
# because there is only ever one helm.
#
# WHAT IT REPLACES.  In style B, when the Keeper faces E, this node is shown and the
# knight's Grok walk_E / idle_E cells are hidden.  Every other direction is unchanged.
# G swaps E between RIG and GROK in place so the two can be compared on the same spot;
# scripts/style_toggle.gd owns the key and the HUD line, scripts/knight_skin.gd owns
# the decision, and this script only plays what it is told.
#
# GEOMETRY.  The rig is a child of KnightSprite and inherits its scale (0.727647), so
# it is authored in the same 512-cell pixel units as the Grok cells with its origin on
# the same foot pivot.  It is registered against sprites_knight/rest/idle_E.png helm
# crown to sole, so pressing G changes the MOTION and nothing else -- no size change,
# no sideways shunt.  (frames/knight_rig_E.json records the measurements.)
#
# TIMING.  walk is exactly one Keeper stride, 0.5797 s, and the planted foot's screen
# x is a straight line in time at the scene's own walk speed -- the plant is the
# parameterisation, not an approximation of one.  idle is the same 2.0 s breath the
# Grok idle cells use.

const WALK := "walk"
const IDLE := "idle"

@onready var _anim: AnimationPlayer = $Anim
@onready var _skel: Skeleton2D = $Skel

var _current: String = ""


func _ready() -> void:
	if _anim == null:
		push_error("knight_rig: no AnimationPlayer")
		return
	play_state(IDLE)


# Called by knight_skin.gd every frame it is active.  `kind` is already mapped
# (walk/idle) -- this node does no state mapping of its own.
func play_state(kind: String) -> void:
	if _anim == null:
		return
	var want: String = WALK if kind == WALK else IDLE
	if _current == want and _anim.is_playing():
		return
	_current = want
	_anim.play(want)


func current_animation() -> String:
	return _current


func animation_length(name: String) -> float:
	if _anim == null or not _anim.has_animation(name):
		return 0.0
	return _anim.get_animation(name).length


# --- introspection for the probe and the foot-slide measurement ----------------

# The near foot's bone.  Its global position is what "does the foot slide?" is a
# question about, so the measurement reads the RIG, not a re-rendered picture of it.
func near_foot_global() -> Vector2:
	var b := _skel.get_node_or_null(^"hip/leg_n_th/leg_n_sh/leg_n_ft")
	return Vector2.ZERO if b == null else (b as Node2D).global_position


func far_foot_global() -> Vector2:
	var b := _skel.get_node_or_null(^"hip/leg_f_th/leg_f_sh/leg_f_ft")
	return Vector2.ZERO if b == null else (b as Node2D).global_position


func hip_global() -> Vector2:
	var b := _skel.get_node_or_null(^"hip")
	return Vector2.ZERO if b == null else (b as Node2D).global_position


func seek(t: float) -> void:
	if _anim != null:
		_anim.seek(t, true)


func bone_count() -> int:
	return _skel.get_bone_count() if _skel != null else 0


func sprite_count() -> int:
	var n := 0
	for b in _skel.find_children("*", "Sprite2D", true, false):
		n += 1
	return n
