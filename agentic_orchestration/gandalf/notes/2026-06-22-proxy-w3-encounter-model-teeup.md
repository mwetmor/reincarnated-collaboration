# Proxy Wave-3 encounter-model — tee-up (pre-framing the SHAPE ruling so it's fast when gamora's calibration evidence lands)

**Author:** gandalf (design seam). **Mode:** Pattern-B development, verification-first. **Status:** TEE-UP, **NOT a ruling.** It pre-frames the W3 encounter-model SHAPE ruling against the *known* Path B floor + compound guard, so that when gamora's W3 calibration evidence (the 4 SCAFFOLD magnitudes) lands, the ruling is fast instead of a cold start. It also closes the one proxy-specific question the homogenization reconciliation note opened but did not answer: **how the army-commanding caster's defensive read differs from the solo player's.**

**Builds on (all verified first-hand):**
- `2026-06-21-encounter-model-firm-up-disposition.md` — the already-ruled SOLO shape (build-floor + dodge-ceiling; telegraphed signature slam) + its "Proxy convergence" §.
- `2026-06-21-defensive-axis-recal-encounter-model-ruling.md` §2.4 — **already ruled: proxy W3 INHERITS the real death channel; does NOT re-decide A-vs-B; it narrows to calibrating "proxy survivability + caster-self exposure" against the SAME channel solo now carries.**
- `2026-06-12-session-2-proxy-companion-architecture-spec.md` §2.2 — the proxy taxonomy (types 1 Passive Fighter / 3 Golem-taunt / 5 Bodyguard-intercept are the minion-wall mechanisms, already specced as ProxyCombatant entities).
- `2026-06-22-path-b-defensive-axis-homogenization-reconciliation.md` §3 — the COMPOUND-floor guard (elemental resist + physical mitigation, one gear budget). **This memo extends it: the proxy is a potential THIRD axis.**

---

## TL;DR — the army is a defensive LAYER, not a defensive SUBSTITUTE. That one sentence is the ruling I will hand down; everything below is why, and the single number-set from gamora that confirms or breaks it.

The solo encounter model is ruled. The proxy "fourth answer" — **command an army that walls the slam** — is genre-canonical and already specced in our own taxonomy. The genuinely-new risk is a **compound-guard leak from a new direction:** the army is bought with a *different currency* than resist/armor (summon-allocation / trait / T4, **not** gear slots), so army-as-defense does **not** compete with offense the way the reconciliation note's two gear-axes do. If the wall reliably holds, the proxy build skips BOTH personal defensive axes Path B and the recal are trying to make matter — **and pays no fragility cost for skipping them.** That is the §11.3 guard failing from the *optional-bypass* direction (not the mandatory-tax direction it was written against). The W3 calibration's job is to make the army behave like offense-substitution does: a real choice with a real risk (the slam evaporates the wall; in the resummon gap the under-defended caster is exposed), **not** a free lunch.

---

## 1. The foundation that is ALREADY ruled — do not re-open (state it, inherit it)

Two things are settled and the W3 ruling INHERITS them; I name them so the ruling builds on rock, not sand:

1. **The solo encounter shape (firm-up disposition).** A **telegraphed signature slam**, answerable on the **build-floor** (resist / tank / out-range — live now, the only live answers) and rewarding on the **dodge-ceiling** (i-frame roll vs the minted wind-up geometry — deferred behind Godot combat, inert in sim by design). Build-primary by necessity, not just philosophy. The cure for a soft floor is *build the ceiling*, never *harden the floor* (the dm=6.0 mistake my own anchor ruling rejected).

2. **Proxy W3 inherits the real death channel (defensive-axis recal §2.4).** Matt ruled death is a core pillar; the proxy boss is graded on the SAME two-axis gate (survive AND kill, both graded). The proxy packet §4's "grade-on-clear-time OR add-a-death-channel" fork **collapsed to "AND, inherited."** W3 does **not** re-rule the encounter model. It calibrates **one** thing inside the answered model: **how the summoner's defensive profile — proxy survivability + caster-self exposure — reads against the channel solo already carries.**

**So W3 is a calibration inside a ruled model, with one design SHAPE question still open: what is the army's defensive *role*?** That is what this memo frames.

---

## 2. The proxy-specific fourth answer — the army as a minion-wall (genre-canonical, and already in our taxonomy)

The solo player answers the slam with resist / tank / out-range (+ future dodge). The summoner gets a **fourth answer the solo player does not have: a body of allies between the slam and the caster.** This is not invention — it is the spine of the summoner archetype across the genre, and we have already specced its mechanisms:

