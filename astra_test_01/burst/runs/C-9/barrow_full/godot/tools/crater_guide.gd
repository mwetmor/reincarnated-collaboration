extends SceneTree
## C-9 CRATER v4 (R-C9-109), layer 2's GUIDE -- the 3D crater rendered on the painted Barrow at the game camera. drax.
##   Godot --path godot --resolution 1920x1080 --script tools/crater_guide.gd -- --as-web --c sorceress \
##         --glb ABS.glb --heights ABS_heights.json --out DIR [--at x,z]
## The crater mesh (tools/crater_mesh.py) sits at a clear point of the snow, in a greybox CLAY lit by the
## painting's own sun (lambert + the painter's shadow colour), drawn over the snow (no depth test: the bowl goes
## below the snow's surface). Writes DIR/guide_full.png (the whole frame), DIR/guide.png (1536 x 1024 round the
## crater), and DIR/project.json: the crop's origin and the screen pixel of every grid vertex (for the
## projection bake, tools/crater_project.py).
const CLAY := """
shader_type spatial;
render_mode unshaded, blend_mix, depth_test_disabled, depth_draw_never, cull_disabled, shadows_disabled;
uniform vec3 sun_dir = vec3(0.5, 0.7, 0.5);
uniform vec3 clay : source_color = vec3(0.66, 0.63, 0.60);
uniform vec3 shade : source_color = vec3(0.34, 0.37, 0.56);
uniform sampler2D cracks : filter_linear;
varying vec3 v_n;
varying float v_a;
varying float v_h;
void vertex() { v_n = (MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz; v_a = COLOR.a; v_h = VERTEX.y; }
void fragment() {
	// a greybox CLAY for the painter: lit by the painting's sun, darker the deeper the bowl, the fault
	// lines drawn as dark grooves, the rim catching the light
	float l = clamp(dot(normalize(v_n), normalize(sun_dir)), 0.0, 1.0);
	vec3 c = mix(clay * mix(shade, vec3(1.0), 0.3), clay * 1.08, smoothstep(0.2, 0.8, l));
	c *= mix(0.55, 1.0, smoothstep(-0.2, 0.0, v_h));
	c = mix(c, vec3(1.0), smoothstep(0.04, 0.1, v_h) * 0.25);
	float k = texture(cracks, UV).r;
	c = mix(c, vec3(0.12, 0.1, 0.09), smoothstep(0.25, 0.7, k) * 0.85);
	ALBEDO = c;
	ALPHA = v_a;
}
"""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := String(args[args.find("--out") + 1])
	var glb := String(args[args.find("--glb") + 1])
	var hj := String(args[args.find("--heights") + 1])
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	# her at the cast spot, the camera settled on her; then she is hidden and the crater goes under the frame's
	# centre (the ground point the centre ray meets): the play camera's own framing, nobody in the guide
	scene.place_knight(-1.0, -0.5, "E")
	for f in 60:
		await process_frame
	scene.knight.visible = false
	var vp := root.get_visible_rect().size
	var ro: Vector3 = scene.cam.project_ray_origin(vp * 0.5)
	var rn: Vector3 = scene.cam.project_ray_normal(vp * 0.5)
	var at := ro + rn * ((0.05 - ro.y) / rn.y)
	if args.has("--at"):
		var p := String(args[args.find("--at") + 1]).split(",")
		at = Vector3(float(p[0]), 0.0, float(p[1]))
	at.y = scene.snow.surface_y(Vector2(at.x, at.z)) if scene.snow != null else 0.0
	if args.has("--at"):
		scene.park_camera(at, 1.0)          # R-C9-118: an ice or earth spot, at the play camera, centred
	var doc := GLTFDocument.new()
	var st := GLTFState.new()
	doc.append_from_file(glb, st)
	var node: Node3D = doc.generate_scene(st)
	scene.add_child(node)
	node.global_position = at
	var mat := ShaderMaterial.new()
	var sh := Shader.new()
	sh.code = CLAY
	mat.shader = sh
	mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	var to_sun: Vector3 = scene.meteor_fx._to_sun if scene.get("meteor_fx") != null else Vector3(0.5, 0.7, 0.5)
	mat.set_shader_parameter("sun_dir", to_sun)
	var cp := String(args[args.find("--cracks") + 1]) if args.has("--cracks") else ""
	if cp != "":
		mat.set_shader_parameter("cracks", ImageTexture.create_from_image(Image.load_from_file(cp)))
	var mis := node.find_children("*", "MeshInstance3D", true, false)
	for mi in mis:
		(mi as MeshInstance3D).material_override = mat
	for f in 20:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(out_dir.path_join("guide_full.png"))
	var c0: Vector2 = scene.cam.unproject_position(at)
	var cx := clampi(int(c0.x) - 768, 0, img.get_width() - 1536)
	var cy := clampi(int(c0.y) - 512, 0, img.get_height() - 1024)
	img.get_region(Rect2i(cx, cy, 1536, 1024)).save_png(out_dir.path_join("guide.png"))
	# every grid vertex's screen pixel, in the crop (the height field from the mesh builder, as JSON)
	var H: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(hj))
	var xs: Array = H["x"]
	var hh: Array = H["h"]
	var n := xs.size()
	var px := PackedFloat32Array()
	px.resize(n * n * 2)
	for j in n:
		for i in n:
			# Blender (x, y, z up) -> Godot (x, z up, -y)
			var w := at + Vector3(float(xs[i]), float((hh[j] as Array)[i]), -float(xs[j]))
			var s: Vector2 = scene.cam.unproject_position(w)
			px[(j * n + i) * 2] = s.x - cx
			px[(j * n + i) * 2 + 1] = s.y - cy
	var f2 := FileAccess.open(out_dir.path_join("project.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify({"at": [at.x, at.y, at.z], "crop_origin": [cx, cy], "crop": [1536, 1024], "n": n,
		"frame": [img.get_width(), img.get_height()], "to_sun": [to_sun.x, to_sun.y, to_sun.z], "px": Array(px)}))
	f2.close()
	print("[crater_guide] at=%s crop=(%d,%d) -> %s" % [at, cx, cy, out_dir])
	quit(0)
