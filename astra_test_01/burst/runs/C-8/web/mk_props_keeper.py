#!/usr/bin/env python3
"""Derive a per-character props set from CS-props-trio.

Matt's rule: each build's props exclude the character you are PLAYING, and only
that one. Precedent is runs/C-6/artifacts/CS-props-necro -- "the necro IS the
player" (runs/C-6 ledger, M-C6-P5-EXPORT).

CS-props-trio carries exactly two character stills:
    keeper_rest_still        the Keeper, resting
    necro_standing_still     the Necromancer, standing
and NO warlord still, so the trio set is already warlord-correct and only the
Keeper and Necromancer builds need a derived set.

NOTE ON THE EXISTING CS-props-necro: it drops BOTH stills, not just the necro.
It was derived from the older v25 props set, before the trio added the Keeper
still -- so it is not "trio minus necro", it is an earlier lineage that never had
the Keeper. Using it would have silently removed the Keeper statue from the
Necromancer's scene, which is not the rule. Hence this script builds a fresh
trio-minus-one for BOTH derived characters.

Idempotent: re-running on an already-pruned set is a no-op.
The loader requires exactly the six legacy collections plus optional
glows/swarms, so no key is added.

usage: mk_props_keeper.py <char>        char in {keeper, necro}
"""
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TRIO = HERE.parent.parent / 'C-6' / 'artifacts' / 'CS-props-trio'
DROP = {'keeper': 'keeper_rest_still', 'necro': 'necro_standing_still'}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in DROP:
        sys.exit('usage: mk_props_keeper.py {keeper|necro}')
    char = sys.argv[1]
    drop = DROP[char]
    root = HERE / 'props' / f'CS-props-{char}'

    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(TRIO, root)

    props = root / 'props.json'
    data = json.loads(props.read_text())
    before = (len(data['assets']), len(data['instances']))

    data['assets'] = [a for a in data['assets'] if a['name'] != drop]
    data['instances'] = [i for i in data['instances'] if i.get('asset') != drop]
    for key in ('shadows', 'overhead', 'near', 'particles', 'glows', 'swarms'):
        if isinstance(data.get(key), list):
            data[key] = [v for v in data[key] if drop not in json.dumps(v)]

    props.write_text(json.dumps(data, indent=2))

    png = root / 'assets' / (drop + '.png')
    if png.exists():
        png.unlink()

    after = (len(data['assets']), len(data['instances']))
    kept = [a['name'] for a in data['assets'] if a['name'].endswith('_still')]
    print(f'{char}: dropped {drop}; assets/instances {before} -> {after}; '
          f'stills kept {kept}')
    if after != (49, 49) or len(kept) != 1:
        sys.exit('unexpected counts after prune')


if __name__ == '__main__':
    main()
