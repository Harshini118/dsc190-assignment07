# Assignment 07 starter

This starter includes the three DVC stages (`clean`, `transform`, `features`) and a
Marimo report. It is **not yet a complete submission**, because your original
`data/raw/events.csv`, existing repository metadata, and public GitHub URL are
not accessible here. Do not overwrite a preexisting `dvc.yaml` without reviewing
it. Keep `data/raw/events.csv` committed to Git rather than using `dvc add`.

## Install

From the root of your existing repository (the folder containing
`data/raw/events.csv`), copy `scripts/`, `notebooks/`, `config/`, `dvc.yaml`, and
`setup_assignment07.sh` from this starter.

**Before running the pipeline**, inspect `config/valid_event_types.txt` and
update the accepted event names. The assignment excerpt never states the legal
values, and the sample entries are only a placeholder. The setup script prints
what actually appears in your CSV so you can verify them.

Run:

```bash
bash setup_assignment07.sh
```

The script will create the `uv` project if needed, add the dependencies, initialize
DVC if needed, run and validate the pipeline, and print Git commands. It will
not automatically commit or push changes.

To run the notebook, use:

```bash
uv run marimo edit notebooks/report.py
```

To rerun after changing raw data or code:

```bash
uv run dvc repro
```

After reviewing changes, commit and push to a **public** GitHub repository.
Create a file called `repo_url.txt` containing only the public repo URL, then
submit that file to Gradescope. `repo_url.txt` is the submission file, not the
project folder.
