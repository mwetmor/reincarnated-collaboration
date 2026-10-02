# EN-E3 Godot check: load the shipped GLB AT RUNTIME (GLTFDocument, no import step, nothing written into any project),
# verify the skin, the clips and the EMBEDDED texture, then render the game camera (ortho, 52.95 deg) at chosen clip times.
# env: EN3_GLB=<abs glb>  EN3_OUT=<abs png prefix>  EN3_SHOTS="clip:time,clip:time"
extends Node3D
func _ready():
	var path = OS.get_environment("EN3_GLB"); var out = OS.get_environment("EN3_OUT")
	var doc = GLTFDocument.new(); var st = GLTFState.new()
	var err = doc.append_from_file(path, st)
	if err != OK:
		print("[chk] LOAD FAIL ", err); get_tree().quit(2); return
	var scene = doc.generate_scene(st); add_child(scene)
	var ap: AnimationPlayer = scene.find_child("AnimationPlayer", true, false)
	var sk: Skeleton3D = scene.find_child("*", true, false) as Skeleton3D
	for n in scene.find_children("*", "Skeleton3D", true, false): sk = n
	var meshes = scene.find_children("*", "MeshInstance3D", true, false)
	print("[chk] glb ", path.get_file(), " skeleton bones ", sk.get_bone_count() if sk else -1, " meshes ", meshes.size())
	var tex_ok = true
	for m in meshes:
		var mi: MeshInstance3D = m
		for s in range(mi.mesh.get_surface_count()):
			var mat = mi.mesh.surface_get_material(s)
			var t = mat.albedo_texture if mat is StandardMaterial3D else null
			print("[chk] surface ", s, " material ", mat.resource_name if mat else "none", " albedo_texture ", (str(t.get_width()) + "x" + str(t.get_height())) if t else "NONE", " skin ", mi.skin != null)
			if s == 0 and t == null: tex_ok = false
	if ap:
		for a in ap.get_animation_list():
			var an = ap.get_animation(a)
			print("[chk] anim ", a, " length ", snapped(an.length, 0.0001), " tracks ", an.get_track_count())
	print("[chk] texture_embedded ", tex_ok)
	# EN3_SOCK = "bone,along,lx,ly,lz": the socket at REST, computed the renderer's way (bone global rest origin + along x basis.y + local)
	if OS.get_environment("EN3_SOCK") != "" and sk:
		var a = OS.get_environment("EN3_SOCK").split(",")
		var g: Transform3D = sk.global_transform * sk.get_bone_global_rest(sk.find_bone(a[0]))
		var p = g.origin + g.basis.y.normalized() * float(a[1]) + g.basis.x.normalized() * float(a[2]) + g.basis.y.normalized() * float(a[3]) + g.basis.z.normalized() * float(a[4])
		print("[chk] socket_rest_world ", p)
	var cam = Camera3D.new(); add_child(cam); cam.projection = Camera3D.PROJECTION_ORTHOGONAL; cam.size = 3.6
	var el = deg_to_rad(52.9535411256029); var aim = Vector3(0, 0.45, 0)
	cam.position = aim + Vector3(0, sin(el), cos(el)) * 20.0; cam.look_at(aim, Vector3.UP); cam.current = true
	var sun = DirectionalLight3D.new(); add_child(sun); sun.rotation_degrees = Vector3(-50, -40, 0); sun.light_energy = 1.2
	var env = WorldEnvironment.new(); var e = Environment.new(); e.background_mode = Environment.BG_COLOR; e.background_color = Color(0.86, 0.83, 0.77)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; e.ambient_light_color = Color(1, 1, 1); e.ambient_light_energy = 0.9; env.environment = e; add_child(env)
	var shots = OS.get_environment("EN3_SHOTS").split(",")
	var i = 0
	for sh in shots:
		var p = sh.split(":")
		if ap and p.size() == 2:
			ap.play(p[0]); ap.seek(float(p[1]), true); ap.pause()
		scene.rotation_degrees.y = 45.0 * (i % 8) * 0.0 + 35.0
		await get_tree().process_frame; await get_tree().process_frame; await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png(out + "_%02d.png" % i)
		print("[chk] shot ", sh, " -> ", out + "_%02d.png" % i); i += 1
	get_tree().quit(0)
