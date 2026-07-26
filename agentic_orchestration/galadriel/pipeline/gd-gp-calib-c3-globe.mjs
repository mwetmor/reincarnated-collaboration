// gd-gp-calib-c3-globe.mjs — C3 / extraction target E3: HP globe.
//
// Two sub-capabilities are scored separately because they turn out to be very
// different instruments on the same pixels:
//
//   C3a  GLOBE-NUMERAL OCR   — read the `NNN/NNN` overlay text off the orb.
//                              Scored against hp_current / hp_max in fixtures.db.
//   C3b  FILL-FRACTION       — the method the protocol § 4.4 actually specified:
//                              locate the liquid boundary and report filled fraction.
//                              Scored against the two labelled points 282/282 (100 %)
//                              and 269/282 (95.4 %).
//
// METHOD LAW: all measurement is on native-resolution pixels. The only resampling is
// an integer nearest-neighbour upscale of the numeral crop for OCR legibility.
//
// Usage: node gd-gp-calib-c3-globe.mjs

import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createWorker } from 'tesseract.js';
import { FIXTURES_DB, WORK, ensureDirs, cropNative, rawRegion, px, writeJSON } from './gd-gp-calib-lib.mjs';

const REPO = '/Users/admin/Games/reincarnated-collaboration';

// ------------------------------------------------------------------- geometry
// Located from native 1x/3x probe crops of the bottom-left HUD. The orb is anchored to
// the screen edge; identical offset in round-2 and round-3 stills.
export const ORB = { cx: 630, cy: 1013, r: 58 };
// The numeral overlay sits horizontally centred on the orb, slightly above centre.
export const NUMERAL_BOX = { left: 572, top: 994, width: 120, height: 34 };

const isRed = (r, g, b) => r > 55 && r - g > 22 && r - b > 18;
const isNumeralInk = (r, g, b) => r > 170 && g > 170 && b > 170;

/**
 * C3b — fill fraction by liquid-boundary detection.
 * For each scanline inside the inscribed circle, compute the red fraction of the chord,
 * ignoring numeral-ink pixels. The liquid surface, if it exists as a boundary, is the
 * topmost run of rows whose red fraction is below `emptyThreshold`.
 * Returns the profile as well as the estimate, so the estimate is auditable.
 */
export async function fillFraction(srcPath, { emptyThreshold = 0.35, runLen = 3 } = {}) {
  const { cx, cy, r } = ORB;
  const box = { left: cx - r, top: cy - r, width: 2 * r, height: 2 * r };
  const reg = await rawRegion(srcPath, box);
  const profile = [];
  for (let y = 0; y < reg.height; y++) {
    const dy = box.top + y - cy;
    if (Math.abs(dy) > r) { profile.push(null); continue; }
    const half = Math.sqrt(r * r - dy * dy);
    let red = 0, tot = 0;
    for (let x = 0; x < reg.width; x++) {
      const dx = box.left + x - cx;
      if (Math.abs(dx) > half) continue;
      const [pr, pg, pb] = px(reg, x, y);
      if (isNumeralInk(pr, pg, pb)) continue;
      tot++;
      if (isRed(pr, pg, pb)) red++;
    }
    profile.push(tot ? red / tot : null);
  }
  // Topmost sustained empty run, measured from the top of the orb downward.
  let boundaryRow = null, run = 0;
  for (let y = 0; y < profile.length; y++) {
    const v = profile[y];
    if (v === null) { run = 0; continue; }
    if (v < emptyThreshold) { run++; if (run >= runLen && boundaryRow === null) boundaryRow = y - run + 1; }
    else run = 0;
  }
  // If no empty run is found at the top, the orb reads as full.
  // Linear-height model (GD renders the orb liquid as a horizontal surface).
  const heightFrac = boundaryRow === null ? 1.0 : 1 - boundaryRow / (2 * r);
  // Circle-area model, for comparison — a cap of height h on a circle of radius r.
  let areaFrac = 1.0;
  if (boundaryRow !== null) {
    const h = boundaryRow; // cap height in px from the top of the circle
    const d = r - h;
    const capArea = r * r * Math.acos(d / r) - d * Math.sqrt(Math.max(0, r * r - d * d));
    areaFrac = 1 - capArea / (Math.PI * r * r);
  }
  return { boundaryRow, heightFrac, areaFrac, profile, params: { emptyThreshold, runLen } };
}

