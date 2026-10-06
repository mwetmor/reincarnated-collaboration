import sys, json, sqlite3, dataclasses
root, db, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root)
from reincarnated.simulation.kit_compiler.kit_compiler import compile_kit
from reincarnated.simulation.kit_compiler.kit_reader import CorpusKitReader
from reincarnated.simulation.kit_compiler.acceptance import author_asserts
r = CorpusKitReader(db)
ids = [x[0] for x in sqlite3.connect(f'file:{db}?mode=ro', uri=True).execute('select kit_id from canon_corpus order by kit_id')]
res = {}
for k in ids:
    try:
        ck = compile_kit(k, r)
        d = {'element': ck.element, 'class_dict': ck.class_dict, 'notes': ck.notes,
             'skills': [s.skill_dict for s in ck.skills]}
        try:
            d['asserts'] = [dataclasses.asdict(a) for a in author_asserts(ck, r)]
        except Exception as e:
            d['asserts'] = 'ERR ' + repr(e)[:120]
        res[k] = d
    except Exception as e:
        res[k] = 'ERR ' + type(e).__name__ + ' ' + str(e)[:150]
json.dump(res, open(out, 'w'), sort_keys=True, default=repr)
print(len(ids), sum(1 for v in res.values() if isinstance(v, str)))
