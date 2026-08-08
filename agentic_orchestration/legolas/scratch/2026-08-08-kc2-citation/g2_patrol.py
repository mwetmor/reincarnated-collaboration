#!/usr/bin/env python3
"""F-12a — parse the inline PatrolPoint placement block at the head of every survivalworld_*.map.
Layout is auto-detected rather than assumed: find the group header, then walk
[uid][u32 len][path][uid][f32 x][f32 y][f32 z] with the uid width solved empirically. READ-ONLY."""
import pathlib, struct, math, json, collections, csv

def u32(b, o): return struct.unpack_from("<I", b, o)[0]
def f32(b, o): return struct.unpack_from("<f", b, o)[0]

def pstr(b, o):
    """length-prefixed ascii string at o -> (text, offset_after)"""
    n = u32(b, o)
    if n > 4096: return None, o
    return b[o + 4:o + 4 + n].decode("ascii", "replace"), o + 4 + n

def parse_group(b):
    """Header: ... [pstr group_key][pstr group_label][u32 count] then count entries."""
    # locate 'PatrolPoint_Attack' as a length-prefixed string
    tag = b"PatrolPoint_Attack"
    i = b.find(tag)
    if i < 0 or u32(b, i - 4) != len(tag): return None
    o = i + len(tag)
    label, o = pstr(b, o)
    n = u32(b, o); o += 4
    if not (0 < n < 512): return None
    return dict(key="PatrolPoint_Attack", label=label, count=n, off=o)

def walk(b, o, n):
    """Auto-detect the uid width: try widths, keep the one that yields n consistent entries."""
    for W1 in range(0, 33):
        for W2 in range(0, 33):
            p = o
            out, ok = [], True
            for _ in range(n):
                try:
                    p += W1                      # per-entry uid PRECEDES the length field
                    L = u32(b, p)
                    if not (8 <= L <= 512): ok = False; break
                    path = b[p + 4:p + 4 + L].decode("ascii", "replace")
                    if not path.startswith("records/") or not path.endswith(".dbr"):
                        ok = False; break
                    q = p + 4 + L + W2
                    x, y, z = f32(b, q), f32(b, q + 4), f32(b, q + 8)
                    if not all(abs(v) < 1e5 for v in (x, y, z)): ok = False; break
                    out.append((path, x, y, z))
                    p = q + 12
                except Exception:
                    ok = False; break
            if ok and len(out) == n:
                return W1, W2, out, p
    return None, None, None, None

rows = []
for p in sorted(pathlib.Path("maps").rglob("*.map")):
    b = p.read_bytes()
    g = parse_group(b)
    if not g:
        print(f"{str(p):34s}  no PatrolPoint_Attack group"); continue
    W1, W2, ents, end = walk(b, g["off"], g["count"])
    if ents is None:
        print(f"{str(p):34s}  group found (n={g['count']}) but layout not solved"); continue
    xs = [e[1] for e in ents]; ys = [e[2] for e in ents]; zs = [e[3] for e in ents]
    cx, cz = sum(xs) / len(xs), sum(zs) / len(zs)
    rad = [math.hypot(e[1] - cx, e[3] - cz) for e in ents]
    span = math.hypot(max(xs) - min(xs), max(zs) - min(zs))
    print(f"\n=== {p}  group='{g['label']}' n={g['count']} uid_pre={W1} uid_post={W2} ===")
    for i, (path, x, y, z) in enumerate(ents):
        print(f"   [{i:2d}] {path.split('/')[-1]:22s} ({x:9.3f}, {y:8.3f}, {z:9.3f})  r={rad[i]:7.3f}")
    print(f"   centroid=({cx:.3f}, {cz:.3f})  y {min(ys):.2f}..{max(ys):.2f}")
    print(f"   radius  min={min(rad):.3f}  mean={sum(rad)/len(rad):.3f}  max={max(rad):.3f}")
    print(f"   bbox X {min(xs):.2f}..{max(xs):.2f} ({max(xs)-min(xs):.2f})  "
          f"Z {min(zs):.2f}..{max(zs):.2f} ({max(zs)-min(zs):.2f})  diag={span:.2f}")
    for i, (path, x, y, z) in enumerate(ents):
        rows.append(dict(arena_map=p.name, arena_archive=p.parent.name, group=g["label"],
                         idx=i, record=path, x=round(x, 4), y=round(y, 4), z=round(z, 4),
                         r_from_centroid=round(rad[i], 4),
                         centroid_x=round(cx, 4), centroid_z=round(cz, 4)))

if rows:
    with open("kc2_crucible_patrolpoints.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"\n[wrote] kc2_crucible_patrolpoints.csv  {len(rows)} rows")
