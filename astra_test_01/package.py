"""Package rejected checkpoint evidence; never manufacture missing animations."""
from pathlib import Path
import json
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent
DIRS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']


def main():
    evidence = ROOT / 'evidence' / 'turnaround_1'
    character = ROOT / 'character'
    for folder in ['sheets', 'contact', 'frames/idle']:
        (character / folder).mkdir(parents=True, exist_ok=True)
    for name in ['turnaround.png', 'turnaround_64px.png']:
        shutil.copyfile(evidence / name, character / name)
    sheet = Image.new('RGBA', (512, 4096))
    frame_rects = {}
    for row, direction in enumerate(DIRS):
        name = f'idle_{direction}_00.png'
        src = evidence / 'frames' / direction / name
        dest = character / 'frames' / 'idle' / direction / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        sheet.paste(Image.open(src), (0, row * 512))
        frame_rects[direction] = [{'index': 0, 'rect': [0, row * 512, 512, 512],
                                 'file': f'frames/idle/{direction}/{name}'}]
    sheet.save(character / 'sheets' / 'idle.png')
    sheet.resize((128, 1024), Image.Resampling.LANCZOS).save(character / 'contact' / 'idle.png')
    atlas = {
        'status': 'REJECTED_CHECKPOINT', 'production_ready': False,
        'selection': 'First attempt retained; failed SW repair is evidence only.',
        'direction_order': DIRS, 'required_frames': 224, 'available_frames': 8,
        'animations': {'idle': {
            'status': 'INCOMPLETE_REJECTED', 'sheet': 'sheets/idle.png',
            'canvas_size': [512, 512], 'pivot': [256, 400],
            'pivot_is_requirement_not_verified': True,
            'fps': 8, 'loop': True, 'available_frames_per_direction': 1,
            'required_frames_per_direction': 8, 'frames': frame_rects}},
        'not_generated': {
            'walk': {'frames_per_direction': 8, 'fps': 10, 'loop': True},
            'cast': {'frames_per_direction': 12, 'fps': 16, 'loop': False, 'spawn_frame_index': 5},
            'sprint': {'optional': True, 'frames_per_direction': 8, 'fps': 14, 'loop': True}},
    }
    (character / 'atlas.json').write_text(json.dumps(atlas, indent=2) + '\n')
    (ROOT / 'vfx').mkdir(exist_ok=True)
    (ROOT / 'vfx' / 'atlas.json').write_text(json.dumps({
        'status': 'NOT_TESTED_CHECKPOINT_STOP', 'available_frames': 0, 'required_frames': 24,
        'modules': {}, 'planned': {
            'cast': {'frame_count': 8, 'canvas_size': [256, 256], 'fps': 20, 'loop': False},
            'travel': {'frame_count': 6, 'canvas_size': [256, 128], 'fps': 20, 'loop': True},
            'impact': {'frame_count': 10, 'canvas_size': [384, 384], 'fps': 20, 'loop': False}}}, indent=2) + '\n')
    print('Packaged 8 rejected checkpoint frames; 0 animation sequences; 0 VFX frames.')


if __name__ == '__main__':
    main()
