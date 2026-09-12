# Legolas — Mode A commission: AI tells in painted game art · art-bible practice · deterministic oracles for generated art

> **From:** gandalf (RUN-CONDUCTOR, Astra burst lane Run C-1). **To:** legolas (UNKNOWN-RESEARCHER, Mode A analytical). **Date:** 2026-09-11. **Priority:** gates K1 (pilot identity) of Run C-1 — the run is paused on this return.
> **Budget:** ≤ 1 session. Read-only. Web research permitted; **primary sources cited** (talks, papers, docs, artist-authored critiques); practitioner claims graded (VERIFIED / PRACTITIONER-REPORT / UNVERIFIED). No paid resources, no code, no images generated. Two focused search passes per thread, then stop and record the gap.
> **File at:** `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` (+ `sources.json` per your OP). Report the path in your completion record.

## 0. Why (context you need, nothing more)

We are testing whether `gpt-6-astra` (OpenAI Codex, built-in `image_gen`) can produce **painted-2D** ARPG sprite sheets, gear layers, VFX and scene plates under strict guidelines, judged by numeric gates + a separate Astra instance. Charter: `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md`. Register anchors (view them): `astra_test_01/design/experiments/E07V/art/F04.png` (clean-clarity target), `F03.png` (light/detail target), `astra_test_01/run_03/evidence/vfx_style_match.png` (painted VFX edge language).

**The observed defect (Matt, 2026-09-11):** on F04's advanced figure the handheld astrolabe's ring-and-spoke geometry recurs as a pauldron emblem, a chest-strap boss, chart diagrams on three tabard panels, and the starter satchel's clasp — *motif bleed*. F03's figure (prompted with construction/material nouns — coat, harness, firearm) shows only rivet over-texture and doubled straps. Working hypothesis: **motif-nouns bleed; material/construction-nouns over-texture; the tell is detail without ownership** (straps carrying nothing, buckles closing nothing). Matt's question: *if we remove tells, do we remove detail — and must we supply the detail (insignias, stitching, construction) ourselves?* gandalf's working answer: yes, via a faction art bible; your job is to ground or refute that with evidence.

## 1. Thread R6 — AI tells in painted / illustrated game art

1. **Taxonomy.** Confirm, correct or extend this candidate list with sources (illustrator-authored "how to spot AI art" critiques; concept-art community discourse; academic "generative artifact" literature): motif bleed / semantic leakage · ornament without function · near-symmetry drift · glyph gibberish (pseudo-text sigils) · material confusion at boundaries · specular-on-everything / HDR sheen in "painted" work · hands & weapon grips · intra-object perspective drift · the default face · photographic artifacts (bokeh, flare) in painted work · texture stutter / repeating micro-pattern · non-functional armor / impossible anatomy · edge halos.
2. **Which tells are *stylistic* vs *structural*.** Stylistic tells vanish with restraint vocabulary; structural tells (ownership, construction logic, symmetry) need authored input. Evidence for the split.
3. **Prompt-level mitigations with evidence, for GPT-image-class models specifically:** single-naming + exclusion clauses ("appears on X only; all other surfaces plain") · negative/avoid lists — what these models actually honour · reference-image conditioning of an isolated motif (copy vs interpret) · two-pass generation (plain planes first, ornament as an edit with invariants) · "restraint" / "production asset, not concept art" vocabulary · material-first vs motif-first prompting. Primary sources: OpenAI image-generation prompting guidance (the local skill docs at `~/.codex/skills/.system/imagegen/references/` are a start; find the published counterparts), credible practitioner reports. **Mark folklore as folklore.**
4. **What a tell-free painted asset still needs to read as "detailed"** — the rendering-vs-decoration argument (form, edge control, value hierarchy, material response). Sources from concept-art pedagogy (e.g., published concept-art instruction on detail vs rendering), not AI discourse.

## 2. Thread R7 — what real ARPG / stylized-2D art bibles contain

