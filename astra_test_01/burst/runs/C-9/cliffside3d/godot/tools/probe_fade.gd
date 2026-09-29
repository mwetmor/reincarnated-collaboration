extends SceneTree
# C-9 R-C9-70: does the occluder fade give the character back, and does it leave alone the
# props he stands in FRONT of?
#
# Counted the same way the occlusion was, and at FULL RESOLUTION on purpose: the fade is a
# per-screen-pixel discard, so counting it on a downscaled frame samples a fixed sub-
# lattice of the dither and measures the lattice rather than the fade.
#
#   A  card hidden, body on     B  card hidden, body off   -> silhouette is A != B
#   C  card on,     body on     D  card on,     body off   -> hidden is C == D
#
# run twice per step, fade off and fade on, so the pair is like for like.
#
#   Godot --path godot --resolution 1920x1080 --script tools/probe_fade.gd -- [--out D]

const SHOT := Vector2i(1920, 1080)
const PPM := 100.617553710938
# the two paths the deliverable captures walk, verbatim from tools/capture.gd
const TREE := {"asset": "tree_living_a", "px": Vector2(1896.0139860139861, 2765.0),
			   "axis": "x", "from": -230.0, "to": 190.0, "at": -60.0,
			   "zoom": 1.5, "aim": Vector2(1896.0, 2640.0)}
const POST := {"asset": "bridge_post_1", "px": Vector2(2996.0, 1247.0),
			   "axis": "y", "steps": [200.0, 140.0, 90.0, 35.0, 0.0],
			   "zoom": 1.15}
# THE CONTROL THAT MATTERS. The post proves a prop without the flag never fades; it does
# not prove the DEPTH half of the rule, because he is never behind it. This walks straight
# up the same tree: down-screen he is farther (behind it, and it should fade), up-screen
# this slope puts him nearer (in front of it, and it must NOT fade) -- all while his box
# still overlaps the canopy, so the rect test cannot be what turns it off.
const CONTROL := {"asset": "tree_living_a", "px": Vector2(1896.0139860139861, 2765.0),
				  "axis": "y", "steps": [200.0, 120.0, 40.0, -40.0, -120.0, -200.0],
				  "zoom": 1.5, "aim": Vector2(1896.0, 2640.0)}
