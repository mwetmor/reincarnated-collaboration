# Judgment resolutions v1 — gandalf per-kit rulings on the 48-flag queue

> **Authored:** gandalf 2026-07-12. Authority: mapping-pass judgment (rules doc prime law — flagged kits resolve per-kit by gandalf); D2 block ruling delegation (def-prep §5); Q15 Walls named-workstream; post-cutoff law. **Application:** a mechanical pass applies these into `corpus-engine-key-v1.jsonl` (flags → `resolved:*` or reclass) and regenerates boards. Matt veto open on every ruling here.

## 1. J-SUM ×5 — RATIFIED `totem`

`gd-skeleton-ritualist` · `le-wraithlord-necro` · `poe2-infernal-legion` · `poe2-minion-infernalist` · `tl2-bot-engineer` → keep `totem`; flag → `resolved:totem-ratified`. Placement is the honest cast geometry; the army's autonomous behavior is exactly what GX-19 (SU mechanics) must build — these five are the SU demand's hardest cases (heavy-proxy: the PROXY delivers all damage). They stay in Board 1's SU mechanics-demand set.

## 2. J-ORB ×4 — reclass `gx-candidate:orbit` (pause-2 add-list item; do NOT key)

`poe1-poison-bv` · `d3-inarius-bonestorm` · `d4-ball-lightning` · `d4-bouldercane`. The orbit family (persistent objects rotating at radius, hitting on contact, stack-maintained) is mechanically DISTINCT from both `whirlwind` (body-spin radial) and `circle` (radial pulse): uptime economy + contact-on-rotation. Four canon kits across three games — BV is a poe1 archetype pillar, Bone Storm a set-defining D3 build, Ball Lightning D4's most-overtuned season build. Keying them to circle/whirlwind would bend the kit (prime law). **Verdict: `orbit` is a real 25th-geometry GX candidate; the four rows carry `gx-candidate:orbit` and enter the pause-2 mechanics-leverage board as their own line (orbit unlocks 4 canon kits).**

## 3. J-GEO ×14 — reclass `row_class: system-record` (not combat kits; exit combat denominators)

These are genre-GRAMMAR records the corpus rightly carries but which have no combat geometry to key. The mapping pass correctly refused to bend them. Each routes to the spec that consumes it (`route:` tag applied in the JSONL):

| kit | route |
|---|---|
| `di-essence-transfer`, `ud-gear-enchant-economy`, `hot-gear-well-retrieval` | `loot-economy` (agnostic-loot spec reference) |
| `di-resonance-awakening`, `di-inferno-ladder`, `ud-zodiac-board`, `ud-chaos-dungeon-ladder`, `ud-classless-triad` | `progression` (progression-design reference) |
| `ud-link-rune-grammar`, `ud-multishot-link` *(J-DEF-only row; same class)* | `modifier-grammar` (the explicit convergence-test: 6-link TAG-GATED sockets vs our modifier scaffold) |
| `hades1-privileged-status` | `ailment-synergy` — **flagged as ailment-layer design INPUT**: mechanized multi-ailment damage multiplier is a proven genre answer to "why stack different elements' ailments" |
| `hades2-omega-magick` | `commitment-grammar` (reference for our instant/wind-up/channel axis) |
| `hot-artifact-stack` | `difficulty-authoring` (self-authored difficulty; Rider-3/difficulty-ladder reference) |
| `vs-big-trouser` | `meta-currency` (build-as-bank archetype; loot/economy reference) |
| `tli-sage-elixir` | `consumable-economy` (post-cutoff; dossier_owed stands) |

Combat-kit denominator becomes **463** (478 − 14 system-records − 1 ud-multishot-link... = 463; boards recompute exactly). Board 2 separates system-records from unmapped combat kits (there are now ZERO unmapped combat kits).

## 4. J-DEF ×24 — resolved as follows

- **D2 block trio** `d2-hammerdin` · `d2-zealot` · `d2-charger` → **`evade` + rider `trigger:block`.** The D2 ruling's own genre table classifies D2 Holy-Shield max-block as **binary negate = evade-physics**. The script lacked per-kit physics text; the design ruling already settled the game-level physics. RESOLVED by delegation authority.
- **`le-harvest-lich`** → **`glass`.** Death Seal's HP-lock is the ECON fact (self-cost); the defense identity is deliberate low-life offense-as-defense. `self-cost` stays visible in econ + fact layer.
- **`poe2-walking-calamity`** → **`tank`** (kb text: "~20K armor autobomber") · **`poe2-shaman-bear`** → **`tank`** ("built-in armour tank body"). Both at post-cutoff conf cap (≤0.5), `dossier_owed` confirm stands.
- **`poe2-spiral-volley` · `poe2-whirling-assault-ma` · `poe2-snipe-mirage-deadeye` · `poe2-archmage-totems`** → **`post-cutoff-deferred`** (no defense facts in kb; dossier resolves; POST-CUTOFF law — do not guess).
- **Remaining 14** → resolved by §3 reclass (system-records have no defense identity).

## 5. Placed-lane / Walls demand — 3 kits (Q15 workstream evidence)

- `di-bone-wall-necro-pvp` — RATIFIED `J-GEO:placed-lane`.
- **`d2-firewall-sorc` — gandalf per-kit OVERRIDE: re-key `line` → `J-GEO:placed-lane`.** Design truth: Firewall is cast at a ground location as a persistent lane-zone; whatever the probe's delivery literal, the engine's `line` (cast pierce-line) misdescribes it. Probe facts stand as provenance; override documented here.
- `le-frost-wall-rm` — stays `totem` (placed object; defensible until Walls exists) but is COUNTED in the Walls demand set.

**Walls corpus demand = 3 kits** → recorded on Board 1 as its own line (the Q15 named-workstream now has corpus demand evidence, exactly like orbit).

## 6. Escalation to Matt (carried in the session report, not ruled here)

**Fork D4 fired:** sustain-leech primaries = **12 > 10 threshold.** Kit list: d2-frenzy-barb, poe1-cyclone, d4-blood-surge, le-reaper-form-lich, le-healing-hands-paladin, di-blood-knight, tq-ternion-bone-charmer, vs-vlad-dracula, vs-bloody-tear, vs-soul-eater, vs-fuwalafuwaloo, hot-cleric-radiant. **gandalf lean: keep 5 verbs; `sustain:leech` stays a rider** — PoE itself files leech under *recovery*, not defense (defences = armour/evasion/ES/block; recovery = regen/leech/recoup); sustain answers "how do I refill between hits," not "what happens when the hit lands" — a temporally orthogonal axis, not a sixth hit-response verb. If recovery-texture ever needs first-class representation, it enters as an orthogonal descriptor axis, not a bin. Matt rules.

**Signed:** gandalf 2026-07-12. 48 flags: 45 resolved here, 4 parked as gx-candidate:orbit (pause-2), Fork D4 escalated.

> **§6 RESOLVED — Q23 RULED 2026-07-12 (Matt: "yes, please add it as a rider.").** Defense stays 5 verbs; `sustain:leech` is a rider permanently. The 12 kits stand exactly as keyed (`tank` + rider) — zero re-keys. Residue routed: kit-native leech channel (vs today's gear-affix/substrate-template sourcing) joins the pause-2 add-list with the 12-kit demand evidence (econ `partial:LC`).
