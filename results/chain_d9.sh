#!/usr/bin/env bash
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8 PYTHONPATH=.
rm -rf results/equiv-v12s results/stripes-v12s
.venv/Scripts/python -W ignore results/equivalence_check.py versions/v11t results/v12s-bot results/equiv-v12s
echo "$(date -u +%H:%M) EQUIV DONE"
.venv/Scripts/python -W ignore results/next-steps-20261004/stripes_confirm.py results/v12s-bot results/stripes-v12s
echo "$(date -u +%H:%M) D9 DONE"
