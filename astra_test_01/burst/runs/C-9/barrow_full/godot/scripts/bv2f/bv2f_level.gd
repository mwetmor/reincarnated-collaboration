extends "res://scripts/barrow_full.gd"
## BV2F lane LV, Phase 1.3 -- BARROW_V2 (layout v7b) AS A LEVEL OF THE V1 BARROW, the CLASS-TINTED GUIDE build.
##
## This EXTENDS v1's barrow_full.gd and inherits all of it unchanged: v1's camera (orthographic, pitch 52.95354, YAW 47),
## v1's one winter sun (55 deg up, screen azimuth 305), v1's pen (paint_stack post + the prop hull), his rig, the bounds
## walls, the capture API the frozen Tier-B tools call. It replaces only the PLACE -- read from data/bv2f/level.json
## (fid/lv/tools/bv2f_level_prep.py, from fid/lv/layout_v7b.json).
##
## THE FRAME FIX (DEV-4, R-C9-165): v1's Level node carries (u, v) as local (u, h, -v), and its local axes ARE barrow_v2's
## sim (x, z, y) rotated by the camera yaw: world = R_y(+47).(x, z, y) (fid/lv/frame.py, frame.gd). So everything here is
## built in the Level node's local frame with sim coordinates as they stand: u = x, v = -y.
##
## v1's GUIDE RECIPE: flat class tints through paint_stack's own world material (_flat_params: no mottle, hatch, wash,
## snow), models in flat tints (adopt_prop, use_tex off -- not their Tripo textures), v1's hull pen, NO PLANTS.
## v1's tint values for v1's classes; DEV-2 provisional tints for the new ones (level.json tints_srgb).
##
## Run a guide SECTION by env BV2F_SECTION=s00|s01|s10|s11 (the frame's guide_window is that section's).

## the layout VARIANT (data/bv2f/<variant>/): env BV2F_VARIANT, default v7c (R-C9-177)
var BV2F_DATA := "res://data/bv2f/" + (OS.get_environment("BV2F_VARIANT") if OS.get_environment("BV2F_VARIANT") != "" else "art") + "/"
var lvl := {}
var sim := {}
var class_meshes := {}
var _glb_cache := {}
var model_report := {"loaded": 0, "missing": []}
# R-C9-188/189: the terrain as the walk surface (floor_y_at + the HeightMapShape3D collider)
var _hf := PackedFloat32Array()
var _hf_rows := 0
var _hf_cols := 0
var _hf_ppm := 4.0
var _hf_x0 := 0.0
var _hf_y0 := 0.0


func _read_json(path: String) -> Dictionary:
	if path != LAYOUT_JSON:
		return super._read_json(path)
	var d := super._read_json(BV2F_DATA + "level.json")
	var sec := OS.get_environment("BV2F_SECTION")
	if sec != "":
		for s in d["frame"]["sections"]:
			if String(s["id"]) == sec:
				d["frame"]["guide_window"] = {"centre_uv": s["centre_uv"], "u": s["u"], "v": s["v"]}
	lvl = d
	sim = d["sim"]
	return d


func _S(x: float, z: float, y: float) -> Vector3:
	## sim (x east, y south, z up) -> the Level node's local frame
	return Vector3(x, z, y)


func _tint_of(cls: String) -> Color:
	return _tint.get(cls, _tint["primitive_grey"])


func _class_mat(cls: String) -> ShaderMaterial:
	var m := PaintStack.world_material(fbm, _tint_of(cls), _flat_params())
	world_mats.append(m)
	return m


var _groups := {}
var _cur_collider := ""


func _xf_to(root: Node3D, n: Node3D) -> Transform3D:
	## the transform of n relative to root's PARENT frame (root's own transform included)
	var t := Transform3D.IDENTITY
	var c: Node = n
	while c != null and c != root.get_parent():
		if c is Node3D:
			t = (c as Node3D).transform * t
		c = c.get_parent()
	return t


func _group(gid: String, cls: String) -> Node3D:
	## ONE id per slot / per blob class: v1's ID code (capture_ids, frozen) has 256 distinct colours (R = (i % 16) * 16 + 8,
	## G = (i / 16) * 16 + 8) -- instanced slots (181 palisade stakes) would overflow it
	if not _groups.has(gid):
		var g := Node3D.new()
		g.name = gid
		level.add_child(g)
		_groups[gid] = g
		_register(gid, g, cls, "group")
	return _groups[gid]


func _register(id: String, root: Node3D, cls: String, piece: String, uv_at = null) -> void:
	nodes[id] = root
	built[id] = {"class": cls, "piece": piece}
	(layout["placements"] as Array).append({"id": id, "kind": "bv2f", "class": cls, "piece": piece, "uv": uv_at})


