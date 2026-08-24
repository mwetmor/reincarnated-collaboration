"""D-4c STEP 10 — does ANY archive (expansions, survival modes, mods) override
`damageMagnitude`? Closes the self-critique gap: the rule's one decisive datum is a single
array, so an override anywhere would silently change the stacking regime. READ-ONLY."""
import sys, struct, lz4.block; sys.path.insert(0, '.')
from d4b_lib import ArzArchive, VENDOR_FULL, VENDOR_E3

TYPES = {0: 'int', 1: 'real', 2: 'string', 3: 'bool'}
found = 0
for tag, root in (('FULL v1.2.3.4', VENDOR_FULL), ('ED-III 20260808', VENDOR_E3)):
    for arz in sorted(root.rglob('*.arz')):
        try: a = ArzArchive(arz)
        except Exception as e:
            print(f'  !! {arz.relative_to(root)}: {e}'); continue
        hits = 0
        for rp, m in a.records.items():
            try:
                dec = lz4.block.decompress(
                    a.raw[24+m['data_offset']: 24+m['data_offset']+m['comp_size']],
                    uncompressed_size=m['decomp_size'])
            except Exception:
                continue
            pos = 0
            while pos + 8 <= len(dec):
                typ, cnt, nid = struct.unpack_from('<HHi', dec, pos); pos += 8
                vals = struct.unpack_from(f'<{cnt}I', dec, pos); pos += 4*cnt
                if a.strings[nid] == 'damageMagnitude':
                    fv = [struct.unpack('<f', struct.pack('<I', x))[0] for x in vals]
                    print(f'  [{tag}] {arz.relative_to(root)} :: {rp}'
                          f'   type={TYPES[typ]} COUNT={cnt} values={fv}')
                    hits += 1; found += 1
                    break
        print(f'  scanned {arz.relative_to(root)}  records={len(a.records):>6}  '
              f'damageMagnitude occurrences={hits}')
print(f'\nTOTAL damageMagnitude occurrences across ALL archives, BOTH pulls: {found}')
