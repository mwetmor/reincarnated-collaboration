#!/usr/bin/env python3
"""
gd_arc_reader_2026_07_26.py — minimal GD `ARC` v3 container reader (localization archives).

WHY THIS EXISTS
    The GD display-name -> `.dbr` record bridge needs `tags*_creatures.txt`, which ships inside
    `resources/Text_EN.arc` (+ one per expansion). That is an `ARC` v3 container -- a DIFFERENT
    container from the `.arz` the corpus lane already reads, but the SAME LZ4-block payload codec.
    Format mapped by legolas probe `2026-07-26-gd-displayname-bridge.md` §1; this module
    productionizes that sketch into elrond curation tooling (probe = instrument, this = product).

FORMAT (little-endian throughout)
    header, 28 bytes:
        magic b'ARC\\x00' | version u32 (=3) | num_file_entries u32 | num_data_records u32
        | record_table_size u32 | string_table_size u32 | record_table_offset u32
    layout:
        [ compressed part blobs ][ record table ][ string table ][ file entries ]
        record table entry (12 B) : part_offset u32, comp_size u32, decomp_size u32
        string table              : NUL-separated filenames (a flat byte block)
        file entry (44 B)         : entry_type u32, file_offset u32, comp_size u32, decomp_size u32,
                                    crc u32, file_time u64, num_parts u32, first_part_index u32,
                                    name_len u32, name_offset u32
    decode: per part, if comp_size == decomp_size -> STORED; else lz4.block.decompress(blob,
            uncompressed_size=decomp_size). Parts are concatenated in index order.

KNOWN LIMITATION (carried forward from probe §7)
    The 44-byte file entry's `crc` field is read but NOT validated against the payload. A stricter
    extractor should verify it. Recorded so a clean extraction here is not mistaken for a
    CRC-verified one.

READ-ONLY. Never writes to the vendor tree.
"""
import struct
import pathlib

import lz4.block

ARC_MAGIC = b"ARC\x00"
HEADER_FMT = "<4sIIIIII"
HEADER_SIZE = 28
RECORD_ENTRY_FMT = "<III"
RECORD_ENTRY_SIZE = 12
FILE_ENTRY_FMT = "<IIIIIQIIII"
FILE_ENTRY_SIZE = 44


class ArcArchive:
    """Minimal ARC v3 reader. Indexes file entries by name; decodes one file on demand."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.raw = self.path.read_bytes()
        self._parse_header()
        self._parse_tables()

    # -------------------------------------------------------------- header
    def _parse_header(self):
        if len(self.raw) < HEADER_SIZE:
            # survivalmode2/text_en.arc is a legitimately EMPTY archive (probe §1). Treat as 0 entries
            # rather than as a parse failure -- an empty container is data, not an error.
            (self.magic, self.version, self.num_file_entries, self.num_data_records,
             self.record_table_size, self.string_table_size, self.record_table_offset) = (
                ARC_MAGIC, 3, 0, 0, 0, 0, 0)
            self.empty = True
            return
        (self.magic, self.version, self.num_file_entries, self.num_data_records,
         self.record_table_size, self.string_table_size,
         self.record_table_offset) = struct.unpack_from(HEADER_FMT, self.raw, 0)
        if self.magic != ARC_MAGIC:
            raise ValueError(f"BLOCKED-FORMAT: magic={self.magic!r}, expected {ARC_MAGIC!r} ({self.path})")
        if self.version != 3:
            raise ValueError(f"BLOCKED-FORMAT: ARC version={self.version}, only v3 mapped ({self.path})")
        self.empty = self.num_file_entries == 0

    # -------------------------------------------------------------- tables
    def _parse_tables(self):
        self.parts = []      # [(part_offset, comp_size, decomp_size)]
        self.entries = {}    # name -> dict
        if self.empty:
            return
        b = self.raw
        pos = self.record_table_offset
        for _ in range(self.num_data_records):
            self.parts.append(struct.unpack_from(RECORD_ENTRY_FMT, b, pos))
            pos += RECORD_ENTRY_SIZE

        st_start = self.record_table_offset + self.record_table_size
        self.string_block = b[st_start: st_start + self.string_table_size]

        fe_start = st_start + self.string_table_size
        pos = fe_start
        for _ in range(self.num_file_entries):
            (entry_type, file_offset, comp_size, decomp_size, crc, file_time,
             num_parts, first_part_index, name_len, name_offset) = struct.unpack_from(
                FILE_ENTRY_FMT, b, pos)
            pos += FILE_ENTRY_SIZE
            name = self.string_block[name_offset: name_offset + name_len].decode("latin-1")
            self.entries[name] = dict(
                entry_type=entry_type, file_offset=file_offset, comp_size=comp_size,
                decomp_size=decomp_size, crc=crc, num_parts=num_parts,
                first_part_index=first_part_index)

    # -------------------------------------------------------------- payload
    def names(self):
        return list(self.entries.keys())

    def read_file(self, name):
        """Return decoded bytes for one archived file."""
        e = self.entries[name]
        if e["num_parts"] == 0:
            # stored whole, no part indirection
            blob = self.raw[e["file_offset"]: e["file_offset"] + e["comp_size"]]
            if e["comp_size"] == e["decomp_size"]:
                return blob
            return lz4.block.decompress(blob, uncompressed_size=e["decomp_size"])
        out = bytearray()
        for i in range(e["num_parts"]):
            p_off, p_comp, p_decomp = self.parts[e["first_part_index"] + i]
            blob = self.raw[p_off: p_off + p_comp]
            out += blob if p_comp == p_decomp else lz4.block.decompress(
                blob, uncompressed_size=p_decomp)
        if len(out) != e["decomp_size"]:
            raise ValueError(f"BLOCKED-SIZE: {name} decoded {len(out)} B, header says {e['decomp_size']} B")
        return bytes(out)


def parse_tag_file(payload):
    """
    Parse a GD `tags*.txt` payload into an ordered list of (key, value).

    GD tag files are `key=value` per line. Encoding is UTF-8 with an occasional BOM; a few files
    carry `//` comment lines and blank lines. Values may legitimately contain `=`, so split on the
    FIRST `=` only. Duplicate keys WITHIN one file are preserved in the returned list (the caller
    decides collision policy) -- silently de-duplicating here would hide a real source property.
    """
    text = payload.decode("utf-8-sig", errors="replace")
    out = []
    for line in text.splitlines():
        line = line.strip("﻿").rstrip("\r")
        if not line.strip() or line.lstrip().startswith("//"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        out.append((k.strip(), v))
    return out
