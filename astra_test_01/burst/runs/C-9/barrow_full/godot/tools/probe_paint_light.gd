extends SceneTree
## C-9 T10-2 step 4: THE TWO QUESTIONS THE PAINTED LIGHT RESTS ON, measured before anything is
## built on them. drax.
##
##   Godot --path godot --resolution 640x360 --script tools/probe_paint_light.gd -- --out FILE.json
##   (the phone's renderer: add --rendering-method gl_compatibility --rendering-driver opengl3_angle
##    before --script; the mark-channel half is skipped there -- Compatibility has no such buffer)
##
## 1. LIGHT LAYERS. Can one sun light the painted world with ONLY HIS shadow in it, while a second,
##    identical sun lights him with EVERY caster's shadow in it? Two directional lights, one
##    direction: light A (red) lights layer 1 (him) with casters on layers 1|2; light B (green)
##    lights layer 2 (the painted world) with casters on layer 1 only. A receiver that outputs
##    ATTENUATION per light, per channel, says which shadows reached it and from which light.
## 2. THE PEN'S MARK CHANNEL. The screen-space pen reads ROUGHNESS back from the normal-roughness
##    buffer to tell him, thin growth and snow apart. A new mark for painted pieces needs the
##    channel's real encoding: quads write 0.0 .. 1.0 (one of them moving every frame, in case the
##    renderer tags moving instances), and a full-screen pass reads the buffer back.

const W := 640
const H := 320

var out_file := ""
var vp: SubViewport


func _recv_shader() -> Shader:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_disabled, fog_disabled;
void fragment() { ALBEDO = vec3(1.0); }
void light() { DIFFUSE_LIGHT += (LIGHT_COLOR / PI) * ATTENUATION * 0.5; }
"""
	return sh


func _mark_shader() -> Shader:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, specular_disabled, cull_disabled;
uniform float mark = 1.0;
void fragment() { ALBEDO = vec3(0.5); ROUGHNESS = mark; }
"""
	return sh


