extends RefCounted
class_name BarrowStandIn
## C-9 T10 — THE STAND-IN BARROW, generated in code, at TRUE METRES.
##
## The point of this file is that the render stack can be judged BEFORE the real terrain and
## the real Tripo assets exist. It is deliberately primitive -- a heightfield, tapered
## prisms, displaced spheres, tapered trunks -- because anything more would start to be an
## opinion about the world's art, which is another drax's work and Matt's call.
##
## WHAT IT MUST GET RIGHT is scale and surface variety, because those are what the stack is
## measured against:
##   a gentle snowy HILL, so the ramp has a long slow N.L gradient to band across;
##   a barrow MOUND, so there is a convex form with a rim to outline;
##   a shallow BASIN, so the height fog has somewhere to pool;
##   STANDING STONES at 3.5 m and ROCKS at 1-2 m, so the snow layer has surfaces at every
##     angle between flat and vertical and the report can state a real coverage share;
##   bare BIRCH trunks, because thin geometry is the case a screen-space ink pass fails at,
##     and a stack that has not been shown a 12 cm trunk has not been tested.
##
## ONE HEIGHT FUNCTION. `height_at` is sampled by the render mesh, by the collision trimesh
## and by every prop placement, so a stone cannot float and the knight's ground ray cannot
## disagree with what he is standing on. Two derivations of one surface is how a figure ends
## up 5 cm inside a hill in one frame out of thirty.
##
## Replacing this with the real terrain: keep `height_at` (or hand `place_on_ground` a new
## one), keep TERRAIN_BIT, and the stack needs no change at all -- it reads world position
## and world normal from whatever geometry it is given.

const TERRAIN_BIT := 1 << 1        # knight.gd masks its ground ray to this
const EXTENT := 46.0               # half-size, metres: a 92 m square
const CELL := 0.55                 # metres per quad

# the named places, so the scene and the capture tool refer to the same spots
const MOUND_CENTRE := Vector2(0.0, -4.0)
const MOUND_RADIUS := 6.2
const MOUND_HEIGHT := 3.05
const BASIN_CENTRE := Vector2(-16.5, 12.0)
const BASIN_RADIUS := 7.6
const BASIN_DEPTH := 1.4
const RING_RADIUS := 11.4
const RING_STONES := 9
const HILL_CENTRE := Vector2(23.0, -21.0)
const RIDGE_Y := 8.6               # roughly the crest height, for the gust emitter

# WHERE THE HEIGHTS COME FROM. Null means this file's own procedural surface; set it to a
# BarrowHeightfield (the sibling drax's measured barrow ground, same interface by design)
# and every height this file reports -- terrain, stones, rocks, birches, the spawn -- comes
# from there instead. One branch, one source of truth: props cannot end up placed on a
# surface other than the one drawn, which is the whole reason height_at was a single
# function in the first place.
var height_source = null

var _n1: FastNoiseLite
var _n2: FastNoiseLite
var _n3: FastNoiseLite
var report := {}


func _init() -> void:
	_n1 = FastNoiseLite.new()
	_n1.seed = 20260929
	_n1.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	_n1.frequency = 0.018
	_n2 = FastNoiseLite.new()
	_n2.seed = 771
	_n2.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	_n2.frequency = 0.058
	_n3 = FastNoiseLite.new()
	_n3.seed = 9931
	_n3.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	_n3.frequency = 0.19


func height_at(x: float, z: float) -> float:
	"""THE surface. Metres."""
	if height_source != null:
		return height_source.height_at(x, z)
	var y := 0.0
	y += _n1.get_noise_2d(x, z) * 3.1                      # broad undulation
	y += _n2.get_noise_2d(x, z) * 0.85
	y += _n3.get_noise_2d(x, z) * 0.17                     # the tooth snow settles into
	# the hill, rising away from the play space
	var hd := Vector2(x - HILL_CENTRE.x, z - HILL_CENTRE.y)
	y += 9.4 * exp(-(pow(hd.x / 27.0, 2.0) + pow(hd.y / 23.0, 2.0)))
	# a long crest, so there is a ridge line to lift snow off
	y += 2.1 * exp(-pow((x - 14.0 - (z + 26.0) * 0.20) / 5.4, 2.0)) \
		* clampf(1.0 - absf(z + 18.0) / 30.0, 0.0, 1.0)
	# the barrow itself
	var md := Vector2(x - MOUND_CENTRE.x, z - MOUND_CENTRE.y).length()
	y += MOUND_HEIGHT * exp(-pow(md / MOUND_RADIUS, 2.3))
	# the shallow basin, for the height fog
	var bd := Vector2(x - BASIN_CENTRE.x, z - BASIN_CENTRE.y).length()
	y -= BASIN_DEPTH * exp(-pow(bd / BASIN_RADIUS, 2.0))
	return y


