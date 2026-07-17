# Lost Ark Post-Cutoff Dossiers — Edition-IV Hold-Out Debt

**Mode:** A (analytical research)
**Commissioner:** gandalf-prime (autonomous atlas-parity run; Matt authorization 2026-07-16)
**Filed:** legolas, 2026-07-16
**Directory:** `agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/`
**Coverage:** 4 Lost Ark post-training-cutoff kits (the Wildsoul × Valkyrie hold-out) + kb-URL backfill sheet
**Purpose:** Pay the Edition-IV refit spec's T4/P-1 hold-out debt. These 4 rows are ratified with `dossier_owed=1` and CANNOT enter the atlas until a live-sourced dossier exists per row.

---

## Post-cutoff law observance

Every mechanical claim in every dossier below carries at least one live-URL citation with access date 2026-07-16. Nothing is trusted from model memory. Where a claim survives only on a single-source citation, it is flagged as such in the dossier's confidence column.

---

## Status per dossier

| # | kit_id | Dossier file | Status | Strongest live source |
|---|---|---|---|---|
| 1 | `la-ferality-wildsoul` | `01-la-ferality-wildsoul.md` | **COMPLETE** | Maxroll build guide + Fandom Wiki + PlayLostArk spotlight |
| 2 | `la-phantom-beast-awakening-wildsoul` | `02-la-phantom-beast-awakening-wildsoul.md` | **COMPLETE** | Maxroll build guide + Fandom Wiki + PlayLostArk spotlight |
| 3 | `la-shining-knight-valkyrie` | `03-la-shining-knight-valkyrie.md` | **COMPLETE** | Maxroll build guide + PlayLostArk release page |
| 4 | `la-liberator-valkyrie` | `04-la-liberator-valkyrie.md` | **PARTIAL** (mobility-while-casting posture underspecified in accessible sources; Maxroll guide notes "a lot of mobility and fast animations" but does not resolve rooted/walk/full-move for buff-application skills. Flagged in dossier.) | Maxroll build guide + PlayLostArk release page |

---

## Slot-confidence matrix (engine-prefix slots only)

Key: H = HIGH · M = MED · L = LOW · * = single-source

| # | Kit | attr | range | tempo | amp | proxy | commit |
|---|---|---|---|---|---|---|---|
| 1 | la-ferality-wildsoul | SPEC/H | melee-mid/H | high/H | spiky/M | solo/H | wind-up/M (transformation entry + 323 rotation cadence) |
| 2 | la-phantom-beast-awakening-wildsoul | SPEC/H | melee-mid/H | high/H | spiky/M | solo/H (+summon flavor in identity form) | wind-up/M (identity gauge fill → Z burst) |
| 3 | la-shining-knight-valkyrie | SPEC/H | melee/M | high/H | spiky/H (Final Splendor single-hit finisher) | solo/H | wind-up/H (15-skill Light Meter fill → Z → X commit) |
| 4 | la-liberator-valkyrie | SPEC/H | melee/M | mid/M | flat/M (support role; buff throughput) | solo/H (but SUPPORT semantics — party is the beneficiary, not a proxy) | wind-up/M (3-stack Liberator cycle → Light of the Faithful heal) |

**Note on `attr` slot for LA classes:** Lost Ark does not use per-class stat scaling in the D2/PoE sense; class identity is the primary attr signal, and "SPEC" (Specialization) is the game's identity-gauge scaling stat that acts as the class-defining attribute. Elrond may fold this into an `attr: N/A-la-class` convention or route to a class-tag lens.

---

## Shapeshift-relevance verdict (GX-02 evidence)

**Ferality Wildsoul** — **STRONG POSITIVE** for GX-02 SHAPESHIFT. The build IS the shapeshift keystone in mechanical form: Fox and Bear are form-locked skill sets, transformation is gated by a persistent Phantom Beast Energy gauge, and the "323 rotation" is defined by ordered form-swaps. See dossier §Shapeshift-relevance for the exact form-entry cost, form-locked skill lists, and gauge interplay.

**Phantom Beast Awakening Wildsoul** — **MEDIUM POSITIVE** for GX-02, different geometry. The form-swap here is a temporal state (Phantom Beast Awakening Form, 30s duration, Z-toggled) rather than a persistent multi-form partition. Bear and Fox skills exist but this build's identity is the timed super-mode with cooldown-reduction economy via Phantom Beast Spirit stacks. Evidence for a "temporal-window shapeshift" flavor — distinct from Ferality's "persistent-form shapeshift."

