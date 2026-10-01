extends RefCounted
class_name PaintedWorld
## C-9 T10-2 step 4 -- THE PAINTING IS THE WORLD'S LIGHT AND ITS INK (the conductor's ruling).
##
##   STATIC PAINTED PIECES (the 54 heroes, the birches, the painted ground) show the painting as
##     painted: no ramp, no pen. Their outline ink is in the plate already.
##   DYNAMIC THINGS (him, later the monsters, the heather, the snow's trails, particles) keep the
##     ramp under the same sun, and the pen.
##   WHERE THEY MEET: (a) his shadow darkens the painted world; (b) he is darkened inside a
##     painted shadow; (c) static pieces cast no real shadow onto the painted world.
##
## THE MECHANISM, MEASURED FIRST (tools/probe_paint_light.gd, work/probe/probe_paint_light.json):
## TWO SUNS, ONE DIRECTION. Godot 4.6's Light3D.shadow_caster_mask is independent of its cull mask:
##   the SUN (light A) lights everything but the painted layers, and every caster shadows it --
##     so a ring stone's shadow falls on HIM (b), with the geometry the painter painted over;
##   the PAINT SUN (light B) lights ONLY the painted layers, and ONLY he casts for it -- so his
##     shadow is the one shadow the painted world receives (a), and no stone shadows it (c).
## Probe: painted receiver under a static caster 0.737 (unshadowed) / under him 0.459; dynamic
## receiver under a static caster 0.486; a block on his layer lit by A only (G = 0).
##
## THE PAINTED SURFACE is unlit paint times ONE term: his shadow, as the PAINTER'S shadow -- the
## painting's own shadow colour over its own light (shadow_mul, measured off the painting by
## tools/paint_world_prep.py) -- and only where the painting shows direct sun (lit_map, rendered
## from the blockout's own sun by tools/capture_light.gd): a shadow falling into a painted shadow
## adds nothing, as a real one would not.
##
## THE PROJECTION. The play camera never turns (pitch 52.95354, yaw 47, orthographic), so the
## painting is the complete view of every static surface. A fragment's guide pixel is analytic:
##   x = (u - u0) * ppm ;  y = (v1 - v) * ppm sin(pitch) - h * ppm cos(pitch)
## and a projected piece wears the painting at exactly the pixel the camera sees it at.

const LAYER_PAINTED := 1 << 10       # the static painted pieces: lit by the paint sun only
const LAYER_ON_PAINT := 1 << 11      # dynamic things that wear the painting (heather, the snow)
const ALL_LAYERS := (1 << 20) - 1
const PAINTED_MARK := 0.0            # the pen's mark channel (paint_stack POST_SHADER)
const DATA := "res://data/painted/"
const MANIFEST := "res://data/painted/manifest.json"
# THE PHONE PAGE'S DATA (tools/paint_world_prep.py --web): the same files, sized for a phone -- the
# painting within 4096 px (WebGL2's safe texture size), the bakes at 512, the light map at a
# quarter -- read on the web, or on the desktop with -- --as-web (PaintStack.is_web)
const DATA_WEB := "res://data/painted_web/"
# THE WEB PEN'S "NO PEN" CLASS FOR THE PAINTING (PaintStack's stencil classes: 0 full pen, 1 thin,
# 2 snow). Compatibility has no roughness buffer to carry PAINTED_MARK, so a painted piece writes
# stencil 3 and none of the post pass's three passes reads 3: no ink on it, its colour untouched
const STENCIL_PAINTED := 3


static func data_dir() -> String:
	return DATA_WEB if PaintStack.is_web() else DATA

const GUIDE_PX := Vector2(5376.0, 3328.0)
const U0 := -28.715
const V1 := 17.7203
const PPM := 100.617553710938
const PITCH_DEG := 52.95354112560294

const PROJ_UNIFORMS := """
uniform vec3 g_u_hat = vec3(0.681998, 0.0, -0.731354);
uniform vec3 g_v_hat = vec3(-0.731354, 0.0, -0.681998);
uniform vec3 g_frame = vec3(-28.715, 17.7203, 100.617553710938);   // u0, v1, px per metre
uniform vec2 g_px_per = vec2(80.3076, 60.6183);                     // ppm sin(pitch), ppm cos(pitch)
uniform vec2 g_size = vec2(5376.0, 3328.0);
// the painting's DIRECT SUN share, in guide space: 1 where the painter painted sunlight, 0 in a
// painted shadow (cast or turned away). His shadow darkens by it.
uniform sampler2D lit_map : filter_linear, repeat_disable;
// the painter's shadow over the painter's light, LINEAR, per channel (measured on open snow)
uniform vec3 shadow_mul = vec3(0.4, 0.46, 0.63);
uniform float his_shadow_on = 1.0;
"""

const PROJ_FUNCS := """
vec2 guide_uv(vec3 p) {
	float u = dot(p, g_u_hat);
	float v = dot(p, g_v_hat);
	return vec2((u - g_frame.x) * g_frame.z, (g_frame.y - v) * g_px_per.x - p.y * g_px_per.y) / g_size;
}

vec3 his_shadow(float att, vec3 wpos) {
	float lit = textureLod(lit_map, guide_uv(wpos), 0.0).r;
	return mix(vec3(1.0), shadow_mul, clamp((1.0 - att) * lit * his_shadow_on, 0.0, 1.0));
}
"""

