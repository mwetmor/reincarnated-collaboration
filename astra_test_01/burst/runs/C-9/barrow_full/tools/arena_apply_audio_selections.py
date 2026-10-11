#!/usr/bin/env python3
"""Apply the approved listening handoff; keep find-more/pending cues unchanged.

Run under the shared heavy lock: staging can convert WAV headers for Godot.
"""
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = Path('/Users/admin/Games/reincarnated-demo/public/audio')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'pc_arena/build/SFX_and_Sound_Selections')
    args = parser.parse_args()
    source_selection = args.input / 'barrow-sfx-selections.json'
    selections = json.loads(source_selection.read_text())
    catalogue = json.loads((ROOT / 'audio_review/SFX_REVIEW_CATALOG.json').read_text())
    if selections.get('catalog_sha256') != catalogue['catalog_sha256'] or selections.get('manifest_sha256') != catalogue['manifest_sha256']:
        raise ValueError('Handoff does not match the reviewed baseline')
    manifest_path = ROOT / 'godot/data/audio/arena_audio.json'
    baseline_path = ROOT / 'audio_review/ARENA_AUDIO_REVIEW_BASELINE.json'
    if not baseline_path.exists():
        if sha(manifest_path) != catalogue['manifest_sha256']:
            raise ValueError('Live manifest changed before baseline was archived')
        shutil.copy2(manifest_path, baseline_path)
    if sha(baseline_path) != catalogue['manifest_sha256']:
        raise ValueError('Review baseline changed')
    baseline = json.loads(baseline_path.read_text())
    manifest = copy.deepcopy(baseline)
    inventory = {row['path']: row for row in json.loads((ROOT / 'audio_review/AUDIO_INVENTORY.json').read_text())['files']}
    actions = {a['key']: a for a in catalogue['actions']}
    if set(selections['choices']) - set(actions):
        raise ValueError('Unknown handoff cue')
    receipt = {'selection_sha256': sha(source_selection), 'baseline_sha256': sha(baseline_path), 'applied': [], 'kept': [], 'deferred': [], 'pending': []}
    next_id = max(int(key.split('_')[1]) for key in manifest['clips']) + 1

    def add(path, root=DEMO, source_root=None):
        nonlocal next_id
        for key, clip in manifest['clips'].items():
            if clip['source'] == path and clip.get('source_root') == source_root:
                return key
        source = root / path
        metadata = inventory.get(path)
        if metadata is None:
            info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'format=duration:stream=channels', '-of', 'json', str(source)]))
            metadata = {'seconds': float(info['format']['duration']), 'channels': info['streams'][0]['channels'], 'sha256': sha(source)}
        if sha(source) != metadata['sha256']:
            raise ValueError('Changed source: ' + str(source))
        key = 'clip_%03d' % next_id
        next_id += 1
        format_name = source.suffix[1:].lower()
        clip = {'source': path, 'file': key + '.' + format_name + '.bin', 'format': format_name,
                'bytes': source.stat().st_size, 'sha256': metadata['sha256'], 'seconds': metadata['seconds']}
        if source_root:
            clip['source_root'] = source_root
        if format_name == 'wav':
            # These purchased/source WAVs may use a WAVE header Godot cannot read.
            # Preserve the originals; derive plain PCM16 for engine playback.
            clip['source_sha256'] = metadata['sha256']
            clip['conversion'] = {'codec': 'pcm_s16le', 'sample_rate': 48000, 'channels': metadata['channels']}
        manifest['clips'][key] = clip
        return key

    for key, action in actions.items():
        row = selections['choices'].get(key, {'choice': 'pending', 'notes': ''})
        choice = row['choice']
        note = row.get('notes', '')
        if choice in ('find_more', 'pending', 'current'):
            receipt[{'find_more': 'deferred', 'pending': 'pending', 'current': 'kept'}[choice]].append({'cue': key, 'label': action['label'], 'notes': note})
            continue
        if choice == 'mute':
            manifest['cues'][key] = []
        else:
            if choice not in [o['id'] for o in action['options']]:
                raise ValueError('Unreviewed choice: ' + choice)
            paths = [choice]
            if key == 'ghost_cast' and 'alternate' in note.lower():
                paths.append('sfx/monsters_creatures_sfx_1_wav/Ghost/0014_monster_ghost_vocal_b.wav')
            if key == 'enemy_death' and 'assortment' in note.lower():
                paths.extend('sfx/monsters_creatures_sfx_1_wav/' + name for name in [
                    'Demon/Muerte_001.wav', 'Troll/0014_monster_troll_death.wav',
                    'Minotaur/0014_monster_minotaur_death.wav', 'Fire Elemental/0014_monster_elemental_fire_death.wav'])
            manifest['cues'][key] = [add(path) for path in paths]
        receipt['applied'].append({'cue': key, 'notes': note, 'clips': manifest['cues'][key]})

    # Keep user uploads outside a disposable native-build folder.
    soundtrack_root = ROOT / 'audio_review/soundtracks'
    soundtrack_root.mkdir(parents=True, exist_ok=True)
    for name in ['Northern Omen.mp3', 'Fjordstormen.mp3']:
        source = args.input / name
        target = soundtrack_root / name
        if not target.exists() or sha(target) != sha(source):
            shutil.copy2(source, target)
    manifest['source_roots'] = {'soundtracks': str(soundtrack_root)}
    score = add('Northern Omen.mp3', soundtrack_root, 'soundtracks')
    nature = add('Fjordstormen.mp3', soundtrack_root, 'soundtracks')
    manifest['music'].insert(0, {'clip': score, 'title': 'Northern Omen'})
    manifest['default_music'] = 0
    manifest['ambience'] = {'clip': nature, 'title': 'Fjordstormen', 'crossfade_seconds': 1.5}
    manifest['mix'] = {'music_db': -22.0, 'music_combat_db': -28.0, 'ambience_db': -28.0, 'ambience_combat_db': -32.0}
    needed = {clip for ids in manifest['cues'].values() for clip in ids} | {t['clip'] for t in manifest['music']} | {nature}
    manifest['clips'] = {key: value for key, value in manifest['clips'].items() if key in needed}
    manifest['selection_sha256'] = receipt['selection_sha256']
    manifest['notes'] = ['Approved handoff applied; find-more and pending cues retain their reviewed baseline until new approval.',
                         'New WAV selections use derived PCM16; original hashes and conversion recipes are pinned.',
                         'Northern Omen is the default score; Fjordstormen is a separate quieter looping environment layer.']
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    shutil.copy2(source_selection, ROOT / 'audio_review/APPROVED_SFX_SELECTIONS.json')
    subprocess.run(['python3', str(ROOT / 'tools/arena_stage_audio.py'), '--update-derived-hashes'], check=True)
    receipt['manifest_sha256'] = sha(manifest_path)
    receipt['soundtracks'] = {name: sha(soundtrack_root / name) for name in ['Northern Omen.mp3', 'Fjordstormen.mp3']}
    (ROOT / 'audio_review/SELECTION_APPLICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: len(receipt[key]) for key in ['applied', 'kept', 'deferred', 'pending']}))


if __name__ == '__main__':
    main()
