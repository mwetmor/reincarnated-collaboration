// gd-gp-calib-c5-overlay.mjs — C5 / extraction target E5: green console-overlay text.
//
// The overlay is the `LogData` + `ShowAngerLevels` channel: per entity, a controller-state
// line above an `[entityId] Action State: X` line, rendered in bright green in WORLD space.
// It therefore has NO fixed crop — position tracks the entity. Detection is by colour mask
// + row-band grouping, which is the form that transfers to video frames unchanged.
//
// Truth (fixtures.db `trial_trace`, round 3):
//   t1s  monster-68957 (Pursue, Move)   + entity-17677 (LongIdle, Fidget)
//   t2s  monster-75289 (—, Move)
//   t3s  monster-77775 (Pursue, Move)
//
// METHOD LAW: the green mask and all band geometry are computed on native-resolution
// pixels; the only resampling is an integer nearest-neighbour upscale of the binary mask.
//
// Usage: node gd-gp-calib-c5-overlay.mjs

import path from 'node:path';
import sharp from 'sharp';
import { execFileSync } from 'node:child_process';
import { createWorker } from 'tesseract.js';
import { STILLS_V3, TRIAL_FRAMES, WORK, FIXTURES_DB, ensureDirs, rawRegion, px, writeJSON } from './gd-gp-calib-lib.mjs';

// Bright-green overlay ink. Tuned to exclude the mana orb's green glow by requiring a
// strong green-over-both-others margin; the orb is additionally excluded by geometry.
const isGreenInk = ([r, g, b]) => g > 140 && g - r > 50 && g - b > 50;

// The mana orb is HUD chrome anchored to the bottom-centre-right and is bright green.
// It is excluded by rectangle, not by threshold — thresholds that kill it also kill text.
const HUD_EXCLUSIONS = [{ x0: 1150, y0: 930, x1: 1400, y1: 1080 }];
const inExclusion = (x, y) => HUD_EXCLUSIONS.some((e) => x >= e.x0 && x <= e.x1 && y >= e.y0 && y <= e.y1);

const MIN_ROW_INK = 4;     // px of green in a row for it to count as a text row
const ROW_GAP = 3;         // rows of silence that close a band
const MIN_BAND_INK = 150;  // total green px for a band to be a text block, not a speck
const COL_GAP = 40;        // px of empty columns that split a row-band into two entity blocks

/**
 * Detect overlay text blocks on a native-resolution frame.
 * Two-stage: row-banding, then COLUMN splitting inside each band. Row-banding alone
 * merges two entities that happen to share screen rows — observed on t2s, where a
 * `Dying` block at x~699 and the player's block at x~960 landed in one band.
 */
export async function detectBands(srcPath, W = 1920, H = 1080) {
  const reg = await rawRegion(srcPath, { left: 0, top: 0, width: W, height: H });
  const mask = new Uint8Array(W * H);
  const rows = new Array(H).fill(0);
  for (let y = 0; y < H; y++) {
    let n = 0;
    for (let x = 0; x < W; x++) {
      if (inExclusion(x, y)) continue;
      if (!isGreenInk(px(reg, x, y))) continue;
      mask[y * W + x] = 1;
      n++;
    }
    rows[y] = n;
  }
  const rowBands = [];
  let cur = null, gap = 0;
  for (let y = 0; y < H; y++) {
    if (rows[y] >= MIN_ROW_INK) {
      if (!cur) cur = { y0: y, y1: y, ink: 0 };
      cur.y1 = y; cur.ink += rows[y]; gap = 0;
    } else if (cur) {
      gap++;
      if (gap > ROW_GAP) { rowBands.push(cur); cur = null; }
    }
  }
  if (cur) rowBands.push(cur);

  const blocks = [];
  for (const b of rowBands) {
    const cols = new Array(W).fill(0);
    for (let y = b.y0; y <= b.y1; y++)
      for (let x = 0; x < W; x++) if (mask[y * W + x]) cols[x]++;
    let seg = null, cgap = 0;
    const segs = [];
    for (let x = 0; x < W; x++) {
      if (cols[x] > 0) {
        if (!seg) seg = { x0: x, x1: x, ink: 0 };
        seg.x1 = x; seg.ink += cols[x]; cgap = 0;
      } else if (seg) {
        cgap++;
        if (cgap > COL_GAP) { segs.push(seg); seg = null; }
      }
    }
    if (seg) segs.push(seg);
    for (const sg of segs) {
      // tighten the row extent to this column segment
      let y0 = b.y1, y1 = b.y0;
      for (let y = b.y0; y <= b.y1; y++) {
        let n = 0;
        for (let x = sg.x0; x <= sg.x1; x++) if (mask[y * W + x]) n++;
        if (n > 0) { if (y < y0) y0 = y; if (y > y1) y1 = y; }
      }
      blocks.push({ y0, y1, x0: sg.x0, x1: sg.x1, ink: sg.ink });
    }
  }
  return blocks.filter((b) => b.ink >= MIN_BAND_INK);
}

