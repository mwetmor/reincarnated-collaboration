import json, math
d = json.load(open('export/bloom/bloom.rig.json'))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "attack_bite": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's snapping bite (melee 0-2.86 m)"},
  "cast_spit": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the roster's venom seed (mortar projectile 3.6-23 m)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True},
  "spawn": {"kind": "oneshot", "role": "oneshot", "frames": 12, "sampling": "ends", "skill": "the p05 sprout (1.5 s): grows up out of the floor"}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl + 0.02), (0, y0 + 0.05, zl - 0.06)), 4), "_what": "the jaw tip (the seed leaves here; the bite lands here)"},
  "head_top": {"bone": "head", "along_bone_m": 0.1, "local_m": [0.0, 0.0, 0.35], "_what": "the top of the pod head (HUD anchor)"},
  "chest": {"bone": "stem2", "_what": "the upper stem"}}}
json.dump(st, open('work/states_bloom.json', 'w'), indent=1); print('states_bloom ok')
