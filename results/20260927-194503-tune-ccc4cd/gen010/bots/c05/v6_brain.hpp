// V7 port, part 2: action_value (v3 features), tactics, core_search,
// core_king, core_split and the Brain turn order. See v6.hpp for the rules.
#pragma once

#include <cmath>
#include <ctime>
#include <deque>
#include <string>
#include <tuple>

#include "v6.hpp"

namespace v6 {

// ---- V7 section 5: CPU meter ------------------------------------------------
// On the judge, clock() advances with CPU points spent (0.1 s = 100M points),
// so this reads "points used so far" in normal play. Only consulted when the
// points budget (CPP_BUDGET) is on; with it off there are no clock reads and
// behaviour is byte-identical to the matching build.
inline double cpu_points() {
    return static_cast<double>(std::clock()) / CLOCKS_PER_SEC * 1e9;
}

// ---- tactics.py -------------------------------------------------------------
inline std::unordered_set<int> danger_cells(const Obs& obs, char team) {
    std::unordered_set<int> out;
    for (int k : obs.enemy_heads(team))
        for (char d : DIRS)
            if (obs.edge(k, d) == OPEN) { int n = Obs::step(k, d); if (n >= 0) out.insert(n); }
    return out;
}
inline int room(const Obs& obs, int start, int cap) {
    std::unordered_set<int> seen{start};
    std::vector<int> stack{start};
    while (!stack.empty() && static_cast<int>(seen.size()) < cap) {
        int k = stack.back(); stack.pop_back();
        for (char d : DIRS)
            if (obs.passable(k, d)) { int n = Obs::step(k, d); if (seen.insert(n).second) stack.push_back(n); }
    }
    return static_cast<int>(seen.size());
}
inline bool edge_of_window(int k) { int r = k / 7, c = k % 7; return r == 0 || r == 6 || c == 0 || c == 6; }

// ---- action_value.py: the 24 v3 features + linear model ---------------------
inline double v3_continuation(const Obs& obs, int k, std::unordered_set<int> visited, int depth) {
    if (depth == 0) return 0;
    int best = 0;
    for (char nd : DIRS) {
        int n = Obs::step(k, nd);
        if (n >= 0 && !visited.count(n) && obs.passable(k, nd)) {
            auto v2 = visited; v2.insert(n);
            best = std::max<int>(best, 1 + static_cast<int>(v3_continuation(obs, n, v2, depth - 1)));
            if (best == depth) break;
        }
    }
    return best;
}

// v3 score per requested direction (matching action_value.features + score)
inline std::unordered_map<char, double> v3_scores(const Obs& obs, char team, const std::vector<char>& dirs) {
    int did = obs.occ[CENTER] ? obs.occ[CENTER]->id : -1;
    std::unordered_set<int> re_enemy, re_friendly, re_later;
    for (int k = 0; k < 49; ++k) {
        auto& p = obs.occ[k];
        if (!p || !p->head || p->id == did) continue;
        bool friendly = (p->team == team);
        for (char d : DIRS) {
            if (obs.edge(k, d) != OPEN) continue;
            int n = Obs::step(k, d);
            if (n < 0) continue;
            (friendly ? re_friendly : re_enemy).insert(n);
            if (!friendly && p->id > did) re_later.insert(n);
        }
    }
    double length = std::min(obs.length, 64) / 64.0;
    double population = obs.unit_count / 64.0;
    std::unordered_map<char, double> out;
    std::unordered_set<int> blockedC{CENTER};
    for (char d : dirs) {
        int start = Obs::step(CENTER, d);
        auto paths = obs.bfs(start, &blockedC);
        double food = 0; bool food_any = false;
        double soon = 0; bool soon_any = false;
        double pearl_count = 0, spawn_count = 0, boundary = 0;
        for (auto& [k, dp] : paths) {
            int dist = dp.first;
            if (obs.pearl[k]) { double v = 1.0 / (dist + 1); if (!food_any || v > food) food = v; food_any = true; pearl_count += 1; }
            if (obs.pearl_in[k] >= 0) { spawn_count += 1; if (0 <= obs.pearl_in[k] && obs.pearl_in[k] <= dist + 1) { double v = 1.0 / (dist + 2); if (!soon_any || v > soon) soon = v; soon_any = true; } }
            if (k / 7 == 0 || k / 7 == 6 || k % 7 == 0 || k % 7 == 6) boundary += 1;
        }
        int exits = 0; for (char nd : DIRS) if (obs.passable(start, nd)) ++exits;
        double friendly = 0, enemy = 0, own = 0;
        for (int k = 0; k < 49; ++k) {
            auto& p = obs.occ[k];
            if (!p) continue;
            if (std::abs(k / 7 - start / 7) + std::abs(k % 7 - start % 7) <= 2) {
                if (p->team == team && p->id != did) friendly += 1;
                if (p->team != team) enemy += 1;
                if (p->id == did) own += 1;
            }
        }
        double space = paths.size() / 49.0;
        double cont = v3_continuation(obs, start, {CENTER, start}, 3);
        std::array<double, 24> row = {
            food, soon, pearl_count / 49.0, spawn_count / 49.0, space,
            exits / 3.0, (exits == 0) ? 1.0 : 0.0, (d == obs.facing) ? 1.0 : 0.0,
            friendly / 13.0, enemy / 13.0,
            re_enemy.count(start) ? 1.0 : 0.0, re_friendly.count(start) ? 1.0 : 0.0,
            re_later.count(start) ? 1.0 : 0.0, own / 13.0, boundary / 24.0,
            cont / 3.0, length, obs.round / 500.0, population,
            food * length, space * length, (friendly / 13.0) * population,
            exits / 3.0 * length, boundary / 24.0 * ((food == 0.0) ? 1.0 : 0.0)};
        double s = 0; for (int j = 0; j < 24; ++j) s += row[j] * model::WEIGHT[j];
        out[d] = s + model::BIAS;
    }
    return out;
}

// ---- core_search.py ---------------------------------------------------------
inline int torus_distance(int a, int b, int width, int height) {
    int ax = a % width, ay = a / width, bx = b % width, by = b / width;
    int dx = std::abs(ax - bx), dy = std::abs(ay - by);
    return std::min(dx, width - dx) + std::min(dy, height - dy);
}

// ---- V7 section 5: portal-aware path distances (CPP_PATH_DIST) --------------
// One BFS per turn from our head over remembered terrain (book portals
// included), ignoring dragons (they move). Gives, for each candidate move
// direction and a target cell, a path distance that follows real corridors and
// portals instead of the straight-line torus distance. Off (CPP_PATH_DIST=0)
// nothing is built and the straight-line terms are used unchanged.
struct PathDist {
    std::unordered_map<int, int> dist;    // cell -> path distance from head
    std::unordered_map<int, char> first;  // cell -> first step direction

