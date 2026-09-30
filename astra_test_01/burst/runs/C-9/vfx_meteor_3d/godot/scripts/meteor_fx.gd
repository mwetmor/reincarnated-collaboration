extends Node3D
class_name MeteorFx
## C-9 -- HER METEOR, BUILT 3D FIRST (the VFX bake-off's lane B, vfx_meteor_3d; accepted). drax.
##
## ON HER PAINTED PAGE BEHIND ?meteor=b (desktop: -- --c sorceress --meteor b). barrow_full asks wanted()
## before it builds anything -- so the painted surfaces carry the ground terms (PaintedWorld.with_fx) and
## the characters' ramp the fire (PaintStack.with_char_fire) -- and calls attach() once the scene is built.
## Without ?meteor=b none of this exists and the page is exactly as before.
##
##   CALL   at her release (casts.cast_meteor.release_s in her package): a flare of flame tongues at her
##          staff crown, its light on her, and lane A's PAINTED target ring on the ground AHEAD m ahead.
##   FALL   FALL_S: a burning rock in a corona with a torn trail comes down OUT OF THE SUN -- along the
##          Barrow's own sun ray onto the target -- so its shadow stays pinned on the ring and GROWS AND
##          SHARPENS as it lands (an area-light shadow: PaintedWorld's fx_occlusion) while the rock closes
##          on it. At this orthographic camera a fall and a slide toward the camera are the same screen
##          motion; the shadow meeting the rock, and the warm pool tightening under it, say "height".
##   IMPACT a flash, a crown of hooked flame tongues squashing into the ground and rising, torn flame
##          scraps flung out, the fire's light spiking on him and her and on the painted snow, a 7 px shake.
##   BURN   BURN_S: lane A's PAINTED burning ground carries it, burning down plane by plane from its outer
##          planes in; the 3D crown dies within the first second.
##
## THE LOOK: rock, trail and burst are the value-index vocabulary as a STEPPED four-plane shader on 3D
## geometry (the plane index is the surface's facing, broken by a noise flowing along each tongue, cut into
## the kit palette); the two ground marks are lane A's paintings, worn through the fixed camera as the Barrow
## wears its own. The pen draws the 3D silhouettes. No sparks, no smoke: torn scraps.
##
## PERFORMANCE (R-C9-89): everything is built ONCE at attach and pooled (POOL instances, round-robin);
## every material is drawn once at load, invisible (warm = 1 discards every fragment). Nothing is
## instantiated, freed or loaded at cast. The ground terms and the fire's light on the characters are
## GLOBAL UNIFORMS read by shaders that already draw: no light node, no light list, no variant to meet at
## cast time, no shadow. At the impact's peak the effect adds 3-4 meshes (burst, flash, scraps, the comet's
## last frame).

const PAL := [Color(0.25, 0.08, 0.04), Color(0.70, 0.16, 0.08), Color(1.0, 0.55, 0.12), Color(1.0, 0.94, 0.75)]
const FX_LAYER := 1 << 12            # the effect's own layer: no light, no shadow map touches it
const POOL := 2
const AHEAD := 3.5
const T_FALL0 := 0.12                # the fall starts under the flare
const FALL_S := 0.70
const T_IMPACT := T_FALL0 + FALL_S
const BURN_S := 3.0
const FALL_L := 12.0                 # metres along the sun ray (9.8 m up)
const ROCK_R := 0.34
const SHADOW_R := 0.5                # the occluder the shadow is cast by: the rock and its densest fire
const SUN_ANG_R := 0.075             # the sun's angular radius for the rock's shadow (4.3 deg: exaggerated
                                     # ~9x so the grow-and-sharpen reads inside 0.7 s)
const RING_R := 1.05
const BURN_R := 1.25
const SCRAPS := 28
const CROWN_SOCKET := "main_tip"     # the conductor: the call is at her staff crown
const PLATES_DIR := "res://data/meteor/"
const RING_HALF_W_M := 1.1           # lane A's painted ring, laid on the ground this wide either side
const POOL_HALF_W_M := 1.3           # its painted burning ground
const FIRE_COL := Color(1.0, 0.62, 0.30)   # the fire's light (sRGB); its range per phase below
const PPM := 100.617553710938

const FIRE_COMMON := """
uniform vec3 pal0 : source_color = vec3(0.25, 0.08, 0.04);
uniform vec3 pal1 : source_color = vec3(0.70, 0.16, 0.08);
uniform vec3 pal2 : source_color = vec3(1.00, 0.55, 0.12);
uniform vec3 pal3 : source_color = vec3(1.00, 0.94, 0.75);
uniform sampler2D noise_tex : filter_linear_mipmap, repeat_enable;
uniform float fx_time = 0.0;
uniform float heat = 0.0;       // moves every plane toward the core (+) or the rim (-)
uniform float erode = 0.0;      // the hard cut: what falls under it is torn away
uniform float warm = 0.0;       // 1: the load-time draw -- the pipeline is built, nothing is seen
uniform float noise_amp = 0.62;
uniform float flow = 1.4;       // the noise's run along the flame, per second
uniform float mark = 1.0;       // the pen's mark channel: 1.0 is the world's (the full pen)

// FOUR FLAT PLANES, HARD-EDGED: one pixel of anti-aliasing on each edge, nothing more
vec3 fire_planes(float v) {
	float w = max(fwidth(v), 1e-4) * 0.75;
	vec3 c = mix(pal0, pal1, smoothstep(0.30 - w, 0.30 + w, v));
	c = mix(c, pal2, smoothstep(0.48 - w, 0.48 + w, v));
	return mix(c, pal3, smoothstep(0.68 - w, 0.68 + w, v));
}
"""

const RENDER := "render_mode unshaded, cull_disabled, depth_draw_opaque, shadows_disabled, fog_disabled, specular_disabled;\n"

# THE TONGUES: the impact's crown and the call's flare (UV.x = along the tongue, UV.y = round it,
# UV2 = (the tongue's angle / tau, its base radius): each grows from its own base)
const TONGUE_SHADER := "shader_type spatial;\n" + RENDER + FIRE_COMMON + """
uniform float grow = 1.0;
uniform float spread = 1.0;
uniform float squash = 1.0;
uniform float wobble = 0.05;
uniform float stagger = 0.4;
varying float v_t;
varying float v_seed;
float hash1(float x) { return fract(sin(x * 91.3458 + 7.13) * 47453.5453); }
void vertex() {
	v_t = UV.x;
	v_seed = hash1(UV2.x * 17.0);
	float phi = UV2.x * 6.2831853;
	vec2 base = vec2(cos(phi), sin(phi)) * UV2.y;
	float g = max(grow * mix(1.0, 0.6 + 0.8 * v_seed, stagger), 0.0);
	vec3 p = VERTEX;
	p.xz = base + (p.xz - base) * g * spread;
	p.y *= g;
	float t2 = UV.x * UV.x;
	p.x += sin(fx_time * 8.0 + v_seed * 40.0) * wobble * t2 * g;
	p.z += cos(fx_time * 6.7 + v_seed * 57.0) * wobble * t2 * g;
	p.y *= squash;
	p.xz *= inversesqrt(max(squash, 0.25));
	VERTEX = p;
}
void fragment() {
	if (warm > 0.5) { discard; }
	float facing = abs(NORMAL.z);
	float nz = texture(noise_tex, vec2(UV.y * 2.0 + v_seed * 5.3, UV.x * 1.2 - fx_time * flow + v_seed * 3.1)).r;
	float v = facing * 0.85 + (nz - 0.5) * noise_amp - v_t * 0.5 + heat + 0.12;
	if (v < 0.12 + erode * (0.7 + 0.6 * v_seed)) { discard; }
	ALBEDO = fire_planes(v);
	ROUGHNESS = mark;
}
"""

