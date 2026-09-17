# HALT (external-state) — the ASTRA path: Codex usage limit exhausted

- **ts:** 2026-09-17T04:43Z (first VOID N11-jdg-01 04:42:45Z; retry N11-jdg-01-r1 04:43:46Z)
- **cause (verbatim from codex events):** "You've hit your usage limit. Visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Sep 22nd, 2026 11:55 PM."
- **scope:** every Astra burst (GENERATE / JUDGE / PACK / TOOLING) on this Mac — Run C-5's FL-6d and FL-6d-r1 VOIDed identically at 04:40/04:43Z. Not a C-6 lane defect; the two VOIDs are the same outage, not two model failures.
- **what continues without Astra:** Grok i2v (separate budget); the frozen T3 tools run locally (conductor-driven CUT/CHECK/TRANSCRIBE per the C-3 `cut_signed.py` / `assemble_cells.py` precedent); PIL packets built by the conductor.
- **what waits:** any further re-mint/edit of a seed; Astra-authored PACK review pages; C-5's TOOLING.
- **C-6 disposition:** the N11 judgment was written by the first VOID before its turn failed → harvested to `runs/C-6/artifacts/N11-jdg-01-harvest/` (no receipt; provenance = events.jsonl). If W/NW/SE pass it, P2 closes on the conductor-built Packet 102 for Matt's eye; P3 (Grok) proceeds on his word. Resume of the Astra path is Matt's (top-up) or Sep 22.
