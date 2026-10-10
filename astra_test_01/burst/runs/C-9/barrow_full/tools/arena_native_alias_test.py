#!/usr/bin/env python3
"""Prove absolute packed reads without a host file, and reject corrupt payloads."""
import hashlib
import os
import struct
import subprocess
import tempfile
import uuid
from pathlib import Path
from pck_native_alias import TABLE, PIN, add_alias


def main():
    source = Path('/Users/admin/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv')
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == PIN
    name = TABLE.encode()
    name += b'\0' * (-len(name) % 4)
    row = struct.pack('<I', len(name)) + name + struct.pack('<QQ', 0, len(data)) + hashlib.md5(data).digest() + struct.pack('<I', 0)
    header = struct.pack('<4sIIIIIQQ', b'GDPC', 3, 4, 6, 3, 2, 104, 104 + len(data)) + b'\0' * 64
    alias = '/__barrow_pck_probe_' + uuid.uuid4().hex + '/pinned.csv'
    with tempfile.TemporaryDirectory(prefix='barrow-alias-') as folder:
        root = Path(folder)
        good = root / 'good.pck'
        good.write_bytes(header + data + struct.pack('<I', 1) + row)
        add_alias(good, alias)
        bad = root / 'bad.pck'
        bad.write_bytes(header + b'X' + data[1:] + struct.pack('<I', 1) + row)
        try:
            add_alias(bad)
        except ValueError:
            print('NEGATIVE_ALIAS: PASS; corrupted table refused')
        else:
            raise AssertionError('corrupt data admitted')
        script = root / 'probe.gd'
        script.write_text('''extends SceneTree
func _initialize() -> void:
\tvar args := OS.get_cmdline_user_args()
\tif FileAccess.file_exists(args[1]):
\t\tquit(1)
\t\treturn
\tif not ProjectSettings.load_resource_pack(args[0]):
\t\tquit(2)
\t\treturn
\tvar ok := FileAccess.get_sha256(args[1]) == args[2]
\tprint("ABSOLUTE_PACKED_ALIAS: ", "PASS" if ok else "FAIL")
\tquit(0 if ok else 3)
''')
        godot = os.environ.get('GODOT', '/Applications/Godot.app/Contents/MacOS/Godot')
        subprocess.run([godot, '--headless', '--path', folder, '--script', str(script), '--', str(good), alias, PIN], check=True)


if __name__ == '__main__':
    main()
