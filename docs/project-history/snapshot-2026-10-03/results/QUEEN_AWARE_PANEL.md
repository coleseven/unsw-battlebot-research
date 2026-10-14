# Queen-aware opponent panel (3 Oct)

Specialists built from our own controller (one shared lineage, not independent
strategies), to stop local tests underpricing queen survival:

- opp-careful-queen: v11q behaviour (light queen + 3-step escape search), small careful queen.
- opp-raider: v11q + CPP_QUEEN_HUNT (bonus 600, pull 400): workers chase and trade into enemy queens.
- opp-growth-queen: v11q + queen food x3 + keep length 6: big queen.
- opp-economy: v11ms (multistep, no queen protection): strong economy, careless queen.

Report results against this family separately from the old nicked-family panel.
