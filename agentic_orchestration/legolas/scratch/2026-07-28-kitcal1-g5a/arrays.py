import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G = R.G
for n in range(1,7):
    p=f"records/skills/nonplayerskills/passive/armorbase0{n}.dbr"
    for a in R.ARCS:
        if p in G.arc(a).records:
            r=G.arc(a).read_record(p)
            lm=r.get("characterLifeModifier")
            print(f"armorbase0{n} [{a}] len={len(lm) if isinstance(lm,list) else lm} first25={lm[:25] if isinstance(lm,list) else lm}")
print()
for b in ["bio_zombie_01","bio_hero_standard_01","bio_boss_standard_01","bio_boar_01","bio_champion_standard_01"]:
    p=f"records/creatures/enemies/bios/{b}.dbr"
    for a in R.ARCS:
        if p in G.arc(a).records:
            r=G.arc(a).read_record(p)
            print(f"{b} [{a}] life={r.get('characterLife')} mana={r.get('characterMana')}")
