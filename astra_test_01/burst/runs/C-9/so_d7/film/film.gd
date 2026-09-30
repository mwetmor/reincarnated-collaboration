extends Node3D
## D7 film: the sorceress walking, idling and casting, AT THE PLAY CAMERA, in the Barrow's light.
##
## The camera and the sun are the Barrow's own numbers, copied from
## runs/C-9/barrow_full/godot/scripts/barrow_full.gd and paint_stack.gd::winter_sun --
## not re-derived, because "the Barrow's light" means that light and not one like it.
##   PlayCamera  orthographic, keep height, 100.617553710938 px/m, pitch 52.9535 deg, yaw 47 deg
##   WinterSun   55 deg elevation, screen azimuth 305 (upper-left in the CAMERA's frame),
##               colour (1.0, 0.955, 0.885), energy 0.90, shadows on, blur 1.7
##
## The clips ship IN PLACE, so she is moved by this script at each clip's FOOT-LOCK speed
## (manifest locomotion.*.speed_m_s): the speed at which her planted foot stays still.

const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const CAM_STANDOFF := 60.0
const SUN_ELEV_DEG := 55.0
const SUN_SCREEN_AZ_DEG := 305.0

var cam: Camera3D
var who: Node3D
var ap: AnimationPlayer
var plan: Array = []      # [{clip, seconds, speed, heading_deg}] from shot.json
var t_shot := 0.0
var i_shot := -1

func winter_sun(elev_deg := 55.0, screen_az_deg := 305.0) -> DirectionalLight3D:
	# VERBATIM from paint_stack.gd, bar the comments: ONE light, low, pale-warm, from screen
	# upper-left. screen_az is in the camera's yaw frame, so the parent is yawed to match.
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
	var cfg: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://shot.json"))
	plan = cfg["plan"]
	# the sun, in a node yawed like the camera so "upper left" stays upper left on screen
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
	# snow: albedo 0.80, the value the sun's 0.90 energy was solved against
	var g := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(80, 80)
	g.mesh = pm
	var sm := StandardMaterial3D.new()
	sm.albedo_color = Color(0.80, 0.80, 0.82)
	sm.roughness = 0.95
	g.material_override = sm
	add_child(g)
	# her
	var packed: PackedScene = load(cfg["glb"])
	who = packed.instantiate()
	add_child(who)
	ap = who.find_child("AnimationPlayer", true, false)
	# the play camera
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.size = float(cfg.get("view_rows", 1080)) / PPM
	cam.near = 0.05
	cam.far = CAM_STANDOFF + 300.0
	add_child(cam)
	cam.current = true
	_aim()
	_next()

func _aim() -> void:
	var p := deg_to_rad(PL_PITCH_DEG)
	var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := who.global_position + Vector3(0, 0.85, 0)
	cam.look_at_from_position(at - f * CAM_STANDOFF, at, Vector3.UP)

func _next() -> void:
	i_shot += 1
	if i_shot >= plan.size():
		get_tree().quit()
		return
	t_shot = 0.0
	var s: Dictionary = plan[i_shot]
	who.rotation_degrees.y = float(s.get("heading_deg", 0.0))
	if ap and ap.has_animation(s["clip"]):
		ap.play(s["clip"])
	else:
		push_error("missing clip %s" % s["clip"])

func _process(dt: float) -> void:
	if i_shot < 0 or i_shot >= plan.size():
		return
	var s: Dictionary = plan[i_shot]
	var v := float(s.get("speed", 0.0))
	if v > 0.0:
		# HER forward is +Z here: Blender -Y (she faces it) exports as glTF +Z. The first draft
		# moved her along -Z, which would have walked her backwards across the snow.
		who.global_position += who.global_transform.basis.z * v * dt
	_aim()
	t_shot += dt
	if t_shot >= float(s["seconds"]):
		_next()
