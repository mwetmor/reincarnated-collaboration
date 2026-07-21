// kits-contract.test.ts — the per-kit "single source of truth" interface contract.
//
// The MATT-APPROVED sample (2026-07-20-glance-per-kit-sample.json) is the FROZEN shape;
// elrond emits it at scale into public/kits/. These tests lock (1) the render-side helper
// functions and (2) that the STAGED corpus conforms to the 10-section contract drax renders
// — so a shape drift on the elrond side (added/renamed/removed field) trips a red test here
// before it reaches the page. node-env, no DOM (matches the atlas suite discipline).

import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import {
  DOSSIER_FAMILY_LABEL,
  DOSSIER_FAMILY_ORDER,
  displayGame,
  gradeTone,
  rowCountTotal,
  verdictTone,
  type DossierFamily,
  type KitDetail,
  type KitIndexRow,
} from '../data/kitTypes';

const KITS_DIR = join(__dirname, '..', '..', 'public', 'kits');
const hasStaged = existsSync(join(KITS_DIR, 'index.json'));

function readJson<T>(name: string): T {
  return JSON.parse(readFileSync(join(KITS_DIR, name), 'utf8')) as T;
}

// The 6 canonical dossier families (spec: "grouped by 6 families").
const SIX_FAMILIES: DossierFamily[] = [
  'author_credit',
  'capstone_alterations',
  'item_alterations',
  'skill_geometry',
  'skill_loop',
  'variants',
];

describe('kit helpers (pure, render-side)', () => {
  it('gradeTone returns a distinct static class per known grade + a neutral fallback', () => {
    const grades = ['EXACT', 'CLOSE', 'APPROX', 'GAPPED'];
    const classes = grades.map(gradeTone);
    // all non-empty, all distinct (each grade reads differently at a glance)
    expect(new Set(classes).size).toBe(grades.length);
    for (const c of classes) expect(c.length).toBeGreaterThan(0);
    // unknown/null grade falls back to a neutral slate chip (never crashes)
    expect(gradeTone(null)).toContain('slate');
    expect(gradeTone('WHATEVER')).toContain('slate');
  });

  it('verdictTone flags CONFIRMED/CONTRADICTED/UNSUPPORTED distinctly', () => {
    expect(verdictTone('CONFIRMED')).toContain('emerald');
    expect(verdictTone('CONTRADICTED')).toContain('rose');
    expect(verdictTone('UNSUPPORTED')).toContain('amber');
    expect(verdictTone('SOMETHING_ELSE')).toContain('slate');
  });

  it('displayGame title-cases slugs for display without mutating meaning; null → em dash', () => {
    // very short tokens (≤3) upper-case (gd/di/le/la read as initialisms); longer tokens
    // title-case. Display-only — the underlying slug is never mutated.
    expect(displayGame('gd')).toBe('GD');
    expect(displayGame('poe2')).toBe('Poe2'); // 4-char token → title-case
    expect(displayGame('chronicon')).toBe('Chronicon');
    expect(displayGame('grim-dawn')).toBe('Grim Dawn'); // hyphen split, per-token rule
    expect(displayGame(null)).toBe('—');
  });

  it('rowCountTotal sums the five density counts', () => {
    expect(
      rowCountTotal({ citations: 2, dossier_facts: 6, verify_claims: 3, mints_anchored: 1, dockets: 0 }),
    ).toBe(12);
  });

  it('the dossier family render-order + labels cover exactly the 6 canonical families', () => {
    expect(new Set(DOSSIER_FAMILY_ORDER)).toEqual(new Set(SIX_FAMILIES));
    for (const f of SIX_FAMILIES) {
      expect(DOSSIER_FAMILY_LABEL[f]).toBeTruthy();
    }
  });
});

