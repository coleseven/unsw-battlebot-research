// V7 C++ bot entry point. Reads the same stdin protocol as framework/bc.py's
// bc.run: the spawn header, then one round block per turn, replying with the
// action line and ENDTURN. One buffered write per turn.
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

#include "v6_brain.hpp"

namespace {

bool read_line(std::string& out) {
    if (!std::getline(std::cin, out)) return false;
    if (!out.empty() && out.back() == '\r') out.pop_back();
    return true;
}

std::string second_token(const std::string& line) {
    std::stringstream ss(line);
    std::string a, b;
    ss >> a >> b;
    return b;
}

}  // namespace

int main() {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 16);

    // Spawn header, up to and including the UNIT_LIMIT line.
    std::vector<std::string> header;
    std::string line;
    while (read_line(line)) {
        std::string trimmed = line;
        std::size_t s = trimmed.find_first_not_of(" \t");
        if (s == std::string::npos) { if (!header.empty()) break; else continue; }
        header.push_back(line);
        if (line.rfind("UNIT_LIMIT", 0) == 0) break;
    }
    std::string init_text;
    for (auto& h : header) init_text += h + "\n";
    v6::Brain brain(v6::parse_init(init_text));

    while (true) {
        std::vector<std::string> lines;
        // skip to the next ROUND line
        while (read_line(line) && line.rfind("ROUND", 0) != 0) {}
        if (std::cin.eof() && line.rfind("ROUND", 0) != 0) return 0;
        lines.push_back(line);
        for (int i = 0; i < 4; ++i) { if (!read_line(line)) return 0; lines.push_back(line); }
        int n = std::stoi(second_token(lines.back()));  // NUM_MSGS
        for (int i = 0; i < n + 49; ++i) { if (!read_line(line)) return 0; lines.push_back(line); }
        if (!read_line(line)) return 0;                 // DRAGON_BODIES header
        lines.push_back(line);
        int b = std::stoi(second_token(line));
        for (int i = 0; i < b + 15; ++i) { if (!read_line(line)) return 0; lines.push_back(line); }

        std::string block;
        for (auto& l : lines) block += l + "\n";
        v6::Obs obs = v6::parse_obs(block);
        std::string action = brain.turn(obs);
        std::cout << action << "\n" << "ENDTURN\n";
        std::fflush(stdout);
    }
}
