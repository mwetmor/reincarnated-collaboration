# C-9 barrow_v2 arena: review of Astra's (Codex) completion work, 2026-10-10..11

> **STATUS:** CURRENT (verdict-class note). **Author:** gandalf (C-9 RUN-CONDUCTOR, DRIFT-CRITIC). **Date:** 2026-10-13.
> **Scope:** the 18 collaboration commits after `e2b234846` (`c6ac9b55f` … `56a5024bc`) and the loadout commits `644bf8a` … `d29465e`. Codex worked under Matt's direct authority while Claude's usage limit was hit. Its commits are authored as Matt without an agent prefix, so this note is their lineage record.

## Verdict: ACCEPTED, with one WARN for Matt's ratification and two items left open

### What Astra delivered
- **Audio:**
  - arena SFX picked by Matt through an offline and Wi-Fi review tool (`audio_review/`, `tools/arena_sfx_review*`);
  - Matt's own score, with the fjord-storm layer;
  - hero skill cues, using the ElevenLabs War Cry and Might sounds Matt selected;
  - the Whirlwind contact-hit mix lowered under the pendulum sweep. This is an **audio** balance only; no damage changed.
- **Web parity repairs** (`tools/WEB_ARENA_BUGS.md`, WEB-01..10):
  - terrain fields restored, and the walk map matches native (29,264 vs 29,200 reachable cells);
  - all 42 kits;
  - hero colour correction;
  - streamed WebAudio, verified by destination PCM;
  - shader and animation warm-up before play;
  - concurrent pack loads;
  - bakes at half native size, lossless.
- **Public route:** https://reincarnated-loadout.vercel.app/playtest/barrow-arena/ (WEB-05 resolved; no login).
- **A Windows x64 native package**, `pc_arena/build/BarrowArena-Windows-x64.zip`, built at Matt's request after the earlier "skip PC" ruling (R-C9-391). It is local only; I found no hosting record.

### Checks that PASS
- **Sealed runtime untouched:** reincarnated-godot has no commits since 2026-10-10 and a clean `kc2_runtime/`. The bundle still pins runtime tree `a0e75469…` and model pack `997117…`, both byte-verified at launch (`tools/WEB_ARENA_NOTES.md`).
- **Ledger untouched:** `ledger.json` changes since `e2b234846` are conductor rows only.
- **Licensing recorded** (`audio_review/AUDIO_CREDITS.txt`):
  - the purchased WSP pack;
  - CC0 Kenney, OGA and kmontesdev sounds;
  - Matt's own Suno tracks;
  - the ElevenLabs picks Matt chose.
  No franchise names were found in the shipped strings.

### WARN-1, needs Matt's explicit ratification: the platform-solver reroute
`godot/scripts/arena/arena_session.gd` `open()` (commit `c6ac9b55f`) handles the case where the sealed runtime refuses to start because there is no native contact library for the platform (`PLAY-CONTACT-SOLVER: ORACLE: no native contact library is built for <platform>`). On web and Windows x64 it then:
1. switches to the runtime's own GDScript reference solver through its public `select_contact_solver("gdscript")`;
2. clears `fight.last_error` and `load_error`;
3. calls `_bind_summons()` and `play_open()` itself.

No sealed byte changes, and the code's own note says *"no … oracle refusal rule is changed"*. It is still an arena-side reroute around a refusal the sealed runtime raises, which is exactly what R-C9-394 told drax to stop and report on. The GDScript solver is the runtime's exact reference, so fight outcomes should match native. **Owed:** Matt's explicit OK, plus one same-seed probe showing native vs GDScript decisions identical over a few waves.

### Open items
- **R-C9-396, whirlwind smoke missing.** Deferred by Matt and not addressed by Astra's work. Still to root-cause; suspect the R-C9-392 mace-emission change.
- **Download size.** The higher-detail export is about 650 MB before compression (WEB-08). On phones the load time and memory are the real limits. WEB-06 has no confirmed device report yet.