# --- the ground: one mesh per class over the heightfield --------------------------------------
func _build_ground() -> void:
	report["ground"] = {"bv2f": true}
	var hf: Dictionary = sim["heightfield"]
	var H := FileAccess.get_file_as_bytes(BV2F_DATA + String(hf["file"])).to_float32_array()
	var hrows := int(hf["shape"][0])
	var hcols := int(hf["shape"][1])
	var hppm := float(hf["px_per_m"])
	var ex: Dictionary = hf["extent_sim_m"]
	var x0 := float(ex["x0"])
	var y0 := float(ex["y0"])
	var cp: Dictionary = sim["classes_png"]
	var img := Image.new()
	img.load_png_from_buffer(FileAccess.get_file_as_bytes(BV2F_DATA + String(cp["file"])))
	report["ground"]["classes_sha256_ok"] = FileAccess.get_sha256(BV2F_DATA + String(cp["file"])) == String(cp["sha256"])
	var W := img.get_width()
	var Hn := img.get_height()
	var cppm := float(cp["px_per_m"])
	var raw := img.get_data()
	var bpp := raw.size() / (W * Hn)
	var names: Array = lvl["classes"]
	# corner heights at the class grid (bilinear in the heightfield)
	var Z := PackedFloat32Array()
	Z.resize((W + 1) * (Hn + 1))
	for j in Hn + 1:
		var fy := (float(j) / cppm) * hppm
		var j0 := clampi(int(floor(fy)), 0, hrows - 2)
		var ty := clampf(fy - float(j0), 0.0, 1.0)
		for i in W + 1:
			var fx := (float(i) / cppm) * hppm
			var i0 := clampi(int(floor(fx)), 0, hcols - 2)
			var tx := clampf(fx - float(i0), 0.0, 1.0)
			var a := H[j0 * hcols + i0]
			var b := H[j0 * hcols + i0 + 1]
			var c := H[(j0 + 1) * hcols + i0]
			var d := H[(j0 + 1) * hcols + i0 + 1]
			Z[j * (W + 1) + i] = (a * (1.0 - tx) + b * tx) * (1.0 - ty) + (c * (1.0 - tx) + d * tx) * ty
	var V := {}
	var N := {}
	var step := 1.0 / cppm
	var smooth := bool((sim.get("route", {}) as Dictionary).get("heightfield_collider", false)) and not sim.has("stair_steps_legacy") and (sim.get("slabs", null) != null)
	for j in Hn:
		var i := 0
		while i < W:
			var k := int(raw[(j * W + i) * bpp])
			if k == 0:
				i += 1
				continue
			# run-length merge along the row while the class holds and the ground is flat (the floor is exactly 0)
			var i1 := i + 1
			var flat := Z[j * (W + 1) + i] == 0.0 and Z[(j + 1) * (W + 1) + i] == 0.0
			if flat:
				while i1 < W and int(raw[(j * W + i1) * bpp]) == k and Z[j * (W + 1) + i1] == 0.0 and Z[(j + 1) * (W + 1) + i1] == 0.0 \
						and Z[j * (W + 1) + i1 + 1] == 0.0 and Z[(j + 1) * (W + 1) + i1 + 1] == 0.0:
					i1 += 1
			if not V.has(k):
				V[k] = PackedVector3Array()
				N[k] = PackedVector3Array()
			var xa := x0 + float(i) * step
			var xb := x0 + float(i1) * step
			var ya := y0 + float(j) * step
			var yb := y0 + float(j + 1) * step
			var pa := _S(xa, Z[j * (W + 1) + i], ya)
			var pb := _S(xb, Z[j * (W + 1) + i1], ya)
			var pc := _S(xb, Z[(j + 1) * (W + 1) + i1], yb)
			var pd := _S(xa, Z[(j + 1) * (W + 1) + i], yb)
			var vv: PackedVector3Array = V[k]
			var nn: PackedVector3Array = N[k]
			vv.append_array(PackedVector3Array([pa, pb, pd, pb, pc, pd]))
			if smooth:
				# Phase 1'': SMOOTH vertex normals off the height grid (the clifftop ramps, the beach, the stream banks read as
				# slopes, not as the facets of 6 cm cells)
				var na := _gn(Z, W, Hn, i, j, step)
				var nb := _gn(Z, W, Hn, i1, j, step)
				var nc := _gn(Z, W, Hn, i1, j + 1, step)
				var nd := _gn(Z, W, Hn, i, j + 1, step)
				nn.append_array(PackedVector3Array([na, nb, nd, nb, nc, nd]))
			else:
				var n1 := (pd - pa).cross(pb - pa).normalized()
				var n2 := (pd - pb).cross(pc - pb).normalized()
				nn.append_array(PackedVector3Array([n1, n1, n1, n2, n2, n2]))
			V[k] = vv
			N[k] = nn
			i = i1
	var tris := {}
	for k in V:
		var cls := String(names[k])
		var root := Node3D.new()
		root.name = "ground_" + cls
		level.add_child(root)
		var arr := []
		arr.resize(Mesh.ARRAY_MAX)
		arr[Mesh.ARRAY_VERTEX] = V[k]
		arr[Mesh.ARRAY_NORMAL] = N[k]
		var am := ArrayMesh.new()
		am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
		var mi := MeshInstance3D.new()
		mi.name = "mesh"
		mi.mesh = am
		mi.material_override = _class_mat(cls)
		root.add_child(mi)
		class_meshes[cls] = mi
		_register("ground_" + cls, root, cls, "ground")
		tris[cls] = (V[k] as PackedVector3Array).size() / 3
	# the sea: one plane at the one sea level (R-C9-162(a): no lagoon)
	var sz := float(sim["sea_z"])
	var sroot := Node3D.new()
	sroot.name = "ground_sea"
	level.add_child(sroot)
	var SV := PackedVector3Array()
	var SN := PackedVector3Array()
	var e := 160.0
	_tri(SV, SN, _S(-e, sz, -e), _S(e, sz, -e), _S(e, sz, e), Vector3.UP)
	_tri(SV, SN, _S(-e, sz, -e), _S(e, sz, e), _S(-e, sz, e), Vector3.UP)
	_mesh(SV, SN, _class_mat("sea"), "mesh", sroot)
	_register("ground_sea", sroot, "sea", "ground")
	_hf = H
	_hf_rows = hrows
	_hf_cols = hcols
	_hf_ppm = hppm
	_hf_x0 = x0
	_hf_y0 = y0
	var body := _body(level, "FloorBody")
	var cs := CollisionShape3D.new()
	var RT: Dictionary = sim.get("route", {})
	if bool(RT.get("heightfield_collider", false)):
		# R-C9-188/189: SOUTH of v = hf_collider_v_max the walk surface IS the terrain -- a HeightMapShape3D of the same
		# heightfield the ground mesh is built from (cell 1/px_per_m m: scaled uniformly by that, heights pre-multiplied),
		# so the shelf, the cave floor, the stair's landing and the clifftop are walked where they are drawn. NORTH of
		# v = floor_box_v_min the floor stays v1's own box (top face at 0), cut in two at v = +9 so the box under the
		# start keeps its centre at the origin: the knight the frozen guide capture draws at the start stands exactly as he did.
		var vcut := float(RT["hf_collider_v_max"])
		var j0 := clampi(int(ceil((-vcut - y0) * hppm)), 0, hrows - 2)
		var rows := hrows - j0
		var hm := HeightMapShape3D.new()
		hm.map_width = hcols
		hm.map_depth = rows
		var hd := PackedFloat32Array()
		hd.resize(rows * hcols)
		for q in rows * hcols:
			hd[q] = H[j0 * hcols + q] * hppm
		hm.map_data = hd
		cs.shape = hm
		cs.scale = Vector3.ONE / hppm
		cs.position = _S(x0 + float(hcols - 1) / hppm / 2.0, 0.0, y0 + float(j0) / hppm + float(rows - 1) / hppm / 2.0)
		body.add_child(cs)
		var vb := float(RT["floor_box_v_min"])
		for bb in ([] if vb > 900.0 else [[vb, -vb], [-vb, 75.0]]):
			var c2 := CollisionShape3D.new()
			var b2 := BoxShape3D.new()
			b2.size = Vector3(150.0, 2.0, float(bb[1]) - float(bb[0]))
			c2.shape = b2
			c2.position = Vector3(0.0, -1.0, -(float(bb[0]) + float(bb[1])) / 2.0)
			body.add_child(c2)
		report["ground"]["collider"] = "v >= %.2f: v1's box floor (top 0); v <= %.2f: HeightMapShape3D %d x %d @ %.3f m" % [vb, vcut, hcols, rows, 1.0 / hppm]
		cs = null
	else:
		# the walkable floor's collider: ONE box, top face at y = 0 (v1's), over the whole site
		var bx := BoxShape3D.new()
		bx.size = Vector3(150.0, 2.0, 150.0)
		cs.shape = bx
		cs.position = Vector3(0.0, -1.0, 0.0)
	if cs != null:
		body.add_child(cs)
	report["ground"]["class_triangles"] = tris
	report["ground"]["sea_z"] = sz


