#!/usr/bin/env python3
"""
vfx_x4_binding_drift_check.py — the drift guard for the X-4 VFX binding surface.

WHY THIS EXISTS
---------------
X-4 (`vfx_x4_materialization_2026_08_24.py`) landed two artifacts that BOTH encode
the fold set:

  1. `v_vfx_kit_skill_binding` — hardcoded CASE literals, transcribed verbatim
     from sealed spec § 4.1. Reads ONLY `vfx_archetype_member`.
  2. `vfx_archetype.folded_into` / `.fold_survives_as` — the L-38 bridge columns.

The view does NOT read the bridge. So the fold mapping has TWO HOMES carrying
ZERO independent information, and today they agree 2/2 with no counterexamples.

That is the same structural shape rocket measured at X-3c (`c7f8a87f`): a second
copy of a field, 100% agreement, no independent information — harmless until it
isn't. Measured here (2026-08-24) on a throwaway copy:

  * mutate `vfx_archetype.folded_into` for `ring` -> the view keeps reporting the
    old mapping and `circle` keeps reporting 93. Nothing complains.
  * re-run the X-4 migration -> it SILENTLY HEALS the bridge back to its constants
    and never reports that it found a divergence.

Drift is silent in BOTH directions. This script makes it loud.

THE TIE-BREAK (named here so a merge never decides it later)
------------------------------------------------------------
  * Sealed spec T-A § 3.1b is the SOLE AUTHORITY for the fold set.
  * `v_vfx_kit_skill_binding` is its executable form and is AUTHORITATIVE FOR BINDING.
  * `vfx_archetype.folded_into` / `.fold_survives_as` / `.fold_receives` are a
    DERIVED READER-AID and are NEVER AUTHORITATIVE.
  * If the three disagree, the SPEC wins, and that is a HALT to the conductor —
    not a data decision, because T-A is sealed law.

DISCIPLINE #76 (derive, don't hand-list)
----------------------------------------
Every list this script checks is PARSED FROM THE SPEC AT RUN TIME. There is no
hand-written fold set, no hand-written 24-row roster, and no hand-written count
anywhere below. Deltas are reported in BOTH directions — named-but-absent AND
derived-but-unnamed — per the second clause.

Read-only. Never writes. Exit 0 = consistent; exit 1 = divergence (details on stdout).

Owner: elrond (catalogue seam). Companion:
  ../curated/MIGRATION-vfx-x4-materialization-2026-08-24.md
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "research" / "curated" / "corpus.db"
SPEC = ROOT / "gandalf" / "notes" / "2026-08-24-vfx-archetype-binding-spec-DRAFT.md"
VOTE_RUN = "vfx-archetype-vote-2026-08-23"

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def delta(label: str, named: set[str], derived: set[str]) -> None:
    """Discipline #76 second clause: report the delta in BOTH directions."""
    missing = sorted(named - derived)
    extra = sorted(derived - named)
    if missing:
        fail(f"{label}: named-but-absent  -> {missing}")
    if extra:
        fail(f"{label}: derived-but-unnamed -> {extra}")
    if not missing and not extra:
        ok(f"{label}: both directions empty ({len(named)} entries)")


# ---------------------------------------------------------------- spec parsing
def parse_spec(text: str):
    """Derive the named lists from the sealed spec. Nothing is hand-listed."""
    idx_block = text[text.index("### 3.1a Index"): text.index("### 3.1b")]
    index_rows: dict[str, tuple[int, int]] = {}
    for line in idx_block.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        name = re.findall(r"`([a-z_]+)`", cells[1])
        counts = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", cells[2])
        if name and counts:
            index_rows[name[0]] = (int(counts.group(1)), int(counts.group(2)))

    fold_block = text[text.index("### 3.1b"): text.index("### 3.1 The rows")]
    folds: dict[str, str] = {}
    for line in fold_block.splitlines():
        if not line.startswith("|") or "Folded" in line or "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        src = re.findall(r"`([a-z_]+)`", cells[0])
        dst = re.findall(r"`([a-z_]+)`", cells[1])
        if src and dst:
            folds[src[0]] = dst[0]

    # Independent second parse of the same roster: the § 3.1.N row headings.
    sections = {n for _, n in re.findall(r"^#### 3\.1\.(\d+) · `([a-z_]+)`", text, re.M)}

    # Tier-1 surface class per row (col 7) — used for the FIELD-class boundary.
    surface: dict[str, str] = {}
    for line in idx_block.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        name = re.findall(r"`([a-z_]+)`", cells[1])
        if name and len(cells) > 7:
            surface[name[0]] = cells[7].split()[0].strip("*")
    return index_rows, folds, sections, surface


