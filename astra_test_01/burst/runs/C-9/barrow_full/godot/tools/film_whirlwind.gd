extends SceneTree
## C-9 R-C9-128 -- THE PORTED WHIRLWIND, FILMED FOR MATT. The dark knight in the painted Barrow presses EYE OF
## RECKONING (the real input path: its action, one frame -- `--action shield_bash`, his BASH key), spins the source harness's 2.30 s channel, walks east for 0.7 s
## mid-channel (the source's caster moved at full speed while channelling), and spins down. Once at play speed, then
## once at a quarter speed (Engine.time_scale 0.25). Run under Movie Maker by tools/film_whirlwind.sh.
const SETTLE := 90
var scene
var k
var frame := 0
var settle_end := -1
var plan := [1.0, 0.25]
var step := 0
var t := 0.0
var pressed := false
var act := "shield_bash"


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
		var a := OS.get_cmdline_user_args()
		var pp := (String(a[a.find("--place") + 1]) if a.has("--place") else "0.8,-1.2,S").split(",")
		scene.place_knight(float(pp[0]), float(pp[1]), String(pp[2]))
		if a.has("--action"):
			act = String(a[a.find("--action") + 1])
		if a.has("--single"):
			plan = [1.0]
		settle_end = frame + SETTLE
		return false
	if frame < settle_end:
		return false
	if frame == settle_end:
		print("[film] {\"trim_frames\":%d}" % settle_end)
	if step >= plan.size():
		t += dt
		if t > 0.6:
			print("[film] done frames=%d ww=%s" % [frame, JSON.stringify(scene.report.get("whirlwind", {}))])
			return true
		return false
	Engine.time_scale = float(plan[step])
	var gt := t                            # game seconds since this pass began (_process dt is already scaled)
	if not pressed:
		Input.action_press(act)
		pressed = true
		print("[film] pass %d at x%.2f" % [step, Engine.time_scale])
	elif Input.is_action_pressed(act):
		Input.action_release(act)
	if gt >= 1.6 and gt < 2.3:
		Input.action_press("move_right")
	else:
		Input.action_release("move_right")
	t += dt
	var busy: bool = scene.whirl != null and scene.whirl.busy()
	if gt > 3.6 and not busy:
		step += 1
		t = 0.0
		pressed = false
		Engine.time_scale = 1.0
	return false
