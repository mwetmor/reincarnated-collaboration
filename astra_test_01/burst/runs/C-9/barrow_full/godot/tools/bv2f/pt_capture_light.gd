extends SceneTree
## BV2F lane PT (R-C9-191): v1's tools/capture_light.gd COPIED, two marked changes (BV2F-PT): the pilot plate size and
## the pilot scene (its guide window = the pilot window). Everything else -- the ramp, atlas, MSAA, sun -- is v1's.
## C-9 T10-2 step 4: THE PAINTING'S LIGHT, AS A MAP -- where the painter painted direct sun. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/capture_light.gd -- --out DIR
##
## The painter painted over the blockout's own render, and the rules held the shadows where the
## render put them ("shadows stay where the render puts them": one winter sun, 55 degrees). So
## the blockout, re-rendered at the guide camera with the guide's own sun, shadow atlas (8192) and
## filter, but with every static surface writing ITS LIGHT instead of its colour, is the map of
## what the painting shows lit and what it shows in shadow:
##   R  the direct-sun share through the guide's OWN ramp (the pre-T10-1c stack the guide was
##      rendered with: the cast shadow multiplied in BEFORE the bands; no wash noise):
##      (band - m0) / (m2 - m0) -- 1 on sunlit flat snow, 0 in a cast shadow or on a face turned
##      from the sun, 0.56 on a flank in the middle band
##   G  the cast shadow alone (ATTENUATION), 1 lit
##   B  N.L, clamped
## His shadow on the painted world darkens by the DIRECT SUN'S SHARE, G x min(B / sin 55, 1) --
## the cast shadow times N.L over flat ground's (tools/paint_world_prep.py builds lit.bin from it;
## R is kept as the record of the guide's own bands, where flat sunlit snow sits at 0.82): a
## shadow falling into a painted shadow adds nothing (PaintedWorld.his_shadow). No knight (the
## guide's barbarian was painted out); no ink.

const GUIDE := Vector2i(4096, 2560)   # BV2F-PT: the pilot plate
const ATLAS := 8192

var out_dir := ""
var vp: SubViewport
var scene


func _lit_shader() -> Shader:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_back, fog_disabled;
uniform float e0 = 0.47;
uniform float e1 = 0.90;
uniform float m0 = 0.10;
uniform float m1 = 0.60;
uniform float m2 = 1.00;
uniform float soft = 0.075;
void fragment() { ALBEDO = vec3(1.0); ROUGHNESS = 1.0; }
void light() {
	float ndl = dot(normalize(NORMAL), normalize(LIGHT));
	float t = (ndl * 0.5 + 0.5) * ATTENUATION;
	float b = m0 + smoothstep(e0 - soft, e0 + soft, t) * (m1 - m0) + smoothstep(e1 - soft, e1 + soft, t) * (m2 - m1);
	DIFFUSE_LIGHT += vec3(clamp((b - m0) / (m2 - m0), 0.0, 1.0), ATTENUATION, clamp(ndl, 0.0, 1.0));
}
"""
	return sh


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	if out_dir == "":
		print("[light] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = GUIDE
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/bv2f_pilot.tscn").instantiate()   # BV2F-PT
	scene.skip_character = true
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[light] HALT: the scene never finished building")
		quit(3)
		return
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	scene.set_markers(false)
	scene.post_q.visible = false
	for ink in scene._prop_inks:
		(ink as MeshInstance3D).visible = false
	var env: Environment = scene.env_node.environment
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.glow_enabled = false
	env.adjustment_enabled = false
	env.fog_enabled = false
	env.volumetric_fog_enabled = false
	env.ssao_enabled = false
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0)
	var m := ShaderMaterial.new()
	m.shader = _lit_shader()
	var n := 0
	for top in [scene.level, scene.props_root]:
		for mi in (top as Node).find_children("*", "MeshInstance3D", true, false):
			var x := mi as MeshInstance3D
			if x.mesh == null or String(x.name).ends_with("_ink") or not x.is_visible_in_tree():
				continue
			x.material_override = m
			n += 1
	RenderingServer.directional_shadow_atlas_set_size(ATLAS, true)
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	scene.park_camera(scene.uv_to_world(float(gc[0]), float(gc[1])), 1.0)
	for i in 8:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	img.save_png(out_dir.path_join("lit_guide.png"))
	var sun: DirectionalLight3D = scene.sun
	var info := {"px": [img.get_width(), img.get_height()], "meshes_relit": n, "shadow_atlas_px": ATLAS,
		"msaa": "4x", "sun": {"shadow_blur": sun.shadow_blur, "shadow_bias": sun.shadow_bias,
		"shadow_normal_bias": sun.shadow_normal_bias, "max_distance": sun.directional_shadow_max_distance},
		"encoding": "8-bit sRGB of the linear values written (decode before use)",
		"channels": {"R": "direct-sun share through the guide's ramp", "G": "cast shadow (ATTENUATION)", "B": "N.L"}}
	var f := FileAccess.open(out_dir.path_join("lit_guide.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(info, " "))
	f.close()
	print("[light] " + JSON.stringify(info))
	quit(0)
