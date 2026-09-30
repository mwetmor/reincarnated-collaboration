# T12 rank 6, checks 2-7: the WEAPON GATE, read off a measured table.
#
#   python3 scripts/53_weapon_gate.py <weapon_table.json> [--states a,b] [--strikes a,b|none] [--json out]
#
# The table is measured in Godot and archived beside the export it describes (nb_d2/tables/):
#   attack_lab/t12/godot/tools/guard_accept.gd   "source": "tree" -- the HOLD STATES as the scene
#       plays them (idle, walk, run, block, both strafes: through the AnimationTree, every layer
#       on) and the STRIKES fired through the tree too (the one-shot, its fades, the recovery
#       release), each row keyed by its clip with "strike_key" slash / chop / bash. Since T12 (c)
#       the axe arm's guard and its release are RUNTIME layers (knight.gd's blend_r and rel_<key>),
#       so a raw clip carries neither by design, and both are measured where they are made.
#   attack_lab/t12/godot/tools/hold_table.gd     legacy, no "source" -- every clip raw.
# Check 1, SKELETON IDENTITY, is a rule in 21_lint_export.py.
#
# RULES
#   HOLD  (check 2)  every hold state -- idle, walk, run, block, both strafes (legacy: the armed hold
#                    clips) -- holds the axe at GUARD on at least 90% of its frames: tilt 30-60 deg
#                    from vertical, haft forward and outboard, head outboard of the fist, |edge
#                    heading| <= 45 deg. FAIL below.
#   EDGE  (check 3)  each AXE strike's (the slash, the chop) EDGE LEADS: the edge lies ALONG THE
#                    HEAD'S TRAVEL (the edge direction against the travel with its along-haft part
#                    removed) -- cos >= 0.707 (45 deg) at the STRIKE FRAME, AND the speed-weighted
#                    mean over the ACTIVE SWING >= 0.8. The active swing is the clip's own (found on
#                    the raw clip): the frames contiguous with the head's peak speed at >= 50% of it;
#                    the strike frame is the frame inside it where the head reaches furthest forward
#                    of the hips. The edge's heading against his forward is REPORTED, not gated.
#   ARC   (check 4)  the axe head's screen path over one loop of the idle and each locomotion state
#                    <= 60 px in every play-camera cell (the waffle budget, from walk_armed's own
#                    25-46 px). FAIL over. A strike whose peak single-frame step exceeds 35 px
#                    (a quarter of the 140 px figure) is FLAGGED: it needs a trail.
#   PEN   (check 5)  no axe vertex inside the body on any frame of any hold state or strike, the
#                    hand that holds it excluded. FAIL on any. The instrument (guard_accept.gd,
#                    _pen): every 4th axe vertex; INSIDE = an odd number of crossings along all SIX
#                    axis directions against the posed, CPU-skinned body with its morphs; the fist
#                    excluded geometrically (the stretch of haft the closed hand wraps, from the
#                    hand mesh) and any point the right hand encloses on all six sides.
#   TTI   (check 6)  each axe strike reaches its strike frame within 0.8 s of the fire.
#   READ  (check 7)  each axe strike's active swing draws the head >= 42 px across the screen in
#                    EVERY play-camera cell -- a 0.9 m vertical sweep, the camera's least visible
#                    direction (legolas 2026-09-29 Part 3: 0.603 x 0.9 m x 77.8 px/m).
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
#   2026-09-30  PEN INSTRUMENT, second version. The first counted a point inside when the rays up
#               AND down both crossed the body an odd number of times, the fist excluded when both
#               first hits were right-hand triangles. Probed on the re-sourced chop's raise, it
#               reported 20 points 8.7 cm "deep" where rays in the four other directions put every
#               one of them outside: the body mesh's own overlaps and open seams at the wrist and the
#               raised arm fool two opposite rays; a closed body answers odd in all six. Six rays,
#               and the fist taken from the hand mesh itself. Every table from here is measured with
#               it, before and after alike.
#   2026-09-30  STRIKES measured through the tree (the recovery release is a runtime rule), the
#               strike set taken from the table (rows with "strike_key"), the active swing taken
#               from the raw clip (through the tree, the fade-in is a fast move of the head into the
#               clip's first pose, and it is not a swing). TTI and READ added: the coordinator's
#               criteria for the re-sourced chop (time-to-impact <= 0.8 s; a readable arc at the play
#               camera), applied to every axe strike.
#   2026-09-30  HAND CONTACT, a named class (coordinator's POMMEL RULING, the JOIN sword): the pommel/butt
#               against the heel of ITS OWN holding hand is grip contact up to 2 cm, not penetration.
#               guard_accept.gd classes each inside point: zone butt (below the grip), the nearest surface
#               over the six rays a hand-dominant triangle of the holding hand, and no deeper than 2 cm.
#               Those are reported in the HAND row and taken out of PEN; anything deeper, or into the body
#               (hips, thigh), stays PEN. A table without the class (older) is judged as before.
#   2026-09-30  --states a,b,c / --strikes a,b (or none): gate a SUBSET -- the JOIN kit's hold states are idle,
#               walk and run (Whirlwind + Battle Orders: no block, no strafe, no strike).
#
# A standing gate: run on every staged set and reported; NOT wired to stop the export chain.
import json, sys

HOLD_STATES = ["idle", "walk", "run", "block", "strafe_l", "strafe_r"]
ARC_STATES = ["idle", "walk", "run", "strafe_l", "strafe_r"]
HOLD_CLIPS_LEGACY = ["idle_armed", "walk_armed", "run_armed", "run_armed_L", "run_armed_R",
                     "strafe_L_armed", "strafe_R_armed", "block"]