func _build_mound() -> void:
	pass


func _build_overlay() -> void:
	pass


func _build_crucible() -> void:
	pass


func floor_y_at(u: float, v: float) -> float:
	## R-C9-188/189: the walk surface under (u, v) -- the terrain (bilinear, as the ground mesh), or the stair's ramp
	if _hf.is_empty():
		return 0.0
	var RT: Dictionary = sim.get("route", {})
	if not RT.has("floor_box_v_min") or v > (float(RT["floor_box_v_min"]) + float(RT["hf_collider_v_max"])) / 2.0:
		return 0.0                                   # v1's box floor (the knight's spawn as v1 placed him)
	var fx := (u - _hf_x0) * _hf_ppm
	var fy := (-v - _hf_y0) * _hf_ppm
	var i0 := clampi(int(floor(fx)), 0, _hf_cols - 2)
	var j0 := clampi(int(floor(fy)), 0, _hf_rows - 2)
	var tx := clampf(fx - float(i0), 0.0, 1.0)
	var ty := clampf(fy - float(j0), 0.0, 1.0)
	var z := (_hf[j0 * _hf_cols + i0] * (1.0 - tx) + _hf[j0 * _hf_cols + i0 + 1] * tx) * (1.0 - ty) \
		+ (_hf[(j0 + 1) * _hf_cols + i0] * (1.0 - tx) + _hf[(j0 + 1) * _hf_cols + i0 + 1] * tx) * ty
	for rt in (sim.get("route", {}) as Dictionary).get("walk_boxes", []):
		var d := Vector2(u - float(rt["c_sim"][0]), -v - float(rt["c_sim"][1]))
		var dir := Vector2(float(rt["dir_sim"][0]), float(rt["dir_sim"][1]))
		var al := d.dot(dir)
		var ac := d.dot(Vector2(-dir.y, dir.x))
		if absf(al) <= float(rt["along_h"]) / 2.0 and absf(ac) <= float(rt["across"]) / 2.0:
			z = maxf(z, float(rt["z_c"]) - al * tan(deg_to_rad(float(rt["pitch_deg"]))))
	return z


# --- the models (layout v7b's slots), in flat class tints -------------------------------------
func _load_glb(p: String) -> Node3D:
	## every GLB is a RAW copy in data/bv2f/ext/*.glb.bin (bv2f_level_prep.py): read by bytes, so the same code runs in the
	## editor project and in an exported app (an export ships include_filter files as themselves)
	if p == "" or p == "<null>":
		return null
	var path := "res://" + p
	if not FileAccess.file_exists(path):
		if not (model_report["missing"] as Array).has(p):
			model_report["missing"].append(p)
		return null
	if not _glb_cache.has(path):
		var doc := GLTFDocument.new()
		var st := GLTFState.new()
		if doc.append_from_buffer(FileAccess.get_file_as_bytes(path), "", st) != OK:
			model_report["missing"].append(p + " (load failed)")
			return null
		_glb_cache[path] = doc.generate_scene(st)
	return (_glb_cache[path] as Node3D).duplicate()


func _aabb_of(n: Node, xf: Transform3D) -> AABB:
	var out := AABB()
	var first := true
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		out = t * (n as MeshInstance3D).mesh.get_aabb()
		first = false
	for ch in n.get_children():
		var b := _aabb_of(ch, t)
		if b.size == Vector3.ZERO:
			continue
		out = b if first else out.merge(b)
		first = false
	return out


func _dress(root: Node3D, cls: String) -> void:
	## v1's own: adopt_prop (the ramp + the hull pen), then the albedo OFF and the class tint ON (barrow_full.gd _place_model)
	var saved := PaintStack.adopt_prop(root, fbm, PaintStack.INK, HULL_PX / PPM, _flat_params())
	for s in saved.get("meshes", []):
		var mat: ShaderMaterial = s["ramp"]
		mat.set_shader_parameter("use_tex", false)
		mat.set_shader_parameter("base_color", _tint_of(cls))
		world_mats.append(mat)
	for s in saved.get("inks", []):
		_prop_inks.append(s["mi"])


func _place_box(id: String, cls: String, model: Node3D, pos: Vector2, z: float, yaw_deg: float, size: Vector3, group := "") -> void:
	var ab := _aabb_of(model, model.transform.affine_inverse())
	var holder := Node3D.new()
	holder.name = id
	var sc := Vector3(size.x / maxf(ab.size.x, 1e-3), size.y / maxf(ab.size.y, 1e-3), size.z / maxf(ab.size.z, 1e-3))
	holder.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(yaw_deg)) * Basis.from_scale(sc), _S(pos.x, z, pos.y))
	holder.set_meta("bv2f_fit", {"slot": group if group != "" else id, "instance": id, "kind": "box", "fit_scale_xyz": [sc.x, sc.y, sc.z],
		"model_aabb_m": [ab.size.x, ab.size.y, ab.size.z], "slot_size_m": [size.x, size.y, size.z]})
	model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
	holder.add_child(model)
	if bool(sim.get("colliders", false)) and _cur_collider == "trimesh_walls":
		# the CAVE ARCH (R-C9-206): its walls, arch and roof collide as built; its rough floor rubble (up-facing triangles in
		# its lowest 1.2 m, and every triangle wholly in its lowest 1.0 m) does not -- the walk surface inside is the
		# shelf-level terrain, flush with the shelf (a body's middle still meets the walls)
		var wb := StaticBody3D.new()
		wb.collision_layer = TERRAIN_BIT
		wb.collision_mask = 0
		wb.name = id + "_walls"
		level.add_child(wb)
		var faces := PackedVector3Array()
		for mi in model.find_children("*", "MeshInstance3D", true, false):
			var m4 := mi as MeshInstance3D
			if m4.mesh == null:
				continue
			var xf4: Transform3D = holder.transform * _xf_to(model, m4)
			var fv: PackedVector3Array = m4.mesh.get_faces()
			for f in range(0, fv.size(), 3):
				var a := xf4 * fv[f]
				var b := xf4 * fv[f + 1]
				var c := xf4 * fv[f + 2]
				var nrm := (b - a).cross(c - a).normalized()
				if (absf(nrm.y) > 0.6 and minf(a.y, minf(b.y, c.y)) < z + 1.2) or maxf(a.y, maxf(b.y, c.y)) < z + 1.0:
					continue
				faces.append_array(PackedVector3Array([a, b, c]))
		var cp := ConcavePolygonShape3D.new()
		cp.set_faces(faces)
		var cs5 := CollisionShape3D.new()
		cs5.shape = cp
		wb.add_child(cs5)
	elif bool(sim.get("colliders", false)) and _cur_collider == "trimesh":
		# Phase 1'' (R-C9-204/206): the cliff kit collides AS BUILT -- one concave shape per mesh, the model's own triangles
		# (the cave's arch, interior and floor edge are walked as drawn)
		var tb := StaticBody3D.new()
		tb.collision_layer = TERRAIN_BIT
		tb.collision_mask = 0
		tb.name = id + "_trimesh"
		level.add_child(tb)
		for mi in model.find_children("*", "MeshInstance3D", true, false):
			var m3 := mi as MeshInstance3D
			if m3.mesh == null:
				continue
			var cs3 := CollisionShape3D.new()
			cs3.shape = m3.mesh.create_trimesh_shape()
			cs3.transform = holder.transform * _xf_to(model, m3)
			tb.add_child(cs3)
	elif bool(sim.get("colliders", false)):
		# Phase 1' walk: a box collider of the uniformly scaled model (85 % of its footprint), on its own body
		var body := StaticBody3D.new()
		body.collision_layer = TERRAIN_BIT
		body.collision_mask = 0
		var cs := CollisionShape3D.new()
		var bx := BoxShape3D.new()
		bx.size = Vector3(size.x * 0.85, size.y, size.z * 0.85)
		cs.shape = bx
		cs.position = _S(pos.x, z + size.y / 2.0, pos.y)
		cs.rotation = Vector3(0.0, deg_to_rad(yaw_deg), 0.0)
		body.add_child(cs)
		level.add_child(body)
	if group != "":
		_group(group, cls).add_child(holder)
		_dress(holder, cls)
		return
	level.add_child(holder)
	_dress(holder, cls)
	_register(id, holder, cls, "model", [pos.x, -pos.y] if absf(z) < 0.01 else null)
	built[id]["fit_scale"] = _v3(sc)


