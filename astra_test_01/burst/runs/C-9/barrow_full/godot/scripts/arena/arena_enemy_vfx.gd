extends Node3D
## C-9 BV2F ARENA (R-C9-358..361, R-C9-374/376) -- THE ENEMY ATTACK VFX: OUR EXISTING EFFECTS, re-used.
##
## NO NEW EFFECT ART except the hit spark (R-C9-376). Every other frame is an existing asset, staged unaltered by
## tools/arena_stage_vfx.py into godot/kc2/vfx_x/ (sha256 of each source recorded in its index.json):
##   fire ranged     barrow's fire_ball_fx.gd ITSELF (cliffside e1_B baked; the speedy fireball), two instances,
##                   only aimed and timed here; its burst drawn at FIREBALL_BURST_K of its c75 size
##   other ranged    the C-9 en_e2 per-element enemy flipbooks: `bolt` in flight, `burst` on arrival
##   lightning       the C-7 cliffside lightning_blast kit (cast flare, travel, impact + its additive glow layer,
##                   residual), its own palette and hold frames; en_q_storm only past the explosion cap
##   area            en_e2 ring_burst (ground) + burst + ring_smoke
##   aura            en_e2 `aura` (ground, looping) at the caster; poison: en_b_blight ring_tele
##   thrown          the V45 Blackwater cocktail: flask.png on its arc; for fire its floor field + three pulse licks
##                   (vfx_g2_flame_dance.gd's rules: 2.5 s, licks flickering 3.3-3.6 Hz); else en_g_mud's burst
##   melee           en_e2 `slash` of the element; the hit SPARK on landing (the one new piece, procedural)
##   warlord hit     a red flash on his card
## The pack draws as camera-facing billboards / ground quads exactly as the monsters are drawn (premultiplied, at the
## barrow's 100.6 px/m), in ONE MultiMesh over a Texture2DArray of the staged pages (one draw call), every instance
## pooled. At most MAX_BURSTS explosions alive; past it only the residue. No lights.
## Driven by the event stream, read only: no fight function is called, no fight state written.

const POOL := 512
const MAX_BURSTS := 6
const MAX_FIREBALLS_NODES := 2           # x 2 casts each (fire_ball_fx's CASTS): past 4 alive, en_r_flame takes over
const FIREBALL_BURST_K := 0.41           # 0.55 of Matt's c75 burst (tighten_k 0.75 x 0.55)
const LIGHTNING_K := 0.55                # the strike drawn at 0.55 of its own impact scale (R-C9-360)
const TOWARD_CAM_M := 2.6
const PACK_DIR := "res://kc2/vfx_x/"
const PPM := 100.617553710938
const FB_END_PX := 520.0
const FB_HEAD_PX := 74.66
const FB_IMPACT_TICK := 18

const ATLAS := {"fire": "en_u_flame", "cold": "en_n_frost", "poison": "en_b_blight", "vitality": "en_v_void",
	"aether": "en_d_aether", "physical": "en_s_stone", "lightning": "en_q_storm"}
const AURA := {"fire": "en_u_flame/aura", "cold": "en_n_frost/aura", "vitality": "en_v_void/aura",
	"aether": "en_d_aether/aura", "physical": "en_o_bone/aura", "lightning": "en_d_aether/aura",
	"poison": "en_b_blight/ring_tele"}
const THROWN_WORDS: PackedStringArray = ["bomb", "grenade", "throw", "lob", "flask", "bottle", "vial", "molotov", "toss"]
enum { M_PREMUL, M_PALETTE, M_PREMUL_ADD, M_PALETTE_ADD, M_SPARK }

