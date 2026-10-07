extends SceneTree
## C-9 T10-2 step 1 (spec v2): capture and MEASURE the Barrow blockout.
##
##   Godot --path godot --resolution 640x360 --script tools/capture_blockout.gd -- --out DIR
##         [--no-walks] [--no-cost] [--atlas 8192] [--painted]
##
## --painted (T10-2 step 4): the same scene dressed in the painting (barrow_full.gd `painted`) --
## every instrument unchanged, so tools/accept_painted.py can hold its numbers to the blockout's.
##
## Windowed, not headless: every still is read back from a SubViewport, which needs a Metal
## surface. The OS window is small on purpose -- nothing it draws is kept.
##
## Writes into --out:
##   built.json            every placement as BUILT, and every collider's ground footprint
##   walk_grid.json        the 0.1 m free-space grid and the flood fill from the entry
##   capture_report.json   the measurements: flood fill, door floor, the walks, the door's
##                         visibility, the crucible's lines of sight, the frame cost, the guide's
##                         projected corners and markers
##   guide_calibration.png 5376 x 3328 with the 1 m / 2 m markers (the instrument check)
##   guide.png             5376 x 3328, the paint-over guide (no crucible marks)
##   still_ring.png, still_tarn.png     1920 x 1080 play-screen stills
##   still_crucible.png    2400 x 1500 at the play camera's scale, every crucible mark visible
##   still_door.png        1920 x 1080, him on the centre line where the door first shows whole
##   topdown.png           the map's base render, straight down, 40 px/m

var GUIDE := Vector2i(5376, 3328)        # BV2F Tier-B: was const; --frame-grid guide_px
var SCENE := "res://scenes/barrow_full.tscn"   # BV2F Tier-B: --frame-grid scene
const PLAY := Vector2i(1920, 1080)
const CRUCIBLE_SHOT := Vector2i(2400, 1500)
var TOP_PX_PER_M := 40.0                 # BV2F Tier-B: was const; --frame-grid topdown.px_per_m
var TOP := Vector2i(2296, 1816)          # BV2F Tier-B: was const; --frame-grid topdown.px
const DT := 1.0 / 60.0
const TERRAIN_BIT := 1 << 1
var GRID_STEP := 0.1                     # BV2F Tier-B: was const; --frame-grid walk_grid.step
var GRID_U := Vector2(-21.0, 18.0)       # BV2F Tier-B: was const; --frame-grid walk_grid.u
var GRID_V := Vector2(-19.0, 12.0)       # BV2F Tier-B: was const; --frame-grid walk_grid.v

