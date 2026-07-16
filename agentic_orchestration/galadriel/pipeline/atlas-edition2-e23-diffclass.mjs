// atlas-edition2-e23-diffclass.mjs
// -----------------------------------------------------------------------------
// DIFF-CLASS RECEIPT for the E2.3 rail-arrow-orientation fix-pass.
//
// Proves that the ONLY change between the VENDORED "Build Horizon — Edition II"
// SVGs (reincarnated-loadout/public/atlas/, emitted by the E2.2 head
// atlas-edition2-r7-render.mjs) and the E2.3 re-render (this repo's E2.3 head
// atlas-edition2-e23-render.mjs) is the two ROTATED rail-label arrow glyphs on
// each skin:
//   west  rail  `← DEPLOY`  → `↑ DEPLOY`   (on-screen arrow now points LEFT/outward)
//   east  rail  `PERFORM →` → `PERFORM ↓`  (on-screen arrow now points RIGHT/outward)
//
// The emission timestamp does NOT drift (the E2.2 head stamps the footer from
// atlas.emitted_at, a frozen data field — verified re-render byte-equal), so the
// SVG diff is EXACTLY these two <text> elements per skin and nothing else.
//
// FAIL-LOUD: exits non-zero and prints the offending lines if ANY line other than
// the two rail-label text elements differs, or if the changed lines are not the
// expected old→new glyph swap. Read-only against both trees.
// -----------------------------------------------------------------------------
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const VENDORED_DIR = `${process.env.HOME}/Games/reincarnated-loadout/public/atlas`;
const E23_DIR = new URL('../captures/2026-07-16-atlas-edition2-e23/', import.meta.url).pathname;

const sha256 = (buf) => createHash('sha256').update(buf).digest('hex');

// The exact old→new substitutions we EXPECT (and only these).
// Each is asserted to appear as the sole content difference on exactly the lines
// carrying the rotated rail <text> for that pole. West = DEPLOY (left rail);
// East = PERFORM (right rail).
const EXPECTED = [
  { pole: 'DEPLOY (west/left rail)', old: '>← DEPLOY</text>', neu: '>↑ DEPLOY</text>' },
  { pole: 'PERFORM (east/right rail)', old: '>PERFORM →</text>', neu: '>PERFORM ↓</text>' },
];

let anyFail = false;
const report = [];

