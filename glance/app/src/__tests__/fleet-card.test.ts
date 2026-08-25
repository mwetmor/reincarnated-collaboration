// Fleet rear-view — parser fold + card render contract (U-1 §12.4 / AM-1 §13.1, drax).
//
// Two halves, both load-bearing:
//   1. the FOLD (parser/fleet.mjs) must match `flight/schema.py`'s semantics — corrections
//      drop superseded rows from the view, identity comes from ENQUEUE/START with CLOSE only
//      filling nulls, SEALED means a terminal event exists, and every aggregate carries its
//      denominator.
//   2. the CARD must stay REAR-VIEW ONLY and honest when empty. A live-lane word appearing
//      on this surface is a bug by construction: a Vercel build cannot see pre-push facts.
//
// Rendered with `react-dom/server` (already a dependency) so the whole tree is exercised in
// the node environment — no DOM, no new devDependency.

import { describe, it, expect } from 'vitest';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

import { buildFleet, fold, applyCorrections } from '../../../parser/fleet.mjs';
import { FleetPage } from '../pages/Fleet';
import { cacheRate, fmtSpan, fmtTokens } from '../state';

const render = (fleet: unknown) =>
  renderToStaticMarkup(createElement(FleetPage as never, { fleet } as never));

// ---------------------------------------------------------------- fold semantics
describe('fleet fold', () => {
  it('drops rows superseded by a correction, from the VIEW only', () => {
    const rows = [
      { row_id: 'a', ts: '2026-08-01T00:00:00Z', event: 'CLOSE', unit_id: 'u1', rc: 1 },
      { row_id: 'b', ts: '2026-08-01T00:01:00Z', event: 'CLOSE', unit_id: 'u1', rc: 0,
        corrects: 'a' },
    ];
    const kept = applyCorrections(rows);
    expect(kept.map((r) => r.row_id)).toEqual(['b']);
    expect(rows).toHaveLength(2); // the input (the tape) is untouched
  });

  it('folds state from events: SEALED / IN-FLIGHT / QUEUED / OPEN', () => {
    const units = fold([
      { row_id: '1', ts: '2026-08-01T00:00:00Z', event: 'ENQUEUE', unit_id: 'q' },
      { row_id: '2', ts: '2026-08-01T00:00:00Z', event: 'START', unit_id: 'f' },
      { row_id: '3', ts: '2026-08-01T00:00:00Z', event: 'START', unit_id: 's' },
      { row_id: '4', ts: '2026-08-01T00:05:00Z', event: 'CLOSE', unit_id: 's' },
      { row_id: '5', ts: '2026-08-01T00:00:00Z', event: 'GATE', unit_id: 'o' },
    ]);
    const state = Object.fromEntries(units.map((u) => [u.unit_id, u.state]));
    expect(state).toEqual({ q: 'QUEUED', f: 'IN-FLIGHT', s: 'SEALED', o: 'OPEN' });
    expect(units.find((u) => u.unit_id === 's')!.duration).toBe(300);
  });

  it('takes identity from ENQUEUE/START, never from a gatekeeper\'s GATE row', () => {
    const [u] = fold([
      { row_id: '1', ts: '2026-08-01T00:00:00Z', event: 'START', unit_id: 'r',
        operator: 'gandalf', lane: 'claude-agent' },
      { row_id: '2', ts: '2026-08-01T01:00:00Z', event: 'GATE', unit_id: 'r',
        operator: 'jack-ryan', gatekeeper: 'jack-ryan' },
      { row_id: '3', ts: '2026-08-01T02:00:00Z', event: 'CLOSE', unit_id: 'r',
        operator: 'someone-else', pin: 'p1' },
    ]);
    expect(u.ident.operator).toBe('gandalf');   // owner, not last actor
    expect(u.ident.pin).toBe('p1');             // CLOSE fills what START left null
  });
});

