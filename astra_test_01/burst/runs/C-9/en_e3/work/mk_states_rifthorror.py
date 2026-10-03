import json, math
d = json.load(open('export/rifthorror/rifthorror.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']; aL = d['arms']['L']; aR = d['arms']['R']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_swipe": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "spike_L", "skill": "basic melee: a double rake of the great spike-arms"},
  "attack_impale": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "spike_L", "skill": "the roster's impale (melee 0-2.59 m, slow): both spikes driven down into the target"},
  "cast_rift": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "chest", "skill": "the roster's rift vortex (projectile aoe r 3.75 m, range 16.3 m): the arms throw forward"},
  "cast_drain": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "chest", "skill": "the roster's life-drain nova (r 4 m around itself); the tentacle summon shares this clip"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl + 0.03), (0, y0 + 0.05, zl - 0.06)), 4), "_what": "the slit mouth"},
  "spike_L": {"bone": "arm_L_3", "along_bone_m": round(math.dist(aL['wr'], aL['tip']), 4), "_what": "the left bone-spike tip (wrist -> tip)"},
  "spike_R": {"bone": "arm_R_3", "along_bone_m": round(math.dist(aR['wr'], aR['tip']), 4), "_what": "the right bone-spike tip"},
  "head_top": {"bone": "chest", "local_m": [0.0, 0.0, 0.45], "along_bone_m": 0.0, "_what": "above the hump and tentacle crown (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_rifthorror.json', 'w'), indent=1); print('states_rifthorror ok')
