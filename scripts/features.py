"""Create event duration and weekday features without changing row count."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transformed/events.csv"
DESTINATION = ROOT / "data/features/events.csv"


def main() -> None:
    df = pd.read_csv(SOURCE)
    df["duration_minutes"] = pd.to_numeric(df["duration_seconds"]) / 60
    df["weekday"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DESTINATION, index=False)
    print(f"features: {len(df)} rows -> {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
