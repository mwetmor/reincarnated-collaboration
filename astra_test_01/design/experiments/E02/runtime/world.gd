extends Node2D

var perspective = true
var actor_world = Vector2.ZERO
var tracking = false
var bad_control = false
var profile: Dictionary
var layout: Dictionary
var mage: Sprite2D
var socket: Marker2D
var alpha_probe: Dictionary
var t: float
var yaw: float
var focal: float
var center_height = 38.475
var source_root = Vector2(256.25, 399.5)
var source_height = 223.5

func _ready():
	var profiles = JSON.parse_string(FileAccess.get_file_as_string("res://../inputs/projection-candidates.json"))
	profile = profiles[2] if perspective else profiles[1]
	layout = JSON.parse_string(FileAccess.get_file_as_string("res://../inputs/chamber-layout.json"))
	t = deg_to_rad(profile.elevation_deg)
	yaw = deg_to_rad(profile.yaw_deg)
	focal = 405.0 / 2.0 / tan(deg_to_rad(31.7861018306) / 2.0)
	var art = Image.load_from_file("res://../inputs/legacy-idle-S.png")
	alpha_probe = {"width":art.get_width(),"height":art.get_height(),"alpha_mode":art.detect_alpha(),"bytes":art.get_data_size()}
	mage = Sprite2D.new()
	mage.texture = ImageTexture.create_from_image(art)
	mage.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	mage.centered = false
	mage.offset = -source_root
	add_child(mage)
	socket = Marker2D.new()
	# A texture-coordinate attachment marker, not a qualified weapon socket.
	socket.position = Vector2(203, 187) - source_root
	mage.add_child(socket)
	update_actor()

func project(world: Vector2, height: float = 0.0) -> Vector2:
	var rel = world - (actor_world if tracking else Vector2.ZERO)
	var right = cos(yaw)*rel.x-sin(yaw)*rel.y
	var depth = sin(yaw)*rel.x+cos(yaw)*rel.y
	var factor: float = focal/(profile.distance_m-cos(t)*depth-sin(t)*height) if perspective else profile.uniform_scale_px_per_m
	return Vector2(profile.anchor[0],profile.anchor[1])+factor*Vector2(right,sin(t)*depth-cos(t)*height)

func update_actor():
	if not is_instance_valid(mage):
		return
	mage.position = project(actor_world)
	var body_height = project(actor_world).y-project(actor_world,2).y
	mage.scale = Vector2.ONE*body_height/source_height*(1.25 if bad_control else 1.0)
	queue_redraw()

func text(at: Vector2, value: String, size: int = 13, color: Color = Color("c8cbd0")):
	draw_string(ThemeDB.fallback_font,at,value,HORIZONTAL_ALIGNMENT_LEFT,-1,size,color)

func polygon(points: Array, color: Color):
	var screen = PackedVector2Array()
	for p in points:
		screen.append(project(Vector2(p[0],p[1])))
	draw_colored_polygon(screen,color)

func _draw():
	if profile == null or profile.is_empty():
		return
	draw_rect(Rect2(0,0,720,405),Color("20262c"))
	for surface in layout.surfaces:
		var r = surface.rect
		polygon([[r[0],r[1]],[r[2],r[1]],[r[2],r[3]],[r[0],r[3]]],Color("3d464e") if surface.id=="stone" else Color("514737"))
	for u in range(-5,6):
		draw_line(project(Vector2(u,-4)),project(Vector2(u,4)),Color("71736d"),0.7,true)
	for v in range(-4,5):
		draw_line(project(Vector2(-5,v)),project(Vector2(5,v)),Color("71736d"),0.7,true)
	# Footprints only: collision and sorting are outside this isolated probe.
	for object in layout.static_blocks+layout.objects:
		var r = object.rect
		var points = PackedVector2Array([project(Vector2(r[0],r[1])),project(Vector2(r[2],r[1])),project(Vector2(r[2],r[3])),project(Vector2(r[0],r[3])),project(Vector2(r[0],r[1]))])
		draw_polyline(points,Color("a49a82"),1,true)
	for exit in layout.exits:
		var point = project(Vector2(exit.point[0],exit.point[1]))
		draw_circle(point,3,Color("d8b87b"))
		text(point+Vector2(5,4),exit.id,11)
	var ring = PackedVector2Array()
	for i in range(65):
		var a = TAU*i/64.0
		ring.append(project(actor_world+Vector2(cos(a),sin(a))*.7))
	draw_polyline(ring,Color("c9ac6c"),1,true)
	var root = project(actor_world)
	draw_circle(root,2,Color("f5dfab"))
	# Known-size vertical calibration poles frame the actor without claiming anatomy.
	for offset in [-1.1,1.1]:
		var w = actor_world+Vector2(cos(yaw),-sin(yaw))*offset
		var a = project(w)
		var b = project(w,2)
		draw_line(a,b,Color("91a5b5"),1,true)
		draw_circle(b,2,Color("91a5b5"))
	# Keep masks/data visible. No painted environment or occlusion pass.
	draw_rect(Rect2(0,369,720,36),Color("13171b"))
	text(Vector2(12,390),"DIAGNOSTIC FLOOR / footprints only / frozen pose / no collision",12)
