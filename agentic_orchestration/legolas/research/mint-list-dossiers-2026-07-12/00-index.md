# Mint-List Dossiers — Index

**Commissioned by:** gandalf (2026-07-12, Matt's usage-offload directive)
**Filed:** legolas, 2026-07-12
**Directory:** `agentic_orchestration/legolas/research/mint-list-dossiers-2026-07-12/`
**Coverage:** 9 mint-list kits (V4-r2 §F4) + Unit 2 PoE2 crossbow check

---

## Slot-confidence matrix (engine-prefix slots only)

Key: H = HIGH · M = MED · L = LOW · N/A = not applicable (NO-MINT or PENDING) · * = speculative

| # | Kit | Dossier | attr | range | tempo | amp | proxy | commit |
|---|---|---|---|---|---|---|---|---|
| 1 | poe1 Totem (Hierophant/Ancestral Warchief) | `01-poe1-totem-…` | STR/M | mid/M | low/M | flat/M | heavy/H | instant/H |
| 2 | d3 Call of the Ancients (IK Ancients Barb) | `02-d3-call-of-…` | STR/H | melee/H | high/H | spiky/M | light/M | instant/H |
| 3 | poe1 Ring of Shields (+ Replica) | `03-poe1-ring-of-…` | ?/L | mid/L* | low/L* | var/L* | heavy/L* | instant/M* |
| 4 | poe1 Blood Magic Keystone | `04-poe1-blood-…` | STR/M | mid/L | low/M | flat/M | solo/H | instant/H |
| 5 | d2 Teleport Sorceress | `05-d2-teleport-…` | INT/H | ranged/H | high/H | flat/M | solo/H | instant/H |
| 6a | d3 Dashing Strike Monk | `06-movement-…` | DEX/H | melee/H | high/H | spiky/H | solo/H | instant/H |
| 6b | le Shift Bladedancer | `06-movement-…` | DEX/H | melee/H | high/H | var/M | light/M | instant/H |
| 7 | poe1 Vaal Blade Vortex | `07-poe1-vaal-…` | INT/M | mid/M | high/H | var/M | solo/H | wind-up/M |
| 8 | d2 Sacrifice | `08-d2-sacrifice.md` | STR/H | melee/H | high/M | flat/M | solo/H | instant/H |
| 9 | poe1 Flame Dash | `09-poe1-flame-…` | N/A | N/A | N/A | N/A | N/A | N/A |
| U2 | PoE2 Crossbow (HVR Mercenary) | `10-unit2-poe2-…` | DEX-partial/M | ranged/H | low/H | spiky/H | solo/H | wind-up/M |

---

## Status per kit

| # | Kit | Priority | Status | Mint action |
|---|---|---|---|---|
| 1 | poe1 Totem / Hierophant / Ancestral Warchief | HIGH | READY TO MINT | New record `poe1-ancestral-warchief-totem`; check G1 grain split for Spell Totem arm |
| 2 | d3 Call of the Ancients | HIGH | READY TO MINT | Elrond reconcile call: is this a distinct record from `d3-ik-hota` or a proxy-lens note? Recommend distinct row focused on light-proxy characterization |
| 3 | poe1 Ring of Shields (+ Replica) | MED | **PENDING — KNOWLEDGE GAP** | Cannot mint; source build unconfirmed. See §Recommended resolution pathway in dossier 03. Flag for post-training-cutoff wiki verification. |
| 4 | poe1 Blood Magic Keystone | MED | READY TO MINT | New record `poe1-blood-magic-rf` (RF as canonical form); check if existing PoE1 records carry BM as a note |
| 5 | d2 Teleport Sorceress | MED | READY TO MINT | Elrond reconcile: fold mob-note into existing d2-blizzard-sorc OR standalone `d2-teleport-sorc` record per GX-01 attestation. Recommend standalone. |
| 6a | d3 Dashing Strike Monk | MED | READY TO MINT (NEGATIVE ANNOTATION) | New record `d3-dashing-strike-monk` with `eras: ["2.4-brief"]` + killed-by-nerf flag |
| 6b | le Shift Bladedancer | MED | READY TO MINT | New record `le-shift-bladedancer`; verify vs existing LE records for duplication |
| 7 | poe1 Vaal Blade Vortex | LOW-MED | READY TO MINT | New record `poe1-vaal-blade-vortex`; operator-tier variant of `poe1-poison-bv`; Elrond confirms grain separation vs parent |
| 8 | d2 Sacrifice | LOW | MATT RULING REQUESTED | Commission flags "arguably negative-canon; Matt rules." Legolas recommends: NEGATIVE CANON (`negative: true`). Mint either way for GX-06 evidential value. |
| 9 | poe1 Flame Dash | LOW | NO-MINT RECOMMENDED | Fails community-named-loop criterion; utility-only; useful as GX-01 negative discriminator note on another record but not standalone corpus row |
| U2 | PoE2 Crossbow HVR Mercenary | — | ATTESTATION COMPLETE | K8 cell `DRLS__` attested by HVR Mercenary on 4/5 slots (ranged/low/spiky/solo confirmed; attr = partial DEX; commitment = wind-up proposed). Not a new mint — attestation evidence only. Check `canon-corpus-poe2.jsonl` for existing HVR record. |

---

## Action items for downstream agents

**→ Elrond:**
1. Kit #2 (d3 CotA): Reconcile with existing `d3-ik-hota` — distinct record or proxy-lens note on parent?
2. Kit #3 (Ring of Shields): Route to UNRESOLVED; do not mint. Wiki verification pass needed.
3. Kit #5 (Teleport Sorc): Reconcile with existing `d2-blizzard-sorc` etc. — standalone movement-verb record or mob-note fold?
4. Kit #7 (VBV): Confirm grain separation from `poe1-poison-bv` and `poe1-minion-pact-bv`
5. Unit 2: Check `canon-corpus-poe2.jsonl` for existing HVR crossbow record; update with attestation if found

**→ Matt (ruling queue):**
1. Kit #8 (d2 Sacrifice): Shipped/negative status ruling requested. Legolas recommends: NEGATIVE CANON.
2. Kit #9 (poe1 Flame Dash): NO-MINT recommendation; confirm or override.
3. Kit #3 (Ring of Shields): If Matt has the source for this name, provide to legolas for dossier completion.

**→ Gandalf:**
1. Kit #6a (Dashing Strike Monk): Era note — killed-by-nerf flag appropriate, or does the shallow-canon value still warrant a positive record?
2. Unit 2: Commitment slot for K8 — WIND-UP (proposed from HVR rotation evidence); design team confirms if this is the intended commitment model for the Crossbow Sniper identity.

---

## Knowledge gaps not resolved

1. **poe1 Ring of Shields source identity** — no evidence found in any accessible source; post-training-cutoff candidate (3.25–3.29 PoE1 leagues). Requires direct wiki verification.
2. **PoE2 post-0.2 crossbow changes** — 0.3–0.5 patch details unavailable; HVR Mercenary attestation based on 0.2 era guides.
3. **D2R Sacrifice changes** — any balance adjustments post-2021 launch not verified.
4. **D3 Dashing Strike** — exact GR tier ceiling for the brief 2.4 viable window not measured (canon_tier = shallow; longevity ~1 patch cycle).

---

## Source summary

| Source type | Used for |
|---|---|
| Knowledge base (kb) | All PoE1 baseline mechanics; D2 baseline mechanics; D3 baseline mechanics; LE baseline |
| Mobalytics (live, July 2026) | PoE2 crossbow builds (0.2+) |
| Maxroll (live, July 2026) | D3 IK HotA; PoE2 Galvanic Shards; LE Bladedancer |
| Icy Veins (live, July 2026) | D3 Dashing Strike Monk; D3 IK HotA |
| Diablo wiki (live, July 2026) | D2 Sacrifice mechanics; D2 Teleport |
| PoB Archives (live, July 2026) | PoE1 VBV build count (216 records confirmed) |
| V4-r2 + corpus-rekey-spec-v1 | Context + mint list authority |