func _place_beam(id: String, cls: String, model: Node3D, a: Vector3, b: Vector3, th: float, fit_height := false, group := "") -> void:
	var ab := _aabb_of(model, model.transform.affine_inverse())
	var holder := Node3D.new()
	holder.name = id
	var d := b - a
	var ln := d.length()
	if fit_height:
		var s := ln / maxf(ab.size.y, 1e-3)
		holder.transform = Transform3D(Basis.from_scale(Vector3(s, s, s)), a)
		model.position = -(ab.position + Vector3(ab.size.x / 2.0, 0.0, ab.size.z / 2.0))
	else:
		var k := 0
		if ab.size.y > ab.size[k]:
			k = 1
		if ab.size.z > ab.size[k]:
			k = 2
		var zz := d / maxf(ln, 1e-3)
		var xx := Vector3.UP.cross(zz)
		xx = Vector3.RIGHT if xx.length() < 0.05 else xx.normalized()
		var yy := zz.cross(xx).normalized()
		var cols := [Vector3.ZERO, Vector3.ZERO, Vector3.ZERO]
		var others := [0, 1, 2]
		others.erase(k)
		cols[k] = zz * (ln / maxf(ab.size[k], 1e-3))
		cols[others[0]] = xx * (th / maxf(ab.size[others[0]], 1e-3))
		cols[others[1]] = yy * (th / maxf(ab.size[others[1]], 1e-3))
		holder.transform = Transform3D(Basis(cols[0], cols[1], cols[2]), (a + b) / 2.0)
		model.position = -(ab.position + ab.size / 2.0)
	var bs := holder.transform.basis
	holder.set_meta("bv2f_fit", {"slot": group if group != "" else id, "instance": id, "kind": "beam" if not fit_height else "beam_fit_height",
		"fit_scale_xyz": [bs.x.length(), bs.y.length(), bs.z.length()], "model_aabb_m": [ab.size.x, ab.size.y, ab.size.z],
		"slot_size_m": [th, (b - a).length(), th]})
	holder.add_child(model)
	if group != "":
		_group(group, cls).add_child(holder)
		_dress(holder, cls)
		return
	level.add_child(holder)
	_dress(holder, cls)
	_register(id, holder, cls, "model")


func _model_class(sid: String) -> String:
	var mc: Dictionary = sim["model_class"]
	if mc.has(sid):
		return String(mc[sid])
	if sid.begins_with("rock_outcrop"):
		return String(mc["_outcrop"])
	return "primitive_grey"


func _build_placements() -> void:
	var skip: Array = sim["skip_models"]
	for m in sim["models"]:
		var sid := String(m["id"])
		if skip.has(sid):
			continue
		var cls := _model_class(sid)
		var glb_slot := str(m.get("glb", ""))
		var insts: Array = m.get("instances", []) if m.get("instances") != null else []
		var pos := Vector2(float(m["pos"][0]), float(m["pos"][1]))
		var sz: Dictionary = m["size_m"]
		if insts.is_empty():
			var node := _load_glb(glb_slot)
			if node != null:
				_place_box(sid, cls, node, pos, float(m["z"]), float(m["godot_rot_y_deg"]),
					Vector3(float(sz["w_local_x"]), float(m.get("aabb_h_m", sz["h"])), float(sz["d_local_z"])))
				model_report["loaded"] += 1
			continue
		var n := 0
		for ins in insts:
			var g := str(ins.get("glb", glb_slot))
			var node2 := _load_glb(g)
			if node2 == null and String(m["kind"]) == "prop" and String(ins["type"]) == "box":
				# R-C9-178 (1): no build exists for the braziers (godot/models/build/brazier.glb was never made) -- a
				# primitive STAND-IN of the slot's size: a stand and a bowl, so the guide shows the object where it stands
				node2 = Node3D.new()
				var st := MeshInstance3D.new()
				var cy := CylinderMesh.new()
				cy.top_radius = 0.12
				cy.bottom_radius = 0.2
				cy.height = 1.5
				st.mesh = cy
				st.position = Vector3(0, 0.75, 0)
				node2.add_child(st)
				var bw := MeshInstance3D.new()
				var bc := CylinderMesh.new()
				bc.top_radius = 0.55
				bc.bottom_radius = 0.3
				bc.height = 0.8
				bw.mesh = bc
				bw.position = Vector3(0, 1.9, 0)
				node2.add_child(bw)
				model_report["stand_ins"] = int(model_report.get("stand_ins", 0)) + 1
			if String(ins.get("procedural", "")) != "" and String(ins["type"]) == "beam":
				_place_primitive_beam("%s_%d" % [sid, n], cls, ins, sid)
				model_report["procedural_beams"] = int(model_report.get("procedural_beams", 0)) + 1
				n += 1
				continue
			if node2 == null:
				continue
			if bool(ins.get("lie_z90", false)):
				# R-C9-181: a fallen stone LIES -- the model turned 90 deg about its Z before the (uniform) fit
				var wrap := Node3D.new()
				node2.rotation = Vector3(0.0, 0.0, PI / 2.0)
				wrap.add_child(node2)
				node2 = wrap
			var iid := "%s_%d" % [sid, n]
			_cur_collider = String(ins.get("collider", ""))
			if String(ins["type"]) == "box":
				var ip := Vector2(float(ins["pos"][0]), float(ins["pos"][1]))
				var s3 := Vector3(float(ins["size_m"][0]), float(ins["size_m"][2]), float(ins["size_m"][1]))
				_place_box(iid, cls, node2, ip, float(ins["z"]), float(ins["godot_rot_y_deg"]), s3, sid)
			else:
				var a := _S(float(ins["a"][0]), float(ins["a"][2]), float(ins["a"][1]))
				var b := _S(float(ins["b"][0]), float(ins["b"][2]), float(ins["b"][1]))
				_place_beam(iid, cls, node2, a, b, float(ins["thickness_m"]), String(ins.get("fit", "")) == "height", sid)
			model_report["loaded"] += 1
			n += 1
	_cur_collider = ""
	_build_stair()
	_build_slabs()
	_build_blobs()
	_build_curtains()
	_build_probes()
	# v1's door-visibility instrument (capture_blockout) asks for v1's three door pieces by id: barrow_v2's King's door is
	# ONE build (barrow_front), so these are EMPTY stand-ins -- the instrument reads nothing (no meshes), it does not fail
	for did in ["door_lintel", "door_post_L", "door_post_R"]:
		var stub := Node3D.new()
		stub.name = did
		level.add_child(stub)
		_register(did, stub, "none", "v1-instrument-stub")
	_build_hall_panels()
	report["placements"] = model_report


