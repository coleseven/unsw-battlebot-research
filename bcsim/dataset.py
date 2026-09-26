"""Public V2 dataset API and CLI. Legacy files in data/dataset are preserved.

See DATASET_V2.md. The implementation lives in dataset_v2 so spawned workers
have a stable importable module when this entry point runs via python -m.
"""
from .dataset_v2 import (
    SCHEMA_VERSION, OUT, REPLAYS, FIXED_COLUMNS, DatasetError,
    build_game, iter_batches, load_all, make_partitions, pipeline_hash,
    read_metadata, save_partitions, shards, main,
)

if __name__ == "__main__":
    main()