    void build(const WorldMemory& mem, const Obs& obs) {
        int head = mem.cell(obs.x[CENTER], obs.y[CENTER]);
        int cap = mem.width * mem.height;
        dist[head] = 0; first[head] = 0;
        std::deque<int> q{head};
        int expanded = 0;
        while (!q.empty() && expanded < cap) {
            int c = q.front(); q.pop_front(); ++expanded;
            for (char d : DIRS) {
                auto nxt = mem.nav.destination(c, d);
                if (!nxt || dist.count(*nxt)) continue;
                dist[*nxt] = dist[c] + 1;
                first[*nxt] = first[c] ? first[c] : d;
                q.push_back(*nxt);
            }
        }
    }
    // Effective distance to `target` for a move in `dir`; the first step of the
    // real shortest path gets dist-1, others dist+1. Unreachable within the map
    // falls back to the straight-line distance passed in.
    double eff(char dir, int target, int fallback) const {
        auto it = dist.find(target);
        if (it == dist.end()) return fallback;
        auto fit = first.find(target);
        char fT = fit == first.end() ? 0 : fit->second;
        return (fT && dir == fT) ? std::max(0, it->second - 1) : it->second + 1;
    }
};
inline std::unordered_map<int, int> own_free_times(const WorldMemory& mem, const Obs& obs) {
    auto body = mem.trail_body(obs.length);
    std::unordered_map<int, int> out;
    if (!body) return out;
    for (int i = 0; i < static_cast<int>(body->size()); ++i) out[(*body)[i]] = obs.length - i + 1;
    return out;
}
inline bool blocked(const WorldMemory& mem, int cell, int arrival, char team, int did,
                    const std::unordered_map<int, int>& own_free) {
    const OccPart* part = mem.occupied.find(cell);
    if (part == nullptr) return false;
    if (part->team == team && part->id == did) {
        auto it = own_free.find(cell);
        int free = (it == own_free.end()) ? 1000000000 : it->second;
        return arrival < free;
    }
    return true;
}
inline std::unordered_map<char, int> legal_moves(const WorldMemory& mem, const Obs& obs, char team, int did,
                                                 std::unordered_map<char, int>* attacks, std::vector<char>* order) {
    int start = mem.cell(obs.x[CENTER], obs.y[CENTER]);
    std::unordered_map<char, int> out;
    for (char d : DIRS) {
        if (obs.length > 1 && didx(d) == OPP[didx(obs.facing)]) continue;
        int e = obs.edge(CENTER, d);
        if (e == KELP) continue;
        auto dest = mem.nav.destination(start, d);
        if (!dest) continue;
        if (e == OPEN) {
            int local = Obs::step(CENTER, d);
            if (local < 0) continue;
            auto& part = obs.occ[local];
            if (part) {
                if (attacks == nullptr || part->team == team || !part->head) continue;
                (*attacks)[d] = part->id;
            }
        } else if (mem.occupied.find(*dest) != nullptr) continue;
        out[d] = *dest;
        if (order) order->push_back(d);
    }
    return out;
}
struct Threats {
    std::unordered_set<int> enemy, friendly, ahead;
    std::vector<int> mates;
};
inline Threats head_threats(const WorldMemory& mem, const Obs& obs, char team, int did) {
    Threats t;
    for (int cell : mem.occupied.order) {
        const OccPart& p = *mem.occupied.find(cell);
        if (!p.head || p.seen != obs.round || p.id == did) continue;
        if (p.team == team) t.mates.push_back(cell);
        for (char d : DIRS) {
            if (didx(d) == OPP[didx(p.facing)]) continue;
            auto dest = mem.nav.destination(cell, d);
            if (dest) (p.team == team ? t.friendly : t.enemy).insert(*dest);
        }
        auto nc = mem.nav.destination(cell, p.facing);
        if (nc) { t.ahead.insert(*nc); auto second = mem.nav.destination(*nc, p.facing); if (second) t.ahead.insert(*second); }
    }
    return t;
}
// Voronoi-lite pearl targeting (CPP_VOR): visible head cells this turn.
struct VorCtx {
    std::vector<int> enemy, mates;
};
// Scale a pearl's value by who reaches it first: we arrive in hops + 1 moves; a
// visible enemy head strictly sooner takes it (x LOST), one arriving within 2
// moves after us contests it (x CONTEST, take it now); a teammate head strictly
// sooner should have it (x MATE, spread out over a hub).
inline double vor_mult(const WorldMemory& mem, int cell, int hops, const VorCtx& v) {
    int ours = hops + 1;
    int de = 1 << 30;
    for (int e : v.enemy) de = std::min(de, torus_distance(cell, e, mem.width, mem.height));
    double m = 1.0;
    if (de < ours) m = params::CPP_VOR_LOST;
    else if (de <= ours + 2) m = params::CPP_VOR_CONTEST;
    for (int t : v.mates)
        if (torus_distance(cell, t, mem.width, mem.height) < ours) { m *= params::CPP_VOR_MATE; break; }
    return m;
}
inline double food_value(const WorldMemory& mem, const Obs& obs, int cell, int hops, const VorCtx* vor = nullptr) {
    double value = 0;
    auto vit = mem.nav.visible.find(cell);
    if (vit != mem.nav.visible.end() && obs.pearl[vit->second]) value = params::W_PEARL / (1 + hops);
    else if (mem.pearl.count(cell)) value = params::W_MEM_PEARL / (1 + hops);
    if (vor != nullptr && value > 0) value *= vor_mult(mem, cell, hops, *vor);
    auto sit = mem.spawn_ready.find(cell);
    if (sit != mem.spawn_ready.end()) {
        int wait = sit->second - obs.round - hops;
        if (0 <= wait && wait <= params::H_SPAWN) value = std::max(value, params::W_SPAWN / (1 + hops + 0.2 * wait));
    }
    return value;
}
struct Terms { double food = 0, hub = 0, progress = 0; int unseen = 0, stale = 0, room = 0, exits = 0, expanded = 0; };

// `deadline` is an absolute cpu_points() value; < 0 means no meter (matching
// build). With it set (CPP_BUDGET on) the search also stops once the turn's CPU
// points reach the deadline, so a larger N_SEARCH is capped by real cost.
inline Terms search_one(const WorldMemory& mem, const Obs& obs, char team, int did, int dest, char direction,
                        const std::unordered_map<int, int>& own_free, double deadline = -1,
                        const VorCtx* vor = nullptr) {
    std::unordered_map<int, int> best; best[dest] = 0;
    using Node = std::tuple<int, int, int>;  // (cost, arrival, cell)
    std::priority_queue<Node, std::vector<Node>, std::greater<Node>> queue;
    queue.push({0, 1, dest});
    Terms tm;
    const auto& hub_area = mem.hub_area;
    bool has_goal = mem.goal.has_value();
    double base = 0;
    if (has_goal) base = torus_distance(mem.cell(obs.x[CENTER], obs.y[CENTER]), *mem.goal, mem.width, mem.height);
    while (!queue.empty() && tm.expanded < params::N_SEARCH) {
        if (deadline >= 0 && (tm.expanded & 31) == 0 && cpu_points() > deadline) break;
        auto [cost, arrival, cell] = queue.top(); queue.pop();
        auto bit = best.find(cell);
        if (bit == best.end() || cost != bit->second) continue;
        tm.expanded += 1;
        tm.food = std::max(tm.food, food_value(mem, obs, cell, arrival - 1, vor));
        if (has_goal) {
            double gained = base - torus_distance(cell, *mem.goal, mem.width, mem.height) - params::GOAL_STEP_COST * (arrival - 1);
            if (gained > tm.progress) tm.progress = gained;
        }
        if (!hub_area.empty()) {
            auto hit = hub_area.find(cell);
            if (hit != hub_area.end() && hit->second != 0) tm.hub = std::max(tm.hub, hit->second / (1 + (arrival - 1) / params::HUB_SCALE));
        }
        int seen_round = mem.nav.seen[cell];
        tm.unseen += (seen_round < 0) ? 1 : 0;
        tm.stale += (seen_round >= 0 && obs.round - seen_round >= params::STALE_ROUNDS) ? 1 : 0;
        if (arrival >= params::DEPTH_MAX) continue;
        for (char step : DIRS) {
            auto nxt = mem.nav.destination(cell, step);
            if (!nxt || blocked(mem, *nxt, arrival + 1, team, did, own_free)) continue;
            int new_cost = cost + 1 + (mem.nav.seen[*nxt] < 0 ? 1 : 0);
            auto nb = best.find(*nxt);
            if (nb == best.end() || new_cost < nb->second) { best[*nxt] = new_cost; queue.push({new_cost, arrival + 1, *nxt}); }
        }
    }
    tm.room = static_cast<int>(best.size());
    for (char step : DIRS) {
        if (didx(step) == OPP[didx(direction)]) continue;
        auto nxt = mem.nav.destination(dest, step);
        if (nxt && !blocked(mem, *nxt, 2, team, did, own_free)) tm.exits += 1;
    }
    return tm;
}

// ---- V7 section 5: lookahead beam (CPP_BEAM) --------------------------------
// A short beam over OUR OWN moves that simulates our body (growth on a known
// pearl, tail release otherwise) and treats other dragons and the cells enemy
// heads can reach as blocked. It demotes a first move whose best continuation
// gets trapped before the horizon, reusing W_LETHAL, so v6's immediate scoring
// is kept and only trap-prone moves are penalised. Off (CPP_BEAM=0) it is never
// called and scores are unchanged.
inline bool beam_is_food(const WorldMemory& mem, const Obs& obs, int cell) {
    auto vit = mem.nav.visible.find(cell);
    if (vit != mem.nav.visible.end() && obs.pearl[vit->second]) return true;
    return mem.pearl.count(cell) != 0;
}
inline int beam_room(const WorldMemory& mem, int head, const std::unordered_set<int>& body,
                     const std::unordered_set<int>& blockers, int cap) {
    std::unordered_set<int> seen{head};
    std::vector<int> st{head};
    while (!st.empty() && static_cast<int>(seen.size()) < cap) {
        int c = st.back(); st.pop_back();
        for (char d : DIRS) {
            auto n = mem.nav.destination(c, d);
            if (!n || seen.count(*n) || body.count(*n) || blockers.count(*n)) continue;
            seen.insert(*n); st.push_back(*n);
        }
    }
    return static_cast<int>(seen.size());
}
struct BeamNode { std::vector<int> body; char facing; };  // body is head-first

// Deepest ply (1..D) at which some line stays alive, starting AFTER `first_dir`.
inline int beam_survive(const WorldMemory& mem, const Obs& obs, const std::vector<int>& start_body,
                        char first_dir, int first_dest, const std::unordered_set<int>& blockers,
                        int width, int depth) {
    std::vector<int> body{first_dest};
    bool grew = beam_is_food(mem, obs, first_dest);
    for (int c : start_body) body.push_back(c);
    if (!grew) body.pop_back();
    std::vector<BeamNode> live{{body, first_dir}};
    int reached = 1;
    for (int ply = 2; ply <= depth && !live.empty(); ++ply) {
        std::vector<std::pair<int, BeamNode>> children;  // (room, node)
        for (auto& node : live) {
            int head = node.body.front();
            std::unordered_set<int> bodyset(node.body.begin(), node.body.end());
            for (char d : DIRS) {
                if (didx(d) == OPP[didx(node.facing)]) continue;
                auto nd = mem.nav.destination(head, d);
                if (!nd || blockers.count(*nd)) continue;
                bool g = beam_is_food(mem, obs, *nd);
                int tail = node.body.back();
                if (bodyset.count(*nd) && !(!g && *nd == tail)) continue;  // self-collision
                std::vector<int> nb; nb.reserve(node.body.size() + 1);
                nb.push_back(*nd);
                for (int c : node.body) nb.push_back(c);
                if (!g) nb.pop_back();
                std::unordered_set<int> nbset(nb.begin(), nb.end());
                int room = beam_room(mem, *nd, nbset, blockers, static_cast<int>(nb.size()) + 6);
                children.emplace_back(room, BeamNode{std::move(nb), d});
            }
        }
        if (children.empty()) break;
        std::stable_sort(children.begin(), children.end(),
                         [](auto& a, auto& b) { return a.first > b.first; });
        live.clear();
        for (int i = 0; i < width && i < static_cast<int>(children.size()); ++i)
            live.push_back(std::move(children[i].second));
        reached = ply;
    }
    return reached;
}
inline void beam_adjust(WorldMemory& mem, const Obs& obs, char team, int did,
                        std::vector<std::pair<char, double>>& scores,
                        const std::unordered_map<char, int>& moves) {
    auto start_body = mem.trail_body(obs.length);
    if (!start_body) return;  // body not fully known yet; leave scores unchanged
    std::unordered_set<int> blockers;
    for (int cell : mem.occupied.order) {
        const OccPart& p = *mem.occupied.find(cell);
        if (p.id != did) blockers.insert(cell);  // other dragons (teammates and enemies)
    }
    // cells any enemy head can step onto next turn: risky to enter
    for (int cell : mem.occupied.order) {
        const OccPart& p = *mem.occupied.find(cell);
        if (p.head && p.seen == obs.round && p.team != team)
            for (char d : DIRS) { auto n = mem.nav.destination(cell, d); if (n) blockers.insert(*n); }
    }
    int width = std::max(1, params::CPP_BEAM_WIDTH), depth = std::max(2, params::CPP_BEAM_DEPTH);
    for (auto& [dir, val] : scores) {
        auto it = moves.find(dir);
        if (it == moves.end()) continue;  // an attack move: leave its trade value alone
        int survived = beam_survive(mem, obs, *start_body, dir, it->second, blockers, width, depth);
        val -= params::W_LETHAL * (depth - survived) / static_cast<double>(depth);
    }
}

// cash target: (head cell, front cell or none, local k)
struct CashTarget { int head; std::optional<int> front; int local; };

// Returns scores in Python dict insertion order (attacks first, then moves).
inline std::vector<std::pair<char, double>> score_moves(WorldMemory& mem, const Obs& obs, char team, int did,
                                                        bool protectedFlag, const std::optional<CashTarget>& cash,
                                                        double t0 = -1, int born = -1) {
    bool budget = params::CPP_BUDGET != 0 && t0 >= 0;
    PathDist pd;
    bool usePath = params::CPP_PATH_DIST != 0;
    if (usePath) pd.build(mem, obs);
    bool hunter = !protectedFlag && obs.length <= params::HUNT_MAXLEN;
    bool attacker = !protectedFlag && obs.length <= params::ATTACK_MAXLEN;
    std::unordered_map<char, int> attacks_map;
    std::unordered_map<char, int>* attacks = attacker ? &attacks_map : nullptr;
    std::vector<char> move_order;
    auto moves = legal_moves(mem, obs, team, did, attacks, &move_order);
    std::vector<std::pair<char, double>> scores;
    if (moves.empty()) return scores;

    std::unordered_map<int, int> enemy_len;
    std::vector<std::pair<int, int>> enemy_heads;  // (cell, id)
    for (int cell : mem.occupied.order) {
        const OccPart& p = *mem.occupied.find(cell);
        if (p.seen == obs.round && p.team != team) {
            enemy_len[p.id] += 1;
            if (p.head) enemy_heads.emplace_back(cell, p.id);
        }
    }
    // attacks in NESW order (move_order already NESW); scores.push in that order
    for (char d : DIRS) {
        auto it = attacks_map.find(d);
        if (attacks == nullptr || it == attacks_map.end()) continue;
        int pid = it->second;
        int gain = (enemy_len.count(pid) ? enemy_len[pid] : 1) - obs.length;
        if (gain >= params::ATTACK_MIN_GAIN) scores.emplace_back(d, params::W_ATTACK + params::W_TRADE * gain);
        moves.erase(d);
    }
    // rebuild remaining move order (NESW minus popped attacks)
    std::vector<char> remaining;
    for (char d : move_order) if (moves.count(d)) remaining.push_back(d);
    if (remaining.empty()) return scores;

    auto v3 = v3_scores(obs, team, remaining);
    Threats th = head_threats(mem, obs, team, did);
    std::unordered_map<int, int> reach;
    for (auto& [cell, pid] : enemy_heads)
        for (char step : DIRS) {
            auto dest = mem.nav.destination(cell, step);
            if (dest) { int el = enemy_len.count(pid) ? enemy_len[pid] : 1; auto it = reach.find(*dest); if (it == reach.end() || el > it->second) reach[*dest] = el; }
        }
    auto own_free = own_free_times(mem, obs);
    std::unordered_map<int, int> latest_visit;
    for (auto& [c, r] : mem.trail) latest_visit[c] = r;
    int start = mem.cell(obs.x[CENTER], obs.y[CENTER]);
    double protection = protectedFlag ? params::PROTECT_MULT : 1.0;
    double margin = params::SPACE_MARGIN * (obs.round >= 400 ? params::ENDGAME_SPACE_MULT : 1.0);
    double need = std::min(params::SPACE_MULT * obs.length + margin, static_cast<double>(params::SPACE_CAP));
    // CPP_TRAP_OPEN: the room/trap penalty is scaled down in open terrain and
    // kept in full where kelp is dense in view (Queen Of Spades needs it; open
    // ladder maps did better without it). 1.0 = today's behaviour exactly.
    double trap_mult = 1.0;
    if (params::CPP_TRAP_OPEN != 1.0) {
        int kelp = 0, total = 0;
        for (int r = 0; r < W + 1; ++r) for (int c = 0; c < W; ++c) { ++total; kelp += obs.hedge[r][c] == KELP; }
        for (int r = 0; r < W; ++r) for (int c = 0; c < W + 1; ++c) { ++total; kelp += obs.vedge[r][c] == KELP; }
        double tight = std::min(1.0, (kelp / static_cast<double>(total)) / params::CPP_TRAP_KELP_REF);
        trap_mult = params::CPP_TRAP_OPEN + (1.0 - params::CPP_TRAP_OPEN) * tight;
    }
    VorCtx vor_ctx;
    const VorCtx* vor = nullptr;
    if (params::CPP_VOR) {
        for (auto& [cell, _] : enemy_heads) vor_ctx.enemy.push_back(cell);
        vor_ctx.mates = th.mates;
        vor = &vor_ctx;
    }

    for (std::size_t mi = 0; mi < remaining.size(); ++mi) {
        char direction = remaining[mi];
        int dest = moves[direction];
        double deadline = -1;
        if (budget) {
            if (cpu_points() - t0 > params::CPP_HARD_POINTS) break;  // over hard: stop, take best so far
            int moves_left = static_cast<int>(remaining.size() - mi);
            double remaining_pts = params::CPP_SOFT_POINTS - (cpu_points() - t0);
            deadline = cpu_points() + (remaining_pts > 0 ? remaining_pts / moves_left : 0.0);
        }
        Terms tm = search_one(mem, obs, team, did, dest, direction, own_free, deadline, vor);
        double room = std::min(static_cast<double>(tm.room), need);
        double value = tm.food * (protectedFlag ? params::PROTECT_FOOD_MULT : 1.0);
        value += (params::W_UNSEEN * tm.unseen + params::W_STALE * tm.stale) / static_cast<double>(params::N_SEARCH);
        value -= protection * params::W_TRAP * trap_mult * std::max(0.0, need - room);
        if (room < obs.length + 2) value -= protection * params::W_LETHAL * trap_mult;
        if (tm.exits == 0) value -= params::W_DEADEND;
        else if (tm.exits == 1) value -= params::W_CORRIDOR;
        int threat = reach.count(dest) ? reach[dest] : 0;
        if (th.enemy.count(dest) && !(hunter && threat >= obs.length + params::HUNT_MIN_GAIN))
            value -= protection * params::W_HEAD_ENEMY * std::max(1.0, obs.length / 4.0);
        if (hunter && obs.round >= params::HUNT_ROUND) {
            double add = 0;
            for (auto& [cell, pid] : enemy_heads)
                if ((enemy_len.count(pid) ? enemy_len[pid] : 1) >= obs.length + params::HUNT_MIN_GAIN) {
                    double sl = torus_distance(dest, cell, mem.width, mem.height);
                    double d = usePath ? pd.eff(direction, cell, static_cast<int>(sl)) : sl;
                    add = std::max(add, params::W_HUNT / (1 + d));
                }
            value += add;
        }
        if (mem.goal.has_value()) {
            bool poor = mem.local_rate.has_value() && *mem.local_rate < params::POOR_RATE;
            value += params::W_GOAL * tm.progress * (poor ? params::POOR_MULT : 1.0) * (protectedFlag ? params::KING_GOAL_MULT : 1.0);
        }
        if (!mem.hubs.empty()) {
            int crowd = 0;
            for (auto& [hub, _] : mem.hubs) {
                int s = 0; for (int m : th.mates) if (torus_distance(hub, m, mem.width, mem.height) <= 3) ++s;
                crowd = std::max(crowd, s);
            }
            crowd += 1;
            double far = 0;
            for (auto& [hub, v] : mem.hubs) {
                double sl = torus_distance(dest, hub, mem.width, mem.height);
                double d = usePath ? pd.eff(direction, hub, static_cast<int>(sl)) : sl;
                far = std::max(far, v / (1 + d / params::HUB_SCALE));
            }
            far *= params::HUB_FAR_MULT;
            value += params::W_HUB * std::max(tm.hub, far) / crowd;
        }
        if (obs.length >= params::DEFEND_LEN) {
            int near = 0; for (auto& [cell, _] : enemy_heads) if (torus_distance(dest, cell, mem.width, mem.height) <= 2) ++near;
            value -= protection * params::W_DEFEND * near * obs.length / 4.0;
        }
        if (th.friendly.count(dest)) value -= params::W_HEAD_TEAM;
        if (th.ahead.count(dest)) value -= params::W_AHEAD;
        auto lv = latest_visit.find(dest);
        if (lv != latest_visit.end()) value -= params::W_REVISIT * std::max(0.0, 1 - (obs.round - lv->second) / static_cast<double>(params::REVISIT_ROUNDS));
        int near_mates = 0; for (int head : th.mates) if (torus_distance(dest, head, mem.width, mem.height) <= 2) ++near_mates;
        value -= (obs.round < params::FAN_ROUNDS ? params::W_FAN_EARLY : params::W_FAN_LATE) * near_mates;
        bool portal = mem.nav.edges[mem.nav.edge_key(start, direction)] >= 0;
        if (portal) {
            value -= params::W_PORTAL;
            bool unseen = obs.round - mem.nav.seen[dest] > params::PORTAL_STALE;
            if (params::CPP_PORTAL_AGE) {
                // By the dragon's own age, so a child born mid-game still scouts:
                // an unseen exit earns the scout bonus while young, then its
                // penalty ramps in over CPP_PORTAL_RAMP rounds.
                int age = born >= 0 ? obs.round - born : obs.round;
                if (unseen) {
                    double ramp = age < params::SCOUT_ROUNDS ? 0.0
                        : params::CPP_PORTAL_RAMP > 0
                            ? std::min(1.0, (age - params::SCOUT_ROUNDS) / static_cast<double>(params::CPP_PORTAL_RAMP))
                            : 1.0;
                    value -= protection * params::W_PORTAL_UNSEEN * ramp;
                    if (age < params::SCOUT_ROUNDS) value += params::W_PORTAL_SCOUT;
                }
                if (params::CPP_PORTAL_SPREAD > 0)
                    for (int m : th.mates)
                        if (torus_distance(start, m, mem.width, mem.height) <= 2) { value -= params::CPP_PORTAL_SPREAD; break; }
            } else {
                if (unseen) value -= protection * params::W_PORTAL_UNSEEN;
                if (obs.round < params::SCOUT_ROUNDS) value += params::W_PORTAL_SCOUT;
            }
        }
        if (cash.has_value()) {
            double sl = torus_distance(dest, cash->head, mem.width, mem.height);
            double d = usePath ? pd.eff(direction, cash->head, static_cast<int>(sl)) : sl;
            value += params::W_CASH / (1 + d);
            if (cash->front.has_value() && dest == *cash->front) value -= params::W_LETHAL;
        }
        value += params::W_V3 * v3[direction];
        value += params::W_STRAIGHT * (direction == obs.facing ? 1.0 : 0.0);
        scores.emplace_back(direction, value);
    }
    // Lookahead beam (off by default). Skipped if the points budget is already
    // spent, so it never pushes a turn over the hard limit.
    if (params::CPP_BEAM && !(budget && cpu_points() - t0 > params::CPP_SOFT_POINTS))
        beam_adjust(mem, obs, team, did, scores, moves);
    return scores;
}

// ---- core_king.py -----------------------------------------------------------
inline bool king_protected(const Obs& obs, int born_round) {
    return (born_round == 0 && obs.round >= params::FOUNDER_PROTECT_ROUND) ||
           (obs.round >= params::PROTECT_ROUND && obs.length >= params::PROTECT_LEN);
}
inline std::optional<CashTarget> visible_target(WorldMemory& mem, const Obs& obs, char team, int did) {
    if (obs.round < params::FEED_ROUND || obs.length > params::FEED_MAXLEN) return std::nullopt;
    std::unordered_map<int, int> segments;
    std::vector<std::tuple<int, int, char>> heads;  // (k, id, facing)
    for (int k = 0; k < 49; ++k) {
        auto& p = obs.occ[k];
        if (!p || p->team != team || p->id == did) continue;
        segments[p->id] += 1;
        if (p->head) heads.emplace_back(k, p->id, p->facing);
    }
    int needed = std::max(params::FEED_KING_MIN, 2 * obs.length);
    std::optional<std::tuple<int, int, int>> best_key;  // (dist, -seg, head)
    CashTarget best{};
    for (auto& [k, other_id, facing] : heads) {
        if (segments[other_id] < needed) continue;
        int head = mem.cell(obs.x[k], obs.y[k]);
        auto front = mem.nav.destination(head, facing);
        int dist = torus_distance(mem.cell(obs.x[CENTER], obs.y[CENTER]), head, mem.width, mem.height);
        std::tuple<int, int, int> key{dist, -segments[other_id], head};
        if (!best_key || key < *best_key) { best_key = key; best = CashTarget{head, front, k}; }
    }
    if (!best_key) return std::nullopt;
    return best;
}
inline bool should_feed(WorldMemory& mem, const Obs& obs, char team, const std::optional<CashTarget>& target) {
    if (!target) return false;
    int own = mem.cell(obs.x[CENTER], obs.y[CENTER]);
    int distance = torus_distance(own, target->head, mem.width, mem.height);
    if (!(params::FEED_DMIN <= distance && distance <= params::FEED_DMAX) ||
        (target->front.has_value() && own == *target->front)) return false;
    if (params::FEED_ENEMY_CHECK) {
        for (int k : obs.enemy_heads(team)) {
            int enemy = mem.cell(obs.x[k], obs.y[k]);
            if (torus_distance(enemy, target->head, mem.width, mem.height) <= 2) return false;
        }
    }
    return true;
}

// ---- core_split.py ----------------------------------------------------------
inline std::optional<std::string> should_split(int width, int height, int unit_limit, const Obs& obs,
                                               char team, bool protectedFlag) {
    if (obs.length < params::SPLIT_AT || obs.length < params::CHILD + 2) return std::nullopt;
    if (obs.unit_count >= std::min(params::CAP, unit_limit)) return std::nullopt;
    if (danger_cells(obs, team).count(CENTER)) return std::nullopt;
    int cutoff = (width * height < params::AREA_SPLIT) ? params::SPLIT_UNTIL_SMALL : params::SPLIT_UNTIL_LARGE;
    bool late = obs.round > cutoff;
    if (protectedFlag && (late || obs.unit_count >= params::FLOOR)) return std::nullopt;
    if (late && (obs.unit_count >= params::FLOOR || obs.round >= params::FLOOR_UNTIL)) return std::nullopt;
    return std::string("SPLIT ") + std::to_string(params::CHILD);
}

// ---- brain.py ---------------------------------------------------------------
struct Init { int id; char team; int width; int height; int unit_limit; };

inline Init parse_init(const std::string& text) {
    Init in{0, 'A', 0, 0, 64};
    std::stringstream ss(text); std::string line;
    while (std::getline(ss, line)) {
        std::stringstream ls(line); std::vector<std::string> p; std::string w;
        while (ls >> w) p.push_back(w);
        if (p.empty()) continue;
        if (p[0] == "ID") in.id = std::stoi(p[1]);
        else if (p[0] == "TEAM") in.team = p[1][0];
        else if (p[0] == "MAP") { in.width = std::stoi(p[1]); in.height = std::stoi(p[2]); }
        else if (p[0] == "UNIT_LIMIT") in.unit_limit = std::stoi(p[1]);
    }
    return in;
}

class Brain {
  public:
    Init init;
    WorldMemory memory;
    std::optional<int> born_round;

