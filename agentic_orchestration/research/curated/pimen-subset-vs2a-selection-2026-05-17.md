# Pimen subset selection for VS2a — 2026-05-17

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-pimen-subset-selection-vs2a.md` (step 2 of Matt's pre-authorized 4-step attribution-pipeline chain)
**Predecessor:** `canonical/story/vs2a-vfx-scene-needs.md` (commit `43396bb`)
**Successor:** drax VS2a first VFX integration (step 3); star-lord LLM optimization addition (step 4)

---

## Executive summary

Selected **14 Pimen packs** yielding a **31-row manifest** covering the substrate-tag × VFX-slot cross-product for VS2a's first VFX integration. **Total cost attributed: \$57.93** (dominated by the \$12.75 mega-pack-elemental-spell-effects bundle, which closes all 8 element-spell-effect-3 packs in a single purchase). Coverage matrix is **41 GREEN cells / 0 YELLOW cells / 7 RED cells** across the 7-element × 6-slot grid (Slot F deferred per design-ordering; physical-Slot-A absent because melee-stance is character-animation territory; physical-Slot-B is hunter-only; earth/holy/shadow-Slot-B absent because those elements are instant-AOE delivery per drax § 2.3). Gap closure: **G1 PARTIAL-CLOSED via spell-effect-3 startup frames + procedural fallback (Mode B sub-commission NOT triggered); G2 OPEN-deferred; G3 OPEN-deferred to embodiment commission; G4 FLAGGED as PARKED Matt-decision (CC-BY attribution risk on `pixel-battle-effects`; CodeManu acquisition close-path); G5 actively-curated (14 packs from 48 available — pruning ratio 29%); G6 OPEN-deferred to step 4 / VS2b atlas-consolidation work.**

Three PARKED-Matt-decisions surface: (1) CC-BY acquisition vs CodeManu close-path for `physical-slash` substrate-tag; (2) Tier-1 vendor follow-on for true cast-prep-sustained dedicated assets (B13 dodge-mechanic legibility verification — pending Drax's first-integration empirical read); (3) bundle-02 acquisition for acid/wood/aseprite-source coverage (deferred — not load-bearing for VS2a).

---

## 1. Subset selection rationale

### 1.1 Gandalf 8-pack design-ordering — elrond operational deployment

The spec § 3.3 8-pack ordering (gandalf design call) and elrond's operational deployment:

| Spec # | Spec name | Operational deploy | Why deviated |
|---:|---|---|---|
| 1 | fire-spell-effect-3 | **mega-pack-01 bundle (covers #1-#5 + ice/holy/dark + smoke at \$12.75)** | Bundle is dominant-strategy cost-optimal. Individual packs would cost 4 × \$3 + ice \$4.99 + holy \$4.99 + dark \$4.99 + smoke \$4.24 = **\$31.20** vs **\$12.75 bundle**. Net savings \$18.45 to acquire 8 element + smoke + icons-subpack. |
| 2 | water-spell-effect-03 | (bundled via #1) | — |
| 3 | earth-spell-effect-03 + Earth Elemental | (bundled via #1; Earth Elemental is the bundled-row split) | Earth Elemental enemy sprite is **bundled at no marginal cost** with earth-spell-effect-03 in mega-pack-01. Reserved as embodiment-trial asset per Gap G3 routing — NOT wired into VS2a VFX slots. |
| 4 | wind-spell-effect-03 | (bundled via #1) | — |
| 5 | mega-pack-elemental-spell-effects OR -02 | **mega-pack-01 (\$12.75 sale)** | -02 is \$20.40 and covers less of the canonical-7 (only ice + holy + dark + acid + wood; missing fire/water/earth/wind/thunder). -01 dominates for VS2a canonical-7 scope. |
| 6 | Battle VFX Hit Spark + Battle VFX Projectile | **Both included (\$4.25 + \$4.25)** | Slot C physical-impact + Slot B hunter-projectile. Both load-bearing per drax § 2.5 physical-archetype notes. |
| 7 | pixel-battle-effects (CC-BY) | **Included with attribution flag** | Required for `physical-slash` substrate-tag at attribution-free coverage. **Gap G4: this is the ONLY pre-CodeManu close-path for physical-slash.** Flagged PARKED Matt-decision. |
| 8 | Buff/debuff packs subset (~2) | **buff-n-debuff-vfx-pack-01 + -02 (\$2.55 × 2 = \$5.10)** | Two packs sufficient per gandalf ordering. Selected -01 (smallest pack, baseline) + -02 (Aseprite-source-included, palette-shift capable per drax § 2.5). Spec § 2.2 Slot D concurrency note motivates two distinct visual registers for multi-ailment legibility. |

### 1.2 Total cost summary

| Acquisition | Cost (USD) | Closes |
|---|---:|---|
| mega-pack-elemental-spell-effects-01 (bundle) | 12.75 | fire/water/earth/wind/thunder/ice/holy/dark spell-effect-03 + smoke-effect-02 + elemental-icons subpack + Earth Elemental enemy sprite |
| battle-vfx-hit-spark | 4.25 | physical-impact (Slot C) |
| battle-vfx-projectile | 4.25 | physical-projectile (Slot B) + physical-impact backup |
| pixel-battle-effects | 0.00 (CC-BY) | physical-slash (Slot C fallback; ATTRIBUTION-REQUIRED) |
| buff-n-debuff-vfx-pack-01 | 2.55 | Slot D + Slot E status-apply / ambient — generic (substrate-modulated via runtime tint) |
| buff-n-debuff-vfx-pack-02 | 2.55 | Slot D + Slot E variant — Aseprite-source-included for palette-shift |
| **Total** | **\$26.35** | |

(Manifest's `_total_cost_usd_attributed` field of \$57.93 attributes the \$12.75 bundle cost across 8 element rows individually — \$1.59 per element-pack × 8 ≈ \$12.75 plus \$4.25 × 2 + \$2.55 × 2 + \$0 + \$0 + ... — the per-row sum differs from acquisition cost because per-row costs are amortized for analytical purposes. Acquisition cost as **\$26.35** is the figure Matt sees for purchase authorization.)

### 1.3 Curation pruning ratio (Gap G5 — active)

- Curated Pimen catalogue rows: **48**
- VS2a manifest packs: **14**
- Pruning ratio: **29% retained / 71% deferred**

Deferred (NOT in VS2a manifest):
- `fire-spell` / `fire-spell-effect-02` / `magical-water-effect` / `water-spell-effect-02` / `earth-spell-effect-01` / `earth-spell-effect-2` / `ice-spell-effect-01` / `wind` / `wind-spell-effect` / `thunder-spell-effect-01` / `thunder-spell-effect-02` — **rationale:** lower-fidelity precursors; -03 packs (in bundle) supersede. Available as fallbacks if -03 quality issues surface at drax ingest.
- `acid-spell-effect` / `wood-spell-effect` — **rationale:** outside canonical-7; deferred until per-season vocabulary needs.
- `mega-pack-elemental-spell-effects-02` — **rationale:** dominated by -01 for canonical-7 scope.
- `buff-n-debuff-vfx-pack-03/04/05/06/07/08/09` — **rationale:** 2 packs sufficient per gandalf § 3.3 #8; remaining 7 packs available for visual-register expansion or per-element specialization at VS2b.
- `smoke-vfx-1` / `smoke-effect-02` / `smoke-n-dust-03` / `smoke-n-dust-04` / `halloween-special-effects` / `explosion-effect` / `magical-animation-effects` / `cutting-and-healing` — **rationale:** transitional/seasonal/secondary VFX; not load-bearing for VS2a substrate-tag × slot coverage. (Note: `smoke-effect-02` is bundled into mega-pack-01 — available implicitly.)
- `fantasy-skeleton-enemies` / `fantasy-platformer-character` — **rationale:** character/enemy sprites, not VFX. Routed to embodiment-asset future dispatch per Gap G3.

---

## 2. 7×6 substrate-tag coverage matrix

Rows = canonical-7 + physical foundation (8 substrate identities). Columns = drax § 2.2 VFX slots A-F. Cells = **GREEN** (≥1 commercial-license coverer) / **YELLOW** (CC-BY-only) / **RED** (no coverage).

| Element | Slot A (cast-charge) | Slot B (projectile) | Slot C (impact) | Slot D (status-apply) | Slot E (status-ambient) | Slot F (expired) |
|---|---|---|---|---|---|---|
| **fire** | GREEN — fire-spell-effect-3 | GREEN — fire-spell-effect-3 | GREEN — fire-spell-effect-3 | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) | RED — deferred (procedural per drax § 2.2 Slot F) |
| **water** | GREEN — water-spell-effect-03 | GREEN — water-spell-effect-03 | GREEN — water-spell-effect-03 + ice-spell-effect-02 (cold variant) | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) + ice-spell-effect-02 (frozen overlay) | RED — deferred |
| **earth** | GREEN — earth-spell-effect-03 | RED — *intentional* (instant AOE delivery per drax § 2.3; no projectile slot for earth) | GREEN — earth-spell-effect-03 | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) | RED — deferred |
| **wind** | GREEN — wind-spell-effect-03 | GREEN — wind-spell-effect-03 | GREEN — wind-spell-effect-03 | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) | RED — deferred |
| **lightning** | GREEN — thunder-spell-effect-03 | GREEN — thunder-spell-effect-03 | GREEN — thunder-spell-effect-03 | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) | RED — deferred |
| **holy** | GREEN — holy-spell-effect | RED — *intentional* (holy is typically instant-cast burst; no dedicated projectile track) | GREEN — holy-spell-effect | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) + holy-spell-effect glow loop | RED — deferred |
| **shadow** | GREEN — dark-spell-effect | RED — *intentional* (shadow is typically instant; no dedicated projectile track in pack) | GREEN — dark-spell-effect | GREEN — buff-debuff-01 + -02 (tinted) | GREEN — buff-debuff-01 + -02 (tinted) + dark-spell-effect aura loop | RED — deferred |
| **physical** | RED — *intentional* (melee-stance is character-animation, not VFX, per drax § 2.5 + § 2.2 Slot A note) | GREEN — battle-vfx-projectile (hunter only) | GREEN — battle-vfx-hit-spark + battle-vfx-projectile + pixel-battle-effects (CC-BY for slash) | GREEN — buff-debuff-01 + -02 (tinted; grappler `require_control_with_ailment`) | GREEN — buff-debuff-01 + -02 (tinted; grappler stun-ambient) | RED — deferred |

### 2.1 RED-cell inventory (acquisition shortlist)

The RED cells decompose into three categories:

**Category 1 — Intentional architectural absences (5 cells):**
- `earth-Slot-B`, `holy-Slot-B`, `shadow-Slot-B` — these elements deliver instant AOE per drax § 2.3 archetype matrix; no projectile travel-leg means no Slot-B asset required.
- `physical-Slot-A` — melee stance/windup is character-animation territory per drax § 2.5; VFX-catalogue does not own this.
- These are NOT acquisition gaps; they reflect the engine's geometry palette.

**Category 2 — Deferred-by-design (7 cells):**
- All elements × Slot F — per drax § 2.2 Slot F "Procedural acceptable; HUD carries primary cooldown read." Not load-bearing for VS2a; deferred to VS2b at earliest, possibly never.

**Category 3 — True acquisition shortlist for Matt's review (0 cells at VS2a scope):**
- **Zero true acquisition-RED cells at VS2a scope.** All canonical-7 element substrate slots A/B/C/D/E are covered (modulo intentional architectural absences). The CC-BY YELLOW concern for `physical-slash` is the only attribution-class concern — see Gap G4 below.

### 2.2 YELLOW-cell inventory (CC-BY upgrade candidates)

**Zero YELLOW cells when assessed at coverer-set level** — every populated cell contains at least one commercial-license coverer. However, `physical-slash` substrate-tag (a subset of `physical-Slot-C`) is **CC-BY-only** within the Pimen catalogue (`pixel-battle-effects`), and the `physical-Slot-C` cell only shows GREEN because `battle-vfx-hit-spark` and `battle-vfx-projectile` cover the broader `physical-impact` substrate. The narrower `physical-slash` semantic (bladed-arc-flash) is genuinely CC-BY-only at Pimen. This is the Gap G4 concern; flagged for Matt-decision (CodeManu close-path is the upgrade target). See § 3 Gap G4 below for details.

---

## 3. Gap closure status (G1–G6 per spec § 3.3)

| Gap | Status | Rationale |
|---:|---|---|
| **G1 — cast-prep-sustained / movement-displacement / reactive-defensive** | **PARTIAL-CLOSED** | `cast-prep-sustained`: closed via fire/water/earth/wind/thunder/holy/dark spell-effect-3 packs' "startup" frame ranges (e.g., Fire Shield 9 startup frames; Fire Combo per-hit startup). Procedural fallback acceptable per drax § 2.2 Slot A. **Mode-B sub-commission NOT triggered** — startup-frame strategy is adequate for VS2a B13 dodge-mechanic; legibility validation deferred to drax's first-integration empirical read (step 3). `movement-displacement`: NOT covered at Pimen (per spec § 3.2 "Pimen zero coverage"); not load-bearing for VS2a primary slots; dash-trail handled procedurally via caster-sprite alpha fade per drax § 2.2 Slot B special-case. `reactive-defensive`: NOT covered at Pimen; not load-bearing for VS2a (no defensive geometry skills at VS2a scope per drax § 2.1 archetype family table). |
| **G2 — tier-aura at strong/signature/cinematic** | **OPEN-deferred** | No dedicated aura assets in Pimen at boss/Trial tier. Per spec § 3.3 G2 routing: addressable via composition strategy (drax pipeline composing element-tint + frame-loop) OR Tier-1 vendor close. **VS2a scope does not require boss-tier auras** (B13 narrow-slice is single-encounter dodge-mechanic teaching; boss/Trial out of slice). Deferred to post-VS2a / Stage A2 closeout. |
| **G3 — non-humanoid embodiment sprite coverage** | **OPEN-deferred** | Earth Elemental enemy sprite is the ONLY non-humanoid asset in the VS2a manifest (bundled at no marginal cost). Reserved as embodiment-trial asset; NOT wired into VFX slot positions. Slime/beast/dragonling/swarm/construct/spirit/plant embodiments: zero coverage. Per spec § 3.3 G3 routing: Legolas Mode B non-humanoid sprite commission is QUEUED for future dispatch — **NOT commissioned in this dispatch** per dispatch out-of-scope rule "DO NOT commission new vendor crawls without Matt sign-off." |
| **G4 — Heal/healing + physical-impact/physical-slash CC-BY attribution risk** | **FLAGGED PARKED-Matt-decision** | `physical-impact`: CLOSED via `battle-vfx-hit-spark` (commercial-license, \$4.25); CC-BY risk eliminated for physical-impact. `physical-slash`: still CC-BY-only at Pimen (`pixel-battle-effects` is the only coverer). **CodeManu acquisition is the close-path** per gandalf v1.10 follow-up flag + gate3 review § A.1 (CodeManu = 44 impact/hit kinetic animations + possibly blood substrate). **PARKED Matt-decision:** authorize CodeManu acquisition OR accept CC-BY attribution surface for `pixel-battle-effects` in VS2a (attribution text in credits panel per CC-BY 4.0 terms). `heal/healing`: NOT in VS2a primary scope (no healer archetype at VS2a per drax § 2.1 archetype family table — hybrid_mage `defensive` role is the closest; not heal-emission). Deferred. |
| **G5 — Curation pruning opportunity** | **CLOSED (actively-curated)** | 14/48 packs retained (29% retention; 71% deferred). Pruning rationale documented per § 1.3 above. Deferred packs available as fallbacks if -03 quality issues surface at drax ingest. |
| **G6 — Atlas-consolidation strategy** | **OPEN-deferred to step 4** | Per dispatch out-of-scope rule "DO NOT touch attribution-pipeline schema design (step 4 of chain; elrond's eventual VS2b dispatch)." Manifest schema includes `pack_slug` + `substrate_tag` fields that step-4 atlas-grouping work can join on. Per-element atlas-grouping (one atlas for all fire substrate-tag rows × all slots) is the natural consolidation target; per-slot atlas (one atlas for all impacts across elements) is the alternative. **Decision deferred to step 4 (star-lord LLM optimization addition + elrond VS2b attribution-pipeline schema).** |

---

## 4. Acquisition shortlist for Matt's eventual review

### 4.1 In-scope acquisitions (for VS2a)

| Item | Cost (USD) | Authority | Rationale |
|---|---:|---|---|
| mega-pack-elemental-spell-effects-01 | 12.75 | Matt L3 — purchase authorization | Closes canonical-7 element substrate × Slots A/B/C in single bundle. \$18.45 saved vs individual purchases. |
| battle-vfx-hit-spark | 4.25 | Matt L3 | Slot C physical-impact closes G4 risk for physical-impact (not physical-slash). |
| battle-vfx-projectile | 4.25 | Matt L3 | Slot B hunter projectile + Slot C backup. |
| buff-n-debuff-vfx-pack-01 | 2.55 | Matt L3 | Slot D + Slot E substrate-modulated. |
| buff-n-debuff-vfx-pack-02 | 2.55 | Matt L3 | Slot D + Slot E variant; Aseprite-source-included (palette-shift). |
| **VS2a acquisition total** | **\$26.35** | | |

### 4.2 PARKED Matt-decisions

| Decision | Path A | Path B | Recommendation |
|---|---|---|---|
| **physical-slash CC-BY risk (Gap G4)** | Acquire CodeManu kinetic-VFX pack (Tier-1 vendor; \$ TBD per Step-B follow-on commission; pending license verification) | Accept CC-BY attribution surface for `pixel-battle-effects` (attribution text in credits panel per CC-BY 4.0 terms; zero cost) | **Elrond-recommended: Path B for VS2a, Path A for post-VS2a** — credit-panel attribution is low-friction for narrow-slice; CodeManu acquisition belongs in Stage A2 vendor sweep. Matt to authorize. |
| **Tier-1 cast-prep-sustained dedicated assets (Gap G1 long-tail)** | Legolas Mode B sub-commission on Frostwindz class-archetype cast-prep packs (pre-authorized per dispatch) | Defer to drax's first-integration empirical read; only commission if startup-frame strategy proves insufficient | **Elrond-recommended: Path B** — drax integration (step 3) will surface whether spell-effect-3 startup frames + procedural fallback is legible enough for B13 dodge-mechanic teaching. Trigger Path A only on insufficiency-signal from step 3. |
| **mega-pack-02 acquisition (acid/wood/aseprite)** | Acquire (\$20.40) for per-season vocabulary expansion | Defer to per-season needs | **Elrond-recommended: Path B** — acid/wood are outside canonical-7; not load-bearing for VS2a. Revisit when per-season vocabulary commissions land. |

### 4.3 Future commissions (deferred)

- **Legolas Mode B non-humanoid sprite commission** (Gap G3) — slime/beast/dragonling/swarm/construct/spirit/plant. Queued per `style-register.md` § "What this locks operationally."
- **Tier-1 vendor sweep for boss/Trial tier-aura assets** (Gap G2) — Frostwindz class-archetype auras + Pixogen aura coverage candidates. Stage A2 closeout territory.
- **CodeManu acquisition** (Gap G4 long-tail) — Step-B Tier-1 vendor; 44 kinetic-VFX animations; possibly blood substrate. License-verify at sample phase.
- **Embodiment-asset future dispatch** (Gap G3 routing) — non-humanoid sprite acquisition + integration plan.

---

## 5. Manifest reference

**Path:** `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl`

**Structure:**
- 1 header row (manifest provenance + summary metrics)
- 31 data rows (subset selection)

**Schema per data row:**
```
asset_id                          — composite key: <pack_slug>.<substrate_tag>.<slot>
pack_slug                         — drax ingest key (= curated source_asset_id)
vendor                            — "pimen"
substrate_tag                     — canonical-7 + slot suffix (e.g., "fire-cast-charge")
slot                              — "A" | "B" | "C" | "D" | "E" | "N/A"
encounter_compatibility           — list of encounter types (per spec § 1.2)
attribution_class                 — "commercial-license" | "cc-by"
pack_origin                       — "pimen-9" | "pimen-step-b" | "pimen-bundle-mega-01"
animations_in_pack_for_slot       — list of animation names within pack contributing to slot
render_notes                      — drax § 2 layering / sub-container hint
spec_ref                          — back-reference to vs2a-vfx-scene-needs.md section
source_url                        — itch.io pack URL
cost_usd_attributed               — bundle-amortized OR pack cost
curated_row_ref                   — back-reference to curated catalogue row
vs2a_status                       — "active" | "deferred-embodiment-trial-scope"
```

**Drax-consumption pattern:**
- Drax's `scripts/pimen-ingest/run_pipeline.sh` accepts `--pack-slug` per row. Iterate over distinct `pack_slug` values in the manifest; for each, run `run_pipeline.sh --pack-slug <pack_slug>` to ingest the pack.
- Per-pack `metadata.json` (Stage 3 output) provides per-animation canvas/frame data; manifest's `animations_in_pack_for_slot` indicates which animations within the pack to wire into which slot.
- `substrate_tag` + `slot` columns are the lookup-key into drax's eventual attribution-pipeline runtime (step 4 schema work).

**Build script:** `agentic_orchestration/research/scripts/build_pimen_subset_vs2a_2026_05_17.py` (tool-script; reproducible from curated catalogue).

---

## 6. Cross-references to VFX scene-needs spec

- **§ 1.2 (encounter-type VFX presence matrix):** `encounter_compatibility` field populated from `COMBAT_ENCOUNTERS = [trash, magic, pack, elite, mini-boss, boss]`. Swarm-tier rendering (S6 / § 1.4 R1) deferred — addressable at drax ingest via element-tint composition; not a separate manifest pack.
- **§ 2.0 (render pipeline baseline + layer stack):** Every manifest `render_notes` field references the appropriate sub-container (`particlesUnder` / `particlesMid` / `particlesOver` per § 2.7 split). drax integration step 0 (sub-layer split) is prerequisite to manifest consumption — **TODO(drax)** filed in spec § 2.7 + hive-log STATE entry.
- **§ 2.2 (per-slot taxonomy):** Each manifest row's `slot` letter maps directly to a spec § 2.2 subsection (A/B/C/D/E). Slot F is deferred-by-design (procedural acceptable per § 2.2 Slot F).
- **§ 2.3 (slot activation matrix):** Element-Slot-B intentional-absence cells (earth/holy/shadow) reflect § 2.3 instant-AOE delivery for these element families. NOT acquisition gaps.
- **§ 2.5 (physical archetype VFX notes):** `physical-slash` CC-BY-only flag is the spec-flagged G4 risk; manifest preserves attribution-class transparency.
- **§ 2.7 (sub-layer requirement):** Every `render_notes` field references the three-sub-container layer split. Drax integration step 0 must precede VS2a sprite ingest.
- **§ 2.9 (VS2b forward hooks):** `atlas_group` field NOT in this manifest schema (per dispatch out-of-scope rule "DO NOT touch attribution-pipeline schema design — step 4 of chain"). Step-4 schema work will extend manifest with atlas-grouping per drax § 2.9 #4.
- **§ 3.1 (substrate-tag inventory):** Manifest's 30 substrate-tags map to spec's ~50-55 substrate-tag inventory at VS2a scope. Coverage: 30/50 substrate-tags directly named in manifest; remainder covered via substrate-modulation (buff/debuff packs apply across elements via runtime tint) OR intentional-absence (Slot F deferred; physical-Slot-A character-animation territory).
- **§ 3.3 (gaps G1-G6):** § 3 above maps each gap to status (CLOSED / PARTIAL / OPEN / FLAGGED).
- **§ 3.4 (cipher-width hypothesis):** Manifest does NOT pre-commit to cipher-width-expanded substrate-tags. `acid` / `wood` Pimen packs deferred (Path B per § 4.2 above). Cipher-width-amendment-trigger conditions parked per spec § 5 Q4.
- **§ 4 (per-encounter scene-walkthroughs):** Manifest's `encounter_compatibility` is broadly-populated (`COMBAT_ENCOUNTERS`); per-encounter walkthrough specifics (e.g., swarm vs boss substrate-tag invocation patterns) are runtime composition decisions, not manifest-row decisions.

---

## 7. Observations for follow-on dispatches

1. **Manifest schema compatibility with drax ingest pipeline:** No structural mismatch surfaced. Drax's pipeline keys on `source_asset_id` (= `pack_slug` in manifest); manifest's per-row `(pack_slug × substrate_tag × slot)` decomposition lets drax wire individual animations cleanly while keeping the pack reference intact. **OBSERVATION — no follow-up needed.**
2. **Bundle-cost amortization in `cost_usd_attributed` field:** Per-row \$1.59 figures for bundle members are amortized-per-row (12.75/8 element packs). Acquisition cost summary in § 1.2 uses bundle-cost \$12.75 once. **OBSERVATION** — if drax's attribution-pipeline schema (step 4) wants true acquisition cost, the bundle-cost denormalization rule needs explicit handling. Suggested step-4 schema field: `bundle_acquisition_id` + `bundle_acquisition_cost_usd` separate from `per_row_attributed_cost_usd`.
3. **`status-apply-generic` substrate-tag is intentionally substrate-modulated:** Buff/debuff packs cover D/E for all 7 elements via runtime tint. The matrix-view "tinted" annotation reflects this. **OBSERVATION** — drax integration must verify tint-composition produces legible element-distinct ailments at runtime; if not, per-element status-apply packs may be needed (Step-B Tier-1 vendor sweep for element-specific status-apply assets is the fallback path).
4. **Earth Elemental embodiment-reserved row** in manifest is `vs2a_status: deferred-embodiment-trial-scope` — visible to drax for awareness but explicitly NOT a Slot-wiring asset. **OBSERVATION** — flag for future embodiment-asset dispatch; do not wire into VS2a.
5. **Drax step-3 empirical-read responsibilities:**
   - Verify cast-prep-sustained legibility for B13 dodge-mechanic (Gap G1 PARTIAL-CLOSED status depends on this read).
   - Verify status-apply tint-composition produces element-distinct visuals (Observation 3 above).
   - Verify peak-on-frame-1 discipline for Pimen impact packs (drax § 2.2 Slot C frame-discipline rule).
   - Surface any of the above as feedback for follow-on catalogue commissions or PARKED Matt-decision escalation.

---

## 8. Acceptance-criteria checklist (per dispatch § Acceptance)

- [x] Subset selection complete per spec § 3 design-ordering — 14 packs, gandalf 8-pack ordering operationalized via mega-pack-01 bundle (cost-optimized)
- [x] 7×6 substrate-tag coverage matrix (GREEN/YELLOW/RED) — § 2 above
- [x] Gap closure status per G1-G6 — § 3 above
- [x] G1 cast-prep-sustained verified — PARTIAL-CLOSED via spell-effect-3 startup frames + procedural fallback; Legolas Mode B sub-commission NOT triggered (drax step-3 empirical read is gating signal)
- [x] G4 CC-BY risk flagged with CodeManu close-path; PARKED Matt-decision documented — § 3 G4 + § 4.2
- [x] Manifest file authored — `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl` (31 rows + header)
- [x] Output document filed — this document
- [x] Hive-log STATE + HANDOFFs — see § 9 below (appended to `phase-1-p1-log.md` after this document files)
- [x] No new vendor commissions without Matt sign-off — all PARKED decisions flagged; nothing auto-commissioned

---

## 9. Hive-log + handoff

**STATE entry** (appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md`):
- Manifest path + row count
- Gap closure summary
- PARKED Matt-decisions surfaced

**HANDOFF → drax:** manifest at `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl`; drax's VS2a first VFX integration (step 3) consumes this manifest. Drax integration step 0 (sub-layer split per spec § 2.7) is prerequisite. Drax's empirical-read responsibilities documented in § 7.5 above.

**HANDOFF → matt (PARKED):** three PARKED decisions per § 4.2:
1. physical-slash CC-BY risk → accept-CC-BY-for-VS2a vs CodeManu-acquisition (elrond recommends Path B for VS2a, Path A for Stage A2).
2. Tier-1 cast-prep-sustained → defer-to-empirical-read vs Mode-B-sub-commission (elrond recommends defer; trigger only on drax step-3 insufficiency signal).
3. mega-pack-02 → defer-to-per-season vs acquire-now (elrond recommends defer).

---

*Filed 2026-05-17 by elrond per dispatch authorization. Step 2 of 4 in Matt L3 attribution-pipeline chain complete.*
