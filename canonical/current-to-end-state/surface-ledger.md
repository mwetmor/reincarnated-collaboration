# SURFACE LEDGER — Trivialization Audit + Matt Per-Surface Agreement Gate (LIVING)

> **STATUS:** LIVING CANONICAL — born 2026-07-08 (Matt directive, verbatim: *"build a surface
> chart/table out EXACTLY like this in the Glance report as we go along. Once I agree on all
> surfaces for the engine, story, demo/game and content emission pipeline, then we can proceed
> with the demo in full view."*). Fifth canon card (Glance contract v1.3 §7.2).
> **Steward:** gandalf (rows accrue from the commissioned trivialization audit — any agent may
> surface a row; gandalf curates; **Matt rules every row**). **Authority record:**
> `agentic_orchestration/gandalf/notes/2026-07-08-full-run-pivot-four-rulings.md`.

---

## HOW THIS DOC WORKS

- **What a row is:** a surface where the build narrowed, stubbed, or fixed something the spec
  wants varied/deep — discovered by the trivialization audit (Matt 2026-07-08: *"I cringe to
  think of what else was trivialized in the name of 'sprint to Demo'"*) — OR a surface Matt has
  explicitly ruled in the pivot. **Survey-mode:** the *Current state* cell is what-IS, cited;
  the *Classification* cell is the disposition lean (FLIP / FLAG / KEEP per gandalf OP §3.7).
- **Row lifecycle (the Matt gate, per row):** `⚖` surfaced (classification = steward lean) →
  Matt rules → **KEEP** = `✓` agreed as-is · **FLIP** = `IN-FLIGHT` while the gap closes → `✓`
  when landed + Matt-seen · **FLAG** = stays `⚖` with the fork named until ruled.
- **THE GATE:** demo assembly + emission of any size fire only when **every row reads ✓**
  (GATE1 below). This is Matt's gate sentence made structural.
- **NOT a fifth tracker.** The four `current-to-end-state/` trackers hold the full build queues
  (what the work owes the spec). This ledger holds ONLY the audit surfaces + Matt's agreement
  state. Rows cross-reference tracker rows where they exist. Never silently delete — strike
  with date, per house law.

---

## FLOW (end-to-end at a glance — Glance shape #6, contract spec § 2.7)

> Stage state is DERIVED from each section's modeled rows. All-✓ across all four domains closes
> GATE1 — that is the demo gate, visible as a flow-bar.

1. **Engine surfaces** ← ENGINE
2. **Content-emission surfaces** ← CONTENT-EMISSION
3. **Demo / game surfaces** ← DEMO-GAME
4. **Story surfaces** ← STORY
5. **The gate** ← THE GATE

---

## SESSION-DELTA LOG (latest governs all below)

### 2026-07-08 — Ledger born; seeded with the session's source-verified engine rows + the four ruled pivot surfaces

Born under the Matt-ratified full-run pivot (four rulings: seed scrapped · demo re-sourced
curated-20 · full-spec main line per-axis · trivialization audit commissioned). Seed rows:
**ENGINE E1–E9** = this session's source-verified findings (every claim file:line — the
geometry-collapse headline E1 is the main line's first axis); **CONTENT-EMISSION C1–C4** +
**DEMO-GAME G1–G2** = the pivot's ruled surfaces (C1/G1/G2 enter already-ruled); **STORY S1** =
audit pending (no story-side surface walked yet — rows accrue, never invented). GATE1 declared
dangling-open by design (§2.4 named gate; closes in a future delta when the last row flips ✓).

**Signed:** gandalf, 2026-07-08.

---

## ENGINE surfaces

> Source-verified 2026-07-08 (gandalf session; file:line per row). E-rows are the "what else was
> trivialized" answer for the kit/skill emission path — the sim side is largely NOT the
> bottleneck (it already resolves the rich vocabulary; see E1).

| # | Surface | Current state (what-IS, cited) | Classification (lean) | Matt gate |
|---|---|---|---|---|
| **E1** | Skill geometry palette (emitter) | `_BC_AMPLITUDE_TO_GEOMETRY` maps 3 amplitude values → single_target / small_aoe / large_aoe; ONE geometry per kit (`per_skill_emitter.py:215-219, :585`). Sim already resolves a 24-type rich vocabulary → 6 spatial classes (`spatial_gauntlet/spatial_engine.py:404-429`) + B11 per-geometry mechanics — chain 0.7, fork 0.6, multiproj 0.65, ring 1.2×, leap 1.3× (`damage_resolver.py:85-139`). Bottleneck = the one rocket-side table. | **FLIP** — first axis of the main line (rocket). Movement-verb geometries (dash/blink → spatial "none") = named design fork riding the axis (kit-side mobility is the PoE-true F4 answer). | ⚖ awaiting Matt |
| **E2** | Skill damage / economy scalars | `BASE_SPELL_DAMAGE_L50` uniform 20,532.2 across ALL tiers/kits (`per_skill_emitter.py:106-115`); fixed energy/cooldown/cast tables per (tier, role) (`:49-54` + tables) — no per-kit economy texture. | **FLIP** — per-kit economy variation (doc-48 five kernel economies exist as *labels*; make them mechanical). | ⚖ awaiting Matt |
| **E3** | Hybrid scaling patterns | `hybrid_pattern=None` population-wide (Q-W05-R4 deferral); hybrids get chain_B secondary *element* only — content-distinct, mechanics-identical. | **FLIP** — Amendment 7a intends hybrids as builds, not palette swaps. | ⚖ awaiting Matt |
| **E4** | Skill timing variety | Instant-cast everything except T4-channeled (`per_skill_emitter.py` timing emission) — no cast-time / wind-up / charge texture. | **FLIP** — timing is a core ARPG feel axis (D2 FCR breakpoints, PoE cast-speed builds). | ⚖ awaiting Matt |
| **E5** | Investment expression in certification | Certification fights a fixed L50 instrument state; player investment (levels/gear/traits) has no expression in what certifies. | **FLAG** — design fork: what investment state(s) must a kit certify at? (Single-point vs envelope; envelope = D3 GR-ladder shape.) | ⚖ awaiting Matt |
| **E6** | Summon / proxy T4 suite | Five ratified PROXY-family members, two-phase activation per `reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3; B1-rebase in flight; proxy-dominant cells append the 13th summon skill (`season_generation_pipeline.py:1140+`). | **FLIP — already in-flight** (ruled 2026-07-02; execution rides the main line). | IN-FLIGHT |
| **E7** | Soul-bound weapon mechanics | Substrate weapon = identity-YES / mechanics-NO: cultural lineage/period/register bind (`season_generation_pipeline.py:356-441`), zero-contribution weapon shell in cert gear (`combatant.py:491-545`). | **KEEP — sequenced**, not trivialized: loot campaign inherits the certified instrument; `express_gear` succession = function swap + band re-fit (planned). | ⚖ awaiting Matt |
| **E8** | Skill naming / flavor | Placeholder names (`skill_a1`-style) at emission; Phase-5 LLM naming layer fills downstream (`per_skill_emitter.py:616-620`). | **KEEP — layer-handoff** (the legitimate deferred class, OP §3.7a; D7 AI-tell line governs the fill). | ⚖ awaiting Matt |
| **E9** | Mob build depth | Mobs are stat-blocks + threat-tier skills via `emit_skills_for_threat_tier`, not kit-built units; no mob gear. | **FLAG** — fork: how deep do mob builds go? (Gearing mobs vs player gear violates the §7 sawtooth guard [DECISION/CRITICAL]; depth must come from another axis if wanted.) | ⚖ awaiting Matt |

## CONTENT-EMISSION surfaces

| # | Surface | Current state (what-IS, cited) | Classification (lean) | Matt gate |
|---|---|---|---|---|
| **C1** | Certification population sourcing | Was: seed-57000000, 18 BC cells × 100 = 1,800 template-lattice kits (`season_generation_pipeline.py:1108`). | **✓ RULED 2026-07-08 (pivot a):** population SCRAPPED — never becomes content; F1 pilot findings survive as *instrument* evidence; regeneration is per-axis on the main line. | ✓ ruled |
| **C2** | Pilot instrument (two-leg, arms S/G) | Halt-verified gaps: `measured_gear_stats` plumbed leaf-only (absent w4g1/w4g2/w5g1); Leg-i cell-grain two-arm driver never written (only the Leg-ii harness exists). | **KEEP as instrument — completion-build AUTHORIZED (disposition A)**, population-agnostic; converts to the standing per-axis certification instrument. Fire on the old seed = optional machine smoke-test, zero content authority. | IN-FLIGHT |
| **C3** | KPM band tables | All live bands fit to STRIPPED distributions on the scrapped population (2026-07-08 ratified set = current-instrument only). | **FLIP** — re-fit at every declared baseline (arm-G gear × each per-axis population). `gates-on: E1` (first re-fit lands with the geometry axis). | OPEN |
| **C4** | Emission fire (any size) | Blocked by construction pre-pivot (F4 catalog hole, closed) — now gated on the ledger itself. | **Gate-bound:** `gates-on: GATE1` — no emission until all surfaces agreed + re-pilot on the widened population at re-fit bands. | ⛔ gated |

## DEMO-GAME surfaces

| # | Surface | Current state (what-IS, cited) | Classification (lean) | Matt gate |
|---|---|---|---|---|
| **G1** | Demo roster sourcing | Was: 18 kits = 18 BC cells 1:1 from the certified emission population (2026-07-06 ruling). | **✓ RULED 2026-07-08 (pivot b):** Matt-curated **~20 hand-picked** from the full-spec population, each **kit-grain certified** (Leg-ii GRAIN mode). Count supersedes 18; cell-coverage-at-pick = Matt's choice at curation (steward lean: preserve breadth). "Zero hand-authored shipped content" SURVIVES — curation ≠ authorship. | ✓ ruled |
| **G2** | "Sprint-to-demo" as scope license | The framing that licensed E1–E4-class narrowing; inverted the orientation anchor (Engine first. Game second. Phase third.). | **✓ RETIRED 2026-07-08 (pivot b):** demo stays THE DENOMINATOR (scope anchor, `one-realm-mvp-scope.md` unchanged); never again a build-shortcut license. | ✓ ruled |

## STORY surfaces

| # | Surface | Current state (what-IS, cited) | Classification (lean) | Matt gate |
|---|---|---|---|---|
| **S1** | Story-side trivialization audit | Not yet walked — candidate surfaces: flavor/naming pass shapes vs D7, faction-derivation depth at consumption, register filters. No finding yet; rows accrue from the audit, never invented. | Audit PENDING (commissioned 2026-07-08, pivot d). | OPEN |

## THE GATE

| # | Surface | Current state | Classification | Matt gate |
|---|---|---|---|---|
| **GATE1** | Demo proceeds "in full view" + emission un-gates | Matt 2026-07-08: *"Once I agree on all surfaces … then we can proceed with the demo in full view."* | Closes when **every row above reads ✓**. `gates-on: all-surfaces-agreed (named gate — closed in a delta when the last row flips)` | ⛔ open by design |

---

**Signed:** gandalf, 2026-07-08 (born). The trackers say what the work owes the spec; the Matt
queues say what waits on Matt; **this ledger says what was narrowed, what we call it, and
whether Matt has agreed — row by row, until the demo may proceed in full view.**
