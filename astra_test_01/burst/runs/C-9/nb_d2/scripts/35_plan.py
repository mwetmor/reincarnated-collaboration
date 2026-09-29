# Choose the block and the armed locomotion BY MEASUREMENT, then write the
# merge plan the assembler reads.
#
#   python3 scripts/35_plan.py
#
# Meshy's library calls them "Block1".."Block10" with no other information, so
# the name cannot choose. A shield block raises the LEFT hand in front of the
# chest; a sword parry raises the RIGHT and sweeps across. guard_score is
# (left rise - right rise) + forward reach of the left hand, at the clip's peak.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
G = json.load(open(os.path.join(ROOT, "work", "guard_pick.json")))
# THE DISCRIMINATOR IS l_rise MINUS r_rise, not the composite guard_score.
#
# guard_score adds the left hand's FORWARD reach, and every clip in the set has
# a hand out in front, so the "<- LEFT ARM LEADS" label it drove fired on all
# eleven -- including an axe chop. A label that is true of everything says
# nothing. The rise difference separates them cleanly on the first read:
#
#   block1   L +0.472  R +0.419   left higher  -> a SHIELD block
#   block9   L +0.349  R +0.436   right higher -> a sword parry
#   block4   L +0.296  R +0.440   right higher -> a sword parry
#
# shield_push is excluded from the block choice on purpose: it scores highest of
# anything here (L +0.604 against R +0.146) but "Shield Push Left" is a SHOVE,
# an attack with the shield, not a block. It ships as its own clip.
BLOCKS = [k for k in G if k.startswith("block")]
sc = {k: G[k]["l_rise_max"] - G[k]["r_rise_max"] for k in BLOCKS}
rank = sorted(sc, key=lambda k: -sc[k])
print("block candidates by LEFT-minus-RIGHT hand rise:")
for k in rank:
    print("  %-12s L-R %+0.3f   left rise %+0.3f fwd %+0.3f | right rise %+0.3f  %s"
          % (k, sc[k], G[k]["l_rise_max"], G[k]["l_fwd_max"], G[k]["r_rise_max"],
             "SHIELD BLOCK" if sc[k] > 0 else "sword parry -- rejected"))
rank = [k for k in rank if sc[k] > 0]
best = rank[0] if rank else None
plan = {"idle_armed": "axe_stance", "walk_armed_m": "walk_fight",
        "run_armed_L": "run_fight_L", "run_armed_R": "run_fight_R",
        "attack_chop": "axe_chop"}
if best:
    plan["block"] = best
    print("chose %-12s as the block (L-R %+0.3f)" % (best, sc[best]))
else:
    print("NO fetched Block clip leads with the left arm -- that is a GAP")
if "shield_push" in G:
    plan["shield_bash"] = "shield_push"
    print("shield_push ships as shield_bash (a shove, not a block)")
gs = G.get("ss_alert_L", {})
print("guard source ss_alert_L: left rise %+0.3f fwd %+0.3f, peak score %+0.3f"
      % (gs.get("l_rise_max", 0), gs.get("l_fwd_max", 0),
         gs.get("peak", {}).get("guard_score", 0)))
json.dump(plan, open(os.path.join(ROOT, "work", "merge_plan.json"), "w"), indent=1)
print("wrote work/merge_plan.json: %s" % plan)
