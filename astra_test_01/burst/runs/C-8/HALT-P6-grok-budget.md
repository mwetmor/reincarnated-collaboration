# HALT — Run C-8 (F7 external state: Grok Build usage balance exhausted)

- **ts:** 2026-09-20T23:03:21Z
- **call:** `grok_image_ref.sh S_battle_seed_p1` (battle-stance seed still for the attack redesign, R-C8-3)
- **cause (verbatim):** `API error (status 402 Payment Required): Grok Build usage balance exhausted`
- **charter:** § 7 — "Grok's own out-of-budget reply = external-state HALT." No retry, no second route.

## What this blocks
- The **attack redesign** Matt ordered (pommel grip at the base of the haft, wide swing at full reach, bent-knee battle stance): needs 5 new seed stills + 5 new clips.
- The optional **battle idle** that would share those seeds.
- Any further C-8 generation (N cast re-gen, E/NE run third attempts) — none were authorized anyway.

## What this does NOT block
- The **attack port into the cliffside scene** (Matt authorized 2026-09-20). The plumbing — an `attack` state in the exported project, an input action, the state machine branch — is silhouette-agnostic: the redesigned cells drop into the same state when Grok returns. Routed to **drax** (Godot seam) as a post-export patch script.
- The SW/SE walk fix (landed: `cliffside_v40-warlord2`, proof clean).

## Resume condition
Matt's word that the Grok Build balance is topped up (queued as a Matt-to-do alongside T25 Codex). No conductor retry.

---

## SECOND EXHAUSTION — 2026-09-21T01:33Z (`H-C8-GROK-BUDGET-2`)

Matt topped up and said *finish the grok work*. The top-up bought **8 successful calls** before the balance went again:

| # | call | result |
|---|---|---|
| 1 | `S_battle_p1` still | stance right; grip mid-haft, arm cocked (the two things Matt named, both missed) |
| 2 | `S_battle_p2` still | overcorrected — floating barbell + duplicated mace |
| 3 | `S_battle_p3` still | **APPROVED** — pommel grip, arm out, knees sunk, clean plate |
| 4 | `N_cast_r1` clip | re-generate of the flagged overhead-raise cast; cut clean (release 65) |
| 5 | `S_battle_spin` clip | stance held perfectly · **body never revolved** |
| 6 | `S_battle_spin_r1` clip | revolved · legs straightened · zoomed |
| 7 | `S_battle_spin_r2` clip | revolved · knees bent · scale stable · **blur gone** · mace raised beside the helm |
| 8 | `S_battle_spin_r3` clip | arm locked out straight · spin rate collapsed · blur returned |

Then all seven `S_battle_turn_*` stills refused in under 2 s each.

**Reading: clips are the expensive unit.** Three stills and one re-generate plus four 6-second clips drained it. The turnaround-as-spin ruling (**R-C8-5**) is the cheap path forward — 7 stills, no clips — and it is queued and ready to fire unchanged.

**Resume:** top up, then `python3 runs/C-8/conductor_scripts/turn_stills.py` (fires all seven; takes about five minutes).
