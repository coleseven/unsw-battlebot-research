#!/usr/bin/env bash
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
.venv/Scripts/python -W ignore results/sprinter_check.py
echo "$(date -u +%H:%M) CHECK DONE"
A=results/20261006-180726-ablate-ea6fce
.venv/Scripts/python -W ignore -m bcsim.queen_runtime bcsim.ablate $A --run --workers 12 >> $A/run.log 2>&1
echo "$(date -u +%H:%M) done $A rc=$?"
.venv/Scripts/python -W ignore -m bcsim.queen_runtime bcsim.ablate $A --report > /dev/null 2>&1
echo "$(date -u +%H:%M) CHAIN DONE"
