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
