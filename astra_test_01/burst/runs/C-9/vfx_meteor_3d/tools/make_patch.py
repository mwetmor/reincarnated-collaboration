#!/usr/bin/env python3
"""C-9 VFX bake-off, LANE B -- THE INTEGRATION PATCH, generated from barrow_full's files AT COLLAB HEAD.

Every edit to an existing barrow_full file is an ASSERTED swap on HEAD's own text (a swap that finds its
anchor other than exactly once stops the script), and every one is ADDITIVE: with the Meteor not wanted
(no ?meteor=b) the painted surfaces' shaders and the characters' ramp are HEAD's, byte for byte.

  make_patch.py write   HEAD + the patch -> vfx_meteor_3d/godot (the copy the measurements run on)
  make_patch.py patch   the patch file -> vfx_meteor_3d/integration/lane_b_meteor.patch, built in a
                        TEMPORARY git index (the shared index and working tree are never touched), then
                        checked with `git apply --cached --check` against HEAD in a second one.
"""
import os, pathlib, subprocess, sys, tempfile

REPO = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
BF = "astra_test_01/burst/runs/C-9/barrow_full"
MINE = REPO / "astra_test_01/burst/runs/C-9/vfx_meteor_3d"


def head(path: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), "show", f"HEAD:{BF}/{path}"], check=True,
                          capture_output=True, text=True).stdout


def swap(s: str, a: str, b: str, what: str) -> str:
    n = s.count(a)
    assert n == 1, f"{what}: anchor found {n} times, not once"
    return s.replace(a, b)


# ------------------------------------------------------------------------------------------------
# project.godot: the Meteor's global shader uniforms
GLOBALS = [("fx_on", "float", "0.0"), ("fx_web", "float", "0.0"), ("fx_rock", "vec4", "Vector4(0, 0, 0, 0)"),
           ("fx_sun", "vec4", "Vector4(0, 1, 0, 0.075)"), ("fx_fall_light", "vec4", "Vector4(0, 0, 0, 0)"),
           ("fx_mark", "vec4", "Vector4(0, 0, 0, 0)"),
           ("fx_burn", "vec4", "Vector4(0, 0, 0, 0)"), ("fx_ring", "vec4", "Vector4(0, 0, 0, 0)"),
           ("fx_char_light", "vec4", "Vector4(0, 0, 0, 0)"), ("fx_char_light_col", "vec4", "Vector4(1, 0.342, 0.073, 7)")]


def project_godot(s: str) -> str:
    block = ("\n; LANE B METEOR (scripts/meteor_fx.gd): its GLOBAL shader uniforms. Only the shaders built with its terms\n"
             "; (?meteor=b: PaintedWorld.with_fx, PaintStack.with_char_fire) read them; declared here so they exist.\n"
             "[shader_globals]\n\n"
             + "".join('%s={\n"type": "%s",\n"value": %s\n}\n' % g for g in GLOBALS))
    return swap(s, "\n[rendering]\n", block + "\n[rendering]\n", "project [rendering]")


# ------------------------------------------------------------------------------------------------
# painted_world.gd: the ground terms, built into the painted surfaces only when fx_ground is on
PW_BLOCK = r'''

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
	var ground := "" if surface == "heather" else (FX_GROUND_PLATES if style == "plates" else FX_GROUND_PROCEDURAL)
	s = _swap(s, FX_HIS_SHADOW, FX_FUNCS + ground + FX_SHADOW, "fx his_shadow")
	if surface == "painted":
		s = _swap(s, "\tROUGHNESS = painted_mark;\n", "\tROUGHNESS = painted_mark;\n"
			+ "\tif (fx_on > 0.5 && !id_black) { ALBEDO = fx_ground(v_world, ALBEDO); }\n", "fx painted albedo")
	elif surface == "snow":
		s = _swap(s, "\tALBEDO = (id_black || trail_id) ? vec3(0.0) : pb;\n", "\tALBEDO = (id_black || trail_id) ? vec3(0.0) : pb;\n"
			+ "\tif (fx_on > 0.5 && !(id_black || trail_id)) { ALBEDO = fx_ground(vec3(v_world.x, floor_y + D, v_world.z), ALBEDO); }\n",
			"fx snow albedo")
	return s'''


def painted_world(s: str) -> str:
    return swap(s, "static var _shaders := {}\n", "static var _shaders := {}\n" + PW_BLOCK + "\n", "pw block")


