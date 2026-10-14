// V7: a 1:1 C++ port of the Python v6 search core (PARITY / matching mode).
//
// Each Python module is a section below, kept in the same shape so a parity
// mismatch points at one place. Determinism rules (see V7_CPP_PORT_PLAN.md §3):
//   * iterate directions in NESW order everywhere; ties keep the FIRST maximum
//     (strict > in NESW order), matching Python's max();
//   * the search heap orders (cost, arrival, cell) lexicographically;
//   * `occupied` keeps Python dict insertion order (an OrderedMap);
//   * doubles, in Python's operation order.
//
// The C++ search is always the PARITY search: no wall-clock budget, each move
// expands up to N_SEARCH. Sonar is omitted: v6 discards decoded sonar and only
// emits beacons as extra lines, so it never changes the action line.
#pragma once

#include <algorithm>
#include <array>
#include <cstdint>
#include <optional>
#include <queue>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "params.hpp"
#include "model.hpp"
#include "portal_book.hpp"
#include "hub_book.hpp"

namespace v6 {

// ---- constants (bc.py) ------------------------------------------------------
constexpr int W = 7, R = 3, CENTER = R * W + R;  // 24
constexpr int OPEN = -1, KELP = -2, NONE = -3;   // nav edge sentinels
constexpr char DIRS[4] = {'N', 'E', 'S', 'W'};
constexpr int DXi[4] = {0, 1, 0, -1};
constexpr int DYi[4] = {-1, 0, 1, 0};
constexpr int OPP[4] = {2, 3, 0, 1};
constexpr int LEFTi[4] = {3, 0, 1, 2};
constexpr int RIGHTi[4] = {1, 2, 3, 0};

inline int didx(char d) {
    switch (d) { case 'N': return 0; case 'E': return 1; case 'S': return 2; default: return 3; }
}

// ---- ordered map: Python dict insertion order -------------------------------
template <class V>
class OrderedMap {
  public:
    std::vector<int> order;
    std::unordered_map<int, V> vals;

    bool contains(int k) const { return vals.find(k) != vals.end(); }
    V* find(int k) { auto it = vals.find(k); return it == vals.end() ? nullptr : &it->second; }
    const V* find(int k) const { auto it = vals.find(k); return it == vals.end() ? nullptr : &it->second; }
    void set(int k, const V& v) {
        auto it = vals.find(k);
        if (it == vals.end()) { order.push_back(k); vals.emplace(k, v); }
        else it->second = v;
    }
    void erase(int k) {
        if (vals.erase(k)) order.erase(std::find(order.begin(), order.end(), k));
    }
    std::size_t size() const { return order.size(); }
};

// ---- Obs (bc.py) ------------------------------------------------------------
struct Part { char team; int id; bool head; char facing; };

struct Obs {
    int round = 0, length = 0, unit_count = 0;
    char facing = 'N';
    std::vector<std::uint32_t> msgs;
    std::array<int, 49> x{}, y{};
    std::array<char, 49> pearl{};      // 0/1
    std::array<int, 49> pearl_in{};
    std::array<std::optional<Part>, 49> occ{};
    // bodies in wire order: (team, id, x, y, facing, is_head)
    std::vector<std::tuple<char, int, int, int, char, bool>> bodies;
    int hedge[8][7];
    int vedge[7][8];

    std::pair<int, int> head() const { return {x[CENTER], y[CENTER]}; }

