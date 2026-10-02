extends SceneTree
## C-9 BIND-ORDER FENCE (the coordinator, after the E1 lane's finding: Godot builds each GLB's Skeleton3D in THAT FILE's
## node order, and a skin bound by bone INDEX onto the body's skeleton lands on the wrong bones whenever a piece's file
## order differs from the body's). drax.
##   Godot --path godot --resolution 640x640 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --script tools/probe_bind_order.gd -- --out DIR [--only LABEL]
## For every gear piece of every pack, on its body's skeleton held in one fixed non-rest pose, three renders:
##   index    -- each bind on the piece file's bone INDEX (the name cleared): what an index binding draws
##   name     -- each bind on the piece file's bone NAME (gear.gd's binding since this fence; wl_e1 gear_stills _bind())
##   shipped  -- the skin exactly as imported, untouched (what the build drew BEFORE gear.gd bound by name)
## FAIL on ANY pixel difference between index and name (the piece's file order differs from the body's), and records
## whether shipped differed from name (the piece WAS misbound in the build). DIR/bind_order.json; DIR/<label>_<piece>_*.png
## for every failing piece. Exit 1 on any FAIL.

const PACKS := [
	["barbarian", "res://data/character.json"],
	["barb_t1211", "res://data/slots/barb_t1211.json"],
	["barb_f25l", "res://data/slots/barb_f25l.json"],
	["barb_f40l", "res://data/slots/barb_f40l.json"],
	["barb_gladb", "res://data/slots/barb_gladb.json"],
	["barb_gladc", "res://data/slots/barb_gladc.json"],
	["sorceress", "res://data/character_sorceress.json"],
	["so_bmc", "res://data/slots/so_bmc.json"],
	["so_bmd", "res://data/slots/so_bmd.json"],
	["warlord", "res://data/slots/warlord.json"],
	["warlord_ice", "res://data/slots/warlord_ice.json"],
]
const W := 384
const H := 640

var vp: SubViewport
var cam: Camera3D


func _json(p: String):
	return JSON.parse_string(FileAccess.get_file_as_string(p))


func _skel_of(n: Node) -> Skeleton3D:
	var out: Skeleton3D = null
	for s in n.find_children("*", "Skeleton3D", true, false):
		out = s
	return out


func _pose(sk: Skeleton3D) -> void:
	# one fixed, deterministic, clearly non-rest pose: every bone turned 0.35 rad about its own axis
	for i in sk.get_bone_count():
		var ax := Vector3(sin(i * 1.7 + 0.3), cos(i * 1.3), sin(i * 0.7 + 1.1)).normalized()
		sk.set_bone_pose_rotation(i, sk.get_bone_rest(i).basis.get_rotation_quaternion() * Quaternion(ax, 0.35))


func _snap() -> Image:
	for f in 3:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
	return vp.get_texture().get_image()


func _diff(a: Image, b: Image) -> int:
	var da := a.get_data()
	var db := b.get_data()
	if da.size() != db.size():
		return -1
	var n := 0
	var px := da.size() / 4 if a.get_format() == Image.FORMAT_RGBA8 else da.size() / 3
	var step := 4 if a.get_format() == Image.FORMAT_RGBA8 else 3
	for i in px:
		var o := i * step
		if da[o] != db[o] or da[o + 1] != db[o + 1] or da[o + 2] != db[o + 2]:
			n += 1
	return n


