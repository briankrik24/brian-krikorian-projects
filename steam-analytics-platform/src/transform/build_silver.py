"""
build_silver.py

Transforms the Bronze dataset into the Silver layer by
cleaning, standardizing, and validating the source data.
"""

from pathlib import Path

import pandas as pd


BRONZE_FILE = Path("data/bronze/games_march2025_cleaned.csv")
SILVER_FILE = Path("data/silver/games_clean.csv")

SILVER_COLUMNS = [
    "appid",
    "name",
    "release_date",
    "required_age",
    "price",
    "dlc_count",
    "windows",
    "mac",
    "linux",
    "metacritic_score",
    "achievements",
    "recommendations",
    "developers",
    "publishers",
    "categories",
    "genres",
    "user_score",
    "positive",
    "negative",
    "estimated_owners",
    "average_playtime_forever",
    "average_playtime_2weeks",
    "median_playtime_forever",
    "median_playtime_2weeks",
    "discount",
    "peak_ccu",
    "pct_pos_total",
    "num_reviews_total",
    "pct_pos_recent",
    "num_reviews_recent",
]

COLUMN_RENAMES = {
    "name": "game_name",
    "positive": "positive_reviews",
    "negative": "negative_reviews",
    "pct_pos_total": "pct_positive_reviews",
    "num_reviews_total": "total_reviews",
    "pct_pos_recent": "pct_positive_recent",
    "num_reviews_recent": "recent_reviews",
}


def load_bronze():
    """Load the Bronze dataset."""

    if not BRONZE_FILE.exists():
        raise FileNotFoundError(
            f"Bronze dataset not found:\n{BRONZE_FILE.resolve()}"
        )

    return pd.read_csv(BRONZE_FILE)


def select_columns(df):
    """Keep only the columns defined in the Silver schema."""
    return df[SILVER_COLUMNS]


def rename_columns(df):
    """Rename columns for consistency."""
    return df.rename(columns=COLUMN_RENAMES)


def convert_data_types(df):
    """Convert columns to their appropriate data types."""

    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    return df


def validate_dataset(df):
    """Run validation checks before saving."""

    if df["appid"].duplicated().any():
        raise ValueError("Duplicate App IDs detected.")

    if df["appid"].isnull().any():
        raise ValueError("Missing App IDs detected.")

    print("Silver dataset validation passed.")

    if df["release_date"].isnull().any():
        print(
            f"Warning: {df['release_date'].isnull().sum()} release dates could not be parsed."
        )


def save_silver(df):
    """Save the Silver dataset."""

    SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(SILVER_FILE, index=False)

    print("\nSilver dataset successfully saved.")
    print(f"Location: {SILVER_FILE.resolve()}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


def main():
    df = load_bronze()

    df = select_columns(df)
    df = rename_columns(df)
    df = convert_data_types(df)

    # Keep output deterministic
    df = df.sort_values("appid").reset_index(drop=True)

    validate_dataset(df)

    save_silver(df)


if __name__ == "__main__":
    main()