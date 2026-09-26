# Portal addition to clean v3 + feeding + sonar

The current upload-ready additive bot does not intentionally enter portals.
This isolated addition wraps its decision with the previously tested
last-resort portal escape policy. It considers a portal only when there is
no known-empty ordinary step, rejects a visibly occupied exit, and preserves
splits, ordinary movement, and the existing direct enemy-head trade. Feeding,
sonar, and v3's split schedule are unchanged. Unknown portal exits remain
risky; this is emergency escape, not global portal navigation.

Predeclared screen: five official portal maps (Colosseum, Default, Queen of
Spades, Schooltime, Trophy), two new bot seeds (44004-44005), both sides.
The unchanged additive bot and additive+portal bot each face frozen v3:
40 matched games total. One synthetic portal-dense map tests mechanism
through two direct additive+portal versus additive games, kept separate from
the official comparison. Everything runs in one in-process worker with
frozen bot/map/source hashes and saved replays. A replay audit must verify
that portal moves actually occur. A nonnegative paired official score is
only a screen, not a promotion guarantee. No live bot, frozen version or
website submission is changed by this experiment.

## Emergency-portal result

Frozen run: `results/20260924-180920-v4-additive-portal-ed6674/`.
All 42 games completed without errors. Against v3 on the official portal
maps, unchanged additive went 10-10 while additive+emergency-portals went
8-12. The paired difference was -10 percentage points (five-map clustered
interval -40 to +20 points), failing the predeclared nonnegative screen.
The synthetic portal-dense direct pairing split 1-1. The emergency wrapper
must **not** replace the current additive upload candidate.

Replay audit counted 160 portal entries by the new bot on official maps.
Every one had an exit outside the current 7x7 view, and 62 entrants died
in the same round. The portal-dense stress map had 124 entries, all into
visibly empty exits. These are associations, not a counterfactual proof of
why two net games were lost, but they give a concrete safety hypothesis:
test a separate visible-empty-exit-only rule. It will not inherit this
failed policy's promotion status or results.
