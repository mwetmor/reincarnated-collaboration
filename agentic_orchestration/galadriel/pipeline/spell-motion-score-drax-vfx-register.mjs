// spell-motion-score-drax-vfx-register.mjs
// ─────────────────────────────────────────────────────────────────────────────────────────────────
// galadriel Wave-2 PARAMETERIZED sidecar of the LOCKED spell-motion-score.mjs.
//
// WHY A NEW SIDECAR (locked-instrument discipline — the locked instrument is NOT edited):
//   spell-motion-score.mjs is HARDCODED to the 7-frame Godot descent fire-cast (DIR/FILES/CASTER/THREAT
//   constants) and takes no CLI args. Wave-2 must score drax's Binbun-emission VFX-register frames
//   ({v0,v1,v2}_primary_NNN, 20-frame lifecycle). Per galadriel's "no silent transformation / do not
//   edit the locked instrument" discipline, this is a SEPARATE sidecar that:
//     - copies the spell-mask isolation (ADDITIVE-FLOOR subtraction) + all 5 metric primitives VERBATIM,
//     - re-points DIR/FILES at drax's frames + selects 7 representative lifecycle frames per variant,
//     - re-grounds the geometry EMPIRICALLY from drax's frames (see GEOMETRY note below),
//     - runs all 3 variants so the V1-V0 delta (the headline) + V2 cross-check are computed in one pass.
//   Methodology is IDENTICAL to the locked instrument; only the inputs + a documented geometry/applicability
//   adaptation differ. Another galadriel-instance reproduces these EXACTLY.
//
// THE INPUTS (drax's render, gandalf VFX-register-test spec 2026-06-18):
//   {v0,v1,v2}_primary_000..019.png — 20-frame temporal lifecycle, PRIMARY angle, on a FEATURELESS
//   grey stage. V0=stock Binbun fire_ball blend_mix no-sub-emitter. V1=blend_add + emission 2.0 +
//   32-billboard ember sub-emitter (the lever). V2=Brackeys fire_01_8x8 flipbook-into-3D additive.
//   7 representative frames selected per variant spanning the lifecycle (emerge->grow->peak->fade):
//   indices [0,4,7,10,13,16,19]. (The spec asked for ~7 frames across cast->travel->impact->residual;
//   these frames are the lifecycle analog — see GEOMETRY/APPLICABILITY note.)
//
// ════════════════════════════════════════════════════════════════════════════════════════════════
// GEOMETRY / APPLICABILITY note (surfaced, not papered-over — load-bearing for verdict interpretation):
//   I grounded the caster->threat geometry by probing the bright-core centroid trajectory across all
//   three 20-frame sequences (the same brightest-pixel/bright-core method the locked instrument uses).
//   FINDING: drax's captures are NOT a directed caster->threat PROJECTILE STRIP (which is what the
//   descent sequence was, and what M1 energy-travel + M5 directionality were designed to score).
//   They are an IN-PLACE LIFECYCLE — a fireball that EMERGES, GROWS to peak, and FADES, centered near
//   frame-center (core x stays ~46-50% across the whole sequence; core MASS swings 2.3k->29k->18k px).
//   There is no caster origin and no threat target in the captures. CONSEQUENCE:
//     - M1 energy-travel (axis-projection) + M5 directionality (axis-alignment) are reported for
//       completeness BUT are NOT load-bearing here — there is no caster->threat axis in a centered
//       lifecycle. I set CASTER/THREAT to a nominal horizontal axis through frame-center purely so the
//       projection math runs; the AXIS-FRAC + AXIS-ALIGN numbers are not meaningful and are flagged.
//     - The MEANINGFUL temporal axes for these captures are:
//         M2 motion-presence (does spell energy PROPAGATE/GROW frame-to-frame — a live verb vs a frozen
//            decal) + a GROWTH read (peak mask-px vs emerge mask-px), AND
//         M3 fire-hue + M4 premium-layering (per-frame, lifecycle-tracked).
//     - This is an honest instrument-applicability boundary: the spec's load-bearing JUICE axes for the
//       verdict are HLF (bloom, from register-metrics on stills), layering/depth (M4 + still-probe), and
//       MOTION (M2 motion-presence here). Energy-travel-as-directed-cast is N/A for a centered lifecycle
//       and does not gate the verdict.
//
// DETERMINISM + no-silent-transform: 960w inside-fit resize (documented), no random sampling, raw
//   captures untouched (reads only; writes JSON only — no strip, to avoid clutter). All thresholds are
//   the SAME stated constants as the locked instrument.
// ─────────────────────────────────────────────────────────────────────────────────────────────────

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

