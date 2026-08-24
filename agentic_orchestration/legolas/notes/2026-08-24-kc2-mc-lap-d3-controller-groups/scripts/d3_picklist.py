#!/usr/bin/env python3
"""D-3 STEP 5 — the PICKLIST decode.

Picklist fields are loaded as STRINGS then mapped to an integer enum by a chain of
string-compare / store pairs inside ControllerMonster::Load:

    push <default-string VA>
    push <field-name VA>
    call [vtable+0x14]                  ; LoadTable::GetString
    ... construct a std::string ...
    mov edx, <candidate literal VA>     ; the picklist token being tested
    call <string::operator==>
    test al, al ; je <next>
    mov dword ptr [edi + SLOT], <ENUM>  ; <- this token maps to this enum ordinal

We recover (token -> enum ordinal, slot) for every picklist field.  READ-ONLY."""
from __future__ import annotations
import json, pathlib, re, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L, d3_binary as B
OUT = pathlib.Path(__file__).resolve().parent

RAW = re.compile(r"^\s*([0-9a-f]{8}):\s+((?:[0-9a-f]{2} )+)\s*(.*)$")


def cstr_at(pe, va, maxlen=64):
    off = pe.rva_to_off(va - pe.image_base)
    if off is None:
        return None
    end = pe.raw.find(b"\0", off, off + maxlen)
    if end < 0:
        return None
    try:
        return pe.raw[off:end].decode("ascii")
    except Exception:
        return None


def main():
    pe = L.PE.PE32(L.PE.GD / "Game.dll")
    ts = L.template_surface()
    va2f = {}
    for r in ts:
        for va in B.find_cstr(pe, r["name"]):
            va2f[va] = r["name"]
    picklists = {r["name"] for r in ts if r["vclass"] == "picklist"}

    ins = []
    for line in open(OUT / "d3_ctrlmonster_load.asm"):
        m = RAW.match(line.rstrip("\n").replace("\t", " "))
        if m:
            ins.append((int(m.group(1), 16), " ".join(m.group(3).split())))

    res = {}
    for i, (a, t) in enumerate(ins):
        m = re.match(r"push (0x1[0-9a-f]{7})$", t)
        if not m:
            continue
        va = int(m.group(1), 16)
        f = va2f.get(va)
        if f not in picklists:
            continue
        default_va = None
        pm = re.match(r"push (0x1[0-9a-f]{7})$", ins[i - 1][1])
        if pm:
            default_va = int(pm.group(1), 16)
        mapping, slot, pending = [], None, None
        for j in range(i + 1, min(i + 90, len(ins))):
            tt = ins[j][1]
            if re.match(r"push (0x1[0-9a-f]{7})$", tt) and va2f.get(int(tt.split()[-1], 16)):
                break
            c = re.match(r"mov edx, (0x1[0-9a-f]{7})$", tt)
            if c:
                pending = cstr_at(pe, int(c.group(1), 16))
                continue
            s = re.match(r"mov dword ptr \[edi \+ (0x[0-9a-f]+)\], (0x[0-9a-f]+)$", tt)
            if s:
                slot = int(s.group(1), 16)
                mapping.append((pending, int(s.group(2), 16)))
                pending = None
                continue
            s2 = re.match(r"mov dword ptr \[edi \+ (0x[0-9a-f]+)\], eax$", tt)
            if s2:
                slot = int(s2.group(1), 16)
                mapping.append((pending, "eax(=0 on this path)"))
                pending = None
        res[f] = dict(slot=hex(slot) if slot is not None else None,
                      default_string=cstr_at(pe, default_va) if default_va else None,
                      mapping=mapping)
        print(f"\n{f}  slot={res[f]['slot']}  engine-default-string={res[f]['default_string']!r}")
        for tok, val in mapping:
            print(f"    {str(tok):28s} -> {val}")
    json.dump(res, open(OUT / "d3_picklist.json", "w"), indent=2)


if __name__ == "__main__":
    main()
