"""Debug copy of v10 that logs founders' per-move score breakdown (rounds <= 40).

Not a bot to use: it only adds LOG lines. Built from results/v10c-bot.
"""
import shutil
from pathlib import Path

src, dst = Path("results/v10c-bot"), Path("results/v10dbg-bot")
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".unswbc-build"))
p = dst / "v6_brain.hpp"
s = p.read_text(encoding="utf8")

def after(anchor, text, count=1):
    global s
    assert s.count(anchor) >= 1, anchor
    s = s.replace(anchor, anchor + text, count)

# globals for the debug trace
s = s.replace("namespace v6 {", "namespace v6 {\ninline std::string g_dbg; inline bool g_dbg_on = false;\n", 1)
# per-move marks: the change in `value` since the last mark
after("    for (std::size_t mi = 0; mi < remaining.size(); ++mi) {",
      "\n        double dbg_last = 0; std::string dbg_line;"
      "\n        auto mark = [&](const char* name, double v) { if (g_dbg_on) { char b[64]; std::snprintf(b, sizeof b, \" %s=%.1f\", name, v - dbg_last); dbg_line += b; dbg_last = v; } };")
after("        double value = tm.food * (protectedFlag ? params::PROTECT_FOOD_MULT : 1.0);", "\n        mark(\"food\", value);")
after("        value += (params::W_UNSEEN * tm.unseen + params::W_STALE * tm.stale) / static_cast<double>(params::N_SEARCH);",
      "\n        mark(\"explore\", value);")
after("            value -= params::CPP_DEADEND_PEN;", "\n        mark(\"safety\", value);")
after("            value += add;\n        }", "\n        mark(\"hunt\", value);")
after("            value += params::W_GOAL * tm.progress * (poor ? params::POOR_MULT : 1.0) * (protectedFlag ? params::KING_GOAL_MULT : 1.0);\n        }",
      "\n        mark(\"goal\", value);")
after("            value += params::W_HUB * std::max(tm.hub, far) / crowd;\n        }", "\n        mark(\"hub\", value);")
s = s.replace("        value += params::W_V3 * v3[direction];",
              "        mark(\"misc\", value);\n        value += params::W_V3 * v3[direction];\n        mark(\"v3\", value);", 1)
s = s.replace("        scores.emplace_back(direction, value);",
              "        if (g_dbg_on) { char b[80]; std::snprintf(b, sizeof b, \"\\nLOG DBG r%d dir %c total=%.1f\", obs.round, direction, value); g_dbg += b; g_dbg += dbg_line; }\n        scores.emplace_back(direction, value);", 1)
# switch the trace on for founders in the opening and attach it to the reply
s = s.replace("    std::string turn(const Obs& obs) {\n        std::string action = decide(obs);",
              "    std::string turn(const Obs& obs) {\n        g_dbg.clear();\n        g_dbg_on = obs.round <= 40 && (!born_round || *born_round == 0);\n"
              "        std::string action = decide(obs);\n"
              "        if (g_dbg_on && !action.empty()) {\n"
              "            char b[160]; std::snprintf(b, sizeof b, \"\\nLOG DBG r%d id%d head %d,%d len %d hubs %d goal %d chose %s\", obs.round, init.id,"
              " obs.x[CENTER], obs.y[CENTER], obs.length, (int)memory.hubs.size(), memory.goal ? *memory.goal : -1, action.substr(0, 7).c_str());\n"
              "            action += b; action += g_dbg;\n        }\n        g_dbg_on = false;", 1)
p.write_text(s, encoding="utf8")
print("debug bot written:", dst)
