# MX audition (R-C9-149): BATCHED e40a -- one Blender process converts a list of Mixamo FBX (read in place from
# reincarnated-godot/animations/mixamo; never copied) to rig-named GLBs, by running en_e2's e40a_mixamo_fbx.py UNCHANGED once per
# file with its own argv. One short heavy-lock job instead of N lock acquisitions (the lock was contended by KC2 + barrow_v2).
#   python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- blender -b -noaudio --python scripts/mx01b_batch.py -- <list.txt>
# list.txt: one line per clip, "<Pack>/<clip>" (no .fbx). Output mxglb/<tag>__<slug>.glb + .json; existing outputs are skipped.
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); E40A = os.path.join(HERE, '..', '..', 'en_e2', 'scripts', 'e40a_mixamo_fbx.py')
MX = os.path.expanduser('~/Games/reincarnated-godot/animations/mixamo'); OUT = os.path.join(HERE, '..', 'mxglb')
TAG = [('Not So Scary Zombie Pack', 'nsz'), ('Scary Zombie Pack', 'sz'), ('Creature NPC Pack', 'cnpc'), ('Creature Pack', 'cr')]
lst = sys.argv[sys.argv.index('--') + 1]
code = compile(open(E40A).read(), E40A, 'exec')
for ln in open(lst):
    ln = ln.strip()
    if not ln: continue
    pk, cl = ln.split('/', 1); tag = dict(TAG)[pk]; slug = re.sub(r'[()]', '', cl.lower()).replace(' ', '_')
    o = os.path.join(OUT, '%s__%s.glb' % (tag, slug))
    if os.path.exists(o): continue
    sys.argv = ['blender', '--', os.path.join(MX, pk, cl + '.fbx'), o, '--json', o[:-4] + '.json']
    try: exec(code, {'__name__': '__main__'})
    except Exception as e: print('MXFAIL', ln, repr(e)[:200])
