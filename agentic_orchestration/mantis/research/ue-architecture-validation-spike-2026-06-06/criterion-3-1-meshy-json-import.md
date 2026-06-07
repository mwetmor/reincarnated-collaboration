# Criterion 3.1 — JSON → Meshy Import

**Verdict:** BLOCKED (Meshy API key required)
**Date:** 2026-06-06 Session 1
**Blocker type:** External API access + full kit substrate tuple needed

---

## Blocking gates

1. **Meshy API key** — not available in this agent session. Matt must provide Meshy API credentials (or confirm team account access) to proceed.

2. **Full substrate tuple per kit** — cycle-14 JSON in meta-repo has `kit_name_canonical` and `kit_identity_narrative` but does NOT contain the full appearance descriptor tuple Meshy needs:
   - `element_primary` (fire / water / earth / wind / lightning / holy / shadow)
   - `attribute_primary` (str / dex / int / wis)
   - `cultural_tradition` (European-medieval / Japanese / Ottoman / etc.)
   - `weapon_form_token` (e.g., "longsword", "staff", "katana", "scimitar")
   - `historical_period` (medieval / renaissance / ancient / modern)

   These fields are derivable from the engine's Phase 2 substrate derivation. The kit_id encodes attribute and BC axes but not element, cultural_tradition, or weapon_form_token directly.

   **Resolution:** either (a) Matt provides 3 kit IDs with their substrate tuples from the engine repo on Mac, or (b) star-lord adds substrate_trace to export packet.

---

## Pre-work completed (ready when unblocked)

### 3 candidate kits identified

| Kit | kit_id | BC signature | Notes |
|---|---|---|---|
| Kit A — Named bearer | Duskweaver identity (kit_name: Twilight Inversion Shell) | Shadow / mid / high / int | Cohesion-judge approved; referenced in dispatch § 2 as target |
| Kit B — Broad Blade Convergence | `S1_endgame_bc_melee_high_flat_dex_none_s0` | Melee / high / flat / dex | PROVISIONAL per playtest validation flag |
| Kit C — Ranged INT cluster | `S1_endgame_bc_ranged_low_spiky_int_none_s0` | Ranged / low / spiky / int | Archetypally distinct (caster vs warrior) |

### Meshy prompt template (ready for substrate tuple input)

```
Generate a humanoid 3D character.

Style: [cultural_tradition] [historical_period] fantasy warrior
Primary element: [element_primary]
Primary attribute: [attribute_primary]
Weapon: [weapon_form_token]
Appearance notes: [first 50 words of kit_identity_narrative]

Requirements:
- Humanoid skeleton (bipedal, two arms, two legs, head)
- Closed mesh (watertight)
- Suitable for rigging with Unreal Engine 5 Control Rig
- Poly count target: 30,000-80,000 triangles
- Output format: FBX with embedded textures
```

### Acceptance evaluation criteria ready

Per dispatch § 2:
- PASS: 3/3 kits produce usable humanoid 3D models (poly count in range; textures readable; mesh closed)
- YELLOW: 2/3 PASS + 1 has resolvable issues
- RED: ≤1/3 PASS or systemic Meshy ingestion failure

### Cost estimate
~$5-15 (10 Meshy generation credits across 3 kits, with 1-2 retry allowance). Within $0 spike LLM budget caveat — Meshy generation credit costs are a spike operational cost, not LLM API cost. Matt aware per dispatch § 4 note.

---

## What criterion 3.1 gates

- Criterion 3.2 (Meshy → UE 5.7 import) — needs the mesh output
- Criterion 3.3 (image-pass-through comparison) — parallel test using same Meshy pipeline
- Criterion 3.6 (TAA/TSR) — needs an imported character from 3.2

---

*Criterion 3.1 status: BLOCKED — awaiting Meshy API key + 3 kit substrate tuples from Matt.*
*All pre-work complete. Will execute within one session once unblocked.*
