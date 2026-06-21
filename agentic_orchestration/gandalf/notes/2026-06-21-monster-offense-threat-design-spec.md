# Monster-offense threat-design spec — the CONTENT that fills the two-axis gate (gandalf design ruling; recal-wave input)

**Type:** gandalf threat-design spec. The forward content-design layer of the defensive-axis recalibration. Stage-1 prerequisite to the recal wave's seam build (rocket content + gamora calibration).
**Date:** 2026-06-21
**Author:** gandalf (story-and-design steward)
**Fills:** the encounter-model SHAPE ruling (`2026-06-21-defensive-axis-recal-encounter-model-ruling.md`) named monster-offense as Part-3 constraint **#5** ("RULED entry condition... monster-offense DESIGN work the wave must scope, not a scalar re-fit") and clear-shell death as constraint **#4** ("evaluate per-hit variance / not-fully-coverable threats"). It named the requirement; it did not design the threat vocabulary. **This rules the vocabulary.**
**Authority:** encounter-MODEL + content-design calls are reserved to gandalf/Matt per the instrument-validity workstream brief. This rules WHAT the monsters do (threat archetypes, player-read, magnitude SHAPE, avoidance model, genre brackets, the candidates the wave evaluates first). It does NOT set exact constants (gamora's calibration lane) or the emission schema (rocket's build, jack-ryan Gate-1).
**Does NOT touch:** the banked offensive instrument. This is design input to a future Matt-authorized production wave.
**Grounded first-hand in:** `spatial_engine.py:1933-2000` (mob-cast branch), `:1968-1988` (telegraph-mint), `:906-976` (movement behaviors), `t4_sim_cycling.py:1082` (skill-less synthetic mobs).

---

## 0. The one-line

The encounter-model ruling settled the **gate** — survive AND kill, both graded, the 2D disposition, the homogenization guard, trash<boss ordering. This settles the **content that makes the gate's death real**: not a cranked scalar, but *what monsters do to the player*. There are **two threat archetypes** — the **boss-threat** ("the throne room": heavy, readable, the test) and the **swarm-threat** ("the hallway": light, attritional, rare texture) — and they are different player-feels delivered by different engine mechanisms. Both already have engine substrate; the skill-less synthetic mob (`"skills": []`) is the only thing missing, and it is exactly what this design fills.

---

## 1. The substrate the threats build on (read first-hand — the design is recompose-first, not net-new engine)

The engine ALREADY carries everything the threats need; the production endgame path simply doesn't use it.