var out_dir := ""
var do_walks := true
var do_cost := true
var atlas := 8192
var painted := false                # T10-2 step 4: the SAME instruments on the painted Barrow
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
		if args[i] == "--painted":
			painted = true
		if args[i] == "--frame-grid" and i + 1 < args.size():   # BV2F Tier-B
			_bv2f_frame_grid(args[i + 1])
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
	scene = load(SCENE).instantiate()   # BV2F Tier-B: was the literal res://scenes/barrow_full.tscn
	scene.painted = painted
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

	# ---- 1. what was built, and every collider's footprint -----------------------------
	var t0 := Time.get_ticks_msec()
	var recs: Dictionary = scene.build_records()
	var cfp: Array = scene.collider_footprints()
	_write("built.json", {"records": recs, "collider_footprints": cfp, "scene_report": scene.report,
		"_": "BUILT numbers, measured off the scene; finalize.py merges them into barrow_full_layout.json"})
	rep["records_ms"] = Time.get_ticks_msec() - t0
	print("[capture] records: %d pieces, %d collider footprints" % [recs.size(), cfp.size()])

	# ---- 2. walkability, the door's floor, the crucible's lines of sight -----------------
	vp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	rep["walk_grid"] = await _walk_grid()
	rep["door_floor"] = await _door_floor()
	rep["crucible_los"] = await _crucible_los()
	print("[capture] walk grid: %s" % JSON.stringify(rep["walk_grid"]["summary"]))

	# ---- 3. he walks it -----------------------------------------------------------------------
	var k = scene.knight
	if do_walks:
		rep["walks"] = await _walks()
		print("[capture] walks done")
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS

	# ---- 4. the guide: the 4 x 4 window, 5376 x 3328, centred at (-2, -3) -------------------
	k.set_physics_process(false)
	scene.set_hud_visible(false)
	scene.set_overlay(false)
	scene.set_crucible_visible(false)
	var gk: Array = scene.layout["knight"]["guide_uv"]
	scene.place_knight(float(gk[0]), float(gk[1]), String(scene.layout["knight"].get("guide_facing", "S")))
	for i in 10:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	var prev_atlas := int(ProjectSettings.get_setting("rendering/lights_and_shadows/directional_shadow/size", 4096))
	RenderingServer.directional_shadow_atlas_set_size(atlas, true)
	vp.size = GUIDE
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var gc: Array = gw["centre_uv"]
	var guide_aim: Vector3 = scene.uv_to_world(float(gc[0]), float(gc[1]))
	scene.park_camera(guide_aim, 1.0)
	var mk: Dictionary = scene.set_markers(true)
	await _settle()
	rep["guide"] = _guide_geometry(mk)
	rep["guide"]["shadow_atlas_px"] = atlas
	rep["guide"]["him_screen_rect_px"] = _rect(scene.character_screen_rect())
	await _shot("guide_calibration")
	scene.set_markers(false)
	await _settle()
	await _shot("guide")

	# ---- 5. the door: seen whole, covered, and from where ---------------------------------
	rep["door_visibility"] = await _door_visibility(guide_aim)
	RenderingServer.directional_shadow_atlas_set_size(prev_atlas, true)

	# ---- 6. play-screen stills -----------------------------------------------------------------
	vp.size = PLAY
	for spec in [["still_ring", Vector2(0.0, 1.0), "NE"], ["still_tarn", Vector2(-11.5, -4.5), "W"]]:
		await _still_at(spec[0], spec[1], spec[2])
	var vfull: float = float(rep["door_visibility"].get("first_v_door_whole_in_frame", 6.0))
	await _still_at("still_door", Vector2(0.0, vfull), "N")
	# the crucible, every mark in frame, at the play camera's own scale on a bigger canvas
	scene.set_crucible_visible(true)
	scene.freeze_pose(false)
	scene.place_knight(0.0, 1.0, "S")
	for i in 10:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	vp.size = CRUCIBLE_SHOT
	scene.park_camera(scene.uv_to_world(-2.4, 1.3), 1.0)
	await _settle()
	rep["still_crucible"] = {"px": [CRUCIBLE_SHOT.x, CRUCIBLE_SHOT.y], "centre_uv": [-2.4, 1.3],
		"scale": "the play camera's own (100.6 px/m across)", "marks_projected_px": _crucible_px()}
	await _shot("still_crucible")
	scene.set_crucible_visible(false)

	# ---- 7. the map's base: straight down, +u right, +v up, 40 px/m, shadows off ---------------
	vp.size = TOP
	var sun: DirectionalLight3D = scene.sun
	sun.shadow_enabled = false
	scene.place_knight(float(gk[0]), float(gk[1]), "S")
	scene.set_topdown(Vector2(float(gc[0]), float(gc[1])), float(TOP.y) / TOP_PX_PER_M)
	await _settle()
	rep["topdown"] = {"px": [TOP.x, TOP.y], "px_per_m": TOP_PX_PER_M, "centre_uv": [float(gc[0]), float(gc[1])],
					  "u": [float(gc[0]) - float(TOP.x) * 0.5 / TOP_PX_PER_M, float(gc[0]) + float(TOP.x) * 0.5 / TOP_PX_PER_M],
					  "v": [float(gc[1]) - float(TOP.y) * 0.5 / TOP_PX_PER_M, float(gc[1]) + float(TOP.y) * 0.5 / TOP_PX_PER_M],
					  "shadows": "off -- a plan, not a view"}
	await _shot("topdown")
	sun.shadow_enabled = true

	# ---- 8. frame cost at 1080p, him walking, vsync off; checked at 2.25x the pixels ----------
	if do_cost:
		vp.size = PLAY
		scene.freeze_pose(false)
		scene.unpark_camera()
		scene.set_crucible_visible(true)
		scene.place_knight(0.0, -3.0, "N")
		await _settle()
		rep["frame_cost_ms"] = {
			"_at": "SubViewport, MSAA 4x, Apple M2 8 GB, vsync off, him walking a loop in the ring with the full kit, crucible marks on",
			"play_1920x1080": await _time_frames(240, PLAY),
			"instrument_check_2880x1620": await _time_frames(160, Vector2i(2880, 1620)),
		}
		print("[capture] frame cost: %s" % JSON.stringify(rep["frame_cost_ms"]))
	_write("capture_report.json", rep)
	print("[capture] -> %s" % out_dir)
	quit(0)