| Mechanism | Genre canon | Our already-specced proxy type |
|---|---|---|
| **Aggro-sink / taunt wall** — enemies preferentially hit the wall, not the caster | D2 Clay/Iron Golem body-block; PoE Feeding Frenzy + Convocation repositioning; minions that hold the boss's attention | **Type 3 Golem/Construct** — "draws enemy aggro (taunt behavior); tanky damage mitigation" |
| **Hit-interceptor** — a body that eats the big incoming hit in the caster's place | PoE Animate Guardian / a tanky Spectre soaking a slam; the bodyguard fantasy | **Type 5 Bodyguard** — "intercepts player-targeted hits when player would take >20% max HP in a single hit" |
| **Meat-wall / distraction mass** — sheer number of bodies that the AoE has to chew through first | D2 Skeleton Mastery wall; PoE Summon Raging Spirits / Raise Zombie swarm; D3 Command Skeletons; Last Epoch skeleton/wolf packs | **Type 1 Passive Fighter** — "follows player; auto-attacks; simple combat AI" (the bodies in the way) |

**The firm-up disposition already named the headline:** the heavy-slow telegraphed slam *"evaporates army AND threatens the caster."* That is exactly right and it is the whole design tension in one phrase: the slam is big enough and slow enough that it **clears the wall** — and then the question is whether, having cleared it, it **reaches the caster.** The wall buys time and redirection; it does not confer immunity. That is the D2 Necromancer's life: the skeleton wall holds the line until a boss AoE vaporizes it, and a naked Necro standing behind a dead wall is one slam from the floor.

---

## 3. The genuinely-new recognition — the army is a THIRD defensive axis, and it can BYPASS the compound guard (the leak)

The reconciliation note made the homogenization guard a **2-axis compound:** elemental resist + physical mitigation, **sharing one gear budget**, so the build space is 3-way (two defensive axes + offense) and no corner may be *forced*. The proxy archetype adds a third defensive axis — **army-soak** — and it is structurally different from the other two in the one way that matters:

> **Resist and armor are bought with the SAME currency offense is bought with (gear slots) → they COMPETE with offense. The army is bought with a DIFFERENT currency (summon-allocation / trait / T4, per architecture spec §1) → it does NOT compete with the gear budget at all.**

This inverts the guard's safety condition. §11.3(b) — *"offense can partially substitute for defense"* — is a GOOD property precisely because the substitution carries a COST: you skip defense, you pay in fragility (you must kill faster, you die more). It is a real choice with a real risk. **Army-as-defense threatens to be substitution WITHOUT the cost:** if the wall reliably holds, the proxy build spends its entire *gear* budget on offense, pays *nothing* for the army out of that budget, AND is not fragile — because the wall is doing the defending. That is not the guard working (a costed trade); it is the guard **leaking** (a free defense that lets one archetype skip both costed defenses the rest of the roster must weigh).

**The failure this produces, stated as the player would meet it:** *the one build that doesn't have to play the defensive game.* Resist budget (Path B) inert for summoners. Armor threshold (recal) inert for summoners. The boss's telegraph never read, because the wall eats it every time. This is the **Diablo Immortal "just get more X" stat-check feel** the firm-up disposition already named as the all-floor failure — except here it is localized to one archetype and arrives through a *bypass*, not a threshold. It is also the well-documented genre temptation that D2/D3/PoE all had to actively design against: the **un-killable minion wall that trivializes the encounter** (why PoE minions die to map-boss AoE, why D2 boss AoE clears skeletons, why a low-life summoner with no personal resist/life still dies in the resummon gap). The genre's fix is uniform — **the wall must be killable on the boss's timeline, and the gap must be lethal to an under-defended caster.**

---

## 4. The SHAPE ruling I will hand down when the evidence lands (pre-framed here)

**The army is a defensive LAYER (a meat-wall + aggro-sink that buys TIME), NOT a defensive SUBSTITUTE (it does not confer immunity).** Three clauses, each tied to a clause the rest of the roster already lives under:

1. **The slam must remain able to REACH the caster.** The army reduces the *frequency* with which the slam lands on the caster; it must not drive that frequency to zero. Mechanically: the slam evaporates the wall (per the firm-up headline), and the **resummon gap is a real window of personal exposure.** If the wall never falls inside the boss's timeline, clause 1 is violated and the bypass is live.

2. **A proxy build that skips BOTH personal defensive axes (resist AND armor) must land in the SAME disposition the glass cannon got, not a better one.** The defensive-axis recal ruled the glass cannon "viable but high-variance — play sharp" (~0.6–0.8 survive). The all-offense-behind-a-wall summoner must land **there too**: viable, sharp, *dies more in the gap* — **not** "safe and fast," which would be a corner no gear-budget build can reach. Same compound guard, applied to the third axis: army-substitution must carry a fragility cost exactly as offense-substitution does.

3. **The army must not let the caster pay LESS total defense than every other archetype pays.** A summoner who *also* invests personal resist/armor is the durable, safe summoner (the bruiser-equivalent). A summoner who dumps everything into offense + army is the high-variance summoner. Both viable; the spread between them is the archetype's internal 2D axis — **but neither corner may sit below the floor the rest of the roster stands on.** The wall is allowed to be *a* defense; it is not allowed to be a *free* defense.

This keeps the proxy archetype inside the compound guard as a **third axis**, not a hole in it. It is the same principled landing the recal used for the glass cannon: a costed, high-variance trade — never a safe bypass.