const SHADER := """
shader_type spatial;
render_mode unshaded, blend_premul_alpha, depth_draw_never, cull_disabled, shadows_disabled, ambient_light_disabled, fog_disabled;
uniform sampler2DArray pages : filter_linear, repeat_disable;
uniform vec4 pal[16];                 // 4 palettes x 4 bands, LINEAR (converted by the script)
varying flat vec4 v_c;                // page, mode, palette, fade
varying flat vec4 v_r;                // the frame's rect on its page (0..1)
float lin(float c) { return c <= 0.04045 ? c / 12.92 : pow((c + 0.055) / 1.055, 2.4); }
void vertex() {
	v_c = COLOR;
	v_r = INSTANCE_CUSTOM;
}
void fragment() {
	int mode = int(v_c.g + 0.5);
	vec3 rgb;
	float a;
	if (mode == 4) {
		// THE HIT SPARK (the one new piece): a four-point star with a hot core; v_r.x = age 0..1
		vec2 p = UV * 2.0 - 1.0;
		float s = 1.0 - v_r.x;
		float rays = max(exp(-abs(p.x) * 16.0) * exp(-abs(p.y) * 2.4), exp(-abs(p.y) * 16.0) * exp(-abs(p.x) * 2.4));
		float core = exp(-dot(p, p) * 18.0);
		a = clamp(rays + core, 0.0, 1.0) * s;
		vec3 c = mix(vec3(1.0, 0.72, 0.30), vec3(1.0, 0.98, 0.9), core);
		rgb = vec3(lin(c.r), lin(c.g), lin(c.b)) * a;
	} else {
		vec4 t = texture(pages, vec3(v_r.xy + UV * v_r.zw, v_c.r));
		if (mode == 0 || mode == 2) {
			rgb = vec3(lin(t.r), lin(t.g), lin(t.b));     // the pack is premultiplied sRGB (as fire_ball_fx's atlas)
			a = t.a;
		} else {
			// the cliffside kits' index palette (vfx_material_mix_unlit.gdshader): R picks one of four bands
			int band = int(floor(clamp(t.r, 0.0, 1.0) * 3.0 + 0.5));
			vec4 p = pal[int(v_c.b + 0.5) * 4 + band];
			a = t.a * p.a;
			rgb = p.rgb * a;
		}
	}
	rgb *= v_c.a;
	a *= v_c.a;
	ALBEDO = rgb;
	ALPHA = (mode == 2 || mode == 3) ? 0.0 : a;   // additive layers: colour added, nothing covered
}
"""

var mode = null
var cam: Camera3D = null
var mm: MultiMesh = null
var mmi: MultiMeshInstance3D = null
var mat: ShaderMaterial = null
var sets: Dictionary = {}
var pal_ids: Dictionary = {}
var ok := false
var free_slots: Array[int] = []
var parts: Array = []
var fxs: Array = []
var pending: Array = []
var cls_cache := {}
var fam_by := {}
var bursts_live := 0
var now := 0.0
var fireballs: Array = []
var _collapsed := Transform3D(Basis(Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3(0, -1000, 0))
var _spark_last := {}
var report := {"casts": 0, "by_cls": {}, "by_el": {}, "bursts": 0, "bursts_capped": 0, "peak_live": 0,
	"peak_bursts": 0, "player_hits": 0, "dropped_pool_full": 0, "fireballs": 0, "fireball_overflow": 0, "pack": ""}


func setup(p_mode) -> void:
	mode = p_mode
	cam = mode.scene.cam
	_build_families()
	if not _load_pack():
		push_warning("[arena] enemy vfx: pack not staged (python3 tools/arena_stage_vfx.py) -- " + String(report["pack"]))
		return
	var sh := Shader.new()
	sh.code = SHADER
	mat = ShaderMaterial.new()
	mat.shader = sh
	mat.render_priority = 126
	var quad := ArrayMesh.new()
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	# the unit quad, (0,0) the frame's TOP-left, y running DOWN the frame (the transform's y axis points down)
	arr[Mesh.ARRAY_VERTEX] = PackedVector3Array([Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(1, 1, 0), Vector3(0, 1, 0)])
	arr[Mesh.ARRAY_TEX_UV] = PackedVector2Array([Vector2(0, 0), Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)])
	arr[Mesh.ARRAY_INDEX] = PackedInt32Array([0, 1, 2, 0, 2, 3])
	quad.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	quad.surface_set_material(0, mat)
	mat.set_shader_parameter("pages", _pages)
	mat.set_shader_parameter("pal", _pal_array)
	mm = MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	mm.use_custom_data = true
	mm.mesh = quad
	mm.instance_count = POOL
	for i in POOL:
		mm.set_instance_transform(i, _collapsed)
		mm.set_instance_color(i, Color(0, 0, 0, 0))
		mm.set_instance_custom_data(i, Color(0, 0, 0, 0))
		free_slots.append(POOL - 1 - i)
	mmi = MultiMeshInstance3D.new()
	mmi.name = "EnemyVFX"
	mmi.multimesh = mm
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.custom_aabb = AABB(Vector3(-500, -100, -500), Vector3(1000, 200, 1000))
	add_child(mmi)
	# the speedy fireball: fire_ball_fx.gd itself
	for n in MAX_FIREBALLS_NODES:
		var fb = load("res://scripts/fire_ball_fx.gd").new()
		fb.name = "EnemyFireBall%d" % n
		fb.tighten = true
		add_child(fb)
		if fb.setup(mode.scene, cam):
			fb.mat.set_shader_parameter("tighten_k", FIREBALL_BURST_K)
			fb.warm_up()
			fireballs.append(fb)
		else:
			push_warning("[arena] enemy vfx: fire_ball_fx refused: " + str(fb.report))
	ok = true


var _pages: Texture2DArray = null
var _pal_array := PackedVector4Array()


