"""Copy the shared framework into every framework bot.

    python -m bcsim.sync            # bc.py + tactics.py into mybot/, opponents/*/

A bot directory is a framework bot if it has a brain.py. Bots that have
diverged can keep their own tactics.py by listing the bot in KEEP_TACTICS.
"""

from __future__ import annotations

import shutil

from .paths import FRAMEWORK, bot_dirs

KEEP_TACTICS: set[str] = set()


def main() -> None:
    for bot in bot_dirs():
        if not (bot / "brain.py").is_file():
            continue
        shutil.copy2(FRAMEWORK / "bc.py", bot / "bc.py")
        if bot.name not in KEEP_TACTICS:
            shutil.copy2(FRAMEWORK / "tactics.py", bot / "tactics.py")
        print(f"synced {bot}")


if __name__ == "__main__":
    main()
