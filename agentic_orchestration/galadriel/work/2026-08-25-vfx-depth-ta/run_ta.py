import sys, json, time, traceback
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline')
from frame_forensics_depth import analyse_depth

# row -> (media file, raster, relation-to-T-A-canonical)
MAP = [
 ("whirlwind",              "media/barbarian_whirlwind.flv",              (1280,720)),
 ("melee_strike_CANON",     "media/le-rive.mp4",                          (1920,1080)),
 ("cone",                   "media/barbarian_seismic-slam.flv",           (1280,720)),
 ("dash_attack",            "media/barbarian_furious-charge.flv",         (1280,720)),
 ("ground_targeted_circle", "media/wizard_meteor.flv",                    (1280,720)),
 ("single_target",          "media/le-javelin.mp4",                       (1280,500)),
 ("ground_slam",            "media/barbarian_hammer-of-the-ancients.flv", (1280,720)),
 ("leap_strike",            "media/barbarian_leap.flv",                   (1280,720)),
 ("melee_arc",              "media/barbarian_cleave.flv",                 (1280,720)),
 ("melee_strike",           "media/monk_way-of-the-hundred-fists.flv",    (1280,720)),
 ("circle_ring",            "media/demon-hunter_fan-of-knives.flv",       (1280,720)),
 ("circle_ring_alt",        "media/wizard_wave-of-force.flv",             (1280,720)),
 ("vortex_pull",            "media/monk_cyclone-strike.flv",              (1280,720)),
 ("beam_channel",           "media/wizard_disintegrate.flv",              (1280,720)),
 ("chain",                  "media/wizard_electrocute.flv",               (1280,720)),
 ("teleport",               "media/wizard_teleport.flv",                  (1280,720)),
 ("blink",                  "media/monk_dashing-strike.flv",              (1280,720)),
 ("multi_projectile",       "media/demon-hunter_multishot.flv",           (1280,720)),
 ("orbit",                  "media/monk_sweeping-wind.flv",               (1280,720)),
 ("ricochet_bounce",        "media/demon-hunter_chakram.flv",             (1280,720)),
 ("fork",                   "media/demon-hunter_cluster-arrow.flv",       (1280,720)),
 ("placed_lane",            "media/witch-doctor_wall-of-zombies.flv",     (1280,720)),
 ("totem",                  "media/demon-hunter_sentry.flv",              (1280,720)),
 ("self_buff",              "media/barbarian_wrath-of-the-berserker.flv", (1280,720)),
 ("aura",                   "media/monk_mantra-of-conviction.flv",        (1280,720)),
 ("line_weak",              "media/wizard_arcane-orb.flv",                (1280,720)),
]
out={}
for row, path, (w,h) in MAP:
    t0=time.time()
    try:
        r = analyse_depth(path, row, w=w, h=h, fps=30.0)
        out[row] = {"media": path, "raster": [w,h], "meta": r["meta"],
                    "derived": r["derived"], "summary": r["summary"]}
        json.dump(r["series"], open(f"out/series_{row}.json","w"), default=str)
        print(f"{row:24s} ok  {time.time()-t0:5.0f}s", flush=True)
    except Exception as e:
        out[row] = {"media": path, "error": repr(e), "tb": traceback.format_exc()}
        print(f"{row:24s} ERR {e}", flush=True)
    json.dump(out, open("out/ta_depth.json","w"), indent=2, default=str)
print("DONE")
