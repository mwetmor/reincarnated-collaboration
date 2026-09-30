extends RefCounted
class_name BarrowInstancer
## C-9 T10-1c -- REPEATED PROPS AS MULTIMESHES. The ceiling on density.
##
## T10-1b measured every Tripo prop at ~25 us of frame time WHATEVER ITS SIZE ON SCREEN -- a
## 0.4 m rock as much as a 1.6 m one -- while a 272-face procedural heather cost ~1 us. That is
## per-instance cost: a draw, a material bind and a full-detail mesh in each of four passes,
## for every copy of the same rock. 305 props was the budget's edge; the full-area build wants
## thousands.
##
## So each repeated asset becomes ONE MultiMeshInstance3D per spatial chunk: one material, one
## draw per pass per chunk, however many copies are in it. Two things make that honest rather
## than just fewer draws:
##
##   THE MESH IS DECIMATED HERE, ONCE. A MultiMesh picks ONE level of detail for the whole
##     draw, from its whole AABB -- and a chunk several metres across projects large, so it
##     would pick full detail for every copy. That turns the per-instance overhead into a
##     per-triangle one of the same size. Instead each asset is reduced to a target triangle
##     count with the same meshoptimizer the importer uses (ImporterMesh.generate_lods), at
##     load, and the instances draw that.
##   THE PEN COMES WITH IT. A hull line is an inflated copy of the mesh; instanced, it is a
##     second MultiMesh of the same decimated mesh whose inflation is PER INSTANCE, carried in
##     INSTANCE_CUSTOM.x -- because each copy is scaled differently and the hull's width is
##     applied in model space, before the scale.
##
## Chunked so the frustum still culls: a chunk off-screen costs nothing.

const HULL_INK_MM_SHADER := """
shader_type spatial;
render_mode unshaded, cull_front, depth_draw_opaque, shadows_disabled, fog_disabled;
uniform vec4 line_color : source_color = vec4(0.113, 0.082, 0.067, 1.0);
// the per-instance width, model space, from INSTANCE_CUSTOM.x -- see the header
void vertex() { VERTEX += normalize(NORMAL) * INSTANCE_CUSTOM.x; }
void fragment() { ALBEDO = line_color.rgb; }
"""

static var _lod_cache := {}
static var _ink_shader: Shader


static func decimate(mesh: Mesh, target_tris: int) -> Dictionary:
	"""The mesh at or under `target_tris`, from meshoptimizer's own LOD chain. Cached by mesh
	and target. Falls back to the mesh itself -- and SAYS so -- if it has no triangles to spare
	or the LOD chain cannot be built."""
	var key := "%d|%d" % [mesh.get_instance_id(), target_tris]
	if _lod_cache.has(key):
		return _lod_cache[key]
	var full := 0
	for s in mesh.get_surface_count():
		var ix = mesh.surface_get_arrays(s)[Mesh.ARRAY_INDEX]
		full += (ix.size() / 3) if ix != null else 0
	var out := {"mesh": mesh, "tris_full": full, "tris": full, "decimated": false, "why": ""}
	if full <= target_tris:
		out["why"] = "already under target"
		_lod_cache[key] = out
		return out
	var im := ImporterMesh.new()
	for s in mesh.get_surface_count():
		im.add_surface(Mesh.PRIMITIVE_TRIANGLES, mesh.surface_get_arrays(s))
	im.generate_lods(25.0, 60.0, [])
	var am := ArrayMesh.new()
	var got := 0
	for s in im.get_surface_count():
		var arrs := im.get_surface_arrays(s)
		var best: PackedInt32Array = arrs[Mesh.ARRAY_INDEX]
		for l in im.get_surface_lod_count(s):
			var idx: PackedInt32Array = im.get_surface_lod_indices(s, l)
			# the coarsest LOD still at or above a third of the target, else the first under it
			if idx.size() / 3 <= target_tris:
				best = idx
				break
			best = idx
		arrs[Mesh.ARRAY_INDEX] = best
		am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrs)
		got += best.size() / 3
	if got <= 0 or got >= full:
		out["why"] = "no LOD under the full mesh"
		_lod_cache[key] = out
		return out
	out = {"mesh": am, "tris_full": full, "tris": got, "decimated": true, "why": ""}
	_lod_cache[key] = out
	return out


