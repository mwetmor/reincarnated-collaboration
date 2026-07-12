# Dossier — poe1 Flame Dash

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** B5 (movement-verb adjacent; commission flags as "utility not kit identity — candidate for a NO-MINT recommendation")
**Priority:** LOW
**Corpus gap confirmed:** No Flame Dash record in `canon-corpus-poe1.jsonl`
**Crawl date:** 2026-07-12

---

## Identity

**Game:** poe1 (Path of Exile 1)
**Patch/era span:** 2.3 (Prophecy league, June 2016) — 3.29 (ongoing); present for 9+ years; used in thousands of builds as a utility movement skill.
**Canon tier:** utility-note (NOT a standalone kit; see recommendation)
**Folk names:** "Flame Dash," "FD" (typically referenced as a movement option, never as a build-defining loop)
**Shipped / negative-canon status:** The skill is shipped and widely used. However, as a KIT IDENTITY — as the defining mechanical loop that makes a build community-named — it does NOT qualify.

---

## Recommendation: NO-MINT

**"Flame Dash" does not meet the community-named-mechanical-loop criterion for a corpus record.**

### Evidence for NO-MINT:

**G1 grain law failure:** Flame Dash appears in hundreds (possibly thousands) of distinct PoE1 builds across every class and playstyle. It is a utility choice for casters (preferred over Whirling Blades or Shield Charge because it's a spell with no weapon requirements). It folds into the parent build's identity under G1 — it is never the loop.

**Community naming test:** No build is named "Flame Dash Build" in mainstream community sources. The search for community-named Flame Dash builds returned:
- One 3.19 niche guide: "Flame Dash Ignite Elementalist" using Divergent Flame Dash's unique quality modifier ("2% more Burning Damage per 1% quality") to deal meaningful ignite damage on each dash
- This is a gimmick/challenge build with minimal community uptake; not a recognized canon archetype

**Corpus grain check:** The corpus is organized around community-named builds where the loop IS the build. Flame Dash's loop: (1) move to next pack, (2) cast your actual build skills, (3) move again. Step (1) is never the loop.

**Contrast with teleport identities:** The D2 Teleport Sorceress earns a corpus record because Teleport IS the engagement verb — the loop is: Teleport → cast → Teleport. Flame Dash in PoE1 is: Flame Dash → [your build happens] → Flame Dash again. The dash is step 0, not step 1 of the loop.

**Charge system limits kit identity:** Flame Dash has 3 charges with ~4-second recharge. This limits it from being a constant-movement verb (unlike D2 Teleport or LE Shift which can be used continuously). The charge system specifically gates Flame Dash from the "movement-as-combat-verb" role.

### GX-01 note:

Flame Dash provides supporting evidence for GX-01 (movement verbs) as a NEGATIVE DISCRIMINATOR: it shows that movement skills with charge-systems and cooldown gates do NOT achieve kit-identity status even when widely used. This is useful GX-01 calibration data but does not require a standalone corpus record.

If retained in the corpus, it should be as a GAP-REF note on an existing PoE1 record (e.g., on a caster record as `mob: flame_dash_movement`) or as a one-line GX-01 negative note. NOT as a standalone record.

---

## For completeness: engine-prefix claims if minted

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | INT | MED | Flame Dash is a spell; used primarily by INT-class casters; no weapon requirements |
| range | RANGED | MED | The dash repositions the player; subsequent spells are ranged; the dash destination is typically mid-to-ranged |
| tempo | MED | LOW | Charge system limits frequency; 3 charges ≈ 3 dashes before 4-second wait; moderate cadence |
| amp | VARIABLE | LOW | Flame Dash deals marginal base damage (burning ground on path); completely variable by build context |
| proxy | SOLO | HIGH | No proxy; the player dashes and casts |
| commitment | INSTANT | HIGH | Flame Dash is an instant teleport; no cast time (unlike Flame Wall) |

## Raw descriptors

**geo:** Short teleport (~20-unit range); burning ground trail (minor area, brief duration); primarily a positional tool, not a damage tool.

**ctrl:** Minor deterrent: burning ground on path can tickle enemies but no meaningful CC.

**mob:** Excellent repositioning within charge count; the charge system means it's BURSTS of mobility, not continuous mobility.

---

## Sources

- Flame Dash PoE Wiki: https://pathofexile.fandom.com/wiki/Flame_Dash
- PoE movement skills ranking article: goldenhorsegaming.com — confirms utility role
- "Flame Dash Ignite Elementalist" guide (odealo, 3.19) — the only found example of Flame Dash as primary damage; classified as gimmick
- Knowledge base (kb) — confirmed widespread utility role from training data
- V4-r2 §F4 mint-list commission: "LOW | poe1 Flame Dash | B5 | utility not kit identity — candidate for a NO-MINT recommendation"
