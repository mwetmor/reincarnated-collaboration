// atlas-filters.test.ts — the D3-a filter engine (spec §9.3, acceptance #54/#55).
//
// D3 (spec §9.3, Matt 2026-07-15): pivot grouping + lens interaction retired —
// pivots→filters, zoom→fixed S_max. This SUPERSEDES the pivot-grouping conformance
// suite (atlas-pivot.test.ts, DELETED) with the filter model that replaced it:
//   - makeFilterPredicate: AND composition across the five controls, incl. the
//     NON-APPLICABLE-FAILS law (Liveness=Graveyard ⇒ ghosts drop; Family ⇒ ghosts +
//     graveyard drop; Family=Single ⇒ live kit with condensation null).
//   - familyOptions: family entries ENUMERATED FROM THE DATA (distinct emitted
//     condensations among live kits, sorted) — never a hand-typed list.
//   - countShown: the live result readout (builds shown · ghost cells shown).
//   - builds-then-ghosts emitted order is preserved by a linear filter pass.
// Expected Ns are HAND-COUNTED against a fixture that mirrors the atlas ratios.

import { describe, it, expect } from 'vitest';
import {
  makeFilterPredicate,
  familyOptions,
  gameOptions,
  countShown,
  filtersAreDefault,
  DEFAULT_FILTERS,
  type PivotItem,
  type AtlasFilterState,
} from '../utils/atlasPivot';
import type { AtlasKitRow, AtlasGhostRow, AtlasInteractiveData } from '../data/atlasTypes';

function kit(partial: Partial<AtlasKitRow>): AtlasKitRow {
  return {
    kit_id: 'k',
    cls: 'live',
    condensation: null,
    death_class: null,
    x: 1,
    y: 1,
    quadrant: 'EN',
    folk_name: null,
    game: null,
    era_year: null,
    stabilization_patch: null,
    engine_key: null,
    ...partial,
  } as AtlasKitRow;
}
function ghost(partial: Partial<AtlasGhostRow>): AtlasGhostRow {
  return {
    core: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    depth: 1,
    lit: false,
    kit_count: 0,
    x: 1,
    y: 1,
    quadrant: 'EN',
    ...partial,
  } as AtlasGhostRow;
}

/**
 * A hand-countable fixture (mirrors the atlas kinds). Positions:
 *   - live single  EN (x+ y+)              [PERFORM·E / LAUNCH·N]
 *   - live WHIRLWIND WS (x- y-)            [DEPLOY·W / EMBODY·S]
 *   - live AURA      EN (x+ y+)
 *   - graveyard      ES (x+ y-)            [PERFORM·E / EMBODY·S]
 *   - ghost          EN (x+ y+)
 *   - ghost          WN (x- y+)
 *   - ghost          WS (x- y-)
 */
// D7-b: `game` slugs added so the SOURCE GAME predicate + gameOptions are covered.
// d2 carries TWO live kits (single + aura) so a game filter can keep >1; poe1 is a
// single live kit; d3 is carried by the GRAVEYARD kit ONLY — proving SOURCE GAME binds
// live AND graveyard (it is NOT live-only like Family).
const KITS: AtlasKitRow[] = [
  kit({ kit_id: 'live-single-EN', cls: 'live', condensation: null, x: 5, y: 5, game: 'd2' }),
  kit({ kit_id: 'live-whirl-WS', cls: 'live', condensation: 'WHIRLWIND', x: -3, y: -2, game: 'poe1' }),
  kit({ kit_id: 'live-aura-EN', cls: 'live', condensation: 'AURA', x: 4, y: 6, game: 'd2' }),
  kit({ kit_id: 'grave-ES', cls: 'graveyard', death_class: 'intrinsic-red', x: 2, y: -7, game: 'd3' }),
];
const GHOSTS: AtlasGhostRow[] = [
  ghost({ x: 1, y: 1 }), // EN
  ghost({ x: -1, y: 1, core: ['H', 'I', 'J', 'K', 'L', 'M', 'N'] }), // WN
  ghost({ x: -1, y: -1, core: ['O', 'P', 'Q', 'R', 'S', 'T', 'U'] }), // WS
];
// Root order: builds first, then ghosts (as the page composes it).
const ROOT: PivotItem[] = [
  ...KITS.map((row) => ({ kind: 'kit', row }) as PivotItem),
  ...GHOSTS.map((row) => ({ kind: 'ghost', row }) as PivotItem),
];