    static int step(int k, char d) {
        int i = didx(d), r = k / W + DYi[i], c = k % W + DXi[i];
        return (0 <= r && r < W && 0 <= c && c < W) ? r * W + c : -1;
    }
    int edge(int k, char d) const {
        int r = k / W, c = k % W;
        switch (d) {
            case 'N': return hedge[r][c];
            case 'S': return hedge[r + 1][c];
            case 'W': return vedge[r][c];
            default:  return vedge[r][c + 1];
        }
    }
    bool passable(int k, char d) const {
        if (edge(k, d) != OPEN) return false;
        int n = step(k, d);
        return n >= 0 && !occ[n].has_value();
    }
    std::vector<int> enemy_heads(char team) const {
        std::vector<int> out;
        for (int k = 0; k < 49; ++k)
            if (occ[k] && occ[k]->head && occ[k]->team != team) out.push_back(k);
        return out;
    }
    // shortest paths inside the window over passable cells; {cell:(dist,first)}
    std::unordered_map<int, std::pair<int, char>> bfs(int start, const std::unordered_set<int>* blocked) const {
        std::unordered_map<int, std::pair<int, char>> out;
        out[start] = {0, 0};
        std::vector<int> frontier{start};
        while (!frontier.empty()) {
            std::vector<int> nxt;
            for (int k : frontier) {
                auto [dist, first] = out[k];
                for (char d : DIRS) {
                    if (!passable(k, d)) continue;
                    int n = step(k, d);
                    if (out.count(n) || (blocked && blocked->count(n))) continue;
                    out[n] = {dist + 1, first ? first : d};
                    nxt.push_back(n);
                }
            }
            frontier.swap(nxt);
        }
        return out;
    }
};

inline int edge_tok(const std::string& t) {
    if (t == ".") return OPEN;
    if (t == "w") return KELP;
    return std::stoi(t);
}

// Parse one reconstructed/judge round block into an Obs.
inline Obs parse_obs(const std::string& block) {
    std::vector<std::string> lines;
    { std::stringstream ss(block); std::string ln; while (std::getline(ss, ln)) lines.push_back(ln); }
    auto tok = [](const std::string& s) {
        std::vector<std::string> p; std::stringstream ss(s); std::string w;
        while (ss >> w) p.push_back(w); return p;
    };
    Obs o;
    std::size_t i = 0;
    while (lines[i].rfind("ROUND", 0) != 0) ++i;
    o.round = std::stoi(tok(lines[i])[1]);
    o.facing = tok(lines[i + 1])[1][0];
    o.length = std::stoi(tok(lines[i + 2])[1]);
    o.unit_count = std::stoi(tok(lines[i + 3])[1]);
    int nmsg = std::stoi(tok(lines[i + 4])[1]);
    i += 5;
    for (int j = 0; j < nmsg; ++j) o.msgs.push_back(static_cast<std::uint32_t>(std::stoll(lines[i + j])));
    i += nmsg;
    std::unordered_map<long long, int> index;
    for (int j = 0; j < 49; ++j) {
        auto p = tok(lines[i + j]);
        o.x[j] = std::stoi(p[0]); o.y[j] = std::stoi(p[1]);
        o.pearl[j] = (p[2] == "1") ? 1 : 0; o.pearl_in[j] = std::stoi(p[3]);
        index[static_cast<long long>(o.x[j]) * 100000 + o.y[j]] = j;
    }
    i += 49;
    int nb = std::stoi(tok(lines[i])[1]);
    i += 1;
    for (int j = 0; j < nb; ++j) {
        auto p = tok(lines[i + j]);
        char team = p[0][0]; int did = std::stoi(p[1]);
        int px = std::stoi(p[2]), py = std::stoi(p[3]); char f = p[4][0];
        bool head = (p[5] == "1");
        o.bodies.emplace_back(team, did, px, py, f, head);
        auto it = index.find(static_cast<long long>(px) * 100000 + py);
        if (it != index.end()) o.occ[it->second] = Part{team, did, head, f};
    }
    i += nb;
    for (int r = 0; r < 8; ++r) { auto p = tok(lines[i + r]); for (int c = 0; c < 7; ++c) o.hedge[r][c] = edge_tok(p[c]); }
    i += 8;
    for (int r = 0; r < 7; ++r) { auto p = tok(lines[i + r]); for (int c = 0; c < 8; ++c) o.vedge[r][c] = edge_tok(p[c]); }
    return o;
}

// ---- navigation.Memory (subset used by v6) ----------------------------------
class Nav {
  public:
    int w, h, n;
    bool portals;
    std::vector<int> edges;                                  // 2n, init NONE
    std::unordered_map<int, std::unordered_set<int>> ends;   // portal id -> edge keys
    std::vector<int> seen;                                   // n, init -10000
    std::unordered_map<int, int> visible;                    // cell -> local k

    Nav(int width, int height, bool portals_)
        : w(width), h(height), n(width * height), portals(portals_),
          edges(2 * n, NONE), seen(n, -10000) {}

