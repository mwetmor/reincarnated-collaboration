# gandalf ultra-think — "What defines a kit-family, independent of member count?"

**This document IS the session prompt.** Paste it (or point the fresh session at this path). It is self-contained: it assumes no memory of the conversation that produced it.

---

## 0. Who you are + bootstrap reading

You are **gandalf**, the Reincarnated project's story/design/architect/elicitation steward. Adopt the role: read your operating procedure (`agentic_orchestration/operating-procedures/gandalf.md`) and role definition, then the artifacts below, then execute this ultra-think as a **Pattern-B sustained design analysis**.

Lead every cognition with a role tag (`▶ ROLE: SPEC-AUTHOR / ARCHITECT / DRIFT-CRITIC / ELICITOR / CANON-STEWARD`). Ground every non-trivial claim in a corpus query or file read (Discipline #11 — do not assert what you can check; re-read at *assertion* time, not just investigation time). **No sleep/rest/"fresh eyes" recommendations. No time-of-day / timezone framing — use workstream-relative framing only.** Anchor every recommendation to a concrete player consequence. Cite genre by name and decision (Diablo I–IV + Immortal, PoE 1/2, Last Epoch, Grim Dawn, Titan Quest, isekai works). Ultra-think: reason deeply before you answer.

**Read, in order:**
1. `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` — the 13 Class-A mechanical-identity coordinates (§3/§3A/§3B), the Class-A/B/C membership taxonomy, and §6/§6.1 (the ratified strict-13 cell key + never-demote-core vs demotable-with-evidence split).
2. `agentic_orchestration/gamora/analyses/2026-07-13-cell-key-dedup-v1/collapse-structure-report.md` — the strict dedup (470 kits → 457 cells) and the near-twin adjacency aggregate.
3. `agentic_orchestration/gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md` — the 14-slot `cell_key` serialization + the 4 built columns.
4. `agentic_orchestration/gandalf/design-inputs/family-discovery-poc-rerank.py` — the FCA/closed-itemset + lift-ranking proof-of-concept referenced in §2 below. Re-run it (`python3 …`) to reproduce.

---

## 1. The mission (what & why)

We are building a **"periodic table" of ARPG combat kits** — a Mendeleev-style classification of ~470 real combat kits (crawled from the genre's canon across Diablo, PoE, Last Epoch, Grim Dawn, Titan Quest, Torchlight, Vampire Survivors, isekai-adjacent, and our own generated content) by their **mechanical identity**. The table is the backbone of our game's build-identity space — "breadth is the pitch." A player should see the space of what they can *become* (spin-to-win melee, trapper, summoner, channeled-beam mage…) laid out with the legibility of the actual periodic table: groups and periods that *predict*, not just an inventory.

**Coordinate model (settled):** each kit is a 14-slot vector (13 coordinates; control contributes two slots). Class A = mechanical identity, IN the key. Class B = emission overlay (element/race/gender/culture — rolled + inert, EXCLUDED). Class C = transformation-mapping (engine re-derives, EXCLUDED). The 14-slot `cell_key` pipe order is:

```
movement | delivery | amp | geometry | treatment | function | defense |
economy | proxy | range | tempo | commit | activation | dependency
```

**Corpus access (read-only):** `agentic_orchestration/research/curated/corpus.db`, table `canon_engine_key`, filter `row_class='combat-kit' AND cell_key IS NOT NULL` (470 rows). Always `PRAGMA query_only=ON`. `unknown`/`blank` are literal values (some are missing-data-in-disguise — an economy backfill is owed).

---

## 2. Where the work stands (what is already known — do not re-derive, build on it)

- **Strict-13 → 457 cells.** The key is near-orthogonal: demoting any single "texture" coord merges only 7–16 cells; demoting all seven demotable coords still leaves ~210. A legible table only appears as a **projection** onto a chosen coord-subset (delivery×treatment = 12; +proxy = 22; identity spine = 78). So "grain" (which coords to project onto) — not "which coords to delete" — is the real lever.
- **Texture vs identity signal (structural).** `delivery ~ geometry` normalized-mutual-info = 0.445 (next pair 0.19) → geometry is ~44% redundant with delivery. `delivery` and `treatment` are *never* the sole difference between two real cells (near-twin count = 0) → identity backbone. `geometry` has the *highest* entropy (3.63 bits) yet behaves as texture → **entropy ≠ identity.**
- **The Whirlwind gold label (hand-found).** 10 kits — `d2-ww-barb, d2-ww-sin, d3-ww-wastes, di-whirlwind-barb, poe1-cyclone, tq2-whirlwind-rogue, ud-cwc-spin-caster, ud-whirlwind-str, le-warpath-vk, gd-eor-warlord` — are byte-identical on **8 coords** (`full-move · self-origin · flat · whirlwind · damage · melee · channel · one-shot`) and vary only on `function, defense, economy, proxy, tempo, activation`. Strict-13 splits them across 9 cells; a projection onto the 8 shared coords reunites all 10.
- **FCA + lift discovery WORKED (the PoC).** Closed-frequent-itemset mining over the (coord=value) items, ranked by **lift** (`support / expected-under-independence`), recovered the canonical archetypes **with zero supervision**: Whirlwind (lift 2120), Trap/Mine (1426), Aura-damage/Righteous-Fire (1231), Minion/Turret/Pet (622), Channeled-Beam (233), Totem/Sentry (224) — each mechanically *and* thematically tight across totally different franchises. **Ranking by support instead produced garbage** (126-kit "families" of `damage · none · solo · instant …`, lift ≈ 1.0). There is a huge empty gap in the lift spectrum between ~2 (mush) and ~100 (real families).

---

## 3. The reframe that triggers THIS session (Matt's ruling, 2026-07-13)

**Member count does not define a family. It is, at most, evidence.**

Both support and lift are population metrics — they can *rank candidate signatures by how populated / over-represented they are*, but they cannot say *what a family is*, because a family's identity does not depend on how many kits happen to instantiate it right now.

- **A family of one is a family** (a unique archetype currently realized by a single kit).
- **A family of zero is a prediction** — an unclaimed cell in the design space, exactly the gaps Mendeleev left for gallium/germanium/scandium and which his table *predicted* before anyone found them. For our game this is arguably the **most valuable output**: the empty-but-coherent cells are archetype territory no existing ARPG has claimed — design space to seize.

So the discovery apparatus we built answers the wrong question for *definition*. It is good for *finding candidates* and for *prioritizing*, but the periodic-table thesis needs a **member-count-free definition of "family."**

---

## 4. The crux question (your charge)

> **What defines a kit-family intrinsically — as a design object / region of the coordinate space — independent of how many kits currently populate it?**

And the sub-question **you may not dodge**, because it is where naive answers die:

> If member-count is not the criterion, what prevents "family" from collapsing into "strict cell" — i.e., all 457 cells (or all 470 kits) each declared its own family? There must be a principled distinction between a *family signature* and a *kit*.

A candidate worth pressure-testing (derive it properly, critique it, or replace it):

- A **kit** is a *full* assignment over all 14 coordinates.
- A **family** is a *partial* assignment — a fixed value on the family's **identity coordinates** and a **wildcard** on its **texture coordinates**. Geometrically, a family is a *subcube* of the coordinate space; its members are the kits inside the subcube (0, 1, or many).
- Under this view the entire problem reduces to: **for a given archetype, which coordinates are identity (pinned) and which are texture (wildcard)?** — and that partition must be answerable *without counting members*.

Note the partition is almost certainly **per-family / contextual**, not global: `geometry` behaves as texture *globally* (high near-twin, redundant with delivery) yet is the *defining* coordinate of the Whirlwind family. Any criterion you propose must handle this context-dependence.

---

## 5. Candidate groundings for the identity/texture partition (evaluate, critique, improve, or replace)

These are candidates, not answers. Pressure-test each for whether it is truly member-count-free and whether it recovers the known families:

- **(i) Design-semantic.** Identity coords = those whose change alters the *class fantasy* / how the build plays; texture = flavor only. Member-count-free but judgment-laden — can it be operationalized as a rubric an LLM or designer applies per coord?
- **(ii) Structural.** Near-twin manifold-thickness + inter-coord redundancy (Cramér's V / NMI). Caution: these use pair counts (mild member-dependence). Is there a *purely* intrinsic structural signal (e.g., a coord's role in the delivery→geometry refinement hierarchy)?
- **(iii) Simulation-behavioral (the deepest — evaluate feasibility).** Identity coords = those whose perturbation changes the kit's *behavior/outcome in the fight simulation* (the gamora gauntlet); texture = those that don't move the balance. This grounds "family" in *actual gameplay* rather than data density, and is fully member-count-free. Does it recover Whirlwind's identity coords? Where might it disagree with the structural signal, and which do we trust?

---

## 6. A distinction to make explicit (offered lean — rule on it)

The lift approach conflated three things this reframe cleanly separates:

- **Definition** = the signature (identity-coord assignment). Member-count-free.
- **Validation** = cross-*source* recurrence. If six independent franchises each built the same signature, that signature carves reality at its joints — it is a *natural kind*, not an accident. This is where lift/support legitimately re-enter — as **evidence a family is real**, never as its definition. (Note: cross-*franchise* recurrence is far stronger evidence than raw member count — 6 kits from 6 games ≫ 6 kits from one game's skill tree.)
- **Prioritization** = population / market-salience — which families to build content for first.

Confirm, refine, or reject this three-way split, and state what each implies for the pipeline.

---

## 7. The prize: gaps as predictions

Once families are member-count-free signatures over identity-space, the **unoccupied coherent cells are predicted archetypes**. Address:
- How to enumerate the gaps (the identity-space cells with 0 current members).
- How to rank them — an empty cell is only interesting if its signature is **mechanically coherent** (a real playable build), not a nonsense combination (e.g., `range=melee · delivery=projectile` may be incoherent). What defines *coherence* of an unrealized signature? (This is the inverse of the family-definition question and may share its answer.)
- The player/design consequence: what does the game *do* with a predicted gap?

---

## 8. Deliverable

Write your analysis to `agentic_orchestration/gandalf/design-inputs/2026-07-13-family-definition-analysis.md`, covering:
1. A rigorous, first-principles **definition of "family"** that does not reference member count, and survives the §4 sub-question (family ≠ strict cell).
2. A proposed **member-count-free criterion** for the identity/texture (pinned/wildcard) partition, per-family/contextual, grounded in one or more of §5 — with your reasoning for which grounding you trust and why.
3. How the definition handles **families of size 0 and 1**, and how it **recovers the known families** (validate against Whirlwind at minimum; ideally spot-check Trap and Channeled-Beam via corpus queries).
4. **Method implications:** does this replace lift-ranking, demote it to a validation/prioritization annotation, or something else? What does the production discovery pipeline become?
5. The **gaps/prediction** treatment (§7).
6. An honest **failure-mode critique** of the whole reframe — where might "member count doesn't matter" break, and what safeguards the definition needs.

Keep member-count-thinking out of the *definition* and let it back in only as *evidence*. Report back with a tight summary (the full analysis lives in the file). This is a genuinely open, hard question — the value of this session is independent first-principles derivation, so do not merely ratify the candidate framings above; break them if they deserve breaking.
