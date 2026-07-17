#!/usr/bin/env node
// export-kit-provenance-sidecar.mjs
// D1-h: repeatable READ-ONLY re-export of the kit-provenance sidecar from corpus.db
// `canon_corpus`, joined by kit_id into the atlas build at slim time.
//
// v1.13 CUTOVER (drax, Matt-ruled 2026-07-17): the D1-h sidecar was originally a
// ONE-SHOT export (query documented in its `__provenance__` stanza). The Edition-IV
// serving cutover needs a REPEATABLE twin (the corpus has since had 182 rows hard-
// deleted, 56 curated LA rows re-admitted, and ruling-17 folk_name metadata), so
// this script mirrors the engine-key exporter's shape (same-dir, sqlite3 CLI,
// __provenance__ stanza with self-documenting query + export_date + row_count).
// The query itself is UNCHANGED from the one-shot (SELECT kit_id, folk_name, game,
// era_year, stabilization_patch FROM canon_corpus) so the sidecar SCHEMA + tests
// stay byte-compatible; only the row-set refreshes to current DB truth.
//
// READ-ONLY: corpus.db is never written. Uses the `sqlite3` CLI (no node sqlite dep).
//
// Run: node scripts/atlas/export-kit-provenance-sidecar.mjs
//   Emits scripts/atlas/kit-provenance-sidecar.json (overwrite)
// Spec: agentic_orchestration/gandalf/notes/2026-07-15-atlas-interactive-glance-spec.md §9 D1-h

import { execFileSync } from 'node:child_process';
import { writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const DB = resolve(
  '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db'
);
const OUT = resolve(__dirname, 'kit-provenance-sidecar.json');

// The one-shot query — carried VERBATIM so the sidecar SHAPE (and every test/assertion
// that greps for it in __provenance__.query) stays byte-compatible.
const QUERY = 'SELECT kit_id, folk_name, game, era_year, stabilization_patch FROM canon_corpus;';

function sqliteJson(query) {
  const out = execFileSync('sqlite3', ['-readonly', DB, '-json', query], {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
  });
  const t = out.trim();
  return t === '' ? [] : JSON.parse(t);
}

function main() {
  if (!existsSync(DB)) {
    console.error(`EXPORT-FAIL: corpus.db not found at ${DB} (READ-ONLY source).`);
    process.exit(2);
  }

  const rows = sqliteJson(QUERY);

  // sqlite3 -json emits null-column values as JS null already; keep the rows verbatim
  // (kit_id, folk_name, game, era_year, stabilization_patch). No massaging.

  const out = {
    __provenance__: {
      source_db: DB,
      query: QUERY,
      export_date: new Date().toISOString(),
      row_count: rows.length,
      note:
        'READ-ONLY sidecar exported from canon_corpus for the atlas Build Horizon ' +
        'provenance-name join (D1-h). Every displayed build name/year/patch traces to a ' +
        'row here; missing fields render nothing (zero invention). v1.13 (E4 cutover): the ' +
        'query is UNCHANGED from the one-shot, but this export is REPEATABLE — the row-set ' +
        'refreshes to current DB truth (post 182 hard-deletes + 56 LA re-admissions + ' +
        'ruling-17 folk_name metadata).',
    },
    rows,
  };

  writeFileSync(OUT, JSON.stringify(out, null, 0));

  console.log('kit-provenance-sidecar.json exported:');
  console.log(`  source : ${DB} (READ-ONLY)`);
  console.log(`  out    : ${OUT}`);
  console.log(`  rows   : ${rows.length}`);
  const withFolk = rows.filter((r) => r.folk_name != null && r.folk_name !== '').length;
  console.log(`  folk_name non-null : ${withFolk}/${rows.length}`);
}

main();
