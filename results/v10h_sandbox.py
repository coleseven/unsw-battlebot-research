import subprocess, sys
from bcsim import guard
U = r"C:\Users\Sea7\AppData\Local\Python\pythoncore-3.14-64\Scripts\unswbc.exe"
with guard.slot("v10h-sandbox"):
    for m, opp, seed in (("maps/big_empty.map", "sparring/cpp_nicked_v92", 7), ("maps/schooltime.map", "sparring/cpp_nicked_v92", 8), ("maps/default.map", "versions/v10", 9)):
        out = f"results/v10h-sandbox/{m.split('/')[-1][:-4]}.replay"
        r = subprocess.run([U, "run", m, "versions/v10h", opp, "--sandbox", "--seed", str(seed), "--no-logs", "-o", out], capture_output=True, text=True)
        print(m, r.returncode); print(r.stdout[-1500:]); print(r.stderr[-800:], flush=True)