func _still_at(nm: String, at: Vector2, facing: String) -> void:
	var k = scene.knight
	scene.freeze_pose(false)
	scene.place_knight(at.x, at.y, facing)
	for i in 10:
		k.drive_dir(Vector2.ZERO, false, DT)
		await physics_frame
	scene.freeze_pose(true)
	scene.park_camera(scene._camera_aim(), 1.0)
	await _settle()
	rep[nm] = {"him_uv": [at.x, at.y], "facing": facing, "camera_clamped": scene.clamp_on,
		"him_screen_rect_px": _rect(scene.character_screen_rect())}
	await _shot(nm)


# --- measurements ------------------------------------------------------------------------
func _walk_grid() -> Dictionary:
	"""FREE SPACE FOR HIM, by the physics server: at every 0.1 m cell, does a vertical cylinder of
	his capsule's radius (0.35 m), 1.8 m tall and lifted 5 cm off the floor, touch anything on the
	terrain layer? Then a 4-connected flood fill from the entry."""
	await physics_frame
	var space: PhysicsDirectSpaceState3D = (scene as Node3D).get_world_3d().direct_space_state
	var cyl := CylinderShape3D.new()
	cyl.radius = 0.35
	cyl.height = 1.8
	var q := PhysicsShapeQueryParameters3D.new()
	q.shape = cyl
	q.collision_mask = TERRAIN_BIT
	var nu := int(round((GRID_U.y - GRID_U.x) / GRID_STEP)) + 1
	var nv := int(round((GRID_V.y - GRID_V.x) / GRID_STEP)) + 1
	var free := PackedByteArray()
	free.resize(nu * nv)
	var t0 := Time.get_ticks_msec()
	for j in nv:
		for i in nu:
			var u := GRID_U.x + float(i) * GRID_STEP
			var v := GRID_V.x + float(j) * GRID_STEP
			q.transform = Transform3D(Basis(), scene.uv_to_world(u, v, 0.05 + 0.9))
			free[j * nu + i] = 1 if space.intersect_shape(q, 1).is_empty() else 0
	var t_q := Time.get_ticks_msec() - t0
	var L: Dictionary = scene.layout
	var sp: Array = L["knight"]["spawn_uv"]
	var si := int(round((float(sp[0]) - GRID_U.x) / GRID_STEP))
	var sj := int(round((float(sp[1]) - GRID_V.x) / GRID_STEP))
	var seen := PackedByteArray()
	seen.resize(nu * nv)
	var queue := []
	if free[sj * nu + si] == 1:
		seen[sj * nu + si] = 1
		queue.append(sj * nu + si)
	var head := 0
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
	var poly := PackedVector2Array()
	for p in L["bounds"]["polygon_uv"]:
		poly.append(Vector2(float(p[0]), float(p[1])))
	var R: Dictionary = L["regions"]
	var ic: Array = R["ice"]["centre_uv"]
	var ia := float(R["ice"]["axes_m"][0]) * 0.5
	var ib := float(R["ice"]["axes_m"][1]) * 0.5
	var m: Dictionary = scene._mound_spec()
	var mc := Vector2(float(m["uv"][0]), float(m["uv"][1]))
	var ma := float(m["semi_axes"][0])
	var mb := float(m["semi_axes"][1])
	var cu: Dictionary = m["cutting"]
	var reach := 0
	var leak_n := 0
	var leak := []
	var ice_free := 0
	var ice_reach := 0
	var mound_reach := 0
	var mound_list := []
	var ext := {"u_min": INF, "u_max": -INF, "v_min": INF, "v_max": -INF}
	var rows := []
	for j in nv:
		var row := ""
		for i in nu:
			var c := j * nu + i
			var u := GRID_U.x + float(i) * GRID_STEP
			var v := GRID_V.x + float(j) * GRID_STEP
			var ch := "#"
			if free[c] == 1:
				ch = "."
			if seen[c] == 1:
				ch = "o"
				reach += 1
				ext["u_min"] = minf(ext["u_min"], u)
				ext["u_max"] = maxf(ext["u_max"], u)
				ext["v_min"] = minf(ext["v_min"], v)
				ext["v_max"] = maxf(ext["v_max"], v)
				if not Geometry2D.is_point_in_polygon(Vector2(u, v), poly):
					leak_n += 1
					if leak.size() < 12:
						leak.append([u, v])
				var in_cut: bool = absf(u) < float(cu["half_w"]) and v < float(cu["v_facade"])
				if pow((u - mc.x) / ma, 2.0) + pow((v - mc.y) / mb, 2.0) < 1.0 and not in_cut:
					mound_reach += 1
					if mound_list.size() < 12:
						mound_list.append([u, v])
			if pow((u - float(ic[0])) / ia, 2.0) + pow((v - float(ic[1])) / ib, 2.0) <= 1.0 and free[c] == 1:
				ice_free += 1
				if seen[c] == 1:
					ice_reach += 1
			row += ch
		rows.append(row)
	var at := func(u: float, v: float) -> bool:
		var i := int(round((u - GRID_U.x) / GRID_STEP))
		var j := int(round((v - GRID_V.x) / GRID_STEP))
		return i >= 0 and j >= 0 and i < nu and j < nv and seen[j * nu + i] == 1
	var targets := {
		"arena_centre_(0,1)": at.call(0.0, 1.0),
		"ice_centre_(-13.5,-5)": at.call(-13.5, -5.0),
		"cutting_mouth_(0,8.6)": at.call(0.0, 8.6),
		"at_the_door_(0,10.1)": at.call(0.0, 10.1),
	}
	var summary := {"cells": nu * nv, "cell_m": GRID_STEP, "free_cells": _count(free), "reachable_cells": reach,
		"reachable_m2": snappedf(float(reach) * GRID_STEP * GRID_STEP, 0.1), "targets": targets,
		"ice_free_cells": ice_free, "ice_reachable_cells": ice_reach,
		"ice_reachable_share": snappedf(float(ice_reach) / maxf(float(ice_free), 1.0), 0.0001),
		"reachable_outside_bounds": leak_n, "reachable_inside_mound_outside_cutting": mound_reach,
		"reachable_extent_uv": ext, "query_ms": t_q}
	_write("walk_grid.json", {"u0": GRID_U.x, "v0": GRID_V.x, "step": GRID_STEP, "nu": nu, "nv": nv,
		"legend": {"#": "blocked (his capsule touches something)", ".": "free, NOT reachable from the entry", "o": "reachable from the entry"},
		"rows_from_v0_up": rows, "spawn_uv": sp})
	return {"summary": summary, "leak_samples_uv": leak, "mound_samples_uv": mound_list,
		"instrument": "PhysicsDirectSpaceState3D.intersect_shape, a CylinderShape3D r 0.35 h 1.8, bottom 5 cm off the floor, mask TERRAIN_BIT, every 0.1 m; 4-connected flood fill from spawn_uv"}


