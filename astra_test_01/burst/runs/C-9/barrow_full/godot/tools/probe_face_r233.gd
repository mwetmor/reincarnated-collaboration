extends SceneTree
## C-9 R-C9-233 -- THE SORCERESS'S FACE UNDER THE HOOD, AT THE PLAY CAMERA (Matt: "her face is so dark that she looks like a
## shadow/ghost.. the hood gets painted over her face awkwardly"). An ISOLATION GRID in the painted Barrow itself (Compatibility
## on ANGLE, the web branches on, her real ramp materials, her real hull ink, the real pen/grade/paper post pass): per clip x
## heading, ONE frozen pose, rendered under each variant so the only thing that changes between two frames is the variant.
## drax, lane SO.
##   Godot --path godot --resolution 1920x1080 --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --fixed-fps 60 --script tools/probe_face_r233.gd -- --as-web --c sorceress --armor bm134 \
##         --out DIR --class /abs/class.png [--variants live,nofronthair,...] [--headings S,SE,...] [--shots idle@1.0,...]
## POSE: her tree and her physics are switched OFF and the AnimationPlayer is seeked to the clip's time and paused (her bm134
## slot has NO layers -- arm_layer_armed_R, arm_layer_armed, upper_armed and strike_release are all empty -- so the raw clip
## IS her pose); the heading is place_knight's facing, which turns the rig at once.
## VARIANTS (applied, rendered, undone; one frozen pose):
##   live         as played
##   nofronthair  the FRONT hair (class G: hair, centroid z > 0.035 m) discarded, in her ramp material AND her hull ink
##   nohood       the hood (and its cap, and its hull ink) hidden
##   headzero     Head and neck bone rotations put back to REST (the clip's head/neck pitch removed; the spine keeps its own)
##   fill         a soft face fill: a directional light from the camera's own direction, her layer only, no shadow
##   noink        THE WEB PEN OFF (post pass ink_on 0; grade and paper kept) -- on the web build her hull lines are HIDDEN
##                (barrow_full.gd: "one pen on him"), so the lines on her face are the depth-only screen pen's; the
##                measuring script composites this inside the face opening only
##   <v>_..._z3_nopen.png  (every ID variant) the same frame with the pen off: pen pixels = what the pen darkened
## STEP 1 (the fix candidates; --fixA / --fixB name a body GLB, loaded at run time and swapped onto her body AND its hull ink):
##   inksync      live, with her body's hull ink given her body's own morph values (knight.gd sets a morph on the body only,
##                so the ink still draws the un-morphed shape: the tucked braid's line down her back)
##   fixA         inksync + so_mx/export/ss233a (hood_braid also tucks the front strands that cross her face)
##   fixB         inksync + so_mx/export/ss233b (ss233a + the face island of the atlas lifted)
##   fixC/fixD    any further body (--fixC/--fixD), with --<v>_hood naming an imported hood GLB swapped onto her hood too
## (on the WEB build the hull inks are hidden, so "inksync" changes nothing there; the fixes are body/hood swaps)
## PASSES, each saved as a crop around her head (the Head bone, unprojected):
##   <v>_<clip>_<H>_z<zoom>_beauty.png   at zoom 1 (play) and 3 (the same camera, 3x: measurement resolution)
##   <v>_<clip>_<H>_z3_ida.png           unshaded ID, inks hidden: face R, front hair G, other hair C, rest of her body Y,
##                                       hood B, other gear M (cull_back like the real materials; the post pass hidden)
##   <v>_<clip>_<H>_z3_idb.png           the inks only coloured: hood ink R, body ink G, other gear ink B, every surface Y
##   <v>_<clip>_<H>_z<zoom>_foot.png     the FACE FOOTPRINT: her face texels alone (nothing else drawn) -- the face as if
##                                       nothing covered it; the denominator of every coverage number
const SPOT := Vector2(-1.0, -0.5)
const CHAR_LAYER := 4
const ALL_VARIANTS := ["live", "nofronthair", "nohood", "headzero", "fill", "noink"]
const ID_VARIANTS := ["live", "nofronthair", "nohood", "headzero", "fixA", "fixB", "fixC", "fixD", "fixE", "fixF", "fixG"]

