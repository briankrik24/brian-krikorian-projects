"""
build_gold.py

Transforms the Silver dataset into an analytics-ready
Gold dataset by creating business metrics and
derived columns for reporting.
"""

"""
Gold Layer

Purpose:
- Preserve all Silver data
- Add business-friendly derived columns
- Create analytics-ready fields for SQL and Power BI
- Never overwrite existing Silver columns
"""

from pathlib import Path
import re

import pandas as pd


SILVER_FILE = Path("data/silver/games_clean.csv")
GOLD_FILE = Path("data/gold/games_gold.csv")


def load_silver():
    """Load the Silver dataset."""

    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            f"Silver dataset not found:\n{SILVER_FILE.resolve()}"
        )

    return pd.read_csv(
        SILVER_FILE,
        parse_dates=["release_date"]
    )


# ==================================================
# Time
# ==================================================

def add_time_columns(df):
    """Create release date derived columns."""

    df["release_year"] = df["release_date"].dt.year

    df["release_month"] = df["release_date"].dt.month

    df["release_month_name"] = (
        df["release_date"].dt.month_name()
    )

    df["release_decade"] = (
        (df["release_year"] // 10) * 10
    ).astype(str) + "s"

    return df


# ==================================================
# Price
# ==================================================

def price_bucket(price):
    """Categorize games into pricing tiers."""

    if price == 0:
        return "Free to Play"

    elif price < 10:
        return "Budget"

    elif price < 30:
        return "Mid-Range"

    elif price < 60:
        return "Premium"

    return "Deluxe"


def add_price_columns(df):
    """Create price-related derived columns."""

    df["is_free_to_play"] = (
        df["price"] == 0
    )

    df["price_bucket"] = (
        df["price"]
        .apply(price_bucket)
    )

    return df


# ==================================================
# Reviews
# ==================================================

def review_category(
    positive_review_percentage,
    total_reviews,
):
    """Assign review quality categories."""

    if total_reviews < 10:
        return "Insufficient Reviews"

    if positive_review_percentage >= 95:
        return "Exceptional"

    elif positive_review_percentage >= 90:
        return "Excellent"

    elif positive_review_percentage >= 80:
        return "Very Good"

    elif positive_review_percentage >= 70:
        return "Good"

    elif positive_review_percentage >= 50:
        return "Mixed"

    elif positive_review_percentage >= 30:
        return "Poor"

    return "Very Poor"


def add_review_columns(df):
    """Create review-related derived columns."""

    # Recalculate total reviews from raw counts
    df["total_reviews"] = (
        df["positive_reviews"] +
        df["negative_reviews"]
    )

    # Calculate positive review percentage
    df["positive_review_percentage"] = (
        df["positive_reviews"]
        / df["total_reviews"].replace(0, pd.NA)
    ) * 100

    df["positive_review_percentage"] = (
        df["positive_review_percentage"]
        .fillna(0)
        .round(1)
    )

    # Assign review category
    df["review_category"] = df.apply(
        lambda row: review_category(
            row["positive_review_percentage"],
            row["total_reviews"],
        ),
        axis=1,
    )

    return df


# ==================================================
# Estimated Owners
# ==================================================

def parse_owner_range(owner_range):
    """Split estimated owner ranges into numeric values."""

    if pd.isna(owner_range):
        return pd.Series(
            {
                "estimated_owner_min": None,
                "estimated_owner_max": None,
            }
        )

    numbers = re.findall(
        r"\d[\d,]*",
        owner_range,
    )

    if len(numbers) != 2:
        return pd.Series(
            {
                "estimated_owner_min": None,
                "estimated_owner_max": None,
            }
        )

    minimum = int(
        numbers[0].replace(",", "")
    )

    maximum = int(
        numbers[1].replace(",", "")
    )

    return pd.Series(
        {
            "estimated_owner_min": minimum,
            "estimated_owner_max": maximum,
        }
    )


def estimated_owner_bucket(midpoint):
    """Categorize games by estimated ownership."""

    if pd.isna(midpoint):
        return "Unknown"

    if midpoint < 10_000:
        return "Indie"

    elif midpoint < 100_000:
        return "Small"

    elif midpoint < 1_000_000:
        return "Medium"

    elif midpoint < 10_000_000:
        return "Large"

    return "Massive"


# ==================================================
# Estimated Owners
# ==================================================

def add_owner_columns(df):
    """Create ownership-related derived columns."""

    # Split owner ranges

    df[
        [
            "estimated_owner_min",
            "estimated_owner_max",
        ]
    ] = df["estimated_owners"].apply(
        parse_owner_range
    )

    # Midpoint

    df["estimated_owner_midpoint"] = (
        df["estimated_owner_min"]
        + df["estimated_owner_max"]
    ) / 2

    # Ownership bucket

    df["estimated_owner_bucket"] = (
        df["estimated_owner_midpoint"]
        .apply(estimated_owner_bucket)
    )

    return df


# ==================================================
# Playtime
# ==================================================

def playtime_bucket(hours):
    """Categorize games by average playtime."""

    if hours < 5:
        return "Very Casual"

    elif hours < 20:
        return "Casual"

    elif hours < 100:
        return "Dedicated"

    return "Hardcore"


def add_playtime_columns(df):
    """Create playtime-related derived columns."""

    # Convert minutes to hours

    df["average_playtime_hours"] = (
        df["average_playtime_forever"] / 60
    ).round(1)

    # Playtime bucket

    df["playtime_bucket"] = (
        df["average_playtime_hours"]
        .apply(playtime_bucket)
    )

    return df


# ==================================================
# Metadata
# ==================================================

def add_metadata_columns(df):
    """Create metadata-related derived columns."""

    df["has_metacritic"] = (
        df["metacritic_score"] > 0
    )

    df["has_achievements"] = (
        df["achievements"] > 0
    )

    return df


# ==================================================
# Validation
# ==================================================

def validate_dataset(df):
    """Validate the Gold dataset."""

    # -----------------------------
    # Data integrity
    # -----------------------------

    if df["appid"].duplicated().any():
        raise ValueError(
            "Duplicate App IDs detected."
        )

    if df["appid"].isnull().any():
        raise ValueError(
            "Missing App IDs detected."
        )

    if df["release_date"].isnull().any():
        raise ValueError(
            "Missing release dates detected."
        )

    # -----------------------------
    # Business rule validation
    # -----------------------------
    invalid_reviews = df[
        ~df["positive_review_percentage"].between(0, 100)
    ]

    if not invalid_reviews.empty:

        print("\nInvalid review percentages:")
        print(
            invalid_reviews[
                [
                    "appid",
                    "game_name",
                    "positive_reviews",
                    "negative_reviews",
                    "total_reviews",
                    "positive_review_percentage",
                ]
            ].head(10)
        )

        raise ValueError(
            f"{len(invalid_reviews)} games have invalid review percentages."
        )


    if (
        df["average_playtime_hours"] < 0
    ).any():

        raise ValueError(
            "Negative playtime hours detected."
        )

    if (
        df["estimated_owner_midpoint"] < 0
    ).any():

        raise ValueError(
            "Negative estimated owner midpoint detected."
        )

    print("\nGold dataset validation passed.")


# ==================================================
# Save
# ==================================================

def save_gold(df):
    """Save the Gold dataset."""

    GOLD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        GOLD_FILE,
        index=False,
    )

    print("\nGold dataset successfully saved.")
    print(f"Location: {GOLD_FILE.resolve()}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print(
        f"New Gold Columns: {len(df.columns) - 30}"
    )


# ==================================================
# Main
# ==================================================

def main():

    df = load_silver()

    df = add_time_columns(df)

    df = add_price_columns(df)

    df = add_review_columns(df)

    df = add_owner_columns(df)

    df = add_playtime_columns(df)

    df = add_metadata_columns(df)

    validate_dataset(df)

    save_gold(df)


if __name__ == "__main__":
    main()