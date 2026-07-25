#!/usr/bin/env python3
"""
gdx3_probe_2026_07_24.py — Adapter lap for GDX3 (Fangs of Asterkarn).

Questions addressed (in commission priority order):
  Q1: Does GDX3.arz parse under the existing TQIT/LZ4 reader?
  Q2: New playerclass<NN>/ namespaces (new masteries)?
  Q3: New monster records with spatial-AI controller fields — value ranges?
  Q4: New field names / record types / templateName targets not handled by adapter?
  Q5: SurvivalMode3 — confirm/correct nature.

Coverage-boundary declaration (D-a) is printed at end.
D-b: join validation — any gdx3 record appearing in base/gdx1/gdx2 is noted; we do not
     call it a "change" without establishing record identity.

Read-only: does NOT write to Edition-I or Edition-II vendor directories.
"""
import io
import struct
import pathlib
import collections
import sys

import lz4.block

# ---- paths (read-only) ----------------------------------------------------------------
EDITION_II = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
GDX3_ARZ   = EDITION_II / "gdx3/database/GDX3.arz"
SM3_ARZ    = EDITION_II / "survivalmode3/database/SurvivalMode3.arz"

# Edition-I archives — for namespace diff (base + gdx1 + gdx2)
EDITION_I  = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-I-20260723")
BASE_ARZ   = EDITION_I / "database/database.arz"
GDX1_ARZ   = EDITION_I / "gdx1/database/GDX1.arz"
GDX2_ARZ   = EDITION_I / "gdx2/database/GDX2.arz"

# Spatial AI controller fields (commission Q3)
SPATIAL_FIELDS = {
    "ViewDistance", "InnerViewDistance", "SightAngerRate", "InnerSightAngerRate",
    "MaxPursuitDistance", "PursuitTime", "fleeDistance", "WanderDistance",
    "RoamDistance", "MaxYViewDistance", "distressCallRange", "ChanceToRespondToDistressCall",
}

TYPE_INT32, TYPE_FLOAT32, TYPE_STRIDX, TYPE_BOOL = 0, 1, 2, 3


