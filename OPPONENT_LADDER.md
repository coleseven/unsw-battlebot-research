# Opponent ladder (2026-09-25)

A ladder of local opponents to train against: beat each rung, then move up.
Research only: nothing new was run to build this. Rankings come from games
already on disk, the public leaderboard, and the bots' own write-ups. All
third-party bots live in git-ignored `sparring/`, passed the static security
review in `sparring/TRIAGE.md`, and must never be copied into our bot (no
licenses).

Every comparison should use the same map set as `V5_VS_NICKED_BRIEF.md`: the 9
ranked maps plus Arena and Colosseum, both sides, one seed (games are
deterministic): **22 games per pairing**.

## The ladder

| Rung | Opponent | Where | Evidence | Confidence |
|---|---|---|---|---|
| 0 | Our scripted bots: wanderer, greedy, hunter, splitter, turtle, starter | `opponents/` | v3 beats splitter/hunter ~90% | measured |
| 1 | v1, v2 | `versions/` | v3 beat v2 126-50 locally; v2 went 48-55 in ranked games on the site | measured |
| 1 | **ctmes** (Python, CMA-ES tuned) | `sparring/ctmes` | **3-8 against v3** (11 distinct games); won only Trauma twice and Queen once | measured |
| 2 | v3 | `versions/v3` | Frozen reference | measured |
| 2 | additive v4 (our live bot) | Codex experiments | Beat v2 8-0 locally; 7-20 in its first 27 site games against 1,440-2,100 teams | measured, small |
| 3 | **nicked v34** (Python) | `sparring/nicked` | **8-2 against v3** (10 distinct games): wins Default, Default Small, Queen, Trauma on both sides; loses Colosseum both sides. Beat every v3/v4/v5 variant tested | measured |
| 3-4 | **nicked v44** (Python, current) | `sparring/nicked_v44` | Adds founder kings, long-dragon protection and endgame cash-in on top of v34's engine. Its own history: v42 was "mostly revert back to v23", so newer is not guaranteed stronger | unmeasured |
| 3-4 | **Leviathan / KrakenSlayer** (C++, TX140907) | `sparring/cpp_leviathan`, `cpp_krakenslayer` (= `cpp_leviathan3`) | Team "An IQ too high?" (site id 128): **rank 68, rated 1713** on 25 Sep (1743 on 24 Sep). Their docs: Leviathan beat NamBot and their mybot 40-0; Kraken lost 6-14 to Leviathan | ladder-linked, unmeasured locally |
| ? | devkadaba Python (`main.py`, sonar flagship) and C++ `cpp_bot` (v6) | `sparring/devkadaba`, `cpp_devkadaba` | Own acceptance tests only (80-100% against their own practice bots). C++ v6 was their ranked submission; they report 82 of 91 round-limit losses on longest dragon | unknown |
| ? | zylotomous mybot2 ("v30") and mybot3 | `sparring/zylotomous2`, `zylotomous3` | No results published | unknown |
| ? | seadragon / portoff (C++, Aarav) | `sparring/cpp_seadragon`, `cpp_portoff` | 30-2 against their own starter-level bots only | unknown, probably low-mid |
| low | NamBot (Python, TX140907's early bot) | `sparring/nambot` | Lost 0-20 to Leviathan | probably low |
| 5 | Top-10 ladder teams | not public | Only their replays: `TOP_TEAMS_SCOUTING.md` | study only |

## How to fill in the unknowns (for Codex)

1. **Python round-robin first** (cheapest; no compiler needed): v3, additive v4,
   ctmes, nicked v34, nicked v44, devkadaba, zylotomous2, zylotomous3, nambot.
   22 games per pairing. Run one third-party bot build at a time (the Windows
   `.unswbc-build` race hit earlier), with bounded workers. Fit Elo from the
   results (`bcsim.arena tournament` fits Elo; it needs these directories
   registered as opponents, or pointed to by path).
2. **C++ bots through the judge's own compiler:** the toolkit ships clang for
   wasm32-wasi (`--sandbox` path in `unswbc`), so no local g++ is needed.
   Build from the reviewed source only, never the prebuilt `.exe` files in their
   repos. Never build seadragon/portoff with `-DSEAD_*` (enables debug file
   writes). Add Leviathan, KrakenSlayer, Kraken, devkadaba `cpp_bot`,
   seadragon, and portoff to the round-robin once they build.
3. **Re-rank** by fitted Elo, then keep only the rungs that separate: 1-2 bots
   per tier is enough. Suggested regular gauntlet: ctmes (floor check),
   additive v4 (regression), nicked v34, nicked v44, Leviathan (ladder anchor
   at ~1713).
4. **Anchor to the real ladder:** Leviathan's team rating (~1713) is the only
   link between local Elo and site Elo. Our team (site id 590) is rank 183 at
   1478 of 788 teams on 25 Sep. If our bot beats Leviathan locally but sits
   well below ~1713 on the site, the local ladder is missing something the real
   ladder punishes (likely king feeding; see `TOP_TEAMS_SCOUTING.md`).
5. **Refresh opponents:** nicked went from v29 to v44 in about a day; re-pull
   `nicked` and TX140907 weekly, re-run the static review, and keep old
   snapshots as lower rungs.

## What beating each rung requires (from the evidence so far)

- **ctmes:** v3 already does (8-3).
- **nicked v34:** portals, survival and economy (P1-P3 in
  `V5_VS_NICKED_BRIEF.md`); v3's only wins came on Colosseum, where early
  elimination matters more than economy.
- **nicked v44 and the ladder top:** additionally, early kings and high-volume
  feeding from round ~400 (P6), since the top teams' kings reach 30-46.
