"""Big-board split brake: preserve growth instead of filling the 64-unit cap."""

import action_value


def choose(init, obs, team, model, original):
    if not original.startswith("SPLIT ") or init.width * init.height < 2000:
        return original
    # The existing v3 rule remains the eligibility and legality gate. This
    # ablation only suppresses ordinary splitting when the team is already
    # numerous, or after round 300 unless population has fallen below 24.
    if obs.unit_count >= 48 or (obs.round >= 300 and obs.unit_count >= 24):
        return action_value.choose(obs, team, model)
    return original