func _load_pack() -> bool:
	var ip := ProjectSettings.globalize_path(PACK_DIR + "index.json")
	if not FileAccess.file_exists(ip):
		report["pack"] = "no " + ip
		return false
	var idx: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ip))
	var imgs: Array[Image] = []
	for pg in idx["pages"]:
		var fp := ProjectSettings.globalize_path(PACK_DIR + String(pg["file"]))
		var img := Image.load_from_file(fp)
		if img == null or img.is_empty():
			report["pack"] = "page " + fp
			return false
		img.convert(Image.FORMAT_RGBA8)
		imgs.append(img)
	_pages = Texture2DArray.new()
	_pages.create_from_images(imgs)
	var pn := 0
	_pal_array.resize(16)
	for k in (idx["palettes"] as Dictionary).keys():
		pal_ids[k] = pn
		var cols: Array = idx["palettes"][k]
		for b in 4:
			var c := Color(float(cols[b][0]), float(cols[b][1]), float(cols[b][2]), float(cols[b][3])).srgb_to_linear()
			_pal_array[pn * 4 + b] = Vector4(c.r, c.g, c.b, float(cols[b][3]))
		pn += 1
	sets = idx["sets"]
	report["pack"] = "%d sets, %d pages" % [sets.size(), imgs.size()]
	return true


## The damage families of every (record, slot), from the roster's damage rows (read once; keyed rec|kind|slot|).
func _build_families() -> void:
	var r = mode.session.fight.roster
	for dk in r.damage_by_slot.keys():
		var parts_k := String(dk).split("|")
		if parts_k.size() < 3:
			continue
		var key := parts_k[0] + "|" + parts_k[2]
		if not fam_by.has(key):
			fam_by[key] = {}
		for dr in r.damage_by_slot[dk]:
			if (dr as Dictionary).has("damage_type"):
				fam_by[key][String(dr["damage_type"])] = true


# ------------------------------------------------------------------------------------------------ classification
func classify(rec: String, slot_key: String) -> Dictionary:
	if cls_cache.has(slot_key):
		return cls_cache[slot_key]
	var entry := {}
	for s_any in mode.session.fight.roster.slots_for(rec):
		if String((s_any as Dictionary).get("_slot_key", "")) == slot_key:
			entry = s_any
			break
	var skill := String(entry.get("skill", ""))
	if skill == "" and slot_key.contains("|"):
		skill = slot_key.get_slice("|", slot_key.get_slice_count("|") - 1)
	var p := skill.to_lower()
	var nm := p.get_file()
	var ec := String(entry.get("extent_carrier", "")).to_lower()
	var fams: Dictionary = fam_by.get(rec + "|" + String(entry.get("slot", "")), {})
	var el := _element(fams, p)
	var dv: Variant = mode.session.fight.defer_velocity.get(skill, null)
	var melee_path := p.contains("/attackmelee/") or p.contains("/attackcharge/")
	var cls := "melee"
	if p.contains("/buffoffensive/") or p.contains("/buff/") or nm.contains("aura"):
		cls = "aura"
	elif dv != null or p.contains("attackprojectile") or p.contains("rangeddirect") \
			or ((ec.contains("projectile") or ec.begins_with("wave_")) and not melee_path):
		cls = "ranged"
		for w in THROWN_WORDS:
			if nm.contains(w):
				cls = "thrown"
				break
	elif p.contains("attackradius") or p.contains("/aoe/") or p.contains("attackrain") \
			or ((ec == "skill_target_radius" or ec == "skill_radius") and not melee_path):
		cls = "area"
	var was := cls
	if el == "lightning" and (cls == "ranged" or cls == "area"):
		cls = "bolt"
	var out := {"cls": cls, "was": was, "el": el, "v": float(dv) if dv != null else 0.0, "skill": nm}
	cls_cache[slot_key] = out
	return out


static func _element(fams: Dictionary, path: String) -> String:
	# the first non-physical family, in this order; else the path's words; else physical
	for pair in [["Lightning", "lightning"], ["Fire", "fire"], ["Cold", "cold"], ["Poison", "poison"],
			["Aether", "aether"], ["Chaos", "vitality"], ["Life", "vitality"], ["LifeLeech", "vitality"],
			["SlowPoison", "poison"], ["SlowFire", "fire"], ["SlowCold", "cold"], ["SlowLightning", "lightning"],
			["Elemental", "fire"]]:
		if fams.has(pair[0]):
			return pair[1]
	var n := path.get_file()
	for pair in [["lightning", "lightning"], ["storm", "lightning"], ["shock", "lightning"], ["fire", "fire"],
			["flame", "fire"], ["burn", "fire"], ["ember", "fire"], ["ice", "cold"], ["frost", "cold"],
			["cold", "cold"], ["freeze", "cold"], ["poison", "poison"], ["acid", "poison"], ["toxic", "poison"],
			["venom", "poison"], ["blight", "poison"], ["aether", "aether"], ["chaos", "vitality"],
			["void", "vitality"], ["blood", "vitality"], ["vitality", "vitality"], ["necro", "vitality"]]:
		if n.contains(pair[0]):
			return pair[1]
	return "physical"


