extends SceneTree
# C-9 R-C9-61 (T3): fit the 3D knight's camera to the SPRITE knight already in the build,
# by rendering it and measuring, then write frames/knight3d_camera.json.
#
# WHY A FIT AND NOT A CONSTANT.  Two px-per-metre figures are in circulation for this
# character and they disagree by 6.6%: the dispatch's 117.5 (meshy_test/render_anim.py's
# ortho_scale) and 110.185 (knight3d/10_render.py's BODY_PX / 1.80).  Picking one by
# argument would be a coin toss that shows up as the figure jumping size when K is
# pressed.  Neither is needed: the sprite cells are IN the build and can be measured, the
# 3D camera can be rendered and measured, and the fit between two measurements does not
# care which number was right.
#
# It also survives the swap.  When the real 8-direction set lands and replaces the
# placeholder, re-running this re-fits against the new cells -- so the one-line source
# change T1 promises does not silently leave the 3D skin calibrated to the old artwork.
#
# WHAT IS MATCHED, and why these two and not others:
#   SOLE ROW    the lowest opaque row over the cycle -- the ground line the eye reads.
#               Both figures stand on the same floor, so this must agree or the knight
#               hovers or sinks.
#   BODY HEIGHT the median PER-FRAME crown-to-sole span.  Per-frame, and median, because
#               max-sole-minus-min-crown mixes frames and inflates the height by the
#               whole vertical bob -- 10 px on these cells, a 5% error in the scale.
# The pollaxe is hidden for the fit: the placeholder cells are weapon-free, so a
# silhouette including a haft would be measuring two different characters.

const SPRITE_FRAMES := "res://frames/knight_test.tres"
const KEEPER_FRAMES := "res://frames/keeper.tres"
const OUT := "res://frames/knight3d_camera.json"
const CLIP := "c_idle"
const DIRECTIONS := ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
const CAMERA_JSON := "res://frames/camera_meshy_t1.json"
const PHASES := 12                 # sample the cycle at the sprite set's own frame count
const ALPHA := 8

var report := {}