async function bandMask(src, band, name, pad = 4, scale = 6) {
  const box = {
    left: Math.max(0, band.x0 - pad),
    top: Math.max(0, band.y0 - pad),
    width: Math.min(1920, band.x1 + pad) - Math.max(0, band.x0 - pad) + 1,
    height: Math.min(1080, band.y1 + pad) - Math.max(0, band.y0 - pad) + 1,
  };
  const reg = await rawRegion(src, box);
  const buf = Buffer.alloc(reg.width * reg.height);
  for (let y = 0; y < reg.height; y++)
    for (let x = 0; x < reg.width; x++) buf[y * reg.width + x] = isGreenInk(px(reg, x, y)) ? 0 : 255;
  const out = path.join(WORK, 'upscaled', `${name}.png`);
  await sharp(buf, { raw: { width: reg.width, height: reg.height, channels: 1 } })
    .resize({ width: reg.width * scale, height: reg.height * scale, kernel: 'nearest' })
    .extend({ top: 20, bottom: 20, left: 20, right: 20, background: { r: 255, g: 255, b: 255 } })
    .png()
    .toFile(out);
  return { out, box };
}

// `[68957] Action State: Move`
// `[68957] Action State: Move`. Observed OCR variants of the literal: Achion, Acton,
// Actlon. The bracket glyphs are routinely mangled to ] | ( { and are not required.
const ACTION_RE = /[\[\]|({]?\s*([\dOo]{4,6})\s*[\]\[|)}]?\s*A[ck][thil]{0,3}[oi]n\s*Stat[ec]?\s*[:;.]?\s*([A-Za-z]+)/i;
const CONTROLLER_TOKENS = [
  'Pursue', 'LongIdle', 'Idle', 'AlertBeforePursue', 'Startup', 'FollowLeader',
  'Attack', 'Flee', 'Wander', 'Return', 'Dying', 'UseSkill', 'Fidget', 'Move',
];

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

/**
 * Fuzzy-match a controller line to the known token roster. The overlay font renders
 * `LongIdle` as `Lomgldle` (rn->m, I->l) reliably enough that exact matching throws away
 * a correct read. Threshold: edit distance <= 2 AND unique best candidate.
 */
function snapController(line) {
  // Use the FIRST alphabetic token only: the controller line is a single word, and the
  // overlay's decorative specks land after it ("Lomgldle i A _").
  const tok = (line.match(/[A-Za-z]{3,}/) || [])[0];
  if (!tok) return null;
  const bare = tok;
  const scored = CONTROLLER_TOKENS
    .map((t) => ({ t, d: lev(bare.toLowerCase(), t.toLowerCase()) }))
    .sort((a, b) => a.d - b.d);
  if (scored[0].d > 2) return null;
  if (scored.length > 1 && scored[1].d === scored[0].d) return null; // ambiguous
  return scored[0].t;
}

export function parseOverlay(text) {
  const lines = text.split('\n').map((s) => s.trim()).filter(Boolean);
  const out = { entity_id: null, action_state: null, controller_state: null, lines };
  for (const l of lines) {
    const m = l.match(ACTION_RE);
    if (m) { out.entity_id = m[1].replace(/[Oo]/g, '0'); out.action_state = m[2]; continue; }
    const snapped = snapController(l);
    if (snapped && out.controller_state === null) out.controller_state = snapped;
  }
  return out;
}

// ------------------------------------------------------------------ ground truth
function loadTruth() {
  const rows = JSON.parse(
    execFileSync(
      'sqlite3',
      ['-json', FIXTURES_DB,
       `select capture_id, entity_ref, channel, trace_token from trial_trace where capture_id like '%s3%'`],
      { encoding: 'utf8' }
    )
  );
  const byFrame = {};
  for (const r of rows) {
    const k = r.capture_id.split('/').pop();
    const ent = (byFrame[k] ||= {});
    const id = (r.entity_ref.match(/(\d{4,6})/) || [])[1] || r.entity_ref;
    const e = (ent[id] ||= { entity_ref: r.entity_ref, entity_id: id });
    if (r.channel === 'logdata-console') e.action_state = r.trace_token;
    else e.controller_state = r.trace_token;
  }
  return byFrame;
}

