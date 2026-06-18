// spell-motion-score.mjs — galadriel's NEW time-sequence motion-aware spell scorer.
//
// WHY THIS INSTRUMENT EXISTS (the core problem):
//   A spell is a VERB. The static register-2 scorer (LDR/SHF/warmCool) cannot score a verb —
//   a frozen charge-frame looks identical whether the spell MOVES (a cast) or just SITS (a glyph).
//   The descent VFX was carried as "inherited PASS" precisely because no still can score motion.
//   Matt's ask is "MEANINGFUL spell effects" — meaning is carried by EMANATION + MOTION +
//   ELEMENT-LEGIBILITY + COMBAT-INTENT, none of which a single frame holds. So this instrument
//   reads the STRIP (charge -> release -> travel -> impact -> fade) and measures whether energy
//   is a character-driven cast travelling caster->threat, or a static summon-glyph.
//
// THE CAPTURES: descent_spellfx_warhall_seq_01..07.png, 1152x648, godot 3b1daa2.
//   t = 0.08/0.18/0.30/0.47/0.63/0.74/0.92 = charge / charge-peak / release / mid-travel /
//   impact-onset / impact / fade. Synty-derivative, local-only + git-ignored. md5-distinct verified.
//
// ════════════════════════════════════════════════════════════════════════════════════════════════
// THE METHODOLOGY CRUX — spell-mask isolation by ADDITIVE-FLOOR subtraction (no-silent-transform):
//
//   The naive "warm-energy centroid over the whole frame" is the WRONG instrument here, and I proved
//   it on this very strip: a whole-frame warm centroid barely moves (48%->46% x) because it is
//   SWAMPED by the static warm chamber backdrop (torchlit walls, braziers, warm floor). This is the
//   SAME trap the blue-slab diagnostic header warned of — measure the THING THAT CHANGED, not the
//   whole field. The spell is ADDITIVE light on a STATIC rig (the GREEN-locked chamber didn't move),
//   so the correct isolation is:
//
//       backdrop_floor(x,y) = MIN over all 7 frames of warm-luma(x,y)      [the static warm field]
//       spell_energy(x,y,t) = max(0, warm-luma(x,y,t) - backdrop_floor(x,y))  [the transient cast]
//
//   spell_energy is therefore the EXCESS warm-bright light the cast ADDS above the always-present
//   warm backdrop. The static torchlit walls have ~0 excess (they're warm in every frame -> the floor
//   eats them). The KEEP-locked pale CombatFill disc under the caster is COOL-pale, not warm, AND
//   static -> excluded twice over (warm gate + floor subtraction). The spell core is the only thing
//   with large positive excess. THE SPELL-MASK = pixels where spell_energy > SPELL_THRESH.
//   warm-luma := luma gated to warm pixels (r>b), so cool backdrop never enters the energy field.
//
// ════════════════════════════════════════════════════════════════════════════════════════════════
// THE FIVE MOTION-AWARE METRICS (all computed on the isolated spell-mask):
//
//  1. ★ ENERGY-TRAVEL (headline). Per-frame center-of-energy-mass = the spell_energy-weighted
//     centroid (brightness x warmth). Track its trajectory across the strip. PASS = centroid TRAVELS
//     from caster (early frames) toward threat/marquee (late frames). FAIL = static at one ground
//     point. Reports per-frame centroid (x%,y%) + net caster->threat displacement (% of frame width).
//       REFINEMENT (no-silent-transform, mask-viz-corroborated): the FULL-mask centroid (e>=28) is
//       CONTAMINATED in the charge frames (F01-F03) by a diffuse warm FLOOR-WASH — the charge lights
//       a broad warm pool on the floor that the additive-floor min-subtraction under-cancels (the
//       floor is dimmer in some frames so the per-pixel min doesn't fully remove it). The mask-viz
//       (spell_mask diag) shows this plainly: F01-F03 = a big red floor blob; F04-F07 = a tight
//       bright bloom that marches right. So the HEADLINE track is the BRIGHT-CORE centroid (e>=90 =
//       CORE_THRESH) — the projectile/bolt the eye actually follows — reported ALONGSIDE the full-mask
//       centroid for transparency. The bright-core centroid is the cleaner caster->threat signal and
//       matches the independent brightest-pixel probe (33%->53% x). BOTH are in the JSON.
//
//  2. INTER-FRAME MOTION-PRESENCE. Frame-to-frame |spell_energy(t)-spell_energy(t-1)| over the
//     spell region. A real cast has high PROPAGATING delta (the leading edge advances frame to
//     frame); a static glyph pulses in place (delta centroid stationary). Reports mean inter-frame
//     delta + whether the high-delta band's centroid MOVES across frames (propagation) vs pulses.
//
//  3. ELEMENT-HUE LEGIBILITY (fire). Hue histogram of the spell-mask. Fire = high-R, mid-G, low-B
//     (hue in the red->orange->amber band, ~0-50deg). Reports dominant hue + fraction of spell-mask
//     pixels in the fire band (0-50deg), consistency across the lifecycle. FAIL = element-ambiguous
//     (no warm dominant hue) or a non-fire cast hue.
//
//  4. PREMIUM-LAYERING (not a flat billboard). The blue-slab flat-panel signature INVERTED: a
//     premium spell has HIGH local-luma-variance within the mask (core + glow gradient + particle
//     scatter = layered depth); a flat saturated billboard has LOW local variance (cardboard).
//     Reports mean local-luma-std inside the spell-mask. PASS = layered/high-variance; FAIL = flat.
//
//  5. DIRECTIONALITY / PRINCIPAL-AXIS. PCA of the spell-mask pixel cloud (weighted by spell_energy).
//     The principal axis + elongation (lambda1/lambda2). PASS = elongated AND its axis aligns with
//     the caster->threat vector (points at the enemy). FAIL = radially-symmetric (elongation ~1 =
//     a round ground-glow, points nowhere = decoration not a cast).
//
//  PLUS — BACKDROP-INVARIANCE (Gate-B-adjacent). OUTSIDE the spell mask, confirm the chamber
//     backdrop is unchanged frame-to-frame (the spell is additive; the GREEN-locked rig must not
//     have moved). Reports per-frame backdrop-luma drift + warm/cool drift vs F01, OUTSIDE-mask only.
//     Any drift above tolerance = the cast perturbed the rig = a Gate-B fail to flag.
//
// CASTER / THREAT GEOMETRY (grounded empirically, not assumed — I probed the pixels first):
//   The hero/caster stands center-bottom (~x=34%, the brightest-pixel origin in F01 charge).
//   The threat/marquee mob cluster sits screen-RIGHT (~x=53%, where the impact-burst lands F05-06).
//   So the caster->threat vector points RIGHTWARD + slightly UP (charge is low/ground, travel/impact
//   rise off the floor). CASTER=(34,72)% , THREAT=(53,58)% in frame-fraction (from the F01 brightest
//   origin and the F06 impact centroid). The headline PASS = energy-centroid marches caster->threat.
//
// DETERMINISM + no-silent-transform: 960w inside-fit resize (documented), no random sampling, raw
//   captures preserved untouched (reads only; writes JSON + an annotated strip). Another
//   galadriel-instance reproduces these EXACTLY. All thresholds are stated constants below.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

