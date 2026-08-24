#!/usr/bin/env python3
"""D-3 STEP 3 — THE BINARY. Which code READS each ControllerMonster record field.

Method (the Lap-U route-5 method, generalised):
  1. locate the field-name string literal in Game.dll (.rdata), get its VA
  2. scan .text for `push <VA>` (opcode 0x68 + imm32) — the LoadTable::GetX(name, default) call form
  3. resolve each hit to its enclosing EXPORTED symbol (nearest export at-or-below the RVA)
  4. disassemble a window around the hit to recover the DEFAULT immediate and the STORE
     displacement (`fstp [reg+disp]` / `mov [reg+disp]`) — that displacement is the controller
     field slot, which we then chase to its READERS.

A field is DECODED only if a named code path reads it and the condition is readable (GL-12).
READ-ONLY.
"""
from __future__ import annotations
import json, pathlib, re, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L
PE = L.PE
OUT = pathlib.Path(__file__).resolve().parent


def find_cstr(pe, s: str):
    """All VAs of the null-terminated ASCII literal `s` in the image."""
    b, needle = pe.raw, s.encode() + b"\0"
    out, p = [], 0
    while True:
        p = b.find(needle, p)
        if p < 0:
            break
        # require a preceding null / padding so we match the whole literal, not a suffix
        if p == 0 or b[p - 1] in (0, 0xCC) or not (32 <= b[p - 1] < 127):
            rva = pe.off_to_rva(p)
            if rva is not None:
                out.append(pe.image_base + rva)
        p += 1
    return out


def ordered_exports(pe):
    return sorted(((r, n) for n, r in pe.exports().items()))


def enclosing(ordered, rva):
    lo, hi, best = 0, len(ordered) - 1, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if ordered[mid][0] <= rva:
            best = ordered[mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def push_sites(pe, va):
    """Every `push imm32` in .text whose immediate is `va`."""
    b = pe.raw
    text = next(s for s in pe.sections if s["name"] == ".text")
    lo, hi = text["raddr"], text["raddr"] + text["rsize"]
    needle = b"\x68" + struct.pack("<I", va)
    out, p = [], lo
    while True:
        p = b.find(needle, p, hi)
        if p < 0:
            break
        rva = pe.off_to_rva(p)
        if rva is not None:
            out.append(rva)
        p += 1
    return out


def disp_sites(pe, disp):
    """Every instruction in .text carrying disp32 == `disp` in modrm mod=10 form."""
    b = pe.raw
    text = next(s for s in pe.sections if s["name"] == ".text")
    lo, hi = text["raddr"], text["raddr"] + text["rsize"]
    needle = struct.pack("<I", disp)
    out, p = [], lo
    while True:
        p = b.find(needle, p, hi)
        if p < 0:
            break
        for back in range(1, 4):
            mrm = b[p - back]
            if (mrm >> 6) == 0b10:
                rva = pe.off_to_rva(p - back)
                if rva is not None:
                    out.append(rva)
                break
        p += 1
    return sorted(set(out))


FIELDS = None


def main():
    pe = PE.PE32(PE.GD / "Game.dll")
    ordered = ordered_exports(pe)
    ts = L.template_surface()
    fields = [r["name"] for r in ts]

    res = {}
    for f in fields:
        vas = find_cstr(pe, f)
        entry = dict(field=f, literal_vas=[hex(v) for v in vas], readers=[], store_disp=None)
        for va in vas:
            for rva in push_sites(pe, va):
                sym = enclosing(ordered, rva)
                entry["readers"].append(dict(rva=hex(rva),
                                             enclosing=sym[1] if sym else None,
                                             enclosing_rva=hex(sym[0]) if sym else None))
        res[f] = entry
        print(f"{f:34s} lit={len(vas)}  readers={len(entry['readers'])}  "
              f"{sorted({r['enclosing'] for r in entry['readers']})}")

    json.dump(res, open(OUT / "d3_binary_readers.json", "w"), indent=2)
    print("\nwrote d3_binary_readers.json")


if __name__ == "__main__":
    main()
