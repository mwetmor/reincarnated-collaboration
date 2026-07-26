// gd-gp-calib-c1-panel.mjs — C1 / extraction target E1: PlayStats panel OCR.
//
// Scores automated panel-counter OCR against the human-read values banked in
// fixtures.db (`trial_measurement`, read_method='screenshot-fullres', uncertainty_abs=0).
//
// Calibration set: 13 panel-bearing native 1920x1080 stills —
//   6 round-3 trial frames + 6 round-2 panel shots + 1 round-1 baseline panel.
//
// METHOD LAW: the crop is taken from the native PNG at native resolution; the only
// resampling is an integer nearest-neighbour upscale for OCR legibility. No value is
// read from any downscaled render.
//
// hp_current / hp_max are NOT panel fields — they are the HP-globe numerals. They are
// excluded here and scored under C3 (gd-gp-calib-c3-globe.mjs).
//
// Two parsers are kept deliberately:
//   --parser=v1  naive: strict labels, strict `label: value`, no glyph repair.
//   --parser=v2  tuned: fuzzy labels + glyph-confusion repair + decimal recovery (default).
// Reporting both is the honest way to show how much of the accuracy is OCR and how much
// is post-processing.
//
// Usage: node gd-gp-calib-c1-panel.mjs [--variant=thr4x] [--parser=v2]

import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createWorker } from 'tesseract.js';
import { WORK, FIXTURES_DB, ensureDirs, cropNative, writeJSON } from './gd-gp-calib-lib.mjs';

const REPO = '/Users/admin/Games/reincarnated-collaboration';

// ---------------------------------------------------------------- panel geometry
// Located once from a LOCATOR render + native 1x probe crops. Panel is top-right,
// anchored to the screen edge; identical offset in all three sittings.
export const PANEL_BOX = { left: 1400, top: 20, width: 520, height: 330 };

const VARIANTS = {
  raw4x: { scale: 4 },
  graynorm4x: { scale: 4, grayscale: true, normalize: true },
  thr4x: { scale: 4, grayscale: true, normalize: true, threshold: 150 },
};

// Panel fields only. hp_current/hp_max deliberately absent (see header).
const PANEL_KEYS = new Set([
  'play_time',
  'total_score',
  'deaths',
  'kills',
  'health_potions_used',
  'mana_potions_used',
  'max_level_achieved',
  'dps_field',
  'life_healed',
  'shield_block_chance',
  'skill_use_count',
]);

// -------------------------------------------------------------- glyph repair (v2)
// Systematic tesseract confusions observed across the 13-frame set, not per-frame hacks:
//   "0"  -> "©" (copyright) in the deaths line, every frame, all three sittings
//   "."  -> "_" or " " in 2-dp float values
//   "x"  -> "z", "n" -> "p" in small-cap labels ("Maz. level", "Mapa potions")
//   "u"  -> "v" ("vsed", "defavlt")
function repairNumeric(s) {
  return s
    .replace(/[©®Ｏ]/g, '0')
    .replace(/(?<=[\s:])[Oo](?=[\s|.,]|$)/g, '0')
    .replace(/[|]/g, '');
}

const parseInt10 = (s) => {
  const m = repairNumeric(s).match(/(-?\d+)/);
  return m ? parseInt(m[1], 10) : null;
};

// 2-dp float where the decimal separator may have been eaten or mangled.
const parseFixed2 = (s) => {
  const t = repairNumeric(s);
  let m = t.match(/(-?\d+)\s*[._,]\s*(\d{2})(?!\d)/);
  if (m) return parseFloat(`${m[1]}.${m[2]}`);
  m = t.match(/(-?\d+)\s+(\d{2})(?!\d)/); // separator lost to whitespace
  if (m) return parseFloat(`${m[1]}.${m[2]}`);
  m = t.match(/(-?\d+)/);
  return m ? parseFloat(m[1]) : null;
};

const parseFloatLoose = (s) => {
  const m = repairNumeric(s).match(/(-?\d+(?:[.,]\d+)?)/);
  return m ? parseFloat(m[1].replace(',', '.')) : null;
};

// "145 min 35 sec" -> 8735 s. Tolerates an hours term.
function parseClock(s) {
  const t = repairNumeric(s);
  const hr = t.match(/(\d+)\s*hr/i);
  const min = t.match(/(\d+)\s*m[il]n/i);
  const sec = t.match(/(\d+)\s*sec/i);
  if (!hr && !min && !sec) return null;
  return (
    (hr ? +hr[1] * 3600 : 0) + (min ? +min[1] * 60 : 0) + (sec ? +sec[1] : 0)
  );
}