// ──────────────────────────── config + stated thresholds ────────────────────────────
const TARGET_W = 960;                       // inside-fit resize width (documented transform)
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const N = 7;
const T = [0.08, 0.18, 0.30, 0.47, 0.63, 0.74, 0.92];
const BEAT = ['charge', 'charge-peak', 'release', 'mid-travel', 'impact-onset', 'impact', 'fade'];

const SPELL_THRESH = 28;     // spell_energy (warm-luma excess above static floor) to enter the FULL mask
const CORE_THRESH  = 90;     // spell_energy to enter the BRIGHT-CORE mask (the projectile/bolt the eye follows)
const WARM_MARGIN  = 6;      // r - b >= this for a pixel to count as warm (so cool backdrop is excluded)
const FIRE_HUE_LO  = 0;      // fire band: hue in [0,50] deg (red->orange->amber)
const FIRE_HUE_HI  = 50;
const BACKDROP_DRIFT_TOL = 4.0;  // mean abs luma drift (0-255) outside mask vs F01 considered "invariant"

// caster / threat geometry, in frame-fraction (grounded by the pixel-probe, see header)
const CASTER = { x: 0.34, y: 0.72 };
const THREAT = { x: 0.53, y: 0.58 };

const FILES = Array.from({ length: N }, (_, i) =>
  `descent_spellfx_warhall_seq_0${i + 1}.png`);

