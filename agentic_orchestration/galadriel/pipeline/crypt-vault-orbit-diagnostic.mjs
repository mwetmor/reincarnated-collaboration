// crypt-vault-orbit-diagnostic.mjs — galadriel Gate-2 SANITY layer for the crypt-vault orbit.
// Three honesty checks the headline numbers need before the verdict stands:
//   (1) AM I MEASURING THE RIGHT PIXELS? — top-1% bright centroid + mean luma (are the eye-magnets the
//       braziers, i.e. a real lit hot core, or a UI/artifact?), and is warm-dominance a REAL warm key or
//       a flat red tint? Report per-frame warm% / cool% by pixel-classification (same family as the
//       descent blue-slab diagnostic) so warmCool is corroborated by an independent path.
//   (2) WHY IS SHF HIGHER THAN CATHEDRAL? — band-split SHF (top third / mid / bottom third). A dressed
//       crypt with a deep pit + void surround legitimately reads more dark than a furnished cathedral; the
//       descent oubliette PASSED at SHF 61.67. The question is whether the dark is STRUCTURED (lit props
//       punching out of a deep bed = premium-lit-in-dark) or a flat underexposed black (a register break).
//       poolBedGap already answers this numerically; here I localize WHERE the dark sits.
//   (3) drax's 3 EYES-ON FLAGS — confirm/deny against metrics, and separate any SPATIAL observation out:
//       (a) sarcophagi read as generic light boxes at distance; (b) cold-rim blue on shadowed walls;
//       (c) mezzanine deck reads large/bright.
//
// Instrument math is the SAME family (960w inside-fit, luma, raw RGB). warm/cool pixel signatures are the
// descent diagnostic's (WARM r-b>=20 & r>=70 & r>=g*0.85 ; COOL b==max & b-r>=15 & b>40). Deterministic.
// Synty-derivative captures git-ignored — reads only, writes JSON + a few /tmp eye crops (NEVER committed).

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/crypt_vault_orbit_2026-06-19';
const TMP = '/tmp/galadriel_crypt_crops';

const FRAMES = [
  { file: 'crypt_vault_orbit_01_orbit_az000.png', tag: 'orbit_az000', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_00_orbit_az045.png', tag: 'orbit_az045', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_07_orbit_az090.png', tag: 'orbit_az090', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_06_orbit_az135.png', tag: 'orbit_az135', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_05_orbit_az180.png', tag: 'orbit_az180', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_04_orbit_az225.png', tag: 'orbit_az225', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_03_orbit_az270.png', tag: 'orbit_az270', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_02_orbit_az315.png', tag: 'orbit_az315', cls: 'ORBIT' },
  { file: 'crypt_vault_orbit_08_oblique_az030.png', tag: 'oblique_az030', cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_11_oblique_az150.png', tag: 'oblique_az150', cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_10_oblique_az240.png', tag: 'oblique_az240', cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_09_oblique_az300.png', tag: 'oblique_az300', cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_12_through_entrance.png', tag: 'through_entrance', cls: 'THROUGH' },
  { file: 'crypt_vault_orbit_13_through_pit_to_mezzanine.png', tag: 'through_pit_to_mezzanine', cls: 'THROUGH' },
  { file: 'crypt_vault_orbit_14_plan_footprint.png', tag: 'plan_footprint', cls: 'PLAN' },
];

function percentile(sorted, p) {
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.floor(p * sorted.length)));
  return sorted[idx];
}

