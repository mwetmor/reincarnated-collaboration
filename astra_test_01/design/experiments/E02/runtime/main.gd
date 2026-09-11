extends Node2D

const World = preload("res://world.gd")
var worlds = []
var viewports = []
var samples: Array
var sample_index = 0
var tracking = false
var elapsed = 0.0
var animate = true
var capture = false
var capture_frame = 0
var batch = ""
var run_checks = []

func _ready():
	samples = JSON.parse_string(FileAccess.get_file_as_string("res://../evidence/analysis.json")).samples
	var args = OS.get_cmdline_user_args()
	capture = args.has("--capture")
	batch = "fixed-v2" if not args.has("--tracking") else "tracking-v2"
	tracking = args.has("--tracking")
	for i in range(2):
		var viewport = SubViewport.new()
		viewport.size = Vector2i(720,405)
		viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		add_child(viewport)
		var world = World.new()
		world.perspective = (i==1)
		viewport.add_child(world)
		worlds.append(world)
		viewports.append(viewport)
	if capture:
		animate = false
		capture_all.call_deferred()

func _unhandled_key_input(event):
	if event is InputEventKey and event.pressed:
		if event.keycode==KEY_SPACE:
			animate = not animate
		if event.keycode==KEY_T:
			tracking = not tracking
		if event.keycode==KEY_RIGHT:
			sample_index = (sample_index+1)%samples.size()
			animate = false
		if event.keycode==KEY_LEFT:
			sample_index = (sample_index+samples.size()-1)%samples.size()
			animate = false
		if event.keycode==KEY_B:
			worlds[1].bad_control = not worlds[1].bad_control

func _process(delta):
	if capture:
		return
	elapsed += delta
	if animate:
		sample_index = int(elapsed/2.0)%samples.size()
	update_worlds()

func update_worlds():
	var point = Vector2(samples[sample_index].world[0],samples[sample_index].world[1])
	for world in worlds:
		world.actor_world = point
		world.tracking = tracking
		world.update_actor()
	queue_redraw()

func text(at: Vector2, value: String, size: int = 16, color: Color = Color("e2e0db")):
	draw_string(ThemeDB.fallback_font,at,value,HORIZONTAL_ALIGNMENT_LEFT,-1,size,color)

func _draw():
	if worlds.size()!=2:
		return
	text(Vector2(20,30),"E02 / C PERSPECTIVE / PAINTED SPRITE TRANSFER",23)
	text(Vector2(20,59),"Following camera" if tracking else "Fixed room camera",17)
	text(Vector2(340,59),"Position: "+samples[sample_index].id+" | same painted source in both views",16)
	for i in range(2):
		var off = Vector2(i*720,95)
		text(off+Vector2(15,-10),"B / affine diagnostic control" if i==0 else "C / chosen perspective candidate",18)
		draw_texture(viewports[i].get_texture(),off)
		var root = worlds[i].project(worlds[i].actor_world)
		var region = Rect2(root-Vector2(85,105),Vector2(170,135))
		draw_texture_rect_region(viewports[i].get_texture(),Rect2(i*720+60,555,510,405),region)
		text(Vector2(i*720+60,539),"3x diagnostic enlargement / judge normal size above",14)
	text(Vector2(610,590),"SPACE pause",13)
	text(Vector2(610,613),"arrows position",13)
	text(Vector2(610,636),"T camera policy",13)
	text(Vector2(610,659),"B bad scale",13)
	if worlds[1].bad_control:
		text(Vector2(745,59),"BAD CONTROL: 25% oversized",17,Color("ffaf80"))

func capture_all():
	# Avoid assuming a successful dummy renderer is evidence.
	for i in range(samples.size()):
		sample_index = i
		update_worlds()
		await RenderingServer.frame_post_draw
		await get_tree().process_frame
		await RenderingServer.frame_post_draw
		var image = get_viewport().get_texture().get_image()
		var path = "res://../evidence/"+batch+"-"+samples[i].id+".png"
		var err = image.save_png(path)
		assert(err==OK)
		var world = worlds[1]
		var expected_root = world.project(world.actor_world)
		var expected_socket = expected_root+(Vector2(203,187)-world.source_root)*world.mage.scale
		var actual_socket = world.socket.global_position
		var measured_root = world.mage.position
		var measured_top = world.project(world.actor_world,2)
		world.mage.position.x += 8
		var bad_root_error = world.mage.position.distance_to(expected_root)
		world.mage.position = measured_root
		var old_socket = world.socket.position
		world.socket.position.x += 8 / world.mage.scale.x
		var bad_socket_error = world.socket.global_position.distance_to(expected_socket)
		world.socket.position = old_socket
		run_checks.append({"sample":samples[i].id,"tracking":tracking,"root_px":[measured_root.x,measured_root.y],"top_px":[measured_top.x,measured_top.y],"source_scale":world.mage.scale.x,"root_error_px":measured_root.distance_to(expected_root),"socket_error_px":actual_socket.distance_to(expected_socket),"bad_root_error_px":bad_root_error,"bad_socket_error_px":bad_socket_error,"screenshot":path,"image_size":[image.get_width(),image.get_height()]})
		if samples[i].id in ["center","right","near","far"]:
			viewports[1].get_texture().get_image().save_png("res://../evidence/godot-"+batch+"-"+samples[i].id+"-native.png")
	# Render a visible known-bad control in the same process.
	sample_index = 0
	worlds[1].bad_control = true
	update_worlds()
	await RenderingServer.frame_post_draw
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("res://../evidence/"+batch+"-bad-scale.png")
	var record = {"godot":Engine.get_version_info(),"adapter":RenderingServer.get_video_adapter_name(),"renderer":RenderingServer.get_current_rendering_method(),"alpha":worlds[1].alpha_probe,"checks":run_checks}
	FileAccess.open("res://../evidence/runtime-"+batch+".json",FileAccess.WRITE).store_string(JSON.stringify(record,"  ")+"\n")
	get_tree().quit()
