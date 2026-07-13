#!/usr/bin/env python3
"""
apply-resolutions-v1.py — Apply human design rulings from judgment-resolutions-v1.md
into corpus-engine-key-v1.jsonl and regenerate boards-v1.md.

Authored: 2026-07-12 (gandalf resolution pass)
Authority: judgment-resolutions-v1.md §1–5. DO NOT RE-RUN apply-rules-v1.py (would erase these).

Rulings applied:
  §1: 5 J-SUM kits → flag replaced with resolved:totem-ratified; geometry stays totem
  §2: 4 J-ORB kits → flag replaced with gx-candidate:orbit; geometry stays unkeyed/None
  §3: 14 J-GEO system kits + ud-multishot-link (15 total) → row_class=system-record,
      route=<tag>, flags → resolved:system-record; all others get row_class=combat-kit
  §4: def-bin resolutions for 10 J-DEF kits:
      - d2-hammerdin, d2-zealot, d2-charger → def.bin=evade, rider trigger:block added, → resolved:block-evade-physics
      - le-harvest-lich → def.bin=glass → resolved:glass
      - poe2-walking-calamity, poe2-shaman-bear → def.bin=tank conf=0.4 → resolved:tank-postcutoff
      - poe2-spiral-volley, poe2-whirling-assault-ma, poe2-snipe-mirage-deadeye, poe2-archmage-totems
        → def.bin=post-cutoff-deferred → resolved:dossier-deferred
      (remaining 14 J-DEF resolved by §3 system-record reclass)
  §5: di-bone-wall-necro-pvp → flag stays J-GEO:placed-lane, add walls-demand:true
      d2-firewall-sorc → geo.value=null, rule_fired=gandalf-override, add flag J-GEO:placed-lane, add walls-demand:true
      le-frost-wall-rm → geometry stays totem, add walls-demand:true
"""

import json
import collections
from pathlib import Path

DIR = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/views/engine-key")
JSONL = DIR / "corpus-engine-key-v1.jsonl"
BOARDS = DIR / "boards-v1.md"


# ─── §1 J-SUM RATIFIED ───────────────────────────────────────────────────────
JSUM_KITS = {
    "gd-skeleton-ritualist",
    "le-wraithlord-necro",
    "poe2-infernal-legion",
    "poe2-minion-infernalist",
    "tl2-bot-engineer",
}

# ─── §2 J-ORB RECLASS ────────────────────────────────────────────────────────
JORB_KITS = {
    "poe1-poison-bv",
    "d3-inarius-bonestorm",
    "d4-ball-lightning",
    "d4-bouldercane",
}

# ─── §3 SYSTEM-RECORD RECLASS ────────────────────────────────────────────────
# 14 J-GEO kits + ud-multishot-link = 15 total
SYSTEM_RECORDS = {
    "di-essence-transfer":       "loot-economy",
    "ud-gear-enchant-economy":   "loot-economy",
    "hot-gear-well-retrieval":   "loot-economy",
    "di-resonance-awakening":    "progression",
    "di-inferno-ladder":         "progression",
    "ud-zodiac-board":           "progression",
    "ud-chaos-dungeon-ladder":   "progression",
    "ud-classless-triad":        "progression",
    "ud-link-rune-grammar":      "modifier-grammar",
    "ud-multishot-link":         "modifier-grammar",
    "hades1-privileged-status":  "ailment-synergy",
    "hades2-omega-magick":       "commitment-grammar",
    "hot-artifact-stack":        "difficulty-authoring",
    "vs-big-trouser":            "meta-currency",
    "tli-sage-elixir":           "consumable-economy",
}

# ─── §4 DEF-BIN RESOLUTIONS ──────────────────────────────────────────────────
# d2 block trio → evade + trigger:block rider
D2_BLOCK_TRIO = {"d2-hammerdin", "d2-zealot", "d2-charger"}

# poe2 kits with actual tank resolution
POE2_TANK_KITS = {"poe2-walking-calamity", "poe2-shaman-bear"}

