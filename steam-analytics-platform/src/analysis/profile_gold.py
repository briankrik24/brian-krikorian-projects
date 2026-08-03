"""
profile_gold.py

Profiles the Gold dataset by validating derived business
metrics and summarizing the analytics-ready dataset.
"""

from pathlib import Path

import pandas as pd


GOLD_FILE = Path("data/gold/games_gold.csv")

EXPECTED_COLUMNS = 46
SILVER_COLUMNS = 30


def load_gold():
    """Load the Gold dataset."""

    if not GOLD_FILE.exists():
        raise FileNotFoundError(
            f"Gold dataset not found:\n{GOLD_FILE.resolve()}"
        )

    return pd.read_csv(
        GOLD_FILE,
        parse_dates=["release_date"]
    )


def dataset_overview(df):
    """Print basic dataset information."""

    print("=" * 50)
    print("Gold Layer Profile")
    print("=" * 50)

    print(f"Rows:    {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    memory = (
        df.memory_usage(deep=True).sum()
        / 1024 ** 2
    )

    print(f"Memory:  {memory:.1f} MB")

    print()
    print(f"Silver Columns: {SILVER_COLUMNS}")
    print(f"Gold Columns:   {EXPECTED_COLUMNS}")
    print(
        f"Derived Columns Added: "
        f"{len(df.columns) - SILVER_COLUMNS}"
    )

    print("\nColumn Types")
    print("-" * 50)

    type_counts = (
        df.dtypes
        .astype(str)
        .replace({
            "int64": "Integer",
            "float64": "Float",
            "bool": "Boolean",
            "object": "Object",
            "datetime64[ns]": "Datetime",
        })
        .value_counts()
    )

    print(type_counts.to_string())

    print("\nDuplicate App IDs")
    print("-" * 50)

    duplicates = df["appid"].duplicated().sum()

    print(
        f"{duplicates:,} duplicates "
        f"({duplicates / len(df):.2%})"
    )

    print("\nRelease Date Range")
    print("-" * 50)

    print(f"Earliest: {df['release_date'].min().date()}")
    print(f"Latest:   {df['release_date'].max().date()}")


def business_summary(df):
    """Print business-oriented summaries."""

    print("\nBusiness Metric Summary")
    print("=" * 50)

    print("\nPrice Buckets")
    print("-" * 50)
    print(
        df["price_bucket"]
        .value_counts()
        .to_string()
    )

    print("\nReview Categories")
    print("-" * 50)
    print(
        df["review_category"]
        .value_counts()
        .to_string()
    )

    print("\nEstimated Owner Buckets")
    print("-" * 50)
    print(
        df["estimated_owner_bucket"]
        .value_counts()
        .to_string()
    )

    print("\nPlaytime Buckets")
    print("-" * 50)
    print(
        df["playtime_bucket"]
        .value_counts()
        .to_string()
    )

    print("\nMetadata Summary")
    print("-" * 50)

    metacritic = df["has_metacritic"].sum()
    achievements = df["has_achievements"].sum()

    print(
        f"Games with Metacritic: "
        f"{metacritic:,} "
        f"({metacritic / len(df):.1%})"
    )

    print(
        f"Games with Achievements: "
        f"{achievements:,} "
        f"({achievements / len(df):.1%})"
    )


def key_metrics(df):
    """Print summary statistics."""

    print("\nKey Metrics Summary")
    print("-" * 50)

    columns = [
        "price",
        "positive_reviews",
        "negative_reviews",
        "total_reviews",
        "positive_review_percentage",
        "estimated_owner_midpoint",
        "average_playtime_hours",
    ]

    print(df[columns].describe())


def validate_gold(df):
    """Validate Gold transformations."""

    print("\nTransformation Validation")
    print("=" * 50)

    checks = {
        "Expected Column Count":
            len(df.columns) == EXPECTED_COLUMNS,

        "Duplicate App IDs":
            df["appid"].duplicated().sum() == 0,

        "Missing App IDs":
            df["appid"].isna().sum() == 0,

        "Review Percentage Valid":
            df["positive_review_percentage"].between(0, 100).all(),

        "Price Buckets Created":
            df["price_bucket"].notna().all(),

        "Review Categories Created":
            df["review_category"].notna().all(),

        "Owner Buckets Created":
            df["estimated_owner_bucket"].notna().all(),

        "Playtime Buckets Created":
            df["playtime_bucket"].notna().all(),

        "Metadata Flags Created":
            (
                df["has_metacritic"].notna().all()
                and
                df["has_achievements"].notna().all()
            ),

        "Release Dates Parsed":
            df["release_date"].notna().all(),
    }

    passed = 0

    for name, result in checks.items():

        status = "PASS" if result else "FAIL"

        print(
            f"{'✅' if result else '❌'} "
            f"{name:<30} {status}"
        )

        if result:
            passed += 1

    print("\nGold Health Summary")
    print("=" * 50)

    overall = (
        "HEALTHY ✅"
        if passed == len(checks)
        else "ISSUES FOUND ❌"
    )

    print(f"Overall Status: {overall}")
    print(f"Checks Passed:  {passed}/{len(checks)}")

    if passed == len(checks):
        print("\nGold Layer Ready for DuckDB ✅")


def top_games(df):
    """Display the most popular games."""

    print("\nTop 10 Most-Owned Games")
    print("-" * 50)

    top = (
        df[
            [
                "game_name",
                "estimated_owner_midpoint",
                "review_category",
            ]
        ]
        .sort_values(
            "estimated_owner_midpoint",
            ascending=False,
        )
        .head(10)
        .reset_index(drop=True)
    )

    for i, row in top.iterrows():

        owners = f"{row['estimated_owner_midpoint']:,.0f}"

        print(f"{i + 1:>2}. {row['game_name']}")
        print(f"    Estimated Owners: {owners}")
        print(f"    Reviews: {row['review_category']}")
        print()


def main():

    df = load_gold()

    dataset_overview(df)

    business_summary(df)

    key_metrics(df)

    validate_gold(df)

    top_games(df)


if __name__ == "__main__":
    main()