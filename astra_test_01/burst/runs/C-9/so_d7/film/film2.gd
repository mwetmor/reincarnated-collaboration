extends Node3D
## D7 PASS 2 film: the ember seeress HOLDING THE STAFF (staff_layer.gd) -- idle, walk, run, Fire Ball,
## Meteor -- at the Barrow's play camera, in the Barrow's light. The camera and sun are film.gd's
## (pass 1), which copied them VERBATIM from barrow_full.gd and paint_stack.gd::winter_sun.
##
## SCALE: rendered, not upscaled. shot2.json `rows` and `scale`: 540 rows at 1x is the play camera's
## own 100.6 px/m in a 960x540 frame; 2x renders 1080 rows of the SAME world extent (201.2 px/m).
## Pass 1's "2x" was a lanczos enlargement of the 1x pixels -- it could show nothing the 1x lacked.
##
## LOOPS: pass 1 never set a loop mode. Godot's glTF import leaves every clip LOOP_NONE unless its
## name says loop/cycle, so pass 1's walk played ONE second and she slid the other three frozen
## (frames 3.5 s and 5.5 s differ by 28 px of 518,400). staff_layer.gd sets them.
##
## CAPTURE: env FILM_OUT=<x.mp4> FILM_W FILM_H FILM_SCALE. She is rendered into an OFFSCREEN
## SubViewport of exactly FILM_W x FILM_H and every frame is piped raw to ffmpeg -> MP4, stepping
## time by exactly 1/30 s per frame. Movie Maker is NOT used: it records at the project's window
## size and RESCALES whatever the real viewport was -- a 960x540 window came out as a 1920x1080
## file of doubled pixels, and a 1080-row window cannot even open on this 1080-line display (it
## clamps to 971). The pipe writes exactly the pixels rendered.
##
## env IK_PROBE=1: no film -- evaluate the off-hand IK ENABLED at chosen instants and print how
## close the palm gets to its shaft target, then quit. Proves the wiring works, and cross-checks
## Blender's reach numbers for the Meteor in Godot's own solver.

const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const CAM_STANDOFF := 60.0
const SUN_ELEV_DEG := 55.0
const SUN_SCREEN_AZ_DEG := 305.0
const Staff := preload("res://staff_layer.gd")

var cam: Camera3D
var who: Node3D
var hold
var plan: Array = []
var t_shot := 0.0
var i_shot := -1
var cfg: Dictionary
var sv: SubViewport = null
var pipe: Dictionary = {}
var frames := 0

func winter_sun(elev_deg := 55.0, screen_az_deg := 305.0) -> DirectionalLight3D:
	var l := DirectionalLight3D.new()
	l.name = "WinterSun"
	var e := deg_to_rad(elev_deg)
	var a := deg_to_rad(screen_az_deg)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	l.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	l.light_color = Color(1.0, 0.955, 0.885)
	l.light_energy = 0.90
	l.shadow_enabled = true
	l.shadow_blur = 1.7
	return l

func _ready() -> void:
	cfg = JSON.parse_string(FileAccess.get_file_as_string("res://shot2.json"))
	plan = cfg["plan"]
	var sun_rig := Node3D.new()
	sun_rig.rotation_degrees.y = PL_YAW_DEG
	add_child(sun_rig)
	var sun := winter_sun(SUN_ELEV_DEG, SUN_SCREEN_AZ_DEG)
	sun.directional_shadow_max_distance = CAM_STANDOFF + 50.0
	sun_rig.add_child(sun)
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.88, 0.90)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1)
	env.ambient_light_energy = 0.30
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	var g := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(80, 80)
	g.mesh = pm
	var sm := StandardMaterial3D.new()
	sm.albedo_color = Color(0.80, 0.80, 0.82)
	sm.roughness = 0.95
	g.material_override = sm
	add_child(g)
	who = (load(cfg["glb"]) as PackedScene).instantiate()
	add_child(who)
	hold = Staff.new()
	add_child(hold)
	var probe := OS.get_environment("IK_PROBE") == "1"
	hold.setup(who, probe)
	if probe:
		await get_tree().process_frame
		_ik_probe()
		get_tree().quit()
		return
	var sc := float(OS.get_environment("FILM_SCALE")) if OS.has_environment("FILM_SCALE") else 1.0
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = 0.05
	cam.far = CAM_STANDOFF + 300.0
	var rows := float(get_viewport().get_visible_rect().size.y)
	if OS.has_environment("FILM_OUT"):
		sv = SubViewport.new()
		sv.size = Vector2i(int(OS.get_environment("FILM_W")), int(OS.get_environment("FILM_H")))
		sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		add_child(sv); sv.add_child(cam)
		rows = float(sv.size.y)
		hold.tree.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
		var args := ["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % [sv.size.x, sv.size.y],
			"-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
			"-movflags", "+faststart", OS.get_environment("FILM_OUT")]
		pipe = OS.execute_with_pipe(OS.get_environment("FFMPEG") if OS.has_environment("FFMPEG") else "/opt/homebrew/bin/ffmpeg", args, true)
	else:
		add_child(cam)
	cam.current = true
	cam.size = rows / (PPM * sc)
	print("[film2] frame %s, scale %.0fx -> %.2f px/m%s" % [sv.size if sv else get_viewport().get_visible_rect().size, sc,
		rows / cam.size, " -> " + OS.get_environment("FILM_OUT") if sv else ""])
	_aim()
	_next()
	if sv:
		_capture()