// ──────────────────────────── pixel helpers ────────────────────────────
function luma(r, g, b) { return 0.299 * r + 0.587 * g + 0.114 * b; }
// warm-luma: luma if the pixel is warm (r meaningfully > b), else 0. This is the field the
// additive-floor subtraction operates on — cool backdrop is structurally excluded.
function warmLuma(r, g, b) { return (r - b) >= WARM_MARGIN ? luma(r, g, b) : 0; }
// hue in degrees (HSV). 0=red, 60=yellow, 120=green, 240=blue.
function hueDeg(r, g, b) {
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  if (d === 0) return -1; // achromatic
  let h;
  if (mx === r) h = ((g - b) / d) % 6;
  else if (mx === g) h = (b - r) / d + 2;
  else h = (r - g) / d + 4;
  h *= 60; if (h < 0) h += 360;
  return h;
}
// local luma std over a 3x3 neighborhood (the premium-layering / flat-cardboard signature)
function localStd(L, w, h, x, y) {
  let s = 0, ss = 0, n = 0;
  for (let dy = -1; dy <= 1; dy++) { const yy = y + dy; if (yy < 0 || yy >= h) continue;
    for (let dx = -1; dx <= 1; dx++) { const xx = x + dx; if (xx < 0 || xx >= w) continue;
      const v = L[yy * w + xx]; s += v; ss += v * v; n++; } }
  const m = s / n; return Math.sqrt(Math.max(0, ss / n - m * m));
}

// ──────────────────────────── load all frames as raw RGB ────────────────────────────
async function loadRaw(path) {
  const { data, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  return { rgb: data, w: info.width, h: info.height };
}

process.stderr.write('loading 7 frames...\n');
const frames = [];
for (const f of FILES) frames.push(await loadRaw(join(DIR, f)));
const w = frames[0].w, h = frames[0].h, P = w * h;
for (const fr of frames) if (fr.w !== w || fr.h !== h) throw new Error('frame dim mismatch');

// per-frame warm-luma field + per-frame full luma field (for backdrop-invariance)
const warm = frames.map(fr => {
  const a = new Float32Array(P);
  for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = warmLuma(fr.rgb[i], fr.rgb[i + 1], fr.rgb[i + 2]);
  return a;
});
const lumaF = frames.map(fr => {
  const a = new Float32Array(P);
  for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = luma(fr.rgb[i], fr.rgb[i + 1], fr.rgb[i + 2]);
  return a;
});
// signed warm-bias (r-b) per frame, for backdrop warm/cool drift
const warmBias = frames.map(fr => {
  const a = new Float32Array(P);
  for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = fr.rgb[i] - fr.rgb[i + 2];
  return a;
});

// ──────────────────────────── THE CRUX: static warm backdrop floor ────────────────────────────
// backdrop_floor(p) = MIN over all frames of warm-luma(p). The static warm field (walls/braziers/
// floor that are warm in EVERY frame) survives; the transient spell (warm only in the frames it
// occupies) is subtracted away to ~0 there.
const floor = new Float32Array(P);
for (let p = 0; p < P; p++) {
  let m = Infinity;
  for (let t = 0; t < N; t++) if (warm[t][p] < m) m = warm[t][p];
  floor[p] = m;
}
// per-frame spell_energy = max(0, warm-luma - floor); and the boolean spell-mask
const energy = frames.map((_, t) => {
  const e = new Float32Array(P);
  for (let p = 0; p < P; p++) { const v = warm[t][p] - floor[p]; e[p] = v > 0 ? v : 0; }
  return e;
});
const mask = energy.map(e => {
  const m = new Uint8Array(P);
  for (let p = 0; p < P; p++) m[p] = e[p] >= SPELL_THRESH ? 1 : 0;
  return m;
});
// union mask (any frame's spell) — defines the "spell region" vs the "backdrop region"
const unionMask = new Uint8Array(P);
for (let p = 0; p < P; p++) for (let t = 0; t < N; t++) if (mask[t][p]) { unionMask[p] = 1; break; }

// ════════════════════════════════════════════════════════════════════════════════════════════════
// METRIC 1 — ENERGY-TRAVEL (headline): spell_energy-weighted centroid per frame
// ════════════════════════════════════════════════════════════════════════════════════════════════
function centroid(e, thr) {
  let sx = 0, sy = 0, sw = 0, n = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x, ww = e[p];
    if (ww >= thr) { sx += x * ww; sy += y * ww; sw += ww; n++; }
  }
  if (sw === 0) return { x: -1, y: -1, mass: 0, px: 0 };
  return { x: sx / sw / w, y: sy / sw / h, mass: sw, px: n };  // x,y in frame-fraction
}
const cents = energy.map(e => centroid(e, SPELL_THRESH));   // full-mask (transparency)
const cores = energy.map(e => centroid(e, CORE_THRESH));    // bright-core (HEADLINE — the bolt the eye follows)

