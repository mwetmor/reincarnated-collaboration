extends SceneTree
## C-9 T10-2 step 1: capture and MEASURE the Barrow blockout.
##
##   Godot --path godot --resolution 640x360 --script tools/capture_blockout.gd -- --out DIR
##         [--no-walks] [--no-cost] [--atlas 8192]
##
## Windowed, not headless: every still is read back from a SubViewport, which needs a Metal
## surface. The OS window is small on purpose -- nothing it draws is kept.
##
## Writes into --out:
##   built.json            every placement as BUILT: world transform, loaded AABB, fit, footprint
##   walk_grid.json        the free-space grid and the flood fill from the entry, row strings
##   capture_report.json   the measurements: flood fill, door floor, the walks, the frame cost,
##                         the projected guide corners and markers
##   guide_calibration.png 4096 x 2560 with the 1 m / 2 m markers (the instrument check)
##   guide.png             4096 x 2560, the paint-over guide
##   still_ring.png, still_tarn.png   1920 x 1080 play-screen stills
##   topdown.png           the map's base render, straight down, 48 px/m

const GUIDE := Vector2i(4096, 2560)
const PLAY := Vector2i(1920, 1080)
const TOP_PX_PER_M := 48.0
const TOP := Vector2i(2112, 1690)
const DT := 1.0 / 60.0
const TERRAIN_BIT := 1 << 1

