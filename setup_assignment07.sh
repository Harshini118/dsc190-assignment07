#!/usr/bin/env bash
set -euo pipefail

# Run from the root of your existing GitHub repository after copying the
# scripts/, notebooks/, config/, and dvc.yaml files from this starter.
if [[ ! -f data/raw/events.csv ]]; then
  echo "ERROR: Can't find data/raw/events.csv. Run in the correct repo root." >&2
  exit 1
fi
if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: uv is not installed. See https://docs.astral.sh/uv/" >&2
  exit 1
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init
fi
if [[ ! -f pyproject.toml ]]; then
  uv init --bare
fi
uv add dvc marimo pandas matplotlib python-dateutil
if [[ ! -d .dvc ]]; then
  uv run dvc init
fi

echo
echo "Event types found in raw input (check config/valid_event_types.txt):"
uv run python - <<'PY'
from pathlib import Path
import pandas as pd
path = Path('data/raw/events.csv')
frame = pd.read_csv(path, dtype='string')
if 'event_type' not in frame.columns:
    raise SystemExit('raw input missing event_type column')
print(frame['event_type'].value_counts(dropna=False).to_string())
PY

echo
echo "Edit config/valid_event_types.txt to match allowed event types before grading."
uv run dvc repro
uv run python - <<'PY'
import pandas as pd
from pathlib import Path
root = Path('data')
clean = pd.read_csv(root / 'clean/events.csv')
transformed = pd.read_csv(root / 'transformed/events.csv')
features = pd.read_csv(root / 'features/events.csv')
expected = ['user_id', 'timestamp', 'event_type', 'duration_seconds', 'date', 'duration_minutes', 'weekday']
assert list(features.columns) == expected, features.columns
assert len(features) == len(transformed), (len(features), len(transformed))
assert all(features['duration_minutes'] == features['duration_seconds'] / 60)
print(f'SUCCESS: {len(clean)} cleaned events, {len(features)} feature rows')
PY

echo
echo "Review outputs, then run:"
echo "  git add pyproject.toml uv.lock .dvc dvc.yaml dvc.lock scripts/ notebooks/ config/ data/raw/events.csv data/"
echo '  git commit -m "Add reproducible DVC pipeline and Marimo report"'
echo "  git push"
echo "Submit a repo_url.txt containing only your public GitHub repository URL."
