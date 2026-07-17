#!/usr/bin/env node
/**
 * Glance asset-staging — DERIVED static assets → public/ before vite build.
 *
 * KEPT SEPARATE FROM THE PARSER ON PURPOSE. The parser (glance/parser/parse.mjs)
 * has a closed charter: it reads canonical/** + the two Matt queues and emits the
 * state.json truth model — no LLM, no judgment, no side assets. This step provisions
 * DB-DERIVED static artifacts that are NOT part of the state-model truth path.
 *
 * v1.13 EDITION-IV SERVING CUTOVER (drax, Matt-ruled 2026-07-17): the /atlas page is
 * now Build Horizon Edition IV. This step:
 *   (1) stages the two verified Edition-IV render SVGs (instrument + archive, served
 *       UNMODIFIED — byte-copy, never hand-edited/scraped) + render-provenance.json from
 *       galadriel's VERIFY-ACCEPTED E4 capture (52/52 acceptance + G-3 anchoring PASS
 *       0-moved/0-missing) into public/atlas/;
 *   (2) runs the build-time slim derivation (build-atlas-interactive.mjs) which reads the
 *       in-repo 7.5MB Edition-IV emission (BUILD INPUT ONLY, never client-shipped) +
 *       the corpus provenance/engine-key sidecars + the prior-edition (E3) atlas for the
 *       Path-A additive floor, and writes public/atlas/atlas-interactive.json (~2MB) with
 *       its build-fail guard intact.
 *
 * The v1.12 Edition-III staging RETIRES with the E4 cutover (git keeps the lineage).
 * public/atlas/ is gitignored — every artifact here is a regenerated build output,
 * single source of truth stays upstream.
 *
 * Founding law honored: DERIVED not authored · no LLM in the truth path · no hand-drawn
 * state. The provenance stamp (source commit) is git-derived, not hand-typed.
 */