// caster->threat axis (unit vector) and projection of the centroid onto it (0=caster, 1=threat)
const axis = { x: THREAT.x - CASTER.x, y: THREAT.y - CASTER.y };
const axisLen = Math.hypot(axis.x, axis.y);
const axU = { x: axis.x / axisLen, y: axis.y / axisLen };
function projOnAxis(cx, cy) { // fraction along caster->threat (can be <0 or >1)
  return ((cx - CASTER.x) * axU.x + (cy - CASTER.y) * axU.y) / axisLen;
}
const travel = cents.map((c, t) => {
  const co = cores[t];
  return {
    frame: t + 1, t: T[t], beat: BEAT[t],
    // HEADLINE: bright-core centroid (the bolt the eye follows)
    core_cx: co.x < 0 ? null : +(co.x * 100).toFixed(1),
    core_cy: co.y < 0 ? null : +(co.y * 100).toFixed(1),
    core_axis_frac: co.x < 0 ? null : +projOnAxis(co.x, co.y).toFixed(3),  // 0=caster .. 1=threat
    core_px: co.px,
    // transparency: full-mask centroid (floor-wash-contaminated in charge frames)
    full_cx: c.x < 0 ? null : +(c.x * 100).toFixed(1),
    full_cy: c.y < 0 ? null : +(c.y * 100).toFixed(1),
    full_axis_frac: c.x < 0 ? null : +projOnAxis(c.x, c.y).toFixed(3),
    full_px: c.px,
  };
});
// net caster->threat displacement: from EARLY (charge) to LATE (impact) — computed on the BRIGHT CORE
const early = cores.find(c => c.x >= 0);
const lateIdx = [5, 6, 4].find(i => cores[i].x >= 0); // prefer impact(F06) then fade(F07) then onset(F05)
const late = cores[lateIdx];
const netDispX = (early && late) ? +((late.x - early.x) * 100).toFixed(1) : null;     // % frame width
const netDispAxis = (early && late) ? +(projOnAxis(late.x, late.y) - projOnAxis(early.x, early.y)).toFixed(3) : null;

// ════════════════════════════════════════════════════════════════════════════════════════════════
// METRIC 2 — INTER-FRAME MOTION-PRESENCE: |energy(t)-energy(t-1)|, and does the high-delta band MOVE?
// ════════════════════════════════════════════════════════════════════════════════════════════════
const motion = [];
for (let t = 1; t < N; t++) {
  let sum = 0, n = 0, sx = 0, sy = 0, sw = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x;
    const d = Math.abs(energy[t][p] - energy[t - 1][p]);
    if (unionMask[p]) { sum += d; n++; }
    if (d >= SPELL_THRESH) { sx += x * d; sy += y * d; sw += d; }  // high-delta band centroid
  }
  motion.push({
    pair: `${t}->${t + 1}`, beat: `${BEAT[t - 1]}->${BEAT[t]}`,
    mean_delta_in_region: n ? +(sum / n).toFixed(2) : 0,
    delta_centroid_x: sw ? +(sx / sw / w * 100).toFixed(1) : null,
    delta_centroid_y: sw ? +(sy / sw / h * 100).toFixed(1) : null,
  });
}
// propagation = does the high-delta centroid advance along the caster->threat axis across pairs?
const dcx = motion.map(m => m.delta_centroid_x).filter(v => v !== null);
const propagationSpanX = dcx.length ? +(Math.max(...dcx) - Math.min(...dcx)).toFixed(1) : 0;

