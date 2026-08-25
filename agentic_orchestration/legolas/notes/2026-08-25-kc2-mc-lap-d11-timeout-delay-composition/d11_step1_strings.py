"""D-11 step 1 — locate every `specialAttack*` C-string in Game.dll, report RVA + VA,
then find every 4-byte reference to those VAs anywhere in the image (a push of a string
pointer is the loader's field-name argument).  READ-ONLY."""
import sys, struct, re; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base; raw=pe.raw

def off2rva(i):
    for s in pe.sections:
        if s['raddr'] <= i < s['raddr']+s['rsize']:
            return s['vaddr'] + (i - s['raddr']), s['name']
    return None, '-'

pats = [b'specialAttack', b'shortRangeMin', b'mediumRangeMin', b'longRangeMin',
        b'healSkillDelay', b'berserkSkillName', b'initialSkillName']
found = {}
for p in pats:
    i = raw.find(p)
    while i != -1:
        # full C string
        e = raw.index(b'\0', i)
        s = raw[i:e].decode('latin-1')
        # must start at a string boundary (preceded by NUL)
        if raw[i-1:i] == b'\0' and len(s) < 64:
            r, sec = off2rva(i)
            if r is not None:
                found[s] = (r, IB+r, sec)
        i = raw.find(p, i+1)

for s,(r,va,sec) in sorted(found.items(), key=lambda kv: kv[1][0]):
    print(f'{r:#010x}  VA {va:#010x}  {sec:8s}  {s}')
print(f'--- {len(found)} strings')
