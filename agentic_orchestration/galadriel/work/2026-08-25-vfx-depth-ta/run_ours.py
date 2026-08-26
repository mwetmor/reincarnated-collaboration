import sys, json, time, traceback
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline')
from frame_forensics_depth import analyse_depth
# OUR side of the five matched pairs. v3 is the set Matt verified by eye
# ("the _v3 mp4s from drax now have the character facing the correct way").
# v4 exists and is NOT owner-attested, so it is not the leg to report on.
B = "/Users/admin/Games/reincarnated-godot/harness_logs/mp4_review_2026-08-25_v3/"
MAP = [("OURS_dash_attack", B+"01_dash_attack_CATHEDRAL.mp4"),
       ("OURS_blink",       B+"02_blink_CATHEDRAL.mp4"),
       ("OURS_teleport",    B+"03_teleport_CATHEDRAL.mp4"),
       ("OURS_leap_strike", B+"04_leap_strike_CATHEDRAL.mp4"),
       ("OURS_ground_slam", B+"05_ground_slam_CATHEDRAL.mp4"),
       ("OURS_melee_combo", B+"06_melee_combo_CATHEDRAL.mp4")]
out={}
for row, path in MAP:
    t0=time.time()
    try:
        r = analyse_depth(path, row, w=1280, h=720, fps=30.0)
        out[row] = {"media": path, "raster": [1280,720], "meta": r["meta"],
                    "derived": r["derived"], "summary": r["summary"]}
        json.dump(r["series"], open(f"out/series_{row}.json","w"), default=str)
        print(f"{row:24s} ok  {time.time()-t0:5.0f}s", flush=True)
    except Exception as e:
        out[row] = {"media": path, "error": repr(e)}
        print(f"{row:24s} ERR {e}", flush=True); traceback.print_exc()
    json.dump(out, open("out/ours_depth.json","w"), indent=2, default=str)
print("DONE-OURS")