# THE PAINTED SURFACE. ambient_light_disabled: the environment adds nothing, so the pixel is the
# paint times the paint sun's one term. The paint sun's LIGHT_COLOR is never read -- the painting
# is the light; only its ATTENUATION (his shadow) is.
# R-C9-118 (c): THE IMPACTS' BURN, one term for every dressing shader (the painted stones and birches here, the heather
# in barrow_heather.gd): four global impact slots (centre xyz, radius; radius 0 = empty), their ages, the fire field's
# life. A surface inside a radius chars, carries an ember rim while the field is hot, and (plants only) crumbles.
# Read behind one global count (fx_imp_n), so an idle page pays a uniform branch; no swap, no per-plant node.
const FX_IMP := """
global uniform vec4 fx_imp0;
global uniform vec4 fx_imp1;
global uniform vec4 fx_imp2;
global uniform vec4 fx_imp3;
global uniform vec4 fx_imp_age;      // seconds since each slot's impact
global uniform float fx_imp_life;    // the fire field's life, s (12.6 at level 20)
global uniform float fx_imp_n;       // live slots (0: nothing is computed)
// the strongest impact over p: x inside (0..1, soft and torn at the edge), y its age over the field's life
vec2 fx_imp_at(vec3 p) {
	vec2 o = vec2(0.0);
	for (int i = 0; i < 4; i++) {
		vec4 c = i == 0 ? fx_imp0 : (i == 1 ? fx_imp1 : (i == 2 ? fx_imp2 : fx_imp3));
		if (c.w <= 0.0) { continue; }
		vec2 dv = p.xz - c.xz;
		float ang = atan(dv.y, dv.x);
		float edge = c.w * (0.86 + 0.08 * sin(ang * 5.0 + c.x * 3.1) + 0.06 * sin(ang * 11.0 + c.z));
		float inside = 1.0 - smoothstep(edge * 0.82, edge, length(dv));
		float a = clamp(fx_imp_age[i] / max(fx_imp_life, 1e-3), 0.0, 1.0);
		if (inside > o.x) { o = vec2(inside, a); }
	}
	return o;
}
// char (toward a warm soot), the ember rim (hot at the char's edge, cooling over the field), as (char, ember)
vec2 fx_imp_char(vec2 ia, float age_s) {
	float ch = ia.x * smoothstep(0.0, 0.04, ia.y) * 0.88;
	float rim = ia.x * (1.0 - ia.x) * 4.0;
	float em = (rim * 0.85 + ia.x * 0.07) * (1.0 - smoothstep(0.1, 0.75, ia.y)) * smoothstep(0.0, 0.02, ia.y);
	return vec2(ch, em * (0.75 + 0.25 * sin(age_s * 9.0 + ia.x * 20.0)));
}
"""

const PAINTED_SHADER := """
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, cull_back, fog_disabled;
""" + PROJ_UNIFORMS + """
uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;
uniform bool project_uv = true;      // true: the guide projection; false: the mesh's own UV (a bake)
uniform float painted_mark = 0.0;
uniform bool id_black = false;      // the overlay's heather-mask pass: the painted world drawn black
uniform bool char_ok = false;       // R-C9-118: the stones and birches char in an impact (the ground and the mound do not)
varying vec3 v_world;
""" + PROJ_FUNCS + FX_IMP + """
void vertex() {
	v_world = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	ALBEDO = id_black ? vec3(0.0) : texture(paint_tex, project_uv ? guide_uv(v_world) : UV).rgb;
	ROUGHNESS = painted_mark;
	if (char_ok && fx_imp_n > 0.5 && !id_black) {
		vec2 ia = fx_imp_at(v_world);
		if (ia.x > 0.0) {
			vec2 ce = fx_imp_char(ia, fx_imp_age.x + fx_imp_age.y);
			ALBEDO = mix(ALBEDO, ALBEDO * vec3(0.16, 0.13, 0.11), ce.x);
			EMISSION = vec3(1.0, 0.36, 0.07) * ce.y * 0.9;
		}
	}
}

void light() {
	DIFFUSE_LIGHT += his_shadow(ATTENUATION, v_world);
}
"""

static var _shaders := {}