func _count(a: PackedByteArray) -> int:
	var n := 0
	for x in a:
		n += int(x)
	return n


func _door_floor() -> Dictionary:
	"""Straight down in the cutting and at the door: where does a ray find the floor? From 1.5 m,
	under the lintel (1.99 m)."""
	await physics_frame
	var space: PhysicsDirectSpaceState3D = (scene as Node3D).get_world_3d().direct_space_state
	var out := {}
	for v in [8.7, 9.2, 9.7, 10.0, 10.2, 10.4]:
		var a: Vector3 = scene.uv_to_world(0.0, v, 1.5)
		var b: Vector3 = scene.uv_to_world(0.0, v, -3.0)
		var hit := space.intersect_ray(PhysicsRayQueryParameters3D.create(a, b, TERRAIN_BIT))
		out["v=%.1f" % v] = snappedf(float(hit["position"].y), 0.0001) if not hit.is_empty() else null
	return {"floor_y_by_v_at_u0": out, "instrument": "intersect_ray from y 1.5 to -3.0, mask TERRAIN_BIT"}


func _crucible_los() -> Dictionary:
	"""EACH SPAWN'S LINE OF SIGHT TO THE STATION at his eye height (1.70 m): one ray, spawn to
	station, against every collider on the terrain layer. Blocked means a collider stands in it;
	the report names which one."""
	await physics_frame
	var space: PhysicsDirectSpaceState3D = (scene as Node3D).get_world_3d().direct_space_state
	var cr: Dictionary = scene.layout["crucible"]
	var eye := float(cr["eye_height_m"])
	var st: Array = cr["station"]["uv"]
	var b: Vector3 = scene.uv_to_world(float(st[0]), float(st[1]), eye)
	var out := {}
	for s in cr["spawns"]:
		var a: Vector3 = scene.uv_to_world(float(s["uv"][0]), float(s["uv"][1]), eye)
		var hit := space.intersect_ray(PhysicsRayQueryParameters3D.create(a, b, TERRAIN_BIT))
		var who := ""
		if not hit.is_empty():
			who = scene._group_of(hit["collider"])
		out[String(s["id"])] = {"clear": hit.is_empty(), "blocked_by": who,
			"hit_uv": ([snappedf(scene.world_to_uv(hit["position"]).x, 0.01), snappedf(scene.world_to_uv(hit["position"]).y, 0.01)] if not hit.is_empty() else null)}
	return {"eye_height_m": eye, "by_spawn": out, "instrument": "intersect_ray spawn -> station at eye height, mask TERRAIN_BIT"}