func _initialize():
	print("=== C-9 R-C9-61 T3 camera fit ===")
	var target := _target()
	if target.is_empty():
		print("FAIL: could not measure the sprite cells")
		quit(1)
		return

	var scene = load("res://scenes/cliffside.tscn").instantiate()
	root.add_child(scene)
	await physics_frame
	var k3 = scene.find_child("Knight3D", true, false)
	if k3 == null:
		print("FAIL: no Knight3D node in the scene (run tools/patch_scene.py --with-3d)")
		quit(1)
		return
	k3.call("set_active", true)
	# Hide the haft, KEEP the pose. camera.json's 199 px is measured with the pollaxe
	# split off, so the fit must measure the same silhouette or it is scaling the figure
	# to fit a weapon. set_armed(false) would also swap to the weapon-off clip set and
	# fit the camera to a pose the armed knight never stands in.
	k3.call("set_weapon_visible", false)
	await process_frame

	var st: Dictionary = k3.call("status")
	var ppm: float = float(st["px_per_m"])
	var aim: float = float(st["aim_up_m"])
	print("start   %.3f px/m   aim %.4f m" % [ppm, aim])
	print("target  sole row %.1f   body %.2f px   from %s"
		% [target.sole, target.height, str(target.get("source", "?"))])

	var passes := []
	for it in 4:
		k3.call("set_fit", ppm, aim)
		await process_frame
		var got := await _measure_3d(k3)
		if got.is_empty():
			print("FAIL: the 3D render is empty -- nothing to measure")
			quit(1)
			return
		var dh: float = target.height - got.height
		var ds: float = target.sole - got.sole
		print("pass %d  ppm %.3f aim %+.4f  ->  sole %.1f (%+.1f)  body %.2f (%+.2f)"
			% [it, ppm, aim, got.sole, ds, got.height, dh])
		passes.append({"pass": it, "ppm": ppm, "aim_up_m": aim,
					   "sole": got.sole, "sole_err": ds,
					   "height": got.height, "height_err": dh})
		if absf(ds) <= 0.5 and absf(dh) <= 0.5:
			break
		# Height is linear in the scale; the sole is linear in the aim. Correcting the
		# scale MOVES the sole, so scale first and let the next pass take the sole up.
		if absf(dh) > 0.5:
			ppm *= target.height / maxf(got.height, 1e-3)
		aim += ds / ppm

	# The BEST pass, not the last. A silhouette bound is an integer pixel, so the fit
	# cannot settle finer than +/-1 px and simply oscillates once it is there -- 199,
	# 200, 198. Taking whichever iteration the loop happened to stop on throws away a
	# better one it already found.
	var final = passes[0]
	for pr in passes:
		if absf(float(pr.sole_err)) + absf(float(pr.height_err)) \
			< absf(float(final.sole_err)) + absf(float(final.height_err)):
			final = pr
	report = {
		"note": "C-9 R-C9-61 T3. Written by tools/fit_knight3d.gd -- a measured fit of "
			+ "the 3D camera to the sprite cells in this build, not a typed constant. "
			+ "Re-run after swapping the sprite source.",
		"fitted_against": target.get("source", SPRITE_FRAMES),
		"sprite_target": target,
		"px_per_m_screen": float(final.ppm),
		"aim_up_m": float(final.aim_up_m),
		"sole_row": target.sole,
		"view_px": int(st["view_px"]) if st.has("view_px") else 512,
		"elevation_deg": 19.77,
		"passes": passes,
		"residual_px": {"sole": float(final.sole_err), "height": float(final.height_err)},
		"keeper_cycle_s": _keeper_cycles(),
		"px_per_m_note": {
			"what_this_number_is": "orthographic screen pixels per metre of SCREEN-VERTICAL "
				+ "world extent: Camera3D.size = view_px / this. It is NOT camera.json's "
				+ "px_per_m, which is projected crown-to-sole pixels per metre of CHARACTER "
				+ "HEIGHT. The two differ by roughly cos(elevation).",
			"110.556": "meshy_t1/camera.json -- 199 px / 1.80 m, measured on the Grok cells",
			"117.5": "gandalf / meshy_test render_anim.py ortho_scale; 117.5 * cos(19.77) "
				+ "= 110.574, so these two are ONE camera in two conventions, not a "
				+ "disagreement",
			"110.185": "knight_fit.json's carried-over figure_h_src_px / 1.80",
			"114.729": "my earlier fit, against the PLACEHOLDER cells, which are a paint-over "
				+ "of a 117.5 px/m render and measure 202 px where the game's measure 199. "
				+ "Correct about the cells; the cells were not the game. Retired.",
		},
	}
	var f := FileAccess.open(OUT, FileAccess.WRITE)
	f.store_string(JSON.stringify(report, " "))
	f.close()
	# 1.5 px, because a silhouette bound is an integer and the target is not (199.0008 =
	# 110.556 x 1.80), so a residual of exactly one pixel reads as 1.0008 and a 1.0
	# tolerance calls a converged fit a failure. Half a pixel of slack, not a loosened
	# standard: the instrument cannot resolve better than one.
	var ok: bool = absf(float(final.sole_err)) <= 1.5 and absf(float(final.height_err)) <= 1.5
	print("=== fit %s: %.3f px/m, aim %.4f m, residual sole %+.2f px / height %+.2f px ==="
		% ["PASS" if ok else "NOT CONVERGED", final.ppm, final.aim_up_m,
		   final.sole_err, final.height_err])
	print("wrote ", OUT)
	quit(0 if ok else 1)


func _bounds(img: Image) -> Dictionary:
	# Raw bytes, not get_pixel: this runs 512 x 512 x 12 phases x 4 passes, and get_pixel
	# turns a one-off calibration into a coffee break.
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	var d := img.get_data()
	var w := img.get_width()
	var h := img.get_height()
	var top := -1
	var bot := -1
	for y in h:
		var row := y * w * 4 + 3
		var any := false
		for x in w:
			if d[row + x * 4] > ALPHA:
				any = true
				break
		if any:
			if top < 0:
				top = y
			bot = y
	return {} if top < 0 else {"top": float(top), "bot": float(bot),
							   "height": float(bot - top)}


func _target() -> Dictionary:
	"""What the render must hit -- from the SPRITE PIPELINE'S OWN camera file when it
	exists, and only from the local cells when it does not.

	This used to fit against the placeholder sprite cells, and that is what produced
	114.729. The fit was right about the cells and the cells are not the game: they are
	an Astra paint-over of an earlier 117.5 px/m render, and painting fattens an outline,
	so they measure 202 px where the game's own cells measure 199. A fit is only ever as
	correct as the thing it is fitted to, and placeholder art is by definition not the
	thing. meshy_t1/camera.json is the measurement of the real cells; it wins.

	Note what px_per_m MEANS there: 199 px / 1.80 m, a PROJECTED crown-to-sole per metre
	of character height -- not an orthographic scale. The two differ by cos(elevation),
	which is exactly the 117.5-vs-110.556 gap (117.5 * cos 19.77 = 110.574). Rather than
	convert between them and hope, the target is stated in PIXELS and the camera is
	solved for, which no convention can corrupt."""
	if ResourceLoader.exists(CAMERA_JSON) or FileAccess.file_exists(CAMERA_JSON):
		var j = JSON.parse_string(FileAccess.get_file_as_string(CAMERA_JSON))
		if typeof(j) == TYPE_DICTIONARY and j.has("px_per_m"):
			var h := float(j.get("character_height_m", 1.8))
			return {"source": CAMERA_JSON,
					"sole": float(j.get("ground_row_y", 398.0)),
					"height": float(j["px_per_m"]) * h,
					"frames": 1, "height_spread": 0.0,
					"declared_px_per_m": float(j["px_per_m"]),
					"character_height_m": h}
	var m := _measure_sprites()
	if not m.is_empty():
		m["source"] = SPRITE_FRAMES + "  (PLACEHOLDER ART -- no camera.json present)"
	return m


