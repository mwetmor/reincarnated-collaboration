// register2-score-crypt-vault-orbit.mjs — galadriel GATE 2 (register CV) for the crypt-vault clear-room
// node PoC. drax authored the FIRST composable ARPG map "node" (a crypt-vault clear-room) and it PASSED
// Gate 1 (structural, engine-truth, camera-independent). This is Gate 2: does the REGISTER (held CONSTANT
// at the proven cathedral_lift / register-2 recipe — the same one the descent run-to-green closed on) HOLD
// across SEVERAL framings, or does it BREAK? The recipe is LOCKED; the only variable under test in this
// PoC is SPATIAL COHERENCE (Matt's Gate 3). So this gate is NARROW: confirm the register didn't BREAK
// across the orbit — NOT "is the recipe right" (it is) and NOT "is the room laid out well" (Matt's gate).
//
// PROVENANCE — instrument math is BYTE-IDENTICAL to the committed register2-score-descent-iter7.mjs /
// -iter6.mjs / lifecycle-score-cathedral.mjs / register-metrics.mjs:
//   TARGET_W=960 inside-fit; gray luma for LDR/SHF/HLF/HFD/LMV; raw RGB for SAT + warmCool;
//   cut-points HLF>204 (>0.80*255), SHF<31 (<0.12*255), bright>180; LDR=p95-p05; poolBedGap=p98-p50;
//   warmCool=(R+0.5G)/(B+0.5G); laplacianEnergy + localMaterialVariance(8x8) unchanged.
// I changed NOTHING in the substrate math. The ONLY additions are (1) the frame list + framing-class
// tags (ORBIT / OBLIQUE / THROUGH / PLAN), and (2) the band application, scored PER-FRAME across all 15.
//
// THE BAND (what "holds" means here) — the cathedral register-2 band + the descent DRESSED-kind SHF gate:
//   LIGHTING (cathedral, MANDATORY): LDR >= 115 AND SHF >= the kind-appropriate floor.
//     The crypt content is DRESSED (Gate-1 collected sarcophagi/piers/deck/stairs + braziers/clutter/
//     statues — a furnished room, NOT a bare void). Per the descent kind-aware gate, dressed content fills
//     frame-area an empty arena leaves black, so it legitimately reads premium-lit-in-dark at a LOWER SHF.
//     DRESSED SHF floor = 17.5 (the descent-codified dressed floor). STARK floor 30 is the WRONG bar for a
//     furnished room and would mis-fail dressing as "not dark enough" — a known calibration trap.
//   REGISTER DIRECTION (descent): warmCool >= 1.0 (warm-dominant) is the descent establish bar. Reported
//     per-frame; flagged where a framing trades toward cool (the descent proved elevating/broadside framings
//     trade cool by frame-area — a FRAMING effect, not a register break).
//   VFX (cathedral, MANDATORY in the recipe): INHERITED-PASS, NOT re-scored here. This orbit harness stages
//     NO hero VFX event (it is a pure spatial/architectural orbit of a STATIC scene; braziers are always-on
//     atmosphere only). The recipe's VFX is proven (cathedral HLF peak 9.354%, descent erupt 2x). Failing
//     this node for lacking a bloom it was never asked to stage would be a category error. HLF is reported
//     as always-on brazier-glow atmosphere, NOT graded against the 1.5% hero-bloom bar.
//   MATERIAL (cathedral): LMV reported (light-responsive surface, not flat per-face). Secondary; the recipe
//     scored material 5/5 on real Synty content — carried, spot-confirmed, not the gate.
//
// WHY PER-FRAME-ACROSS-FRAMINGS, not lifecycle: the cathedral/descent scores were LIFECYCLE captures (one
// camera, many time-steps, a hero VFX event windowed across them). This is 15 DIFFERENT CAMERAS of ONE
// static scene. So the right read is the register-HOLD across framings: does each frame sit in-band, and do
// the framings CLUSTER (a held register) or SCATTER for a register reason (a break)? Drift that tracks the
// KNOWN framing axes (through-room = less architecture in frame; plan = top-down floor-dominated; oblique =
// steeper) is FRAMING-DEPENDENT and EXPECTED — I separate it from a register break, and I separate any
// SPATIAL-COHERENCE observation out to Matt's Gate 3 (it is not mine to rule).
//
// Synty-derivative captures are git-ignored IP — this reads them, writes only JSON. Deterministic: another
// galadriel-instance reproduces every value exactly (no random sampling).

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/crypt_vault_orbit_2026-06-19';