func _door_rect() -> Rect2i:
	"""Where the door frame can be on screen: its pieces' world bounds projected, with a margin.
	Counting magenta only inside it gives the same count as the whole frame (nothing else is
	magenta) at a fraction of the cost -- a GDScript loop over 17.9 M pixels is minutes."""
	var cam: Camera3D = scene.cam
	var lo := Vector2(INF, INF)
	var hi := Vector2(-INF, -INF)
	for id in ["door_lintel", "door_post_L", "door_post_R"]:
		for p in scene.world_verts(scene.nodes[id]):
			var s := cam.unproject_position(p)
			lo = lo.min(s)
			hi = hi.max(s)
	var r := Rect2i(int(floor(lo.x)) - 8, int(floor(lo.y)) - 8, int(ceil(hi.x - lo.x)) + 16, int(ceil(hi.y - lo.y)) + 16)
	return r.intersection(Rect2i(0, 0, vp.size.x, vp.size.y))


func _mask_px() -> int:
	await _settle()
	var r := _door_rect()
	if r.size.x <= 0 or r.size.y <= 0:
		return 0
	var img: Image = vp.get_texture().get_image().get_region(r)
	img.convert(Image.FORMAT_RGBA8)
	var data := img.get_data()
	var n := 0
	for i in range(0, data.size(), 4):
		if data[i] > 220 and data[i + 1] < 40 and data[i + 2] > 220:
			n += 1
	return n


func _door_visibility(guide_aim: Vector3) -> Dictionary:
	"""THE DOOR, BY ITS OWN PIXELS. The door frame's camera-facing surfaces render pure magenta
	(scene.set_door_mask) and the magenta pixels are counted:
	  * in the guide's view with everything drawn, against the same view with the door ALONE --
	    the share not hidden by the mound, the cutting or anything else;
	  * in the PLAY frame, the camera centred on him at the arena centre, against a play frame
	    centred on the door -- the share of the door's face that frame shows;
	  * stepping him up the centre line, the first place from which the whole face is in frame."""
	var out := {}
	vp.size = GUIDE
	scene.park_camera(guide_aim, 1.0)
	scene.set_door_mask("mask")
	var n_all: int = await _mask_px()
	scene.set_door_mask("alone")
	var n_alone: int = await _mask_px()
	scene.set_door_mask("off")
	scene.set_door_mask("mask")
	out["guide_view"] = {"door_face_px_everything_drawn": n_all, "door_face_px_door_alone": n_alone,
		"unoccluded_share": snappedf(float(n_all) / maxf(float(n_alone), 1.0), 0.0001)}
	vp.size = PLAY
	var door_c: Vector3 = scene.uv_to_world(0.0, 10.3, 1.6)
	scene.park_camera(door_c, 1.0)
	var n_door: int = await _mask_px()
	var k = scene.knight
	var scan := []
	var first_whole := -1.0
	var first_half := -1.0
	var v := 1.0
	while v <= 10.05:
		scene.place_knight(0.0, v, "N")
		scene.park_camera(scene.aim_for(k.global_position), 1.0)
		var n: int = await _mask_px()
		var share := float(n) / maxf(float(n_door), 1.0)
		scan.append([snappedf(v, 0.01), snappedf(share, 0.0001)])
		if first_half < 0.0 and share >= 0.5:
			first_half = v
		if first_whole < 0.0 and share >= 0.99:
			first_whole = v
		v += 0.25
	scene.set_door_mask("off")
	var at_centre: float = float(scan[0][1])
	out["play_frame"] = {"door_face_px_frame_centred_on_the_door": n_door,
		"share_in_frame_him_at_the_arena_centre": at_centre,
		"first_v_half_in_frame": first_half, "first_v_door_whole_in_frame": first_whole,
		"scan_v_share": scan,
		"_why_zero_at_the_centre": "the play frame reaches 595 px (7.41 m of ground) up-screen from his feet; from (0, 1) that is v 8.41, and the door stands at v 10.3-10.6 behind the arena's own r 7 edge (v 8.0)"}
	out["first_v_door_whole_in_frame"] = first_whole
	out["instrument"] = "magenta pixel counts (R>220, G<40, B>220) of the door frame's -v-facing surfaces, unlit, the pen off; MSAA 4x"
	return out


