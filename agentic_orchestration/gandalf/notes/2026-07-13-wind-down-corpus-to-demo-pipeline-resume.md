# Wind-down state-of-record + resume — the corpus-to-demo pipeline

> **STATUS:** CURRENT — single resume surface for the next session (Matt directive 2026-07-13: *"a single document that captures what we have done… and keys up the plans to get the views up so that we can ultimately develop the periodic table of kits and then move them all from corpus to engine roster and then actually emit them as JSON so that I can make the selection of which kits I want to include in the Demo."*)
>
> **Authored:** gandalf, 2026-07-13 (session close). V1.2 findings folded in (agent returned + verified before authoring). §7 naming-law + Steam-validation rider folded same session (Matt-forwarded Gemini research, gandalf ADOPT-with-refinements verdict).
> **Companions:** Q19/Q25 rows in `canonical/matt_decision_needed/README.md` · serial tracker CONTINUATIONs 18–19 (pointers) · `gandalf/views/v1-plane/plane-b-prime-lock-addendum.md` (the plane's technical record) · `matt_notes_handoff_docs/gemini-steam-mothership-research-and-kit-naming-advice-for-devlog` (§7 source).

---

## §1 THE RULED PLANE — the session's central product

**Plane = 3 movement rows × 7 delivery columns, every cell stratified by damage tempo.**

| Axis | Values | Source of record | Semantics |
|---|---|---|---|
| **Rows** | FREE-MOVE / WALK / ROOTED | `canon_engine_key.mob_policy_while_casting` | **FEEL** — what your legs do while you deal damage |
| **Columns** | PROJECTILE · ORBITAL · NOVA · ZONE · BEAM · MELEE · SUMMON | `geometry_value` (+ cone Path 2 refinement; RING merged into ORBITAL; NOVA/ZONE = burst-at-caster vs placed-persistent) | **LOOK** — what the screen shows |
| **Strata (within cell)** | FLAT / SPIKY / VAR, fixed top→bottom order | `canon_corpus.amp_val` | **TEXTURE** — how the damage arrives |

**Rulings, verbatim-anchored (all Matt, 2026-07-13):**
1. **Cone Path 2** — *"agreed"*: geometry `cone` refines by probe `delivery.value` → cone-beam ×5 → BEAM (Incinerate, FoI, Flamethrower, Dragon's Breath, Burn Exterminator); cone-projectile ×6 → PROJECTILE (Multishot, Strafe, Frost Claw, Galvanic Shards, Shotgonne, Ternion). ZONE purifies 116→94.
2. **Rows + strata** — *"3X Rows (FREE-MOVE/WALK/ROOTED) each split by (DAMAGE TEMPO [spiky, flat, etc]) X 7X delivery-family columns… the box would be split/grouped/stratified (whatever works best) by DAMAGE TEMPO (flat, spike, var)."* Rendering grammar (gandalf's call under "whatever works best"): fixed stratum order in every cell so strata align into chart-wide scannable bands; empty strata stay visible (frontier signal).

**Why the rows changed:** Matt challenged the inherited commitment rows (instant/wind-up/channel) — the one assumption both candidate planes shared and my delta read never stress-tested. Empirics vindicated the challenge: instant = 413/463 (89% pileup, ~1.25 effective rows). Movement-tax was already keyed corpus-wide (269/108/80) and Matt's amp compound was too (313/115/34 — the `amp_val` enum literally matches his "spiky, flat" language). **Commitment is NOT demoted** — it stays a measured archive axis, design-active in GX-19/GX-20.

**The discriminative-power arc across the lock sequence** (max-pileup / HHI at cell grain):
Plane A spec 174 / 0.222 → Matt's mock 157 / 0.208 → B′ V1.1 109 / 0.157 → **RULED V1.2 65 / 0.081**. Each ruling roughly halved the pileup.

### V1.2 render — delivered, verified, and Matt-approved on look

`plane_view_v1_2_stratified.png/.svg` + `render_v1_2_stratified.py` + `occupancy-stats-v1-2.md` + addendum §10 (commit `62183c1a`). Gandalf verification: FREE-MOVE×PROJECTILE=65 exact, WALK×BEAM=0 exact, amp-NULL kit + poe2-unknowns exact, all cross-tab anchors clean; raster inspected visually. **Matt: "I love the V1.2 plane view btw!"** — look-half of look-and-lock is positive.

- **Cell grain (21):** 20 occupied · only empty = WALK×BEAM · max 65 · HHI 0.081
- **Bucket grain (63):** 50 occupied · 13 empty (12 are VAR-band) · max 53 (FREE-MOVE×PROJECTILE×FLAT) · HHI 0.046
- **Whitespace headline:** ROOTED×VAR empty in 5 of 7 columns; VAR scarcity corpus-wide (34 kits). These are frontier cells for expansion design.
- **DL-03 divergence marker:** genre beams mostly root (ROOTED×BEAM = 14; WALK×BEAM = 0; FREE-MOVE×BEAM = 2). DL-03 (*streams never tax movement*, design law per GX-21) points engine stream-kits at the FREE-MOVE×BEAM cell the genre barely ships — the atlas will visibly display corpus dots in a cell our emissions treat as forbidden (ROOTED×BEAM) and engine dots where the genre is thin. The chart shows where we deliberately diverge.
- **UNMAPPED residue:** 7 corpus (6 poe2 movement-unknown — single-source keying gap: archmage-totems, shaman-bear, snipe-mirage, spiral-volley, walking-calamity, whirling-assault — + Temporalis Blink pure-mobility) · 1 amp-NULL (d2-wl-void-rift, honest sliver in WALK×ZONE) · 45 roster kits pending backfill.

**REMAINING GATE ON Q19: Matt's formal lock word** — lock the RULE (axes + assignment rules + stratum order = permanent cell addresses as kit identity), not the raster (dots/badges stay per-version payload).

---

## §2 Session ledger (2026-07-12 → 13, hash-anchored)

1. **Corpus DB landed + VERIFIED 30/30** (`c124e90` elrond ingest; `83a5a2c` gandalf verification): 524 canon_corpus (515 CSV + 9 mint) · 4,780 probe facts (478×10) · 478 engine-key (463 combat / 15 system-record) · 45 roster_atlas + 45 lineage enrichment. Errata fixed at source: damage-amp 100→97, freeze 43→42 (board generation pre-dated J-GEO strip), walls=3 machine-encoded (`resolved:walls-demand` on frost-wall). **D6 law:** boards are derived views; the DB governs; clean rebuild reproduces.
2. **V3 mechanics-leverage board BUILT** (`d685e86`) — the pause-2 decision surface.
3. **PAUSE-2 CONVENED — Matt ruled the full batch (Q25):** add-list ALL-IN rows 1–11 (#12 draft/pool-steering OUT) · wave order **A summoner/proxy → B reservation/aura → C trigger+mark-consume**, small adds ride open seams, ailments parallel · caster/summoner/aura growth tilt ACCEPTED · ailment design session COMMISSIONED (damage-amp + freeze + stun + poison-dot; taunt rides Wave A; GX-15 folded in) · GX hearings: 02 RATIFIED→keystone, 12 PARKED + hypothesis-as-descriptor (*"could this be produced naturally via element pipeline?"*), 15 FOLDED, 18 RATIFIED, 19 RATIFIED (Wave-A nucleus: proxies that ABSORB commitment), 20 RATIFIED→econ/commitment design, 21 RATIFIED + **DL-03 adopted as design law: streams never tax movement** · emission gate unchanged (§F.4 Matt-judged coverage, no count).
4. **Evidence dossiers delivered + verified (pause-2 fan-out):**
   - `gandalf/design-inputs/wave-a-summon-proxy-evidence-v1.md` (`04880d99`) — 48 kits / 15 games / 5 clusters; `_DEFERRED_PROXY_BINS` frozenset = the single emission gate (`bc_target_composer.py:97/:318` — verified exact); ranged-ally nav seam at `spatial_gauntlet/spatial_engine.py:1149/:1769/:2650` (**erratum: dossier said ~1996**); economy patterns — cooldown-gated dominant (20), reservation + harvest have NO engine analog (Wave-B seam must stay open in the Wave-A spec).
   - `gandalf/design-inputs/ailment-layer-evidence-v1.md` (`460ecc65`) — damage-amp 97 kits (~21%, genre's #1 missing mechanic; **erratum: dossier says 100/43 in two spots — DB-governed counts are 97/42**); **shock naming collision:** engine `shock` = control-class, genre shock = %-damage-taken amp (67 of the damage-amp citations are lightning) — agenda item #1 for the ailment session; freeze = chill's hard-lock escalation + shatter payoff in 6 games (completes an existing engine pair, not a new concept).
5. **Q19 lock sequence executed end-to-end** (§1 above): V1 dual render `177f0cc` → B′ verdict → B′ addendum + V1.1 `97343067` → row challenge → compound ruling → V1.2 `62183c1a`. Ruling records: `05513601` (cone), `dcdd49c3` (rows).
6. **Agent-routing pattern established (Matt directive):** offload prompts run as **seam-typed agents on opus** (`subagent_type` + `model:"opus"`), never fable, no sonnet down-shift. Validated 3-for-3 (B′ addendum, V1.2 render, + evidence agents). Trust-but-verify caught real drift every time it was applied this session (nav line numbers, freeze count, cone→ZONE misroute — the last surfaced by the sub-agent against my own brief, discipline working as designed).
7. **Push stack: 15 commits ahead of origin/main** — HELD behind E4 Gate-2 (jack-ryan verdict on `785956c`), Matt-gated.

---

## §3 THE ARC — from here to Matt's demo selection

Operationalizes the already-RULED emission-selection order (PART F §F.5: pool → mechanics buildout for maximal coverage → cell-duplication tiebreak → emission realizes full kits → demo curated kit-by-kit, no count) into stages with gates and owners.

| Stage | What | Owner(s) | Gate / depends on |
|---|---|---|---|
| **S0 — Q19 formal lock** | Matt speaks the lock word on the ruled plane → gandalf canonizes the plane rule (renderer-spec §2 amendment: movement×delivery×amp supersedes commitment×dispersion for the atlas; archive axes unchanged) | Matt → gandalf | **Only Matt's word.** Look-half already positive |
| **S1 — Data completion wave** | ONE elrond rebuild carrying: 45-roster backfill (movement + amp + commit from engine sources of record — `bc_target_cell_sampler.py` CellDefs + battle-sim configs); `delivery.value` probe→keyed column; 6 poe2 movement-unknowns; void-rift amp if resolvable; **`era_year` + `stabilization_patch` columns (public-register naming feed, §7.1** — era from per-game meta ×19 already landed; patch pin from probe `sources_used` where present, NULL-honest otherwise). Parallel legolas: mint dossiers ×9 (paste-ready, queue row 4) + kb live-URL backfill | elrond + legolas (seam agents, opus) | Rebuild UNBLOCKED (no agents mid-read). Gandalf drafts the brief |
| **S2 — Remaining views** | **V7 negative-space map** (seed exists; now supercharged by the 63-bucket whitespace: 12 VAR-band empties, ROOTED×VAR 5/7, WALK×BEAM) · **V8 behavior map** Edition-I display contract (synthetic watermark) · **NEW: migration-readiness census** — per-kit expressibility: emittable-with-current-mechanics vs Wave-A/B/C-gated vs mint-only. This census is the steering table for S5 | gandalf (+ sub-agents) | S1 for full fidelity; V7 can fire before |
| **S3 — PERIODIC TABLE (PROMPT 5)** | The renderer harness proper on the locked plane: isotope-seq sub-ordering within strata, badges/dots as per-version payload, **permanent cell addresses = kit identity**, corpus ghosts + engine solids on equal footing. V1.2 is the coverage dashboard ancestor ("a contingency table wearing the periodic table's costume" — views README); the table adds identity payload + browse affordances. This is Matt's selection surface. **Harness requirement (§7.1): `--public-labels` render mode** — two-register naming law; any view screenshot destined for the dev log renders under it | gandalf spec → render agent | S0 lock + S1 data |
| **S4 — Mechanics waves (parallel track)** | **Wave A** summoner/proxy: gandalf ELICITOR grill of Matt (forks: summon economy — cooldown/spend/reserve/harvest; re-summon cadence; GX-19 absorption seam) → engine spec → KR sequences gamora/rocket (un-gate `_DEFERRED_PROXY_BINS`; nav behavior-branch; mid-fight re-spawn loop; AI tiers). **Ailments** parallel (session evidence in hand; shock collision #1). Then **Wave B** reservation/aura, **Wave C** trigger+mark-consume; econ/commitment design (GX-20); keystone (GX-02) | gandalf + Matt → KR → gamora/rocket | Evidence DELIVERED; sessions await Matt convening |
| **S5 — Corpus → engine roster migration** | Per §F.5: candidate pool (corpus positives + mint ×9 + founding roster) → true cell-duplication tiebreak (tier · lineage/longevity · recency, engine frame) → kits become lattice occupants (roster = occupant set over the 972 cells). **Staged by the S2 readiness census:** expressible-now kits migrate immediately; wave-gated kits migrate as A/B/C land | gandalf (tiebreak surfaces) + Matt (calls) | S2 census + S4 waves for full coverage |
| **S6 — JSON emission** | Emission realizes full kits (elements/skills/T4s/names/factions) → engine kit JSONs (`kit_space/kits/` pattern) | rocket + star-lord via KR | **§F.4 gate:** Matt-judged genre-canon coverage — no count, one-word veto standing |
| **S7 — DEMO SELECTION** | Matt browses the periodic table + kit JSONs, curates the demo roster kit-by-kit to a substantial lineup (no count) → Godot test ladder: **(1) mannequins → (2) exact battle-sim replica → (3) full demo (four areas + escapes)** | **Matt** | S6 |

---

## §4 Open Matt-gates (the decision queue, in firing order)

1. **Q19 lock word** — the ruled plane awaits formal lock (§1). One word.
2. **E4 Gate-2 → push** — 15-commit stack held; jack-ryan verdict on `785956c` per standing resume-order; PASS → push; taint → rebase plan. Unlocks the post-push hygiene wave (support retirement · rime one-worder · drax element-label follow-on · "snap"→"instant" rename Unit 2).
3. **Wave-A design forks** — rule in the ELICITOR session (economy model / cadence / GX-19 absorption).
4. **Ailment session convening** — shock naming collision resolution + damage-amp design (GX-15 folded) + freeze/stun/poison-dot tranche.
5. *(later)* **§F.4 emission judgment** and **S7 demo curation** — Matt's throughout.

## §5 Next-session start block (paste-ready order)

1. Matt: Q19 lock word (or veto) → gandalf canonizes plane rule in renderer spec + finalizes addendum STATUS.
2. Gandalf drafts + fires **elrond data-completion brief** (S1: one rebuild — roster backfill, delivery.value column, poe2 unknowns) and **legolas mint-dossier brief** (paste-ready). Seam agents, opus.
3. Gandalf fires **V7 negative-space** sub-agent (63-bucket whitespace input) + drafts the **migration-readiness census** spec (S2).
4. Convene **Wave-A ELICITOR grill** (Matt + gandalf) when Matt calls it → Wave-A engine spec → KR.
5. **Ailment session** when Matt calls it.
6. Post-S0+S1: **periodic-table harness spec** (PROMPT 5) → render agent (S3).
7. ~~Legolas Mode A — Steam-mechanics verification~~ **DONE same session** (Matt-fired; `f9dc5467`; verdicts folded into §7.2 — discovery-coupling REFUTED, prologue-deprecation tailwind CONFIRMED, Jan-2026 AI-form rewrite caught).
8. **GTM fold:** mothership + satellite plan + naming law + verification verdicts → `canonical/reap-die-rise-game/` (launch-scope home) when the game-spec pass opens. Carries the market-stage gate: multi-mode-hub grey area (support ticket or phased rollout).
9. Standing: E4 Gate-2 resolution → push; PoE1 3.29 re-harvest ~Jul 24; GX-12 hypothesis rides next element-design opening.

## §6 Operational notes carried forward

- **Seam-typed opus agents, never fable** (Matt 2026-07-13). Judgment stays banked with gandalf-prime; sub-agents operationalize made verdicts; trust-but-verify on every return (it caught drift 3-for-3 this session).
- **DB is read-only while any agent reads it**; rebuilds only in a quiet window (currently quiet).
- **Multi-writer tree:** agents `git add` only their own files; auto-commit no-push per team addendum.
- **Rulings recorded verbatim-anchored same-turn** (Q19/Q25 rows + tracker deltas); one-word veto stays open on every record.
- **DB governs; boards/views are derived** (D6). Any count in any doc must reproduce from SQL.

---

## §7 ADOPTED (Matt + gandalf concur, 2026-07-13 wind-down rider): customer-facing naming law + Steam mothership validation

Source: `matt_notes_handoff_docs/gemini-steam-mothership-research-and-kit-naming-advice-for-devlog` (Gemini research, Matt-forwarded; committed for durability). Gandalf design verdict: **ADOPT the naming scheme with refinements · TREAT the Steam research as directionally-supporting, verification owed.**

### §7.1 The chronological-taxonomy naming law (public register)

**Rule:** customer-facing surfaces (dev-log posts, Steam pages, the public periodic table) never render corpus internal names — kit_id/display_name entries like "Nova Sorceress," "Multishot Demon Hunter," "Whirlwind Barbarian" carry trademarked class names and proprietary skill names. The public register labels cells/kits by factual chronological metadata + OUR descriptive mechanical vocabulary:

> **`[game-id]-[era year] (v[stabilization patch]) + [mechanical description]`** — e.g. `D2-2001 (v1.09) Splintering Ice Radial`

**Why this costs almost nothing (the deep reason to adopt):** the mechanical-description half is exactly the engine frame we already built — plane cell address (movement × delivery × tempo) + engine-key descriptors (element/damage-mode, geometry, signature mechanic). **The rekey pass IS the trademark-laundering machine:** descriptive coordinates instead of proprietary names, produced systematically for all 463 combat kits. The naming law is a **display contract** (same class as V8's synthetic watermark), not new data work.

**Refinements (gandalf, binding on implementation):**
1. **Two-register law.** Internal register unchanged everywhere (kit_id + display_name keep provenance legibility; renaming internal vocabulary would be churn and damage our own lineage reads). Public register is DERIVED: `label_public = f(game-id, era_year, stabilization_patch, engine-key descriptors, plane cell)`. DB governs (D6); hand-polish allowed (Matt curation) but the default derives.
2. **Render modes.** Every view renderer destined for the dev log grows `--public-labels` (PROMPT 5 harness requirement, §3 S3; V1.2-class views re-render under it before any screenshot ships publicly — current rasters carry internal names and are internal-only artifacts).
3. **The description half must also be launder-clean.** No proprietary skill names inside the mechanical description ("Frozen Orb" out; "splintering ice radial" in). Engine-frame vocabulary satisfies this by construction; the rule guards hand-polish.
4. **"Legal air gap" is an overclaim — downgrade to "material risk reduction."** Factual game/year/patch citation is classic nominative-use territory and far safer than class names, but a cheap legal sanity check rides before the Steam page goes live (a market-stage Matt-gate, not a now-gate).
5. **Data feed:** `era_year` + `stabilization_patch` join the S1 elrond wave (§3). Where the patch pin is absent, the label honestly omits the segment (`D2-2001 · Splintering Ice Radial`) — never invented.

**Engagement thesis endorsed (senior-designer concur):** hardcore ARPG min-maxers remember patch eras precisely — v1.09 Hammerdin vs v1.10 synergy-era is a *lived distinction* for this audience. Presenting cells as historical data points invites veteran audit; the Cunningham's-Law pull drives exactly the community our corpus work courts, into exactly the surface (the periodic table) we're building anyway.

### §7.2 Steam mothership + satellite validation (research — supporting, verification owed)

The research supports the standing mothership + satellite plan: single premium App ID; **Standalone Demo** ("Simulation Hub") with its own store page, reviews, and community hub hosting the free mini-game satellites; Valve-native wishlist/buy overlay; demo volume feeding the mothership's discovery index; permanent pre/during/post-launch lifecycle. Mini-games = thin rule-set wrappers over battle-sim-certified kit JSONs (hero-line-wars/horde-defense ~1-2wk-class; TD/auto-chess ~3-4wk-class) — **our factory-is-the-product doctrine wearing a GTM face**; the §F.4 Godot ladder is the same harness the satellites reuse.

- **AI-compliance shape confirmed by architecture:** pre-runtime LLM emission → static JSON, zero live client calls → "Pre-generated content" disclosure box; the doc's draft statement is usable after rewording "seasonal" → "periodic pre-runtime content updates" (retired-vocabulary law). Composes with the D7 AI-tell line.
- **Lore bridge endorsed in shape:** mini-games framed in-fiction as memory re-enactments of harvested souls composes cleanly with the RDR death-faith frame and the "Keep What You Kill" hook. Specific naming ("Tactical Soul Simulations" etc.) = story-side call when the hub is specced.
- **Verification RETURNED same session (legolas Mode A, Matt-fired: `legolas/findings/2026-07-13-steam-mothership-demo-mechanics-verification.md`, commit `f9dc5467`) — 5 CONFIRMED · 3 PARTIAL · 1 REFUTED:**
  - **REFUTED (the load-bearing claim):** demo volume/reviews do NOT algorithmically elevate the mothership's discovery index; demo reviews stay on the demo page, never roll into the main score. The coupling was folklore. **The REAL levers (confirmed):** native wishlist/buy funnel on the demo page · one-shot event triggers (demo-launch wishlist email, notify-followers, New & Trending entry — spend deliberately, they don't repeat) · permanent pre/during/post-launch lifecycle · Next Fest = once per game EVER (pick the window strategically).
  - **CONFIRMED (the strategic tailwind):** Valve deprecated separate prologue App IDs in favor of demos (Aug 2024, Valve verbatim) — the platform steers everyone toward exactly our satellite pattern. Demo store page/library/reviews confirmed; free bi-weekly build updates confirmed (no per-update review). **Correction: demos get NO community hub** (Valve verbatim) — veteran argument-traffic lands on the MOTHERSHIP's hub + external channels, which is where we want it anyway.
  - **AI compliance (post-cutoff catch):** Steamworks form REWRITTEN Jan 16–17 2026 — AI-assisted CODE now explicitly out of scope (would have been in-scope 2024–25); pre-generated disclosure statement usable with the "seasonal"→"periodic" reword; **gap: AI-generated MARKETING/store-page assets also require disclosure — audit the full ship-to-Steam surface, not just the binary.**
  - **Strategy reshape (gandalf read):** the plan SURVIVES — arguably strengthens on the prologue-deprecation tailwind — but its engine changes from "algorithmic transfer" to **funnel + one-shot events + the dev log as the recurring channel** (bi-weekly mode drops can't re-fire the notify email; cadence communication rides Steam news posts + the text-first dev-log strategy — which the naming law §7.1 serves). **Market-stage gate: multi-mode hub inside one demo = Valve-review grey area** (no prohibition, no precedent surfaced) — resolve via Steamworks support ticket or phased mode rollout before the hub ships.
- **Fold targets:** GTM plan + naming law + verification verdicts → `canonical/reap-die-rise-game/` (§5 item 8); naming law display contract → views README rulings log (done this session) + PROMPT 5 spec (S3).

---

**Signed:** gandalf, 2026-07-13. The plane is ruled, the raster is loved, the pipeline to the demo is staged — and the table now knows what name to wear in public. Next session opens on the lock word.
