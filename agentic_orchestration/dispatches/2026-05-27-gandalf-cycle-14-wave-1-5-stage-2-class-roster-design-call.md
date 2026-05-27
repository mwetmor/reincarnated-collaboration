# Dispatch — 2026-05-27 — gandalf — Cycle 14 Wave 1.5 Stage 2: class-roster design call + season cardinality canonical decision

**From:** knight-rider
**To:** gandalf (story-and-design steward; design-call partner per Matt Option C ratification)
**Approved by:** Matt 2026-05-27 ratified Option C (substrate-evidence audit → gandalf design call) per scaffold-drift consolidated package § 3.5
**Estimated effort:** ~1-2 days design-call + canonical authoring (per consolidated doc § 3.5 Option C — gandalf curates from elrond Stage 1 audit; not the 3-4 weeks of Option B bottom-up)
**Acceptance:** canonical class roster authored (per-archetype + chain-count + supporting-chain identity + active T4 mechanism design-spec); 14 Stage 1 questions resolved; doc 41 § 4 season cardinality amendment authored (n_kits=40 default per consolidated doc § 3.4); rocket Stage 3 implementation unblocked

## Context

Wave 1.5 Stage 1 elrond substrate class-roster audit landed clean 2026-05-27 at commit `06a3b7f`. Audit produced 34 candidate archetype seeds with substrate-evidence anchoring + BC-axis coverage cross-reference + chain-count + supporting-chain candidate evidence + 14 Stage 2 design-call questions.

This is **Wave 1.5 Stage 2** — the gandalf design call that consumes elrond's substrate-evidence audit + produces the canonical class roster + per-class chain count + supporting-chain identity + active T4 mechanism design-spec. Stage 3 (rocket Wave 1.5 implementation) consumes your output.

**Per consolidated doc § 3.5 Option C path:** "Wave 1 BC-target review pulls archetype-vocabulary from substrate [✅ elrond Stage 1]; **gandalf curates class list** [your task]."

**Elrond's substrate vote summary (per audit § 1):**
- 34 archetype seeds (tighter side of 30-50 range; substrate-natural clustering peaks ~30; no manufacture-to-pad)
- Distribution: STR-martial-heavy (10 — over-saturated 2.7×) / STR-ranged (3 — thin) / DEX-martial-light (7) / DEX-ranged (5 — rich form vocabulary) / INT-caster-arcane (4) / WIS-caster-faith (4) + § 2.7 support-archetype substrate (184 rows — shield/banner/talisman/horn)
- Chain-count vote: ~65% 3-chain / 15% 4-chain / 12% ambiguous / 9% thin-fold-candidate (substrate leans concentrated-identity 3-chain)
- Strongest supporting-chain candidate: DEX-Shield-Skirmisher (17 shield rows; DEFENSIVE_CONVERSION fit per doc 40 § 8.4)

**Critical BC-axis gaps surfaced by elrond:**
- INT-AoE near-empty (canonical fireball/chain-lightning mage ABSENT from substrate)
- INT-high-tempo + WIS-high-tempo + WIS-melee-light (monk) + STR-thrown-ranged (barbarian javelin) all 0 rows
- DEX-AoE thin (33 rows)

**Critical BC-axis over-saturation:**
- STR-melee-cleave-medium-tempo: 5 competing seeds
- DEX-ranged-single-medium-tempo: 4 competing seeds
- INT-mid-ranged-single-medium-tempo: 3 competing seeds

Gandalf's task: curate final class roster from this substrate evidence + author design-spec for Stage 3 rocket implementation. Substrate vote is binding at the geometry layer per Discipline #25; semantic interpretation (which archetypes ship; how they map to classes) is gandalf design call.

