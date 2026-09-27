extends StaticBody2D
# C-9 scene v3: a static, south-facing painted figure that exists only in style B.
#
# Matt's call was STILLS, no animation, so there is no AnimationPlayer here and nothing
# ticks per frame.  The node's ORIGIN is the figure's feet -- the child Sprite2D carries
# the offset that puts it there -- so the y_sort_enabled Actors/ parent sorts this
# figure against the knight on their ground contact points, and he passes in front of
# one and behind the other exactly as their feet say he should.
#
# HIDING IS NOT ENOUGH.  In style A these figures are not part of the register and must
# not be there at all.  `visible = false` stops the drawing and leaves the collision
# standing, so the Keeper would walk into an invisible wall in A.  set_active() takes
# the CollisionShape2D down with the sprite -- deferred, because a body's shapes may not
# be re-entrantly edited during physics resolution.

@export var figure_name: String = ""

@onready var _shape: CollisionShape2D = $CollisionShape2D


func _ready() -> void:
	add_to_group("b_figures")


func set_active(on: bool) -> void:
	visible = on
	if _shape != null:
		_shape.set_deferred("disabled", not on)


func is_active() -> bool:
	return visible and _shape != null and not _shape.disabled
