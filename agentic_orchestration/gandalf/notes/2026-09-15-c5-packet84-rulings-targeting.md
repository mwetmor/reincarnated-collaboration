# Run C-5 — Matt rulings on targeting (Packet 84 follow-up, 2026-09-15) — held here while T4c runs (no writes under burst/ during TOOLING); ledger R-C5-9 + SPEC T4f rewrite follow

Matt, verbatim: *"You're right we do not need or want cast order or cast lock. The problem I found was that the tap of my finger did not cast.. only pressing the cast button. So remove the cast button and make it so tapping my finger casts to that location. Also, based on that you will need to remove the maximum range of the skill casts (unless the specific skill calls for it). I think we also need to show something like damage to the dummies in text. Full/partial."* Earlier the same session: *"I agree with skill pierce."*

## Rulings
- **R1 — No lock, no cycle.** T4f's F2/F3/F4 STRUCK. Aim = the tap point (pointer/touch); keyboard fallback = nearest target in the facing cone. **The overlay CAST button is removed** (drax, next web build); **a tap on the scene casts at that location** (exporter/keeper, T4f). Finding: the T3o overlay's tap did not reach the cast action on the phone — only the button did.
- **R2 — No maximum cast range by default.** A cast travels to the tap point at any distance. Per-skill ranges only where the source skill has one (proposed: Frozen Orb travel distance, Blackwater / Poisonous Concoction throw range; Lightning Blast, Zeus, Healing Hands unbounded) — Matt to confirm the three exceptions or rule all six unbounded for the test.
- **R3 — Damage text on dummies: FULL / PARTIAL** (proposed definition, one recommendation): floating label in the kit's colour, rising/fading ~0.6 s; FULL = the effect's primary body contacts the dummy (head hit / field centre / chain hop); PARTIAL = a secondary part only (shard, field rim, pierce pass-through after the first body). No numbers (no damage model exists in the scene). Alt: placeholder numbers · hit-flash only.
- **Pierce per skill — AGREED** (F6): Frozen Orb −1, others 0; strike response once per cast (F5 stands unless struck).

## Consequences
- SPEC § 7 lap 3 T4f row rewritten: tap-to-cast + cone fallback; no lock/cycle/toggle; per-skill `range` (null = unbounded) + `pierce` in kit.json; FULL/PARTIAL floating label on `contact` events with a `contact_class` field (primary / secondary); T4a test re-point kept.
- drax: overlay v8 — CAST button removed; tap = cast; joystick + JUMP + VFX remain. Fires with the next web build after T4f lands.
- Packet 85 (grey bolt at a dummy) is judged under this protocol.