// --- band constants (cathedral lighting + descent DRESSED-kind SHF + descent warmCool direction) ---
const LDR_MIN = 115;                 // cathedral lighting-drama floor (every cathedral frame cleared it)
const DRESSED_SHF_MIN = 17.5;        // descent-codified DRESSED floor (furnished room reads premium-lit-in-dark lower)
const STARK_SHF_MIN = 30;            // reported for reference only — NOT the bar for dressed content
const WARMCOOL_MIN = 1.0;            // descent establish register-direction bar (warm-dominant)
const HLF_BLOOM_BAR = 1.5;           // the HERO-BLOOM bar — NOT applied here (no hero event staged); shown for context only

// reference band values for at-a-glance comparison (from the committed scorecards)
const CATHEDRAL = { LDR_whole: 231.9, SHF_whole: 41.8, HLF_peak: 9.354, LMV_whole: 36.4 };
const DESCENT_ESTABLISH = { LDR: '124/119/127', warmCool: '1.026/1.018/1.015', note: 'low warm katabasis beats' };
const BOSS_NORTHSTAR = { LDR: 175.97, SHF: 42.74, HLF_peak: 4.013 };

// --- the 15 frames + framing-class tags (from shoot_crypt_vault_orbit.gd _build_shot_list) ---
// ORBIT  = 8 azimuths at pitch 42 (the genre 2.5D ARPG framing — whole room, full compass): the PRIMARY
//          register-hold set. These are the frames that MUST hold; they are the recipe's home framing.
// OBLIQUE= 4 azimuths at pitch 26 (architecture-audit angle; de-foreshortens verticality): secondary;
//          steeper-into-the-walls, expected slightly different fill.
// THROUGH= 2 through-room (entrance->exit at pitch 14; pit->mezzanine at pitch 18): EXPECTED to skew —
//          camera pulled low/far, LESS architecture in frame, more void/doorway. Brief flags this.
// PLAN   = 1 top-down-ish (pitch 68, fight-footprint read): EXPECTED to skew HARD — top-down floor-
//          dominated, the rake-lit walls largely out of frame. Brief flags this. NOT a register-break input.
const FRAMES = [
  { file: 'crypt_vault_orbit_01_orbit_az000.png',            tag: 'orbit_az000',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_00_orbit_az045.png',            tag: 'orbit_az045',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_07_orbit_az090.png',            tag: 'orbit_az090',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_06_orbit_az135.png',            tag: 'orbit_az135',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_05_orbit_az180.png',            tag: 'orbit_az180',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_04_orbit_az225.png',            tag: 'orbit_az225',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_03_orbit_az270.png',            tag: 'orbit_az270',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_02_orbit_az315.png',            tag: 'orbit_az315',            cls: 'ORBIT'   },
  { file: 'crypt_vault_orbit_08_oblique_az030.png',          tag: 'oblique_az030',          cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_11_oblique_az150.png',          tag: 'oblique_az150',          cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_10_oblique_az240.png',          tag: 'oblique_az240',          cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_09_oblique_az300.png',          tag: 'oblique_az300',          cls: 'OBLIQUE' },
  { file: 'crypt_vault_orbit_12_through_entrance.png',       tag: 'through_entrance',        cls: 'THROUGH' },
  { file: 'crypt_vault_orbit_13_through_pit_to_mezzanine.png', tag: 'through_pit_to_mezzanine', cls: 'THROUGH' },
  { file: 'crypt_vault_orbit_14_plan_footprint.png',         tag: 'plan_footprint',          cls: 'PLAN'    },
];

// ---- instruments (BYTE-IDENTICAL to register2-score-descent-iter7.mjs / register-metrics.mjs) ----
function laplacianEnergy(gray, w, h) {
  let sum = 0, n = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const lap = -4 * gray[i] + gray[i - 1] + gray[i + 1] + gray[i - w] + gray[i + w];
      sum += Math.abs(lap); n++;
    }
  }
  return sum / n;
}
function localMaterialVariance(gray, w, h, gx = 8, gy = 8) {
  const tw = Math.floor(w / gx), th = Math.floor(h / gy);
  const tileStds = [];
  for (let ty = 0; ty < gy; ty++) {
    for (let tx = 0; tx < gx; tx++) {
      let s = 0, ss = 0, cnt = 0;
      for (let y = ty * th; y < (ty + 1) * th; y++) {
        for (let x = tx * tw; x < (tx + 1) * tw; x++) {
          const v = gray[y * w + x]; s += v; ss += v * v; cnt++;
        }
      }
      const mean = s / cnt;
      tileStds.push(Math.sqrt(Math.max(0, ss / cnt - mean * mean)));
    }
  }
  return tileStds.reduce((a, b) => a + b, 0) / tileStds.length;
}
function percentile(sorted, p) {
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.floor(p * sorted.length)));
  return sorted[idx];
}

