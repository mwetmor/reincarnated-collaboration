# Executed in the Godot editor through MCP after create_scene/open_scene.
var root: Node3D = EditorInterface.get_edited_scene_root() as Node3D
assert(root != null and root.name == "Courtyard")
assert(root.get_child_count() == 0, "Author only into an empty test scene")

var stone: StandardMaterial3D = StandardMaterial3D.new()
stone.albedo_color = Color("333b45")
stone.roughness = 0.88
var trim: StandardMaterial3D = StandardMaterial3D.new()
trim.albedo_color = Color("ae8850")
trim.metallic = 0.45
trim.roughness = 0.5
var dark: StandardMaterial3D = StandardMaterial3D.new()
dark.albedo_color = Color("1a222c")
dark.roughness = 0.9

var environment_node: WorldEnvironment = WorldEnvironment.new()
environment_node.name = "EveningSky"
root.add_child(environment_node)
environment_node.owner = root
var environment: Environment = Environment.new()
environment.background_mode = Environment.BG_COLOR
environment.background_color = Color("171f2b")
environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
environment.ambient_light_color = Color("a8b9d4")
environment.ambient_light_energy = 0.4
environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
environment_node.environment = environment

var sun: DirectionalLight3D = DirectionalLight3D.new()
sun.name = "SoftSun"
sun.rotation_degrees = Vector3(-52, -26, 0)
sun.light_color = Color("ffe9ce")
sun.light_energy = 0.8
sun.shadow_enabled = true
sun.directional_shadow_max_distance = 40.0
root.add_child(sun)
sun.owner = root

var floor_body: StaticBody3D = StaticBody3D.new()
floor_body.name = "CourtyardFloor"
root.add_child(floor_body)
floor_body.owner = root
var floor_collision: CollisionShape3D = CollisionShape3D.new()
var floor_shape: BoxShape3D = BoxShape3D.new()
floor_shape.size = Vector3(20, 0.3, 20)
floor_collision.shape = floor_shape
floor_collision.position.y = -0.15
floor_body.add_child(floor_collision)
floor_collision.owner = root
var floor_mesh: MeshInstance3D = MeshInstance3D.new()
var floor_box: BoxMesh = BoxMesh.new()
floor_box.size = Vector3(20, 0.3, 20)
floor_mesh.mesh = floor_box
floor_mesh.material_override = dark
floor_mesh.position.y = -0.16
floor_body.add_child(floor_mesh)
floor_mesh.owner = root

# A single MultiMesh keeps the stone paving inexpensive.
var paving: MultiMeshInstance3D = MultiMeshInstance3D.new()
paving.name = "StonePaving"
var paving_mesh: BoxMesh = BoxMesh.new()
paving_mesh.size = Vector3(0.975, 0.04, 0.975)
paving_mesh.material = stone
var tiles: MultiMesh = MultiMesh.new()
tiles.transform_format = MultiMesh.TRANSFORM_3D
tiles.use_colors = true
tiles.mesh = paving_mesh
tiles.instance_count = 400
var tile_index: int = 0
for x: int in range(-10, 10):
	for z: int in range(-10, 10):
		tiles.set_instance_transform(tile_index, Transform3D(Basis.IDENTITY, Vector3(x + 0.5, -0.02, z + 0.5)))
		var value: float = 0.82 + float(posmod(x * 17 + z * 31, 7)) * 0.045
		tiles.set_instance_color(tile_index, Color(value, value, value, 1))
		tile_index += 1
stone.vertex_color_use_as_albedo = true
paving.multimesh = tiles
root.add_child(paving)
paving.owner = root

for radius: float in [2.6, 2.68]:
	var ring: MeshInstance3D = MeshInstance3D.new()
	ring.name = "BrassInlay"
	var ring_mesh: TorusMesh = TorusMesh.new()
	ring_mesh.inner_radius = radius
	ring_mesh.outer_radius = radius + 0.013
	ring_mesh.rings = 96
	ring_mesh.ring_segments = 6
	ring.mesh = ring_mesh
	ring.position.y = 0.003
	ring.material_override = trim
	root.add_child(ring)
	ring.owner = root

