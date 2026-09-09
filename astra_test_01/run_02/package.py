"""Package only the eight existing, rejected idle-00 frames; never pad counts."""
import json
import shutil
from pathlib import Path
from PIL import Image
from pipeline import ROOT, CONFIG, save_json


def package():
    evidence = ROOT / 'evidence/checkpoint_2'
    character = ROOT / 'character'
    character.mkdir(exist_ok=True)
    for name in ['turnaround.png', 'turnaround_64px.png']:
        shutil.copyfile(evidence / name, character / name)
    sheet = Image.new('RGBA', (512, 4096))
    entries = []
    for row, direction in enumerate(CONFIG['directions']):
        relative = f'frames/idle/{direction}/idle_{direction}_00.png'
        dest = character / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(evidence / direction / 'frame.png', dest)
        sheet.paste(Image.open(dest), (0, row * 512))
        entries.append({'direction': direction, 'index': 0, 'file': relative,
                        'rect': [0, row * 512, 512, 512]})
    (character / 'sheets').mkdir(exist_ok=True)
    (character / 'contact').mkdir(exist_ok=True)
    sheet.save(character / 'sheets/idle.png')
    sheet.resize((128, 1024), Image.Resampling.LANCZOS).save(character / 'contact/idle.png')
    save_json(character / 'atlas.json', {
        'status': 'REJECTED_CHECKPOINT', 'production_ready': False,
        'directions': CONFIG['directions'], 'canvas': [512, 512], 'pivot': [256, 400],
        'required_character_frames': 224, 'available_character_frames': 8,
        'animations': {'idle': {'sheet': 'sheets/idle.png', 'fps': 8,
            'required_frames_per_direction': 8, 'available_frames_per_direction': 1,
            'loop': False, 'intended_loop': True, 'frames': entries}},
        'missing_animations': ['walk', 'cast'], 'cast_spawn_index': 5})
    save_json(ROOT / 'vfx/atlas.json', {'status': 'NOT_GENERATED', 'modules': {},
        'required_counts': {'cast': 8, 'travel': 6, 'impact': 10},
        'reason': 'Generation stopped at the brief\'s two-failed-turnaround rule.'})
    # Embed measurements so the dependency-free viewer also works with file://.
    html = (ROOT / 'preview_template.html').read_text()
    measurements = {str(n): json.loads((ROOT / f'evidence/checkpoint_{n}/checks.json').read_text()) for n in (1, 2)}
    html = html.replace('__CHECKPOINT_DATA__', json.dumps(measurements))
    (ROOT / 'preview').mkdir(exist_ok=True)
    (ROOT / 'preview/index.html').write_text(html)


if __name__ == '__main__':
    package()