var out_dir := ""
var do_walks := true
var do_cost := true
var atlas := 8192
var vp: SubViewport
var scene
var rep := {}


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
		if args[i] == "--no-walks":
			do_walks = false
		if args[i] == "--no-cost":
			do_cost = false
		if args[i] == "--atlas" and i + 1 < args.size():
			atlas = int(args[i + 1])
	if out_dir == "":
		print("[capture] HALT: --out DIR is required")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = PLAY
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_4X
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/barrow_full.tscn").instantiate()
	vp.add_child(scene)
	var waited := 0
	while not scene.ready_done and waited < 1500:
		await process_frame
		waited += 1
	if not scene.ready_done:
		print("[capture] HALT: the scene never finished building")
		quit(3)
		return
	for i in 20:
		await physics_frame
		await process_frame
	rep["scene"] = scene.report
	rep["viewport"] = {"msaa": "4x", "play": [PLAY.x, PLAY.y], "guide": [GUIDE.x, GUIDE.y]}

	# ---- 1. what was built --------------------------------------------------------------
	var t0 := Time.get_ticks_msec()
	var recs: Dictionary = scene.build_records()
	_write("built.json", {"records": recs, "scene_report": scene.report,
		"_": "BUILT numbers, measured off the scene; finalize.py merges them into barrow_full_layout.json"})
	rep["records_ms"] = Time.get_ticks_msec() - t0
	print("[capture] records: %d pieces" % recs.size())

	# ---- 2. walkability: free space for HIS capsule, and the flood fill from the entry ----
	vp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	rep["walk_grid"] = await _walk_grid()
	rep["door_floor"] = await _door_floor()
	print("[capture] walk grid: %s" % JSON.stringify(rep["walk_grid"]["summary"]))

	# ---- 3. he walks it: the routes the layout promises, and the ones it must refuse ------
	var k = scene.knight
	if do_walks:
		rep["walks"] = await _walks()
		print("[capture] walks done")
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS

	# ---- 4. the guide, at the play camera's own scale, 4096 x 2560 ------------------------
	k.set_physics_process(false)
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	var gk: Array = scene.layout["knight"]["guide_uv"]
	scene.place_knight(float(gk[0]), float(gk[1]), String(scene.layout["knight"].get("guide_facing", "S")))
	for i in 10:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	var prev_atlas := int(ProjectSettings.get_setting("rendering/lights_and_shadows/directional_shadow/size", 4096))
	RenderingServer.directional_shadow_atlas_set_size(atlas, true)
	vp.size = GUIDE
	scene.park_camera(Vector3.ZERO, 1.0)
	var mk: Dictionary = scene.set_markers(true)
	await _settle()
	rep["guide"] = _guide_geometry(mk)
	rep["guide"]["shadow_atlas_px"] = atlas
	rep["guide"]["him_screen_rect_px"] = _rect(scene.character_screen_rect())
	await _shot("guide_calibration")
	scene.set_markers(false)
	await _settle()
	await _shot("guide")
	RenderingServer.directional_shadow_atlas_set_size(prev_atlas, true)

	# ---- 5. two play-screen stills, 1920 x 1080, the play camera as the app frames it -----
	vp.size = PLAY
	for spec in [["still_ring", Vector2(0.0, 1.0), "NE"], ["still_tarn", Vector2(-10.5, -4.5), "W"]]:
		scene.freeze_pose(false)
		scene.place_knight(spec[1].x, spec[1].y, spec[2])
		for i in 10:
			k.drive_dir(Vector2.ZERO, false, DT)
			await physics_frame
		scene.freeze_pose(true)
		scene.park_camera(scene._camera_aim(), 1.0)
		await _settle()
		rep[spec[0]] = {"him_uv": [spec[1].x, spec[1].y], "facing": spec[2],
			"camera_clamped": scene.clamp_on, "him_screen_rect_px": _rect(scene.character_screen_rect())}
		await _shot(spec[0])

	# ---- 6. the map's base: straight down, +u right, +v up, 48 px/m, shadows off ----------
	vp.size = TOP
	var sun: DirectionalLight3D = scene.sun
	sun.shadow_enabled = false
	scene.place_knight(float(gk[0]), float(gk[1]), "S")
	scene.set_topdown(Vector2(0.0, 0.0), float(TOP.y) / TOP_PX_PER_M)
	await _settle()
	rep["topdown"] = {"px": [TOP.x, TOP.y], "px_per_m": TOP_PX_PER_M, "centre_uv": [0.0, 0.0],
					  "u": [-float(TOP.x) * 0.5 / TOP_PX_PER_M, float(TOP.x) * 0.5 / TOP_PX_PER_M],
					  "v": [-float(TOP.y) * 0.5 / TOP_PX_PER_M, float(TOP.y) * 0.5 / TOP_PX_PER_M],
					  "shadows": "off -- a plan, not a view"}
	await _shot("topdown")
	sun.shadow_enabled = true

	# ---- 7. frame cost at 1080p, him walking, vsync off; checked at 2.25x the pixels -------
	if do_cost:
		vp.size = PLAY
		scene.freeze_pose(false)
		scene.unpark_camera()
		scene.place_knight(0.0, -3.0, "N")
		await _settle()
		rep["frame_cost_ms"] = {
			"_at": "SubViewport, MSAA 4x, Apple M2 8 GB, vsync off, him walking a loop in the ring with the full kit",
			"play_1920x1080": await _time_frames(240, PLAY),
			"instrument_check_2880x1620": await _time_frames(160, Vector2i(2880, 1620)),
		}
		print("[capture] frame cost: %s" % JSON.stringify(rep["frame_cost_ms"]))
	_write("capture_report.json", rep)
	print("[capture] -> %s" % out_dir)
	quit(0)


