#!/usr/bin/env python3
"""Restore missing raw bundle-cache members from a previously verified web export.

Each PCK member's MD5 is checked before writing; the bundler subsequently checks
the sealed runtime/model SHA-256 pins. This never extracts imported resources.
"""
import hashlib
import sys
from pathlib import Path
from pck_native_alias import entries

root = Path(sys.argv[1]).resolve()
prefixes = ('kc2/bundle/', 'kc2/art/', 'kc2/model_pack/', 'kc2/kc2_runtime/')
count = 0
for pack in sorted((root / 'build/web').glob('*.pck')):
    with pack.open('rb') as f:
        base, rows = entries(f)
        for name, offset, size, row in rows:
            if not name.startswith(prefixes):
                continue
            target = root / name
            if not target.resolve().is_relative_to(root):
                raise ValueError('Unsafe cache member')
            if target.is_file():
                continue
            f.seek(base + offset)
            data = f.read(size)
            if len(data) != size or hashlib.md5(data).digest() != row[-20:-4]:
                raise ValueError('Corrupt cached web member: ' + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            count += 1
print('WEB_CACHE: restored %d checked raw members' % count)