var scene
var k
var skel: Skeleton3D
var cls: ImageTexture
var out_dir := ""
var crops := {1: 220, 3: 600}   # generous: the Head bone unprojects ~0.3 m off her face; r233_03 re-centres on the face footprint
var rep := {"poses": []}
var saved_vis := {}
var saved_mat := {}
var hood_mis: Array = []
var gear_mis: Array = []       # every other gear mesh
var body_ink: MeshInstance3D


func _arg(key: String, dflt: String) -> String:
	var a := OS.get_cmdline_user_args()
	var i := a.find("--" + key)
	return String(a[i + 1]) if i >= 0 and i + 1 < a.size() else dflt


func _initialize() -> void:
	out_dir = _arg("out", "")
	DirAccess.make_dir_recursive_absolute(out_dir)
	cls = ImageTexture.create_from_image(Image.load_from_file(_arg("class", "")))
	var variants := _arg("variants", ",".join(PackedStringArray(ALL_VARIANTS))).split(",")
	var heads := _arg("headings", "S,SE,E,NE,N,NW,W,SW").split(",")
	var shots := []
	for s in _arg("shots", "idle@1.0,walk@0.5,cast_fireball_m@0.2667").split(","):
		shots.append([s.split("@")[0], float(s.split("@")[1])])
	scene = load("res://scenes/barrow_painted.tscn").instantiate()
	root.add_child(scene)
	while not scene.ready_done:
		await process_frame
	var v = scene.get("veil")
	while v != null and not v.stage_done():
		await process_frame
	for f in 30:
		await process_frame
	scene.set_hud_visible(false)
	for c in scene.get_children():
		if c is CanvasLayer:
			(c as CanvasLayer).visible = false
	if scene.heather_mat != null:
		scene.heather_mat.set_shader_parameter("wind_on", 0.0)
	if scene.snowfall != null:
		scene.snowfall.visible = false
		scene.snowfall.emitting = false
	k = scene.knight
	skel = k._skel
	body_ink = k._outline
	for nm in (k.gear["_pieces"] as Dictionary):
		if String(nm).begins_with("_markers_"):
			continue
		for mi in (k.gear["_pieces"][nm] as Array):
			if not (mi as MeshInstance3D).visible:
				continue
			if String(nm) == "hood":
				hood_mis.append(mi)
			else:
				gear_mis.append(mi)
	rep["who"] = scene.who; rep["slot"] = scene.slot; rep["gear_stack"] = k.gear_stack
	rep["hood_meshes"] = hood_mis.size(); rep["other_gear_meshes"] = gear_mis.size()
	rep["body_ink"] = body_ink != null and body_ink.visible
	rep["morphs"] = {}
	for i in k._mesh.mesh.get_blend_shape_count():
		rep["morphs"][String(k._mesh.mesh.get_blend_shape_name(i))] = k._mesh.get_blend_shape_value(i)
	if body_ink != null:
		var inkm := {}
		for i in body_ink.mesh.get_blend_shape_count():
			inkm[String(body_ink.mesh.get_blend_shape_name(i))] = body_ink.get_blend_shape_value(i)
		rep["body_ink_morphs"] = inkm
	# FREEZE: no tree, no physics on her; the player is the pose
	k._tree.active = false
	k.set_physics_process(false)
	k._anim.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	for shot in shots:
		for h in heads:
			await _pose(String(shot[0]), float(shot[1]), String(h))
			for zoom in [1, 3]:
				scene.park_camera(scene.aim_for(k.global_position), float(zoom))
				for vname in variants:
					for part in String(vname).split("+"):
						await _variant(part, true)
					var base := "%s/%s_%s_%s_z%d" % [out_dir, vname, shot[0], h, zoom]
					await _shoot(base + "_beauty.png", zoom)
					if zoom == 3 and String(vname).split("+")[0] in ID_VARIANTS:
						PaintStack.post_set(scene.post_mat, "ink_on", 0.0)
						await _shoot(base + "_nopen.png", zoom)
						PaintStack.post_set(scene.post_mat, "ink_on", 1.0)
						await _id_pass("a"); await _shoot(base + "_ida.png", zoom); _restore_all()
					if String(vname) in ["live", "headzero"]:
						await _id_pass("foot"); await _shoot(base + "_foot.png", zoom); _restore_all()
					var parts := String(vname).split("+"); parts.reverse()
					for part in parts:
						await _variant(part, false)
			var hp := _head_pitch()
			rep["poses"].append({"clip": shot[0], "t": shot[1], "heading": h, "head": hp})
			print("[face233] %s@%.4f %s head %s" % [shot[0], shot[1], h, JSON.stringify(hp)])
	var f2 := FileAccess.open(out_dir.path_join("face233.json"), FileAccess.WRITE)
	f2.store_string(JSON.stringify(rep, " "))
	f2.close()
	print("[face233] done ", JSON.stringify({"poses": rep["poses"].size(), "variants": variants, "gear_stack": rep["gear_stack"]}))
	quit(0)


