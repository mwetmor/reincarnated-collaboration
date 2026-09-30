# The D7 manifest. Every duration is READ FROM THE SHIPPED GLB (46_clip_timing), never typed:
# the barbarian's manifest once carried 0.667 s for a clip that was 0.8333 s, and the scene read it.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
T = __import__('46_clip_timing')
L = __import__('21_lint_export')
W = lambda f: json.load(open(os.path.join(ROOT, "work", f)))
glb = os.path.join(ROOT, "export", "so-body.glb")
tim, mpu = T.timing(glb)
lint = L.lint(glb)
g, _ = L.load_glb(glb)
joints = [g['nodes'][i]['name'] for i in g['skins'][0]['joints']]
casts, fl, asm = W("s5_casts.json"), W("s6_footlock.json"), W("s9_assemble.json")
m = dict(
  character="the ember seeress (D7, Matt R-C9-80; Costume A, base SO-1 b, Matt G1-S)",
  body="so-body.glb", height_m=1.70,
  height_note=("authored at 1.70 m, 0.92x the barbarian's 1.85 m. If the scene normalises each "
               "character to a fixed pixel height she will read as tall as him -- apply the "
               "BARBARIAN's world factor to her too so the difference survives."),
  facing="-Y", his_right="-X", up="+Z",
  skeleton=dict(joints=len(joints), weapon_r_index=joints.index("weapon_r"),
                weapon_l_index=joints.index("weapon_l"),
                note=("26 joints, weapon_r/weapon_l APPENDED last (indices 24, 25) by 52_weapon_bones, "
                      "identical in the body and every piece (gear.gd compares the lists in order). "
                      "Indices match legolas's Godot 4.6.3 probe of the convention.")),
  clips=sorted(tim), fps=24,
  clip_selection=dict(
    idle="idle", walk="walk", run="run", hit="hit", death="death",
    cast=dict(fireball="cast_fireball", meteor="cast_meteor"),
    staff="the staff is on weapon_r; the grip calibration (--roll) and off-hand IK are a later step"),
  locomotion_in_place=dict(
    rule="locomotion ships IN PLACE. Drive her at the FOOT-LOCK speed: the speed that holds the planted foot still.",
    walk=dict(seconds=tim["walk"]["seconds"], speed_m_s=fl["clips"]["walk"]["foot_lock_speed_m_s"],
              planted_intervals=fl["clips"]["walk"]["planted_intervals"]),
    run=dict(seconds=tim["run"]["seconds"], speed_m_s=fl["clips"]["run"]["foot_lock_speed_m_s"],
             planted_intervals=fl["clips"]["run"]["planted_intervals"],
             caution="only 10 planted intervals (a run's contacts are brief): the widest estimate here"),
    method=("Meshy's walk and run are in place AT SOURCE (net root travel 0.000 / 0.004 m), so "
            "travel/duration gives ~0. The planted foot slides back at exactly her ground speed; "
            "the median of that, over intervals with the foot down at both ends, is the speed.")),
  casts={
    "cast_fireball": dict(release_s=casts["decision"]["fireball"]["release_s"],
                          source="Meshy 132 Mage Spell Cast 3", why=casts["decision"]["fireball"]["why"],
                          definition=casts["decision"]["release_s_definition"]["fireball"]),
    "cast_meteor": dict(release_s=casts["decision"]["meteor"]["release_s"],
                        source="Meshy 127 Charged Ground Slam", why=casts["decision"]["meteor"]["why"],
                        definition=casts["decision"]["release_s_definition"]["meteor"])},
  root_motion=dict(
    in_place=["walk", "run", "idle", "hit", "death"],
    hit_travel_m=1.1953, death_travel_m=0.9783,
    note=("hit and death carried ~1 m of knockback; shipped IN PLACE with the travel here, so the "
          "scene can re-apply it if the design wants the capsule to move. The casts do not drift.")),
  clip_hygiene=dict(
    joint_scale=("idle AND walk ('Walking Woman') both arrived with Meshy's constant Hips scale "
                 "1.176471 -- the barbarian's defect, in two clips. The ARRIVAL LINT RECORDED BOTH AS "
                 "FAIL; stripped and re-grounded from the feet (min rule)."),
    stripped=W("s6_hygiene.json")["stripped"]),
  gear=dict(layer_order=["body", "robe", "belt", "mantle", "bracers", "circlet", "staff"],
            pieces={k: v for k, v in asm["pieces"].items()},
            isolation_predicates=dict(
              note="recorded here because D2's were passed on the command line and lost",
              robe=dict(region="robe", seed="(gr < 0.62) & (sat > 0.45) & (dist > 0.02)",
                        grow="((gr < 0.66) & (sat > 0.42) & (val > 0.24)) | ((dist > 0.03) & (gr < 0.70) & (val > 0.24))"),
              mantle=dict(region="shoulders", seed="(sat < 0.28) & (val > 0.25) & (dist > 0.025) & (zf > 0.70)",
                          grow="(sat < 0.34) & (val > 0.22) & (dist > 0.008) & (zf > 0.64)"),
              belt=dict(region="waist", seed="(val < 0.34) & (dist > 0.006) & (zf > 0.49) & (zf < 0.64) & (ax > 0.04)",
                        grow="(val < 0.42) & (dist > 0.003) & (zf < 0.68) & ((zf > 0.49) | ((zf > 0.38) & (ax > 0.08)))"),
              bracers=dict(region="forearms", seed="(val < 0.34) & (dist > 0.004)", grow="(val < 0.42) & (dist > 0.002)"),
              circlet="PROCEDURAL -- see gear.pieces.circlet")),
  texture=dict(sheet_A=W("sopa_pick.json"), sheet_B=W("sopb_pick.json"),
               unseen_pct=24.361, sheetB_unpainted_share_pct=W("sheetB_blind_share.json")["overall_pct"]),
  lint=dict(verdict=lint["verdict"], fails=lint["fails"], warns=len(lint["warns"])))
json.dump(m, open(os.path.join(ROOT, "export", "manifest.json"), "w"), indent=1)
print("manifest: %d clips, casts %s, locomotion walk %.3f run %.3f m/s, lint %s"
      % (len(tim), {k: v["release_s"] for k, v in m["casts"].items()},
         m["locomotion_in_place"]["walk"]["speed_m_s"], m["locomotion_in_place"]["run"]["speed_m_s"], lint["verdict"]))
