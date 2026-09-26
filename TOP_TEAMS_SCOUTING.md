# Top 10 teams: scouting report (2026-09-24)

Research only. Source: the 12 most recent ranked battles of each of the current
top 10 leaderboard teams (600 team-games, 555 distinct after removing identical
rematches). Full tables: `data/scout-top10-20260924.md` / `.json`.

Reproduce or refresh:

```
python -m bcsim.scrape --team 470 --team 545 ... --max-battles 12 --pages 3
python -m bcsim.scout  --team 470 --team 545 ...        # or --leaderboard 10
```

## Caveats

- **Identical rematches:** a rematch between the same two submissions on the
  same map produces an identical game, so outcomes look deterministic. Duplicates
  are counted once (forgot to mention had 21 of 60).
- **Sample:** about 55 distinct games per team, mostly against 1,850-2,000 rated
  teams. Map cells hold 1-10 games each, so per-map records are indicative only.
- **Sonar contents are not readable:** every public-replay sonar value decodes as
  0. Ping counts are real (our v2 sends none and shows none).
- **Which submission:** most teams played one or two submissions in the sample
  (listed in the full report). Check Raise's sample is older (22 Sep) and it has
  dropped to ~1840 since.
- "Elo" is the rating recorded with each team's latest downloaded battle.

## The shared playbook

Nine of the ten play the same macro plan; the differences are in execution:

1. Split at length 4 into length-2 children from round 0 (every team).
2. Grow a swarm to 35-60 dragons, eating 650-1,040 pearls per game.
3. Stop splitting around rounds 440-477.
4. **Feed a king in the last ~50-100 rounds.** Swarm dragons die on purpose next
   to the chosen dragon, and it eats the pearls their corpses drop (⌈L/2⌉ each).

Evidence for feeding: after round 400, **52-73% of the pearls eaten by the final
longest dragon come from its own team's corpses** for seven of the ten teams.
Their longest dragon typically goes from ~5 at round 400 to 20-30 at round 450
and 30-46 at round 499, while alive count halves and total length barely drops.

| Team | King's late pearls from own corpses | How feeders die (late deaths) | King median r400 → r450 → r499 |
|---|---|---|---|
| 龙虎豹 | 70% | self-collision 58% | 5 → 28 → 46 |
| dev test 1 :P | 58% | self-collision 61% | 6 → 23 → 43 |
| SSS | 69% | empty turn 64% | 8 → 22 → 38 |
| 𓎼𓃭𓅱𓂋𓇌 𓏏𓅱 𓂋𓄿 | 59% | empty turn 36%, self 32% | 11 → 22 → 28 |
| Sabotage-d | 68% | self-collision 42% | 5 → 12 → 28 |
| SHINK AI 6500 | 52% | self-collision 52% | 15 → 20 → 30 |
| forgot to mention | 73% | empty turn 81% | 15 → 29 → 33 |
| NeungzAI | 25% (no feeding) | head-on 43% | 18 → 10 → 18 |
| Check Raise | 38% (no feeding) | head-on 68% | 12 → 4 → 14 |
| Sponge | 39% (little) | head-on 41% | 7 → 17 → 22 |