// ════════════════════════════════════════════════════════════════════════════════════════════════
// METRIC 3 — ELEMENT-HUE LEGIBILITY (fire): hue histogram of the spell-mask, per frame
// ════════════════════════════════════════════════════════════════════════════════════════════════
const hue = [];
for (let t = 0; t < N; t++) {
  const fr = frames[t], m = mask[t];
  const hist = new Array(36).fill(0); // 10deg bins
  let fireN = 0, tot = 0, meanR = 0, meanG = 0, meanB = 0;
  for (let p = 0, i = 0; p < P; p++, i += 3) {
    if (!m[p]) continue;
    const r = fr.rgb[i], g = fr.rgb[i + 1], b = fr.rgb[i + 2];
    const hd = hueDeg(r, g, b);
    tot++; meanR += r; meanG += g; meanB += b;
    if (hd >= 0) { hist[Math.min(35, Math.floor(hd / 10))]++; }
    if (hd >= FIRE_HUE_LO && hd <= FIRE_HUE_HI) fireN++;
  }
  let domBin = -1, domVal = -1;
  for (let b = 0; b < 36; b++) if (hist[b] > domVal) { domVal = hist[b]; domBin = b; }
  hue.push({
    frame: t + 1, beat: BEAT[t], mask_px: tot,
    dominant_hue_deg: tot ? `${domBin * 10}-${domBin * 10 + 10}` : null,
    fire_band_frac: tot ? +(fireN / tot).toFixed(3) : null,
    mean_rgb: tot ? [Math.round(meanR / tot), Math.round(meanG / tot), Math.round(meanB / tot)] : null,
  });
}

// ════════════════════════════════════════════════════════════════════════════════════════════════
// METRIC 4 — PREMIUM-LAYERING: mean local-luma-std inside the spell-mask (blue-slab signature inverted)
// ════════════════════════════════════════════════════════════════════════════════════════════════
const layering = [];
for (let t = 0; t < N; t++) {
  const L = lumaF[t], m = mask[t];
  let s = 0, n = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x;
    if (!m[p]) continue;
    s += localStd(L, w, h, x, y); n++;
  }
  layering.push({ frame: t + 1, beat: BEAT[t], mask_px: n, mean_local_std: n ? +(s / n).toFixed(2) : null });
}

// ════════════════════════════════════════════════════════════════════════════════════════════════
// METRIC 5 — DIRECTIONALITY / PRINCIPAL-AXIS: PCA of the spell-mask cloud (energy-weighted)
// ════════════════════════════════════════════════════════════════════════════════════════════════
function pca(e) {
  // weighted mean
  let sw = 0, mx = 0, my = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x, ww = e[p]; if (ww < SPELL_THRESH) continue;
    sw += ww; mx += x * ww; my += y * ww;
  }
  if (sw === 0) return null;
  mx /= sw; my /= sw;
  let cxx = 0, cyy = 0, cxy = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = y * w + x, ww = e[p]; if (ww < SPELL_THRESH) continue;
    const dx = x - mx, dy = y - my;
    cxx += ww * dx * dx; cyy += ww * dy * dy; cxy += ww * dx * dy;
  }
  cxx /= sw; cyy /= sw; cxy /= sw;
  // eigenvalues/vectors of [[cxx,cxy],[cxy,cyy]]
  const tr = cxx + cyy, det = cxx * cyy - cxy * cxy;
  const disc = Math.sqrt(Math.max(0, tr * tr / 4 - det));
  const l1 = tr / 2 + disc, l2 = tr / 2 - disc;
  // principal eigenvector (for l1)
  let vx, vy;
  if (Math.abs(cxy) > 1e-6) { vx = l1 - cyy; vy = cxy; }
  else { vx = cxx >= cyy ? 1 : 0; vy = cxx >= cyy ? 0 : 1; }
  const vn = Math.hypot(vx, vy) || 1; vx /= vn; vy /= vn;
  return { l1, l2, elong: l2 > 1e-6 ? Math.sqrt(l1 / l2) : Infinity, vx, vy, mx: mx / w, my: my / h };
}
// caster->threat axis in PIXEL space (note y grows downward; axis already in fraction, convert dir only)
const axPxX = (THREAT.x - CASTER.x) * w, axPxY = (THREAT.y - CASTER.y) * h;
const axPxN = Math.hypot(axPxX, axPxY);
const axDir = { x: axPxX / axPxN, y: axPxY / axPxN };
const direction = [];
for (let t = 0; t < N; t++) {
  const pc = pca(energy[t]);
  if (!pc) { direction.push({ frame: t + 1, beat: BEAT[t], elongation: null }); continue; }
  // alignment = |cos angle| between principal axis and caster->threat dir (axis is undirected)
  const dot = Math.abs(pc.vx * axDir.x + pc.vy * axDir.y);
  direction.push({
    frame: t + 1, beat: BEAT[t],
    elongation: +pc.elong.toFixed(2),                          // 1 = round/radial, >1 = elongated
    axis_align_cos: +dot.toFixed(3),                            // 1 = points exactly along caster->threat
    principal_axis_deg: +(Math.atan2(pc.vy, pc.vx) * 180 / Math.PI).toFixed(1),
    casterThreat_axis_deg: +(Math.atan2(axDir.y, axDir.x) * 180 / Math.PI).toFixed(1),
  });
}

