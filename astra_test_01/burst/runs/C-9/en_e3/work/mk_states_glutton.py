import json, math
d = json.load(open('export/glutton/glutton.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']; aL = d['arms']['L']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_bite": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's charging bite (melee, poison)"},
  "attack_thrash": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "claw_L", "skill": "the roster's thrash (double rake)"},
  "cast_vomit": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "maw", "skill": "the roster's bile cone (5 m x 1-2 m)"},
  "cast_vomit3": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "maw", "skill": "the roster's violent barf (3 gobbets; they land as worm spawn)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl + 0.03), (0, y0 + 0.05, zl - 0.06)), 4), "_what": "the jaw tip"},
  "claw_L": {"bone": "arm_L_3", "along_bone_m": round(math.dist(aL['wr'], aL['tip']), 4), "_what": "the left claw tip (wrist -> tip)"},
  "head_top": {"bone": "chest", "local_m": [0.0, 0.0, 0.35], "along_bone_m": 0.0, "_what": "above the shoulder hump (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_glutton.json', 'w'), indent=1); print('states_glutton ok')
