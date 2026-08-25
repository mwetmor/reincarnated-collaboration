"""RESID-D1-2 step 1: enumerate the candidate locomotion / update surface by symbol.
READ-ONLY. Emits a symbol census so nothing downstream is picked by guess."""
import sys, re, json; sys.path.insert(0, '.')
import d4b_dis as D

pats = sys.argv[1:] or ['Move', 'Locomot', 'Velocit', 'Speed', 'Path', 'Update', 'Steer', 'Walk', 'Run']
out = {}
for p in pats:
    rx = re.compile(p, re.I)
    hits = sorted(((r, n) for n, r in D.EX.items() if rx.search(n)), key=lambda t: t[0])
    out[p] = [f'{r:#010x}  {n}' for r, n in hits]
    print(f'=== /{p}/  {len(hits)} ===')
    for line in out[p]:
        print(' ', line)
json.dump(out, open('evidence/r1_symscan.json', 'w'), indent=1)