// ════════════════════════════════════════════════════════════════════════════════════════════════
// BACKDROP-INVARIANCE (Gate-B-adjacent): OUTSIDE the union spell-mask, drift vs F01
// ════════════════════════════════════════════════════════════════════════════════════════════════
const backdrop = [];
let outN = 0; for (let p = 0; p < P; p++) if (!unionMask[p]) outN++;
for (let t = 0; t < N; t++) {
  let dL = 0, dW = 0;
  for (let p = 0; p < P; p++) {
    if (unionMask[p]) continue;
    dL += Math.abs(lumaF[t][p] - lumaF[0][p]);
    dW += Math.abs(warmBias[t][p] - warmBias[0][p]);
  }
  backdrop.push({
    frame: t + 1, beat: BEAT[t],
    backdrop_luma_drift_vs_F01: +(dL / outN).toFixed(3),
    backdrop_warmbias_drift_vs_F01: +(dW / outN).toFixed(3),
  });
}
const maxBackdropDrift = Math.max(...backdrop.map(b => b.backdrop_luma_drift_vs_F01));
const backdropInvariant = maxBackdropDrift <= BACKDROP_DRIFT_TOL;

// ──────────────────────────── annotated trajectory strip (no silent transform: docs the path) ──────────────────────────
async function annotatedStrip() {
  const TW = 384;
  const tiles = [];
  for (let t = 0; t < N; t++) {
    const scale = TW / w;
    const c = cores[t].x >= 0 ? cores[t] : cents[t];  // mark the BRIGHT-CORE (the bolt) when present
    const overlays = [];
    // mark the bright-core centroid (the headline trajectory point) as a small cross via SVG
    if (c.x >= 0) {
      const px = Math.round(c.x * TW), py = Math.round(c.y * h * scale);
      const svg = `<svg width="${TW}" height="${Math.round(h * scale)}">
        <line x1="${px - 7}" y1="${py}" x2="${px + 7}" y2="${py}" stroke="#00ffff" stroke-width="2"/>
        <line x1="${px}" y1="${py - 7}" x2="${px}" y2="${py + 7}" stroke="#00ffff" stroke-width="2"/>
        <circle cx="${Math.round(CASTER.x * TW)}" cy="${Math.round(CASTER.y * h * scale)}" r="4" fill="none" stroke="#33ff33" stroke-width="2"/>
        <circle cx="${Math.round(THREAT.x * TW)}" cy="${Math.round(THREAT.y * h * scale)}" r="4" fill="none" stroke="#ff3333" stroke-width="2"/>
        </svg>`;
      overlays.push({ input: Buffer.from(svg), top: 0, left: 0 });
    }
    const base = await sharp(join(DIR, FILES[t])).resize(TW, null, { fit: 'inside' }).toBuffer();
    const tile = await sharp(base).composite(overlays).toBuffer();
    tiles.push(tile);
  }
  const meta = await sharp(tiles[0]).metadata();
  const tw = meta.width, th = meta.height, cols = 4, rows = 2, gap = 4;
  const W = cols * tw + (cols + 1) * gap, H = rows * th + (rows + 1) * gap;
  const comp = tiles.map((t, i) => ({ input: t, left: gap + (i % cols) * (tw + gap), top: gap + Math.floor(i / cols) * (th + gap) }));
  await sharp({ create: { width: W, height: H, channels: 3, background: { r: 18, g: 18, b: 22 } } })
    .composite(comp).png().toFile(join(process.cwd(), 'spell-motion-trajectory.png'));
  return `${W}x${H}`;
}
const stripDims = await annotatedStrip();

