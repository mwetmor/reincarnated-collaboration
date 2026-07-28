import importlib.util, sys
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
for p in sys.argv[1:]:
    r=R.rec(p); print("====",p)
    for k,v in sorted(r.items()):
        if v in (0,0.0,False,"",None): continue
        if isinstance(v,list) and not any(x for x in v if x not in (0,0.0,False,"")): continue
        if isinstance(v,list) and len(v)>12: v=str(v[:12])+f"...len{len(v)}"
        print(f"  {k} = {v}")
