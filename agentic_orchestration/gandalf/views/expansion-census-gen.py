#!/usr/bin/env python3
"""Expansion census generator (Unit A, continuation brief 2026-07-12).
Deterministic pass over rdr-kit-atlas-v3.csv CANON ROWS ONLY (source=='canon';
roster/bench source rows excluded). Buckets by the 6-slot engine prefix (bc6);
negatives counted separately, never in coverage. Joins roster occupancy from
roster-atlas-rebuilt-v1.csv (bc5 ex-commitment key — roster commit mostly unpinned).
Selection principle (Matt verbatim): "simple coverage of the count of genre kits,
weighted by the longevity/lineage." Ruled weight (transparent first cut) =
kit_count x distinct_era_count; cross-decade flag reported alongside.

Outputs: expansion-census-v1.csv  (+ stdout summary consumed by findings md).
Re-runnable: python3 expansion-census-gen.py
"""
import csv, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(HERE, '..', '..', '..',
    'claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv')
ROSTER = os.path.join(HERE, 'roster-atlas-rebuilt-v1.csv')
OUT = os.path.join(HERE, 'expansion-census-v1.csv')

# Game release years (for cross-decade longevity flag). d2->poe2 = ~24yr recurrence.
GAME_YEAR = {'d2':2000,'tq':2006,'tl':2009,'d3':2012,'poe1':2013,'gd':2016,
             'le':2019,'chronicon':2019,'hades':2020,'vs':2021,'di':2022,
             'undecember':2022,'d4':2023,'hot':2023,'poe2':2024}

def bc6(k): return k[:6]
def bc5(k): return k[:5]

# ---- load canon ----
rows = list(csv.DictReader(open(V3)))
canon = [r for r in rows if r['source'] == 'canon']

# ---- load roster occupancy (rebuilt rows; bc5 ex-commitment key) ----
roster = list(csv.DictReader(open(ROSTER)))
def rkey5(r):
    return ''.join((r[s] if r[s] not in ('', '_') else '_')
                   for s in ['attr','range','tempo','amp','proxy'])
def rkey6(r):
    return rkey5(r) + (r['commit'] if r['commit'] not in ('','_') else '_')
# occupancy indexed by bc5; only kits with a COMPLETE bc5 (no '_') can occupy a cell
occ5 = collections.defaultdict(list)
occ6 = collections.defaultdict(list)
for r in roster:
    k5 = rkey5(r)
    if '_' not in k5:
        occ5[k5].append(r['kit_id'])
        occ6[rkey6(r)].append(r['kit_id'])

# ---- bucket canon by bc6 ----
cells = collections.defaultdict(list)
for r in canon:
    cells[bc6(r['atlas_key'])].append(r)

def era_set(members):
    s = set()
    for r in members:
        for e in r['eras'].split(';'):
            if e.strip(): s.add(e.strip())
    return s

def summarize(key, members):
    pos = [r for r in members if r['negative'] == 'False']
    neg = [r for r in members if r['negative'] == 'True']
    games = sorted({r['game'] for r in pos})
    tiers = collections.Counter(r['tier'] for r in pos)
    eras = era_set(pos)
    years = [GAME_YEAR[g] for g in games if g in GAME_YEAR]
    yspan = (max(years) - min(years)) if years else 0
    cross_decade = yspan >= 10
    lineage = sorted({r['lineage'] for r in pos if r['lineage'].strip()})
    gx = sorted({g for r in pos for g in r['gx'].split() if g.startswith('GX-')})
    k5 = bc5(key)
    occ = occ5.get(k5, [])
    occ_exact = occ6.get(key, [])
    kit_count = len(pos)
    era_ct = len(eras)
    if occ:
        status = 'occupied-by-us'
    elif kit_count > 0:
        status = 'genre-attested'
    elif neg:
        status = 'genre-negative'
    else:
        status = 'whitespace'
    return {
        'bc6': key, 'bc5': k5, 'status': status,
        'kit_count': kit_count, 'neg_count': len(neg),
        'distinct_games': len(games), 'games': '|'.join(games),
        'tier_mix': ';'.join(f'{t}:{tiers[t]}' for t in sorted(tiers)),
        'distinct_era_count': era_ct, 'year_span': yspan,
        'cross_decade': 'Y' if cross_decade else '',
        'lineage_present': 'Y' if lineage else '',
        'lineage': '|'.join(lineage),
        'gx_families': '|'.join(gx),
        'occupied_by': '|'.join(sorted(set(occ))),
        'occupied_exact_commit': '|'.join(sorted(set(occ_exact))),
        'ruled_weight': kit_count * era_ct,
    }