(Median over round-limit games; the king is the team's longest dragon at the
end, so earlier values are that same dragon's length.)

Two execution habits separate the top from us:

- **Few deaths into their own dragons:** 5-11 per game for the top four, versus
  ~101 for our v2. NeungzAI (102) is the exception.
- **Heavy sonar** (one ping per dragon per turn, 11k-39k per game) for seven
  teams, and **portal use** (23-104 portal steps per game) for most. Nobody uses
  sprint (at most 1% of moves). Enemy-body kills are rare (1-3 per game).

## Comparison

Per game, their side. "Head-on up/even/down" = our dead dragon was
shorter/equal/longer than the enemy it traded with.

| Team | Elo | Games | W-L | Elim W / L | Pearls | Last split (median round) | Peak alive | Longest @499 in wins | Own-team deaths | Head-on up/even/down | Portal steps | Sonar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 龙虎豹 | 2075 | 57 | 45-12 | 16 / 5 | 1040 | 471 | 60 | 49 | 8 | 24/35/41% | 46 | 18,012 |
| dev test 1 :P | 2076 | 56 | 46-10 | 23 / 3 | 882 | 466 | 52 | 48 | 11 | 28/38/35% | 53 | 11,945 |
| SSS | 2049 | 57 | 36-21 | 15 / 14 | 646 | 319 | 47 | 42 | 22 | 44/33/23% | 104 | 28,025 |
| 𓎼𓃭𓅱𓂋𓇌 𓏏𓅱 𓂋𓄿 | 2018 | 54 | 30-24 | 12 / 7 | 732 | 472 | 35 | 47 | 5 | 38/24/38% | 23 | 38,846 |
| Sabotage-d (Python) | 1962 | 60 | 33-27 | 14 / 11 | 825 | 477 | 52 | 47 | 30 | 38/35/28% | 60 | 2,478 |
| SHINK AI 6500 | 2002 | 57 | 32-25 | 14 / 12 | 751 | 457 | 43 | 32 | 47 | 34/33/33% | 104 | 1,422 |
| forgot to mention | 1987 | 39 | 23-16 | 12 / 8 | 732 | 369 | 42 | 56 | 8 | 37/41/22% | 57 | 20,182 |
| NeungzAI | 1982 | 60 | 39-21 | 19 / 11 | 973 | 470 | 36 | 18 | 102 | 28/34/38% | 47 | 18,344 |
| Check Raise | 1842 | 49 | 22-27 | 12 / 12 | 832 | 467 | 39 | 12 | 34 | 38/39/23% | 10 | 0 |
| Sponge | 1993 | 54 | 36-18 | 21 / 7 | 768 | 439 | 43 | 28 | 25 | 37/30/34% | 65 | 1 |

## Team profiles

### 1. 龙虎豹 (2075, C++): the reference implementation
- **Plan:** biggest economy on the ladder (1,040 pearls/game, peak 60 alive),
  splits until ~471, then feeds a king through self-collision deaths.
- **Strong:** round-limit maps (Schooltime 8-2, stronghold 8-1, Big Empty 7-1,
  king 46-62 long) and small-map eliminations (Default Small 6-0, Trophy 5-0).
  Only 8 own-team deaths per game.
- **Weak:** Devil 3-4 (three elimination losses) and Queen Of Spades 3-2. In its
  losses it is out-populated early (alive 9 vs 26 at round 100) and then
  eliminated. Loses the longer dragon in 41% of head-on trades.
- **Lost to:** dev test 1 :P, forgot to mention, SHINK AI, Sponge.

### 2. dev test 1 :P (2076, C++): same plan, the best eliminator
- **Plan:** the 龙虎豹 playbook (feeds via self-collision, 58% own-corpse).
- **Strong:** 23 elimination wins, 3 elimination losses: Queen 6-0, Trophy 6-1,
  Default 5-0 by elimination; Schooltime 9-1.
- **Weak:** round-limit games against other feeders are close (Big Empty 60 v 62;
  stronghold 48 v 48, lost on total length). Devil 3-3 (round-limit 0-2). Loses
  to lower-rated teams sometimes (Default twice to a ~1800 team, Devil to a
  1580). Its schedule was the weakest here (median opponent 1764).

### 3. SSS (2049, C++): early king, weak small-map defence
- **Plan:** stops splitting early (median round 319, almost no late splits),
  grows a king sooner, feeds via empty turns, heaviest portal use (104 steps).
- **Strong:** structured and large maps: Queen 7-0, Default 7-0, stronghold 4-0,
  Trauma 5-2.
- **Weak:** small maps, all by elimination: Default Small 1-6, Trophy 2-5,
  Devil 4-6. In losses it has 4 dragons to the opponent's 14 at round 50: an
  early swarm overwhelms it.

### 4. 𓎼𓃭𓅱𓂋𓇌 𓏏𓅱 𓂋𓄿 (2018, C++): fewer, bigger dragons
- **Plan:** smallest swarm (peak 35), more length 5-7 splits and some length-4
  children, a king already ~11 by round 400; the most sonar (~39k per game).
- **Strong:** Trophy 7-2, Devil 4-2; only 5 own-team deaths per game.
- **Weak:** round-limit losses on long maps: Trauma 2-6, Schooltime 2-5; loses
  Big Empty to larger swarms (54 v 69).

### 5. Sabotage-d (1962, Python): the only Python bot in the top 10
- **Plan:** standard feeder (68% own-corpse via self-collision); little sonar.
- **Strong:** Big Empty 7-2, Trophy 6-1, Schooltime 4-2.
- **Weak:** Devil 1-5, stronghold 3-5, Default Small 3-4; eliminated by SHINK
  and Sponge. Proof that Python can reach ~2000.

### 6. SHINK AI 6500 (2002, C++): portal-heavy, grinds opponents down
- **Plan:** heavy portal use (104 steps/game), king grown earlier (15 at r400),
  modest feeding (52%).
- **Strong:** Default 7-4, Trauma 4-2; wins keep ~31 alive vs ~1 for the opponent.
- **Weak:** 47 own-team deaths/game; Trophy 2-4 (eliminations), Schooltime 2-4.
  In losses it drops to 2 alive by round 400.

### 7. forgot to mention (1987, C++): recycling by suicide, map holes
- **Plan:** dragons die by empty turn throughout the game (~98/game), most on
  maps it wins (Devil ~159, Trauma ~244 per game), so this is deliberate
  recycling, not crashes. Largest kings in wins (56). Feeds 73%.
- **Strong:** Devil 8-0, Trauma 7-0, Trophy 4-0.
- **Weak:** catastrophic on Default 1-9 and Queen Of Spades 0-7 (collapses to 1
  alive by round 400; mostly against Yueci Li).

### 8. NeungzAI (1982, C++): swarm without a king
- **Plan:** economy and numbers (973 pearls, 19 elimination wins) but no feeding
  (king only 18 in wins) and ~102 own-team deaths per game, like our v2.
- **Strong:** Devil 7-2, Trophy 5-1, Queen 5-1, Schooltime 4-1.
- **Weak:** Default Small 3-6 (eliminations), stronghold 3-3, Trauma 1-2; in
  losses it collapses to 1 alive by round 300.

### 9. Check Raise (older sample, 22 Sep; ~1840 now)
- **Plan:** no sonar, few portals, no feeding; 78% of deaths are head-on.
- **Weak:** Trophy 1-7, Default Small 3-6, Default 3-6. Likely an old version.

### 10. Sponge (1993, C++): numbers, no sonar, little feeding
- **Plan:** wins by elimination (21-7): Default 9-1, Default Small 7-1.
- **Weak:** Devil 2-5 (eliminations), Trophy 4-5; loses round-limit games to
  feeders (Trophy 5 v 45, Schooltime 27 v 46 against 龙虎豹).

## Patterns worth acting on

1. **Feeding the king is the meta.** Seven of the top ten do it, and it produces
   30-60 length kings. Our v2 and v3 stop splitting at 450 and never feed, which
   matches our losses: round-limit games lost on longest dragon.
2. **Friendly-collision control:** 5-11 own-team deaths per game for the top four
   versus ~101 for us is the second clear gap.
3. **Feeders lose early, not late.** When 龙虎豹, SSS, SHINK and NeungzAI lose, the
   opponent already has 2-3 times their dragon count by round 100-200. A strong
   early swarm with good survival is how feeders are beaten; the non-feeders
   (Sponge, NeungzAI) win mainly by elimination.
4. **Devil is the shared weak map** (32x16, fast eliminations): 龙虎豹 3-4, SSS 4-6,
   Sabotage-d 1-5, Sponge 2-5, dev test 3-3. forgot to mention (8-0) and
   NeungzAI (7-2) handle it.
5. **Small maps are elimination maps** (Default Small, Trophy, Queen, Devil): an
   early-game population edge decides them; the king barely matters there.
6. **Close round-limit games reach the second tiebreak** (dev test v 龙虎豹
   stronghold: 48 v 48, decided on total length), so feeding should not throw
   away total length for no gain in the longest dragon.
7. **Portals and sonar are standard at the top;** sprint is not used by anyone.
8. **Unseen map in the ranked pool:** `INTERNAL_PRIVATE_TESTING_MAP` appears in
   Check Raise and Sponge games; it is not in `maps/` yet (extractable from
   those replays).

## Open questions (not answered by replays)

- What sonar carries (payloads are 0 in public replays).
- How a feeder is chosen and routed to the king (needs per-dragon position
  tracking around the king; the pearl-origin trace shows only that it happens).
- Whether the self-collision deaths are all deliberate (some are ordinary
  accidents; the late-game spike and the pearl flow to the king say most are).
