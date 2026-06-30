@tool
class_name SidekickCharacter extends Node3D

var sk_root = ProjectSettings.get_setting(SidekickCreatorPlugin.setting_sidekick_root, SidekickCreatorPlugin.setting_sidekick_root_default)
var sk_base_model = sk_root.path_join("Resources/Meshes/SK_BaseModel.fbx")
var sk_color_map = sk_root.path_join("Resources/Textures/T_ColorMap.png")
var sk_db = sk_root.path_join("Database/Proto_Side_Kick_Data")

var db: SQLite

#@export_tool_button("Randomize", "Callable") var _rand = randomize
#@export_tool_button("Clear", "Callable") var _clear = clear

enum Species {
	Human = 1,
	Goblin
}

enum PartGroup {
	Head = 1,
	UpperBody,
	LowerBody,
}

enum Part {
	Head = 1,
	Hair,
	EyebrowLeft,
	EyebrowRight,
	EyeLeft,
	EyeRight,
	EarLeft,
	EarRight,
	FacialHair,
	Torso,
	ArmUpperLeft,
	ArmUpperRight,
	ArmLowerLeft,
	ArmLowerRight,
	HandLeft,
	HandRight,
	Hips,
	LegLeft,
	LegRight,
	FootLeft,
	FootRight,
	AttachmentHead,
	AttachmentFace,
	AttachmentBack,
	AttachmentHipsFront,
	AttachmentHipsBack,
	AttachmentHipsLeft,
	AttachmentHipsRight,
	AttachmentShoulderLeft,
	AttachmentShoulderRight,
	AttachmentElbowLeft,
	AttachmentElbowRight,
	AttachmentKneeLeft,
	AttachmentKneeRight,
	Nose,
	Teeth,
	Tongue,
}

enum ColorGroup {
	Species = 1,
	Outfits,
	Attachments,
	Materials,
	Elements
}

enum ColorType {
	MainColor,
	Metallic,
	Smoothness,
	Reflection,
	Emission,
	Opacity
}

enum BlendShape {
	Feminine,
	Heavy,
	Skinny,
	Bulk
}

var part_groups: Dictionary[PartGroup, Array] = {
	PartGroup.Head: [
		Part.Head,
		Part.Hair,
		Part.EyebrowLeft,
		Part.EyebrowRight,
		Part.EyeLeft,
		Part.EyeRight,
		Part.EarLeft,
		Part.EarRight,
		Part.FacialHair,
		Part.AttachmentHead,
		Part.AttachmentFace,
		Part.Nose,
		Part.Teeth,
		Part.Tongue,
	],
	PartGroup.UpperBody: [
		Part.Torso,
		Part.ArmUpperLeft,
		Part.ArmUpperRight,
		Part.ArmLowerLeft,
		Part.ArmLowerRight,
		Part.HandLeft,
		Part.HandRight,
		Part.AttachmentBack,
		Part.AttachmentShoulderLeft,
		Part.AttachmentShoulderRight,
		Part.AttachmentElbowLeft,
		Part.AttachmentElbowRight,
	],
	PartGroup.LowerBody: [
		Part.Hips,
		Part.LegLeft,
		Part.LegRight,
		Part.FootLeft,
		Part.FootRight,
		Part.AttachmentHipsFront,
		Part.AttachmentHipsBack,
		Part.AttachmentHipsLeft,
		Part.AttachmentHipsRight,
		Part.AttachmentKneeLeft,
		Part.AttachmentKneeRight,
	]
}

var part_bones: Dictionary[Part, String] = {
	Part.AttachmentBack: "backAttach",
	Part.AttachmentHipsFront: "hipAttachFront",
	Part.AttachmentHipsBack: "hipAttachBack",
	Part.AttachmentHipsLeft: "hipAttach_l",
	Part.AttachmentHipsRight: "hipAttach_r",
	Part.AttachmentShoulderLeft: "shoulderAttach_l",
	Part.AttachmentShoulderRight: "shoulderAttach_r",
	Part.AttachmentElbowLeft: "elbowAttach_l",
	Part.AttachmentElbowRight: "elbowAttach_r",
	Part.AttachmentKneeLeft: "kneeAttach_l",
	Part.AttachmentKneeRight: "kneeAttach_r"
}

