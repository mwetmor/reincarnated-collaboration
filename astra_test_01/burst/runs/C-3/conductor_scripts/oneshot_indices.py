# Conductor reading of frozen video_cut output (R-46 precedent): explicit 8 key-pose native indices for one-shot cells whose detection stopped at settle.
# Rule (R-C3-15): settle = first native index after the last detected pose where the tracked quantity is back within a FLOORED tolerance, sustained 6 samples.
import json, sys, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/artifacts')
def settle_after(start, ok, n):
    run = 0
    for i in range(start + 1, n):
        run = run + 1 if ok(i) else 0
        if run >= 6: return i - 5
    return None
res = {}
for cb in sys.argv[1:]:
    d = B/cb/'cut'; s = json.load(open(d/'series.json')); r = json.load(open(d/'registration.json')); det = r.get('detection') or {}
    kind = r['kind']; k = det.get('key_poses') or {}; base = det.get('baseline') or {}; n = len(s['head_top_y'])
    out = dict(cell=cb, kind=kind, detection_confidence=det.get('confidence'), key_poses=k, notes=det.get('notes'))
    if det.get('detection') is not None and r.get('output_frames'):
        out['status'] = 'tool_detection_ok'; res[cb] = out; continue
    H = s['H'][0] if isinstance(s['H'], list) else s['H']
    if kind == 'jump' and all(x in k for x in ('onset', 'crouch', 'take_off', 'apex', 'touchdown', 'landing_crouch')):
        hb, sb = base['head_top_y'], base['sole_y']; tol = max(3 * base.get('head_noise', 0), 0.01 * H)
        ok = lambda i: s['head_top_y'][i] is not None and s['sole_y'][i] is not None and abs(s['head_top_y'][i] - hb) <= tol and abs(s['sole_y'][i] - sb) <= 3
        st = settle_after(k['landing_crouch'], ok, n)
        if st is None:
            tail = [(abs(s['head_top_y'][i] - hb) + abs(s['sole_y'][i] - sb), i) for i in range(k['landing_crouch'] + 6, n) if s['head_top_y'][i] is not None and s['sole_y'][i] is not None]
            if tail: st = min(tail)[1]; out['settle_closest_return'] = True
        if st is not None:
            out['indices'] = [k['onset'], k['crouch'], k['take_off'], round((k['take_off'] + k['apex']) / 2), k['apex'], round((k['apex'] + k['touchdown']) / 2), k['landing_crouch'], st]
            out['settle'] = st; out['tolerance_px'] = round(tol, 2); out['status'] = 'explicit_from_series'
    elif kind == 'cast' and all(x in k for x in ('onset', 'gather', 'release')):
        tb = base.get('tip_xy'); tol = max(3 * base.get('tip_noise', 0), 0.02 * H)
        def ok(i):
            t = s['tip_xy'][i]
            return t is not None and t[0] is not None and ((t[0] - tb[0]) ** 2 + (t[1] - tb[1]) ** 2) ** 0.5 <= tol
        last = max(v for v in k.values() if isinstance(v, int)); st = k.get('settle') or settle_after(last, ok, n)
        if st is not None:
            rm = k.get('raise_mid', round((k['onset'] + k['gather']) / 2)); ft = k.get('follow_through', round((k['release'] + st) / 3 + k['release'] * 0)); 
            ret = k.get('return', round((k['release'] + st) / 2)); ft = k.get('follow_through', round((k['release'] + ret) / 2))
            out['indices'] = [k['onset'], rm, k['gather'], k['release'], ft, round((ft + ret) / 2), ret, st]
            out['settle'] = st; out['tolerance_px'] = round(tol, 2); out['status'] = 'explicit_from_series'
    if out.get('indices'):
        ix = out['indices']
        for _ in range(3):
            for j in range(len(ix) - 2, 0, -1):
                if ix[j] <= ix[j-1]: ix[j] = round((ix[j-1] + ix[j+1]) / 2)
        if ix[-1] <= ix[-2]: ix[-1] = ix[-2] + 1
        out['strictly_increasing'] = all(b > a for a, b in zip(ix, ix[1:]))
    out.setdefault('status', 'needs_contact_sheet')
    res[cb] = out
print(json.dumps(res, indent=1))