# --- LANE B: THE METEOR'S GROUND TERMS (vfx_meteor_3d; scripts/meteor_fx.gd) --------------------------
# NOTHING ABOVE CHANGES AND NOTHING HERE IS CALLED UNLESS THE METEOR IS WANTED (her page, ?meteor=b). Then
# MeteorFx derives, AT LOAD, a second shader for each painted surface's material (the painted pieces, the 3D
# snow, the heather) with with_fx(<its live code>), draws each once unseen, and SWAPS IT IN ONLY WHILE A
# METEOR IS ALIVE: the ground terms, read from GLOBAL uniforms (project.godot [shader_globals]) and drawn by
# the surface's OWN draw call. Idle, every surface runs the shader above, byte for byte -- measured: a
# shader carrying these terms costs ~1.5 ms a frame on the desktop even with its branch never taken, so
# they are never left compiled into the idle page:
#   fx_occlusion  the falling rock's shadow from the Barrow's sun as an AREA light -- the share of the sun's
#                 disc its sphere covers, seen from the ground point: faint and wide while it is high, dark
#                 and sharp as it lands -- in the painter's shadow colour, where the painting shows sun (his
#                 shadow's own rule: the larger of the two wins, one shadow value, as painted);
#   fx_light_at   the fire's light on the painting: a pool sized by the light's height, in three hard bands,
#                 laid on as a warm tint of the one light term (added light only clips the snow to white);
#   fx_ground     lane A's two PAINTED plates -- the target ring before the impact, the burning ground after
#                 it -- worn through the fixed camera exactly as the Barrow wears its painting, value-index
#                 mapped to the kit palette (fx_on 2); or the procedural ring and scorch (fx_on 1).

const FX_UNIFORMS := """// LANE B: the Meteor's ground terms (MeteorFx writes the globals; project.godot declares them)
global uniform float fx_on;          // 0 off; 1 the procedural ring and scorch; 2 lane A's painted plates
global uniform float fx_web;         // 1 on Compatibility, where ALBEDO is read as sRGB
global uniform vec4 fx_rock;         // the falling rock: centre, the radius its shadow is cast by
global uniform vec4 fx_sun;          // toward the sun, its angular radius (exaggerated, for the read)
global uniform vec4 fx_fall_light;   // the fire's light on the ground: the falling rock's, then the impact's and the burn's
global uniform vec4 fx_mark;         // the target: centre, the ring's strength
global uniform vec4 fx_burn;         // the burn: centre, its strength
global uniform vec4 fx_ring;         // x the ring's size, y its heat (then the burn's), z the clock, w the burn's size
uniform sampler2D fx_plates : filter_linear_mipmap, repeat_disable;   // RG the ring, BA the burning ground
"""

const FX_HIS_SHADOW := """vec3 his_shadow(float att, vec3 wpos) {
	float lit = textureLod(lit_map, guide_uv(wpos), 0.0).r;
	return mix(vec3(1.0), shadow_mul, clamp((1.0 - att) * lit * his_shadow_on, 0.0, 1.0));
}
"""

const FX_FUNCS := """float fx_hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float fx_vnoise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(fx_hash(i), fx_hash(i + vec2(1.0, 0.0)), f.x),
		mix(fx_hash(i + vec2(0.0, 1.0)), fx_hash(i + vec2(1.0, 1.0)), f.x), f.y);
}
// sRGB palette values into the space ALBEDO is read in: linear on Forward+, sRGB on Compatibility
vec3 fx_col(vec3 srgb) { return fx_web > 0.5 ? srgb : pow(srgb, vec3(2.2)); }
// the value index's four planes onto the kit palette (a filtered plate edge is its own anti-aliasing)
vec3 fx_palette(float v) {
	vec3 c = fx_col(vec3(0.25, 0.08, 0.04));
	c = v >= 0.25 ? fx_col(vec3(0.70, 0.16, 0.08)) : c;
	c = v >= 0.55 ? fx_col(vec3(1.00, 0.55, 0.12)) : c;
	return v >= 0.87 ? fx_col(vec3(1.00, 0.94, 0.75)) : c;
}

float fx_occlusion(vec3 p) {
	if (fx_rock.w <= 0.0) return 0.0;
	vec3 d = fx_rock.xyz - p;
	float L = length(d);
	float c = dot(d, fx_sun.xyz) / max(L, 1e-4);
	// outside the cone the shadow can reach, nothing: one dot and one cos for nearly every pixel
	if (c < cos(min(fx_rock.w / max(L, 1e-3) + fx_sun.w + 0.02, 1.5))) return 0.0;
	// small angles (inside the cone the rock is < 12 deg across): no asin, no acos
	float a = fx_rock.w / L;
	float b = fx_sun.w;
	float th = sqrt(max(2.0 * (1.0 - c), 0.0));
	float cover = min((a * a) / (b * b), 1.0);
	return cover * (1.0 - smoothstep(abs(a - b), a + b, th));
}

float fx_light_at(vec3 p, vec4 l) {
	if (l.w <= 0.0) return 0.0;
	float h = max(l.y - p.y, 0.3);
	float R = 0.45 + 0.5 * h;
	vec2 dd = p.xz - l.xz;
	if (dot(dd, dd) > R * R * 1.8) return 0.0;      // the noise only inside the pool (past its broken edge)
	// the broken edge: a cheap wobble, not a noise (every instruction here is paid on every pixel)
	float q = length(dd) / R + sin(p.x * 5.3 + fx_ring.z * 3.1) * sin(p.z * 4.7 - fx_ring.z * 2.3) * 0.11;
	float k = clamp(l.w * 1.3 / (0.45 + h), 0.0, 1.0);
	float w = 0.015;                                   // a fixed edge: no derivatives inside a branch
	float b = (1.0 - smoothstep(1.0 - w, 1.0 + w, q)) * 0.34 + (1.0 - smoothstep(0.62 - w, 0.62 + w, q)) * 0.33
		+ (1.0 - smoothstep(0.3 - w, 0.3 + w, q)) * 0.33;
	return b * k;
}

"""

