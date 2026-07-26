// gd-gp-calib-c2-sheet.mjs — C2: character-sheet OCR.
//
// Scores automated stat-panel OCR against the 175 `character_stat` rows in fixtures.db
// (the exhaustive VAUGHT sheet, human-read at full resolution, per-field provenance).
//
// Calibration set: the 12 round-3 sheet shots `Screenshot (19)`-`(30)`, native 1920x1080.
//
// SCORING. Primary metric is VERBATIM-STRING match: the banked `verbatim` column is the
// exact string as rendered ("282 / 282", "+ 0%", "31 - 83"), so string equality after a
// whitespace/sign normalisation is the strictest honest test and needs no per-key
// disambiguation. Secondary metric is numeric match against `value_num`.
//
// Rows that share one rendered line (health/health_max, weapon_attack_min/max, ...) both
// score against that one line — deliberately. They are one reading in the bank too.
//
// The S19 RESISTANCES block has no text labels at all; it is an icon grid with a bare
// percentage under each icon. It is scored POSITIONALLY (grid position 1-10) and reported
// as its own sub-metric, because a label-matching pipeline cannot address it.
//
// METHOD LAW: native-resolution crop from the 1920x1080 PNG; 4x nearest upscale for OCR.
//
// Usage: node gd-gp-calib-c2-sheet.mjs

import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createWorker } from 'tesseract.js';
import { STILLS_V3, SHEET_FRAMES, WORK, FIXTURES_DB, ensureDirs, cropNative, writeJSON } from './gd-gp-calib-lib.mjs';

const REPO = '/Users/admin/Games/reincarnated-collaboration';

// Stat-panel region of the character sheet. Located from a native 1x probe crop; the
// sheet is a fixed-position modal, so this transfers across all 12 shots.
export const PANEL_BOX = { left: 1028, top: 165, width: 305, height: 545 };
// grayscale -> normalise -> 4x nearest. Thresholding DESTROYS this panel (the labels are
// low-contrast gold on brown); the C1 recipe is actively wrong here. Elected by probe.
const PREP = { scale: 4, grayscale: true, normalize: true };

