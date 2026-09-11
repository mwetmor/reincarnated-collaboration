extends Node2D
var data: Dictionary
var textures: Dictionary = {}
var sample = 0
var images: Array = []
var drawing: Node2D
func _ready():
 data = JSON.parse_string(FileAccess.get_file_as_string("res://../scenes.json"))
 for id in data.assets:
  textures[id] = ImageTexture.create_from_image(Image.load_from_file("res://../"+data.assets[id].path))
 show_scene(0)
 if OS.get_cmdline_user_args().has("--capture"):
  capture_all.call_deferred()
func _unhandled_key_input(event):
 if event is InputEventKey and event.pressed and event.keycode == KEY_RIGHT:
  show_scene((sample+1)%data.scenes.size())
func show_scene(i):
 sample = i
 images = []
 if is_instance_valid(drawing):
  remove_child(drawing)
  drawing.queue_free()
 drawing = Node2D.new()
 add_child(drawing)
 for c in data.scenes[i].commands:
  if c.type == "image":
   var sprite: Node2D
   if data.assets[c.asset].has("mask"):
    var poly = Polygon2D.new()
    var points = PackedVector2Array()
    for pt in data.assets[c.asset].mask: points.append(Vector2(pt[0],pt[1]))
    poly.polygon = points
    poly.uv = points
    poly.texture = textures[c.asset]
    sprite = poly
   else:
    var plain = Sprite2D.new()
    plain.texture = textures[c.asset]
    plain.centered = false
    sprite = plain
   sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
   sprite.position = Vector2(c.x,c.y)
   sprite.scale = Vector2.ONE*c.scale
   drawing.add_child(sprite)
   images.append({"id":c.id,"x":sprite.position.x,"y":sprite.position.y,"scale":sprite.scale.x})
  elif c.type == "rect":
   var rect = Polygon2D.new()
   rect.polygon = PackedVector2Array([Vector2(c.x,c.y),Vector2(c.x+c.w,c.y),Vector2(c.x+c.w,c.y+c.h),Vector2(c.x,c.y+c.h)])
   rect.color = Color.hex(int(c.color)*256+255)
   drawing.add_child(rect)
  elif c.type == "line":
   var line = Line2D.new()
   for pt in c.points: line.add_point(Vector2(pt[0],pt[1]))
   line.width = c.width
   line.default_color = Color.hex(int(c.color)*256+255)
   line.antialiased = true
   drawing.add_child(line)
func capture_all():
 var records = []
 for i in range(data.scenes.size()):
  show_scene(i)
  await RenderingServer.frame_post_draw
  await get_tree().process_frame
  await RenderingServer.frame_post_draw
  var path = "res://../evidence/godot-"+data.scenes[i].id+".png"
  var err = get_viewport().get_texture().get_image().save_png(path)
  assert(err == OK)
  records.append({"scene":data.scenes[i].id,"images":images.duplicate(true)})
 var receipt = {"engine":"godot","version":Engine.get_version_info(),"adapter":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"cases":records}
 FileAccess.open("res://../evidence/godot-runtime.json",FileAccess.WRITE).store_string(JSON.stringify(receipt,"  ")+"\n")
 get_tree().quit()