async function measure(path) {
  const g = sharp(path).resize(TARGET_W, null, { fit: 'inside' }).grayscale();
  const { data: gray, info } = await g.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const hfd = laplacianEnergy(gray, w, h);
  const lmv = localMaterialVariance(gray, w, h);
  const lumaSorted = Float64Array.from(gray).slice().sort();
  const p05 = percentile(lumaSorted, 0.05), p50 = percentile(lumaSorted, 0.50);
  const p95 = percentile(lumaSorted, 0.95), p98 = percentile(lumaSorted, 0.98);
  const ldr = p95 - p05;
  const poolBedGap = p98 - p50;
  let hi = 0, lo = 0, brt = 0;
  for (let i = 0; i < gray.length; i++) {
    const v = gray[i];
    if (v > 204) hi++;
    if (v < 31) lo++;
    if (v > 180) brt++;
  }
  const hlf = (100 * hi) / gray.length;
  const shf = (100 * lo) / gray.length;
  const { data: rgb, info: ri } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  let satSum = 0, satSS = 0, np = ri.width * ri.height;
  let rSum = 0, gSum = 0, bSum = 0;
  for (let i = 0; i < rgb.length; i += 3) {
    const r = rgb[i] / 255, gg = rgb[i + 1] / 255, b = rgb[i + 2] / 255;
    const max = Math.max(r, gg, b), min = Math.min(r, gg, b);
    const s = max === 0 ? 0 : (max - min) / max;
    satSum += s; satSS += s * s;
    rSum += rgb[i]; gSum += rgb[i + 1]; bSum += rgb[i + 2];
  }
  const satMean = satSum / np;
  const satStd = Math.sqrt(Math.max(0, satSS / np - satMean * satMean));
  const warmCool = +((rSum + gSum * 0.5) / (bSum + gSum * 0.5)).toFixed(3);
  return {
    HFD: +hfd.toFixed(2), LMV: +lmv.toFixed(2), LDR: +ldr.toFixed(1),
    SAT_mean: +satMean.toFixed(3), SAT_std: +satStd.toFixed(3),
    HLF_pct: +hlf.toFixed(3), SHF_pct: +shf.toFixed(2),
    warmCool, p05, p50, p95, p98, poolBedGap, bright_pct: +((100 * brt) / gray.length).toFixed(2),
    dims: `${w}x${h}`,
  };
}

