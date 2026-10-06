# PR8 saved-trajectory sequence audit

The current parser and sequence matcher were applied to all 335 saved PR8 r2 smoke trajectories without model generation. **Both the full measurement checks and the registered cached paired screen still fail. Do not restart formal generation on the strength of unit tests.**

See [REPORT.zh-CN.md](REPORT.zh-CN.md) for fixes, assumptions, numerical results, and remaining work. [measurement_report.json](measurement_report.json) is the unmodified offline output, with input and measurement-source hashes, per-problem/per-op results, and 24 full plus eight cached-screen trajectory rows. [validation.json](validation.json) records code verification and evidence checks; [checksums.sha256](checksums.sha256) covers these files.

The source is the immutable server prepare directory `/mnt/mydata/wja/reasoning-diff/runs/pr8-12h-20261006-r2/smoke/prepare`, read through a local copy. Raw trajectories, token arrays, weights, features, and caches are excluded. Previous evidence packages remain unchanged. The new matching policy assumes order preservation; mathematical uniqueness within that model is not an independent semantic correspondence audit.