# THE COMET: the rock's corona and its trail, one surface of revolution round local +Z (the travel);
# UV.x runs 0 at the front pole to 1 at the tail's tip; the tail is built 1 m long and stretched here
const COMET_SHADER := "shader_type spatial;\n" + RENDER + FIRE_COMMON + """
uniform float tail_len = 2.5;
uniform float cap_off = -0.3;
uniform float tongue_amp = 1.25;
varying float v_s;
void vertex() {
	float s = UV.x;
	v_s = s;
	vec3 p = VERTEX;
	if (p.z < cap_off) { p.z = cap_off + (p.z - cap_off) * tail_len; }
	// the tail's tongues: the surface pushed out and in by the flowing noise, more toward the tip
	float nz = textureLod(noise_tex, vec2(UV.y * 2.0, s * 1.7 - fx_time * flow), 0.0).r;
	vec2 rad = normalize(NORMAL.xy + vec2(1e-5, 0.0));
	p.xy += rad * (nz - 0.42) * tongue_amp * smoothstep(0.04, 0.5, s) * (length(VERTEX.xy) + 0.06);
	VERTEX = p;
}
void fragment() {
	if (warm > 0.5) { discard; }
	float facing = abs(NORMAL.z);
	float nz = texture(noise_tex, vec2(UV.y * 3.0 + 0.37, v_s * 2.4 - fx_time * flow * 1.3)).r;
	float v = facing * 0.8 + (nz - 0.5) * noise_amp - v_s * 0.6 + heat + 0.28;
	// the tail tears: its last third is cut through by the noise
	if (v < 0.12 + erode + smoothstep(0.55, 1.0, v_s) * 0.2) { discard; }
	ALBEDO = fire_planes(v);
	ROUGHNESS = mark;
}
"""

# THE FLASH: a lumpy shell, expanding and burning away in a few frames
const SHELL_SHADER := "shader_type spatial;\n" + RENDER + FIRE_COMMON + """
uniform float lump = 0.3;
void vertex() {
	float nz = textureLod(noise_tex, vec2(UV.y * 2.0, UV.x * 1.5 - fx_time * 2.0), 0.0).r;
	VERTEX += NORMAL * (nz - 0.5) * lump;
}
void fragment() {
	if (warm > 0.5) { discard; }
	float facing = abs(NORMAL.z);
	float nz = texture(noise_tex, vec2(UV.y * 3.0, UV.x * 2.0 - fx_time * 3.0)).r;
	float v = facing * 0.9 + (nz - 0.5) * noise_amp + heat;
	if (v < 0.12 + erode) { discard; }
	ALBEDO = fire_planes(v);
	ROUGHNESS = mark;
}
"""

# THE TORN SCRAPS: one MultiMesh; each instance's heat, cut and seed in INSTANCE_CUSTOM
# (no vertex COLOR is read: Compatibility reads a MultiMesh's vertex colour as black without
# instance colours -- the heather's trap)
const SCRAP_SHADER := "shader_type spatial;\n" + RENDER + FIRE_COMMON + """
varying float v_t;
varying float v_heat;
varying float v_cut;
varying float v_seed;
void vertex() {
	v_t = UV.x;
	v_heat = INSTANCE_CUSTOM.x;
	v_cut = INSTANCE_CUSTOM.y;
	v_seed = INSTANCE_CUSTOM.z;
}
void fragment() {
	if (warm > 0.5) { discard; }
	float facing = abs(NORMAL.z);
	float nz = texture(noise_tex, vec2(UV.y * 2.0 + v_seed * 7.0, UV.x - fx_time * flow + v_seed)).r;
	float v = facing * 0.85 + (nz - 0.5) * noise_amp - abs(v_t - 0.45) * 0.55 + v_heat + 0.18;
	if (v < 0.12 + v_cut) { discard; }
	ALBEDO = fire_planes(v);
	ROUGHNESS = mark;
}
"""

# THE ROCK: craggy facets, two stone planes by the sun, and hot seams between the facets
# (UV2 = the facet's barycentric coordinates)
const ROCK_SHADER := "shader_type spatial;\n" + RENDER + """
uniform vec3 stone_lit : source_color = vec3(0.25, 0.08, 0.04);
uniform vec3 stone_dark : source_color = vec3(0.113, 0.082, 0.067);
uniform vec3 seam_hot : source_color = vec3(1.00, 0.55, 0.12);
uniform vec3 seam_core : source_color = vec3(1.00, 0.94, 0.75);
uniform vec3 to_sun = vec3(0.0, 1.0, 0.0);
uniform float warm = 0.0;
uniform float mark = 1.0;
varying vec3 v_wn;
void vertex() { v_wn = (MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz; }
void fragment() {
	if (warm > 0.5) { discard; }
	vec3 b = vec3(UV2.x, UV2.y, 1.0 - UV2.x - UV2.y);
	float edge = min(b.x, min(b.y, b.z));
	vec3 c = dot(normalize(v_wn), to_sun) > 0.2 ? stone_lit : stone_dark;
	float w = max(fwidth(edge), 1e-4);
	c = mix(seam_hot, c, smoothstep(0.07 - w, 0.07 + w, edge));
	c = mix(seam_core, c, smoothstep(0.025 - w, 0.025 + w, edge));
	ALBEDO = c;
	ROUGHNESS = mark;
}
"""

var scene                              # barrow_full
var her                                # her knight.gd node
var cam: Camera3D
var sockets := {}
var sun: DirectionalLight3D
var noise: Texture2D
var style := "plates"                  # "plates" (lane A's painted ring and burning ground) or "procedural"
var plates: ImageTexture
var plates_rep := {}
var _ring_half_uv := 0.48              # the plates' content half-widths (data/meteor/manifest.json)
var _pool_half_uv := 0.48
var pool: Array = []
var _next := 0
var _owner := -1                       # the pool slot the ground terms follow
var _clock := 0.0
var shake_px := Vector2.ZERO           # applied to the camera's offsets (h_offset / v_offset), never its transform
var _shake_t := -1.0
var enabled := true                    # false: casts are ignored (a measurement's control run)
var report := {"casts": [], "impacts": []}
var last_update_us := 0                # this node's own CPU time in its last _process
var warmed := false
var _shaders := {}
var _to_sun := Vector3.UP
var _globals_on := false
var _fx_on_value := 2.0
# THE SWAP: every painted surface's and every character's material, with its own shader and the Meteor's
# variant of it (PaintedWorld.with_fx / PaintStack.with_char_fire), made at load; the variant is IN only
# while a Meteor is alive. Idle, the page draws exactly the shaders it draws without ?meteor=b -- a shader
# carrying the terms cost ~1.5 ms a frame on the desktop with its branch never taken (lane B's first A/B).
var _swaps: Array = []                 # [{mat, plain, fx, kind}]
var _fx_cache := {}                    # plain Shader -> its variant
var _fx_live := false
var swap_report := {}


static func wanted(sc) -> bool:
	"""HER PAINTED PAGE WITH ?meteor=b (desktop: -- --meteor b). barrow_full asks before it builds anything."""
	if not bool(sc.painted) or String(sc._character_choice()) != "sorceress":
		return false
	var q := PaintStack.web_query("meteor")
	var args := OS.get_cmdline_user_args()
	var i := args.find("--meteor")
	if q == "" and i >= 0 and i + 1 < args.size():
		q = String(args[i + 1])
	return q.to_lower() == "b"


