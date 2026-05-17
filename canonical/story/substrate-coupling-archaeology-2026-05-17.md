# Substrate Coupling Archaeology — 2026-05-17

**Authority:** gandalf (story-and-design steward), commissioning Explore agents for systematic engine walks.
**Status:** audit-traceable archaeology record of substrate-keyed coupling sites in the Reincarnated engine, captured at the substrate-expansion + diversity-architecture decision commitment moment.
**Companion artifacts:** `archetype-coupling-archaeology-2026-05-17.md` + `wide-net-coupling-archaeology-2026-05-17.md`. This doc covers **substrate-keyed coupling** specifically (sites where canonical-four element labels are hardcoded).
**Consumers:** jack-ryan engineering-disciplines pass; knight-rider Phase-1 P1 dispatch cascade sequencing; rocket / gamora / star-lord implementation reference; Matt audit trail.

---

## § 0 — Why this exists

Before committing to canonical-four → canonical-7 substrate expansion + the five-layer diversity architecture, Matt requested coupling archaeology — specifically: *"go into the depths of the engine mechanics where the Balrogs roam and see if you can find out an answer for me [on substrate-coupling]."* The first archaeology pass (substrate-keyed) ran 2026-05-17 against `reincarnated-engine/src/reincarnated/`.

This doc is the record of what was found.

---

## § 1 — Headline summary

