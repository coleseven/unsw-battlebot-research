#!/usr/bin/env bash
# Detached overnight chain (2 Oct): each step waits for the guard lock and resumes
# completed variants, so it is safe to run while another guarded job is active.
cd "/c/Users/Sea7/Desktop/unsw battlebot"
export PATH="/c/Users/Sea7/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.WinLibs.POSIX.UCRT.LLVM_Microsoft.Winget.Source_8wekyb3d8bbwe/mingw64/bin:$PATH"
export BCSIM_DETERMINISTIC_V6=1 BCSIM_CPP_INPROC=1 PYTHONIOENCODING=utf-8
for A in results/20261002-133325-ablate-192622; do
  echo "$(date -u +%H:%M) start $A"
  .venv/Scripts/python -W ignore -m bcsim.queen_runtime bcsim.ablate $A --run --workers 12 >> $A/run.log 2>&1
  echo "$(date -u +%H:%M) done $A rc=$?"
  .venv/Scripts/python -W ignore -m bcsim.queen_runtime bcsim.ablate $A --report > /dev/null 2>&1
done
echo "$(date -u +%H:%M) CHAIN DONE"