// ──────────────────────────── config + stated thresholds (VERBATIM from locked instrument) ────────────────────────────
const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/vfx_register_2026-06-18';
const VARIANTS = ['v0', 'v1', 'v2'];
const FRAME_IDX = [0, 4, 7, 10, 13, 16, 19];          // 7 representative lifecycle frames
const N = FRAME_IDX.length;                             // 7
const BEAT = ['emerge', 'grow-1', 'grow-2', 'near-peak', 'post-peak', 'fade-1', 'residual'];

const SPELL_THRESH = 28;     // spell_energy (warm-luma excess above static floor) to enter the FULL mask
const CORE_THRESH  = 90;     // spell_energy to enter the BRIGHT-CORE mask
const WARM_MARGIN  = 6;      // r - b >= this for a pixel to count as warm (so cool grey backdrop excluded)
const FIRE_HUE_LO  = 0;      // fire band: hue in [0,50] deg (red->orange->amber)
const FIRE_HUE_HI  = 50;
const BACKDROP_DRIFT_TOL = 4.0;

// nominal horizontal axis through frame-center (NOT a real caster->threat — see GEOMETRY note).
// Used only so the projection math runs; AXIS-FRAC numbers are flagged non-meaningful for a centered lifecycle.
const CASTER = { x: 0.35, y: 0.50 };
const THREAT = { x: 0.65, y: 0.50 };

// ──────────────────────────── pixel helpers (VERBATIM from locked instrument) ────────────────────────────
function luma(r, g, b) { return 0.299 * r + 0.587 * g + 0.114 * b; }
function warmLuma(r, g, b) { return (r - b) >= WARM_MARGIN ? luma(r, g, b) : 0; }
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

