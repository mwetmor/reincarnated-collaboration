extends SceneTree
# C-9 T10: IS THE FOG DOING ANYTHING, and where.
#
# The delivered capture measured `fog_enabled` on versus off at the play camera as changing
# EXACTLY 0.0% of the frame -- byte-identical PNGs. That is not a fog that is too subtle to
# see; it is a fog that is not being applied, and the reason is arithmetic rather than
# mysterious: the play camera is orthographic with 10.73 m of screen height, which is 13.4 m
# of ground depth at 52.95 deg, and it sits CAM_STANDOFF = 60 m back. So the whole frame lies
# between about 53 and 67 m of view depth, and fog_depth_begin is 60 + 8 = 68 m. The frame
# ends where the fog starts.
#
# This asks the question the capture could not: at what framing does the fog begin to do
# something, and how much. Three zooms, each with the fog on and off, differenced.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_fog.gd -- --out DIR

const SHOT := Vector2i(960, 540)

var out := ""
var report := {}


func _initialize() -> void:
	out = ProjectSettings.globalize_path("user://probe_fog")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out)

	var vp := SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var scene = preload("res://scripts/barrow_world.gd").new()
	scene.skip_character = true
	vp.add_child(scene)
	for i in 60:
		await process_frame
		await physics_frame
	scene.set_hud_visible(false)
	scene.set_particles(false)

	var env: Environment = scene.env_node.environment
	report["fog"] = {"begin_m": env.fog_depth_begin, "end_m": env.fog_depth_end,
					 "density": env.fog_density, "height_m": env.fog_height,
					 "height_density": env.fog_height_density,
					 "cam_standoff_m": scene.CAM_STANDOFF}
	var aim := Vector3(BarrowStandIn.MOUND_CENTRE.x,
		scene.world.height_at(BarrowStandIn.MOUND_CENTRE.x, BarrowStandIn.MOUND_CENTRE.y + 6.0) + 1.2,
		BarrowStandIn.MOUND_CENTRE.y + 6.0)
	var rows := {}
	for zoom in [1.0, 0.5, 0.25, 0.12]:
		scene.park_camera(aim, zoom)
		var half_depth: float = (scene.cam.size / sin(deg_to_rad(52.95354112560294))) * 0.5
		scene.set_fog(true)
		await _settle(vp)
		var a: Image = vp.get_texture().get_image()
		scene.set_fog(false)
		await _settle(vp)
		var b: Image = vp.get_texture().get_image()
		scene.set_fog(true)
		var n := 0
		var changed := 0
		var sum := 0.0
		for y in range(0, a.get_height(), 2):
			for x in range(0, a.get_width(), 2):
				var ca := a.get_pixel(x, y)
				var cb := b.get_pixel(x, y)
				var d: float = absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)
				sum += d
				if d > 0.008:
					changed += 1
				n += 1
		if zoom <= 0.5:
			a.save_png("%s/fog_on_z%.2f.png" % [out, zoom])
			b.save_png("%s/fog_off_z%.2f.png" % [out, zoom])
		rows["zoom_%.2f" % zoom] = {
			"ortho_size_m": snappedf(scene.cam.size, 0.01),
			"frame_depth_span_m": snappedf(half_depth * 2.0, 0.1),
			"view_depth_range_m": [snappedf(scene.CAM_STANDOFF - half_depth, 0.1),
								   snappedf(scene.CAM_STANDOFF + half_depth, 0.1)],
			"px_changed_share": snappedf(float(changed) / float(n), 0.0001),
			"mean_abs_delta": snappedf(sum / float(n), 0.00001),
		}
		print("[fog] zoom %.2f  depth %.1f..%.1f m  changed %.2f%%" % [zoom,
			scene.CAM_STANDOFF - half_depth, scene.CAM_STANDOFF + half_depth,
			100.0 * float(changed) / float(n)])
	report["by_zoom"] = rows
	var f := FileAccess.open(out + "/probe_fog.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	print("[fog] -> %s" % out)
	quit(0)


func _settle(vp: SubViewport) -> void:
	for i in 6:
		await process_frame
	RenderingServer.force_draw()
	await process_frame
