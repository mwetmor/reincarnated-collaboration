# One Realm — MVP Scope (the demo, the denominator)

**STATUS:** CANONICAL — CURRENT (load-bearing). Matt-ratified 2026-07-02 (five of six forks as leaned + the **kit-composition correction**, § 3). This doc is the **denominator**: every tracker queue re-reads as MVP-critical vs launch-scope against it.
**Author:** gandalf (SPEC-AUTHOR / SCENEWRIGHT). **Ruled by:** Matt, 2026-07-02.
**Companion docs:** `../reap-die-rise-story/gameplay-loop-design.md` (§6–§10, §20, §23 — the loop this demo enacts once); `../current-to-end-state/current-to-end-state-game.md` (the build delta); `../reap-die-rise-engine/38-downstream-delivery-strategy-2026-05-23.md` (delivery lineage).
**Tracker-delta:** game tracker (B-rows tagged; SESSION-DELTA 2026-07-02); engine + story trackers get the MVP-tag pass as the follow-up unit.

---

## 0. What this is

**One Realm** is the minimum viable prototype of *Reap. Die. Rise.*: a free Steam demo (Next-Fest-bound) whose job is **wishlists**. It is one complete run — the full loop verb enacted once: *descend, best the champion, become it, escape the realm you erupted, choose what to do with its soul.* Genre precedent: Hades EA (one biome), Slay the Spire EA (one act), Death Must Die (Act 1 only), Halls of Torment (demo-first) — small feel-complete slices built the wishlists; breadth never did.

