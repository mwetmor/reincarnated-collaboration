extends RefCounted
class_name CharGear
## C-9 D2 (gate G3): the barbarian's modular gear, loaded by manifest.
##
## THE MANIFEST DECLARES THREE BIND MODES AND THE FILES CARRY ONE. It lists `bone` for the
## helmet and bracers, `skin` for the byrnie and mantle, and `socket` for the axe and
## shield -- which is a faithful description of how they were AUTHORED. What was exported
## is another matter, and it is the exported file that has to be bound: every piece,
## including both sockets, arrives as a SKINNED mesh carrying a 24-bone skeleton whose bone
## names are identical to the body's, in the same order (measured, tools/probe_gear.gd).
##
## So all six bind the same way -- reparent under the body's own Skeleton3D, keep the skin,
## point `skeleton` at it -- and that is not a shortcut. A socketed axe would need a
## BoneAttachment3D plus a hand-fitted offset, and an offset fitted by eye is a number
## nobody can check; a skin weighted to RightHand puts the axe where the artist put it, and
## the rig moves it. The manifest's mode is kept in the record beside what was found, and
## where they disagree the file wins.
##
## `offset_m` is likewise already in the geometry -- the byrnie's 5 mm and the mantle's
## 8 mm are baked shells, not a runtime push -- so nothing is displaced here. Poke-through
## is therefore a MEASUREMENT of the export, not something this code can tune away, and it
## is measured per clip in tools/probe_poke.gd.

const CHAR_LAYER := 4
const LINE_PX := 1.1
const PPM := 100.617553710938


static func build(body_skel: Skeleton3D, manifest_path: String, dir: String,
				  figure_scale: float, mesh_scale: float) -> Dictionary:
	"""Every piece, bound to the body's skeleton and hidden. Returns piece -> [meshes]."""
	var out := {"_pieces": {}, "_report": {}}
	if not FileAccess.file_exists(manifest_path):
		return out
	var mf = JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
	if typeof(mf) != TYPE_DICTIONARY:
		return out
	var body_names := []
	for i in body_skel.get_bone_count():
		body_names.append(body_skel.get_bone_name(i))
	var pieces := {}
	var report := {}
	for spec in mf.get("pieces", []):
		var name := String(spec["piece"])
		var path := dir + "/" + String(spec["glb"])
		if not ResourceLoader.exists(path):
			report[name] = {"error": "missing " + path}
			continue
		var src := (load(path) as PackedScene).instantiate()
		# the source skeleton, so its bone order can be checked against the body's
		var ssk: Skeleton3D = null
		for n in src.find_children("*", "Skeleton3D", true, false):
			ssk = n
		var snames := []
		if ssk != null:
			for i in ssk.get_bone_count():
				snames.append(ssk.get_bone_name(i))
		var taken: Array[MeshInstance3D] = []
		var tris := 0
		var empties := 0
		for m in src.find_children("*", "MeshInstance3D", true, false):
			var mi := m as MeshInstance3D
			if mi.mesh == null:
				continue
			var t := 0
			for s in mi.mesh.get_surface_count():
				var ix = mi.mesh.surface_get_arrays(s)[Mesh.ARRAY_INDEX]
				t += (ix.size() / 3) if ix != null else 0
			tris += t
			if t <= 8:
				empties += 1
			var local := mi.transform          # relative to the source Skeleton3D
			var skin := _bind_by_name(mi)
			var mat := mi.get_active_material(0)
			mi.owner = null                    # it belongs to the source scene until it does not
			mi.get_parent().remove_child(mi)
			body_skel.add_child(mi)
			mi.transform = local               # the same place under an identical rig
			mi.skin = skin
			mi.skeleton = NodePath("..")
			mi.visible = false
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			_style(mi, mat)
			_set_layer(mi, CHAR_LAYER)
			_add_outline(mi, figure_scale, mesh_scale)
			taken.append(mi)
		# MARKERS COME ACROSS TOO. axe.glb carries a Node3D named `axe_edge` under a
		# RightHand BoneAttachment3D -- the edge marker the last report asked for. Taking
		# only the MeshInstance3D and freeing the source drops it, and the one thing it
		# exists to answer goes back to being unanswerable. Recreate the attachment on the
		# body's own skeleton and hang the marker off it with the same local transform.
		var marks := {}
		for n in src.find_children("*", "Node3D", true, false):
			var par := n.get_parent()
			if not (par is BoneAttachment3D):
				continue
			if n is MeshInstance3D or n is Skeleton3D:
				continue
			var att := BoneAttachment3D.new()
			att.name = name + "_" + String((par as BoneAttachment3D).bone_name)
			att.bone_name = (par as BoneAttachment3D).bone_name
			body_skel.add_child(att)
			var mk := Node3D.new()
			mk.name = String(n.name)
			att.add_child(mk)
			mk.transform = (n as Node3D).transform
			marks[String(n.name)] = mk
		src.queue_free()
		pieces[name] = taken
		if not marks.is_empty():
			pieces["_markers_" + name] = marks
		report[name] = {
			"glb": String(spec["glb"]),
			"manifest_mode": String(spec.get("mode", "?")),
			"found": "skinned mesh on a skeleton whose bones match the body" if snames == body_names \
				else ("skinned, but a DIFFERENT skeleton" if ssk != null else "no skeleton"),
			"bones_match_body": snames == body_names,
			"meshes": taken.size(),
			"triangles": tris,
			"near_empty_objects": empties,
			"manifest_bones": spec.get("bones", []),
			"manifest_offset_m": spec.get("offset_m", 0.0),
			"markers": marks.keys(),
		}
	out["_pieces"] = pieces
	out["_report"] = report
	out["layer_order"] = mf.get("layer_order", [])
	return out


