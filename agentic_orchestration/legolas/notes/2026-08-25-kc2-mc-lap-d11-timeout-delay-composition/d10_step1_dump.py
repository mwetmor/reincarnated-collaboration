"""D-10 step 1 — bounded disassembly of a named export or RVA. READ-ONLY.
Usage: python3 d10_step1_dump.py <symbol-or-0xRVA> [maxn]
Bounded by the next exported RVA (d8_lib convention), so a listing cannot leak into a neighbour."""
import sys; sys.path.insert(0, '.')
import d4b_dis as D
import d8_lib as B

for tgt in sys.argv[1:]:
    if tgt.isdigit():
        continue
    rva = int(tgt, 16) if tgt.startswith('0x') else D.EX[tgt]
    print(f'=== {tgt}  @ RVA {rva:#010x}  (nearest={D.nearest(rva)})')
    for l in B.bounded(rva, 400):
        print(l)
    print()
