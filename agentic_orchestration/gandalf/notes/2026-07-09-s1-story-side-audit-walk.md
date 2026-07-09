# S1 Story-Side Audit Walk — Identity-Layer Findings

**Author:** gandalf (DRIFT-CRITIC, survey-mode). **Date:** 2026-07-09.
**Commission:** full-run pivot item (d), 2026-07-08 — story-side trivialization audit. Acceptance test gained 2026-07-08 (4): **Matt's necromancer pair** — *"bone spear necromancer, human, necronomical order"* vs *"dark matter soul laser necromancer, space orc, necromonger order"* — must differentiate at demo-pick consumption.
**Method:** (a) what the story spec DECLARES about the identity layers, line-cited; (b) what the engine actually consumes/emits, file:line-verified (engine half via Explore sweep, 25 tool-uses, source-verified); (c) gaps classified FLIP / FLAG / KEEP / net-new-BUILD per OP § 3.7(a). Findings accrue as ledger rows — never invented.
**Feeds:** surface-ledger rows S1 (updated) + **S2 / S3 / S4 (born ⚖)**; E10 Leg 3 (shared bestiary-wells dependency, confirmed both-sided).

---

## 0. Headline verdict

**The acceptance test fails 2 of 3 identity dimensions today.** Of Matt's necromancer pair:

| Pair dimension | Carrier | Engine state | Differentiates at demo-pick? |
|---|---|---|---|
| bone spear vs soul laser (build) | skill geometry + naming | LIVE (E1 `bfc94eb`; WS1A.4-lite + Phase-5 skill naming) | **YES** |
| weapon-substrate identity (culture/period/register/lineage) | `main_weapon` export fields | LIVE end-to-end | **YES** |
| human vs space orc (race) | — | **DEAD — zero fields anywhere** | **NO** |
| necronomical vs necromonger order (faction/order) | Phase-5 faction machinery | derivation LIVE, **consumption ZERO** (v1 `faction_visibility=invisible` → labels null at export) | **NO** |

The two failing dimensions are exactly the wells E10 Leg 3 needs mob-side (Fork 2(c): one identity architecture, two consumers). The story-side trivialization is real, it is localized, and it is buildable — no spec rewrite needed.

## 1. What the story spec declares (line-cited)

1. **`gameplay-loop-design.md` §19:** race/culture/period are *"substrate inputs to generation, not cosmetic wrappers"*; *"the bone-spear-necromancer is findable across seasons"* — Matt's acceptance example is literal spec text.
2. **§11a bestiary-as-pillar:** internal taxonomy [OPEN/FRAGILE] — archetype families, faction sets, element groups, rarity tiers. Four bestiary jobs; record of conquest.
3. **Line 158:** factions are per-floor; **line 144:** lieutenants = faction floor bosses = **becomable kits**.
4. **§12 spawn-influence:** PURSUE / BIAS / DISCOVER — the player steers toward identity groups; groups must therefore be *visible*.
5. **`agnostic-loot-engine-spec.md` line 70 (provenance law):** *"kits vote BARE in the faction derivation — loot never contaminates the derivation population."*
6. **`story-expansion.md` §2 [DECISION]:** *"You are one of thousands in a large order/cult"* — **THE order** is the player's own institution (singular, definite-article, worldbuilding). §10: a hidden inner order steers it. §14: the vessel is *"the soul-clay / corpse-vessel the order shapes."*
7. **Register disambiguation (recorded):** `style-register.md` = VISUAL register (A-lock, Synty/Godot). The identity-layer register = substrate weapon-binding register (4-enum). Two different locks; no conflict.

## 2. What the engine consumes/emits (file:line-verified)

| Well | Engine state | Evidence |
|---|---|---|
| cultural_lineage | **LIVE** — kit-gen input + emitted + export | `substrate_weapon_binding.py:339-343` → `ExportWeaponDescriptor.lineage` (`export/schemas.py:239`) |
| period | **LIVE** | same chain → `.period` (`schemas.py:240`) |
| register (substrate 4-enum) | **LIVE** | `bc_target_player_class.py:197` → `.cultural_register` (`schemas.py:239`) |
| named-bearer lineage | **LIVE** | `substrate_weapon_binding.py:343` |
| faction — derivation | **LIVE (Phase 5)** — PM-1 multimodal clustering (modal cultural_lineage/tech/tone/element) + PM-2 LLM labels | `phase5_pm1_multimodal_clustering.py:26,101,118,1005-1043`; `phase5_orchestrator.py:69-97` |
| faction — consumption | **ZERO** — v1 `faction_visibility=invisible`; `faction_label_canonical` null at export | `export/schemas.py:588-731` |
| race | **DEAD** — no field, no stub, engine-wide | Explore sweep, exhaustive |
| order (kit-identity sense) | **DEAD** | Explore sweep |
| family (kit/bestiary identity) | **DEAD** — `family_id` exists only as canonical-token scaffolding, not identity | `emit_substrate_registry.py:273+` |
| monster identity | archetype + element + tier ONLY — no race/family/order/faction | `monster_generator.py:393-462` (re-confirms E10 Leg 2 finding) |
| naming machinery | multi-stage LLM: Wave A faction labels (fires only if visible), Wave B kit names, WS1A.4-lite + per-node skill names/flavor | `phase5_orchestrator.py:1600+`; `ws1a4_lite_flavor_judgment.py:560-650`; `phase5_skill_naming.py:123+` |
| kit flavor coverage | **35/~700** — Beat B glyph flavor covers the finalists shortlist only; others null | `w3_batch1_flavor_writer.py` |

