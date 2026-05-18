# 2026-05-17 — gandalf — D11 ARPG-balance advisory (hybrid_mage tuning direction)

**Authority:** Matt L3 2026-05-17 evening — "Invoke Gandalf for decision as to how to tune sprint towards ARPG balance."
**Type:** Pattern B (short) — design advisory; ~0.5-1 day; design steward in lane.
**Predecessor:** rocket v1.12 D10 salvage completion record (37.1% convergence; hybrid_mage structural over-generation identified as residual blocker).

---

## Why this matters

Rocket D10 salvage hit 37.1% convergence (vs >50% target). The residual is concentrated in **hybrid_mage**: even at 9-12 skills (ceiling applied), hybrid_mage maintains 0.63-0.82 WR at the modifier floor due to **multi-element coverage immunity against gauntlet resistance profiles**. Non-hybrid archetypes converge well (controllers 40-100%; physical 100%; hunters 100%; experimental small kits).

Two technical options sit on the table for D11 (rocket's note in completion record):
- (i) Reduce hybrid_mage ceiling to 8-9 skills
- (ii) Redesign element distribution rules

But **neither is a pure-math choice**. The deeper question is design: **what is hybrid_mage supposed to BE in this ARPG, and how should the genre's canon shape D11's tuning lever?** That's your lane.

Matt's explicit directive: gandalf decides how to tune D11 toward ARPG balance. Gamora's D11 math note will translate your advisory into engine-side gen-math + balance-loop changes; rocket's D11 implementation will encode it.

This is also empirically anchored on Matt's queued **L3 #42 (hybrid_mage retain-or-retire)** — your advisory closes that question.

---

## Required reading

1. **Rocket D10 completion record** — `agentic_orchestration/dispatches/2026-05-17-rocket-d10-implementation-and-staged-data-salvage-queued.md` § Completion record + § Known limitations (this is the diagnostic anchor)
2. **Gamora D10 math note** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D10-substrate-coherent-gen-math-note-2026-05-17.md` (substrate-coherent rules; what already shipped)
3. **Gamora v1.5 convergence analysis** — sample-class triad (converged / over-band / under-band) at `reincarnated-engine/output/standard-demo-regen-2026-05-17/v1.5-convergence-analysis/` — empirical hybrid_mage exemplars
4. **Project memory** — `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md` + `project_geometry_palette.md` + `project_role_orientation_taxonomy.md` — current trait/role taxonomy (hybrid is a role-orientation class)
5. **Phase 1 P1 canonical-7 substrate work** — your own `canonical/story/` body of work on substrate coherence + your v1.5 anti-drift framing
6. **A live hybrid_mage sample** — pick one from season_002011-015 D10-curated; inspect skills/element distribution/balance trace; ground the recommendation in actual data
7. **L3 #42 context** — Matt's queued question on hybrid_mage retain-or-retire (search `decisions-log.md` + handoff notes for context)

---

## Scope — five sub-questions to answer

### Sub-Q 1 — ARPG-canon survey: how do successful ARPGs handle multi-element / hybrid builds?

Survey the genre. Evidence-anchor your recommendation in: Path of Exile (chromatic / multi-tree), Diablo 2 (Sorc multi-tree investment), Diablo 4 (Sorcerer split), Last Epoch (Runemaster, multi-element masteries), Grim Dawn (dual-mastery system), Path of Achra (if relevant), Torchlight, others.

Categorize what the genre does:
- (a) **Universally weak** — multi-element is an intentional jack-of-all-trades penalty; specialists win
- (b) **Build-cost gated** — you pay in skill points/passive levels for breadth; viable but expensive
- (c) **Endgame specialized** — only viable at very high investment levels
- (d) **Strong on paper, build-dependent** — mastery curve gates it
- (e) **Genre-rejection** — successful ARPGs simply don't have a "hybrid" archetype

Note which categorization fits Reincarnated's design intent.

### Sub-Q 2 — Hybrid_mage identity: retain, retire, or reshape?

Three paths:
- **(i) Retain as canon ARPG archetype** with proper trade-offs (D11 implements the trade-off lever from Sub-Q 3)
- **(ii) Retire entirely** — admit the engine can't model "hybrid_mage" cleanly at scale; L3 #42 closes "retire"
- **(iii) Rename/reshape** — e.g., "spellblade" / "elementalist" / "chromatic_mage" — different mechanic profile that's structurally tunable; the name we have ("hybrid_mage") is generic, may need replacement

Recommend one. Justify in story/design terms (what does the player FEEL when they play this archetype; what does the world canonically allow; what does the form-library narrative support).

### Sub-Q 3 — IF retained: what's the trade-off lever?

If your Sub-Q 2 answer is (i) retain or (iii) reshape, recommend the trade-off mechanism. Candidates:
- **Lower skill ceiling** (8-9 skills not 12) — rocket's option (i); pure math
- **Element-coverage damage tax** — e.g., -10% damage per element beyond the second; tunable continuous lever
- **No legendary trait pool / weaker per-class intrinsics** — the trade-off is in trait architecture not skill count
- **Higher XP curve / slower scaling** — mid-late game viable, early game weak
- **Lower base stats** (HP / mana / dodge) — survivability tax for offensive breadth
- **Element-specific drawback** (e.g., resistance hole or self-damage at element edges)
- **Multi-element kit composition rule** (e.g., must include "anchor" element that takes 40%+ slots; others are accents)

Recommend one (or a composite of two). Anchor in ARPG-canon evidence from Sub-Q 1.

### Sub-Q 4 — Thematic framing in Reincarnated

Does the substrate-coherent gen-math from D10 align with how hybrids should FEEL in the world? Your narrative voice on:
- Does "hybrid mage" make thematic sense given the canonical-7 substrate map + the form-library accumulation framing?
- Are there form-library / spirit-guide / earth-self framings that naturally explain why a hybrid_mage is constrained vs a specialist?
- Does the answer affect how D11's tuning gets surfaced to the player (UI, spirit guide commentary, narrative beats)?

### Sub-Q 5 — Adjacent archetypes — D11 scope

D11 is the hybrid_mage sprint, but the recommendation may bleed to adjacent archetypes:
- **hybrid_physical** (if it exists) — same multi-element / multi-skill-tree issues?
- **hybrid** (warrior-mage / generalist) — should D11 cover it or is it already converging?
- Any other multi-element existing classes (per gamora v1.5 sample analysis)

Should D11 scope tight on hybrid_mage only, or extend to a broader "hybrid family" tuning pass?

---

## Output — design advisory document

Author at: `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md`

Structure:
1. **Executive recommendation** (1-2 paragraphs; the headline answer to "how do we tune D11")
2. **ARPG-canon evidence base** (Sub-Q 1 survey; cite specific games + specific systems)
3. **Identity decision** (Sub-Q 2 recommendation with justification)
4. **Tuning lever recommendation** (Sub-Q 3; specific enough that gamora can translate to math)
5. **Thematic framing** (Sub-Q 4; story-side implications)
6. **D11 scope guidance** (Sub-Q 5; what gamora math note should cover)
7. **Open questions for Matt** (anything you can't decide unilaterally)
8. **Handoffs**: → gamora (D11 math note inputs); → drax (any UI/narrative surface implications); → jack-ryan (Gate 1 advisory readiness)

Length: target 1000-2000 lines. ARPG-canon evidence section is the load-bearing one; don't skimp.

---

## Out of scope (DO NOT)

- ❌ DO NOT author engine-side gen-math (gamora's lane; you set the design direction)
- ❌ DO NOT modify any code, manifests, or decisions-log (Matt + jack-ryan sign-off paths)
- ❌ DO NOT extend to D12+ (your recommendation may FLAG broader concerns; gamora can scope D11 tight)
- ❌ DO NOT pre-empt L3 #42 lock by Matt — your advisory INFORMS Matt's decision; doesn't make it
- ❌ DO NOT touch jack-ryan's Gate 2 review process (your output goes through Gate 1 advisory readiness check, not Gate 2)

---

## Acceptance criteria

- [ ] All 5 sub-questions answered with evidence
- [ ] ARPG-canon survey grounded in specific game / system examples
- [ ] Tuning lever recommendation is concrete enough for gamora to translate to math (specific magnitudes / mechanics, not "make it weaker")
- [ ] Thematic framing aligned with current canonical-7 substrate + form-library + earth-self body of work
- [ ] D11 scope guidance is explicit (hybrid_mage only vs broader hybrid family)
- [ ] Hive log STATE + HANDOFF → gamora + HANDOFF → jack-ryan (Gate 1 readiness)
- [ ] No new vendor commissions; no code changes; pure design advisory

---

## Coordination

- **Triggers gamora D11 math note** (queued at `agentic_orchestration/dispatches/2026-05-17-gamora-d11-hybrid-mage-tuning-math-note-queued.md`) on advisory completion
- **Parallel-safe with** drax v1.11 SEASON_IDS flip (demo seam) and any post-VS2a M2-M7 work
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **Pattern B short:** target same-day or next-day turnaround; this gates the D11 sprint

---

*Dispatched 2026-05-17 by knight-rider per Matt L3. ~0.5-1 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** gandalf
**Tag:** `gandalf/v1.3-d11-hybrid-mage-tuning-advisory-1` (local; push gated per ADR-006)
**Authored:** `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` — 1046 lines

### Executive recommendation

**Retain hybrid_mage. Reshape via composite lever.** Closes Matt L3 #42 in the **(iii) reshape** direction.

- **(Primary) Quadratic element-coverage damage tax:** `tax_multiplier = 1.0 − α × max(0, n_elements − 2)²` with α=0.07. Universal formula; applies at kit-finalization (Site A); tax coefficient lives in config near substrate-identity declarations (P2-compat).
- **(Secondary) Element-breadth ceiling tightened:** `_ARCHETYPE_ELEMENT_CEILING["hybrid_mage"] = 3` (was 4). 4-element ceremonial path deferred to D12+ as flagged design item.

Tax magnitudes:
- 2 elements: tax_multiplier=1.0 (no tax; comfortable hybrid)
- 3 elements (D11 ceiling): tax_multiplier=0.93 (7% tax; mid-tier playable)
- 4 elements (ceremonial D12+ only): tax_multiplier=0.72 (28% tax; genre-canonical band)

Calibration anchored against v1.5 Class C sample (season_002012 hybrid_mage "Cartographer of Erased Borders"; 4 elements; pre-modifier WR 1.000; floor-pinned). Gamora validates empirically; α may shift ±0.02.

### Five sub-questions answered

1. **ARPG canon (Sub-Q 1):** Category **(b) build-cost gated**. Survey of 13 titles in advisory §§ 2 + 12. Dominant pattern across PoE / LE / D2 / D4 (6 of 13). Reincarnated's chromatic_mage lineage = PoE Elementalist + LE Runemaster + D4 Sorcerer mid-band. D3-launch and Lost Ark explicitly rejected as cautionary tales / contradicting form-library narrative.
2. **Identity decision (Sub-Q 2):** **Reshape.** Retain archetype; tighten mechanical envelope; preserve canonical-7 framing; optional rename to `chromatic_mage` (Matt's call). Retire rejected (form-library requires the integrator-form slot; the technical reason "engine can't model" is empirically wrong — the math is tractable).
3. **Tuning lever (Sub-Q 3):** Composite of quadratic damage tax (primary) + ceiling tightening (secondary). Rejected: pure skill-ceiling (already exhausted at D10); trait-pool penalty (D12+ heavy-weight); XP curve (doesn't fix balance loop); base stats (orthogonal); element-specific drawback (D12+ ceremonial path candidate); anchor-element rule (redundant with ceiling).
4. **Thematic framing (Sub-Q 4):** Aligned across canonical-7 substrate-commitment framework (substrates respond honestly to forms that hold many commitments); form-library Court-of-Forms narrative (chromatic_mage is the integrator-form earned through accumulation); Earth-Self diversity-via-grace (tax is substrate truth-telling, not punishment). Serious-isekai genre register validated against Mushoku Tensei / Solo Leveling / Re:Zero accumulation-cost patterns. Comedic-isekai (Konosuba) rejected.
5. **D11 scope (Sub-Q 5):** **Tight on hybrid_mage.** Universal tax formula but per-archetype ceiling; only hybrid_mage currently has ceiling > 2. Phase-1 P2 hybrid-composer will inherit clean. Flagged-not-blocked adjacencies: ceremonial 4-element path, resistance-hole-at-seam, ailment-overlap diminishing returns, monster-immunity structure, future hybrid roles (controller/caster variants).

### Open questions for Matt (5)

1. Rename `hybrid_mage` → `chromatic_mage` (or `elementalist`)? My recommendation: chromatic_mage. Not blocking.
2. 4-element ceremonial path D12+ pass? My recommendation: defer-but-flag.
3. Accept empirical α calibration by gamora? My recommendation: yes.
4. Tax interaction with D10 DPS density gate (Site A application reduces pre-eval WR)? Flagged for awareness; no decision needed.
5. Future hybrid archetypes (hybrid_physical, etc.) inherit universal tax? My recommendation: yes.

### Acceptance criteria

- [x] All 5 sub-questions answered with evidence
- [x] ARPG-canon survey grounded in specific game / system examples (§ 2 + § 12 appendix; 13 titles covered)
- [x] Tuning lever recommendation concrete enough for gamora (specific formula, α magnitude, application site, worked calibration table, 8-item gamora-readiness checklist)
- [x] Thematic framing aligned with canonical-7 + form-library + earth-self (explicit cross-refs to 7 canonical artifacts)
- [x] D11 scope guidance explicit (tight; flagged adjacencies; out-of-scope enumerated)
- [x] Hive log STATE shipped (entry appended 2026-05-17 ~late)
- [x] HANDOFF → gamora (D11 math note inputs in advisory § 8.1)
- [x] HANDOFF → jack-ryan (Gate 1 readiness in advisory § 8.2)
- [x] HANDOFF → drax (UI/narrative surface follow-on in advisory § 8.3; deferred post-D11)
- [x] No new vendor commissions; no code changes; pure design advisory
- [x] PRE-SIGNAL § 14.1.1 before hive log append (no concurrent writers detected)
- [x] Tag `gandalf/v1.3-d11-hybrid-mage-tuning-advisory-1` (local; push gated per ADR-006)

### Handoffs triggered

- **gamora D11 math note** (queued dispatch `agentic_orchestration/dispatches/2026-05-17-gamora-d11-hybrid-mage-tuning-math-note-queued.md`) — **AUTO-FIRES** on this completion record.
- **jack-ryan Gate 1 advisory review** — parallel-safe with gamora math note.
- **drax surface follow-on** — deferred to post-D11; low priority; flagged in advisory § 8.3.

### Disciplines observed

- #1 (math-before-code): advisory → math note → implementation sequencing correct.
- #11 (empirical inspection): v1.5 Class C as α anchor; gamora validates.
- #12 (semantic shift): tax mechanic flagged for MIGRATION.md.
- #13 (implicit-pillar drift): tax in P2-compat config; not hardcoded magic number.
- R11(b) (round-trip): kit-finalization application site (§ 4.8 Site A) means export sees taxed kits; round-trip clean.

D11 sprint is now **ungated**. Gamora math note auto-fires; jack-ryan Gate 1 parallel-safe; rocket implementation downstream from gamora.

*Completed 2026-05-17 by gandalf.*
