// ladder-anchor-still-probe.mjs — galadriel Wave-1 ladder-anchoring calibration probe.
//
// WHY THIS EXISTS (the instrument-maturity boundary, surfaced not papered-over):
//   spell-motion-score.mjs is the locked time-sequence instrument. It is HARDCODED to a 7-frame
//   Godot capture sequence and isolates the spell by ADDITIVE-FLOOR subtraction across that temporal
//   sequence (a static rig assumption). It CANNOT ingest single genre stills, and 3 of its 5 axes
//   (energy-travel, motion-presence, directionality) are INHERENTLY TEMPORAL — a single still has no
//   time axis, so those three are UN-ANCHORABLE from stills, full stop. This is an honest v0.1 boundary.
//
//   But TWO of gandalf's load-bearing juice axes rest on SINGLE-FRAME primitives:
//     - hue-legibility  : fire-band hue fraction (hueDeg in [0,50] deg) — spell-motion METRIC 3
//     - layering-variance: mean local-luma-std inside the spell region — spell-motion METRIC 4
//   This probe computes EXACTLY those two using the IDENTICAL primitives the locked instrument uses
//   (hueDeg + localStd, copied verbatim from spell-motion-score.mjs, same FIRE_HUE band + 3x3 std),
//   so the genre-anchor values are apples-to-apples with what spell-motion will report on drax's frames.
//   The locked instrument is NOT modified; this is a separate read-only sidecar probe.
//
// THE STILL-ADAPTATION (documented, no silent transform):
//   On a single still there is NO temporal floor to subtract, so the "spell region" cannot be isolated
//   by additive-floor masking. Instead the spell/VFX region is isolated by a HIGHLIGHT-LUMA GATE — the
//   bright emissive VFX pixels — which is the SAME luma>0.80 highlight concept register-metrics HLF uses.
//   Two gates reported for transparency:
//     - HI gate (luma >= 0.62 * 255 = 158): the bright VFX-glow region (the spell bloom + its falloff)
//     - WARM-HI gate: HI gate AND warm (r-b >= 6) — the FIRE-specific spell region (matches spell-motion's
//       warm-gate so fire-hue legibility is measured on the warm spell, not cool backdrop glow).
//   layering-variance is reported on the HI gate (luma layering of the whole bright VFX, element-agnostic,
//   matching spell-motion METRIC 4 which is element-agnostic local-std). fire-hue legibility is the
//   fire-band fraction within the WARM-HI gate (the warm spell region), matching METRIC 3's intent.
//
//   CAVEAT (stated up-front, load-bearing for interpretation): a genre still is a FULL COMBAT SCENE,
//   not an isolated spell on a neutral grey stage (which is what drax's Godot frames will be, per spec §3).
//   So the still's HI-gate region includes ALL bright VFX in frame (multiple spells, loot beams, fire
//   props), whereas drax's frame will be ONE spell on grey. The anchor is therefore a GENRE-SCENE
//   fire-VFX reference, not a single-isolated-spell reference — the absolute number is "as good as the
//   anchors allow" (gandalf's own framing). The DELTA (V1 vs V0) is the primary signal and is robust to this.
//
// DETERMINISM: 960w inside-fit resize (same as both locked instruments), raw images untouched, all
//   thresholds stated constants. Another galadriel-instance reproduces these EXACTLY.

import sharp from 'sharp';
import { writeFileSync } from 'fs';

const TARGET_W = 960;
const HI_LUMA = 158;     // 0.62*255 — bright VFX-glow gate (the spell bloom + falloff)
const WARM_MARGIN = 6;   // r-b >= this = warm (verbatim from spell-motion-score.mjs)
const FIRE_HUE_LO = 0, FIRE_HUE_HI = 50;  // fire band (verbatim from spell-motion-score.mjs)

// ── primitives copied VERBATIM from spell-motion-score.mjs (apples-to-apples) ──
function luma(r, g, b) { return 0.299 * r + 0.587 * g + 0.114 * b; }
function hueDeg(r, g, b) {
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  if (d === 0) return -1;
  let h;
  if (mx === r) h = ((g - b) / d) % 6;
  else if (mx === g) h = (b - r) / d + 2;
  else h = (r - g) / d + 4;
  h *= 60; if (h < 0) h += 360;
  return h;
}
function localStd(L, w, h, x, y) {
  let s = 0, ss = 0, n = 0;
  for (let dy = -1; dy <= 1; dy++) { const yy = y + dy; if (yy < 0 || yy >= h) continue;
    for (let dx = -1; dx <= 1; dx++) { const xx = x + dx; if (xx < 0 || xx >= w) continue;
      const v = L[yy * w + xx]; s += v; ss += v * v; n++; } }
  const m = s / n; return Math.sqrt(Math.max(0, ss / n - m * m));
}