// ---- per-frame band application (LIGHTING mandatory; warmCool direction; HLF/LMV reported) ----
// Lighting holds iff LDR>=115 AND SHF>=DRESSED floor (the content is dressed). I flag PLAN/THROUGH framing
// effects separately so a top-down or void-heavy framing's skew is not mistaken for a register break.
function applyBand(m, cls) {
  const ldrHold = m.LDR >= LDR_MIN;
  const shfHoldDressed = m.SHF_pct >= DRESSED_SHF_MIN;
  const lightingHold = ldrHold && shfHoldDressed;
  const warmDominant = m.warmCool >= WARMCOOL_MIN;
  const fails = [];
  if (!ldrHold) fails.push(`LDR ${m.LDR} < ${LDR_MIN}`);
  if (!shfHoldDressed) fails.push(`SHF ${m.SHF_pct} < ${DRESSED_SHF_MIN} (dressed floor)`);
  return {
    cls,
    ldrHold, shfHoldDressed, lightingHold, warmDominant,
    // framing-effect annotations (NOT pass/fail inputs — context so drift is read honestly)
    framing_skew_expected: (cls === 'PLAN' || cls === 'THROUGH'),
    lighting_basis: lightingHold
      ? `LIGHTING HOLD: LDR ${m.LDR} >= ${LDR_MIN} AND SHF ${m.SHF_pct} >= ${DRESSED_SHF_MIN} (dressed)`
      : `LIGHTING REVIEW: ${fails.join('; ')}`,
    warmcool_basis: warmDominant
      ? `warm-dominant (warmCool ${m.warmCool} >= ${WARMCOOL_MIN})`
      : `cool-leaning (warmCool ${m.warmCool} < ${WARMCOOL_MIN}) — check framing class`,
  };
}

function agg(rows, keys) {
  const out = {};
  for (const k of keys) {
    const vals = rows.map(r => r.metrics[k]);
    const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
    out[k] = {
      mean: +mean.toFixed(3),
      min: +Math.min(...vals).toFixed(3),
      max: +Math.max(...vals).toFixed(3),
      // coefficient of variation: the tightness-of-cluster read (low CV across framings = held register)
      cv: +(Math.sqrt(vals.reduce((a, b) => a + (b - mean) ** 2, 0) / vals.length) / (mean || 1)).toFixed(3),
    };
  }
  return out;
}

const out = {
  scored_at: new Date().toISOString(),
  gate: 'GATE 2 (register CV) — crypt-vault clear-room node PoC',
  question: 'Does the LOCKED cathedral_lift/register-2 recipe HOLD across SEVERAL framings of the node? (NARROW: not "is the recipe right" — it is; not spatial coherence — Matt Gate 3.)',
  build: 'drax crypt-vault clear-room node (reincarnated-godot scenes/crypt_vault_node_baked.tscn); register held CONSTANT at the proven cathedral_lift recipe; Gate 1 (structural) PASSED.',
  capture_set: 'crypt_vault_orbit_2026-06-19 — 15 framings, 2560x1440, Godot SubViewport (8 orbit pitch42 / 4 oblique pitch26 / 2 through-room / 1 plan pitch68).',
  instrument_provenance: 'BYTE-IDENTICAL substrate math to register2-score-descent-iter7.mjs / lifecycle-score-cathedral.mjs / register-metrics.mjs (960w inside-fit, gray luma, raw RGB sat+warmCool; HLF>204, SHF<31, LDR=p95-p05, poolBedGap=p98-p50, warmCool=(R+0.5G)/(B+0.5G)).',
  band: {
    LIGHTING_mandatory: `LDR >= ${LDR_MIN} (cathedral) AND SHF >= ${DRESSED_SHF_MIN} (descent DRESSED floor — content is furnished, NOT a bare void; STARK ${STARK_SHF_MIN} is the wrong bar)`,
    REGISTER_DIRECTION: `warmCool >= ${WARMCOOL_MIN} (descent establish bar; framing-class-aware — broadside/steep framings trade cool by frame-area)`,
    VFX: `INHERITED-PASS, NOT re-scored — this orbit stages NO hero VFX event (static-scene architectural orbit; braziers always-on atmosphere only). HLF reported as atmosphere, NOT graded against the ${HLF_BLOOM_BAR}% hero-bloom bar.`,
    MATERIAL: 'LMV reported (light-responsive surface); secondary, recipe scored material 5/5 on real Synty content.',
  },
  reference_bands: { CATHEDRAL, DESCENT_ESTABLISH, BOSS_NORTHSTAR },
  frames: [],
};

for (const f of FRAMES) {
  process.stderr.write(`scoring ${f.tag} (${f.cls})...\n`);
  const m = await measure(join(DIR, f.file));
  out.frames.push({ ...f, metrics: m, band: applyBand(m, f.cls) });
}

