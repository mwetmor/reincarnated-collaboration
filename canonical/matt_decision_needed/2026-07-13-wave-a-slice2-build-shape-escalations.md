# MATT DECISION NEEDED — Wave-A Slice-2: two build-shape escalations (gate ranged-summon + A3)

> **Surfaced:** 2026-07-13 by knight-rider, sequencing the Wave-A engine spec (gandalf SPEC-AUTHOR → KR handoff).
> **Nature:** two build-shape decisions the spec deliberately did NOT self-authorize (Gate-1 fold D — gandalf did not self-authorize; routed to Matt/gamora before the specialist builds).
> **What proceeds without you:** **Slice 1 is fully authorized and independent** — melee economies (A1/A2/A4) + GX-19 absorption clock + C1a/C1b calibration are dispatched now (`dispatches/2026-07-13-rocket-wave-a-summon-economy-config.md`, `…-gamora-wave-a-summon-simulation.md`). These two escalations gate **only Slice 2** (ranged-summon + the A3 economy). Do NOT block all of Wave A on these — that's the load-bearing sequencing call KR already made per gandalf's recommendation.
> **Empirical close criterion:** your ruling on each item below — not time-passage. Neither Slice-2 item builds until its ruling lands here.

---

## Escalation 1 — Ranged-proxy nav defect: which fix-shape?

**The defect (evidence §6, spec §8):** a ranged proxy (archer) parks **38.9 m** from a boss it can hit at 10 m — ally-nav chases nearest-enemy adds instead of holding boss-focus at range (`spatial_engine.py:~1996` nearest-enemy nav; `:2350` attack-phase boss-focus parity). **No magnitude/tuning lever moves `proxy_realized_damage_dealt` — this is a navigation MECHANIC, not a number.** So it needs a design-shape ruling, not calibration.

**Why it's yours (not gamora's alone):** it changes how proxies *behave in space* — a mechanic with player-experience consequences for the drop-and-forget C1b fantasy. gandalf declined to self-authorize the fix-shape (Gate-1 fold D).

**Fix-shape options (gamora scopes engineering cost/risk into this file before you rule):**
| Option | Shape | gandalf read |
|---|---|---|
| **(a)** boss-focus **inheritance** — ranged ally adopts the player's boss-focus target | cleaner for the drop-and-forget C1b fantasy (proxy tracks what the player is fighting) | **leaned** |
| **(b)** **hold-at-range** behavior variant — proxy maintains engagement distance vs its own target | more general (a reusable behavior branch) | **leaned** |
| **(c)** nav_target priority override | narrowest patch | — |

**Consequence of NOT ruling:** melee-summon ships now (nav-complete); **ranged-summon cert stays blocked.** No harm to Slice 1.

**What's asked of you:** pick a fix-shape (a / b / c), OR delegate the pick to gamora once she posts her engineering read here. gamora will append cost / blast-radius / E4-nav-entanglement risk to this file before the pick.

---

## Escalation 2 — A3 reservation economy: build-true or approximate?

**The mechanic (Fork A, rulings; spec §2):** A3 = **reservation** — each active proxy permanently lowers the player's *regenerating-resource cap* (an army-size wall = permanent tax), NOT a per-cast spend. There is **no engine analog** (evidence §9).

**The fork:**
| Option | Build | Consequence |
|---|---|---|
| **(a) build-true** | a real `reserved` resource type: `regen_cap -= reservation_per_proxy × active_count` | preserves A3's whole identity — the permanent-ceiling model + the abandonment-tax **inversion** (weakest re-drop tax, hardest leash) documented in the rulings. **gandalf lean.** |
| **(b) approximate** | map A3 to a spend-economy approximation | simpler, but **collapses A3 into A2** — loses the permanent-tax fantasy; we'd ship 3.5 distinct economies, not 4 |

**Why it's yours:** you ruled **ship all 4 economies** for veteran gamers (Fork A, verbatim: *"ship all 4 economies"*). Whether A3 is build-true or approximated determines whether the catalogue actually delivers 4 distinct mobility-vs-uptime tension shapes or 3 + a near-duplicate. That's a product-integrity call against your own all-4 mandate.

**Consequence of NOT ruling:** rocket holds A3 (Slice 2). A1/A2/A4 (melee) ship in Slice 1 regardless. A3 is orthogonal to melee-vs-ranged — it can ride Slice 2 with either nav decision.

**What's asked of you:** confirm **build-true (a)** [gandalf lean, consistent with your all-4 mandate] or rule **approximate (b)** knowing it collapses A3 toward A2.

---

## References

- Wave-A engine spec: `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` §2 (A3), §8 (nav)
- Wave-A rulings: `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-RULINGS-2026-07-13.md` (Fork A ALL-4)
- KR handoff: `agentic_orchestration/gandalf/design-inputs/wave-a-KR-handoff-2026-07-13.md`
- Dispatches (Slice 1 authorized, Slice 2 held): `dispatches/2026-07-13-rocket-wave-a-summon-economy-config.md`, `dispatches/2026-07-13-gamora-wave-a-summon-simulation.md`
- PAUSE-2 Wave-A mandate: Q25 (this queue, ruled 2026-07-12) — wave order A→B→C, GX-19 ratified

---

## RULING RECORD
_(Matt: append your ruling on each escalation here; KR/gandalf strike the queue rows to RESOLVED on your ruling. gamora appends her nav-fix engineering read above Escalation 1's pick.)_

- Escalation 1 (nav fix-shape): _pending_
- Escalation 2 (A3 build-true vs approximate): _pending_
