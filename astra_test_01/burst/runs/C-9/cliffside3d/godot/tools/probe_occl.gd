extends SceneTree
# C-9 T7-A: WHERE does a prop card actually hide the stand-in?
#
# The first sweep past tree_living_a came back "in front of the card" at every step, and
# the pictures agree. That is not a bug -- this hillside climbs toward the camera faster
# than a person is tall, so a walker on it is almost always nearer than a tree rooted
# beside him -- but it means the occlusion frame has to be FOUND rather than assumed.
#
# Measured by RENDERING, not by arithmetic about depths: four frames per sample
#   A knight on,  props off      B knight off, props off   -> the silhouette is A != B
#   C knight on,  props on       D knight off, props on    -> hidden is where C == D
# so "occluded" is the share of the stand-in's own pixels that a prop takes away. A depth
# comparison between a card's ORIGIN and a body's FEET is not the same question and gave
# the wrong answer once already.
#
#   Godot --path godot --resolution 640x360 --script tools/probe_occl.gd -- [--out D]

const SHOT := Vector2i(640, 360)
const PPM := 100.617553710938
const CANDIDATES := [
	["bridge_post_0", Vector2(3238.5, 1428.0)],
	["bridge_post_1", Vector2(2996.0, 1247.0)],
	["bridge_post_2", Vector2(3922.0, 836.0)],
	["bridge_post_3", Vector2(3680.0, 656.0)],
	["cache_crates_barrel", Vector2(2803.8, 2475.0)],
	["stump_b", Vector2(2182.2, 2769.0)],
]
# a grid around the anchor: down-screen / up-screen AND across, because the card is a
# PLANE and the across-axis is where a trunk can halve a body
const OFFSETS := [Vector2(0, 160), Vector2(0, 110), Vector2(0, 70), Vector2(0, 35),
				  Vector2(0, 0), Vector2(-30, 35), Vector2(30, 35), Vector2(-30, 70),
				  Vector2(30, 70), Vector2(-30, 110), Vector2(30, 110), Vector2(0, 200)]

var out_dir := ""
var scene
var vp: SubViewport
var cam: Camera3D
var props: Node3D
var lines: Array[String] = []


func say(s: String) -> void:
	print(s)
	lines.append(s)


func _initialize() -> void:
	out_dir = ProjectSettings.globalize_path("user://probe_occl")
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--out" and i + 1 < args.size():
			out_dir = args[i + 1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = SubViewport.new()
	vp.size = SHOT
	vp.own_world_3d = false
	vp.msaa_3d = Viewport.MSAA_DISABLED
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
	props = scene.get_node_or_null(^"Props")
	var k = scene.knight
	k.set_physics_process(false)      # no sliding: the sample must be where it is put
	var space: PhysicsDirectSpaceState3D = scene.get_world_3d().direct_space_state

	var best := {}
	say("%-22s %-14s %7s %7s %7s | %6s %6s %7s   %s" %
		["prop", "offset_px", "sil_px", "hid_px", "hid_%", "prop", "covrd", "covrd_%",
		 "knight/card depth (m)"])
	for c in CANDIDATES:
		var name: String = c[0]
		var anchor: Vector2 = c[1]
		var card: MeshInstance3D = null
		for ch in props.get_children():
			if (ch as MeshInstance3D).name == name:
				card = ch
				break
		for off in OFFSETS:
			var px: Vector2 = anchor + off
			var g := CliffWorld.ground_at(space, px, scene.right, scene.up, scene.fwd)
			if g.is_empty():
				continue
			k.global_position = (g["position"] as Vector3) + Vector3.UP * 0.02
			k.visible = true
			# FRAME BOTH, and frame them the same way every sample. The first run aimed at
			# the anchor at zoom 1.6 and the stand-in walked out of the picture: the
			# silhouette count fell from 19410 px to 797 and the "best" occlusion it then
			# reported -- 27.6% of 797 px -- was 27.6% of a body that was mostly off-frame.
			# A ratio whose denominator is the instrument's own cropping is not a
			# measurement of occlusion.
			scene.look_at_canvas((anchor + px) * 0.5 + Vector2(0, -90), 0.0, 1.15)
			_mirror()
			var toggle: Node3D = card if card != null else props
			toggle.visible = false
			var A := await _grab()
			k.visible = false
			var B := await _grab()
			toggle.visible = true
			var D := await _grab()
			k.visible = true
			var C := await _grab()
			var sil := 0
			var hid := 0
			var psil := 0
			var phid := 0
			for y in SHOT.y:
				for x in SHOT.x:
					var qa := A.get_pixel(x, y)
					var qb := B.get_pixel(x, y)
					var qc := C.get_pixel(x, y)
					var qd := D.get_pixel(x, y)
					if _ne(qa, qb):
						sil += 1
						if not _ne(qc, qd):
							hid += 1
					if _ne(qd, qb):
						psil += 1
						if not _ne(qc, qa):
							phid += 1
			var pct: float = 100.0 * float(hid) / maxf(float(sil), 1.0)
			var kd: float = k.global_position.dot(scene.fwd)
			var cd: float = card.global_position.dot(scene.fwd) if card != null else 0.0
			var ppct: float = 100.0 * float(phid) / maxf(float(psil), 1.0)
			say("%-22s %-14s %7d %7d %6.1f%% | %6d %6d %6.1f%%   %7.2f / %7.2f" %
				[name, str(off), sil, hid, pct, psil, phid, ppct, kd, cd])
			if sil > 6000 and psil > 300 and ppct > float(best.get("ppct", 0.0)):
				best = {"prop": name, "offset": [off.x, off.y], "ppct": ppct,
						"anchor": [anchor.x, anchor.y], "sil": sil, "props_hidden": phid}
	say("")
	say("BEST: %s" % JSON.stringify(best))
	var f := FileAccess.open(out_dir + "/probe_occl.txt", FileAccess.WRITE)
	f.store_string("\n".join(lines) + "\n")
	f.close()
	var j := FileAccess.open(out_dir + "/probe_occl.json", FileAccess.WRITE)
	j.store_string(JSON.stringify(best, " "))
	j.close()
	quit(0)


func _ne(a: Color, b: Color) -> bool:
	return absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.02


func _mirror() -> void:
	cam.global_transform = scene.cam.global_transform
	cam.size = float(SHOT.y) / PPM * (scene.cam.size / (float(scene._view_height()) / PPM))


func _grab() -> Image:
	for i in 3:
		await process_frame
	return vp.get_texture().get_image()
