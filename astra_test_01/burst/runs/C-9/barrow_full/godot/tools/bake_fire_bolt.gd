extends SceneTree
## C-9 (c) -- THE FIRE BALL BAKE: cliffside's fire_bolt_e1_B, rendered by ITS OWN RUNTIME, frame by frame,
## into the passes a flipbook needs. drax.
##
## Runs in a SCRATCH COPY of C-7's cliffside_v45 (the kit, its scripts and its renderer exactly as the
## live /playtest/cliffside/ plays them), never in C-7:
##   Godot --path <copy> --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --fixed-fps 60 --resolution 320x180 --script res://bake_fire_bolt.gd -- --out DIR --seed N [--impact-only]
##
## THE CAST, as keeper.gd makes it for kit B (painted_travel: no flare sprite): G1.acquire from the release
## socket, facing east, in the PROCESS step (where keeper.gd's frame_changed hook fires it), aimed as the
## touch policy aims (the forward point at range_px), with a caster whose feet are 100 px below the socket.
## The projectile is pre-placed in the pool with a fixed flame-dance seed; the global RNG is seeded, so the
## impact's interleave seed (effect_id ^ contact frame ^ randi()) is reproducible per --seed.
##
## ONE STATE, MANY PASSES, THE SAME FRAME. The kit's clocks are physics-frame counts, which advance whatever
## Engine.time_scale says -- so nothing is frozen and re-drawn. Instead every pass is its own SubViewport
## sharing the main one's World2D, choosing what it draws by canvas_cull_mask: each drawing item gets the
## ONE visibility bit of its (phase, blend) -- re-assigned every frame, before the draw -- and every
## container the bits of what it holds. Per phase:
##   S  = the phase, all its layers, over transparent black   -> the premultiplied colour, and its rect
##   M0 = its MIX layers only, over opaque black
##   M1 = its MIX layers only, over opaque white               -> A = 1 - (M1 - M0), the MIX coverage
## Phases: travel (the projectile: head, streak, their dark copies, core, halo, smear, flame-dance
## copies), puff and cast_floor (the cast pool), impact (the burst but its FloorLight), impact_floor,
## halo (keeper.gd's cast halo, 32 steps of its windup t). The trail motes are world-anchored: the port
## re-plays them from this log. Crops go to DIR as PNG; the log to DIR/bake_log.json.

const VP := Vector2i(1600, 900)
const SOCKET := Vector2(300.25, 450.5)
const FEET := Vector2(300.25, 550.5)
const HALO_AT := Vector2(1200.0, 200.0)
const KIT := "fire_bolt_e1_B"
const DANCE_SEED := 20260930
const PHASES := ["travel", "puff", "cast_floor", "impact", "impact_floor", "motes", "halo"]
const BIT_BG_BLACK := 20
const BIT_BG_WHITE := 21

