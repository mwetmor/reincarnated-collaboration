#!/usr/bin/env python3
"""Small local audition excerpts; original tracks are never modified."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
inventory = json.loads((root / 'audio_review/AUDIO_INVENTORY.json').read_text())
destination = root / 'audio_review/previews'
destination.mkdir(parents=True, exist_ok=True)
for track in inventory['music']:
    source = Path(inventory['source']) / track['path']
    target = destination / source.name
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', '45',
                    '-i', str(source), '-t', '20', '-af',
                    'afade=t=in:st=0:d=0.25,afade=t=out:st=19:d=1',
                    '-ar', '44100', '-ac', '2', '-b:a', '64k', '-map_metadata', '-1',
                    str(target)], check=True)
print('AUDIO_PREVIEWS: five 20-second excerpts at 0:45; 64 kbps MP3 for local audition')
