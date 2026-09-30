# T12 rank 6, checks 2-5: the WEAPON GATE, read off a measured table.
#
#   python3 scripts/53_weapon_gate.py <weapon_table.json> [--json out]
#
# The table is measured in Godot and archived beside the export it describes (nb_d2/tables/):
#   attack_lab/t12/godot/tools/guard_accept.gd   "source": "tree" -- the HOLD STATES as the scene
#       plays them (idle, walk, run, block, both strafes: through the AnimationTree, every layer
#       on) and the strikes raw. Since T12 (c) the axe arm's guard is a RUNTIME layer (axe_guard_R,
#       knight.gd's blend_r), so a raw clip no longer carries the hold by design, and the hold is
#       measured where it is made.
#   attack_lab/t12/godot/tools/hold_table.gd     legacy, no "source" -- every clip raw.
# Check 1, SKELETON IDENTITY, is a rule in 21_lint_export.py.
#
# RULES
#   HOLD  (check 2)  every hold state -- idle, walk, run, block, both strafes (legacy: the armed hold
#                    clips) -- holds the axe at GUARD on at least 90% of its frames: tilt 30-60 deg
#                    from vertical, haft forward and outboard, head outboard of the fist, |edge
#                    heading| <= 45 deg. FAIL below.
#   EDGE  (check 3)  each axe strike's EDGE LEADS: the edge lies ALONG THE HEAD'S TRAVEL (the edge
#                    direction against the travel with its along-haft part removed) -- cos >= 0.707
#                    (45 deg) at the STRIKE FRAME, AND the speed-weighted mean over the ACTIVE SWING
#                    >= 0.8. The active swing is the frames contiguous with the head's peak speed at
#                    >= 50% of it; the strike frame is the frame inside it where the head reaches
#                    furthest forward of the hips. The edge's heading against his forward is
#                    REPORTED, not gated. FAIL otherwise.
#   ARC   (check 4)  the axe head's screen path over one loop of the idle and each locomotion state
#                    <= 60 px in every play-camera cell (the waffle budget, from walk_armed's own
#                    25-46 px). FAIL over. A strike whose peak single-frame step exceeds 35 px
#                    (a quarter of the 140 px figure) is FLAGGED: it needs a trail.
#   PEN   (check 5)  no axe vertex inside the body, the closed fist excluded, on any frame of any
#                    hold state or strike (every 4th vertex, crossing parity against the posed,
#                    CPU-skinned body). FAIL on any.
#
# CHANGES
#   2026-09-30  EDGE redefined, approved by the coordinator (Run C-9 Phase 2, T12 (c)). It was:
#               |edge heading| <= 45 deg at the clip's furthest-forward frame AND cos >= 0.5 against
#               the travel. REASON: THE SLASH IS A LATERAL SWEEP. At its strike the head travels
#               ACROSS him, so an edge that leads the cut faces sideways, and the heading rule failed
#               exactly the edge a cut needs: the two halves of the old rule asked for opposite
#               things on a sweep. What "the edge leads" means physically is the edge along the
#               travel, so that is the rule, tightened to 0.707 at the strike and required over
#               the whole swing (0.8), not one frame. The strike frame moved inside the active
#               swing because the charged chop's whole-clip furthest-forward frame (3.83 s) is in
#               its overhead raise, which is not a cut.
#   2026-09-30  HOLD at >= 90% of frames (was at least half): the T12 (c) acceptance. The hold set is
#               the runtime states when the table is measured through the tree.
#   2026-09-30  PEN added: the T12 (c) acceptance, penetration 0 with the fist excluded.
#
# A standing gate: run on every staged set and reported; NOT wired to stop the export chain.
import json, sys

HOLD_STATES = ["idle", "walk", "run", "block", "strafe_l", "strafe_r"]
ARC_STATES = ["idle", "walk", "run", "strafe_l", "strafe_r"]
HOLD_CLIPS_LEGACY = ["idle_armed", "walk_armed", "run_armed", "run_armed_L", "run_armed_R",
                     "strafe_L_armed", "strafe_R_armed", "block"]
