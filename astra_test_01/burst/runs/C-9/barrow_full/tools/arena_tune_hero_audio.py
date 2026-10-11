#!/usr/bin/env python3
"""Replace rejected hero cues using Matt's handoff notes; preserve approved cues.

Run under the shared heavy lock. Demo inputs stay read-only; recipes and hashes
are recorded. These are implemented listening revisions, not inferred approvals.
"""
import array
import base64
import hashlib
import html
import io
import json
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = Path('/Users/admin/Games/reincarnated-demo/public/audio')
RATE = 48000
SELECTED = ROOT / 'audio_review/selected_sfx'
WAR_CRY_SHA = 'adf412b8e02d28f01a1d02a5013946af4b08a154db9612933781f09b7148de3e'
RECIPES = {
    'blitz': ('Heavy weapon-air charge', [
        ('sfx/MAGIC WEPONES/Weapons/0009_combat_sword_swing_c.wav',
         'asetrate=36000,aresample=48000,lowpass=f=3200,highpass=f=65', 0.0, 0.85),
        ('sfx/Hits/Metal_Hit_05.wav',
         'asetrate=31200,aresample=48000,lowpass=f=1800,highpass=f=65', 0.16, 0.22)], 0.85),
    'potion': ('Bottle opening / handling', [
        ('sfx/oga/RPG Sound Pack/inventory/bottle.wav',
         'highpass=f=80,lowpass=f=8500', 0.0, 1.0)], 0.75),
    'vires_might': ('Might — Fortify (new candidate)', [
        ('sfx/Pixel Magic Sound Effects Pack/PM_SPELL_Buff28_Fortify.wav',
         'highpass=f=60,lowpass=f=5000', 0.0, 1.0)], 0.80),

}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(path, filters):
    chain = 'aresample=48000,' + filters + ',silenceremove=start_periods=1:start_duration=0.005:start_threshold=-55dB'
    result = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-i', str(path),
        '-af', chain, '-ac', '1', '-f', 'f32le', 'pipe:1'], capture_output=True, check=True)
    values = array.array('f', result.stdout)
    if sys.byteorder != 'little':
        values.byteswap()
    return list(values), chain


