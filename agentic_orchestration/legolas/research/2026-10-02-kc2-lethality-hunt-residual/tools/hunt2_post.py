"""Runner for post-registration diagnostic arms: registers arms_post, then hunt2.main()."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import arms_post  # noqa: F401
import hunt2
hunt2.main()
