#!/usr/bin/env python3
"""D-3 STEP 4 — the SLOT MAP.  Disassemble ControllerMonster::Load, pair each field-name push
with the store displacement that follows it, then enumerate every OTHER site in .text that
touches that displacement — those are the field's CONSUMERS, i.e. the semantics.  READ-ONLY."""
from __future__ import annotations
import json, pathlib, re, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L
import d3_binary as B
PE = L.PE
OUT = pathlib.Path(__file__).resolve().parent


def main():
    pe = PE.PE32(PE.GD / "Game.dll")
    ordered = B.ordered_exports(pe)
    exp = pe.exports()
    load_rva = exp["?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z"]
    # find the end: next export after it
    nxt = min((r for r in (v for v in exp.values()) if r > load_rva), default=load_rva + 0x2000)
    n = min(nxt - load_rva, 0x4000)
    txt = pe.disasm(load_rva, n)
    open(OUT / "d3_ctrlmonster_load.asm", "w").write(txt)
    print(f"ControllerMonster::Load @ {load_rva:#x}  len={n:#x}  lines={txt.count(chr(10))}")

    # literal VA -> field name
    ts = L.template_surface()
    va2f = {}
    for r in ts:
        for va in B.find_cstr(pe, r["name"]):
            va2f[va] = r["name"]

    lines = [l for l in txt.splitlines() if re.match(r"\s*[0-9a-f]+:", l)]
    slots, pending = {}, None
    for l in lines:
        m = re.search(r"push\s+\$?(0x1[0-9a-f]{7})", l)
        if m and int(m.group(1), 16) in va2f:
            pending = va2f[int(m.group(1), 16)]
            continue
        if pending:
            s = re.search(r"(fstp|mov)\s+.*?\[%?e?[a-z]{2}\s*[+\-]\s*(0x[0-9a-f]+)\]", l)
            if not s:
                s = re.search(r"(fstp|mov)\s+(?:DWORD PTR|BYTE PTR|WORD PTR)?\s*\[e?[a-z]{2}\+(0x[0-9a-f]+)\]", l)
            if s:
                slots[pending] = int(s.group(2), 16)
                pending = None
    print(f"\nslots recovered: {len(slots)} / {len(ts)}")
    for k, v in slots.items():
        print(f"  {k:34s} +{v:#06x}")
    json.dump({k: hex(v) for k, v in slots.items()}, open(OUT / "d3_slots.json", "w"), indent=2)


if __name__ == "__main__":
    main()
