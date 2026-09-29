extends Node3D
## C-9 T10: the Frost King's Barrow ground, built from the heightfield at TRUE SCALE.
##
## The heightfield ships as a 16-bit PNG plus a JSON that says what its levels mean, and
## the mesh is built here rather than exported as geometry. A 300x300 grid is 178,802
## triangles; as an .obj that is about 10 MB of text to carry a picture that is 180 kB,
## and it would have to be re-exported every time the terrain is re-derived. The PNG is
## the artifact; this is the reader.
##
## THE PNG IS 16-BIT AND MUST NOT BE IMPORTED AS A TEXTURE. Godot's importer will happily
## turn it into a compressed 8-bit VRAM texture, which quantises 4.00 m of relief into 256
## steps of 1.6 cm and looks fine. It is loaded with Image.load_from_file off a real path
## for that reason -- the same trap the cliffside's v4_zones.png fell into, from the other
## side.
##
##   var t = preload("res://scripts/barrow_terrain.gd").new()
##   t.height_png = "res://data/height_a_marigold.png"
##   t.meta_json  = "res://data/height_a_marigold.json"
##   add_child(t)

@export var height_png := "res://data/height_a_marigold.png"
@export var meta_json := "res://data/height_a_marigold.json"
@export var splat_png := "res://data/splat_ids_a_marigold.png"
@export var build_collision := true

var grid_m := 0.05
var height_min := 0.0
var height_max := 1.0
var size_cells := Vector2i.ZERO
var report := {}


func _ready() -> void:
	var meta = JSON.parse_string(FileAccess.get_file_as_string(meta_json))
	if typeof(meta) != TYPE_DICTIONARY:
		push_error("[barrow] cannot read %s" % meta_json)
		return
	grid_m = float(meta["png"]["metres_per_pixel"])
	height_min = float(meta["png"]["height_min_m"])
	height_max = float(meta["png"]["height_max_m"])

	var img := Image.new()
	if img.load(height_png) != OK:
		push_error("[barrow] cannot load %s" % height_png)
		return
	var w := img.get_width()
	var h := img.get_height()
	size_cells = Vector2i(w, h)
	var span := height_max - height_min

	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	# Heights are read once into a flat array: get_pixel per vertex, three times per
	# triangle, is the same read six times over on a 90,000-vertex grid.
	var hs := PackedFloat32Array()
	hs.resize(w * h)
	for y in h:
		for x in w:
			hs[y * w + x] = height_min + img.get_pixel(x, y).r * span
	for y in h - 1:
		for x in w - 1:
			var p00 := Vector3(x * grid_m, hs[y * w + x], y * grid_m)
			var p10 := Vector3((x + 1) * grid_m, hs[y * w + x + 1], y * grid_m)
			var p01 := Vector3(x * grid_m, hs[(y + 1) * w + x], (y + 1) * grid_m)
			var p11 := Vector3((x + 1) * grid_m, hs[(y + 1) * w + x + 1], (y + 1) * grid_m)
			var uv00 := Vector2(float(x) / w, float(y) / h)
			var uv10 := Vector2(float(x + 1) / w, float(y) / h)
			var uv01 := Vector2(float(x) / w, float(y + 1) / h)
			var uv11 := Vector2(float(x + 1) / w, float(y + 1) / h)
			st.set_uv(uv00); st.add_vertex(p00)
			st.set_uv(uv01); st.add_vertex(p01)
			st.set_uv(uv11); st.add_vertex(p11)
			st.set_uv(uv00); st.add_vertex(p00)
			st.set_uv(uv11); st.add_vertex(p11)
			st.set_uv(uv10); st.add_vertex(p10)
	st.generate_normals()
	st.generate_tangents()
	var mi := MeshInstance3D.new()
	mi.name = "BarrowGround"
	mi.mesh = st.commit()
	add_child(mi)

	if build_collision:
		var body := StaticBody3D.new()
		var shape := CollisionShape3D.new()
		shape.shape = mi.mesh.create_trimesh_shape()
		body.add_child(shape)
		mi.add_child(body)

	report = {"cells": [w, h], "grid_m": grid_m,
			  "extent_m": [snappedf(w * grid_m, 0.01), snappedf(h * grid_m, 0.01)],
			  "relief_m": snappedf(span, 0.001),
			  "triangles": (w - 1) * (h - 1) * 2}
	print("[barrow] ground %s" % JSON.stringify(report))