@export_group("Combiner", "combiner_")
#@export
var combiner_merge: bool
## Bake blends and disable runtime blending. Disabling this option will make meshes local to scene. See Godot issue #10402
#@export var combiner_bake_blend: bool = true

@export var filter_id: int:
	set(value):
		if filter_id == value:
			return
		filter_id = value
		_properties = []
		notify_property_list_changed()

@export var species: Species = Species.Human:
	set(value):
		if species == value:
			return
		species = value
		_properties = []
		notify_property_list_changed()

@export var parts: Dictionary[Part, String]
@export var colors: Dictionary[int, Color]
@export var part_presets: Dictionary[int, String]
@export var color_presets: Dictionary[int, String]

var body_shape_preset: String = "None":
	set(value):
		body_shape_preset = value
		queue_combine()

var color_properties: Array

var queued: bool
var _properties: Array

func _ready() -> void:
	if db == null:
		init()

func init():
	db = SQLite.new()
	db.default_extension = ""
	db.path = sk_db
	db.open_db()

	db.query("select * from sk_color_property")
	color_properties = db.query_result

func queue_combine():
	if not queued and is_inside_tree():
		queued = true
		combine.call_deferred()

func combine():
	queued = false

	var material := get_material()
	var blends := get_blend_shapes()

	var skel: Skeleton3D = find_child("*Skeleton*")
	if skel == null:
		skel = load(sk_base_model).instantiate().find_child("*Skeleton*")
		skel.owner = null
		skel.scene_file_path = ""
		skel.reparent(self, false)
		if Engine.is_editor_hint():
			skel.owner = EditorInterface.get_edited_scene_root()
	else:
		skel.reset_bone_poses()
		var from_skel: Skeleton3D = load(sk_base_model).instantiate().find_child("*Skeleton*")
		for idx in range(from_skel.get_bone_count()):
			skel.set_bone_pose(idx, from_skel.get_bone_pose(idx))
			skel.set_bone_rest(idx, from_skel.get_bone_rest(idx))

	for child in skel.get_children():
		if child is MeshInstance3D and child.name.begins_with("SK_"):
			skel.remove_child(child)

	var parts = self.parts.duplicate()
	for group in part_presets:
		var preset = part_presets[group]
		if preset == "None":
			continue
		load_part_preset(group, preset, parts)

	var mis: Array[MeshInstance3D]

	for part in parts:
		var name = parts[part]
		if name == "None":
			continue

		db.query("select * from sk_part where name = '%s'" % name)
		if db.query_result.size() < 1:
			push_error("missing part %s" % name)
			continue

		var res := load("res://%s" % db.query_result[0]["part_location"])
		if res == null:
			push_error("missing file %s" % name)
			continue

		var node: Node3D = res.instantiate()

		var from_skel: Skeleton3D = node.find_child("*Skeleton*")
		var mi: MeshInstance3D = from_skel.get_child(0)
		mis.append(mi)

		for i in range(mi.skin.get_bind_count()):
			var bone_name := mi.skin.get_bind_name(i)
			if skel.find_bone(bone_name) != -1:
				continue

			var from_bone := from_skel.find_bone(bone_name)
			var to_bone := skel.add_bone(bone_name)

			var parent_name = from_skel.get_bone_name(from_skel.get_bone_parent(from_bone))
			var parent_idx = skel.find_bone(parent_name)
			if parent_idx == -1:
				push_warning("missing parent bone %s" % parent_name)
			skel.set_bone_parent(to_bone, parent_idx)

			skel.set_bone_rest(to_bone, from_skel.get_bone_rest(from_bone))
			skel.set_bone_pose(to_bone, from_skel.get_bone_pose(from_bone))

		for idx in range(mi.get_blend_shape_count()):
			var blend_shape_name: String = mi.mesh.get_blend_shape_name(idx)
			var arr = blend_shape_name.split(".")
			if arr.size() > 1:
				mi.mesh.set_blend_shape_name(idx, arr[1])

		apply_blend_shapes(skel, mi, blends)

		## duplicating meshes breaks blend shape
		## https://github.com/godotengine/godot/issues/10402
		#if combiner_bake_blend:
			#mi.mesh = mi.bake_mesh_from_current_blend_shape_mix()
		#else:
			#from_mi.mesh.resource_local_to_scene = true

	apply_blend_rig_movement(skel, blends)

	for mi in mis:
		for surface in range(mi.mesh.get_surface_count()):
			mi.set_surface_override_material(surface, material)
		mi.owner = null
		mi.reparent(skel, false)
		if Engine.is_editor_hint():
			mi.owner = EditorInterface.get_edited_scene_root()

