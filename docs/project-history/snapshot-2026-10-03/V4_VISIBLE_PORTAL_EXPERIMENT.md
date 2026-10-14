# Visible-exit portal follow-up

The first emergency-portal addition lost 10 paired percentage points on
official maps. All 160 official portal entries had exits outside the current
view, whereas all 124 stress-map entries had visibly empty exits. This new
fixed policy takes a portal override only when the paired exit is visible
and empty. It otherwise leaves the original additive decision intact;
feeding, sonar, and v3's split policy are unchanged. It may still retain
the additive bot's forced fallback into a portal, because that is not a new
override.

Predeclared: the same five official portal maps, new seed 44006, both sides.
Visible-portal and unchanged additive each play v3 in ten matched games
(20 total). A separate synthetic portal-dense map gets two direct games
against additive for mechanism stress. All run one worker with bot/map/source
hashes and saved replays. Check replay portal entries and require a
nonnegative official paired score and no errors before considering further
validation. A passing small screen would not prove improved ladder play;
judge-sandbox and broader-map tests would still be needed. No automatic
upload or change to the existing zip.

## Screen and runtime result

Frozen run: `results/20260924-182411-v4-visible-portal-ada92a/`.
All 22 games completed without errors. On five official portal maps at
seed 44006, visible-portal and unchanged additive each went 5-5 against
v3. Their ten paired official action traces were **identical**, so this
particular official screen shows no portal benefit or cost. The synthetic
portal-dense direct pairing split 1-1. The visible-portal bot made 124
portal moves there (54 as side A, 70 as side B), all into visibly empty
exits. These counts confirm the feature is real, but only on the stress map
in this sample.

A complete judge-sandbox game on the same stress map ended with the
visible-portal bot eliminating additive. It made 54 visible-empty portal
moves, with zero recorded runtime errors; among 4,488 metered turns, maximum
use was 56,318,273 CPU points (p99 40,161,357), below the 100M limit.
One sandbox win is a compatibility check, not strength evidence. The
visible-only addition remains experimental pending a matched v2 regression
and broader opponent/map evidence; the current additive upload zip is
unchanged.

Predeclared v2 regression: same five official portal maps, new seed 44007,
both sides, ten games of frozen visible-portal directly against frozen v2,
one worker. This tests whether the candidate remains a plausible practical
replacement for the currently uploaded v2; it does not isolate the portal
contribution or prove an advantage over unchanged additive.

The frozen visible-portal v2 regression at
`results/20260924-183910-v4-visible-portal-v2-fb319a/` went 7-3 with no
errors. A post-screen unchanged-additive control on the exact same ten
map/seed/side matchups at `results/20260924-184143-v4-portal-control-e3989f/`
also went 7-3; **all ten paired action traces were identical**. This
establishes that the portal rule neither helped nor hurt on those v2 games.
The control was diagnostic and not part of the original selection plan.

Decision: visible-only portal support is implemented and runtime-tested,
but no official-map benefit has been observed. It is an experimental
capability, not a reason to replace the current additive upload zip.
Earlier terrain/portal-memory routing also failed its held-out v2 gate
(`NAVIGATION_EXPERIMENT.md`), so broader deliberate portal navigation
needs a genuinely new hypothesis rather than silently merging that code.
