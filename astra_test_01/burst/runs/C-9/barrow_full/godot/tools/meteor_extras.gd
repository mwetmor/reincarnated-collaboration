extends RefCounted
## C-9 (d) -- LANE A'S METEOR: its two GROUND layers, in the kit's own material (the burst kit's
## mix / outside-in / noise-erosion shader, the fire palette). The G1 kit (meteor_e1: the painted head and
## trail, fl6 travel layers; its impact the burst template cut from VF-met-impact-01) has no grammar for a
## target ring or a burning pool, so these two are driven here, by the same 60 Hz tick the kit counts in,
## and the SAME code runs in the bake (bake_meteor.gd) and in the proof (proof_meteor.gd).
##   RING  (VF-met-ring-01, 340 px): at the landing point from the call; erodes in over 8 ticks, holds,
##         and erodes away over 12 ticks from the impact.
##   BURN  (C-5 VF-prim-fire-pool-01, 346 px): from the impact + 3 ticks it erodes in over 10 ticks, boils
##         (erode +-0.05 at 6 Hz, the burst's own boil rate) for 3 s, the last second eroding away.
## Both centred GROUND_DY px below the burst's anchor: where its flames meet the ground.

const DIR := "res://vfx/meteor_e1_extra/"
const RING_SCALE := 340.0 / 422.0
const BURN_SCALE := 0.8
const GROUND_DY := 110.0
const RING_IN := 8
const RING_OUT := 12
const BURN_DELAY := 3
const BURN_IN := 10
const BURN_TOTAL := 180
const BURN_FADE := 60

var ring: Sprite2D
var burn: Sprite2D
var impact_tick := -1


func build(parent: Node2D) -> void:
	var base: ShaderMaterial = load("res://vfx/meteor_e1_burst/materials/Piece_Peak.tres")
	for spec in [["ring", RING_SCALE, -3], ["burn", BURN_SCALE, -2]]:
		var s := Sprite2D.new()
		s.name = "Meteor_" + String(spec[0])
		s.texture = load(DIR + String(spec[0]) + ".png")
		s.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var m := base.duplicate() as ShaderMaterial
		m.set_shader_parameter("distance_texture", load(DIR + String(spec[0]) + "_distance.png"))
		m.set_shader_parameter("erode", 1.0)
		m.set_shader_parameter("dissolve", 0.0)
		s.material = m
		s.scale = Vector2.ONE * float(spec[1])
		s.z_index = int(spec[2])
		s.visible = false
		parent.add_child(s)
		if spec[0] == "ring":
			ring = s
		else:
			burn = s


func place(target_anchor: Vector2) -> void:
	ring.position = target_anchor + Vector2(0, GROUND_DY)
	burn.position = target_anchor + Vector2(0, GROUND_DY)


## tick: physics ticks since the release; impact: the tick the burst spawned (-1 before it)
func step(tick: int, impact: int) -> bool:
	impact_tick = impact
	var re := 1.0 - clampf(float(tick) / float(RING_IN), 0.0, 1.0)
	if impact >= 0:
		re = maxf(re, clampf(float(tick - impact) / float(RING_OUT), 0.0, 1.0))
	ring.visible = re < 1.0
	(ring.material as ShaderMaterial).set_shader_parameter("erode", re)
	var alive := ring.visible
	if impact >= 0:
		var b := tick - impact - BURN_DELAY
		var be := 1.0
		if b >= 0 and b < BURN_TOTAL:
			be = 1.0 - clampf(float(b) / float(BURN_IN), 0.0, 1.0)
			be = maxf(be, clampf(float(b - (BURN_TOTAL - BURN_FADE)) / float(BURN_FADE), 0.0, 1.0))
			be = clampf(be + 0.05 * sin(TAU * 6.0 * float(b) / 60.0), 0.0, 1.0)
		burn.visible = be < 1.0
		(burn.material as ShaderMaterial).set_shader_parameter("erode", be)
		alive = alive or (b < BURN_TOTAL)
	else:
		burn.visible = false
		alive = true
	return alive
