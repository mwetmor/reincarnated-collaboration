"""jack-ryan, KC-1b delta Gate-2: blast radius of the KC-1 -> KC-1b narrowing over every corpus record.

Inputs are three outputs of `../2026-10-06-join1-b0n-gate2/jr_compile_all_records.py`, each compiled on the SAME
corpus.db (read-only) with the kit_compiler package exported by `git archive` at:
  preKC1 = ccd89e38^ · KC1 = ccd89e38 · KC1b = 4f6a8443
Reports, per pair, which records differ and in which top-level fields (element / class_dict / notes / skills /
asserts), and the element transitions.

usage: python3 jr_kc1b_blast_radius.py <compile_preKC1.json> <compile_KC1.json> <compile_KC1b.json> <out.json>
"""
import json, sys

P, K1, K1b = (json.load(open(sys.argv[i])) for i in (1, 2, 3))
out = sys.argv[4]


def delta(a, b):
    res = {}
    for k in sorted(set(a) | set(b)):
        va, vb = a.get(k), b.get(k)
        if va == vb:
            continue
        if isinstance(va, dict) and isinstance(vb, dict):
            fields = sorted(f for f in set(va) | set(vb) if va.get(f) != vb.get(f))
            ent = {"fields": fields}
            if "element" in fields:
                ent["element"] = [va.get("element"), vb.get("element")]
            if "notes" in fields:
                ent["notes_added"] = [n for n in (vb.get("notes") or []) if n not in (va.get("notes") or [])][:3]
            res[k] = ent
        else:
            res[k] = {"fields": ["<compile error on one side>"], "a": str(va)[:120], "b": str(vb)[:120]}
    return res


R = {"n_records": [len(P), len(K1), len(K1b)],
     "n_compile_errors": [sum(isinstance(v, str) for v in d.values()) for d in (P, K1, K1b)],
     "preKC1_vs_KC1": delta(P, K1), "KC1_vs_KC1b": delta(K1, K1b), "preKC1_vs_KC1b": delta(P, K1b)}
json.dump(R, open(out, "w"), indent=1, sort_keys=True)
for k in ("preKC1_vs_KC1", "KC1_vs_KC1b", "preKC1_vs_KC1b"):
    print(k, len(R[k]), {r: (e.get("element"), e["fields"]) for r, e in R[k].items()})
print("records", R["n_records"], "compile errors", R["n_compile_errors"])
