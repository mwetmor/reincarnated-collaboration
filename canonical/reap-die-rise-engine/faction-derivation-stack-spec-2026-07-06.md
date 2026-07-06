# Faction Derivation Stack — full-emission-first · derived factions · the two-cut library · run composition

> **STATUS:** SPEC-CURRENT v1.0 (2026-07-06) — **Matt rulings embedded (2026-07-06 session): full-emission-first pipeline order · anti-faction redefinition (vertical factions) · 18-kit run-composition model · F-B rotating factions · F-C 4 factions/run · 30–50 faction library · realm = one people · race-after.**
> **Author:** gandalf (SPEC-AUTHOR; realm-coherence synthesis as STORYWRIGHT). **Ruled by:** Matt, 2026-07-06 (verbatim quotes inline).
> **Companions:** `../reap-die-rise-story/gameplay-loop-design.md` (§5 lieutenants-are-kits, §8 becoming, §9 Goldilocks, §19 realm-peoples, §23 descent structure — the story law this spec obeys) · `../reap-die-rise-game/one-realm-mvp-scope.md` (the denominator; its §3 roster accounting is superseded by §5 below — third ruling set amended in place) · `../current-to-end-state/current-to-end-state-serial-content-emission.md` (the pipeline ledger this spec extends).
> **Supersessions:** one-realm §3 "~8–10 validated kits" accounting → **18-kit / 1-per-BC-cell roster** (§5). Doc-2 §3 G7a roster session (2026-07-03) → DEAD — the 35 flavored finalists become **pipeline fixtures/regression anchors**, not roster candidates; roster selection re-fires against the post-batch-2 full emission.
> **Gate-1:** jack-ryan DESIGN-MODE review queued (this spec + the one-realm third-ruling-set amendment ride his next pass; decisions-log registration of the 2026-07-06 ruling set batches there per standing practice).

---

## 0. What this is

The complete spec for **how factions come to exist** in *Reap. Die. Rise.* — and everything that ruling reorders: pipeline sequence, monster derivation, run composition, demo roster selection, race. One session (2026-07-06) produced all of it; this doc is the single home so the rulings stop living in chat.

The one-sentence version: **the population is emitted first; factions are discovered in it; monsters are derived from factions; the demo shops the result.** Substrate-led discipline applied at the faction layer — the same arrow that governs element names and cluster labels (math finds, LLM names, human curates; D7).

## 1. RULING — full-emission-first pipeline order

Matt (2026-07-06, verbatim): *"We need to have a complete pipeline emission with a large enough number of kits to derive factions and then anti-factions for the monsters so that we can derive the monsters. Then the Demo needs to select the best subset of the full pipeline generations which has the most interesting/unique kits with the most sensible faction coverage."*

**Order of operations (supersedes any curate-then-emit sequencing):**

1. **Full 18-cell emission** — every BC cell populated at the corpus floor (≥100 gauntlet-passed kits/cell → ~1,800-kit population). Requires the batch-2 variation build (factions **cannot be derived from reskins** — a 100×-reskin cell contributes one mechanical voice, not a population; the variation pilot gates this).
2. **Faction derivation** — population analysis discovers the faction library (§3).
3. **Monster derivation** — monsters derive **from** the faction structure (§7), not from a separate anti-faction axis.
4. **Demo selection** — the roster is the *best subset* of the full population: most interesting/unique kits + most sensible faction coverage (§6).

## 2. RULING — anti-factions redefined: the vertical faction model

Matt (verbatim): *"I think that we need to re-think what anti-factions are… Monsters must actually fit into player combatant factions because they will be supporting the lieutenants/bosses who will eventually be player controlled."*

The old anti-faction concept (opposing mechanical pole; already dropped once — engine tracker :247/:405 "v2 drops the anti-faction concept entirely") is now **positively replaced**: there is no separate monster-faction axis. A faction is a **vertical slice of a realm's society**, and monsters are its lower stratum:

