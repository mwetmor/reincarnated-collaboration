"""READ-ONLY Game.dll (Ed IV, 32-bit) disassembly helper for the AI-movement decode.
Builds on the range-audit harness (d4b_pe / d4b_dis); adds string-literal annotation for
immediate operands that point into .rdata, and export-bounded listings."""
import bisect
import re
import struct
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "research/2026-10-01-kc2-enemy-range-audit/scripts")
import d4b_dis as D  # noqa: E402

pe, EX, IB = D.pe, D.EX, D.IB


def cstr_at(rva, maxlen=80):
    b = pe.at(rva, maxlen)
    if not b:
        return None
    e = b.find(b"\0")
    if e <= 1:
        # try UTF-16
        try:
            s = pe.at(rva, maxlen * 2).decode("utf-16-le").split("\0")[0]
            if len(s) >= 2 and all(32 <= ord(c) < 127 for c in s):
                return 'L"' + s + '"'
        except Exception:
            pass
        return None
    s = b[:e]
    if all(32 <= c < 127 for c in s):
        return '"' + s.decode() + '"'
    return None


def annotate(ins):
    ann = ""
    if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
        t = int(ins.op_str, 16) - IB
        s = D.nearest(t)
        if s:
            ann = f"   ; -> {s}"
        return ann
    for m in re.finditer(r"0x[0-9a-f]{8}", ins.op_str):
        t = int(m.group(0), 16) - IB
        if D.in_const_sec(t):
            st = cstr_at(t)
            if st:
                ann += f"   ; {st}"
            else:
                c = D.const_at(t)
                s = D.sym(t)
                ann += f'   ; {"[" + s + "] " if s else ""}{c or ""}'
    return ann


def bounded(name_or_rva, maxn=1500):
    rva = EX[name_or_rva] if isinstance(name_or_rva, str) else name_or_rva
    i = bisect.bisect_right(D.SORTED_RVA, rva)
    end = D.SORTED_RVA[i] if i < len(D.SORTED_RVA) else rva + 0x400
    code = pe.at(rva, min(end - rva, maxn * 8))
    out = []
    for ins in D.md.disasm(code, IB + rva):
        r = ins.address - IB
        if r >= end:
            break
        out.append(f"  {r:#010x}  {ins.mnemonic:<8} {ins.op_str}{annotate(ins)}")
    return out


def find(pat):
    rx = re.compile(pat)
    return sorted((r, n) for n, r in EX.items() if rx.search(n))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "find":
        for r, n in find(sys.argv[2]):
            print(f"{r:#010x}  {n}")
    elif cmd == "dis":
        tgt = sys.argv[2]
        if tgt.startswith("0x"):
            tgt = int(tgt, 16)
        print(f"=== {tgt} ===")
        print("\n".join(bounded(tgt)))