# poe2 kits deferred post-cutoff
POE2_DEFERRED = {
    "poe2-spiral-volley",
    "poe2-whirling-assault-ma",
    "poe2-snipe-mirage-deadeye",
    "poe2-archmage-totems",
}

# ─── §5 WALLS DEMAND ─────────────────────────────────────────────────────────
WALLS_KITS = {"di-bone-wall-necro-pvp", "d2-firewall-sorc", "le-frost-wall-rm"}


def apply_resolutions(records):
    out = []
    for rec in records:
        kit_id = rec["kit_id"]
        flags = list(rec.get("flags", []))

        # ── §1: J-SUM → resolved:totem-ratified ──────────────────────────────
        if kit_id in JSUM_KITS:
            flags = [f for f in flags if f != "J-SUM"]
            flags.append("resolved:totem-ratified")
            # geometry stays totem (already correct)

        # ── §2: J-ORB → gx-candidate:orbit ───────────────────────────────────
        if kit_id in JORB_KITS:
            flags = [f for f in flags if f != "J-ORB"]
            flags.append("gx-candidate:orbit")
            # geometry stays None/unkeyed

        # ── §3: system-record reclass ─────────────────────────────────────────
        if kit_id in SYSTEM_RECORDS:
            route = SYSTEM_RECORDS[kit_id]
            rec["row_class"] = "system-record"
            rec["route"] = route
            # Remove J-GEO and J-DEF flags, replace with resolved:system-record
            flags = [f for f in flags if f not in ("J-GEO", "J-DEF")]
            if "resolved:system-record" not in flags:
                flags.append("resolved:system-record")
        else:
            # All other rows: combat-kit (only set if not already set)
            if "row_class" not in rec:
                rec["row_class"] = "combat-kit"

        # ── §4: DEF-BIN resolutions ───────────────────────────────────────────
        if kit_id in D2_BLOCK_TRIO:
            rec["def"]["bin"] = "evade"
            riders = list(rec["def"].get("riders", []))
            if "trigger:block" not in riders:
                riders.append("trigger:block")
            rec["def"]["riders"] = riders
            flags = [f for f in flags if f != "J-DEF"]
            flags.append("resolved:block-evade-physics")

        elif kit_id == "le-harvest-lich":
            rec["def"]["bin"] = "glass"
            flags = [f for f in flags if f != "J-DEF"]
            flags.append("resolved:glass")

        elif kit_id in POE2_TANK_KITS:
            rec["def"]["bin"] = "tank"
            rec["def"]["conf"] = 0.4
            flags = [f for f in flags if f != "J-DEF"]
            flags.append("resolved:tank-postcutoff")

        elif kit_id in POE2_DEFERRED:
            rec["def"]["bin"] = "post-cutoff-deferred"
            flags = [f for f in flags if f != "J-DEF"]
            flags.append("resolved:dossier-deferred")

        # ── §5: walls-demand ──────────────────────────────────────────────────
        if kit_id == "di-bone-wall-necro-pvp":
            # flag stays J-GEO:placed-lane; add walls-demand
            rec["walls_demand"] = True

        elif kit_id == "d2-firewall-sorc":
            # Override geo: line → null, rule_fired → gandalf-override
            rec["engine_geometry"]["value"] = None
            rec["engine_geometry"]["rule_fired"] = "gandalf-override"
            # Add J-GEO:placed-lane flag and walls-demand
            if "J-GEO:placed-lane" not in flags:
                flags.append("J-GEO:placed-lane")
            rec["walls_demand"] = True

        elif kit_id == "le-frost-wall-rm":
            # geometry stays totem; add walls-demand
            rec["walls_demand"] = True

        rec["flags"] = flags
        out.append(rec)
    return out