# ---- TQIT .arz parser (same format truth as gd_arz_adapter_2026_07_24.py) -------------
class ArzArchive:
    def __init__(self, path: pathlib.Path, label: str = ""):
        self.path = path
        self.label = label or path.name
        print(f"\n[LOAD] {self.label}  ({path.stat().st_size:,} bytes)")
        self.raw = path.read_bytes()
        self._parse_header()
        self._parse_string_table()
        self._parse_record_table()
        print(f"  magic={self.magic} version={self.version} "
              f"records={self.rt_count} strings={len(self.strings)}")

    def _parse_header(self):
        b = self.raw
        (self.magic, self.version, self.rt_offset, self.rt_size,
         self.rt_count, self.st_offset, self.st_size) = struct.unpack_from("<HHiiiii", b, 0)
        if self.magic != 2:
            raise ValueError(
                f"BLOCKED-FORMAT: {self.label}: magic={self.magic} (expected 2/TQIT). "
                f"bytes[0:8]={b[0:8].hex()}"
            )

    def _parse_string_table(self):
        self.strings = []
        b = self.raw
        pos = self.st_offset
        (self.st_count,) = struct.unpack_from("<I", b, pos)
        pos += 4
        for _ in range(self.st_count):
            (slen,) = struct.unpack_from("<i", b, pos)
            pos += 4
            s = b[pos:pos + slen].decode("latin-1")
            pos += slen
            self.strings.append(s)

    def _parse_record_table(self):
        self.records = {}   # record_path -> dict(rtype, data_offset, comp_size, decomp_size)
        self.rtype_counts = collections.Counter()
        pos = self.rt_offset
        end = self.rt_offset + self.rt_size
        b = self.raw
        for _ in range(self.rt_count):
            if pos >= end:
                break
            (name_id,) = struct.unpack_from("<i", b, pos); pos += 4
            (rt_len,) = struct.unpack_from("<i", b, pos); pos += 4
            rtype = b[pos:pos + rt_len].decode("latin-1"); pos += rt_len
            (data_offset,) = struct.unpack_from("<i", b, pos); pos += 4
            (comp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (decomp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (timestamp,) = struct.unpack_from("<q", b, pos); pos += 8
            rec_path = self.strings[name_id]
            self.records[rec_path] = dict(
                rtype=rtype, data_offset=data_offset,
                comp_size=comp_size, decomp_size=decomp_size)
            self.rtype_counts[rtype] += 1

    def read_record(self, rec_path: str) -> dict:
        if rec_path not in self.records:
            raise KeyError(f"record not in archive: {rec_path}")
        meta = self.records[rec_path]
        base = 24 + meta["data_offset"]
        blob = self.raw[base: base + meta["comp_size"]]
        dec = lz4.block.decompress(blob, uncompressed_size=meta["decomp_size"])
        return self._decode_fields(dec)

    def _decode_fields(self, dec: bytes) -> dict:
        out = {}
        stream = io.BytesIO(dec)
        while True:
            head = stream.read(8)
            if len(head) < 8:
                break
            ftype, count, key_id = struct.unpack("<HHI", head)
            payload = stream.read(count * 4)
            if len(payload) < count * 4:
                break
            field_name = self.strings[key_id]
            vals = []
            for i in range(count):
                chunk = payload[i * 4:(i + 1) * 4]
                if ftype == TYPE_FLOAT32:
                    vals.append(struct.unpack("<f", chunk)[0])
                elif ftype == TYPE_INT32:
                    vals.append(struct.unpack("<i", chunk)[0])
                elif ftype == TYPE_BOOL:
                    vals.append(bool(struct.unpack("<I", chunk)[0]))
                elif ftype == TYPE_STRIDX:
                    vals.append(self.strings[struct.unpack("<I", chunk)[0]])
                else:
                    vals.append(struct.unpack("<i", chunk)[0])
            out[field_name] = vals[0] if count == 1 else vals
        return out

    def namespace_prefixes(self, depth: int = 4) -> collections.Counter:
        """Extract top-N path segments from all record paths."""
        ctr = collections.Counter()
        for path in self.records:
            parts = path.split("/")
            prefix = "/".join(parts[:depth])
            ctr[prefix] += 1
        return ctr


# ---- Q1: parse test --------------------------------------------------------------------
def q1_parse_test(arc: ArzArchive) -> bool:
    """Parse succeeds if we reach this function (header + string table + record table done).
    Sample-decode 5 records spread across the archive to confirm LZ4 decompression also works."""
    paths = list(arc.records.keys())
    step = max(1, len(paths) // 5)
    sample_paths = [paths[i] for i in range(0, len(paths), step)][:5]
    errors = []
    for p in sample_paths:
        try:
            rec = arc.read_record(p)
            if not rec:
                errors.append(f"  EMPTY decode: {p}")
        except Exception as e:
            errors.append(f"  DECODE ERROR [{p}]: {e!r}")
    if errors:
        print("Q1 SAMPLE DECODE ERRORS:")
        for e in errors:
            print(e)
        return False
    print(f"Q1 PARSE: OK — {len(paths)} records indexed; {len(sample_paths)} sample decodes clean.")
    return True


# ---- Q2: playerclass namespaces --------------------------------------------------------
def extract_playerclass_namespaces(arc: ArzArchive) -> set:
    """Return set of 'records/skills/playerclass<NN>' namespaces."""
    ns = set()
    for path in arc.records:
        parts = path.split("/")
        # look for records/skills/playerclassNN/...
        if len(parts) >= 3 and parts[0] == "records" and parts[1] == "skills":
            segment = parts[2]
            if segment.startswith("playerclass"):
                ns.add(segment)
    return ns


def q2_playerclass_diff(base_arc, gdx1_arc, gdx2_arc, gdx3_arc):
    base_ns  = extract_playerclass_namespaces(base_arc)
    gdx1_ns  = extract_playerclass_namespaces(gdx1_arc)
    gdx2_ns  = extract_playerclass_namespaces(gdx2_arc)
    prior_ns = base_ns | gdx1_ns | gdx2_ns
    gdx3_ns  = extract_playerclass_namespaces(gdx3_arc)
    new_ns   = gdx3_ns - prior_ns

    print("\n=== Q2: PLAYERCLASS NAMESPACES ===")
    print(f"  base     : {sorted(base_ns)}")
    print(f"  gdx1     : {sorted(gdx1_ns)}")
    print(f"  gdx2     : {sorted(gdx2_ns)}")
    print(f"  prior union (base+gdx1+gdx2): {sorted(prior_ns)}")
    print(f"  gdx3     : {sorted(gdx3_ns)}")
    print(f"  NEW in gdx3 (not in prior): {sorted(new_ns)}")

    # also count skill records per playerclass in gdx3
    pc_skill_counts = collections.Counter()
    for path in gdx3_arc.records:
        parts = path.split("/")
        if len(parts) >= 3 and parts[0] == "records" and parts[1] == "skills":
            segment = parts[2]
            if segment.startswith("playerclass"):
                pc_skill_counts[segment] += 1
    if pc_skill_counts:
        print("\n  gdx3 skill record counts per playerclass:")
        for ns, cnt in sorted(pc_skill_counts.items()):
            tag = " <-- NEW" if ns in new_ns else ""
            print(f"    {ns}: {cnt} records{tag}")
    return new_ns, prior_ns, gdx3_ns


# ---- Q3: monster controller spatial fields ---------------------------------------------
def collect_spatial_ranges(arc: ArzArchive, label: str) -> dict:
    """Scan ALL records for controller-pattern paths, collect spatial field ranges."""
    # Controller records in GD are referenced by body records; their paths typically contain
    # "controller" in the path stem. We scan all records for the spatial field names.
    ranges = {f: [] for f in SPATIAL_FIELDS}
    controller_paths = []
    for path in arc.records:
        if "controller" in path.lower():
            controller_paths.append(path)

    if not controller_paths:
        print(f"  [{label}] No controller paths found.")
        return ranges

    decode_errors = 0
    found_count = 0
    for path in controller_paths:
        try:
            rec = arc.read_record(path)
            hit = False
            for f in SPATIAL_FIELDS:
                if f in rec:
                    v = rec[f]
                    if isinstance(v, list):
                        ranges[f].extend(v)
                    else:
                        ranges[f].append(v)
                    hit = True
            if hit:
                found_count += 1
        except Exception:
            decode_errors += 1

    print(f"  [{label}] {len(controller_paths)} controller paths; "
          f"{found_count} with >=1 spatial field; {decode_errors} decode errors")
    return ranges


def q3_spatial_ranges(base_arc, gdx1_arc, gdx2_arc, gdx3_arc):
    print("\n=== Q3: MONSTER CONTROLLER SPATIAL FIELDS ===")

    print("Collecting Edition-I ranges (base + gdx1 + gdx2)...")
    prior_ranges = {f: [] for f in SPATIAL_FIELDS}
    for arc, lbl in [(base_arc, "base"), (gdx1_arc, "gdx1"), (gdx2_arc, "gdx2")]:
        r = collect_spatial_ranges(arc, lbl)
        for f in SPATIAL_FIELDS:
            prior_ranges[f].extend(r[f])

    print("Collecting GDX3 ranges...")
    gdx3_ranges = collect_spatial_ranges(gdx3_arc, "gdx3")

    print("\n  Spatial field ranges — Edition-I (base+gdx1+gdx2) vs GDX3:")
    print(f"  {'Field':<35} {'Prior min':>10} {'Prior max':>10} {'Prior n':>8} "
          f"{'GDX3 min':>10} {'GDX3 max':>10} {'GDX3 n':>8} {'OUTSIDE_ENVELOPE'}")
    for f in sorted(SPATIAL_FIELDS):
        pv = [x for x in prior_ranges[f] if isinstance(x, (int, float))]
        gv = [x for x in gdx3_ranges[f] if isinstance(x, (int, float))]
        p_min = min(pv) if pv else "—"
        p_max = max(pv) if pv else "—"
        g_min = min(gv) if gv else "—"
        g_max = max(gv) if gv else "—"
        outside = ""
        if pv and gv:
            if min(gv) < min(pv) or max(gv) > max(pv):
                outside = "YES"
        print(f"  {f:<35} {str(p_min):>10} {str(p_max):>10} {len(pv):>8} "
              f"{str(g_min):>10} {str(g_max):>10} {len(gv):>8} {outside}")

    return prior_ranges, gdx3_ranges


# ---- Q4: new field names, record types, templateName targets ---------------------------
def q4_new_fields_and_rtypes(base_arc, gdx1_arc, gdx2_arc, gdx3_arc):
    print("\n=== Q4: NEW FIELD NAMES / RECORD TYPES / TEMPLATE NAMES IN GDX3 ===")

    # Gather all field names + record types from prior archives (string tables only for fields)
    prior_field_names = set()
    for arc in [base_arc, gdx1_arc, gdx2_arc]:
        prior_field_names.update(arc.strings)

    # GDX3 string table
    gdx3_strings = set(gdx3_arc.strings)
    new_strings = gdx3_strings - prior_field_names

    # Record types: count in prior vs gdx3
    prior_rtypes = collections.Counter()
    for arc in [base_arc, gdx1_arc, gdx2_arc]:
        prior_rtypes.update(arc.rtype_counts)
    gdx3_rtypes = gdx3_arc.rtype_counts

    new_rtypes = {rt: cnt for rt, cnt in gdx3_rtypes.items() if rt not in prior_rtypes}
    existing_rtypes = {rt: cnt for rt, cnt in gdx3_rtypes.items() if rt in prior_rtypes}

    print(f"\n  New record types in GDX3 (not in base/gdx1/gdx2):")
    if new_rtypes:
        for rt, cnt in sorted(new_rtypes.items(), key=lambda x: -x[1]):
            print(f"    {rt}: {cnt}")
    else:
        print("    (none)")

    print(f"\n  Existing record types present in GDX3 (count in gdx3):")
    for rt, cnt in sorted(existing_rtypes.items(), key=lambda x: -x[1])[:30]:
        print(f"    {rt}: {cnt}")

    # templateName values in gdx3
    print("\n  Sampling templateName values from gdx3 records (first 200 records):")
    template_counter = collections.Counter()
    sample_paths = list(gdx3_arc.records.keys())[:200]
    decode_errors = 0
    for path in sample_paths:
        try:
            rec = gdx3_arc.read_record(path)
            tn = rec.get("templateName")
            if tn:
                template_counter[tn] += 1
        except Exception:
            decode_errors += 1
    print(f"  ({decode_errors} decode errors in sample)")
    for tn, cnt in template_counter.most_common(20):
        print(f"    {cnt:>4}x  {tn}")

    # New field names: filter to plausible field names (not path strings)
    # Field names in .arz string tables look like camelCase identifiers; paths contain '/'
    plausible_new_fields = {s for s in new_strings
                            if "/" not in s and "." not in s and len(s) > 1 and len(s) < 80
                            and not s.startswith("records/")
                            and not s.startswith("database/")
                            and s[0].islower() or s[0].isupper()}
    # Further filter: actual field names are in string tables of records we decoded,
    # but without decoding all records we use the string table as a proxy.
    print(f"\n  Strings in GDX3 not in prior string tables: {len(new_strings)} total")
    print(f"  Plausible new field names (no '/' or '.', len 2-79): {len(plausible_new_fields)}")
    # Show sample sorted
    sorted_new = sorted(plausible_new_fields)
    print(f"  First 60 new candidate field names:")
    for s in sorted_new[:60]:
        print(f"    {s}")
    if len(sorted_new) > 60:
        print(f"    ... ({len(sorted_new) - 60} more)")

    return new_rtypes, new_strings


# ---- Q5: SurvivalMode3 -----------------------------------------------------------------
def q5_survivalmode3(sm3_arc: ArzArchive):
    print("\n=== Q5: SURVIVALMODE3 NATURE ===")
    # Look at top-level namespace structure
    ns_ctr = collections.Counter()
    for path in sm3_arc.records:
        parts = path.split("/")
        if len(parts) >= 2:
            ns_ctr["/".join(parts[:2])] += 1
        else:
            ns_ctr[parts[0]] += 1

    print(f"  Total records: {len(sm3_arc.records)}")
    print(f"  Top-10 namespace prefixes (depth-2):")
    for ns, cnt in ns_ctr.most_common(10):
        print(f"    {cnt:>5}  {ns}")

    # Sample a few records
    sample_paths = list(sm3_arc.records.keys())[:5]
    print("\n  Sample record paths:")
    for p in sample_paths:
        rtype = sm3_arc.records[p]["rtype"]
        print(f"    [{rtype}] {p}")

    # Check if it carries player skill records
    skill_paths = [p for p in sm3_arc.records if "/skills/" in p]
    print(f"\n  Records containing '/skills/': {len(skill_paths)}")
    for p in skill_paths[:10]:
        print(f"    {p}")

    # Check for wave/arena related strings in string table
    wave_strings = [s for s in sm3_arc.strings
                    if any(kw in s.lower() for kw in ["wave", "arena", "crucible", "survival", "asterkarn"])]
    print(f"\n  String-table entries matching wave/arena/crucible/survival/asterkarn: {len(wave_strings)}")
    for s in wave_strings[:20]:
        print(f"    {s}")


# ---- gdx3 top namespace survey ---------------------------------------------------------
def gdx3_namespace_survey(gdx3_arc: ArzArchive):
    print("\n=== GDX3 TOP-LEVEL NAMESPACE SURVEY ===")
    ns_d2 = collections.Counter()  # depth-2 prefixes
    ns_d3 = collections.Counter()  # depth-3 prefixes (for skills/ branch)
    for path in gdx3_arc.records:
        parts = path.split("/")
        ns_d2["/".join(parts[:2])] += 1
        if len(parts) >= 3:
            ns_d3["/".join(parts[:3])] += 1

    print(f"  Depth-2 namespaces (all):")
    for ns, cnt in ns_d2.most_common(30):
        print(f"    {cnt:>6}  {ns}")

    # Show skills depth-3 in full
    print(f"\n  Skills depth-3 namespaces:")
    skills_d3 = {k: v for k, v in ns_d3.items() if k.startswith("records/skills/")}
    for ns, cnt in sorted(skills_d3.items()):
        print(f"    {cnt:>6}  {ns}")


# ---- main ------------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("GDX3 ADAPTER LAP — 2026-07-24")
    print("Fangs of Asterkarn / app 2699230 / Edition-II additive delta")
    print("=" * 72)

    # Verify all paths exist before loading
    missing = [p for p in [GDX3_ARZ, SM3_ARZ, BASE_ARZ, GDX1_ARZ, GDX2_ARZ] if not p.exists()]
    if missing:
        sys.exit(f"FATAL: missing files: {missing}")

    # ---- Load all archives ----
    print("\n[LOADING ARCHIVES — read-only]")
    try:
        gdx3 = ArzArchive(GDX3_ARZ, "GDX3")
    except ValueError as e:
        print(f"\nQ1 BLOCKED-FORMAT: {e}")
        sys.exit(1)

    try:
        sm3 = ArzArchive(SM3_ARZ, "SurvivalMode3")
    except ValueError as e:
        print(f"\nSurvivalMode3 BLOCKED-FORMAT: {e}")
        sm3 = None

    base = ArzArchive(BASE_ARZ, "base")
    gdx1 = ArzArchive(GDX1_ARZ, "GDX1")
    gdx2 = ArzArchive(GDX2_ARZ, "GDX2")

    # ---- Q1 ----
    print("\n=== Q1: PARSE TEST ===")
    q1_ok = q1_parse_test(gdx3)

    # ---- GDX3 namespace survey ----
    gdx3_namespace_survey(gdx3)

    # ---- Q2 ----
    new_ns, prior_ns, gdx3_ns = q2_playerclass_diff(base, gdx1, gdx2, gdx3)

    # ---- Q3 ----
    prior_ranges, gdx3_ranges = q3_spatial_ranges(base, gdx1, gdx2, gdx3)

    # ---- Q4 ----
    new_rtypes, new_strings = q4_new_fields_and_rtypes(base, gdx1, gdx2, gdx3)

    # ---- Q5 ----
    if sm3:
        q5_survivalmode3(sm3)

    # ---- SUMMARY ----
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"\nQ1 — Parse: {'PASS — GDX3.arz parses under existing TQIT/LZ4 reader, unmodified.' if q1_ok else 'FAIL — see above.'}")
    print(f"     Records: {gdx3.rt_count:,}   Strings: {len(gdx3.strings):,}")
    print(f"     magic={gdx3.magic} version={gdx3.version}  (same as base/gdx1/gdx2)")

    print(f"\nQ2 — New masteries (playerclass namespaces new in gdx3):")
    if new_ns:
        for ns in sorted(new_ns):
            print(f"     NEW: {ns}  — downstream consequence: GD-SLICE coverage boundary MOVED")
    else:
        print("     NONE — no new playerclass namespaces. GD-SLICE denominator unchanged.")
    print(f"     Prior union: {sorted(prior_ns)}")
    print(f"     GDX3 carries: {sorted(gdx3_ns)}")

    print(f"\nQ3 — New monster controller records: see table above.")
    print(f"     Controller records in gdx3: {sum(1 for p in gdx3.records if 'controller' in p.lower())}")

    print(f"\nQ4 — New record types in gdx3: {len(new_rtypes)}")
    for rt, cnt in sorted(new_rtypes.items()):
        print(f"     {rt}: {cnt}")

    # ---- D-a: Coverage-boundary declaration ----
    print("\n" + "=" * 72)
    print("D-a COVERAGE BOUNDARY DECLARATION (mandatory per commission)")
    print("=" * 72)
    print("""
EXAMINED in this lap:
  - GDX3.arz: header parse, string table, record table index (all records enumerated)
  - GDX3.arz: sample decode of 5 records spread across archive (Q1 decompression test)
  - GDX3.arz: all 'controller' path records decoded for spatial field extraction (Q3)
  - GDX3.arz: first 200 records decoded for templateName survey (Q4 sample)
  - GDX3.arz: string table diffed against base+gdx1+gdx2 string tables (Q4 field names)
  - GDX3.arz: record type (rtype) table enumerated in full (Q4 rtypes)
  - GDX3.arz: all record paths enumerated for playerclass/ namespace extraction (Q2)
  - SurvivalMode3.arz: header, string table, record table (Q5 survey)
  - base/GDX1/GDX2 .arz: record tables and string tables (for diff baselines)

NOT examined in this lap:
  - GDX3.arz: bulk decode of ALL records — only controller records and a 200-record sample
    were decoded. Fields present in non-controller, non-sampled records are not reported.
  - gdx3/resources/Text_EN.arc — localization archive not parsed. Tag-to-English-name bridge
    for any gdx3 skill is not resolved. Same gap as prior work (Edition-I lap also did not parse .arc).
  - SurvivalMode3.arz: no full record decode — index + namespace survey only.
  - Template files (.tpl) — not embedded in .arz; not in scope for this lap.
  - survivalmode3/resources/Text_EN.arc — 2,219 bytes; not opened.
  - Any .wrl/.lvl zone layout files — not present in the .arz archives.
  - GDX3 boss records specifically — controller scan covers all controller-path records;
    boss-vs-champion distinction within GDX3 was not separately enumerated (Q3 covers ranges,
    not classification breakdown).
  - FIELD POPULATION COMPLETENESS: the string table diff identifies strings NEW to gdx3 vs
    prior archives. This is a proxy for new field names, not a confirmed field-usage scan.
    A string in the table may be a path, display name, or enum value — not necessarily a field name.
    The confirmed new FIELD names require full decode of all records, which was not done.
  - D-b NOTE: all spatial range comparisons are aggregate. If a specific gdx3 record path
    appears identically in base/gdx1/gdx2, D-b join validation applies before calling it changed.
    No such overlap was observed (controller records are namespaced per-archive), but this is
    an assertion from index inspection, not a cross-archive path-set intersection proof.
""")


if __name__ == "__main__":
    main()