    explicit Brain(const Init& in) : init(in), memory(in.width, in.height) {}

    std::string fallback(const Obs& obs) {
        int f = didx(obs.facing);
        for (int d : {f, LEFTi[f], RIGHTi[f]})
            if (obs.passable(CENTER, DIRS[d])) return std::string("MOVE ") + DIRS[d];
        return std::string("MOVE ") + obs.facing;
    }

    // ---- CPP_SONAR_HUB: share learned hubs ------------------------------------
    // 32-bit message (protocol 2 carries 32-bit sonar): team tag 8 | x 6 | y 6 |
    // value 4 | type 2 (0 = hub) | checksum 6. The team tag keeps the other team,
    // including a mirror copy of this bot, from reading or feeding us hubs.
    Hubs shared_hubs;
    static std::uint32_t hub_tag(char team) { return team == 'A' ? 0xB7u : 0x6Du; }
    static std::uint32_t hub_check(std::uint32_t tag, std::uint32_t x, std::uint32_t y, std::uint32_t v) {
        return (tag + 7 * x + 13 * y + 3 * v) & 63u;
    }
    std::uint32_t encode_hub(int cell, double value) const {
        std::uint32_t tag = hub_tag(init.team), x = cell % memory.width, y = cell / memory.width;
        long q = std::lround(value * 15.0);
        std::uint32_t v = static_cast<std::uint32_t>(std::clamp(q, 1L, 15L));
        return (tag << 24) | (x << 18) | (y << 12) | (v << 8) | hub_check(tag, x, y, v);
    }
    void receive_hubs(const Obs& obs) {
        std::uint32_t tag = hub_tag(init.team);
        int best_cell = -1; std::uint32_t best_v = 0;
        for (std::uint32_t m : obs.msgs) {
            if ((m >> 24) != tag || ((m >> 6) & 3u) != 0) continue;
            std::uint32_t x = (m >> 18) & 63u, y = (m >> 12) & 63u, v = (m >> 8) & 15u;
            if (v == 0 || (m & 63u) != hub_check(tag, x, y, v)) continue;
            if (static_cast<int>(x) >= memory.width || static_cast<int>(y) >= memory.height) continue;
            if (v > best_v) { best_v = v; best_cell = static_cast<int>(y) * memory.width + static_cast<int>(x); }
        }
        if (best_cell >= 0) shared_hubs = {{best_cell, best_v / 15.0}};
        // own knowledge (book or learned) wins; a dragon that knows no hub adopts the shared one
        if (memory.hubs.empty() && !shared_hubs.empty()) memory.set_hubs(shared_hubs);
    }
    std::string sonar_lines(const Obs& obs) const {
        if (memory.hubs.empty() || (obs.round + init.id) % params::CPP_SONAR_EVERY != 0) return "";
        const auto* best = &memory.hubs[0];
        for (const auto& h : memory.hubs) if (h.second > best->second) best = &h;
        std::string msg = std::to_string(encode_hub(best->first, best->second)), out;
        for (char d : DIRS) out += std::string("\nSONAR ") + d + " " + msg;
        return out;
    }

