# Monster Coverage Matrix — VS2a (2026-05-17)

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-monster-subset-curation-vs2a-final.md`
**Authority:** Matt L3 2026-05-17 — VS2a Final Sprint Q7 monster-subset curation YES authorization
**Companion deliverables:**
- `monster-subset-vs2a-2026-05-17.jsonl` — per-monster manifest (10 priority-3+ rows + 2 priority-2 deferred-noted)
- `monster-curation-summary-vs2a-2026-05-17.md` — executive summary + handoffs

---

## § 1 — Axes

**Substrate axis (8 rows):** fire / water / earth / wind / lightning / holy / shadow / physical

- The canonical-7 (fire/water/earth/wind/lightning/holy/shadow) per `canonical/story/substrate-expansion-decision-2026-05-17.md`
- Plus **physical** as 8th row (physical is damage-type in ARPG canon; classes can be physical-coded — sword-warrior, goblin-mage, orc — and this row captures non-element monster coverage)

**Role-tier axis (3 columns):** trash / elite / boss

- Trash = wave 1-3 trash adds (engine 'standard' + 'swarm' tiers visually mapped here)
- Elite = wave 3-4 elites + magic-tier ranged casters
- Boss = wave 5+ mini-boss + boss + act-boss (collapsed for matrix simplicity; per-tier breakdown in monsterSprites.ts ENEMY_TIER_CHARACTER_MAP)

**Note:** The current `monsterSprites.ts` distinguishes mini-boss from boss tier; this matrix collapses mini-boss into "boss" column for substrate-coverage clarity. Per-tier mini-boss-vs-boss differentiation is captured in the manifest's `tier` field and in § 4 below.

---

## § 2 — Coverage matrix

Per cell:
- **Current (CK):** currently wired CreativeKind monster filling this substrate/tier slot (if any)
- **Candidate (CP):** CraftPix candidate from this curation (if any)
- **Status:** GREEN (well-covered or candidate ready) / YELLOW (partial coverage; candidate optional or coverage thin) / RED (gap; no current and no candidate)

| Substrate | Trash | Elite | Boss (mini+full) |
|---|---|---|---|
| **fire** | CK: — / CP: **imp** (priority 4) — **GREEN** | CK: fire-lord-v5 / CP: — — **GREEN** | CK: — / CP: **dragon** (priority 5) — **GREEN** |
| **water** | CK: — / CP: **slime** (priority 5) — **GREEN** | CK: — / CP: — — **YELLOW** | CK: — / CP: **slime-boss** (priority 5) — **GREEN** |
| **earth** | CK: — / CP: **plant** (priority 3) — **GREEN** | CK: crystal-golem / CP: **ent** (priority 4 — supplement) — **GREEN** | CK: — / CP: **golem** (priority 5, mini-boss) — **GREEN (mini-boss only)** |
| **wind** | CK: — / CP: — — **YELLOW** | CK: — / CP: **beholder** (priority 5) — **GREEN** | CK: — / CP: — — **RED** |
| **lightning** | CK: — / CP: — — **RED** | CK: — / CP: — — **RED** | CK: fire-lord-creativkind-thunder (mini-boss; thunder-shifted from fire pack) / CP: — — **YELLOW** |
| **holy** | CK: — / CP: — — **RED** | CK: — / CP: — — **RED** | CK: angel-guardian / CP: — — **GREEN (boss only)** |
| **shadow** | CK: mutant-skeleton + evil-eye / CP: **zombie** (priority 4) — **GREEN** | CK: demon-mage / CP: lich-net-543463 (priority 2; deferred-noted) — **GREEN** | CK: lich (mini-boss; CK pack) / CP: — — **YELLOW (mini-boss only; no full-boss)** |
| **physical** | CK: sword-warrior + goblin-mage / CP: — — **GREEN** | CK: — / CP: **orc** (priority 4) — **GREEN** | CK: — / CP: — — **RED** |

**Legend:**
- **CK** = CreativeKind (currently wired in monsterSprites.ts)
- **CP** = CraftPix (from this curation)
- **Priority N** = vs2a_slot_priority per the manifest (5 = wire immediately; 1 = nice-to-have)

---

## § 3 — Pre-curation vs post-curation coverage

### § 3.1 — Before this curation (current state)

Counted from `monsterSprites.ts` ENEMY_TIER_CHARACTER_MAP active pool (11 slugs):

| Substrate × Tier | trash | elite | boss | Total wired |
|---|---|---|---|---|
| fire | 0 | 1 (fire-lord-v5) | 0 | 1 |
| water | 0 | 0 | 0 | **0** |
| earth | 0 | 1 (crystal-golem) | 0 | 1 |
| wind | 0 | 0 | 0 | **0** |
| lightning | 0 | 0 | 1 (fire-lord-thunder mini-boss) | 1 |
| holy | 0 | 0 | 1 (angel-guardian) | 1 |
| shadow | 2 (mutant-skeleton, evil-eye) | 1 (demon-mage) | 1 (lich mini-boss) | 4 |
| physical | 2 (sword-warrior, goblin-mage) | 0 | 0 | 2 |
| hellfire-rhino | — | — | 1 (mini-boss; unclassified — fire-coded but mechanically distinct) | 1 |
| **Total wired** | **4** | **3** | **4** | **11** |

**Gaps before curation:**
- 4 substrates have ZERO trash coverage (fire, water, earth, wind)
- 5 substrates have ZERO elite coverage (water, wind, lightning, holy, physical)
- 5 substrates have ZERO boss coverage (water, earth, wind, physical, and lightning/holy partially via mini-boss-only)
- Water and wind substrates have ZERO wired sprites at ANY tier — CRITICAL gap

### § 3.2 — After this curation (target state — 10 priority-3+ CraftPix additions)

| Substrate × Tier | trash adds | elite adds | boss adds | Net new wired |
|---|---|---|---|---|
| fire | +1 (imp) | — | +1 (dragon) | +2 |
| water | +1 (slime) | — | +1 (slime-boss) | +2 |
| earth | +1 (plant) | +1 (ent) | +1 (golem mini-boss) | +3 |
| wind | — | +1 (beholder) | — | +1 |
| lightning | — | — | — | 0 |
| holy | — | — | — | 0 |
| shadow | +1 (zombie) | — | — | +1 |
| physical | — | +1 (orc) | — | +1 |
| **Total adds** | **+4** | **+3** | **+3** | **+10** |

**Post-curation wired total: 21 monsters (was 11; +91% variety).**

### § 3.3 — Remaining RED cells after curation

| Cell | Severity | Notes |
|---|---|---|
| **wind boss** | **MEDIUM** | Wind has elite (beholder) post-curation but no boss tier. Could use beholder Beholder3 variant scaled-up if drax wants quick fix, or defer to Matt acquisition decision. |
| **lightning trash** | **LOW** | Lightning is genre-canonically rare at trash tier across ARPG history (lightning is typically caster/elite/boss flavor). Not a high-priority gap. |
| **lightning elite** | **LOW-MEDIUM** | Could shift fire-lord-creativkind-thunder from mini-boss back to elite as a lightning-elite slot if needed; or new vendor acquisition. |
| **holy trash** | **MEDIUM** | Holy at trash tier is also genre-rare but lore-coherent (small holy entities — cherubs, acolytes). No CraftPix candidate. ACQUISITION GAP — see summary § 5. |
| **holy elite** | **MEDIUM** | Same as above. ACQUISITION GAP. |
| **shadow boss** | **MEDIUM-LOW** | Shadow has lich at mini-boss but no full-boss. Could elevate lich-CraftPix-net-543463 to boss tier (it has 3 variants, including a more boss-like variant) or use boss-monsters-pixel-art demon variant (in pack craftpix-897123 — see § 4 below). |
| **physical boss** | **MEDIUM-LOW** | Physical boss (orc-king / warlord) absent. boss-monsters-pixel-art demon could serve as physical-boss substitute (demon is canonically melee-physical). |

---

## § 4 — Mini-boss vs boss decomposition

The matrix collapses mini-boss and boss. Per-tier decomposition (relevant to monsterSprites.ts ENEMY_TIER_CHARACTER_MAP):

| Tier | Current CK active pool (11) | Post-curation adds (10) | Post-curation total |
|---|---|---|---|
| trash | goblin-mage, mutant-skeleton, evil-eye, sword-warrior (4) | imp, slime, plant, zombie (4) | 8 |
| elite | crystal-golem, fire-lord-v5, demon-mage (3) | beholder, ent, orc (3) | 6 |
| mini-boss | lich, hellfire-rhino, fire-lord-creativkind-thunder (3) | golem (1) | 4 |
| boss | angel-guardian (1) | slime-boss, dragon (2) | 3 |
| **Total** | **11** | **+10** | **21** |

**Boss-tier expansion 1 → 3 is the highest-impact change.** Currently every act-boss encounter shows angel-guardian; post-curation enables dragon (fire), slime-boss (water), angel-guardian (holy) rotation — substrate-flavored bosses.

**Bonus pack not in the priority-3+ curation:** `craftpix-897123-boss-monsters-pixel-art` (Mage / Demon / Ooze bosses, full state-rich pack with projectile sub-assets — FireBall, IceBlock, Ray, orb_of_venom). This pack is a HIGH-VALUE secondary candidate that could fill multiple RED cells (lightning-elite via Mage; physical/shadow boss via Demon; alternative water boss via Ooze). Reason it's deferred: 10 monsters is already at the upper drax-wiring budget for v1.14. Recommend re-evaluating in v1.15 or as part of "VS2b boss expansion" — see summary § 6.

---

## § 5 — Substrate gap-closure scoring

Quantitative summary of how this curation closes substrate gaps:

| Substrate | Wired before | Wired after | Gap-closure | Status post-curation |
|---|---|---|---|---|
| fire | 1 | 3 | +2 | GREEN (trash + elite + boss) |
| water | 0 | 2 | +2 | YELLOW (trash + boss; missing elite) |
| earth | 1 | 4 | +3 | GREEN (trash + elite + mini-boss; elite stacked 2-deep) |
| wind | 0 | 1 | +1 | YELLOW (elite only; trash + boss gaps) |
| lightning | 1 | 1 | 0 | YELLOW (mini-boss only; trash + elite + full-boss gaps) |
| holy | 1 | 1 | 0 | YELLOW (boss only; trash + elite + mini-boss gaps) |
| shadow | 4 | 5 | +1 | GREEN (trash 3-deep, elite 1, mini-boss 1; no full-boss) |
| physical | 2 | 3 | +1 | YELLOW (trash 2-deep, elite 1; no boss) |

**Substrates that move from RED to GREEN/YELLOW with this curation:** water (RED → YELLOW; gained trash+boss), wind (RED → YELLOW; gained elite)

**Substrates that remain YELLOW (require future acquisition or pack-897123 follow-on):**
- **lightning** — needs trash + elite; project-wide gap; current resolution is the thunder-shifted Fire_Lord (Case D dispatch)
- **holy** — needs trash + elite + mini-boss; no native CraftPix pack covers holy substrate; acquisition gap for Matt
- **physical boss** — could be addressed via craftpix-897123 Demon boss (deferred to v1.15)
- **wind boss + water elite** — minor gaps; can be addressed via pack-897123 or beholder-tier-elevation

---

## § 6 — Substrate gap surface for Matt

| Gap | Severity | Recommendation |
|---|---|---|
| Holy substrate non-boss tiers | MEDIUM | ACQUISITION — holy-coded monster pack search needed (CraftPix has no holy-substrate pack; possible vendors: chierit pack already has light-valkyrie hint per substrate-expansion doc § 1 line 36) |
| Lightning substrate native | MEDIUM | ACQUISITION — chierit lightning-ronin per substrate-expansion doc § 1 (mentioned but not on disk per legolas-3 inventory) or new vendor crawl |
| Wind boss tier | LOW-MEDIUM | DEFER — beholder3 variant scale-up at drax v1.14; or pack-897123 follow-on at v1.15 |
| Physical boss tier | LOW-MEDIUM | DEFER — pack-897123 Demon boss at v1.15 |

These are surfaced to Matt via summary doc handoff (§ HANDOFFs).

---

*Matrix authored 2026-05-17 by elrond per dispatch + Matt L3 Q7 YES authorization. Companion to monster-subset-vs2a manifest + summary doc.*
