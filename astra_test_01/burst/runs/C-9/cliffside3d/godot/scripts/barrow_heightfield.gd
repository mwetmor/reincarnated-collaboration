extends RefCounted
class_name BarrowHeightfield
## C-9 T10: the barrow ground from a MEASURED heightfield, as a drop-in for BarrowStandIn.
##
## Same interface, deliberately: height_at / normal_at / build_terrain / place_on_ground,
## the same TERRAIN_BIT, the same EXTENT and CELL. Swapping one line in barrow_world.gd
##
##     world = BarrowStandIn.new()
##     world = BarrowHeightfield.new("res://data/height_a_marigold.png", ".json")
##
## puts a real surface under the same scene, so the comparison at the play camera is of the
## GROUND and not of two different scenes. Nothing here touches a shader or a material.
##
## TWO HEIGHTFIELDS SHIP, and they are two hypotheses rather than a draft and a final:
##
##   height_a_marigold.*  DERIVED from the concept by monocular depth. It has the painting's
##                        own lumps in it, and it carries a 1.71x calibration spread, because
##                        the absolute depth scale is the one thing an orthographic painting
##                        does not contain. Relief 4.00 m, median slope 18.8 deg, 1.73% of
##                        cells over 70 deg.
##   height_a_authored.*  AUTHORED from the half of the evidence that IS solid -- the plan,
##                        which is ruler work through the barbarian's 1.85 m -- plus four
##                        stated constraints: tarn flat and 1.15 m low, mound a 1.70 m dome,
##                        ground sloping 0.055 m/m away from the camera, outcrops up 0.55 m.
##                        Relief 2.37 m, median slope 3.1 deg, NOTHING over 70 deg.
##
## Look at both. The derived one is the painting's claim; the authored one is what the
## painting's plan supports without a depth model's word for the scale.
##
## THE PNG IS 16-BIT AND IS LOADED OFF A REAL PATH. Godot's importer would turn it into a
## compressed 8-bit texture, which quantises the relief into 256 steps and still looks like
## a terrain. Image.load() reads the file, not the import.

const TERRAIN_BIT := 1 << 1        # knight.gd masks its ground ray to this
const EXTENT := 46.0               # half-size, metres -- matches BarrowStandIn
const CELL := 0.55                 # metres per quad -- matches BarrowStandIn
const MOUND_CENTRE := Vector2(0.0, -4.0)   # where the barrow sits in the scene's frame

var report := {}
var _h := PackedFloat32Array()
var _w := 0
var _hgt := 0
var _grid := 0.05
var _lo := 0.0
var _span := 1.0
var _off := Vector2.ZERO           # world (x,z) of the heightfield's cell (0,0)
var _edge := 0.0                   # the level the surface relaxes to outside the data
var _ok := false


func _init(png := "res://data/height_a_authored.png",
		   meta := "res://data/height_a_authored.json") -> void:
	var m = JSON.parse_string(FileAccess.get_file_as_string(meta))
	if typeof(m) != TYPE_DICTIONARY:
		push_error("[barrowhf] cannot read %s" % meta)
		return
	_grid = float(m["png"]["metres_per_pixel"])
	_lo = float(m["png"]["height_min_m"])
	_span = float(m["png"]["height_max_m"]) - _lo
	var img := Image.new()
	if img.load(png) != OK:
		push_error("[barrowhf] cannot load %s" % png)
		return
	_w = img.get_width()
	_hgt = img.get_height()
	_h.resize(_w * _hgt)
	for y in _hgt:
		for x in _w:
			_h[y * _w + x] = _lo + img.get_pixel(x, y).r * _span

	# Anchor the data so the BARROW lands where the scene expects it. The mound's centre is
	# measured in 22_authored_heightfield.py; without it the footprint would sit whereever
	# the unprojection's min corner happened to fall, which is not a place.
	var mc := Vector2(float(_w) * _grid * 0.5, float(_hgt) * _grid * 0.5)
	if m.has("mound") and m["mound"].has("centre_xz"):
		mc = Vector2(float(m["mound"]["centre_xz"][0]), float(m["mound"]["centre_xz"][1]))
	_off = MOUND_CENTRE - mc

	# Outside the data the world still has to exist: 15 m of concept inside a 92 m scene.
	# The surface relaxes to the median height of the data's RIM rather than to zero, so
	# the join does not step.
	var rim := 0.0
	var n := 0
	for x in _w:
		rim += _h[x] + _h[(_hgt - 1) * _w + x]
		n += 2
	for y in _hgt:
		rim += _h[y * _w] + _h[y * _w + _w - 1]
		n += 2
	_edge = rim / maxf(float(n), 1.0)
	_ok = true
	report = {"source": png, "cells": [_w, _hgt], "grid_m": _grid,
			  "extent_m": [snappedf(_w * _grid, 0.01), snappedf(_hgt * _grid, 0.01)],
			  "relief_m": snappedf(_span, 0.001),
			  "origin_xz": [snappedf(_off.x, 0.01), snappedf(_off.y, 0.01)],
			  "edge_level_m": snappedf(_edge, 0.01)}
	print("[barrowhf] %s" % JSON.stringify(report))


func height_at(x: float, z: float) -> float:
	"""THE surface. Metres. Bilinear inside the data, relaxing outside it."""
	if not _ok:
		return 0.0
	var fx := (x - _off.x) / _grid
	var fz := (z - _off.y) / _grid
	# how far outside the data we are, in metres, for the relax blend
	var ox: float = maxf(maxf(-fx, fx - float(_w - 1)), 0.0) * _grid
	var oz: float = maxf(maxf(-fz, fz - float(_hgt - 1)), 0.0) * _grid
	var out := sqrt(ox * ox + oz * oz)
	var cx: int = clampi(int(floor(fx)), 0, _w - 2)
	var cz: int = clampi(int(floor(fz)), 0, _hgt - 2)
	var tx: float = clampf(fx - float(cx), 0.0, 1.0)
	var tz: float = clampf(fz - float(cz), 0.0, 1.0)
	var h00 := _h[cz * _w + cx]
	var h10 := _h[cz * _w + cx + 1]
	var h01 := _h[(cz + 1) * _w + cx]
	var h11 := _h[(cz + 1) * _w + cx + 1]
	var h: float = lerpf(lerpf(h00, h10, tx), lerpf(h01, h11, tx), tz)
	if out > 0.0:
		var t: float = clampf(out / 12.0, 0.0, 1.0)
		h = lerpf(h, _edge, t * t * (3.0 - 2.0 * t))
	return h


func normal_at(x: float, z: float, eps := 0.28) -> Vector3:
	var hx := height_at(x + eps, z) - height_at(x - eps, z)
	var hz := height_at(x, z + eps) - height_at(x, z - eps)
	return Vector3(-hx, 2.0 * eps, -hz).normalized()


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
			var k := j * (n + 1) + i
			idx.append_array([k, k + n + 1, k + n + 2, k, k + n + 2, k + 1])
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
	shape.shape = mesh.create_trimesh_shape()
	body.add_child(shape)
	mi.add_child(body)
	report["terrain_tris"] = n * n * 2
	return mi


func place_on_ground(node: Node3D, x: float, z: float, sink := 0.0) -> void:
	node.global_position = Vector3(x, height_at(x, z) - sink, z)