# Low perimeter walls provide real collision and keep the walk test contained.
for side: int in range(4):
	var wall: StaticBody3D = StaticBody3D.new()
	wall.name = "Boundary%d" % side
	wall.position = Vector3(0, 0.35, -9.5) if side == 0 else (Vector3(0, 0.35, 9.5) if side == 1 else (Vector3(-9.5, 0.35, 0) if side == 2 else Vector3(9.5, 0.35, 0)))
	var size: Vector3 = Vector3(19.4, 0.7, 0.3) if side < 2 else Vector3(0.3, 0.7, 19.4)
	root.add_child(wall)
	wall.owner = root
	var collision: CollisionShape3D = CollisionShape3D.new()
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = size
	collision.shape = shape
	wall.add_child(collision)
	collision.owner = root
	var visible: MeshInstance3D = MeshInstance3D.new()
	var box_mesh: BoxMesh = BoxMesh.new()
	box_mesh.size = size
	visible.mesh = box_mesh
	visible.material_override = stone
	wall.add_child(visible)
	visible.owner = root

for location: Vector3 in [Vector3(-4.2,0,-4.2), Vector3(4.2,0,-4.2), Vector3(-4.2,0,4.2), Vector3(4.2,0,4.2)]:
	var column: StaticBody3D = StaticBody3D.new()
	column.name = "CourtyardPillar"
	column.position = location
	root.add_child(column)
	column.owner = root
	var shape: CylinderShape3D = CylinderShape3D.new()
	shape.height = 1.7
	shape.radius = 0.29
	var collider: CollisionShape3D = CollisionShape3D.new()
	collider.shape = shape
	collider.position.y = 0.85
	column.add_child(collider)
	collider.owner = root
	for tier: int in range(3):
		var pillar_part: MeshInstance3D = MeshInstance3D.new()
		var cylinder: CylinderMesh = CylinderMesh.new()
		cylinder.top_radius = 0.34 if tier != 1 else 0.24
		cylinder.bottom_radius = cylinder.top_radius
		cylinder.height = 0.17 if tier != 1 else 1.35
		cylinder.radial_segments = 8
		pillar_part.mesh = cylinder
		pillar_part.position.y = [0.085, 0.845, 1.6][tier]
		pillar_part.material_override = trim if tier == 2 else stone
		column.add_child(pillar_part)
		pillar_part.owner = root

var player: CharacterBody3D = CharacterBody3D.new()
player.name = "Player"
player.set_script(load("res://scripts/wizard_player.gd"))
root.add_child(player)
player.owner = root
var capsule: CollisionShape3D = CollisionShape3D.new()
capsule.name = "BodyCollision"
var capsule_shape: CapsuleShape3D = CapsuleShape3D.new()
capsule_shape.height = 1.8
capsule_shape.radius = 0.24
capsule.shape = capsule_shape
capsule.position.y = 0.9
player.add_child(capsule)
capsule.owner = root
var visual: Node3D = Node3D.new()
visual.name = "Visual"
player.add_child(visual)
visual.owner = root
var wizard_scene: PackedScene = load("res://assets/purple_wizard.glb") as PackedScene
assert(wizard_scene != null)
var wizard: Node3D = wizard_scene.instantiate()
wizard.name = "Wizard"
visual.add_child(wizard)
wizard.owner = root
var camera: Camera3D = Camera3D.new()
camera.name = "Camera3D"
camera.current = true
camera.fov = 39.0
camera.near = 0.05
camera.far = 80.0
camera.position = Vector3(2.5, 2.8, 4.0)
player.add_child(camera)
camera.owner = root

var hud: CanvasLayer = CanvasLayer.new()
hud.name = "HUD"
root.add_child(hud)
hud.owner = root
for definition: Dictionary in [
	{"name":"Title", "text":"THE GILDED GRIMOIRE", "position":Vector2(32,25), "size":26, "color":Color("e7c58e")},
	{"name":"Subtitle", "text":"A wizard in motion", "position":Vector2(33,61), "size":16, "color":Color("a8b5c6")},
	{"name":"Controls", "text":"W A S D   MOVE     /     SHIFT   SPRINT     /     SCROLL   ZOOM     /     ESC   EXIT", "position":Vector2(32,753), "size":15, "color":Color("e1dfda")},
	{"name":"Status", "text":"IDLE   /   0.0 m/s", "position":Vector2(1030,34), "size":17, "color":Color("e7c58e")}
]:
	var label: Label = Label.new()
	label.name = definition["name"]
	label.text = definition["text"]
	label.position = definition["position"]
	label.add_theme_font_size_override("font_size", definition["size"])
	label.add_theme_color_override("font_color", definition["color"])
	label.add_theme_color_override("font_shadow_color", Color(0,0,0,0.75))
	label.add_theme_constant_override("shadow_offset_y", 2)
	hud.add_child(label)
	label.owner = root

EditorInterface.mark_scene_as_unsaved()
_mcp_print({"scene":root.name,"children":root.get_child_count(),"wizard_imported":wizard_scene.resource_path})