static func attach(sc) -> Node3D:
	"""Build the Meteor into the scene (once, at load), then warm and arm it over the next frames."""
	var fx = load("res://scripts/meteor_fx.gd").new()
	fx.name = "MeteorFx"
	sc.add_child(fx)
	fx._attach(sc)
	return fx


func _attach(sc) -> void:
	scene = sc
	her = sc.knight
	cam = sc.cam
	sun = sc.sun
	noise = sc.fbm
	process_priority = 10              # after the scene has aimed its camera: the shake is on top
	var st := PaintStack.web_query("meteor_style")
	var args := OS.get_cmdline_user_args()
	var ai := args.find("--meteor-style")
	if st == "" and ai >= 0 and ai + 1 < args.size():
		st = String(args[ai + 1])
	style = "procedural" if st == "procedural" else "plates"
	_fx_on_value = 2.0 if style == "plates" else 1.0
	sockets = sc._read_json("res://data/sockets_sorceress.json")
	# HER RELEASE, from her package (spell_fx's source): the chop slot's cast
	var casts: Dictionary = her.cfg.get("casts", {})
	for clip in casts:
		if not String(clip).begins_with("_") and typeof(casts[clip]) == TYPE_DICTIONARY and String(casts[clip].get("slot", "")) == "chop":
			release_s = float(casts[clip]["release_s"])
			report["release"] = {"clip": String(clip), "release_s": release_s}
	# THE PLACEHOLDER METEOR OFF (spell_fx keeps the Fire Ball)
	var placeholder := "absent"
	var fire_ball := "absent"
	if sc.spell_fx != null and "casts_by_slot" in sc.spell_fx:
		if sc.spell_fx.casts_by_slot.has("chop"):
			sc.spell_fx.casts_by_slot.erase("chop")
			placeholder = "off"
		fire_ball = "kept" if sc.spell_fx.casts_by_slot.has("attack") else "absent"
	report["placeholder_meteor"] = placeholder
	report["fire_ball"] = fire_ball
	# NO SCENE LIGHT REACHES THE EFFECT'S LAYER (unshaded; on Compatibility a lit layer would also pay for
	# the shadowed suns' additive passes)
	sun.light_cull_mask &= ~FX_LAYER
	if sc.paint_sun != null:
		sc.paint_sun.light_cull_mask &= ~FX_LAYER
	_setup()
	_load_plates()
	collect_materials()
	var lab = sc.get_node_or_null(^"FxLabel")
	if lab != null:
		for c in lab.get_children():
			if c is Label:
				(c as Label).text = "METEOR: 3D (LANE B)  ·  FIRE BALL: PLACEHOLDER"
	_arm()


func _load_plates() -> void:
	"""Lane A's two painted plates, off their raw bytes (a PNG named .bin: never imported), sha-checked
	against data/meteor/manifest.json, onto every material built with the ground terms."""
	var mpath := PLATES_DIR + "manifest.json"
	var man = JSON.parse_string(FileAccess.get_file_as_string(mpath)) if FileAccess.file_exists(mpath) else null
	if typeof(man) != TYPE_DICTIONARY:
		plates_rep = {"error": "no manifest"}
		return
	_ring_half_uv = float(man["ring"]["content_half_w_uv"])
	_pool_half_uv = float(man["pool"]["content_half_w_uv"])
	var path := PLATES_DIR + String(man["plates"]["file"])
	var r := {"path": path}
	if FileAccess.file_exists(path):
		var bytes := FileAccess.get_file_as_bytes(path)
		var ctx := HashingContext.new()
		ctx.start(HashingContext.HASH_SHA256)
		ctx.update(bytes)
		r["sha256_ok"] = ctx.finish().hex_encode() == String(man["plates"]["sha256"])
		var img := Image.new()
		if img.load_png_from_buffer(bytes) == OK:
			img.generate_mipmaps()
			plates = ImageTexture.create_from_image(img)
			r["px"] = [img.get_width(), img.get_height()]
		else:
			r["error"] = "decode"
	else:
		r["error"] = "missing"
	plates_rep = r


func collect_materials() -> void:
	"""Every painted surface's and every character's ramp material under the scene, each with its Meteor
	variant (one per distinct shader, derived from the LIVE code). Call again after adding a character."""
	var n := {"painted": 0, "snow": 0, "heather": 0, "char": 0, "shaders": 0}
	var seen := {}
	for e in _swaps:
		seen[e["mat"]] = true
	for pair in PaintStack._materials_under(scene):
		var sm := pair[1] as ShaderMaterial
		if sm == null or sm.shader == null or seen.has(sm):
			continue
		var code: String = sm.shader.code
		var kind := ""
		if code.contains("uniform float his_shadow_on"):
			if code.contains("uniform float trail_relief_only"):
				kind = "snow"
			elif code.contains("uniform float painted_mark"):
				kind = "painted"
			elif code.contains("uniform bool id_white"):
				kind = "heather"
		elif code.contains("uniform float char_mark = 0.5;") and code.contains("void light()"):
			kind = "char"
		if kind == "":
			continue
		if not _fx_cache.has(sm.shader):
			var fx := Shader.new()
			fx.code = PaintStack.with_char_fire(code) if kind == "char" else PaintedWorld.with_fx(code, kind, style)
			_fx_cache[sm.shader] = fx
			n["shaders"] += 1
		if kind != "char" and plates != null:
			sm.set_shader_parameter("fx_plates", plates)
		_swaps.append({"mat": sm, "plain": sm.shader, "fx": _fx_cache[sm.shader], "kind": kind})
		seen[sm] = true
		n[kind] += 1
	for k in n:
		swap_report[k] = int(swap_report.get(k, 0)) + int(n[k])
	if _fx_live:
		_fx_shaders(true)


func _fx_shaders(on: bool) -> void:
	for e in _swaps:
		var m: ShaderMaterial = e["mat"]
		m.shader = e["fx"] if on else e["plain"]
		if on and e["kind"] != "char" and plates != null:
			m.set_shader_parameter("fx_plates", plates)
	_fx_live = on


func _arm() -> void:
	await get_tree().process_frame
	await warm_up(her.global_position)
	var line := "style=%s plates_sha_ok=%s fx_materials=%d warmed=%s warm_ms=%s release_s=%s placeholder_meteor=%s fire_ball=%s pool=%d fx_layer_unlit=%s" % [
		style, str(plates_rep.get("sha256_ok", false)), _swaps.size(), str(warmed),
		str(report.get("warm_ms")), str(release_s), String(report.get("placeholder_meteor")),
		String(report.get("fire_ball")), POOL, str((sun.light_cull_mask & FX_LAYER) == 0)]
	line += " swaps=%s" % JSON.stringify(swap_report)
	report["armed"] = line
	print("[meteor_b] armed " + line)