def main() -> int:
    if not DB.exists():
        print(f"FATAL: {DB} not found", file=sys.stderr)
        return 2
    if not SPEC.exists():
        print(f"FATAL: {SPEC} not found", file=sys.stderr)
        return 2

    spec_text = SPEC.read_text()
    index_rows, spec_folds, sections, surface = parse_spec(spec_text)
    cx = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    q = lambda s, a=(): cx.execute(s, a).fetchall()

    print(f"\nspec : {SPEC.name}")
    print(f"db   : {DB}")
    print(f"\nderived from spec: {len(index_rows)} index rows | {len(spec_folds)} folds | "
          f"{len(sections)} row-sections")

    # ------------------------------------------------ A. spec-internal coherence
    print("\n[A] spec-internal coherence")
    delta("§3.1a index vs §3.1.N headings", set(index_rows), sections)

    # ------------------------------------------------ B. roster: spec vs DB view
    print("\n[B] roster — spec §3.1a vs the view")
    view_arch = {r[0] for r in q("SELECT DISTINCT archetype_id FROM v_vfx_kit_skill_binding")}
    delta("§3.1a index vs view archetypes", set(index_rows), view_arch)

    # ------------------------------------------------ C. the 27 = 24 + 2 + 1 gap
    print("\n[C] DB-27 vs spec-24 — closed by derivation")
    all_arch = {r[0] for r in q(
        "SELECT archetype_id FROM vfx_archetype WHERE vote_run=?", (VOTE_RUN,))}
    by_status = {s: {r[0] for r in q(
        "SELECT archetype_id FROM vfx_archetype WHERE vote_run=? AND fold_status=?",
        (VOTE_RUN, s))} for s in ("active", "folded", "held")}
    residue = all_arch - set(index_rows)
    ok(f"vfx_archetype rows = {len(all_arch)}; spec-named active = {len(index_rows)}; "
       f"residue = {sorted(residue)}")
    if len(all_arch) != len(by_status['active']) + len(by_status['folded']) + len(by_status['held']):
        fail("fold_status does not partition the archetype set")
    else:
        ok(f"partition holds: {len(all_arch)} = {len(by_status['active'])} active "
           f"+ {len(by_status['folded'])} folded + {len(by_status['held'])} held")
    delta("residue vs (folded ∪ held)", residue, by_status["folded"] | by_status["held"])
    delta("spec §3.1a vs DB fold_status='active'", set(index_rows), by_status["active"])

    # ------------------------------------------------ D. THE SECOND-HOME CHECK
    print("\n[D] second-home check — spec folds vs bridge columns vs view CASE")
    bridge = {r[0]: (r[1], r[2]) for r in q(
        "SELECT archetype_id, folded_into, fold_survives_as FROM vfx_archetype "
        "WHERE vote_run=? AND fold_status='folded'", (VOTE_RUN,))}
    view_case = {pre: (post, flag) for pre, post, flag in q(
        "SELECT DISTINCT archetype_id_prefold, archetype_id, tier1_layer_flag "
        "FROM v_vfx_kit_skill_binding WHERE archetype_id_prefold <> archetype_id")}

    delta("spec folds vs bridge columns", set(spec_folds), set(bridge))
    delta("spec folds vs view CASE", set(spec_folds), set(view_case))
    for src, dst in spec_folds.items():
        b = bridge.get(src, (None, None))
        v = view_case.get(src, (None, None))
        if b[0] != dst:
            fail(f"fold target drift on '{src}': spec says '{dst}', bridge says '{b[0]}'")
        if v[0] != dst:
            fail(f"fold target drift on '{src}': spec says '{dst}', view says '{v[0]}'")
        if b[1] != v[1]:
            fail(f"layer-flag drift on '{src}': bridge '{b[1]}' vs view '{v[1]}'")
        if b[0] == dst and v[0] == dst and b[1] == v[1]:
            ok(f"'{src}' -> '{dst}' (layer '{v[1]}') agrees across spec / bridge / view")

    # HELD is not a fold — the state distinction the L-38 shorthand would have collapsed.
    for a in by_status["held"]:
        tgt = q("SELECT folded_into FROM vfx_archetype WHERE vote_run=? AND archetype_id=?",
                (VOTE_RUN, a))[0][0]
        if tgt is not None:
            fail(f"held archetype '{a}' carries folded_into='{tgt}' — HELD is not a fold")
        else:
            ok(f"held archetype '{a}' carries folded_into=NULL (HELD is not a fold)")
        if a in view_arch:
            fail(f"held archetype '{a}' leaked into the binding view")

    # Bridge reciprocity: every fold target must declare what it received.
    for src, dst in spec_folds.items():
        rec = q("SELECT fold_receives FROM vfx_archetype WHERE vote_run=? AND archetype_id=?",
                (VOTE_RUN, dst))
        if not rec or not rec[0][0]:
            fail(f"fold target '{dst}' does not declare fold_receives (bridge not reciprocal)")
        else:
            ok(f"fold target '{dst}' declares receipt: {rec[0][0]!r}")

    # ------------------------------------------------ E. counts, re-derived
    print("\n[E] counts — re-derived, never inherited")
    bound = q("SELECT COUNT(*) FROM v_vfx_kit_skill_binding")[0][0]
    kits = q("SELECT COUNT(DISTINCT kit_id) FROM v_vfx_kit_skill_binding")[0][0]
    spec_sum = sum(s for s, _ in index_rows.values())
    if bound != spec_sum:
        fail(f"view rows {bound} != spec §3.1a index sum {spec_sum}")
    else:
        ok(f"view rows {bound} == spec §3.1a index sum {spec_sum}")
    assigned = q("SELECT COUNT(*) FROM vfx_archetype_member WHERE vote_run=? "
                 "AND skill_ordinal>=0 AND archetype_id IS NOT NULL", (VOTE_RUN,))[0][0]
    held_members = q("SELECT COUNT(*) FROM vfx_archetype_member WHERE vote_run=? "
                     "AND archetype_id IN (SELECT archetype_id FROM vfx_archetype "
                     "WHERE vote_run=? AND fold_status='held')", (VOTE_RUN, VOTE_RUN))[0][0]
    if assigned - held_members != bound:
        fail(f"assigned {assigned} - held {held_members} != bound {bound}")
    else:
        ok(f"assigned {assigned} - held {held_members} = bound {bound}  "
           f"(X007: 'assigned' and 'bound' are different numbers)")
    ok(f"distinct kits = {kits}")

    # Per-row post-fold counts, derived from members rather than from member_skills.
    for name, (s_exp, k_exp) in sorted(index_rows.items()):
        got = q("SELECT COUNT(*), COUNT(DISTINCT kit_id) FROM v_vfx_kit_skill_binding "
                "WHERE archetype_id=?", (name,))[0]
        if got != (s_exp, k_exp):
            fail(f"row '{name}': spec says {s_exp}/{k_exp}, view derives {got[0]}/{got[1]}")
    if not any(f.startswith("row '") for f in failures):
        ok(f"all {len(index_rows)} per-row skill/kit counts match the spec index exactly")

    # ------------------------------------------------ F. losslessness, both ways
    print("\n[F] losslessness — bidirectional")
    orphan = q("SELECT COUNT(*) FROM v_vfx_kit_skill_binding v WHERE NOT EXISTS "
               "(SELECT 1 FROM vfx_archetype_member m WHERE m.kit_id=v.kit_id "
               "AND m.skill_ordinal=v.skill_ordinal AND m.vote_run=?)", (VOTE_RUN,))[0][0]
    dropped = q("SELECT COUNT(*) FROM vfx_archetype_member m WHERE m.vote_run=? "
                "AND m.archetype_id IS NOT NULL AND m.skill_ordinal>=0 "
                "AND m.archetype_id NOT IN (SELECT archetype_id FROM vfx_archetype "
                "WHERE vote_run=? AND fold_status='held') AND NOT EXISTS "
                "(SELECT 1 FROM v_vfx_kit_skill_binding v WHERE v.kit_id=m.kit_id "
                "AND v.skill_ordinal=m.skill_ordinal)", (VOTE_RUN, VOTE_RUN))[0][0]
    (ok if orphan == 0 else fail)(f"view rows with no member parent = {orphan}")
    (ok if dropped == 0 else fail)(f"eligible member rows missing from view = {dropped}")
    nolineage = q("SELECT COUNT(*) FROM v_vfx_kit_skill_binding WHERE "
                  "archetype_id_prefold <> archetype_id AND tier1_layer_flag IS NULL")[0][0]
    (ok if nolineage == 0 else fail)(f"folded rows without a layer flag = {nolineage}")

    # ------------------------------------------------ G. the aura FIELD boundary
    print("\n[G] aura emitter-anchor finding — the class boundary, derived")
    field = sorted(a for a, s in surface.items() if s == "FIELD")
    notes.append(
        f"Tier-1 surface FIELD = {field} (derived from spec §3.1a col 7). "
        "This is what bounds the X001 emitter-anchor class: only a FIELD-carried "
        "archetype presumes a caster-anchored emitting surface, so only a FIELD row "
        "can mis-absorb delegate bodies. X005 tested the other FIELD row (self_buff) "
        "and found it clean — a COMPLETE control of the class, not a sample of one.")
    ok(f"FIELD-carried archetypes = {field}")
    n_find = q("SELECT COUNT(*) FROM vfx_curation_finding WHERE curation_run=?",
               ("vfx-x4-materialization-2026-08-24",))[0][0]
    ok(f"X-4 curation findings on record = {n_find}")

    # ------------------------------------------------ verdict
    print("\n" + "=" * 66)
    for n in notes:
        print("NOTE: " + n)
    if failures:
        print(f"\nDRIFT DETECTED — {len(failures)} divergence(s).")
        print("Tie-break: sealed spec T-A § 3.1b wins. The bridge columns are a "
              "reader-aid and are never authoritative. A spec/view disagreement is a "
              "HALT to the conductor, not a data fix.")
        return 1
    print("\nCONSISTENT — spec, bridge, and view tell one story.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
