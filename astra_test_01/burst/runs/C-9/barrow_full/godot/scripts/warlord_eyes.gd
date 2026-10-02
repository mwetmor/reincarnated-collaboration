extends Node
## C-9 R-C9-121 -- THE DARK KNIGHT'S EYE GLOW: runtime nodes, not in the GLB (E1 commit 677cc44a0; the reference is
## wl_e1/film_rt/gear_stills.gd _eyes() / _eye_flicker()). drax.
## A BoneAttachment3D on Head; per eye (data/slots/warlord_eyes.json, the Head bone's local frame) one 0.07 m quad:
## billboard, unshaded, ADDITIVE, depth-tested, no shadow; a radial alpha (sqrt falloff) with a hot near-white inner
## half; the colour by ?eye (violet #9e4dff, ice #59bfff); a slow breath and a faint 3.7 Hz flicker. One shared
## material, one texture, two quads -- built once at load.
const SOCKETS := "res://data/slots/warlord_eyes.json"
var mat: StandardMaterial3D
var nodes: Array = []
var colour := Color("9e4dff")
var _t := 0.0


func setup(skel: Skeleton3D, eye: String) -> void:
	colour = Color("59bfff") if eye == "ice" else Color("9e4dff")
	var E: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(SOCKETS))
	var img := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	for y in 64:
		for x in 64:
			var r := Vector2(x - 31.5, y - 31.5).length() / 31.5
			var a := sqrt(clampf(1.0 - r, 0.0, 1.0))
			var c := colour.lerp(Color(1, 0.97, 1), clampf(1.0 - r / 0.5, 0.0, 1.0))
			img.set_pixel(x, y, Color(c.r * a, c.g * a, c.b * a, a))
	mat = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	mat.billboard_keep_scale = true
	mat.albedo_texture = ImageTexture.create_from_image(img)
	mat.render_priority = PaintStack.AFTER_POST_PRIORITY
	var att := BoneAttachment3D.new()
	att.name = "Eyes"
	att.bone_name = String(E.get("bone", "Head"))
	skel.add_child(att)
	for k in (E["eyes"] as Dictionary):
		var p: Array = E["eyes"][k]["head_local"]
		var n := Node3D.new()
		n.name = String(k)
		n.position = Vector3(float(p[0]), float(p[1]), float(p[2]))
		att.add_child(n)
		var q := MeshInstance3D.new()
		q.material_override = mat
		q.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		n.add_child(q)
		nodes.append(q)
	await get_tree().process_frame
	for q in nodes:
		var qm := QuadMesh.new()
		var sc: float = (q as Node3D).global_transform.basis.get_scale().x
		qm.size = Vector2.ONE * float(E.get("sprite_size_m", 0.07)) / maxf(sc, 1e-6)
		(q as MeshInstance3D).mesh = qm


func _process(dt: float) -> void:
	_t += dt
	if mat == null:
		return
	var v := 1.0 - 0.15 * (0.5 + 0.5 * sin(TAU * 0.4 * _t)) - 0.04 * sin(TAU * 3.7 * _t)
	mat.albedo_color = Color(v, v, v, 1.0)