var out_dir := ""
var gseed := 1
var impact_only := false
var vp: SubViewport
var world: Node2D
var actors: Node2D
var caster: Node2D
var kit: Dictionary
var bolt
var halo: Sprite2D
var passes := {}                 # "phase:S|M0|M1" -> SubViewport
var log_rows: Array = []
var shots := 0
var warnings: Array = []


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		var a := String(args[i])
		if a == "--out" and i + 1 < args.size():
			out_dir = String(args[i + 1])
		elif a == "--seed" and i + 1 < args.size():
			gseed = int(args[i + 1])
		elif a == "--impact-only":
			impact_only = true
	DirAccess.make_dir_recursive_absolute(out_dir)
	vp = _viewport(true, 0)
	root.add_child(vp)
	world = Node2D.new()
	world.name = "World"
	vp.add_child(world)
	for spec in [[BIT_BG_BLACK, Color(0, 0, 0, 1)], [BIT_BG_WHITE, Color(1, 1, 1, 1)]]:
		var r := Polygon2D.new()
		r.polygon = PackedVector2Array([Vector2.ZERO, Vector2(VP.x, 0), Vector2(VP), Vector2(0, VP.y)])
		r.color = spec[1]
		r.z_index = -4096
		r.visibility_layer = 1 << int(spec[0])
		world.add_child(r)
	actors = Node2D.new()
	actors.name = "Actors"
	actors.y_sort_enabled = true           # as cliffside's Actors
	world.add_child(actors)
	caster = Node2D.new()
	caster.name = "Caster"
	caster.position = FEET
	actors.add_child(caster)
	for pi in PHASES.size():
		var ph: String = PHASES[pi]
		var mix := 1 << (pi * 2)
		var add := 1 << (pi * 2 + 1)
		passes[ph + ":S"] = _viewport(true, mix | add)
		passes[ph + ":M0"] = _viewport(false, mix | (1 << BIT_BG_BLACK))
		passes[ph + ":M1"] = _viewport(false, mix | (1 << BIT_BG_WHITE))
	for key in passes:
		(passes[key] as SubViewport).world_2d = vp.world_2d
		root.add_child(passes[key])
	for k in load("res://scripts/keeper.gd").VFX_KITS:
		if String(k["name"]) == KIT:
			kit = (k as Dictionary).duplicate(true)
	if kit.is_empty():
		print("[bake] HALT: no kit ", KIT)
		quit(2)
		return
	for i in 10:
		await RenderingServer.frame_post_draw
	if not impact_only:
		await _bake_halo()
	seed(gseed)
	bolt = load(String(kit["bolt"])).instantiate()
	actors.add_child(bolt)
	bolt.set_meta("flame_dance_seed", DANCE_SEED)
	for i in 6:
		await physics_frame
	await process_frame
	var dest := {"point": SOCKET + Vector2.RIGHT * float(kit["range_px"]), "target": null, "kind": "cursor",
		"facing": Vector2.RIGHT}
	var p = load("res://scripts/vfx_g1.gd").acquire(actors, kit, SOCKET, dest, caster, 1.0)
	if p != bolt:
		print("[bake] HALT: acquire did not take the pre-placed projectile")
		quit(3)
		return
	var tick := 0
	var last_pf := -1
	while tick < 400:
		_assign_layers()
		await RenderingServer.frame_post_draw
		var row := _snapshot(tick)
		if last_pf >= 0 and int(row["physics_frame"]) != last_pf + 1:
			warnings.append("tick %d: physics frame %d after %d" % [tick, row["physics_frame"], last_pf])
		last_pf = int(row["physics_frame"])
		_capture(tick, row)
		log_rows.append(row)
		var alive := bool(row["travel_visible"]) or row.has("impact") or bool(row["cast_busy"]) or bool(row["trail_busy"])
		if tick > 5 and not alive:
			break
		tick += 1
		await process_frame
	var f := FileAccess.open(out_dir.path_join("bake_log.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"kit": KIT, "kit_config": kit, "seed": gseed, "dance_seed": DANCE_SEED,
		"socket": [SOCKET.x, SOCKET.y], "feet": [FEET.x, FEET.y], "halo_at": [HALO_AT.x, HALO_AT.y], "vp": [VP.x, VP.y],
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"impact_only": impact_only, "ticks": log_rows, "shots": shots, "warnings": warnings}))
	f.close()
	print("[bake] seed %d: %d ticks, %d shots, %d warnings -> %s" % [gseed, log_rows.size(), shots, warnings.size(), out_dir])
	for w in warnings.slice(0, 10):
		print("[bake] warning: ", w)
	quit(0)


func _viewport(transparent: bool, mask: int) -> SubViewport:
	var v := SubViewport.new()
	v.size = VP
	v.disable_3d = true
	v.transparent_bg = transparent
	v.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	v.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	if mask != 0:
		v.canvas_cull_mask = mask
	return v


# ---- which bit each item draws on --------------------------------------------------------------
func _phase_of(n: Node) -> String:
	var ff = bolt.fire_fx if bolt != null and bolt.fire_fx != null and is_instance_valid(bolt.fire_fx) else null
	var tm = bolt.trail_motes if bolt != null and bolt.trail_motes != null and is_instance_valid(bolt.trail_motes) else null
	var p: Node = n
	while p != null and p != actors:
		if p == halo:
			return "halo"
		if bolt != null and p == bolt:
			return "travel"
		if ff != null and p == ff.puff:
			return "puff"
		if ff != null and p == ff.floor_disc:
			return "cast_floor"
		if tm != null and p == tm:
			return "motes"
		if String(p.scene_file_path) == String(kit.get("impact", "")):
			return "impact_floor" if n == p.get_node_or_null("FloorLight") else "impact"
		p = p.get_parent()
	return ""


