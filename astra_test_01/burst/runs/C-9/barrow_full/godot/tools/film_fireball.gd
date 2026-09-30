extends SceneTree
## C-9 (c) -- THE FIRE BALL FILM FOR MATT: her Fire Ball in the painted Barrow, at play speed, then at
## quarter speed (Engine.time_scale 0.25: her strike and the baked Fire Ball both run on game time).
## Run under Movie Maker by tools/film_fireball.sh; the phone page's look (Compatibility, the web branches
## on). Three casts facing east, south and north; then east and south again at a quarter speed.

const SETTLE := 90
var scene
var k
var frame := 0
var settle_end := -1
var plan := [[Vector2(1, 0), 1.0], [Vector2(-0.8, 0.6), 1.0], [Vector2(0.3, -1), 1.0], [Vector2(1, 0), 0.25], [Vector2(-0.8, 0.6), 0.25]]
var turn := 0
var step := 0
var t_since := 0.0
var casting := false


func _initialize() -> void:
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)


func _process(dt: float) -> bool:
	frame += 1
	if scene == null or not bool(scene.ready_done):
		return false
	if settle_end < 0:
		scene.set_hud_visible(false)
		for c in scene.get_children():
			if c is CanvasLayer and String(c.name) != "FxLabel":
				(c as CanvasLayer).visible = false
		k = scene.knight
		settle_end = frame + SETTLE
		scene.place_knight(0.8, -1.2, "E")
		return false
	if frame < settle_end:
		return false
	if frame == settle_end:
		print("[film] {\"trim_frames\":%d}" % settle_end)
	t_since += dt / maxf(Engine.time_scale, 1e-3)       # real seconds of film
	if step >= plan.size():
		if t_since > 1.0:
			print("[film] done frames=%d" % frame)
			return true
		return false
	var spec: Array = plan[step]
	if not casting:
		Engine.time_scale = float(spec[1])
		# TURN HER: a few steps toward the aim (her rig faces where she walks), a beat, then the cast
		turn += 1
		if turn <= 8:
			k.drive_dir((spec[0] as Vector2).normalized(), false, 1.0 / 60.0)
			return false
		if turn <= 26:
			k.drive_dir(Vector2.ZERO, false, 1.0 / 60.0)
			return false
		if k.try_strike("slash"):
			casting = true
			turn = 0
			t_since = 0.0
	elif t_since > 3.6 / float(spec[1]):
		casting = false
		step += 1
		t_since = 0.0
	return false
