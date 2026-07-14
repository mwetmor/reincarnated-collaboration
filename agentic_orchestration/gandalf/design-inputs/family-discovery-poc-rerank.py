import sqlite3, math
from collections import defaultdict, deque, Counter

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
NAMES = ["movement","delivery","amp","geometry","treatment","function","defense",
         "economy","proxy","range","tempo","commit","activation","dependency"]
MASK = {"unknown","blank","post-cutoff-deferred","post-cutoff"}
MINSUP = 5

con = sqlite3.connect(DB)
rows = con.execute("SELECT kit_id, cell_key FROM canon_engine_key "
                   "WHERE row_class='combat-kit' AND cell_key IS NOT NULL").fetchall()
kit_ids, kit_items, kit_vals = [], [], []
for kid, ck in rows:
    v = ck.split("|"); kit_ids.append(kid); kit_vals.append(v)
    kit_items.append(frozenset((NAMES[i], v[i]) for i in range(14) if v[i] not in MASK))
N = len(kit_items)
ext = defaultdict(set)
for k, s in enumerate(kit_items):
    for it in s: ext[it].add(k)
p_item = {it: len(e)/N for it, e in ext.items()}
freq_items = [it for it, e in ext.items() if len(e) >= MINSUP]

def closure_of_extent(E):
    it = None
    for k in E: it = kit_items[k] if it is None else (it & kit_items[k])
    return frozenset(it) if it else frozenset()
def extent_of_intent(C):
    E = None
    for it in C: E = set(ext[it]) if E is None else (E & ext[it])
    return E if E is not None else set(range(N))

c0 = closure_of_extent(set(range(N)))
seen = {c0: extent_of_intent(c0)}; work = deque([c0])
while work:
    C = work.popleft(); E = seen[C]
    for it in freq_items:
        if it in C: continue
        E2 = E & ext[it]
        if len(E2) < MINSUP: continue
        C2 = closure_of_extent(E2)
        if C2 not in seen: seen[C2] = E2; work.append(C2)
concepts = [(C, E) for C, E in seen.items()]

def coordset(C): return {c for (c, _) in C}
hist = Counter(len(coordset(C)) for C, _ in concepts)
print(f"closed frequent concepts={len(concepts)}  (minsup={MINSUP})")
print("intent-size histogram (#pinned coords -> #concepts):")
for k in sorted(hist): print(f"   {k:2d} coords : {hist[k]}")

def lift(C, E):
    prod = 1.0
    for it in C: prod *= p_item[it]
    return (len(E)/N) / prod if prod > 0 else 0.0

def show(C, E):
    ic = coordset(C)
    intent = " · ".join(f"{c}={v}" for (c, v) in sorted(C, key=lambda p: NAMES.index(p[0])))
    varies = {}
    for nm in [n for n in NAMES if n not in ic]:
        idx = NAMES.index(nm)
        vals = sorted({kit_vals[k][idx] for k in E if kit_vals[k][idx] not in MASK})
        if len(vals) > 1: varies[nm] = vals
    samp = ", ".join(sorted(kit_ids[k] for k in E)[:6])
    print(f"[{len(E):2d} kits · {len(ic)} coords · lift {lift(C,E):6.1f}]  {intent}")
    if varies: print("        varies: " + " | ".join(f"{k}{{{','.join(v)}}}" for k, v in varies.items()))
    print(f"        e.g. {samp}{' …' if len(E)>6 else ''}\n")

def novelty_top(cands, k, jac=0.55):
    shown = []
    for C, E in cands:
        if all(len(E & S)/len(E | S) <= jac for S in shown):
            show(C, E); shown.append(E)
            if len(shown) >= k: break

# RANK 1: interestingness (lift), floors support>=6 & intent>=5, novelty-deduped
print("\n============ FAMILIES BY LIFT (support>=6, intent>=5, deduped) ============\n")
cand = sorted([(C, E) for C, E in concepts if len(E) >= 6 and len(coordset(C)) >= 5],
              key=lambda ce: -lift(*ce))
novelty_top(cand, 16)

# RANK 2: biggest SPECIFIC families (intent>=6), rank by support, deduped -> the meso archetypes
print("\n============ BIGGEST SPECIFIC FAMILIES (intent>=6) by support, deduped ============\n")
cand2 = sorted([(C, E) for C, E in concepts if len(coordset(C)) >= 6 and len(E) >= 6],
               key=lambda ce: (-len(ce[1]), -len(coordset(ce[0]))))
novelty_top(cand2, 16)
