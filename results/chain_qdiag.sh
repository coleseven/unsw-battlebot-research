#!/usr/bin/env bash
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
echo "$(date -u +%H:%M) start"
.venv/Scripts/python -W ignore results/queen_replays.py results/20261003-134712-ablate-e3fcd5 t2 results/qdiag-t2
echo "$(date -u +%H:%M) QDIAG DONE rc=$?"
