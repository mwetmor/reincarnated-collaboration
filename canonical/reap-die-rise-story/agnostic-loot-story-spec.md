# Loot & the Soul's Claim — STORY spec (soul-as-lens, gleaning, cementing, soul weapons)

**STATUS:** CANONICAL — authored 2026-07-07 (gandalf, SPEC-AUTHOR), absorbing Matt's mobile draft (`matt_notes_handoff_docs/reap-die-rise-agnostic-loot-system.md`, now bannered superseded-by-canon) + the 2026-07-06 review (`agentic_orchestration/gandalf/notes/2026-07-06-agnostic-loot-system-review.md`) + the 2026-07-07 Pattern-B ruling set (C1–C5 · G1 · G3 · body-persistence).
**Companion (engine half):** `../reap-die-rise-engine/agnostic-loot-engine-spec.md` — operator algebra, universal axes, validation campaign, engine contracts. **This doc owns the fiction + the player-facing story surfaces; the engine doc owns the math + the build.** Where they overlap, each defers to the other's seam.
**Governing anchors:** `gameplay-loop-design.md` §8 (sidegrade law) · §11 (Grimoire two-register + LISTING-FIRST) · §23 (run model: harvest §23.2, escape + body-persistence ruling §23.3, conduit moral economy §23.4–23.5).
**Micro-rulings:** **Q9 ✓ RULED 2026-07-07 (Matt — all five as recommended; §4).** No open story-side rulings remain in this spec.

---

## 1. The soul-as-lens (the gear fiction — LOCKED)

Every quality a piece of gear will ever have was **always in the item**. The item is **fixed light; the soul is the lens.** What changes across a player's lives is not the world's objects — it is the soul's **capacity to read them**. Reincarnation makes you see MORE in the same object.

This is the rare case where the mechanic IS the theme. *Reap. Die. Rise.* is about a soul that accretes across deaths while the world stays what it is — and the loot system now says exactly that, every time an item's color deepens in a returning reaper's hands. Nearest genre precedent: Last Epoch's Weaver's Will items (hidden potential awakening with use) — ours is stronger because the reveal is **soul-indexed, not item-indexed**: the item never changed; *you* did.

**Corollary (fiction-level):** gear belongs to the **soul**, not the body. A body is an instrument the soul plays; an item is a score the soul reads. The same item played through different bodies produces different music — that is the operator model (engine doc §1) heard from inside the fiction.

## 2. Two clocks, three verbs — the soul's claim on objects (LOCKED, Matt 2026-07-07)

G3's resolution: **gleaning and cementing are different mechanics on different clocks.** They compose with the run-scale harvest verb into a clean hierarchy:

| Verb | Clock | Chosen? | What it claims | Anchor |
|---|---|---|---|---|
| **The Harvest** (macro) | per-run, mandatory | no — the run's objective | the realm's souls, bound into **conduits**, banked **for the faith** | §23.2 |
| **Cementing** (micro) | **intra-run**, at-will within limits | yes — the run's personal stake | 1–3 chosen items, soul-bound so they **cross out of the realm** | this doc §4 |
| **Gleaning** | **inter-run**, passive | no — it happens *to* your held gear | deeper reading of what you already carry | this doc §3 |

Cementing is the **personal micro-version of the harvest verb**: the cult binds a realm's treasure to the god; the reaper binds a trinket to their own soul. Same gesture, different altar.

## 3. Gleaning — the inter-run reveal

- **Soul level** — a function of experience level × number of reincarnations — determines how many of an item's **latent operators are awake** (engine doc §1 holds the operator mechanics). As soul level rises, held gear **deepens**: operators gated behind soul-level thresholds activate.
- **Color on pickup reflects the current soul's glean** — an item's effective revealed rarity *for you, now*. Two reapers stand over the same drop and see different lights.
- **Guardrail (LOCKED, draft §3.3):** re-gleaning is a **bonus** progression layer, NOT the primary one. **Drop-acquisition dopamine stays the main loop** ("more loot than Diablo"). This is the D3 loot-2.0 lesson: when deepening-what-you-have replaces finding-what's-next, the core loot thrill starves. Both run in parallel — frequent drops (acquisition) + soul-level re-gleaning of held gear (deepening).
- **Pacing note:** gleaning thresholds tune in **hours, not minutes** — it is meta-progression spine material (beside the form library / Grimoire), and its threshold math waits on the persistence structure now settled here (gear crosses runs only by cementing, §4; soul level crosses always).

## 4. Cementing — the intra-run binding rite

