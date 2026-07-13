#!/usr/bin/env node
/**
 * Glance asset-staging — DERIVED static assets → public/ before vite build.
 *
 * KEPT SEPARATE FROM THE PARSER ON PURPOSE. The parser (glance/parser/parse.mjs)
 * has a closed charter: it reads canonical/** + the two Matt queues and emits the
 * state.json truth model — no LLM, no judgment, no side assets. This step provisions
 * DB-DERIVED static artifacts that are NOT part of the state-model truth path.
 *
 * What it stages (Glance contract v1.10 §7.7 render-adjacent addition):
 *   the RULED V1.2 Stratified Plane View (Q19 LOCKED 2026-07-13) — a provenance-clean
 *   derived artifact, chart = render(corpus.db), same class as chart = render(atlas.json).
 *   Source of truth stays gandalf's committed SVG; this step copies it in on every push
 *   so a re-render upstream flows through automatically. No duplicated committed binary.
 *
 * Founding law honored: DERIVED not authored · no LLM in the truth path · no hand-drawn
 * state. The provenance stamp (source commit, generator) is git-derived, not hand-typed.
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
// glance/app/scripts → repo root is three levels up.
const REPO_ROOT = resolve(__dirname, '..', '..', '..');

const VIEW_DIR_REL = 'agentic_orchestration/gandalf/views/v1-plane';
const SRC_REL = `${VIEW_DIR_REL}/plane_view_v1_2_stratified.svg`;
const SRC = join(REPO_ROOT, SRC_REL);
// The per-dot JSON (Phase-2 mouseover source). CELL-addressed, provenance-clean derived
// artifact from the same render (render_v1_2_stratified.py); one record per rendered dot.
// Staged exactly like the SVG — single source of truth stays gandalf's committed render.
const DOTS_REL = `${VIEW_DIR_REL}/plane_dots_v1_2.json`;
const DOTS_SRC = join(REPO_ROOT, DOTS_REL);
const OUT_DIR = join(REPO_ROOT, 'glance', 'app', 'public', 'atlas');
const OUT_SVG = join(OUT_DIR, 'plane_view_v1_2_stratified.svg');
const OUT_DOTS = join(OUT_DIR, 'plane_dots_v1_2.json');
const OUT_POS = join(OUT_DIR, 'plane_dot_positions.json');
const OUT_META = join(OUT_DIR, 'plane-provenance.json');

if (!existsSync(SRC)) {
  console.error(`[stage-assets] FAIL — source SVG missing: ${SRC_REL}`);
  process.exit(1);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT_SVG);

// Phase-2: the per-dot JSON. Not fatal-missing on its own — the SVG (Phase-1) still
// renders without it; the interactive cell explorer degrades to "not staged" if absent.
// But once emitted upstream it must flow through, so warn loudly rather than silently skip.
const dotsStaged = existsSync(DOTS_SRC);
if (dotsStaged) {
  copyFileSync(DOTS_SRC, OUT_DOTS);
} else {
  console.warn(`[stage-assets] WARN — per-dot JSON missing (Phase-2 mouseover disabled): ${DOTS_REL}`);
}

/**
 * Per-dot POSITION binder (Phase-2 v3 — single-kit-per-dot hover).
 *
 * The committed per-dot JSON is CELL-addressed only (no x/y — the jitter is PCG64,
 * not JS-reproducible). But the committed SVG carries every dot's exact pixel position
 * in its <use> elements, and the render scatters each cell+stratum group in kit order.
 * So we read the render's OWN dot coordinates back and bind each on-screen dot to its
 * kit — the same faithful "read the render's own geometry" method used for the cell grid
 * (galadriel-verified), NOT invented coordinates.
 *
 * Classification is glyph→kind (circle=corpus, star=mint, diamond=amp-null sliver),
 * centroid-y sort→stratum (FLAT always above SPIKY above VAR), and per-group COUNT
 * reconciliation against the JSON as a fail-loud self-check. If a future re-render
 * changes any assumption, the count check throws and we DEGRADE to the cell-level
 * popover (never emit silently-wrong per-dot bindings).
 *
 * The amp-null sliver draws ONE diamond per cell aggregating all its unkeyed kits
 * (render line ~622), so those kits share a marker position (shared_marker:true) and
 * the hover surfaces them together — honest to what the render actually shows.
 */
