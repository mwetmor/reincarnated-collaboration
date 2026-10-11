#!/usr/bin/env python3
"""Reproduce Matt's slower metal Whirlwind and louder Fjordstormen tuning.

Original demo files stay read-only. Run under the shared heavy lock.
"""
import array
import hashlib
import io
import json
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('/Users/admin/Games/reincarnated-demo/public/audio')
RATE = 48000
SOURCES = {
    'swing': ('sfx/MAGIC WEPONES/Weapons/0009_combat_sword_swing_c.wav', '3dbfe4d5bf99581186672b0889c32ad98689c40a6635c90f90fc0680fbc53670'),
    'metal': ('sfx/Hits/Metal_Hit_05.wav', '38e5de64d70465371c88c83bba8d8f9980ab06cdbfe3eef56c11bbbd31818ace'),
    'clang': ('sfx/Hits/Metal_Hit_08.wav', '2b44915672f6c05bc45a398c8b2b35ce2ef7252822ab1941c1efcb48a0d08c32'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest_path = ROOT / 'godot/data/audio/arena_audio.json'
    manifest = json.loads(manifest_path.read_text())
    # Validate every input before processing.
    for path, digest in SOURCES.values():
        if sha((SOURCE / path).read_bytes()) != digest:
            raise ValueError('Whirlwind source changed: ' + path)
    sounds = {}
    for name, (path, _) in SOURCES.items():
        # 0.70 speed/pitch = about six semitones lower; soften bright metallic hiss.
        result = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-i', str(SOURCE / path),
            '-af', 'aresample=48000,asetrate=33600,aresample=48000,lowpass=f=4200,highpass=f=55',
            '-ac', '1', '-f', 'f32le', 'pipe:1'], check=True, capture_output=True)
        samples = array.array('f', result.stdout)
        if sys.byteorder != 'little':
            samples.byteswap()
        peak = max(abs(v) for v in samples) or 1
        sounds[name] = [v / peak for v in samples]
    duration = 4.8
    count = round(RATE * duration)
    loop = [0.0] * count
    start = [0.0] * round(RATE * 2.5)
    def layer(target, name, offset, gain, wrap=False):
        for i, v in enumerate(sounds[name]):
            at = i + round(offset * RATE)
            if wrap:
                at %= len(target)  # ring tails across the loop boundary, without a hard cut
            if at < len(target):
                target[at] += v * gain
    for beat in range(6):
        layer(loop, 'swing', beat * 0.8, 0.30, True)
        layer(loop, 'metal' if beat % 2 == 0 else 'clang', beat * 0.8 + 0.20, 0.75, True)
    layer(start, 'swing', 0, 0.30)
    layer(start, 'metal', 0.20, 0.75)
    output = ROOT / 'audio_review/derived_sfx'
    output.mkdir(parents=True, exist_ok=True)
    receipt = {'request': 'Slower, deeper strike/clanging Whirlwind; Fjordstormen +8 dB',
        'sources': {name: {'path': path, 'sha256': digest} for name, (path, digest) in SOURCES.items()},
        'speed_and_pitch': 0.70, 'strike_spacing_seconds': 0.8, 'loop_seconds': duration, 'outputs': {}}
    for key, cue, samples in [('whirlwind_metal_start', 'whirlwind_start', start), ('whirlwind_metal_loop', 'whirlwind_loop', loop)]:
        gain = 0.85 / (max(abs(v) for v in samples) or 1)
        pcm = array.array('h', [round(max(-1, min(1, v * gain)) * 32767) for v in samples])
        if sys.byteorder != 'little':
            pcm.byteswap()
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(RATE); wav.writeframes(pcm.tobytes())
        data = buffer.getvalue()
        (output / (key + '.wav')).write_bytes(data)
        manifest['clips'][key] = {'source': key + '.wav', 'source_root': 'derived_sfx', 'file': key + '.wav.bin',
            'format': 'wav', 'bytes': len(data), 'sha256': sha(data), 'seconds': len(samples) / RATE}
        manifest['cues'][cue] = [key]
        receipt['outputs'][key] = manifest['clips'][key]
    manifest['source_roots']['derived_sfx'] = str(output)
    manifest['mix']['ambience_db'] = -20.0
    manifest['mix']['ambience_combat_db'] = -24.0
    used = {c for ids in manifest['cues'].values() for c in ids} | {m['clip'] for m in manifest['music']} | {manifest['ambience']['clip']}
    manifest['clips'] = {k: v for k, v in manifest['clips'].items() if k in used}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    receipt['manifest_sha256'] = sha(manifest_path.read_bytes())
    (ROOT / 'audio_review/WHIRLWIND_TUNING.json').write_text(json.dumps(receipt, indent=2) + '\n')
    subprocess.run(['python3', str(ROOT / 'tools/arena_stage_audio.py')], check=True)
    print('AUDIO_TUNING: PASS; six low metal strikes / 4.8 seconds; environment +8 dB')


if __name__ == '__main__':
    main()