async function diagnose(path) {
  // grayscale for luma centroids + band-split SHF
  const g = sharp(path).resize(TARGET_W, null, { fit: 'inside' }).grayscale();
  const { data: gray, info } = await g.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const sorted = Float64Array.from(gray).slice().sort();
  const p99 = percentile(sorted, 0.99);

  // top-1% bright centroid + mean luma (the eye-magnet read)
  let bx = 0, by = 0, bn = 0, bsum = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const v = gray[y * w + x];
    if (v >= p99) { bx += x; by += y; bn++; bsum += v; }
  }
  const brightCentroid = bn ? { x_pct: +(100 * bx / bn / w).toFixed(1), y_pct: +(100 * by / bn / h).toFixed(1), mean_luma: +(bsum / bn).toFixed(0), n: bn } : null;

  // band-split SHF (shadow<31) by vertical thirds: TOP / MID / BOTTOM (where does the dark sit?)
  const third = Math.floor(h / 3);
  const bandDark = [0, 0, 0], bandN = [third * w, third * w, (h - 2 * third) * w];
  for (let y = 0; y < h; y++) {
    const band = y < third ? 0 : (y < 2 * third ? 1 : 2);
    for (let x = 0; x < w; x++) if (gray[y * w + x] < 31) bandDark[band]++;
  }
  const shfBand = bandDark.map((d, i) => +(100 * d / bandN[i]).toFixed(1)); // [top, mid, bottom]

  // warm/cool pixel classification (independent corroboration of warmCool) + per-band warm/cool
  const { data: rgb } = await sharp(path).resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  let warm = 0, cool = 0;
  const bandWarm = [0, 0, 0], bandCool = [0, 0, 0];
  // hot-warm cluster centroid (the brazier hot core in COLOR, not just luma)
  let wx = 0, wy = 0, wn = 0;
  for (let y = 0; y < h; y++) {
    const band = y < third ? 0 : (y < 2 * third ? 1 : 2);
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 3;
      const r = rgb[i], gg = rgb[i + 1], b = rgb[i + 2];
      const isWarm = (r - b >= 20) && (r >= 70) && (r >= gg * 0.85);
      const isCool = (b >= r) && (b >= gg) && (b - r >= 15) && (b > 40);
      if (isWarm) { warm++; bandWarm[band]++; wx += x; wy += y; wn++; }
      if (isCool) { cool++; bandCool[band]++; }
    }
  }
  const np = w * h;
  const warmCentroid = wn ? { x_pct: +(100 * wx / wn / w).toFixed(1), y_pct: +(100 * wy / wn / h).toFixed(1) } : null;

  return {
    dims: `${w}x${h}`,
    brightCentroid,
    shf_band_top_mid_bottom: shfBand,
    warm_pct: +(100 * warm / np).toFixed(2),
    cool_pct: +(100 * cool / np).toFixed(2),
    warm_cool_ratio: cool ? +(warm / cool).toFixed(2) : null,
    warmCentroid,
    warm_by_band_pct: bandWarm.map((v, i) => +(100 * v / bandN[i]).toFixed(1)),
    cool_by_band_pct: bandCool.map((v, i) => +(100 * v / bandN[i]).toFixed(1)),
  };
}

const out = { scored_at: new Date().toISOString(), note: 'Gate-2 sanity layer: right-pixels check (bright/warm centroids), SHF band-split (where the dark sits), warm/cool pixel-class corroboration, + drax 3-flag evidence.', frames: [] };
for (const f of FRAMES) {
  process.stderr.write(`diagnosing ${f.tag}...\n`);
  out.frames.push({ ...f, diag: await diagnose(join(DIR, f.file)) });
}

writeFileSync(join(process.cwd(), 'crypt-vault-orbit-diagnostic.json'), JSON.stringify(out, null, 2));

// ---- eye crops: 3 representative frames at native, + the SHF-outlier through_entrance, to /tmp ----
import { mkdirSync } from 'fs';
mkdirSync(TMP, { recursive: true });
const cropList = [
  ['crypt_vault_orbit_01_orbit_az000.png', 'orbit_az000_hero'],
  ['crypt_vault_orbit_04_orbit_az225.png', 'orbit_az225_dimmest'],
  ['crypt_vault_orbit_12_through_entrance.png', 'through_entrance_OUTLIER'],
  ['crypt_vault_orbit_14_plan_footprint.png', 'plan_footprint'],
];
for (const [file, name] of cropList) {
  await sharp(join(DIR, file)).resize(1100, null, { fit: 'inside' }).toFile(join(TMP, `${name}.png`));
}
console.log('=== CRYPT-VAULT ORBIT DIAGNOSTIC ===\n');
const cols = ['frame', 'cls', 'bright x%/y%/luma', 'SHF top/mid/bot', 'warm%', 'cool%', 'w:c', 'warm x%/y%'];
const cw = [26, 9, 20, 20, 8, 8, 7, 14];
console.log(cols.map((c, i) => c.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const d = f.diag;
  const bc = d.brightCentroid ? `${d.brightCentroid.x_pct}/${d.brightCentroid.y_pct}/${d.brightCentroid.mean_luma}` : '-';
  const wc = d.warmCentroid ? `${d.warmCentroid.x_pct}/${d.warmCentroid.y_pct}` : '-';
  console.log([
    f.tag, f.cls, bc, d.shf_band_top_mid_bottom.join('/'),
    d.warm_pct, d.cool_pct, d.warm_cool_ratio, wc,
  ].map((c, i) => String(c).padEnd(cw[i])).join(''));
}
console.log(`\nwrote crypt-vault-orbit-diagnostic.json + eye crops to ${TMP}/`);