const PLANE_ROWS = ['FREE-MOVE', 'WALK', 'ROOTED'];
const PLANE_COLS = ['PROJECTILE', 'ORBITAL', 'NOVA', 'ZONE', 'BEAM', 'MELEE', 'SUMMON'];
const AMP_STRATA = ['FLAT', 'SPIKY', 'VAR'];
// Cell grid geometry — the render's OWN cell-background corners (galadriel-verified 0.00 offset).
const CELL_X0 = 110.541763, CELL_Y0 = 169.239412, CELL_PITCH = 103.68;
// matplotlib marker-path def ids for this render (verified against JSON counts:
// 455 corpus circles + 6 mint stars + 2 sliver diamonds = 463 grid dots).
const GLYPH_CORPUS = 'me898b4409d', GLYPH_MINT = 'm219d2e7fba', GLYPH_SLIVER = 'md1ae64e445';

function bindDotPositions(svgText, dotRecords) {
  const pcRe = /<g id="PathCollection_(\d+)">([\s\S]*?)<\/g>/g;
  const pcs = [];
  let m;
  while ((m = pcRe.exec(svgText))) {
    const body = m[2];
    const glyph = (body.match(/xlink:href="#(\w+)"/) || [])[1];
    const dots = [];
    const uRe = /x="([\d.]+)"\s+y="([\d.]+)"/g;
    let u;
    while ((u = uRe.exec(body))) dots.push([parseFloat(u[1]), parseFloat(u[2])]);
    if (!dots.length) continue;
    const cx = dots.reduce((s, d) => s + d[0], 0) / dots.length;
    const cy = dots.reduce((s, d) => s + d[1], 0) / dots.length;
    const ci = Math.floor((cx - CELL_X0) / CELL_PITCH);
    const ri = Math.floor((cy - CELL_Y0) / CELL_PITCH);
    const kind = glyph === GLYPH_CORPUS ? 'corpus' : glyph === GLYPH_MINT ? 'mint'
      : glyph === GLYPH_SLIVER ? 'sliver' : '?';
    pcs.push({ ri, ci, cy, kind, dots });
  }
  const cellPCs = new Map();
  for (const pc of pcs) {
    if (pc.ri < 0 || pc.ri > 2 || pc.ci < 0 || pc.ci > 6) {
      throw new Error(`PathCollection centroid outside grid (ri=${pc.ri} ci=${pc.ci})`);
    }
    const k = `${pc.ri}|${pc.ci}`;
    if (!cellPCs.has(k)) cellPCs.set(k, []);
    cellPCs.get(k).push(pc);
  }
  const grid = dotRecords.filter((r) => r.cell.movement && r.cell.delivery);
  const positions = [];
  const carry = (r, px, py, shared) => positions.push({
    px, py, shared_marker: shared,
    dot_id: r.dot_id, source: r.source, display_name: r.display_name,
    public_label: r.public_label, label_parts: r.label_parts, cell: r.cell,
    cell_confident: r.cell_confident, negative_canon: r.negative_canon,
  });
  for (let ri = 0; ri < 3; ri++) {
    for (let ci = 0; ci < 7; ci++) {
      const move = PLANE_ROWS[ri], deliv = PLANE_COLS[ci];
      const cellRecs = grid.filter((r) => r.cell.movement === move && r.cell.delivery === deliv);
      if (!cellRecs.length) continue;
      const pcList = cellPCs.get(`${ri}|${ci}`) || [];
      // keyed strata (corpus, then mint): sort PCs top→bottom = FLAT,SPIKY,VAR order.
      for (const kind of ['corpus', 'mint']) {
        const isMint = kind === 'mint';
        const groupPCs = pcList.filter((p) => p.kind === kind).sort((a, b) => a.cy - b.cy);
        const strataPresent = AMP_STRATA.filter((s) =>
          cellRecs.some((r) => r.cell.amp === s && (r.source === 'mint') === isMint));
        if (groupPCs.length !== strataPresent.length) {
          throw new Error(`${move}×${deliv} ${kind}: ${groupPCs.length} scatter groups vs ${strataPresent.length} JSON strata`);
        }
        strataPresent.forEach((stratum, idx) => {
          const pc = groupPCs[idx];
          const kits = cellRecs.filter((r) => r.cell.amp === stratum && (r.source === 'mint') === isMint);
          if (pc.dots.length !== kits.length) {
            throw new Error(`${move}×${deliv} ${kind} ${stratum}: ${pc.dots.length} dots vs ${kits.length} kits`);
          }
          kits.forEach((r, i) => carry(r, pc.dots[i][0], pc.dots[i][1], false));
        });
      }
      // amp-null sliver: ONE diamond per cell aggregating all its unkeyed kits.
      const sliver = cellRecs.filter((r) => r.cell.amp == null);
      if (sliver.length) {
        const diamonds = pcList.filter((p) => p.kind === 'sliver');
        if (diamonds.length !== 1 || diamonds[0].dots.length !== 1) {
          throw new Error(`${move}×${deliv} sliver: expected 1 diamond, got ${diamonds.length} groups`);
        }
        const [x, y] = diamonds[0].dots[0];
        for (const r of sliver) carry(r, x, y, true);
      }
    }
  }
  if (positions.length !== grid.length) {
    throw new Error(`bound ${positions.length} positions but JSON has ${grid.length} grid dots`);
  }
  return positions;
}

