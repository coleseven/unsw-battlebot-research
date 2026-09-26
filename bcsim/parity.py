"""Matching harness for the V7 C++ port: identical actions from Python v6
(PARITY mode) and the C++ v7 bot on the same observation sequences.

    python -m bcsim.parity                 # build, generate replays, compare
    python -m bcsim.parity --replays DIR   # compare on existing .replay files

For every dragon in a replay, `bcsim.reconstruct.turns` gives the exact round
block the engine sent it, in order. A fresh Python brain and a fresh C++
process are fed those blocks and their action lines compared. A dragon is
dropped at its first mismatch (memories then diverge). Both implementations run
with the wall-clock budget off (PARITY); the C++ search is always deterministic.

Pass mark (plan G1): 100% identical actions on >= 20,000 dragon-turns spread
over all 11 official maps and both sides.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

from . import match, official_suite, reconstruct
from . import replay as rp
from . import v6_initial
from .paths import ROOT

CPPBOT = ROOT / "cppbot"


# ---- building --------------------------------------------------------------

def build_cpp(out: pathlib.Path) -> pathlib.Path:
    """Compile cppbot/main.cpp with clang++ (preferred) or g++."""
    for cxx in ("clang++", "g++"):
        if shutil.which(cxx) is None:
            continue
        cmd = [cxx, "-std=c++17", "-O2", "-I", str(CPPBOT),
               str(CPPBOT / "main.cpp"), "-o", str(out)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            return out
        sys.stderr.write(f"{cxx} failed:\n{proc.stderr}\n")
    raise RuntimeError("no working C++ compiler (need clang++ or g++)")


def python_parity_bot(tmp: pathlib.Path) -> match.InProcessBot:
    """A framework-source v6 snapshot with PARITY = True."""
    dest = tmp / "v6_parity"
    v6_initial.variant(dest)
    params = dest / "core_params.py"
    params.write_text(params.read_text(encoding="utf8") + "\nPARITY = True\n", encoding="utf8")
    return match.InProcessBot(dest)


# ---- the C++ process wrapper -----------------------------------------------

class CppDragon:
    def __init__(self, binary: pathlib.Path, init_text: str) -> None:
        self.proc = subprocess.Popen([str(binary)], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True)
        self.proc.stdin.write(init_text)
        self.proc.stdin.flush()

    def step(self, block: str) -> str:
        if not block.endswith("\n"):
            block += "\n"
        self.proc.stdin.write(block)
        self.proc.stdin.flush()
        first = None
        while True:
            line = self.proc.stdout.readline()
            if line == "":
                raise RuntimeError("C++ bot exited early")
            line = line.rstrip("\n")
            if first is None:
                first = line
            if line == "ENDTURN":
                return first

    def close(self) -> None:
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        self.proc.terminate()


# ---- comparison ------------------------------------------------------------

def init_text(turn, width: int, height: int) -> str:
    return f"ID {turn.id}\nTEAM {turn.team}\nMAP {width} {height}\nUNIT_LIMIT 64\n"


def compare(replay: rp.Replay, py_bot: match.InProcessBot, binary: pathlib.Path):
    """Return (width, height, turns_compared, mismatches list)."""
    board = reconstruct.Board(replay.map_text)
    w, h = board.w, board.h
    py, cpp, dead = {}, {}, set()
    compared = 0
    mismatches = []
    for turn in reconstruct.turns(replay):
        if turn.id in dead:
            continue
        if turn.id not in py:
            it = init_text(turn, w, h)
            py[turn.id] = py_bot.new_brain(it, seed=0)
            cpp[turn.id] = CppDragon(binary, it)
        py_action = py[turn.id].step(turn.block).split("\n")[0]
        cpp_action = cpp[turn.id].step(turn.block)
        compared += 1
        if py_action != cpp_action:
            mismatches.append((turn.id, turn.round, py_action, cpp_action, turn.block))
            dead.add(turn.id)
            cpp[turn.id].close()
    for d in cpp.values():
        d.close()
    return w, h, compared, mismatches


def replay_specs(opponents: list[str]):
    """Yield (map_path, bot_a, bot_b, name): v6 on both sides vs each opponent."""
    v6 = ROOT / "versions/v6"
    for map_path in official_suite.official_maps():
        for opp in opponents:
            other = ROOT / opp
            for a, b, tag in ((v6, other, "A"), (other, v6, "B")):
                yield map_path, a, b, f"{map_path.stem}-{other.name}-{tag}.replay"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--replays", type=pathlib.Path,
                    help="directory of .replay files to compare on")
    ap.add_argument("--opponents", nargs="*", default=["versions/v6", "opponents/splitter"],
                    help="bots v6 plays (both sides) to generate replays")
    ap.add_argument("--binary", type=pathlib.Path, help="prebuilt C++ bot")
    ap.add_argument("--show", type=int, default=3, help="mismatches to print per map")
    args = ap.parse_args()

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="parity-"))
    binary = args.binary or build_cpp(tmp / "cppbot")
    py_bot = python_parity_bot(tmp)

    # Stream: generate (or load) each replay, compare and print before the next,
    # so a hang or a mismatch shows up immediately, not after the whole suite.
    def sources():
        if args.replays:
            for p in sorted(args.replays.glob("*.replay")):
                yield rp.load(p), p.name
        else:
            rdir = tmp / "replays"
            rdir.mkdir(parents=True, exist_ok=True)
            for map_path, a, b, name in replay_specs(args.opponents):
                match.play(map_path, a, b, seed=1, replay_to=rdir / name)
                yield rp.load(rdir / name), name

    per_map_turns: dict[str, int] = defaultdict(int)
    per_map_mismatch: dict[str, int] = defaultdict(int)
    total_turns = total_mismatch = 0
    empty = True
    for replay, name in sources():
        empty = False
        w, h, compared, mismatches = compare(replay, py_bot, binary)
        key = f"{w}x{h}"
        per_map_turns[key] += compared
        per_map_mismatch[key] += len(mismatches)
        total_turns += compared
        total_mismatch += len(mismatches)
        flag = "OK" if not mismatches else f"MISMATCH x{len(mismatches)}"
        print(f"{name:42s} {key:8s} turns={compared:6d}  {flag}", flush=True)
        for did, rnd, pa, ca, block in mismatches[:args.show]:
            print(f"    dragon {did} round {rnd}: py={pa!r} cpp={ca!r}", flush=True)

    if empty:
        sys.exit("no replays to compare")
    print("\n=== per map size ===")
    for key in sorted(per_map_turns):
        print(f"  {key:8s} turns={per_map_turns[key]:7d} mismatched_dragons={per_map_mismatch[key]}")
    print(f"\nTOTAL dragon-turns compared: {total_turns}")
    print(f"TOTAL mismatched dragons:    {total_mismatch}")
    ok = total_mismatch == 0 and total_turns >= 20000
    print("G1:", "PASS" if ok else f"not yet ({'mismatches' if total_mismatch else 'need 20k turns'})")
    sys.exit(0 if total_mismatch == 0 else 1)


if __name__ == "__main__":
    main()
