# F5 cost-TYPE pass — design note (the P-1a build authority)

> **STATUS:** DESIGN NOTE — CURRENT · authored gandalf 2026-07-11 (SPEC-AUTHOR) per Matt's
> elicitation ruling **P-1(a)**: B1/B2/B3 PROMOTION-AUTHORIZED under **ONE** F5 cost-TYPE pass
> covering all three R-4 reserved Axis-5 bins. Precedent shape: the E4 commitment-axis note
> (`2026-07-10-e4-commitment-axis-design-note.md`) — design grain here; line-level truth lands in
> gamora's math note.
>
> **Consumers:** gamora (LEAD — math note + sim build) · rocket (co-sign — doc-48 assigner,
> packet/enum emission) · star-lord (co-sign — economy columns, MIGRATION.md per ADR-004) ·
> jack-ryan (Gate-2) · KR (sequencing). **Three open forks for Matt** in §9 — the build fires
> after those rulings; nothing else in this note is gated.
>
> **Name lineage:** "F5" = the **pre-registered re-derivation trigger** at batch-2
> derivation-stack §11 (R-4 companion ruling, tracker 2026-07-06 entry): *structural-cost arrival
> = re-derivation event.* This pass IS that arrival; §6 executes the trigger as pre-registered.

---

## §0 — Authority + scope

- **Ruled:** P-1(a), Matt 2026-07-11 — one pass, three bins: **HP-economy (blood magic) ·
  damage-taken-converts (vengeance) · charge-stack (builder/spender)** (canon bin names per the
  Axis-5 R-4 ruling). L1-live 12,960 → **22,680** on completion.
