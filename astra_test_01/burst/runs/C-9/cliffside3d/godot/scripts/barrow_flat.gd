extends RefCounted
class_name BarrowFlat
## C-9 R-C9-74: THE WALKABLE GROUND IS ONE FLAT LEVEL. Matt, on the 15:20 build:
##
##   "The hills are probably not great for gameplay as they may confuse combat. I would stay
##    away from non-flat ground other than the occasional stairway/etc."
##
## So the floor is y = 0 and nothing about it varies. Same interface as BarrowStandIn and
## BarrowHeightfield -- height_at / normal_at / build_terrain / place_on_ground, the same
## TERRAIN_BIT, the same EXTENT -- so it is the same one-line swap, and the two heightfields
## stay selectable for comparison at no cost.
##
## WHAT MOVES TO THE STRUCTURE SIDE. The authored heightfield carried four things, and three
## of them are relief the player walked on:
##
##   the MOUND (1.70 m dome at scene (0, -4))  -> barrow_world._build_mound: a mesh with a
##       cut entrance passage and a vertical-sided collider. Non-walkable, door at floor level.
##   the OUTCROPS (0.55 m rises)               -> the rock props already in the scene list,
##       now with collision. Obstacles, not terrain.
##   the TARN (1.15 m hollow)                  -> flat, at floor level, wearing the splat's
##       own ice class. A frozen tarn IS flat; the hollow was the only part the player felt.
##   the 0.055 m/m CAMERA-WARD SLOPE           -> gone. It is the part that makes a top-down
##       fight read wrong, and it is worth nothing to look at.
##
## THE GRID IS COARSE AND THAT IS NOT A SHORTCUT. Nothing in the render stack reads a
## terrain vertex: the ramp, the snow layer and the tile blend all work off world position
## and world normal in the fragment shader, and the tile UV is world metres. A flat plane
## needs vertices only for the shadow map's depth range and for the snow measurement's area
## weighting, so 2 m quads (4,232 triangles against the heightfield's 55,778) render the
## identical picture -- checked by rendering both, not assumed.

const TERRAIN_BIT := 1 << 1        # knight.gd masks its ground ray and its body to this
const EXTENT := 46.0               # half-size, metres -- matches the other two grounds
const CELL := 2.0                  # metres per quad; nothing samples between them
const MOUND_CENTRE := Vector2(0.0, -4.0)
const FLOOR_Y := 0.0

var report := {}


func height_at(_x: float, _z: float) -> float:
	return FLOOR_Y


func normal_at(_x: float, _z: float, _eps := 0.28) -> Vector3:
	return Vector3.UP


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
			verts[k] = Vector3(x, FLOOR_Y, z)
			norms[k] = Vector3.UP
			uvs[k] = Vector2(x, z) * 0.25
	for j in n:
		for i in n:
			var k := j * (n + 1) + i
			# THE WINDING IS THE HEIGHTFIELD'S, COPIED DELIBERATELY. Godot's front faces are
			# CLOCKWISE seen from the front, so the order that gives a +Y right-hand normal is
			# BACK-facing and the ground is INVISIBLE under the default cull -- not dim, not
			# wrong-side-lit, gone. That was caught by rendering both orders and counting
			# pixels (0 of 25,600 against 70.9%), not by reading face normals, which reported
			# the broken one as correct.
			idx.append_array([k, k + n + 2, k + n + 1, k, k + 1, k + n + 2])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = norms
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.name = "BarrowGround"
	mi.mesh = mesh
	mi.material_override = mat
	parent.add_child(mi)
	var body := StaticBody3D.new()
	body.collision_layer = TERRAIN_BIT
	body.collision_mask = 0
	var shape := CollisionShape3D.new()
	# A BOX, NOT THE MESH. The floor is a plane; a trimesh of 4,232 triangles to describe one
	# is work the broadphase does every frame for a shape that has one answer. The box sits
	# with its top face exactly at FLOOR_Y, so is_on_floor() lands where height_at says.
	var bs := BoxShape3D.new()
	bs.size = Vector3(EXTENT * 2.0, 2.0, EXTENT * 2.0)
	shape.shape = bs
	shape.position = Vector3(0.0, FLOOR_Y - 1.0, 0.0)
	body.add_child(shape)
	mi.add_child(body)
	report = {"kind": "flat", "floor_y": FLOOR_Y, "extent_m": EXTENT * 2.0, "cell_m": CELL,
			  "terrain_tris": n * n * 2,
			  "collider": "box, top face at floor_y",
			  "_why": "R-C9-74: one flat walkable level; elevation only from architected steps"}
	return mi


func place_on_ground(node: Node3D, x: float, z: float, sink := 0.0) -> void:
	node.global_position = Vector3(x, FLOOR_Y - sink, z)
