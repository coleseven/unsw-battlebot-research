#!/usr/bin/env bash
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
.venv/Scripts/python -W ignore results/next-steps-20261004/zone_probe.py results/v11t12-bot results/wh-notrap results/wh-gpath results/wh-unseen3 results/wh-nogoal sparring/cpp_nicked_v92
echo "$(date -u +%H:%M) ZONE DONE"
