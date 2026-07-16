// atlas-refit-candidate-1-composite.mjs — build the side-by-side comparison composites + crop receipts
// for the Refit-Candidate-1 comparison package (gandalf brief 2026-07-16-galadriel-a-render-refit-
// candidate-plates-brief.md). Edition III (final r8 plates) LEFT, Refit Candidate 1 RIGHT, SAME PIXEL
// SCALE (both 3200×2400), one labeled composite PNG per skin — the first thing Matt sees. Plus crop
// receipts: title band (candidate identity legible), the BUILD FAMILIES key, one dense-region crop per
// plate for point-texture comparison. READ-ONLY on the Edition-III captures (composite reads, never writes).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const E3_DIR = resolve(__dirname, '../captures/2026-07-16-atlas-edition3-r8-furniture');       // READ-ONLY
const RC_DIR = resolve(__dirname, '../captures/2026-07-16-atlas-refit-candidate-1');
const CROP_DIR = join(RC_DIR, 'crops');
mkdirSync(CROP_DIR, { recursive: true });

const SKINS = ['instrument', 'archive'];
// per-skin composite chrome (label band): light plate → dark ink; dark plate → light ink.
const CHROME = {
  instrument: { bg: '#ffffff', ink: '#111418', sub: '#555b66', divider: '#c8ccd2' },
  archive: { bg: '#0e1016', ink: '#e8eaf0', sub: '#9aa0ad', divider: '#2a2e38' },
};

const BAND_H = 120;          // header label band above each plate pair
const GAP = 40;              // gap between the two plates
const PAD = 36;              // outer pad

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// SVG text label band (a header strip that names LEFT=Edition III, RIGHT=Refit Candidate 1).
function labelBandSvg(totalW, plateW, c) {
  const leftCx = PAD + plateW / 2;
  const rightCx = PAD + plateW + GAP + plateW / 2;
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${totalW}" height="${BAND_H}">
  <rect width="${totalW}" height="${BAND_H}" fill="${c.bg}"/>
  <text x="${leftCx}" y="52" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="40" font-weight="700" fill="${c.ink}">Edition III  ·  SERVED TRUTH</text>
  <text x="${leftCx}" y="92" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="26" fill="${c.sub}">atlas-edition3.json  ·  469 active  ·  ratified, byte-untouched</text>
  <text x="${rightCx}" y="52" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="40" font-weight="700" fill="${c.ink}">Refit Candidate 1  ·  UNRATIFIED</text>
  <text x="${rightCx}" y="92" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="26" fill="${c.sub}">full re-derivation  ·  628 active  ·  plane Q-aligned to Edition-I orientation (rot -117.3477 deg)</text>
  <line x1="${PAD + plateW + GAP / 2}" y1="16" x2="${PAD + plateW + GAP / 2}" y2="${BAND_H - 12}" stroke="${c.divider}" stroke-width="2"/>
</svg>`);
}

async function buildComposite(skin) {
  const c = CHROME[skin];
  const e3Path = join(E3_DIR, `atlas-edition3-${skin}.png`);
  const rcPath = join(RC_DIR, `atlas-refit-candidate-1-${skin}.png`);
  const e3 = sharp(e3Path), rc = sharp(rcPath);
  const [e3m, rcm] = [await e3.metadata(), await rc.metadata()];
  // both plates are the same pixel scale (asserted); use a shared plate box = max of the two.
  const plateW = Math.max(e3m.width, rcm.width);
  const plateH = Math.max(e3m.height, rcm.height);
  const totalW = PAD * 2 + plateW * 2 + GAP;
  const totalH = PAD + BAND_H + plateH + PAD;

  const band = labelBandSvg(totalW, plateW, c);
  const e3Buf = await sharp(e3Path).toBuffer();
  const rcBuf = await sharp(rcPath).toBuffer();
  // vertical divider between the two plates (full plate height).
  const dividerSvg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="4" height="${plateH}"><rect width="4" height="${plateH}" fill="${c.divider}"/></svg>`);

  const out = join(RC_DIR, `composite-edition3-vs-refit-candidate-1-${skin}.png`);
  await sharp({ create: { width: totalW, height: totalH, channels: 4, background: c.bg } })
    .composite([
      { input: band, top: PAD - 12, left: 0 },
      { input: e3Buf, top: PAD + BAND_H, left: PAD },
      { input: dividerSvg, top: PAD + BAND_H, left: PAD + plateW + GAP / 2 - 2 },
      { input: rcBuf, top: PAD + BAND_H, left: PAD + plateW + GAP },
    ])
    .png()
    .toFile(out);
  console.log(`[composite] ${out} (${totalW}x${totalH})`);
  return { out, plateW, plateH };
}