func _assign_layers() -> void:
	var items := actors.find_children("*", "CanvasItem", true, false)
	for n in items:
		(n as CanvasItem).visibility_layer = 0
	for n in items:
		var ci := n as CanvasItem
		if not _draws(ci):
			continue
		var ph := _phase_of(ci)
		if ph == "":
			continue
		var bit := 1 << (PHASES.find(ph) * 2 + (1 if _blend_is_add(ci) else 0))
		var q: Node = ci
		while q != null and q != world:
			if q is CanvasItem:
				(q as CanvasItem).visibility_layer |= bit
			q = q.get_parent()
	for n in items:
		var ci := n as CanvasItem
		if _draws(ci) and ci.is_visible_in_tree() and ci.get_child_count() > 0:
			var own := 1 << (PHASES.find(_phase_of(ci)) * 2 + (1 if _blend_is_add(ci) else 0)) if _phase_of(ci) != "" else 0
			if own != 0 and ci.visibility_layer != own and _has_drawable(ci):
				var w := "drawing parent %s carries child bits %x (own %x)" % [ci.name, ci.visibility_layer, own]
				if not warnings.has(w):
					warnings.append(w)
	actors.visibility_layer = 0xFFFFF
	world.visibility_layer = 0xFFFFFFFF


func _has_drawable(ci: CanvasItem) -> bool:
	if ci is Sprite2D:
		return (ci as Sprite2D).texture != null
	return true