func _pose(clip: String, t: float, h: String) -> void:
	scene.place_knight(SPOT.x, SPOT.y, h)
	k._anim.play(clip)
	k._anim.seek(t, true)
	k._anim.pause()
	k._anim.advance(0.0)
	for f in 4:
		await process_frame


func _head_world() -> Vector3:
	var i := skel.find_bone("Head")
	return skel.global_transform * skel.get_bone_global_pose(i).origin


func _head_pitch() -> Dictionary:
	# the head's rest-forward through the posed bone, world frame (the probe's own cross-check of r233_02's FK)
	var out := {}
	for b in ["Head", "neck"]:
		var i := skel.find_bone(b)
		var rest_g := skel.get_bone_global_rest(i).basis.orthonormalized()
		var pose_g := skel.get_bone_global_pose(i).basis.orthonormalized()
		var sk := skel.global_basis.orthonormalized()
		# her facing in the world: the rest head forward is the rig's forward
		var f_local: Vector3 = rest_g.inverse() * (sk.inverse() * (k._rig.global_basis.orthonormalized() * k._forward_axis)).normalized()
		var f: Vector3 = (sk * pose_g * f_local).normalized()
		out[b] = snappedf(rad_to_deg(asin(clampf(-f.y, -1.0, 1.0))), 0.01)
	return out


func _shoot(path: String, zoom: int) -> void:
	for f in 3:
		await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	var sp: Vector2 = scene.cam.unproject_position(_head_world())
	var c: int = crops[zoom]
	var x := clampi(int(sp.x) - c / 2, 0, img.get_width() - c)
	var y := clampi(int(sp.y) - c / 2, 0, img.get_height() - c)
	img.get_region(Rect2i(x, y, c, c)).save_png(path)


# --- variants --------------------------------------------------------------------------------------------------------
var _fill: DirectionalLight3D
var _thin_save := {}
var _headsave := {}
var _nfh := {}


func _discard_variant(m: Material) -> Material:
	var sm := m as ShaderMaterial
	if sm == null or sm.shader == null:
		return m
	var code := sm.shader.code
	assert(code.contains("void fragment() {"), "no fragment() in the material to discard from")
	code = code.replace("void fragment() {", "uniform sampler2D r233_hide : filter_nearest;\nvoid fragment() {\n\tif (texture(r233_hide, UV).g > 0.5) { discard; }")
	var sh := Shader.new(); sh.code = code
	var nm := ShaderMaterial.new(); nm.shader = sh
	for u in sm.shader.get_shader_uniform_list():
		var key := String(u["name"])
		nm.set_shader_parameter(key, sm.get_shader_parameter(key))
	nm.set_shader_parameter("r233_hide", cls)
	return nm