func _setup() -> void:
	_to_sun = sun.global_transform.basis.z.normalized()
	for key in ["tongue", "comet", "shell", "scrap", "rock"]:
		var code: String = {"tongue": TONGUE_SHADER, "comet": COMET_SHADER, "shell": SHELL_SHADER,
			"scrap": SCRAP_SHADER, "rock": ROCK_SHADER}[key]
		if PaintStack.is_compatibility():
			# THE WEB PEN READS THE STENCIL (PaintStack.STENCIL_*): the fire writes class 0, the full pen,
			# or a flame drawn over the snow (class 2) would keep the snow's "no pen"
			code = PaintStack.stencil_write(code, 0)
		var sh := Shader.new()
		sh.code = code
		_shaders[key] = sh
	var burst_mesh := _burst_mesh()
	var flare_mesh := _flare_mesh()
	var comet_mesh := _comet_mesh()
	var shell_mesh := _ico_mesh(2, 1.0, 0.0)
	var rock_mesh := _rock_mesh()
	var scrap_mesh := _scrap_mesh()
	for i in POOL:
		pool.append(_make_slot(i, burst_mesh, flare_mesh, comet_mesh, shell_mesh, rock_mesh, scrap_mesh))
	RenderingServer.global_shader_parameter_set("fx_web", 1.0 if PaintStack.is_compatibility() else 0.0)
	RenderingServer.global_shader_parameter_set("fx_sun", Vector4(_to_sun.x, _to_sun.y, _to_sun.z, SUN_ANG_R))
	RenderingServer.global_shader_parameter_set("fx_on", 0.0)
	_char_light(Vector3.ZERO, 0.0, 7.0)
	report["setup"] = {"pool": POOL, "shaders": _shaders.size(), "to_sun": [snappedf(_to_sun.x, 1e-3),
		snappedf(_to_sun.y, 1e-3), snappedf(_to_sun.z, 1e-3)], "sun_ang_r_rad": SUN_ANG_R,
		"compat_stencil_write": PaintStack.is_compatibility(),
		"tris": {"burst": _tris(burst_mesh), "flare": _tris(flare_mesh), "comet": _tris(comet_mesh),
			"shell": _tris(shell_mesh), "rock": _tris(rock_mesh), "scrap_each": _tris(scrap_mesh)}}


func _tris(m: ArrayMesh) -> int:
	var n := m.surface_get_array_index_len(0)
	return (n if n > 0 else m.surface_get_array_len(0)) / 3


func _mat(key: String, params := {}) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shaders[key]
	if key != "rock":
		m.set_shader_parameter("noise_tex", noise)
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m


func _mi(mesh: Mesh, mat: Material, nm: String, parent: Node3D) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = nm
	mi.mesh = mesh
	mi.material_override = mat
	mi.layers = FX_LAYER
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.gi_mode = GeometryInstance3D.GI_MODE_DISABLED
	mi.visible = false
	parent.add_child(mi)
	return mi


func _make_slot(i: int, burst_mesh: ArrayMesh, flare_mesh: ArrayMesh, comet_mesh: ArrayMesh,
		shell_mesh: ArrayMesh, rock_mesh: ArrayMesh, scrap_mesh: ArrayMesh) -> Dictionary:
	var root := Node3D.new()
	root.name = "Meteor_%d" % i
	add_child(root)
	var s := {"i": i, "root": root, "active": false, "t": 0.0}
	s["m_flare"] = _mat("tongue", {"wobble": 0.02, "stagger": 0.5, "flow": 2.2})
	s["m_burst"] = _mat("tongue", {"wobble": 0.07, "stagger": 0.45})
	s["m_comet"] = _mat("comet", {"flow": 3.2})
	s["m_flash"] = _mat("shell", {"flow": 3.0, "lump": 0.45, "noise_amp": 0.9})
	s["m_rock"] = _mat("rock", {"to_sun": _to_sun})
	s["m_scrap"] = _mat("scrap", {"flow": 2.5})
	s["flare"] = _mi(flare_mesh, s["m_flare"], "Flare", root)
	s["burst"] = _mi(burst_mesh, s["m_burst"], "Burst", root)
	s["comet"] = _mi(comet_mesh, s["m_comet"], "Comet", root)
	s["flash"] = _mi(shell_mesh, s["m_flash"], "Flash", root)
	s["rock"] = _mi(rock_mesh, s["m_rock"], "Rock", root)
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_custom_data = true
	mm.use_colors = true            # white, never read: the Compatibility MultiMesh trap, avoided twice
	mm.mesh = scrap_mesh
	mm.instance_count = SCRAPS
	for k in SCRAPS:
		mm.set_instance_transform(k, Transform3D(Basis().scaled(Vector3.ZERO), Vector3.ZERO))
		mm.set_instance_custom_data(k, Color(0, 1, 0, 0))
		mm.set_instance_color(k, Color(1, 1, 1, 1))
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "Scraps"
	mmi.multimesh = mm
	mmi.material_override = s["m_scrap"]
	mmi.layers = FX_LAYER
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.gi_mode = GeometryInstance3D.GI_MODE_DISABLED
	mmi.visible = false
	# the scraps fly anywhere round the impact: a generous box, so the MultiMesh is never culled
	mmi.custom_aabb = AABB(Vector3(-40, -5, -40), Vector3(80, 30, 80))
	root.add_child(mmi)
	s["scraps"] = mmi
	s["mm"] = mm
	s["sc"] = []                    # live scraps: {k, age, life, pos, vel, axis, spin, size, heat}
	s["free"] = range(SCRAPS)
	return s


# --- the geometry, generated once --------------------------------------------------------------
static func _arrays() -> Dictionary:
	return {"v": PackedVector3Array(), "n": PackedVector3Array(), "uv": PackedVector2Array(),
		"uv2": PackedVector2Array(), "i": PackedInt32Array()}


static func _commit(a: Dictionary) -> ArrayMesh:
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = a["v"]
	arr[Mesh.ARRAY_NORMAL] = a["n"]
	arr[Mesh.ARRAY_TEX_UV] = a["uv"]
	arr[Mesh.ARRAY_TEX_UV2] = a["uv2"]
	if (a["i"] as PackedInt32Array).size() > 0:
		arr[Mesh.ARRAY_INDEX] = a["i"]
	var m := ArrayMesh.new()
	m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	return m


static func _add_tongue(a: Dictionary, base: Vector3, dir: Vector3, hook: Vector3, length: float,
		r0: float, hook_rad: float, uv2: Vector2, rings := 10, seg := 7, spindle := false) -> void:
	"""A HOOKED FLAME TONGUE: a tapered tube along a curve that rises along `dir` and curls toward
	`hook` by `hook_rad` at the tip (the vocabulary's hooked tongues, in the round)."""
	var d := dir.normalized()
	var h := (hook - d * hook.dot(d))
	h = h.normalized() if h.length() > 1e-4 else d.cross(Vector3.RIGHT).normalized()
	var bn := d.cross(h).normalized()
	var start := (a["v"] as PackedVector3Array).size()
	var p := base
	for i in rings + 1:
		var t := float(i) / float(rings)
		var th := hook_rad * pow(t, 2.2)
		var tng := d * cos(th) + h * sin(th)
		var nrm := -d * sin(th) + h * cos(th)
		var r: float
		if spindle:
			r = r0 * pow(maxf(sin(PI * t), 0.0), 0.8)
		else:
			r = r0 * pow(1.0 - t, 0.85) * (1.0 + 0.35 * sin(PI * minf(t * 1.6, 1.0)))
		for j in seg:
			var ang := TAU * float(j) / float(seg)
			var radial := nrm * cos(ang) + bn * sin(ang)
			a["v"].append(p + radial * r)
			a["n"].append(radial)
			a["uv"].append(Vector2(t, float(j) / float(seg)))
			a["uv2"].append(uv2)
		p += tng * length / float(rings)
	for i in rings:
		for j in seg:
			var j2 := (j + 1) % seg
			var i0 := start + i * seg + j
			var i1 := start + i * seg + j2
			var i2 := start + (i + 1) * seg + j
			var i3 := start + (i + 1) * seg + j2
			a["i"].append_array(PackedInt32Array([i0, i2, i1, i1, i2, i3]))