# ------------------------------------------------------------------------------------------------ events
func on_cast_start(actor_id: int, t, slot_key: String, aim: Vector2) -> void:
	if not ok or t == null or t.dying:
		return
	var c := classify(String(t.record), slot_key)
	report["casts"] = int(report["casts"]) + 1
	report["by_cls"][c["cls"]] = int(report["by_cls"].get(c["cls"], 0)) + 1
	report["by_el"][c["el"]] = int(report["by_el"].get(c["el"], 0)) + 1
	var after := 0.0
	if t.has_method("swing_after_s"):
		after = float(t.swing_after_s())
	pending.append({"at": now + after, "actor": actor_id, "aim": aim, "c": c})


func on_player_hit(src_id: int, warlord) -> void:
	report["player_hits"] = int(report["player_hits"]) + 1
	if warlord != null and warlord.body != null and warlord.body.has_method("flash_red"):
		warlord.body.flash_red()
	if not ok or now - float(_spark_last.get(src_id, -9.0)) < 0.1:
		return
	_spark_last[src_id] = now
	var t = mode.actors.get(src_id, null)
	var cls := "melee"
	var el := "physical"
	if t != null and t.has_meta("vfx_last"):
		cls = String(t.get_meta("vfx_last")["cls"])
		el = String(t.get_meta("vfx_last")["el"])
	if cls != "melee" and el != "physical":
		return                          # the arrival already burst on him
	_spark(_player_chest())


# ------------------------------------------------------------------------------------------------ positions
func _actor_chest(t) -> Vector3:
	return mode.to_world(t.pos_m) + Vector3.UP * (float(t.true_height_m) * 0.55)


func _player_chest() -> Vector3:
	return mode.to_world(mode.player_pos_m) + Vector3.UP * 1.0


func _screen_angle(a: Vector3, b: Vector3) -> float:
	var sp := cam.unproject_position(b) - cam.unproject_position(a)
	return atan2(-sp.y, sp.x)


# ------------------------------------------------------------------------------------------------ the releases
func _release(pr: Dictionary) -> void:
	var t = mode.actors.get(int(pr["actor"]), null)
	var c: Dictionary = pr["c"]
	var from: Vector3
	var radius := 0.8
	var pos_m: Vector2
	if pr.has("from_m"):                       # the gallery's stand-in caster
		pos_m = pr["from_m"]
		from = mode.to_world(pos_m) + Vector3.UP * 1.1
	else:
		if t == null or t.dying:
			return
		t.set_meta("vfx_last", c)
		from = _actor_chest(t)
		radius = float(t.radius_m)
		pos_m = t.pos_m
	var el: String = c["el"]
	var to := _player_chest()
	var dist := Vector2(to.x - from.x, to.z - from.z).length()
	var lat := 0.0                              # the sim's own latency for a deferred skill, to the tick (KC2 CEIL)
	if float(c["v"]) > 0.0:
		var tps := float(mode.session.fight.ticks_per_s)
		lat = ceilf(dist / float(c["v"]) * tps) / tps
	match String(c["cls"]):
		"melee":
			var d := to - from
			d.y = 0.0
			var at := from + d.normalized() * maxf(radius, 0.5) * 0.6
			_play(ATLAS[el] + "/slash", at, {"ang": _screen_angle(from, to)})
		"ranged":
			if el == "fire" and _fire_ball(from, to, lat):
				return
			if el == "fire":
				report["fireball_overflow"] = int(report["fireball_overflow"]) + 1
			var aid: String = "en_r_flame" if el == "fire" else ATLAS[el]
			var dur := lat if lat > 0.0 else clampf(dist / 18.0, 0.12, 0.45)
			fxs.append({"kind": "missile", "el": el, "set": aid + "/bolt", "burst": aid + "/burst", "from": from,
				"t0": now, "dur": dur, "body": _play(aid + "/bolt", from, {"ang": _screen_angle(from, to), "life": dur + 0.05})})
		"bolt":
			_lightning(from, to if String(c.get("was", "")) != "area" else mode.to_world(pr["aim"]) + Vector3.UP * 0.9,
				lat, String(c.get("was", "")) == "area")
		"area":
			var g: Vector3 = mode.to_world(pr["aim"])
			_play(ATLAS[el] + "/ring_burst", g, {"ground": true})
			_explode(ATLAS[el], g + Vector3.UP * 0.8)
		"thrown":
			var dur2 := maxf(lat, 0.4)              # V45's flight: 0.4 s, apex 42 px
			fxs.append({"kind": "thrown", "el": el, "from": from, "t0": now, "dur": dur2,
				"body": _play("cocktail/flask", from, {"life": dur2 + 0.05, "k_w": 45.5})})
		"aura":
			fxs.append({"kind": "aura", "actor": int(pr["actor"]), "t0": now, "dur": 2.4,
				"body": _play(AURA[el], mode.to_world(pos_m), {"ground": true, "life": 2.4})})