# the two ground styles, only one of which a derived shader carries (plates: fx_on 2; procedural: fx_on 1)
const FX_GROUND_PLATES := """vec3 fx_ground(vec3 p, vec3 alb) {
	if (abs(p.y - fx_mark.y) > 0.3) return alb;      // the ground only: never up a stone's face
	// LANE A'S PAINTED PLATES, through the fixed camera: a plate's pixel is this guide pixel's offset from
	// the target's, so each lies on the ground at the size and in the shape it was painted
	vec2 gp = guide_uv(p) * g_size;
	if (fx_burn.w > 0.0) {
		vec2 uv = (gp - guide_uv(fx_burn.xyz) * g_size) / fx_ring.w + 0.5;
		if (uv.x > 0.0 && uv.y > 0.0 && uv.x < 1.0 && uv.y < 1.0) {
			// the heat's shimmer, 2 px
			uv += vec2(sin(fx_ring.z * 9.0 + uv.y * 23.0), cos(fx_ring.z * 7.0 + uv.x * 19.0)) * (2.0 / fx_ring.w);
			vec4 t = texture(fx_plates, uv);
			// IT BURNS DOWN from its outer planes in: a flame plane stays while its value clears the falling
			// cut; the dark puddle goes last, broken up
			bool flame = t.b >= 0.25;
			float keep = flame ? step((1.0 - fx_ring.y) * 0.8, t.b - 0.2)
				: step(fx_vnoise(uv * 23.0), fx_burn.w * 1.3);
			alb = mix(alb, fx_palette(t.b + (flame ? 0.1 * fx_ring.y : 0.0)), step(0.5, t.a) * keep);
		}
	}
	if (fx_mark.w > 0.0) {
		vec2 uv = (gp - guide_uv(fx_mark.xyz) * g_size) / fx_ring.x + 0.5;
		if (uv.x > 0.0 && uv.y > 0.0 && uv.x < 1.0 && uv.y < 1.0) {
			vec4 t = texture(fx_plates, uv);
			// it heats as the rock closes: every plane one step toward the core by the impact
			alb = mix(alb, fx_palette(t.r + 0.3 * fx_ring.y), step(0.5, t.g) * clamp(fx_mark.w * 3.0, 0.0, 1.0));
		}
	}
	return alb;
}

"""

const FX_GROUND_PROCEDURAL := """vec3 fx_ground(vec3 p, vec3 alb) {
	if (abs(p.y - fx_mark.y) > 0.3) return alb;      // the ground only: never up a stone's face
	vec3 c0 = fx_col(vec3(0.25, 0.08, 0.04));
	vec3 c1 = fx_col(vec3(0.70, 0.16, 0.08));
	vec3 c2 = fx_col(vec3(1.00, 0.55, 0.12));
	vec3 c3 = fx_col(vec3(1.00, 0.94, 0.75));
	if (fx_burn.w > 0.0) {
		vec2 d = p.xz - fx_burn.xz;
		float r = length(d);
		float R = fx_ring.w;
		if (r < R * 1.5) {
			float n = fx_vnoise(d * 2.3 + 11.0) * 0.6 + fx_vnoise(d * 5.1 + 3.0) * 0.4;
			float edge = R * (0.45 + 0.6 * n) * (0.4 + 0.6 * fx_burn.w);
			float w = 0.012;
			float charred = 1.0 - smoothstep(-w, w, r - edge);
			alb = mix(alb, alb * fx_col(vec3(0.52, 0.44, 0.41)), charred * clamp(fx_burn.w * 1.6, 0.0, 0.9));
			float k = abs(fx_vnoise(d * 3.7 + 5.0) - 0.5) + abs(fx_vnoise(d * 7.3) - 0.5) * 0.35;
			float heat = fx_ring.y;
			float wk = 0.006;
			float crack = (1.0 - smoothstep(0.045 * heat - wk, 0.045 * heat + wk, k)) * charred;
			float ck = (1.0 - smoothstep(0.02 * heat - wk, 0.02 * heat + wk, k)) * charred;
			vec3 hot = heat > 0.66 ? c2 : (heat > 0.33 ? c1 : c0);
			alb = mix(alb, hot, crack);
			alb = mix(alb, heat > 0.66 ? c3 : c2, ck * step(0.33, heat));
		}
	}
	if (fx_mark.w > 0.0) {
		vec2 d = p.xz - fx_mark.xz;
		float r = length(d);
		float R = fx_ring.x;
		if (r < R * 1.8 && r > R * 0.5) {
			float ang = atan(d.y, d.x) / 6.2831853 + 0.5;
			float k = fract(ang * 13.0 - fx_ring.z * 0.35);
			float tooth = pow(k, 1.8) * (0.75 + 0.5 * fx_vnoise(vec2(ang * 13.0, fx_ring.z * 2.5)));
			float inner = R - 0.05;
			float outer = R + 0.04 + 0.26 * tooth * fx_mark.w;
			float w = 0.012;
			float band = smoothstep(inner - w, inner + w, r) * (1.0 - smoothstep(outer - w, outer + w, r));
			float core = smoothstep(inner + 0.015 - w, inner + 0.015 + w, r) * (1.0 - smoothstep(inner + 0.05 - w, inner + 0.05 + w, r));
			float rim = smoothstep(outer - 0.035 - w, outer - 0.035 + w, r);
			vec3 rc = mix(c1, c2, step(r, R + 0.02));
			rc = mix(rc, c3, core * step(0.5, fx_mark.w));
			rc = mix(rc, c0, rim);
			alb = mix(alb, rc, band * clamp(fx_mark.w * 3.0, 0.0, 1.0));
		}
	}
	return alb;
}

"""

