import json, math
d = json.load(open('export/raptor/raptor.rig.json'))['landmarks']
L = lambda a, b: round(math.dist(a, b), 4)
a = d['arms']['L']; lr = d['leg_R']; y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_swipe": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "claw_L_tip", "skill": "the roster's double swipe (melee 0-2.95 m); release = the left rake's contact"},
  "attack_kick": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "sickle_R", "skill": "the roster's leg claw (melee 0-3.02 m); release = the sickle claw's stab"},
  "attack_leap": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "chest", "skill": "the roster's leap (aoe r 2.8 m at landing); release = the landing; the travel is the runtime's"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": L((0, yh, zl + 0.03), (0, y0 + 0.06, zl - 0.05)), "_what": "the jaw tip"},
  "claw_L_tip": {"bone": "arm_L_3", "along_bone_m": L(a['wr'], a['tip']), "_what": "the LEFT forelimb's claw tip (wrist -> tip, measured)"},
  "sickle_R": {"bone": "leg_R_3", "along_bone_m": L(lr['ankle'], lr['ball']), "_what": "the RIGHT foot's ball, where the sickle claw sits"},
  "head_top": {"bone": "head", "along_bone_m": 0.15, "local_m": [0.0, 0.0, 0.18], "_what": "the crest at the back of the skull"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_raptor.json', 'w'), indent=1); print('states_raptor ok')
