"""Add the ISO calendar date to cleaned event records."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/clean/events.csv"
DESTINATION = ROOT / "data/transformed/events.csv"


def main() -> None:
    df = pd.read_csv(SOURCE)
    df["date"] = df["timestamp"].str[:10]
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DESTINATION, index=False)
    print(f"transform: {len(df)} rows -> {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
