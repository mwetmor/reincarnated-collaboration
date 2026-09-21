#!/usr/bin/env python3
"""Assemble three per-character Godot web exports into ONE shared-engine route.

Architecture (knight-rider amendment, 2026-09-21): a character is chosen BEFORE
the engine boots, so exactly one character's assets are ever downloaded. The
Godot engine (index.wasm / index.js / the audio worklets) is IDENTICAL across the
three exports -- same Godot build, same export preset, same options -- so it ships
once and the three builds contribute only their .pck.

This script refuses to proceed unless the engine files are byte-identical across
the three builds, because "one shared wasm" is a claim about bytes, not intent.
If a pck were ever built against a different engine, the page would fail at load
with an opaque error and the cause would be invisible.

Staged layout (loadout public/playtest/cliffside/):
    index.html            patched shell: ?c=<char> picks the pack
    index.js index.wasm   the shared engine, one copy
    index.audio*.js       shared
    index.icon.png index.apple-touch-icon.png index.png
    warlord.pck keeper.pck necro.pck

usage: assemble_trio.py <stage_root> <out_dir>
    stage_root holds stage-<char>/build/web for each character.
"""
import filecmp
import hashlib
import json
import pathlib
import re
import shutil
import sys

CHARS = ['warlord', 'keeper', 'necro']
BASE = 'warlord'          # the build whose shell + engine + splash are shipped
SHARED = ['index.js', 'index.wasm', 'index.audio.worklet.js',
          'index.audio.position.worklet.js', 'index.icon.png',
          'index.apple-touch-icon.png', 'index.png']
ENGINE_IDENTICAL = ['index.js', 'index.wasm', 'index.audio.worklet.js',
                    'index.audio.position.worklet.js']

# Injected ahead of `const engine = new Engine(GODOT_CONFIG);`. Keeps the
# generated shell's own logic untouched -- it only rewrites which pack is named.
PICKER = """
// --- character pack selection (drax, three-pck trio) ---------------------
// The pack is chosen before the engine boots; only one character's assets
// are ever fetched. An unknown or absent ?c= falls back to the default so a
// bare /playtest/cliffside/ URL still plays rather than 404-ing on a pack.
const GODOT_PACKS = __PACKS__;
const GODOT_DEFAULT_PACK = '__DEFAULT__';
(function () {
\tlet pick = new URLSearchParams(window.location.search).get('c') || '';
\tif (!Object.prototype.hasOwnProperty.call(GODOT_PACKS, pick)) {
\t\tpick = GODOT_DEFAULT_PACK;
\t}
\tGODOT_CONFIG['mainPack'] = GODOT_PACKS[pick].pack;
\tGODOT_CONFIG['fileSizes'] = {
\t\t[GODOT_PACKS[pick].pack]: GODOT_PACKS[pick].size,
\t\t'index.wasm': GODOT_CONFIG['fileSizes']['index.wasm'],
\t};
\tdocument.title = GODOT_PACKS[pick].label + ' \\u2014 Cliffside';
\t// Explicit window assignment: a top-level `const` in a classic script makes a
\t// global BINDING but not a window PROPERTY, so the chip script in <head>
\t// cannot see GODOT_PACKS by name. Publish what the chip actually needs.
\twindow.GODOT_PICKED = pick;
\twindow.GODOT_LABEL = GODOT_PACKS[pick].label;
}());
"""

