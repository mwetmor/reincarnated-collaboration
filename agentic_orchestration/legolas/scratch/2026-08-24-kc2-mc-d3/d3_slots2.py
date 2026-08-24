#!/usr/bin/env python3
"""D-3 STEP 4b — the SLOT MAP, done properly.

Call shape in ControllerMonster::Load (edi = this, esi = LoadTable):
      mov  dword ptr [esp], <DEFAULT imm32>     ; the engine-side default
      push <VA of the record field-name literal>
      call [vtable]                             ; LoadTable::GetFloat / GetInt / GetBool / GetString
      [ fmul dword ptr [<const>] ]              ; optional unit conversion
      [ cvttss2si ]                             ; optional float->int
      fstp/mov  dword ptr [edi + <SLOT>]        ; the controller field slot   <-- what we want

We anchor on `push <lit>` and walk forward at most 24 instructions to the FIRST store whose base
register is edi (this).  Any fmul constant seen on the way is reported: it is the unit conversion.
READ-ONLY."""
from __future__ import annotations
import json, pathlib, re, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L
import d3_binary as B
PE = L.PE
OUT = pathlib.Path(__file__).resolve().parent

LINE = re.compile(r"^([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s*\t(.*)$")


def main():
    pe = PE.PE32(PE.GD / "Game.dll")
    ts = L.template_surface()
    va2f = {}
    for r in ts:
        for va in B.find_cstr(pe, r["name"]):
            va2f[va] = r["name"]

    raw = open(OUT / "d3_ctrlmonster_load.asm").read().splitlines()
    ins = []
    for l in raw:
        m = LINE.match(l.strip())
        if m:
            ins.append((int(m.group(1), 16), m.group(3).strip()))

    def f32(va):
        off = pe.rva_to_off(va - pe.image_base)
        return struct.unpack_from("<f", pe.raw, off)[0] if off is not None else None

    out = {}
    for i, (addr, txt) in enumerate(ins):
        m = re.match(r"push\s+(0x1[0-9a-f]{7})$", txt)
        if not m:
            continue
        va = int(m.group(1), 16)
        if va not in va2f:
            continue
        fld = va2f[va]
        # default: nearest preceding `mov dword ptr [esp], imm32`
        default = None
        for j in range(i - 1, max(i - 6, -1), -1):
            d = re.match(r"mov\s+dword ptr \[esp\], (0x[0-9a-f]+|-?\d+)$", ins[j][1])
            if d:
                default = d.group(1)
                break
        conv, slot, store = None, None, None
        for j in range(i + 1, min(i + 26, len(ins))):
            t = ins[j][1]
            c = re.match(r"fmul\s+dword ptr \[(0x1[0-9a-f]{7})\]", t)
            if c:
                conv = f32(int(c.group(1), 16))
            s = re.match(r"(fstp|mov)\s+(dword|byte|word) ptr \[edi \+ (0x[0-9a-f]+)\]", t)
            if s:
                slot, store = int(s.group(3), 16), t
                break
            if re.match(r"push\s+(0x1[0-9a-f]{7})$", t) and int(t.split()[-1], 16) in va2f:
                break                       # next field started; no edi store found
        out[fld] = dict(addr=hex(addr), literal_va=hex(va), default=default,
                        conversion_mul=conv, slot=hex(slot) if slot is not None else None,
                        store=store)

    for r in ts:
        f = r["name"]
        e = out.get(f)
        if e is None:
            print(f"{f:34s}  NO PUSH-SITE IN ControllerMonster::Load")
            continue
        d = e["default"]
        try:
            if d and d.startswith("0x") and r["vtype"] == "real":
                d = f"{struct.unpack('<f', struct.pack('<I', int(d, 16)))[0]}f"
        except Exception:
            pass
        print(f"{f:34s} slot={str(e['slot']):8s} default={str(d):14s} "
              f"conv={e['conversion_mul']}  {e['store']}")
    json.dump(out, open(OUT / "d3_slots2.json", "w"), indent=2)


if __name__ == "__main__":
    main()