# ------------------------------------------------------------------------------------------------
# paint_stack.gd: the Meteor's fire on him and her, inside the sun's pass
PS_BLOCK = r'''

# --- LANE B: THE METEOR'S FIRE ON HIM AND HER (vfx_meteor_3d; scripts/meteor_fx.gd) -------------------
# NOTHING ABOVE CHANGES. With the Meteor wanted, MeteorFx derives a second shader for the characters' ramp
# materials, with_char_fire(<their live code>), and swaps it in only while a Meteor is alive: the fire's light
# is added INSIDE THE SUN'S PASS -- the way the phone build's ambient is (ambient_in_light),
# and for the same reason: Compatibility sRGB-encodes each light's pass before it adds them, so a separate
# fire light (the first build's OmniLight3D) summed hot on the web. Here the sum is one, in linear light, on
# both renderers. Two hard warm bands by N.L times an omni light's own falloff (range window x 1/d); the
# light itself is two global uniforms, so there is no light node, no light list and no shader variant to
# meet at cast time.
const CHAR_FIRE_UNIFORMS := """global uniform vec4 fx_char_light;       // LANE B: the Meteor's fire on him and her: centre, energy
global uniform vec4 fx_char_light_col;   // its colour (linear) and its range (m)
"""

const CHAR_FIRE_LIGHT := """	// LANE B: the Meteor's fire, in this (the sun's) pass
	if (LIGHT_IS_DIRECTIONAL && fx_char_light.w > 0.0) {
		vec3 wn = normalize((INV_VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
		vec3 fd = fx_char_light.xyz - v_world;
		float dist = max(length(fd), 1e-3);
		float win = pow(max(1.0 - pow(dist / max(fx_char_light_col.w, 1e-3), 4.0), 0.0), 2.0);
		float e = max(dot(wn, fd / dist), 0.0) * win / dist;
		float s = smoothstep(0.05 - band_soft * 0.3, 0.05 + band_soft * 0.3, e) * 0.45
			+ smoothstep(0.30 - band_soft * 0.3, 0.30 + band_soft * 0.3, e) * 0.55;
		DIFFUSE_LIGHT += fx_char_light_col.rgb * fx_char_light.w * s;
	}
"""


static func with_char_fire(code: String) -> String:
	"""LANE B: a character ramp material's live code (CHAR_SHADER) with the Meteor's fire folded into the
	sun's pass (see above)."""
	var s := code
	assert(s.count("uniform float char_mark = 0.5;\n") == 1, "with_char_fire: the char mark uniform moved")
	s = s.replace("uniform float char_mark = 0.5;\n", "uniform float char_mark = 0.5;\n" + CHAR_FIRE_UNIFORMS)
	var tail := "	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop\n}\n"
	assert(s.count(tail) == 1, "with_char_fire: the ramp's light() tail moved")
	return s.replace(tail, "	SPECULAR_LIGHT += web_sheen;      // the phone build's sky reflection; 0 on the desktop\n"
		+ CHAR_FIRE_LIGHT + "}\n")'''


def paint_stack(s: str) -> str:
    s = swap(s, "static var _shader_cache := {}\n", "static var _shader_cache := {}\n" + PS_BLOCK + "\n", "ps block")
    return s


# ------------------------------------------------------------------------------------------------
# barrow_full.gd: three hooks
def barrow_full(s: str) -> str:
    s = swap(s, "var spell_fx: Node3D\n", "var spell_fx: Node3D\n"
             "var meteor_fx: Node3D               # LANE B: her Meteor, 3D first (?meteor=b; scripts/meteor_fx.gd)\n",
             "meteor var")
    s = swap(s, "	assert(TERRAIN_BIT == PaintStack.TERRAIN_BIT and TERRAIN_BIT == CliffWorld.TERRAIN_BIT)\n",
             "	assert(TERRAIN_BIT == PaintStack.TERRAIN_BIT and TERRAIN_BIT == CliffWorld.TERRAIN_BIT)\n"
             "", "meteor flags")
    s = swap(s, "	ready_done = true\n",
             "	if MeteorFx.wanted(self):\n"
             "		# LANE B METEOR (her page, ?meteor=b): built once here, warmed over the next frames, then it prints\n"
             "		# \"[meteor_b] armed\". Without ?meteor=b nothing of it exists and nothing above has changed.\n"
             "		meteor_fx = MeteorFx.attach(self)\n"
             "	ready_done = true\n", "meteor attach")
    return s