static func _bind_by_name(mi: MeshInstance3D) -> Skin:
	"""C-9 BIND-ORDER (the coordinator, after wl_e1 stage K): bind every piece's skin by bone NAME, taken from the
	piece's OWN skeleton. Godot builds each GLB's Skeleton3D in that file's node order, and a bind left on a bone INDEX
	lands on whatever bone holds that index on the body -- right only while the piece's file order equals the body's
	(the barbarian's own set; not a Blender-exported piece). A bind that already carries a name keeps it. The reference
	is _bind() in wl_e1/film_rt/gear_stills.gd (GS_BIND_BY_NAME). Fenced by tools/probe_bind_order.gd."""
	var skin := mi.skin
	var ps := mi.get_node_or_null(mi.skeleton) as Skeleton3D
	if skin == null or ps == null:
		return skin
	skin = skin.duplicate() as Skin
	for bi in skin.get_bind_count():
		var bb := skin.get_bind_bone(bi)
		if String(skin.get_bind_name(bi)) == "" and bb >= 0 and bb < ps.get_bone_count():
			skin.set_bind_name(bi, ps.get_bone_name(bb))
	return skin


static func _style(mi: MeshInstance3D, src: Material) -> void:
	"""Lit, like the body: the gear is the one thing in this scene that is not painted."""
	var b := src as BaseMaterial3D
	var m := StandardMaterial3D.new()
	if b != null:
		m.albedo_texture = b.albedo_texture if b.albedo_texture != null else b.emission_texture
	m.roughness = 0.58
	m.metallic = 0.30
	mi.material_override = m


static func _set_layer(n: Node, layer: int) -> void:
	if n is VisualInstance3D:
		(n as VisualInstance3D).layers = layer
	for c in n.get_children():
		_set_layer(c, layer)


static func _add_outline(mi: MeshInstance3D, figure_scale: float, mesh_scale: float) -> void:
	"""The ink line has to follow the GEAR silhouette too, or a helmeted head is drawn
	inside a line that still traces a bare one."""
	var sh := Shader.new()
	sh.code = """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled;
uniform float width_model = 0.01;
uniform vec4 line_color : source_color = vec4(0.055, 0.043, 0.063, 1.0);
void vertex() { VERTEX += normalize(NORMAL) * width_model; }
void fragment() { ALBEDO = line_color.rgb; }
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("width_model",
		(LINE_PX / PPM) / maxf(figure_scale * mesh_scale, 1e-9))
	var o := MeshInstance3D.new()
	o.name = mi.name + "_ink"
	o.mesh = mi.mesh
	o.skin = mi.skin
	mi.get_parent().add_child(o)
	o.transform = mi.transform
	o.skeleton = NodePath("..")
	o.material_override = mat
	o.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	o.visible = false
	mi.set_meta("ink", o)


static func show_pieces(gear: Dictionary, on: Array) -> void:
	for name in (gear["_pieces"] as Dictionary):
		if String(name).begins_with("_markers_"):
			continue
		var want: bool = on.has(name)
		for mi in (gear["_pieces"][name] as Array):
			(mi as MeshInstance3D).visible = want
			var ink = (mi as MeshInstance3D).get_meta("ink", null)
			if ink != null:
				(ink as MeshInstance3D).visible = want
