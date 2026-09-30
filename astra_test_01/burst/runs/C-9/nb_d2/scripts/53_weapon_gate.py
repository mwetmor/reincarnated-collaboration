# T12 rank 6, checks 2-4: the WEAPON GATE, read off the standing per-clip table.
#
#   python3 scripts/53_weapon_gate.py <weapon_table.json> [--json out]
#
# The table is measured in Godot by attack_lab/t12/godot/tools/hold_table.gd -- every clip raw,
# the axe carried by whatever bone its skin binds -- and archived beside the export it describes
# (nb_d2/tables/). Check 1, SKELETON IDENTITY, is a rule in 21_lint_export.py.
#
# RULES
#   HOLD  (check 2)  every ARMED hold clip -- idle, walk, run and its diagonals, both strafes, the
#                    block -- holds the axe at GUARD on at least half its frames: tilt 30-60 deg
#                    from vertical, haft forward and outboard, head outboard of the fist, |edge
#                    heading| <= 45 deg. FAIL below half.
#   EDGE  (check 3)  each axe strike's EDGE LEADS at the cut's strike -- the frame the head reaches
#                    furthest forward (14_axe_assert's definition: "the strike of a cut is where the
#                    EDGE reaches furthest forward"): |edge heading| <= 45 deg there AND the edge
#                    within 60 deg of the head's travel (cos >= 0.5). FAIL otherwise.
#   ARC   (check 4)  the axe head's screen path over one loop of each armed idle or locomotion clip
#                    <= 60 px in every direction cell (the waffle budget, from walk_armed's own
#                    25-46 px). FAIL over. A strike whose peak single-frame step exceeds 35 px
#                    (a quarter of the 140 px figure) is FLAGGED: it needs a trail.
#
# It FAILS TODAY BY DESIGN -- no armed hold clip passes HOLD -- so it is a standing gate, run on
# every staged set and reported, and NOT wired to stop the export chain until the weapon channel
# (rank 3) and the guard retarget (rank 2b) land.
import json, sys

HOLD_CLIPS = ["idle_armed", "walk_armed", "run_armed", "run_armed_L", "run_armed_R",
              "strafe_L_armed", "strafe_R_armed", "block"]
ARC_CLIPS = [c for c in HOLD_CLIPS if c != "block"]
STRIKES = ["attack", "attack_chop"]
HOLD_MIN, EDGE_HEADING_MAX, EDGE_COS_MIN, ARC_MAX_PX, STEP_FLAG_PX = 0.5, 45.0, 0.5, 60.0, 35.0


def gate(table):
    c = table["clips"]
    rows, fails, flags = [], [], []
    for cn in HOLD_CLIPS:
        if cn not in c:
            continue
        ok = c[cn]["pass_frac"] >= HOLD_MIN
        rows.append(("HOLD", cn, "PASS" if ok else "FAIL",
                     "%d%% of frames at guard (tilt %.0f, fwd %+.2f, out %+.2f, head out %+.2f, edge %+.0f)"
                     % (round(100 * c[cn]["pass_frac"]), c[cn]["tilt"], c[cn]["fwd"], c[cn]["out"],
                        c[cn]["head_out"], c[cn]["edge"])))
        if not ok:
            fails.append("HOLD %s" % cn)
    for cn in STRIKES:
        e = c.get(cn, {}).get("edge_lead")
        if not e:
            continue
        ok = abs(e["heading_strike"]) <= EDGE_HEADING_MAX and e["on_travel_strike"] >= EDGE_COS_MIN
        rows.append(("EDGE", cn, "PASS" if ok else "FAIL",
                     "at the cut's strike (%.2f s): edge heading %+.0f deg, edge on the travel %+.2f "
                     "| legacy leads %d/%d, best %.3f" % (e["strike_t"], e["heading_strike"],
                                                         e["on_travel_strike"], e["leads"], e["frames"], e["best"])))
        if not ok:
            fails.append("EDGE %s" % cn)
    for cn in ARC_CLIPS:
        if cn not in c:
            continue
        ok = c[cn]["arc_max"] <= ARC_MAX_PX
        rows.append(("ARC", cn, "PASS" if ok else "FAIL",
                     "axe-head screen path %.0f-%.0f px per loop over the 8 cells (budget %.0f)"
                     % (c[cn]["arc_min"], c[cn]["arc_max"], ARC_MAX_PX)))
        if not ok:
            fails.append("ARC %s" % cn)
    for cn in STRIKES:
        if cn in c and c[cn]["step_max"] > STEP_FLAG_PX:
            rows.append(("ARC", cn, "FLAG", "peak step %.1f px > %.0f px: needs a trail" % (c[cn]["step_max"], STEP_FLAG_PX)))
            flags.append(cn)
    return rows, fails, flags


if __name__ == "__main__":
    t = json.load(open(sys.argv[1]))
    rows, fails, flags = gate(t)
    print("weapon gate on '%s' (axe on %s, %d bones)" % (t.get("label"), t.get("axe_bone"), t.get("bones", 0)))
    for r in rows:
        print("  %-4s %-15s %-4s  %s" % r)
    print("  VERDICT: %s (%d fail, %d trail flag)" % ("FAIL" if fails else "PASS", len(fails), len(flags)))
    if "--json" in sys.argv:
        json.dump(dict(rows=rows, fails=fails, flags=flags), open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if fails else 0)