for (const skin of ['archive', 'instrument']) {
  const vPath = `${VENDORED_DIR}/atlas-edition2-${skin}.svg`;
  const ePath = `${E23_DIR}atlas-edition2-${skin}.svg`;
  const vBuf = readFileSync(vPath);
  const eBuf = readFileSync(ePath);
  const vLines = vBuf.toString('utf8').split('\n');
  const eLines = eBuf.toString('utf8').split('\n');

  const skinReport = {
    skin,
    vendored_path: vPath,
    e23_path: ePath,
    vendored_sha256: sha256(vBuf),
    e23_sha256: sha256(eBuf),
    vendored_bytes: vBuf.length,
    e23_bytes: eBuf.length,
    vendored_lines: vLines.length,
    e23_lines: eLines.length,
    changed_lines: [],
    element_counts: {},
    verdict: null,
  };

  // (1) Line-count must match (a pure in-place glyph swap cannot add/remove lines).
  if (vLines.length !== eLines.length) {
    anyFail = true;
    skinReport.verdict = `FAIL — line count differs (vendored ${vLines.length} vs e23 ${eLines.length}); NOT a pure glyph swap`;
    report.push(skinReport);
    continue;
  }

  // (2) Positional line diff — collect every line index whose content differs.
  const diffs = [];
  for (let i = 0; i < vLines.length; i++) {
    if (vLines[i] !== eLines[i]) diffs.push({ line: i + 1, vendored: vLines[i], e23: eLines[i] });
  }
  skinReport.changed_lines = diffs;

  // (3) EXACTLY two lines may differ, and each must be one of the expected swaps.
  const matchedExpected = new Set();
  let unexpected = 0;
  for (const d of diffs) {
    let matched = false;
    for (const exp of EXPECTED) {
      // The vendored line contains the OLD glyph string; the e23 line contains the
      // NEW glyph string; and the two lines are identical everywhere else (i.e.
      // vendored with old→new substitution yields the e23 line exactly).
      if (d.vendored.includes(exp.old) && d.e23.includes(exp.neu)
          && d.vendored.split(exp.old).join(exp.neu) === d.e23) {
        matched = true;
        matchedExpected.add(exp.pole);
        d.classified_as = exp.pole;
        d.substitution = `${exp.old.replace('</text>', '')} → ${exp.neu.replace('</text>', '')}`;
        break;
      }
    }
    if (!matched) { unexpected++; d.classified_as = 'UNEXPECTED'; }
  }

  // (4) <text> element count must be identical (no elements added/removed).
  const countText = (s) => (s.match(/<text\b/g) || []).length;
  const countCircle = (s) => (s.match(/<circle\b/g) || []).length;
  skinReport.element_counts = {
    text_vendored: countText(vBuf.toString('utf8')),
    text_e23: countText(eBuf.toString('utf8')),
    circle_vendored: countCircle(vBuf.toString('utf8')),
    circle_e23: countCircle(eBuf.toString('utf8')),
  };
  const ec = skinReport.element_counts;
  const elementCountsOk = ec.text_vendored === ec.text_e23 && ec.circle_vendored === ec.circle_e23;

  // (5) Verdict for this skin.
  const ok = diffs.length === 2
    && unexpected === 0
    && matchedExpected.size === EXPECTED.length
    && elementCountsOk;
  if (!ok) {
    anyFail = true;
    const reasons = [];
    if (diffs.length !== 2) reasons.push(`${diffs.length} changed lines (want exactly 2)`);
    if (unexpected > 0) reasons.push(`${unexpected} UNEXPECTED changed line(s)`);
    if (matchedExpected.size !== EXPECTED.length) reasons.push(`only matched swaps for [${[...matchedExpected].join(', ')}]`);
    if (!elementCountsOk) reasons.push(`element-count drift (text ${ec.text_vendored}→${ec.text_e23}, circle ${ec.circle_vendored}→${ec.circle_e23})`);
    skinReport.verdict = `FAIL — ${reasons.join('; ')}`;
  } else {
    skinReport.verdict = `PASS — exactly 2 changed lines, both the expected rail-arrow glyph swaps; <text> count ${ec.text_e23} unchanged; <circle> count ${ec.circle_e23} unchanged`;
  }
  report.push(skinReport);
}

// ---- print ----
console.log('================ E2.3 DIFF-CLASS RECEIPT ================');
console.log('VENDORED (E2.2, emitted by atlas-edition2-r7-render.mjs) vs E2.3 (atlas-edition2-e23-render.mjs)');
console.log('');
for (const r of report) {
  console.log(`---- skin=${r.skin} ----`);
  console.log(`  vendored: ${r.vendored_path}`);
  console.log(`            sha256=${r.vendored_sha256}  bytes=${r.vendored_bytes}  lines=${r.vendored_lines}`);
  console.log(`  e23:      ${r.e23_path}`);
  console.log(`            sha256=${r.e23_sha256}  bytes=${r.e23_bytes}  lines=${r.e23_lines}`);
  console.log(`  <text> count: vendored=${r.element_counts.text_vendored} e23=${r.element_counts.text_e23}   <circle> count: vendored=${r.element_counts.circle_vendored} e23=${r.element_counts.circle_e23}`);
  console.log(`  changed lines: ${r.changed_lines.length}`);
  for (const d of r.changed_lines) {
    console.log(`    · line ${d.line} [${d.classified_as}]${d.substitution ? `  ${d.substitution}` : ''}`);
    if (d.classified_as === 'UNEXPECTED') {
      console.log(`        VENDORED: ${d.vendored.slice(0, 200)}`);
      console.log(`        E23:      ${d.e23.slice(0, 200)}`);
    }
  }
  console.log(`  VERDICT: ${r.verdict}`);
  console.log('');
}
console.log(`OVERALL: ${anyFail ? 'FAIL — diff class exceeds the two rail-label text elements (see above)' : 'PASS — diff class = the two rail-label text elements per skin, nothing else'}`);
process.exit(anyFail ? 1 : 0);
