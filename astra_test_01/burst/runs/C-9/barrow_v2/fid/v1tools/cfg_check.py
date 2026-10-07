#!/usr/bin/env python3
"""BV2F paint-cfg check (lane PT, Gate-2 W-2(a)). The frozen driver calls this BEFORE staging any chunk.
    python3 cfg_check.py <cfg.json>      exit 0 = ok; exit 1 = HALT (printed reason)
  rules == v1 rules with DEV12_substitutions.json applied (exact string equality)
  refs  == v1 refs + DEV11_refs.json extra_refs (exact list equality, v1's first, in order)
v1 = tierA/conductor_scripts/cfg_t10bf.json (sha-checked against SHA256SUMS first)."""
import hashlib, json, os, sys
V = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(V, "tierA", "conductor_scripts", "cfg_t10bf.json")
want = [l.split()[0] for l in open(os.path.join(V, "SHA256SUMS")) if l.strip().endswith("./tierA/conductor_scripts/cfg_t10bf.json")]
got = hashlib.sha256(open(V1, "rb").read()).hexdigest()
if not want or want[0] != got:
    sys.exit("[cfg_check] HALT: frozen v1 cfg sha mismatch")
v1 = json.load(open(V1))
cfg = json.load(open(sys.argv[1]))
subs = json.load(open(os.path.join(V, "DEV12_substitutions.json")))["substitutions"]
extra = json.load(open(os.path.join(V, "DEV11_refs.json")))["extra_refs"]
rules = v1["rules"]
for s in subs:
    old, new = s["v1"], s["v2"]
    if old not in rules:
        sys.exit("[cfg_check] HALT: DEV-12 entry %r is not in v1's rules" % old)
    rules = rules.replace(old, new)
fail = []
if cfg.get("rules") != rules:
    a, b = cfg.get("rules") or "", rules
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    fail.append("rules != v1 rules + DEV-12 table (first difference at char %d: cfg %r vs expected %r)" % (i, a[i:i + 60], b[i:i + 60]))
if cfg.get("refs") != v1["refs"] + extra:
    fail.append("refs != v1 refs + DEV-11 entries (cfg has %d, expected %d)" % (len(cfg.get("refs") or []), len(v1["refs"]) + len(extra)))
if fail:
    for f in fail:
        print("[cfg_check] HALT:", f)
    sys.exit(1)
print("[cfg_check] OK: rules = v1 + %d DEV-12 substitutions; refs = v1 (%d) + %d DEV-11" % (len(subs), len(v1["refs"]), len(extra)))