## The speedy fireball (fire_ball_fx.gd, unmodified): its baked flight is FB_END_PX - FB_HEAD_PX long and lands on its
## tick 18. Aimed so the burst lands on him; timed so it lands on the sim's hit; from a caster closer than the flight,
## the first (1 - d / flight) of the flight is skipped (R-C9-376) so the ball starts AT the caster.
func _fire_ball(from: Vector3, to: Vector3, lat: float) -> bool:
	for fb in fireballs:
		var free := false
		for cst in fb.casts:
			if (cst as Dictionary).is_empty():
				free = true
				break
		if not free:
			continue
		var d := to - from
		d.y = 0.0
		var dist := d.length()
		var dir := d.normalized() if dist > 1e-3 else Vector3.RIGHT
		var socket := to - dir * (FB_END_PX / PPM)
		var b0 := 0
		var want_px := FB_END_PX - dist * PPM       # the travel dx at which the ball is at the caster
		if want_px > FB_HEAD_PX:
			for tr in fb.travel:
				if float(tr["dx"]) >= want_px:
					b0 = int(tr["tick"])
					break
		var arrive := float(FB_IMPACT_TICK - b0) / 60.0
		fxs.append({"kind": "fb", "fb": fb, "at": now + maxf(0.0, lat - arrive), "socket": socket, "dir": dir,
			"feet": Vector3(from.x, from.y - 1.1, from.z), "b0": b0, "fired": false, "t0": now, "dur": 99.0})
		report["fireballs"] = int(report["fireballs"]) + 1
		return true
	return false


## The cliffside lightning_blast: its cast flare at the caster, its travel (1400 px/s) to him, then its impact and
## additive glow (layers.glow: alpha 0.75, scale 1.35) and residual -- at LIGHTNING_K. Past the cap: en_q_storm.
func _lightning(from: Vector3, to: Vector3, lat: float, area: bool) -> void:
	if not area:
		_play("lightning_blast/cast", from, {"k": LIGHTNING_K})
		var speed := float(sets["lightning_blast/travel"].get("speed_px_s", 1400.0)) / PPM
		var dur := lat if lat > 0.0 else clampf(from.distance_to(to) / speed, 0.08, 0.6)
		fxs.append({"kind": "strike", "from": from, "t0": now, "dur": dur,
			"body": _play("lightning_blast/travel", from, {"ang": _screen_angle(from, to), "life": dur + 0.03})})
	else:
		_strike(to)          # an area strike: on the aim, now


func _strike(at: Vector3) -> void:
	if bursts_live >= MAX_BURSTS:
		report["bursts_capped"] = int(report["bursts_capped"]) + 1
		_play("en_q_storm/bolt", at, {"life": 0.3})
		return
	_play("lightning_blast/impact", at, {"k": LIGHTNING_K, "burst": true})
	var glow: Dictionary = sets["lightning_blast/layers"].get("glow", {})
	_play("lightning_blast/impact", at, {"k": LIGHTNING_K * float(glow.get("scale", 1.35)), "add": true,
		"fade": float(glow.get("alpha", 0.75)), "palette": "lightning_blast_add"})
	_play("lightning_blast/residual", at + Vector3.DOWN * 0.9, {"k": LIGHTNING_K,
		"squash": float(sets.get("lightning_blast/ground_squash", 0.6))})
	report["bursts"] = int(report["bursts"]) + 1


## An en_e2 explosion: `burst` (counted against the cap) and its `ring_smoke`; past the cap only the smoke (residue).
func _explode(aid: String, at: Vector3) -> void:
	if bursts_live < MAX_BURSTS:
		_play(aid + "/burst", at, {"burst": true, "k": _burst_k(aid)})
		report["bursts"] = int(report["bursts"]) + 1
	else:
		report["bursts_capped"] = int(report["bursts_capped"]) + 1
	if sets.has(aid + "/ring_smoke"):
		_play(aid + "/ring_smoke", at + Vector3.UP * 0.2, {})


## R-C9-360: an explosion at 0.5-0.6 of the fireball's (c75, ~3.8 m across) -- each element's own burst scaled down to
## BURST_D_M across where it is bigger (frost's and blight's are already smaller and stay as drawn)
const BURST_D_M := 2.1
var _bk := {}
func _burst_k(aid: String) -> float:
	if _bk.has(aid):
		return _bk[aid]
	var st: Dictionary = sets.get(aid + "/burst", {})
	var mw := 1.0
	for fr in (st.get("frames", []) as Array):
		if fr != null:
			mw = maxf(mw, float(fr["rect"][2]))
	var k := minf(1.0, BURST_D_M * float(st.get("ppm", PPM)) / mw)
	_bk[aid] = k
	return k