    std::string turn(const Obs& obs) {
        std::string action = decide(obs);
        if (params::CPP_SONAR_HUB && !action.empty()) action += sonar_lines(obs);
        return action;
    }

    std::string decide(const Obs& obs) {
        double t0 = cpu_points();  // CPU points at the turn's start (for CPP_BUDGET)
        memory.update(obs);
        if (params::CPP_SONAR_HUB) receive_hubs(obs);
        if (params::GOAL) memory.update_goal(obs, init.id);
        if (!born_round) born_round = obs.round;
        bool protectedFlag = king_protected(obs, *born_round);
        auto target = visible_target(memory, obs, init.team, init.id);
        if (should_feed(memory, obs, init.team, target)) return "";
        auto split = should_split(init.width, init.height, init.unit_limit, obs, init.team, protectedFlag);
        if (split) return *split;
        auto scores = score_moves(memory, obs, init.team, init.id, protectedFlag, target, t0, *born_round);
        if (scores.empty()) {
            if (obs.length >= 4 && obs.unit_count < init.unit_limit)
                return std::string("SPLIT ") + std::to_string(obs.length - 2);
            return fallback(obs);
        }
        // max by (score, d==facing), keeping the first maximum in insertion order
        char best_dir = scores[0].first;
        double best_score = scores[0].second;
        bool best_face = scores[0].first == obs.facing;
        for (std::size_t i = 1; i < scores.size(); ++i) {
            bool face = scores[i].first == obs.facing;
            if (scores[i].second > best_score || (scores[i].second == best_score && face && !best_face)) {
                best_score = scores[i].second; best_face = face; best_dir = scores[i].first;
            }
        }
        return std::string("MOVE ") + best_dir;
    }
};

}  // namespace v6