// ---------------------------------------------------------------------------- main
async function main() {
  await ensureDirs();
  const truth = loadTruth();
  const worker = await createWorker('eng');
  await worker.setParameters({ tessedit_pageseg_mode: '6' });

  const frames = [];
  let idHit = 0, idN = 0, actHit = 0, actN = 0, ctrlHit = 0, ctrlN = 0;
  // Token-only scoring: was the (controller, action) pair READ correctly anywhere on the
  // frame, regardless of whether the entity-id attribution succeeded? This separates the
  // MEASUREMENT channel from the ATTRIBUTION channel, which fail independently.
  let tokActHit = 0, tokCtrlHit = 0;

  for (const [k, file] of Object.entries(TRIAL_FRAMES)) {
    const src = path.join(STILLS_V3, file);
    const bands = await detectBands(src);
    const reads = [];
    for (let i = 0; i < bands.length; i++) {
      const { out, box } = await bandMask(src, bands[i], `c5-${k}-band${i}`);
      const { data } = await worker.recognize(out);
      reads.push({
        band: bands[i], crop: box,
        upscaled: path.relative(WORK, out),
        raw_ocr: data.text.trim(),
        confidence: data.confidence,
        parsed: parseOverlay(data.text),
      });
    }

    // Score each banked entity for this frame against the best-matching detected band.
    const frameTruth = truth[k] || {};
    const scored = [];
    for (const [id, t] of Object.entries(frameTruth)) {
      const match = reads.find((r) => r.parsed.entity_id === id) || null;
      idN++;
      if (match) idHit++;
      if (t.action_state) {
        actN++;
        if (match && match.parsed.action_state &&
            match.parsed.action_state.toLowerCase() === t.action_state.toLowerCase()) actHit++;
      }
      if (t.controller_state) {
        ctrlN++;
        if (match && match.parsed.controller_state &&
            match.parsed.controller_state.toLowerCase() === t.controller_state.toLowerCase()) ctrlHit++;
      }
      const anyAct = t.action_state && reads.some((r) => r.parsed.action_state?.toLowerCase() === t.action_state.toLowerCase());
      const anyCtrl = t.controller_state && reads.some((r) => r.parsed.controller_state?.toLowerCase() === t.controller_state.toLowerCase());
      if (anyAct) tokActHit++;
      if (anyCtrl) tokCtrlHit++;
      scored.push({
        truth: t,
        action_state_read_somewhere: !!anyAct,
        controller_state_read_somewhere: !!anyCtrl,
        matched_band: match ? reads.indexOf(match) : null,
        ocr: match ? match.parsed : null,
        entity_id_ok: !!match,
        action_state_ok: !!(match && t.action_state && match.parsed.action_state?.toLowerCase() === t.action_state.toLowerCase()),
        controller_state_ok: !!(match && t.controller_state && match.parsed.controller_state?.toLowerCase() === t.controller_state.toLowerCase()),
      });
    }

    // Bands the bank has no row for — candidate un-banked observations, not errors.
    const unbanked = reads
      .filter((r) => r.parsed.entity_id && !frameTruth[r.parsed.entity_id])
      .map((r) => r.parsed);

    frames.push({ frame: k, source: file, bands_detected: bands.length, reads, scored, unbanked_entities: unbanked });
  }
  await worker.terminate();

  const report = {
    capability: 'C5 overlay text (E5)',
    generated: new Date().toISOString(),
    method_law: 'green mask + band grouping on native-resolution pixels; 6x nearest upscale of the binary mask for OCR only',
    engine: 'tesseract.js 6 (eng) psm 6',
    detector: { isGreenInk: 'g>140 && g-r>50 && g-b>50', hud_exclusions: HUD_EXCLUSIONS, MIN_ROW_INK, ROW_GAP, MIN_BAND_INK },
    totals: {
      banked_entities: idN,
      entity_id_located: idHit,
      action_state: { n: actN, hit: actHit },
      controller_state: { n: ctrlN, hit: ctrlHit },
      token_only_action_state: { n: actN, hit: tokActHit },
      token_only_controller_state: { n: ctrlN, hit: tokCtrlHit },
    },
    accuracy: {
      entity_id: idN ? idHit / idN : null,
      action_state: actN ? actHit / actN : null,
      controller_state: ctrlN ? ctrlHit / ctrlN : null,
      token_only_action_state: actN ? tokActHit / actN : null,
      token_only_controller_state: ctrlN ? tokCtrlHit / ctrlN : null,
    },
    frames,
  };
  const p = await writeJSON('c5-overlay.json', report);

  console.log(`[C5] ATTRIBUTED  entity id ${idHit}/${idN} · action state ${actHit}/${actN} · controller state ${ctrlHit}/${ctrlN}`);
  console.log(`[C5] TOKEN-ONLY  action state ${tokActHit}/${actN} · controller state ${tokCtrlHit}/${ctrlN}  (read correctly somewhere on the frame, ignoring id attribution)`);
  for (const f of frames) {
    console.log(`  ${f.frame}  bands=${f.bands_detected}`);
    for (const r of f.reads)
      console.log(`     band@${r.band.y0}-${r.band.y1} x${r.band.x0}-${r.band.x1}  ${JSON.stringify(r.raw_ocr.replace(/\n/g, ' | '))}  -> id=${r.parsed.entity_id} action=${r.parsed.action_state} ctrl=${r.parsed.controller_state}`);
    for (const s of f.scored)
      console.log(`     TRUTH ${s.truth.entity_ref} action=${s.truth.action_state ?? '-'} ctrl=${s.truth.controller_state ?? '-'}  => id:${s.entity_id_ok ? 'HIT' : 'MISS'} action:${s.truth.action_state ? (s.action_state_ok ? 'HIT' : 'MISS') : 'n/a'} ctrl:${s.truth.controller_state ? (s.controller_state_ok ? 'HIT' : 'MISS') : 'n/a'}`);
    if (f.unbanked_entities.length)
      console.log(`     UNBANKED reads: ${f.unbanked_entities.map((u) => `[${u.entity_id}] ${u.controller_state ?? '?'}/${u.action_state ?? '?'}`).join(', ')}`);
  }
  console.log('->', p);
}

await main();