func _spark(at: Vector3) -> void:
	_add({"set": "", "mode": M_SPARK, "t0": now, "life": 0.18, "pos": at, "w": 0.95, "h": 0.95, "ang": randf() * TAU})


# ------------------------------------------------------------------------------------------------ composites
func _tick_fx(fx: Dictionary) -> bool:
	var s := (now - float(fx["t0"])) / float(fx["dur"])
	var to := _player_chest()
	match String(fx["kind"]):
		"fb":
			if not fx["fired"] and now >= float(fx["at"]):
				var fb = fx["fb"]
				var sock: Vector3 = fx["socket"]
				var g: int = fb.cast_started(func() -> Vector3: return sock, 2)
				fb.released(g, sock, fx["dir"], fx["feet"])
				if g >= 0 and int(fx["b0"]) > 0:
					fb.casts[g]["clock"] = float(fx["b0"]) / 60.0     # skip the head of the flight (caster closer)
				fx["fired"] = true
				return false
			return true
		"aura":
			var t = mode.actors.get(int(fx["actor"]), null)
			var b: Dictionary = fx["body"]
			if t != null and not b.is_empty():
				b["pos"] = mode.to_world(t.pos_m)
			return s < 1.0
		"missile", "strike", "thrown":
			var from: Vector3 = fx["from"]
			var sc := clampf(s, 0.0, 1.0)
			var p := from.lerp(to, sc)
			if String(fx["kind"]) == "thrown":
				p += Vector3.UP * (4.0 * (42.0 / PPM) * 3.0 * sc * (1.0 - sc))
			var b2: Dictionary = fx["body"]
			if not b2.is_empty():
				b2["pos"] = p
				if String(fx["kind"]) == "thrown":
					b2["ang"] = now * 11.0
				else:
					b2["ang"] = _screen_angle(from, to)
			if s < 1.0:
				return true
			match String(fx["kind"]):
				"strike":
					_strike(to)
				"missile":
					_explode(String(fx["burst"]).get_slice("/", 0), to)
				"thrown":
					_cocktail_land(String(fx["el"]), to)
			return false
		"licks":
			for lk in (fx["licks"] as Array):
				var q: Dictionary = lk
				if q.is_empty():
					continue
				# V45 _lick_sample: a damped narrow-band oscillator per lick -> scale 1 + 0.18 tanh(.), alpha ~0.7
				var hz := float(q["hz"])
				var v := sin(now * TAU * hz + float(q["seed"])) + 0.5 * sin(now * TAU * hz * 1.9 + float(q["seed"]) * 2.3)
				q["k"] = float(q["k0"]) * (1.0 + 0.18 * tanh(v * 0.9))
				q["fade"] = clampf(0.62 + 0.18 * v, 0.35, 0.9) * float((q["env"] as Callable).call(now - float(fx["t0"])))
			return s < 1.0
	return false


## V45's landing: fire -> the floor field (its palette; 2.5 s, eased in and out) + three flickering licks + a splash;
## poison -> blight ring; anything else -> mud burst.
func _cocktail_land(el: String, to: Vector3) -> void:
	var ground: Vector3 = mode.to_world(mode.player_pos_m)
	if el == "fire":
		var dur := 2.5
		var env := func(age: float) -> float: return clampf(age / 0.15, 0.0, 1.0) * clampf((dur - age) / 0.4, 0.0, 1.0)
		var field := _play("cocktail/field", ground + Vector3.UP * 0.05, {"k_w": 2.0 * 181.0, "squash": 0.58, "life": dur})
		var licks: Array = []
		for i in 3:
			var an := float(i) * TAU / 3.0 + randf() * 0.6
			var off := Vector3(cos(an), 0.0, sin(an)) * (181.0 / PPM) * 0.35
			var lk := _play("cocktail/pulse", ground + off + Vector3.UP * 0.35, {"k_w": 65.0, "life": dur, "ang": PI * 0.5})
			if not lk.is_empty():
				lk["hz"] = randf_range(3.3, 3.6)
				lk["seed"] = randf() * TAU
				lk["k0"] = lk["k"]
				lk["env"] = env
			licks.append(lk)
		fxs.append({"kind": "licks", "t0": now, "dur": dur, "licks": licks, "field": field})
		_explode("en_u_flame", to)
	elif el == "poison":
		_play("en_b_blight/ring_burst", ground, {"ground": true})
		_explode("en_b_blight", to)
	else:
		_explode("en_g_mud", to)