func _skin_variant(skin: Skin, ps: Skeleton3D, mode: String) -> Skin:
	if mode == "shipped" or skin == null:
		return skin
	var s := skin.duplicate() as Skin
	for bi in s.get_bind_count():
		var nm := String(s.get_bind_name(bi))
		var bb := s.get_bind_bone(bi)
		if nm == "" and bb >= 0 and ps != null:
			nm = ps.get_bone_name(bb)
		if bb < 0 and ps != null:
			bb = ps.find_bone(nm)
		if mode == "index":
			s.set_bind_name(bi, &"")
			s.set_bind_bone(bi, bb)
		elif mode == "control":
			s.set_bind_name(bi, &"")
			s.set_bind_bone(bi, (bb + 1) % ps.get_bone_count())
		else:
			s.set_bind_name(bi, StringName(nm))
	return s


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir := String(args[args.find("--out") + 1])
	var only := String(args[args.find("--only") + 1]) if args.has("--only") else ""
	var dump_all := args.has("--dump")
	DirAccess.make_dir_recursive_absolute(out_dir)
	await process_frame
	vp = SubViewport.new()
	vp.size = Vector2i(W, H)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	vp.transparent_bg = false
	root.add_child(vp)
	var env := WorldEnvironment.new()
	env.environment = Environment.new()
	env.environment.background_mode = Environment.BG_COLOR
	env.environment.background_color = Color(0.5, 0.5, 0.55)
	env.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.environment.ambient_light_color = Color(0.6, 0.6, 0.6)
	vp.add_child(env)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-50, 30, 0)
	vp.add_child(sun)
	cam = Camera3D.new()
	vp.add_child(cam)
	var report := {"packs": {}, "fails": 0, "was_misbound": 0, "pieces": 0}
	for pk in PACKS:
		var label := String(pk[0])
		if only != "" and label != only:
			continue
		var cfg = _json(String(pk[1]))
		var bps := load(String(cfg["model"])) as PackedScene
		if bps == null:
			report["packs"][label] = {"error": "body failed to load: " + String(cfg["model"])}
			report["fails"] += 1
			print("BIND FAIL %-12s %-14s body failed to load" % [label, "(body)"])
			continue
		var body := bps.instantiate()
		vp.add_child(body)
		var sk := _skel_of(body)
		for m in body.find_children("*", "MeshInstance3D", true, false):
			(m as MeshInstance3D).visible = false    # the piece alone, so a pixel can only be the piece's
		var ap := body.find_children("*", "AnimationPlayer", true, false)
		for a in ap:
			(a as AnimationPlayer).stop()
		_pose(sk)
		var bg: Image = null
		var mf = _json(String(cfg["gear_manifest"]))
		var gdir := String(cfg.get("gear_dir", ""))
		var bnames := []
		for i in sk.get_bone_count():
			bnames.append(sk.get_bone_name(i))
		var prow := {"body": String(cfg["model"]), "manifest": String(cfg["gear_manifest"]), "pieces": {}}
		for spec in mf.get("pieces", []):
			var pname := String(spec["piece"])
			var path := gdir + "/" + String(spec["glb"])
			if not ResourceLoader.exists(path):
				prow["pieces"][pname] = {"result": "FAIL", "error": "missing " + path}
				report["fails"] += 1
				continue
			var pps := load(path) as PackedScene
			if pps == null:
				prow["pieces"][pname] = {"result": "FAIL", "error": "failed to load " + path}
				report["fails"] += 1
				print("BIND FAIL %-12s %-14s failed to load" % [label, pname])
				continue
			var src := pps.instantiate()
			var ps := _skel_of(src)
			var pnames := []
			if ps != null:
				for i in ps.get_bone_count():
					pnames.append(ps.get_bone_name(i))
			var named := 0
			var binds := 0
			var mis := []
			for m in src.find_children("*", "MeshInstance3D", true, false):
				var mi := m as MeshInstance3D
				if mi.mesh == null:
					continue
				mis.append(mi)
				if mi.skin != null:
					for bi in mi.skin.get_bind_count():
						binds += 1
						named += int(String(mi.skin.get_bind_name(bi)) != "")
			# bones whose INDEX names a different bone on the body than on the piece's own file
			var order_diff := 0
			for i in mini(pnames.size(), bnames.size()):
				order_diff += int(pnames[i] != bnames[i])
			# centre the camera on the piece's own bounds, in the pose
			var imgs := {}
			for mode in ["index", "name", "shipped", "control"]:
				var made: Array[MeshInstance3D] = []
				for mi in mis:
					var o := MeshInstance3D.new()
					o.mesh = mi.mesh
					for s in mi.mesh.get_surface_count():
						o.set_surface_override_material(s, mi.get_active_material(s))
					sk.add_child(o)
					o.transform = mi.transform
					o.skin = _skin_variant(mi.skin, ps, mode)
					o.skeleton = NodePath("..")
					made.append(o)
				if mode == "index":
					# frame the POSED skeleton (its bones' world positions), not a mesh AABB: a skinned mesh's AABB is its
					# rest bounds in its own space, and it put the camera below the figure (the first frames read empty)
					var ab := AABB(sk.global_transform * sk.get_bone_global_pose(0).origin, Vector3.ZERO)
					for bi in sk.get_bone_count():
						ab = ab.expand(sk.global_transform * sk.get_bone_global_pose(bi).origin)
					ab = ab.grow(0.25)
					var c := ab.get_center()
					var hgt := maxf(ab.size.y, ab.size.x * float(H) / float(W)) * 1.15
					cam.projection = Camera3D.PROJECTION_ORTHOGONAL
					cam.size = hgt
					cam.global_transform = Transform3D(Basis(), c + Vector3(0.4, 0.2, 1.0).normalized() * 6.0)
					cam.look_at(c, Vector3.UP)
				if mode == "index" and bg == null:
					for o in made:
						o.visible = false
					bg = await _snap()
					for o in made:
						o.visible = true
				imgs[mode] = await _snap()
				for o in made:
					sk.remove_child(o)
					o.queue_free()
			src.queue_free()
			var d_in := _diff(imgs["index"], imgs["name"])
			var d_sn := _diff(imgs["shipped"], imgs["name"])
			var d_ct := _diff(imgs["control"], imgs["name"])
			var lit := _diff(imgs["name"], bg)       # the piece's own pixels against the empty frame
			# the check running is not the check passing: an empty frame, or a control the render cannot see, FAILS
			var res := "PASS" if (d_in == 0 and d_ct > 0 and lit > 0) else "FAIL"
			var row := {"result": res, "px_index_vs_name": d_in, "px_shipped_vs_name": d_sn,
				"was_misbound_in_build": d_sn != 0, "px_control_vs_name": d_ct, "px_piece": lit, "binds": binds, "binds_named_on_import": named,
				"piece_bones": pnames.size(), "body_bones": bnames.size(), "bone_index_names_differ": order_diff}
			prow["pieces"][pname] = row
			report["pieces"] += 1
			report["fails"] += int(res == "FAIL")
			report["was_misbound"] += int(d_sn != 0)
			if res == "FAIL" or d_sn != 0 or dump_all:
				for mode in imgs:
					(imgs[mode] as Image).save_png(out_dir + "/" + label + "_" + pname + "_" + mode + ".png")
			print("BIND %-4s %-12s %-14s index~name %6d px  shipped~name %6d px  control~name %6d px  piece %6d px  order-diff %3d  named %d/%d" % [
				res, label, pname, d_in, d_sn, d_ct, lit, order_diff, named, binds])
		report["packs"][label] = prow
		vp.remove_child(body)
		body.queue_free()
		await process_frame
	var f := FileAccess.open(out_dir + "/bind_order.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("bind order: %d/%d pass; %d were misbound in the build" % [
		report["pieces"] - report["fails"], report["pieces"], report["was_misbound"]])
	quit(1 if report["fails"] > 0 else 0)
