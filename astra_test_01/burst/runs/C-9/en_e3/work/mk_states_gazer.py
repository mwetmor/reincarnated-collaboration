import json, math
d = json.load(open('export/gazer/gazer.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "cast_glare": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "eye_L", "skill": "the roster's petrifying glare (cone 6 m x 1.4-2 m); the eyes flare (runtime sprite at eye_L/eye_R)"},
  "cast_breath": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "maw", "skill": "the roster's acid retch (cone 4 m x 2 m)"},
  "attack_tail": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "chest", "skill": "the roster's tail swipe (aoe r 3.8 m)"},
  "cast_spit": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's acid spit (projectile 18 m/s)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl + 0.03), (0, y0 + 0.05, zl - 0.06)), 4), "_what": "the jaw tip"},
  "head_top": {"bone": "head", "along_bone_m": 0.15, "local_m": [0.0, 0.0, 0.2], "_what": "the horn crown (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
for k, v in d['eye_sockets_head_local'].items():
    st['sockets']['eye_' + k] = {"bone": "head", "along_bone_m": v[1], "local_m": [v[0], 0.0, v[2]],
                                 "_what": "the %s eye's centre (n09b, from the painted eye on the surface), head-bone rest frame" % k}
json.dump(st, open('work/states_gazer.json', 'w'), indent=1); print('states_gazer ok', list(st['sockets']))
