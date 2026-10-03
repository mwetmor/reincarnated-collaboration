# jack-ryan H-5 instrument: re-run star-lord's v3.11 closure captures (14 + 6 bare + 2 sweeps) in a scratch
# copy of engine 969fbd8d (instrument path constants relocated; see relocation.diff). Nothing else changed.
import sys, time
from reincarnated.export import kc2_v3p11_closure as C
t = time.time()
C.run_captures("kc2-v3p11-JR", sys.argv[1], parallel=int(sys.argv[2]) if len(sys.argv) > 2 else 3)
print("elapsed_s", round(time.time() - t, 1))
