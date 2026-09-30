extends Node3D
## D7 pass 2 instrument: beauty + ID stills at the PLAY CAMERA, 1x and 2x, several facings.
## ID pass: every MeshInstance3D gets an UNSHADED flat colour by what it is --
##   body (char1) RED, garments BLUE, staff/circlet GREEN -- so a body pixel enclosed by garment
##   pixels is a HOLE in the garment, and nothing about lighting or texture can move that count.
const PPM := 100.617553710938
const PL_PITCH_DEG := 52.95354112560294
const PL_YAW_DEG := 47.0
const CAM_STANDOFF := 60.0
var cfg: Dictionary
var who: Node3D
var ap: AnimationPlayer
var cam: Camera3D
## THE RENDER TARGET IS A 1920x1080 SubViewport, not the window. The window cannot be 1080 rows on
## this Mac (a 1920x1080 display less its menu and title bars): every still before this was
## 1920x971, and with cam.size = 1080/PPM that is 971/1080 x 100.6 = 90.5 px/m -- the whole
## pass-2 speckle series ran at 0.90x the play scale. An offscreen SubViewport is exactly 1080 rows.
var sv: SubViewport
var ground: MeshInstance3D
var orig := {}
var hold = null
const Staff := preload("res://staff_layer.gd")

func winter_sun() -> DirectionalLight3D:
	var l := DirectionalLight3D.new()
	var e := deg_to_rad(55.0); var a := deg_to_rad(305.0)
	var d := Vector3(-sin(a) * cos(e), -sin(e), -cos(a) * cos(e)).normalized()
	l.look_at_from_position(Vector3(0, 30, 0), Vector3(0, 30, 0) + d, Vector3.UP)
	l.light_color = Color(1.0, 0.955, 0.885); l.light_energy = 0.90
	l.shadow_enabled = true; l.shadow_blur = 1.7
	l.directional_shadow_max_distance = CAM_STANDOFF + 50.0
	return l

func _ready() -> void:
	cfg = JSON.parse_string(FileAccess.get_file_as_string("res://stills.json"))
	var rig := Node3D.new(); rig.rotation_degrees.y = PL_YAW_DEG; add_child(rig); rig.add_child(winter_sun())
	var env := Environment.new(); env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.86, 0.88, 0.90)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1); env.ambient_light_energy = 0.30
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	ground = MeshInstance3D.new(); var pm := PlaneMesh.new(); pm.size = Vector2(80, 80); ground.mesh = pm
	var sm := StandardMaterial3D.new(); sm.albedo_color = Color(0.80, 0.80, 0.82); sm.roughness = 0.95
	ground.material_override = sm; add_child(ground)
	who = (load(cfg["glb"]) as PackedScene).instantiate(); add_child(who)
	ap = who.find_child("AnimationPlayer", true, false)
	# PASS 2: pose her THROUGH the staff layer (carry, grip) when stills.json says "layer": the dots
	# are counted on the pose the player sees, not on the raw clip
	if bool(cfg.get("layer", false)):
		hold = Staff.new(); add_child(hold); hold.setup(who, true)
		hold.undress_keys = bool(cfg.get("under_keys", true))
	cam = Camera3D.new(); cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT; cam.near = 0.05; cam.far = CAM_STANDOFF + 300.0
	sv = SubViewport.new(); sv.size = Vector2i(1920, 1080)
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(sv); sv.add_child(cam); cam.current = true
	for mi in who.find_children("*", "MeshInstance3D", true, false):
		orig[mi] = mi.material_override
	# EXPERIMENT (pass 2): garments DOUBLE-SIDED. The tripo garment materials are single-sided, so any
	# garment face that faces away from the camera -- a flipped triangle, or a thick hem's inner wall
	# where the outer wall has a gap -- is culled and the body behind it shows as a dot
	if bool(cfg.get("garment_double_sided", false)):
		for mi in orig:
			if _kind(String(mi.name)) == Color(0, 0, 1):
				for si in (mi as MeshInstance3D).mesh.get_surface_count():
					var m0 = (mi as MeshInstance3D).get_active_material(si)
					if m0 is BaseMaterial3D:
						var m1: BaseMaterial3D = (m0 as BaseMaterial3D).duplicate()
						m1.cull_mode = BaseMaterial3D.CULL_DISABLED
						(mi as MeshInstance3D).set_surface_override_material(si, m1)
	# WATCHDOG: the first version hung for five minutes on a script error inside _ready, never
	# reaching quit(). Nothing this instrument does should take 90 s.
	get_tree().create_timer(float(cfg.get("watchdog_s", 90.0))).timeout.connect(func(): push_error("stills WATCHDOG"); get_tree().quit(3))
	await _shoot()
	get_tree().quit()

func _kind(n: String) -> Color:
	var s := n.to_lower()
	if s.contains("char1"): return Color(1, 0, 0)
	if s.contains("staff") or s.contains("circlet"): return Color(0, 1, 0)
	return Color(0, 0, 1)