func _variant(v: String, on: bool) -> void:
	match v:
		"nofronthair":
			for mi in [k._mesh, body_ink]:
				if mi == null:
					continue
				if on:
					_nfh[mi] = mi.material_override
					mi.material_override = _discard_variant(mi.material_override)
				else:
					mi.material_override = _nfh[mi]
		"nohood":
			for mi in hood_mis:
				(mi as MeshInstance3D).visible = not on
				var ink = (mi as MeshInstance3D).get_meta("ink", null)
				if ink != null:
					(ink as MeshInstance3D).visible = not on
		"thin", "thinall":
			# R-C9-236: THE WEB PEN AT ITS "THIN" STRENGTH on her: her ramp material(s) write the pen's THIN stencil class
			# (PaintStack.stencil_write, STENCIL_THIN -- the class the heather and twigs write; the post pass draws a line
			# whose NEAR side is that class at thin_pen_scale, 0.28). "thin" = her BODY only (face, neck, tucked hair: the
			# lines inside the opening whose near side is her face), so the hood's own lines -- its silhouette and the
			# opening's rim, whose near side is the hood -- stay full; "thinall" = body and every gear piece
			var tg: Array = [k._mesh] if v == "thin" else [k._mesh] + hood_mis + gear_mis
			for mi in tg:
				if on:
					_thin_save[mi] = (mi as MeshInstance3D).material_override
					var sm := (mi as MeshInstance3D).material_override as ShaderMaterial
					var sh := Shader.new(); sh.code = PaintStack.stencil_write(sm.shader.code, PaintStack.STENCIL_THIN)
					var nm := ShaderMaterial.new(); nm.shader = sh
					for u in sm.shader.get_shader_uniform_list():
						nm.set_shader_parameter(String(u["name"]), sm.get_shader_parameter(String(u["name"])))
					(mi as MeshInstance3D).material_override = nm
				else:
					(mi as MeshInstance3D).material_override = _thin_save[mi]
		"thinlining":
			# the hood's LINING surfaces (index >= 2: r233_05 appends them after the shell and the cap) at the THIN pen
			# strength, the shell and cap at full: the brim's underside seen through the opening is the lining, so its
			# lines thin, while the hood's silhouette (near side: the outer shell) keeps its full line
			for mi in hood_mis:
				var hm := mi as MeshInstance3D
				if on:
					var ramp := hm.material_override as ShaderMaterial
					_thin_save[hm] = ramp
					var sh := Shader.new(); sh.code = PaintStack.stencil_write(ramp.shader.code, PaintStack.STENCIL_THIN)
					var nm := ShaderMaterial.new(); nm.shader = sh
					for u in ramp.shader.get_shader_uniform_list():
						nm.set_shader_parameter(String(u["name"]), ramp.get_shader_parameter(String(u["name"])))
					hm.material_override = null
					for s in hm.mesh.get_surface_count():
						hm.set_surface_override_material(s, nm if s >= 2 else ramp)
				else:
					for s in hm.mesh.get_surface_count():
						hm.set_surface_override_material(s, null)
					hm.material_override = _thin_save[hm]
		"headzero":
			for b in ["Head", "neck"]:
				var i := skel.find_bone(b)
				if on:
					_headsave[b] = skel.get_bone_pose_rotation(i)
					skel.set_bone_pose_rotation(i, skel.get_bone_rest(i).basis.get_rotation_quaternion())
				else:
					skel.set_bone_pose_rotation(i, _headsave[b])
		"fill":
			if on:
				_fill = DirectionalLight3D.new()
				_fill.light_cull_mask = CHAR_LAYER
				_fill.light_energy = 0.55
				_fill.light_color = Color(1.0, 0.95, 0.88)
				_fill.shadow_enabled = false
				scene.add_child(_fill)
				# the light travels the way the camera looks: it lights what faces the camera
				var d: Vector3 = -scene.cam.global_basis.z
				_fill.look_at_from_position(Vector3.ZERO, d, Vector3.UP)
			else:
				_fill.queue_free()
				_fill = null
		"inksync":
			if on:
				_save_ink_morphs()
				_sync_ink()
			else:
				_restore_ink_morphs()
		"fixA", "fixB", "fixC", "fixD", "fixE", "fixF", "fixG":
			if on:
				_swap_body(_arg(v, ""))
				if _arg(v + "_hood", "") != "":
					_swap_hood(_arg(v + "_hood", ""))
			else:
				if not _hood_save.is_empty():
					_unswap_hood()
				_unswap_body()
		"noink":
			PaintStack.post_set(scene.post_mat, "ink_on", 0.0 if on else 1.0)
	for f in 2:
		await process_frame


# --- STEP 1: the body swap and the ink's morphs ---------------------------------------------------------------------
var _ink_save := {}
var _swap_save := {}
var _glb_cache := {}


func _morphs_of(mi: MeshInstance3D) -> Dictionary:
	var d := {}
	for i in mi.mesh.get_blend_shape_count():
		d[String(mi.mesh.get_blend_shape_name(i))] = mi.get_blend_shape_value(i)
	return d


func _apply_morphs(mi: MeshInstance3D, d: Dictionary) -> void:
	for i in mi.mesh.get_blend_shape_count():
		var n := String(mi.mesh.get_blend_shape_name(i))
		mi.set_blend_shape_value(i, float(d.get(n, 0.0)))


func _save_ink_morphs() -> void:
	if body_ink != null:
		_ink_save = _morphs_of(body_ink)


func _restore_ink_morphs() -> void:
	if body_ink != null:
		_apply_morphs(body_ink, _ink_save)


