# Native Windows arena package — 2026-10-10

Matt requested an offline PC package of the existing `godot/scenes/bv2f_arena.tscn`, preserving its native presentation, before returning to the web/mobile bugs recorded in `WEB_ARENA_BUGS.md`.

Build from this directory: `tools/build_pc_arena.sh`. Requires the existing Godot 4.6.3 stable app and its installed Windows x64 export template. The script uses the conductor heavy lock and the existing native 20 GiB initial disk gate. Generated mirror, logs, binaries and ZIP live under ignored `pc_arena/`; they are not committed.

The mirror changes only the application name/main scene. Forward+, native materials/lighting, full site painting, 3D geometry/hero, snow/water, walk collisions and original texture import settings remain the native source's. `arena_bundle_native.py` vendors the pinned runtime/model and the full original catalogue plus native variants. Strip files gain `.bin` and the corresponding index filenames change; image bytes, cell dimensions, anchors and scale are preserved. Enemy VFX also retain their original bytes. No web rescaling, WebP encoding, texture limits or shader switches run.

Windows portability stays in the presentation/export layer:

- The sealed runtime/model remain byte-identical to pins `a0e75469a78b3b81d979d9d525e0bbf1c5324459260c62110192878c33a53f1c` / `997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788`.
- `arena_session.gd` resumes only the exact unsupported-platform native-solver stop for Web or Windows x64. It explicitly selects the runtime's existing exact GDScript contact solver through its public API, then completes the parent's summon binding and play-open sequence. Windows has no compiled solver in the sealed pin; this can reduce performance. Mac native selection is unchanged. No cross-platform oracle parity or seal acceptance is claimed.
- `pck_web_extensions.py` suppresses only the generated `.godot/extension_list.cfg` startup entry in the portable PCK. The sealed Mac extension config/library bytes remain in the payload for runtime verification.
- `pck_native_alias.py` adds a read-only PCK directory alias from the loader's legacy absolute leech-table path to the existing pinned bundled payload. Godot 4.6 `FileAccess::open/exists` consult PackedData first, including absolute paths, and PackedData indexes these by their simplified path. This avoids OS path creation or privileged launcher requirements; no runtime byte changes. The absent-host-file probe proves the packed lookup, and corrupt table bytes are rejected before adding an alias.

Verification requires actual packed files. `arena_native_package.py` parses the PCK directory, verifies every runtime/model member, all kit/VFX bytes, bundle inputs and native raw data, and checks the executable's PE x64 header. `arena_native_probe.gd` launches from an empty project with only the Windows PCK. On Mac, it loads the unchanged pinned Mac extension solely to execute this probe, then uses the public reference solver switch for the Windows algorithm path. It checks native painting, live 3D hero, enemy VFX, geometry/collision counts, reachable walk cells, decoding one original strip per kit, advancing combat ticks and physical movement. `arena_native_zip.py` verifies the audited files and ZIP CRCs and writes a SHA256 sidecar.

This validates packed dependency completeness and the native scene on Mac. A Mac executing the Windows PCK is not a Windows executable launch test. Actual Windows GPU appearance, runtime startup, permissions and performance remain PC playtest criteria. The physical-phone web failure also remains unverified; desktop touch emulation was never physical-device acceptance.

Godot notices in the package are fetched from the official `4.6.3-stable` tag: `LICENSE.txt` and `COPYRIGHT.txt`.

The first isolated scene probe failed because the initial preset omitted raw `.f32` heightfield/carved-geometry inputs: startup could continue with incomplete ground meshes and no reachable walk cells. The preset now includes `.f32`, and payload auditing verifies all 65 native float-data files before the scene probe. This is an export correction; source terrain/game behavior is unchanged.

The bundle includes the whole original JOIN-1 catalogue and arena variants, including worm/larva and `eor_overlay` entries outside `wave_kits.json`. The ZIP gate refuses a bundle missing any original catalogue kit.

Expected export warning: the sealed extension declares only a Mac arm64 library, so Godot warns that it has no Windows x64 library. The generated startup list is suppressed, and the Windows adapter uses the reference solver. Native probes retain the pre-existing 78 NUL decoder warnings from the sealed data reader and Godot shutdown resource/RID leak diagnostics; no sealed reader or shutdown behavior was changed. Fatal script/scene errors are not accepted.

Initial package, before the audio update: `pc_arena/build/BarrowArena-Windows-x64.zip`, 2,439,475,745 bytes, SHA256 `8ea2874dfe0b101e18698b4c72a9e6eb9d6f489b9832d4f4982c8233663b068b`. The final payload audit passed for 3,401 raw/pinned inputs (2,625 original art/VFX files, 42 kits). The isolated Mac reference-solver scene probe passed: native painting, 825 mesh instances, 334 collision shapes, 10 MultiMeshes, 29,200 reachable walk cells, live 3D hero, 51 enemy VFX sets, all 42 kits decoded, 125 combat ticks and 3 m of physical movement. Counts of actor meshes vary with the test seed. Actual Windows executable launch is explicitly unverified in the package manifest.

The final graphics probe also passed from an empty project using the Windows PCK on this Mac: Metal 3.2 / Forward+ / Apple M2, all 42 kits decoded, 812 live mesh instances, 334 collision shapes, 29,200 reachable cells, 125 advancing combat ticks and 3 m of movement. The screenshot `pc_arena/build/logs/native-gpu/native_probe.png` was visually inspected: painted terrain, the barrow structure/door, palisade, snow, hero rig, monster art, shadows and combat effects are present. This is local graphics evidence, not a Windows GPU acceptance claim.


## Audio update — 2026-10-10

The current Windows ZIP includes 42 SFX and all five original demo music tracks, with
Ossuary Procession as the provisional default. M toggles music, K toggles effects,
and B selects the next track. Inventory, gaps, provenance and evidence are in
`../audio_review/AUDIO_REVIEW.md` and `AUDIO_VERIFICATION.json`.

`tools/refresh_pc_arena_audio.sh` updates only the audio manifest/assets and three
presentation scripts in an existing native mirror. It preserves the full build's
20 GiB gate; its separate 8 GiB incremental gate accounts for the existing export
and temporary ZIP. The last delivered ZIP remains intact until the replacement
passes CRC/hash checks and is atomically substituted.

Updated artifact: 2,497,882,092 bytes; SHA256
`e25e01072058e34c96b6a8d60bd55feb40130f2079b614939c9386b2d9a7b3b1`.
Payload audit: 3,449 byte-verified inputs, including all 47 original-byte audio files.
Packed scene probe: all 42 native kits, Forward+, 334 collision shapes, 29,200
reachable cells, 125 advancing ticks and 3 m movement; 42 SFX decoded and five
music tracks available. Packed CoreAudio probe on Mac, using the PC's GDScript
reference solver: 480,256 mixed frames, peak 0.441226 (-7.1 dBFS), no silent
output/clipping, successful/failed cooldown distinction, unchanged snapshot after
audio event consumption, loop lifecycle, independent mutes and the 11-voice cap.
Actual Windows launch, Windows audio/GPU behavior and final listening balance
remain playtest criteria.
