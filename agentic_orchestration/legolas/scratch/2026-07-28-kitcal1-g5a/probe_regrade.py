import importlib.util, pathlib, sys, json, re
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)

T = R.tags()
q = sys.argv[1] if len(sys.argv)>1 else "Thundersnout"
hits = [(k,v) for k,v in T.items() if q.lower() in str(v).lower()]
for k,v in hits[:40]: print("TAG", k, "=", v)