async function loadRaw(path) {
  const { data, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  return { rgb: data, w: info.width, h: info.height };
}

// ──────────────────────────── score ONE variant (full locked methodology) ────────────────────────────
async function scoreVariant(variant) {
  const files = FRAME_IDX.map(i => `${variant}_primary_${String(i).padStart(3, '0')}.png`);
  const frames = [];
  for (const f of files) frames.push(await loadRaw(join(DIR, f)));
  const w = frames[0].w, h = frames[0].h, P = w * h;
  for (const fr of frames) if (fr.w !== w || fr.h !== h) throw new Error('frame dim mismatch');

  const warm = frames.map(fr => { const a = new Float32Array(P);
    for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = warmLuma(fr.rgb[i], fr.rgb[i + 1], fr.rgb[i + 2]); return a; });
  const lumaF = frames.map(fr => { const a = new Float32Array(P);
    for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = luma(fr.rgb[i], fr.rgb[i + 1], fr.rgb[i + 2]); return a; });
  const warmBias = frames.map(fr => { const a = new Float32Array(P);
    for (let p = 0, i = 0; p < P; p++, i += 3) a[p] = fr.rgb[i] - fr.rgb[i + 2]; return a; });

  // THE CRUX: static warm backdrop floor = per-pixel MIN warm-luma over all frames (grey bg has ~0 warm -> ~0 floor)
  const floor = new Float32Array(P);
  for (let p = 0; p < P; p++) { let m = Infinity;
    for (let t = 0; t < N; t++) if (warm[t][p] < m) m = warm[t][p]; floor[p] = m; }
  const energy = frames.map((_, t) => { const e = new Float32Array(P);
    for (let p = 0; p < P; p++) { const v = warm[t][p] - floor[p]; e[p] = v > 0 ? v : 0; } return e; });
  const mask = energy.map(e => { const m = new Uint8Array(P);
    for (let p = 0; p < P; p++) m[p] = e[p] >= SPELL_THRESH ? 1 : 0; return m; });
  const unionMask = new Uint8Array(P);
  for (let p = 0; p < P; p++) for (let t = 0; t < N; t++) if (mask[t][p]) { unionMask[p] = 1; break; }

  // axis
  const axis = { x: THREAT.x - CASTER.x, y: THREAT.y - CASTER.y };
  const axisLen = Math.hypot(axis.x, axis.y);
  const axU = { x: axis.x / axisLen, y: axis.y / axisLen };
  const projOnAxis = (cx, cy) => ((cx - CASTER.x) * axU.x + (cy - CASTER.y) * axU.y) / axisLen;

  // METRIC 1 — energy-travel (reported, NOT load-bearing for a centered lifecycle)
  function centroid(e, thr) { let sx = 0, sy = 0, sw = 0, n = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = y * w + x, ww = e[p];
      if (ww >= thr) { sx += x * ww; sy += y * ww; sw += ww; n++; } }
    if (sw === 0) return { x: -1, y: -1, mass: 0, px: 0 };
    return { x: sx / sw / w, y: sy / sw / h, mass: sw, px: n }; }
  const cents = energy.map(e => centroid(e, SPELL_THRESH));
  const cores = energy.map(e => centroid(e, CORE_THRESH));
  const travel = cents.map((c, t) => { const co = cores[t]; return {
    frame: FRAME_IDX[t], beat: BEAT[t],
    core_cx: co.x < 0 ? null : +(co.x * 100).toFixed(1), core_cy: co.y < 0 ? null : +(co.y * 100).toFixed(1),
    core_axis_frac: co.x < 0 ? null : +projOnAxis(co.x, co.y).toFixed(3), core_px: co.px,
    full_cx: c.x < 0 ? null : +(c.x * 100).toFixed(1), full_cy: c.y < 0 ? null : +(c.y * 100).toFixed(1),
    full_px: c.px, full_mass: +c.mass.toFixed(0) }; });
  const early = cores.find(c => c.x >= 0);
  const lateIdx = [4, 5, 6, 3].find(i => cores[i] && cores[i].x >= 0);
  const late = lateIdx !== undefined ? cores[lateIdx] : null;
  const netDispX = (early && late) ? +((late.x - early.x) * 100).toFixed(1) : null;

  // GROWTH read (the meaningful lifecycle signal): full-mask px emerge->peak->residual
  const maskPxSeq = cents.map(c => c.px);
  const massSeq = cents.map(c => +c.mass.toFixed(0));
  const peakMaskPx = Math.max(...maskPxSeq);
  const peakMass = Math.max(...massSeq);
  const emergeMaskPx = maskPxSeq[0];
  const growthRatio = emergeMaskPx > 0 ? +(peakMaskPx / emergeMaskPx).toFixed(2) : null;

  // METRIC 2 — inter-frame motion-presence (LOAD-BEARING: live verb vs frozen decal)
  const motion = [];
  for (let t = 1; t < N; t++) { let sum = 0, n = 0, sx = 0, sy = 0, sw = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = y * w + x;
      const d = Math.abs(energy[t][p] - energy[t - 1][p]);
      if (unionMask[p]) { sum += d; n++; }
      if (d >= SPELL_THRESH) { sx += x * d; sy += y * d; sw += d; } }
    motion.push({ pair: `${FRAME_IDX[t - 1]}->${FRAME_IDX[t]}`, beat: `${BEAT[t - 1]}->${BEAT[t]}`,
      mean_delta_in_region: n ? +(sum / n).toFixed(2) : 0,
      delta_centroid_x: sw ? +(sx / sw / w * 100).toFixed(1) : null,
      delta_centroid_y: sw ? +(sy / sw / h * 100).toFixed(1) : null }); }
  const meanMotion = +(motion.reduce((a, m) => a + m.mean_delta_in_region, 0) / motion.length).toFixed(2);
  const dcx = motion.map(m => m.delta_centroid_x).filter(v => v !== null);
  const propagationSpanX = dcx.length ? +(Math.max(...dcx) - Math.min(...dcx)).toFixed(1) : 0;

  // METRIC 3 — fire-hue legibility (LOAD-BEARING)
  const hue = [];
  for (let t = 0; t < N; t++) { const fr = frames[t], m = mask[t];
    const hist = new Array(36).fill(0); let fireN = 0, tot = 0, meanR = 0, meanG = 0, meanB = 0;
    for (let p = 0, i = 0; p < P; p++, i += 3) { if (!m[p]) continue;
      const r = fr.rgb[i], g = fr.rgb[i + 1], b = fr.rgb[i + 2]; const hd = hueDeg(r, g, b);
      tot++; meanR += r; meanG += g; meanB += b;
      if (hd >= 0) hist[Math.min(35, Math.floor(hd / 10))]++;
      if (hd >= FIRE_HUE_LO && hd <= FIRE_HUE_HI) fireN++; }
    let domBin = -1, domVal = -1; for (let b = 0; b < 36; b++) if (hist[b] > domVal) { domVal = hist[b]; domBin = b; }
    hue.push({ frame: FRAME_IDX[t], beat: BEAT[t], mask_px: tot,
      dominant_hue_deg: tot ? `${domBin * 10}-${domBin * 10 + 10}` : null,
      fire_band_frac: tot ? +(fireN / tot).toFixed(3) : null,
      mean_rgb: tot ? [Math.round(meanR / tot), Math.round(meanG / tot), Math.round(meanB / tot)] : null }); }
  const hueFracs = hue.map(x => x.fire_band_frac).filter(v => v !== null);
  const meanHue = hueFracs.length ? +(hueFracs.reduce((a, b) => a + b, 0) / hueFracs.length).toFixed(3) : null;
  const peakHue = hueFracs.length ? +Math.max(...hueFracs).toFixed(3) : null;

  // METRIC 4 — premium-layering (LOAD-BEARING depth axis)
  const layering = [];
  for (let t = 0; t < N; t++) { const L = lumaF[t], m = mask[t]; let s = 0, n = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = y * w + x; if (!m[p]) continue;
      s += localStd(L, w, h, x, y); n++; }
    layering.push({ frame: FRAME_IDX[t], beat: BEAT[t], mask_px: n, mean_local_std: n ? +(s / n).toFixed(2) : null }); }
  const layVals = layering.map(x => x.mean_local_std).filter(v => v !== null);
  const meanLayering = layVals.length ? +(layVals.reduce((a, b) => a + b, 0) / layVals.length).toFixed(2) : null;
  const peakLayering = layVals.length ? +Math.max(...layVals).toFixed(2) : null;

  // METRIC 5 — directionality (reported, NOT load-bearing for a centered lifecycle)
  function pca(e) { let sw = 0, mx = 0, my = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = y * w + x, ww = e[p]; if (ww < SPELL_THRESH) continue;
      sw += ww; mx += x * ww; my += y * ww; }
    if (sw === 0) return null; mx /= sw; my /= sw;
    let cxx = 0, cyy = 0, cxy = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const p = y * w + x, ww = e[p]; if (ww < SPELL_THRESH) continue;
      const dx = x - mx, dy = y - my; cxx += ww * dx * dx; cyy += ww * dy * dy; cxy += ww * dx * dy; }
    cxx /= sw; cyy /= sw; cxy /= sw;
    const tr = cxx + cyy, det = cxx * cyy - cxy * cxy; const disc = Math.sqrt(Math.max(0, tr * tr / 4 - det));
    const l1 = tr / 2 + disc, l2 = tr / 2 - disc; let vx, vy;
    if (Math.abs(cxy) > 1e-6) { vx = l1 - cyy; vy = cxy; } else { vx = cxx >= cyy ? 1 : 0; vy = cxx >= cyy ? 0 : 1; }
    const vn = Math.hypot(vx, vy) || 1; vx /= vn; vy /= vn;
    return { l1, l2, elong: l2 > 1e-6 ? Math.sqrt(l1 / l2) : Infinity, vx, vy }; }
  const axPxX = (THREAT.x - CASTER.x) * w, axPxY = (THREAT.y - CASTER.y) * h;
  const axPxN = Math.hypot(axPxX, axPxY); const axDir = { x: axPxX / axPxN, y: axPxY / axPxN };
  const direction = [];
  for (let t = 0; t < N; t++) { const pc = pca(energy[t]);
    if (!pc) { direction.push({ frame: FRAME_IDX[t], beat: BEAT[t], elongation: null }); continue; }
    const dot = Math.abs(pc.vx * axDir.x + pc.vy * axDir.y);
    direction.push({ frame: FRAME_IDX[t], beat: BEAT[t], elongation: +pc.elong.toFixed(2), axis_align_cos: +dot.toFixed(3) }); }
  const elongs = direction.map(d => d.elongation).filter(v => v !== null && isFinite(v));
  const meanElong = elongs.length ? +(elongs.reduce((a, b) => a + b, 0) / elongs.length).toFixed(2) : null;

  // backdrop-invariance (OUTSIDE union mask)
  let outN = 0; for (let p = 0; p < P; p++) if (!unionMask[p]) outN++;
  const backdrop = [];
  for (let t = 0; t < N; t++) { let dL = 0;
    for (let p = 0; p < P; p++) { if (unionMask[p]) continue; dL += Math.abs(lumaF[t][p] - lumaF[0][p]); }
    backdrop.push({ frame: FRAME_IDX[t], backdrop_luma_drift_vs_F0: +(dL / outN).toFixed(3) }); }
  const maxBackdropDrift = Math.max(...backdrop.map(b => b.backdrop_luma_drift_vs_F0));

  return {
    variant, files,
    metric1_energy_travel_NOT_LOADBEARING: { note: 'centered lifecycle, no caster->threat axis — axis-frac not meaningful', per_frame: travel, net_core_dispX_pct: netDispX },
    lifecycle_growth: { mask_px_seq: maskPxSeq, mass_seq: massSeq, emerge_mask_px: emergeMaskPx, peak_mask_px: peakMaskPx, peak_mass: peakMass, growth_ratio_peak_over_emerge: growthRatio },
    metric2_motion_presence: { pairs: motion, mean_inter_frame_delta: meanMotion, propagation_span_x_pct: propagationSpanX },
    metric3_fire_hue: { per_frame: hue, mean_fire_band_frac: meanHue, peak_fire_band_frac: peakHue },
    metric4_premium_layering: { per_frame: layering, mean_local_std: meanLayering, peak_local_std: peakLayering },
    metric5_directionality_NOT_LOADBEARING: { note: 'centered lifecycle — axis-align not meaningful', per_frame: direction, mean_elongation: meanElong },
    backdrop_invariance: { per_frame: backdrop, max_luma_drift: +maxBackdropDrift.toFixed(3), invariant: maxBackdropDrift <= BACKDROP_DRIFT_TOL },
    SUMMARY: {
      mean_motion_presence: meanMotion,
      mean_fire_band_frac: meanHue, peak_fire_band_frac: peakHue,
      mean_layering_local_std: meanLayering, peak_layering_local_std: peakLayering,
      lifecycle_growth_ratio: growthRatio, peak_mask_px: peakMaskPx,
    },
  };
}