// ------------------------------------------------------------------- line specs
// v1 = strict; v2 = fuzzy. Both are ordered; first match wins per line.
const SPECS = {
  v1: [
    { key: 'play_time', re: /play\s*time\s*:/i, parse: parseClock },
    { key: 'total_score', re: /total\s*score\s*:/i, parse: parseInt10 },
    { key: 'deaths', re: /number\s*of\s*deaths\s*:/i, parse: (s) => { const m=s.match(/(-?\d+)/); return m?+m[1]:null; } },
    { key: 'kills', re: /number\s*of\s*kills\s*:/i, parse: (s) => { const m=s.match(/(-?\d+)/); return m?+m[1]:null; } },
    { key: 'health_potions_used', re: /health\s*potions\s*used\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+)/);return m?+m[1]:null;} },
    { key: 'mana_potions_used', re: /mana\s*potions\s*used\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+)/);return m?+m[1]:null;} },
    { key: 'max_level_achieved', re: /max\.\s*level\s*achieved\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+)/);return m?+m[1]:null;} },
    { key: 'dps_field', re: /damage\s*per\s*second\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+\.\d+)/);return m?parseFloat(m[1]):null;} },
    { key: 'life_healed', re: /life\s*healed\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+\.\d+)/);return m?parseFloat(m[1]):null;} },
    { key: 'shield_block_chance', re: /shield\s*block\s*chance\s*:/i, parse: (s)=>{const m=s.match(/(-?\d+\.\d+)/);return m?parseFloat(m[1]):null;} },
  ],
  v2: [
    { key: 'play_time', re: /pl?ay\s*t[il]me/i, parse: parseClock },
    { key: 'total_score', re: /t[o0]tal\s*sc/i, parse: parseInt10 },
    { key: 'deaths', re: /deaths/i, parse: parseInt10 },
    { key: 'kills', re: /k[il]lls|kills/i, parse: parseInt10 },
    { key: 'health_potions_used', re: /h[eo]a?lth\s*p[o0]t[il]ons?/i, parse: parseInt10 },
    { key: 'mana_potions_used', re: /\bm[aoe][npr][aoe]?\s*p[o0]t[il]ons?/i, parse: parseInt10 },
    { key: 'max_level_achieved', re: /ma[xz][\W_]*level\s*ach[il]eved/i, parse: parseInt10 },
    { key: 'dps_field', re: /damage\s*per\s*sec/i, parse: parseFixed2 },
    { key: 'life_healed', re: /l[il1]fe\s*healed/i, parse: parseFixed2 },
    { key: 'shield_block_chance', re: /sh[il]eld\s*bl[o0]ck/i, parse: parseFixed2 },
  ],
};

// `records/skills/default/defaultweaponattack.dbr : 22`
// Observed separators across the set: ":", "-", ":-", and "." eaten to " ".
const SKILL_LINE = {
  v1: /records\/skills\/([^:]*?)\s*:\s*(\d+)\s*$/,
  v2: /rec[o0]r\s?ds?\W{0,3}\s*skills?\W(.*?)[\s:;\-~_.]+(\d+)\s*$/i,
};

function resolveSkillSubkey(tail) {
  const flat = tail.toLowerCase().replace(/[^a-z]/g, '');
  if (/weap[o0]nat[tl]ack|weaponatlack|weapenattack|weaponattack/.test(flat))
    return 'records/skills/default/defaultweaponattack.dbr';
  if (/kickattack/.test(flat)) return 'records/skills/default/defaultkickattack.dbr';
  return `UNRESOLVED:${tail.trim()}`;
}

export function parsePanel(text, parser = 'v2') {
  const specs = SPECS[parser];
  const skillRe = SKILL_LINE[parser];
  const out = { skills: {} };
  for (const rawLine of text.split('\n')) {
    const line = rawLine.trim();
    if (!line) continue;
    const sk = line.match(skillRe);
    if (sk) {
      out.skills[resolveSkillSubkey(sk[1])] = parseInt(sk[2], 10);
      continue;
    }
    for (const spec of specs) {
      const m = line.match(spec.re);
      if (!m) continue;
      const v = spec.parse(line.slice(m.index + m[0].length));
      if (v !== null && out[spec.key] === undefined) out[spec.key] = v;
      break;
    }
  }
  return out;
}

// ------------------------------------------------------------------ ground truth
function loadCaptures() {
  const rows = JSON.parse(
    execFileSync('sqlite3', ['-json', FIXTURES_DB, `select capture_id, path from capture`], {
      encoding: 'utf8',
    })
  );
  return Object.fromEntries(rows.map((r) => [r.capture_id, path.join(REPO, r.path)]));
}

function loadGroundTruth() {
  const rows = JSON.parse(
    execFileSync(
      'sqlite3',
      [
        '-json',
        FIXTURES_DB,
        `select trial_id, phase, measure_key, measure_subkey, value_num, read_method,
                capture_id, verbatim
         from trial_measurement
         where capture_id is not null and phase in ('before','after')`,
      ],
      { encoding: 'utf8' }
    )
  );
  const byCapture = {};
  for (const r of rows) {
    if (!PANEL_KEYS.has(r.measure_key)) continue;
    (byCapture[r.capture_id] ||= []).push(r);
  }
  return byCapture;
}

