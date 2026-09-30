extends SceneTree
## C-9 (c) -- THE FIRE BALL FIDELITY PROOF: the kit's own runtime against its baked flipbook, the same
## frames, the same camera, over the same painted ground. drax.
##
##   Godot --path <cliffside scratch copy> --rendering-method gl_compatibility --rendering-driver opengl3_angle \
##         --fixed-fps 60 --resolution 320x180 --script res://proof_fire_bolt.gd -- \
##         --pack <dir with fire_ball.json + atlas_*.bin> --bg <png> --out FILE.json [--seed 1] [--impact-set 0] [--samples DIR]
##
## TWO WORLDS, ONE CLOCK. World A is bake_fire_bolt.gd's own cast (the same seeds, so the same states):
## the kit's runtime, drawn by its own renderer, over the ground image. World B plays the atlas over the
## same ground: one Sprite2D per phase (a CanvasItemMaterial in PREMULT_ALPHA: out = rgb + ground*(1-a),
## the formula the atlas was made for) at the phase's anchor + the frame's offset, and the trail motes
## re-played from the log's births by vfx_fire_motes_fl4.gd's own rule (so the port's replay is proven
## too). Every tick both are read back and compared texel by texel: mean |d| over the effect's
## FOOTPRINT (texels where either world differs from the bare ground), max, and the share of footprint
## texels over 3/255. The halo first: keeper.gd's replica against its 32 baked steps.

const VP := Vector2i(1600, 900)
const SOCKET := Vector2(300.25, 450.5)
const FEET := Vector2(300.25, 550.5)
const HALO_AT := Vector2(1200.0, 200.0)
const KIT := "fire_bolt_e1_B"
const DANCE_SEED := 20260930

var pack_dir := ""
var bg_path := ""
var out_file := ""
var samples_dir := ""
var gseed := 1
var impact_set := 0
var no_halo := false          # --no-halo: as bake_fire_bolt.gd --impact-only (the same frame count before the cast, so the same interleave seed)
var impact_seed := -1
var va: SubViewport
var vb: SubViewport
var actors: Node2D
var caster: Node2D
var kit: Dictionary
var meta: Dictionary
var pages: Array = []
var bolt
var bg_bytes: PackedByteArray
var sprites := {}
var motes_b := {}
var results: Array = []
var halo_results: Array = []


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		var a := String(args[i])
		var nxt := String(args[i + 1]) if i + 1 < args.size() else ""
		match a:
			"--pack": pack_dir = nxt
			"--bg": bg_path = nxt
			"--out": out_file = nxt
			"--samples": samples_dir = nxt
			"--seed": gseed = int(nxt)
			"--impact-set": impact_set = int(nxt)
			"--no-halo": no_halo = true
	if samples_dir != "":
		DirAccess.make_dir_recursive_absolute(samples_dir)
	meta = JSON.parse_string(FileAccess.get_file_as_string(pack_dir.path_join("fire_ball.json")))
	for f in meta["atlas"]["files"]:
		var bytes := FileAccess.get_file_as_bytes(pack_dir.path_join(String(f["file"])))
		var img := Image.new()
		img.load_webp_from_buffer(bytes)
		pages.append(ImageTexture.create_from_image(img))
	var bg_img := Image.load_from_file(bg_path)
	bg_img.convert(Image.FORMAT_RGB8)
	bg_bytes = bg_img.get_data()
	var bg_tex := ImageTexture.create_from_image(bg_img)
	va = _viewport()
	vb = _viewport()
	root.add_child(va)
	root.add_child(vb)
	for v in [va, vb]:
		var s := Sprite2D.new()
		s.texture = bg_tex
		s.centered = false
		s.z_index = -4096
		v.add_child(s)
	actors = Node2D.new()
	actors.y_sort_enabled = true
	va.add_child(actors)
	caster = Node2D.new()
	caster.position = FEET
	actors.add_child(caster)
	var premul := CanvasItemMaterial.new()
	premul.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
	# B's draw order, back to front, as the kit's canvas order puts them for an east cast
	for ph in ["cast_floor", "impact_floor", "motes", "puff", "travel", "impact", "halo"]:
		if ph == "motes":
			continue
		var sp := Sprite2D.new()
		sp.centered = false
		sp.region_enabled = true
		sp.material = premul
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		sp.visible = false
		sp.name = "B_" + ph
		vb.add_child(sp)
		sprites[ph] = sp
		if ph == "impact_floor":
			var mnode := Node2D.new()
			mnode.name = "B_motes"
			vb.add_child(mnode)
			motes_b["root"] = mnode
	for k in load("res://scripts/keeper.gd").VFX_KITS:
		if String(k["name"]) == KIT:
			kit = (k as Dictionary).duplicate(true)
	for i in 10:
		await RenderingServer.frame_post_draw
	if not no_halo:
		await _halo_proof()
	seed(gseed)
	bolt = load(String(kit["bolt"])).instantiate()
	actors.add_child(bolt)
	bolt.set_meta("flame_dance_seed", DANCE_SEED)
	for i in 6:
		await physics_frame
	await process_frame
	var dest := {"point": SOCKET + Vector2.RIGHT * float(kit["range_px"]), "target": null, "kind": "cursor", "facing": Vector2.RIGHT}
	load("res://scripts/vfx_g1.gd").acquire(actors, kit, SOCKET, dest, caster, 1.0)
	var tick := 0
	var imp_at := Vector2.INF
	while tick < 200:
		_play_b(tick)
		await RenderingServer.frame_post_draw
		var a_img := va.get_texture().get_image()
		var b_img := vb.get_texture().get_image()
		var st := _compare(a_img, b_img)
		st["tick"] = tick
		results.append(st)
		if samples_dir != "" and tick in [2, 10, 17, 20, 24, 30, 45, 90]:
			a_img.save_png(samples_dir.path_join("kit_%03d.png" % tick))
			b_img.save_png(samples_dir.path_join("baked_%03d.png" % tick))
		var imn := _impact_node()
		if imn != null and impact_seed < 0:
			impact_seed = int(imn.get("interleave_seed"))
		var alive: bool = bolt.visible or _impact_node() != null or (bolt.trail_motes != null and bool(bolt.trail_motes.busy))
		if tick > 5 and not alive and st["footprint"] == 0:
			break
		tick += 1
		await process_frame
	var worst := 0.0
	var worst_tick := -1
	for r in results:
		if float(r["mean_fp"]) > worst:
			worst = float(r["mean_fp"])
			worst_tick = int(r["tick"])
	var hw := 0.0
	for r in halo_results:
		hw = maxf(hw, float(r["mean_fp"]))
	var f := FileAccess.open(out_file, FileAccess.WRITE)
	f.store_string(JSON.stringify({"what": "kit runtime (A) vs baked flipbook (B), same frames and camera, over " + bg_path.get_file(),
		"seed": gseed, "impact_set": impact_set, "impact_interleave_seed": impact_seed,
		"baked_interleave_seed": int((meta["impact_seeds"] as Array)[impact_set]), "worst_mean_fp_255": worst * 255.0, "worst_tick": worst_tick,
		"halo_worst_mean_fp_255": hw * 255.0, "ticks": results, "halo": halo_results,
		"renderer": RenderingServer.get_current_rendering_method()}))
	f.close()
	print("[proof] interleave seed %d (baked %d)" % [impact_seed, int((meta["impact_seeds"] as Array)[impact_set])])
	print("[proof] seed %d set %d: %d ticks, worst footprint mean |d| %.3f/255 at tick %d; halo worst %.3f/255 -> %s" % [
		gseed, impact_set, results.size(), worst * 255.0, worst_tick, hw * 255.0, out_file])
	quit(0)