// The staged-corpus conformance suite only runs when public/kits/ is present (it is, after
// `pretest` runs stage-kits). Skips cleanly in an unstaged checkout rather than false-failing.
describe.skipIf(!hasStaged)('staged corpus conforms to the frozen 10-section contract', () => {
  const index = readJson<KitIndexRow[]>('index.json');

  it('index.json is a non-empty array of thin rows with the contract fields', () => {
    expect(Array.isArray(index)).toBe(true);
    expect(index.length).toBeGreaterThan(0);
    for (const r of index.slice(0, 50)) {
      expect(typeof r.kit_id).toBe('string');
      // folk_name/game/tier/grade are nullable but the KEYS must be present-or-absent
      // (never a wrong type); _row_counts is required with five numeric fields.
      expect(r._row_counts).toBeTruthy();
      for (const k of ['citations', 'dossier_facts', 'verify_claims', 'mints_anchored', 'dockets'] as const) {
        expect(typeof r._row_counts[k]).toBe('number');
      }
    }
  });

  it('every per-kit file carries all 10 sections with the contract-legal types', () => {
    // sample a spread across the corpus (first 40) to keep the suite fast but representative.
    for (const row of index.slice(0, 40)) {
      const k = readJson<KitDetail>(`${row.kit_id}.json`);
      expect(k.kit_id).toBe(row.kit_id);

      // 1 spine — required object; elements/ailments normalized to arrays
      expect(k.spine).toBeTruthy();
      expect(Array.isArray(k.spine.elements_attested)).toBe(true);
      expect(Array.isArray(k.spine.ailments_attested)).toBe(true);

      // 2 mapping — object OR null (both legal)
      expect(k.mapping === null || typeof k.mapping === 'object').toBe(true);

      // 3 mints_anchored / 4 dockets / 7 citations / 8 verify_ledger — always arrays
      for (const arrKey of ['mints_anchored', 'dockets', 'citations', 'verify_ledger'] as const) {
        expect(Array.isArray(k[arrKey])).toBe(true);
      }

      // 5 atlas_group / 6 lineage_enrichment — object OR null
      expect(k.atlas_group === null || typeof k.atlas_group === 'object').toBe(true);
      expect(k.lineage_enrichment === null || typeof k.lineage_enrichment === 'object').toBe(true);

      // 9 dossier — a keyed object; every present family value is an array; every key is
      // one of the 6 canonical families (a NEW family would be a shape change → re-sync).
      expect(k.dossier && typeof k.dossier === 'object').toBe(true);
      for (const [fam, rows] of Object.entries(k.dossier)) {
        expect(SIX_FAMILIES).toContain(fam as DossierFamily);
        expect(Array.isArray(rows)).toBe(true);
        for (const dr of rows ?? []) {
          // abstained rows are legal + common (source silent); abstained is 0|1
          expect(dr.abstained === 0 || dr.abstained === 1).toBe(true);
        }
      }

      // 10 _row_counts — five numbers
      for (const ck of ['citations', 'dossier_facts', 'verify_claims', 'mints_anchored', 'dockets'] as const) {
        expect(typeof k._row_counts[ck]).toBe('number');
      }

      // citations quarantined flag is 0|1 (the visual-flag discriminator)
      for (const c of k.citations) {
        expect(c.quarantined === 0 || c.quarantined === 1).toBe(true);
      }
    }
  });

  it('the diagnostic gaps the page must render honestly are actually PRESENT in the corpus', () => {
    // This page is also a diagnostic: prove the empty/null/flagged states exist so the
    // graceful-render paths are exercised by real data (not hypothetical).
    let emptyMints = 0;
    let nullAtlas = 0;
    let nullLineage = 0;
    let quarantined = 0;
    let abstainedRows = 0;
    for (const row of index) {
      const k = readJson<KitDetail>(`${row.kit_id}.json`);
      if (k.mints_anchored.length === 0) emptyMints++;
      if (k.atlas_group === null) nullAtlas++;
      if (k.lineage_enrichment === null) nullLineage++;
      if (k.citations.some((c) => c.quarantined === 1)) quarantined++;
      for (const rows of Object.values(k.dossier)) {
        for (const dr of rows ?? []) if (dr.abstained === 1) abstainedRows++;
      }
    }
    // every honest-gap render path has real corpus coverage
    expect(emptyMints).toBeGreaterThan(0);
    expect(nullAtlas).toBeGreaterThan(0);
    expect(nullLineage).toBeGreaterThan(0); // corpus kits: none placed in roster_atlas (expected)
    expect(quarantined).toBeGreaterThan(0);
    expect(abstainedRows).toBeGreaterThan(0);
  });
});
