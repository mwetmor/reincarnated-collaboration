#!/usr/bin/env python3
"""F-12a — Crucible arena geometry probe. Parse the survivalworld_*.map files for entity
placements. Strategy: locate every length-prefixed DBR path string, then read the float triple
that precedes it (empirically established from the header layout). READ-ONLY."""
import pathlib, struct, re, collections, sys, math

MAPS = sorted(pathlib.Path("maps").rglob("*.map"))
DBR = re.compile(rb"records/[a-z0-9_/&'\. \-]+?\.dbr")

def le_u32(b, o): return struct.unpack_from("<I", b, o)[0]
def le_f32(b, o): return struct.unpack_from("<f", b, o)[0]

def strings(buf):
    """Yield (offset_of_length_field, path) for every length-prefixed DBR path."""
    for m in DBR.finditer(buf):
        s, e = m.start(), m.end()
        if s < 4: continue
        n = le_u32(buf, s - 4)
        if n == e - s:
            yield s - 4, buf[s:e].decode("ascii", "replace")

def plausible(f):
    return (f == 0.0) or (1e-4 < abs(f) < 1e6)

def probe(p):
    buf = p.read_bytes()
    ents = list(strings(buf))
    counts = collections.Counter(path for _, path in ents)
    return buf, ents, counts

print(f"{'map':34s} {'bytes':>10s} {'dbr-refs':>9s} {'distinct':>9s}")
ALL = {}
for p in MAPS:
    buf, ents, counts = probe(p)
    ALL[str(p)] = (buf, ents, counts)
    print(f"{str(p):34s} {len(buf):>10,d} {len(ents):>9,d} {len(counts):>9,d}")

# ── which maps carry the Crucible spawn points? ───────────────────────────────────────────────
print("\n=== spawnpoint / playerspawnpoint references per map ===")
for k, (buf, ents, counts) in ALL.items():
    hits = {c: n for c, n in counts.items() if "spawnpoint" in c or "patrolpoint" in c}
    if hits:
        print(f"  {k}")
        for c, n in sorted(hits.items()): print(f"      {n:4d} x {c}")

# ── float-triple extraction around a named entity ─────────────────────────────────────────────
def triples_near(buf, off, back=64, fwd=64):
    """Return candidate (x,y,z) float triples in a window around a string's length field."""
    out = []
    for o in range(max(0, off - back), min(len(buf) - 12, off + fwd)):
        x, y, z = le_f32(buf, o), le_f32(buf, o + 4), le_f32(buf, o + 8)
        if all(plausible(v) for v in (x, y, z)) and 0 < abs(y) < 500 and abs(x) < 5000 and abs(z) < 5000:
            out.append((o - off, round(x, 3), round(y, 3), round(z, 3)))
    return out

TARGET = "spawnpoint"
print(f"\n=== float-triple windows around '{TARGET}' refs (first map that has them) ===")
for k, (buf, ents, counts) in ALL.items():
    sel = [(o, c) for o, c in ents if TARGET in c]
    if not sel: continue
    print(f"\n--- {k}  ({len(sel)} refs) ---")
    for o, c in sel[:8]:
        tr = triples_near(buf, o)
        print(f"  @0x{o:08x}  {c}")
        for d, x, y, z in tr[:6]:
            print(f"        d={d:+4d}  ({x:9.3f}, {y:8.3f}, {z:9.3f})")
    break
