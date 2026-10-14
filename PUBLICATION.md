# Public research archive — 14 October 2026

Repository: [coleseven/unsw-battlebot-research](https://github.com/coleseven/unsw-battlebot-research).

The completed [project writeup](PROJECT_WRITEUP.md), [audited history](PROJECT_HISTORY.md), source, frozen versions, experiments, reports, outcome tables, and original submission ZIPs are in Git. Original development history is preserved. The publication commit is made on a separate branch; the working development branch and its index are left intact.

Large replay files, dataset shards, and research bundles are distributed as independently extractable ZIP assets on the [research archive release](https://github.com/coleseven/unsw-battlebot-research/releases/tag/archive-2026-10-14). They preserve paths relative to the repository root. A regular clone contains the reports and manifests; download the release assets to restore the bulky evidence.

## Restore the full evidence corpus

1. Clone the repository.
2. Download `research-data-*.zip` from the release. Each ZIP is independent; they are not fragments requiring concatenation.
3. Compare each downloaded file's SHA-256 and byte size with [ARCHIVES.json](docs/publication/ARCHIVES.json).
4. Extract the ZIPs into the repository root, preserving relative paths.
5. [FILE_MANIFEST.jsonl](docs/publication/FILE_MANIFEST.jsonl) records the original path, byte size, SHA-256, and storage location of each payload file. [SUMMARY.json](docs/publication/SUMMARY.json) gives counts and sizes. Manifest/index files are authenticated by the Git commit rather than recursively hashing themselves.

The ZIPs use ordinary deflate compression. Dependencies and compiler caches must be installed or rebuilt separately. Existing scripts may contain the original machine's absolute paths; consult each frozen plan before reproducing experiments. No bot tests or matches were rerun for publication.

GitHub permits release assets under 2 GiB each; these archives are grouped below that limit. See [GitHub's release documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

## Deliberate exclusions

- Credentials, local account configuration, `.git` internals, virtual environments, installed engine/dependency packages, compiler outputs and caches are not research payloads.
- External opponent sources marked local-only or lacking redistribution permission are excluded, including copies inside experiment snapshots. [EXTERNAL_SOURCES.json](docs/publication/EXTERNAL_SOURCES.json) retains their repository/commit provenance and exclusion paths. Match results and replay evidence outside those source directories remain included.
- The existing private repository is not made public or overwritten. This is a new public research repository.

The review scanned 1,122 reachable Git blobs and 26,175 current text files for high-signal credential patterns, with no matches. This is a bounded signature scan, not a guarantee. No exact copies of the audited restricted opponent sources were found in reachable Git history. See [AUDIT_SUMMARY.json](docs/publication/AUDIT_SUMMARY.json) and [third-party notices](THIRD_PARTY_NOTICES.md).

Historical archives and original result files retain their original wording, including rejected conclusions and stale paths. The completed writeup and later history chapter explain corrections. Publication is preservation of work and evidence, not an assertion that every saved run completed or that every proposed idea succeeded.