func normal_at(x: float, z: float, eps := 0.28) -> Vector3:
	var hx := height_at(x + eps, z) - height_at(x - eps, z)
	var hz := height_at(x, z + eps) - height_at(x, z - eps)
	return Vector3(-hx, 2.0 * eps, -hz).normalized()


# =============================================================================
#  TERRAIN
# =============================================================================
func build_terrain(parent: Node3D, mat: Material) -> MeshInstance3D:
	var n := int(round(EXTENT * 2.0 / CELL))
	var verts := PackedVector3Array()
	var norms := PackedVector3Array()
	var uvs := PackedVector2Array()
	var idx := PackedInt32Array()
	verts.resize((n + 1) * (n + 1))
	norms.resize((n + 1) * (n + 1))
	uvs.resize((n + 1) * (n + 1))
	for j in n + 1:
		var z := -EXTENT + float(j) * CELL
		for i in n + 1:
			var x := -EXTENT + float(i) * CELL
			var k := j * (n + 1) + i
			verts[k] = Vector3(x, height_at(x, z), z)
			norms[k] = normal_at(x, z)
			uvs[k] = Vector2(x, z) * 0.25
	for j in n:
		for i in n:
			var a := j * (n + 1) + i
			var b := a + 1
			var c := a + (n + 1)
			var d := c + 1
			# GODOT'S FRONT FACE IS CLOCKWISE, so a front-facing triangle's right-hand-rule
			# normal points AWAY from the viewer. This was [a, c, b, b, c, d], whose
			# right-hand normal is +Y -- toward a camera looking down -- which made every
			# ground triangle back-facing. The whole terrain was culled, silently: props,
			# snow, sky and the barbarian all drew, and the world had no floor.
			#
			# I derived "this should render" by hand twice and was wrong twice.
			# tools/probe_terrain.gd settled it in one run by drawing the SAME mesh three
			# ways: CULL_BACK drew nothing, CULL_DISABLED filled the frame, CULL_FRONT drew.
			# That is not a winding argument, it is a winding measurement.
			idx.append_array([a, b, c, b, d, c])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = norms
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.name = "Terrain"
	mi.mesh = am
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	parent.add_child(mi)
	# collision from the SAME arrays, so the ground the ray finds is the ground drawn
	var body := StaticBody3D.new()
	body.name = "TerrainBody"
	body.collision_layer = TERRAIN_BIT
	body.collision_mask = 0
	var cs := CollisionShape3D.new()
	var shape := ConcavePolygonShape3D.new()
	var faces := PackedVector3Array()
	faces.resize(idx.size())
	for t in idx.size():
		faces[t] = verts[idx[t]]
	shape.set_faces(faces)
	cs.shape = shape
	body.add_child(cs)
	parent.add_child(body)
	report["terrain"] = {
		"extent_m": EXTENT * 2.0, "cell_m": CELL,
		"vertices": verts.size(), "triangles": idx.size() / 3,
	}
	return mi