// ---------------------------------------------------------------------------- main
async function main() {
  await ensureDirs();
  const arg = (n, d) => (process.argv.find((a) => a.startsWith(`--${n}=`)) || `--${n}=${d}`).split('=')[1];
  const variantName = arg('variant', 'thr4x');
  const parser = arg('parser', 'v2');
  const variant = VARIANTS[variantName];
  if (!variant) throw new Error(`unknown variant ${variantName}`);

  const captures = loadCaptures();
  const gt = loadGroundTruth();
  const worker = await createWorker('eng');

  const perFrame = [];
  const perKey = {};
  let hit = 0, miss = 0, absentHit = 0;

  for (const [captureId, rows] of Object.entries(gt)) {
    const src = captures[captureId];
    if (!src) continue;
    const safe = captureId.replace(/[^A-Za-z0-9]/g, '_');
    const { upPath } = await cropNative(src, PANEL_BOX, `c1-${safe}-${variantName}`, variant);
    const { data } = await worker.recognize(upPath);
    const read = parsePanel(data.text, parser);

    const fields = [];
    for (const r of rows) {
      const got =
        r.measure_key === 'skill_use_count' ? read.skills[r.measure_subkey] : read[r.measure_key];
      const bucket = (perKey[r.measure_key] ||= { n: 0, hit: 0 });

      if (r.read_method === 'absent') {
        const found = got !== undefined && got !== null;
        fields.push({
          measure_key: r.measure_key,
          measure_subkey: r.measure_subkey || null,
          truth_absent: true,
          ocr: found ? got : null,
          verdict: found ? 'FALSE-POSITIVE' : 'HIT-ABSENT',
        });
        bucket.n++;
        if (found) miss++;
        else { absentHit++; bucket.hit++; }
        continue;
      }

      const truth = r.value_num;
      const ok = got !== undefined && got !== null && Math.abs(got - truth) < 1e-9;
      fields.push({
        measure_key: r.measure_key,
        measure_subkey: r.measure_subkey || null,
        truth,
        ocr: got === undefined ? null : got,
        verdict: ok ? 'HIT' : got === undefined || got === null ? 'NO-READ' : 'MISREAD',
        verbatim: r.verbatim,
      });
      bucket.n++;
      if (ok) { hit++; bucket.hit++; } else miss++;
    }

    perFrame.push({
      capture_id: captureId,
      source: path.relative(REPO, src),
      crop_box: PANEL_BOX,
      variant: variantName,
      parser,
      upscaled: path.relative(WORK, upPath),
      raw_ocr: data.text,
      fields,
      hits: fields.filter((f) => f.verdict === 'HIT' || f.verdict === 'HIT-ABSENT').length,
      scored: fields.length,
    });
  }

  await worker.terminate();

  const totalScored = hit + miss + absentHit;
  const report = {
    capability: 'C1 panel OCR (E1)',
    generated: new Date().toISOString(),
    method_law:
      'native-resolution crop from 1920x1080 PNG; 4x nearest-neighbour upscale for legibility only',
    engine: 'tesseract.js 6 (eng), LSTM default',
    variant: variantName,
    parser,
    crop_box: PANEL_BOX,
    frames_scored: perFrame.length,
    totals: {
      scored_fields: totalScored,
      value_hits: hit,
      absent_hits: absentHit,
      misses: miss,
    },
    accuracy_all: totalScored ? (hit + absentHit) / totalScored : null,
    accuracy_valued_only: hit + miss ? hit / (hit + miss) : null,
    per_key: Object.fromEntries(
      Object.entries(perKey).map(([k, v]) => [k, { n: v.n, hit: v.hit, acc: v.hit / v.n }])
    ),
    frames: perFrame,
  };
  const p = await writeJSON(`c1-panel-${variantName}-${parser}.json`, report);

  console.log(
    `[C1 ${variantName}/${parser}] ${hit + absentHit}/${totalScored} = ${(100 * report.accuracy_all).toFixed(1)}%  ` +
      `(valued-only ${hit}/${hit + miss} = ${(100 * report.accuracy_valued_only).toFixed(1)}%)`
  );
  for (const f of perFrame) {
    const bad = f.fields.filter((x) => x.verdict !== 'HIT' && x.verdict !== 'HIT-ABSENT');
    console.log(
      `  ${f.capture_id.padEnd(34)} ${f.hits}/${f.scored}` +
        (bad.length
          ? '  FAIL: ' +
            bad
              .map((x) => `${x.measure_key}${x.measure_subkey ? '[' + x.measure_subkey.split('/').pop() + ']' : ''}=${x.ocr}${x.truth_absent ? ' (truth ABSENT)' : ` (truth ${x.truth})`}`)
              .join(', ')
          : '')
    );
  }
  console.log('per-key:', JSON.stringify(report.per_key));
  console.log('->', p);
}

await main();
