# VDM-1 b05 author_credit backfill — 2026-07-18

**Backfill scope:** 10 previously-abstained author_credit rows from batch-05-dossier.jsonl.
**Trigger:** batch-06 falsified the b05 premise that maxroll.gg guides do not expose author handles.
**Output file:** `batch-05-dossier-authorcredit-backfill.jsonl`

## Per-kit handle table

| kit_id | handle | site | source type | conf |
|---|---|---|---|---|
| le-fire-aura-spellblade | Lizard_IRL | maxroll.gg | byline ("Written by") | 0.95 |
| le-flame-reave-spellblade | Lizard_IRL | maxroll.gg | byline ("Written by") | 0.95 |
| le-ghostflame-warlock | Volca | maxroll.gg | byline ("Written by") | 0.95 |
| le-hammer-throw-paladin | Volca | maxroll.gg | byline ("Written by") | 0.95 |
| le-harvest-lich | Volca | maxroll.gg | byline ("Written by") | 0.95 |
| le-healing-hands-paladin | Aayron | forum.lastepoch.com | thread OP | 0.80 |
| le-judgement-paladin | Volca | maxroll.gg | byline ("Written by") | 0.95 |
| le-lightning-blast | BinaQc | maxroll.gg | byline ("Written by") | 0.95 |
| le-low-life-ward | Zaodon | forum.lastepoch.com | thread OP | 0.75 |
| le-manifest-armor | Lizard_IRL | maxroll.gg | byline ("Written by") | 0.95 |

## Summary counts

- **Recovered:** 10 / 10
- **Still abstained:** 0 / 10
- **Fetch failures:** 0

## Notes

- All 10 maxroll.gg and forum.lastepoch.com pages returned clean author attribution on first fetch.
- The b05 abstention premise ("maxroll guides do not expose individual author handles in page prose") was incorrect — bylines are present in the rendered page content as "Written by \<handle\>" blocks.
- Forum kits (le-healing-hands-paladin, le-low-life-ward) use thread OP username as author_credit per schema convention; conf is lower (0.80, 0.75) because thread OP identity is weaker attribution than a named guide byline.
- Reviewer handles captured in payload_json for completeness but are not the primary author_credit handle.
- le-frost-claw and le-frost-wall-rm were already populated in b05 and are NOT included here.
