# NON-GRADED-CONTROL displacer: the witness recorder in every process EXCEPT the named cell
import importlib.util, os, sys
_t = os.environ.get('BPRIME_DISPLACE_CELL'); _a = sys.argv; _skip = False
if _t and '--cell' in _a:
    _i = _a.index('--cell'); _skip = (_a[_i + 1] + ':' + _a[_i + 2]) == _t
if not _skip:
    _s = importlib.util.spec_from_file_location('_join2_bprime_witness_lib', '/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/join2_bprime_witness_hook_v2/sitecustomize.py')
    _m = importlib.util.module_from_spec(_s); sys.modules[_s.name] = _m; _s.loader.exec_module(_m)
    _m.install_recorder(os.environ['BPRIME_WITNESS_DIR'])
