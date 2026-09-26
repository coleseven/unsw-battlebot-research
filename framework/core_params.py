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