func _prism(id: String, cls: String, poly: Array, z0: float, z1: float) -> void:
	var p2 := PackedVector2Array()
	for p in poly:
		p2.append(Vector2(float(p[0]), float(p[1])))
	var idx := Geometry2D.triangulate_polygon(p2)
	var V := PackedVector3Array()
	var N := PackedVector3Array()
	for t in range(0, idx.size(), 3):
		_tri(V, N, _S(p2[idx[t]].x, z1, p2[idx[t]].y), _S(p2[idx[t + 2]].x, z1, p2[idx[t + 2]].y), _S(p2[idx[t + 1]].x, z1, p2[idx[t + 1]].y), Vector3.UP)
	for i in p2.size():
		var a := p2[i]
		var b := p2[(i + 1) % p2.size()]
		var n2 := Vector2(b.y - a.y, a.x - b.x).normalized()
		var nr := Vector3(n2.x, 0.0, n2.y)
		_tri(V, N, _S(a.x, z0, a.y), _S(b.x, z0, b.y), _S(b.x, z1, b.y), nr)
		_tri(V, N, _S(a.x, z0, a.y), _S(b.x, z1, b.y), _S(a.x, z1, a.y), nr)
	var root := Node3D.new()
	root.name = id
	level.add_child(root)
	var p := _flat_params()
	p["_two_sided"] = true
	var m := PaintStack.world_material(fbm, _tint_of(cls), p)
	world_mats.append(m)
	_mesh(V, N, m, "mesh", root)
	_register(id, root, cls, "prism")


func _build_stair() -> void:
	if sim.has("stair_steps"):
		_build_steps()
	if sim.get("stair") == null:
		return
	var S: Dictionary = sim["stair"]
	_prism("stair_top_landing", "path", S["top_landing"]["polygon"], -0.6, 0.0)
	_prism("stair_ledge", "rock", S["bottom_landing"]["polygon"], float(S["flight"]["z_bottom_m"]) - 0.3, float(S["bottom_landing"]["z_m"]))


func _build_blobs() -> void:
	var bc: Dictionary = sim["blob_class"]
	var sphere := SphereMesh.new()
	sphere.radius = 1.0
	sphere.height = 2.0
	sphere.radial_segments = 10
	sphere.rings = 5
	var box := BoxMesh.new()
	box.size = Vector3(2, 2, 2)
	var n := 0
	for b in sim["blobs"]:
		var cls := String(bc.get(String(b["k"]), "rock"))
		var root := Node3D.new()
		root.name = "blob_%d" % n
		var mi := MeshInstance3D.new()
		mi.name = "mesh"
		mi.mesh = box if String(b["proto"]) == "box" else sphere
		var r: Array = b["r"]
		mi.transform = Transform3D(Basis(Vector3.UP, -deg_to_rad(float(b["rot"]))).scaled(Vector3(float(r[0]), float(r[2]), float(r[1]))),
			_S(float(b["c"][0]), float(b["cz"]), float(b["c"][1])))
		root.add_child(mi)
		_group("blobs_" + cls, cls).add_child(root)
		_dress(root, cls)
		n += 1
	report["blobs"] = n


func _build_curtains() -> void:
	## A DECLARED OPENING READS AS AN OPENING: v1 drew its door's passage in its own `passage_dark` tint (barrow_full.gd
	## _build_mound); with the albedo off a build's doorway is the same flat tint as its jambs. So a dark plane stands just
	## inside each declared dark opening (barrow door, great door, sea cave) -- the jambs, lintel and roof in front of it
	## occlude it exactly as built. Openings that are not dark (the gable's breach, the wreck's rail) get none.
	var n := 0
	for o in sim["openings"]:
		if not bool(o.get("dark", false)):
			continue
		var t := deg_to_rad(float(o["faces_deg"]))
		var face := Vector2(sin(t), -cos(t))
		var c := Vector2(float(o["centre_sim"][0]), float(o["centre_sim"][1])) - face * float(o["curtain_inset_m"])
		var w := float(o["w"])
		var h := float(o["h"])
		var root := Node3D.new()
		root.name = "curtain_" + String(o["id"])
		var mi := MeshInstance3D.new()
		mi.name = "mesh"
		var bm := BoxMesh.new()
		bm.size = Vector3(w, h, 0.3)
		mi.mesh = bm
		mi.material_override = PaintStack.world_material(fbm, _tint_of("passage_dark"), _flat_params())
		world_mats.append(mi.material_override)
		# box local +Z = the opening's facing: Basis(UP, a) turns +Z to (sin a, 0, cos a) in (x, z) = sim (x, y)
		var yaw := atan2(face.x, face.y)
		mi.transform = Transform3D(Basis(Vector3.UP, yaw), _S(c.x, float(o["z0"]) + h / 2.0, c.y))
		root.add_child(mi)
		level.add_child(root)
		_register("curtain_" + String(o["id"]), root, "passage_dark", "declared_opening")
		n += 1
	report["curtains"] = n


