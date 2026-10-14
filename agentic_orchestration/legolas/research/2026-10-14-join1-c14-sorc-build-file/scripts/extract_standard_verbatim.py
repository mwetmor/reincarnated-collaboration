#!/usr/bin/env python3
"""C-14: copy the guide's 'Standard' variant VERBATIM out of the captured d2planner data (no edits, no derived values)."""
import json, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
data = json.loads((P / "captures" / "maxroll-d2planner-gca1a0l6.data.json").read_text())
p = data["profiles"][1]
assert p["name"] == "Standard"
ids = set(p["items"].values()) | set(p["mercItems"].values()) | {x for x in p["inventory"] if x and x not in ("box", "tbk")}
for iid in list(ids):
    for s in data["items"][str(iid)].get("socketedItems", []):
        if isinstance(s, int) or (isinstance(s, str) and s.isdigit()):
            ids.add(str(s))
out = {"source": "https://planners.maxroll.gg/profiles/d2/gca1a0l6 (embedded by https://maxroll.gg/d2/guides/meteor-sorceress, tab 'Standard' = data-d2planner-set 2)",
       "profile": p, "items": {str(i): data["items"][str(i)] for i in sorted(ids, key=lambda x: int(x))}}
(P / "build_file_standard_verbatim.json").write_text(json.dumps(out, indent=1))
print(len(out["items"]), "items")
