// register2-blueslab-diagnostic-establish.mjs — galadriel's INDEPENDENT blue-slab / katabasis-composition
// diagnostic for the Round-4 iter7 CAMERA-ONLY establish recompose (gandalf Round-4 brief §2 — "quantify
// the blue-slab kill, the headline"). This is the instrument gandalf's composition rule consumes.
//
// METHODOLOGY NOTE (galadriel, no-silent-transformation discipline): my FIRST signature was a pure-blue
// flat-panel mass (B-dominant-over-BOTH R and G). It produced a number that CONTRADICTED my eye (it
// reported iter7 with MORE "blue-slab" than iter6) — so I diagnosed it before reporting. Root cause:
// the iter6 slab is a DARK TEAL/CYAN tilted plane (meanRGB ~(21,64,83); B and G near-equal, only 0.37%
// bright), NOT pure-blue; and the iter7 deep recession IS pure-blue and large-area. A naive blue-pixel
// COUNT therefore goes UP, not down. The eye does NOT read "fewer blue pixels" — it reads a RELOCATION:
// the cool mass moved OUT of the focus-competing eye-level foreground and INTO a fog-veiled deep
// recession, while the foreground flipped to warm-hero-dominant. So the correct, eye-corroborating
// instrument measures THREE things, not a single blue-pixel count:
//   (A) FOREGROUND warm-vs-cool dominance — does the NEAR band read warm-hero (the fix) or cool/dark (iter6)?
//   (B) WHOLE-FRAME warm:cool ratio — did the frame flip from cool-dominant (iter6 0.83) to warm-dominant?
//   (C) COOL RELOCATION — what fraction of the cool mass now sits in the FAR/deep band (receded, fine)
//       vs the MID eye-level band (where the iter6 slab competed)?
// Plus a secondary FLAT-SLAB cardboard test (dark-flat face-on plane signature) for completeness.
//
// COOL pixel := blue is the max channel AND clearly above red (b===max & b-r>=15 & b>40) — this
//   superset captures the teal/cyan slab AND the pure-blue recession (the eye's "cool slab" family).
// WARM pixel := red/orange/gold dominant (r-b>=20 & r>=70 & r>=g*0.85) — the hero brazier/floor family.
// Bands := vertical thirds. FAR = top third (the deep recession in a look-down katabasis framing);
//   NEAR = bottom third (the foreground where a focus-competing slab does its damage).
//
// PASS on this axis (the eye's reading, quantified):
//   - NEAR foreground flips to WARM-dominant (warm:cool fore ratio rises well above iter6's ~2.75, and
//     near-warm% climbs from iter6's ~8% to a clear hero majority), AND
//   - whole-frame warm:cool flips from iter6's 0.83 (cool-dominant) to >1.0 (warm-dominant), AND
//   - the cool mass RELOCATES toward the FAR recession (FAR-cool-share rises from iter6's ~3% upward).
//
// Synty-derivative captures local-only, git-ignored — this reads them, writes only JSON.
// Deterministic: no random sampling; another galadriel-instance reproduces these exactly.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';

const FRAMES = [
  { tag: 'iter6_establish_01', file: 'descent_iter6_establish_01.png', iter: 6 },
  { tag: 'iter6_establish_02', file: 'descent_iter6_establish_02.png', iter: 6 },
  { tag: 'iter6_establish_03', file: 'descent_iter6_establish_03.png', iter: 6 },
  { tag: 'iter7_establish_01_HERO', file: 'descent_iter7_establish_01.png', iter: 7 },
  { tag: 'iter7_establish_02_ElevatedLookDown', file: 'descent_iter7_establish_02.png', iter: 7 },
  { tag: 'iter7_establish_03_GroundIntimate', file: 'descent_iter7_establish_03.png', iter: 7 },
];

function luma(r, g, b) { return 0.299 * r + 0.587 * g + 0.114 * b; }
function isCool(r, g, b) { const mx = Math.max(r, g, b); return b === mx && (b - r) >= 15 && b > 40; }
function isWarm(r, g, b) { return (r - b) >= 20 && r >= 70 && r >= g * 0.85; }

// local std of luma over a 3x3 neighborhood (for the secondary dark-flat-slab cardboard test)
function localStd(L, w, h, x, y) {
  let s = 0, ss = 0, n = 0;
  for (let dy = -1; dy <= 1; dy++) { const yy = y + dy; if (yy < 0 || yy >= h) continue;
    for (let dx = -1; dx <= 1; dx++) { const xx = x + dx; if (xx < 0 || xx >= w) continue;
      const v = L[yy * w + xx]; s += v; ss += v * v; n++; } }
  const m = s / n; return Math.sqrt(Math.max(0, ss / n - m * m));
}

