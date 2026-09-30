# The JOIN sword's manifest: every number read from the record its step wrote.
#   python3 scripts/w8_manifest.py      -> export/sword_manifest.json
import hashlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = lambda *p: os.path.join(ROOT, *p)
J = lambda *p: json.load(open(W(*p)))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
sk = J("work", "w3_skin.json"); pa = J("work", "w5_pairing.json")
# 2026-09-30: roll 0 ADOPTED (conductor), -39 WITHDRAWN. The guard numbers are the FIXED instrument's re-measure at roll 0
# (w5_measure.py header: Blender held the un-keyed weapon_r at the file's first animation's pose); the -39 record stays
# as w5_mount.json for the history, and its idle edges are void.
mo = J("work", "w5_mount_roll0_fixed.json"); mo_void = J("work", "w5_mount.json"); mo0_void = J("work", "w5_mount_roll0.json")
ro = J("work", "w6_roll.json"); al = J("work", "w7_axe_left.json"); cl = J("work", "w2_clean.json")
m0 = J("work", "w1_measure_NB-W2_a.json"); m1 = J("work", "w1_measure_NB-W2L.json")
tr = J("work", "tripo_sword.json"); led = J("work", "fal_spend_R-C9-81.json"); t12 = J("t12_5_guard", "weapon_mount.json")
rcpt = json.load(open(os.path.join(os.path.dirname(ROOT), "artifacts", "NB-W2L", "receipt.json")))
rows = {}
for e in (json.loads(l) for l in open(W("work", "timing.jsonl")) if l.strip()):
    r = rows.setdefault(e["step"], dict(start=None, end=None, wait=0.0))
    if e["ev"] == "start" and r["start"] is None: r["start"] = e["t"]
    elif e["ev"] == "end": r["end"] = e["t"]
    elif e["ev"] == "wait": r["wait"] += e["s"]
timing = {k: dict(wall_s=round(v["end"] - v["start"]), vendor_wait_s=round(v["wait"]), agent_s=round(v["end"] - v["start"] - v["wait"]))
          for k, v in rows.items() if v["start"] and v["end"]}