ARC_CLIPS_LEGACY = [c for c in HOLD_CLIPS_LEGACY if c != "block"]
STRIKES = ["attack", "attack_chop"]
HOLD_MIN = 0.9
EDGE_COS_STRIKE_MIN, EDGE_COS_SWING_MIN = 0.707, 0.8
ARC_MAX_PX, STEP_FLAG_PX = 60.0, 35.0


def gate(table):
    c = table["clips"]
    tree = table.get("source") == "tree"
    holds = HOLD_STATES if tree else HOLD_CLIPS_LEGACY
    arcs = ARC_STATES if tree else ARC_CLIPS_LEGACY
    rows, fails, flags = [], [], []
    for cn in holds:
        if cn not in c:
            continue
        r = c[cn]
        ok = r["pass_frac"] >= HOLD_MIN
        turn = (", fist turn %.1f/%.1f deg" % (r["turn_med"], r["turn_p90"])) if "turn_med" in r else ""
        rows.append(("HOLD", cn, "PASS" if ok else "FAIL",
                     "%d%% of frames at guard (tilt %.0f, fwd %+.2f, out %+.2f, head out %+.2f, edge %+.0f%s)"
                     % (round(100 * r["pass_frac"]), r["tilt"], r["fwd"], r["out"], r["head_out"], r["edge"], turn)))
        if not ok:
            fails.append("HOLD %s" % cn)
    for cn in STRIKES:
        e = c.get(cn, {}).get("edge_lead")
        if not e:
            continue
        if "swing_mean" not in e:
            rows.append(("EDGE", cn, "FAIL", "not measurable: a legacy table has no active-swing measurement "
                                            "(re-measure with guard_accept.gd)"))
            fails.append("EDGE %s" % cn)
            continue
        ok = e["on_travel_strike"] >= EDGE_COS_STRIKE_MIN and e["swing_mean"] >= EDGE_COS_SWING_MIN
        rows.append(("EDGE", cn, "PASS" if ok else "FAIL",
                     "edge along the travel %+.2f at the strike (%.2f s; >= %.3f) and %+.2f over the swing "
                     "(%.2f-%.2f s; >= %.1f) | heading at the strike %+.0f deg (info) | whole-clip furthest "
                     "forward %.2f s: along %+.2f, heading %+.0f (info)"
                     % (e["on_travel_strike"], e["strike_t"], EDGE_COS_STRIKE_MIN, e["swing_mean"], e["swing"][0],
                        e["swing"][1], EDGE_COS_SWING_MIN, e["heading_strike"], e["strike_global_t"],
                        e["on_travel_global"], e["heading_global"])))
        if not ok:
            fails.append("EDGE %s" % cn)
    for cn in arcs:
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
    for cn in holds + STRIKES:
        if cn not in c or "pen_max" not in c[cn]:
            continue
        r = c[cn]
        ok = r["pen_max"] == 0
        rows.append(("PEN", cn, "PASS" if ok else "FAIL",
                     "axe vertices inside the body (fist excluded): worst frame %d, %d of %d frames%s"
                     % (r["pen_max"], r["pen_frames"], r["frames"],
                        (" -- " + ", ".join("%s %d" % kv for kv in sorted(r["pen_parts"].items()))) if r.get("pen_parts") else "")))
        if not ok:
            fails.append("PEN %s" % cn)
    return rows, fails, flags


if __name__ == "__main__":
    t = json.load(open(sys.argv[1]))
    rows, fails, flags = gate(t)
    print("weapon gate on '%s' (axe on %s, %d bones, %s)" % (t.get("label"), t.get("axe_bone"), t.get("bones", 0),
                                                           "measured through the tree" if t.get("source") == "tree" else "legacy: raw clips"))
    for r in rows:
        print("  %-4s %-15s %-4s  %s" % r)
    print("  VERDICT: %s (%d fail, %d trail flag)" % ("FAIL" if fails else "PASS", len(fails), len(flags)))
    if "--json" in sys.argv:
        json.dump(dict(rows=rows, fails=fails, flags=flags), open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if fails else 0)