#for mesh in meshes:
	#for i in range(mesh.get_blend_shape_count()):
		#var bs_name: String = mesh.get_blend_shape_name(i)
		#var exists: bool
		#for j in range(merged_mesh.get_blend_shape_count()):
			#if merged_mesh.get_blend_shape_name(i) == bs_name:
				#print("exists")
				#exists = true
				#break
		#if not exists:
			#merged_mesh.add_blend_shape(bs_name)

	if combiner_merge:
		var mi := MeshInstance3D.new()
		var mm := ArrayMesh.new()
		mi.mesh = mm
		for mesh: MeshInstance3D in skel.get_children():
			for surface in range(mesh.mesh.get_surface_count()):
				mm.add_surface_from_arrays(
					Mesh.PRIMITIVE_TRIANGLES,
					mesh.mesh.surface_get_arrays(surface),
					#mesh.surface_get_blend_shape_arrays(surface)
				)

				mm.surface_set_material(mm.get_surface_count() - 1, material)

			skel.remove_child(mesh)

		skel.add_child(mi)
		if Engine.is_editor_hint():
			mi.owner = EditorInterface.get_edited_scene_root()

func get_blend_shapes() -> Dictionary[BlendShape, float]:
	var blends: Dictionary[BlendShape, float] = {
		BlendShape.Heavy: 0.0,
		BlendShape.Skinny: 0.0,
		BlendShape.Feminine: 0.0,
		BlendShape.Bulk: 0.0,
	}

	if body_shape_preset == "None":
		return blends

	db.query("select * from sk_body_shape_preset where name = '%s'" % body_shape_preset)
	if db.query_result.size() < 1:
		push_warning("reset missing body shape preset %s" % body_shape_preset)
		body_shape_preset = "None"
		return blends
	var preset = db.query_result[0]

	var body_size = int(preset["body_size"]) / 100.0
	blends[BlendShape.Heavy] = body_size if body_size > 0 else 0
	blends[BlendShape.Skinny] = -body_size if body_size < 0 else 0
	blends[BlendShape.Feminine] = remap(int(preset["body_type"]), -100, 100, 0, 1.0)
	blends[BlendShape.Bulk] = remap(int(preset["musculature"]), -100, 100, 0, 1.0)

	return blends

func apply_blend_shapes(sk: Skeleton3D, mi: MeshInstance3D, blends: Dictionary[BlendShape, float]):
	mi.set("blend_shapes/defaultHeavy", blends[BlendShape.Heavy])
	mi.set("blend_shapes/defaultSkinny", blends[BlendShape.Skinny])
	mi.set("blend_shapes/masculineFeminine", blends[BlendShape.Feminine])
	mi.set("blend_shapes/defaultBuff", blends[BlendShape.Bulk])

