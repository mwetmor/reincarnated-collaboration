extends SceneTree
## BV2F PT (R-C9-314): DEV-5 BOBBING-FLOE COST -- N free floes in open water, each bobbing on its own phase with its
## shape kept, drawn three ways with the REAL floe shader (pt_water.gd floe_shader_code: v1's painted shader + FLOE_BOB):
##   per_mat  : one MeshInstance3D + one ShaderMaterial per floe (DEV-5 as built: the phase a material uniform)
##   instance : one MeshInstance3D per floe, ONE shared material, the phase an `instance uniform`
##   merged   : ALL floes in ONE mesh, the phase per vertex (CUSTOM0.x) -- one draw call
## Floes: irregular 24-gon slabs 1.5-4 m across, 0.3 m thick (~92 tris), scattered over a 60 x 40 m sea at the play
## camera (orthographic, pitch 52.95, yaw 47, 1920 x 1080). vsync off; 120 warm frames then 600 timed.
##   Godot --path . --resolution 1920x1080 --script res://tools/bv2f/pt_floe_bench.gd -- <mode> <N> <OUT.json>
const PT_WATER := preload("res://scripts/bv2f/pt_water.gd")

func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	_run(a[0], int(a[1]), a[2])

func _floe(rng: RandomNumberGenerator, phase: float, merged: bool) -> Dictionary:
	var r0 := rng.randf_range(0.75, 2.0)
	var n := 24
	var top := PackedVector3Array(); var rad := []
	for i in n:
		var t := TAU * float(i) / float(n)
		var r := r0 * rng.randf_range(0.7, 1.15)
		top.append(Vector3(cos(t) * r, 0.15, sin(t) * r))
	var V := PackedVector3Array(); var N := PackedVector3Array(); var CU := PackedFloat32Array()
	var add := func(p: Vector3, nn: Vector3):
		V.append(p); N.append(nn)
		CU.append_array(PackedFloat32Array([phase, 0.0, 0.0, 0.0]))
	for i in n:
		var j := (i + 1) % n
		add.call(Vector3(0, 0.15, 0), Vector3.UP); add.call(top[i], Vector3.UP); add.call(top[j], Vector3.UP)
		var b0 := Vector3(top[i].x, -0.15, top[i].z); var b1 := Vector3(top[j].x, -0.15, top[j].z)
		var sn := (top[j] - top[i]).cross(Vector3.DOWN).normalized()
		add.call(top[i], sn); add.call(b0, sn); add.call(top[j], sn)
		add.call(top[j], sn); add.call(b0, sn); add.call(b1, sn)
	return {"v": V, "n": N, "c": CU}

func _mesh(parts: Array, with_custom: bool, offsets: Array) -> ArrayMesh:
	var V := PackedVector3Array(); var N := PackedVector3Array(); var CU := PackedFloat32Array()
	for k in parts.size():
		var p: Dictionary = parts[k]
		for v in (p["v"] as PackedVector3Array):
			V.append(v + (offsets[k] as Vector3))
		N.append_array(p["n"]); CU.append_array(p["c"])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = V; arr[Mesh.ARRAY_NORMAL] = N
	var flags := 0
	if with_custom:
		arr[Mesh.ARRAY_CUSTOM0] = CU
		flags = Mesh.ARRAY_CUSTOM_RGBA_FLOAT << Mesh.ARRAY_FORMAT_CUSTOM0_SHIFT
	var m := ArrayMesh.new()
	m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr, [], {}, flags)
	return m

func _run(mode: String, nfl: int, out: String) -> void:
	var rng := RandomNumberGenerator.new(); rng.seed = 314
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 1080.0 / 100.617553710938
	root.add_child(cam)
	cam.rotation_degrees = Vector3(-52.95354112560294, 47.0, 0.0)
	cam.position = Vector3(0, 0, 0) - cam.global_transform.basis.z * -60.0
	cam.look_at_from_position(cam.global_transform.basis.z * 60.0, Vector3.ZERO)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-55, -30, 0); root.add_child(sun)
	var base := PT_WATER.floe_shader_code()
	var code := base
	if mode == "instance":
		code = base.replace("uniform float bob_phase = 0.0;", "instance uniform float bob_phase = 0.0;")
	elif mode == "merged":
		code = base.replace("float ph = bob_phase * 6.2831;", "float ph = CUSTOM0.x * 6.2831;")
	var sh := Shader.new(); sh.code = code
	var shared := ShaderMaterial.new(); shared.shader = sh
	var parts := []; var offs := []
	for i in nfl:
		var ph := fposmod(float(i) * 0.6180339, 1.0)
		parts.append(_floe(rng, ph, mode == "merged"))
		offs.append(Vector3(rng.randf_range(-12, 12), 0.0, rng.randf_range(-9, 9)))
	var draws := 0
	if mode == "merged":
		var mi := MeshInstance3D.new(); mi.mesh = _mesh(parts, true, offs); mi.material_override = shared; root.add_child(mi); draws = 1
	else:
		for i in nfl:
			var mi := MeshInstance3D.new(); mi.mesh = _mesh([parts[i]], false, [Vector3.ZERO]); mi.position = offs[i]
			if mode == "per_mat":
				var m := ShaderMaterial.new(); m.shader = sh; m.set_shader_parameter("bob_phase", fposmod(float(i) * 0.6180339, 1.0)); mi.material_override = m
			else:
				mi.material_override = shared; mi.set_instance_shader_parameter("bob_phase", fposmod(float(i) * 0.6180339, 1.0))
			root.add_child(mi)
		draws = nfl
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	for i in 120:
		await process_frame
	var t := PackedFloat64Array(); var tp := Time.get_ticks_usec()
	for i in 600:
		await process_frame
		var tq := Time.get_ticks_usec(); t.append(float(tq - tp) / 1000.0); tp = tq
	var s := Array(t); s.sort()
	var rep := {"mode": mode, "floes": nfl, "draw_objects": draws, "p50_ms": s[300], "p99_ms": s[594], "max_ms": s[599],
				"render_draw_calls": Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),
				"prims": Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)}
	var f := FileAccess.open(out, FileAccess.WRITE); f.store_string(JSON.stringify(rep)); f.close()
	print("[floe_bench] ", JSON.stringify(rep))
	quit(0)