func _viewport() -> SubViewport:
	var v := SubViewport.new()
	v.size = VP
	v.disable_3d = true
	v.transparent_bg = false
	v.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	v.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	return v


func _impact_node() -> Node2D:
	for c in actors.get_children():
		if String(c.scene_file_path) == String(kit["impact"]) and c.is_inside_tree() and not c.is_queued_for_deletion():
			return c
	return null


func _frame_for(ph: String, tick: int) -> Dictionary:
	var key := ph if ph != "impact" else "impact_%d" % impact_set
	for fr in meta["frames"].get(key, []):
		if int(fr["tick"]) == tick:
			return fr
	return {}


func _show(ph: String, fr: Dictionary, anchor: Vector2, alpha := 1.0) -> void:
	var sp: Sprite2D = sprites[ph]
	if fr.is_empty():
		sp.visible = false
		return
	sp.texture = pages[int(fr["page"])]
	sp.region_rect = Rect2(float(fr["x"]), float(fr["y"]), float(fr["w"]), float(fr["h"]))
	sp.position = anchor + Vector2(float(fr["ox"]), float(fr["oy"]))
	# premultiplied: the fade scales colour AND cover (a plain alpha would scale only the cover)
	sp.modulate = Color(alpha, alpha, alpha, alpha)
	sp.visible = true


