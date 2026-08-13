# RUN KC2-PM2 — the FIGHT lap (charter + ledger)

**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-08-12 at Matt's word ("agreed on F-5 and F-6", closing the six-fork elicitation — KC2-PM1 ledger § E-1)
**Lineage:** KC2-PM1 (movement lap, CLOSED 2026-08-12) → **PM-2 = incoming damage exists** (single delta: THREAT). SB-1 scene lane is separate and untouched.

## Intent (Matt, verbatim anchors)

- *"I am quite frustrated that we simulated something that wasn't a fight."* — PM-2's reason to exist. The sim gains real enemy damage; the player can die; survival becomes measurable.
- Avoidance directive (banked verbatim at PM-1 ledger R-PM1-6): attempt to avoid a large telegraphed AOE ~once per 20 s; succeed ~half the time; favor avoidance of telegraphs the player has been inside longer and nearer the edge of; mimic a real player with attention-loaded reaction time.

## The six fork rulings (all Matt-ruled 2026-08-12; detail at PM-1 ledger E1-3..E1-5)

| fork | ruling |
|---|---|
| **F-1 player defense** | **Matt-provided data, two-source:** 117 screenshots `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/screenshots/` = **PRIMARY** (played-state truth; Screenshot (495) = EoRWarlGuts L100 Warlord, Health 20,005 EXACT-matches the baton `player_hp` track) + pristine `player.gdc` forum zip (URL in `/Volumes/reincarnated/agent-prompts/2026-08-01-eor-warlord-playtest-directions-v3.md` § R-V3-2) = machine-readable **cross-check**. Disagreement resolves toward screenshots. |
| **F-2 monster damage magnitudes** | **(a)** legolas decode lap extends `tg2_attack_slots.csv` with per-rank damage min/max + OA/DA hit math. The .arz corpus has them (`n_damage_ranks` proves it); the 08-08 harness never pulled them. |
| **F-3 sustain** | **(a)** leech (ADCtH — rides the existing damage-dealt rows) + regen, values from the F-1 sheet. |
| **F-4 avoidance AI** | **Ratified both refinements as written:** (i) geometry-decided dodge success — ONE declared reaction-latency constant; move full speed toward nearest telegraph edge, channel on; success = escape before detonation; Matt's ~50% = the calibration target; his favor-criteria (long-exposure, near-edge) emerge from the geometry. (ii) attention-load-scaled reaction — latency scales with live enemy count by a declared function. Telegraph identification = geometry-decided from decoded `skill_radius` + warmup/charge durations (gamora reasoning-boundary, declared rule). |
| **F-5 run matrix** | **(c)** the full 2×2 factorial, four cells, same seed, all under threat: **CAMP · DRIVE · DRIVE+DODGE · CAMP+DODGE**. Determinism ×2 each; survival + kill curves compared cell-vs-cell AND against both frozen threat-free batons. Yields both main effects + the seek×dodge interaction; Cell 4 (plant–clear–sidestep–replant) is the most realistic melee pattern of the four. |
| **F-6 summon threat (92/169)** | **Conditional (a):** full pet actors (spawned actor + owner pointer + cap ≤4; worst case ~368 extra bodies) **gated decidable** on Lap B's pet-record chain — clean decode → (a) fires on real substrate; extraction cliff → **pre-registered honorable fallback (b)**: declared exclusion with the cliff documented + excluded-threat fraction quantified on the wire. No fabrication either way (GL-12). |

## Laws (binding)