| Stratum | What | Becomable? | Source |
|---|---|---|---|
| **Fodder / soldier-mass** | The faction's rank-and-file monsters — palette, silhouette, verbs all derived from the faction's mechanical profile (§7) | **NO — law** (see F3, §11) | derived from faction profile |
| **Lieutenants / champions** | Kit-grade individuals: rare, individuated, a few levels hot — the Goldilocks spread (§9) and the becoming targets (§8). *Eventually player-controlled* (Matt, above). | **YES** — these ARE kits (loop-doc §5:144) | gauntlet-passed emission, faction-member |
| **Mega-boss** | The realm holdout (§8's 401st) | launch-scope holdout | launch |

**Arrow law (III.7 preserved, now stack-wide):** mechanics → cluster → faction-name. Never faction-name → mechanics. The existing `emit_faction_block` DESIGN-INTENT GUARD (*"factions are ORGANIZING + PRESENTATION, never combat mechanical"*) survives verbatim — what changes is where clusters come from (derived, not designed; §9).

**Scarcity guard (loop-doc §5:148):** *"If everything is becomable, becoming is noise."* The vertical model is what keeps becoming scarce — fodder is faction-flavored mass, never kit-grade. The fodder/champion boundary is written as law in §11 (F3) with a strike-through invitation if Matt ever wants fodder-becoming.

## 3. RULING — the faction library: 30–50, derived, two-cut

Matt (verbatim): *"there will be no fighting the substrate as we will have a plethora of factions to select from when factions number in the 30-50 range with enumerated kits."*

**Derivation method** (Matt-accepted: *"this sounds like a much more well-tuned process for the game's needs"*):

- **Feature vectors:** ~20 mixed-type columns per kit — element pair, BC cell, role mix, chain composition, T4 strategy (26-enum), resource model, weapon family, proxy share, gear signature.
- **Distance:** weighted **Gower** (mixed categorical/numeric).
- **Clustering:** agglomerative hierarchical (Ward/average linkage — elrond consult picks).
- **Two cuts of ONE dendrogram, selected by bootstrap stability:**
  - **HIGH cut → families/peoples** (~6–12): realm-level identities. A family is a broad mechanical *culture* (e.g., "fire/earth attrition peoples").
  - **LOW cut → factions/orders** (30–50): zone-level identities. An order is a family's internal specialization — same culture, distinct dialect.
- **Family vs faction, technically:** they are **the same object at two granularities** — nested cluster memberships from one tree. A faction carries `family_id`; a family enumerates `member_factions`. No second pipeline, no second ontology.
- **Feature-weighting subtlety (consult scope):** element/T4/resource-weighted metrics produce cell-*spanning* orders (a people whose orders span melee and caster); geometry-weighted metrics produce cell refinements. The elrond consult evaluates 2–3 weightings; **the 30–50-stable-clusters target is the power criterion** — it answers N empirically (floor 100/cell; extend cells whose clusters are bootstrap-unstable).
- **NO LLM in the truth path.** Math finds the clusters; LLM names them (naming consumes faction membership — §9); Matt ratifies both cuts at the ratification gate (§9). Same discipline as Glance and the element-name pipeline.
- **Discipline #18:** elrond methodology consult is **mandatory before clustering executes** — and correctly timed per the §4.2 refinement: the consult fires AFTER the emission population exists, so methodology is chosen against real marginals, not in the dark.

## 4. RULING — realm coherence: one realm = ONE PEOPLE; no intra-realm war

Matt posed the fork (all-one-faction vs loosely-related vs opposing-factions-per-realm); the synthesis below was accepted.

- **A realm is ONE PEOPLE** — one dendrogram family. Its zones (Temple 1, Biome, Temple 2) cast the family's **distinct orders**. Mechanical coherence comes free (they're kin in feature space); variety comes from the orders' dialects.
- **NO opposing factions within a realm — story law.** §23.3's manufactured-rebellion frame requires the realm to *believe itself at peace* under the demigod's cage; an openly warring realm breaks the peace-illusion and with it the reveal (Q4's keystone cluster). Opposition the player *feels* lives at **per-lieutenant Goldilocks temperature** (§9 hot/right/cold) and **across-realm variety** (§19: *"its peoples become the season's factions"* — plural across the game, singular per realm).
- **Rival-order TENSION is allowed and wanted** — politics, precedence, doctrinal rivalry (the existing `relationships` machinery: `tension_narrative`, `shared_history_hook`, RELATIONSHIP_TYPE_ENUM). Constraint (§9): **family-internal relationships are tension-grade only, never war-grade.**
- **Fractal casting:** library (30–50) → realm casts one family → run casts 4 of its orders (§5). Same selection verb at every scale.

## 5. RULING — run composition: 3 zones · 18 kits · 4 rotating factions

Built across three Matt iterations (4-zone/20-kit proposal → *"Let's remove the second Biome, reducing to 18 total kits (3-4 kits per dungeon/temple and 2 kits per Biome)"* → *"F-B: Rotating factions per run. F-C: 4 factions."*).

**The model:**

| Zone (§23.1 verbatim order) | Champions cast | Faction role | Must-beat |
|---|---|---|---|
| **Temple 1** | 3–4 | anchor faction **A** | ≥1 (holds the lesser conduit) |
| **Biome** | 2 | support faction **C** | 0 — optional encounters (face or pass by) |
| **Temple 2** | 3–4 | anchor faction **B** | ≥1 (primary conduit → reincarnate → eruption) |
| **Escape** | 0 | fodder only (faction-derived soldier-mass) | — |

- **Roster = 18 kits = 18 BC cells, exactly 1:1.** Every mechanical voice in the engine's space is present exactly once. (Supersedes one-realm §3's ~8–10 accounting — amended in place, third ruling set.)
- **4 factions across the 18** (5/5/4/4 or similar — the derivation decides natural sizes), **rotating roles per run**: which faction anchors Temple 1, which supports the Biome, rotates run-over-run.
- **Recorded gandalf lean (open pin, §11):** asymmetric 3-at-Temple-1 / 4-at-Temple-2 → 9 kits/run = exactly half of 18 → **run 2 can be a perfect partition** — a guaranteed fully-fresh second run, which is precisely the wishlist-conversion moment (the demo proving it re-rolls). Anti-repeat casting director thereafter (Hades-class: bias against recently-seen, never hard-exclude).
- **Casting director** is a Godot-side ask — added to one-realm §6.