import { copyFileSync, existsSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
// glance/app/scripts → repo root is three levels up.
const REPO_ROOT = resolve(__dirname, '..', '..', '..');
const OUT_DIR = join(REPO_ROOT, 'glance', 'app', 'public', 'atlas');

// v1.12: WIPE the staged atlas dir first so ONE served truth remains (retired-edition
// plates + prior-iteration provenance don't linger and bloat dist). The dir is
// gitignored + fully regenerated below, so a clean wipe is safe.
rmSync(OUT_DIR, { recursive: true, force: true });

// ── Atlas Edition-IV (the Matt-ruled 2026-07-17 serving cutover render) — the interactive
//    instrument's vendored plates. VENDORED from galadriel's VERIFY-ACCEPTED E4 capture
//    (52/52 acceptance + G-3 anchoring PASS 0-moved/0-missing, commit 56ccb83b). Served
//    UNMODIFIED (byte-copy); we NEVER hand-edit them and NEVER scrape values out of them —
//    the page reads its numbers from the slim atlas-interactive.json (built below) +
//    render-provenance.json. Two verified deterministic skins: instrument (light) +
//    archive (dark, black-copy lead). E4 plates carry the same data-hook grammar as E3
//    (data-el / data-kit / data-core, layer groups) PLUS: new data-el="positive" class
//    (50 marks, sat-blue) + a reserved EMPTY <g id="layer-family-candidates"> between
//    layer-positives and layer-chrome — inert at this cutover (an islands-toggle charge
//    populates it later).
const EDITION4_DIR_REL = 'agentic_orchestration/galadriel/captures/2026-07-17-atlas-edition4-serving';
const E4_INSTRUMENT_REL = `${EDITION4_DIR_REL}/atlas-edition4-instrument.svg`;
const E4_ARCHIVE_REL = `${EDITION4_DIR_REL}/atlas-edition4-archive.svg`;
const E4_PROVENANCE_REL = `${EDITION4_DIR_REL}/render-provenance.json`;
const E4_INSTRUMENT_SRC = join(REPO_ROOT, E4_INSTRUMENT_REL);
const E4_ARCHIVE_SRC = join(REPO_ROOT, E4_ARCHIVE_REL);
const E4_PROVENANCE_SRC = join(REPO_ROOT, E4_PROVENANCE_REL);
const OUT_E4_INSTRUMENT = join(OUT_DIR, 'atlas-edition4-instrument.svg');
const OUT_E4_ARCHIVE = join(OUT_DIR, 'atlas-edition4-archive.svg');
const OUT_E4_PROVENANCE = join(OUT_DIR, 'render-provenance.json');

mkdirSync(OUT_DIR, { recursive: true });

// FAIL-LOUD: the two skins + provenance are the shipped payload of contract §7.8 /atlas;
// a missing artifact is a broken build, not a degrade.
for (const [rel, src] of [
  [E4_INSTRUMENT_REL, E4_INSTRUMENT_SRC],
  [E4_ARCHIVE_REL, E4_ARCHIVE_SRC],
  [E4_PROVENANCE_REL, E4_PROVENANCE_SRC],
]) {
  if (!existsSync(src)) {
    console.error(`[stage-assets] FAIL — Atlas Edition-IV artifact missing: ${rel}`);
    process.exit(1);
  }
}
// Serve the verified render UNMODIFIED (byte-copy). render-provenance.json carries the
// skin→canvas map (the page binds the black-copy lead by CANVAS, never by skin name) + the
// P-DF-1 verdict the provenance panel reads at runtime.
copyFileSync(E4_INSTRUMENT_SRC, OUT_E4_INSTRUMENT);
copyFileSync(E4_ARCHIVE_SRC, OUT_E4_ARCHIVE);
copyFileSync(E4_PROVENANCE_SRC, OUT_E4_PROVENANCE);

// Git-derived source commit for the render (never hand-typed). Prefer the commit that last
// touched the SVG; fall back to deploy HEAD / VERCEL SHA / honest 'unknown'.
function gitTry(cmd) {
  try {
    return execSync(cmd, { cwd: REPO_ROOT, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString()
      .trim();
  } catch {
    return '';
  }
}
const e4SourceCommit =
  gitTry(`git log -1 --format=%H -- "${E4_INSTRUMENT_REL}"`) ||
  gitTry('git rev-parse HEAD') ||
  process.env.VERCEL_GIT_COMMIT_SHA ||
  'unknown';
// A tiny staging stamp (audit only; the render's own render-provenance.json is authoritative).
writeFileSync(
  join(OUT_DIR, 'edition4-staging.json'),
  JSON.stringify(
    {
      title: 'Build Horizon — Edition IV',
      derivation: 'render(atlas-edition4.json)',
      skins: {
        instrument: '/atlas/atlas-edition4-instrument.svg',
        archive: '/atlas/atlas-edition4-archive.svg',
      },
      source_path_instrument: E4_INSTRUMENT_REL,
      source_path_archive: E4_ARCHIVE_REL,
      source_path_provenance: E4_PROVENANCE_REL,
      source_commit: e4SourceCommit,
      staged_at: new Date().toISOString(),
    },
    null,
    2
  ) + '\n'
);

// ── Build-time slim derivation (build-atlas-interactive.mjs) — the ~2MB client JSON from
//    the 7.5MB Edition-IV emission + corpus sidecars + the prior-edition atlas (Path-A
//    additive floor). FAIL-LOUD: a build-fail guard trip (missing/renamed emitted field,
//    stale sidecar, E3-carried drift) is a broken build, never a degrade.
const BUILDER = join(__dirname, 'atlas', 'build-atlas-interactive.mjs');
try {
  const out = execSync(`node "${BUILDER}"`, {
    cwd: join(REPO_ROOT, 'glance', 'app'),
    stdio: ['ignore', 'pipe', 'pipe'],
  }).toString();
  // Surface the builder's own receipt (kit/ghost counts, coverage, slim size).
  process.stdout.write(out);
} catch (err) {
  const msg = (err.stdout || '').toString() + (err.stderr || '').toString();
  console.error('[stage-assets] FAIL — atlas slim derivation (build-atlas-interactive.mjs):');
  console.error(msg || err.message);
  process.exit(1);
}

console.log(
  `[stage-assets] staged Atlas Edition-IV (instrument + archive + provenance) + slim JSON ` +
    `(source_commit ${e4SourceCommit.slice(0, 8)})`
);