func _build_probes() -> void:
	## R-C9-177 CHECK (a): env BV2F_PROBES = "with" (each deliverer opening's probe among everything -- what the play camera
	## sees of it) or "only" (the probes alone -- the unoccluded reference). Unset: no probes (the guide never has them).
	var mode := OS.get_environment("BV2F_PROBES")
	if mode == "":
		return
	if mode == "only":
		for ch in level.get_children():
			(ch as Node3D).visible = false
	for o in sim["openings"]:
		if not o.has("probe"):
			continue
		var pr: Dictionary = o["probe"]
		var V := PackedVector3Array()
		var N := PackedVector3Array()
		var t := String(pr["type"])
		if t == "v":
			var a := deg_to_rad(float(pr["faces_deg"]))
			var f := Vector2(sin(a), -cos(a))
			var tg := Vector2(-f.y, f.x)
			var c := Vector2(float(pr["centre"][0]), float(pr["centre"][1])) + f * 0.4   # in front of a face-mounted curtain (a 0.3 m box centred 0.1 out)
			var hw := float(pr["w"]) / 2.0
			var z0 := float(pr["z0"])
			var z1 := z0 + float(pr["h"])
			var p0 := c - tg * hw
			var p1 := c + tg * hw
			var nr := Vector3(f.x, 0.0, f.y)
			_tri(V, N, _S(p0.x, z0, p0.y), _S(p1.x, z0, p1.y), _S(p1.x, z1, p1.y), nr)
			_tri(V, N, _S(p0.x, z0, p0.y), _S(p1.x, z1, p1.y), _S(p0.x, z1, p0.y), nr)
		elif t == "h_rect":
			var r := deg_to_rad(float(pr["rot_deg"]))
			var ax := Vector2(cos(r), sin(r))
			var ay := Vector2(-ax.y, ax.x)
			var c2 := Vector2(float(pr["centre"][0]), float(pr["centre"][1]))
			var l2 := float(pr["L"]) / 2.0
			var w2 := float(pr["W"]) / 2.0
			var z := float(pr["z"])
			var q := [c2 - ax * l2 - ay * w2, c2 + ax * l2 - ay * w2, c2 + ax * l2 + ay * w2, c2 - ax * l2 + ay * w2]
			_tri(V, N, _S(q[0].x, z, q[0].y), _S(q[1].x, z, q[1].y), _S(q[2].x, z, q[2].y), Vector3.UP)
			_tri(V, N, _S(q[0].x, z, q[0].y), _S(q[2].x, z, q[2].y), _S(q[3].x, z, q[3].y), Vector3.UP)
		else:
			var p2 := PackedVector2Array()
			for pp in pr["polygon"]:
				p2.append(Vector2(float(pp[0]), float(pp[1])))
			var idx := Geometry2D.triangulate_polygon(p2)
			var z2 := float(pr["z"])
			for k in range(0, idx.size(), 3):
				_tri(V, N, _S(p2[idx[k]].x, z2, p2[idx[k]].y), _S(p2[idx[k + 1]].x, z2, p2[idx[k + 1]].y), _S(p2[idx[k + 2]].x, z2, p2[idx[k + 2]].y), Vector3.UP)
		var root := Node3D.new()
		root.name = "probe_" + String(o["id"])
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.albedo_color = Color(1, 0, 1)
		_mesh(V, N, m, "mesh", root, false)
		level.add_child(root)
		_register("probe_" + String(o["id"]), root, "probe", "check_a")


func _place_primitive_beam(id: String, cls: String, ins: Dictionary, group: String) -> void:
	## R-C9-181: a piece BUILT TO A LENGTH (a palisade post, a log) is a primitive at its TRUE dimensions -- a cylinder of
	## the slot's thickness and the segment's length (a post gets a cone tip) -- never a model stretched to fit (v1's slabs)
	var a := _S(float(ins["a"][0]), float(ins["a"][2]), float(ins["a"][1]))
	var b := _S(float(ins["b"][0]), float(ins["b"][2]), float(ins["b"][1]))
	var th := float(ins["thickness_m"])
	var d := b - a
	var ln := d.length()
	var zz := d / maxf(ln, 1e-3)
	var xx := Vector3.UP.cross(zz)
	xx = Vector3.RIGHT if xx.length() < 0.05 else xx.normalized()
	var yy := zz.cross(xx).normalized()
	var holder := Node3D.new()
	holder.name = id
	# a CylinderMesh's axis is its local Y: map Y -> the segment direction
	holder.transform = Transform3D(Basis(xx, zz, -yy), (a + b) / 2.0)
	var post := String(ins.get("procedural", "")) == "post"
	var body_len := ln - (th * 1.2 if post else 0.0)
	var cy := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = th / 2.0
	cm.bottom_radius = th / 2.0
	cm.height = body_len
	cm.radial_segments = 10
	cy.mesh = cm
	cy.position = Vector3(0.0, -(ln - body_len) / 2.0, 0.0)
	holder.add_child(cy)
	if post:
		var tip := MeshInstance3D.new()
		var tc := CylinderMesh.new()
		tc.top_radius = 0.0
		tc.bottom_radius = th / 2.0
		tc.height = th * 1.2
		tc.radial_segments = 10
		tip.mesh = tc
		tip.position = Vector3(0.0, ln / 2.0 - th * 0.6, 0.0)
		holder.add_child(tip)
	holder.set_meta("bv2f_fit", {"slot": group, "instance": id, "kind": "procedural_" + String(ins.get("procedural", "")),
		"fit_scale_xyz": [1.0, 1.0, 1.0], "model_aabb_m": [th, ln, th], "slot_size_m": [th, ln, th],
		"_": "procedural primitive at true dimensions: no model, no fit (P6' scale N/A)"})
	_group(group, cls).add_child(holder)
	_dress(holder, cls)


func _build_steps() -> void:
	## Phase 1' (art): the straight open-sided stair as procedural treads at TRUE size (rise/tread/width), each a block
	## down to the ledge -- v1's slab practice; walkable (each tread a collider)
	var root := Node3D.new()
	root.name = "stair_steps"
	level.add_child(root)
	var body := _body(root, "stair_body")
	var n := 0
	for st in sim["stair_steps"]:
		var c := Vector2(float(st["c_sim"][0]), float(st["c_sim"][1]))
		var zt := float(st["z_top"])
		var z0 := float(sim["sea_z"]) - 0.5
		var mi := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(float(st["w"]), zt - z0, float(st["tread"]) + 0.02)
		mi.mesh = bm
		mi.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(float(st["yaw_deg"]))), _S(c.x, (zt + z0) / 2.0, c.y))
		root.add_child(mi)
		if not sim.has("route"):
			var cs := CollisionShape3D.new()
			var bx := BoxShape3D.new()
			bx.size = bm.size
			cs.shape = bx
			cs.transform = mi.transform
			body.add_child(cs)
		n += 1
	_dress(root, "rock")
	_register("stair_steps", root, "rock", "procedural")
	report["stair_steps"] = n
	if sim.has("route"):
		_build_route(body)


