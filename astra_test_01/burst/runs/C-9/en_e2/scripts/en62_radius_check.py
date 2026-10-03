# EN-E2: the KP-256 radius check (KC2 ledger KP-256 / KP-269). Drawn half-width of the body in a pack's IDLE cells (every heading,
# every idle frame: the widest alpha column distance from the anchor x = 384, in metres at ppm_render 151.337) against each roster
# record's actor radius (roster.json radius_x_scale = actorRadius x scale), both at the record's TRUE size (drawn x true_size factor).
# KP-269 guidance: GD draws bodies wider than their collision circle; a ratio consistent with the footage (~1-2.5x) passes, a
# gross disagreement is flagged for a ruling. Bands (EN-E2's own, not KC2's): PASS 0.6-2.5x; FLAG-narrow < 0.6; FLAG-wide > 2.5. python3 scripts/en62_radius_check.py <pack_dir> <type_id> [--json out]
import json, os, sys, glob
import numpy as np
from PIL import Image
PACK, TID = sys.argv[1], sys.argv[2]; PPM = 151.33680669505316
R = json.load(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-02-crucible-enemy-roster-packet/roster.json'))
t = [x for x in R['types'] if x['type_id'] == TID][0]
idx = json.load(open(os.path.join(PACK, 'matrix_index.json'))); K = os.path.basename(PACK.rstrip('/'))
kit = json.load(open(os.path.join(os.path.dirname(os.path.dirname(PACK.rstrip('/'))), 'join1_render/kits/%s.json' % K)))
ts = kit.get('true_size', {}); fac = {k: v.get('factor', 1.0) for k, v in ts.get('records', {}).items()}
half = []
for f in sorted(glob.glob(os.path.join(PACK, 'cells/idle/*/*.png'))):
    a = np.asarray(Image.open(f))[..., 3] > 0
    xs = np.nonzero(a.any(0))[0]
    if len(xs): half.append(max(384 - xs.min(), xs.max() - 384) / PPM)
drawn = float(np.median(half)); out = dict(pack=K, type_id=TID, drawn_half_width_m_median=round(drawn, 4), drawn_half_width_m_max=round(max(half), 4), records={})
for m in t['members_detail']:
    rec = os.path.basename(m['record']).replace('.dbr', ''); rad = m['actorRadius_m'] * m['scale']
    f = next((v for k, v in fac.items() if rec in k.split(' (')[0].split('/') or rec + '.dbr' in k), 1.0)
    ratio = drawn * f / rad; out['records'][rec] = dict(role=m.get('role'), radius_x_scale_m=round(rad, 3), true_size_factor=f, drawn_at_true_m=round(drawn * f, 3),
                                                         ratio=round(ratio, 2), verdict='PASS' if 0.6 <= ratio <= 2.5 else ('FLAG-narrow' if ratio < 0.6 else 'FLAG-wide'))
print('RADIUS', K, 'drawn half-width median %.3f m (max %.3f)' % (drawn, max(half)), {k: (v['radius_x_scale_m'], v['ratio'], v['verdict']) for k, v in out['records'].items()})
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