- **What it is:** during a run, the player may **soul-bind ("cement") a small number of items — cap 1–3 —** so they cross out of the realm at the escape. Everything else worn or carried is realm-stuff and stays (§6, cleansed crossing).
- **The window closes at the eruption.** Once the conduits are combined and the realm turns (§23.3), there is no more cementing — the flight is for surviving, not shopping. Choose what you'll keep *before* you light the fuse. This puts a real decision-beat inside every run: of everything this realm gave me, what do I make **mine**?
- **Diegetic valence — SANCTIONED (✓ RULED Matt 2026-07-07, spec default confirmed):** cementing is **the reaper's wage**, an allowed personal take within the holy work — NOT a transgression. Rationale (load-bearing): §23.4's conduit hand-in-vs-keep is deliberately **the** moral decision-object of the run economy; introducing a second transgressive-take mechanic would dilute the one dilemma the whole defiance↔devotion axis (§16/§23.5) is built on. The faith pays its instruments; the *conduit* is where your soul is weighed.
- **Sanctioned payout channel is exempt from the cap:** the performance-scaled **bonus treasures** of §23.2 (faster clear / more possessions → more loot) cross home as the faith's payout without consuming cement slots. Cement slots are for **chosen** attachments; the wage is the wage. *(✓ Q9 confirmed, Matt 2026-07-07.)*
- **Micro-rulings — ✓ RULED (Q9, Matt 2026-07-07, all as recommended):**
  1. **The cement-act's shape — RULED: (b) shrine-stations** — a brief rite at fixed stations along the descent. Legible, procgen-friendly (one per beat: Structure 1 / crossing / Structure 2), and the pre-eruption "last chance" station is a natural dramatic beat. *(Rejected: (a) spend-anywhere, (c) boss-deed.)*
  2. **Cap size + growth — RULED: start at 1**, expand to 2–3 via meta-progression keyed to **soul level** — the soul that sees more can carry more; gleaning and cementing climb the same fictional spine.
  3. **Failed escape — RULED: cemented survives** — the binding is a **soul fact, not a pocket fact**; death costs the run's un-cemented spoils + §23.2 bonuses, which keeps escape-death expensive without confiscating the one thing the player deliberately made theirs.

## 5. Soul weapons — the flagship item (fiction LOCKED; build = engine doc §8 / Track D)

- **The player's weapon is a soul weapon:** a manifestation of the soul's armament that **takes the form appropriate to the body wearing it** — blade in a warrior body, bow in an archer body, focus in a caster — while carrying the same operators. It is agnostic **diegetically**, not just mechanically: "why is my archer carrying a sword" never happens, at the fiction layer. This is the isekai divine-armament-that-grows trope done with mechanical honesty.
- **Identity comes from the catalogue substrate (C4, ruled):** soul-weapon bases draw on the **museum/mythic weapon corpus** already curated (`weapon_knowledge_entries` — cultural_lineage / historical_period / register fields live). A soul weapon is not a generic glow — it is *a real weapon's soul*, with a lineage the codex can surface, re-expressed per body. Provenance is the flavor: the substrate IS the myth.
- **Per-body re-expression is the showcase:** reincarnate mid-run into the champion (§23.3) and watch your soul weapon melt from bow into the champion's culture-true greatblade, same name, same operators, new music. The loot system's whole thesis — soul-owned, body-expressed — performed in one beat.

## 6. The body and the loot (composition with the §23.3 ruling, Matt 2026-07-07)

- **You are your latest body.** The escape body persists as the active self — you walk into realm N+1 wearing realm N's champion. Identity is **serial, not parallel** (one chain of lives; the Grimoire's living page; §11 LISTING-FIRST untouched). §8's sidegrade law is the balance governor — the form is kept, its situational level-heat normalizes, every run starts in-band.
- **The body crosses home CLEANSED:** its worn gear stays in the realm **unless cemented**. Body-keeping and gear-cementing coexist without either eating the other — you keep the vessel; you keep only what you bound.
- **The banking triad (the run's take, in one line):** the **conduits** are what you bank **for the faith** · the **body** is what you bank **for yourself** · the **cemented items** are what you bank **for the soul.**

## 7. Names, descriptions, and the AI-tell line (C5, ruled — story-side surface contract)

- **The LLM invents the NAME only** — and the name must be a **readable compression of the item's function** (draft §5.1): "Twinfang" for chain-to-second-target, "Hollowcost" for resource conversion. Anti-goal: flavorful-but-opaque ("Shadowmourne of the Endless Void"). D1 vocabulary-commonness lessons bind: common-vocabulary compression, no obscure-vocab prestige words.
- **Realized descriptions are COMPUTED** — a deterministic template render of the item's awake operators on the **current body** at the **current soul level** ("Your arrows split to a second target"). Rules text is never LLM-paraphrased: an LLM paraphrase of rules risks WRONG rules on a player-facing surface (D7 AI-tell line). An optional flavor sentence may ride below, clearly subordinate.
- **Fixed vs. generated naming (draft §5.3, adopted):** marquee legendaries/sets = fixed authored names + fixed points (stable identity players trade knowledge about — "everyone knows Twinfang"); the generated mass = procedural LLM names under the compression constraint. Same authored-spine / generated-body split used everywhere else.

## 8. What this doc does NOT decide

- ~~Q9 micro-rulings~~ **✓ RULED 2026-07-07** (all five as recommended — §4: shrine-stations · cap starts 1 · cemented survives · payout exempt · sanctioned wage).
- **Engine-side open items (engine doc §9–§10 / Q10):** ~~ω-penalty · band widths~~ ✓ RULED 2026-07-07 — the one remaining Q10 item is resist/mitigation cap VALUES (band-time) · everything about the build.
- **Reincarnation-choice pacing** (draft §10's second bullet — whether declining reincarnation needs its own gear path) — rides the §23.7 open-questions family, not this spec.

---

**Signed:** gandalf, 2026-07-07. *The item never changed; you did. Choose what you'll keep before you light the fuse.*