def encode(samples, peak):
    gain = peak / (max(abs(v) for v in samples) or 1)
    # Short edge ramps avoid clicks without changing the cue's timing.
    ramp = min(round(RATE * 0.005), len(samples) // 2)
    for i in range(ramp):
        samples[i] *= i / ramp
        samples[-i - 1] *= i / ramp
    pcm = array.array('h', [round(max(-1, min(1, v * gain)) * 32767) for v in samples])
    if sys.byteorder != 'little':
        pcm.byteswap()
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(pcm.tobytes())
    return buffer.getvalue()


def main():
    path = ROOT / 'godot/data/audio/arena_audio.json'
    manifest = json.loads(path.read_text())
    before = json.loads(path.read_text())
    baseline = json.loads((ROOT / 'audio_review/ARENA_AUDIO_REVIEW_BASELINE.json').read_text())
    inventory = {row['path']: row for row in json.loads((ROOT / 'audio_review/AUDIO_INVENTORY.json').read_text())['files']}
    war_data = (SELECTED / 'war_cry_elevenlabs.mp3').read_bytes()
    if sha(war_data) != WAR_CRY_SHA:
        raise ValueError('Your selected War Cry differs from its receipt')
    for _, layers, _ in RECIPES.values():
        for source, _, _, _ in layers:
            if sha((DEMO / source).read_bytes()) != inventory[source]['sha256']:
                raise ValueError('Changed hero audio input: ' + source)
    output = ROOT / 'audio_review/derived_sfx'
    output.mkdir(parents=True, exist_ok=True)
    receipt = {'request': "Use Matt's ElevenLabs War Cry unchanged; replace rejected Might Star Power with Fortify",
               'status': 'implemented_for_listening; artistic approval pending', 'cues': {}}
    sections = []
    for cue, (label, layers, peak) in RECIPES.items():
        decoded, sources = [], []
        for source, filters, offset, gain in layers:
            samples, chain = decode(DEMO / source, filters)
            normalized = max(abs(v) for v in samples) or 1
            decoded.append((samples, round(offset * RATE), gain / normalized))
            sources.append({'path': source, 'sha256': inventory[source]['sha256'],
                            'ffmpeg_filter': chain, 'offset_seconds': offset, 'layer_gain': gain})
        samples = [0.0] * max(len(s) + offset for s, offset, _ in decoded)
        for values, offset, gain in decoded:
            for i, value in enumerate(values):
                samples[i + offset] += value * gain
        data = encode(samples, peak)
        key = 'hero_' + cue + '_revision'
        filename = key + '.wav'
        (output / filename).write_bytes(data)
        clip = {'source': filename, 'source_root': 'derived_sfx', 'file': filename + '.bin',
                'format': 'wav', 'bytes': len(data), 'sha256': sha(data), 'seconds': len(samples) / RATE}
        manifest['clips'][key] = clip
        manifest['cues'][cue] = [key]
        receipt['cues'][cue] = {'label': label, 'sources': sources, 'peak_target': peak, 'output': clip}
        old_id = baseline['cues'][cue][0]
        old_source = baseline['clips'][old_id]['source']
        old_samples, _ = decode(DEMO / old_source, 'anull')
        old_audio = encode(old_samples, min(0.99, max(abs(v) for v in old_samples)))
        def player(payload):
            return '<audio controls preload="none" src="data:audio/wav;base64,' + base64.b64encode(payload).decode() + '"></audio>'
        sections.append('<section><h2>' + html.escape(label) + '</h2><p>Implemented in the local scene</p>' + player(data)
                        + '<details><summary>Previous rejected cue</summary>' + player(old_audio) + '</details></section>')
    war_key = 'hero_war_cry_elevenlabs'
    war_clip = {'source': 'war_cry_elevenlabs.mp3', 'source_root': 'selected_sfx',
                'file': 'war_cry_elevenlabs.mp3.bin', 'format': 'mp3',
                'bytes': len(war_data), 'sha256': WAR_CRY_SHA, 'seconds': 2.48}
    manifest['clips'][war_key] = war_clip
    manifest['cues']['war_cry'] = [war_key]
    manifest.setdefault('source_roots', {})['selected_sfx'] = str(SELECTED)
    receipt['cues']['war_cry'] = {'label': 'War Cry — your ElevenLabs selection',
        'status': 'user_selected', 'processing': 'none; original MP3 bytes and pitch preserved', 'output': war_clip}
    sections.append('<section><h2>War Cry — your ElevenLabs selection</h2><p>Original voice and pitch, installed in game.</p><audio controls preload="none" src="data:audio/mpeg;base64,' + base64.b64encode(war_data).decode() + '"></audio></section>')
    # No changes to Haste, Whirlwind, physical hits, approved monster cues or mix.
    for cue in set(before['cues']) - set(RECIPES) - {'war_cry'}:
        assert manifest['cues'][cue] == before['cues'][cue]
    assert manifest['mix'] == before['mix']
    needed = {c for ids in manifest['cues'].values() for c in ids} | {t['clip'] for t in manifest['music']} | {manifest['ambience']['clip']}
    manifest['clips'] = {k: v for k, v in manifest['clips'].items() if k in needed}
    manifest.setdefault('source_roots', {})['derived_sfx'] = str(output)
    manifest['hero_revision'] = 'HERO_SFX_REVISION.json'
    manifest['notes'][0] = 'Approved handoff plus later Whirlwind and hero SFX revisions; only poison find-more cues retain baseline.'
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    receipt['manifest_sha256'] = sha(path.read_bytes())
    (ROOT / 'audio_review/HERO_SFX_REVISION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    subprocess.run(['python3', str(ROOT / 'tools/arena_stage_audio.py')], check=True)
    for cue, label in [('whirlwind_loop', 'Whirlwind — rotating pendulum sweeps'), ('rune_of_rush', 'Haste — your selected Dash02')]:
        clip = manifest['clips'][manifest['cues'][cue][0]]
        data = (ROOT / 'godot/data/audio' / clip['file']).read_bytes()
        sections.append('<section><h2>' + html.escape(label) + '</h2><p>Current local cue</p>' + player(data) + '</section>')
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hero SFX revisions</title><style>body{background:#131a21;color:#eef1f6;font:17px system-ui;max-width:740px;margin:32px auto;padding:16px}section{background:#23303d;padding:18px;margin:18px 0;border-radius:10px}audio{width:100%}summary{cursor:pointer;padding:12px 0}h2{font-size:21px}</style><h1>Hero SFX revisions</h1><p>These four sounds are now in the local playable scene. Haste uses your selected Dash02; Whirlwind keeps the deep rotating pendulum sweeps. War Cry uses your supplied ElevenLabs MP3 without pitch or timing changes. Might now uses Fortify instead of Star Power; this new candidate still needs your listening verdict.</p>' + ''.join(sections) + '<script>document.addEventListener("play",e=>{if(e.target.tagName==="AUDIO")document.querySelectorAll("audio").forEach(a=>{if(a!==e.target)a.pause()})},true)</script></html>'
    (output / 'HERO_SFX_REVIEW.html').write_text(page)
    print('HERO_SFX: PASS; 4 changed cues; approved Haste/Whirlwind/monster cues preserved')


if __name__ == '__main__':
    main()