# MIX v2 (Matt, 2026-09-30: "the flames left on the ground afterwards ... more like real smoldering cinders"):
# the burn as a SCORCH -- a ragged charred patch, darkest at its heart, its edge soft and broken -- netted with
# EMBER CRACKS that glow in continuous colour (not the kit's four planes), pulse, and cool from yellow-orange
# through orange to a dull red with the burn's heat (fx_ring.y, 1 at the impact to 0), plus a few ember specks.
# The small flames above it are cinders_fx.gd's. fx_burn.w fades the whole scorch out over the burn.
const FX_GROUND_CINDERS := """vec3 fx_ground(vec3 p, vec3 alb) {
	if (abs(p.y - fx_mark.y) > 0.3) return alb;      // the ground only: never up a stone's face
	if (fx_burn.w <= 0.0) return alb;
	vec2 d = p.xz - fx_burn.xz;
	float r = length(d);
	float R = fx_ring.w;
	if (r > R * 1.35) return alb;
	float n = fx_vnoise(d * 2.1 + 11.0) * 0.6 + fx_vnoise(d * 6.3 + 3.0) * 0.4;
	float edge = R * (0.5 + 0.5 * n);
	float charred = 1.0 - smoothstep(edge * 0.9, edge, r);
	float strength = clamp(fx_burn.w * 1.5, 0.0, 1.0);
	// the ash: charred black at the heart, a grey-brown scorch toward its broken rim, mottled
	float ash = fx_vnoise(d * 13.0) * 0.5 + fx_vnoise(d * 31.0) * 0.5;
	vec3 burnt = mix(fx_col(vec3(0.10, 0.085, 0.075)), fx_col(vec3(0.38, 0.33, 0.29)), smoothstep(0.25, 1.0, r / edge) * 0.8 + ash * 0.25);
	alb = mix(alb, alb * burnt, charred * strength);
	float heat = fx_ring.y;
	float k = abs(fx_vnoise(d * 3.6 + 5.0) - 0.5) + abs(fx_vnoise(d * 8.7 + 1.7) - 0.5) * 0.45;
	float width = 0.035 + 0.05 * heat;
	float crack = (1.0 - smoothstep(width * 0.35, width, k)) * smoothstep(0.25, 0.8, charred);
	float pulse = 0.72 + 0.28 * sin(fx_ring.z * 2.7 + fx_vnoise(d * 2.4) * 6.2832);
	float t = clamp(heat * pulse * (0.55 + 0.45 * fx_vnoise(d * 5.0 + vec2(fx_ring.z * 0.21, 0.0))), 0.0, 1.0);
	vec3 ember = mix(fx_col(vec3(0.30, 0.04, 0.02)), fx_col(vec3(0.95, 0.30, 0.05)), smoothstep(0.08, 0.55, t));
	ember = mix(ember, fx_col(vec3(1.0, 0.72, 0.30)), smoothstep(0.6, 0.95, t));
	alb = mix(alb, ember, crack * smoothstep(0.03, 0.2, t) * strength);
	float speck = step(0.985, fx_hash(floor(d * 26.0))) * charred * heat * pulse;
	alb = mix(alb, fx_col(vec3(1.0, 0.45, 0.1)), speck * strength);
	return alb;
}

"""

const FX_SHADOW := """vec3 his_shadow(float att, vec3 wpos) {
	float lit = textureLod(lit_map, guide_uv(wpos), 0.0).r;
	float occ = clamp((1.0 - att) * his_shadow_on, 0.0, 1.0);
	float fire = 0.0;
	if (fx_on > 0.5) {
		occ = max(occ, fx_occlusion(wpos));
		fire = clamp(fx_light_at(wpos, fx_fall_light), 0.0, 1.0);      // ONE light: the fall's, then the burn's
	}
	vec3 shade = mix(vec3(1.0), shadow_mul, clamp(occ * lit, 0.0, 1.0));
	// the fire's warm tint (linear light): red up, blue down -- orange on the snow, never white
	return mix(shade, shade * vec3(1.32, 0.58, 0.2), fire);
}
"""


