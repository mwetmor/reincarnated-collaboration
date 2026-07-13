#!/usr/bin/env python3
"""
gen-unit-b.py — Unit B: founding-roster lineage enrichment (45 rows)
Output: roster-lineage-enrichment.jsonl
Content: genre-lineage stats ONLY — bc6 coordinates, lineage target resolution,
         nearest corpus neighbors (d=0/1/2), genre coverage counts.
"""

import csv, json, re
from pathlib import Path

BASE = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12")
ROSTER_CSV = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/views/roster-atlas-rebuilt-v1.csv")
CORPUS_CSV = Path("/Users/admin/Games/reincarnated-collaboration/claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv")

# ─── BC6 SLOT DECODING ───────────────────────────────────────────────────────

ATTR_DEC  = {'S':'STR','D':'DEX','I':'INT','W':'WIS','_':'__'}
RANGE_DEC = {'M':'melee','D':'mid','R':'ranged','_':'__'}
TEMPO_DEC = {'L':'low','M':'med','H':'high','_':'__'}
AMP_DEC   = {'F':'flat','S':'spiky','V':'variable','_':'__'}
PROXY_DEC = {'S':'solo','L':'light','H':'heavy','_':'__'}
COMMIT_DEC = {'I':'instant','W':'wind-up','C':'channel','_':'__'}

SLOTS = ['attr','range','tempo','amp','proxy','commit']

def roster_bc6(row):
    return {
        'attr':   ATTR_DEC.get(row['attr'],'__'),
        'range':  RANGE_DEC.get(row['range'],'__'),
        'tempo':  TEMPO_DEC.get(row['tempo'],'__'),
        'amp':    AMP_DEC.get(row['amp'],'__'),
        'proxy':  PROXY_DEC.get(row['proxy'],'__'),
        'commit': COMMIT_DEC.get(row['commit'],'__'),
    }

def parse_atlas_key_bc6(atlas_key):
    """Parse corpus atlas_key prefix (6-char) into bc6 dict."""
    parts = atlas_key.split('-')
    if not parts or len(parts[0]) != 6:
        return None
    p = parts[0]
    return {
        'attr':   ATTR_DEC.get(p[0],'__'),
        'range':  RANGE_DEC.get(p[1],'__'),
        'tempo':  TEMPO_DEC.get(p[2],'__'),
        'amp':    AMP_DEC.get(p[3],'__'),
        'proxy':  PROXY_DEC.get(p[4],'__'),
        'commit': COMMIT_DEC.get(p[5],'__'),
    }

def bc6_distance(a, b):
    """Hamming distance on known (non-__) slots. Returns (diff, compared_slots)."""
    diff, compared = 0, 0
    for s in SLOTS:
        av, bv = a.get(s,'__'), b.get(s,'__')
        if av == '__' or bv == '__':
            continue
        compared += 1
        if av != bv:
            diff += 1
    return diff, compared

# ─── LINEAGE TARGET PARSING ──────────────────────────────────────────────────

def parse_lineage_targets(lt_str):
    """Parse 'game:kit|game2:kit2' into list of dicts."""
    if not lt_str.strip():
        return []
    targets = []
    for part in lt_str.split('|'):
        part = part.strip()
        if ':' in part:
            game, kit = part.split(':', 1)
            targets.append({'game': game.strip(), 'kit_name': kit.strip()})
        elif part:
            targets.append({'game': 'unknown', 'kit_name': part})
    return targets

def normalize_kit_name(name):
    """Normalize kit name for corpus lookup."""
    return name.lower().strip().replace(' ', '-').replace('/', '-')