# =============================================================================
#  PROPS — primitives, but at real sizes and with real surfaces
# =============================================================================
func _outward_normals(verts: PackedVector3Array, idx: PackedInt32Array) -> PackedVector3Array:
	"""Smooth normals, pointed OUTWARD BY MEASUREMENT rather than by sign algebra.

	Accumulating right-hand face normals gives a smooth field whose SIGN depends on the
	winding -- and the winding convention is the thing I just got wrong twice in this file.
	So the direction is not argued: for a closed solid the outward normal must, on average,
	agree with (vertex - centroid), and if it does not, every normal is flipped. Costs one
	pass and removes a whole class of "lit from inside" bug that looks like a lighting
	problem and is not one."""
	var nrm := PackedVector3Array()
	nrm.resize(verts.size())
	for i in nrm.size():
		nrm[i] = Vector3.ZERO
	for t in range(0, idx.size(), 3):
		var fn := (verts[idx[t + 1]] - verts[idx[t]]).cross(verts[idx[t + 2]] - verts[idx[t]])
		nrm[idx[t]] += fn
		nrm[idx[t + 1]] += fn
		nrm[idx[t + 2]] += fn
	var centroid := Vector3.ZERO
	for v in verts:
		centroid += v
	centroid /= maxf(float(verts.size()), 1.0)
	var agree := 0.0
	for i in nrm.size():
		var r := verts[i] - centroid
		if r.length() > 1e-6 and nrm[i].length() > 1e-9:
			agree += nrm[i].normalized().dot(r.normalized())
	var flip: float = -1.0 if agree < 0.0 else 1.0
	for i in nrm.size():
		nrm[i] = (nrm[i].normalized() * flip) if nrm[i].length() > 1e-9 else Vector3.UP
	return nrm



func _displaced_sphere(radius: float, squash: Vector3, lumpiness: float,
		seed_i: int, rings := 10, segs := 14) -> ArrayMesh:
	"""A boulder. A SphereMesh's own arrays, pushed along their normals by a noise field, so
	the silhouette is irregular -- which is what the ink pass has to trace. Normals are
	RECOMPUTED from the displaced triangles, not kept: a displaced vertex with its original
	normal lights like the sphere it used to be, and the ramp would band it in smooth rings."""
	var sm := SphereMesh.new()
	sm.radius = radius
	sm.height = radius * 2.0
	sm.radial_segments = segs
	sm.rings = rings
	var src := sm.get_mesh_arrays()
	var v: PackedVector3Array = src[Mesh.ARRAY_VERTEX]
	var uv: PackedVector2Array = src[Mesh.ARRAY_TEX_UV]
	var ix: PackedInt32Array = src[Mesh.ARRAY_INDEX]
	var nl := FastNoiseLite.new()
	nl.seed = seed_i
	nl.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	nl.frequency = 0.85 / maxf(radius, 0.05)
	var out := PackedVector3Array()
	out.resize(v.size())
	for i in v.size():
		var p := v[i]
		var d: float = 1.0 + nl.get_noise_3d(p.x * 2.0, p.y * 2.0, p.z * 2.0) * lumpiness
		out[i] = Vector3(p.x * squash.x, p.y * squash.y, p.z * squash.z) * d
	# recompute normals by area-weighted face accumulation, oriented by measurement
	var nrm := _outward_normals(out, ix)
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = out
	arr[Mesh.ARRAY_NORMAL] = nrm
	arr[Mesh.ARRAY_TEX_UV] = uv
	arr[Mesh.ARRAY_INDEX] = ix
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	return am


