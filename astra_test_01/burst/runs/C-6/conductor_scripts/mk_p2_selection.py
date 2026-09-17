# Conductor selection note for C-6 P2: per direction, which attempt STANDS (v1 or r1) from the two judgments; flags carried to the packet.
# Rule (R-C6-7): for retried directions take the attempt with the higher axis-4, tie → higher axis sum, tie → r1 (the correction was applied);
# a direction whose standing attempt has axis-4 < 4 or back_details_wrong ships FLAGGED. Non-retried directions stand on v1.
import json, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-6/artifacts'
j1 = {c['claimed']: c for c in json.load(open(A/'N5-jdg-01/judgment.json'))['candidates'] if c['image'] != 5}
j2 = {c['claimed']: c for c in json.load(open(A/'N5-jdg-02/judgment.json'))['candidates'] if c['image'] != 4}
sel = {}
for d in ['SW','W','NW','N','NE','E','SE']:
    v1 = j1[d]; r1 = j2.get(d)
    def score(c): return (c['axes']['4'], sum(c['axes'].values()), 0 if c.get('back_details_wrong') else 1)
    pick = 'v1'; c = v1
    if r1 is not None and score(r1) >= score(v1): pick, c = 'r1', r1
    path = f'N5-turn-{d}-r1/n5_{d}_r1.png' if pick == 'r1' else f'N5-turn-{d}/n5_{d}.png'
    flags = []
    if c['axes']['4'] < 4: flags.append(f"axis-4 {c['axes']['4']}: {c['reasons']['4'][:160]}")
    if c.get('back_details_wrong'): flags.append('front details drawn on the back')
    if c.get('mirrored'): flags.append('MIRRORED per judge')
    if not c.get('head_level', True): flags.append('head not level')
    sel[d] = dict(stands=pick, path=path, judge=('N5-jdg-02' if pick == 'r1' else 'N5-jdg-01'), axes=c['axes'], axis4_reason=c['reasons']['4'], flags=flags,
                  v1_axes=v1['axes'], r1_axes=(r1['axes'] if r1 else None))
out = dict(rule='R-C6-7: higher axis-4, tie → higher axis sum, tie → r1; axis-4 < 4 or back_details_wrong → FLAGGED', controls={'N5-jdg-01': 'image 5 = mirrored SE claiming SW', 'N5-jdg-02': 'image 4 = mirrored E-r1 claiming W'}, selection=sel)
json.dump(out, open(B/'runs/C-6/p2_selection.json', 'w'), indent=1)
for d, s in sel.items(): print(d, s['stands'], s['axes'], 'FLAGS' if s['flags'] else '', s['flags'])