tot = {k: sum(x[k] for x in timing.values()) for k in ("wall_s", "vendor_wait_s", "agent_s")}
man = {
    "piece": "the JOIN SWORD, main hand (Matt R-C9-81: sword right, bearded axe left)",
    "file": "sword.glb", "sha256": sha(W("export", "sword.glb")), "bytes": os.path.getsize(W("export", "sword.glb")),
    "mesh": dict(verts=sk["verts"], tris=sk["tris"], islands=cl["islands"]["count"], welded_before_decimation=cl["welded"],
                 budget="9,000 triangles, the axe's"),
    "skeleton": dict(joints=sk["joints"], weapon_r_index=sk["weapon_r_joint_index"],
                     note="the T12_5_guard skeleton, joint list identical in name and order (gear.gd compares them); 100% on weapon_r"),
    "lint": sk["lint"],
    "frame": sk["frame"] + " -- the axe's convention (52_weapon_bones), so the mount code is shared",
    "dims_m": sk["features"],
    "dims_note": "overall set to 0.90 m; the rest follows the painted proportions (blade/grip 4.82 on the sheet, 5.20 on the model, "
                 "whose grip band ends at the collars). The dispatch's 5x and its 72 cm / 11-12 cm targets disagree (72/11.5 = 6.3x); "
                 "0.90 m overall gives a 68 cm blade and a 13 cm grip including both bronze collars. Blade thickness: Tripo made the "
                 "edge-on line 2.3 cm; thinned x0.5 to 1.2 cm over the blade only (above the guard, blended over 1 cm).",
    "sockets": dict(sk["sockets"], contract="reincarnated-godot docs/join1-sprite-cell-contract-2026-09-29.md 3.2/5: main_tip, main_grip "
                    "(the main hand carries the sword). Child nodes of weapon_r; gear.gd's marker path brings them onto the body.",
                    read_back="Godot, bound gear.gd's way, at idle_guard: main_tip 0.7768 m from main_grip; tip height 1.4869 m against "
                              "Blender's 1.4860 from the skinned geometry"),
    "mount": dict(method="T12: the SQUARE SEAT (the blade turned onto the fist's channel, gearlib.hand_frame); NO roll",
                  seat="the T12_5_guard mount (weapon_mount.json, 52_weapon_bones --roll 0): the channel is the hand's, not the weapon's",
                  roll_deg=ro["roll_deg"],
                  roll_withdrawn=dict(
                      was_deg=-39.0,
                      why="the scene drax gated the sword through the scene's tree (53_weapon_gate): at roll 0 its edge sits exactly on the "
                          "axe's, and -39 FAILS the edge row on both strikes (+0.71, +0.64). The -39 fit minimised |edge| over hold rows whose "
                          "IDLE half was measured with the sword turned 65.74 deg about its blade -- Blender held weapon_r, which idle_guard "
                          "does not key, at the file's first animation's pose (attack's first key), where glTF and Godot put it at rest. The "
                          "roll corrected the instrument, not the sword. Found bone by bone: every joint's Blender pose matched the "
                          "glTF-evaluated global to 0.00 deg except weapon_r, 65.74, in idle_guard only; walk_armed, which keys weapon_r, "
                          "measured 0.6 deg off (the PCA's own 0.57).",
                      void_records=dict(idle_edge_roll0=mo0_void["idle"]["median"]["edge"], idle_edge_roll_m39=mo_void["idle"]["median"]["edge"]),
                      fix="w5_measure.py bind() resets every pose bone to rest before binding a clip"),
                  seat_measured=mo["seat"], fist_centroid_to_main_grip_m=mo["idle"]["median"]["fist_to_grip_m"],
                  body="export/nb-body_sword.glb: the T12_5_guard body, BYTE-IDENTICAL (roll 0 is the T12_5 mount; w6_roll.py --roll 0 "
                       "copies it, sha %s)" % ro["sha256"][:12],
                  record_T12_5=t12),
    "guard_gate": dict(
        predicate="sword HOLD (the T12 gate adapted): blade tilt 30-60 deg from vertical, blade forward AND outboard, tip outboard of the "
                  "fist, |edge heading| <= 45 deg; the frame from the sword's own skinned geometry (grip = weapon_r's joint, blade = to "
                  "the farthest vertex, edge = the blade's widest spread)",
        instrument="w5_measure.py, FIXED 2026-09-30 (un-keyed channels at rest): its idle edge now agrees with the glTF-evaluated edge "
                   "to 0.6 deg on every row. The walk's verdict still belongs to the scene's tree (the edge row on the strikes too)",
        idle=dict(clip="idle_guard", at_guard="%d/%d" % (mo["idle"]["at_guard"], mo["idle"]["frames"]), median=mo["idle"]["median"], pen=mo["idle"]["pen_max"]),
        walk=dict(clip="walk_armed + axe_guard_R right-arm layer", at_guard="%d/%d" % (mo["walk"]["at_guard"], mo["walk"]["frames"]),
                  median=mo["walk"]["median"], pen=mo["walk"]["pen_max"],
                  caveat="NOT knight.gd's tree (no armed-speed split): tilt exceeds 60 deg on 7 of 16 frames here; the T12 gate measured "
                         "the axe's walk at tilt 35 through the scene's tree. The walk's verdict belongs to guard_accept.gd in the scene."),
        pen_instrument="six-ray parity against the posed body with grip_R = 1; the grip's own length and anything within 2 cm of a "
                       "RightHand-weighted vertex excluded (the fist)"),
    "pairing_first_look": dict(file="axe_l.glb", what="the axe's right-hand placement mirrored across his sagittal plane onto weapon_l -- a "
                               "first look only, NOT an off-hand hold", rest_asymmetry_m=al["rest_asymmetry_m"],
                               axe_verts_in_body_idle_guard=mo.get("weapon_l_idle_guard_pen"), sword_to_axe_min_m=mo.get("weapon_to_weapon_min_m"),
                               measured="at roll 0 with the fixed instrument (work/w5_mount_roll0_fixed.json)"),
    "provenance": dict(
        source_sheet=dict(path="runs/C-9/artifacts/NB-W2/NB-W2_a.png", sha256="472639634e1e93fe337c024576913d1f1345859d9d0d01e3fbe911152bb39015",
                          blade_over_grip=m0["views"]["front"]["blade_over_grip"]),
        edit=dict(burst="NB-W2L", path="runs/C-9/artifacts/NB-W2L/NB-W2L.png", sha256=sha(os.path.join(os.path.dirname(ROOT), "artifacts", "NB-W2L", "NB-W2L.png")),
                  image_calls=rcpt["calls_used"], retries=len(rcpt.get("retries", [])), concerns=rcpt["self_report"]["concerns"],
                  blade_over_grip=m1["views"]["front"]["blade_over_grip"], views_total_spread_pct=m1["views_total_spread_pct"],
                  hilt=m1["views"]["front"]),
        matte="BiRefNet v2 (fal) through fal_ledger, W2's own ledger",
        tripo=dict(endpoint=tr["endpoint"], request_id=tr["request_id"], views=tr["views"], elapsed_s=tr["elapsed_s"], glb_mb=tr["glb_mb"], builds=1)),
    "budget": dict(astra_image_calls="1 of 2", fal=dict(ledger="work/fal_spend_R-C9-81.json", spent_usd=led.get("running_usd"), cap_usd=1.00,
                   entries=[(e["endpoint"], e["usd"]) for e in led["entries"]]), meshy_credits=0),
    "timing": dict(steps=timing, total=tot, note="WALL = end - start; VENDOR = the generator's own measured wait; AGENT = wall - vendor. "
                   "W2-S2-build was closed retroactively at W2-S3's start (the end call was missed)."),
    "deliverables": dict(stills="8 headings x idle_guard at 100.6 and 201.2 px/m (offscreen 1920x1080) + the pairing at 2 headings",
                         film="artifacts/W2-sword-film-2x.mp4 (1920x1080, 201.2 px/m, 255 frames: idle_guard, walk_armed + guard arm at 1.179 m/s, idle_guard)",
                         caution="the stills and the film were rendered at the WITHDRAWN -39 roll and are not re-rendered here: the blade's "
                                 "tilt and position are unchanged (the roll turns it about its own axis), its face is not"),
}
json.dump(man, open(W("export", "sword_manifest.json"), "w"), indent=1)
print("wrote export/sword_manifest.json; sword sha %s; timing total wall %ds (vendor %ds, agent %ds)" % (man["sha256"][:12], tot["wall_s"], tot["vendor_wait_s"], tot["agent_s"]))
