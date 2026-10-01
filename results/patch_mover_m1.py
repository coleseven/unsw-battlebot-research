"""One-off patch: R5 mover hooks in cppbot (M1). Run once from the repo root."""
from pathlib import Path

p = Path("cppbot/v6_brain.hpp")
s = p.read_text(encoding="utf8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


# 1. v3_scores can hand back its raw 24-feature rows
rep("inline std::unordered_map<char, double> v3_scores(const Obs& obs, char team, const std::vector<char>& dirs) {",
    "inline std::unordered_map<char, double> v3_scores(const Obs& obs, char team, const std::vector<char>& dirs,\n"
    "                                                  std::unordered_map<char, std::array<double, 24>>* rows_out = nullptr) {")
rep("        const auto& wt = params::CPP_V3_R4 ? model::WEIGHT_R4 : model::WEIGHT;\n",
    "        if (rows_out) (*rows_out)[d] = row;\n        const auto& wt = params::CPP_V3_R4 ? model::WEIGHT_R4 : model::WEIGHT;\n")

# 2. the trace struct, before score_moves
rep("// Returns scores in Python dict insertion order (attacks first, then moves).",
    """// ---- R5 mover (NEW_MOVER_PLAN.md) -------------------------------------------
// MoverTrace collects, for each ordinary candidate move, the incumbent's complete
// score S0, its v3 part, and the 64 mover features: 24 v3 inputs, 12 decision
// context (filled by Brain::decide), 28 candidate context. Raw S0 values sit in
// slots 36-38 until inference centres and scales them.
constexpr int MV_N = 64;
struct MoverTrace {
    bool want = false;
    int n_attacks = 0;
    std::array<double, 12> ctx{};       // decision context (slots 24-35)
    int target_age = -1;                // rounds since the beaconed king spoke, -1 = not a beacon target
    std::vector<char> dirs;
    std::vector<double> s0, v3c;
    std::vector<std::array<double, MV_N>> f;
};

// Returns scores in Python dict insertion order (attacks first, then moves).""")

# 3. score_moves signature
rep("                                                        bool protectedFlag, const std::optional<CashTarget>& cash,\n"
    "                                                        double t0 = -1, int born = -1) {",
    "                                                        bool protectedFlag, const std::optional<CashTarget>& cash,\n"
    "                                                        double t0 = -1, int born = -1, MoverTrace* trace = nullptr) {")
rep("    if (usePath || params::CPP_HUB_GRAD > 0 || (params::CPP_KING_GRAD > 0 && cash.has_value())) pd.build(mem, obs);",
    "    bool tracing = trace != nullptr && trace->want;\n"
    "    if (usePath || params::CPP_HUB_GRAD > 0 || (params::CPP_KING_GRAD > 0 && cash.has_value()) || tracing) pd.build(mem, obs);")
rep("        if (gain >= params::ATTACK_MIN_GAIN) scores.emplace_back(d, params::W_ATTACK + params::W_TRADE * gain);",
    "        if (gain >= params::ATTACK_MIN_GAIN) { scores.emplace_back(d, params::W_ATTACK + params::W_TRADE * gain); if (trace) ++trace->n_attacks; }")
rep("    auto v3 = v3_scores(obs, team, remaining);\n",
    "    std::unordered_map<char, std::array<double, 24>> v3rows;\n"
    "    auto v3 = v3_scores(obs, team, remaining, tracing ? &v3rows : nullptr);\n")

# 4. per-candidate features, after the complete score
rep("""        value += params::W_V3 * v3[direction];
        value += params::W_STRAIGHT * (direction == obs.facing ? 1.0 : 0.0);
        scores.emplace_back(direction, value);""",
    """        value += params::W_V3 * v3[direction];
        value += params::W_STRAIGHT * (direction == obs.facing ? 1.0 : 0.0);
        scores.emplace_back(direction, value);
        if (tracing) {
            std::array<double, MV_N> f{};
            const auto& row = v3rows[direction];
            for (int j = 0; j < 24; ++j) f[j] = row[j];
            int w = mem.width, h = mem.height;
            double span = static_cast<double>(w + h);
            auto clip = [](double v, double lo, double hi) { return std::max(lo, std::min(hi, v)); };
            double v3part = params::W_V3 * v3[direction];
            f[36] = value; f[37] = v3part; f[38] = value - v3part;          // raw; centred/scaled at inference
            f[39] = direction == obs.facing ? 1.0 : 0.0;
            // topology
            f[40] = portal ? 1.0 : 0.0;
            int hx = obs.x[CENTER], hy = obs.y[CENTER], dxv = std::abs(dest % w - hx), dyv = std::abs(dest / w - hy);
            bool in_view = std::min(dxv, w - dxv) <= 3 && std::min(dyv, h - dyv) <= 3;
            f[41] = in_view ? 1.0 : 0.0;
            f[42] = clip((obs.round - mem.nav.seen[dest]) / 50.0, 0.0, 1.0);
            f[43] = clip(tm.room / std::max(1.0, static_cast<double>(obs.length)), 0.0, 4.0) / 4.0;
            f[44] = tm.exits / 3.0;
            int known = 0; for (char e : DIRS) known += mem.nav.edges[mem.nav.edge_key(dest, e)] != NONE;
            f[45] = known / 4.0;
            // resources: nearest known hub by walking distance through this move
            f[46] = (in_view || mem.pearl.count(dest)) ? 1.0 : 0.0;
            { auto pit = mem.pearl.find(dest); f[47] = (pit != mem.pearl.end() && pit->second == obs.round) ? 1.0 : 0.0; }
            if (!mem.hubs.empty()) {
                double best_after = 1e9, best_now = 1e9;
                for (auto& [hub, _] : mem.hubs) {
                    double sl = torus_distance(dest, hub, w, h);
                    double after = pd.eff(direction, hub, static_cast<int>(sl));
                    auto it = pd.dist.find(hub);
                    double now = it != pd.dist.end() ? it->second : torus_distance(start, hub, w, h);
                    if (after < best_after) { best_after = after; best_now = now; }
                }
                f[48] = clip(best_after / span, 0.0, 1.0);
                f[49] = clip(best_now - best_after, -2.0, 2.0) / 2.0;
            }
            f[50] = mem.hub_best_abs > 0 ? 1.0 : 0.0;
            f[51] = clip(mem.hub_best_abs, 0.0, 5.0) / 5.0;
            // collection target
            if (cash.has_value()) {
                double sl = torus_distance(dest, cash->head, w, h);
                double after = pd.eff(direction, cash->head, static_cast<int>(sl));
                auto it = pd.dist.find(cash->head);
                double now = it != pd.dist.end() ? it->second : torus_distance(start, cash->head, w, h);
                f[52] = clip(after / span, 0.0, 1.0);
                f[53] = clip(now - after, -2.0, 2.0) / 2.0;
                f[54] = trace->target_age >= 0 ? clip(trace->target_age / 10.0, 0.0, 1.0) : 0.0;
                f[55] = trace->target_age >= 0 ? 1.0 : 0.0;
                f[56] = (cash->front.has_value() && dest == *cash->front) ? 1.0 : 0.0;
                f[57] = cash->local >= 0 ? 1.0 : 0.0;
            }
            // interactions
            int fh = 0; for (int m : th.mates) if (torus_distance(dest, m, w, h) <= 2) ++fh;
            int eh = 0, lower = 0, higher = 0, big = 0;
            for (auto& [cell, pid] : enemy_heads) {
                int dd = torus_distance(dest, cell, w, h);
                if (dd <= 2) ++eh;
                if (dd == 1) { if (pid < did) lower = 1; else higher = 1; }
                if (dd <= 3) big = std::max(big, enemy_len.count(pid) ? enemy_len[pid] : 1);
            }
            f[58] = std::min(fh, 4) / 4.0;
            f[59] = std::min(eh, 4) / 4.0;
            f[60] = lower; f[61] = higher;
            int own_seen = 0; for (int k = 0; k < 49; ++k) own_seen += obs.occ[k] && obs.occ[k]->id == did;
            f[62] = clip(own_seen / std::max(1.0, static_cast<double>(obs.length)), 0.0, 1.0);
            f[63] = clip(big / std::max(1.0, static_cast<double>(obs.length)), 0.0, 4.0) / 4.0;
            trace->dirs.push_back(direction);
            trace->s0.push_back(value);
            trace->v3c.push_back(v3part);
            trace->f.push_back(f);
        }""")

# 5. decide(): fill context, log, apply the residual
rep("""        auto scores = score_moves(memory, obs, init.team, init.id, protectedFlag, target, t0, *born_round);""",
    """        MoverTrace trace;
        trace.want = params::CPP_MOVER != 0 || params::CPP_MOVER_LOG > 0;
        if (trace.want) {
            int age = obs.round - *born_round;
            int known = 0; for (int e : memory.nav.edges) known += e != NONE;
            double rate = 0; int spawns = 0;
            for (int k = 0; k < 49; ++k) if (obs.pearl_in[k] >= 0) { ++spawns; rate += 1.0 / (1 + obs.pearl_in[k]); }
            trace.ctx = {obs.round / 500.0, (500 - obs.round) / 500.0,
                         std::log(1.0 + obs.length) / std::log(65.0),
                         obs.unit_count / static_cast<double>(std::max(1, init.unit_limit)),
                         std::min(age, 100) / 100.0, *born_round == 0 ? 1.0 : 0.0,
                         protectedFlag ? 1.0 : 0.0, target ? 1.0 : 0.0,
                         memory.hubs.empty() ? 0.0 : 1.0,
                         known / static_cast<double>(std::max<std::size_t>(1, memory.nav.edges.size())),
                         std::min(rate, 5.0) / 5.0, spawns > 0 ? 1.0 : 0.0};
            if (target && target->local < 0 && params::CPP_KING_BEACON) trace.target_age = obs.round - king_round;
        }
        auto scores = score_moves(memory, obs, init.team, init.id, protectedFlag, target, t0, *born_round, &trace);""")

rep("""        return std::string("MOVE ") + best_dir;
    }
};""",
    """        if (trace.want && trace.n_attacks == 0 && trace.dirs.size() >= 2 && trace.dirs.size() == scores.size()) {
            for (auto& fv : trace.f) for (int j = 0; j < 12; ++j) fv[24 + j] = trace.ctx[j];
            if (params::CPP_MOVER) best_dir = mover_choice(trace, best_dir);
            if (params::CPP_MOVER_LOG > 0 && (init.id * 31 + obs.round) % params::CPP_MOVER_LOG == 0)
                mover_log = mover_line(obs, trace, best_dir);
        }
        return std::string("MOVE ") + best_dir;
    }

    // R5 residual: q(a) = q0(a) + lambda * 2 tanh(f(a)), q0 = (S0 - mean S0) / scale;
    // override the incumbent's a0 only if q(a*) - q(a0) > tau (ties keep a0).
    // With the generated zero weights this returns a0 exactly.
    char mover_choice(const MoverTrace& t, char a0) const {
        std::size_t n = t.dirs.size();
        double mean = 0; for (double v : t.s0) mean += v; mean /= n;
        double scale = std::max(1e-6, mover::SCORE_SCALE);
        std::vector<double> q(n);
        std::size_t i0 = 0;
        for (std::size_t i = 0; i < n; ++i) {
            if (t.dirs[i] == a0) i0 = i;
            std::array<double, MV_N> x = t.f[i];
            x[36] = (t.s0[i] - mean) / scale;
            x[37] = t.v3c[i] / scale;
            x[38] = (t.s0[i] - t.v3c[i] - mean) / scale;
            double out = mover_forward(x);
            if (!std::isfinite(out)) return a0;
            q[i] = x[36] + params::CPP_MOVER_LAMBDA * 2.0 * std::tanh(out);
        }
        std::size_t best = i0;
        for (std::size_t i = 0; i < n; ++i) if (q[i] > q[best]) best = i;
        return (q[best] - q[i0] > params::CPP_MOVER_TAU) ? t.dirs[best] : a0;
    }
    static double mover_forward(const std::array<double, MV_N>& raw) {
        std::array<double, MV_N> x;
        for (int j = 0; j < MV_N; ++j) x[j] = (raw[j] - mover::MEAN[j]) / mover::STD[j];
        double out = mover::B2;
        for (int u = 0; u < mover::HIDDEN; ++u) {
            double a = mover::B1[u];
            for (int j = 0; j < MV_N; ++j) a += mover::W1[u * MV_N + j] * x[j];
            if (a > 0) out += mover::W2[u] * a;
        }
        return out;
    }
    std::string mover_log;
    std::string mover_line(const Obs& obs, const MoverTrace& t, char chosen) const {
        char b[64];
        std::snprintf(b, sizeof b, "\\nLOG MV %d %d %c %zu", obs.round, init.id, chosen, t.dirs.size());
        std::string out = b;
        for (std::size_t i = 0; i < t.dirs.size(); ++i) {
            out += std::string("\\nLOG MVC ") + t.dirs[i];
            for (int j = 0; j < MV_N; ++j) { std::snprintf(b, sizeof b, " %.6g", t.f[i][j]); out += b; }
        }
        return out;
    }
};""")

# 6. attach the log to the reply (turn()), last so it never changes the action
rep("""    std::string turn(const Obs& obs) {
        std::string action = decide(obs);
        if (action.empty()) return action;""",
    """    std::string turn(const Obs& obs) {
        mover_log.clear();
        std::string action = decide(obs);
        if (action.empty()) return action;
        action += mover_log;""")

rep('#include "v6.hpp"', '#include "v6.hpp"\n#include "mover.hpp"')
p.write_text(s, encoding="utf8")
print("patched v6_brain.hpp")
