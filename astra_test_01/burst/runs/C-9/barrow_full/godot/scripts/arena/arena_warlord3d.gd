extends Node3D
## C-9 BV2F ARENA (R-C9-348) -- THE WARLORD AS KC2 PLAYS HIM: the JOIN-1 hero pack (gd-eor-warlord-eor3) and the
## Eye of Reckoning overlay (eor_overlay: an UNDER layer below him, an OVER layer above), driven exactly as
## kc2_play/src/kc2p_warlord.gd drives them (its "dressed" path), on billboards in the barrow scene.
##   channel_on   -> eor_spin_start, then the eor_spin_loop; overlay start (7 f @30) then loop phase-locked to the body's
##                   spin frame (16 * (rev mod 4) + frame)
##   channel_off  -> overlay end (25 f @30), the under layer looping and fading over 0.8 s
##   war_cry cast -> the warcry clip, release on the tick
##   player_death -> the death clip, held
##   else         run (charging) / walk (moving) / idle; facing = the step's bearing
## The OVER layer's cells are TILED (32 px tiles per frame); they are composed by a 2D drawer inside a SubViewport
## (the same draw calls kc2p_eor_fx.gd makes) whose texture the over billboard shows.

const J = preload("res://scripts/arena/arena_art.gd")
const Body3D = preload("res://scripts/arena/arena_body3d.gd")
const OV_FPS := 30.0
const OV_UNDER_FADE_S := 0.8
const OVER_VP := Vector2i(768, 768)
const OVER_ANCHOR := Vector2(384.0, 416.0)     # the over layer's canvas anchor (768, 832) at stage scale 0.5

var hero_kit: String = ""
var body: Sprite3D = null
var under: Sprite3D = null
var over: Sprite3D = null
var over_vp: SubViewport = null
var over_draw: Node2D = null
var dir: String = "S"
var state: String = "idle"
var pos_m: Vector2 = Vector2.ZERO
var last_pos_m: Vector2 = Vector2.ZERO
var channel: bool = false
var dead: bool = false
var ov_seg: String = ""
var ov_t0: float = 0.0
var ov_end_t0: float = -1.0
var ov_last_loop_frame: int = 0
var ok: bool = false


class OverDraw extends Node2D:
	var cid: String = ""
	var fi: int = 0
	var a: float = 1.0

	func _draw() -> void:
		if cid == "" or a <= 0.0:
			return
		var c: Dictionary = J.cell("eor_overlay", cid)
		if c.is_empty():
			return
		var tex: Texture2D = J.cell_tex("eor_overlay", cid)
		if tex == null:
			return
		var n := int(c["n"])
		var f := clampi(fi, 0, n - 1)
		var anc: Array = c["anchor_px"]
		var ax := float(anc[0])
		var ay := float(anc[1])
		var mod := Color(1, 1, 1, a)
		var T := float(c["tile"])
		var P := int(c["tile_pitch"])
		var C := int(c["atlas_cols"])
		for t_any in ((c["frames"] as Array)[f] as Array):
			var t: Array = t_any
			var ti := int(t[2])
			var src := Rect2(float((ti % C) * P + 1), float((ti / C) * P + 1), T, T)
			var dst := Rect2(float(t[0]) - ax + 384.0, float(t[1]) - ay + 416.0, T, T)
			draw_texture_rect_region(tex, dst, src, mod)


func setup() -> void:
	hero_kit = J.hero_kit()
	if hero_kit == "" or J.kit_meta(hero_kit).is_empty():
		push_error("[arena] the JOIN-1 hero pack is not staged (kc2_play/art/join1/%s)" % hero_kit)
		return
	var om := J.kit_meta("eor_overlay")
	var layers: Dictionary = om.get("layers", {})
	# UNDER: a plain strip, drawn below him
	under = Sprite3D.new()
	under.name = "EorUnder"
	under.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	under.shaded = false
	under.centered = false
	under.region_enabled = true
	under.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	under.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	under.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	under.render_priority = Body3D.PRIORITY_UNDER
	under.no_depth_test = true          # a ground haze several metres across: never cut by the terrain
	under.pixel_size = 1.0 / float((layers.get("under", {}) as Dictionary).get("staged_ppm", 37.834))
	under.visible = false
	add_child(under)
	body = Body3D.new()
	body.name = "Body"
	body.setup_body(hero_kit, 1.0)
	add_child(body)
	# OVER: composed in a SubViewport, shown above him
	over_vp = SubViewport.new()
	over_vp.size = OVER_VP
	over_vp.transparent_bg = true
	over_vp.disable_3d = true
	over_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	over_draw = OverDraw.new()
	over_vp.add_child(over_draw)
	add_child(over_vp)
	over = Sprite3D.new()
	over.name = "EorOver"
	over.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	over.shaded = false
	over.centered = false
	over.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	over.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	over.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	over.render_priority = Body3D.PRIORITY_OVER
	over.no_depth_test = true
	over.texture = over_vp.get_texture()
	over.offset = Vector2(-OVER_ANCHOR.x, OVER_ANCHOR.y - float(OVER_VP.y))
	over.pixel_size = 1.0 / float((layers.get("over", {}) as Dictionary).get("staged_ppm", 75.668))
	over.visible = false
	add_child(over)
	J.prefetch(hero_kit)
	J.prefetch("eor_overlay")
	body.play_loop("idle")
	ok = true


