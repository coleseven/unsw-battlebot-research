// Local-simulation C ABI around the v7 C++ brain.
//
// Compiled into a shared library and loaded by bcsim.match through ctypes when
// BCSIM_CPP_INPROC=1, so the tuner can run the C++ bot in-process (one handle
// per dragon) instead of one OS process per dragon. This file is NOT part of
// the uploaded bot: it lives outside every bot directory, so the judge build
// (bot.toml's *.cpp/*.hpp globs) never sees it. It is built with -I <botdir>,
// so it uses that directory's own headers and params.hpp -- the exact same
// sources and numbers main.cpp builds from -- and every reply is byte-identical
// to what main.cpp writes for the same input.
//
// All mutable state lives in the handle (one v6::Brain per dragon); the only
// file-scope state in the headers is read-only book data, so dragons are
// isolated exactly as separate processes are on the judge.
#include <string>

#include "v6_brain.hpp"

namespace {
struct Handle {
    v6::Brain brain;
    std::string reply;  // keeps the returned C string alive until the next call
    explicit Handle(const std::string& init) : brain(v6::parse_init(init)) {}
};
}  // namespace

extern "C" {

// One handle = one dragon = one fresh brain. `seed` is accepted for a general
// ABI but unused: the C++ bot is deterministic, exactly as main.cpp is.
void* bc_new(const char* init_text, unsigned long long seed) {
    (void)seed;
    try {
        return new Handle(std::string(init_text));
    } catch (...) {
        return nullptr;
    }
}

// Returns the full reply for one turn, "<action>\nENDTURN\n", identical to what
// main.cpp prints. The pointer is valid until the next bc_step/bc_free on this
// handle. A C++ exception must never cross the C boundary, so it is caught and
// turned into a no-op reply (in practice the port never throws).
const char* bc_step(void* h, const char* turn_block) {
    Handle* handle = static_cast<Handle*>(h);
    try {
        v6::Obs obs = v6::parse_obs(std::string(turn_block));
        handle->reply = handle->brain.turn(obs) + "\nENDTURN\n";
    } catch (...) {
        handle->reply = "\nENDTURN\n";
    }
    return handle->reply.c_str();
}

void bc_free(void* h) { delete static_cast<Handle*>(h); }

}  // extern "C"
