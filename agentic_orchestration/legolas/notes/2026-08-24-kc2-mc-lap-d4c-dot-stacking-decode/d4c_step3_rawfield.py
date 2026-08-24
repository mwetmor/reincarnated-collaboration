"""D-4c STEP 3 — raw .arz encoding of gameengine.dbr:damageMagnitude.
Decodes the field block by hand (type, COUNT, values) so the array LENGTH is read off the
container rather than inferred from the adapter's collapse-singleton behaviour. READ-ONLY."""
import sys, struct, lz4.block; sys.path.insert(0, '.')
from d4b_lib import ArzArchive, VENDOR_FULL, VENDOR_E3

TYPES = {0: 'int', 1: 'real', 2: 'string', 3: 'bool'}

def raw_fields(a, rec_path, want):
    m = a.records[rec_path]
    dec = lz4.block.decompress(a.raw[24 + m['data_offset']: 24 + m['data_offset'] + m['comp_size']],
                               uncompressed_size=m['decomp_size'])
    pos, out = 0, []
    while pos + 8 <= len(dec):
        typ, cnt, nid = struct.unpack_from('<HHi', dec, pos); pos += 8
        vals = struct.unpack_from(f'<{cnt}I', dec, pos); pos += 4 * cnt
        name = a.strings[nid]
        if name in want:
            if typ == 1: v = [struct.unpack('<f', struct.pack('<I', x))[0] for x in vals]
            elif typ == 2: v = [a.strings[x] for x in vals]
            else: v = list(vals)
            out.append((name, TYPES.get(typ, typ), cnt, v))
    return out

WANT = {'damageMagnitude'}
for tag, root in (('FULL v1.2.3.4', VENDOR_FULL), ('ED-III 20260808', VENDOR_E3)):
    a = ArzArchive(root / 'database' / 'database.arz')
    for name, typ, cnt, v in raw_fields(a, 'records/game/gameengine.dbr', WANT):
        print(f'[{tag}] records/game/gameengine.dbr  {name}: type={typ}  COUNT={cnt}  values={v}')
