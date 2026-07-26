// gd-gp-calib-c4-nameplate.mjs — C4 / extraction target E4: monster nameplate.
//
// Truth (fixtures.db `fixture_set` L0-gd-s3-set1 + elrond A1):
//   line 1 = "Walking Dead"  ·  level = 6  ·  line 3 = "Aether Corruption"
//
// FINDING filed by this script: the protocol § 4.4 table says the calibration source is
// "6 zombie trial frames". It is THREE. The *_end frames carry no nameplate at all — the
// monster is dead and the target frame has cleared. The nameplate calibration n is 3.
//
// The nameplate font is BLACKLETTER. Tesseract `eng` mangles it; `frk` (Fraktur) is the
// correct model and is what this script uses for the two text lines. The level numeral is
// a ~10x7 px colour-keyed glyph and needs psm 8 with a digit whitelist.
//
// METHOD LAW: masks are computed on native-resolution pixels; the only resampling is an
// integer nearest-neighbour upscale of the binary mask for OCR legibility.
//
// Usage: node gd-gp-calib-c4-nameplate.mjs

import path from 'node:path';
import sharp from 'sharp';
import { createWorker } from 'tesseract.js';
import { STILLS_V3, TRIAL_FRAMES, WORK, ensureDirs, rawRegion, px, writeJSON } from './gd-gp-calib-lib.mjs';

// ------------------------------------------------------------------- geometry
// Located by bright-ink row/column profiling of the top-centre target frame; identical
// in all three start frames (GD anchors the target frame to screen top-centre, so these
// offsets transfer to video frames at the same 1920x1080 / same UI scale).
export const NAME_BOX = { left: 868, top: 13, width: 184, height: 24 };
export const LEVEL_BOX = { left: 948, top: 41, width: 28, height: 16 };
export const THIRD_BOX = { left: 868, top: 88, width: 184, height: 18 };
// The target-frame chrome (gold bar surround). Presence of a nameplate is decided on
// THIS, not on ink count in the name band — bright world background can put >120 ink
// pixels in the name band on a frame with no target at all (observed on t3e).
export const CHROME_BOX = { left: 870, top: 52, width: 200, height: 16 };
const CHROME_MIN_GOLD_PX = 150; // observed: 396-405 present, 0 absent. Wide margin.

async function chromeGoldCount(src) {
  const reg = await rawRegion(src, CHROME_BOX);
  let gold = 0;
  for (let y = 0; y < reg.height; y++)
    for (let x = 0; x < reg.width; x++) {
      const [r, g, b] = px(reg, x, y);
      if (r > 150 && g > 110 && g < 200 && b < 150 && r - b > 60) gold++;
    }
  return gold;
}

// Nameplate ink: bright + low-saturation (cream/white). Rank is encoded in this colour,
// so the mean ink RGB is banked per frame as the rank-classifier feature (§ 4.3).
const inkPred = ([r, g, b]) => {
  const L = 0.299 * r + 0.587 * g + 0.114 * b;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
  return L > 150 && (mx ? (mx - mn) / mx : 0) < 0.35;
};
// Level numeral: GD colour-codes it by level differential. Keys the green/yellow band
// (at-level) and the orange/red band (above-level).
const levelPred = ([r, g, b]) =>
  (g > 110 && g - b > 55 && r > 80) || (r > 150 && g > 90 && b < 90 && r - b > 70);

async function maskCrop(src, box, name, pred, scale) {
  const reg = await rawRegion(src, box);
  const buf = Buffer.alloc(reg.width * reg.height);
  const ink = [];
  for (let y = 0; y < reg.height; y++)
    for (let x = 0; x < reg.width; x++) {
      const p = px(reg, x, y);
      const on = pred(p);
      buf[y * reg.width + x] = on ? 0 : 255; // black ink on white
      if (on) ink.push(p);
    }
  const out = path.join(WORK, 'upscaled', `${name}.png`);
  await sharp(buf, { raw: { width: reg.width, height: reg.height, channels: 1 } })
    .resize({ width: reg.width * scale, height: reg.height * scale, kernel: 'nearest' })
    .extend({ top: 24, bottom: 24, left: 24, right: 24, background: { r: 255, g: 255, b: 255 } })
    .png()
    .toFile(out);
  const meanInk = ink.length
    ? ink.reduce((a, p) => [a[0] + p[0], a[1] + p[1], a[2] + p[2]], [0, 0, 0]).map((v) => Math.round(v / ink.length))
    : null;
  return { out, inkPixels: ink.length, meanInk };
}

// ------------------------------------------------------------------ scoring utils
export function levenshtein(a, b) {
  const m = a.length, n = b.length;
  if (!m) return n; if (!n) return m;
  let prev = Array.from({ length: n + 1 }, (_, j) => j);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++)
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    prev = cur;
  }
  return prev[n];
}
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9 ]/g, '').replace(/\s+/g, ' ').trim();

// ---------------------------------------------------------------------------- main
const TRUTH = { name: 'Walking Dead', level: 6, third: 'Aether Corruption' };