func _read_shader() -> Shader:
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, depth_draw_never, depth_test_disabled, cull_disabled, fog_disabled, shadows_disabled;
uniform sampler2D nrm_tex : hint_normal_roughness_texture, filter_nearest;
void vertex() { POSITION = vec4(VERTEX.xy * 2.0, 1.0, 1.0); }
void fragment() { ALBEDO = vec3(texture(nrm_tex, SCREEN_UV).a); }
"""
	return sh


func _box(parent: Node3D, pos: Vector3, size: Vector3, mat: Material, layer: int) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	mi.material_override = mat
	mi.layers = layer
	mi.position = pos
	parent.add_child(mi)
	return mi


func _px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_file = args[i + 1]
	vp = SubViewport.new()
	vp.size = Vector2i(W, H)
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var world := Node3D.new()
	vp.add_child(world)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(0, 0, 0)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color(0, 0, 0)
	env.environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	world.add_child(env)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_WIDTH
	cam.size = 20.0
	world.add_child(cam)
	cam.look_at_from_position(Vector3(0, 30, 0), Vector3.ZERO, Vector3(0, 0, -1))
	cam.current = true
	var result := {"godot": Engine.get_version_info()["string"],
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name()}
	result["light3d_has_shadow_caster_mask"] = "shadow_caster_mask" in DirectionalLight3D.new()

	# ---- 1. light layers ----
	var recv := ShaderMaterial.new()
	recv.shader = _recv_shader()
	var mag := StandardMaterial3D.new()
	mag.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mag.albedo_color = Color(1, 0, 1)
	# painted receiver (layer 2) on the left, dynamic receiver (layer 1) on the right
	_box(world, Vector3(-5, -0.05, 0), Vector3(10, 0.1, 8), recv, 2)
	_box(world, Vector3(5, -0.05, 0), Vector3(10, 0.1, 8), recv, 1)
	# casters, hovering, their shadows thrown 2.5 m toward +z by the tilted sun
	_box(world, Vector3(-7.5, 2.5, -2.5), Vector3(1.2, 0.3, 1.2), mag, 2)   # STATIC over painted
	_box(world, Vector3(-2.5, 2.5, -2.5), Vector3(1.2, 0.3, 1.2), mag, 1)   # HIM over painted
	_box(world, Vector3(2.5, 2.5, -2.5), Vector3(1.2, 0.3, 1.2), mag, 2)    # STATIC over dynamic
	_box(world, Vector3(7.5, 2.5, -2.5), Vector3(1.2, 0.3, 1.2), mag, 1)    # HIM over dynamic
	# a lit "him" block standing on the dynamic side: which lights reach it?
	_box(world, Vector3(5.0, 0.5, 2.5), Vector3(1.0, 1.0, 1.0), recv, 1)
	var dir := Vector3(0.0, -1.0, 1.0).normalized()          # the light travels down and to +z
	var la := DirectionalLight3D.new()
	la.light_color = Color(1, 0, 0)
	la.shadow_enabled = true
	la.light_cull_mask = 1
	la.set("shadow_caster_mask", 1 | 2)
	world.add_child(la)
	la.look_at_from_position(Vector3.ZERO, dir, Vector3(1, 0, 0))
	var lb := DirectionalLight3D.new()
	lb.light_color = Color(0, 1, 0)
	lb.shadow_enabled = true
	lb.light_cull_mask = 2
	lb.set("shadow_caster_mask", 1)
	world.add_child(lb)
	lb.look_at_from_position(Vector3.ZERO, dir, Vector3(1, 0, 0))
	for i in 8:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	img.convert(Image.FORMAT_RGBF)
	var to_px := func(p: Vector3) -> Vector2i:
		var s := cam.unproject_position(p)
		return Vector2i(int(s.x), int(s.y))
	var probes := {
		"painted_open": Vector3(-5.0, 0.0, 2.8),
		"painted_under_STATIC_shadow": Vector3(-7.5, 0.0, 0.0),
		"painted_under_HIM_shadow": Vector3(-2.5, 0.0, 0.0),
		"dynamic_open": Vector3(5.0, 0.0, -3.5),
		"dynamic_under_STATIC_shadow": Vector3(2.5, 0.0, 0.0),
		"dynamic_under_HIM_shadow": Vector3(7.5, 0.0, 0.0),
		"him_block_top": Vector3(5.0, 1.0, 2.5),
	}
	var lay := {}
	for k in probes:
		var q: Vector2i = to_px.call(probes[k])
		lay[k] = {"px": [q.x, q.y], "rgb_linear": _px(img, q.x, q.y)}
	result["light_layers"] = {"A_red": "lights layer 1 (him), casters 1|2", "B_green": "lights layer 2 (painted), casters 1 only",
		"receiver_writes": "per light (LIGHT_COLOR/PI) * ATTENUATION * 0.5: an unshadowed light = 0.5 in its channel",
		"probes": lay}
	img.save_png(out_file.get_basename() + "_layers.png")

	# ---- 2. the mark channel (Forward+ only: Compatibility has no normal-roughness buffer) ----
	if RenderingServer.get_current_rendering_method() == "gl_compatibility":
		var fc := FileAccess.open(out_file, FileAccess.WRITE)
		fc.store_string(JSON.stringify(result, "  "))
		fc.close()
		print("[probe] " + JSON.stringify(result))
		quit(0)
		return
	for ch in world.get_children():
		if ch is MeshInstance3D or ch is DirectionalLight3D:
			ch.queue_free()
	await process_frame
	var marks := [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
	var quads := []
	for i in marks.size():
		var m := ShaderMaterial.new()
		m.shader = _mark_shader()
		m.set_shader_parameter("mark", marks[i])
		quads.append(_box(world, Vector3(-8.0 + 3.2 * i, 0.0, -2.0), Vector3(2.4, 0.1, 2.4), m, 1))
	var mm := ShaderMaterial.new()
	mm.shader = _mark_shader()
	mm.set_shader_parameter("mark", 0.5)
	var mover := _box(world, Vector3(0.0, 0.0, 2.5), Vector3(2.4, 0.1, 2.4), mm, 1)
	var rd := ShaderMaterial.new()
	rd.shader = _read_shader()
	rd.render_priority = 100
	var q := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(1, 1)
	q.mesh = qm
	q.material_override = rd
	q.extra_cull_margin = 16384.0
	cam.add_child(q)
	q.position = Vector3(0, 0, -1)
	for i in 8:
		mover.position.x = 0.02 * float(i)
		await process_frame
	await RenderingServer.frame_post_draw
	var img2 := vp.get_texture().get_image()
	img2.convert(Image.FORMAT_RGBF)
	var mk := {}
	for i in marks.size():
		var p: Vector2i = to_px.call(Vector3(-8.0 + 3.2 * i, 0.05, -2.0))
		mk["%.2f" % marks[i]] = _px(img2, p.x, p.y)[0]
	var pm: Vector2i = to_px.call(mover.position + Vector3(0, 0.05, 0))
	mk["0.50_moving"] = _px(img2, pm.x, pm.y)[0]
	result["mark_channel"] = {"written_roughness -> read_back (the alpha of hint_normal_roughness_texture)": mk}
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify(result, "  "))
	f.close()
	print("[probe] " + JSON.stringify(result))
	quit(0)