# --- measurements ------------------------------------------------------------------------
func _walk_grid() -> Dictionary:
	"""FREE SPACE FOR HIM, by the physics server: at every 0.25 m cell, does a vertical cylinder
	of his capsule's radius (0.35 m), 1.8 m tall and lifted 5 cm off the floor, touch anything on
	the terrain layer? Then a 4-connected flood fill from the entry. What the grid says is what
	his collider can occupy; the scripted walks below check that his controller agrees."""
	await physics_frame
	var space: PhysicsDirectSpaceState3D = (scene as Node3D).get_world_3d().direct_space_state
	var cyl := CylinderShape3D.new()
	cyl.radius = 0.35
	cyl.height = 1.8
	var q := PhysicsShapeQueryParameters3D.new()
	q.shape = cyl
	q.collision_mask = TERRAIN_BIT
	var step := 0.25
	var u0 := -21.0
	var v0 := -17.5
	var nu := int(round(42.0 / step)) + 1
	var nv := int(round(34.5 / step)) + 1
	var free := PackedByteArray()
	free.resize(nu * nv)
	var t0 := Time.get_ticks_msec()
	for j in nv:
		for i in nu:
			var u := u0 + float(i) * step
			var v := v0 + float(j) * step
			var fy: float = scene.floor_y_at(u, v)
			var lift := 0.05 if absf(fy) < 1e-6 else 0.30
			q.transform = Transform3D(Basis(), scene.uv_to_world(u, v, fy + lift + 0.9))
			free[j * nu + i] = 1 if space.intersect_shape(q, 1).is_empty() else 0
	var t_q := Time.get_ticks_msec() - t0
	var L: Dictionary = scene.layout
	var sp: Array = L["knight"]["spawn_uv"]
	var si := int(round((float(sp[0]) - u0) / step))
	var sj := int(round((float(sp[1]) - v0) / step))
	var seen := PackedByteArray()
	seen.resize(nu * nv)
	var queue := [sj * nu + si]
	var head := 0
	if free[sj * nu + si] == 1:
		seen[sj * nu + si] = 1
	else:
		queue = []
	while head < queue.size():
		var c: int = queue[head]
		head += 1
		var ci := c % nu
		var cj := c / nu
		for d in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
			var ni: int = ci + d[0]
			var nj: int = cj + d[1]
			if ni < 0 or nj < 0 or ni >= nu or nj >= nv:
				continue
			var n := nj * nu + ni
			if free[n] == 1 and seen[n] == 0:
				seen[n] = 1
				queue.append(n)
	# the checks
	var bounds: Array = L["bounds"]["polygon_uv"]
	var poly := PackedVector2Array()
	for p in bounds:
		poly.append(Vector2(float(p[0]), float(p[1])))
	var R: Dictionary = L["regions"]
	var ic: Array = R["ice"]["centre_uv"]
	var ia := float(R["ice"]["axes_m"][0]) * 0.5
	var ib := float(R["ice"]["axes_m"][1]) * 0.5
	var m: Dictionary = scene._mound_spec()
	var mc := Vector2(float(m["uv"][0]), float(m["uv"][1]))
	var ma := float(m["semi_axes"][0])
	var mb := float(m["semi_axes"][1])
	var pa: Dictionary = m["passage"]
	var reach := 0
	var leak := []
	var leak_n := 0
	var ice_free := 0
	var ice_reach := 0
	var mound_reach := 0
	var mound_list := []
	var rows := []
	for j in nv:
		var row := ""
		for i in nu:
			var c := j * nu + i
			var u := u0 + float(i) * step
			var v := v0 + float(j) * step
			var ch := "#"
			if free[c] == 1:
				ch = "."
			if seen[c] == 1:
				ch = "o"
				reach += 1
				if not Geometry2D.is_point_in_polygon(Vector2(u, v), poly):
					leak_n += 1
					if leak.size() < 12:
						leak.append([u, v])
				var in_passage: bool = absf(u) < float(pa["half_w"]) and v > float(pa["v0"]) - 0.01 and v < float(pa["v_mouth"])
				if pow((u - mc.x) / ma, 2.0) + pow((v - mc.y) / mb, 2.0) < 1.0 and not in_passage:
					mound_reach += 1
					if mound_list.size() < 12:
						mound_list.append([u, v])
			var in_ice := pow((u - float(ic[0])) / ia, 2.0) + pow((v - float(ic[1])) / ib, 2.0) <= 1.0
			if in_ice and free[c] == 1:
				ice_free += 1
				if seen[c] == 1:
					ice_reach += 1
			row += ch
		rows.append(row)
	var at := func(u: float, v: float) -> bool:
		var i := int(round((u - u0) / step))
		var j := int(round((v - v0) / step))
		return i >= 0 and j >= 0 and i < nu and j < nv and seen[j * nu + i] == 1
	var targets := {
		"arena_centre_(0,1)": at.call(0.0, 1.0),
		"ice_centre_(-13,-5)": at.call(-13.0, -5.0),
		"before_the_door_(0,7.25)": at.call(0.0, 7.25),
		"in_the_doorway_(0,7.5)": at.call(0.0, 7.5),
		# 8.5, not 8.75: the bottom tread is 0.30 m deep before the passage mouth, so a 0.35 m
		# capsule can never be CENTRED on it -- the deepest cell his collider fits is 8.5
		"on_the_steps_(0,8.5)": at.call(0.0, 8.5),
	}
	var summary := {"cells": nu * nv, "cell_m": step, "free_cells": _count(free), "reachable_cells": reach,
		"reachable_m2": snappedf(float(reach) * step * step, 0.1), "targets": targets,
		"ice_free_cells": ice_free, "ice_reachable_cells": ice_reach,
		"ice_reachable_share": snappedf(float(ice_reach) / maxf(float(ice_free), 1.0), 0.0001),
		"reachable_outside_bounds": leak_n, "reachable_inside_mound_outside_passage": mound_reach,
		"query_ms": t_q}
	_write("walk_grid.json", {"u0": u0, "v0": v0, "step": step, "nu": nu, "nv": nv,
		"legend": {"#": "blocked (his capsule touches something)", ".": "free, NOT reachable from the entry", "o": "reachable from the entry"},
		"rows_from_v0_up": rows, "spawn_uv": sp})
	return {"summary": summary, "leak_samples_uv": leak, "mound_samples_uv": mound_list,
		"instrument": "PhysicsDirectSpaceState3D.intersect_shape, a CylinderShape3D r 0.35 h 1.8, bottom 5 cm off the floor (30 cm in the passage), mask TERRAIN_BIT; 4-connected flood fill from spawn_uv"}