Extract the **structure** (fields, rules, examples) of published or talk-documented art style guides: Diablo II / III / IV (Blizzard art books, GDC/BlizzCon art-direction talks — D3's readability/"iconic silhouette" rules; D4's "return to darkness" material/palette rules), Path of Exile (GGG art talks — per-act material palettes, silhouette), Grim Dawn (Crate art direction), Hades / Hades II (Supergiant — Jen Zee character design language, painted world), Darkest Dungeon (Red Hook — Chris Bourassa's style rules), Bastion. Specifically: motif inventories + placement rules · material palettes with counts · construction logic · silhouette / read-at-distance rules · palette + value rules · the *plain-surface budget* (if any studio names it) · how they keep 100+ characters "one game" (shared language vs per-character motifs). Deliver as a **schema proposal** for our faction bible (see § 4) with each field justified by at least one precedent.

## 3. Thread R8 — deterministic oracles and judgment gates for AI-generated art (games; 2D painted)

**Matt's ask, verbatim intent:** *"research any headway that researchers or game devs have made in developing deterministic oracles or judgement gates for AI-generated art (especially for games and 2D painted style) … methods that could be applied in our work here and could feed the bible itself with vocabulary rulings as the gates."*

1. **Academic / tooling metrics applicable to per-frame painted sprites:** identity-preservation across frames (CLIP-I, DINO-I, IP-Adapter/DreamBooth-style eval metrics; face/character-embedding distances); temporal consistency metrics borrowed from video generation (warping error, FVD-class) and their applicability to 8–12-frame loops; artifact detectors (hands, text/glyphs); symmetry/structure metrics; palette-adherence metrics; high-frequency/grain metrics (Laplacian variance, spectral energy) as a "brush-grain" oracle vs an anchor; shading-gradient → light-direction estimation as a key-light oracle; silhouette shape descriptors at 64 px; template/feature matching of a motif reference to **count motif instances outside declared placement boxes** (the motif-bleed oracle); AI-image detectors as a *tell* oracle (what they actually detect). For each: what it measures, known failure modes, cost, whether it needs a trained model or is closed-form.
2. **Game-dev practice:** published gen-AI asset pipelines with acceptance gates (GDC 2024–2026 talks, studio blogs, indie postmortems); commercial tools (Scenario, Layer.ai, Ludo, SpriteCook, Frame Lab, Spriterrific) — do any expose *gates* or consistency scoring, and on what basis? Distinguish marketing from measured.
3. **Applicability to Run C-1 — the shortlist (≤ 10):** each with: what it enforces (which tell / which bible rule) · inputs it needs *from the bible* (placement boxes, palette hex list, motif reference crop, plain-surface mask, anchor set) · closed-form vs model-backed · estimated cost to stand up with Pillow/numpy/OpenCV only (our T0 tooling constraint — no GPU models unless trivially available) · confidence.
4. **The bible ↔ oracle coverage table:** rows = tell categories / bible rule classes; columns = mitigation (prompt lever) · deterministic oracle (id or none) · JUDGE-only · what vocabulary the bible must carry for the oracle to run · evidence grade. **Rules with no oracle stay JUDGE-only; that list is the R8 backlog.**

## 4. Target shape — how your findings are consumed (do not build it; tag findings so it can be built)

gandalf authors **Faction Bible v0 (F04 Keepers)** + charter v1.1 from your return; Matt rules the vocabulary with your findings in hand. Bible rule schema (draft):

```
RULE { id, faction, class: motif|material|construction|silhouette|palette|plain-budget|light|scale,
       statement (one sentence), placements[] {where, scale, count}, exclusions[] (where NOT),
       reference_asset (crop path | null), oracle {id | JUDGE-only, threshold, inputs},
       known_bad (crop path), source: matt-ruling|bible-author|oracle-feedback, date }
```
Tag every R6/R7/R8 finding with the rule class(es) it informs and whether it yields a **prompt lever**, an **oracle**, a **JUDGE axis**, or a **bible field**.

## 5. Stop rules and honesty

- Two focused primary-source passes per thread; record the gap and move on. No "marketing page = inspected."
- Grade every claim. Distinguish "used in a shipped game" from "paper result" from "forum practice."
- Nothing here authorizes tooling, spend, or generation. Findings only.

— gandalf, 2026-09-11
