#!/usr/bin/env python3
"""Disable the generated native-extension startup list in the Web PCK.

Godot includes the Mac-only KC2 extension because it is a manifest member. All
sealed members must remain byte-identical for arena_paths.verify_bundle(). Only
the generated .godot/extension_list.cfg table entry is changed to an empty file;
the presentation adapter explicitly selects the runtime's GDScript solver on Web.
Godot 4.6 pack format 3, the same table format used by pck_list.py.
"""
import hashlib
import struct
import sys


def suppress_native_startup(path):
    with open(path, "r+b") as f:
        magic, version, _, _, _, flags = struct.unpack("<4sIIIII", f.read(24))
        if magic != b"GDPC" or version != 3 or flags & 1:
            raise ValueError("expected an unencrypted Godot format-3 pack")
        base, directory = struct.unpack("<QQ", f.read(16))
        f.seek(directory)
        count = struct.unpack("<I", f.read(4))[0]
        for _ in range(count):
            length = struct.unpack("<I", f.read(4))[0]
            name = f.read(length).rstrip(b"\0").decode()
            entry = f.tell()
            offset, size = struct.unpack("<QQ", f.read(16))
            f.read(20)
            if name != ".godot/extension_list.cfg":
                continue
            f.seek(base + offset)
            contents = f.read(size)
            expected = b"res://kc2/kc2_runtime/native/kc2rt_contact.gdextension\n"
            if contents not in (b"", expected):
                raise ValueError("unexpected extension startup list: %r" % contents)
            f.seek(entry + 8)
            f.write(struct.pack("<Q", 0))
            f.write(hashlib.md5(b"").digest())
            print("Web PCK: native startup list empty; sealed runtime members preserved")
            return
        print("Web PCK: no native startup list")


if __name__ == "__main__":
    suppress_native_startup(sys.argv[1])