function apply(f: AtlasFilterState): PivotItem[] {
  return ROOT.filter(makeFilterPredicate(f));
}

describe('D3-a filter engine — defaults (spec §9.3)', () => {
  it('DEFAULT_FILTERS is all-pass; filtersAreDefault true', () => {
    expect(filtersAreDefault(DEFAULT_FILTERS)).toBe(true);
    expect(apply(DEFAULT_FILTERS)).toHaveLength(ROOT.length); // 4 builds + 3 ghosts = 7
    const c = countShown(apply(DEFAULT_FILTERS));
    expect(c).toEqual({ builds: 4, ghosts: 3 });
  });

  it('any non-All setting makes filtersAreDefault false', () => {
    expect(filtersAreDefault({ ...DEFAULT_FILTERS, entity: 'ghosts' })).toBe(false);
    expect(filtersAreDefault({ ...DEFAULT_FILTERS, family: 'AURA' })).toBe(false);
  });
});

describe('D3-a filter engine — single-control predicates (hand-counted)', () => {
  it('Axis-X=PERFORM·E (x>=0): 3 builds (single,aura,grave) + 1 ghost(EN) = 4', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisX: 'east' });
    expect(countShown(r)).toEqual({ builds: 3, ghosts: 1 });
  });
  it('Axis-X=DEPLOY·W (x<0): 1 build(whirl) + 2 ghosts(WN,WS) = 3', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisX: 'west' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 2 });
  });
  it('Axis-Y=LAUNCH·N (y>=0): 2 builds(single,aura) + 2 ghosts(EN,WN) = 4', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisY: 'north' });
    expect(countShown(r)).toEqual({ builds: 2, ghosts: 2 });
  });
  it('Axis-Y=EMBODY·S (y<0): 2 builds(whirl,grave) + 1 ghost(WS) = 3', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisY: 'south' });
    expect(countShown(r)).toEqual({ builds: 2, ghosts: 1 });
  });
  it('Entity=Builds: all 4 builds, 0 ghosts', () => {
    expect(countShown(apply({ ...DEFAULT_FILTERS, entity: 'builds' }))).toEqual({
      builds: 4,
      ghosts: 0,
    });
  });
  it('Entity=Ghosts: 0 builds, all 3 ghosts', () => {
    expect(countShown(apply({ ...DEFAULT_FILTERS, entity: 'ghosts' }))).toEqual({
      builds: 0,
      ghosts: 3,
    });
  });
});

