import json, math, sys
d = json.load(open(sys.argv[1]))['landmarks']; out = sys.argv[2]
cl = d['claw_L']; L = lambda a, b: round(math.dist(a, b), 4)
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_impale": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "scythe_L", "skill": "the roster's impale (melee, bleeding)"},
  "attack_slash": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "scythe_L", "skill": "a single-scythe slash"},
  "cast_spit": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "mouth", "skill": "the roster's spit burst (boss: + the chaos wave)"},
  "cast_rear": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "mouth", "skill": "the casting stance (blood pool lob)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "mouth": {"bone": "Hips", "along_bone_m": 1.3, "local_m": [0.0, 0.0, -0.35], "_what": "the mandibles at the front of the shell (shell bone rear->front 0.70 m, +0.6 m beyond, 0.35 m down)"},
  "scythe_L": {"bone": "claw_L_1", "along_bone_m": 0.0, "local_m": [0.0, 0.0, 0.0], "_what": "the left scythe's shoulder (the whole blade is rigid on this bone; the tip is at the rest offset below)"},
  "head_top": {"bone": "Hips", "along_bone_m": 0.35, "local_m": [0.0, 0.0, 0.8], "_what": "above the shell (HUD anchor)"},
  "chest": {"bone": "Hips", "along_bone_m": 0.35, "_what": "the shell's centre"}}}
json.dump(st, open(out, 'w'), indent=1); print('states ok', out)
