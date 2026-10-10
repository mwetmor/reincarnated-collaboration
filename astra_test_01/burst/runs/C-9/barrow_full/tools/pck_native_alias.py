#!/usr/bin/env python3
"""Add a read-only packed alias for the sealed loader's legacy absolute path.

Godot FileAccess checks PackedData before the OS filesystem, for absolute paths
as well as res://. Append a directory entry referring to the existing verified
leech-table payload. No source/runtime bytes or OS files are rewritten. This
uses the Godot 4.6 format-3 directory; reject encryption and unknown flags.
See Godot 4.6 core/io/{file_access,file_access_pack}.cpp.
"""
import hashlib
import struct
import sys

TABLE = 'kc2/bundle/pm4p_leech_resistance.csv.bin'
ALIAS = '/Users/admin/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv'
PIN = 'cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e'


def entries(f):
    f.seek(0)
    magic, version, _, _, _, flags = struct.unpack('<4sIIIII', f.read(24))
    if magic != b'GDPC' or version != 3 or flags != 2:
        raise ValueError('expected unencrypted format-3 pack with relative file base')
    base, directory = struct.unpack('<QQ', f.read(16))
    f.seek(directory)
    count = struct.unpack('<I', f.read(4))[0]
    rows = []
    for _ in range(count):
        length_bytes = f.read(4)
        length = struct.unpack('<I', length_bytes)[0]
        name_bytes = f.read(length)
        payload = f.read(36)
        if len(payload) != 36:
            raise ValueError('truncated directory')
        offset, size = struct.unpack('<QQ', payload[:16])
        rows.append((name_bytes.rstrip(b'\0').decode(), offset, size,
                     length_bytes + name_bytes + payload))
    return base, rows


def add_alias(pack, alias=ALIAS):
    with open(pack, 'r+b') as f:
        base, rows = entries(f)
        matches = [r for r in rows if r[0] == TABLE]
        if len(matches) != 1 or any(r[0] == alias for r in rows):
            raise ValueError('expected one table and no existing alias')
        _, offset, size, original = matches[0]
        f.seek(base + offset)
        data = f.read(size)
        if hashlib.sha256(data).hexdigest() != PIN:
            raise ValueError('leech-table bytes do not match pin')
        name = alias.encode()
        name += b'\0' * (-len(name) % 4)
        row = struct.pack('<I', len(name)) + name + original[-36:]
        f.seek(0, 2)
        directory = f.tell()
        f.write(struct.pack('<I', len(rows) + 1))
        for r in rows:
            f.write(r[3])
        f.write(row)
        f.seek(32)
        f.write(struct.pack('<Q', directory))
    print('Native PCK: pinned leech-table alias added; payloads preserved')


if __name__ == '__main__':
    add_alias(sys.argv[1])
