extends AnimatedSprite2D
# C-9: the Illuminated knight, worn by the Keeper as her style-B skin.
#
# This node is a PURE SKIN.  It is a second AnimatedSprite2D parented to the same
# Keeper CharacterBody2D, so the physics body, collision footprint, camera, walkable
# polygon, VFX sockets and keeper.gd's whole state machine are untouched -- the knight
# only READS the Keeper's `state` and `facing` each frame and plays the matching cell.
# scripts/style_toggle.gd shows this node and hides the Keeper's own AnimatedSprite2D
# in B, and the reverse in A, so T swaps the player sprite along with the scenery.
#
# GEOMETRY (computed by tools/build_knight_frames.py, recorded in frames/knight_fit.json
# and baked into scenes/cliffside.tscn):
#   scale  0.727647   so the knight's helm-crown-to-sole height on the cliffside canvas
#                     equals the Keeper's 150.2 px
#   offset (-256.5, -395.2)   the knight's feet pivot -- his mean sole row across all 16
#                     registered rest frames -- pinned to the body origin, same as the
#                     Keeper's own (-256, -400)
#
# TIMING is carried by the SpriteFrames resource, not by this script, and since
# 2026-09-27 it MATCHES THE KEEPER rather than the painting: tools/build_knight_frames.py
# reads her walk cadence out of frames/keeper.tres (12 frames at 20.7 fps = 0.5797 s per
# stride, the same in all eight directions) and gives every knight walk_<D> that stride
# duration.  The clips' own painted timing was 3.130-6.545 fps -- 3.2x to 6.6x slower
# than the character standing beside him in the other register, which is what Matt saw
# when he played v2 ("about half time motion of the keeper"; it was worse than half).
# Idle is unchanged at 6 fps (12 frames over the 2.0 s breath).  speed_scale stays 1.0.
#
# STATE MAP.  The knight has walk and idle cells only.  For B: run -> walk, and
# cast/jump -> idle.  style_toggle.gd states this on the HUD line so nobody reads a
# mapped state as a painted one.

const STATE_MAP := {
	"walk": "walk",
	"run": "walk",
	"idle": "idle",
	"cast": "idle",
	"jump": "idle",
}
const DIRECTIONS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]

var _keeper: Node = null
var _missing: Dictionary = {}


func _ready() -> void:
	_keeper = get_parent()
	if _keeper == null or not ("state" in _keeper and "facing" in _keeper):
		push_error("knight_skin: parent is not the Keeper (no state/facing)")
		_keeper = null
		return
	sync_now()


func _process(_delta: float) -> void:
	if visible:
		sync_now()


# Public so the headless probe can drive it without waiting on a process frame.
func sync_now() -> void:
	if _keeper == null or sprite_frames == null:
		return
	var kind: String = STATE_MAP.get(String(_keeper.state), "idle")
	var facing: String = String(_keeper.facing)
	if not DIRECTIONS.has(facing):
		facing = "S"
	var want: String = kind + "_" + facing
	if not sprite_frames.has_animation(want):
		# No mirroring is used -- all 8 directions are painted -- so this is a real gap.
		if not _missing.has(want):
			_missing[want] = true
			push_warning("knight_skin: no animation '%s'" % want)
		want = "idle_" + facing
		if not sprite_frames.has_animation(want):
			return
	if animation != want or not is_playing():
		play(want)


# --- introspection for tools/probe_ab.gd ---------------------------------------

func mapped_state() -> String:
	return "" if _keeper == null else String(STATE_MAP.get(String(_keeper.state), "idle"))


func animation_fps(name: StringName) -> float:
	return sprite_frames.get_animation_speed(name)
