#!/usr/bin/env bash
# Plays the showcase matches (one guarded job at a time). See make_showcase.py.
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
rm -rf showcase/run-old showcase/run-queen showcase/replays
.venv/Scripts/python -W ignore showcase/make_showcase.py old
echo "OLD DONE rc=$?"
.venv/Scripts/python -W ignore showcase/make_showcase.py queen
echo "QUEEN DONE rc=$?"
