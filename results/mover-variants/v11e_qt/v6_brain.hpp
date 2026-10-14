// V7 port, part 2: action_value (v3 features), tactics, core_search,
// core_king, core_split and the Brain turn order. See v6.hpp for the rules.
#pragma once

#include <cmath>
#include <ctime>
#include <deque>
#include <functional>
#include <string>
#include <tuple>

#include "v6.hpp"
#include "mover.hpp"

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
inline std::unordered_map<char, double> v3_scores(const Obs& obs, char team, const std::vector<char>& dirs,
                                                  std::unordered_map<char, std::array<double, 24>>* rows_out = nullptr) {
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
        if (rows_out) (*rows_out)[d] = row;
        const auto& wt = params::CPP_V3_R4 ? model::WEIGHT_R4 : model::WEIGHT;
        double s = 0; for (int j = 0; j < 24; ++j) s += row[j] * wt[j];
        out[d] = s + (params::CPP_V3_R4 ? model::BIAS_R4 : model::BIAS);
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

// CPP_DEADEND_LOOK: follow the corridor a move enters, never reversing (a
// dragon of length >= 2 cannot turn around). True if it ends in known kelp
// within the look-ahead: a dead end the dragon can only leave by dying.
// Unknown edges, portals with an unknown exit and junctions all count as a way
// out, so exploring is never blocked by this.
inline bool dead_end_ahead(const WorldMemory& mem, int dest, char direction, int look = params::CPP_DEADEND_LOOK) {
    int cell = dest;
    char came = direction;
    for (int step = 0; step < look; ++step) {
        int open = 0, next = -1;
        char next_dir = came;
        for (char d : DIRS) {
            if (didx(d) == OPP[didx(came)]) continue;
            int v = mem.nav.edges[mem.nav.edge_key(cell, d)];
            if (v == NONE) return false;
            if (v == KELP) continue;
            auto nc = mem.nav.destination(cell, d);
            if (!nc) return false;
            ++open; next = *nc; next_dir = d;
        }
        if (open == 0) return true;
        if (open >= 2) return false;
        cell = next;
        came = next_dir;
    }
    return false;
}

// ---- R5 mover (NEW_MOVER_PLAN.md) -------------------------------------------
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

// Returns scores in Python dict insertion order (attacks first, then moves).
inline std::vector<std::pair<char, double>> score_moves(WorldMemory& mem, const Obs& obs, char team, int did,
                                                        bool protectedFlag, const std::optional<CashTarget>& cash,
                                                        double t0 = -1, int born = -1, MoverTrace* trace = nullptr) {
    bool budget = params::CPP_BUDGET != 0 && t0 >= 0;
    PathDist pd;
    bool usePath = params::CPP_PATH_DIST != 0;
    bool tracing = trace != nullptr && trace->want;
    if (usePath || params::CPP_HUB_GRAD > 0 || (params::CPP_KING_GRAD > 0 && cash.has_value()) || tracing) pd.build(mem, obs);
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
        if (gain >= params::ATTACK_MIN_GAIN) { scores.emplace_back(d, params::W_ATTACK + params::W_TRADE * gain); if (trace) ++trace->n_attacks; }
        moves.erase(d);
    }
    // rebuild remaining move order (NESW minus popped attacks)
    std::vector<char> remaining;
    for (char d : move_order) if (moves.count(d)) remaining.push_back(d);
    if (remaining.empty()) return scores;

    std::unordered_map<char, std::array<double, 24>> v3rows;
    auto v3 = v3_scores(obs, team, remaining, tracing ? &v3rows : nullptr);
    // CPP_V3_PORTAL: v3 describes the cells beside our head, but a portal move
    // lands at the far end; give portal moves the mean of the ordinary moves.
    if (params::CPP_V3_PORTAL) {
        double sum = 0; int n = 0;
        for (char d : remaining) if (obs.edge(CENTER, d) < 0) { sum += v3[d]; ++n; }
        for (char d : remaining) if (obs.edge(CENTER, d) >= 0) v3[d] = n ? sum / n : 0.0;
    }
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
    bool is_queen = params::CPP_QUEEN && did <= 1;
    double protection = is_queen ? params::CPP_QUEEN_SAFE_MULT : protectedFlag ? params::PROTECT_MULT : 1.0;
    // our queen's head this round (workers keep clear of it: own head-ons and
    // collisions killed 3 of 12 queens in a diagnostic, 2 Oct)
    int queen_head = -1;
    if (params::CPP_QUEEN && !is_queen && params::CPP_QUEEN_GUARD_PEN > 0)
        for (int cell : mem.occupied.order) {
            const OccPart& p = *mem.occupied.find(cell);
            if (p.head && p.team == team && p.id <= 1 && p.seen == obs.round) queen_head = cell;
        }
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
        if (params::CPP_DEADEND_LOOK > 0 && obs.length >= 2 && dead_end_ahead(mem, dest, direction))
            value -= params::CPP_DEADEND_PEN;
        // Queen safety (queen rules): an enemy head of visible length L can now
        // move ceil(L/4) cells (visible length is a lower bound); dead ends kill
        // short queens (5 of 12 diagnostic queen deaths were walls/kelp).
        if (is_queen) {
            if (params::CPP_QUEEN_REACH_PEN > 0)
                for (auto& [cell, pid] : enemy_heads) {
                    int el = enemy_len.count(pid) ? enemy_len[pid] : 1;
                    if (torus_distance(dest, cell, mem.width, mem.height) <= std::max(1, (el + 3) / 4) + params::CPP_QUEEN_REACH_EXTRA)
                        value -= params::CPP_QUEEN_REACH_PEN;
                }
            if (params::CPP_QUEEN_DEADEND > 0 && obs.length >= 2 && dead_end_ahead(mem, dest, direction, params::CPP_QUEEN_DEADEND))
                value -= params::CPP_QUEEN_DEADEND_PEN;
        } else if (queen_head >= 0 && torus_distance(dest, queen_head, mem.width, mem.height) <= params::CPP_QUEEN_GUARD_R) {
            value -= params::CPP_QUEEN_GUARD_PEN;
        }
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
            // CPP_HUB_GRAD: a constant pull per step closer to the best hub. The
            // term above changes by about 1 point between neighbouring moves when
            // the hub is far, so the local v3 ranker (10-30 point differences)
            // decided the Trophy opening and our founders drifted to the far side
            // while nicked took the centre hub (142 vs 39 pearls by round 100).
            if (params::CPP_HUB_GRAD > 0 && obs.round < params::CPP_HUB_GRAD_UNTIL) {
                int w = mem.width, h = mem.height;
                // target: the most attractive hub (value discounted by distance)
                int target = -1; double target_v = 0, best_score = -1;
                for (auto& [hub, v] : mem.hubs) {
                    double score = v / (1 + torus_distance(start, hub, w, h) / params::HUB_SCALE);
                    if (score > best_score) { best_score = score; target = hub; target_v = v; }
                }
                if (target >= 0 && torus_distance(start, target, w, h) > 2) {   // at the hub, food and local play take over
                    // walking distance where known (pd: +1 closer for the first
                    // step of the shortest path, 1 further otherwise), else straight line
                    auto it = pd.dist.find(target);
                    double now = it != pd.dist.end() ? it->second : torus_distance(start, target, w, h);
                    double after = pd.eff(direction, target, torus_distance(dest, target, w, h));
                    value += params::CPP_HUB_GRAD * target_v * (now - after) / crowd;
                }
            }
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
            // CPP_KING_GRAD: a constant pull per step closer to the king by walking
            // distance (W_CASH/(1+d) is ~3 points at 20 cells, drowned by v3's
            // 10-30 point spread: against nicked v92 we lose on the longest dragon
            // with more total length, e.g. Autarky 12 vs 26 longest, 86 vs 52 total)
            if (params::CPP_KING_GRAD > 0) {
                int head = mem.cell(obs.x[CENTER], obs.y[CENTER]);
                auto it = pd.dist.find(cash->head);
                if (it != pd.dist.end())
                    value += params::CPP_KING_GRAD * (it->second - pd.eff(direction, cash->head, it->second));
                else
                    value += params::CPP_KING_GRAD * (torus_distance(head, cash->head, mem.width, mem.height) - sl);
            }
            if (cash->front.has_value() && dest == *cash->front) value -= params::W_LETHAL;
        }
        value += params::W_V3 * v3[direction];
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
        }
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
inline std::optional<CashTarget> visible_target(WorldMemory& mem, const Obs& obs, char team, int did, int shift = 0) {
    // Queen mode deliberately uses exact visible identity, not size or an
    // aliased king beacon. A missing queen is unknown, never presumed dead.
    if (params::CPP_QUEEN) {
        if (did <= 1 || obs.round < params::FEED_ROUND - shift || obs.length > params::FEED_MAXLEN)
            return std::nullopt;
        for (int k = 0; k < 49; ++k) {
            const auto& p = obs.occ[k];
            if (p && p->head && p->team == team && p->id <= 1) {
                int head = mem.cell(obs.x[k], obs.y[k]);
                return CashTarget{head, mem.nav.destination(head, p->facing), k};
            }
        }
        return std::nullopt;
    }
    if (obs.round < params::FEED_ROUND - shift || obs.length > params::FEED_MAXLEN) return std::nullopt;
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
// CPP_FEED_REACH: steps the king (head at view index k) needs to reach the
// nearest of our body cells, which turn into pearls when we feed, moving
// through free cells and our own body in view; a large value if it cannot.
// Geometric distance alone ignores kelp, bodies and walls between us.
inline int king_reach_to_body(const Obs& obs, int king_k, int did) {
    auto ours = [&](int k) { return obs.occ[k] && obs.occ[k]->id == did; };
    std::vector<int> dist(49, -1);
    std::vector<int> frontier{king_k};
    dist[king_k] = 0;
    while (!frontier.empty()) {
        std::vector<int> nxt;
        for (int k : frontier)
            for (char d : DIRS) {
                if (obs.edge(k, d) != OPEN) continue;
                int n = Obs::step(k, d);
                if (n < 0 || dist[n] >= 0) continue;
                if (ours(n)) return dist[k] + 1;
                if (obs.occ[n]) continue;
                dist[n] = dist[k] + 1;
                nxt.push_back(n);
            }
        frontier.swap(nxt);
    }
    return 1 << 20;
}

inline bool should_feed(WorldMemory& mem, const Obs& obs, char team, const std::optional<CashTarget>& target) {
    if (!target || target->local < 0) return false;   // local < 0: a beaconed king not in view
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
    if (params::CPP_FEED_REACH > 0 && obs.occ[CENTER] &&
        king_reach_to_body(obs, target->local, obs.occ[CENTER]->id) > params::CPP_FEED_REACH)
        return false;
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
    int pfloor = params::CPP_PROTECT_FLOOR >= 0 ? params::CPP_PROTECT_FLOOR : params::FLOOR;
    if (protectedFlag && (late || obs.unit_count >= pfloor)) return std::nullopt;
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
    int last_split = -1000;   // round of this dragon's last split (CPP_RESCUE_EVERY)

    // CPP_FEED_SHIFT_LARGE: big maps start the cash-in schedule earlier (drops there
    // are rarely taken by the enemy; nicked starts 40 rounds earlier on big maps).
    int feed_shift() const { return init.width * init.height >= params::AREA_SPLIT ? params::CPP_FEED_SHIFT_LARGE : 0; }

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
        if (best_cell >= 0) {
            // keep up to 4 distinct shared hubs (strongest first), like learned hubs
            bool found = false;
            for (auto& h : shared_hubs)
                if (h.first == best_cell) { h.second = std::max(h.second, best_v / 15.0); found = true; }
            if (!found) shared_hubs.emplace_back(best_cell, best_v / 15.0);
            std::stable_sort(shared_hubs.begin(), shared_hubs.end(),
                             [](const auto& a, const auto& b) { return a.second > b.second; });
            if (shared_hubs.size() > 4) shared_hubs.resize(4);
        }
        // own knowledge (book or learned) wins; a dragon that knows no hub adopts the shared one
        // CPP_SONAR_ADOPT_AGE: adopt only after this many rounds alive without a hub of
        // its own: founders that never see a spawner (Prisoners Dilemma) adopt, while
        // newborns that would find food themselves keep spreading out (Slithery Fight)
        int age = born_round ? obs.round - *born_round : 0;
        if (memory.hubs.empty() && !shared_hubs.empty() && age >= params::CPP_SONAR_ADOPT_AGE) memory.set_hubs(shared_hubs);
    }
    std::string sonar_lines(const Obs& obs) const {
        if (memory.hubs.empty() || (obs.round + init.id) % params::CPP_SONAR_EVERY != 0) return "";
        // CPP_SONAR_HUB_MIN: only share a learned farm (fast respawns), not an ordinary
        // patch: sharing helps where food is one concentrated farm (Prisoners Dilemma)
        // and crowds dragons where it is spread (Slithery Fight, Portals)
        if (params::CPP_SONAR_HUB_MIN > 0 && memory.hub_best_abs < params::CPP_SONAR_HUB_MIN) return "";
        // rotate through every known hub, so receivers learn all of them rather
        // than all converging on one
        const auto& hub = memory.hubs[(obs.round / params::CPP_SONAR_EVERY) % memory.hubs.size()];
        std::string msg = std::to_string(encode_hub(hub.first, hub.second)), out;
        for (char d : DIRS) out += std::string("\nSONAR ") + d + " " + msg;
        return out;
    }

    // ---- CPP_KING_BEACON: the longest known king, broadcast and relayed ------
    // Same 32-bit frame as the hub message with bit 6 set: team tag 8 | x 6 |
    // y 6 | length/4 (5 bits, up to 124) | 1 | checksum 6. Every dragon sends the
    // best king it knows (itself if it is at least as long), so the position
    // spreads past the first dragon each ray reaches.
    int king_cell = -1, king_q = 0, king_round = -1000;
    static std::uint32_t king_check(std::uint32_t tag, std::uint32_t x, std::uint32_t y, std::uint32_t q) {
        return (tag + 7 * x + 13 * y + 5 * q + 1) & 63u;
    }
    std::uint32_t encode_king(int cell, int q) const {
        std::uint32_t tag = hub_tag(init.team), x = cell % memory.width, y = cell / memory.width;
        std::uint32_t uq = static_cast<std::uint32_t>(std::clamp(q, 0, 31));
        return (tag << 24) | (x << 18) | (y << 12) | (uq << 7) | (1u << 6) | king_check(tag, x, y, uq);
    }
    static int length_q(int length) { return std::min(31, length / 4); }

    // ---- CPP_KB_V2: king beacon with identity and origin age ----------------
    // tag 5 | x 6 | y 6 | length/4 (4 bits, up to 60) | origin round mod 8 (3) |
    // king token = id mod 16 (4) | checksum 4. Relays keep the origin round, so
    // the TTL measures time since the king itself spoke (a dead king expires);
    // feeders bind to the head whose id matches the token.
    int king_tok = -1;
    static std::uint32_t kb2_tag(char team) { return (hub_tag(team) ^ 0x15u) & 31u; }
    static std::uint32_t kb2_check(std::uint32_t body) {
        std::uint32_t h = body * 2654435761u;
        return (h >> 28) & 15u;
    }
    std::uint32_t encode_king2(int cell, int q, int origin, int tok) const {
        std::uint32_t x = cell % memory.width, y = cell / memory.width;
        std::uint32_t body = (kb2_tag(init.team) << 23) | (x << 17) | (y << 11) |
                             (static_cast<std::uint32_t>(std::clamp(q, 0, 15)) << 7) |
                             ((static_cast<std::uint32_t>(origin) & 7u) << 4) | (static_cast<std::uint32_t>(tok) & 15u);
        return (body << 4) | kb2_check(body);
    }
    static int kb2_ttl() { return std::min(params::CPP_KB_TTL, 7); }
    // better(candidate) than the stored king: the same king with fresher news, or
    // a longer king, or an equally long one with a lower token (deterministic)
    bool kb2_better(int q, int origin, int tok, int now) const {
        if (king_cell < 0 || now - king_round > kb2_ttl()) return true;
        if (tok == king_tok) return origin > king_round;
        return q > king_q || (q == king_q && tok < king_tok);
    }
    void receive_king2(const Obs& obs) {
        std::uint32_t tag = kb2_tag(init.team);
        for (std::uint32_t m : obs.msgs) {
            std::uint32_t body = m >> 4;
            if ((body >> 23) != tag || (m & 15u) != kb2_check(body)) continue;
            int x = (body >> 17) & 63, y = (body >> 11) & 63, q = (body >> 7) & 15;
            int r8 = (body >> 4) & 7, tok = body & 15;
            if (x >= memory.width || y >= memory.height) continue;
            int age = (obs.round - r8) & 7;
            if (age > kb2_ttl()) continue;
            int origin = obs.round - age;
            if (kb2_better(q, origin, tok, obs.round)) {
                king_cell = y * memory.width + x; king_q = q; king_round = origin; king_tok = tok;
            }
        }
        if (obs.round - king_round > kb2_ttl()) { king_cell = -1; king_q = 0; king_tok = -1; }
        // contradicted: where the king must be is in view, but its head is not
        if (king_cell >= 0 && king_tok != (init.id & 15)) {
            int head = memory.cell(obs.x[CENTER], obs.y[CENTER]);
            int w = memory.width, h = memory.height;
            int ax = std::abs(head % w - king_cell % w), ay = std::abs(head / w - king_cell / w);
            int cheb = std::max(std::min(ax, w - ax), std::min(ay, h - ay));
            if (cheb + (obs.round - king_round) <= 3 && king_head_in_view(obs) < 0) {
                king_cell = -1; king_q = 0; king_tok = -1;
            }
        }
    }
    // index k of the visible teammate head carrying the king's token, or -1
    int king_head_in_view(const Obs& obs) const {
        int best = -1, best_d = 1 << 30;
        for (int k = 0; k < 49; ++k) {
            const auto& p = obs.occ[k];
            if (!p || !p->head || p->team != init.team || p->id == init.id || (p->id & 15) != king_tok) continue;
            int d = torus_distance(memory.cell(obs.x[k], obs.y[k]), king_cell, memory.width, memory.height);
            if (d < best_d) { best_d = d; best = k; }
        }
        return best;
    }
    std::string king_lines2(const Obs& obs) {
        int own_q = std::min(15, obs.length / 4), own_tok = init.id & 15;
        std::uint32_t msg;
        if (obs.length >= params::CPP_KB_MINLEN && (king_tok == own_tok || kb2_better(own_q, obs.round, own_tok, obs.round))) {
            int cell = memory.cell(obs.x[CENTER], obs.y[CENTER]);
            king_cell = cell; king_q = own_q; king_round = obs.round; king_tok = own_tok;
            msg = encode_king2(cell, own_q, obs.round, own_tok);
        } else if (king_cell >= 0) {
            msg = encode_king2(king_cell, king_q, king_round, king_tok);   // relay, origin kept
        } else {
            return "";
        }
        std::string out, s = std::to_string(msg);
        for (char d : DIRS) out += std::string("\nSONAR ") + d + " " + s;
        return out;
    }

    void receive_king(const Obs& obs) {
        if (params::CPP_KB_V2) { receive_king2(obs); return; }
        std::uint32_t tag = hub_tag(init.team);
        for (std::uint32_t m : obs.msgs) {
            if ((m >> 24) != tag || ((m >> 6) & 1u) != 1u) continue;
            std::uint32_t x = (m >> 18) & 63u, y = (m >> 12) & 63u, q = (m >> 7) & 31u;
            if ((m & 63u) != king_check(tag, x, y, q)) continue;
            if (static_cast<int>(x) >= memory.width || static_cast<int>(y) >= memory.height) continue;
            bool stale = obs.round - king_round > params::CPP_KB_TTL;
            if (stale || static_cast<int>(q) >= king_q) {
                king_cell = static_cast<int>(y) * memory.width + static_cast<int>(x);
                king_q = static_cast<int>(q);
                king_round = obs.round;
            }
        }
        if (obs.round - king_round > params::CPP_KB_TTL) { king_cell = -1; king_q = 0; }
    }
    std::string king_lines(const Obs& obs) {
        if (params::CPP_KB_V2) return king_lines2(obs);
        std::uint32_t msg;
        int own_q = length_q(obs.length);
        if (obs.length >= params::CPP_KB_MINLEN && (king_cell < 0 || own_q >= king_q))
            msg = encode_king(memory.cell(obs.x[CENTER], obs.y[CENTER]), own_q);
        else if (king_cell >= 0)
            msg = encode_king(king_cell, king_q);   // relay
        else
            return "";
        std::string out, s = std::to_string(msg);
        for (char d : DIRS) out += std::string("\nSONAR ") + d + " " + s;
        return out;
    }
    // A feeding target from the beacon: small dragons after FEED_ROUND and, with
    // CPP_BIG_FEED, dragons of any length once the king is MARGIN longer. When a
    // teammate head is in view near the beaconed cell it is used as the king (so
    // should_feed can fire); otherwise the target only pulls (local = -1).
    std::optional<CashTarget> beacon_target(const Obs& obs) {
        int shift = feed_shift();
        if (king_cell < 0 || obs.round < params::CPP_KB_ROUND - shift) return std::nullopt;
        if (params::CPP_KB_V2 ? king_tok == (init.id & 15) : length_q(obs.length) >= king_q)
            return std::nullopt;   // this dragon is (a) king
        bool small = obs.round >= params::FEED_ROUND - shift && obs.length <= params::FEED_MAXLEN;
        bool big = params::CPP_BIG_FEED && obs.round >= params::CPP_BIG_FEED_ROUND - shift &&
                   4 * king_q >= obs.length + params::CPP_BIG_FEED_MARGIN;
        if (!small && !big) return std::nullopt;
        if (params::CPP_KB_V2) {
            // bind to the head carrying the king's token, not any teammate near the cell
            int k = king_head_in_view(obs);
            if (k >= 0) {
                int head = memory.cell(obs.x[k], obs.y[k]);
                if (torus_distance(head, king_cell, memory.width, memory.height) <= 4 + (obs.round - king_round))
                    return CashTarget{head, memory.nav.destination(head, obs.occ[k]->facing), k};
            }
            return CashTarget{king_cell, std::nullopt, -1};
        }
        std::optional<CashTarget> best;
        int best_d = 1 << 30;
        for (int k = 0; k < 49; ++k) {
            const auto& p = obs.occ[k];
            if (!p || !p->head || p->team != init.team || p->id == init.id) continue;
            int head = memory.cell(obs.x[k], obs.y[k]);
            int d = torus_distance(head, king_cell, memory.width, memory.height);
            if (d <= 4 && d < best_d) { best_d = d; best = CashTarget{head, memory.nav.destination(head, p->facing), k}; }
        }
        if (best) return best;
        return CashTarget{king_cell, std::nullopt, -1};
    }

    // CPP_SPLIT_SAFE: the child is born at the parent's tail facing away from
    // the parent; if that corridor is a known dead end the child (length >= 2,
    // cannot reverse) is born dead. 90% of our kelp deaths were length-2
    // dragons, most within 3-5 rounds of birth.
    bool child_can_escape(const Obs& obs) const {
        auto body = memory.trail_body(obs.length);
        if (!body || body->size() < 2) return true;   // body unknown: allow the split
        int tail = body->back(), before = (*body)[body->size() - 2];
        int w = memory.width, h = memory.height;
        int dx = ((tail % w) - (before % w) + w) % w, dy = ((tail / w) - (before / w) + h) % h;
        char face;
        if (dx == 1 && dy == 0) face = 'E';
        else if (dx == w - 1 && dy == 0) face = 'W';
        else if (dy == 1 && dx == 0) face = 'S';
        else if (dy == h - 1 && dx == 0) face = 'N';
        else return true;                              // a portal between the last two segments
        if (dead_end_ahead(memory, tail, face, params::CPP_SPLIT_SAFE_LOOK)) return false;
        if (params::CPP_SPLIT_ROOM > 0) {
            // room around the birth cell: known open tiles reachable from the tail,
            // not counting tiles any dragon occupies this round (the parent's own
            // body included: it is still there when the child first moves). On
            // Slithery Fight children were born onto a crowded two-wide spawner patch
            // and died in the kelp with no legal move.
            std::unordered_set<int> own(body->begin(), body->end());
            std::vector<int> queue{tail};
            std::unordered_set<int> seen{tail};
            int room = 0;
            for (std::size_t i = 0; i < queue.size() && room < params::CPP_SPLIT_ROOM; ++i) {
                int c = queue[i];
                for (char d : DIRS) {
                    auto nc = memory.nav.destination(c, d);
                    if (!nc || seen.count(*nc)) continue;
                    seen.insert(*nc);
                    const OccPart* part = memory.occupied.find(*nc);
                    if (own.count(*nc) || (part != nullptr && part->seen == obs.round)) continue;
                    ++room;
                    queue.push_back(*nc);
                }
            }
            if (room < params::CPP_SPLIT_ROOM) return false;
        }
        return true;
    }

    // ---- CPP_BRIEF: brief the newborn child ------------------------------------
    // A child starts with no memory. At a split the parent sends one message
    // backward into its own body; it exits at the tail, where the child now
    // is, and the child reads it on its first turn (later the same round).
    // Frame: team tag 8 | unused 12 | dead-end mask 4 (N E S W) | 1 0 | checksum 6.
    // A mask bit means: moving that way from the child's birth cell enters a
    // corridor the parent knows is a dead end.
    static std::uint32_t brief_check(std::uint32_t tag, std::uint32_t mask) {
        return (tag + 11 * mask + 2) & 63u;
    }
    std::string brief_line(const Obs& obs) const {
        auto body = memory.trail_body(obs.length);
        if (!body || body->size() < 2) return "";
        int tail = body->back(), before = (*body)[body->size() - 2];
        int w = memory.width, h = memory.height;
        int dx = ((tail % w) - (before % w) + w) % w, dy = ((tail / w) - (before / w) + h) % h;
        char face;
        if (dx == 1 && dy == 0) face = 'E';
        else if (dx == w - 1 && dy == 0) face = 'W';
        else if (dy == 1 && dx == 0) face = 'S';
        else if (dy == h - 1 && dx == 0) face = 'N';
        else return "";
        std::uint32_t mask = 0;
        for (int i = 0; i < 4; ++i) {
            char d = DIRS[i];
            if (i == OPP[didx(face)]) continue;               // the child cannot reverse
            auto dest = memory.nav.destination(tail, d);
            if (dest && dead_end_ahead(memory, *dest, d, params::CPP_SPLIT_SAFE_LOOK)) mask |= 1u << i;
        }
        if (mask == 0) return "";
        std::uint32_t tag = hub_tag(init.team);
        std::uint32_t msg = (tag << 24) | (mask << 8) | (2u << 6) | brief_check(tag, mask);
        // into our own body: the ray leaves at the tail, towards the child
        return std::string("\nSONAR ") + DIRS[OPP[didx(obs.facing)]] + " " + std::to_string(msg);
    }
    std::uint32_t read_brief(const Obs& obs) const {
        std::uint32_t tag = hub_tag(init.team);
        for (std::uint32_t m : obs.msgs) {
            if ((m >> 24) != tag || ((m >> 6) & 3u) != 2u) continue;
            std::uint32_t mask = (m >> 8) & 15u;
            if ((m & 63u) == brief_check(tag, mask)) return mask;
        }
        return 0;
    }

    std::string turn(const Obs& obs) {
        mover_log.clear();
        std::string action = decide(obs);
        if (action.empty()) return action;
        action += mover_log;
        if ((!params::CPP_QUEEN || params::CPP_QUEEN_KB) && params::CPP_KING_BEACON && obs.round >= params::CPP_KB_ROUND - feed_shift()) action += king_lines(obs);
        else if (params::CPP_SONAR_HUB) action += sonar_lines(obs);
        // last, so it wins the backward direction over a beacon
        if (params::CPP_BRIEF && action.rfind("SPLIT ", 0) == 0) action += brief_line(obs);
        return action;
    }

    std::string decide(const Obs& obs) {
        double t0 = cpu_points();  // CPU points at the turn's start (for CPP_BUDGET)
        memory.update(obs);
        if (params::CPP_SONAR_HUB) receive_hubs(obs);
        if ((!params::CPP_QUEEN || params::CPP_QUEEN_KB) && params::CPP_KING_BEACON) receive_king(obs);
        if (params::GOAL) memory.update_goal(obs, init.id);
        if (!born_round) born_round = obs.round;
        bool protectedFlag = king_protected(obs, *born_round);
        bool queen = params::CPP_QUEEN && init.id <= 1;
        if (queen) protectedFlag = true;
        auto target = visible_target(memory, obs, init.team, init.id, feed_shift());
        if ((!params::CPP_QUEEN || params::CPP_QUEEN_KB) && params::CPP_KING_BEACON && !target) target = beacon_target(obs);
        if (should_feed(memory, obs, init.team, target)) return "";
        auto split = should_split(init.width, init.height, init.unit_limit, obs, init.team, protectedFlag);
        if (queen && (obs.round >= params::CPP_QUEEN_SPLIT_UNTIL ||
                      obs.unit_count >= params::CPP_QUEEN_FLOOR ||
                      obs.length - params::CHILD < params::CPP_QUEEN_KEEP)) split.reset();
        // CPP_ANCHOR: founders (alive at round 0) stop splitting from
        // FOUNDER_PROTECT_ROUND so they grow into kings early, as nicked's anchors
        // do from round 80 (our longest dragon was 4 at round 300 vs their 11).
        // They split again only if the team falls below CPP_ANCHOR_RESCUE dragons.
        if (split && params::CPP_ANCHOR && *born_round == 0 && obs.round >= params::FOUNDER_PROTECT_ROUND &&
            obs.unit_count >= params::CPP_ANCHOR_RESCUE)
            split.reset();
        if (split && params::CPP_SPLIT_SAFE && !child_can_escape(obs)) split.reset();
        // CPP_RESCUE_EVERY: a protected (long) dragon below the floor rebuilds the
        // population slowly instead of splitting itself back down every turn.
        if (split && params::CPP_RESCUE_EVERY > 0 && protectedFlag && obs.round - last_split < params::CPP_RESCUE_EVERY)
            split.reset();
        if (split) { last_split = obs.round; return *split; }
        MoverTrace trace;
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
        auto scores = score_moves(memory, obs, init.team, init.id, protectedFlag, target, t0, *born_round, &trace);
        if (scores.empty()) {
            if (obs.length >= 4 && obs.unit_count < init.unit_limit)
                return std::string("SPLIT ") + std::to_string(queen ? 2 : obs.length - 2);
            return fallback(obs);
        }
        // max by (score, d==facing), keeping the first maximum in insertion order
        if (params::CPP_BRIEF && obs.round == *born_round) {
            std::uint32_t mask = read_brief(obs);
            if (mask)
                for (auto& [d, v] : scores)
                    if (mask & (1u << didx(d))) v -= params::CPP_BRIEF_PEN;
        }
        char best_dir = scores[0].first;
        double best_score = scores[0].second;
        bool best_face = scores[0].first == obs.facing;
        for (std::size_t i = 1; i < scores.size(); ++i) {
            bool face = scores[i].first == obs.facing;
            if (scores[i].second > best_score || (scores[i].second == best_score && face && !best_face)) {
                best_score = scores[i].second; best_face = face; best_dir = scores[i].first;
            }
        }
        if (trace.want && trace.n_attacks == 0 && trace.dirs.size() >= 2 && trace.dirs.size() == scores.size()) {
            for (auto& fv : trace.f) for (int j = 0; j < 12; ++j) fv[24 + j] = trace.ctx[j];
            if (params::CPP_MOVER) best_dir = mover_choice(trace, best_dir);
            if (params::CPP_MOVER_LOG > 0 && (init.id * 31 + obs.round) % params::CPP_MOVER_LOG == 0)
                mover_log = mover_line(obs, trace, best_dir);
        }
        // CPP_QUEEN_TACTICS: the queen keeps the incumbent's move unless it survives
        // fewer look-ahead steps (or fewer full lines when no move is fully safe)
        // than another legal move; among the best, the incumbent's score decides.
        if (params::CPP_QUEEN_TACTICS && init.id <= 1 && scores.size() >= 2) {
            std::vector<std::tuple<int, int, double, char>> opts;   // (survived, full lines, score, dir)
            for (auto& [d, v] : scores) {
                auto [s, f] = queen_escape(obs, d, params::CPP_QUEEN_TACTICS_DEPTH);
                opts.emplace_back(s, std::min(f, 1), v, d);
            }
            auto inc = std::find_if(opts.begin(), opts.end(), [&](auto& o) { return std::get<3>(o) == best_dir; });
            auto top = std::max_element(opts.begin(), opts.end(), [](auto& a, auto& b) {
                return std::tie(std::get<0>(a), std::get<1>(a), std::get<2>(a)) < std::tie(std::get<0>(b), std::get<1>(b), std::get<2>(b)); });
            if (inc != opts.end() && std::tie(std::get<0>(*inc), std::get<1>(*inc)) < std::tie(std::get<0>(*top), std::get<1>(*top)))
                best_dir = std::get<3>(*top);
        }
        std::string path(1, best_dir);
        if (params::CPP_MULTISTEP && (!(params::CPP_QUEEN && init.id <= 1) || params::CPP_MULTISTEP_QUEEN))
            path += extra_steps(obs, best_dir);
        return std::string("MOVE ") + path;
    }

    // CPP_QUEEN_TACTICS (Q4): short exact escape search for our queen (id 0/1).
    // For one first move, search every move sequence up to `depth` steps in the
    // view, simulating the queen's own body (the head advances, the whole current
    // body including the tail blocks: the engine checks collision before the tail
    // moves). Other dragons' bodies are static obstacles. A cell is deadly at our
    // step t if a threat head (enemy, and with CPP_QUEEN_TACTICS_FRIENDS our own
    // workers) can reach it in t of its turns at ceil(visible length / 4) steps
    // per turn (visible length is a lower bound). Returns (steps survived on the
    // best line, number of lines surviving the full depth).
    std::pair<int, int> queen_escape(const Obs& obs, char first, int depth) const {
        int w = memory.width, h = memory.height;
        int head = memory.cell(obs.x[CENTER], obs.y[CENTER]);
        std::unordered_set<int> in_view, others;
        std::unordered_map<int, int> seg_count;
        std::vector<std::pair<int, int>> threats;   // (cell, steps per turn)
        for (int k = 0; k < 49; ++k) {
            int c = memory.cell(obs.x[k], obs.y[k]);
            in_view.insert(c);
            const auto& p = obs.occ[k];
            if (!p) continue;
            seg_count[p->id] += 1;
            if (p->id != init.id) others.insert(c);
        }
        for (int k = 0; k < 49; ++k) {
            const auto& p = obs.occ[k];
            if (!p || !p->head || p->id == init.id) continue;
            if (p->team == init.team && !params::CPP_QUEEN_TACTICS_FRIENDS) continue;
            int speed = std::max(1, (seg_count[p->id] + 3) / 4) + params::CPP_QUEEN_TACTICS_MARGIN;
            threats.emplace_back(memory.cell(obs.x[k], obs.y[k]), speed);
        }
        // own body, head first; a trail with gaps (multi-step turns) is not a body
        std::vector<int> body;
        if (auto tb = memory.trail_body(obs.length)) {
            bool ok = (*tb)[0] == head;
            for (std::size_t i = 1; ok && i < tb->size(); ++i)
                ok = torus_distance((*tb)[i - 1], (*tb)[i], w, h) == 1;
            if (ok) body = *tb;
        }
        if (body.empty()) {   // fall back: visible own cells as static obstacles
            body.push_back(head);
            for (int k = 0; k < 49; ++k)
                if (obs.occ[k] && obs.occ[k]->id == init.id && k != CENTER) others.insert(memory.cell(obs.x[k], obs.y[k]));
        }
        auto deadly = [&](int c, int t) {
            for (auto& [tc, sp] : threats) if (torus_distance(c, tc, w, h) <= t * sp) return true;
            return false;
        };
        int best = 0, full = 0;
        // iterative DFS over (body, step, direction)
        std::function<void(const std::vector<int>&, int, char)> go = [&](const std::vector<int>& b, int t, char d) {
            auto n = memory.nav.destination(b[0], d);
            if (!n) return;
            if (b.size() > 1 && *n == b[1]) return;                       // reversal into the neck
            if (others.count(*n)) return;
            for (int c : b) if (c == *n) return;                          // own body, tail included
            if (deadly(*n, t)) return;
            best = std::max(best, t);
            if (t == depth || !in_view.count(*n)) { if (t == depth) ++full; else best = std::max(best, depth); return; }
            std::vector<int> nb; nb.reserve(b.size());
            nb.push_back(*n);
            for (std::size_t i = 0; i + 1 < b.size(); ++i) nb.push_back(b[i]);
            for (char nd : DIRS) go(nb, t + 1, nd);
        };
        go(body, 1, first);
        return {best, full};
    }

    // CPP_MULTISTEP (queen rules, unswbc 1.2.3): a dragon may move ceil(length / 4)
    // times per turn for free (start-of-move length). After the incumbent's first
    // step, spend the remaining free steps only on reaching a visible pearl by the
    // shortest path through free cells of the view. Conservative: every occupied
    // cell (own body included, even the tail) and every cell already entered this
    // turn is blocked, portals are not taken, no paid (sprint) steps; the endpoint
    // must keep two open exits and stay out of reach (distance <= 2) of enemy heads.
    std::string extra_steps(const Obs& obs, char first) const {
        int free_steps = (obs.length + 3) / 4;
        if (free_steps < 2) return "";
        if (obs.edge(CENTER, first) != OPEN) return "";
        int start = Obs::step(CENTER, first);
        if (start < 0 || obs.occ[start]) return "";            // attack or off-view: single step
        std::vector<int> enemy;
        for (int k = 0; k < 49; ++k)
            if (obs.occ[k] && obs.occ[k]->head && obs.occ[k]->team != init.team) enemy.push_back(k);
        auto near_enemy = [&](int k) {
            for (int e : enemy) if (std::abs(e / 7 - k / 7) + std::abs(e % 7 - k % 7) <= 2) return true;
            return false;
        };
        int budget = free_steps - 1;
        // BFS from the first step's cell, depth <= budget, avoiding occupied/entered cells
        std::array<int, 49> prev; prev.fill(-2);
        std::array<char, 49> how{};
        std::array<int, 49> depth{};
        prev[start] = -1;
        std::vector<int> frontier{start};
        int goal = -1;
        for (int dpt = 1; dpt <= budget && goal < 0 && !frontier.empty(); ++dpt) {
            std::vector<int> nxt;
            for (int k : frontier) {
                for (char d : DIRS) {
                    if (obs.edge(k, d) != OPEN) continue;           // kelp, unknown or portal
                    int n = Obs::step(k, d);
                    if (n < 0 || n == CENTER || prev[n] != -2 || obs.occ[n]) continue;
                    prev[n] = k; how[n] = d; depth[n] = dpt;
                    if (obs.pearl[n] && goal < 0) goal = n;
                    nxt.push_back(n);
                }
            }
            frontier.swap(nxt);
        }
        if (goal < 0 || near_enemy(goal)) return "";
        int exits = 0;
        for (char d : DIRS) {
            if (obs.edge(goal, d) != OPEN) continue;
            int n = Obs::step(goal, d);
            if (n >= 0 && !obs.occ[n] && n != CENTER) {
                bool on_path = false;
                for (int c = goal; c >= 0; c = prev[c]) if (c == n) { on_path = true; break; }
                if (!on_path && n != start) ++exits;
            }
        }
        if (exits < 2) return "";
        std::string steps;
        for (int c = goal; c != start; c = prev[c]) steps.insert(steps.begin(), how[c]);
        return steps;
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
        std::snprintf(b, sizeof b, "\nLOG MV %d %d %c %zu", obs.round, init.id, chosen, t.dirs.size());
        std::string out = b;
        for (std::size_t i = 0; i < t.dirs.size(); ++i) {
            out += std::string("\nLOG MVC ") + t.dirs[i];
            for (int j = 0; j < MV_N; ++j) { std::snprintf(b, sizeof b, " %.6g", t.f[i][j]); out += b; }
        }
        return out;
    }
};

}  // namespace v6
