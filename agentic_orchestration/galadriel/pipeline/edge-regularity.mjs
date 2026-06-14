// edge-regularity.mjs — distinguishes voxel/blocky edge-busyness from organic-stylized detail.
//
// Insight from register-metrics.mjs run: raw HFD (edge energy) is HIGHEST for voxel imagery
// (Katana Dragon) yet voxels read LESS premium. So edge-COUNT is not the premium signal.
// This script measures EDGE-ORIENTATION REGULARITY: voxel/blocky art concentrates gradient
// energy on axis-aligned (horizontal/vertical) edges; organic-stylized + VFX-heavy art spreads
// gradient energy across all orientations. AAR (axis-aligned ratio) high => blocky/voxel.
//
// Method: Sobel gx, gy per px. For px with gradient magnitude above a threshold, bin the
// gradient orientation into axis-aligned (within ±15deg of horizontal OR vertical) vs diagonal.
// AAR = axis-aligned-strong-px / all-strong-px. Reproducible; no silent transform.

import sharp from 'sharp';
const TARGET_W = 960;
const MAG_THRESH = 40; // gradient magnitude floor to count as a "strong edge"

async function measure(path) {
  const { data: g, info } = await sharp(path).resize(TARGET_W, null, { fit: 'inside' })
    .grayscale().raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  let axisAligned = 0, diagonal = 0, strong = 0;
  let gxAbsSum = 0, gyAbsSum = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const gx = (g[i - 1 - w] + 2 * g[i - 1] + g[i - 1 + w]) - (g[i + 1 - w] + 2 * g[i + 1] + g[i + 1 + w]);
      const gy = (g[i - w - 1] + 2 * g[i - w] + g[i - w + 1]) - (g[i + w - 1] + 2 * g[i + w] + g[i + w + 1]);
      const mag = Math.hypot(gx, gy);
      if (mag < MAG_THRESH) continue;
      strong++;
      gxAbsSum += Math.abs(gx); gyAbsSum += Math.abs(gy);
      // orientation: atan2(gy,gx) in deg; gradient is perpendicular to edge, but axis-alignment
      // is symmetric so we can test the gradient direction directly.
      let ang = Math.abs(Math.atan2(gy, gx) * 180 / Math.PI); // 0..180
      if (ang > 90) ang = 180 - ang; // fold to 0..90
      // gradient near 0deg (horizontal gradient => vertical edge) OR near 90 (vertical grad => horiz edge)
      if (ang <= 15 || ang >= 75) axisAligned++; else diagonal++;
    }
  }
  const aar = strong === 0 ? 0 : axisAligned / strong;
  return {
    AAR: +aar.toFixed(3),                         // axis-aligned ratio; high => blocky/voxel
    strong_pct: +((100 * strong) / (w * h)).toFixed(2),
  };
}

const args = process.argv.slice(2);
const rows = [];
for (const a of args) {
  const eq = a.indexOf('='); const label = a.slice(0, eq); const path = a.slice(eq + 1);
  try { rows.push({ label, ...(await measure(path)) }); }
  catch (e) { rows.push({ label, error: String(e.message || e) }); }
}
const cols = ['label', 'AAR', 'strong_pct'];
const widths = cols.map(c => Math.max(c.length, ...rows.map(r => String(r[c] ?? '').length)));
console.log(cols.map((c, i) => c.padEnd(widths[i])).join('  '));
console.log(widths.map(w => '-'.repeat(w)).join('  '));
for (const r of rows) console.log(cols.map((c, i) => String(r[c] ?? '').padEnd(widths[i])).join('  '));
