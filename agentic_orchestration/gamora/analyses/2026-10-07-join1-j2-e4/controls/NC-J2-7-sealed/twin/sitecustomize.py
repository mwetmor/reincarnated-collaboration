# NON-GRADED-CONTROL sealed twin (E4): in-memory perturbation of the SEALED oracle, at site time
import dataclasses, importlib, json
_S = json.loads('{"attr": [["secondary_streams", "SOULFIRE_PERIOD_S", 0.2]]}')
K = 'reincarnated.simulation.kc2.'
for name, val in _S.get('cited', []):
    fx = importlib.import_module(K + 'fixture'); object.__setattr__(getattr(fx, name), 'value', val)
for mod, name, val in _S.get('attr', []):
    setattr(importlib.import_module(K + mod), name, val)
for mod, name, key, val in _S.get('dictitem', []):
    m = importlib.import_module(K + mod); d = dict(getattr(m, name)); d[key] = val; setattr(m, name, d)
for mod, name, key, delta in _S.get('dictitem_delta', []):
    m = importlib.import_module(K + mod); d = dict(getattr(m, name)); d[key] = d[key] + delta; setattr(m, name, d)
for mod, cls, meth in _S.get('method_none', []):
    c = getattr(importlib.import_module(K + mod), cls)
    def _none(self, *a, **k):
        return None
    setattr(c, meth, _none)
if _S.get('board_delta'):
    w, col, delta = _S['board_delta']
    po = importlib.import_module(K + 'player_offense'); so = importlib.import_module(K + 'summon_offense')
    m = po._load_mitigation()
    for k in [k for k in m if k[1] == w]:
        m[k] = dataclasses.replace(m[k], **{col + '_pct': getattr(m[k], col + '_pct') + delta})
    b = so._full_board()
    for k in [k for k in b if k[1] == w]:
        b[k][col] = repr(float(b[k][col]) + delta)
