import json, math
d = json.load(open('export/frosthorn/frosthorn.rig.json'))['landmarks']
y0 = d['y_snout']; yhb = d['y_head_base']; zl = d['z_lip']; fl = d['leg_FL']
st = {"states": {
  "idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"},
  "walk": {"kind": "loop", "role": "locomotion_walk", "frames": 12, "sampling": "loop"},
  "run": {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"},
  "attack_gore": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "horn", "skill": "the roster's gore (melee 0-2.99 m, bleed): the horn toss; release = the hook-up contact"},
  "attack_butt": {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "horn", "skill": "the basic melee lunge (attack_a01)"},
  "attack_charge": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "horn", "skill": "the charge special: coil then drive; the runtime moves the body"},
  "cast_roar": {"kind": "oneshot", "role": "oneshot_release", "frames": 16, "sampling": "release", "release_socket": "claw_FL", "skill": "the roar clip every cast fires on (novas, rings, fields): rear and stamp"},
  "hit": {"kind": "oneshot", "role": "oneshot", "frames": 8, "sampling": "ends"},
  "death": {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}},
 "sockets": {
  "horn": {"bone": "head", "along_bone_m": round(abs(yhb - y0), 4), "_what": "the front horn's tip end of the head (the gore lands here)"},
  "claw_FL": {"bone": "leg_FL_3", "along_bone_m": round(math.dist(fl['ankle'], fl['toe']), 4), "_what": "the left forefoot (the stamp)"},
  "head_top": {"bone": "chest", "along_bone_m": 0.0, "local_m": [0.0, 0.0, 0.7], "_what": "the shoulder hump (HUD anchor)"},
  "chest": {"bone": "chest", "_what": "the chest bone's head"}}}
json.dump(st, open('work/states_frosthorn.json', 'w'), indent=1); print('states_frosthorn ok')