# A persistent way back to the select screen. Matt is using this to compare
# animation styles, so returning to swap characters must not be a URL hunt.
# Pointer-events are off except on the chip itself, so it never eats input
# meant for the game, and it hides while a touch-joystick drag is live.
CHIP = """<style>
#char-chip{position:fixed;top:calc(env(safe-area-inset-top,0px) + 8px);
left:calc(env(safe-area-inset-left,0px) + 8px);z-index:20;display:flex;gap:8px;
align-items:center;font:600 13px/1 system-ui,-apple-system,sans-serif}
#char-chip a{display:block;padding:9px 13px;border-radius:999px;
background:rgba(11,15,22,.78);color:#e8eef7;border:1px solid rgba(143,200,255,.45);
text-decoration:none;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
#char-chip a:active{background:rgba(143,200,255,.9);color:#07111d}
#char-chip .who{color:#9aa8bb;padding:9px 0}
</style>
<script>addEventListener('DOMContentLoaded',function(){
var n=document.createElement('div');n.id='char-chip';
n.innerHTML='<a href="/play">\\u2190 Change character</a><span class="who"></span>';
n.querySelector('.who').textContent=window.GODOT_LABEL||'';
document.body.appendChild(n);
// Godot takes keyboard focus on the canvas; clicking the chip must not be
// swallowed by the canvas listener, hence the capture-phase stop.
n.addEventListener('pointerdown',function(e){e.stopPropagation();},true);
});</script>"""


def sha(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit('usage: assemble_trio.py <stage_root> <out_dir>')
    root = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()

    builds = {}
    for char in CHARS:
        web = root / f'stage-{char}' / 'build' / 'web'
        if not (web / 'index.pck').is_file():
            sys.exit(f'missing build for {char}: {web}/index.pck')
        builds[char] = web

    # The claim "one shared engine" has to be true of the bytes.
    print('engine identity check:')
    for name in ENGINE_IDENTICAL:
        digests = {c: sha(builds[c] / name) for c in CHARS}
        unique = set(digests.values())
        print(f'  {name:32s} {list(unique)[0][:16]}  '
              f'{"IDENTICAL" if len(unique) == 1 else "DIVERGENT " + str(digests)}')
        if len(unique) != 1:
            sys.exit(f'engine file {name} differs across builds -- '
                     'one shared wasm is not safe; rebuild all three on one preset')

    out.mkdir(parents=True, exist_ok=True)
    for stale in out.iterdir():
        (shutil.rmtree if stale.is_dir() else pathlib.Path.unlink)(stale)

    for name in SHARED:
        src = builds[BASE] / name
        if src.is_file():
            shutil.copy2(src, out / name)

    packs = {}
    for char in CHARS:
        dest = out / f'{char}.pck'
        shutil.copy2(builds[char] / 'index.pck', dest)
        packs[char] = dest.stat().st_size

    labels = {'warlord': 'Warlord', 'keeper': 'Keeper', 'necro': 'Necromancer'}
    config = {c: {'pack': f'{c}.pck', 'size': packs[c], 'label': labels[c]} for c in CHARS}

    shell = (builds[BASE] / 'index.html').read_text()
    anchor = 'const engine = new Engine(GODOT_CONFIG);'
    if shell.count(anchor) != 1:
        sys.exit('generated shell does not carry the expected Engine construction line')
    picker = (PICKER.replace('__PACKS__', json.dumps(config))
                    .replace('__DEFAULT__', BASE))
    shell = shell.replace(anchor, picker + anchor, 1)

    if '</head>' not in shell:
        sys.exit('generated shell has no </head> to hang the chip on')
    shell = shell.replace('</head>', CHIP + '\n\t</head>', 1)

    # The generated shell still names index.pck in fileSizes; the picker
    # overwrites that object wholesale, but leave nothing that would 404.
    if re.search(r'"index\.pck"', shell.split(anchor)[1] if anchor in shell else ''):
        sys.exit('index.pck still referenced after the picker')

    (out / 'index.html').write_text(shell)

    total_shared = sum((out / n).stat().st_size for n in SHARED if (out / n).is_file())
    print('\nstaged:', out)
    print(f'  shared engine + shell   {total_shared / 1e6:8.2f} MB')
    for char in CHARS:
        print(f'  {char + ".pck":24s}{packs[char] / 1e6:8.2f} MB'
              f'   -> session total {(total_shared + packs[char]) / 1e6:.2f} MB')
    print(f'  hosted total            {(total_shared + sum(packs.values())) / 1e6:8.2f} MB')


if __name__ == '__main__':
    main()
