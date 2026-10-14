import json, os, sys
from pathlib import Path
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"
from bcsim import match
if __name__ == "__main__":
    out = []
    for m, a, b in [("maps/trophy.map", "versions/v7", "opponents/splitter"),
                    ("maps/default_small.map", "versions/v6", "versions/v3"),
                    ("maps/server/Portals.map", "versions/v7", "versions/v6"),
                    ("maps/server/Slithery_Fight.map", "versions/v3", "opponents/greedy")]:
        r = match.play(Path(m), Path(a), Path(b))
        out.append([m, a, b, r.winner, r.rounds, r.a_length, r.b_length, r.a_dragons, r.b_dragons, r.deaths, r.error])
        print(out[-1], flush=True)
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
