from pathlib import Path
import unswbc.engine as E
from bcsim import guard, match, replay as rp
out = Path("results/pd-diag/hubdbg.replay")
with guard.slot("pd-hubdbg"):
    r = match.play(Path("maps/server/Prisoners_Dilemma.map"), Path("results/v10h-hubdbg-bot"), Path("sparring/cpp_nicked_v92"), seed=281001, replay_to=out, debug=E.DEBUG_ALL)
print(r.winner, r.reason, r.rounds)
rr = rp.load(out)
logs = [str(ev[2]) for ev in rr.events if ev[0] == rp.DRAGON_LOG and "HUB" in str(ev[2])]
print(len(logs), "hub logs")
for l in logs:
    rnd = int(l.split()[1][1:])
    if rnd in (5, 20, 40, 60, 100, 150): print(l)