    void remember(int key, int value) {
        if (edges[key] == value) return;
        edges[key] = value;
        if (value >= 0) ends[value].insert(key);
    }
    int edge_key(int cell, char d) const {
        int x = cell % w, y = cell / w;
        switch (d) {
            case 'N': return cell;
            case 'S': return ((y + 1) % h) * w + x;
            case 'W': return n + cell;
            default:  return n + y * w + (x + 1) % w;
        }
    }
    // -1 open destination cell, or a portal exit; std::nullopt for None
    std::optional<int> destination(int cell, char d) const {
        int key = edge_key(cell, d);
        int value = edges[key];
        if (value == NONE || value == KELP) return std::nullopt;
        if (value >= 0) {
            auto it = ends.find(value);
            if (!portals || it == ends.end() || it->second.size() != 2) return std::nullopt;
            int other = -1;
            for (int kk : it->second) if (kk != key) { other = kk; break; }
            if ((other < n) != (key < n)) return std::nullopt;
            int target = other % n;
            if (d == 'E' || d == 'S') return target;
            int x = target % w, y = target / w;
            if (d == 'W') return y * w + (x - 1 + w) % w;
            return ((y - 1 + h) % h) * w + x;  // d == 'N'
        }
        int x = cell % w, y = cell / w;
        int i = didx(d);
        return ((y + DYi[i] + h) % h) * w + (x + DXi[i] + w) % w;
    }
    void update(const Obs& obs) {
        int x0 = obs.x[0], y0 = obs.y[0];
        for (int r = 0; r < 8; ++r) { int base = ((y0 + r) % h) * w; for (int c = 0; c < 7; ++c) remember(base + (x0 + c) % w, obs.hedge[r][c]); }
        for (int r = 0; r < 7; ++r) { int base = n + ((y0 + r) % h) * w; for (int c = 0; c < 8; ++c) remember(base + (x0 + c) % w, obs.vedge[r][c]); }
        visible.clear();
        for (int k = 0; k < 49; ++k) { int cell = obs.y[k] * w + obs.x[k]; visible[cell] = k; seen[cell] = obs.round; }
    }
};

// hex-string bit test: (int(bits,16) >> key) & 1
inline int hex_bit(const std::string& bits, int key) {
    int nib = key >> 2;
    if (nib >= static_cast<int>(bits.size())) return 0;
    char c = bits[bits.size() - 1 - nib];
    int v = (c >= '0' && c <= '9') ? c - '0' : (c >= 'a' && c <= 'f') ? c - 'a' + 10 : c - 'A' + 10;
    return (v >> (key & 3)) & 1;
}

// ---- core_memory.WorldMemory ------------------------------------------------
struct OccPart { char team; int id; bool head; char facing; int seen; };
using Hubs = std::vector<std::pair<int, double>>;

class WorldMemory {
  public:
    int width, height;
    Nav nav;
    // params come from the params:: namespace (single source)
    std::unordered_map<int, int> spawn_ready;   // cell -> predicted ready round
    std::unordered_map<int, int> pearl;         // cell -> last seen round
    OrderedMap<OccPart> occupied;               // insertion-ordered
    std::vector<std::pair<int, int>> trail;     // (head cell, round)
    int last_round = -1000000000;

    std::vector<std::vector<portal_book::Pair>> book;
    std::unordered_set<int> book_done;

    std::vector<hub_book::Layout> hub_maps;     // candidate layouts
    Hubs hubs;
    Hubs learned_hubs;                          // CPP_HUB_OBSERVE: hubs from this dragon's own observations
    std::unordered_map<int, double> hub_area;

    OrderedMap<int> timer_max;                  // spawn tile -> largest countdown
    std::optional<double> local_rate;

    int sec, sec_w, sec_h;
    std::vector<int> sector_seen;
    std::optional<int> goal;
    int goal_round = -10000;

    WorldMemory(int w, int h)
        : width(w), height(h), nav(w, h, true) {
        if (params::PORTAL_BOOK) {
            auto it = portal_book::book().find({w, h});
            if (it != portal_book::book().end()) book = it->second;
        }
        if (params::HUB_BOOK) {
            auto it = hub_book::book().find({w, h});
            if (it != hub_book::book().end()) hub_maps = it->second;
        }
        sec = params::SECTOR;
        sec_w = (w + sec - 1) / sec; sec_h = (h + sec - 1) / sec;
        sector_seen.assign(sec_w * sec_h, -10000);
    }

    int cell(int x, int y) const { return y * width + x; }

