#!/usr/bin/env python3
"""Split oversized format-3 exports below Vercel's file fence; preserve all bytes.

Each input member is MD5 checked, each new pack is re-read and SHA-256 checked.
The mirror's mount list is updated before the build re-exports its main pack.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path
from pck_native_alias import entries

root = Path(sys.argv[1]).resolve()
output = root / 'build/web'
stamp_path = root / 'kc2/bundle/BUNDLE_STAMP.json'
stamp = json.loads(stamp_path.read_text())
mounts = []
report = {}
for name in stamp['kit_packs']:
    source = output / name
    if source.stat().st_size < 50_000_000:
        mounts.append(name)
        continue
    with source.open('rb') as f:
        header = bytearray(f.read(104))
        base, rows = entries(f)
        groups, group, size = [], [], 0
        for row in rows:
            if row[2] > 39_000_000:
                raise ValueError('Single resource exceeds bounded pack budget: ' + row[0])
            if group and size + row[2] > 39_000_000:
                groups.append(group)
                group, size = [], 0
            group.append(row)
            size += row[2]
        if group:
            groups.append(group)
        parts = []
        for i, group in enumerate(groups):
            part = output / (source.stem + '_part%d.pck' % i)
            expected, directory_rows = {}, []
            with part.open('wb') as dest:
                dest.write(header)
                dest.write(b'\0' * 8)
                for path, offset, length, row in group:
                    f.seek(base + offset)
                    data = f.read(length)
                    if len(data) != length or hashlib.md5(data).digest() != row[-20:-4]:
                        raise ValueError('Corrupt source resource: ' + path)
                    dest.write(b'\0' * (-dest.tell() % 16))
                    new_offset = dest.tell() - 112
                    dest.write(data)
                    directory_rows.append(row[:-36] + struct.pack('<QQ', new_offset, length) + row[-20:])
                    expected[path] = hashlib.sha256(data).hexdigest()
                directory = dest.tell()
                dest.write(struct.pack('<I', len(directory_rows)))
                for row in directory_rows:
                    dest.write(row)
                dest.seek(24)
                dest.write(struct.pack('<QQ', 112, directory))
            with part.open('rb') as verify:
                new_base, new_rows = entries(verify)
                actual = {}
                for path, offset, length, _ in new_rows:
                    verify.seek(new_base + offset)
                    actual[path] = hashlib.sha256(verify.read(length)).hexdigest()
            if actual != expected or part.stat().st_size >= 50_000_000:
                raise ValueError('Split resource verification failed: ' + part.name)
            parts.append(part.name)
        mounts.extend(parts)
        report[name] = parts
    source.unlink()
stamp['kit_packs'] = mounts
stamp['split_packs'] = report
stamp_path.write_text(json.dumps(stamp, indent=1))
(root / 'build/logs/pack_split.json').write_text(json.dumps(report, indent=2) + '\n')
print('PACK_SPLIT: PASS;', len(report), 'oversized packs;', len(mounts), 'mounts')