// ──────────────────────────── run all variants + compute deltas ────────────────────────────
process.stderr.write('scoring v0, v1, v2 (7 frames each)...\n');
const results = {};
for (const v of VARIANTS) results[v] = await scoreVariant(v);

const d = (a, b) => +(a - b).toFixed(3);
const v0 = results.v0.SUMMARY, v1 = results.v1.SUMMARY, v2 = results.v2.SUMMARY;
const deltas = {
  'V1-V0 (THE HEADLINE)': {
    motion_presence: d(v1.mean_motion_presence, v0.mean_motion_presence),
    peak_layering: d(v1.peak_layering_local_std, v0.peak_layering_local_std),
    mean_layering: d(v1.mean_layering_local_std, v0.mean_layering_local_std),
    peak_fire_band_frac: d(v1.peak_fire_band_frac, v0.peak_fire_band_frac),
    mean_fire_band_frac: d(v1.mean_fire_band_frac, v0.mean_fire_band_frac),
    peak_mask_px: v1.peak_mask_px - v0.peak_mask_px,
    note: 'positive motion/layering delta = the emission+sub-emitter lever adds live-verb + depth in-engine. NEGATIVE fire-band delta = the white-hot-core hue cost (additive blows the core white, OUT of the fire band) — premium-bloom-WITH-hue-cost, the eye<->number divergence.',
  },
  'V2-V1 (harvest cross-check)': {
    motion_presence: d(v2.mean_motion_presence, v1.mean_motion_presence),
    peak_layering: d(v2.peak_layering_local_std, v1.peak_layering_local_std),
    peak_fire_band_frac: d(v2.peak_fire_band_frac, v1.peak_fire_band_frac),
    note: 'V2>>V1 on juice axes = flipbook structurally richer => harvest worth it. V2<=V1 => no harvest needed.',
  },
};

