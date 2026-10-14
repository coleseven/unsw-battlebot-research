import os, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from bcsim import match
d = Path("results/20260928-140413-ablate-2970a3/variants/dead")
def load(_):
    t = time.time(); match.build_cpp_lib(d); return round(time.time() - t, 3)
if __name__ == "__main__":
    t = time.time(); match.build_cpp_lib(d); print(f"main process: {time.time()-t:.1f}s")
    with ProcessPoolExecutor(8) as ex:
        print("8 worker processes, seconds each:", list(ex.map(load, range(8))))
