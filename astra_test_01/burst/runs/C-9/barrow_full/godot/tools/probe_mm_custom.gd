extends SceneTree
## C-9 T10-2 phone page: DOES THE PHONE'S RENDERER HAND A MULTIMESH ITS INSTANCE_CUSTOM? drax.
##
##   Godot --path godot [--rendering-method gl_compatibility --rendering-driver opengl3_angle] \
##         --resolution 640x360 --script tools/probe_mm_custom.gd -- --out FILE.json
##
## The painted heather's per-spray colour rides in INSTANCE_CUSTOM (the painting beneath each
## spray). On Compatibility every spray came out black. Three quads, one MultiMesh, custom data
## (1, 0, 0), (0, 1, 0), (0, 0, 1): unshaded they must read red, green, blue; the same under a
## lit shader with a directional light and no ambient says whether the light reaches them.

const W := 480
const H := 160
var out_file := ""


func _mm(shader_code: String, layer: int) -> MultiMeshInstance3D:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_custom_data = true
	var q := QuadMesh.new()
	q.size = Vector2(2.4, 2.4)
	mm.mesh = q
	mm.instance_count = 3
	for i in 3:
		mm.set_instance_transform(i, Transform3D(Basis(), Vector3(-3.0 + 3.0 * i, 0.0, 0.0)))
		mm.set_instance_custom_data(i, Color(1.0 if i == 0 else 0.0, 1.0 if i == 1 else 0.0, 1.0 if i == 2 else 0.0, 1.0))
	var mi := MultiMeshInstance3D.new()
	mi.multimesh = mm
	var m := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = shader_code
	m.shader = sh
	mi.material_override = m
	mi.layers = layer
	return mi


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_file = args[i + 1]
	var vp := SubViewport.new()
	vp.size = Vector2i(W, H)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var w := Node3D.new()
	vp.add_child(w)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(0, 0, 0)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color(0, 0, 0)
	env.environment.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	w.add_child(env)
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_WIDTH
	cam.size = 9.0
	w.add_child(cam)
	cam.position = Vector3(0, 0, 10)
	cam.current = true
	var res := {"rendering_method": RenderingServer.get_current_rendering_method()}
	var unshaded := """
shader_type spatial;
render_mode unshaded, cull_disabled;
varying vec3 v_c;
void vertex() { v_c = INSTANCE_CUSTOM.rgb; }
void fragment() { ALBEDO = v_c; }
"""
	var lit := """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_disabled;
varying vec3 v_c;
void vertex() { v_c = INSTANCE_CUSTOM.rgb; }
void fragment() { ALBEDO = vec3(1.0); }
void light() { DIFFUSE_LIGHT += v_c * ATTENUATION; }
"""
	var a := _mm(unshaded, 1)
	w.add_child(a)
	await process_frame
	for i in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	res["unshaded_custom_rgb_at_quads"] = [_px(img, 80), _px(img, 240), _px(img, 400)]
	a.queue_free()
	var b := _mm(lit, 2048)
	w.add_child(b)
	var l := DirectionalLight3D.new()
	l.shadow_enabled = true
	l.light_cull_mask = 2048
	w.add_child(l)
	l.look_at_from_position(Vector3(0, 0, 5), Vector3.ZERO, Vector3.UP)
	for i in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	img = vp.get_texture().get_image()
	res["lit_custom_rgb_at_quads"] = [_px(img, 80), _px(img, 240), _px(img, 400)]
	# AND THE VERTEX COLOUR on a MultiMesh without instance colours (the sprays carry theirs per vertex)
	b.queue_free()
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(-1.2, -1.2, 0), Vector3(1.2, -1.2, 0), Vector3(1.2, 1.2, 0),
		Vector3(-1.2, -1.2, 0), Vector3(1.2, 1.2, 0), Vector3(-1.2, 1.2, 0)])
	arr[Mesh.ARRAY_NORMAL] = PackedVector3Array([Vector3.BACK, Vector3.BACK, Vector3.BACK, Vector3.BACK, Vector3.BACK, Vector3.BACK])
	var cc := Color(1.0, 0.5, 0.25)
	arr[Mesh.ARRAY_COLOR] = PackedColorArray([cc, cc, cc, cc, cc, cc])
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var c3 := _mm("""
shader_type spatial;
render_mode unshaded, cull_disabled;
varying vec3 v_c;
void vertex() { v_c = COLOR.rgb; }
void fragment() { ALBEDO = v_c; }
""", 1)
	c3.multimesh.mesh = am
	w.add_child(c3)
	for i in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	img = vp.get_texture().get_image()
	res["unshaded_vertex_color_1_0.5_0.25_at_quads"] = [_px(img, 80), _px(img, 240), _px(img, 400)]
	# THE FIX TO TEST: instance colours ON, every one white -- Compatibility then reads the vertex
	# colour times white, as Forward+ reads the vertex colour
	var mm2 := MultiMesh.new()
	mm2.transform_format = MultiMesh.TRANSFORM_3D
	mm2.use_custom_data = true
	mm2.use_colors = true
	mm2.mesh = am
	mm2.instance_count = 3
	for i in 3:
		mm2.set_instance_transform(i, Transform3D(Basis(), Vector3(-3.0 + 3.0 * i, 0.0, 0.0)))
		mm2.set_instance_color(i, Color(1, 1, 1, 1))
		mm2.set_instance_custom_data(i, Color(0.5, 0.5, 0.5, 1.0))
	c3.multimesh = mm2
	for i in 6:
		await process_frame
	await RenderingServer.frame_post_draw
	img = vp.get_texture().get_image()
	res["with_white_instance_colours_vertex_color_at_quads"] = [_px(img, 80), _px(img, 240), _px(img, 400)]
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify(res, " "))
	f.close()
	print("[probe_mm] " + JSON.stringify(res))
	quit(0)


func _px(img: Image, x: int) -> Array:
	var c := img.get_pixel(x, H / 2)
	return [snappedf(c.r, 0.01), snappedf(c.g, 0.01), snappedf(c.b, 0.01)]
