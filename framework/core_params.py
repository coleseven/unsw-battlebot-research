"""Hand-default v6 parameters. Tuning snapshots replace this file only."""

N_SEARCH = 200
DEPTH_MAX = 16
W_PEARL = 80.0
W_MEM_PEARL = 20.0
W_SPAWN = 30.0
H_SPAWN = 40
W_UNSEEN = 8.0
W_STALE = 3.0
STALE_ROUNDS = 30
SPACE_MULT = 2.0
SPACE_MARGIN = 8.0
SPACE_CAP = 100
ENDGAME_SPACE_MULT = 2.0
W_TRAP = 10.0
W_LETHAL = 100.0
W_DEADEND = 60.0
W_CORRIDOR = 8.0
W_HEAD_ENEMY = 60.0
W_HEAD_TEAM = 60.0
W_AHEAD = 20.0
W_REVISIT = 3.0
REVISIT_ROUNDS = 20
W_FAN_EARLY = 8.0
W_FAN_LATE = 1.5
FAN_ROUNDS = 30
W_STRAIGHT = 0.5
W_PORTAL = 8.0
W_PORTAL_UNSEEN = 60.0
PORTAL_STALE = 3
W_PORTAL_SCOUT = 40.0
PORTAL_BOOK = True
SCOUT_ROUNDS = 100
W_V3 = 10.0
SPLIT_AT = 4
CHILD = 2
CAP = 56
FLOOR = 24
FLOOR_UNTIL = 400
SPLIT_UNTIL_SMALL = 450
SPLIT_UNTIL_LARGE = 300
AREA_SPLIT = 1000
FOUNDER_PROTECT_ROUND = 250
PROTECT_ROUND = 80
PROTECT_LEN = 5
PROTECT_MULT = 1.5
PROTECT_FOOD_MULT = 2.0
FEED_ROUND = 410
FEED_MAXLEN = 5
FEED_KING_MIN = 6
W_CASH = 80.0
FEED_DMIN = 2
FEED_DMAX = 4
FEED_ENEMY_CHECK = True
SONAR = True
PEARL_TTL = 8
OCC_TTL = 2
SOFT_S = 0.045
HARD_S = 0.065
# Matching mode for the C++ port (V7): turn off the wall-clock cutoffs so the
# search is host-independent. Each move then expands until its queue empties or
# it hits the N_SEARCH cap, and the HARD_S v3 fallback never fires. Release play
# keeps PARITY = False and the time budget.
PARITY = False
# Aggression: trade short dragons into longer enemy heads; keep long ones clear
ATTACK_MAXLEN = 4
ATTACK_MIN_GAIN = 1
W_ATTACK = 150.0
W_TRADE = 10.0
HUNT_MAXLEN = 4
HUNT_MIN_GAIN = 2
HUNT_ROUND = 0
W_HUNT = 40.0
DEFEND_LEN = 6
W_DEFEND = 15.0
# Pearl hubs from the official-map hub book (only once the map is identified)
HUB_BOOK = True
W_HUB = 60.0
HUB_SCALE = 4.0
HUB_FAR_MULT = 0.5
# Learned hubs when no book map fits (new or changed maps)
LEARN_HUBS = True
LEARN_EVERY = 10
# Exploration goal: a stale/unseen SECTOR x SECTOR block, pursued along search paths
GOAL = True
SECTOR = 8
GOAL_EVERY = 12
GOAL_STALE_CAP = 150
GOAL_DIST_W = 1.0
GOAL_NOISE = 20.0
W_GOAL = 3.0
GOAL_STEP_COST = 0.5
POOR_RATE = 0.01       # mean 1/(1 + max countdown) of tiles in view below this = poor area
POOR_MULT = 2.5
KING_GOAL_MULT = 0.3