async function measure(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const L = new Float32Array(w * h);
  for (let i = 0, p = 0; i < rgb.length; i += 3, p++) L[p] = luma(rgb[i], rgb[i + 1], rgb[i + 2]);

  const t1 = Math.floor(h / 3), t2 = Math.floor((2 * h) / 3);
  const bands = {
    far: { cool: 0, warm: 0, n: 0, coolSlabFlat: 0 },
    mid: { cool: 0, warm: 0, n: 0, coolSlabFlat: 0 },
    near: { cool: 0, warm: 0, n: 0, coolSlabFlat: 0 },
  };
  for (let y = 0; y < h; y++) {
    const bn = y < t1 ? 'far' : (y < t2 ? 'mid' : 'near');
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 3;
      const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
      bands[bn].n++;
      if (isCool(r, g, b)) {
        bands[bn].cool++;
        // secondary: dark-flat "cardboard" slab signature (a flat face-on cool panel)
        if (localStd(L, w, h, x, y) <= 9.0) bands[bn].coolSlabFlat++;
      }
      if (isWarm(r, g, b)) bands[bn].warm++;
    }
  }

  const totCool = bands.far.cool + bands.mid.cool + bands.near.cool;
  const totWarm = bands.far.warm + bands.mid.warm + bands.near.warm;
  const totN = w * h;
  const pct = (x, n) => +((100 * x) / n).toFixed(2);

  const nearWarmPct = pct(bands.near.warm, bands.near.n);
  const nearCoolPct = pct(bands.near.cool, bands.near.n);
  const midCoolPct = pct(bands.mid.cool, bands.mid.n);
  const farCoolPct = pct(bands.far.cool, bands.far.n);

  return {
    dims: `${w}x${h}`,
    // (A) foreground warm-vs-cool dominance
    near_warm_pct: nearWarmPct,
    near_cool_pct: nearCoolPct,
    fore_warm_cool_ratio: +(nearWarmPct / Math.max(0.1, nearCoolPct)).toFixed(2),
    // (B) whole-frame warm:cool
    frame_warm_pct: pct(totWarm, totN),
    frame_cool_pct: pct(totCool, totN),
    frame_warm_cool_ratio: +(totWarm / Math.max(1, totCool)).toFixed(2),
    // (C) cool relocation
    coolShare_FAR_pct: totCool ? +((100 * bands.far.cool) / totCool).toFixed(1) : 0,
    coolShare_MID_pct: totCool ? +((100 * bands.mid.cool) / totCool).toFixed(1) : 0,
    coolShare_NEAR_pct: totCool ? +((100 * bands.near.cool) / totCool).toFixed(1) : 0,
    band_cool_pct: { far: farCoolPct, mid: midCoolPct, near: nearCoolPct },
    // secondary: dark-flat slab mass per band (cardboard signature)
    coolSlabFlat_pct: {
      far: pct(bands.far.coolSlabFlat, bands.far.n),
      mid: pct(bands.mid.coolSlabFlat, bands.mid.n),
      near: pct(bands.near.coolSlabFlat, bands.near.n),
    },
  };
}

const out = {
  scored_at: new Date().toISOString(),
  instrument: 'register2-blueslab-diagnostic-establish.mjs (galadriel independent; eye-corroborating composition metric)',
  method: 'COOL=blue-max & b-r>=15 & b>40 (teal+blue family). WARM=r-b>=20 & r>=70 & r>=g*0.85. Bands=vertical thirds (FAR=top/deep recession, NEAR=bottom/foreground). Reports: (A) foreground warm:cool dominance, (B) whole-frame warm:cool, (C) cool relocation FAR-vs-MID, + secondary dark-flat cardboard-slab mass per band. See header for why a naive blue-pixel count is the WRONG instrument here (the iter6 slab is dark teal, not bright blue; the kill is a RELOCATION + warm-fore flip, not a blue-pixel reduction).',
  frames: [],
};

for (const f of FRAMES) {
  process.stderr.write(`blueslab ${f.tag}...\n`);
  out.frames.push({ ...f, metrics: await measure(join(DIR, f.file)) });
}

const outPath = join(process.cwd(), 'register2-blueslab-diagnostic-establish.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

console.log('=== BLUE-SLAB KILL / KATABASIS-COMPOSITION DIAGNOSTIC — iter6 -> iter7 establish (galadriel) ===');
console.log('the kill is a RELOCATION (cool foreground slab -> fog-veiled deep recession) + a warm-fore flip,');
console.log('NOT a blue-pixel reduction (the iter6 slab is dark teal; iter7 recession is pure-blue & larger).\n');

console.log('(A) FOREGROUND (NEAR band) — warm-hero established?');
let c = ['frame', 'near warm%', 'near cool%', 'fore warm:cool'];
let cw = [38, 12, 12, 16];
console.log(c.map((x, i) => x.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) { const m = f.metrics;
  console.log([f.tag, m.near_warm_pct, m.near_cool_pct, m.fore_warm_cool_ratio].map((x, i) => String(x).padEnd(cw[i])).join('')); }

console.log('\n(B) WHOLE-FRAME warm:cool — did the frame flip warm-dominant?  (iter6 ~0.83 cool-dominant -> target >1.0)');
c = ['frame', 'frame warm%', 'frame cool%', 'frame warm:cool'];
cw = [38, 12, 12, 16];
console.log(c.map((x, i) => x.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) { const m = f.metrics;
  console.log([f.tag, m.frame_warm_pct, m.frame_cool_pct, m.frame_warm_cool_ratio].map((x, i) => String(x).padEnd(cw[i])).join('')); }

console.log('\n(C) COOL RELOCATION — % of the cool mass per band (FAR=receded/fine, MID=eye-level/competed in iter6)');
c = ['frame', 'cool FAR%', 'cool MID%', 'cool NEAR%'];
cw = [38, 12, 12, 12];
console.log(c.map((x, i) => x.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) { const m = f.metrics;
  console.log([f.tag, m.coolShare_FAR_pct, m.coolShare_MID_pct, m.coolShare_NEAR_pct].map((x, i) => String(x).padEnd(cw[i])).join('')); }

console.log('\nsecondary — dark-flat "cardboard slab" mass per band (% of band; a face-on flat cool panel):');
c = ['frame', 'flat FAR%', 'flat MID%', 'flat NEAR%'];
cw = [38, 12, 12, 12];
console.log(c.map((x, i) => x.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) { const m = f.metrics;
  console.log([f.tag, m.coolSlabFlat_pct.far, m.coolSlabFlat_pct.mid, m.coolSlabFlat_pct.near].map((x, i) => String(x).padEnd(cw[i])).join('')); }

console.log(`\nwrote ${outPath}`);