# ------------------------------------------------------------------------------------------------
# tools/build_web_painted.sh: ship the plates, and fence ?meteor=b
def build_web(s: str) -> str:
    s = swap(s, 'data/painted_web/bakes/*.bin"\n', 'data/painted_web/bakes/*.bin,data/meteor/*.bin,data/meteor/*.json"\n',
             "include_filter")
    anchor = '[ "$FAIL" -eq 0 ] || { echo "== VERIFY FAILED" >&2; exit 6; }\n'
    fence = r'''# LANE B METEOR (?c=sorceress&meteor=b: her page with the Meteor built 3D first, scripts/meteor_fx.gd):
# the painted plates read and sha-matched, every pipeline warmed at load, the placeholder Meteor off,
# the Fire Ball kept -- and no script or shader error. Without ?meteor=b nothing above changes.
"$GODOT" --main-pack "$W/index.pck" --rendering-method gl_compatibility --rendering-driver opengl3_angle \
  --resolution 640x360 --quit-after 1500 -- --as-web --c sorceress --meteor b > "$LOG/launch_meteor_b.log" 2>&1 || true
MLINE=$(grep -a '^\[meteor_b\] armed' "$LOG/launch_meteor_b.log" | head -1 || true)
echo "   launch (meteor=b): $(echo "$MLINE" | cut -c1-200)"
echo "$MLINE" | grep -q "plates_sha_ok=true" && echo "$MLINE" | grep -q "warmed=true" \
  && echo "$MLINE" | grep -q "placeholder_meteor=off" && echo "$MLINE" | grep -q "fire_ball=kept" \
  && ck 0 "?meteor=b: the Meteor armed (plates matched, pipelines warmed, placeholder off, Fire Ball kept)" \
  || ck 1 "?meteor=b: the Meteor did not arm"
if grep -a -q -E "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_b.log"; then
  ck 1 "?meteor=b launch free of script and shader errors"; grep -a -E -A2 "SCRIPT ERROR|SHADER ERROR|Parse Error" "$LOG/launch_meteor_b.log" | head -12 >&2
else
  ck 0 "?meteor=b launch free of script and shader errors"
fi
'''
    return swap(s, anchor, fence + anchor, "meteor fence")


FILES = {  # barrow_full path -> transform
    "godot/project.godot": project_godot,
    "godot/scripts/painted_world.gd": painted_world,
    "godot/scripts/paint_stack.gd": paint_stack,
    "godot/scripts/barrow_full.gd": barrow_full,
    "tools/build_web_painted.sh": build_web,
}
NEW = {  # barrow_full path -> the file in lane B's copy
    "godot/scripts/meteor_fx.gd": MINE / "godot/scripts/meteor_fx.gd",
    "godot/data/meteor/plates.bin": MINE / "godot/data/meteor/plates.bin",
    "godot/data/meteor/manifest.json": MINE / "godot/data/meteor/manifest.json",
}


def patched() -> dict:
    return {p: f(head(p)) for p, f in FILES.items()}


def cmd_write():
    out = patched()
    for p, text in out.items():
        if p.startswith("godot/"):
            dst = MINE / p
        else:
            dst = MINE / "integration" / "patched" / p
        if p == "godot/project.godot":
            # THE HARNESS'S TWO LINES, in lane B's copy only (never in the patch): its own name -- Godot keeps
            # the shader cache per project name, and the cold measurements clear lane B's, never barrow_full's
            # -- and the harness scene as the main scene (the page's own scene is still there, unchanged)
            text = swap(text, 'config/name="C-9 Barrow blockout"', 'config/name="C-9 Meteor lane B (3D first)"', "harness name")
            text = swap(text, 'run/main_scene="res://scenes/barrow_full.tscn"', 'run/main_scene="res://scenes/meteor_test.tscn"', "harness main")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text)
        print("wrote", dst.relative_to(REPO))


def git(*a, env=None, inp=None):
    return subprocess.run(["git", "-C", str(REPO), *a], check=True, capture_output=True, env=env, input=inp)


def cmd_patch():
    out = patched()
    tmp = tempfile.mkdtemp(prefix="laneb_idx_")
    env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
    git("read-tree", "HEAD", env=env)
    for p, text in out.items():
        sha = git("hash-object", "-w", "--stdin", inp=text.encode()).stdout.decode().strip()
        mode = "100755" if p.endswith(".sh") else "100644"
        git("update-index", "--add", "--cacheinfo", f"{mode},{sha},{BF}/{p}", env=env)
    for p, src in NEW.items():
        sha = git("hash-object", "-w", str(src)).stdout.decode().strip()
        git("update-index", "--add", "--cacheinfo", f"100644,{sha},{BF}/{p}", env=env)
    diff = git("diff", "--cached", "--binary", "HEAD", env=env).stdout
    dst = MINE / "integration" / "lane_b_meteor.patch"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(diff)
    # the check: a fresh index at HEAD takes the patch cleanly
    env2 = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index2"))
    git("read-tree", "HEAD", env=env2)
    git("apply", "--cached", "--check", str(dst), env=env2)
    stat = git("apply", "--stat", str(dst)).stdout.decode()
    print(stat)
    print("patch:", dst.relative_to(REPO), len(diff), "bytes; applies cleanly to HEAD",
          git("rev-parse", "--short", "HEAD").stdout.decode().strip())


if __name__ == "__main__":
    {"write": cmd_write, "patch": cmd_patch}[sys.argv[1]]()