func _count(a: PackedByteArray) -> int:
	var n := 0
	for x in a:
		n += int(x)
	return n


func _door_floor() -> Dictionary:
	"""Straight down at the door and on each step: where does a ray find the floor? Started at
	1.5 m, under the lintel (2.04 m), so the beam overhead is not what it hits."""
	await physics_frame
	var space: PhysicsDirectSpaceState3D = (scene as Node3D).get_world_3d().direct_space_state
	var out := {}
	for v in [7.3, 7.5, 7.6, 7.8, 8.1, 8.5, 8.9]:
		var a: Vector3 = scene.uv_to_world(0.0, v, 1.5)
		var b: Vector3 = scene.uv_to_world(0.0, v, -3.0)
		var rq := PhysicsRayQueryParameters3D.create(a, b, TERRAIN_BIT)
		var hit := space.intersect_ray(rq)
		out["v=%.1f" % v] = snappedf(float(hit["position"].y), 0.0001) if not hit.is_empty() else null
	return {"floor_y_by_v_at_u0": out, "instrument": "intersect_ray from y 1.5 to -3.0, mask TERRAIN_BIT"}


func _walk_route(nm: String, start: Vector2, wps: Array, run: bool, max_frames: int,
		expect_reach: bool) -> Dictionary:
	var k = scene.knight
	scene.place_knight(start.x, start.y, "N")
	await physics_frame
	var wi := 0
	var frames := 0
	var track := []
	var best := INF
	while wi < wps.size() and frames < max_frames:
		var pos: Vector2 = scene.knight_uv()
		var tgt: Vector2 = wps[wi]
		var last := wi == wps.size() - 1
		if pos.distance_to(tgt) < (0.3 if last else 0.7):
			wi += 1
			continue
		if last:
			best = minf(best, pos.distance_to(tgt))
		k.drive_dir(scene.canvas_dir_uv(pos, tgt), run and pos.distance_to(tgt) > 2.5, DT)
		await physics_frame
		frames += 1
		if frames % 20 == 0:
			track.append([snappedf(pos.x, 0.01), snappedf(pos.y, 0.01)])
	for i in 20:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	var end: Vector2 = scene.knight_uv()
	var tgt_end: Vector2 = wps[wps.size() - 1]
	var reached := wi >= wps.size()
	return {"from_uv": [start.x, start.y], "to_uv": [tgt_end.x, tgt_end.y], "reached": reached,
		"expected_to_reach": expect_reach, "PASS": reached == expect_reach,
		"end_uv": [snappedf(end.x, 0.01), snappedf(end.y, 0.01)],
		"end_floor_y": snappedf(k.global_position.y, 0.001),
		"end_distance_to_target_m": snappedf(end.distance_to(tgt_end), 0.01),
		"frames": frames, "seconds": snappedf(float(frames) * DT, 0.01), "track_uv": track}


