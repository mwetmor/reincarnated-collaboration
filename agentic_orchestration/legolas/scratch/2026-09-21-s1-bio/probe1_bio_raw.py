#!/usr/bin/env python3
"""S-1 probe 1: dump character_bio as RAW 32-bit words, both interpretations,
for every sample. READ-ONLY."""
import struct
import gdcg7 as G

def dump(path):
    r, bid, blen, end = G.parse(path, stop_before="character_bio")
    ver = r.read_int()
    words = []
    while r.p + 4 <= end:
        off = r.p
        raw = r.d[r.p:r.p+4]
        v = struct.unpack("<I", raw)[0] ^ r.key
        r.p += 4
        r._advance(raw)
        f = struct.unpack("<f", struct.pack("<I", v & 0xFFFFFFFF))[0]
        words.append((off, v & 0xFFFFFFFF, f))
    return ver, blen, words, end - r.p

for path in [l.strip() for l in open("samples.txt") if l.strip()]:
    print("="*104)
    print(path.split("/legolas/")[-1])
    try:
        ver, blen, words, tail = dump(path)
    except Exception as e:
        print("  FAILED:", type(e).__name__, e); continue
    print(f"  block_len={blen}  version={ver}  words={len(words)}  tail_bytes={tail}")
    for i,(off,v,f) in enumerate(words):
        fs = f"{f:.6g}" if abs(f) < 1e12 and (f==f) else repr(f)
        print(f"    [{i:2d}] 0x{off:06x}  u32={v:>12d}  0x{v:08x}  f32={fs}")
