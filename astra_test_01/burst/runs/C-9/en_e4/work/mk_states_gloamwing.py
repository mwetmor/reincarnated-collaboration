import json, math
d = json.load(open('export/gloamwing/gloamwing.rig.json'))['landmarks']
L = lambda a, b: round(math.dist(a, b), 4)
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_claw": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "talon_L", "skill": "the talon rake (melee; the record's SpellAttack clip: vitality wave / gas cloud on h03 / h02)"},
  "attack_peck": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "the beak strike (basic attack b)"},
  "cast_breath": {"kind": "oneshot", "role": "oneshot_release", "frames": 24, "sampling": "release", "release_socket": "maw", "skill": "DARK BREATH (projectile burst 2-3 sparks, 13 metres per second, area 1 m); release = the first burst; the clip's later bursts are listed in the manifest"},
  "cast_roar": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "chest", "skill": "the aura toggle (BuffSelf clip): the dark aura switches on at the release"},
  "emerge": {"kind": "oneshot", "role": "oneshot", "frames": 16, "sampling": "ends", "skill": "the p05 drop-in (1667 ms; shown from frame 1, mortal at the last frame)"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "maw": {"bone": "jaw", "along_bone_m": round(0.85 * L((0, d['y_hinge'], d['z_lip']), (0, d['y_snout'], d['z_lip'])), 4), "_what": "near the beak tip"},
  "talon_L": {"bone": "leg_FL_3", "along_bone_m": L(d['leg_FL']['ankle'], d['leg_FL']['toe']), "_what": "the LEFT fore-foot's talon tips"},
  "head_top": {"bone": "head", "along_bone_m": 0.10, "local_m": [0.0, 0.0, 0.15], "_what": "the crown (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_gloamwing.json', 'w'), indent=1); print('states_gloamwing ok')
