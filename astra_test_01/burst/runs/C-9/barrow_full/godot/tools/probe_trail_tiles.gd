extends SceneTree
## C-9 -- THE TILED TRAIL MAP SAMPLES WHAT THE SINGLE MAP SAMPLED (snow_field.gd, the cast-start fix).
##   Godot --path godot --script tools/probe_trail_tiles.gd -- [--px 1024] [--half]
## A trail buffer of random values; the OLD texture (one RGBAF ImageTexture, clamped, bilinear) and
## the NEW one (SnowField's own tile builder -> Texture2DArray, sampled by the trail_at() in
## SnowField.SHADER) are sampled at the same uv by one canvas shader, 1600^2 samples at sub-texel
## steps across every tile border and the map's edges; the difference is written x 4096 into a
## float target and read back.

var px := 1024
var half := false


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--px" and i + 1 < args.size():
			px = int(args[i + 1])
		elif args[i] == "--half":
			half = true
	var sf := SnowField.new()
	sf.trail_px = px
	sf.half_float_textures = half
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	sf._trail_buf = PackedFloat32Array()
	sf._trail_buf.resize(px * px * 4)
	for k in px * px * 4:
		sf._trail_buf[k] = rng.randf()
	sf._trail_tile_px = SnowField.TRAIL_TILE_PX if px % SnowField.TRAIL_TILE_PX == 0 else px
	sf._trail_tiles_n = px / sf._trail_tile_px
	var tiles: Array[Image] = []
	for ty in sf._trail_tiles_n:
		for tx in sf._trail_tiles_n:
			tiles.append(sf._trail_tile_image(tx, ty))
	var arr := Texture2DArray.new()
	arr.create_from_images(tiles)
	var one := ImageTexture.create_from_image(sf._gpu_image(px, sf._trail_buf))
	var S := 1600
	var vp := SubViewport.new()
	vp.size = Vector2i(S, S)
	vp.use_hdr_2d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var cr := ColorRect.new()
	cr.size = Vector2(S, S)
	var sh := Shader.new()
	var i := SnowField.SHADER.find("vec4 trail_at(vec2 uv) {")
	var j := SnowField.SHADER.find("}", i)
	sh.code = """shader_type canvas_item;
uniform sampler2D one : filter_linear, repeat_disable;
uniform sampler2DArray trail_tex : filter_linear, repeat_disable;
uniform float trail_tiles_n;
uniform float trail_tile_px;
""" + SnowField.SHADER.substr(i, j - i + 1) + """
void fragment() {
	// sub-texel sweep, a little past both edges of the map
	vec2 uv = UV * 1.02 - 0.01;
	vec4 d = abs(texture(one, uv) - trail_at(uv));
	COLOR = vec4(d.rgb * 4096.0, 1.0 + d.a * 4096.0);
}
"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("one", one)
	m.set_shader_parameter("trail_tex", arr)
	m.set_shader_parameter("trail_tiles_n", float(sf._trail_tiles_n))
	m.set_shader_parameter("trail_tile_px", float(sf._trail_tile_px))
	cr.material = m
	vp.add_child(cr)
	for f in 4:
		await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	img.convert(Image.FORMAT_RGBAF)
	var mx := 0.0
	var sum := 0.0
	var n := 0
	for y in range(0, S, 2):
		for x in range(0, S, 2):
			var c := img.get_pixel(x, y)
			var v := maxf(maxf(c.r, c.g), maxf(c.b, c.a - 1.0)) / 4096.0
			mx = maxf(mx, v)
			sum += v
			n += 1
	print("[probe_trail_tiles] px=%d half=%s tiles=%dx%d of %d: max |old - new| = %.6f, mean %.8f over %d samples" % [
		px, half, sf._trail_tiles_n, sf._trail_tiles_n, sf._trail_tile_px, mx, sum / float(n), n])
	sf.free()
	quit(0)