// ──────────────────────────── verdict assembly ────────────────────────────
const out = {
  scored_at: new Date().toISOString(),
  instrument: 'spell-motion-score.mjs (galadriel — NEW time-sequence motion-aware spell scorer)',
  godot_commit: '3b1daa2',
  captures: { dir: DIR, files: FILES, dims: `${w}x${h}`, t: T, beats: BEAT },
  method: 'spell-mask isolated by ADDITIVE-FLOOR subtraction: spell_energy=max(0, warmLuma - per-pixel-min-warmLuma-over-all-frames); mask = spell_energy>=' + SPELL_THRESH + '. warmLuma=luma gated to r-b>=' + WARM_MARGIN + ' (cool backdrop + pale CombatFill disc excluded). 5 metrics computed on that mask; backdrop-invariance computed OUTSIDE the union mask. Deterministic, 960w inside-fit, raw captures untouched.',
  geometry: { caster_frac: CASTER, threat_frac: THREAT, note: 'caster=F01 brightest-pixel origin; threat=F06 impact centroid; grounded by pixel-probe not assumed' },
  thresholds: { SPELL_THRESH, WARM_MARGIN, FIRE_HUE_BAND_DEG: [FIRE_HUE_LO, FIRE_HUE_HI], BACKDROP_DRIFT_TOL },
  metric1_energy_travel: { headline_track: 'bright-core centroid (e>=' + CORE_THRESH + '); full-mask track carried for transparency (floor-wash-contaminated in charge frames)', per_frame: travel, net_displacement_x_pct_CORE: netDispX, net_displacement_axisFrac_CORE: netDispAxis, axis_frac_legend: '0=caster .. 1=threat' },
  metric2_motion_presence: { pairs: motion, propagation_span_x_pct: propagationSpanX },
  metric3_fire_hue: hue,
  metric4_premium_layering: layering,
  metric5_directionality: direction,
  backdrop_invariance: { per_frame: backdrop, max_luma_drift_vs_F01: +maxBackdropDrift.toFixed(3), invariant: backdropInvariant, tol: BACKDROP_DRIFT_TOL },
  trajectory_strip: 'spell-motion-trajectory.png (' + stripDims + ')',
};