func _sync_ink() -> void:
	if body_ink != null:
		_apply_morphs(body_ink, _morphs_of(k._mesh))


func _swap_body(path: String) -> void:
	assert(path != "", "no GLB for the fix variant")
	if not _glb_cache.has(path):
		# res:// = IMPORTED by the project exactly as her shipped body is (LODs, the extracted atlas): the parity the
		# control (an imported byte copy of ss152b) checks; a file path = loaded raw (NOT comparable to live)
		var sc: Node
		if path.begins_with("res://"):
			sc = (load(path) as PackedScene).instantiate()
		else:
			var doc := GLTFDocument.new(); var st := GLTFState.new()
			assert(doc.append_from_file(path, st) == OK, "glTF load failed: " + path)
			sc = doc.generate_scene(st)
		var found: MeshInstance3D = null
		for m in sc.find_children("*", "MeshInstance3D", true, false):
			if (m as MeshInstance3D).skin != null and (m as MeshInstance3D).mesh.get_blend_shape_count() > 0:
				found = m
		assert(found != null, "no skinned body in " + path)
		var mat := found.get_active_material(0) as BaseMaterial3D
		_glb_cache[path] = {"mesh": found.mesh, "tex": mat.albedo_texture if mat != null else null}
		sc.queue_free()
	var e: Dictionary = _glb_cache[path]
	var morphs := _morphs_of(k._mesh)
	var ramp := k._mesh.material_override as ShaderMaterial
	_swap_save = {"mesh": k._mesh.mesh, "ink_mesh": body_ink.mesh if body_ink != null else null, "morphs": morphs,
		"ink_morphs": _morphs_of(body_ink) if body_ink != null else {}, "tex": ramp.get_shader_parameter("albedo_tex") if ramp != null else null}
	k._mesh.mesh = e["mesh"]
	_apply_morphs(k._mesh, morphs)
	if body_ink != null:
		body_ink.mesh = e["mesh"]
		_apply_morphs(body_ink, morphs)
	if ramp != null and e["tex"] != null:
		ramp.set_shader_parameter("albedo_tex", e["tex"])


func _unswap_body() -> void:
	var ramp := k._mesh.material_override as ShaderMaterial
	k._mesh.mesh = _swap_save["mesh"]
	_apply_morphs(k._mesh, _swap_save["morphs"])
	if body_ink != null:
		body_ink.mesh = _swap_save["ink_mesh"]
		_apply_morphs(body_ink, _swap_save["ink_morphs"])
	if ramp != null and _swap_save["tex"] != null:
		ramp.set_shader_parameter("albedo_tex", _swap_save["tex"])


var _hood_save := {}


func _swap_hood(path: String) -> void:
	# the hood's mesh from an IMPORTED hood GLB (a lining added): its own ramp material (the hood atlas) is kept
	var sc := (load(path) as PackedScene).instantiate()
	var found: MeshInstance3D = null
	for m in sc.find_children("*", "MeshInstance3D", true, false):
		if (m as MeshInstance3D).skin != null:
			found = m
	assert(found != null, "no skinned hood in " + path)
	var hm := hood_mis[0] as MeshInstance3D
	_hood_save = {"mi": hm, "mesh": hm.mesh}
	hm.mesh = found.mesh
	sc.queue_free()


func _unswap_hood() -> void:
	(_hood_save["mi"] as MeshInstance3D).mesh = _hood_save["mesh"]
	_hood_save = {}


# --- ID passes -------------------------------------------------------------------------------------------------------
func _flat(c: Color, ink_w := -1.0) -> ShaderMaterial:
	var sh := Shader.new()
	if ink_w >= 0.0:
		sh.code = "shader_type spatial;\nrender_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled, fog_disabled;\nuniform float width_model = 0.01;\nuniform vec3 col;\nvoid vertex() { VERTEX += normalize(NORMAL) * width_model; }\nvoid fragment() { ALBEDO = col; }\n"
	else:
		sh.code = "shader_type spatial;\nrender_mode unshaded, cull_back, shadows_disabled, fog_disabled;\nuniform vec3 col;\nvoid fragment() { ALBEDO = col; }\n"
	var m := ShaderMaterial.new(); m.shader = sh
	m.set_shader_parameter("col", Vector3(c.r, c.g, c.b))
	if ink_w >= 0.0:
		m.set_shader_parameter("width_model", ink_w)
	return m