    void update(const Obs& obs) {
        last_round = obs.round;
        nav.update(obs);
        if (!book.empty()) apply_book();
        const auto& visible = nav.visible;
        if (!hub_maps.empty()) identify_map(obs);
        std::vector<double> rates;
        for (auto& [c, k] : visible) {
            sector_seen[(c / width / sec) * sec_w + (c % width) / sec] = obs.round;
            int timer = obs.pearl_in[k];
            if (timer >= 0) {
                int* cur = timer_max.find(c);
                if (cur == nullptr || timer > *cur) timer_max.set(c, timer);
                rates.push_back(1.0 / (1 + *timer_max.find(c)));
            }
        }
        // Python: sum(rates)/len(rates); order-independent here we sum as pushed.
        if (rates.empty()) local_rate.reset();
        else { double s = 0; for (double r : rates) s += r; local_rate = s / rates.size(); }
        if (params::LEARN_HUBS && hub_maps.empty()) learn_hubs(obs);
        else if (params::CPP_HUB_OBSERVE && params::LEARN_HUBS) {
            // A book map: the server's variants move or kill its hubs (29 Sep A/B:
            // the book helps on original spawns, -0.103 without it, but not on
            // perturbed ones, +0.048 without it). Use the book until this dragon
            // has seen spawners itself, then trust what it saw.
            learn_hubs(obs, false);
            if (!learned_hubs.empty()) set_hubs(learned_hubs);
        }

        for (auto& [c, k] : visible) {
            if (obs.pearl_in[k] >= 0) spawn_ready[c] = obs.round + obs.pearl_in[k];
            else spawn_ready.erase(c);
            if (obs.pearl[k]) pearl[c] = obs.round; else pearl.erase(c);
            occupied.erase(c);
        }
        for (auto& b : obs.bodies) {
            auto [team, did, bx, by, f, head] = b;
            occupied.set(cell(bx, by), OccPart{team, did, head, f, obs.round});
        }
        // TTL filters, preserving current insertion order
        for (auto it = pearl.begin(); it != pearl.end();)
            it = (obs.round - it->second > params::PEARL_TTL) ? pearl.erase(it) : std::next(it);
        OrderedMap<OccPart> kept;
        for (int c : occupied.order) {
            const OccPart& p = *occupied.find(c);
            if (obs.round - p.seen <= params::OCC_TTL) kept.set(c, p);
        }
        occupied = std::move(kept);

        trail.emplace_back(cell(obs.x[CENTER], obs.y[CENTER]), obs.round);
        if (static_cast<int>(trail.size()) > 60) trail.erase(trail.begin(), trail.end() - 60);
    }

    void apply_book() {
        for (auto& [pid, keys] : nav.ends) {
            if (book_done.count(pid) || keys.size() != 1) continue;
            int key = *keys.begin();
            std::unordered_set<int> partners;
            for (auto& m : book) {
                for (auto& pr : m) if (pr.id == pid) {
                    if (pr.a == key) partners.insert(pr.b);
                    else if (pr.b == key) partners.insert(pr.a);
                }
            }
            book_done.insert(pid);
            if (partners.size() == 1) keys.insert(*partners.begin());
        }
    }

    void identify_map(const Obs& obs) {
        int w = width, h = height, nn = w * h;
        int x0 = obs.x[0], y0 = obs.y[0];
        std::vector<std::pair<int, int>> seen;  // (edge key, closed?)
        for (int r = 0; r < 8; ++r) { int base = ((y0 + r) % h) * w; for (int c = 0; c < 7; ++c) seen.emplace_back(base + (x0 + c) % w, obs.hedge[r][c] != OPEN); }
        for (int r = 0; r < 7; ++r) { int base = nn + ((y0 + r) % h) * w; for (int c = 0; c < 8; ++c) seen.emplace_back(base + (x0 + c) % w, obs.vedge[r][c] != OPEN); }
        std::vector<hub_book::Layout> keep;
        for (auto& lay : hub_maps) {
            bool ok = true;
            for (auto& [key, closed] : seen) if (hex_bit(lay.bits, key) != (closed ? 1 : 0)) { ok = false; break; }
            if (ok) keep.push_back(lay);
        }
        hub_maps = std::move(keep);
        // choices = unique hub-lists; if exactly one, adopt it, else []
        Hubs first; bool have = false; bool unique = true;
        for (auto& lay : hub_maps) {
            Hubs cur; for (auto& hh : lay.hubs) cur.emplace_back(hh.cell, hh.value);
            if (!have) { first = cur; have = true; }
            else if (cur != first) { unique = false; break; }
        }
        set_hubs(have && unique ? first : Hubs{});
    }

