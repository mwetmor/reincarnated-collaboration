#!/usr/bin/env python3
"""
NON-PRODUCTION SCRATCH — KIT-CAL-1 phase P-2 / G-4 (gandalf sub-agent, 2026-07-28).

Read-only probe of the Edition-II .arz corpus for the werewolf kit spec:
  - Fangs-of-Asterkarn werewolf transform record(s) -> skill-exclusion / conversion machinery
  - claws AoE radius / arc parameters
  - Onslaught record (augment-vs-replacement determination)
  - spawn/proxy density priors for the leveling zones

Reuses legolas's PROVEN TQIT parser from
  agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py
(imported, not reimplemented). Nothing is written outside this scratch dir.

Usage: python3 g4_arz_probe.py <subcommand> [args]
"""
import sys
import json
import pathlib
import importlib.util

REPO = pathlib.Path(__file__).resolve().parents[3]
ADAPTER = REPO / "research" / "scripts" / "gd_arz_adapter_2026_07_24.py"
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")

ARCHIVES = {
    "database": VENDOR / "database" / "database.arz",
    "GDX1": VENDOR / "gdx1" / "database" / "GDX1.arz",
    "GDX2": VENDOR / "gdx2" / "database" / "GDX2.arz",
    "GDX3": VENDOR / "gdx3" / "database" / "GDX3.arz",
}


def _load_adapter():
    spec = importlib.util.spec_from_file_location("gd_arz_adapter", ADAPTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ADP = _load_adapter()
_CACHE = {}


def arc(name):
    if name not in _CACHE:
        _CACHE[name] = ADP.ArzArchive(ARCHIVES[name])
    return _CACHE[name]


def find(pattern, archives=None):
    """List record paths containing pattern (case-insensitive)."""
    out = []
    for a in (archives or ARCHIVES):
        for p in arc(a).records:
            if pattern.lower() in p.lower():
                out.append((a, p, arc(a).records[p]["rtype"]))
    return out


def dump(archive, path):
    a = arc(archive)
    rec = a.read_record(path)
    return rec


def main():
    cmd = sys.argv[1]
    if cmd == "find":
        pat = sys.argv[2]
        archives = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        for a, p, t in find(pat, archives):
            print(f"{a}\t{t}\t{p}")
    elif cmd == "dump":
        rec = dump(sys.argv[2], sys.argv[3])
        for k in sorted(rec):
            v = rec[k]
            if isinstance(v, list) and len(v) > 30:
                print(f"{k} = [{len(v)}] {v[:6]} ... {v[-3:]}")
            else:
                print(f"{k} = {v}")
    elif cmd == "dumpjson":
        print(json.dumps(dump(sys.argv[2], sys.argv[3]), indent=1, default=str))
    elif cmd == "grepfield":
        # find records in an archive whose field set contains a given field name
        a, field = sys.argv[2], sys.argv[3]
        pat = sys.argv[4] if len(sys.argv) > 4 else ""
        A = arc(a)
        for p in A.records:
            if pat and pat.lower() not in p.lower():
                continue
            try:
                rec = A.read_record(p)
            except Exception:
                continue
            if field in rec:
                print(f"{p}\t{field}={rec[field]}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()


def dumpnz(archive, path):
    """Print only fields whose value is not the 'zero' default (0, 0.0, False, '')."""
    rec = dump(archive, path)
    def nz(v):
        if isinstance(v, list):
            return any(nz(x) for x in v)
        return not (v == 0 or v is False or v == "")
    return {k: v for k, v in rec.items() if nz(v)}