// Crop receipts. Plate is 3200×2400 (2× the 1600×1200 SVG viewBox → scale factor 2.0 for coords).
const S = 2.0; // px per SVG unit
// title band: SVG y[0,110] x[0,~900] → the identity + banner + deriv gloss.
const TITLE = { left: 0, top: 0, width: Math.round(920 * S), height: Math.round(112 * S) };
// BUILD FAMILIES key: top-right, SVG x[~1300,1504] y[~58,270].
const KEY = { left: Math.round(1290 * S), top: Math.round(52 * S), width: Math.round(220 * S), height: Math.round(230 * S) };
// dense region: the settled archipelago core, SVG x[560,1040] y[560,1000] (the WHIRLWIND/beam cluster).
const DENSE = { left: Math.round(560 * S), top: Math.round(560 * S), width: Math.round(480 * S), height: Math.round(440 * S) };

async function crops(skin) {
  const rcPath = join(RC_DIR, `atlas-refit-candidate-1-${skin}.png`);
  const e3Path = join(E3_DIR, `atlas-edition3-${skin}.png`);
  const jobs = [
    // candidate title band — identity legible receipt
    { src: rcPath, region: TITLE, name: `crop-title-refit-candidate-1-${skin}.png` },
    // candidate key
    { src: rcPath, region: KEY, name: `crop-key-refit-candidate-1-${skin}.png` },
    // dense-region per plate (both) for point-texture comparison
    { src: rcPath, region: DENSE, name: `crop-dense-refit-candidate-1-${skin}.png` },
    { src: e3Path, region: DENSE, name: `crop-dense-edition3-${skin}.png` },
  ];
  for (const j of jobs) {
    const out = join(CROP_DIR, j.name);
    await sharp(j.src).extract(j.region).toFile(out);
    console.log(`[crop] ${out} (${j.region.width}x${j.region.height})`);
  }
}

function writeManifest() {
  const md = `# Refit-Candidate-1 comparison package — deliverable manifest

**UNRATIFIED COMPARISON ARTIFACT.** Static plates for Matt's Tier-3 atlas refit adoption decision
(Refit Candidate 1 — full re-derivation of the FIT on the 628-active corpus — vs the served Edition III).
Edition III is byte-untouched and READ-ONLY. Nothing here is served; the candidate reaches Matt as these
plates (interactivity follows adoption, not precedes it). Authority: Matt 2026-07-16 "I want to see both
versions so we cna make a decision." · gandalf brief 2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md.

## Side-by-side composites (the first thing Matt sees — Edition III LEFT, candidate RIGHT, same pixel scale)
- \`composite-edition3-vs-refit-candidate-1-instrument.png\` (LIGHT skin)
- \`composite-edition3-vs-refit-candidate-1-archive.png\` (DARK skin)

## Candidate plates (both skins, SVG + PNG)
- \`atlas-refit-candidate-1-instrument.svg\` + \`.png\` (LIGHT)
- \`atlas-refit-candidate-1-archive.svg\` + \`.png\` (DARK)

## Receipts + provenance
- \`verification-note.md\` — framed as an unratified comparison artifact; acceptance tally (re-pointed), cross-check verdict, demoted-observations table.
- \`render-provenance.json\` — machine-readable render metadata + plane_alignment stamp + render-vs-emission cross-check.

## Crop receipts (crops/)
- \`crop-title-refit-candidate-1-{instrument,archive}.png\` — candidate identity band legible (title + UNRATIFIED banner + derivation gloss).
- \`crop-key-refit-candidate-1-{instrument,archive}.png\` — BUILD FAMILIES key.
- \`crop-dense-refit-candidate-1-{instrument,archive}.png\` + \`crop-dense-edition3-{instrument,archive}.png\` — one dense-region crop per plate (same viewport) for point-texture comparison.
- \`crop-dense-COMPARE-{instrument,archive}.png\` — Edition III vs candidate dense core, side-by-side (the point-texture receipt).

## Read this alongside
- The composite is the entry point. The verification-note carries the acceptance tally + the CHANGED observations (mcd- on-plane-vs-ledger tension; density 3.1 vs 2.3; meso-beyond group profile; 1 lit cell just outside the candidate's own frame). gandalf's interpretation section (comparison report) closes the package.
`;
  const out = join(RC_DIR, 'comparison-package-manifest.md');
  writeFileSync(out, md, 'utf8');
  console.log(`[manifest] ${out}`);
}

async function main() {
  for (const skin of SKINS) {
    await buildComposite(skin);
    await crops(skin);
  }
  writeManifest();
  console.log('\n[done] composites + crop receipts + manifest written to', RC_DIR);
}
main();
