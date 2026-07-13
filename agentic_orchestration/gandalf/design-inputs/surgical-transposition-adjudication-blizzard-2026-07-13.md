# Surgical-transposition adjudication — Blizzard pass (`public_display_name` register)

**Author:** gandalf (CANON-STEWARD) · **Date:** 2026-07-13 · **For:** Matt ratification.
**Gate:** Q28 (`canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md`), decision-item 3 (RATIFIED surgical scope).
**Evidence:** Legolas Q28 probe (`agentic_orchestration/legolas/findings/ip-clearance-probe-2026-07-13/q28-ip-clearance-2026-07-13.md`).

---

## The register this fills
The middle rung of the naming ladder: **`public_display_name`** = exact `display_name` **for all but a few flagged tokens**, minimally transposed per-token where a distinctive coined class mark exists. Player-facing dev-log surface only (in-game kits are pipeline-named; Glance uses `display_name` exact). Held until Q28-#1 clears, but the ruleset is ratifiable now.

## The transposition RULE (per-token, from Matt's "Totem Witch not Witch Doctor")
> Keep every **mechanical / generic** token exact. Soften only the **distinctive coined class token**, dropping the coined half and retaining a generic descriptor. Never touch skill/set/mechanical tokens — those carry the recognition and are the least distinctive marks.

Example: `Multishot Demon Hunter` → keep "Multishot" (skill, generic), soften "Demon Hunter" (coined D3 class) → `Multishot Marksman`.

## The headline finding (steward-honest)
**The probe supports exact-by-default more strongly than we assumed, so the surgical list is genuinely tiny — 2 class tokens, ~9 affected names.** Maxroll/Icy Veins/poe.ninja use full class names with zero enforcement; the residual is commercial-adjacency (prong 3), which disclaimer + editorial framing address at the *page* level, **not** by transposing names. So this register is a light belt-and-suspenders hedge on the newest, most-distinctive, most-actively-defended Blizzard class marks — not a wholesale scrub.

---

## SCOPE-LINE — one ruling I need before the list is final
Where does "distinctive coined mark" cut?

- **Line A (my lean): coined CLASS tokens only.** Transpose Spiritborn / Demon Hunter / (Witch Doctor). Keep all set/unique proper-nouns exact (Akkhan, Zunimassa, Trag'Oul, Tal Rasha, Rathma…) — they read as **factual set attribution** in an editorial context (prong-1 necessity is strongest for them; there's no other way to name that build), and transposing them *destroys* recognition for near-zero risk gain. This matches your example (a class token) and the probe's "class marks are the most distinctive **product identifiers**."
- **Line B: class tokens + distinctive set/unique proper-nouns.** Bigger scrub (~40+ names), materially more recognition lost, marginal extra protection. I do **not** recommend it — but it's the fuller hedge if you want maximum distance from Blizzard specifically.

**My lean: Line A.** The rest of the doc assumes Line A; say the word and I expand to B.

---

## TIER 1 — TRANSPOSE (coined class tokens · Line A) — your keep/transpose call on each

| kit_id | exact `display_name` | proposed `public_display_name` | token softened |
|---|---|---|---|
| `d4-evade-sb` | Evade Spiritborn | Evade Spirit Adept | Spiritborn → Spirit Adept |
| `d4-payback-sb` | Payback Spiritborn | Payback Spirit Adept | " |
| `d4-quill-volley` | Quill Volley Spiritborn | Quill Volley Spirit Adept | " |
| `d4-touch-of-death` | Touch of Death Spiritborn | Touch of Death Spirit Adept | " |
| `di-multishot-dh` | Multishot Demon Hunter | Multishot Marksman | Demon Hunter → Marksman |
| `d3-ue-multishot` | UE Multishot | UE Multishot | *(no class token — KEEP exact)* |
| `di-vengeance-strafe-dh` | Strafe Weave DH | Strafe Weave Marksman | DH → Marksman |

**Proposed transposed tokens (your call — adjust freely):**
- **Spiritborn → "Spirit Adept"** (keeps the spirit theme, drops the coined `-born`; D4's newest class = highest active-defense value). Alternatives: "Spiritkin," "Spirit Warrior."
- **Demon Hunter → "Marksman"** (clean generic; the archer fantasy is already carried generically by d2 Bowazon / d4 Rogue). Alternatives: "Bounty Hunter," "Dark Ranger."

**Pre-registered rule (token absent from current data but keep the rule):**
- **Witch Doctor → "Witch"** (your example). No current folk_name contains it — D3 WD builds are set-named (Arachyr/Helltooth/Jade/Mundunugu/Zunimassa) — so nothing to transpose today, but the rule stands if a WD-class name enters.

## TIER 2 — KEEP EXACT (my recommendation under Line A)
Everything else in d2/d3/d4/di, including:
- **Generic class tokens** (public-domain / universal fantasy): Sorceress, Sorcerer, Barbarian, Necromancer, Druid, Paladin, Assassin, Amazon, Monk, Rogue, Wizard, Warlock, Crusader, Berserker, Zealot, Avenger, Enchantress, all `-mancer` variants, Were-forms.
- **Skill tokens** (generic mechanics): Blizzard, Fireball, Meteor, Frozen Orb, Bone Spear, Chain Lightning, Whirlwind, Multishot, etc.
- **Set / unique proper-nouns** (Line A): Akkhan, Arachyr, Helltooth, Inarius, Inna, Jade Harvester, Legacy of Dreams/LoD, LoN, Manald, Marauder, Masquerade, Mundunugu, Natalya, Pestilence, Raekor, Raiment, Rathma, Roland's, Sunwuko, Tal Rasha, Trag'Oul, Typhon, Uliana, Vyr, Chantodo, Zunimassa, Andariel, Immortal. → factual set attribution, editorial-defensible, recognition-critical.

## Non-Blizzard games (follow-on, NOT this pass)
Matt ratified **Blizzard-first** (probe flags Blizzard as materially more aggressive than GGG, which is community-tolerant with public APIs). PoE ascendancy class tokens (Hierophant, Deadeye, Elementalist, Occultist…) and LE mastery tokens (Bladedancer, Sentinel…) are the next-tier candidates *if* the register proves out — but GGG's posture makes them low-priority. Not adjudicated here.

---

## Ratification checklist (Matt)
- [ ] **Scope line:** A (class-tokens-only) [gandalf lean] · or B (+ set/proper-nouns)
- [ ] **Spiritborn → "Spirit Adept"** (or your token) — the 4 `-sb` names
- [ ] **Demon Hunter / DH → "Marksman"** (or your token) — the 2 DH names
- [ ] **Witch Doctor → "Witch"** rule pre-registered (no current effect)
- [ ] Tier-2 KEEP-EXACT confirmed

## Sequencing once ratified
1. gandalf: finalize the transposed tokens → hand Elrond a `public_display_name` column spec (exact `display_name` for all rows; overridden string for the flagged ~6).
2. Elrond: add `public_display_name` to `canon_corpus`, populate.
3. gandalf: renderer emits `public_display_name` in the per-dot JSON alongside `display_name` + `public_label`.
4. Drax: the register-switch variable flips to `public_display_name` when the dev-log surface publishes (still Q28-#1-gated).
