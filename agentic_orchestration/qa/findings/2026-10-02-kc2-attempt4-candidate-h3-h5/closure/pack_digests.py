"""jack-ryan H-5: independent recomputation of the v3.11 pack digests (PACK_DIGEST_LAW_V3P3), no engine import.
Members re-hashed from disk; manifest member digests compared; pack digest recomputed; cross-pin checked;
the same done on the copies the GODOT runtime vendors (if a path is given)."""
import hashlib, json, os, sys

def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def check(root):
    man = json.load(open(os.path.join(root, "manifest.json"), encoding="utf-8"))
    mem = man["members"]
    rows = mem if isinstance(mem, list) else [{"path": k, **(v if isinstance(v, dict) else {"sha256": v})} for k, v in mem.items()]
    bad, lines = [], []
    for r in rows:
        p, want = r["path"], r["sha256"]
        got = sha(os.path.join(root, p))
        if got != want:
            bad.append((p, want, got))
        lines.append((p, want))
    on_disk = sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs if f != "manifest.json")
    listed = sorted(p for p, _ in lines)
    digest = hashlib.sha256("\n".join(f"{p}  {s}" for p, s in sorted(lines)).encode("utf-8")).hexdigest()
    return {"root": os.path.basename(root), "n_members": len(lines), "member_mismatches": bad,
            "unlisted_files": sorted(set(on_disk) - set(listed)), "missing_files": sorted(set(listed) - set(on_disk)),
            "recomputed_pack_digest": digest, "manifest_pack_digest": man["pack_digest"],
            "agrees": digest == man["pack_digest"], "cross_pin": man.get("cross_pin")}

out = {}
for root in sys.argv[1:]:
    out[root] = check(root)
for root, r in out.items():
    print(json.dumps({k: v for k, v in r.items()}, indent=1, ensure_ascii=False, default=str))