# ------------------------------------------------------------------------------------------------ the gallery
## `-- --arena-vfx-gallery`: the eye-check (captures/enemy_vfx/families.mp4) -- one example of every family, fired by
## a stand-in caster round him, one every GALLERY_STEP_S, captioned with the family and the asset it reuses.
const GALLERY_STEP_S := 1.6
var gallery: Array = []
var _g_i := 0
var _g_next := 1.0
var _g_label: Label = null


func start_gallery() -> void:
	var L := [["melee", "physical", "en_s_stone slash + spark"], ["melee", "fire", "en_u_flame slash + spark"],
		["ranged", "fire", "fire_ball_fx (cliffside e1_B)"], ["ranged", "fire", "fire_ball_fx, close caster", 2.5],
		["ranged", "cold", "en_n_frost bolt + burst"], ["ranged", "poison", "en_b_blight bolt + burst"],
		["ranged", "vitality", "en_v_void bolt + burst"], ["ranged", "aether", "en_d_aether bolt + burst"],
		["ranged", "physical", "en_s_stone bolt + burst"], ["bolt", "lightning", "cliffside lightning_blast"],
		["area", "fire", "en_u_flame ring_burst + burst"], ["area", "cold", "en_n_frost ring_burst + burst"],
		["thrown", "fire", "V45 Blackwater cocktail"], ["thrown", "physical", "flask -> en_g_mud burst"],
		["aura", "aether", "en_d_aether aura"], ["aura", "poison", "en_b_blight ring_tele"]]
	for e in L:
		gallery.append({"c": {"cls": e[0], "el": e[1], "v": 0.0, "skill": "gallery"}, "label": e[2],
			"r": float(e[3]) if e.size() > 3 else 6.0})
	var cl := CanvasLayer.new()
	cl.layer = 6
	add_child(cl)
	_g_label = Label.new()
	_g_label.add_theme_font_size_override("font_size", 34)
	_g_label.add_theme_color_override("font_color", Color(1, 1, 1))
	_g_label.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	_g_label.add_theme_constant_override("outline_size", 8)
	_g_label.position = Vector2(24, 24)
	cl.add_child(_g_label)


func _gallery_tick() -> void:
	if gallery.is_empty() or now < _g_next or _g_i >= gallery.size():
		return
	var e: Dictionary = gallery[_g_i]
	var c: Dictionary = e["c"]
	_g_next = now + GALLERY_STEP_S * (2.0 if String(c["cls"]) in ["aura", "thrown"] else 1.0)
	var ang := PI + float(_g_i % 3 - 1) * 0.5           # from his left, the sun's side
	var r: float = 1.6 if String(c["cls"]) == "melee" else float(e["r"])
	var from_m: Vector2 = mode.player_pos_m + Vector2(cos(ang), sin(ang)) * r
	_release({"actor": -1, "from_m": from_m, "aim": mode.player_pos_m, "c": c})
	if String(c["cls"]) == "melee":
		pending.append({"at": now + 0.15, "actor": -1, "hit_src": true, "c": c})
	_g_label.text = "%s / %s  -  %s" % [c["cls"], c["el"], e["label"]]
	_g_i += 1


# ------------------------------------------------------------------------------------------------ the frame
func _process(delta: float) -> void:
	now += delta
	if not ok or mode == null or mode.session == null:
		return
	_gallery_tick()
	var i := 0
	while i < pending.size():
		var pr: Dictionary = pending[i]
		if now >= float(pr["at"]):
			pending.remove_at(i)
			if pr.has("hit_src"):
				on_player_hit(-1, mode.warlord)
			else:
				_release(pr)
		else:
			i += 1
	var j := 0
	while j < fxs.size():
		if _tick_fx(fxs[j]):
			j += 1
		else:
			fxs.remove_at(j)
	var basis := cam.global_transform.basis
	var rgt := basis.x.normalized()
	var up := basis.y.normalized()
	var back := basis.z.normalized()
	var k := 0
	var live_b := 0
	while k < parts.size():
		var q: Dictionary = parts[k]
		var age := now - float(q["t0"])
		if age >= float(q["life"]):
			_free(q)
			parts.remove_at(k)
			continue
		if bool(q.get("burst", false)):
			live_b += 1
		_write(q, age, rgt, up, back)
		k += 1
	bursts_live = live_b
	report["peak_live"] = maxi(int(report["peak_live"]), parts.size())
	report["peak_bursts"] = maxi(int(report["peak_bursts"]), live_b)


