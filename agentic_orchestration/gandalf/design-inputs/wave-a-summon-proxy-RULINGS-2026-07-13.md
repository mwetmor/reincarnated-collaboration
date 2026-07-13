# Wave A — Summon / Proxy mechanics: CLOSED RULINGS

**Ruled by Matt 2026-07-13** (ELICITOR grill, gandalf). Evidence base: `wave-a-summon-proxy-evidence-v1.md` (48 kits / 15 games / 5 clusters). This doc is the ratified input to the **Wave-A engine spec** (→ KR → gamora/rocket).

---

## Fork A — Summon economies: **SHIP ALL 4**

Matt verbatim: *"we need to ship the full catalogue where we can… ship all 4 economies."* Dev-log audience = veteran gamers who have played these games; a thin summoner offering disappoints them.

| Economy | Mechanic | Engine analog | Abandonment-tax curve (Fork-C interaction) |
|---|---|---|---|
| **A1 cooldown-gated** | re-summon on cooldown | only existing engine analog | drop-rate hard-capped by cooldown → move faster than cooldown = guaranteed abandonment. **Cleanest, strongest tax.** |
| **A2 spend-to-summon** | resource-priced summon | none | drop-rate capped by resource regen; kiting often = not generating. **Real, skill-expressive.** |
| **A3 reservation** | permanent reserved-resource proxies | none | no re-drop cost → **weakest abandonment tax**, but **hardest leash** (proxies literally can't follow). Inverted shape. |
| **A4 harvest/corpse** | kill-fueled summon | none | totem-starved at pack-open, drowning mid-pack. **Tax spikes when danger spikes.** Spiciest curve. |

Four economies = four distinct mobility-vs-uptime tension shapes. Redundancy fear withdrawn — this is a design asset.

## Fork B — Re-summon cadence: **B1** (manual re-summon, native cadence per economy)

No auto-refresh. Each economy carries its own natural re-establish rhythm (A1 cooldown, A2 resource, A3 permanent, A4 kill-gated).

## Fork C — GX-19 absorption seam (commitment/cost transfer to proxies)

The tech that lets a kit legitimately occupy **FREE-MOVE × BEAM** — the cell the genre barely ships (DL-03 generalized). Canonical exhibit: PoE Pizza Sticks (totem carries the Flameblast channel; player's cast is instant + mobile).

### C2 — Plane address: **C2a — DUAL / bridge address**
Kit occupies BOTH the player-movement cell AND the proxy-delivery cell, rendered as a **tethered pair** on the selection table. Makes the native mechanic legible ("I move free, my totem beams").
- **Render requirement:** tether carries a **weighted center-of-gravity** indicating which cell the kit leans toward at its tuned config — otherwise C2a lies at the extremes. CoG **slides with progression** (see C1).

### C1 — Balancing lever: **C1a floor + C1b as end-game balance coordinate**
- **C1a (the floor, holds throughout):** ramp-time + fragility, **protected from buy-out**. Ramp shortens with investment but never reaches literal-instant (illustrative floor ~0.5–0.8s). Totems stay killable/expirable, so count-stacking always trades uptime for exposure.
- **C1b (the target):** the **FREE-MOVE × BEAM drop-and-forget fantasy is the intended endgame payoff coordinate** — not an exploit. The archetype earns its way into the rare cell.
- **Composed = a progression arc:** abandonment tension high at low investment, asymptotes toward FREE-MOVE × BEAM at endgame, C1a floor is the permanent asymptote gap. Mirrors PoE's *healthy* Hierophant window with the zero-floor failure mode designed out.
- **S6 matchup gate certifies at the C1b endgame coordinate.**
- **Render consequence:** tether CoG sits near ROOTED × BEAM at low investment, slides toward (never onto) FREE-MOVE × BEAM at endgame.

### C3 — Wave-A absorption scope: **channel + wind-up absorption ship in Wave A**
Commitment-species absorption (channel time, wind-up) is Wave-A engine work. **Life/mana cost-absorption rides the economy layer** (A2/A3/A4) — already covered, no separate Wave-A work. *(Carried as leaned; not explicitly re-ruled — open to veto.)*

---

## Enrichment kits (mint dossiers 2026-07-13) relevant to the Wave-A exhibit set
- `d3-call-of-the-ancients` — summon-3-ancients (proxy economy exhibit; A1/A4-adjacent)
- `le-ring-of-shields` — orbital proxy shields (corrected from `poe1-*`; see returns-adjudication)
- `le-shift-bladedancer` — proxy-light shadow-generation layer
- `poe1-totem-hierophant` — canonical PoE1 totem archetype

These enrich the engine-spec exhibit set; they do **not** re-open the closed forks.

---

## Next step
Author the **Wave-A engine spec** — 4 economies × proxy-AI branch × absorption modes (channel + wind-up) — routed to KR for gamora (simulation/proxy-AI) + rocket (generation of the economy/absorption config). Engine gap flagged in evidence-v1: proxy-AI variant taxonomy (line 435), `_DEFERRED_PROXY_BINS` emission gate, ranged-proxy nav.
