import json, math
d = json.load(open('export/rimethorn/rimethorn.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']; fl = d['leg_FL']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_swipe": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "claw_FL", "skill": "the roster's ice slash (melee 0-2.98 m); release = the cross-swipe contact"},
  "cast_impale": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "claw_FL", "skill": "the roster's avalanche (aoe wave 16 m x 2 m) -- the forefeet slam"},
  "cast_shards": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's ice shard burst (projectile)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl + 0.03), (0, y0 + 0.05, zl - 0.06)), 4), "_what": "the jaw tip"},
  "claw_FL": {"bone": "leg_FL_3", "along_bone_m": round(math.dist(fl['ankle'], fl['toe']), 4), "_what": "the left fore-claw tip"},
  "head_top": {"bone": "chest", "along_bone_m": 0.0, "local_m": [0.0, 0.0, 0.55], "_what": "the thorn hump (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_rimethorn.json', 'w'), indent=1); print('states_rimethorn ok')
