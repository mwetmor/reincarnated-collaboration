"""jack-ryan H-3 RUNS: compare my G3 re-run (oracle trace + port summary) per cell against drax's filed KP-261 evidence.
Usage: cmp_cells.py <my_out_dir> <filed_evidence_dir> ARM:salt[,ARM:salt...]
Trace: byte sha + equality with composition.engine_src blanked (the only path-bearing field).
Summary: byte sha + equality with trace_sha256 blanked (it hashes the trace, so inherits the engine_src path)."""
import json, sys, gzip, hashlib
mine, filed, cells = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
rows = []
for c in cells:
    arm, s = c.split(':')
    mt = open(f'{mine}/oracle_traces/{arm}_s{s}.json', 'rb').read()
    ft = gzip.open(f'{filed}/oracle_traces/{arm}_s{s}.json.gz').read()
    a, b = json.loads(mt), json.loads(ft)
    a['composition']['engine_src'] = b['composition']['engine_src'] = None
    ms = open(f'{mine}/summaries/{arm}_s{s}.json', 'rb').read()
    fs = open(f'{filed}/summaries/{arm}_s{s}.json', 'rb').read()
    x, y = json.loads(ms), json.loads(fs)
    diff_keys = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
    x2, y2 = dict(x), dict(y)
    x2.pop('trace_sha256', None); y2.pop('trace_sha256', None)
    cs = x.get('contact_solver') or {}
    rows.append({
        'cell': f'{arm}|{s}',
        'trace_mine_sha256': hashlib.sha256(mt).hexdigest(), 'trace_filed_sha256': hashlib.sha256(ft).hexdigest(),
        'trace_byte_equal': mt == ft, 'trace_equal_mod_engine_src': a == b,
        'summary_mine_sha256': hashlib.sha256(ms).hexdigest(), 'summary_filed_sha256': hashlib.sha256(fs).hexdigest(),
        'summary_byte_equal': ms == fs, 'summary_equal_mod_trace_sha': x2 == y2, 'summary_differing_keys': diff_keys,
        'decision_divergences': x.get('decision_divergences'), 'draw_mismatches': x.get('draw_mismatches'),
        'death': x.get('death'), 'oracle_complete': (x.get('oracle_complete') or {}).get('complete') if isinstance(x.get('oracle_complete'), dict) else x.get('oracle_complete'),
        'census_equal': x.get('census_equal'), 'control_term_equal': (x.get('control_term') or {}).get('equal'),
        'contact': {k: cs.get(k) for k in ('contact_solver', 'native_lib_sha256', 'shadow_ticks_compared', 'shadow_mismatch_ticks',
                    'place_shadow_calls', 'place_shadow_mismatch_calls', 'petpath_shadow_calls',
                    'petpath_shadow_mismatch_calls', 'petpath_shadow_goal_hits')},
        'injected': x.get('injected'), 'port_only_streams': x.get('port_only_streams'),
    })
print(json.dumps(rows, indent=1))