describe('D3-a NON-APPLICABLE-FAILS composition law (spec §9.3)', () => {
  it('Liveness=Graveyard ⇒ ghosts DROP (no liveness) — 1 build, 0 ghosts', () => {
    const r = apply({ ...DEFAULT_FILTERS, liveness: 'graveyard' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r.every((it) => it.kind === 'kit')).toBe(true);
  });
  it('Liveness=Live Builds ⇒ ghosts DROP — 3 live builds, 0 ghosts', () => {
    const r = apply({ ...DEFAULT_FILTERS, liveness: 'live' });
    expect(countShown(r)).toEqual({ builds: 3, ghosts: 0 });
  });
  it('Family=WHIRLWIND ⇒ ghosts + graveyard DROP — exactly the 1 live whirl build', () => {
    const r = apply({ ...DEFAULT_FILTERS, family: 'WHIRLWIND' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('live-whirl-WS');
  });
  it('Family=Single ⇒ live kits with condensation null only (1); ghosts + families drop', () => {
    const r = apply({ ...DEFAULT_FILTERS, family: 'single' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('live-single-EN');
  });
});

describe('D7-b SOURCE GAME predicate — matches by slug, kits only (spec §D7-b)', () => {
  it('game=d2 ⇒ the 2 d2 builds (single + aura), 0 ghosts (ghosts have no game)', () => {
    const r = apply({ ...DEFAULT_FILTERS, game: 'd2' });
    expect(countShown(r)).toEqual({ builds: 2, ghosts: 0 });
    const ids = r.map((it) => (it as { row: AtlasKitRow }).row.kit_id);
    expect(ids).toEqual(['live-single-EN', 'live-aura-EN']);
  });
  it('game=poe1 ⇒ exactly the 1 poe1 build (whirl)', () => {
    const r = apply({ ...DEFAULT_FILTERS, game: 'poe1' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('live-whirl-WS');
  });
  it('game binds GRAVEYARD too (NOT live-only like Family): game=d3 ⇒ the 1 graveyard kit', () => {
    const r = apply({ ...DEFAULT_FILTERS, game: 'd3' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('grave-ES');
  });
  it('a game with no rows ⇒ zero results (honest empty)', () => {
    expect(apply({ ...DEFAULT_FILTERS, game: 'nonexistent-slug' })).toHaveLength(0);
  });
  it('INERT with ENTITY=Ghosts: any non-All game drops ALL ghosts (they carry no game)', () => {
    // Every non-All game setting fails ghosts; combined with Entity=Ghosts → empty.
    for (const g of ['d2', 'poe1', 'd3']) {
      const r = apply({ ...DEFAULT_FILTERS, entity: 'ghosts', game: g });
      expect(r).toHaveLength(0);
    }
    // And game='all' + Entity=Ghosts is the ordinary all-ghosts case (slicer inert).
    expect(countShown(apply({ ...DEFAULT_FILTERS, entity: 'ghosts', game: 'all' }))).toEqual({
      builds: 0,
      ghosts: 3,
    });
  });
  it('composes AND with other controls: game=d2 AND Axis-Y=LAUNCH·N ⇒ both d2 builds (both north)', () => {
    expect(countShown(apply({ ...DEFAULT_FILTERS, game: 'd2', axisY: 'north' }))).toEqual({
      builds: 2,
      ghosts: 0,
    });
    // game=d2 AND Family=AURA ⇒ only the aura d2 build (single is d2 but not AURA).
    const r = apply({ ...DEFAULT_FILTERS, game: 'd2', family: 'AURA' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('live-aura-EN');
    // game=poe1 AND Axis-Y=LAUNCH·N ⇒ 0 (the poe1 whirl build is south).
    expect(apply({ ...DEFAULT_FILTERS, game: 'poe1', axisY: 'north' })).toHaveLength(0);
  });
  it('any non-All game makes filtersAreDefault false', () => {
    expect(filtersAreDefault({ ...DEFAULT_FILTERS, game: 'd2' })).toBe(false);
    expect(filtersAreDefault({ ...DEFAULT_FILTERS, game: 'all' })).toBe(true);
  });
});

describe('D3-a AND composition — combined-filter spot checks (hand-counted)', () => {
  it('Axis-X=PERFORM·E AND Entity=Builds: single,aura,grave (x>=0 builds) = 3', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisX: 'east', entity: 'builds' });
    expect(countShown(r)).toEqual({ builds: 3, ghosts: 0 });
  });
  it('Axis-Y=EMBODY·S AND Liveness=Live Builds: only the whirl build (grave is y- too but not live) = 1', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisY: 'south', liveness: 'live' });
    expect(countShown(r)).toEqual({ builds: 1, ghosts: 0 });
    expect(r[0].kind === 'kit' && r[0].row.kit_id).toBe('live-whirl-WS');
  });
  it('Axis-X=DEPLOY·W AND Entity=Ghosts: WN + WS ghosts = 2', () => {
    const r = apply({ ...DEFAULT_FILTERS, axisX: 'west', entity: 'ghosts' });
    expect(countShown(r)).toEqual({ builds: 0, ghosts: 2 });
  });
  it('Family=AURA AND Axis-Y=LAUNCH·N: the one AURA build (EN) = 1; AURA AND EMBODY·S = 0', () => {
    expect(countShown(apply({ ...DEFAULT_FILTERS, family: 'AURA', axisY: 'north' }))).toEqual({
      builds: 1,
      ghosts: 0,
    });
    // ZERO-RESULT combination (AURA build is north, not south).
    expect(apply({ ...DEFAULT_FILTERS, family: 'AURA', axisY: 'south' })).toHaveLength(0);
  });
});

describe('D3-a familyOptions — enumerated from the data (spec §9.3)', () => {
  it('distinct emitted condensations among LIVE kits, sorted; graveyard/single excluded', () => {
    const data = { kits: KITS } as unknown as AtlasInteractiveData;
    // Live families: WHIRLWIND, AURA (single is null; grave has no live family).
    expect(familyOptions(data)).toEqual(['AURA', 'WHIRLWIND']);
  });

  it('a graveyard-only condensation is NOT offered (only LIVE families count)', () => {
    const data = {
      kits: [kit({ cls: 'graveyard', condensation: 'DEAD-FAM', death_class: 'x' })],
    } as unknown as AtlasInteractiveData;
    expect(familyOptions(data)).toEqual([]);
  });
});

describe('D7-b gameOptions — enumerated from data, display via displayGame, sorted (spec §D7-b)', () => {
  it('distinct game slugs (live + graveyard), display names + counts, sorted by display', () => {
    const data = { kits: KITS } as unknown as AtlasInteractiveData;
    // Slugs present: d2 (x2: single+aura), poe1 (x1), d3 (x1, graveyard). Display names via
    // displayGame (first-char upper): D2, D3, Poe1. Sorted by display: D2, D3, Poe1.
    expect(gameOptions(data)).toEqual([
      { slug: 'd2', display: 'D2', count: 2 },
      { slug: 'd3', display: 'D3', count: 1 },
      { slug: 'poe1', display: 'Poe1', count: 1 },
    ]);
  });

  it('a null/empty game is skipped (no invented slug)', () => {
    const data = {
      kits: [kit({ game: null }), kit({ game: '' }), kit({ game: 'gd' })],
    } as unknown as AtlasInteractiveData;
    expect(gameOptions(data)).toEqual([{ slug: 'gd', display: 'Gd', count: 1 }]);
  });

  it('display names come from the SAME formatter the leaf rows use (no second mapping)', () => {
    // gameOptions must NOT fabricate 'poe1'->'Path of Exile'; it title-cases only, exactly
    // like buildProvenanceName's game tail. This guards against a divergent second mapping.
    const data = { kits: [kit({ game: 'poe1' })] } as unknown as AtlasInteractiveData;
    expect(gameOptions(data)[0].display).toBe('Poe1');
  });
});

describe('D3-a builds-then-ghosts order preserved by the filter pass', () => {
  it('a filter that keeps both kinds keeps all builds before all ghosts', () => {
    // Axis-Y=north keeps single+aura (builds) then EN+WN (ghosts).
    const r = apply({ ...DEFAULT_FILTERS, axisY: 'north' });
    const kinds = r.map((it) => it.kind);
    const firstGhost = kinds.indexOf('ghost');
    const lastKit = kinds.lastIndexOf('kit');
    expect(lastKit).toBeLessThan(firstGhost); // every kit precedes every ghost
    // And within each kind, emitted order is preserved (stable filter).
    const kitIds = r.filter((it) => it.kind === 'kit').map((it) => (it as { row: AtlasKitRow }).row.kit_id);
    expect(kitIds).toEqual(['live-single-EN', 'live-aura-EN']);
  });
});