async function probe(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height, P = w * h;
  const L = new Float32Array(P);
  for (let p = 0, i = 0; p < P; p++, i += 3) L[p] = luma(rgb[i], rgb[i + 1], rgb[i + 2]);

  // gates
  const hiMask = new Uint8Array(P);     // bright VFX-glow region
  const warmHiMask = new Uint8Array(P); // fire-specific (bright AND warm)
  let hiN = 0, warmHiN = 0;
  for (let p = 0, i = 0; p < P; p++, i += 3) {
    if (L[p] >= HI_LUMA) {
      hiMask[p] = 1; hiN++;
      if (rgb[i] - rgb[i + 2] >= WARM_MARGIN) { warmHiMask[p] = 1; warmHiN++; }
    }
  }

  // METRIC-4 analog: layering-variance = mean local-luma-std inside HI gate (element-agnostic, matches spell-motion M4)
  let lsSum = 0, lsN = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x; if (!hiMask[p]) continue;
    lsSum += localStd(L, w, h, x, y); lsN++;
  }
  const layeringVariance = lsN ? lsSum / lsN : null;

  // METRIC-3 analog: fire-band fraction within WARM-HI gate (the warm spell region)
  let fireN = 0, warmHiTot = 0;
  for (let p = 0, i = 0; p < P; p++, i += 3) {
    if (!warmHiMask[p]) continue;
    warmHiTot++;
    const hd = hueDeg(rgb[i], rgb[i + 1], rgb[i + 2]);
    if (hd >= FIRE_HUE_LO && hd <= FIRE_HUE_HI) fireN++;
  }
  const fireBandFrac = warmHiTot ? fireN / warmHiTot : null;

  // also: fire-band fraction within HI gate (all-bright, for transparency — un-warm-gated)
  let fireN_hi = 0, hiTot = 0;
  for (let p = 0, i = 0; p < P; p++, i += 3) {
    if (!hiMask[p]) continue;
    hiTot++;
    const hd = hueDeg(rgb[i], rgb[i + 1], rgb[i + 2]);
    if (hd >= FIRE_HUE_LO && hd <= FIRE_HUE_HI) fireN_hi++;
  }
  const fireBandFrac_hiGate = hiTot ? fireN_hi / hiTot : null;

  return {
    dims: `${w}x${h}`,
    hi_gate_px: hiN, hi_gate_pct: +(100 * hiN / P).toFixed(2),
    warmhi_gate_px: warmHiN, warmhi_gate_pct: +(100 * warmHiN / P).toFixed(2),
    layering_variance_HIgate: layeringVariance === null ? null : +layeringVariance.toFixed(2),
    fire_band_frac_WARMHIgate: fireBandFrac === null ? null : +fireBandFrac.toFixed(3),
    fire_band_frac_HIgate: fireBandFrac_hiGate === null ? null : +fireBandFrac_hiGate.toFixed(3),
  };
}

const args = process.argv.slice(2);
if (args.length === 0) { console.error('usage: node ladder-anchor-still-probe.mjs <label=path> [...]'); process.exit(1); }

const rows = [];
for (const a of args) {
  const eq = a.indexOf('=');
  const label = eq > 0 ? a.slice(0, eq) : a;
  const path = eq > 0 ? a.slice(eq + 1) : a;
  try { rows.push({ label, ...(await probe(path)) }); }
  catch (e) { rows.push({ label, error: String(e.message || e) }); }
}

const cols = ['label', 'hi_gate_pct', 'warmhi_gate_pct', 'layering_variance_HIgate', 'fire_band_frac_WARMHIgate', 'fire_band_frac_HIgate'];
const widths = cols.map(c => Math.max(c.length, ...rows.map(r => String(r[c] ?? '').length)));
console.log(cols.map((c, i) => c.padEnd(widths[i])).join('  '));
console.log(widths.map(w => '-'.repeat(w)).join('  '));
for (const r of rows) console.log(cols.map((c, i) => String(r[c] ?? '').padEnd(widths[i])).join('  '));
console.log('\nJSON:');
console.log(JSON.stringify({
  probe: 'ladder-anchor-still-probe.mjs',
  note: 'Wave-1 ladder-anchoring. layering_variance + fire_band primitives copied VERBATIM from spell-motion-score.mjs (the locked instrument is NOT modified). Still-adaptation: HI-gate luma>=158 isolates bright VFX region (no temporal floor on a single still); WARM-HI adds r-b>=6 for fire-specific region. Genre stills are full combat scenes not isolated spells — anchor = genre-scene fire-VFX reference.',
  thresholds: { HI_LUMA, WARM_MARGIN, FIRE_HUE_BAND_DEG: [FIRE_HUE_LO, FIRE_HUE_HI] },
  rows,
}, null, 2));