## 3. Findings, classified (OP § 3.7a)

### F1 — Race well: net-new-BUILD, and the build has a natural home → **row S2 (⚖)**

Spec declares race a substrate input (§19); Matt's pair requires it; engine carries zero. The design question is *what substrate feeds race* — weapons give culture/period/register naturally, but nothing gives human-vs-space-orc.

**Lean — the vessel's race = bestiary provenance.** The player has no race; the **VESSEL** does — and vessels come from the reaped (`story-expansion.md` §14: the corpse-vessel the order shapes; loop-doc line 144: lieutenants are *becomable*). Race becomes a **bestiary well** consumed by both mobs (E10 affix affinity profiles) and kits (vessel provenance at generation) — the same one-architecture-two-consumers move Matt ratified as Fork 2(c). The bone-spear human and the space-orc necromonger differentiate by *which realm's bestiary their vessels were reaped from*. **Consequence: S2 and E10 Leg 3 are the same build** — one bestiary-wells workstream, two consumers, zero duplicated schema. Alternatives (authored race list; LLM-derived race) both weaker: the first is a parallel well the fiction doesn't need, the second violates substrate-grounded provenance (D7's methodological analog).

### F2 — Faction visibility: **FLIP** (deferral now conflicts with spec) → **row S3 (⚖)**

`faction_visibility=invisible` was a v1-era identity-sparse choice. The v2 spec needs factions visible on four independent surfaces: per-floor faction identity (line 158), lieutenant floor-bosses (line 144), bestiary faction sets (§11a), spawn-influence steering (§12 — you cannot PURSUE what you cannot see), plus Matt's pair naming orders at demo-pick. Per OP § 3.7(a): a code-level deferral that conflicts with the spec the work tracks against is a **GAP-TO-CLOSE**, not an accepted state. Derivation machinery already exists and runs — the flip is consumption-side (un-gate the flag, Wave A labels fire, D7 review pass on outputs). **Timing lean: land with E10 Leg 3** — factions become real when mobs wear them; flipping earlier ships labels nothing consumes.

### F3 — "Order" vocabulary collision → **row S4 (⚖)**

Story canon: **THE order** = the player's crusade (singular; `story-expansion.md` §2). Matt's pair: "necronomical order" / "necromonger order" = plural kit-identity affiliations. If both use "order" bare, the player's own institution and enemy factions blur. **Lean: no new mechanical well — "order" is faction-label NOUN VOCABULARY.** Faction labels draw their institutional noun from the faction's own register (order / dynasty / court / choir / warband / covenant…), so "the Necromonger Order" is a *faction whose label wears the noun*, while THE order keeps definite-article uniqueness. Genre precedent: D2 never called every institution a clan — Sisterhood of the Sightless Eye, Zakarum priesthood, Horadrim *order* — distinct institutional nouns did the identity work. Implementation cost ≈ one noun-register instruction in the PM-2 labeling prompt (D7-compliant narrow-blank fill).

### F4 — "Kits vote BARE" provenance law: **KEEP with FLAG** (no row)

Engine mechanism is PM-1 clustering over modal substrate evidence, not literal per-kit ballots. **The law's substance holds:** the derivation population is bare kits (lineage/tech/tone/element); loot never enters; the derivation is bottom-up from kit evidence. "Vote" reads as *kits determine factions from below* — clustering IS that. Flagged so Matt sees the mechanism difference; no flip warranted.

### F5 — Naming machinery vs D7: **KEEP** (commissioned candidate — answers clean)

All naming is narrow-blank LLM fill inside templated structure (names, 3–7-word labels, flavor blurbs) — no raw LLM dialogue at story moments. D7-compliant as built.

### F6 — Flavor coverage 35/~700: **FLAG** (no row)

Beat B glyph flavor covers finalists only. Not a gap **if** demo curation picks from the finalists shortlist; if Matt wants a wider pick pool, a flavor-extension pass rides the curation decision. Named here so the constraint is visible at C4 (demo assembly) time.

### F7 — Register filters: **KEEP** (commissioned candidate — answers clean)

Substrate register LIVE end-to-end; visual style-register is a separate lock (§1.7). No trivialization found.

## 4. Answers to the original commission

The S1 commission named three candidate surfaces: **flavor/naming pass shapes vs D7** → KEEP (F5), with a coverage FLAG (F6). **Faction-derivation depth at consumption** → the trivialization is real and is exactly at consumption: derivation LIVE, consumption ZERO → FLIP (F2/S3). **Register filters** → KEEP (F7). Beyond the commission, the walk surfaced the race well (F1/S2) and the order-noun collision (F3/S4) — both directly against the acceptance test.

## 5. What closes the acceptance test

Necromancer pair differentiates at demo-pick when: **S2** lands (vessel-race from bestiary wells — with E10 Leg 3), **S3** lands (faction labels visible + D7-reviewed), **S4** is ruled (order-noun grammar). Build/weapon dimensions already pass. No story-spec rewrite required; the spec's declarations are buildable as written.

**Signed:** gandalf, 2026-07-09. Survey-mode held: §§1–2 report what IS; §3 carries the leans. Matt rules S2/S3/S4 via Q12.