func _standing_stone(height: float, width: float, depth: float, seed_i: int) -> ArrayMesh:
	"""A menhir: a tapered prism in 7 horizontal slices, each slice jittered and rotated a
	little, with a closed top and bottom. CLOSED matters -- the character's hull outline
	only works on a mesh with an inside, and if a future session puts the hull pass back on
	props it must not meet the T9 open-skirt defect again."""
	var slices := 7
	var nl := FastNoiseLite.new()
	nl.seed = seed_i
	nl.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	nl.frequency = 0.7
	var verts := PackedVector3Array()
	var idx := PackedInt32Array()
	var sides := 6
	for s in slices:
		var f := float(s) / float(slices - 1)
		var y := f * height
		var taper: float = lerpf(1.0, 0.62, pow(f, 1.35))
		var twist := (nl.get_noise_2d(float(s) * 3.1, 0.0)) * 0.30
		var lean := Vector2(nl.get_noise_2d(0.0, f * 4.0), nl.get_noise_2d(7.0, f * 4.0)) * height * 0.055
		for a in sides:
			var ang := TAU * float(a) / float(sides) + twist
			var rr: float = 1.0 + nl.get_noise_3d(cos(ang) * 2.0, f * 5.0, sin(ang) * 2.0) * 0.22
			verts.append(Vector3(cos(ang) * width * 0.5 * taper * rr + lean.x, y,
								 sin(ang) * depth * 0.5 * taper * rr + lean.y))
	for s in slices - 1:
		for a in sides:
			var a0 := s * sides + a
			var a1 := s * sides + (a + 1) % sides
			var b0 := a0 + sides
			var b1 := a1 + sides
			# clockwise-front, same correction as the terrain: this was
			# [a0, b0, a1, a1, b0, b1], whose right-hand normal points OUTWARD, i.e. at the
			# viewer, i.e. back-facing. The stones were not missing like the ground was --
			# they were drawing their far shell's INSIDE, which is why they read as flat dark
			# slabs with the light in the wrong places.
			idx.append_array([a0, a1, b0, a1, b1, b0])
	# caps, so the prism is a closed solid
	var top_c := verts.size()
	var ty := 0.0
	var tc := Vector3.ZERO
	for a in sides:
		tc += verts[(slices - 1) * sides + a]
	verts.append(tc / float(sides))
	var bot_c := verts.size()
	var bc := Vector3.ZERO
	for a in sides:
		bc += verts[a]
	verts.append(bc / float(sides))
	for a in sides:
		var t0 := (slices - 1) * sides + a
		var t1 := (slices - 1) * sides + (a + 1) % sides
		idx.append_array([t0, t1, top_c])
		idx.append_array([a, bot_c, (a + 1) % sides])
	var nrm := _outward_normals(verts, idx)
	var uvs := PackedVector2Array()
	uvs.resize(verts.size())
	for i in verts.size():
		uvs[i] = Vector2(verts[i].x, verts[i].z) * 0.5 + Vector2(verts[i].y, 0.0) * 0.5
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = nrm
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var am := ArrayMesh.new()
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	return am


func _birch(height: float, seed_i: int) -> Node3D:
	"""A dead birch: a tapered trunk plus four bare limbs. THIN ON PURPOSE -- the trunk is
	0.13 m at the base, which at the play camera's 100.6 px/m is 13 px, and a limb is 3 px.
	If the ink pass can hold a line on that without dissolving or doubling, it can hold one
	on anything the real world will contain."""
	var root := Node3D.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_i
	var trunk := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = 0.045
	cm.bottom_radius = 0.13
	cm.height = height
	cm.radial_segments = 8
	cm.rings = 1
	trunk.mesh = cm
	trunk.position = Vector3(0, height * 0.5, 0)
	trunk.rotation = Vector3(deg_to_rad(rng.randf_range(-3.5, 3.5)), 0.0,
							 deg_to_rad(rng.randf_range(-3.5, 3.5)))
	root.add_child(trunk)
	for i in 4:
		var limb := MeshInstance3D.new()
		var lm := CylinderMesh.new()
		lm.top_radius = 0.012
		lm.bottom_radius = 0.045
		lm.height = rng.randf_range(0.9, 1.7)
		lm.radial_segments = 6
		lm.rings = 1
		limb.mesh = lm
		var h := height * rng.randf_range(0.52, 0.93)
		var ang := rng.randf_range(0.0, TAU)
		limb.position = Vector3(0, h, 0)
		limb.rotation = Vector3(deg_to_rad(rng.randf_range(38.0, 62.0)), ang, 0.0)
		limb.position += limb.transform.basis.y * lm.height * 0.5
		root.add_child(limb)
	return root


func place_on_ground(n: Node3D, x: float, z: float, sink := 0.0) -> void:
	n.position = Vector3(x, height_at(x, z) - sink, z)