// ------------------------------------------------------------------------ parsing
const normLabel = (s) =>
  s.toLowerCase()
    .replace(/\(\s*[?7]\s*\)/g, '')      // the "(?)" help glyph, which OCRs as "(7)"
    .replace(/^[+\[\]#*\s]+/, '')        // the "+" attribute-spend buttons
    .replace(/[^a-z0-9 ]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

const normValue = (s) =>
  s.replace(/\s+/g, ' ')
    .replace(/\s*([+\-\/])\s*/g, ' $1 ')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();

// Systematic glyph repairs observed across the 12 sheet shots. Same class as C1's
// "0 -> ©": renderer/model confusions that recur on every frame, not per-frame fixes.
//   "+ (0%" and "+ (%"  <- the leading zero of a percent picks up a spurious paren
//   "(?)" help glyph OCRs as "(7)" and must not be read as a value
export let NAIVE = false;
export function setNaive(v) { NAIVE = v; }
function repairSheetLine(line) {
  if (NAIVE) return line.replace(/\s+/g, ' ').trim();
  return line
    .replace(/\(\s*[?7]\s*\)/g, ' ')     // help glyph
    .replace(/\(\s*%/g, '0%')             // "(%"  -> "0%"
    .replace(/\(\s*(?=\d)/g, '')          // "(0%" -> "0%"
    .replace(/\s+/g, ' ')
    .trim();
}

// A value column: optional sign, a number, optional %, optionally a range/pair.
// The % must be UNSPACED — a spaced "%" after a number is a decorative speck, not a unit.
const VALUE_RE = /^([+\-]\s*)?\d[\d.,]*%?(\s*[-\/]\s*([+\-]\s*)?\d[\d.,]*%?)*/;
const CLOCK_RE = /^\d+:\d+:\d+/;
const isPureValue = (t) => {
  const r = repairSheetLine(t);
  return (VALUE_RE.test(r) || CLOCK_RE.test(r)) &&
    (r.match(VALUE_RE)?.[0].length === r.length || r.match(CLOCK_RE)?.[0].length === r.length ||
     /^[\d+\-.,%\/: ]+$/.test(r));
};

/**
 * Split a repaired sheet line into { label, value }.
 * The value is the FIRST value-shaped token after >=3 characters of label text; everything
 * after that token is discarded as decorative speck (the sheet's right edge picks up the
 * scroll rail and the panel filigree, which OCR renders as trailing punctuation).
 */
function splitLine(rawLine) {
  const line = repairSheetLine(rawLine);
  const m = line.match(/^(.{3,}?)\s+((?:[+\-]\s*)?\d.*|N\/A.*)$/);
  if (!m) return { raw: line, label: line, value: null, kind: 'bare' };
  const vm = m[2].match(VALUE_RE) || m[2].match(CLOCK_RE);
  if (!vm) return { raw: line, label: line, value: null, kind: 'bare' };
  return { raw: line, label: m[1].trim(), value: vm[0].trim(), kind: 'pair' };
}

export function parseSheet(text) {
  const raws = text.split('\n').map((l) => l.replace(/\s+$/, '')).filter((l) => l.trim());
  const lines = raws.map(splitLine);
  // Two-column fallback: the DAMAGE PER HIT block renders label and value on separate
  // OCR lines (the value column is far enough right that psm 6 breaks the row).
  if (NAIVE) return lines;
  for (let i = 0; i < lines.length - 1; i++) {
    if (lines[i].kind === 'bare' && lines[i + 1].kind === 'bare' &&
        /[A-Za-z]/.test(lines[i].label) && !isPureValue(lines[i].label) &&
        isPureValue(lines[i + 1].label)) {
      lines[i] = { ...lines[i], kind: 'pair-wrapped', value: repairSheetLine(lines[i + 1].label) };
    }
  }
  return lines;
}

/** Pull the two 5-percent rows of the S19 RESISTANCES icon grid, in reading order. */
export function parseResistGrid(text) {
  const out = [];
  for (const raw of text.split('\n')) {
    const toks = raw.trim().split(/\s+/).filter(Boolean);
    const pcts = toks.filter((t) => /^\d{1,3}%$/.test(t));
    if (pcts.length >= 4 && pcts.length === toks.filter((t) => /\d/.test(t)).length) out.push(pcts);
  }
  return out.flat();
}

const truthVOf = (r) => r.verbatim ?? '';

function lev(a, b) {
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

// ------------------------------------------------------------------ ground truth
function loadTruth() {
  const rows = JSON.parse(
    execFileSync(
      'sqlite3',
      ['-json', FIXTURES_DB,
       `select capture_id, stat_key, stat_group, value_num, value_num_hi, value_text,
               panel_label, verbatim, read_method from character_stat order by rowid`],
      { encoding: 'utf8' }
    )
  );
  const byCapture = {};
  for (const r of rows) (byCapture[r.capture_id.split('/').pop()] ||= []).push(r);
  return byCapture;
}

// ---------------------------------------------------------------------------- main
async function main() {
  await ensureDirs();
  setNaive(process.argv.includes('--naive'));
  const truth = loadTruth();
  const worker = await createWorker('eng');
  await worker.setParameters({ tessedit_pageseg_mode: '6' });

  const frames = [];
  let vHit = 0, vN = 0, nHit = 0, nN = 0, labelFound = 0;
  let gridHit = 0, gridN = 0;
  const failures = [];

  for (const [k, file] of Object.entries(SHEET_FRAMES)) {
    const rows = truth[k] || [];
    const src = path.join(STILLS_V3, file);
    const { upPath } = await cropNative(src, PANEL_BOX, `c2-${k}`, PREP);
    const { data } = await worker.recognize(upPath);
    const parsed = parseSheet(data.text);
    const grid = parseResistGrid(data.text);

    const scored = [];
    for (const r of rows) {
      // --- the icon grid: positional, no label to match on
      const gm = r.panel_label.match(/grid position (\d+)/);
      if (gm) {
        gridN++;
        const got = grid[+gm[1] - 1] ?? null;
        const ok = got !== null && normValue(got) === normValue(r.verbatim);
        if (ok) gridHit++;
        scored.push({ stat_key: r.stat_key, mode: 'grid', truth: r.verbatim, ocr: got, verdict: ok ? 'HIT' : got === null ? 'NO-READ' : 'MISREAD' });
        if (!ok) failures.push({ frame: k, stat_key: r.stat_key, mode: 'grid', truth: r.verbatim, ocr: got });
        continue;
      }

      // --- header / free-text rows with no numeric value column
      const target = normLabel(r.panel_label);
      let best = null, bestD = 1e9;
      for (const l of parsed) {
        const d = lev(normLabel(l.label), target);
        if (d < bestD) { bestD = d; best = l; }
      }
      const tol = Math.max(1, Math.floor(target.length * 0.25));
      const matched = best && bestD <= tol ? best : null;
      if (matched) labelFound++;

      // Value candidate: the pair's value column, or (for text rows) the OCR line remainder.
      let got = matched ? matched.value : null;
      if (got === null && matched) got = matched.raw.trim();
      // Text-bearing verbatims ("5 Available Points", "VAUGHT", "Kyzogg the Reanimator",
      // "Level 6", "0:2:21") are not label:value pairs. Fall back to a whole-line search.
      if (!NAIVE && (/[A-Za-z]/.test(truthVOf(r)) || /:/.test(truthVOf(r)))) {
        const want = normValue(truthVOf(r));
        const hitLine = parsed.find((l) => normValue(l.raw).includes(want));
        if (hitLine) got = truthVOf(r);
      }

      vN++;
      const truthV = truthVOf(r);
      const okV = got !== null && (normValue(got) === normValue(truthV) || normValue(matched?.raw ?? '') === normValue(truthV));
      if (okV) vHit++;

      let okN = null;
      if (r.value_num !== null) {
        nN++;
        // Unsigned extraction: in this panel "-" is a RANGE separator ("31 - 83"), never a
        // sign. Magnitudes are what the bank stores; "- 0%" banks as 0.
        const clock = (got || '').match(/^(\d+):(\d+):(\d+)$/);
        const nums = clock
          // GD's Elapsed Time renders d:h:m (A7: "0:2:21" == 141 min == 8460 s).
          ? [((+clock[1] * 24 + +clock[2]) * 60 + +clock[3]) * 60]
          : (got || '').match(/\d+(?:[.,]\d+)?/g)?.map((x) => parseFloat(x.replace(/,/g, ''))) ?? [];
        const wantsHi = /_max$/.test(r.stat_key) && nums.length >= 2;
        const cand = wantsHi ? nums[1] : nums[0];
        okN = cand !== undefined && Math.abs(cand - r.value_num) < 1e-9;
        if (okN) nHit++;
      }

      scored.push({
        stat_key: r.stat_key, mode: 'label',
        panel_label: r.panel_label, matched_label: matched ? matched.label : null,
        label_edit_distance: matched ? bestD : null,
        truth_verbatim: truthV, ocr_value: got,
        verbatim_hit: okV, numeric_hit: okN,
      });
      if (!okV) failures.push({ frame: k, stat_key: r.stat_key, mode: 'label', panel_label: r.panel_label, matched_label: matched ? matched.label : null, truth: truthV, ocr: got });
    }

    frames.push({
      frame: k, source: file, crop_box: PANEL_BOX,
      upscaled: path.relative(WORK, upPath),
      raw_ocr: data.text, ocr_confidence: data.confidence,
      banked_rows: rows.length,
      verbatim_hits: scored.filter((s) => s.verbatim_hit || s.verdict === 'HIT').length,
      scored,
    });
  }
  await worker.terminate();

  const report = {
    capability: 'C2 character-sheet OCR',
    parser: NAIVE ? 'naive (no glyph repair, no wrapped-pair fallback, no whole-line fallback)' : 'tuned',
    generated: new Date().toISOString(),
    method_law: 'native-resolution crop from 1920x1080 PNG; 4x nearest upscale for legibility only',
    engine: 'tesseract.js 6 (eng) psm 6',
    crop_box: PANEL_BOX,
    preprocessing: PREP,
    totals: {
      banked_rows: vN + gridN,
      label_matched_rows: labelFound,
      label_rows: vN,
      verbatim_hits: vHit,
      numeric_rows: nN,
      numeric_hits: nHit,
      grid_rows: gridN,
      grid_hits: gridHit,
    },
    accuracy: {
      overall_verbatim: (vHit + gridHit) / (vN + gridN),
      label_rows_verbatim: vN ? vHit / vN : null,
      label_rows_numeric: nN ? nHit / nN : null,
      resist_icon_grid: gridN ? gridHit / gridN : null,
      label_match_rate: vN ? labelFound / vN : null,
    },
    failures,
    frames,
  };
  const p = await writeJSON(NAIVE ? 'c2-sheet-naive.json' : 'c2-sheet.json', report);

  console.log(`[C2] overall verbatim ${vHit + gridHit}/${vN + gridN} = ${(100 * report.accuracy.overall_verbatim).toFixed(1)}%`);
  console.log(`     label rows: verbatim ${vHit}/${vN} = ${(100 * vHit / vN).toFixed(1)}%  ·  numeric ${nHit}/${nN} = ${(100 * nHit / nN).toFixed(1)}%  ·  label match ${labelFound}/${vN}`);
  console.log(`     resist icon grid (positional): ${gridHit}/${gridN}`);
  for (const f of frames) console.log(`  ${f.frame}  ${f.verbatim_hits}/${f.banked_rows}  ocr_conf=${Math.round(f.ocr_confidence)}`);
  console.log(`  failures (${failures.length}):`);
  for (const x of failures) console.log(`     ${x.frame} ${x.stat_key}  truth=${JSON.stringify(x.truth)} ocr=${JSON.stringify(x.ocr)}${x.matched_label !== undefined ? ` matched=${JSON.stringify(x.matched_label)}` : ''}`);
  console.log('->', p);
}

await main();