def recompute_boards(records):
    """
    Regenerate boards-v1.md from post-resolution data.
    Board 2: combat-kit denominator only (row_class=combat-kit).
    Board 1: add orbit and walls lines per ruling.
    Board 4: recompute with resolved def-bins.
    """

    # Split combat vs system records
    combat_kits = [r for r in records if r.get("row_class") == "combat-kit"]
    system_records = [r for r in records if r.get("row_class") == "system-record"]

    n_combat = len(combat_kits)
    n_system = len(system_records)

    # ── Board 1 data ──────────────────────────────────────────────────────────
    gap_kits = collections.defaultdict(list)
    for rec in records:
        for g in rec.get("econ", {}).get("gaps", []):
            gap_kits[g].append(rec["kit_id"])

    # SU mechanics demand: totem-keyed combat kits + resolved:totem-ratified
    su_demand_kits = []
    for rec in records:
        geo_val = rec.get("engine_geometry", {}).get("value")
        flags = rec.get("flags", [])
        if geo_val == "totem" or "resolved:totem-ratified" in flags:
            su_demand_kits.append(rec["kit_id"])
    su_demand_kits = list(dict.fromkeys(su_demand_kits))

    # Orbit kits (§2)
    orbit_kits = [r["kit_id"] for r in records if "gx-candidate:orbit" in r.get("flags", [])]

    # Walls kits (§5)
    walls_kits_list = [r["kit_id"] for r in records if r.get("walls_demand") is True]

    # ── Board 2 data (combat kits only) ─────────────────────────────────────
    geo_dist = collections.Counter()
    for rec in combat_kits:
        geo_val = rec.get("engine_geometry", {}).get("value")
        if geo_val:
            geo_dist[geo_val] += 1
        else:
            geo_dist["FLAGGED"] += 1

    # Collect flag counts over ALL records
    flag_counts = collections.Counter()
    for rec in records:
        for f in rec.get("flags", []):
            flag_counts[f] += 1

    # ── Board 3 data ──────────────────────────────────────────────────────────
    ailment_gap_kits = collections.defaultdict(list)
    for rec in records:
        for ag in rec.get("ctrl", {}).get("ailment_gaps", []):
            cls = ag.replace("GAP-AILMENT:", "")
            ailment_gap_kits[cls].append(rec["kit_id"])

    # ── Board 4 data ──────────────────────────────────────────────────────────
    def_bin_counts = collections.Counter()
    sustain_leech_count = 0
    block_kits = {"binary-negate": [], "flat-absorb": [], "percent-reduce": [], "unresolved": []}

    for rec in records:
        def_data = rec.get("def", {})
        bin_ = def_data.get("bin")
        riders = def_data.get("riders", [])
        if bin_:
            def_bin_counts[bin_] += 1
        else:
            def_bin_counts["FLAGGED"] += 1
        if "sustain:leech" in riders:
            sustain_leech_count += 1
        if "trigger:block" in riders:
            if bin_ == "evade":
                block_kits["binary-negate"].append(rec["kit_id"])
            elif bin_ == "absorb":
                block_kits["flat-absorb"].append(rec["kit_id"])
            elif bin_ == "mitigate":
                block_kits["percent-reduce"].append(rec["kit_id"])
            else:
                block_kits["unresolved"].append(rec["kit_id"])

    # ── Build boards text ─────────────────────────────────────────────────────
    lines = [
        "# Boards v1 — engine-key mapping pass\n\n",
        "> Generated by apply-resolutions-v1.py (post-judgment-resolutions-v1.md). 2026-07-12.\n",
        "> Four boards. Board 2 denominator = combat kits only (system-records excluded).\n\n",
        "---\n\n",
    ]

    # Board 1
    lines.append("## Board 1 — Mechanics-Gap Leverage\n\n")
    lines.append("*Per gap code: kit count + kit list. Feeds pause-2/V3 maximal-coverage objective.*\n\n")
    gap_code_order = ["SU", "AM", "PC", "RC", "RS", "DR", "HV", "BT", "LC", "UNKNOWN"]

    lines.append("| Gap Code | Count | Kit IDs |\n")
    lines.append("|---|---|---|\n")

    for code in gap_code_order:
        kits = gap_kits.get(code, [])
        if kits:
            kits_str = ", ".join(kits[:15]) + (f" (+{len(kits)-15} more)" if len(kits) > 15 else "")
            if code == "SU":
                demand_count = len(su_demand_kits)
                demand_str = ", ".join(su_demand_kits[:15]) + (
                    f" (+{demand_count-15} more)" if demand_count > 15 else "")
                lines.append(
                    f"| SU | economy={len(kits)} / mechanics-demand={demand_count} "
                    f"(totem+ratified) | economy kits: {kits_str} |\n"
                )
                lines.append(
                    f"| SU-demand | {demand_count} | {demand_str} |\n"
                )
            else:
                lines.append(f"| {code} | {len(kits)} | {kits_str} |\n")

    # Any unlisted gap codes
    for code, kits in sorted(gap_kits.items()):
        if code not in gap_code_order and kits:
            kits_str = ", ".join(kits[:15])
            lines.append(f"| {code} | {len(kits)} | {kits_str} |\n")

    # Orbit and walls lines (§2, §5)
    orbit_str = ", ".join(orbit_kits)
    walls_str = ", ".join(walls_kits_list)
    lines.append(f"| orbit (gx-candidate) | 4 | {orbit_str} |\n")
    lines.append(f"| walls (Q15 workstream) | 3 | {walls_str} |\n")

    lines.append("\n")

    # Board 2
    lines.append("## Board 2 — Geometry Distribution\n\n")
    lines.append(f"*Engine type → count. Denominator = combat kits only ({n_combat}); "
                 f"system-records={n_system} (listed separately).*\n\n")

    # Placed-lane and orbit flagged combat kits
    placed_lane_combat = [r["kit_id"] for r in combat_kits if "J-GEO:placed-lane" in r.get("flags", [])]
    orbit_combat = [r["kit_id"] for r in combat_kits if "gx-candidate:orbit" in r.get("flags", [])]

    lines.append("| Engine Type | Count |\n")
    lines.append("|---|---|\n")
    for gtype, cnt in sorted(geo_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| `{gtype}` | {cnt} |\n")

    lines.append(f"\n**System records (excluded from denominator):** {n_system}\n")
    if placed_lane_combat:
        lines.append(f"\n**Placed-lane flagged combat kits:** {', '.join(placed_lane_combat)}\n")
    if orbit_combat:
        lines.append(f"\n**Orbit flagged combat kits (gx-candidate):** {', '.join(orbit_combat)}\n")

    lines.append("\n**Flag inventory (post-resolution):**\n\n")

    # Show resolved vs active flags clearly
    active_flags = {k: v for k, v in flag_counts.items()
                    if not k.startswith("resolved:") and k not in ("gx-candidate:orbit",)}
    resolved_flags = {k: v for k, v in flag_counts.items() if k.startswith("resolved:")}
    candidate_flags = {k: v for k, v in flag_counts.items() if k == "gx-candidate:orbit"}

    lines.append("*Active (non-resolved) flags:*\n")
    for f, cnt in sorted(active_flags.items()):
        lines.append(f"  {f}={cnt}  ")
    lines.append("\n\n")

    lines.append("*Candidate flags:*\n")
    for f, cnt in sorted(candidate_flags.items()):
        lines.append(f"  {f}={cnt}  ")
    lines.append("\n\n")

    lines.append("*Resolved flags (audit trail):*\n")
    for f, cnt in sorted(resolved_flags.items()):
        lines.append(f"  {f}={cnt}  ")
    lines.append("\n\n")

    # Board 3
    lines.append("## Board 3 — Ailment-Gap Census\n\n")
    lines.append("*GAP-AILMENT class → count → ailment-layer design.*\n\n")
    lines.append("| Gap Class | Count | Representative Kits |\n")
    lines.append("|---|---|---|\n")
    for cls, kits in sorted(ailment_gap_kits.items(), key=lambda x: -len(x[1])):
        kits_sample = ", ".join(kits[:8]) + (f" (+{len(kits)-8} more)" if len(kits) > 8 else "")
        lines.append(f"| {cls} | {len(kits)} | {kits_sample} |\n")
    lines.append("\n")

    # Board 4
    lines.append("## Board 4 — Def-Bin Distribution\n\n")
    lines.append("*Recomputed post-resolution. Denominator = all records (combat + system).*\n\n")
    lines.append("| Def Bin | Count |\n")
    lines.append("|---|---|\n")
    for bin_, cnt in sorted(def_bin_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{bin_}` | {cnt} |\n")

    lines.append(f"\n**sustain-leech primary count (Fork D4 evidence — ESCALATED to Matt):** {sustain_leech_count}\n")
    lines.append(
        f"\n*(Fork D4: sixth-verb candidacy escalates to Matt if >10; current count is "
        f"{'ABOVE' if sustain_leech_count > 10 else 'AT OR BELOW'} threshold)*\n\n"
    )

    lines.append("### Block-physics split\n\n")
    lines.append("| Physics Bin | Count | Kit IDs |\n")
    lines.append("|---|---|---|\n")
    for btype, kits in block_kits.items():
        kits_str = ", ".join(kits)
        lines.append(f"| {btype} | {len(kits)} | {kits_str} |\n")
    lines.append("\n")

    return "".join(lines)


def main():
    # Read all records
    records = []
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Read {len(records)} records from {JSONL}")

    # Apply resolutions
    records = apply_resolutions(records)

    # Write JSONL back
    with open(JSONL, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    print(f"Wrote {len(records)} records → {JSONL}")

    # Report modification counts per section
    s1 = sum(1 for r in records if "resolved:totem-ratified" in r.get("flags", []))
    s2 = sum(1 for r in records if "gx-candidate:orbit" in r.get("flags", []))
    s3 = sum(1 for r in records if r.get("row_class") == "system-record")
    s4_block = sum(1 for r in records if "resolved:block-evade-physics" in r.get("flags", []))
    s4_glass = sum(1 for r in records if "resolved:glass" in r.get("flags", []))
    s4_tank = sum(1 for r in records if "resolved:tank-postcutoff" in r.get("flags", []))
    s4_deferred = sum(1 for r in records if "resolved:dossier-deferred" in r.get("flags", []))
    s5 = sum(1 for r in records if r.get("walls_demand") is True)

    print(f"\n§1 (J-SUM ratified):     {s1} rows")
    print(f"§2 (J-ORB → orbit):      {s2} rows")
    print(f"§3 (system-record):      {s3} rows")
    print(f"§4 block-evade-physics:  {s4_block} rows")
    print(f"§4 glass:                {s4_glass} rows")
    print(f"§4 tank-postcutoff:      {s4_tank} rows")
    print(f"§4 dossier-deferred:     {s4_deferred} rows")
    print(f"§5 walls-demand:         {s5} rows")

    # Flag inventory post-resolution
    flag_counts = collections.Counter()
    for rec in records:
        for f in rec.get("flags", []):
            flag_counts[f] += 1

    print("\nPost-resolution flag inventory:")
    for f, cnt in sorted(flag_counts.items()):
        print(f"  {f}: {cnt}")

    # Verify no unresolved J-flags remain (except J-GEO:placed-lane which stays per §5)
    unresolved = {k: v for k, v in flag_counts.items()
                  if k in ("J-SUM", "J-ORB", "J-GEO", "J-DEF")}
    if unresolved:
        print(f"\nWARNING: Unresolved J-flags remain: {unresolved}")
    else:
        print("\nOK: No unresolved J-SUM/J-ORB/J-GEO/J-DEF flags remain.")

    # Def-bin distribution
    def_bin_counts = collections.Counter()
    for rec in records:
        bin_ = rec.get("def", {}).get("bin")
        if bin_:
            def_bin_counts[bin_] += 1
        else:
            def_bin_counts["FLAGGED"] += 1
    print("\nDef-bin distribution (post-resolution):")
    for b, cnt in sorted(def_bin_counts.items(), key=lambda x: -x[1]):
        print(f"  {b}: {cnt}")

    # Combat vs system split
    n_combat = sum(1 for r in records if r.get("row_class") == "combat-kit")
    n_system = sum(1 for r in records if r.get("row_class") == "system-record")
    print(f"\nRow classes: combat-kit={n_combat}, system-record={n_system}, total={n_combat+n_system}")

    # Regenerate boards
    boards_text = recompute_boards(records)
    with open(BOARDS, "w") as f:
        f.write(boards_text)
    print(f"\nWrote boards → {BOARDS}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