const out = {
  scored_at: new Date().toISOString(),
  instrument: 'spell-motion-score-drax-vfx-register.mjs (galadriel Wave-2 PARAMETERIZED sidecar; methodology VERBATIM from locked spell-motion-score.mjs; locked instrument NOT edited)',
  inputs: { dir: DIR, variants: VARIANTS, frame_indices: FRAME_IDX, beats: BEAT },
  geometry_applicability_caveat: 'drax captures are a CENTERED IN-PLACE LIFECYCLE (emerge->grow->peak->fade, core ~48% x throughout), NOT a directed caster->threat projectile strip. M1 energy-travel + M5 directionality are reported but NOT load-bearing (no caster/threat axis exists). The load-bearing temporal axis is M2 motion-presence (+ lifecycle growth); M3 fire-hue + M4 layering are per-frame depth/element reads. Surfaced not papered-over.',
  background_caveat: 'Stage background measured at luma ~129 (mid-grey RGB[128,128,139]), IDENTICAL across all variants — controlled comparison holds. NOTE: this is mid-grey, NOT the 0.10 dark-neutral the Wave-2 handoff stated; flagged in the report. Additive-floor subtraction is valid (static rig, grey bg has ~0 warm-luma so it does not enter the spell field).',
  thresholds: { SPELL_THRESH, CORE_THRESH, WARM_MARGIN, FIRE_HUE_BAND_DEG: [FIRE_HUE_LO, FIRE_HUE_HI] },
  per_variant: results,
  deltas,
};
const outPath = join(process.cwd(), 'spell-motion-score-drax-vfx-register.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ──────────────────────────── console report ────────────────────────────
const L = console.log;
L('══════════════════════════════════════════════════════════════════════════════════════════');
L('  SPELL-MOTION (drax VFX-register sidecar) — V0/V1/V2 fire lifecycle, 7 frames each');
L('  methodology VERBATIM from locked spell-motion-score.mjs; centered-lifecycle applicability caveat applies');
L('══════════════════════════════════════════════════════════════════════════════════════════\n');
for (const v of VARIANTS) {
  const s = results[v].SUMMARY;
  L(`── ${v.toUpperCase()} ──  motion=${s.mean_motion_presence}  layering(mean/peak)=${s.mean_layering_local_std}/${s.peak_layering_local_std}  fire-band(mean/peak)=${s.mean_fire_band_frac}/${s.peak_fire_band_frac}  growth=${s.lifecycle_growth_ratio}x  peak-px=${s.peak_mask_px}`);
}
L('\n── V1-V0 DELTA (THE HEADLINE) ──');
for (const [k, val] of Object.entries(deltas['V1-V0 (THE HEADLINE)'])) if (k !== 'note') L(`   ${k.padEnd(22)} ${val}`);
L('\n── V2-V1 DELTA (harvest cross-check) ──');
for (const [k, val] of Object.entries(deltas['V2-V1 (harvest cross-check)'])) if (k !== 'note') L(`   ${k.padEnd(22)} ${val}`);
L(`\nwrote ${outPath}`);