func _crucible_px() -> Dictionary:
	var cam: Camera3D = scene.cam
	var cr: Dictionary = scene.layout["crucible"]
	var out := {}
	for s in cr["spawns"]:
		var c := Vector2(float(s["uv"][0]), float(s["uv"][1]))
		var lo := Vector2(INF, INF)
		var hi := Vector2(-INF, -INF)
		for kk in 16:
			var a := TAU * float(kk) / 16.0
			var p := cam.unproject_position(scene.uv_to_world(c.x + 1.5 * cos(a), c.y + 1.5 * sin(a), 0.012))
			lo = lo.min(p)
			hi = hi.max(p)
		out[String(s["id"])] = [snappedf(lo.x, 0.1), snappedf(lo.y, 0.1), snappedf(hi.x, 0.1), snappedf(hi.y, 0.1)]
	for nm in ["boss_gate", "station"]:
		var p2: Array = cr[nm]["uv"]
		var p := cam.unproject_position(scene.uv_to_world(float(p2[0]), float(p2[1]), 0.012))
		out[nm] = [snappedf(p.x, 0.1), snappedf(p.y, 0.1)]
	out["_all_inside"] = true
	for kk in out:
		if kk.begins_with("_"):
			continue
		var a: Array = out[kk]
		for idx in a.size():
			var lim: float = float(CRUCIBLE_SHOT.x) if idx % 2 == 0 else float(CRUCIBLE_SHOT.y)
			if float(a[idx]) < 0.0 or float(a[idx]) > lim:
				out["_all_inside"] = false
	return out


func _walk_route(start: Vector2, wps: Array, run: bool, max_frames: int, expect_reach: bool) -> Dictionary:
	var k = scene.knight
	scene.place_knight(start.x, start.y, "N")
	await physics_frame
	var wi := 0
	var frames := 0
	var track := []
	while wi < wps.size() and frames < max_frames:
		var pos: Vector2 = scene.knight_uv()
		var tgt: Vector2 = wps[wi]
		var last := wi == wps.size() - 1
		if pos.distance_to(tgt) < (0.3 if last else 0.7):
			wi += 1
			continue
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
	out["entry_to_arena"] = await _walk_route(S,
		[Vector2(-2.3, -11.0), Vector2(-0.6, -8.0), Vector2(0.0, -6.2), Vector2(0.0, 1.0)], true, 1500, true)
	# out through the ring's west gap, between the -95 (fallen) and -115 stones
	out["arena_to_ice"] = await _walk_route(Vector2(0.0, 1.0),
		[Vector2(-5.5, -0.4), Vector2(-8.6, -0.3), Vector2(-10.5, -2.5), Vector2(-12.0, -5.0)], true, 1500, true)
	out["ice_to_the_door"] = await _walk_route(Vector2(-12.0, -5.0),
		[Vector2(-10.5, -2.5), Vector2(-8.6, -0.3), Vector2(-4.0, 2.0), Vector2(0.0, 6.5), Vector2(0.0, 9.3), Vector2(0.0, 10.1)],
		true, 2400, true)
	out["refused_into_the_passage"] = await _walk_route(Vector2(0.0, 9.3), [Vector2(0.0, 12.0)], false, 420, false)
	out["refused_up_the_mound"] = await _walk_route(Vector2(3.2, 8.0), [Vector2(3.2, 12.5)], false, 480, false)
	out["refused_out_east"] = await _walk_route(Vector2(10.0, 1.0), [Vector2(23.0, 1.0)], true, 600, false)
	out["refused_out_north_east"] = await _walk_route(Vector2(10.5, 7.5), [Vector2(10.5, 14.0)], false, 600, false)
	out["refused_out_north_west"] = await _walk_route(Vector2(-12.5, 7.5), [Vector2(-12.5, 14.0)], false, 600, false)
	out["refused_out_bottom_right"] = await _walk_route(Vector2(4.0, -12.0), [Vector2(4.0, -20.0)], false, 700, false)
	out["refused_off_the_ice_west"] = await _walk_route(Vector2(-15.0, -5.0), [Vector2(-25.0, -5.0)], false, 700, false)
	out["refused_out_the_entry"] = await _walk_route(Vector2(-3.0, -14.0), [Vector2(-3.6, -20.0)], false, 480, false)
	out["_instrument"] = "knight.drive_dir each physics frame toward the next waypoint (run on legs over 2.5 m), his physics_process off, move_and_slide on the real colliders; reached = within 0.3 m of the last waypoint"
	return out