func _walks() -> Dictionary:
	var k = scene.knight
	k.set_physics_process(false)
	var out := {}
	var sp: Array = scene.layout["knight"]["spawn_uv"]
	var S := Vector2(float(sp[0]), float(sp[1]))
	out["entry_to_arena"] = await _walk_route("entry_to_arena", S,
		[Vector2(-2.3, -11.0), Vector2(-0.6, -8.0), Vector2(0.0, -6.2), Vector2(0.0, 1.0)], true, 1500, true)
	# THROUGH THE RING'S WEST GAP, between the -95 (fallen) and -125 stones. The first version
	# drove a straight line from (-4.6, -1) to (-11, -5), which passes 0.43 m from the -125
	# stone: he walked into it and stayed there for 25 s. That was the ROUTE, not the layout --
	# the flood fill had every ice cell reachable -- and a steering script is not a path-finder.
	out["arena_to_ice"] = await _walk_route("arena_to_ice", Vector2(0.0, 1.0),
		[Vector2(-5.5, -0.8), Vector2(-8.3, -1.0), Vector2(-10.5, -3.0), Vector2(-11.0, -5.0)], true, 1500, true)
	out["ice_to_door_and_down_the_steps"] = await _walk_route("ice_to_door", Vector2(-11.0, -5.0),
		[Vector2(-4.6, -1.0), Vector2(-1.0, 3.5), Vector2(0.0, 6.9), Vector2(0.0, 7.7), Vector2(0.0, 8.8)],
		true, 2400, true)
	out["refused_up_the_mound"] = await _walk_route("up_the_mound", Vector2(3.0, 6.6),
		[Vector2(3.0, 11.0)], false, 480, false)
	out["refused_out_east"] = await _walk_route("out_east", Vector2(10.0, 1.0),
		[Vector2(23.0, 1.0)], true, 600, false)
	out["refused_out_bottom_right"] = await _walk_route("out_bottom_right", Vector2(4.0, -12.0),
		[Vector2(4.0, -19.0)], false, 600, false)
	out["refused_off_the_ice_west"] = await _walk_route("off_ice_west", Vector2(-14.0, -5.0),
		[Vector2(-23.0, -5.0)], false, 700, false)
	out["refused_out_the_entry"] = await _walk_route("out_the_entry", Vector2(-3.0, -14.0),
		[Vector2(-3.6, -19.0)], false, 480, false)
	out["_instrument"] = "knight.drive_dir each physics frame toward the next waypoint (run on legs over 2.5 m), his physics_process off, move_and_slide on the real colliders; reached = within 0.3 m of the last waypoint"
	return out