func _build_route(stair_body: StaticBody3D) -> void:
	## R-C9-188/189. (1) THE STAIR'S WALK SURFACE: one ramp collider through every nosing (the treads above stay visual).
	## v1's knight (scripts/knight.gd) is a CharacterBody3D capsule (r 0.35, h 1.8, x figure scale) on plain
	## move_and_slide() under 18 m/s2 of gravity, with no step-up code and Godot's default floor_max_angle (45 deg): a
	## capsule mounts an edge only while the contact normal is within 45 deg of up, i.e. an edge no higher than
	## r (1 - cos 45) = 0.10 m -- a 0.179 m riser stops him. The ramp is v6's walk model ("one plane under the step
	## nosings"), 33.5 deg < 45, flush with the shelf one tread out from the foot and with the landing at the top.
	## The landing's walk surface is a plate at 0 that meets the ramp's top edge exactly (the terrain under both is lower).
	var R: Dictionary = sim["route"]
	var wb := []
	for rp in R.get("walk_boxes", [R["ramp"]]):
		var cs := CollisionShape3D.new()
		var bx := BoxShape3D.new()
		var th := float(rp["thick"])
		bx.size = Vector3(float(rp["across"]), th, float(rp["along"]))
		cs.shape = bx
		var bas := Basis(Vector3.UP, deg_to_rad(float(rp["yaw_deg"]))) * Basis(Vector3.RIGHT, deg_to_rad(float(rp["pitch_deg"])))
		var top := _S(float(rp["c_sim"][0]), float(rp["z_c"]), float(rp["c_sim"][1]))
		cs.transform = Transform3D(bas, top - bas.y.normalized() * th / 2.0)
		cs.name = String(rp["id"])
		stair_body.add_child(cs)
		wb.append({"id": rp["id"], "pitch_deg": rp["pitch_deg"], "across_m": rp["across"], "along_m": rp["along"]})
	report["walk_boxes"] = wb
	# (2) THE SEA CAVE HOOD: brow, cheeks, back -- procedural rock at true size, each with its collider; drawn as part of
	# the cliff (its id is cliff_faces': the hood IS the cliff, and no new id shifts v1's ID colour order)
	var hb := _body(level, "cave_hood_body")
	var n := 0
	for b in R["hood"]:
		var holder := Node3D.new()
		holder.name = "cave_" + String(b["id"])
		var mi := MeshInstance3D.new()
		var bm := BoxMesh.new()
		var z0 := float(b["z0"])
		var z1 := float(b["z1"])
		bm.size = Vector3(float(b["across"]), z1 - z0, float(b["along"]))
		mi.mesh = bm
		holder.transform = Transform3D(Basis(Vector3.UP, deg_to_rad(float(b["yaw_deg"]))), _S(float(b["c_sim"][0]), (z0 + z1) / 2.0, float(b["c_sim"][1])))
		holder.add_child(mi)
		holder.set_meta("bv2f_fit", {"slot": "cliff_faces", "instance": holder.name, "kind": "procedural_cave_hood",
			"fit_scale_xyz": [1.0, 1.0, 1.0], "model_aabb_m": [bm.size.x, bm.size.y, bm.size.z], "slot_size_m": [bm.size.x, bm.size.y, bm.size.z],
			"_": "procedural rock at true dimensions: no model, no fit (P6' scale N/A)"})
		_group("cliff_faces", "rock").add_child(holder)
		_dress(holder, "rock")
		var c2 := CollisionShape3D.new()
		var b2 := BoxShape3D.new()
		b2.size = bm.size
		c2.shape = b2
		c2.transform = holder.transform
		hb.add_child(c2)
		n += 1
	report["cave_hood"] = n


func _build_hall_panels() -> void:
	## R-C9-188/189 (Matt): the burnt hall CLOSED but for its great door -- a plank panel in the build's own local metres,
	## a child of the placed build (so it takes the hall's one uniform scale and yaw), dressed in the hall's class
	var k := 0
	for pn in sim.get("hall_panels", []):
		var holder: Node3D = nodes.get(String(pn["model"]), null)
		if holder == null or holder.get_child_count() == 0:
			continue
		var mdl := holder.get_child(0) as Node3D
		var xa := float(pn["x_m"][0])
		var xb := float(pn["x_m"][1])
		var poly := PackedVector2Array()
		for q in pn["poly_zy_m"]:
			poly.append(Vector2(float(q[0]), float(q[1])))
		var V := PackedVector3Array()
		var N := PackedVector3Array()
		var idx := Geometry2D.triangulate_polygon(poly)
		for t in range(0, idx.size(), 3):
			var a := poly[idx[t]]
			var b := poly[idx[t + 1]]
			var c := poly[idx[t + 2]]
			_tri(V, N, Vector3(xb, a.y, a.x), Vector3(xb, b.y, b.x), Vector3(xb, c.y, c.x), Vector3.RIGHT)
			_tri(V, N, Vector3(xa, a.y, a.x), Vector3(xa, c.y, c.x), Vector3(xa, b.y, b.x), Vector3.LEFT)
		for i in poly.size():
			var p := poly[i]
			var q := poly[(i + 1) % poly.size()]
			var e := (q - p)
			var nr := Vector3(0.0, -e.x, e.y).normalized()
			_tri(V, N, Vector3(xa, p.y, p.x), Vector3(xb, p.y, p.x), Vector3(xb, q.y, q.x), nr)
			_tri(V, N, Vector3(xa, p.y, p.x), Vector3(xb, q.y, q.x), Vector3(xa, q.y, q.x), nr)
		var root := Node3D.new()
		root.name = "hall_panel_%d" % k
		var p2 := _flat_params()
		p2["_two_sided"] = true
		_mesh(V, N, PaintStack.world_material(fbm, _tint_of(String(pn["class"])), p2), "mesh", root)
		mdl.add_child(root)
		_dress(root, String(pn["class"]))
		k += 1
	report["hall_panels"] = k


