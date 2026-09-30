extends SceneTree
## C-9 -- THE SHADER AUDIT (the conductor's ruling (b), audit only): every distinct shader the painted page
## compiles at load, grouped by the shader each material draws with (Material.get_shader_rid(): a
## StandardMaterial3D's generated shader is shared by every material with its features), with who uses it.
## Lane B's Meteor variants (compiled at load by its warm-up) are listed from MeteorFx._swaps.
##   Godot --path godot --rendering-method gl_compatibility --rendering-driver opengl3_angle --resolution 640x360 \
##         --script tools/audit_shaders.gd -- --as-web --c sorceress --out FILE.json
var out_file := ""
var groups := {}          # shader rid id -> {code_hash, kind, first_line, materials, users[]}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--out")
	out_file = String(args[i + 1]) if i >= 0 else "user://audit.json"
	var scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	var w := 0
	while not scene.ready_done and w < 4000:
		await process_frame
		w += 1
	for f in 120:
		await process_frame
	var mats := {}
	for n in scene.find_children("*", "Node", true, false):
		_scan(n, mats)
	var mfx = scene.get("meteor_fx")
	var lane_b := []
	if mfx != null:
		var seen := {}
		for s in mfx._swaps:
			var fx: Shader = s["fx"]
			if not seen.has(fx):
				seen[fx] = true
				lane_b.append({"kind": String(s["kind"]), "code_hash": fx.code.hash(), "lines": fx.code.count("\n")})
	var rows := []
	for k in groups:
		var g: Dictionary = groups[k]
		g["materials"] = (g["mats"] as Dictionary).size()
		g["shader_resources"] = (g["resources"] as Dictionary).size()
		g.erase("mats")
		g.erase("resources")
		g["users"] = (g["users"] as Array).slice(0, 6)
		rows.append(g)
	rows.sort_custom(func(a, b): return int(a["materials"]) > int(b["materials"]))
	var by_code := {}
	for r in rows:
		by_code[int(r["code_hash"])] = int(by_code.get(int(r["code_hash"]), 0)) + 1
	var dup := 0
	for h in by_code:
		if int(by_code[h]) > 1:
			dup += int(by_code[h]) - 1
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify({"who": scene.who, "renderer": RenderingServer.get_current_rendering_method(),
		"distinct_shaders_drawn": rows.size(), "same_code_compiled_twice": dup, "lane_b_variants": lane_b,
		"shaders": rows}, " "))
	f.close()
	print("[audit] who=%s shaders=%d same-code duplicates=%d lane_b_variants=%d -> %s" % [scene.who, rows.size(), dup, lane_b.size(), out_file])
	quit(0)


func _add(m: Material, user: String, mats: Dictionary) -> void:
	if m == null:
		return
	var key := ""
	var code := ""
	var kind := m.get_class()
	if m is ShaderMaterial:
		var sh: Shader = (m as ShaderMaterial).shader
		if sh == null:
			return
		code = sh.code
		key = "S%d" % code.hash()          # the same CODE is the same program, whichever Shader resource holds it
	else:
		# a BaseMaterial3D's generated shader is shared by every material with the same FEATURES: key on
		# its enum/bool properties and which texture slots are filled (values and colours are uniforms)
		var sig := []
		for pr in m.get_property_list():
			var t := int(pr["type"])
			var nm := String(pr["name"])
			if (t == TYPE_BOOL or t == TYPE_INT) and not nm.begins_with("resource_") and nm != "render_priority":
				sig.append("%s=%s" % [nm, str(m.get(nm))])
			elif t == TYPE_OBJECT and nm.ends_with("_texture"):
				sig.append("%s=%s" % [nm, "1" if m.get(nm) != null else "0"])
		code = ",".join(PackedStringArray(sig))
		key = "B%d" % code.hash()
	if not groups.has(key):
		var first := ""
		for ln in code.split("\n"):
			var t2 := ln.strip_edges()
			if t2.begins_with("//") or t2.begins_with("render_mode"):
				first = t2.substr(0, 110)
				if t2.begins_with("render_mode"):
					break
		groups[key] = {"kind": kind, "code_hash": code.hash(), "lines": code.count("\n"), "first_line": first,
			"mats": {}, "users": [], "resources": {}}
	if m is ShaderMaterial:
		(groups[key]["resources"] as Dictionary)[(m as ShaderMaterial).shader.get_instance_id()] = true
	(groups[key]["mats"] as Dictionary)[m.get_instance_id()] = true
	if (groups[key]["users"] as Array).size() < 6 and not (groups[key]["users"] as Array).has(user):
		(groups[key]["users"] as Array).append(user)
	if m.next_pass != null:
		_add(m.next_pass, user + " (next_pass)", mats)


func _scan(n: Node, mats: Dictionary) -> void:
	var nm := "%s:%s" % [n.get_class(), n.name]
	# only what DRAWS: a hidden instance compiles nothing
	if n is Node3D and not (n as Node3D).is_visible_in_tree():
		return
	if n is CanvasItem and not (n as CanvasItem).is_visible_in_tree():
		return
	if n is GeometryInstance3D:
		var g := n as GeometryInstance3D
		_add(g.material_override, nm, mats)
		_add(g.material_overlay, nm + " (overlay)", mats)
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		var mi := n as MeshInstance3D
		for s in mi.mesh.get_surface_count():
			_add(mi.get_active_material(s), nm, mats)
	if n is MultiMeshInstance3D and (n as MultiMeshInstance3D).multimesh != null and (n as MultiMeshInstance3D).multimesh.mesh != null:
		var mm := (n as MultiMeshInstance3D).multimesh.mesh
		for s in mm.get_surface_count():
			_add(mm.surface_get_material(s), nm, mats)
	if n is GPUParticles3D:
		var p := n as GPUParticles3D
		_add(p.process_material, nm + " (process)", mats)
		if p.draw_pass_1 != null:
			for s in p.draw_pass_1.get_surface_count():
				_add(p.draw_pass_1.surface_get_material(s), nm + " (draw)", mats)
	if n is CanvasItem:
		_add((n as CanvasItem).material, nm, mats)