static func with_fx(code: String, surface: String, style := "plates") -> String:
	"""LANE B: `code` -- a painted surface's LIVE shader code (the painting, its bakes, the snow, the
	heather; with or without the web's stencil line) -- with the Meteor's ground terms. surface: "painted",
	"snow" or "heather" (MeteorFx tells them apart by their own uniforms). Asserted, as the snow's derivation
	is (_swap): a derivation that silently stopped applying would ship a Meteor with no shadow, unannounced."""
	var s := _swap(code, "uniform float his_shadow_on = 1.0;\n", "uniform float his_shadow_on = 1.0;\n" + FX_UNIFORMS,
		"fx uniforms")
	# ONLY WHAT THIS SURFACE AND STYLE USE: the heather has no ground marks; a plates shader carries no
	# procedural ring (every line of dead code here is paid for on every pixel of the frame)
	var ground := "" if surface == "heather" else (FX_GROUND_PLATES if style == "plates" else (FX_GROUND_CINDERS if style == "cinders" else FX_GROUND_PROCEDURAL))
	s = _swap(s, FX_HIS_SHADOW, FX_FUNCS + ground + FX_SHADOW, "fx his_shadow")
	if surface == "painted":
		s = _swap(s, "\tROUGHNESS = painted_mark;\n", "\tROUGHNESS = painted_mark;\n"
			+ "\tif (fx_on > 0.5 && !id_black) { ALBEDO = fx_ground(v_world, ALBEDO); }\n", "fx painted albedo")
	elif surface == "snow":
		s = _swap(s, "\tALBEDO = (id_black || trail_id) ? vec3(0.0) : pb;\n", "\tALBEDO = (id_black || trail_id) ? vec3(0.0) : pb;\n"
			+ "\tif (fx_on > 0.5 && !(id_black || trail_id)) { ALBEDO = fx_ground(vec3(v_world.x, floor_y + D, v_world.z), ALBEDO); }\n",
			"fx snow albedo")
	return s


static func _shader(key: String, code: String) -> Shader:
	if not _shaders.has(key):
		var sh := Shader.new()
		sh.code = code
		_shaders[key] = sh
	return _shaders[key]


static func bind_projection(m: ShaderMaterial, lit: Texture2D, shadow_mul: Vector3, u_hat: Vector3,
		v_hat: Vector3) -> void:
	"""The guide camera and his shadow's two inputs, onto any material built on PROJ_UNIFORMS.
	u_hat and v_hat are the LIVE ground basis the scene built in (residual to the analytic one
	~1e-7, reported by the scene)."""
	var p := deg_to_rad(PITCH_DEG)
	m.set_shader_parameter("g_u_hat", u_hat)
	m.set_shader_parameter("g_v_hat", v_hat)
	m.set_shader_parameter("g_frame", Vector3(U0, V1, PPM))
	m.set_shader_parameter("g_px_per", Vector2(PPM * sin(p), PPM * cos(p)))
	m.set_shader_parameter("g_size", GUIDE_PX)
	m.set_shader_parameter("lit_map", lit)
	m.set_shader_parameter("shadow_mul", shadow_mul)


static func painted_material(tex: Texture2D, project: bool, lit: Texture2D, shadow_mul: Vector3,
		u_hat: Vector3, v_hat: Vector3) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	if PaintStack.is_compatibility():
		m.shader = _shader("painted_compat", PaintStack.stencil_write(PAINTED_SHADER, STENCIL_PAINTED))
	else:
		m.shader = _shader("painted", PAINTED_SHADER)
	m.set_shader_parameter("paint_tex", tex)
	m.set_shader_parameter("project_uv", project)
	m.set_shader_parameter("painted_mark", PAINTED_MARK)
	bind_projection(m, lit, shadow_mul, u_hat, v_hat)
	return m


# --- the snow: the installed field, the painting as its albedo, relit where he has moved it ------
static func _swap(code: String, a: String, b: String, what: String) -> String:
	"""A replacement that finds nothing FAILS: the snow shader is derived from the installed one,
	and a derivation that silently stopped applying would ship the installed look unannounced."""
	assert(code.count(a) == 1, "snow_shader_code: '%s' found %d times, not once" % [what, code.count(a)])
	return code.replace(a, b)


