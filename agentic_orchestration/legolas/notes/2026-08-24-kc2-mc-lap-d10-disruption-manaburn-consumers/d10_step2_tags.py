"""D-10 step 2 — resolve the DBR field-name string literals returned by every `GetLoad*Tag` /
`GetDisplayTag` on the named attribute classes.  Each body is `mov eax, <rdata VA>; ret`, so the
returned C-string is read directly out of the image.  This is the record-field join, DECODED from
the consumer rather than guessed from a column header.  READ-ONLY."""
import sys, re; sys.path.insert(0, '.')
import d4b_dis as D
import d8_lib as B

pats = sys.argv[1:] or ['Disruption', 'ManaBurn', 'Convert', 'Confusion', 'Stun']
for p in pats:
    print(f'######## {p}')
    for n in sorted(D.EX):
        if p not in n:
            continue
        if not re.match(r'\?(GetLoad\w*Tag|GetDisplayTag|GetType|GetDamageRatio)@', n):
            continue
        rva = D.EX[n]
        lines = B.bounded(rva, 12)
        s = None
        for l in lines:
            m = re.search(r'mov\s+eax, (0x[0-9a-f]+)', l)
            if m:
                t = int(m.group(1), 16) - D.IB
                try:
                    v = D.pe.cstr(t)
                    if v.isprintable() and 1 <= len(v) < 80:
                        s = v
                        break
                except Exception:
                    pass
        # GetType bodies return a small immediate
        imm = None
        for l in lines:
            m = re.search(r'mov\s+eax, (\d+)$', l.strip())
            if m:
                imm = int(m.group(1))
                break
        print(f'  {rva:#010x}  {n}')
        if s is not None:
            print(f'        -> "{s}"')
        elif imm is not None:
            print(f'        -> enum {imm}')
        else:
            print('        -> ' + ' | '.join(x.split('  ', 3)[-1].strip() for x in lines[:4]))
    print()
