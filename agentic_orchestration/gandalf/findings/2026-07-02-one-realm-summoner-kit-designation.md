# One Realm demo — summoner-kit designation (D2/D3 → D1 re-emit gap)

> **STATUS:** DESIGN DESIGNATION (in-scope One Realm demo curation, Matt-ratified summoner mandate —
> ~8–10 hand-curated becomable kits, ≥1 summoner). Fills the dispatch-sequencing gap: nobody had
> designated WHICH of star-lord's 54 emitted kits become the two hand-authored necromancer summoners.
> **Author:** gandalf (story/design steward), 2026-07-02.
> **Feeds:** star-lord re-emit (attach D2 proxies to the two chosen kits) → drax D4 loader round-trip.
> **Denominator:** `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §3 (summoner mandate) / §20d
> (is-the-engine-the-product cheapness test) / §5.2 (hand-authored decls acceptable at demo scope).
> **Inputs read first-hand:** `src/reincarnated/output/one_realm_demo_bundle.json` (54 kits),
> `src/reincarnated/generation/demo_summoner_kits.py` (2 melee summoner fantasies; gravecaller DEFERRED),
> `src/reincarnated/generation/math/demo-summoner-proxy-decls-content-shape-2026-07-02.md` (rocket D2 note).

---

## 1. The designation

| D2 proxy id | Chosen emitted kit id | Emitted name (as-is) | Read |
|---|---|---|---|
| **`demo_bone_acolyte`** (horde caller — count-2 skeletons, "a line of bone") | **`S1_endgame_bc_melee_high_flat_int_none_s2`** | *Shadow Warden of the Grounded Reach* | native necromancer read — **clean attach** |
| **`demo_crypt_lieutenant`** (single heavy bone-guard bruiser — count-1, slow cadence) | **`S1_endgame_bc_melee_high_flat_int_none_s1`** | *Tidewarden of the Grounded Reach* | caster body OK, theme wrong — **attach-plus-restyle** |

Both are `melee / int:100 / chain_mage / hybrid / earth`, same BC family, same `high_flat` tempo — a
matched caster pair, which is exactly what a starting-pool-summoner + its lieutenant should be (they are
kin, one heavier than the other). The two summon proxies both resolve to `golem_construct / full / taunt /
1.5 m` (rocket note §2), so the *player-body* wants to be a melee-band caster who stands where the bone
emerges — both picks satisfy that. The on-screen difference is carried by the **proxy**, not the host.

## 2. Why these two, specifically

**`Shadow Warden` → `demo_bone_acolyte` (the load-bearing minute-one raise).** Of all 54 emitted kits this
is the *only* one whose generated flavor already carries the death read — verbatim: "channels **shadow
force** through melee bursts… releasing cascading **dark pressure** outward along the chain… treats
**shadow as one more element**." It is INT-driven (a caster, not a brute), melee (stands in the raise-band),
`high_flat` (a steady re-raise cadence, not spiky burst). This is the fantasy promise the whole death-cult
demo hinges on (raise something in minute one) and it should land on the kit that needs zero theme-work.
**Clean attach.**

**`Tidewarden` → `demo_crypt_lieutenant` (the heavy bone-guard binder).** The lieutenant is the caster kin
of the acolyte — I want the *same* INT-melee-`high_flat` family so the pair reads as master-and-apprentice
(or master-and-lesser), differentiated by the guard they raise. The two remaining INT-melee kits are
`Stormcaller` (lightning/fire, aoe_mage) and `Tidewarden` (water, chain_mage). I pick **Tidewarden**
because it is the same `chain_mage/earth` archetype as Shadow Warden (a matched pair, not a fire-mage
bolted onto a shadow-mage), and "water's pressure and weight… anchor opponents in place" restyles into
grave-cold/bind imagery more cheaply than lightning does. But **its theme is water, not death** — this is a
restyle, and I say so plainly (§4).

## 3. Horde-vs-bruiser on-screen legibility (how a player tells them apart)

The rocket decls already do the mechanical work; the read is legible **from the summoned proxies**, not the
casters' bodies (which are near-identical INT-melee silhouettes):

- **`demo_bone_acolyte` (horde):** count-2, `melee_strike`→lone-skeleton silhouette, 6 s re-raise cadence,
  permanent-until-death. The player sees **a replenishing LINE of light skeletal soldiers** streaming into
  the fray — many small bodies, constant churn. Read: *"I raise the dead in numbers."*
- **`demo_crypt_lieutenant` (bruiser):** count-1, `ground_slam`→heavier/bigger silhouette, 9 s cadence,
  permanent-until-death. The player sees **ONE big bone-guard that slams**, re-summoned slowly. Read:
  *"I bind one heavy guardian."*

The distinction is **many-light-fast vs one-heavy-slow** — the strongest legibility axis you can give two
summons that share a proxy_type (rocket note §2 "Distinct from S1"). This satisfies the legibility rider I
queued in the D3 disposition: the two summoners read distinctly on-screen. **Legibility: PASS**, and it
lands on the proxy layer where it belongs — the host-body restyle (§4) does not gate the read.

## 4. §20d cheapness verdict — ATTACH-PLUS-NAMED-RESTYLE (honest datapoint)

**The honest §20d answer is NOT "clean attach for both."** Attaching summon-proxies to bc-target-emitted
kits is *mechanically* free (the `proxies` field already exists; the bridge already runs; zero schema
change) — that part of §20d passes cleanly and is a real win. But the **theme fights the palette**, and
pretending otherwise would corrupt the test the demo exists to run.

**The palette finding (the load-bearing §20d datapoint):** across all 54 emitted kits the dominant-element
distribution is **earth 33 / fire 12 / physical 9 — and ZERO death/necrotic/shadow element.** A
Necromancer-themed demo has no native death element in its own emitted kit pool. Exactly one kit
(`Shadow Warden`) backed into a shadow read via generated flavortext, not via a `dominant_element`. So:

- **`demo_bone_acolyte` = CLEAN ATTACK.** Shadow Warden's name + flavor already read necromancer. Star-lord
  attaches the proxies; nothing else owed. (Its `dominant_element` is still `earth`, which is *fine* — a
  grave-necromancer commanding bone from the earth is coherent; earth is the death-cult's native soil.)

- **`demo_crypt_lieutenant` = ATTACH + NAMED RESTYLE (rocket owes exactly this):**
  1. **name:** `Tidewarden of the Grounded Reach` → a crypt/grave name (e.g. *Crypt-Lieutenant of the
     Grounded Reach* / *Barrow-Warden of the Sunken Cairn*). "Tidewarden" reads sea-priest, not death-cult.
  2. **flavor_text:** rotate the water imagery to grave/bind imagery. "channels water's pressure and weight
     into melee strikes that anchor opponents in place" → grave-cold / grave-weight that binds the dead in
     place. Keep the *mechanics* ("anchor opponents in place… fast flat bursts") — only the elemental skin
     rotates. This is a ~3-sentence flavor rewrite + one name change, no stat/geometry/BC change.
  3. **dominant_element:** OPTIONAL rotation `water → dark/shadow` IF the loadout/Godot skin keys color off
     `dominant_element`. If it keys off `color_palette` only, leave the element and let the flavor carry the
     read. **Flag for drax:** does the round-trip loader color-key off `dominant_element`? That decides
     whether item 3 is owed or free.

**Why this is a datapoint, not a failure:** §20d asks "can ~10 emitted kits become ~10 distinct playable
verbs *cheaply*?" The verb attach IS cheap (bridge + one JSON field). The **thematic** attach is cheap for
kits the generator happened to flavor on-theme (1 of 54 here) and costs a named flavor/name restyle for the
rest. That is the true shape of the cost: **the mechanism is free; the theme is a per-kit flavor tax when
the emitted palette doesn't natively cover the demo's theme.** For a 2-summoner demo that tax is one
restyle — trivially payable. But it names a real launch-scale question the demo was built to surface:

> **Launch-scale flag (not demo-blocking):** if the death-cult theme needs summoners across many kits, the
> generator's element palette (earth/fire/physical, no death) will impose a flavor-restyle tax on nearly
> every summoner unless a death/necrotic element enters the generation palette OR summoner kits are always
> hand-flavored. This is a §20d "is the engine the product" signal: the engine emits *mechanically*
> becomable kits cheaply, but *thematically* on-theme kits only when the palette covers the theme. Route to
> the current-to-end-state engine tracker as an open question for post-demo — do NOT let it block D1/D4.

## 5. What each downstream owner does with this

- **star-lord (re-emit):** attach `demo_bone_acolyte` proxies to `S1_endgame_bc_melee_high_flat_int_none_s2`
  and `demo_crypt_lieutenant` proxies to `S1_endgame_bc_melee_high_flat_int_none_s1`, via
  `all_demo_summoner_proxies()` / the D1 hand-join. Result: exactly two kits with non-empty `proxies`.
- **rocket (restyle, small):** the §4 named restyle on the `crypt_lieutenant` host kit (name + flavor rotate;
  element rotate iff drax confirms color-keys off `dominant_element`). Shadow Warden needs nothing.
- **drax (D4 round-trip):** now has two proxy-bearing kits to load — the §20d "is the engine the product"
  loader test can close. Confirm the color-key question in §4 item 3.
- **gandalf (me):** the launch-scale palette flag (§4) is mine to route to the engine current-to-end-state
  tracker as a post-demo open question. Not firing it now — it does not block the demo.

## 6. What I did NOT do

Did not edit code, did not re-emit the bundle, did not author the restyle text (rocket's lane — I specified
*what* to rotate, not the final strings). This is a designation; the re-emit is star-lord's, the restyle is
rocket's, the round-trip is drax's.