static func _burst_mesh() -> ArrayMesh:
	"""THE IMPACT'S CROWN: 9 outer tongues leaning out and hooking sideways, 4 inner ones nearly
	upright and taller -- the peak vocabulary's silhouette, as 13 tongues round the impact."""
	var a := _arrays()
	var rng := RandomNumberGenerator.new()
	rng.seed = 90113
	var n_out := 9
	for i in n_out:
		var phi := TAU * (float(i) + rng.randf_range(-0.25, 0.25)) / float(n_out)
		var rb := rng.randf_range(0.28, 0.42)
		var out := Vector3(cos(phi), 0.0, sin(phi))
		var lean := deg_to_rad(rng.randf_range(28.0, 52.0))
		var dir := (Vector3.UP * cos(lean) + out * sin(lean)).normalized()
		var side := out.cross(Vector3.UP) * (1.0 if i % 2 == 0 else -1.0)
		var hook := (side * 0.8 + out * 0.4).normalized()
		_add_tongue(a, Vector3(out.x * rb, -0.08, out.z * rb), dir, hook, rng.randf_range(0.85, 1.35),
			rng.randf_range(0.15, 0.22), deg_to_rad(rng.randf_range(80.0, 140.0)),
			Vector2(phi / TAU, rb), 10, 7)
	var n_in := 4
	for i in n_in:
		var phi := TAU * (float(i) + 0.5 + rng.randf_range(-0.2, 0.2)) / float(n_in)
		var rb := rng.randf_range(0.02, 0.14)
		var out := Vector3(cos(phi), 0.0, sin(phi))
		var dir := (Vector3.UP + out * rng.randf_range(0.05, 0.3)).normalized()
		var hook := out.cross(Vector3.UP) * (1.0 if i % 2 == 0 else -1.0)
		_add_tongue(a, Vector3(out.x * rb, -0.08, out.z * rb), dir, hook, rng.randf_range(1.3, 1.9),
			rng.randf_range(0.22, 0.3), deg_to_rad(rng.randf_range(60.0, 110.0)),
			Vector2(phi / TAU, rb), 12, 8)
	return _commit(a)


static func _flare_mesh() -> ArrayMesh:
	"""THE CALL: seven small tongues bursting from one point (the staff crown), mostly up and out."""
	var a := _arrays()
	var rng := RandomNumberGenerator.new()
	rng.seed = 4471
	for i in 7:
		var phi := TAU * float(i) / 7.0 + rng.randf_range(-0.3, 0.3)
		var el := deg_to_rad(rng.randf_range(10.0, 80.0))
		var dir := Vector3(cos(phi) * cos(el), sin(el), sin(phi) * cos(el))
		var hook := dir.cross(Vector3.UP) * (1.0 if i % 2 == 0 else -1.0) + Vector3.UP * 0.3
		_add_tongue(a, Vector3.ZERO, dir, hook, rng.randf_range(0.26, 0.42), rng.randf_range(0.06, 0.085),
			deg_to_rad(rng.randf_range(70.0, 130.0)), Vector2(float(i) / 7.0, 0.0), 8, 6)
	return _commit(a)


static func _scrap_mesh() -> ArrayMesh:
	"""ONE TORN SCRAP: a small hooked spindle of flame (pointed at both ends)."""
	var a := _arrays()
	_add_tongue(a, Vector3(0, -0.11, 0), Vector3.UP, Vector3.RIGHT, 0.24, 0.055, deg_to_rad(110.0),
		Vector2(0.37, 0.0), 7, 5, true)
	return _commit(a)


static func _comet_mesh(R := 0.5, cap_off := -0.3, rings_cap := 5, rings_tail := 20, seg := 14) -> ArrayMesh:
	"""THE CORONA AND THE TRAIL: a round cap (radius R, centred cap_off behind the rock's centre, so the
	rock's leading face stands out of it) and a tail 1 m long tapering to a point, round local +Z."""
	var a := _arrays()
	var prof := []                 # [z, r, s, nz, nr]
	for k in rings_cap + 1:
		var psi := (PI * 0.5) * float(k) / float(rings_cap)
		prof.append([cap_off + R * cos(psi), R * sin(psi), 0.12 * float(k) / float(rings_cap), cos(psi), sin(psi)])
	for k in range(1, rings_tail + 1):
		var w := float(k) / float(rings_tail)
		var r := R * pow(1.0 - w, 0.9)
		prof.append([cap_off - w, r, 0.12 + 0.88 * w, 0.25, 0.97])
	for k in prof.size():
		var e: Array = prof[k]
		for j in seg:
			var ang := TAU * float(j) / float(seg)
			var c := cos(ang)
			var sn := sin(ang)
			a["v"].append(Vector3(c * float(e[1]), sn * float(e[1]), float(e[0])))
			a["n"].append(Vector3(c * float(e[4]), sn * float(e[4]), float(e[3])).normalized())
			a["uv"].append(Vector2(float(e[2]), float(j) / float(seg)))
			a["uv2"].append(Vector2.ZERO)
	for k in prof.size() - 1:
		for j in seg:
			var j2 := (j + 1) % seg
			var i0 := k * seg + j
			var i1 := k * seg + j2
			var i2 := (k + 1) * seg + j
			var i3 := (k + 1) * seg + j2
			a["i"].append_array(PackedInt32Array([i0, i2, i1, i1, i2, i3]))
	return _commit(a)


