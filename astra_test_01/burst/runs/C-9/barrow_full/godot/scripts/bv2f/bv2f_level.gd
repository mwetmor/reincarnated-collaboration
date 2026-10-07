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
var BV2F_DATA := "res://data/bv2f/" + (OS.get_environment("BV2F_VARIANT") if OS.get_environment("BV2F_VARIANT") != "" else "v7c") + "/"
var lvl := {}
var sim := {}
var class_meshes := {}
var _glb_cache := {}
var model_report := {"loaded": 0, "missing": []}


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
			var n1 := (pd - pa).cross(pb - pa).normalized()
			var n2 := (pd - pb).cross(pc - pb).normalized()
			var vv: PackedVector3Array = V[k]
			var nn: PackedVector3Array = N[k]
			vv.append_array(PackedVector3Array([pa, pb, pd, pb, pc, pd]))
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
	# the walkable floor's collider: ONE box, top face at y = 0 (v1's), over the whole site
	var body := _body(level, "FloorBody")
	var cs := CollisionShape3D.new()
	var bx := BoxShape3D.new()
	bx.size = Vector3(150.0, 2.0, 150.0)
	cs.shape = bx
	cs.position = Vector3(0.0, -1.0, 0.0)
	body.add_child(cs)
	report["ground"]["class_triangles"] = tris
	report["ground"]["sea_z"] = sz


func _build_mound() -> void:
	pass


func _build_overlay() -> void:
	pass


func _build_crucible() -> void:
	pass


func floor_y_at(_u: float, _v: float) -> float:
	return 0.0


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
	_build_stair()
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
