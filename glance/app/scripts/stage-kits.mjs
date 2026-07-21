#!/usr/bin/env node
/**
 * Glance per-kit "single source of truth" staging — DERIVED static assets → public/kits/.
 *
 * SAME PATTERN AS stage-assets.mjs (the /atlas staging): a build-time step that
 * provisions DB-DERIVED static artifacts into public/ (gitignored) before vite build.
 * The DB is read at GENERATE-time only (by elrond's corpus→JSON generator), never from
 * the browser — glance's founding law (no DB / no server / no LLM in the live truth path).
 *
 * OUTPUT (contract-frozen shape, spec: 2026-07-20-glance-per-kit-join-spec.md):
 *   public/kits/index.json        — thin browse/filter list: one row per kit
 *                                    (kit_id, folk_name, game, tier, grade, _row_counts)
 *   public/kits/<kit_id>.json      — the full per-kit object (the 10 sections)
 *   public/kits/kits-provenance.json — git-derived source stamp (never hand-typed)
 *
 * ── SOURCE SEAM (elrond ↔ drax) ─────────────────────────────────────────────────────
 * The AUTHORITATIVE source is elrond's productionized generator emitting all 574 kits.
 * Until that lands, this step stages the MATT-APPROVED 5-kit sample (the FROZEN interface
 * contract) so drax's render can be built + self-reviewed against it. The two are
 * interchangeable because the sample IS the contract: elrond emits exactly this shape.
 *
 * TODO(drax): when elrond ships the full-corpus generator, point KITS_SOURCE at its
 * emitted `index.json` + per-kit dir (or invoke it here like stage-assets.mjs invokes
 * build-atlas-interactive.mjs) and drop the sample-split branch. Tracked in AGENT_STATE.md.
 * ────────────────────────────────────────────────────────────────────────────────────
 *
 * Founding law honored: DERIVED not authored · no LLM in the truth path · no hand-drawn
 * state. The provenance stamp (source commit) is git-derived, not hand-typed.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
// glance/app/scripts → repo root is three levels up.
const REPO_ROOT = resolve(__dirname, '..', '..', '..');
const OUT_DIR = join(REPO_ROOT, 'glance', 'app', 'public', 'kits');

// The MATT-APPROVED, FROZEN 5-kit sample (the interface contract). SOURCE SEAM: replaced
// by elrond's full-corpus emission when it lands (see header TODO).
const SAMPLE_REL = 'agentic_orchestration/gandalf/notes/2026-07-20-glance-per-kit-sample.json';
const SAMPLE_SRC = join(REPO_ROOT, SAMPLE_REL);

// If elrond's full-corpus output is present (a pre-split index.json + per-kit dir under
// this committed path), prefer it. Absent for now — the sample is the source of truth.
// This path mirrors the one the app .gitignore already anticipates for public/kits/'s
// upstream (kits-export/). TODO(drax): confirm exact path + filename convention with
// elrond's report before finalizing; re-sync if the emission lands elsewhere.
const FULL_INDEX_REL = 'agentic_orchestration/research/curated/kits-export/index.json';
const FULL_INDEX_SRC = join(REPO_ROOT, FULL_INDEX_REL);

// WIPE first so ONE served truth remains (no stale per-kit files from a prior corpus
// snapshot linger). The dir is gitignored + fully regenerated below, so a clean wipe is safe.
rmSync(OUT_DIR, { recursive: true, force: true });
mkdirSync(OUT_DIR, { recursive: true });

// Git-derived source commit (never hand-typed). Prefer the commit that last touched the
// source; fall back to deploy HEAD / VERCEL SHA / honest 'unknown'.
function gitTry(cmd) {
  try {
    return execSync(cmd, { cwd: REPO_ROOT, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString()
      .trim();
  } catch {
    return '';
  }
}

/** Thin index row for the browse/filter list — the spine header fields + density counts. */
function indexRow(kit) {
  const s = kit.spine ?? {};
  return {
    kit_id: kit.kit_id,
    folk_name: s.folk_name ?? null,
    game: s.game ?? null,
    tier: s.tier ?? null,
    grade: s.grade ?? null,
    terminal_state: s.terminal_state ?? null,
    _row_counts: kit._row_counts ?? {
      citations: 0, dossier_facts: 0, verify_claims: 0, mints_anchored: 0, dockets: 0,
    },
  };
}

