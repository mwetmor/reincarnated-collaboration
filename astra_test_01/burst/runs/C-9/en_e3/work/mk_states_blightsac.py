import json, math
d = json.load(open('export/blightsac/blightsac.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']; ztop = d['z_body_top']; zc = d['body_c'][2]
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "cast_breath": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "maw", "skill": "the roster's acid breath (cone 3.5 m x 1 m)"},
  "cast_orb": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's poison orb (projectile)"},
  "cast_aura": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "crown", "skill": "the roster's caustic presence (aura r 3.5 m)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl), (0, y0 + 0.04, zl - 0.08)), 4), "_what": "the lower lip of the mouth ring"},
  "crown": {"bone": "crown", "along_bone_m": round(ztop - 0.05 - (zc + 0.05), 4), "_what": "the vents on the back (the haze leaves here)"},
  "head_top": {"bone": "crown", "along_bone_m": round(ztop - 0.05 - (zc + 0.05), 4), "local_m": [0.0, 0.0, 0.15], "_what": "above the vents (HUD anchor)"},
  "chest": {"bone": "Hips", "_what": "the sac's centre"}}}
json.dump(st, open('work/states_blightsac.json', 'w'), indent=1); print('states_blightsac ok')
