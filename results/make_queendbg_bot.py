"""Debug copy of v11c in queen mode that logs the queen's state each turn (LOG QN).
Not a bot to use: it only adds LOG lines."""
import re, shutil
from pathlib import Path
src, dst = Path("results/v11c-bot"), Path("results/v11c-queendbg-bot")
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".unswbc-build"))
p = dst / "params.hpp"; s = p.read_text()
for k, v in {"CPP_QUEEN": 1, "CPP_QUEEN_KB": 1, "CPP_QUEEN_SAFE_MULT": 4.0, "CPP_QUEEN_REACH_PEN": 300.0,
             "CPP_QUEEN_DEADEND": 12, "CPP_QUEEN_GUARD_PEN": 200.0}.items():
    s, n = re.subn(rf"(inline constexpr \w+ {k} = )[^;]+;", rf"\g<1>{v};", s); assert n == 1, k
p.write_text(s)
b = dst / "v6_brain.hpp"; t = b.read_text(encoding="utf8")
a = "    std::string turn(const Obs& obs) {\n        mover_log.clear();\n        std::string action = decide(obs);\n"
assert a in t
add = ('        if (init.id <= 1) {\n'
       '            int legal = 0; for (char d : DIRS) legal += obs.passable(CENTER, d);\n'
       '            int ens = 0; for (int k = 0; k < 49; ++k) ens += obs.occ[k] && obs.occ[k]->head && obs.occ[k]->team != init.team;\n'
       '            char buf[160]; std::snprintf(buf, sizeof buf, "\nLOG QN r%d len %d legal %d enemies %d units %d act %s",\n'
       '                obs.round, obs.length, legal, ens, obs.unit_count, action.empty() ? "FEED/NONE" : action.substr(0, 12).c_str());\n'
       '            action += buf;\n'
       '        }\n')
t = t.replace(a, a + add, 1)
b.write_text(t, encoding="utf8")
print("wrote", dst)
