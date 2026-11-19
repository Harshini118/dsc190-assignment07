"""Validate raw event records and write normalized, clean events."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from dateutil.parser import ParserError, parse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/raw/events.csv"
DESTINATION = ROOT / "data/clean/events.csv"
EVENT_TYPES = ROOT / "config/valid_event_types.txt"
REQUIRED = ["user_id", "timestamp", "event_type", "duration_seconds"]


def normalize_timestamp(value: str) -> str | None:
    """Parse common timestamp representations into local/UTC ISO-like seconds."""
    try:
        parsed = parse(value)
        # Avoid silently discarding a timezone offset. UTC normalization keeps
        # instant ordering consistent, while the required output has no suffix.
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed.strftime("%Y-%m-%dT%H:%M:%S")
    except (ParserError, OverflowError, ValueError, TypeError):
        return None


def main() -> None:
    allowed = {
        item.strip()
        for item in EVENT_TYPES.read_text(encoding="utf-8").splitlines()
        if item.strip() and not item.lstrip().startswith("#")
    }
    if not allowed:
        raise ValueError(f"No valid event types configured in {EVENT_TYPES}")

    df = pd.read_csv(SOURCE, dtype=str, encoding="utf-8-sig")
    missing_columns = sorted(set(REQUIRED) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.loc[:, REQUIRED].copy()
    for column in REQUIRED:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace("", pd.NA)
    df = df.dropna(subset=REQUIRED).copy()
    df = df.loc[df["event_type"].isin(allowed)].copy()

    # Data arriving as 45.0 is serialized as 45, never 45.0.
    numeric_durations = pd.to_numeric(df["duration_seconds"], errors="coerce")
    valid_durations = numeric_durations.notna() & (numeric_durations > 0)
    # Seconds are stored as integer counts; reject fractional values rather
    # than silently rounding/truncating events in the raw data.
    valid_durations &= numeric_durations.mod(1).eq(0)
    df = df.loc[valid_durations].copy()
    df["duration_seconds"] = numeric_durations.loc[valid_durations].astype("int64")

    df["timestamp"] = df["timestamp"].map(normalize_timestamp)
    df = df.dropna(subset=["timestamp"])

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DESTINATION, index=False)
    print(f"clean: {len(df)} rows -> {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
