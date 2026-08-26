import sys, json, time, traceback
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline')
from frame_forensics_depth import analyse_depth
# The RADIAL archetypes -- payload is a burst or a field, not a streak, so the
# axial F1/F2 question is ill-posed and the axis gate refuses them. These are
# exactly the rows G-7 exists for.
MAP = [("R_ground_targeted_circle", "media/wizard_meteor.flv"),
       ("R_ground_slam",            "media/barbarian_hammer-of-the-ancients.flv"),
       ("R_circle_ring",            "media/demon-hunter_fan-of-knives.flv"),
       ("R_aura",                   "media/monk_mantra-of-conviction.flv"),
       ("R_whirlwind",              "media/barbarian_whirlwind.flv"),
       ("R_vortex_pull",            "media/monk_cyclone-strike.flv"),
       ("R_OURS_ground_slam",       "/Users/admin/Games/reincarnated-godot/harness_logs/mp4_review_2026-08-25_v3/05_ground_slam_CATHEDRAL.mp4")]
out={}
for row, path in MAP:
    t0=time.time()
    try:
        r = analyse_depth(path, row, w=1280, h=720, fps=30.0)
        out[row] = {"media": path, "summary": r["summary"], "derived": r["derived"],
                    "meta": r["meta"]}
        print(f"{row:26s} ok {time.time()-t0:5.0f}s", flush=True)
    except Exception as e:
        out[row] = {"media": path, "error": repr(e)}
        print(f"{row:26s} ERR {e}", flush=True); traceback.print_exc()
    json.dump(out, open("out/radial_depth.json","w"), indent=2, default=str)
print("DONE-RADIAL")
