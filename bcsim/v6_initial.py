"""Freeze a v6 search-core bot snapshot from local source-of-truth modules."""

import shutil
from pathlib import Path

from . import population
from .paths import ROOT


MODULES = (
    ("experiments/v6/brain.py", "brain.py"),
    ("framework/navigation.py", "navigation.py"),
    ("framework/core_memory.py", "core_memory.py"),
    ("framework/core_search.py", "core_search.py"),
    ("framework/core_split.py", "core_split.py"),
    ("framework/core_king.py", "core_king.py"),
    ("framework/core_params.py", "core_params.py"),
    ("framework/v6_portal_book.py", "v6_portal_book.py"),
    ("framework/v6_hub_book.py", "v6_hub_book.py"),
    ("framework/v4_sonar.py", "v4_sonar.py"),
)


def variant(dest: Path, params: Path | None = None):
    population.snapshot(ROOT / "versions/v3", dest)
    for source, target in MODULES:
        shutil.copy2(ROOT / source, dest / target)
    if params is not None:
        shutil.copy2(params, dest / "core_params.py")
    return dest