- **Design condition carried from the ruling (LAW for this pass):** B2 requires an **active
  conversion trigger** — the anti-Invoker guard (D3 Invoker stand-there turret play is the named
  anti-pattern; D4's Flay-thorns is the fix pattern: taken damage BANKS, a cast SPENDS).
- **Scope:** design decomposition, invariants, measurement obligations, roster proposal,
  acceptance criteria, seam plan. NOT in scope: line-level sim semantics (mitigation ordering,
  event-vs-magnitude accumulation grain, floor mechanics at `_take_action`) — those are the math
  note's §-questions, listed in §8.

## §1 — What exists already (survey-grain correction — the bench overstated the gap)

The F.3 bench rows were authored at the 2026-07-09 ARPG-canon survey grain. Code inspection
(2026-07-11, this note) corrects them. **What-IS, by layer:**

| Layer | HP-economy (B1) | damage-taken-converts (B2) | charge/builder-spender (B3) |
|---|---|---|---|
| **Generation** — `_assign_doc48_economy` (`season_generation_pipeline.py:320`, doc-48 §3.1 LOCKED G1 table) | **NAMED DEFER IN CODE:** "Crusader HP-economy DEFER → mana" (WIS row) | no signature | **EMITTED TODAY:** DEX melee&spiky → `charge-stack`; STR melee → `rage`; ranged → `combo` |
| **Schema** — `bc_target_player_class.py:306/:387` | `hp` not in enum {mana, rage, charge, focus} | absent | **present** (`rage`, `charge`) |
| **Ability grammar** — `_get_energy_cost` (`ability_grammar.py:340`) | n/a (cost target, not cost size) | absent | **builder-spender cost structure EXISTS:** combo primary = 0-cost, builds +1/cast; spenders cost 3; rage 15–40, built via hit accumulation |
| **Sim** — `combatant.py` `_ENERGY_CONFIGS` (~:427) + T4 | **HP deduction branch EXISTS as T4 overlay:** `t4_cost_resource` (`combatant.py:286-293/:794`, RESOURCE_CONVERSION strategy, Cycle 12 W5; read by fight-engine `_take_action`) | **genuinely missing** — no thorns/retaliation path anywhere in the sim seam | **full charge-stack behaviors LIVE** (gamora `dae0349` 2026-06-12, proxy-kernel Item 4): pool (10, start-empty, no regen), on-hit accumulation, spend-all dispatch, passive held bonus; plus rage (100/empty/0), combo (5/empty/0), focus (100/full/−5·s⁻¹), stamina (150/full/+20·s⁻¹) |
| **Measurement** — Axis 5 | bin reserved, no detection | bin reserved, no detection | bin reserved, no detection — charge/rage/combo kits exist in the population but the classifier cannot SEE them (batch-2 families bootstrapped on mana cells only) |

**Corrections to the bench rows:** B3's block ("all kits flat-resource today") is **false at code
grain** — five energy types run end-to-end, three of them builder-shaped. B1's block ("HP-spend
path doesn't exist") is **partial** — the deduction branch exists; what's missing is kit-NATIVE
cost targeting + the un-deferral of the doc-48 WIS row. B2's block is **true** — the only
genuinely new sim mechanism in this pass.

**Consequence:** F5 is a **completion + generalization + measurement pass, not a from-scratch
resource-model build.** The heavy new work: B2's damage-taken builder, kit-native HP costs + the
floor ruling, the Axis-5 structural detector, the doc-48 table amendment, the §11 F5
re-derivation event, and the three roster kits.

**Build-to-spec flag (OP §3.7):** the doc-48 `DEFER → mana` on the Crusader HP-economy row is
exactly the deferral class the discipline forbids passing through as settled — P-1(a) flips it.
A second named deferral observed in the same table — **"Skirmisher DEFER"** (DEX melee-other →
mana) — is a doc-48 signature gap, NOT an Axis-5 structural bin: **out of F5 scope**, logged in
the tracker so it isn't invisible-by-omission.

## §2 — The decomposition: TWO mechanisms cover THREE bins

The three bins are **behavior-grain** (Axis 5 values the gauntlet measures). Mechanisms are
**design-grain plumbing** (the R-4 two-grain law: one dimension, two grains, never double-count —
so bins need not map 1:1 to mechanisms). The pass builds exactly two:

| Mechanism | Question it answers | Serves |
|---|---|---|
| **A — resource target** | WHERE does the cost land? (`pool` vs `hp`) | B1 |
| **B — builder source** | HOW does the pool fill? (`on_cast` · `on_hit` · `on_damage_taken`) | B3 (exists) + B2 (new value) |

The unification insight that made ONE pass right: **thorns IS a charge-state kit whose builder is
damage-taken** — B2 = mechanism B with `builder_source: on_damage_taken`, and its spender is the
active conversion trigger the P-1a law demands. No third mechanism exists.

## §3 — Mechanism A: kit-native resource target (→ B1, HP-economy)

- **Field:** `cost_model.resource_target ∈ {pool, hp}` at kit grain (packet texture). Default
  `pool` = today's behavior under whatever `energy_type` governs — every existing kit is
  byte-unchanged by construction. `hp` = skill costs deduct from HP.
- **Reuse, don't duplicate:** the fight-engine HP deduction branch already consumed by
  `t4_cost_resource="HP"` becomes the SHARED consumer; the T4 RESOURCE_CONVERSION strategy is
  redefined as a transform that SETS the same field (T4 stays in the catalog — it moves the
  expressed coordinate, per the projection table's CONSTRAINT/TRANSFORM row; the base field is
  what F5 adds).
- **Spend gate symmetry:** `can_use_skill` (`combatant.py:409`) gates casts on the mana pool; the
  `hp` target needs its mirror gate — WHAT that gate does is fork **F5-Q1** (§9).
- **Generation:** doc-48 assigner amendment — the Crusader HP-economy row un-defers (seat per
  fork **F5-Q2**); enum gains the target field (schema + validator `bc_target_player_class.py:387`).

## §4 — Mechanism B: builder-source generalization (→ B3 + B2)

- **Field:** `cost_model.builder_source ∈ {on_cast, on_hit, on_damage_taken}` — the first two
  values NAME what already runs (combo builds per cast; rage/charge-stack build per hit); the
  third is the new value. Generalizing the existing machinery, not building beside it.
- **B2 (damage-taken-converts):** charge pool fills from damage-taken events; output ONLY via
  spender cast — **the anti-Invoker guard is structural**, not tuned: no spender, no output, so
  stand-there turret play is inexpressible by construction. Player feel target: D4 Flay-thorns —
  getting hit is BANKING, the cast is the payoff swing. Event grain (per-hit count vs damage
  magnitude; pre- vs post-mitigation) = math-note question (§8) — genre prior is flat-per-event
  (D3/D4 thorns), which also resists degenerate scaling against many-weak-hits encounters.
- **B3 (builder-spender warrior):** substrate live end-to-end (rage today at STR melee); the F5
  work is roster + measurement grain, plus the composition that makes it the most generative bin:
  **charge × commitment** — E4's `bc_commitment` prices cast-state; a high-commitment charge
  spender (build fast, spend big and slow) is the D3 fury-spender / D2 FCR charge-up composition,
  adjacent to H6 without duplicating it.
- **v1 accumulation = direct resolver writes** (mirror of the per-chain ailment hardwiring at
  `per_skill_emitter.py:772`) with a **NAMED migration**: when the hook layer lands (E4-PHASE-2
  adjacency), `on_damage_taken` becomes a hook-vocabulary trigger and the direct writes migrate.
  Named now so the shortcut is a lineage entry, not drift.

## §5 — Invariants (lattice + projection obligations)

1. **L0 = 972 UNCHANGED.** Economy is never a catalog coordinate — nothing new is sampled; the
   sampler is untouched. (R-1-class discipline: cost-TYPE is the design-grain face of BC-MEASURED
   Axis 5, per R-4.)
2. **L1 arithmetic:** the archive's economy axis is already arity-7 inside 68,040; the pass flips
   live coverage 4-of-7 → 7-of-7: **L1-live 12,960 → 22,680** (the P-1a number). Claims cite
   their level (claim-grain law).
3. **TRIPLE-LAW same-commit obligations bind the BUILD commit** (not this note): the
   `projection-atlas.md` §2 "Resource economy (behavior)" row amends (3 bins RESERVED → LIVE;
   `cost_model` fields noted as the design-grain lever) · the Codex resource-model section gains
   the two fields · the lattice §0 Axis-5 row's live-fraction updates. One commit, all three
   surfaces — an unprojected field is a live alarm.

## §6 — Measurement half: detector 4→7 + the pre-registered F5 re-derivation event

- **Structural-priority detection** (the lattice row's own phrase): classify structural mechanisms
  FIRST — and since `cost_model` is packet truth, detection is **packet-read + behavior-verify**
  (assert the fingerprint shows the declared economy actually expressed), not behavior-inference.
  Mana-substrate kits then fall through to the existing 4-bin behavior classifier. Honest and
  cheap.
- **The §11 F5 trigger FIRES as pre-registered** (this is why the pass bears the name):
  new-branch derivation entry · existing families **bootstrap-stable** (mana-cell derivations are
  not re-opened) · **affected-cut re-ratification only** · elrond #18 registry-honesty consult ·
  no unbacked identity claims at naming. Consult timing per the Discipline-#18 refinement (OP
  §4.2): AFTER the build's baseline gauntlet output exists — the trigger was pre-registered
  exactly so this isn't a consultation-in-the-dark.

## §7 — Roster: K26–K28 (promotion emission; denominator 31 → 34 on acceptance)

| ID | ARPG Genre Canon kit | Seat | cost_model texture | Lineage |
|---|---|---|---|---|
| **K26** | Blood Mage / Martyr | per fork **F5-Q2** (doc-48 prior: WIS) | `resource_target: hp` | PoE Blood Magic; D2 Sacrifice (a PALADIN skill — the martyr lineage is genuine) |
| **K27** | Thorns / Vengeance Knight | STR melee | `builder_source: on_damage_taken` + spender law | D3 Invoker (the anti-pattern), D4 Flay-thorns (the fix) |
| **K28** | Builder-Spender Warrior | STR melee | `builder_source: on_hit`, commitment-composed spender | D3 fury economy; D2 FCR charge-up adjacency (H6-adjacent, not duplicate) |

Cells assigned at emission against the catalog (F.1 column pattern); B1/B2/B3 bench rows retire
on promotion per fork **F5-Q3**. **Emission lands BEFORE the ONE Q14 re-anchor** — P-4(a)'s
operational reading: the re-anchor waits for exactly this trio.

## §8 — Sequencing, seams, acceptance

- **Order:** gamora-led **math note FIRST** (math-before-code), pinning: HP floor semantics at
  `_take_action` under fork F5-Q1 · damage-taken event grain (count vs magnitude; mitigation
  order) · charge-pool arity for K27/K28 vs the existing (10, empty, 0) config · byte-guard scope
  and harness. rocket + star-lord co-sign the math note; then build.
- **Seam split:** gamora `simulation/` (mechanisms, configs, gates) · rocket `generation/`
  (doc-48 assigner amendment, schema/enum, packet emission, grammar cost branches) · star-lord
  economy fingerprint columns + `MIGRATION.md` per ADR-004 — **sequenced AFTER the
  attribution-spine purity pass lands** (same `damage_resolver.py` surface; one pair of hands at
  a time) · jack-ryan Gate-2.
- **KR slots** the build after the attribution pass + whole-v1 push; independent of the walls
  re-spike; before batch-2 promotion emission.
- **Acceptance criteria:** (1) **flat-resource byte-identity** — every existing kit's fight
  outcomes SHA-identical (third wearing of the guard pattern: rocket's mono guard → gamora's
  attribution purity → F5's flat-resource guard) · (2) all three bins DETECTED on the promoted
  kits' gauntlet output · (3) smoke suite green · (4) same-commit TRIPLE-LAW rows (§5.3) ·
  (5) §11 F5 re-derivation artifacts filed (§6).

## §9 — Open forks (Matt rules; the build fires on these)

- **F5-Q1 — HP floor:** **(a) floor-guarded** — the cast is refused when HP can't cover the cost
  (mirrors the `:409` mana gate exactly; PoE Blood Magic precedent; keeps self-KO tails out of
  gauntlet KPIs, which certify against opponent-caused outcomes) · **(b) suicide-legal** — cost
  always paid, self-KO possible (the sharper D2 Sacrifice self-harm fantasy; degenerate-tail risk
  in certification). **Lean (a) for v1**; (b) revisitable as T4 texture once gauntlet evidence
  exists.
- **F5-Q2 — K26 seat:** **(a) WIS Crusader/Martyr** — honors the LOCKED doc-48 G1 seat; D2
  Sacrifice is a Paladin skill; gives WIS (the 3-element pool) a distinctive economy identity;
  holy blood-offering is the fresher fantasy · **(b) INT necromantic blood mage** — D2 Necro
  lineage, shadow-pool affinity; requires a doc-48 re-seat amendment (wider blast radius).
  **Lean (a).**
- **F5-Q3 — roster IDs:** **(a) K26–K28 sequential; bench rows retire on promotion** (one roster,
  one numbering — a persistent B-series would give promoted kits dual identities) · (b) keep
  B-series IDs. **Lean (a).**

---

**Signed:** gandalf, 2026-07-11 — SPEC-AUTHOR. Anchors: P-1(a) elicitation ruling (tracker eighth
entry) · R-4 / batch-2 §8 R1 + derivation-stack §11 F5 (tracker 2026-07-06 entry) ·
`substrate-coordinates.md` §0 Axis-5 row · `projection-atlas.md` §2 · engine cites in §1 (verified
2026-07-11 against source).