# Explicit lineage target → corpus kit_id overrides for known-hard fuzzy matches
LINEAGE_OVERRIDES = {
    'd2:whirlwind':           'd2-ww-barb',
    'd2:whirlwindbarb':       'd2-ww-barb',
    'd2:whirlwind barb':      'd2-ww-barb',
    'd3:call of the ancients':'',           # CORPUS GAP
    'd3:calloftheancients':   '',
    'd3:ancestors':           '',
    'd3:raiment generator':   'd3-raiment-generator',
    'd3:generator':           'd3-raiment-generator',
    'poe1:totems':            '',           # CORPUS GAP (poe1 hierophant)
    'poe1:hierophant':        '',
    'poe1:warchief':          '',
    'poe1:ancestral warchief':'',
    'poe1:ring of shields':   '',
    'poe1:blood magic keystone': '',
    'poe1:vaal blade vortex': '',
    'poe1:flame dash':        '',
    'd3:dashing strike':      '',
    'le:shift bladedancer':   '',
    'd2:trapsin':             'd2-trapsin',
    'd2:trap assassin':       'd2-trapsin',
    'd2:summonmancer':        'd2-summonmancer',
    'd2:necromancer summoner':'d2-summonmancer',
    'd2:skele':               'd2-summonmancer',
    'd2:skeleton summoner':   'd2-summonmancer',
    'd2:skeleton':            'd2-summonmancer',
    'd2:hammerdin':           'd2-hammerdin',
    'le:hammerdin':           'le-hammer-throw-paladin',
    'le:hammer throw':        'le-hammer-throw-paladin',
    'poe2:titan slam':        'poe2-titan-hotg',
    'poe2:smith of kitava':   'poe2-smith-ignite',
    'hades2:hephaestus':      'hades2-hephaestus-blast',
    'poe1:winter orb':        'poe1-winter-orb',
    'poe1:storm brand':       'poe1-storm-brand',
    'poe1:blade vortex':      'poe1-blade-vortex',
}

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    # Load roster
    with open(ROSTER_CSV) as f:
        roster = list(csv.DictReader(f))

    # Load corpus (positive only for neighbor search; all for lineage resolution)
    with open(CORPUS_CSV) as f:
        all_corpus = list(csv.DictReader(f))

    # Build corpus index — exclude rdr-roster rows (those are the roster kits themselves)
    corp_entries = []
    for r in all_corpus:
        if r.get('game','') == 'rdr-roster':
            continue  # don't include roster rows as corpus neighbors
        bc6 = parse_atlas_key_bc6(r.get('atlas_key',''))
        if not bc6:
            continue
        corp_entries.append({
            'kit_id': r['kit_id'],
            'folk_name': r['folk_name'],
            'game': r['game'],
            'atlas_key': r['atlas_key'],
            'bc6': bc6,
            'negative': r.get('negative','').lower() == 'true',
            'status': 'negative' if r.get('negative','').lower() == 'true' else 'positive',
        })

    # Index by kit_id for lineage target lookup
    corp_by_id = {e['kit_id']: e for e in corp_entries}
    # Also index by game+normalized-folk-name for fuzzy lookup
    corp_by_game_name = {}
    for e in corp_entries:
        key = e['game'] + ':' + normalize_kit_name(e['folk_name'])
        corp_by_game_name.setdefault(key, []).append(e)

    def find_lineage_corpus_match(lt):
        """Try to resolve a lineage target to a corpus kit."""
        game = lt['game']
        kit_name = lt['kit_name']
        ref_key = f"{game}:{kit_name.lower()}"

        # Check explicit overrides first
        override_id = LINEAGE_OVERRIDES.get(ref_key)
        if override_id is not None:
            if override_id == '':
                return None  # explicit gap
            return corp_by_id.get(override_id)

        # Also check normalized ref key
        norm = normalize_kit_name(kit_name)
        norm_key = f"{game}:{norm}"
        override_id = LINEAGE_OVERRIDES.get(norm_key)
        if override_id is not None:
            if override_id == '':
                return None
            return corp_by_id.get(override_id)

        # Fuzzy: prefer folk_name token overlap over kit_id substring match
        norm_tokens = set(norm.replace('-', ' ').split())
        scored = []
        for e in corp_entries:
            if e['game'] != game:
                continue
            fn_norm = normalize_kit_name(e['folk_name'])
            fn_tokens = set(fn_norm.replace('-', ' ').split())
            overlap = len(norm_tokens & fn_tokens)
            if overlap > 0:
                scored.append((overlap, e))

        if scored:
            scored.sort(key=lambda x: -x[0])
            return scored[0][1]

        # Fallback: kit_id substring
        for e in corp_entries:
            if e['game'] != game:
                continue
            if norm in e['kit_id'] or kit_name.lower() in e['kit_id'].lower():
                return e

        return None

    def find_nearest_neighbors(bc6_target, exclude_ids=None, max_results=8, max_dist=2):
        """Find nearest corpus neighbors by bc6 Hamming distance."""
        exclude = set(exclude_ids or [])
        neighbors = []
        for e in corp_entries:
            if e['kit_id'] in exclude:
                continue
            if e['negative']:
                continue
            d, compared = bc6_distance(bc6_target, e['bc6'])
            if compared < 3:
                continue  # too few slots to compare reliably
            if d <= max_dist:
                neighbors.append({'kit_id': e['kit_id'], 'folk_name': e['folk_name'],
                                   'game': e['game'], 'bc6': e['bc6'],
                                   'distance': d, 'slots_compared': compared})
        neighbors.sort(key=lambda x: (x['distance'], -x['slots_compared']))
        return neighbors[:max_results]

    out_rows = []
    for row in roster:
        kit_id = row['kit_id']
        bc6 = roster_bc6(row)
        class_v4r2 = row.get('class_v4r2','').strip()
        lt_raw = row.get('lineage_targets','').strip()
        lts = parse_lineage_targets(lt_raw)

        # Resolve each lineage target to corpus
        resolved_targets = []
        exclude_ids = []
        for lt in lts:
            match = find_lineage_corpus_match(lt)
            if match:
                d, comp = bc6_distance(bc6, match['bc6'])
                resolved_targets.append({
                    'target_ref': f"{lt['game']}:{lt['kit_name']}",
                    'corpus_kit_id': match['kit_id'],
                    'corpus_folk_name': match['folk_name'],
                    'corpus_bc6': match['bc6'],
                    'bc6_distance': d,
                    'slots_compared': comp,
                    'resolved': True,
                })
                exclude_ids.append(match['kit_id'])
            else:
                resolved_targets.append({
                    'target_ref': f"{lt['game']}:{lt['kit_name']}",
                    'corpus_kit_id': None,
                    'corpus_folk_name': None,
                    'corpus_bc6': None,
                    'bc6_distance': None,
                    'slots_compared': None,
                    'resolved': False,
                    'gap': True,  # corpus gap — mint candidate
                })

        # Nearest neighbors (all positive corpus kits)
        neighbors = find_nearest_neighbors(bc6, exclude_ids=exclude_ids, max_results=8, max_dist=2)

        # Summary stats
        d0 = sum(1 for n in neighbors if n['distance'] == 0)
        d1 = sum(1 for n in neighbors if n['distance'] == 1)
        d2 = sum(1 for n in neighbors if n['distance'] == 2)

        # Resolved target distance stats
        resolved_dists = [t['bc6_distance'] for t in resolved_targets if t.get('resolved') and t['bc6_distance'] is not None]
        min_target_dist = min(resolved_dists) if resolved_dists else None

        out_rows.append({
            'kit_id': kit_id,
            'folk_name': row['name'],
            'class_v4r2': class_v4r2,
            'bc6': bc6,
            'bc6_raw': ''.join([row['attr'], row['range'], row['tempo'], row['amp'], row['proxy'], row['commit']]),
            'provenance': row.get('provenance','').strip(),
            'note': row.get('note','').strip(),
            'lineage_targets': resolved_targets,
            'target_count': len(lts),
            'targets_resolved': sum(1 for t in resolved_targets if t.get('resolved')),
            'targets_gap': sum(1 for t in resolved_targets if t.get('gap')),
            'min_lineage_target_distance': min_target_dist,
            'nearest_corpus_neighbors': neighbors,
            'neighbor_count_d0': d0,
            'neighbor_count_d1': d1,
            'neighbor_count_d2': d2,
            'genre_density': d0 + d1 + d2,
            'whitespace_flag': (d0 == 0 and d1 == 0),  # no corpus kits within d=1
        })

    # Write output
    out_path = BASE / 'roster-lineage-enrichment.jsonl'
    with open(out_path, 'w') as f:
        for row in out_rows:
            f.write(json.dumps(row) + '\n')

    # Summary
    print(f"Written {len(out_rows)} rows to {out_path}")
    whitespace = [r for r in out_rows if r['whitespace_flag']]
    lineage = [r for r in out_rows if r['class_v4r2'].startswith('LINEAGE')]
    gaps = [r for r in out_rows if r['targets_gap'] > 0]
    print(f"  LINEAGE kits: {len(lineage)}")
    print(f"  WHITESPACE (d0+d1=0): {len(whitespace)} → {[r['kit_id'] for r in whitespace]}")
    print(f"  Kits with corpus gaps: {len(gaps)} → {[(r['kit_id'], r['targets_gap']) for r in gaps]}")

    # Show sample records
    for r in out_rows[:3]:
        print(f"\n  {r['kit_id']} {r['folk_name']} [{r['class_v4r2']}]")
        for t in r['lineage_targets']:
            print(f"    → {t['target_ref']}: corpus={t['corpus_kit_id']} d={t['bc6_distance']}")
        print(f"    neighbors: d0={r['neighbor_count_d0']} d1={r['neighbor_count_d1']} d2={r['neighbor_count_d2']}")

if __name__ == '__main__':
    main()