func _guide_geometry(mk: Dictionary) -> Dictionary:
	"""Where the guide window's corners and the markers' ends land, by the camera's own
	projection -- the numeric half of the scale check (finalize.py measures the pixels)."""
	var cam: Camera3D = scene.cam
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var corners := {}
	for c in [["top_left", -1.0, 1.0], ["top_right", 1.0, 1.0], ["bottom_left", -1.0, -1.0], ["bottom_right", 1.0, -1.0]]:
		var p: Vector3 = scene.uv_to_world(float(c[1]) * float(gw["u"][1]), float(c[2]) * float(gw["v"][1]))
		var s := cam.unproject_position(p)
		corners[c[0]] = [snappedf(s.x, 0.01), snappedf(s.y, 0.01)]
	var marks := {}
	for kname in mk:
		var a: Array = mk[kname]["from_uv"]
		var b: Array = mk[kname]["to_uv"]
		var pa := cam.unproject_position(scene.uv_to_world(float(a[0]), float(a[1]), 0.004))
		var pb := cam.unproject_position(scene.uv_to_world(float(b[0]), float(b[1]), 0.004))
		marks[kname] = mk[kname].duplicate()
		marks[kname]["projected_px"] = [[snappedf(pa.x, 0.01), snappedf(pa.y, 0.01)], [snappedf(pb.x, 0.01), snappedf(pb.y, 0.01)]]
		marks[kname]["projected_length_px"] = snappedf(pa.distance_to(pb), 0.001)
	return {"px": [GUIDE.x, GUIDE.y], "camera_ortho_size_m": snappedf(cam.size, 0.0001),
		"window_corners_projected_px": corners,
		"_corners_expect": "top_left (0,0), top_right (4096,0), bottom_left (0,2560), bottom_right (4096,2560) to within ~0.1 px",
		"markers": marks}


func _rect(r: Rect2) -> Array:
	return [snappedf(r.position.x, 0.1), snappedf(r.position.y, 0.1), snappedf(r.size.x, 0.1), snappedf(r.size.y, 0.1)]


func _time_frames(n: int, res: Vector2i) -> Dictionary:
	"""barrow_world's instrument: vsync off, frames as fast as the engine will, wall time over
	frames, and the loop does NOT await physics_frame (that gates it at the physics rate)."""
	var k = scene.knight
	var prev := vp.size
	vp.size = res
	scene.unpark_camera()
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	var loop := [Vector2(4.0, 1.0), Vector2(0.0, 5.0), Vector2(-4.0, 1.0), Vector2(0.0, -3.0)]
	var wi := 0
	for i in 40:
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, DT)
		await process_frame
	var t0 := Time.get_ticks_usec()
	for i in n:
		if scene.knight_uv().distance_to(loop[wi]) < 0.6:
			wi = (wi + 1) % loop.size()
		k.drive_dir(scene.canvas_dir_uv(scene.knight_uv(), loop[wi]), false, DT)
		await process_frame
	var ms: float = float(Time.get_ticks_usec() - t0) / 1000.0 / float(n)
	vp.size = prev
	return {"ms_per_frame": snappedf(ms, 0.01), "fps": snappedf(1000.0 / maxf(ms, 1e-3), 0.1),
			"frames": n, "render_px": [res.x, res.y]}


func _settle() -> void:
	for i in 8:
		await physics_frame
		await process_frame
	RenderingServer.force_draw()
	await process_frame


func _shot(nm: String) -> void:
	for i in 3:
		await process_frame
	var img: Image = vp.get_texture().get_image()
	# THE SIZE IS CHECKED, because the first run shipped a 1920x1080 "guide": _shot was called
	# without await, so every still was read three frames late, after the NEXT step had resized
	# the viewport (and the calibration frame after its markers were freed).
	if img.get_width() != vp.size.x or img.get_height() != vp.size.y:
		print("[capture] SIZE MISMATCH %s: image %dx%d, viewport %dx%d" % [nm, img.get_width(), img.get_height(), vp.size.x, vp.size.y])
	img.save_png("%s/%s.png" % [out_dir, nm])
	print("[capture] %s.png  %dx%d" % [nm, img.get_width(), img.get_height()])


func _write(nm: String, d: Dictionary) -> void:
	var f := FileAccess.open("%s/%s" % [out_dir, nm], FileAccess.WRITE)
	f.store_string(JSON.stringify(d, " "))
	f.close()