func _kind_g(n: String) -> Color:
	var s := n.to_lower()
	if s.contains("robe"): return Color(0, 0, 1)
	if s.contains("mantle"): return Color(0, 1, 1)
	if s.contains("belt"): return Color(1, 0, 1)
	if s.contains("tripo_node"): return Color(1, 1, 0)
	return _kind(n)

func _set_id(on: bool) -> void:
	ground.visible = not on
	for mi in orig:
		if on:
			var m := StandardMaterial3D.new(); m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			if bool(cfg.get("garment_double_sided", false)) and _kind(String(mi.name)) == Color(0, 0, 1):
				m.cull_mode = BaseMaterial3D.CULL_DISABLED
			m.albedo_color = _kind(String(mi.name)); mi.material_override = m
		else:
			mi.material_override = orig[mi]
	for c in get_children():
		if c is WorldEnvironment:
			(c as WorldEnvironment).environment.background_color = Color(0, 0, 0) if on else Color(0.86, 0.88, 0.90)
		if c is Node3D and c.get_child_count() > 0 and c.get_child(0) is DirectionalLight3D:
			c.get_child(0).visible = not on

var _zm: ShaderMaterial = null
## view depth as colour: R = coarse (Z_NEAR..Z_FAR over 255 steps), G = the fraction within the step
func _zmat() -> ShaderMaterial:
	if _zm == null:
		var sh := Shader.new()
		sh.code = """shader_type spatial;
render_mode unshaded, cull_back;
uniform float z_near = 57.0;
uniform float z_far = 63.0;
// the viewport stores sRGB: pre-apply the inverse so the 8-bit values ARE the code
float lin(float v) { return v <= 0.04045 ? v / 12.92 : pow((v + 0.055) / 1.055, 2.4); }
void fragment() {
	float t = clamp((-VERTEX.z - z_near) / (z_far - z_near), 0.0, 1.0) * 255.0;
	ALBEDO = vec3(lin(floor(t) / 255.0), lin(fract(t)), lin(1.0));
}"""
		_zm = ShaderMaterial.new(); _zm.shader = sh
	return _zm

func _aim(scale: float) -> void:
	cam.size = (float(sv.size.y) / PPM) / scale
	var p := deg_to_rad(PL_PITCH_DEG); var y := deg_to_rad(PL_YAW_DEG)
	var f := Vector3(-sin(y) * cos(p), -sin(p), -cos(y) * cos(p)).normalized()
	var at := who.global_position + Vector3(0, 0.85, 0)
	cam.look_at_from_position(at - f * CAM_STANDOFF, at, Vector3.UP)

func _shoot() -> void:
	var out: String = cfg["out"]
	for clip in cfg["clips"]:
		for hd in cfg["headings"]:
			who.rotation_degrees.y = float(hd)
			if hold:
				hold.play(clip, float(cfg["t"])); hold.evaluate(0.0)
			elif ap and ap.has_animation(clip):
				ap.play(clip); ap.seek(float(cfg["t"]), true); ap.pause()
			for sc in cfg["scales"]:
				_aim(float(sc))
				var modes := ["beauty", "id"]
				if bool(cfg.get("id_nobody", false)):
					modes.append("idnb")
				if bool(cfg.get("depth_passes", false)):
					modes.append_array(["zb", "zg"])
				if bool(cfg.get("garment_ids", false)):
					modes.append("idg")
				for mode in modes:
					_set_id(mode != "beauty")
					# idnb: the ID pass with the BODY HIDDEN -- what lies behind a body pixel.
					# BUT "garment behind" is not yet a poke: through a real opening the ray meets the
					# body and then the robe's far side. The DEPTH passes settle it:
					#   zb  body only, zg  garments only, each writing view depth as colour
					# a dot is a POKE when the garment behind is within a few cm of the body pixel,
					# and a GAP in the near cloth when the garment behind is the far side of her.
					for mi in orig:
						var k := _kind(String(mi.name))
						var vis := true
						if mode == "idnb":
							vis = k != Color(1, 0, 0)
						elif mode == "zb":
							vis = k == Color(1, 0, 0)
						elif mode == "zg":
							vis = k == Color(0, 0, 1)
						(mi as MeshInstance3D).visible = vis
						if mode == "zb" or mode == "zg":
							mi.material_override = _zmat()
						if mode == "idg":
							# which GARMENT: robe blue, mantle cyan, belt magenta, bracers yellow
							var gm := StandardMaterial3D.new(); gm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
							gm.albedo_color = _kind_g(String(mi.name)); mi.material_override = gm
					for i in 4: await RenderingServer.frame_post_draw
					var img := sv.get_texture().get_image()
					img.save_png("%s/%s_%s_h%d_s%d_%s.png" % [out, cfg["tag"], clip, int(hd), int(sc), mode])