static func snow_shader_code() -> String:
	"""SnowField.SHADER, four edits, each asserted:
	  1. no ambient, no fog: the painting is the light (as PAINTED_SHADER);
	  2. the projection uniforms and the painting;
	  3. THE BASE IS THE PAINTING BENEATH: the painting at the UNDISTURBED surface over this point
	     -- his trail moves the snow, not the paint, so the painter's dabs stay where he put them
	     and the base stays the painting's warm white (the ruling's clause 4, as for the heather);
	  4. THE RAMP ADDS ONLY THE RELIEF: the ramp at the surface's normal NOW over the ramp at its
	     UNDISTURBED normal, as one luminance ratio r (exactly 1 on untouched snow). Where the
	     dent turns from the sun (r < 1) the snow goes toward the PAINTER'S shadow colour, as far
	     as the ramp's own full shadow would take it; where the berm turns to the sun (r > 1) it
	     lifts, but never past the channel that clips first -- a warm off-white lifted by a
	     multiplier goes white in red first, and reads cool. Times his shadow.

	THE FIRST VERSION (trail_relief_only 0, kept for the A/B): the base sampled at the DISPLACED
	surface, the snow's cool press tint on the prints, and the ramp's full per-channel ratio,
	clamped at 2. On the film (the coordinator, 12 s) the trail read as a bright, cool, raised
	white rope over the warm painted snow -- measured in take/build/trail_polish.json."""
	var s: String = SnowField.SHADER
	s = _swap(s, "render_mode specular_disabled, cull_back;",
		"render_mode specular_disabled, cull_back, ambient_light_disabled, fog_disabled;", "render_mode")
	s = _swap(s, "varying float v_press;\n", "varying float v_press;\n" + PROJ_UNIFORMS
		+ "uniform sampler2D paint_tex : source_color, filter_linear_mipmap, repeat_disable;\n"
		+ "uniform float trail_relief_only = 1.0;\nuniform bool trail_id = false;\n", "varyings")
	s = _swap(s, "// ONE definition of the snow's height", PROJ_FUNCS + "\n// ONE definition of the snow's height",
		"snow_h head")
	s = _swap(s, "	ALBEDO = id_black ? vec3(0.0) : base;\n",
		"""	vec3 pb;
	if (trail_relief_only > 0.5) {
		pb = texture(paint_tex, guide_uv(vec3(v_world.x, floor_y + D, v_world.z))).rgb;
	} else {
		pb = texture(paint_tex, guide_uv(v_world)).rgb;
		pb = mix(pb, pb * press_tint, clamp(p, 0.0, 1.0) * press_tint_amt);
	}
	ALBEDO = (id_black || trail_id) ? vec3(0.0) : pb;
	// the polish's instrument: where his trail is, press in red and berm in green, nothing else
	EMISSION = trail_id ? vec3(clamp(p, 0.0, 1.0), clamp(b, 0.0, 1.0), 0.0) : vec3(0.0);
""", "albedo")
	var i := s.find("void light() {")
	assert(i > 0, "snow_shader_code: no light() in SnowField.SHADER")
	s = s.substr(0, i) + """void light() {
	vec4 f0 = textureLod(field_tex, v_uv, 0.0);
	vec3 n0 = normalize((VIEW_MATRIX * vec4(normalize(vec3(-f0.b, 1.0, -f0.a)), 0.0)).xyz);
	vec3 relief = vec3(1.0);
	// UNTOUCHED SNOW IS THE PAINTING, EXACTLY: where his trail has not turned the surface the
	// relief is 1 and none of the ramp is evaluated -- nearly every snow pixel, every frame (the
	// polish's third ramp evaluation cost 1.06 ms on the full frame until this). (A branch, not a
	// return: Godot refuses 'return' in light().)
	if (trail_relief_only < 0.5 || dot(normalize(NORMAL), n0) < 0.99999) {
		vec3 now = _ramp_light(NORMAL, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
			band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
			shadow_bite, shadow_color, shadow_energy, ramp_mix);
		vec3 ref = _ramp_light(n0, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
			band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
			shadow_bite, shadow_color, shadow_energy, ramp_mix);
		if (trail_relief_only > 0.5) {
			vec3 lw = vec3(0.2126, 0.7152, 0.0722);
			vec3 dark = _ramp_light(n0, LIGHT, 0.0, LIGHT_COLOR, v_world, wash_noise,
				band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
				shadow_bite, shadow_color, shadow_energy, ramp_mix);
			float r = dot(now, lw) / max(dot(ref, lw), 1e-4);
			float r0 = dot(dark, lw) / max(dot(ref, lw), 1e-4);
			float s = clamp((1.0 - r) / max(1.0 - r0, 1e-3), 0.0, 1.0);
			float top = 1.0 / max(max(ALBEDO.r, ALBEDO.g), max(ALBEDO.b, 1e-3));
			relief = r < 1.0 ? mix(vec3(1.0), shadow_mul, s) : vec3(min(r, top));
		} else {
			relief = clamp(now / max(ref, vec3(1e-3)), vec3(0.0), vec3(2.0));
		}
	}
	DIFFUSE_LIGHT += relief * his_shadow(ATTENUATION, v_world);
}
"""
	return s