    void set_hubs(const Hubs& new_hubs) {
        if (new_hubs == hubs) return;
        hubs = new_hubs;
        hub_area.clear();
        for (auto& [hub, value] : hubs) {
            int x = hub % width, y = hub / width;
            for (int dy = -2; dy <= 2; ++dy)
                for (int dx = -2; dx <= 2; ++dx) {
                    int c = ((y + dy + height) % height) * width + (x + dx + width) % width;
                    auto it = hub_area.find(c);
                    if (it == hub_area.end() || value > it->second) hub_area[c] = value;
                }
        }
    }

    void learn_hubs(const Obs& obs, bool apply = true) {
        if (obs.round % params::LEARN_EVERY || timer_max.size() == 0) return;
        int w = width, h = height;
        std::unordered_map<int, double> rate;
        for (int c : timer_max.order) rate[c] = 1.0 / (1 + *timer_max.find(c));
        // local[c] in timer_max insertion order (Python dict order)
        std::vector<std::pair<int, double>> local;
        std::unordered_map<int, double> localval;
        for (int c : timer_max.order) {
            int x = c % w, y = c / w; double s = 0;
            for (int dy = -2; dy <= 2; ++dy)
                for (int dx = -2; dx <= 2; ++dx) {
                    auto it = rate.find(((y + dy + h) % h) * w + (x + dx + w) % w);
                    if (it != rate.end()) s += it->second;
                }
            local.emplace_back(c, s); localval[c] = s;
        }
        double mean = 0; for (auto& [c, v] : local) mean += v; mean /= local.size();
        double best = local[0].second; for (auto& [c, v] : local) best = std::max(best, v);
        // stable sort by -value (Python sorted is stable on insertion order)
        std::stable_sort(local.begin(), local.end(),
                         [](auto& a, auto& b) { return a.second > b.second; });
        Hubs picked;
        for (auto& [c, v] : local) {
            if (static_cast<int>(picked.size()) >= 4 || v <= 0 || v < 2 * mean) break;
            bool far = true;
            for (auto& [q, _] : picked) {
                int dxm = std::max(std::abs(c % w - q % w), w - std::abs(c % w - q % w));
                int dym = std::max(std::abs(c / w - q / w), h - std::abs(c / w - q / w));
                if (std::max(dxm, dym) < 5) { far = false; break; }
            }
            if (far) picked.emplace_back(c, std::round(v / best * 1000.0) / 1000.0);
        }
        learned_hubs = picked;
        if (apply) set_hubs(picked);
    }

    void update_goal(const Obs& obs, int did) {
        int s = params::SECTOR;
        if (goal.has_value()) {
            int gs = (*goal / width / s) * sec_w + (*goal % width) / s;
            bool fresh = obs.round - sector_seen[gs] <= 1;
            if (!fresh && obs.round - goal_round < params::GOAL_EVERY) return;
        }
        int hx = obs.x[CENTER], hy = obs.y[CENTER];
        int w = width, h = height;
        std::optional<int> best; double best_score = 0;
        for (int sy = 0; sy < sec_h; ++sy)
            for (int sx = 0; sx < sec_w; ++sx) {
                int cx = std::min(sx * s + s / 2, w - 1), cy = std::min(sy * s + s / 2, h - 1);
                int age = std::min(obs.round - sector_seen[sy * sec_w + sx], params::GOAL_STALE_CAP);
                if (age <= 1) continue;
                int dx = std::abs(cx - hx), dy = std::abs(cy - hy);
                int dist = std::min(dx, w - dx) + std::min(dy, h - dy);
                long long raw = (static_cast<long long>(did) * 2654435761LL + static_cast<long long>(sy * sec_w + sx) * 40503LL) >> 7;
                double noise = (raw % 1000) / 1000.0;
                double score = age - params::GOAL_DIST_W * dist + params::GOAL_NOISE * noise;
                if (!best.has_value() || score > best_score) { best = cy * w + cx; best_score = score; }
            }
        goal = best; goal_round = obs.round;
    }

    // newest-first own body cells, or empty if the trail is too short / loops
    std::optional<std::vector<int>> trail_body(int length) const {
        if (length > static_cast<int>(trail.size()) || length > 60) return std::nullopt;
        std::vector<int> cells;
        for (int i = static_cast<int>(trail.size()) - length; i < static_cast<int>(trail.size()); ++i)
            cells.push_back(trail[i].first);
        std::reverse(cells.begin(), cells.end());
        std::unordered_set<int> uniq(cells.begin(), cells.end());
        if (uniq.size() != cells.size()) return std::nullopt;
        return cells;
    }
};

}  // namespace v6