const COUNT_STEPS := [1, 5, 8]          # where the tree hides most of him

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://probe_fade")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED     # exact pixels: MSAA would blur the stipple
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	scene = load("res://scenes/cliffside3d.tscn").instantiate()
	root.add_child(scene)
	for i in 50:
		await process_frame
	cam = Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.keep_aspect = Camera3D.KEEP_HEIGHT
	cam.near = scene.cam.near
	cam.far = scene.cam.far
	cam.cull_mask = scene.cam.cull_mask
	vp.add_child(cam)
	cam.current = true

	var report := {}
	report["tree"] = await _walk(TREE, true)
	report["post"] = await _walk(POST, false)
	report["control_same_tree_up_and_down"] = await _walk(CONTROL, false)
	var f := FileAccess.open(out_dir + "/probe_fade.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	var g := FileAccess.open(out_dir + "/probe_fade.txt", FileAccess.WRITE)
	g.store_string("\n".join(lines) + "\n")
	g.close()
	print("[fade] -> ", out_dir)
	quit(0)


func _walk(spec: Dictionary, count_pixels: bool) -> Array:
	var k = scene.knight
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state
	var holder = scene.get_node_or_null(^"Props")
	var card: MeshInstance3D = null
	for c in holder.get_children():
		if (c as MeshInstance3D).name == String(spec["asset"]):
			card = c
	var anchor: Vector2 = spec["px"]
	var offsets := []
	if spec.has("steps"):
		for s in spec["steps"]:
			offsets.append(Vector2(0.0, float(s)))
	else:
		for i in 9:
			var u: float = float(spec["from"]) + (float(spec["to"]) - float(spec["from"])) \
				* float(i) / 8.0
			offsets.append(Vector2(u, float(spec["at"])))
	say("")
	say("== %s   (fade_when_behind = %s)" %
		[String(spec["asset"]), str(card.get_meta("fade_when_behind"))])
	say("   %-5s %-22s %6s %7s | %8s %8s %8s" %
		["step", "canvas_px", "fade", "depth", "sil_px", "hid_off", "hid_on"])
	var rows := []
	for i in offsets.size():
		var px: Vector2 = anchor + offsets[i]
		var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
		if g.is_empty():
			continue
		k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
		k.velocity = Vector3.ZERO
		k.facing = "E" if String(spec.get("axis", "y")) == "x" else "N"
		k.state = "walk"
		k.play("walk")
		k.visible = true
		var aim: Vector2 = spec["aim"] if spec.has("aim") else (anchor + px) * 0.5 + Vector2(0, -90)
		scene.look_at_canvas(aim, 0.0, float(spec["zoom"]))
		for j in 4:
			await physics_frame
			await process_frame
		scene.settle_fade()
		await process_frame
		var op: float = (card.material_override as ShaderMaterial).get_shader_parameter("fade")
		var kd: float = k.global_position.dot(scene.fwd)
		var y_feet: float = scene.character_box().position.y + scene.character_box().size.y
		var card_here: float = float(card.get_meta("d0")) + (float(card.get_meta("y0")) - y_feet) \
			* (Vector3.UP.dot(scene.fwd) / (100.617553710938 * 0.602462407085))
		var row := {"step": i, "canvas_px": [snappedf(px.x, 0.1), snappedf(px.y, 0.1)],
					"fade_opacity": snappedf(op, 0.001),
					"card_depth_at_his_feet_m": snappedf(card_here, 0.01),
					"overlaps": card.get_meta("rect_px").intersects(scene.character_box()),
					"he_is": "behind it" if card_here < kd else "in front of it",
					"knight_depth_m": snappedf(k.global_position.dot(scene.fwd), 0.01),
					"card_faded": op < 0.999}
		if count_pixels and i in COUNT_STEPS:
			var m := await _count(k, card)
			row.merge(m)
			say("   %-5d %-22s %6.3f %7.2f | %8d %8d %8d   %.1f%% -> %.1f%% of him visible" %
				[i, str(row["canvas_px"]), op, row["knight_depth_m"],
				 m["silhouette_px"], m["hidden_no_fade_px"], m["hidden_faded_px"],
				 m["visible_no_fade_pct"], m["visible_faded_pct"]])
		else:
			say("   %-5d %-22s %6.3f %7.2f |  card %7.2f  overlap %-5s  %-14s  %s" %
				[i, str(row["canvas_px"]), op, row["knight_depth_m"], card_here,
				 str(row["overlaps"]), String(row["he_is"]),
				 "FADED" if row["card_faded"] else "solid"])
		rows.append(row)
	return rows


func _count(k, card: MeshInstance3D) -> Dictionary:
	scene.set_fade_enabled(false)
	card.visible = false
	var A := await _grab()
	k.visible = false
	var B := await _grab()
	card.visible = true
	var Doff := await _grab()
	k.visible = true
	var Coff := await _grab()
	scene.set_fade_enabled(true)
	k.visible = false
	var Don := await _grab()
	k.visible = true
	var Con := await _grab()
	var sil := 0
	var hoff := 0
	var hon := 0
	for y in SHOT.y:
		for x in SHOT.x:
			if _ne(A.get_pixel(x, y), B.get_pixel(x, y)):
				sil += 1
				if not _ne(Coff.get_pixel(x, y), Doff.get_pixel(x, y)):
					hoff += 1
				if not _ne(Con.get_pixel(x, y), Don.get_pixel(x, y)):
					hon += 1
	var s := maxf(float(sil), 1.0)
	return {"silhouette_px": sil, "hidden_no_fade_px": hoff, "hidden_faded_px": hon,
			"visible_no_fade_pct": snappedf(100.0 * float(sil - hoff) / s, 0.1),
			"visible_faded_pct": snappedf(100.0 * float(sil - hon) / s, 0.1)}


func _ne(a: Color, b: Color) -> bool:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02


func _grab() -> Image:
	_mirror()
	for i in 3:
		await process_frame
	return vp.get_texture().get_image()


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))