const outPath = join(process.cwd(), 'spell-motion-score.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ──────────────────────────── console report ────────────────────────────
const line = (s) => console.log(s);
line('═══════════════════════════════════════════════════════════════════════════════════════');
line('  SPELL-MOTION-SCORE — war_hall FIRE cast, godot 3b1daa2 (galadriel, INDEPENDENT)');
line('  time-sequence instrument — a spell is a VERB; this scores the strip, not a still');
line('═══════════════════════════════════════════════════════════════════════════════════════');
line(`  spell-mask isolated by additive-floor subtraction (static warm backdrop removed).`);
line(`  caster=(${(CASTER.x*100)|0},${(CASTER.y*100)|0})%  threat=(${(THREAT.x*100)|0},${(THREAT.y*100)|0})%  (grounded by pixel-probe)\n`);

line('METRIC 1 ★ ENERGY-TRAVEL (headline) — does the bright spell-core march caster->threat?');
line('  CORE = bright-core centroid e>=' + CORE_THRESH + ' (the bolt the eye follows; headline). FULL = full-mask e>=' + SPELL_THRESH + ' (floor-wash-contaminated in charge).');
line(['frame', 'beat', 'CORE(x%,y%)', 'CORE axis', 'full(x%,y%)', 'full axis'].map((s,i)=>s.padEnd([7,14,16,11,16,11][i])).join(''));
line('-'.repeat(75));
for (const r of travel) line([`F0${r.frame}`, r.beat, r.core_cx===null?'(none)':`(${r.core_cx},${r.core_cy})`, r.core_axis_frac===null?'-':r.core_axis_frac, r.full_cx===null?'(none)':`(${r.full_cx},${r.full_cy})`, r.full_axis_frac===null?'-':r.full_axis_frac].map((s,i)=>String(s).padEnd([7,14,16,11,16,11][i])).join(''));
line(`  -> NET caster->threat (CORE): dx=${netDispX}% frame-width, axis-advance=${netDispAxis} (charge->impact; 0=caster 1=threat)\n`);

line('METRIC 2 INTER-FRAME MOTION-PRESENCE — does the high-delta band PROPAGATE or pulse in place?');
line(['pair', 'beat', 'mean delta', 'delta-centroid x%'].map((s,i)=>s.padEnd([7,26,12,18][i])).join(''));
line('-'.repeat(63));
for (const m of motion) line([m.pair, m.beat, m.mean_delta_in_region, m.delta_centroid_x===null?'-':m.delta_centroid_x].map((s,i)=>String(s).padEnd([7,26,12,18][i])).join(''));
line(`  -> high-delta band x-span across strip = ${propagationSpanX}% frame-width (large=propagates; ~0=pulses in place)\n`);

line('METRIC 3 FIRE-HUE LEGIBILITY — dominant hue + fire-band fraction (fire = 0-50deg)');
line(['frame', 'beat', 'dom hue deg', 'fire-band frac', 'mean RGB'].map((s,i)=>s.padEnd([7,14,14,16,16][i])).join(''));
line('-'.repeat(67));
for (const r of hue) line([`F0${r.frame}`, r.beat, r.dominant_hue_deg||'-', r.fire_band_frac===null?'-':r.fire_band_frac, r.mean_rgb?`[${r.mean_rgb}]`:'-'].map((s,i)=>String(s).padEnd([7,14,14,16,16][i])).join(''));
line('');

line('METRIC 4 PREMIUM-LAYERING — mean local-luma-std in mask (HIGH=layered core+glow+particles; LOW=flat billboard)');
line(['frame', 'beat', 'mean local-std', 'mask px'].map((s,i)=>s.padEnd([7,14,16,10][i])).join(''));
line('-'.repeat(47));
for (const r of layering) line([`F0${r.frame}`, r.beat, r.mean_local_std===null?'-':r.mean_local_std, r.mask_px].map((s,i)=>String(s).padEnd([7,14,16,10][i])).join(''));
line('');

line('METRIC 5 DIRECTIONALITY / PRINCIPAL-AXIS — elongation (1=round) + alignment to caster->threat (1=points at enemy)');
line(['frame', 'beat', 'elongation', 'axis-align cos', 'princ deg', 'c->t deg'].map((s,i)=>s.padEnd([7,14,12,16,11,10][i])).join(''));
line('-'.repeat(70));
for (const r of direction) line([`F0${r.frame}`, r.beat, r.elongation===null?'-':r.elongation, r.axis_align_cos===undefined?'-':r.axis_align_cos, r.principal_axis_deg===undefined?'-':r.principal_axis_deg, r.casterThreat_axis_deg===undefined?'-':r.casterThreat_axis_deg].map((s,i)=>String(s).padEnd([7,14,12,16,11,10][i])).join(''));
line('');

line('BACKDROP-INVARIANCE (Gate-B-adjacent) — OUTSIDE the spell mask, drift vs F01 (rig must not have moved)');
line(['frame', 'beat', 'luma drift', 'warmbias drift'].map((s,i)=>s.padEnd([7,14,12,16][i])).join(''));
line('-'.repeat(49));
for (const b of backdrop) line([`F0${b.frame}`, b.beat, b.backdrop_luma_drift_vs_F01, b.backdrop_warmbias_drift_vs_F01].map((s,i)=>String(s).padEnd([7,14,12,16][i])).join(''));
line(`  -> max backdrop luma-drift = ${maxBackdropDrift.toFixed(3)} (tol ${BACKDROP_DRIFT_TOL}); INVARIANT=${backdropInvariant ? 'YES ✓' : 'NO ✗ (cast perturbed the rig — flag)'}\n`);

line(`wrote ${outPath}`);
line(`wrote ${join(process.cwd(), 'spell-motion-trajectory.png')} (${stripDims})`);