// ---- aggregates: overall + per-framing-class (the cluster-tightness read) ----
const NUM = ['LDR', 'SHF_pct', 'HLF_pct', 'warmCool', 'LMV', 'HFD', 'SAT_mean', 'poolBedGap', 'bright_pct'];
out.aggregate_all = agg(out.frames, NUM);
out.aggregate_by_class = {};
for (const cls of ['ORBIT', 'OBLIQUE', 'THROUGH', 'PLAN']) {
  const sub = out.frames.filter(f => f.cls === cls);
  if (sub.length) out.aggregate_by_class[cls] = { n: sub.length, ...agg(sub, NUM) };
}

// ---- roll-up: lighting-hold counts overall + per class (the gate's core read) ----
const lightingHoldAll = out.frames.filter(f => f.band.lightingHold).length;
const orbitFrames = out.frames.filter(f => f.cls === 'ORBIT');
const lightingHoldOrbit = orbitFrames.filter(f => f.band.lightingHold).length;
const warmAll = out.frames.filter(f => f.band.warmDominant).length;
out.rollup = {
  lighting_hold_all: `${lightingHoldAll}/${out.frames.length}`,
  lighting_hold_orbit_PRIMARY: `${lightingHoldOrbit}/${orbitFrames.length}`,
  warm_dominant_all: `${warmAll}/${out.frames.length}`,
  ldr_all_clear_115: out.frames.every(f => f.band.ldrHold),
  shf_all_clear_dressed_floor: out.frames.every(f => f.band.shfHoldDressed),
};

const outPath = join(process.cwd(), 'register2-scores-crypt-vault-orbit.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ---- console report ----
console.log('=== GATE 2 (register CV) — CRYPT-VAULT ORBIT (15 framings) ===\n');
console.log(`BAND: LIGHTING mandatory = LDR>=${LDR_MIN} AND SHF>=${DRESSED_SHF_MIN} (DRESSED floor). warmCool>=${WARMCOOL_MIN} direction. VFX inherited-PASS (no hero event staged).`);
console.log(`cathedral ref: LDR ${CATHEDRAL.LDR_whole} / SHF ${CATHEDRAL.SHF_whole}% / LMV ${CATHEDRAL.LMV_whole}  |  boss north-star: LDR ${BOSS_NORTHSTAR.LDR} / SHF ${BOSS_NORTHSTAR.SHF}%\n`);
const cols = ['frame', 'cls', 'LDR', 'SHF%', 'warmCool', 'HLF%', 'LMV', 'gap', 'LIGHT', 'WARM'];
const cw = [26, 9, 7, 8, 10, 8, 7, 6, 7, 6];
console.log(cols.map((c, i) => c.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const m = f.metrics, b = f.band;
  console.log([
    f.tag, f.cls, m.LDR, m.SHF_pct, m.warmCool, m.HLF_pct, m.LMV, m.poolBedGap,
    b.lightingHold ? 'HOLD' : 'REVIEW', b.warmDominant ? 'warm' : 'cool',
  ].map((c, i) => String(c).padEnd(cw[i])).join(''));
}
console.log('\n--- per framing-class aggregate (mean [min..max], cv=cluster-tightness) ---');
for (const cls of ['ORBIT', 'OBLIQUE', 'THROUGH', 'PLAN']) {
  const a = out.aggregate_by_class[cls]; if (!a) continue;
  console.log(`${cls} (n=${a.n}):  LDR ${a.LDR.mean} [${a.LDR.min}..${a.LDR.max}] cv${a.LDR.cv}   SHF ${a.SHF_pct.mean} [${a.SHF_pct.min}..${a.SHF_pct.max}] cv${a.SHF_pct.cv}   warmCool ${a.warmCool.mean} [${a.warmCool.min}..${a.warmCool.max}] cv${a.warmCool.cv}   HLF ${a.HLF_pct.mean}   LMV ${a.LMV.mean}`);
}
console.log('\n--- ROLL-UP ---');
console.log(JSON.stringify(out.rollup, null, 2));
console.log(`\nwrote ${outPath}`);