func apply_blend_rig_movement(sk: Skeleton3D, blends: Dictionary[BlendShape, float]):
	var offsets: Dictionary[int, Vector3]
	var rotations: Dictionary[int, Vector3]

	db.query("select * from sk_blend_shape_rig_movement")
	for movement in db.query_result:
		var idx := sk.find_bone(part_bones[movement["part_type"]])
		var offset = Vector3(movement["max_offset_x"], movement["max_offset_y"], movement["max_offset_z"])
		var rotation = deg_to_rad(1.0) * Vector3(movement["max_rotation_x"], movement["max_rotation_y"], movement["max_rotation_z"])

		var blend = blends[movement["blend_type"]]
		rotation *= blend
		offset *= blend

		offsets.get_or_add(idx, Vector3.ZERO)
		offsets[idx] += offset

		rotations.get_or_add(idx, Vector3.ZERO)
		rotations[idx] += rotation

	# TODO this isn't entirely right (or we're just missing rotation)
	for idx in offsets:
		if offsets[idx].is_zero_approx():
			continue

		var rest := sk.get_bone_rest(idx)
		var parent_origin := sk.get_bone_global_rest(sk.get_bone_parent(idx)).origin
		var bone_dir := parent_origin.direction_to(sk.get_bone_global_rest(idx).origin)

		var axis := offsets[idx].normalized()

		var rotation := Basis().rotated(axis.cross(bone_dir).normalized(), axis.angle_to(bone_dir))
		rest.origin += rotation * offsets[idx]

		sk.set_bone_rest(idx, rest)

	# TODO this is completely wrong
	#for idx in rotations:
		#var rest := sk.get_bone_rest(idx)
		#var parent_origin := sk.get_bone_global_rest(sk.get_bone_parent(idx)).origin
		#var bone_dir := parent_origin.direction_to(sk.get_bone_global_rest(idx).origin)
#
		#var rotation = rotations[idx]
		#if rotation != Vector3.ZERO:
			#rest.basis = Basis(rotation.normalized(), rotation.length())
			##rest.basis = rest.basis.rotated(rotation.normalized(), rotation.length())
		#sk.set_bone_rest(idx, rest)

	sk.reset_bone_poses()

func clear():
	for name in Part.keys():
		set(name, "None")

func randomize():
	for name in Part.keys():
		var id = Part[name]
		var all_parts = query_parts(id)
		while all_parts.size() > 0:
			var part = all_parts[randi_range(0, all_parts.size() - 1)]
			if FileAccess.file_exists("res://%s" % part["part_location"]):
				parts[id] = part["name"]
				break
	combine()

