"""Post-screen matched control: unchanged additive versus v2 on portal maps."""

import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

SOURCE = RESULTS / "20260924-172250-v4-additive-9c22dc/bots/additive"
V2 = ROOT / "versions/v2"
PORTAL_RUN = RESULTS / "20260924-183910-v4-visible-portal-v2-fb319a"


def main():
    source_plan = json.loads((PORTAL_RUN / "plan.json").read_text())
    assert bot_hash(SOURCE) == "bf33497158a49a7b"
    assert bot_hash(V2) == source_plan["v2_hash"]
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-portal-control-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(SOURCE, out / "bots/additive")
    population.snapshot(V2, out / "bots/reference_v2")
    (out / "maps").mkdir()
    maps = []
    for name in source_plan["maps"]:
        source = Path(name)
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(dest)
    assert len({map_signature(p) for p in maps}) == len(maps) == 5
    plan = {"question": "Did visible-only portals change the 7-3 v2 result?",
            "provenance": "Post-screen diagnostic control, not a predeclared promotion test.",
            "compared_run": str(PORTAL_RUN), "candidate_hash": bot_hash(SOURCE),
            "v2_hash": bot_hash(V2), "live_hash": bot_hash(ROOT / "mybot"),
            "maps": [str(p) for p in maps],
            "map_hashes": {str(p): file_hash(p) for p in maps},
            "seed": source_plan["seed"], "workers": 1, "games": 10}
    population.write_json(out / "plan.json", plan)
    games = guarded.stage(out, "vs-v2", [out / "bots/additive"],
                          [out / "bots/reference_v2"], maps, [plan["seed"]], 1, True)
    assert len(games) == 10 and bot_hash(SOURCE) == plan["candidate_hash"]
    t = population.tally(games, "additive")
    result = {"wins": t.w, "draws": t.d, "losses": t.l, "score": t.score}
    population.write_json(out / "comparison.json", result)
    print(out, flush=True)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
