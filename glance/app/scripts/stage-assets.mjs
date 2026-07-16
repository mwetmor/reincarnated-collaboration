#!/usr/bin/env node
/**
 * Glance asset-staging — DERIVED static assets → public/ before vite build.
 *
 * KEPT SEPARATE FROM THE PARSER ON PURPOSE. The parser (glance/parser/parse.mjs)
 * has a closed charter: it reads canonical/** + the two Matt queues and emits the
 * state.json truth model — no LLM, no judgment, no side assets. This step provisions
 * DB-DERIVED static artifacts that are NOT part of the state-model truth path.
 *
 * v1.12 RE-HOME (drax, Matt-ruled 2026-07-16 · contract §7.8): the interactive
 * Build-Horizon instrument re-homed from reincarnated-loadout into glance/app and is now
 * the /atlas page lead at EDITION III. This step:
 *   (1) stages the two verified Edition-III render SVGs (instrument + archive, served
 *       UNMODIFIED — byte-copy, never hand-edited/scraped) + render-provenance.json from
 *       galadriel's VERIFY-ACCEPTED capture into public/atlas/;
 *   (2) runs the build-time slim derivation (build-atlas-interactive.mjs) which reads the
 *       in-repo 7.5MB Edition-III emission (BUILD INPUT ONLY, never client-shipped) +
 *       the corpus provenance/engine-key sidecars and writes public/atlas/atlas-
 *       interactive.json (~2MB) with its build-fail guard intact.
 *
 * The v1.11 static Edition-I plate + RULED-V1.2 plane-view staging RETIRED with the
 * static lead they fed (git keeps the lineage). public/atlas/ is gitignored — every
 * artifact here is a regenerated build output, single source of truth stays upstream.
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

// v1.12: WIPE the staged atlas dir first so ONE served truth remains (the retired v1.11
// Edition-I plates + RULED-V1.2 plane-view artifacts don't linger and bloat dist). The dir
// is gitignored + fully regenerated below, so a clean wipe is safe.
rmSync(OUT_DIR, { recursive: true, force: true });

// ── Atlas Edition-III (the Matt-ruled re-home render) — the interactive instrument's
//    vendored plates. VENDORED from galadriel's VERIFY-ACCEPTED capture (gandalf brief
//    2026-07-16-galadriel-edition3-render-brief.md). Served UNMODIFIED (byte-copy); we
//    NEVER hand-edit them and NEVER scrape values out of them — the page reads its numbers
//    from the slim atlas-interactive.json (built below) + render-provenance.json.
//    Two verified deterministic skins: instrument (light) + archive (dark, black-copy lead).
const EDITION3_DIR_REL = 'agentic_orchestration/galadriel/captures/2026-07-16-atlas-edition3';
const E3_INSTRUMENT_REL = `${EDITION3_DIR_REL}/atlas-edition3-instrument.svg`;
const E3_ARCHIVE_REL = `${EDITION3_DIR_REL}/atlas-edition3-archive.svg`;
const E3_PROVENANCE_REL = `${EDITION3_DIR_REL}/render-provenance.json`;
const E3_INSTRUMENT_SRC = join(REPO_ROOT, E3_INSTRUMENT_REL);
const E3_ARCHIVE_SRC = join(REPO_ROOT, E3_ARCHIVE_REL);
const E3_PROVENANCE_SRC = join(REPO_ROOT, E3_PROVENANCE_REL);
const OUT_E3_INSTRUMENT = join(OUT_DIR, 'atlas-edition3-instrument.svg');
const OUT_E3_ARCHIVE = join(OUT_DIR, 'atlas-edition3-archive.svg');
const OUT_E3_PROVENANCE = join(OUT_DIR, 'render-provenance.json');

mkdirSync(OUT_DIR, { recursive: true });

// FAIL-LOUD: the two skins + provenance are the shipped payload of contract §7.8 /atlas;
// a missing artifact is a broken build, not a degrade.
for (const [rel, src] of [
  [E3_INSTRUMENT_REL, E3_INSTRUMENT_SRC],
  [E3_ARCHIVE_REL, E3_ARCHIVE_SRC],
  [E3_PROVENANCE_REL, E3_PROVENANCE_SRC],
]) {
  if (!existsSync(src)) {
    console.error(`[stage-assets] FAIL — Atlas Edition-III artifact missing: ${rel}`);
    process.exit(1);
  }
}
// Serve the verified render UNMODIFIED (byte-copy). render-provenance.json carries the
// skin→canvas map (the page binds the black-copy lead by CANVAS, never by skin name) + the
// P-DF-1 verdict the provenance panel reads at runtime.
copyFileSync(E3_INSTRUMENT_SRC, OUT_E3_INSTRUMENT);
copyFileSync(E3_ARCHIVE_SRC, OUT_E3_ARCHIVE);
copyFileSync(E3_PROVENANCE_SRC, OUT_E3_PROVENANCE);

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
const e3SourceCommit =
  gitTry(`git log -1 --format=%H -- "${E3_INSTRUMENT_REL}"`) ||
  gitTry('git rev-parse HEAD') ||
  process.env.VERCEL_GIT_COMMIT_SHA ||
  'unknown';
// A tiny staging stamp (audit only; the render's own render-provenance.json is authoritative).
writeFileSync(
  join(OUT_DIR, 'edition3-staging.json'),
  JSON.stringify(
    {
      title: 'Build Horizon — Edition III',
      derivation: 'render(atlas-edition3.json)',
      skins: {
        instrument: '/atlas/atlas-edition3-instrument.svg',
        archive: '/atlas/atlas-edition3-archive.svg',
      },
      source_path_instrument: E3_INSTRUMENT_REL,
      source_path_archive: E3_ARCHIVE_REL,
      source_path_provenance: E3_PROVENANCE_REL,
      source_commit: e3SourceCommit,
      staged_at: new Date().toISOString(),
    },
    null,
    2
  ) + '\n'
);

// ── Build-time slim derivation (build-atlas-interactive.mjs) — the ~2MB client JSON from
//    the 7.5MB Edition-III emission + corpus sidecars. FAIL-LOUD: a build-fail guard trip
//    (missing/renamed emitted field, stale sidecar) is a broken build, never a degrade.
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
  `[stage-assets] staged Atlas Edition-III (instrument + archive + provenance) + slim JSON ` +
    `(source_commit ${e3SourceCommit.slice(0, 8)})`
);
