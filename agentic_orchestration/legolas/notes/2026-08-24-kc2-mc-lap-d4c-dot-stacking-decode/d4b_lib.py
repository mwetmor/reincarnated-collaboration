"""D-4b shared substrate access. READ-ONLY on every vendor path."""
import sys, pathlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts')
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file
from gd_arz_adapter_2026_07_24 import ArzArchive

VENDOR_FULL = pathlib.Path('/Users/admin/Games/vendor/grim-dawn')                       # full Win install (has Game.dll)
VENDOR_E3   = pathlib.Path('/Users/admin/Games/vendor/grim-dawn-edition-III-20260808')  # Lap I's magnitude source