func _get_property_list():
	if db == null:
		init()

	if not _properties.is_empty():
		return _properties

	db.query("select * from sk_part_filter")
	var hint = "All,"
	for part_filter in db.query_result:
		hint += "%s," % part_filter["filter_term"]
	_properties.append({
		"name": "filter",
		"type": TYPE_STRING,
		"hint": PROPERTY_HINT_ENUM,
		"hint_string": hint,
	})

	_properties.append({
		"name": "Presets",
		"type": TYPE_NIL,
		"usage": PROPERTY_USAGE_GROUP,
	})

	db.query("select * from sk_body_shape_preset")
	hint = "None"
	for part_filter in db.query_result:
		hint += ",%s" % part_filter["name"]
	_properties.append({
		"name": "body_shape_preset",
		"type": TYPE_STRING,
		"hint": PROPERTY_HINT_ENUM,
		"hint_string": hint,
	})

	_properties.append({
		"name": "Parts",
		"type": TYPE_NIL,
		"usage": PROPERTY_USAGE_SUBGROUP,
		"hint_string": "part_preset_",
	})
	for group in PartGroup.values():
		db.query("select * from sk_part_preset where part_group = %d" % group)
		hint = "None"
		for part_filter in db.query_result:
			hint += ",%s" % part_filter["name"]
		_properties.append({
			"name": "part_preset_%s" % PartGroup.find_key(group),
			"type": TYPE_STRING,
			"hint": PROPERTY_HINT_ENUM,
			"hint_string": hint,
		})

	_properties.append({
		"name": "Colors",
		"type": TYPE_NIL,
		"usage": PROPERTY_USAGE_SUBGROUP,
		"hint_string": "color_preset_",
	})
	for group in ColorGroup.values():
		db.query("select * from sk_color_preset where color_group = %d and ptr_species = %d" % [group, species])
		hint = "None,"
		for preset in db.query_result:
			hint += "%s," % preset["name"]
		_properties.append({
			"name": color_preset_to_prop(group),
			"type": TYPE_STRING,
			"hint": PROPERTY_HINT_ENUM,
			"hint_string": hint,
		})

	_properties.append({
		"name": "Parts",
		"type": TYPE_NIL,
		"usage": PROPERTY_USAGE_GROUP,
	})
	for group in PartGroup.keys():
		_properties.append({
			"name": group,
			"type": TYPE_NIL,
			"usage": PROPERTY_USAGE_SUBGROUP,
			"hint_string": "part_",
		})
		for id in part_groups[PartGroup[group]]:
			hint = "None"
			for part in query_parts(id):
				if not FileAccess.file_exists("res://%s" % part["part_location"]):
					continue
				hint += ",%s" % part["name"]

			_properties.append({
				"name": part_to_prop(id),
				"type": TYPE_STRING,
				"hint": PROPERTY_HINT_ENUM,
				"hint_string": hint,
			})


	_properties.append({
		"name": "Colors",
		"type": TYPE_NIL,
		"usage": PROPERTY_USAGE_GROUP,
		"hint_string": "color_",
	})
	for group in ColorGroup.values():
		_properties.append({
			"name": ColorGroup.find_key(group),
			"type": TYPE_NIL,
			"usage": PROPERTY_USAGE_SUBGROUP,
			"hint_string": "color_",
		})
		for color_prop in color_properties.filter(func(p): return p["color_group"] == group):
			_properties.append({
				"name": color_to_prop(color_prop["id"]),
				"type": TYPE_COLOR,
			})

	return _properties

func _property_can_revert(property: StringName) -> bool:
	if property.begins_with("part_"):
		return true
	elif property.begins_with("color_"):
		return true
	elif property == "body_shape_preset":
		return true

	return false

func _property_get_revert(property: StringName) -> Variant:
	if property.begins_with("part_"):
		return "None"
	elif property.begins_with("color_preset_"):
		return "None"
	elif property.begins_with("color_"):
		return Color.TRANSPARENT
	elif property == "body_shape_preset":
		return "None"

	return null

func _set(name: StringName, value: Variant) -> bool:
	var part_group = part_preset_from_prop(name)
	if part_group != null:
		if value == null:
			value = "None"
		part_presets[part_group] = value
		queue_combine()
		return true

	var part = part_from_prop(name)
	if part != null:
		if value == null:
			value = "None"
		parts[part] = value
		queue_combine()
		return true

	if name == "filter" and db != null:
		if value == "All":
			filter_id = 0
			return true
		db.query("select id from sk_part_filter where filter_term = '%s'" % value)
		filter_id = db.query_result[0]["id"]
		return true

	var color = color_from_prop(name)
	if color != null:
		colors[color] = value
		queue_combine()
		return true

	var color_group = color_preset_from_prop(name)
	if color_group != null:
		color_presets[color_group] = value
		queue_combine()
		return true

	return false

func _get(name: StringName) -> Variant:
	var part_group = part_preset_from_prop(name)
	if part_group != null:
		if part_presets.has(part_group):
			return part_presets[part_group]
		return "None"

	var part = part_from_prop(name)
	if part != null:
		if parts.has(part):
			return parts[part]
		return "None"

	if name == "filter":
		db.query("select filter_term from sk_part_filter where id = %d" % filter_id)
		if db.query_result.size() < 1:
			return "All"
		return db.query_result[0]["filter_term"]

	var color = color_from_prop(name)
	if color != null:
		if colors.has(color):
			return colors[color]
		return Color.TRANSPARENT

	var color_group = color_preset_from_prop(name)
	if color_group != null:
		if color_presets.has(color_group):
			return color_presets[color_group]
		return "None"

	return null

