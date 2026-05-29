# Amendment 7a Spec — Per-Chain Element Wiring Fix for Behavioral Hybrid

> **STATUS:** CURRENT — Cycle 14 cascade-resumption-3 Amendment 7a fix-pack spec. Authored by gandalf 2026-05-29 evening late post-Amendment-7-empirical-surface. Routes to rocket via KR halt + Amendment 7a dispatch sequence.
>
> **Composes with:** Amendment 7 (E4c + hybrid layer; shipped at engine commit `8d5be1b`). Amendment 7a is a fix-pack closing the Instance 6 #4 behavioral-vs-structural gap surfaced post-Amendment-7-close.

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward)
**Authorized:** Matt 2026-05-29 evening late ("sent to KR" + prior Path B authorization verbatim)
**Composition:** Amendment 7 fix-pack; cascade-resumption-3 work program; pre-Phase-5 halt

---

## 0. TL;DR

Amendment 7 (commit `8d5be1b`) shipped Layer 1 (E4c element coverage; behavioral; all 8 elements at primary mono) + Layer 2 (hybrid 17.5%; behavioral at metadata layer) + **Layer 3 (chain assignment) shipped as structural-only at skill emitter layer.** `chain_2.element` on `ChainSpec` is set for hybrid kits, but `emit_skills_for_kit` does not read it — the function consumes `SkillEmissionConfig.element` (single field) and produces 12 skills with primary element only.

**Amendment 7a fixes:** extend `SkillEmissionConfig` with `chain_elements: dict[str, str] | None`; amend `emit_skills_for_kit` to resolve per-chain element; thread chain_elements at the call site for hybrid kits.

**Effect:** Layer 3 graduates from structural-only to behavioral. Hybrid kits' chain_2 emits 4 skills with skill.element = secondary; chain_1 + supporting emit 8 skills with skill.element = primary. Player-facing experience matches design intent.

**Cost:** ~30-60min rocket; ~5-10 new tests; backward-compatible (chain_elements optional; default None preserves existing mono behavior).

---

## 1. Problem statement (empirical surface)

### 1.1 What shipped vs intent

**Amendment 7 spec § 2 Layer 3 intent:** for hybrid kits, chain_1.element = primary; chain_2.element = secondary; supporting_chain.element = primary. Hybrid kits produce CHAIN-LEVEL CONTENT VARIANCE (chain_2's 4 skills differ from chain_1's 4 skills at element layer).

**Amendment 7 implementation (commit `8d5be1b`):**
- `ChainSpec.element` field IS assigned per chain (chain_2 = secondary for hybrid) ✅
- `KitCandidate.secondary_element` IS set for hybrid kits ✅
- `KitCandidate.is_hybrid` flag IS set ✅
- **BUT:** `emit_skills_for_kit` at `season_generation_pipeline.py:901-907` is called once per kit with `SkillEmissionConfig(element=primary_element, ...)` — single element threaded; ChainSpec.element is never read by the emitter
- **Result:** all 12 skills emitted with skill.element = primary; secondary element exists as KitCandidate metadata only; chain_2's 4 skills are identical-content to chain_1's at element layer

### 1.2 Pre-Phase-5 halt rationale

If Phase 5 fires under current state:
- LLM Wave A faction labels operate on substrate where hybrid kits look behaviorally mono at skill content layer
- LLM F-C cohesion judge cannot differentiate hybrid kits via skill content (all skills primary-element-named)
- LLM Wave B kit names generated against partly-broken substrate
- ~$50 LLM cost spent; if discovered post-Phase-5, re-fire burns $50 cap twice

**Halt-now cost:** ~1hr (Amendment 7a fix + Phase 2-4 re-fire). **Halt-now value:** $50 LLM spend protected; Instance 6 #4 pattern interrupted at cheapest refutation layer (pre-Phase-5).

### 1.3 Cumulative Disc #42a Instance 6 pattern — 4 surfaces in one work program

1. Wave B phantom-component → CLOSED
2. Variant Pareto-dominance → pre-ratified per Recognition record A3
3. Amendment 6 Sub-fix 3 emit_skills_for_kit deterministic namespace-only → PASS-with-INFO at Gate-2
4. **Amendment 7 hybrid chain_2 metadata-only at skill emitter → Amendment 7a fix-pack target**

