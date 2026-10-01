"""Debug copy of v10n (current code) that logs each dragon's hubs, goal and timer knowledge every 5 rounds.
Not a bot to use: it only adds LOG lines. Built from versions/v10n (current code)."""
import shutil
from pathlib import Path
src, dst = Path("results/v10n-bot"), Path("results/v10n-hubdbg-bot")
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".unswbc-build", "FROZEN.txt"))
p = dst / "v6_brain.hpp"
s = p.read_text(encoding="utf8")
a = "    std::string turn(const Obs& obs) {\n        std::string action = decide(obs);\n        if (action.empty()) return action;\n"
assert a in s
b = a + ("        if (obs.round % 5 == 0 && obs.round <= 200) {\n"
         "            std::string l = \"\\nLOG HUB r\" + std::to_string(obs.round) + \" id\" + std::to_string(init.id) +\n"
         "                \" at \" + std::to_string(obs.x[CENTER]) + \",\" + std::to_string(obs.y[CENTER]) + \" len \" + std::to_string(obs.length) +\n"
         "                \" timers \" + std::to_string(memory.timer_max.size()) + \" goal \" + std::to_string(memory.goal ? *memory.goal : -1) + \" abs \" + std::to_string(memory.hub_best_abs).substr(0, 5) + \" hubs\";\n"
         "            for (auto& [c, v] : memory.hubs) l += \" \" + std::to_string(c % memory.width) + \",\" + std::to_string(c / memory.width) + \":\" + std::to_string(v).substr(0, 4);\n"
         "            action += l;\n        }\n")
s = s.replace(a, b, 1)
p.write_text(s, encoding="utf8")
print("wrote", dst)