func _play_b(tick: int) -> void:
	# travel: the node's position is the anchor (the port computes it; here the kit's own path)
	var trav: Array = meta["timing"]["travel"]
	var tr := {}
	for t in trav:
		if int(t["tick"]) == tick:
			tr = t
	if tr.is_empty():
		sprites["travel"].visible = false
	else:
		_show("travel", _frame_for("travel", tick), SOCKET + Vector2(float(tr["dx"]), float(tr["dy"])))
	_show("puff", _frame_for("puff", tick), SOCKET)
	# the floors: one frame with an alpha, or their own frames
	for ph in ["cast_floor", "impact_floor"]:
		var anchor := FEET if ph == "cast_floor" else SOCKET + Vector2(float(meta["timing"]["impact_dx"]), float(meta["timing"]["impact_dy"]))
		var t0 := 0 if ph == "cast_floor" else int(meta["timing"]["impact_spawn_tick"])
		var als: Array = meta["floor_alpha"].get(ph, [])
		var frs: Array = meta["frames"][ph]
		if not als.is_empty():
			var i := tick - t0
			if i >= 0 and i < als.size() and float(als[i]) > 0.0:
				_show(ph, frs[0], anchor, float(als[i]) / float(als[0]))
			else:
				sprites[ph].visible = false
		else:
			_show(ph, _frame_for(ph, tick), anchor)
	_show("impact", _frame_for("impact", tick), SOCKET + Vector2(float(meta["timing"]["impact_dx"]), float(meta["timing"]["impact_dy"])))
	# the motes, re-played by the kit's rule from their births
	var mroot: Node2D = motes_b["root"]
	var lat := float(meta["motes"]["lateral_px"])
	var rise := float(meta["motes"]["rise_px_s"])
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	for b in meta["motes"]["births"]:
		var id := int(b["id"])
		var node: Polygon2D = motes_b.get(id)
		if node == null:
			node = Polygon2D.new()
			var h := float(b["half_px"])
			node.polygon = PackedVector2Array([Vector2(-h, 0), Vector2(0, -h), Vector2(h, 0), Vector2(0, h)])
			var c: Array = b["color"]
			node.color = Color(float(c[0]), float(c[1]), float(c[2]), 1)
			node.material = add
			mroot.add_child(node)
			motes_b[id] = node
		var age := float(tick - int(b["birth_tick"])) / 60.0
		var life := float(b["life_s"])
		# NOT ON ITS BIRTH TICK: the kit's pool shows a born mote before its first position update, so on
		# that one frame it stands at the canvas origin (off the play frame) -- the port starts it a tick on
		if age <= 0.0 or age >= life:
			node.visible = false
			continue
		var ph := float(b["phase"])
		var origin := SOCKET + Vector2(float(b["origin_dx"]), float(b["origin_dy"]))
		node.position = origin + Vector2(lat * (sin(ph + age * 8.0) - sin(ph)) * 0.5, -rise * age)
		node.modulate.a = 1.0 - age / life
		node.visible = true


const CMP := Rect2i(100, 80, 1200, 770)       # the cast, the flight, the burst and the halo, with margin


func _compare(a: Image, b: Image) -> Dictionary:
	a.convert(Image.FORMAT_RGB8)
	b.convert(Image.FORMAT_RGB8)
	var da := a.get_data()
	var db := b.get_data()
	var fp := 0
	var sum := 0
	var over3 := 0
	var mx := 0
	for y in range(CMP.position.y, CMP.end.y):
		var i := (y * VP.x + CMP.position.x) * 3
		var e := i + CMP.size.x * 3
		while i < e:
			var r0 := da[i]
			var g0 := da[i + 1]
			var b0 := da[i + 2]
			var r1 := db[i]
			var g1 := db[i + 1]
			var b1 := db[i + 2]
			if r0 != bg_bytes[i] or g0 != bg_bytes[i + 1] or b0 != bg_bytes[i + 2] or r1 != bg_bytes[i] or g1 != bg_bytes[i + 1] or b1 != bg_bytes[i + 2]:
				fp += 1
				sum += absi(r0 - r1) + absi(g0 - g1) + absi(b0 - b1)
				var dm: int = maxi(absi(r0 - r1), maxi(absi(g0 - g1), absi(b0 - b1)))
				if dm > mx:
					mx = dm
				if dm > 3:
					over3 += 1
			i += 3
	return {"footprint": fp, "mean_fp": (float(sum) / float(max(fp, 1) * 3)) / 255.0, "max": mx,
		"over3_share": float(over3) / float(max(fp, 1))}


func _halo_proof() -> void:
	var halo := Sprite2D.new()
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
	var frs: Array = meta["frames"]["halo"]
	for i in 32:
		var t := float(i) / 31.0
		halo.scale = Vector2.ONE * (2.0 * 0.35 * 130.0 / 64.0) * (1.0 + 0.15 * sin(PI * t))
		halo.modulate = Color(float(band[0]), float(band[1]), float(band[2]), lerpf(0.6, 0.9, t))
		_show("halo", frs[i], HALO_AT)
		await RenderingServer.frame_post_draw
		var st := _compare(va.get_texture().get_image(), vb.get_texture().get_image())
		st["i"] = i
		halo_results.append(st)
		await process_frame
	halo.queue_free()
	sprites["halo"].visible = false
	await RenderingServer.frame_post_draw
