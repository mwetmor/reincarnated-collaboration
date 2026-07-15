"""Gate-A frozen label extraction — 2026-07-14 (gandalf, prereg amendment A1).

Re-derives the SIX CONFIRMED cross-franchise groups (handoff View-2 table:
WHIRLWIND 15 / TOTEM-SENTRY 26 / TRAP-MINE 24 / CHANNELED-BEAM 9 / AURA 8 /
MINION-PET 7) as deterministic FCA concept extents, lineage of
family-discovery-poc-rerank.py, corrected for the post-A.5 snapshot:
`negative=0` added (A.5 keyed the 38 corpses as combat-kit rows; the original
POC ran when they were unkeyed — the original denominator minus d2-sacrifice).

Output: gate-a-group-labels CSV (kit_id, group, intent-rationale) — the frozen
artifact Gate A consumes. Committed BEFORE any decomposition runs.
"""
import sqlite3, csv, sys
from collections import defaultdict, deque, Counter

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/design-inputs/2026-07-14-gate-a-group-labels.csv"
NAMES = ["movement","delivery","amp","geometry","treatment","function","defense",
         "economy","proxy","range","tempo","commit","activation","dependency"]
MASK = {"unknown","blank","post-cutoff-deferred","post-cutoff"}
MINSUP = 5

con = sqlite3.connect(DB)
rows = con.execute(
    "SELECT k.kit_id, k.cell_key, c.game FROM canon_engine_key k "
    "JOIN canon_corpus c ON c.kit_id=k.kit_id "
    "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=0"
).fetchall()
kit_ids, kit_items, kit_game = [], [], []
for kid, ck, game in rows:
    v = ck.split("|")
    kit_ids.append(kid); kit_game.append(game)
    kit_items.append(frozenset((NAMES[i], v[i]) for i in range(14) if v[i] not in MASK))
N = len(kit_items)
print(f"denominator N={N} (combat-kit, keyed, negative=0)")

ext = defaultdict(set)
for k, s in enumerate(kit_items):
    for it in s: ext[it].add(k)
p_item = {it: len(e)/N for it, e in ext.items()}
freq_items = [it for it, e in ext.items() if len(e) >= MINSUP]

def closure_of_extent(E):
    it = None
    for k in E: it = kit_items[k] if it is None else (it & kit_items[k])
    return frozenset(it) if it else frozenset()
def extent_of_intent(C):
    E = None
    for it in C: E = set(ext[it]) if E is None else (E & ext[it])
    return E if E is not None else set(range(N))

c0 = closure_of_extent(set(range(N)))
seen = {c0: extent_of_intent(c0)}; work = deque([c0])
while work:
    C = work.popleft(); E = seen[C]
    for it in freq_items:
        if it in C: continue
        E2 = E & ext[it]
        if len(E2) < MINSUP: continue
        C2 = closure_of_extent(E2)
        if C2 not in seen: seen[C2] = E2; work.append(C2)

def lift(C, E):
    prod = 1.0
    for it in C: prod *= p_item[it]
    return (len(E)/N) / prod if prod > 0 else 0.0

# ---- signature match: locate each confirmed group by content anchor, then pick
#      the concept whose (support, lift) best matches the confirmed record.
TARGETS = [
    # (name, anchor item test, confirmed support, confirmed lift)
    ("WHIRLWIND",      lambda C: ("geometry","whirlwind") in C, 15, 2120.0),
    ("TOTEM-SENTRY",   lambda C: ("geometry","totem") in C,     26,  224.0),
    ("TRAP-MINE",      lambda C: ("activation","triggered") in C, 24, 1426.0),
    ("CHANNELED-BEAM", lambda C: ("delivery","beam") in C,       9,  233.0),
    ("AURA",           lambda C: ("geometry","aura") in C,       8, 1231.0),
    ("MINION-PET",     lambda C: ("function","taunt") in C or ("geometry","minion") in C or ("proxy","heavy") in C, 7, 622.0),
]

candidate = defaultdict(list)   # kit index -> [(group, intent_size, intent_str)]
report = []
for name, anchor, sup_t, lift_t in TARGETS:
    cands = [(C, E) for C, E in seen.items() if anchor(C) and len(E) >= MINSUP]
    if not cands:
        print(f"!! {name}: NO candidate concepts"); continue
    # score: exact-support first, then lift proximity (log-scale)
    import math
    def score(ce):
        C, E = ce
        return (abs(len(E)-sup_t), abs(math.log(max(lift(C,E),1e-9)) - math.log(lift_t)))
    cands.sort(key=score)
    C, E = cands[0]
    intent = " · ".join(f"{c}={v}" for (c, v) in sorted(C, key=lambda p: NAMES.index(p[0])))
    games = sorted({kit_game[k] for k in E})
    report.append((name, len(E), lift(C,E), len(games), intent))
    print(f"\n{name}: support={len(E)} (target {sup_t})  lift={lift(C,E):.1f} (target {lift_t})  games={len(games)}")
    print(f"  intent: {intent}")
    print(f"  games: {', '.join(games)}")
    for k in sorted(E):
        candidate[k].append((name, len(C), intent))

# ---- overlap resolution (gandalf ruling, prereg A1): a kit claimed by two
#      concepts is assigned to the MOST SPECIFIC intent (more pinned coords =
#      tighter identity). Matches genre truth on all three 2026-07-14 cases:
#      d2-auradin -> AURA (not TRAP-MINE); tl2-bot-engineer / tli-moto-bots ->
#      MINION-PET (mobile taunt-pets, not stationary sentries).
labels = {}
for k, opts in candidate.items():
    if len(opts) > 1:
        opts.sort(key=lambda o: -o[1])
        print(f"  OVERLAP {kit_ids[k]}: {[o[0] for o in opts]} -> {opts[0][0]} (most-specific, {opts[0][1]} pins)")
    labels[k] = (opts[0][0], opts[0][2])

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kit_id","group","group_intent_rationale"])
    for k in sorted(labels, key=lambda k: (labels[k][0], kit_ids[k])):
        w.writerow([kit_ids[k], labels[k][0], labels[k][1]])
print(f"\nwrote {len(labels)} labeled kits -> {OUT}")
print("summary:", Counter(g for g,_ in labels.values()))