func build_props(parent: Node3D, stone_mat: Material, rock_mat: Material,
		wood_mat: Material) -> Dictionary:
	var out := {"stones": [], "rocks": [], "trees": [], "sizes": {}}
	var props := Node3D.new()
	props.name = "Props"
	parent.add_child(props)
	var rng := RandomNumberGenerator.new()
	rng.seed = 424242

	# THE RING. Nine menhirs about the barrow, ~3.5 m, each unique, each leaning a little.
	var stone_h := []
	for i in RING_STONES:
		var a := TAU * float(i) / float(RING_STONES) + 0.22
		var r: float = RING_RADIUS + rng.randf_range(-0.7, 0.7)
		var x: float = MOUND_CENTRE.x + cos(a) * r
		var z: float = MOUND_CENTRE.y + sin(a) * r
		var h: float = rng.randf_range(3.15, 3.85)
		var mi := MeshInstance3D.new()
		mi.name = "Stone%d" % i
		mi.mesh = _standing_stone(h, rng.randf_range(0.80, 1.10), rng.randf_range(0.42, 0.62),
								  5000 + i * 37)
		mi.material_override = stone_mat
		props.add_child(mi)
		place_on_ground(mi, x, z, 0.18)
		mi.rotation = Vector3(deg_to_rad(rng.randf_range(-6.0, 6.0)), rng.randf_range(0.0, TAU),
							  deg_to_rad(rng.randf_range(-6.0, 6.0)))
		var body := StaticBody3D.new()
		body.collision_layer = TERRAIN_BIT
		body.collision_mask = 0
		var cs := CollisionShape3D.new()
		var bs := BoxShape3D.new()
		bs.size = Vector3(0.95, h, 0.60)
		cs.shape = bs
		cs.position = Vector3(0, h * 0.5, 0)
		body.add_child(cs)
		mi.add_child(body)
		out["stones"].append(mi)
		stone_h.append(snappedf(h, 0.01))

	# THE LINTEL. One slab across two stones at the barrow's mouth, so there is a horizontal
	# top surface high off the ground for the snow layer to catch and for the ink to rim.
	var lint := MeshInstance3D.new()
	lint.name = "Lintel"
	lint.mesh = _standing_stone(2.55, 0.95, 0.55, 8123)
	lint.material_override = stone_mat
	props.add_child(lint)
	place_on_ground(lint, MOUND_CENTRE.x + 2.6, MOUND_CENTRE.y + 6.4, 0.0)
	lint.rotation = Vector3(0.0, deg_to_rad(18.0), deg_to_rad(90.0))
	lint.position += Vector3(0.0, 2.05, 0.0)

	# ROCKS, 1 to 2 m, scattered, half sunk so they read as bedrock rather than as marbles.
	var rock_d := []
	for i in 16:
		var a := rng.randf_range(0.0, TAU)
		var r: float = rng.randf_range(4.5, 30.0)
		var x: float = MOUND_CENTRE.x + cos(a) * r
		var z: float = MOUND_CENTRE.y + sin(a) * r
		var rad: float = rng.randf_range(0.50, 1.02)
		var mi := MeshInstance3D.new()
		mi.name = "Rock%d" % i
		mi.mesh = _displaced_sphere(rad, Vector3(1.0, rng.randf_range(0.58, 0.86), 1.0),
									rng.randf_range(0.18, 0.34), 3100 + i * 53)
		mi.material_override = rock_mat
		props.add_child(mi)
		place_on_ground(mi, x, z, rad * rng.randf_range(0.30, 0.55))
		mi.rotation = Vector3(0.0, rng.randf_range(0.0, TAU), 0.0)
		var ab := mi.mesh.get_aabb()
		out["rocks"].append(mi)
		rock_d.append(snappedf(ab.size.y, 0.01))
		if rad > 0.80:
			var body := StaticBody3D.new()
			body.collision_layer = TERRAIN_BIT
			body.collision_mask = 0
			var cs := CollisionShape3D.new()
			var sp := SphereShape3D.new()
			sp.radius = rad * 0.85
			cs.shape = sp
			cs.position = Vector3(0, rad * 0.4, 0)
			body.add_child(cs)
			mi.add_child(body)

	# BARE BIRCHES — the thin-geometry test for the ink pass.
	var tree_h := []
	for i in 5:
		var a := rng.randf_range(0.0, TAU)
		var r: float = rng.randf_range(13.0, 26.0)
		var h: float = rng.randf_range(4.2, 6.4)
		var t := _birch(h, 600 + i * 17)
		t.name = "Birch%d" % i
		for m in t.find_children("*", "MeshInstance3D", true, false):
			(m as MeshInstance3D).material_override = wood_mat
		props.add_child(t)
		place_on_ground(t, MOUND_CENTRE.x + cos(a) * r, MOUND_CENTRE.y + sin(a) * r, 0.0)
		out["trees"].append(t)
		tree_h.append(snappedf(h, 0.01))

	out["sizes"] = {
		"standing_stone_h_m": stone_h,
		"rock_h_m": rock_d,
		"birch_h_m": tree_h,
		"_note": "true metres; the brief asks stones ~3.5 m and rocks 1-2 m",
	}
	report["props"] = out["sizes"]
	return out