1. **FROZEN substrate:** baseline baton `d7ecd866…` + PM-1 sibling `4585eeb8…` — read-only, digest-verified before load (GL-6).
2. **Determinism ×2** per cell, masked digest EXACT (FG-10; mask = emitter's own PROVENANCE_VOLATILE_KEYS, imported not invented).
3. **NO balance tuning.** Survival curves are FINDINGS — including "sim player dies where Matt survived" (reference truth: Matt survived the real run; divergence is the headline metric, not a bug to tune away). **Calibration rider:** setting the ONE reaction-latency constant to hit Matt's ~50% dodge-success directive is charter-directed calibration, NOT balance tuning.
4. **Schema delta declared on the wire:** new event families (damage_taken / dodge_attempt / player_death / pet_spawn if F-6(a)) ride informative rows, kc2-baton-v1 family retained where possible; any field addition named in the receipt.
5. **Seams:** gamora writes ALL engine code (charter word carried from PM-1); export amendments minimal + `export/MIGRATION.md` per ADR-004 + star-lord flagged. legolas laps are read-only extraction filed to `legolas/notes/`. Conductor writes no production code; CL-10 verification from own seat at every landing.
6. **L-0 pins fire at the gamora cell's launch** (engine HEAD, porcelain baseline per FG-17, substrate digests). **`/Volumes/reincarnated/` capture dirs are FIRST-CLASS substrate** (procedural fix from the E1-2 conductor miss — substrate sweeps enumerate them).
7. Basis discipline (NOTE-9 family): every quantity asserts its population; instrument schemas declared (the two-surface cliff + the magnitude gap were both instrument-schema misses).

## Cell sequence

| cell | seat | scope | gate |
|---|---|---|---|
| **Lap A — player sheet extraction** | legolas | Transcribe the character sheet from the eor-test-2 screenshots (attributes, OA/DA, armor, ALL resistances, health/energy, ADCtH/leech sources, regen, movement speed, relevant proc/granted skills); re-download pristine zip, parse `player.gdc` as cross-check; file measured-sheet artifact + discrepancy table. | fires NOW, parallel with Lap B |
| **Lap B — threat decode extension** | legolas | Per-rank damage magnitudes + OA/DA hit-math constants for all attack slots + damage-bearing granted-tree skills; the summon-skill→pet-record chain for the 92 summoners (pet stats/attacks/caps). Extends the tg2_* CSV set. **Decides the F-6 gate.** | fires NOW, parallel with Lap A |
| **Fight cell** | gamora | Incoming damage + defense math + sustain (F-3) + avoidance AI (F-4) + the 2×2 matrix (F-5) + pets per the F-6 gate; four sibling batons + digests ×2 + assert wall + comparative survival findings. | fires ONLY after Laps A+B land + conductor verifies |
| **Landing** | conductor | CL-10 verification from own seat; findings to Matt; **HALT before any scene-side consumption** (SB-1 machinery, separate beat on Matt's word). | — |

## Target-state (decidable)

Four sibling batons emitted + digest ×2 exact per cell + policy/damage asserts green + survival-curve findings vs both frozen batons AND vs reference truth (Matt survived) + F-6 gate outcome documented + this ledger updated → **HALT to Matt with the numbers.**

## Matt interface

Commitment-boundaries: F-6 fallback firing (if the cliff hits, the (b) fallback executes per pre-registration but the outcome HALTs to Matt with the excluded fraction) · any tuning temptation beyond the declared latency constant · scene-side consumption. Everything else = reasoning-boundaries, veto-open, ledgered.

---

## Ledger

| row | content |
|---|---|
| **L-0** | Charter authored + Matt's closing word banked: **"agreed on F-5 and F-6"** (2026-08-12). Laps A + B fired in parallel (legolas ×2, background). |
| **L-1** | **F-1 SOURCE UPGRADE (Matt-offered, conductor-accepted): Matt sends his ACTUAL played save** — strictly better than the re-downloadable pristine zip, and Screenshot (495) already proves the delta (Gutsmasher carries a Potent Olexra's Fervor Black Legion rank augment absent from the pristine build; played state = post-v1.2-migration + applied augments). Requested drop: the full character folder (`save\main\_<Name>\` zipped, sidecars included) at `/Volumes/reincarnated/GD-matt-test/eor-test-2/save/` — a `matt_to_do`-class action (host-level; PC tunnel machinery retired). **Source ranking re-based: screenshots = PRIMARY for effective stats (computed totals with live buffs) · played save = machine-readable truth for gear/skills/devotions · pristine zip = lineage/fallback.** Lap A's parser (built against the pristine zip) re-runs on the played save when it lands; nothing blocks meanwhile. |

| **L-2** | **PLAYED SAVE RETRIEVED (Matt's word: "please just tunnel into my PC's GD save file folder and copy the warlord file here" — ADR-006 Matt-directed external action).** Tunnel coordinates recovered from git-lineage (pre-teardown CLAUDE.md @ `44bb9286`): `mhwet@192.168.1.133`, passwordless. Source located at `C:\Users\mhwet\OneDrive\Documents\My Games\Grim Dawn\save\main\_EoRWarlGuts\` (**Documents is OneDrive-redirected** — the plain Documents path 404s; the directions doc § 5 "confirm the path" clause proved out). Landed at `/Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/`: **111 files, 2.3 MB; `player.gdc` 98,101 bytes byte-count-EXACT vs PC source, PC mtime 2026-08-05 (post-playtest), sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`**; rolling backups (.g00–.g09, .gdc.bak) + **`maps_survivalworld_*` dirs = the Crucible's own save state** (flag to Lap A at landing — parse the PLAYED save as gear/skills/devotions truth per L-1 ranking; the survival-map state is a possible reference-truth cross-check). |

*Charter + ledger opened by gandalf (`RUN-CONDUCTOR`), 2026-08-12.*