func _measure_sprites() -> Dictionary:
	if not ResourceLoader.exists(SPRITE_FRAMES):
		return {}
	var sf: SpriteFrames = load(SPRITE_FRAMES)
	var anim := "walk_E"
	if not sf.has_animation(anim):
		var names := sf.get_animation_names()
		if names.is_empty():
			return {}
		anim = names[0]
	var soles := []
	var heights := []
	for i in sf.get_frame_count(anim):
		var tex: Texture2D = sf.get_frame_texture(anim, i)
		var b := _bounds(tex.get_image())
		if b.is_empty():
			continue
		soles.append(b.bot)
		heights.append(b.height)
	if soles.is_empty():
		return {}
	heights.sort()
	return {"animation": anim, "frames": soles.size(),
			"sole": float(soles.max()),
			"height": float(heights[heights.size() / 2]),
			"height_spread": float(heights[-1] - heights[0])}


func _measure_3d(k3) -> Dictionary:
	# Sample the whole cycle, the same way the sprite side is sampled, so the two
	# medians are medians of the same thing.
	var vp: SubViewport = k3.call("viewport")
	# The knight's own STANDING pose -- the armed idle -- because that is what the rule
	# is stated for and what the size probe will measure downstream. The bind pose was
	# deterministic and is not a pose the player ever sees; fitting to it left the idle
	# 20 px tall on screen. Sampled across the clip and taken as a median, since an idle
	# breathes.
	var length: float = k3.call("clip_length", CLIP)
	if length <= 0.0:
		length = 1.0
	var soles := []
	var heights := []
	# Across all EIGHT azimuths, not one. A 3D figure's projected crown-to-sole is not
	# constant with viewing angle -- an elevated orthographic view mixes height with
	# depth, and the depth between crown and toes changes as the body turns. Fitted at S
	# alone the knight stood 150.0 px there and 146.7 px at E, so the fit was right about
	# the direction it saw and wrong about the other seven. The median centres the error
	# instead of loading it all onto whichever direction was not measured.
	for di in DIRECTIONS.size():
		k3.call("drive", "idle", DIRECTIONS[di])
		k3.call("play_clip", CLIP, length * 0.3)
		await process_frame
		await process_frame
		var b := _bounds(vp.get_texture().get_image())
		if b.is_empty():
			continue
		soles.append(b.bot)
		heights.append(b.height)
	if soles.is_empty():
		return {}
	heights.sort()
	soles.sort()
	return {"sole": float(soles[soles.size() / 2]),
			"height": float(heights[heights.size() / 2]),
			"samples": soles.size(), "pose": CLIP,
			"height_spread": [heights[0], heights[-1]],
			"sole_spread": [soles[0], soles[-1]]}


func _measure_3d_unused(k3) -> Dictionary:
	var vp: SubViewport = k3.call("viewport")
	var length: float = k3.call("clip_length", CLIP)
	if length <= 0.0:
		length = 1.0
	var soles := []
	var heights := []
	for i in PHASES:
		k3.call("play_clip", CLIP, length * float(i) / float(PHASES))
		await process_frame
		await process_frame
		var img := vp.get_texture().get_image()
		var b := _bounds(img)
		if b.is_empty():
			continue
		soles.append(b.bot)
		heights.append(b.height)
	if soles.is_empty():
		return {}
	heights.sort()
	return {"sole": float(soles.max()), "height": float(heights[heights.size() / 2]),
			"samples": soles.size()}


func _keeper_cycles() -> Dictionary:
	# The Keeper's stride lengths, so the 3D clips can be retimed to them. Read from her
	# own SpriteFrames rather than transcribed: if she is ever retuned the knight follows.
	var out := {}
	if not ResourceLoader.exists(KEEPER_FRAMES):
		return out
	var sf: SpriteFrames = load(KEEPER_FRAMES)
	for pair in [["walk_E", "k_walk"], ["run_E", "k_run"], ["idle_E", "k_idle"]]:
		if sf.has_animation(pair[0]):
			var n := sf.get_frame_count(pair[0])
			var fps := sf.get_animation_speed(pair[0])
			if fps > 0.0:
				out[pair[1]] = float(n) / fps
	return out