func _validate_property(property: Dictionary):
	if property.name in ["parts", "filter_id", "colors", "color_presets", "part_presets"]:
		property.usage = PROPERTY_USAGE_NO_EDITOR

func query_parts(type: Part):
	var query = "select * from sk_part where type = %d and ptr_species = %d" % [type, species]
	if filter_id > 0:
		query = "select * from sk_part p inner join sk_part_filter_row r on p.id = r.ptr_part where type = %d and ptr_species = %d and r.ptr_filter = %d" % [type, species, filter_id]
	db.query(query)
	return db.query_result

func load_part_preset(group: PartGroup, name: String, out: Dictionary[Part, String]):
	db.query("select * from sk_part_preset where name = '%s' and part_group = %d" % [name, group])
	var preset = db.query_result[0]
	var ptr_species = preset["ptr_species"]
	var part_group = preset["part_group"]

	db.query("select * from sk_part p inner join sk_part_preset_row r on p.name = r.part_name where r.ptr_part_preset = %d" % preset["id"])

	for part in db.query_result:
		if parts.has(part["type"]) and parts[part["type"]] != "None":
			continue
		out[part["type"]] = part["name"]

func load_color_preset(id: int, out: Dictionary):
	db.query("select * from sk_color_preset_row where ptr_color_preset = %d" % id)
	for row in db.query_result:
		var color = row["ptr_color_property"]
		if out.has(color) and out[color] != Color.TRANSPARENT:
			continue
		out[color] = Color(row["color"])

func part_preset_to_prop(group: PartGroup) -> String:
	return "part_preset_%s" % Part.find_key(group)

func part_preset_from_prop(prop: String) -> Variant:
	if not prop.begins_with("part_preset_"):
		return null
	return PartGroup[prop.trim_prefix("part_preset_")]

func part_to_prop(part: Part) -> String:
	return "part_%s" % Part.find_key(part)

func part_from_prop(prop: String) -> Variant:
	if not prop.begins_with("part_"):
		return null
	return Part[prop.trim_prefix("part_")]

func color_preset_to_prop(g: ColorGroup) -> String:
	return "color_preset_%s" % ColorGroup.find_key(g)

func color_preset_from_prop(prop: String) -> Variant:
	if not prop.begins_with("color_preset_"):
		return null
	return ColorGroup[prop.trim_prefix("color_preset_")]

func color_to_prop(color: int) -> String:
	return "color_%s" % get_color_prop(color)["name"]

func color_from_prop(prop: String) -> Variant:
	if not prop.begins_with("color_"):
		return null
	var key = prop.trim_prefix("color_")
	var i = color_properties.find_custom(func(c): return c["name"] == key)
	if i == -1:
		return null
	return color_properties[i]["id"]

func get_color_prop(color: int) -> Dictionary:
	var i = color_properties.find_custom(func(p): return p["id"] == color)
	return color_properties[i]

func get_material() -> StandardMaterial3D:
	var image: Image = load(sk_color_map).get_image().duplicate()
	if image.is_compressed():
		image.decompress()
	var final_colors := colors.duplicate()
	for group in color_presets:
		if color_presets[group] == "None":
			continue
		db.query("select id from sk_color_preset where name = '%s' and color_group = %d" % [color_presets[group], group])
		load_color_preset(db.query_result[0]["id"], final_colors)

	for id in final_colors:
		if final_colors[id] == Color.TRANSPARENT:
			continue
		var prop = get_color_prop(id)
		var u = prop["u"] * 2
		var v = prop["v"] * 2 * -1 + 31 # unity (0,0) is bottom left
		image.set_pixel(u, v, final_colors[id])
		image.set_pixel(u + 1, v, final_colors[id])
		image.set_pixel(u, v - 1, final_colors[id])
		image.set_pixel(u + 1, v - 1, final_colors[id])

	var material = StandardMaterial3D.new()
	material.albedo_texture = ImageTexture.create_from_image(image)
	return material