4 surfaces in one work program is no longer incidental. **Systemic Phase-2-generation tendency: ship structural variation without behavioral variation when spec language permits both interpretations.** Canonical-write material for Cycle 14 wave-close. Amendment 7a interrupts the pattern at cheapest pre-fire layer.

---

## 2. Amendment 7a mechanism (3 changes)

### 2.1 Extend `SkillEmissionConfig` (`per_skill_emitter.py`)

```python
@dataclass
class SkillEmissionConfig:
    character_id: str
    element: str                                      # PRIMARY element (existing; semantics unchanged)
    bc_attribute: str
    bc_amplitude: str
    chains: list[str] = field(default_factory=lambda: ["chain_A", "chain_B", "chain_C"])
    tiers_per_chain: list[int] = field(default_factory=lambda: [1, 2, 3, 4])
    chain_elements: dict[str, str] | None = None    # NEW: optional per-chain override; None = use config.element for all chains
```

**Backward compatibility:** existing callers (Phase 3 deserialization, telemetry re-emission, mono kits at Phase 2) pass no `chain_elements` → default None → existing mono behavior preserved. **No existing test should fail.**

### 2.2 Amend `emit_skills_for_kit` inner loop (`per_skill_emitter.py:400+`)

```python
for chain_id in config.chains:
    chain_letter = _CHAIN_LETTER.get(chain_id, chain_id[-1].upper())
    chain_roles = _CHAIN_ROLE.get(chain_id, {t: "primary_attack" for t in config.tiers_per_chain})

    # NEW: resolve per-chain element (Amendment 7a)
    chain_elem = (
        config.chain_elements.get(chain_id, config.element)
        if config.chain_elements is not None
        else config.element
    )

    for tier in config.tiers_per_chain:
        ...
        # Use chain_elem (NOT config.element) for placeholder name + skill.element field
        placeholder_name = (
            f"{chain_elem.title()} Chain {chain_letter} - T{tier} {role.replace('_', ' ').title()}"
            if tier < 4
            else f"{chain_elem.title()} Chain {chain_letter} - T4 Capstone"
        )
        # ... skill = Skill(..., element=chain_elem, ...)
```

**Affected fields in emitted Skill:** `skill.element` + placeholder name string (per math doc § 6). Tier coefficient, damage scaling, geometry, cooldown — these depend on `bc_attribute` / `bc_amplitude` / `tier` / `role`, NOT element — so they remain unchanged per chain (correct architectural separation).

### 2.3 Thread chain_elements at call site (`season_generation_pipeline.py:898-907`)

```python
# Amendment 7a: for hybrid kits, build per-chain element map; for mono, pass None
if sample_is_hybrid and sample_secondary_element is not None:
    sample_chain_elements = {
        "chain_A": sample_element,                # chain_1 = primary
        "chain_B": sample_secondary_element,      # chain_2 = secondary (HYBRID CHAIN)
        "chain_C": sample_element,                # supporting = primary
    }
else:
    sample_chain_elements = None  # mono kit → existing behavior

sample_emission_config = SkillEmissionConfig(
    character_id=sample_character_id,
    element=sample_element,                      # PRIMARY (kit.element semantics preserved)
    bc_attribute=enc.bc_attribute,
    bc_amplitude=enc.bc_amplitude,
    chain_elements=sample_chain_elements,        # NEW: per-chain override for hybrid
)
sample_skills = emit_skills_for_kit(sample_emission_config)
```

**Important chain_id-to-ChainSpec mapping verification:** before implementing, rocket must verify the chain_id naming convention used by both `_build_chain_specs` (line 463+) and `emit_skills_for_kit` (default chains: `["chain_A", "chain_B", "chain_C"]`). The Amendment 7 implementation maps `chain_1 → primary; chain_2 → secondary; supporting → primary` — the chain_id labels in `emit_skills_for_kit` ("chain_A", "chain_B", "chain_C") must align with the ChainSpec chain_id values ("t4_chain_1", "t4_chain_2", "supporting_chain"). If labels differ, rocket implements a consistent mapping. The DESIGN INTENT is unambiguous: chain_2 = the T4 chain carrying the secondary element for hybrid kits.

---

## 3. Test acceptance criteria

### 3.1 Behavioral hybrid verification (NEW tests; ~5-10)

