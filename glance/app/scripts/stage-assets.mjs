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

import { copyFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
// glance/app/scripts → repo root is three levels up.
const REPO_ROOT = resolve(__dirname, '..', '..', '..');

const SRC_REL = 'agentic_orchestration/gandalf/views/v1-plane/plane_view_v1_2_stratified.svg';
const SRC = join(REPO_ROOT, SRC_REL);
const OUT_DIR = join(REPO_ROOT, 'glance', 'app', 'public', 'atlas');
const OUT_SVG = join(OUT_DIR, 'plane_view_v1_2_stratified.svg');
const OUT_META = join(OUT_DIR, 'plane-provenance.json');

if (!existsSync(SRC)) {
  console.error(`[stage-assets] FAIL — source SVG missing: ${SRC_REL}`);
  process.exit(1);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT_SVG);

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
const sourceCommit =
  gitTry(`git log -1 --format=%H -- "${SRC_REL}"`) ||
  gitTry('git rev-parse HEAD') ||
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
  `[stage-assets] staged plane SVG + provenance (source_commit ${sourceCommit.slice(0, 8)})`,
);