// ------------------------------------------------------------------ ground truth
function loadCaptures() {
  const rows = JSON.parse(
    execFileSync('sqlite3', ['-json', FIXTURES_DB, 'select capture_id, path from capture'], { encoding: 'utf8' })
  );
  return Object.fromEntries(rows.map((r) => [r.capture_id, path.join(REPO, r.path)]));
}

function loadHpTruth() {
  const rows = JSON.parse(
    execFileSync(
      'sqlite3',
      [
        '-json',
        FIXTURES_DB,
        `select capture_id, measure_key, value_num, verbatim, read_method
         from trial_measurement
         where measure_key in ('hp_current','hp_max') and capture_id is not null`,
      ],
      { encoding: 'utf8' }
    )
  );
  const byCapture = {};
  for (const r of rows) (byCapture[r.capture_id] ||= {})[r.measure_key] = r;
  return byCapture;
}

// ---------------------------------------------------------------------------- main
async function main() {
  await ensureDirs();
  const captures = loadCaptures();
  const truth = loadHpTruth();

  const worker = await createWorker('eng');
  await worker.setParameters({
    tessedit_char_whitelist: '0123456789/',
    tessedit_pageseg_mode: '7', // single text line
  });

  // Numeral OCR is attempted on every capture that has an orb on screen: all 6 round-3
  // trial frames plus the round-2 panel shots. Only frames with banked hp values score.
  const candidates = Object.keys(captures).filter(
    (id) => /s3\/t[123][se]$/.test(id) || /s2\/1[3-8]$/.test(id)
  );

  const frames = [];
  let hpHit = 0, hpMiss = 0, hpScored = 0;

  for (const id of candidates) {
    const src = captures[id];
    const safe = id.replace(/[^A-Za-z0-9]/g, '_');
    const { upPath } = await cropNative(src, NUMERAL_BOX, `c3-numeral-${safe}`, {
      scale: 6, grayscale: true, normalize: true,
    });
    const { data } = await worker.recognize(upPath);
    const text = data.text.trim();
    const m = text.match(/(\d+)\s*\/\s*(\d+)/);
    const ocr = m ? { hp_current: +m[1], hp_max: +m[2] } : null;

    const fill = await fillFraction(src);

    const t = truth[id];
    const scored = [];
    if (t) {
      for (const key of ['hp_current', 'hp_max']) {
        if (!t[key] || t[key].read_method === 'absent' || t[key].value_num === null) continue;
        hpScored++;
        const got = ocr ? ocr[key] : null;
        const ok = got !== null && Math.abs(got - t[key].value_num) < 1e-9;
        if (ok) hpHit++; else hpMiss++;
        scored.push({ measure_key: key, truth: t[key].value_num, ocr: got, verbatim: t[key].verbatim, verdict: ok ? 'HIT' : got === null ? 'NO-READ' : 'MISREAD' });
      }
    }

    frames.push({
      capture_id: id,
      source: path.relative(REPO, src),
      numeral_crop: NUMERAL_BOX,
      numeral_upscaled: path.relative(WORK, upPath),
      numeral_ocr_raw: text,
      numeral_ocr: ocr,
      numeral_confidence: data.confidence,
      numeral_scored: scored,
      fill_fraction: {
        boundary_row: fill.boundaryRow,
        height_model: fill.heightFrac,
        area_model: fill.areaFrac,
        params: fill.params,
        top_of_orb_red_profile: fill.profile.slice(0, 24).map((v) => (v === null ? null : +v.toFixed(3))),
      },
      // The ratio the fill fraction is *supposed* to reproduce, where OCR supplies it.
      implied_true_fraction: ocr ? ocr.hp_current / ocr.hp_max : null,
    });
  }

  await worker.terminate();

  // C3b scoring against the two labelled points.
  const labelled = frames.filter((f) => f.implied_true_fraction !== null);
  const c3bResiduals = labelled.map((f) => ({
    capture_id: f.capture_id,
    truth: f.implied_true_fraction,
    height_model: f.fill_fraction.height_model,
    residual: f.fill_fraction.height_model - f.implied_true_fraction,
  }));
  const distinctTruth = [...new Set(labelled.map((f) => f.implied_true_fraction.toFixed(4)))];
  const distinctEst = [...new Set(labelled.map((f) => f.fill_fraction.height_model.toFixed(4)))];

  // Is the estimator even ORDER-consistent with truth? Count discordant pairs.
  let concordant = 0, discordant = 0, tiedTruth = 0;
  for (let i = 0; i < labelled.length; i++)
    for (let j = i + 1; j < labelled.length; j++) {
      const dt = labelled[i].implied_true_fraction - labelled[j].implied_true_fraction;
      const de = labelled[i].fill_fraction.height_model - labelled[j].fill_fraction.height_model;
      if (Math.abs(dt) < 1e-9) { tiedTruth++; continue; }
      if (dt * de > 0) concordant++;
      else if (dt * de < 0) discordant++;
    }
  // Spread of the estimator across frames whose truth is identical (all 100 % full).
  const fullFrames = labelled.filter((f) => Math.abs(f.implied_true_fraction - 1) < 1e-9);
  const fullEst = fullFrames.map((f) => f.fill_fraction.height_model);
  const nullSpread = fullEst.length ? { min: Math.min(...fullEst), max: Math.max(...fullEst) } : null;

  const report = {
    capability: 'C3 HP globe (E3)',
    generated: new Date().toISOString(),
    method_law: 'all measurement on native-resolution pixels; numeral crop upscaled 6x nearest for OCR only',
    orb_geometry: ORB,
    numeral_box: NUMERAL_BOX,
    c3a_numeral_ocr: {
      engine: 'tesseract.js 6 (eng), psm 7, whitelist 0-9/',
      frames_attempted: frames.length,
      frames_read: frames.filter((f) => f.numeral_ocr).length,
      banked_fields_scored: hpScored,
      hits: hpHit,
      misses: hpMiss,
      accuracy: hpScored ? hpHit / hpScored : null,
    },
    c3b_fill_fraction: {
      labelled_points: distinctTruth,
      distinct_estimates_produced: distinctEst,
      // NOT a quality metric — different numbers can still be wrong numbers.
      produces_varying_estimates: distinctEst.length > 1,
      order_consistency: { concordant_pairs: concordant, discordant_pairs: discordant, tied_truth_pairs: tiedTruth },
      // The null band: how far the estimator wanders on frames whose truth is IDENTICAL.
      // If this band is wider than the labelled separation (4.61 pp), the method cannot
      // resolve the phenomenon at all.
      null_band_on_identical_truth: nullSpread,
      labelled_separation: 1 - 269 / 282,
      residuals: c3bResiduals,
    },
    frames,
  };
  const p = await writeJSON('c3-globe.json', report);

  console.log(`[C3a numeral OCR] ${hpHit}/${hpScored} banked fields exact` + (hpScored ? ` = ${(100 * hpHit / hpScored).toFixed(1)}%` : ''));
  for (const f of frames) console.log(`  ${f.capture_id.padEnd(30)} OCR=${JSON.stringify(f.numeral_ocr_raw)} conf=${f.numeral_confidence?.toFixed?.(0)}` + (f.numeral_scored.length ? `  banked: ${f.numeral_scored.map((s) => `${s.measure_key} ${s.verdict}`).join(', ')}` : '  (no banked hp row)'));
  console.log(`[C3b fill fraction] truth values present: ${distinctTruth.join(', ')}`);
  console.log(`                    estimates produced:   ${distinctEst.join(', ')}`);
  console.log(`                    labelled separation:  ${(100 * report.c3b_fill_fraction.labelled_separation).toFixed(2)} pp`);
  console.log(`                    null band on IDENTICAL-truth frames: ${nullSpread ? `${nullSpread.min.toFixed(4)} .. ${nullSpread.max.toFixed(4)} (${(100 * (nullSpread.max - nullSpread.min)).toFixed(1)} pp)` : 'n/a'}`);
  console.log(`                    order consistency: ${concordant} concordant / ${discordant} discordant pairs`);
  for (const r of c3bResiduals) console.log(`  ${r.capture_id.padEnd(30)} truth ${r.truth.toFixed(4)}  est ${r.height_model.toFixed(4)}  residual ${r.residual >= 0 ? '+' : ''}${r.residual.toFixed(4)}`);
  console.log('->', p);
}

await main();
