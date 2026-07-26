// gd-gp-calib-lib.mjs — shared harness for the GD general-play CV calibration (protocol G4).
//
// METHOD LAW (inherited from M3 / protocol § 4.4):
//   No digit is ever read off a downscaled frame. Crops are taken at NATIVE resolution
//   (1920x1080 source), then upscaled for legibility only. Downscaled renders exist ONLY
//   under overview/ and are named LOCATOR-*; nothing is ever read from them.
//
// Author: galadriel (visual-perception steward), 2026-07-26.

import sharp from 'sharp';
import path from 'node:path';
import fs from 'node:fs/promises';

export const STILLS_V3 =
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/knowledge/gd/live-probe-3';
export const STILLS_V1 =
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/knowledge/gd/live-probe-1';
export const STILLS_V2 =
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/knowledge/gd/live-probe-2';
export const WORK =
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-26-gd-gp-calibration';
export const FIXTURES_DB =
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/fixtures.db';

// The six round-3 trial frames, keyed by their fixtures.db capture_id suffix.
export const TRIAL_FRAMES = {
  t1s: 'zombie-01-start.png',
  t1e: 'zombie-01-end.png',
  t2s: 'zombie_02_start.png',
  t2e: 'zombie_02_end.png',
  t3s: 'zombie-03-start.png',
  t3e: 'zombie-03-end.png',
};

export const SHEET_FRAMES = Object.fromEntries(
  Array.from({ length: 12 }, (_, i) => [`S${19 + i}`, `Screenshot (${19 + i}).png`])
);

export async function ensureDirs() {
  for (const d of ['overview', 'crops', 'upscaled', 'results'])
    await fs.mkdir(path.join(WORK, d), { recursive: true });
}

/** Downscaled render for REGION LOCATION ONLY. Never read a value from these. */
export async function locator(srcPath, outName, width = 1280) {
  const out = path.join(WORK, 'overview', `LOCATOR-${outName}`);
  await sharp(srcPath).resize(width).png().toFile(out);
  return out;
}

/**
 * Native-resolution crop + integer upscale. Returns { cropPath, upPath }.
 * `box` = { left, top, width, height } in SOURCE pixel coordinates.
 * Upscale uses nearest-neighbour so no interpolated pixels are invented.
 */
export async function cropNative(srcPath, box, name, { scale = 4, invert = false, grayscale = false, threshold = null, normalize = false } = {}) {
  const cropPath = path.join(WORK, 'crops', `${name}.png`);
  const upPath = path.join(WORK, 'upscaled', `${name}@${scale}x.png`);
  await sharp(srcPath).extract(box).png().toFile(cropPath);
  let p = sharp(cropPath).resize({
    width: box.width * scale,
    height: box.height * scale,
    kernel: 'nearest',
  });
  if (grayscale) p = p.grayscale();
  if (normalize) p = p.normalise();
  if (threshold !== null) p = p.threshold(threshold);
  if (invert) p = p.negate({ alpha: false });
  await p.png().toFile(upPath);
  return { cropPath, upPath };
}

/** Raw RGBA pixel buffer for a native-resolution region. No resampling anywhere. */
export async function rawRegion(srcPath, box) {
  const { data, info } = await sharp(srcPath)
    .extract(box)
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  return { data, width: info.width, height: info.height, channels: info.channels };
}

export function px(reg, x, y) {
  const i = (y * reg.width + x) * reg.channels;
  return [reg.data[i], reg.data[i + 1], reg.data[i + 2], reg.data[i + 3]];
}

export async function writeJSON(name, obj) {
  const p = path.join(WORK, 'results', name);
  await fs.writeFile(p, JSON.stringify(obj, null, 2));
  return p;
}
