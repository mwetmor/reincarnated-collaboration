#!/usr/bin/env python3
"""kc2set v2 — re-emit of kc2set_verdicts.json with BASENAME RE-RESOLUTION for every
ABSENT-BOTH row (Discipline #70 founding instance 4: the v1 artefact carried stale
path-guesses that jack-ryan re-resolved by hand at L-62(d)).

Equality predicate DECLARED at the verdict site (Discipline #69 clause (i)):
  IDENTICAL        = same field set AND same normalised values AND same owner-archive list
  IDENTICAL-FIELDS = same field set AND same normalised values, DIFFERENT owner list
  CHANGED / ONLY-II / ONLY-III / ABSENT-BOTH as per lib2.diff_rec.
READ-ONLY. Trees: GD-Edition-II 20260724 and GD-Edition-III 20260808.
"""
import json, sys, collections
sys.path.insert(0,".")
import lib2
E2,E3=lib2.E2,lib2.E3
src=json.load(open("kc2set_verdicts.json"))

def resolve(p):
    """If p is absent from both indices, try a unique basename match. -> (path, how)"""
    lp=p.lower()
    if lp in E2.idx or lp in E3.idx: return p, "as-given"
    base="/"+p.split("/")[-1].lower()
    c2=[q for q in E2.idx if q.endswith(base)]
    c3=[q for q in E3.idx if q.endswith(base)]
    cand=sorted(set(c2)|set(c3))
    if len(cand)==1: return cand[0], "basename-resolved"
    if len(cand)>1: return p, f"AMBIGUOUS-{len(cand)}"
    return p, "genuinely-absent"

out=collections.OrderedDict()
stats=collections.Counter(); repairs=[]
for group, rows in src.items():
    newrows=[]
    for row in rows:
        p, old = row[0], row[1]
        rp, how = resolve(p)
        verdict, _ = lib2.diff_rec(rp)
        if how=="basename-resolved":
            repairs.append((p, rp, old, verdict))
        newrows.append({"path_as_given": p, "path_resolved": rp,
                        "resolution": how, "verdict_v1": old, "verdict": verdict})
        stats[verdict]+=1
    out[group]=newrows

meta={"emitted":"2026-08-08 legolas consolidated record touch (item 7 re-emit)",
      "supersedes":"kc2set_verdicts.json (STALE: unresolved path-guesses reported ABSENT-BOTH)",
      "equality_predicate":{"IDENTICAL":"same fields + same normalised values + same owner list",
                            "IDENTICAL-FIELDS":"same fields + same values, different owner list",
                            "CHANGED":"field added/removed or value differs",
                            "ABSENT-BOTH":"record absent from both trees after basename re-resolution"},
      "trees":{"II":str(lib2.ROOTS['II']),"III":str(lib2.ROOTS['III'])},
      "verdict_counts":dict(stats),
      "repairs_vs_v1":[{"as_given":a,"resolved":b,"v1":c,"v2":d} for a,b,c,d in repairs]}
json.dump({"_meta":meta, **out}, open("kc2set_verdicts_v2.json","w"), indent=1)
print("verdict counts:", dict(stats))
print(f"\nrows repaired by basename resolution: {len(repairs)}")
for a,b,c,d in repairs: print(f"   {a}\n      -> {b}\n      v1={c}  v2={d}")
grp="(2b) summon bodies (crabling/spikeshell/archer/apparition)"
n=len(out[grp]); ident=sum(1 for r in out[grp] if r["verdict"].startswith("IDENTICAL"))
print(f"\nSUMMON-BODY GROUP: {ident}/{n} IDENTICAL   <-- the note's 15/15 claim")