static func ink_material(ink: Color) -> ShaderMaterial:
	if _ink_shader == null:
		_ink_shader = Shader.new()
		_ink_shader.code = HULL_INK_MM_SHADER
	var m := ShaderMaterial.new()
	m.shader = _ink_shader
	m.set_shader_parameter("line_color", ink)
	return m


static func build(parent: Node3D, entries: Array, chunk_m: float, ink: Color,
		targets: Dictionary) -> Dictionary:
	"""entries: [{key, asset, mesh, mat, xf (world Transform3D), hull_world_m, scale,
	shadow (bool)}]. Groups by key (asset + source mesh), decimates each mesh once, and builds
	one MultiMeshInstance3D per key per chunk, plus its ink twin where hull_world_m > 0."""
	var groups := {}
	for e in entries:
		var c: Vector3 = (e["xf"] as Transform3D).origin
		var ck := "%s|%d|%d" % [e["key"], int(floor(c.x / chunk_m)), int(floor(c.z / chunk_m))]
		if not groups.has(ck):
			groups[ck] = []
		groups[ck].append(e)
	var ink_mat := ink_material(ink)
	var mmis := []
	var inks := []
	var per_asset := {}
	for ck in groups:
		var arr: Array = groups[ck]
		var e0: Dictionary = arr[0]
		var d := decimate(e0["mesh"], int(targets.get(e0["asset"], 1500)))
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.use_custom_data = true
		mm.mesh = d["mesh"]
		mm.instance_count = arr.size()
		for i in arr.size():
			var e: Dictionary = arr[i]
			mm.set_instance_transform(i, e["xf"])
			var sc: float = maxf(float(e.get("scale", 1.0)), 1e-6)
			mm.set_instance_custom_data(i, Color(float(e.get("hull_world_m", 0.0)) / sc, 0, 0, 0))
		var mmi := MultiMeshInstance3D.new()
		mmi.name = "MM_" + String(ck).replace("|", "_")
		mmi.multimesh = mm
		mmi.material_override = e0["mat"]
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if bool(e0.get("shadow", true)) \
			else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mmi.set_meta("asset", e0["asset"])
		mmi.set_meta("part", String(e0.get("part", "")))
		parent.add_child(mmi)
		mmis.append(mmi)
		if float(e0.get("hull_world_m", 0.0)) > 0.0:
			var line := MultiMeshInstance3D.new()
			line.name = mmi.name + "_ink"
			line.multimesh = mm
			line.material_override = ink_mat
			line.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			line.set_meta("asset", e0["asset"])
			line.set_meta("part", String(e0.get("part", "")))
			parent.add_child(line)
			inks.append(line)
		var pa: Dictionary = per_asset.get(e0["asset"], {"instances": 0, "chunks": 0,
			"tris_full": d["tris_full"], "tris_drawn": d["tris"], "decimated": d["decimated"]})
		pa["instances"] = int(pa["instances"]) + arr.size()
		pa["chunks"] = int(pa["chunks"]) + 1
		per_asset[e0["asset"]] = pa
	return {"mmis": mmis, "inks": inks, "per_asset": per_asset}


static func set_transforms(mmis: Array, asset: String, xfs_by_chunk: Dictionary) -> void:
	"""Re-pose one asset's instances in place -- the rocks' upright/low A-B -- without
	rebuilding the MultiMeshes: same chunks, same order, new transforms."""
	for mmi in mmis:
		var m := mmi as MultiMeshInstance3D
		if String(m.get_meta("asset", "")) != asset or not xfs_by_chunk.has(m.name):
			continue
		var xs: Array = xfs_by_chunk[m.name]
		for i in mini(xs.size(), m.multimesh.instance_count):
			m.multimesh.set_instance_transform(i, xs[i])