# ---- the halo ---------------------------------------------------------------------------------------
func _bake_halo() -> void:
	halo = Sprite2D.new()
	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 0.25, 1.0])
	gradient.colors = PackedColorArray([Color.WHITE, Color(1, 1, 1, 0.7), Color(1, 1, 1, 0)])
	var disc := GradientTexture2D.new()
	disc.gradient = gradient
	disc.width = 64
	disc.height = 64
	disc.fill = GradientTexture2D.FILL_RADIAL
	disc.fill_from = Vector2(0.5, 0.5)
	disc.fill_to = Vector2(1.0, 0.5)
	halo.texture = disc
	var additive := CanvasItemMaterial.new()
	additive.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	halo.material = additive
	halo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	halo.position = HALO_AT
	actors.add_child(halo)
	var band: Array = kit["palette_2"]
	var bh := 130.0
	var rows := []
	for i in 32:
		var t := float(i) / 31.0
		var pulse := 1.0 + 0.15 * sin(PI * t)
		halo.scale = Vector2.ONE * (2.0 * 0.35 * bh / 64.0) * pulse
		halo.modulate = Color(float(band[0]), float(band[1]), float(band[2]), lerpf(0.6, 0.9, t))
		_assign_layers()
		await RenderingServer.frame_post_draw
		var img := (passes["halo:S"] as SubViewport).get_texture().get_image()
		var r := img.get_used_rect().grow(2).intersection(Rect2i(Vector2i.ZERO, VP))
		img.get_region(r).save_png(out_dir.path_join("halo_%02d_S.png" % i))
		shots += 1
		rows.append({"i": i, "t": t, "rect": [r.position.x, r.position.y, r.size.x, r.size.y], "scale": halo.scale.x,
			"alpha": halo.modulate.a})
		await process_frame
	halo.queue_free()
	halo = null
	await RenderingServer.frame_post_draw
	var f := FileAccess.open(out_dir.path_join("halo_log.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"anchor": [HALO_AT.x, HALO_AT.y], "frames": rows}))
	f.close()


# ---- per tick -----------------------------------------------------------------------------------
func _impact_node() -> Node2D:
	for c in actors.get_children():
		if String(c.scene_file_path) == String(kit["impact"]) and c.is_inside_tree() and not c.is_queued_for_deletion():
			return c
	return null


func _snapshot(tick: int) -> Dictionary:
	var row := {"tick": tick, "physics_frame": Engine.get_physics_frames()}
	row["travel_visible"] = bolt.visible
	row["bolt_pos"] = [bolt.global_position.x, bolt.global_position.y]
	row["bolt_active"] = bool(bolt.active)
	row["bolt_draining"] = bool(bolt.draining)
	var ff = bolt.fire_fx
	row["cast_busy"] = ff != null and is_instance_valid(ff) and bool(ff.busy)
	if row["cast_busy"]:
		row["puff"] = {"visible": ff.puff.visible, "pos": [ff.puff.global_position.x, ff.puff.global_position.y],
			"rotation": ff.puff.rotation, "scale": ff.puff.scale.x, "alpha": ff.puff.modulate.a} if ff.puff != null else {}
		row["cast_floor"] = {"visible": ff.floor_disc.visible, "pos": [ff.floor_disc.global_position.x, ff.floor_disc.global_position.y],
			"alpha": ff.floor_disc.modulate.a} if ff.floor_disc != null else {}
	var tm = bolt.trail_motes
	row["trail_busy"] = tm != null and is_instance_valid(tm) and bool(tm.busy)
	if tm != null and is_instance_valid(tm):
		row["trail_source"] = [tm.source_point.x, tm.source_point.y]
		row["trail_emitting"] = bool(tm.emitting)
		var motes := []
		for s in tm.slots:
			if bool(s.get("live", false)) and (s["node"] as Node2D).visible:
				var n: Polygon2D = s["node"]
				motes.append({"id": int(s["id"]), "pos": [n.global_position.x, n.global_position.y], "alpha": n.modulate.a,
					"color": [n.color.r, n.color.g, n.color.b], "half": absf(n.polygon[0].x), "origin": [s["origin"].x, s["origin"].y],
					"phase": float(s["phase"]), "life": float(s["life"]), "birth_tick": int(s["tick"])})
		row["motes"] = motes
	var im := _impact_node()
	if im != null:
		row["impact"] = {"pos": [im.global_position.x, im.global_position.y], "age": int(im.last_age),
			"seed": int(im.get("interleave_seed")), "stage": String(im.stage),
			"floor_visible": im.get_node("FloorLight").visible, "floor_alpha": im.get_node("FloorLight").modulate.a}
	return row


func _capture(tick: int, row: Dictionary) -> void:
	row["phases"] = {}
	var present := {}
	for n in actors.find_children("*", "CanvasItem", true, false):
		var ci := n as CanvasItem
		if _draws(ci) and ci.is_visible_in_tree():
			var ph := _phase_of(ci)
			if ph == "" or ph == "motes" or ph == "halo":
				continue
			if impact_only and not ph.begins_with("impact"):
				continue
			if not present.has(ph):
				present[ph] = {"mix": 0, "add": 0}
			present[ph]["add" if _blend_is_add(ci) else "mix"] += 1
	for ph in present:
		var s_img := (passes[ph + ":S"] as SubViewport).get_texture().get_image()
		var rect := s_img.get_used_rect()
		var rec := {"rect": null, "mix_items": present[ph]["mix"], "add_items": present[ph]["add"]}
		if rect.size.x > 0 and rect.size.y > 0:
			rect = rect.grow(2).intersection(Rect2i(Vector2i.ZERO, VP))
			rec["rect"] = [rect.position.x, rect.position.y, rect.size.x, rect.size.y]
			s_img.get_region(rect).save_png(out_dir.path_join("%s_%03d_S.png" % [ph, tick]))
			shots += 1
			if int(present[ph]["mix"]) > 0:
				(passes[ph + ":M0"] as SubViewport).get_texture().get_image().get_region(rect).save_png(
					out_dir.path_join("%s_%03d_M0.png" % [ph, tick]))
				(passes[ph + ":M1"] as SubViewport).get_texture().get_image().get_region(rect).save_png(
					out_dir.path_join("%s_%03d_M1.png" % [ph, tick]))
				shots += 2
		row["phases"][ph] = rec


func _blend_is_add(ci: CanvasItem) -> bool:
	var m: Material = ci.material
	var p: Node = ci
	while m == null and p is CanvasItem and (p as CanvasItem).use_parent_material:
		p = p.get_parent()
		m = (p as CanvasItem).material if p is CanvasItem else null
	if m is CanvasItemMaterial:
		return (m as CanvasItemMaterial).blend_mode == CanvasItemMaterial.BLEND_MODE_ADD
	if m is ShaderMaterial and (m as ShaderMaterial).shader != null:
		var code := (m as ShaderMaterial).shader.code
		var i := code.find("render_mode")
		if i >= 0:
			var line := code.substr(i, code.find(";", i) - i)
			return line.contains("blend_add")
	return false


func _draws(ci: CanvasItem) -> bool:
	return ci is Sprite2D or ci is AnimatedSprite2D or ci is Polygon2D or ci is Line2D or ci is ColorRect \
		or ci is TextureRect or ci is GPUParticles2D or ci is CPUParticles2D or ci is MeshInstance2D