- **Total substrate-keyed coupling sites found:** 13
- **HIGH-severity (convergence-forcing if unaddressed):** 2
- **MEDIUM-severity (silent default → convergence risk):** 9
- **LOW-severity (edge cases):** 2
- **GOOD PATTERNS (registry-driven; no action):** 2
- **Form-bias recovery status:** registry-aware at substrate-set scope; LLM naming layer has implicit convergence fallback (Coupling #8)
- **LLM prompt-layer status:** Stage 3 cipher migration successfully hides canonical-four from LLM prompts; grouping-label fallback creates implicit coupling

---

## § 2 — HIGH-severity sites

### Coupling #1 — SeasonalElements 4-slot Pydantic model

**File:** `reincarnated-engine/src/reincarnated/element/schema.py:27-30`
**Pattern:** Hardcoded 4-slot structure.

```python
class SeasonalElements(BaseModel):
    fire_slot: SlotSelection
    wind_slot: SlotSelection
    water_slot: SlotSelection
    earth_slot: SlotSelection
```

**Extensibility:** HARDCODED-BRANCH — adding electric requires Pydantic model edit.
**Convergence risk:** Any code referencing `elements.fire_slot` etc. breaks. LLM naming layer's `_SLOT_ATTRS` dict has only 4 keys; electric falls through to None → wrong grouping label.
**Fix-shape:** Replace hardcoded slot fields with `slots: dict[str, SlotSelection]` keyed by canonical element name. Telemetry recorder + LLM naming consume registry iteration.
**Estimated impact:** ~35 LOC across telemetry + LLM naming.

### Coupling #2 — VALID_SLOTS validation tuple

**File:** `reincarnated-engine/src/reincarnated/element/selector.py:34`
**Pattern:** Hardcoded validation tuple.

```python
VALID_SLOTS = ("fire", "wind", "water", "earth")
```

**Extensibility:** HARDCODED-BRANCH.
**Convergence risk:** Element proposals with `primary_slot="electric"` fail structural validation. D1 rubric pipeline rejects new substrates at proposal stage → never reach pool.
**Fix-shape:** Compute `VALID_SLOTS = tuple(e.name for e in foundation.get_rotating_elements())` at initialization.
**Estimated impact:** ~20 LOC schema changes + 10 LLM call refactor.

---

## § 3 — MEDIUM-severity sites

### Coupling #3 — Element affinity + hybrid forbidden pairs

**File:** `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py:22-35`

```python
ELEMENT_AFFINITY: dict[str, list[str]] = {
    "fire": ["wind", "earth"],
    "water": ["earth", "wind"],
    "earth": ["fire", "water"],
    "wind": ["fire", "water"],
    "physical": [],
}
HYBRID_FORBIDDEN_PAIRS = frozenset({
    frozenset({"fire", "water"}),
    frozenset({"earth", "wind"}),
})
```

**Convergence risk:** Electric has no entry → falls back to `ROTATING_ELEMENTS` (any element) → no designed affinity opposition → every electric class gets the same affinity bias as physical. Forbidden pairs hardcoded: electric pairs freely with any other → potentially unbalanced hybrids.
**Fix-shape:** Load `ELEMENT_AFFINITY` from `config/elements.yaml`. Add `allowed_secondaries` field to Element. Forbidden pairs computed algorithmically from pair-structure.

### Coupling #4 — Monster resistance roll

**File:** `reincarnated-engine/src/reincarnated/generation/monster_generator.py:234-241`

```python
def _roll_resistances(self, dominant_element: str, rng) -> dict[str, float]:
    elements = ["fire", "water", "earth", "wind"]
    # ...
```

**Convergence risk:** Electric monsters have zero electric self-resistance (silent `.get()` default) → mechanical convergence; electric lacks the self-resistance buff fire/water/earth/wind gain.
**Fix-shape:** Iterate `foundation.get_rotating_elements()`.

### Coupling #5 — Trial boss resistance roll

**File:** `reincarnated-engine/src/reincarnated/generation/trial_generator.py:112-116`

Same pattern as #4 for trial bosses. Identical fix-shape.

### Coupling #6 — b6_kit_builder element sampling

**File:** `reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py:191, 201`

```python
elements = list(rng.choice(ROTATING_ELEMENTS, size=n_elements, replace=False))
```

**Convergence risk:** REGISTRY-DRIVEN-WITH-CAVEAT — sampling works if `ROTATING_ELEMENTS` is updated; if foundation adds electric but the import path doesn't propagate, only 4 elements sampled.
**Fix-shape:** Compute at initialization from `foundation.get_rotating_elements()` instead of importing static tuple.

### Coupling #7 — Balance loop element redistribution

**File:** `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:233-267, 415-425`

Element-distribution lever in balance tuning iterates hardcoded 4-element list.
**Convergence risk:** Electric skills cannot participate in balance redistribution → excluded from balance tuning → over- or under-powered relative to reference gauntlet.
**Fix-shape:** Pass `foundation.get_rotating_elements()` as context to balance loop.

### Coupling #8 — LLM naming layer canonical-to-grouping (**the critical-fallback site**)

**File:** `reincarnated-engine/src/reincarnated/llm/naming.py:32, 37-42`

```python
_SLOT_ATTRS = {"fire": "fire_slot", "wind": "wind_slot", "water": "water_slot", "earth": "earth_slot"}
_CANONICAL_TO_GROUPING: dict[str, str] = {
    "fire": "ignition", "water": "suffusion", "earth": "bulwark",
    "wind": "displacement", "physical": "impact",
}
```

**Convergence risk:** **This is the convergence-by-stealth site.** Electric has no entry. `_grouping_label("electric")` falls back to `f"impact-mode-{canonical_element}"` → electric described to LLM as `"impact-mode-electric"` → LLM names electric skills like physical/impact skills → semantic convergence.

**The deepest concern:** form-bias recovery is correctly registry-aware (it iterates the foundation registry), but the LLM naming fallback is silently undoing form-bias's protection at vocab-output time. The wards on the upper bridges are intact; the LLM stair has a step missing.

**Fix-shape:** Load `_CANONICAL_TO_GROUPING` from `canonical/story/grouping-layer-vocabulary.md` machine-extractable section. **Assert non-fallback** — raise if a substrate has no grouping label rather than silently emitting `impact-mode-*`.

### Coupling #9 — Telemetry recorder slot iteration

**File:** `reincarnated-engine/src/reincarnated/telemetry/recorder.py:123, 713`

```python
for slot in ("fire", "wind", "water", "earth"):
    sel = getattr(elements, f"{slot}_slot")
```

**Convergence risk:** Telemetry records only 4 seasonal_elements rows. Electric never recorded → schema mismatch → silent data loss.
**Fix-shape:** Iterate `foundation.get_rotating_elements()`; use `getattr(elements, f"{elem}_slot")` (or dict-keyed lookup after Coupling #1 fix).

### Coupling #13 — Cosmological vocabulary 2-2-1 pair structure

**File:** `reincarnated-engine/src/reincarnated/llm/cosmological_vocabulary.py:63-75`

```python
GROUPING_SLOTS = ("ignition", "suffusion", "bulwark", "displacement", "impact")
_PRIMARY_PAIR = ("ignition", "suffusion")
_SECONDARY_PAIR = ("bulwark", "displacement")
_FOUNDATION_SLOT = "impact"
```

**Convergence risk:** The pair-structure framework (2-2-1) is wired into LLM vocabulary generation. Expanding L1 substrate from 4 (+1 foundation) to 6-7 requires either reassigning to existing slots (compromises identity distinctness) OR growing the pair structure (3-3, or 3-2-1-1). **This is the same site flagged in wide-net archaeology as the critical-surprise finding** — escalated there from substrate-keyed to LLM-prompt-structure-coupling.
**Fix-shape:** Refactor to read pair-structure shape from `canonical/story/grouping-layer-vocabulary.md` machine-extractable section.

---

## § 4 — LOW-severity sites

### Coupling #12 — Ability grammar long-range physical

**File:** `reincarnated-engine/src/reincarnated/generation/ability_grammar.py:239`

```python
if range_profile == "long" and element == "physical":
```

**Note:** EXPLICIT BRANCH for physical only. Electric/holy/shadow unaffected. Not a coupling issue per se.
**Severity:** LOW.

---

## § 5 — GOOD PATTERNS (no action required)

### Coupling #10 — season_orchestrator registry iteration

**File:** `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py:317, 522, 537, 564`

```python
rotating = self.foundation.get_rotating_elements()
elements = [e.name for e in self.foundation.get_rotating_elements()]
```

**Status:** REGISTRY-DRIVEN ✅ — automatically includes electric if foundation extended.

### Coupling #11 — gear_catalog registry iteration

**File:** `reincarnated-engine/src/reincarnated/generation/gear_catalog.py:117`

```python
for elem in [e.name for e in foundation.get_rotating_elements()]:
```

**Status:** REGISTRY-DRIVEN ✅ — correct pattern.

**These two sites prove the engine *can* be registry-driven. The other 11 substrate-keyed sites copied an older idiom and never adopted the registry-iteration pattern.** Surface to jack-ryan as evidence the engine has the foundation but lacks perimeter discipline.

---

## § 6 — Form-bias recovery interaction

Form-bias recovery (per `canonical/37-form-bias-diagnosis-and-recovery.md`) is registry-aware: it iterates the foundation registry. **However, the LLM naming layer's grouping-label fallback (Coupling #8) silently undoes form-bias's protection** by emitting `impact-mode-{element}` for unmapped substrates. The mechanical layer is registry-driven; the vocabulary layer is fallback-driven; the vocabulary layer is what the LLM sees.

This is the single most important finding for the diversity architecture. Layer 4 (LLM Flavor Diversifier) must close this gap.

---

## § 7 — Verdict and diversity-architecture impact

The engine has **mixed extensibility**: foundation registry is registry-driven (good); call-sites are not uniformly faithful to that pattern (bad). **13 substrate-keyed sites need work for substrate expansion from canonical-4 to canonical-7.**

| Severity | Sites | Phase-1 P1 effort |
|---|---|---|
| HIGH | 2 | Schema migration; 1-2 days |
| MEDIUM | 9 | Registry-iteration refactor; ~3-5 days |
| LOW | 2 | No action |
| GOOD | 2 | Reference patterns for fix-shape |

**Estimated total Phase-1 P1 effort for substrate-keyed refactor:** ~300-400 LOC across 8-10 files, plus the grouping-layer-vocabulary pair-structure decision (Coupling #13).

---

## § 8 — Cross-references

- `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` (sibling; 14 additional coupling sites across 17 construct categories)
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` (sibling; 10 archetype-keyed coupling sites)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` (the decision this archaeology supports)
- `canonical/story/grouping-layer-vocabulary.md` (current 2-2-1 vocabulary; § Q4 future-expansion reserved labels)
- `canonical/37-form-bias-diagnosis-and-recovery.md` (form-bias recovery; § 6 cipher architecture)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #13 implicit-pillar drift; Discipline-candidate #X registry-perimeter inviolability — proposed by wide-net archaeology)

---

*Authored 2026-05-17 by gandalf. Captures substrate-keyed coupling state at the substrate-expansion-decision commitment moment. Read-only audit artifact.*