func _body_id(foot: bool, hide_front: bool, solid := false) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode unshaded, cull_back, shadows_disabled, fog_disabled;\nuniform sampler2D cls : filter_nearest;\nuniform float foot = 0.0;\nuniform float hide_front = 0.0;\nuniform float solid = 0.0;\nvoid fragment() {\n\tvec3 c = texture(cls, UV).rgb;\n\tvec3 o = vec3(1.0, 1.0, 0.0);\n\tif (c.r > 0.5) { o = vec3(1.0, 0.0, 0.0); } else if (c.g > 0.5) { o = vec3(0.0, 1.0, 0.0); if (hide_front > 0.5) { discard; } } else if (c.b > 0.5) { o = vec3(0.0, 1.0, 1.0); }\n\tif (foot > 0.5 && c.r < 0.5) { discard; }\n\tif (solid > 0.5) { o = vec3(1.0, 1.0, 0.0); }\n\tALBEDO = o;\n}\n"
	var m := ShaderMaterial.new(); m.shader = sh
	m.set_shader_parameter("cls", cls)
	m.set_shader_parameter("foot", 1.0 if foot else 0.0)
	m.set_shader_parameter("hide_front", 1.0 if hide_front else 0.0)
	m.set_shader_parameter("solid", 1.0 if solid else 0.0)
	return m


func _ink_w(ink: MeshInstance3D) -> float:
	var sm := ink.material_override as ShaderMaterial
	if sm != null and sm.get_shader_parameter("width_model") != null:
		return float(sm.get_shader_parameter("width_model"))
	return 0.011


func _keep(mi: MeshInstance3D) -> void:
	if not saved_mat.has(mi):
		saved_mat[mi] = mi.material_override
		saved_vis[mi] = mi.visible


func _id_pass(kind: String) -> void:
	scene.post_q.visible = false
	var hide_front := false
	if _nfh.has(k._mesh) and k._mesh.material_override != _nfh[k._mesh]:
		hide_front = true            # the nofronthair variant is on: its ID pass discards the same texels
	_keep(k._mesh)
	if kind == "foot":
		k._mesh.material_override = _body_id(true, false)
		for mi in hood_mis + gear_mis:
			_keep(mi); (mi as MeshInstance3D).visible = false
		var inks := [body_ink]
		for mi in hood_mis + gear_mis:
			inks.append((mi as MeshInstance3D).get_meta("ink", null))
		for ink in inks:
			if ink != null:
				_keep(ink); (ink as MeshInstance3D).visible = false
	elif kind == "a":
		k._mesh.material_override = _body_id(false, hide_front)
		for mi in hood_mis:
			_keep(mi); (mi as MeshInstance3D).material_override = _flat(Color(0, 0, 1))
		for mi in gear_mis:
			_keep(mi); (mi as MeshInstance3D).material_override = _flat(Color(1, 0, 1))
		var inks := [body_ink]
		for mi in hood_mis + gear_mis:
			inks.append((mi as MeshInstance3D).get_meta("ink", null))
		for ink in inks:
			if ink != null:
				_keep(ink); (ink as MeshInstance3D).visible = false
	else:
		k._mesh.material_override = _body_id(false, hide_front, true)
		for mi in hood_mis + gear_mis:
			_keep(mi); (mi as MeshInstance3D).material_override = _flat(Color(1, 1, 0))
		if body_ink != null:
			_keep(body_ink); var bim := _flat(Color(0, 1, 0), _ink_w(body_ink)); body_ink.material_override = _discard_variant(bim) if hide_front else bim
		for mi in hood_mis:
			var ink = (mi as MeshInstance3D).get_meta("ink", null)
			if ink != null:
				_keep(ink); (ink as MeshInstance3D).material_override = _flat(Color(1, 0, 0), _ink_w(ink))
		for mi in gear_mis:
			var ink = (mi as MeshInstance3D).get_meta("ink", null)
			if ink != null:
				_keep(ink); (ink as MeshInstance3D).material_override = _flat(Color(0, 0, 1), _ink_w(ink))
	for f in 2:
		await process_frame


func _restore_all() -> void:
	for mi in saved_mat:
		(mi as MeshInstance3D).material_override = saved_mat[mi]
		(mi as MeshInstance3D).visible = saved_vis[mi]
	saved_mat.clear()
	saved_vis.clear()
	scene.post_q.visible = true
