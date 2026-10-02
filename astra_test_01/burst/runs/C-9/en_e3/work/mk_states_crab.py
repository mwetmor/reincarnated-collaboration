import json, math
d = json.load(open('export/crab/crab.rig.json'))['landmarks']
L = lambda a, b: round(math.dist(a, b), 4)
cl = d['claw_L']; cr = d['claw_R']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_slam": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "claw_L_tip", "skill": "the roster's claw slam (melee 0-3.09 m); release = both claws striking the ground"},
  "attack_strike": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "claw_L_tip", "skill": "the roster's spout strike / shell spin (melee); release = the left claw's stab"},
  "cast_breath": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "mouth", "skill": "the roster's freezing breath (aoe wave 3.5 m x 1 m, cold)"},
  "cast_lob": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "claw_L_tip", "skill": "the roster's lobbed spout (projectile, area r 3 m)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "mouth": {"bone": "Hips", "along_bone_m": 0.9, "local_m": [0.0, 0.0, -0.12], "_what": "the mouth plates under the shell's front edge (shell bone rear->front 0.70 m, +0.20 m beyond, 0.12 m down)"},
  "claw_L_tip": {"bone": "claw_L_3", "along_bone_m": L(cl['wrist'], cl['tip']), "_what": "the LEFT pincer tip (wrist -> tip, measured)"},
  "claw_R_tip": {"bone": "claw_R_3", "along_bone_m": L(cr['wrist'], cr['tip']), "_what": "the RIGHT pincer tip"},
  "head_top": {"bone": "Hips", "along_bone_m": 0.35, "local_m": [0.0, 0.0, 0.45], "_what": "the top of the shell (HUD anchor)"},
  "chest": {"bone": "Hips", "along_bone_m": 0.35, "_what": "the shell's centre"}}}
json.dump(st, open('work/states_crab.json', 'w'), indent=1); print('states_crab ok')
