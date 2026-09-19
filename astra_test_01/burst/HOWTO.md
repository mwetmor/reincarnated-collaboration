# HOWTO — the burst lane, procedures a conductor otherwise re-derives (adoption 1, Matt R-C7-15; born 2026-09-19)

> Each entry ≤ 15 lines and points at the script that does it. Law lives in `SPEC.md`, `BURST_RULES.md`, the run charter; this is the *how*. Scripts referenced live in `runs/C-7/conductor_scripts/` (copy + re-point for a new run: `--run`, `briefs/<run>/`, ledger path in `cl.py`). Traps at the end are all things that actually bit.

## 1. Start a conductor session
Read: `.claude/agents/gandalf.md` → OP § 2 → `desirable-run-pattern.md` §§ 3–5 → the run charter → the ledger tail (`python3 cl.py show 8`) → the running account → `runs/FREEZE_NOTICES.md` → `df -h /`. Check concurrency: `ls ~/astra-burst/.heavy.lock && cat` (who holds heavy work) and `ls */scratchpad/c5_*.log` for a WAVE START without DONE. Then the task.

## 2. Fire a burst
Brief = `briefs/<run>/<ID>.task.json` with ALL of: `text`, `references` (list), `image_cap`, `minutes_cap` (≤ 40 TOOLING / ≤ 15 else), `tool_call_cap` (≤ 60 / ≤ 20), `outputs`, `effort: "high"`, `add_dirs` (TOOLING: the burst dir; else `[]`), `experiment`. Missing a key → the wrapper rejects it silently as `invalid task field …` in `<ID>_run.err`.
Add a `SPEC.md § 7` row for every TOOLING burst (its contract). Launch DETACHED, never in the foreground: `zsh wave_detached.sh <logname> <ID>:<TYPE>`; TOOLING alone, under the heavy lock (wave.sh does that). Wait with a background `until grep -q "WAVE DONE" ~/astra-burst/logs/<run>/<logname>.log`. Receipt: `~/astra-burst/runs/<run>/<ID>/out/receipt.json` (+ `acceptance.json` under `runs/<run>/t3/<ID>/`). VOID exit 3 with 0 tool calls = read `events.jsonl` — usually the codex usage limit. Accept/reject in the ledger (`cl.py rulings`), then § 3.

## 3. The freeze ritual (after every TOOLING burst)
`verify.sh suite` (outside suite under the lock; reds listed — compare to the last freeze's list, name every new one) → `verify.sh freeze` (`freeze.sh` = MANIFEST rows/sha/delta; `restamp.py` = 00-system.md § 7 SYNC rows + check_sync 10/10) → append a row to `runs/FREEZE_NOTICES.md` (C-6 reads it) → `cl.py rulings` the freeze with the sha → commit `--only` the named paths (export/, tests/, kits, MANIFEST, 00-system.md, notices, ledger, small evidence JSON — never frames/tarballs).

## 4. PACK + stage + captures
PACK brief = copy the last `CS-pack-v<N>.task.json`, bump N and the kit count/description; fire `CS-pack-v<N>:PACK` (not TOOLING; ≤ 15 min). Output `runs/<run>/artifacts/CS-pack-v<N>/godot` → copy to `runs/<run>/cliffside_v<N>` → headless import under the lock → probes. Picker mapping: `KIT_CYCLES` = the kit's index in `kits_v9.json` FROM 0 (blackwater_cocktail_e3 is entry 12 → 11). Probes: `probe_events.gd` (event trace, one cast), `probe_cast_dir.gd` (8-direction frames), `probe_cast_ab.gd` (N casts spaced `CAST_GAP_FRAMES`, `CAPTURE_FRAMES`). Chain template: `ab_chain_v45.sh` (import → traces → captures → sheets → realtime + third-speed MP4 → purge frames).

## 5. Packet + phone
Desktop folder `~/Desktop/Astra Burst Review - 2026-09-15/<NNN> <title> (open X first)/` with a README (what, arms, verdict list) — and ALWAYS `SendUserFile` the MP4s to Matt's phone (R-C7-0c). Number continues from the last packet.

## 6. The video path (Grok → four-plane frames → bind)
Seed still = OUR painting/primitive, greyscale, on #00ff00, first-frame pinned (never a source clip — class E is measurement-only). Prompt in `runs/<run>/xvideo/prompts.json`, REGISTER CARD clauses carried; `zsh grok_clip.sh <cell> <still> <suffix>` (CLI, ledgered in `grok_calls`). Cut + gates: `bw_cut.py <mp4> <outdir>` (hue key → luma → four planes → gates JSON + sheet). Frames for the bind: the cut in `artifacts/BW-video-r1/frames/` + `frames.json` (timeline, anchor, per-frame sha). Bind = a TOOLING burst (`BL-2v` brief is the template: flipbook body, held last frame, ticks on the clip clock). Two-attempt rule applies to clips as to bursts.

## 7. Web deploy
Dispatch drax (`drax/dispatches/2026-09-18-web13-…md` is the template): build + stage + verify, STOP before push; Matt's push word ledgered as `matt`, relayed by SendMessage; conductor verifies the live `index.pck` sha independently (curl + shasum). Deploy truth lands in `drax/captures/`.

## 8. Concurrency with another run (C-6 law, mirrored)
Heavy work (TOOLING, suite, headless Godot) under `heavy_lock.py <run> -- <cmd>`. Wave logs mirrored as `c5_c7_*.log` into a `*/scratchpad/` dir so the other run's glob sees them. Every freeze → `runs/FREEZE_NOTICES.md`. `--only` commits; never `add -A`; pushes are Matt's.

## 9. Ledger conventions
`cl.py <rulings|milestones|halts|grok_calls|notes> '<json>'`; ruling ids `R-<run>-n`; class `matt` (veto_open false, verbatim words) / `conductor` (veto_open true). HALTs to `halts` with `status`. `cl.py show n` to read.

## Traps that bit (2026-09-18/19)
- zsh does NOT word-split `$P` — use `${=P}` for path lists in `git commit --only`.
- `git -C <repo> add <path>`: paths are relative to the REPO root, not the cwd.
- `${c/BW_spine/BW-video}` in a loop produced `BW-video_r1` (the `_` survived) — check outdirs before chaining.
- `tests/t0c_summary.json` went STALE when the writer crashed on a setUpClass error (fixed BL-2v-b) — `t0c_suite_output.txt` is the record; a burst's sandbox suite OVERWRITES it (keep the outside run's copy in `~/astra-burst/logs/<run>/`).
- Kit PNGs, frames and `artifacts/` PNGs are gitignored: substrate is disk-only — back it up into the packet; the sha list lives in `frames.json`.
- A green check on the wrong question (the picker-path probe was clean while the generic G2 path crashed): the guard must cover every path that loads the resource, not the one you tested.
