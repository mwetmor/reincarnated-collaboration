#!/usr/bin/env python3
"""Canon-corpus v1.0 ingest DRY-RUN + row-level validator.

READ-ONLY: parses rdr-kit-atlas-v3.csv, decodes the atlas_key prefix into the typed engine-lattice
columns, maps raw suffix descriptors, and reports dry-run counts + validation findings.
Writes NOTHING (no DB, no files). This is the staged-ingest validation stage; actual ingest is
gated on Matt's housing D-ruling + ADR-006 authorization.

Usage:  python3 corpus_ingest_dryrun_2026_07_12.py [path/to/rdr-kit-atlas-v3.csv]
"""
import csv, sys
from collections import Counter

DEFAULT_CSV = ("/Users/admin/Games/reincarnated-collaboration/claude-mobile-session-docs/"
               "ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv")

# prefix decode maps (invert generator code_* fns). Position in atlas_key prefix: attr,range,tempo,amp,proxy,commit
ATTR  = {'S':'STR','D':'DEX','I':'INT','W':'WIS','_':None}
RANGE = {'M':'melee','D':'mid','R':'ranged','_':None}
TEMPO = {'L':'low','M':'med','H':'high','_':None}
AMP   = {'F':'flat','S':'spiky','V':'var','_':None}
PROXY = {'S':'solo','L':'light','H':'heavy','_':None}
COMMIT= {'I':'instant','W':'wind-up','C':'channel','_':None}   # enum OF RECORD
# measured 4-slot codes (ctrl/def raw are code-derived — v3 CSV drops the source-raw strings)
CTRL  = {'C':'control-pure','M':'mixed','D':'damage','_':None}
DEFN  = {'T':'tank','M':'mitigation','D':'dodge','G':'glass','_':None}

# game-of-record = the `game` column (NOT `corpus`, which is the harvest BUCKET:
#   corpus='hades' splits into game hades1/hades2; corpus='tl' splits into tl1/tl2/tli).
VALID_GAMES = {'poe1','poe2','d2','d3','d4','le','gd','tq','tq2','tl','tl1','tl2','tli','chronicon',
               'hades1','hades2','di','undecember','vs','hot','rdr-roster'}

def parse_prefix(atlas_key):
    """Return (attr,range,tempo,amp,proxy,commit, ctrl_code, def_code) decoded, plus lattice_coord."""
    parts = (atlas_key or '').split('-')
    pre = parts[0] if parts else ''
    meas = parts[1] if len(parts) > 1 else ''
    pre = (pre + '______')[:6]
    meas = (meas + '____')[:4]
    return {
        'lattice_coord': pre,
        'attr': ATTR.get(pre[0]), 'range': RANGE.get(pre[1]), 'tempo': TEMPO.get(pre[2]),
        'amp': AMP.get(pre[3]), 'proxy': PROXY.get(pre[4]), 'commit': COMMIT.get(pre[5]),
        'ctrl_raw': CTRL.get(meas[2]), 'def_raw': DEFN.get(meas[3]),
    }

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    rows = list(csv.DictReader(open(path)))
    n = len(rows)
    findings = []           # (severity, kit_id, msg)
    ids = Counter()
    src = Counter(); games = Counter(); routing = Counter()

    for r in rows:
        kid = r['kit_id']; ids[kid] += 1
        source = r['source']; src[source] += 1
        game = r['game']; games[game] += 1     # game-of-record; `corpus` is the harvest bucket

        # routing classification (which staged bucket the row lands in)
        kc = int(r['key_completeness'] or 0)
        kg = r['key_group']
        is_sys = kg.startswith('SYS')
        unresolved = (not is_sys) and kc < 4
        prov_only = source in ('roster', 'bench')
        if is_sys: routing['SYS-annex (is_system=1)'] += 1
        elif prov_only: routing['roster/bench (roster_provenance_only=1)'] += 1
        elif unresolved: routing['canon UNRESOLVED (unresolved=1)'] += 1
        else: routing['canon substrate (v_corpus_substrate)'] += 1

        # ---- row-level validation ----
        pre = parse_prefix(r['atlas_key'])
        # enum sanity: proxy/commit raw cols should agree with decoded prefix when both present
        raw_proxy = (r.get('proxy') or '').lower()
        if pre['proxy'] and raw_proxy and pre['proxy'] not in raw_proxy and raw_proxy not in pre['proxy']:
            findings.append(('WARN', kid, f"proxy decode '{pre['proxy']}' vs raw col '{r.get('proxy')}'"))
        raw_commit = (r.get('commit') or '').lower()
        if pre['commit'] and raw_commit:
            norm = 'wind-up' if 'wind' in raw_commit else ('channel' if 'chan' in raw_commit else ('instant' if 'inst' in raw_commit else raw_commit))
            if norm != pre['commit']:
                findings.append(('WARN', kid, f"commit decode '{pre['commit']}' vs raw col '{r.get('commit')}'"))
        # game whitelist
        if game not in VALID_GAMES:
            findings.append(('ERROR', kid, f"unknown game-of-record '{game}'"))
        # avg_conf range
        try:
            ac = float(r['avg_conf'] or 0)
            if not (0.0 <= ac <= 1.0):
                findings.append(('ERROR', kid, f"avg_conf out of [0,1]: {ac}"))
        except ValueError:
            findings.append(('ERROR', kid, f"avg_conf non-numeric: {r['avg_conf']!r}"))
        # negative flag domain
        if r['negative'] not in ('True', 'False'):
            findings.append(('ERROR', kid, f"negative not boolean: {r['negative']!r}"))

    dupes = {k: c for k, c in ids.items() if c > 1}
    for k, c in dupes.items():
        findings.append(('ERROR', k, f"duplicate kit_id x{c} (PRIMARY KEY collision)"))

    # ---- report ----
    print("="*72)
    print("CANON-CORPUS v1.0 — INGEST DRY-RUN (READ-ONLY; no writes)")
    print("="*72)
    print(f"source CSV: {path}")
    print(f"TOTAL ROWS: {n}\n")
    print("-- source class --")
    for k, v in src.most_common(): print(f"   {v:4}  {k}")
    print("\n-- staged routing buckets --")
    for k, v in routing.most_common(): print(f"   {v:4}  {k}")
    print(f"\n   => canon substrate (WHERE source='canon' AND is_system=0 AND unresolved=0): "
          f"{routing['canon substrate (v_corpus_substrate)']}")
    print("\n-- game-of-record (top) --")
    for k, v in games.most_common(): print(f"   {v:4}  {k}")
    hot = games.get('hot', 0)
    print(f"\n-- HoT (own game; tier lean T3, tier_confirm_pending=1): {hot} rows --")
    print("\n" + "-"*72)
    errs = [f for f in findings if f[0] == 'ERROR']
    warns = [f for f in findings if f[0] == 'WARN']
    print(f"VALIDATION: {len(errs)} ERROR, {len(warns)} WARN")
    print(f"  unique kit_id: {len(ids)} / {n}  |  duplicate ids: {len(dupes)}")
    for sev, kid, msg in errs[:20]:
        print(f"   [ERROR] {kid}: {msg}")
    for sev, kid, msg in warns[:15]:
        print(f"   [warn ] {kid}: {msg}")
    if len(warns) > 15: print(f"   ... +{len(warns)-15} more warnings")
    print("\nGATE: dry-run only. Ingest fires after Matt housing D-ruling + ADR-006 authorization.")

if __name__ == '__main__':
    main()
