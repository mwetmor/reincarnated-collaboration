#!/usr/bin/env python3
"""Fetch the second-source pages gen_j4b.py verifies against (read-only GETs) and write
whitespace-collapsed plain text into ./sources (or $J4B_SOURCES).

Basin Wiki pages are live wiki pages: if they are edited, the tables can change and the
generator will abort with a MISMATCH naming the cell. That abort is the intended behaviour.
Pages as read for the 2026-10-01 commit: see README "Source list".
"""
import html, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("J4B_SOURCES", os.path.join(HERE, "sources"))
UA = "Mozilla/5.0 (research; read-only)"  # fetched with curl (system CA store); TLS verification stays on
BASIN = "https://www.theamazonbasin.com/wiki/index.php?title="
PAGES = {
    "b_Fire_Ball.txt": BASIN + "Fire_Ball",
    "b_Meteor.txt": BASIN + "Meteor",
    "b_Fire_Bolt.txt": BASIN + "Fire_Bolt",
    "b_Fire_Mastery.txt": BASIN + "Fire_Mastery",
    "b_Warmth.txt": BASIN + "Warmth",
    "arreat_fire.txt": "https://classic.battle.net/diablo2exp/skills/sorceress-fire.shtml",
}

def to_text(raw):
    s = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", raw)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s)

os.makedirs(SRC, exist_ok=True)
for fn, url in PAGES.items():
    raw = subprocess.run(["curl", "-s", "-L", "--fail", "--max-time", "30", "-A", UA, url],
                         check=True, capture_output=True).stdout.decode("utf-8", errors="replace")
    open(os.path.join(SRC, fn), "w").write(to_text(raw))
    print(fn, url)
    time.sleep(1)