func _aim() -> void:
	var p := deg_to_rad(PL_PITCH_DEG)
	var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := who.global_position + Vector3(0, 0.85, 0)
	cam.look_at_from_position(at - f * CAM_STANDOFF, at, Vector3.UP)

func _next() -> void:
	i_shot += 1
	if i_shot >= plan.size():
		if sv == null:
			get_tree().quit()
		return
	t_shot = 0.0
	var s: Dictionary = plan[i_shot]
	who.rotation_degrees.y = float(s.get("heading_deg", 0.0))
	hold.play(String(s["clip"]), 0.0)
	print("[film2] %5.2fs %s (layer %s, IK %s)" % [Time.get_ticks_msec() / 1000.0, s["clip"],
		Staff.LAYER.get(s["clip"], "none"), "on" if Staff.IK_ON.get(s["clip"], false) else "off"])

func _process(dt: float) -> void:
	if sv == null:
		_step(dt)

## one fixed step of the shot: move her, aim the IK and the camera, advance the plan
func _step(dt: float) -> void:
	if i_shot < 0 or i_shot >= plan.size():
		return
	var s: Dictionary = plan[i_shot]
	var v := float(s.get("speed", 0.0))
	if v > 0.0:
		# her forward is +Z (Blender -Y exports as glTF +Z)
		who.global_position += who.global_transform.basis.z * v * dt
	hold.aim_ik()
	hold.grips(bool(Staff.IK_ON.get(hold.clip, false)))
	_aim()
	t_shot += dt
	if t_shot >= float(s["seconds"]) - 1e-6:
		_next()

## the capture loop: render, pipe the frame, step exactly 1/30 s -- until the plan ends
func _capture() -> void:
	var dt := 1.0 / 30.0
	var io: FileAccess = pipe["stdio"]
	while i_shot < plan.size():
		hold.evaluate(0.0)
		await RenderingServer.frame_post_draw
		var img := sv.get_texture().get_image()
		img.convert(Image.FORMAT_RGB8)
		io.store_buffer(img.get_data())
		frames += 1
		hold.tree.advance(dt)
		_step(dt)
	io.close()
	var pid := int(pipe["pid"])
	while OS.is_process_running(pid):
		await get_tree().create_timer(0.2).timeout
	print("[film2] %d frames piped (%.2f s at 30 fps)" % [frames, frames / 30.0])
	get_tree().quit()

func _ik_probe() -> void:
	# The IK's result exists only INSIDE the skeleton's update: Skeleton3D restores the unmodified
	# pose after `skeleton_updated`, so a read after it sees the arm as if the IK never ran (the
	# first probe read 0.860 m with the IK off AND on). Read the wrist in the signal instead.
	var sk: Skeleton3D = hold.skel
	var seen := {}
	sk.skeleton_updated.connect(func(): seen["wrist"] = hold.bone_world("LeftHand").origin)
	var out := []
	for c in [["idle", 1.0], ["walk", 0.5], ["run", 0.4], ["cast_fireball", 0.9167], ["cast_meteor", 0.5],
			["cast_meteor", 1.0], ["cast_meteor", 1.625], ["cast_meteor", 2.2]]:
		hold.play(String(c[0]), float(c[1]))
		hold.ik.active = false
		hold.evaluate(0.0)
		var tgt: Vector3 = hold.ik_target.global_position
		var sh: Vector3 = hold.bone_world("LeftArm").origin
		var el: Vector3 = hold.bone_world("LeftForeArm").origin
		var w0: Vector3 = seen["wrist"]
		var reach := sh.distance_to(el) + el.distance_to(w0) + Staff.PALM_M
		hold.ik.active = true
		hold.evaluate(0.0)
		var w1: Vector3 = seen["wrist"]
		hold.ik.active = false
		# palm residual: the virtual end sits PALM_M beyond the wrist, so it is ON the target exactly
		# when wrist->target == PALM_M; beyond reach it is (wrist->target - PALM_M) short
		var r := {"clip": c[0], "t": c[1], "shoulder_to_target_m": snappedf(sh.distance_to(tgt), 0.001),
				  "reach_m": snappedf(reach, 0.001),
				  "palm_short_ik_off_m": snappedf(maxf(w0.distance_to(tgt) - Staff.PALM_M, 0.0), 0.001),
				  "palm_short_ik_on_m": snappedf(maxf(w1.distance_to(tgt) - Staff.PALM_M, 0.0), 0.001),
				  "wrist_moved_m": snappedf(w0.distance_to(w1), 0.001)}
		out.append(r)
		print("[ik] %-14s t=%.3f  shoulder->target %.3f m vs reach %.3f m | palm short of the shaft: IK off %.3f m, IK ON %.3f m (wrist moved %.3f m)"
			% [c[0], c[1], r["shoulder_to_target_m"], r["reach_m"], r["palm_short_ik_off_m"], r["palm_short_ik_on_m"], r["wrist_moved_m"]])
	var f := FileAccess.open(OS.get_environment("IK_OUT") if OS.has_environment("IK_OUT") else "/dev/null", FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(out, " ")); f.close()