static func dir_of(v: Vector2) -> String:
	return J.dir_of(v)


func on_event(e: Dictionary) -> void:
	if not ok or dead:
		return
	var ev := String(e.get("event", ""))
	if ev == "channel_on":
		channel = true
		body.play_oneshot("eor_spin_start")
		ov_seg = "start"
		ov_t0 = body.clock_s
		ov_end_t0 = -1.0
	elif ev == "channel_off":
		channel = false
		ov_seg = "end"
		ov_end_t0 = body.clock_s
	elif ev == "cast_start" and int(e.get("actor_id", -1)) == 0:
		if String(e.get("skill_id", "")) == "war_cry" and not channel and J.has_state(hero_kit, "warcry"):
			body.release_now("warcry", body.clip_T("warcry") - body.rel_s("warcry"))
	elif ev == "player_death":
		dead = true
		channel = false
		body.play_oneshot("death", true)
		ov_seg = "end" if ov_seg != "" else ""
		ov_end_t0 = body.clock_s


## Per frame: the player's KC2-frame position (for facing) and the driver (channel / charge).
func sync(player_m: Vector2, driver) -> void:
	if not ok:
		return
	last_pos_m = pos_m
	pos_m = player_m
	var v := pos_m - last_pos_m
	var moving := v.length() > 1e-6
	if moving:
		dir = dir_of(v)
	body.dir = dir
	if dead:
		state = "death"
		return
	if channel or driver.channel_on:
		state = "attack"
		if body.a_state == "eor_spin_start" and not body.busy():
			body.play_loop("eor_spin_loop")
		elif body.a_state != "eor_spin_start" and body.a_state != "eor_spin_loop":
			body.play_loop("eor_spin_loop")
		return
	if body.busy():
		return
	if driver.charge_to != null:
		state = "run"
	elif moving:
		state = "walk"
	else:
		state = "idle"
	body.play_loop(state)


func advance(dt: float) -> void:
	if not ok:
		return
	body.advance(dt)
	_drive_overlay()


func _drive_overlay() -> void:
	var t: float = body.clock_s
	match ov_seg:
		"":
			_under_hide()
			_over_hide()
		"start":
			var f := int(floor((t - ov_t0) * OV_FPS))
			if body.a_state == "eor_spin_loop":
				ov_seg = "loop"
				_drive_overlay()
				return
			_under_show("start", mini(f, 6), 1.0)
			_over_show("start", mini(f, 6), 1.0)
		"loop":
			var lf: int = 16 * posmod(int(body.loop_rev()), 4) + clampi(int(body.frame_i), 0, 15)
			ov_last_loop_frame = lf
			_under_show("loop", lf, 1.0)
			_over_show("loop", lf, 1.0)
		"end":
			var te: float = t - ov_end_t0
			var fe := int(floor(te * OV_FPS))
			var a := maxf(0.0, 1.0 - te / OV_UNDER_FADE_S)
			var lf2 := (ov_last_loop_frame + int(floor(te * 53.333333))) % 64
			if a > 0.0:
				_under_show("loop", lf2, a)
			else:
				_under_hide()
			if fe < 25:
				_over_show("end", fe, 1.0)
			else:
				_over_hide()
			if a <= 0.0 and fe >= 25:
				ov_seg = ""


func _under_show(seg: String, f: int, a: float) -> void:
	var cid := "under/%s" % seg
	var c := J.cell("eor_overlay", cid)
	var tex := J.cell_tex("eor_overlay", cid)
	if c.is_empty() or tex == null:
		return
	var n := int(c["n"])
	var fi := clampi(f, 0, n - 1)
	var cols := int(c["cols"])
	var fw := float(c["fw"])
	var fh := float(c["fh"])
	var anc: Array = c["anchor_px"]
	under.texture = tex
	under.region_rect = Rect2(float(fi % cols) * fw, float(fi / cols) * fh, fw, fh)
	under.offset = Vector2(-float(anc[0]), float(anc[1]) - fh)
	under.modulate = Color(1, 1, 1, a)
	under.visible = true


func _under_hide() -> void:
	under.visible = false


func _over_show(seg: String, f: int, a: float) -> void:
	over_draw.cid = "over/%s/%s" % [seg, dir]
	over_draw.fi = f
	over_draw.a = a
	over_draw.queue_redraw()
	over.visible = true


func _over_hide() -> void:
	if over_draw.cid != "":
		over_draw.cid = ""
		over_draw.queue_redraw()
	over.visible = false