let posStaged = false;
if (dotsStaged) {
  try {
    const svgText = readFileSync(SRC, 'utf8');
    const dotRecords = JSON.parse(readFileSync(DOTS_SRC, 'utf8')).dots;
    const positions = bindDotPositions(svgText, dotRecords);
    writeFileSync(OUT_POS, JSON.stringify({
      schema: 'atlas-plane-dot-positions/v1',
      note: 'Per-dot pixel positions READ BACK from the committed render SVG and bound to '
        + 'kits by cell+stratum+kit-order. NOT invented — the render\'s own <use> coordinates.',
      viewBox: { w: 873.423631, h: 705.037812 },
      count: positions.length,
      dots: positions,
    }, null, 2) + '\n');
    posStaged = true;
  } catch (err) {
    // Fail-loud but non-fatal: a binding mismatch means an assumption broke upstream.
    // Do NOT emit silently-wrong per-dot data — degrade to the cell-level popover.
    console.warn(`[stage-assets] WARN — per-dot position binding failed (falling back to cell popover): ${err.message}`);
  }
}

// Git-derived source commit for the SVG (never hand-typed). Prefer the commit that
// last touched the file; fall back to deploy HEAD if history is shallow (Vercel).
function gitTry(cmd) {
  try {
    return execSync(cmd, { cwd: REPO_ROOT, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString()
      .trim();
  } catch {
    return '';
  }
}
// Prefer the commit that last touched the SVG (its true render provenance). On a
// remote Vercel build there is no .git in the upload, so fall back to the deploy SHA
// Vercel injects, then HEAD, then honest 'unknown'. LOCAL builds (where drax validates
// and the committed state is authoritative) resolve the exact render commit.
const sourceCommit =
  gitTry(`git log -1 --format=%H -- "${SRC_REL}"`) ||
  gitTry('git rev-parse HEAD') ||
  process.env.VERCEL_GIT_COMMIT_SHA ||
  'unknown';

const meta = {
  asset: '/atlas/plane_view_v1_2_stratified.svg',
  title: 'RULED V1.2 Stratified Plane View',
  ruling: 'Q19 LOCKED 2026-07-13',
  generator: 'render_v1_2_stratified.py',
  source_path: SRC_REL,
  source_commit: sourceCommit,
  // render = render(corpus.db): DB-DERIVED occupancy, not hand-derived — honors the
  // provenance law even though /atlas otherwise renders no occupancy (contract §7.7 r7).
  derivation: 'render(corpus.db)',
  staged_at: new Date().toISOString(),
};
writeFileSync(OUT_META, JSON.stringify(meta, null, 2) + '\n');

console.log(
  `[stage-assets] staged plane SVG${dotsStaged ? ' + dots JSON' : ''}${posStaged ? ' + dot positions' : ''} + provenance (source_commit ${sourceCommit.slice(0, 8)})`,
);