| Test | Expected output |
|---|---|
| Hybrid kit's chain_2 skills | All 4 chain_2 skills have `skill.element = secondary_element` (NOT primary) |
| Hybrid kit's chain_1 skills | All 4 chain_1 skills have `skill.element = primary_element` |
| Hybrid kit's supporting chain skills | All 4 supporting chain skills have `skill.element = primary_element` |
| Hybrid kit's placeholder names | chain_2 names use secondary element label ("Shadow Chain B - T1 ..." for fire-primary-shadow-secondary hybrid kit) |
| Mono kit (no hybrid) | All 12 skills have `skill.element = config.element` (existing mono behavior preserved) |

### 3.2 Backward compatibility verification

| Test | Expected output |
|---|---|
| Existing Phase 3 deserialization | `emit_skills_for_kit(SkillEmissionConfig(...))` without chain_elements field works identically to pre-Amendment-7a |
| Phase 5 cohesion telemetry re-emission | Hybrid kits produce content-distinct chain_2 skills; downstream consumers see secondary element via `skill.element` field |
| 554 existing Amendment 7 tests | All pass without modification (backward compat) |

### 3.3 Population element coverage (Amendment 7 acceptance preserved)

| Test | Expected output |
|---|---|
| All 8 elements at primary mono layer | Preserved per Amendment 7 § 7 (unchanged) |
| Hybrid rate 6-13 of 54 | Preserved per Amendment 7 § 7 (unchanged) |
| Hybrid chain_2 element distribution | All 8 elements appear as `skill.element` at chain_2 layer across the ~9-13 hybrid kits in a 54-kit population (chain-level element coverage now genuinely behavioral) |

---

## 4. Composition + non-impact

### 4.1 Composes cleanly with

- **Amendment 6** (S7 deepcopy + Pareto-2 + S8 Bound 4): unchanged; Amendment 7a operates at skill emitter layer, not substrate/Pareto layer
- **Amendment 7** Layer 1 (E4c element coverage; behavioral): preserved
- **Amendment 7** Layer 2 (hybrid 17.5% rate): preserved; rate semantics unchanged
- **Amendment 7** Layer 3 (chain assignment): graduates from structural-only to behavioral via Amendment 7a wiring
- **Amendment 8** (Matt-gate retired + $50 cap): preserved; halt-now-fix pattern operates pre-Phase-5 so $50 cap is protected
- **Canonical doc 47 § 4.6 ELEMENT_CONVERSION strategy:** hybrid kit's chain_2 now genuinely carries secondary element at skill content — ELEMENT_CONVERSION Layer 2 T4 strategy operates on real content-level hybrid substrate

### 4.2 Does NOT modify

- Phase 2 BC cell discovery
- Substrate weapon binding (Amendment 6 Sub-fix 1)
- Pareto-2 partition (Amendment 6 Sub-fix 2)
- Skill content tier coefficients / damage / geometry / cooldown / cast time (those are bc_attribute/bc_amplitude/tier/role-driven, not element-driven)
- Wave A / F-C / Wave B prompt templates (unchanged; downstream consumes the now-correct hybrid skill content)
- Cycle 14 wave-close canonical-write deferred list (Amendment 7a is in-cycle implementation; wave-close canonical-writes deferred separately)

---

## 5. KR routing instructions

**Dispatch sequence:**

1. **KR confirms halt** of rocket production fire at current phase (pre-Phase-5)
2. **KR dispatches Amendment 7a to rocket** with reference to this spec at `agentic_orchestration/gandalf/notes/2026-05-29-amendment-7a-per-chain-element-wiring-fix-spec.md`
3. **Rocket implements** § 2 changes; ~30-60min work; auto-commit per CLAUDE.md addendum
4. **Jack-ryan Gate-2 quick review** of Amendment 7a (composition verification; backward compat verification; behavioral hybrid acceptance)
5. **Rocket re-fires Phase 2-4** post-Amendment-7a-Gate-2-PASS (~50sec; $0 LLM)
6. **Phase 5 entry** without Matt-gate per Amendment 8; $50 cap monitoring per Amendment 8
7. **Continue cascade** per existing Phase A2 sequence

**Phase 2-4 re-fire required:** Amendment 7a changes skill content for hybrid kits; Phase 2 base kit candidates must re-emit with corrected skills before Phase 5 LLM substrate ingestion.