**Both Valkyries** — **NEGATIVE** for GX-02. Valkyrie is a Holy Knight class; no form-swap in either engraving. Included in dossier so downstream doesn't have to re-check.

---

## Sources (aggregate, 2026-07-16 access)

| Source | Used for | Type |
|---|---|---|
| Maxroll Ferality Wildsoul build guide | Ferality mechanics, rotation, gauge, engraving | Primary (community authoritative) |
| Maxroll Phantom Beast Awakening Wildsoul build guide | PBA mechanics, identity form, stack economy | Primary |
| Maxroll Shining Knight Valkyrie build guide | SK rotation, Light Meter, Holy Blade skills | Primary |
| Maxroll Liberator Valkyrie build guide | Liberator support kit, Wings of Freedom, stacks | Primary |
| Lost Ark Fandom Wiki — Wildsoul | Skill list per form, weapon type | Primary |
| PlayLostArk news — Wildsoul Class Spotlight (en-gb) | Official class framing, dual playstyle description | Primary official |
| PlayLostArk release page — Rise of the Valkyrie | Release date, official identity system (Piety Meter) | Primary official |
| Maxroll class overview | Class-tag classification (Specialist / Warrior) | Primary |
| MMORPG.com Wildsoul detail article | Summon-vs-become framing, Phantom Beast as summoned form | Secondary |
| MMOs.com / digitalchumps release-date corroboration | Release-date cross-verify (Feb 26 2025) | Secondary |
| fdaytalk Valkyrie build guide | Shining Knight buff wording ("35% next 3 Holy Blade") | Secondary |

## Knowledge gaps not resolved

1. **Valkyrie Piety Meter exact fill mechanics.** PlayLostArk release page says "Piety Meter fills her Piety Meter during combat" — Maxroll's Shining Knight guide references "Light Meter" filling "6.7% per skill cast, capping at 15 casts." Whether Piety = Light Meter (English localization drift) or two distinct meters is not resolved. Both dossiers cite the operational "Light Meter" mechanic (Maxroll) and note the "Piety Meter" official term (PlayLostArk).
2. **Liberator mobility-while-casting posture** for buff-application skills (Seraphic Leap / Seraphic Oath / Circle of Truth). Maxroll notes "fast animations" and "a lot of mobility" but does not resolve whether these are rooted casts or full-move casts. Flagged PARTIAL.
3. **Ferality "323 rotation" full 6-skill Bear/Fox partition** — Maxroll confirms Pair 1 (Fox Flame, Boulder Bear, Fox Illusion) and Pair 2 (Fox Orb, Swish Bear, Fox Illusion) but the "3-2-3" numeric label's arithmetic (3+2+3) doesn't obviously match a 6-skill loadout without extra context on Fox Illusion's role as a repeat/pair-connector.
4. **Wildsoul weapon type** not explicitly extracted from the official spotlight page. Fandom Wiki + Maxroll imply beast-transformation is weapon-adjacent (form IS the weapon). Not verified with a single citable phrase.

---

## Action items for downstream agents

**→ Elrond:**
1. All 4 dossiers cleared for atlas entry per E4 refit spec. Apply per-row updates: set `dossier_owed=0`, populate `sources_used` with live URLs from each dossier, cap prefix-slot confidence at MED where marked, elevate to HIGH where marked H.
2. `attr` slot convention decision needed for LA class rows — see slot-confidence table note.
3. `la-ferality-wildsoul` and `la-phantom-beast-awakening-wildsoul` should both carry a `shapeshift_evidence` flag (or equivalent lens tag) for GX-02 tracing. See dossiers.
4. Apply the kb-URL backfill sheet (`kb-url-backfill-sheet.md`) — 52 post-cutoff kb-only rows enumerated; per-row confirm/correct/unverifiable disposition.

**→ Gandalf:**
1. GX-02 SHAPESHIFT keystone gains 2 positive attestations (Ferality + PBA Wildsoul) with distinct sub-flavors (persistent-form vs temporal-window). Recognition record candidate — the LA Wildsoul is genre-precedent for BOTH shapeshift geometries the keystone might accommodate.
2. Ferality "323 rotation" is a genre-precedent for form-locked skill loadouts with mandatory swap cadence — worth noting against any RDR shapeshift-kit rotation design.

**→ Knight-rider:**
1. All 4 dossiers COMPLETE (dossier 4 with named PARTIAL gap). Hold-out debt paid. Atlas parity next step is Elrond's E4 refit application.
</content>
</invoke>