async function main() {
  await ensureDirs();
  const wf = await createWorker('frk');
  await wf.setParameters({ tessedit_pageseg_mode: '7' });
  const wd = await createWorker('eng');
  await wd.setParameters({ tessedit_pageseg_mode: '8', tessedit_char_whitelist: '0123456789' });

  const frames = [];
  for (const [k, file] of Object.entries(TRIAL_FRAMES)) {
    const src = path.join(STILLS_V3, file);
    const gold = await chromeGoldCount(src);
    const present = gold >= CHROME_MIN_GOLD_PX;

    const nm = await maskCrop(src, NAME_BOX, `c4-name-${k}`, inkPred, 8);
    const th = await maskCrop(src, THIRD_BOX, `c4-third-${k}`, inkPred, 8);
    const lv = await maskCrop(src, LEVEL_BOX, `c4-level-${k}`, levelPred, 16);

    // No target frame -> nothing to read. Do not run OCR on world background.
    const rn = present ? (await wf.recognize(nm.out)).data : { text: '', confidence: 0 };
    const rt = present ? (await wf.recognize(th.out)).data : { text: '', confidence: 0 };
    const rl = present ? (await wd.recognize(lv.out)).data : { text: '', confidence: 0 };

    const nameOcr = rn.text.trim();
    const thirdOcr = rt.text.trim();
    const levelOcr = rl.text.trim();

    frames.push({
      frame: k,
      source: file,
      nameplate_present_detected: present,
      chrome_gold_px: gold,
      ink_pixels: { name: nm.inkPixels, third: th.inkPixels, level: lv.inkPixels },
      rank_feature_mean_ink_rgb: nm.meanInk, // § 4.3 rank classifier feature
      name: {
        ocr: nameOcr, confidence: rn.confidence,
        exact: nameOcr === TRUTH.name,
        normalized_exact: norm(nameOcr) === norm(TRUTH.name),
        cer: TRUTH.name.length ? levenshtein(nameOcr, TRUTH.name) / TRUTH.name.length : null,
      },
      level: {
        ocr: levelOcr === '' ? null : parseInt(levelOcr, 10),
        confidence: rl.confidence,
        exact: parseInt(levelOcr, 10) === TRUTH.level,
      },
      third_line: {
        ocr: thirdOcr, confidence: rt.confidence,
        exact: thirdOcr === TRUTH.third,
        normalized_exact: norm(thirdOcr) === norm(TRUTH.third),
        cer: levenshtein(thirdOcr, TRUTH.third) / TRUTH.third.length,
      },
      crops: { name: NAME_BOX, level: LEVEL_BOX, third: THIRD_BOX },
    });
  }
  await wf.terminate();
  await wd.terminate();

  const withPlate = frames.filter((f) => f.nameplate_present_detected);
  const agg = (sel) => ({
    n: withPlate.length,
    exact: withPlate.filter((f) => sel(f).exact).length,
    normalized_exact: withPlate.filter((f) => sel(f).normalized_exact).length,
    mean_cer: withPlate.reduce((a, f) => a + (sel(f).cer ?? 0), 0) / (withPlate.length || 1),
  });

  const report = {
    capability: 'C4 nameplate OCR (E4)',
    generated: new Date().toISOString(),
    method_law: 'colour/luminance mask on native-resolution pixels; 8x/16x nearest upscale of the binary mask for OCR only',
    engines: { text_lines: 'tesseract.js frk (Fraktur) psm 7', level_numeral: 'tesseract.js eng psm 8, whitelist 0-9' },
    truth: TRUTH,
    finding_calibration_n:
      'Protocol § 4.4 lists 6 zombie trial frames as the E4 calibration source. Only the 3 *_start frames carry a nameplate; the 3 *_end frames have none (target cleared on death). n = 3, not 6.',
    nameplate_presence_detection: {
      detected_present: frames.filter((f) => f.nameplate_present_detected).map((f) => f.frame),
      detected_absent: frames.filter((f) => !f.nameplate_present_detected).map((f) => f.frame),
      correct: frames.every((f) => f.nameplate_present_detected === f.frame.endsWith('s')),
      detector: `target-frame gold chrome pixel count in ${JSON.stringify(CHROME_BOX)} >= ${CHROME_MIN_GOLD_PX}`,
      counts: Object.fromEntries(frames.map((f) => [f.frame, f.chrome_gold_px])),
    },
    name_line: agg((f) => f.name),
    level_numeral: { n: withPlate.length, exact: withPlate.filter((f) => f.level.exact).length },
    third_line: agg((f) => f.third_line),
    rank_calibration: {
      classes_with_a_calibration_source: ['normal'],
      classes_without: ['champion', 'hero', 'boss'],
      normal_ink_rgb_samples: withPlate.map((f) => ({ frame: f.frame, rgb: f.rank_feature_mean_ink_rgb })),
      note: 'Protocol § 2.1 item 8 (the three rank tooltips) remains the only calibration blocker. One class does not make a classifier.',
    },
    frames,
  };
  const p = await writeJSON('c4-nameplate.json', report);

  console.log(`[C4] nameplate presence: ${report.nameplate_presence_detection.correct ? 'CORRECT on 6/6 frames' : 'MISDETECTED'} (present ${report.nameplate_presence_detection.detected_present.join(',')} | absent ${report.nameplate_presence_detection.detected_absent.join(',')})`);
  for (const f of withPlate)
    console.log(
      `  ${f.frame}  name=${JSON.stringify(f.name.ocr)} exact=${f.name.exact} norm=${f.name.normalized_exact} CER=${f.name.cer.toFixed(3)}` +
        `  level=${f.level.ocr} exact=${f.level.exact}` +
        `  third=${JSON.stringify(f.third_line.ocr)} CER=${f.third_line.cer.toFixed(3)}`
    );
  console.log(`  name line:  exact ${report.name_line.exact}/${report.name_line.n}, normalized ${report.name_line.normalized_exact}/${report.name_line.n}, mean CER ${report.name_line.mean_cer.toFixed(3)}`);
  console.log(`  level:      exact ${report.level_numeral.exact}/${report.level_numeral.n}`);
  console.log(`  third line: exact ${report.third_line.exact}/${report.third_line.n}, normalized ${report.third_line.normalized_exact}/${report.third_line.n}, mean CER ${report.third_line.mean_cer.toFixed(3)}`);
  console.log('->', p);
}

await main();