---

## 5. The calibration evidence that resolves it — and why it converges at Path B 1c

gamora's W3 SIM wave calibrates four SCAFFOLD magnitudes. Read against the §4 ruling shape, each one maps to a clause:

| W3 magnitude | What it decides for the encounter model | Binds clause |
|---|---|---|
| **`base_hp`** (army durability) | How long the wall survives the slam — i.e. whether it *evaporates* (good) or *holds* (leak) | §4.1 (slam reaches caster) |
| **`proxy_max_active`** (wall size) | How much mass the slam must chew through; whether resummon refills faster than the slam clears | §4.1 + §4.3 (gap is real) |
| **`attack_interval_s`** (resummon / re-engage cadence) | The length of the exposure gap — short gap = low caster risk (leak); real gap = costed trade | §4.2 (high-variance, not safe) |
| **`damage_multiplier`** (army offense) | Whether the army is *also* the kill-speed answer — if so, army doubles as offense-substitute AND defense-substitute, the worst case | §4.3 (no free total-defense discount) |

**The single read that confirms-or-breaks the ruling:** at the chosen knob-set, does a proxy kit that buys **zero personal resist and zero personal armor** survive the boss at **glass-cannon variance (~0.6–0.8), not bruiser safety (~0.95+)?** If it survives at bruiser-safety with no personal defense, the wall is a free defense — clause 1/2 violated, recalibrate (lower `base_hp` / `proxy_max_active`, lengthen the exposure gap). If it survives at glass-variance and dies in the resummon gap, the army is a costed layer — ruling holds.

**Why this converges at Path B Step 1c (the three-way binding):** the proxy caster-threat read cannot be set in isolation, because the same gear budget feeds **all three** of:
- **Path B elemental resist budget** (1c) — what the caster pays for personal elemental defense,
- **defensive-axis physical recal** (`MOB_DAMAGE_SCALE` 0.40→4.0 + armor/HP) — what the caster pays for personal physical defense,
- **proxy army-soak** — the non-gear third axis that can substitute for *both* of the above.

If the army is calibrated against an encounter where the caster is *assumed* to also carry resist+armor, but the actual dominant proxy build skips both (because the wall covers them), the army knob is set against a fiction. **All three must be co-evaluated against the COMPOUND guard, now extended to the proxy's third axis** — which is precisely the co-calibration coupling the reconciliation note §4 already flagged for 1c ↔ recal, with the proxy as the third strand. This is a gamora calibration job under jack-ryan's Gate-2; I set only the SHAPE (§4) and the confirm-or-break read (above), not the numbers.

---

## 6. Player consequence (the anchor — the two fantasies, one to land, one to forbid)

**The fantasy to LAND (army as costed layer):** *"My wall of skeletons holds the line; I rain death from behind it. The boss winds up its signature slam — and I watch my whole front rank get vaporized. Now I've got about two seconds: resummon, or reposition, before that slam finds ME. I run light on personal armor because the wall IS my armor — which means when the wall's down, I'm sweating."* That is the D2 Necromancer / PoE summoner at its best: high-variance, sharp, the defensive game *relocated* onto wall-management and gap-timing rather than removed. It is the glass cannon's "play sharp," wearing a different costume.

**The fantasy to FORBID (army as free bypass):** *"I dumped everything into offense, skipped resist and armor entirely, and my wall just... never lets anything reach me. I never read the boss's telegraph. I never resummon under pressure. Defense is a stat I literally never bought and never missed."* That is the build that doesn't have to play the game — Path B's resist budget and the recal's armor threshold both dead for this archetype. The W3 calibration exists to make the first true and the second impossible.

---

## 7. What's mine / what routes / what stays gated

- **gandalf owns:** the §4 SHAPE ruling (army = costed layer, not free substitute; the three clauses), the §3 recognition (the army is a third compound-guard axis with an inverted-substitution leak), and the §5 confirm-or-break read (zero-personal-defense proxy kit must survive at glass-variance, not bruiser-safety). These are design criteria — pre-framed here, *handed down as the ruling* when gamora's evidence lands.
- **Routes to gamora under jack-ryan's Gate-2:** the four SCAFFOLD magnitudes, co-calibrated against the compound guard extended to the proxy's third axis (the §5 convergence at 1c). All numbers, including the exposure-gap length and the army-durability ceiling, are gamora's to set and jack-ryan's to ratify.
- **Routes to KR:** the recognition that **proxy W3 is now a third strand of the 1c three-way binding** (Path B elemental + physical recal + proxy army-soak) — it cannot be calibrated against a caster assumed to also carry personal defense it may skip. This extends the reconciliation note's 1c↔recal coupling to a triple. A sequencing input.
- **Inherits (do not re-open):** the solo encounter shape (firm-up) and the proxy-inherits-death-channel ruling (recal §2.4). W3 is a calibration inside an answered model.
- **Stays Matt-gated (unchanged):** the proxy architecture build itself; content emission; all push.
- **No code touched.** Design pre-framing only. The ruling fires when the evidence does.