func _build_bounds() -> void:
	## R-C9-188/189: v1's bounds walls (scripts/barrow_full.gd _build_bounds), run from below the sea to 3 m up -- the
	## walkable route lies under the clifftop -- plus the inner walls on the lip the route runs beneath (open at the landing)
	var bd: Dictionary = layout["bounds"]
	if not bd.has("wall_z_m"):
		super._build_bounds()
		return
	var poly: Array = bd["polygon_uv"]
	var body := _body(level, "Bounds")
	var z0 := float(bd["wall_z_m"][0])
	var z1 := float(bd["wall_z_m"][1])
	var total := 0.0
	for i in poly.size():
		var p := Vector2(float(poly[i][0]), float(poly[i][1]))
		var q := Vector2(float(poly[(i + 1) % poly.size()][0]), float(poly[(i + 1) % poly.size()][1]))
		var d := q - p
		_box_rot(body, (p + q) * 0.5, d.length() + 0.3, 0.3, z0, z1, atan2(d.y, d.x))
		total += d.length()
	var nin := 0
	for w in bd.get("inner_walls_uv", []):
		for i in (w as Array).size() - 1:
			var p := Vector2(float(w[i][0]), float(w[i][1]))
			var q := Vector2(float(w[i + 1][0]), float(w[i + 1][1]))
			var d := q - p
			_box_rot(body, (p + q) * 0.5, d.length() + 0.3, 0.3, float(bd["inner_wall_z_m"][0]), float(bd["inner_wall_z_m"][1]), atan2(d.y, d.x))
			nin += 1
	report["bounds"] = {"edges": poly.size(), "perimeter_m": snappedf(total, 0.01), "inner_walls": nin, "wall_z_m": [z0, z1]}


func freeze_pose(on: bool) -> void:
	## R-C9-191: the GUIDE's scale-knight pose is DETERMINISTIC. v1's freeze only stops the animation where it happens to
	## be -- and how far his AnimationTree has run when the frozen capture freezes him depends on how many physics ticks
	## the load took (two renders of one scene differed by 2939 px on him). Frozen here = ONE fixed frame: his idle clip
	## (character roles "idle") at t = 0.0 straight off the AnimationPlayer (the tree and the foot-lock IK set aside);
	## unfrozen = v1's own tree back on.
	super.freeze_pose(on)
	if knight == null:
		return
	var anim = knight.get("_anim")
	var tree = knight.get("_tree")
	var fl = knight.get("_foot_lock")
	if anim == null:
		return
	if on:
		if tree != null:
			(tree as AnimationTree).active = false
		if fl != null:
			(fl as SkeletonModifier3D).active = false
		var clip := String((knight.get("_roles") as Dictionary).get("idle", "idle"))
		var ap := anim as AnimationPlayer
		ap.active = true
		ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
		ap.play(clip)
		ap.seek(0.0, true)
		report["guide_knight_pose"] = {"clip": clip, "t_s": 0.0, "rule": "R-C9-191 fixed frame"}
	else:
		(anim as AnimationPlayer).active = false
		if tree != null:
			(tree as AnimationTree).active = true
		if fl != null:
			(fl as SkeletonModifier3D).active = true



func _build_slabs() -> void:
	## Phase 1'' (R-C9-204/206): every procedural prism at true size -- the sea's shore-fast ice, plates and floes (the
	## loose outer floes in their own group, tagged to bob), the mere's cracked plates, the stream's ice, the shelf's rime,
	## the rock-cut stair's treads and the snow on their back edges. ONE mesh and ONE id per group (v1's ID code has 256
	## colours); each item a polygon extruded from z0 to z1; the gaps between them are the cracks (dark water below).
	var n_all := 0
	var rep := {}
	for gid in (sim.get("slabs", {}) as Dictionary).keys():
		var g: Dictionary = sim["slabs"][gid]
		var cls := String(g["class"])
		var V := PackedVector3Array()
		var N := PackedVector3Array()
		for it in g["items"]:
			var p2 := PackedVector2Array()
			for q in it["poly"]:
				p2.append(Vector2(float(q[0]), float(q[1])))
			var z0 := float(it["z0"])
			var z1 := float(it["z1"])
			var idx := Geometry2D.triangulate_polygon(p2)
			if idx.is_empty():
				var c := Vector2.ZERO
				for q in p2:
					c += q
				c /= float(p2.size())
				for i in p2.size():
					_tri(V, N, _S(c.x, z1, c.y), _S(p2[i].x, z1, p2[i].y), _S(p2[(i + 1) % p2.size()].x, z1, p2[(i + 1) % p2.size()].y), Vector3.UP)
			else:
				for t in range(0, idx.size(), 3):
					_tri(V, N, _S(p2[idx[t]].x, z1, p2[idx[t]].y), _S(p2[idx[t + 1]].x, z1, p2[idx[t + 1]].y), _S(p2[idx[t + 2]].x, z1, p2[idx[t + 2]].y), Vector3.UP)
			var sgn := 0.0
			for i in p2.size():
				sgn += p2[i].x * p2[(i + 1) % p2.size()].y - p2[(i + 1) % p2.size()].x * p2[i].y
			for i in p2.size():
				var a := p2[i]
				var b := p2[(i + 1) % p2.size()]
				var e := b - a
				if e.length() < 1e-4:
					continue
				var nr := Vector3(e.y, 0.0, -e.x).normalized() * (1.0 if sgn > 0.0 else -1.0)   # OUTWARD whichever way the polygon winds
				_tri(V, N, _S(a.x, z0, a.y), _S(b.x, z0, b.y), _S(b.x, z1, b.y), nr)
				_tri(V, N, _S(a.x, z0, a.y), _S(b.x, z1, b.y), _S(a.x, z1, a.y), nr)
			n_all += 1
		var root := Node3D.new()
		root.name = String(gid)
		root.set_meta("bv2f_bob", bool(g.get("bob", false)))
		var p := _flat_params()
		p["_two_sided"] = true
		if V.size() > 0:
			_mesh(V, N, PaintStack.world_material(fbm, _tint_of(cls), p), "mesh", root)
		level.add_child(root)
		_dress(root, cls)
		_register(String(gid), root, cls, "slabs")
		rep[gid] = (g["items"] as Array).size()
	report["slabs"] = rep



func _gn(Z: PackedFloat32Array, W: int, Hn: int, i: int, j: int, step: float) -> Vector3:
	var i0 := maxi(i - 1, 0)
	var i1 := mini(i + 1, W)
	var j0 := maxi(j - 1, 0)
	var j1 := mini(j + 1, Hn)
	var dzx := (Z[j * (W + 1) + i1] - Z[j * (W + 1) + i0]) / (float(i1 - i0) * step)
	var dzy := (Z[j1 * (W + 1) + i] - Z[j0 * (W + 1) + i]) / (float(j1 - j0) * step)
	return Vector3(-dzx, 1.0, -dzy).normalized()