ARC_CLIPS_LEGACY = [c for c in HOLD_CLIPS_LEGACY if c != "block"]
STRIKES_LEGACY = ["attack", "attack_chop"]
AXE_KEYS = ("slash", "chop")
HOLD_MIN = 0.9
EDGE_COS_STRIKE_MIN, EDGE_COS_SWING_MIN = 0.707, 0.8
ARC_MAX_PX, STEP_FLAG_PX = 60.0, 35.0
TTI_MAX_S, READ_MIN_PX = 0.8, 42.0


def gate(table, states=None, strike_set=None):
    c = table["clips"]
    tree = table.get("source") == "tree"
    holds = HOLD_STATES if tree else HOLD_CLIPS_LEGACY
    arcs = ARC_STATES if tree else ARC_CLIPS_LEGACY
    if states is not None:
        holds = [h for h in holds if h in states]; arcs = [a for a in arcs if a in states]
    strikes = [k for k, v in c.items() if "strike_key" in v] or [s for s in STRIKES_LEGACY if s in c]
    if strike_set is not None:
        strikes = [k for k in strikes if c[k].get("strike_key", k) in strike_set or k in strike_set]
    axe = [s for s in strikes if c[s].get("strike_key", "slash" if s == "attack" else "chop") in AXE_KEYS]
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
    for cn in axe:
        e = c[cn].get("edge_lead")
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
                     "(%.2f-%.2f s; >= %.1f) | heading at the strike %+.0f deg (info)"
                     % (e["on_travel_strike"], e["strike_t"], EDGE_COS_STRIKE_MIN, e["swing_mean"], e["swing"][0],
                        e["swing"][1], EDGE_COS_SWING_MIN, e["heading_strike"])))
        if not ok:
            fails.append("EDGE %s" % cn)
        ok = e["strike_t"] <= TTI_MAX_S
        rows.append(("TTI", cn, "PASS" if ok else "FAIL", "strike frame %.2f s after the fire (<= %.1f)" % (e["strike_t"], TTI_MAX_S)))
        if not ok:
            fails.append("TTI %s" % cn)
        if "swing_arc_min" in c[cn]:
            ok = c[cn]["swing_arc_min"] >= READ_MIN_PX
            rows.append(("READ", cn, "PASS" if ok else "FAIL", "the swing draws the head %.0f-%.0f px across the 8 cells (>= %.0f)"
                         % (c[cn]["swing_arc_min"], c[cn]["swing_arc_max"], READ_MIN_PX)))
            if not ok:
                fails.append("READ %s" % cn)
    for cn in arcs:
        if cn not in c:
            continue
        ok = c[cn]["arc_max"] <= ARC_MAX_PX
        rows.append(("ARC", cn, "PASS" if ok else "FAIL",
                     "axe-head screen path %.0f-%.0f px per loop over the 8 cells (budget %.0f)"
                     % (c[cn]["arc_min"], c[cn]["arc_max"], ARC_MAX_PX)))
        if not ok:
            fails.append("ARC %s" % cn)
    for cn in strikes:
        if c[cn].get("step_max", 0.0) > STEP_FLAG_PX:
            rows.append(("ARC", cn, "FLAG", "peak step %.1f px > %.0f px: needs a trail" % (c[cn]["step_max"], STEP_FLAG_PX)))
            flags.append(cn)
    for cn in holds + strikes:
        if cn not in c or "pen_max" not in c[cn]:
            continue
        r = c[cn]
        ok = r["pen_max"] == 0
        rows.append(("PEN", cn, "PASS" if ok else "FAIL",
                     "axe vertices inside the body (the hand excluded): worst frame %d (%.3f m deep), %d of %d frames%s"
                     % (r["pen_max"], r.get("pen_depth_m", 0.0), r["pen_frames"], r["frames"],
                        (" -- " + ", ".join("%s %d" % kv for kv in sorted(r["pen_parts"].items()))) if r.get("pen_parts") else "")))
        if not ok:
            fails.append("PEN %s" % cn)
    for cn in holds + strikes:
        if cn not in c or not c[cn].get("hand_classed"):
            continue
        r = c[cn]
        rows.append(("HAND", cn, "PASS", "grip contact (the pommel in its own holding hand, <= 2 cm, the pommel ruling): %d points on the worst frame, "
                     "%.3f m deep, %d of %d frames%s" % (r["hand_contact_max"], r["hand_contact_depth_m"], r["hand_contact_frames"], r["frames"],
                                                        "" if r["hand_contact_max"] else " -- none")))
    return rows, fails, flags


if __name__ == "__main__":
    t = json.load(open(sys.argv[1]))
    a = sys.argv
    states = a[a.index("--states") + 1].split(",") if "--states" in a else None
    strike_set = ([] if a[a.index("--strikes") + 1] == "none" else a[a.index("--strikes") + 1].split(",")) if "--strikes" in a else None
    rows, fails, flags = gate(t, states, strike_set)
    print("weapon gate on '%s' (axe on %s, %d bones, %s)" % (t.get("label"), t.get("axe_bone"), t.get("bones", 0),
                                                           "measured through the tree" if t.get("source") == "tree" else "legacy: raw clips"))
    for r in rows:
        print("  %-4s %-16s %-4s  %s" % r)
    print("  VERDICT: %s (%d fail, %d trail flag)" % ("FAIL" if fails else "PASS", len(fails), len(flags)))
    if "--json" in sys.argv:
        json.dump(dict(rows=rows, fails=fails, flags=flags), open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if fails else 0)