**Ruled forks (Matt 2026-07-02):** demo endpoint = end-card after escape + choice · store page opens when the escape-crescendo trailer cut exists · Next Fest fires at the first Fest *after* the demo is at its best (one-shot rule, treat as hard) · this doc founds `canonical/reap-die-rise-game/` (resolving game-tracker B3's home question) · the MVP-tag pass across all three trackers is ratified · **kit composition corrected per § 3 (lean overruled).**

## 1. The player path (one run, ~25–27 min, per loop-doc §23.1)

1. **Opening** — the king-rig scene (LIVE, game-tracker A4) → **Binding-Rite-LITE**: a cut-down assignment beat that sets the first kit. The full §13a cathedral rite is launch/someday (game-tracker B5); the demo needs the *beat*, not the ceremony.
2. **Structure 1** (~7–8 min) — tight architectural rooms, dense and fast; ends at a **lieutenant boss floor** (Goldilocks spread, § 3) holding the **lesser conduit**.
3. **Biome crossing** (~6–7 min) — open WFC field, ranged/environmental threats, the register-shift beat.
4. **Structure 2** (~7–9 min) — tight rooms escalating to the **realm champion**; the **primary conduit** is the guaranteed #1 treasure.
5. **The Escape** (~5–7 min) — reap the champion = **become it** (+3); combining the conduits erupts the realm; flee as the stolen god-body, plowing through the soldier-mass. *This is the trailer.*
6. **Hand in OR keep** (§23.4) — the moral choice, consequences stubbed to one NPC-reaction line.
7. **End-card → wishlist ask.**

**Replayability is in-scope by construction:** procgen middle + starting-kit variety + the becoming fork mean repeat runs differ — which is what makes the demo streamable past one sitting. The procgen IS the product; the demo should show it re-rolling.

## 2. Non-negotiables (compromise these and the demo is a net negative)

- **Combat feel.** The genre convicts in the first ninety seconds of hitting things (D2 stagger, Hades responsiveness). Feel outranks content count everywhere in this scope.
- **The becoming moment** (§8) — the hook enacted, opt-in, +3.
- **The escape crescendo** (§23.3) — generous-but-urgent clock; winning must feel won.
- **The locked register** — every authored floor passes galadriel's G2 register-CV gate (game-tracker A3 three-gate method; `../reap-die-rise-story/style-register.md`).
- **The min-spec floor** — Next Fest judges on GTX-1650-class machines, not Mac/Metal (the perf doc's "flattering machine" warning goes live at *demo* time). Burn min-spec verification into the build cadence now.
- **Patent hygiene** (loop-doc §1a) — becoming is beat-it-become-it; no enemies-that-remember-you drift (WB nemesis-system territory).

## 3. The demo roster — corrected accounting + the summoner mandate (Matt 2026-07-02)

**Correction 1 — lieutenants and the champion ARE player kits** (loop-doc §5/§8: champions are kits, becomable). The roster budget counts them:

| Slot | Count | Notes |
|---|---|---|
| Starting pool | 4–6 | player picks/receives one per run; spans melee / caster / ranged / controller / **summoner** |
| Structure-1 lieutenants | 2–3 | the Goldilocks spread, **hand-picked temperatures** (hot / right / cold) — curated, not matrix-measured |
| Structure-2 champion | 1 | the escape body — pick a kit whose verbs read spectacular in flight |
| **Total validated player kits** | **~8–10** | **every one becomable** — beat a lieutenant, wear it |

**Correction 2 — the summoner mandate.** The game is Necromancer-themed; a death-cult demo where nothing can be raised breaks the fantasy promise in minute one (and the grimoire itself is a summoning fantasy — story-tracker A11: claimed souls usable/summonable). **≥1 summoner in the starting pool; ideally 1 summoner lieutenant** (a necromancer lieutenant raising adds is also the thematically perfect Structure-1 boss — and enemy-side adds are near-existing tech, `boss_with_adds` shell). Summoner kits are **hand-tuned, playtest-validated demo content**; only the *certification instrument* (multi-actor sim, engine-tracker III.1b) stays launch-track. What the mandate pulls demo-critical is in § 5.

## 4. Scope table

**IN (demo-critical):** the §23.1 three-beat descent + escape · becoming +3 (§8) · two conduits + hand-in-or-keep choice (§23.2/§23.4) · grimoire-as-record with **visibly numbered pages ("page N of 400+")** · scouting glyphs, minimal label→glyph mapping (engine-tracker III.8 — Discipline #41 respected) · **~6–10 ability primitives realized as distinct Godot verbs, including the summon-verb class** · per-floor element rotation (engine-supported today) + faction as presentation-restyle (III.7 invariant protected) · locked register + G2 gate · min-spec floor.

**STUBBED:** hub = a single altar/hand-in beat (no ensemble) · hand-in/keep consequences = one reaction line (no vendor economy) · Binding-Rite-LITE (assignment beat, not the rite).

**OUT (launch-track, unchanged in the specs):** hub ensemble + banter tech (§15/§21) · temporal summoning (§13) · spawn-influence economy (§12) · molting depth · experimental kits (§18) · mega-boss/401st (§8) · entry tiers (§6) · companion (story-tracker B3) · cosmograph presentation (game-tracker A′3) · full Binding Rite (B5) · PvP (§23.6 — already launch-independent) · emergent personality (§16 — already cheap-version-scoped) · matchup-matrix measurement (III.1) · per-level harness (III.2) · `SCENARIO_OVERRUN` certification (III.3) · unified emission driver (II.2) · the 100-kit launch roster (III.4).

**How a 10-kit demo carries a 400-kit hook honestly (§20a/§20c):** the demo shows the *loop* (the showable thing); the *scale claim* rides store copy + trailer + in-demo gestures — numbered grimoire pages, scouting glyphs previewing archetypes the demo never spawns. Cheap, showable, honest.

## 5. Engine asks (demo-critical ONLY — everything else stays launch-track)

1. **One-realm emission hand-join** (star-lord): a single Godot-consumable bundle — kits + monsters + gear + flavortext for the demo realm. A bounded hand-join of the two tracks, NOT the II.2 unified driver. Weapon descriptors: nice-not-critical for the demo; faction fields stay presentation-side (III.7).
2. **Proxy decls for the demo summoners** (rocket): the summoner kits need real `proxies` payloads — hand-authored decls are acceptable at demo scope (`proxy_vocabulary_bridge.py` emits `[]` today; the full `_DEFERRED_PROXY_BINS` un-gate + generation path is launch-track III.1b).
3. **Nothing else.** The three sim instruments (III.1/III.2/III.3) certify *scale*; the demo is *curated*. Goldilocks = hand-picked spread; sawtooth = one descent hand-tuned by playtest; escape fodder density = hand-tuned (Godot renders the mass; certification-at-density lags).

## 6. Godot asks (the critical path — this IS the demo)

1. **Bundle loader** — engine-emitted content playable in Godot. Hand-building kits Godot-side is forbidden: the engine is the product, and §20d is the condition under test.
2. **Verb realization** — the § 4 primitive subset as distinct playable verbs, **including summon** (spawn / proxy AI / fight / despawn — the net-new verb class the mandate adds).
3. **The three-beat floors** — authored through the three-gate method (G1 engine-truth / G2 register-CV / G3 Matt), consuming the banked ravine/crypt ruleset; **camera ratifies on the first floor** (game-tracker B1/A′1).
4. **Enemy AI baseline** + horde-density *rendering* for the escape (50+ on screen at min-spec; balance hand-tuned).
5. **Grimoire + scouting UI, minimal** (numbered pages; glyph preview).
6. **King-rig → descent stitch** (Binding-Rite-LITE joins them; A′2's cheap-recurring-transition principle ratifies here).
7. **Min-spec verification cadence** — GTX-1650-class checks as a standing build gate, not a launch surprise.

## 7. Wishlist machinery (gates are workstream-relative, ruled 2026-07-02)

- **Store page** opens when the **escape-crescendo trailer cut** exists (trailer-first; page accumulates baseline wishlists; Fest spikes it).
- **Next Fest** fires at the first Fest *after* the demo is at its best — the one-shot rule is hard.
- **Trailer grammar** (§20a): the loop in motion — champion after champion, become each; the escape as the closing beat; the creed on screen. Store copy carries "no meta / every hero unique" + the slop-defusing line.
- **Streamability** is a design input: the escape clip is the autoplay unit; repeat-run variety is the stream-session unit.

## 8. What the demo empirically validates (recognition → validate → commit)

The demo is the validation instrument for the design's currently-unfalsifiable claims: the sawtooth's *feel* (§7) · the +3 becoming payoff (§8) · the escape clock's generous-but-urgent band (§23.3) · whether the conduit dilemma is too thin without a power hook (§23.7's own open question) · legibility compression (§20c) · **the §20d parametric-verb condition — THE test**: if ~10 kits cannot become 10 distinct playable verbs cheaply, we must know before promising 400 · combat feel at min-spec. Playtest data from One Realm gates the corresponding launch-scope commitments.

## 9. Sequencing handoff

- **KR** converts § 5/§ 6 into dispatches (drax-heavy; star-lord + rocket bounded).
- **The MVP-tag pass** (ratified): engine + story tracker queues re-tag `MVP-critical` vs `launch-scope` against this doc (game tracker tagged at founding). Follow-up unit, gandalf.
- **In-flight engine work continues** — this doc re-prioritizes *new starts*, it does not halt the instrument build (perception-asymmetry producer, deferral un-gates proceed).
- **Q2 (persistence)** stays the one story item with engine teeth (gates III.2) — unchanged by this doc; a demo banks trivially or not at all.

---

**Signed:** gandalf, 2026-07-02. One realm, whole: the loop enacted once, felt completely. The four hundred are a promise the demo makes credible — not a crowd it ships.
