shader_type spatial;
// kc2_etch_mm.gdshader — C-9 R-C9-143 EOR2 PORT 19: kc2_etch.gdshader (below, verbatim) drawn as a MULTIMESH.
//   ONE mesh holds all 12 stroke variants; each vertex carries its variant in COLOR.b ((id + 0.5) / 16). Each
//   instance carries INSTANCE_CUSTOM = (variant id, stroke_age, 0, 0); a vertex of any other variant collapses to
//   the origin (degenerate, no fragments). stroke_age moves from a per-material uniform to that per-instance
//   value. The fragment is unchanged. Blend is ADD with depth_draw_never, so the order sheaths-then-cores
//   (here) vs sheath/core per stroke (the pool) sums to the same pixels.
// ============================================================================
// kc2_etch.gdshader — SB-1 Cell A2c item 1 / A2d item 3. THE CUT.
// drax, presentation seam, 2026-08-12 / 2026-08-13.
//
// ⚑ MATT'S THREE IMAGES, ONE PROPERTY SET (R-CPB-7, ratified: "the extraction is
//   correct — proceed"):
//     "laser, etching a line across metal"
//     "a New York Subway train, derailing and etching a line of glowing sparks
//      across metal, or a wall"
//     "a sharp version of an afterglow when you stare into the sun... then
//      close your eyes as the trails remain, etching across the sky"
//   -> CONTINUOUS · DENSE · PERSISTENT · SHARP-EDGED · HOT. All five still
//   govern; R-CPB-12 truncates the PERSISTENT one and multiplies the strokes.
//
// This shader owns SHARP-EDGED, HOT, and R-CPB-12's palette clause. The other
// three are geometry and live in `kc2_player_channel.gd`.
//
// ⚑ HOT IS AN HDR CLAIM, NOT A COLOUR CLAIM. `head_energy` runs well above 1.0
//   so the stroke's core lands in HDR and the WorldEnvironment's glow pass
//   (threshold 1.0) actually catches it. A white-hot core painted at 1.0 would
//   tonemap to plain white and bloom nothing.
//
// ⚑ SHARP IS A FALLOFF CLAIM. `v_rim` runs 0 on the stroke's axis to 1 at its
//   edge, and the falloff is pow(1 - rim, edge_sharpness): a crisp bright spine
//   with the softness pushed OUT into the bloom sheath, which is what "a sharp
//   version" of the after-image means. A gaussian across the whole width would
//   be the fuzz the ruling excludes by name.
//
// ⚑ R-CPB-12 CLAUSE 4 — THE PALETTE NOW HAS THREE STOPS AND ENDS IN RED.
//   white-hot -> orange -> RED, "with slow disappearance in the tail". The
//   `decay_gamma < 1` shape is KEPT and it is what makes that possible: energy
//   drops fast off the steel and then CRAWLS, and the crawl is where the red
//   lives. A gamma above 1 would hold the stroke white-hot for half its life and
//   then drop it, which is an after-image with no after-image quality — the
//   defect the A2c draft had before it was measured.
//
// ⚑ NO CLOCK. There is no TIME here and there must not be. `stroke_age` is a
//   uniform written per tick by `apply_tick`, and its value is a pure function
//   of the sim tick — hashes of (seed, revolution, slot), no RNG state, no wall
//   clock, no accumulation. One clock in the whole scene (GL-18 / FG-10).
// ============================================================================
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;

// white-hot at the steel -> orange -> RED as the cut cools behind it. DECLARED
// taste: no wire carries a colour.
uniform vec3 core_color : source_color = vec3(1.0, 0.97, 0.90);
uniform vec3 mid_color : source_color = vec3(1.0, 0.42, 0.06);
uniform vec3 tail_color : source_color = vec3(0.98, 0.07, 0.02);
uniform float head_energy = 9.0;      // HDR at the steel
uniform float mid_energy = 1.70;      // HDR at the orange knee
uniform float tail_energy = 0.26;     // HDR one full persistence behind it
uniform float mid_at = 0.34;          // where the orange knee sits on the age axis
// ⚑ BELOW 1, AND THE FIRST DRAFT HAD IT ABOVE. `a = age^gamma` feeds the mix,
//   so gamma > 1 makes `a` SMALL for small age — which holds the stroke at
//   white-hot for half its life. Below 1 the energy drops fast off the steel and
//   then crawls: bright at the head, a long red tail behind it.
uniform float decay_gamma = 0.55;
// R-CPB-12 clause 4's "slow disappearance": the last fraction of the life ramps
// smoothly to nothing instead of popping off at the truncation.
uniform float tail_fade = 0.28;
uniform float edge_sharpness = 2.6;   // crisp core; the sheath carries the bloom
// THIS stroke's leading edge, as a fraction of CUT_PERSIST_REVS. Written per
// tick, per pool slot, from the tick alone.
varying float stroke_age;            // PORT 19: INSTANCE_CUSTOM.y, per instance

varying float v_age;                  // this vertex's OWN age behind the leading edge
varying float v_rim;                  // 0 on the stroke's axis, 1 at its edge

void vertex() {
	v_age = COLOR.r;
	v_rim = COLOR.g;
	stroke_age = INSTANCE_CUSTOM.y;
	if (abs(floor(COLOR.b * 16.0) - INSTANCE_CUSTOM.x) > 0.5) {
		VERTEX = vec3(0.0);
	}
}

void fragment() {
	float total = clamp(stroke_age + v_age, 0.0, 1.0);
	float a = pow(total, decay_gamma);
	vec3 c;
	float e;
	if (a < mid_at) {
		float k = a / max(mid_at, 1e-4);
		c = mix(core_color, mid_color, k);
		e = mix(head_energy, mid_energy, k);
	} else {
		float k = (a - mid_at) / max(1.0 - mid_at, 1e-4);
		c = mix(mid_color, tail_color, k);
		e = mix(mid_energy, tail_energy, k);
	}
	float fade = smoothstep(1.0, 1.0 - tail_fade, total);
	float f = pow(clamp(1.0 - v_rim, 0.0, 1.0), edge_sharpness);
	ALBEDO = c * e * fade * f;
	ALPHA = 1.0;
}
