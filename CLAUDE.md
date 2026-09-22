See README.md for layout and commands.

- Use `.venv\Scripts\python` for all tooling. The unswbc CLI may not be on PATH: `C:\Users\Sea7\AppData\Local\Python\pythoncore-3.14-64\Scripts\unswbc.exe`.
- Edit shared code in `framework/`, never the copies inside bot folders; run `python -m bcsim.sync` after.
- Bots must keep state on `self` only (the arena gives each dragon fresh module copies; the judge gives each its own process).
- Judge budget: 100M CPU points per dragon-turn, Python 3.13 + NumPy only. Verify heavy changes with `unswbc run ... --sandbox`.
- Before claiming an improvement, run `python -m bcsim.arena eval mybot --vs <latest version>,splitter` with enough seeds that the CI excludes 50%.
- Do not submit (`unswbc submit`) without the user's go-ahead.