// ---------------------------------------------------------------- absence + emptiness
describe('fleet node tolerance', () => {
  it('returns null when there is no flight directory at all', () => {
    expect(buildFleet('/nonexistent/flight/dir/for/this/test')).toBeNull();
  });

  it('renders "no flight recorder in this repo" for a null node', () => {
    const html = render(null);
    expect(html).toContain('no flight recorder in this repo');
    expect(html).toContain('ABSENCE IS NEVER AN ERROR');
  });

  it('renders an empty tape honestly, with both vendor lanes still present', () => {
    const empty = {
      source: 'agentic_orchestration/flight',
      tape_files: [], rows_on_disk: 0, rows_after_corrections: 0, unparseable_lines: 0,
      schema_versions: [], coverage: { first_ts: null, last_ts: null },
      units_total: 0, units_sealed: 0,
      workstreams: [], scorecards: [], months: [],
      lanes: [
        { lane: 'codex-serial', provider: 'openai', on_tape: false, spellings_seen: [],
          pins: [], units: 0, tokens: { input: 0, cached_input: 0, cache_write: 0, output: 0,
            reasoning: 0 }, n_tokens: 0, rc_zero: 0, rc_total: 0, verdicts: {}, cost_usd: 0,
          n_cost: 0, median_wall_s: null, currencies: [], last_close: null },
        { lane: 'grok-serial', provider: 'xai', on_tape: false, spellings_seen: [],
          pins: [], units: 0, tokens: { input: 0, cached_input: 0, cache_write: 0, output: 0,
            reasoning: 0 }, n_tokens: 0, rc_zero: 0, rc_total: 0, verdicts: {}, cost_usd: 0,
          n_cost: 0, median_wall_s: null, currencies: [], last_close: null },
      ],
      claude: { units: 0, closes: 0, with_tokens: 0 },
      verdicts: { totals: {}, recent: [] },
      snapshots: [],
    };
    const html = render(empty);
    expect(html).toContain('No rows on the tape yet');
    // AM-1 parity: grok renders wherever codex does, even with nothing to show.
    expect(html).toContain('codex-serial');
    expect(html).toContain('grok-serial');
    expect(html).toContain('no rows on tape');
    // honest nulls, not zeroes
    expect(html).toContain('no SNAPSHOT row on the tape');
    expect(html).toContain('no sealed unit on the tape yet');
  });
});

// ---------------------------------------------------------------- live tape (this repo)
describe('fleet node against the committed tape', () => {
  const fleet = buildFleet(new URL('../../../../agentic_orchestration/flight',
    import.meta.url).pathname);

  it('folds the committed tape (or is null if this checkout has none)', () => {
    if (!fleet) return;                       // absence is legal, including in CI forks
    expect(fleet.rows_on_disk).toBeGreaterThan(0);
    expect(fleet.units_sealed).toBeLessThanOrEqual(fleet.units_total);
    expect(fleet.lanes.map((l: { lane: string }) => l.lane))
      .toEqual(['codex-serial', 'grok-serial']);
  });

  it('emits no live-state NODE — rear-view scope is enforced in the data, not the prose', () => {
    if (!fleet) return;
    const json = JSON.stringify(fleet);
    // Lane liveness, in-flight lists and health probes belong to the local board; a static
    // build cannot know them, so they must not be in the payload AT ALL. (Prose on the page
    // is allowed to NAME them while explaining where they live — hence the node check.)
    for (const forbidden of ['busy-lock', 'busy-out-of-band', 'auth-expired', 'cli-missing',
      'queue-pending', 'ENABLE_PROMPT_CACHING_1H', 'in_flight', 'inflight', 'health']) {
      expect(json).not.toContain(forbidden);
    }
    expect(Object.keys(fleet)).not.toContain('in_flight');
  });

  it('renders lane state nowhere on the page, and says which window owns it', () => {
    if (!fleet) return;
    const html = render(fleet);
    for (const forbidden of ['busy-lock', 'busy-out-of-band', 'auth-expired',
      'probe: degraded']) {
      expect(html).not.toContain(forbidden);
    }
    expect(html).toContain('rear-view mirror, not the windshield');
    expect(html).toContain('the local board renders it');
  });

  it('carries a denominator wherever it carries a cost', () => {
    if (!fleet) return;
    for (const b of [...fleet.workstreams, ...fleet.scorecards, ...fleet.lanes]) {
      if (b.n_cost === 0) expect(b.cost_usd).toBe(0);   // absent is never a partial sum
      expect(b.n_cost).toBeLessThanOrEqual(b.units);
      expect(b.n_tokens).toBeLessThanOrEqual(b.units);
      expect(b.rc_zero).toBeLessThanOrEqual(b.rc_total);
    }
  });
});

// ---------------------------------------------------------------- display helpers
describe('display helpers', () => {
  it('formats tokens and spans the way the Tier-1 report does', () => {
    expect(fmtTokens(72375471)).toBe('72.4M');
    expect(fmtTokens(259471)).toBe('259K');
    expect(fmtTokens(null)).toBe('—');
    expect(fmtSpan(38041)).toBe('10.6h');
    expect(fmtSpan(1408)).toBe('23m');
    expect(fmtSpan(null)).toBe('—');
  });

  it('returns null for a cache rate with no denominator, never 0%', () => {
    expect(cacheRate({ input: 0, cached_input: 0, cache_write: 0, output: 0, reasoning: 0 }))
      .toBeNull();
    const r = cacheRate({ input: 72375471, cached_input: 67431424, cache_write: 0,
      output: 0, reasoning: 0 });
    expect(r).not.toBeNull();
    expect(r!.toFixed(1)).toBe('93.2');
  });
});