let sourceMode;
let sourceRel;
let kits;

if (existsSync(FULL_INDEX_SRC)) {
  // ── FULL CORPUS (elrond) — a pre-split index + per-kit files already exist upstream.
  //    Byte-copy them through (they are the authoritative emission). We still re-derive
  //    kits-provenance from git so the stamp is honest to THIS build.
  sourceMode = 'full-corpus';
  sourceRel = FULL_INDEX_REL;
  const FULL_DIR = dirname(FULL_INDEX_SRC);
  const index = JSON.parse(readFileSync(FULL_INDEX_SRC, 'utf8'));
  writeFileSync(join(OUT_DIR, 'index.json'), JSON.stringify(index, null, 2) + '\n');
  let copied = 0;
  for (const row of index) {
    const perKitSrc = join(FULL_DIR, `${row.kit_id}.json`);
    if (!existsSync(perKitSrc)) {
      console.error(`[stage-kits] FAIL — per-kit file missing for ${row.kit_id}: ${perKitSrc}`);
      process.exit(1);
    }
    writeFileSync(join(OUT_DIR, `${row.kit_id}.json`), readFileSync(perKitSrc, 'utf8'));
    copied += 1;
  }
  kits = index;
  console.log(`[stage-kits] staged FULL corpus — ${copied} per-kit files + index.json`);
} else {
  // ── SAMPLE (frozen contract) — split the 5-kit array into index + per-kit files.
  sourceMode = 'sample-5kit';
  sourceRel = SAMPLE_REL;
  if (!existsSync(SAMPLE_SRC)) {
    console.error(`[stage-kits] FAIL — sample source missing: ${SAMPLE_REL}`);
    process.exit(1);
  }
  const sample = JSON.parse(readFileSync(SAMPLE_SRC, 'utf8'));
  if (!Array.isArray(sample) || sample.length === 0) {
    console.error('[stage-kits] FAIL — sample is not a non-empty array.');
    process.exit(1);
  }
  const index = sample.map(indexRow);
  writeFileSync(join(OUT_DIR, 'index.json'), JSON.stringify(index, null, 2) + '\n');
  for (const kit of sample) {
    writeFileSync(join(OUT_DIR, `${kit.kit_id}.json`), JSON.stringify(kit, null, 2) + '\n');
  }
  kits = index;
  console.log(`[stage-kits] staged SAMPLE — ${sample.length} per-kit files + index.json`);
}

const sourceCommit =
  gitTry(`git log -1 --format=%H -- "${sourceRel}"`) ||
  gitTry('git rev-parse HEAD') ||
  process.env.VERCEL_GIT_COMMIT_SHA ||
  'unknown';

writeFileSync(
  join(OUT_DIR, 'kits-provenance.json'),
  JSON.stringify(
    {
      title: 'Per-kit single source of truth',
      derivation: 'project(corpus.db) — every corpus row for one kit',
      source_mode: sourceMode,
      source_path: sourceRel,
      source_commit: sourceCommit,
      kit_count: kits.length,
      staged_at: new Date().toISOString(),
      // honest note when serving the sample: this is NOT the full 574-kit corpus yet.
      note:
        sourceMode === 'sample-5kit'
          ? 'SAMPLE (5 kits) — the frozen interface contract. Full corpus lands via elrond.'
          : 'Full corpus emission (elrond).',
    },
    null,
    2
  ) + '\n'
);

console.log(
  `[stage-kits] wrote kits-provenance.json (mode ${sourceMode}, source_commit ${sourceCommit.slice(0, 8)})`
);
