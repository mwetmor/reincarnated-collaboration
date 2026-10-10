#!/usr/bin/env python3
"""Build a private, offline listening sheet. Does not modify game/source audio.

Run under C-7/conductor_scripts/heavy_lock.py (ffmpeg transcodes are serial).
"""
import argparse
import base64
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOM = "sfx/tommusic/Free Fantasy SFX Pack By TomMusic/OGG Files/SFX/"
LEO = "sfx/leohpaz/"
PM = "sfx/Pixel Magic Sound Effects Pack/"
WEAPON = "sfx/MAGIC WEPONES/Weapons/"
CREATURE = "sfx/monsters_creatures_sfx_1_wav/"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pm(name):
    return PM + name + ".wav"


def leo(name):
    return LEO + name + ".wav"


def tom(name):
    return TOM + name + ".ogg"


def creature(name):
    return CREATURE + name + ".wav"


# Intent-based shortlists from source names, for Matt's ear approval.
# A shortlist is not an artistic acceptance or a claim that a loop is seamless.
def actions():
    sword = "Attacks/Sword Attacks Hits and Blocks/"
    spells = "Spells/"
    return [
        ("slash", "Character", "Sword swing / basic slash", "Also used for physical melee monster attacks. Contact has its own sound below.", [
            WEAPON + "0009_combat_sword_swing_c.wav", tom(sword + "Sword Attack 1"), leo("27_sword_miss_1"), leo("07_human_atk_sword_1")]),
        ("physical_hit", "Character", "Sword contact / physical hit", "Shared by physical hits involving the character, including incoming damage.", [
            WEAPON + "0009_combat_sword_hit_flesh_a.wav", tom(sword + "Sword Impact Hit 1"), leo("26_sword_hit_1"), "sfx/Hits/Body_HIts_01.wav"]),
        ("blitz", "Character", "Charge / Blitz", "Sound on an accepted charge cast.", [leo("08_human_charge_1"), leo("15_human_dash_1"), pm("PM_GENERIC_Flee_L2_Whoosh")]),
        ("potion", "Character", "Potion / healing", "Sound on an accepted potion use.", [leo("8_Buffs_Heals_SFX/02_Heal_02"), leo("10_UI_Menu_SFX/051_use_item_01"), pm("PM_SPELL_Buff32_Mend_v1")]),
        ("vires_might", "Character", "Might / strength buff", "Sound on activating Vires Might.", [leo("8_Buffs_Heals_SFX/16_Atk_buff_04"), leo("8_Buffs_Heals_SFX/17_Def_buff_01"), pm("PM_SPELL_Buff12_Shield")]),
        ("war_cry", "Character", "Battle Cry", "The current cue is a buff, not a voiced shout. Scream is an audition candidate, not a confirmed battle cry.", [leo("10_human_special_atk_1"), "sfx/Human_amb/Scream Male 26.wav", leo("8_Buffs_Heals_SFX/16_Atk_buff_04")]),
        ("rune_of_rush", "Character", "Haste / Rune of Rush", "Sound on activating the speed buff.", [leo("8_Buffs_Heals_SFX/48_Speed_up_02"), pm("PM_SPELL_Buff22_Quick"), pm("PM_GENERIC_Dash02")]),
        ("whirlwind_start", "Character", "Whirlwind — start", "One-shot at the start of the channel; separate from the repeating body.", [leo("10_human_special_atk_2"), pm("PM_ELEM_Wind01_Gust"), leo("8_Atk_Magic_SFX/25_Wind_01")]),
        ("whirlwind_loop", "Character", "Whirlwind — repeating body", "Use Repeat preview to hear repetition. Alternatives still need a loop-seam check before game integration.", [leo("09_human_charging_1_loop"), leo("09_human_charging_2_loop"), pm("PM_ELEM_Wind04_Cyclone")]),
        ("snow_step", "Character", "Movement / footsteps", "Current sound rotates five snow steps. Alternatives include other surfaces for comparison.", [tom("Footsteps/Dirt/Dirt Chain Walk 1"), leo("16_human_walk_stone_1"), "sfx/kenney/Audio/footstep_concrete_000.ogg"]),
        ("player_death", "Character", "Character death", "One-shot on player death. These voice candidates may need tailoring.", ["sfx/Human_amb/Scream Male 60.wav", leo("11_human_damage_1"), pm("PM_GENERIC_Death_Monster01")]),
        ("energy_refused", "Character", "Not enough energy", "Short feedback sound when a skill cannot start.", [leo("10_UI_Menu_SFX/033_Denied_03"), leo("10_UI_Menu_SFX/029_Decline_09"), "sfx/kenney/Audio/error_002.ogg"]),
        ("arrow_cast", "Monster spells", "Physical ranged attack / arrow", "Shared by monsters classified as physical ranged attackers.", [tom("Attacks/Bow Attacks Hits and Blocks/Bow Attack 2"), WEAPON + "0009_combat_bow_fire_c.wav", WEAPON + "0009_combat_crossbow_fire_b.wav"]),
        ("fire_cast", "Monster spells", "Fire — cast / projectile", "Current mapping groups fire monster casts by element.", [tom(spells + "Fireball 1"), tom(spells + "Firespray 1"), creature("Fire Elemental/0014_monster_elemental_fire_attack_a")]),
        ("fire_hit", "Monster spells", "Fire — impact", "Shared by fire hits involving the character.", [leo("8_Atk_Magic_SFX/04_Fire_explosion_04_medium"), tom(spells + "Spell Impact 1"), pm("PM_GENERIC_Explosion_Single02")]),
        ("cold_cast", "Monster spells", "Cold / ice — cast / projectile", "Current mapping groups cold monster casts by element.", [tom(spells + "Ice Throw 1"), tom(spells + "Ice Barrage 1"), tom(spells + "Ice Freeze 1")]),
        ("cold_hit", "Monster spells", "Cold / ice — impact", "Shared by cold hits involving the character.", [leo("8_Atk_Magic_SFX/13_Ice_explosion_01"), tom(spells + "Ice Freeze 2"), tom(spells + "Spell Impact 2")]),
        ("lightning_cast", "Monster spells", "Lightning — cast", "Current mapping groups lightning monster casts by element.", [leo("8_Atk_Magic_SFX/18_Thunder_02"), pm("PM_ELEM_Electric07_Lightning_Small"), pm("PM_SPELL_Cast01_Low_Wind")]),
        ("lightning_hit", "Monster spells", "Lightning — impact", "Shared by lightning hits involving the character.", [leo("8_Atk_Magic_SFX/18_Thunder_02"), pm("PM_ELEM_Electric06_Flash_Zap"), tom(spells + "Spell Impact 3")]),
        ("poison_cast", "Monster spells", "Poison — cast", "Poison has a small dedicated shortlist; other candidates are thematic approximations.", [leo("8_Atk_Magic_SFX/46_Poison_01"), pm("PM_ELEM_Dark02_Hex_P1_Trigger"), tom(spells + "Waterspray 1")]),
        ("poison_hit", "Monster spells", "Poison — impact", "Shared by poison hits involving the character. Some candidates are thematic approximations.", [pm("PM_ELEM_Dark07_Poison"), pm("PM_ELEM_Dark03_Dispel"), tom(spells + "Waterspray 2")]),
        ("aether_cast", "Monster spells", "Aether — cast", "Current light-magic substitution is provisional. No dedicated aether pack is asserted.", [pm("PM_SPELL_Cast30_Subtle_Light_Beam"), pm("PM_GENERIC_Missile_P1_Cast"), leo("8_Atk_Magic_SFX/45_Charge_05")]),
        ("aether_hit", "Monster spells", "Aether — impact", "Shared by aether hits involving the character; candidates are provisional.", [tom(spells + "Spell Impact 1"), pm("PM_GENERIC_Missile_P2_Impact"), pm("PM_ELEM_Light15_Dazzle")]),
        ("vitality_cast", "Monster spells", "Vitality / dark magic — cast", "Current mapping groups vitality monster casts by element.", [pm("PM_ELEM_Dark04_Absorb_P1_Cast"), pm("PM_ELEM_Dark02_Hex_P1_Trigger"), leo("8_Buffs_Heals_SFX/21_Debuff_01")]),
        ("vitality_hit", "Monster spells", "Vitality / dark magic — impact", "Shared by vitality hits involving the character.", [leo("8_Buffs_Heals_SFX/39_Absorb_04"), pm("PM_ELEM_Dark04_Absorb_P2_Light_Impact"), pm("PM_ELEM_Dark10_P2_Impact")]),
        ("ghost_cast", "Creature voices", "Ghost / wraith — melee attack", "Creature voice replaces the elemental cast sound for spectral melee attackers. Keep current if this is one you love.", [creature("Ghost/0014_monster_ghost_vocal_a"), creature("Ghost/0014_monster_ghost_vocal_b"), pm("PM_ELEM_Dark05_Ghost_Laughter")]),
        ("ghost_death", "Creature voices", "Ghost / wraith — death", "Also includes records named spectre or banshee.", [creature("Ghost/0014_monster_ghost_vocal_b"), pm("PM_GENERIC_Death_Monster01"), leo("10_Battle_SFX/69_Enemy_death_01")]),
        ("ghoul_death", "Creature voices", "Ghoul / zombie — death", "Keep current if this is one of the creature sounds you love.", [creature("Ghoul/0014_monster_ghoul_vocal_a"), leo("10_Battle_SFX/69_Enemy_death_01"), creature("Troll/0014_monster_troll_death")]),
        ("golem_death", "Creature voices", "Golem / construct — death", "Earth elemental voice; also used for records named construct.", [creature("Earth Elemental/0014_monster_elemental_earth_vocal_a"), creature("Giant/Enemy_Walker_Rock_LandRock"), creature("Giant/Enemy_Walker_Rock_Grunts_02")]),
        ("orc_death", "Creature voices", "Orc — death", "Keep current if this is one of the creature sounds you love.", [leo("24_orc_death_spin"), creature("Orc/0014_monster_orc_vocal_b"), leo("21_orc_damage_1")]),
        ("enemy_death", "Creature voices", "Other monsters — death", "Fallback for records outside the four named voice families. Note the creature if you want a more specific sound.", [creature("Goblin/0014_monster_goblin_death"), creature("Demon/Muerte_001"), pm("PM_GENERIC_Death_Monster02")]),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/Users/admin/Games/reincarnated-demo/public/audio"))
    args = parser.parse_args()
    inventory = json.loads((ROOT / "audio_review/AUDIO_INVENTORY.json").read_text())
    indexed = {row["path"]: row for row in inventory["files"]}
    manifest_bytes = (ROOT / "godot/data/audio/arena_audio.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    rows, wanted = [], set()
    for key, group, label, note, alternatives in actions():
        current = [manifest["clips"][clip]["source"] for clip in manifest["cues"][key]]
        alternatives = list(dict.fromkeys(path for path in alternatives if path not in current))
        options = [{"id": "current", "label": "Keep current" + (" rotation" if len(current) > 1 else " sound"), "sources": current}]
        options += [{"id": path, "label": Path(path).stem, "sources": [path]} for path in alternatives]
        rows.append({"key": key, "group": group, "label": label, "note": note, "options": options})
        wanted.update(current + alternatives)
    assert {row["key"] for row in rows} == set(manifest["cues"]), "Review must cover every live cue"
    # Validate every input before creating any preview. Originals are read-only.
    for path in wanted:
        assert path in indexed, f"Not inventoried: {path}"
        assert digest((args.source / path).read_bytes()) == indexed[path]["sha256"], f"Source changed: {path}"
    for key, clip in manifest["clips"].items():
        if clip["source"] in wanted:
            assert clip["sha256"] == indexed[clip["source"]]["sha256"], f"Live/inventory mismatch: {key}"
    catalogue = {
        "schema": "barrow_sfx_review_v1", "manifest_sha256": digest(manifest_bytes),
        "source_root": str(args.source), "music": "accepted_for_now",
        "feedback": {"character": "needs_review", "monster_casts": "mostly_rejected_pending_audition", "creature_voices": "some_loved_pending_identification"},
        "preview": "Full duration MP3, stereo 48 kHz, 160 kbps; no trimming, gain adjustment, or normalization. Browser volume defaults to 50%. Game mix differs.",
        "actions": rows,
        "clips": {path: {k: indexed[path][k] for k in ("group", "seconds", "sha256")} for path in sorted(wanted)},
    }
    canonical = json.dumps(catalogue, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    catalogue["catalog_sha256"] = digest(canonical)
    out = ROOT / "audio_review"
    (out / "SFX_REVIEW_CATALOG.json").write_text(json.dumps(catalogue, indent=2) + "\n")
    cache = out / "previews/sfx"
    cache.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    assert ffmpeg, "ffmpeg is required; no dependencies are installed by this tool"
    media = {}
    for path in sorted(wanted):
        clip = catalogue["clips"][path]
        target = cache / (clip["sha256"] + ".stereo48-160.mp3")
        if not target.exists():
            temporary = target.with_suffix(".pending.mp3")
            subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(args.source / path),
                            "-map_metadata", "-1", "-vn", "-ar", "48000", "-ac", "2", "-codec:a", "libmp3lame", "-b:a", "160k", str(temporary)], check=True)
            temporary.replace(target)
        media[path] = "data:audio/mpeg;base64," + base64.b64encode(target.read_bytes()).decode()
    payload = {**catalogue, "media": media}
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = (ROOT / "tools/arena_sfx_review.html").read_text()
    assert template.count("__REVIEW_DATA__") == 1
    html = template.replace("__REVIEW_DATA__", encoded)
    output = out / "SFX_REVIEW.html"
    output.write_text(html)
    print(json.dumps({"html": str(output), "bytes": output.stat().st_size, "actions": len(rows), "unique_sfx": len(wanted), "catalog_sha256": catalogue["catalog_sha256"]}))


if __name__ == "__main__":
    main()