static func _ico(subdiv: int) -> Array:
	"""An icosphere: [verts (unit), faces (index triples)]."""
	var t := (1.0 + sqrt(5.0)) / 2.0
	var vs: Array = [Vector3(-1, t, 0), Vector3(1, t, 0), Vector3(-1, -t, 0), Vector3(1, -t, 0),
		Vector3(0, -1, t), Vector3(0, 1, t), Vector3(0, -1, -t), Vector3(0, 1, -t),
		Vector3(t, 0, -1), Vector3(t, 0, 1), Vector3(-t, 0, -1), Vector3(-t, 0, 1)]
	for i in vs.size():
		vs[i] = (vs[i] as Vector3).normalized()
	var fs: Array = [[0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], [1, 5, 9], [5, 11, 4],
		[11, 10, 2], [10, 7, 6], [7, 1, 8], [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
		[4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]]
	for _s in subdiv:
		var mid := {}
		var nf: Array = []
		for f in fs:
			var m := []
			for e in [[f[0], f[1]], [f[1], f[2]], [f[2], f[0]]]:
				var key := "%d_%d" % [mini(e[0], e[1]), maxi(e[0], e[1])]
				if not mid.has(key):
					vs.append(((vs[e[0]] as Vector3) + (vs[e[1]] as Vector3)).normalized())
					mid[key] = vs.size() - 1
				m.append(mid[key])
			nf.append([f[0], m[0], m[2]])
			nf.append([f[1], m[1], m[0]])
			nf.append([f[2], m[2], m[1]])
			nf.append([m[0], m[1], m[2]])
		fs = nf
	return [vs, fs]


static func _ico_mesh(subdiv: int, r: float, _crag: float) -> ArrayMesh:
	var ico := _ico(subdiv)
	var a := _arrays()
	for v in ico[0]:
		var u := v as Vector3
		a["v"].append(u * r)
		a["n"].append(u)
		a["uv"].append(Vector2(0.5 - 0.5 * u.y, atan2(u.z, u.x) / TAU + 0.5))
		a["uv2"].append(Vector2.ZERO)
	for f in ico[1]:
		a["i"].append_array(PackedInt32Array([f[0], f[1], f[2]]))
	return _commit(a)


static func _rock_mesh() -> ArrayMesh:
	"""THE ROCK: an icosphere knocked into crags, FLAT-SHADED (each facet its own three vertices, with
	its barycentric coordinates in UV2 for the seams)."""
	var ico := _ico(1)
	var rng := RandomNumberGenerator.new()
	rng.seed = 2207
	var vs: Array = ico[0]
	var disp := []
	for v in vs:
		var u := v as Vector3
		var k := 0.78 + 0.34 * rng.randf() + 0.12 * sin(u.x * 5.0 + u.y * 3.0)
		disp.append(u * ROCK_R * k * Vector3(1.0, 0.88, 1.08))
	var a := _arrays()
	var bary := [Vector2(1, 0), Vector2(0, 1), Vector2(0, 0)]
	for f in ico[1]:
		var p0: Vector3 = disp[f[0]]
		var p1: Vector3 = disp[f[1]]
		var p2: Vector3 = disp[f[2]]
		var n := (p1 - p0).cross(p2 - p0).normalized()
		if n.dot(p0 + p1 + p2) < 0.0:
			n = -n
		var ps := [p0, p1, p2]
		for k in 3:
			a["v"].append(ps[k])
			a["n"].append(n)
			a["uv"].append(Vector2.ZERO)
			a["uv2"].append(bary[k])
	return _commit(a)


# --- load: every pipeline drawn once, unseen ---------------------------------------------------
func warm_up(at: Vector3) -> void:
	"""Every material this effect draws with, drawn at `at` (in view) for three frames with every
	fragment discarded, the ground terms on (their branch taken once); then all of it hidden again."""
	var t0 := Time.get_ticks_usec()
	for s in pool:
		for key in ["flare", "burst", "comet", "flash", "rock"]:
			var mi: MeshInstance3D = s[key]
			mi.global_position = at + Vector3(0, 0.8, 0)
			mi.visible = true
			(mi.material_override as ShaderMaterial).set_shader_parameter("warm", 1.0)
		var mm: MultiMesh = s["mm"]
		mm.set_instance_transform(0, Transform3D(Basis(), at + Vector3(0, 0.8, 0)))
		(s["scraps"] as MultiMeshInstance3D).visible = true
		(s["m_scrap"] as ShaderMaterial).set_shader_parameter("warm", 1.0)
	RenderingServer.global_shader_parameter_set("fx_on", _fx_on_value)
	_fx_shaders(true)
	for _f in 3:
		await get_tree().process_frame
	for s in pool:
		for key in ["flare", "burst", "comet", "flash", "rock"]:
			var mi: MeshInstance3D = s[key]
			mi.visible = false
			(mi.material_override as ShaderMaterial).set_shader_parameter("warm", 0.0)
		(s["mm"] as MultiMesh).set_instance_transform(0, Transform3D(Basis().scaled(Vector3.ZERO), Vector3.ZERO))
		(s["scraps"] as MultiMeshInstance3D).visible = false
		(s["m_scrap"] as ShaderMaterial).set_shader_parameter("warm", 0.0)
	RenderingServer.global_shader_parameter_set("fx_on", 0.0)
	_fx_shaders(false)
	warmed = true
	report["warm_ms"] = snappedf(float(Time.get_ticks_usec() - t0) / 1000.0, 0.1)


# --- the cast ------------------------------------------------------------------------------------
var _watch_t := -1.0
var _watch_fired := false
var release_s := 1.6333                # replaced at attach by her package's own


func _physics_process(dt: float) -> void:
	"""HER RELEASE, watched from outside knight.gd (spell_fx.gd's method): the frame the chop strike
	starts, then the clip's own release time on the physics tick the animation runs on."""
	if her == null:
		return
	var att: bool = her.attacking()
	if att and _watch_t < 0.0:
		_watch_t = 0.0
		_watch_fired = String(her._strike_anim) != "a_chop"
	elif not att:
		_watch_t = -1.0
	if _watch_t >= 0.0:
		_watch_t += dt
		if not _watch_fired and _watch_t >= release_s:
			_watch_fired = true
			if enabled:
				cast(her.global_position + facing_dir() * AHEAD)


func facing_dir() -> Vector3:
	var fa: Array = her.cfg.get("forward_axis", [0.0, 0.0, 1.0])
	var f: Vector3 = her._rig.global_transform.basis * Vector3(float(fa[0]), float(fa[1]), float(fa[2]))
	f.y = 0.0
	return f.normalized() if f.length() > 1e-4 else Vector3.FORWARD


func socket_point(nm: String) -> Vector3:
	var s: Dictionary = sockets.get(nm, {})
	var skel: Skeleton3D = her._skel
	if s.is_empty() or skel == null:
		return her.global_position + Vector3(0, 1.6, 0)
	var bi := skel.find_bone(String(s["bone"]))
	if bi < 0:
		return her.global_position + Vector3(0, 1.6, 0)
	var t: Transform3D = skel.global_transform * skel.get_bone_global_pose(bi)
	return t.origin + t.basis.y.normalized() * float(s.get("along_bone_m", 0.0)) * float(her._figure_scale)


func cast(target: Vector3) -> Dictionary:
	var s: Dictionary = pool[_next]
	_next = (_next + 1) % POOL
	if not _fx_live:
		_fx_shaders(true)
	target.y = _ground_y(target)
	s["active"] = true
	s["t"] = 0.0
	s["target"] = target
	s["start"] = target + _to_sun * FALL_L
	s["hit"] = target + Vector3(0, ROCK_R * 0.6, 0)
	s["impacted"] = false
	s["spin_axis"] = Vector3(0.3, 1.0, -0.6).normalized().rotated(Vector3.UP, float(report["casts"].size()) * 1.7)
	s["shed_acc"] = 0.0
	(s["flare"] as MeshInstance3D).visible = true
	(s["flare"] as MeshInstance3D).global_position = socket_point(CROWN_SOCKET)
	(s["burst"] as MeshInstance3D).global_position = target
	(s["flash"] as MeshInstance3D).global_position = target + Vector3(0, 0.3, 0)
	_owner = s["i"]
	var rec := {"n": report["casts"].size() + 1, "slot": s["i"], "frame": Engine.get_process_frames(),
		"target": [snappedf(target.x, 0.01), snappedf(target.y, 0.01), snappedf(target.z, 0.01)]}
	report["casts"].append(rec)
	return rec


func _ground_y(p: Vector3) -> float:
	if scene != null and scene.snow != null:
		return scene.snow.surface_y(Vector2(p.x, p.z))
	var uv: Vector2 = scene.world_to_uv(p)
	return scene.floor_y_at(uv.x, uv.y)


func _char_light(at: Vector3, energy: float, reach: float) -> void:
	"""THE FIRE ON HIM AND HER: two globals read inside the characters' sun pass (PaintStack.with_char_fire)."""
	var c := FIRE_COL.srgb_to_linear()
	RenderingServer.global_shader_parameter_set("fx_char_light", Vector4(at.x, at.y, at.z, maxf(energy, 0.0)))
	RenderingServer.global_shader_parameter_set("fx_char_light_col", Vector4(c.r, c.g, c.b, reach))


# --- the clock -----------------------------------------------------------------------------------
static func _ease_out(x: float) -> float:
	x = clampf(x, 0.0, 1.0)
	return 1.0 - (1.0 - x) * (1.0 - x)


func _process(dt: float) -> void:
	var t0 := Time.get_ticks_usec()
	_clock += dt
	var any := false
	for s in pool:
		if s["active"]:
			_step(s, dt)
			any = any or bool(s["active"])
	if any != _globals_on:
		_globals_on = any
		RenderingServer.global_shader_parameter_set("fx_on", _fx_on_value if any else 0.0)
		if not any:
			_char_light(Vector3.ZERO, 0.0, 7.0)
			_fx_shaders(false)
	_step_shake(dt)
	if cam != null:
		cam.h_offset = shake_px.x / PPM
		cam.v_offset = shake_px.y / PPM
	last_update_us = Time.get_ticks_usec() - t0


func _step(s: Dictionary, dt: float) -> void:
	s["t"] = float(s["t"]) + dt
	var t: float = s["t"]
	var owner := int(s["i"]) == _owner
	var target: Vector3 = s["target"]
	# --- CALL: the flare at her staff crown -------------------------------------------------
	var flare: MeshInstance3D = s["flare"]
	if t < 0.34:
		var mf: ShaderMaterial = s["m_flare"]
		flare.global_position = socket_point(CROWN_SOCKET)
		mf.set_shader_parameter("fx_time", _clock)
		mf.set_shader_parameter("grow", _ease_out(t / 0.07) * (1.0 + 0.15 * sin(t * 40.0)))
		mf.set_shader_parameter("heat", lerpf(0.32, -0.05, clampf(t / 0.34, 0.0, 1.0)))
		mf.set_shader_parameter("erode", clampf((t - 0.14) / 0.2, 0.0, 1.0))
		if owner and t < T_FALL0 + 0.06:
			# the call's light on her, from the crown
			_char_light(flare.global_position, 3.2 * (1.0 - clampf(t / (T_FALL0 + 0.06), 0.0, 1.0)) + 0.4, 4.0)
	elif flare.visible:
		flare.visible = false
	# --- FALL ------------------------------------------------------------------------------
	var rock: MeshInstance3D = s["rock"]
	var comet: MeshInstance3D = s["comet"]
	var pos := Vector3.ZERO
	var vel := -_to_sun
	if t >= T_FALL0 and t < T_IMPACT:
		var tau := (t - T_FALL0) / FALL_S
		var u := pow(tau, 1.45)
		var start: Vector3 = s["start"]
		var hit: Vector3 = s["hit"]
		pos = start.lerp(hit, u)
		var speed := 1.45 * pow(maxf(tau, 0.02), 0.45) * start.distance_to(hit) / FALL_S
		rock.visible = true
		comet.visible = true
		rock.global_position = pos
		rock.rotate(s["spin_axis"], dt * 9.0)
		# the comet's +Z along the travel: look_at points -Z at its target, so look back up the path
		comet.global_position = pos
		comet.look_at(pos - vel, Vector3.UP if absf(vel.y) < 0.99 else Vector3.RIGHT)
		var mc: ShaderMaterial = s["m_comet"]
		mc.set_shader_parameter("fx_time", _clock)
		mc.set_shader_parameter("tail_len", clampf(1.2 + speed * 0.16, 1.2, 4.2))
		mc.set_shader_parameter("heat", 0.05 + 0.1 * tau)
		mc.set_shader_parameter("erode", 0.0)
		# TORN SCRAPS off the tail, about one every 30 ms
		s["shed_acc"] = float(s["shed_acc"]) + dt
		while float(s["shed_acc"]) > 0.03:
			s["shed_acc"] = float(s["shed_acc"]) - 0.03
			var back := pos - vel * randf_range(0.5, 1.6)
			var side := vel.cross(Vector3.UP).normalized() * randf_range(-0.25, 0.25)
			_spawn_scrap(s, back + side, -vel * randf_range(1.0, 2.5) + Vector3.UP * randf_range(0.3, 1.2),
				randf_range(0.22, 0.34), randf_range(0.7, 1.1), 0.08)
		if owner:
			RenderingServer.global_shader_parameter_set("fx_rock", Vector4(pos.x, pos.y, pos.z, SHADOW_R))
			# the fire's light on the painting: dim while it is high, growing as it comes in
			RenderingServer.global_shader_parameter_set("fx_fall_light", Vector4(pos.x, pos.y, pos.z, 0.55 + 0.45 * tau))
			_char_light(pos, 1.4 + 3.0 * tau, 8.0)
	elif t >= T_IMPACT and rock.visible:
		rock.visible = false
	if t >= T_IMPACT + 0.03 and comet.visible:
		comet.visible = false
	elif t >= T_IMPACT and comet.visible:
		(s["m_comet"] as ShaderMaterial).set_shader_parameter("erode", 0.6)
	# --- the target ring --------------------------------------------------------------------------
	if owner:
		var ring := 0.0
		if t < T_IMPACT:
			ring = _ease_out(t / 0.14) * (0.85 + 0.15 * sin(_clock * 22.0))
		else:
			ring = clampf(1.0 - (t - T_IMPACT) / 0.06, 0.0, 1.0)
		var closing := clampf((t - T_FALL0) / FALL_S, 0.0, 1.0)
		RenderingServer.global_shader_parameter_set("fx_mark", Vector4(target.x, target.y, target.z, ring))
		# x the ring's size, y its heat before the impact (the burn's after), z the clock, w the burn's size:
		# plates in guide px (content half-width over the plate's own), the procedural marks in metres
		var heat: float = closing if t < T_IMPACT else float(s.get("burn_heat", 1.0))
		if style == "plates":
			RenderingServer.global_shader_parameter_set("fx_ring", Vector4(
				RING_HALF_W_M * PPM / _ring_half_uv * lerpf(1.1, 0.95, closing), heat, _clock,
				POOL_HALF_W_M * PPM / _pool_half_uv))
		else:
			RenderingServer.global_shader_parameter_set("fx_ring", Vector4(RING_R * lerpf(1.18, 0.92, closing),
				heat, _clock, BURN_R))
	# --- IMPACT ----------------------------------------------------------------------------------
	if t >= T_IMPACT and not s["impacted"]:
		s["impacted"] = true
		(s["burst"] as MeshInstance3D).visible = true
		(s["flash"] as MeshInstance3D).visible = true
		(s["scraps"] as MultiMeshInstance3D).visible = true
		for k in 18:
			var a := TAU * float(k) / 18.0 + randf_range(-0.2, 0.2)
			var out := Vector3(cos(a), 0.0, sin(a))
			_spawn_scrap(s, target + out * randf_range(0.2, 0.5) + Vector3(0, randf_range(0.1, 0.6), 0),
				out * randf_range(2.5, 5.0) + Vector3.UP * randf_range(2.0, 4.5), randf_range(0.4, 0.75),
				randf_range(0.9, 1.5), 0.25)
		_shake_t = 0.0
		report["impacts"].append({"n": report["casts"].size(), "frame": Engine.get_process_frames()})
		if owner:
			RenderingServer.global_shader_parameter_set("fx_rock", Vector4(0, 0, 0, 0))
	if s["impacted"]:
		var ti := t - T_IMPACT
		var burst: MeshInstance3D = s["burst"]
		var mb: ShaderMaterial = s["m_burst"]
		var g: float
		if ti < 0.11:
			g = _ease_out(ti / 0.11) * 1.06
		elif ti < 0.3:
			g = lerpf(1.06, 1.0, (ti - 0.11) / 0.19)
		elif ti < 0.8:
			g = lerpf(1.0, 0.34, smoothstep(0.3, 0.8, ti))
		else:
			g = 0.34 * (1.0 - smoothstep(BURN_S - 0.9, BURN_S, ti)) * (1.0 + 0.12 * sin(_clock * 17.0) + 0.08 * sin(_clock * 29.0))
		var squash := 1.0
		if ti < 0.16:
			squash = lerpf(0.55, 1.1, smoothstep(0.0, 0.08, ti)) if ti < 0.08 else lerpf(1.1, 1.0, (ti - 0.08) / 0.08)
		mb.set_shader_parameter("fx_time", _clock)
		mb.set_shader_parameter("grow", g)
		mb.set_shader_parameter("squash", squash)
		mb.set_shader_parameter("spread", 1.0 + 0.25 * smoothstep(0.3, 1.0, ti))
		mb.set_shader_parameter("heat", lerpf(0.34, -0.02, smoothstep(0.0, 0.9, ti)) - 0.08 * smoothstep(1.5, BURN_S, ti))
		if style == "plates":
			# the painted burning ground carries the burn: the 3D crown is gone within its first second
			mb.set_shader_parameter("erode", 0.28 * smoothstep(0.35, 0.8, ti) + 0.9 * smoothstep(0.75, 1.15, ti))
			if ti > 1.2 and burst.visible:
				burst.visible = false
		else:
			mb.set_shader_parameter("erode", 0.28 * smoothstep(0.35, 0.9, ti) + 0.9 * smoothstep(BURN_S - 0.8, BURN_S, ti))
		# the flash: out and burnt away in 0.18 s
		var flash: MeshInstance3D = s["flash"]
		if ti < 0.2:
			var mfl: ShaderMaterial = s["m_flash"]
			flash.scale = Vector3(1.0, 0.8, 1.0) * lerpf(0.3, 1.05, _ease_out(ti / 0.1))
			mfl.set_shader_parameter("fx_time", _clock)
			mfl.set_shader_parameter("heat", lerpf(0.5, -0.2, clampf(ti / 0.16, 0.0, 1.0)))
			mfl.set_shader_parameter("erode", clampf((ti - 0.025) / 0.12, 0.0, 1.0))
		elif flash.visible:
			flash.visible = false
		var cool := clampf(1.0 - ti / BURN_S, 0.0, 1.0)
		s["burn_heat"] = cool
		if owner:
			var flick := 1.0 + 0.18 * sin(_clock * 23.0) + 0.12 * sin(_clock * 37.0)
			var burn_w := clampf(1.0 - smoothstep(BURN_S * 0.4, BURN_S, ti), 0.0, 1.0)
			RenderingServer.global_shader_parameter_set("fx_burn", Vector4(target.x, target.y, target.z, burn_w))
			var li := 1.6 * exp(-ti / 0.12) + 0.75 * (1.0 - smoothstep(0.6, BURN_S, ti)) * flick
			var lh := 0.5 + 1.6 * exp(-ti / 0.15)
			# ONE ground light: the burn's takes over the fall's at the impact
			RenderingServer.global_shader_parameter_set("fx_fall_light", Vector4(target.x, target.y + lh, target.z, li))
			_char_light(target + Vector3(0, 0.9, 0), 14.0 * exp(-ti / 0.12) + 2.8 * (1.0 - smoothstep(0.5, BURN_S, ti)) * flick, 6.5)
		if ti >= BURN_S:
			_end(s)
	_step_scraps(s, dt)


func _spawn_scrap(s: Dictionary, at: Vector3, vel: Vector3, life: float, size: float, heat: float) -> void:
	var free: Array = s["free"]
	var k: int
	if free.is_empty():
		# the pool is full: the oldest scrap is torn away early
		var oldest: Dictionary = (s["sc"] as Array).pop_front()
		k = int(oldest["k"])
	else:
		k = int(free.pop_back())
	(s["scraps"] as MultiMeshInstance3D).visible = true
	(s["sc"] as Array).append({"k": k, "age": 0.0, "life": life, "pos": at, "vel": vel,
		"axis": Vector3(randf() - 0.5, randf() - 0.5, randf() - 0.5).normalized(), "spin": randf_range(6.0, 14.0),
		"size": size, "heat": heat, "seed": randf(), "rot": Basis(Vector3(randf() - 0.5, 1.0, randf() - 0.5).normalized(), randf() * TAU)})


func _step_scraps(s: Dictionary, dt: float) -> void:
	var sc: Array = s["sc"]
	if sc.is_empty():
		return
	var mm: MultiMesh = s["mm"]
	(s["m_scrap"] as ShaderMaterial).set_shader_parameter("fx_time", _clock)
	var keep := []
	for e in sc:
		e["age"] = float(e["age"]) + dt
		var k: int = e["k"]
		var f: float = float(e["age"]) / float(e["life"])
		if f >= 1.0:
			mm.set_instance_transform(k, Transform3D(Basis().scaled(Vector3.ZERO), Vector3.ZERO))
			(s["free"] as Array).append(k)
			continue
		var v: Vector3 = e["vel"]
		v += Vector3(0, -6.0, 0) * dt
		v *= 1.0 - 1.8 * dt
		e["vel"] = v
		e["pos"] = (e["pos"] as Vector3) + v * dt
		e["rot"] = (e["rot"] as Basis).rotated(e["axis"], float(e["spin"]) * dt).orthonormalized()
		var sz: float = float(e["size"]) * (1.0 - 0.45 * f)
		mm.set_instance_transform(k, Transform3D((e["rot"] as Basis).scaled(Vector3.ONE * sz), e["pos"]))
		mm.set_instance_custom_data(k, Color(float(e["heat"]) - 0.35 * f, 0.55 * f * f, float(e["seed"]), 0.0))
		keep.append(e)
	s["sc"] = keep
	if keep.is_empty() and not s["active"]:
		(s["scraps"] as MultiMeshInstance3D).visible = false


func _end(s: Dictionary) -> void:
	s["active"] = false
	for key in ["flare", "burst", "comet", "flash", "rock"]:
		(s[key] as MeshInstance3D).visible = false
	if (s["sc"] as Array).is_empty():
		(s["scraps"] as MultiMeshInstance3D).visible = false
	if int(s["i"]) == _owner:
		RenderingServer.global_shader_parameter_set("fx_burn", Vector4(0, 0, 0, 0))
		RenderingServer.global_shader_parameter_set("fx_fall_light", Vector4(0, 0, 0, 0))
		RenderingServer.global_shader_parameter_set("fx_mark", Vector4(0, 0, 0, 0))
		_char_light(Vector3.ZERO, 0.0, 7.0)


func _step_shake(dt: float) -> void:
	"""THE IMPACT'S SHAKE: 7 px, gone in 0.32 s, on the camera's offsets (_process)."""
	if _shake_t < 0.0:
		shake_px = Vector2.ZERO
		return
	_shake_t += dt
	var k := _shake_t / 0.32
	if k >= 1.0:
		_shake_t = -1.0
		shake_px = Vector2.ZERO
		return
	var a := 7.0 * (1.0 - k) * (1.0 - k)
	shake_px = Vector2(sin(_shake_t * 61.0), cos(_shake_t * 47.0 + 0.7)) * a


func active_count() -> int:
	var n := 0
	for s in pool:
		if s["active"]:
			n += 1
	return n