**No Matt-surface required:** Amendment 7a is in-scope cascade-resumption-3 work + fix-pack for Amendment 7 already-Matt-authorized; routes via hive-mind decision routing (Matt 2026-05-23 directive). Matt-surface only at $50 cap approach OR Gate-2 BLOCK OR additional material-fail per Amendment 4 enumeration.

---

## 6. Discipline composition

| Discipline | Application |
|---|---|
| **Disc #41 substrate-led discipline** | Hybrid intent is behavioral per Matt design call authorization; metadata-only fails substrate-led at content layer. Amendment 7a restores substrate-led discipline at chain content layer. |
| **Disc #42a framing-audit (Q1-Q6)** | Q3 catch: "if refutation evidence exists, refine framing rather than execute as-framed" — fired POST-Amendment-7-close via empirical engine investigation (Matt's diversity-range question + my code reading). Caught Instance 6 #4 at pre-Phase-5 layer. **First case in cascade-r3 where framing-audit Q3 fires AFTER ship but BEFORE downstream cost (Phase 5 LLM) burns.** Cycle 14 wave-close canonical-write candidate: "framing-audit applies post-ship pre-downstream-cost at cheapest-empirical-refutation layer." |
| **Disc #18 math hotspot consultation** | Per-chain element wiring is a content-layer math hotspot at Phase-2-skill-emitter; Amendment 7a operationalizes spec disambiguation at the implementation layer. |
| **Disc #19 background processes** | Halt + fix + re-fire pattern compatible with KR-coordinated parallel work (no cross-dispatch resource conflict). |
| **Recognition → empirical validation → commit** | Recognition: design intent for behavioral hybrid (Matt verbatim "we actually want to promote hybrids"). Empirical validation: post-ship code reading caught structural-only gap. Commit: Amendment 7a interrupts the pattern at cheapest pre-downstream-cost layer. |

---

## 7. Cumulative Instance 6 pattern observation — Cycle 14 wave-close canonical-write candidate

**Pattern observed at 4 surfaces in cascade-resumption-3:**

1. Wave B phantom-component (structural without behavioral wire-up) — CLOSED via S5/S5b
2. Variant Pareto-dominance (structural without behavioral variance signal) — pre-ratified via Recognition record A3 H0 inheritance
3. Amendment 6 Sub-fix 3 emit_skills_for_kit deterministic (structural namespace without behavioral content) — PASS-with-INFO; jack-ryan named "structural-vs-behavioral variation gap"
4. **Amendment 7 hybrid chain_2 (structural metadata without behavioral content)** — Amendment 7a fix

**Hypothesis (worth canonical-write at wave-close):** Phase-2-generation seam has a systemic tendency to ship structural variation without behavioral variation when spec language permits both interpretations. Mitigation candidates:
- **Spec discipline:** mandate explicit "behavioral OR structural" labeling on any variation-introducing amendment
- **Implementation discipline:** Disc #42a Q-extension — Q7 "does the implementation route the variation through the BEHAVIORAL execution layer (vs. metadata-only)?"
- **Test discipline:** acceptance criteria require ≥1 test asserting behavioral effect (Pareto-visible OR content-distinct OR downstream-consumer-observable) for any variation-introducing change

Jack-ryan + gandalf canonical-write at Cycle 14 wave-close. Discipline candidate #50 (or Disc #42a Q7 amendment).

---

## 8. Sign-off

**Authored:** gandalf (story-and-design steward) per Path B authorization 2026-05-29 evening late
**Election authority:** Matt 2026-05-29 evening late ("halt now, fix-then-resume" implicit authorization via "sent to KR" verbatim)
**Composition:** Amendment 7 fix-pack; pre-Phase-5 halt; cascade-resumption-3 work program

**For KR:** confirm rocket halt; dispatch Amendment 7a to rocket with reference to this spec; route through jack-ryan Gate-2; resume cascade post-fix per § 5 sequence.

**For rocket:** implement § 2 (3 changes); add tests per § 3; verify acceptance criteria; auto-commit per CLAUDE.md addendum (do NOT push).

**For jack-ryan Gate-2:** verify § 3.1 behavioral hybrid acceptance + § 3.2 backward compatibility + § 3.3 population element coverage preserved + Amendment 6 composition unbroken.

**For Cycle 14 wave-close:** § 7 cumulative Instance 6 pattern observation worth canonical-write attention; § 6 framing-audit Q3 post-ship pre-downstream-cost application worth canonical-write attention.
