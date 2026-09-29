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
# something, and how much. Each place is rendered with the fog on and off, and differenced.
#
# ⚠ UNITS: the delta below is a SUM OVER THREE CHANNELS. Divide by 3 for the per-channel
# figure a person can picture. Reported both ways because reading the sum as per-channel is
# how I concluded that a 7%-per-channel veil was a total white-out and nearly threw it away
# -- and because the basin at the play camera is almost featureless snow, which the eye
# reads as sky, so the number is the only honest judge of what changed.
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
	report["fog"] = {"mode": env.fog_mode, "distance_density": env.fog_density,
					 "height_y": env.fog_height, "height_density": env.fog_height_density,
					 "cam_standoff_m": scene.CAM_STANDOFF,
					 "_q": "with the distance term at 0, does the HEIGHT term still act?"}
	# THE QUESTION IS NOW NARROWER: the distance term is off by decision, so what is left is
	# whether the HEIGHT term reads IN THE BASIN AT THE PLAY CAMERA. The mound is the control
	# -- it stands above the fog height, so it must come back at essentially zero, and if it
	# does not then what is being measured is not height fog.
	var places := {
		"basin_play": [BarrowStandIn.BASIN_CENTRE, 1.0],
		"basin_wide": [BarrowStandIn.BASIN_CENTRE, 0.45],
		"mound_play_CONTROL": [BarrowStandIn.MOUND_CENTRE, 1.0],
	}
	var rows := {}
	for name in places:
		var c: Vector2 = places[name][0]
		var zoom: float = places[name][1]
		var ground: float = scene.world.height_at(c.x, c.y)
		var aim := Vector3(c.x, ground + 1.0, c.y)
		scene.park_camera(aim, zoom)
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
		a.save_png("%s/fog_on_%s.png" % [out, name])
		b.save_png("%s/fog_off_%s.png" % [out, name])
		rows[name] = {
			"aim_xz": [c.x, c.y], "ground_y": snappedf(ground, 0.01),
			"fog_height_y": snappedf(env.fog_height, 0.01),
			"ground_below_fog_top_by_m": snappedf(env.fog_height - ground, 0.01),
			"ortho_size_m": snappedf(scene.cam.size, 0.01),
			"px_changed_share": snappedf(float(changed) / float(n), 0.0001),
			"mean_abs_delta_3ch_SUM": snappedf(sum / float(n), 0.00001),
			"mean_abs_delta_per_channel": snappedf(sum / float(n) / 3.0, 0.00001),
		}
		print("[fog] %-20s ground %.2f  fog top %.2f  changed %.2f%%  mean|d| %.5f" % [name,
			ground, env.fog_height, 100.0 * float(changed) / float(n), sum / float(n)])
	report["by_place"] = rows

	# --- HOW MUCH IS "A LITTLE" ---------------------------------------------
	# 0.55 whited the basin out completely: 98.4% of the frame changed and only a birch top
	# survived. Rather than halve it and look again, and again, the density is swept and the
	# number chosen off the curve. The target is a VEIL -- the ground still legible through
	# it -- which is a mean absolute delta of a few hundredths, not a fifth.
	var c: Vector2 = BarrowStandIn.BASIN_CENTRE
	var ground: float = scene.world.height_at(c.x, c.y)
	scene.park_camera(Vector3(c.x, ground + 1.0, c.y), 1.0)
	scene.set_fog(false)
	await _settle(vp)
	var clean: Image = vp.get_texture().get_image()
	var sweep := {}
	for dens in [0.006, 0.012, 0.025, 0.05, 0.10, 0.20]:
		env.fog_height_density = dens
		scene.set_fog(true)
		await _settle(vp)
		var f: Image = vp.get_texture().get_image()
		var n := 0
		var changed := 0
		var sum := 0.0
		for y in range(0, f.get_height(), 2):
			for x in range(0, f.get_width(), 2):
				var ca := f.get_pixel(x, y)
				var cb := clean.get_pixel(x, y)
				var d: float = absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)
				sum += d
				if d > 0.008:
					changed += 1
				n += 1
		f.save_png("%s/fog_dens_%.3f.png" % [out, dens])
		sweep["%.3f" % dens] = {"px_changed_share": snappedf(float(changed) / float(n), 0.0001),
								"mean_abs_delta_3ch_SUM": snappedf(sum / float(n), 0.00001),
								"mean_abs_delta_per_channel": snappedf(sum / float(n) / 3.0, 0.00001)}
		print("[fog] density %.3f  changed %.1f%%  mean|d| %.5f" % [dens,
			100.0 * float(changed) / float(n), sum / float(n)])
		scene.set_fog(false)
		await _settle(vp)
	report["height_density_sweep_at_basin_play"] = sweep

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
