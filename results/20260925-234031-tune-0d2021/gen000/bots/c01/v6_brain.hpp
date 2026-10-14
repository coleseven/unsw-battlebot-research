// V7 port, part 2: action_value (v3 features), tactics, core_search,
// core_king, core_split and the Brain turn order. See v6.hpp for the rules.
#pragma once

#include <cmath>
#include <string>
#include <tuple>

#include "v6.hpp"

namespace v6 {

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
inline double food_value(const WorldMemory& mem, const Obs& obs, int cell, int hops) {
    double value = 0;
    auto vit = mem.nav.visible.find(cell);
    if (vit != mem.nav.visible.end() && obs.pearl[vit->second]) value = params::W_PEARL / (1 + hops);
    else if (mem.pearl.count(cell)) value = params::W_MEM_PEARL / (1 + hops);
    auto sit = mem.spawn_ready.find(cell);
    if (sit != mem.spawn_ready.end()) {
        int wait = sit->second - obs.round - hops;
        if (0 <= wait && wait <= params::H_SPAWN) value = std::max(value, params::W_SPAWN / (1 + hops + 0.2 * wait));
    }
    return value;
}
struct Terms { double food = 0, hub = 0, progress = 0; int unseen = 0, stale = 0, room = 0, exits = 0, expanded = 0; };

inline Terms search_one(const WorldMemory& mem, const Obs& obs, char team, int did, int dest, char direction,
                        const std::unordered_map<int, int>& own_free) {
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
        auto [cost, arrival, cell] = queue.top(); queue.pop();
        auto bit = best.find(cell);
        if (bit == best.end() || cost != bit->second) continue;
        tm.expanded += 1;
        tm.food = std::max(tm.food, food_value(mem, obs, cell, arrival - 1));
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

// cash target: (head cell, front cell or none, local k)
struct CashTarget { int head; std::optional<int> front; int local; };

// Returns scores in Python dict insertion order (attacks first, then moves).
inline std::vector<std::pair<char, double>> score_moves(WorldMemory& mem, const Obs& obs, char team, int did,
                                                        bool protectedFlag, const std::optional<CashTarget>& cash) {
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

    for (char direction : remaining) {
        int dest = moves[direction];
        Terms tm = search_one(mem, obs, team, did, dest, direction, own_free);
        double room = std::min(static_cast<double>(tm.room), need);
        double value = tm.food * (protectedFlag ? params::PROTECT_FOOD_MULT : 1.0);
        value += (params::W_UNSEEN * tm.unseen + params::W_STALE * tm.stale) / static_cast<double>(params::N_SEARCH);
        value -= protection * params::W_TRAP * std::max(0.0, need - room);
        if (room < obs.length + 2) value -= protection * params::W_LETHAL;
        if (tm.exits == 0) value -= params::W_DEADEND;
        else if (tm.exits == 1) value -= params::W_CORRIDOR;
        int threat = reach.count(dest) ? reach[dest] : 0;
        if (th.enemy.count(dest) && !(hunter && threat >= obs.length + params::HUNT_MIN_GAIN))
            value -= protection * params::W_HEAD_ENEMY * std::max(1.0, obs.length / 4.0);
        if (hunter && obs.round >= params::HUNT_ROUND) {
            double add = 0;
            for (auto& [cell, pid] : enemy_heads)
                if ((enemy_len.count(pid) ? enemy_len[pid] : 1) >= obs.length + params::HUNT_MIN_GAIN)
                    add = std::max(add, params::W_HUNT / (1 + torus_distance(dest, cell, mem.width, mem.height)));
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
            for (auto& [hub, v] : mem.hubs) far = std::max(far, v / (1 + torus_distance(dest, hub, mem.width, mem.height) / params::HUB_SCALE));
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
            if (obs.round - mem.nav.seen[dest] > params::PORTAL_STALE) value -= protection * params::W_PORTAL_UNSEEN;
            if (obs.round < params::SCOUT_ROUNDS) value += params::W_PORTAL_SCOUT;
        }
        if (cash.has_value()) {
            value += params::W_CASH / (1 + torus_distance(dest, cash->head, mem.width, mem.height));
            if (cash->front.has_value() && dest == *cash->front) value -= params::W_LETHAL;
        }
        value += params::W_V3 * v3[direction];
        value += params::W_STRAIGHT * (direction == obs.facing ? 1.0 : 0.0);
        scores.emplace_back(direction, value);
    }
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

    std::string turn(const Obs& obs) {
        memory.update(obs);
        if (params::GOAL) memory.update_goal(obs, init.id);
        if (!born_round) born_round = obs.round;
        bool protectedFlag = king_protected(obs, *born_round);
        auto target = visible_target(memory, obs, init.team, init.id);
        if (should_feed(memory, obs, init.team, target)) return "";
        auto split = should_split(init.width, init.height, init.unit_limit, obs, init.team, protectedFlag);
        if (split) return *split;
        auto scores = score_moves(memory, obs, init.team, init.id, protectedFlag, target);
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
