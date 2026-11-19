"""Marimo report: event-duration distribution from DVC features output."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return Path, mo, pd, plt


@app.cell
def _(Path, pd):
    root = Path(__file__).resolve().parents[1]
    events = pd.read_csv(root / "data/features/events.csv")
    return (events,)


@app.cell
def _(events, plt):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(events["duration_minutes"].dropna(), bins=20, edgecolor="black")
    ax.set_title("Distribution of event durations")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    fig.tight_layout()
    return (fig,)


@app.cell
def _(fig, mo):
    mo.mpl.interactive(fig)
    return


if __name__ == "__main__":
    app.run()
