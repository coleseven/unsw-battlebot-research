"""Deterministic, harness-only approximation of v6's judge CPU clock.

The sandbox profile on Big Empty found a median of 77 search expansions per
moving turn and soft-cutoff events on 16,940 of 19,461 moving turns. Local
host wall time is therefore not a usable match budget. This clock charges a
fixed setup amount, a fixed amount per v3 feature row, and a fixed amount per
search-loop clock call. It changes only in-process evaluation, never a judge
bot's files or the actual sandbox clock.
"""

SETUP_SECONDS = 0.009
FEATURE_ROW_SECONDS = 0.0015
SEARCH_TICK_SECONDS = 0.00042


class WorkClock:
    def __init__(self):
        self.start_turn()

    def start_turn(self):
        self.value = 0.0
        self.calls = 0

    def perf_counter(self):
        self.calls += 1
        if self.calls == 1:  # Brain.turn's start timestamp
            return 0.0
        self.value += (SETUP_SECONDS if self.calls == 2
                       else SEARCH_TICK_SECONDS)
        return self.value

    def charge_features(self, count):
        self.value += FEATURE_ROW_SECONDS * count


def install(brain):
    """Patch only this isolated in-process dragon's imported module objects."""
    scope = brain.turn.__func__.__globals__
    search = scope["core_search"]
    values = scope["action_value"]
    clock = WorkClock()
    original_features = values.features

    def features(obs, team, directions=None):
        result = original_features(obs, team, directions)
        clock.charge_features(len(result[1]))
        return result

    scope["time"] = clock
    search.time = clock
    values.features = features
    brain._bcsim_clock = clock
    return brain