**Composition with Cycle 14 work:**
- Discipline #40 LOAD-BEARING (your prior canonical write `b282966`): class-roster decision is canonical lock per § 40 (a); SCAFFOLD-WITH-PENDING-DECISION not acceptable for class roster — must be ratified canonically
- Doc 40 § 8.3 amendment + D66 + D69 + D83 + supporting chain Option C: these are the architectural commitments your class-roster design-spec implements
- Wave 5 fresh roster generation (per Q9 disposition): Stage 3 implementation feeds Wave 5; your class roster IS the Cycle 14 production season's character roster

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` — **PRIMARY SUBSTANTIVE INPUT** (elrond Stage 1 audit; 34 seeds + 14 questions)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 (Wave 1.5 substantive spec) + § 3.4 (season cardinality canonical decision) + § 3.5 (Option C path)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` § 2 Dispatch 2 (Wave 1.5 routing source)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains AMENDED 2026-05-27) + § 6.6.1 (supporting chain Option C; class-intrinsic) + D66 (one T4 unlocked at a time) + D69 (branching gated by depth ≥4) + D83 (T4 count = chain count − 1)
- `canonical/41-progression-framework-2026-05-27.md` § 2-3 (L50 hybrid; § 4 will receive season cardinality amendment)
- `canonical/46-concentration-architecture-2026-05-27.md` (Wave 1 architectural foundation; doc 46 Layer 1-7 implemented at `98b68aa`)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile — your class-roster respects per-attribute archetype identity)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (substrate composition reference)
- `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md` (Fix C audit; caster-faith mace 62% pending HYBRID remediation per your prior verdict `38d0d73`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #40 (your canonical write at `b282966`)
- `.claude/skills/reincarnated-gandalf-operating-procedure` (Pattern A-deep substantive verdict mode appropriate)
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-canonical-doc-format` (doc 41 § 4 amendment authoring)

## Math-before-code

This is design-spec authoring (your seam). The "math" deliverables are the canonical design-spec content + doc 41 § 4 season cardinality amendment. Rocket Stage 3 implementation consumes your design-spec + authors 3 implementation math-notes per consolidated doc § 3.3.

Your design-spec should include for each class:
- Class identity (name + thematic anchor + cultural lineage/register)
- Per-class chain count (3 or 4) with substrate-evidence rationale
- Per-class supporting chain identity (T3-cap; class-intrinsic per doc 40 § 6.6.1 Option C) with substrate-evidence rationale
- Per-class active T4 mechanism (runtime-active marker per D66; respec-via-legendary-trigger per D65)
- BC-axis primary coverage (which cells does this class cover)

## Cross-seam contract change? (Principle 6 gate)

**NO** for canonical doc amendments (doc 41 § 4 season cardinality + class-roster canonical doc — gandalf seam; no inter-seam fixture dict change at design-spec layer). Stage 3 rocket implementation WILL change character JSON schema (per consolidated doc § 3.6: `active_t4_chain` + `supporting_chain` fields); MIGRATION.md at Stage 3.

**Round-trip:** not applicable for Stage 2 design-spec authoring; round-trip clause at Stage 3 implementation.

## Scope

### Item 1 — Class roster curation (~6-12 hrs design call equivalent)

- [ ] Read elrond Stage 1 audit in full; consume 34 seeds + BC-axis coverage + chain-count vote + 14 questions
- [ ] Resolve **Q-S2-1 cardinality** — how many classes in Cycle 14 v1 roster? Substrate has 34 seeds + 184 support-archetype rows; consolidated doc § 3.4 recommends Option 2 n_kits=40 default (within multi-fire extension cap 50). Class count ≠ kit count (per-class chain combinations produce multiple kits per class). Recommend ~8-14 classes (substrate-supported + thematic coherence).
- [ ] Resolve **Q-S2-2 fold-vs-distinct** — STR-melee over-saturation (5 cleave seeds): fold into 1 archetype (Barbarian — variants by weapon choice) OR ship multiple distinct (Berserker / Slayer / Reaver / Tribal Warrior / etc.)? Decide + record rationale.
- [ ] Resolve **Q-S2-3 substrate-gap closure** — INT-AoE empty (canonical fireball mage absent): commission elrond substrate enrichment OR design class without substrate anchor (gandalf-authored thematic identity) OR drop INT-AoE coverage v1 (defer to v1.1). Substrate-led discipline (Discipline #25 + Path A architectural commitment) prefers enrichment OR defer; do NOT design without substrate anchor.
- [ ] Resolve **Q-S2-4 lineage architecture** — substrate named pool is 95% fantasy_generic; lineage-discriminator surfaced. Cycle 14 v1 lineage palette: fantasy-only OR mixed historical+fantasy? Decide + record (composes with cultural-lineage discipline + AI-tell mitigation per D7).

### Item 2 — Per-class chain count + supporting-chain identity (~4-8 hrs)

- [ ] For each curated class:
  - Assign chain count (3 or 4) per substrate evidence + thematic identity (Q-S2-5)
  - Identify supporting chain (T3-cap; class-intrinsic theme) per substrate evidence (Q-S2-6)
  - Cross-class supporting-chain sharing (Q-S2-7) — do any classes share supporting chain identity (e.g., multiple martial classes share "Iron Discipline" supporting chain) OR all unique? Decide per substrate evidence + design coherence

### Item 3 — Active T4 mechanism design-spec (~2-4 hrs)

- [ ] Design-spec for D66 active-T4-at-a-time discipline:
  - Runtime-active marker (`active_t4_chain: str` per consolidated doc § 3.3 Item 5)
  - Switching mechanism (legendary-trigger respec per D65)
  - Validation rules (only one T4 capstone active at a given moment; supporting chain has no T4)
  - Cross-seam: gamora damage_resolver consumes `active_t4_chain` per consolidated doc § 3.6 (Stage 3 MIGRATION)

### Item 4 — BC-cell coverage finalization (~2-4 hrs)

- [ ] Resolve **Q-S2-8 INT-AoE gap** — per Q-S2-3 disposition; cross-reference
- [ ] Resolve **Q-S2-9 DEX-firearm class architecture** — substrate has firearm/gunslinger/shotgun/MG variants; one class with weapon variants OR multiple distinct classes?
- [ ] Resolve **Q-S2-10 over-saturated STR-melee** — per Q-S2-2 fold-vs-distinct disposition; cross-reference
- [ ] Resolve **Q-S2-11 cross-attribute hybrids** — does Cycle 14 v1 ship any cross-attribute hybrid classes (e.g., Spellsword INT+DEX; Battle Mage STR+INT)? Composes with doc 47 § 2.1 hybrid scaling type + Option C cross-attribute ω-penalty (`OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80` per your prior verdict `da16652`). Substrate has hybrid rows (`STR_or_DEX` proxy_attribute_class etc.); design call to include or defer to v1.1.

### Item 5 — Substrate-enrichment commission candidates (Q-S2-12 through Q-S2-14)

- [ ] Resolve **Q-S2-12 INT-AoE enrichment** — if Q-S2-3 chooses commission, route elrond Mode A research or Mode B targeted crawl for canonical fireball/chain-lightning/blizzard mage substrate
- [ ] Resolve **Q-S2-13 lineage re-tagging on named pool** — substrate named pool 95% fantasy_generic; targeted re-tagging pass for historical lineage candidates? KR routes elrond dispatch if chosen.
- [ ] Resolve **Q-S2-14 hybrid-attribute substrate** — if Q-S2-11 ships hybrid classes, route legolas Mode B targeted crawl for hybrid-archetype substrate

### Item 6 — Doc 41 § 4 season cardinality amendment (~1-2 hrs)

- [ ] Author doc 41 § 4 amendment per consolidated doc § 3.4:
  - Season cardinality: Option 2 (multi-fire extension to 30-50 base kits) for Cycle 14 Wave 5
  - Default `n_kits=40` (within multi-fire extension cap 50)
  - Gauntlet PASS rate target: ~70-80% pass through (40 base → ~28-32 surviving)
  - Output canonical decision STATUS-stamped per canonical-doc-format skill
- [ ] Cross-reference doc 46 Layer 6 cohesion architecture + doc 47 § 3 weapon profile + class roster (Item 1) for character-per-class distribution

### Item 7 — Class-roster canonical doc authoring

- [ ] Author canonical class-roster doc at `canonical/48-cycle-14-class-roster-2026-05-27.md` (or your OP-preferred location) capturing:
  - § 0 STATUS + authority + companion docs
  - § 1 Class list with per-class identity + thematic anchor + cultural lineage/register
  - § 2 Per-class chain count + supporting chain + active T4 mechanism (Stage 3 rocket implementation input)
  - § 3 BC-axis coverage mapping
  - § 4 Substrate-evidence anchoring per class (cross-reference elrond Stage 1 audit § 2 seed numbers)
  - § 5 Substrate-enrichment commissions (if Q-S2-12/13/14 surface)
  - § 6 Stage 3 implementation guidance for rocket
  - § 7 Cross-references to doc 40 + doc 41 + doc 46 + doc 47 + framing brief
- [ ] Update `canonical/00-ground-state.md` § 1 registration per canonical-doc-format skill

### Closure

- [ ] Discipline #40 obligation: class roster decision is CANONICAL LOCK (option (a) per § 40), not SCAFFOLD-WITH-PENDING-DECISION. doc 48 ratifies the decision.
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)
- [ ] Note for KR: Stage 3 rocket Wave 1.5 implementation dispatch fires after this Stage 2 lands; KR consumes doc 48 + 14 Q-resolutions

## Acceptance criteria

- [ ] All 14 Stage 1 questions resolved (Q-S2-1 through Q-S2-14)
- [ ] Class roster authored at canonical doc with substrate-evidence anchoring per class
- [ ] Per-class chain count + supporting chain identity + active T4 mechanism design-spec complete
- [ ] BC-axis coverage finalized (gaps + over-saturation addressed)
- [ ] Substrate-enrichment commissions surfaced (if needed) for KR routing
- [ ] doc 41 § 4 season cardinality amendment authored (n_kits=40 default)
- [ ] canonical/00-ground-state.md § 1 registration updated
- [ ] Completion record appended; commit + push
- [ ] Round-trip: not applicable (Stage 3 implementation handles cross-seam contract change)

## Out of scope (explicit non-goals)

- Do NOT implement Wave 1.5 (Stage 3 / rocket territory)
- Do NOT touch substrate library DB (elrond seam; substrate-enrichment via separate dispatch if Q-S2-12/13/14 surface)
- Do NOT amend doc 40 / doc 46 / doc 47 beyond what consolidated doc § 3 amendments already define (existing canonical commitments preserved)
- Do NOT touch caster-faith remediation (separate HYBRID verdict `38d0d73`; awaiting Matt sign-off on Cycle 15 deferral commitment)
- Do NOT touch character JSON output schema (rocket Stage 3 seam)
- Do NOT enter Pattern B sustained dialogue with Matt (this is Pattern A-deep substantive verdict mode; Matt-level escalation only if you can't resolve a question from elrond audit + canonical docs alone)

## Open questions for gandalf (additional to elrond's 14)

- **Q-S2-15:** If Q-S2-11 ships hybrid classes, how does this compose with rocket Wave 1 LegendaryCapabilityScope enum (5 local scopes; no character_wide/chain_wide)? Hybrid classes may need scope extension OR the 5 local scopes are sufficient. Gandalf decides + records rationale per doc 46 Layer 3.
- **Q-S2-16:** Class-roster naming convention — do classes get human-readable names (e.g., "Berserker") OR fantasy-evocative names (e.g., "Wolfborn") OR Latin/genre-trope names? Composes with D7 AI-tell discipline (Wave 3 cohesion-judge LLM consumes class names). Decide + record.
- **Q-S2-17:** Per-class equip restrictions — do classes have weapon-family restrictions (Barbarian must equip martial-heavy; Mage must equip caster-arcane) OR are they substrate-suggested with player flexibility? Composes with doc 47 § 3 + substrate weapon binding output per Wave 0.5.

## References

- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` (Stage 1 substantive input)
- `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 3 + § 3.4 + § 3.5
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 + D66 + D69 + D83
- `canonical/41-progression-framework-2026-05-27.md` § 4 (amendment target)
- `canonical/46-concentration-architecture-2026-05-27.md`
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 + § 2.1
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Discipline #40 (your prior canonical write `b282966`)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-caster-faith-remediation-verdict.md` (HYBRID verdict; caster-faith composes with Item 4 BC-cell coverage)
- Hive-mind protocol § 4 (decision-routing) + § 7 (math hotspots; class-roster is design hotspot)

## Sequencing note

After this dispatch lands, KR authors **Stage 3 (rocket Wave 1.5 implementation)** consuming your class roster + per-class chain count + supporting-chain identity + active T4 mechanism design-spec + 3 implementation math-notes per consolidated doc § 3.3 items 1-5 (chain count + T4 count rule + supporting chain + branching + active T4 marker). Stage 3 ships per-class chain count + active T4 runtime marker; bundles Fix B + Fix B-prime per gandalf caster-faith verdict `38d0d73` if Matt signs off on HYBRID approach (pending).

Cycle 14 substrate state at Stage 2 firing time:
- Wave 0 ✅ / Wave 0.5 ✅ / Wave 0.5 follow-on ✅ / Wave 1 ✅
- Substrate sidecar Dispatch 1 ✅ / Discipline #40 ✅ (LOAD-BEARING)
- Wave 1.5 Stage 1 ✅ (`06a3b7f`)
- Stage 2 ← THIS DISPATCH
- Wave 1.5 Stage 3 + Wave 2 + Wave 3 + Wave 4 + Wave 5 queued