## One instance of a staged set: plays its frames (fps, or the cliffside kits' hold frames at 60/s), once or looping.
func _play(set_id: String, pos: Vector3, opt: Dictionary) -> Dictionary:
	if not sets.has(set_id):
		return {}
	var st: Dictionary = sets[set_id]
	var frames: Array = st["frames"]
	var life := 0.0
	if st.has("holds_60"):
		for h in (st["holds_60"] as Array):
			life += float(h) / 60.0
	else:
		life = float(frames.size()) / maxf(float(st.get("fps", 20.0)), 1.0)
	var k := float(opt.get("k", 1.0))
	if opt.has("k_w"):                                  # a cliffside still sized by its used width in px
		k = float(opt["k_w"]) / maxf(float(st.get("used_w", 1.0)), 1.0)
	var q := {"set": set_id, "mode": M_PREMUL if String(st["mode"]) == "premul" else M_PALETTE, "t0": now,
		"life": float(opt.get("life", life)), "pos": pos, "k": k, "ang": float(opt.get("ang", 0.0)),
		"ground": bool(opt.get("ground", String(st.get("plane", "")) == "ground")), "squash": float(opt.get("squash", 1.0)),
		"fade": float(opt.get("fade", 1.0)), "burst": bool(opt.get("burst", false)),
		"pal": pal_ids.get(str(opt.get("palette", st.get("palette", ""))), 0)}
	if bool(opt.get("add", false)):
		q["mode"] = M_PALETTE_ADD if q["mode"] == M_PALETTE else M_PREMUL_ADD
	return _add(q)


func _add(q: Dictionary) -> Dictionary:
	if free_slots.is_empty():
		report["dropped_pool_full"] = int(report["dropped_pool_full"]) + 1
		return {}
	q["i"] = free_slots.pop_back()
	parts.append(q)
	return q


func _free(q: Dictionary) -> void:
	var i := int(q["i"])
	mm.set_instance_transform(i, _collapsed)
	mm.set_instance_color(i, Color(0, 0, 0, 0))
	free_slots.append(i)


func _frame_of(st: Dictionary, age: float) -> int:
	var n := (st["frames"] as Array).size()
	if st.has("holds_60"):
		var tick := int(age * 60.0)
		var hs: Array = st["holds_60"]
		var total := 0
		for h in hs:
			total += int(h)
		if bool(st.get("loop", false)):
			tick = tick % maxi(total, 1)
		var acc := 0
		for fi in hs.size():
			acc += int(hs[fi])
			if tick < acc:
				return fi
		return n - 1
	var f := int(age * float(st.get("fps", 20.0)))
	return f % n if bool(st.get("loop", false)) else mini(f, n - 1)


func _write(q: Dictionary, age: float, rgt: Vector3, up: Vector3, back: Vector3) -> void:
	var i := int(q["i"])
	var at: Vector3 = q["pos"]
	if int(q["mode"]) == M_SPARK:
		var an := float(q["ang"])
		var ex := (rgt * cos(an) + up * sin(an)) * float(q["w"])
		var ey := -(-rgt * sin(an) + up * cos(an)) * float(q["h"])
		mm.set_instance_transform(i, Transform3D(Basis(ex, ey, back * 0.01), at - ex * 0.5 - ey * 0.5 + back * TOWARD_CAM_M))
		mm.set_instance_color(i, Color(0, M_SPARK, 0, 1.0))
		mm.set_instance_custom_data(i, Color(age / float(q["life"]), 0, 0, 0))
		return
	var st: Dictionary = sets[q["set"]]
	var fr = (st["frames"] as Array)[_frame_of(st, age)]
	if fr == null:
		mm.set_instance_transform(i, _collapsed)
		return
	var page := int(fr["page"])
	var rect: Array = fr["rect"]
	var off: Array = fr["off"]
	var s := float(q["k"]) / float(st.get("ppm", PPM))
	var w := float(rect[2]) * s
	var h := float(rect[3]) * s
	var ox := float(off[0]) * s
	var oy := float(off[1]) * s
	var b: Basis
	var origin: Vector3
	if bool(q["ground"]):
		var rg := Vector3(rgt.x, 0.0, rgt.z).normalized()
		var bg := Vector3(back.x, 0.0, back.z).normalized()       # the frame's "down" = toward the camera on the ground
		b = Basis(rg * w, bg * h, Vector3.UP * 0.01)
		origin = at + rg * ox + bg * oy + Vector3.UP * 0.06 + back * 0.3
	else:
		var an := float(q["ang"])
		var r2 := rgt * cos(an) + up * sin(an)
		var u2 := -rgt * sin(an) + up * cos(an)
		var sq := float(q["squash"])
		b = Basis(r2 * w, -u2 * h * sq, back * 0.01)
		origin = at + r2 * ox - u2 * oy * sq + back * TOWARD_CAM_M
	mm.set_instance_transform(i, Transform3D(b, origin))
	mm.set_instance_color(i, Color(float(page), float(q["mode"]), float(q["pal"]), float(q["fade"])))
	var pp := 4096.0
	mm.set_instance_custom_data(i, Color(float(rect[0]) / pp, float(rect[1]) / pp, float(rect[2]) / pp, float(rect[3]) / pp))