recs = [summarize(k, m) for k, m in cells.items()]

# ---- roster whitespace: roster bc5 cells with NO canon at that bc5 ----
canon_bc5 = {bc5(k) for k in cells}
whitespace = []
for k5, kits in sorted(occ5.items()):
    if k5 not in canon_bc5:
        whitespace.append((k5, sorted(set(kits))))

cols = ['bc6','bc5','status','kit_count','neg_count','distinct_games','games',
        'tier_mix','distinct_era_count','year_span','cross_decade',
        'lineage_present','lineage','gx_families','occupied_by',
        'occupied_exact_commit','ruled_weight']
recs.sort(key=lambda r: (-r['ruled_weight'], -r['kit_count'], r['bc6']))
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in recs: w.writerow(r)

# ---- stdout summary for findings ----
print(f"canon rows: {len(canon)} | bc6 cells: {len(recs)}")
sc = collections.Counter(r['status'] for r in recs)
print(f"status split (canon bc6 cells): {dict(sc)}")
print(f"roster occupancy: bc5 keys occupying {sum(1 for r in recs if r['status']=='occupied-by-us')} canon cells")
print(f"roster-whitespace bc5 (no canon at bc5): {len(whitespace)}")
for k5, kits in whitespace:
    print(f"   WS {k5}: {kits}")

print("\nTOP 20 UNOCCUPIED genre-attested cells by ruled_weight (expansion targets):")
unocc = [r for r in recs if r['status'] == 'genre-attested']
for r in unocc[:20]:
    cd = ' [CROSS-DECADE]' if r['cross_decade'] else ''
    print(f"  {r['bc6']}  w={r['ruled_weight']:>3}  kits={r['kit_count']:>2} eras={r['distinct_era_count']:>2} "
          f"games={r['distinct_games']} span={r['year_span']:>2}yr{cd}  [{r['games']}]")

print("\nBC5 ex-commitment rollup (top 15 by kit_count):")
roll = collections.defaultdict(lambda: {'kits':0,'eras':set(),'games':set(),'occ':set()})
for k, m in cells.items():
    pos = [r for r in m if r['negative']=='False']
    d = roll[bc5(k)]
    d['kits'] += len(pos)
    for r in pos:
        d['games'].add(r['game'])
        for e in r['eras'].split(';'):
            if e.strip(): d['eras'].add(e.strip())
for k5 in occ5:
    roll[k5]['occ'].update(occ5[k5])
top = sorted(roll.items(), key=lambda kv:-kv[1]['kits'])[:15]
for k5, d in top:
    occ = 'OURS:'+','.join(sorted(d['occ'])) if d['occ'] else 'UNOCC'
    print(f"  {k5}  kits={d['kits']:>2} eras={len(d['eras']):>2} games={len(d['games'])}  {occ}")

print("\nMECHANICS CUT (GX family x coverage):")
gxcov = collections.defaultdict(lambda: {'cells':set(),'games':set(),'occ_cells':set()})
for r in recs:
    for g in r['gx_families'].split('|'):
        if not g: continue
        gxcov[g]['cells'].add(r['bc6'])
        for gm in r['games'].split('|'):
            if gm: gxcov[g]['games'].add(gm)
        if r['status'] == 'occupied-by-us':
            gxcov[g]['occ_cells'].add(r['bc6'])
for g in sorted(gxcov, key=lambda x:(int(x.split('-')[1]))):
    d = gxcov[g]
    print(f"  {g:>6}  cells={len(d['cells']):>2} games={len(d['games']):>2} "
          f"occupied_by_founding={'Y' if d['occ_cells'] else 'no'}")
