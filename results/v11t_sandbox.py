from bcsim import queen_runtime
queen_runtime.activate()
import unswbc
from unswbc import cli
from bcsim import guard
with guard.slot("v11t-sandbox"):
    for m, opp in (("maps/v129/unsw.map", "sparring/cpp_nicked_v92"), ("maps/v129/australia.map", "sparring/cpp_nicked_v92"),
                   ("maps/v129/schooltime.map", "versions/v11q"), ("maps/v129/islands.map", "sparring/cpp_nicked_v75"), ("maps/v129/trophy.map", "sparring/nicked_lab")):
        print("##", m, unswbc.__version__, flush=True)
        try:
            cli.main(["run", m, "versions/v11t", opp, "--sandbox", "--seed", "51", "--no-logs", "-o", "results/v11t-sandbox"])
        except SystemExit as e:
            print("exit", e.code, flush=True)
print("SANDBOX DONE", flush=True)