## 6. Demo selection — the shopping solve

The demo shops the full population for **one family whose ≥4 orders are internally distinct and jointly tile the 18 cells** at 4–6 champions per order, with **≥1 order carrying the proxy/summoner dialect** (the summoner mandate, one-realm §3). Fallback if no single family tiles cleanly: **adjacent-branch kin** — pull the nearest sibling order from the same high-cut branch (still one people to the player's eye; the dendrogram guarantees kinship is real, not asserted).

Selection criteria (Matt's words, operationalized): *most interesting/unique* = high intra-order distinctiveness + low pairwise kit similarity; *most sensible faction coverage* = the tiling property above.

## 7. Monster derivation — monsters FROM factions

Monsters are **parameterized from their faction's mechanical profile**: element palette, resource temperament, verb family, silhouette cues all inherit from the order they serve — because (Matt, §2) *they will be supporting the lieutenants/bosses*. A fire/earth attrition order fields fire/earth attrition fodder. The old 44-monsters/season standalone pool re-scopes: monster emission takes a faction handle, not a free draw.

- Fodder inherits palette + verbs at fodder magnitude; **never kit-grade, never becomable** (F3).
- The `boss_with_adds` shell (near-existing tech) is the natural lieutenant+fodder composite — the adds are the lieutenant's own order's fodder.
- Escape soldier-mass = the realm-family's fodder at density (one-realm §6.4).
- `corpus_floor_verification.py` NPC floors (`npc_min_per_faction: 20`) re-scope to the **cast realm** (the 4 cast orders + family fodder), not the whole library.

## 8. RULING — race comes AFTER family/order/faction

Matt (verbatim): *"I am suspecting after as a family may itself lean towards a race in a real way."* Confirmed — **after**, because:

- A family already has a mechanical *culture*; race is the **presentation attribute diagnosed from that lean** at the family-naming/ratification gate (§9). A family whose profile reads brutal/heavy/attrition may diagnose orcish; one reading precise/ranged/evasive may diagnose elven.
- **Never a generation input** (would violate the arrow law — race→mechanics is faction-name→mechanics wearing a costume). **Never combat math** (III.7).
- **Unmatched families are the feature, not a failure:** a family whose lean fits no stock fantasy race gets an **engine-invented race** — differentiation the derivation pays for by itself.
- Story composition: **race = form-family** in the form-library sense — reincarnation across forms means race is something the player *wears*, which is exactly what a presentation attribute is.

## 9. Emission rewiring — what actually changes in code

The scaffold **already half-exists**; this is rewiring + one new layer, not greenfield:

1. **`emit_faction_block(clusters_raw, relationships_raw)`** (`cycle14_unified_bundle_emitters.py:211`): input swap — clusters arrive from the **derived registry** (population analysis output), not designed configs. The DESIGN-INTENT GUARD and telemetry provenance (pm1_algorithm, compactness, cosine_similarity_max, pairwise_distance_distribution) survive; provenance now records the dendrogram cut parameters.
2. **Family layer added** — new block above clusters. Bundle schema sketch (v2):

```jsonc
"factions": {
  "families":  [{ "family_id": "fam_03", "name": "…", "palette": "fire/earth · attrition",
                  "creed": "…", "member_factions": ["fac_11","fac_17","fac_29"],
                  "race": "…" }],                      // §8 — diagnosed at ratification, presentation-only
  "clusters":  [{ "cluster_id": "fac_17", "family_id": "fam_03", "name": "…",
                  "mechanical_profile": { "elements": ["fire","earth"], "t4_family": "graveyard",
                                          "resource": "attrition", "cell_span": 5 },
                  "member_kits": ["…×45"], "champion_grade": ["…×6"] }],
  "relationships": [{ "between": ["fac_11","fac_17"], "type": "rivalry",
                      "tension_narrative": "…" }]      // family-internal: tension-grade only, never war (§4)
}
```

3. **Relationship constraint:** family-internal pairs restricted to tension-grade enum values (rivalry/precedence/doctrine); war-grade reserved for cross-family (launch-scope; the demo is one family).
4. **`corpus_floor_verification.py`:** Q10-era "8 or 9" factions is Q4-mutable config → **30–50 library target**; `player_min_per_faction`/`npc_min_per_faction` re-scope per §7; `UNASSIGNED_FACTION` survives as the heretic-bucket (kits no stable cluster claims — expected at low rate, surfaced at ratification). Decisions-log touch rides jack-ryan's pass.
5. **Pipeline insertion point:** population-analysis stage lands **after gauntlet certification, before LLM naming** — naming consumes faction membership (an order's kits are named in its register). **Ratification gate:** Matt rules both cuts (family count + faction count) before naming fires.

## 10. Sequencing + seams

| Step | What | Seam | State / gates-on |
|---|---|---|---|
| 1 | Variation pilot (Leg-1 ✓ landed `a49ccd4`; Leg-3 join-bug triage IN-FLIGHT) | rocket · star-lord | IN-FLIGHT — gates-on: join-key-contract-fix |
| 2 | Batch-2 variation build + full 18-cell emission (~1,800 kits @ ≥100/cell) | rocket → star-lord | OPEN — gates-on: 1 |
| 3 | elrond #18 methodology consult (weightings, linkage, stability protocol) | elrond | OPEN — gates-on: 2 |
| 4 | Clustering + two-cut derivation → faction registry | elrond (analysis) · star-lord (registry) | OPEN — gates-on: 3 |
| 5 | **Matt ratification gate** (both cuts + race diagnoses) | Matt | OPEN — gates-on: 4 |
| 6 | LLM naming/flavor in faction registers → bundle v2 (§9 schema) | star-lord | OPEN — gates-on: 5 |
| 7 | Demo shopping pass (§6) + G7a-successor roster pick | gandalf shortlist → Matt picks | OPEN — gates-on: 6 |
| 8 | Casting director (rotation + anti-repeat) | drax (Godot; one-realm §6) | OPEN — gates-on: 7 |

## 11. Open-items register (named, not silently pending)

| # | Item | Shape | Gate |
|---|---|---|---|
| F1 | **3/4 asymmetry pin** — Temple 1 = 3 vs Temple 2 = 4 (gandalf lean: yes → 9/run → perfect-partition run 2) | Matt pin, one line | before casting director spec (step 8) |
| F2 | **N empirical vs veto** — 100/cell floor with extend-unstable-cells rule; Matt may veto cost at the consult return | consult output | step 3 return |
| F3 | **Fodder-boundary LAW (written, strike-through invited):** *fodder is faction-derived monster mass and is NEVER becomable; becoming targets are kit-grade lieutenants/champions only.* Guards §5:148 scarcity. If Matt ever wants fodder-becoming, strike this row with a ruling — never drift into it. | law | standing |
| F4 | **Flavor-references-faction** — does kit flavortext name its order? (Lean: yes at naming time — cheap coherence; D7 curation catches overreach.) | Matt pin | step 6 |
| F5 | **Faction persistence across emissions** — when batch-3+ lands, does the library re-derive (drift) or assign-to-existing (stability)? (Lean: assign-to-existing with periodic re-derivation at Matt's call — players learn faction identities; churning them costs recognition.) | design decision | before any batch-3 |

---

**Signed:** gandalf, 2026-07-06 (SPEC-AUTHOR). The population votes, the tree is cut twice, the realm is one people, and the demo shops the result. Anchors: Matt rulings 2026-07-06 (verbatim inline) · loop-doc §5/§8/§9/§19/§23 · one-realm third ruling set (same-day amendment) · serial-emission ledger PART C.
