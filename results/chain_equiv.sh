#!/usr/bin/env bash
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
rm -rf results/equiv-v11t
.venv/Scripts/python -W ignore results/equivalence_check.py versions/v11t results/v11t5-bot results/equiv-v11t
echo "$(date -u +%H:%M) EQUIV DONE rc=$?"