func _guide_geometry(mk: Dictionary) -> Dictionary:
	var cam: Camera3D = scene.cam
	var gw: Dictionary = scene.layout["frame"]["guide_window"]
	var corners := {}
	for c in [["top_left", 0, 1], ["top_right", 1, 1], ["bottom_left", 0, 0], ["bottom_right", 1, 0]]:
		var p: Vector3 = scene.uv_to_world(float(gw["u"][int(c[1])]), float(gw["v"][int(c[2])]))
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
		"_corners_expect": "top_left (0,0), top_right (5376,0), bottom_left (0,3328), bottom_right (5376,3328) to within ~0.1 px",
		"markers": marks}


func _rect(r: Rect2) -> Array:
	return [snappedf(r.position.x, 0.1), snappedf(r.position.y, 0.1), snappedf(r.size.x, 0.1), snappedf(r.size.y, 0.1)]


func _time_frames(n: int, res: Vector2i) -> Dictionary:
	"""Wall-clock throughput with vsync off; the loop does NOT await physics_frame (that gates it
	at the physics rate). Checked by running it at 2.25x the pixels."""
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
	# THE SIZE IS CHECKED: v1's first run shipped a 1920x1080 "guide" because a still was read
	# after the next step had resized the viewport.
	if img.get_width() != vp.size.x or img.get_height() != vp.size.y:
		print("[capture] SIZE MISMATCH %s: image %dx%d, viewport %dx%d" % [nm, img.get_width(), img.get_height(), vp.size.x, vp.size.y])
	img.save_png("%s/%s.png" % [out_dir, nm])
	print("[capture] %s.png  %dx%d" % [nm, img.get_width(), img.get_height()])


func _write(nm: String, d: Dictionary) -> void:
	var f := FileAccess.open("%s/%s" % [out_dir, nm], FileAccess.WRITE)
	f.store_string(JSON.stringify(d, " "))
	f.close()


# ---- BV2F Tier-B patch (fid/v1tools/ALLOWLIST.md): frame/grid/scene from --frame-grid JSON; ----
# ---- with no --frame-grid every value is v1's own, so v1's behaviour is unchanged.            ----
func _bv2f_frame_grid(p: String) -> void:
	var fg = JSON.parse_string(FileAccess.get_file_as_string(p))
	if typeof(fg) != TYPE_DICTIONARY:
		push_error("[bv2f] cannot read --frame-grid %s" % p)
		quit(5)
		return
	if fg.has("guide_px"):
		GUIDE = Vector2i(int(fg["guide_px"][0]), int(fg["guide_px"][1]))
	if fg.has("scene"):
		SCENE = String(fg["scene"])
	if fg.has("topdown"):
		TOP = Vector2i(int(fg["topdown"]["px"][0]), int(fg["topdown"]["px"][1]))
		TOP_PX_PER_M = float(fg["topdown"]["px_per_m"])
	if fg.has("walk_grid"):
		GRID_U = Vector2(float(fg["walk_grid"]["u"][0]), float(fg["walk_grid"]["u"][1]))
		GRID_V = Vector2(float(fg["walk_grid"]["v"][0]), float(fg["walk_grid"]["v"][1]))
		GRID_STEP = float(fg["walk_grid"]["step"])
	print("[bv2f] frame-grid %s: guide %dx%d scene %s" % [p, GUIDE.x, GUIDE.y, SCENE])
