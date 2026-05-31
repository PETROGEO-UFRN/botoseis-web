# plotServer test fixtures

Large binary fixtures used by `plotServer/tests/`. Not committed to the repo
(`*.su` and `*.dat` are git-ignored).

## Expected files

| File | Source | Used by |
|---|---|---|
| `marmousi_4ms_stack.su` | `PETROGEO-UFRN/mock_large_files` (Git LFS) | `test_bandwidth_visualization.py`, `test_bandwidth_app.py` |

## How to populate locally

Either copy from an existing dev workspace:

```sh
cp ../../../server/app/tests/mock/files/marmousi_4ms_stack.su .
```

Or clone the fixtures repo and copy:

```sh
git clone https://github.com/PETROGEO-UFRN/mock_large_files.git /tmp/mock_large_files
cp /tmp/mock_large_files/marmousi_4ms_stack.su .
```

Tests that need this file will be **skipped** with a clear message when it is
missing, so the suite still runs cleanly without it.
