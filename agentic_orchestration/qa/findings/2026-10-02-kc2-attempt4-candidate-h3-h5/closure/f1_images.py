"""List every IC7-F-* file image in the pack, grouped by path; flag paths with >1 image (KP-213 class)."""
import json, os, sys
M = sys.argv[1]
def walk(o, out, member):
    if isinstance(o, dict):
        if str(o.get("id", "")).startswith("IC7-F-") and isinstance(o.get("value"), dict):
            v = o["value"]; out.setdefault(v.get("path"), []).append((o["id"], member, v.get("sha256", "")[:12], len(v.get("columns") or []), len(v.get("cells") or [])))
        for x in o.values(): walk(x, out, member)
    elif isinstance(o, list):
        for x in o: walk(x, out, member)
out = {}
for f in sorted(os.listdir(M)):
    if f.endswith(".json"):
        walk(json.load(open(os.path.join(M, f), encoding="utf-8")), out, f)
print("n_paths", len(out), "n_images", sum(len(v) for v in out.values()))
for p, v in sorted(out.items(), key=lambda kv: str(kv[0])):
    if len(v) > 1 or any("V311" in i[0] for i in v):
        print(p, v)