# --- the heather: BarrowHeather's sprays and wind, coloured from the painting beneath ------------
static func heather_shader_code() -> String:
	"""BarrowHeather's stems, its wind and his push-aside unchanged; two things differ:
	  the colour: v_col (the spray's own dark-stem-to-rust ramp) times albedo_mul (one grade,
	    measured by the overlay) times INSTANCE_CUSTOM -- the painting beneath THIS spray, over
	    the mean of all of them, so a tuft the painter put in shadow is a darker, bluer spray;
	  the light: the ramp for its FORM only (att 1 -- no stone shadows it, the painting has them),
	    times his shadow as the painter's shadow, where the painting shows sun."""
	var vfun: String = BarrowHeather._SHADER_FUNCS
	assert(vfun.count("v_col = COLOR.rgb;") == 1, "heather: the vertex colour line moved")
	vfun = vfun.replace("v_col = COLOR.rgb;", "v_col = COLOR.rgb;\n\tv_mul = INSTANCE_CUSTOM.rgb;")
	return BarrowHeather._SHADER_HEAD + PaintStack.RAMP_UNIFORMS + BarrowHeather._SHADER_UNIFORMS \
		+ PROJ_UNIFORMS + "varying vec3 v_mul;\nuniform bool id_white = false;\n" \
		+ "uniform float albedo_srgb_out = 0.0;\n" + PaintStack.RAMP_BODY + PROJ_FUNCS + vfun + """
void fragment() {
	// THE WEB'S ALBEDO IS READ AS sRGB (PaintStack.WEB_GAMMA): the spray's own colours and the
	// painting's per-spray multiplier are linear, so on Compatibility their product goes out raised
	// to 1/2.2 -- albedo_mul is raised by PaintStack.web_color_space, once, like every tint
	vec3 lin = v_col * v_mul;
	vec3 base = (albedo_srgb_out > 0.5 ? pow(max(lin, vec3(0.0)), vec3(1.0 / 2.2)) : lin) * albedo_mul;
	float m = texture(mottle_noise, v_world.xz * mottle_scale).r;
	base *= (1.0 - mottle_amp * 0.5 + m * mottle_amp);
	ALBEDO = id_white ? vec3(0.0) : base;
	EMISSION = id_white ? vec3(1.0) : vec3(0.0);
	ROUGHNESS = mesh_mark;
}

void light() {
	DIFFUSE_LIGHT += _ramp_light(NORMAL, LIGHT, 1.0, LIGHT_COLOR, v_world, wash_noise,
		band_e0, band_e1, band_m0, band_m1, band_m2, band_soft, wash_amp, wash_scale,
		shadow_bite, shadow_color, shadow_energy, ramp_mix) * his_shadow(ATTENUATION, v_world);
}
"""


static func heather_material(fbm: Texture2D, albedo_mul: Vector3, lit: Texture2D, shadow_mul: Vector3,
		u_hat: Vector3, v_hat: Vector3) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	if PaintStack.is_compatibility():
		# the web pen's THIN class, as the installed Barrow's thin props write it
		m.shader = _shader("heather_compat", PaintStack.stencil_write(heather_shader_code(), PaintStack.STENCIL_THIN))
		m.set_shader_parameter("albedo_srgb_out", 1.0)
	else:
		m.shader = _shader("heather", heather_shader_code())
	m.set_shader_parameter("wash_noise", fbm)
	m.set_shader_parameter("mottle_noise", fbm)
	m.set_shader_parameter("gust_noise", fbm)
	m.set_shader_parameter("albedo_mul", albedo_mul)
	m.set_shader_parameter("mesh_mark", 0.25)
	bind_projection(m, lit, shadow_mul, u_hat, v_hat)
	return m


# --- loading, from the pck, with proof --------------------------------------------------------
static func read_manifest() -> Dictionary:
	var path := data_dir() + "manifest.json"
	if not FileAccess.file_exists(path):
		return {}
	var j = JSON.parse_string(FileAccess.get_file_as_string(path))
	return j if typeof(j) == TYPE_DICTIONARY else {}


static func load_png_bin(rel: String, want_sha: String, mipmaps: bool, rep: Dictionary) -> ImageTexture:
	"""An image off its RAW bytes (a PNG named .bin: the importer never sees it, so nothing is
	re-compressed, and an include_filter ships the file itself), its sha256 checked against the
	manifest. `rep[rel]` says what happened -- the app's launch line is built from these."""
	var path := data_dir() + rel
	var r := {"path": path}
	rep[rel] = r
	if not FileAccess.file_exists(path):
		r["error"] = "missing"
		return null
	var bytes := FileAccess.get_file_as_bytes(path)
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(bytes)
	var sha := ctx.finish().hex_encode()
	r["sha256_ok"] = sha == want_sha
	r["bytes"] = bytes.size()
	var img := Image.new()
	# PNG or WebP (the phone page's painting and bakes), by the file's own signature
	var webp := bytes.size() > 12 and bytes.slice(0, 4).get_string_from_ascii() == "RIFF" \
		and bytes.slice(8, 12).get_string_from_ascii() == "WEBP"
	r["format"] = "webp" if webp else "png"
	var err := img.load_webp_from_buffer(bytes) if webp else img.load_png_from_buffer(bytes)
	if err != OK:
		r["error"] = "decode %d" % err
		return null
	r["px"] = [img.get_width(), img.get_height()]
	if mipmaps:
		img.generate_mipmaps()
	return ImageTexture.create_from_image(img)


static func load_f32_bin(rel: String, want_sha: String, rep: Dictionary) -> PackedFloat32Array:
	var path := data_dir() + rel
	var r := {"path": path}
	rep[rel] = r
	if not FileAccess.file_exists(path):
		r["error"] = "missing"
		return PackedFloat32Array()
	var bytes := FileAccess.get_file_as_bytes(path)
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(bytes)
	r["sha256_ok"] = ctx.finish().hex_encode() == want_sha
	r["bytes"] = bytes.size()
	return bytes.to_float32_array()
