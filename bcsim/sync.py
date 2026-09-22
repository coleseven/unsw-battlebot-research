"""Copy the shared framework into every live framework bot.

    python -m bcsim.sync        # mybot/ and opponents/*/ (never versions/)

A bot directory is a framework bot if it has a brain.py. Every bot gets
bc.py and tactics.py; any other framework module (e.g. features.py) is
refreshed only in bots that already carry a copy. Bots that have diverged
can keep their own tactics.py by listing the bot in KEEP_TACTICS.
Frozen snapshots in versions/ are deliberately left alone.
"""

from __future__ import annotations

import pathlib
import shutil

from .paths import FRAMEWORK, ROOT, sync_targets

ALWAYS = ("bc.py", "tactics.py")
KEEP_TACTICS: set[str] = set()


def sync(root: pathlib.Path = ROOT, framework: pathlib.Path = FRAMEWORK,
         keep_tactics: set[str] = KEEP_TACTICS) -> list[pathlib.Path]:
    """Returns the bot directories that were updated."""
    modules = sorted(p.name for p in framework.glob("*.py"))
    done = []
    for bot in sync_targets(root):
        for name in modules:
            if name == "tactics.py" and bot.name in keep_tactics:
                continue
            if name in ALWAYS or (bot / name).is_file():
                shutil.copy2(framework / name, bot / name)
        done.append(bot)
    return done


def main() -> None:
    for bot in sync():
        print(f"synced {bot}")


if __name__ == "__main__":
    main()
