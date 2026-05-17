# 2026-05-17 — rocket — AOE windup ARPG-tuning YAML amendment (earth + holy)

**Authority:** Phase-1 P1 hive-mind L1 (rocket in-seam; substrate identity YAMLs are rocket-owned). Knight-rider Pattern A pre-authorization from gandalf hand-off per gandalf dispatch `2026-05-17-gandalf-aoe-windup-timing-arpg-validation.md`.
**Type:** Pattern A (short task) — micro-task; ~5-10 min total.
**Trigger:** Matt mid-flight playtest 2026-05-17 ~12:10 EDT asked whether locked windup values match ARPG genre mean. Gandalf validation completed: 5 KEEP, 2 ADJUST (earth 0.4 → 0.5; holy 0.7 → 0.9). See `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 11 for the full ARPG-genre-mean characterization and per-substrate rationale.
**Predecessor tag:** `gandalf/v1.6-aoe-windup-arpg-validation-1` (gandalf addendum + this dispatch).

---

## Required reading (in order, ~5 min)

1. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` **§ 11** (the validation addendum; especially § 11.3 per-substrate verdicts and § 11.6 summary table)
2. `reincarnated-engine/config/substrate_identities/earth.yaml` — current declaration (in scope for amendment)
3. `reincarnated-engine/config/substrate_identities/holy.yaml` — current declaration (in scope for amendment)
4. `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` lines 79, 171, 380-386, 497-500 (windup_duration_seconds field + validation rule #11; bounds [0.0, 5.0]s — both new values are inside bounds)

---

## What to change

### File 1 — `reincarnated-engine/config/substrate_identities/earth.yaml`

**Line 75 (currently):** `windup_duration_seconds: 0.4`
**Change to:** `windup_duration_seconds: 0.5`

**Rationale (one-line for any inline comment if you author one):** earth cosmology is *positional refusal — what does not move and will not be moved* (per substrate-identity-declarations § 3); 0.5s honors the deliberateness identity and matches genre-canon mob-tier floor for earth-coded mobs (D3/D4/PoE earth mobs 0.5-0.9s). See gandalf briefing § 11.3 earth-verdict.

### File 2 — `reincarnated-engine/config/substrate_identities/holy.yaml`

**Line 76 (currently):** `windup_duration_seconds: 0.7`
**Change to:** `windup_duration_seconds: 0.9`

**Rationale (one-line):** holy cosmology is *revelation — the substrate that announces itself with light before the strike* (per substrate-identity-declarations § 6); 0.9s makes holy the unambiguously-slowest substrate (correct cosmology) and lands inside the genre-canon "obvious telegraph" range (D3 Tyrael / D4 angel mobs 0.8-1.2s; PoE consecrated ground 1.0s+). See gandalf briefing § 11.3 holy-verdict.

---

## How to verify

After both edits:

1. Run substrate_identity_loader against the 7 YAMLs (your existing test harness; rule #11 validates bounds [0.0, 5.0]; both 0.5 and 0.9 are well inside).
2. Confirm loader output shows the new values: earth `windup_duration_seconds=0.5`, holy `windup_duration_seconds=0.9`.
3. Run the loader unit tests — expect all GREEN (these values are still valid floats inside bounds; no schema change).
4. No regen needed for this dispatch itself — values are consumed at engine startup; next gamora regen pass (whenever scheduled) will pick them up.

---

## MIGRATION.md note

Add a brief entry to `reincarnated-engine/src/reincarnated/foundation/MIGRATION.md` (or wherever substrate_identities live in your MIGRATION pattern):

```
## §v1.7+ — windup_duration_seconds ARPG-tuning amendment (2026-05-17, gandalf-validated)

- earth: 0.4 → 0.5
- holy: 0.7 → 0.9

Per gandalf ARPG-genre-mean validation (briefing § 11). All other substrates KEEP locked values
(shadow 0.2 / wind 0.5 / lightning 0.5 / fire 0.6 / water 0.7). Both new values inside loader
bounds [0.0, 5.0]; no schema or rule change. Consumers (gamora reactive-escape AI; drax indicator
opacity-ramp) read field as-is — no consumer changes needed.
```

---

## Out of scope (DO NOT)

- ❌ DO NOT modify the other 5 YAMLs (shadow / wind / lightning / fire / water) — all KEEP verdicts per § 11
- ❌ DO NOT change `indicator_color_hex` values (not in scope; different concern per dispatch boundaries)
- ❌ DO NOT change the loader bounds or rule #11 (values are inside existing bounds)
- ❌ DO NOT touch downstream consumers (gamora reactive-escape AI; drax indicator renderer) — they read the field correctly already
- ❌ DO NOT expand scope to player-AOE telegraph fields (status quo preserved per § 11.5 — no player-AOE telegraphing)

---

## Acceptance criteria

- [ ] `earth.yaml` line 75: `windup_duration_seconds: 0.5`
- [ ] `holy.yaml` line 76: `windup_duration_seconds: 0.9`
- [ ] Substrate identity loader tests GREEN
- [ ] MIGRATION.md entry authored (one stanza, ~5 lines)
- [ ] Tag `rocket/v1.11-aoe-windup-arpg-tuning-yaml-amendment-1` (or next available rocket tag)
- [ ] Hive log STATE entry confirming completion + tag
- [ ] HANDOFF entry → gamora (next regen pass consumes new values automatically; no immediate action needed) AND → drax (indicator opacity-ramp timing scales correctly with new values; no consumer changes needed)

---

## Smoke expectation

After landing: next regen pass (gamora-scheduled) will produce telemetry with new windup values; drax indicator rendering will adapt automatically (opacity ramp computes from windup_duration_seconds). Matt's next playtest will perceive earth as ~+6 frames more deliberate and holy as ~+12 frames more announcing. Substrate spread on timing widens from 0.5s to 0.7s, improving D27 perception-test discriminability.

---

## Cross-seam impact

- **Gamora:** no immediate action; next regen pass consumes new values via existing `identity.windup_duration_seconds` access pattern. Forward-note: when reactive-escape AI smoke tests run against earth/holy mobs, escape windows widen slightly — this should improve elite-escape readability for those substrates.
- **Drax:** no code changes; indicator opacity-ramp computes from windup_duration_seconds per § 3.3 of the briefing; ramp duration extends automatically with the new values.
- **Jack-ryan:** observation-only; values inside bounds; no rule violation; no Discipline #13 concern (substrate identity declarations remain coherent with values).

---

## Dispatch lineage

- Predecessor: `2026-05-17-rocket-narrow-slice-engine-schema-fields.md` (rocket v1.7; introduced `windup_duration_seconds` field + initial values)
- Predecessor: `2026-05-17-gandalf-aoe-windup-timing-arpg-validation.md` (the gandalf validation Pattern A that produced the recommended changes; tag `gandalf/v1.6-aoe-windup-arpg-validation-1`)
- Successor: none planned; B13-post-VS2a may revisit two-stage lightning telegraph (first-arc instant + chain telegraphed) per § 11.3 lightning forward-note

---

*Dispatched 2026-05-17 by gandalf hand-off (Pattern A pre-authorization under hive-mind § 14.1.3 minor-operational-amendment authority). Append completion record when done.*