- **Mobs cast damaging spatial skills** (`spatial_engine.py:1933-2000`). A ready mob skill resolves through `_compute_aoe_hits(mob, [player], skill, geo)` — **positional hit-detection**: the skill lands ONLY if the player is inside the geometry footprint when it fires. Damage = `damage_multiplier × 300 × MOB_DAMAGE_SCALE × (1 − armor_factor)`; cadence = `cooldown_seconds`. So **positioning + HP + armor already mediate the threat** — the channel is there, unused on the endgame path.
- **A telegraph-mint system already exists** (`:1968-1988`, `_mint_telegraph_spec`): danger-zone footprint, fire-time, damage-amount, minted even on a no-hit cast. The "readable danger" half of the boss-threat is **already built** — BUT it is "ADDITIVE METADATA ONLY... adds NO avoidance branch." The sim mints the telegraph; it does not yet model a player *reading and dodging* it. (This sets §5.)
- **Geometry palette:** `point` (short-range/melee), `circle` (AOE disc), `line` (beam/charge lane), `cone` (frontal breath) are the load-bearing four; `burst/ring/nova/wave/chain/arc` exist as rarer shapes. `self`/`none` = self-cast (the branch heals the mob, `:1942-1944`).
- **Movement behaviors:** `melee_aggressive` (default), `stationary_caster`, `charge_then_melee`, `ranged_kite`, `cast_at_range`, `hit_and_run` (`:906-976`). These already determine whether an entity is *in a footprint* when a skill fires.
- **The gap (constraint #5):** the production endgame boss path builds synthetic mobs with `"skills": []` (`t4_sim_cycling.py:1082`) → they never enter the cast branch → zero damage by construction. **This design gives them skills.** Nothing here is a new engine system; it is content poured into existing pipes.

---

## 2. Boss-threat archetype — "the throne room" (the PEAK death-risk; the test)

**Player-read:** a *small number* of heavy, readable, wind-up'd mechanics. The boss is the moment the build is proven or found wanting. A glass cannon racing the kill is **gambling** — land it before the slam, or eat the slam; a competent kit reads the cadence and survives; a bruiser stands in it and grinds.

**Genre brackets (the target sits BETWEEN two named failures):**
- **AVOID — D4-launch telegraph-soup:** every elite a floor of overlapping ground-effects; combat became dodge-the-floor instead of fight-the-monster; walked back over a year. *Too many threats = no threat is read; it is noise.*
- **AVOID — PoE off-screen one-shot ("rippy"):** death from an unseen, unreactable source. *A threat you cannot read is not difficulty, it is unfairness.*
- **TARGET — D3 Rift Guardian readable mechanics:** a few discrete, telegraphed, heavy events (Orlash's beam-sweep, Perdition's frozen pulse) you move out of — punishing if ignored, fair because read.

**Mechanism (engine-grounded):** the boss (and elite adds) carry a **damaging spatial skill** on a **HEAVY-per-hit + SLOW-cadence** profile — a `circle` slam, a `line` charge-lane, or a `cone` breath, with a **high `damage_multiplier` and a LONG `cooldown_seconds`** (few big hits, not a chip stream). The telegraph-mint already shows the danger zone. **The heavy-slow shape is the design crux:** a big discrete hit is what makes HP and armor *matter* — one slam is a large fraction of a paper kit's HP and an absorbable dent to a bruiser's. That is precisely how a boss-threat produces the ~0.6–0.8 glass / ~0.95+ bruiser **spread** (constraint #2). A fast chip-stream would homogenize (everyone bleeds the same rate); the heavy discrete hit *discriminates by HP/armor*, which is the axis the boss must test.

**Guard compliance (constraint #6 — verified-satisfiable shape):** heavy-slow hits preserve the two viable paths. The **kill-fast** kit ends the fight before many slams land (kill-speed-as-defense — the burst glass passes). The **endure** kit absorbs the slams (HP/armor — the bruiser passes). Neither is forced to one armor number; offense partially substitutes for defense exactly as gamora's guard sweep proved. A heavy-slow boss-threat is the *natural* shape that keeps the axis 2D.

---

## 3. Swarm-threat archetype — "the hallway" (rare texture; STRICTLY below the boss)

**Player-read:** attrition that punishes the **under-defended AND over-extended** — the D3 "I pulled three packs and melted" moment. Trash is *texture*, not the gate: it should occasionally punish genuine recklessness, never be the test. **Rare-by-design.**

**Genre brackets:**
- **AVOID — D4-launch "every white mob is a threat":** trash deadlier than the boss → the encounter rhythm inverts (you fear the hallway, not the throne room). This is the inversion constraint #3 forbids.
- **AVOID — re-introducing coverage-crank:** the encounter-model ruling already settled that a fast-AOE kit clearing the swarm before bleed accrues is **the guard working as designed** (clearing-fast IS mitigation). Cranking coverage so even a fast-AOE kit dies to trash = a mandatory defensive floor on trash = PoE-capped-resist failure on the hallway. **Forbidden.**

**Mechanism (the two ruled candidates from constraint #4, now designed; evaluated in this order):**

- **(a) PREFERRED — per-hit damage variance (burst spikes).** Mob hits are currently *flat*; flat hits make the sharp cliff gamora measured (safe→dead over ~0.10 armor) AND can only punish by clear-shape. Give mob damage **variance** — occasional high rolls. A high-HP kit absorbs the spike; a paper kit doesn't. **This makes DEFENSE (HP/armor), not clear-speed, the mediator** — so even a fast-AOE paper kit can get unlucky-bursted before it clears, while a fast-AOE *tanky* kit shrugs it off. That is the right axis for trash to test (it tests defense, not build-shape), and it doubles as the §2.1 cliff-softener (variance turns the binary into a graded slope). **This is the cleaner candidate and the wave evaluates it first.**
- **(b) TEXTURE LAYER — not-fully-coverable threats.** A *small fraction* of `ranged_kite` / `cast_at_range` mobs that stay OUTSIDE the player's AOE footprint and poke. The fast-AOE kit clears the melee swarm but the ranged pokers chip it. This punishes the build with ONLY AOE and no answer to range — a **build-completeness** gap, genre-true (D3: the kit with no ranged/single-target answer struggles in ranged density). Secondary because it tests build-shape, not pure defense; add as texture if (a) alone doesn't deliver a rare-but-real punish inside the guard.

Coverage-pressure stays **as-is** — the slow/melee/point punish it already does is correct and complementary; it is not cranked.

**Hard ordering (constraint #3):** swarm death-rate **STRICTLY below boss death-rate for every kit profile**. The swarm-threat is a *tail event* (the unlucky burst, the greedy over-pull), never a baseline grind. **Fallback (constraint #4):** if no variant delivers rare-but-real swarm death while respecting the guard AND the ordering, the ruled fallback is **boss-only death** (clear shells carry no death channel), logged explicitly as a scope decision — a coherent, genre-defensible model (only the gate carries the test). Swarm-threat is the *preferred* design for texture richness; boss-only is the acceptable floor.

---

## 4. Threat-magnitude SHAPE (what I rule; what gamora calibrates)

I rule the **shape**, not the constants:

- **Boss-threat = HEAVY per-hit × SLOW cadence.** Few big readable hits. This is the shape that makes HP/armor matter and produces the spread. (gamora tunes exact `damage_multiplier` × `cooldown_seconds` against the ~0.70-heart-of-band glass / ~0.95+ bruiser target + the guard sweep, off the validated anchor `MOB_DAMAGE_SCALE=4.0`, boss-armor ≈0.76.)
- **Swarm-threat = LIGHT per-hit + VARIANCE.** Chip plus tail-risk, never a homogenizing baseline grind. (gamora wires variance and tunes the spike distribution so the swarm punishes paper-AND-careless only, always below the boss.)

The two archetypes share `MOB_DAMAGE_SCALE` but live at opposite ends of the per-hit × cadence plane. **That separation is the design** — same scalar, different threat *texture*.

---

## 5. How avoidance reads in the sim — RULING: positional, recompose-first (NOT a new dodge model)

The telegraph-mint exists but no avoidance branch. **RULING: the recal wave does NOT add an explicit dodge/reaction-probability model.** Avoidance reads **positionally**, through the existing movement behaviors and `_compute_aoe_hits`:

- A `stationary_caster` glass cannon that parks-and-channels is *in the footprint* when the slam fires → eats it (the "greedy" kill-racer takes real risk). A kiting/repositioning kit vacates the footprint → avoids it (the "competent read"). This is **genre-true** (the stand-still-and-channel build eats the slam; the mobile build doesn't) and it **reuses existing engine structure** — no new branch, the wave stays bounded.
- The defensive axis the recal restores is therefore **HP / armor / clear-speed / kill-speed / positioning** — NOT twitch-dodge. That is the correct axis-set for a population-simulation instrument (it measures *build*, not *player reflex*).
- **Named future fork (NOT this wave):** an explicit telegraph-reaction model (the sim modeling a kit *seeing* the telegraph and dodging on a reaction stat) is a real future depth lever if we ever want skill-expression in the instrument. It is named here so it is a logged choice, not silent drift. This wave uses positional avoidance only.

---

## 6. What each seam builds (the buildable handoff — Gate-1 verifies against this)

- **rocket (content):** give the endgame boss/elite/synthetic mobs **real skills** (replacing `"skills": []` at `t4_sim_cycling.py:1082`): a damaging spatial skill with geometry + `damage_multiplier` + `cooldown_seconds`, on the **heavy-slow** profile for the boss-threat. Surface a **per-hit variance** field for swarm candidate (a). Optionally a small fraction of `ranged_kite`/`cast_at_range` behavior for candidate (b). The monster-offense vocabulary, emitted into the pipes §1 confirmed exist.
- **gamora (calibration):** tune the magnitudes (per-archetype `damage_multiplier` × cadence) against the spread target + the **guard sweep as acceptance test**; wire per-hit variance (the cliff-softener); the **joint clear-shell re-derivation** of `PLAYER_ARMOR_FACTOR_VS_STANDARD` + `MOB_DAMAGE_SCALE` (constraint #3 — no boss-only patch); the two-axis joint re-rate.
- **jack-ryan (Gate-1 DESIGN-MODE):** verify the threat-design respects all nine encounter-model constraints AND is buildable on the named engine mechanisms (no invented systems). The boundary: this spec rules *intent + vocabulary + shape*; the build translates it.

---

## 7. Player consequence (the anchor)

**The throne room:** the boss's heavy readable slam means the glass cannon racing the kill is *gambling* — land the kill before the slam fires, or eat a hit that's a third of your HP. That is the D3 speed-GR tension restored: the glass wizard is *good*, ships, and dies more. The bruiser stands in the slam and grinds it down — the outlast fantasy, also good, also ships. The paper-AND-slow kit eats the slam AND can't kill in time — correctly failed, the corner the 1D instrument was blind to.

**The hallway:** trash is texture. It punishes the over-pull and the unlucky under-defended kit — rarely, and *always less than the boss*. A fast-AOE kit clears it (clear-speed-as-defense, the guard working); a careless paper kit occasionally gets burst-melted (the swarm-punish). You **fear the throne room, not the hallway** — the encounter rhythm runs the right direction.

**The whole point:** the player who trades defense for kill-speed CAN, and the threats are *shaped* so that trade is real (heavy boss hits make the gamble matter) without forcing one armor number (variance + multiple viable paths preserve the guard). The boss becomes the test it was always dressed as; the death the gate measures is now content a player can *see, read, and respect* — not a scalar turned up until the numbers move.

---

**Signed:** gandalf, 2026-06-21. The encounter-model ruling settled the gate; this settles the content that fills it. Two threat archetypes on existing engine substrate (mob spatial skills + telegraph-mint + positional hit-detection): the **boss-threat** (heavy-slow, readable, the peak test — D3 Rift Guardian between D4-soup and PoE-rip) and the **swarm-threat** (light + per-hit variance, rare texture, strictly below the boss — punishing the under-defended via HP not clear-shape, with not-fully-coverable threats as a texture layer and boss-only death as the logged fallback). Avoidance reads positionally (recompose-first; explicit dodge is a named future fork). Magnitude SHAPE ruled (heavy-slow vs light-variance, same scalar, opposite ends of the per-hit×cadence plane); constants are gamora's. rocket pours content into the skill-less mobs; gamora calibrates against the spread + guard; jack-ryan Gate-1s against the nine constraints. The death is now something the player fights, not a number that grew.
