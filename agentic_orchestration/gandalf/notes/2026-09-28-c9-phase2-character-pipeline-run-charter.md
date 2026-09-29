# Run C-9 · Phase 2: the character pipeline, conducted autonomously (charter)

> **STATUS:** CURRENT — APPROVED by Matt 2026-09-28 (R-C9-70: "Yes, as drafted"; barbarian B; all four cleanup categories under the § 4 rule, the Godot logs/temp after the KC2 conductor confirms). Author gandalf (ARCHITECT, then RUN-CONDUCTOR), 2026-09-28.
>
> **Matt, verbatim:** *"Can we turn this into an automated RUN conducted by you? One thing to consider is storage space on this PC... We may need to delete some of our recent work and also make a plan to delete more as we go potentially. There is a battle simulation run also going on right now and they have an auto halt at 40GB of space where we are currently at 51GB of available space."*
>
> **Continuity:** this is Phase 2 of Run C-9, not a new run. It keeps the C-9 ledger (`astra_test_01/burst/runs/C-9/ledger.json`), the lane, refs_guard and all rulings to date (R-C9-41 … R-C9-69). Phase 1 was the search that ended in the 3D route (R-C9-60 … R-C9-67).

## 1 · Target state (decidable: each item is done or it is not)

| # | Deliverable | Done when |
|---|---|---|
| D1 | **Barbarian base body** (T8, R-C9-69) | Rigged; idle, walk, run, attack and block clips; a painted texture by the T5 projection method; walking in the 3D cliffside at the real 52.95° camera (R-C9-68); capture MP4 filed |
| D2 | **Barbarian modular gear** | Helmet and bracers (rigid, on bones); tunic and mail shirt (deforming, weights from the body); fur mantle; bearded axe and round shield on hand sockets. Each piece is made by EDITING the NB-1 sheet, so it shares his pose and scale. A swap test with no repaint; capture MP4 filed |
| D3 | **Manticore NPC** (R-C9-66) | Per-frame paint in all 8 directions × walk, idle, run and attack, gated (pose, matte, face) and assembled into `sprites_t2/`; live in the 2D cliffside as an NPC (the push only under R-C9-61 or Matt's word) |
| D4 | **Test verdicts** | T4 Kling vs Ludo (drift numbers on the same input) · T5 painted-texture manticore · T6 generator bake-off · T7-A projected-paint 3D cliffside · T7-B World Labs world. Each is one short verdict with captures |
| D5 | **The pipeline recommendation** | One page for 100+ characters: the route, per-character cost and time, gear cost, what remains manual |

## 2 · Where the run stops for Matt (everything else proceeds without asking)

- **G1:** the barbarian's look. The base sheet and the first 3D build are ready now. Texture and gear work waits on this.
- **G2:** the barbarian walking in the 3D cliffside.
- **G3:** the first gear layer on him.
- **G4:** any push. Only the loadout `/playtest/cliffside/` route is already authorized (R-C9-61). No push of reincarnated-godot or collaboration without Matt's word. A new route also needs Matt's word.
- **G5:** any spend beyond the caps in § 3, and any deletion outside the policy in § 4.
- Unchanged: no seed changes; no franchise, studio or living-artist names in prompts; copyrighted game images stay look-only.

## 3 · Spend caps (Phase 2 totals)

| Service | Cap | Planned use |
|---|---|---|
| Astra (lane) | 300 images | Gear sheets, texture paint sheets, manticore re-fires. The binding limit is the weekly ChatGPT allowance |
| Meshy | 600 credits | Barbarian model, rig and clips; the gear pieces (~30 each); text-to-motion (10 each) |
| fal.ai | $20 | Background removal; a generator re-run on the barbarian if T6 names one better than Meshy. **Kling in 8 directions (~$40) is NOT included (Matt's call)** |
| Ludo | 300 credits (of 1,030) | Test 4 close-out; one barbarian run at Ludo's steep top-down setting |
| World Labs | 5,000 credits (of 7,000) | T7-B: one draft (230), then one or two standard worlds (1,580 each). **An HQ mesh export (3,500) is NOT included (Matt's call)** |

## 4 · Disk guard (Matt's constraint; binding on every agent in this run)

- **The shared floor:** a battle-simulation run halts at 40 GB free. At charter time there were **45 GB free** (`df -H`; Finder's figure, 51 GB, counts purgeable space).
- **This run's floor is 44 GB free.** Before every burst group, render batch, model download or world generation, the conductor checks `df -H`. Below 44 GB, heavy work pauses and pruning runs. Heavy work resumes above 46 GB.
- **Net growth budget for Phase 2: 5 GB**, measured against the charter-time baseline.
- **Prune at every stage close (pre-authorized for this run's own files only).** Delete regenerable intermediates:
  - frame dumps extracted from videos;
  - render sequences a committed script can re-create;
  - lane burst workspaces of delivered bursts (their outputs are in `artifacts/` with sha256);
  - scratch.
- **Record every deletion in the ledger** (path, size, reason).
- **Never deleted:** approved outputs, receipts and provenance, ledgers, scripts, final MP4 captures, final models.
- **Anything outside this run's own files needs Matt's approval of a listed manifest:**
  - older runs;
  - other agents' captures;
  - other repositories;
  - untracked files git cannot restore.

## 5 · Reporting

- One short message at each milestone (a gate, a test verdict, a halt).
- Captures go to Matt's device as they land.
- The ledger carries the record: milestones, notes and any halts, with verbatim Matt quotes for rulings.

*— gandalf (ARCHITECT), 2026-09-28. Anchors: R-C9-60 … R-C9-69 (C-9 ledger); `2026-09-28-character-pipeline-review.md`; `2026-09-28-humanoid-animation-common-thread-verdict.md`.*
