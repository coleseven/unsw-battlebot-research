See README.md for layout and commands.

- Use `.venv\Scripts\python` for all tooling. The unswbc CLI may not be on PATH: `C:\Users\Sea7\AppData\Local\Python\pythoncore-3.14-64\Scripts\unswbc.exe`.
- Edit shared code in `framework/`, never the copies inside bot folders; run `python -m bcsim.sync` after.
- Bots must keep state on `self` only (the arena gives each dragon fresh module copies; the judge gives each its own process).
- Judge budget: 100M CPU points per dragon-turn, Python 3.13 + NumPy only. Verify heavy changes with `unswbc run ... --sandbox`.
- Before claiming an improvement, compare against the latest version and distinct sparring opponents on the full official suite; require a benefit that is robust across maps and opponents. Do not treat duplicate deterministic seed runs or their narrow CI as independent evidence.
- For **every bot-change evaluation**, including map-specific logic, play both sides on all 11 distinct official maps using `bcsim.official_suite.official_maps()` and `require_coverage()`. Small-map diagnostic probes are allowed, but never substitute for the full-suite result. The suite is Default Small, Trophy, Queen Of Spades, Default, Devil, stronghold, Trauma, Schooltime, Big Empty, Arena, Colosseum.
- Use memory-safe full compute by default: `bcsim.official_suite.DEFAULT_WORKERS` (currently eight workers on this host), `bcsim.guarded.stage` / `bcsim.bounded.run`, and their RAM checks. A 16-worker nicked screen exhausted available RAM on 25 Sep; its 49 valid games were resumed at six workers. Training may use available CPU/GPU rather than the former one-worker testing throttle, but keep memory checks and checkpoints. Use one bot RNG seed for deterministic in-process policies: changing that seed does not independently reseed the map engine, so repeated identical replays are not extra evidence. Add distinct opponents/maps instead.
- Do not submit (`unswbc submit`) without the user's go-ahead.
