# Phase 1 Toggle Operational — Cosmograph A/B Spike

**Date:** 2026-06-07
**Author:** drax

The A/B view toggle is deployed as part of Phase 1 (before Phase 2 full corpus fires).

## Toggle location

Forge page header, top right. Two buttons: "primitive" (Mode A) and "constellation" (Mode B).

## URL scheme

- `/forge` or `/forge?view=primitive` — Mode A (primitive-galaxy, full Phase A render, unchanged)
- `/forge?view=constellation` — Mode B (kit-as-bounded-constellation, Phase 1: 10-kit sample)

## Mode B badge

"SPIKE·P1·10 kits" label appears next to the constellation button when Mode B is active. Clear demarcation that this is spike work, not full corpus.

## Comparison notes for Matt

To compare A/B:
1. Navigate to `/forge` (Mode A — full 570-star primitive galaxy)
2. Click "constellation" toggle in top-right header
3. Mode B renders 10 bounded constellation clusters
4. Click "primitive" to return to Mode A
5. The side panel is shared between both modes (lasso results appear identically)

**Known Phase 1 Mode B limitation:** lasso resolution in Mode B resolves deduped primitives against the full 1000-kit corpus, so the best match in the side panel may be a kit NOT visible in the 10-kit sample. This is correct Phase 1 behavior — Phase 2 renders the full corpus.

## Production status

Phase 1 toggle is committed to `main` on `reincarnated-loadout`. Preview deploy to Vercel fires as part of this commit's push (per established push pattern for this cycle). Production Vercel deploy (`vercel --prod`) requires Matt authorization per ADR-006 — Phase 2 deliverable.