# --- C++ port only (V7 section 5); the Python core ignores these ------------
# Every switch defaults to today's behaviour, so parity stays 100% with them
# off. Ints so bcsim.tune can rewrite them; booleans are 0/1.
CPP_BUDGET = 0          # C++ only: 1 = points meter + fair split; 0 = fixed N_SEARCH
CPP_SOFT_POINTS = 60000000  # C++ only: stop expanding past this many points/turn
CPP_HARD_POINTS = 80000000  # C++ only: past this, take a cheap safe move
CPP_PATH_DIST = 0       # C++ only: 1 = portal-aware head-BFS path distances for pulls
CPP_BEAM = 0            # C++ only: 1 = lookahead beam over our own moves
CPP_BEAM_WIDTH = 8      # C++ only: beam width
CPP_BEAM_DEPTH = 6      # C++ only: beam depth
# Portal scouting by the dragon's own age (27 Sep: stalls on portal maps)
CPP_PORTAL_AGE = 0      # C++ only: 1 = scout bonus / unseen-exit penalty by dragon age, not game round
CPP_PORTAL_RAMP = 150   # C++ only: rounds over which the unseen-exit penalty ramps in after SCOUT_ROUNDS of age
CPP_PORTAL_SPREAD = 0.0  # C++ only: penalty for entering a portal with a teammate head within 2 tiles
# Trap weight by local tightness
CPP_TRAP_OPEN = 1.0     # C++ only: W_TRAP/W_LETHAL multiplier in open terrain (1 = today; scales to 1 as view kelp rises)
CPP_TRAP_KELP_REF = 0.25  # C++ only: kelp share of the view's edges that counts as fully tight
# Voronoi-lite pearl targeting (nicked lab: 27/40 with a BFS version)
CPP_VOR = 0             # C++ only: 1 = scale pearl values by who reaches them first
CPP_VOR_LOST = 0.5      # C++ only: a visible enemy head reaches the pearl first
CPP_VOR_CONTEST = 1.5   # C++ only: an enemy head reaches it within 2 moves after us (take it now)
CPP_VOR_MATE = 0.6      # C++ only: a teammate head is closer (leave it to them)
# Hub sharing by sonar: a split child starts with no memory, so it never learns a hub it
# has not seen (Prisoners Dilemma: 8 pearls eaten vs nicked's 59 in rounds 0-100)
CPP_SONAR_HUB = 0       # C++ only: 1 = dragons that know a hub send it; ones that know none adopt it
CPP_SONAR_HUB_MIN = 0.0  # C++ only: share a learned hub only if its 5x5 respawn-rate sum is at least this (0 = always)
CPP_SONAR_ADOPT_AGE = 0  # C++ only: a dragon adopts a shared hub only after this many rounds alive without one
CPP_SONAR_EVERY = 5     # C++ only: send the best known hub every this many rounds (all 4 directions)
# King beacon + big-dragon feeding (28 Sep ladder: losses on the longest-dragon tiebreak with
# more total length; long non-kings never feed, only length <= FEED_MAXLEN dragons that see the king)
CPP_KING_BEACON = 0     # C++ only: 1 = dragons broadcast/relay the longest known king over sonar
CPP_KB_ROUND = 300      # C++ only: first round of king beacons
CPP_KB_MINLEN = 8       # C++ only: shortest dragon that claims king
CPP_KB_TTL = 8          # C++ only: rounds a heard king beacon stays valid
CPP_BIG_FEED = 0        # C++ only: 1 = dragons of any length feed a king at least MARGIN longer
CPP_BIG_FEED_ROUND = 430  # C++ only: first round big dragons feed
CPP_BIG_FEED_MARGIN = 4  # C++ only: the king must be this much longer than the feeder
# Dead-end corridors (kelp deaths: 43/game vs 26 for opponents; a length >= 2 dragon cannot reverse)
CPP_DEADEND_LOOK = 0    # C++ only: walk this many corridor steps ahead (0 = off)
CPP_DEADEND_PEN = 400.0  # C++ only: penalty for a move into a known dead-end corridor
CPP_SPLIT_SAFE = 0      # C++ only: 1 = do not split when the child would be born facing into a known dead end
CPP_SPLIT_SAFE_LOOK = 12  # C++ only: corridor steps checked from the child's birth cell
CPP_SPLIT_ROOM = 0      # C++ only: with CPP_SPLIT_SAFE, split only if the child's birth cell reaches this many free tiles
CPP_BRIEF = 0           # C++ only: 1 = at a split the parent sonars the child a dead-end mask (read on the child's first turn)
CPP_BRIEF_PEN = 200.0   # C++ only: first-turn penalty for a direction the parent flagged as a dead end
CPP_HUB_OBSERVE = 0     # C++ only: 1 = on a hub-book map, replace the book hubs with learned ones once any are observed
CPP_ANCHOR = 0          # C++ only: 1 = founders never split from FOUNDER_PROTECT_ROUND (grow early kings)
CPP_ANCHOR_RESCUE = 12  # C++ only: ...unless the team has fewer dragons than this
CPP_HUB_GRAD = 0.0      # C++ only: points per step closer to the best known hub (0 = off)
CPP_HUB_GRAD_UNTIL = 500  # C++ only: apply the hub gradient before this round
CPP_BOOK_MAP = 0        # C++ only: 1 = fill the identified book map's open edges (paths known from turn one)
# King growth (nicked's kings are ~11 long at round 300, ours ~4: our protected long dragons keep
# splitting until the team has FLOOR units, theirs stop at a quarter of the cap)
CPP_PROTECT_FLOOR = -1  # C++ only: protected dragons stop splitting at this many units (-1 = FLOOR)
CPP_RESCUE_EVERY = 0    # C++ only: below that floor a protected dragon splits at most once per this many rounds (0 = no limit)
CPP_FEED_SHIFT_LARGE = 0  # C++ only: on large maps (area >= AREA_SPLIT) feeding and king beacons start this many rounds earlier
# Defects found in review (30 Sep): learned-hub spacing used max instead of min of the wrapped
# distances; v3 scores portal moves by the cells beside the head instead of the far end
CPP_HUB_SEP_FIX = 0     # C++ only: 1 = learned hubs use the true wrapped distance for their 5-cell spacing
CPP_V3_PORTAL = 0       # C++ only: 1 = portal moves get the mean v3 score of the ordinary moves
CPP_FEED_REACH = 0      # C++ only: feed only if the king can walk to our body (the drops) within this many steps in view (0 = off)
CPP_KING_GRAD = 0.0     # C++ only: points per step closer (walking distance) to the feeding target (0 = off)
CPP_V3_R4 = 0           # C++ only: 1 = move ranker weights refit on nicked v92's moves (model.hpp WEIGHT_R4)
# R5 mover (NEW_MOVER_PLAN.md): residual on the complete move score, weights in mover.hpp
CPP_MOVER = 0           # C++ only: 1 = apply the R5 residual (zero weights = incumbent exactly)
CPP_MOVER_LAMBDA = 1.0  # C++ only: residual strength
CPP_MOVER_TAU = 0.0     # C++ only: override the incumbent's move only if q gains more than this
CPP_MOVER_LOG = 0       # C++ only: log the 64 mover features of every N-th eligible decision (0 = off)
CPP_KB_V2 = 0           # C++ only: 1 = king beacon carries a king token and origin age (relays keep it); feeders bind to the token
CPP_MULTISTEP = 0       # Q2 (queen rules): spend extra free steps (ceil(len/4) - 1) reaching a visible pearl
CPP_MULTISTEP_QUEEN = 0  # Q2: with CPP_QUEEN, let the queen take extra steps too (default: workers only)
CPP_MULTISTEP_TRAVEL = 0  # Q2b: with no reachable pearl, spend extra free steps travelling toward the best hub
CPP_QUEEN_LIGHT = 0     # Q4: minimal queen rules: the queen never feeds; workers keep CPP_QUEEN_GUARD_* clear of it
CPP_QUEEN_LIGHT_SPLIT_UNTIL = 1000  # light queen: the queen stops splitting from this round (1000 = never)
CPP_QUEEN_LIGHT_FEED = 0  # small late feeders target our visible queen by id (queen-mode feeding branch)
CPP_QUEEN_LIGHT_FOOD = 1.0  # light queen: multiplier on the queen's food term
CPP_QUEEN_LIGHT_KEEP = 0  # light queen: split only if the queen keeps at least this length (0 = off)
CPP_QUEEN_LIGHT_SAFE = 1.0  # light queen: multiplier on its trap/lethal (room) penalties
CPP_QUEEN_FLIGHT = 0    # queen: when threatened, spend extra free steps maximising distance from threat heads
CPP_QUEEN_HUNT = 0      # workers (<= ATTACK_MAXLEN) attack the enemy queen head at any length difference
CPP_QUEEN_HUNT_BONUS = 300.0  # added to W_ATTACK for a head-on into the enemy queen
CPP_QUEEN_HUNT_PULL = 150.0   # pull toward a visible enemy queen head: PULL / (1 + distance)
CPP_QUEEN_TACTICS2 = 0  # corrected queen escape search (food keeps the tail, path-aware threat reach, unknown exits separate, line counts); queen takes no extra pearl steps unless CPP_MULTISTEP_QUEEN
CPP_QUEEN_YIELD = 0     # workers avoid taking our visible queen's free exit cells
CPP_QUEEN_YIELD_PEN = 150.0  # base penalty (x3 if the queen has one exit, x1.5 if two)
CPP_QUEEN_REFUGE = 0    # crowded light queen is pulled toward open, uncrowded cells
CPP_QUEEN_REFUGE_W = 100.0  # points per 10 openness units relative to the best move
CPP_QUEEN_SPLIT_EXITS = 0  # light queen splits only with >= this many free open exits (0 = off)
CPP_QUEEN_SPRINT = 0  # corrected search: threats may also sprint up to this many paid steps once (each costs a segment; 0 = off)
CPP_DOOMED_SPARE_QUEEN = 0  # a trapped worker never spends its last move on our queen's head (rams an enemy head if it can)
CPP_QUEEN_BODYGUARD = 0  # workers trade head-on with enemy heads within this many cells of our queen's head (0 = off)
CPP_QUEEN_BODYGUARD_BONUS = 200.0  # added to W_ATTACK for such a trade
CPP_GOAL_PATH = 0  # exploration-goal progress by path distance over remembered terrain (unknown edges open) instead of straight line
CPP_HUB_PATH = 0  # hub area = cells within this walking distance of the hub over remembered terrain (0 = the 5x5 square)
CPP_QUEEN_FULL_CAP = 4  # corrected search: full-depth escape lines count up to this many (4 = v11t)
CPP_QUEEN_DEBUG = 0  # debug only: log the queen's corrected-search options each turn (LOG QT lines)
CPP_QUEEN_PORTAL_TRUST = 0  # corrected search never overrides a queen move through a portal (the in-view search cannot follow portals)
CPP_FEED_TRAVEL = 0.0  # small workers start feeding this many rounds earlier per cell of distance to the beaconed king (0 = off)
CPP_FEED_TRAVEL_CAP = 60  # at most this many rounds earlier
CPP_QUEEN_CALM_CAP = 0  # corrected search: full-line cap used when no enemy head is in view (0 = always CPP_QUEEN_FULL_CAP)
CPP_QUEEN_EARLY = 0  # before this round the queen moves like a worker (no corrected-search override, extra pearl steps allowed)
CPP_SEARCH_UNKNOWN = 0  # move search expands through unknown edges (assumed open), so unexplored areas carry exploration value
CPP_QUEEN_EARLY_AREA_MAX = 0  # CPP_QUEEN_EARLY applies only on maps of at most this many cells (0 = all maps)
CPP_MOVE_DEBUG = 0  # debug only: log each candidate move's score terms (LOG MD lines)
CPP_EXPLORE_MULT = 1.0  # goal-progress multiplier for a move whose search finds no food and no hub (1 = off)
CPP_QUEEN_HUNT_SPRINT = 0  # opponent model: a worker rams a visible enemy queen head using up to this many paid (sprint) steps (0 = off)
CPP_QUEEN_SPRINT_MAXLEN = 0  # CPP_QUEEN_SPRINT applies only to enemy heads of at most this visible length (0 = all)
CPP_QUEEN_PAID_FLIGHT = 0  # queen (length >= 3) pays one segment for a 2-step escape when a small enemy can sprint-reach its chosen cell
CPP_QUEEN_TACTICS = 0   # Q4: exact short escape search for our queen (id 0/1), any mode
CPP_QUEEN_TACTICS_DEPTH = 3  # Q4: look-ahead steps (view radius is 3)
CPP_QUEEN_TACTICS_MARGIN = 0  # Q4: extra steps per turn assumed for threat heads
CPP_QUEEN_TACTICS_FRIENDS = 1  # Q4: our own workers' heads count as threats
CPP_QUEEN = 0           # Q1: fixed-ID queen policy; historical behavior remains the default
CPP_QUEEN_SPLIT_UNTIL = 80
CPP_QUEEN_FLOOR = 4     # queen supplies the opening economy only below this population
CPP_QUEEN_KEEP = 5      # retain at least two free steps after an opening split
CPP_QUEEN_SAFE_MULT = 1.5  # queen's trap/lethal/head safety multiplier (1.5 = PROTECT_MULT, unchanged)
CPP_QUEEN_REACH_PEN = 0.0  # queen: penalty per enemy head that can reach the cell with ceil(len/4) steps
CPP_QUEEN_DEADEND = 0      # queen: dead-end corridor look-ahead (0 = off)
CPP_QUEEN_DEADEND_PEN = 400.0
CPP_QUEEN_GUARD_PEN = 0.0  # workers: penalty for moving next to our queen's head
CPP_QUEEN_KB = 0           # 1 = keep the king beacon / big-dragon feeding in queen mode
CPP_QUEEN_REACH_EXTRA = 0  # queen: extra cells of margin beyond an enemy head's ceil(len/4) reach
CPP_QUEEN_GUARD_R = 1      # workers: guard radius around our queen's head
