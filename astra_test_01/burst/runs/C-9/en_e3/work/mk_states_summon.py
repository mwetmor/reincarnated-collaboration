import json, math, sys
N = sys.argv[1]; d = json.load(open('export/%s/%s.rig.json' % (N, N)))['landmarks']
y0 = d['y_snout']; yh = d['y_hinge']; zl = d['z_lip']
st = {"states": {"idle": {"kind": "loop", "role": "locomotion_idle", "frames": 12, "sampling": "loop"}}, "sockets": {}}
if N == 'larva':
    st['states']['crawl'] = {"kind": "loop", "role": "locomotion_run", "frames": 12, "sampling": "loop"}
else:
    st['states']['emerge'] = {"kind": "oneshot", "role": "oneshot", "frames": 12, "sampling": "ends", "skill": "the stationary worm rises out of its burrow (it never travels)"}
st['states']['attack_bite'] = {"kind": "oneshot", "role": "oneshot_release", "frames": 12, "sampling": "release", "release_socket": "maw", "skill": "a sucker-maw lunge"}
st['states']['death'] = {"kind": "oneshot", "role": "oneshot_hold", "frames": 16, "sampling": "ends", "hold_last": True}
st['sockets'] = {"maw": {"bone": "jaw", "along_bone_m": round(math.dist((0, yh, zl), (0, y0 + 0.04, zl - 0.08)), 4), "_what": "the sucker maw"},
                 "head_top": {"bone": "head", "along_bone_m": 0.0, "local_m": [0.0, 0.0, 0.25 if N == 'worm' else 0.1], "_what": "above the maw (HUD anchor)"},
                 "chest": {"bone": "Hips", "_what": "the body's middle"}}
json.dump(st, open('work/states_%s.json' % N, 'w'), indent=1); print('states', N)
